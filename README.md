# The Zollverein Cartel — a report-form companion site

A one-page static site that walks the argument of *The Zollverein Cartel* through the
real, named structures of the Zeche Zollverein in Essen. The architecture is used as a
factual frame — locations as section dividers, not metaphors.

## Serving

The site is built to be served under the `/zollverein/` URL path (e.g. GitHub Pages
project site at `https://<user>.github.io/zollverein/`). `index.html` sets
`<base href="/zollverein/">`, so every asset path is written relative to `zollverein/`
(e.g. `images/...`, `css/style.css`). If you ever serve it from a different base, change
that one `<base>` tag.

Local preview from the repo root:

```sh
python3 -m http.server 8000
# then open http://localhost:8000/   (base tag still resolves assets correctly)
```

The page is **mobile-first**: single column by default, fluid type, lazy-loaded images,
a sticky waypoint bar that tracks the section in view, and a tap-to-jump route menu.
Tablet/desktop layouts (floated figures, wider measure) are layered on as progressive
enhancements at `min-width` breakpoints.

## Status — what's done

- **Text:** all six sections + coda are written inline in `index.html` (grounded-history
  draft; the source is in `content/sections.md`, marked `[DRAFT]` for revision).
- **Images:** all 12 are real, CC-licensed photos pulled from Wikimedia Commons /
  Bundesarchiv and content-verified. Attribution is in the footer and `content/captions.txt`.
- **Diagram:** the "Triangle of Power" SVG is done and matches the grounded text.

Only the **event card** (name / date / time / link, bottom of `index.html`) is left to fill.

## Layout

```
zollverein/
├── index.html              # the page — 6 spatial sections + diagram + event coda
├── css/style.css           # mobile-first report aesthetic; desktop = progressive enhancement
├── js/route.js             # sticky waypoint bar + tap-to-jump route menu
├── images/
│   ├── placeholder.svg     # auto-fallback if any photo is ever missing (onerror)
│   ├── diagram-triangle.svg# the "Triangle of Power" diagram
│   ├── zollverein/         # site photos (filenames match index.html + captions.txt)
│   └── figures/            # portraits: Schiller, Arendt, Beitz
├── content/
│   ├── sections.md         # the prose draft, split by section
│   ├── captions.txt        # filename | caption | source (license)
│   └── spatial-note.md     # the framing paragraph at the top of the page
└── tools/
    ├── fetch_images.py     # re-pull images from Wikimedia Commons (uses curl)
    └── credits.json        # machine-readable attribution manifest
```

## Re-fetching or swapping images

`tools/fetch_images.py` queries the Wikimedia Commons API per target, downloads the best
match at ~960px, validates it's a real JPEG/PNG, and records author + license in
`tools/credits.json`. It skips targets that already have a good file, so re-running only
fills gaps. To swap a specific image, just drop a new file in with the same name and update
its caption/credit in `index.html` + `content/captions.txt`.

## Image sourcing notes

Photos came from **Wikimedia Commons** ("Zeche Zollverein", "Kokerei Zollverein", etc.) and
the **Bundesarchiv** collection on Commons (the Schiller/Arendt portraits). All are CC BY /
BY-SA — attribution is required and is present in the footer and `captions.txt`.

Optional additions not yet sourced: a scan of § 8 *Gesetz gegen Wettbewerbsbeschränkungen*
(gesetze-im-internet.de / Bundestag archive), a 1968/69 Ruhrkohle AG press front page
(Spiegel / Die Zeit / WAZ archive), a 1970s wage slip (montan.dok, Deutsches
Bergbau-Museum Bochum). Drop any of these into `images/documents/` and add a section if wanted.
