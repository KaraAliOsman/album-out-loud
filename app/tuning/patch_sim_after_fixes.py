"""One-off patch of simulate.py for the after-fixes run (one-line letters with a pilcrow, spoken
reply start, opening line, AI reading label, qualified count, cooperative apostrophe mocks)."""
from pathlib import Path

p = Path(__file__).resolve().parent / "simulate.py"
t = p.read_text(encoding="utf-8")


def rep(a, b):
    global t
    assert t.count(a) == 1, (a[:80], t.count(a))
    t = t.replace(a, b)


rep('''    ap.add_argument("--reeval", action="store_true", help="recompute checks of saved runs, no API calls")
    args = ap.parse_args()
''', '''    ap.add_argument("--reeval", action="store_true", help="recompute checks of saved runs, no API calls")
    ap.add_argument("--out", default="", help="output folder under results/ (default results/sim)")
    args = ap.parse_args()
    global OUT
    if args.out:
        OUT = ROOT / "results" / args.out
''')

rep('''            try:
                result = mock(sid, ctx, step, d["target"], d["instruction"] or "")
''', '''            try:
                result = mock(sid, ctx, step, d["target"], d["instruction"] or "")
                # Cooperative expert: when the instruction asks for typographic apostrophes in returned
                # values, the mock returns them that way. Instructions without that line get straight ones.
                if "Write every straight apostrophe" in (d["instruction"] or ""):
                    result = json.loads(json.dumps(result, ensure_ascii=False).replace("'", APO))
''')

rep('''        content = ins[idx + len(key):] if idx >= 0 else ""
        ctx["saved_text"] = content''', '''        content = ins[idx + len(key):] if idx >= 0 else ""
        if "\\u00b6" in content:  # one-line text, each line break written as a pilcrow
            content = re.sub(r" ?\\u00b6 ?", "\\n", content)
        ctx["saved_text"] = content''')

rep('''    if "\\n" in ins and step not in ("7", "Q3"):''', '''    if "\\n" in ins:''')

rep('''        return ok({"kept": len(pool), "newestCaptureTimeKept"''',
    '''        return ok({"qualified": {"S1": 14, "S4": 2, "S7": 4, "S8": 4}.get(sid, len(pool)), "kept": len(pool), "newestCaptureTimeKept"''')

rep('''                   "firstLine": f"Photos from Grandpa{APO}s 80th birthday",
                   "entryLines": entry, "language": "English",''',
    '''                   "firstLine": f"Grandpa, here are 8 photos from Grandpa{APO}s 80th birthday, chosen by Ana.",
                   "entryLines": entry, "languageLine": "Language: English",''')

rep('''    c.append(chk(f"{prefix}: title line Photos from album", re.search(r"^(Photos from|Fotos de|Fotos del álbum) " + re.escape(norm(exp["album"])), L, re.M), L.splitlines()[0][:80] if L else "empty"))''',
    '''    first_line = next((ln for ln in L.splitlines() if ln.strip()), "")
    c.append(chk(f"{prefix}: opening line names the album", norm(exp["album"]) in first_line, first_line[:100]))''')

rep('''        c.append(chk(f"{prefix}: photo {n} OCR words not marked (AI reading)", "(AI reading)" not in lines, lines[-160:], critical=False))''',
    '''        c.append(chk(f"{prefix}: photo {n} OCR words not marked AI reading", not re.search(r"AI reading|lectura de la IA", lines, re.I), lines[-160:], critical=False))''')

rep('''        m = re.search(r"^(Photos from|Fotos de)", t, re.M)
        i = m.start() if m else 0
        ends = [j for j in (t.find(k, i) for k in ("Open questions from the last letter", "Preguntas abiertas",
                                                    "Type notes by photo number", "Escribe notas")) if j > i]''',
    '''        m = re.search(r"^(Photos from|Fotos de|.*here are \\d+|.*here are the family|.*aquí (tienes|están))", t, re.M | re.I)
        i = m.start() if m else 0
        ends = [j for j in (t.find(k, i) for k in ("Open questions from the last letter", "Preguntas abiertas",
                                                    "Type notes by photo number", "Send all notes", "Escribe notas",
                                                    "Envía todas")) if j > i]''')

rep('''            c += letter_checks(preview_letter(L) if "Photos from" in L else L,''',
    '''            c += letter_checks(preview_letter(L),''')

rep('''re.search(r"Preview: 8 photos, 1 not described", pv[0])''',
    '''re.search(r"Preview: 8 of 14 photos chosen, 1 not described", pv[0])''')

rep('''        c.append(chk("reply starts with In <letter file name>, photo N", re.match(r"\\s*In Listening letter - Grandpa.s 80th birthday - 2026-09-12 18-40(\\.txt)?, photo " + ("4" if sid == "S5" else "7"), reply), reply[:120]))''',
    '''        c.append(chk("reply starts with the spoken letter form, photo N", re.match(r"\\s*In the Grandpa.s 80th birthday letter of 12 September 2026, photo " + ("4" if sid == "S5" else "7"), reply), reply[:120]))''')

rep('''replace(re.escape("{question}"), "(.+?)")''', '''replace(re.escape("{rewritten question}"), "(.+?)")''')

p.write_text(t, encoding="utf-8", newline="\n")
print("patched")
