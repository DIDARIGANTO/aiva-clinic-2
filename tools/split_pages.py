# Разовый скрипт: разбивает одностраничный index.html на главную и шесть внутренних страниц,
# а общие части (шапка, меню, футер) выносит в js/layout.js.
import re
src=open('index.html').read()
lines=src.split('\n')
def idx(pred, start=0):
    for i in range(start,len(lines)):
        if pred(lines[i]): return i
    raise ValueError
i_sprite=idx(lambda l: l.startswith('<!-- SVG-спрайт')); i_main=idx(lambda l: l=='<main>')
layout_top='\n'.join(lines[i_sprite:i_main]).rstrip()+'\n'
i_foot=idx(lambda l: l.startswith('<!-- ============ ФУТЕР')); i_foot_end=idx(lambda l: l=='</footer>')
footer='\n'.join(lines[i_foot:i_foot_end+1])
wa=[l for l in lines if l.startswith('<a class="wa-float"')][0]
head_end=idx(lambda l: l=='<body>')
head='\n'.join(lines[:head_end+1])
marks=[i for i,l in enumerate(lines) if l.startswith('<!-- ============ ') and i>i_main and i<i_foot and 'ФУТЕР' not in l]
i_main_end=idx(lambda l: l=='</main>')
blocks={}
for k,i in enumerate(marks):
    j=marks[k+1] if k+1<len(marks) else i_main_end
    name=re.sub(r'<!-- ============ \d*\.? ?','',lines[i]).split(' ====')[0].split(' (')[0].strip()
    blocks[name]='\n'.join(lines[i:j]).rstrip()+'\n'
B=blocks
hero=B['ГЛАВНЫЙ ЭКРАН']; promo=B['КАРТОЧКА-АКЦИЯ']; about=B['О КЛИНИКЕ']; prices=B['ПРАЙС-ЛИСТ']; doctors=B['НАШИ ВРАЧИ']; offers=B['АКЦИИ']
reviews=B['ОТЗЫВЫ: цифры и рейтинги']; slider=B['СЛАЙДЕР ОТЗЫВОВ']; services=B['УСЛУГИ']; steps=B['ПЕРВЫЙ ПРИЁМ']; booking=B['ЗАПИСЬ']; family=B['БОЛЬШОЕ ФОТО С ПОДПИСЬЮ']; social=B['СОЦСЕТИ']; contacts=B['КОНТАКТЫ']; maps=B['КЛИНИКА НА КАРТАХ']
navlinks=lambda s: re.findall(r'<a (?![^>]*data-href)[^>]*href="(#[^"]*)"',s)
L=layout_top
L=L.replace('<a class="logo" href="#top">','<a class="logo" href="index.html">')
L=L.replace('<a class="top-info top-info-addr" href="#contacts">','<a class="top-info top-info-addr" href="contacts.html">')
L=L.replace('<a class="btn btn-grad btn-sm top-cta" href="#booking">','<a class="btn btn-grad btn-sm top-cta" data-href="whatsappHref" href="https://wa.me/77472274096" target="_blank" rel="noopener">')
L=L.replace('<a class="branchbar-all" href="#contacts">','<a class="branchbar-all" href="contacts.html">')
for a,b in [('#about','about.html'),('#prices','prices.html'),('#doctors','doctors.html'),('#reviews','reviews.html'),('#offers','offers.html'),('#contacts','contacts.html')]:
    L=L.replace('href="%s"'%a,'href="%s"'%b)
assert not navlinks(L), navlinks(L)
F=footer
F=F.replace('<a class="logo logo-light" href="#top">','<a class="logo logo-light" href="index.html">')
for a,b in [('<div><h4>Основное</h4><a href="#top">Главная</a><a href="#about">О клинике</a><a href="#services">Услуги</a></div>','<div><h4>Основное</h4><a href="index.html">Главная</a><a href="about.html">О клинике</a><a href="prices.html">Прайс-лист</a></div>'),
            ('<div><h4>Клиника</h4><a href="#doctors">Наши врачи</a><a href="#offers">Акции</a><a href="#reviews">Отзывы о клинике</a><a href="#contacts">Контакты</a></div>','<div><h4>Клиника</h4><a href="doctors.html">Наши врачи</a><a href="offers.html">Акции</a><a href="reviews.html">Отзывы о клинике</a><a href="contacts.html">Контакты</a></div>'),
            ('<div><h4>Услуги</h4><a href="#svc-doctors">Консультации врачей</a><a href="#svc-uzi">Диагностика</a><a href="#svc-physio">Физиотерапия</a><a href="#svc-rehab">Реабилитация</a></div>','<div><h4>Услуги</h4><a href="prices.html#svc-doctors">Консультации врачей</a><a href="prices.html#svc-uzi">Диагностика</a><a href="prices.html#svc-physio">Физиотерапия</a><a href="prices.html#svc-rehab">Реабилитация</a></div>')]:
    assert a in F, a[:40]; F=F.replace(a,b)
assert not navlinks(F), navlinks(F)
layout_js='''/* ============================================================
   Общие части всех страниц: иконки, шапка, полоса с адресом,
   липкое меню, выезжающее меню, футер и кнопка WhatsApp.
   Правятся здесь один раз — и меняются на всех страницах.
   ============================================================ */
(function () {
  var TOP = `
'''+L+'''`;
  var BOTTOM = `
'''+F+'\n\n<!-- Плавающая кнопка WhatsApp -->\n'+wa+'''
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
assert '${' not in layout_js and layout_js.count('`')==4
open('js/layout.js','w').write(layout_js)
V='?v=16'
def page(fname, title, desc, body, bodyclass=''):
    h=head.replace('<title>AIVA CLINIC — клиника терапии, физиотерапии и реабилитации в Астане</title>','<title>%s</title>'%title)
    h=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="%s">'%desc,h)
    h=h.replace('css/style.css?v=15','css/style.css'+V)
    if bodyclass: h=h.replace('<body>','<body class="%s">'%bodyclass)
    out=h+'\n\n<main>\n\n'+body+'\n</main>\n\n<script src="js/config.js%s"></script>\n<script src="js/layout.js%s"></script>\n<script src="js/main.js%s"></script>\n</body>\n</html>\n'%(V,V,V)
    open(fname,'w').write(out); print('wrote',fname,len(out)//1024,'KB')
hero=hero.replace('<a class="btn btn-light btn-lg" href="#services">Выбрать услугу</a>','<a class="btn btn-light btn-lg" href="prices.html">Выбрать услугу</a>')
assert not navlinks(hero)
about_short='''<!-- ============ 3. О КЛИНИКЕ (кратко) ============ -->
<section class="section teaser" id="about">
  <div class="container container-narrow">
    <p class="eyebrow reveal">О клинике</p>
    <h2 class="h2 reveal">Врачи, диагностика и восстановление — <br>в одной клинике</h2>
    <p class="teaser-text reveal">AIVA CLINIC объединяет консультации врачей, диагностику, физиотерапию и восстановление. К нам можно обратиться с жалобами на самочувствие, для обследования или подбора программы реабилитации.</p>
    <div class="center reveal"><a class="btn btn-grad btn-lg glow" href="about.html">Подробнее о клинике</a></div>
  </div>
</section>

'''
cats=[('svc-doctors','Консультации врачей','терапевт, ВОП, гастроэнтеролог, эндокринолог, травматолог-ортопед, уролог-андролог'),
      ('svc-uzi','УЗИ-диагностика','органы, сосуды и комплексные исследования'),
      ('svc-checkup','Чек-апы','базовый, печень, щитовидная железа, сосуды, суставы'),
      ('svc-physio','Физиотерапия','TECAR, магнитотерапия, УВТ, ультразвук, прессотерапия'),
      ('svc-iv','Процедурный кабинет','капельницы и инъекции по назначению врача'),
      ('svc-rehab','Реабилитация','ЛФК, лечебный массаж, программы восстановления'),
      ('svc-lab','Лабораторные анализы','в составе чек-апов и по назначению врача')]
tiles=''.join('      <a class="cat reveal" href="prices.html#%s"><h3>%s</h3><p>%s</p><span>Смотреть →</span></a>\n'%c for c in cats)
prices_short='''<!-- ============ 4. ПРАЙС-ЛИСТ (кратко) ============ -->
<section class="section teaser teaser-gray" id="prices">
  <div class="container">
    <p class="eyebrow reveal">Прайс-лист</p>
    <h2 class="h2 reveal">Цены на услуги <br>AIVA CLINIC</h2>
    <div class="cat-grid">
'''+tiles+'''    </div>
    <div class="center reveal"><a class="btn btn-grad btn-lg glow" href="prices.html">Открыть прайс-лист</a></div>
  </div>
</section>

'''
doctors_home=doctors.replace('    </div>\n  </div>\n</section>','    </div>\n    <div class="center reveal" style="margin-top:40px"><a class="btn btn-light btn-lg" href="doctors.html">Все врачи</a></div>\n  </div>\n</section>')
assert 'doctors.html' in doctors_home
offers_short='''<!-- ============ 6. АКЦИИ (кратко) ============ -->
<section class="section offers" id="offers">
  <div class="container">
    <p class="eyebrow reveal">Акции</p>
    <h2 class="h2 reveal">Специальные <br>предложения</h2>
    <div class="offers-compact">
      <a class="offer-mini reveal" href="offers.html"><h3>Комплексные УЗИ</h3><p>Три комплекса исследований по сниженным ценам</p><b>от 15 000 ₸</b></a>
      <a class="offer-mini reveal" href="offers.html"><h3>Экзотерапия</h3><p>Магнитно-волновой массаж, скидка 30% на курс</p><b>6 000 ₸ / 5 мин</b></a>
      <a class="offer-mini reveal" href="offers.html"><h3>Чек-ап печени</h3><p>Анализы, УЗИ брюшной полости и приём врача</p><b>21 000 ₸</b></a>
    </div>
    <div class="center reveal"><a class="btn btn-grad btn-lg glow" href="offers.html">Все акции</a></div>
  </div>
</section>

'''
rat_start=reviews.index('    <div class="ratings">'); rat_end=reviews.index('    </div>\n', rat_start)+len('    </div>\n')
ratings_html=reviews[rat_start:rat_end]
reviews_short='''<!-- ============ 7. ОТЗЫВЫ (кратко) ============ -->
<section class="section teaser" id="reviews">
  <div class="container">
    <p class="eyebrow reveal">Отзывы</p>
    <h2 class="h2 reveal">Нам доверяют <br>своё здоровье</h2>
'''+ratings_html+'''    <div class="center reveal" style="margin-top:40px"><a class="btn btn-grad btn-lg glow" href="reviews.html">Все отзывы</a></div>
  </div>
</section>

'''
contacts_short='''<!-- ============ 10. КОНТАКТЫ (кратко) ============ -->
<section class="contacts contacts-short" id="contacts">
  <div class="container">
    <div class="contact-row">
      <div><h2 data-bind="address">Астана, ул. Е 669, 13</h2><p><svg><use href="#i-clock"/></svg><span data-bind="hours">Ежедневно с 08:00 до 20:00, без выходных</span></p><p><svg><use href="#i-phone"/></svg><a data-href="phoneHref" href="tel:+77472274096" data-bind="phone">+7 (747) 227-40-96</a></p></div>
      <div class="contact-row-btns">
        <a class="btn btn-outline" data-href="whatsappHref" href="https://wa.me/77472274096" target="_blank" rel="noopener"><svg><use href="#i-chat"/></svg>Написать в WhatsApp</a>
        <a class="btn btn-outline" href="contacts.html"><svg><use href="#i-route"/></svg>Схема проезда</a>
      </div>
    </div>
  </div>
</section>

'''
home=hero+'\n'+promo+'\n'+about_short+prices_short+doctors_home+'\n'+offers_short+reviews_short+booking+'\n'+social+'\n'+contacts_short
page('index.html','AIVA CLINIC — клиника терапии, физиотерапии и реабилитации в Астане','AIVA CLINIC в Астане: консультации врачей, УЗИ-диагностика, чек-апы, физиотерапия и реабилитация. Ежедневно с 08:00 до 20:00, ул. Е 669, 13.',home,'home')
page('about.html','О клинике — AIVA CLINIC','Как устроена работа AIVA CLINIC: консультация, индивидуальный подбор помощи, понятные следующие шаги.',about+'\n'+steps+'\n'+family+'\n'+booking,'page-inner')
page('prices.html','Прайс-лист — AIVA CLINIC','Цены на консультации, УЗИ-диагностику, чек-апы, физиотерапию, процедуры и реабилитацию в AIVA CLINIC.',services.replace('<p class="eyebrow reveal">Наши услуги</p>','<p class="eyebrow reveal">Направления</p>')+'\n'+prices+'\n'+booking,'page-inner')
page('doctors.html','Наши врачи — AIVA CLINIC','Врачи AIVA CLINIC: терапевт, врачи общей практики, эндокринолог, травматолог-ортопед, нейрохирург.',doctors+'\n'+booking,'page-inner')
page('reviews.html','Отзывы — AIVA CLINIC','Отзывы пациентов AIVA CLINIC в 2ГИС и на Яндекс Картах.',reviews+'\n'+slider+'\n'+booking,'page-inner')
page('offers.html','Акции — AIVA CLINIC','Специальные предложения AIVA CLINIC: комплексные УЗИ, экзотерапия, чек-ап печени.',offers+'\n'+booking,'page-inner')
page('contacts.html','Контакты — AIVA CLINIC','AIVA CLINIC: Астана, ул. Е 669, 13. Ежедневно с 08:00 до 20:00. Телефон и WhatsApp +7 (747) 227-40-96.',contacts+'\n'+maps,'page-inner')
s=open('css/style.css').read()
anchor='/* ============================================================\n   Наши врачи'
assert anchor in s
css='''/* ============================================================
   Короткие блоки главной страницы и внутренние страницы
   ============================================================ */
.teaser-gray { background: var(--gray-bg); }
.teaser-text { max-width: 760px; margin: -10px auto 32px; text-align: center; font-size: 18px; line-height: 1.6; }
.cat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; margin-bottom: 40px; }
.cat {
  display: flex; flex-direction: column; gap: 8px; padding: 24px 24px 22px; background: #fff; border: 1px solid var(--green); border-radius: 22px;
  transition: opacity 1s ease, transform 1s ease, box-shadow .3s;
}
.cat:hover { box-shadow: 0 20px 44px -22px rgba(114, 186, 69, .7); }
.cat h3 { font-size: 18px; line-height: 1.3; font-weight: 700; color: var(--green-dark); }
.cat p { font-size: 13px; line-height: 1.45; flex: 1; }
.cat span { font-size: 14px; font-weight: 600; color: var(--green); }
.offers-compact { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-bottom: 40px; }
.offer-mini {
  display: flex; flex-direction: column; gap: 8px; padding: 26px 26px 24px; background: #fff; border: 1px solid var(--green); border-radius: 22px;
  transition: opacity 1s ease, transform 1s ease, box-shadow .3s;
}
.offer-mini:hover { box-shadow: 0 20px 44px -22px rgba(114, 186, 69, .7); }
.offer-mini h3 { font-size: 20px; font-weight: 700; color: var(--green-dark); }
.offer-mini p { font-size: 14px; line-height: 1.45; flex: 1; }
.offer-mini b { font-size: 22px; font-weight: 700; color: var(--green-dark); }
.contacts-short { padding: 50px 0; }
.contact-row { display: flex; align-items: center; justify-content: space-between; gap: 40px; }
.contact-row h2 { font-size: 30px; line-height: 1.2; font-weight: 700; text-transform: uppercase; margin-bottom: 14px; }
.contact-row p { display: flex; align-items: center; gap: 10px; font-size: 18px; margin-bottom: 8px; }
.contact-row p svg { width: 24px; height: 24px; flex: none; }
.contact-row-btns { display: flex; flex-direction: column; gap: 12px; }
.contact-row-btns .btn-outline { min-width: 320px; }
.page-inner main > .section:first-child, .page-inner main > .contacts:first-child { padding-top: 70px; }
.stickynav nav a.is-active, .menu-panel nav a.is-active { color: var(--green); }
.stickynav nav a.is-active::after { transform: scaleX(1); }
.menu-panel nav a.is-active { color: var(--yellow); }

'''
s=s.replace(anchor,css+anchor)
m="  .cards { grid-template-columns: 1fr 1fr; }"; assert m in s
s=s.replace(m,m+"\n  .cat-grid { grid-template-columns: 1fr 1fr; }\n  .offers-compact { grid-template-columns: 1fr; }\n  .contact-row { flex-direction: column; align-items: stretch; }\n  .contact-row h2 { font-size: 24px; }\n  .contact-row-btns .btn-outline { min-width: 0; }")
m2="  .cards { grid-template-columns: 1fr; }"; assert m2 in s
s=s.replace(m2,m2+"\n  .cat-grid { grid-template-columns: 1fr; }")
open('css/style.css','w').write(s)
print('done')
