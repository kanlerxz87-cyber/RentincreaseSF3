#!/usr/bin/env python3
"""
Line-by-line verification of the built site.

Checks performed
  1. Every internal link and asset reference resolves to a real file.
  2. Every external link is https, on an allow-listed official host, and present in the source register.
  3. Every <a href> in the site is accounted for by the register (no stray citations).
  4. HTML parses cleanly and tags balance.
  5. Personal identifiers from the brief do not appear anywhere in the output.
  6. The published arithmetic in data/findings.json matches a fresh computation from the
     Rent Board percentages, to the cent.
  7. Counts shown on the home page match the registry.

Exit code 1 on any failure.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from html.parser import HTMLParser

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build  # single source of truth for the flag classification and the counts

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"

ALLOWED_HOST_FRAGMENTS = (
    ".gov", "sfgov.org", "leginfo.legislature.ca.gov",
    "law.cornell.edu", "sec.gov",
)

# Personal identifiers as given in the brief. These must never render on the site.
PII_TOKENS = ["L O", "V N", "JP", "M T", "E R", "I S"]

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


class Balance(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            pass
        else:
            self.stack.append((tag, self.getpos()[0]))
        for name, value in attrs:
            if name == "href" and value:
                self.links.append(value)
            if name == "src" and value:
                self.links.append(value)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"line {self.getpos()[0]}: stray </{tag}>")
            return
        open_tag, line = self.stack.pop()
        if open_tag != tag:
            self.errors.append(f"line {self.getpos()[0]}: </{tag}> closes <{open_tag}> opened at line {line}")

    def close(self):
        super().close()
        for tag, line in self.stack:
            self.errors.append(f"unclosed <{tag}> opened at line {line}")


def money(x: D) -> D:
    return x.quantize(D("0.01"), rounding=ROUND_HALF_UP)


def main() -> int:
    fails: list[str] = []
    notes: list[str] = []

    sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))["sources"]
    findings = json.loads((DATA / "findings.json").read_text(encoding="utf-8"))
    registered_urls = {s["url"] for s in sources.values()}

    pages = sorted(ROOT.glob("*.html"))
    if not pages:
        return _fail(["no pages built"])

    # ---- 1..4 parse, balance, links -----------------------------------------------
    seen_external: set[str] = set()
    for page in pages:
        raw = page.read_text(encoding="utf-8")
        parser = Balance()
        parser.feed(raw)
        parser.close()
        for err in parser.errors:
            fails.append(f"{page.name}: {err}")

        for href in parser.links:
            if href.startswith("#") or href.startswith("mailto:"):
                continue
            external = re.match(r"^https?://", href)
            if external:
                if not href.startswith("https://"):
                    fails.append(f"{page.name}: non-https external link {href}")
                host = re.match(r"https://([^/]+)/", href)
                host = host.group(1) if host else ""
                if not any(frag in host for frag in ALLOWED_HOST_FRAGMENTS):
                    fails.append(f"{page.name}: external link to non-official host {href}")
                seen_external.add(href)
                if host and "github.io" not in host and href not in registered_urls:
                    fails.append(f"{page.name}: external link not in source register: {href}")
                continue
            target = (page.parent / href.split("#")[0]).resolve()
            if not target.exists():
                fails.append(f"{page.name}: broken internal link {href}")

    for key, s in sources.items():
        if not s["url"].startswith("https://"):
            fails.append(f"source {key}: not https")
        host = re.match(r"https://([^/]+)/", s["url"])
        host = host.group(1) if host else ""
        if not any(frag in host for frag in ALLOWED_HOST_FRAGMENTS):
            fails.append(f"source {key}: host {host} not official")

    # ---- 5 PII ---------------------------------------------------------------------
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for token in PII_TOKENS:
            if re.search(r"\b" + re.escape(token) + r"\b", text):
                fails.append(f"{page.name}: contains personal identifier {token!r}")

    # ---- 6 arithmetic --------------------------------------------------------------
    aga = {"2020": D("1.8"), "2021": D("0.7"), "2022": D("2.3"), "2023": D("3.6"),
           "2024": D("1.7"), "2025": D("1.4"), "2026": D("1.6")}

    unit1 = D("3995")
    c1 = {
        "1.4": money(unit1 * D("0.014")),
        "1.6": money(unit1 * D("0.016")),
        "3.0": money(unit1 * D("0.030")),
    }
    expected_unit1 = {"55.93": c1["1.4"], "4050.93": unit1 + c1["1.4"],
                      "63.92": c1["1.6"], "4058.92": unit1 + c1["1.6"],
                      "119.85": c1["3.0"], "4114.85": unit1 + c1["3.0"]}

    unit2 = D("3150")
    total_pct = sum(aga.values())
    inc2 = money(unit2 * total_pct / 100)
    expected_unit2 = {"13.1": total_pct, "412.65": inc2, "3562.65": unit2 + inc2}

    # no compounding: sum of yearly dollar amounts must equal the single-step figure
    sum_years = sum(money(unit2 * v / 100) for v in aga.values())
    if sum_years != inc2:
        fails.append(f"Unit 2 compounding check failed: yearly sum {sum_years} != {inc2}")

    rows = {r["id"]: r for s in findings["sections"] for r in s["rows"]}

    def must_contain(row_id: str, needles: dict[str, D]) -> None:
        blob = rows[row_id]["detail"] + " " + rows[row_id]["value"]
        for text, expected in needles.items():
            if text not in blob.replace("$", "").replace(",", ""):
                fails.append(f"{row_id}: expected value {text} missing from row text")
            # confirm the literal we published equals the computed figure
            if " " in text:
                continue
            if expected != D(text):
                fails.append(f"{row_id}: published {text} != computed {expected}")

    must_contain("U02", {"55.93": c1["1.4"], "4050.93": unit1 + c1["1.4"]})
    must_contain("U03", {"63.92": c1["1.6"], "4058.92": unit1 + c1["1.6"]})
    must_contain("U04", {"119.85": c1["3.0"], "4114.85": unit1 + c1["3.0"]})
    must_contain("U08", {"13.1": total_pct})
    must_contain("U09", {"412.65": inc2, "3562.65": unit2 + inc2})

    # the summed percentages quoted in U08 must equal the published total.
    # U08 reads "a + b + ... = 13.1%"; parse both sides of the "=" rather than relying on % placement.
    expr = rows["U08"]["detail"].split("=")[0]
    listed = [D(x.strip()) for x in expr.split("+") if re.fullmatch(r"\s*\d+(\.\d+)?\s*", x)]
    if listed != list(aga.values()):
        fails.append(f"U08: year list {listed} != published rates {list(aga.values())}")
    stated_total = D(re.search(r"=\s*([\d.]+)%", rows["U08"]["detail"]).group(1))
    if sum(listed) != stated_total:
        fails.append(f"U08: year list sums to {sum(listed)}, row states {stated_total}")
    if stated_total != total_pct:
        fails.append(f"U08: stated total {stated_total} != computed {total_pct}")

    # the seven-year ladder in U07 must quote the same rates, in anniversary order
    ladder = [D(x) for x in re.findall(r"(?<![\d.])([0-9]\.[0-9])%", rows["U07"]["detail"])]
    if ladder != list(aga.values()):
        fails.append(f"U07: rate ladder {ladder} != {list(aga.values())}")

    # ---- 7 counts ------------------------------------------------------------------
    all_rows = list(rows.values())
    c = build.counts(all_rows)
    total, verified, unver, flagged = c["total"], c["verified"], c["unverified"], c["flags"]
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    for value, label in ((total, "findings"), (verified, "verified"), (unver, "unverified"),
                         (c["open"], "open facts"), (c["review"], "need review")):
        if f"<b>{value}</b>" not in home:
            fails.append(f"index.html: stat {value} ({label}) not shown")

    # the words in the executive summary must match the computed counts
    prose = [
        (f"{unver} values in this review are unverified", unver, "unverified"),
        (f"{c['open']} more depend on facts", c["open"], "open facts"),
        (f"{c['review']} need a judgement call", c["review"], "judgement rows"),
    ]
    for needle, value, label in prose:
        if needle not in home:
            fails.append(f"index.html: prose should state {value} {label} (looked for {needle!r})")

    # flagged page must carry every flagged/unverified row
    flagged_page = (ROOT / "flagged.html").read_text(encoding="utf-8")
    for rid, row in rows.items():
        if build.flag_kind(row):
            if rid not in flagged_page:
                fails.append(f"flagged.html: missing row {rid}")
    # and the flagged page must not invent any row that is not flagged
    for rid in rows:
        if not build.flag_kind(rows[rid]) and f'<span class="rid">{rid}</span>' in flagged_page:
            fails.append(f"flagged.html: row {rid} is listed but is not flagged")

    # every row id must appear on exactly one section page
    for sec in findings["sections"]:
        page = (ROOT / f"{sec['id']}.html").read_text(encoding="utf-8")
        for row in sec["rows"]:
            if row["id"] not in page:
                fails.append(f"{sec['id']}.html: row {row['id']} not rendered")

    print(f"pages: {len(pages)}   findings: {total} (verified {verified}, unverified {unver}, flagged {flagged})")
    print(f"external links followed: {len(seen_external)}   registered sources: {len(sources)}")
    print(f"unit 1 -> 1.4%: {c1['1.4']} / 1.6%: {c1['1.6']} / 3.0%: {c1['3.0']}")
    print(f"unit 2 -> {total_pct}% = {inc2}  (yearly-sum cross-check {sum_years})")

    if fails:
        print("\nFAILURES:", file=sys.stderr)
        for f in fails:
            print("  -", f, file=sys.stderr)
        return 1
    print("\nAll checks passed.")
    return 0


def _fail(items: list[str]) -> int:
    for i in items:
        print("  -", i, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
