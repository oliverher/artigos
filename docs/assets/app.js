document.querySelectorAll('button[aria-expanded]').forEach(function (b) {
  b.addEventListener('click', function () {
    var open = b.getAttribute('aria-expanded') === 'true';
    var card = b.parentElement, dot = b.children[0], chev = b.children[2], panel = b.nextElementSibling;
    b.setAttribute('aria-expanded', String(!open));
    card.classList.toggle('border-ochre/60', !open);
    card.classList.toggle('shadow-[var(--shadow-lift)]', !open);
    card.classList.toggle('shadow-[var(--shadow-soft)]', open);
    dot.classList.toggle('bg-ochre', !open);
    dot.classList.toggle('bg-sage', open);
    chev.classList.toggle('rotate-180', !open);
    chev.classList.toggle('text-ochre', !open);
    chev.classList.toggle('text-muted-foreground', open);
    panel.classList.toggle('grid-rows-[1fr]', !open);
    panel.classList.toggle('opacity-100', !open);
    panel.classList.toggle('grid-rows-[0fr]', open);
    panel.classList.toggle('opacity-0', open);
  });
});
