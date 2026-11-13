"""Build one blog answer page from a JSON spec, then wire it into sitemap.xml, llms.txt and blog/index.html.

Usage:  python3 aeo/build_page.py aeo/specs/<slug>.json [--no-wire]

Spec keys: slug, author (francisco|alec), title, headline, description, kicker, h1, h1_text,
subtitle, body (HTML; may contain {{FAQ}}), faqs ([[q, a], ...]), card_tag, card_blurb, llms_line.
Optional: date (YYYY-MM-DD, default today).
Head, nav, styles and footer are copied from blog/linkedin-ghostwriting-cost-2026.html so
GTM, consent.js, favicons and the privacy link always match the live site.
"""
import json, html, re, math, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = open(f"{ROOT}/blog/linkedin-ghostwriting-cost-2026.html", encoding="utf-8").read()

def cut(start, end, include_end=True):
    i = TPL.index(start)
    j = TPL.index(end, i)
    return TPL[i:j + (len(end) if include_end else 0)]

HEAD_TOP = cut("<!DOCTYPE html>", '<script src="/assets/attribution.js" defer></script>')
STYLE = cut('<script src="https://cdn.tailwindcss.com"></script>', "</style>", include_end=False)
BODY_TOP = cut("</head>", "</nav>")
FOOTER = TPL[TPL.index("<!-- FOOTER -->"):]

EXTRA_CSS = """
  .limits { border: 1px solid rgba(11,16,32,0.1); background: #f7f8fb; border-radius: 16px; padding: 22px 26px; margin: 32px 0; }
  .limits h3 { margin: 0 0 12px; font-size: 20px; color: var(--ru-ink); }
  .limits ul { margin: 0; }
  .limits ul li { font-size: 16px; }
  .math { background: #f7f8fb; border: 1px solid rgba(11,16,32,0.06); border-radius: 14px; padding: 18px 22px; margin: 18px 0; font-size: 16px; line-height: 1.8; color: #374151; }
  .math strong { color: var(--ru-ink); }
"""

AUTHORS = {
    "francisco": {
        "id": "https://rallyup.team/authors/francisco-gost-scagliarini.html#person",
        "name": "Francisco Gost Scagliarini", "jobTitle": "Partner",
        "url": "https://rallyup.team/authors/francisco-gost-scagliarini.html",
        "slug": "francisco-gost-scagliarini",
        "sameAs": "https://www.linkedin.com/in/franciscogost",
        "byline": "francisco gost scagliarini", "role": "partner",
    },
    "alec": {
        "id": "https://rallyup.team/authors/alec-kremins.html#person",
        "name": "Alec Kremins", "jobTitle": "CEO",
        "url": "https://rallyup.team/authors/alec-kremins.html",
        "slug": "alec-kremins",
        "sameAs": "https://www.linkedin.com/in/aleckremins",
        "byline": "alec kremins", "role": "ceo",
    },
}

def visible_words(body_html):
    t = re.sub(r"<!--.*?-->", " ", body_html, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    return len(t.split())

def build(p):
    p.setdefault("date", datetime.date.today().isoformat())
    month = datetime.date.fromisoformat(p["date"]).strftime("%B %Y").lower()
    a = AUTHORS[p["author"]]
    url = f"https://rallyup.team/blog/{p['slug']}.html"
    faq_html = "\n".join(
        f"    <h3>{html.escape(q.lower() if p.get('lower_faq', True) else q, quote=False)}</h3>\n    <p>{html.escape(ans, quote=False)}</p>"
        for q, ans in p["faqs"])
    body_inner = p["body"].replace("{{FAQ}}", faq_html)
    words = visible_words(p["h1_text"] + " " + p["subtitle"] + " " + body_inner)
    mins = max(1, round(words / 230))
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": url + "#article",
                "headline": p["headline"],
                "description": p["description"],
                "datePublished": p["date"],
                "dateModified": p["date"],
                "image": "https://rallyup.team/assets/og-image.png?v=2",
                "author": {"@type": "Person", "@id": a["id"], "name": a["name"], "jobTitle": a["jobTitle"],
                           "url": a["url"], "sameAs": [a["sameAs"]], "worksFor": {"@id": "https://rallyup.team/#organization"}},
                "publisher": {"@id": "https://rallyup.team/#organization"},
                "mainEntityOfPage": url,
                "wordCount": words,
            },
            {
                "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q,
                                "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in p["faqs"]],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://rallyup.team/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://rallyup.team/blog/"},
                    {"@type": "ListItem", "position": 3, "name": p["headline"], "item": url},
                ],
            },
        ],
    }
    e = lambda s: html.escape(s, quote=True)
    head_meta = f"""
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['description'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#3d68f5">

<!-- Open Graph -->
<meta property="og:type" content="article">
<meta property="og:site_name" content="rallyup">
<meta property="og:title" content="{e(p['headline'])}">
<meta property="og:description" content="{e(p['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://rallyup.team/assets/og-image.png?v=2">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@rallyup">
<meta name="twitter:title" content="{e(p['headline'])}">
<meta name="twitter:description" content="{e(p['description'])}">
<meta name="twitter:image" content="https://rallyup.team/assets/og-image.png?v=2">

<!-- Analytics (GA4 + Microsoft Clarity) load via the shared consent loader above -->

<!-- Structured data: Article + FAQ + Breadcrumbs -->
<script type="application/ld+json">
{json.dumps(graph, indent=2, ensure_ascii=False)}
</script>

"""
    article = f"""
<article class="max-w-3xl mx-auto px-6 pt-12 pb-20">
  <p class="text-sm font-bold uppercase tracking-widest text-ru-blue mb-4"><a href="index.html" class="text-ru-blue no-underline">blog</a> · {p['kicker']}</p>
  <h1 class="text-4xl md:text-6xl font-black leading-[1.02] tracking-tight text-ru-blue-dark mb-6">
    {p['h1']}
  </h1>
  <p class="text-xl text-gray-500 mb-6 serif">{p['subtitle']}</p>
  <p class="text-sm text-gray-400 mb-2">published {month} · by <a href="/authors/{a['slug']}.html" class="underline">{a['byline']}</a>, {a['role']} · {mins} min read</p>
  <p class="text-sm text-gray-400 mb-10">last updated: {month}</p>
  <div class="prose">
{body_inner}
  </div>
</article>

"""
    out = (HEAD_TOP + "\n" + head_meta + STYLE + EXTRA_CSS + "</style>\n" + BODY_TOP + "\n" + article + FOOTER)
    path = f"{ROOT}/blog/{p['slug']}.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    return path, words, mins


def wire(p, mins):
    url = f"https://rallyup.team/blog/{p['slug']}.html"
    sm_path = f"{ROOT}/sitemap.xml"; sm = open(sm_path, encoding="utf-8").read()
    if url not in sm:
        entry = (f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{p['date']}</lastmod>\n"
                 f"    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n")
        sm = sm.replace("</urlset>", entry + "</urlset>"); open(sm_path, "w", encoding="utf-8").write(sm)
    ll_path = f"{ROOT}/llms.txt"; ll = open(ll_path, encoding="utf-8").read()
    if url not in ll:
        line = f"- [{p['headline']}]({url}){': ' + p['llms_line'] if p.get('llms_line') else ''}\n"
        anchor = "- [Francisco Gost Scagliarini, Partner]"
        assert anchor in ll, "llms.txt anchor missing"
        ll = ll.replace(anchor, line + anchor, 1); open(ll_path, "w", encoding="utf-8").write(ll)
    ix_path = f"{ROOT}/blog/index.html"; ix = open(ix_path, encoding="utf-8").read()
    if f'href="{p["slug"]}.html"' not in ix:
        month = datetime.date.fromisoformat(p["date"]).strftime("%B %Y").lower()
        card = (f'    <a href="{p["slug"]}.html" class="post-card">\n'
                f'      <span class="tag">{p.get("card_tag", "guide")}</span>\n'
                f'      <h2 class="text-2xl font-extrabold tracking-tight text-ru-blue-dark mb-2">{p["h1_text"]}</h2>\n'
                f'      <p class="text-gray-600 text-lg leading-relaxed">{p["card_blurb"]}</p>\n'
                f'      <p class="text-sm text-gray-400 mt-4">{month} · {mins} min read →</p>\n'
                f'    </a>\n\n')
        anchor = '<div class="grid gap-5">\n'
        assert anchor in ix, "blog index anchor missing"
        ix = ix.replace(anchor, anchor + card, 1); open(ix_path, "w", encoding="utf-8").write(ix)


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    spec["faqs"] = [tuple(x) for x in spec["faqs"]]
    path, words, mins = build(spec)
    if "--no-wire" not in sys.argv:
        wire(spec, mins)
    print(f"built {os.path.relpath(path, ROOT)}: {words} words, {mins} min read")
