"""
render_heatmap_svg.py
Reads data/contributions.json and renders an animated GitHub-style
contribution heatmap SVG to contrib-heatmap.svg.

Usage:
    python scripts/render_heatmap_svg.py
    python scripts/render_heatmap_svg.py data/contributions.json contrib-heatmap.svg
"""

import sys
import json
import datetime

# ── Design constants ──────────────────────────────────────────────────────────
CELL      = 11      # cell size (px)
GAP       = 3       # gap between cells
WEEKS     = 53
DAYS      = 7
LABEL_W   = 30      # left gutter for day labels (Mon/Wed/Fri)
LABEL_H   = 20      # top gutter for month labels
PAD_X     = 16      # outer horizontal padding
PAD_Y     = 16      # outer vertical padding
FOOTER_H  = 44      # space below grid for legend + stats text

# Derived geometry
GRID_W    = WEEKS * (CELL + GAP) - GAP          # 53*(11+3)-3 = 737
GRID_H    = DAYS  * (CELL + GAP) - GAP          # 7*(11+3)-3  = 95
CANVAS_W  = PAD_X * 2 + LABEL_W + GRID_W        # 16+16+30+737 = 799
CANVAS_H  = PAD_Y * 2 + LABEL_H + GRID_H + FOOTER_H  # 16+16+20+95+44 = 207

# Grid origin (top-left corner of first cell)
OX = PAD_X + LABEL_W   # 46
OY = PAD_Y + LABEL_H   # 36

# GitHub-style green ramp (level 0-5)
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

# Month abbreviations
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def render(input_path: str = "data/contributions.json",
           output_path: str = "contrib-heatmap.svg") -> None:

    # ── Load data ─────────────────────────────────────────────────────────────
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days_list  = data.get("days", [])
    total      = data.get("total", 0)
    username   = data.get("username", "user")
    best_day   = data.get("best_day", {})
    best_count = best_day.get("count", 0)
    best_date  = best_day.get("date", "")

    # Build date → cell map
    day_map = {d["date"]: d for d in days_list}
    dates   = sorted(day_map.keys())
    if not dates:
        print("No contribution data found in", input_path)
        sys.exit(1)

    # Align start to Monday of the week containing the first date
    first = datetime.date.fromisoformat(dates[0])
    # weekday(): Mon=0 … Sun=6 — subtract to get the Monday of that week
    start = first - datetime.timedelta(days=first.weekday())

    # Build 53×7 grid
    grid: list[list[dict | None]] = []
    for wi in range(WEEKS):
        col: list[dict | None] = []
        for di in range(DAYS):
            d = start + datetime.timedelta(weeks=wi, days=di)
            col.append(day_map.get(d.strftime("%Y-%m-%d")))
        grid.append(col)

    # ── Collect month label positions ─────────────────────────────────────────
    month_labels: list[tuple[int, str]] = []
    seen_months: set[int] = set()
    for wi, col in enumerate(grid):
        for di, cell in enumerate(col):
            if cell is None:
                continue
            d = datetime.date.fromisoformat(cell["date"])
            if d.month not in seen_months:
                seen_months.add(d.month)
                month_labels.append((wi, MONTHS[d.month - 1]))
            break  # only need first hit per week

    # ── SVG builder ───────────────────────────────────────────────────────────
    parts: list[str] = []

    def w(line: str) -> None:
        parts.append(line)

    w(f'<svg xmlns="http://www.w3.org/2000/svg"'
      f' viewBox="0 0 {CANVAS_W} {CANVAS_H}"'
      f' width="{CANVAS_W}" height="{CANVAS_H}">')

    # ── Defs ──────────────────────────────────────────────────────────────────
    w('<defs>')
    w('  <linearGradient id="shimmer" x1="-100%" y1="0%" x2="0%" y2="0%">')
    w('    <stop offset="0%"   stop-color="rgba(255,255,255,0)"/>')
    w('    <stop offset="50%"  stop-color="rgba(255,255,255,0.35)"/>')
    w('    <stop offset="100%" stop-color="rgba(255,255,255,0)"/>')
    w('    <animate attributeName="x1" values="-100%;100%" dur="3s" repeatCount="indefinite"/>')
    w('    <animate attributeName="x2" values="0%;200%"    dur="3s" repeatCount="indefinite"/>')
    w('  </linearGradient>')
    w('  <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">')
    w('    <stop offset="0%"   stop-color="#7C3AED">')
    w('      <animate attributeName="stop-color" values="#7C3AED;#22D3EE;#7C3AED" dur="5s" repeatCount="indefinite"/>')
    w('    </stop>')
    w('    <stop offset="100%" stop-color="#22D3EE">')
    w('      <animate attributeName="stop-color" values="#22D3EE;#7C3AED;#22D3EE" dur="5s" repeatCount="indefinite"/>')
    w('    </stop>')
    w('  </linearGradient>')
    w('</defs>')

    # ── Background ────────────────────────────────────────────────────────────
    w(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="16" fill="#0d1117"/>')

    # Border
    w(f'<rect x="0.5" y="0.5" width="{CANVAS_W - 1}" height="{CANVAS_H - 1}" rx="15.5"'
      f' fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="1">')
    w('  <animate attributeName="stroke-opacity" values="0.07;0.15;0.07" dur="3s" repeatCount="indefinite"/>')
    w('</rect>')
    w(f'<rect x="0.5" y="0.5" width="{CANVAS_W - 1}" height="{CANVAS_H - 1}" rx="15.5"'
      f' fill="none" stroke="url(#shimmer)" stroke-width="1" opacity="0.5"/>')

    # ── Month labels ──────────────────────────────────────────────────────────
    w('<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"'
      ' font-size="10" fill="#8b949e">')
    for wi, label in month_labels:
        x = OX + wi * (CELL + GAP)
        y = OY - 6
        w(f'  <text x="{x}" y="{y}">{label}</text>')
    w('</g>')

    # ── Day-of-week labels (Mon/Wed/Fri on rows 1/3/5) ────────────────────────
    w('<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"'
      ' font-size="9" fill="#8b949e" text-anchor="end">')
    for di, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = OY + di * (CELL + GAP) + CELL - 1
        w(f'  <text x="{OX - 4}" y="{y}">{label}</text>')
    w('</g>')

    # ── Cell grid with diagonal reveal animation ──────────────────────────────
    for wi, col in enumerate(grid):
        for di, cell in enumerate(col):
            if cell is None:
                continue
            level  = min(cell.get("level", 0), 5)
            color  = PALETTE[level]
            cx     = OX + wi * (CELL + GAP)
            cy     = OY + di * (CELL + GAP)
            # Diagonal stagger: earlier weeks/rows appear first
            delay  = round((wi * 0.04 + di * 0.015), 3)
            w(f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="2"'
              f' fill="{color}" opacity="0">'
              f'<animate attributeName="opacity" values="0;1" dur="0.3s"'
              f' fill="freeze" begin="{delay}s"/>'
              f'</rect>')

    # ── Legend ────────────────────────────────────────────────────────────────
    legend_y = OY + GRID_H + 16
    legend_x = OX
    w('<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"'
      f' font-size="10" fill="#8b949e">')
    w(f'  <text x="{legend_x}" y="{legend_y + CELL - 1}">Less</text>')
    swatch_start = legend_x + 34
    for i, color in enumerate(PALETTE):
        sx = swatch_start + i * (CELL + 2)
        w(f'  <rect x="{sx}" y="{legend_y}" width="{CELL}" height="{CELL}" rx="2" fill="{color}"/>')
    more_x = swatch_start + len(PALETTE) * (CELL + 2) + 4
    w(f'  <text x="{more_x}" y="{legend_y + CELL - 1}">More</text>')
    w('</g>')

    # ── Stats footer ─────────────────────────────────────────────────────────
    stats_y = legend_y + CELL + 14
    w('<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"'
      ' font-size="10" fill="#8b949e">')
    w(f'  <text x="{PAD_X}" y="{stats_y}">'
      f'{total:,} contributions in the last year'
      f'</text>')
    if best_date:
        best_label = f'  &#9650; best day: {best_count} on {best_date}'
        w(f'  <text x="{CANVAS_W // 2}" y="{stats_y}" text-anchor="middle">'
          f'{best_count} on {best_date}'
          f'</text>')
    w(f'  <text x="{CANVAS_W - PAD_X}" y="{stats_y}" text-anchor="end">'
      f'@{username}'
      f'</text>')
    w('</g>')

    w('</svg>')

    # ── Write output ──────────────────────────────────────────────────────────
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

    print(f"Heatmap written → {output_path}  ({CANVAS_W}×{CANVAS_H}px, {len(days_list)} days)")


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"
    render(inp, out)
