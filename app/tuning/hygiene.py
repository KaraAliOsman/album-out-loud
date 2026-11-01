"""Check prompt files against the Skill checker hygiene rules.

Usage: python -I hygiene.py prompts/D_brief.txt prompts/D_rich.txt ...
Fails on: straight apostrophe, double quotes (straight or curly), backtick, the sequences
' > ', '|', '&&', '--', 'cat ' (as a word), a line break, and any placeholder other than
{language} (plus {question} in question prompts). Also checks the English sentinel words.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
BAD = {"straight apostrophe": "'", "double quote": '"', "curly double quote": "\u201c",
       "curly double quote close": "\u201d", "backtick": "`", "redirect": " > ", "pipe": "|",
       "and-and": "&&", "double dash": "--"}
ok_all = True
for f in sys.argv[1:]:
    text = Path(f).read_text(encoding="utf-8").strip()
    problems = [name for name, s in BAD.items() if s in text]
    if re.search(r"\bcat ", text):
        problems.append("cat followed by space")
    if "\n" in text:
        problems.append("line break")
    allowed = {"{language}"} | ({"{question}"} if "question" in Path(f).name else set())
    extra = set(re.findall(r"\{[^}]*\}", text)) - allowed
    if extra:
        problems.append("placeholders " + ", ".join(sorted(extra)))
    if "{language}" not in text:
        problems.append("missing {language}")
    need = ["UNCLEAR"] if "question" in Path(f).name else ["Line 1", "Words", "none", "Not described"]
    problems += [f"sentinel {w} missing" for w in need if w not in text]
    ok_all &= not problems
    print(("OK   " if not problems else "FAIL ") + f + (": " + "; ".join(problems) if problems else "")
          + f"  ({len(text.split())} words)")
sys.exit(0 if ok_all else 1)
