"""Tuning bench: send the Album Out Loud vision prompts to the cloud stand-in models.

Usage examples (run from anywhere; paths are resolved from this file):
  python -I bench.py --dry-run
  python -I bench.py --images 12,13 --variants A,B,C --modes brief,rich,question --langs English
  python -I bench.py --images all --variants A,B --modes brief --models nemotron --runs 3

Prompts come from prompts/{variant}_{mode}.txt. Placeholders: {language}, {question}, {album}.
Each call uses temperature 0.2 and the mode budget (brief 90, rich 170, question 80).
Both endpoints can reason. Models listed in --think (default: mimo) run with thinking on and get
REASONING_EXTRA tokens on top of the mode budget; the others run with thinking off, so they
honour the mode budget like the NAS model. Extra tokens and reasoning tokens are recorded.
Records with empty or truncated content are not counted as done and are re-run on the next call;
consumers use the latest record per key.
Every call is retried once on error. Raw outputs are appended to results/raw.jsonl; a record
that already exists (same key) is skipped, so runs can resume.
Images go only to the cloud tuning API; only CC0, public-domain or synthetic images live in images/.
"""
import argparse
import hashlib
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (IMAGES, MODELS, PROMPTS, REASONING_EXTRA, RESULTS, THINKING_OFF,  # noqa: E402
                    calls_logged, chat_retry, extract, image_data_url, load_truth)

TEMPERATURE = 0.2
MODE_TOKENS = {"brief": 90, "rich": 170, "question": 80}
MAX_RECORDS = 2  # at most 2 records (each with up to 2 attempts) per key


def load_prompts(variants, modes):
    prompts = {}
    for v in variants:
        for m in modes:
            p = PROMPTS / f"{v}_{m}.txt"
            prompts[(v, m)] = p.read_text(encoding="utf-8").strip()
    # C must be B plus one context sentence; warn if they drifted apart.
    for m in modes:
        if ("B", m) in prompts and ("C", m) in prompts and prompts[("B", m)] not in prompts[("C", m)]:
            print(f"WARNING: C_{m}.txt no longer contains B_{m}.txt")
    return prompts


def fill(template, language, question=None, album=None):
    text = template.replace("{language}", language)
    if question is not None:
        text = text.replace("{question}", question)
    if album is not None:
        text = text.replace("{album}", album)
    if "{" in text or "}" in text:
        raise ValueError("unfilled placeholder in prompt: " + text[:80])
    return text


def plan_jobs(args, truth, prompts):
    names = sorted(k for k in truth if not k.startswith("_"))
    if args.images != "all":
        wanted = [s.strip() for s in args.images.split(",")]
        names = [n for n in names if any(n.startswith(w) for w in wanted)]
    jobs = []
    for img in names:
        t = truth[img]
        for model in args.models:
            for lang in args.langs:
                for v in args.variants:
                    for mode in args.modes:
                        album = t.get("album") if v == "C" else None
                        qs = t["questions"] if mode == "question" else [None]
                        for qi, q in enumerate(qs):
                            if q is not None and args.pairs and f"{img[:2]}:{qi}" not in args.pairs:
                                continue
                            for run in range(1, args.runs + 1):
                                qtext = None
                                if q is not None:
                                    qtext = q["q_es"] if lang == "Spanish" else q["q"]
                                prompt = fill(prompts[(v, mode)], lang, qtext, album)
                                think = model in args.think
                                key = (f"{img}|{model}|{lang}|{v}|{mode}|q{qi if q else '-'}|r{run}"
                                       f"|t{int(think)}")
                                jobs.append({
                                    "key": key, "image": img, "model": model, "language": lang,
                                    "variant": v, "mode": mode, "run": run,
                                    "question_index": qi if q else None,
                                    "question": qtext, "question_kind": q["kind"] if q else None,
                                    "question_expect": q["expect"] if q else None,
                                    "album": album, "prompt": prompt, "thinking": think,
                                })
    return jobs


def run_job(job, args):
    model = job["model"]
    budget = MODE_TOKENS[job["mode"]]
    thinking = job["thinking"]
    extra_tokens = REASONING_EXTRA[model] if thinking else 0
    extra_body = None if thinking else THINKING_OFF
    messages = [{"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": image_data_url(IMAGES / job["image"])}},
        {"type": "text", "text": job["prompt"]},
    ]}]
    r = chat_retry(MODELS[model], messages, TEMPERATURE, budget + extra_tokens, extra=extra_body)
    e = extract(r["response"])
    usage = e["usage"] or {}
    reasoning_tokens = ((usage.get("completion_tokens_details") or {}).get("reasoning_tokens")) or 0
    completion = usage.get("completion_tokens")
    visible = (completion - reasoning_tokens) if completion is not None else None
    rec = {k: v for k, v in job.items() if k != "prompt"}
    rec.update({
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "model_id": MODELS[model],
        "prompt_sha1": hashlib.sha1(job["prompt"].encode("utf-8")).hexdigest()[:12],
        "prompt_words": len(job["prompt"].split()),
        "temperature": TEMPERATURE,
        "max_tokens_mode": budget,
        "extra_reasoning_tokens": extra_tokens,
        "max_tokens_sent": budget + extra_tokens,
        "ok": r["ok"], "attempts": r["attempts"], "errors": r["errors"], "seconds": r["seconds"],
        "content": e["content"], "finish_reason": e["finish_reason"],
        "reasoning_chars": e["reasoning_chars"], "reasoning_tokens": reasoning_tokens,
        "completion_tokens": completion, "visible_tokens": visible,
        "over_mode_budget": (visible is not None and visible > budget),
        "usage": usage,
    })
    return rec


def is_complete(rec):
    """A record counts as done when the call worked and returned visible, untruncated text."""
    return bool(rec.get("ok") and (rec.get("content") or "").strip() and rec.get("finish_reason") != "length")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", default="all", help="comma list of file prefixes, or all")
    ap.add_argument("--variants", default="A,B,C")
    ap.add_argument("--modes", default="brief,rich,question")
    ap.add_argument("--models", default="mimo,nemotron")
    ap.add_argument("--langs", default="English,Spanish")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--out", default=str(RESULTS / "raw.jsonl"))
    ap.add_argument("--max-calls", type=int, default=400, help="budget for all API attempts logged in --out plus this run")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--think", default="mimo",
                    help="comma list of models that run with thinking on (others get thinking off)")
    ap.add_argument("--pairs", default="", help="question mode only: comma list of image:question, e.g. 12:0,22:1")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    for name in ("variants", "modes", "models", "langs", "think", "pairs"):
        setattr(args, name, [s.strip() for s in getattr(args, name).split(",") if s.strip()])

    truth = load_truth()
    prompts = load_prompts(args.variants, args.modes)
    jobs = plan_jobs(args, truth, prompts)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done, used, tries = set(), 0, {}
    if out.exists():
        for line in out.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                used += rec.get("attempts", 1)
                tries[rec["key"]] = tries.get(rec["key"], 0) + 1
                if is_complete(rec):
                    done.add(rec["key"])
    # A key that already failed MAX_RECORDS times (for example a reasoning loop that hits the
    # token limit every time) is given up and left as a failure for checks.py to count.
    given_up = [j for j in jobs if j["key"] not in done and tries.get(j["key"], 0) >= MAX_RECORDS]
    if given_up:
        print(f"given up after {MAX_RECORDS} records: {len(given_up)} keys")
    todo = [j for j in jobs if j["key"] not in done and tries.get(j["key"], 0) < MAX_RECORDS]
    n_done = sum(1 for j in jobs if j["key"] in done)
    print(f"planned {len(jobs)}, already done {n_done}, given up {len(given_up)}, to run {len(todo)}; "
          f"attempts already logged {used}, budget {args.max_calls}")
    used = max(used, calls_logged())
    print(f"all attempts logged (bench + judges): {used}")
    if args.dry_run:
        return
    if used + len(todo) > args.max_calls:
        sys.exit("over budget: narrow the selection or raise --max-calls")

    lock = threading.Lock()

    def work(job):
        rec = run_job(job, args)
        with lock, open(out, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        status = "ok" if rec["ok"] else "FAIL"
        print(f"{status} {rec['key']} {rec['seconds']}s vis={rec['visible_tokens']} "
              f"reason={rec['reasoning_tokens']} fin={rec['finish_reason']}", flush=True)

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        list(ex.map(work, todo))


if __name__ == "__main__":
    main()
