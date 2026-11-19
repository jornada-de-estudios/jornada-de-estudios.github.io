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


def card(entry, today, *, archive=False, eager=False):
    kind = entry["type"]
    date = entry.get("date", entry.get("updated", entry["published"]))
    attributes = f'data-type="{kind}"'
    label = LABELS[kind]
    if kind == "eventos":
        event_end = entry.get("end", date)
        attributes += f' data-event-end="{event_end}"'
        label += f'<span data-past-label{"" if event_end < today else " hidden"}> pasado</span>'
    summary = escape(entry["summary"])
    end = f'<span> – {date_label(entry["end"])}</span>' if "end" in entry else ""
    timestamp = f'<time datetime="{date}">{date_label(date)}</time>{end}'
    title = escape(entry["title"])
    href = escape(entry["url"])
    if not archive:
        return (
            f'        <li class="news-card" {attributes}><a class="resource-card" href="{href}">'
            f'<span class="section-kicker">{label}</span><h3>{title}</h3>{timestamp}'
            f'<p>{summary}</p></a></li>'
        )

    image = entry.get("image")
    media = (
        f'<div class="news-entry-image"><img src="{escape(image)}" alt="" '
        f'loading="{"eager" if eager else "lazy"}" decoding="async"></div>'
        if image else ""
    )
    format_label = entry.get("format")
    if format_label:
        label += f' <span class="news-entry-format">{escape(format_label)}</span>'
    return (
        f'        <li class="news-entry{"" if image else " news-entry-text"}" {attributes} '
        f'data-published="{entry["published"]}">\n'
        f'          <a class="news-entry-link" href="{href}">{media}\n'
        f'            <div class="news-entry-copy"><p class="news-entry-type">{label}</p>'
        f'<h2>{title}</h2><p class="news-entry-summary">{summary}</p>'
        f'<p class="news-entry-date">{timestamp}</p></div>\n'
        '          </a>\n'
        '        </li>'
    )


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
        if not entry.get("summary", "").strip():
            raise SystemExit(f"Missing editorial summary: {url}")
        image = entry.get("image")
        if image and not (image.startswith("https://") or
                          image.startswith("/") and (ROOT / image[1:]).is_file()):
            raise SystemExit(f"Missing publication image: {image}")
        urls.add(url)

    visible = sorted((entry for entry in entries if entry["published"] <= today),
                     key=lambda entry: entry["published"], reverse=True)
    upcoming = min(
        (entry for entry in visible if entry["type"] == "eventos"
         and entry.get("end", entry["date"]) >= today),
        key=lambda entry: entry["date"], default=None
    )
    archive_entries = [upcoming, *(entry for entry in visible if entry is not upcoming)] if upcoming else visible
    archive_cards = [card(entry, today, archive=True, eager=index < 2)
                     for index, entry in enumerate(archive_entries)]
    replace_block(archive, "NEWS ARCHIVE", "\n".join([
        '      <ul class="news-feed" aria-label="Publicaciones">',
        *archive_cards,
        '      </ul>',
    ]), args.check)
    replace_block(home, "NEWS PREVIEW", "\n".join(card(entry, today) for entry in visible[:3]), args.check)


if __name__ == "__main__":
    main()
