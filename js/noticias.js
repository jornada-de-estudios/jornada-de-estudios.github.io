(() => {
  const filters = document.querySelector('.news-filters');
  const upcoming = document.querySelector('#proximos-eventos ul');
  const past = document.querySelector('#eventos-pasados ul');
  const recent = document.querySelector('#publicaciones-recientes ul');
  const today = new Intl.DateTimeFormat('sv-SE', {
    timeZone: 'America/Santiago', year: 'numeric', month: '2-digit', day: '2-digit'
  }).format(new Date());

  const events = [...document.querySelectorAll('[data-event-end]')].sort((left, right) =>
    left.querySelector('time').dateTime.localeCompare(right.querySelector('time').dateTime)
  );
  events.forEach(card => {
    const expired = card.dataset.eventEnd < today;
    card.querySelector('[data-past-label]').hidden = !expired;
    if (expired) past.prepend(card);
    else upcoming.append(card);
  });

  function update() {
    const selection = [...filters.querySelectorAll('[data-filter]')].find(
      link => link.hash === location.hash
    )?.dataset.filter || 'all';

    filters.querySelectorAll('[data-filter]').forEach(link => {
      if (link.dataset.filter === selection) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });

    recent.querySelectorAll('[data-type]').forEach(card => {
      card.hidden = selection !== 'all' && card.dataset.type !== selection;
    });
    upcoming.closest('section').hidden = !upcoming.children.length ||
      !['all', 'eventos'].includes(selection);
    past.closest('section').hidden = !past.children.length ||
      !['all', 'eventos'].includes(selection);
    recent.closest('section').hidden = !recent.querySelector('li:not([hidden])');
  }

  filters.hidden = false;
  window.addEventListener('hashchange', update);
  update();
})();
