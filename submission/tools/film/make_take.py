# One continuous narration take (eleven_v3, the presenter's clone), then cut per cue using ElevenLabs character timestamps.
# Usage: python -I -X utf8 make_take.py <api_key_file> <voice_name> <stability 0|0.5|1> <take_dir>
import json, os, sys, base64, subprocess, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__))
FF = __import__("os").environ.get("FFMPEG", "ffmpeg")  # path to ffmpeg; set FFMPEG if it is not on PATH
K = open(sys.argv[1]).read().strip(); name, stab, out = sys.argv[2], float(sys.argv[3]), sys.argv[4]; os.makedirs(out, exist_ok=True)
H = {"xi-api-key": K, "Content-Type": "application/json"}
V = [v for v in json.load(urllib.request.urlopen(urllib.request.Request("https://api.elevenlabs.io/v1/voices", headers=H)))["voices"] if v["name"].startswith(name)][0]["voice_id"]
cues = [c for c in json.load(open(os.path.join(HERE, "script.json"), encoding="utf-8")) if c["kind"] == "nar"]
# paragraph breaks between cues give the model room to breathe like a real talk
full, spans = "", []
for c in cues:
    if full: full += "\n\n"
    spans.append((c["id"], len(full), len(full) + len(c["say"]))); full += c["say"]
body = {"text": full, "model_id": "eleven_v3", "voice_settings": {"stability": stab}}
try:
    r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{V}/with-timestamps?output_format=mp3_44100_128", json.dumps(body).encode(), H), timeout=600))
except urllib.error.HTTPError as e: sys.exit(f"HTTP {e.code} {e.read().decode()[:300].replace(K, '***')}")
full_mp3 = os.path.join(out, "full.mp3"); open(full_mp3, "wb").write(base64.b64decode(r["audio_base64"]))
al = r["alignment"]; chars = al["characters"]; st = al["character_start_times_seconds"]; en = al["character_end_times_seconds"]
assert "".join(chars) == full, "alignment text differs from input"
def first_spoken(a, b):  # skip [tags] and spaces at the start
    i, depth = a, 0
    while i < b:
        ch = full[i]
        if ch == "[": depth += 1
        elif ch == "]": depth -= 1
        elif depth == 0 and ch.isalnum(): return i
        i += 1
    return a
def last_spoken(a, b):
    i = b - 1
    while i > a and not full[i].isalnum(): i -= 1
    return i
meta = {}
for cid, a, b in spans:
    s = max(0.0, st[first_spoken(a, b)] - 0.12); e = en[last_spoken(a, b)] + 0.35
    meta[cid] = [round(s, 3), round(e, 3)]
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{s:.3f}", "-to", f"{e:.3f}", "-i", full_mp3, "-af", "afade=t=in:d=0.04,areverse,afade=t=in:d=0.12,areverse", "-c:a", "libmp3lame", "-b:a", "192k", os.path.join(out, f"nar_{cid}.mp3")], check=True)
json.dump(meta, open(os.path.join(out, "cuts.json"), "w"), indent=1)
print("take ok:", out, "| length", round(en[-1], 1), "s")
