"""Gera docs/projetos/index.html e acrescenta o link 'Projetos' ao menu das páginas dos artigos."""
import html, os, re, shutil, sys
sys.path.insert(0, 'build')
import shell

S = 'docs'
e = html.escape

CATS = [
    ('gov', 'Governo e serviços públicos', '#137d5c'),
    ('gestao', 'Gestão e projetos', '#276fa0'),
    ('dia', 'Dia a dia', '#cf7638'),
    ('carreira', 'Carreira e estudo', '#7a4fa3'),
]
# (categoria, nome, plataforma, url, descrição)
PROJ = [
    ('gov', 'Portal das Jornadas', 'ChatGPT', 'https://portal-jornadas-goias.carlos-hernane-olive.chatgpt.site/',
     'Ponto de partida único para as jornadas de serviços do Governo de Goiás: vida do cidadão, servidor público, investidor, cidadão de Goiânia e atendente omnicanal.'),
    ('gov', 'Cadeia de Valor Integrada', 'ChatGPT', 'https://cadeia-valor-goias.carlos-hernane-olive.chatgpt.site/',
     'Mapa navegável de 23 macrofunções, 13 macroprocessos gerenciais e de suporte e 4.261 processos de trabalho do Estado, com filtros por órgão e por situação de digitalização e exportação para Excel e PDF.'),
    ('gov', 'Regulamentos e Estatutos', 'Lovable', 'https://regulamentos-orgaos-go.lovable.app/',
     'Painel de consulta dos regulamentos e estatutos dos órgãos do Estado de Goiás, com busca, filtro por tipo de documento e exportação da lista em PDF.'),
    ('gov', 'Assistente da Carta de Serviços', 'ChatGPT', 'https://carta-servicos-sead-gecart.carlos-hernane-olive.chatgpt.site/',
     'Apoio para reescrever serviços públicos em linguagem mais clara: lê documentos ou links, extrai as informações, devolve perguntas sobre o que falta e deixa a decisão final com o órgão responsável.'),
    ('gov', 'Relatório Executivo CLP 2026', 'ChatGPT', 'https://goias-ranking-insight-2026.carlos-hernane-olive.chatgpt.site/#capital',
     'Leitura executiva do Ranking de Competitividade dos Estados (CLP): Goiás comparado aos demais estados em dez pilares e 100 indicadores, com série histórica e projeções para 2026.'),
    ('gov', 'Pesquisar Nome no Diário Oficial do Estado', 'ChatGPT', 'https://consultar-nome-doe-goias.carlos-hernane-olive.chatgpt.site/',
     'Busca nomes nas edições do Diário Oficial de Goiás em períodos de até 12 meses e abre a edição original. As consultas ficam apenas no dispositivo.'),
    ('gov', 'Pesquisar Nome no Diário Oficial de Aparecida', 'ChatGPT', 'https://convoca-aparecida.carlos-hernane-olive.chatgpt.site/',
     'A mesma ideia para o Diário Oficial de Aparecida de Goiânia: pesquisa edições e suplementos de um período e abre os PDFs oficiais.'),
    ('gestao', 'Validador de Projetos', 'Lovable', 'https://entrega-de-valor-projetos.lovable.app/',
     'Painel para avaliar fatores críticos de sucesso e benefícios da gestão por projetos em instituições de ensino, alinhado ao PMBOK 7ª e 8ª edições, com quadro de conexões, simulador de cenários e assistente de decisão.'),
    ('dia', 'Controle de Despesas', 'ChatGPT', 'https://controle-de-despesas.carlos-hernane-olive.chatgpt.site/',
     'Controle financeiro pessoal: receitas, despesas, saldo do mês, gastos por categoria e taxa de economia. Funciona no navegador e guarda os dados só no aparelho.'),
    ('dia', 'Tela e Cuidado', 'Lovable', 'https://html-hugger-65.lovable.app/tela-e-cuidado.html',
     'Guia sobre o uso realista de telas por crianças, pensado para quem cuida sozinho: orientações por faixa etária, atividades sem custo, plano de quatro semanas e rede pública de apoio.'),
    ('dia', 'Studio Ket', 'ChatGPT', 'https://studio-ketellen-agenda.carlos-hernane-olive.chatgpt.site/',
     'Agendamento online de um estúdio de unhas: a cliente escolhe o serviço e o horário e confirma os dados em três passos, sem precisar ligar.'),
    ('carreira', 'Currículo', 'Lovable', 'https://curriculo-carlos-hernane-oliveira.lovable.app/',
     'Currículo online com experiência em governança, gestão de TI, projetos e processos no setor público, formação, certificações, publicações e projetos.'),
    ('carreira', 'Aulas ESPGTI & DSS-BI', 'Claude', 'https://claude.ai/artifact/HqLzXH5JDMQ2BehUu8BeQQ',
     'Biblioteca das aulas gravadas das especializações do Instituto de Informática da UFG, organizada por temporada e disciplina, com busca e marcação das aulas já assistidas.'),
]
COLOR = {k: c for k, _, c in CATS}
LABEL = {k: n for k, n, _ in CATS}
ARROW = ('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 7h10v10"/><path d="M7 17 17 7"/></svg>')

cards = ''.join(
    '<a class="proj" data-cat="%s" href="%s" target="_blank" rel="noopener noreferrer" style="--c:%s">'
    '<span class="proj-top"><span class="proj-cat">%s</span><span class="proj-plat">%s</span></span>'
    '<span class="proj-name">%s</span><span class="proj-desc">%s</span>'
    '<span class="proj-go">Abrir o projeto %s</span></a>' % (c, e(u), COLOR[c], e(LABEL[c]), p, e(n), e(d), ARROW)
    for c, n, p, u, d in PROJ)
chips = '<button type="button" class="chip is-on" data-f="all">Todos <b>%d</b></button>' % len(PROJ) + ''.join(
    '<button type="button" class="chip" data-f="%s">%s <b>%d</b></button>' % (k, e(n), sum(1 for x in PROJ if x[0] == k))
    for k, n, c in CATS)

SCRIPT = ("<script>(function(){var b=document.querySelectorAll('.chip'),c=document.querySelectorAll('.proj');"
          "b.forEach(function(x){x.addEventListener('click',function(){b.forEach(function(y){y.classList.toggle('is-on',y===x)});"
          "c.forEach(function(p){p.hidden=x.dataset.f!=='all'&&p.dataset.cat!==x.dataset.f})})})})();</script>")

page = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Projetos | Carlos Hernane de Oliveira</title>'
        '<meta name="description" content="Aplicativos e ferramentas desenvolvidos por Carlos Hernane de Oliveira: serviços públicos, gestão de processos e projetos, e utilidades do dia a dia.">'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter+Tight:wght@400;500;600&display=swap">'
        '<link rel="stylesheet" href="../assets/styles.css"><link rel="stylesheet" href="../assets/home.css"></head><body>'
        + shell.sidebar('projetos', '../') + '<div class="home-main">' + shell.nav('projetos', '../') +
        '<header class="home-hero"><div class="home-wrap proj-wrap"><p class="home-eyebrow">Aplicativos e ferramentas</p>'
        '<h1>O que venho <span>construindo</span></h1>'
        '<p>Projetos que desenvolvi, de serviços públicos a utilidades do dia a dia. Cada um abre em uma nova aba.</p></div></header>'
        '<main class="proj-main"><div class="chips" role="group" aria-label="Filtrar por tema">' + chips + '</div>'
        '<div class="proj-grid">' + cards + '</div></main></div>' + SCRIPT + '</body></html>')
os.makedirs(S + '/projetos', exist_ok=True)
open(S + '/projetos/index.html', 'w', encoding='utf8').write(page)
shutil.copy('build/home.css', S + '/assets/home.css')

# link "Projetos" no menu das páginas dos artigos (idempotente)
for slug, _, _, _ in shell.ARTS:
    f = '%s/%s/index.html' % (S, slug)
    h = open(f, encoding='utf8').read()
    if 'href="../projetos/"' in h:
        continue
    m = re.search(r'<a href="\.\./pmbok-dialetica/"[^>]*>Evolução do PMBOK</a>', h)
    cls = re.search(r'<a href="\.\./pmbok-dialetica/" class="([^"]*)"', h)
    if cls:  # páginas com menu em pílulas
        new = '<a href="../projetos/" class="%s">Projetos</a>' % cls.group(1).replace('bg-primary text-primary-foreground', 'text-muted-foreground hover:bg-secondary')
    else:  # artigo 05, menu simples
        new = '\n<a href="../projetos/">Projetos</a>'
    h = h.replace(m.group(0), m.group(0) + new, 1)
    open(f, 'w', encoding='utf8').write(h)
