"""Tell Bing and the other IndexNow engines (Yandex, Seznam, Naver) about new or changed pages.
ChatGPT search and Copilot draw on Bing's index. Google does not use IndexNow; keep using Search Console for it.

Run after `git push`, once GitHub Pages has deployed (the key file must be live):
    python3 tools/indexnow.py                # pages whose sitemap lastmod is within the last 3 days
    python3 tools/indexnow.py --days 30
    python3 tools/indexnow.py URL [URL ...]  # specific pages
"""
import datetime, json, pathlib, re, sys, urllib.request

BASE = "https://dream.ischool.illinois.edu/"
ROOT = pathlib.Path(__file__).resolve().parent.parent
key = next(p.stem for p in ROOT.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}", p.stem))

args = sys.argv[1:]
if args and args[0] != "--days":
    urls = args
else:
    days = int(args[1]) if args else 3
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    sitemap = (ROOT / "sitemap.xml").read_text()
    urls = [u for u, m in re.findall(r"<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", sitemap) if m >= since]
if not urls:
    sys.exit("nothing to submit")

body = json.dumps({"host": BASE.split("/")[2], "key": key, "keyLocation": f"{BASE}{key}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print(f"IndexNow: HTTP {r.status} for {len(urls)} url(s)")
    for u in urls:
        print("  " + u)
