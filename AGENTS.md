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
