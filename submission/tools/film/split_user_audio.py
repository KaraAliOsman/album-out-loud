# Cuts the presenter's own ElevenLabs narration (one file) into the film's cues.
# Speech-to-text word timestamps (ElevenLabs scribe_v1) are aligned to the script words; each cue becomes audio/nar_<id>.mp3.
# Usage: python -I -X utf8 split_user_audio.py <api_key_file> <narration.mp3>
import json, os, re, sys, uuid, difflib, subprocess, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); AU = os.path.join(HERE, "audio")
FF = __import__("os").environ.get("FFMPEG", "ffmpeg")  # path to ffmpeg; set FFMPEG if it is not on PATH
K = open(sys.argv[1]).read().strip(); SRC = sys.argv[2]
cache = os.path.join(AU, "user_stt.json")
if not os.path.exists(cache):
    b = uuid.uuid4().hex
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"model_id\"\r\n\r\nscribe_v1\r\n--{b}\r\nContent-Disposition: form-data; name=\"language_code\"\r\n\r\nen\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"timestamps_granularity\"\r\n\r\nword\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n").encode() + open(SRC, "rb").read() + f"\r\n--{b}--\r\n".encode()
    r = json.load(urllib.request.urlopen(urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", body, {"xi-api-key": K, "Content-Type": f"multipart/form-data; boundary={b}"}), timeout=300))
    json.dump(r, open(cache, "w"), indent=1)
r = json.load(open(cache))
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower().replace("twenty-three", "23").replace("twenty-four", "24"))
hw = [(norm(w["text"]), w["start"], w["end"]) for w in r["words"] if w.get("type", "word") == "word" and norm(w["text"])]
cues = [c for c in json.load(open(os.path.join(HERE, "script.json"), encoding="utf-8")) if c["kind"] == "nar"]
ref = []
for c in cues:
    for w in re.sub(r"\[[^\]]*\]", " ", c["say"]).replace("Twenty-three", "23").replace("twenty-four", "24").split():
        if norm(w): ref.append((norm(w), c["id"]))
sm = difflib.SequenceMatcher(None, [x[0] for x in ref], [x[0] for x in hw], autojunk=False)
print("word match:", round(sm.ratio(), 3), "| transcript:", r["text"][:120], "...")
pos = {}
for a, b2, n in sm.get_matching_blocks():
    for k in range(n): pos[a + k] = b2 + k
span = {}
for i, (w, cid) in enumerate(ref):
    if i in pos: s, e = hw[pos[i]][1], hw[pos[i]][2]; span.setdefault(cid, [s, e]); span[cid][0] = min(span[cid][0], s); span[cid][1] = max(span[cid][1], e)
ids = [c["id"] for c in cues]; total = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", subprocess.run([FF, "-i", SRC], capture_output=True, text=True).stderr).group(3)) + 60 * 1
for k, cid in enumerate(ids):
    s, e = span[cid]
    # cut in the middle of the gap to the neighbours, so breaths and tails are kept
    prev_e = span[ids[k - 1]][1] if k else 0.0; nxt_s = span[ids[k + 1]][0] if k + 1 < len(ids) else e + 0.6
    cs = max(prev_e, s - min(0.25, (s - prev_e) / 2)); ce = min(nxt_s, e + min(0.45, (nxt_s - e) / 2))
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{cs:.3f}", "-to", f"{ce:.3f}", "-i", SRC, "-af", "afade=t=in:d=0.03,areverse,afade=t=in:d=0.08,areverse",
                    "-c:a", "libmp3lame", "-b:a", "192k", os.path.join(AU, f"nar_{cid}.mp3")], check=True)
    print(f"{cid:4} {cs:6.2f} -> {ce:6.2f}  ({ce - cs:4.1f}s)")
missing = [ref[i][0] + "@" + ref[i][1] for i in range(len(ref)) if i not in pos]
print("script words not heard:", missing)
