"""Gera a vitrine de projetos de IA (site separado) a partir de projetos_data.py.
Uso: python build/vitrine.py [pasta_de_saida]   (padrão: ../projetos-ia)"""
import html, os, sys
sys.path.insert(0, 'build')
from projetos_data import CATS, PROJ
from slug import slug

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join('..', 'projetos-ia')
e = html.escape
COLOR = {k: c for k, _, c in CATS}
LABEL = {k: n for k, n, _ in CATS}
ARROW = ('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 7h10v10"/><path d="M7 17 17 7"/></svg>')

def mono(nome):
    w = [x for x in nome.replace('&', ' ').split() if x[0].isalnum() and len(x) > 2] or nome.split()
    return (w[0][0] + (w[1][0] if len(w) > 1 else '')).upper()

def art(n, p):
    img = os.path.join(OUT, 'img', slug(n) + '.jpg')
    if os.path.exists(img):
        return ('<span class="card-art has-img" aria-hidden="true"><img src="img/%s.jpg" alt="" loading="lazy" width="800" height="500">'
                '<span class="plat">%s</span></span>' % (slug(n), e(p)))
    return '<span class="card-art" aria-hidden="true"><span class="mono">%s</span><span class="plat">%s</span></span>' % (e(mono(n)), e(p))

cards = ''.join(
    '<a class="card" data-cat="%s" href="%s" target="_blank" rel="noopener noreferrer" style="--c:%s">'
    '%s<span class="card-body"><span class="cat">%s</span><span class="name">%s</span><span class="desc">%s</span>'
    '<span class="go">Abrir o projeto %s</span></span></a>' % (c, e(u), COLOR[c], art(n, p), e(LABEL[c]), e(n), e(d), ARROW)
    for c, n, p, u, d in PROJ)
chips = '<button type="button" class="chip is-on" data-f="all">Todos <b>%d</b></button>' % len(PROJ) + ''.join(
    '<button type="button" class="chip" data-f="%s">%s <b>%d</b></button>' % (k, e(n), sum(1 for x in PROJ if x[0] == k))
    for k, n, c in CATS)

CSS = """
:root{--bg:#f7f4ea;--fg:#1d3a30;--muted:#5a7066;--border:#ddd9c6;--ochre:#c9923a;--green:#0f3d2a;--display:"Fraunces",Georgia,serif;--shadow:0 1px 2px rgba(20,60,40,.08),0 12px 32px -16px rgba(20,60,40,.25)}
@media (prefers-color-scheme:dark){:root{--bg:#10201a;--fg:#eee9d8;--muted:#a9b8a8;--border:#2c4036;--green:#08261a;--shadow:0 12px 32px -16px rgba(0,0,0,.6)}}
*{box-sizing:border-box;margin:0}
body{background:var(--bg);color:var(--fg);font:16px/1.6 "Inter Tight",system-ui,sans-serif}
.hero{background:var(--green);color:#fff;padding:44px 24px 38px}
.wrap{max-width:68rem;margin:0 auto}
.eyebrow{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--ochre)}
h1{font-family:var(--display);font-weight:600;font-size:clamp(2rem,6vw,3rem);line-height:1.12;margin-top:14px}
h1 span{color:var(--ochre)}
.hero p{margin-top:14px;max-width:42rem;color:rgba(255,255,255,.85);font-weight:500}
.hero .by{margin-top:18px;font-size:.9rem;color:rgba(255,255,255,.7)}
.hero .by a{color:#fff}
main{max-width:68rem;margin:0 auto;padding:26px 24px 56px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:24px}
.chip{display:inline-flex;gap:8px;align-items:center;border:1px solid var(--border);background:transparent;color:var(--fg);border-radius:999px;padding:6px 14px;font:inherit;font-size:13.5px;font-weight:500;cursor:pointer}
.chip b{font-size:12px;color:var(--muted)}
.chip:hover{border-color:var(--ochre)}
.chip.is-on{background:var(--green);border-color:var(--green);color:#fff}
.chip.is-on b{color:rgba(255,255,255,.7)}
.chip:focus-visible,.card:focus-visible{outline:2px solid var(--ochre);outline-offset:2px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(20rem,1fr));gap:20px}
.card{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:color-mix(in srgb,var(--bg) 70%,#fff);border:1px solid var(--border);border-radius:16px;overflow:hidden;transition:transform .2s,box-shadow .2s}
.card[hidden]{display:none}
.card:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
.card-art{position:relative;height:132px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,var(--c),color-mix(in srgb,var(--c) 45%,#000))}
.card-art.has-img{height:auto;aspect-ratio:8/5;background:var(--border);border-bottom:1px solid var(--border)}.card-art img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.mono{font-family:var(--display);font-weight:600;font-size:3.2rem;color:rgba(255,255,255,.92);letter-spacing:.02em}
.plat{position:absolute;top:12px;right:12px;font-size:11.5px;color:#fff;background:rgba(0,0,0,.25);border-radius:999px;padding:2px 10px}
.card-body{display:flex;flex-direction:column;gap:8px;padding:18px 20px 20px;flex:1}
.cat{font-size:11.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--c)}
.name{font-family:var(--display);font-size:1.3rem;line-height:1.25;font-weight:600}
.desc{font-size:14.5px;color:var(--muted);flex:1}
.go{display:inline-flex;gap:6px;align-items:center;margin-top:6px;font-size:14px;font-weight:600}
footer{border-top:1px solid var(--border);padding:22px 24px;text-align:center;font-size:13.5px;color:var(--muted)}
footer a{color:inherit}
"""
SCRIPT = ("<script>(function(){var b=document.querySelectorAll('.chip'),c=document.querySelectorAll('.card');"
          "b.forEach(function(x){x.addEventListener('click',function(){b.forEach(function(y){y.classList.toggle('is-on',y===x)});"
          "c.forEach(function(p){p.hidden=x.dataset.f!=='all'&&p.dataset.cat!==x.dataset.f})})})})();</script>")

page = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Projetos de IA | Carlos Hernane de Oliveira</title>'
        '<meta name="description" content="Vitrine de aplicativos desenvolvidos com inteligência artificial por Carlos Hernane de Oliveira: serviços públicos, gestão, dia a dia e carreira.">'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter+Tight:wght@400;500;600&display=swap">'
        '<style>' + CSS + '</style></head><body>'
        '<header class="hero"><div class="wrap"><p class="eyebrow">Vitrine de projetos</p>'
        '<h1>Aplicativos feitos com <span>inteligência artificial</span></h1>'
        '<p>Ferramentas que desenvolvi para resolver problemas reais, do serviço público ao dia a dia. Escolha um tema e abra o projeto.</p>'
        '<p class="by">Por Carlos Hernane de Oliveira · <a href="https://oliverher.github.io/artigos/">Ver os artigos</a></p></div></header>'
        '<main><div class="chips" role="group" aria-label="Filtrar por tema">' + chips + '</div><div class="grid">' + cards + '</div></main>'
        '<footer>Carlos Hernane de Oliveira · <a href="https://oliverher.github.io/artigos/projetos/">Lista completa de projetos</a></footer>'
        + SCRIPT + '</body></html>')
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8').write(page)
open(os.path.join(OUT, 'README.md'), 'w', encoding='utf8').write('# Projetos de IA\n\nVitrine de aplicativos desenvolvidos com IA, por Carlos Hernane de Oliveira. Gerada por `build/vitrine.py` do repositório `artigos`.\n')
print('ok', OUT, len(PROJ), 'projetos')
