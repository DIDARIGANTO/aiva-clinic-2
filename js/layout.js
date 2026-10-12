/* ============================================================
   Общие части всех страниц: иконки, шапка, полоса с адресом,
   липкое меню, выезжающее меню, футер и кнопка WhatsApp.
   Правятся здесь один раз — и меняются на всех страницах.
   ============================================================ */
(function () {
  var TOP = `
<!-- SVG-спрайт: иконки и декоративные треугольники -->
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="12" cy="9.5" r="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/></symbol>
  <symbol id="i-phone" viewBox="0 0 24 24"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 12l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></symbol>
  <symbol id="i-insta" viewBox="0 0 24 24"><rect x="3.5" y="3.5" width="17" height="17" rx="5" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="17" cy="7" r="1" fill="currentColor"/></symbol>
  <symbol id="i-yt" viewBox="0 0 28 24"><rect x="2" y="3.5" width="24" height="17" rx="5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M11.5 8.5v7l6-3.5-6-3.5Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></symbol>
  <symbol id="i-tt" viewBox="0 0 24 24"><path d="M14 4v10.5a3.5 3.5 0 1 1-3.5-3.5M14 4c.3 2.400 1.900 4 4.500 4.300" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="i-chat" viewBox="0 0 24 24"><path d="M12 3.5a8.5 8.5 0 0 0-7.3 12.8L3.5 20.5l4.300-1.100A8.5 8.5 0 1 0 12 3.5Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></symbol>
  <symbol id="i-route" viewBox="0 0 24 24"><path d="M20.5 3.5 3.5 10.5l7 3 3 7 7-17Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></symbol>
  <symbol id="i-doc" viewBox="0 0 24 24"><path d="M7 3.500h7l4 4V20.500H7V3.500ZM14 3.500v4h4M9.500 12h6M9.500 15.500h6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/></symbol>
  <symbol id="i-arrow" viewBox="0 0 52 14"><path d="M0 7h49M43 1l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="i-chev" viewBox="0 0 24 24"><path d="m9 5 7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="tri-outline" viewBox="0 0 320 290"><path d="M34 62 L286 22 Q304 20 300 38 L236 262 Q230 280 216 268 L26 92 Q14 68 34 62 Z" fill="none" stroke="currentColor" stroke-width="12" stroke-linejoin="round"/></symbol>
  <symbol id="tri-thin" viewBox="0 0 320 290"><path d="M24 58 L296 26 L214 272 Z" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/></symbol>
  <symbol id="tri-solid" viewBox="0 0 100 100"><path d="M12 16 L88 8 Q96 8 93 16 L66 88 Q62 96 56 90 L8 26 Q4 18 12 16 Z" fill="currentColor"/></symbol>
  <symbol id="tri-pattern" viewBox="0 0 520 520">
    <g fill="currentColor">
      <path d="M40 60 L200 40 L150 190 Z" opacity=".9"/><path d="M215 45 L330 150 L165 195 Z" opacity=".55"/>
      <path d="M345 30 L490 80 L350 140 Z" opacity=".8"/><path d="M360 160 L500 100 L470 260 Z" opacity=".6"/>
      <path d="M30 210 L150 205 L70 330 Z" opacity=".6"/><path d="M170 210 L340 170 L250 330 Z" opacity=".85"/>
      <path d="M270 345 L355 180 L455 280 Z" opacity=".5"/><path d="M60 350 L235 345 L120 490 Z" opacity=".8"/>
      <path d="M255 360 L450 300 L380 480 Z" opacity=".7"/><path d="M140 500 L245 370 L360 495 Z" opacity=".45"/>
    </g>
  </symbol>
</svg>

<!-- ============ ШАПКА ============ -->
<header class="topbar" id="top">
  <a class="logo" href="index.html"><img src="img/logo.png" alt="AIVA CLINIC" width="854" height="211"></a>

  <a class="top-info top-info-addr" href="contacts.html">
    <svg class="top-ico"><use href="#i-pin"/></svg>
    <span><strong data-bind="address">Астана, ул. Е 669, 13</strong><u>Контакты и схема проезда</u></span>
  </a>
  <a class="top-info" data-href="phoneHref" href="tel:+77472274096">
    <svg class="top-ico"><use href="#i-phone"/></svg>
    <span><strong data-bind="phone">+7 (747) 227-40-96</strong><small data-bind="hoursShort">Ежедневно с 08:00 до 20:00</small></span>
  </a>

  <a class="btn btn-grad btn-sm top-cta" data-href="whatsappHref" href="https://wa.me/77472274096" target="_blank" rel="noopener">Записаться на прием</a>

  <div class="top-social">
    <a class="soc-btn" data-href="instagramHref" href="https://www.instagram.com/aiva.clinic_astana" target="_blank" rel="noopener" aria-label="Instagram"><svg><use href="#i-insta"/></svg></a>
    <a class="soc-btn soc-btn-wide" data-href="youtubeHref" href="https://www.youtube.com/channel/UC1EBxPu6hds8KHRhQzTv8gw" target="_blank" rel="noopener" aria-label="YouTube"><svg><use href="#i-yt"/></svg></a>
  </div>

  <button class="burger" type="button" aria-label="Меню" data-menu-open><span></span><span></span><span></span></button>
</header>

<!-- Полоса с адресом и лицензией -->
<div class="branchbar">
  <strong class="branchbar-title">Найти клинику на карте</strong>
  <div class="branchbar-item">
    <span data-bind="address">Астана, ул. Е 669, 13</span>
  </div>
  <div class="branchbar-item">
    <span data-bind="license">Лицензия № 24026583, ДКМФК МЗ РК по г. Астана</span>
  </div>
  <a class="branchbar-all" href="contacts.html">Все контакты →</a>
</div>

<!-- Липкое меню (появляется при прокрутке) -->
<div class="stickynav">
  <a class="logo" href="index.html"><img src="img/logo.png" alt="AIVA CLINIC" width="854" height="211"></a>
  <nav>
    <a href="about.html">О клинике</a>
    <a href="prices.html">Прайс-лист</a>
    <a href="doctors.html">Наши врачи</a>
    <a href="reviews.html">Отзывы</a>
    <a href="offers.html">Акции</a>
    <a href="contacts.html">Контакты</a>
  </nav>
  <button class="burger" type="button" aria-label="Меню" data-menu-open><span></span><span></span><span></span></button>
</div>

<!-- Выезжающее меню -->
<div class="menu" aria-hidden="true">
  <div class="menu-backdrop" data-menu-close></div>
  <aside class="menu-panel">
    <img class="menu-ornament" src="img/favicon.png" alt="" aria-hidden="true">
    <button class="menu-close" type="button" aria-label="Закрыть" data-menu-close></button>
    <nav>
      <a href="about.html">О клинике</a>
      <a href="prices.html">Прайс-лист</a>
      <a href="doctors.html">Наши врачи</a>
      <a href="reviews.html">Отзывы</a>
      <a href="offers.html">Акции</a>
      <a href="contacts.html">Контакты</a>
    </nav>
    <div class="menu-footer">
      <p class="menu-slogan">Помогаем вернуться к активной жизни.<br>© AIVA CLINIC</p>
      <p class="menu-contact"><a data-href="phoneHref" href="tel:+77472274096" data-bind="phone">+7 (747) 227-40-96</a><span data-bind="hoursShort">Ежедневно с 08:00 до 20:00</span><span data-bind="address">Астана, ул. Е 669, 13</span></p>
      <div class="menu-soc">
        <a data-href="instagramHref" href="https://www.instagram.com/aiva.clinic_astana" target="_blank" rel="noopener" aria-label="Instagram"><svg><use href="#i-insta"/></svg></a>
        <a data-href="tiktokHref" href="https://www.tiktok.com/@aiva.clinic" target="_blank" rel="noopener" aria-label="TikTok"><svg><use href="#i-tt"/></svg></a>
        <a data-href="youtubeHref" href="https://www.youtube.com/channel/UC1EBxPu6hds8KHRhQzTv8gw" target="_blank" rel="noopener" aria-label="YouTube"><svg viewBox="0 0 28 24"><use href="#i-yt"/></svg></a>
      </div>
      <a class="menu-btn" data-href="whatsappHref" href="https://wa.me/77472274096" target="_blank" rel="noopener">WhatsApp</a>
      <a class="menu-btn" data-href="gisReviewsHref" href="https://2gis.kz/astana/firm/70000001090259641/tab/reviews" target="_blank" rel="noopener">Оценить работу</a>
    </div>
  </aside>
</div>
`;
  var BOTTOM = `
<!-- ============ ФУТЕР ============ -->
<footer class="footer">
  <div class="container container-narrow footer-grid">
    <div class="footer-brand">
      <a class="logo logo-light" href="index.html"><img src="img/logo-white.png" alt="AIVA CLINIC" width="854" height="211"></a>
      <p data-bind="tagline">клиника терапии, физиотерапии и реабилитации</p>
      <div class="footer-soc">
        <a data-href="instagramHref" href="https://www.instagram.com/aiva.clinic_astana" target="_blank" rel="noopener" aria-label="Instagram"><svg><use href="#i-insta"/></svg></a>
        <a data-href="youtubeHref" href="#" target="_blank" rel="noopener" aria-label="YouTube"><svg viewBox="0 0 28 24"><use href="#i-yt"/></svg></a>
        <a data-href="tiktokHref" href="https://www.tiktok.com/@aiva.clinic" target="_blank" rel="noopener" aria-label="TikTok"><svg><use href="#i-tt"/></svg></a>
      </div>
      <small data-bind="license">Лицензия № 24026583, ДКМФК МЗ РК по г. Астана</small>
      <small>Имеются противопоказания. Необходима консультация специалиста.</small>
      <small>© <span data-bind="year">2026</span> AIVA CLINIC. Все права защищены</small>
    </div>
    <div><h4>Основное</h4><a href="index.html">Главная</a><a href="about.html">О клинике</a><a href="prices.html">Прайс-лист</a></div>
    <div><h4>Клиника</h4><a href="doctors.html">Наши врачи</a><a href="offers.html">Акции</a><a href="reviews.html">Отзывы о клинике</a><a href="contacts.html">Контакты</a></div>
    <div><h4>Услуги</h4><a href="prices.html#svc-diag">Консультация и диагностика</a><a href="prices.html#svc-iv">IV и интегративная терапия</a><a href="prices.html#svc-physio">Физиотерапия</a><a href="prices.html#svc-rehab">Реабилитация и восстановление</a></div>
  </div>
</footer>

<!-- Плавающая кнопка WhatsApp -->
<a class="wa-float" data-href="whatsappHref" href="https://wa.me/77472274096" target="_blank" rel="noopener" aria-label="WhatsApp"><svg><use href="#i-chat"/></svg></a>
`;
  document.body.insertAdjacentHTML('afterbegin', TOP);
  document.body.insertAdjacentHTML('beforeend', BOTTOM);

  // подсветка текущей страницы в меню
  var page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.stickynav nav a, .menu nav a').forEach(function (a) {
    if (a.getAttribute('href') === page) a.classList.add('is-active');
  });
})();
