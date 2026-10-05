"""Barra lateral e menu de pílulas compartilhados pela página inicial e pela página de projetos."""

ARTS = [
    ('proposito-de-vida', 'Artigo 01', 'Propósito de vida', '#137d5c'),
    ('mente-e-corpo', 'Artigo 02', 'Mente e corpo', '#cf7638'),
    ('bpm-em-pmes', 'Artigo 03', 'BPM em PMEs', '#276fa0'),
    ('passaporte-pessoa-idosa', 'Artigo 04', 'Transformação de Serviço', '#7a4fa3'),
    ('pmbok-dialetica', 'Artigo 05', 'Evolução do PMBOK', '#a8483a'),
    ('mmdi-go', 'Artigo 06', 'MMDI-GO', '#1f8a8a'),
]
PILL = 'shrink-0 rounded-full px-4 py-1.5 text-sm font-medium transition-colors '
OFF = PILL + 'text-muted-foreground hover:bg-secondary'
ON = PILL + 'bg-primary text-primary-foreground'


def sidebar(active, base):
    def link(href, label, key, dot=None, small=None):
        cls = 'side-link' + (' is-active' if key == active else '')
        cur = ' aria-current="page"' if key == active else ''
        d = '<span class="side-dot" style="background:%s"></span>' % dot if dot else '<span class="side-dot side-home"></span>'
        s = '<small>%s</small>' % small if small else ''
        return '<a href="%s" class="%s"%s>%s<span>%s%s</span></a>' % (href, cls, cur, d, s, label)
    items = (link(base or './', 'Início', 'home') + link(base + 'projetos/', 'Projetos - Aplicativos desenvolvidos com IA', 'projetos')
             + '<p class="side-label">Artigos</p>'
             + ''.join(link(base + s + '/', n, s, c, t) for s, t, n, c in ARTS))
    return ('<aside class="sidebar" aria-label="Menu lateral"><div class="side-brand"><span>Coleção de artigos</span>'
            '<strong>Carlos Hernane de Oliveira</strong></div><nav class="side-nav">%s</nav>'
            '<p class="side-foot">Goiânia, 2026</p></aside>') % items


def nav(active, base):
    items = [(base or './', 'Início', 'home')] + [(base + s + '/', n, s) for s, _, n, _ in ARTS] + [(base + 'projetos/', 'Projetos', 'projetos')]
    links = ''.join('<a href="%s" class="%s"%s>%s</a>' % (h, ON if k == active else OFF, ' aria-current="page"' if k == active else '', l) for h, l, k in items)
    return ('<nav class="sticky top-0 z-50 border-b border-border/60 bg-background/90 backdrop-blur">'
            '<div class="mx-auto flex max-w-3xl items-center gap-2 overflow-x-auto px-6 py-3">%s</div></nav>') % links


def patch_menus(root):
    """Acrescenta os links dos artigos novos e de Projetos ao menu das páginas já geradas (idempotente)."""
    import re
    order = [a[0] for a in ARTS] + ['projetos']
    labels = {a[0]: a[2] for a in ARTS}
    labels['projetos'] = 'Projetos'
    for slug, _, _, _ in ARTS:
        f = '%s/%s/index.html' % (root, slug)
        h = open(f, encoding='utf8').read()
        for i, t in enumerate(order):
            if i < 5 or 'href="../%s/"' % t in h:
                continue
            m = re.search(r'<a href="\.\./%s/"[^>]*>[^<]*</a>' % re.escape(order[i - 1]), h)
            if not m:
                continue
            a = m.group(0).replace('../%s/' % order[i - 1], '../%s/' % t).replace(' aria-current="page"', '')
            a = re.sub(r'>[^<]*</a>$', '>%s</a>' % labels[t], a)
            a = a.replace('bg-primary text-primary-foreground', 'text-muted-foreground hover:bg-secondary')
            h = h.replace(m.group(0), m.group(0) + ('' if 'class=' in a else chr(10)) + a, 1)
        open(f, 'w', encoding='utf8').write(h)
