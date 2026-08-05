/* =========================================================================
   rallyup.team — cookie consent + Swan analytics loader
   -------------------------------------------------------------------------
   Swan is only loaded AFTER the visitor accepts. The choice is remembered
   in localStorage so the banner shows once. Declining prevents Swan from
   ever loading for that visitor.
   ========================================================================= */
(function () {
  var w = window, d = document;
  var CONSENT_KEY = 'ru.cookieConsent';   // 'accepted' | 'declined'
  var SWAN_PK = 'cmevnk77u0005l70537an0s07';

  /* ---- Swan analytics loader (fires only with consent) ---- */
  function loadSwan() {
    var swan = (w.swan = w.swan || []);
    if (swan.isLoaded) return;
    swan.isLoaded = true;
    swan.pk = SWAN_PK;
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
    var s = d.createElement('script');
    s.type = 'text/javascript';
    s.async = true;
    s.src = 'https://script.getswan.com?pk=' + SWAN_PK + '&sid=' + encodeURIComponent(sid);
    if (swan.eId) { s.src += '&eId=' + encodeURIComponent(swan.eId); }
    (d.getElementsByTagName('head')[0] || d.documentElement).appendChild(s);
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
  if (choice === 'accepted') { loadSwan(); return; }
  if (choice === 'declined') { return; }

  /* ---- otherwise show the banner ---- */
  function injectStyles() {
    if (d.getElementById('ru-consent-styles')) return;
    var css =
      '#ru-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483000;' +
      'max-width:760px;margin:0 auto;background:#2a3ad8;color:#fff;border-radius:16px;' +
      'box-shadow:0 18px 50px rgba(30,58,138,.35);padding:18px 20px;' +
      'font-family:inherit;display:flex;flex-wrap:wrap;align-items:center;gap:14px 18px;' +
      'opacity:0;transform:translateY(12px);transition:opacity .3s ease,transform .3s ease;}' +
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
      '@media (max-width:520px){#ru-consent .ru-consent-actions{flex:1 1 100%;}' +
      '#ru-consent button{flex:1 1 auto;}}';
    var style = d.createElement('style');
    style.id = 'ru-consent-styles';
    style.appendChild(d.createTextNode(css));
    (d.getElementsByTagName('head')[0] || d.documentElement).appendChild(style);
  }

  function showBanner() {
    injectStyles();
    var bar = d.createElement('div');
    bar.id = 'ru-consent';
    bar.setAttribute('role', 'dialog');
    bar.setAttribute('aria-label', 'cookie consent');
    bar.innerHTML =
      '<p>we use cookies and analytics (including Swan) to understand site traffic and improve rallyup. ' +
      'see our <a href="/privacy.html">privacy policy</a>.</p>' +
      '<div class="ru-consent-actions">' +
      '<button class="ru-decline" type="button">decline</button>' +
      '<button class="ru-accept" type="button">accept</button>' +
      '</div>';
    d.body.appendChild(bar);
    // fade in
    w.requestAnimationFrame(function () {
      w.requestAnimationFrame(function () { bar.classList.add('ru-show'); });
    });

    function dismiss() {
      bar.classList.remove('ru-show');
      w.setTimeout(function () { if (bar.parentNode) bar.parentNode.removeChild(bar); }, 300);
    }
    bar.querySelector('.ru-accept').addEventListener('click', function () {
      setConsent('accepted'); loadSwan(); dismiss();
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
