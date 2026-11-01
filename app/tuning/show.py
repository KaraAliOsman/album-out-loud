"""Print failing (or all) checked records. Usage: python -I show.py [--all] [--filter substr,...] [--mode m]"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent
args = sys.argv[1:]
show_all = "--all" in args
flt = []
if "--filter" in args:
    flt = args[args.index("--filter") + 1].split(",")
raw = {}
for line in (ROOT / "results" / "raw.jsonl").read_text(encoding="utf-8").splitlines():
    if line.strip():
        r = json.loads(line)
        raw[r["key"]] = r
for line in (ROOT / "results" / "checks.jsonl").read_text(encoding="utf-8").splitlines():
    r = json.loads(line)
    if not all(f in r["key"] for f in flt):
        continue
    if not show_all and r["pass"]:
        continue
    x = raw[r["key"]]
    print("#", r["key"].replace(".jpg", ""), r["hard"], r["soft"], x["finish_reason"], x["visible_tokens"])
    if x.get("question"):
        print("   Q:", x["question"])
    print("   ", (r["content"] or "").replace("\n", " / ")[:400])
