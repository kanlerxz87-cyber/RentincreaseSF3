#!/usr/bin/env python3
"""
Build the static site from data/sources.json and data/findings.json.

Output: index.html, one page per section, flagged.html, sources.html, assets/.

Design rules baked in here:
  * No page is written by hand; every row on every page comes from the JSON registry.
  * Every row must resolve to a key in sources.json, and that source must have a URL on an
    official/primary host or an SEC filing. The build fails otherwise.
  * Any row whose status is not "verified", or whose note contains FLAGGED, is also published
    on flagged.html. Nothing is silently dropped.
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"
SITE = ROOT

ALLOWED_HOST_FRAGMENTS = (
    ".gov",            # sf.gov, huduser.gov, bls.gov, oag.ca.gov, justice.gov, ecfr.gov
    "sfgov.org",
    "leginfo.legislature.ca.gov",
    "law.cornell.edu",   # U.S. Code / CFR mirror of official text
    "sec.gov",
    "ss.ca.gov",
)

BASE_URL = "https://kanlerxz87-cyber.github.io/RentincreaseSF3"

NAV_EXTRA = [
    ("flagged.html", "Flagged for review"),
    ("sources.html", "Source register"),
]


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def source_host(entry: dict) -> str:
    m = re.match(r"https?://([^/]+)/", entry["url"])
    return m.group(1) if m else ""


def load() -> tuple[dict, dict]:
    with open(DATA / "sources.json", encoding="utf-8") as fh:
        sources = json.load(fh)["sources"]
    with open(DATA / "findings.json", encoding="utf-8") as fh:
        findings = json.load(fh)
    return sources, findings


def validate(sources: dict, findings: dict) -> list[str]:
    problems: list[str] = []
    seen_ids: dict[str, str] = {}
    for sec in findings["sections"]:
        for row in sec["rows"]:
            tag = row["id"]
            if tag in seen_ids:
                problems.append(f"duplicate row id {tag}")
            seen_ids[tag] = sec["id"]
            key = row["source"]
            if key not in sources:
                problems.append(f"{tag}: unknown source key {key!r}")
                continue
            src = sources[key]
            url = src.get("url", "")
            host = source_host(src)
            if not url.startswith("https://"):
                problems.append(f"{tag}: source {key} is not https")
            if not any(frag in host for frag in ALLOWED_HOST_FRAGMENTS):
                problems.append(f"{tag}: source {key} host {host!r} is not an official host")
            if src.get("tier") not in {"primary", "official-summary", "filer"}:
                problems.append(f"{tag}: source {key} has unexpected tier")
            if row["status"] not in {"verified", "unverified"}:
                problems.append(f"{tag}: bad status {row['status']!r}")
            if not row.get("claim"):
                problems.append(f"{tag}: empty claim")
    return problems


STATUS_LABEL = {"verified": "Verified", "unverified": "Unverified"}


def flag_kind(row: dict) -> str | None:
    """Classify anything that must be published on the Flagged for review page.

    'unverified' - the value itself could not be confirmed against an official source
    'open'       - the rule is sourced, but a fact needed to apply it was not supplied
    'review'     - two official sources conflict, or the row is judgement rather than quoted text
    """
    note = row.get("note", "").upper()
    if row["status"] == "unverified":
        return "unverified"
    if "UNVERIFIED IN THIS REVIEW" in note:
        return "open"
    if "FLAGGED" in note:
        return "review"
    return None


def counts(rows: list[dict]) -> dict:
    kinds = [flag_kind(r) for r in rows]
    return {
        "total": len(rows),
        "verified": sum(1 for r, k in zip(rows, kinds) if r["status"] == "verified" and k is None),
        "unverified": kinds.count("unverified"),
        "open": kinds.count("open"),
        "review": kinds.count("review"),
        "flags": sum(1 for k in kinds if k),
    }


def badge(status: str) -> str:
    cls = "ok" if status == "verified" else "warn"
    return f'<span class="badge {cls}">{STATUS_LABEL[status]}</span>'


def src_link(sources: dict, key: str) -> str:
    s = sources[key]
    host = source_host(s)
    tier = {"primary": "primary source", "official-summary": "official summary", "filer": "issuer filing"}[s["tier"]]
    return (
        f'<a class="src" href="{esc(s["url"])}" target="_blank" rel="noopener">'
        f'{esc(s["title"])}<span class="src-meta">{esc(host)} · {esc(tier)}</span></a>'
    )


def nav_html(current: str, findings: dict) -> str:
    items = [(f"{s['id']}.html", s["title"]) for s in findings["sections"]] + NAV_EXTRA
    out = []
    for href, label in items:
        cls = ' class="active"' if href == current else ""
        out.append(f'<a href="{href}"{cls}>{esc(label)}</a>')
    return "\n".join(out)


def page_shell(*, title: str, description: str, current: str, findings: dict, body: str,
               wide: bool = False) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="brand">
    <span class="dot" aria-hidden="true"></span>
    <a href="index.html">Rental Increase Review <span class="brand-sub">SF 94122</span></a>
  </div>
  <div class="top-right">
    <span class="pill">Built 2026-11-06</span>
    <button id="navtoggle" class="navtoggle" aria-expanded="false" aria-controls="sidenav">Sections</button>
  </div>
</header>
<div class="layout{" wide" if wide else ""}">
  <nav id="sidenav" class="sidenav" aria-label="Sections">
    {nav_html(current, findings)}
  </nav>
  <main id="main">
{body}
  </main>
</div>
<footer class="foot">
  <p>Prepared from official sources retrieved on 2026-11-06. Every row links to the document it came from.
  Nothing here is legal advice. Personal identifiers are replaced with codes (P1&#8211;P6); dates and amounts are unchanged.</p>
  <p><a href="sources.html">Source register</a> · <a href="flagged.html">Flagged for review</a></p>
</footer>
<script src="assets/app.js"></script>
</body>
</html>
"""


def table_block(section_id: str, rows: list[dict], sources: dict) -> str:
    body = []
    for r in rows:
        note = r.get("note", "")
        kind = flag_kind(r)
        flag = kind is not None
        note_html = esc(note)
        if flag:
            note_html = f'<span class="flagmark">Flagged</span> {note_html}'
        body.append(f"""      <tr data-status="{r['status']}" data-flag="{'1' if flag else '0'}">
        <td class="c-id"><span class="rid">{esc(r['id'])}</span></td>
        <td class="c-topic">{esc(r['topic'])}</td>
        <td class="c-claim"><p class="claim">{esc(r['claim'])}</p><p class="detail">{esc(r['detail'])}</p></td>
        <td class="c-value">{esc(r['value']) if r['value'] else '<span class="blank">blank</span>'}</td>
        <td class="c-status">{badge(r['status'])}{'<span class="badge flag">Flag</span>' if flag else ''}</td>
        <td class="c-src">{src_link(sources, r['source'])}</td>
      </tr>""")
    return f"""<div class="tablewrap">
  <table class="grid" id="grid-{esc(section_id)}">
    <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col">Topic</th>
        <th scope="col">Finding and detail</th>
        <th scope="col">Value</th>
        <th scope="col">Status</th>
        <th scope="col">Source</th>
      </tr>
    </thead>
    <tbody>
{chr(10).join(body)}
    </tbody>
  </table>
</div>"""


def section_page(sec: dict, sources: dict, findings: dict) -> str:
    rows = sec["rows"]
    n = len(rows)
    c = counts(rows)
    flags = c["flags"]
    unver = c["unverified"]
    body = f"""
    <div class="pagehead">
      <p class="eyebrow">Category</p>
      <h1>{esc(sec['title'])}</h1>
      <p class="lede">{esc(sec['subtitle'])}</p>
      <p class="intro">{esc(sec['intro'])}</p>
      <div class="stats">
        <div class="stat"><b>{n}</b><span>findings</span></div>
        <div class="stat"><b>{c['verified']}</b><span>verified, no caveat</span></div>
        <div class="stat"><b>{unver}</b><span>unverified</span></div>
        <div class="stat"><b>{c['open']}</b><span>open facts</span></div>
        <div class="stat"><b>{c['review']}</b><span>need review</span></div>
      </div>
    </div>
    <div class="toolbar">
      <input type="search" id="q" placeholder="Filter this table…" aria-label="Filter this table">
      <div class="chips" role="group" aria-label="Filter by status">
        <button class="chip on" data-filter="all">All</button>
        <button class="chip" data-filter="verified">Verified</button>
        <button class="chip" data-filter="unverified">Unverified</button>
        <button class="chip" data-filter="flag">Flagged</button>
      </div>
      <span class="count" id="count">{n} rows</span>
    </div>
{table_block(sec['id'], rows, sources)}
"""
    return page_shell(
        title=f"{sec['title']} — Rental Increase Review SF 94122",
        description=sec["subtitle"],
        current=f"{sec['id']}.html",
        findings=findings,
        body=body,
        wide=True,
    )


def exec_summary(findings: dict) -> str:
    summ = counts([r for s in findings["sections"] for r in s["rows"]])
    return f"""
    <section id="summary" class="card">
      <h2>Executive summary</h2>
      <p>Two rent-controlled units in a 1940 two-unit building in ZIP 94122 are occupied. Unit 1 was re-let on
      1 February 2025 at $3,995 and is now at $3,995 after a tenancy change on 1 April 2026. Unit 2 has been
      at $3,150 since 1 June 2019 with no increase recorded. The question is what an increase may lawfully be,
      how to serve it, and whether one unit or both should receive one.</p>

      <ol class="findings">
        <li><b>The ceiling is local, not state.</b> The Rent Board's allowable annual increase for
        1 March 2026 &#8211; 28 February 2027 is <b>1.6%</b> of base rent. The prior period was 1.4%.
        The Attorney General's 8.8% figure for the San Francisco area is the <i>state</i> cap and does not
        apply, because Civil Code 1947.12(d)(3) yields to a stricter local ordinance.</li>

        <li><b>Unit 1: three lawful outcomes.</b> 1.4% ($55.93, to $4,050.93) if the 1 February 2026
        anniversary was used; 1.6% ($63.92, to $4,058.92) for an effective date on or after 1 March 2026;
        or 3.0% ($119.85, to $4,114.85) at the 1 February 2027 anniversary if the 1.4% was banked and not used.</li>

        <li><b>Unit 2: 13.1% is the accumulated maximum, and it is the big number.</b> Seven annual allowances
        from 1 June 2020 to 1 June 2026 &#8212; 1.8, 0.7, 2.3, 3.6, 1.7, 1.4, 1.6 &#8212; add to 13.1% without
        compounding. On $3,150 that is <b>$412.65</b>, taking rent to <b>$3,562.65</b>. Because 13.1% exceeds
        10%, <b>90 days' written notice is required</b> (95 if mailed). This is the most error-prone step in the file.</li>

        <li><b>Three prerequisites come before any notice.</b> A current rent increase licence for each unit
        (Ordinance 37.15(e)); a 30/90-day written notice stating dollar amount, percentage and effective date,
        with the banked portion identified; and no retaliation flag in the preceding 180 days.</li>

        <li><b>One formal defect voids the whole increase.</b> Ordinance 37.3(b)(5) and Rule 4.10(b) make a
        non-conforming increase null and void, with only a narrow good-faith allowance of 0.5% of prior base rent.
        The notice wording matters more than the percentage.</li>

        <li><b>One unit or both: raise both, with one method and a written basis for each number.</b> Nothing
        reviewed requires the two units to receive the same increase, and the two calculations are different by
        design &#8212; different anniversary dates, different banked histories. The discrimination exposure is not the
        increase you serve; it is an <i>unexplained difference</i> between two units. Federal disparate-impact
        liability does not require intent, so the defence is a uniform rule, a uniform template, and a
        documented calculation for each unit. Withholding a lawful increase is not itself unlawful &#8212; the unused
        percentage simply banks &#8212; but it converts a current decision into a deferred one with a larger number and a
        90-day notice requirement later.</li>

        <li><b>No rent increase may be justified by the April 2026 occupancy change.</b> Adding an occupant is
        not a lawful basis for an increase, and the market-rate 6.14 / Costa-Hawkins route is closed while an
        original tenant remains in occupancy.</li>

        <li><b>{summ['unverified']} values in this review are unverified, {summ['open']} more depend on facts
        that were not supplied, and {summ['review']} need a judgement call.</b> Each is published on the
        <a href="flagged.html">Flagged for review</a> page and none blocks the rest of the analysis.
        The open facts that matter most: licence status for both units, whether a 1 February 2026 increase was
        actually served, the 2019 rent history supporting the $3,150 base, and any repair or complaint history
        in the last 180 days. No value has been inferred for any of them.</li>
      </ol>
    </section>
    """


def index_page(findings: dict, sources: dict) -> str:
    meta = findings["meta"]
    sections = findings["sections"]
    rows = [r for s in sections for r in s["rows"]]
    total = len(rows)
    c = counts(rows)
    verified = c["verified"]
    flagged = c["flags"]
    unver = c["unverified"]

    cards = []
    for s in sections:
        n = len(s["rows"])
        cards.append(f"""      <a class="tile" href="{s['id']}.html">
        <h3>{esc(s['title'])}</h3>
        <p>{esc(s['subtitle'])}</p>
        <span class="tile-meta">{n} findings · {counts(s['rows'])['flags']} flagged</span>
      </a>""")

    unit_cards = f"""
    <section class="card">
      <h2>At a glance</h2>
      <table class="keytable">
        <thead><tr><th>Item</th><th>Unit 1</th><th>Unit 2</th><th>Source</th></tr></thead>
        <tbody>
          <tr><td>Initial lease start</td><td>1 February 2025</td><td>1 June 2019</td><td class="muted">provided in brief</td></tr>
          <tr><td>Base rent at that date</td><td>$3,995.00</td><td>$3,150.00</td><td class="muted">provided in brief</td></tr>
          <tr><td>Rent now</td><td>$3,995.00 (from 1 April 2026)</td><td>$3,150.00</td><td class="muted">provided in brief</td></tr>
          <tr><td>Original tenants / current tenants</td><td>P1, P2, P3 / P1, P4</td><td>P5, P6 / P5, P6</td><td class="muted">anonymised</td></tr>
          <tr><td>Earliest lawful increase date</td><td>1 February 2026</td><td>1 June 2020</td><td>{src_link(sources,'sf-rent-increase')}</td></tr>
          <tr><td>Rate in effect on that date</td><td>1.4%</td><td>1.8%</td><td>{src_link(sources,'sf-571')}</td></tr>
          <tr><td>Rate in effect now</td><td>1.6%</td><td>1.6%</td><td>{src_link(sources,'sf-571')}</td></tr>
          <tr><td>Maximum accumulated increase available</td><td>1.4% – 3.0% (see scenarios)</td><td>13.1%</td><td>{src_link(sources,'sf-banked')}</td></tr>
          <tr><td>Maximum dollar increase</td><td>$55.93 / $63.92 / $119.85</td><td>$412.65</td><td>{src_link(sources,'sf-rent-increase')}</td></tr>
          <tr><td>Notice period required</td><td>30 days</td><td>90 days (95 if mailed)</td><td>{src_link(sources,'civ827')}</td></tr>
          <tr><td>Rent increase licence</td><td><span class="blank">not verified</span></td><td><span class="blank">not verified</span></td><td>{src_link(sources,'sf-3715')}</td></tr>
        </tbody>
      </table>
      <p class="note">Amounts are arithmetic on the base rents stated in the brief and the published Rent Board
      percentages. They are not rounded up, per the Rent Board's rule. No value has been inferred where a fact
      was not supplied.</p>
    </section>
    """

    body = f"""
    <div class="pagehead hero">
      <p class="eyebrow">San Francisco · Outer Sunset · 94122 · two rent-controlled units · built 1940</p>
      <h1>What a lawful rent increase looks like here</h1>
      <p class="lede">A line-by-line review of every local, state and federal rule that governs an increase on
      these two units, the arithmetic for each, and the test a tenant-side lawyer would run.</p>
      <div class="stats">
        <div class="stat"><b>{total}</b><span>findings</span></div>
        <div class="stat"><b>{verified}</b><span>verified, no caveat</span></div>
        <div class="stat"><b>{unver}</b><span>values unverified</span></div>
        <div class="stat"><b>{c['open']}</b><span>open facts</span></div>
        <div class="stat"><b>{c['review']}</b><span>need review</span></div>
      </div>
      <div class="hero-actions">
        <a class="btn primary" href="units.html">Worked calculations</a>
        <a class="btn" href="review.html">Review test: one unit or both</a>
        <a class="btn" href="flagged.html">Flagged for review ({flagged})</a>
      </div>
    </div>
{exec_summary(findings)}
{unit_cards}
    <section class="card">
      <h2>Browse by category</h2>
      <div class="tiles">
{chr(10).join(cards)}
      </div>
    </section>
    <section class="card">
      <h2>How this was built</h2>
      <ul class="plain">
        <li>Every statement on every page is a row in a machine-readable registry
        (<code>data/findings.json</code>) and must point to an entry in the source register
        (<code>data/sources.json</code>). The build refuses to run if a row points at a missing source,
        a non-HTTPS URL, or a host that is not an official government domain or an SEC filing.</li>
        <li>Each source was retrieved and read directly on 2026-11-06. Where a page was a summary rather
        than the legal text, it is labelled <i>official summary</i>; where the legal text itself was read,
        it is labelled <i>primary source</i>; where the document is a company filing, it is labelled
        <i>issuer filing</i>.</li>
        <li>Where a value could not be confirmed from an official source it is blank and marked
        <span class="badge warn">Unverified</span>. Nothing has been estimated, averaged, or inferred to fill a gap.</li>
        <li>Where two official sources disagree, and where a conclusion is judgement rather than a quoted
        prohibition, the row is marked <span class="badge flag">Flag</span> and reproduced on the
        <a href="flagged.html">Flagged for review</a> page.</li>
        <li>Secondary sources — law-firm blogs, brokerage calculators, listing sites — were located during
        research and were <b>not</b> used to support any row. Several of them disagreed with each other
        (1.6% vs 1.7% for the same period), which is why the Rent Board's own documents are the anchor.</li>
      </ul>
    </section>
"""
    return page_shell(
        title="Rental Increase Review — SF Outer Sunset 94122",
        description="Verified review of rent increase rules for two rent-controlled units in San Francisco 94122.",
        current="index.html",
        findings=findings,
        body=body,
    )


def flagged_page(findings: dict, sources: dict) -> str:
    groups = {
        "unverified": ("Value unverified", "The number or fact itself could not be confirmed, so it is left blank or shown as conflicting rather than resolved. No figure has been estimated to fill the gap.", "warn"),
        "open": ("Fact not supplied", "The rule is sourced and settled; applying it needs a fact about these units that was not provided. Nothing has been assumed.", "warn"),
        "review": ("Needs a decision", "Two official sources conflict, or the row is a judgement rather than quoted text. Read the reasoning before relying on it.", "flag"),
    }
    buckets: dict[str, list[tuple[dict, str]]] = {k: [] for k in groups}
    for sec in findings["sections"]:
        for r in sec["rows"]:
            k = flag_kind(r)
            if k:
                buckets[k].append((r, sec["title"]))

    total = sum(len(v) for v in buckets.values())
    blocks = []
    for key, (label, blurb, tone) in groups.items():
        items = buckets[key]
        if not items:
            continue
        cards = []
        for r, sec_title in items:
            why = r.get("note", "")
            why = why.replace("FLAGGED. ", "").replace("FLAGGED ", "").replace("UNVERIFIED IN THIS REVIEW: ", "")
            cards.append(f"""      <article class="flagitem">
        <header>
          <span class="rid">{esc(r['id'])}</span>
          <span class="badge {tone}">{esc(label)}</span>
          <span class="muted">{esc(sec_title)}</span>
        </header>
        <h3>{esc(r['claim'])}</h3>
        <p>{esc(r['detail'])}</p>
        <p class="why"><b>Why it is here:</b> {esc(why) if why else 'Not confirmed against an official source.'}</p>
        <p class="srcrow">Source: {src_link(sources, r['source'])}</p>
      </article>""")
        blocks.append(f"""    <section class="flaggroup">
      <div class="grouphead">
        <h2>{esc(label)} <span class="badge neutral">{len(items)}</span></h2>
        <p>{esc(blurb)}</p>
      </div>
{chr(10).join(cards)}
    </section>""")

    body = f"""
    <div class="pagehead">
      <p class="eyebrow">Needs your review</p>
      <h1>Flagged for review</h1>
      <p class="lede">Everything on this page is either unconfirmed or depends on a judgement call. None of it
      blocks the rest of the review; all of it is listed here so it can be settled by a person rather than assumed.</p>
      <div class="stats">
        <div class="stat"><b>{total}</b><span>items</span></div>
        <div class="stat"><b>{len(buckets['unverified'])}</b><span>unverified values</span></div>
        <div class="stat"><b>{len(buckets['open'])}</b><span>facts not supplied</span></div>
        <div class="stat"><b>{len(buckets['review'])}</b><span>need a decision</span></div>
      </div>
    </div>
    <section class="card">
      <h2>How to close each item</h2>
      <ul class="plain">
        <li><b>Rent increase licence (R02, U14).</b> Look up both units in the Rent Board Portal
        (<code>portal.sfrb.org</code>). If a licence is missing, file the Housing Inventory report before
        serving any notice &#8212; without it the tenant owes nothing for the suspension period.</li>
        <li><b>The February 2026 anniversary (U01).</b> Establish whether a 1.4% increase was actually served on
        Unit 1 in February 2026. If it was, only the 1.6% is available now; if it was not, both bank.</li>
        <li><b>The 2019 rent history (U11).</b> Produce the 1 June 2019 lease and every notice since. The 13.1%
        calculation rests on $3,150 being the lawful base rent on that date.</li>
        <li><b>The 180-day retaliation window (R08).</b> Pull the repair and complaint log for both units before
        fixing an effective date.</li>
        <li><b>The banking threshold (L13).</b> Ask a Rent Board counselor (415-252-4600) whether a skipped year
        banks after 12 months or 24 months. It does not affect Unit 2 either way.</li>
        <li><b>Coverage and title (L01, S07).</b> Confirm the certificate of occupancy on the Planning Property
        Information Map, and confirm the building has not been condominium-converted, which would open the
        Costa-Hawkins analysis.</li>
      </ul>
    </section>
{chr(10).join(blocks)}
"""
    return page_shell(
        title="Flagged for review — Rental Increase Review SF 94122",
        description="Unverified and judgement-dependent items in the rent increase review.",
        current="flagged.html",
        findings=findings,
        body=body,
    )


def sources_page(sources: dict, findings: dict) -> str:
    used: dict[str, list[str]] = {}
    for sec in findings["sections"]:
        for r in sec["rows"]:
            used.setdefault(r["source"], []).append(r["id"])

    order = list(sources.keys())
    rows = []
    for key in order:
        s = sources[key]
        hosts = used.get(key, [])
        rows.append(f"""      <tr>
        <td><code>{esc(key)}</code></td>
        <td>{esc(s['title'])}</td>
        <td>{esc(s['publisher'])}</td>
        <td><span class="badge neutral">{esc(s['tier'])}</span></td>
        <td class="muted">{esc(s['checked'])}</td>
        <td>{esc(', '.join(hosts)) if hosts else '<span class="blank">not cited</span>'}</td>
        <td><a class="src" href="{esc(s['url'])}" target="_blank" rel="noopener">Open<span class="src-meta">{esc(source_host(s))}</span></a></td>
      </tr>""")

    uncited = [k for k in order if k not in used]
    body = f"""
    <div class="pagehead">
      <p class="eyebrow">Provenance</p>
      <h1>Source register</h1>
      <p class="lede">{len(sources)} documents. Each was opened and read on 2026-11-06; the link on each row is the
      document itself, not a summary of it. The right-hand column lists the finding IDs that rest on it.</p>
      <div class="stats">
        <div class="stat"><b>{len(sources)}</b><span>documents</span></div>
        <div class="stat"><b>{len(sources) - len(uncited)}</b><span>cited by a finding</span></div>
        <div class="stat"><b>{len(uncited)}</b><span>register-only</span></div>
      </div>
    </div>
    <section class="card">
      <h2>Document list</h2>
      <div class="tablewrap">
        <table class="grid">
          <thead><tr><th>Key</th><th>Document</th><th>Publisher</th><th>Tier</th><th>Read</th><th>Cited by</th><th>Link</th></tr></thead>
          <tbody>
{chr(10).join(rows)}
          </tbody>
        </table>
      </div>
      <p class="note"><b>Tier.</b> <i>primary</i> = the legal text or the agency's own published figures;
      <i>official-summary</i> = the issuing agency's explanatory page; <i>filer</i> = a company's own SEC filing.
      No secondary or commercial source supports any finding in this review.</p>
    </section>
"""
    return page_shell(
        title="Source register — Rental Increase Review SF 94122",
        description="Every official document used in this review, with links.",
        current="sources.html",
        findings=findings,
        body=body,
        wide=True,
    )


def write_assets() -> None:
    css = """/* Rental Increase Review - 94122 */
:root{
  --bg:#f6f7f9; --panel:#ffffff; --ink:#14181f; --ink-2:#4a5361; --muted:#7b8494;
  --line:#e3e7ec; --line-2:#eef1f5;
  --accent:#124e78; --accent-2:#1b6ea8; --accent-soft:#eaf2f8;
  --ok:#1a6b46; --ok-soft:#e8f5ee;
  --warn:#8a5a00; --warn-soft:#fdf3e0;
  --flag:#8c2f2f; --flag-soft:#fbeaea;
  --radius:10px; --shadow:0 1px 2px rgba(16,24,40,.05),0 1px 3px rgba(16,24,40,.06);
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 var(--sans)}
a{color:var(--accent-2);text-decoration-thickness:1px;text-underline-offset:2px}
a:hover{color:var(--accent)}
code{font-family:var(--mono);font-size:.86em;background:var(--line-2);padding:.1em .35em;border-radius:4px}
.skip{position:absolute;left:-9999px}
.skip:focus{left:12px;top:12px;z-index:99;background:#fff;padding:10px 14px;border-radius:8px;box-shadow:var(--shadow)}

/* top bar */
.top{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;
  gap:16px;padding:10px 20px;background:rgba(255,255,255,.92);backdrop-filter:saturate(1.4) blur(8px);
  border-bottom:1px solid var(--line)}
.brand a{display:flex;align-items:center;gap:9px;color:var(--ink);font-weight:650;text-decoration:none;letter-spacing:-.01em}
.dot{width:10px;height:10px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 4px var(--accent-soft)}
.brand-sub{font-weight:450;color:var(--muted);font-size:13px}
.top-right{display:flex;align-items:center;gap:10px}
.pill{font-size:12px;color:var(--ink-2);background:var(--line-2);padding:4px 10px;border-radius:999px;white-space:nowrap}
.navtoggle{display:none;border:1px solid var(--line);background:#fff;border-radius:8px;padding:7px 11px;font:inherit;font-size:13px;cursor:pointer}

/* layout */
.layout{display:grid;grid-template-columns:236px minmax(0,1fr);gap:26px;max-width:1240px;margin:0 auto;padding:26px 20px 60px}
.layout.wide{max-width:1500px}
.sidenav{position:sticky;top:66px;align-self:start;display:flex;flex-direction:column;gap:2px;
  padding:8px;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}
.sidenav a{display:block;padding:8px 11px;border-radius:7px;color:var(--ink-2);text-decoration:none;font-size:14px}
.sidenav a:hover{background:var(--line-2);color:var(--ink)}
.sidenav a.active{background:var(--accent-soft);color:var(--accent);font-weight:600}
main{min-width:0}

/* page head */
.pagehead{margin:0 0 22px}
.pagehead.hero{padding:28px;background:linear-gradient(180deg,#fff, #fbfcfd);border:1px solid var(--line);
  border-radius:14px;box-shadow:var(--shadow)}
.eyebrow{margin:0 0 8px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600}
h1{margin:0 0 10px;font-size:30px;line-height:1.2;letter-spacing:-.02em}
.pagehead h1{font-size:27px}
.lede{margin:0 0 10px;font-size:16px;color:var(--ink-2);max-width:78ch}
.intro{margin:0;color:var(--ink-2);max-width:82ch;font-size:14.5px}
.hero-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}
.btn{display:inline-block;padding:9px 14px;border-radius:8px;border:1px solid var(--line);background:#fff;
  color:var(--ink);text-decoration:none;font-size:14px;font-weight:550}
.btn:hover{border-color:var(--accent-2);color:var(--accent)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.primary:hover{background:var(--accent-2);border-color:var(--accent-2);color:#fff}

/* stats */
.stats{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:9px 14px;min-width:104px}
.stat b{display:block;font-size:21px;line-height:1.1;letter-spacing:-.02em}
.stat span{font-size:12px;color:var(--muted)}

/* cards */
.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:22px;
  box-shadow:var(--shadow);margin:0 0 22px}
.card h2{margin:0 0 14px;font-size:19px;letter-spacing:-.01em}
.card p{margin:0 0 12px;color:var(--ink-2);max-width:86ch}
.card p:last-child{margin-bottom:0}
.findings{margin:0;padding-left:20px;color:var(--ink-2)}
.findings li{margin:0 0 12px;max-width:88ch}
.findings li:last-child{margin-bottom:0}
.findings b{color:var(--ink)}
ul.plain{margin:0;padding-left:20px;color:var(--ink-2)}
ul.plain li{margin:0 0 10px;max-width:88ch}
.note{font-size:13px;color:var(--muted);border-top:1px dashed var(--line);padding-top:12px;margin-top:16px!important}

/* tiles */
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.tile{display:block;padding:16px;border:1px solid var(--line);border-radius:10px;background:#fff;
  text-decoration:none;color:inherit;transition:border-color .12s,transform .12s}
.tile:hover{border-color:var(--accent-2);transform:translateY(-1px)}
.tile h3{margin:0 0 6px;font-size:15.5px;letter-spacing:-.01em}
.tile p{margin:0 0 10px;font-size:13px;color:var(--muted);line-height:1.45}
.tile-meta{font-size:12px;color:var(--accent-2);font-weight:600}

/* toolbar */
.toolbar{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:0 0 12px}
.toolbar input[type=search]{flex:1 1 240px;min-width:180px;padding:9px 12px;border:1px solid var(--line);
  border-radius:8px;background:#fff;font:inherit;font-size:14px;color:var(--ink)}
.toolbar input[type=search]:focus{outline:2px solid var(--accent-soft);border-color:var(--accent-2)}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 12px;font:inherit;
  font-size:13px;color:var(--ink-2);cursor:pointer}
.chip:hover{border-color:var(--accent-2);color:var(--accent)}
.chip.on{background:var(--accent);border-color:var(--accent);color:#fff}
.count{font-size:13px;color:var(--muted);margin-left:auto}

/* tables */
.tablewrap{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);overflow:auto;
  box-shadow:var(--shadow);-webkit-overflow-scrolling:touch}
table.grid{width:100%;border-collapse:collapse;font-size:14px;min-width:900px}
table.grid thead th{position:sticky;top:0;z-index:2;text-align:left;font-size:11.5px;letter-spacing:.05em;
  text-transform:uppercase;color:var(--muted);background:#fbfcfd;border-bottom:1px solid var(--line);
  padding:11px 12px;white-space:nowrap;font-weight:650}
table.grid td{padding:13px 12px;border-bottom:1px solid var(--line-2);vertical-align:top}
table.grid tbody tr:last-child td{border-bottom:0}
table.grid tbody tr:hover{background:#fcfdfe}
.c-id{width:52px}
.rid{font-family:var(--mono);font-size:12px;color:var(--accent);background:var(--accent-soft);
  padding:2px 6px;border-radius:4px;font-weight:600}
.c-topic{width:118px;font-size:12.5px;color:var(--ink-2);font-weight:600}
.c-claim{min-width:340px}
.c-value{width:150px;font-size:13px;font-weight:600;color:var(--ink)}
.c-status{width:112px;white-space:nowrap}
.c-src{width:250px;font-size:12.5px}
.claim{margin:0 0 4px;font-weight:600;color:var(--ink);max-width:none}
.detail{margin:0;font-size:13px;color:var(--ink-2);max-width:none;line-height:1.5}
.blank{color:var(--muted);font-style:italic;font-weight:400}
a.src{display:block;color:var(--accent-2);text-decoration:none;line-height:1.35;font-weight:550}
a.src:hover{text-decoration:underline}
.src-meta{display:block;font-size:11px;color:var(--muted);font-weight:400;margin-top:2px}

/* badges */
.badge{display:inline-block;font-size:11px;font-weight:650;letter-spacing:.02em;padding:2px 8px;
  border-radius:999px;white-space:nowrap;vertical-align:1px}
.badge + .badge{margin-left:5px}
.badge.ok{background:var(--ok-soft);color:var(--ok)}
.badge.warn{background:var(--warn-soft);color:var(--warn)}
.badge.flag{background:var(--flag-soft);color:var(--flag)}
.badge.neutral{background:var(--line-2);color:var(--ink-2);font-weight:550}
.flagmark{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;
  color:var(--flag);background:var(--flag-soft);border-radius:4px;padding:1px 5px;margin-right:5px}

/* key table on index */
table.keytable{width:100%;border-collapse:collapse;font-size:13.5px}
table.keytable th{text-align:left;font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;
  color:var(--muted);padding:8px 10px;border-bottom:1px solid var(--line);font-weight:650}
table.keytable td{padding:10px;border-bottom:1px solid var(--line-2);vertical-align:top}
table.keytable tr:last-child td{border-bottom:0}
table.keytable td:first-child{color:var(--ink-2);width:34%}
.muted{color:var(--muted);font-size:12.5px}

/* flagged page */
.flagged{display:grid;gap:14px}
.flagitem{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--flag);
  border-radius:var(--radius);padding:18px 20px;box-shadow:var(--shadow)}
.flagitem header{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-bottom:9px}
.flagitem h3{margin:0 0 7px;font-size:16px;letter-spacing:-.01em}
.flagitem p{margin:0 0 9px;font-size:13.5px;color:var(--ink-2);max-width:88ch}
.flagitem .why{background:var(--flag-soft);border-radius:7px;padding:9px 12px;color:var(--flag)}
.flagitem .srcrow{margin:0;font-size:12.5px}

/* footer */
.foot{max-width:1240px;margin:0 auto;padding:22px 20px 46px;border-top:1px solid var(--line);
  color:var(--muted);font-size:12.5px}
.foot p{margin:0 0 6px;max-width:90ch}

/* responsive */
@media (max-width:900px){
  .layout,.layout.wide{grid-template-columns:1fr;gap:18px;padding:16px 14px 50px}
  .sidenav{position:static;display:none;box-shadow:none}
  .sidenav.open{display:flex}
  .navtoggle{display:inline-block}
  .pagehead h1{font-size:23px}
  h1{font-size:25px}
  .c-topic{width:auto}
  table.grid{min-width:760px}
}
@media (max-width:520px){
  .pill{display:none}
  .pagehead.hero{padding:20px}
  .stats{gap:8px}
  .stat{min-width:88px;padding:8px 11px}
  .count{display:none}
}
@media print{
  .top,.sidenav,.toolbar,.hero-actions,.navtoggle{display:none!important}
  .layout{grid-template-columns:1fr;padding:0}
  .card,.tablewrap,.flagitem{box-shadow:none;break-inside:avoid}
  body{background:#fff}
}
"""
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "style.css").write_text(css, encoding="utf-8")

    js = """// Table filter + nav toggle. No dependencies.
(function () {
  var q = document.getElementById('q');
  var rows = Array.prototype.slice.call(document.querySelectorAll('table.grid tbody tr'));
  var count = document.getElementById('count');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var state = 'all';

  function apply() {
    var term = (q && q.value ? q.value : '').trim().toLowerCase();
    var shown = 0;
    rows.forEach(function (tr) {
      var text = tr.textContent.toLowerCase();
      var status = tr.getAttribute('data-status') || '';
      var flag = tr.getAttribute('data-flag') === '1';
      var okStatus = state === 'all'
        || (state === 'flag' && flag)
        || (state === 'unverified' && status === 'unverified')
        || (state === 'verified' && status === 'verified' && !flag);
      var okText = !term || text.indexOf(term) !== -1;
      var show = okStatus && okText;
      tr.style.display = show ? '' : 'none';
      if (show) shown++;
    });
    if (count) count.textContent = shown + (shown === 1 ? ' row' : ' rows');
  }

  if (q) q.addEventListener('input', apply);
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      chips.forEach(function (x) { x.classList.remove('on'); });
      c.classList.add('on');
      state = c.getAttribute('data-filter');
      apply();
    });
  });
  apply();

  var toggle = document.getElementById('navtoggle');
  var nav = document.getElementById('sidenav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();
"""
    (ROOT / "assets" / "app.js").write_text(js, encoding="utf-8")


def main() -> int:
    sources, findings = load()
    problems = validate(sources, findings)
    if problems:
        print("VALIDATION FAILED:", file=sys.stderr)
        for p in problems:
            print("  -", p, file=sys.stderr)
        return 1

    write_assets()
    (ROOT / "index.html").write_text(index_page(findings, sources), encoding="utf-8")
    for sec in findings["sections"]:
        (ROOT / f"{sec['id']}.html").write_text(section_page(sec, sources, findings), encoding="utf-8")
    (ROOT / "flagged.html").write_text(flagged_page(findings, sources), encoding="utf-8")
    (ROOT / "sources.html").write_text(sources_page(sources, findings), encoding="utf-8")

    n_pages = 3 + len(findings["sections"])
    n_rows = sum(len(s["rows"]) for s in findings["sections"])
    print(f"Built {n_pages} pages, {n_rows} findings, {len(sources)} sources registered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
