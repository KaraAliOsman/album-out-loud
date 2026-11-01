"""Reviewer variant R2 rich = final rich + gender line + corner text + Line 2 group and Behind fixes (BW rule unchanged)."""
from pathlib import Path
P = Path(__file__).resolve().parent / "prompts"
def sub(t, a, b):
    assert t.count(a) == 1, a[:60]
    return t.replace(a, b)
r = (P / "final_rich.txt").read_text("utf-8").strip()
r = sub(r, "never man, woman, boy, girl, he or she.", "never man, woman, boy, girl, he or she. In a language with gendered words, use one form for everyone, such as un adulto, un niño or un bebé in Spanish.")
r = sub(r, "logos, watermarks, number plates", "logos, watermarks, names or dates printed in a corner, number plates")
r = sub(r, "The first sentence, of at most 25 words, covers all the people or things in front together, with clothing, position from left to right as seen by the viewer and visible action. The second sentence starts with Behind, said in {language}, and gives what is behind them, with plain colour names.",
        "The first sentence, of at most 25 words, covers the people or things in front, with clothing, position from left to right as seen by the viewer and visible action; for more than 5 people, do not list them one by one, but say a group and what most of them wear or do. The second sentence says in {language} what is behind them, with plain colour names.")
(P / "R2_rich.txt").write_text(r, "utf-8")
