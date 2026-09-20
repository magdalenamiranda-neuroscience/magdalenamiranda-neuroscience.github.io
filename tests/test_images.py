import pathlib
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
import prepare_images as pi  # noqa: E402


class ToWebpTests(unittest.TestCase):
    def test_downsizes_and_writes_webp(self):
        d = pathlib.Path(tempfile.mkdtemp())
        Image.new("RGB", (3000, 2000), "#001965").save(d / "big.png")
        size = pi.to_webp(d / "big.png", d / "big.webp", max_w=1400)
        self.assertEqual(size, (1400, 933))
        self.assertEqual(Image.open(d / "big.webp").format, "WEBP")

    def test_keeps_small_images(self):
        d = pathlib.Path(tempfile.mkdtemp())
        Image.new("RGBA", (400, 300), (0, 25, 101, 255)).save(d / "s.png")
        self.assertEqual(pi.to_webp(d / "s.png", d / "s.webp"), (400, 300))


if __name__ == "__main__":
    unittest.main()
