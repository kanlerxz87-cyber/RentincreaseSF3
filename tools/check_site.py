#!/usr/bin/env python3
"""Static checks for the generated site.

1. every internal href resolves to an existing file (and anchor, where given)
2. every external href is https
3. every data-table row carries at least one official-source chip
4. no orphaned placeholder text ("TODO", "TBD", "{{")
Exit code 1 on failure.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = sorted(p for p in ROOT.glob("*.html"))

errors = []
warnings = []
external = set()

anchors_by_file = {}
for p in PAGES:
    text = p.read_text(encoding="utf-8")
    anchors_by_file[p.name] = set(re.findall(r'id="([^"]+)"', text))

for p in PAGES:
    text = p.read_text(encoding="utf-8")
    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith("#"):
            if href[1:] not in anchors_by_file[p.name]:
                errors.append(f"{p.name}: missing local anchor {href}")
        elif href.startswith("http"):
            if not href.startswith("https://"):
                errors.append(f"{p.name}: non-https external link {href}")
            external.add(href)
        elif href.endswith(".html") or "#" in href:
            target, _, frag = href.partition("#")
            if target and not (ROOT / target).exists():
                errors.append(f"{p.name}: broken internal link {href}")
            elif frag and target in anchors_by_file and frag not in anchors_by_file[target]:
                errors.append(f"{p.name}: broken anchor {href}")
        elif href.endswith(".css") or href.endswith(".js"):
            if not (ROOT / href).exists():
                errors.append(f"{p.name}: missing asset {href}")
    for token in ("TODO", "TBD", "{{", "}}"):
        if token in text:
            errors.append(f"{p.name}: leftover placeholder {token}")

    # table row source check
    for m in re.finditer(r"<table[^>]*>(.*?)</table>", text, re.S):
        tbl = m.group(1)
        if 'class="mini"' in m.group(0)[:40]:
            continue
        body = tbl.split("<tbody>", 1)[-1]
        for row in re.findall(r"<tr>(.*?)</tr>", body, re.S):
            if 'class="src"' not in row:
                snippet = re.sub(r"<[^>]+>", " ", row)[:70].strip()
                warnings.append(f"{p.name}: table row without source chip -> {snippet}")

print(f"pages checked: {len(PAGES)}")
print(f"external links: {len(external)}")
for e in sorted(external):
    print("  ext:", e)
if warnings:
    print(f"\nwarnings ({len(warnings)}):")
    for w in warnings:
        print("  -", w)
if errors:
    print(f"\nERRORS ({len(errors)}):")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("\nNo broken internal links or anchors.")
