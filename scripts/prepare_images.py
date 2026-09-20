"""Convert an image to an optimised WebP.

  python scripts/prepare_images.py SRC DST [MAX_WIDTH]
"""
import sys

from PIL import Image


def to_webp(src, dst, max_w=1400, quality=82):
    im = Image.open(src)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=quality, method=6)
    return im.size


if __name__ == "__main__":
    size = to_webp(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1400)
    print("wrote", sys.argv[2], size)
