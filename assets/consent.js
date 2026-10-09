/* =========================================================================
   rallyup.team — analytics loader
   -------------------------------------------------------------------------
   Loads analytics/advertising on page load for every visitor: the Meta
   (Facebook) Pixel, Google Analytics (GA4), Microsoft Clarity, and the
   Snitcher visitor-identification tracker. No cookie-consent banner — the
   site serves US traffic; see /privacy.html for disclosures and how to opt out.
   (Filename kept as consent.js so existing <script src> references and the
   published URL stay valid.)
   ========================================================================= */
(function () {
  var w = window, d = document;
  if (w.__ruAnalyticsLoaded) return;
  w.__ruAnalyticsLoaded = true;

  var META_PIXEL_ID = '1027686310240354';
  var GA4_ID = 'G-0KD96EK20Z';
  var CLARITY_ID = 'wfms73p8co';
  var SNITCHER_PROFILE_ID = 'sTXBlXu2Ib';

  function loadMetaPixel() {
    if (w.fbq) return;
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0';
      n.queue = []; t = b.createElement(e); t.async = !0;
      t.src = v; s = b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t, s);
    }(w, d, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    w.fbq('init', META_PIXEL_ID);
    w.fbq('track', 'PageView');
  }

  function loadGA4() {
    if (w.gtag) return;
    var s = d.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
    (d.getElementsByTagName('head')[0] || d.documentElement).appendChild(s);
    w.dataLayer = w.dataLayer || [];
    w.gtag = function () { w.dataLayer.push(arguments); };
    w.gtag('js', new Date());
    w.gtag('config', GA4_ID);
  }

  function loadClarity() {
    if (w.clarity) return;
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(w, d, 'clarity', 'script', CLARITY_ID);
  }

  function loadSnitcher() {
    if (w.Snitcher && (w.Snitcher.initialized || w.Snitcher._loaded)) return;
    // Snitcher install snippet, verbatim.
    !function(e){"use strict";var t=e&&e.namespace;if(t&&e.profileId&&e.cdn){var i=window[t];if(i&&Array.isArray(i)||(i=window[t]=[]),!i.initialized&&!i._loaded)if(i._loaded)console&&console.warn("[Radar] Duplicate initialization attempted");else{i._loaded=!0;["track","page","identify","company","group","alias","ready","debug","on","off","once","trackClick","trackSubmit","trackLink","trackForm","pageview","screen","reset","register","setAnonymousId","addSourceMiddleware","addIntegrationMiddleware","addDestinationMiddleware","giveCookieConsent","denyCookieConsent"].forEach((function(e){var a;i[e]=(a=e,function(){var e=window[t];if(e.initialized)return e[a].apply(e,arguments);var i=[].slice.call(arguments);return i.unshift(a),e.push(i),e})})),-1===e.apiEndpoint.indexOf("http")&&(e.apiEndpoint="https://"+e.apiEndpoint),i.bootstrap=function(){var t,i=document.createElement("script");i.async=!0,i.type="text/javascript",i.id="__radar__",i.setAttribute("data-settings",JSON.stringify(e)),i.src=[-1!==(t=e.cdn).indexOf("http")?"":"https://",t,"/releases/latest/radar.min.js"].join("");var a=document.scripts[0];a.parentNode.insertBefore(i,a)},i.bootstrap()}}else"undefined"!=typeof console&&console.error("[Radar] Configuration incomplete")}({
      "apiEndpoint": "radar.snitcher.com",
      "cdn": "cdn.snitcher.com",
      "namespace": "Snitcher",
      "profileId": SNITCHER_PROFILE_ID
    });
  }

  loadMetaPixel();
  loadGA4();
  loadClarity();
  loadSnitcher();
})();
