#!/usr/bin/env python3
"""Add (or refresh) a single link banner on the canonical root page pointing at site/.

The root site (index.html, pages/, assets/style.css) is owned by another session. This script
does NOT rewrite it. It inserts one self-contained block immediately after the <main id="main">
opening tag, delimited by markers, and is idempotent: running it twice leaves one banner.

Run from the repository root:  python3 tools/link_consolidated.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
START = "<!-- CONSOLIDATED-EDITION-LINK:start -->"
END = "<!-- CONSOLIDATED-EDITION-LINK:end -->"

BANNER = f"""{START}
<div style="max-width:1080px;margin:18px auto 0;padding:0 20px">
  <div style="border:1px solid #cfe0ef;border-left:4px solid #0b5d8f;background:#eef5fb;
              border-radius:10px;padding:14px 18px;font-size:.94rem;line-height:1.6">
    <strong>Second edition — consolidated review, verified 10 November 2026.</strong>
    Ten categorized pages covering the Rent Board licence and reporting steps, every lawful
    increase option for both units to the cent, the full 1982–2027 rate table, the notice
    requirements, the tenant-lawyer test, and a Flagged for review register.
    <a href="site/index.html"><strong>Open the consolidated review →</strong></a>
  </div>
</div>
{END}"""


def main() -> int:
    if not INDEX.exists():
        print("root index.html not found", file=sys.stderr)
        return 1
    text = INDEX.read_text(encoding="utf-8")
    # remove any previous banner
    text = re.sub(re.escape(START) + r".*?" + re.escape(END), "", text, flags=re.S)
    m = re.search(r'<main\b[^>]*>', text)
    if not m:
        print("no <main> element found; refusing to guess where to insert", file=sys.stderr)
        return 1
    at = m.end()
    text = text[:at] + "\n" + BANNER + text[at:]
    INDEX.write_text(text, encoding="utf-8")
    print(f"banner written to {INDEX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
