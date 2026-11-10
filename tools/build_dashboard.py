#!/usr/bin/env python3
"""Build the canonical root site (index.html + pages/*.html + assets/style.css).

The generator is deterministic and idempotent; running it twice produces the same
files. Content lives in the sibling modules so that the verification script can
inspect the same data structures.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from site_layout import CSS, ALL_PAGES  # noqa: E402
import site_pages_core as core  # noqa: E402
import site_pages_rules as rules  # noqa: E402
import site_pages_ref as ref  # noqa: E402

PAGES = {
    "index.html": core.index,
    "pages/executive-summary.html": core.executive_summary,
    "pages/process.html": core.process,
    "pages/units.html": core.units,
    "pages/laws.html": rules.laws,
    "pages/reasonable.html": rules.reasonable,
    "pages/practice.html": rules.practice,
    "pages/notice.html": rules.notice,
    "pages/review.html": rules.review,
    "pages/discrimination.html": rules.discrimination,
    "pages/requirements.html": ref.requirements,
    "pages/sources.html": ref.sources,
    "pages/flagged.html": ref.flagged,
}


def main():
    written = []
    css_path = ROOT / "assets" / "style.css"
    css_path.write_text(CSS, encoding="utf-8")
    written.append(("assets/style.css", len(CSS)))
    for rel, fn in PAGES.items():
        html = fn()
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        written.append((rel, len(html)))
    print("built %d files" % len(written))
    for rel, size in written:
        print("  %-38s %7d bytes" % (rel, size))
    missing = [p for p, _ in ALL_PAGES if not (ROOT / p).exists()]
    if missing:
        print("MISSING PAGES:", missing)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
