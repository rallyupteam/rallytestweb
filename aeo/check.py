"""Validate every blog page before it ships. Exit 1 on any ERROR; STALE lines are a to-do list, not failures.

Usage:  python3 aeo/check.py            # all blog pages
        python3 aeo/check.py blog/x.html # just these
"""
import datetime, glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTHOR_IDS = {
    "https://rallyup.team/authors/francisco-gost-scagliarini.html#person",
    "https://rallyup.team/authors/alec-kremins.html#person",
}
STALE_DAYS = 90
FORBIDDEN = [l.strip() for l in open(f"{ROOT}/aeo/forbidden.txt", encoding="utf-8")
             if l.strip() and not l.startswith("#")]

def read(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()

def visible(s):
    s = re.sub(r"<(script|style)\b.*?</\1>", " ", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))

def check(rel, sitemap, llms, index, today):
    s = read(rel)
    errs, notes = [], []
    url = "https://rallyup.team/" + rel
    if s.count("GTM-582JGF2D") < 2: errs.append("GTM script + noscript missing")
    if '<script src="/assets/consent.js" defer></script>' not in s: errs.append("consent.js missing")
    if 'href="/favicon.ico"' not in s: errs.append("favicons missing")
    if "/privacy.html" not in s: errs.append("privacy link missing")
    m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    if not m or m.group(1) != url: errs.append(f"canonical != {url}")
    graph = []
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            d = json.loads(b)
        except ValueError as e:
            errs.append(f"JSON-LD does not parse: {e}"); continue
        graph += d.get("@graph", [d])
    art = next((g for g in graph if g.get("@type") in ("Article", "BlogPosting")), None)
    if art is None:
        errs.append("no Article JSON-LD")
    else:
        if art.get("author", {}).get("@id") not in AUTHOR_IDS: errs.append("Article author is not a known Person @id")
        mod = art.get("dateModified")
        if mod:
            age = (today - datetime.date.fromisoformat(mod[:10])).days
            if age > STALE_DAYS: notes.append(f"STALE: dateModified {mod} ({age} days)")
        else:
            errs.append("Article has no dateModified")
    faq = next((g for g in graph if g.get("@type") == "FAQPage"), None)
    if faq:
        sec = re.search(r'<h2 id="faq">(.*?)</article>', s, re.S)
        vis = [html.unescape(q).strip().lower() for q in re.findall(r"<h3>(.*?)</h3>", sec.group(1))] if sec else []
        schema = [q["name"].strip().lower() for q in faq["mainEntity"]]
        # The schema may carry one extra question: the page's headline question, answered in "the short answer".
        missing = [q for q in vis if q not in schema]
        if missing or len(schema) - len(vis) > 1:
            errs.append(f"FAQ mismatch: {len(schema)} in schema, {len(vis)} on page, not in schema: {missing}")
    body = visible(re.search(r"<article.*?</article>|<main.*?</main>", s, re.S).group(0)) if re.search(r"<article|<main", s) else visible(s)
    if "—" in body: errs.append("em dash in visible text (house style)")
    for f in FORBIDDEN:
        if f.lower() in s.lower(): errs.append(f"forbidden phrase: {f!r}")
    for href in set(re.findall(r'href="([^"#:?]+\.html)"', s)):
        target = os.path.normpath(os.path.join(ROOT, href.lstrip("/")) if href.startswith("/") else os.path.join(ROOT, os.path.dirname(rel), href))
        if not os.path.exists(target): errs.append(f"broken internal link: {href}")
    if url not in sitemap: errs.append("not in sitemap.xml")
    if url not in llms: errs.append("not in llms.txt")
    if f'href="{os.path.basename(rel)}"' not in index: errs.append("not linked from blog/index.html")
    return errs, notes

def main():
    today = datetime.date.today()
    files = sys.argv[1:] or sorted(os.path.relpath(p, ROOT) for p in glob.glob(f"{ROOT}/blog/*.html")
                                   if not p.endswith("/index.html"))
    sitemap, llms, index = read("sitemap.xml"), read("llms.txt"), read("blog/index.html")
    bad = 0
    for rel in files:
        errs, notes = check(rel, sitemap, llms, index, today)
        for e in errs: print(f"ERROR {rel}: {e}")
        for n in notes: print(f"{n.split(':')[0]} {rel}:{n.split(':', 1)[1]}")
        bad += bool(errs)
    print(f"{len(files)} pages checked, {bad} with errors")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
