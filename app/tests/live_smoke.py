# Live smoke test of the final Skill prompts on CC0/synthetic images (cloud stand-in model). Key read from file, never printed.
import json, base64, sys, urllib.request, concurrent.futures as cf, re
sys.stdout.reconfigure(encoding="utf-8")
KEY = open(sys.argv[1], encoding="utf-8").read().strip()
# Prompts are read from the shipped package, never from copies, so the test always covers what is in the ZIP.
_V = open("app/album-out-loud/references/vision-prompts.md", encoding="utf-8").read()
P = dict(re.findall(r"^## (Brief|Rich|Question) prompt[^\n]*\n\n([^\n]+)\n", _V, re.M))
assert set(P) == {"Brief", "Rich", "Question"}, "prompt sections not found in vision-prompts.md"
B, R, Q = P["Brief"], P["Rich"], P["Question"]
def call(prompt, img, mt):
    b64 = base64.b64encode(open("app/tuning/images/" + img, "rb").read()).decode()
    body = {"model": "primalabs-ai/Nemotron-3.5-Super-VL-NVFP4", "temperature": 0.2, "max_tokens": mt,
            "chat_template_kwargs": {"enable_thinking": False},
            "messages": [{"role": "user", "content": [{"type": "text", "text": prompt},
                         {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + b64}}]}]}
    r = urllib.request.Request("https://api.primalabs.ai/v1/chat/completions", json.dumps(body).encode(),
                               {"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=90))["choices"][0]["message"]["content"] or ""
GENDER = re.compile(r"\b(man|woman|men|women|boy|girl|he|she|his|her|husband|wife|groom|bride|una adulta|ella|él)\b", re.I)
cases = [
  ("brief EN cake text", B.replace("{language}", "English"), "12_cake_happy_birthday.jpg", 90, lambda o: "birthday" in o.lower() and "Words" in o),
  ("brief EN ID card -> Not described", B.replace("{language}", "English"), "22_synthetic_id_card.jpg", 90, lambda o: "Not described" in o),
  ("brief EN chat screenshot -> Not described", B.replace("{language}", "English"), "23_synthetic_chat_screenshot.jpg", 90, lambda o: "Not described" in o),
  ("brief EN lab sheet -> Not described", B.replace("{language}", "English"), "24_synthetic_lab_sheet.jpg", 90, lambda o: "Not described" in o),
  ("brief EN dark photo flagged", B.replace("{language}", "English"), "25_dark_blurry_group.jpg", 90, lambda o: any(w in o.lower() for w in ["dark", "blur"])),
  ("brief EN group no gender", B.replace("{language}", "English"), "05_wedding_group.jpg", 90, lambda o: not GENDER.search(o)),
  ("brief EN b/w opening", B.replace("{language}", "English"), "11_bw_adult_baby.jpg", 90, lambda o: "black and white" in o.lower() or "old print" in o.lower()),
  ("brief ES street sign verbatim", B.replace("{language}", "Spanish"), "14_spanish_street_sign.jpg", 90, lambda o: "ESCORIAZA" in o.upper()),
  ("brief ES group no gender", B.replace("{language}", "Spanish"), "03_picnic_park.jpg", 90, lambda o: not GENDER.search(o)),
  ("rich EN 3 lines, no gender", R.replace("{language}", "English"), "09_birthday_beach_group.jpg", 170, lambda o: "Line 3" in o or o.count("Words") == 1 and not GENDER.search(o)),
  ("rich EN b/w opening", R.replace("{language}", "English"), "02_bw_birthday_hats.jpg", 170, lambda o: "black and white" in o.lower() or "old print" in o.lower()),
  ("rich EN ID card -> Not described", R.replace("{language}", "English"), "22_synthetic_id_card.jpg", 170, lambda o: "Not described" in o),
  ("rich ES statue said first", R.replace("{language}", "Spanish"), "21_statue_children_dog.jpg", 170, lambda o: any(w in o.lower() for w in ["estatua", "escultura", "bronce"])),
  ("question EN visible", Q.replace("{language}", "English").replace("{rewritten question}", "What is on the table?"), "01_outdoor_party_table.jpg", 80, lambda o: len(o.split()) <= 60 and "UNCLEAR" not in o and "not see" not in o.lower() and any(w in o.lower() for w in ["plate", "glass", "cup", "food", "drink", "bowl"])),
  ("question EN false premise", Q.replace("{language}", "English").replace("{rewritten question}", "What colour is the horse?"), "12_cake_happy_birthday.jpg", 80, lambda o: any(w in o.lower() for w in ["do not see", "don't see", "no horse", "unclear", "not see"])),
]
def run(c):
    name, p, img, mt, ok = c
    try:
        o = call(p, img, mt); return name, ok(o), o.strip().replace("\n", " | ")[:160]
    except Exception as e:
        return name, False, "ERROR " + str(e)[:120]
with cf.ThreadPoolExecutor(15) as ex:
    res = list(ex.map(run, cases))
for n, ok, o in res: print(("PASS" if ok else "FAIL"), "|", n, "|", o)
print("LIVE:", sum(r[1] for r in res), "/", len(res))
