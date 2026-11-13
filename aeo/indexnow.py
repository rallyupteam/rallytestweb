"""Tell Bing/Yandex/Seznam (and through them, ChatGPT search) which pages changed.

Usage:  python3 aeo/indexnow.py blog/a.html index.html ...
Paths are repo-relative; index.html files map to their folder URL.
"""
import json, sys, urllib.request

KEY = "8a47b565d1617092c26596b08f0617c7"  # public by design: served at /<key>.txt

def to_url(path):
    path = path.lstrip("./")
    if path == "index.html":
        return "https://rallyup.team/"
    if path.endswith("/index.html"):
        return "https://rallyup.team/" + path[: -len("index.html")]
    return "https://rallyup.team/" + path

def main():
    urls = sorted({to_url(p) for p in sys.argv[1:] if p.endswith(".html")})
    if not urls:
        print("no html changes, nothing to ping"); return
    body = json.dumps({"host": "rallyup.team", "key": KEY,
                       "keyLocation": f"https://rallyup.team/{KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow HTTP {r.status} for {len(urls)} URLs")
        for u in urls: print("  " + u)
        if r.status not in (200, 202):
            sys.exit(1)

if __name__ == "__main__":
    main()
