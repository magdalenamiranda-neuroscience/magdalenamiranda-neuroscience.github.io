import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
from contrast import ratio  # noqa: E402

# (foreground, background, minimum ratio). 4.5 = normal text, 3.0 = large text (>=24px or 19px bold).
PAIRS = [
    ("#222222", "#ffffff", 4.5),
    ("#555555", "#ffffff", 4.5),
    ("#555555", "#f7f8fb", 4.5),
    ("#005ad2", "#ffffff", 4.5),
    ("#005ad2", "#f7f8fb", 4.5),
    ("#001965", "#ffffff", 4.5),
    ("#001965", "#dfefee", 4.5),
    ("#001965", "#f8dce5", 4.5),
    ("#0f3b44", "#dfefee", 4.5),
    ("#ffffff", "#001965", 4.5),
    ("#c9d5f2", "#001965", 4.5),
    ("#8fb2f0", "#001965", 4.5),
    ("#c9d5f2", "#0d3391", 4.5),
    ("#8fb2f0", "#0d3391", 4.5),
]


class ContrastTests(unittest.TestCase):
    def test_pairs_meet_wcag_aa(self):
        for fg, bg, minimum in PAIRS:
            self.assertGreaterEqual(ratio(fg, bg), minimum, f"{fg} on {bg}")


if __name__ == "__main__":
    unittest.main()
