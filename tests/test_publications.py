import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
import build_publications as bp  # noqa: E402

ORCID_FIXTURE = {
    "group": [
        {"external-ids": {"external-id": [
            {"external-id-type": "doi", "external-id-value": "10.1371/JOURNAL.PBIO.3002706"},
            {"external-id-type": "issn", "external-id-value": "1545-7885"},
        ]}},
        {"external-ids": {"external-id": [
            {"external-id-type": "doi", "external-id-value": "10.7554/eLife.33746"},
        ]}},
        {"external-ids": {"external-id": [
            {"external-id-type": "doi", "external-id-value": "10.1371/journal.pbio.3002706"},
        ]}},
    ]
}

CROSSREF_FIXTURE = {
    "title": ["Retrieval of <i>contextual</i> memory &amp; CA3 remapping."],
    "container-title": ["PLOS Biology"],
    "issued": {"date-parts": [[2024, 8]]},
    "volume": "22",
    "page": "e3002706",
    "author": [
        {"given": "Magdalena", "family": "Miranda"},
        {"given": "Azul", "family": "Silva"},
    ],
}


class HelperTests(unittest.TestCase):
    def test_dois_are_lowercased_and_unique(self):
        self.assertEqual(
            bp.dois_from_orcid_json(ORCID_FIXTURE),
            ["10.1371/journal.pbio.3002706", "10.7554/elife.33746"],
        )

    def test_is_self(self):
        self.assertTrue(bp.is_self("Magdalena", "Miranda"))
        self.assertTrue(bp.is_self("M.", "Miranda"))
        self.assertTrue(bp.is_self("M", "Miranda"))
        self.assertFalse(bp.is_self("Maria", "Miranda"))
        self.assertFalse(bp.is_self("Magdalena", "Pereyra"))

    def test_strip_tags(self):
        self.assertEqual(bp.strip_tags("A <i>b</i> &amp; c"), "A b & c")

    def test_authors_from_crossref(self):
        self.assertEqual(
            bp.authors_from_crossref(CROSSREF_FIXTURE["author"]),
            [{"name": "Magdalena Miranda", "self": True}, {"name": "Azul Silva", "self": False}],
        )

    def test_entry_type(self):
        self.assertEqual(bp.entry_type("10.3389/fnbeh.2023.1205371"), "editorial")
        self.assertEqual(bp.entry_type("10.1016/j.conb.2023.102696"), "review")
        self.assertEqual(bp.entry_type("10.1371/journal.pbio.3002706"), "article")


class BuildEntryTests(unittest.TestCase):
    def test_lead_article(self):
        e = bp.build_entry("10.1371/journal.pbio.3002706", CROSSREF_FIXTURE, True)
        self.assertEqual(e["title"], "Retrieval of contextual memory & CA3 remapping")
        self.assertEqual(e["year"], 2024)
        self.assertEqual(e["journal"], "PLOS Biology")
        self.assertTrue(e["lead"])
        self.assertFalse(e["corresponding"])
        self.assertTrue(e["oa"])
        self.assertEqual(e["type"], "article")

    def test_corresponding_flag(self):
        e = bp.build_entry("10.3389/fnbeh.2024.1478656", CROSSREF_FIXTURE, True)
        self.assertTrue(e["lead"])
        self.assertTrue(e["corresponding"])

    def test_non_lead_and_journal_fix(self):
        cr = dict(CROSSREF_FIXTURE)
        cr["container-title"] = ["The Journal of neuroscience : the official journal of the Society for Neuroscience"]
        e = bp.build_entry("10.1523/jneurosci.2578-20.2021", cr, False)
        self.assertEqual(e["journal"], "The Journal of Neuroscience")
        self.assertFalse(e["lead"])
        self.assertFalse(e["oa"])


if __name__ == "__main__":
    unittest.main()
