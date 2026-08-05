"""
render_stats_card.py
Generates self-contained GitHub stats + streak card SVGs from
data/contributions.json. No external service dependency — immune to
the rate-limiting / 500 errors that affect github-profile-summary-cards
and github-readme-stats.

Produces two files:
  - github-stats.svg      (profile stats: total, best day, streaks)
  - github-streak.svg     (streak-only card matching streak-stats style)

Usage:
    python scripts/render_stats_card.py
    python scripts/render_stats_card.py data/contributions.json github-stats.svg github-streak.svg
"""

import sys
import json
import datetime

# Tokyonight theme palette
BG = "#1a1b26"
FG = "#a9b1d6"
FG_DIM = "#565f89"
ACCENT_BLUE = "#7aa2f7"
ACCENT_PURPLE = "#bb9af7"
ACCENT_GREEN = "#9ece6a"
ACCENT_YELLOW = "#e0af68"
ACCENT_RED = "#f7768e"
ACCENT_CYAN = "#7dcfff"


def _compute_streaks(days):
    """Return (current_streak, longest_streak) from a list of day dicts."""
    sorted_days = sorted(days, key=lambda d: d["date"])
    if not sorted_days:
        return 0, 0

    longest = 0
    current_run = 0
    prev_date = None

    for d in sorted_days:
        count = d.get("count", 0)
        date_str = d["date"]
        try:
            date_obj = datetime.date.fromisoformat(date_str)
        except ValueError:
            continue

        if count > 0:
            if prev_date is not None and (date_obj - prev_date).days == 1:
                current_run += 1
            else:
                current_run = 1
            longest = max(longest, current_run)
        else:
            current_run = 0
        prev_date = date_obj

    # Current streak: count backwards from the last day with contributions.
    # Allow today to be 0 without breaking the streak (today may not have
    # contributions yet but yesterday's streak should persist).
    current = 0
    seen_active = False
    for d in reversed(sorted_days):
        if d.get("count", 0) > 0:
            current += 1
            seen_active = True
        else:
            if seen_active:
                break
            # skip leading zero(s) at the tail (today not yet counted)
            continue

    return current, longest


def _fmt_num(n: int) -> str:
    """Format number with k/M suffixes for large values."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}k"
    return str(n)


def render_stats_card(data, output_path: str) -> None:
    """Render the main stats card SVG."""
    total = data.get("total", 0)
    best_day = data.get("best_day", {})
    best_count = best_day.get("count", 0)
    best_date = best_day.get("date", "—")
    days = data.get("days", [])

    current_streak, longest_streak = _compute_streaks(days)
    active_days = sum(1 for d in days if d.get("count", 0) > 0)

    W, H = 820, 200
    parts = []
    def w(line):
        parts.append(line)

    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    w('<defs>')
    w('  <linearGradient id="statGrad" x1="0%" y1="0%" x2="100%" y2="100%">')
    w(f'    <stop offset="0%" stop-color="{ACCENT_BLUE}"/>')
    w(f'    <stop offset="100%" stop-color="{ACCENT_PURPLE}"/>')
    w('  </linearGradient>')
    w('  <linearGradient id="shimmer" x1="-100%" y1="0%" x2="0%" y2="0%">')
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
    w(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="11.5" fill="none" stroke="url(#shimmer)" stroke-width="1" opacity="0.5"/>')

    # Title
    w(f'<text x="24" y="32" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="14" font-weight="bold" fill="{FG}">Adnan-Umar GitHub Stats</text>')
    w(f'<text x="{W-24}" y="32" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="10" fill="{FG_DIM}" text-anchor="end">tokyonight</text>')

    # Divider
    w(f'<line x1="24" y1="44" x2="{W-24}" y2="44" stroke="rgba(255,255,255,0.07)" stroke-width="1"/>')

    # Stats grid — 2 rows x 3 columns
    stats = [
        ("Total Contributions", _fmt_num(total), ACCENT_BLUE),
        ("Active Days", str(active_days), ACCENT_GREEN),
        ("Best Day", f"{best_count} commits", ACCENT_YELLOW),
        ("Current Streak", f"{current_streak} days", ACCENT_CYAN),
        ("Longest Streak", f"{longest_streak} days", ACCENT_PURPLE),
        ("Best Day Date", best_date, ACCENT_RED),
    ]

    col_w = (W - 48) // 3
    row_h = 60
    start_y = 60

    for i, (label, value, color) in enumerate(stats):
        col = i % 3
        row = i // 3
        x = 24 + col * col_w
        y = start_y + row * row_h

        w(f'<text x="{x}" y="{y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="10" fill="{FG_DIM}">{label}</text>')
        w(f'<text x="{x}" y="{y + 20}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="18" font-weight="bold" fill="{color}">{value}</text>')
        w(f'<rect x="{x}" y="{y + 28}" width="0" height="2" rx="1" fill="{color}" opacity="0.6">')
        w(f'<animate attributeName="width" values="0;{col_w - 20};0" dur="3s" begin="{i*0.3}s" repeatCount="indefinite"/>')
        w('</rect>')

    w('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Stats card written -> {output_path}  ({W}x{H}px)")


def render_streak_card(data, output_path: str) -> None:
    """Render a streak-only card SVG matching the streak-stats visual style."""
    days = data.get("days", [])
    current_streak, longest_streak = _compute_streaks(days)
    total = data.get("total", 0)

    W, H = 820, 120
    parts = []
    def w(line):
        parts.append(line)

    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    w('<defs>')
    w('  <linearGradient id="flameGrad" x1="0%" y1="0%" x2="0%" y2="100%">')
    w(f'    <stop offset="0%" stop-color="{ACCENT_YELLOW}"/>')
    w(f'    <stop offset="100%" stop-color="{ACCENT_RED}"/>')
    w('  </linearGradient>')
    w('  <linearGradient id="streakShimmer" x1="-100%" y1="0%" x2="0%" y2="0%">')
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
    w(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="11.5" fill="none" stroke="url(#streakShimmer)" stroke-width="1" opacity="0.5"/>')

    # Three columns: Current Streak | Longest Streak | Total Contributions
    col_w = W // 3
    items = [
        ("Current Streak", f"{current_streak}", "days", "url(#flameGrad)"),
        ("Longest Streak", f"{longest_streak}", "days", ACCENT_PURPLE),
        ("Total Contributions", _fmt_num(total), "", ACCENT_BLUE),
    ]

    for i, (label, value, unit, color) in enumerate(items):
        cx = col_w * i + col_w // 2
        w(f'<text x="{cx}" y="38" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11" fill="{FG_DIM}" text-anchor="middle">{label}</text>')
        w(f'<text x="{cx}" y="68" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="26" font-weight="bold" fill="{color}" text-anchor="middle">{value}</text>')
        if unit:
            w(f'<text x="{cx + 48}" y="68" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11" fill="{FG_DIM}" text-anchor="start">{unit}</text>')
        if i < 2:
            div_x = col_w * (i + 1)
            w(f'<line x1="{div_x}" y1="28" x2="{div_x}" y2="{H-28}" stroke="rgba(255,255,255,0.07)" stroke-width="1"/>')

    w(f'<text x="{W//2}" y="{H-10}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9" fill="{FG_DIM}" text-anchor="middle">GitHub Streak — Adnan-Umar</text>')

    w('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Streak card written -> {output_path}  ({W}x{H}px)")


def render(input_path: str = "data/contributions.json",
           stats_output: str = "github-stats.svg",
           streak_output: str = "github-streak.svg") -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    render_stats_card(data, stats_output)
    render_streak_card(data, streak_output)


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    stats_out = sys.argv[2] if len(sys.argv) > 2 else "github-stats.svg"
    streak_out = sys.argv[3] if len(sys.argv) > 3 else "github-streak.svg"
    render(inp, stats_out, streak_out)