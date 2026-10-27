(() => {
  const hero = document.querySelector('.hero');
  if (!hero) return;
  const track = hero.querySelector('.hero-slides');
  const slides = [...track.querySelectorAll('.hero-slide')];
  const dots = [...hero.querySelectorAll('.hero-dot')];
  const pause = hero.querySelector('.hero-pause');
  const status = hero.querySelector('.hero-status');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let active = 0, paused = reduced.matches, timer, settle;
  function render() {
    slides.forEach((slide, i) => {
      slide.classList.toggle('is-active', i === active);
      slide.setAttribute('aria-roledescription', 'diapositiva');
      slide.setAttribute('aria-label', `${i + 1} de ${slides.length}`);
      slide.setAttribute('aria-hidden', String(i !== active));
      slide.inert = i !== active;
      dots[i].classList.toggle('is-active', i === active);
      dots[i].setAttribute('aria-pressed', String(i === active));
    });
    pause.innerHTML = paused ? '<span aria-hidden="true">▶</span> Reanudar' : '<span aria-hidden="true">Ⅱ</span> Pausar';
    pause.setAttribute('aria-label', paused ? 'Reanudar rotación automática' : 'Pausar rotación automática');
  }
  function schedule() {
    clearInterval(timer);
    if (!paused && !document.hidden) timer = setInterval(() => go(active + 1), 7000);
  }
  function setPaused(value) { paused = value; render(); schedule(); }
  function go(index, manual = false) {
    active = (index + slides.length) % slides.length;
    if (manual) { paused = true; status.textContent = `Destacado ${active + 1} de ${slides.length}`; }
    render();
    track.scrollTo({ left: slides[active].offsetLeft, behavior: reduced.matches ? 'instant' : 'smooth' });
    schedule();
  }
  hero.querySelector('[data-hero-prev]').addEventListener('click', () => go(active - 1, true));
  hero.querySelector('[data-hero-next]').addEventListener('click', () => go(active + 1, true));
  dots.forEach((dot, i) => dot.addEventListener('click', () => go(i, true)));
  pause.addEventListener('click', () => setPaused(!paused));
  track.addEventListener('pointerdown', () => setPaused(true), { passive: true });
  track.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault(); go(active + (event.key === 'ArrowRight' ? 1 : -1), true);
    }
  });
  hero.addEventListener('focusin', event => { if (!pause.contains(event.target)) setPaused(true); });
  track.addEventListener('scroll', () => {
    clearTimeout(settle);
    settle = setTimeout(() => {
      const index = Math.round(track.scrollLeft / track.clientWidth);
      if (index >= 0 && index < slides.length && index !== active) { active = index; render(); }
    }, 180);
  }, { passive: true });
  window.addEventListener('resize', () => track.scrollTo({ left: slides[active].offsetLeft, behavior: 'instant' }));
  document.addEventListener('visibilitychange', schedule);
  reduced.addEventListener('change', () => { if (reduced.matches) setPaused(true); });
  render(); schedule();
})();
