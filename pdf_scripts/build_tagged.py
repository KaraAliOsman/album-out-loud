import re, sys, base64, html
import markdown
src, fig, out_html = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src, encoding="utf-8").read()
s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
img = base64.b64encode(open(fig, "rb").read()).decode()
alt = ("Flow diagram. Letter mode: the helper asks; 1 find album (photo-agent); 2 last letter, since mode only (file-agent); "
       "3 choose photos (photo-agent); 4 describe with vision-vlm and vision-ocr (photo-agent); 5 whole letter shown in chat, "
       "family notes by photo number; the helper says save, the one approval; 6 free file name (file-agent); 7 save letter "
       "(knowledge-agent save-text); 8 read back (file-agent); the listener hears it with a screen reader. Question mode Q1 to Q3: "
       "family notes first, otherwise the question is kept for the family. Next month: photos since the last letter, plus family answers.")
fig_html = (f'<figure><img src="data:image/png;base64,{img}" alt="{html.escape(alt)}">'
            '<figcaption>Figure: letter mode (steps 1 to 8) and question mode (Q1 to Q3), with the one approval of a letter.</figcaption></figure>')
parts = s.split("[[FIGURE]]")
LEADS = ["Done:", "Not done:", "Core 1:", "Core 2:", "Edge:", "Pass:", "Helper:", "Next month:", "Unknown:", "Entrant:", "Signature:", "Date:", "Dry run,", "Inputs:",
         "Third-party components and open source libraries:", "Platform:", "Run time:", "AI tools used to build it:", "Guidance read and paraphrased, nothing copied:", "Test data:"]
def prep(t):
    t = re.sub(r"_{3,}", lambda m: "\_" * 18, t)
    return t
def bold(h):
    for e in sorted(LEADS, key=len, reverse=True):
        h = h.replace(e, f"<strong>{e}</strong>")
    return h
parts = [prep(x) for x in parts]
body = markdown.markdown(parts[0], extensions=["tables"]) + fig_html + (markdown.markdown(parts[1], extensions=["tables"]) if len(parts) > 1 else "")
css = """
@page { size: A4; margin: 1.6cm 1.7cm 1.6cm 1.7cm; }
body { font-family: 'Segoe UI', Calibri, Arial, sans-serif; font-size: 9.6pt; line-height: 1.34; color: #1d2430; }
h1 { font-size: 20pt; color: #1f4e79; margin: 0 0 2pt 0; }
h1 + p { color: #5a6472; margin-top: 0; }
h2 { font-size: 11pt; color: #1f4e79; margin: 9pt 0 2pt 0; }
h3 { font-size: 10.5pt; color: #1f4e79; margin: 10pt 0 2pt 0; }
p { margin: 2pt 0 4pt 0; }
ul { margin: 2pt 0 4pt 0; padding-left: 16pt; }
li { margin: 1pt 0; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 4pt 0 6pt 0; }
th { background: #2f5d8a; color: white; text-align: left; padding: 3pt 5pt; }
td { border-bottom: 1px solid #c9d1dc; padding: 3pt 5pt; vertical-align: top; }
tr:last-child td { background: #e6f2ef; }
figure { margin: 6pt 0; }
figure img { width: 100%; }
figcaption { font-size: 8.5pt; color: #5a6472; font-style: italic; }
"""
body = bold(body)
doc = f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Album Out Loud: Round 1 proposal, UGREEN Hackathon 2026 on AI NAS</title><style>{css}</style></head><body>{body}</body></html>'
open(out_html, "w", encoding="utf-8").write(doc)
print("html ok")
