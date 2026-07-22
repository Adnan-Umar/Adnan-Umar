# Project Rules

**Project:** Md Adnan Umar — GitHub Profile  
**Last Updated:** 2026-07-22

---

## 1. SVG Rules

### Must

- All SVG files must be pure SVG — no embedded HTML, no JavaScript, no `<style>` blocks
- All animations must use SMIL: `<animate>`, `<animateTransform>`, `<animateMotion>`
- Colours must be set via SVG presentation attributes (`fill`, `stroke`, `stop-color`)
- External images must be embedded as `data:image/png;base64,…` data URIs
- Filters must use only SVG filter primitives (`feGaussianBlur`, `feTurbulence`, `feBlend`, etc.)
- All `<clipPath>` and `<mask>` elements must be defined inside `<defs>`
- Every SVG must have a closing `</svg>` tag

### Must Not

- No `<script>` tags — GitHub's renderer strips them silently
- No `<style>` tags — GitHub's renderer strips them silently
- No `style="…"` inline attributes — stripped by Camo proxy
- No `href="https://…"` inside `<image>` — Camo blocks external image URLs
- No `xlink:href` — deprecated; use `href` instead
- No `<foreignObject>` — stripped by GitHub
- No `class` attributes for styling — no CSS to select them

### Dimensions

| Asset | Width | Height | Rationale |
|:---|:---:|:---:|:---|
| `dark.svg` | 1180 | 610 | Fills GitHub profile column at 2× retina |
| `light.svg` | 1180 | 610 | Matches `dark.svg` for seamless switching |
| `info-card.svg` | 760 | 310 | Secondary card, readable at full column width |
| `contrib-heatmap.svg` | 801 | 191 | 53 weeks × 14px cell + labels + padding |

---

## 2. Python Rules

- All scripts run from the **repo root** as the working directory
- Scripts must handle missing files gracefully (check before open, exit with message)
- No hard-coded absolute paths — use `pathlib.Path` relative to cwd
- No placeholder/stub functions — every function must be complete
- Type hints on all function signatures
- Docstring on every module and public function
- Python 3.10+ features are acceptable (match, `|` union types)

### Naming conventions

| Pattern | Convention |
|:---|:---|
| Build scripts (generate assets) | `_` prefix, e.g. `_build_svgs.py` |
| One-time processing | `_process_noun.py`, e.g. `_process_photo.py` |
| Data scripts (fetch/process data) | `verb_noun.py`, e.g. `fetch_contributions.py` |
| Make scripts (regenerate single asset) | `make_asset.py`, e.g. `make_info_card.py` |

---

## 3. Commit Rules

| Type | Scope | Example |
|:---|:---|:---|
| `feat` | new feature or asset | `feat: add rotating photo ring to hero SVG` |
| `fix` | bug fix | `fix: correct legend text in heatmap SVG` |
| `docs` | documentation only | `docs: update architecture with SVG data flow` |
| `chore` | automation, deps, config | `chore: refresh contribution data [skip ci]` |
| `refactor` | code improvement, no feature change | `refactor: extract pill builder into _pill()` |

- Never commit `pic-b64.txt` changes alone — bundle with the SVG rebuild
- Add `[skip ci]` to automated commits to prevent workflow loops

---

## 4. Design Rules

- Maximum 3 accent colours per SVG (prevents visual noise)
- Every animation must have a motion purpose — no purely decorative motion
- Reveal animations always cascade top-to-bottom or left-to-right
- Particle effects must be subtle: opacity ≤ 0.55, radius ≤ 2.5 px
- Border shimmer duration: 2.8–3.5s (faster feels cheap, slower feels broken)
- Glow filter `stdDeviation` ≤ 6 (higher causes visible halos at low contrast)

---

## 5. Documentation Rules

- Every doc must have a header with project name, last-updated date
- `memory.md` is append-only — never delete entries
- `implementation-log.md` gets an entry for every significant change
- `decisions.md` explains the *why* behind non-obvious choices
- All docs must accurately reflect the current state of the project

## 6. README / External Service Rules

- Minimise external HTTP dependencies in `README.md`
- Prefer static markdown over third-party badge APIs for:
  - Profile visit counts (use static text or self-hosted counters)
  - Achievement trophies (use static markdown table or native GitHub achievements)
  - Quote widgets (use static quotes or self-hosted alternatives)
- Allowed external services (required for functionality):
  - `github-profile-summary-cards.vercel.app` — profile stats cards
  - `streak-stats.demolab.com` — streak statistics
  - `quotes-github-readme.vercel.app` — dev quotes
  - `img.shields.io` — technology badges (reliable CDN)
- Prohibited external services (unreliable or deprecated):
  - `komarev.com/ghpvc/` — profile view counter (deprecated/unreliable)
  - `github-profile-trophy.vercel.app` — trophy generator (rate-limited, slow)
  - `visitcount.itsvg.in` — visit counter (unreliable)
- External SVG assets must be embedded as base64 data URIs, not linked via URL

