import pathlib
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
THEME_IDS = ["memory-discrimination", "cognitive-ageing", "eeg-ml", "aversive-learning", "retinal-ischemia"]
NEEDS_CREDIT = {"memory-discrimination", "eeg-ml", "aversive-learning"}


class FigureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.figs = yaml.safe_load((ROOT / "_data" / "figures.yml").read_text(encoding="utf-8"))

    def test_every_theme_has_a_figure_file(self):
        for tid in THEME_IDS:
            fig = self.figs[tid]
            self.assertTrue((ROOT / fig["src"].lstrip("/")).is_file(), tid)

    def test_alt_text_is_real(self):
        for tid in THEME_IDS:
            alt = self.figs[tid]["alt"]
            self.assertGreater(len(alt), 15, tid)
            self.assertNotIn("<", alt, tid)
            self.assertNotIn("PENDIENTE", alt, tid)

    def test_paper_figures_are_credited(self):
        for tid in NEEDS_CREDIT:
            self.assertTrue(self.figs[tid].get("credit"), tid)

    def test_cc0_images_are_not_credited(self):
        for tid in set(THEME_IDS) - NEEDS_CREDIT:
            self.assertNotIn("credit", self.figs[tid], tid)

    def test_sources_file_has_no_placeholders(self):
        text = (ROOT / "assets" / "img" / "SOURCES.md").read_text(encoding="utf-8")
        self.assertNotIn("[", text)


class ResearchDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.themes = yaml.safe_load((ROOT / "_data" / "research.yml").read_text(encoding="utf-8"))
        pubs = yaml.safe_load((ROOT / "_data" / "publications.yml").read_text(encoding="utf-8"))
        cls.dois = {p["doi"] for p in pubs}

    def test_five_themes_in_order(self):
        self.assertEqual([t["id"] for t in self.themes], THEME_IDS)
        self.assertEqual([t["number"] for t in self.themes], ["01", "02", "03", "04", "05"])

    def test_fields_present(self):
        for t in self.themes:
            for key in ("species", "title", "summary", "text"):
                self.assertTrue(t[key].strip(), f"{t['id']}.{key}")
            self.assertTrue(t["tags"])
            self.assertTrue(t["papers"])

    def test_papers_exist_in_publications(self):
        for t in self.themes:
            for d in t["papers"]:
                self.assertIn(d, self.dois, f"{t['id']}: {d}")


if __name__ == "__main__":
    unittest.main()
