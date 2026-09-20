"""Build _data/publications.yml from ORCID + Crossref + OpenAlex.

Run from the repo root:  python scripts/build_publications.py
"""
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ORCID = "0000-0002-6789-274X"
OUT = Path(__file__).resolve().parent.parent / "_data" / "publications.yml"

# First / co-first author, confirmed by the author and checked against Crossref author order.
LEAD_DOIS = {
    "10.1016/j.cub.2025.11.006",        # Current Biology 2025
    "10.3389/fnbeh.2024.1478656",       # Front Behav Neurosci 2024 (enrichment, middle-aged rats)
    "10.1371/journal.pbio.3002706",     # PLOS Biology 2024
    "10.1016/j.bandc.2021.105831",      # Brain and Cognition (fMRI, double motor cortex)
    "10.1016/j.nlm.2018.08.019",        # Neurobiol Learn Mem 2018
    "10.1002/hipo.23269",               # Hippocampus 2020
    "10.1523/eneuro.0293-17.2017",      # eNeuro 2017
}
CORRESPONDING_DOIS = {"10.3389/fnbeh.2024.1478656"}
REVIEW_DOIS = {
    "10.1016/j.conb.2023.102696",
    "10.3389/fncir.2020.00026",
    "10.3389/fncel.2019.00363",
    "10.1016/j.neuroscience.2017.06.002",
}
EDITORIAL_DOIS = {"10.3389/fnbeh.2023.1205371"}
JOURNAL_FIXES = {
    "The Journal of neuroscience : the official journal of the Society for Neuroscience": "The Journal of Neuroscience",
    "eneuro": "eNeuro",
}


def strip_tags(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text or "")).strip()


def is_self(given, family):
    g = given.strip().lower()
    return family.strip().lower() == "miranda" and (g.startswith("magdalena") or re.fullmatch(r"m\.?", g) is not None)


def authors_from_crossref(raw):
    out = []
    for a in raw or []:
        given, family = a.get("given", ""), a.get("family", "") or a.get("name", "")
        out.append({"name": (given + " " + family).strip(), "self": is_self(given, family)})
    return out


def dois_from_orcid_json(data):
    seen, out = set(), []
    for group in data.get("group", []):
        for ext in group.get("external-ids", {}).get("external-id", []):
            if ext.get("external-id-type") == "doi":
                doi = ext["external-id-value"].strip().lower()
                if doi not in seen:
                    seen.add(doi)
                    out.append(doi)
    return out


def entry_type(doi):
    if doi in EDITORIAL_DOIS:
        return "editorial"
    if doi in REVIEW_DOIS:
        return "review"
    return "article"


def build_entry(doi, cr, is_oa):
    doi = doi.lower()
    parts = (cr.get("issued", {}).get("date-parts") or [[None]])[0]
    journal = strip_tags((cr.get("container-title") or [""])[0])
    return {
        "doi": doi,
        "title": strip_tags((cr.get("title") or [""])[0]).rstrip("."),
        "authors": authors_from_crossref(cr.get("author")),
        "journal": JOURNAL_FIXES.get(journal, journal),
        "year": parts[0],
        "volume": cr.get("volume", ""),
        "pages": cr.get("page", ""),
        "type": entry_type(doi),
        "lead": doi in LEAD_DOIS,
        "corresponding": doi in CORRESPONDING_DOIS,
        "oa": bool(is_oa),
    }


def fetch_json(url, headers=None):
    h = {"User-Agent": "personal-site-build/1.0"}
    h.update(headers or {})
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
        return json.load(r)


def main():
    orcid = fetch_json(f"https://pub.orcid.org/v3.0/{ORCID}/works", {"Accept": "application/json"})
    entries = []
    for doi in dois_from_orcid_json(orcid):
        quoted = urllib.parse.quote(doi)
        cr = fetch_json(f"https://api.crossref.org/works/{quoted}")["message"]
        oa = fetch_json(f"https://api.openalex.org/works/doi:{quoted}").get("open_access", {}).get("is_oa", False)
        entries.append(build_entry(doi, cr, oa))
    entries.sort(key=lambda e: (-(e["year"] or 0), e["title"]))
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(
        yaml.safe_dump(entries, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8",
    )
    print(f"wrote {len(entries)} entries to {OUT}")


if __name__ == "__main__":
    main()
