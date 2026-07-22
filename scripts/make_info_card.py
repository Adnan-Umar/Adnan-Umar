"""
make_info_card.py
Generates info-card.svg — a premium neofetch-style terminal card with:
  • Embedded circular avatar (from scripts/pic-b64.txt)
  • Two-column layout  (avatar + OS-style left | skill pills + highlights right)
  • Gradient header bar with traffic lights
  • Staggered SMIL animated line reveals  (no JavaScript)
  • Colour-theme tokens  (easy to swap)
  • Modular builder functions

Usage (from repo root):
    python scripts/make_info_card.py
    python scripts/make_info_card.py info-card.svg
"""

from __future__ import annotations
import base64
import io
import os
import pathlib
import sys
from dataclasses import dataclass, field
from typing import Sequence


# ─────────────────────────────────────────────────────────────────────────────
#  Profile data
# ─────────────────────────────────────────────────────────────────────────────
PROFILE = {
    "name":      "Md Adnan Umar",
    "user":      "adnan",
    "host":      "backend",
    "role":      "Software Engineer",
    "location":  "India \U0001f1ee\U0001f1f3",
    "education": "B.Tech CSE \u00b7 Final Year",
    "terminal":  "Spring Boot 3 \u00b7 Java 21",
    "packages":  "Kafka \u00b7 K8s \u00b7 Docker \u00b7 Spring AI",
    "shell":     "Event-driven microservices",
    "uptime":    "Building since 2022",
    "website":   "adnan-portfolio-lykp.onrender.com",
    "skills": [
        ("Java",         "cyan"),
        ("Spring Boot",  "violet"),
        ("Kafka",        "emerald"),
        ("Kubernetes",   "violet"),
        ("Docker",       "cyan"),
        ("PostgreSQL",   "emerald"),
        ("Redis",        "cyan"),
        ("Python",       "violet"),
        ("React",        "emerald"),
        ("Next.js",      "cyan"),
        ("Spring AI",    "violet"),
        ("FastAPI",      "emerald"),
        ("CI/CD",        "cyan"),
        ("AWS",          "violet"),
        ("TypeScript",   "emerald"),
        ("Git",          "cyan"),
    ],
    "highlights": [
        "Distributed microservices on Kubernetes",
        "Event-driven pipelines with Apache Kafka",
        "AI-integrated Spring Boot applications",
        "Clean, observable, scalable systems",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
#  Theme tokens
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class Theme:
    bg:         str = "#0A0F1E"
    panel:      str = "rgba(15,23,42,0.55)"
    border:     str = "rgba(255,255,255,0.07)"
    text1:      str = "#F8FAFC"
    text2:      str = "#94A3B8"
    muted:      str = "#64748B"
    cyan:       str = "#22D3EE"
    violet:     str = "#A78BFA"
    emerald:    str = "#34D399"
    accent1:    str = "#7C3AED"
    accent2:    str = "#22D3EE"
    accent3:    str = "#10B981"
    # pill fills / strokes per colour name
    pill_fill:  dict = field(default_factory=lambda: {
        "cyan":    ("rgba(34,211,238,0.12)",  "rgba(34,211,238,0.35)"),
        "violet":  ("rgba(124,58,237,0.12)",  "rgba(124,58,237,0.35)"),
        "emerald": ("rgba(16,185,129,0.12)",  "rgba(16,185,129,0.35)"),
    })
    pill_text:  dict = field(default_factory=lambda: {
        "cyan":    "#22D3EE",
        "violet":  "#A78BFA",
        "emerald": "#34D399",
    })


DARK = Theme()

# ─────────────────────────────────────────────────────────────────────────────
#  Canvas geometry
# ─────────────────────────────────────────────────────────────────────────────
W        = 760    # total width
H        = 310    # total height
HDR_H    = 46     # header bar height
AVATAR_X = 18     # avatar centre-x
AVATAR_Y = HDR_H + 62   # avatar centre-y
AVATAR_R = 52     # avatar radius
INFO_X   = AVATAR_X * 2 + AVATAR_R * 2 + 14   # right of avatar
INFO_Y   = HDR_H + 18
PILL_X0  = INFO_X
PILL_Y0  = HDR_H + 172
RIGHT_X  = 400    # second column x (highlights)
FONT     = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

# ─────────────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _e(text: str) -> str:
    """XML-escape minimal set."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _pill(x: int, y: int, label: str, colour: str, t: Theme,
          begin: float, w: int | None = None) -> list[str]:
    PH, PR = 20, 10
    pw   = w or (len(label) * 7 + 20)
    fill, stroke = t.pill_fill[colour]
    fc   = t.pill_text[colour]
    return [
        f'<rect x="{x}" y="{y}" width="{pw}" height="{PH}" rx="{PR}"'
        f' fill="{fill}" stroke="{stroke}" stroke-width="1">',
        f'  <animate attributeName="stroke-opacity" values="0.35;0.75;0.35"'
        f' dur="2.6s" repeatCount="indefinite" begin="{begin:.2f}s"/>',
        f'</rect>',
        f'<text x="{x + pw//2}" y="{y + PH//2 + 4}" font-family="{FONT}"'
        f' font-size="9" fill="{fc}" text-anchor="middle">{_e(label)}</text>',
    ]


def _reveal_group(content: list[str], begin: float) -> list[str]:
    lines = [f'<g opacity="0">',
             f'  <animate attributeName="opacity" values="0;1" dur="0.25s"'
             f' fill="freeze" begin="{begin:.2f}s"/>']
    lines += content
    lines.append('</g>')
    return lines


def _info_row(label: str, value: str, y: int, t: Theme,
              begin: float, value_colour: str | None = None) -> list[str]:
    vc = value_colour or t.text2
    inner = [
        f'<text x="{INFO_X}" y="{y}" font-family="{FONT}"'
        f' font-size="11" fill="{t.muted}">{_e(label)}</text>',
        f'<text x="{INFO_X + 76}" y="{y}" font-family="{FONT}"'
        f' font-size="11" fill="{vc}">{_e(value)}</text>',
    ]
    return _reveal_group(inner, begin)


# ─────────────────────────────────────────────────────────────────────────────
#  Section builders
# ─────────────────────────────────────────────────────────────────────────────
def _build_defs(t: Theme) -> list[str]:
    return [
        '<defs>',
        f'  <linearGradient id="accentG" x1="0%" y1="0%" x2="100%" y2="0%">',
        f'    <stop offset="0%"   stop-color="{t.accent1}">',
        f'      <animate attributeName="stop-color"'
        f' values="{t.accent1};{t.accent2};{t.accent1}" dur="5s" repeatCount="indefinite"/>',
        f'    </stop>',
        f'    <stop offset="100%" stop-color="{t.accent2}">',
        f'      <animate attributeName="stop-color"'
        f' values="{t.accent2};{t.accent1};{t.accent2}" dur="5s" repeatCount="indefinite"/>',
        f'    </stop>',
        f'  </linearGradient>',
        f'  <linearGradient id="headerG" x1="0%" y1="0%" x2="100%" y2="0%">',
        f'    <stop offset="0%"   stop-color="{t.accent1}" stop-opacity="0.35"/>',
        f'    <stop offset="60%"  stop-color="{t.accent2}" stop-opacity="0.18"/>',
        f'    <stop offset="100%" stop-color="{t.accent3}" stop-opacity="0.08"/>',
        f'  </linearGradient>',
        f'  <linearGradient id="shimmer" x1="-100%" y1="0%" x2="0%" y2="0%">',
        f'    <stop offset="0%"   stop-color="rgba(255,255,255,0)"/>',
        f'    <stop offset="50%"  stop-color="rgba(255,255,255,0.28)"/>',
        f'    <stop offset="100%" stop-color="rgba(255,255,255,0)"/>',
        f'    <animate attributeName="x1" values="-100%;100%" dur="3s" repeatCount="indefinite"/>',
        f'    <animate attributeName="x2" values="0%;200%"    dur="3s" repeatCount="indefinite"/>',
        f'  </linearGradient>',
        f'  <radialGradient id="blob1" cx="12%" cy="50%" r="40%">',
        f'    <stop offset="0%" stop-color="{t.accent1}" stop-opacity="0.14">',
        f'      <animate attributeName="stop-opacity" values="0.14;0.04;0.14" dur="6s" repeatCount="indefinite"/>',
        f'    </stop>',
        f'    <stop offset="100%" stop-color="{t.accent1}" stop-opacity="0"/>',
        f'  </radialGradient>',
        f'  <clipPath id="avatarClip"><circle cx="{AVATAR_X + AVATAR_R}" cy="{AVATAR_Y}" r="{AVATAR_R}"/></clipPath>',
        f'  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">',
        f'    <feGaussianBlur stdDeviation="2.5" result="b"/>',
        f'    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>',
        f'  </filter>',
        '</defs>',
    ]


def _build_background(t: Theme) -> list[str]:
    return [
        f'<rect width="{W}" height="{H}" rx="14" fill="{t.bg}"/>',
        f'<rect width="{W}" height="{H}" rx="14" fill="url(#blob1)"/>',
    ]


def _build_header(t: Theme) -> list[str]:
    cx, cy, r = 22, HDR_H // 2, 5.5
    return [
        # gradient bar
        f'<rect x="0" y="0" width="{W}" height="{HDR_H}" rx="14" fill="url(#headerG)"/>',
        f'<rect x="0" y="{HDR_H - 10}" width="{W}" height="10" fill="url(#headerG)" opacity="0.5"/>',
        # accent underline
        f'<line x1="0" y1="{HDR_H}" x2="{W}" y2="{HDR_H}"'
        f' stroke="url(#accentG)" stroke-width="1.5" opacity="0.55"/>',
        # traffic lights
        f'<circle cx="{cx}"      cy="{cy}" r="{r}" fill="#FF5F57">'
        f'<animate attributeName="opacity" values="1;0.7;1" dur="2.1s" repeatCount="indefinite"/></circle>',
        f'<circle cx="{cx + 18}" cy="{cy}" r="{r}" fill="#FEBC2E">'
        f'<animate attributeName="opacity" values="1;0.7;1" dur="2.1s" repeatCount="indefinite" begin="0.2s"/></circle>',
        f'<circle cx="{cx + 36}" cy="{cy}" r="{r}" fill="#28C840">'
        f'<animate attributeName="opacity" values="1;0.7;1" dur="2.1s" repeatCount="indefinite" begin="0.4s"/></circle>',
        # title
        f'<text x="{W//2}" y="{HDR_H//2 + 4}" font-family="{FONT}"'
        f' font-size="11" fill="{t.muted}" text-anchor="middle">'
        f'neofetch \u2014 {PROFILE["user"]}@{PROFILE["host"]}</text>',
    ]


def _build_avatar(b64_uri: str, t: Theme) -> list[str]:
    cx = AVATAR_X + AVATAR_R
    cy = AVATAR_Y
    return [
        # photo
        f'<image href="{b64_uri}" x="{AVATAR_X}" y="{cy - AVATAR_R}"'
        f' width="{AVATAR_R * 2}" height="{AVATAR_R * 2}"'
        f' clip-path="url(#avatarClip)" preserveAspectRatio="xMidYMid slice"/>',
        # pulsing outer ring
        f'<circle cx="{cx}" cy="{cy}" r="{AVATAR_R + 4}" fill="none"'
        f' stroke="{t.accent2}" stroke-width="1.5" opacity="0.45">',
        f'  <animate attributeName="r" values="{AVATAR_R+4};{AVATAR_R+7};{AVATAR_R+4}" dur="3s" repeatCount="indefinite"/>',
        f'  <animate attributeName="stroke-opacity" values="0.45;0.85;0.45" dur="3s" repeatCount="indefinite"/>',
        f'</circle>',
        # dashed rotate ring
        f'<circle cx="{cx}" cy="{cy}" r="{AVATAR_R + 10}" fill="none"'
        f' stroke="{t.accent1}" stroke-width="1" stroke-dasharray="5 4" opacity="0.3">',
        f'  <animateTransform attributeName="transform" type="rotate"'
        f' from="0 {cx} {cy}" to="360 {cx} {cy}" dur="18s" repeatCount="indefinite"/>',
        f'</circle>',
        # open-to-work badge
        f'<rect x="{AVATAR_X}" y="{cy + AVATAR_R + 6}" width="{AVATAR_R * 2}" height="18" rx="9"'
        f' fill="{t.pill_fill["emerald"][0]}" stroke="{t.pill_fill["emerald"][1]}" stroke-width="1">',
        f'  <animate attributeName="stroke-opacity" values="0.35;0.75;0.35" dur="2s" repeatCount="indefinite"/>',
        f'</rect>',
        f'<circle cx="{AVATAR_X + 12}" cy="{cy + AVATAR_R + 15}" r="3.5" fill="{t.accent3}">',
        f'  <animate attributeName="r" values="3.5;4.5;3.5" dur="1.6s" repeatCount="indefinite"/>',
        f'</circle>',
        f'<text x="{AVATAR_X + AVATAR_R + 4}" y="{cy + AVATAR_R + 19}" font-family="{FONT}"'
        f' font-size="8.5" fill="{t.accent3}" text-anchor="middle">accepting offers</text>',
    ]


def _build_info_lines(t: Theme) -> list[str]:
    rows = [
        ("Name",      PROFILE["name"],     None,       0.5),
        ("Role",      PROFILE["role"],      "url(#accentG)", 0.7),
        ("Location",  PROFILE["location"], None,       0.9),
        ("Education", PROFILE["education"],None,       1.1),
        ("Terminal",  PROFILE["terminal"], None,       1.3),
        ("Packages",  PROFILE["packages"], None,       1.5),
        ("Shell",     PROFILE["shell"],    None,       1.7),
        ("Uptime",    PROFILE["uptime"],   None,       1.9),
    ]
    out: list[str] = []
    y = INFO_Y
    # user@host header
    out += _reveal_group([
        f'<text x="{INFO_X}" y="{y}" font-family="{FONT}" font-size="12"'
        f' font-weight="700" fill="{t.accent2}" filter="url(#glow)">{PROFILE["user"]}</text>',
        f'<text x="{INFO_X + len(PROFILE["user"])*8}" y="{y}" font-family="{FONT}"'
        f' font-size="12" fill="{t.muted}">@</text>',
        f'<text x="{INFO_X + len(PROFILE["user"])*8 + 10}" y="{y}" font-family="{FONT}"'
        f' font-size="12" font-weight="700" fill="{t.accent3}" filter="url(#glow)">{PROFILE["host"]}</text>',
        f'<line x1="{INFO_X}" y1="{y + 5}" x2="{RIGHT_X - 10}" y2="{y + 5}"'
        f' stroke="{t.border}" stroke-width="1"/>',
    ], 0.35)
    y += 20
    for label, value, vc, begin in rows:
        inner = [
            f'<text x="{INFO_X}" y="{y}" font-family="{FONT}"'
            f' font-size="10.5" fill="{t.muted}">{_e(label)}</text>',
            f'<text x="{INFO_X + 76}" y="{y}" font-family="{FONT}"'
            f' font-size="10.5" fill="{vc or t.text2}">{_e(value)}</text>',
        ]
        out += _reveal_group(inner, begin)
        y += 17
    return out


def _build_palette(t: Theme, begin: float = 2.2) -> list[str]:
    swatches = [t.bg, t.accent1, t.accent2, t.accent3,
                "#F8FAFC", "#A78BFA", "#34D399", "#94A3B8"]
    cx = AVATAR_X
    y  = AVATAR_Y + AVATAR_R + 34
    inner = [
        f'<text x="{cx}" y="{y}" font-family="{FONT}" font-size="8.5" fill="{t.muted}">// palette</text>',
    ]
    sx = cx
    for colour in swatches:
        inner.append(
            f'<rect x="{sx}" y="{y + 6}" width="14" height="14" rx="3" fill="{colour}"/>'
        )
        sx += 18
    return _reveal_group(inner, begin)


def _build_pills(t: Theme) -> list[str]:
    """Lay out skill pills in two rows, left column."""
    out: list[str] = [
        f'<text x="{PILL_X0}" y="{PILL_Y0 - 8}" font-family="{FONT}"'
        f' font-size="9" fill="{t.muted}">// stack</text>',
    ]
    PH, GAP_X, GAP_Y = 20, 6, 5
    x, y = PILL_X0, PILL_Y0
    max_x = RIGHT_X - 8
    begin = 2.05
    for label, colour in PROFILE["skills"]:
        pw = len(label) * 7 + 20
        if x + pw > max_x:
            x  = PILL_X0
            y += PH + GAP_Y
        out += _reveal_group(_pill(x, y, label, colour, t, begin), begin)
        x += pw + GAP_X
        begin += 0.06
    return out


def _build_highlights(t: Theme) -> list[str]:
    """Right column: highlights list."""
    x = RIGHT_X
    y = HDR_H + 18
    out: list[str] = []
    out += _reveal_group([
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="10"'
        f' font-weight="600" fill="{t.accent2}">// highlights</text>',
        f'<line x1="{x}" y1="{y + 5}" x2="{W - 16}" y2="{y + 5}"'
        f' stroke="{t.border}" stroke-width="1"/>',
    ], 2.0)
    y += 20
    begin = 2.15
    for h in PROFILE["highlights"]:
        out += _reveal_group([
            f'<text x="{x + 14}" y="{y}" font-family="{FONT}"'
            f' font-size="10" fill="{t.text2}">\u25c6  {_e(h)}</text>',
        ], begin)
        y += 18
        begin += 0.15

    # website
    y += 6
    out += _reveal_group([
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="9" fill="{t.muted}">// web</text>',
        f'<text x="{x}" y="{y + 14}" font-family="{FONT}"'
        f' font-size="9.5" fill="{t.accent2}">{_e(PROFILE["website"])}</text>',
    ], 2.8)

    # colour palette (right side)
    y += 34
    swatches = [t.bg, t.accent1, t.accent2, t.accent3,
                "#F8FAFC", "#A78BFA", "#34D399", "#94A3B8"]
    inner = [
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="8.5" fill="{t.muted}">// palette</text>',
    ]
    sx = x
    for colour in swatches:
        inner.append(f'<rect x="{sx}" y="{y + 6}" width="13" height="13" rx="3" fill="{colour}"/>')
        sx += 17
    out += _reveal_group(inner, 3.0)
    return out


def _build_border(t: Theme) -> list[str]:
    return [
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="13.5"'
        f' fill="none" stroke="{t.border}" stroke-width="1">',
        f'  <animate attributeName="stroke-opacity" values="0.07;0.18;0.07" dur="3s" repeatCount="indefinite"/>',
        f'</rect>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="13.5"'
        f' fill="none" stroke="url(#shimmer)" stroke-width="1" opacity="0.55"/>',
    ]


# ─────────────────────────────────────────────────────────────────────────────
#  Main assembler
# ─────────────────────────────────────────────────────────────────────────────
def build_info_card(b64_uri: str,
                    theme: Theme = DARK,
                    output_path: str = "info-card.svg") -> None:
    sections: list[list[str]] = [
        [f'<svg xmlns="http://www.w3.org/2000/svg"'
         f' viewBox="0 0 {W} {H}" width="{W}" height="{H}">'],
        _build_defs(theme),
        _build_background(theme),
        _build_header(theme),
        _build_avatar(b64_uri, theme),
        _build_info_lines(theme),
        _build_pills(theme),
        _build_highlights(theme),
        _build_border(theme),
        ["</svg>"],
    ]
    svg = "\n".join(line for section in sections for line in section)
    out = pathlib.Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    kb = out.stat().st_size // 1024
    print(f"  info-card.svg  {W}x{H}  {kb} KB  ->  {out}")


# ─────────────────────────────────────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    b64_path = pathlib.Path("scripts/pic-b64.txt")
    if b64_path.exists():
        b64_uri = b64_path.read_text(encoding="utf-8").strip()
    else:
        svg_path = pathlib.Path("info-card.svg")
        if svg_path.exists():
            text = svg_path.read_text(encoding="utf-8")
            start_marker = '<image href="data:image/png;base64,'
            idx = text.find(start_marker)
            if idx != -1:
                start = idx + len(start_marker)
                end = text.find('"', start)
                b64_uri = 'data:image/png;base64,' + text[start:end]
            else:
                print("ERROR: no embedded image found in info-card.svg", file=sys.stderr)
                sys.exit(1)
        else:
            print("ERROR: scripts/pic-b64.txt not found and no info-card.svg to extract from.", file=sys.stderr)
            sys.exit(1)

    out = sys.argv[1] if len(sys.argv) > 1 else "info-card.svg"
    print(f"Building {out} …")
    build_info_card(b64_uri, DARK, out)
    print("Done.")


if __name__ == "__main__":
    main()
