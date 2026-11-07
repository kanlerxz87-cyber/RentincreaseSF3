#!/usr/bin/env python3
"""Pre-publish checks for the verified edition.

Run from the repository root:  python3 tools/verify_edition.py

Checks, in order:
 1. every internal link (href) points at a file that exists;
 2. every same-page or cross-page anchor (#id) resolves;
 3. every table row carries a citation: a link to an official domain, or an explicit
    blank / analysis / flag marker (reported as a warning for manual review otherwise);
 4. no row is left with no link and no marker at all (error);
 5. privacy sweep: tenant identifiers, street address and ZIP must not appear;
 6. no external scripts, iframes or tracking pixels (the site is fully static).
"""

from __future__ import annotations

import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent

# Pages produced by this edition. Other editions in the repository are checked for
# link integrity only, not for citations (they are marked superseded or are historical).
EDITION = [
    "verified/index.html",
    "verified/guide/executive-summary.html",
    "verified/guide/license-and-process.html",
    "verified/guide/units.html",
    "verified/guide/allowable-increases.html",
    "verified/guide/notice.html",
    "verified/guide/laws.html",
    "verified/guide/reasonable-and-normal.html",
    "verified/guide/flagged.html",
    "verified/guide/sources.html",
]

OFFICIAL_HOSTS = {
    "www.sf.gov",
    "sf.gov",
    "media.api.sf.gov",
    "sfgov.legistar.com",
    "portal.sfrb.org",
    "codelibrary.amlegal.com",
    "leginfo.legislature.ca.gov",
    "oag.ca.gov",
    "calcivilrights.ca.gov",
    "govinfo.gov",
    "justice.gov",
    "hud.gov",
    "sfplanninggis.org",
    "bls.gov",
    "dir.ca.gov",
}

PRIVATE_PATTERNS = [
    (r"\b94122\b", "ZIP code"),
    (r"(?i)outer\s+sunset", "neighbourhood"),
    (r"(?i)\bsunset\s+district\b", "neighbourhood"),
    (r"\bL\.?\s?O\b(?!\w)", "possible tenant initials"),
    (r"\bV\.?\s?N\b(?!\w)", "possible tenant initials"),
    (r"\bJ\.?\s?P\b(?!\w)", "possible tenant initials"),
    (r"\bE\.?\s?R\b(?!\w)", "possible tenant initials"),
    (r"\bI\.?\s?S\b(?!\w)", "possible tenant initials"),
    (r"\bM\.?\s?T\b(?!\w)", "possible tenant initials"),
]


class Doc(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.rows: list[list[tuple[str, str]]] = []  # per <tr>: list of (tag, href or text)
        self._row: list[tuple[str, str]] | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "name" in a:
            self.ids.add(a["name"])
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
            if self._row is not None:
                self._row.append(("a", a["href"]))
        if tag == "tr":
            self._row = []
        if tag in ("th", "td") and self._row is not None:
            self._row.append(("cell", tag))
        if self._row is not None:
            classes = (a.get("class") or "") + " "
            for c in classes.split():
                self._row.append(("class", c))

    def handle_endtag(self, tag):
        if tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None

    def handle_data(self, data):
        if self._row is not None and data.strip():
            self._row.append(("text", data.strip()))


def host_of(url: str) -> str:
    h = urlsplit(url).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    docs: dict[str, Doc] = {}
    for rel in EDITION:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing page: {rel}")
            continue
        d = Doc()
        d.feed(path.read_text(encoding="utf-8"))
        docs[rel] = d

    # 1 + 2 link and anchor integrity (edition pages and superseded pages alike)
    link_pages = EDITION + [
        "pages/executive-summary.html",
        "pages/flagged.html",
        "pages/laws.html",
        "pages/process.html",
        "pages/units.html",
    ]
    for rel in link_pages:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"]+)"', text):
            href = html.unescape(href)
            if href.startswith(("mailto:", "tel:", "http://", "https://", "//")):
                continue
            target, _, frag = href.partition("#")
            if target:
                dest = (path.parent / target).resolve()
                try:
                    dest.relative_to(ROOT)
                except ValueError:
                    errors.append(f"{rel}: link escapes repository: {href}")
                    continue
                if not dest.exists():
                    errors.append(f"{rel}: broken link -> {href}")
                    continue
            else:
                dest = path
            if frag and dest.exists():
                sub = Doc()
                sub.feed(dest.read_text(encoding="utf-8"))
                if frag not in sub.ids:
                    errors.append(f"{rel}: missing anchor #{frag} in {dest.relative_to(ROOT)}")

    # 3 + 4 citation coverage per table row
    for rel, d in docs.items():
        for i, row in enumerate(d.rows, start=1):
            if any(k == "cell" and v == "th" for k, v in row):
                continue  # header row
            hrefs = [v for k, v in row if k == "a"]
            classes = {v for k, v in row if k == "class"}
            text = " ".join(v for k, v in row if k == "text")
            official = [
                h
                for h in hrefs
                if h.startswith(("http://", "https://"))
                and host_of(h) in OFFICIAL_HOSTS
            ]
            marked = bool(classes & {"blank", "b-info", "b-warn", "b-blank", "b-stop", "b-record"}) or bool(
                re.search(r"\bF-\d+\b", text)
            )
            if official:
                continue
            if marked:
                warnings.append(f"{rel}: row {i} has no official link (blank/flag/analysis marker present)")
                continue
            if hrefs:
                warnings.append(f"{rel}: row {i} cites only an internal or non-official link: {hrefs}")
            else:
                errors.append(f"{rel}: row {i} has no link at all")

    # 5 privacy sweep over every page in the repository that this edition publishes
    for rel in EDITION:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern, label in PRIVATE_PATTERNS:
            for m in re.finditer(pattern, text):
                snippet = text[max(0, m.start() - 40) : m.end() + 40].replace("\n", " ")
                errors.append(f"{rel}: {label} matched ({m.group(0)!r}): …{snippet}…")

    # 6 no remote code
    for rel in EDITION:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for bad in ("<script", "<iframe", "src=\"http", "google-analytics"):
            if bad in text:
                errors.append(f"{rel}: remote or executable content found ({bad})")

    # 7 duplicate external URL sanity: no trailing-period leginfo links
    for rel in EDITION:
        path = ROOT / rel
        if not path.exists():
            continue
        for href in re.findall(r'href="([^"]+)"', path.read_text(encoding="utf-8")):
            if "leginfo.legislature.ca.gov" in href and re.search(r"sectionNum=\d+\.(?!\d)", href):
                errors.append(f"{rel}: leginfo link keeps a trailing period: {href}")

    print(f"pages checked: {len(docs)}")
    print(f"rows checked:  {sum(len(d.rows) for d in docs.values())}")
    if warnings:
        print(f"\n{len(warnings)} warning(s) for manual review:")
        for w in warnings:
            print("  ~", w)
    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print("  x", e)
        print("\nCHECKS FAILED")
        return 1
    print("\nALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
