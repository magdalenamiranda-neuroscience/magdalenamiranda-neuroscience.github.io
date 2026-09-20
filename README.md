# magdalenamiranda-neuroscience.github.io

Personal academic site of Magdalena Miranda, built with Jekyll and published with GitHub Pages.

## Preview locally
    bundle exec jekyll serve      # then open http://localhost:4000

## Add a news item
Create `_posts/YYYY-MM-DD-short-title.md`:

    ---
    title: "Headline"
    date: YYYY-MM-DD
    ---
    Two to four lines of text.

## Update publications
    python scripts/build_publications.py
Re-reads ORCID, Crossref and OpenAlex and rewrites `_data/publications.yml`. If a new first-author paper appears, add its DOI to `LEAD_DOIS` in the script (and `REVIEW_DOIS` if it is a review) before running.

## Show a Google Scholar link
Uncomment `scholar:` in `_data/links.yml` and paste the profile URL.

## Change research themes or figures
Text: `_data/research.yml`. Images, alt text and credits: `_data/figures.yml`. Image origins and licences: `assets/img/SOURCES.md`. Figures from papers must keep a caption with the citation.

## Tests
    bundle exec jekyll build
    python -m unittest discover -s tests -v
