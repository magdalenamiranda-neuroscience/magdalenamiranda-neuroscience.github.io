"""Search Wikimedia Commons for CC0 / public-domain bitmaps and print candidates.

  python scripts/find_cc0.py "retina histology"
"""
import json
import re
import sys
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
OK = ("cc0", "public domain", "pd")


def search(query, limit=40):
    params = {
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"{query} filetype:bitmap", "gsrlimit": limit,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 800,
    }
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"User-Agent": "personal-site-build/1.0"})
    data = json.load(urllib.request.urlopen(req, timeout=30))
    for page in (data.get("query", {}).get("pages", {})).values():
        info = page["imageinfo"][0]
        meta = info.get("extmetadata", {})
        lic = meta.get("LicenseShortName", {}).get("value", "")
        if not lic.lower().startswith(OK):
            continue
        desc = re.sub(r"<[^>]+>", "", meta.get("ImageDescription", {}).get("value", ""))[:110]
        print(f"[{lic}] {page['title']}  {info['width']}x{info['height']}\n   {info['descriptionurl']}\n   thumb: {info.get('thumburl')}\n   {desc}\n")


if __name__ == "__main__":
    search(" ".join(sys.argv[1:]))
