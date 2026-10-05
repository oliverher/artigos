/* Galeria animada do artigo 06: entrada em cortina, partículas, inclinação 3D, brilho que segue o cursor
   e um "tour" com holofote que percorre as regiões de cada imagem. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var figs = document.querySelectorAll('.gfig');
  if (!figs.length) return;
  var STEP = 4600;
  var ICON_PAUSE = '<svg class="i-pause" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>';
  var ICON_PLAY = '<svg class="i-play" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.8v14.4a1 1 0 0 0 1.5.86l12-7.2a1 1 0 0 0 0-1.72l-12-7.2A1 1 0 0 0 7 4.8z"/></svg>';

  function esc(s) { return s.replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }

  function setup(fig) {
    var tour = [];
    try { tour = JSON.parse(fig.getAttribute('data-tour') || '[]'); } catch (e) { }
    var stage = fig.querySelector('.gfig-stage');
    var zoom = fig.querySelector('.gfig-zoom');
    var fx = fig.querySelector('.gfig-fx');
    var spot = fig.querySelector('.gfig-spot');
    var bar = fig.querySelector('.gfig-bar');
    var idx = -1, timer = null, playing = !reduce, inView = false, manual = false;

    // partículas
    if (!reduce) {
      for (var i = 0; i < 16; i++) {
        var p = document.createElement('i');
        p.className = 'gfig-p';
        p.style.setProperty('--x', (Math.random() * 100).toFixed(1) + '%');
        p.style.setProperty('--s', (2 + Math.random() * 3).toFixed(1) + 'px');
        p.style.setProperty('--d', (7 + Math.random() * 7).toFixed(1) + 's');
        p.style.setProperty('--dl', (-Math.random() * 10).toFixed(1) + 's');
        p.style.setProperty('--r', (180 + Math.random() * 320).toFixed(0) + 'px');
        p.style.setProperty('--c', Math.random() > .5 ? '#ffd36b' : '#3df2b5');
        fx.appendChild(p);
      }
    }

    // controles
    var playBtn = null, dots = [], live = null;
    if (bar && tour.length) {
      bar.innerHTML = '<button type="button" class="gfig-play" aria-label="Pausar ou retomar o destaque automático">' + ICON_PAUSE + ICON_PLAY + '</button>' +
        '<div class="gfig-dots" role="group" aria-label="Regiões em destaque">' +
        tour.map(function (t, k) { return '<button type="button" class="gfig-dot" aria-label="Destaque ' + (k + 1) + ': ' + esc(t[4]).replace(/"/g, '&quot;') + '">' + (k + 1) + '</button>'; }).join('') +
        '</div><p class="gfig-live" aria-live="polite"></p>';
      playBtn = bar.querySelector('.gfig-play');
      dots = [].slice.call(bar.querySelectorAll('.gfig-dot'));
      live = bar.querySelector('.gfig-live');
      playBtn.addEventListener('click', function () {
        playing = !playing; manual = false;
        syncBtn();
        if (playing) { idx = idx < 0 ? -1 : idx; next(); } else clearTimeout(timer);
      });
      dots.forEach(function (d, k) {
        d.addEventListener('click', function () { playing = false; syncBtn(); clearTimeout(timer); show(k); });
      });
      syncBtn();
      live.innerHTML = '<span>Use os números para destacar as regiões da imagem.</span>';
    }

    function syncBtn() { if (playBtn) playBtn.setAttribute('data-state', playing ? 'playing' : 'paused'); }

    function show(k) {
      idx = k;
      var t = tour[k];
      spot.style.setProperty('--l', t[0] + '%');
      spot.style.setProperty('--t', t[1] + '%');
      spot.style.setProperty('--w', t[2] + '%');
      spot.style.setProperty('--h', t[3] + '%');
      spot.setAttribute('data-n', k + 1);
      spot.classList.add('on');
      dots.forEach(function (d, j) { if (j === k) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); });
      if (live) live.innerHTML = '<span><b>' + (k + 1) + '/' + tour.length + '</b> ' + esc(t[4]) + '</span>';
    }

    function clear() {
      spot.classList.remove('on');
      dots.forEach(function (d) { d.removeAttribute('aria-current'); });
      if (live) live.innerHTML = '<span>Use os números para destacar as regiões da imagem.</span>';
      idx = -1;
    }

    function next() {
      clearTimeout(timer);
      if (!playing || !inView || !tour.length) return;
      if (idx + 1 >= tour.length) {           // fim do ciclo: mostra a imagem inteira e recomeça
        clear();
        timer = setTimeout(next, 2600);
        return;
      }
      show(idx + 1);
      timer = setTimeout(next, STEP);
    }

    // inclinação 3D e brilho que segue o cursor
    if (!reduce && window.matchMedia('(pointer: fine)').matches) {
      stage.addEventListener('pointermove', function (e) {
        var r = stage.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        stage.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
        stage.style.setProperty('--my', (y * 100).toFixed(1) + '%');
        zoom.style.transform = 'rotateX(' + ((.5 - y) * 3.2).toFixed(2) + 'deg) rotateY(' + ((x - .5) * 4.2).toFixed(2) + 'deg)';
        zoom.style.animation = 'none';
      });
      stage.addEventListener('pointerleave', function () {
        zoom.style.transition = 'transform .6s ease';
        zoom.style.transform = '';
        zoom.style.animation = '';
        setTimeout(function () { zoom.style.transition = ''; }, 650);
      });
    }

    return {
      enter: function () {
        inView = true; fig.classList.add('is-in'); fig.classList.add('is-live');
        if (playing && idx < 0) { clearTimeout(timer); timer = setTimeout(next, reduce ? 0 : 1700); }
        else if (playing) next();
      },
      leave: function () { inView = false; fig.classList.remove('is-live'); clearTimeout(timer); }
    };
  }

  var items = [].map.call(figs, function (f) { return { f: f, api: setup(f) }; });

  if (!('IntersectionObserver' in window)) {
    items.forEach(function (it) { it.f.classList.add('is-in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      var it = items.filter(function (x) { return x.f === en.target; })[0];
      if (en.isIntersecting) it.api.enter(); else it.api.leave();
    });
  }, { threshold: 0.35 });
  items.forEach(function (it) { io.observe(it.f); });
})();
