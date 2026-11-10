#!/usr/bin/env python3
"""Offline integration checks; NOT a legal or remote-page verifier."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from decimal import Decimal
import json
import re
import sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from privacy_scan import scan_text
CANON=[ROOT/'index.html', *sorted((ROOT/'audit').glob('*.html'))]
DOMAINS={'www.sf.gov','sf.gov','leginfo.legislature.ca.gov','calcivilrights.ca.gov','www.hud.gov','sfgov.legistar.com'}
errors=[]
class Scan(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True); self.links=[]; self.ids=set(); self.rows=[]; self.row=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for attr in ['href','src']:
   if attr in a:self.links.append(a[attr])
  if tag=='tr':self.row={'data':False,'official':False}
  if self.row is not None:
   if tag=='td':self.row['data']=True
   if tag=='a' and urlsplit(a.get('href','')).hostname in DOMAINS:self.row['official']=True
 def handle_endtag(self,tag):
  if tag=='tr' and self.row is not None:self.rows.append(self.row); self.row=None
scans={}
for f in ROOT.rglob('*.html'):
 if '.git' in f.parts:continue
 s=Scan(); s.feed(f.read_text()); scans[f]=s
for f,s in scans.items():
 for href in s.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  target=(f.parent/unquote(u.path)).resolve() if u.path else f
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{f.relative_to(ROOT)}: missing {href}')
  elif u.fragment and target in scans and unquote(u.fragment) not in scans[target].ids:
   errors.append(f'{f.relative_to(ROOT)}: missing anchor {href}')
for f in CANON:
 s=scans[f]; text=f.read_text()
 for i,row in enumerate(s.rows,1):
  if row['data'] and not row['official']:errors.append(f'{f.name} row {i}: no official source')
 if not s.ids or 'main' not in s.ids:errors.append(f'{f.name}: missing main anchor')
 # Private values are deliberately not written in this public file; generic detectors live in tools/privacy_scan.py.
 for label,hit in scan_text(text,f):errors.append(f'{f.name}: private {label}')
for f in scans:
 if f.parent.name in {'pages','docs','review','dashboard'} and 'ARCHIVED RESEARCH' not in f.read_text():errors.append(f'{f}: no archive warning')
for base,pct,inc,total in [('3995','.016','63.92','4058.92'),('3150','.016','50.40','3200.40'),('3995','.030','119.85','4114.85'),('3150','.115','362.25','3512.25'),('3150','.131','412.65','3562.65')]:
 assert Decimal(base)*Decimal(pct)==Decimal(inc)
 assert Decimal(base)+Decimal(inc)==Decimal(total)
register=json.loads((ROOT/'audit/sources.json').read_text())
assert len(register)==13
print(f'Checked {len(scans)} HTML files for local links/anchors; {len(CANON)} canonical pages for official row sources; 5 decimal scenarios; archive labels; privacy patterns.')
if errors:
 print('\n'.join(errors));sys.exit(1)
print('PASS. External availability and legal eligibility are not certified by this test.')
