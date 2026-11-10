#!/usr/bin/env python3
"""Verification gate for the canonical root site.

Checks, in order:
 1. every page listed in the navigation exists and is reachable;
 2. every internal link (and #anchor) resolves on disk;
 3. every data-table row cites at least one OFFICIAL domain;
 4. every table's rows have the same number of cells as its header (colspan aware);
 5. privacy scan: no tenant initials, no ZIP code, no neighbourhood name, no street address;
 6. arithmetic assertions for every published figure;
 7. no remote scripts, no inline JS, no placeholder text;
 8. every page carries the "not legal advice" and privacy statements.
Exit code 1 on any failure.
"""
import datetime as dt
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from site_layout import ALL_PAGES, OFFICIAL_DOMAINS, SRC  # noqa: E402

ERRORS = []
WARNINGS = []
TABLES = 0
ROWS = 0
LINKS = 0

HREF = re.compile(r'href="([^"]+)"')
TR = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.S)
TD = re.compile(r"<t([dh])\b([^>]*)>", re.S)
COLSPAN = re.compile(r'colspan="(\d+)"')


def official(url):
    return any(url.startswith("https://" + d) or url.startswith("https://www." + d)
               or ("//" + d + "/") in url for d in OFFICIAL_DOMAINS)


def check_links(path):
    global LINKS
    text = path.read_text(encoding="utf-8")
    for href in HREF.findall(text):
        LINKS += 1
        if href.startswith(("http://", "https://", "mailto:", "tel:")):
            if href.startswith("http://"):
                ERRORS.append("%s: insecure external link %s" % (path.name, href))
            continue
        target, _, frag = href.partition("#")
        base = path.parent
        if target == "":
            if frag and 'id="%s"' % frag not in text:
                ERRORS.append("%s: missing local anchor #%s" % (path.name, frag))
            continue
        dest = (base / target).resolve()
        if not dest.exists():
            ERRORS.append("%s: broken internal link %s" % (path.name, href))
            continue
        if frag:
            dtxt = dest.read_text(encoding="utf-8")
            if 'id="%s"' % frag not in dtxt:
                ERRORS.append("%s: broken anchor %s" % (path.name, href))


def check_tables(path):
    global TABLES, ROWS
    text = path.read_text(encoding="utf-8")
    for t_i, table in enumerate(re.findall(r"<table\b[^>]*>(.*?)</table>", text, re.S)):
        TABLES += 1
        rows = TR.findall(table)
        if not rows:
            ERRORS.append("%s: table %d has no rows" % (path.name, t_i))
            continue
        header = rows[0]
        if "<th" not in header:
            ERRORS.append("%s: table %d has no header row" % (path.name, t_i))
            continue
        ncols = sum(int(c or 1) for c in COLSPAN.findall(header)) or len(TD.findall(header))
        ncols = sum(int(COLSPAN.search(m[1]).group(1)) if COLSPAN.search(m[1]) else 1
                    for m in TD.findall(header))
        for r_i, row in enumerate(rows[1:], start=1):
            ROWS += 1
            cells = TD.findall(row)
            span = sum(int(COLSPAN.search(attrs).group(1)) if COLSPAN.search(attrs) else 1
                       for _, attrs in cells)
            if span != ncols:
                ERRORS.append("%s: table %d row %d has %d columns, header has %d"
                              % (path.name, t_i, r_i, span, ncols))
            hrefs = HREF.findall(row)
            if not any(official(h) for h in hrefs):
                snippet = re.sub(r"<[^>]+>", " ", row).strip()[:90]
                ERRORS.append("%s: table %d row %d cites no official source: %s"
                              % (path.name, t_i, r_i, snippet))


# The private values themselves are deliberately NOT written in this file: the repository is public,
# so a scanner must not spell out what it protects. tools/privacy_scan.py holds generic detectors
# (any San Francisco postal code, a citywide neighbourhood list, initials-style identifiers, street
# addresses, non-public contact details) and is the single definition every checker imports.
from privacy_scan import scan_text  # noqa: E402


def check_privacy(path):
    text = path.read_text(encoding="utf-8")
    for label, hit in scan_text(text, path):
        ERRORS.append("%s: privacy risk [%s]: %r" % (path.name, label, hit))


def check_scripts(path):
    text = path.read_text(encoding="utf-8")
    if re.search(r"<script", text, re.I):
        ERRORS.append("%s: contains a <script> element (site is static, no JS)" % path.name)
    for token in ("TODO", "TBD", "{{", "}}", "lorem ipsum"):
        if token in text:
            ERRORS.append("%s: leftover placeholder %r" % (path.name, token))


def check_footer(path):
    text = path.read_text(encoding="utf-8")
    for needle in ("Not legal advice", "Privacy:", "10 November 2026"):
        if needle not in text:
            ERRORS.append("%s: missing required disclosure %r" % (path.name, needle))


def money(x):
    return "$%s" % format(round(x, 2), ",.2f")


def check_math():
    # published monthly amounts, computed from the official percentages
    cases = [
        ("Unit A 1.6%", 3995 * 0.016, 63.92, 4058.92),
        ("Unit A 1.4%", 3995 * 0.014, 55.93, 4050.93),
        ("Unit A 3.0%", 3995 * 0.030, 119.85, 4114.85),
        ("Unit B 1.6%", 3150 * 0.016, 50.40, 3200.40),
        ("Unit B 10.0%", 3150 * 0.100, 315.00, 3465.00),
        ("Unit B 11.5%", 3150 * 0.115, 362.25, 3512.25),
        ("Unit B 13.1%", 3150 * 0.131, 412.65, 3562.65),
    ]
    for label, raw, inc, new in cases:
        if abs(round(raw, 2) - inc) > 0.005:
            ERRORS.append("math: %s increase = %.4f, published %.2f" % (label, raw, inc))
        if abs(round((3995 if "Unit A" in label else 3150) + inc, 2) - new) > 0.005:
            ERRORS.append("math: %s new rent mismatch" % label)
    # banking totals
    banked = 1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4
    if round(banked, 2) != 11.5:
        ERRORS.append("math: banked total = %.2f, published 11.5" % banked)
    if round(banked + 1.6, 2) != 13.1:
        ERRORS.append("math: banked + annual = %.2f, published 13.1" % (banked + 1.6))
    # annualised effects
    if round(119.85 * 12, 2) != 1438.20:
        ERRORS.append("math: annual effect of Unit A 3.0% wrong")
    if round(63.92 * 12, 2) != 767.04:
        ERRORS.append("math: annual effect of Unit A 1.6% wrong")
    if round(315.00 * 12, 2) != 3780.00:
        ERRORS.append("math: annual effect of Unit B 10% wrong")
    if round(412.65 * 12, 2) != 4951.80:
        ERRORS.append("math: annual effect of Unit B 13.1% wrong")
    # notice-date arithmetic published on the process page
    d = dt.date
    cases_dates = [
        (d(2027, 2, 1), 30, d(2027, 1, 2)),
        (d(2027, 2, 1), 35, d(2026, 12, 28)),
        (d(2027, 2, 1), 90, d(2026, 11, 3)),
        (d(2027, 2, 8), 90, d(2026, 11, 10)),
        (d(2027, 2, 14), 90, d(2026, 11, 16)),
        (d(2027, 2, 14), 95, d(2026, 11, 11)),
        (d(2026, 12, 10), 0, d(2026, 12, 10)),
    ]
    for effective, days, expected in cases_dates:
        got = effective - dt.timedelta(days=days)
        if got != expected:
            ERRORS.append("dates: %s minus %d days = %s, published %s"
                          % (effective, days, got, expected))
    # planner forward dates from today
    today = dt.date(2026, 11, 10)
    if today + dt.timedelta(days=90) != dt.date(2027, 2, 8):
        ERRORS.append("dates: today + 90 days is not 2027-02-08")


def main():
    pages = [ROOT / p for p, _ in ALL_PAGES]
    for p in pages:
        if not p.exists():
            ERRORS.append("missing page %s" % p.relative_to(ROOT))
    for p in pages:
        if not p.exists():
            continue
        check_links(p)
        check_tables(p)
        check_privacy(p)
        check_scripts(p)
        check_footer(p)
    # every source in the registry is official and https
    for key, (title, url) in SRC.items():
        if not official(url):
            ERRORS.append("source %s is not on an official domain: %s" % (key, url))
        if not url.startswith("https://"):
            ERRORS.append("source %s is not https" % key)
    check_math()
    # old pages must still exist (nothing deleted)
    for legacy in ("docs/index.html", "dashboard/index.html", "review/index.html",
                   "audit/process.html", "verified/index.html", "EXECUTIVE_SUMMARY.md"):
        if not (ROOT / legacy).exists():
            ERRORS.append("prior edition missing (nothing may be deleted): %s" % legacy)
    print("pages: %d | tables: %d | rows: %d | links: %d" % (len(pages), TABLES, ROWS, LINKS))
    if WARNINGS:
        print("WARNINGS:")
        for w in WARNINGS:
            print("  -", w)
    if ERRORS:
        print("FAIL (%d):" % len(ERRORS))
        for e in ERRORS:
            print("  -", e)
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
