# rallyup.team — project conventions

Static HTML site (no framework/build step). Each page is a standalone `.html` file.
Hosted on AWS Amplify — every push to `main` auto-deploys.

## Required on every page: analytics + consent

Analytics/advertising (the Meta/Facebook Pixel) is loaded through a shared,
consent-gated loader in [assets/consent.js](assets/consent.js). It renders the
cookie-consent banner and only loads the pixel **after** the visitor clicks
"accept" (declining keeps it off). Do NOT inline the raw Meta Pixel snippet on
pages (and no `<noscript>` fallback pixel, which can't be consent-gated) — always
go through the shared file so consent gating stays uniform.

**Every new HTML page MUST include**, in the `<head>` (right after the
`<meta charset>` / `<meta viewport>` tags):

```html
<!-- Cookie consent + Meta Pixel (pixel loads only after consent) -->
<script src="/assets/consent.js" defer></script>
```

**And in the footer**, a link to the privacy policy:

```html
<a href="/privacy.html" class="hover:text-ru-yellow">privacy policy</a>
```

Use absolute paths (`/assets/...`, `/privacy.html`) so they resolve from any
directory depth (`blog/`, `case-studies/`, etc.).

Pages currently wired up: `index.html`, `blog/index.html`,
`blog/best-linkedin-ghostwriting-agencies-2026.html`, `case-studies/index.html`,
`case-studies/pandadoc.html`, `case-studies/deway.html`,
`case-studies/prettydamnquick.html`, `privacy.html`.

## Privacy policy

[privacy.html](privacy.html) discloses the analytics/advertising (Meta Pixel) usage.
If you change what data is collected or which third parties are used, update that
page and its "last updated" date.
