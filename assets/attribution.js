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

  var LAST_TOUCH = 'ru_attr_last'; // localStorage: last non-direct arrival
  var LAST_TOUCH_DAYS = 30;

  // AI assistants that tag their own outbound links. ChatGPT appends
  // utm_source=chatgpt.com to every link it cites; left alone, that reads as a
  // tagged campaign with no name and lands in 'unattributed' on the report.
  var AI_SOURCE = /^(chatgpt(\.com)?|chat\.openai\.com|openai(\.com)?|perplexity(\.ai)?|claude(\.ai)?|gemini(\.google\.com)?|copilot(\.microsoft\.com)?|you\.com|phind(\.com)?)$/;

  function save(store, key, value) {
    try { store.setItem(key, JSON.stringify(value)); } catch (e) {}
  }
  function load(store, key) {
    try {
      var v = JSON.parse(store.getItem(key) || '{}');
      return v && Object.keys(v).length ? v : null;
    } catch (e) { return null; }
  }

  function resolve() {
    var found = {};
    try {
      var q = new URLSearchParams(window.location.search);
      PARAMS.forEach(function (k) {
        var v = q.get(k);
        if (v) found[k] = v;
      });
    } catch (e) {}

    // An AI assistant's own tag is an AI visit, not a campaign.
    if (found.utm_source && !found.utm_campaign &&
        AI_SOURCE.test(String(found.utm_source).toLowerCase())) {
      found = { utm_medium: 'site_cta', utm_campaign: 'site', utm_source: 'ai',
                utm_term: String(found.utm_source).toLowerCase(), landing: landingPath() };
    }

    // Inbound tags win and are remembered for the rest of the visit, so the
    // attribution survives a click through to the case studies and back.
    if (Object.keys(found).length) {
      save(sessionStorage, KEY, found);
      if (found.utm_campaign === 'site') save(localStorage, LAST_TOUCH, stamp(found));
      return found;
    }

    var stored = load(sessionStorage, KEY);
    if (stored) return stored;

    // Nothing inbound and nothing remembered: this is the first page of the
    // visit. Classify the referrer now (it only exists on arrival) and KEEP
    // it for the visit. Before 2026-11-16 this was recomputed on every page,
    // so someone who landed on a blog post from ChatGPT and booked from the
    // homepage was counted as 'direct' (page two's referrer is our own site).
    var arrived = classifyReferrer();

    // A direct arrival within 30 days of an AI, search, list or other
    // referral keeps that earlier source: buyers often read an answer, leave,
    // and type the URL back in days later. Tagged campaigns are unaffected.
    if (arrived.utm_source === 'direct') {
      var last = load(localStorage, LAST_TOUCH);
      if (last && last.ts && Date.now() - last.ts < LAST_TOUCH_DAYS * 86400000) {
        delete last.ts;
        arrived = last;
      }
    } else {
      save(localStorage, LAST_TOUCH, stamp(arrived));
    }

    save(sessionStorage, KEY, arrived);
    return arrived;
  }

  function stamp(a) {
    var out = merge(a, {});
    out.ts = Date.now();
    return out;
  }

  // The page the visitor first landed on, e.g. /blog/linkedin-ghostwriting-cost-2026.
  // It travels to Cal inside utm_content, so the report shows which answer page
  // brought the booking in.
  function landingPath() {
    try { return location.pathname.replace(/\.html$/, '').slice(0, 80) || '/'; } catch (e) { return ''; }
  }

  /*
   * Buckets the referring host into a source we can report on.
   *
   * Deliberately coarse. The useful question is "did search, an AI assistant,
   * or another site send this person", not which of nine search engines.
   *
   * Honest limits: document.referrer is empty for a large share of real
   * traffic — typed URLs, most in-app browsers, anything with a strict
   * referrer policy — and all of that lands in 'direct' whether or not it
   * truly was. AI assistants are the worst case: several open links in a way
   * that strips the referrer, so that bucket undercounts. Treat these as a
   * floor, not a census.
   */
  function classifyReferrer() {
    var base = { utm_medium: 'site_cta', utm_campaign: 'site', landing: landingPath() };
    var host = '';
    try {
      if (!document.referrer) return merge(base, { utm_source: 'direct' });
      host = new URL(document.referrer).hostname.replace(/^www\./, '').toLowerCase();
    } catch (e) {
      return merge(base, { utm_source: 'direct' });
    }

    // Our own pages are not a referrer.
    if (host === location.hostname.replace(/^www\./, '').toLowerCase()) {
      return merge(base, { utm_source: 'direct' });
    }

    var SEARCH = /^(google|bing|duckduckgo|yahoo|ecosia|brave|baidu|yandex|startpage)\./;
    var AI = /^(chatgpt\.com|chat\.openai\.com|openai\.com|perplexity\.ai|claude\.ai|gemini\.google\.com|copilot\.microsoft\.com|you\.com|phind\.com)$/;
    // The "best agency" lists and directories rallyup is on. These are the
    // pages AI engines cite, so a click from one is counted as AEO.
    var LISTING = /^(ghostwriterindex\.com|getaob\.com|tryordinal\.com|clutch\.co|goodfirms\.co|sortlist\.com|sortlist\.co\.uk)$/;
    var SOCIAL = /^(linkedin|twitter|x|facebook|instagram|t|lnkd|reddit|news\.ycombinator)\./;

    if (AI.test(host)) return merge(base, { utm_source: 'ai', utm_term: host });
    if (LISTING.test(host)) return merge(base, { utm_source: 'listing', utm_term: host });
    if (SEARCH.test(host)) return merge(base, { utm_source: 'search', utm_term: host });
    if (SOCIAL.test(host)) return merge(base, { utm_source: 'social', utm_term: host });
    return merge(base, { utm_source: 'referral', utm_term: host });
  }

  function merge(a, b) {
    var out = {};
    for (var k in a) if (Object.prototype.hasOwnProperty.call(a, k)) out[k] = a[k];
    for (var j in b) if (Object.prototype.hasOwnProperty.call(b, j)) out[j] = b[j];
    return out;
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
      if (!u.searchParams.has('utm_content')) {
        // CTA label, plus the landing page for website traffic:
        // "blog_callout@/blog/linkedin-ghostwriting-cost-2026".
        var content = (where || '') + (attr.landing ? '@' + attr.landing : '');
        if (content) u.searchParams.set('utm_content', content.slice(0, 120));
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
