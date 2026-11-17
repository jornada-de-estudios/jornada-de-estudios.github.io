(() => {
  const host = document.getElementById('ordo');
  const status = document.getElementById('ordo-status');
  if (!host || !status) return;

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
      status.hidden = true;
    } catch {
      try {
        await load('la');
        status.textContent = 'El Ordo integrado está disponible por ahora en latín. Puede consultar el sitio del Ordo en español mediante el enlace superior.';
      } catch {
        status.textContent = 'No se pudo cargar el calendario. Consulte el Ordo mediante el enlace superior.';
      }
    }
  };
  start();
})();
