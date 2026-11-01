# Static test suite for the Album Out Loud submission. Run from project root: python -I app/tests/static_suite.py
import os, re, sys, json, zipfile, hashlib, subprocess, wave
from struct import unpack
sys.stdout.reconfigure(encoding="utf-8")
PKG = "app/album-out-loud"; Z = "submission/album-out-loud.zip"
results = []
def t(name, ok, info=""): results.append((name, bool(ok), info))
def rd(p): return open(p, encoding="utf-8").read()
files = []
for dp, dn, fn in os.walk(PKG):
    for f in fn: files.append(os.path.join(dp, f).replace("\\", "/"))

def check(path):
    out = subprocess.run(["node", "refs/uliya-skill-kit/scripts/check-skill.mjs", path], capture_output=True, text=True, encoding="utf-8")
    d = json.loads(out.stdout); return d["status"], len(d.get("diagnostics", []))
st, n = check(PKG); t("Official checker on package: static-pass, 0 diagnostics", st == "static-pass" and n == 0, f"{st}/{n}")
tmp = os.path.join(os.environ.get("TEMP", "/tmp"), "aol_suite_zip"); os.makedirs(tmp, exist_ok=True)
z = zipfile.ZipFile(Z); z.extractall(tmp)
st, n = check(os.path.join(tmp, "album-out-loud")); t("Official checker on extracted ZIP", st == "static-pass" and n == 0, f"{st}/{n}")
names = [i.filename for i in z.infolist() if not i.is_dir()]
t("ZIP has one top folder album-out-loud/", all(x.startswith("album-out-loud/") for x in names))
t("ZIP holds only SKILL.md + references/*.md", all(x == "album-out-loud/SKILL.md" or re.fullmatch(r"album-out-loud/references/[A-Za-z0-9._-]+\.md", x) for x in names), str(len(names)) + " files")
t("ZIP size < 10 MB and < 100 files", os.path.getsize(Z) < 10_000_000 and len(names) < 100, f"{os.path.getsize(Z)} B")
t("ZIP == package byte for byte", all(z.read(x) == open("app/" + x, "rb").read() for x in names))
t("ZIP sha256 matches CHECKLIST", hashlib.sha256(open(Z, "rb").read()).hexdigest() in rd("submission/CHECKSUMS.md"))
t("No backslash paths in ZIP", all("\\" not in x for x in names))
for f in files:
    b = open(f, "rb").read()
    try: b.decode("utf-8"); ok8 = True
    except Exception: ok8 = False
    t(f"UTF-8, no BOM, LF only: {os.path.basename(f)}", ok8 and not b.startswith(b"\xef\xbb\xbf") and b"\r\n" not in b)
S = rd(PKG + "/SKILL.md")
m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", S)
t("Frontmatter only name + description", bool(m))
t("name lowercase-hyphen 2-64 and equals folder", bool(m) and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", m.group(1)) and m.group(1) == "album-out-loud")
t("description <= 1024 chars with 'Use when'", bool(m) and len(m.group(2)) <= 1024 and "Use when" in m.group(2), f"{len(m.group(2)) if m else 0} chars")
for h in ["# Goal", "# Required input", "# Generation-time capability evidence", "# Workflow", "# Completion and failure"]:
    t(f"Required heading {h}", re.search(r"^" + re.escape(h) + r"\s*$", S, re.M))
for s in ["completed", "failed", "cancelled", "waiting_user", "waiting_approval", "no results"]:
    t(f"Handles state '{s}'", s in S)
ev = re.findall(r"^- `([a-z-]+)` \u2192 `([a-z-]+)`\s*$", S, re.M)
cat = json.load(open("refs/uliya-skill-kit/data/capability-catalog.json", encoding="utf-8"))
cli_agent = {c["name"]: c["agent"] for c in cat["clis"]}
t("Evidence lines match catalog CLI -> agent", bool(ev) and all(cli_agent.get(c) == a for c, a in ev), str(ev))
dl = [l for l in S.splitlines() if "delegate --" in l]
targets = set(a for _, a in ev)
t("Delegate lines present", len(dl) >= 8, str(len(dl)) + " delegates")
bad = []
for l in dl:
    mm = re.search(r"delegate --target ([a-z-]+) --instruction '(.*)'\s*$", l)
    if not mm: bad.append("format:" + l[:60]); continue
    tg, ins = mm.groups()
    if tg not in targets: bad.append("target:" + tg)
    if "'" in ins: bad.append("apostrophe:" + ins[:50])
    for tok in ['"', "`", " --", " > ", " | ", "&&", "$("]:
        if tok in ins: bad.append(f"token {tok!r}:" + ins[:40])
    if re.search(r"<[a-z][^>]*>", ins): bad.append("placeholder:" + ins[:40])
t("Every delegate: registered target, single-quoted, no forbidden tokens", not bad, "; ".join(bad[:3]))
actions = {(c["name"], a["name"]) for c in cat["clis"] for a in c["actions"]}
anames = {a for _, a in actions}
cm = rd(PKG + "/references/capability-map.md")
mentioned = set(re.findall(r"`([a-z]+(?:-[a-z]+)*)`", cm))
unknown = [x for x in mentioned if x not in anames and x not in cli_agent and x not in set(cli_agent.values()) and x not in {"photo-agent", "file-agent", "knowledge-agent"}]
t("capability-map: every backticked action/CLI exists in catalog", not unknown, ",".join(sorted(unknown)[:8]))
refs = sorted(os.path.basename(f) for f in files if "/references/" in f)
links = set(re.findall(r"\]\(references/([^)]+)\)", S))
t("Every reference linked from SKILL.md", set(refs) <= links, f"missing {set(refs) - links}")
t("Every link points to an existing file", links <= set(refs), f"broken {links - set(refs)}")
t("SKILL.md size within checker limit (<= 1 MB, body <= 500 lines)", len(S.encode()) < 1_000_000 and S.count(chr(10)) <= 500, f"{len(S.encode())} B, {S.count(chr(10))} lines")
alltext = "\n".join(rd(f) for f in files)
probs = []
for f in files:
    for l in rd(f).splitlines():
        if "delegate --" in l: continue
        if re.search(r"\bcat\s", l): probs.append("cat-space")
        if re.search(r"\b(bypass|skip|disable|ignore)\b.{0,40}\b(approval|permission|audit|gateway)", l, re.I): probs.append("bypass-near-approval")
        if re.search(r"\b(curl|wget)\b", l, re.I): probs.append("curl/wget")
        if re.search(r"[\s\"'](/volume\d|/nas/|/mnt\b|/shares?\b)", l): probs.append("nas-path")
        if re.search(r"request[ -]id|expert id|host cli|hermes|ug-ai", l, re.I): probs.append("internal")
        if re.search(r"```(bash|sh|shell|python|py|js|javascript|node|ts|typescript)\b", l): probs.append("script-fence")
        if re.search(r"\b(TODO|TBD)\b|replace-with-", l): probs.append("placeholder")
t("No checker-trap patterns in any package file", not probs, ",".join(sorted(set(probs))))
banned = [w for w in ["story", "chapters", "archive", "recap", "memory album", "seamless", "empower", "revolutioniz", "game-changer", "unlock"] if re.search(r"\b" + w, alltext, re.I)]
t("No banned / slop words in package", not banned, ",".join(banned))
t("No key-like secrets in package", not re.search(r"sk-[A-Za-z0-9]{12,}", alltext))
pdf = open("submission/AlbumOutLoud_Round1_Proposal.pdf", "rb").read()
t("PDF < 1 MB", len(pdf) < 1_000_000, f"{len(pdf)} B")
t("PDF accessible: tagged, language, alt text", all(k in pdf for k in [b"/StructTreeRoot", b"/Lang", b"/Alt"]))
src = rd("submission/pdf_source.md")
wc = subprocess.run([sys.executable, "-I", "pdf_scripts/count_words.py", "submission/pdf_source.md"], capture_output=True, text=True).stdout
tot = int(re.search(r"TOTAL (\d+)", wc).group(1)); t("PDF ten answers <= 500 words", tot <= 500, str(tot) + " words")
t("PDF answers the 10 official questions", len(re.findall(r"^## (10|[1-9])\. ", src, re.M)) == 10)
dv = rd("submission/DEVPOST.md")
tag = re.search(r"## Tagline[^\n]*\n\n([^\n]+)", dv)
t("Devpost tagline <= 200 chars", bool(tag) and len(tag.group(1)) <= 200, f"{len(tag.group(1)) if tag else '?'} chars")
t("Track consistent in PDF and Devpost", "Bring Memories to Life" in src and "Bring Memories to Life" in dv)
t("Honesty: PDF states NAS run not done", "Not done" in src and "NAS run" in src)
t("Numbers consistent: 419 of 421, 23 of 24 (PDF, Devpost, SIMULATION.md)", all("419 of 421" in x and "23 of 24" in x for x in (src, dv, rd("app/tuning/SIMULATION.md"))))
dis = rd(PKG + "/references/disclosure.md")
t("Disclosure names cloud tuning models", all(k in dis for k in ["Nemotron", "MiMo"]))
t("Licence stated (all rights reserved during the hackathon)", "Licence of this package" in dis and "No other licence is granted" in dis)
for p in ["flow_diagram.png", "letter_card.png", "comparison.png"]:
    b = open("submission/assets/" + p, "rb").read(); w, h = unpack(">II", b[16:24])
    t(f"Asset {p} valid PNG >= 1200 px", b[:8] == b"\x89PNG\r\n\x1a\n" and w >= 1200, f"{w}x{h}")
with wave.open("submission/assets/sample_letter.wav") as wv: dur = wv.getnframes() / wv.getframerate()
t("Sample letter WAV plays (valid header, > 30 s)", dur > 30, f"{dur:.0f} s")
sl = rd("submission/assets/sample_letter.txt")
t("Sample letter has no markdown symbols (screen-reader safe)", not re.search(r"^#|\*\*|\|", sl, re.M))
t("Sample letter has 8 numbered entries", len(re.findall(r"^Photo \d of 8\.", sl, re.M)) == 8)
t("Sample letter AI guesses free of gender words", not re.search(r"AI guess:.*\b(man|woman|boy|girl|he|she)\b", sl, re.I))
t("Gallery comparison names no other entrant", b"Remember When" not in open("submission/tools/make_images.py", "rb").read())
key = open(os.environ["PRIMALABS_KEY_FILE"], encoding="utf-8").read().strip() if os.environ.get("PRIMALABS_KEY_FILE") else None  # optional: only to prove the key is in no file
leak = []
for dp in ([] if key is None else [None]):
    break
for dp, dn, fn in os.walk("."):
    parts = dp.replace("\\", "/").split("/")
    if "refs" in parts or ".git" in parts: continue
    for f in fn:
        try:
            if key and key.encode() in open(os.path.join(dp, f), "rb").read(): leak.append(f)
        except Exception: pass
t("API key absent from every project file", not leak, ",".join(leak))
p = sum(1 for r in results if r[1])
for n, ok, info in results: print(("PASS" if ok else "FAIL"), "|", n, ("| " + str(info) if info else ""))
print(f"STATIC: {p} / {len(results)}")
