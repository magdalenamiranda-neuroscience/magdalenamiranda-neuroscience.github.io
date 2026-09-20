import pathlib
import re
import unittest
from html.parser import HTMLParser

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"

# path (relative to _site) -> text that must appear on that page. Later tasks add rows.
PAGES = {
    "index.html": "Memory, and how the brain keeps similar things apart.",
    "about/index.html": "appointment pending national budget approval",
    "research/index.html": "From single molecules to whole-brain dynamics.",
    "publications/index.html": "Modulation of relative aversive and safety learning",
    "outreach/index.html": "Science Speaks: Tools for Public Outreach",
    "news/index.html": "Student Knowledge Network",
    "404.html": "Page not found",
}


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.imgs, self.links, self.resources = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "img":
            self.imgs.append(a)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("link", "script", "img", "iframe", "source", "video"):
            url = a.get("href") if tag == "link" else a.get("src")
            if url:
                self.resources.append((tag, url))


def all_pages():
    return sorted(SITE.rglob("*.html"))


def parse(path):
    c = Collector()
    c.feed(path.read_text(encoding="utf-8"))
    return c


class SiteTests(unittest.TestCase):
    def test_site_is_built(self):
        self.assertTrue(SITE.exists(), "run: bundle exec jekyll build")

    def test_expected_pages(self):
        for rel, text in PAGES.items():
            f = SITE / rel
            self.assertTrue(f.exists(), f"missing page {rel}")
            self.assertIn(text, f.read_text(encoding="utf-8"), rel)

    def test_pages_have_title_and_lang(self):
        for p in all_pages():
            html = p.read_text(encoding="utf-8")
            self.assertRegex(html, r"<html[^>]*\blang=\"en\"", p.name)
            self.assertRegex(html, r"<title>[^<]+</title>", p.name)

    def test_images_have_alt(self):
        for p in all_pages():
            for img in parse(p).imgs:
                self.assertIn("alt", img, f"{p.name}: {img.get('src')}")

    def test_no_third_party_resources(self):
        for p in all_pages():
            for tag, url in parse(p).resources:
                self.assertFalse(
                    url.startswith(("http://", "https://", "//")),
                    f"{p.name}: <{tag}> loads {url}",
                )

    def test_internal_links_resolve(self):
        for p in all_pages():
            for href in parse(p).links:
                if href.startswith(("http", "mailto:", "#", "tel:")):
                    continue
                path = href.split("#")[0].split("?")[0]
                if not path:
                    continue
                target = SITE / path.lstrip("/")
                ok = (target.exists() and target.is_file()) or (target / "index.html").exists()
                self.assertTrue(ok, f"{p.name}: broken link {href}")

    def test_no_phone_or_plain_email(self):
        for p in all_pages():
            text = p.read_text(encoding="utf-8")
            self.assertNotIn("+33", text, p.name)
            self.assertNotRegex(text, r"[\w.]+@gmail\.com", p.name)

    def test_nav_has_five_items_in_order(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        found = re.findall(r'<nav class="nav__links"[^>]*><ul>(.*?)</ul>', html, re.S)[0]
        labels = re.findall(r">([A-Za-z]+)</a>", found)
        self.assertEqual(labels, ["About", "Research", "Publications", "Outreach", "News"])

    def test_publications_page_lists_every_publication(self):
        pubs = yaml.safe_load((ROOT / "_data" / "publications.yml").read_text(encoding="utf-8"))
        html = (SITE / "publications" / "index.html").read_text(encoding="utf-8")
        self.assertEqual(html.count('class="pub"'), len(pubs))
        self.assertEqual(html.count("badge--lead"), sum(p["lead"] for p in pubs))
        for p in pubs:
            self.assertIn(f"https://doi.org/{p['doi']}", html)

    def test_home_shows_computed_facts_and_status(self):
        pubs = yaml.safe_load((ROOT / "_data" / "publications.yml").read_text(encoding="utf-8"))
        html = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn(f"<strong>{len(pubs)}</strong>", html)
        self.assertIn(f"{sum(p['lead'] for p in pubs)} as first or co-first author", html)
        self.assertIn("Incoming Assistant Researcher", html)
        self.assertNotIn("IGF", html)

    def test_home_shows_three_theme_cards_and_research_shows_five(self):
        home = (SITE / "index.html").read_text(encoding="utf-8")
        research = (SITE / "research" / "index.html").read_text(encoding="utf-8")
        self.assertEqual(home.count('<article class="card">'), 3)
        self.assertEqual(research.count('<section class="theme"'), 5)

    def test_paper_figures_have_captions_on_research_page(self):
        research = (SITE / "research" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Miranda et al., 2024, PLOS Biology. CC BY 4.0.", research)
        self.assertIn("Miranda et al., 2025, Current Biology. CC BY-NC-ND 4.0", research)
        self.assertIn("Preliminary, unpublished data.", research)

    def test_paper_figures_have_captions_on_home_cards(self):
        home = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("Miranda et al., 2024, PLOS Biology. CC BY 4.0.", home)
        self.assertIn("Preliminary, unpublished data.", home)

    def test_about_facts(self):
        html = (SITE / "about" / "index.html").read_text(encoding="utf-8")
        for text in (
            "Institute of Functional Genomics",
            "2021–2025",
            "Universidad Favaloro",
            "Instituto Superior de Formación Docente y Técnica Nº 77",
            "Licenciatura",
            "Human Frontier Science Program",
            "Fyssen Foundation",
            "French (B2)",
        ):
            self.assertIn(text, html)
        self.assertNotIn("2021–Present", html)

    def test_outreach_video_is_click_to_load_and_privacy_friendly(self):
        html = (SITE / "outreach" / "index.html").read_text(encoding="utf-8")
        self.assertIn('data-embed="https://www.youtube-nocookie.com/embed/ZvORHezcs_s', html)
        self.assertNotIn("<iframe", html)  # YouTube only loads after a click
        self.assertIn("https://www.youtube.com/watch?v=ZvORHezcs_s", html)  # plain fallback link
        for text in ("eLife", "Juan Facundo Morici", "Azul Silva", "Brain Awareness Week", "Educando al Cerebro", "Student Knowledge Network"):
            self.assertIn(text, html)
        for logo in ("elife-logo", "embo", "logo.png"):
            self.assertNotIn(logo, html.lower())

    def test_first_news_post_and_home_teaser(self):
        post = SITE / "news" / "2026" / "09" / "19" / "student-knowledge-network" / "index.html"
        self.assertTrue(post.exists())
        html = post.read_text(encoding="utf-8")
        self.assertIn("call for short talks", html)
        self.assertIn("Arduino programming", html)
        home = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("Student Knowledge Network", home)
        self.assertIn("Latest news", home)

    def test_no_email_address_anywhere_in_the_repository(self):
        skip_dirs = {".git", "_site", "incoming", "tests", "vendor", ".bundle", ".jekyll-cache", "__pycache__"}
        binary = {".webp", ".woff2", ".png", ".jpg", ".jpeg", ".pyc"}
        needles = ("gmail", "miranda." + "magdalena")
        for f in ROOT.rglob("*"):
            if not f.is_file() or binary & {f.suffix.lower()} or skip_dirs & set(f.relative_to(ROOT).parts):
                continue
            text = f.read_text(encoding="utf-8", errors="ignore").lower()
            for n in needles:
                self.assertNotIn(n, text, f"{f.relative_to(ROOT)} contains '{n}'")
        self.assertNotIn("data-email", (SITE / "index.html").read_text(encoding="utf-8"))

    def test_google_scholar_link_is_shown(self):
        scholar = "https://scholar.google.com/citations?user=CNZ1axcAAAAJ"
        for rel in ("index.html", "publications/index.html"):
            html = (SITE / rel).read_text(encoding="utf-8")
            self.assertIn(scholar, html, rel)
            self.assertIn("Google Scholar", html, rel)

    def test_no_cv_page_or_download(self):
        self.assertFalse((SITE / "cv").exists())
        self.assertEqual(list(SITE.rglob("*.pdf")), [])


if __name__ == "__main__":
    unittest.main()
