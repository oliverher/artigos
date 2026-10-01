import shutil
S = 'docs'
shutil.copy('build/app.js', S + '/assets/app.js')
shutil.copy('build/home.css', S + '/assets/home.css')


def icon(paths):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>') % paths


ICONS = {
    'compass': icon('<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>'),
    'heart': icon('<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M3.22 12H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/>'),
    'factory': icon('<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/>'),
    'layers': icon('<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>'),
    'users': icon('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'),
}

arts = [
    ('proposito-de-vida', 'ARTIGO 01', 'Propósito de vida ao longo do desenvolvimento humano', '#137d5c', 'compass',
     [('91', 'publicações'), ('488.765', 'pessoas'), ('HR 0,76', 'mortalidade')]),
    ('mente-e-corpo', 'ARTIGO 02', 'Limites da recuperação física na relação mente e corpo', '#cf7638', 'heart',
     [('100', 'textos abertos'), ('20', 'trabalhos'), ('5', 'níveis de afirmação')]),
    ('bpm-em-pmes', 'ARTIGO 03', 'Framework de gestão de processos para PMEs em Goiás', '#276fa0', 'factory',
     [('265', 'intervenções'), ('37', 'empresas'), ('83%', 'micro e pequenas')]),
    ('passaporte-pessoa-idosa', 'ARTIGO 04', 'Transformação digital e design de serviços no setor público: o Passaporte da Pessoa Idosa em Goiás', '#7a4fa3', 'users',
     [('126', 'pessoas idosas'), ('60 → 5', 'dias de emissão'), ('3', 'canais de acesso')]),
    ('pmbok-dialetica', 'ARTIGO 05', 'A evolução dialética do gerenciamento de projetos: PMBOK® 6ª, 7ª e 8ª edições', '#a8483a', 'layers',
     [('3', 'edições comparadas'), ('4', 'proposições avaliadas'), ('3', 'leituras concorrentes')]),
]
cards = ''
for slug, tag, title, color, ic, stats in arts:
    st = ''.join('<span><b>%s</b> %s</span>' % s for s in stats)
    cards += ('<a class="art" href="%s/"><span class="art-tile" style="background:%s">%s</span>'
              '<span class="art-body"><span class="art-tag">%s</span><span class="art-title">%s</span>'
              '<span class="art-stats">%s</span></span>'
              '<span class="art-go" aria-hidden="true">→</span></a>') % (slug, color, ICONS[ic], tag, title, st)

pill = 'shrink-0 rounded-full px-4 py-1.5 text-sm font-medium text-muted-foreground transition-colors hover:bg-secondary'
nav = ('<nav class="sticky top-0 z-50 border-b border-border/60 bg-background/90 backdrop-blur">'
       '<div class="mx-auto flex max-w-3xl items-center gap-2 overflow-x-auto px-6 py-3">'
       '<a href="./" class="shrink-0 rounded-full px-4 py-1.5 text-sm font-medium bg-primary text-primary-foreground" aria-current="page">Início</a>'
       '<a href="proposito-de-vida/" class="%s">Propósito de vida</a>'
       '<a href="mente-e-corpo/" class="%s">Mente e corpo</a>'
       '<a href="bpm-em-pmes/" class="%s">BPM em PMEs</a>'
       '<a href="passaporte-pessoa-idosa/" class="%s">Transformação de Serviço</a>'
       '<a href="pmbok-dialetica/" class="%s">Evolução do PMBOK</a></div></nav>') % (pill, pill, pill, pill, pill)
home = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Artigos de Carlos Hernane de Oliveira</title>'
        '<meta name="description" content="Coleção de artigos de Carlos Hernane de Oliveira: propósito de vida, relações mente-corpo, gestão de processos em PMEs e design de serviços públicos.">'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter+Tight:wght@400;500;600&display=swap">'
        '<link rel="stylesheet" href="assets/styles.css"><link rel="stylesheet" href="assets/home.css"></head><body>'
        + nav +
        '<header class="home-hero"><div class="home-wrap"><p class="home-eyebrow">Coleção de artigos · Goiânia, 2026</p>'
        '<h1>Cinco ensaios, uma <span>leitura por vez</span></h1><p>Escolha o artigo do seu interesse.</p></div></header>'
        '<main class="home-list"><h2>Escolha um artigo</h2>' + cards + '</main></body></html>')
open(S + '/index.html', 'w', encoding='utf8').write(home)
