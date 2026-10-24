import os
import math
import html
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone
from collections import defaultdict

USERNAME = os.environ.get("GITHUB_USERNAME", "")
TOKEN = os.environ.get("GH_TOKEN", "")

if not USERNAME:
    raise ValueError("GITHUB_USERNAME পাওয়া যায়নি। GitHub Actions workflow চেক করুন।")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Saptak-GitHub-Profile",
}

if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def github_get(url):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8")


def get_json(url):
    import json
    return json.loads(github_get(url))


def polar(cx, cy, radius, angle_deg):
    angle_rad = math.radians(angle_deg)
    return (
        cx + radius * math.cos(angle_rad),
        cy + radius * math.sin(angle_rad),
    )


def describe_arc(cx, cy, radius, start_angle, end_angle):
    start_x, start_y = polar(cx, cy, radius, start_angle)
    end_x, end_y = polar(cx, cy, radius, end_angle)
    large_arc = 1 if end_angle - start_angle > 180 else 0

    return (
        f"M {start_x:.2f} {start_y:.2f} "
        f"A {radius} {radius} 0 {large_arc} 1 {end_x:.2f} {end_y:.2f}"
    )


def get_recent_commit_count():
    """গত 30 দিনের public commit-এর আনুমানিক সংখ্যা।"""
    since = (datetime.now(timezone.utc) - timedelta(days=30)).date().isoformat()

    query = urllib.parse.quote(
        f"author:{USERNAME} committer-date:>={since}"
    )

    url = f"https://api.github.com/search/commits?q={query}&per_page=1"

    try:
        data = get_json(url)
        return min(data.get("total_count", 0), 1000)
    except Exception as error:
        print(f"Commit count পাওয়া যায়নি: {error}")
        return 0


def get_language_data():
    """নিজের non-fork repo-গুলোর language bytes যোগ করে percentage বানায়।"""
    languages = defaultdict(int)
    page = 1

    while True:
        url = (
            "https://api.github.com/user/repos"
            f"?affiliation=owner&per_page=100&page={page}"
            "&sort=updated"
        )

        try:
            repos = get_json(url)
        except Exception as error:
            print(f"Repo list পাওয়া যায়নি: {error}")
            break

        if not repos:
            break

        for repo in repos:
            if repo.get("fork") or repo.get("archived"):
                continue

            lang_url = repo.get("languages_url")
            if not lang_url:
                continue

            try:
                repo_languages = get_json(lang_url)
                for language, bytes_count in repo_languages.items():
                    languages[language] += bytes_count
            except Exception as error:
                print(f"{repo.get('name')} language data পাওয়া যায়নি: {error}")

        page += 1

    return languages


def create_speedometer(commit_count):
    # 0–100 activity score; 100+ commits হলে max zone
    score = min(commit_count, 100)

    # Needle: left = 160°, right = 20°
    needle_angle = 160 - (score / 100) * 140

    # needle line end point
    end_x, end_y = polar(250, 225, 132, needle_angle)

    if score < 30:
        status = "CRUISING"
        status_color = "#00e676"
    elif score < 70:
        status = "BOOSTING"
        status_color = "#ffd600"
    else:
        status = "REDLINE"
        status_color = "#ff1744"

    ticks = []
    for value in range(0, 101, 10):
        angle = 160 - (value / 100) * 140
        outer_x, outer_y = polar(250, 225, 165, angle)
        inner_x, inner_y = polar(250, 225, 148, angle)
        text_x, text_y = polar(250, 225, 128, angle)

        ticks.append(
            f'<line x1="{outer_x:.1f}" y1="{outer_y:.1f}" '
            f'x2="{inner_x:.1f}" y2="{inner_y:.1f}" '
            f'stroke="#e8e8e8" stroke-width="3" />'
        )

        if value % 20 == 0:
            ticks.append(
                f'<text x="{text_x:.1f}" y="{text_y + 5:.1f}" '
                f'text-anchor="middle" fill="#ffffff" '
                f'font-size="13" font-family="monospace">{value}</text>'
            )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="330" viewBox="0 0 500 330">
  <defs>
    <radialGradient id="bg" cx="50%" cy="45%" r="70%">
      <stop offset="0%" stop-color="#292929"/>
      <stop offset="100%" stop-color="#070707"/>
    </radialGradient>

    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <linearGradient id="needle" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff5252"/>
      <stop offset="100%" stop-color="#b71c1c"/>
    </linearGradient>
  </defs>

  <rect width="500" height="330" rx="22" fill="#0a0a0a"/>
  <text x="250" y="38" text-anchor="middle" fill="#ff3d3d"
        font-size="23" font-family="monospace" font-weight="bold">
    COMMIT SPEEDOMETER
  </text>

  <circle cx="250" cy="225" r="185" fill="url(#bg)" stroke="#444" stroke-width="5"/>

  <!-- Speed zones -->
  <path d="{describe_arc(250, 225, 170, 160, 112)}"
        fill="none" stroke="#00e676" stroke-width="19" filter="url(#glow)"/>
  <path d="{describe_arc(250, 225, 170, 110, 65)}"
        fill="none" stroke="#ffd600" stroke-width="19" filter="url(#glow)"/>
  <path d="{describe_arc(250, 225, 170, 63, 20)}"
        fill="none" stroke="#ff1744" stroke-width="19" filter="url(#glow)"/>

  {''.join(ticks)}

  <!-- Needle -->
  <line x1="250" y1="225" x2="{end_x:.1f}" y2="{end_y:.1f}"
        stroke="url(#needle)" stroke-width="9" stroke-linecap="round"
        filter="url(#glow)"/>

  <circle cx="250" cy="225" r="20" fill="#111" stroke="#f5f5f5" stroke-width="4"/>
  <circle cx="250" cy="225" r="7" fill="#ff1744"/>

  <text x="250" y="275" text-anchor="middle" fill="{status_color}"
        font-size="22" font-family="monospace" font-weight="bold">
    {status}
  </text>

  <text x="250" y="302" text-anchor="middle" fill="#ffffff"
        font-size="16" font-family="monospace">
    {commit_count} COMMITS / LAST 30 DAYS
  </text>
</svg>'''


def create_jdm_rim(languages):
    total = sum(languages.values())

    if total == 0:
        top_languages = [("Python", 100)]
    else:
        sorted_languages = sorted(
            languages.items(),
            key=lambda item: item[1],
            reverse=True
        )

        top_languages = []
        used = 0

        for language, amount in sorted_languages[:4]:
            percent = round((amount / total) * 100, 1)
            top_languages.append((language, percent))
            used += percent

        other = round(max(0, 100 - used), 1)
        if other > 0.1:
            top_languages.append(("Other", other))

    colors = [
        "#3776AB",  # Python
        "#e34c26",  # HTML
        "#264de4",  # CSS
        "#f7df1e",  # JS
        "#b07219",  # Other
    ]

    arcs = []
    legend = []
    start = -90

    for index, (language, percent) in enumerate(top_languages):
        sweep = (percent / 100) * 360
        end = start + sweep - 2
        color = colors[index % len(colors)]

        if sweep > 2:
            arcs.append(
                f'<path d="{describe_arc(250, 250, 178, start, end)}" '
                f'fill="none" stroke="{color}" stroke-width="25" '
                f'stroke-linecap="round"/>'
            )

        legend_y = 440 + (index * 24)
        safe_language = html.escape(language)

        legend.append(
            f'<circle cx="105" cy="{legend_y - 5}" r="7" fill="{color}"/>'
            f'<text x="122" y="{legend_y}" fill="#f5f5f5" '
            f'font-size="16" font-family="monospace">'
            f'{safe_language}: {percent}%</text>'
        )

        start += sweep

    spokes = []
    for angle in range(0, 360, 45):
        x2, y2 = polar(250, 250, 125, angle)
        spokes.append(
            f'<line x1="250" y1="250" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#303030" stroke-width="15" stroke-linecap="round"/>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="590" viewBox="0 0 500 590">
  <defs>
    <radialGradient id="metal" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f4f4f4"/>
      <stop offset="30%" stop-color="#777"/>
      <stop offset="70%" stop-color="#202020"/>
      <stop offset="100%" stop-color="#080808"/>
    </radialGradient>

    <filter id="shadow">
      <feDropShadow dx="0" dy="5" stdDeviation="6" flood-opacity="0.65"/>
    </filter>
  </defs>

  <rect width="500" height="590" rx="22" fill="#090909"/>

  <text x="250" y="38" text-anchor="middle" fill="#00e5ff"
        font-size="22" font-family="monospace" font-weight="bold">
    JDM LANGUAGE RIM
  </text>

  <!-- Tire -->
  <circle cx="250" cy="250" r="205" fill="#111" stroke="#000" stroke-width="10" filter="url(#shadow)"/>

  <!-- Language-colored outer rim -->
  {''.join(arcs)}

  <!-- Metallic wheel -->
  <circle cx="250" cy="250" r="150" fill="url(#metal)" stroke="#555" stroke-width="5"/>

  <!-- JDM spokes -->
  {''.join(spokes)}

  <!-- Center hub -->
  <circle cx="250" cy="250" r="58" fill="#101010" stroke="#00e5ff" stroke-width="4"/>
  <circle cx="250" cy="250" r="35" fill="#252525" stroke="#777" stroke-width="3"/>

  <text x="250" y="246" text-anchor="middle" fill="#ffffff"
        font-size="16" font-family="monospace" font-weight="bold">CODE</text>
  <text x="250" y="267" text-anchor="middle" fill="#00e5ff"
        font-size="13" font-family="monospace">RPM</text>

  <text x="250" y="405" text-anchor="middle" fill="#bbbbbb"
        font-size="14" font-family="monospace">
    AUTO-GENERATED FROM YOUR REPOSITORIES
  </text>

  {''.join(legend)}
</svg>'''


def save_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def main():
    commits = get_recent_commit_count()
    languages = get_language_data()

    save_file("assets/speedometer.svg", create_speedometer(commits))
    save_file("assets/jdm-rim.svg", create_jdm_rim(languages))

    print("Profile SVG files updated successfully.")


if __name__ == "__main__":
    main()
