# Narration in the presenter's own ElevenLabs voice clone, one clip per "nar" cue of script.json -> audio/nar_<id>.mp3
# Usage: python -I -X utf8 make_voice.py <api_key_file> [--voice-name NAME] [--model eleven_v3] [--only n1,n5] [--samples]
# The key is read at run time and never printed. Only the English narration text is sent.
import json, os, sys, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__)); AU = os.path.join(HERE, "audio")
arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
K = open(sys.argv[1]).read().strip(); model = arg("--model", "eleven_multilingual_v2"); name = arg("--voice-name")
only = set(arg("--only").split(",")) if arg("--only") else None
def api(path, body=None):
    r = urllib.request.Request("https://api.elevenlabs.io" + path, json.dumps(body).encode() if body else None,
                               {"xi-api-key": K, "Content-Type": "application/json"})
    try: return urllib.request.urlopen(r, timeout=180).read()
    except urllib.error.HTTPError as e: sys.exit(f"HTTP {e.code} {e.read().decode()[:240].replace(K, '***')}")
allv = json.loads(api("/v1/voices"))["voices"]
voices = [v for v in allv if v["name"].startswith(name)] if name else [v for v in allv if v["category"] == "cloned"]
if len(voices) != 1: sys.exit("pick the voice with --voice-name: " + ", ".join(v["name"] for v in voices))
V = voices[0]["voice_id"]; print("voice:", voices[0]["name"], "| model:", model)
cues = [c for c in json.load(open(os.path.join(HERE, "script.json"), encoding="utf-8")) if c["kind"] == "nar"]
for i, c in enumerate(cues):
    if only and c["id"] not in only: continue
    body = {"text": c.get("say", c["text"]) if model == "eleven_v3" else c["text"], "model_id": model,
            "voice_settings": {"stability": float(arg("--stability", "0.6")), "similarity_boost": 0.85, "style": float(arg("--style", "0.0")), "use_speaker_boost": True} if model != "eleven_v3" else {"stability": float(arg("--stability", "0.5"))}}
    if model != "eleven_v3":   # v3 does not take request stitching
        if i > 0: body["previous_text"] = cues[i - 1]["text"]
        if i < len(cues) - 1: body["next_text"] = cues[i + 1]["text"]
    open(os.path.join(AU, f"nar_{c['id']}.mp3"), "wb").write(api(f"/v1/text-to-speech/{V}?output_format=mp3_44100_128", body)); print("ok", c["id"])
