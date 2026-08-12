/* =========================================================================
   rallyup.team — cookie consent + analytics loader
   -------------------------------------------------------------------------
   Analytics/advertising — the Meta (Facebook) Pixel, Google Analytics (GA4),
   and Microsoft Clarity — load only AFTER the visitor accepts. The choice is
   remembered in localStorage so the banner shows once. Declining prevents all
   of them from loading for that visitor. No <noscript> fallback pixels — a
   no-JS beacon can't be consent-gated, so they are intentionally omitted.
   ========================================================================= */
(function () {
  var w = window, d = document;
  var CONSENT_KEY = 'ru.cookieConsent';   // 'accepted' | 'declined'
  var META_PIXEL_ID = '1027686310240354';
  var GA4_ID = 'G-0KD96EK20Z';
  var CLARITY_ID = 'wfms73p8co';

  /* ---- analytics loaders (fire only with consent) ---- */
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

  function loadAnalytics() {
    loadMetaPixel();
    loadGA4();
    loadClarity();
  }

  /* ---- consent storage helpers ---- */
  function getConsent() {
    try { return w.localStorage.getItem(CONSENT_KEY); } catch (e) { return null; }
  }
  function setConsent(v) {
    try { w.localStorage.setItem(CONSENT_KEY, v); } catch (e) {}
  }

  /* ---- decide up front ---- */
  var choice = getConsent();
  if (choice === 'accepted') { loadAnalytics(); return; }
  if (choice === 'declined') { return; }

  /* ---- otherwise show the banner ---- */
  function injectStyles() {
    if (d.getElementById('ru-consent-styles')) return;
    var css =
      '#ru-consent-overlay{position:fixed;inset:0;z-index:2147482999;' +
      'background:rgba(15,23,42,.55);-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px);' +
      'opacity:0;transition:opacity .3s ease;}' +
      '#ru-consent-overlay.ru-show{opacity:1;}' +
      '#ru-consent{position:fixed;left:16px;right:16px;top:24px;z-index:2147483000;' +
      'max-width:760px;margin:0 auto;background:#2a3ad8;color:#fff;border-radius:16px;' +
      'box-shadow:0 18px 50px rgba(15,23,42,.45);padding:18px 20px;' +
      'font-family:inherit;display:flex;flex-wrap:wrap;align-items:center;gap:14px 18px;' +
      'opacity:0;transform:translateY(-14px);transition:opacity .3s ease,transform .3s ease;}' +
      '#ru-consent.ru-show{opacity:1;transform:translateY(0);}' +
      '#ru-consent p{margin:0;flex:1 1 320px;font-size:13px;line-height:1.55;color:rgba(255,255,255,.85);}' +
      '#ru-consent a{color:#DDFF4D;text-decoration:underline;text-underline-offset:2px;}' +
      '#ru-consent .ru-consent-actions{display:flex;gap:10px;flex:0 0 auto;}' +
      '#ru-consent button{cursor:pointer;border:0;border-radius:999px;padding:9px 18px;' +
      'font-size:13px;font-weight:700;font-family:inherit;transition:background .2s ease,color .2s ease;}' +
      '#ru-consent .ru-accept{background:#DDFF4D;color:#2a3ad8;}' +
      '#ru-consent .ru-accept:hover{background:#cbf02f;}' +
      '#ru-consent .ru-decline{background:transparent;color:rgba(255,255,255,.8);' +
      'box-shadow:inset 0 0 0 1px rgba(255,255,255,.35);}' +
      '#ru-consent .ru-decline:hover{color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.7);}' +
      'html.ru-consent-lock,body.ru-consent-lock{overflow:hidden !important;}' +
      '@media (max-width:520px){#ru-consent .ru-consent-actions{flex:1 1 100%;}' +
      '#ru-consent button{flex:1 1 auto;}}';
    var style = d.createElement('style');
    style.id = 'ru-consent-styles';
    style.appendChild(d.createTextNode(css));
    (d.getElementsByTagName('head')[0] || d.documentElement).appendChild(style);
  }

  function lockScroll(on) {
    var root = d.documentElement, body = d.body;
    if (on) { root.classList.add('ru-consent-lock'); if (body) body.classList.add('ru-consent-lock'); }
    else { root.classList.remove('ru-consent-lock'); if (body) body.classList.remove('ru-consent-lock'); }
  }

  function showBanner() {
    injectStyles();

    // full-page backdrop — blocks interaction until a choice is made
    var overlay = d.createElement('div');
    overlay.id = 'ru-consent-overlay';
    d.body.appendChild(overlay);

    var bar = d.createElement('div');
    bar.id = 'ru-consent';
    bar.setAttribute('role', 'alertdialog');
    bar.setAttribute('aria-modal', 'true');
    bar.setAttribute('aria-label', 'cookie consent');
    bar.innerHTML =
      '<p>we use cookies for analytics and advertising (including the Meta/Facebook pixel) to understand site traffic and measure our ads. ' +
      'to continue, please choose. see our <a href="/privacy.html">privacy policy</a>.</p>' +
      '<div class="ru-consent-actions">' +
      '<button class="ru-decline" type="button">decline</button>' +
      '<button class="ru-accept" type="button">accept</button>' +
      '</div>';
    d.body.appendChild(bar);

    lockScroll(true);

    // fade in
    w.requestAnimationFrame(function () {
      w.requestAnimationFrame(function () {
        overlay.classList.add('ru-show');
        bar.classList.add('ru-show');
      });
    });

    // trap focus lightly + block Escape (no dismiss without a choice)
    var acceptBtn = bar.querySelector('.ru-accept');
    if (acceptBtn && acceptBtn.focus) { try { acceptBtn.focus(); } catch (e) {} }
    function onKey(e) { if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); } }
    d.addEventListener('keydown', onKey, true);

    function dismiss() {
      d.removeEventListener('keydown', onKey, true);
      lockScroll(false);
      overlay.classList.remove('ru-show');
      bar.classList.remove('ru-show');
      w.setTimeout(function () {
        if (bar.parentNode) bar.parentNode.removeChild(bar);
        if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
      }, 300);
    }
    acceptBtn.addEventListener('click', function () {
      setConsent('accepted'); loadAnalytics(); dismiss();
    });
    bar.querySelector('.ru-decline').addEventListener('click', function () {
      setConsent('declined'); dismiss();
    });
  }

  if (d.readyState === 'loading') {
    d.addEventListener('DOMContentLoaded', showBanner);
  } else {
    showBanner();
  }
})();
