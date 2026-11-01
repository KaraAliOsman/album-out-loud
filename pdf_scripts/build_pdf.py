import re, sys
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Image, ListFlowable, ListItem, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

src, fig, out = sys.argv[1], sys.argv[2], sys.argv[3]
F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("Body", F + "calibri.ttf"))
pdfmetrics.registerFont(TTFont("Body-Bold", F + "calibrib.ttf"))
pdfmetrics.registerFont(TTFont("Body-Italic", F + "calibrii.ttf"))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-Italic", boldItalic="Body-Bold")

INK = colors.HexColor("#1F2A36"); ACC = colors.HexColor("#2F5D8A"); MUTED = colors.HexColor("#5A6470")
body = ParagraphStyle("b", fontName="Body", fontSize=10, leading=12.6, textColor=INK, spaceAfter=3)
small = ParagraphStyle("s", parent=body, fontSize=8.9, leading=11.0, spaceAfter=2)
h1 = ParagraphStyle("h1", fontName="Body-Bold", fontSize=19, leading=22, textColor=ACC, spaceAfter=1)
sub = ParagraphStyle("sub", parent=body, fontSize=10, textColor=MUTED, spaceAfter=6)
h2 = ParagraphStyle("h2", keepWithNext=1, fontName="Body-Bold", fontSize=10.6, leading=13, textColor=ACC, spaceBefore=6, spaceAfter=2)
cell = ParagraphStyle("c", parent=body, fontSize=8.9, leading=10.6, spaceAfter=0)
cellh = ParagraphStyle("ch", parent=cell, fontName="Body-Bold", textColor=colors.white)

LEADS = ["User Value:", "Innovation & Differentiation:", "Technical Quality:", "AI NAS Fit:", "Done:", "Not done:",
         "Core 1:", "Core 2:", "Edge:", "Pass:", "Helper:", "Next month:", "Unknown:", "Entrant:", "Signature:", "Date:",
         "Third-party components and open source libraries:", "Platform:", "Run time:", "AI tools used to build it:",
         "Guidance read and paraphrased, nothing copied:", "Test data:", "Inputs:", "Dry run,"]
def fmt(t):
    t = escape(t)
    for L in LEADS:
        e = escape(L)
        t = t.replace(e, f"<b>{e}</b>")
    return re.sub(r"\*([^*]+)\*", r"<i>\1</i>", t)

lines = open(src, encoding="utf-8").read().splitlines()
story = []; i = 0; section = "pre"
def style_for():
    return small if section == "after" else body
while i < len(lines):
    s = lines[i].rstrip()
    if not s or s.startswith("<!--"):
        if "answers end" in s: section = "after"
        i += 1; continue
    if s.startswith("# "):
        story.append(Paragraph(fmt(s[2:]), h1)); i += 1; continue
    if s.startswith("## "):
        story.append(Paragraph(fmt(s[3:]), h2)); i += 1; continue
    if s == "[[FIGURE]]":
        w = 17.4 * cm
        img = Image(fig, width=w, height=w * 5.9 / 17.0)
        story.append(Spacer(1, 2)); story.append(img)
        story.append(Paragraph("Figure: letter mode (steps 1 to 8) and question mode (Q1 to Q3), with the one approval of a letter.",
                               ParagraphStyle("cap", parent=small, textColor=MUTED, fontName="Body-Italic")))
        i += 1; continue
    if s.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            r = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r"-+", c) for c in r): rows.append(r)
            i += 1
        data = [[Paragraph(fmt(c), cellh if k == 0 else cell) for c in r] for k, r in enumerate(rows)]
        t = Table(data, colWidths=[5.2 * cm, 4.0 * cm, 3.8 * cm, 4.4 * cm], hAlign="LEFT")
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), ACC),
            ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#EAF4EC")),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C2CC")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
            ("FONTNAME", (0, 3), (0, 3), "Body-Bold"),
        ]))
        story.append(Spacer(1, 1)); story.append(t); story.append(Spacer(1, 3)); continue
    if s.startswith("- "):
        items = []
        st = style_for()
        while i < len(lines) and lines[i].startswith("- "):
            items.append(ListItem(Paragraph(fmt(lines[i][2:]), ParagraphStyle("li", parent=st, spaceAfter=1)), leftIndent=11))
            i += 1
        story.append(ListFlowable(items, bulletType="bullet", start="\u2022", leftIndent=11, bulletFontSize=8))
        story.append(Spacer(1, 2)); continue
    story.append(Paragraph(fmt(s), sub if section == "pre" and lines[i-2].startswith("# ") else style_for()))
    i += 1

def deco(c, d):
    c.saveState(); c.setFont("Body", 8); c.setFillColor(MUTED)
    c.drawString(1.8 * cm, 1.0 * cm, "Album Out Loud, Round 1 proposal, UGREEN Hackathon 2026 on AI NAS")
    c.drawRightString(A4[0] - 1.8 * cm, 1.0 * cm, f"Page {d.page}")
    c.restoreState()

doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.5 * cm, bottomMargin=1.6 * cm,
                        title="Album Out Loud: Round 1 proposal", author="Entrant", subject="UGREEN Hackathon 2026 on AI NAS")
doc.build(story, onFirstPage=deco, onLaterPages=deco)
print("built", out)
