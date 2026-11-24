#!/usr/bin/env python3
"""Diagnose every missed AI recommendation, per buyer decision (Granola AEO method).

Usage:
  python3 aeo/diagnose.py CITATIONS.json [MORE.json ...] [--tracker TRACKER.json] [--out FILE.md]

Citation files use the aeo-outreach shape: a list of rows with
  {engine, prompt, url, domain, date, answer_mentions_us, competitors}
(Otterly exports and the Claude web-search sweep both produce it.)

For each decision in aeo/decisions.json it reports, per engine, whether the answer MENTIONS
rallyup and whether it CITES a rallyup.team page, which competitors were named instead, and the
third-party sources the engines leaned on. Then it puts the decision in one bucket:

  WINNING          mentioned in at least half the engines measured: defend, keep it fresh
  CITED-NOT-NAMED  an engine read our page but its answer didn't name us: CLAIM problem, the page
                   doesn't state plainly who rallyup is best for. Sharpen the short answer.
  NOT-RETRIEVED    we have a page but no engine cited it: coverage/technical. Match the title and
                   short answer to the buyer's phrasing, add internal links, check it's indexed.
  NO-PAGE          no page answers it: OWN. First add a section or FAQ to the closest existing
                   page; a new page only if no existing page can carry it.
  TOO-NEW          not cited, but every page for it was under 3 weeks old at the latest measurement: retest.
  NOT-MEASURED     no citation rows for it yet: add it to the next sweep.
Separately, EARN flags the third-party pages engines cite that don't list us (outreach targets),
and branded decisions are reported apart from non-branded ones.
"""
import json, re, sys, os, difflib, collections, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OURS = re.compile(r'(^|\.)rallyup\.team$')
# Where buyers talk (Granola: 'show up where buyers already talk'). Not outreach targets: we join
# these conversations ourselves, as named people, never as promotion.
COMMUNITY = re.compile(r'(^|\.)(reddit\.com|linkedin\.com|youtube\.com|quora\.com|x\.com|twitter\.com)$')
NEUTRAL = re.compile(r'(^|\.)(wikipedia\.org)$')
MONTHS = {m: i for i, m in enumerate(['january','february','march','april','may','june','july','august','september','october','november','december'], 1)}


def published(page):
    """datePublished from the page's JSON-LD, or None."""
    try: s = open(os.path.join(HERE, '..', page)).read()
    except OSError: return None
    m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', s)
    return datetime.date.fromisoformat(m.group(1)) if m else None


def norm(s):
    s = re.sub(r'\(.*?\)', '', s or '').lower()
    return ' '.join(re.sub(r'[^a-z0-9 ]+', ' ', s).split())


def main(argv):
    files, tracker, out = [], None, None
    it = iter(argv)
    for a in it:
        if a == '--tracker': tracker = next(it)
        elif a == '--out': out = next(it)
        else: files.append(a)
    if not files:
        print(__doc__); return 2
    dec = json.load(open(os.path.join(HERE, 'decisions.json')))['decisions']
    alias = {}
    for d in dec:
        for p in d['prompts']: alias[norm(p)] = d['id']
    rows, unmatched = [], collections.Counter()
    for f in files:
        for r in json.load(open(f)):
            n = norm(r.get('prompt'))
            did = alias.get(n)
            if not did:
                m = difflib.get_close_matches(n, list(alias), n=1, cutoff=0.85)
                did = alias[m[0]] if m else None
            if not did:
                unmatched[r.get('prompt')] += 1; continue
            r['_d'] = did; rows.append(r)
    trk = {}
    if tracker:
        t = json.load(open(tracker)); t = t.get('domains', t)
        trk = t if isinstance(t, dict) else {x['domain']: x for x in t}
    dates = sorted({r.get('date') for r in rows if r.get('date')})

    by = collections.defaultdict(list)
    for r in rows: by[r['_d']].append(r)
    report, buckets, kpi = [], collections.Counter(), collections.Counter()
    for d in dec:
        rs = by.get(d['id'], [])
        eng = sorted({r['engine'] for r in rs})
        named = sorted({r['engine'] for r in rs if r.get('answer_mentions_us')})
        cited = collections.defaultdict(set)
        for r in rs:
            if OURS.search(r.get('domain') or ''):
                cited[r['engine']].add(re.sub(r'^https?://(www\.)?rallyup\.team/?', '/', r['url']))
        comp = collections.Counter(c for r in rs for c in (r.get('competitors') or []))
        ext = [r for r in rs if not OURS.search(r.get('domain') or '')]
        third = collections.Counter(r['url'] for r in ext)
        talk = collections.Counter(r['url'] for r in ext if COMMUNITY.search(r['domain']))
        doms = collections.Counter(r['domain'] for r in ext if not COMMUNITY.search(r['domain']) and not NEUTRAL.search(r['domain']))
        pub = [published(p) for p in d['pages']]
        first_data = max((r['date'] for r in rs if r.get('date')), default=None)
        too_new = bool(pub) and first_data and all(
            x and (datetime.date.fromisoformat(first_data) - x).days < 21 for x in pub)
        cited_not_named = sorted(e for e in cited if e not in named)
        if not rs: b = 'NOT-MEASURED'
        elif len(named) * 2 >= len(eng): b = 'WINNING'
        elif cited_not_named: b = 'CITED-NOT-NAMED'
        elif not d['pages']: b = 'NO-PAGE'
        elif not cited and too_new: b = 'TOO-NEW'
        elif not cited: b = 'NOT-RETRIEVED'
        else: b = 'CITED-NOT-NAMED'
        branded = d.get('branded', False)
        if not branded:
            buckets[b] += 1
            kpi['cells'] += len(eng); kpi['named'] += len(named)
            kpi['cited_cells'] += len(cited)
        earn = []
        for dm, _ in doms.most_common(12):
            st = (trk.get(dm) or {}).get('status')
            if st in (None, 'candidate', 'sent', 'promised', 'no-reply'):
                earn.append(f"{dm} ({st or 'not in tracker'})")
        report.append(dict(d=d, b=b, eng=eng, named=named, cited=cited, comp=comp, third=third,
                           doms=doms, earn=earn[:5], branded=branded, n=len(rs), talk=talk))

    L = [f"# AEO diagnosis, {datetime.date.today()}", "",
         f"Source: {', '.join(os.path.basename(f) for f in files)} ({len(rows)} citation rows, answers dated {dates[0] if dates else '?'} to {dates[-1] if dates else '?'}).", "",
         "## Scorecard (non-branded decisions only)", "",
         f"- Mention share: rallyup named in **{kpi['named']} of {kpi['cells']}** decision x engine answers.",
         f"- Citation share: a rallyup.team page cited in **{kpi['cited_cells']} of {kpi['cells']}**.",
         "- Buckets: " + ', '.join(f"{k} {v}" for k, v in sorted(buckets.items())), ""]
    order = ['NO-PAGE', 'NOT-RETRIEVED', 'CITED-NOT-NAMED', 'TOO-NEW', 'NOT-MEASURED', 'WINNING']
    L += ["## Ledger", "", "| decision | stage | bucket | named by | cited by | named instead |", "|---|---|---|---|---|---|"]
    for x in sorted(report, key=lambda x: (x['branded'], order.index(x['b']), x['d']['stage'])):
        L.append(f"| {x['d']['id']}{' (branded)' if x['branded'] else ''} | {x['d']['stage']} | {x['b']} | "
                 f"{', '.join(x['named']) or '-'} / {len(x['eng'])} | {', '.join(sorted(x['cited'])) or '-'} | "
                 f"{', '.join(c for c, _ in x['comp'].most_common(3)) or '-'} |")
    L += ["", "## Per decision", ""]
    for x in sorted(report, key=lambda x: (x['branded'], order.index(x['b']))):
        d = x['d']
        L += [f"### {d['id']}: {d['decision']}", f"- Bucket: **{x['b']}**. Keyword: `{d['keyword']}`. Our page(s): {', '.join(d['pages']) or 'none'}."]
        if x['cited']:
            L.append('- Our pages cited: ' + '; '.join(f"{e}: {', '.join(sorted(u))}" for e, u in sorted(x['cited'].items())))
        if x['third']:
            L.append('- Sources the engines used most: ' + ', '.join(f"{u} ({n})" for u, n in x['third'].most_common(4)))
        if x['talk']:
            L.append('- Where buyers talk (join as a named person, never promote): ' + ', '.join(f"{u} ({n})" for u, n in x['talk'].most_common(4)))
        if x['earn']:
            L.append('- EARN (cited, not ours, not ruled out in tracker): ' + ', '.join(x['earn']))
        L.append('')
    if unmatched:
        L += ["## Prompts in the data that match no decision", ""] + [f"- {p} ({n} rows)" for p, n in unmatched.most_common()]
    text = '\n'.join(L) + '\n'
    if out: open(out, 'w').write(text)
    print(text)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
