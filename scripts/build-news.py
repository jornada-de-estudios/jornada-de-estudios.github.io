"""Refresh the static news archive and homepage preview from the publication list."""

import argparse
from datetime import datetime
from html import escape
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
LABELS = {"eventos": "Evento", "avisos": "Aviso", "articulos": "Artículo"}
MONTHS = "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()


def date_label(value):
    _, month, day = value.split("-")
    return f"{int(day)} de {MONTHS[int(month) - 1]} de {value[:4]}"


def card(entry, past=False):
    kind = entry["type"]
    date = entry.get("date", entry.get("updated", entry["published"]))
    attributes = f'data-type="{kind}"'
    label = LABELS[kind]
    if kind == "eventos":
        attributes += f' data-event-end="{entry.get("end", date)}"'
        label += f'<span data-past-label{"" if past else " hidden"}> pasado</span>'
    summary = f'<p>{escape(entry["summary"])}</p>' if entry.get("summary") else ""
    end = f' – {date_label(entry["end"])}' if "end" in entry else ""
    return (
        f'        <li class="news-card" {attributes}><span class="section-kicker">{label}</span>'
        f'<h3><a href="{escape(entry["url"])}">{escape(entry["title"])}</a></h3>'
        f'<time datetime="{date}">{date_label(date)}</time>{f"<span>{end}</span>" if end else ""}'
        f'{summary}</li>'
    )


def section(identifier, title, cards):
    return "\n".join([
        f'      <section id="{identifier}"{" hidden" if not cards else ""}>',
        f'        <h2>{title}</h2>',
        '        <ul class="news-grid">',
        *cards,
        '        </ul>',
        '      </section>',
    ])


def replace_block(path, block, content, check):
    source = path.read_text(encoding="utf-8")
    pattern = rf'(<!-- BEGIN {block} -->)\n.*?(^[ \t]*<!-- END {block} -->)'
    updated, count = re.subn(pattern, lambda match: f"{match[1]}\n{content}\n{match[2]}",
                             source, flags=re.S | re.M)
    if count != 1:
        raise SystemExit(f"Expected one {block} block in {path}")
    if source != updated:
        if check:
            raise SystemExit(f"{path.relative_to(ROOT)} is stale. Run python3 scripts/build-news.py.")
        path.write_text(updated, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--as-of", help="Override the Santiago date for the static event labels")
    args = parser.parse_args()
    today = args.as_of or datetime.now(ZoneInfo("America/Santiago")).date().isoformat()
    archive = ROOT / "noticias/index.html"
    home = ROOT / "index.html"
    entries = json.loads((ROOT / "noticias/publicaciones.json").read_text(encoding="utf-8"))
    urls = set()
    for entry in entries:
        url = entry["url"]
        target = ROOT / url.lstrip("/")
        if url.endswith("/"):
            target /= "index.html"
        if url in urls or not url.startswith("/") or not target.is_file():
            raise SystemExit(f"Duplicate or missing publication URL: {url}")
        urls.add(url)

    visible = [entry for entry in entries if entry["published"] <= today]
    events = sorted((entry for entry in visible if entry["type"] == "eventos"),
                    key=lambda entry: entry["date"])
    upcoming = [entry for entry in events if entry.get("end", entry["date"]) >= today]
    past = [entry for entry in reversed(events) if entry.get("end", entry["date"]) < today]
    recent = sorted((entry for entry in visible if entry["type"] != "eventos"),
                    key=lambda entry: entry.get("updated", entry["published"]), reverse=True)
    replace_block(archive, "NEWS ARCHIVE", "\n".join([
        section("proximos-eventos", "Próximos eventos", [card(entry) for entry in upcoming]),
        section("publicaciones-recientes", "Publicaciones recientes", [card(entry) for entry in recent]),
        section("eventos-pasados", "Eventos pasados", [card(entry, past=True) for entry in past]),
    ]), args.check)
    hero = home.read_text(encoding="utf-8").split('id="hero-slides"', 1)[1].split('class="hero-controls"', 1)[0]
    featured = set(re.findall(r'href="([^"]+)"', hero))
    preview = [entry for entry in recent
               if entry["url"] not in featured and not entry["url"].startswith("/sermones/")][:3]
    replace_block(home, "NEWS PREVIEW", "\n".join(card(entry) for entry in preview), args.check)


if __name__ == "__main__":
    main()
