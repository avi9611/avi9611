#!/usr/bin/env python3
"""Draw a year of GitHub contributions as a 3D skyline, as two SVG files.

A port of the Contribution Skyline component from 21st.dev. A profile README
can only show images, so this keeps the look and the rising-bars animation and
drops the parts that need JavaScript: hover, drag to orbit, the 2D/3D toggle.

.github/workflows/skyline.yml runs it every day. To run it yourself:
    GITHUB_TOKEN=<token> python3 .github/scripts/skyline.py --user avi9611
    python3 .github/scripts/skyline.py --days days.json   # [{"date": "2026-01-31", "count": 4}, ...]
"""

import argparse
import json
import math
import os
import sys
import urllib.request
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

# Camera from the component: 45° around, 34° above the floor.
COS_YAW = SIN_YAW = math.sqrt(0.5)
SIN_EL = math.sin(math.radians(34))
COS_EL = math.cos(math.radians(34))

BAR = 0.9  # bar width in grid cells; the rest is the gap between bars
GAP = (1 - BAR) / 2
RISE_MS = 2000  # the whole wave, oldest week to newest
WAVE = 0.42  # share of RISE_MS a bar spends waiting for its turn
GROW_MS = round(RISE_MS * (1 - WAVE))

WIDTH = 880
PAD = 20  # inside the card
INSET = 16  # inside the chart box
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif'
EASE_OUT = "cubic-bezier(.33,1,.68,1)"
EASE_IN_OUT = "cubic-bezier(.65,0,.35,1)"

THEMES = {
    "light": {"bg": "#ffffff", "fg": "#1f2328", "border": "#d0d7de", "muted": "#59636e",
              "levels": ["#c6e48b", "#7bc96f", "#239a3b", "#196127"], "empty_mix": 0.075},
    "dark": {"bg": "#0d1117", "fg": "#e6edf3", "border": "#30363d", "muted": "#9198a1",
             "levels": ["#0e4429", "#006d32", "#26a641", "#39d353"], "empty_mix": 0.11},
}

# Sides grow upward from the floor; tops slide up with them. Stats fade in once the wave is mostly done.
ANIMATION_CSS = (
    f".grow{{transform-origin:0 0;animation:grow {GROW_MS}ms {EASE_OUT} var(--d) both}}"
    f".lift{{animation:lift {GROW_MS}ms {EASE_OUT} var(--d) both}}"
    "@keyframes grow{from{transform:scale(1,0)}}"
    "@keyframes lift{from{transform:translateY(var(--h))}}"
    f".drop{{animation:drop 600ms {EASE_IN_OUT} {round(RISE_MS * 0.55)}ms both}}"
    f".rise{{animation:rise 600ms {EASE_IN_OUT} {round(RISE_MS * 0.65)}ms both}}"
    "@keyframes drop{from{opacity:0;transform:translateY(-10px)}}"
    "@keyframes rise{from{opacity:0;transform:translateY(10px)}}"
    "@media (prefers-reduced-motion:reduce){.grow,.lift,.drop,.rise{animation:none}}"
)

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
  }
}
"""


@dataclass
class Cell:
    day: date
    count: int
    week: int
    row: int  # 0 is Sunday
    level: int = 0


@dataclass
class Streak:
    days: int = 0
    start: date | None = None
    end: date | None = None


def fetch_days(login, token):
    if not token:
        sys.exit("Set GITHUB_TOKEN, or pass --days FILE to draw from a saved file.")
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    headers = {"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "skyline"}
    request = urllib.request.Request("https://api.github.com/graphql", data=body, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        sys.exit(f"GitHub API error: {payload['errors']}")
    user = payload["data"]["user"]
    if user is None:
        sys.exit(f"No GitHub user called {login!r}")
    weeks = user["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [{"date": d["date"], "count": d["contributionCount"]} for week in weeks for d in week["contributionDays"]]


def build_grid(days, end):
    """Weeks left to right, Sunday on top, ending on `end`. Same layout as GitHub's own calendar."""
    counts = {}
    for item in days:
        when = date.fromisoformat(item["date"])
        counts[when] = counts.get(when, 0) + int(item["count"])
    first = end - timedelta(days=364)
    first -= timedelta(days=(first.weekday() + 1) % 7)  # weekday() counts from Monday
    total_days = (end - first).days + 1
    cells = []
    for i in range(total_days):
        when = first + timedelta(days=i)
        cells.append(Cell(when, counts.get(when, 0), i // 7, i % 7))
    # The 95th percentile, not the max, so one freak day can't push every other day down to level 1.
    nonzero = sorted(c.count for c in cells if c.count > 0)
    busy = nonzero[int(0.95 * (len(nonzero) - 1))] if nonzero else 0
    for cell in cells:
        cell.level = level_of(cell.count, busy)
    return cells


def level_of(count, busy):
    if count <= 0:
        return 0
    if busy <= 0:
        return 4
    return 1 + min(3, math.floor(count / busy * 4))


def bar_height(count, peak):
    """In grid cells. Empty days are thin slabs; the busiest day is about 7.6 cells tall."""
    if count <= 0 or peak <= 0:
        return 0.2
    return 0.4 + (count / peak) ** 0.85 * 7.2


def longest_streak(cells):
    best = Streak()
    run = 0
    start = None
    for cell in cells:
        if cell.count == 0:
            run = 0
            continue
        if run == 0:
            start = cell.day
        run += 1
        if run > best.days:
            best = Streak(run, start, cell.day)
    return best


def month_labels(cells, weeks):
    """A label on each week that starts a new month. A cramped first label is dropped."""
    labels = []
    previous = None
    for week in range(weeks):
        first_day = cells[week * 7].day
        if first_day.month != previous:
            labels.append((week, MONTHS[first_day.month - 1]))
        previous = first_day.month
    if len(labels) > 1 and labels[1][0] - labels[0][0] < 3:
        labels.pop(0)
    return labels


def project(x, y, z):
    """Grid (x = week, y = weekday, z = up) to screen, before scaling."""
    return x * COS_YAW - y * SIN_YAW, (x * SIN_YAW + y * COS_YAW) * SIN_EL - z * COS_EL


def fit(cells, heights, weeks, stage_w):
    """Scale and offset that fit the tallest skyline in the stage. Returns (scale, ox, oy, stage_h)."""
    points = []
    for cell, height in zip(cells, heights):
        x0, y0 = cell.week + GAP, cell.row + GAP
        x1, y1 = x0 + BAR, y0 + BAR
        points += [project(x0, y0, height), project(x1, y0, height), project(x0, y1, height),
                   project(x1, y1, 0), project(x0, y1, 0), project(x1, y0, 0)]
    points += [project(0, 8.5, 0), project(weeks, 8.5, 0)]  # room for the month labels
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    span_x = max(xs) - min(xs)
    span_y = max(ys) - min(ys)
    natural = span_y / span_x * (stage_w - 40) + 40
    stage_h = max(min(natural, stage_w * 0.72, 620), min(natural, 240))
    inner_w = stage_w - 40
    inner_h = stage_h - 40
    scale = min(inner_w / span_x, inner_h / span_y)
    ox = 20 + (inner_w - span_x * scale) / 2 - min(xs) * scale
    oy = 20 + (inner_h - span_y * scale) / 2 - min(ys) * scale
    return scale, ox, oy, stage_h


def render_bars(cells, heights, weeks, scale, ox, oy):
    # Every bar has the same face shapes. Only its floor position and height change.
    left = (-BAR * COS_YAW * scale, -BAR * SIN_YAW * SIN_EL * scale)
    right = (BAR * SIN_YAW * scale, -BAR * COS_YAW * SIN_EL * scale)
    up = -COS_EL * scale
    left_face = f"matrix({left[0]:.3f} {left[1]:.3f} 0 {up:.3f} 0 0)"
    right_face = f"matrix({right[0]:.3f} {right[1]:.3f} 0 {up:.3f} 0 0)"
    top_corners = [(0, 0), left, (left[0] + right[0], left[1] + right[1]), right]
    # Painter's order: back to front, so nearer bars cover farther ones.
    order = sorted(range(len(cells)), key=lambda i: (cells[i].week + 0.5) * SIN_YAW + (cells[i].row + 0.5) * COS_YAW)
    parts = []
    for i in order:
        cell = cells[i]
        height = heights[i]
        floor_x, floor_y = project(cell.week + GAP + BAR, cell.row + GAP + BAR, 0)  # nearest corner
        lift = height * COS_EL * scale
        top = " ".join(f"{x:.1f},{y - lift:.1f}" for x, y in top_corners)
        delay = round(((cell.week / max(1, weeks - 1)) * 0.36 + (cell.row / 6) * 0.06) * RISE_MS)
        parts.append(
            f'<g transform="translate({ox + floor_x * scale:.1f} {oy + floor_y * scale:.1f})" style="--d:{delay}ms;--h:{lift:.1f}px">'
            f'<g transform="{left_face}"><rect class="grow l{cell.level}" width="1" height="{height:.2f}"/></g>'
            f'<g transform="{right_face}"><rect class="grow r{cell.level}" width="1" height="{height:.2f}"/></g>'
            f'<polygon class="lift k{cell.level}" points="{top}"/></g>'
        )
    return parts


def render_months(cells, weeks, scale, ox, oy, stage_w):
    parts = []
    right_edge = -math.inf
    for week, label in month_labels(cells, weeks):
        sx, sy = project(week + 0.5, 7.3, 0)
        x = ox + sx * scale
        width = len(label) * 6  # rough width at 10px; only used to skip overlaps
        if x < right_edge or x + width > stage_w:
            continue
        parts.append(f'<text x="{x:.1f}" y="{oy + sy * scale + 11:.1f}" class="muted" font-size="10">{label}</text>')
        right_edge = x + width + 10
    return parts


def stat(x, y, anchor, label, value, unit, sub, accent, size):
    value_y = y + 16 + size * 0.82
    return (
        f'<text x="{x}" y="{y + 13}" text-anchor="{anchor}" class="muted" font-size="13">{label}</text>'
        f'<text x="{x}" y="{value_y:.0f}" text-anchor="{anchor}"><tspan class="num" fill="{accent}" font-size="{size}">{value}</tspan>'
        f'<tspan dx="6" font-size="15">{unit}</tspan></text>'
        f'<text x="{x}" y="{value_y + 19:.0f}" text-anchor="{anchor}" class="muted" font-size="13">{sub}</text>'
    )


def short_date(day, with_year=False):
    text = f"{MONTHS[day.month - 1]} {day.day}"
    return f"{text}, {day.year}" if with_year else text


def date_range(start, end, with_year=False):
    if start is None or end is None:
        return "—"
    return f"{short_date(start, with_year)} — {short_date(end, with_year)}"


def plural(n, word):
    return word if n == 1 else word + "s"


def render_stats(cells, stage_w, stage_h, accent):
    total = sum(c.count for c in cells)
    busiest = max(cells, key=lambda c: c.count)
    longest = longest_streak(cells)
    # The component shows the current streak here. On a profile that often reads "0 days" after a
    # weekend, so this shows how much of the year had any activity instead.
    active = sum(1 for c in cells if c.count > 0)
    size = round(max(30, min(56, stage_w * 0.058)))
    block = 16 + size * 0.82 + 23  # label, number, sub line
    right = stage_w - 4
    bottom = stage_h - 4 - (2 * block + 20)
    return (
        f'<g class="drop">'
        + stat(right, 4, "end", "1 year total", f"{total:,}", plural(total, "contribution"),
               date_range(cells[0].day, cells[-1].day, with_year=True), accent, size)
        + stat(right, 4 + block + 20, "end", "Busiest day", f"{busiest.count:,}", plural(busiest.count, "contribution"),
               short_date(busiest.day) if busiest.count else "—", accent, size)
        + '</g><g class="rise">'
        + stat(4, bottom, "start", "Longest streak", f"{longest.days:,}", plural(longest.days, "day"),
               date_range(longest.start, longest.end), accent, size)
        + stat(4, bottom + block + 20, "start", "Active days", f"{active:,}", plural(active, "day"),
               f"{round(active / len(cells) * 100)}% of the year", accent, size)
        + "</g>"
    )


def hex_to_rgb(color):
    return [int(color[i:i + 2], 16) for i in (1, 3, 5)]


def rgb_to_hex(rgb):
    return "#" + "".join(f"{round(max(0, min(255, c))):02x}" for c in rgb)


def mix(a, b, t):
    return rgb_to_hex([x + (y - x) * t for x, y in zip(hex_to_rgb(a), hex_to_rgb(b))])


def shade(color, k):
    return rgb_to_hex([c * k for c in hex_to_rgb(color)])


def style_block(theme, swatches):
    rules = [f"text{{font-family:{FONT};fill:{theme['fg']}}}", f".muted{{fill:{theme['muted']}}}",
             ".num{font-weight:600;font-variant-numeric:tabular-nums;letter-spacing:-.02em}"]
    # Left sides a little darker than the top, right sides darker still, as if lit from the upper left.
    for level, color in enumerate(swatches):
        rules.append(f".k{level}{{fill:{color}}}.l{level}{{fill:{shade(color, 0.84)}}}.r{level}{{fill:{shade(color, 0.68)}}}")
    return "".join(rules) + ANIMATION_CSS


def render_legend(swatches, right, y):
    first_x = right - 36 - 5 * 11 - 4 * 6  # "More" is about 28px wide at 12px
    parts = [f'<text x="{first_x - 8}" y="{y}" text-anchor="end" class="muted" font-size="12">Less</text>']
    for i, color in enumerate(swatches):
        parts.append(f'<rect x="{first_x + i * 17}" y="{y - 10}" width="11" height="11" rx="2" fill="{color}"/>')
    parts.append(f'<text x="{right}" y="{y}" text-anchor="end" class="muted" font-size="12">More</text>')
    return "".join(parts)


def render(cells, theme):
    weeks = cells[-1].week + 1
    peak = max(c.count for c in cells)
    total = sum(c.count for c in cells)
    heights = [bar_height(c.count, peak) for c in cells]
    swatches = [mix(theme["bg"], theme["fg"], theme["empty_mix"])] + theme["levels"]
    stage_w = WIDTH - 2 * PAD - 2 * INSET
    scale, ox, oy, stage_h = fit(cells, heights, weeks, stage_w)
    box_top = PAD + 32
    stage_x = PAD + INSET
    stage_y = box_top + INSET
    footer_y = stage_y + stage_h + 26
    box_bottom = footer_y + 14
    height = round(box_bottom + PAD)
    title = f"{total:,} {plural(total, 'contribution')} in the last year"
    return "".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="t">',
        f'<title id="t">{title}, drawn as a 3D skyline</title><style>{style_block(theme, swatches)}</style>',
        f'<rect x=".5" y=".5" width="{WIDTH - 1}" height="{height - 1}" rx="12" fill="{theme["bg"]}" stroke="{theme["border"]}"/>',
        f'<text x="{PAD}" y="{PAD + 15}" font-size="15"><tspan class="num">{total:,}</tspan> {plural(total, "contribution")} in the last year</text>',
        f'<rect x="{PAD + .5}" y="{box_top + .5}" width="{WIDTH - 2 * PAD - 1}" height="{box_bottom - box_top:.0f}" rx="8" fill="none" stroke="{theme["border"]}"/>',
        f'<g transform="translate({stage_x} {stage_y})">',
        *render_bars(cells, heights, weeks, scale, ox, oy),
        *render_months(cells, weeks, scale, ox, oy, stage_w),
        render_stats(cells, stage_w, stage_h, theme["levels"][3]),
        "</g>",
        f'<text x="{stage_x}" y="{footer_y:.0f}" class="muted" font-size="12">Updated {short_date(cells[-1].day, with_year=True)}</text>',
        render_legend(swatches, WIDTH - PAD - INSET, round(footer_y)),
        "</svg>",
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--user", help="GitHub username to fetch")
    parser.add_argument("--days", type=Path, help="draw from a saved JSON file instead of the API")
    parser.add_argument("--out", type=Path, default=Path("dist"), help="folder for the SVG files")
    args = parser.parse_args()
    if args.days is None and args.user is None:
        parser.error("pass --user to fetch from GitHub, or --days to draw from a file")

    days = json.loads(args.days.read_text()) if args.days else fetch_days(args.user, os.environ.get("GITHUB_TOKEN"))
    if not days:
        sys.exit("No contribution days came back. Refusing to draw an empty skyline.")
    last_day = max(date.fromisoformat(d["date"]) for d in days)
    cells = build_grid(days, last_day)

    args.out.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        path = args.out / f"skyline-{name}.svg"
        path.write_text(render(cells, theme), encoding="utf-8")
        print(f"Wrote {path}")
    # The interactive version at avi9611.github.io/activity reads this file in the browser.
    (args.out / "days.json").write_text(json.dumps(days, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {args.out / 'days.json'}")


if __name__ == "__main__":
    main()
