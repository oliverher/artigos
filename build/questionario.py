# -*- coding: utf-8 -*-
"""Gera, a partir de build/questionario_data.py:
  1) docs/ia-no-setor-publico/questionario/index.html  (página do site, só as perguntas, por dimensão)
  2) docs/assets/pdf/Questionario_Diagnostico_IA_Servidores_GO_perguntas.docx  (versão só com as perguntas)
  3) work/questionario/Questionario_v04_para_aplicacao.docx  (versão completa, não publicada)
"""
import html, os, sys
sys.path.insert(0, 'build')
import shell
import questionario_data as Q

S = 'docs'
SLUG = 'ia-no-setor-publico'
DOCX_NAME = 'Questionario_Diagnostico_IA_Servidores_GO_perguntas.docx'
e = html.escape

# ======================= página do site =======================
CSS = """
.q-wrap{max-width:48rem;margin:0 auto;padding:40px 24px 72px}
.q-note{border-left:3px solid var(--ochre);background:var(--accent);padding:12px 16px;border-radius:8px;font-size:15px;line-height:1.55;color:var(--accent-foreground)}
.q-scale{display:flex;flex-wrap:wrap;gap:6px 14px;margin:14px 0 0;padding:12px 16px;border:1px solid var(--border);border-radius:10px;background:var(--secondary);font-size:13px;color:var(--muted-foreground)}
.q-scale b{color:var(--primary)}
.q-sec{margin-top:44px}
.q-sec h2{display:flex;gap:14px;align-items:baseline;font-size:1.45rem;font-weight:600}
.q-sec h2 span{font-family:var(--font-display);color:var(--ochre);font-size:1.7rem}
.q-instr{margin-top:6px;font-size:14px;color:var(--muted-foreground)}
.q-list{list-style:none;margin:16px 0 0;padding:0;display:grid;gap:10px}
.q-item{border:1px solid var(--border);border-radius:12px;background:var(--card);padding:14px 16px;box-shadow:var(--shadow-soft)}
.q-n{display:inline-block;min-width:2.2rem;font-family:var(--font-display);font-weight:600;color:var(--ochre)}
.q-text{line-height:1.5}
.q-sc{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
.q-sc i{font-style:normal;display:grid;place-items:center;width:30px;height:30px;border-radius:999px;border:1.5px solid var(--border);font-size:12px;color:var(--muted-foreground);background:#fff}
.q-opts{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:6px}
.q-opts li{display:flex;gap:10px;align-items:center;font-size:15px;color:var(--muted-foreground)}
.q-opts li:before{content:"";flex:none;width:14px;height:14px;border:1.5px solid var(--border);border-radius:999px;background:#fff}
.q-flow{margin-top:8px;font-size:13px;font-style:italic;color:var(--muted-foreground)}
.q-line{margin-top:10px;height:64px;border:1px dashed var(--border);border-radius:8px;background:#fff}
.q-btn{display:inline-flex;gap:8px;align-items:center;margin-top:18px;padding:11px 22px;border-radius:999px;background:var(--ochre);color:var(--ochre-foreground);font-weight:600;font-size:14px;text-decoration:none}
.q-btn:hover{transform:translateY(-2px)}
@media print{nav,.q-btn,.q-back{display:none!important}.q-item{box-shadow:none;break-inside:avoid}}
"""


def _opts(opts):
    return '<ul class="q-opts">' + ''.join('<li>%s</li>' % e(o) for o in opts) + '</ul>'


def _single(items, n0):
    out, n = '', n0
    for code, text, opts, flow in items:
        out += '<li class="q-item"><span class="q-n">%d.</span><span class="q-text">%s</span>%s%s</li>' % (
            n, e(text), _opts(opts), ('<p class="q-flow">%s</p>' % e(flow) if flow else ''))
        n += 1
    return out, n


def page():
    n = 1
    parts = []
    # filtro e perfil
    a, n = _single(Q.FILTER + Q.PROFILE, n)
    parts.append(('A', 'Filtro e perfil', 'Todas as faixas são amplas e há a opção de não informar, para que combinações de respostas não identifiquem ninguém.', a))
    b, n = _single(Q.EXPERIENCE, n)
    parts.append(('B', 'Experiência com inteligência artificial', '', b))
    letters = 'CDEFGHIJKLMNOP'
    sc = '<div class="q-sc" aria-hidden="true">' + ''.join('<i>%d</i>' % k for k in range(1, 6)) + '</div>'
    for i, (key, title, instr, items) in enumerate(Q.DIMS):
        li = ''
        for code, text, inv, org in items:
            li += '<li class="q-item"><span class="q-n">%d.</span><span class="q-text">%s</span>%s</li>' % (n, e(text), sc)
            n += 1
        parts.append((letters[i], title, instr, li))
    ol = ''.join('<li class="q-item"><span class="q-n">%d.</span><span class="q-text">%s</span><div class="q-line"></div></li>' % (n + k, e(t)) for k, (c, t) in enumerate(Q.OPEN))
    parts.append((letters[len(Q.DIMS)], 'Perguntas abertas (opcionais)', Q.OPEN_NOTE, ol))
    secs = ''.join('<section class="q-sec" aria-labelledby="q-%s"><h2 id="q-%s"><span>%s</span>%s</h2>%s<ol class="q-list">%s</ol></section>'
                   % (p[0], p[0], p[0], e(p[1]), ('<p class="q-instr">%s</p>' % e(p[2]) if p[2] else ''), p[3]) for p in parts)
    legend = '<div class="q-scale" aria-label="Escala de resposta">' + ''.join('<span><b>%d</b> %s</span>' % (k + 1, e(t)) for k, t in enumerate(Q.SCALE)) + '</div>'
    header = ('<header class="relative overflow-hidden text-primary-foreground" style="background-image:var(--gradient-deep)">'
              '<div class="surface-paper absolute inset-0 opacity-30" aria-hidden="true"></div>'
              '<div class="relative mx-auto max-w-3xl px-6 py-16 sm:py-20">'
              '<p class="text-xs font-semibold uppercase tracking-[0.2em] text-ochre">Instrumento de pesquisa · Preliminar</p>'
              '<h1 class="mt-5 text-3xl leading-[1.15] font-semibold sm:text-4xl">%s</h1>'
              '<p class="mt-4 text-base leading-relaxed text-primary-foreground/80">Apenas as perguntas, separadas por dimensão. Acompanha o artigo sobre os fatores organizacionais associados à intenção de servidores públicos de aprender e usar IA.</p>'
              '<p class="mt-6 text-sm text-primary-foreground/70">Carlos Hernane de Oliveira</p></div></header>' % e(Q.TITLE))
    intro = ('<p class="q-note">%s</p>'
             '<p style="margin-top:18px;line-height:1.6;color:var(--muted-foreground)">São %d perguntas: %d afirmações em escala de 1 a 5, %d de filtro, perfil e experiência e %d abertas e opcionais. O tempo estimado de resposta é de 12 a 14 minutos, estimativa a confirmar no piloto. As respostas são anônimas.</p>'
             '<p style="margin-top:12px;line-height:1.6;color:var(--muted-foreground)">%s</p><p style="margin-top:10px;line-height:1.6;color:var(--muted-foreground)">%s</p>'
             % (e(Q.STATUS), Q.N_TOTAL, Q.N_SCALE, Q.N_OTHER, len(Q.OPEN), e(Q.DEFINITIONS[0]), e(Q.DEFINITIONS[1]))
             + legend + '<p class="q-instr" style="margin-top:12px">Em todas as afirmações das dimensões (partes C em diante), responda de 1 a 5 conforme a escala acima.</p>'
             '<a class="q-btn" href="../../assets/pdf/%s" download>Baixar as perguntas em Word</a>' % DOCX_NAME)
    foot = ('<footer class="border-t bg-card"><div class="mx-auto max-w-3xl px-6 py-10 text-sm text-muted-foreground">'
            '<p><a class="q-back underline underline-offset-2" href="../">Voltar ao artigo</a></p>'
            '<p class="mt-3">As escalas de segurança psicológica e de motivação para o serviço público vêm de versões validadas no Brasil (Ramalho e Porto, 2021; Assis, 2024). Os demais itens foram adaptados de Wolfe et al. (2025) e de Abbad e Sallorenzo (2001) ou são de redação própria, ainda sem validação.</p></div></footer>')
    return ('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>'
            '<title>%s</title><meta name="description" content="Apenas as perguntas do questionário, separadas por dimensão: intenção de aprender e usar IA, apoio, tempo, acesso, segurança para experimentar, regras, utilidade, confiança, propósito e receios."/>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter+Tight:wght@400;500;600&display=swap"/>'
            '<link rel="stylesheet" href="../../assets/styles.css"/><style>%s</style></head><body>' % (e(Q.TITLE), CSS)
            + shell.nav(SLUG, '../../') + '<div class="min-h-screen">' + header + '<main class="q-wrap">' + intro + secs + '</main>' + foot + '</div>'
            '<script src="../../assets/app.js"></script></body></html>')


# ======================= documentos Word =======================
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def _doc():
    d = Document()
    s = d.sections[0]
    s.left_margin = s.right_margin = Cm(2.2); s.top_margin = s.bottom_margin = Cm(2)
    st = d.styles['Normal']; st.font.name = 'Arial'; st.font.size = Pt(10.5)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
    return d


def _shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), color); tcPr.append(sh)


def _p(d, text, bold=False, italic=False, size=None, after=6, color=None, align=None):
    p = d.add_paragraph(); r = p.add_run(text); r.bold = bold; r.italic = italic
    if size: r.font.size = Pt(size)
    if color: r.font.color.rgb = RGBColor.from_string(color)
    p.paragraph_format.space_after = Pt(after)
    if align: p.alignment = align
    return p


def _h(d, text, level=1):
    p = d.add_paragraph(); r = p.add_run(text); r.bold = True
    r.font.size = Pt({1: 14, 2: 12, 3: 11}[level]); r.font.color.rgb = RGBColor.from_string('0F3D2A')
    p.paragraph_format.space_before = Pt(14 if level == 1 else 10); p.paragraph_format.space_after = Pt(4); p.paragraph_format.keep_with_next = True


def _single_q(d, n, code, text, opts, flow, show_code=False):
    p = d.add_paragraph(); r = p.add_run('%s%s. %s' % ((code + ' · ') if show_code else '', n, text)); r.bold = True
    p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(2); p.paragraph_format.keep_with_next = True
    for o in opts:
        q = d.add_paragraph('( )  ' + o); q.paragraph_format.left_indent = Cm(0.8); q.paragraph_format.space_after = Pt(0)
    if flow: _p(d, flow, italic=True, size=9, after=2, color='666666')


def _matrix(d, items, n0, show_code=False):
    t = d.add_table(rows=1, cols=6); t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths = [Cm(10.6)] + [Cm(1.1)] * 5
    hd = ['Afirmação', '1', '2', '3', '4', '5']
    for i, h in enumerate(hd):
        c = t.rows[0].cells[i]; c.text = ''; r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(9.5); _shade(c, 'D9E7DF'); c.width = widths[i]
        if i: c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    n = n0
    for code, text, inv, org in items:
        row = t.add_row().cells
        row[0].text = ''; r = row[0].paragraphs[0].add_run(('%s · ' % code if show_code else '') + '%d. %s' % (n, text)); r.font.size = Pt(10)
        for i in range(6):
            row[i].width = widths[i]
            if i:
                row[i].text = '( )'; row[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        n += 1
    d.add_paragraph().paragraph_format.space_after = Pt(2)
    return n


def _scale_legend(d):
    _p(d, 'Escala de resposta: ' + '; '.join('%d = %s' % (i + 1, s.lower()) for i, s in enumerate(Q.SCALE)) + '.', italic=True, size=9.5, after=6, color='444444')


def docx_questions(path):
    d = _doc()
    _p(d, Q.TITLE, bold=True, size=16, after=2, color='0F3D2A')
    _p(d, 'Versão apenas com as perguntas, separadas por dimensão', italic=True, size=11, after=6)
    _p(d, Q.STATUS, size=9.5, after=8, color='7A4B00')
    _p(d, '%d perguntas: %d afirmações em escala de 1 a 5, %d de filtro, perfil e experiência e %d abertas e opcionais. Tempo estimado: 12 a 14 minutos (estimativa a confirmar no piloto). Respostas anônimas.' % (Q.N_TOTAL, Q.N_SCALE, Q.N_OTHER, len(Q.OPEN)), after=6)
    for t in Q.DEFINITIONS: _p(d, t, after=4)
    n = 1
    _h(d, 'A. Filtro e perfil')
    for code, text, opts, flow in Q.FILTER + Q.PROFILE:
        _single_q(d, n, code, text, opts, flow); n += 1
    _h(d, 'B. Experiência com inteligência artificial')
    for code, text, opts, flow in Q.EXPERIENCE:
        _single_q(d, n, code, text, opts, flow); n += 1
    letters = 'CDEFGHIJKLMNOP'
    for i, (key, title, instr, items) in enumerate(Q.DIMS):
        _h(d, '%s. %s' % (letters[i], title))
        _p(d, instr, italic=True, size=9.5, after=3)
        if i == 0: _scale_legend(d)
        n = _matrix(d, items, n)
    _h(d, '%s. Perguntas abertas (opcionais)' % letters[len(Q.DIMS)])
    _p(d, Q.OPEN_NOTE, italic=True, size=9.5, after=3)
    for k, (c, t) in enumerate(Q.OPEN):
        _p(d, '%d. %s' % (n + k, t), bold=True, after=2)
        _p(d, '_' * 80, after=2, color='999999'); _p(d, '_' * 80, after=8, color='999999')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    d.save(path)


def _grid(d, head, rows, widths, size=9):
    t = d.add_table(rows=1, cols=len(head)); t.style = 'Table Grid'
    for i, h in enumerate(head):
        c = t.rows[0].cells[i]; c.text = ''; r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(size); _shade(c, 'D9E7DF'); c.width = Cm(widths[i])
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ''; r = cells[i].paragraphs[0].add_run(v); r.font.size = Pt(size); cells[i].width = Cm(widths[i])
    d.add_paragraph().paragraph_format.space_after = Pt(2)


def docx_full(path):
    d = _doc()
    _p(d, Q.TITLE, bold=True, size=16, after=2, color='0F3D2A')
    _p(d, 'Versão 0.4, revisada para aplicação', italic=True, size=11, after=6)
    _p(d, Q.STATUS, size=9.5, after=8, color='7A4B00')
    _h(d, '1. Visão geral do instrumento')
    for t in [
        'Formato: questionário online anônimo com %d perguntas (%d afirmações em escala, %d de filtro, perfil e experiência, %d abertas opcionais). Tempo estimado de 12 a 14 minutos, estimativa sem teste, a confirmar no piloto.' % (Q.N_TOTAL, Q.N_SCALE, Q.N_OTHER, len(Q.OPEN)),
        'Escala das afirmações: ' + '; '.join('%d = %s' % (i + 1, s.lower()) for i, s in enumerate(Q.SCALE)) + '.',
        'Ordem: apresentação, filtro e perfil, experiência com IA, intenção de aprender e de usar (variáveis dependentes), fatores organizacionais, utilidade percebida e confiança (controles), propósito, receios e perguntas abertas. As intenções vêm antes dos fatores para reduzir a influência de uma resposta sobre a outra.',
        'Plataforma: usar uma que não registre IP, e-mail nem identificador de dispositivo (por exemplo, o Google Forms sem coleta de e-mail e sem exigir login). Confirmar a configuração antes de divulgar. Embaralhar a ordem dos itens dentro de cada dimensão, mantendo a checagem de atenção no meio do questionário.',
        'Regras de fluxo: F1 = Não e P1 = Outro vínculo encerram o questionário com agradecimento. Nos itens AC1 a AC4, oferecer a opção "Não tenho chefia imediata".']:
        _p(d, t, after=5)
    _h(d, '2. O que mudou em relação à versão 0.3')
    _grid(d, ['Alteração', 'Motivo'], [
        ('Novo item IAP4: querer entender como a IA funciona, seus limites e riscos.', 'A revisão de escopo mostrou que a intenção de aprender quase nunca é medida e se confunde com a de usar. O item separa "entender" de "saber usar".'),
        ('Novo item TE4 (invertido): o volume de trabalho impede de dedicar tempo a aprender.', 'A carga de trabalho percebida aparece como barreira nos estudos. TE1 a TE3 mediam o tempo só em termos positivos.'),
        ('Novo item RC3: receio de ser responsabilizado por erro com apoio de IA.', 'A hipótese H4 prevê receios de responsabilização, de exposição de dados e de substituição, mas só havia itens para os dois últimos.'),
        ('AC2 e AC3 reescritos sem combinar duas ideias.', 'AC2 juntava identificar e remover obstáculos; evita-se pergunta de duplo sentido.'),
        ('SE1 a SE6 mantidos com a redação da escala validada.', 'Qualquer mudança nesses itens quebraria a validação.'),
        ('Checagem de atenção (ATN) movida para o meio do questionário.', 'No fim, ela detecta cansaço, e não desatenção; no meio, filtra respostas automáticas.'),
        ('Definições de IA e de IA generativa na tela inicial e instruções por dimensão.', 'E1 e E2 falam em IA generativa, que precisa estar definida para quem responde.'),
        ('Versão só com as perguntas e ficha de codificação separadas.', 'Quem responde não precisa ver códigos, origem das escalas nem itens invertidos.')], [8.2, 8.2])
    _h(d, '3. Hipóteses e variáveis')
    _grid(d, ['Hipótese', 'Variável explicativa', 'Desfecho'], [
        ('H1', 'Apoio da chefia imediata e dos colegas (AC)', 'Intenção de aprender (IAP) e de usar (IU)'),
        ('H2', 'Tempo para aprender (TE) e acesso a ferramentas e cursos (AF)', 'IAP e IU'),
        ('H3', 'Segurança para experimentar (SE) e clareza das regras (CR)', 'IAP e IU'),
        ('Controles', 'Utilidade percebida (UP) e confiança para usar IA com segurança (CF)', 'IAP e IU, para evitar superestimar os fatores organizacionais'),
        ('H4 (opcional)', 'Receios de substituição, exposição de dados e responsabilização (RC)', 'IAP e IU, associação negativa'),
        ('H5 (secundária)', 'Propósito percebido (PP, CP), além dos fatores organizacionais', 'IAP e IU'),
        ('H6 (exploratória)', 'Tipo de vínculo (P1) como moderador das associações', 'IAP e IU')], [3.0, 8.0, 5.4])
    _h(d, '4. Texto de apresentação (tela inicial)')
    for t in Q.CONSENT: _p(d, t, after=5)
    for t in Q.DEFINITIONS: _p(d, t, after=5)
    _p(d, 'Pendências do texto: informar o contato do pesquisador e o número do parecer do comitê de ética. Conferir com o comitê se este texto basta ou se é necessária a dispensa formal.', italic=True, size=9.5, color='7A4B00')
    _h(d, '5. Questionário completo, com códigos')
    n = 1
    _h(d, 'A. Filtro e perfil', 2)
    for code, text, opts, flow in Q.FILTER + Q.PROFILE:
        _single_q(d, n, code, text, opts, flow, show_code=True); n += 1
    _h(d, 'B. Experiência com inteligência artificial', 2)
    for code, text, opts, flow in Q.EXPERIENCE:
        _single_q(d, n, code, text, opts, flow, show_code=True); n += 1
    letters = 'CDEFGHIJKLMNOP'
    for i, (key, title, instr, items) in enumerate(Q.DIMS):
        _h(d, '%s. %s' % (letters[i], title), 2)
        _p(d, instr, italic=True, size=9.5, after=3)
        if i == 0: _scale_legend(d)
        n = _matrix(d, items, n, show_code=True)
    _h(d, '%s. Perguntas abertas (opcionais)' % letters[len(Q.DIMS)], 2)
    _p(d, "Aviso na tela: '%s' As respostas abertas devem ser revisadas antes da análise, para retirar qualquer informação que identifique alguém." % Q.OPEN_NOTE, italic=True, size=9.5, after=3)
    for k, (c, t) in enumerate(Q.OPEN):
        _p(d, '%s · %d. %s' % (c, n + k, t), bold=True, after=6)
    _h(d, '6. Ficha de codificação e origem dos itens')
    _p(d, 'Recodificar os itens invertidos antes de calcular as médias: novo valor = 6 menos o valor dado (1 vira 5, 2 vira 4, 3 permanece 3, 4 vira 2 e 5 vira 1). SE1 a SE6 formam a escala validada de segurança psicológica; SE7 é analisado à parte.', size=9.5, after=6)
    rows = []
    for key, title, instr, items in Q.DIMS:
        for code, text, inv, org in items:
            rows.append((code, title, 'Sim' if inv else '', Q.ORIG.get(org, 'Item de controle (descartar quem errar)')))
    _grid(d, ['Código', 'Dimensão', 'Invertido', 'Origem'], rows, [1.8, 5.6, 1.8, 7.2], size=8.5)
    _h(d, '7. Plano de análise (resumo)')
    for t in [
        'Calcular a média de cada dimensão (IAP, IU, AC, TE, AF, SE1 a SE6, CR, UP, CF, PP) e a consistência interna (alfa de Cronbach). Analisar SE7 e CP1 à parte.',
        'Descrever a amostra por vínculo e comparar as intenções entre os grupos.',
        'Regressão múltipla para IAP e para IU, com os fatores organizacionais, o propósito e o vínculo (dummies), controlando utilidade percebida, confiança, tempo de serviço, escolaridade, experiência com IA e função de coordenação. Comparar os modelos com e sem UP e CF para ver quanto da associação dos fatores organizacionais se mantém.',
        'Comparar IAP e IU: verificar se os fatores associados a uma diferem dos associados à outra, que é o ponto central da revisão de escopo.',
        'Se a amostra permitir (cerca de 200 ou mais), análise fatorial para checar se as dimensões se separam como esperado. Se os grupos de vínculo tiverem menos de 30 respostas, agrupar (efetivos e não efetivos) ou apenas descrever.',
        'Limitações a registrar: autosseleção (quem responde tende a ter mais interesse em IA), fonte única (teste de viés de método comum), concordância em itens afirmativos e ausência de ferramenta aprovada em parte dos órgãos (E4). Interpretar como associação, sem causalidade, e como amostra de conveniência.']:
        _p(d, '• ' + t, after=4)
    _h(d, '8. Antes de aplicar')
    for t in [
        'Revisar o texto com o comitê de ética da instituição (dispensa ou apreciação) e preencher o contato do pesquisador e o parecer.',
        'Pré-teste cognitivo com 5 a 8 servidores de perfis diferentes, para checar se os itens, em especial AC1 a AC5, TE4, IAP4 e CP1, são entendidos como pretendido.',
        'Piloto com cerca de 30 respostas, para ver a confiabilidade das dimensões e o tempo de resposta.',
        'Revisão por 2 ou 3 especialistas (gestão de pessoas e metodologia).',
        'Confirmar com o órgão se o canal de divulgação for interno, e definir o canal (associações, grupos de servidores, e-mail pessoal ou canal do órgão) e a meta de 200 a 300 respostas válidas.',
        'Conferir a configuração da plataforma: sem coleta de e-mail, IP ou login, com a ordem dos itens embaralhada por dimensão.']:
        _p(d, '• ' + t, after=4)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    d.save(path)


def build():
    os.makedirs('%s/%s/questionario' % (S, SLUG), exist_ok=True)
    open('%s/%s/questionario/index.html' % (S, SLUG), 'w', encoding='utf8').write(page())
    docx_questions('%s/assets/pdf/%s' % (S, DOCX_NAME))
    docx_full('work/questionario/Questionario_v04_para_aplicacao.docx')
    print('questionário: %d perguntas (%d em escala)' % (Q.N_TOTAL, Q.N_SCALE))


if __name__ == '__main__':
    build()
