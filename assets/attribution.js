/*
 * Campaign attribution passthrough.
 *
 * Carries whatever brought a visitor here onto every Cal.com booking link, so
 * someone who clicks one of Alec's LinkedIn posts, lands on the homepage and
 * books from there is counted as LinkedIn — not as "website". Without this, the
 * site silently claims credit for every channel that routes through it.
 *
 * Cal picks the values up through five hidden booking questions whose
 * identifiers match these parameter names exactly; they travel from there into
 * Attio and the weekly attribution report.
 *
 * The CTA labels already on each link (data-cta-location) become utm_content,
 * so per-CTA conversion comes for free and no markup needs to change.
 *
 * Every storage and URL call is wrapped: a browser blocking site data, or a
 * malformed href, must still leave a working booking link behind.
 */
(function () {
  'use strict';

  var KEY = 'ru_attr';
  var PARAMS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];

  function resolve() {
    var found = {};
    try {
      var q = new URLSearchParams(window.location.search);
      PARAMS.forEach(function (k) {
        var v = q.get(k);
        if (v) found[k] = v;
      });
    } catch (e) {}

    // Inbound tags win and are remembered for the rest of the visit, so the
    // attribution survives a click through to the case studies and back.
    if (Object.keys(found).length) {
      try { sessionStorage.setItem(KEY, JSON.stringify(found)); } catch (e) {}
      return found;
    }

    try {
      var stored = JSON.parse(sessionStorage.getItem(KEY) || '{}');
      if (stored && Object.keys(stored).length) return stored;
    } catch (e) {}

    // Nothing inbound, nothing remembered: this really is a direct site visit.
    return { utm_source: 'website', utm_medium: 'site_cta', utm_campaign: 'site' };
  }

  var attr = resolve();

  function tag(a) {
    if (!a || !a.href || a.href.indexOf('cal.com') === -1) return;
    try {
      var u = new URL(a.href, window.location.href);
      PARAMS.forEach(function (k) {
        if (attr[k] && !u.searchParams.has(k)) u.searchParams.set(k, attr[k]);
      });
      var where = a.getAttribute('data-cta-location') || a.getAttribute('data-cta');
      if (where && !u.searchParams.has('utm_content')) {
        u.searchParams.set('utm_content', where);
      }
      a.href = u.toString();
    } catch (e) {}
  }

  function tagAll() {
    var links = document.querySelectorAll('a[href*="cal.com"]');
    for (var i = 0; i < links.length; i++) tag(links[i]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', tagAll);
  } else {
    tagAll();
  }

  // Re-tag at click time as well. Tagging is idempotent (it only fills params
  // that are absent), and the click is the one moment a link is guaranteed to
  // exist — which covers anything rendered after load.
  document.addEventListener(
    'click',
    function (e) {
      var t = e.target;
      var a = t && t.closest ? t.closest('a[href*="cal.com"]') : null;
      if (a) tag(a);
    },
    true
  );
})();
