# rallyup.team — project conventions

Static HTML site (no framework/build step). Each page is a standalone `.html` file.
Hosted on AWS Amplify — every push to `main` auto-deploys.

## Required on every page: analytics

Analytics/advertising (the Meta/Facebook Pixel, Google Analytics GA4,
Microsoft Clarity, and the Snitcher visitor-identification tracker) is loaded
through a shared loader in [assets/consent.js](assets/consent.js). There is NO
cookie-consent banner — the tools load on page load for every visitor (the site
serves US traffic; disclosures + opt-out live in [privacy.html](privacy.html)).
Do NOT inline raw analytics snippets on pages — always go through the shared file
so the tracking stays uniform. Pages may contain guarded `typeof gtag`/`typeof
clarity` event-tracking helpers; those no-op until the libraries load.

(The file is still named `consent.js` so existing `<script src>` references and
the published URL stay valid, even though it no longer gates on consent.)

**Every new HTML page MUST include**, in the `<head>` (right after the
`<meta charset>` / `<meta viewport>` tags):

```html
<!-- Analytics: Meta Pixel, GA4, Clarity & Snitcher -->
<script src="/assets/consent.js" defer></script>
```

This single include is all a new page needs — it wires up **all four** tools
(Meta Pixel, GA4, Microsoft Clarity, and Snitcher). There is nothing else to
paste per page; do NOT add separate GA4 or Clarity snippets (they would
double-load). To change IDs or add a tool, edit
[assets/consent.js](assets/consent.js) once.

**Google Tag Manager** (container `GTM-582JGF2D`, feeds GA4 stream
`G-E6S7WP4S7L`) is installed **inline on every page** — this is the one exception
to "don't inline analytics," because GTM requires it. It runs alongside, and
separately from, `consent.js` (do not move it in there). Two blocks, kept
verbatim:

- the GTM `<script>` as high in the `<head>` as possible (right after
  `<meta charset>` / `<meta viewport>`, before the favicons);
- the GTM `<noscript>` iframe immediately after the opening `<body>` tag.

New pages MUST include both.

**And in the footer**, a link to the privacy policy:

```html
<a href="/privacy.html" class="hover:text-ru-yellow">privacy policy</a>
```

**Favicons** — every page's `<head>` also carries the shared favicon block (built
from the logo mark; source is [favicon.svg](favicon.svg), rasterized to
`/favicon.ico`, `/favicon-96x96.png`, `/apple-touch-icon.png`):

```html
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

Use absolute paths (`/assets/...`, `/privacy.html`) so they resolve from any
directory depth (`blog/`, `case-studies/`, etc.).

Pages currently wired up: `index.html`, `privacy.html`, `blog/index.html`,
`blog/best-linkedin-ghostwriting-agencies-2026.html`, `case-studies/index.html`,
`case-studies/pandadoc.html`, `case-studies/deway.html`,
`case-studies/prettydamnquick.html`, `alec-on-x/index.html`,
`book-a-call/index.html`, `lets-connect/index.html`, `lets-talk/index.html`,
`speak-with-alec/index.html`, `speak-with-matt/index.html`.

## Privacy policy

[privacy.html](privacy.html) discloses the analytics/advertising (Meta Pixel) usage.
If you change what data is collected or which third parties are used, update that
page and its "last updated" date.

## Exception: `audience-building/` (LinkedIn ads landing page)

Vite/React bundle, originally built by our ads contractor (Shimi, Aurum Media), with copy, logo
and visuals reworked by RallyUp on 2026-11-10 (he cleared copy/visual changes; form, calendar,
consent lines, GTM and payload are his and unchanged). Served files:
`audience-building/index.html`, `/assets/index-C0NPREZy.js`, `/assets/index-Bxa2nGHJ.css` and the
two `.woff2` fonts in `/assets/` (the bundle uses root paths). The hero logo strip and result cards
load the existing `/assets/logos/*` and `/assets/wordmarks/lightbank.png`; the hero "backed by" row
also loads `/assets/wordmarks/verissimo.png` (Verissimo Ventures, from verissimo.vc, added 2026-11-11).
Editable source lives in the rallyupcontext repo at `landing-pages/audience-building/`: edit there, `npx vite build`, replace
these files. It deliberately carries GTM only, without `consent.js`, at the contractor's request
to avoid double-counting ad traffic. It is `noindex,nofollow` and kept out of `sitemap.xml`.

## AEO pipeline (`aeo/`)

Blog answer pages are built and maintained by a monthly cloud routine that follows
[aeo/RUNBOOK.md](aeo/RUNBOOK.md) and opens a PR (it never pushes to `main`).
- `python3 aeo/build_page.py aeo/specs/<slug>.json` builds a page and wires sitemap, llms.txt, blog index.
- `python3 aeo/check.py` validates every blog page (tags, schema, FAQ match, links, forbidden phrases). Must pass.
- `.github/workflows/aeo.yml` runs the check on PRs and pushes, and pings IndexNow for changed pages after deploy.
- Phrases that must never appear publicly go in `aeo/forbidden.txt`.
