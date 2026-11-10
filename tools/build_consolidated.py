#!/usr/bin/env python3
"""Build the consolidated edition under site/ (final integration, 2026-11-10).

Run:  python3 tools/build_consolidated.py
No third-party dependencies. Plain static HTML + one stylesheet, so GitHub Pages can serve
it directly from the repository root.
"""

import html
import pathlib
import re
import sys
from decimal import Decimal

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import site_content as C  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
TITLE = "San Francisco Rent Increase Review"
SUB = "Two rent-controlled units in a 1940 building · San Francisco (location withheld)"

NAV = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive summary"),
    ("process.html", "Process &amp; licence"),
    ("units.html", "Units &amp; calculations"),
    ("laws.html", "Laws &amp; caps"),
    ("reasonable.html", "Reasonable &amp; normal"),
    ("notice.html", "Notice &amp; reasons"),
    ("review.html", "Tenant-lawyer test"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged for review"),
]


def esc(s):
    return html.escape(str(s), quote=False)


def chip(key):
    """Single official-source chip."""
    label, url, _ = C.SRC[key]
    return f'<a class="src" href="{html.escape(url, quote=True)}">{esc(label)}</a>'


def srcs(keys, sep=" · "):
    return sep.join(chip(k) for k in keys)


def tablerow(cells, keys, cls=""):
    """A data row; the last cell is always the source cell."""
    tds = "".join(f"<td>{c}</td>" for c in cells)
    attr = f' class="{cls}"' if cls else ""
    return f"<tr{attr}>{tds}<td class=\"srcell\">{srcs(keys)}</td></tr>"


def page(name, title, description, body, active, dest=None, prefix=""):
    links = "".join(
        '<a href="{}{}"{}>{}</a>'.format(
            prefix, href, ' class="active"' if href == active else "", label)
        for href, label in NAV
    )
    if prefix:
        # Re-point every relative link in the body at the subdirectory edition.
        body = re.sub(r'href="(?!https?:|mailto:|tel:|#|/)', 'href="' + prefix, body)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — {TITLE}</title>
<meta name="description" content="{esc(description)}">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <div class="brand">
      <span class="mark" aria-hidden="true">SF</span>
      <div>
        <div class="brand-title">{TITLE}</div>
        <div class="brand-sub">{SUB}</div>
      </div>
    </div>
    <nav class="main" aria-label="Sections">{links}</nav>
  </div>
</header>
<main id="main" class="wrap">
{body}
</main>
<footer class="wrap">
  <p><strong>Anonymised internal research document.</strong> Tenant names are replaced with placeholder
  labels; dates and dollar amounts are unchanged; the property's street address, ZIP code and neighbourhood
  are withheld because they were supplied as internal information. Nothing here is unique to a location —
  the rules cited apply citywide.</p>
  <p><strong>Not legal advice.</strong> Every figure was read from, or computed from, an official source on
  <time datetime="2026-11-10">10 November 2026</time> and each row carries its source link. Confirm with a
  Rent Board counsellor on <a href="tel:+14152524600">415-252-4600</a> and a California attorney before
  serving any notice. Unverified or disputed items are published, not hidden, on
  <a href="{prefix}flagged.html">Flagged for review</a>.</p>
  <p class="small">Rebuilt 10 November 2026 from the consolidated verification pass. Earlier editions in
  this repository (<code>docs/</code>, <code>dashboard/</code>, <code>review/</code>,
  <code>audit/</code>, <code>verified/</code>, <code>pages/</code>) are superseded by this one and are kept
  for provenance only.</p>
</footer>
</body>
</html>
"""
    target = pathlib.Path(dest) if dest else (OUT / name)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc, encoding="utf-8")
    return str(target.relative_to(ROOT))


def kpi(value, label, key):
    return f"""<div class="kpi"><div class="kpi-value">{value}</div>
    <div class="kpi-label">{label}</div><div class="kpi-src">{chip(key)}</div></div>"""


def stat(value, label):
    return f'<div class="stat"><div class="num">{value}</div><div class="lbl">{label}</div></div>'


# --------------------------------------------------------------------------------------
# LANDING / DASHBOARD
# --------------------------------------------------------------------------------------
INDEX_DESC = ("Answer-first dashboard on whether an individual San Francisco owner must report "
              "to the Rent Board and hold a rent-increase licence before raising rent; verified "
              "allowances and calculations for two rent-controlled units.")


def _index_body():
    return f"""
<section class="hero card">
  <span class="tag">Answer first</span>
  <h1>Does an individual owner need permission from the Rent Board before raising rent?</h1>
  <p class="lead"><strong>You do not need the Rent Board's permission for the amount, and you do not need to
  file the increase notice with it. But you do need two things from the Rent Board's Housing Inventory before
  the increase can take effect.</strong> First, report both units into the Housing Inventory (due 1 March each
  year). Second, make sure the rent-increase licence that the report generates is current
  <em>on the effective date</em> of the increase. A correct 1.6% increase served without a current licence is
  unenforceable, and the tenant can recover it.</p>
  <table>
    <thead><tr><th>Your question, in your words</th><th>Verified answer</th><th>Official source</th></tr></thead>
    <tbody>
    {tablerow(["&ldquo;Do I need to inform the Rent Board before notifying tenants?&rdquo;",
               "<strong>Yes, once a year.</strong> All owners of residential property must report into the Housing Inventory by 1 March. Reporting a tenant-occupied unit is what produces the licence. Reporting is free and is done online.",
               ], ["inventory", "s3715"])}
    {tablerow(["&ldquo;Do I need to apply for a licence if I am an individual, not a corporation?&rdquo;",
               "<strong>Yes. There is no individual-owner exemption.</strong> The ordinance draws its line by building size (10+ units vs 1–9 units and condominiums), never by whether the owner is a person or a company. A two-unit building is in the 1–9 unit group, which has been reporting since 1 March 2023.",
               ], ["inventory", "s3715", "noncompliance"])}
    {tablerow(["&ldquo;Do I need the Rent Board to approve the amount of the increase?&rdquo;",
               "<strong>No.</strong> Annual allowable increases and banked increases require no petition and no approval. The licence is a reporting-compliance licence, not a per-increase authorisation. Petitions are only for extra increases above the allowance (operating and maintenance, capital improvement and similar).",
               ], ["bank", "multiyear", "s373"])}
    {tablerow(["&ldquo;What happens if I skip it?&rdquo;",
               "The licence is <strong>suspended</strong> while reporting is not substantially compliant, and the tenant is <strong>not obligated to pay</strong> the increase for the months of the suspension. A notice that took effect while unlicensed may be null and void for several years. The Rent Board may write to your tenants to tell them.",
               ], ["s3715", "noncompliance"])}
    {tablerow(["&ldquo;Does getting the maths right fix it?&rdquo;",
               "<strong>No.</strong> The licence condition is independent of the percentage. Both have to be right.",
               ], ["inventory", "rates"])}
    {tablerow(["&ldquo;Which rate applies to me?&rdquo;",
               "<strong>1.6%</strong> for an increase effective 1 March 2026 – 28 February 2027. The prior year's rate was 1.4%. Use the rate in effect on the <em>effective date</em>, not the day you serve the notice.",
               ], ["rates", "announce", "form571"])}
    {tablerow(["&ldquo;Do I need to file the increase notice itself with the Rent Board?&rdquo;",
               "<strong>No.</strong> There is no filing requirement for an annual or banked notice. Your obligation is to give the tenant written notice (30 or 90 days) and to keep proof of service.",
               ], ["civ827", "bank", "rates"])}
    </tbody>
  </table>
  <p class="note">The order matters: <strong>report → confirm licence → serve notice.</strong> Doing it the
  other way round is the most common reason a lawful-percentage increase gets overturned.</p>
</section>

<section class="grid four">
  {kpi("1.6%", "Allowable annual increase, 1 March 2026 – 28 February 2027", "rates")}
  {kpi("1.4%", "Prior year's rate, 1 March 2025 – 28 February 2026", "form571")}
  {kpi("30 / 90", "Days of written notice — 90 if the increase exceeds 10%; add 5 days if mailed", "civ827")}
  {kpi("1 March", "Annual Housing Inventory deadline; no licence on the effective date voids the increase", "inventory")}
</section>

<section class="card">
  <h2>What is available on each unit</h2>
  <p class="small">Amounts are computed from the published percentages only, on base rent, with no rounding up
  and no compounding. The licence condition applies to every figure in this table.</p>
  <table>
    <thead><tr><th>Unit</th><th>Base rent</th><th>Option</th><th>Rate</th><th>Increase</th><th>New rent</th><th>Notice</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["<strong>Unit 1</strong><br><span class='small'>Tenancy began 1 Feb 2025 · anniversary 1 Feb</span>", "$3,995.00", "Single year, conservative", "1.6%", C.money(C.U1_16[0]), C.money(C.U1_16[1]), "30 days", ], ["rates", "form571"])}
    {tablerow(["<strong>Unit 1</strong>", "$3,995.00", "Plus the 1.4% available from 1 Feb 2026 (12-month reading — see F-02)", "3.0%", C.money(C.U1_30[0]), C.money(C.U1_30[1]), "30 days", ], ["bank", "form571"])}
    {tablerow(["<strong>Unit 2</strong><br><span class='small'>Tenancy began 1 Jun 2019 · anniversary 1 Jun</span>", "$3,150.00", "Single year, conservative", "1.6%", C.money(C.U2_16[0]), C.money(C.U2_16[1]), "30 days", ], ["rates", "form571"])}
    {tablerow(["<strong>Unit 2</strong>", "$3,150.00", "Banked 2020–2024 + current year (24-month reading)", "11.7%", C.money(C.U2_117[0]), C.money(C.U2_117[1]), "90 days", ], ["bank", "form571"])}
    {tablerow(["<strong>Unit 2</strong>", "$3,150.00", "Banked 2020–2025 only, current year left for later", "11.5%", C.money(C.U2_115[0]), C.money(C.U2_115[1]), "90 days", ], ["bank", "form571"])}
    {tablerow(["<strong>Unit 2</strong>", "$3,150.00", "Maximum on the 12-month reading: banked 2020–2025 + current year", "13.1%", C.money(C.U2_131[0]), C.money(C.U2_131[1]), "90 days", ], ["bank", "form571"])}
    {tablerow(["<strong>Unit 2</strong>", "$3,150.00", "<strong>Recommended</strong>: phased, stays lawful even if File #261020 passes", "10.0%", C.money(C.U2_100[0]), C.money(C.U2_100[1]), "90 days", ], ["legistar", "bank"])}
    </tbody>
  </table>
  <p class="note"><strong>Why the recommended Unit 2 figure is 10%:</strong> the district's pending ordinance
  (File #261020) would cap combined banked and capital-improvement increases at 10% a year, and sf.gov says it
  would apply to banked increases <em>noticed on or after 15 September 2026</em>. It is not law. Capping the
  notice at 10% now keeps the increase lawful under both the current and the proposed rule, which is worth more
  than the extra $47.50 a month. See <a href="flagged.html#f-01">F-01</a>.</p>
</section>

<section class="card">
  <h2>The one fact that decides the most</h2>
  <p>Unit 1 has a continuing tenancy. One original tenant is still there and a new occupant moved in on
  1 April 2026. That means <strong>there was no vacancy, so the rent cannot be reset to market</strong>, and
  <strong>the owner may not charge more because an extra person moved in</strong>. Rule §6.14 would allow a
  market-rate increase only if the <em>last</em> original occupant had left and a proper written 6.14 notice had
  been served; and under Costa-Hawkins a <strong>co-tenant</strong> — someone with an agreement with the owner —
  is not subject to that increase regardless of when they moved in. This is the point a tenant-side lawyer would
  test first, and it is absent from every earlier edition of this site.</p>
  <p>{srcs(["s614", "civ1954_53", "rates"])}</p>
</section>

<section class="card">
  <h2>Read next</h2>
  <div class="grid three">
    <a class="linkcard" href="executive-summary.html"><strong>Executive summary</strong><span>The whole file in one page: answer, findings, figures, actions.</span></a>
    <a class="linkcard" href="process.html"><strong>Process &amp; licence</strong><span>The nine steps from coverage check to served notice, in order.</span></a>
    <a class="linkcard" href="units.html"><strong>Units &amp; calculations</strong><span>Every option to the cent, including which reading of the banking rule gives which number.</span></a>
    <a class="linkcard" href="laws.html"><strong>Laws &amp; caps</strong><span>Local, state and federal rules side by side, with the full 1982–2027 rate table.</span></a>
    <a class="linkcard" href="review.html"><strong>Tenant-lawyer test</strong><span>What a free tenant-side lawyer would check, and whether to raise one unit or both.</span></a>
    <a class="linkcard" href="flagged.html"><strong>Flagged for review</strong><span>Nine items that are unverified, disputed or not yet law.</span></a>
  </div>
</section>
"""



# --------------------------------------------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------------------------------------------
def build_exec():
    body = f"""
<section class="card hero">
  <span class="tag">Executive summary</span>
  <h1>Rent increases for two rent-controlled San Francisco units</h1>
  <p class="lead">Prepared 10 November 2026. Two units in a two-unit building constructed in 1940, in San
  Francisco. Unit 1: tenancy began 1 February 2025 at $3,995 a month; one original tenant remains and an
  additional occupant joined on 1 April 2026 at the same rent. Unit 2: tenancy began 1 June 2019 at $3,150 a
  month. Both are rent-controlled. Tenant names are replaced by placeholder labels; dates and amounts are
  unchanged; the location is withheld because it was supplied as internal information.</p>
</section>

<section class="card highlight">
  <h2>1. The Rent Board question, answered first</h2>
  <p><strong>You are an individual owner, not a corporation. You still have to report to the Rent Board and
  hold a rent-increase licence — but you do not need the Board's approval of the amount, and you do not file the
  increase notice with the Board.</strong></p>
  <p>There are exactly two Rent Board obligations that bear on a rent increase, and they are both reporting
  obligations under Administrative Code §37.15:</p>
  <ol>
    <li><strong>Report into the Housing Inventory by 1 March every year.</strong> All owners of residential
    property must do this, including owners who are individuals and including owners who do not currently let a
    unit. Buildings with 1–9 residential units and condominiums have been in scope since 1 March 2023; buildings
    with 10 or more units since 1 July 2022. This two-unit building is in the first group.</li>
    <li><strong>Make sure the resulting rent-increase licence is current on the effective date of the
    increase.</strong> When you report a unit as tenant-occupied, the licence is generated automatically —
    there is no separate application and no fee. The licence is not an approval of the percentage.</li>
  </ol>
  <p>If you report late, you can still file, and you will still get the licence. But an increase whose
  effective date falls while you are unlicensed does not have to be paid: §37.15(e) suspends the licence during
  non-compliance and says the tenant is not obligated to pay the increased rent for the months of suspension, and
  sf.gov warns that a notice taking effect while unlicensed may be null and void, potentially for more than one
  year.</p>
  <p>{srcs(["inventory", "s3715", "noncompliance", "rates"])}</p>
  <p class="note">Practical consequence: <strong>report first, confirm the licence, then serve the notice.</strong>
  Nothing else about the Rent Board needs to happen before you notify tenants.</p>
</section>

<section class="card">
  <h2>2. What is "reasonable and normal" here</h2>
  <p>For a rent-controlled unit in San Francisco the answer is not a matter of judgement. The lawful ceiling
  <em>is</em> the normal figure, because the ordinance sets it citywide at 60% of the Bay Area CPI change, capped
  at 7%:</p>
  <table>
    <thead><tr><th>Question</th><th>Verified answer</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["What is the lawful annual increase now?", "<strong>1.6%</strong> for increases effective 1 March 2026 – 28 February 2027. It was <strong>1.4%</strong> the year before.", ], ["rates", "announce"])}
    {tablerow(["Is a larger increase reasonable?", "Only if it is made up of correctly banked prior years, and only up to the arithmetic maximum. There is no discretion to charge more because costs rose or because market rent is higher; that requires a separate petition.", ], ["s373", "bank"])}
    {tablerow(["Does the state cap allow more?", "AB 1482 caps at 5% + CPI, maximum 10% (8.8% for the San Francisco metro for increases starting 1 August 2026 – 31 July 2027), but it <strong>does not apply</strong> where a local ordinance already restricts increases to less. San Francisco's 1.6% is lower, so the local rule governs.", ], ["civ1947_12", "oag"])}
    {tablerow(["Is there a federal ceiling?", "<strong>No.</strong> Federal law has no rent cap. It does govern the reasons: discrimination in the terms of a rental on protected grounds is unlawful.", ], ["fha"])}
    {tablerow(["What is normal for this specific ZIP code?", "<strong>Blank — no official source publishes it.</strong> Neither HUD, the Census Bureau, the Rent Board nor the Attorney General publishes a lawful or market rent benchmark at ZIP level. Flagged as F-04 rather than estimated. Nothing in the advice depends on it, because the lawful ceiling is citywide.", ], ["oag", "form571"])}
    {tablerow(["Is a banked catch-up normal?", "It is lawful but it is not routine, and it is the specific practice the Board of Supervisors is currently trying to cap. A phased increase is the more defensible course.", ], ["legistar", "bank"])}
    </tbody>
  </table>
</section>

<section class="card">
  <h2>3. The figures, to the cent</h2>
  <table>
    <thead><tr><th>Unit</th><th>Base</th><th>Increase</th><th>New rent</th><th>Basis</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["Unit 1", "$3,995.00", "1.6% = " + C.money(C.U1_16[0]), C.money(C.U1_16[1]), "One rate year. Available from 1 February 2027 (the 12-month interval).", ], ["rates", "form571"])}
    {tablerow(["Unit 1", "$3,995.00", "3.0% = " + C.money(C.U1_30[0]), C.money(C.U1_30[1]), "Adds the 1.4% that became available on 1 February 2026. Only available on the 12-month reading of the banking rule — see F-02.", ], ["bank", "form571"])}
    {tablerow(["Unit 2", "$3,150.00", "1.6% = " + C.money(C.U2_16[0]), C.money(C.U2_16[1]), "One rate year, no banking assumed.", ], ["rates", "form571"])}
    {tablerow(["Unit 2", "$3,150.00", "11.7% = " + C.money(C.U2_117[0]), C.money(C.U2_117[1]), "Banked 2020–2024 (1.8 + 0.7 + 2.3 + 3.6 + 1.7 = 10.1%) plus the current 1.6%. Requires a 24-month gap between rises, so it assumes the 2025 increase went unused.", ], ["bank", "form571"])}
    {tablerow(["Unit 2", "$3,150.00", "11.5% = " + C.money(C.U2_115[0]), C.money(C.U2_115[1]), "Banked 2020–2025 (1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 = 11.5%), current year left for later.", ], ["bank", "form571"])}
    {tablerow(["Unit 2", "$3,150.00", "13.1% = " + C.money(C.U2_131[0]), C.money(C.U2_131[1]), "Arithmetic maximum on the 12-month reading: 11.5% banked plus the current 1.6%. Conditional on no increase since 2019 (F-03) and on the pending ordinance not passing (F-01).", ], ["bank", "form571", "legistar"])}
    {tablerow(["Unit 2", "$3,150.00", "<strong>10.0% = " + C.money(C.U2_100[0]) + "</strong>", "<strong>" + C.money(C.U2_100[1]) + "</strong>", "<strong>Recommended.</strong> Phased, so it remains lawful whether or not File #261020 is enacted.", ], ["legistar", "bank"])}
    </tbody>
  </table>
  <p class="small">All percentages are added, never compounded, and applied once to base rent. Passthroughs are
  excluded. Amounts are not rounded up.</p>
</section>

<section class="card">
  <h2>4. How to inform tenants, and what the reason may be</h2>
  <p>The reason for an annual or banked increase does not have to be justified to the tenant: it is the
  ordinance formula. What matters is that the reason is <em>not</em> a prohibited one, and that the notice is
  correct. The owner's written reason should be the same for both units.</p>
  <table>
    <thead><tr><th>Element</th><th>Requirement</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["Form", "Written notice served on the tenant. Personal delivery, or mail with the extra days.", ], ["civ827", "ccp1013"])}
    {tablerow(["Lead time", "At least <strong>30 days</strong> if the increase is 10% or less; at least <strong>90 days</strong> if it is more than 10%, measured alone or combined with other increases in the previous 12 months. <strong>Add 5 calendar days</strong> if served by mail inside California.", ], ["civ827", "ccp1013"])}
    {tablerow(["Content", "Dollar amount of the increase, the percentage, the effective date, and for a banked increase which part is banked and from which years.", ], ["rates", "bank"])}
    {tablerow(["Rate used", "The percentage in effect on the <strong>effective date</strong>, not the service date.", ], ["rates"])}
    {tablerow(["Lawful reasons", "The Rent Board's published allowance; documented banked years; a certified capital-improvement or operating-and-maintenance petition. Nothing about the tenant.", ], ["s373", "bank"])}
    {tablerow(["Unlawful reasons", "Anything tied to a protected characteristic; retaliation for a habitability complaint or for organising; charging more because an occupant was added.", ], ["gov12955", "civ1942_5", "rates"])}
    </tbody>
  </table>
</section>

<section class="card">
  <h2>5. Would a tenant-side lawyer accept it?</h2>
  <p>San Francisco tenants have access to free counsel, and an increase will be tested on procedure before it is
  tested on policy. An increase that satisfies all of the following is ordinary business practice and should
  survive that review. Each test is set out with its source on <a href="review.html">Tenant-lawyer test</a>.</p>
  <ol class="tight">
    <li>Licence current on the effective date, provable from the Rent Board Portal.</li>
    <li>Amount at or below the published allowance, plus only correctly computed banking, on base rent only.</li>
    <li>At least 12 months since the last increase, on the correct anniversary date.</li>
    <li>Notice of the right length, with the four required elements, served.</li>
    <li>No protected characteristic, complaint or added occupant anywhere in the reasoning.</li>
    <li>One written policy applied to both units, with any difference explained by tenancy history.</li>
  </ol>
</section>

<section class="card">
  <h2>6. One unit or both?</h2>
  <p><strong>Raise both, on the same written policy.</strong> Raising a single unit is not automatically
  unlawful, but it removes the simplest answer to a discrimination or retaliation inquiry. If both units are
  treated by the same written rule — the published allowance plus documented banking, applied on each unit's own
  anniversary — then any difference in outcome is explained by objective tenancy history rather than by who the
  tenants are. If only one unit is raised, record the objective reason in writing and keep it with the file.</p>
  <p>{srcs(["gov12955", "civ1942_5", "discrim"])}</p>
</section>

<section class="card">
  <h2>7. What to do next</h2>
  <ol>
    <li>Report both units into the Housing Inventory and confirm the licence for the intended effective date.
    {chip("inventory")}</li>
    <li>Assemble the full rent ledger for Unit 2 from 2019 and for Unit 1 from 2025. Everything about banking
    rests on it. <a href="flagged.html#f-03">F-03</a></li>
    <li>Decide the figures. Unit 1: 1.6% ($63.92) on 1 February 2027, or 3.0% ($119.85) if the 1.4% is treated as
    banked. Unit 2: 1.6% ($50.40), or a phased 10% ($315.00) now, with the remainder available later.</li>
    <li>Re-check Legistar File #261020 before serving any notice over 10%. <a href="flagged.html#f-01">F-01</a></li>
    <li>Serve the notice with the correct lead time and keep proof of service.</li>
    <li>Have a California attorney review the two notices before they are served. This document is research, not
    legal advice.</li>
  </ol>
</section>
"""
    return page("executive-summary.html", "Executive summary",
                "Executive summary: the Rent Board reporting and licence obligations for an individual owner, the verified allowable increases, cents-exact figures for both units, notice requirements and the one-unit-or-both analysis.",
                body, "executive-summary.html")


# --------------------------------------------------------------------------------------
# PROCESS & LICENCE
# --------------------------------------------------------------------------------------
def build_process():
    steps = [
        ("Confirm the units are covered",
         "Check the certificate of occupancy date, not the build year. Units built on or before 13 June 1979 that are not single-family dwellings are generally covered by both rent control and eviction protection. A 1940 two-unit building almost certainly is; confirm it.",
         ["laws"]),
        ("Pull the rent history for each unit",
         "You need the date and amount of every increase, or the absence of one, because that fixes the anniversary date and the bankable percentage. Without it nothing else can be calculated safely.",
         ["bank", "rates"]),
        ("Create a Rent Board Portal account and add the property",
         "Reporting is done online, is free, and can be done at any time. Paper filings are possible but slower.",
         ["inventory", "portal"]),
        ("Submit the Housing Inventory for both units",
         "For each non-owner-occupied unit you report the owner or manager contact details, any business registration number, approximate square footage in 250 sq ft increments, number of bedrooms and bathrooms, the date the current occupancy began, vacancy and occupancy dates for the past 12 months, and the base rent in $250 increments plus which utilities it includes. The submission is made under penalty of perjury.",
         ["inventory", "s3715"]),
        ("Confirm the rent-increase licence",
         "Reporting an occupied unit generates the licence automatically. In the Portal, search the property, open it, and check that a licence is listed and that its period covers your intended effective date. Tenants can see the same record.",
         ["inventory", "noncompliance"]),
        ("Fix the effective date and the percentage",
         "At least 12 months must have passed since the tenancy began or since the last increase. Use the rate in force on the effective date. Do not round up. Do not compound. Base rent only.",
         ["rates", "civ827"]),
        ("Choose a figure you can defend",
         "The published allowance alone is the safest. Adding banked years is lawful but invites scrutiny and may be capped by the pending ordinance; a phased increase keeps you inside both the current and the proposed rule.",
         ["bank", "legistar"]),
        ("Serve the written notice",
         "30 days if the increase is 10% or less, 90 days if more, plus 5 calendar days if mailed inside California. State the dollar amount, the percentage, the effective date, and which part is banked.",
         ["civ827", "ccp1013", "rates"]),
        ("Keep the file, and repeat every March",
         "Keep the notice, proof of service and the licence record together. Re-file the Housing Inventory by 1 March each year and update owner or manager contact details within 30 days of any change.",
         ["inventory", "unlawful"]),
    ]
    rows = "\n".join(
        f"<tr><td class=\"step\">{i}</td><td><strong>{esc(t)}</strong><p>{d}</p></td>"
        f"<td class=\"srcell\">{srcs(keys)}</td></tr>"
        for i, (t, d, keys) in enumerate(steps, 1)
    )
    lic = "\n".join(
        tablerow([q, a], keys)
        for q, a, keys in [
            ("Who must report?",
             "<strong>All owners of residential property.</strong> Most owners must report even if they are not currently letting a unit. There is no exemption for an owner who is a private individual.",
             ["inventory", "s3715"]),
            ("Is there a separate licence application?",
             "<strong>No.</strong> The licence is generated automatically once an occupied unit is reported. There is no form to file and no fee.",
             ["inventory", "s3715"]),
            ("When must the licence be in place?",
             "On the <strong>effective date</strong> of the increase. Being licensed by the time you serve the notice is not enough if the licence lapses before the increase takes effect.",
             ["inventory", "bank"]),
            ("What is the deadline?",
             "<strong>1 March each year.</strong> Late filing is possible and carries no monetary penalty, but it does not retroactively validate an increase that took effect while unlicensed.",
             ["inventory"]),
            ("What is the consequence of non-compliance?",
             "The licence is <strong>temporarily suspended</strong>, and the tenant is <strong>not obligated to pay</strong> the increase for the months of suspension. The Board may notify tenants directly. Tenants may file an Unlawful Rent Increase Petition, at no charge and with no time limit.",
             ["s3715", "noncompliance", "unlawful"]),
            ("Is the licence the same as approval of the amount?",
             "<strong>No.</strong> It is a reporting-compliance licence. The amount is separately constrained by §37.3 (60% of CPI, maximum 7%) and needs no approval.",
             ["s373", "s3715"]),
            ("Does the notice need to be filed with the Rent Board?",
             "<strong>No.</strong> There is no filing requirement for an annual or banked notice.",
             ["bank", "multiyear"]),
            ("When is an extra petition needed?",
             "Only for increases <strong>above</strong> the annual allowance: operating and maintenance expenses, capital improvements, rehabilitation, energy improvements, utility and bond passthroughs. None of those are assumed here.",
             ["s373", "rates"]),
        ]
    )
    body = f"""
<section class="card hero">
  <span class="tag">Process</span>
  <h1>From coverage check to served notice: nine steps</h1>
  <p class="lead">Written for an owner who has never dealt with the Rent Board. Steps 1 to 3 must happen before
  any notice is served. Steps 4 and 5 are the ones that invalidate otherwise correct increases when they are
  skipped.</p>
</section>

<section class="card">
  <h2>The licence and reporting questions in detail</h2>
  <table>
    <thead><tr><th>Question</th><th>Verified answer</th><th>Source</th></tr></thead>
    <tbody>{lic}</tbody>
  </table>
</section>

<section class="card">
  <h2>Step by step</h2>
  <table class="steps">
    <thead><tr><th>#</th><th>What to do</th><th>Source</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</section>

<section class="card">
  <h2>What the statute actually says</h2>
  <p>§37.15(e) is the provision that creates the licence, and it is worth reading in full because it contains
  both the licence and the penalty for not having one: <em>&ldquo;If a landlord has substantially complied with
  the obligation to report information about a rental unit as required under this Section 37.15, the landlord
  shall receive a license to impose rent increases on tenants in that unit under Sections 37.3(a)(1)-(2). If the
  landlord has not substantially complied with the reporting obligation, then the license to impose rent
  increases shall be temporarily suspended during the period of the landlord's noncompliance. Upon receipt of the
  required information from the landlord, the suspension shall be terminated, and the license to impose rent
  increases shall be restored prospectively, but a tenant shall not be obligated to pay the increased rent for
  months during the period of suspension.&rdquo;</em></p>
  <p>{srcs(["s3715", "s373"])}</p>
  <p class="note">Note the words <em>restored prospectively</em>. Catching up on reporting fixes the future; it
  does not cure the months that have already passed.</p>
</section>

<section class="card">
  <h2>Getting help with the process</h2>
  <table>
    <thead><tr><th>Who</th><th>What for</th><th>Contact</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["Rent Board counselling", "Whether your units are covered, how to calculate a banked increase, how to file the Housing Inventory", "415-252-4600, weekdays 9–12 and 1–4", ], ["laws", "inventory"])}
    {tablerow(["Rent Board Portal", "Filing the Housing Inventory and checking the licence for a specific date", "portal.sfrb.org", ], ["portal", "inventory"])}
    {tablerow(["Bar Association of San Francisco — Conflict Intervention Service", "Mediation with a tenant before or instead of a dispute", "415-782-8940", ], ["resources"])}
    {tablerow(["Rent Board Tenant Petitions", "What a tenant can file against an increase, and on what grounds", "No fee; no filing deadline", ], ["petitions", "unlawful"])}
    </tbody>
  </table>
</section>
"""
    return page("process.html", "Process &amp; licence",
                "Step-by-step San Francisco rent-increase process for an individual owner: Housing Inventory reporting, rent-increase licence, effective date, notice and record keeping, with official sources.",
                body, "process.html")


# --------------------------------------------------------------------------------------
# UNITS & CALCULATIONS
# --------------------------------------------------------------------------------------
def build_units():
    body = f"""
<section class="card hero">
  <span class="tag">Units</span>
  <h1>Both units, every lawful option, to the cent</h1>
  <p class="lead">Tenant names are replaced with placeholder labels; dates and dollar amounts are exactly as
  supplied. No value below is estimated: each comes from the published percentage table or from arithmetic on the
  stated base rent.</p>
</section>

<section class="card">
  <h2>The two tenancies</h2>
  <table>
    <thead><tr><th>Fact</th><th>Unit 1</th><th>Unit 2</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["Tenancy began", C.UNIT1["start"], C.UNIT2["start"], ], ["rates"])}
    {tablerow(["Base rent", C.UNIT1["base_fmt"], C.UNIT2["base_fmt"], ], ["rates"])}
    {tablerow(["Who lives there now", C.UNIT1["status"], C.UNIT2["status"], ], ["rates", "s614"])}
    {tablerow(["Anniversary date", "1 February (the 1 April 2026 continuation did not reset it)", "1 June", ], ["rates"])}
    {tablerow(["First increase became available", C.UNIT1["first_available"], C.UNIT2["first_available"], ], ["form571", "rates"])}
    {tablerow(["Next available effective date", C.UNIT1["next"], C.UNIT2["next"], ], ["rates", "bank"])}
    {tablerow(["Rent control", "Covered — built 1940, before 13 June 1979, two units, not a single-family dwelling", "Same", ], ["laws"])}
    {tablerow(["Licence needed before the increase", "Yes — Housing Inventory report and a current licence on the effective date", "Yes", ], ["inventory", "s3715"])}
    </tbody>
  </table>
</section>

<section class="card">
  <h2>Unit 1 calculations</h2>
  <table>
    <thead><tr><th>Option</th><th>Percentage</th><th>Arithmetic</th><th>Increase</th><th>New rent</th><th>Notice</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["Single rate year, effective 1 February 2027", "1.6%", "$3,995.00 × 0.016", C.money(C.U1_16[0]), C.money(C.U1_16[1]), "30 days", ], ["rates", "form571"])}
    {tablerow(["Plus the 1.4% available from 1 February 2026", "3.0%", "(1.4 + 1.6) applied once to $3,995.00", C.money(C.U1_30[0]), C.money(C.U1_30[1]), "30 days", ], ["bank", "form571"])}
    </tbody>
  </table>
  <p class="note">The 3.0% option depends entirely on <a href="flagged.html#f-02">F-02</a>. On the reading that a
  skipped year needs a <strong>24-month</strong> gap before it can be banked, the 1.4% from 2026 is <em>lost</em>
  and only 1.6% ($63.92) is available on 1 February 2027. On the reading that a 12-month gap is enough — which is
  what the Rent Board's own worked examples use — 3.0% is available. The 1.6% figure is safe under both
  readings, which is why it is the conservative recommendation.</p>
</section>

<section class="card">
  <h2>Unit 2 calculations</h2>
  <p>The rate years that have become available since this tenancy began, taken from the Rent Board's own table:</p>
  <table>
    <thead><tr><th>Rate year</th><th>Percentage</th><th>Available from</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["3/1/2026 – 2/28/2027", "1.6%", "1 June 2027 (or the effective date chosen, at the rate then in force)", ], ["form571"])}
    {tablerow(["3/1/2025 – 2/28/2026", "1.4%", "1 June 2026", ], ["form571"])}
    {tablerow(["3/1/2024 – 2/28/2025", "1.7%", "1 June 2025", ], ["form571"])}
    {tablerow(["3/1/2023 – 2/29/2024", "3.6%", "1 June 2024", ], ["form571"])}
    {tablerow(["3/1/2022 – 2/28/2023", "2.3%", "1 June 2023", ], ["form571"])}
    {tablerow(["3/1/2021 – 2/28/2022", "0.7%", "1 June 2022", ], ["form571"])}
    {tablerow(["3/1/2020 – 2/28/2021", "1.8%", "1 June 2021", ], ["form571"])}
    {tablerow(["3/1/2019 – 2/29/2020", "2.6%", "1 June 2020", ], ["form571"])}
    </tbody>
  </table>
  <p class="small">The 2.6% for the 2019–20 rate year was first available on 1 June 2020. It is excluded from
  every banked total below because it would be the fifth or sixth banked year on the 24-month reading, and
  because the arithmetic maximum is already well above the 10% that is prudent to serve. Its omission makes the
  figures conservative. If a full catch-up were attempted it would have to be computed and noticed separately.</p>
  <table>
    <thead><tr><th>Option</th><th>Years included</th><th>Percentage</th><th>Increase</th><th>New rent</th><th>Notice</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["Single rate year", "Current year only", "1.6%", "$3,150.00 × 0.016 = " + C.money(C.U2_16[0]), C.money(C.U2_16[1]), "30 days", ], ["rates", "form571"])}
    {tablerow(["Banked 2020–2024 + current", "1.8 + 0.7 + 2.3 + 3.6 + 1.7 = 10.1%, plus 1.6%", "11.7%", "$3,150.00 × 0.117 = " + C.money(C.U2_117[0]), C.money(C.U2_117[1]), "90 days", ], ["bank", "form571"])}
    {tablerow(["Banked 2020–2025 only", "1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 = 11.5%", "11.5%", "$3,150.00 × 0.115 = " + C.money(C.U2_115[0]), C.money(C.U2_115[1]), "90 days", ], ["bank", "form571"])}
    {tablerow(["Maximum on the 12-month reading", "11.5% banked + 1.6% current", "13.1%", "$3,150.00 × 0.131 = " + C.money(C.U2_131[0]), C.money(C.U2_131[1]), "90 days", ], ["bank", "form571"])}
    {tablerow(["<strong>Recommended: phased</strong>", "A round 10% now; the remainder stays available", "<strong>10.0%</strong>", "$3,150.00 × 0.100 = " + C.money(C.U2_100[0]), C.money(C.U2_100[1]), "90 days", ], ["legistar", "bank"])}
    </tbody>
  </table>
  <p class="note">Every banked figure assumes <strong>no increase has been imposed since 1 June 2019</strong>,
  which is what the owner reported but which has not been evidenced. See <a href="flagged.html#f-03">F-03</a>.
  An increase served now would also fall within the scope of the pending ordinance described on sf.gov, which
  applies to banked increases <em>noticed on or after 15 September 2026</em>. See
  <a href="flagged.html#f-01">F-01</a>.</p>
</section>

<section class="card">
  <h2>What the notice must say for a banked increase</h2>
  <p>Where any part of the increase is banked, the notice should identify which part is banked. In practice that
  means breaking the percentage down by the year it was earned, so that the tenant can check it against the
  published rate table. A notice that simply says 13.1% invites a petition even when the arithmetic is right.</p>
  <p>{srcs(["bank", "rates", "unlawful"])}</p>
</section>

<section class="card">
  <h2>Assumptions, stated plainly</h2>
  <ul class="tight">
    <li>Both units are covered by the Rent Ordinance (1940 building, two units). The certificate of occupancy was not produced — see <a href="flagged.html#f-08">F-08</a>.</li>
    <li>The owner's statement of rent history is accurate and complete — see <a href="flagged.html#f-03">F-03</a>.</li>
    <li>No increase was imposed on Unit 1 before 1 February 2026 and none on Unit 2 since the tenancy began.</li>
    <li>Neither unit is subsidised, which would displace the ordinance arithmetic — see <a href="flagged.html#f-06">F-06</a>.</li>
    <li>No petition-based increase (operating and maintenance, capital improvement, passthrough) is included.</li>
    <li>Base rent excludes any passthrough, and includes any parking or storage charge.</li>
  </ul>
</section>
"""
    return page("units.html", "Units &amp; calculations",
                "Both rent-controlled units with every lawful increase option computed to the cent, the rate years available, the two readings of the banking rule, and the stated assumptions.",
                body, "units.html")


# --------------------------------------------------------------------------------------
# LAWS & CAPS
# --------------------------------------------------------------------------------------
def build_laws():
    law_rows = "\n".join(
        tablerow([f"<strong>{i}</strong>", s], keys)
        for i, s, keys, _ in C.FACTS
    )
    rates_rows = "\n".join(
        f"<tr><td>{p}</td><td class=\"num\">{r}%</td><td class=\"srcell\">{chip('form571')}</td></tr>"
        for p, r in C.RATES
    )
    body = f"""
<section class="card hero">
  <span class="tag">Laws &amp; caps</span>
  <h1>Local, state and federal rules that apply</h1>
  <p class="lead">Twenty-six verified propositions, each with the official source it came from. Where the local
  rule is stricter than the state rule, the local rule governs.</p>
</section>

<section class="card">
  <h2>The legal framework</h2>
  <table>
    <thead><tr><th>Ref</th><th>Rule</th><th>Source</th></tr></thead>
    <tbody>{law_rows}</tbody>
  </table>
</section>

<section class="card">
  <h2>Allowable annual increases, as published</h2>
  <p>The Rent Board publishes the full table back to 1982 in Form 571. These are the nine most recent rate
  years, which are the ones that can matter for a tenancy that began in 2019 or 2025. The 7% statutory maximum
  in §37.3(a)(1) has never been reached in this period; the highest published rate was 7.0% in 1982–84.</p>
  <table>
    <thead><tr><th>Effective period</th><th>Allowable increase</th><th>Source</th></tr></thead>
    <tbody>{rates_rows}</tbody>
  </table>
</section>

<section class="card">
  <h2>How the three layers interact</h2>
  <table>
    <thead><tr><th>Layer</th><th>Ceiling</th><th>Applies here?</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["San Francisco — Rent Ordinance §37.3", "1.6% for 2026–27; 60% of Bay Area CPI change, maximum 7%", "<strong>Yes — this is the governing rule</strong>", ], ["s373", "rates"])}
    {tablerow(["California — Tenant Protection Act, Civ. Code §1947.12", "5% + CPI, maximum 10% (8.8% for this metro area for increases starting 1 August 2026 – 31 July 2027)", "No — expressly inapplicable where a local ordinance restricts increases to a lower amount", ], ["civ1947_12", "oag"])}
    {tablerow(["Federal", "No rent ceiling", "Only the prohibition on discriminatory terms applies", ], ["fha"])}
    </tbody>
  </table>
  <p class="note">The practical effect of the interaction is that the <em>lowest</em> applicable ceiling governs.
  Quoting the 8.8% state figure to a tenant on a covered unit would be a misstatement of the lawful rent.</p>
</section>

<section class="card">
  <h2>Rules that constrain the reason, not the amount</h2>
  <p>These do not change what may be charged, but they decide whether a charge that is arithmetically correct is
  nevertheless unlawful:</p>
  <ul class="tight">
    <li><strong>Discrimination</strong> in the terms of a rental on protected grounds is unlawful under federal
    law, California law and the Rent Ordinance's harassment provision. {srcs(["fha", "gov12955", "discrim"])}</li>
    <li><strong>Retaliation</strong> — an increase within 180 days of a tenant's habitability complaint, or for
    organising, is prohibited. {chip("civ1942_5")}</li>
    <li><strong>Harassment</strong> — a rent increase substantially above market comparables, or within six
    months of an attempt to recover possession, can be evidence of bad faith. {chip("s3710b")}</li>
    <li><strong>Additional occupants</strong> — no extra rent for a new occupant joining an existing tenancy.
    {chip("rates")}</li>
    <li><strong>Algorithmic rent-setting</strong> — sale and use prohibited for San Francisco residential units.
    {chip("s3710c")}</li>
  </ul>
</section>

<section class="card">
  <h2>Not yet law</h2>
  <p>Legistar File #261020, <em>Administrative Code — Cap On Rent Increases for Rent-Controlled Units</em>, would
  limit combined banked and capital-improvement increases to 10% a year for three years. Status as recorded on
  the Board of Supervisors' own system: <strong>Pending Committee Action</strong>, introduced 15 September 2026,
  in the Land Use and Transportation Committee, with a Youth Commission response received 7 October 2026 and no
  final action. sf.gov's own notice states that it has not been enacted. It is therefore <em>not</em> applied to
  any figure in this review, but it is the reason the recommended Unit 2 figure is capped at 10%.</p>
  <p>{srcs(["legistar", "rates", "bank"])}</p>
</section>
"""
    return page("laws.html", "Laws &amp; caps",
                "Local, state and federal rent-increase rules with official sources, the published 2023-2027 rate table, and the pending San Francisco ordinance that would cap banked increases.",
                body, "laws.html")


# --------------------------------------------------------------------------------------
# REASONABLE & NORMAL (incl. corporate vs individual)
# --------------------------------------------------------------------------------------
def build_reasonable():
    body = f"""
<section class="card hero">
  <span class="tag">Reasonable &amp; normal</span>
  <h1>What a reasonable increase means for a rent-controlled unit</h1>
  <p class="lead">For these units "reasonable" is not a matter of judgement or local market custom. The lawful
  ceiling is the normal figure, because the ordinance sets it citywide at 60% of the Bay Area CPI change.</p>
</section>

<section class="card">
  <h2>The benchmark</h2>
  <table>
    <thead><tr><th>Question</th><th>Verified answer</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["What is the lawful ceiling now?", "1.6% for an increase effective 1 March 2026 – 28 February 2027; 1.4% the year before.", ], ["rates", "announce"])}
    {tablerow(["How is it set?", "On 1 March each year the Board publishes the CPI change for the preceding 12 months, and the allowance is 60% of that, never more than 7%.", ], ["s373"])}
    {tablerow(["What is a normal increase in practice?", "For a covered unit, the published allowance applied once a year on the anniversary. Anything larger means a banked breakdown or a granted petition, and either will be examined.", ], ["bank", "s373"])}
    {tablerow(["What is a normal increase for this ZIP code?", "<strong>Blank — no official figure exists.</strong> No government source publishes a lawful or market rent benchmark at ZIP level, so none is asserted here.", ], ["oag", "form571"])}
    {tablerow(["Can market rent be used as the target?", "<strong>No.</strong> A covered unit's rent can only reach market through the mechanisms in the ordinance — banked years, a granted petition, or a lawful vacancy reset. The owner cannot simply move the rent toward market because it is below it.", ], ["s373", "civ1954_53"])}
    {tablerow(["Is 1.6% below the cost of living?", "That is a policy question the ordinance answers, not a legal one. The formula is 60% of CPI by design, so the allowance normally lags CPI. Disagreement with it is not a lawful basis for charging more.", ], ["s373"])}
    </tbody>
  </table>
</section>

<section class="card">
  <h2>How large owners and individual owners actually differ</h2>
  <p>The rules are identical. What differs is process discipline, and that is what decides whether an increase
  survives review.</p>
  <table>
    <thead><tr><th>Element</th><th>Portfolio owner</th><th>Individual owner of one or two units</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["Legal ceiling", "Identical — no corporate exemption and no higher allowance", "Identical", ], ["s373", "inventory"])}
    {tablerow(["Applying the allowance", "Calendar-driven: the published percentage applied on each anniversary without a decision each year", "Often skipped in busy years, which is where banking records are lost", ], ["rates", "bank"])}
    {tablerow(["Reporting and licence", "Kept current as a standing compliance task; bulk upload available for properties of five or more units", "Frequently missed, because the 1 March deadline is easy to overlook", ], ["inventory", "s3715"])}
    {tablerow(["Rent records", "Retained in a management system, which makes a banked calculation provable", "Often scattered across leases, emails and bank statements", ], ["bank", "unlawful"])}
    {tablerow(["Notice", "Templated and served with tracked proof of service", "Commonly drafted per occasion, which is where the 30/90-day and content errors arise", ], ["civ827", "ccp1013"])}
    {tablerow(["Rent-setting software", "Sold to larger owners; <strong>now prohibited</strong> for San Francisco residential units", "Not applicable", ], ["s3710c"])}
    {tablerow(["Data on relative increase rates", "<strong>No official dataset exists</strong> comparing corporate and individual owners' increases", "<strong>No official dataset</strong>", ], ["ordinance", "inventory"])}
    </tbody>
  </table>
  <p class="note">The last row matters. It is often asserted that corporations raise rents faster than small
  owners. No official source in the record supports a figure either way, so the claim is not made here and is
  published instead as an open item on <a href="flagged.html#f-07">F-07</a>.</p>
</section>

<section class="card">
  <h2>What is genuinely normal, and defensible</h2>
  <ol class="tight">
    <li>One written rule for the whole property: <em>"each covered unit is increased annually by the Rent Board's
    allowable percentage, plus any banked percentage that has been properly earned, applied on that unit's
    anniversary date."</em></li>
    <li>Applying it every year, even when the amount is small. The allowance is lost if it is not banked, and
    losing it is not reversible.</li>
    <li>Phasing a large accumulated figure rather than serving it in one notice.</li>
    <li>Notifying a few weeks earlier than the statutory minimum, so the effective date holds even if service is
    disputed.</li>
    <li>Keeping every notice and proof of service. A petition can be filed years later, with no deadline.</li>
  </ol>
  <p>{srcs(["rates", "bank", "unlawful"])}</p>
</section>
"""
    return page("reasonable.html", "Reasonable &amp; normal",
                "What counts as a reasonable and normal rent increase for rent-controlled San Francisco units, and how large owners differ from individual owners in practice, with official sources.",
                body, "reasonable.html")


# --------------------------------------------------------------------------------------
# NOTICE & REASONS
# --------------------------------------------------------------------------------------
def build_notice():
    body = f"""
<section class="card hero">
  <span class="tag">Notice &amp; reasons</span>
  <h1>How to tell the tenants, and what may be said as the reason</h1>
  <p class="lead">The procedure is fixed by statute and is the part most often got wrong. The reason is
  narrower than most owners expect: for an annual or banked increase, the reason <em>is</em> the ordinance
  formula, and the legal risk lies in what must not be said or relied upon.</p>
</section>

<section class="card">
  <h2>The notice requirements</h2>
  <table>
    <thead><tr><th>Requirement</th><th>Detail</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["Form", "Written notice served on the tenant. Personal delivery, or service by mail.", ], ["civ827"])}
    {tablerow(["30 days", "Required where the increase is <strong>10% or less</strong> of the rent charged at any time in the previous 12 months, alone or combined with other increases in that period.", ], ["civ827"])}
    {tablerow(["90 days", "Required where the increase is <strong>more than 10%</strong> on the same measure. A banked catch-up on Unit 2 will usually cross this line.", ], ["civ827"])}
    {tablerow(["Mailed notice", "Add <strong>5 calendar days</strong> when both the place of mailing and the address are in California.", ], ["ccp1013"])}
    {tablerow(["Dollar amount", "State the dollar amount of the increase.", ], ["rates"])}
    {tablerow(["Percentage", "State the percentage, using the rate in effect on the <strong>effective date</strong> of the increase.", ], ["rates"])}
    {tablerow(["Effective date", "State the date the new rent takes effect. It must be at least 12 months after the tenancy began or the last increase.", ], ["rates"])}
    {tablerow(["Banked breakdown", "Where part of the increase is banked, state which part, ideally broken down by the year each portion was earned.", ], ["bank"])}
    {tablerow(["No rounding", "The increase may not be rounded up to the nearest dollar.", ], ["rates"])}
    {tablerow(["Base rent only", "Calculate on base rent, including any parking or storage charge, and excluding passthroughs.", ], ["rates"])}
    {tablerow(["Licence", "The licence does not have to be enclosed with the notice, but it must exist on the effective date.", ], ["inventory"])}
    </tbody>
  </table>
</section>

<section class="card">
  <h2>Model notice — placeholders only</h2>
  <div class="letter">
    <p class="meta">[Date] · Served on [Tenant label] by [personal delivery / first-class mail]</p>
    <p><strong>NOTICE OF RENT INCREASE</strong></p>
    <p>To: [Tenant label], [Unit label], San Francisco, CA</p>
    <p>Under the San Francisco Residential Rent Stabilization and Arbitration Ordinance (Administrative Code
    Chapter 37) and California Civil Code section 827, your base rent will change as follows:</p>
    <table class="mini">
      <tr><td>Current base rent</td><td>$[amount] per month</td></tr>
      <tr><td>Annual allowable increase, [rate period]</td><td>[x.x]% = $[amount]</td></tr>
      <tr><td>Banked increase, [year] at [x.x]%</td><td>$[amount]</td></tr>
      <tr><td>Total increase</td><td>[x.x]% = $[amount]</td></tr>
      <tr><td>New base rent</td><td>$[amount] per month</td></tr>
      <tr><td>Effective date</td><td>[date]</td></tr>
    </table>
    <p>The rent-increase licence required by Administrative Code section 37.15 is on file with the San
    Francisco Rent Board for this unit.</p>
    <p>[Owner name] · [Owner contact for questions]</p>
  </div>
  <p>{srcs(["civ827", "rates", "bank", "s3715"])}</p>
  <p class="note">This is a model for review by a California attorney, not a form to serve unaltered. Delete the
  banked line if no part of the increase is banked.</p>
</section>

<section class="card">
  <h2>Reasonable reasons — and reasons that create liability</h2>
  <table>
    <thead><tr><th>Category</th><th>Examples</th><th>Status</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["The ordinance allowance", "The Rent Board's published annual percentage applied on the anniversary", "<strong>Lawful, no justification needed</strong>", ], ["rates", "s373"])}
    {tablerow(["Documented banking", "Rate years earned and not used, itemised by year", "<strong>Lawful</strong>, subject to the threshold question at F-02", ], ["bank"])}
    {tablerow(["Granted petition", "Operating and maintenance expenses; certified capital improvements; utility or bond passthroughs", "<strong>Lawful only if the petition is granted</strong>, and not assumed in this review", ], ["s373"])}
    {tablerow(["Costs rising", "Insurance, taxes, maintenance, mortgage costs", "<strong>Not a lawful reason on its own</strong> for a covered unit. It is the reason a petition exists.", ], ["s373"])}
    {tablerow(["Market rent is higher", "Comparable units let for more", "<strong>Not a lawful reason on its own.</strong> It is what a §6.14 notice or a vacancy reset is for, and neither applies here", ], ["s614", "civ1954_53"])}
    {tablerow(["Tenant conduct", "Complaints, requests for repairs, organising, or a disagreement", "<strong>Unlawful if retaliatory</strong>", ], ["civ1942_5"])}
    {tablerow(["Who the tenant is", "Any protected characteristic, or source of income including a voucher", "<strong>Unlawful discrimination</strong>", ], ["gov12955", "fha", "discrim"])}
    {tablerow(["A person moved in", "An extra occupant joining an existing tenancy", "<strong>Unlawful</strong> — no extra rent may be charged", ], ["rates"])}
    </tbody>
  </table>
</section>

<section class="card">
  <h2>If the tenant disputes it</h2>
  <p>A tenant in a covered unit can file an Unlawful Rent Increase Petition with the Rent Board. There is no
  filing fee and <strong>no time limit</strong>. The case is usually mediated, and if not it goes to a hearing
  before an Administrative Law Judge. The hearing is informal and counsel is not required, though both sides may
  be represented.</p>
  <p>If the notice is defective but the increase has not yet taken effect, a Tenant Summary Petition can be used
  instead, which prompts the Board to write to the owner.</p>
  <p>{srcs(["unlawful", "petitions", "noncompliance"])}</p>
  <p class="note">This is why the file matters more than the argument. An itemised, correctly calculated notice
  with proof of service and a licence record settles most petitions before a hearing.</p>
</section>
"""
    return page("notice.html", "Notice &amp; reasons",
                "How to serve a San Francisco rent increase notice: 30 and 90 day periods, mailing extension, required content, a model notice with placeholders, and which reasons are lawful.",
                body, "notice.html")


# --------------------------------------------------------------------------------------
# TENANT-LAWYER TEST
# --------------------------------------------------------------------------------------
def build_review():
    tests = [
        ("1", "Is there a licence on the effective date?",
         "Look the property up in the Rent Board Portal and check the licence record for the exact date the increase takes effect, not the date the notice was served. No licence means no enforceable increase, whatever the percentage.",
         ["inventory", "noncompliance"]),
        ("2", "Is the amount at or below the published allowance?",
         "Recompute it. Base rent × the rate in force on the effective date. Check that nothing was rounded up and that no passthrough was folded into the base.",
         ["rates", "form571"]),
        ("3", "Is any banked portion actually bankable?",
         "Itemise each year claimed, check each against Form 571, and check the gap requirement. This is the weakest link in the file and is disputed between official pages — see F-02.",
         ["bank", "form571"]),
        ("4", "Has 12 months passed, and on the right anniversary?",
         "Count from the tenancy start or the last increase. For Unit 1 the anniversary is 1 February, not 1 April: a continuing tenancy with an added occupant does not restart it.",
         ["rates"]),
        ("5", "Was the notice the right length and content?",
         "30 or 90 days by the size of the increase, plus 5 days if mailed. Dollar, percentage, effective date, and the banked breakdown.",
         ["civ827", "ccp1013", "bank"]),
        ("6", "Is the reason free of protected grounds?",
         "Any reference to who the tenant is, to a voucher, to family composition, to a complaint, or to organising is fatal.",
         ["gov12955", "fha", "civ1942_5"]),
        ("7", "Was the increase used to pressure the tenant out?",
         "A rent increase substantially above market comparables, or within six months of an attempt to recover possession, can be evidence of bad faith harassment.",
         ["s3710b"]),
        ("8", "Is the tenant being charged for the extra occupant?",
         "Unit 1 gained an occupant. If any part of the increase is attributable to that, it is unlawful.",
         ["rates"]),
        ("9", "Is the same policy applied to both units?",
         "Write the policy down. Differences explained by anniversary date and rent history are defensible; differences explained by the tenants are not.",
         ["discrim", "gov12955"]),
    ]
    rows = "\n".join(
        tablerow([f"<strong>{n}</strong>", f"<strong>{esc(t)}</strong><p>{d}</p>"], keys)
        for n, t, d, keys in tests
    )
    body = f"""
<section class="card hero">
  <span class="tag">Tenant-lawyer test</span>
  <h1>Would a free tenant-side lawyer accept these increases?</h1>
  <p class="lead">San Francisco tenants' access to free counsel means an increase will be tested adversarially,
  and procedure is tested before policy. The nine checks below are the ones that actually decide cases, ordered
  so that the cheapest objection comes first.</p>
</section>

<section class="card">
  <h2>The nine checks</h2>
  <table class="steps">
    <thead><tr><th>#</th><th>Check and what would satisfy it</th><th>Source</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <p class="note">An increase that passes all nine is ordinary business practice and should survive review. An
  increase that fails any one of the first five will be overturned regardless of how reasonable the percentage
  looks.</p>
</section>

<section class="card">
  <h2>One unit or both?</h2>
  <table>
    <thead><tr><th>Approach</th><th>Lawful?</th><th>Risk</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["Raise both, by the same written rule", "<strong>Yes</strong>", "<strong>Lowest.</strong> A uniform policy answers the discrimination and retaliation question before it is asked. This is normal practice.", ], ["discrim", "gov12955"])}
    {tablerow(["Raise one only, without a documented objective reason", "<strong>Not automatically unlawful</strong>", "<strong>High.</strong> It invites an inquiry into why, and the owner carries the burden of explaining it.", ], ["gov12955", "civ1942_5"])}
    {tablerow(["Raise one only, with a documented objective reason", "Yes", "Moderate. Defensible if the reason is genuinely objective — a different anniversary, a different rent history, a decision to phase one unit for cash-flow reasons recorded in writing.", ], ["discrim", "civ1942_5"])}
    {tablerow(["Raise one only because of who lives there", "<strong>No</strong>", "Unlawful discrimination or harassment.", ], ["gov12955", "s3710b"])}
    </tbody>
  </table>
  <p><strong>Recommendation:</strong> adopt one written policy for the property — the published allowance plus
  properly earned banked years, applied on each unit's anniversary — and apply it to both units. The resulting
  amounts will differ, because the tenancy histories differ, and that difference is the explanation.</p>
</section>

<section class="card">
  <h2>Where the tenants can get free help</h2>
  <table>
    <thead><tr><th>Service</th><th>What it covers</th><th>Contact</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["Rent Board counselling", "Whether a unit is covered, how an increase should be calculated, how to file a petition", "415-252-4600", ], ["laws", "petitions"])}
    {tablerow(["Unlawful Rent Increase Petition", "Challenging the amount, the notice or the licence. No fee, no deadline.", "Rent Board, 25 Van Ness Avenue, Suite 700", ], ["unlawful"])}
    {tablerow(["Eviction Defense Collaborative", "Free legal help for tenants who have received eviction court papers", "415-659-9184", ], ["resources"])}
    {tablerow(["Housing Rights Committee and other tenant counselling organisations", "General tenant counselling, multiple languages", "415-703-8644", ], ["resources"])}
    {tablerow(["San Francisco Human Rights Commission", "Discrimination complaints", "Via sf.gov", ], ["discrim"])}
    {tablerow(["California Civil Rights Department", "State fair-housing complaints", "800-884-1684", ], ["discrim", "crd"])}
    {tablerow(["U.S. Department of Housing and Urban Development", "Federal fair-housing complaints", "800-347-3739", ], ["discrim", "fha"])}
    </tbody>
  </table>
  <p class="note">A tenant who is represented will usually raise the licence question first, because it is
  decisive and easy to check. That is the single strongest argument for doing the Housing Inventory reporting
  before anything else.</p>
</section>
"""
    return page("review.html", "Tenant-lawyer test",
                "The nine checks a free San Francisco tenant-side lawyer would apply to a rent increase, whether to raise one unit or both, and where tenants can get free help.",
                body, "review.html")


# --------------------------------------------------------------------------------------
# SOURCES
# --------------------------------------------------------------------------------------
def build_sources():
    groups = [
        ("San Francisco — Rent Board and sf.gov", ["rates", "announce", "form571", "bank", "multiyear", "irregular", "inventory", "noncompliance", "s3715", "s373", "s3710b", "s3710c", "ordinance", "laws", "petitions", "unlawful", "resources", "s614", "discrim", "portal", "legistar"]),
        ("California statutes and statewide guidance", ["civ827", "civ1942_5", "civ1947_12", "civ1954_53", "ccp1013", "gov12955", "oag", "crd"]),
        ("Federal", ["fha"]),
    ]
    sections = []
    n = 0
    for heading, keys in groups:
        rows = []
        for k in keys:
            n += 1
            label, url, _ = C.SRC[k]
            attr = html.escape(url, quote=True)
            rows.append(
                f'<tr><td class="num">{n}</td><td><a href="{attr}">{esc(label)}</a></td>'
                f'<td class="url"><code>{html.escape(url)}</code></td>'
                f'<td>Fetched and read 10 Nov 2026</td></tr>'
            )
        sections.append(f"""
<section class="card">
  <h2>{heading}</h2>
  <table>
    <thead><tr><th>#</th><th>Source</th><th>URL</th><th>Retrieved</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</section>""")
    body = f"""
<section class="card hero">
  <span class="tag">Sources</span>
  <h1>Source register</h1>
  <p class="lead">Every figure and rule in this review traces to one of these {n} documents, each fetched and
  read on 10 November 2026. Nothing here is drawn from a secondary commentary, a blog, a law firm page or a
  news article.</p>
</section>
{''.join(sections)}
<section class="card">
  <h2>How the verification was done</h2>
  <ol class="tight">
    <li>Each source was retrieved directly from its publisher on 10 November 2026 and read in full, not
    summarised from a search result.</li>
    <li>Each rate was read from Form 571 and cross-checked against the Rent Board's announcement for the same
    year. The two agreed for every year used.</li>
    <li>Each arithmetic result was recomputed in code from the published percentage and the stated base rent,
    with the result asserted at build time, so a wrong figure fails the build rather than reaching the page.</li>
    <li>Each table row is required by an automated check to carry at least one link to an official domain.
    A row with no official source fails the build.</li>
    <li>Where two official pages disagree, both readings are published and the disagreement is listed on
    <a href="flagged.html">Flagged for review</a> instead of being resolved by preference. See F-02.</li>
    <li>Values that no official source supports — the ZIP-level benchmark, the comparative corporate-versus-
    individual data — are left <strong>blank</strong> and flagged, not filled with an estimate.</li>
  </ol>
</section>
<section class="card">
  <h2>Sources deliberately not used</h2>
  <p>Law-firm summaries, landlord-association guidance, tenant-advocacy explainers and news coverage of the
  pending ordinance were consulted to identify <em>which</em> questions to ask, but no figure, rule or conclusion
  in this review rests on any of them. Where such material made a claim, the claim was traced back to the
  official document before being included.</p>
</section>
"""
    return page("sources.html", "Sources",
                "Register of the official sources used, with URLs and retrieval date, and a description of the verification method.",
                body, "sources.html")


# --------------------------------------------------------------------------------------
# FLAGGED FOR REVIEW
# --------------------------------------------------------------------------------------
def build_flagged():
    rows = []
    for fid, sev, title, detail, action, keys in C.FLAGS:
        anchor = fid.lower().replace("-", "-")
        rows.append(f"""
<tr id="{anchor}">
  <td class="nowrap"><strong>{fid}</strong></td>
  <td><span class="pill sev-{sev.lower()}">{sev}</span></td>
  <td><strong>{title}</strong><p>{detail}</p><p class="action"><em>What would close it:</em> {action}</p></td>
  <td class="srcell">{srcs(keys)}</td>
</tr>""")
    body = f"""
<section class="card hero warn">
  <span class="tag">Flagged</span>
  <h1>Flagged for review</h1>
  <p class="lead">Nine items that are unverified, disputed between official sources, or not yet law. None of them
  blocks the published analysis; each one is recorded here with its source so it can be checked and closed.
  Nothing on the list has been filled in with an estimate.</p>
</section>

<section class="card">
  <table class="flags">
    <thead><tr><th>Ref</th><th>Severity</th><th>Item, why it is flagged, and what would close it</th><th>Source</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</section>

<section class="card">
  <h2>The three that change a number</h2>
  <table>
    <thead><tr><th>Flag</th><th>Effect if the worse reading holds</th><th>Source</th></tr></thead>
    <tbody>
    {tablerow(["<a href='#f-01'>F-01</a> — pending 10% cap", "A Unit 2 notice above 10% served now could be reduced to 10% if File #261020 is enacted, because sf.gov states it would apply to banked increases noticed on or after 15 September 2026. The recommended 10.0% ($315.00) is unaffected either way.", ], ["legistar", "rates"])}
    {tablerow(["<a href='#f-02'>F-02</a> — banking threshold", "On the 24-month reading, Unit 1 loses the 1.4% (leaving 1.6% = $63.92) and Unit 2 loses one year, so 13.1% becomes 11.7% ($368.55).", ], ["bank", "multiyear"])}
    {tablerow(["<a href='#f-03'>F-03</a> — Unit 2 rent history", "If any increase was imposed on Unit 2 since 2019, every banked figure falls and the anniversary date may move. No banked notice should be served before the ledger is assembled.", ], ["bank", "rates"])}
    </tbody>
  </table>
</section>

<section class="card">
  <h2>How to close an item</h2>
  <p>Each entry states what would close it. In most cases that means one of three things: a document the owner
  holds (lease, ledger, notice), a written answer from a Rent Board counsellor on 415-252-4600, or a final
  action recorded on the Board of Supervisors' own legislation system. When an item is closed, the figure it
  affects can be restated with certainty; until then the conservative figure is the one to rely on.</p>
</section>
"""
    return page("flagged.html", "Flagged for review",
                "Items that are unverified, disputed between official sources or not yet law, each with the source link and what would close it.",
                body, "flagged.html")


# --------------------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------------------
CSS = """
:root{
  --ink:#15202b; --muted:#5b6b7c; --line:#dfe6ee; --bg:#f6f8fb; --card:#fff;
  --accent:#0b5d8f; --accent-soft:#eef5fb; --warn:#b42318; --warn-soft:#fef3f0;
  --good:#12703f; --good-soft:#eef8f2; --radius:10px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  color:var(--ink);background:var(--bg)}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.skip{position:absolute;left:-9999px}
.skip:focus{left:12px;top:12px;background:#fff;padding:8px 12px;z-index:99;border-radius:6px}
header.top{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20}
header.top .wrap{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;
  padding-top:14px;padding-bottom:14px}
.brand{display:flex;gap:10px;align-items:center;min-width:0}
.mark{width:36px;height:36px;border-radius:9px;background:var(--accent);color:#fff;display:grid;
  place-items:center;font-weight:700;font-size:.85rem;flex:none}
.brand-title{font-weight:700;font-size:1rem;line-height:1.2}
.brand-sub{font-size:.76rem;color:var(--muted);line-height:1.3}
nav.main{display:flex;flex-wrap:wrap;gap:2px}
nav.main a{padding:6px 10px;border-radius:7px;font-size:.85rem;color:var(--muted)}
nav.main a:hover{background:var(--accent-soft);text-decoration:none;color:var(--accent)}
nav.main a.active{background:var(--accent);color:#fff}
main{padding:26px 0 10px}
h1{font-size:1.6rem;line-height:1.25;margin:.2em 0 .5em}
h2{font-size:1.16rem;margin:0 0 .55em;line-height:1.3}
h3{font-size:1rem;margin:1.1em 0 .4em}
p{margin:.55em 0}
ul,ol{margin:.5em 0;padding-left:1.35em}
li{margin:.3em 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:20px 22px;margin:0 0 18px}
.card.hero{border-top:5px solid var(--accent)}
.card.highlight{border-left:4px solid var(--accent);background:var(--accent-soft)}
.card.warn{border-top:5px solid var(--warn)}
.tag{display:inline-block;font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;
  background:var(--accent-soft);border:1px solid #cfe0ef;color:var(--accent);padding:3px 9px;
  border-radius:999px;font-weight:700;margin-bottom:10px}
.lead{font-size:1.04rem;color:#243342}
.note{background:#fbfcfe;border-left:3px solid var(--accent);padding:10px 14px;border-radius:0 6px 6px 0;
  font-size:.93rem}
.small{font-size:.87rem;color:var(--muted)}
.grid{display:grid;gap:14px;margin:16px 0}
.grid.two{grid-template-columns:repeat(2,minmax(0,1fr))}
.grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}
.grid.four{grid-template-columns:repeat(4,minmax(0,1fr))}
@media(max-width:860px){.grid.four,.grid.three{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:560px){.grid.four,.grid.three,.grid.two{grid-template-columns:1fr}}
.kpi,.stat{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px}
.kpi{align-self:stretch}
.kpi-value{font-size:1.5rem;font-weight:700;color:var(--accent);line-height:1.1}
.kpi-label{font-size:.84rem;color:#31404f;margin-top:4px}
.kpi-src{font-size:.75rem;margin-top:6px}
.stat .num{font-size:1.35rem;font-weight:700;color:var(--accent)}
.stat .lbl{font-size:.82rem;color:var(--muted)}
.linkcard{display:block;background:#fff;border:1px solid var(--line);border-radius:var(--radius);
  padding:14px 16px;color:var(--ink)}
.linkcard:hover{border-color:var(--accent);text-decoration:none}
.linkcard strong{display:block;color:var(--accent);margin-bottom:4px}
.linkcard span{font-size:.86rem;color:var(--muted)}
table{width:100%;border-collapse:collapse;margin:12px 0;font-size:.9rem;background:#fff}
th,td{text-align:left;vertical-align:top;padding:9px 11px;border-bottom:1px solid var(--line)}
th{background:#f1f5f9;font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;color:#40556b;
  font-weight:700;border-bottom:2px solid var(--line)}
tr:last-child td{border-bottom:none}
tbody tr:hover{background:#fbfdff}
td p{margin:.35em 0 0;font-size:.88rem;color:#3c4c5c}
td.num{white-space:nowrap;font-variant-numeric:tabular-nums}
td.nowrap{white-space:nowrap}
td.step{font-weight:700;color:var(--accent);font-size:1.05rem;width:2.2em}
td.srcell{font-size:.76rem;min-width:130px}
td.srcell a{display:inline-block;margin:0 0 3px}
.src{display:inline-block;background:var(--accent-soft);border:1px solid #cfe0ef;color:var(--accent);
  padding:1px 7px;border-radius:999px;font-size:.72rem;line-height:1.5;white-space:nowrap}
.src:hover{background:var(--accent);color:#fff;text-decoration:none}
table.mini{font-size:.88rem}
table.mini td{border-bottom:1px dashed var(--line);padding:6px 8px}
.letter{background:#fffdf6;border:1px solid #e8dfc4;border-radius:8px;padding:18px 20px;margin:14px 0;
  font-size:.92rem}
.letter .meta{font-size:.8rem;color:var(--muted)}
.pill{display:inline-block;font-size:.72rem;font-weight:700;padding:2px 9px;border-radius:999px}
.sev-high{background:var(--warn-soft);color:var(--warn);border:1px solid #f3c3bb}
.sev-medium{background:#fff7e6;color:#8a5a00;border:1px solid #f0dcb0}
.sev-low{background:var(--good-soft);color:var(--good);border:1px solid #bfe3ce}
.action{color:var(--accent)!important;font-weight:600}
code{font-size:.8em;background:#f1f5f9;padding:1px 4px;border-radius:4px;word-break:break-all}
td.url code{background:transparent;padding:0}
footer{border-top:1px solid var(--line);margin-top:26px;padding:22px 20px 40px;font-size:.86rem;
  color:var(--muted)}
footer p{margin:.6em 0}
@media print{header.top{position:static}nav.main{display:none}.card{break-inside:avoid}}
"""


def build_index(dest=None, prefix="", active="index.html"):
    """Dashboard. dest/prefix let the same content be published at site/ and at the root."""
    body = _index_body()
    return page("index.html", "Dashboard", INDEX_DESC, body, active,
                dest=dest, prefix=prefix)


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "assets").mkdir(exist_ok=True)
    (OUT / "assets" / "style.css").write_text(CSS, encoding="utf-8")

    # This edition is ADDITIVE. The canonical root site (index.html + pages/ + assets/style.css) is
    # owned by another session and is left untouched: overwriting it would discard that session's
    # published work, which the coordination rules forbid. Everything this builder writes lives
    # under site/, and the only change it makes outside site/ is a single link in the root
    # index.html pointing here (see tools/link_consolidated.py).
    built = [
        build_index(),
        build_exec(),
        build_process(),
        build_units(),
        build_laws(),
        build_reasonable(),
        build_notice(),
        build_review(),
        build_sources(),
        build_flagged(),
    ]
    print(f"built {len(built)} pages in {OUT.relative_to(ROOT)}/ (root site untouched)")


if __name__ == "__main__":
    main()
