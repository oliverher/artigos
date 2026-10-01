"""Infográficos animados dos artigos 01 a 03 (HTML/SVG), no lugar de uma figura estática de cada artigo."""
import math
from html import escape as e

DUR = 4.2
T0 = 0.2


def _pins(items):
    out = ''
    for n, (x, y, delay, label) in enumerate(items, 1):
        out += ('<span class="ig-pin" data-a="pop" style="left:%.2f%%;top:%.2f%%;--d:%.2fs" aria-hidden="true">%d</span>'
                % (x / 160 * 100, y / 62 * 100, delay, n))
        if label:
            out += ('<span class="ig-chip" data-a="up" style="left:%.2f%%;top:%.2f%%;--d:%.2fs" aria-hidden="true">%s</span>'
                    % (x / 160 * 100, y / 62 * 100, delay + .3, e(label)))
    return out


def _cards(steps, delays):
    out = ''
    for n, ((t, txt), d) in enumerate(zip(steps, delays), 1):
        out += ('<div class="ig-step" data-a="up" style="--d:%.2fs"><b><i aria-hidden="true">%d</i>%s</b><p>%s</p></div>'
                % (d, n, e(t), e(txt)))
    return '<div class="ig-steps">%s</div>' % out


# ------------------------------------------------- BPM: ciclo de cinco fases
def ciclo():
    a, cx, cy = 70, 80, 31
    pts = []
    for i in range(361):
        t = math.pi + i / 360 * 2 * math.pi
        k = 1 + math.sin(t) ** 2
        pts.append((cx + a * math.cos(t) / k, cy + 0.9 * a * math.sin(t) * math.cos(t) / k))
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(seg)
    d = 'M' + ' L'.join('%.2f,%.2f' % p for p in pts) + 'Z'
    items, delays = [], []
    for k in range(5):
        idx = int(len(seg) * (0.04 + 0.2 * k))
        frac = sum(seg[:idx]) / total
        dl = T0 + DUR * frac
        items.append((pts[idx][0], pts[idx][1], dl, ''))
        delays.append(dl + .15)
    steps = [('Fase 1: entendimento do negócio', 'Alinhamento estratégico e definição do “Ganho Central”.'),
             ('Fase 2: modelagem (AS-IS)', 'Mapeamento da realidade atual (notação BPMN).'),
             ('Fase 3: análise do processo', 'Identificação de gargalos, riscos e desconexões de valor.'),
             ('Fase 4: projeto (TO-BE)', 'Redesenho focado no estado futuro desejado e projeção de cenários.'),
             ('Fase 5: transformação', 'Execução do plano de ação e acompanhamento tático.')]
    return ('<div class="ig light" role="group" aria-label="Infográfico animado: o ciclo contínuo de cinco fases do frame-BPM.">'
            '<p class="ig-title">O motor da transformação: um ciclo de 5 fases</p>'
            '<div class="ig-maze ig-loop"><svg viewBox="0 0 160 62" preserveAspectRatio="none" aria-hidden="true">'
            '<path pathLength="1" d="%s"/><circle r="1.7" class="ig-dot"><animateMotion dur="9s" repeatCount="indefinite" path="%s"/></circle></svg>%s</div>%s</div>'
            ) % (d, d, _pins(items), _cards(steps, delays))


# ------------------------------------------------- Propósito: bússola em movimento
def trilha():
    def y(x, dy):
        return 38 - 0.16 * x + 5 * math.sin(x / 14) + dy
    bands = ''
    for dy, color, w, dl in [(-5, '#7f9fc2', 1.6, 0.0), (0, '#8fb89a', 1.8, .35), (5, '#efe9d8', 1.3, .7)]:
        d = 'M' + ' L'.join('%d,%.2f' % (x, y(x, dy)) for x in range(0, 161, 2))
        bands += '<path pathLength="1" class="band" style="stroke:%s;stroke-width:%s;animation-delay:%.2fs" d="%s"/>' % (color, w, T0 + dl, d)
    xs = [30, 80, 130]
    items = [(x, y(x, 0), T0 + DUR * x / 160 + .35, lab) for x, lab in zip(xs, ['Apoio social', 'Recursos materiais', ''])]
    steps = [('Adolescência', 'Articulado à construção da identidade. Não exige definição precoce isenta de ambivalência. A busca e a exploração são saudáveis (Krok, 2018).'),
             ('Idade adulta', 'Focado em vínculos de confiança, transições de papéis e inserção cultural. Organização de objetivos diante da realidade material.'),
             ('Velhice', 'Profundamente associado à conexão social e ao enfrentamento do declínio. A solidão é a maior ameaça ao propósito nesta fase (Neville et al., 2018).')]
    return ('<div class="ig slate" role="group" aria-label="Infográfico animado: o propósito de vida como uma bússola em movimento, da adolescência à velhice, atravessado por apoio social e recursos materiais.">'
            '<p class="ig-title ig-left">Uma bússola em movimento (desenvolvimento humano)</p>'
            '<p class="ig-lead" data-a="up">O propósito não é um destino cristalizado, mas uma orientação adaptativa que responde às fases da vida e às relações pessoa-ambiente.</p>'
            '<div class="ig-maze ig-river"><svg viewBox="0 0 160 62" preserveAspectRatio="none" aria-hidden="true">%s</svg>%s</div>%s</div>'
            ) % (bands, _pins(items), _cards(steps, [d + .15 for _, _, d, _ in items]))


# ------------------------------------------------- Mente e corpo: níveis de afirmação
def niveis():
    cols = [('Associação', 'Relação estatística.', '(Ex.: estresse e cicatrização lenta)', 'Não implica causalidade direta isolada.'),
            ('Mecanismo', 'Via fisiológica.', '(Ex.: carga alostática)', 'Plausibilidade celular não resolve a eficácia clínica.'),
            ('Intervenção', 'Teste de eficácia.', '(Ex.: relaxamento vs. cuidado usual)', 'Exige comparador adequado e desfecho definido.'),
            ('Experiência', 'Sentido vivido.', '(Ex.: escuta narrativa)', 'Aumenta o vínculo, mas não é diagnóstico etiológico.'),
            ('Interpretação simbólica', 'Correspondência hermenêutica.', '', 'Requer teste empírico rigoroso antes de ser transformada em afirmação de saúde.')]
    out = ''
    for i, (t, a, ex, b) in enumerate(cols):
        out += ('<div class="ig-col%s" data-a="up" style="--d:%.2fs"><h4>%s</h4><div><p>%s%s</p><p>%s</p></div></div>'
                % (' hot' if i == 4 else '', .15 + i * .5, e(t), e(a), (' <em>%s</em>' % e(ex)) if ex else '', e(b)))
    return ('<div class="ig light" role="group" aria-label="Infográfico animado: matriz crítica dos cinco níveis de afirmação, de associação a interpretação simbólica.">'
            '<p class="ig-title">A matriz crítica de níveis de afirmação (Quadro 3)</p><div class="ig-cols">%s</div></div>') % out
