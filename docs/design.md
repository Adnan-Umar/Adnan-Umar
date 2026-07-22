# Design

**Project:** Md Adnan Umar — GitHub Profile  
**Last Updated:** 2026-07-22

---

## 1. Design Philosophy

Three principles drive every visual decision:

1. **Signal over decoration** — every element communicates something about Adnan's work. Decorative elements (particles, noise, scanline) add depth without adding noise to the message.
2. **Motion with purpose** — animations reveal information sequentially, guide the eye, and reinforce a sense of a live terminal. No animation exists purely for spectacle.
3. **Consistent restraint** — a three-colour accent palette (violet / cyan / emerald) used consistently across all assets. No random colour choices.

---

## 2. Colour Palette

### Dark Theme

| Token | Hex | Usage |
|:---|:---|:---|
| `bg` | `#030712` | Canvas background |
| `panel` | `rgba(15,23,42,0.58)` | Glassmorphism panel fill |
| `panel2` | `rgba(15,23,42,0.45)` | Inner panel / code block |
| `border` | `rgba(255,255,255,0.07)` | Panel borders |
| `text1` | `#F8FAFC` | Primary text |
| `text2` | `#94A3B8` | Secondary text |
| `muted` | `#64748B` | Labels, comments |
| `accent1` | `#7C3AED` | Violet — primary accent, keywords |
| `accent2` | `#22D3EE` | Cyan — secondary accent, types |
| `accent3` | `#10B981` | Emerald — status, strings, open-to-work |

### Light Theme

| Token | Hex | Usage |
|:---|:---|:---|
| `bg` | `#F8FAFC` | Canvas background |
| `panel` | `rgba(248,250,252,0.72)` | Glassmorphism panel fill |
| `accent1` | `#2563EB` | Blue — primary accent |
| `accent2` | `#06B6D4` | Cyan — secondary accent |
| `accent3` | `#059669` | Green — status |

---

## 3. Typography

All text uses the system monospace stack:

```
ui-monospace, SFMono-Regular, Menlo, Consolas, monospace
```

This renders as:
- SF Mono on macOS / iOS
- Consolas on Windows
- DejaVu Sans Mono / Liberation Mono on Linux

Chosen because it matches the terminal aesthetic, renders consistently across GitHub's supported platforms, and requires no web font loading.

---

## 4. Layout System

### Hero SVGs (1180×610)

```
┌──────────────────────────────────────────────────────────────┐
│  16px outer glass frame                                       │
│  ┌────────────────────┐  ┌───────────────────────────────┐   │
│  │  LEFT PANEL        │  │  RIGHT PANEL                  │   │
│  │  460×546 px        │  │  640×546 px                   │   │
│  │                    │  │                               │   │
│  │  • Photo (220×220) │  │  • Terminal titlebar          │   │
│  │  • Rotating ring   │  │  • Traffic lights             │   │
│  │  • Name (28px)     │  │  • Name (28px bold)           │   │
│  │  • Role + cursor   │  │  • Role + cursor              │   │
│  │  • Info lines      │  │  • 4 metric stat cards        │   │
│  │  • Skill pills ×2  │  │  • Java code block (8 lines)  │   │
│  │  • Social pills    │  │  • 3 "what I ship" cards      │   │
│  │                    │  │  • Footer quote               │   │
│  └────────────────────┘  └───────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

### Info Card (760×310)

```
┌────────────────────────────────────────────────────────────┐
│  Gradient header bar  |  Traffic lights  |  user@host      │
├──────────┬─────────────────────────────────────────────────┤
│  Avatar  │  user@host header                               │
│  (52px r)│  Name / Role / Location / Education /           │
│          │  Terminal / Packages / Shell / Uptime           │
│  OTW     ├──────────────┬──────────────────────────────────┤
│  badge   │  Skill pills │  // highlights                   │
│          │  (16 skills) │  ◆ item × 4                      │
│          │              │  // web + palette swatches       │
└──────────┴──────────────┴──────────────────────────────────┘
```

---

## 5. Animation System

All animations use SMIL (Synchronized Multimedia Integration Language), the only animation mechanism GitHub's SVG renderer preserves.

### Animation catalogue

| Effect | Mechanism | Duration | Purpose |
|:---|:---|:---|:---|
| Gradient colour cycle | `animate stop-color` | 4–6s loop | Accent colour breathing |
| Border shimmer sweep | `animate x1/x2` on gradient | 2.8s loop | Glass panel shimmer |
| Scanline sweep | `animate y` on mask rect | 3.5s loop | CRT terminal feel |
| Noise texture | `animate seed` on feTurbulence | 12s loop | Grain / film texture |
| Pulsing ring | `animate r` + `animate stroke-opacity` | 3s loop | Avatar vitality |
| Rotating dashed ring | `animateTransform type=rotate` | 18s loop | Orbital movement |
| Floating particles | `animate cy` + `animate opacity` | 5–9s loop | Depth / atmosphere |
| Staggered text reveal | `animate opacity` with `begin` delay | 0.3s each | Sequential information reveal |
| Traffic light pulse | `animate opacity` | 2.1s loop | Terminal authenticity |
| Cursor blink | `animate opacity` 1→0→1 | 1s loop | Active typing illusion |
| Pulsing open-to-work | `animate r` | 1.6s loop | Status prominence |
| Ambient blob | `animate stop-opacity` | 7–9s loop | Background depth |

### Reveal timing sequence (hero SVGs)

```
0.0s  canvas fades in
0.5s  name appears
0.8s  role + cursor
1.1s  info line 1 (location)
1.3s  info line 2 (education)
1.5s  info line 3 (focus)
1.7s  info line 4 (status)
2.1s  metric cards
2.4s  skill pills (staggered)
2.7s  social links
2.0s  code block (right panel)
2.5s  what-I-ship cards
```

---

## 6. Photo Processing Pipeline

The avatar photo is embedded as base64 directly into the SVGs:
- `scripts/pic-b64.txt` contains the base64 data URI
- `make_info_card.py` reads `pic-b64.txt` and embeds it into `info-card.svg`
- `dark.svg` and `light.svg` were hand-crafted with the same base64 embedded
- If `pic-b64.txt` is missing, `make_info_card.py` extracts the base64 from the existing `info-card.svg`

The base64 image is a circular-cropped PNG with soft alpha edges, embedded inside an SVG `<clipPath>` for the avatar circle.

---

## 7. Design Decisions — Quick Reference

| Decision | Choice | Reason |
|:---|:---|:---|
| Animation technology | SMIL only | GitHub strips CSS and JS from SVGs |
| Photo embedding | base64 data URI | GitHub Camo proxy blocks external image URLs |
| Font | System monospace stack | No web font loading; consistent across platforms |
| Layout | Split panel (photo left / terminal right) | Clear separation of identity vs. technical detail |
| Colour accent count | 3 (violet/cyan/emerald or blue/cyan/green) | Enough variety without visual noise |
| Card dimensions | Hero 1180×610, Info 760×310, Heatmap 801×191 | Optimised for GitHub profile column width |
| Background removal | rembg (u2net) | Best quality for headshot photos; no manual masking |
