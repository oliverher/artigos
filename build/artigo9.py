"""Artigo 09: Ciência comportamental dentro do órgão: pressupostos que falham e um framework para substituí-los.

Gera docs/ciencia-comportamental-orgao/index.html a partir do texto estruturado do artigo (build/artigo9_texto.py)
e dos 7 slides da apresentação (src/orig/ciencia-comportamental-orgao/img). As imagens usam a galeria animada de
build/mmdi.css e build/mmdi.js, como nos artigos 06 a 08.
"""
import os, shutil, sys
sys.path.insert(0, 'build')
import shell
from artigo4 import acc, e, BOOK
from artigo9_texto import SECOES, REFS

S = 'docs'
SLUG = 'ciencia-comportamental-orgao'
SRC = 'src/orig/ciencia-comportamental-orgao'
PDF = 'Ciencia_comportamental_dentro_do_orgao.pdf'
SEQ = {}


def gfig(n, title, alt):
    """Imagem animada: slide n da apresentação, na galeria de build/mmdi.css."""
    SEQ[n] = len(SEQ) + 1
    img = 'cc-slide-%02d.jpg' % n
    return ('<figure class="gfig mt-6 overflow-hidden rounded-xl border bg-card shadow-[var(--shadow-soft)]" data-tour=\'[]\'>'
            '<div class="gfig-stage"><div class="gfig-zoom">'
            '<img class="gfig-img" src="../assets/img/%s" width="1376" height="774" loading="lazy" alt="%s"/>'
            '<div class="gfig-fx" aria-hidden="true"><i class="gfig-sweep"></i><i class="gfig-scan"></i><i class="gfig-glare"></i><i class="gfig-wipe"></i></div>'
            '</div></div>'
            '<figcaption class="border-t px-5 py-4 text-sm leading-relaxed text-muted-foreground">%s'
            '<span class="mt-1 block text-xs text-muted-foreground/80">Imagem %d da apresentação do artigo. '
            '<a class="underline underline-offset-2" href="../assets/img/%s" target="_blank" rel="noopener">Ver a imagem original</a></span></figcaption></figure>'
            % (img, e(alt), e(title, quote=False), SEQ[n], img))


def section(num, sid, title, sub, blocks, accs):
    return ('<section id="%s" aria-labelledby="%s-titulo"><div class="flex items-baseline gap-4">'
            '<span class="font-display text-3xl text-ochre">%s</span><div><h2 id="%s-titulo" class="text-2xl font-semibold">%s</h2>'
            '<p class="mt-1 text-sm text-muted-foreground">%s</p></div></div>%s<div class="mt-6 space-y-3">%s</div></section>'
            % (sid, sid, num, sid, e(title, quote=False), e(sub, quote=False), ''.join(blocks), ''.join(accs)))


def table(caption, head, rows, source):
    th = 'style="padding:8px 10px;text-align:left;border-bottom:2px solid var(--border);font-weight:600"'
    td = 'style="padding:8px 10px;border-bottom:1px solid var(--border);vertical-align:top"'
    hh = ''.join('<th %s>%s</th>' % (th, e(h)) for h in head)
    bb = ''.join('<tr>' + ''.join('<td %s>%s</td>' % (td, e(c)) for c in r) + '</tr>' for r in rows)
    return ('<figure class="mt-6 rounded-xl border bg-card p-5 shadow-[var(--shadow-soft)]"><p class="text-sm font-medium text-foreground">%s</p>'
            '<div style="overflow-x:auto;margin-top:12px"><table style="width:100%%;border-collapse:collapse;font-size:13.5px;line-height:1.45;min-width:560px">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            '<p class="mt-3 text-xs text-muted-foreground">%s</p></figure>' % (e(caption), hh, bb, e(source)))


# ---------- figuras (slides) ----------
F1 = gfig(1, 'Ciência comportamental dentro do órgão público: pressupostos que falham e um framework de cinco camadas para substituí-los.',
          'Slide de abertura: título Ciência Comportamental dentro do Órgão Público, o subtítulo sobre pressupostos que falham e um framework de 5 camadas, e uma ilustração de servidores em torno de três etapas: análise comportamental, desenho de políticas públicas e implementação e avaliação.')
F2 = gfig(2, 'Servidores públicos demandam alvos relacionais e normas éticas distintas das aplicadas a cidadãos.',
          'Slide com quatro tópicos (mudança de paradigma, administração pública comportamental, relações de emprego e hierarquia, desfecho relacional) ao lado do Quadro 1, que compara três alvos: cidadão, organização decisora e servidor no órgão.')
F3 = gfig(3, 'Quatro pressupostos implícitos falham ao ignorar a hierarquia e o desenho por equipe.',
          'Slide com quatro cartões coloridos: P2 unidade individual, P4 alvos independentes, P5 ausência de autoridade e P7 chefia sem papel, cada um com o que o framework tradicional presume e por que isso falha.')
F4 = gfig(4, 'O framework de cinco camadas integra o diagnóstico relacional e a ética às etapas gerais de intervenção.',
          'Slide com o diagrama do framework: as etapas gerais (alvo, exploração, desenho, teste e ampliação) com as camadas 1, 2, 3 e 5 acopladas a elas e a camada 4, de ética da relação de emprego, como portão transversal.')
F5 = gfig(5, 'Diagnóstico relacional e canal de chefia priorizam a mudança de contexto antes de mensagens.',
          'Slide com o detalhamento das camadas 1 e 2: diagnóstico relacional (mapa de interdependência, auditoria de sludge interno) e canal e desenho (prioridade ao contexto, feedback concreto da chefia, equipe como unidade).')
F6 = gfig(6, 'Ensaios por equipe exigem análise por cluster e salvaguardas contra o uso coercitivo de dados.',
          'Slide com o detalhamento das camadas 3 e 4: teste por equipe (unidade de alocação, análise por cluster e correlação intraclasse, efeitos realistas) e ética da relação de emprego (voluntariedade sob hierarquia, anonimato e vedação de uso disciplinar).')
F7 = gfig(7, 'Três proposições refutáveis orientam a validação empírica e a agenda de pesquisa.',
          'Slide com as três proposições refutáveis (unidade de alocação, canal de chefia, voluntariedade e poder) e a agenda de pesquisa em seis etapas, da revisão sistemática ao estudo de persistência.')

# ---------- seções ----------
META = {
    '1': ('introducao', 'Os frameworks de uso corrente nasceram do cidadão; o servidor dentro do órgão é um alvo diferente.', []),
    '2': ('referencial', 'Três alvos da intervenção, a administração pública comportamental, os frameworks em uso e a ética.', [F2]),
    '3': ('metodo', 'Artigo conceitual: auditoria de pressupostos, busca de anterioridade e derivação do framework.', []),
    '4': ('pressupostos', 'Sete pressupostos implícitos, dos quais quatro aparecem pouco tratados nos documentos lidos.', [F3]),
    '5': ('framework', 'Cinco camadas acopladas às etapas já conhecidas, com a ética como portão em cada uma.', [F4, F5, F6]),
    '6': ('proposicoes', 'Três proposições refutáveis, com o desenho de teste de cada uma.', []),
    '7': ('discussao', 'Posicionamento em relação às obras próximas, objeções previsíveis e limites.', []),
    '8': ('agenda', 'Seis frentes de pesquisa, em ordem de dependência, e as considerações finais.', []),
}
INTRO_ACC = [
    ('Do cidadão ao servidor', 0, 2),
    ('Pressupostos que falham, e por quê', 2, 4),
    ('Trabalhos próximos e a lacuna', 4, 6),
    ('Objetivo e organização do texto', 6, 7),
]


def paras_do_sub(itens):
    """Parágrafos de um bloco; listas de alíneas viram parágrafos a), b), c)."""
    out, tabelas = [], []
    for tipo, v in itens:
        if tipo == 'P':
            out.append(v)
        elif tipo == 'B':
            for i, t in enumerate(v):
                out.append('%s) %s' % (chr(97 + i), t))
        elif tipo == 'T':
            tabelas.append(table(v['cap'], v['rows'][0], v['rows'][1:], v['fonte'] or 'Fonte: elaboração própria.'))
    return out, tabelas


sections = []
for sec in SECOES:
    sid, sub, blocks = META[sec['num']]
    accs, tabs = [], []
    for s in sec['subs']:
        if not s['itens']:
            continue
        paras, tb = paras_do_sub(s['itens'])
        tabs += tb
        if s['titulo'] is None and sec['num'] == '1':
            for t, a, b in INTRO_ACC:
                accs.append(acc(t, paras[a:b]))
        else:
            accs.append(acc(s['titulo'], paras))
    if sec['num'] == '8':
        accs.append(acc('Referências (%d)' % len(REFS), REFS))
    sections.append(section('%02d' % int(sec['num']), sid, sec['titulo'], sub, blocks + tabs, accs))

closing = ('<section aria-labelledby="sintese" class="mt-16 rounded-2xl border bg-secondary/50 p-7"><h2 id="sintese" class="text-2xl font-semibold">A síntese</h2>'
           '<p class="mt-3 leading-relaxed text-muted-foreground">Os frameworks de ciência comportamental de uso corrente foram desenvolvidos, em grande parte, com o cidadão em mente, e suas etapas gerais continuam úteis para o servidor dentro do órgão. Quando o comportamento de interesse é relacional, porém, alguns pressupostos deixam de valer: a unidade individual, a independência entre os alvos, a ausência de autoridade de quem intervém e o papel nulo da chefia. O artigo apresenta esses pressupostos com o nível de evidência de cada um, propõe um framework de cinco camadas que os trata de forma explícita e deriva três proposições refutáveis.</p>'
           + F7 +
           '<p class="mt-6 rounded-lg border-l-2 border-ochre bg-accent/50 px-4 py-3 text-[15px] italic leading-relaxed text-accent-foreground">Em busca não sistemática, não encontramos um framework que reúna o servidor como alvo, um desfecho relacional, o desenho por equipe e a ética da relação de emprego. Essa é uma afirmação sobre o que não encontramos, e a agenda começa por confirmá-la ou refutá-la com uma revisão sistemática.</p></section>')


def build():
    stat = lambda n, l: ('<div><dt class="font-display text-2xl text-ochre">%s</dt>'
                         '<dd class="mt-1 text-xs uppercase tracking-wide text-primary-foreground/70">%s</dd></div>' % (n, l))
    header = ('<header class="relative overflow-hidden text-primary-foreground" style="background-image:var(--gradient-deep)">'
              '<div class="surface-paper absolute inset-0 opacity-30" aria-hidden="true"></div>'
              '<div class="relative mx-auto max-w-3xl px-6 py-20 sm:py-28">'
              '<p class="text-xs font-semibold uppercase tracking-[0.2em] text-ochre">Ciência comportamental · Administração pública · Servidores públicos</p>'
              '<h1 class="mt-6 text-4xl leading-[1.1] font-semibold sm:text-5xl">Ciência comportamental <span class="text-gradient-warm">dentro do órgão</span></h1>'
              '<p class="mt-5 text-lg leading-relaxed text-primary-foreground/80">Pressupostos que falham e um framework para substituí-los.</p>'
              '<p class="mt-4 text-base leading-relaxed text-primary-foreground/70">Cinco camadas para desenhar, testar e cuidar da ética quando o alvo é o servidor.</p>'
              '<p class="mt-8 text-sm text-primary-foreground/70">Carlos Hernane de Oliveira</p>'
              '<div class="mt-6" style="display:flex;flex-wrap:wrap;gap:12px"><a href="../assets/pdf/%s" target="_blank" rel="noopener noreferrer" '
              'class="inline-flex items-center gap-2 rounded-full bg-ochre px-6 py-3 text-sm font-semibold text-ochre-foreground shadow-lift">'
              % PDF + BOOK + 'Leia o Artigo na Íntegra</a></div>'
              '<p class="mt-3 max-w-md text-sm leading-relaxed text-primary-foreground/70">Abre o PDF completo do artigo em uma nova aba, para leitura direta no navegador.</p>'
              '<dl class="mt-10 grid grid-cols-2 gap-6 sm:grid-cols-4">'
              + stat('7', 'pressupostos') + stat('4', 'pouco tratados') + stat('5', 'camadas') + stat('3', 'proposições refutáveis')
              + '</dl></div></header>')
    intro = ('<section aria-labelledby="resumo-cc"><h2 id="resumo-cc" class="text-2xl font-semibold">Do que trata o artigo</h2>'
             '<p class="mt-4 leading-relaxed text-muted-foreground">Os frameworks de ciência comportamental de uso corrente no setor público foram desenvolvidos, em grande parte, com o cidadão em mente. O artigo examina o que muda quando o alvo é o servidor dentro do órgão e o comportamento de interesse é relacional, como colaborar ou engajar-se.</p>'
             '<p class="mt-4 leading-relaxed text-muted-foreground">Por meio de uma auditoria de pressupostos de seis documentos (TESTS, BASIC, CINCO, EAST, COM-B e BEAR) e de uma busca de anterioridade, identificam-se sete pressupostos implícitos, dos quais quatro aparecem pouco tratados: a unidade individual de alocação, a independência entre os alvos, a ausência de autoridade de quem intervém e a ausência de papel da chefia imediata. O texto propõe um framework de cinco camadas, acoplado às etapas gerais de intervenção, com a ética da relação de emprego como portão em cada etapa, e deriva três proposições refutáveis.</p>'
             '<p class="mt-4 rounded-lg border-l-2 border-ochre bg-accent/50 px-4 py-3 text-[15px] leading-relaxed text-accent-foreground">Artigo teórico: o framework não foi testado, a busca de anterioridade não foi sistemática e a aplicação fica para um segundo artigo. A afirmação de que não se encontrou um framework equivalente depende de revisão sistemática.</p>'
             + F1 + '</section>'
             '<section aria-labelledby="objetivos-cc" class="mt-10 rounded-2xl border bg-secondary/50 p-7"><h2 id="objetivos-cc" class="text-2xl font-semibold">Pergunta e objetivo</h2>'
             '<div class="mt-6"><h3 class="text-lg font-semibold text-ochre">Pergunta de pesquisa</h3><p class="mt-2 leading-relaxed text-muted-foreground">Que pressupostos dos frameworks vigentes deixam de valer quando o alvo é o servidor dentro do órgão e o comportamento é relacional, e que elementos um framework precisa ter para tratá-los?</p></div>'
             '<div class="mt-6"><h3 class="text-lg font-semibold text-ochre">Objetivo</h3><p class="mt-2 leading-relaxed text-muted-foreground">Identificar quais pressupostos deixam de valer nesse contexto, com o nível de evidência de cada um, e propor um framework de cinco camadas, acoplado às etapas gerais já conhecidas, do qual derivam três proposições refutáveis.</p></div></section>')
    main = '<main class="mx-auto max-w-3xl px-6 py-16">' + intro + '<div class="mt-14 space-y-14">' + ''.join(sections) + '</div>' + closing + '</main>'
    footer = ('<footer class="border-t bg-card"><div class="mx-auto max-w-3xl px-6 py-10 text-sm text-muted-foreground">'
              '<p class="font-display text-base text-foreground">Ciência comportamental dentro do órgão: pressupostos que falham e um framework para substituí-los</p>'
              '<p class="mt-2">Carlos Hernane de Oliveira.</p>'
              '<p class="mt-2">Aspectos éticos: o estudo usa apenas literatura publicada e documentos públicos, sem coleta de dados com pessoas.</p>'
              '<p class="mt-4">Palavras-chave: ciência comportamental; administração pública comportamental; servidores públicos; nudge; framework; ética.</p></div></footer>')
    page = ('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>'
            '<title>Ciência comportamental dentro do órgão: pressupostos que falham e um framework</title>'
            '<meta name="description" content="Artigo teórico que examina quais pressupostos dos frameworks de ciência comportamental deixam de valer quando o alvo é o servidor dentro do órgão e propõe um framework de cinco camadas, com a ética da relação de emprego como portão, e três proposições refutáveis.">'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter+Tight:wght@400;500;600&display=swap"/>'
            '<link rel="stylesheet" href="../assets/styles.css"/><link rel="stylesheet" href="../assets/mmdi.css"/>'
            '<script>document.documentElement.classList.add("js")</script></head><body>'
            + shell.nav(SLUG, '../') + '<div class="min-h-screen">' + header + main + footer + '</div>'
            '<script src="../assets/app.js"></script><script src="../assets/mmdi.js"></script></body></html>')
    os.makedirs('%s/%s' % (S, SLUG), exist_ok=True)
    open('%s/%s/index.html' % (S, SLUG), 'w', encoding='utf8').write(page)
    for f in os.listdir(SRC + '/img'):
        shutil.copy(SRC + '/img/' + f, S + '/assets/img/' + f)
    shutil.copy(SRC + '/' + PDF, S + '/assets/pdf/' + PDF)
    shutil.copy('build/mmdi.css', S + '/assets/mmdi.css')
    shutil.copy('build/mmdi.js', S + '/assets/mmdi.js')


if __name__ == '__main__':
    build()
