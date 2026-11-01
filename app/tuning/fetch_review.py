"""Reviewer check: fetch a few CC0 / public-domain candidates for privacy-gate edge cases.
Usage: uv run --with pillow python -I fetch_review.py <outdir>
Reuses search() from fetch_candidates.py. Files are re-encoded as JPEG (image data only)."""
import io, json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_candidates import search, get_bytes  # noqa: E402
from PIL import Image  # noqa: E402

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
Q = {"hospital": ["patient hospital bed", "hospital patient visit"],
     "swim": ["bathing beauties beach", "swimsuit beach adults"]}
index = {}
for cat, qs in Q.items():
    got = []
    for q in qs:
        for t in ["CC-zero", "PD-self", "PD-USGov-Military", "PD-USGov", "PD-old"]:
            if len(got) >= 4: break
            try: hits = search(q, t, limit=6)
            except Exception as e: print("fail", q, t, e); continue
            for h in hits:
                if len(got) < 4 and h["title"] not in [g["title"] for g in got]: got.append(h)
            time.sleep(2)
    for n, h in enumerate(got, 1):
        name = f"{cat}_{n}.jpg"
        try:
            im = Image.open(io.BytesIO(get_bytes(h["thumb_url"]))).convert("RGB")
            im.thumbnail((1024, 1024)); im.save(out / name, "JPEG", quality=88)
            h["file"] = name; index[name] = h
            print("ok", name, h["licence"], h["title"][:80].encode("ascii", "replace").decode())
        except Exception as e: print("dl fail", name, e)
        time.sleep(2)
(out / "candidates.json").write_text(json.dumps(index, indent=1, ensure_ascii=False), "utf-8")
