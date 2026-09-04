(() => {
  const pullouts = document.querySelector('#site-pullouts');
  const menuButton = document.querySelector('.menu-button');
  if (!pullouts || !menuButton) return;

  const panelToggles = [...document.querySelectorAll('[data-panel-toggle]')];
  const panels = [...document.querySelectorAll('.network-menu-section')];
  const setPanelState = (targetId) => {
    pullouts.hidden = false;
    panels.forEach((panel) => { panel.hidden = targetId ? panel.id !== targetId : false; });
    panelToggles.forEach((button) => button.setAttribute('aria-expanded', String(button.dataset.panelToggle === targetId)));
    menuButton.setAttribute('aria-expanded', 'false');
  };

  panelToggles.forEach((button) => button.addEventListener('click', () => {
    const targetId = button.dataset.panelToggle;
    const isOpen = button.getAttribute('aria-expanded') === 'true';
    if (isOpen) {
      pullouts.hidden = true;
      panels.forEach((panel) => { panel.hidden = true; });
      button.setAttribute('aria-expanded', 'false');
    } else setPanelState(targetId);
  }));

  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!open));
    pullouts.hidden = open;
    panels.forEach((panel) => { panel.hidden = open ? true : false; });
    panelToggles.forEach((button) => button.setAttribute('aria-expanded', 'false'));
  });
})();
