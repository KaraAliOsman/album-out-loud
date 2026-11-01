import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

out = sys.argv[1]
plt.rcParams["font.family"] = "Arial"
W, H = 17.0, 5.9
fig = plt.figure(figsize=(W / 2.54, H / 2.54), dpi=220)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

READ = ("#EEF3F8", "#5B7FA6")   # read-only expert step
CHAT = ("#F4F1E8", "#9A8A5A")   # chat with the helper, no command
SAVE = ("#FBE9E2", "#B5543A")   # state change, approval
FAM  = ("#EAF4EC", "#4E8A5B")   # listener and family loop

def box(x, y, w, h, title, sub, c):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.18",
                                fc=c[0], ec=c[1], lw=1.0))
    ax.text(x + w / 2, y + h * 0.64, title, ha="center", va="center", fontsize=7.9, weight="bold", color="#222222")
    ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center", fontsize=6.5, color="#444444", linespacing=1.05)
    return (x, y, w, h)

def arrow(p, q, rad=0.0, color="#555555", ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=7, lw=0.9, color=color,
                                 connectionstyle=f"arc3,rad={rad}", linestyle=ls, shrinkA=1, shrinkB=1))

bw, bh, gap = 2.45, 1.35, 0.30
y1, y2 = 3.85, 1.65
xs = [0.45 + i * (bw + gap) for i in range(6)]
r1 = [
    ("Helper asks", "setup message,\none reply: go", CHAT),
    ("1  Find album", "photo-agent\nug-photo albums", READ),
    ("2  Last letter", "file-agent, since mode\nfind, cat", READ),
    ("3  Choose photos", "photo-agent\nsearch-picture, meta", READ),
    ("4  Describe", "photo-agent\nvision-vlm, vision-ocr", READ),
    ("5  Preview", "whole letter in chat;\nnotes by photo number", CHAT),
]
r2 = [
    ("Helper says save", "the one approval:\nchat save + dialog", SAVE),
    ("6  Free file name", "file-agent\nget-user-dir, find", READ),
    ("7  Save letter", "knowledge-agent\nsave-text", SAVE),
    ("8  Read back", "file-agent\nstat, cat", READ),
    ("Listener hears it", "screen reader,\nPhoto N of M", FAM),
    ("Q1-Q3  Photo N?", "family notes first;\nelse kept for family", FAM),
]
B1 = [box(xs[i], y1, bw, bh, *r1[i]) for i in range(6)]
B2 = [box(xs[i], y2, bw, bh, *r2[i]) for i in range(6)]
for i in range(5):
    arrow((xs[i] + bw, y1 + bh / 2), (xs[i + 1], y1 + bh / 2))
    arrow((xs[i] + bw, y2 + bh / 2), (xs[i + 1], y2 + bh / 2))
# 5 Preview -> Helper says save (wrap to second row)
arrow((xs[5] + bw / 2, y1), (xs[0] + bw / 2, y2 + bh), rad=0.0)
# since loop: kept questions and new photos feed the next letter
gx = xs[5] + bw / 2
ax.plot([gx, gx], [y2, 0.62], color="#4E8A5B", lw=0.9, ls="--")
ax.plot([gx, 0.18], [0.62, 0.62], color="#4E8A5B", lw=0.9, ls="--")
ax.plot([0.18, 0.18], [0.62, y1 + bh / 2], color="#4E8A5B", lw=0.9, ls="--")
ax.annotate("", xy=(xs[0], y1 + bh / 2), xytext=(0.18, y1 + bh / 2),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#4E8A5B", mutation_scale=7))
ax.text(W / 2, 0.36, "Next month: photos since the last letter, plus family answers to the kept questions",
        ha="center", fontsize=6.4, color="#3E7A4B", style="italic")
# legend
lx, ly = 0.45, H - 0.38
for c, t in [(READ, "read-only expert step"), (CHAT, "chat with the helper, no command"),
             (SAVE, "writes a file, approval"), (FAM, "listener and family")]:
    ax.add_patch(FancyBboxPatch((lx, ly - 0.13), 0.32, 0.26, boxstyle="round,pad=0.01,rounding_size=0.05", fc=c[0], ec=c[1], lw=0.8))
    ax.text(lx + 0.42, ly, t, va="center", fontsize=6.2, color="#333333")
    lx += 0.42 + len(t) * 0.105 + 0.45
fig.savefig(out, dpi=220)
print("ok", out)
