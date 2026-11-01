"""Reviewer variant R = final prompts plus the reviewer edits. Writes prompts/R_*.txt."""
from pathlib import Path
P = Path(__file__).resolve().parent / "prompts"
GENDER = " In a language with gendered words, use one form for everyone, such as un adulto, un niño or un bebé in Spanish."
BW_OLD = "If the photo is black and white or an old print, begin Line 1 with the words In black and white or An old print, said in {language}, never with this photo shows."
BW_NEW = "If the photo is black and white or an old print, end Line 1 with the words in black and white or an old print, said in {language}."
WM_OLD = "logos, watermarks, number plates"
WM_NEW = "logos, watermarks, names or dates printed in a corner, number plates"
def sub(t, a, b):
    assert t.count(a) == 1, a[:50]
    return t.replace(a, b)
b = (P / "final_brief.txt").read_text("utf-8").strip()
b = sub(b, "never man, woman, boy, girl, he or she, and give their main visible action.",
        "never man, woman, boy, girl, he or she, and give their main visible action." + GENDER)
b = sub(sub(b, BW_OLD, BW_NEW), WM_OLD, WM_NEW)
r = (P / "final_rich.txt").read_text("utf-8").strip()
r = sub(r, "never man, woman, boy, girl, he or she.", "never man, woman, boy, girl, he or she." + GENDER)
r = sub(sub(r, BW_OLD, BW_NEW), WM_OLD, WM_NEW)
q = (P / "final_question.txt").read_text("utf-8").strip()
q = sub(q, "if the question asks who a person is or which person is someone, uses a role or family word in any language, such as groom, bride, husband, wife, father, mother, grandmother, son or daughter, even when one person looks likely, or asks how people are related, a name, a feeling,",
        "if the question, in any language, asks who a person is, which person has a role or whether a person has a role, such as groom, bride, husband, wife, father, mother, grandmother, son or daughter, even when one person looks likely, or asks how people are related, a name, a gender, a feeling,")
for n, t in (("brief", b), ("rich", r), ("question", q)):
    (P / f"R_{n}.txt").write_text(t, "utf-8")
