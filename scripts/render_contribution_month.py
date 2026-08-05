"""
render_contribution_month.py
Generates a self-contained "Last 30 Days" contribution detail SVG from
data/contributions.json. No external service dependency — immune to the
outages / rate-limiting of github-readme-activity-graph and
github-readme-stats.

Usage:
    python scripts/render_contribution_month.py
    python scripts/render_contribution_month.py data/contributions.json contribution-month.svg
"""

import datetime
import json
import sys

# Tokyonight palette (matches render_stats_card.py)
BG = "#1a1b26"
FG = "#a9b1d6"
FG_DIM = "#565f89"
ACCENT_BLUE = "#7aa2f7"
ACCENT_GREEN = "#9ece6a"
ACCENT_YELLOW = "#e0af68"
ACCENT_RED = "#f7768e"
BAR_BG = "rgba(255,255,255,0.06)"

W, H = 820, 260
PAD_LEFT, PAD_RIGHT = 34, 20
PAD_TOP, PAD_BOTTOM = 50, 30
CHART_W = W - PAD_LEFT - PAD_RIGHT
CHART_H = H - PAD_TOP - PAD_BOTTOM
DAYS = 30


def render(input_path: str = "data/contributions.json",
           output_path: str = "contribution-month.svg") -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    day_map = {d["date"]: d for d in data.get("days", [])}
    dates = sorted(day_map.keys())
    if not dates:
        print("No contribution data found in", input_path)
        sys.exit(1)

    last_date = datetime.date.fromisoformat(dates[-1])
    start_date = last_date - datetime.timedelta(days=DAYS - 1)

    labels = []
    values = []
    for i in range(DAYS):
        d = start_date + datetime.timedelta(days=i)
        key = d.strftime("%Y-%m-%d")
        cell = day_map.get(key)
        count = cell.get("count", 0) if cell else 0
        labels.append(d.strftime("%d %b"))
        values.append(count)

    total_month = sum(values)
    max_val = max(values) if values else 1
    active_days = sum(1 for v in values if v > 0)

    bar_w = 12
    gap = (CHART_W - DAYS * bar_w) / (DAYS - 1) if DAYS > 1 else 0

    parts = []
    def w(line):
        parts.append(line)

    # Gradient used for bars — color scales by value
    def bar_color(v):
        if v == 0:
            return BAR_BG
        ratio = v / max_val
        if ratio >= 0.75:
            return ACCENT_BLUE
        if ratio >= 0.5:
            return ACCENT_GREEN
        if ratio >= 0.25:
            return ACCENT_YELLOW
        return ACCENT_RED

    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    w('<defs>')
    w('  <linearGradient id="monthShimmer" x1="-100%" y1="0%" x2="0%" y2="0%">')
    w('    <stop offset="0%" stop-color="rgba(255,255,255,0)"/>')
    w('    <stop offset="50%" stop-color="rgba(255,255,255,0.08)"/>')
    w('    <stop offset="100%" stop-color="rgba(255,255,255,0)"/>')
    w('    <animate attributeName="x1" values="-100%;100%" dur="4s" repeatCount="indefinite"/>')
    w('    <animate attributeName="x2" values="0%;200%" dur="4s" repeatCount="indefinite"/>')
    w('  </linearGradient>')
    w('</defs>')

    # Background
    w(f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>')
    w(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="11.5" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="1"/>')
    w(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="11.5" fill="none" stroke="url(#monthShimmer)" stroke-width="1" opacity="0.5"/>')

    # Title
    w(f'<text x="24" y="30" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="14" font-weight="bold" fill="{FG}">Adnan-Umar Contributions — Last 30 Days</text>')
    w(f'<text x="{W-24}" y="30" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="10" fill="{FG_DIM}" text-anchor="end">tokyonight</text>')
    w(f'<text x="24" y="46" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="10" fill="{FG_DIM}">{start_date.strftime("%b %d, %Y")} → {last_date.strftime("%b %d, %Y")} · {total_month} contributions · {active_days} active days</text>')

    # Baseline
    base_y = PAD_TOP + CHART_H
    w(f'<line x1="{PAD_LEFT}" y1="{base_y}" x2="{W - PAD_RIGHT}" y2="{base_y}" stroke="rgba(255,255,255,0.10)" stroke-width="1"/>')

    # Y-axis gridlines + max label
    w(f'<text x="{PAD_LEFT - 6}" y="{PAD_TOP + 4}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{FG_DIM}" text-anchor="end">{max_val}</text>')
    w(f'<line x1="{PAD_LEFT}" y1="{PAD_TOP}" x2="{W - PAD_RIGHT}" y2="{PAD_TOP}" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>')

    # Bars (animated height)
    for i, (label, val) in enumerate(zip(labels, values)):
        x = PAD_LEFT + i * (bar_w + gap)
        bar_h = (val / max_val) * CHART_H if val > 0 else 2
        y = base_y - bar_h
        color = bar_color(val)
        w(f'<rect x="{x:.1f}" y="{base_y}" width="{bar_w}" height="0" rx="2" fill="{color}">')
        w(f'<animate attributeName="y" values="{base_y};{y:.1f};{y:.1f}" dur="0.6s" begin="{i*0.03}s" fill="freeze"/>')
        w(f'<animate attributeName="height" values="0;{bar_h:.1f};{bar_h:.1f}" dur="0.6s" begin="{i*0.03}s" fill="freeze"/>')
        w('</rect>')

    # Day labels — show every 5th day
    for i in range(0, DAYS, 5):
        x = PAD_LEFT + i * (bar_w + gap)
        w(f'<text x="{x + bar_w/2:.1f}" y="{base_y + 16}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{FG_DIM}" text-anchor="middle">{labels[i]}</text>')

    w('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Last 30 days contribution card written -> {output_path}  ({W}x{H}px)")


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "contribution-month.svg"
    render(inp, out)
