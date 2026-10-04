(function () {
  'use strict';

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  /* ---------- Подстановка данных из js/config.js ---------- */
  function lookup(path) {
    return path.split('.').reduce(function (obj, key) { return obj == null ? undefined : obj[key]; }, window.SITE || {});
  }
  $$('[data-bind]').forEach(function (el) {
    var value = lookup(el.dataset.bind);
    if (value != null) el.textContent = value;
  });
  $$('[data-href]').forEach(function (el) {
    var value = lookup(el.dataset.href);
    if (value) el.setAttribute('href', value);
  });

  /* ---------- Появление блоков при прокрутке ---------- */
  if ('IntersectionObserver' in window) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        revealObserver.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    $$('.reveal').forEach(function (el, i) {
      // карточки в одном ряду появляются с небольшой задержкой друг за другом
      if (el.matches('.card, .rating')) el.style.transitionDelay = (i % 3) * 0.12 + 's, ' + (i % 3) * 0.12 + 's, 0s';
      revealObserver.observe(el);
    });

    // покачивание фигур: каждый раз, когда элемент входит в экран
    var rockObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { entry.target.classList.toggle('in-view', entry.isIntersecting); });
    }, { threshold: 0.3 });
    $$('.rock').forEach(function (el) { rockObserver.observe(el); });
  } else {
    $$('.reveal').forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- Смена фото на главном экране ---------- */
  (function () {
    var slides = $$('.hero-slide');
    if (slides.length < 2) return;
    var index = 0;
    setInterval(function () {
      var current = slides[index];
      index = (index + 1) % slides.length;
      var next = slides[index];
      current.classList.remove('is-active');
      current.classList.add('is-leaving');
      next.classList.add('is-active');
      setTimeout(function () {
        // возвращаем ушедший слайд направо без анимации
        current.style.transition = 'none';
        current.classList.remove('is-leaving');
        current.offsetWidth; // reflow
        current.style.transition = '';
      }, 700);
    }, 4000);
  })();

  /* ---------- Липкое меню ---------- */
  (function () {
    var nav = $('.stickynav');
    if (!nav) return;
    var onScroll = function () {
      var visible = window.scrollY > 160;
      nav.classList.toggle('is-visible', visible);
      nav.setAttribute('aria-hidden', String(!visible));
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  })();

  /* ---------- Выезжающее меню ---------- */
  (function () {
    var menu = $('.menu');
    if (!menu) return;
    var setOpen = function (open) {
      menu.classList.toggle('is-open', open);
      menu.setAttribute('aria-hidden', String(!open));
      document.body.style.overflow = open ? 'hidden' : '';
    };
    $$('[data-menu-open]').forEach(function (btn) { btn.addEventListener('click', function () { setOpen(true); }); });
    $$('[data-menu-close], .menu nav a').forEach(function (el) { el.addEventListener('click', function () { setOpen(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
  })();

  /* ---------- «О нас»: переключатель с фото ---------- */
  $$('[data-about]').forEach(function (root) {
    var items = $$('[data-about-item]', root);
    var photos = $$('.about-photos img', root);
    var activate = function (i) {
      items.forEach(function (el, n) { el.classList.toggle('is-active', n === i); });
      photos.forEach(function (el, n) { el.classList.toggle('is-active', n === i); });
    };
    items.forEach(function (el, i) {
      el.addEventListener('click', function () { activate(i); });
      el.addEventListener('mouseenter', function () { activate(i); });
    });
  });

  /* ---------- Слайдер отзывов ---------- */
  $$('[data-slider]').forEach(function (root) {
    var track = $('.rs-track', root);
    var count = track.children.length;
    var index = 0;
    var go = function (i) {
      index = (i + count) % count;
      track.style.transform = 'translateX(' + (-100 * index) + '%)';
    };
    $('.rs-prev', root).addEventListener('click', function () { go(index - 1); });
    $('.rs-next', root).addEventListener('click', function () { go(index + 1); });

    // свайп на телефоне
    var startX = null;
    track.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
    track.addEventListener('touchend', function (e) {
      if (startX === null) return;
      var dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 40) go(index + (dx < 0 ? 1 : -1));
      startX = null;
    });
  });

  /* ---------- Аккордеон ---------- */
  $$('[data-accordion] .acc-head').forEach(function (head) {
    head.addEventListener('click', function () { head.parentElement.classList.toggle('is-open'); });
  });

  /* ---------- Вкладки ---------- */
  $$('[data-tabs]').forEach(function (root) {
    var buttons = $$('.tabs-head button', root);
    var panes = $$('.tab-pane', root);
    buttons.forEach(function (btn, i) {
      btn.addEventListener('click', function () {
        buttons.forEach(function (b, n) { b.classList.toggle('is-active', n === i); });
        panes.forEach(function (p, n) { p.classList.toggle('is-active', n === i); });
      });
    });
  });
})();
