"""
render_top_languages.py
Generates a self-contained "Top Languages" card SVG from the GitHub API.
No external stats-service dependency — immune to the rate-limiting / 500
errors that affect github-readme-stats and github-profile-summary-cards.

Usage:
    python scripts/render_top_languages.py
    python scripts/render_top_languages.py Adnan-Umar top-languages.svg
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

# Tokyonight theme palette (matches render_stats_card.py)
BG = "#1a1b26"
FG = "#a9b1d6"
FG_DIM = "#565f89"
BAR_BG = "rgba(255,255,255,0.06)"
ACCENTS = [
    "#7aa2f7", "#bb9af7", "#9ece6a", "#e0af68",
    "#f7768e", "#7dcfff", "#73daca", "#f9c7c0",
]

_HEADERS = {
    "User-Agent": "github-profile-builder",
    "Accept": "application/vnd.github+json",
}


def _get_json(url: str, retries: int = 3) -> dict:
    """GET a JSON URL. Uses GITHUB_TOKEN/GH_TOKEN when available (5000 req/hr
    instead of the 60 req/hr anonymous limit shared per runner IP)."""
    headers = dict(_HEADERS)
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    last_err: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_err = exc
            if exc.code in (403, 429) and attempt < retries - 1:
                time.sleep(2 * (attempt + 1))  # back off on rate limiting
                continue
            raise
    raise last_err  # pragma: no cover


def fetch_language_bytes(username: str, max_repos: int = 200) -> dict:
    """Sum bytes of code per language across non-fork repos."""
    totals: dict = {}
    page = 1
    fetched = 0
    while fetched < max_repos:
        repos = _get_json(
            f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        )
        if not repos:
            break
        for repo in repos:
            if fetched >= max_repos:
                break
            fetched += 1
            if repo.get("fork"):
                continue
            langs = _get_json(
                f"https://api.github.com/repos/{username}/{repo['name']}/languages"
            )
            for lang, nbytes in langs.items():
                totals[lang] = totals.get(lang, 0) + nbytes
        if len(repos) < 100:
            break
        page += 1
    return totals


def _fmt_bytes(n: int) -> str:
    """Format byte counts with K/M suffixes."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(n)


def render_top_languages(username: str, output_path: str) -> None:
    totals = fetch_language_bytes(username)
    if not totals:
        print("No language data found.")
        return

    # Sort descending, keep top 8
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:8]
    total = sum(totals.values())

    W = 820
    row_h = 38
    top_pad = 52  # title + divider
    bottom_pad = 26
    H = top_pad + len(ranked) * row_h + bottom_pad

    parts = []
    def w(line):
        parts.append(line)

    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    w('<defs>')
    w('  <linearGradient id="langShimmer" x1="-100%" y1="0%" x2="0%" y2="0%">')
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
    w(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="11.5" fill="none" stroke="url(#langShimmer)" stroke-width="1" opacity="0.5"/>')

    # Title
    w(f'<text x="24" y="32" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="14" font-weight="bold" fill="{FG}">{username} Top Languages</text>')
    w(f'<text x="{W-24}" y="32" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="10" fill="{FG_DIM}" text-anchor="end">tokyonight</text>')
    w(f'<line x1="24" y1="44" x2="{W-24}" y2="44" stroke="rgba(255,255,255,0.07)" stroke-width="1"/>')

    bar_x = 24
    bar_x_end = W - 24
    bar_width_total = bar_x_end - bar_x
    bar_h = 6

    for i, (lang, nbytes) in enumerate(ranked):
        pct = nbytes / total * 100
        row_y = top_pad + 16 + i * row_h
        color = ACCENTS[i % len(ACCENTS)]

        # Label + percentage
        w(f'<text x="{bar_x}" y="{row_y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="12" fill="{FG}">{lang}</text>')
        w(f'<text x="{bar_x_end}" y="{row_y}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="11" fill="{FG_DIM}" text-anchor="end">{_fmt_bytes(nbytes)} · {pct:.1f}%</text>')

        # Track + animated bar
        w(f'<rect x="{bar_x}" y="{row_y + 8}" width="{bar_width_total}" height="{bar_h}" rx="3" fill="{BAR_BG}"/>')
        bar_w = int(bar_width_total * (nbytes / total))
        w(f'<rect x="{bar_x}" y="{row_y + 8}" width="0" height="{bar_h}" rx="3" fill="{color}">')
        w(f'<animate attributeName="width" values="0;{bar_w};{bar_w}" dur="1s" begin="{i*0.12}s" fill="freeze"/>')
        w('</rect>')

    w('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Top languages card written -> {output_path}  ({W}x{H}px)")


if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "Adnan-Umar"
    out = sys.argv[2] if len(sys.argv) > 2 else "top-languages.svg"
    try:
        render_top_languages(username, out)
    except Exception as exc:
        # Fail soft in CI: keep the previous SVG instead of breaking the
        # rest of the daily pipeline (month/chart/line-graph + auto-commit).
        print(
            f"WARN: could not refresh top languages ({exc}); keeping existing {out}",
            file=sys.stderr,
        )
        sys.exit(0)
