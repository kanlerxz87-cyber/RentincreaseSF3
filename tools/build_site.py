#!/usr/bin/env python3
"""Static site generator for the Rental Increase Review (San Francisco, location withheld).

Run:  python3 tools/build_site.py
Outputs: index.html, *.html, data/*.csv|json, research/source-register.md
No third-party dependencies.
"""
import csv
import html
import json
import os
import pathlib

import sitedata as D

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "review"          # this edition lives under /review/ so it never collides with
                               # the two editions other sessions published at the repo root and in docs/.
SITE_TITLE = "Rental Increase Review"
SITE_SUB = "San Francisco (location withheld) - two rent-controlled units"

NAV = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive summary"),
    ("units.html", "Units &amp; coverage"),
    ("requirements.html", "Rules &amp; limits"),
    ("calculations.html", "Calculations"),
    ("notices.html", "Notices"),
    ("fair-housing.html", "One unit or both?"),
    ("practice.html", "Owner practice"),
    ("review.html", "Tenant-lawyer test"),
    ("flagged.html", "Flagged for review"),
    ("sources.html", "Sources"),
    ("../index.html", "All editions"),
]


def esc(s):
    return html.escape(str(s), quote=True)


def money(v):
    return "${:,.2f}".format(v)


def src_links(keys):
    """Render a list of source keys like 'S1, S2' as tiny links into sources.html."""
    parts = []
    for k in [x.strip() for x in keys.split(",") if x.strip()]:
        parts.append(f'<a class="src" href="sources.html#{k.lower()}" title="{esc(D.SOURCES[k]["title"])}">{k}</a>')
    return " ".join(parts)


def table(headers, rows, cls="", filt=False, rowids=None):
    hid = f'<div class="filterbar"><input type="search" data-filter="{id(rows)}" placeholder="Filter rows..."></div>' if filt else ""
    thead = "".join(f"<th>{h}</th>" for h in headers)
    body = []
    for i, r in enumerate(rows):
        rid = f' id="{rowids[i]}"' if rowids else ""
        body.append(f"<tr{rid}>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    return (
        f'<div class="tablewrap{(" " + cls) if cls else ""}">{hid}'
        f'<table data-rows="{id(rows)}"><thead><tr>{thead}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
    )


def callout(kind, title, body):
    return f'<div class="callout {kind}"><strong>{title}</strong><div>{body}</div></div>'


def page(filename, title, lead, body, wide=False):
    links = []
    for href, label in NAV:
        cls = ' class="active"' if href == filename else ''
        links.append(f'<a href="{href}"{cls}>{label}</a>')
    nav = "".join(links)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} - {SITE_TITLE}</title>
<meta name="description" content="Verified rent-increase analysis for two rent-controlled units in San Francisco (location withheld), built only from official sources.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <div class="brand">
      <span class="mark" aria-hidden="true">SF</span>
      <div>
        <div class="brand-title">{SITE_TITLE}</div>
        <div class="brand-sub">{SITE_SUB}</div>
      </div>
      <span class="verified">Verified {D.VERIFIED_ON}</span>
    </div>
    <nav class="mainnav" aria-label="Sections">{nav}</nav>
  </div>
</header>
<main id="main" class="wrap{' wide' if wide else ''}">
  <div class="pagehead">
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </div>
  {body}
</main>
<footer class="foot">
  <div class="wrap">
    <p><strong>Not legal advice.</strong> This site is an information and audit trail prepared from official
    government sources retrieved on {D.VERIFIED_ON}. Every rule and rate is linked to its source on the
    <a href="sources.html">Sources</a> page; items that could not be verified are listed on
    <a href="flagged.html">Flagged for review</a> rather than filled in. Rent-control coverage, prior rent history and
    licensing have not been independently verified. Confirm your specific situation with the
    San Francisco Rent Board (415-252-4600) and a lawyer.</p>
    <p>Personal identifiers are withheld: tenants and units are referred to by placeholder labels only. Dates and
    dollar amounts are shown exactly as provided, because they drive the legal arithmetic.</p>
  </div>
</footer>
<script src="assets/app.js"></script>
</body>
</html>
"""
    OUT.mkdir(exist_ok=True)
    (OUT / filename).write_text(doc, encoding="utf-8")
    return filename


# ---------------------------------------------------------------------------
# shared snippets
# ---------------------------------------------------------------------------
def unit_snapshot_table():
    rows = []
    for u in D.UNITS:
        rows.append([
            f"<strong>{esc(u['label'])}</strong><div class='muted'>{esc(u['type'])}</div>",
            esc(u["tenancy_start"]),
            f"<strong>{money(u['base_rent'])}</strong><div class='muted'>since {esc(u['base_rent_since'])}</div>",
            esc(u["occupants_now"]),
            f'<a class="src" href="flagged.html#f5">F5</a> <span class="muted">owner records</span>',
        ])
    return table(["Unit", "Tenancy start (per owner)", "Current base rent", "Occupants now", "Basis"], rows)


def scenario_table(scenarios, unit_rent):
    rows = []
    for s in scenarios:
        rows.append([
            f"<strong>{esc(s['name'])}</strong>",
            f"{s['pct']:.1f}%",
            money(s["dollars"]),
            f"<strong>{money(s['new_rent'])}</strong>",
            esc(s["notice"]),
            esc(s["effective"]),
            esc(s["note"]) + " " + src_links(s["src"]),
        ])
    return table(["Option", "Increase", "$ / month", "New base rent", "Notice", "Earliest effective", "Notes &amp; sources"], rows)


def must_do_list():
    return """
    <ol class="steplist">
      <li><strong>Confirm coverage.</strong> Pull the property record (year built, unit count, use) and keep a printout.
        Rent control generally attaches to units built on or before 13 June 1979 in a multi-unit building.
        """ + src_links("S5") + """</li>
      <li><strong>Check the rent increase license.</strong> File or refresh the Housing Inventory report; the increase is
        unenforceable without a current license on its effective date. """ + src_links("S6") + """</li>
      <li><strong>Rebuild the lawful rent history.</strong> Original lease, every prior increase notice, proof of service,
        and the rent actually charged. Do not rely on memory. """ + src_links("S11") + """</li>
      <li><strong>Decide the amount.</strong> Either the published annual increase, or the banked total if at least
        24 full months have passed without an increase. """ + src_links("S3, S8") + """</li>
      <li><strong>Serve the right notice, early enough.</strong> 30 days for 10% or less; 90 days for more than 10%;
        5 extra days if mailed. Include the banked breakdown. """ + src_links("S15, S13, S14") + """</li>
      <li><strong>Apply the same rule to both units</strong> and write down the criteria before serving anything.
        """ + src_links("S19, S20, S18") + """</li>
      <li><strong>Keep the file.</strong> Any tenant may petition the Rent Board at no charge and with no time limit.
        """ + src_links("S10, S11") + """</li>
    </ol>"""


# ---------------------------------------------------------------------------
# pages
# ---------------------------------------------------------------------------
def build_index():
    combined_now = sum(u["base_rent"] for u in D.UNITS)
    combined_rec = 4114.85 + 3465.00
    cards = f"""
    <section class="kpis">
      <div class="kpi">
        <div class="kpi-label">Lawful annual cap, 3/1/2026 - 2/28/2027</div>
        <div class="kpi-value">1.6%</div>
        <div class="kpi-note">60% of the Bay Area CPI change; was 1.4% the year before. {src_links("S1, S4, S21")}</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">Unit A - maximum lawful increase</div>
        <div class="kpi-value">{money(119.85)}</div>
        <div class="kpi-note">3.0% = 1.4% banked + 1.6% current, effective 1 Feb 2027. Banking-rule caveat: F1. {src_links("S3, S8")}</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">Unit B - maximum lawful increase</div>
        <div class="kpi-value">{money(412.65)}</div>
        <div class="kpi-note">13.1% of seven banked years; needs 90-day notice. {src_links("S3, S15")}</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">Recommended for Unit B</div>
        <div class="kpi-value">{money(315.00)}</div>
        <div class="kpi-note">10.0% now ($3,465.00), remainder stays banked - inside the pending 10% cap. {src_links("S22")}</div>
      </div>
    </section>
    <section class="twocol">
      <div class="panel">
        <h2>What this site answers</h2>
        <ul class="tight">
          <li>What counts as a reasonable, lawful increase under federal, state and local law.</li>
          <li>How the annual and banked increases actually calculate, to the cent, for each unit.</li>
          <li>How to notify tenants, and what may and may not be said as a reason.</li>
          <li>Whether to raise one unit or both, tested against fair-housing and retaliation law.</li>
          <li>How large owners behave, and how individual owners behave, with links to the primary record.</li>
          <li>A 15-point stress test a tenant-side lawyer would apply.</li>
        </ul>
        <p class="muted">Every rule and rate links to an official source. Anything unverified is blank and listed on
        <a href="flagged.html">Flagged for review</a>.</p>
      </div>
      <div class="panel">
        <h2>Bottom line</h2>
        <p>On the owner's description of the building (1940, two rented units), both units sit under the San Francisco
        Rent Ordinance, so the ceiling is not "market rent" and not the state's 8.8% cap: it is the Rent Board's published annual increase, plus any increases the owner skipped for at
        least 24 months.</p>
        <p>The two units differ because their tenancies started six years apart. That difference is a lawful,
        documentable reason for different dollar increases - and it is also the reason to apply one identical rule to
        both, in writing.</p>
        <p class="muted">Current rent roll: <strong>{money(combined_now)}</strong>/month.
        Under the recommended options: <strong>{money(combined_rec)}</strong>/month (+{money(combined_rec - combined_now)}).</p>
      </div>
    </section>
    """

    snapshot = f"""
    <section>
      <h2>Unit snapshot</h2>
      <p class="muted">Names are replaced with placeholder labels. Dates and amounts are unaltered because the legal
      calculation depends on them.</p>
      {unit_snapshot_table()}
    </section>
    <section>
      <h2>Action plan and deadlines</h2>
      {table(["When", "Action", "Why", "Source"], [
        ["Now", "Pull the property record and the Housing Inventory / licence status.",
         "Coverage and licensing decide whether any increase is enforceable at all.", src_links("S5, S6")],
        ["Now", "Assemble the rent history file for both units.",
         "A tenant petition has no filing fee and no time limit; the owner carries the arithmetic burden.", src_links("S10, S11")],
        ["By 2026-12-28", "Serve Unit A notice for a 1 Feb 2027 effective date (30 days, or 35 if mailed).",
         "Preserves the 1 February anniversary and captures 1.4% + 1.6%.", src_links("S2, S9")],
        ["By 2026-11-30", "Serve Unit B notice if the full 13.1% is wanted (90 days to 28 Feb 2027).",
         "The 1.6% rate year ends 28 Feb 2027; after that the 2026-27 rate is no longer the current annual rate.", src_links("S15, S4")],
        ["Before service", "Re-check Legistar File 261020 (pending 10% cap).",
         "A cap on banked increases could apply to notices served after 15 Sep 2026 if enacted.", src_links("S22")],
        ["Every year", "File the Housing Inventory report by 1 March; review the new rate each March.",
         "The allowable increase changes every 1 March and the licence must stay current.", src_links("S6, S4")],
      ])}
    </section>
    <section>
      <h2>Seven findings</h2>
      <ol class="findings">
        <li><strong>The local cap governs, not the state cap.</strong> AB 1482 exempts housing already limited by a
        stricter local ordinance; the state ceiling for this region would be 8.8% for increases starting between
        1 Aug 2026 and 31 Jul 2027. {src_links("S16, S21")}</li>
        <li><strong>The current lawful annual increase is 1.6%.</strong> On $3,995 that is $63.92; on $3,150 it is
        $50.40. {src_links("S1, S4")}</li>
        <li><strong>Unit A has a fresh tenancy.</strong> Because the lease began 1 Feb 2025, the first increase could
        not be imposed before 1 Feb 2026, and nothing was imposed - so one 1.4% year is now available to add to the
        1.6%: 3.0%, or $119.85. {src_links("S2, S3")}</li>
        <li><strong>The April 2026 co-tenant adds nothing.</strong> San Francisco prohibits extra rent solely because
        an additional occupant moved in, even where the lease says otherwise. {src_links("S2, S13")}</li>
        <li><strong>Unit B has banked seven years.</strong> 1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 + 1.6 = 13.1%, i.e.
        $412.65, but that is a large single step and it crosses the 10% threshold for longer notice. {src_links("S3, S4, S15")}</li>
        <li><strong>Process decides enforceability.</strong> Licence, 12-month spacing, correct notice length, and a
        notice that breaks out the banked portion by year are all prerequisites, not formalities. {src_links("S6, S14")}</li>
        <li><strong>The timing window matters.</strong> Any increase that relies on the 1.6% rate must take effect on or
        before 28 Feb 2027; 90 days' notice means Unit B must be served by 30 Nov 2026 at the latest. {src_links("S15, S1")}</li>
      </ol>
    </section>
    <section>
      <h2>Go deeper</h2>
      <div class="cards">
        <a class="card" href="executive-summary.html"><span>Executive summary</span><em>One page for a decision-maker.</em></a>
        <a class="card" href="requirements.html"><span>Rules &amp; limits</span><em>Federal, state and local rows, each with its source.</em></a>
        <a class="card" href="calculations.html"><span>Calculations</span><em>The arithmetic, per anniversary date, to the cent.</em></a>
        <a class="card" href="notices.html"><span>Notices</span><em>Deadlines, required contents, and a model letter.</em></a>
        <a class="card" href="fair-housing.html"><span>One unit or both?</span><em>Discrimination and retaliation risk, tested.</em></a>
        <a class="card" href="review.html"><span>Tenant-lawyer test</span><em>15 checks an advocate or ALJ would run.</em></a>
      </div>
    </section>
    """
    body = callout(
        "warn",
        "Read this first",
        "Two official descriptions of the banking rule disagree (12 months vs 24 months), a 10% cap on banked increases "
        "is pending at the Board of Supervisors, and neither the property record nor the rent-increase licence has been "
        "verified. All three are documented on <a href='flagged.html'>Flagged for review</a>; the calculations show a "
        "lawful-under-every-reading fallback.",
    ) + cards + snapshot + must_do_block() + findings_block()
    return page("index.html", "Rental increase review dashboard",
                "A single-page view of what two rent-controlled San Francisco units may lawfully be charged, "
                "what notice is required, and what still needs verifying.", body)


def must_do_block():
    return f"""
    <section>
      <h2>Required steps before any notice is served</h2>
      {must_do_list()}
    </section>"""


def findings_block():
    return """
    <section>
      <h2>How to read the tables</h2>
      <p>Each row that states a rule, a rate or a calculation carries source tags such as
      <a class="src" href="sources.html#s1">S1</a>. Click a tag to jump to the source register, which quotes the
      relevant passage and links to the official page. Where a value could not be confirmed from an official source it
      is left blank - never estimated - and recorded on <a href="flagged.html">Flagged for review</a>.</p>
    </section>"""


def build_exec():
    body = f"""
    <section class="exec">
      <h2>Purpose</h2>
      <p>The owner of two flats in a 1940 building in San Francisco (location withheld) asked what a reasonable
      and normal rent increase looks like, whether it would survive review by a tenant-side advocate or lawyer, and
      whether to raise one unit or both. This site records the official-source answer, the arithmetic, the notice
      procedure, and the open items.</p>

      <h2>1. The ceiling is set locally, and it is small</h2>
      <p>Both units are rent-controlled on the owner's description: the building predates 13 June 1979. Because a tenant
      from each original tenancy remains in possession, no vacancy has occurred, so neither rent can be reset to
      market. The allowable annual increase is
      set each 1 March at 60% of the prior year's Bay Area CPI change, capped at 7%.</p>
      <ul>
        <li><strong>3/1/2026 - 2/28/2027: 1.6%</strong> {src_links("S1, S4, S7")}</li>
        <li><strong>3/1/2025 - 2/28/2026: 1.4%</strong> {src_links("S1, S4")}</li>
        <li>Average of the last eight published years: 1.96% (2.6, 1.8, 0.7, 2.3, 3.6, 1.7, 1.4, 1.6) {src_links("S4")}</li>
      </ul>
      <p>The statewide Tenant Protection Act is not the operative rule: it caps increases at 5% + CPI (8.8% for this
      region for 1 Aug 2026 - 31 Jul 2027), but it exempts housing already subject to a local ordinance that restricts
      increases to a lower amount. {src_links("S16, S21")} No federal statute sets a rent ceiling; the federal rule
      that does apply to increase decisions is the Fair Housing Act's ban on discriminatory terms. {src_links("S20")}</p>

      <h2>2. Skipped years can be added, subject to a 24-month condition</h2>
      <p>If the owner does not take an increase, the unused amount can be banked and taken later. The Rent Board's
      current guidance requires <strong>at least 24 full months without any rent increase</strong> before a skipped
      increase is treated as banked; percentages are added, never compounded, and never rounded up. There is no ceiling
      on the banked total, and banked amounts do not expire during the tenancy. {src_links("S3, S8, S14")}</p>

      <h2>3. Unit A - $3,995, tenancy from 1 Feb 2025</h2>
      <p>The first increase could not be imposed before 1 Feb 2026 (1.4%), and none was imposed. On 1 Feb 2027 the
      owner is 24 months without an increase, so both years are available: <strong>1.4% + 1.6% = 3.0% = $119.85</strong>,
      taking base rent to <strong>$4,114.85</strong>. A 30-day notice is enough because 3.0% is well under 10%.</p>
      <p>The 1 April 2026 renewal, at which a second tenant joined the original tenant, does <em>not</em> create a
      vacancy and does <em>not</em> allow extra rent: San Francisco prohibits additional rent solely because an
      occupant moved in. {src_links("S2, S13, S17")}</p>
      <p>Conservative fallback: if a counselor reads the 24-month condition narrowly, the current 1.6% alone is
      $63.92, taking rent to $4,058.92. {src_links("S2")}</p>

      <h2>4. Unit B - $3,150, tenancy from 1 Jun 2019, no increase since</h2>
      <p>Seven anniversary increases have been skipped, and the 24-month condition is met many times over. The
      percentages in effect on each anniversary (June 2020 through June 2026) are 1.8, 0.7, 2.3, 3.6, 1.7, 1.4 and
      1.6: <strong>13.1% = $412.65</strong>, taking base rent to <strong>$3,562.65</strong>. Because the increase
      exceeds 10%, a <strong>90-day</strong> notice is required. {src_links("S3, S4, S15")}</p>
      <p>Two cautions. First, the 1.6% year ends 28 Feb 2027, so a notice relying on it must be served by 30 Nov 2026.
      Second, a pending ordinance (File 261020) would cap combined banked and capital-improvement increases at 10% per
      year; it is not law yet, but an increase of exactly 10% ($315.00, to $3,465.00) is lawful today, would remain
      lawful if the cap passes, and leaves $97.65 banked. {src_links("S22, S3")}</p>

      <h2>5. Reasonable and normal</h2>
      <p>For a rent-controlled San Francisco unit, "reasonable and normal" means: the published annual percentage,
      applied on the anniversary date, with correct notice and a current licence. That is what the ordinance
      contemplates and what the Rent Board's own examples show. A banked catch-up is also lawful, but it is the
      practice that tenant advocates and the Board of Supervisors are actively targeting, it draws petitions, and after
      the pending cap it may be limited to 10% a year. There is no legal requirement to raise rent at all, and no
      requirement that both units be raised.</p>

      <h2>6. One unit or both?</h2>
      <p>Nothing in the ordinance or in fair-housing law requires equal dollar increases. Raising only one unit is not
      unlawful by itself; unlawful treatment arises when the difference is tied to a protected characteristic or to
      retaliation. The defensible pattern is to adopt one written rule (for example: "the annual allowable increase, or
      the banked total if 24 months have passed"), apply it to both units on the same schedule, and document the
      tenancy-history reason for any difference. Applying different rules to similarly placed tenants is what invites
      inquiry. {src_links("S19, S20, S18")}</p>

      <h2>7. What must still be verified</h2>
      <ul>
        <li>Property record (year built, unit count, use) - coverage is argued from the owner's statement. {src_links("S5")}</li>
        <li>Housing Inventory report and current rent increase licence. {src_links("S6")}</li>
        <li>Prior notices, leases and proofs of service for both units. {src_links("S11")}</li>
        <li>Status of the pending 10% cap. {src_links("S22")}</li>
        <li>The 12-vs-24-month banking discrepancy between two official pages. {src_links("S3, S14")}</li>
      </ul>
      <p>All five are on <a href="flagged.html">Flagged for review</a> with what would close them.</p>
    </section>
    """
    return page("executive-summary.html", "Executive summary",
                "The decision, the numbers, and the risks - on one page.", body)


def build_units():
    rows = []
    for u in D.UNITS:
        rows.append([
            esc(u["label"]),
            esc(u["type"]),
            esc(u["tenancy_start"]),
            money(u["base_rent"]),
            esc(u["history_note"]),
            f'<a class="src" href="flagged.html#f5">F5</a> <span class="muted">owner records, unverified</span>',
        ])
    coverage = table(["Question", "Answer", "Status", "Source"], [
        ["Was the building built on or before 13 June 1979?", "Owner states 1940.", "<span class='tag ok'>supports coverage</span>", src_links("S5")],
        ["Is it a multi-unit residential building rather than a single-family dwelling or condo?",
         "Two units are described, both rented.", "<span class='tag ok'>supports coverage</span>", src_links("S5")],
        ["Does a local ordinance cap increases more tightly than AB 1482?",
         "Yes - 1.6% versus the state's 8.8% for the current state year.", "<span class='tag ok'>verified</span>", src_links("S16, S21")],
        ["Has any exemption been claimed (new construction, substantial rehabilitation, subsidy)?",
         "", "<span class='tag bad'>unverified - F6/F8</span>", src_links("S5")],
        ["Is the unit reported in the Housing Inventory with a current licence?",
         "", "<span class='tag bad'>unverified - F7</span>", src_links("S6")],
        ["What was the lawful base rent before the current tenancy?", "", "<span class='tag bad'>unverified - F5</span>", src_links("S11")],
    ])
    body = f"""
    {callout("info", "Privacy by design",
      "Personal names are not stored in this repository. Units and tenants are referred to by placeholder labels; the "
      "key that maps labels to real names is deliberately not kept here. Dates and amounts are shown unchanged, because "
      "the lawful increase cannot be computed without them.")}
    <section>
      <h2>Anonymised unit record</h2>
      {table(["Unit", "Type", "Tenancy start", "Current base rent", "History supplied", "Basis"], rows)}
    </section>
    <section>
      <h2>Coverage determination</h2>
      <p>San Francisco rent control attaches to most residential units in buildings with a certificate of occupancy on
      or before 13 June 1979, and limits increases during a continuing tenancy; the rent can be reset only once the
      unit is vacant and no tenant from the prior tenancy remains. Building age is the owner's statement, so the
      determination below is <em>provisional</em> until the property record is pulled.
      {src_links("S5, S13")}</p>
      {coverage}
    </section>
    <section>
      <h2>Why Unit A did not become a new tenancy in April 2026</h2>
      <p>Vacancy decontrol applies to a new tenancy in which no tenant from the prior tenancy remains in lawful
      possession (Civ. Code 1947.12(b); Costa-Hawkins, Civ. Code 1954.52). On 1 April 2026 one of the original Unit A
      tenants was still in place, with a co-tenant added, so the tenancy continued; the rent therefore stayed at its
      lawful level and did not reset. {src_links("S16, S17, S13")}</p>
      <p>The addition of the co-tenant is not a rentable event in San Francisco: the ordinance prohibits increases
      imposed solely because a tenant added an occupant, and states that this applies even where the lease expressly
      allows a charge for additional occupants. {src_links("S2, S13")}</p>
    </section>
    <section>
      <h2>Facts intentionally not filled in</h2>
      <p>Square footage, bedroom count, whether utilities are included, whether parking or storage is part of base rent,
      security deposit amounts, and any prior rent notices are all unknown. Each affects either the arithmetic or the
      comparison, so none has been assumed. See <a href="flagged.html">Flagged for review</a>.</p>
    </section>"""
    return page("units.html", "Units and coverage",
                "What is known about each unit, what the law requires to be true for rent control to apply, and what "
                "remains unverified.", body)


def build_requirements():
    rows = []
    for layer, req, meaning, src in D.REQUIREMENTS:
        rows.append([f"<strong>{esc(layer)}</strong>", esc(req), esc(meaning), src_links(src)])
    body = f"""
    <section>
      <h2>Federal, state and local rules that govern these two increases</h2>
      <p>Twenty-one rows, each tied to statute text or to a government publication. Rows describing what applies to
      these specific units are analysis; the rule itself is always linked.</p>
      {table(["Layer", "Rule", "What it means here", "Source"], rows, filt=True)}
    </section>
    <section>
      <h2>How the three layers fit together</h2>
      <div class="stack">
        <div class="layer"><span class="layer-tag">Federal</span>
          <p>No rent ceiling. The binding federal rules are non-discrimination in rental terms
          (42 U.S.C. 3604) and antitrust limits on algorithmic rent-setting, which San Francisco has also banned
          locally. {src_links("S20, S24, S23")}</p></div>
        <div class="layer"><span class="layer-tag">State</span>
          <p>Sets the outer limit and the notice mechanics: 5% + CPI capped at 10% under AB 1482, displaced here by the
          stricter local cap; 30/90-day notice under Civil Code 827; no retaliation under Civil Code 1942.5; no
          discrimination under Government Code 12955. {src_links("S16, S21, S15, S18, S19")}</p></div>
        <div class="layer"><span class="layer-tag">Local</span>
          <p>Sets the number that actually applies: 1.6% for 3/1/2026-2/28/2027, banked years added on top, one increase
          per 12 months, licence required, base rent only, no rounding, no charge for additional occupants.
          {src_links("S1, S3, S6, S2")}</p></div>
      </div>
    </section>
    <section>
      <h2>Notice-period arithmetic</h2>
      {table(["Increase size", "Minimum written notice", "If served by mail", "Source"], [
        ["10% or less (alone or combined with other increases in the prior 12 months)", "30 days", "35 days",
         src_links("S15, S2")],
        ["More than 10%", "90 days", "95 days", src_links("S15, S2")],
      ])}
      <p class="muted">Civil Code 827 measures the 10% against the rent charged at any time in the 12 months before the
      effective date, and requires personal delivery or mail service under Code of Civil Procedure 1013. The Rent Board
      expresses the same rule as "5 more days if the notice is mailed". {src_links("S15, S2")}</p>
    </section>"""
    return page("requirements.html", "Rules and limits",
                "Every federal, state and local requirement that touches a rent increase on these units, with the "
                "official source for each.", body, wide=True)


def build_calculations():
    def ledger_rows(unit, rows, rent):
        out = []
        for anniv, period, pct, status, src in rows:
            dollars = round(rent * pct / 100, 2)
            out.append([
                esc(anniv),
                esc(period),
                f"{pct:.1f}%",
                money(dollars),
                esc(status),
                f"{money(rent)} &times; {pct/100:.3f} = {money(dollars)}",
                src_links(src),
            ])
        return out

    a_rows = ledger_rows("A", D.LEDGER_A, 3995.00)
    b_rows = ledger_rows("B", D.LEDGER_B, 3150.00)

    b_total = round(sum(3150 * p / 100 for _, _, p, _, _ in D.LEDGER_B), 2)
    a_pct = sum(p for _, _, p, _, _ in D.LEDGER_A)

    body = f"""
    {callout("info", "Rules applied to every line",
      "One increase per 12 months; percentages are added, never compounded; the percentage applied is the one in effect "
      "on the effective date of the increase; the calculation is on base rent only; no rounding up to the nearest "
      "dollar. " + src_links("S2, S3, S8, S9"))}

    <section>
      <h2>Unit A - $3,995.00 base rent, tenancy began 1 Feb 2025</h2>
      <p>Because the tenancy began on 1 Feb 2025, the earliest possible increase was 1 Feb 2026 (the first anniversary), at the rate then in
      effect (1.4%). No increase was imposed. By 1 Feb 2027 the unit has gone 24 full months without an increase, which
      is the Rent Board's condition for treating a skipped year as banked. {src_links("S2, S3, S9")}</p>
      {table(["Anniversary date", "Rate period in effect", "Rate", "$ on $3,995", "Status", "Arithmetic", "Source"], a_rows)}
      <div class="sums">
        <div><span>Banked 1.4% + current 1.6%</span><strong>{a_pct:.1f}%</strong></div>
        <div><span>Dollar increase</span><strong>{money(round(3995*a_pct/100,2))}</strong></div>
        <div><span>New base rent</span><strong>{money(round(3995*(1+a_pct/100),2))}</strong></div>
      </div>
      <h3>Options</h3>
      {scenario_table(D.SCENARIOS_A, 3995.00)}
      <p class="muted">Increase must take effect on or before 28 Feb 2027 to use the 1.6% rate. A 30-day notice (35 if
      mailed) means serving by 2 Jan 2027, or 28 Dec 2026 if mailed. {src_links("S15, S4")}</p>
      <p class="muted">The April 2026 co-tenant is not a factor in any line above, and cannot be. {src_links("S2, S13")}</p>
    </section>

    <section>
      <h2>Unit B - $3,150.00 base rent, tenancy began 1 Jun 2019</h2>
      <p>No increase has been imposed since the tenancy began. Each June anniversary from 2020 to 2026 therefore
      produced an unused annual increase, and the 24-month condition is met many times over. The seven percentages add
      to 13.1%. {src_links("S3, S4, S8")}</p>
      {table(["Anniversary date", "Rate period in effect", "Rate", "$ on $3,150", "Status", "Arithmetic", "Source"], b_rows)}
      <div class="sums">
        <div><span>Banked (2020-2025)</span><strong>11.5% = {money(362.25)}</strong></div>
        <div><span>Current annual 2026-27</span><strong>1.6% = {money(50.40)}</strong></div>
        <div><span>Total</span><strong>13.1% = {money(b_total)}</strong></div>
        <div><span>New base rent</span><strong>{money(3150 + b_total)}</strong></div>
      </div>
      <h3>Options</h3>
      {scenario_table(D.SCENARIOS_B, 3150.00)}
      <div class="twocol">
        <div class="panel">
          <h3>Timing window</h3>
          <p>To use the 1.6% rate the increase must take effect on or before 28 Feb 2027. With a 90-day notice, service
          must happen by <strong>30 Nov 2026</strong> (25 Nov 2026 if mailed). Served on 6 Nov 2026, the earliest lawful
          effective date is 4 Feb 2027 (9 Feb 2027 if mailed). {src_links("S15")}</p>
          <p>Waiting instead for the 1 Jun 2027 anniversary would add the 2027-28 annual rate, which the Rent Board will
          publish by 1 Mar 2027 and which cannot be stated today. {src_links("S4")}</p>
        </div>
        <div class="panel">
          <h3>If the 10% cap passes</h3>
          <p>File 261020 would limit combined banked and capital-improvement increases to 10% per year for three years.
          It is not law on {D.VERIFIED_ON}. Option B2 (10.0%, $315.00) is lawful now and would stay lawful if the cap
          is enacted; B3 (13.1%) could be reduced. {src_links("S22")}</p>
        </div>
      </div>
    </section>

    <section>
      <h2>Side-by-side</h2>
      {table(["Measure", "Unit A", "Unit B", "Why", "Source"], [
        ["Current base rent", money(3995.00), money(3150.00), "Set at the start of each tenancy.",
         '<a class="src" href="flagged.html#f5">F5</a>'],
        ["Tenancy start", "2025-02-01", "2019-06-01", "Drives which years are available.",
         '<a class="src" href="flagged.html#f5">F5</a>'],
        ["Available years", "2 (1.4% + 1.6%)", "7 (1.8 ... 1.6)", "Anniversary dates since the last increase." + " " + src_links("S4")],
        ["Maximum lawful increase", "3.0% = " + money(119.85), "13.1% = " + money(412.65), "Percentages added, not compounded." + " " + src_links("S3")],
        ["Resulting base rent", money(4114.85), money(3562.65), "Base rent + increase.", src_links("S3, S8")],
        ["Notice required", "30 days", "90 days", "Civil Code 827: more than 10% needs 90 days." + " " + src_links("S15")],
        ["Recommended option", "A2 - 3.0% (" + money(119.85) + ")", "B2 - 10.0% (" + money(315.00) + ")",
         "Captures what is clearly available, stays inside the pending cap, keeps the rest banked.",
         src_links("S3, S22")],
      ])}
      <p class="muted">Note the ordering effect: Unit A's rent is already $845 higher than Unit B's. Even after the
      recommended increases the ordering is unchanged ($4,114.85 vs $3,465.00), which is relevant to the fair-housing
      analysis on <a href="fair-housing.html">One unit or both?</a></p>
    </section>

    <section>
      <h2>Verification of the arithmetic</h2>
      <ul class="checklist">
        <li>Percentages taken from the Rent Board's published table, not from memory. {src_links("S4")}</li>
        <li>Each percentage matched to the rate period in effect on that anniversary date. {src_links("S2, S9")}</li>
        <li>Simple addition, no compounding: 1.4 + 1.6 = 3.0; 1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 + 1.6 = 13.1. {src_links("S3, S8")}</li>
        <li>Dollar amounts are base rent x summed percentage, computed once; cents kept, nothing rounded up. {src_links("S2")}</li>
        <li>Cross-checked against the Rent Board's own multi-year worked example and the 6.7% banked example. {src_links("S8, S3")}</li>
      </ul>
    </section>"""
    return page("calculations.html", "Calculations",
                "The lawful ceiling for each unit, anniversary by anniversary, with the arithmetic shown so it can be "
                "re-checked line by line.", body, wide=True)


def build_notices():
    elems = [[esc(a), esc(b), src_links(c)] for a, b, c in D.NOTICE_ELEMENTS]
    body = f"""
    <section>
      <h2>The four things that make a notice enforceable</h2>
      <div class="cards four">
        <div class="card static"><span>1. A current licence</span><em>Housing Inventory report filed; licence live on the effective date. {src_links("S6")}</em></div>
        <div class="card static"><span>2. The right amount</span><em>Published annual rate plus properly banked years, on base rent, unrounded. {src_links("S1, S3")}</em></div>
        <div class="card static"><span>3. The right interval</span><em>At least 12 months since the last increase, and 24 months without an increase for banking. {src_links("S2, S3")}</em></div>
        <div class="card static"><span>4. The right notice</span><em>30 days for 10% or less, 90 days for more, served personally or by mail, with the required content. {src_links("S15, S14")}</em></div>
      </div>
    </section>

    <section>
      <h2>Required contents of the notice</h2>
      {table(["Element", "What to include", "Source"], elems)}
      <p class="muted">Civil Code 827 governs the length and service of the notice; Rent Ordinance 37.3(b) and Rent Board
      Rule 4.10 add the content requirements for annual and banked increases. {src_links("S15, S13, S14")}</p>
    </section>

    <section>
      <h2>Deadline planner for the two units</h2>
      {table(["Unit", "Increase", "Notice length", "Serve by", "Earliest effective", "Notes"], [
        ["A", "3.0% (" + money(119.85) + ")", "30 days", "2 Jan 2027 (28 Dec 2026 if mailed)", "1 Feb 2027",
         "Preserves the 1 February anniversary. " + src_links("S15, S2")],
        ["A - fallback", "1.6% (" + money(63.92) + ")", "30 days", "2 Jan 2027 (28 Dec 2026 if mailed)", "1 Feb 2027",
         "Only the current annual increase; lawful under every reading. " + src_links("S2")],
        ["B", "10.0% (" + money(315.00) + ")", "30 days (10% or less)",
         "At least 30 days before the effective date (service on 6 Nov 2026 supports 6 Dec 2026)",
         "6 Dec 2026 at the earliest", "Leaves 3.1% banked. " + src_links("S15, S3")],
        ["B", "13.1% (" + money(412.65) + ")", "90 days", "30 Nov 2026 (25 Nov 2026 if mailed)", "28 Feb 2027 at the latest",
         "Only this window keeps the 1.6% as the current annual rate. " + src_links("S15, S4")],
      ])}
    </section>

    <section>
      <h2>Model notice (placeholders only)</h2>
      <div class="letter">
        <p class="letter-meta">[Date] &middot; Served on [tenant label] by [personal delivery / first-class mail]</p>
        <p><strong>NOTICE OF RENT INCREASE</strong></p>
        <p>To: [Tenant label], [Unit label], San Francisco, CA [ZIP]</p>
        <p>Under the San Francisco Residential Rent Stabilization and Arbitration Ordinance (Administrative Code
        Chapter 37) and California Civil Code section 827, your base rent will change as follows.</p>
        <table class="mini">
          <tr><td>Current base rent</td><td>$[amount] per month</td></tr>
          <tr><td>Annual increase at the Rent Board's rate for [rate period]</td><td>[x.x]% = $[amount]</td></tr>
          <tr><td>Banked increase: [anniversary date(s)]</td><td>[x.x]% = $[amount]</td></tr>
          <tr><td>Total increase</td><td>[x.x]% = $[amount]</td></tr>
          <tr><td>New base rent effective [date]</td><td>$[amount] per month</td></tr>
        </table>
        <p>The increase is calculated on base rent only, using the percentages published by the San Francisco Rent
        Board (document 571); percentages are added and not compounded, and the amount is not rounded up.</p>
        <p>This increase takes effect at least [30/90] days after service, as required by Civil Code section 827, and at
        least 12 months after your last increase.</p>
        <p>If you believe this increase is unlawful, you may contact the San Francisco Rent Board at 415-252-4600, or
        file a tenant petition at no charge; there is no time limit for filing. [Adjust this sentence if you prefer not
        to include it - it is not legally required, but it reduces the risk of a harassment or retaliation claim.]</p>
        <p>[Owner name / agent] &middot; [Contact] &middot; Rent increase licence: [confirmation reference]</p>
      </div>
      <p class="muted">The model text is a starting point built strictly from the required elements above. It is not
      legal advice and should be reviewed before use. {src_links("S13, S14, S15, S2")}</p>
    </section>

    <section>
      <h2>Reasonable reasons - what the law does and does not require</h2>
      <p>The ordinance authorises the annual and banked increase by formula. Neither the ordinance text nor the Rent
      Board guidance requires the owner to give a reason, and the Rent Board's worked examples contain no justification
      step. {src_links("S13, S2, S8")} Reasons become mandatory only when the owner seeks more than the annual
      allowance - for example a capital-improvement or operating-and-maintenance petition, which is decided on evidence
      by an Administrative Law Judge. {src_links("S10, S11")}</p>
      {table(["If asked, say this", "Do not say this", "Why"], [
        ["The increase is the Rent Board's published annual allowable increase for the rate period stated, plus banked "
         "years the ordinance allows; the notice shows the calculation.",
         "Anything about the tenant's family, immigration status, source of income, disability, age, or who else lives "
         "in the unit.",
         "Those are protected characteristics under Government Code 12955 and 42 U.S.C. 3604. " + src_links("S19, S20")],
        ["The rent has not been adjusted since [date] and the banked amounts are now being taken, as the Rent Board "
         "guidance permits.",
         "That the increase is because the tenant complained, requested repairs, joined a tenant association or filed a "
         "petition.",
         "Retaliatory increases are unlawful, with a 180-day presumption after protected activity. " + src_links("S18")],
        ["Operating costs, insurance and maintenance have risen - as context, not as the legal basis.",
         "That the increase will be larger unless the tenant does something, or that a new roommate triggered it.",
         "Increases for additional occupants are prohibited outright. " + src_links("S2, S13")],
      ])}
      <p class="muted">Reasons are not the mechanism of compliance; the calculation, licence, timing and notice are. A
      stated reason that is inconsistent with the file is worse than no reason at all.</p>
    </section>"""
    return page("notices.html", "Informing tenants",
                "What to serve, when to serve it, exactly what the notice must say, and what is safe - and unsafe - to "
                "give as a reason.", body)


def build_fair():
    body = f"""
    <section>
      <h2>The question</h2>
      <p class="big">Is it acceptable to raise the rent on one unit, or is it safer to raise both so that no
      discrimination claim can be made?</p>
      <p>Short answer: neither choice is required by law, and neither is automatically safer. What protects the owner
      is a <strong>written, objective rule applied consistently and documented before it is applied</strong>. A
      difference in outcome is lawful when it follows from a difference in facts - here, seven years of skipped
      increases in Unit B versus two in Unit A. A difference in <em>treatment</em> between similarly placed tenants is
      what invites inquiry.</p>
    </section>

    <section>
      <h2>What the law actually prohibits</h2>
      {table(["Legal rule", "Prohibits", "Does not prohibit", "Source"], [
        ["Government Code 12955 (state)",
         "Discriminating or harassing a tenant because of race, colour, religion, sex, gender identity, sexual "
         "orientation, marital status, national origin, ancestry, familial status, source of income, disability, "
         "veteran/military status or genetic information.",
         "Different dollar increases that follow from different tenancy dates, base rents or documented rent histories.",
         src_links("S19")],
        ["42 U.S.C. 3604 (federal)",
         "Discriminating in the terms, conditions or privileges of a rental because of race, colour, religion, sex, "
         "familial status or national origin (and disability under subsection (f)).",
         "Applying the ordinance's formula unit by unit.",
         src_links("S20")],
        ["Civil Code 1942.5 (retaliation)",
         "Increasing rent in retaliation for repair or habitability complaints, inspections, arbitration, or protected "
         "organising (180-day presumption).",
         "A scheduled annual increase that would have happened anyway.",
         src_links("S18")],
        ["Rent Ordinance 37.3 (amount)",
         "Increases above the annual allowance, extra rent for additional occupants, more than one increase in 12 months.",
         "Taking the annual increase on one unit and not the other.",
         src_links("S13, S2")],
      ])}
    </section>

    <section>
      <h2>Risk comparison</h2>
      {table(["Approach", "Lawful?", "Fair-housing exposure", "Retaliation exposure", "Practical verdict", "Source"], [
        ["Raise both units by the annual allowable rate only",
         "Yes",
         "Low - identical treatment, identical rule.",
         "Low.",
         "<span class='tag ok'>Safest</span> but captures only 1.6% on Unit B and leaves 11.5% banked.", src_links("S2, S3")],
        ["Raise only the unit with the banked history (Unit B) by a larger amount",
         "Yes, if noticed and licensed",
         "Low to moderate - the difference is explained by tenancy history, but differential treatment between "
         "households in the same building is the fact pattern that draws complaints.",
         "Moderate if either household has recently made complaints.",
         "Defensible with documentation; see the written-rule approach below.", src_links("S3, S19, S20")],
        ["Raise only one unit, with no written rule and no rent history on file",
         "Unclear in practice",
         "Moderate - no contemporaneous explanation for the difference.",
         "Moderate.",
         "<span class='tag bad'>Avoid</span>.", src_links("S19, S20, S18")],
        ["Raise both, with a written rule, retroactive rent histories and matching notices",
         "Yes",
         "Lowest - the reason for any difference is in the file before the increase.",
         "Low.",
         "<span class='tag ok'>Recommended</span>", src_links("S2, S14, S19")],
      ])}
      <p class="muted">Nothing in the ordinance or the cited statutes requires equal percentage or equal dollar
      increases, and no official source requires an owner to raise rent on every unit. The risk management is
      evidentiary, not numerical.</p>
    </section>

    <section>
      <h2>How to document it in one page</h2>
      <ol class="steplist">
        <li>Write the rule before serving anything: for example, "each year the owner applies the Rent Board's annual
        allowable increase on each unit's anniversary date, and takes banked years where at least 24 months have passed
        without an increase." {src_links("S2, S3")}</li>
        <li>Record each unit's tenancy start, base rent, and every prior increase (date, percentage, dollar amount,
        notice and proof of service). {src_links("S11")}</li>
        <li>Show the calculation for each unit, including the rate period used. {src_links("S4")}</li>
        <li>Serve both notices on the same schedule, using the same template, so the only difference between them is the
        arithmetic. {src_links("S14")}</li>
        <li>If a decision is made to raise one unit and not the other, write down the reason (for example: recent
        hardship, a repair dispute being resolved, a pending lease change) and keep it. A reason recorded at the time is
        evidence; a reason reconstructed later is not.</li>
        <li>Never make a protected characteristic, a complaint, or a request for repairs part of the reasoning.
        {src_links("S18, S19, S20")}</li>
      </ol>
    </section>

    <section>
      <h2>If a tenant raises it</h2>
      <p>The Rent Board does not adjudicate discrimination, harassment or retaliation; those claims go to court or
      another forum. {src_links("S10")} The Rent Board does adjudicate whether the amount was lawful, at no charge and
      with no time limit. {src_links("S11")} That split matters: the arithmetic file answers the Rent Board; the written
      rule and the consistency record answer the discrimination question.</p>
    </section>"""
    return page("fair-housing.html", "One unit or both?",
                "Whether to raise one unit or both, tested against fair-housing, retaliation and Rent Ordinance rules - "
                "and what documentation makes either choice defensible.", body)


def build_practice():
    body = f"""
    <section>
      <h2>Two different operating models, one set of rules</h2>
      <p>Institutional owners and individual owners face the same ordinance. What differs is process: scale,
      standardisation and the presence of pricing software and counsel. The table separates what is documented in
      official sources from what is general practice (labelled as such).</p>
      {table(["Dimension", "Large institutional owner", "Individual owner (two-unit building)", "Evidence status"], [
        ["Which cap applies",
         "The same local cap for covered pre-1979 buildings; the state cap only for buildings outside local rent control.",
         "The same local cap for covered pre-1979 buildings.",
         "Verified " + src_links("S16, S21, S5")],
        ["Annual increase practice",
         "Take the published annual increase on each unit's anniversary, applied portfolio-wide on a common calendar.",
         "Often the same, but frequently skipped to keep a good tenant - which builds a bank.",
         "Practice, not a legal requirement " + src_links("S2, S3")],
        ["Banked increases",
         "Tracked in property-management systems and typically taken on turnover or on a scheduled catch-up.",
         "Usually tracked informally or not at all; the 24-month condition is easily missed.",
         "Rule verified; practice is inference " + src_links("S3")],
        ["Pricing method",
         "Historically used revenue-management software that ingests competitors' non-public data; San Francisco "
         "banned algorithmic rent-setting devices in 2024, and the DOJ has pursued the largest vendor and several large "
         "landlords.",
         "Comparable listings and judgement.",
         "Verified " + src_links("S23, S24")],
        ["Notice production",
         "Standard templates, proof-of-service routines, licence checks, counsel review.",
         "A letter, often without the banked breakdown or proof of service.",
         "Rule verified; practice is inference " + src_links("S14, S15")],
        ["Dispute posture",
         "Responds to Rent Board petitions with records and counsel; litigation budget exists.",
         "Often resolves informally, or concedes arithmetic errors.",
         "Inference from the petition process " + src_links("S10, S11")],
        ["Transparency burden",
         "Housing Inventory reporting, licence status visible to tenants in the portal.",
         "Same obligation - and tenants can check licence status themselves.",
         "Verified " + src_links("S6")],
      ])}
    </section>

    <section>
      <h2>What that means for these two units</h2>
      <p>An institutional owner would almost certainly do three things that an individual owner often skips: file the
      Housing Inventory report every year, run the arithmetic from a documented rent roll rather than memory, and break
      out the banked portion year by year in the notice. Those three steps are precisely what a tenant petition
      attacks. {src_links("S6, S14, S11")}</p>
      <p>What an institutional owner would <em>not</em> do, and what is now illegal in San Francisco, is set these rents
      with algorithmic pricing software, or coordinate pricing with other owners. {src_links("S23, S24")}</p>
    </section>

    <section>
      <h2>Primary record for manual review</h2>
      <p>No official source quantifies "how a big landlord sets increases" beyond the filings each company makes. The
      filing below is provided for manual review only: it is the annual report of Essex Property Trust, a large
      apartment REIT headquartered in San Mateo, California, and its risk-factor section is where rent-regulation
      constraints are described. It is <strong>not</strong> relied on for any statement on this site.</p>
      <p><a href="https://www.sec.gov/Archives/edgar/data/920522/000092052226000003/0000920522-26-000003-index.htm"
      target="_blank" rel="noopener">Essex Property Trust, Inc., Form 10-K for fiscal year 2025 (SEC EDGAR)</a>
      {src_links("S27")}</p>
    </section>

    <section>
      <h2>Where an individual owner should spend the effort</h2>
      <ol class="steplist">
        <li>Rebuild the rent roll from documents, not memory. {src_links("S11")}</li>
        <li>Keep the licence current - an unlicensed increase is unenforceable however correct the maths. {src_links("S6")}</li>
        <li>Use one template that shows the banked breakdown and the rate period. {src_links("S14")}</li>
        <li>Serve early: 90 days is easy to miss and impossible to cure retroactively. {src_links("S15")}</li>
        <li>Do not delegate the calculation to a spreadsheet formula that compounds or rounds. {src_links("S2, S3")}</li>
      </ol>
    </section>"""
    return page("practice.html", "How owners handle increases",
                "What large institutional owners do, what individual owners do, and which parts are documented in "
                "official sources.", body)


def build_review():
    rows = [[esc(i), esc(q), esc(std), src_links(s)] for i, q, std, s in D.STRESS_TEST]
    body = f"""
    {callout("info", "The test being applied",
      "San Francisco tenants have access to free Rent Board counseling and, in eviction proceedings, a City-funded "
      "right to counsel, and any tenant may file an unlawful-rent-increase petition at no charge and with no time "
      "limit. " + src_links("S10, S11, S12, S25") + " The checklist below is what such a review would look for, in the "
      "order it would look for it.")}
    <section>
      <h2>Fifteen checks</h2>
      {table(["#", "Question a reviewer asks", "What a compliant file shows", "Source"], rows, filt=True)}
    </section>
    <section>
      <h2>What happens if a check fails</h2>
      {table(["Defect", "Consequence", "Source"], [
        ["No current rent increase licence on the effective date", "The increase is not enforceable; the tenant can be refunded the difference through a petition.", src_links("S6")],
        ["Arithmetic error, compounding, or rounding up", "The base rent is readjusted to the correct amount; good-faith overages of half a percent may be corrected rather than voided.", src_links("S14")],
        ["Notice too short for the size of the increase", "The increase is not effective as noticed; a new notice with the correct period is needed.", src_links("S15, S14")],
        ["Banked amount not identified, or its dates not given", "A notice defect; Rule 4.12(b) says it does not by itself void the increase, but it invites a petition.", src_links("S14")],
        ["Increase attributable to an additional occupant", "Unlawful rent increase - prohibited outright, even if the lease allows it.", src_links("S2, S13")],
        ["Increase during or after protected activity", "Retaliation exposure under Civil Code 1942.5, with a 180-day presumption.", src_links("S18")],
        ["Different terms tied to a protected characteristic", "Discrimination exposure under Government Code 12955 and 42 U.S.C. 3604.", src_links("S19, S20")],
      ])}
    </section>
    <section>
      <h2>The file to keep, per unit</h2>
      <ul class="checklist">
        <li>Original lease and every renewal, including the 1 April 2026 Unit A lease.</li>
        <li>Every prior rent-increase notice, with proof of service.</li>
        <li>Housing Inventory submission confirmation and the rent increase licence.</li>
        <li>The Rent Board rate printout (document 571) for each year used. {src_links("S4")}</li>
        <li>The calculation worksheet showing percentages added and the final cent amount.</li>
        <li>The written rule applied to both units, dated before service.</li>
        <li>Any complaint, repair request or petition history, for the retaliation check. {src_links("S18")}</li>
      </ul>
    </section>"""
    return page("review.html", "Tenant-lawyer stress test",
                "The fifteen checks a tenant-side advocate or a Rent Board Administrative Law Judge would run against "
                "these increases, and the consequence of each failure.", body, wide=True)


def build_flagged():
    rows = []
    for fid, sev, title, detail, action, src in D.FLAGS:
        badge = {"High": "bad", "Medium": "warn", "Low": "ok"}[sev]
        rows.append([
            f"<strong>{esc(fid)}</strong>",
            f"<span class='tag {badge}'>{esc(sev)}</span>",
            f"<strong>{esc(title)}</strong>",
            esc(detail),
            esc(action),
            src_links(src),
        ])
    body = f"""
    {callout("warn", "Nothing on this page blocks the analysis",
      "These items are published deliberately. Where a value could not be confirmed from an official source it was "
      "left blank rather than estimated. Each entry states what is missing, what it affects, and what would close it.")}
    <section>
      <h2>Flagged items</h2>
      {table(["#", "Severity", "Item", "What is uncertain", "What closes it", "Source"], rows, filt=True, rowids=[f[0].lower() for f in D.FLAGS])}
    </section>
    <section>
      <h2>Two conflicting official statements, in full</h2>
      <div class="twocol">
        <div class="panel">
          <h3>"24 months"</h3>
          <blockquote>If a landlord does not impose an allowed rent increase, they may be able to "bank" it and use it
          later. A skipped increase is only banked if at least 24 full months pass without any rent increase. If less
          than 24 months pass, the skipped increase is lost and cannot be imposed at a later date.</blockquote>
          <p class="muted">sf.gov, Banked rent increases {src_links("S3")}</p>
          <p>Consistent with the "irregular periods" guidance, which allows adding earlier years only at 24 months or
          more. {src_links("S9")}</p>
        </div>
        <div class="panel">
          <h3>"12 months"</h3>
          <blockquote>A full 12 months must have elapsed from the date that an annual rent increase, or a portion
          thereof, could have been imposed before this banking section becomes applicable.</blockquote>
          <p class="muted">Rent Board Rules and Regulations, Rule 4.12(a), as published on sf.gov {src_links("S14")}</p>
          <p>And a worked example on the main rent-increase page applies a 12-month test. {src_links("S2")}</p>
        </div>
      </div>
      <p>The site uses the 24-month reading because it is the dedicated banking page plus the timing page, and because
      it is the more conservative test. Under either reading, the 1.6%-only option for Unit A and the 10% option for
      Unit B are lawful. Unit B's full 13.1% is lawful under both readings for an effective date after 1 June 2026.</p>
    </section>
    <section>
      <h2>Also worth a manual look</h2>
      <ul>
        <li>The Rent Board's publicly searchable Housing Inventory record for the property (licence status and reported
        occupancy date). {src_links("S6")}</li>
        <li>The Planning Property Information Map entry for the parcel (year built, unit count). {src_links("S5")}</li>
        <li>Legistar File 261020, up to and including the final enactment record. {src_links("S22")}</li>
        <li>Any tenant petition already on file - the Rent Board does not charge for filing and imposes no time limit.
        {src_links("S11")}</li>
      </ul>
    </section>"""
    return page("flagged.html", "Flagged for review",
                "Unverified values, conflicting official guidance, pending legislation and documentation gaps - the "
                "items to check before serving any notice.", body, wide=True)


def build_sources():
    rows = []
    for k, v in D.SOURCES.items():
        rows.append([
            f"<strong>{esc(k)}</strong>",
            f"<a href='{esc(v['url'])}' target='_blank' rel='noopener'>{esc(v['title'])}</a>",
            esc(v["publisher"]),
            esc(v["supports"]),
            esc(v["quote"]),
        ])
    body = f"""
    <section>
      <h2>Source register</h2>
      <p>Twenty-seven sources, all government publications or primary statute text, retrieved on {D.VERIFIED_ON}.
      Each entry gives what the source is used for on this site and the passage it rests on. The register is also
      written to <code>research/source-register.md</code> for offline review.</p>
      {table(["ID", "Source", "Publisher", "Used for", "Quoted passage"], rows, filt=True, rowids=[k.lower() for k in D.SOURCES])}
    </section>
    <section>
      <h2>What is excluded, and why</h2>
      <ul>
        <li>Property-management blog posts and calculators - useful for orientation, but not authoritative.</li>
        <li>Any figure that could not be retrieved from a government source during verification, including a ZIP-level
        market-rent benchmark. {src_links("S21")}</li>
        <li>Statements about what a particular large landlord does, beyond what its filings and the enforcement record
        show. {src_links("S27, S24")}</li>
      </ul>
      <p class="muted">Retrieval method: each page was fetched and read directly; rates were cross-checked against the
      Rent Board's own historical table (document 571) and, where applicable, against the Attorney General's published
      table. {src_links("S4, S21")}</p>
    </section>"""
    return page("sources.html", "Sources",
                "The full register of official sources, with what each one supports and the passage relied on.", body,
                wide=True)


# ---------------------------------------------------------------------------
# data exports
# ---------------------------------------------------------------------------
def build_data():
    (OUT / "data").mkdir(parents=True, exist_ok=True)
    with (OUT / "data" / "ledger.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["unit", "anniversary_date", "rate_period", "rate_pct", "base_rent", "dollars", "status", "sources"])
        for anniv, period, pct, status, src in D.LEDGER_A:
            w.writerow(["A", anniv, period, pct, "3995.00", f"{3995*pct/100:.2f}", status, src])
        for anniv, period, pct, status, src in D.LEDGER_B:
            w.writerow(["B", anniv, period, pct, "3150.00", f"{3150*pct/100:.2f}", status, src])

    with (OUT / "data" / "requirements.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["layer", "requirement", "meaning_here", "sources"])
        for row in D.REQUIREMENTS:
            w.writerow(row)

    (OUT / "data" / "sources.json").write_text(
        json.dumps({"verified_on": D.VERIFIED_ON, "sources": D.SOURCES}, indent=2, ensure_ascii=False),
        encoding="utf-8")

    lines = [f"# Source register ({D.VERIFIED_ON})", "",
             "Every rule and rate on the site traces to one of these government sources.", ""]
    for k, v in D.SOURCES.items():
        lines += [f"## {k} - {v['title']}", "", f"- Publisher: {v['publisher']}",
                  f"- URL: {v['url']}", f"- Used for: {v['supports']}", f"- Passage: > {v['quote']}", ""]
    (ROOT / "research").mkdir(exist_ok=True)
    (ROOT / "research" / "source-register.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    built = [
        build_index(), build_exec(), build_units(), build_requirements(), build_calculations(),
        build_notices(), build_fair(), build_practice(), build_review(), build_flagged(), build_sources(),
    ]
    build_data()
    print("Built:", ", ".join(built))


if __name__ == "__main__":
    main()
