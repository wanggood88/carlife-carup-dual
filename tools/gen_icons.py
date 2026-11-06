#!/usr/bin/env python3
"""Generate iOS style (squircle) icons for the merged app."""
import math, os
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get("SRC_DIR") or os.path.join(ROOT, "work")
OUT_DIR = os.environ.get("MERGE_OUT") or os.path.join(ROOT, "build", "merged")

S = 4  # supersample factor


def squircle_mask(size, radius_ratio=0.235, n=5.0):
    w = size
    m = Image.new("L", (w, w), 0)
    d = ImageDraw.Draw(m)
    # superellipse
    pts = []
    a = w / 2.0
    c = w / 2.0
    for i in range(720):
        t = 2 * math.pi * i / 720
        ct, st = math.cos(t), math.sin(t)
        x = c + a * math.copysign(abs(ct) ** (2.0 / n), ct)
        y = c + a * math.copysign(abs(st) ** (2.0 / n), st)
        pts.append((x, y))
    d.polygon(pts, fill=255)
    return m


def gradient(size, c1, c2, angle=135):
    w = size
    base = Image.new("RGB", (w, w))
    px = base.load()
    rad = math.radians(angle)
    dx, dy = math.cos(rad), math.sin(rad)
    # projection range
    vals = [0, dx * w, dy * w, dx * w + dy * w]
    lo, hi = min(vals), max(vals)
    for y in range(w):
        for x in range(w):
            t = ((x * dx + y * dy) - lo) / (hi - lo)
            t = max(0.0, min(1.0, t))
            px[x, y] = (int(c1[0] + (c2[0] - c1[0]) * t),
                        int(c1[1] + (c2[1] - c1[1]) * t),
                        int(c1[2] + (c2[2] - c1[2]) * t))
    return base


def squircle_image(size_out, c1, c2, angle=135):
    w = size_out * S
    img = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    grad = gradient(w, c1, c2, angle).convert("RGBA")
    mask = squircle_mask(w)
    img.paste(grad, (0, 0), mask)
    # top gloss
    gloss = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gloss)
    gd.ellipse([-w * 0.35, -w * 0.9, w * 1.35, w * 0.45], fill=(255, 255, 255, 26))
    img = Image.alpha_composite(img, Image.composite(gloss, Image.new("RGBA", (w, w), (0, 0, 0, 0)), mask))
    return img


def draw_phone(d, w, color=(255, 255, 255, 255), box=None):
    x0, y0, x1, y1 = box
    r = (x1 - x0) * 0.22
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, outline=color, width=int(w * 0.05))
    # speaker notch
    bw = (x1 - x0) * 0.24
    d.rounded_rectangle([(x0 + x1) / 2 - bw / 2, y0 + (y1 - y0) * 0.085,
                         (x0 + x1) / 2 + bw / 2, y0 + (y1 - y0) * 0.115],
                        radius=(y1 - y0) * 0.015, fill=color)
    # home indicator
    hw = (x1 - x0) * 0.34
    d.rounded_rectangle([(x0 + x1) / 2 - hw / 2, y1 - (y1 - y0) * 0.115,
                         (x0 + x1) / 2 + hw / 2, y1 - (y1 - y0) * 0.075],
                        radius=(y1 - y0) * 0.02, fill=color)


def draw_car(d, w, color=(255, 255, 255, 255)):
    # simple car silhouette
    cx, cy = w / 2, w / 2
    body_w = w * 0.50
    body_h = w * 0.135
    top = cy + w * 0.02
    # cabin
    cab = [(cx - body_w * 0.30, top - w * 0.13), (cx + body_w * 0.30, top - w * 0.13),
           (cx + body_w * 0.42, top), (cx - body_w * 0.42, top)]
    d.polygon(cab, fill=color)
    d.rounded_rectangle([cx - body_w / 2, top, cx + body_w / 2, top + body_h],
                        radius=body_h * 0.45, fill=color)
    for sx in (-1, 1):
        d.ellipse([cx + sx * body_w * 0.28 - w * 0.055, top + body_h - w * 0.045,
                   cx + sx * body_w * 0.28 + w * 0.055, top + body_h + w * 0.055],
                  fill=color)


def build(path, size, c1, c2, glyph, angle=135):
    img = squircle_image(size, c1, c2, angle)
    w = img.size[0]
    d = ImageDraw.Draw(img)
    if glyph == "phone":
        draw_phone(d, w, box=(w * 0.355, w * 0.20, w * 0.645, w * 0.80))
    elif glyph == "car":
        draw_car(d, w)
    elif glyph == "dual":
        # two overlapping app tiles
        bw = w * 0.30
        for i, (dx, dy, alpha) in enumerate([(-0.11, -0.02, 255), (0.11, 0.06, 255)]):
            x0 = w * (0.5 + dx) - bw / 2
            y0 = w * (0.5 + dy) - bw / 2
            d.rounded_rectangle([x0, y0, x0 + bw, y0 + bw], radius=bw * 0.30,
                                outline=(255, 255, 255, alpha), width=int(w * 0.035))
    img = img.resize((size, size), Image.LANCZOS)
    img.save(path, "PNG")
    print("wrote", path, size)


if __name__ == "__main__":
    res = os.path.join(OUT_DIR, "res")
    build(f"{res}/drawable-nodpi/ic_dual_carlife.png", 216, (10, 132, 255), (90, 200, 250), "phone")
    build(f"{res}/drawable-nodpi/ic_dual_carup.png", 216, (94, 92, 230), (191, 90, 242), "car")
    for dpi, px in [("drawable-mdpi-v4", 48), ("drawable-hdpi-v4", 144),
                    ("drawable-xhdpi-v4", 144), ("drawable-xxhdpi-v4", 192)]:
        build(f"{res}/{dpi}/ic_launcher.png", px, (10, 132, 255), (150, 90, 245), "dual", 120)


def gen_ui_icons():
    from PIL import ImageDraw
    res = os.path.join(OUT_DIR, "res")
    blue = (0, 122, 255, 255)
    # back chevron (24dp @3x)
    s = 3
    im = Image.new("RGBA", (24 * s, 24 * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.line([(16 * s, 5 * s), (9 * s, 12 * s), (16 * s, 19 * s)], fill=blue, width=int(2.2 * s), joint="curve")
    im.resize((24 * s, 24 * s), Image.LANCZOS).save(f"{res}/drawable-nodpi/ios_ic_back.png")
    print("wrote ios_ic_back")

    # connect illustration: phone + wifi arcs
    W = 360
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # phone body (left)
    d.rounded_rectangle([W * 0.16, W * 0.20, W * 0.46, W * 0.80], radius=W * 0.06,
                        outline=blue, width=int(W * 0.028))
    d.rounded_rectangle([W * 0.245, W * 0.285, W * 0.375, W * 0.325], radius=W * 0.012, fill=(0, 122, 255, 60))
    # wifi arcs (right)
    import math
    cx, cy = W * 0.735, W * 0.62
    for i, r in enumerate([W * 0.085, W * 0.155, W * 0.225]):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340,
              fill=blue, width=int(W * 0.028))
    d.ellipse([cx - W * 0.022, cy - W * 0.022, cx + W * 0.022, cy + W * 0.022], fill=blue)
    im.save(f"{res}/drawable-nodpi/ios_ic_connect.png")
    print("wrote ios_ic_connect")


gen_ui_icons()
