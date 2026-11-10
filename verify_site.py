#!/usr/bin/env python3
"""Verification pass: internal links, table-row source links, PII scan."""
import re, sys, pathlib

root = pathlib.Path(__file__).parent
site = root / "dashboard"
html_files = sorted(site.glob("*.html"))
errors = []
warnings = []

# 1) Internal link check + row-source check per file
row_re = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.S)
href_re = re.compile(r'href="([^"]+)"')

for f in html_files:
    text = f.read_text(encoding="utf-8")
    # internal hrefs
    for href in href_re.findall(text):
        if href.startswith(("http://", "https://", "mailto:", "tel:")):
            continue
        target, _, frag = href.partition("#")
        if target == "":
            if frag and f'id="{frag}"' not in text and f'name="{frag}"' not in text:
                errors.append(f"{f.name}: missing anchor #{frag}")
            continue
        path = f.parent / target
        if not path.exists():
            errors.append(f"{f.name}: broken internal link -> {href}")
        elif frag:
            t = path.read_text(encoding="utf-8")
            if f'id="{frag}"' not in t and f'name="{frag}"' not in t:
                errors.append(f"{f.name}: missing anchor {href}")
    # table rows (tbody rows only) must contain >=1 href
    for m in re.finditer(r"<tbody>(.*?)</tbody>", text, re.S):
        for row in row_re.findall(m.group(1)):
            if "<th" in row:
                continue
            if not href_re.search(row):
                errors.append(f"{f.name}: table row without any source link: {row[:80].strip()}...")

# 2) PII scan across all repo text files
# The private values themselves are deliberately NOT written here: this repository is public, so a
# scanner must not spell out what it protects. tools/privacy_scan.py holds generic detectors (any
# San Francisco postal code, any neighbourhood name, initials-style identifiers, street addresses).
sys.path.insert(0, str(root / "tools"))
from privacy_scan import scan_text  # noqa: E402

for f in list(site.glob("*.html")) + [root / "README.md", root / "COORDINATION.md"] + list(root.glob("pages/*.html")) + list(root.glob("docs/*.html")) + list(root.glob("review/*.html")):
    if not f.exists():
        continue
    text = f.read_text(encoding="utf-8")
    for label, hit in scan_text(text, f):
        errors.append(f"{f.name}: PII risk [{label}]: {hit!r}")

# 3) Math sanity checks
checks = [
    ("3995 * 1.016", round(3995 * 1.016, 2), 4058.92),
    ("3995 * 1.030", round(3995 * 1.030, 2), 4114.85),
    ("3150 * 1.131", round(3150 * 1.131, 2), 3562.65),
    ("1.8+0.7+2.3+3.6+1.7+1.4", round(1.8+0.7+2.3+3.6+1.7+1.4, 1), 11.5),
    ("11.5+1.6", round(11.5+1.6, 1), 13.1),
]
for label, got, want in checks:
    if got != want:
        errors.append(f"math: {label} = {got}, expected {want}")

print(f"checked {len(html_files)} html files")
if warnings:
    print("WARNINGS:")
    [print("  -", w) for w in warnings]
if errors:
    print("FAIL:")
    [print("  -", e) for e in errors]
    sys.exit(1)
print("ALL CHECKS PASSED")
