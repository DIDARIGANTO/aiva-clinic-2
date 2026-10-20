/* ============================================================
   Переключение языка KZ / RU.
   Переводы лежат в js/i18n-kz.js (словарь window.KZ: русский текст → казахский).
   Выбор запоминается в браузере; при KZ все тексты страницы,
   подписи к картинкам, заголовок вкладки и описание подменяются.
   ============================================================ */
(function () {
  var LANG_KEY = 'aiva-lang';
  var params = new URLSearchParams(location.search);
  if (params.get('lang')) {
    try { localStorage.setItem(LANG_KEY, params.get('lang')); } catch (e) {}
    history.replaceState(null, '', location.pathname + location.hash);
  }
  var lang = 'ru';
  try { lang = localStorage.getItem(LANG_KEY) || 'ru'; } catch (e) {}

  // кнопки KZ / RU в шапке
  document.querySelectorAll('[data-lang-pick]').forEach(function (b) {
    b.classList.toggle('is-active', b.dataset.langPick === lang);
    b.addEventListener('click', function () {
      try { localStorage.setItem(LANG_KEY, b.dataset.langPick); } catch (e) {}
      location.href = location.pathname + location.hash;
    });
  });

  if (lang !== 'kz' || !window.KZ) return;
  var D = window.KZ;
  var tr = function (s) {
    var m = s.match(/^(\s*)([\s\S]*?)(\s*)$/);
    var key = m[2].replace(/\s+/g, ' ');
    return D.hasOwnProperty(key) ? m[1] + D[key] + m[3] : null;
  };

  document.documentElement.lang = 'kk';
  var t = tr(document.title); if (t) document.title = t;
  var meta = document.querySelector('meta[name="description"]');
  if (meta) { t = tr(meta.content); if (t) meta.content = t; }

  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode: function (n) {
      var p = n.parentNode && n.parentNode.nodeName;
      return (p === 'SCRIPT' || p === 'STYLE' || !/\S/.test(n.nodeValue)) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
    }
  });
  var nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(function (n) { var v = tr(n.nodeValue); if (v !== null) n.nodeValue = v; });

  ['alt', 'title', 'aria-label', 'placeholder'].forEach(function (a) {
    document.querySelectorAll('[' + a + ']').forEach(function (el) {
      var v = tr(el.getAttribute(a)); if (v !== null) el.setAttribute(a, v);
    });
  });
})();
