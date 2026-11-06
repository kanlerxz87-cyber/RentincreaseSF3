#!/usr/bin/env python3
"""Verification pass: internal links, table-row source links, PII scan."""
import re, sys, pathlib

root = pathlib.Path(__file__).parent
html_files = sorted(root.glob("*.html"))
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
        path = root / target
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
pii_patterns = {
    "tenant initials": r"\b[LMVJEI]\s+[ONPTSR]\b",
    "zip 94122": r"94122",
    "outer sunset": r"(?i)outer\s+sunset",
    "street-ish": r"(?i)\b\d{1,5}\s+[A-Z][a-z]+\s+(street|st|ave|avenue|blvd)\b",
}
for f in list(root.glob("*.html")) + [root / "README.md", root / "COORDINATION.md"]:
    if not f.exists():
        continue
    text = f.read_text(encoding="utf-8")
    for label, pat in pii_patterns.items():
        for m in re.finditer(pat, text):
            errors.append(f"{f.name}: PII risk [{label}]: {m.group(0)!r}")

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
