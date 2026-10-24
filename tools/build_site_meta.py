"""Regenerate sitemap.xml, feed.xml and llms.txt from tools/posts.json, and the JSON-LD blocks
(between the jsonld:auto markers) in blogs.html, publications.html and preprints.html.

Run from the repo root after adding a post or editing the publication lists:  python3 tools/build_site_meta.py
"""
import datetime, email.utils, html, json, pathlib, re, subprocess
from xml.sax.saxutils import escape

BASE = "https://dream.ischool.illinois.edu/"
ROOT = pathlib.Path(__file__).resolve().parent.parent
posts = sorted(json.loads((ROOT / "tools/posts.json").read_text()), key=lambda p: p["date"], reverse=True)

STATIC = [("", "1.0"), ("overview.html", "0.9"), ("publications.html", "0.9"), ("preprints.html", "0.8"), ("blogs.html", "0.9"), ("people.html", "0.8"), ("people/yurui-li/", "0.6"), ("people/haibo-jin/", "0.6"), ("people/peng-kuang/", "0.6"), ("people/xiaopeng-yuan/", "0.6"),
          ("secfid/", "0.8"), ("software.html", "0.7"), ("contact.html", "0.5")]


def lastmod(path):
    """Last git commit date of a file, falling back to today."""
    f = ROOT / (path + "index.html" if path.endswith("/") or path == "" else path)
    if subprocess.run(["git", "status", "--porcelain", "--", str(f)], cwd=ROOT, capture_output=True, text=True).stdout.strip():
        return datetime.date.today().isoformat()
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

> DREAM Lab (Developing Reliable and Efficient AI for Medicine) is Haohan Wang's research lab at the School of Information Sciences, University of Illinois Urbana-Champaign. The lab builds reliable agentic AI for scientific discovery, studies the security of AI agents, and develops AI methods for computational biology.

Research areas:
- Agentic AI for scientific discovery: LLM agents and multi-agent systems that analyze biological data and do scientific reasoning, e.g. GenoTEX (benchmark for gene expression analysis agents), GenoMAS (multi-agent gene expression analysis, ACL Findings 2026), SCTA (target gene discovery from single-cell RNA-seq), and agentic transcriptomic and proteomic discovery.
- Multi-agent LLM systems and their reliability: agent primitives, agent communication, test-time scaling, self-evolving agents.
- Security of AI agents: prompt injection (SecFid, ICML 2026 Spotlight), jailbreaks, guardrails, and visibility in LLM-based search (CORE).
- AI for computational biology: genetics of complex traits such as Alzheimer's disease and cancer.

Haohan Wang is an Assistant Professor in the School of Information Sciences, affiliated with the Beckman Institute and the Siebel School of Computing and Data Science. He gives invited talks, seminars, and tutorials on agentic AI for scientific discovery and on LLM security; his homepage lists past talks and contact details.

## Lab
- [Research overview]({BASE}overview.html): research directions and projects
- [Publications]({BASE}publications.html): peer-reviewed publications, 2013 to present, with paper and code links
- [Preprints]({BASE}preprints.html): arXiv and bioRxiv preprints not yet peer reviewed
- [Software]({BASE}software.html): AI agent tools for data analysis and genomics, and other software
- [People]({BASE}people.html): PI Haohan Wang and lab members
- [Contact]({BASE}contact.html): contact and information for prospective students
- [Haohan Wang]({BASE.replace('dream.', 'haohanwang.')}): PI homepage

## Project pages
- [SecFid]({BASE}secfid/): benchmark for security and fidelity of prompt injection defenses (ICML 2026 Spotlight)

## Blog posts
{post_lines}
""")

# JSON-LD for list pages. Each page has a marker pair in <head>; everything between them is replaced.
PI = {"@id": "https://haohanwang.ischool.illinois.edu/#person"}
MARK = re.compile(r"(    <!-- jsonld:auto[^>]*-->\n).*?(    <!-- /jsonld:auto -->)", re.S)


def inject(page, graph):
    f = ROOT / page
    s = f.read_text()
    block = ('    <script type="application/ld+json">'
             + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
             + "</script>\n")
    s, n = MARK.subn(lambda m: m.group(1) + block + m.group(2), s)
    if n != 1:
        raise SystemExit(f"{page}: expected one jsonld:auto marker pair, found {n}")
    f.write_text(s)


def text(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def parse_authors(raw):
    """Author lines in the formats the lists use ('Kuang P, Jin H, et al., Wang H', 'Wang H., Lopez O, and Xing E. P.',
    'Wang X, Wang, H., Yang D.') -> ['Kuang P', 'Xing EP', ...]; [] if any name can't be read, so the caller falls back."""
    raw = re.sub(r"\s*,?\s*\band\b\s*|\s*&\s*", ", ", raw.replace("*", ""))
    names = []
    for t in (t.strip(" .") for t in raw.split(",")):
        if not t or t == "et al":
            continue
        if re.fullmatch(r"[A-Z](?:\.?\s?[A-Z])*", t) and names and " " not in names[-1]:
            names[-1] += " " + t  # "Wang", "H" -> "Wang H"
        else:
            names.append(t)
    out = []
    for n in names:
        parts = n.split()
        i = len(parts)
        while i > 1 and re.fullmatch(r"[A-Z][A-Z\-.]*", parts[i - 1]):
            i -= 1
        if i == len(parts) and not (len(parts) > 1 and all(re.fullmatch(r"[A-Z][a-z'\-]+", x) for x in parts)):
            return []  # neither "Surname Initials" nor a plain full name like "Songwei Ge"
        out.append((" ".join(parts[:i]).rstrip(".") + " " + "".join(x.replace(".", "") for x in parts[i:])).strip())
    return out


def papers(page):
    """Entries are <div id="tag..."><li>authors <span bold><a href=url>title</a></span>, venue</li></div> in year sections."""
    out = []
    for sec_id, body in re.findall(r'<section id="([^"]+)">(.*?)</section>', (ROOT / page).read_text(), re.S):
        for li in re.findall(r'<div id="tag[^"]*">\s*<li[^>]*>(.*?)</li>', body, re.S):
            m = re.search(r'<span style="font-weight: bold;">\s*(?:<a\s+href="([^"]+)"[^>]*>)?(.*?)(?:</a>\s*)?</span>', li, re.S)
            if not m:
                continue
            url, title = m.group(1), text(m.group(2)).rstrip(".")
            item = {"@type": "ScholarlyArticle", "name": title}
            if url:
                item["url"] = url
            names = parse_authors(text(li[:m.start()]))
            if names:
                item["author"] = [dict(PI, name="Haohan Wang") if n == "Wang H" else {"@type": "Person", "name": n} for n in names]
            else:
                item["author"] = [dict(PI, name="Haohan Wang")]
            rest = li[m.end():]
            venue = re.search(r"<i>(.*?)</i>", rest, re.S)
            low = rest.lower()
            if venue:
                item["isPartOf"] = {"@type": "CreativeWork", "name": text(venue.group(1)).strip(" .,")[:150]}
            elif "biorxiv" in low or "biorxiv" in (url or ""):
                item["isPartOf"] = {"@type": "CreativeWork", "name": "bioRxiv"}
            elif "arxiv" in low or "arxiv" in (url or ""):
                item["isPartOf"] = {"@type": "CreativeWork", "name": "arXiv"}
            year = sec_id if re.fullmatch(r"(19|20)\d\d", sec_id) else (re.findall(r"\b(?:19|20)\d\d\b", text(li)) or [None])[-1]
            if year:
                item["datePublished"] = year
            out.append(item)
    return out


for page, name in [("publications.html", "Publications | Haohan Wang and the DREAM Lab, UIUC"),
                   ("preprints.html", "Preprints | Haohan Wang and the DREAM Lab, UIUC")]:
    items = papers(page)
    inject(page, [{"@type": "CollectionPage", "@id": BASE + page + "#page", "url": BASE + page, "name": name,
                   "isPartOf": {"@id": BASE + "#site"}, "about": [PI, {"@id": BASE + "#lab"}],
                   "mainEntity": {"@type": "ItemList", "numberOfItems": len(items),
                                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": it} for i, it in enumerate(items)]}}])
    print(f"{page}: {len(items)} papers in JSON-LD")

inject("blogs.html", [{"@type": "Blog", "@id": BASE + "blogs.html#blog", "url": BASE + "blogs.html", "name": "DREAM Lab blog (UIUC)",
                       "inLanguage": "en", "isPartOf": {"@id": BASE + "#site"}, "publisher": {"@id": BASE + "#lab"},
                       "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": BASE + p["path"], "datePublished": p["date"],
                                     "description": p["description"]} for p in posts]}])

print(f"wrote sitemap.xml ({len(urls)} urls), feed.xml ({len(posts)} items), llms.txt, JSON-LD in blogs/publications/preprints")
