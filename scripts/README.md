# Profile Art Scripts

## Overview
This folder contains Python scripts that generate the animated SVG assets for the GitHub profile.

## Scripts

### `prep_photo.py`
Removes background and boosts local contrast from a source photo.
```bash
python scripts/prep_photo.py source-photo.jpg
```
Outputs `source-prepped.png`.

### `make_ascii_svg.py`
Converts a prep photo into an animated monochrome ASCII SVG.
```bash
python scripts/make_ascii_svg.py source-prepped.png ascii-art.svg
```

### `make_info_card.py`
Generates a neofetch-style terminal info card.
```bash
python scripts/make_info_card.py
```
Outputs `info-card.svg`.

### `fetch_contributions.py`
Scrapes public GitHub contribution data without a token.
```bash
python scripts/fetch_contributions.py Adnan-Umar
```
Outputs `data/contributions.json`.

### `render_heatmap_svg.py`
Renders the contribution JSON as an animated heatmap.
```bash
python scripts/render_heatmap_svg.py
```
Outputs `contrib-heatmap.svg`.

### `render_contribution_month.py`
Renders a self-contained "Last 30 Days" contribution detail bar chart from
`data/contributions.json`. Replaces the external `github-readme-activity-graph`
service (which suffers from outages / rate-limiting).
```bash
python scripts/render_contribution_month.py
```
Outputs `contribution-month.svg`.

### `render_stats_card.py`
Generates self-contained GitHub stats + streak card SVGs from
`data/contributions.json`. Replaces the external `github-profile-summary-cards`
and `streak-stats` services (which suffer from rate-limiting / 500 errors).
```bash
python scripts/render_stats_card.py
```
Outputs `github-stats.svg` and `github-streak.svg`.

### `render_top_languages.py`
Generates a self-contained "Top Languages" card SVG from the GitHub API
(stdlib only, no third-party dependency). Replaces the external
`github-readme-stats` top-langs service (which suffers from rate-limiting /
500 errors). Top 8 languages are shown with byte counts and percentages.
```bash
python scripts/render_top_languages.py
python scripts/render_top_languages.py Adnan-Umar top-languages.svg
```
Outputs `top-languages.svg`.

## Notes
- `rembg` downloads ML models on first run (~300 MB).
- The daily GitHub Actions workflow only requires `requests` and `beautifulsoup4`.
- Photo-based scripts require `Pillow`, `numpy`, `opencv-python`, and `rembg`.
