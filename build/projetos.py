"""Gera docs/projetos/index.html e acrescenta o link 'Projetos' ao menu das páginas dos artigos."""
import html, os, re, shutil, sys
sys.path.insert(0, 'build')
import shell

S = 'docs'
e = html.escape

from projetos_data import CATS, PROJ
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

shell.patch_menus(S)
