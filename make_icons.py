#!/usr/bin/env python3
"""Generate PWA / apple-touch icons: dark tile with the formula's fraction motif."""

from PIL import Image, ImageDraw

BG = (13, 17, 23)
ACCENT = (88, 166, 255)
TEXT = (230, 237, 243)


def make_icon(size: int, path: str) -> None:
    img = Image.new("RGB", (size, size), BG)
    d = ImageDraw.Draw(img)
    s = size / 100.0  # work in a 100x100 design space

    # rounded-square inner panel
    d.rounded_rectangle(
        [8 * s, 8 * s, 92 * s, 92 * s], radius=14 * s,
        fill=(22, 27, 34), outline=(48, 54, 61), width=max(1, int(1.5 * s)),
    )

    # numerator block (VIX)
    d.rounded_rectangle([30 * s, 22 * s, 70 * s, 40 * s], radius=4 * s, fill=ACCENT)
    # fraction bar
    d.rectangle([22 * s, 48 * s, 78 * s, 52 * s], fill=TEXT)
    # denominator blocks (spread + 2.5)
    d.rounded_rectangle([24 * s, 60 * s, 52 * s, 78 * s], radius=4 * s, fill=(63, 185, 80))
    d.rounded_rectangle([58 * s, 60 * s, 76 * s, 78 * s], radius=4 * s, fill=(210, 153, 34))

    img.save(path)
    print(f"wrote {path} ({size}x{size})")


if __name__ == "__main__":
    make_icon(180, "icons/apple-touch-icon.png")
    make_icon(192, "icons/icon-192.png")
    make_icon(512, "icons/icon-512.png")
