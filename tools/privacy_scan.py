#!/usr/bin/env python3
"""Repository-wide privacy sweep that does not contain any private value itself.

Run from the repository root:  python3 tools/privacy_scan.py

Why this file exists
--------------------
This repository is public. Earlier scanners spelled out the very strings they were meant to keep
out of it (the withheld postal code, the neighbourhood name and the occupants' initials), and they
only scanned selected HTML pages - never themselves, the generators or the data files. A scanner in
a public repository must not name what it protects, so this one uses *generic* detectors only:

 1. any San Francisco postal code (941xx) other than a short allow-list of public offices;
 2. any San Francisco neighbourhood or district name, from a citywide list (the list covers the
    whole city, so it says nothing about which neighbourhood is withheld);
 3. initials-style identifiers: two single capital letters separated by a space, dotted initials,
    or a two-capital token straight after "Tenant(s):";
 4. street addresses (number + street name + street type) other than public offices;
 5. e-mail addresses and telephone numbers other than published public-office contacts.

Every tracked text file is scanned - tools, data and this file included. People are referred to
only by placeholder labels (Tenant A-F, Unit 1 / Unit 2). Dates and dollar amounts are not private
and are never flagged.

Other scripts import ``scan_text`` so that there is exactly one definition of "private".
Exit code 1 when anything is found.
"""

from __future__ import annotations

import re
import subprocess
import sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()

# --- 1. postal codes ---------------------------------------------------------------------------
# Public offices whose published addresses legitimately appear on the site.
PUBLIC_OFFICE_ZIPS = {
    "94102",  # San Francisco Rent Board, 25 Van Ness Avenue (public office address)
}
ZIP_RE = re.compile(r"(?<![\d.])941\d{2}(?![\d])")

# --- 2. neighbourhood / district names (citywide list; reveals nothing) -------------------------
_PREFIXED = [
    " ".join(p)
    for p in product(
        ("inner", "outer", "central", "lower", "upper"),
        ("sunset", "richmond", "parkside", "mission", "haight"),
    )
]
_DISTRICTS = [
    f"{name} district"
    for name in (
        "sunset", "richmond", "marina", "mission", "castro", "excelsior", "bayview", "parkside",
        "ingleside", "portola", "haight", "tenderloin", "financial",
    )
]
_NAMED = [
    "noe valley", "bernal heights", "visitacion valley", "hunters point", "potrero hill", "dogpatch",
    "south of market", "nob hill", "russian hill", "north beach", "telegraph hill", "pacific heights",
    "presidio heights", "laurel heights", "cow hollow", "haight-ashbury", "cole valley", "glen park",
    "west portal", "forest hill", "twin peaks", "western addition", "hayes valley", "japantown",
    "mission bay", "mission dolores", "crocker-amazon", "sea cliff", "diamond heights",
    "golden gate heights", "lake merced", "merced heights", "st. francis wood", "sunnyside",
    "miraloma", "stonestown", "lakeshore", "oceanview", "balboa terrace", "westwood park",
    "anza vista", "lone mountain", "duboce triangle", "eureka valley", "parkmerced",
    "treasure island", "silver terrace", "little hollywood", "india basin",
]
# Words may be separated by spaces, hyphens, underscores or a regex-style "\s+" (an earlier scanner
# hid a name inside a regular expression, so that spelling is caught too).
_SEP = r"(?:\\[sSbB]|[^A-Za-z]){1,6}"
NEIGHBOURHOOD_RE = re.compile(
    r"(?i)(?<![a-z])(?:"
    + "|".join(_SEP.join(re.escape(w) for w in n.split(" ")) for n in _PREFIXED + _DISTRICTS + _NAMED)
    + r")(?![a-z])"
)

# --- 3. initials-style identifiers --------------------------------------------------------------
SPACED_INITIALS_RE = re.compile(r"(?<![A-Za-z0-9.&'’/])[A-Z] [A-Z](?![A-Za-z0-9'’])")
DOTTED_INITIALS_RE = re.compile(r"(?<![A-Za-z0-9.])[A-Z]\.\s?[A-Z]\.(?![A-Za-z])")
DOTTED_OK = {"U.S.", "U. S.", "S.F.", "D.C.", "A.M.", "P.M.", "P.O.", "N.A."}
LABELLED_INITIALS_RE = re.compile(r"\b[Tt]enants?\s*(?:names?\s*)?[:=]\s*[A-Z]{2}\b")

# --- 4. street addresses ------------------------------------------------------------------------
STREET_RE = re.compile(
    r"\b\d{1,5}\s+(?:[A-Z][a-z]+\.?\s+){1,3}"
    r"(?:Street|St|Avenue|Ave|Boulevard|Blvd|Way|Drive|Dr|Court|Ct|Place|Pl|Road|Rd|Lane|Ln|Terrace)\b"
)
NUMBERED_STREET_RE = re.compile(r"(?i)\b\d{1,5}\s+\d{1,2}(?:st|nd|rd|th)\s+(?:avenue|ave|street|st)\b")
PUBLIC_OFFICE_ADDRESSES = {
    "25 Van Ness Avenue",  # San Francisco Rent Board
}

# --- 5. contact details -------------------------------------------------------------------------
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PUBLIC_EMAIL_DOMAINS = {
    "sfgov.org", "sf.gov", "evictiondefense.org", "users.noreply.github.com", "hud.gov",
    "calcivilrights.ca.gov",
}
PHONE_RE = re.compile(r"(?<![\d-])\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}(?![\d-])")
PUBLIC_PHONES = {
    "4152524600",  # San Francisco Rent Board counselling line
    "4156599184",  # Eviction Defense Collaborative
    "8008841684",  # California Civil Rights Department
    "8003473739",  # HUD housing-discrimination line
    "4154896524",  # public-agency number already published on the site
}

TEXT_SUFFIXES = {
    ".html", ".htm", ".md", ".py", ".json", ".csv", ".txt", ".yml", ".yaml", ".css", ".js", ".xml", ".svg", "",
}


def scan_text(text: str, path: Path | None = None) -> list[tuple[str, str]]:
    """Return a list of (label, matched text) for anything that looks private."""
    hits: list[tuple[str, str]] = []
    is_self = path is not None and Path(path).resolve() == SELF

    for m in ZIP_RE.finditer(text):
        if m.group(0) not in PUBLIC_OFFICE_ZIPS:
            hits.append(("postal code", m.group(0)))

    if not is_self:  # this file holds the citywide list by design
        for m in NEIGHBOURHOOD_RE.finditer(text):
            hits.append(("neighbourhood name", m.group(0)))

    for m in SPACED_INITIALS_RE.finditer(text):
        hits.append(("initials-style identifier", m.group(0)))
    for m in DOTTED_INITIALS_RE.finditer(text):
        if m.group(0) not in DOTTED_OK:
            hits.append(("initials-style identifier", m.group(0)))
    for m in LABELLED_INITIALS_RE.finditer(text):
        hits.append(("initials-style identifier", m.group(0)))

    for m in STREET_RE.finditer(text):
        if m.group(0) not in PUBLIC_OFFICE_ADDRESSES:
            hits.append(("street address", m.group(0)))
    for m in NUMBERED_STREET_RE.finditer(text):
        hits.append(("street address", m.group(0)))

    for m in EMAIL_RE.finditer(text):
        domain = m.group(0).rsplit("@", 1)[1].lower()
        if domain not in PUBLIC_EMAIL_DOMAINS:
            hits.append(("e-mail address", m.group(0)))
    for m in PHONE_RE.finditer(text):
        digits = re.sub(r"\D", "", m.group(0))
        if digits not in PUBLIC_PHONES:
            hits.append(("telephone number", m.group(0)))
    return hits


def tracked_text_files() -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
        ).stdout.decode("utf-8")
        files = [ROOT / f for f in out.split("\0") if f]
    except Exception:  # not a git checkout (e.g. an exported archive): walk the tree instead
        files = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
    return sorted(p for p in files if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES)


def main() -> int:
    problems: list[str] = []
    files = tracked_text_files()
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, hit in scan_text(text, path):
            problems.append(f"{path.relative_to(ROOT)}: {label}: {hit!r}")
    print(f"privacy sweep: {len(files)} tracked text files scanned")
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print("  x", p)
        print("PRIVACY SWEEP FAILED")
        return 1
    print("PRIVACY SWEEP PASSED - no postal code, neighbourhood, initials, street address or private contact detail found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
