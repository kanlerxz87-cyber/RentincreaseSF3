"""Reference pages: sources register, requirements checklist, flagged for review."""
from site_layout import SRC, src, srcs, cell, page

RETRIEVED = "13 Nov 2026"

# key, what it supports
USED_FOR = {
    "SF_LI": "Current allowable percentage (1.6%), base-rent rule, no-rounding rule, anniversary rules, 30/90-day notice elements, additional-occupant prohibition, vacancy pricing, the 9 Nov 2026 notice on File #261020",
    "SF_RULE4": "Written annual/banked breakdown and dates underlying banked amounts, §§ 4.10 and 4.12",
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
    "SF_614": "Rule § 6.14 may apply to subsequent occupants including co-tenants with timely notice; Costa-Hawkins distinguishes co-tenants from subtenants. Obtain legal advice.",
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
    "OPM_HOLIDAYS": "11 November 2026 is a federal holiday (Veterans Day, 5 U.S.C. 6103) — relevant to any mail-by deadline that falls on that day",
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
  <p class="lede">Every official source used on this site, the claim it supports, and the date it was retrieved. The register was reviewed on 10 November 2026, every registered source was re-fetched and read on 11 November 2026, and the sources this site leans on were fetched again and re-read on 13 November 2026. Availability can change.</p>
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
    ("R-09", "Confirm rent-control status of the two reported units in a 1940 building", "Owner-reported; government record not obtained", "pages/laws.html", "SF_LAWS"),
    ("R-10", "State the local cap, the state cap and the federal position", "Answered", "pages/laws.html", "LEG_1947"),
    ("R-11", "Explain whether the ZIP code changes the answer", "Answered — no ZIP-level rate exists", "pages/reasonable.html", "SF_LI"),
    ("R-12", "How large real-estate corporations handle increases", "Answered within official evidence; statistics unavailable", "pages/practice.html", "DOJ_ALGO"),
    ("R-13", "How individual owners handle increases", "Answered", "pages/practice.html", "SF_LI"),
    ("R-14", "Correct way to inform tenants of an increase", "Answered", "pages/notice.html", "LEG_827"),
    ("R-15", "Reasonable reasons for an increase", "Answered", "pages/notice.html", "SF_LANDPET"),
    ("R-16", "Test the increases against what a tenant lawyer would review", "Answered — 16-point test", "pages/review.html", "SF_UNLAWFUL"),
    ("R-17", "Decide whether to raise one unit or both to avoid discrimination exposure", "Answered", "pages/discrimination.html", "LEG_12955"),
    ("R-18", "Anonymise all personal information, keep dates and amounts", "Answered — placeholders, no ZIP or neighbourhood published", "pages/flagged.html", "SF_HI"),
    ("R-19", "Every table row must link an official source; unverifiable values blank and flagged", "Canonical rows checked; archived editions have exceptions (FR-24)", "pages/sources.html", "SF_571"),
    ("R-20", "Clean GitHub Pages site, dashboard landing, subpages by category", "Answered", "index.html", "SF_LI"),
    ("R-21", "Flag irregularities for manual review", "Answered — {nflags} flags published", "pages/flagged.html", "SF_BANK"),
    ("R-22", "Coordinate with parallel sessions via COORDINATION.md", "Answered — claim, scope and record logged", "index.html", "SF_HI"),
    ("R-23", "Open a pull request, merge it and confirm the Pages deployment", "Answered — recorded in COORDINATION.md", "index.html", "SF_HI"),
    ("R-24", "Is the duty to inform the Rent Board (the 2023 licence law) a state or a local law?", "Answered — local law (Ordinance 265-20)", "pages/executive-summary.html", "SF_ORD265"),
    ("R-25", "A clear list of questions, information and answers to address before any decision, including how to discover missing information", "Answered", "pages/questions.html", "SF_HI"),
    ("R-26", "A dedicated suggestions section where options can be reviewed and a path chosen before anything is implemented", "Answered", "pages/suggestions.html", "SF_LI"),
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
        "pages/questions.html": "Questions &amp; answers",
        "pages/suggestions.html": "Suggestions",
        "pages/requirements.html": "Requirements checklist",
        "pages/sources.html": "Sources register",
        "pages/flagged.html": "Flagged for review",
    }
    rows = "".join(
        '<tr><td class="nowrap"><b>%s</b></td><td>%s</td><td>%s</td>'
        '<td><a href="../%s">%s</a></td>%s</tr>'
        % (rid, text, status.replace("{nflags}", str(len(FLAGS))), dest,
           labels.get(dest, dest), cell(k))
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
    <div class="stat"><div class="num">26</div><div class="lbl">requirements tracked</div></div>
    <div class="stat"><div class="num">23</div><div class="lbl">answered from official sources</div></div>
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
     "The owner supplied a 1 June 2019 lease start and $3,150 rent but no complete increase ledger. The 11.5% banked / 13.1% total figures are therefore <b>conditional</b> on no increase ever having been imposed: a prior increase requires recalculating the balance, base rent and timing; an unused portion of a partial increase may be bankable.",
     "Leases, notices, proofs of service and a rent ledger 2019–2026.", "SF_BANK"),
    ("FR-02", "Unit A anniversary date: 1 February or 1 April?", "Open",
     "The tenancy began 1 February 2025 and continued when a new co-tenant joined on 1 April 2026 at the same rent. The Rent Board's rule starts the clock 12 months after the lease began, but its pages do not address a mid-tenancy lease renewal with a new occupant. Both outcomes are computed: 1 Feb 2027 (3.0%) and 1 Apr 2027 (percentage not yet announced).",
     "Written confirmation from a Rent Board counsellor; keep the original lease and the 2026 renewal together.", "SF_LI"),
    ("FR-03", "Three official texts describe banking differently", "Irregularity",
     "Re-checked against the sources on 11 Nov 2026, there are <b>three</b> official texts, not two. (1) The banked-increases page says a skipped increase “is only banked if at least 24 full months pass without any rent increase”. (2) The worked example on the rent-increases page applies a <b>12-month</b> test to each skipped increase. (3) The binding regulation, <b>Rules &amp; Regulations § 4.12(a)</b>, says: “A full 12 months must have elapsed from the date that an annual rent increase, or a portion thereof, could have been imposed before this banking section becomes applicable.” The Rent Board's own worked example (tenant 8/1/2022, first increase 8/1/2025, banks both 8/1/2023 and 8/1/2024) is consistent with the 12-month text and cannot be reconciled with a strict per-anniversary 24-month reading. Under the 12-month reading Unit B's 11.5% banked balance and Unit A's 3.0% total stand; under a strict per-anniversary 24-month reading Unit B's balance for a Feb-2027 date would fall to 10.1% banked (10.1% + 1.6% annual = 11.7%). Both readings are published; the 1.6%-only option is lawful under either.",
     "Rent Board counsellor confirmation, or a written determination; publish both texts until then.", "SF_BANK", ),
    ("FR-04", "Rent-increase licence status unknown", "Unverified",
     "No Housing Inventory filing history was provided. Without a licence in effect on the effective date the notice is not enforceable, whatever the percentage.",
     "Portal screenshot for both units dated immediately before service.", "SF_HI"),
    ("FR-05", "Allowable percentage for 1 March 2027 – 29 February 2028", "Blank",
     "Not yet announced, so no figure is given for any effective date on or after 1 March 2027. The table cells are left blank rather than estimated.",
     "The Rent Board's announcement and document 571 for 2027–28.", "SF_LI"),
    ("FR-06", "File #261020 — proposed 10% annual cap", "Pending — not law",
     "Introduced 15 September 2026; status <b>Pending Committee Action</b>. The Rent Board's 9 November 2026 notice states it would apply to banked increases noticed on or after 15 September 2026 if enacted, and that it “has not been enacted and is subject to change”. The illustrative 13.1% total includes 11.5% banked, exceeding the proposed 10% combined banked-and-capital limit; the 1.6% annual component is distinct. The effect of any final law and other passthroughs is unverified.",
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
    ("FR-14", "Building record: year, unit count and legal status", "Unverified",
     "The 1940 year is owner-reported; two units were described, but the total number of units in the building and their legal status were not established. Coverage turns on a certificate of occupancy before 14 June 1979 and on the unit not being a single-family dwelling or condominium; an unpermitted conversion can change the analysis.",
     "City property record / certificate of occupancy.", "SF_LAWS"),
    ("FR-15", "Earlier editions of this site contained claims now corrected", "Corrected",
     "Corrections applied: the Unit A anniversary was once shown as 1 April; banking was once described as “capped at three years”; a Unit B figure of 11.5% was once presented without the annual component that makes the total 13.1%; the pre-9-November-2026 status of File #261020 was stated without the Rent Board's new notice; and six end-dates in the 1982–2027 rate table did not match Form 571 — five written as 29 February in years that are not leap years (1985, 1997, 2001, 2005, 2013), corrected to 28 February, and the 1995–96 period written as ending 28 February 1996, corrected to 29 February 1996 — see FR-26. Prior editions remain online for audit but are no longer the canonical pages.",
     "This page and the corrected pages are the canonical record.", "SF_LI"),
    ("FR-16", "Non-compliance consequence wording", "Verified — closed 10 Nov 2026",
     "The Notice of Owner Noncompliance page was re-retrieved on 10 November 2026 and is now quoted directly: a notice that goes into effect while the unit is unlicensed “may be null and void (this may apply for multiple years)”, and the tenant “may be entitled to a rent refund”. It also confirms the 1 July 2022 / 1 March 2023 start dates, paper filing fallback, and the Tenant Summary Petition (Form 518) route while an increase has not yet taken effect, alongside Admin. Code § 37.3(b)(5).",
     "Closed — cited across the Dashboard, Summary, Process, Rules and Review pages.", "SF_NONCOMP"),
    ("FR-21", "Rule § 6.14 and Costa-Hawkins co-tenant distinction", "Corrected 11 Nov 2026",
     "The earlier source-register description wrongly said neither rule ever allows an increase against a co-tenant. The Rent Board says a timely § 6.14 notice can be served on a subsequent co-tenant or subtenant; its Costa-Hawkins discussion distinguishes co-tenants. Applicability depends on the actual facts and legal advice is needed.",
     "Confirm the occupancy history and any § 6.14 notices with qualified counsel before relying on either rule.", "SF_614"),
    ("FR-22", "No independent tenant-lawyer approval or normal-rate evidence", "Unverified",
     "The illustrative 10% and other scenarios are not independently reviewed by a tenant lawyer and no official typical increase was established. Past language implying approval or a guaranteed outcome has been corrected. Confirm records and law before service.",
     "Obtain independent legal review; select any amount only after checking tenant impact and eligibility.", "SF_UNLAWFUL"),
    ("FR-23", "Actual notices, service, motive and compliance not verified", "Unverified",
     "No owner records, served notice or tenant-lawyer assessment were available. The earlier review table incorrectly marked numerous factual and legal checks as passing, and described every increase within 180 days of a complaint as retaliation. Those statements have been corrected; arithmetic is not legal clearance.",
     "Independently review the complete facts and applicable law before serving any notice.", "LEG_1942"),
    ("FR-24", "Archived editions: row-source exceptions", "Unverified",
     "Automated checks require official links for canonical data rows; preserved historical editions have 25 row-source warnings and may contain stale or corrected claims. They are not a fully verified current source; use the canonical pages and linked official sources.",
     "Review archived row warnings and prior-edition corrections before relying on any historical page.", "SF_LI"),
    ("FR-25", "Fixed-term lease provisions and actual notice", "Unverified",
     "Lease end dates and any mid-term rent adjustment clauses were not supplied. Civil Code § 827 describes specified periodic tenancies; these scenarios do not establish that an increase can be imposed during an unexpired fixed term.",
     "Review both signed leases and obtain legal advice before choosing a date or serving notice.", "LEG_827"),
    ("FR-27", "Postal service on 11 November 2026 (a federal holiday)", "Unverified",
     "The planner's mailing day of 11 November 2026 for a 14 February 2027 effective date was a federal holiday (Veterans Day) per OPM, and the sf.gov pages read on that date carried a City closure banner. Whether a rent-increase notice can be validly deposited in the mail on a federal holiday — and how that interacts with the 5-day extension in Code of Civil Procedure § 1013 — is not established by any source this site cites. That mail-by day has since passed: by the 13 November 2026 research pass only personal service by 16 November 2026 remains open for that effective date. No conclusion is asserted.",
     "Serve in person by the date shown on the planner, or mail on a business day; confirm with the USPS holiday schedule and counsel.", "OPM_HOLIDAYS"),
    ("FR-28", "Federal source link for voucher rent reasonableness was broken", "Corrected 11 Nov 2026",
     "The internal source register cited <i>24 CFR 982</i> at an eCFR URL using <b>chapter-II/subchapter-B/part-982/subpart-M</b>. That URL returns <b>HTTP 404</b> (checked 11 Nov 2026): Part 982 sits in <b>Chapter IX</b> (Office of Assistant Secretary for Public and Indian Housing), and the “rent reasonableness” provision the register describes is <b>24 CFR § 982.507 — Rent to owner: Reasonable rent</b>, in <b>Subpart K</b>. The corrected URL is published in the source register and cited here. No figure, percentage or date on this site depended on the broken link.",
     "Closed — corrected in the source register and cited on the units page. Confirm voucher status (FR-13) before relying on any federal program rule.", "CFR_982"),
    ("FR-29", "Whether a banked increase may be served on its own", "Irregularity",
     "Rule § 4.12(a) states: “This banked amount may only be given <b>at the time of an annual increase</b>.” The banked-increases page says a landlord “may impose it on a future anniversary date, <b>or at another time when they are allowed to raise the rent</b> (as long as at least 12 months have passed since the last increase)”, and that a landlord “may also combine a banked increase with a regular annual increase”. Unit B's “banked only (11.5%)” row assumes the second wording. If the Rule's narrower wording governs, a banked balance can only be imposed together with the annual increase in force on that date — which is what the 13.1% combined row already shows. Nothing on this site advises serving a banked amount without the annual component.",
     "Rent Board counsellor confirmation before serving a banked-only increase; both texts are published rather than one being chosen.", "SF_RULE4"),
    ("FR-30", "Notice-content rules carry a safe harbour the site had not published", "Verified — added 11 Nov 2026",
     "Rule § 4.12(b) requires the landlord to inform the tenant, on or before the date legal notice is given, which portion of the increase is banked <b>and</b> the dates on which the banked amount is based — but adds: “provided, however, that <b>failure to include such information shall not render the increase null and void</b>.” Separately, Rule § 4.10(b) provides that a rent increase which does not conform to § 4.10(a) “shall render the entire rent increase null and void, unless the amount requested equals no more than the allowable annual and banked rent increase(s)”, with a readjustment where a good-faith increase exceeds the limit by no more than one-half of one percent of the prior base rent. The site previously stated the notice contents without either qualification.",
     "Published for completeness; include the banked portion and its dates in every notice regardless of the safe harbour.", "SF_RULE4"),
    ("FR-31", "Two licence details not previously published", "Verified — added 11 Nov 2026",
     "Re-reading the enabling pages on 11 Nov 2026 surfaced two points the site did not state. (1) <b>Suspension:</b> the Rent Board's Ordinance 265-20 page states that if the owner does not provide the required information, “the owner's license to impose annual and/or banked rent increases will be suspended for the period of noncompliance” — a consequence distinct from a notice being unenforceable. (2) <b>Carve-out:</b> the Notice of Owner Noncompliance page states the Rent Increase License “is not required in some situations where the original occupant(s) no longer live in the unit” (and for Ordinance passthroughs). That carve-out does <b>not</b> apply to Unit A on the reported facts, because an original occupant (<b>Tenant A</b>) remains in lawful possession — so the licence requirement stands for Unit A.",
     "Published for completeness; confirm licence status in the Portal (FR-04) before serving any notice.", "SF_ORD265"),
    ("FR-17", "“13.1%” was labelled a maximum catch-up / June 2027 ceiling", "Corrected 10 Nov 2026",
     "13.1% is 11.5% banked (2020–2025) plus the 1.6% annual allowance in force through 28 February 2027. It is therefore the conditional maximum only for an effective date <b>on or before 28 February 2027</b>. For 1 Mar – 31 May 2027 (off-anniversary before 1 June 2027) only 11.5% is banked plus the unannounced 2027–28 rate; on <b>1 June 2027</b> (once 12 full months have elapsed since 1 June 2026) all seven skipped years 2020–2026 (<b>13.1%</b>) are banked plus whatever 2027–28 rate the Rent Board publishes.",
     "Re-check the Rent Board's published percentage before any effective date on or after 1 March 2027.", "SF_571"),
    ("FR-18", "Total building unit count and historical reporting start date", "Unverified",
     "The brief describes two rental units, but does not state the total number of units in the building. Unit B $3,150 is its 2019 starting rent; current rent and both units' complete histories are unverified. Do not infer a two-unit building or choose a historical reporting start date. The individual-owner licensing obligation applies regardless of this uncertainty.",
     "Confirm total building unit count and property record. Reporting began 1 March 2023 for condominiums and buildings under 10 units, and 1 July 2022 for other buildings of 10 or more units.", "SF_HI"),
    ("FR-19", "Older editions and legal-review limits", "Irregularity",
     "Archived editions and previous versions may include unsupported claims about building size, the proposed cap, passthrough procedures, retaliation or guaranteed legal review. The preserved verified edition check reports 25 rows without official links or with only internal links; automated checks do not certify all external links or claims. They are preserved for history, not current advice. The canonical pages have been corrected; no lawyer reviewed these facts and no checklist guarantees an outcome.",
     "Use the canonical dashboard and obtain legal advice before serving; check current law and individual records.", "SF_LANDPET"),
    ("FR-20", "Filing a copy of an ordinary increase notice", "Unverified",
     "The cited official pages establish that ordinary annual and banked increases need no approval petition, and that the licence need not accompany the tenant notice. Those propositions do not themselves establish whether a copy of the notice must be filed separately.",
     "Confirm any separate filing obligation with the Rent Board; other types of increases have distinct procedures.", "SF_HI"),
    ("FR-26", "Rate table row end-dates", "Corrected 11 Nov 2026",
     "The 1982–2027 table on <b>Rules &amp; caps</b> had six row end-dates that did not match document 571: five fell on 29 February in a year that is not a leap year (3/1/84 – <b>2/29/85</b>, 3/1/96 – <b>2/29/97</b>, 3/1/00 – <b>2/29/01</b>, 3/1/04 – <b>2/29/05</b>, 3/1/12 – <b>2/29/13</b>), which are not real dates, and the 1995–96 period ended <b>2/28/96</b> in a leap year that document 571 runs to <b>2/29/96</b>. All 46 rows were published throughout — re-counted from the pre-correction HTML — and every percentage was already correct; an earlier draft of this flag also said the Board's separate <b>12/8/92 – 2/28/93 (1.6%)</b> row was missing, which the same recount disproved. The table is now compared row by row against a transcription of the PDF, and each period must parse as a real, contiguous, descending calendar range, so an impossible date fails the build.",
     "None — corrected against the Rent Board's document 571 and re-checked row by row.", "SF_571"),
]


def flagged():
    rows = ""
    # Render in numeric flag order so a reviewer can work down the list without hunting.
    ordered = sorted(FLAGS, key=lambda f: int(f[0].split("-")[1]))
    for fid, item, status, detail, closes, key in ordered:
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


# ------------------------------------------------------------------ questions
def questions():
    """The brief's decision list: answered / open / how to discover what is missing."""
    answered = [
        ("Q-01", "Must an individual owner (not a corporation) inform the Rent Board and hold a licence before notifying tenants of an increase?",
         "<b>Yes.</b> All owners of residential property must report into the Rent Board Housing Inventory; a tenant-occupied report generates a rent-increase licence, and the licence must be in effect on the <b>effective date</b> of the increase. The duty turns on building size, not on the owner's legal form.",
         "SF_HI"),
        ("Q-02", "Is the “since 2023” duty to inform the Rent Board a state or a local law?",
         "<b>Local.</b> San Francisco <b>Ordinance No. 265-20</b> (effective 18 January 2021) created the Housing Inventory and licence; reporting for condominiums and buildings with fewer than 10 units began <b>1 March 2023</b>. State law (AB 1482, Civ. Code § 1947.12) caps increases and Civ. Code § 827 sets notice periods — neither requires a Rent Board filing. No federal law imposes one.",
         "SF_ORD265"),
        ("Q-03", "What is the current allowable annual increase?",
         "<b>1.6%</b> for effective dates 1 March 2026 – 28 February 2027 (60% of Bay Area CPI), multiplied against base rent only, no rounding up.",
         "SF_LI"),
        ("Q-04", "Do annual or banked increases need a Rent Board approval petition?",
         "<b>No.</b> “Landlords are not required to file a petition with the City to impose these types of rent increases.” Other increases (capital improvement, operating and maintenance, etc.) have their own petition procedures.",
         "SF_MULTI"),
        ("Q-05", "How much notice must a tenant get?",
         "30 days if the increase is 10% or less (measured against the rent charged at any time in the previous 12 months, alone or combined), <b>90 days</b> if more than 10%; <b>+5 days</b> if mailed within California.",
         "LEG_827"),
        ("Q-06", "How do banked increases work?",
         "Skipped annual increases may be added later: added, not compounded; no cap; allowed only since 1 April 1982; no expiry during a tenancy; the banked part and its dates belong in the notice. Two official texts disagree on the waiting test (12 vs 24 months) — both are published on the <a href=\"flagged.html\">Flagged</a> page (FR-03).",
         "SF_BANK"),
        ("Q-07", "What is a “reasonable and normal” increase here?",
         "The lawful ceiling for a rent-controlled unit is the citywide Rent Board percentage plus properly banked amounts. The Rent Board publishes one citywide figure — <b>no ZIP-level or neighbourhood benchmark exists</b>. State AB 1482 (8.8% in this region for 1 Aug 2026 – 31 Jul 2027) does not govern where the local cap is lower.",
         "SF_LI"),
        ("Q-08", "Should both units be increased, or only one, to avoid discrimination exposure?",
         "No official source requires uniform increases. Fair-housing law prohibits different treatment <i>because of</i> a protected characteristic — the control is a documented, non-protected reason per unit. Raising both on the same lawful formula is the lower-risk pattern; the Rent Board does not hear discrimination claims (Civil Rights Department or HUD do).",
         "LEG_12955"),
        ("Q-09", "What does the tenant side cost, and what can they file?",
         "Tenants file an unlawful-rent-increase petition (Form 516C, Box C) <b>free of charge</b>, with <b>no filing deadline</b>, before an Administrative Law Judge; a Tenant Summary Petition (Form 518) is available while an increase has not yet taken effect. The hearing is designed so no attorney is required — but tenants can and do obtain free legal help, so an increase must survive that scrutiny.",
         "SF_UNLAWFUL"),
        ("Q-10", "Is there a separate annual fee besides the free Housing Inventory report?",
         "<b>Yes.</b> The Rent Board Fee is <b>$59.00 per dwelling unit</b> for 2026–27, due 1 March, with a 5% monthly late penalty up to 15%; 50% ($29.50) is recoverable from qualifying tenants; the 2027 exemption window closes 14 December 2026. Neither obligation satisfies the other.",
         "SF_FEE"),
        ("Q-11", "Has anything changed in the law that would block a large banked increase today?",
         "Not yet. <b>File #261020</b> (10%/yr cap on combined banked + capital-improvement increases, if enacted as proposed applying to banked increases noticed on or after 15 September 2026) was re-checked on 13 November 2026: status <b>Pending Committee Action</b>, no final action — <b>not law</b>.",
         "LEGISTAR_261020"),
    ]
    open_qs = [
        ("Q-12", "Are both units actually covered by rent control?",
         "Every calculation on this site assumes coverage. A 1940 construction year is owner-reported; a government building record has not been pulled.",
         "Unverified — owner statement only", "SF_LAWS"),
        ("Q-13", "How many units are in the building?",
         "The brief describes two rental units; the total building count is not stated. It decides which reporting start date applied (10+ units: 1 July 2022; 1–9 units: 1 March 2023) — though the licence duty itself applies either way.",
         "Unverified — FR-18", "SF_HI"),
        ("Q-14", "Is the Housing Inventory filed, and is the licence current on the planned effective date?",
         "Without a licence on the effective date the increase “will not be enforceable” and “may be null and void (this may apply for multiple years)”, with refund exposure. This is the single largest legal risk in the whole process.",
         "Unverified — FR-04", "SF_NONCOMP"),
        ("Q-15", "What is Unit B's complete rent history from June 2019 to today?",
         "The 11.5% banked / 13.1% combined figures assume no increase was ever imposed. One prior increase changes the banked total, the base rent and the timing.",
         "Unverified — FR-01", "SF_BANK"),
        ("Q-16", "Which anniversary applies to Unit A — 1 February or 1 April 2026?",
         "The tenancy began 1 February 2025 and a new co-tenant joined 1 April 2026 at the same rent. The official rule starts the clock 12 months after the lease began, but the Rent Board pages do not address a mid-tenancy renewal with a new occupant. Both dates are computed; the earliest effective date differs.",
         "Open — FR-02", "SF_LI"),
        ("Q-17", "Is either unit subsidised (voucher / regulated rent)?",
         "Federal voucher rules and the Rent Ordinance's partial exemption can change the lawful amount and the notice.",
         "Unverified — FR-13", "ADMIN_373"),
        ("Q-18", "Do the leases run to a fixed term that has not expired?",
         "Civil Code § 827 describes periodic tenancies. Nothing here establishes that an increase may be imposed mid-term under a fixed-term lease; both leases must be read.",
         "Unverified — FR-25", "LEG_827"),
        ("Q-19", "Does a copy of the rent-increase notice have to be filed with the Rent Board?",
         "Ordinary annual/banked increases need no approval petition, and the licence need not accompany the notice — but the cited pages do not answer whether a separate notice-copy filing exists.",
         "Unverified — FR-20", "SF_HI"),
        ("Q-20", "Which effective date will actually be chosen (anniversary vs later)?",
         "The date decides the governing percentage (the 1.6% runs only to 28 February 2027), the banked set, and the 30/90-day clock. The 2027–28 percentage is blank until the Rent Board announces it.",
         "Decision pending", "SF_571"),
        ("Q-21", "Will File #261020 be enacted before the notice is served?",
         "If enacted as proposed it would apply to banked increases noticed on or after 15 September 2026 — which would change what a lawful large banked increase looks like. Status must be re-checked immediately before service.",
         "Pending — not law", "LEGISTAR_261020"),
        ("Q-22", "Is the 2026–27 Rent Board Fee paid (or an exemption on file)?",
         "The fee is separate from the licence; arrears accrue 5%/month up to 15% and are referred to the Bureau of Delinquent Revenue after 1 June.",
         "Unverified — owner record", "SF_FEE"),
    ]
    discovery = [
        ("Building record (construction date, legal unit count, unit type)",
         "Search the address on the City's Property Information Map (linked from the Rent Board's rental-laws page) and pull the certificate-of-occupancy / assessor records; confirm any exemption with a Rent Board counsellor.",
         "SF_LAWS"),
        ("Licence status for both units",
         "Open the Rent Board Portal, search the address or APN, and screenshot the Rent Increase License status for every relevant year — including the planned effective date.",
         "SF_PORTAL"),
        ("Unit B rent history 2019–2026",
         "Assemble the owner's own file: every lease, every rent-increase notice with proof of service, and the rent ledger. The unlawful-rent page shows exactly what tenants attach (leases, notices, receipts) — the same documents answer the question.",
         "SF_UNLAWFUL"),
        ("Unit A anniversary (1 Feb vs 1 Apr)",
         "Call the Rent Board counselling line (415-252-4600, weekdays 9am–noon and 1–4pm) with the lease and renewal dates and record the counsellor's answer in the file.",
         "SF_COUNSEL"),
        ("Whether a separate notice-copy filing exists",
         "Ask a Rent Board counsellor directly and record the answer; the published pages this site cites do not address it (FR-20).",
         "SF_HI"),
        ("Voucher / subsidy status",
         "Review each lease and the rent roll; if a voucher is possible, confirm the interaction with the Rent Ordinance's partial exemption and 24 CFR § 982.507 with counsel before serving.",
         "CFR_982"),
        ("File #261020 status",
         "Re-open the Legistar file page immediately before serving any banked increase; the status on 13 November 2026 is Pending Committee Action with no final action.",
         "LEGISTAR_261020"),
        ("The 2027–28 allowable percentage (blank)",
         "Watch the Rent Board's rent-increase page and Form 571; the new percentage is published for effective dates from 1 March 2027 and cannot be inferred before then.",
         "SF_571"),
        ("Fixed-term lease question",
         "Read both signed leases end to end; if either runs to a fixed end date, obtain legal advice before choosing an effective date.",
         "LEG_827"),
        ("Rent Board Fee / exemption status",
         "Check the Rent Board Portal account and the annual Informational Notice; the 2027 exemption request window closes 14 December 2026.",
         "SF_FEE"),
    ]
    a_rows = "".join(
        '<tr><td class="nowrap"><b>%s</b></td><td>%s</td><td>%s</td>%s</tr>'
        % (qid, q, ans, cell(key)) for qid, q, ans, key in answered)
    b_rows = "".join(
        '<tr><td class="nowrap"><b>%s</b></td><td>%s</td><td>%s</td><td><span class="badge warn">%s</span></td>%s</tr>'
        % (qid, q, why, status, cell(key)) for qid, q, why, status, key in open_qs)
    c_rows = "".join(
        '<tr><td>%s</td><td>%s</td>%s</tr>' % (need, how, cell(key))
        for need, how, key in discovery)
    body = f"""
<div class="card hero">
  <h1>Questions, answers &amp; missing information</h1>
  <p class="lede">The decision list this brief asked for: what is already answered from official sources, what is still open, and a concrete suggestion for discovering every missing fact. Nothing here is filled in with a guess — open items stay open until a record or an official answer closes them. Research pass: 13 November 2026.</p>
</div>

<div class="card ok">
  <h2>A. Answered — the information we already have ({len(answered)} questions)</h2>
  <table>
    <thead><tr><th style="width:6%">ID</th><th style="width:30%">Question</th><th>Answer (verified)</th><th style="width:20%">Official source</th></tr></thead>
    <tbody>{a_rows}</tbody>
  </table>
</div>

<div class="card warn">
  <h2>B. Open — information still missing before a decision can be made ({len(open_qs)} questions)</h2>
  <p class="small">Each row states why the answer changes the decision. Full flag detail: <a href="flagged.html">Flagged for review</a>. Owner-record facts need the owner; official gaps need a publication or an office answer — more research alone will not close them.</p>
  <table>
    <thead><tr><th style="width:6%">ID</th><th style="width:27%">Question</th><th>Why it must be answered first</th><th style="width:14%">Status</th><th style="width:17%">Official source</th></tr></thead>
    <tbody>{b_rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>C. Suggestions — how to discover each missing item ({len(discovery)} suggestions)</h2>
  <table>
    <thead><tr><th style="width:26%">Missing information</th><th>Suggested way to obtain it</th><th style="width:22%">Official source</th></tr></thead>
    <tbody>{c_rows}</tbody>
  </table>
  <p class="small">Sequencing suggestion: licence status (Q-14) and rent history (Q-15) first — they can change or void every number; then the anniversary question (Q-16) with a counsellor; then choose an effective date; then re-check File #261020 (Q-21) immediately before service. Decision options built on these answers: <a href="suggestions.html">Suggestions &amp; decision paths</a>.</p>
</div>
"""
    return page("pages/questions.html", "Questions, answers &amp; missing information", body,
                "Decision list: verified answers, open questions with why they matter, and suggestions for discovering missing information.")


# ------------------------------------------------------------------ suggestions
def suggestions():
    """Site-improvement suggestions (status-labelled) and decision paths for the owner."""
    site_sugg = [
        ("S-01", "Keep the licence question at the forefront of the dashboard and executive summary",
         "A first-time reader meets the highest-consequence obligation (licence before effective date) before any number.",
         "Implemented", "SF_HI"),
        ("S-02", "Publish this questions page: answered / open / discovery suggestions",
         "Separates what is known from what is assumed, so a decision is never built on a blank cell.",
         "Implemented — 13 Nov 2026", "SF_LI"),
        ("S-03", "Publish this suggestions page with status labels and decision paths",
         "Gives a reviewer one place to choose a path before anything is implemented.",
         "Implemented — 13 Nov 2026", "SF_LI"),
        ("S-04", "Roll the research pass and the notice-date planner on every verification session",
         "Deadlines silently going stale is how a compliant notice becomes late; the planner now fails the build if a deadline passes unmarked.",
         "Implemented — gate in tools/verify_core_site.py", "LEG_827"),
        ("S-05", "Keep every unverified item on a public Flagged for review page",
         "Blanks and conflicts stay visible instead of being smoothed over — the reviewer sees exactly what is not established.",
         "Implemented", "SF_BANK"),
        ("S-06", "Maintain an independent second-pass edition (verification/) beside the canonical pages",
         "A separate re-fetch of every source is the check on the main build.",
         "Implemented", "SF_571"),
        ("S-07", "Add a gate that every table row cites an official domain",
         "Makes “source link on every row” a build requirement, not a promise.",
         "Implemented — gate in tools/verify_core_site.py", "SF_571"),
        ("S-08", "Re-check Legistar File #261020 immediately before serving any banked increase",
         "The proposal, if enacted, applies to banked increases noticed on or after 15 September 2026 — status must be fresh at service, not at publication.",
         "Proposed — owner checklist item", "LEGISTAR_261020"),
        ("S-09", "Record a Rent Board counsellor's answers (anniversary, notice-copy filing) in the property file",
         "Two open questions (Q-16, Q-19) can only be closed by an official answer; a dated note makes the file defensible later.",
         "Proposed — owner action", "SF_COUNSEL"),
        ("S-10", "Obtain an independent California lawyer's review of the final notice before service",
         "The tenant-lawyer test page is a checklist, not legal clearance; a review by counsel is the strongest answer to “would a tenant lawyer accept it”.",
         "Proposed — owner decision", "SF_UNLAWFUL"),
        ("S-11", "Keep a dated decision log: which path was chosen, why, and the evidence at the time",
         "Discrimination and retaliation challenges turn on the reason and the record, not on the arithmetic.",
         "Proposed — owner decision", "LEG_1942"),
        ("S-12", "Re-verify the headline figures against the official pages before every notice",
         "Percentages change on 1 March each year and official pages change without notice; this session's re-fetch found no figure drift on 13 November 2026.",
         "Implemented — done this pass", "SF_571"),
    ]
    paths = [
        ("Path A — Conservative",
         "Increase <b>both</b> units by the annual allowance only (1.6% through 28 Feb 2027) on their anniversaries; no banked amounts.",
         "Smallest increase that sits squarely inside the published allowance; works under either banking wording; 30-day notice; no reliance on the rent history.",
         "If the priority is minimal challenge risk while records are still being assembled.",
         "Awaiting your choice", "SF_LI"),
        ("Path B — Full lawful ceiling",
         "Unit A: 1.6% + 1.4% banked = <b>3.0%</b> ($119.85 → $4,114.85) on 1 Feb 2027. Unit B: up to <b>13.1%</b> ($412.65 → $3,562.65) only if the rent history shows no increase since 2019, for an effective date on or before 28 Feb 2027.",
         "Highest amount, but conditional: needs the verified ledger, the licence on the effective date, 90-day notice for &gt;10%, and a fresh File #261020 check.",
         "Only after Q-14, Q-15, Q-16 and Q-21 are closed.",
         "Awaiting your choice", "SF_BANK"),
        ("Path C — Defer and close the records first",
         "Serve nothing yet: file/confirm the Housing Inventory licence, assemble Unit B's ledger, get the counsellor's anniversary answer, then choose an effective date.",
         "No notice risk now; the trade-off is time (and whatever the 2027–28 percentage turns out to be).",
         "If the licence status or rent history cannot be confirmed this month.",
         "Awaiting your choice", "SF_HI"),
        ("Path D — Petition-based increase (different procedure)",
         "Capital improvement, operating & maintenance, or other passthrough increases via a landlord petition — a different, evidence-heavy route with its own forms.",
         "Can exceed the annual ceiling, but requires a petition <i>before</i> notice and Rent Board approval; not needed for annual or banked amounts.",
         "Only if a qualifying expense actually occurred; not a substitute for Paths A–C.",
         "Awaiting your choice", "SF_LANDPET"),
    ]
    s_rows = "".join(
        '<tr><td class="nowrap"><b>%s</b></td><td>%s</td><td>%s</td>'
        '<td><span class="badge %s">%s</span></td>%s</tr>'
        % (sid, sugg, why,
           "ok" if st.startswith("Implemented") else "warn", st, cell(key))
        for sid, sugg, why, st, key in site_sugg)
    p_rows = "".join(
        '<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td>'
        '<td><span class="badge warn">%s</span></td>%s</tr>'
        % (name, involves, tradeoff, when, status, cell(key))
        for name, involves, tradeoff, when, status, key in paths)
    body = f"""
<div class="card hero">
  <h1>Suggestions &amp; decision paths</h1>
  <p class="lede">A dedicated place to review suggestions and choose a path <b>before</b> anything is implemented. Status labels are honest: “Implemented” means it already exists on this site; “Proposed” means nothing has been done — a reviewer picks what to adopt. Research pass: 13 November 2026.</p>
</div>

<div class="card">
  <h2>How to use this page</h2>
  <ol class="steps">
    <li><b>Read the suggestions</b> in Table 1 and mark each one: adopt, adapt or reject. Nothing marked “Proposed” has been implemented anywhere on this site.</li>
    <li><b>Close the open questions first</b> — the paths below assume the licence, rent history and anniversary questions are answered: <a href="questions.html">Questions, answers &amp; missing information</a>.</li>
    <li><b>Choose one path</b> in Table 2, record the choice and the reason in a dated note, then execute through <a href="process.html">Licence &amp; process</a> (licence → calculate → notice → serve).</li>
    <li><b>Re-check the pending ordinance</b> (File #261020) immediately before serving any banked amount.</li>
  </ol>
</div>

<div class="card">
  <h2>Table 1 — Suggestions for improving this site and the decision process ({len(site_sugg)} items)</h2>
  <table>
    <thead><tr><th style="width:6%">ID</th><th style="width:33%">Suggestion</th><th>Why it improves decisions</th><th style="width:15%">Status</th><th style="width:17%">Official source</th></tr></thead>
    <tbody>{s_rows}</tbody>
  </table>
  <p class="small">Status meanings: <span class="badge ok">Implemented</span> already live on this site · <span class="badge warn">Proposed</span> awaiting a reviewer's decision — not implemented · every suggestion cites the official rule it serves.</p>
</div>

<div class="card alert">
  <h2>Table 2 — Decision paths for the rent increase ({len(paths)} options, none chosen yet)</h2>
  <table>
    <thead><tr><th style="width:14%">Path</th><th style="width:30%">What it involves</th><th>Main trade-off</th><th>Choose it when…</th><th style="width:12%">Decision status</th><th style="width:15%">Official source</th></tr></thead>
    <tbody>{p_rows}</tbody>
  </table>
  <p class="small">Amounts shown are the calculated ceilings from <a href="units.html">Units &amp; maths</a>; percentages are official, dollars are arithmetic on the owner-reported base rent. No path is recommended by this site — the choice, and the record of why it was made, belongs to the owner. Not legal advice.</p>
</div>
"""
    return page("pages/suggestions.html", "Suggestions &amp; decision paths", body,
                "Site-improvement suggestions with status labels, and the decision paths for the rent increase, to be reviewed and chosen before implementation.")
