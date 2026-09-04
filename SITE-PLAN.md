# Priorato Cristo Rey — Website Plan

## Purpose

Make the parish website the authoritative, easy-to-find public reference for the traditional Mass in Santiago: when Mass is celebrated, where the church is, what is happening this week, and where parish media and resources can be found.

The tone should be clear, dignified, and Catholic rather than promotional. The visual language should remain closely inspired by the SSPX sites: white space, Century serif headings, Libre Franklin interface text, restrained red and warm orange accents, soft gray surfaces, editorial photography, and a structured header with the SSPX network links.

## Proposed information architecture

### 1. Inicio

The homepage should answer a visitor's main questions quickly:

- What is this place?
- Where is it?
- When is Mass?
- What is happening this week?
- Where can I watch or read more?

It should contain the hero, regular Mass schedule, address/map link, a compact weekly-calendar teaser, latest YouTube content, and a small resource highlight. It should not contain the complete weekly calendar.

### 2. Horarios

Regular Mass schedule for the Priorato Cristo Rey, including:

- Sunday: 9:00, 11:00 sung Mass, 19:00
- Monday: 19:00
- Tuesday–Friday: 7:15 and 19:00
- Saturday: 7:15 and 12:00
- Confessions during all Masses
- First Friday and First Saturday information
- Notice that schedules may change

### 3. Esta semana

The full weekly calendar page, currently represented by `calendario.html`.

It should support:

- Liturgical day and feast information
- Separate columns for Santiago and Viña del Mar
- Activities such as catechism, Vespers, exposition, and courses
- Visits to other Chilean and foreign Mass centers
- A printable/downloadable version when available

The calendar should be transcribed into accessible HTML, with the original image or PDF optionally preserved as an attachment.

### 4. Centros de Misa

A stable directory for Mass centers and missions, separate from the changing weekly calendar. Each entry can include city, chapel, address, dates, contact details, and a map link.

### 5. Multimedia

A focused page for the Priorate's YouTube content:

- Live and recorded Masses
- Classes
- Conferences
- Homilies or other recurring categories, if available

The homepage should show only a small selection or latest-content block.

### 6. Recursos

A searchable or clearly categorized library for:

- Sacred Heart PDFs
- Devotional and doctrinal reading
- Bulletin or calendar downloads
- Links to Librería Fátima

### 7. Coro

A separate, low-prominence section for the choir. It can contain:

- Partitions by liturgical season or composer
- Audio practice files
- Notes for choir members
- A link to the existing music archive

It should not compete with Mass times, parish information, or public-facing media on the homepage.

### 8. El Priorato

Background information about the Priorato Cristo Rey, the Fraternidad Sacerdotal San Pío X in Chile, the priests, apostolates, catechism, and parish life. This content should be written deliberately rather than filled with generic promotional copy.

### 9. Contacto / Cómo llegar

Address, map, email or phone contact when confirmed, regular Mass times, and practical information for first-time visitors.

## Content and update model

The inexpensive first version should remain a static site suitable for GitHub Pages. Weekly information can live in one simple Markdown or JSON file, for example:

```text
content/weekly/2026-09-06.json
```

The calendar page would render that content into the same visual template each week. This preserves low hosting cost and makes the weekly update repeatable. A lightweight CMS can be added later only if someone needs browser-based editing.

## Visual/content work still required

1. Confirm the final parish name, subtitle, contact details, and public email.
2. Replace provisional homepage copy with approved Spanish wording.
3. Choose or photograph the final hero and section images.
4. Decide whether the weekly source image should also be downloadable.
5. Rebuild the existing music page within the new visual system as the choir section.
6. Add the remaining pages using the shared header, footer, typography, and network menus.
7. Add basic SEO and structured data for a Catholic church/Mass location.
8. Test mobile layout, accessibility, links, PDF downloads, and YouTube embeds.

## Implementation phases

### Phase 1 — Design approval

Finalize the homepage proportions, image treatment, colors, typography, header behavior, and Spanish copy.

### Phase 2 — Shared site shell

Create reusable page structure for header, SSPX network menus, footer, navigation, typography, buttons, cards, and responsive behavior.

### Phase 3 — Core pages

Build Horarios, Esta semana, Centros de Misa, Multimedia, Recursos, Coro, El Priorato, and Contacto.

### Phase 4 — Weekly publishing workflow

Move calendar content into a structured data file and document the weekly update process. Preserve the original calendar artwork when useful.

### Phase 5 — Quality and launch

Review copy, images, mobile behavior, accessibility, search indexing, link integrity, and performance. Deployment/hosting can remain separate until the design and content are approved.

## Current prototype status

- New SSPX-inspired homepage in `index.html`
- Separate weekly calendar page in `calendario.html`
- Core pages now scaffolded: `horarios.html`, `centros.html`, `multimedia.html`, `recursos.html`, `coro.html`, `priorato.html`, and `contacto.html`
- Actual SSPX `Century-Light` font loaded locally
- Actual SSPX logo asset used in the site shell
- Existing PDFs, YouTube channel, Librería Fátima link, and music archive retained
- Homepage copy and image choices still provisional
