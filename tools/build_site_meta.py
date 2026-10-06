"""Regenerate sitemap.xml, feed.xml and llms.txt from tools/posts.json.

Run from the repo root after adding a post:  python3 tools/build_site_meta.py
"""
import datetime, email.utils, json, pathlib, subprocess
from xml.sax.saxutils import escape

BASE = "https://dream.ischool.illinois.edu/"
ROOT = pathlib.Path(__file__).resolve().parent.parent
posts = sorted(json.loads((ROOT / "tools/posts.json").read_text()), key=lambda p: p["date"], reverse=True)

STATIC = [("", "1.0"), ("overview.html", "0.9"), ("publications.html", "0.9"), ("preprints.html", "0.8"), ("blogs.html", "0.9"),
          ("secfid/", "0.8"), ("software.html", "0.7"), ("contact.html", "0.5")]


def lastmod(path):
    """Last git commit date of a file, falling back to today."""
    f = ROOT / (path + "index.html" if path.endswith("/") or path == "" else path)
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(f)], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return out or datetime.date.today().isoformat()


urls = [(BASE + p, lastmod(p), pr) for p, pr in STATIC] + [(BASE + p["path"], lastmod(p["path"]), "0.8") for p in posts]
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{m}</lastmod>\n    <priority>{pr}</priority>\n  </url>\n" for u, m, pr in urls)
    + "</urlset>\n")


def rfc822(d):
    return email.utils.format_datetime(datetime.datetime.fromisoformat(d).replace(hour=12, tzinfo=datetime.timezone.utc))


items = "".join(
    f"""  <item>
    <title>{escape(p['title'])}</title>
    <link>{BASE}{p['path']}</link>
    <guid>{BASE}{p['path']}</guid>
    <pubDate>{rfc822(p['date'])}</pubDate>
    <category>{escape(p.get('topic', ''))}</category>
    <description>{escape(p['description'])}</description>
  </item>
""" for p in posts)
(ROOT / "feed.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>DREAM Lab blog (UIUC)</title>
  <link>{BASE}blogs.html</link>
  <atom:link href="{BASE}feed.xml" rel="self" type="application/rss+xml"/>
  <description>Plain-language explainers of research from the DREAM Lab at the University of Illinois Urbana-Champaign.</description>
  <language>en</language>
  <lastBuildDate>{rfc822(posts[0]['date'])}</lastBuildDate>
{items}</channel>
</rss>
""")

post_lines = "\n".join(f"- [{p['title']}]({BASE}{p['path']}) ({p['date']}): {p['description']}" for p in posts)
(ROOT / "llms.txt").write_text(f"""# DREAM Lab (UIUC)

> DREAM (Developing Reliable and Efficient AI for Medicine) is a research lab at the School of Information Sciences, University of Illinois Urbana-Champaign, led by Assistant Professor Haohan Wang. The lab works on agentic AI and multi-agent LLM systems, the security of AI agents (e.g. prompt injection), LLM reasoning, trustworthy machine learning, and AI methods for computational biology.

## Lab
- [Research overview]({BASE}overview.html): research directions and projects
- [Publications]({BASE}publications.html): peer-reviewed publications, 2013 to present, with paper and code links
- [Preprints]({BASE}preprints.html): arXiv and bioRxiv preprints not yet peer reviewed
- [Software]({BASE}software.html): open-source tools
- [Contact]({BASE}contact.html): contact and information for prospective students
- [Haohan Wang]({BASE.replace('dream.', 'haohanwang.')}): PI homepage

## Project pages
- [SecFid]({BASE}secfid/): benchmark for security and fidelity of prompt injection defenses (ICML 2026 Spotlight)

## Blog posts
{post_lines}
""")
print(f"wrote sitemap.xml ({len(urls)} urls), feed.xml ({len(posts)} items), llms.txt")
