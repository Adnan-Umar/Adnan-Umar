"""
render_monthly_heatmap.py
Generates a compact 4-week contribution heatmap SVG showing the last 28 days.

Usage:
    python scripts/render_monthly_heatmap.py
    python scripts/render_monthly_heatmap.py data/contributions.json monthly-heatmap.svg
"""

import sys
import json
import datetime

CELL = 11
GAP = 3
WEEKS = 4
DAYS = 7
PAD_X = 16
PAD_Y = 16

GRID_W = WEEKS * (CELL + GAP) - GAP
GRID_H = DAYS * (CELL + GAP) - GAP
CANVAS_W = PAD_X * 2 + 30 + GRID_W
CANVAS_H = PAD_Y * 2 + 20 + GRID_H + 24

OX = PAD_X + 30
OY = PAD_Y + 20

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]


def render(input_path: str = "data/contributions.json",
           output_path: str = "monthly-heatmap.svg") -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days_list = data.get("days", [])
    total = data.get("total", 0)
    day_map = {d["date"]: d for d in days_list}
    dates = sorted(day_map.keys())
    if not dates:
        print("No contribution data found in", input_path)
        sys.exit(1)

    # Last 28 days
    last_date = datetime.date.fromisoformat(dates[-1])
    start_date = last_date - datetime.timedelta(days=27)
    start = start_date - datetime.timedelta(days=start_date.weekday())

    grid = []
    for wi in range(WEEKS):
        col = []
        for di in range(DAYS):
            d = start + datetime.timedelta(weeks=wi, days=di)
            key = d.strftime("%Y-%m-%d")
            col.append(day_map.get(key))
        grid.append(col)

    parts = []
    def w(line):
        parts.append(line)

    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" width="{CANVAS_W}" height="{CANVAS_H}">')
    w('<defs>')
    w('  <linearGradient id="shimmer" x1="-100%" y1="0%" x2="0%" y2="0%">')
    w('    <stop offset="0%"   stop-color="rgba(255,255,255,0)"/>')
    w('    <stop offset="50%"  stop-color="rgba(255,255,255,0.35)"/>')
    w('    <stop offset="100%" stop-color="rgba(255,255,255,0)"/>')
    w('    <animate attributeName="x1" values="-100%;100%" dur="3s" repeatCount="indefinite"/>')
    w('    <animate attributeName="x2" values="0%;200%"    dur="3s" repeatCount="indefinite"/>')
    w('  </linearGradient>')
    w('</defs>')

    w(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="#0d1117"/>')
    w(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="11.5" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="1">')
    w('  <animate attributeName="stroke-opacity" values="0.07;0.15;0.07" dur="3s" repeatCount="indefinite"/>')
    w('</rect>')
    w(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="11.5" fill="none" stroke="url(#shimmer)" stroke-width="1" opacity="0.5"/>')

    # Title
    w(f'<text x="{CANVAS_W//2}" y="14" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="10" fill="#8b949e" text-anchor="middle">Last 28 days</text>')

    # Day labels
    w('<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="#8b949e" text-anchor="end">')
    for di, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = OY + di * (CELL + GAP) + CELL - 1
        w(f'  <text x="{OX - 4}" y="{y}">{label}</text>')
    w('</g>')

    # Cells
    for wi, col in enumerate(grid):
        for di, cell in enumerate(col):
            if cell is None:
                continue
            level = min(cell.get("level", 0), 5)
            color = PALETTE[level]
            cx = OX + wi * (CELL + GAP)
            cy = OY + di * (CELL + GAP)
            delay = round((wi * 0.05 + di * 0.02), 3)
            w(f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="2" fill="{color}" opacity="0">')
            w(f'<animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="{delay}s"/>')
            w('</rect>')

    # Legend
    legend_y = OY + GRID_H + 14
    w('<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="#8b949e">')
    w(f'  <text x="{OX}" y="{legend_y + CELL - 1}">Less</text>')
    for i, color in enumerate(PALETTE):
        sx = OX + 30 + i * (CELL + 2)
        w(f'  <rect x="{sx}" y="{legend_y}" width="{CELL}" height="{CELL}" rx="2" fill="{color}"/>')
    w(f'  <text x="{OX + 30 + 6*(CELL+2) + 4}" y="{legend_y + CELL - 1}">More</text>')
    w('</g>')

    # Stats
    month_total = sum(cell.get("count", 0) for col in grid for cell in col if cell)
    w(f'<text x="{PAD_X}" y="{CANVAS_H - 6}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="#8b949e">{month_total} contributions in the last 28 days</text>')

    w('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Monthly heatmap written -> {output_path}  ({CANVAS_W}x{CANVAS_H}px)")


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "monthly-heatmap.svg"
    render(inp, out)
