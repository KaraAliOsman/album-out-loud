"""Draw the presentation images for Album Out Loud.

Usage (from any folder):
    uv run --with matplotlib --with pillow python -I make_images.py ROOT
ROOT is the project root. Writes flow_diagram.png, letter_card.png and
comparison.png into ROOT/submission/assets.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(sys.argv[1])
OUT = ROOT / "entrega" / "assets"
IMAGES = ROOT / "app" / "tuning" / "images"
LETTER = OUT / "sample_letter.txt"
FONTS = Path("C:/Windows/Fonts")

INK = (28, 33, 40)
MUTED = (92, 100, 112)
LINE = (206, 211, 218)
BG = (250, 249, 246)
WHITE = (255, 255, 255)

# One tint and one strong colour per lane.
LANES = {
    "chat": ((236, 239, 244), (70, 84, 110)),
    "photo": ((226, 242, 240), (20, 110, 100)),
    "file": ((250, 240, 222), (150, 92, 10)),
    "knowledge": ((238, 233, 248), (95, 70, 160)),
}
APPROVAL = (196, 64, 40)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


F = {
    "title": font("segoeuib.ttf", 40),
    "sub": font("segoeui.ttf", 22),
    "lane": font("segoeuib.ttf", 22),
    "lane_s": font("segoeui.ttf", 17),
    "step": font("segoeuib.ttf", 21),
    "body": font("segoeui.ttf", 18),
    "small": font("segoeui.ttf", 16),
    "small_b": font("segoeuib.ttf", 16),
    "num": font("segoeuib.ttf", 20),
}


def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if draw.textlength(test, font=fnt) <= width:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, width, fill, spacing=6):
    x, y = xy
    asc, desc = fnt.getmetrics()
    lh = asc + desc + spacing
    for ln in wrap(draw, text, fnt, width):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def block_height(draw, text, fnt, width, spacing=6):
    asc, desc = fnt.getmetrics()
    return len(wrap(draw, text, fnt, width)) * (asc + desc + spacing)


def arrow(draw, pts, fill, width=3, head=11):
    draw.line(pts, fill=fill, width=width, joint="curve")
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    if x1 == x2:
        s = 1 if y2 > y1 else -1
        draw.polygon([(x2, y2), (x2 - head * 0.7, y2 - s * head), (x2 + head * 0.7, y2 - s * head)], fill=fill)
    else:
        s = 1 if x2 > x1 else -1
        draw.polygon([(x2, y2), (x2 - s * head, y2 - head * 0.7), (x2 - s * head, y2 + head * 0.7)], fill=fill)


# ---------------------------------------------------------------- flow diagram
def flow_diagram():
    W = 1600
    margin = 48
    lane_keys = ["chat", "photo", "file", "knowledge"]
    lane_titles = {
        "chat": ("In chat", "the Skill and the helper"),
        "photo": ("photo-agent", "ug-photo"),
        "file": ("file-agent", "ug-filesystem, file-workflow"),
        "knowledge": ("knowledge-agent", "ug-knowledge"),
    }
    steps = [
        ("chat", "", "Setup message",
         "Album, listener and language, brief or rich, photo limit, who signs the notes, new or since the last letter. One reply: go.", "no command"),
        ("photo", "1", "Find the album",
         "Regular, folder, condition or custom album only. Never a face, baby or pet album.", "read only"),
        ("file", "2", "Read the last letter",
         "Since mode only: newest photo checked, listed photos, questions kept for the family.", "read only"),
        ("photo", "3", "Choose the photos",
         "Still photos in capture order, selection rule 1, metadata in one call.", "read only"),
        ("photo", "4", "Describe, at most 4 per group",
         "vision-vlm with a fixed prompt; vision-ocr only when words were seen. Private papers stay Not described.", "read only"),
        ("chat", "5", "Preview the whole letter",
         "The helper adds family notes by photo number, removes photos, answers open questions, then says save.", "nothing saved yet"),
        ("file", "6", "Find the folder and a free name",
         "Real letter folder and the names already there, so nothing is overwritten.", "read only"),
        ("knowledge", "7", "Save one text file",
         "save-text with the exact letter shown in the preview.", "THE ONE APPROVAL"),
        ("file", "8", "Read it back",
         "First and last 300 bytes and the size must match the letter.", "read only"),
    ]

    lane_w = (W - 2 * margin) // 4
    box_w = lane_w - 28
    header_top = 150
    header_h = 74
    first_row = header_top + header_h + 26
    gap = 34

    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    heights = []
    for lane, num, title, body, tag in steps:
        th = block_height(probe, title, F["step"], box_w - 88, 2)
        h = 16 + th + 10 + block_height(probe, body, F["body"], box_w - 36) + 34 + 12
        heights.append(max(h, 112))
    total = first_row + sum(heights) + gap * (len(steps) - 1) + 210
    img = Image.new("RGB", (W, total), BG)
    d = ImageDraw.Draw(img)

    d.text((margin, 40), "One listening letter: eight steps, three experts, one approval", font=F["title"], fill=INK)
    d.text((margin, 96), "Letter mode of the Album Out Loud Skill. Each delegate step sends one plain instruction to one expert and waits for its result.",
           font=F["sub"], fill=MUTED)

    # lane backgrounds and headers
    for i, key in enumerate(lane_keys):
        x0 = margin + i * lane_w
        tint, strong = LANES[key]
        d.rounded_rectangle([x0 + 4, header_top, x0 + lane_w - 4, total - 150], radius=18, fill=tint)
        t1, t2 = lane_titles[key]
        d.text((x0 + 22, header_top + 12), t1, font=F["lane"], fill=strong)
        d.text((x0 + 22, header_top + 44), t2, font=F["lane_s"], fill=MUTED)

    # boxes
    y = first_row
    boxes = []
    for (lane, num, title, body, tag), h in zip(steps, heights):
        i = lane_keys.index(lane)
        x0 = margin + i * lane_w + 14
        tint, strong = LANES[lane]
        is_save = num == "7"
        outline = APPROVAL if is_save else strong
        d.rounded_rectangle([x0, y, x0 + box_w, y + h], radius=14, fill=WHITE, outline=outline, width=4 if is_save else 2)
        tx = x0 + 18
        if num:
            r = 17
            cx, cy = x0 + 18 + r, y + 16 + r - 2
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=outline)
            d.text((cx, cy), num, font=F["num"], fill=WHITE, anchor="mm")
            tx = x0 + 18 + 2 * r + 12
        ty_end = text_block(d, (tx, y + 16), title, F["step"], box_w - 88, INK, 2)
        by = text_block(d, (x0 + 18, ty_end + 10), body, F["body"], box_w - 36, INK)
        tag_font = F["small_b"]
        tag_fill = APPROVAL if is_save else MUTED
        d.text((x0 + 18, y + h - 30), tag, font=tag_font, fill=tag_fill)
        boxes.append((x0, y, x0 + box_w, y + h))
        y += h + gap

    # connectors
    for a, b in zip(boxes, boxes[1:]):
        ax = (a[0] + a[2]) // 2
        bx = (b[0] + b[2]) // 2
        midy = a[3] + gap // 2
        if ax == bx:
            arrow(d, [(ax, a[3]), (bx, b[1] - 2)], MUTED)
        else:
            arrow(d, [(ax, a[3]), (ax, midy), (bx, midy), (bx, b[1] - 2)], MUTED)

    # approval note beside step 7
    s7 = boxes[7]
    note_x0 = margin + 14
    note_w = 2 * lane_w - 28
    note = ("Approval, once per letter: the helper reads the whole preview and says save; "
            "Uliya may then ask to confirm the save. Steps 1 to 6 and 8 only read.")
    nh = block_height(d, note, F["body"], note_w - 40) + 28
    ny = s7[1] + (s7[3] - s7[1] - nh) // 2
    d.rounded_rectangle([note_x0, ny, note_x0 + note_w, ny + nh], radius=12, fill=(253, 236, 231), outline=APPROVAL, width=2)
    text_block(d, (note_x0 + 20, ny + 12), note, F["body"], note_w - 40, (120, 36, 20))

    # footer
    fy = total - 128
    foot = [
        "Only step 7 changes anything: it adds one new text file. Photos is never changed, and names come only from the family notes.",
        "A letter of the default 6 photos needs 7 delegations (step 4 runs twice), plus step 2 in since mode.",
        "Question mode is separate: read one entry, answer from the family notes or ask vision-vlm, and keep what the photo cannot answer for the family (its own optional save).",
    ]
    for ln in foot:
        fy = text_block(d, (margin, fy), ln, F["small"], W - 2 * margin, MUTED, spacing=4)

    img.save(OUT / "flow_diagram.png", optimize=True)
    return img.size


# ---------------------------------------------------------------- letter card
LABEL_COLOURS = {
    "When:": (70, 84, 110),
    "Where:": (70, 84, 110),
    "Family says:": (20, 110, 100),
    "AI guess:": (150, 92, 10),
    "Words in the photo, AI reading:": (95, 70, 160),
    "Words in the photo:": (95, 70, 160),
}


def letter_card():
    lines = LETTER.read_text(encoding="utf-8").split("\n")
    head = lines[0:3]
    # first two entries
    entries, cur = [], []
    for ln in lines[4:]:
        if ln.startswith("Photo ") and " of " in ln and cur:
            entries.append(cur)
            cur = []
        if ln == "":
            if cur:
                entries.append(cur)
                cur = []
            if len(entries) >= 2:
                break
            continue
        cur.append(ln)
    entries = entries[:2]
    thumbs = ["11_bw_adult_baby.jpg", "12_cake_happy_birthday.jpg"]

    W = 1600
    pad = 64
    thumb_w = 330
    text_x = pad + thumb_w + 44
    text_w = W - text_x - pad - 20
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    big = font("segoeui.ttf", 27)
    big_b = font("segoeuib.ttf", 27)
    head_f = font("segoeui.ttf", 22)

    def entry_h(entry):
        h = 0
        for ln in entry:
            h += block_height(probe, ln, big, text_w, spacing=8) + 4
        return h

    head_h = sum(block_height(probe, ln, head_f, W - 2 * pad - 40, spacing=6) + 6 for ln in head)
    eh = [max(entry_h(e), 250) for e in entries]
    H = 150 + head_h + 40 + sum(eh) + 60 * len(eh) + 120
    img = Image.new("RGB", (W, H), (240, 237, 230))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([28, 28, W - 28, H - 28], radius=26, fill=WHITE, outline=LINE, width=2)

    d.text((pad, 58), "A listening letter, as the listener hears it", font=F["title"], fill=INK)
    y = 124
    for ln in head:
        y = text_block(d, (pad, y), ln, head_f, W - 2 * pad - 40, MUTED, spacing=6) + 6
    y += 22
    d.line([(pad, y), (W - pad, y)], fill=LINE, width=2)
    y += 34

    for entry, thumb, h in zip(entries, thumbs, eh):
        im = Image.open(IMAGES / thumb).convert("RGB")
        im.thumbnail((thumb_w, thumb_w))
        img.paste(im, (pad, y + 4))
        d.rectangle([pad, y + 4, pad + im.width - 1, y + 4 + im.height - 1], outline=LINE, width=1)
        ty = y
        for ln in entry:
            label = next((k for k in sorted(LABEL_COLOURS, key=len, reverse=True) if ln.startswith(k)), None)
            if ln.startswith("Photo "):
                d.text((text_x, ty), ln, font=big_b, fill=INK)
                ty += block_height(d, ln, big_b, text_w, spacing=8) + 4
                continue
            if label:
                rest = ln[len(label):].strip()
                lw = d.textlength(label + " ", font=big_b)
                colour = LABEL_COLOURS[label]
                d.text((text_x, ty), label, font=big_b, fill=colour)
                # wrap the rest, first line shorter
                first_lines = wrap(d, rest, big, text_w - lw)
                first = first_lines[0] if first_lines else ""
                d.text((text_x + lw, ty), first, font=big, fill=INK)
                asc, desc = big.getmetrics()
                ty += asc + desc + 8
                remainder = rest[len(first):].strip()
                if remainder:
                    ty = text_block(d, (text_x, ty), remainder, big, text_w, INK, spacing=8)
                ty += 4
            else:
                ty = text_block(d, (text_x, ty), ln, big, text_w, INK, spacing=8) + 4
        y += h + 60

    cap = ("Sample letter. Photos: CC0, Willem van de Poll and Brassluff, via Wikimedia Commons. "
           "AI guess and Words lines are real outputs of a cloud stand-in model during prompt tuning; "
           "family notes, dates and places are invented. The listener hears plain text through a screen reader; the photos are shown here for sighted readers.")
    text_block(d, (pad, H - 128), cap, F["small"], W - 2 * pad, MUTED, spacing=4)
    img.save(OUT / "letter_card.png", optimize=True)
    return img.size


# ---------------------------------------------------------------- comparison
def comparison():
    cols = [
        "",
        "Made for",
        "Who says who is in the photo",
        "Source named on every line",
        "Questions from the listener",
        "New photos since last time",
        "Where the photos go",
    ]
    rows = [
        ("Phone describers", "built-in screen-reader and app image descriptions", [
            "The blind user, one photo at a time, on demand",
            "No one. The AI describes what it sees",
            "No",
            "Asked to the AI, which answers or guesses",
            "No",
            "On the phone or in the cloud, depending on the tool",
        ]),
        ("Photo highlights and reminiscence tools", "AI memory reels and caregiver prompts", [
            "Sighted viewers, or a caregiver guiding a session",
            "Face grouping or the caregiver; not shown to the listener",
            "No",
            "None, or questions suggested to the caregiver",
            "Sometimes, as new highlight reels",
            "Varies: phone, cloud or local",
        ]),
        ("Album Out Loud", "this Skill", [
            "A blind or low-vision relative with a screen reader; plain text, numbered photos",
            "Only the family notes, which come before the AI guess",
            "Yes: When, Where, Family says, AI guess, Words in the photo",
            "Asked through the helper; what the photo cannot answer is kept for the family and answered in the next letter",
            "Yes: since the last letter",
            "Only to vision-vlm and vision-ocr of the NAS photo expert (on-device run not yet verified)",
        ]),
    ]
    W = 1600
    pad = 48
    first_w = 250
    other_w = (W - 2 * pad - first_w) // 6
    widths = [first_w] + [other_w] * 6
    cell_pad = 16
    hf = font("segoeuib.ttf", 19)
    bf = font("segoeui.ttf", 18)
    nf = font("segoeuib.ttf", 21)
    sf = font("segoeui.ttf", 16)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))

    head_h = max(block_height(probe, c, hf, w - 2 * cell_pad, 4) for c, w in zip(cols, widths)) + 2 * cell_pad
    row_hs = []
    for name, sub, cells in rows:
        hs = [block_height(probe, name, nf, first_w - 2 * cell_pad, 4) + block_height(probe, sub, sf, first_w - 2 * cell_pad, 4)]
        hs += [block_height(probe, c, bf, w - 2 * cell_pad, 5) for c, w in zip(cells, widths[1:])]
        row_hs.append(max(hs) + 2 * cell_pad)
    top = 140
    H = top + head_h + sum(row_hs) + 120
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    d.text((pad, 36), "What the listener gets, compared", font=F["title"], fill=INK)
    d.text((pad, 90), "Album Out Loud does not compete on describing pixels. It adds the family, the source of each line, and a question loop.",
           font=F["sub"], fill=MUTED)

    x = pad
    y = top
    d.rectangle([pad, y, W - pad, y + head_h], fill=(236, 239, 244))
    for c, w in zip(cols, widths):
        text_block(d, (x + cell_pad, y + cell_pad), c, hf, w - 2 * cell_pad, INK, 4)
        x += w
    y += head_h
    for ri, ((name, sub, cells), rh) in enumerate(zip(rows, row_hs)):
        ours = ri == 2
        if ours:
            d.rectangle([pad, y, W - pad, y + rh], fill=(226, 242, 240))
        x = pad
        ny = text_block(d, (x + cell_pad, y + cell_pad), name, nf, first_w - 2 * cell_pad, (20, 110, 100) if ours else INK, 4)
        text_block(d, (x + cell_pad, ny + 2), sub, sf, first_w - 2 * cell_pad, MUTED, 4)
        x += first_w
        for c, w in zip(cells, widths[1:]):
            text_block(d, (x + cell_pad, y + cell_pad), c, bf, w - 2 * cell_pad, INK, 5)
            x += w
        d.line([(pad, y), (W - pad, y)], fill=LINE, width=2)
        y += rh
    d.line([(pad, y), (W - pad, y)], fill=LINE, width=2)
    x = pad
    for w in widths[:-1]:
        x += w
        d.line([(x, top), (x, y)], fill=LINE, width=1)
    note = ("Other rows summarise common categories of tools from their public descriptions, not any single product. "
            "Album Out Loud is a Skill package that has not yet run on a NAS; its prompts were tuned with cloud stand-in models on openly licensed images.")
    text_block(d, (pad, y + 24), note, F["small"], W - 2 * pad, MUTED, 4)
    img.save(OUT / "comparison.png", optimize=True)
    return img.size


if __name__ == "__main__":
    print("flow_diagram.png", flow_diagram())
    print("letter_card.png", letter_card())
    print("comparison.png", comparison())
