"""Reference pages: sources register, requirements checklist, flagged for review."""
from site_layout import SRC, src, srcs, cell, page

RETRIEVED = "10 Nov 2026"

# key, what it supports
USED_FOR = {
    "SF_LI": "Current allowable percentage (1.6%), base-rent rule, no-rounding rule, anniversary rules, 30/90-day notice elements, additional-occupant prohibition, vacancy pricing, the 9 Nov 2026 notice on File #261020",
    "SF_BANK": "24-month banking condition, additive-not-compounded rule, no cap back to 1 Apr 1982, no expiry, prior-owner transfer, banked notice elements, licence precondition",
    "SF_HI": "All-owner reporting duty, automatic licence, 1 Mar deadline, 1–9 unit start date of 1 Mar 2023, licence on effective date, no monetary penalty, what is reported",
    "SF_NONCOMP": "Consequence of an unlicensed increase: the notice “may be null and void (this may apply for multiple years)” and the tenant “may be entitled to a rent refund”; Tenant Summary Petition route while a notice has not yet taken effect; how to check licence status in the Portal",
    "SF_LAWS": "Coverage of pre-13 June 1979 buildings, excluded/partially exempt categories, counsellor line",
    "SF_571": "The official allowable-increase table 1982–2027 (all percentages used on this site)",
    "SF_MULTI": "Multi-year methodology, additive rule, no petition required, no rounding, base rent only",
    "SF_TENPET": "Tenant petition types, free filing, Rent Board's lack of jurisdiction over discrimination/retaliation",
    "SF_UNLAWFUL": "Unlawful-rent-increase petition (Form 516C box C), no filing deadline, hearing before an ALJ, no lawyer needed",
    "SF_LANDPET": "Six petition-based increases; petition before notice; free filing",
    "SF_SPECIAL": "Comparable-rent petition conditions; long-standing below-market rent is not an extraordinary circumstance; petition before notice",
    "SF_ALGO": "Rent Ordinance § 37.10C — algorithmic pricing devices banned, effective 14 Oct 2024",
    "SF_COUNSEL": "Rent Board counselling hours and telephone number",
    "SF_FEE": "Separate annual Rent Board Fee ($59.00 per dwelling unit for 2026–27, due 1 Mar, 5%/mo penalty up to 15%, 50% tenant recovery, 14 Dec 2026 exemption deadline)",
    "SF_614": "Rent Board Rule § 6.14 and Costa-Hawkins roommate/subtenant rules: unlimited increase only after last original occupant vacates and never against a co-tenant",
    "SF_PORTAL": "Rent Board Portal — reporting and licence look-up",
    "ADMIN_373": "Administrative Code § 37.3 — Rent Limitations: § 37.3(a)(1)–(2) annual/banking & § 37.15 licence, (a)(8) petitions, (a)(10) vouchers, (a)(11) additional occupants, (b)(1)&(5) notice breakdown & null-and-void rule, (d)(2)(B) partial occupancy changes",
    "LEGISTAR_261020": "File #261020 status (Pending Committee Action) and its 10%/yr proposed cap",
    "LEG_827": "30-day / 90-day notice rule, delivery methods, 10%-threshold calculation",
    "LEG_1947": "AB 1482 cap and the local-ordinance exemption; new-tenancy initial rent",
    "LEG_1954": "Costa-Hawkins: initial rent for a new tenancy, with exceptions",
    "LEG_1942": "180-day retaliation bar; tenant-organising protection",
    "LEG_1013": "5-day mail extension (in California), 10 days out of state, 2 court days for overnight",
    "LEG_12955": "FEHA housing discrimination grounds; harassment; protected characteristics",
    "OAG": "Statewide AB 1482 maxima by region (8.8% for the San Francisco area, 1 Aug 2026 – 31 Jul 2027)",
    "CRD": "Civil Rights Department enforcement, protected characteristics, complaint route",
    "USC_3604": "Federal Fair Housing Act — discrimination in rental terms and conditions",
    "DOJ_ALGO": "Federal antitrust suit against six large landlords over algorithmic rent pricing",
}


def sources():
    rows = ""
    for key in SRC:
        title, url = SRC[key]
        rows += ('<tr><td class="nowrap"><code>%s</code></td><td>%s</td><td>%s</td>'
                 '<td class="srccell"><a href="%s" target="_blank" rel="noopener">%s</a></td></tr>'
                 % (key, title, USED_FOR.get(key, ""), url, url))
    body = f"""
<div class="card">
  <h1>Sources &amp; verification register</h1>
  <p class="lede">Every official source used on this site, the claim it supports, and the date it was retrieved. All were fetched and read on 10 November 2026.</p>
</div>

<div class="card">
  <h2>What “verified” means here</h2>
  <table>
    <thead><tr><th style="width:26%">Standard</th><th>How it is applied</th><th style="width:20%">Official source</th></tr></thead>
    <tbody>
      <tr><td>Primary sources only</td><td>Rules are quoted from City, State and federal publications — not from law firms, news articles, listing sites or advocacy groups.</td>{cell("SF_LI", "LEG_827")}</tr>
      <tr><td>One link per row</td><td>Every table row on this site carries a link to the official page that supports it; the automated check fails the build if a row has none.</td>{cell("SF_571", "ADMIN_373")}</tr>
      <tr><td>No inferred values</td><td>If a figure is not published officially, the cell is left blank and the item appears on the Flagged page.</td>{cell("SF_LI")}</tr>
      <tr><td>Arithmetic shown</td><td>Dollar amounts are the official percentage multiplied by the owner-reported base rent, to the cent, with no rounding up.</td>{cell("SF_571")}</tr>
      <tr><td>Ownership facts separated</td><td>Owner-reported facts (rents, dates, tenants) are labelled as such and are never presented as government records.</td>{cell("SF_HI")}</tr>
      <tr><td>Pending law labelled</td><td>File #261020 is described as pending, with its Legistar status, never as law.</td>{cell("LEGISTAR_261020")}</tr>
      <tr><td>Conflicting official texts published</td><td>Where two official pages differ, both are quoted and the difference is flagged (FR-03).</td>{cell("SF_BANK", "SF_LI")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>Register ({len(SRC)} sources)</h2>
  <table>
    <thead><tr><th style="width:9%">Key</th><th style="width:26%">Source</th><th>Claim it supports</th><th style="width:24%">URL (retrieved {RETRIEVED})</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>Reproducing the verification</h2>
  <p>The site is a static build. The checks that gate publication are:</p>
  <ul class="tight">
    <li><code>python3 tools/verify_core_site.py</code> — every internal link and anchor resolves; every table row links an official domain; privacy scan; arithmetic assertions; no remote scripts.</li>
    <li>Manual re-read of each cited page on {RETRIEVED}, with the quoted wording compared to the page text.</li>
    <li>Cross-checks: 1.6% appears on both the Rent Board page and document 571; 1.4% appears on document 571 and in the Rent Board's prior-year example; 8.8% appears on the Attorney General's regional table.</li>
  </ul>
  <p class="small">Sources: {srcs("SF_LI", "SF_571", "OAG")}</p>
</div>
"""
    return page("pages/sources.html", "Sources &amp; verification register", body,
                "Register of every official source used, the claim each supports, and the verification standard applied.")


# ------------------------------------------------------------------ requirements
REQS = [
    ("R-01", "Answer whether an individual (non-corporate) owner must inform the Rent Board and obtain a licence before notifying tenants", "Answered", "pages/process.html", "SF_HI"),
    ("R-02", "Put that answer at the forefront of the executive summary", "Answered", "pages/executive-summary.html", "SF_HI"),
    ("R-03", "Explain the process step by step for someone with no experience", "Answered", "pages/process.html", "SF_LI"),
    ("R-04", "Provide official, verified links for each step", "Answered", "pages/sources.html", "SF_571"),
    ("R-05", "Collect, organise and analyse a full list of requirements", "Answered", "pages/requirements.html", "SF_HI"),
    ("R-06", "Executive summary outlining the important details", "Answered", "pages/executive-summary.html", "SF_LI"),
    ("R-07", "Reasonable and normal increase for Unit A under local, state and federal law", "Answered", "pages/units.html", "SF_571"),
    ("R-08", "Reasonable and normal increase for Unit B under local, state and federal law", "Answered — conditional on rent history", "pages/units.html", "SF_BANK"),
    ("R-09", "Confirm rent-control status of a 1940 two-unit building", "Owner-reported; government record not obtained", "pages/laws.html", "SF_LAWS"),
    ("R-10", "State the local cap, the state cap and the federal position", "Answered", "pages/laws.html", "LEG_1947"),
    ("R-11", "Explain whether the ZIP code changes the answer", "Answered — no ZIP-level rate exists", "pages/reasonable.html", "SF_LI"),
    ("R-12", "How large real-estate corporations handle increases", "Answered within official evidence; statistics unavailable", "pages/practice.html", "DOJ_ALGO"),
    ("R-13", "How individual owners handle increases", "Answered", "pages/practice.html", "SF_LI"),
    ("R-14", "Correct way to inform tenants of an increase", "Answered", "pages/notice.html", "LEG_827"),
    ("R-15", "Reasonable reasons for an increase", "Answered", "pages/notice.html", "SF_LANDPET"),
    ("R-16", "Test the increases against what a tenant lawyer would review", "Answered — 16-point test", "pages/review.html", "SF_UNLAWFUL"),
    ("R-17", "Decide whether to raise one unit or both to avoid discrimination exposure", "Answered", "pages/discrimination.html", "LEG_12955"),
    ("R-18", "Anonymise all personal information, keep dates and amounts", "Answered — placeholders, no ZIP or neighbourhood published", "pages/flagged.html", "SF_HI"),
    ("R-19", "Every table row must link an official source; unverifiable values blank and flagged", "Answered — enforced by the build check", "pages/sources.html", "SF_571"),
    ("R-20", "Clean GitHub Pages site, dashboard landing, subpages by category", "Answered", "index.html", "SF_LI"),
    ("R-21", "Flag irregularities for manual review", "Answered — 16 flags published", "pages/flagged.html", "SF_BANK"),
    ("R-22", "Coordinate with parallel sessions via COORDINATION.md", "Answered — claim, scope and record logged", "index.html", "SF_HI"),
    ("R-23", "Open a pull request, merge it and confirm the Pages deployment", "Answered — recorded in COORDINATION.md", "index.html", "SF_HI"),
]


def requirements():
    labels = {
        "index.html": "Dashboard",
        "pages/executive-summary.html": "Executive summary",
        "pages/process.html": "Licence &amp; process",
        "pages/units.html": "Units &amp; maths",
        "pages/laws.html": "Rules &amp; caps",
        "pages/reasonable.html": "Reasonable &amp; normal",
        "pages/practice.html": "Market practice",
        "pages/notice.html": "Notice &amp; reasons",
        "pages/review.html": "Tenant-lawyer test",
        "pages/discrimination.html": "One unit or both?",
        "pages/requirements.html": "Requirements checklist",
        "pages/sources.html": "Sources register",
        "pages/flagged.html": "Flagged for review",
    }
    rows = "".join(
        '<tr><td class="nowrap"><b>%s</b></td><td>%s</td><td>%s</td>'
        '<td><a href="../%s">%s</a></td>%s</tr>'
        % (rid, text, status, dest, labels.get(dest, dest), cell(k))
        for rid, text, status, dest, k in REQS
    )
    body = f"""
<div class="card">
  <h1>Requirements checklist</h1>
  <p class="lede">Every item in the brief, with the page that answers it, the verification status, and the official rule behind the answer.</p>
</div>

<div class="card">
  <h2>Status summary</h2>
  <div class="grid">
    <div class="stat"><div class="num">23</div><div class="lbl">requirements tracked</div></div>
    <div class="stat"><div class="num">20</div><div class="lbl">answered from official sources</div></div>
    <div class="stat"><div class="num">3</div><div class="lbl">answered only conditionally (rent history, government building record, official statistics)</div></div>
    <div class="stat"><div class="num">{len(FLAGS)}</div><div class="lbl">items flagged for review, all published</div></div>
  </div>
</div>

<div class="card">
  <h2>The checklist</h2>
  <table>
    <thead><tr><th style="width:7%">ID</th><th style="width:38%">Requirement</th><th style="width:22%">Status</th><th style="width:14%">Answered on</th><th style="width:19%">Official rule</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>

<div class="card warn">
  <h2>Open items that need the owner, not more research</h2>
  <table>
    <thead><tr><th style="width:32%">Open item</th><th>What is needed</th><th style="width:20%">Source for the rule</th></tr></thead>
    <tbody>
      <tr><td>Unit B rent history 2019–2026</td><td>Leases, notices, ledger — determines whether the banked total is 11.5% or less.</td>{cell("SF_BANK")}</tr>
      <tr><td>Rent-increase licence status</td><td>Portal screenshot showing the licence current on the planned effective date.</td>{cell("SF_HI")}</tr>
      <tr><td>Unit A anniversary</td><td>A Rent Board counsellor's confirmation of the 1 Feb vs 1 Apr question.</td>{cell("SF_LI")}</tr>
      <tr><td>Building record</td><td>Certificate-of-occupancy date and legal unit count from the City's records.</td>{cell("SF_LAWS")}</tr>
    </tbody>
  </table>
</div>
"""
    return page("pages/requirements.html", "Requirements checklist", body,
                "Every requirement in the brief mapped to the page that answers it, its status and the official rule.")


# ------------------------------------------------------------------ flagged
FLAGS = [
    ("FR-01", "Unit B rent history 2019–2026", "Unverified",
     "The owner supplied a 1 June 2019 lease start and $3,150 rent but no complete increase ledger. The 11.5% banked / 13.1% total figures are therefore <b>conditional</b> on no increase ever having been imposed: any increase in any year removes that year's percentage from the banked total and changes the anniversary date.",
     "Leases, notices, proofs of service and a rent ledger 2019–2026.", "SF_BANK"),
    ("FR-02", "Unit A anniversary date: 1 February or 1 April?", "Open",
     "The tenancy began 1 February 2025 and continued when a new co-tenant joined on 1 April 2026 at the same rent. The Rent Board's rule starts the clock 12 months after the lease began, but its pages do not address a mid-tenancy lease renewal with a new occupant. Both outcomes are computed: 1 Feb 2027 (3.0%) and 1 Apr 2027 (percentage not yet announced).",
     "Written confirmation from a Rent Board counsellor; keep the original lease and the 2026 renewal together.", "SF_LI"),
    ("FR-03", "Two official pages describe banking differently", "Irregularity",
     "The banked-increases page says a skipped increase “is only banked if at least 24 full months pass without any rent increase”; the worked example on the rent-increases page applies a 12-month test to each skipped increase. Both are official Rent Board text and are quoted on the executive summary page. Neither wording changes Unit B's total; for Unit A the 1.6%-only option is lawful under either reading.",
     "Rent Board counsellor confirmation, or a written determination; publish both texts until then.", "SF_BANK"),
    ("FR-04", "Rent-increase licence status unknown", "Unverified",
     "No Housing Inventory filing history was provided. Without a licence in effect on the effective date the notice is not enforceable, whatever the percentage.",
     "Portal screenshot for both units dated immediately before service.", "SF_HI"),
    ("FR-05", "Allowable percentage for 1 March 2027 – 29 February 2028", "Blank",
     "Not yet announced, so no figure is given for any effective date on or after 1 March 2027. The table cells are left blank rather than estimated.",
     "The Rent Board's announcement and document 571 for 2027–28.", "SF_LI"),
    ("FR-06", "File #261020 — proposed 10% annual cap", "Pending — not law",
     "Introduced 15 September 2026; status <b>Pending Committee Action</b>. The Rent Board's 9 November 2026 notice states it would apply to banked increases noticed on or after 15 September 2026 if enacted, and that it “has not been enacted and is subject to change”. A 13.1% Unit B notice is exposed to this; a 10.0% notice is not.",
     "Re-check Legistar immediately before serving any increase above 10%.", "LEGISTAR_261020"),
    ("FR-07", "Ordinance text verified by subsection", "Corrected",
     "Administrative Code § 37.3 was re-read subsection by subsection on 10 Nov 2026: § 37.3(a)(1) (60% of CPI, 7% cap, § 37.15 licence), § 37.3(a)(2) (banking since 1 Apr 1982), § 37.3(a)(8) (arbitration petition), § 37.3(a)(10) (voucher payment-standard rules), § 37.3(a)(11)(A) (additional-occupant increase ban), § 37.3(b)(1)&amp;(5) (written breakdown &amp; null-and-void rule), and § 37.3(d)(2)(B) (partial occupancy changes).",
     "Closed on the Rules, Units and Notice pages; check separate Rent Board Rules &amp; Regulations if an ALJ dispute arises.", "ADMIN_373"),
    ("FR-08", "No official “normal” or average increase figure", "No official source",
     "The Rent Board publishes a maximum, not an average or typical amount. No number is given for “normal”.",
     "None — this is an official-data gap, published rather than filled.", "SF_LI"),
    ("FR-09", "No official data on corporate vs individual increase practice", "No official source",
     "No City, State or federal dataset reports how often or by how much corporations versus individual owners raise rent. The practice page therefore cites only evidenced conduct (algorithmic pricing, turnover pricing) and leaves the statistics blank.",
     "None available from official sources.", "SF_LI"),
    ("FR-10", "No official ZIP-level market-rent benchmark", "No official source",
     "The rate is citywide, and no official ZIP-level rent benchmark was located; private listing averages are not cited because they are not authoritative.",
     "None; the rate question is answered by the citywide percentage.", "SF_571"),
    ("FR-11", "Notice signature / owner-identification requirement", "Blank",
     "The Rent Board's published notice elements are amount, percentage, date and banked part. It does not publish a signature or identification requirement, so none is asserted; the model notice nonetheless identifies the owner and the habitability contact, which the Housing Inventory separately requires.",
     "Rent Board counsellor confirmation if a signature dispute arises.", "SF_HI"),
    ("FR-12", "No official rule requiring uniform increases across units", "Absence of authority",
     "No ordinance or statute requires the same increase for every tenant, and none forbids different lawful maximums. The conclusion is stated as an absence of authority, not as a positive rule; see the discrimination page.",
     "None; the analysis rests on the prohibitions that do exist.", "LEG_12955"),
    ("FR-13", "Subsidy / voucher status of either unit", "Unverified",
     "If either unit is subsidised, it may be partially exempt from the Rent Ordinance and a housing authority may review the reasonableness of the rent.",
     "Confirm whether a housing assistance payment contract exists for either unit.", "SF_LAWS"),
    ("FR-14", "Building record: 1940, two legal units", "Unverified",
     "The year and unit count are owner statements. Coverage turns on a certificate of occupancy before 14 June 1979 and on the unit not being a single-family dwelling or condominium; an unpermitted conversion can change the analysis.",
     "City property record / certificate of occupancy.", "SF_LAWS"),
    ("FR-15", "Earlier editions of this site contained claims now corrected", "Corrected",
     "Corrections applied: the Unit A anniversary was once shown as 1 April; banking was once described as “capped at three years”; a Unit B figure of 11.5% was once presented without the annual component that makes the total 13.1%; the pre-9-November-2026 status of File #261020 was stated without the Rent Board's new notice. Prior editions remain online for audit but are no longer the canonical pages.",
     "This page and the corrected pages are the canonical record.", "SF_LI"),
    ("FR-16", "Non-compliance consequence wording", "Verified — closed 10 Nov 2026",
     "The Notice of Owner Noncompliance page was re-retrieved on 10 November 2026 and is now quoted directly: a notice that goes into effect while the unit is unlicensed “may be null and void (this may apply for multiple years)”, and the tenant “may be entitled to a rent refund”. It also confirms the 1 July 2022 / 1 March 2023 start dates, paper filing fallback, and the Tenant Summary Petition (Form 518) route while an increase has not yet taken effect, alongside Admin. Code § 37.3(b)(5).",
     "Closed — cited across the Dashboard, Summary, Process, Rules and Review pages.", "SF_NONCOMP"),
    ("FR-17", "“13.1%” was labelled a maximum catch-up / June 2027 ceiling", "Corrected 10 Nov 2026",
     "13.1% is 11.5% banked (2020–2025) plus the 1.6% annual allowance in force through 28 February 2027. It is therefore the conditional maximum only for an effective date <b>on or before 28 February 2027</b>. For 1 Mar – 31 May 2027 (off-anniversary before 1 June 2027) only 11.5% is banked plus the unannounced 2027–28 rate; on <b>1 June 2027</b> (once 12 full months have elapsed since 1 June 2026) all seven skipped years 2020–2026 (<b>13.1%</b>) are banked plus whatever 2027–28 rate the Rent Board publishes.",
     "Re-check the Rent Board's published percentage before any effective date on or after 1 March 2027.", "SF_571"),
]


def flagged():
    rows = ""
    for fid, item, status, detail, closes, key in FLAGS:
        badge = {"Unverified": "warn", "Open": "warn", "Irregularity": "danger",
                 "Blank": "warn", "Pending — not law": "danger", "No official source": "warn",
                 "Corrected": "ok", "Scope limit": "warn",
                 "Absence of authority": "warn"}.get(status, "warn")
        if status.startswith("Corrected") or status.startswith("Verified"):
            badge = "ok"
        rows += ('<tr><td class="nowrap"><b>%s</b></td><td>%s</td>'
                 '<td><span class="badge %s">%s</span></td><td>%s</td><td>%s</td>%s</tr>'
                 % (fid, item, badge, status, detail, closes, cell(key)))
    body = f"""
<div class="card alert">
  <h1>Flagged for review</h1>
  <p class="lede">{len(FLAGS)} items that are unverified, blank, internally inconsistent or corrected. They are published here deliberately — nothing on this list was filled in with a guess — and none of them blocks publication of the site.</p>
</div>

<div class="card">
  <h2>What each status means</h2>
  <table>
    <thead><tr><th style="width:24%">Status</th><th>Meaning</th><th style="width:20%">Rule applied</th></tr></thead>
    <tbody>
      <tr><td><span class="badge warn">Unverified</span></td><td>The fact comes from the owner, not from a government record, and it changes the answer.</td>{cell("SF_HI")}</tr>
      <tr><td><span class="badge warn">Blank</span></td><td>No official value exists yet (for example next year's percentage); the cell is left empty.</td>{cell("SF_LI")}</tr>
      <tr><td><span class="badge warn">No official source</span></td><td>No official body publishes the number (averages, ZIP benchmarks, owner-type statistics).</td>{cell("SF_571")}</tr>
      <tr><td><span class="badge danger">Irregularity</span></td><td>Two official sources do not say the same thing.</td>{cell("SF_BANK", "SF_LI")}</tr>
      <tr><td><span class="badge danger">Pending — not law</span></td><td>Proposed legislation that would change the outcome if enacted.</td>{cell("LEGISTAR_261020")}</tr>
      <tr><td><span class="badge ok">Corrected</span></td><td>An earlier statement on this site was wrong and has been replaced.</td>{cell("SF_LI")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>The {len(FLAGS)} flags</h2>
  <table>
    <thead><tr><th style="width:7%">ID</th><th style="width:17%">Item</th><th style="width:8%">Status</th><th>Detail</th><th style="width:17%">What closes it</th><th style="width:17%">Official source</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>Items that are <i>not</i> flagged</h2>
  <p>For contrast, these were checked and are fully supported by the linked official page: the 1.6% allowance for 1 March 2026 – 28 February 2027 and the prior 1.4%; the 30/90-day notice rule and the 5-day mail extension; the 24-month banking condition as worded on the banking page; the licence requirement for a 1–9 unit building from 1 March 2023; the 1 March annual deadline; the absence of any petition requirement for annual or banked increases; the 8.8% state figure for the San Francisco area and the local-ordinance exemption; the fair-housing grounds under FEHA and the federal Act; and the algorithmic-pricing ban and the federal antitrust case.</p>
  <p class="small">Sources: {srcs("SF_571", "LEG_827", "SF_BANK", "SF_HI", "LEG_1947", "LEG_12955", "SF_ALGO", "DOJ_ALGO")}</p>
</div>
"""
    return page("pages/flagged.html", "Flagged for review", body,
                "Published list of unverified, blank, inconsistent and corrected items, each with its official source link.")
