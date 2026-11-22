# -*- coding: utf-8 -*-
"""Сборка главной страницы georgygromov.com, версия от 6 ноября 2026.

Идея оформления: страница читается как партитура. Разделы помечены репетиционными
буквами в рамке - так дирижёр говорит «с буквы C». Над каждым разделом стоит
итальянская ремарка, которая честно описывает его характер. Единственный разделитель
на странице - пять линеек нотного стана. Цвет взят не из бумаги, а из вечернего зала:
сине-чёрные чернила, латунь духовых, бумажно-белый текст.

Шрифты вшиты в страницу (OFL): Cormorant Garamond - заголовки, Spectral - текст,
PT Sans Narrow - служебные надписи, Bravura - нотные знаки.
"""
import base64, os, sys
import text as T
import score

HERE = os.path.dirname(os.path.abspath(__file__))
import pathlib
# Фотографии лежат рядом со сборщиком: раньше путь вёл в /tmp, и сборка ломалась
# после перезапуска сервера. 2026-11-19 перенесено в сам проект.
FOTO = str(pathlib.Path(__file__).resolve().parent / "foto")
# Шрифты лежат в репозитории (assets/fonts), а не во временной папке: 2026-11-22.
FONTS = str(pathlib.Path(__file__).resolve().parents[2] / "assets")
TODAY = "2026-11-06"


def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()


def img(name):
    return "data:image/jpeg;base64," + b64(os.path.join(FOTO, name + ".jpg"))


def face(family, filename, weight="400", fmt="truetype", sub="fonts"):
    data = b64(os.path.join(FONTS, sub, filename))
    mime = "font/woff2" if fmt == "woff2" else "font/ttf"
    return (f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"font-display:swap;src:url(data:{mime};base64,{data}) format('{fmt}');}}")


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ---------------------------------------------------------------- шрифты
fonts = "".join([
    face("Cormorant", "CormorantGaramond%5Bwght%5D.ttf", "300 700"),
    face("Spectral", "Spectral-Regular.ttf", "400"),
    face("PTNarrow", "PT_Sans-Narrow-Web-Regular.ttf", "400"),
    face("PTNarrow", "PT_Sans-Narrow-Web-Bold.ttf", "700"),
    "@font-face{font-family:'Bravura';font-style:normal;font-weight:400;font-display:block;"
    "src:url(data:font/woff2;base64," + b64(os.path.join(FONTS, "fonts", "bravura.woff2")) + ") format('woff2');}",
])

# ---------------------------------------------------------------- стили
CSS = """
:root{
  --ink:#0E1220; --ink2:#151A2B; --ink3:#1D2335;
  --paper:#ECE8DF; --paper-dim:#A8ADBF; --mute:#767D93;
  --brass:#C2A05A; --brass-soft:#8C7236;
  --rule:rgba(236,232,223,.16); --rule-soft:rgba(236,232,223,.09);
  --k-concert:#DCB563; --k-duo:#D78B6D; --k-lecture:#6FA3A0; --k-master:#9A8BC0;
  --shade:rgba(8,10,18,.55);
}
:root:not([data-theme="dark"]){
  --ink:#E7E9EF; --ink2:#DDE0E9; --ink3:#D3D7E2;
  --paper:#141828; --paper-dim:#3C4257; --mute:#5C6379;
  --brass:#7E6222; --brass-soft:#9A7C33;
  --rule:rgba(20,24,40,.22); --rule-soft:rgba(20,24,40,.11);
  --k-concert:#9A7416; --k-duo:#A2552F; --k-lecture:#2F6B68; --k-master:#5C4B91;
  --shade:rgba(10,14,26,.45);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ink:#0E1220; --ink2:#151A2B; --ink3:#1D2335;
    --paper:#ECE8DF; --paper-dim:#A8ADBF; --mute:#767D93;
    --brass:#C2A05A; --brass-soft:#8C7236;
    --rule:rgba(236,232,223,.16); --rule-soft:rgba(236,232,223,.09);
    --k-concert:#DCB563; --k-duo:#D78B6D; --k-lecture:#6FA3A0; --k-master:#9A8BC0;
    --shade:rgba(8,10,18,.55);
  }
}
:root[data-theme="dark"]{
  --ink:#0E1220; --ink2:#151A2B; --ink3:#1D2335;
  --paper:#ECE8DF; --paper-dim:#A8ADBF; --mute:#767D93;
  --brass:#C2A05A; --brass-soft:#8C7236;
  --rule:rgba(236,232,223,.16); --rule-soft:rgba(236,232,223,.09);
  --k-concert:#DCB563; --k-duo:#D78B6D; --k-lecture:#6FA3A0; --k-master:#9A8BC0;
  --shade:rgba(8,10,18,.55);
}

*{box-sizing:border-box;}
body{
  margin:0; background:var(--ink); color:var(--paper);
  font-family:'Spectral',Georgia,serif; font-size:17px; line-height:1.62;
  -webkit-font-smoothing:antialiased; overflow-x:hidden;
}
h1,h2,h3{font-family:'Cormorant',Georgia,serif; font-weight:300; margin:0; text-wrap:balance;}
p{margin:0;}
a{color:inherit;}

.lbl{font-family:'PTNarrow',Arial,sans-serif; text-transform:uppercase;
     letter-spacing:.2em; font-size:12px; color:var(--mute);}

/* ---- каркас: слева поле с репетиционными буквами, как на дирижёрской партитуре */
.sheet{max-width:1180px; margin:0 auto; padding:0 28px;}
.sec{display:grid; grid-template-columns:72px minmax(0,1fr); gap:0 34px;
     padding:86px 0 10px; align-items:start;}
.rail{position:sticky; top:26px; display:flex; flex-direction:column; gap:10px; align-items:center;}
.rehearsal{font-family:'PTNarrow',Arial,sans-serif; font-weight:700; font-size:17px;
  line-height:1; letter-spacing:.04em; color:var(--brass);
  border:1.5px solid var(--brass); padding:7px 9px 6px; border-radius:1px;}
.marking{font-family:'Cormorant',Georgia,serif; font-style:italic; font-size:16px;
  color:var(--mute); writing-mode:vertical-rl; letter-spacing:.06em; white-space:nowrap;}
.body-col{min-width:0;}

h2{font-size:clamp(34px,5.2vw,58px); line-height:1.02; letter-spacing:-.015em; margin:0 0 26px;}
.prose{display:flex; flex-direction:column; gap:20px; max-width:65ch;}
.prose p{font-size:clamp(16.5px,1.5vw,19px);}
.lead{font-size:clamp(19px,2.1vw,24px) !important; line-height:1.48; color:var(--paper);}

/* ---- стан как единственный разделитель */
.staffrule{height:26px; margin:62px 0 0; position:relative;}
.staffrule i{position:absolute; left:0; right:0; height:1px; background:var(--rule-soft);}
.staffrule i:nth-child(1){top:0} .staffrule i:nth-child(2){top:6px}
.staffrule i:nth-child(3){top:12px} .staffrule i:nth-child(4){top:18px}
.staffrule i:nth-child(5){top:24px}

/* ---- первый экран */
.hero{position:relative; height:100svh; min-height:560px; overflow:hidden; background:var(--ink);}
.hero figure{position:absolute; inset:0; margin:0; opacity:0; transition:opacity 1.9s ease;}
.hero figure.on{opacity:1;}
.hero img{width:100%; height:100%; object-fit:cover; display:block;}
.hero .veil{position:absolute; inset:0;
  background:
    linear-gradient(92deg,rgba(8,10,18,.88) 0%,rgba(8,10,18,.66) 26%,rgba(8,10,18,.12) 58%,rgba(8,10,18,.1) 100%),
    linear-gradient(180deg,rgba(8,10,18,.55) 0%,rgba(8,10,18,.1) 30%,rgba(8,10,18,.45) 64%,rgba(8,10,18,.93) 100%);}
.hero-in{position:absolute; inset:auto 0 0 0; padding:0 28px 54px;}
.hero-wrap{max-width:1180px; margin:0 auto;}
.hero h1{font-size:clamp(50px,12.5vw,168px); line-height:.88; letter-spacing:-.025em;
  color:#F3F0E8; font-weight:300; text-shadow:0 2px 40px rgba(0,0,0,.5);}
.hero .kick{color:#DBD6C9; margin-bottom:18px;}
.hero .claim{font-family:'Cormorant',Georgia,serif; font-style:italic; font-weight:300;
  font-size:clamp(20px,2.6vw,31px); line-height:1.3; color:#E4DFD2; max-width:22ch; margin-top:22px;}
.hero-nav{display:flex; gap:22px; flex-wrap:wrap; margin-top:34px;}
.hero-nav a{color:#CFCABC; text-decoration:none; border-bottom:1px solid transparent; padding-bottom:3px;}
.hero-nav a:hover,.hero-nav a:focus-visible{color:#F3F0E8; border-bottom-color:var(--brass);}
.dots{position:absolute; right:30px; bottom:58px; display:flex; gap:9px;}
.dots b{width:7px; height:7px; border-radius:50%; background:rgba(243,240,232,.32); display:block;
  transition:background .5s;}
.dots b.on{background:var(--brass);}

/* ---- цифры */
.facts{display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:30px 26px;
  margin-top:48px; padding-top:34px; border-top:1px solid var(--rule);}
.facts div{display:flex; flex-direction:column; gap:7px;}
.facts b{font-family:'Cormorant',Georgia,serif; font-weight:300; font-size:clamp(40px,5vw,62px);
  line-height:.9; color:var(--brass); font-variant-numeric:tabular-nums;}

.twocol{display:grid; grid-template-columns:minmax(0,1.35fr) minmax(0,1fr); gap:46px; align-items:start;}
.shot{margin:0; position:relative;}
.shot img{width:100%; height:auto; display:block; filter:saturate(.92);}
.shot figcaption{margin-top:10px;}

.card{border-top:1px solid var(--rule); padding-top:18px; display:flex; flex-direction:column; gap:7px;}
.card h3{font-size:25px; font-weight:400; line-height:1.18;}
.card p{color:var(--paper-dim); font-size:16px;}
.cards{display:grid; gap:30px; margin-top:44px;}
@media(min-width:760px){.cards{grid-template-columns:repeat(3,1fr);}}

.next{margin-top:44px; border-left:2px solid var(--brass); padding:4px 0 4px 22px;
  display:flex; flex-direction:column; gap:6px;}
.next .d{font-family:'Cormorant',Georgia,serif; font-size:31px; font-weight:400;}

.rows{margin-top:40px; display:flex; flex-direction:column;}
.row{display:grid; grid-template-columns:150px minmax(0,1fr); gap:6px 26px;
  padding:17px 0; border-top:1px solid var(--rule-soft);}
.row:last-child{border-bottom:1px solid var(--rule-soft);}
.row .w{font-size:16px;}
.row .w b{display:block; font-weight:400;}
.row .w span{color:var(--mute); font-size:15px;}
@media(max-width:620px){.row{grid-template-columns:1fr;}}

.clients{display:flex; flex-wrap:wrap; gap:10px 28px; margin-top:38px; padding-top:26px;
  border-top:1px solid var(--rule);}
.clients span{font-family:'PTNarrow',Arial,sans-serif; letter-spacing:.14em;
  text-transform:uppercase; font-size:13px; color:var(--mute);}

.linkline{margin-top:30px; display:inline-flex; align-items:center; gap:10px;
  font-family:'PTNarrow',Arial,sans-serif; letter-spacing:.14em; text-transform:uppercase;
  font-size:13px; color:var(--brass); text-decoration:none;
  border-bottom:1px solid var(--brass-soft); padding-bottom:5px;}
.linkline:hover{color:var(--paper); border-bottom-color:var(--paper);}

/* ---- нотная лента */
.sc-wrap{margin-top:36px;}
.sc-scroll{overflow-x:auto; overflow-y:hidden; padding-bottom:6px;
  scrollbar-color:var(--brass-soft) transparent;}
.sc{display:block;}
.sc-gl{font-family:'Bravura'; font-size:56px; fill:var(--paper);}
.sc-staff{stroke:var(--paper); stroke-opacity:.5; stroke-width:1.1;}
.sc-bar{stroke:var(--paper); stroke-opacity:.5; stroke-width:1.3;}
.sc-led{stroke:var(--paper); stroke-opacity:.5; stroke-width:1.1;}
.sc-stem{stroke:var(--paper); stroke-width:1.7;}
.sc-stem-s{stroke-width:1.1;}
.sc-beam{fill:var(--paper);}
.sc-rest{fill:var(--paper); opacity:.55;}
.sc-small{font-size:31px; opacity:.5;}
.sc-dot{fill:var(--paper);}
.sc-empty{fill:var(--paper); opacity:.28;}
.sc-year{font-family:'PTNarrow',Arial,sans-serif; font-size:14px; letter-spacing:.16em;
  fill:var(--mute); text-anchor:middle;}
.sc-ytick{stroke:var(--rule); stroke-width:1;}
.sc-hit{fill:transparent; cursor:pointer;}
.sc-note{outline:none;}
.sc-note .sc-head{transition:fill .18s, transform .18s; transform-box:fill-box; transform-origin:center;}
.k-concert .sc-head{fill:var(--k-concert);} .k-duo .sc-head{fill:var(--k-duo);}
.k-lecture .sc-head{fill:var(--k-lecture);} .k-master .sc-head{fill:var(--k-master);}
.sc-note:hover .sc-head,.sc-note:focus-visible .sc-head,.sc-note.on .sc-head{transform:scale(1.42);}
.sc-note:focus-visible .sc-hit{stroke:var(--brass); stroke-width:1.5;}

.legend{display:flex; flex-wrap:wrap; gap:9px 26px; margin-top:22px;}
.legend span{display:inline-flex; align-items:center; gap:9px;
  font-family:'PTNarrow',Arial,sans-serif; text-transform:uppercase; letter-spacing:.13em;
  font-size:12px; color:var(--mute);}
.legend i{width:11px; height:8px; border-radius:50%; transform:rotate(-20deg); display:block;}

.evcard{margin-top:26px; border-top:1px solid var(--rule); padding-top:20px; min-height:112px;
  display:flex; flex-direction:column; gap:8px;}
.evcard .when{font-family:'PTNarrow',Arial,sans-serif; text-transform:uppercase;
  letter-spacing:.18em; font-size:12px; color:var(--brass);}
.evcard .what{font-family:'Cormorant',Georgia,serif; font-size:clamp(24px,3vw,34px);
  font-weight:400; line-height:1.14;}
.evcard .where{color:var(--mute); font-size:16px;}

/* ---- отзывы */
.quotes{display:grid; gap:1px; margin-top:40px; background:var(--rule-soft);}
@media(min-width:720px){.quotes{grid-template-columns:repeat(2,1fr);}}
.q{background:var(--ink); padding:28px 26px; display:flex; flex-direction:column; gap:12px;
   min-height:158px;}
.q .mark{font-family:'Cormorant',Georgia,serif; font-size:50px; line-height:.5; color:var(--brass);
  opacity:.5; height:22px;}
.q .pend{color:var(--mute); font-style:italic; font-family:'Cormorant',Georgia,serif; font-size:20px;}
.q .who{margin-top:auto;}
.q .who b{font-weight:400; display:block; font-size:17px;}
.q .who span{color:var(--mute); font-size:14px;}
.note{margin-top:26px; color:var(--mute); font-size:15.5px; max-width:62ch; font-style:italic;}

/* ---- контакт */
.mail{font-family:'Cormorant',Georgia,serif; font-size:clamp(30px,6vw,64px); font-weight:300;
  text-decoration:none; display:inline-block; margin-top:26px; letter-spacing:-.01em;
  border-bottom:1px solid var(--rule); padding-bottom:6px;}
.mail:hover{border-bottom-color:var(--brass); color:var(--brass);}
footer{padding:70px 0 54px; color:var(--mute); font-size:14px;
  display:flex; justify-content:space-between; gap:18px; flex-wrap:wrap;}

.skip{position:absolute; left:-9999px;}
.skip:focus{left:28px; top:14px; z-index:9; background:var(--ink2); color:var(--paper);
  padding:9px 15px; border:1px solid var(--brass);}
:focus-visible{outline:2px solid var(--brass); outline-offset:3px;}

@media(max-width:780px){
  .dots{bottom:auto; top:26px; right:22px;}
  .hero-nav{gap:16px 20px; margin-top:26px;}
  .sec{grid-template-columns:1fr; gap:0; padding-top:62px;}
  .rail{position:static; flex-direction:row; gap:14px; align-items:center; margin-bottom:20px;}
  .marking{writing-mode:horizontal-tb;}
  .twocol{grid-template-columns:1fr; gap:30px;}
}
@media (prefers-reduced-motion:reduce){
  *{animation:none !important; transition:none !important;}
}
"""

# ---------------------------------------------------------------- сборка
def section(letter, marking, anchor, inner):
    return (f'<section class="sec" id="{anchor}">'
            f'<div class="rail"><span class="rehearsal">{letter}</span>'
            f'<span class="marking">{marking}</span></div>'
            f'<div class="body-col">{inner}</div></section>')


def prose(paras, lead_first=True):
    out = []
    for i, p in enumerate(paras):
        cls = ' class="lead"' if (i == 0 and lead_first) else ''
        out.append(f'<p{cls}>{esc(p)}</p>')
    return '<div class="prose">' + ''.join(out) + '</div>'


RULE = '<div class="staffrule"><i></i><i></i><i></i><i></i><i></i></div>'


def main():
    ev = sorted(T.TIMELINE)
    svg, leftover = score.build(ev, T.KINDS, None, TODAY, T.human)
    if leftover > 0:
        print(f'ВНИМАНИЕ: {leftover} событий не поместилось в мелодию', file=sys.stderr)

    # первый экран
    figs = ''.join(
        f'<figure{" class=\"on\"" if i == 0 else ""}>'
        f'<img src="{img(n)}" alt="{esc(alt)}" style="object-position:{pos}"'
        f'{" loading=\"lazy\"" if i else ""}></figure>'
        for i, (n, alt, pos) in enumerate(T.HERO_SHOTS))
    dots = ''.join(f'<b{" class=\"on\"" if i == 0 else ""}></b>' for i in range(len(T.HERO_SHOTS)))
    nav = ''.join(f'<a href="#{a}">{esc(t)}</a>' for _, _, a, t in T.NAV[:6])

    hero = (f'<header class="hero" id="top">{figs}<div class="veil"></div>'
            f'<div class="hero-in"><div class="hero-wrap">'
            f'<div class="lbl kick">{esc(T.KICKER)}</div>'
            f'<h1>{esc(T.NAME)}</h1>'
            f'<p class="claim">{esc(T.CLAIM)}</p>'
            f'<nav class="hero-nav lbl">{nav}</nav>'
            f'</div></div><div class="dots">{dots}</div></header>')

    # A - кто я
    facts = ''.join(f'<div><b>{n}</b><span class="lbl">{esc(t)}</span></div>' for n, t in T.FACTS)
    a_in = (f'<h2>{esc(T.KTO_H)}</h2>'
            f'<div class="twocol"><div>{prose(T.KTO)}</div>'
            f'<figure class="shot"><img src="{img("p1")}" alt="Портрет Георгия Громова" loading="lazy">'
            f'</figure></div>'
            f'<div class="facts">{facts}</div>')

    # B - музыка
    b_in = (f'<h2>{esc(T.MUZ_H)}</h2>'
            f'<div class="twocol"><div>{prose(T.MUZ)}'
            f'<div class="next"><div class="lbl">{esc(T.NEXT_LABEL)}</div>'
            f'<div class="d">{esc(T.NEXT[0])}</div>'
            f'<div>{esc(T.NEXT[2])}</div>'
            f'<div style="color:var(--mute)">{esc(T.NEXT[3])}</div>'
            f'<div style="color:var(--mute)">{esc(T.NEXT[1])}</div></div></div>'
            f'<figure class="shot"><img src="{img("p2")}" alt="Георгий Громов дирижирует" loading="lazy">'
            f'</figure></div>')

    # C - лидерство
    cards = ''.join(f'<div class="card"><h3>{esc(h)}</h3><p>{esc(d)}</p></div>' for h, d in T.LID_ITEMS)
    clients = ''.join(f'<span>{esc(c)}</span>' for c in T.CLIENTS)
    c_in = (f'<h2>{esc(T.LID_H)}</h2>{prose(T.LID)}'
            f'<div class="cards">{cards}</div>'
            f'<div class="clients">{clients}</div>')

    # D - просвещение
    rows = ''.join(
        f'<div class="row"><div class="w"><b>{esc(d)}</b><span>{esc(place)}</span></div>'
        f'<div>{esc(what)}</div></div>' for d, place, what in T.AKADEM)
    d_in = (f'<h2>{esc(T.LEK_H)}</h2>'
            f'<div class="twocol"><div>{prose(T.LEK)}</div>'
            f'<figure class="shot"><img src="{img("p3")}" alt="Георгий Громов за пультом" loading="lazy">'
            f'</figure></div>'
            f'<div class="rows">{rows}</div>')

    # E - поездки
    e_in = (f'<h2>{esc(T.POE_H)}</h2>{prose(T.POE)}'
            f'<a class="linkline" href="{T.POE_LINK[1]}" target="_blank" rel="noopener">'
            f'{esc(T.POE_LINK[0])}</a>')

    # F - лента
    legend = ''.join(
        f'<span><i style="background:var(--k-{k})"></i>{esc(v)}</span>' for k, v in T.KINDS.items())
    last = ev[-1]
    f_in = (f'<h2>{esc(T.LENTA_H)}</h2>'
            f'<div class="prose"><p>{esc(T.LENTA)}</p></div>'
            f'<div class="sc-wrap"><div class="sc-scroll">{svg}</div>'
            f'<div class="legend">{legend}</div>'
            f'<div class="evcard" id="ev" aria-live="polite">'
            f'<span class="when">{esc(T.human(last[0]))} · {esc(T.KINDS[last[1]])}</span>'
            f'<span class="what">{esc(last[2])}</span>'
            f'<span class="where">{esc(last[3])}</span></div></div>')

    # G - отзывы
    qs = ''.join(
        f'<div class="q"><span class="mark">&#171;</span>'
        f'<span class="pend">текст ожидается</span>'
        f'<span class="who"><b>{esc(n)}</b><span>{esc(r)}</span></span></div>'
        for n, r in T.OTZ_SLOTS)
    g_in = (f'<h2>{esc(T.OTZ_H)}</h2><div class="quotes">{qs}</div>'
            f'<p class="note">{esc(T.OTZ_NOTE)}</p>')

    # H - контакт
    h_in = (f'<h2>{esc(T.KON_H)}</h2><div class="prose"><p class="lead">{esc(T.KON)}</p></div>'
            f'<a class="mail" href="mailto:{T.MAIL}">{T.MAIL}</a>')

    body = [hero, '<main class="sheet">']
    blocks = [a_in, b_in, c_in, d_in, e_in, f_in, g_in, h_in]
    for (letter, marking, anchor, _), inner in zip(T.NAV, blocks):
        body.append(section(letter, marking, anchor, inner))
        if anchor != T.NAV[-1][2]:
            body.append(f'<div class="sheet" style="padding:0">{RULE}</div>')
    body.append('<footer><span>© Георгий Громов, Берлин</span>'
                '<span>Нотная графика - шрифт Bravura (OFL). '
                'Мелодия - W. A. Mozart, KV 525, такты 1-7</span></footer>')
    body.append('</main>')

    js = """
<script>
(function(){
  var figs=document.querySelectorAll('.hero figure'), dots=document.querySelectorAll('.dots b'), i=0;
  if(figs.length>1 && !matchMedia('(prefers-reduced-motion: reduce)').matches){
    setInterval(function(){
      figs[i].classList.remove('on'); dots[i].classList.remove('on');
      i=(i+1)%figs.length;
      figs[i].classList.add('on'); dots[i].classList.add('on');
    },6200);
  }
  var box=document.getElementById('ev');
  function show(g){
    box.querySelector('.when').textContent=g.dataset.when+' · '+g.dataset.kind;
    box.querySelector('.what').textContent=g.dataset.what;
    box.querySelector('.where').textContent=g.dataset.where;
    var cur=document.querySelector('.sc-note.on'); if(cur) cur.classList.remove('on');
    g.classList.add('on');
  }
  document.querySelectorAll('.sc-note').forEach(function(g){
    g.addEventListener('mouseenter',function(){show(g);});
    g.addEventListener('focus',function(){show(g);});
    g.addEventListener('click',function(){show(g);});
    g.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){e.preventDefault();show(g);}
    });
  });
  var sc=document.querySelector('.sc-scroll');
  if(sc){ sc.scrollLeft=sc.scrollWidth; }
})();
</script>"""

    DESC = ('Пианист, дирижёр и коуч PCC ICF. Концерты, мастер-классы '
            'с живым оркестром, лекции о музыке.')
    head_bits = (f'<meta name="viewport" content="width=device-width, initial-scale=1">'
                 f'<title>Георгий Громов</title>'
                 f'<meta name="description" content="{DESC}">')
    inner = (f'<style>{fonts}{CSS}</style>'
             f'<a class="skip" href="#kto">К содержанию</a>' + ''.join(body) + js)

    # версия для артефакта: без doctype, head и body - их добавляет обёртка
    art = head_bits + inner
    out = os.path.join(HERE, 'artifact.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(art)

    # версия для настоящего хостинга: полноценный документ
    full = ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
            + head_bits +
            '<meta property="og:title" content="Георгий Громов">'
            f'<meta property="og:description" content="{DESC}">'
            '<meta property="og:type" content="website">'
            '<link rel="icon" href="data:image/svg+xml,'
            '%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E'
            '%3Crect width=%2732%27 height=%2732%27 fill=%27%230E1220%27/%3E'
            '%3Ctext x=%2716%27 y=%2723%27 font-size=%2722%27 text-anchor=%27middle%27 '
            'fill=%27%23C2A05A%27 font-family=%27Georgia,serif%27%3E%D0%93%3C/text%3E%3C/svg%3E">'
            '</head><body>' + inner + '</body></html>')
    outf = os.path.join(HERE, 'index.html')
    with open(outf, 'w', encoding='utf-8') as f:
        f.write(full)

    print(f'собрано: {out} ({len(art)/1048576:.2f} МБ) и {outf} ({len(full)/1048576:.2f} МБ), '
          f'событий {len(ev)}')


if __name__ == '__main__':
    main()
