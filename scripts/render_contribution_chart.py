"""
render_contribution_chart.py
Generates a compact bar chart SVG showing contribution activity over time.

Usage:
    python scripts/render_contribution_chart.py
    python scripts/render_contribution_chart.py data/contributions.json contribution-chart.svg
"""

import sys
import json
import datetime

def render(input_path: str = "data/contributions.json",
           output_path: str = "contribution-chart.svg") -> None:
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

    labels = []
    values = []
    for i in range(28):
        d = start_date + datetime.timedelta(days=i)
        key = d.strftime("%Y-%m-%d")
        cell = day_map.get(key)
        count = cell.get("count", 0) if cell else 0
        labels.append(d.strftime("%b %d"))
        values.append(count)

    # Dimensions
    W, H = 800, 220
    pad_left, pad_right = 40, 20
    pad_top, pad_bottom = 30, 30
    chart_w = W - pad_left - pad_right
    chart_h = H - pad_top - pad_bottom
    n = len(values)
    bar_w = max(2, chart_w // n - 1)
    gap = (chart_w - n * bar_w) // (n - 1) if n > 1 else 0
    max_val = max(values) if values else 1

    parts = []
    def w(line):
        parts.append(line)

    # Header
    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    w('<defs>')
    w('  <linearGradient id="barGrad" x1="0%" y1="0%" x2="0%" y2="100%">')
    w('    <stop offset="0%" stop-color="#22D3EE"/>')
    w('    <stop offset="100%" stop-color="#7C3AED"/>')
    w('    <animate attributeName="x1" values="0%;100%;0%" dur="4s" repeatCount="indefinite"/>')
    w('    <animate attributeName="x2" values="100%;200%;100%" dur="4s" repeatCount="indefinite"/>')
    w('  </linearGradient>')
    w('  <linearGradient id="shimmer" x1="-100%" y1="0%" x2="0%" y2="0%">')
    w('    <stop offset="0%" stop-color="rgba(255,255,255,0)"/>')
    w('    <stop offset="50%" stop-color="rgba(255,255,255,0.25)"/>')
    w('    <stop offset="100%" stop-color="rgba(255,255,255,0)"/>')
    w('    <animate attributeName="x1" values="-100%;100%" dur="3s" repeatCount="indefinite"/>')
    w('    <animate attributeName="x2" values="0%;200%" dur="3s" repeatCount="indefinite"/>')
    w('  </linearGradient>')
    w('</defs>')

    # Background
    w(f'<rect width="{W}" height="{H}" rx="12" fill="#0d1117"/>')
    w(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="11.5" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="1">')
    w('  <animate attributeName="stroke-opacity" values="0.07;0.15;0.07" dur="3s" repeatCount="indefinite"/>')
    w('</rect>')
    w(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="11.5" fill="none" stroke="url(#shimmer)" stroke-width="1" opacity="0.4"/>')

    # Title
    w(f'<text x="{W//2}" y="18" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11" fill="#8b949e" text-anchor="middle">Daily Contributions — Last 28 Days</text>')

    # Y-axis labels
    w('<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="#8b949e" text-anchor="end">')
    steps = 4
    for i in range(steps + 1):
        val = int(max_val * i / steps)
        y = pad_top + chart_h - (val / max_val) * chart_h if max_val > 0 else pad_top + chart_h
        w(f'  <text x="{pad_left - 6}" y="{y + 3}">{val}</text>')
        if i > 0 and i < steps:
            w(f'  <line x1="{pad_left}" y1="{y}" x2="{W - pad_right}" y2="{y}" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>')
    w('</g>')

    # Bars
    for i, val in enumerate(values):
        x = pad_left + i * (bar_w + gap)
        bar_h = (val / max_val) * chart_h if max_val > 0 else 0
        y = pad_top + chart_h - bar_h
        delay = round(i * 0.02, 3)
        w(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h}" rx="2" fill="url(#barGrad)" opacity="0">')
        w(f'<animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="{delay}s"/>')
        if val > 0:
            w(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h}" rx="2" fill="url(#barGrad)" opacity="0.15">')
            w(f'<animate attributeName="height" values="0;{bar_h}" dur="0.5s" fill="freeze" begin="{delay}s"/>')
            w(f'<animate attributeName="y" values="{pad_top + chart_h};{y}" dur="0.5s" fill="freeze" begin="{delay}s"/>')
            w('<animate attributeName="opacity" values="0;1" dur="0.3s" fill="freeze" begin="' + str(delay) + 's"/>')
            w('</rect>')

    # X-axis labels (every 3rd day)
    w('<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="#8b949e" text-anchor="middle">')
    for i in range(0, n, 3):
        x = pad_left + i * (bar_w + gap) + bar_w / 2
        w(f'  <text x="{x}" y="{pad_top + chart_h + 12}">{labels[i]}</text>')
    w('</g>')

    # Stats footer
    monthly_total = sum(values)
    w(f'<text x="{pad_left}" y="{H - 8}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="#8b949e">{monthly_total} contributions in the last 28 days</text>')

    w('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Contribution chart written -> {output_path}  ({W}x{H}px, {n} days)")


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "contribution-chart.svg"
    render(inp, out)
