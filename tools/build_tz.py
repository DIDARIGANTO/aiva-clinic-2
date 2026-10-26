# -*- coding: utf-8 -*-
"""Сборка страниц сайта по ТЗ («Сайт структура.pdf»).

Запуск:  python3 tools/build_tz.py
Пишет:   index.html, about.html, doctors.html, prices.html, offers.html,
         business.html, contacts.html и js/layout.js (общая шапка/меню/футер).
Тексты правятся здесь; блоки главного экрана, врачей, прайса и контактов — в tools/src/.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
V = '?v=24'

WA = 'https://wa.me/77472274096'
PHONE = '+7 (747) 227-40-96'
TEL = 'tel:+77472274096'
GIS = 'https://2gis.kz/astana/search/%D1%84%D1%88%D0%BC%D1%84/firm/70000001090259641?m=71.482275%2C51.082042%2F14.72&immersive=on'
GIS_REV = 'https://2gis.kz/astana/firm/70000001090259641/tab/reviews'
YA = 'https://yandex.kz/maps/ru/org/aiva_clinic/132063384129/?ll=71.481355%2C51.087490&z=16.63'
GMAPS = 'https://www.google.com/maps/search/AIVA+Clinic+%D0%90%D1%81%D1%82%D0%B0%D0%BD%D0%B0'
INSTA = 'https://www.instagram.com/aiva.clinic_astana'
YT = 'https://www.youtube.com/channel/UC1EBxPu6hds8KHRhQzTv8gw'
TT = 'https://www.tiktok.com/@aiva.clinic'
# пока презентаций нет — кнопки «Скачать» ведут в WhatsApp с готовым запросом
def wa_text(t):
    from urllib.parse import quote
    return WA + '?text=' + quote(t)

wa_btn = lambda label, cls='btn btn-grad btn-lg glow': f'<a class="{cls}" data-href="whatsappHref" href="{WA}" target="_blank" rel="noopener">{label}</a>'
ext = 'target="_blank" rel="noopener"'

# ---------------------------------------------------------------- общие части
SPRITE = open('js/layout.js', encoding='utf-8').read()
SPRITE = SPRITE[SPRITE.index('<!-- SVG-спрайт'):SPRITE.index('</svg>') + len('</svg>')]

NAV_ITEMS = [('index.html', 'Главная'), ('about.html', 'О клинике'), ('doctors.html', 'Врачи'),
             ('prices.html', 'Прайс'), ('offers.html', 'Акции'), ('business.html', 'Для бизнеса')]
nav = lambda ind: '\n'.join(f'{ind}<a href="{h}">{t}</a>' for h, t in NAV_ITEMS)

HEADER = f'''<!-- ============ ШАПКА (по ТЗ: лого, адрес + 2ГИС, график, соцсети, KZ/RU, меню) ============ -->
<header class="topbar" id="top">
  <a class="logo" href="index.html"><img src="img/logo.png" alt="AIVA CLINIC" width="854" height="211"></a>

  <a class="top-info top-info-addr" href="{GIS}" data-href="gisHref" {ext}>
    <svg class="top-ico"><use href="#i-pin"/></svg>
    <span><strong data-bind="address">Астана, ул. Е 669, 13</strong><u>Открыть в 2ГИС</u></span>
  </a>
  <a class="top-info" href="contacts.html">
    <svg class="top-ico"><use href="#i-clock"/></svg>
    <span><strong>График работы</strong><small data-bind="hoursShort">08:00–20:00, ежедневно</small></span>
  </a>

  <div class="top-social">
    <a class="soc-btn" data-href="instagramHref" href="{INSTA}" {ext} aria-label="Instagram"><svg><use href="#i-insta"/></svg></a>
    <a class="soc-btn soc-btn-wide" data-href="youtubeHref" href="{YT}" {ext} aria-label="YouTube"><svg><use href="#i-yt"/></svg></a>
  </div>

  <div class="lang" data-lang>
    <button type="button" data-lang-pick="kz">KZ</button><span>/</span><button type="button" data-lang-pick="ru">RU</button>
  </div>

  <button class="burger" type="button" aria-label="Меню" data-menu-open><span></span><span></span><span></span></button>
</header>

<!-- Строка меню -->
<div class="stickynav">
  <a class="logo" href="index.html"><img src="img/logo.png" alt="AIVA CLINIC" width="854" height="211"></a>
  <nav>
{nav('    ')}
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
{nav('      ')}
      <a href="contacts.html">Контакты</a>
    </nav>
    <div class="menu-footer">
      <p class="menu-slogan">Помогаем вернуться к активной жизни.<br>© AIVA CLINIC</p>
      <p class="menu-contact"><a data-href="phoneHref" href="{TEL}" data-bind="phone">{PHONE}</a><span data-bind="hoursShort">08:00–20:00, ежедневно</span><span data-bind="address">Астана, ул. Е 669, 13</span></p>
      <div class="menu-soc">
        <a data-href="instagramHref" href="{INSTA}" {ext} aria-label="Instagram"><svg><use href="#i-insta"/></svg></a>
        <a data-href="tiktokHref" href="{TT}" {ext} aria-label="TikTok"><svg><use href="#i-tt"/></svg></a>
        <a data-href="youtubeHref" href="{YT}" {ext} aria-label="YouTube"><svg viewBox="0 0 28 24"><use href="#i-yt"/></svg></a>
      </div>
      <a class="menu-btn" data-href="whatsappHref" href="{WA}" {ext}>WhatsApp</a>
      <a class="menu-btn" data-href="gisReviewsHref" href="{GIS_REV}" {ext}>Оценить работу</a>
    </div>
  </aside>
</div>
'''

FOOTER = f'''<!-- ============ ФУТЕР ============ -->
<footer class="footer">
  <div class="container container-narrow footer-grid">
    <div class="footer-brand">
      <a class="logo logo-light" href="index.html"><img src="img/logo-white.png" alt="AIVA CLINIC" width="854" height="211"></a>
      <p data-bind="tagline">клиника терапии, физиотерапии и реабилитации</p>
      <div class="footer-soc">
        <a data-href="instagramHref" href="{INSTA}" {ext} aria-label="Instagram"><svg><use href="#i-insta"/></svg></a>
        <a data-href="youtubeHref" href="{YT}" {ext} aria-label="YouTube"><svg viewBox="0 0 28 24"><use href="#i-yt"/></svg></a>
        <a data-href="tiktokHref" href="{TT}" {ext} aria-label="TikTok"><svg><use href="#i-tt"/></svg></a>
      </div>
      <small data-bind="license">Лицензия № 24026583, ДКМФК МЗ РК по г. Астана</small>
      <small>Имеются противопоказания. Необходима консультация специалиста.</small>
      <small>© <span data-bind="year">2026</span> AIVA CLINIC. Все права защищены</small>
    </div>
    <div><h4>Основное</h4><a href="index.html">Главная</a><a href="about.html">О клинике</a><a href="doctors.html">Врачи</a><a href="prices.html">Прайс</a></div>
    <div><h4>Клиника</h4><a href="offers.html">Акции</a><a href="business.html">Для бизнеса</a><a href="index.html#reviews">Отзывы о клинике</a><a href="contacts.html">Контакты</a></div>
    <div><h4>Услуги</h4><a href="prices.html#svc-diag">Консультация и диагностика</a><a href="prices.html#svc-iv">IV и интегративная терапия</a><a href="prices.html#svc-physio">Физиотерапия</a><a href="prices.html#svc-rehab">Реабилитация и восстановление</a></div>
  </div>
</footer>

<!-- Плавающая кнопка WhatsApp -->
<a class="wa-float" data-href="whatsappHref" href="{WA}" {ext} aria-label="WhatsApp"><svg><use href="#i-chat"/></svg></a>'''

layout_js = '''/* ============================================================
   Общие части всех страниц: иконки, шапка, строка меню,
   выезжающее меню, футер и кнопка WhatsApp.
   Собирается скриптом tools/build_tz.py — правьте там.
   ============================================================ */
(function () {
  var TOP = `
''' + SPRITE + '\n\n' + HEADER + '''`;
  var BOTTOM = `
''' + FOOTER + '''
`;
  document.body.insertAdjacentHTML('afterbegin', TOP);
  document.body.insertAdjacentHTML('beforeend', BOTTOM);

  // подсветка текущей страницы в меню
  var page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.stickynav nav a, .menu nav a').forEach(function (a) {
    if (a.getAttribute('href') === page) a.classList.add('is-active');
  });
})();
'''
assert '${' not in layout_js and layout_js.count('`') == 4
open('js/layout.js', 'w', encoding='utf-8').write(layout_js)

# ---------------------------------------------------------------- блоки
def social(extra_cls=''):
    return f'''<!-- ============ СОЦИАЛЬНЫЕ СЕТИ (по ТЗ, на каждой странице) ============ -->
<section class="section social-tz {extra_cls}">
  <div class="container container-narrow">
    <p class="eyebrow reveal">Социальные сети</p>
    <h2 class="h2 h2-sm reveal">Следите за нами <br>в Instagram и YouTube</h2>
    <p class="teaser-text reveal">Подпишитесь, чтобы не пропустить специальные предложения, бесплатные процедуры, новости клиники и полезные видео от наших врачей.</p>
    <div class="soc-tiles">
      <a class="soc-tile reveal" data-href="instagramHref" href="{INSTA}" {ext}><svg><use href="#i-insta"/></svg><strong>Instagram</strong><small>@aiva.clinic_astana</small><span class="btn btn-grad btn-sm">Подписаться</span></a>
      <a class="soc-tile reveal" data-href="youtubeHref" href="{YT}" {ext}><svg viewBox="0 0 28 24"><use href="#i-yt"/></svg><strong>YouTube</strong><small>AIVA CLINIC</small><span class="btn btn-grad btn-sm">Подписаться</span></a>
    </div>
  </div>
</section>

'''

RATING = f'''<!-- ============ РЕЙТИНГ И ОТЗЫВЫ (по ТЗ) ============ -->
<section class="section teaser-gray" id="reviews">
  <div class="container container-narrow">
    <p class="eyebrow reveal">Наш рейтинг и отзывы</p>
    <h2 class="h2 h2-sm reveal">Нам доверяют пациенты</h2>
    <p class="teaser-text reveal">Прочитайте реальные отзывы и оцените нас на картах. Ваше мнение помогает нам становиться лучше!</p>
    <div class="ratings">
      <a class="rating reveal" data-href="gisReviewsHref" href="{GIS_REV}" {ext}><span class="rating-logo">2<i class="c-gis">GIS</i></span><p><b>4.7</b> из 5</p><u>читать отзывы в 2ГИС</u></a>
      <a class="rating reveal" data-href="yandexHref" href="{YA}" {ext}><span class="rating-logo"><i class="c-ya">Я</i>ндекс Карты</span><strong>Оставьте отзыв</strong><u>оценить на Яндекс Картах</u></a>
      <a class="rating reveal" href="{GMAPS}" {ext}><span class="rating-logo"><i class="c-google">Google</i> Maps</span><strong>Оставьте отзыв</strong><u>оценить в Google Maps</u></a>
    </div>
  </div>
</section>

'''

EXO_PROMO = f'''<!-- ============ АКЦИЯ: ЭКЗОМАССАЖ (по ТЗ) ============ -->
<section class="section exo-promo">
  <div class="container container-narrow">
    <div class="exo-card reveal">
      <p class="eyebrow eyebrow-left">Акция</p>
      <h2>Попробуйте экзомассаж бесплатно!</h2>
      <p>Первая процедура в AIVA Clinic — в подарок. Всего 10 минут, без прикосновений и усилий: вы просто лежите, а аппарат делает всю работу.</p>
      {wa_btn('Записаться')}
    </div>
  </div>
</section>

'''

HELP_DOCTOR = f'''<!-- ============ НЕ ЗНАЕТЕ, К КАКОМУ ВРАЧУ ОБРАТИТЬСЯ ============ -->
<section class="section promo">
  <div class="container">
    <div class="promo-card reveal">
      <div class="zoom promo-img"><img loading="lazy" src="img/promo.jpg" alt="Боль в спине — повод обратиться к врачу"></div>
      <div class="promo-body">
        <h2>Не знаете, к какому врачу обратиться?</h2>
        <p>Поможем выбрать специалиста. На приёме врач <strong>выслушает жалобы</strong> и определит, какие обследования необходимы.</p>
        <p>Свяжитесь с администратором — подберём специалиста и удобное время для консультации.</p>
        {wa_btn('Помогите выбрать врача')}
      </div>
    </div>
  </div>
</section>

'''

def poster_block(img, alt, eyebrow, title, text, bullets, cta_label, second=None, sid=''):
    b = ''.join(f'        <li>{x}</li>\n' for x in bullets)
    second_html = f'\n        <a class="btn btn-light btn-lg" href="{second[1]}">{second[0]}</a>' if second else ''
    return f'''<section class="section poster-section" {('id="%s"' % sid) if sid else ''}>
  <div class="container">
    <div class="poster-card reveal">
      <div class="zoom poster-img"><img loading="lazy" src="img/{img}" alt="{alt}"></div>
      <div class="poster-body">
        <p class="eyebrow eyebrow-left">{eyebrow}</p>
        <h2>{title}</h2>
        <p>{text}</p>
        <ul class="offer-list">
{b}        </ul>
        <div class="poster-btns">{wa_btn(cta_label, 'btn btn-grad btn-lg glow')}{second_html}</div>
      </div>
    </div>
  </div>
</section>

'''

LIVER = dict(img='promo-liver.jpg', alt='Чек-ап печени 8 в 1 за 23 000 ₸', eyebrow='Акция', title='Чек-ап печени «8 в 1» — 23 000 ₸ <s>34 900 ₸</s>',
             text='Комплексная проверка печени за один визит в AIVA Clinic. Приём врача — в подарок.',
             bullets=['общий анализ крови', 'АЛТ, АСТ, ГГТП', 'глюкоза крови', 'общий холестерин', 'УЗИ органов брюшной полости', 'приём врача — в подарок'])
DRIP = dict(img='promo-drip.jpg', alt='Капельницы — скидка 30% до конца месяца', eyebrow='Акция', title='Капельницы — скидка 30% до конца месяца',
            text='Специальные цены на популярные программы IV-терапии. Состав и показания подберёт врач на консультации.',
            bullets=['восстановление и энергия', 'иммунитет и детокс', 'красота и антиэйдж', 'индивидуальные программы по назначению врача'])

# ---------------------------------------------------------------- страницы
HEAD = '''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="img/favicon.png">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AIVA CLINIC">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}img/hero-1.jpg">
<meta property="og:locale" content="ru_RU">
<script type="application/ld+json">{ldjson}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css{v}">
<script>document.documentElement.classList.add('js')</script>
</head>
<body class="{cls}">

<main>

'''
TAIL = '''</main>

<script src="js/config.js{v}"></script>
<script src="js/layout.js{v}"></script>
<script src="js/main.js{v}"></script>
<script src="js/i18n-kz.js{v}"></script>
<script src="js/i18n.js{v}"></script>
</body>
</html>
'''
SITE = 'https://didariganto.github.io/aiva-clinic-2/'
# Schema.org: медицинская организация (адрес, телефон, часы, профили) — читается Google, Яндексом и ИИ-поиском
import json as _json
ORG = {
    "@context": "https://schema.org", "@type": "MedicalClinic", "name": "AIVA Clinic",
    "alternateName": "AIVA CLINIC Астана", "url": SITE, "logo": SITE + "img/logo.png", "image": SITE + "img/hero-1.jpg",
    "description": "Клиника терапии, физиотерапии и реабилитации в Астане: консультации врачей, УЗИ-диагностика, чек-апы, IV-терапия, аппаратная физиотерапия, экзотерапия, ЛФК и лечебный массаж.",
    "telephone": "+77472274096", "email": "aivaclinic01@gmail.com",
    "address": {"@type": "PostalAddress", "streetAddress": "ул. Е 669, 13", "addressLocality": "Астана", "addressCountry": "KZ"},
    "geo": {"@type": "GeoCoordinates", "latitude": 51.08749, "longitude": 71.481355},
    "hasMap": YA,
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "08:00", "closes": "20:00"}],
    "medicalSpecialty": ["Physiotherapy", "Endocrinology", "Gastroenterology", "Urology", "Musculoskeletal"],
    "availableService": [{"@type": "MedicalTherapy", "name": n} for n in ["TECAR-терапия", "Ударно-волновая терапия", "Ультразвуковая терапия", "Магнитотерапия", "Прессотерапия", "Экзотерапия (экзомассаж)", "Лечебная физкультура (ЛФК)", "Лечебный массаж", "IV-терапия (капельницы)"]]
                        + [{"@type": "MedicalTest", "name": "Ультразвуковая диагностика (УЗИ)"}, {"@type": "MedicalTest", "name": "Чек-ап программы"}],
    "sameAs": [INSTA, YT, TT, GIS, YA],
    "areaServed": {"@type": "City", "name": "Астана"}, "currenciesAccepted": "KZT", "inLanguage": ["ru", "kk"]
}
LDJSON = _json.dumps(ORG, ensure_ascii=False)

def page(fname, title, desc, body, cls='page-inner'):
    canonical = SITE if fname == 'index.html' else SITE + fname
    html = HEAD.format(title=title, desc=desc, v=V, cls=cls, canonical=canonical, site=SITE, ldjson=LDJSON) + body + TAIL.format(v=V)
    open(fname, 'w', encoding='utf-8').write(html)
    print('wrote', fname, len(html) // 1024, 'KB')

# ---- Главная
GROUPS = [('svc-diag', 'Консультация и диагностика', ['Консультации врачей', 'Анализы', 'Все виды УЗИ', 'Процедурный кабинет', 'Чек-апы']),
          ('svc-iv', 'IV и интегративная терапия', ['IV-терапия (капельницы)', 'Экзоводород', 'Лимфотропная терапия', 'Пептидная терапия', 'Плазматерапия']),
          ('svc-physio', 'Физиотерапия', ['TECAR-терапия', 'Прессотерапия', 'Ударно-волновая терапия', 'Ультразвуковая терапия', 'Магнитотерапия', 'Инфракрасная терапия']),
          ('svc-rehab', 'Реабилитация и восстановление', ['Экзотерапия', 'ЛФК', 'Лечебный массаж', 'Реабилитация'])]
groups_html = ''.join(f'''      <a class="svc-group reveal" href="prices.html#{gid}">
        <h3>{title}</h3>
        <ol>
{''.join(f'          <li>{x}</li>{chr(10)}' for x in items)}        </ol>
        <span>Смотреть в прайсе →</span>
      </a>
''' for gid, title, items in GROUPS)

hero = open('tools/src/hero.html', encoding='utf-8').read()
assert 'Написать в WhatsApp' in hero and 'prices.html' in hero

home = hero + f'''<!-- ============ НАШИ УСЛУГИ (структура по ТЗ) ============ -->
<section class="section teaser-gray" id="services">
  <div class="container">
    <p class="eyebrow reveal">Наши услуги</p>
    <h2 class="h2 reveal">Четыре направления <br>AIVA CLINIC</h2>
    <div class="svc-groups">
{groups_html}    </div>
    <div class="center reveal"><a class="btn btn-grad btn-lg glow" href="prices.html">Открыть прайс</a> <a class="btn btn-light btn-lg" href="{wa_text('Здравствуйте! Пришлите, пожалуйста, презентацию клиники AIVA CLINIC.')}" {ext}>Презентация клиники</a></div>
  </div>
</section>

''' + HELP_DOCTOR + poster_block(**LIVER, cta_label='Написать в WhatsApp', second=('Другие акции', 'offers.html'), sid='offer-liver') + social() + RATING
page('index.html', 'AIVA CLINIC — клиника терапии, физиотерапии и реабилитации в Астане',
     'AIVA CLINIC в Астане: консультации врачей, УЗИ-диагностика, чек-апы, IV-терапия, физиотерапия и реабилитация. Ежедневно с 08:00 до 20:00, ул. Е 669, 13.', home, 'home')

# ---- О клинике
about = f'''<!-- ============ О КЛИНИКЕ: ГЛАВНЫЙ ЭКРАН ============ -->
<section class="hero hero-page">
  <svg class="deco deco-hero-1 rock"><use href="#tri-outline"/></svg>
  <svg class="deco deco-hero-2 rock"><use href="#tri-outline"/></svg>
  <div class="hero-text">
    <h1>О клинике <br>Aiva Clinic</h1>
    <p class="hero-sub">Консультации врачей, диагностика, <br>физиотерапия и реабилитация в Астане</p>
    <div class="hero-btns">{wa_btn('Написать в WhatsApp')}</div>
  </div>
  <div class="hero-photos" data-hero-slider>
    <img class="hero-slide is-active" src="img/about-3.jpg" alt="Кабинет экзотерапии AIVA CLINIC">
    <img class="hero-slide" loading="lazy" src="img/about-2.jpg" alt="Кабинет физиотерапии">
    <img class="hero-slide" loading="lazy" src="img/service-2.jpg" alt="Зона ожидания">
    <img class="hero-slide" loading="lazy" src="img/service-6.jpg" alt="Кабинет IV-терапии">
  </div>
</section>

<!-- ============ О КЛИНИКЕ: ТЕКСТ ============ -->
<section class="section about-text">
  <div class="container container-narrow">
    <p class="lead reveal"><strong>В AIVA Clinic</strong> мы объединяем врачебную диагностику, современные технологии лечения и восстановительную медицину.</p>
    <p class="lead reveal">В основе нашей работы — индивидуальный подход и последовательное сопровождение пациента: от первичной консультации и обследования до лечения, восстановления и возвращения к привычной активности.</p>
  </div>
</section>

<!-- ============ НАША ЦЕЛЬ ============ -->
<section class="section teaser-gray">
  <div class="container">
    <div class="two-col reveal">
      <div><p class="eyebrow eyebrow-left">Наша цель</p><h2 class="h2 h2-left h2-sm">Помочь человеку лучше понимать своё здоровье</h2><p class="lead">Вовремя получать необходимую помощь и возвращаться к активной жизни.</p></div>
      <div class="zoom two-col-img"><img loading="lazy" src="img/offer-3.jpg" alt="Врач AIVA CLINIC"></div>
    </div>
  </div>
</section>

<!-- ============ ЭКЗОТЕРАПИЯ ============ -->
<section class="section" id="exo">
  <div class="container container-narrow">
    <p class="eyebrow reveal">Экзотерапия</p>
    <h2 class="h2 h2-sm reveal">Что такое ЭкзоТерапия?</h2>
    <p class="teaser-text reveal">Магнитно-волновой массаж на специальном аппарате. Во время процедуры вы просто лежите и отдыхаете — без ручного массажа и переодевания.</p>
    <div class="trio reveal">
      <div class="trio-item"><svg class="tri"><use href="#tri-solid"/></svg><h3>Расслабляет мышцы</h3><p>Снимает напряжение и скованность, уменьшает дискомфорт.</p></div>
      <div class="trio-item"><svg class="tri"><use href="#tri-solid"/></svg><h3>Улучшает самочувствие</h3><p>Помогает почувствовать лёгкость и восстановить силы.</p></div>
      <div class="trio-item"><svg class="tri"><use href="#tri-solid"/></svg><h3>Ускоряет восстановление</h3><p>Поддерживает организм после нагрузок, травм и стресса.</p></div>
    </div>
    <div class="center reveal" style="margin-top:32px"><a class="btn btn-light btn-lg" href="{wa_text('Здравствуйте! Пришлите, пожалуйста, презентацию «Экзотерапия».')}" {ext}>Скачать презентацию «Экзотерапия»</a></div>
  </div>
</section>

''' + EXO_PROMO + f'''<!-- ============ ЭКЗО-ТЕКАР 3 в 1 ============ -->
<section class="section teaser-gray" id="tecar">
  <div class="container">
    <p class="eyebrow reveal">Аппаратная физиотерапия</p>
    <h2 class="h2 reveal">ЭКЗО-ТЕКАР 3 в 1</h2>
    <div class="exo3 reveal">
      <div class="exo3-item"><h3>TECAR-терапия</h3><p>Радиочастотное воздействие на выбранную область: прогревает ткани, снимает боль и ускоряет восстановление.</p></div>
      <div class="exo3-item"><h3>Ультразвуковая терапия</h3><p>Микромассаж тканей ультразвуком: уменьшает отёк и воспаление.</p></div>
      <div class="zoom exo3-img"><img loading="lazy" src="img/device.jpg" alt="Аппарат ЭКЗО-ТЕКАР"></div>
      <div class="exo3-item"><h3>Ударно-волновая терапия</h3><p>Акустические волны воздействуют на болевые зоны, суставы и связки.</p></div>
      <div class="exo3-item"><h3>Инфракрасная терапия</h3><p>Мягкое тепловое воздействие для улучшения кровообращения и расслабления.</p></div>
    </div>
    <div class="center reveal" style="margin-top:32px"><a class="btn btn-light btn-lg" href="{wa_text('Здравствуйте! Пришлите, пожалуйста, презентацию «ЭКЗО-ТЕКАР 3 в 1».')}" {ext}>Скачать презентацию «ЭКЗО-ТЕКАР 3 в 1»</a></div>
  </div>
</section>

<!-- ============ СПОРТИВНОЕ ВОССТАНОВЛЕНИЕ ============ -->
<section class="section" id="sport">
  <div class="container container-narrow">
    <p class="eyebrow reveal">Спортивное восстановление</p>
    <h2 class="h2 h2-sm reveal">Партнёрство с AIVA Clinic <br>для спортивных федераций и клубов</h2>
    <p class="teaser-text reveal">Помогаем вашим спортсменам быстрее восстанавливаться, снижать риск травм и дольше оставаться в лучшей форме. Напишите нам, и мы подготовим предложение под вашу федерацию.</p>
    <div class="center reveal">{wa_btn('Обсудить сотрудничество')}</div>
    <div class="partners reveal">
      <p>Мы сотрудничаем</p>
      <div><span>Сборная Казахстана по хоккею</span><span>Каратэ-клуб</span></div>
    </div>
  </div>
</section>

''' + social()
page('about.html', 'О клинике — AIVA CLINIC', 'AIVA Clinic объединяет врачебную диагностику, современные технологии лечения и восстановительную медицину: экзотерапия, ЭКЗО-ТЕКАР 3 в 1, спортивное восстановление.', about)

# ---- Врачи
doctors = open('tools/src/doctors.html', encoding='utf-8').read()
page('doctors.html', 'Врачи — AIVA CLINIC', 'Врачи AIVA CLINIC: терапевт, врачи общей практики, эндокринолог, травматолог-ортопед, нейрохирург.', doctors + HELP_DOCTOR + social())

# ---- Прайс
prices = open('tools/src/prices.html', encoding='utf-8').read()
prices = prices.replace('    </div>\n  </div>\n</section>', '    </div>\n    <p class="price-discount reveal">Скидка 10% для льготных категорий</p>\n  </div>\n</section>')
assert 'price-discount' in prices
page('prices.html', 'Прайс — AIVA CLINIC', 'Цены на консультации, УЗИ-диагностику, чек-апы, IV-терапию, физиотерапию и реабилитацию в AIVA CLINIC. Скидка 10% для льготных категорий.',
     poster_block(**DRIP, cta_label='Написать в WhatsApp', second=('Другие акции', 'offers.html'), sid='offer-drip') + prices + EXO_PROMO + social())

# ---- Акции
offers = EXO_PROMO.replace('class="section exo-promo"', 'class="section exo-promo exo-hero"') + poster_block(**LIVER, cta_label='Записаться на чек-ап', sid='offer-liver') + poster_block(**DRIP, cta_label='Записаться на капельницу', sid='offer-drip') + social()
page('offers.html', 'Акции — AIVA CLINIC', 'Акции AIVA CLINIC: бесплатный экзомассаж, чек-ап печени 8 в 1 за 23 000 ₸, скидка 30% на капельницы.', offers)

# ---- Для бизнеса
biz_btns = f'''<div class="poster-btns">{wa_btn('Обсудить в WhatsApp')}<a class="btn btn-light btn-lg" href="{wa_text('Здравствуйте! Пришлите, пожалуйста, предложение по корпоративным сертификатам AIVA Clinic.')}" {ext}>Скачать предложение</a></div>'''
business = f'''<!-- ============ ДЛЯ БИЗНЕСА ============ -->
<section class="section" id="business">
  <div class="container container-narrow">
    <p class="eyebrow reveal">Для бизнеса</p>
    <h2 class="h2 reveal">Корпоративные сертификаты <br>AIVA Clinic</h2>
    <p class="teaser-text reveal">Подарите сотрудникам, клиентам и партнёрам заботу о здоровье. Компания платит до 50% меньше номинала, а получатель пользуется услугами клиники на всю сумму сертификата.</p>
    <div class="center reveal">{biz_btns}</div>
  </div>
</section>

<section class="section teaser-gray">
  <div class="container">
    <h2 class="h2 h2-sm reveal">Почему это выгодно</h2>
    <div class="trio trio-4">
      <div class="trio-item reveal"><span class="trio-num">1</span><h3>Экономия до 50%</h3><p>Сертификат на 1 000 000 ₸ обходится компании в 500 000 ₸.</p></div>
      <div class="trio-item reveal"><span class="trio-num">2</span><h3>Подарок, которым пользуются</h3><p>Диагностика, терапия и восстановление вместо очередного сувенира.</p></div>
      <div class="trio-item reveal"><span class="trio-num">3</span><h3>Всё в одной клинике</h3><p>Консультации врачей, анализы, УЗИ, чек-апы, IV-терапия, физиотерапия и реабилитация.</p></div>
      <div class="trio-item reveal"><span class="trio-num">4</span><h3>Именной сертификат</h3><p>У каждого получателя свой номер и QR-код.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container container-narrow">
    <h2 class="h2 h2-sm reveal">Кому подойдёт</h2>
    <ul class="check-list reveal">
      <li>Компаниям, которые хотят дополнить соцпакет сотрудников</li>
      <li>Для подарков коллективу к праздникам</li>
      <li>Для благодарности клиентам и партнёрам</li>
      <li>Для мотивации лучших сотрудников</li>
    </ul>
  </div>
</section>

<section class="section teaser-gray">
  <div class="container container-narrow">
    <h2 class="h2 h2-sm reveal">Три пакета</h2>
    <div class="biz-table-wrap reveal">
      <table class="biz-table">
        <thead><tr><th></th><th>Базовый</th><th class="is-std">Стандарт</th><th class="is-vip">VIP</th></tr></thead>
        <tbody>
          <tr><td>Цена для компании</td><td>100 000 ₸</td><td class="is-std">300 000 ₸</td><td class="is-vip">500 000 ₸</td></tr>
          <tr><td>Номинал сертификата</td><td><b>150 000 ₸</b></td><td class="is-std"><b>500 000 ₸</b></td><td class="is-vip"><b>1 000 000 ₸</b></td></tr>
          <tr><td>Скидка</td><td><b>30%</b></td><td class="is-std"><b>40%</b></td><td class="is-vip"><b>50%</b></td></tr>
          <tr><td>Выгода</td><td>50 000 ₸</td><td class="is-std">200 000 ₸</td><td class="is-vip">500 000 ₸</td></tr>
        </tbody>
      </table>
    </div>
    <p class="teaser-text reveal" style="margin-top:32px">Скачайте предложение с условиями и описанием пакетов или напишите нам в WhatsApp.</p>
    <div class="center reveal">{biz_btns}</div>
  </div>
</section>

''' + social()
page('business.html', 'Для бизнеса — корпоративные сертификаты AIVA CLINIC', 'Корпоративные сертификаты AIVA Clinic: компания платит до 50% меньше номинала, получатель пользуется услугами клиники на всю сумму. Три пакета: Базовый, Стандарт, VIP.', business)

# ---- Контакты (как были) + соцсети
contacts = open('tools/src/contacts.html', encoding='utf-8').read()
page('contacts.html', 'Контакты — AIVA CLINIC', 'AIVA CLINIC: Астана, ул. Е 669, 13. Ежедневно с 08:00 до 20:00. Телефон и WhatsApp +7 (747) 227-40-96.', contacts + social())

# устаревшая страница отзывов больше не нужна — блок рейтинга теперь на главной
if os.path.exists('reviews.html'):
    os.remove('reviews.html'); print('removed reviews.html')

# ---------------------------------------------------------------- CSS
s = open('css/style.css', encoding='utf-8').read()
if '/* ---- блоки по ТЗ ---- */' not in s:
    s += '''
/* ---- блоки по ТЗ ---- */
.lang { display: flex; align-items: center; gap: 6px; position: relative; font-size: 15px; font-weight: 600; color: #9a9a9a; }
.lang button { color: inherit; padding: 4px 2px; }
.lang button.is-active, .lang button:hover { color: var(--green-dark); }
.lang-note { position: absolute; top: 100%; right: 0; margin-top: 6px; padding: 8px 12px; border-radius: 10px; background: var(--green-dark); color: #fff; font-size: 12px; font-weight: 500; white-space: nowrap; }
.hero-page { min-height: 560px; }
.svc-groups { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; margin-bottom: 36px; }
.svc-group { display: flex; flex-direction: column; padding: 26px 24px 22px; background: #fff; border: 1px solid var(--green); border-radius: 22px; transition: opacity 1s ease, transform 1s ease, box-shadow .3s; }
.svc-group:hover { box-shadow: 0 20px 44px -22px rgba(114, 186, 69, .7); }
.svc-group h3 { font-size: 17px; line-height: 1.3; font-weight: 700; text-transform: uppercase; color: var(--green-dark); margin-bottom: 14px; min-height: 44px; }
.svc-group ol { padding-left: 20px; margin-bottom: 14px; flex: 1; list-style: decimal; }
.svc-group li { font-size: 14px; line-height: 1.5; margin-bottom: 4px; }
.svc-group span { font-size: 14px; font-weight: 600; color: var(--green); }
.poster-card { display: grid; grid-template-columns: 360px 1fr; gap: 48px; align-items: center; padding: 32px 48px 32px 32px; background: #fff; border: 1px solid var(--green); border-radius: var(--radius); }
.poster-img { border-radius: 20px; }
.poster-body h2 { font-size: 30px; line-height: 1.2; font-weight: 700; text-transform: uppercase; color: var(--green-dark); margin-bottom: 14px; }
.poster-body h2 s { font-size: 20px; font-weight: 500; color: #9a9a9a; }
.poster-body > p { font-size: 16px; margin-bottom: 14px; }
.poster-body .offer-list { margin-bottom: 24px; font-size: 14px; }
.poster-btns { display: flex; flex-wrap: wrap; gap: 14px; }
.soc-tiles { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; max-width: 760px; margin: 0 auto; }
.soc-tile { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 36px 24px 30px; text-align: center; background: #fff; border: 1px solid var(--green); border-radius: 26px; transition: opacity 1s ease, transform 1s ease, box-shadow .3s; }
.soc-tile:hover { box-shadow: 0 20px 44px -22px rgba(114, 186, 69, .7); }
.soc-tile svg { width: 64px; height: 64px; color: var(--green-dark); }
.soc-tile strong { font-size: 22px; font-weight: 700; color: var(--green-dark); }
.soc-tile small { font-size: 14px; color: #8a8a8a; margin-bottom: 10px; }
.c-google { background: linear-gradient(90deg, #4285f4 0 25%, #ea4335 25% 50%, #fbbc05 50% 75%, #34a853 75%); -webkit-background-clip: text; background-clip: text; color: transparent; }
.exo-card { padding: 44px 48px; text-align: left; background: var(--green-pale); border: 1px solid #dcedd2; border-radius: var(--radius); }
.exo-card h2 { font-size: 30px; line-height: 1.2; font-weight: 700; text-transform: uppercase; color: var(--green-dark); margin-bottom: 12px; }
.exo-card p { max-width: 720px; font-size: 17px; line-height: 1.55; margin-bottom: 24px; }
.exo-hero { padding-top: 70px; }
.about-text .lead { max-width: 860px; margin: 0 auto 18px; font-size: 20px; line-height: 1.6; text-align: center; }
.two-col { display: grid; grid-template-columns: 1fr 480px; gap: 60px; align-items: center; }
.two-col .lead { font-size: 18px; line-height: 1.6; }
.two-col-img { aspect-ratio: 4 / 3; }
.exo3 { display: grid; grid-template-columns: 1fr 300px 1fr; gap: 24px 40px; align-items: center; }
.exo3-img { grid-row: 1 / 3; grid-column: 2; aspect-ratio: 3 / 4; border-radius: 24px; }
.exo3-item { padding: 24px 26px; background: #fff; border: 1px solid var(--green); border-radius: 22px; }
.exo3-item h3 { font-size: 18px; font-weight: 700; text-transform: uppercase; color: var(--green-dark); margin-bottom: 8px; }
.exo3-item p { font-size: 14px; line-height: 1.5; }
.partners { margin-top: 40px; text-align: center; }
.partners p { font-size: 20px; font-weight: 600; margin-bottom: 14px; }
.partners div { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; }
.partners span { padding: 12px 24px; border: 1px solid var(--green); border-radius: 40px; font-size: 15px; font-weight: 600; color: var(--green-dark); }
.price-discount { margin-top: 28px; padding: 18px 24px; text-align: center; font-size: 18px; font-weight: 700; text-transform: uppercase; color: var(--green-dark); background: var(--yellow); border-radius: 16px; }
.trio-4 { grid-template-columns: repeat(4, 1fr); }
.check-list { max-width: 720px; margin: 0 auto; }
.check-list li { position: relative; padding: 12px 0 12px 36px; font-size: 18px; border-bottom: 1px solid var(--line); }
.check-list li::before { content: ''; position: absolute; left: 4px; top: 18px; width: 16px; height: 9px; border-left: 3px solid var(--green); border-bottom: 3px solid var(--green); transform: rotate(-45deg); }
.biz-table-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: 20px; background: #fff; }
.biz-table { width: 100%; border-collapse: collapse; font-size: 16px; }
.biz-table th, .biz-table td { padding: 16px 20px; text-align: center; border-bottom: 1px solid var(--line); }
.biz-table td:first-child { text-align: left; color: #8a8a8a; font-size: 14px; }
.biz-table th { font-size: 15px; font-weight: 700; text-transform: uppercase; color: var(--ink); }
.biz-table .is-std { background: #f3f9ee; }
.biz-table .is-vip { background: #fff9e0; }
.biz-table b { color: var(--green-dark); }
.biz-table tr:last-child td { border-bottom: 0; }
@media (max-width: 1180px) { .topbar .top-info-addr { display: flex; } }
@media (max-width: 1100px) {
  .svc-groups { grid-template-columns: 1fr 1fr; }
  .exo3 { grid-template-columns: 1fr 1fr; }
  .exo3-img { grid-row: auto; grid-column: 1 / -1; aspect-ratio: 16 / 9; }
  .trio-4 { grid-template-columns: 1fr 1fr; }
  .poster-card { grid-template-columns: 300px 1fr; padding: 24px; gap: 28px; }
}
@media (max-width: 960px) {
  .topbar .top-info { display: none; }
  .lang { display: none; }
  .svc-groups, .exo3, .trio-4, .soc-tiles { grid-template-columns: 1fr; }
  .poster-card { grid-template-columns: 1fr; }
  .poster-img { max-width: 360px; margin: 0 auto; }
  .poster-body h2 { font-size: 24px; }
  .two-col { grid-template-columns: 1fr; gap: 24px; }
  .exo-card { padding: 28px 22px; }
  .exo-card h2 { font-size: 24px; }
  .about-text .lead { font-size: 17px; }
}
'''
open('css/style.css', 'w', encoding='utf-8').write(s)

# удалить старые медиа-правила, которые скрывали адрес и прятали строку меню — новые добавлены выше
for f in glob.glob('*.html'):
    t = open(f, encoding='utf-8').read()
    assert t.count(V) == 6, f
print('done')
