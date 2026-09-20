import io
import pathlib
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
import pptx_media as pm  # noqa: E402

RELS = (
    '<Relationships>'
    '<Relationship Id="rId1" Target="../slideLayouts/slideLayout1.xml"/>'
    '<Relationship Id="rId2" Target="../media/image3.png"/>'
    '<Relationship Id="rId3" Target="../media/image7.jpeg"/>'
    '<Relationship Id="rId4" Target="../media/image3.png"/>'
    '</Relationships>'
)


def fake_pptx():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("ppt/slides/_rels/slide2.xml.rels", RELS)
        z.writestr("ppt/media/image3.png", b"png-bytes")
    path = pathlib.Path(tempfile.mkdtemp()) / "deck.pptx"
    path.write_bytes(buf.getvalue())
    return path


class PptxMediaTests(unittest.TestCase):
    def test_slide_media_lists_unique_media_in_order(self):
        self.assertEqual(pm.slide_media(fake_pptx(), 2), ["image3.png", "image7.jpeg"])

    def test_extract_writes_file(self):
        out = pathlib.Path(tempfile.mkdtemp()) / "x.png"
        pm.extract(fake_pptx(), "image3.png", out)
        self.assertEqual(out.read_bytes(), b"png-bytes")


if __name__ == "__main__":
    unittest.main()
