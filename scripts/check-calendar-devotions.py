#!/usr/bin/env python3
"""Check links on announced first-Friday/first-Saturday calendar devotions."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import argparse
import re
import sys
import unicodedata


class Node:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def text(self):
        return ' '.join(c if isinstance(c, str) else c.text() for c in self.children)

    def find(self, predicate):
        for child in self.children:
            if isinstance(child, Node):
                if predicate(child):
                    yield child
                yield from child.find(predicate)


class Document(HTMLParser):
    void = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.void:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def normalize(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text.lower()) if not unicodedata.combining(c))


def check(source):
    root = Document(source).root
    errors, checked = [], 0
    for row in root.find(lambda n: 'calendar-row' in n.attrs.get('class', '').split()):
        cells = list(row.find(lambda n: n.attrs.get('role') == 'cell'))
        if not cells:
            continue
        date = normalize(cells[0].text())
        match = re.search(r'\b(viernes|sabado)\s+([1-7])\s+de\b', date)
        if not match:
            continue
        slug = 'primer-viernes.html' if match[1] == 'viernes' else 'primer-sabado.html'
        for cell, location in zip(cells[1:], ['santiago', 'vina-del-mar']):
            for event in cell.find(lambda n: n.tag == 'li'):
                text = normalize(event.text())
                if not any(word in text for word in ['adoracion', 'hora santa', 'exposicion', 'rosario meditado', 'meditacion del rosario']):
                    continue
                checked += 1
                links = [urlsplit(a.attrs.get('href', '')) for a in event.find(lambda n: n.tag == 'a')]
                if not any(u.path.lstrip('/') == slug and u.fragment == location for u in links):
                    errors.append(f'{match[1]} {match[2]}, {location}: {event.text().strip()} → expected /{slug}#{location}')
    return errors, checked


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('calendar', nargs='?', type=Path, default=Path(__file__).resolve().parents[1] / 'calendario.html')
    args = parser.parse_args()
    errors, checked = check(args.calendar.read_text())
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    print(f'Calendar devotion links OK ({checked} announced devotional events checked).')
