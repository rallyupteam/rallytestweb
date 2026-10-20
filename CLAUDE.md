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
