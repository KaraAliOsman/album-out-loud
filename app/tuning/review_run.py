"""Reviewer independent check on Nemotron only (thinking off, temperature 0.2, mode token budget).
Usage: python -I review_run.py jobs.json   -> appends to results/review_nemotron.jsonl
Job: [variant, mode, language, image, question_or_null]. Variant F means prompts/final_*.txt."""
import json, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import IMAGES, MODELS, PROMPTS, RESULTS, THINKING_OFF, chat_retry, extract, image_data_url  # noqa
sys.stdout.reconfigure(encoding="utf-8")
TOK = {"brief": 90, "rich": 170, "question": 80}
OUT = RESULTS / "review_nemotron.jsonl"
def run(job):
    v, mode, lang, img, q = job
    name = "final" if v == "F" else v
    t = (PROMPTS / f"{name}_{mode}.txt").read_text("utf-8").strip().replace("{language}", lang)
    if q: t = t.replace("{question}", q)
    msgs = [{"role": "user", "content": [{"type": "text", "text": t},
             {"type": "image_url", "image_url": {"url": image_data_url(IMAGES / img)}}]}]
    res = chat_retry(MODELS["nemotron"], msgs, 0.2, TOK[mode], extra=THINKING_OFF)
    ex = extract(res["response"])
    rec = {"variant": v, "mode": mode, "language": lang, "image": img, "question": q,
           "ok": res["ok"], "attempts": res["attempts"], "content": ex["content"],
           "finish_reason": ex["finish_reason"], "usage": ex["usage"], "errors": res["errors"]}
    return rec
jobs = json.loads(Path(sys.argv[1]).read_text("utf-8"))
with ThreadPoolExecutor(4) as pool:
    recs = list(pool.map(run, jobs))
with OUT.open("a", encoding="utf-8") as f:
    for r in recs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
for r in recs:
    print("##", r["variant"], r["mode"], r["language"], r["image"][:24], r["question"] or "", "| fin", r["finish_reason"], "att", r["attempts"])
    print(r["content"])
print("attempts:", sum(r["attempts"] for r in recs))
