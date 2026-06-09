#!/usr/bin/env python3
"""Fetch CC-licensed photos from Wikimedia Commons for the Zollverein site.

For each target we search Commons, take the best photo match, download it at
~960px, and record real author + license so we can attribute correctly
(CC-BY / BY-SA require it). Writes images and a credits.json manifest.
"""
import json, os, subprocess, time, urllib.parse

UA = "ZollvereinSiteBot/1.0 (educational research; contact via repo)"
API = "https://commons.wikimedia.org/w/api.php"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Python's SSL stack doesn't trust the local proxy CA; curl does. Route through curl.
def curl(url, out=None):
    cmd = ["curl", "-sS", "--max-time", "60", "-L", "-A", UA]
    if out:
        cmd += ["-o", out, url]
        subprocess.run(cmd, check=True)
        return None
    return subprocess.run(cmd + [url], check=True, capture_output=True).stdout

# target filename (relative to repo) -> list of search queries (tried in order)
TARGETS = {
    "images/zollverein/aerial-complex.jpg":        ["Zeche Zollverein Luftaufnahme"],
    "images/zollverein/shaft12-winding-tower.jpg": ["Zeche Zollverein Schacht XII Doppelbock Fördergerüst"],
    "images/zollverein/coking-plant-ovens.jpg":    ["Kokerei Zollverein Koksofenbatterie", "Kokerei Zollverein Ofen"],
    "images/zollverein/coal-washery.jpg":          ["Zeche Zollverein Kohlenwäsche", "Ruhr Museum Zollverein Gebäude"],
    "images/zollverein/wage-hall.jpg":             ["Zeche Zollverein Lohnhalle", "Zeche Zollverein Waschkaue Halle"],
    "images/zollverein/compressor-house.jpg":      ["Zeche Zollverein Maschinenhalle", "Kompressorenhalle Zollverein"],
    "images/zollverein/ring-railway.jpg":          ["Zeche Zollverein Gleise", "Zollverein Bahngleise Schienen"],
    "images/figures/schiller.jpg":                 ["Karl Schiller Bundesarchiv"],
    "images/figures/arendt.jpg":                   ["Walter Arendt Bundesarchiv", "Walter Arendt Politiker"],
    "images/figures/sohl-or-beitz.jpg":            ["Berthold Beitz Bundesarchiv", "Berthold Beitz Krupp"],
}

def api(params):
    params = {**params, "format": "json"}
    url = API + "?" + urllib.parse.urlencode(params)
    # The API intermittently returns empty bodies under rapid requests; retry.
    for attempt in range(4):
        body = curl(url)
        if body.strip():
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                pass
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("empty/invalid API response after retries")

def search(query, width):
    d = api({
        "action": "query", "generator": "search",
        "gsrsearch": query, "gsrnamespace": 6, "gsrlimit": 8,
        "prop": "imageinfo", "iiprop": "url|extmetadata|mime|size",
        "iiurlwidth": width,
    })
    pages = d.get("query", {}).get("pages", {})
    # sort by search index to respect relevance order
    return sorted(pages.values(), key=lambda p: p.get("index", 999))

def candidates(pages):
    out = []
    for p in pages:
        ii = p.get("imageinfo", [{}])[0]
        mime = ii.get("mime", "")
        if mime in ("image/jpeg", "image/png") and ii.get("thumburl") and ii.get("width", 0) >= 600:
            out.append((p, ii))
    return out

def meta(ii, title):
    em = ii.get("extmetadata", {})
    def g(k): return em.get(k, {}).get("value", "")
    import re
    author = re.sub("<[^>]+>", "", g("Artist")).strip() or "Unknown"
    return {
        "title": title,
        "author": author[:120],
        "license": g("LicenseShortName") or g("License"),
        "credit": re.sub("<[^>]+>", "", g("Credit")).strip()[:160],
        "descurl": ii.get("descriptionurl", ""),
        "source_url": ii.get("thumburl", ""),
    }

def download(url, dest):
    curl(url, out=dest)
    return os.path.getsize(dest)

def is_real_image(path):
    """Reject Wikimedia HTML error pages saved with a .jpg name."""
    try:
        with open(path, "rb") as f:
            head = f.read(4)
        return head[:3] == b"\xff\xd8\xff" or head[:4] == b"\x89PNG"
    except OSError:
        return False

def fetch_one(rel, queries, dest):
    """Try each query, each candidate, each width until a real JPEG lands."""
    for query in queries:
        for width in (960, 800, 640):
            try:
                cands = candidates(search(query, width))
            except Exception as e:
                print(f"      search error '{query}' @{width}: {e}")
                continue
            for p, ii in cands:
                try:
                    download(ii["thumburl"], dest)
                except Exception:
                    continue
                if is_real_image(dest):
                    return p, ii, query
    return None, None, None

def main():
    # Preserve credits from prior successful runs (so we don't re-fetch good images).
    cpath = os.path.join(ROOT, "tools", "credits.json")
    credits = json.load(open(cpath)) if os.path.exists(cpath) else {}
    for rel, queries in TARGETS.items():
        dest = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if rel in credits and is_real_image(dest):
            print(f"SKIP  {rel}  (already have {credits[rel]['title']})")
            continue
        p, ii, used = fetch_one(rel, queries, dest)
        time.sleep(0.8)
        if not ii:
            if os.path.exists(dest):
                os.remove(dest)
            print(f"MISS  {rel}  (no usable image for {queries})")
            continue
        m = meta(ii, p["title"])
        credits[rel] = m
        n = os.path.getsize(dest)
        print(f"OK    {rel}  {n//1024}KB  <- {m['title']}  [{m['license']}] {m['author']}")
    with open(os.path.join(ROOT, "tools", "credits.json"), "w") as f:
        json.dump(credits, f, indent=2, ensure_ascii=False)
    print(f"\nWrote credits for {len(credits)} images -> tools/credits.json")

if __name__ == "__main__":
    main()
