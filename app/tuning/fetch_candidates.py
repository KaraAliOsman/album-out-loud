"""Fetch candidate CC0 / public-domain images from Wikimedia Commons.

Usage: python -I fetch_candidates.py <candidates_dir> [category ...]
Writes <candidates_dir>/<category>_<n>.jpg plus <candidates_dir>/candidates.json.
Only files whose Commons licence is CC0 or Public domain are kept.
Downloaded files are treated as image data only (re-encoded with Pillow).
"""
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

UA = "AlbumOutLoudTuning/0.1 (accessibility prompt research; non-commercial)"
API = "https://commons.wikimedia.org/w/api.php"
OK_LICENCES = {"cc0", "public domain", "pdm", "pd"}

# category -> list of search queries (tried in order until enough hits)
QUERIES = {
    "party": ["birthday party children", "birthday party family"],
    "picnic": ["family picnic", "picnic people park"],
    "graduation": ["graduation ceremony graduates", "graduation family"],
    "wedding": ["wedding guests", "wedding couple family"],
    "playground": ["children playground", "playground kids"],
    "kitchen": ["family cooking kitchen", "people cooking kitchen"],
    "beach": ["family beach", "people beach children"],
    "table": ["family dinner table", "family meal"],
    "baby": ["baby on lap", "mother baby"],
    "elder": ["grandmother grandchild", "elderly woman"],
    "cake": ["happy birthday cake", "birthday cake writing"],
    "banner": ["welcome banner", "happy birthday banner"],
    "streetsign": ["calle street sign", "street name sign"],
    "shopsign": ["shop sign storefront", "bakery storefront"],
    "tshirt": ["t-shirt slogan", "t-shirt text"],
    "bw": ["old family photograph", "vintage family portrait", "family photograph 1920s"],
    "dog": ["dog garden", "dog"],
    "cat": ["cat sofa", "cat"],
    "landscape": ["mountain lake landscape", "landscape valley"],
    "food": ["plate of food", "pasta dish"],
    "party2": ["children birthday party balloons", "birthday party kids cake candles", "family celebration party"],
    "playground2": ["children playing playground swing", "kids slide playground playing"],
    "calle": ["calle sign Spain", "nombre de calle placa"],
    "playground3": ["children playing park", "kids playing outdoors"],
}
TEMPLATES = ["CC-zero", "PD-self", "PD-old"]


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def get_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def search(query, template, limit=8):
    params = {
        "action": "query", "generator": "search", "format": "json",
        "gsrsearch": f"{query} filetype:bitmap hastemplate:{template}",
        "gsrnamespace": "6", "gsrlimit": str(limit),
        "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime",
        "iiurlwidth": "1024",
        "iiextmetadatafilter": "LicenseShortName|Artist|License|ImageDescription",
    }
    data = get_json(API + "?" + urllib.parse.urlencode(params))
    pages = data.get("query", {}).get("pages", {})
    out = []
    for p in sorted(pages.values(), key=lambda x: x.get("index", 0)):
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        lic = strip_html(em.get("LicenseShortName", {}).get("value", ""))
        if lic.lower() not in OK_LICENCES and not lic.lower().startswith("public domain"):
            continue
        if ii.get("mime") not in ("image/jpeg", "image/png"):
            continue
        out.append({
            "title": p["title"],
            "page_url": ii.get("descriptionurl"),
            "thumb_url": ii.get("thumburl"),
            "licence": lic,
            "author": strip_html(em.get("Artist", {}).get("value", ""))[:120],
            "description": strip_html(em.get("ImageDescription", {}).get("value", ""))[:200],
        })
    return out


def main():
    time.sleep(60)
    cdir = Path(sys.argv[1])
    cdir.mkdir(parents=True, exist_ok=True)
    cats = sys.argv[2:] or list(QUERIES)
    index_path = cdir / "candidates.json"
    index = json.loads(index_path.read_text("utf-8")) if index_path.exists() else {}
    per_cat = 6
    for cat in cats:
        got = []
        seen = set()
        for q in QUERIES[cat]:
            for t in TEMPLATES:
                if len(got) >= per_cat:
                    break
                try:
                    hits = search(q, t)
                except Exception as e:  # network hiccup
                    print("search failed", cat, q, t, e)
                    continue
                for h in hits:
                    if h["title"] in seen or len(got) >= per_cat:
                        continue
                    seen.add(h["title"])
                    got.append(h)
                time.sleep(2.5)
        for n, h in enumerate(got, 1):
            name = f"{cat}_{n}.jpg"
            try:
                raw = get_bytes(h["thumb_url"])
                im = Image.open(io.BytesIO(raw))
                im = im.convert("RGB")
                im.thumbnail((1024, 1024))
                im.save(cdir / name, "JPEG", quality=88)
                h["file"] = name
                index[name] = h
                print("ok", name, h["licence"], h["title"][:70].encode("ascii","replace").decode())
            except Exception as e:
                print("download failed", name, e)
            time.sleep(2.0)
        index_path.write_text(json.dumps(index, indent=1, ensure_ascii=False), "utf-8")


if __name__ == "__main__":
    main()
