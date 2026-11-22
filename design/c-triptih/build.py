# -*- coding: utf-8 -*-
"""Сборка главной georgygromov.com, направление C «Триптих» (выбрано Георгием 22.11.2026).

Запуск: python3 build.py  ->  index.html рядом.
Тексты: text.py. Расписание: timeline.py. Нотная лента: score.py (из версии v2, без изменений).
Фото лежат в foto/ и подключаются файлами, шрифт Bravura берётся из ../../assets/fonts/.
Текстовые шрифты пока с Google Fonts (Forum, Ysabeau Office); перед запуском на домене
положить их в assets/fonts.
"""
import os, html
import text as T
import timeline as TL
import score
import raspisanie as R
R_DEFAULT = "a"   # вариант расписания на главной (index.html); остальные в raspisanie-<x>.html

HERE = os.path.dirname(os.path.abspath(__file__))
TODAY = "2026-11-22"
FONTS_REL = "../../assets/fonts"


def e(s):
    return html.escape(s, quote=True)


def q(s):
    return f"«{e(s)}»"


def section_head(anchor, eyebrow, title):
    return (f'<div class="eyebrow">{e(eyebrow)}</div>'
            f'<h2 class="roman" id="{anchor}-h">{e(title)}</h2>')


def band(photo, pos, quote, who, role, cls=""):
    cap = ""
    if quote:
        cap = (f'<blockquote>{q(quote)}<cite>{e(who)}<span>{e(role)}</span></cite></blockquote>')
    return (f'<figure class="band {cls}"><img src="foto/{photo}.jpg" alt="" loading="lazy" '
            f'style="object-position:{pos}">{cap}</figure>')


def main(variant=R_DEFAULT):
    # ---------------- первый экран
    leaves = []
    for anchor, title, sub, photo, pos, wait in T.LEAVES:
        w = f'<span class="wait">{e(wait)}</span>' if wait else ''
        leaves.append(
            f'<a class="leaf" href="#{anchor}"><img src="foto/{photo}.jpg" alt="{e(T.NAME)}: {e(title.lower())}" '
            f'style="object-position:{pos}">{w}'
            f'<div class="cap"><div class="r roman">{e(title)}</div><div class="s">'
            + '<br>'.join(e(x) for x in sub.split('\n')) + '</div></div></a>')
    nav = ''.join(f'<a href="#{a}">{e(t)}</a>' for a, t in T.NAV)
    # Меню вынесено из .tri: иначе наведение на меню сужало все створки сразу.
    # Имя лежит внутри .tri с pointer-events:none, наведение проходит сквозь него на створку.
    hero = (f'<header class="cover"><div class="top"><h1 class="brand roman">{e(T.NAME)}</h1>'
            f'<nav aria-label="Разделы">{nav}</nav></div>'
            f'<div class="tri">{"".join(leaves)}'
            f'</div></header>')

    # ---------------- Миссия (под первым экраном)
    paths = ''.join(f'<div class="path"><h3 class="roman">{e(t)}</h3>'
                    + ''.join(f'<p>{e(p)}</p>' for p in ps) +
                    f'<a class="more-link" href="#{a}">Подробнее →</a></div>'
                    for a, t, ps in T.MISSION)
    mission = (f'<section class="sec mission"><blockquote class="motto roman">«{e(T.SLOGAN)}»'
               f'<cite>{e(T.NAME)}</cite></blockquote>'
               + ''.join(f'<p class="big">{e(p)}</p>' for p in T.MISSION_LEAD) +
               f'<div class="paths">{paths}</div></section>')

    # ---------------- Музыкант
    refs = ''.join(
        f'<figure class="ref"><img src="foto/{ph}.jpg" alt="{e(n)}" loading="lazy">'
        f'<figcaption><blockquote>{q(t)}</blockquote><cite>{e(n)}<span>{e(r)}</span></cite></figcaption></figure>'
        for ph, t, n, r in T.REFS)
    gal = ''.join(
        f'<a class="g" href="foto/{ph}.jpg" target="_blank" rel="noopener">'
        f'<img src="foto/{ph}.jpg" alt="{e(c) or "Георгий Громов на концерте"}" loading="lazy">'
        + (f'<span>{e(c)}</span>' if c else '') + '</a>'
        for ph, c in T.GALLERY) + f'<div class="g g-wait"><span>{e(T.GALLERY_WAIT)}</span></div>'
    vids = ''.join(
        f'<figure class="vid"><div class="frame"><iframe src="https://www.youtube-nocookie.com/embed/{v}" '
        f'title="{e(t)}" loading="lazy" allow="encrypted-media; picture-in-picture; fullscreen" '
        f'allowfullscreen></iframe></div><figcaption><b>{e(t)}</b><span>{e(n)}</span></figcaption></figure>'
        for v, t, n in T.VIDEOS)
    d, where, who, prog = T.NEXT
    nxt = (f'<div class="next"><div class="lbl">{e(T.NEXT_LABEL)}</div>'
           f'<div class="d roman">{e(d)}</div><div class="w">{e(who)}{"<br>" + e(prog) if prog else ""}</div>'
           f'<div class="p">{e(where)}</div></div>')
    def voice_grid(items):
        if not items:
            return ''
        return '<div class="voices">' + ''.join(
            f'<div><blockquote>{q(t)}</blockquote><cite>{e(n)}<span>{e(r)}</span></cite></div>'
            for t, n, r in items) + '</div>'
    press = ''.join(f'<p>{q(t)}</p>' for t in T.PRESS)
    muz = (f'<section class="sec" id="muzykant">{section_head("muzykant", T.MUZ_EYEBROW, "Музыкант")}'
           f'<div class="refs">{refs}</div>'
           f'<div class="cols bio"><div><p class="big">{e(T.MUZ_LEAD)}</p>'
           + ''.join(f'<p>{e(p)}</p>' for p in T.MUZ) +
           f'{nxt}</div><div class="gallery">{gal}</div></div>'
           f'<div class="vids">{vids}</div></section>'
           + band(*T.BAND_MUZ[:2], *T.BAND_MUZ[2:]) +
           f'<div class="press"><div class="lbl">Пресса</div>{press}<small>{e(T.PRESS_SRC)}</small></div>'
           f'<div class="comp"><h3 class="roman">{e(T.COMP_H)}</h3><div class="cols"><div>'
           + ''.join(f'<p>{e(p)}</p>' for p in T.COMP) +
           f'</div><blockquote>{e(T.COMP_QUOTE[0])}<cite>{e(T.COMP_QUOTE[1])}</cite></blockquote></div></div>')

    # ---------------- Коуч
    formats = ''.join(f'<li><b>{e(a)}</b><span>{e(b)}</span></li>' for a, b in T.FORMATS)
    clients = ''.join(f'<span>{e(c)}</span>' for c in T.CLIENTS)
    kou = (f'<section class="sec" id="kouch">{section_head("kouch", T.KOU_EYEBROW, "Коуч")}'
           f'<div class="cols"><div><p class="big">{e(T.KOU_LEAD)}</p>'
           + ''.join(f'<p>{e(p)}</p>' for p in T.KOU) +
           f'</div><div><div class="lbl">Форматы</div><ul class="formats">{formats}</ul>'
           f'<div class="lbl">Клиенты</div><div class="clients">{clients}</div></div></div></section>'
           + band(*T.BAND_KOU, "" if T.BAND_KOU[2] else "short")
           + voice_grid(T.VOICES_KOU))

    # ---------------- Просветитель
    ak = ''.join(f'<li><span class="when">{e(a)}</span><span class="what">{e(c)}<i>{e(b)}</i></span></li>'
                 for a, b, c in T.AKADEM)
    pro = (f'<section class="sec" id="prosvetitel">{section_head("prosvetitel", T.PRO_EYEBROW, "Просветитель")}'
           f'<div class="cols"><div><p class="big">{e(T.PRO_LEAD)}</p>'
           + ''.join(f'<p>{e(p)}</p>' for p in T.PRO) +
           f'</div><div><div class="lbl">Курсы</div><ul class="formats">'
           + ''.join(f'<li><b>{e(a)}</b><span>{e(b)}</span></li>' for a, b in T.COURSES) +
           f'</ul><div class="lbl">Мастер-классы и выступления</div><ul class="akadem">{ak}</ul></div></div></section>'
           + band(*T.BAND_PRO, "" if T.BAND_PRO[2] else "short")
           + voice_grid(T.VOICES_PRO) +
           f'<section class="sec trips-sec"><div class="trips"><figure><img src="foto/p2.jpg" alt="" loading="lazy"></figure>'
           f'<div><h3 class="roman">{e(T.TRIPS_H)}</h3><p>{e(T.TRIPS)}</p>'
           f'<a class="more-link" href="{e(T.TRIPS_LINK[1])}">{e(T.TRIPS_LINK[0])} →</a></div></div>'
           f'<div class="academy"><h3 class="roman">{e(T.ACADEMY_H)}</h3><p class="big">{e(T.ACADEMY)}</p></div>'
           f'</section>' + voice_grid(T.ACADEMY_VOICES))

    # ---------------- Расписание
    ev = TL.TIMELINE
    vname, _ = R.VARIANTS[variant]
    switch = ''.join(
        f'<a href="{"index.html" if k == R_DEFAULT else f"raspisanie-{k}.html"}#raspisanie"'
        f'{" class=on" if k == variant else ""}>Вариант {k.upper()} {e(n)}</a>'
        for k, (n, _) in R.VARIANTS.items())
    lenta = (f'<section class="sec" id="raspisanie">{section_head("raspisanie", "концерты, лекции, мастер-классы", T.LENTA_H)}'
             f'<div class="vswitch">{switch}</div>'
             f'<p class="intro">{e(T.LENTA_INTRO[variant])}</p>'
             f'<div class="sch">{R.render(variant)}</div></section>')

    # ---------------- Контакт
    kon = (f'<section class="sec contact" id="kontakt">{section_head("kontakt", "концерты, лекции, мастер-классы", T.KON_H)}'
           f'<p class="big">{e(T.KON)}</p><a class="mail" href="mailto:{T.MAIL}">{T.MAIL}</a></section>'
           f'<footer><span>© {e(T.NAME)}, Берлин</span>'
           f'<span>Нотная графика: шрифт Bravura (OFL). Мелодия: W. A. Mozart, KV 525, такты 1–7</span>'
           f'<span class="credits">{e(T.PHOTO_CREDITS)}</span></footer>')

    page = TEMPLATE.replace("{{TITLE}}", e(T.TITLE)).replace("{{DESC}}", e(T.DESC)) \
        .replace("{{FONTS}}", FONTS_REL) \
        .replace("{{SCH_CSS}}", R.CSS).replace("{{SCH_JS}}", R.JS) \
        .replace("{{BODY}}", hero + "<main>" + mission + muz + kou + pro + lenta + kon + "</main>")
    out = "index.html" if variant == R_DEFAULT else f"raspisanie-{variant}.html"
    with open(os.path.join(HERE, out), "w", encoding="utf-8") as f:
        f.write(page)
    print(f"собрано: {out} ({len(page)/1024:.0f} КБ), событий {len(ev)}")


TEMPLATE = r"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<meta property="og:title" content="{{TITLE}}">
<meta property="og:description" content="{{DESC}}">
<meta property="og:image" content="foto/p3.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Forum&family=Ysabeau+Office:ital,wght@0,300;0,400;0,600;1,300&display=swap" rel="stylesheet">
<style>
@font-face{font-family:'Bravura';src:url({{FONTS}}/bravura.woff2) format('woff2');font-display:block}
:root{--night:#0D0F0E;--night2:#151816;--chalk:#ECEAE3;--sage:#A9C8B6;--dim:#8F958F;--line:rgba(236,234,227,.2);
  --k-concert:#A9C8B6;--k-duo:#E6A57E;--k-lecture:#8FB3D9;--k-master:#C9A3D6}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--night);color:var(--chalk);font:300 19px/1.6 'Ysabeau Office',system-ui,sans-serif}
img{display:block;max-width:100%}
a{color:inherit}
.roman{font-family:'Forum',serif;text-transform:uppercase;letter-spacing:.08em;font-weight:400}
.lbl{color:var(--sage);font-size:15px;margin:0 0 12px}

/* ---------- первый экран ---------- */
.cover{position:relative}
.tri{position:relative;height:100svh;min-height:600px;display:flex}
.leaf{position:relative;flex:1;overflow:hidden;transition:flex-grow .7s cubic-bezier(.2,.7,.2,1);text-decoration:none;color:var(--chalk)}
.leaf img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1) brightness(.72);transition:filter .8s,transform 1.2s}
.leaf::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(13,15,14,.94) 0%,rgba(13,15,14,0) 55%),linear-gradient(180deg,rgba(13,15,14,.55) 0%,rgba(13,15,14,0) 18%)}
.leaf+.leaf{border-left:1px solid rgba(236,234,227,.25)}
.tri:hover .leaf{flex-grow:.7}
.tri .leaf:hover{flex-grow:2.2}
.leaf:hover img,.leaf:focus-visible img{filter:grayscale(0) saturate(1.08) brightness(.97);transform:scale(1.03)}
.cap{position:absolute;z-index:2;left:clamp(16px,2.4vw,36px);right:clamp(16px,2.4vw,36px);bottom:clamp(36px,8vh,80px)}
.cap .r{font-size:clamp(26px,2.8vw,44px);line-height:1}
.cap .s{font-size:16px;line-height:1.5;color:var(--sage);max-width:28em;opacity:0;max-height:0;overflow:hidden;margin-top:0;transition:opacity .5s,max-height .6s,margin-top .6s}
.leaf:hover .s,.leaf:focus-visible .s{opacity:1;max-height:12em;margin-top:12px}
.wait{position:absolute;z-index:2;top:64px;left:14px;background:#fff3b0;color:#3a3200;font:12px/1.3 system-ui;padding:4px 8px}
.top{position:absolute;z-index:4;top:0;right:0;left:0;display:flex;justify-content:space-between;align-items:baseline;gap:20px;padding:20px clamp(16px,2.4vw,36px)}
.top nav{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:clamp(16px,2.4vw,34px)}
.brand{margin:0;font-size:clamp(18px,1.6vw,24px);line-height:1;letter-spacing:.14em;color:var(--chalk)}
.top a{text-decoration:none;font-size:16px;color:var(--chalk);opacity:.85}
.top a:hover{opacity:1;color:var(--sage)}
.name{position:absolute;z-index:3;left:0;right:0;bottom:0;padding:0 clamp(16px,2.4vw,36px) clamp(22px,4vh,40px);pointer-events:none;display:flex;justify-content:space-between;align-items:flex-end;gap:20px}
.mission{padding-top:clamp(90px,12vw,180px)}
.motto{margin:0;font-size:clamp(40px,6.4vw,112px);line-height:.98;letter-spacing:.04em;max-width:11em}
.motto cite{display:block;margin-top:24px;font:300 17px/1.3 'Ysabeau Office';letter-spacing:.04em;text-transform:none;color:var(--sage)}
.mission .big{max-width:30em;margin:clamp(40px,6vw,80px) 0 0}
.mission .big + .big{margin-top:.8em}
.paths{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(20px,3vw,48px);margin-top:clamp(36px,5vw,64px)}
.path{display:flex;flex-direction:column;border-top:1px solid var(--sage);padding-top:20px}
.path h3{font-size:clamp(22px,2vw,30px);line-height:1.1;margin:0 0 14px}
.path p{margin:0 0 .9em;color:var(--chalk);opacity:.88}
.path .more-link{margin-top:auto;align-self:flex-start}
.name .q{max-width:24em;font-style:italic;font-size:clamp(15px,1.15vw,18px);text-align:right}
.name .q b{display:block;font-style:normal;font-weight:600;color:var(--sage);margin-top:6px;font-size:14px;letter-spacing:.04em}

/* ---------- разделы ---------- */
.sec{padding:clamp(80px,11vw,160px) clamp(16px,5vw,80px) clamp(40px,6vw,80px)}
.eyebrow{color:var(--sage);font-size:17px}
.sec h2{margin:.15em 0 0;font-size:clamp(56px,9vw,160px);line-height:.9}
.cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(24px,5vw,90px);margin-top:clamp(30px,5vw,70px)}
.big{font-size:clamp(22px,2vw,30px);line-height:1.38;margin:0 0 1em}
.cols p{margin:0 0 1em}
.halls,.formats,.akadem{list-style:none;margin:0 0 36px;padding:0;border-top:1px solid var(--line)}
.halls li{display:flex;justify-content:space-between;gap:16px;padding:13px 0;border-bottom:1px solid var(--line);font-size:18px}
.halls li span:last-child{color:var(--dim)}
.formats li{padding:16px 0;border-bottom:1px solid var(--line)}
.formats b{display:block;font-weight:400;font-size:21px;line-height:1.3}
.formats span{display:block;color:var(--dim);font-size:16px;margin-top:4px}
.clients{display:flex;flex-wrap:wrap;gap:10px 28px;font-family:'Forum',serif;font-size:21px}
.akadem li{display:grid;grid-template-columns:8.5em 1fr;gap:16px;padding:14px 0;border-bottom:1px solid var(--line);font-size:17px}
.akadem .when{color:var(--sage)}
.akadem i{display:block;font-style:normal;color:var(--dim);font-size:15px;margin-top:2px}
.next{border:1px solid var(--sage);padding:22px 24px;margin-top:36px}
/* отзывы музыкантов под заголовком */
.refs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(24px,3.5vw,56px);margin-top:clamp(36px,5vw,64px)}
.ref{margin:0;display:grid;grid-template-columns:88px 1fr;gap:20px;align-items:start}
.ref img{width:88px;height:88px;border-radius:50%;object-fit:cover;filter:grayscale(1);border:1px solid var(--line)}
.ref blockquote{margin:0;font-size:clamp(18px,1.4vw,21px);line-height:1.42}
.ref cite{display:block;margin-top:14px;font-style:normal;font-size:15px;color:var(--sage);letter-spacing:.04em;text-transform:uppercase}
.ref cite span{display:block;text-transform:none;letter-spacing:0;color:var(--dim);margin-top:2px}
.bio{margin-top:clamp(60px,8vw,110px)}
/* галерея */
.gallery{display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:clamp(150px,15vw,230px);gap:10px;align-self:start}
.g{position:relative;display:block;overflow:hidden;background:var(--night2)}
.g:first-child{grid-row:span 2}
.g img{width:100%;height:100%;object-fit:cover;transition:transform .8s,filter .6s;filter:saturate(.85)}
.g:hover img{transform:scale(1.04);filter:saturate(1)}
.g span{position:absolute;left:10px;bottom:8px;font-size:13px;color:var(--chalk);text-shadow:0 1px 6px rgba(0,0,0,.8)}
.g-wait{grid-column:span 2;display:flex;align-items:center;justify-content:center;border:1px dashed var(--dim);background:transparent}
.g-wait span{position:static;color:var(--dim);font-size:14px;text-shadow:none;text-align:center;padding:10px}
/* видео */
.vids{display:grid;grid-template-columns:1fr 1fr;gap:clamp(20px,3vw,48px);margin-top:clamp(60px,8vw,110px)}
.vid{margin:0}
.frame{position:relative;aspect-ratio:16/9;background:#000}
.frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.vid figcaption{margin-top:12px}
.vid b{display:block;font-weight:400;font-size:19px}
.vid span{display:block;color:var(--dim);font-size:15px;margin-top:2px}
footer .credits{flex-basis:100%;font-size:12px}
.next .d{font-size:clamp(30px,2.6vw,40px);line-height:1;margin-bottom:10px}
.next .w{font-size:18px;line-height:1.45}
.next .p{color:var(--dim);font-size:15px;margin-top:8px}

.band{position:relative;margin:0;min-height:86svh;display:flex;align-items:flex-end}
.band.short{min-height:64svh}
.band img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1) brightness(.62)}
.band blockquote{position:relative;z-index:1;margin:0;padding:clamp(24px,5vw,80px);max-width:1100px;font-family:'Forum',serif;font-size:clamp(30px,4.2vw,68px);line-height:1.08}
.band cite{display:block;margin-top:24px;font:600 15px/1.3 'Ysabeau Office';letter-spacing:.06em;text-transform:uppercase;color:var(--sage)}
.band cite span{display:block;font-weight:300;text-transform:none;letter-spacing:0;color:var(--chalk);font-size:16px;margin-top:4px}

.voices{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(20px,3vw,48px);padding:clamp(50px,7vw,100px) clamp(16px,5vw,80px) 0}
.voices blockquote{margin:0;font-size:clamp(20px,1.6vw,24px);line-height:1.4}
.voices cite{display:block;margin-top:16px;font-style:normal;font-size:15px;color:var(--sage);letter-spacing:.04em;text-transform:uppercase}
.voices cite span{display:block;text-transform:none;letter-spacing:0;color:var(--dim);margin-top:2px}
.press{margin:clamp(40px,5vw,70px) clamp(16px,5vw,80px) 0;padding:28px 0 0;border-top:1px solid var(--line);columns:2;column-gap:clamp(24px,5vw,90px)}
.press .lbl{column-span:all}
.press p{margin:0 0 14px;font-style:italic;break-inside:avoid}
.press small{color:var(--dim);font-size:14px;display:block}

.trips{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(24px,5vw,90px);align-items:center}
.comp{margin:clamp(70px,9vw,130px) clamp(16px,5vw,80px) 0;padding-top:clamp(40px,5vw,70px);border-top:1px solid var(--line)}
.comp h3{font-size:clamp(30px,3.4vw,54px);line-height:1;margin:0}
.comp .cols{margin-top:clamp(20px,3vw,40px);align-items:center}
.comp blockquote{margin:0;font-family:'Forum',serif;font-size:clamp(34px,4vw,64px);line-height:1.05;color:var(--sage)}
.comp cite{display:block;margin-top:16px;font:300 16px/1.4 'Ysabeau Office';color:var(--dim)}
.academy{margin-top:clamp(70px,9vw,130px);padding-top:clamp(40px,5vw,70px);border-top:1px solid var(--line);max-width:1100px}
.academy h3{font-size:clamp(30px,3.4vw,54px);line-height:1;margin:0 0 24px}
.academy .big{margin:0}
.academy + .voices,.sec .academy ~ .voices{padding-top:0}
.trips-sec{padding-top:clamp(70px,9vw,130px)}
.voices + .sec{padding-top:clamp(90px,12vw,170px)}
.trips figure{margin:0}
.trips img{width:100%;max-height:80svh;object-fit:cover;filter:saturate(.7)}
.trips h3{font-size:clamp(28px,3vw,48px);line-height:1.05;margin:0 0 20px}
.more-link{display:inline-block;margin-top:10px;color:var(--sage);text-decoration:none;border-bottom:1px solid var(--sage);padding-bottom:2px}

/* ---------- нотная лента ---------- */
.intro{max-width:40em;margin:30px 0 0}
.sc-scroll{overflow-x:auto;overflow-y:hidden;margin-top:40px;padding-bottom:8px;scrollbar-color:var(--dim) transparent}
.sc{display:block}
.sc-gl{font-family:'Bravura';font-size:56px;fill:var(--chalk)}
.sc-staff,.sc-bar,.sc-led{stroke:var(--chalk);stroke-opacity:.45;stroke-width:1.1}
.sc-stem{stroke:var(--chalk);stroke-width:1.7}.sc-stem-s{stroke-width:1.1}
.sc-beam,.sc-dot{fill:var(--chalk)}
.sc-rest{fill:var(--chalk);opacity:.55}.sc-small{font-size:31px;opacity:.5}.sc-empty{fill:var(--chalk);opacity:.25}
.sc-year{font-family:'Ysabeau Office';font-size:15px;fill:var(--dim);text-anchor:middle}
.sc-ytick{stroke:var(--line);stroke-width:1}
.sc-hit{fill:transparent;cursor:pointer}
.sc-note{outline:none}
.sc-note .sc-head{transition:transform .18s;transform-box:fill-box;transform-origin:center}
.k-concert .sc-head{fill:var(--k-concert)}.k-duo .sc-head{fill:var(--k-duo)}
.k-lecture .sc-head{fill:var(--k-lecture)}.k-master .sc-head{fill:var(--k-master)}
.sc-note:hover .sc-head,.sc-note:focus-visible .sc-head,.sc-note.on .sc-head{transform:scale(1.42)}
.sc-note:focus-visible .sc-hit{stroke:var(--sage);stroke-width:1.5}
.legend{display:flex;flex-wrap:wrap;gap:9px 26px;margin-top:20px;font-size:15px;color:var(--dim)}
.legend span{display:inline-flex;align-items:center;gap:9px}
.legend i{width:12px;height:9px;border-radius:50%;transform:rotate(-20deg);display:block}
.legend .k-concert{background:var(--k-concert)}.legend .k-duo{background:var(--k-duo)}
.legend .k-lecture{background:var(--k-lecture)}.legend .k-master{background:var(--k-master)}
.evcard{margin-top:30px;border-top:1px solid var(--line);padding-top:22px;min-height:120px}
.evcard span{display:block}
.evcard .when{color:var(--sage);font-size:16px}
.evcard .what{font-family:'Forum',serif;font-size:clamp(24px,2.4vw,36px);line-height:1.15;margin:6px 0}
.evcard .where{color:var(--dim);font-size:16px}

.contact .big{max-width:28em;margin-top:30px}
.mail{display:inline-block;font-family:'Forum',serif;font-size:clamp(28px,4.6vw,72px);text-decoration:none;border-bottom:1px solid var(--sage);line-height:1.1;word-break:break-all}
.mail:hover{color:var(--sage)}
footer{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px 30px;padding:40px clamp(16px,5vw,80px);color:var(--dim);font-size:14px;border-top:1px solid var(--line);margin-top:60px}

@media (max-width:820px){
  .tri{flex-direction:column;height:auto;min-height:0}
  .leaf{height:46svh;flex:none}
  .leaf+.leaf{border-left:0;border-top:1px solid rgba(236,234,227,.25)}
  .tri:hover .leaf,.tri .leaf:hover{flex-grow:0}
  .cap{bottom:20px}.cap .s{opacity:1;max-height:none;margin-top:10px}
  .wait{top:14px}
  .top{position:absolute}
  .top nav{display:none}
  .name{position:relative;background:var(--night);flex-direction:column;align-items:flex-start;padding-top:28px}
  .name .q{text-align:left}
  .cols,.voices,.trips,.paths,.refs,.vids{grid-template-columns:1fr}
  .ref{grid-template-columns:64px 1fr}.ref img{width:64px;height:64px}
  .press{columns:1}
  .akadem li{grid-template-columns:1fr;gap:2px}
  .band{min-height:70svh}.band.short{min-height:50svh}
}
@media (hover:none){.leaf img{filter:saturate(.9) brightness(.85)}}
{{SCH_CSS}}
.vswitch{display:flex;flex-wrap:wrap;gap:8px;margin-top:26px}
.vswitch a{border:1px dashed var(--dim);padding:6px 12px;font-size:14px;text-decoration:none;color:var(--dim)}
.vswitch a.on{border-style:solid;border-color:#F2D27A;color:#F2D27A}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto}}
</style>
</head>
<body>
{{BODY}}
<script>{{SCH_JS}}</script>
</body>
</html>
"""

if __name__ == "__main__":
    for v in R.VARIANTS:
        main(v)
