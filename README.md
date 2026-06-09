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

## Layout

```
zollverein/
├── index.html              # the page — 6 spatial sections + diagram + event coda
├── css/style.css           # report aesthetic: light bg, dark text, muted images
├── images/
│   ├── placeholder.svg     # shown until a real photo is dropped in (auto-fallback)
│   ├── diagram-triangle.svg# the "Triangle of Power" diagram (editable SVG, done)
│   ├── zollverein/         # site photos (filenames match index.html + captions.txt)
│   ├── figures/            # portraits: Schiller, Sohl/Beitz, Arendt
│   └── documents/          # § 8 GWB scan, 1969 press front page, wage slip
└── content/
    ├── sections.md         # essay split into 6 sections — edit here, paste into index.html
    ├── captions.txt        # filename | caption | source
    └── spatial-note.md     # the framing paragraph at the top of the page
```

## How to finish it

1. **Drop in the prose.** Edit `content/sections.md`, then replace each
   `data-placeholder` paragraph in `index.html` with the finished text.
2. **Drop in the images.** Save photos under `images/` using the exact filenames in
   `content/captions.txt`. They appear automatically; until then the placeholder shows.
3. **Fill the event card** (bottom of `index.html`): name, date, time, link.
4. **Fill the credits** in the footer and the source column of `captions.txt`.

Images use an `onerror` fallback, so missing files degrade gracefully to the placeholder —
the page is always shippable.

## Image sourcing checklist

**Site photos** — Wikimedia Commons ("Zeche Zollverein", "Zollverein Kokerei");
RAG-Stiftung / Zollverein Foundation press kit; Landesarchiv NRW (archive.nrw);
your own camera for present-day shots (no filter, straight angle, good light).

**Figures** — Bundesarchiv digitized photos (free, non-commercial, attribution):
Karl Schiller, Walter Arendt, Hans-Günther Sohl / Berthold Beitz.

**Documents** — § 8 Gesetz gegen Wettbewerbsbeschränkungen (gesetze-im-internet.de /
Bundestag archive); a 1968/69 Ruhrkohle AG front page (Spiegel / Die Zeit / WAZ archive);
a 1970s wage slip / social plan (montan.dok, Deutsches Bergbau-Museum Bochum).

Keep all captions strictly factual: date, place, photographer if known, source/license.
