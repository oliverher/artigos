import shutil
S = 'docs'
shutil.copy('build/app.js', S + '/assets/app.js')
shutil.copy('build/home.css', S + '/assets/home.css')
arts = [
    ('proposito-de-vida', 'ARTIGO 01', 'Propósito de vida ao longo do desenvolvimento humano',
     'Uma revisão crítica sobre direção pessoal, saúde, trabalho e condições sociais — e por que propósito não deveria virar obrigação moral de realização.',
     'figura-12.jpg', 'Construção em três níveis: experiência individual, reconhecimento relacional e estrutura social.',
     [('91', 'publicações'), ('488.765', 'pessoas'), ('HR 0,76', 'mortalidade')]),
    ('mente-e-corpo', 'ARTIGO 02', 'Limites da recuperação física na relação mente e corpo',
     'Estresse, adaptação e adoecimento sob uma matriz crítica: o que as evidências permitem afirmar — e o que ainda não permitem — sobre recuperar a saúde física.',
     'mente-corpo-figura-3.jpg', 'Carga alostática ao longo do tempo, apoiada em determinantes sociais.',
     [('100', 'textos em acesso aberto'), ('20', 'trabalhos discutidos'), ('5', 'níveis de afirmação')]),
    ('bpm-em-pmes', 'ARTIGO 03', 'Framework de gestão de processos para PMEs em Goiás',
     'Da lógica funcional à visão por processos: o ciclo de implementação, os resultados em empresas goianas e o desafio de sustentar a transformação.',
     'bpm-pmes-figura-13.jpg', 'Matriz que cruza assimilação metodológica com engajamento humano e liderança.',
     [('265', 'intervenções'), ('37', 'empresas'), ('83%', 'micro e pequenas')]),
]
cards = ''
for slug, tag, title, desc, img, alt, stats in arts:
    st = ''.join('<span><b>%s</b> %s</span>' % s for s in stats)
    cards += ('<a class="art" href="%s/"><img src="assets/img/%s" alt="%s" loading="lazy">'
              '<div class="art-body"><span class="art-tag">%s</span><span class="art-title">%s</span>'
              '<span class="art-desc">%s</span><div class="art-stats">%s</div></div>'
              '<span class="art-go" aria-hidden="true">→</span></a>') % (slug, img, alt, tag, title, desc, st)
pill = 'shrink-0 rounded-full px-4 py-1.5 text-sm font-medium text-muted-foreground transition-colors hover:bg-secondary'
nav = ('<nav class="sticky top-0 z-50 border-b border-border/60 bg-background/90 backdrop-blur">'
       '<div class="mx-auto flex max-w-3xl items-center gap-2 overflow-x-auto px-6 py-3">'
       '<a href="./" class="shrink-0 rounded-full px-4 py-1.5 text-sm font-medium bg-primary text-primary-foreground" aria-current="page">Início</a>'
       '<a href="proposito-de-vida/" class="%s">Propósito de vida</a>'
       '<a href="mente-e-corpo/" class="%s">Mente e corpo</a>'
       '<a href="bpm-em-pmes/" class="%s">BPM em PMEs</a></div></nav>') % (pill, pill, pill)
home = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Artigos de Carlos Hernane de Oliveira</title>'
        '<meta name="description" content="Coleção de artigos de Carlos Hernane de Oliveira: propósito de vida, relações mente-corpo e gestão de processos em PMEs.">'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter+Tight:wght@400;500;600&display=swap">'
        '<link rel="stylesheet" href="assets/styles.css"><link rel="stylesheet" href="assets/home.css"></head><body>'
        + nav +
        '<header class="home-hero"><div class="home-wrap"><p class="home-eyebrow">Coleção de artigos · Goiânia, 2026</p>'
        '<h1>Três ensaios, uma <span>leitura por vez</span></h1><p>Escolha o artigo do seu interesse.</p>'
        '<p class="home-author">Carlos Hernane de Oliveira</p></div></header>'
        '<main class="home-list"><h2>Escolha um artigo</h2>' + cards + '</main>'
        '<footer class="home-foot"><div class="home-wrap">Carlos Hernane de Oliveira · Goiânia, 2026.</div></footer></body></html>')
open(S + '/index.html', 'w', encoding='utf8').write(home)
