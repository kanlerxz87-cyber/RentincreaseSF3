#!/usr/bin/env python3
"""Verify the consolidated edition under site/ (final integration, 2026-11-10).

Run from the repository root:  python3 tools/verify_consolidated.py

Checks:
 1. every internal link resolves to a file that exists;
 2. every anchor (#id) resolves in the target page;
 3. every data row in every table carries at least one link to an OFFICIAL domain
    (a row with no official link is an ERROR, never a warning);
 4. every external link is https and points at an official domain or a documented exception;
 5. privacy sweep: no tenant initial, no street address, no ZIP code (94102, the Rent
    Board's own public office, is the only permitted 941xx), no neighbourhood name;
 6. no remote scripts, iframes or tracking;
 7. the cents-exact figures on the pages match the arithmetic;
 8. no leftover placeholder tokens.
Exit code 1 on any failure.
"""

from __future__ import annotations

import html
import re
import sys
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

OFFICIAL_HOSTS = {
    "sf.gov", "www.sf.gov", "media.api.sf.gov", "portal.sfrb.org", "sfgov.legistar.com",
    "leginfo.legislature.ca.gov", "oag.ca.gov", "calcivilrights.ca.gov", "govinfo.gov",
}

# The private values are not stored in this repository. Match them generically.
PRIVATE = [
    (r"\b941(?!02)\d{2}\b", "ZIP code"),
    (r"(?i)" + "outer" + r"\s+" + "sunset", "neighbourhood"),
    (r"(?i)" + "sunset" + r"\s+" + "district", "neighbourhood"),
    (r"\bL\.?\s?O\b(?!\w)", "possible tenant initials"),
    (r"\bV\.?\s?N\b(?!\w)", "possible tenant initials"),
    (r"\bJ\.?\s?P\b(?!\w)", "possible tenant initials"),
    (r"\bE\.?\s?R\b(?!\w)", "possible tenant initials"),
    (r"\bI\.?\s?S\b(?!\w)", "possible tenant initials"),
    (r"\bM\.?\s?T\b(?!\w)", "possible tenant initials"),
    (r"(?i)\b\d{1,5}\s+[A-Z][a-z]+\s+(street|st|ave|avenue|blvd|drive|way)\b", "street address"),
]

PLACEHOLDERS = ("TODO", "TBD", "{{", "}}", "FIXME", "lorem ipsum")

HREF = re.compile(r'href="([^"]+)"')
ID = re.compile(r'\bid="([^"]+)"')
ROW = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.S)


def host(u: str) -> str:
    h = urlsplit(u).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    htmls = sorted(SITE.glob("*.html"))
    if not htmls:
        print("FAIL: no pages built")
        return 1
    # The root landing page is generated from the same function and must satisfy the same rules.
    root_index = ROOT / "index.html"
    if not root_index.exists():
        errors.append("root index.html missing")
    pages = htmls + ([root_index] if root_index.exists() else [])

    ids = {p.name: set(ID.findall(p.read_text(encoding="utf-8"))) for p in pages}
    external: set[str] = set()
    rows_checked = 0

    for p in pages:
        raw = p.read_text(encoding="utf-8")
        # The model-notice block is illustrative letter content, not a data table: exclude it
        # from the per-row citation rule (it is cited as a whole, immediately below itself).
        text = re.sub(r'<div class="letter">.*?</div>', "", raw, flags=re.S)

        # 1 + 2 links and anchors
        for href in HREF.findall(text):
            href = html.unescape(href)
            if href.startswith(("mailto:", "tel:")):
                continue
            if href.startswith(("http://", "https://")):
                if not href.startswith("https://"):
                    errors.append(f"{p.name}: non-https external link {href}")
                elif host(href) not in OFFICIAL_HOSTS:
                    errors.append(f"{p.name}: non-official external domain {host(href)} -> {href}")
                external.add(href)
                continue
            target, _, frag = href.partition("#")
            if target:
                dest = (p.parent / target).resolve()
                if not dest.exists():
                    errors.append(f"{p.name}: broken internal link -> {href}")
                    continue
                if frag and dest.suffix == ".html" and frag not in ids.get(dest.name, set()):
                    errors.append(f"{p.name}: missing anchor #{frag} in {dest.name}")
            elif frag:  # same-page anchor
                if frag not in ids[p.name]:
                    errors.append(f"{p.name}: missing same-page anchor #{frag}")

        # 3 every data row must carry an official link
        for i, row in enumerate(ROW.findall(text), start=1):
            if "<th" in row:
                continue
            rows_checked += 1
            hrefs = [html.unescape(h) for h in HREF.findall(row)]
            if not any(host(h) in OFFICIAL_HOSTS for h in hrefs if h.startswith("https://")):
                snippet = re.sub(r"<[^>]+>", " ", row).strip()[:90]
                errors.append(f"{p.name}: data row without an official source link -> {snippet}")

        # 5 privacy (scan the full original file, including any excluded block)
        for pat, label in PRIVATE:
            for m in re.finditer(pat, raw):
                ctx = raw[max(0, m.start() - 45): m.end() + 45].replace("\n", " ")
                errors.append(f"{p.name}: {label} matched ({m.group(0)!r}): …{ctx}…")
        for pat, label in []:
            for m in re.finditer(pat, text):
                ctx = text[max(0, m.start() - 45): m.end() + 45].replace("\n", " ")
                errors.append(f"{p.name}: {label} matched ({m.group(0)!r}): …{ctx}…")

        # 6 remote code
        for bad in ("<script", "<iframe", "google-analytics", "src=\"http"):
            if bad in text:
                errors.append(f"{p.name}: remote or executable content ({bad})")

        # 8 placeholders
        for tok in PLACEHOLDERS:
            if tok in text:
                errors.append(f"{p.name}: leftover placeholder token {tok!r}")

    # 7 arithmetic present on the pages
    units = (SITE / "units.html").read_text(encoding="utf-8")
    expected = {
        "3995 single year": ("$63.92", "$4,058.92"),
        "3995 with banking": ("$119.85", "$4,114.85"),
        "3150 single year": ("$50.40", "$3,200.40"),
        "3150 11.7%": ("$368.55", "$3,518.55"),
        "3150 11.5%": ("$362.25", "$3,512.25"),
        "3150 13.1%": ("$412.65", "$3,562.65"),
        "3150 phased 10%": ("$315.00", "$3,465.00"),
    }
    for label, (inc, total) in expected.items():
        if inc not in units or total not in units:
            errors.append(f"units.html: expected {label} ({inc} / {total}) not found")

    # independent recomputation
    for base, rate, inc, total in [
        ("3995", ".016", "63.92", "4058.92"),
        ("3995", ".030", "119.85", "4114.85"),
        ("3150", ".016", "50.40", "3200.40"),
        ("3150", ".117", "368.55", "3518.55"),
        ("3150", ".115", "362.25", "3512.25"),
        ("3150", ".131", "412.65", "3562.65"),
        ("3150", ".100", "315.00", "3465.00"),
    ]:
        d = Decimal(base) * Decimal(rate)
        if d != Decimal(inc):
            errors.append(f"math: {base} × {rate} = {d}, page implies {inc}")
        if Decimal(base) + d != Decimal(total):
            errors.append(f"math: {base} + {inc} = {Decimal(base) + d}, page implies {total}")

    # structural completeness of the register pages
    flagged = (SITE / "flagged.html").read_text(encoding="utf-8")
    for n in range(1, 10):
        fid = f"f-{n:02d}"
        if f'id="{fid}"' not in flagged:
            errors.append(f"flagged.html: entry {fid} missing")
    sources = (SITE / "sources.html").read_text(encoding="utf-8")
    # every official URL that appears anywhere must appear in the source register
    # The register writes URLs into markup, so "&" is stored as "&amp;". Compare on the
    # normalised text, independent of which escaping the generator happened to use.
    sources_norm = sources.replace("&amp;", "&")
    for url in sorted(external):
        if url.replace("&amp;", "&") not in sources_norm:
            errors.append(f"sources.html: external link not listed in the register -> {url}")

    # every page must be reachable from the nav
    index = (SITE / "index.html").read_text(encoding="utf-8")
    for p in htmls:
        if p.name != "index.html" and p.name not in index:
            warnings.append(f"{p.name}: not linked from the dashboard")

    print(f"pages: {len(htmls)} | table rows checked: {rows_checked} | distinct external links: {len(external)}")
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
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
