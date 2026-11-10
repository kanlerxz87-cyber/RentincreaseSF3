#!/usr/bin/env python3
"""Pre-publish checks for the 2026-11-10 dashboard edition.

Failure (exit 1) conditions
  1. an internal link or anchor does not resolve;
  2. an external link is not https;
  3. a data row has neither an official source link nor an explicit flag marker;
  4. banned identifiers appear (tenant names/initials, street address, ZIP,
     neighbourhood name, unit labels that reveal location);
  5. a computed figure on the site disagrees with the recomputed value;
  6. a leftover placeholder token is present.

Run from the repository root:  python3 tools/check_v2.py
"""
from __future__ import annotations

import html as htmlmod
import re
import sys
from decimal import Decimal as D
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent

NEW_PAGES = [
    f"verification/{n}" for n in sorted(p.name for p in (ROOT / "verification").glob("*.html"))
]

OFFICIAL_HOSTS = {
    "www.sf.gov", "sf.gov", "leginfo.legislature.ca.gov", "govinfo.gov",
    "oag.ca.gov", "sfgov.legistar.com", "codelibrary.amlegal.com",
    "portal.sfrb.org", "calcivilrights.ca.gov", "hud.gov", "www.hud.gov",
    "www.govinfo.gov",
}

# Structural identifiers only. The personal-data detectors (postal codes, neighbourhood names,
# initials, street addresses, contact details) live in tools/privacy_scan.py and are imported so that
# this repository never spells out the values it is protecting — see that file's docstring.
sys.path.insert(0, str(ROOT / "tools"))
from privacy_scan import scan_text  # noqa: E402

BANNED = [
    (r"(?i)\b(?:apt|apartment|suite|ste)\.?\s*#?\s?[0-9]{1,4}\b", "unit number"),
    (r"\bunit\s+#?\s?[0-9]{1,3}\b", "unit number"),
]

PLACEHOLDERS = ["TODO", "TBD", "{{", "}}", "lorem ipsum"]


class Doc(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.rows: list[dict] = []
        self._row: dict | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("name"):
            self.ids.add(a["name"])
        if tag in ("a", "link") and a.get("href"):
            self.links.append(a["href"])
            if self._row is not None and tag == "a":
                self._row["hrefs"].append(a["href"])
        if tag == "tr":
            self._row = {"hrefs": [], "classes": set(), "has_th": False, "text": []}
        if self._row is not None:
            self._row["classes"].update((a.get("class") or "").split())
            if tag == "th":
                self._row["has_th"] = True
        if self._row is not None and tag in ("td", "th"):
            self._row["text"].append("")

    def handle_endtag(self, tag):
        if tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None

    def handle_data(self, data):
        if self._row is not None and data.strip():
            self._row["text"].append(data.strip())


def host(url: str) -> str:
    return urlsplit(url).netloc.lower()


def is_official(url: str) -> bool:
    return url.startswith("https://") and host(url) in OFFICIAL_HOSTS


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    docs: dict[str, Doc] = {}
    for rel in NEW_PAGES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing page: {rel}")
            continue
        d = Doc()
        d.feed(path.read_text(encoding="utf-8"))
        docs[rel] = d

    # 1 + 2: links, anchors, https
    for rel, d in docs.items():
        path = ROOT / rel
        for href in d.links:
            href = htmlmod.unescape(href)
            if href.startswith(("mailto:", "tel:", "#")):
                continue
            if href.startswith(("http://", "https://", "//")):
                if not href.startswith("https://"):
                    errors.append(f"{rel}: non-https external link {href}")
                continue
            target, _, frag = href.partition("#")
            dest = (path.parent / unquote(target)).resolve() if target else path.resolve()
            if not dest.exists():
                errors.append(f"{rel}: broken link -> {href}")
                continue
            if frag:
                key = str(dest.relative_to(ROOT))
                if key in docs:
                    if frag not in docs[key].ids:
                        errors.append(f"{rel}: missing anchor #{frag} in {key}")
                else:
                    sub = Doc()
                    sub.feed(dest.read_text(encoding="utf-8"))
                    if frag not in sub.ids:
                        errors.append(f"{rel}: missing anchor #{frag} in {key}")

    # 3: every data row sourced or flagged
    total_rows = sourced = flagged = 0
    for rel, d in docs.items():
        for i, row in enumerate(d.rows, start=1):
            if row["has_th"]:
                continue
            total_rows += 1
            official = [h for h in row["hrefs"] if is_official(h)]
            text = " ".join(row["text"])
            marked = "flag" in row["classes"] or "blank" in row["classes"] or bool(re.search(r"\bF-\d+\b", text))
            if official:
                sourced += 1
            elif marked:
                flagged += 1
            else:
                errors.append(f"{rel}: row {i} has neither an official source nor a flag marker -> {text[:70]}")

    # 4: identifiers — structural patterns here, personal data via the shared sweep
    for rel, d in docs.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        for pattern, label in BANNED:
            for m in re.finditer(pattern, text):
                errors.append(f"{rel}: banned {label}: {m.group(0)!r}")
        for label, found in scan_text(text, path):
            errors.append(f"{rel}: privacy sweep flagged {label}: {found!r}")

    # 5: recomputed figures must appear exactly as computed
    def money(x: D) -> str:
        return f"${x:,.2f}"

    u1, u2 = D("3995.00"), D("3150.00")
    expect = {
        "verification/index.html": [money((u1 * D("0.030")).quantize(D("0.01"))), money(u1 + (u1 * D("0.030")).quantize(D("0.01")))],
        "verification/units.html": [money((u2 * D("0.131")).quantize(D("0.01"))), money(u2 + (u2 * D("0.131")).quantize(D("0.01")))],
        "verification/executive-summary.html": [money((u2 * D("0.100")).quantize(D("0.01"))), money((u1 * D("0.016")).quantize(D("0.01")))],
    }
    for rel, values in expect.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for v in values:
            if v not in text:
                errors.append(f"{rel}: expected computed figure {v} not found")

    # 6: placeholders
    for rel in NEW_PAGES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for token in PLACEHOLDERS:
            if token.lower() in text.lower():
                errors.append(f"{rel}: leftover placeholder {token!r}")

    # 7: required structure
    for rel, d in docs.items():
        if "main" not in d.ids:
            errors.append(f"{rel}: missing #main landmark")
        if 'lang="en"' not in (ROOT / rel).read_text(encoding="utf-8"):
            errors.append(f"{rel}: missing lang attribute")

    print(f"pages checked:            {len(docs)}")
    print(f"data rows checked:        {total_rows}")
    print(f"  with official source:   {sourced}")
    print(f"  blank + flagged:        {flagged}")
    print(f"official hosts accepted:  {len(OFFICIAL_HOSTS)}")
    if warnings:
        print(f"\nwarnings ({len(warnings)}):")
        for w in warnings:
            print("  -", w)
    if errors:
        print(f"\nFAILURES ({len(errors)}):")
        for e in errors:
            print("  -", e)
        return 1
    print("\nALL CHECKS PASSED — every data row is sourced or flagged, all links resolve, no identifiers present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
