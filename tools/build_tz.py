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
V = '?v=52'

WA = 'https://wa.me/77472274096'
PHONE = '+7 (747) 227-40-96'
TEL = 'tel:+77472274096'
GIS = 'https://2gis.kz/astana/search/%D1%84%D1%88%D0%BC%D1%84/firm/70000001090259641?m=71.482275%2C51.082042%2F14.72&immersive=on'
GIS_REV = 'https://2gis.kz/astana/firm/70000001090259641/tab/reviews'
YA = 'https://yandex.kz/maps/ru/org/aiva_clinic/132063384129/?ll=71.481355%2C51.087490&z=16.63'
GMAPS = 'https://www.google.com/maps/search/AIVA+Clinic+%D0%90%D1%81%D1%82%D0%B0%D0%BD%D0%B0'
INSTA = 'https://www.instagram.com/aiva.clinic'
YT = 'https://www.youtube.com/channel/UC1EBxPu6hds8KHRhQzTv8gw'
TT = 'https://www.tiktok.com/@aiva.clinic'
# пока презентаций нет — кнопки «Скачать» ведут в WhatsApp с готовым запросом
def wa_text(t):
    from urllib.parse import quote
    return WA + '?text=' + quote(t)

wa_btn = lambda label, cls='btn btn-grad btn-lg glow': f'<a class="{cls}" data-href="whatsappHref" href="{WA}" target="_blank" rel="noopener">{label}</a>'
ext = 'target="_blank" rel="noopener"'

# фирменная графика клиента: ленты (широкие дуги) — на первых экранах, кольца (тонкие дуги) — в баннерах и подложках
ARCS = '''<svg class="hero-arcs" viewBox="0 0 1320 760" preserveAspectRatio="xMinYMin slice" aria-hidden="true" fill="none">
    <circle cx="1700" cy="900" r="1000" stroke="#72b34a" stroke-width="88"/>
    <circle cx="1700" cy="900" r="790" stroke="#72b34a" stroke-width="88"/>
  </svg>'''
# внутренние страницы: тонкое кольцо у правого верхнего угла (вторая форма фирменной графики)
ARCS_PAGE = '''<svg class="hero-arcs" viewBox="0 0 1320 760" preserveAspectRatio="xMinYMin slice" aria-hidden="true" fill="none">
    <circle cx="1620" cy="-20" r="420" stroke="#72b34a" stroke-width="28"/>
  </svg>'''

# ---------------------------------------------------------------- общие части
SPRITE = open('js/layout.js', encoding='utf-8').read()
SPRITE = SPRITE[SPRITE.index('<!-- SVG-спрайт'):SPRITE.index('</svg>') + len('</svg>')]

NAV_ITEMS = [('index.html', 'Главная'), ('about.html', 'О клинике'), ('doctors.html', 'Врачи'),
             ('prices.html', 'Прайс'), ('offers.html', 'Акции'), ('news.html', 'Новости'), ('business.html', 'Для бизнеса')]
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
    <div><h4>Клиника</h4><a href="offers.html">Акции</a><a href="news.html">Новости</a><a href="business.html">Для бизнеса</a><a href="index.html#reviews">Отзывы о клинике</a><a href="contacts.html">Контакты</a></div>
    <div><h4>Услуги</h4><a href="prices.html#svc-diag">Консультация и диагностика</a><a href="prices.html#svc-iv">IV и интегративная терапия</a><a href="prices.html#checkups">Чек-апы</a><a href="prices.html#svc-physio">Физиотерапия</a><a href="prices.html#svc-rehab">Реабилитация и восстановление</a></div>
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
INSTAS = [('aiva.clinic', 'Основной аккаунт клиники', 'data-href="instagramHref" '), ('aiva.clinic_sport', 'Клиника реабилитации', ''),
          ('aiva.clinic_exo', 'Экзотерапия · Экзомассаж', ''), ('aiva.clinic_urology', 'Уролог · Андролог', ''), ('aiva.clinic_kids', 'Педиатр · Ортопед', '')]
def social(extra_cls=''):
    tiles = '\n'.join(f'      <a class="soc-tile soc-ig reveal" {attr}href="https://www.instagram.com/{h}" {ext}><span class="soc-ico"><svg><use href="#i-insta"/></svg></span><strong>{h}</strong><small>{d}</small><span class="btn btn-sm">Подписаться</span></a>' for h, d, attr in INSTAS)
    return f'''<!-- ============ СОЦИАЛЬНЫЕ СЕТИ (по ТЗ, на каждой странице): пять Instagram-аккаунтов клиники ============ -->
<section class="section social-tz {extra_cls}">
  <div class="container container-narrow">
    <p class="eyebrow reveal">Социальные сети</p>
    <h2 class="h2 h2-sm reveal">Следите за нами <br>в Instagram</h2>
    <p class="teaser-text reveal">Подпишитесь, чтобы не пропустить специальные предложения, бесплатные процедуры, новости клиники и полезные видео от наших врачей.</p>
    <div class="soc-tiles">
{tiles}
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
      <div class="zoom promo-img"><img loading="lazy" src="img/promo.jpg?v=2" alt="Главный врач AIVA CLINIC Саламбекова Жулдыз Сериковна"></div>
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
# чек-ап печени — широкий баннер по макету: текст, чипы состава и цена слева, анатомия с аппаратом УЗИ справа, кнопки поверх
def liver_block(cta_label, second=None, sid='offer-liver'):
    second_html = f'<a class="btn btn-light btn-lg" href="{second[1]}">{second[0]}</a>' if second else ''
    chips = ''.join(f'<li>{c}</li>' for c in ['УЗИ органов брюшной полости', 'АЛТ', 'АСТ', 'ГГТП', 'Глюкоза', 'Общий анализ крови', 'Холестерин', 'Приём врача — в подарок'])
    return f'''<section class="section liver-section" id="{sid}">
  <div class="container">
    <div class="liver-card reveal">
      <img class="liver-img" loading="lazy" src="img/promo-liver-wide.jpg" alt="Чек-ап печени: анатомия и аппарат УЗИ" width="1000" height="690">
      <div class="liver-body">
        <p class="eyebrow eyebrow-left">Акция</p>
        <h2 class="liver-title"><b>8 в 1</b><span>Чек-ап печени</span></h2>
        <p class="liver-text">Комплексная проверка печени за один визит в AIVA Clinic.</p>
        <ul class="liver-chips">{chips}</ul>
        <div class="liver-price"><b>23 000 ₸</b><s>34 900 ₸</s></div>
        <div class="poster-btns">{wa_btn(cta_label, 'btn btn-grad btn-lg glow')}{second_html}</div>
      </div>
    </div>
  </div>
</section>

'''

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
          ('svc-rehab', 'Реабилитация и восстановление', ['Экзотерапия', 'ЛФК', 'Лечебный массаж', 'Реабилитация', 'Спортивное восстановление'])]
groups_html = ''.join(f'''      <a class="svc-group reveal" href="prices.html#{gid}">
        <h3>{title}</h3>
        <ol>
{''.join(f'          <li>{x}</li>{chr(10)}' for x in items)}        </ol>
        <span>Смотреть в прайсе →</span>
      </a>
''' for gid, title, items in GROUPS)

hero = open('tools/src/hero.html', encoding='utf-8').read().replace('<!--ARCS-->', ARCS)
assert 'WhatsApp' in hero and 'prices.html' in hero and 'hero-arcs' in hero

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

''' + HELP_DOCTOR + liver_block('Написать в WhatsApp', second=('Другие акции', 'offers.html')) + social() + RATING
page('index.html', 'AIVA CLINIC — клиника терапии, физиотерапии и реабилитации в Астане',
     'AIVA CLINIC в Астане: консультации врачей, УЗИ-диагностика, чек-апы, IV-терапия, физиотерапия и реабилитация. Ежедневно с 08:00 до 20:00, ул. Е 669, 13.', home, 'home')

# ---- О клинике
about = f'''<!-- ============ О КЛИНИКЕ: ГЛАВНЫЙ ЭКРАН ============ -->
<section class="hero hero-page">
  {ARCS_PAGE}
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
    <p class="lead lead-first reveal"><strong>В AIVA Clinic</strong> мы объединяем врачебную диагностику, современные технологии лечения и восстановительную медицину.</p>
    <p class="lead reveal">В основе нашей работы — индивидуальный подход и последовательное сопровождение пациента: от первичной консультации и обследования до лечения, восстановления и возвращения к привычной активности.</p>
  </div>
</section>

<!-- ============ НАША ЦЕЛЬ ============ -->
<section class="section teaser-gray">
  <div class="container">
    <div class="two-col reveal">
      <p class="goal">Наша цель — помочь человеку лучше понимать своё здоровье, вовремя получать необходимую помощь и возвращаться к активной жизни.</p>
      <div class="zoom two-col-img"><img loading="lazy" src="img/offer-3.jpg" alt="Врач AIVA CLINIC"></div>
    </div>
  </div>
</section>

<!-- ============ ЭКЗОТЕРАПИЯ ============ -->
<section class="section" id="exo">
  <div class="container container-narrow">
    <p class="eyebrow reveal">Экзотерапия</p>
    <h2 class="h2 h2-sm reveal">Что такое ЭкзоТерапия?</h2>
    <ul class="exo-list reveal">
      <li>Магнитно-волновой массаж на специальном аппарате.</li>
      <li>Во время процедуры вы просто лежите и отдыхаете — без ручного массажа и переодевания.</li>
      <li>Расслабляет напряжённые мышцы.</li>
      <li>Уменьшает дискомфорт и скованность.</li>
      <li>Улучшает общее самочувствие.</li>
      <li>Ускоряет восстановление после нагрузок.</li>
    </ul>
    <div class="center reveal" style="margin-top:32px"><a class="btn btn-light btn-lg" href="{wa_text('Здравствуйте! Пришлите, пожалуйста, презентацию «Экзотерапия».')}" {ext}>Скачать презентацию «Экзотерапия»</a></div>
  </div>
</section>

''' + EXO_PROMO + f'''<!-- ============ ЭКЗО-ТЕКАР 3 в 1 ============ -->
<section class="section teaser-gray" id="tecar">
  <div class="container">
    <p class="eyebrow reveal">Аппаратная физиотерапия</p>
    <h2 class="h2 reveal">ЭКЗО-ТЕКАР 3 в 1</h2>
    <div class="h2-rule reveal"><i></i></div>
    <p class="exo3-sub reveal">Технологии для эффективного восстановления и лечения</p>
    <div class="exo3 reveal">
      <div class="exo3-item exo3-l"><i class="exo3-ico"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="16" cy="16" r="2.5" fill="currentColor" stroke="none"/><path d="M11 11a7 7 0 0 0 0 10M21 11a7 7 0 0 1 0 10M7.5 7.5a12 12 0 0 0 0 17M24.5 7.5a12 12 0 0 1 0 17"/></svg></i><div><h3>TECAR-терапия</h3><p>Радиочастотное воздействие на выбранную область: прогревает ткани, снимает боль и ускоряет восстановление.</p></div></div>
      <div class="exo3-item exo3-l"><i class="exo3-ico"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 16h5l3-8 4 16 4-12 2 4h8"/></svg></i><div><h3>Ударно-волновая терапия</h3><p>Акустические волны воздействуют на болевые зоны, суставы и связки.</p></div></div>
      <div class="exo3-device"><img loading="lazy" src="img/device.webp" alt="Аппарат ЭКЗО-ТЕКАР 3 в 1" width="440" height="520"></div>
      <div class="exo3-item exo3-r"><i class="exo3-ico"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="16" cy="22" r="2.5" fill="currentColor" stroke="none"/><path d="M10 16a8 8 0 0 1 12 0M6 11a14 14 0 0 1 20 0M12.5 19.5a5 5 0 0 1 7 0"/></svg></i><div><h3>Ультразвуковая терапия</h3><p>Микромассаж тканей ультразвуком: уменьшает отёк и воспаление.</p></div></div>
      <div class="exo3-item exo3-r"><i class="exo3-ico"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M10 6c-3 4 3 6 0 10s3 6 0 10M16 6c-3 4 3 6 0 10s3 6 0 10M22 6c-3 4 3 6 0 10s3 6 0 10"/></svg></i><div><h3>Инфракрасная терапия</h3><p>Мягкое тепловое воздействие для улучшения кровообращения и расслабления.</p></div></div>
    </div>
    <div class="center reveal" style="margin-top:36px"><a class="btn btn-grad btn-lg btn-ico" href="{wa_text('Здравствуйте! Пришлите, пожалуйста, презентацию «ЭКЗО-ТЕКАР 3 в 1».')}" {ext}><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 7v8m-3.5-3.5L12 15l3.5-3.5M8 17h8"/></svg><span>Скачать презентацию «ЭКЗО-ТЕКАР 3 в 1»</span></a></div>
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
# Чек-апы — из фирменного прайс-листа «Прайс_чекапы.pdf» (дизайн: зелёная полоса слева, название — цена, «Итого»)
GIFT_DOC, GIFT_PED = 'Приём врача — в подарок', 'Приём педиатра — в подарок'
CHECKUPS = [
    dict(title='Базовый чек-ап (для всех)', total='69 700', items=[('Общий анализ крови (ОАК)', '3 300'), ('Аланинаминотрансфераза (АЛТ)', '1 900'), ('Аспартатаминотрансфераза (АСТ)', '1 900'), ('Гамма-глутамилтрансфераза (ГГТП)', '2 000'), ('Глюкоза крови', '2 000'), ('Креатинин', '2 000'), ('Тиреотропный гормон (ТТГ)', '2 000'), ('Общий холестерин (ХС)', '1 900'), ('Фолиевая кислота (витамин B9)', '5 200'), ('Ферритин', '5 700'), ('Витамин D', '9 900'), ('УЗИ органов брюшной полости (УЗИ ОБП)', '8 000'), ('УЗИ брахиоцефальных артерий (УЗИ БЦА)', '12 000'), ('Приём врача', '11 900')]),
    dict(title='Чек-ап печени', total='23 000', old='34 900', gift=GIFT_DOC, items=[('Общий анализ крови (ОАК)', '3 300'), ('Аланинаминотрансфераза (АЛТ)', '1 900'), ('Аспартатаминотрансфераза (АСТ)', '1 900'), ('Гамма-глутамилтрансфераза (ГГТП)', '2 000'), ('Глюкоза крови', '2 000'), ('Общий холестерин (ХС)', '1 900'), ('УЗИ органов брюшной полости (УЗИ ОБП)', '10 000'), ('Приём врача', '11 900')]),
    dict(title='Чек-ап щитовидной железы', total='32 900', items=[('Тиреотропный гормон (ТТГ)', '3 800'), ('Антитела к тиреопероксидазе (Анти-ТПО)', '4 500'), ('Тироксин свободный (Т4 свободный)', '4 700'), ('УЗИ щитовидной железы', '8 000'), ('Приём врача', '11 900')]),
    dict(title='Чек-ап сосудов', total='31 800', items=[('Ультразвуковая допплерография брахиоцефальных артерий (УЗДГ БЦА)', '12 000'), ('Общий холестерин (ХС)', '1 900'), ('Липопротеины низкой плотности (ЛПНП)', '2 000'), ('Липопротеины высокой плотности (ЛПВП)', '2 000'), ('Триглицериды (ТГ)', '2 000'), ('Приём врача', '11 900')]),
    dict(title='Чек-ап суставов', total='23 500', items=[('Общий анализ крови (ОАК)', '3 300'), ('С-реактивный белок (СРБ)', '2 900'), ('Мочевая кислота', '2 000'), ('Ревматоидный фактор (РФ)', '3 400'), ('Приём врача', '11 900')]),
    dict(title='Чек-ап мужской', total='45 760', items=[('Гормоны: тестостерон, эстрадиол, ЛГ, ФСГ', '16 010'), ('УЗИ мошонки, простаты, мочевого пузыря', '15 000'), ('Консультация уролога', '11 900'), ('Общий анализ крови (ОАК)', '2 850')]),
    dict(title='Чек-ап «Малыш» (3 месяца – 1 год)', total='37 190', old='49 090', gift=GIFT_PED,
         desc='Для первого года жизни, когда малыш растёт быстрее всего. Ортопед проверяет шею и тазобедренные суставы, чтобы вовремя выявить кривошею и дисплазию. Педиатр оценивает рост и развитие и даёт рекомендации по кормлению и прикорму.',
         items=[('Приём педиатра', 'в подарок'), ('Приём детского ортопеда (кривошея, дисплазия ТБС)', '11 900'), ('Общий анализ крови (ОАК)', '2 850'), ('Общий анализ мочи (ОАМ)', '1 705'), ('Аланинаминотрансфераза (АЛТ)', '1 870'), ('Аспартатаминотрансфераза (АСТ)', '1 870'), ('Билирубин общий', '2 035'), ('Билирубин прямой', '1 870'), ('Креатинин', '1 980'), ('Глюкоза', '1 980'), ('Витамин D', '9 130')]),
    dict(title='Чек-ап «Растём и развиваемся» (1–5 лет)', total='38 730', old='50 630', gift=GIFT_PED,
         desc='Для детей, которые начали ходить и активно двигаться. Ортопед проверяет стопы, ноги и осанку, чтобы не пропустить плоскостопие и вальгус. Педиатр оценивает развитие, питание и сон и даёт советы по профилактике заболеваний.',
         items=[('Приём педиатра', 'в подарок'), ('Приём детского ортопеда (плоскостопие, вальгус, нарушение осанки)', '11 900'), ('Общий анализ крови (ОАК)', '2 850'), ('Общий анализ мочи (ОАМ)', '1 705'), ('Аланинаминотрансфераза (АЛТ)', '1 870'), ('Аспартатаминотрансфераза (АСТ)', '1 870'), ('Билирубин общий', '2 035'), ('Креатинин', '1 980'), ('Глюкоза', '1 980'), ('Витамин D', '9 130'), ('Ферритин', '3 410')]),
    dict(title='Чек-ап «Школьный старт» (от 5 лет)', total='47 600', old='59 500', gift=GIFT_PED,
         desc='Для подготовки к школе и для школьников, когда нагрузка на спину растёт. Ортопед проверяет позвоночник и осанку, чтобы вовремя заметить сколиоз, плоскостопие и вальгус. Педиатр оценивает физическое развитие, питание и образ жизни.',
         items=[('Приём педиатра', 'в подарок'), ('Приём детского ортопеда (сколиоз, плоскостопие, вальгус)', '11 900'), ('Общий анализ крови (ОАК)', '2 850'), ('Общий анализ мочи (ОАМ)', '1 705'), ('Аланинаминотрансфераза (АЛТ)', '1 870'), ('Аспартатаминотрансфераза (АСТ)', '1 870'), ('Билирубин общий', '2 035'), ('Креатинин', '1 980'), ('Глюкоза', '1 980'), ('Ферритин', '3 410'), ('Комплексное УЗИ: органы брюшной полости, щитовидная железа, почки', '18 000')]),
]
def checkup_html(c):
    rows = ''.join(f'<div class="pr-row"><div class="pr-name">{n}</div><div class="pr-price">{("<b>%s ₸</b>" % p) if p[0].isdigit() else ("<em>%s</em>" % p)}</div></div>\n' for n, p in c['items'])
    old = f'<s>{c["old"]} ₸</s>' if c.get('old') else ''
    gift = f'<p class="pr-gift">{c["gift"]}</p>' if c.get('gift') else ''
    desc = f'<p class="pr-desc">{c["desc"]}</p>' if c.get('desc') else ''
    return f'''<div class="checkup reveal">
  <h3>{c['title']}</h3>
  <div class="pr-list">
{rows}  </div>
  <div class="pr-total"><span>Итого</span><span>{old}<b>{c['total']} ₸</b></span></div>
  {gift}{desc}
</div>
'''
CHECKUPS_HTML = f'''<!-- ============ ЧЕК-АПЫ (по фирменному прайс-листу) ============ -->
<section class="section price-page section-checkups" id="checkups">
  <div class="container container-narrow">
    <h2 class="price-h2 reveal">Чек-апы</h2>
    <p class="price-intro reveal">Комплексные программы обследования за один визит: анализы, УЗИ и приём врача по фиксированной цене.</p>
    <div class="checkups">
{''.join(checkup_html(c) for c in CHECKUPS)}    </div>
    <div class="center reveal" style="margin-top:20px">{wa_btn('Записаться на чек-ап')}</div>
  </div>
</section>

'''
prices = open('tools/src/prices.html', encoding='utf-8').read()
page('prices.html', 'Прайс — AIVA CLINIC', 'Цены на консультации, чек-апы, IV-терапию, физиотерапию и реабилитацию в AIVA CLINIC. 9 программ чек-апов. Скидка 10% для льготных категорий.',
     prices + CHECKUPS_HTML + poster_block(**DRIP, cta_label='Написать в WhatsApp', second=('Другие акции', 'offers.html'), sid='offer-drip') + EXO_PROMO + social())

# ---- Акции
OFFERS_HEAD = '''<!-- ============ АКЦИИ: ЗАГОЛОВОК СТРАНИЦЫ ============ -->
<section class="section section-head" id="offers">
  <div class="container container-narrow">
    <p class="eyebrow reveal">Акции</p>
    <h1 class="h2 reveal">Акции и специальные <br>предложения</h1>
    <p class="teaser-text reveal">Актуальные предложения AIVA Clinic: бесплатный пробный экзомассаж, чек-ап печени «8 в 1» и скидка на капельницы. Запишитесь в WhatsApp — администратор подберёт удобное время.</p>
  </div>
</section>

'''
offers = OFFERS_HEAD + EXO_PROMO + liver_block('Записаться на чек-ап') + poster_block(**DRIP, cta_label='Записаться на капельницу', sid='offer-drip') + social()
page('offers.html', 'Акции — AIVA CLINIC', 'Акции AIVA CLINIC: бесплатный экзомассаж, чек-ап печени 8 в 1 за 23 000 ₸, скидка 30% на капельницы.', offers)


# ---- Новости
NEWS = [
    dict(img='about-2.jpg', tag='Новость', title='Скидка 10% для льготных категорий пациентов', href='prices.html',
         text='Согласно приказу №38 от 24.09.2026 пенсионеры, многодетные матери, люди с инвалидностью I и II группы и ветераны получают скидку 10% на консультации, анализы, УЗИ и физиопроцедуры.'),
    dict(img='device.jpg', tag='Оборудование', title='ЭКЗО-ТЕКАР 3 в 1: аппаратная физиотерапия в AIVA Clinic', href='about.html',
         text='TECAR-терапия, ударно-волновая, ультразвуковая и инфракрасная терапия на одном аппарате: снимает боль, ускоряет восстановление тканей и суставов.'),
    dict(img='promo-liver.jpg', pos='top', tag='Акция', title='Чек-ап печени «8 в 1» за 23 000 ₸ вместо 34 900 ₸', href='offers.html#offer-liver',
         text='Общий анализ крови, АЛТ, АСТ, ГГТП, глюкоза, холестерин и УЗИ органов брюшной полости за один визит. Приём врача — в подарок.'),
]
news_cards = '\n'.join(f'''      <article class="news-card reveal">
        <a class="news-img" href="{n['href']}"><img src="img/{n['img']}" alt="{n['title']}" loading="lazy" style="object-position:{n.get('pos', 'center')}"></a>
        <div class="news-body">
          <span class="news-tag">{n['tag']}</span>
          <h3><a href="{n['href']}">{n['title']}</a></h3>
          <p>{n['text']}</p>
          <a class="news-more" href="{n['href']}">Подробнее →</a>
        </div>
      </article>''' for n in NEWS)
# ---- Новости: база знаний (структура как у блога-эталона: первый экран, баннер с цифрой, рубрики-фильтр,
#      разделы со статьями «текст + фото», карточки), оформление и вставки — фирменные (дуги, палитра)
KB_MARK = '<svg class="kb-mark" viewBox="0 0 46 22" fill="none" stroke-width="3.5" stroke-linecap="round" aria-hidden="true"><path d="M5 20a13 13 0 0 0 0-18" stroke="#306b4b"/><path d="M15 20a13 13 0 0 0 0-18" stroke="#72b34a"/><path d="M28 11h14" stroke="#306b4b" stroke-width="2.5"/></svg>'
def kb_h3(t):
    return f'<h3 class="kb-h3">{KB_MARK}<span>{t}</span></h3>'
def kb_img(src, alt, cls=''):
    return f'<div class="zoom kb-img {cls}"><img loading="lazy" src="img/{src}" alt="{alt}"></div>'

EXO3 = re.findall(r'<div class="exo3-item exo3-[lr]"><i class="exo3-ico">(<svg.*?</svg>)</i><div><h3>(.*?)</h3><p>(.*?)</p></div></div>', about)
assert len(EXO3) == 4, len(EXO3)
EXO_LIST = re.search(r'<ul class="exo-list reveal">(.*?)</ul>', about, re.S).group(1)
_disc = prices[prices.index('<div class="discount-cols">'):]
DISC_ULS = re.findall(r'<ul>(.*?)</ul>', _disc, re.S)[:2]
assert len(DISC_ULS) == 2
LIVER_CHECK = CHECKUPS[1]
SUMMARY = {
    'Базовый чек-ап (для всех)': 'Анализы крови, печень, щитовидная железа, витамины, УЗИ ОБП и БЦА, приём врача.',
    'Чек-ап печени': 'ОАК, АЛТ, АСТ, ГГТП, глюкоза, холестерин, УЗИ органов брюшной полости.',
    'Чек-ап щитовидной железы': 'ТТГ, Анти-ТПО, Т4 свободный, УЗИ щитовидной железы, приём врача.',
    'Чек-ап сосудов': 'УЗДГ брахиоцефальных артерий, холестерин, ЛПНП, ЛПВП, триглицериды.',
    'Чек-ап суставов': 'ОАК, С-реактивный белок, мочевая кислота, ревматоидный фактор, приём врача.',
    'Чек-ап мужской': 'Гормоны, УЗИ мошонки, простаты и мочевого пузыря, консультация уролога, ОАК.',
    'Чек-ап «Малыш» (3 месяца – 1 год)': 'Детский ортопед, анализы крови и мочи, витамин D. Приём педиатра — в подарок.',
    'Чек-ап «Растём и развиваемся» (1–5 лет)': 'Детский ортопед, анализы крови и мочи, витамин D, ферритин. Приём педиатра — в подарок.',
    'Чек-ап «Школьный старт» (от 5 лет)': 'Детский ортопед, анализы, комплексное УЗИ. Приём педиатра — в подарок.',
}
def checkup_card(c):
    old = f'<s>{c["old"]} ₸</s>' if c.get('old') else ''
    return f'<a class="kb-card reveal" href="prices.html#checkups"><h4>{c["title"]}</h4><p>{SUMMARY[c["title"]]}</p><b>{old}{c["total"]} ₸</b></a>'
liver_rows = ''.join(f'<div class="pr-row"><div class="pr-name">{n}</div><div class="pr-price"><b>{p} ₸</b></div></div>\n' for n, p in LIVER_CHECK['items'])
drip_cards = ''.join(f'<div class="kb-card kb-promo reveal"><h4>{t}</h4><small>по назначению врача</small></div>' for t in ['Восстановление и энергия', 'Иммунитет и детокс', 'Красота и антиэйдж', 'Индивидуальные программы'])
exo3_cards = ''.join(f'<div class="kb-card reveal"><i class="exo3-ico">{svg}</i><h4>{h}</h4><p>{p}</p></div>' for svg, h, p in EXO3)
checkup_cards = ''.join(checkup_card(c) for c in CHECKUPS)

news = f'''<!-- ============ НОВОСТИ: ПЕРВЫЙ ЭКРАН ============ -->
<section class="hero hero-page">
  {ARCS_PAGE}
  <div class="hero-text">
    <h1>Новости <br>и полезные статьи</h1>
    <p class="hero-sub">Акции, новое оборудование и ответы <br>на частые вопросы пациентов</p>
    <div class="hero-btns">{wa_btn('Записаться в WhatsApp')}<a class="btn btn-light btn-lg" href="prices.html">Открыть прайс</a></div>
  </div>
  <div class="hero-photos" data-hero-slider>
    <img class="hero-slide is-active" src="img/kb-stretch.jpg" alt="Активная жизнь без боли">
    <img class="hero-slide" loading="lazy" src="img/kb-iv.jpg" alt="IV-терапия в AIVA CLINIC">
    <img class="hero-slide" loading="lazy" src="img/service-2.jpg" alt="Зона ожидания AIVA CLINIC">
  </div>
</section>

<!-- ============ БАННЕР С ЦИФРОЙ ============ -->
<section class="section kb-banner-section">
  <div class="container">
    <div class="kb-banner reveal">
      <img loading="lazy" src="img/kb-wellness.jpg" alt="">
      <div class="kb-banner-text"><b>4 рубрики</b><span>Новости · Акции · Оборудование · Полезно знать</span></div>
    </div>
  </div>
</section>

<!-- ============ РУБРИКИ И МАТЕРИАЛЫ ============ -->
<section class="section kb" id="news">
  <div class="container container-narrow">
    <h2 class="h2 h2-left h2-sm reveal">Рубрики</h2>
    <div class="kb-tabs reveal" data-kb-tabs>
      <button type="button" class="is-active" data-kb="all">Все материалы</button>
      <button type="button" data-kb="news">Новости клиники</button>
      <button type="button" data-kb="promo">Акции</button>
      <button type="button" data-kb="equip">Оборудование</button>
      <button type="button" data-kb="know">Полезно знать</button>
    </div>

    <div class="kb-group" data-kb-group="news" id="kb-news">
      <h2 class="kb-h2 reveal">Новости клиники</h2>
      <div class="news-grid">
{news_cards}
      </div>
      <article class="kb-article reveal" id="discount">
        {kb_h3('Скидка 10% для льготных категорий')}
        <div class="kb-two">
          <div class="kb-text">
            <p>Согласно приказу №38 от 24.09.2026 г. в AIVA Clinic действует скидка 10% для льготных категорий пациентов.</p>
            <h4>Кто имеет право на скидку</h4><ul>{DISC_ULS[0]}</ul>
            <h4>На какие услуги</h4><ul>{DISC_ULS[1]}</ul>
            <a class="btn btn-light btn-sm" href="prices.html">Открыть прайс</a>
          </div>
          {kb_img('about-2.jpg', 'Кабинет физиотерапии AIVA CLINIC')}
        </div>
      </article>
    </div>

    <div class="kb-group" data-kb-group="promo" id="kb-promo">
      <h2 class="kb-h2 reveal">Акции</h2>
      <article class="kb-article reveal" id="kb-liver">
        {kb_h3('Чек-ап печени «8 в 1» за 23 000 ₸ вместо 34 900 ₸')}
        <div class="kb-two">
          <div class="kb-text">
            <p>{LIVER['text']}</p>
            <div class="pr-list">
{liver_rows}            </div>
            <div class="pr-total"><span>Итого</span><span><s>{LIVER_CHECK['old']} ₸</s><b>{LIVER_CHECK['total']} ₸</b></span></div>
            <p class="pr-gift">{LIVER_CHECK['gift']}</p>
            {wa_btn('Записаться на чек-ап', 'btn btn-grad btn-sm glow')}
          </div>
          {kb_img('offer-1.jpg', 'УЗИ органов брюшной полости')}
        </div>
      </article>
      <article class="kb-article reveal" id="kb-drip">
        {kb_h3(DRIP['title'])}
        <div class="kb-two">
          <div class="kb-text">
            <p>{DRIP['text']}</p>
            <div class="kb-cards kb-cards-2">{drip_cards}</div>
            {wa_btn('Записаться на капельницу', 'btn btn-grad btn-sm glow')}
          </div>
          {kb_img('kb-iv.jpg', 'IV-терапия: капельница в AIVA CLINIC')}
        </div>
      </article>
      <article class="kb-article reveal" id="kb-exo-free">
        {kb_h3('Попробуйте экзомассаж бесплатно!')}
        <div class="kb-two kb-two-rev">
          {kb_img('kb-exo-room.jpg', 'Кабинет экзотерапии AIVA CLINIC', 'kb-img-wide')}
          <div class="kb-text">
            <p>Первая процедура в AIVA Clinic — в подарок. Всего 10 минут, без прикосновений и усилий: вы просто лежите, а аппарат делает всю работу.</p>
            {wa_btn('Записаться', 'btn btn-grad btn-sm glow')}
          </div>
        </div>
      </article>
    </div>

    <div class="kb-group" data-kb-group="equip" id="kb-equip">
      <h2 class="kb-h2 reveal">Оборудование</h2>
      <article class="kb-article reveal" id="kb-tecar">
        {kb_h3('ЭКЗО-ТЕКАР 3 в 1: аппаратная физиотерапия в AIVA Clinic')}
        <div class="kb-two kb-two-rev">
          <div class="kb-device"><img loading="lazy" src="img/device.webp" alt="Аппарат ЭКЗО-ТЕКАР 3 в 1" width="440" height="520"></div>
          <div class="kb-text">
            <p><strong>Технологии для эффективного восстановления и лечения</strong></p>
            <p>TECAR-терапия, ударно-волновая, ультразвуковая и инфракрасная терапия на одном аппарате: снимает боль, ускоряет восстановление тканей и суставов.</p>
            <div class="kb-cards kb-cards-2">{exo3_cards}</div>
            <a class="btn btn-light btn-sm" href="about.html#tecar">Подробнее об аппарате</a>
          </div>
        </div>
      </article>
      <article class="kb-article reveal" id="kb-exostol">
        {kb_h3('Аппарат для экзотерапии')}
        <div class="kb-two">
          <div class="kb-text">
            <p>Магнитно-волновой массаж на специальном аппарате.</p>
            <p>Во время процедуры вы просто лежите и отдыхаете — без ручного массажа и переодевания.</p>
            <a class="btn btn-light btn-sm" href="prices.html#svc-exo">Цены на экзотерапию</a>
          </div>
          {kb_img('kb-exo-bed.jpg', 'Процедура экзотерапии', 'kb-img-wide')}
        </div>
      </article>
    </div>

    <div class="kb-group" data-kb-group="know" id="kb-know">
      <h2 class="kb-h2 reveal">Полезно знать</h2>
      <article class="kb-article reveal" id="kb-exo-what">
        {kb_h3('Что такое ЭкзоТерапия?')}
        <div class="kb-two">
          <div class="kb-text"><ul>{EXO_LIST}</ul><a class="btn btn-light btn-sm" href="about.html#exo">Подробнее об экзотерапии</a></div>
          {kb_img('kb-exo-sit.jpg', 'Пациентка после процедуры экзотерапии')}
        </div>
      </article>
      <article class="kb-article reveal" id="kb-checkups">
        {kb_h3('Какой чек-ап выбрать?')}
        <p class="kb-lead">Девять программ обследования: от базового чек-апа до детских и мужского. Анализы, УЗИ и приём врача — за один визит и по фиксированной цене.</p>
        <div class="kb-cards kb-cards-3">{checkup_cards}</div>
        <div class="center" style="margin-top:28px"><a class="btn btn-grad btn-lg glow" href="prices.html#checkups">Все чек-апы в прайсе</a></div>
      </article>
      <article class="kb-article reveal" id="kb-how">
        {kb_h3('Как записаться на приём')}
        <div class="trio">
          <div class="trio-item"><span class="trio-num">1</span><h3>Напишите в WhatsApp или позвоните</h3><p>Расскажите, что беспокоит, или назовите нужную услугу.</p></div>
          <div class="trio-item"><span class="trio-num">2</span><h3>Администратор подберёт врача и время</h3><p>Подскажем подготовку к анализам и УЗИ, если она нужна.</p></div>
          <div class="trio-item"><span class="trio-num">3</span><h3>Приходите в клинику</h3><p>Астана, ул. Е 669, 13. Ежедневно с 08:00 до 20:00.</p></div>
        </div>
        <div class="center" style="margin-top:28px">{wa_btn('Записаться в WhatsApp')}</div>
      </article>
    </div>
  </div>
</section>

''' + social()
page('news.html', 'Новости — AIVA CLINIC', 'Новости и полезные статьи AIVA CLINIC в Астане: акции, скидки, оборудование ЭКЗО-ТЕКАР, экзотерапия, чек-апы и как записаться на приём.', news)

# ---- Для бизнеса: сертификаты (визуал по макету: белый «Базовый», зелёный «Стандарт», золотой «Gold»)
BIZ_OFFER = wa_text('Здравствуйте! Пришлите, пожалуйста, предложение по корпоративным сертификатам AIVA Clinic.')
TIERS = [dict(cls='base', tier='Базовый', nominal='150 000', price='100 000', disc='30%', gain='50 000', logo='logo.png'),
         dict(cls='std', tier='Стандарт', nominal='500 000', price='300 000', disc='40%', gain='200 000', logo='logo-white.png'),
         dict(cls='gold', tier='Gold', nominal='1 000 000', price='500 000', disc='50%', gain='500 000', logo='logo.png')]
def cert_card(t):
    return f'''      <div class="cert-item reveal">
        <div class="cert cert-{t['cls']}">
          <img class="cert-logo" src="img/{t['logo']}" alt="AIVA CLINIC" width="854" height="211">
          <span class="cert-title">Подарочный сертификат</span>
          <b class="cert-sum">{t['nominal']} ₸</b>
          <span class="cert-note">на услуги AIVA Clinic</span>
          <span class="cert-tier">{t['tier']}</span>
        </div>
        <ul class="cert-specs">
          <li><span>Цена для компании</span><b>{t['price']} ₸</b></li>
          <li><span>Номинал сертификата</span><b>{t['nominal']} ₸</b></li>
          <li><span>Скидка</span><b>{t['disc']}</b></li>
          <li><span>Выгода</span><b>{t['gain']} ₸</b></li>
        </ul>
        <a class="btn btn-light btn-sm" href="{wa_text('Здравствуйте! Хочу заказать корпоративные сертификаты AIVA Clinic, пакет «' + t['tier'] + '».')}" {ext}>Выбрать пакет</a>
      </div>
'''
business = f'''<!-- ============ ДЛЯ БИЗНЕСА: ПЕРВЫЙ ЭКРАН ============ -->
<section class="hero hero-page">
  {ARCS_PAGE}
  <div class="hero-text">
    <h1>Корпоративные <br>сертификаты</h1>
    <p class="hero-sub">Компания платит до 50% меньше номинала, <br>получатель пользуется услугами на всю сумму</p>
    <div class="hero-btns">{wa_btn('Обсудить в WhatsApp')}<a class="btn btn-light btn-lg" href="{BIZ_OFFER}" {ext}>Скачать предложение</a></div>
  </div>
  <div class="hero-photos">
    <img class="hero-slide is-active" src="img/biz-certs.jpg" alt="Подарочные сертификаты AIVA Clinic: Базовый, Стандарт и Gold">
  </div>
</section>

<!-- ============ ТРИ ПАКЕТА ============ -->
<section class="section" id="packages">
  <div class="container">
    <p class="eyebrow reveal">Три пакета</p>
    <h2 class="h2 h2-sm reveal">Выберите номинал сертификата</h2>
    <p class="teaser-text reveal">Подарите сотрудникам, клиентам и партнёрам заботу о здоровье. Чем выше номинал, тем больше скидка для компании.</p>
    <div class="cert-grid">
{''.join(cert_card(t) for t in TIERS)}    </div>
  </div>
</section>

<!-- ============ ПОЧЕМУ ЭТО ВЫГОДНО ============ -->
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

<!-- ============ КАК ЭТО РАБОТАЕТ ============ -->
<section class="section">
  <div class="container container-narrow">
    <h2 class="h2 h2-sm reveal">Как это работает</h2>
    <div class="trio">
      <div class="trio-item reveal"><span class="trio-num">1</span><h3>Выбираете пакет</h3><p>Напишите нам в WhatsApp: подскажем номинал и количество сертификатов под ваш бюджет.</p></div>
      <div class="trio-item reveal"><span class="trio-num">2</span><h3>Получаете именные сертификаты</h3><p>Оформляем сертификат на каждого получателя — со своим номером и QR-кодом.</p></div>
      <div class="trio-item reveal"><span class="trio-num">3</span><h3>Получатель приходит в клинику</h3><p>Записывается в WhatsApp и пользуется услугами на всю сумму сертификата.</p></div>
    </div>
  </div>
</section>

<!-- ============ КОМУ ПОДОЙДЁТ ============ -->
<section class="section teaser-gray">
  <div class="container container-narrow">
    <h2 class="h2 h2-sm reveal">Кому подойдёт</h2>
    <div class="fit-grid">
      <div class="fit-item reveal"><i></i><span>Компаниям, которые хотят дополнить соцпакет сотрудников</span></div>
      <div class="fit-item reveal"><i></i><span>Для подарков коллективу к праздникам</span></div>
      <div class="fit-item reveal"><i></i><span>Для благодарности клиентам и партнёрам</span></div>
      <div class="fit-item reveal"><i></i><span>Для мотивации лучших сотрудников</span></div>
    </div>
  </div>
</section>

<!-- ============ ПРИЗЫВ ============ -->
<section class="section biz-cta">
  <div class="container">
    <div class="biz-cta-card reveal">
      <div>
        <h2>Подарите здоровье <br>своей команде</h2>
        <p>Напишите нам — подготовим предложение с условиями и описанием пакетов для вашей компании.</p>
      </div>
      <div class="biz-cta-btns">{wa_btn('Обсудить в WhatsApp', 'btn btn-white btn-lg')}<a class="btn btn-outline" href="{BIZ_OFFER}" {ext}>Скачать предложение</a></div>
    </div>
  </div>
</section>

''' + social()
page('business.html', 'Для бизнеса — корпоративные сертификаты AIVA CLINIC', 'Корпоративные сертификаты AIVA Clinic: компания платит до 50% меньше номинала, получатель пользуется услугами клиники на всю сумму. Три пакета: Базовый, Стандарт, Gold.', business)

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
