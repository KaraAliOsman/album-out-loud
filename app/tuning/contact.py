"""Make labelled contact sheets from a folder of jpgs.

Usage: python -I contact.py <image_dir> <out_dir> [prefix ...]
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
prefixes = sys.argv[3:]
files = sorted(p for p in src.glob("*.jpg") if not prefixes or p.name.split("_")[0] in prefixes)
W, H, COLS, PER = 400, 300, 6, 24
for s in range(0, len(files), PER):
    chunk = files[s:s + PER]
    rows = (len(chunk) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * W, rows * (H + 24)), "white")
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(chunk):
        im = Image.open(f).convert("RGB")
        im.thumbnail((W - 4, H - 4))
        x, y = (i % COLS) * W, (i // COLS) * (H + 24)
        sheet.paste(im, (x + 2, y + 2))
        d.text((x + 4, y + H + 4), f.name, fill="black")
    sheet.save(out / f"sheet_{s // PER + 1}.jpg", quality=80)
    print(out / f"sheet_{s // PER + 1}.jpg", [f.name for f in chunk])
