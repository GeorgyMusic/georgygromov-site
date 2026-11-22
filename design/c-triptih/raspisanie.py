# -*- coding: utf-8 -*-
"""Блок «Расписание»: три варианта (22.11.2026, просьба Георгия).

A «Сезоны»   – по нотному стану на каждый сезон (сентябрь–август), мелодия Моцарта целиком
               помещается в ширину, новый сезон сверху.
B «Месяцы»   – одна длинная лента, каждая нота – месяц; тема звучит дважды (как экспозиция
               с повтором); в подсказке все события месяца.
C «Афиша»    – карточка особого концерта, переключатель сезонов и список ближайших событий.

Во всех вариантах подсказка всплывает рядом с нотой (а не под станом) и нота не сдвигается.
render(variant) -> (html, css, js). Используется build.py и сборкой страниц сравнения.
"""
import html as H
from collections import Counter, OrderedDict
import score
import timeline as TL

TODAY = "2026-11-22"
SHORT = ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]


def e(s):
    return H.escape(s, quote=True)


def legend(kinds):
    return '<div class="legend">' + ''.join(
        f'<span><i class="k-{k}"></i>{e(v)}</span>' for k, v in kinds.items() if k != 'none') + '</div>'


def staff(events, kinds, bars=None, label=None, cls=''):
    svg, left = score.build(events, kinds, None, TODAY, TL.human, bars=bars, label=label)
    if left > 0:
        raise SystemExit(f"не поместилось событий: {left}")
    return f'<div class="sc-scroll {cls}">{svg}</div>'


def month_label(iso):
    return SHORT[int(iso[5:7]) - 1]


def by_season():
    seasons = OrderedDict()
    for ev in sorted(TL.TIMELINE):
        seasons.setdefault(TL.season(ev[0]), []).append(ev)
    return seasons


# ------------------------------------------------------------------ A
def variant_a():
    rows = []
    for s, evs in reversed(list(by_season().items())):
        cnt = Counter(k for _, k, *_ in evs)
        rows.append(
            f'<div class="season"><div class="season-h"><b class="roman">Сезон {e(s)}</b>'
            f'<span>{len(evs)} событий</span></div>{staff(evs, TL.KINDS, label=month_label, cls="fit")}</div>')
    return legend(TL.KINDS) + '<div class="seasons">' + ''.join(rows) + '</div>'


# ------------------------------------------------------------------ B
def variant_b():
    evs = sorted(TL.TIMELINE)
    first, last = evs[0][0][:7], evs[-1][0][:7]
    months = []
    y, m = int(first[:4]), int(first[5:])
    while f"{y:04d}-{m:02d}" <= last:
        months.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            y, m = y + 1, 1
    prio = ["concert", "duo", "master", "lecture", "course"]
    kinds = dict(TL.KINDS, none="без событий")
    items = []
    for ym in months:
        mevs = [x for x in evs if x[0].startswith(ym)]
        if mevs:
            c = Counter(x[1] for x in mevs)
            top = max(c.items(), key=lambda kv: (kv[1], -prio.index(kv[0])))[0]
            lines = "\n".join(f"{int(x[0][8:])} · {x[2]}" + (f" · {x[3]}" if x[3] else "") for x in mevs)
            hl = any(len(x) > 4 and x[4] for x in mevs)
            when_iso = mevs[-1][0]
            items.append((when_iso, top, lines, f"{len(mevs)} " + plural(len(mevs)), hl))
        else:
            items.append((ym + "-28", "none", "", "без событий", False))
    # подпись: месяц и год текстом
    def hum(iso):
        return f"{TL.MONTHS_NOM[int(iso[5:7]) - 1]} {iso[:4]}"
    svg, left = score.build(items, kinds, None, TODAY, hum, bars=score.BARS * 2,
                            label=lambda iso: iso[:4])
    if left > 0:
        raise SystemExit(f"не поместилось месяцев: {left}")
    return legend(TL.KINDS) + f'<div class="sc-scroll long" data-start="{TODAY[:7]}">{svg}</div>'


def plural(n):
    if n % 10 == 1 and n % 100 != 11:
        return "событие"
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return "события"
    return "событий"


# ------------------------------------------------------------------ C
def variant_c():
    d, tag, title, what, where = TL.HIGHLIGHT
    card = (f'<div class="hl-card"><div class="tag">{e(tag)}</div>'
            f'<div class="d roman">{e(d)}</div><div class="t roman">{e(title)}</div>'
            f'<div class="p">{e(what)} · {e(where)}</div></div>')
    seasons = list(by_season().items())
    cur = TL.season(TODAY)
    tabs = ''.join(f'<button type="button" class="tab{" on" if s == cur else ""}" data-s="{e(s)}">{e(s)}</button>'
                   for s, _ in reversed(seasons))
    panes = ''.join(f'<div class="pane{" on" if s == cur else ""}" data-s="{e(s)}">'
                    f'{staff(evs, TL.KINDS, label=month_label, cls="fit")}</div>'
                    for s, evs in seasons)
    up = [x for x in sorted(TL.TIMELINE) if x[0] >= TODAY][:6]
    lst = ''.join(f'<li class="k-{k}{" is-hl" if len(x) > 4 and x[4] else ""}"><span class="when">{e(TL.human(x[0]))}</span>'
                  f'<span class="what">{e(x[2])}</span><span class="where">{e(x[3])}</span></li>'
                  for x in up for k in [x[1]])
    return (card + f'<div class="tabs" role="tablist">{tabs}</div>' + legend(TL.KINDS) + panes +
            f'<div class="upnext"><div class="lbl">Ближайшие события</div><ul>{lst}</ul></div>')


VARIANTS = {"a": ("«Сезоны»", variant_a), "b": ("«Месяцы»", variant_b), "c": ("«Афиша»", variant_c)}


def render(v):
    return VARIANTS[v][1]() + '<div class="tip" role="tooltip" aria-hidden="true"></div>'


CSS = r"""
.sch{position:relative;margin-top:36px}
:root{--k-concert:#A9C8B6;--k-duo:#E6A57E;--k-course:#8FB3D9;--k-lecture:#D8C27A;--k-master:#C9A3D6;--k-none:#3a403c}
.k-course .sc-head{fill:var(--k-course)}.k-none .sc-head{fill:var(--k-none)}
.k-concert .sc-head{fill:var(--k-concert)}.k-duo .sc-head{fill:var(--k-duo)}
.k-lecture .sc-head{fill:var(--k-lecture)}.k-master .sc-head{fill:var(--k-master)}
.sc-note .sc-head{transform:none!important}
.sc-hov{fill:none;stroke:var(--chalk);stroke-width:1.4;opacity:0;transition:opacity .15s}
.sc-note:hover .sc-hov,.sc-note:focus-visible .sc-hov,.sc-note.on .sc-hov{opacity:1}
.sc-ring{fill:none;stroke:#F2D27A;stroke-width:2;stroke-dasharray:3 3}
.k-none{pointer-events:none}
.legend .k-course{background:var(--k-course)}
.sc-scroll.fit .sc{width:100%;height:auto;min-width:860px}
.sc-scroll.long{cursor:grab}
.season{margin-top:10px}
.season-h{display:flex;align-items:baseline;gap:16px;margin-top:26px}
.season-h b{font-size:clamp(20px,1.8vw,26px)}
.season-h span{color:var(--dim);font-size:15px}
.tip{position:absolute;z-index:30;left:0;top:0;width:max-content;max-width:min(340px,86vw);background:#1b201d;
  border:1px solid var(--sage);box-shadow:0 14px 34px rgba(0,0,0,.55);padding:14px 16px 13px;
  pointer-events:none;opacity:0;transform:translateY(6px);transition:opacity .14s,transform .14s;font-size:15px;line-height:1.4}
.tip.on{opacity:1;transform:none}
.tip::after{content:"";position:absolute;left:var(--ax,50%);width:12px;height:12px;background:#1b201d;
  border:1px solid var(--sage);border-top:0;border-left:0;transform:translateX(-50%) rotate(45deg);bottom:-7px}
.tip.below::after{bottom:auto;top:-7px;transform:translateX(-50%) rotate(225deg)}
.tip .k{display:flex;align-items:center;gap:8px;color:var(--sage);font-size:13px;letter-spacing:.03em}
.tip .k i{width:10px;height:8px;border-radius:50%;transform:rotate(-20deg)}
.tip .t{font-family:'Forum',serif;font-size:20px;line-height:1.15;margin:6px 0 4px;color:var(--chalk)}
.tip .p{color:var(--dim);font-size:14px}
.tip .fut{display:inline-block;margin-left:6px;color:#F2D27A}
.tip ul{list-style:none;margin:8px 0 0;padding:0}
.tip li{padding:5px 0;border-top:1px solid var(--line);font-size:14px}
.hl-card{border:1px solid #F2D27A;padding:24px 26px;max-width:640px;background:linear-gradient(135deg,rgba(242,210,122,.08),transparent)}
.hl-card .tag{color:#F2D27A;font-size:14px;letter-spacing:.06em;text-transform:uppercase}
.hl-card .d{font-size:clamp(26px,2.4vw,36px);margin-top:10px}
.hl-card .t{font-size:clamp(30px,3.4vw,52px);line-height:1;margin-top:6px}
.hl-card .p{color:var(--dim);margin-top:10px}
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin-top:40px}
.tab{background:transparent;color:var(--chalk);border:1px solid var(--line);padding:8px 14px;font:inherit;font-size:15px;cursor:pointer}
.tab.on{border-color:var(--sage);color:var(--sage)}
.pane{display:none}.pane.on{display:block}
.upnext{margin-top:40px}
.upnext ul{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.upnext li{display:grid;grid-template-columns:11em 1fr auto;gap:16px;padding:12px 0;border-bottom:1px solid var(--line);align-items:baseline}
.upnext li::before{content:"";display:none}
.upnext .when{color:var(--sage)}.upnext .where{color:var(--dim);font-size:15px}
.upnext li.is-hl .what{color:#F2D27A}
@media (max-width:820px){.upnext li{grid-template-columns:1fr;gap:2px}}
"""

JS = r"""
(function(){
  document.querySelectorAll('.sch').forEach(function(root){
    var tip=root.querySelector('.tip'), cur=null;
    function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
    function show(g){
      if(cur) cur.classList.remove('on'); cur=g; g.classList.add('on');
      var k=(g.getAttribute('class').match(/k-(\w+)/)||[])[1]||'';
      var fut=g.classList.contains('is-future')?'<span class="fut">впереди</span>':'';
      var what=g.dataset.what||'', where=g.dataset.where||'', body, head;
      if(g.closest('.long')){
        head='<div class="t">'+esc(g.dataset.when)+'</div><div class="p">'+esc(where)+fut+'</div>';
        body='<ul>'+what.split('\n').map(function(l){return '<li>'+esc(l)+'</li>';}).join('')+'</ul>';
        tip.innerHTML=head+body;
      } else {
        tip.innerHTML='<div class="k"><i style="background:var(--k-'+k+')"></i>'+esc(g.dataset.when)+' · '+esc(g.dataset.kind)+fut+'</div>'+
          '<div class="t">'+esc(what)+'</div>'+(where?'<div class="p">'+esc(where)+'</div>':'');
      }
      var wr=root.getBoundingClientRect(), r=g.querySelector('.sc-head').getBoundingClientRect();
      var x=r.left+r.width/2-wr.left, tw=tip.offsetWidth, th=tip.offsetHeight;
      var left=Math.max(4,Math.min(x-tw/2, wr.width-tw-4));
      var top=r.top-wr.top-th-16, below=false;
      if(r.top-th-16<8){top=r.bottom-wr.top+16; below=true;}
      tip.style.left=left+'px'; tip.style.top=top+'px'; tip.style.setProperty('--ax',(x-left)+'px');
      tip.classList.toggle('below',below); tip.classList.add('on'); tip.setAttribute('aria-hidden','false');
    }
    function hide(){ if(cur) cur.classList.remove('on'); cur=null; tip.classList.remove('on'); tip.setAttribute('aria-hidden','true'); }
    root.querySelectorAll('.sc-note').forEach(function(g){
      if(g.classList.contains('k-none')) return;
      g.addEventListener('mouseenter',function(){show(g);});
      g.addEventListener('mouseleave',hide);
      g.addEventListener('focus',function(){show(g);});
      g.addEventListener('blur',hide);
      g.addEventListener('click',function(ev){ev.stopPropagation(); cur===g?hide():show(g);});
      g.addEventListener('keydown',function(ev){if(ev.key==='Escape')hide();});
    });
    document.addEventListener('click',function(ev){ if(!root.contains(ev.target)) hide(); });
    root.querySelectorAll('.sc-scroll').forEach(function(sc){
      sc.addEventListener('scroll',hide,{passive:true});
      if(sc.classList.contains('long')){
        var target=sc.querySelector('.sc-note.is-future');
        if(target){ var b=target.getBBox?target.getBBox():null; sc.scrollLeft=Math.max(0,(b?b.x:0)-sc.clientWidth*0.35); }
        var down=false,sx=0,sl=0;
        sc.addEventListener('mousedown',function(ev){down=true;sx=ev.pageX;sl=sc.scrollLeft;});
        window.addEventListener('mouseup',function(){down=false;});
        sc.addEventListener('mousemove',function(ev){if(down){sc.scrollLeft=sl-(ev.pageX-sx);}});
      }
    });
    root.querySelectorAll('.tab').forEach(function(t){
      t.addEventListener('click',function(){
        hide();
        root.querySelectorAll('.tab').forEach(function(x){x.classList.toggle('on',x===t);});
        root.querySelectorAll('.pane').forEach(function(p){p.classList.toggle('on',p.dataset.s===t.dataset.s);});
      });
    });
  });
})();
"""
