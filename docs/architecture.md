# Architecture

**Project:** Md Adnan Umar — GitHub Profile  
**Last Updated:** 2026-07-22

---

## 1. Repository Layout

```
Adnan-Umar/                        ← GitHub special profile repo (username/username)
│
├── README.md                      ← Profile page rendered by GitHub
│
├── dark.svg                       ← Hero banner, dark theme  (1180×610, SMIL)
├── light.svg                      ← Hero banner, light theme (1180×610, SMIL)
├── info-card.svg                  ← Neofetch terminal card   ( 760×310, SMIL)
├── contrib-heatmap.svg            ← Contribution heatmap     ( 801×191, SMIL)
│
├── requirements.txt               ← Python dependencies
├── .gitignore
│
├── scripts/
│   ├── prep_photo.py              ← Background removal + contrast boost (uses rembg)
│   ├── make_ascii_svg.py          ← Generates animated ASCII SVG from photo
│   ├── make_info_card.py          ← Generates info-card.svg from profile data
│   ├── fetch_contributions.py     ← Scrapes GitHub contribution graph → JSON
│   ├── render_heatmap_svg.py      ← Renders contrib-heatmap.svg from JSON
│   ├── README.md                  ← Scripts usage documentation
│   └── pic-b64.txt                ← Base64 data URI of avatar photo (embedded in SVGs)
│
├── data/
│   └── contributions.json        ← Scraped GitHub contribution data (refreshed daily)
│
├── docs/                         ← Project documentation (this directory)
│   ├── project-requirements.md
│   ├── architecture.md
│   ├── design.md
│   ├── rules.md
│   ├── phases.md
│   └── memory.md
│
└── .github/
    └── workflows/
        ├── update-profile.yml    ← Daily: refresh contributions + rebuild heatmap
        └── snake.yml             ← Every 12h: generate snake animation
```

---

## 2. Data Flow

```
Photo source
    │
    ▼ scripts/prep_photo.py  (rembg bg removal + contrast boost)
    │
    └─► source-prepped.png   (grayscale, high-contrast)
         │
         ▼ scripts/make_ascii_svg.py
         │
         └─► ascii-art.svg   (animated monochrome ASCII, standalone)


scripts/pic-b64.txt (avatar base64)
    │
    ├─► embedded in dark.svg / light.svg  (circular photo with animated ring)
    └─► embedded in info-card.svg          (neofetch-style avatar)


GitHub Contributions Graph (HTML scrape)
    │
    ▼ scripts/fetch_contributions.py
    │
    └─► data/contributions.json
         │
         ▼ scripts/render_heatmap_svg.py
         │
         └─► contrib-heatmap.svg
```

---

## 3. GitHub Actions Pipeline

### `update-profile.yml` (daily, 06:17 UTC)

```
trigger: schedule (cron) + workflow_dispatch + push(main)
│
├─ checkout repo
├─ setup Python 3.11
├─ pip install requirements.txt
├─ python scripts/fetch_contributions.py Adnan-Umar
├─ python scripts/render_heatmap_svg.py
└─ git add + commit "[skip ci] chore: refresh contribution graph [skip ci]" + push
```

### `snake.yml` (every 12 hours)

```
trigger: schedule + workflow_dispatch
│
└─ Platane/snk@v3 generates snake animation SVG/GIF → output branch
```

---

## 4. SVG Rendering Architecture

GitHub serves SVGs through its Camo CDN proxy which:
- Strips `<script>` tags
- Strips `<style>` tags and inline `style=` attributes
- Blocks external URL references (`href`, `src` with `http://`)
- Passes through: `<animate>`, `<animateTransform>`, `<defs>`, `filter`, `mask`, `clipPath`

**Strategy used:**
- All animation via SMIL (`animate`, `animateTransform`)
- All colours via SVG presentation attributes (`fill`, `stroke`, `stop-color`)
- Photo embedded as `data:image/png;base64,…` — no external fetch
- Filters (`feGaussianBlur`, `feTurbulence`, `feBlend`) used for glow + noise
- Masks used for scanline sweep effect

---

## 5. Component Responsibilities

| Component | Responsibility |
|:---|:---|
| `dark.svg` / `light.svg` | Visual identity — first thing a visitor sees |
| `info-card.svg` | Secondary card — profile detail, skill signal |
| `contrib-heatmap.svg` | Activity signal — shows consistency of work |
| `make_info_card.py` | Regenerate info-card with updated profile data |
| `fetch_contributions.py` | Data collection — reads public GitHub HTML, no token required |
| `render_heatmap_svg.py` | Data visualisation — pure SVG output |

---

## 6. README Structure

The README is intentionally split into 14 terminal-style sections:

1. **Hero Banners** — `<picture>` switches between `dark.svg` and `light.svg` based on GitHub theme
2. **Profile Meta** — badges for views, LinkedIn, Portfolio, Email
3. **$ whoami** — brief professional summary
4. **$ cat about.java** — Java class representing the engineer
5. **$ neofetch** — `info-card.svg` embedded
6. **$ cat education.md** — degree and coursework table
7. **$ cat experience.md** — timeline of roles and milestones
8. **$ cat focus.md** — current build areas
9. **$ cat tech-stack.md** — language/framework/tool badges
10. **$ ls projects/** — featured repositories table
11. **$ cat open-source.md** — contribution philosophy
12. **$ cat github-stats.md** — profile cards, streak, language breakdown
13. **$ cat contribution-graph.md** — live `contrib-heatmap.svg`
14. **$ cat achievements.md** — trophy badges
15. **$ cat timeline.md** — year-by-year milestones
16. **$ cat connect.md** — social links
17. **$ cat quote.txt** — rotating dev quote
18. **Footer** — build attribution, visit counter, support links

No JavaScript. No external CSS. All animation is SMIL-only inside self-contained SVGs.
