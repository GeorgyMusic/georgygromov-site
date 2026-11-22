# -*- coding: utf-8 -*-
"""Нотная лента: первая тема «Маленькой ночной серенады» Моцарта, KV 525, I часть.

Каждая нота мелодии - одно событие из жизни Георгия. Цвет головки говорит о виде
события, пустая головка означает, что событие ещё впереди.

Источник мелодии - партия первой скрипки из издания Mutopia Project
(Breitkopf & Härtel, 1883), такты 1-7. Ничего не досочинено.
Нотные знаки рисуются шрифтом Bravura (SMuFL, лицензия OFL).
"""

STEP = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}

def num(p):
    """'G5' -> порядковый номер ступени. До первой октавы = 0."""
    return int(p[-1]) * 7 + STEP[p[0]]

# Такты 1-7. ('n', высота, длительность в восьмых) - нота,
# ('r', длительность) - пауза, ('orn', [высоты]) - четыре тридцать вторых.
BARS = [
    [('n', 'G5', 2), ('r', 1), ('n', 'D5', 1), ('n', 'G5', 2), ('r', 1), ('n', 'D5', 1)],
    [('n', 'G5', 1), ('n', 'D5', 1), ('n', 'G5', 1), ('n', 'B5', 1), ('n', 'D6', 2), ('r', 2)],
    [('n', 'C6', 2), ('r', 1), ('n', 'A5', 1), ('n', 'C6', 2), ('r', 1), ('n', 'A5', 1)],
    [('n', 'C6', 1), ('n', 'A5', 1), ('n', 'F5', 1), ('n', 'A5', 1), ('n', 'D5', 2), ('r', 2)],
    [('n', 'G5', 1), ('r', 1), ('n', 'G5', 3), ('n', 'B5', 1), ('n', 'A5', 1), ('n', 'G5', 1)],
    # 22.11.2026 по просьбе Георгия украшение (четыре тридцать вторых) заменено одной
    # восьмой G5: мелодия идёт без мелких нот, рисунок совпадает с тактом 7.
    [('n', 'G5', 1), ('n', 'F5', 1), ('n', 'F5', 3),
     ('n', 'A5', 1), ('n', 'C6', 1), ('n', 'F5', 1)],
    [('n', 'A5', 1), ('n', 'G5', 1), ('n', 'G5', 3), ('n', 'B5', 1), ('n', 'A5', 1), ('n', 'G5', 1)],
]

GLYPH = {
    'clef':   '\ue050',
    'sharp':  '\ue262',
    'four':   '\ue084',
    'black':  '\ue0a4',
    'hollow': '\ue0a3',
    'rest8':  '\ue4e6',
    'rest4':  '\ue4e5',
    'flag8':  '\ue241',
    'dot':    '\ue1e7',
}

SS = 14.0                 # нотный интервал
FS = SS * 4               # кегль Bravura: высота стана
EW = 31.0                 # ширина одной восьмой
HEAD = 132.0              # ключ, знаки при ключе, размер
BARGAP = 20.0
TOP = 74.0                # верхняя линейка стана
BOT = TOP + 4 * SS        # нижняя линейка
E4 = num('E4')            # нижняя линейка - ми первой октавы


def y_of(p):
    return BOT - (num(p) - E4) * (SS / 2)


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))


def build(events, kinds, colors, today, human):
    """events: список (дата, вид, что, где), уже отсортированный по дате."""
    out = []
    notes = []            # (x, высота, длительность, малая ли)
    runs = []             # группы восьмых под ребром
    bar_x = []

    x = HEAD
    for bi, bar in enumerate(BARS):
        bar_x.append(x)
        pos = x
        run = []
        for item in bar:
            if item[0] == 'n':
                _, p, d = item
                notes.append([pos, p, d, False])
                if d == 1:
                    run.append(len(notes) - 1)
                else:
                    if len(run) > 1: runs.append(run)
                    run = []
                pos += d * EW
            elif item[0] == 'r':
                if len(run) > 1: runs.append(run)
                run = []
                out.append(('rest', pos, item[1]))
                pos += item[1] * EW
            else:
                if len(run) > 1: runs.append(run)
                run = []
                sub = EW / 4.4
                orn = []
                for k, p in enumerate(item[1]):
                    notes.append([pos + k * sub, p, 0, True])
                    orn.append(len(notes) - 1)
                out.append(('ornbeam', orn))
                pos += EW
        if len(run) > 1: runs.append(run)
        x += 8 * EW + BARGAP

    total_w = x + 40
    svg = []
    svg.append(
        f'<svg class="sc" viewBox="0 0 {total_w:.0f} 220" width="{total_w:.0f}" height="220" '
        f'xmlns="http://www.w3.org/2000/svg" role="group" '
        f'aria-label="Мелодия Моцарта, в которой каждая нота - событие">')

    # стан
    for i in range(5):
        y = TOP + i * SS
        svg.append(f'<line class="sc-staff" x1="18" y1="{y:.1f}" x2="{total_w-22:.0f}" y2="{y:.1f}"/>')

    # ключ, диез, размер
    svg.append(f'<text class="sc-gl" x="30" y="{y_of("G4"):.1f}">{GLYPH["clef"]}</text>')
    svg.append(f'<text class="sc-gl" x="76" y="{y_of("F5"):.1f}">{GLYPH["sharp"]}</text>')
    svg.append(f'<text class="sc-gl" x="100" y="{y_of("D5"):.1f}">{GLYPH["four"]}</text>')
    svg.append(f'<text class="sc-gl" x="100" y="{y_of("G4"):.1f}">{GLYPH["four"]}</text>')

    # тактовые черты
    for i, bx in enumerate(bar_x):
        if i:
            svg.append(f'<line class="sc-bar" x1="{bx-BARGAP/2:.1f}" y1="{TOP:.1f}" '
                       f'x2="{bx-BARGAP/2:.1f}" y2="{BOT:.1f}"/>')
    svg.append(f'<line class="sc-bar" x1="{total_w-22:.0f}" y1="{TOP:.1f}" '
               f'x2="{total_w-22:.0f}" y2="{BOT:.1f}"/>')

    # паузы и рёбра тридцать вторых
    for kind, *rest in out:
        if kind == 'rest':
            pos, d = rest
            g = GLYPH['rest4'] if d >= 2 else GLYPH['rest8']
            svg.append(f'<text class="sc-gl sc-rest" x="{pos:.1f}" y="{y_of("B4"):.1f}">{g}</text>')
        else:
            idx = rest[0]
            x1 = notes[idx[0]][0] + 0.06 * SS
            x2 = notes[idx[-1]][0] + 0.06 * SS
            ybot = max(y_of(notes[i][1]) for i in idx) + 2.6 * SS
            for i in idx:
                notes[i].append(ybot)
            for b in range(3):
                yy = ybot - b * 0.42 * SS
                svg.append(f'<rect class="sc-beam" x="{x1:.1f}" y="{yy:.1f}" '
                           f'width="{x2-x1:.1f}" height="{0.26*SS:.1f}"/>')

    # рёбра восьмых
    for run in runs:
        x1 = notes[run[0]][0] + 0.06 * SS
        x2 = notes[run[-1]][0] + 0.06 * SS
        ybot = max(y_of(notes[i][1]) for i in run) + 3.5 * SS
        svg.append(f'<rect class="sc-beam" x="{x1:.1f}" y="{ybot:.1f}" '
                   f'width="{x2-x1:.1f}" height="{0.5*SS:.1f}"/>')
        for i in run:
            notes[i].append(ybot)

    beamed = {i for run in runs for i in run}

    # ноты
    ev_i = 0
    years = {}
    for i, n in enumerate(notes):
        nx, p, d, small = n[0], n[1], n[2], n[3]
        ny = y_of(p)
        sx = nx + 0.06 * SS

        # добавочные линейки
        for led in (num('A5'), num('C6'), num('E6')):
            if num(p) >= led:
                ly = BOT - (led - E4) * (SS / 2)
                svg.append(f'<line class="sc-led" x1="{nx-0.28*SS:.1f}" y1="{ly:.1f}" '
                           f'x2="{nx+1.46*SS:.1f}" y2="{ly:.1f}"/>')

        if small:
            svg.append(f'<text class="sc-gl sc-small" x="{nx:.1f}" y="{ny:.1f}">{GLYPH["black"]}</text>')
            svg.append(f'<line class="sc-stem sc-stem-s" x1="{sx:.1f}" y1="{ny+0.17*SS:.1f}" '
                       f'x2="{sx:.1f}" y2="{n[4]:.1f}"/>')
            continue

        # штиль вниз
        if i in beamed:
            stem_end = n[4]
        else:
            stem_end = ny + 3.5 * SS
        svg.append(f'<line class="sc-stem" x1="{sx:.1f}" y1="{ny+0.17*SS:.1f}" '
                   f'x2="{sx:.1f}" y2="{stem_end:.1f}"/>')
        if d == 1 and i not in beamed:
            svg.append(f'<text class="sc-gl" x="{sx:.1f}" y="{stem_end:.1f}">{GLYPH["flag8"]}</text>')
        if d == 3:
            dy = ny if (num(p) - E4) % 2 else ny - SS / 2
            svg.append(f'<text class="sc-gl sc-dot" x="{nx+1.7*SS:.1f}" y="{dy:.1f}">{GLYPH["dot"]}</text>')

        if ev_i < len(events):
            iso, kind, what, where = events[ev_i]
            future = iso > today
            head = GLYPH['hollow'] if future else GLYPH['black']
            cls = f'sc-note k-{kind}' + (' is-future' if future else '')
            yr = iso[:4]
            if yr not in years:
                years[yr] = nx
            svg.append(
                f'<g class="{cls}" tabindex="0" role="button" data-i="{ev_i}" '
                f'data-when="{esc(human(iso))}" data-kind="{esc(kinds[kind])}" '
                f'data-what="{esc(what)}" data-where="{esc(where)}" '
                f'aria-label="{esc(human(iso))}, {esc(kinds[kind])}, {esc(what)}">'
                f'<text class="sc-gl sc-head" x="{nx:.1f}" y="{ny:.1f}">{head}</text>'
                f'<circle class="sc-hit" cx="{nx+0.6*SS:.1f}" cy="{ny:.1f}" r="{1.5*SS:.1f}"/>'
                f'</g>')
            ev_i += 1
        else:
            svg.append(f'<text class="sc-gl sc-empty" x="{nx:.1f}" y="{ny:.1f}">{GLYPH["hollow"]}</text>')

    # годы над станом
    for yr, xx in sorted(years.items()):
        svg.append(f'<line class="sc-ytick" x1="{xx+0.6*SS:.1f}" y1="{TOP-30:.1f}" '
                   f'x2="{xx+0.6*SS:.1f}" y2="{TOP-12:.1f}"/>')
        svg.append(f'<text class="sc-year" x="{xx+0.6*SS:.1f}" y="{TOP-38:.1f}">{yr}</text>')

    svg.append('</svg>')
    return ''.join(svg), len(events) - ev_i
