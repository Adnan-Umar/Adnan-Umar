"""
fetch_contributions.py
Scrapes the public GitHub contribution calendar for a user without
requiring a GitHub token. Writes results to data/contributions.json.

Usage:
    python scripts/fetch_contributions.py Adnan-Umar
    python scripts/fetch_contributions.py Adnan-Umar data/contributions.json
"""

import sys
import json
import os
import re
import requests
from bs4 import BeautifulSoup


# GitHub occasionally changes its HTML structure. We try multiple selector
# strategies in order so that if one breaks the others can still work.
_SELECTORS = [
    # Current (2024-2025): td with data-date attribute
    'td[data-date]',
    # Older fallback: rect elements in SVG contribution graph
    'rect[data-date]',
]

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
}


def _parse_count(cell) -> int:
    """Extract contribution count from a cell element.
    Tries data-count attr, cell text, adjacent tooltip, then aria labels."""
    # data-count attribute (older GitHub)
    val = cell.get("data-count")
    if val is not None:
        try:
            return int(val)
        except ValueError:
            pass

    # Some themes embed the count in a <title> tooltip
    title_tag = cell.find("title")
    if title_tag and title_tag.string:
        m = re.search(r"(\d+)\s+contribution", title_tag.string, re.IGNORECASE)
        if m:
            return int(m.group(1))

    # Current GitHub (2026): count is in sibling <tool-tip> element
    tooltip_id = cell.get("id")
    if tooltip_id:
        tooltip = cell.find_parent("table").find("tool-tip", {"for": tooltip_id})
        if tooltip and tooltip.string:
            m = re.search(r"(\d+)\s+contribution", tooltip.string, re.IGNORECASE)
            if m:
                return int(m.group(1))

    # Fall back to the element's own text
    text = cell.get_text(strip=True)
    m = re.search(r"(\d+)\s+contribution", text, re.IGNORECASE)
    if m:
        return int(m.group(1))

    return 0


def _parse_level(element, count: int) -> int:
    """Extract contribution level (0-4) from element."""
    val = element.get("data-level")
    if val is not None:
        try:
            return min(int(val), 5)
        except ValueError:
            pass

    # Derive from count if level attribute is missing
    if count == 0:
        return 0
    if count < 2:
        return 1
    if count < 5:
        return 2
    if count < 10:
        return 3
    if count < 15:
        return 4
    return 5


def fetch_contributions(username: str,
                        output_path: str = "data/contributions.json") -> None:
    url = f"https://github.com/users/{username}/contributions"
    print(f"Fetching {url} ...", flush=True)

    try:
        resp = requests.get(url, headers=_HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"ERROR: request failed - {e}", file=sys.stderr)
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    days = []

    for selector in _SELECTORS:
        cells = soup.select(selector)
        if cells:
            for cell in cells:
                date = cell.get("data-date")
                if not date:
                    continue
                count = _parse_count(cell)
                level = _parse_level(cell, count)
                days.append({"date": date, "count": count, "level": level})
            break  # Stop once a working selector is found

    if not days:
        print("WARNING: no contribution cells found. "
              "GitHub may have changed its HTML structure.", file=sys.stderr)

    # Sort by date ascending
    days.sort(key=lambda d: d["date"])

    best_day = max(days, key=lambda d: d["count"]) if days else {"date": None, "count": 0}
    total    = sum(d["count"] for d in days)

    result = {
        "username":  username,
        "total":     total,
        "best_day":  best_day,
        "days":      days,
    }

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Saved {len(days)} days -> {output_path}  (total: {total:,} contributions)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_contributions.py <username> [output.json]")
        sys.exit(1)
    user = sys.argv[1]
    out  = sys.argv[2] if len(sys.argv) > 2 else "data/contributions.json"
    fetch_contributions(user, out)
