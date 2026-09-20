import pathlib
import unittest

import yaml

DATA = pathlib.Path(__file__).resolve().parent.parent / "_data" / "publications.yml"
LEAD = {
    "10.1016/j.cub.2025.11.006", "10.3389/fnbeh.2024.1478656", "10.1371/journal.pbio.3002706",
    "10.1016/j.bandc.2021.105831", "10.1016/j.nlm.2018.08.019", "10.1002/hipo.23269",
    "10.1523/eneuro.0293-17.2017",
}


class PublicationDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pubs = yaml.safe_load(DATA.read_text(encoding="utf-8"))

    def test_counts(self):
        self.assertEqual(len(self.pubs), 21)
        self.assertEqual(sum(p["type"] == "article" for p in self.pubs), 16)
        self.assertEqual(sum(p["type"] in ("review", "editorial") for p in self.pubs), 5)
        self.assertEqual(sum(p["lead"] for p in self.pubs), 7)

    def test_lead_flags_match_confirmed_list(self):
        self.assertEqual({p["doi"] for p in self.pubs if p["lead"]}, LEAD)

    def test_every_entry_is_complete(self):
        for p in self.pubs:
            self.assertTrue(p["title"], p["doi"])
            self.assertTrue(p["journal"], p["doi"])
            self.assertIsInstance(p["year"], int, p["doi"])
            self.assertTrue(p["authors"], p["doi"])

    def test_sorted_by_year_descending(self):
        years = [p["year"] for p in self.pubs]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_author_marked_on_every_paper(self):
        for p in self.pubs:
            self.assertTrue(any(a["self"] for a in p["authors"]), p["doi"])


if __name__ == "__main__":
    unittest.main()
