# Repository publishing guidance

## Bulletin structure

- Keep the bulletin archive at `boletin/index.html`.
- Put each edition at `boletin/YYYYMM/index.html` and its articles in that same edition directory.
- Use the edition page to link to every article in that issue; link the archive to every edition.
- When moving an article, update its canonical URL, breadcrumbs, internal links, archive and edition cards, homepage/resource links, and `sitemap.xml` together.
- Keep established root-level bulletin URLs as redirects to the canonical archive, edition, or article URL so older links continue to work.

## Editorial images

- Give every article its own relevant image set. Do not reuse an editorial image between separate articles, or repeat one image as both an article's hero and body illustration.
- For reporting about a specific real place, use documented photographs of that place; do not use synthetic or generic architecture as if it depicted the location.
- For decorative images, use empty alternative text (`alt=""`) and no caption. Never add filler captions such as “Imagen editorial creada para acompañar el artículo”.
- Keep decorative artwork directly related to the article's subject and visual style.

## First Friday and First Saturday calendar updates

When updating `calendario.html`, including transcribing an uploaded calendar image:

- Identify first Fridays and first Saturdays by weekday and day of month (1–7).
- Link announced devotional celebrations on those dates to `/primer-viernes.html` or `/primer-sabado.html`. Use `#santiago` or `#vina-del-mar` for the relevant location.
- Preserve the image's actual times and exceptions. Never add an unannounced celebration or replace a dated exception with a landing page's usual schedule.
- Keep the homepage's existing devotion paragraphs, with a “Más información” link in each paragraph.
- Run `python3 scripts/check-calendar-devotions.py` after every calendar update and resolve missing links before committing.
- Keep changing dates and exceptional schedules in the weekly calendar; the landing pages explain the usual practice. January and February usually end First Friday adoration at midnight.

## Sermon publishing scope

- Adding or publishing a sermon in the Sermones section must leave the homepage unchanged unless the user explicitly requests a homepage update.
- Do not automatically add sermon highlights, carousel slides, or links to individual sermons on the homepage.
- Preserve the homepage's general link to the sermon archive.

## Authorization for live editorial text

- Never add editorial or process commentary to the live site without the user's explicit authorization. This includes notes about transcription cleanup, removed timestamps or fillers, unclear passages, uncertainty labels, and similar explanations.
- Discuss editorial decisions, limitations, and review concerns in chat instead of publishing them as site content.

## Noticias y artículos

- When publishing a new sermon, article, translation, or substantial parish announcement anywhere on the site, check whether it belongs in Noticias y artículos. Index new sermons and editorial articles by default. Keep the original page in its section (for example, `sermones/` or its `boletin/YYYYMM/` issue), update that section's own listing, and add one entry pointing at its canonical URL in `noticias/publicaciones.json`.
- Use `articulos` for long-form reading, sermons, and devotional guides, `avisos` for news with lasting interest such as a documentary release, and `eventos` for celebrations or activities with a dedicated public program. Put short notices about confession arrangements, cancellations, ordinary service times, and weekly schedule exceptions in `calendario.html`. Leave those out of the publication index.
- Each entry needs `title`, `type`, `published` (YYYY-MM-DD), and `url` (a root-relative canonical page). Add a short Spanish `summary` when helpful. Use optional `updated` for a meaningful follow-up such as a documentary release. Keep corrections and later updates on the existing entry.
- For events, add `date` for the first day and `end` for the final day of a multi-day event, using Santiago local dates. Include time, venue, directions, and visitor details as applicable on the event page. Keep past event pages accessible. Give each year's event its own dated URL.
- Point homepage editorial hero links to the canonical publication or event page. A dated hero slide uses `data-expires` with a timezone-qualified timestamp. Keep slides and their corresponding dots in the same order. The homepage preview excludes individual sermons and items already linked from the hero.
- For a multi-part work, link installments to the series reading order once there are enough published installments for a series page. Include original author, title, edition or year where known, translator, source link, and applicable permissions or credit on translations.
- Run `python3 scripts/build-news.py` whenever the publication list or homepage hero links change. Include the refreshed `noticias/index.html` and homepage preview in the same change. Use `python3 scripts/build-news.py --check` to verify generated markup. Add new canonical pages to `sitemap.xml`.
