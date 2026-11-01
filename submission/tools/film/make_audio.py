# Builds every audio piece of the film and writes cues.js (the timeline the page animates to).
#  - sr cues: Windows "Microsoft Zira" (what a real screen reader sounds like), with word timings from SAPI.
#  - nar cues: audio/nar_<id>.mp3 if present (presenter's voice), otherwise a duration estimate (silent).
#  - sound design: synthesized with ffmpeg (no third-party music).
# Run from this folder: python -I -X utf8 make_audio.py [--sr]   (--sr regenerates the screen-reader clips)
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); AU = os.path.join(HERE, "audio"); os.makedirs(AU, exist_ok=True)
FF = __import__("os").environ.get("FFMPEG", "ffmpeg")  # path to ffmpeg; set FFMPEG if it is not on PATH
cues = json.load(open(os.path.join(HERE, "script.json"), encoding="utf-8"))
def dur(p):
    r = subprocess.run([FF, "-i", p], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r); return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])
def gain(p):
    r = subprocess.run([FF, "-i", p, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    return round(-20.0 - float(re.search(r"mean_volume: ([-\d.]+) dB", r)[1]), 2)
def eleven_sr(cid, text, key_file, voice_name):
    import urllib.request, base64
    K = open(key_file).read().strip(); H = {"xi-api-key": K, "Content-Type": "application/json"}
    vs = json.load(urllib.request.urlopen(urllib.request.Request("https://api.elevenlabs.io/v1/voices", headers=H)))["voices"]
    V = [v for v in vs if v["name"].startswith(voice_name)][0]["voice_id"]
    body = {"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.85, "similarity_boost": 0.75, "style": 0.0, "speed": 1.08}}
    r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{V}/with-timestamps?output_format=mp3_44100_128", json.dumps(body).encode(), H), timeout=180))
    mp3 = os.path.join(AU, f"{cid}.mp3"); open(mp3, "wb").write(base64.b64decode(r["audio_base64"]))
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", mp3, os.path.join(AU, f"{cid}.wav")], check=True); os.remove(mp3)
    al = r["alignment"]; st = al["character_start_times_seconds"]; ev = []
    for m in re.finditer(r"\S+", text): ev.append([st[m.start()], m.start(), len(m.group())])
    return ev
def sapi(cid, text):
    wav = os.path.join(AU, f"{cid}.wav"); txt = wav + ".txt"; open(txt, "w", encoding="utf-8").write(text)
    ps = ("Add-Type -AssemblyName System.Speech; $s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
          "$s.SelectVoice('Microsoft Zira Desktop'); $s.Rate=1; $global:w=New-Object System.Collections.ArrayList; "
          "$s.add_SpeakProgress({param($o,$e) [void]$global:w.Add(\"$($e.AudioPosition.TotalMilliseconds)|$($e.CharacterPosition)|$($e.CharacterCount)\")}); "
          f"$s.SetOutputToWaveFile('{wav}'); $s.Speak([IO.File]::ReadAllText('{txt}')); $s.Dispose(); $global:w")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, check=True).stdout
    ev = {}
    for line in out.split():
        ms, cp, cc = line.split("|"); ev.setdefault(int(cp), (float(ms) / 1000, int(cc)))  # first event per word
    os.remove(txt); return [[t, cp, cc] for cp, (t, cc) in sorted(ev.items())]
regen = "--sr" in sys.argv
timing_file = os.path.join(AU, "sr_words.json")
words = json.load(open(timing_file)) if os.path.exists(timing_file) and not regen else {}
t = 0.0; total_voice = []
for c in cues:
    t += c.get("pre", 0.0); c["t0"] = round(t, 3)
    if c["kind"] == "sr":
        if c["id"] not in words:
            words[c["id"]] = eleven_sr(c["id"], c["text"], sys.argv[sys.argv.index("--sr-eleven") + 1], sys.argv[sys.argv.index("--sr-eleven") + 2]) if "--sr-eleven" in sys.argv else sapi(c["id"], c["text"])
        c["words"] = words[c["id"]]; c["d"] = round(dur(os.path.join(AU, c["id"] + ".wav")), 3); total_voice.append((c["id"] + ".wav", c["t0"], gain(os.path.join(AU, c["id"] + ".wav"))))
    elif c["kind"] == "nar":
        p = os.path.join(AU, f"nar_{c['id']}.mp3")
        if os.path.exists(p): c["d"] = round(dur(p), 3); c["real"] = True; total_voice.append((f"nar_{c['id']}.mp3", c["t0"], gain(p)))
        else: c["d"] = round(len(c["text"].split()) / 2.55 + 0.25, 3); c["real"] = False
    t += c["d"]; c["t1"] = round(t, 3)
json.dump(words, open(timing_file, "w"))
TOTAL = round(t, 2)
open(os.path.join(HERE, "cues.js"), "w", encoding="utf-8").write("window.CUES = " + json.dumps(cues, ensure_ascii=False, indent=1) + ";\nwindow.TOTAL_FROM_CUES = " + str(TOTAL) + ";\n")
print("total", TOTAL, "s |", "narration real:", sum(1 for c in cues if c.get("real")), "/", sum(1 for c in cues if c["kind"] == "nar"))
for c in cues: print(f"  {c['id']:5} {c['kind']:3} {c['t0']:6.2f} -> {c['t1']:6.2f}")
# ---- mix: voice clips at their times + a soft synthesized bed + small ticks
C = {c["id"]: c for c in cues}
args = [FF, "-y", "-loglevel", "error"]; fl = []; n = 0; labels = []
for f, at, g in total_voice:
    args += ["-i", os.path.join(AU, f)]
    fl.append(f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={g}dB,adelay={int(at*1000)}:all=1[v{n}]"); labels.append(f"[v{n}]"); n += 1
# bed: two low sines (A2, E3) slowly breathing + filtered noise air; swells at the letter and the reveal
bed = (f"sine=f=110:d={TOTAL}:r=48000,volume=0.05[b1];sine=f=164.81:d={TOTAL}:r=48000,volume=0.03[b2];"
       f"anoisesrc=d={TOTAL}:r=48000:c=pink:a=0.02,lowpass=f=900[b3];"
       f"[b1][b2][b3]amix=inputs=3:normalize=0,tremolo=f=0.11:d=0.35,lowpass=f=1200,"
       f"volume='0.55+0.45*between(t,{C['sr3']['t0']-1},{C['sr3']['t1']+1})+0.9*gte(t,{C['n13']['t0']})':eval=frame,"
       f"afade=t=in:st=0:d=3,afade=t=out:st={TOTAL-3}:d=3,aformat=channel_layouts=stereo[bed]")
fl.append(bed); labels.append("[bed]")
fl.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,apad=whole_dur={TOTAL},atrim=0:{TOTAL}[o]")
if '--voice-only' in sys.argv: labels = [l for l in labels if l != '[bed]']; fl[-1] = ''.join(labels) + f'amix=inputs={len(labels)}:normalize=0,apad,atrim=0:{TOTAL}[o]'; fl = [f for f in fl if not f.startswith('sine=')]
args += ["-filter_complex", ";".join(fl), "-map", "[o]", "-ar", "48000", os.path.join(AU, "mix.wav")]
raw = os.path.join(AU, "mix_raw.wav"); args[-1] = raw; subprocess.run(args, check=True)
# static loudness to -16 LUFS (two-pass, no time shift), then a soft limiter for peaks
r = subprocess.run([FF, "-i", raw, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+([-\d.]+) LUFS", r)[-1])
subprocess.run([FF, "-y", "-loglevel", "error", "-i", raw, "-af", f"volume={-16 - I:.2f}dB,alimiter=limit=0.89:attack=5:release=60:level=disabled", "-ar", "48000", os.path.join(AU, "mix.wav")], check=True)
os.remove(raw); print("mix:", os.path.join(AU, "mix.wav"), "| measured", I, "LUFS -> -16")
