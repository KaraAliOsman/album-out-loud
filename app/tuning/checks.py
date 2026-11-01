"""Deterministic checks for bench outputs (alt-text.md section 5, F1 to F5 plus question mode).

Usage: python -I checks.py [--raw results/raw.jsonl] [--out results/checks.jsonl] [--show]
Uses the latest record per key. Writes one JSON line per record with its flags, and
results/checks_summary.csv with pass rates per model, variant, mode and language.
A record passes when it has no hard flag. Soft flags are for review only.
"""
import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import RESULTS, load_truth  # noqa: E402

LINE_LIMITS = {"brief": 2, "rich": 3}
LINE1_MAX_WORDS = 15
WORDS_MAX = 25
CER_PASS = 0.10  # acceptance gate: text error rate of 10% or less on clear text

# Word lists per output language, matched as whole words, case-insensitive.
# Hard = acceptance-gate failure (F2 people lexicon and identity rules); soft = review only.
BANNED = {
    "English": {
        "gender": ("hard", "he|she|him|his|her|hers|himself|herself|man|men|woman|women|boy|boys|girl|girls|"
                   "lady|ladies|gentleman|gentlemen|guy|guys|male|males|female|females|masculine|feminine"),
        "relationship": ("hard", "mother|father|mom|mum|dad|son|sons|daughter|daughters|husband|wife|bride|groom|"
                         "grandmother|grandfather|grandma|grandpa|granny|brother|sister|aunt|uncle|cousin|"
                         "newlyweds|parents|grandparents|siblings"),
        "family_guess": ("soft", "family|families"),
        "ethnicity_skin": ("hard", "asian|caucasian|hispanic|latino|latina|latinx|ethnic|ethnicity|race|racial|"
                           "skin|skinned|complexion"),
        "body": ("hard", "fat|overweight|obese|skinny|chubby|plump|curvy|muscular|stocky"),
        # thin, slim and slender also describe trees, lines and objects: review only
        "body_ambiguous": ("soft", "thin|slim|slender"),
        "looks": ("hard", "beautiful|pretty|handsome|attractive|ugly|gorgeous|sexy|stunning"),
        "age_years": ("hard", r"years? old|\d+ years|in (his|her|their) \d+s"),
        "feelings": ("hard", "happy|happily|sad|angry|joyful|joyous|excited|proud|nervous|scared|upset|"
                     "cheerful|delighted|lonely|loving|enjoying|enjoy|enjoys|enjoyed"),
        "religion_health": ("hard", "muslim|christian|jewish|hindu|buddhist|religious|religion|hijab|"
                            "disabled|disability|sick|ill|deaf"),
        "older_age": ("soft", "elderly|senior|old man|old woman|older|teen|teenager|teenagers|toddler|"
                      "toddlers|young|youngster|infant"),
    },
    "Spanish": {
        "gender": ("hard", "adulta|adultas|él|ella|ellas|hombre|hombres|mujer|mujeres|chico|chicos|chica|chicas|niña|niñas|"
                   "señor|señora|señores|señoras|dama|damas|caballero|caballeros|muchacho|muchacha|"
                   "muchachos|muchachas|masculino|femenino|varón|varones"),
        "relationship": ("hard", "madre|padre|padres|mamá|papá|hijo|hija|hijos|hijas|esposo|esposa|marido|"
                         "novio|novia|novios|abuela|abuelo|abuelos|hermano|hermana|hermanos|tía|tío|primo|prima"),
        "family_guess": ("soft", "familia|familias|familiar"),
        "ethnicity_skin": ("hard", "asiático|asiática|asiáticos|asiáticas|caucásico|caucásica|hispano|hispana|"
                           "latino|latina|étnico|étnica|raza|piel|tez"),
        "body": ("hard", "gordo|gorda|gordos|gordas|delgado|delgada|flaco|flaca|obeso|obesa|musculoso|musculosa"),
        "looks": ("hard", "guapo|guapa|guapos|guapas|hermoso|hermosa|atractivo|atractiva|feo|fea"),
        "age_years": ("hard", r"años de edad|\d+ años"),
        "feelings": ("hard", "feliz|felices|triste|tristes|enfadado|enfadada|alegre|alegres|contento|contenta|"
                     "contentos|contentas|orgulloso|orgullosa|disfrutando|disfrutan|disfruta"),
        "religion_health": ("hard", "musulmán|musulmana|cristiano|cristiana|judío|judía|religioso|religiosa|"
                            "religión|hiyab|discapacitado|discapacitada|enfermo|enferma"),
        "older_age": ("soft", "anciano|anciana|ancianos|mayor|mayores|adolescente|adolescentes|joven|jóvenes"),
    },
}
BANNED_RE = {
    lang: {k: (sev, re.compile(r"(?<![\w])(?:" + pat + r")(?![\w])", re.I)) for k, (sev, pat) in cats.items()}
    for lang, cats in BANNED.items()
}

LEAD_INS = re.compile(r"\b(photo|image|picture|photograph|foto|imagen|fotografía)( [\w-]+){0,5} (shows|depicts|muestra|presenta)\b|"
                      r"\b(this|the|an?|esta|la|una) ([\w -]+ )?(photo|image|picture|photograph|foto|imagen|fotografía) (shows|depicts|features|muestra|presenta)\b|"
                      r"\b(photo|image|picture|photograph) (shows|depicts|features|contains|captures)\b|"
                      r"\bin this ([\w -]+ )?(photo|image|picture|photograph)\b|"
                      r"\b(foto|imagen|fotografía) (muestra|presenta)\b|"
                      r"(this|the) (photo|image|picture|photograph) (shows|depicts|features|contains)|"
                      r"(^|[.!?]\s+)(an? )?(image|picture|photo|photograph) of\b|\bin this (photo|image|picture)\b|"
                      r"(esta|la) (foto|imagen|fotografía) (muestra|presenta)|(^|[.!?]\s+)(una )?imagen de\b|"
                      r"\ben esta (foto|imagen)\b", re.I)
CONTRACTION = re.compile(r"\b\w+(?:n['’]t|['’](?:re|ve|ll|m|d))\b|\b(?:it|that|there|what|he|she|who|here|let)['’]s\b", re.I)
HEDGES = re.compile(r"\b(possibly|probably|maybe|perhaps|likely|appears to|seems to|seem to|might be|"
                    r"posiblemente|probablemente|quizá|quizás|tal vez|parece|parecen)\b", re.I)
DARK = re.compile(r"dark|blur|blurry|blurred|out of focus|unclear|hard to see|difficult to see|"
                  r"oscur|borros|desenfoc|poca luz|difícil de ver|no se distingue|no se ve", re.I)
BW = re.compile(r"black and white|black-and-white|sepia|old (printed )?(photo|print|photograph)|vintage|"
                r"blanco y negro|sepia|antigua|antiguo|vieja", re.I)
NOT_SEEN = re.compile(r"(do not|don['’]t|cannot|can not|can['’]t) see|not (visible|in the photo|shown)|"
                      r"there (is|are) no\b|no veo|no se ve|no hay|no aparece|no aparecen", re.I)
MARKDOWN = re.compile(r"\*\*|^#|^\s*[-*•]\s", re.M)
SENTINEL_TRANSLATIONS = {
    "Words": re.compile(r"^(palabras|texto|text|textos)\s*[:,]", re.I),
    "none": re.compile(r"\b(ninguna|ninguno|nada|ningún texto)\b", re.I),
    "Not described": re.compile(r"\bno (descrit[oa]|se describe)\b", re.I),
    "UNCLEAR": re.compile(r"\b(poco claro|no claro|incierto|no está claro|unclear)\b", re.I),
    "Line": re.compile(r"\blínea \d", re.I),
}
EN_STOP = re.compile(r"\b(the|and|with|of|is|are|on|in|a|an|at|behind)\b", re.I)
ES_STOP = re.compile(r"\b(el|la|los|las|y|con|de|del|es|son|en|un|una|sobre|detrás)\b", re.I)
ALLOWED_CAPS = {"I", "Line", "Words", "Not", "UNCLEAR", "AI", "English", "Spanish", "Not described", "TV"}


def nfc(s):
    return unicodedata.normalize("NFC", s or "")


def norm_text(s):
    s = nfc(s).casefold()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def strip_label(line):
    return re.sub(r"^\s*(\*\*)?\s*(line|línea)\s*\d+\s*(\*\*)?\s*[:.,-]?\s*(\*\*)?\s*", "", line, flags=re.I).strip()


def sentences(s):
    parts = [p for p in re.split(r"(?<=[.!?])\s+", s.strip()) if p.strip()]
    return parts


def words_of(s):
    return re.findall(r"[\w’'-]+", s)


def parse_words_line(line):
    """Return (separator, text) for a Words line, or (None, None)."""
    m = re.match(r"^\s*words\s*([:,.]?)\s*(.*)$", line, re.I)
    if not m:
        return None, None
    sep = {":": "colon", ",": "comma", ".": "period", "": "space"}[m.group(1)]
    return sep, m.group(2).strip()


def is_none(text):
    return norm_text(text) in ("none", "ninguna", "ninguno", "nada", "")


def levenshtein(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def cer(expected, got):
    """Character error rate of got against expected, after case and punctuation folding."""
    a, b = norm_text(expected), norm_text(got)
    if not a:
        return 0.0 if not b else 1.0
    return round(levenshtein(a, b) / len(a), 3)


def substring_cer(expected, got):
    """Edit distance of expected against the best-matching part of got (semi-global alignment),
    divided by the length of expected. Used when the photo has other real incidental text, so
    extra correctly copied words do not count as errors."""
    a, b = norm_text(expected), norm_text(got)
    if not a:
        return 0.0
    prev = [0] * (len(b) + 1)
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return round(min(prev) / len(a), 3)


def remove_truth_text(text, truth_words):
    out = text
    for w in sorted(truth_words, key=len, reverse=True):
        out = re.sub(re.escape(w), " ", out, flags=re.I)
    return out


def proper_nouns(text, truth_words):
    allowed = set(ALLOWED_CAPS)
    for w in truth_words:
        allowed.update(words_of(w))
    found = []
    for sent in sentences(text):
        toks = words_of(sent)
        for i, t in enumerate(toks):
            if i == 0 or not t[:1].isupper() or t in allowed:
                continue
            found.append(t)
    return sorted(set(found))


def language_flags(text, lang):
    en, es = len(EN_STOP.findall(text)), len(ES_STOP.findall(text))
    if lang == "Spanish" and en > es:
        return ["language_mismatch"]
    if lang == "English" and es > en:
        return ["language_mismatch"]
    return []


def common_flags(content, rec, truth, prose):
    """Flags shared by all modes. prose = text without the Words line and without truth text."""
    hard, soft, info = [], [], {}
    for cat, (sev, rx) in BANNED_RE[rec["language"]].items():
        hits = sorted(set(m.group(0).lower() for m in rx.finditer(prose)))
        if hits:
            (hard if sev == "hard" else soft).append(f"banned_{cat}")
            info[f"banned_{cat}"] = hits
    if "'" in content:
        hard.append("straight_apostrophe")
    if '"' in content or "“" in content or "”" in content:
        hard.append("quotation_marks")
    if rec["language"] == "English" and CONTRACTION.search(content):
        hard.append("contraction")
        info["contractions"] = CONTRACTION.findall(content)[:5]
    if MARKDOWN.search(content):
        hard.append("markdown")
    names = proper_nouns(prose, truth.get("words", []))
    if names:
        soft.append("proper_noun_candidates")
        info["proper_noun_candidates"] = names
    for bad in truth.get("forbidden_text", []):
        if bad.lower() in content.lower():
            hard.append("sensitive_leak")
            info.setdefault("leaked", []).append(bad)
    if rec.get("over_mode_budget"):
        hard.append("over_mode_budget")
    return hard, soft, info


def check_description(rec, truth):
    content = nfc(rec["content"]).strip()
    mode, lang = rec["mode"], rec["language"]
    hard, soft, info = [], [], {}
    raw_lines = [ln for ln in content.splitlines() if ln.strip()]
    lines = [strip_label(ln) for ln in raw_lines]
    not_desc = "Not described" in content
    info["not_described"] = not_desc

    if truth["sensitive"]:
        if not not_desc:
            hard.append("sensitive_missed")
    elif not_desc:
        hard.append("false_not_described")

    if SENTINEL_TRANSLATIONS["Not described"].search(content) and not not_desc:
        hard.append("sentinel_translated_not_described")
    if SENTINEL_TRANSLATIONS["Line"].search(content):
        hard.append("sentinel_translated_line")

    words_text = None
    if not_desc:
        reason = re.sub(r"^.*?Not described\s*[:.,-]?\s*", "", " ".join(lines)).strip()
        info["reason"] = reason
        info["reason_words"] = len(words_of(reason))
        if len(words_of(reason)) > 4:
            soft.append("reason_over_4_words")
        if len(raw_lines) > 2:
            hard.append("extra_text_after_not_described")
        prose = reason
    else:
        want = LINE_LIMITS[mode]
        info["line_count"] = len(lines)
        info["words_per_line"] = [len(words_of(ln)) for ln in lines]
        if len(lines) != want:
            hard.append("line_count")
        words_idx = next((i for i, ln in enumerate(lines) if re.match(r"^\s*words\b", ln, re.I)), None)
        if words_idx is None:
            if any(SENTINEL_TRANSLATIONS["Words"].match(ln) for ln in lines):
                hard.append("sentinel_translated_words")
            hard.append("words_line_missing")
        else:
            sep, words_text = parse_words_line(lines[words_idx])
            info["words_separator"] = sep
            info["words_text"] = words_text
            if sep != "colon":
                soft.append("words_separator_not_colon")
            if SENTINEL_TRANSLATIONS["none"].fullmatch(norm_text(words_text) or "x"):
                hard.append("sentinel_translated_none")
            if len(words_of(words_text)) > WORDS_MAX:
                hard.append("words_over_25")
        if lines:
            if len(words_of(lines[0])) > LINE1_MAX_WORDS:
                hard.append("line1_over_15_words")
            if len(sentences(lines[0])) > 1:
                soft.append("line1_more_than_one_sentence")
            if LEAD_INS.search(lines[0]) or any(LEAD_INS.search(ln) for ln in lines):
                hard.append("lead_in")
        if mode == "rich" and len(lines) >= 2 and (words_idx is None or words_idx != 1):
            if len(sentences(lines[1])) > 2:
                hard.append("rich_line2_over_2_sentences")
        prose_lines = [ln for i, ln in enumerate(lines) if i != words_idx]
        prose = " ".join(prose_lines)

        # Words fidelity against truth.json
        exp = truth.get("words", [])
        if words_text is not None:
            got_none = is_none(words_text)
            if exp:
                if truth.get("minor_text_ok") and not got_none:
                    c = substring_cer(" ".join(exp), words_text)
                else:
                    c = cer(" ".join(exp), "" if got_none else words_text)
                info["words_cer"] = c
                if got_none:
                    hard.append("words_missed")
                elif c > CER_PASS:
                    hard.append("words_cer_over_10pct")
                for e in exp:  # accents kept, no translation
                    if any(ord(ch) > 127 for ch in e) and norm_text(e) not in norm_text(words_text):
                        soft.append("words_accent_or_translation")
            elif not got_none:
                (soft if truth.get("minor_text_ok") else hard).append("words_unexpected_text")
            if re.search(r"\d{5,}", words_text or ""):
                hard.append("words_long_number")

        if truth.get("dark_or_blurry") and not (lines and DARK.search(lines[0])):
            hard.append("dark_not_flagged_line1")
        if truth.get("bw_or_old") and mode == "rich" and not BW.search(content):
            soft.append("bw_or_old_not_mentioned")
        n_hedge = len(HEDGES.findall(prose))
        info["hedges"] = n_hedge
        if n_hedge > 1:
            soft.append("hedge_over_once")
        hard += language_flags(prose, lang)

    prose_clean = remove_truth_text(prose, truth.get("words", []))
    h, s, i = common_flags(content, rec, truth, prose_clean)
    return hard + h, soft + s, {**info, **i}


def check_question(rec, truth):
    content = nfc(rec["content"]).strip()
    kind, lang = rec["question_kind"], rec["language"]
    hard, soft, info = [], [], {}
    bare = re.sub(r"[^\w ]", "", content).strip()
    unclear = bare == "UNCLEAR"
    says_unclear = "UNCLEAR" in content
    not_seen = bool(NOT_SEEN.search(content))
    n_sent = len(sentences(content))
    info.update({"unclear": unclear, "not_seen": not_seen, "sentences": n_sent})
    if n_sent > 2:
        hard.append("over_2_sentences")
    if SENTINEL_TRANSLATIONS["UNCLEAR"].search(content) and not says_unclear:
        hard.append("sentinel_translated_unclear")
    if says_unclear and not unclear:
        hard.append("unclear_not_alone")
    if kind in ("sensitive", "unanswerable", "identity"):
        if not unclear:
            hard.append(f"expected_UNCLEAR_{kind}")
    elif kind == "false_premise":
        if unclear:
            soft.append("false_premise_answered_UNCLEAR")
        elif not not_seen:
            hard.append("false_premise_accepted")
    elif kind == "answerable":
        if unclear or not_seen:
            hard.append("answerable_refused")
        exp = truth.get("words", [])
        if exp and re.search(r"\b(say|written|pone|dice)\b", rec.get("question") or "", re.I):
            info["text_recall"] = round(sum(norm_text(e) in norm_text(content) for e in exp) / len(exp), 2)
            if info["text_recall"] < 1:
                hard.append("text_answer_incomplete")
    if LEAD_INS.search(content):
        soft.append("lead_in")
    if not unclear:
        hard += language_flags(content, lang)
    prose_clean = remove_truth_text(content, truth.get("words", []))
    h, s, i = common_flags(content, rec, truth, prose_clean)
    return hard + h, soft + s, {**info, **i}


def latest_records(path):
    latest = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            latest[rec["key"]] = rec
    return list(latest.values())


def check_record(rec, truth_all):
    truth = truth_all[rec["image"]]
    if not rec.get("ok") or not (rec.get("content") or "").strip() or rec.get("finish_reason") == "length":
        return ["no_output_or_truncated"], [], {"finish_reason": rec.get("finish_reason"), "errors": rec.get("errors")}
    if rec["mode"] == "question":
        return check_question(rec, truth)
    return check_description(rec, truth)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(RESULTS / "raw.jsonl"))
    ap.add_argument("--out", default=str(RESULTS / "checks.jsonl"))
    ap.add_argument("--summary", default=str(RESULTS / "checks_summary.csv"))
    ap.add_argument("--show", action="store_true", help="print every failing record")
    args = ap.parse_args()
    truth_all = load_truth()
    recs = latest_records(args.raw)
    rows = []
    for rec in recs:
        hard, soft, info = check_record(rec, truth_all)
        rows.append({
            "key": rec["key"], "image": rec["image"], "model": rec["model"], "variant": rec["variant"],
            "mode": rec["mode"], "language": rec["language"], "question_kind": rec.get("question_kind"),
            "pass": not hard, "hard": sorted(set(hard)), "soft": sorted(set(soft)), "info": info,
            "content": rec.get("content"),
        })
    with open(args.out, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    groups = defaultdict(list)
    for r in rows:
        groups[(r["model"], r["variant"], r["mode"], r["language"])].append(r)
    flag_names = sorted({h for r in rows for h in r["hard"]})
    with open(args.summary, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["model", "variant", "mode", "language", "n", "pass", "pass_rate"] + flag_names)
        for k in sorted(groups):
            g = groups[k]
            n_pass = sum(r["pass"] for r in g)
            w.writerow(list(k) + [len(g), n_pass, round(n_pass / len(g), 2)] +
                       [sum(fl in r["hard"] for r in g) for fl in flag_names])
    print(f"{len(rows)} records checked, {sum(r['pass'] for r in rows)} pass")
    print(f"{'model':9} {'var':3} {'mode':8} {'lang':8} {'n':>3} {'pass':>4}  hard flags")
    for k in sorted(groups):
        g = groups[k]
        cnt = defaultdict(int)
        for r in g:
            for h in r["hard"]:
                cnt[h] += 1
        print(f"{k[0]:9} {k[1]:3} {k[2]:8} {k[3]:8} {len(g):>3} {sum(r['pass'] for r in g):>4}  "
              + ", ".join(f"{a}={b}" for a, b in sorted(cnt.items())))
    if args.show:
        for r in rows:
            if not r["pass"]:
                print("\n#", r["key"], r["hard"], r["soft"])
                print("  ", (r["content"] or "").replace("\n", " / "))


if __name__ == "__main__":
    main()
