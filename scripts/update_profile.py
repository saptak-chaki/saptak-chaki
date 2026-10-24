import os
import math
import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from collections import defaultdict

USERNAME = os.environ.get("GITHUB_USERNAME", "")
TOKEN = os.environ.get("GH_TOKEN", "")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Saptak-GitHub-Profile",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def github_get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))


def graphql_query(query):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={**HEADERS, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))


def polar(cx, cy, r, angle_deg):
    a = math.radians(angle_deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def arc_path(cx, cy, r, start, end):
    sx, sy = polar(cx, cy, r, start)
    ex, ey = polar(cx, cy, r, end)
    large = 1 if abs(end - start) > 180 else 0
    return f"M {sx:.2f} {sy:.2f} A {r} {r} 0 {large} 1 {ex:.2f} {ey:.2f}"


def get_recent_commits():
    since = (datetime.now(timezone.utc) - timedelta(days=30)).date().isoformat()
    q = f"author:{USERNAME} committer-date:>={since}"
    url = f"https://api.github.com/search/commits?q={urllib.parse.quote(q)}&per_page=1"
    try:
        data = github_get(url)
        return min(data.get("total_count", 0), 300)
    except Exception as e:
        print("commit fetch error:", e)
        return 0


def get_repo_count():
    try:
        data = github_get(f"https://api.github.com/users/{USERNAME}")
        return data.get("public_repos", 0)
    except Exception as e:
        print("repo count error:", e)
        return 0


def get_streak():
    query = f'''
    {{
      user(login: "{USERNAME}") {{
        contributionsCollection {{
          contributionCalendar {{
            weeks {{
              contributionDays {{
                date
                contributionCount
              }}
            }}
          }}
        }}
      }}
    }}
    '''
    try:
        result = graphql_query(query)
        weeks = result["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        days = []
        for w in weeks:
            days.extend(w["contributionDays"])

        streak = 0
        skipped_today = False
        for day in reversed(days):
            if day["contributionCount"] > 0:
                streak += 1
            else:
                if not skipped_today:
                    skipped_today = True
                    continue
                break
        return streak
    except Exception as e:
        print("streak fetch error:", e)
        return 0


def get_language_data():
    languages = defaultdict(int)
    page = 1
    while page <= 10:
        url = (
            f"https://api.github.com/users/{USERNAME}/repos"
            f"?type=owner&per_page=100&page={page}"
        )
        try:
            repos = github_get(url)
        except Exception as e:
            print("repo list error:", e)
            break
        if not isinstance(repos, list) or not repos:
            break
        for repo in repos:
            if repo.get("fork") or repo.get("archived"):
                continue
            # profile repo-r generator script ke count korbe na
            if repo.get("name") == USERNAME:
                continue
            lang_url = repo.get("languages_url")
            if not lang_url:
                continue
            try:
                langs = github_get(lang_url)
                for lang, size in langs.items():
                    languages[lang] += size
            except Exception as e:
                print(f"{repo.get('name')} language error:", e)
        if len(repos) < 100:
            break
        page += 1
    print("RAW LANGUAGES:", dict(languages))
    return languages


def bucket_languages(languages):
    buckets = {"Python": 0, "HTML": 0, "CSS": 0, "Others": 0}
    css_names = {"CSS", "SCSS", "Sass", "Less"}
    python_names = {"Python", "Jupyter Notebook"}

    for lang, amount in languages.items():
        if lang in python_names:
            buckets["Python"] += amount
        elif lang == "HTML":
            buckets["HTML"] += amount
        elif lang in css_names:
            buckets["CSS"] += amount
        else:
            buckets["Others"] += amount

    total = sum(buckets.values())
    order = ("Python", "HTML", "CSS", "Others")
    if total == 0:
        return [(name, 0.0) for name in order]

    result = []
    used = 0.0
    for i, name in enumerate(order):
        if i == len(order) - 1:
            pct = round(max(0.0, 100.0 - used), 1)
        else:
            pct = round((buckets[name] / total) * 100, 1)
            used += pct
        result.append((name, pct))
    print("RIM BUCKETS:", result)
    return result


def create_gauge(title, value, max_value, unit_text, accent):
    score = min(value, max_value)
    percent = score / max_value if max_value else 0
    start_a, end_a = 160, 20
    target_a = start_a - percent * (start_a - end_a)
    delta = target_a - start_a

    def angle_at(frac):
        return start_a - frac * (start_a - end_a)

    cx, cy, r = 150, 115, 90
    ticks = []
    for i in range(6):
        frac = i / 5
        val = round(max_value * frac)
        a = angle_at(frac)
        tx, ty = polar(cx, cy, r - 18, a)
        ticks.append(
            f'<text x="{tx:.1f}" y="{ty+4:.1f}" text-anchor="middle" '
            f'fill="#ddd" font-size="10" font-family="monospace">{val}</text>'
        )

    if percent < 0.3:
        status, status_color = "CHILL", "#00e676"
    elif percent < 0.7:
        status, status_color = "ACTIVE", "#ffd600"
    else:
        status, status_color = "ON FIRE", "#ff1744"

    needle_tip_x, needle_tip_y = polar(cx, cy, r - 15, start_a)
    safe_title = title.replace(" ", "")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="230" viewBox="0 0 300 230">
  <defs>
    <filter id="glow-{safe_title}">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <radialGradient id="bg-{safe_title}" cx="50%" cy="40%" r="75%">
      <stop offset="0%" stop-color="#262626"/>
      <stop offset="100%" stop-color="#060606"/>
    </radialGradient>
  </defs>
  <rect width="300" height="230" rx="16" fill="#0a0a0a"/>
  <text x="150" y="24" text-anchor="middle" fill="{accent}" font-size="15" font-family="monospace" font-weight="bold">{title}</text>
  <circle cx="{cx}" cy="{cy}" r="{r+20}" fill="url(#bg-{safe_title})" stroke="#3a3a3a" stroke-width="3"/>
  <path d="{arc_path(cx, cy, r, start_a, angle_at(0.5))}" fill="none" stroke="#00e676" stroke-width="12" filter="url(#glow-{safe_title})">
    <animate attributeName="stroke-opacity" values="1;0.55;1" dur="2.2s" repeatCount="indefinite"/>
  </path>
  <path d="{arc_path(cx, cy, r, angle_at(0.5), angle_at(0.8))}" fill="none" stroke="#ffd600" stroke-width="12" filter="url(#glow-{safe_title})">
    <animate attributeName="stroke-opacity" values="1;0.55;1" dur="2.2s" begin="0.3s" repeatCount="indefinite"/>
  </path>
  <path d="{arc_path(cx, cy, r, angle_at(0.8), end_a)}" fill="none" stroke="#ff1744" stroke-width="12" filter="url(#glow-{safe_title})">
    <animate attributeName="stroke-opacity" values="1;0.55;1" dur="2.2s" begin="0.6s" repeatCount="indefinite"/>
  </path>
  {''.join(ticks)}
  <g filter="url(#glow-{safe_title})">
    <line x1="{cx}" y1="{cy}" x2="{needle_tip_x:.1f}" y2="{needle_tip_y:.1f}" stroke="#ff3b3b" stroke-width="5" stroke-linecap="round">
      <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="{delta:.1f} {cx} {cy}" dur="1.3s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
    </line>
  </g>
  <circle cx="{cx}" cy="{cy}" r="10" fill="#111" stroke="#fff" stroke-width="3"/>
  <circle cx="{cx}" cy="{cy}" r="4" fill="#ff1744"/>
  <text x="150" y="190" text-anchor="middle" fill="{status_color}" font-size="15" font-family="monospace" font-weight="bold">{status}</text>
  <text x="150" y="208" text-anchor="middle" fill="#ffffff" font-size="12" font-family="monospace">{value} {unit_text}</text>
</svg>'''


def create_rotating_rim(languages):
    items = bucket_languages(languages)
    colors = {
        "Python": "#3776AB",
        "HTML": "#E34C26",
        "CSS": "#00E5FF",
        "Others": "#C084FC",
    }

    cx, cy, r = 140, 145, 92
    arcs = []
    start = -90
    for name, pct in items:
        sweep = (pct / 100) * 360
        if sweep <= 0.4:
            continue
        gap = 2.5 if sweep > 10 else 0
        end = start + sweep - gap
        arcs.append(
            f'<path d="{arc_path(cx, cy, r, start, end)}" fill="none" '
            f'stroke="{colors[name]}" stroke-width="18" stroke-linecap="butt"/>'
        )
        start += sweep

    spokes = []
    for a in range(0, 360, 45):
        x2, y2 = polar(cx, cy, 52, a)
        spokes.append(
            f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#2b2b2b" stroke-width="9" stroke-linecap="round"/>'
        )

    legend = []
    bar_x = 300
    max_bar_width = 210
    for i, (name, pct) in enumerate(items):
        y = 70 + i * 48
        color = colors[name]
        bar_w = (pct / 100) * max_bar_width
        legend.append(f'''
        <circle cx="{bar_x}" cy="{y - 14}" r="7" fill="{color}"/>
        <text x="{bar_x + 16}" y="{y - 9}" fill="#f5f5f5" font-size="15" font-family="monospace" font-weight="bold">{name}</text>
        <rect x="{bar_x}" y="{y}" width="{max_bar_width}" height="12" rx="6" fill="#222"/>
        <rect x="{bar_x}" y="{y}" width="{bar_w:.1f}" height="12" rx="6" fill="{color}"/>
        <text x="{bar_x + max_bar_width + 10}" y="{y + 11}" fill="{color}" font-size="14" font-family="monospace" font-weight="bold">{pct}%</text>
        ''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="620" height="300" viewBox="0 0 620 300">
  <defs>
    <radialGradient id="metal" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#eaeaea"/>
      <stop offset="35%" stop-color="#8a8a8a"/>
      <stop offset="75%" stop-color="#1c1c1c"/>
      <stop offset="100%" stop-color="#050505"/>
    </radialGradient>
    <filter id="rimGlow">
      <feGaussianBlur stdDeviation="2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="620" height="300" rx="18" fill="#0a0a0a"/>
  <text x="310" y="28" text-anchor="middle" fill="#00e5ff" font-size="16" font-family="monospace" font-weight="bold">LANGUAGE RIM</text>
  <g filter="url(#rimGlow)">
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="4.5s" repeatCount="indefinite"/>
      <circle cx="{cx}" cy="{cy}" r="{r + 24}" fill="#111" stroke="#000" stroke-width="6"/>
      {''.join(arcs)}
      <circle cx="{cx}" cy="{cy}" r="{r - 24}" fill="url(#metal)" stroke="#444" stroke-width="3"/>
      {''.join(spokes)}
      <circle cx="{cx}" cy="{cy}" r="20" fill="#101010" stroke="#00e5ff" stroke-width="3"/>
    </g>
  </g>
  {''.join(legend)}
</svg>'''
def create_trophies(streak, repos, commits, language_count):
    specs = [
        ("STREAK", streak, "days", [(1, "BRONZE", "#cd7f32"), (7, "SILVER", "#e8e8e8"), (30, "GOLD", "#ffd54f"), (100, "LEGEND", "#00e5ff")]),
        ("REPOS", repos, "repos", [(1, "BRONZE", "#cd7f32"), (5, "SILVER", "#e8e8e8"), (15, "GOLD", "#ffd54f"), (30, "LEGEND", "#00e5ff")]),
        ("COMMITS", commits, "30 days", [(1, "BRONZE", "#cd7f32"), (10, "SILVER", "#e8e8e8"), (30, "GOLD", "#ffd54f"), (100, "LEGEND", "#00e5ff")]),
        ("STACK", language_count, "languages", [(1, "BRONZE", "#cd7f32"), (2, "SILVER", "#e8e8e8"), (3, "GOLD", "#ffd54f"), (5, "LEGEND", "#00e5ff")]),
    ]

    cards = []
    for i, (title, value, unit, levels) in enumerate(specs):
        rank, color = "LOCKED", "#666666"
        for minimum, label, rank_color in levels:
            if value >= minimum:
                rank, color = label, rank_color

        x = 20 + i * 190
        cards.append(f'''
        <rect x="{x}" y="24" width="170" height="146" rx="16" fill="#111111" stroke="{color}" stroke-width="2"/>
        <circle cx="{x + 85}" cy="68" r="24" fill="#0a0a0a" stroke="{color}" stroke-width="3">
          <animate attributeName="stroke-opacity" values="1;0.35;1" dur="1.8s" repeatCount="indefinite"/>
        </circle>
        <text x="{x + 85}" y="75" text-anchor="middle" fill="{color}" font-size="20" font-family="monospace" font-weight="bold">★</text>
        <text x="{x + 85}" y="112" text-anchor="middle" fill="#ffffff" font-size="13" font-family="monospace" font-weight="bold">{title}</text>
        <text x="{x + 85}" y="132" text-anchor="middle" fill="{color}" font-size="13" font-family="monospace" font-weight="bold">{rank}</text>
        <text x="{x + 85}" y="152" text-anchor="middle" fill="#aaaaaa" font-size="12" font-family="monospace">{value} {unit}</text>
        ''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="780" height="190" viewBox="0 0 780 190">
  <rect width="780" height="190" rx="18" fill="#0a0a0a"/>
  {''.join(cards)}
</svg>'''

def save_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    if not USERNAME:
        raise ValueError("GITHUB_USERNAME পাওয়া যায়নি।")

    streak = get_streak()
    repos = get_repo_count()
    commits = get_recent_commits()
    languages = get_language_data()
    language_count = sum(1 for amount in languages.values() if amount > 0)

    save_file("assets/speedometer_streak.svg", create_gauge("STREAK", streak, 30, "DAYS", "#ff6b6b"))
    save_file("assets/speedometer_repos.svg", create_gauge("REPOS", repos, 50, "REPOS", "#4dd0e1"))
    save_file("assets/speedometer_commits.svg", create_gauge("COMMITS", commits, 100, "COMMITS / 30D", "#ffd54f"))
    save_file("assets/jdm-rim.svg", create_rotating_rim(languages))
    save_file("assets/trophies.svg", create_trophies(streak, repos, commits, language_count))
    print("All profile SVGs generated successfully.")

if __name__ == "__main__":
    main()
