#!/usr/bin/env python3
"""Row-source audit of every published HTML page.

Run from the repository root:  python3 tools/row_source_audit.py   (DETAIL=1 lists every exception)

The project rule is that every table row carries a link to an official source, or is blank and
flagged. tools/verify_core_site.py enforces that for the canonical pages only. The preserved
editions were never counted consistently, so flag FR-24 once under-reported the gap (25 rows,
measured 276 on 11 Nov 2026). This script counts every table body row on every page and classifies
it by the links it carries:

    official  at least one link to a government or official-publisher host
    nonoff    external links, none of them official
    internal  only links inside this site
    none      no link at all

It fails when a canonical row lacks an official link, or when the number of such rows in the
preserved editions rises above the recorded baseline - so the figure published in FR-24 cannot
drift upwards unnoticed. It does not judge whether a linked page supports the claim in the row.
"""
import re, sys, os, glob, collections
from html.parser import HTMLParser
from urllib.parse import urlparse

OFFICIAL = ('sf.gov','www.sf.gov','media.api.sf.gov','sfgov.org','www.sfgov.org','portal.sfrb.org','www.sfrb.org','sfrb.org',
            'sfgov.legistar.com','codelibrary.amlegal.com','leginfo.legislature.ca.gov','oag.ca.gov','calcivilrights.ca.gov',
            'www.hud.gov','hud.gov','www.govinfo.gov','www.justice.gov','www.congress.gov','www.ecfr.gov','www.sec.gov',
            'sfplanninggis.org','www.sfassessor.org','www.bls.gov','www.opm.gov','opm.gov','www.courts.ca.gov','www.dir.ca.gov','contracostaha.org')
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.rows=[]; s.cur=None; s.intd=0; s.inth=0; s.table=0; s.caption=[]
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=='table': s.table+=1
        if t=='tr': s.cur={'links':[], 'text':[], 'td':0, 'th':0, 'cls':a.get('class','')}
        if s.cur is not None:
            if t=='td': s.cur['td']+=1
            if t=='th': s.cur['th']+=1
            if t=='a' and a.get('href'): s.cur['links'].append(a['href'])
    def handle_endtag(s,t):
        if t=='tr' and s.cur is not None:
            s.rows.append(s.cur); s.cur=None
        if t=='table': s.table-=1
    def handle_data(s,d):
        if s.cur is not None: s.cur['text'].append(d)
def classify(links):
    ext=[l for l in links if l.startswith('http')]
    if any(urlparse(l).netloc.lower() in OFFICIAL for l in ext): return 'official'
    if ext: return 'nonoff'
    if links: return 'internal'
    return 'none'
def audit(path):
    raw=open(path,encoding='utf-8').read()
    raw=re.sub(r'&(?=sectionNum=)','&amp;',raw)
    p=P(); p.feed(raw); out=[]
    for r in p.rows:
        if r['td']==0: continue   # header rows
        text=re.sub(r'\s+',' ',''.join(r['text'])).strip()
        out.append((classify(r['links']), text, r['links']))
    return out
PRESERVED = ('docs', 'dashboard', 'review', 'audit', 'verified', 'verification')
BASELINE_PRESERVED_UNSOURCED = 114   # measured 11 Nov 2026 after this pass; published in FR-24


def main():
    detail = os.environ.get('DETAIL')
    canon_bad = 0; preserved_bad = 0; preserved_rows = 0
    for ed in ('.', 'pages') + PRESERVED:
        files = ['index.html'] if ed == '.' else sorted(glob.glob(ed + '/**/*.html', recursive=True))
        c = collections.Counter(); bad = []
        for f in files:
            for kind, text, links in audit(f):
                c[kind] += 1
                if kind != 'official': bad.append((f, kind, text, links))
        n = sum(c.values())
        label = 'landing page' if ed == '.' else ed + '/'
        print(f"{label:14s} pages={len(files):2d} rows={n:4d} official={c['official']:4d} "
              f"nonoff={c['nonoff']:3d} internal={c['internal']:3d} none={c['none']:3d}")
        if ed in PRESERVED:
            preserved_bad += len(bad); preserved_rows += n
        else:
            canon_bad += len(bad)
        if detail or ed not in PRESERVED:
            for f, kind, text, links in bad:
                print(f"    [{kind:8s}] {f}: {text[:150]}")
    print(f"canonical rows without an official link: {canon_bad}")
    print(f"preserved-edition rows: {preserved_rows}; without an official link: {preserved_bad} "
          f"(baseline {BASELINE_PRESERVED_UNSOURCED})")
    if canon_bad:
        print('FAIL: a canonical row has no official source link'); return 1
    if preserved_bad > BASELINE_PRESERVED_UNSOURCED:
        print('FAIL: preserved editions have more unsourced rows than the published baseline'); return 1
    print('ROW-SOURCE AUDIT PASSED')
    return 0


if __name__ == '__main__':
    sys.exit(main())
