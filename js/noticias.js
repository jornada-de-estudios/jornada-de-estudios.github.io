(() => {
  const archive = document.querySelector('.news-archive');
  const filters = archive.querySelector('.news-filters');
  const feed = archive.querySelector('.news-feed');
  const cards = [...feed.children];
  const choices = [...filters.querySelectorAll('[data-filter]')];
  const today = new Intl.DateTimeFormat('sv-SE', {
    timeZone: 'America/Santiago', year: 'numeric', month: '2-digit', day: '2-digit'
  }).format(new Date());

  feed.querySelectorAll('img').forEach(image => {
    const useTextLayout = () => {
      image.closest('.news-entry').classList.add('news-entry-text');
      image.parentElement.remove();
    };
    if (image.complete && !image.naturalWidth) useTextLayout();
    else image.addEventListener('error', useTextLayout, {once: true});
  });

  const events = cards.filter(card => card.dataset.eventEnd);
  events.forEach(card => {
    card.querySelector('[data-past-label]').hidden = card.dataset.eventEnd >= today;
  });
  const upcoming = events.filter(card => card.dataset.eventEnd >= today).sort((left, right) =>
    left.querySelector('time').dateTime.localeCompare(right.querySelector('time').dateTime)
  )[0];

  cards.sort((left, right) => right.dataset.published.localeCompare(left.dataset.published));
  feed.append(...cards);
  if (upcoming) feed.prepend(upcoming);

  function update() {
    const selection = choices.find(link => link.hash === location.hash)?.dataset.filter || 'all';
    archive.dataset.selection = selection;
    choices.forEach(link => {
      if (link.dataset.filter === selection) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });

    for (const card of cards) {
      card.hidden = selection !== 'all' && card.dataset.type !== selection;
    }
  }

  filters.hidden = false;
  window.addEventListener('hashchange', update);
  update();
})();
