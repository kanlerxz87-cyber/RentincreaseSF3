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
import html
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from site_layout import ALL_PAGES, OFFICIAL_DOMAINS, SRC  # noqa: E402
from site_pages_ref import USED_FOR  # noqa: E402

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
    # The preserved verification edition keeps its own 10 Nov 2026 research-pass date;
    # the canonical pages were re-verified on 13 Nov 2026.
    date_needle = "10 November 2026" if "verification" in path.parts else "13 November 2026"
    for needle in ("Not legal advice", "Privacy:", date_needle):
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
        # rows added for the 13 Nov 2026 research pass
        (d(2027, 2, 11), 90, d(2026, 11, 13)),
        (d(2027, 2, 11), 95, d(2026, 11, 8)),
        (d(2027, 2, 16), 90, d(2026, 11, 18)),
        (d(2027, 2, 16), 95, d(2026, 11, 13)),
        (d(2026, 12, 10), 0, d(2026, 12, 10)),
    ]
    for effective, days, expected in cases_dates:
        got = effective - dt.timedelta(days=days)
        if got != expected:
            ERRORS.append("dates: %s minus %d days = %s, published %s"
                          % (effective, days, got, expected))
    # Historical example, not a rolling current-date calculation.
    example_service = dt.date(2026, 11, 10)
    if example_service + dt.timedelta(days=90) != dt.date(2027, 2, 8):
        ERRORS.append("dates: historical service example is not 2027-02-08")



# ---------------------------------------------------------------------------
# Official transcriptions that must be reproduced exactly on the site.
# Each list is copied from the linked Rent Board document and re-typed by hand
# only from that PDF; if the generator drifts the build fails (FR-26).
# ---------------------------------------------------------------------------
OFFICIAL_RATES = [  # document 571, "Allowable Annual Rent Increases", in published order
    ("3/1/26 – 2/28/27", "1.6%"), ("3/1/25 – 2/28/26", "1.4%"),
    ("3/1/24 – 2/28/25", "1.7%"), ("3/1/23 – 2/29/24", "3.6%"),
    ("3/1/22 – 2/28/23", "2.3%"), ("3/1/21 – 2/28/22", "0.7%"),
    ("3/1/20 – 2/28/21", "1.8%"), ("3/1/19 – 2/29/20", "2.6%"),
    ("3/1/18 – 2/28/19", "1.6%"), ("3/1/17 – 2/28/18", "2.2%"),
    ("3/1/16 – 2/28/17", "1.6%"), ("3/1/15 – 2/29/16", "1.9%"),
    ("3/1/14 – 2/28/15", "1.0%"), ("3/1/13 – 2/28/14", "1.9%"),
    ("3/1/12 – 2/28/13", "1.9%"), ("3/1/11 – 2/29/12", "0.5%"),
    ("3/1/10 – 2/28/11", "0.1%"), ("3/1/09 – 2/28/10", "2.2%"),
    ("3/1/08 – 2/28/09", "2.0%"), ("3/1/07 – 2/29/08", "1.5%"),
    ("3/1/06 – 2/28/07", "1.7%"), ("3/1/05 – 2/28/06", "1.2%"),
    ("3/1/04 – 2/28/05", "0.6%"), ("3/1/03 – 2/29/04", "0.8%"),
    ("3/1/02 – 2/28/03", "2.7%"), ("3/1/01 – 2/28/02", "2.8%"),
    ("3/1/00 – 2/28/01", "2.9%"), ("3/1/99 – 2/29/00", "1.7%"),
    ("3/1/98 – 2/28/99", "2.2%"), ("3/1/97 – 2/28/98", "1.8%"),
    ("3/1/96 – 2/28/97", "1.0%"), ("3/1/95 – 2/29/96", "1.1%"),
    ("3/1/94 – 2/28/95", "1.3%"), ("3/1/93 – 2/28/94", "1.9%"),
    ("12/8/92 – 2/28/93", "1.6%"), ("3/1/92 – 12/7/92", "4.0%"),
    ("3/1/91 – 2/29/92", "4.0%"), ("3/1/90 – 2/28/91", "4.0%"),
    ("3/1/89 – 2/28/90", "4.0%"), ("3/1/88 – 2/28/89", "4.0%"),
    ("3/1/87 – 2/29/88", "4.0%"), ("3/1/86 – 2/28/87", "4.0%"),
    ("3/1/85 – 2/28/86", "4.0%"), ("3/1/84 – 2/28/85", "4.0%"),
    ("3/1/83 – 2/29/84", "7.0%"), ("4/1/82 – 2/28/83", "7.0%"),
]


def check_rate_table():
    path = ROOT / "pages" / "laws.html"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    found = []
    for tr in re.findall(r"<tr>(.*?)</tr>", text, re.S):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                 for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)]
        if cells and re.match(r"^\d+/\d+/\d\d", cells[0]):
            found.append((cells[0], cells[1].replace(" in force now", "").strip()))
    if len(found) != len(OFFICIAL_RATES):
        ERRORS.append("rate table: %d rows published, document 571 has %d"
                      % (len(found), len(OFFICIAL_RATES)))
    for i, (want, got) in enumerate(zip(OFFICIAL_RATES, found), start=1):
        if want != got:
            ERRORS.append("rate table row %d: published %r, document 571 %r" % (i, got, want))
RESEARCH_DATE = dt.date(2026, 11, 13)
MONTHS = {m: i + 1 for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}
PLANNER_DATE = re.compile(r"(\d{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{4})")


def check_planner_freshness(path):
    """Every notice-date planner deadline that has already gone by on the research-pass
    date must be marked "passed" in the published cell, so a stale deadline can never be
    read as still open."""
    if path.name != "process.html":
        return
    text = path.read_text(encoding="utf-8")
    start = text.find("Notice-date planner")
    if start < 0:
        ERRORS.append("process.html: notice-date planner not found")
        return
    end = text.find("</table>", start)
    block = text[start:end if end > 0 else len(text)]
    checked = 0
    for row in TR.findall(block):
        cells = re.findall(r"<td\b[^>]*>(.*?)</td>", row, re.S)
        for cell in cells[1:]:
            for day, mon, year in PLANNER_DATE.findall(cell):
                when = dt.date(int(year), MONTHS[mon], int(day))
                checked += 1
                if when < RESEARCH_DATE and "passed" not in cell:
                    ERRORS.append("process.html: planner deadline %s is before the "
                                  "research-pass date %s but is not marked passed: %s"
                                  % (when, RESEARCH_DATE, re.sub(r"<[^>]+>", "", cell).strip()))
                elif when == RESEARCH_DATE and not any(
                        note in cell for note in ("passed", "holiday", "research-pass")):
                    ERRORS.append("process.html: planner deadline %s falls on the research-pass "
                                  "date itself and must be annotated (passed / holiday / "
                                  "research-pass): %s"
                                  % (when, re.sub(r"<[^>]+>", "", cell).strip()))
    if checked < 5:
        ERRORS.append("process.html: expected at least 5 planner deadlines, found %d" % checked)


def check_rate_calendar():
    """The published periods must be real, contiguous, descending calendar ranges.

    Row-by-row comparison against a transcription cannot catch a transcription error:
    `3/1/84 – 2/29/85` was once written into both the table and OFFICIAL_RATES, and the
    gate passed because both copies were wrong. 29 February 1985 does not exist, so
    parsing the dates rejects that class of mistake outright.
    """
    from site_pages_rules import RATES  # noqa: E402

    def parse(token):
        month, day, year = token.split("/")
        year = int(year)
        year += 2000 if year <= 30 else 1900
        return dt.date(year, int(month), int(day))

    parsed = []
    complete = True
    for period, _pct, _now in RATES:
        try:
            start_s, end_s = [t.strip() for t in period.split("\u2013")]
            start, end = parse(start_s), parse(end_s)
        except Exception:
            ERRORS.append("rate table: %r is not a real calendar period" % period)
            complete = False
            continue
        if end <= start:
            ERRORS.append("rate table: period %r ends before it starts" % period)
        parsed.append((period, start, end))
    if not complete:
        return  # pairing a skipped period would report a false gap
    for (p_hi, s_hi, _e_hi), (p_lo, s_lo, e_lo) in zip(parsed, parsed[1:]):
        if not s_hi > s_lo or e_lo + dt.timedelta(days=1) != s_hi:
            ERRORS.append("rate table: gap or overlap between %r and %r" % (p_hi, p_lo))


def check_decision_pages():
    """The two decision-support pages must keep their structure and their honesty rules."""
    sys.path.insert(0, str(HERE))
    from site_pages_decide import (BLOCKERS, ANSWERED, GAPS, SUGGESTIONS_LAW,
                                   BUNDLE_PATHS, DONE_THIS_PASS)
    ids = [row[0] for row in BLOCKERS] + [row[0] for row in ANSWERED]
    if len(set(x for x in ids if str(x).startswith("Q"))) != len([x for x in ids if str(x).startswith("Q")]):
        ERRORS.append("questions page: duplicate question ID")
    sug_ids = [row[0] for row in SUGGESTIONS_LAW]
    if len(set(sug_ids)) != len(sug_ids):
        ERRORS.append("suggestions page: duplicate proposal ID")
    for key, (title, url) in SRC.items():
        if key not in USED_FOR:
            ERRORS.append("source %s has no register description (renders an empty cell)" % key)
        if not title or not url:
            ERRORS.append("source %s is missing a title or url" % key)
    for q, why, flag, key in GAPS:
        if not str(flag).startswith("FR-"):
            ERRORS.append("questions page: unanswerable row %r must point at a flag ID" % q[:40])
        if key not in SRC:
            ERRORS.append("questions page: unanswerable row %r cites an unknown source" % q[:40])
    for page_name, needles in (
            ("questions.html", ("Open questions", "blocking", "Blank", "1942.4", "business registration")),
            ("suggestions.html", ("Improvement proposals", "Proposed", "Bundle paths",
                                  "Already changed this pass"))):
        text = (ROOT / "pages" / page_name).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                ERRORS.append("%s: required content %r is missing" % (page_name, needle))
    text = (ROOT / "pages" / "suggestions.html").read_text(encoding="utf-8")
    if ">%d</div>" % len(BUNDLE_PATHS) not in text and len(BUNDLE_PATHS) != 0:
        if "Bundle paths" in text and "<th>Contains</th>" not in text:
            ERRORS.append("suggestions.html: bundle-path table header is missing")
    if text.count("<td class=\"nowrap\">13 Nov 2026</td>") != len(DONE_THIS_PASS):
        ERRORS.append("suggestions.html: change rows (%d) are not len(DONE_THIS_PASS)=%d"
                      % (text.count("<td class=\"nowrap\">13 Nov 2026</td>"), len(DONE_THIS_PASS)))


def check_flag_order():
    """Flag IDs are reviewed top to bottom; they must be unique and in ascending order."""
    text = (ROOT / "pages" / "flagged.html").read_text(encoding="utf-8")
    ids = re.findall(r"<b>(FR-\d{2})</b>", text)
    if not ids:
        ERRORS.append("flagged page: no flag IDs found")
        return
    numbers = [int(i.split("-")[1]) for i in ids]
    if numbers != sorted(numbers):
        ERRORS.append("flagged page: flag IDs are not in ascending order")
    if len(set(numbers)) != len(numbers):
        ERRORS.append("flagged page: duplicate flag ID")


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
        check_planner_freshness(p)
    # every source in the registry is official and https
    for key, (title, url) in SRC.items():
        if not official(url):
            ERRORS.append("source %s is not on an official domain: %s" % (key, url))
        if not url.startswith("https://"):
            ERRORS.append("source %s is not https" % key)
    check_math()
    check_rate_table()
    check_rate_calendar()
    check_flag_order()
    check_decision_pages()
    # the flag count is dynamic on the pages; every place it is written as a literal must agree
    from site_pages_ref import FLAGS as FLAG_LIST
    n_flags = len(FLAG_LIST)
    for path, needle in (
            (ROOT / "pages" / "requirements.html", '<div class="num">%d</div>' % n_flags),
            (ROOT / "pages" / "flagged.html", "The %d flags" % n_flags),
            (ROOT / "pages" / "flagged.html", "%d items that are unverified" % n_flags),
            (ROOT / "pages" / "requirements.html", "%d flags published" % n_flags),
            (ROOT / "README.md", "%d flagged items" % n_flags)):
        if not path.exists():
            continue
        if needle not in path.read_text(encoding="utf-8"):
            ERRORS.append("%s: hardcoded flag count does not match FLAGS (%d) — expected %r"
                          % (path.name, n_flags, needle))
    # Guard against previously published unsafe legal assurances.
    canonical = "\n".join(p.read_text(encoding="utf-8") for p in pages if p.exists())
    for unsafe in ("first date reachable from today", "served now cannot take effect before",
                   "never against a co-tenant", "Checks that pass on documents",
                   "the only standard an official reviewer can test", "Smallest lawful step"):
        if unsafe in canonical:
            ERRORS.append("unsafe or stale assurance found: " + unsafe)
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
