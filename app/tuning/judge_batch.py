"""Batched vision judge: one MiMo call grades all selected outputs for one image.

Usage:
  python -I judge_batch.py --dry-run
  python -I judge_batch.py --variants A,B --langs English,Spanish --modes brief,rich,question
  python -I judge_batch.py --variants D --images 02,05

Why batched: judge.py makes one call per output; with ~250 outputs that does not fit the
~400 call budget. Here each call sees one image and up to --chunk outputs for it, in a
shuffled order with no model or variant names, and returns one score object per output.

Scale follows alt-text.md section 5 (0 to 2 per criterion):
  faithfulness, salience, people, text, calibration, ear; plus invented (true = hard fail).
For question mode: salience = direct answer first and the right kind of answer (answer,
I do not see it, or UNCLEAR); text = copied text correct when the question is about text.
Only records whose key ends with |t0 (thinking off, the NAS-like setting) are judged.
Writes results/judge_batch.jsonl, one line per output; the first line of each call carries
judge_attempts (the others 0) so the budget ledger in common.calls_logged stays exact.
"""
import argparse
import hashlib
import json
import random
import re
import sys
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (IMAGES, MODELS, RESULTS, THINKING_OFF, calls_logged, chat_retry,  # noqa: E402
                    extract, image_data_url, load_truth)

JUDGE_MODEL = "mimo"
VISIBLE = 2200
REASONING = 9000
CRITERIA = ["faithfulness", "salience", "people", "text", "calibration", "ear"]

RULES = {
    "brief": "Line 1: one sentence of at most 15 words, main subject and action first. Line 2: Words: "
             "then text copied exactly from the photo, or none.",
    "rich": "Line 1: one sentence of at most 15 words. Line 2: at most 2 short sentences on setting and "
            "details, front to back, plain colours, black and white or old print said when true. "
            "Line 3: Words: then copied text or none.",
    "question": "At most 2 short sentences, direct answer first, then one visible supporting detail. "
                "Thing asked about absent: say it is not seen. Photo cannot show the answer (name, who "
                "someone is, role such as groom or father, relationship, feeling, age, date, before or "
                "after): answer only UNCLEAR. Private item in the photo: only UNCLEAR, whatever the question.",
}

RUBRIC = """You are a strict reviewer of photo descriptions written for a listener who is blind.
You see the photo. Grade each OUTPUT below against the photo itself; the reference notes are a
hand-written aid and may be incomplete. All outputs are about this same photo.

Shared rules for every output: people are called only a baby, a child or an adult, with clothing,
position and visible action; never a name, gender word (man, woman, boy, girl, he, she, and the
same in Spanish), ethnicity, skin, body, looks, age in years, religion, health, relationship
(mother, groom, family) or feeling. A private item (ID card, bank card, medical paper or scene,
screen with personal data, bare body) gets only Not described plus a short reason (descriptions)
or only UNCLEAR (questions). No lead-in such as this photo shows. Required output language is
given per item; the labels Line 1, Line 2, Line 3, Words, none, Not described and UNCLEAR stay
in English by design and are not a language error.

Score each criterion 0, 1 or 2:
- faithfulness: 2 = every object, count, colour, position and action is really there;
  1 = one minor slip; 0 = a major error or anything invented.
- salience: 2 = main subject and action first, general before specific (questions: the direct
  answer first and the right kind of answer); 1 = buried or partly off; 0 = misses the point,
  or a refusal on an ordinary photo or answerable question.
- people: 2 = people handled by the rules above, or no people involved; 1 = life stage or
  clothing missing where it matters; 0 = any identity, gender, role, relationship or feeling guess.
- text: 2 = copied text exact, or none correctly when there is no main text, or a correct
  refusal; 1 = small errors or missed part; 0 = invented, translated or badly wrong text.
- calibration: 2 = dark or blurred flagged, hedges at most once and only on unclear details,
  no confident claims about things that cannot be seen; 1 = small overclaim; 0 = confident wrong claim.
- ear: 2 = heard on a screen reader, a blind listener could picture this photo and tell it
  apart from others; 1 = vague or clumsy; 0 = useless or confusing. A correct Not described
  or UNCLEAR on a private item or unanswerable question scores 2.
Also set invented to true if the output mentions any object, person, animal or text that is
not in the photo.

Reference notes (may be incomplete): {notes}

{items}

Answer with one JSON array only, no other text, one object per output in the same order:
[{{"id": 1, "faithfulness": n, "salience": n, "people": n, "text": n, "calibration": n,
"ear": n, "invented": true or false, "reason": "at most 20 words"}}, ...]"""


def notes_for(truth):
    parts = [f"scene: {truth['scene']}", f"people: {truth['people']}"]
    parts.append("main readable text: " + (" / ".join(truth["words"]) if truth["words"] else "none important"))
    if truth.get("minor_text_ok"):
        parts.append("small incidental text (plates, logos, stamps) may also be present")
    if truth.get("sensitive"):
        parts.append("this is a private item: the correct output is Not described or UNCLEAR")
    if truth.get("dark_or_blurry"):
        parts.append("the photo is too dark and blurred: the output must say so")
    if truth.get("bw_or_old"):
        parts.append("black and white or old print")
    return "; ".join(parts)


def item_block(i, rec):
    head = f"OUTPUT {i}. Mode: {rec['mode']}. Required language: {rec['language']}. Rules: {RULES[rec['mode']]}"
    if rec["mode"] == "question":
        head += f"\nQuestion asked: {rec['question']} (type: {rec['question_kind']}; expected: {rec['question_expect']})"
    return head + "\n<<<\n" + (rec["content"] or "").strip() + "\n>>>"


def parse(text, n):
    if not text:
        return None
    m = re.search(r"\[.*\]", text, re.S)
    if not m:
        return None
    try:
        arr = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    out = {}
    for d in arr:
        try:
            i = int(d["id"])
            s = {c: int(d[c]) for c in CRITERIA}
            if not all(0 <= v <= 2 for v in s.values()):
                continue
            s["invented"] = bool(d.get("invented"))
            s["reason"] = str(d.get("reason", ""))[:200]
            out[i] = s
        except (KeyError, TypeError, ValueError):
            continue
    return out if len(out) == n else None


def judge_chunk(image, recs, truth):
    items = "\n\n".join(item_block(i + 1, r) for i, r in enumerate(recs))
    prompt = RUBRIC.format(notes=notes_for(truth), items=items)
    messages = [{"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": image_data_url(IMAGES / image)}},
        {"type": "text", "text": prompt},
    ]}]
    calls, scores, thinking_used, errors = 0, None, None, []
    for thinking in (True, False):
        extra = None if thinking else THINKING_OFF
        budget = VISIBLE + (REASONING if thinking else 0)
        r = chat_retry(MODELS[JUDGE_MODEL], messages, 0.0, budget, extra=extra)
        calls += r["attempts"]
        errors += r["errors"]
        e = extract(r["response"])
        scores = parse(e["content"], len(recs))
        thinking_used = thinking
        if scores:
            break
    rows = []
    for i, rec in enumerate(recs):
        rows.append({
            "key": rec["key"], "image": image, "model": rec["model"], "variant": rec["variant"],
            "mode": rec["mode"], "language": rec["language"], "question_kind": rec.get("question_kind"),
            "judge_model": MODELS[JUDGE_MODEL], "judge_thinking": thinking_used,
            "judge_attempts": calls if i == 0 else 0, "batch_size": len(recs),
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "ok": scores is not None,
            "scores": scores.get(i + 1) if scores else None, "errors": errors if i == 0 else [],
            "content_sha1": hashlib.sha1(rec["content"].encode("utf-8")).hexdigest()[:12],
        })
    return rows


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(RESULTS / "raw.jsonl"))
    ap.add_argument("--out", default=str(RESULTS / "judge_batch.jsonl"))
    ap.add_argument("--images", default="all")
    ap.add_argument("--variants", default="A,B")
    ap.add_argument("--modes", default="brief,rich,question")
    ap.add_argument("--models", default="mimo,nemotron")
    ap.add_argument("--langs", default="English,Spanish")
    ap.add_argument("--chunk", type=int, default=14)
    ap.add_argument("--max-calls", type=int, default=400)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sel = {n: set(getattr(args, n).split(",")) for n in ("variants", "modes", "models", "langs")}
    truth_all = load_truth()
    latest = {}
    for line in Path(args.raw).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            latest[rec["key"]] = rec
    out = Path(args.out)
    judged = set()
    if out.exists():
        for line in out.read_text(encoding="utf-8").splitlines():
            if line.strip():
                j = json.loads(line)
                if j.get("ok"):
                    judged.add(j["key"])
    wanted = None if args.images == "all" else [s.strip() for s in args.images.split(",")]
    by_image = defaultdict(list)
    for rec in latest.values():
        if not rec["key"].endswith("|t0") or rec["key"] in judged:
            continue
        if wanted and not any(rec["image"].startswith(w) for w in wanted):
            continue
        if (rec["variant"] not in sel["variants"] or rec["mode"] not in sel["modes"]
                or rec["model"] not in sel["models"] or rec["language"] not in sel["langs"]):
            continue
        if not (rec.get("content") or "").strip() or rec.get("finish_reason") == "length":
            continue
        by_image[rec["image"]].append(rec)
    chunks = []
    for image, recs in sorted(by_image.items()):
        random.Random(image).shuffle(recs)
        for s in range(0, len(recs), args.chunk):
            chunks.append((image, recs[s:s + args.chunk]))
    used = calls_logged()
    print(f"outputs to judge {sum(len(c[1]) for c in chunks)} in {len(chunks)} calls; "
          f"attempts logged {used}; budget {args.max_calls}")
    if args.dry_run:
        return
    if used + len(chunks) > args.max_calls:
        sys.exit("over budget: narrow the selection or raise --max-calls")
    lock = threading.Lock()

    def work(ch):
        image, recs = ch
        rows = judge_chunk(image, recs, truth_all[image])
        with lock, open(out, "a", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(("ok " if rows[0]["ok"] else "FAIL ") + image + f" n={len(recs)} calls={rows[0]['judge_attempts']}"
              f" thinking={rows[0]['judge_thinking']}", flush=True)

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        list(ex.map(work, chunks))


if __name__ == "__main__":
    main()
