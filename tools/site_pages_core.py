"""Core pages: dashboard, executive summary, licence & process, units."""
from site_layout import src, srcs, cell, page

# ------------------------------------------------------------------ index
def index():
    body = f"""
<div class="card hero">
  <h1>San Francisco rent increase — verified answers</h1>
  <p class="lede">Two owner-reported rent-controlled units in San Francisco (owner-reported construction year 1940). Total building unit count and coverage are unverified. This dashboard answers the owner's questions in the order asked, with an official source link on every row. Research pass: 13 November 2026.</p>
  <div class="quote"><b>Privacy:</b> tenants are shown as <b>Tenant A–F</b>; the ZIP code, neighbourhood and street address are withheld (unit-level facts plus a location could identify the tenants). <b>Dates and dollar amounts are unchanged.</b> Not legal advice.</div>
  <div class="quote" style="border-left-color:var(--warnbd);background:#fffaf0"><b>Updated 13 November 2026.</b> Added the finding that the Rent Board reporting and licence duty is a <b>local</b> law (Ordinance 265-20 / Administrative Code § 37.15), plus two new pages: <a href="pages/questions.html">Open questions</a> (the decision gate, question by question) and <a href="pages/open-questions.html">Known vs unknown</a> (what we have and what is missing). The <a href="pages/suggestions.html">Suggestions &amp; decision path</a> page consolidates every proposal into one register.. Every row on those pages cites the official source it rests on.</div>
</div>

<div class="card alert">
  <h2>1. First question: is the Rent Board duty a state law or a local law?</h2>
  <p><b>It is a local law.</b> The duty to report to the Rent Board and hold a rent-increase licence comes from <b>San Francisco Ordinance No. 265-20</b> (File 201262, passed 8 December 2020), which added <b>Administrative Code § 37.15</b> to the San Francisco Administrative Code. The “2023” date is only the commencement of reporting for condominiums and buildings with fewer than 10 units. No state statute imposes this. Verified 13 November 2026.</p>
  <table>
    <thead><tr><th style="width:28%">Point</th><th>Verified answer</th><th style="width:22%">Official source</th></tr></thead>
    <tbody>
      <tr><td>State or local?</td><td><b>Local</b> — a San Francisco ordinance codified in the San Francisco Administrative Code, credited on the published code page as “Added by Ord. No. 265-20, effective January 18, 2021”.</td>{cell("SF_3715", "SF_ORD265T")}</tr>
      <tr><td>Why it is remembered as “since 2023”</td><td>Reporting commenced <b>1 March 2023</b> for condominium units and units in buildings with fewer than 10 units, and <b>1 July 2022</b> for units in buildings of 10 or more. One ordinance, three dates — see FR-40.</td>{cell("SF_3715", "SF_HI")}</tr>
      <tr><td>Does state law play any part?</td><td>Only as a limit on the City: § 37.15(d) says the Rent Board shall not use the data to operate a “rental registry within the meaning of California Civil Code Sections 1947.7 – 1947.8”.</td>{cell("SF_3715")}</tr>
      <tr><td>What it requires of you</td><td>Report each unit by <b>1 March each year</b>; substantial compliance earns the licence; non-compliance <b>suspends</b> it and restoration is <b>prospective only</b>.</td>{cell("SF_3715", "SF_HI")}</tr>
    </tbody>
  </table>
  <p class="small" style="margin-top:10px">Full step-by-step for an individual owner: <a href="pages/process.html"><b>Licence &amp; process →</b></a> · What is still missing: <a href="pages/open-questions.html"><b>Open questions →</b></a></p>
</div>

<div class="card alert">
  <h2>2. Do I have to inform the Rent Board and get a licence — as an individual owner, not a corporation?</h2>
  <p><b>Yes — the same rule applies to an individual owner.</b> San Francisco requires <b>all owners of residential property</b> to report their units into the <b>Rent Board Housing Inventory</b>; for a tenant-occupied unit the report generates a <b>rent-increase licence</b>, and the licence must be in effect on the <b>effective date</b> of the increase. Annual and banked increases do not require a petition for approval; whether any separate notice-copy filing applies is not established by those sources (FR-20).</p>
  <table>
    <thead><tr><th style="width:27%">Your question</th><th>Verified answer</th><th style="width:22%">Official source</th></tr></thead>
    <tbody>
      <tr><td>Do I need to tell / report to the Rent Board?</td><td><b>Yes.</b> “All owners of residential property are required to report” into the Housing Inventory, online through the Rent Board Portal. Reporting is free.</td>{cell("SF_HI")}</tr>
      <tr><td>Do I need a licence even though I am a person, not a corporation?</td><td><b>Yes.</b> The rules distinguish by <i>building size</i> (10+ units vs. condominiums and 1–9 unit buildings), not by the owner's legal form. “Property owners who have tenants will receive a rent increase license after the submission.” The total number of units in the building is unverified. For buildings with fewer than 10 units and condominiums reporting began <b>1 March 2023</b>; for other buildings with 10 or more units it began <b>1 July 2022</b>.</td>{cell("SF_HI", "SF_LI")}</tr>
      <tr><td>What the ordinance text itself says about the owner’s legal form</td><td><b>§ 37.15(a) says “Owners” and draws no distinction between a person and a corporation.</b> Verbatim: “<b>Owners</b> of residential dwelling units subject to this Chapter 37 shall be required to report certain information about their units to the Rent Board”, adding only that “in the case of a unit owned by multiple owners, reporting by a single owner shall suffice”. Legal form appears nowhere in § 37.15; the only distinction the ordinance draws is building size.</td>{cell("SF_ORD265T")}</tr>
      <tr><td>Is there a separate application or fee for the licence?</td><td><b>No separate application.</b> “Once you have reported into the Housing Inventory, a rent increase license will be automatically generated for non-owner occupied units.” Reporting is free and the licence “does not need to be included with your rent increase notice”.</td>{cell("SF_HI")}</tr>
      <tr><td>Do I have to file the rent-increase notice with the Rent Board?</td><td>For ordinary annual and banked increases the cited guidance requires no approval petition. It does not explicitly address filing a copy of the tenant notice; confirm any separate filing requirement with the Rent Board. Other increases can have different rules.</td>{cell("SF_571", "SF_BANK")}</tr>
      <tr><td>What happens if I serve the notice without a current licence?</td><td>Two official consequences. The Housing Inventory page: “your rent increase notice will not be enforceable without having a rent increase license on the effective date of the notice”. The noncompliance page: a notice that takes effect while the unit is unlicensed “may be null and void (this may apply for multiple years)”, the tenant “may be entitled to a rent refund”, and the tenant can challenge it by Tenant Petition (Form 516C) or — if the increase has not yet taken effect — by Tenant Summary Petition (Form 518).</td>{cell("SF_HI", "SF_NONCOMP", "ADMIN_373")}</tr>
      <tr><td>Is the licence checked on the notice date or the effective date?</td><td><b>The effective date.</b> Reporting after the deadline is allowed, but the licence must exist <i>on the effective date of the notice</i>.</td>{cell("SF_HI", "SF_NONCOMP")}</tr>
      <tr><td>Does a correct 1.6% calculation cure a missing licence?</td><td><b>No.</b> The licence is a separate pre-condition; the licensing page states the licence must be on file “before any annual or banked rent increase can go into effect”.</td>{cell("SF_HI", "SF_BANK")}</tr>
      <tr><td>Is what I report kept private?</td><td><b>No.</b> “The information entered in the housing inventory submission is public.” The Rent Board lists name and business contact information, approximate square footage, bedrooms, bathrooms and the history of vacancy or occupancy during the past 12 months. The owner reports “the name and business contact information of the owner(s), or of the property manager, if any, designated by the owner(s) to address habitability issues”. The placeholder names on this site therefore cannot be used in the official filing (FR-34).</td>{cell("SF_HI")}</tr>
      <tr><td>Do I need a <b>professional</b> licence to rent my own property?</td><td><b>Not from this rule.</b> The Rent Board “rent increase license” is a unit-level permit generated by the Housing Inventory report — not an occupational licence. Separately, California's broker-licence law regulates people who let, rent or collect rents <i>for another</i> for compensation; renting your own property is not that. Whether an SF business registration number is expected for your rental (“the business registration number for the unit, <b>if any</b>”) is an open item this site cannot confirm — published as FR-37.</td>{cell("LEG_BPC10131", "SF_HI")}</tr>
      <tr><td>Are there increases that need <i>no</i> licence?</td><td>The Rent Board's noncompliance page states the licence rules “apply ONLY to units under San Francisco Rent Control” and that a licence “is not required in some situations where the original occupant(s) no longer live in the unit” (a Section 6.14 or Costa-Hawkins market-rate increase), or for passthroughs allowed under the Rent Ordinance. Petition-based increases have their own filing rules instead.</td>{cell("SF_NONCOMP", "SF_614", "SF_LANDPET")}</tr>      <tr><td>Is the Housing Inventory report the same as the annual Rent Board Fee?</td><td><b>No — separate obligations.</b> Reporting into the Housing Inventory is free and generates the licence; the <b>Rent Board Fee</b> is a separate annual bill (<b>$59.00 per dwelling unit</b> for 2026–27, due 1 March; 50% = $29.50 recoverable from qualifying tenants; 2027 exemption window closes 14 December 2026). Neither satisfies the other.</td>{cell("SF_HI", "SF_FEE")}</tr>
    </tbody>
  </table>
  <p style="margin-top:10px"><b>Bottom line:</b> file the Housing Inventory → confirm the licence is current on the effective date → then calculate, then serve notice. Full sequence: <a href="pages/process.html"><b>Licence &amp; process →</b></a></p>
</div>

<div class="card">
  <h2>3. Key figures</h2>
  <div class="grid">
    <div class="stat"><div class="num">1.6%</div><div class="lbl">Allowable annual increase 1 Mar 2026 – 28 Feb 2027 (60% of Bay Area CPI). Source: {src("SF_LI", "sf.gov")}</div></div>
    <div class="stat"><div class="num">1.4%</div><div class="lbl">Prior year, 1 Mar 2025 – 28 Feb 2026 — the amount at stake for Unit A as a banked increase. Source: {src("SF_571", "Form 571")}</div></div>
    <div class="stat"><div class="num">Unit A: $119.85</div><div class="lbl">3.0% = 1.6% current + 1.4% banked → $3,995 → $4,114.85 on 1 Feb 2027 (calculated; see units page)</div></div>
    <div class="stat"><div class="num">Unit B: $412.65</div><div class="lbl">13.1% = 11.5% banked + 1.6% annual → $3,150 → $3,562.65 — only for an effective date <b>on or before 28 Feb 2027</b>, and <b>conditional</b> on no increase since 2019</div></div>
    <div class="stat"><div class="num">30 / 90 days</div><div class="lbl">Written notice: 30 days if the increase is 10% or less, 90 days if more; +5 days if mailed. Source: {src("LEG_827", "Civ. Code §827")} · {src("LEG_1013", "CCP §1013")}</div></div>
    <div class="stat"><div class="num">Pending: 10%/yr cap</div><div class="lbl">File #261020 (status <b>Pending Committee Action</b>) would cap banked + capital-improvement increases. Source: {src("LEGISTAR_261020", "Legistar")}</div></div>
  </div>
</div>

<div class="card warn">
  <h2>4. What changed on 9 November 2026 — read before serving any notice</h2>
  <p>The Rent Board added a notice to its rent-increase and banking pages on <b>9 November 2026</b>: the Board of Supervisors is considering legislation (<b>File No. 261020</b>) that would <b>temporarily limit the combined amount of banked rent increases and capital improvement rent increases to 10% per year</b>, for the next three years. The Rent Board states that, if enacted as currently proposed, it would apply to <b>banked rent increases noticed on or after 15 September 2026</b> — and that “<b>this legislation has not been enacted and is subject to change</b>”.</p>
  <table>
    <thead><tr><th>Fact</th><th>Status on 13 Nov 2026</th><th>Official source</th></tr></thead>
    <tbody>
      <tr><td>Ordinance title and effect</td><td>Would cap banked + capital-improvement increases at a total of <b>10% per year</b> for rent-controlled units, for three years.</td>{cell("LEGISTAR_261020")}</tr>
      <tr><td>Legislative status</td><td><b>Pending Committee Action</b> — introduced 15 Sep 2026, referred to the Land Use and Transportation Committee; no final action recorded. Not law.</td>{cell("LEGISTAR_261020")}</tr>
      <tr><td>Proposed application date</td><td>Banked increases <b>noticed on or after 15 September 2026</b> (per the Rent Board's 9 Nov 2026 notice).</td>{cell("SF_LI", "SF_BANK")}</tr>
      <tr><td>What this means for a large banked increase</td><td>The illustrative Unit B total of 13.1% includes 11.5% banked, which alone exceeds the proposal’s 10% combined banked-and-capital-improvement limit. The 1.6% annual component is distinct. A 10.0% total contains no more than 10% banked, assuming no capital-improvement increase; eligibility and any final law must still be checked — see <a href="pages/units.html">Units &amp; maths</a>.</td>{cell("SF_BANK", "LEGISTAR_261020")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>5. Short answers to the rest of the brief</h2>
  <table>
    <thead><tr><th style="width:31%">Question</th><th>Answer in one line</th><th style="width:22%">Detail + source</th></tr></thead>
    <tbody>
      <tr><td>What is a reasonable / normal increase under local, state and federal law?</td><td>The annual allowance is not a measure of what is typical or fair. The ceiling is generally the Rent Board percentage (1.6% for 1 Mar 2026 – 28 Feb 2027) plus any properly banked amounts. State law (AB 1482, 8.8% in this region) does not govern because the local cap is lower; the Fair Housing Act prohibits discriminatory terms; federal program rules may also apply.</td>{cell("SF_LI", "LEG_1947", "USC_3604")}</tr>
      <tr><td>How do large corporations handle increases; how do individual owners?</td><td>Official records document allegations involving some large operators and algorithmic pricing; San Francisco prohibits specified algorithmic pricing devices. New-tenancy pricing is subject to exceptions. Individual owners use the Rent Board's annual + banked mechanism, with no petition needed.</td>{cell("SF_ALGO", "DOJ_ALGO", "SF_LI")}</tr>
      <tr><td>How should tenants be told, and what reasons are acceptable?</td><td>Written notice stating the dollar amount, the percentage, the effective date and (if any) the banked part, served 30 or 90 days ahead (+5 if mailed). No reason is required for an annual or banked increase, but the increase must not be retaliatory or based on a protected characteristic or on a new occupant.</td>{cell("SF_LI", "LEG_827", "LEG_1942")}</tr>
      <tr><td>Would a tenant lawyer accept it?</td><td>No result is guaranteed. The 16-point checklist covers lawful percentage, base rent, licence, service, retaliation and discrimination, but it is not a substitute for an independent legal review.</td>{cell("SF_UNLAWFUL", "SF_TENPET", "LEG_12955")}</tr>
      <tr><td>Raise one unit or both?</td><td>No official source requires both units to be raised. Discrimination law prohibits different treatment <i>because of</i> a protected characteristic, so the risk is about the reason and the record, not the number of units. The Rent Board does not hear discrimination claims — those go to the Civil Rights Department or HUD.</td>{cell("LEG_12955", "USC_3604", "SF_TENPET")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>6. Browse by category</h2>
  <div class="cards">
    <a class="tile" href="pages/executive-summary.html"><b>Executive summary</b><span>Every finding in order, licence question first, with the numbers.</span></a>
    <a class="tile" href="pages/process.html"><b>Licence &amp; process</b><span>Step-by-step, notice-date planner, what the Rent Board does and does not need.</span></a>
    <a class="tile" href="pages/units.html"><b>Units &amp; maths</b><span>Unit A and Unit B: dates, percentages, dollars, notice periods, unknowns.</span></a>
    <a class="tile" href="pages/laws.html"><b>Rules &amp; caps</b><span>Local ordinance, state statutes, federal fair housing, 1982–2027 rate table.</span></a>
    <a class="tile" href="pages/questions.html"><b>Open questions</b><span>Every question that blocks a decision, what answers it, and how each answer changes the number.</span></a>
    <a class="tile" href="pages/suggestions.html"><b>Suggestions &amp; decision path</b><span>Decision options, review protocol and 12 improvement proposals — every one still marked <i>Proposed</i>.</span></a>
    <a class="tile" href="pages/reasonable.html"><b>Reasonable &amp; normal</b><span>What the law does and does not call reasonable; what can be benchmarked.</span></a>
    <a class="tile" href="pages/practice.html"><b>Market practice</b><span>Corporate vs individual landlord practice, with official evidence only.</span></a>
    <a class="tile" href="pages/notice.html"><b>Notice &amp; reasons</b><span>Required contents, service, timing, model wording, prohibited reasons.</span></a>
    <a class="tile" href="pages/review.html"><b>Tenant-lawyer test</b><span>16 checks a tenant-side reviewer would run, and how to pass each.</span></a>
    <a class="tile" href="pages/discrimination.html"><b>One unit or both?</b><span>Fair-housing analysis of selective increases, plus a documentation protocol.</span></a>
    <a class="tile" href="pages/open-questions.html"><b>Known vs unknown</b><span>What we already have, what is missing, and the official route that closes each gap.</span></a>
    <a class="tile" href="pages/requirements.html"><b>Requirements checklist</b><span>Every item in the brief, where it is answered, and its verification status.</span></a>
    <a class="tile" href="pages/sources.html"><b>Sources register</b><span>Every official source, the claim it supports, and the date retrieved.</span></a>
    <a class="tile" href="pages/flagged.html"><b>Flagged for review</b><span>Unverified, blank or internally inconsistent items — published, not hidden.</span></a>
    <a class="tile" href="verification/index.html"><b>Independent verification edition</b><span>Second self-contained pass: every official source re-fetched, arithmetic recomputed, flags F-11…F-23.</span></a>
  </div>
</div>

<div class="card tight">
  <p class="small" style="margin:0"><b>Reading order for a first-timer:</b> this page → <a href="pages/process.html">Licence &amp; process</a> → <a href="pages/units.html">Units &amp; maths</a> → <a href="pages/review.html">Tenant-lawyer test</a>. If you are about to serve a notice, also read <a href="pages/notice.html">Notice &amp; reasons</a> and the <a href="pages/flagged.html">open flags</a> (especially the licence status and Unit B rent history).</p>
</div>
"""
    return page("index.html", "Dashboard", body,
                "Verified answers on San Francisco rent increases for two rent-controlled units: Rent Board licence, notice, banking and fair housing.")


# ------------------------------------------------------------------ executive summary
def executive_summary():
    body = f"""
<div class="card">
  <h1>Executive summary</h1>
  <p class="lede">Two owner-reported rent-controlled units, built in 1940, San Francisco. Total building unit count and coverage are unverified. Location withheld; rules cited apply citywide. Tenant names replaced with letters; dates and amounts unchanged.</p>
</div>

<div class="card alert">
  <h2>Forefront, part 1 — is the duty to inform the Rent Board a state law or a local law?</h2>
  <p><b>It is a local law — a San Francisco ordinance — not a state law.</b> The duty comes from <b>Ordinance No. 265-20</b> (Board of Supervisors File No. 201262), which amended the <b>San Francisco Administrative Code</b>: it added <b>§ 37.15 “Reporting Obligations; Licensing”</b>, revised <b>§ 37.3</b> so that the annual increase and banking are both “subject to Section 37.15”, and added a separate surcharge section, <b>§ 37A.4.5</b>. No California statute requires an owner to report to the Rent Board. Verified 13 November 2026.</p>
  <table>
    <thead><tr><th style="width:26%">The question behind the question</th><th>Verified answer</th><th style="width:22%">Official source</th></tr></thead>
    <tbody>
      <tr><td>State or local?</td><td><b>Local.</b> Enacted by the City and County of San Francisco and codified in the San Francisco Administrative Code. The published code section carries the credit line “<b>[Added by Ord. No. 265-20, effective January 18, 2021]</b>”.</td>{cell("SF_3715", "SF_ORD265T")}</tr>
      <tr><td>Then why does it feel like “the 2023 law”?</td><td><b>Three different dates attach to one 2020 ordinance.</b> It was finally passed <b>8 December 2020</b> and approved by the Mayor <b>18 December 2020</b>; § 4 makes it effective 30 days after enactment and <b>operative 1 July 2022</b>; and § 37.15(c) sets the <b>commencement of reporting</b> at <b>1 March 2023</b> for condominium units and units in buildings with fewer than 10 units. A 1–9 unit building's first obligation therefore fell on 1 March 2023 — which is why the requirement is remembered as “since 2023”.</td>{cell("SF_ORD265T", "SF_3715", "SF_HI")}</tr>
      <tr><td>Does state law appear anywhere in it?</td><td><b>Only to say what the inventory is not.</b> § 37.15(d): “The Rent Board shall not use the information to operate a rental registry within the meaning of <b>California Civil Code Sections 1947.7 – 1947.8</b>.” State law is referenced; it does not impose the duty.</td>{cell("SF_3715", "SF_ORD265T")}</tr>
      <tr><td>Does the state rent-cap law (AB 1482) require this?</td><td><b>No.</b> AB 1482 sets a ceiling on the <i>amount</i> of an increase and imposes no filing or licence duty at all; it creates no reporting duty, and it does not govern here because it does not apply where a local ordinance allows a lower increase, and San Francisco's is lower.</td>{cell("LEG_1947", "OAG", "SF_LI")}</tr>
      <tr><td>What the ordinance actually requires of you</td><td>Report each residential unit into the <b>Rent Board Housing Inventory</b> by <b>1 March each year</b>; substantial compliance earns the <b>licence to impose rent increases</b> under §§ 37.3(a)(1)–(2). Without substantial compliance the licence is <b>temporarily suspended</b> for the period of non-compliance and is restored only <b>prospectively</b> — “a tenant shall not be obligated to pay the increased rent for months during the period of suspension”.</td>{cell("SF_3715", "SF_HI")}</tr>
      <tr><td>How to cite it correctly</td><td>Cite <b>Ordinance No. 265-20 (File 201262)</b> and <b>S.F. Admin. Code § 37.15</b>. Citing “the 2023 law” is what produced the state/local confusion in the first place; the date nuance is recorded as FR-40.</td>{cell("SF_ORD265T", "SF_3715")}</tr>
    </tbody>
  </table>
  <p style="margin-top:10px"><b>Bottom line:</b> local ordinance, City obligation, 1 March annual deadline, licence on the effective date. Part 2 below answers what an individual owner must actually do, step by step. The full information register is on <a href="open-questions.html"><b>Known vs unknown →</b></a> and the decision gate is on <a href="questions.html"><b>Open questions →</b></a></p>
</div>

<div class="card alert">
  <h2>Forefront, part 2 — the Rent Board notification and licence question (individual owner)</h2>
  <p><b>Which law?</b> Part 1 above established that this duty is <b>local San Francisco law</b> — Ordinance No. 265-20 (File 201262), codified at Administrative Code § 37.15 — and not a state law. The table below answers what an individual owner must actually do.</p>
  <p><b>Annual and banked increases do not require a Rent Board approval petition. Any separate notice-copy filing requirement remains unverified (FR-20). You do have to report the units into the Housing Inventory and hold a current rent-increase licence on the effective date — and that obligation applies to you as an individual owner exactly as it would to a corporation.</b></p>
  <table>
    <thead><tr><th style="width:30%">Point</th><th>Verified position</th><th style="width:22%">Official source</th></tr></thead>
    <tbody>
      <tr><td>Which level of government imposes it</td><td><b>City and County of San Francisco.</b> Ordinance No. 265-20 became effective 18 January 2021 and created the Housing Inventory plus the licence requirement. State law requires no notice to any board and no licence.</td>{cell("SF_ORD265", "LEG_1947")}</tr>
      <tr><td>Who must report</td><td>All owners of residential property. “Most owners are required to do this even if you are not a landlord.”</td>{cell("SF_HI")}</tr>
      <tr><td>What the report produces</td><td>A rent-increase licence, generated automatically for non-owner-occupied units.</td>{cell("SF_HI")}</tr>
      <tr><td>When the licence must exist</td><td>On the <b>effective date</b> of the increase — not merely by the notice date.</td>{cell("SF_HI")}</tr>
      <tr><td>Reporting start dates by building size</td><td>Reporting began <b>1 March 2023</b> for condominiums and buildings with fewer than 10 units, and <b>1 July 2022</b> for other buildings with 10 or more units. The total building size is unverified.</td>{cell("SF_HI", "SF_LI")}</tr>
      <tr><td>Annual deadline</td><td><b>1 March every year</b>. There is no monetary penalty for filing late, but a late licence does not save an increase that took effect earlier.</td>{cell("SF_HI")}</tr>
      <tr><td>Per-increase approval</td><td><b>None needed</b> for annual or banked increases; no petition is filed for them.</td>{cell("SF_571", "SF_BANK")}</tr>
      <tr><td>Consequence of no licence</td><td>The notice “will not be enforceable without having a rent increase license on the effective date”. The Rent Board's noncompliance page is stronger still: a notice that takes effect while the unit is unlicensed “may be null and void (this may apply for multiple years)”, and the tenant “may be entitled to a rent refund” (Form 516C, or Form 518 before the effective date).</td>{cell("SF_HI", "SF_NONCOMP", "ADMIN_373")}</tr>
      <tr><td>Increases that do <b>not</b> need the licence</td><td>The noncompliance page: the licence rules apply only to rent-controlled units, and “the Rent Increase License is not required in some situations where the original occupant(s) no longer live in the unit” (Section 6.14 / Costa-Hawkins) “or for passthroughs allowed under the Rent Ordinance”. A market-rate increase under those provisions is a different, evidence-heavy track — see FR-21 and FR-33.</td>{cell("SF_NONCOMP", "SF_614")}</tr>
      <tr><td>Separate Rent Board Fee</td><td>Distinct from the free Housing Inventory report: <b>$59.00 per dwelling unit</b> for 2026–27 (due 1 March; 50% recoverable from qualifying tenants; 2027 exemption deadline 14 December 2026).</td>{cell("SF_FEE", "SF_HI")}</tr>
    </tbody>
  </table>
  <p class="small" style="margin-top:8px">Practical sequence: report → confirm licence → calculate → serve notice. Full walk-through with dates: <a href="process.html">Licence &amp; process</a>. Before serving, work down <a href="questions.html">Open questions</a> — 14 blocking items, each naming where its answer comes from.</p>
</div>

<div class="card">
  <h2>1. The two units (owner-reported facts)</h2>
  <div class="facts">
    <div><span>Unit A — lease start</span><br><b>1 February 2025</b></div>
    <div><span>Unit A — base rent</span><br><b>$3,995 / month</b> (unchanged)</div>
    <div><span>Unit A — tenants</span><br>Initial lease: <b>Tenant A</b>, <b>Tenant E</b>, <b>Tenant F</b> · Continuing 1 April 2026 at $3,995: <b>Tenant A</b> (original) and <b>Tenant B</b></div>
    <div><span>Unit B — lease start</span><br><b>1 June 2019</b></div>
    <div><span>Unit B — 2019 starting rent</span><br><b>$3,150 / month</b> (current rent and increase history unverified)</div>
    <div><span>Unit B — tenants</span><br><b>Tenant C</b>, <b>Tenant D</b></div>
  </div>
  <p class="small">These are owner statements, not government records. The rent history and licence status are the two facts that most change the answer — both are on the <a href="flagged.html">Flagged for review</a> page.</p>
</div>

<div class="card">
  <h2>2. What is lawful for each unit</h2>
  <table>
    <thead><tr><th>Unit</th><th>Lawful ceiling</th><th>Dollar amount (calculated)</th><th>Notice period</th><th style="width:22%">Source for the percentage</th></tr></thead>
    <tbody>
      <tr><td>Unit A — conditional first increase on 1 Feb 2027</td><td>1.6% annual + 1.4% banked = <b>3.0%</b></td><td>$119.85 → <b>$4,114.85</b></td><td><b>30 days</b> (35 if mailed)</td>{cell("SF_571", "SF_BANK")}</tr>
      <tr><td>Unit A — conservative alternative</td><td>1.6% annual only = 1.6%</td><td>$63.92 → <b>$4,058.92</b></td><td>30 days (35 if mailed)</td>{cell("SF_571")}</tr>
      <tr><td>Unit B — 10% phased</td><td><b>10.0%</b> (illustrative; subject to history and legislation)</td><td>$315.00 → <b>$3,465.00</b></td><td>30 days (35 if mailed)</td>{cell("SF_BANK", "LEGISTAR_261020")}</tr>
      <tr><td>Unit B — banked only (2020–2025)</td><td>11.5% banked</td><td>$362.25 → <b>$3,512.25</b></td><td><b>90 days</b> (95 if mailed)</td>{cell("SF_BANK", "SF_571")}</tr>
      <tr><td>Unit B — conditional maximum for an effective date on or before 28 Feb 2027</td><td>11.5% banked (2020–2025) + 1.6% annual in force = <b>13.1%</b></td><td>$412.65 → <b>$3,562.65</b></td><td>90 days (95 if mailed)</td>{cell("SF_BANK", "SF_571")}</tr>
      <tr><td>Unit B — on 1 June 2027 anniversary</td><td>13.1% banked floor (seven skipped years 2020–2026) + <b>blank</b> (2027–28 rate not yet announced)</td><td><b>Blank</b> ($412.65 floor before 2027–28 annual)</td><td>90 days if &gt;10%</td>{cell("SF_BANK", "SF_571", "SF_LI")}</tr>
      <tr><td>Unit B — if an increase was taken at any time since 2019</td><td colspan="3"><b>Blank — must be recalculated from the actual rent history.</b> The banked total depends on which years were skipped.</td>{cell("SF_BANK")}</tr>
    </tbody>
  </table>
  <p class="small">Percentages are official; dollar amounts are arithmetic on the owner-reported base rent (base rent only — no passthroughs, no rounding up). Detail and date planners: <a href="units.html">Units &amp; maths</a>.</p>
</div>

<div class="card">
  <h2>3. Findings, in the order the brief asked for them</h2>
  <table>
    <thead><tr><th style="width:26%">Question asked</th><th>Finding</th><th style="width:20%">Where + source</th></tr></thead>
    <tbody>
      <tr><td>Reasonable and normal increases under local, state and federal law (ZIP-level)</td><td><b>Local:</b> 1.6% annual plus properly banked amounts; the Rent Board sets one citywide percentage — it publishes no ZIP-level or neighbourhood rate. <b>State:</b> AB 1482 would allow 8.8% for increases starting 1 Aug 2026 – 31 Jul 2027, but it does not apply where a local ordinance allows a <i>lower</i> increase, and San Francisco's is lower. <b>Federal:</b> fair-housing law prohibits discriminatory rental terms; subsidy or program rules may impose other restrictions.</td>{cell("SF_LI", "OAG", "LEG_1947", "USC_3604")}</tr>
      <tr><td>Are these 1940-built units rent-controlled?</td><td>Units built on or before <b>13 June 1979</b> are generally covered by rent control and eviction protection, except single-family dwellings and most condominiums. Coverage is owner-reported, not verified. Confirm the building record, unit type, and any exemptions before relying on the calculations.</td>{cell("SF_LAWS")}</tr>
      <tr><td>How do big corporations handle increases?</td><td>Documented official evidence is about <b>vacancy/turnover pricing</b> and <b>algorithmic pricing</b>: San Francisco bans selling or using algorithmic devices to set rents (Rent Ordinance § 37.10C), and the U.S. Department of Justice sued six of the largest landlords over shared-data rent algorithms. The Rent Board confirms there is no limit on the first rent charged for an empty covered unit.</td>{cell("SF_ALGO", "DOJ_ALGO", "SF_LI")}</tr>
      <tr><td>How do individual owners handle increases?</td><td>By the annual allowable increase once every 12 months, plus banked amounts, with a rent-increase licence — no petition and no lawyer required, with free counselling from the Rent Board.</td>{cell("SF_LI", "SF_BANK", "SF_COUNSEL")}</tr>
      <tr><td>Correct way to inform tenants / acceptable reasons</td><td>Written notice with the dollar amount, percentage, effective date, banked breakdown and dates used for banking; 30 or 90 days; +5 days if mailed. No reason has to be given for an annual or banked increase, but the increase may not be retaliatory, may not rest on a protected characteristic, and may not charge extra merely because an occupant joined.</td>{cell("SF_LI", "SF_BANK", "LEG_827", "LEG_1942")}</tr>
      <tr><td>Would a tenant lawyer accept it?</td><td>No one can guarantee a tenant lawyer will approve an increase or that it cannot be challenged. The checklist helps identify issues; obtain independent legal advice and confirm the records. Tenants may file an unlawful-rent-increase petition.</td>{cell("SF_UNLAWFUL", "SF_TENPET")}</tr>
      <tr><td>One tenant's unit or both?</td><td>Nothing in the ordinance or in fair-housing law requires uniform increases. The risk to manage is <i>differential treatment for a prohibited reason</i>. A written, dated rationale per unit (rent history, anniversary date, lawful ceiling) is the practical control. Discrimination claims are heard by the Civil Rights Department or HUD, not the Rent Board.</td>{cell("LEG_12955", "USC_3604", "SF_TENPET")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>4. Two official statements that do not say the same thing</h2>
  <p>Both are official Rent Board pages; they matter because they decide whether Unit A's 1.4% can be banked.</p>
  <table>
    <thead><tr><th style="width:22%">Source</th><th>What it says</th><th>Effect for Unit A</th><th style="width:20%">Link</th></tr></thead>
    <tbody>
      <tr><td>Banked rent increases page</td><td>“A skipped increase is only banked if at least <b>24 full months</b> pass without any rent increase. If less than 24 months pass, the skipped increase is lost…”</td><td>On 1 Feb 2027 exactly 24 months have passed since the 1 Feb 2025 rent — so the 1.4% is banked on this reading.</td>{cell("SF_BANK")}</tr>
      <tr><td>“Learn about rent increases” worked example</td><td>Applies a <b>12-month</b> test to each skipped increase (“a full 12 months has not elapsed between the date it first became available … and the date of the rent increase” ⇒ lost).</td><td>1.4% became available 1 Feb 2026; the 1 Feb 2027 increase is 12 months later — banked on this reading too.</td>{cell("SF_LI")}</tr>
      <tr><td>Consequence</td><td>The two page texts use different wording but both permit Unit A's 1.4% at 1 Feb 2027. The gap between them is published on the <a href="flagged.html">Flagged</a> page (FR-03) and should be confirmed with a Rent Board counsellor before the notice is served.</td><td><b>3.0% is supportable; 1.6% is the fallback that is lawful under either reading.</b></td>{cell("SF_COUNSEL")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>5. What to do next</h2>
  <ol class="steps">
    <li><b>Confirm the licence.</b> Log into the Rent Board Portal, check the Housing Inventory entry for both units, and confirm a licence is current for the planned effective date. Source: {src("SF_HI", "sf.gov — Housing Inventory")} · {src("SF_PORTAL", "portal.sfrb.org")}</li>
    <li><b>Confirm Unit B's rent history.</b> Leases, notices and rent ledger 2019–2026. Without it the 13.1% figure stays conditional. Source: {src("SF_BANK", "sf.gov — banked increases")}</li>
    <li><b>Consider the options.</b> The annual-only 1.6% is a smaller illustrative option for each unit through 28 February 2027. Any banked amount, including Unit A at 3.0% or Unit B at 10.0% or 13.1%, needs a verified ledger, correct anniversary, current licence and review of pending legislation; no amount is guaranteed to pass review. Source: {src("SF_LI", "sf.gov — rent increases")} · {src("LEGISTAR_261020", "File #261020")}</li>
    <li><b>Serve notice in time.</b> 30 days for ≤10%, 90 days for &gt;10%, +5 if mailed. Worked dates: <a href="process.html">Licence &amp; process</a>. Source: {src("LEG_827", "Civ. Code §827")} · {src("LEG_1013", "CCP §1013")}</li>
    <li><b>Keep the file.</b> Notice, proof of service, licence screenshot, calculation sheet, and the reason each unit's amount differs.</li>
  </ol>
</div>
"""
    return page("pages/executive-summary.html", "Executive summary", body,
                "Executive summary: Rent Board licence requirement for individual owners, lawful increases for both units, notice and fair-housing findings.", active="pages/executive-summary.html")


# ------------------------------------------------------------------ process
def process():
    body = f"""
<div class="card">
  <h1>Licence &amp; process — step by step</h1>
  <p class="lede">Written for someone who has never raised rent through the Rent Board. Each step states what to do, what the official source says, and what to keep.</p>
</div>

<div class="card hero">
  <h2>The whole process in one sentence</h2>
  <p><b>Report both units in the Rent Board Housing Inventory → check that a rent-increase licence is current on your chosen effective date → calculate the annual percentage in effect on that date (+ any banked amounts) on base rent only → serve the correct written notice with the right lead time → keep proof.</b> Annual and banked increases do not require a petition for approval. The cited guidance does not explicitly resolve whether a notice copy must be filed; confirm that question with the Rent Board.</p>
</div>

<div class="card">
  <h2>Step-by-step</h2>
  <ol class="steps">
    <li><b>Check that the units are covered.</b> Units built on or before 13 June 1979 generally have rent control and eviction protection, unless the unit is a single-family dwelling or most condominiums. The construction year and rent-control status are owner-reported; the total number of units and applicable exemptions are unknown. Confirm the City property record and consult a Rent Board counsellor.
      <div class="small">Source: {srcs("SF_LAWS", "SF_COUNSEL")}</div></li>
    <li><b>Report into the Housing Inventory — every year, by 1 March.</b> Use the Rent Board Portal, create an account, and report each unit: owner/manager business contact, business registration if any, approximate square footage in 250 sq ft increments, bedrooms, bathrooms, occupancy start date and base rent in $250 increments (plus whether utilities are included). Submissions are made under penalty of perjury. Reporting is free and there is no monetary penalty for filing after the deadline; owners who cannot access the online Portal may submit paper filings by email (<code>rentboard.inventory@sfgov.org</code>) or at the Rent Board office, though paper processing is slower. (Note: the annual <b>Rent Board Fee</b> — $59.00 per dwelling unit for 2026–27, due 1 March — is a separate obligation from the free Housing Inventory report.) <b>Two practical points:</b> to add the property to a Portal account you need “the PIN number on your Annual Notice” (call 311 to reset it), and “the information entered in the housing inventory submission is public” — name and business contact information, approximate square footage, bedrooms, bathrooms and recent vacancy or occupancy history (FR-34).
      <div class="small">Source: {srcs("SF_HI", "SF_NONCOMP", "SF_FEE", "SF_PORTAL")}</div></li>
    <li><b>Confirm the licence — on the effective date, not the notice date.</b> A licence is generated automatically for non-owner-occupied units after the report. Check it in the Portal. The Rent Board's exact test is that the licence be held “on the effective date of the notice”; without it the notice “will not be enforceable”. The licence does not have to be sent with the notice. The Rent Board's noncompliance page states the practical stakes: a notice that takes effect while the unit is unlicensed “may be null and void (this may apply for multiple years)” and the tenant “may be entitled to a rent refund”.
      <div class="small">Source: {srcs("SF_HI", "SF_BANK", "SF_NONCOMP")}</div></li>
    <li><b>Calculate on base rent only, using the percentage in effect on the effective date.</b> Base rent includes housing services such as parking or storage and excludes temporary passthroughs and fluctuating charges. Do not round up. Use the percentage that will be in effect on the date of the increase, not the date the notice is served. For an increase effective from 1 March 2026 through 28 February 2027 that is <b>1.6%</b>. Review fixed-term lease provisions with counsel; the statutory notice procedure cited here covers periodic tenancies.
      <div class="small">Source: {srcs("SF_LI", "SF_571")}</div></li>
    <li><b>Add any banked amounts — additively, never compounded.</b> A skipped increase is banked when the Rent Board's conditions are met; banked percentages are added together and then multiplied by the current base rent. There is no cap on banked amounts back to 1 April 1982, they do not expire during the tenancy, and they cannot be carried to a new tenant.
      <div class="small">Source: {srcs("SF_BANK", "SF_MULTI")}</div></li>
    <li><b>Check the timing conditions before you commit.</b> The first annual increase can be imposed 12 months after the lease began; after that, no more than once every 12 months on the tenant's anniversary date; if you increase later than the anniversary, the effective date becomes the new anniversary date and a later annual increase may be lost. Avoid retaliatory increases. A recent habitability complaint or repair request calls for particular caution; protections can extend beyond 180 days. Consult counsel. Do not charge extra because a new occupant moved in. <b>Civil Code § 1942.4</b> bars serving any rent-increase notice while a public officer's written notice of substandard conditions stands unabated more than 35 days without good cause and the tenant did not cause the condition — check the building's inspection record before drafting.
      <div class="small">Source: {srcs("SF_LI", "LEG_1942", "LEG_19424")}</div></li>
    <li><b>Serve the written notice in time.</b> 30 days' written notice if the increase is 10% or less of the rent charged at any time in the previous 12 months (alone or combined with other increases); 90 days if more than 10%. Personal delivery, or mail under Code of Civil Procedure § 1013 — if mailed, add 5 calendar days. State the dollar amount, the percentage, the effective date and, for a banked increase, which part is banked and the dates underlying it.
      <div class="small">Source: {srcs("LEG_827", "LEG_1013", "SF_BANK", "SF_RULE4")}</div></li>
    <li><b>Keep the file and diarise next year.</b> Keep the notice, proof of service, a screenshot of the current licence, the calculation and the rent history. Update owner/manager contact details within 30 days of any change and re-report by 1 March. The date of the increase becomes the new anniversary date.
      <div class="small">Source: {srcs("SF_HI", "SF_LI")}</div></li>
    <li><b>If a tenant petitions, respond with the file.</b> Before an increase takes effect, a tenant who sees no licence in the Portal may file a <b>Tenant Summary Petition (Form 518)</b>; after an increase takes effect, a tenant may file a <b>Tenant Petition (Form 516C, box C)</b> for an unlawful rent increase or a determination of lawful rent — free, with no filing deadline — heard by a Rent Board Administrative Law Judge without needing a lawyer.
      <div class="small">Source: {srcs("SF_NONCOMP", "SF_UNLAWFUL", "SF_TENPET")}</div></li>
  </ol>
</div>

<div class="card">
  <h2>What the Rent Board does and does not do for an annual or banked increase</h2>
  <table>
    <thead><tr><th style="width:34%">Action</th><th>Required?</th><th style="width:24%">Source</th></tr></thead>
    <tbody>
      <tr><td>Report the unit into the Housing Inventory</td><td><b>Yes</b> — annually, by 1 March, all owners (free).</td>{cell("SF_HI")}</tr>
      <tr><td>Obtain a rent-increase licence</td><td><b>Yes</b> — automatic once reported; must be in effect on the effective date.</td>{cell("SF_HI", "SF_NONCOMP")}</tr>
      <tr><td>Pay the separate annual Rent Board Fee</td><td><b>Yes, unless exempt</b> — $59.00 per dwelling unit for 2026–27, due 1 March (5% monthly penalty up to 15%; 50% = $29.50 recoverable from tenants in occupancy as of 1 November; 2027 exemption window closes 14 December 2026). Separate from the licence report.</td>{cell("SF_FEE", "SF_HI")}</tr>
      <tr><td>File a petition for the annual or banked increase</td><td><b>No</b> — no petition is required for these.</td>{cell("SF_571", "SF_MULTI")}</tr>
      <tr><td>Send a copy of the notice to the Rent Board</td><td><b>Unverified</b> — no petition or approval is required, but this alone does not settle whether any separate copy-filing requirement applies. Confirm with the Rent Board (FR-20); the licence does not have to accompany the tenant notice.</td>{cell("SF_HI", "SF_LI")}</tr>
      <tr><td>Other increases and passthroughs</td><td>Rules vary: capital improvement, operating and maintenance, and special-circumstances increases require petitions filed before notice. Bond passthroughs do not require petitions; use the applicable worksheet. Some utility passthrough worksheets must be filed before notice.</td>{cell("SF_LANDPET")}</tr>
      <tr><td>Ask the Rent Board to decide the lawful rent</td><td>Optional — either side may petition for a determination of lawful rent.</td>{cell("SF_LANDPET", "SF_UNLAWFUL")}</tr>
      <tr><td>Licence for a market-rate or passthrough increase</td><td>Not the same track: the licence rules apply to annual and banked increases on rent-controlled units; the noncompliance page states a licence is not required where the original occupants no longer live in the unit (Section 6.14 / Costa-Hawkins) or for passthroughs, which have their own petition rules.</td>{cell("SF_NONCOMP", "SF_614", "SF_LANDPET")}</tr>
      <tr><td>Answer the blocking questions first</td><td>Fourteen questions must be settled from your own records before a notice is defensible — the register, the document list and the sensitivity table are on <a href="questions.html">Open questions</a>.</td>{cell("SF_HI", "SF_BANK")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2 id="planner">Notice-date planner (calculated for this file, 13 November 2026)</h2>
  <p class="small">Arithmetic from the statutory lead times: 30 or 90 days before the effective date; +5 calendar days when served by mail within California. Verify against the statutes before serving.</p>
  <table>
    <thead><tr><th>Target effective date</th><th>Increase size</th><th>Serve in person by</th><th>Mail by</th><th style="width:20%">Rule</th></tr></thead>
    <tbody>
      <tr><td>1 Feb 2027 — Unit A (3.0% or 1.6%)</td><td>≤10%</td><td><b>2 Jan 2027</b></td><td>28 Dec 2026</td>{cell("LEG_827", "LEG_1013")}</tr>
      <tr><td>1 Feb 2027 — Unit B at 10.0%</td><td>10% (not more than 10%)</td><td><b>2 Jan 2027</b></td><td>28 Dec 2026</td>{cell("LEG_827", "LEG_1013")}</tr>
      <tr><td>1 Feb 2027 — Unit B at 13.1%</td><td>&gt;10%</td><td><span class="badge danger">3 Nov 2026 — passed</span></td><td>29 Oct 2026 — passed</td>{cell("LEG_827")}</tr>
      <tr><td>8 Feb 2027 — Unit B at 13.1% (historical example)</td><td>&gt;10%</td><td><span class="badge danger">10 Nov 2026 — passed</span></td><td><span class="badge danger">5 Nov 2026 — passed</span></td>{cell("LEG_827", "LEG_1013")}</tr>
      <tr><td>11 Feb 2027 — Unit B at 13.1% (earliest date reachable from the 13 Nov 2026 pass)</td><td>&gt;10%</td><td><b>13 Nov 2026 — research-pass date (personal service only)</b></td><td><span class="badge danger">8 Nov 2026 — passed</span></td>{cell("LEG_827", "LEG_1013")}</tr>
      <tr><td>14 Feb 2027 — Unit B at 13.1%</td><td>&gt;10%</td><td>16 Nov 2026</td><td><span class="badge danger">11 Nov 2026 — passed</span> federal holiday (Veterans Day); postal service that day unverified (FR-27)</td>{cell("LEG_827", "LEG_1013", "OPM_HOLIDAYS")}</tr>
      <tr><td>18 Feb 2027 — Unit B at 13.1% (example still open on 13 Nov 2026)</td><td>&gt;10%</td><td>20 Nov 2026</td><td>15 Nov 2026</td>{cell("LEG_827", "LEG_1013")}</tr>      <tr><td>16 Feb 2027 — Unit B at 13.1% (first date reachable by mail on the 13 Nov 2026 pass)</td><td>&gt;10%</td><td>18 Nov 2026</td><td><b>13 Nov 2026 — research-pass date (mail today)</b></td>{cell("LEG_827", "LEG_1013")}</tr>      <tr><td>Any date from 1 March 2027 onward</td><td>Any</td><td colspan="2"><b>Blank — the allowable percentage for 1 Mar 2027 – 29 Feb 2028 has not been announced.</b> Use the percentage in effect on the effective date.</td>{cell("SF_LI")}</tr>
    </tbody>
  </table>
  <p class="small">These are fixed-date examples, not a live calculator. Count forward from actual service and allow 30 or 90 days, plus any applicable mailing extension; confirm deadlines and current rules before serving.</p>
</div>

<div class="card">
  <h2>Who to call, officially</h2>
  <table>
    <thead><tr><th>Body</th><th>What for</th><th style="width:22%">Source</th></tr></thead>
    <tbody>
      <tr><td>SF Rent Board counselling line — 415-252-4600, weekdays 9–12 and 1–4</td><td>Confirm coverage, anniversary dates, banked amounts and licence status before serving notice.</td>{cell("SF_COUNSEL")}</tr>
      <tr><td>311 (415-701-2311 from outside San Francisco)</td><td>Questions about the Housing Inventory.</td>{cell("SF_HI")}</tr>
      <tr><td>Rent Board Portal — portal.sfrb.org</td><td>Report units, check licence status, look up a property.</td>{cell("SF_PORTAL")}</tr>
    </tbody>
  </table>
</div>
"""
    return page("pages/process.html", "Licence &amp; process", body,
                "Step-by-step San Francisco rent increase process: Housing Inventory, rent-increase licence, calculation, notice, service and records.")


# ------------------------------------------------------------------ units
def units():
    body = f"""
<div class="card">
  <h1>Units &amp; maths</h1>
  <p class="lede">Facts as reported by the owner, then every lawful option with the arithmetic shown. Percentages are official; dollar amounts are calculated on base rent only.</p>
</div>

<div class="card">
  <h2>Unit A — facts (owner-reported)</h2>
  <div class="facts">
    <div><span>Lease start</span><br><b>1 February 2025</b></div>
    <div><span>Base rent</span><br><b>$3,995.00 / month</b></div>
    <div><span>Reported rent on 1 April 2026</span><br><b>$3,995.00</b> — later history unverified</div>
    <div><span>Tenancy</span><br>Initial lease: <b>Tenant A</b>, <b>Tenant E</b> and <b>Tenant F</b> · Continuing <b>1 April 2026</b> at $3,995: <b>Tenant A</b> (original) and <b>Tenant B</b></div>
    <div><span>First increase available</span><br><b>1 February 2026</b> (12 months after the lease began) — assuming no increase</div>
    <div><span>Next date reachable</span><br><b>1 February 2027</b> — 24 months after the lease began</div>
  </div>
  <p class="small">Why this is a controlled continuation and not a market reset: under Administrative Code § 37.3(d)(2)(B) and Rent Board Rule § 6.14, Costa-Hawkins / § 6.14 unlimited increases do <i>not</i> apply to partial changes in occupancy while an original occupant (<b>Tenant A</b>) remains in lawful possession, and under § 37.3(a)(11)(A) adding an occupant (<b>Tenant B</b>) never authorises an extra rent charge. If instead the 1 April 2026 lease is treated as restarting the 12-month anniversary clock, the first increase would fall on 1 April 2027 — both dates are on the <a href="flagged.html">Flagged</a> page (FR-02). Sources: {srcs("ADMIN_373", "SF_614", "SF_LI")}</p>
</div>

<div class="card">
  <h2>Unit A — lawful options on 1 February 2027 (calculated)</h2>
  <table>
    <thead><tr><th>Basis</th><th>Percentage</th><th>Dollar increase</th><th>New rent</th><th>Notice</th><th style="width:19%">Official source for the %</th></tr></thead>
    <tbody>
      <tr><td>Annual only (1.6% in effect 1 Mar 2026 – 28 Feb 2027)</td><td>1.6%</td><td>$63.92</td><td><b>$4,058.92</b></td><td>30 days</td>{cell("SF_571")}</tr>
      <tr><td>Annual 1.6% + banked 1.4% (the 1.4% applied 1 Mar 2025 – 28 Feb 2026, skipped on 1 Feb 2026)</td><td>3.0%</td><td>$119.85</td><td><b>$4,114.85</b></td><td>30 days</td>{cell("SF_571", "SF_BANK")}</tr>
      <tr><td>If the 1.4% is treated as lost (stricter reading of the banking rule)</td><td>1.6%</td><td>$63.92</td><td><b>$4,058.92</b></td><td>30 days</td>{cell("SF_BANK")}</tr>
      <tr><td>1 April 2027 (if the 1 April 2026 lease restarts the anniversary)</td><td colspan="2"><b>Blank — the percentage for 1 Mar 2027 – 29 Feb 2028 has not been announced</b></td><td>—</td><td>30 days if ≤10%</td>{cell("SF_LI")}</tr>
    </tbody>
  </table>
  <p class="small"><b>Rate to use:</b> the percentage in effect on the <i>effective date</i> — 1.6% for any date up to 28 February 2027. No rounding up. Base rent only.</p>
</div>

<div class="card">
  <h2>Unit B — facts (owner-reported)</h2>
  <div class="facts">
    <div><span>Lease start</span><br><b>1 June 2019</b></div>
    <div><span>Base rent</span><br><b>$3,150.00 / month</b></div>
    <div><span>Starting rent, 2019</span><br><b>$3,150.00</b> — current rent and increase history unverified</div>
    <div><span>Tenants</span><br><b>Tenant C</b> and <b>Tenant D</b></div>
    <div><span>First increase available</span><br><b>1 June 2020</b> — assuming no increase</div>
    <div><span>Assumed anniversary</span><br><b>1 June</b> (only if no increase has reset it)</div>
  </div>
  <p class="small"><b>The critical unknown:</b> if any increase was imposed at any point since 1 June 2019, the banked total below is wrong. Confirm from leases, notices and the rent ledger before serving anything (FR-01).</p>
</div>

<div class="card">
  <h2>Unit B — six annual percentages, assuming all were skipped</h2>
  <table>
    <thead><tr><th>Increase year (anniversary)</th><th>Rate period (Form 571)</th><th>Allowable percentage</th><th>Status</th><th style="width:20%">Official source</th></tr></thead>
    <tbody>
      <tr><td>1 June 2020</td><td>3/1/20 – 2/28/21</td><td>1.8%</td><td>Skipped — banked</td>{cell("SF_571")}</tr>
      <tr><td>1 June 2021</td><td>3/1/21 – 2/28/22</td><td>0.7%</td><td>Skipped — banked</td>{cell("SF_571")}</tr>
      <tr><td>1 June 2022</td><td>3/1/22 – 2/28/23</td><td>2.3%</td><td>Skipped — banked</td>{cell("SF_571")}</tr>
      <tr><td>1 June 2023</td><td>3/1/23 – 2/29/24</td><td>3.6%</td><td>Skipped — banked</td>{cell("SF_571")}</tr>
      <tr><td>1 June 2024</td><td>3/1/24 – 2/28/25</td><td>1.7%</td><td>Skipped — banked</td>{cell("SF_571")}</tr>
      <tr><td>1 June 2025</td><td>3/1/25 – 2/28/26</td><td>1.4%</td><td>Skipped — banked: it became available 1 June 2025, so a full 12 months elapsed on 1 June 2026 — 20 months before a 1 Feb 2027 effective date</td>{cell("SF_571", "SF_BANK", "SF_LI")}</tr>
      <tr><td>Total banked to 1 June 2025 (six anniversaries)</td><td>—</td><td><b>11.5%</b></td><td>Added, not compounded; bankable for a Feb 2027 increase</td>{cell("SF_BANK")}</tr>
      <tr><td>Annual on the effective date (Feb 2027) — or 7th banked year by 1 June 2027</td><td>3/1/26 – 2/28/27</td><td>1.6%</td><td>Current annual through 28 Feb 2027; becomes a 7th banked year (13.1% banked balance) once 12 months elapse on 1 June 2027</td>{cell("SF_571", "SF_BANK")}</tr>
      <tr><td><b>Combined for an effective date on or before 28 Feb 2027</b></td><td>—</td><td><b>13.1%</b></td><td>Requires 90 days' notice; also equals the 7-year banked balance on 1 June 2027, assuming no prior increase</td>{cell("SF_BANK", "SF_571")}</tr>
      <tr><td>Annual percentage for 1 Mar 2027 – 29 Feb 2028 (e.g. 1 June 2027 anniversary)</td><td>3/1/27 – 2/29/28</td><td><b>Blank — not yet published</b></td><td>On 1 June 2027 the 7-year banked balance is 13.1% ($412.65) plus whatever 2027–28 rate the Rent Board publishes (for 1 Mar – 31 May 2027 off-anniversary dates only 11.5% is banked plus the 2027–28 rate)</td>{cell("SF_LI", "SF_BANK")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>Unit B — lawful options (calculated on $3,150)</h2>
  <table>
    <thead><tr><th>Option</th><th>Percentage</th><th>Dollar increase</th><th>New rent</th><th>Notice</th><th>Notes</th><th style="width:18%">Source</th></tr></thead>
    <tbody>
      <tr><td>Annual only (through 28 Feb 2027)</td><td>1.6%</td><td>$50.40</td><td><b>$3,200.40</b></td><td>30 days</td><td>Annual-only illustration, not a minimum; a smaller increase may be chosen. An increase resets the anniversary to its effective date.</td>{cell("SF_571")}</tr>
      <tr><td><b>Phased 10.0%</b></td><td>10.0%</td><td>$315.00</td><td><b>$3,465.00</b></td><td>30 days</td><td>Illustrative, not an official normal rate. Verify the ledger and any capital-improvement increases; the proposal may change. Properly banked unused amounts may remain available.</td>{cell("SF_BANK", "LEGISTAR_261020")}</tr>
      <tr><td>Banked only (2020–2025)</td><td>11.5%</td><td>$362.25</td><td><b>$3,512.25</b></td><td>90 days</td><td>Six skipped anniversaries through 2025; leaves the 1.6% rate unused. <b>Rule § 4.12(a)</b> says a banked amount “may only be given at the time of an annual increase”, while the Rent Board's banking page allows it at another permitted time — see FR-28 before serving a banked-only increase.</td>{cell("SF_BANK")}</tr>
      <tr><td>Maximum for an effective date on or before 28 Feb 2027 <b>(conditional)</b></td><td>13.1%</td><td>$412.65</td><td><b>$3,562.65</b></td><td>90 days</td><td>Conditional on no increase since 1 June 2019: 11.5% banked + the 1.6% annual in force through 28 Feb 2027. The 11.5% banked portion alone exceeds the proposed 10% combined banked-and-capital limit; the annual component is distinct. Check final law.</td>{cell("SF_BANK", "SF_571", "LEGISTAR_261020")}</tr>
      <tr><td>1 June 2027 anniversary maximum</td><td colspan="3"><b>Blank — 13.1% ($412.65) 7-year banked floor plus the unannounced 2027–28 annual percentage.</b></td><td>90 days if &gt;10%</td><td>By 1 June 2027 all seven skipped years 2020–2026 (13.1%) are banked; wait for the 3/1/27 – 2/29/28 rate announcement before computing the June 2027 total (FR-05, FR-17).</td>{cell("SF_LI", "SF_BANK")}</tr>
      <tr><td>Comparable-rent (special circumstances) petition</td><td colspan="3"><b>Blank — no percentage can be stated until the Rent Board decides a petition.</b></td><td>After petition filed</td><td>The Rent Board states that a long-standing tenant paying less than market is <i>not</i> by itself an extraordinary circumstance.</td>{cell("SF_SPECIAL")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>Side-by-side effect (calculated)</h2>
  <table>
    <thead><tr><th>Unit</th><th>Assumed base rent</th><th>Option</th><th>New rent</th><th>Extra per month</th><th>Extra per year</th><th style="width:18%">Basis</th></tr></thead>
    <tbody>
      <tr><td>Unit A</td><td>$3,995.00</td><td>3.0%</td><td>$4,114.85</td><td>$119.85</td><td>$1,438.20</td>{cell("SF_571")}</tr>
      <tr><td>Unit A</td><td>$3,995.00</td><td>1.6%</td><td>$4,058.92</td><td>$63.92</td><td>$767.04</td>{cell("SF_571")}</tr>
      <tr><td>Unit B</td><td>$3,150.00</td><td>10.0%</td><td>$3,465.00</td><td>$315.00</td><td>$3,780.00</td>{cell("SF_BANK")}</tr>
      <tr><td>Unit B</td><td>$3,150.00</td><td>13.1%</td><td>$3,562.65</td><td>$412.65</td><td>$4,951.80</td>{cell("SF_BANK")}</tr>
    </tbody>
  </table>
  <p class="small">Annual figures are 12 × the monthly increase — arithmetic only, before any vacancy, non-payment or passthrough effects.</p>
</div>

<div class="card warn">
  <h2>What must be confirmed before any notice is served</h2>
  <table>
    <thead><tr><th style="width:34%">Item</th><th>Why it changes the answer</th><th style="width:20%">Source</th></tr></thead>
    <tbody>
      <tr><td>Unit B rent history 2019–2026</td><td>A prior increase requires recalculation; partial unused increases may be bankable.</td>{cell("SF_BANK")}</tr>
      <tr><td>Licence in force on the effective date</td><td>Without it the notice is not enforceable, whatever the percentage; the Board's noncompliance page says such a notice may be “null and void” and the tenant may be owed a refund.</td>{cell("SF_HI", "SF_NONCOMP")}</tr>
      <tr><td>Unit A anniversary: 1 Feb or 1 Apr</td><td>Moves the earliest lawful date and the banked amount.</td>{cell("SF_LI")}</tr>
      <tr><td>2027–28 percentage</td><td>Not announced; cannot be used for an effective date on or after 1 March 2027.</td>{cell("SF_LI", "SF_571")}</tr>
      <tr><td>Voucher / subsidy status of either unit</td><td>Subsidised units are partially exempt from the Rent Ordinance; a housing authority may also review reasonableness (24 CFR § 982.507 — rent to owner: reasonable rent). Whether either unit has a housing assistance payment contract is <b>unknown</b> (FR-13); that federal citation was corrected on 11 Nov 2026 (FR-28).</td>{cell("SF_LAWS", "CFR_982")}</tr>
    </tbody>
  </table>
</div>
"""
    return page("pages/units.html", "Units &amp; maths", body,
                "Unit-by-unit calculations: banked percentages, dollar amounts, notice periods and the facts still to be confirmed.")
