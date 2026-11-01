"""Copy the variant A prompts exactly from SKILL.md (text between 'Prompt begins: ' and ' Prompt ends.').

Usage: python -I extract_prompts_A.py <SKILL.md> <prompts_dir>
Order in SKILL.md: brief (step 4), rich (step 4), question (Q2).
"""
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
found = re.findall(r"Prompt begins: (.*?) Prompt ends\.", text)
assert len(found) == 3, len(found)
out = Path(sys.argv[2])
out.mkdir(exist_ok=True)
for name, body in zip(["A_brief.txt", "A_rich.txt", "A_question.txt"], found):
    (out / name).write_text(body + "\n", encoding="utf-8")
    print(name, len(body.split()), "words")
