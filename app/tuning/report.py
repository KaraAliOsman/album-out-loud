"""Merge checks.jsonl and judge_batch.jsonl for thinking-off records (|t0) into tables.

Usage: python -I report.py [--by model,variant,mode,language] [--variants A,B,D] [--images 02,05]
Prints a Markdown table: n, deterministic pass rate, top hard flags, judge means (0 to 2) and
invented count. Run checks.py first.
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CRIT = ["faithfulness", "salience", "people", "text", "calibration", "ear"]


def load():
    checks = {}
    for line in (ROOT / "results" / "checks.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r["key"].endswith("|t0"):
            checks[r["key"]] = r
    judge = {}
    jf = ROOT / "results" / "judge_batch.jsonl"
    if jf.exists():
        for line in jf.read_text(encoding="utf-8").splitlines():
            j = json.loads(line)
            if j.get("ok") and j.get("scores"):
                judge[j["key"]] = j["scores"]
    return checks, judge


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--by", default="model,variant,mode,language")
    ap.add_argument("--variants", default="")
    ap.add_argument("--images", default="")
    ap.add_argument("--models", default="")
    ap.add_argument("--flags", type=int, default=3)
    args = ap.parse_args()
    by = args.by.split(",")
    checks, judge = load()
    groups = defaultdict(list)
    for k, r in checks.items():
        if args.variants and r["variant"] not in args.variants.split(","):
            continue
        if args.models and r["model"] not in args.models.split(","):
            continue
        if args.images and not any(r["image"].startswith(i) for i in args.images.split(",")):
            continue
        groups[tuple(r[b] for b in by)].append(r)
    print("| " + " | ".join(by) + " | n | pass | top hard flags | judged | " + " | ".join(c[:5] for c in CRIT) + " | invented |")
    print("|" + "---|" * (len(by) + 5 + len(CRIT)))
    for g in sorted(groups):
        rs = groups[g]
        n = len(rs)
        p = sum(r["pass"] for r in rs)
        fl = Counter(h for r in rs for h in r["hard"])
        top = ", ".join(f"{a} {b}" for a, b in fl.most_common(args.flags)) or "none"
        js = [judge[r["key"]] for r in rs if r["key"] in judge]
        means = [f"{sum(j[c] for j in js) / len(js):.2f}" if js else "-" for c in CRIT]
        inv = sum(j["invented"] for j in js)
        print(f"| {' | '.join(g)} | {n} | {p}/{n} ({100 * p / n:.0f}%) | {top} | {len(js)} | {' | '.join(means)} | {inv} |")


if __name__ == "__main__":
    main()
