"""Infográficos animados do artigo 04, em HTML/SVG, no lugar das imagens estáticas."""
import math
from html import escape as e

DUR = 4.2   # duração do desenho do labirinto (s), igual ao CSS
T0 = 0.2    # atraso inicial do desenho (s)


# ---------------------------------------------------------------- 1. Labirinto
MAZE = [(6, 8), (14, 30), (26, 18), (36, 34), (20, 48), (44, 52), (54, 26), (40, 12), (70, 10), (84, 30),
        (62, 42), (96, 54), (108, 22), (92, 8), (128, 6), (150, 14), (146, 30), (116, 36), (134, 50), (154, 44)]
PINS = [0, 5, 10, 15, 19]   # vértice do trajeto em que cada etapa aparece

STEPS = [
    ('Descoberta difusa', 'Informação via boca a boca, rodoviárias ou CRAS.'),
    ('Solicitação presencial', 'Deslocamento obrigatório ao Vapt Vupt, SEDS ou CRAS. Filas e risco de documentos faltantes.'),
    ('A caça aos papéis', 'Dificuldade extrema de reunir extratos do INSS e espelho do CadÚnico. Idas forçadas a lan houses.'),
    ('A caixa preta (até 60 dias)', 'Longa espera sem qualquer visibilidade ou acompanhamento do status.'),
    ('A retirada', 'Novo deslocamento físico apenas para buscar o papel.'),
]


def labirinto():
    seg = [math.dist(MAZE[i], MAZE[i + 1]) for i in range(len(MAZE) - 1)]
    total = sum(seg)
    d = 'M' + ' L'.join('%g,%g' % p for p in MAZE)
    pins, cards = '', ''
    for n, (vi, (t, txt)) in enumerate(zip(PINS, STEPS), 1):
        frac = sum(seg[:vi]) / total
        delay = T0 + DUR * frac
        x, y = MAZE[vi]
        pins += '<span class="ig-pin"%s style="left:%.2f%%;top:%.2f%%;--d:%.2fs" aria-hidden="true">%d</span>' % (
            ' data-a="pop"', x / 160 * 100, y / 62 * 100, delay, n)
        cards += ('<div class="ig-step" data-a="up" style="--d:%.2fs"><b><i aria-hidden="true">%d</i>%s</b><p>%s</p></div>'
                  % (delay + .15, n, e(t), e(txt)))
    return ('<div class="ig" role="group" aria-label="Infográfico animado: o labirinto burocrático da jornada atual, em cinco etapas.">'
            '<p class="ig-title">Diagnóstico AS IS: o labirinto burocrático</p>'
            '<div class="ig-maze"><svg viewBox="0 0 160 62" preserveAspectRatio="none" aria-hidden="true">'
            '<path pathLength="1" d="%s"/></svg>%s</div>'
            '<div class="ig-steps">%s</div>'
            '<p class="ig-quote" data-a="up" style="--d:%.2fs">O Estado exigia que a Sra. Maria Aparecida atuasse como <em>“mensageira”</em> '
            'entre órgãos governamentais que não se comunicavam.</p></div>') % (d, pins, cards, T0 + DUR + .3)


# ---------------------------------------------------------------- 2. Matriz
def _ico(p):
    return '<svg viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % p


ICO = [
    _ico('<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>'),
    _ico('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>'),
    _ico('<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>'),
    _ico('<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2 2M9 2h6"/>'),
    _ico('<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>'),
]
ROWS = [
    ('Informação difusa / passiva', 'Proativa via WhatsApp (aos 60 anos)'),
    ('Papel impresso. Dificuldade de reunir', 'Validação automática (INSS/CadÚnico). Digital'),
    ('Apenas presencial. Filas e deslocamento', 'Multicanal: EXPRESSO, WhatsApp ou presencial'),
    ('Até 60 dias de espera. Sem rastreamento', 'Emissão em 24h. Visibilidade total do status'),
    ('Deslocamento obrigatório para retirada', 'Documento digital imediato no celular'),
]


def matriz():
    rows = ''
    for i, ((a, b), ic) in enumerate(zip(ROWS, ICO)):
        d = .3 + i * .9
        rows += ('<div class="ig-mrow"><div class="ig-cell as" data-a="left" style="--d:%.2fs">%s<span>%s</span></div>'
                 '<div class="ig-cell to" data-a="right" style="--d:%.2fs"><span>%s</span></div></div>') % (d, ic, e(a), d + .45, e(b))
    return ('<div class="ig" role="group" aria-label="Infográfico animado: matriz de transformação estrutural, da situação atual (AS IS) à desejada (TO BE), em cinco dimensões.">'
            '<p class="ig-title">Matriz de transformação estrutural</p>'
            '<div class="ig-matrix"><div class="ig-mhead" aria-hidden="true"><span class="as" data-a="up">Situação atual (AS IS)</span>'
            '<span class="to" data-a="up" style="--d:.15s">Situação desejada (TO BE)</span></div>%s</div></div>') % rows


# ---------------------------------------------------------------- 3. Impacto
def impacto():
    return ('<div class="ig" role="group" aria-label="Infográfico animado: impacto operacional. Tempo de emissão de 60 dias para 24 horas na emissão automática, ou 5 dias úteis com análise.">'
            '<p class="ig-title">Impacto operacional: o salto de eficiência</p>'
            '<div class="ig-cards">'
            '<div class="ig-card" data-a="up" style="--d:.1s"><h4>Esforço humano</h4><p>Redução drástica de falhas operacionais e eliminação do retrabalho '
            'de servidores no balcão graças à integração automática SEDS/CadÚnico.</p></div>'
            '<div class="ig-card main" data-a="up" style="--d:.0s"><h4>Tempo de emissão</h4>'
            '<span class="ig-old">60 DIAS</span>'
            '<span class="ig-new"><span data-count data-from="60" data-to="24" data-delay="1900" data-dur="1500">24</span> HORAS</span>'
            '<span class="ig-foot">(Emissão automática) ou<br>5 dias úteis (com análise)</span></div>'
            '<div class="ig-card" data-a="up" style="--d:.2s"><h4>Transparência</h4>'
            '<span class="ig-big" data-count data-from="0" data-to="100" data-suffix="%" data-delay="700" data-dur="1600">100%</span>'
            '<p>Taxa de rastreabilidade do processo subiu para 100%, colocando o cidadão no controle do status via celular.</p></div>'
            '</div></div>')
