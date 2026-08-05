# rallyup.team — project conventions

Static HTML site (no framework/build step). Each page is a standalone `.html` file.
Hosted on AWS Amplify — every push to `main` auto-deploys.

## Required: Swan analytics on every page

**Every new HTML page MUST include the Swan analytics snippet in its `<head>`**,
placed immediately after the `<meta charset>` / `<meta viewport>` tags. This is how
we track visitors across the whole site, so a page without it is a gap in analytics.

When creating any new page, paste this exact snippet into the `<head>`:

```html
<!-- Swan analytics -->
<script>
  (function () {
    var w = window;
    var swan = (w.swan = w.swan || []);
    if (swan.isLoaded) return;
    swan.isLoaded = true;
    swan.pk = 'cmevnk77u0005l70537an0s07';
    var sidKey = 'swan.sid';
    var sid;
    try {
      sid = w.localStorage.getItem(sidKey);
      if (!sid) {
        sid = w.crypto && w.crypto.randomUUID
          ? w.crypto.randomUUID()
          : Date.now().toString(36) + Math.random().toString(36).slice(2);
        w.localStorage.setItem(sidKey, sid);
      }
    } catch (e) {
      sid = Date.now().toString(36) + Math.random().toString(36).slice(2);
    }
    swan.sid = sid;
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.async = true;
    script.src = "https://script.getswan.com?pk=cmevnk77u0005l70537an0s07&sid=" + encodeURIComponent(sid);
    if (swan.eId) { script.src += "&eId=" + encodeURIComponent(swan.eId); }
    var head = document.getElementsByTagName('head')[0];
    head.appendChild(script);
  })();
</script>
```

Pages currently carrying the snippet: `index.html`, `blog/index.html`,
`blog/best-linkedin-ghostwriting-agencies-2026.html`, `case-studies/pandadoc.html`.
