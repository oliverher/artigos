"""Barra lateral e menu de pílulas compartilhados pela página inicial e pela página de projetos."""

ARTS = [
    ('proposito-de-vida', 'Artigo 01', 'Propósito de vida', '#137d5c'),
    ('mente-e-corpo', 'Artigo 02', 'Mente e corpo', '#cf7638'),
    ('bpm-em-pmes', 'Artigo 03', 'BPM em PMEs', '#276fa0'),
    ('passaporte-pessoa-idosa', 'Artigo 04', 'Transformação de Serviço', '#7a4fa3'),
    ('pmbok-dialetica', 'Artigo 05', 'Evolução do PMBOK', '#a8483a'),
    ('mmdi-go', 'Artigo 06', 'MMDI-GO', '#1f8a8a'),
    ('ia-no-setor-publico', 'Artigo 07', 'IA no setor público', '#2d5bd1'),
    ('governanca-ux-ia', 'Artigo 08', 'Governança e UX', '#b8336a'),
    ('ciencia-comportamental-orgao', 'Artigo 09', 'Ciência comportamental', '#4a6b2f'),
]
PILL = 'shrink-0 rounded-full px-4 py-1.5 text-sm font-medium transition-colors '
OFF = PILL + 'text-muted-foreground hover:bg-secondary'
ON = PILL + 'bg-primary text-primary-foreground'


def sidebar(active, base, apps=None, cats=None):
    """Com apps/cats (página de projetos), a lista lateral mostra os aplicativos por tema, em vez dos artigos."""
    def link(href, label, key, dot=None, small=None):
        cls = 'side-link' + (' is-active' if key == active else '')
        cur = ' aria-current="page"' if key == active else ''
        d = '<span class="side-dot" style="background:%s"></span>' % dot if dot else '<span class="side-dot side-home"></span>'
        s = '<small>%s</small>' % small if small else ''
        return '<a href="%s" class="%s"%s>%s<span>%s%s</span></a>' % (href, cls, cur, d, s, label)
    topo = link(base or './', 'Início', 'home') + link('https://oliverher.github.io/projetos-ia/', 'Projetos - Aplicativos desenvolvidos com IA', 'projetos')
    if apps is None:
        items = topo + '<p class="side-label">Artigos</p>' + ''.join(link(base + s + '/', n, s, c, t) for s, t, n, c in ARTS)
    else:
        items = topo
        for k, nome, cor in cats:
            lista = [a for a in apps if a[0] == k]
            items += '<p class="side-label">%s</p>' % nome + ''.join(
                '<a href="%s" class="side-link" target="_blank" rel="noopener noreferrer"><span class="side-dot" style="background:%s"></span><span>%s</span></a>'
                % (a[3], cor, a[1]) for a in lista)
    return ('<aside class="sidebar" aria-label="Menu lateral"><div class="side-brand"><span>Coleção de artigos</span>'
            '<strong>Carlos Hernane de Oliveira</strong></div><nav class="side-nav">%s</nav>'
            '<p class="side-foot">Goiânia, 2026</p></aside>') % items


def nav(active, base):
    items = [(base or './', 'Início', 'home')] + [(base + s + '/', n, s) for s, _, n, _ in ARTS] + [('https://oliverher.github.io/projetos-ia/', 'Projetos', 'projetos')]
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
