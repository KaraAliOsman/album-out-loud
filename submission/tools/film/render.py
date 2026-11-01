# Renders entrega/tools/film/index.html frame by frame (Edge headless, deterministic seek) and encodes it with ffmpeg.
# Run from the project root:
#   uv run --with playwright python -I entrega/tools/film/render.py --still 2,8,20        (PNG stills for review)
#   uv run --with playwright python -I entrega/tools/film/render.py --subs 1 --out entrega/video/AlbumOutLoud_concept_walkthrough_subtitled.mp4
#   uv run --with playwright python -I entrega/tools/film/render.py --subs 0 --out entrega/video/AlbumOutLoud_concept_walkthrough_clean.mp4
# The sound (audio/mix.wav from make_audio.py) is muxed in when --audio 1.
import argparse, os, shutil, subprocess, sys, tempfile, json
from multiprocessing import Pool
sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = "file:///" + os.path.join(HERE, "index.html").replace("\\", "/")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FFMPEG = __import__("os").environ.get("FFMPEG", "ffmpeg")  # path to ffmpeg; set FFMPEG if it is not on PATH
FPS = 30


def open_page(p, subs):
    b = p.chromium.launch(executable_path=EDGE, headless=True, args=["--force-color-profile=srgb", "--hide-scrollbars"])
    pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    pg.goto(PAGE + f"?subs={subs}")
    pg.wait_for_function("window.READY === true", timeout=60000)
    return b, pg


def work(job):
    subs, frames, outdir = job
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, pg = open_page(p, subs)
        for n in frames:
            pg.evaluate(f"window.seek({n / FPS})")
            pg.screenshot(path=os.path.join(outdir, f"f{n:05d}.png"))
        b.close()
    return len(frames)


def meta(subs):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, pg = open_page(p, subs)
        total = pg.evaluate("window.TOTAL"); subtitles = pg.evaluate("window.SUBTITLES")
        b.close()
    return total, subtitles


def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int(round((s % 1) * 1000)) % 1000:03}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subs", default="1"); ap.add_argument("--out", default="")
    ap.add_argument("--still", default=""); ap.add_argument("--audio", default="1"); ap.add_argument("--workers", type=int, default=10)
    a = ap.parse_args()
    if a.still:
        d = os.path.join(tempfile.gettempdir(), "aol_film_stills"); os.makedirs(d, exist_ok=True)
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b, pg = open_page(p, a.subs)
            for t in [float(x) for x in a.still.split(",")]:
                pg.evaluate(f"window.seek({t})"); path = os.path.join(d, f"still_{t:07.2f}.png"); pg.screenshot(path=path); print(path)
            b.close()
        return
    total, subtitles = meta(a.subs)
    n = int(round(total * FPS)); out = os.path.abspath(a.out)
    tmp = os.path.join(tempfile.gettempdir(), "aol_film_frames"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    W = a.workers; chunks = [list(range(i, n, W)) for i in range(W)]
    print(f"rendering {n} frames with {W} workers...")
    with Pool(W) as pool:
        pool.map(work, [(a.subs, c, tmp) for c in chunks])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%05d.png"),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    "-an", out + ".v.mp4"], check=True)
    mix = os.path.join(HERE, "audio", "mix.wav")
    if a.audio == "1" and os.path.exists(mix):
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", out + ".v.mp4", "-i", mix, "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                        "-t", f"{total:.3f}", "-movflags", "+faststart", out], check=True); os.remove(out + ".v.mp4")
    else: os.replace(out + ".v.mp4", out)
    shutil.rmtree(tmp, ignore_errors=True)
    srt = os.path.join(os.path.dirname(out), "AlbumOutLoud_film.en.srt")
    open(srt, "w", encoding="utf-8", newline="\n").write("\n".join(f"{i + 1}\n{ts(s)} --> {ts(e)}\n{t}\n" for i, (s, e, t) in enumerate(subtitles)))
    print("video:", out, f"{total:.1f} s"); print("srt:", srt)


if __name__ == "__main__":
    main()
