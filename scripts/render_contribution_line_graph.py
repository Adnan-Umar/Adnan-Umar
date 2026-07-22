"""
render_contribution_line_graph.py
Generates a line chart SVG showing contribution trends over time.

Usage:
    python scripts/render_contribution_line_graph.py
    python scripts/render_contribution_line_graph.py data/contributions.json contribution-line-graph.svg
"""

import sys
import json
import datetime

W, H = 800, 240
PAD_LEFT, PAD_RIGHT = 40, 20
PAD_TOP, PAD_BOTTOM = 30, 30
CHART_W = W - PAD_LEFT - PAD_RIGHT
CHART_H = H - PAD_TOP - PAD_BOTTOM

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]


def render(input_path: str = "data/contributions.json",
           output_path: str = "contribution-line-graph.svg") -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days_list = data.get("days", [])
    day_map = {d["date"]: d for d in days_list}
    dates = sorted(day_map.keys())
    if not dates:
        print("No contribution data found in", input_path)
        sys.exit(1)

    # Use last 84 days for a nice line chart
    last_date = datetime.date.fromisoformat(dates[-1])
    start_date = last_date - datetime.timedelta(days=83)

    labels = []
    values = []
    for i in range(84):
        d = start_date + datetime.timedelta(days=i)
        key = d.strftime("%Y-%m-%d")
        cell = day_map.get(key)
        count = cell.get("count", 0) if cell else 0
        labels.append(d.strftime("%b %d"))
        values.append(count)

    # Smooth data: aggregate by 3-day windows for cleaner line
    smoothed = []
    for i in range(0, len(values), 3):
        window = values[i:i+3]
        smoothed.append(sum(window))
    values = smoothed
    labels = labels[::3]
    n = len(values)
    max_val = max(values) if values else 1

    # Build points
    points = []
    for i, val in enumerate(values):
        x = PAD_LEFT + (i / max(1, n - 1)) * CHART_W
        y = PAD_TOP + CHART_H - (val / max_val) * CHART_H if max_val > 0 else PAD_TOP + CHART_H
        points.append((x, y))

    # Build path
    path_d = f"M {points[0][0]:.1f} {points[0][1]:.1f}"
    for i in range(1, len(points)):
        path_d += f" L {points[i][0]:.1f} {points[i][1]:.1f}"

    # Area path (for fill under line)
    area_d = path_d + f" L {points[-1][0]:.1f} {PAD_TOP + CHART_H:.1f} L {points[0][0]:.1f} {PAD_TOP + CHART_H:.1f} Z"

    parts = []
    def w(line):
        parts.append(line)

    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    w('<defs>')
    w('  <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">')
    w('    <stop offset="0%" stop-color="#7C3AED"/>')
    w('    <stop offset="50%" stop-color="#22D3EE"/>')
    w('    <stop offset="100%" stop-color="#10B981"/>')
    w('  </linearGradient>')
    w('  <linearGradient id="areaGrad" x1="0%" y1="0%" x2="0%" y2="100%">')
    w('    <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.2"/>')
    w('    <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>')
    w('  </linearGradient>')
    w('  <linearGradient id="shimmer" x1="-100%" y1="0%" x2="0%" y2="0%">')
    w('    <stop offset="0%" stop-color="rgba(255,255,255,0)"/>')
    w('    <stop offset="50%" stop-color="rgba(255,255,255,0.25)"/>')
    w('    <stop offset="100%" stop-color="rgba(255,255,255,0)"/>')
    w('    <animate attributeName="x1" values="-100%;100%" dur="3s" repeatCount="indefinite"/>')
    w('    <animate attributeName="x2" values="0%;200%" dur="3s" repeatCount="indefinite"/>')
    w('  </linearGradient>')
    w('  <filter id="glow">')
    w('    <feGaussianBlur stdDeviation="3" result="b"/>')
    w('    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>')
    w('  </filter>')
    w('</defs>')

    # Background
    w(f'<rect width="{W}" height="{H}" rx="12" fill="#0d1117"/>')
    w(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="11.5" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="1">')
    w('  <animate attributeName="stroke-opacity" values="0.07;0.15;0.07" dur="3s" repeatCount="indefinite"/>')
    w('</rect>')
    w(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="11.5" fill="none" stroke="url(#shimmer)" stroke-width="1" opacity="0.4"/>')

    # Title
    w(f'<text x="{W//2}" y="18" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11" fill="#8b949e" text-anchor="middle">Contribution Trend — Last 3 Months</text>')

    # Y-axis labels
    w('<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="#8b949e" text-anchor="end">')
    steps = 4
    for i in range(steps + 1):
        val = int(max_val * i / steps)
        y = PAD_TOP + CHART_H - (val / max_val) * CHART_H if max_val > 0 else PAD_TOP + CHART_H
        w(f'  <text x="{PAD_LEFT - 6}" y="{y + 3}">{val}</text>')
        if i > 0 and i < steps:
            w(f'  <line x1="{PAD_LEFT}" y1="{y}" x2="{W - PAD_RIGHT}" y2="{y}" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>')
    w('</g>')

    # Area fill
    w(f'<path d="{area_d}" fill="url(#areaGrad)" opacity="0">')
    w('<animate attributeName="opacity" values="0;1" dur="1s" fill="freeze"/>')
    w('</path>')

    # Line
    line_path = f'<path d="{path_d}" fill="none" stroke="url(#lineGrad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)" opacity="0">'
    w(line_path)
    w('<animate attributeName="opacity" values="0;1" dur="0.8s" fill="freeze"/>')
    w('</path>')

    # Dots
    for i, (x, y) in enumerate(points):
        delay = round(i * 0.015, 3)
        w(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#0d1117" stroke="url(#lineGrad)" stroke-width="2" opacity="0">')
        w(f'<animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="{delay}s"/>')
        w('</circle>')

    # X-axis labels (every 7th day)
    w('<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="#8b949e" text-anchor="middle">')
    for i in range(0, n, 7):
        x = PAD_LEFT + (i / max(1, n - 1)) * CHART_W
        w(f'  <text x="{x:.1f}" y="{PAD_TOP + CHART_H + 12}">{labels[i]}</text>')
    w('</g>')

    # Stats footer
    total = sum(values)
    peak = max(values)
    peak_idx = values.index(peak)
    peak_label = labels[peak_idx] if peak_idx < len(labels) else ""
    w(f'<text x="{PAD_LEFT}" y="{H - 8}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="#8b949e">{total} contributions | Peak: {peak} on {peak_label}</text>')

    w('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Line graph written -> {output_path}  ({W}x{H}px, {n} points)")


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "contribution-line-graph.svg"
    render(inp, out)
