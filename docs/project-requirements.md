# Project Requirements

**Project:** Md Adnan Umar — GitHub Profile Repository  
**Owner:** Md Adnan Umar  
**Status:** Production  
**Last Updated:** 2026-07-22

---

## 1. Goal

Produce a flagship GitHub profile repository that represents Md Adnan Umar's background as a Software Engineer. The result must be visually premium, technically correct, and fully automated — comparable in quality to the best public GitHub profiles while being entirely original.

---

## 2. Functional Requirements

### 2.1 Hero SVG Banners

| ID | Requirement |
|:---|:---|
| FR-01 | `dark.svg` renders on dark-mode GitHub backgrounds |
| FR-02 | `light.svg` renders on light-mode GitHub backgrounds |
| FR-03 | README switches hero automatically via `<picture>` + `prefers-color-scheme` |
| FR-04 | Both SVGs are 1180×610 px, pure SVG, no JavaScript |
| FR-05 | Left panel contains circular photo with animated ring, name, role, info lines, skill pills, social links |
| FR-06 | Right panel contains terminal window with code block, metric cards, "what I ship" section |
| FR-07 | All animations use SMIL only (`animate`, `animateTransform`) |
| FR-08 | Photo is embedded as base64 data URI — no external HTTP requests |
| FR-09 | Animations include: gradient sweep, scanline, border shimmer, floating particles, pulsing ring, staggered reveals |
| FR-10 | GitHub CDN renders the SVGs without sanitisation issues |

### 2.2 Info Card

| ID | Requirement |
|:---|:---|
| FR-11 | `info-card.svg` is a neofetch-style terminal card, 760×310 px |
| FR-12 | Gradient header bar with traffic lights and `user@host` title |
| FR-13 | Circular photo avatar with pulsing ring and rotating dashed border |
| FR-14 | Open-to-work animated badge below avatar |
| FR-15 | Left column: avatar + neofetch info lines (Name, Role, Location, Education, Terminal, Packages, Shell, Uptime) |
| FR-16 | Right column: skill pills (16 skills, 3 colour variants) + highlights list + website + palette swatches |
| FR-17 | All reveals staggered with SMIL `begin` delays |

### 2.3 Contribution Heatmap

| ID | Requirement |
|:---|:---|
| FR-18 | `contrib-heatmap.svg` renders a 53-week GitHub-style contribution heatmap |
| FR-19 | Cells appear with diagonal stagger animation |
| FR-20 | Legend with 6-level green ramp |
| FR-21 | Stats footer: total contributions, best day, username |
| FR-22 | Month labels and day-of-week labels correctly positioned |
| FR-23 | Refreshed automatically on schedule via GitHub Actions |

### 2.4 README

| ID | Requirement |
|:---|:---|
| FR-24 | Contains all 14 sections: `whoami`, `about.java`, `neofetch`, `education`, `experience`, `focus`, `tech-stack`, `projects`, `open-source`, `github-stats`, `contribution-graph`, `achievements`, `timeline`, `connect` |
| FR-25 | No generic developer clichés |
| FR-26 | Java code block in `about.java` section reflects real stack |
| FR-27 | Projects table links to real repositories |
| FR-28 | Stats cards use `github-profile-summary-cards`, streak via `streak-stats.demolab.com` |
| FR-29 | `<picture>` tag switches between `dark.svg` and `light.svg` |

### 2.5 Automation

| ID | Requirement |
|:---|:---|
| FR-30 | `update-profile.yml` refreshes contribution data daily and rebuilds SVGs |
| FR-31 | Workflow commits generated assets with `[skip ci]` to prevent infinite loops |
| FR-32 | `snake.yml` generates the contribution snake animation |

---

## 3. Non-Functional Requirements

| ID | Requirement |
|:---|:---|
| NFR-01 | All SVG assets render correctly in GitHub's SVG sanitiser |
| NFR-02 | No `<script>` or `<style>` tags in SVG — GitHub strips them |
| NFR-03 | No external URL references in SVG — GitHub proxy blocks them |
| NFR-04 | Hero SVGs ≤ 250 KB each (GitHub's image display limit) |
| NFR-05 | Info card ≤ 200 KB |
| NFR-06 | Python scripts run with Python 3.10+ |
| NFR-07 | All dependencies pinned in `requirements.txt` |
| NFR-08 | Repository passes GitHub Actions without secrets beyond `GITHUB_TOKEN` |

---

## 4. Out of Scope

- Mobile-responsive SVG layout (GitHub renders at fixed width)
- Dynamic real-time data in SVGs (requires server-side rendering)
- CSS animations (GitHub strips `<style>` from SVGs)
- JavaScript interactions
