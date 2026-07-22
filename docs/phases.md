# Implementation Phases

**Project:** Md Adnan Umar — GitHub Profile  
**Last Updated:** 2026-07-22

---

## Phase 0 — Planning ✅

- Defined project goals, design language, and folder structure
- Chose SMIL-only animation strategy
- Documented colour palette and layout system
- Created `docs/` structure with 9 planning documents
- Wrote `.gitignore` and `requirements.txt`
- Extracted existing base64 avatar into `scripts/pic-b64.txt`

**Deliverables:** `docs/`, `.gitignore`, `requirements.txt`, `scripts/pic-b64.txt`

---

## Phase 1 — Photo Pipeline ✅

- Installed `rembg[cpu]` with onnxruntime backend
- Wrote `scripts/_process_photo.py`:
  - rembg AI background removal on `pic.jpeg`
  - PIL circle crop (top 88% of image, centered)
  - Gaussian soft edge (radius 1.2)
  - Saved `pic-circle.png` (320×320, 85 KB)
  - Generated `scripts/pic-b64.txt` (116 KB base64 data URI)
- Confirmed: Python 3.13 at `C:\Python313\python.exe`

**Deliverables:** `pic-circle.png`, `scripts/pic-b64.txt`, `scripts/_process_photo.py`

---

## Phase 2 — Hero SVG Assets ✅

- Wrote `scripts/_build_svgs.py` — master SVG assembler:
  - `defs()` — shared gradients, filters, masks, clip-paths
  - `left_panel()` — photo ring, name, info lines, skill pills, social links
  - `right_panel()` — terminal titlebar, code block, metric cards, what-I-ship section
  - `particles()` — 8 floating particles
  - `build_hero()` — composes all layers
  - `build_info_card()` — initial info card (superseded by `make_info_card.py`)
- Generated `dark.svg` (141.7 KB), `light.svg` (141.7 KB), `info-card.svg`
- Verified: photo embedded ✓, animations present ✓, SVG properly closed ✓

**Deliverables:** `dark.svg`, `light.svg`, `scripts/_build_svgs.py`

---

## Phase 3 — Info Card & Scripts ✅

- Rewrote `scripts/make_info_card.py`:
  - `Theme` dataclass for colour tokens
  - Modular builder functions for each section
  - 760×310 canvas, gradient header, traffic lights
  - Circular avatar with pulsing ring + dashed rotating ring
  - Open-to-work animated badge
  - 8 neofetch info lines with staggered reveal
  - 16 skill pills in 3 colour variants
  - Highlights list + website + palette swatches
  - Confirmed clean output: 133.2 KB
- Fixed `scripts/fetch_contributions.py`:
  - Multi-selector strategy (`td[data-date]`, `rect[data-date]`)
  - Count extraction from `data-count`, `<title>`, and text content
  - Proper User-Agent headers
- Rewrote `scripts/render_heatmap_svg.py`:
  - Correct geometry constants (CELL=11, GAP=3, WEEKS=53)
  - Fixed f-string legend bug from original
  - Proper month labels with date-based positioning
  - Diagonal stagger animation for cell reveal
  - Stats footer: total, best day, username
- Added `scripts/prep_photo.py` and `scripts/make_ascii_svg.py` for ASCII art generation

**Deliverables:** `scripts/make_info_card.py`, `info-card.svg`, `scripts/fetch_contributions.py`, `scripts/render_heatmap_svg.py`, `scripts/prep_photo.py`, `scripts/make_ascii_svg.py`

---

## Phase 4 — Contribution Heatmap ✅

- Rebuilt `contrib-heatmap.svg`:
  - 801×191 px canvas
  - 53 weeks × 7 days grid, properly aligned to Monday
  - Live data from GitHub scraper (367 days of real contributions)
  - 6-level green ramp palette
  - Month labels auto-positioned from data
  - Mon/Wed/Fri day labels
  - Shimmer + pulse border animation
  - Legend + stats footer

**Deliverables:** `contrib-heatmap.svg`

---

## Phase 5 — README ✅

- Rewrote `README.md`:
  - `<picture>` tag for automatic dark/light switching
  - 14 sections with terminal-style headings (`$ command`)
  - `about.java` code block with real stack
  - Projects table linking to real repositories
  - Full tech-stack badges across 7 categories
  - Timeline from 2022 → 2025
  - Social links, quote, visit counter, footer

**Deliverables:** `README.md`

---

## Phase 6 — Documentation ✅

- Updated all docs to reflect final implementation
- Created `implementation-log.md`, `assets.md`, `decisions.md`
- Every document accurately reflects the current project state

**Deliverables:** All files in `docs/`

---

## Phase 7 — Validate & Ship ✅

- Validated: SVG markers, README links, folder structure, `.gitignore`, `requirements.txt`
- Fixed `make_info_card.py` fallback and Windows encoding
- Synchronized all docs with actual repository contents
- Git commits created by category
- Pushed to `origin/main` (`https://github.com/Adnan-Umar/Adnan-Umar.git`)
