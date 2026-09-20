"""List and extract the images used by a slide of a .pptx.

  python scripts/pptx_media.py list DECK N            # media files of slide N
  python scripts/pptx_media.py get DECK NAME DEST     # extract ppt/media/NAME to DEST
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path


def slide_media(pptx, n):
    with zipfile.ZipFile(pptx) as z:
        rels = z.read(f"ppt/slides/_rels/slide{n}.xml.rels").decode("utf-8")
    seen = []
    for name in re.findall(r'Target="\.\./media/([^"]+)"', rels):
        if name not in seen:
            seen.append(name)
    return seen


def extract(pptx, name, dest):
    with zipfile.ZipFile(pptx) as z, z.open(f"ppt/media/{name}") as src, open(dest, "wb") as out:
        shutil.copyfileobj(src, out)


if __name__ == "__main__":
    cmd, deck = sys.argv[1], sys.argv[2]
    if cmd == "list":
        for m in slide_media(deck, int(sys.argv[3])):
            print(m)
    elif cmd == "get":
        extract(deck, sys.argv[3], Path(sys.argv[4]))
        print("wrote", sys.argv[4])
