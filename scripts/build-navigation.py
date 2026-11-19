"""Synchronize the shared mobile navigation in the static parish pages."""

import argparse
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
LINKS = (
    ("/calendario.html", "Calendario de esta semana"),
    ("/horarios.html", "Horarios de Misa"),
    ("/centros.html", "Centros de Misa"),
    ("/primera-vez.html", "Primera vez en la Misa"),
    ("/noticias/", "Noticias y artículos"),
    ("/media.html", "Media"),
    ("/recursos.html", "Recursos"),
    ("/contacto.html", "Contacto"),
)
HEADER = re.compile(r'<header class="site-header\b[^"]*".*?</header>', re.S)
PARISH_MENU = re.compile(r'<section class="network-menu-section parish-menu"[^>]*>.*?</section>', re.S)
QUICK_NAV = re.compile(r'<nav\b[^>]*\bclass="mobile-quick-nav"[^>]*>.*?</nav>', re.S)
MENU_SCRIPT = '<script src="/js/parish-site.js?v=2" defer></script>'


def link(href, label, current):
    active = ' aria-current="page"' if href == current else ''
    return f'<a href="{href}"{active}>{label}</a>'


def sync(source, current):
    menu = '<section class="network-menu-section parish-menu" aria-label="Menú principal">' + (
        ''.join(link(href, label, current) for href, label in LINKS)
    ) + '</section>'
    quick_links = ''.join(link(href, label, current) for href, label in LINKS[:2])
    quick_nav = f'<nav class="mobile-quick-nav" aria-label="Accesos rápidos">{quick_links}</nav>'

    def update_header(match):
        header = match[0]
        if PARISH_MENU.search(header):
            header = PARISH_MENU.sub(lambda _: menu, header)
        else:
            header, count = re.subn(
                r'(<nav class="primary-nav"[^>]*>.*?</nav>)(</div>\s*</header>)',
                r'<div class="header-right">\1</div>'
                '<button class="menu-button" type="button" aria-label="Abrir menú de navegación" '
                'aria-expanded="false" aria-controls="site-pullouts"><span aria-hidden="true">☰</span></button>'
                r'\2', header, count=1, flags=re.S
            )
            if count != 1:
                raise ValueError(f"Missing parish menu or standalone header on {current}")
            panel = f'<div class="network-panel" id="site-pullouts" hidden><div class="container network-grid">{menu}</div></div>'
            header = header.replace('</header>', panel + '</header>')
        if QUICK_NAV.search(header):
            return QUICK_NAV.sub(lambda _: quick_nav, header, count=1)
        return header.replace('</header>', quick_nav + '</header>')

    source = HEADER.sub(update_header, source, count=1)
    source = re.sub(r'parish-sspx\.css(?:\?v=\d+)?(?=")', 'parish-sspx.css?v=14', source)
    source, count = re.subn(
        r'<script(?: src="/?js/parish-site\.js[^"]*"[^>]*>\s*|>\s*const pullouts = .*?)</script>',
        lambda _: MENU_SCRIPT, source, count=1, flags=re.S
    )
    if not count:
        source = source.replace('</body>', MENU_SCRIPT + '</body>', 1)
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for path in sorted(ROOT.rglob("*.html")):
        relative = path.relative_to(ROOT)
        if any(part.startswith(".") for part in relative.parts):
            continue
        source = path.read_text(encoding="utf-8")
        if not HEADER.search(source):
            continue
        current = "/" + relative.as_posix().removesuffix("index.html") if path.name == "index.html" else "/" + relative.as_posix()
        updated = sync(source, current)
        if updated != source:
            if args.check:
                stale.append(str(relative))
            else:
                path.write_text(updated, encoding="utf-8")
    if stale:
        raise SystemExit("Run python3 scripts/build-navigation.py for: " + ", ".join(stale))


if __name__ == "__main__":
    main()
