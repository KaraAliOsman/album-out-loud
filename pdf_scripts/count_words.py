import re, sys
src = open(sys.argv[1], encoding="utf-8").read()
body = src.split("<!-- answers start -->")[1].split("<!-- answers end -->")[0]
per = {}
cur = None
for line in body.splitlines():
    s = line.strip()
    if s.startswith("## "):
        cur = s[3:].split(".")[0]; per[cur] = 0; continue
    if not s or s.startswith("[[") or re.fullmatch(r"\|[-| ]+\|", s):
        continue
    s = s.lstrip("-").replace("|", " ")
    toks = [t for t in s.split() if re.search(r"[A-Za-z0-9]", t)]
    per[cur] += len(toks)
total = sum(per.values())
print(per, "TOTAL", total)
if len(sys.argv) > 2 and sys.argv[2] == "--write":
    new = re.sub(r"<!-- WORDCOUNT[^>]*-->", f"<!-- WORDCOUNT: ten answers = {total} English words (pdf_scripts/count_words.py: whitespace tokens with a letter or digit, Q5 table cells included, question headings excluded) -->", src, count=1)
    open(sys.argv[1], "w", encoding="utf-8", newline="\n").write(new)
