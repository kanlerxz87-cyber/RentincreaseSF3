#!/usr/bin/env python3
"""Static integration checks. Does not establish legal accuracy or external availability."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from decimal import Decimal
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / 'index.html', *sorted((ROOT / 'pages').glob('*.html'))]
HTML = sorted(p for p in ROOT.rglob('*.html') if '.git' not in p.parts)
errors = []
class Check(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.links = []
        self.row = None
        self.data_cells = 0
        self.row_source = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'tr': self.row, self.data_cells, self.row_source = True, 0, False
        if tag == 'td' and self.row: self.data_cells += 1
        if tag in ('a', 'link') and a.get('href'):
            self.links.append(a['href'])
            if self.row and urlsplit(a['href']).hostname in {'www.sf.gov', 'sf.gov', 'portal.sfrb.org', 'sfgov.legistar.com', 'www.hud.gov', 'calcivilrights.ca.gov', 'leginfo.legislature.ca.gov'}:
                self.row_source = True
        if tag == 'meta' and a.get('http-equiv','').lower() == 'refresh':
            match = re.search(r'url=(.*)', a.get('content',''), re.I)
            if match: self.links.append(match.group(1))
    def handle_endtag(self, tag):
        if tag == 'tr' and self.row:
            if self.data_cells and not self.row_source: errors.append(f'{self.path}: table row without official link')
            self.row = None
parsers = {}
for p in HTML:
    parser = Check(p.relative_to(ROOT))
    parser.feed(p.read_text(encoding='utf-8'))
    parsers[p] = parser
    if p in PAGES:
        text = p.read_text(encoding='utf-8')
        for private in ('94122', 'outer sunset'):
            if private in text.lower(): errors.append(f'{p}: private location found')
for p, parser in parsers.items():
    for href in parser.links:
        u = urlsplit(href)
        if u.scheme or u.netloc: continue
        target = (p.parent / unquote(u.path)).resolve() if u.path else p
        if target.is_dir(): target = target / 'index.html'
        if not target.is_file(): errors.append(f'{p.relative_to(ROOT)}: missing {href}')
        elif u.fragment and target in parsers and unquote(u.fragment) not in parsers[target].ids:
            errors.append(f'{p.relative_to(ROOT)}: missing anchor {href}')
assert Decimal('3995') * Decimal('.016') == Decimal('63.92')
assert Decimal('3150') * Decimal('.016') == Decimal('50.40')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(HTML)} HTML files, internal links/redirects, table source links, location scan and illustrative arithmetic')
print('External availability and substantive legal accuracy require separate source review.')
