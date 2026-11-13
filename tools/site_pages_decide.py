"""Decision-support pages: what must be answered before choosing (open questions) and
how this site could be improved (suggestions, deliberately NOT implemented).

Every table row on both pages carries at least one link to an official source, exactly as the
canonical pages do. Rows whose fact is an owner record say so and leave the answer blank rather
than estimating it, because the site's rule is: never infer a value, flag it instead.
"""
from site_layout import SRC, src, srcs, cell, page

# ---------------------------------------------------------------- open questions

# Question already answered from official sources -> answer -> sources
SETTLED = [
    ("Is the duty to inform the Rent Board and hold a licence a state or a local law?",
     "<b>Local.</b> Created by San Francisco Ordinance No. 265-20 (adopted 2020, effective 18 January 2021), which amended the City's Rent Ordinance; reporting reached condominiums and buildings with fewer than 10 units on <b>1 March 2023</b>. No California statute creates it.",
     ("SF_ORD265", "SF_HI")),
    ("Does being an individual owner rather than a corporation change the duty?",
     "<b>No.</b> The rule is written by owner category, not entity form: “All owners of residential property are required to report … Most owners are required to do this even if you are not a landlord.”",
     ("SF_HI",)),
    ("Is there a separate licence application, hearing or fee?",
     "<b>No.</b> The licence is generated automatically for non-owner-occupied units once the report is filed; reporting is free, and the licence “does not need to be included with your rent increase notice”.",
     ("SF_HI",)),
    ("Does an ordinary annual or banked increase need Rent Board approval?",
     "<b>No petition is required.</b> Approval petitions exist for other increase types — capital improvements, rehabilitation, hardship, comparable rents — not for the annual or banked amount.",
     ("SF_LANDPET", "SF_BANK")),
    ("What is the maximum percentage right now?",
     "<b>1.6%</b> for an increase effective 1 March 2026 – 28 February 2027 (60% of Bay Area CPI). Prior year 1.4%; the full 1982–2027 table is published as document 571.",
     ("SF_LI", "SF_571")),
    ("Does the state cap give me more room?",
     "<b>No.</b> California allows 5% + CPI up to 10% (8.8% for the San Francisco area for increases starting 1 August 2026), but Civil Code § 1947.12(d)(3) excludes housing already restricted by a local ordinance to a lower amount, and the Attorney General's table says the local rule then applies.",
     ("OAG", "LEG_1947")),
    ("What must the notice say, and how far ahead?",
     "Written notice, 30 days if the increase is 10% or less of the rent charged in the prior 12 months (alone or combined), 90 days if more; +5 calendar days if mailed within California. The Rent Board's elements are the dollar amount, the percentage, the effective date and which part is banked.",
     ("LEG_827", "LEG_1013", "SF_LI")),
    ("Must I state a reason?",
     "<b>Not for an annual or banked increase.</b> The published notice elements do not include a justification, and no petition is filed. The prohibition runs the other way: the increase may not be retaliatory, may not turn on a protected characteristic, and may not be charged merely because an occupant moved in.",
     ("SF_LI", "LEG_1942", "LEG_12955")),
    ("May I raise one unit and not the other?",
     "<b>Nothing in the ordinance or fair-housing law requires uniform increases</b> (published as an absence of authority, FR-12). What is prohibited is different treatment <i>because of</i> a protected characteristic; the Rent Board does not hear discrimination claims — the Civil Rights Department and HUD do.",
     ("LEG_12955", "USC_3604", "SF_TENPET")),
    ("Is there a published “normal” or ZIP-level increase for this area?",
     "<b>No.</b> The Rent Board publishes one citywide maximum and no average, typical or ZIP-level figure; those cells stay blank on this site (FR-08, FR-09, FR-10).",
     ("SF_571", "SF_LI")),
    ("What can a tenant do if they object?",
     "Before the increase takes effect, a <b>Tenant Summary Petition</b> (Form 518) — for example where no licence is on record; after it takes effect, a <b>Tenant Petition</b> (Form 516C, box C) for an unlawful rent increase, which has no filing deadline and is heard by an Administrative Law Judge without a lawyer.",
     ("SF_NONCOMP", "SF_UNLAWFUL", "SF_TENPET")),
    ("Is there a law changing these rules in the near future?",
     "<b>Pending, not law.</b> File No. 261020 would cap banked plus capital-improvement increases at 10% per year for three years; status on 13 November 2026 is <b>Pending Committee Action</b>, last recorded action 7 October 2026. The Rent Board's 9 November 2026 notice says it would reach banked increases noticed on or after 15 September 2026 if enacted as proposed.",
     ("LEGISTAR_261020", "SF_LI")),
]

# (id, question, why it blocks, what we have, what is missing, how the answer is obtained, keys)
BLOCKING = [
    ("Q1", "Are these two units actually under the Rent Ordinance?",
     "Everything else assumes it. If a unit is exempt, the ceiling, the banking arithmetic and the licence question all change — and a wrongly assumed exemption is itself a tenant claim.",
     "Owner statement: a 1940 building with two rental units. Rent control applies to units with a certificate of occupancy on or before 13 June 1979, excluding single-family dwellings and most condominiums.",
     "The City property record: certificate-of-occupancy date, legal unit count, whether either unit is a condominium or separately alienable, and whether any conversion was permitted.",
     "Pull the assessor/building record and ask a Rent Board counsellor to confirm coverage; the answer is documentary, not arguable.",
     ("SF_LAWS", "SF_COUNSEL")),
    ("Q2", "Is a rent-increase licence in effect for each unit on the intended effective date?",
     "Without it the notice “will not be enforceable”, and the Board's noncompliance page says such an increase “may be null and void (this may apply for multiple years)” with a possible rent refund.",
     "Nothing on file with this project. No filing history was supplied.",
     "The Housing Inventory submission for the current year and the licence record for each unit, checked on the effective date.",
     "Search the address or parcel number in the Rent Board Portal and keep a dated screenshot; file the report first if no record exists.",
     ("SF_HI", "SF_PORTAL")),
    ("Q3", "What is Unit B's complete increase history since 1 June 2019, and its current base rent?",
     "The 11.5% banked and 13.1% combined figures exist only if no increase was ever imposed. One increase in any year changes the banked balance, the base rent to multiply, and the anniversary date.",
     "A 1 June 2019 lease start and a $3,150 starting rent, plus the owner's statement that the unit is rent controlled.",
     "Every signed notice, proof of service and ledger entry from 2019 to 2026, and the rent actually charged today.",
     "Owner records; if incomplete, the Rent Board's rent-history review (Request to Review Your Rent History) produces the officially recorded lawful rent.",
     ("SF_BANK", "SF_UNLAWFUL")),
    ("Q4", "Which date is Unit A's anniversary — 1 February 2027 or 1 April 2027 — and is a fixed term running on that date?",
     "It sets the earliest lawful effective date, the percentage available, and whether 1.4% can be banked at all. A renewal that added an occupant on 1 April 2026 at the same rent is not addressed by the published rules.",
     "Lease start 1 February 2025; continuation 1 April 2026 at $3,995. The rule: the first annual increase may be imposed 12 months after the date the tenant's lease began, and the effective date then becomes the new anniversary.",
     "A counsellor's or ALJ-level answer on whether the 2026 renewal reset the clock, plus the signed renewal's term dates.",
     "Rent Board counselling line, in writing if possible; keep the answer with the file. This is FR-02 on the flagged page.",
     ("SF_LI", "LEG_827")),
    ("Q5", "Is there an open habitability or code notice for either unit?",
     "California bars a rent-increase notice while substandard conditions that an official has flagged in writing have stood unabated for more than 35 days without good cause; violating it exposes actual damages, $100–$5,000 in special damages and attorney's fees.",
     "Nothing supplied either way.",
     "Any Notice of Violation or inspection record for the building, plus proof of abatement and its date.",
     "Check the department records and the tenant correspondence file before the notice is drafted, not after.",
     ("LEG_19424",)),
    ("Q6", "Does either household receive a rent subsidy (Housing Choice Voucher or a regulated program)?",
     "Subsidy can change who reviews the amount — a housing authority applies its own rent-reasonableness standard — and can change the unit's exemption analysis and the Rent Board Fee position.",
     "Nothing supplied.",
     "Whether a housing assistance payments contract exists for either unit, and the current contract rent.",
     "Owner's own paperwork plus the housing authority; the federal rule for the payment standard is published in 24 CFR § 982.507.",
     ("CFR_982", "SF_LAWS")),
    ("Q7", "Is the Rent Board Fee paid and current for both units?",
     "It is a separate obligation from the licence, and unpaid fees escalate (5% per month to a 15% cap) and can be referred as delinquent. Paying it does not create a licence, and the licence does not pay it.",
     "No filing or payment record supplied. The 2026–27 fee is $59.00 per dwelling unit, due 1 March; the exemption request window for the 2027 fee closes 14 December 2026.",
     "The portal account's fee status for both units for 2026–27 and 2027–28.",
     "Rent Board Portal; the fee page also lists the recoverable half ($29.50) for tenants in occupancy as of 1 November.",
     ("SF_FEE", "SF_HI")),
    ("Q8", "Is there any protected-characteristic or retaliation exposure between the two households?",
     "These are the two grounds on which a tenant-side review actually attacks an increase, and neither can be answered from the numbers.",
     "Nothing but the absence of information. No complaint history, no correspondence, no dates of repair requests.",
     "A dated timeline for each unit: complaints, repair requests, code notices, lease-renewal talks, and the dates of any increase notice, for both units.",
     "Owner records assembled into one timeline per unit, then reviewed by counsel before service.",
     ("LEG_1942", "LEG_12955")),
]

# (id, question, what it changes, what we have, what is missing, keys)
MATERIAL = [
    ("M1", "Which lawful option to take for each unit: annual only, or annual plus banked?",
     "Unit A: $63.92 (1.6%) versus $119.85 (3.0%) per month; Unit B: any figure depends on Q3. Choosing the smaller amount now keeps the remainder banked, and banked amounts do not expire during the tenancy.",
     "Both computations, with the official percentages, on the units page.",
     "The owner's objective — cash flow now versus headroom later — and the rent-history answer from Q3.",
     ("SF_BANK", "SF_571")),
    ("M2", "Raise both units or only one?",
     "Not a legal requirement either way; it is a risk and narrative question. A written, unit-specific reason for each amount is the control that a reviewer can test.",
     "The analysis of selective increases, including that no official source requires uniform treatment.",
     "The per-unit rationale, in writing, before the notices are served.",
     ("LEG_12955", "USC_3604")),
    ("M3", "Which effective date, knowing it becomes the new anniversary date?",
     "An increase effective later than the anniversary makes that later date the anniversary, which can cost a whole year of allowance; a date after 28 February 2027 also depends on a percentage the Rent Board has not yet published.",
     "Both calendars and the blank for the 2027–28 rate.",
     "A chosen date, recorded before the notice is drafted.",
     ("SF_LI", "SF_571")),
    ("M4", "How will the notice be served, and what proof will exist?",
     "Personal delivery, or mail with the statutory extension. Proof of service is a check a tenant-side reviewer runs early, and its absence is difficult to repair later.",
     "The service rules and the model wording.",
     "A method, a date and a document (certificate of mailing or signed receipt).",
     ("LEG_1013", "LEG_827")),
    ("M5", "How should the change be explained to the households?",
     "No official element requires an explanation, but the notice must be accurate and complete; the Rent Board's list is amount, percentage, effective date and the banked part. Tone and advance warning are business choices, not legal ones.",
     "A model notice that states each element.",
     "A plain-language cover note, if wanted, reviewed so it cannot be read as a threat or a inducement.",
     ("SF_LI", "LEG_827")),
    ("M6", "Does the pending 10% cap change the plan?",
     "If enacted as proposed it would reach banked increases noticed on or after 15 September 2026, which is before any notice contemplated here; the Unit B 13.1% total contains 11.5% banked.",
     "The bill text status, re-checked 13 November 2026: still in committee.",
     "A same-day status check immediately before serving any banked notice.",
     ("LEGISTAR_261020", "SF_BANK")),
    ("M7", "Is the annual security-deposit interest duty current for both units?",
     "Separate from any increase and not funded by it — but an unmet habitability or statutory duty invites scrutiny of everything else. The rate for 1 March 2026 – 28 February 2027 is 4.2%.",
     "The published rate and the prior years.",
     "Payment or credit records for each tenancy year.",
     ("SF_RATES",)),
]

# (id, question, when to close it, keys)
CONFIRM = [
    ("C1", "Licence screenshot dated within days before service, for both units.",
     "Immediately before serving; re-check on the effective date itself.", ("SF_HI",)),
    ("C2", "Percentage confirmed as the one in force on the effective date, not the notice date.",
     "At drafting, and again if the date moves across 1 March.", ("SF_LI", "SF_571")),
    ("C3", "Banked amounts listed with the year and percentage of each skipped increase.",
     "In the notice itself, plus in the file.", ("SF_BANK", "SF_RULE4")),
    ("C4", "No rounding up of the dollar amount.",
     "At calculation — the cent is kept.", ("SF_LI",)),
    ("C5", "Owner or manager business contact on file is current (updates due within 30 days of a change).",
     "Whenever contact details change.", ("SF_HI",)),
    ("C6", "Housing Inventory re-filed by 1 March of the following year.",
     "Diarise now; a lapse suspends the licence for the period of non-compliance.", ("SF_HI", "SF_ORD265")),
    ("C7", "If a petition follows, respond with the complete file rather than a new calculation.",
     "Within the period the Board's letter sets.", ("SF_UNLAWFUL", "SF_TENPET")),
]

# (what is missing, how to obtain it, what you will hold afterwards, keys)
DISCOVERY = [
    ("Licence status per unit, per year",
     "Rent Board Portal → search address or assessor parcel number → open the Rent Increase License record; previous years are visible there too.",
     "A dated screenshot per unit showing the licence in effect on the intended effective date.",
     ("SF_PORTAL", "SF_HI")),
    ("Officially recorded rent history for a unit",
     "The Rent Board's combined service for reporting an unlawful increase or requesting a review of rent history; a tenant can initiate it, and the Board's record of the lawful rent follows.",
     "An administrative determination of the lawful rent, which replaces guesswork about prior increases.",
     ("SF_UNLAWFUL", "SF_TENPET")),
    ("Certificate of occupancy, legal unit count, unit type",
     "City property record (the Housing Inventory page itself points to the assessor's property information map for square footage and building facts).",
     "Documentary coverage evidence, which also answers whether the unit is a condominium or separately alienable.",
     ("SF_HI", "SF_LAWS")),
    ("Whether the 2026 renewal reset Unit A's anniversary",
     "Rent Board counselling line 415-252-4600, Monday to Friday 9–12 and 1–4, or drop-in 9–4; put the question in writing and keep the reply.",
     "A named, dated answer to place beside the lease and the renewal.",
     ("SF_COUNSEL", "SF_NONCOMP")),
    ("Open code or health notices for the building",
     "Department records and the tenant correspondence file; the statutory bar turns on a written notice from a housing official and its date.",
     "Either a clean record or an abatement plan with dates before any increase notice.",
     ("LEG_19424",)),
    ("Subsidy or program status",
     "Owner paperwork and the housing authority; the federal payment-standard and rent-reasonableness rules are published in 24 CFR § 982.507.",
     "Confirmation of whether a rent reasonableness review, rather than the local cap, sets the ceiling.",
     ("CFR_982",)),
    ("Whether any law is about to change the caps",
     "Board of Supervisors legislation record for File No. 261020, plus the Rent Board's notices, checked on the day the notice is drafted.",
     "A same-day status note in the file, so a pending bill is never mistaken for law.",
     ("LEGISTAR_261020", "SF_LI")),
    ("The current and prior-year percentages, straight from the source",
     "Rent Board document 571 (full 1982–2027 table) and the Current Rates page, which also carries deposit interest and bankable fee amounts.",
     "The only two numbers any calculation on this site is allowed to rest on.",
     ("SF_571", "SF_RATES")),
    ("An independent read of the draft notice",
     "Counsel, and — on the tenant side — the free legal-aid routes the City and the courts describe; expect the notice to be read for its dates and its arithmetic first.",
     "A mark-up before service rather than an argument after it.",
     ("SF_TENPET", "CRD")),
]

# (item, status, why no number is given, keys)
UNANSWERABLE = [
    ("A “normal” or market increase for this neighbourhood",
     "<b>Blank</b>",
     "The Rent Board publishes a citywide maximum, not an average or typical rate, and no official ZIP-level benchmark was located. Private listing averages are not cited here because they are not authoritative.",
     ("SF_LI", "SF_571")),
    ("How often corporations versus individual owners raise rent, and by how much",
     "<b>Blank</b>",
     "No City, State or federal dataset published to this project reports increase frequency or size by owner type; only evidenced conduct (algorithmic-pricing prohibition, the federal antitrust suit) is described.",
     ("SF_ALGO", "DOJ_ALGO")),
    ("Whether a copy of an ordinary increase notice must be filed with the Rent Board",
     "<b>Blank</b>",
     "The official pages establish that no approval petition is needed and that the licence need not accompany the notice; neither statement settles a separate filing duty. Published as FR-20 rather than inferred.",
     ("SF_HI", "SF_BANK")),
    ("Whether the City expects a business registration number for a two-unit rental",
     "<b>Blank — flagged FR-33</b>",
     "The Housing Inventory asks for “the business registration number for the unit, <i>if any</i>”, which neither requires nor excuses one for this case. Ask the Rent Board rather than assume.",
     ("SF_HI",)),
    ("Whether any specific increase would be “approved” in advance",
     "<b>No such process</b>",
     "For annual and banked increases the Rent Board does not pre-approve; enforceability is tested later, by petition, on the record you kept.",
     ("SF_BANK", "SF_UNLAWFUL")),
]


def open_questions():
    settled_rows = "".join(
        '<tr><td><b>%s</b></td><td>%s</td>%s</tr>' % (q, a, cell(*k))
        for q, a, k in SETTLED
    )
    blocking_rows = "".join(
        '<tr><td class="nowrap"><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'
        '<td>%s</td>%s</tr>' % (i, q, why, have, missing, how, cell(*k))
        for i, q, why, have, missing, how, k in BLOCKING
    )
    material_rows = "".join(
        '<tr><td class="nowrap"><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>%s</tr>'
        % (i, q, changes, have, missing, cell(*k))
        for i, q, changes, have, missing, k in MATERIAL
    )
    confirm_rows = "".join(
        '<tr><td class="nowrap"><b>%s</b></td><td>%s</td><td>%s</td>%s</tr>'
        % (i, q, when, cell(*k)) for i, q, when, k in CONFIRM
    )
    discovery_rows = "".join(
        '<tr><td><b>%s</b></td><td>%s</td><td>%s</td>%s</tr>'
        % (what, how, result, cell(*k)) for what, how, result, k in DISCOVERY
    )
    unanswerable_rows = "".join(
        '<tr><td><b>%s</b></td><td>%s</td><td>%s</td>%s</tr>'
        % (item, status, why, cell(*k)) for item, status, why, k in UNANSWERABLE
    )
    body = f"""
<div class="card">
  <h1>Decision readiness — what must be answered before any amount is chosen</h1>
  <p class="lede">This page is the gate in front of the numbers. It lists what is already settled from official
   sources, the questions that <b>block</b> a reasonable decision, the questions that change the answer but do not
   block it, and how to obtain each missing item. Where no official source publishes a value, the cell is left
   <b>blank</b> and pointed at the flagged page instead of being estimated.</p>
  <div class="grid">
    <div class="stat"><div class="num">{len(SETTLED)}</div><div class="lbl">questions already answered from official sources</div></div>
    <div class="stat"><div class="num">{len(BLOCKING)}</div><div class="lbl">blocking questions — a decision is not defensible until each is closed in writing</div></div>
    <div class="stat"><div class="num">{len(MATERIAL)}</div><div class="lbl">material questions — they change the amount, the date or the story</div></div>
    <div class="stat"><div class="num">{len(CONFIRM)}</div><div class="lbl">confirmations to complete at service time</div></div>
    <div class="stat"><div class="num">0 / {len(BLOCKING)}</div><div class="lbl">blocking questions closed by the material supplied so far</div></div>
    <div class="stat"><div class="num">{len(UNANSWERABLE)}</div><div class="lbl">questions no official source answers — left blank on purpose</div></div>
  </div>
</div>

<div class="card alert">
  <h2>The rule this page enforces</h2>
  <p><b>Not ready to decide.</b> Every question in section 2 turns on a record that sits outside this project —
   the City property record, the Rent Board Portal, the leases and ledger for Unit B, the code-notice file, the
   subsidy file, the fee account and the complaint timeline — except Q4, which needs the Rent Board's own reading
   of a mid-tenancy renewal. Choosing a percentage before those are in hand means choosing on assumptions, and the
   assumptions are the first things a tenant-side reviewer tests. The two that most often invalidate an otherwise
   correct calculation are the licence (Q2) and the rent history (Q3).</p>
</div>

<div class="card">
  <h2>1. Already settled — answers you do not need to re-research</h2>
  <table>
    <thead><tr><th style="width:26%">Question</th><th>Answer, as the official sources state it</th><th style="width:20%">Source</th></tr></thead>
    <tbody>{settled_rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>2. Blocking questions — close each one in writing before choosing</h2>
  <p class="small">“Blocking” means the answer can change whether an increase is enforceable at all, not merely
   how large it is. The answer column is left blank deliberately: these are owner-record questions, and this
   site does not fill them in.</p>
  <table>
    <thead><tr><th style="width:4%">ID</th><th style="width:17%">Question</th><th>Why it blocks</th><th>What we already have</th><th>What is missing</th><th style="width:16%">How the answer is obtained</th><th style="width:13%">Source</th></tr></thead>
    <tbody>{blocking_rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>3. Material questions — they change the amount, the date or the explanation</h2>
  <table>
    <thead><tr><th style="width:5%">ID</th><th style="width:21%">Question</th><th>What it changes</th><th>What we have</th><th>What is missing</th><th style="width:16%">Source</th></tr></thead>
    <tbody>{material_rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>4. Confirmations to complete at service time</h2>
  <table>
    <thead><tr><th style="width:5%">ID</th><th>Confirmation</th><th style="width:28%">When to close it</th><th style="width:18%">Source</th></tr></thead>
    <tbody>{confirm_rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>5. How to discover each missing item</h2>
  <table>
    <thead><tr><th style="width:20%">Missing</th><th>How to obtain it</th><th>What you will hold afterwards</th><th style="width:18%">Official source</th></tr></thead>
    <tbody>{discovery_rows}</tbody>
  </table>
</div>

<div class="card warn">
  <h2>6. Questions no official source can answer — published, not estimated</h2>
  <table>
    <thead><tr><th style="width:24%">Item</th><th style="width:12%">Status</th><th>Why no number is given</th><th style="width:16%">Source</th></tr></thead>
    <tbody>{unanswerable_rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>Suggested order of work</h2>
  <ol class="steps">
    <li><b>Documents first, numbers second.</b> Pull the two leases, the renewal, every notice and the ledger for Unit B; download the assessor record; screenshot the Portal.</li>
    <li><b>Close Q1 and Q2</b> (coverage, licence). Until both are yes, no notice should be drafted.</li>
    <li><b>Close Q3 and Q4</b> (rent history, anniversary). These two decide the percentage and the date together.</li>
    <li><b>Clear Q5–Q8</b> (habitability notices, subsidy, fee status, complaint and contact timeline). Each is a documented yes/no.</li>
    <li><b>Then pick</b> from the lawful options on the units page, and write one sentence of reason per unit for the file.</li>
    <li><b>Then serve</b>, following the notice page and the planner on the process page, and keep the proof.</li>
  </ol>
  <p class="small">Related pages: <a href="units.html">Units &amp; maths</a> · <a href="process.html">Licence &amp; process</a> · <a href="notice.html">Notice &amp; reasons</a> · <a href="review.html">Tenant-lawyer test</a> · <a href="requirements.html">Requirements checklist</a> · <a href="flagged.html">Flagged for review</a>.</p>
</div>
"""
    return page("pages/open-questions.html", "Decision readiness — questions to answer first", body,
                "Every question that must be answered before a rent increase is chosen: what is settled, what blocks, what is missing, and how to find out.",
                active="pages/open-questions.html")


# ---------------------------------------------------------------- suggestions

EFFORT = "S = one line of generated copy · M = one new section in a generator module · L = new module plus a gate change"

# (id, suggestion, problem it fixes, official rule it touches, effort, risk if adopted, keys)
SUGGESTIONS = [
    ("S-01", "Stamp every data row with the date its source was retrieved, and shade rows older than 30 days.",
     "The site publishes one page-level research-pass date in the footer, so a row verified in an earlier pass reads as though it were checked today. Statuses do move: the File #261020 record gains entries as the committee acts.",
     "Legistar file status and the annual rate page both change on their own calendars.",
     "M", "A date stamp invites a second question — “why is this one older?” — which must then be answered honestly in the build log.",
     ("LEGISTAR_261020", "SF_LI")),
    ("S-02", "Fail the build when a cited official page disagrees with the text it is quoted for (a weekly automated re-fetch comparing quoted passages).",
     "Today the quotes were re-read by hand on 13 November 2026. A passage changed on the source page would not be noticed until the next manual pass.",
     "The rate, banking and licence pages are the ones that move.",
     "L", "A fetch failure would have to be treated as “unverified”, not “wrong”, or the gate becomes noise; the current rate is announced once a year, so most weeks produce no change.",
     ("SF_LI", "SF_BANK")),
    ("S-03", "Add a one-page printable decision sheet (print stylesheet only, no scripts) that shows the chosen option, the notice date, the licence check and the file contents.",
     "The information exists but is spread across the site's pages; the document an owner actually wants beside them while serving a notice does not exist. The canonical stylesheet has no print rules at all.",
     "Notice contents and lead time are what the sheet must reproduce exactly.",
     "M", "A summary page risks drifting from the detailed pages unless it is generated from the same data — which it would be.",
     ("LEG_827", "SF_HI")),
    ("S-04", "Publish machine-readable data for the canonical edition (rates ledger, notice deadlines, source register) generated from the same modules the HTML comes from.",
     "The archived review edition has CSV files; the canonical edition publishes only a partial JSON register, so anyone re-checking arithmetic must read it out of HTML.",
     "Document 571 is the authoritative source the ledger would mirror.",
     "M", "A data file is a second thing to keep true; it must be generated, never hand-edited.",
     ("SF_571",)),
    ("S-05", "Turn the notice-date planner into a full grid: for each unit, every candidate effective date with the personal-delivery and mail deadlines, weekend and holiday handling, and the “passed” marker.",
     "The planner currently shows five rows, one of which is a historical example; the arithmetic exists in the gate but is not shown as an integrated grid.",
     "The 30/90-day rule and the mail extension are what the grid computes.",
     "M", "Dates must never be presented as advice; the “confirm with counsel” caveat has to travel with the grid.",
     ("LEG_827", "LEG_1013")),
    ("S-06", "Add a visible “what changed since the last pass” page built from the session log.",
     "Coordination history lives in a 174-kilobyte internal file that the site does not link, so a returning reader cannot tell what moved since their last visit.",
     "A pending ordinance is exactly the kind of item a changelog would surface.",
     "S", "The changelog must not read as legal advice; entries are “we re-checked X”, never “the law changed so you may Y”.",
     ("LEGISTAR_261020",)),
    ("S-07", "Give each section a stable anchor link, and add a table caption to every table.",
     "Each canonical page carries exactly one element id (the main landmark) and no table has a caption or header scope attributes, so a specific row cannot be cited in correspondence.",
     "Citations matter most where a tenant or reviewer would check a rule, e.g. the notice elements.",
     "M", "Anchors must be regenerated, not hand-typed, or they will drift.",
     ("SF_LI",)),
    ("S-08", "Add a compliance-calendar page for the duties that surround an increase: 1 March Housing Inventory report, 1 March Rent Board Fee, the exemption request window, the rate change on 1 March, deposit-interest anniversaries.",
     "These dates each appear once, in different places, and one of them (the 2027 fee exemption window closing 14 December 2026) is nearer than the increase itself.",
     "The fee page and the current-rates page carry the dates and amounts.",
     "M", "A calendar invites the assumption it is complete; it must state which obligations it does not cover.",
     ("SF_FEE", "SF_RATES")),
    ("S-09", "Add a plain-language “if the tenant objects” flow: summary petition before the effective date, unlawful-increase petition after, what the Board sends you, what to file back.",
     "The consequences of a challenge are stated in rows on three pages, but not as one sequence a first-time owner can follow.",
     "The Board's own noncompliance page sets out both petition routes.",
     "M", "It must stay descriptive: no prediction of outcomes.",
     ("SF_NONCOMP", "SF_UNLAWFUL")),
    ("S-10", "Decide the re-identification trade-off deliberately: the site keeps exact rents and dates as instructed, while the City itself publishes Housing Inventory base rent only in $250 increments.",
     "Unit-level facts (a two-unit pre-1979 building, an exact rent, a lease-start month) are cross-referenceable against public records by anyone who knows the address; the site already withholds the address, ZIP and neighbourhood for that reason.",
     "The Housing Inventory page states that what is submitted is public, and shows the increment convention the City chose.",
     "S", "Rounding the published amounts would conflict with the standing instruction to keep dates and amounts unchanged, so this is a decision to record, not a change to make.",
     ("SF_HI",)),
    ("S-11", "Split the flagged list into “blocks a decision” and “does not block”, with the blocking subset repeated at the top of the units page.",
     "Thirty-plus flags are published in one list and the site says none block publication — true, but a reader cannot see which ones stop a decision.",
     "Banking conditions and the licence are the flags that actually stop work.",
     "M", "Any re-classification must keep every original flag published; nothing may be dropped to shorten the list.",
     ("SF_BANK", "SF_HI")),
    ("S-12", "Add an “ask the Rent Board” card listing the exact questions to put to the counselling line, with a place to log the answer and the date.",
     "Four open items (anniversary reset, notice-copy filing, business-registration expectation, banking timing test) are answerable by one phone call and are currently only described as open.",
     "The counselling line and drop-in hours are published by the Rent Board.",
     "S", "A counsellor's oral answer is not a determination; the card must say so.",
     ("SF_COUNSEL", "SF_NONCOMP")),
    ("S-13", "State the six-month and twelve-month record-keeping rule explicitly: keep the notice, proof, calculation, licence screenshot and the per-unit rationale for at least the period a tenant can petition.",
     "The site tells owners to keep a file but not how long the exposure runs; unlawful-increase petitions have no filing deadline, and the state statute for over-cap recovery has its own limitation period.",
     "The Rent Board's petition page and the state remedies provision set the exposure.",
     "S", "Do not imply a statute of limitations covers every claim; the copy must say the reverse.",
     ("SF_UNLAWFUL", "LEG_1947")),
    ("S-14", "Consolidate the archived editions behind one labelled index page, each carrying its own date and correction notice.",
     "Six generations of the site remain published (docs, dashboard, review, audit, verified, verification) with different numbers and wording; the flagged page already records that archived rows carry exceptions.",
     "Where official texts disagree, this site's convention is to publish both and flag it.",
     "L", "Prior work is deliberately preserved for audit; consolidation must not delete anything, only label it.",
     ("SF_BANK", "SF_LI")),
]

# (path, contains, effort, benefit, risk, keys)
PATHS = [
    ("Path 1 — Evidence hygiene only",
     "S-01, S-04, S-07, S-13. No new legal content; the numbers and wording stay exactly as they are.",
     "S–M each; four changes in two generator modules plus one data file.",
     "Makes the existing claims easier to audit and cite, which is what a reviewer or a lawyer will do first.",
     "Low. Mostly presentation and provenance; the gates already cover the arithmetic.",
     ("SF_571",)),
    ("Path 2 — Decision support first",
     "S-03, S-05, S-09, S-12. Everything a notice actually needs, gathered onto one printable sheet and one flow.",
     "M each; two new generated sections and one print stylesheet.",
     "Shortens the distance between reading the rules and doing the task correctly.",
     "Medium. Summaries must be generated from the same data as the detail pages or they will drift.",
     ("LEG_827", "SF_HI")),
    ("Path 3 — Freshness and maintenance",
     "S-02, S-06, S-08, S-11, S-14. Keeps the site honest as the law and the calendar move.",
     "L for the re-fetch gate; M for the rest.",
     "The pending ordinance and the 1 March cycle mean the content goes stale predictably; this path automates noticing.",
     "Higher. A weekly fetch needs a clear rule for what a failure means, or the build becomes unreliable.",
     ("LEGISTAR_261020", "SF_FEE")),
    ("Path 4 — Privacy hardening",
     "S-10 only, plus a decision recorded either way.",
     "S.",
     "Puts the re-identification question in front of the owner with the City's own convention as the comparator.",
     "Any rounding of published amounts conflicts with the standing instruction, so this path ends in a written decision, not a change.",
     ("SF_HI",)),
]

# (date, change, why, keys)
DONE_THIS_PASS = [
    ("13 Nov 2026", "Named the level of government behind every requirement in the executive summary and on the dashboard, with the ordinance number and its two phase-in dates.",
     "The brief's question — state or local — was answered only implicitly.", ("SF_ORD265", "SF_HI")),
    ("13 Nov 2026", "Added the Civil Code § 1942.4 pre-condition to the notice page, the process steps and the summary findings.",
     "A statutory bar on serving an increase notice while an official's written habitability notice stands unabated had not been listed anywhere on the canonical pages.",
     ("LEG_19424",)),
    ("13 Nov 2026", "Added the distinction between the Rent Board's unit-level licence and an occupational licence, citing the definition of a real estate broker.",
     "The word “licence” in the owner's question covers two different things, and only one of them applies.", ("LEG_BPC10131", "SF_HI")),
    ("13 Nov 2026", "Re-fetched every official source used for the forefront answer and rolled the research-pass date; the Legistar status for File No. 261020 is unchanged as at 13 November 2026.",
     "The pending file could have advanced in the two days since the previous pass.", ("LEGISTAR_261020", "SF_LI")),
]


def suggestions():
    rows = "".join(
        '<tr><td class="nowrap"><b>%s</b></td><td><b>%s</b></td><td>%s</td><td>%s</td>'
        '<td class="nowrap">%s</td><td>%s</td><td><span class="badge warn">Unanswered</span></td>%s</tr>'
        % (i, sug, problem, touches, effort, risk, cell(*k))
        for i, sug, problem, touches, effort, risk, k in SUGGESTIONS
    )
    path_rows = "".join(
        '<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>%s</tr>'
        % (p, contains, effort, benefit, risk, cell(*k))
        for p, contains, effort, benefit, risk, k in PATHS
    )
    done_rows = "".join(
        '<tr><td class="nowrap">%s</td><td>%s</td><td>%s</td>%s</tr>'
        % (d, ch, why, cell(*k)) for d, ch, why, k in DONE_THIS_PASS
    )
    n = len(SUGGESTIONS)
    body = f"""
<div class="card">
  <h1>Site improvement suggestions — for owner review</h1>
  <p class="lede">A dedicated register of proposals for making this site more useful to the decision it exists to
   support. <b>Nothing on this page has been implemented.</b> Each item states the problem in the current site that
   prompted it, the effort, the risk of doing it, and an empty decision column for the owner to mark
   <i>adopt</i>, <i>adopt with change</i> or <i>decline</i>. Implementation waits for that mark.</p>
  <div class="grid">
    <div class="stat"><div class="num">{n}</div><div class="lbl">proposals, all awaiting a decision</div></div>
    <div class="stat"><div class="num">0</div><div class="lbl">proposals implemented on this page</div></div>
    <div class="stat"><div class="num">{len(PATHS)}</div><div class="lbl">bundle paths to choose between</div></div>
    <div class="stat"><div class="num">{len(DONE_THIS_PASS)}</div><div class="lbl">changes already made this pass — corrections, listed below for transparency</div></div>
  </div>
  <p class="small">Effort key: {EFFORT}</p>
</div>

<div class="card alert">
  <h2>How to respond</h2>
  <p>Reply with the IDs and a word — “<i>S-03 adopt, S-10 decline, S-01 adopt with change: 90-day threshold</i>”.
   Anything not marked stays proposed. No suggestion is implemented on the strength of being reasonable;
   the record of what was chosen and by when will sit on this page.</p>
  <p class="small"><b>What will not be proposed or implemented here:</b> client-side scripts (the site is static
   by design and its build gate rejects them), any figure not published by an official source, any change to
   dates or amounts, and any tenant-identifying detail. That is why this page has no search box, no
   calculator and no market-rent estimate — and why the values the official sources do not publish are left
   blank on every other page instead of filled in.</p>
</div>

<div class="card">
  <h2>Register of proposals</h2>
  <table>
    <thead><tr><th style="width:5%">ID</th><th style="width:16%">Suggestion</th><th>Problem it fixes in the current site</th><th>Official rule it touches</th><th style="width:5%">Effort</th><th style="width:15%">Risk if adopted</th><th style="width:10%">Your decision</th><th style="width:11%">Source</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <p class="small">The “official rule it touches” column names the rule any implementation would have to stay
   consistent with, and the final column links the official page for it. Neither is authority for changing the
   site, and no legal conclusion about your increase is drawn from either: a proposal on this page is a plan for
   a document, not advice about a tenancy.</p>
</div>

<div class="card">
  <h2>Bundle paths — pick one, or mix by ID</h2>
  <table>
    <thead><tr><th style="width:20%">Path</th><th>Contains</th><th>Effort in total</th><th>What it buys</th><th>Risk</th><th style="width:15%">Rule to check against</th></tr></thead>
    <tbody>{path_rows}</tbody>
  </table>
</div>

<div class="card ok">
  <h2>Already changed this pass — corrections, not improvements</h2>
  <p class="small">These are recorded here so the boundary is clear: items in the register above are proposals and
   stay unimplemented; the rows below were changes of substance to existing pages because an official source
   contradicted or completed what was there.</p>
  <table>
    <thead><tr><th style="width:9%">Date</th><th style="width:34%">Change</th><th>Why</th><th style="width:18%">Source</th></tr></thead>
    <tbody>{done_rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>Standing constraints any accepted suggestion must respect</h2>
  <ul class="tight">
    <li><b>Generate, never hand-edit.</b> Pages are built from the modules in <code>tools/</code>; the CI job fails if the committed HTML differs from a fresh build.</li>
    <li><b>Every data row keeps an official link</b> or is blank and flagged — this page follows the same rule.</li>
    <li><b>Nothing is deleted.</b> Earlier editions stay online, which is why S-14 is a labelling exercise rather than a cleanup.</li>
    <li><b>Anonymisation is not relaxed</b> for convenience: placeholders stay, and the withheld address, ZIP and neighbourhood stay withheld.</li>
    <li><b>Dates and dollar amounts are not adjusted</b> by a site change; the instruction is explicit and the arithmetic assertions in the build enforce it.</li>
    <li><b>Pending law stays pending</b> — File No. 261020 is described by its Legistar status, never as a rule to plan on.</li>
  </ul>
  <p class="small">Sources for the constraints themselves: {srcs("SF_LI", "LEGISTAR_261020", "SF_HI")} · register and status pages: <a href="sources.html">sources</a>, <a href="flagged.html">flags</a>, <a href="requirements.html">requirements</a>.</p>
</div>
"""
    return page("pages/suggestions.html", "Site improvement suggestions", body,
                "Numbered proposals for improving this site, with effort, risk and an empty decision column; none implemented until the owner chooses a path.",
                active="pages/suggestions.html")
