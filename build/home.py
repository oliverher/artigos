import shutil, sys
sys.path.insert(0, 'build')
import shell
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
    'gauge': icon('<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>'),
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
    ('mmdi-go', 'ARTIGO 06', 'Framework de maturidade para a transformação digital e de serviços no setor público goiano', '#1f8a8a', 'gauge',
     [('6', 'dimensões'), ('5', 'níveis'), ('18', 'itens diagnósticos')]),
]
import projetos_data
GRID = icon('<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>')
cards = ''
for slug, tag, title, color, ic, stats in arts:
    st = ''.join('<span><b>%s</b> %s</span>' % s for s in stats)
    cards += ('<a class="gcard" href="%s/"><span class="gcard-tile" style="background:%s">%s</span>'
              '<span class="gcard-body"><span class="art-tag">%s</span><span class="gcard-title">%s</span>'
              '<span class="art-stats">%s</span></span></a>') % (slug, color, ICONS[ic], tag, title, st)
n_proj, n_cat = len(projetos_data.PROJ), len(projetos_data.CATS)
cards += ('<a class="gcard gcard-proj" href="projetos/"><span class="gcard-tile" style="background:#0f3d2a">%s</span>'
          '<span class="gcard-body"><span class="art-tag">PROJETOS</span><span class="gcard-title">Aplicativos desenvolvidos com IA</span>'
          '<span class="art-stats"><span><b>%d</b> projetos</span><span><b>%d</b> temas</span></span></span></a>') % (GRID, n_proj, n_cat)

home = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Artigos de Carlos Hernane de Oliveira</title>'
        '<meta name="description" content="Coleção de artigos de Carlos Hernane de Oliveira: propósito de vida, relações mente-corpo, gestão de processos em PMEs e design de serviços públicos.">'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter+Tight:wght@400;500;600&display=swap">'
        '<link rel="stylesheet" href="assets/styles.css"><link rel="stylesheet" href="assets/home.css"></head><body>'
        + shell.sidebar('home', '') + '<div class="home-main">' + shell.nav('home', '') +
        '<header class="home-hero"><div class="home-wrap proj-wrap"><p class="home-eyebrow">Coleção de artigos · Goiânia, 2026</p>'
        '<h1>Seis ensaios, uma <span>leitura por vez</span></h1><p>Escolha o artigo do seu interesse.</p></div></header>'
        '<main class="home-list"><h2>Artigos e projetos</h2><div class="gallery">' + cards + '</div></main></div></body></html>')
open(S + '/index.html', 'w', encoding='utf8').write(home)
