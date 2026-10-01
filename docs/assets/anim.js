(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els = document.querySelectorAll('.reveal, .ig');

  function run(c) {
    var from = +c.dataset.from, to = +c.dataset.to, suf = c.dataset.suffix || '';
    var delay = +(c.dataset.delay || 0), dur = +(c.dataset.dur || 1400), t0 = null;
    function step(t) {
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / dur), k = 1 - Math.pow(1 - p, 3);
      c.textContent = Math.round(from + (to - from) * k) + suf;
      if (p < 1) requestAnimationFrame(step);
    }
    setTimeout(function () { requestAnimationFrame(step); }, delay);
  }

  if (reduce || !('IntersectionObserver' in window)) {
    els.forEach(function (el) { el.classList.add('is-in'); });
    return;
  }
  document.querySelectorAll('[data-count]').forEach(function (c) {
    c.textContent = c.dataset.from + (c.dataset.suffix || '');
  });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add('is-in');
      en.target.querySelectorAll('[data-count]').forEach(run);
      io.unobserve(en.target);
    });
  }, { threshold: 0.2, rootMargin: '0px 0px -8% 0px' });
  els.forEach(function (el) { io.observe(el); });
})();
