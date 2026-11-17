(() => {
  const host = document.getElementById('ordo');
  if (!host) return;

  // Try Spanish first so upstream support takes effect automatically.
  const load = (lang) => new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = `https://ordo.fsspx.org/embed/lines.js?lang=${lang}&source=chilia&marianBlue=1`;
    script.async = true;
    script.onload = () => host.shadowRoot ? resolve() : reject();
    script.onerror = reject;
    document.head.appendChild(script);
  });

  const start = async () => {
    try {
      await load('es');
    } catch {
      try {
        await load('la');
      } catch {
        console.error('[Ordo] Calendar could not be loaded.');
      }
    }
  };
  start();
})();
