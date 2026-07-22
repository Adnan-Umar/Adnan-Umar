# Implementation Log

**Project:** Md Adnan Umar — GitHub Profile  
**Format:** Chronological record of changes  
**Last Updated:** 2026-07-22

---

## 2026-07-21 — Initial Scaffolding

- Created initial repository structure
- Added `requirements.txt` with core dependencies
- Added `.gitignore`
- Created `docs/` folder with initial stub documents
- Added initial scripts: `fetch_contributions.py`, `make_ascii_svg.py`, `make_info_card.py`, `prep_photo.py`, `render_heatmap_svg.py`
- Added GitHub Actions workflows: `update-profile.yml`, `snake.yml`
- Created initial `dark.svg`, `light.svg`, `info-card.svg` (basic versions)

---

## 2026-07-22 — Full Production Redesign

### Photo Pipeline

- Installed `rembg[cpu]` (onnxruntime backend, downloaded u2net.onnx ~176 MB)
- Wrote `scripts/_process_photo.py`:
  - Uses rembg for AI background removal on `pic.jpeg`
  - PIL circular crop, Gaussian soft edge
  - Saves `pic-circle.png` (320×320, 85 KB)
  - Saves `scripts/pic-b64.txt` (116,706 char base64 data URI)
- Ran successfully; confirmed both output files present

### SVG Rebuild — Hero Banners

- Wrote `scripts/_build_svgs.py` (43.8 KB) — full SVG assembler:
  - `Theme` dataclass with dark/light colour token dictionaries
  - `defs()` — all `<defs>`: gradients, filters (noise, glow, strongGlow), masks (scanline), clipPaths (photo, panels)
  - `left_panel()` — photo ring glow, animated rotate ring, circular photo, name, role, info lines, skill pills (2 rows, 10 skills), social pills
  - `right_panel()` — terminal titlebar, traffic lights, greeting, name, role, 4 metric cards, code block (8 lines Java), 3 "what I ship" cards, footer quote
  - `particles()` — 8 floating particles across both panels
  - `build_hero()` — assembles background + panels + particles + frame
  - `build_info_card()` — initial info card version (superseded)
- Generated:
  - `dark.svg` — 141.7 KB, photo embedded ✓, animations ✓, properly closed ✓
  - `light.svg` — 141.7 KB, photo embedded ✓, animations ✓, properly closed ✓

### Info Card Rebuild

- Rewrote `scripts/make_info_card.py` completely:
  - `Theme` dataclass (colour tokens, pill fill/stroke pairs)
  - Canvas: 760×310 px
  - `_build_defs()` — accent gradient, header gradient, shimmer, blob radial, clipPath for avatar, glow filter
  - `_build_background()` — dark panel + ambient blob
  - `_build_header()` — gradient bar, accent underline, traffic lights, `user@host` title
  - `_build_avatar()` — base64 image, pulsing ring, dashed rotating ring, open-to-work badge
  - `_build_info_lines()` — 8 info rows with staggered SMIL reveals (0.35–1.9s)
  - `_build_pills()` — 16 skills, 3 colour variants, auto-wrapping pill layout
  - `_build_highlights()` — 4 highlights, website link, 8-swatch colour palette
  - `_build_border()` — pulsing border + shimmer sweep
  - `build_info_card()` — master assembler
- Ran `make_info_card.py info-card.svg` → 133.2 KB, confirmed clean
- Added fallback: extracts base64 from existing `info-card.svg` if `scripts/pic-b64.txt` is missing
- Fixed Windows encoding issue with Unicode characters in print statements

### ASCII Pipeline

- `scripts/prep_photo.py`: background removal with rembg, CLAHE contrast boost
- `scripts/make_ascii_svg.py`: animated monochrome ASCII SVG with clip reveal and gradient text

### Contribution Heatmap & Automation

- `scripts/fetch_contributions.py`:
  - Multi-selector strategy (`td[data-date]`, `rect[data-date]`)
  - Count extraction from `data-count`, `<title>`, and text
  - Proper User-Agent headers
- `scripts/render_heatmap_svg.py`:
  - 801×191 canvas with 53×7 grid aligned to Monday
  - Month/day labels, 6-level green ramp
  - Diagonal stagger animation, legend, stats footer
- `.github/workflows/update-profile.yml`: daily cron at 06:17 UTC
- `.github/workflows/snake.yml`: every 12 hours via Platane/snk

### README Rewrite

- `README.md` rewritten with 14 terminal-style sections:
  - Hero banners with `<picture>` dark/light switching
  - `$ whoami`, `$ cat about.java`, `$ neofetch`
  - Education, experience, focus, tech-stack, projects
  - Open source, GitHub stats, contribution graph, achievements
  - Timeline, connect, dev quote, footer
- No JavaScript. No external CSS. All animation is SMIL-only.

### Documentation Synchronization

- Updated `docs/architecture.md` to match actual repository contents
- Updated `docs/phases.md` to reflect actual completed phases
- Updated `docs/memory.md` asset sizes and removed stale references
- Updated `docs/assets.md` to remove references to non-existent files
- Updated `docs/decisions.md` and `docs/rules.md` to remove references to missing scripts
- Updated `docs/design.md` photo pipeline section

### README Resilience Improvements

- Removed external visit count badges:
  - Removed `komarev.com/ghpvc/` profile views badge
  - Removed `visitcount.itsvg.in` visit counter from footer
- Replaced external achievement service with static achievements table:
  - Removed `github-profile-trophy.vercel.app` external API call
  - Added static `$ cat achievements.md` section with 8 common GitHub achievements
- Added freelancing experience entry to timeline:
  - Added **2024 – Present** | Freelancing | Client projects · microservices · Spring Boot · cloud deployments

**Rationale:** External badge services like komarev.com, github-profile-trophy.vercel.app, and visitcount.itsvg.in can suffer from downtime, rate-limiting, or service discontinuation. Static markdown ensures the README always renders correctly regardless of third-party service availability.
