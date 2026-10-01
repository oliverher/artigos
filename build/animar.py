"""Aplica as animações aos artigos 01 a 03 (HTML gerado pelo build.py)."""
import re
import infograficos2

S = 'docs'
# artigo -> (imagem substituída pelo infográfico animado, função)
INFO = {
    'proposito-de-vida': ('figura-5.jpg', infograficos2.trilha),
    'mente-e-corpo': ('mente-corpo-figura-11.jpg', infograficos2.niveis),
    'bpm-em-pmes': ('bpm-pmes-figura-5.jpg', infograficos2.ciclo),
}


def patch(slug):
    f = '%s/%s/index.html' % (S, slug)
    h = open(f, encoding='utf8').read()
    img, fn = INFO[slug]
    h = h.replace('<figure class="mt-6 ', '<figure class="reveal mt-6 ')

    def wrap(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag).group(1)
        if src.endswith(img):
            return fn()
        return ('<a href="%s" target="_blank" rel="noopener" title="Abrir a imagem em tamanho original">%s</a>' % (src, tag))
    h = re.sub(r'<img [^>]*class="aspect-video[^>]*/>', wrap, h)
    # link para a imagem original na legenda do infográfico
    h = re.sub(r'(role="group" aria-label="Infográfico.*?<figcaption.*?<span class="mt-1 block[^>]*>)(.*?)(</span></figcaption>)',
               lambda m: m.group(1) + m.group(2) + ' <a class="underline underline-offset-2" href="../assets/img/%s" target="_blank" rel="noopener">Ver a imagem original</a>' % img + m.group(3),
               h, count=1, flags=re.S)
    h = h.replace('</head>', '<link rel="stylesheet" href="../assets/anim.css"/><script>document.documentElement.classList.add("js")</script></head>', 1)
    h = h.replace('</body>', '<script src="../assets/anim.js"></script></body>', 1)
    open(f, 'w', encoding='utf8').write(h)
