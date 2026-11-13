"""Decision-support pages: the open-questions register and the suggestions register.

Two things the brief asked for that a research site usually leaves out:

* a single list of every question, the information it needs and the answer already
  available, split by whether the answer can come from an official source at all; and
* a place to park improvement proposals so the owner can pick a path *before* anything
  is implemented.

Rows that appear inside a ``<table>`` carry the official rule they are anchored to,
because the site-wide gate requires one official link per data row.  Suggestions that
are purely about the site's own presentation have no legal anchor, so they are
published as lists and say so.
"""
from site_layout import src, srcs, cell, page

# --------------------------------------------------------------------- questions
# (id, question, why it blocks, status, where the answer comes from, source keys)
BLOCKERS = [
    ("Q-01",
     "Has the Housing Inventory been reported for both units, and is a rent-increase licence in effect on the planned effective date?",
     "Without a licence on the effective date the increase is not enforceable however correct the percentage is; the notice may be null and void and the tenant may be owed a refund.",
     "Owner record — not verifiable from any public page",
     "Rent Board Portal: search the address or Assessor's Parcel Number and open each licence year; keep a dated screenshot for both units.",
     ("SF_HI", "SF_NONCOMP", "SF_PORTAL")),
    ("Q-02",
     "Was Unit B's rent increased at any time since 1 June 2019?",
     "It decides whether the lawful ceiling is 1.6% or a banked total above 10%, which also flips the notice period from 30 to 90 days.",
     "Owner record — published as an open flag (FR-01)",
     "Leases, every rent-increase notice, the rent ledger and cancelled cheques 2019–2026; the Rent Board can also determine the lawful rent on petition.",
     ("SF_BANK", "SF_UNLAWFUL")),
    ("Q-03",
     "Is each tenancy month-to-month, or still inside a fixed-term lease on the intended effective date?",
     "The 30/90-day change-of-terms notice in Civil Code § 827 is the mechanism for a periodic tenancy; inside a fixed term the rent can only change as the lease itself allows.",
     "Owner record — lease document required",
     "The current signed lease or rental agreement, including any renewal or addendum.",
     ("LEG_827",)),
    ("Q-04",
     "What exactly is the base rent for each unit, and does it include housing services such as parking, storage or utilities?",
     "The percentage is applied to base rent only; passthroughs and fluctuating charges are excluded, and the increase may not be rounded up to the next dollar.",
     "Owner record — one figure required",
     "The rent stated in the current agreement less any separately identified charges.",
     ("SF_LI",)),
    ("Q-05",
     "Does the building's record show residential units that pre-date 13 June 1979, and is the unit a single-family dwelling?",
     "Coverage is the premise of every other figure on this site. A 1940 building is generally covered, but the owner's statement has not been checked against a City record.",
     "City record — not yet retrieved",
     "The City's own instruction is to look up the building on the Property Information Map linked from the rental-laws page; the assessor record also gives the unit count.",
     ("SF_LAWS",)),
    ("Q-06",
     "Are the units separately alienable (condominium or co-op) and is the owner an individual rather than a corporation, REIT, LLC or partnership?",
     "That combination can exempt a unit from the state rent cap — but the exemption is conditional on giving the tenant the statute's written notice — and separately alienable units are also outside the City ordinance only in defined circumstances.",
     "City record plus title document",
     "The deed or condominium map, the current lease (to check whether the statutory exemption sentence was ever given), plus a Rent Board counsellor or a determination on petition if the answer is unclear.",
     ("LEG_1947", "SF_LAWS", "SF_LANDPET")),
    ("Q-07",
     "What is each unit's anniversary date — the date the last increase actually took effect?",
     "It fixes the earliest lawful effective date and which year's percentage applies; getting it wrong loses a banked increase or voids the notice.",
     "Owner record, then counsellor confirmation (FR-02)",
     "Date of the last effective increase; for Unit A the choice between 1 February and 1 April 2027 should be confirmed in writing.",
     ("SF_LI",)),
    ("Q-08",
     "Has either household complained, requested repairs, asserted a habitability problem, or organised in the last year?",
     "An increase following protected conduct invites a retaliation claim; the Rent Board does not hear retaliation, so the exposure lands in court.",
     "Owner record — communications file required",
     "Every written request, work order and reply since the last increase, with dates.",
     ("LEG_1942", "SF_TENPET")),
    ("Q-09",
     "In Unit A, is the occupant who joined in 2026 a co-tenant or a subtenant, and was a written Section 6.14 notice served within about 60 days of the change?",
     "It decides whether any future market-rate increase is available at all when an original occupant leaves, and it is also why no extra rent could be charged for the new occupant.",
     "Owner record plus legal analysis (FR-21)",
     "The 2026 agreement, rent-acceptance conduct, and any Section 6.14 notice; a Section 6.14 determination may be requested from the Rent Board.",
     ("SF_614", "SF_LANDPET")),
    ("Q-10",
     "Does either household hold a Housing Choice Voucher or another rent subsidy?",
     "A subsidy adds a rent-reasonableness determination by the housing authority, different treatment of increases over 10%, and a Rent Board Fee exemption route.",
     "Owner record — lease file and housing authority",
     "The voucher tenancy addendum and the housing authority's most recent rent determination.",
     ("CFR_982", "ADMIN_373", "SF_FEE")),
    ("Q-11",
     "Is the annual Rent Board Fee paid and current for both units, and were owner contact details kept updated?",
     "A separate duty from the licence: $59.00 per dwelling unit for 2026–27 due 1 March, with 5% monthly penalties capped at 15%; contact changes must be updated within 30 days.",
     "Owner record — portal account",
     "Payment confirmations in the Rent Board Portal and the current owner/manager contact entry.",
     ("SF_FEE", "SF_HI")),
    ("Q-12",
     "Are you also planning a passthrough (capital improvement, utility, or operating and maintenance expense)?",
     "Those six categories require a petition filed with the Rent Board *before* the notice is served, and the tenant does not have to pay until it is approved — a different track from the annual increase.",
     "Owner decision, then petition",
     "Rent Board landlord petitions; filing is free.",
     ("SF_LANDPET",)),
    ("Q-13",
     "Does the draft notice state the dollar amount, the percentage, the effective date and which part is banked — and does it use the percentage in force on the effective date?",
     "The Rent Board lists those as the contents of a compliant notice; the breakdown of annual versus banked amounts and the dates behind them are set by rule.",
     "Drafting step — checkable now",
     "Compare the draft against the published notice contents before serving.",
     ("SF_LI", "SF_BANK")),
    ("Q-14",
     "Has File #261020 moved since 13 November 2026, and would it apply to a notice served now?",
     "If enacted as proposed it would cap combined banked and capital-improvement increases at 10% a year for three years, reaching banked notices served on or after 15 September 2026.",
     "Legislative status — re-check before serving",
     "The Bill file page and the notice the Rent Board posts on its rent-increase pages.",
     ("LEGISTAR_261020", "SF_LI")),
]

# (question, answer, confidence, source keys)
ANSWERED = [
    ("Is the duty to inform the Rent Board and hold a licence a state law or a local law?",
     "<b>Local.</b> It is a San Francisco ordinance — Ordinance No. 265-20, effective 18 January 2021, which added the Housing Inventory and the rent-increase licence to the City's Rent Ordinance. No California statute requires a landlord to notify a rent board or hold a licence to raise rent.",
     "Verified", ("SF_ORD265", "SF_HI")),
    ("Then why does everyone quote 2023?",
     "Because that is when it reached small owners: reporting began 1 July 2022 for units in buildings of 10 or more units, and <b>1 March 2023</b> for condominiums and buildings with fewer than 10 units, with updates due every 1 March.",
     "Verified", ("SF_HI", "SF_LI")),
    ("Do I need the licence because I am an individual owner rather than a corporation?",
     "The rule is written by building size, not by the owner's legal form: all owners of residential property must report, and owners with tenants receive a licence after the submission. The state statute, by contrast, does care about legal form for separately alienable units.",
     "Verified", ("SF_HI", "LEG_1947")),
    ("Is there a licence application, a fee, or an approval process?",
     "No separate application for the licence — it is generated automatically once the report is filed, reporting is free, and the licence does not have to be attached to the tenant's notice. Annual and banked increases need no petition.",
     "Verified", ("SF_HI", "SF_571")),
    ("Can I be told I must file the increase notice with the Rent Board?",
     "No official page in the register requires a copy of an ordinary annual or banked increase notice to be filed; the open question is published rather than answered (FR-20). Petition-based increases are a different matter.",
     "Open item", ("SF_HI", "SF_LANDPET")),
    ("What is the maximum increase available right now?",
     "1.6% for an increase taking effect between 1 March 2026 and 28 February 2027, plus any properly banked amounts. The 2027–28 percentage has not been announced.",
     "Verified", ("SF_LI", "SF_571")),
    ("Does state law add anything on top, or require any filing?",
     "No filing and no licence — the state has no rent board. The state cap is 5% plus regional cost-of-living up to 10% (8.8% for the San Francisco area for increases starting 1 August 2026 – 31 July 2027) and the statute expressly does not apply where a local ordinance allows a smaller increase. What the statute does add is a tenant-facing duty for owners who <i>claim</i> an exemption: a separately alienable unit owned by a non-corporate owner is exempt only if the tenant was given the statute's written exemption notice, and a two-unit structure the owner has occupied as a principal residence since the start of the tenancy is exempt outright.",
     "Verified", ("OAG", "LEG_1947")),
    ("How much notice, and how is it served?",
     "30 days where the increase (alone or with another in the prior 12 months) is 10% or less; 90 days where it exceeds 10%; five extra days when served by mail in California.",
     "Verified", ("LEG_827", "LEG_1013")),
    ("What happens if the tenant challenges it?",
     "A tenant may file an unlawful-rent-increase petition (Form 516C with Form C rent history), or a Tenant Summary Petition before the increase takes effect, and there is <b>no time limit</b> for filing the rent-history review. Hearings are before an Administrative Law Judge and no lawyer is required.",
     "Verified", ("SF_UNLAWFUL", "SF_TENPET")),
    ("Must I raise both units, or neither?",
     "No official source requires uniform increases. Fair-housing law prohibits different treatment <i>because of</i> a protected characteristic, and the Rent Board does not adjudicate discrimination at all — those claims go to the California Civil Rights Department or HUD.",
     "Verified", ("LEG_12955", "USC_3604", "SF_TENPET")),
    ("Can I charge more because a new occupant joined Unit A in 2026?",
     "No. Charging additional rent merely because an additional roommate moved in is an unlawful rent increase even if the lease allows it.",
     "Verified", ("SF_LI", "ADMIN_373")),
    ("What counts as a reasonable or normal increase under local, state or federal law?",
     "None of the three publishes a 'normal' figure. The local rule is a ceiling, not a benchmark; no official body publishes an average or typical increase, and none publishes a ZIP-level rate.",
     "No official source", ("SF_LI",)),
]

# (document, what it proves, why it matters here)
DOCUMENTS = [
    ("Signed leases and every renewal for both units",
     "Term type, base rent, who the named tenants are, any lease clause allowing an increase",
     "Determines whether a notice under Civil Code § 827 is even the right instrument, and when a fixed term ends.", "LEG_827"),
    ("Rent ledger 2019–2026 for both units, month by month",
     "The date and amount of every increase actually taken",
     "The whole Unit B banked calculation is conditional on this; without it only the 1.6% annual is safe.", "SF_BANK"),
    ("Every past rent-increase notice, with proof of service",
     "Which percentage was used, whether the annual/banked breakdown was given, and when the tenant received it",
     "Establishes the anniversary dates and whether prior increases were lawful.", "SF_RULE4"),
    ("Cancelled cheques, bank statements or receipts",
     "Independent evidence of the amount actually paid",
     "A tenant's Form C rent history is built from these; expect them to be produced.", "SF_UNLAWFUL"),
    ("Housing Inventory confirmations and licence records for each year 2023–2027",
     "That the report was filed and a licence existed on each effective date",
     "The single most checkable precondition of an enforceable increase.", "SF_HI"),
    ("Banked-increase entitlement from a prior owner, if any",
     "That unused allowances survive a change of ownership",
     "New owners may use banked increases from prior owners — but only if the paper proves them.", "SF_BANK"),
    ("Assessor / Planning record for the building: year built, unit count, legal structure",
     "Coverage, and whether the 1–9 unit reporting track applies",
     "The starting point for every other answer on the site.", "SF_LAWS"),
    ("Owner or title documents showing whether units are separately alienable",
     "Condominium, co-op or tenant-in-ownership status",
     "Drives the state-law exemption for a non-corporate owner.", "LEG_1947"),
    ("Repair requests, habitability notices, tenancy-complaint log",
     "Whether an increase follows protected conduct",
     "Retaliation is decided in court, not at the Rent Board.", "LEG_1942"),
    ("Security-deposit accounting and the annual interest credit",
     "Separate obligations that a tenant-side review will look at alongside any increase",
     "Not part of the increase itself; a defect here invites scrutiny of everything else.", "SF_TENPET"),
]

# (action, what it resolves, official channel)
DISCOVERY = [
    ("Book the free Rent Board counselling line and ask three questions in writing: coverage, anniversary date, and the banked balance for each unit.",
     "Q-02, Q-07, and the Unit A anniversary flag FR-02 — the counsellor is the only party who can read the file, not just the rules.",
     "SF_COUNSEL"),
    ("Search both units on the Rent Board Portal and export or screenshot the licence record for every year.",
     "Q-01 and Q-11; the same search is what a tenant is told to use to check you.",
     "SF_PORTAL"),
    ("Reconstruct each unit's rent history in a one-line-per-year table, leaving unknown years blank instead of estimated.",
     "Q-02 and Q-04; a blank row is reviewable, an estimated row is not.",
     "SF_UNLAWFUL"),
    ("File the Housing Inventory report now if any year is missing, then re-check the licence status after submission.",
     "Q-01; filing after the 1 March deadline is allowed, but it cannot retroactively licence an increase that already took effect.",
     "SF_HI"),
    ("Ask the Rent Board, by petition, to determine the lawful rent for Unit B if the ledger cannot be reconstructed.",
     "Q-02 — a determination converts a contested banked balance into a record; filing is free and needs the complete rent history you do have.",
     "SF_LANDPET"),
    ("Read the four texts that describe banking side by side before choosing a Unit A or Unit B number.",
     "The 24-month page text, the 12-month worked example, Rules § 4.12 and the multi-year page; the divergence is published as FR-03.",
     "SF_MULTI"),
    ("Check the Bill file status again within 48 hours of serving anything above 10%.",
     "Q-14 — proposed law can change mid-process and the Rent Board posts a notice when it does.",
     "LEGISTAR_261020"),
    ("Have a California landlord-tenant lawyer review the drafted notice, the ledger and the licence record before service.",
     "Everything the site cannot verify: actual service, motive, and the tenancy documents.",
     "SF_TENPET"),
]

# (scenario, unit, ceiling, amount, new rent, notice, sources)
SENSITIVITY = [
    ("Anniversary is 1 Feb 2027 and the 1.4% has banked", "Unit A", "1.6% + 1.4% = <b>3.0%</b>",
     "$119.85", "$4,114.85", "30 days (35 if mailed)", ("SF_571", "SF_BANK")),
    ("Banking is disallowed for Unit A, or you prefer the safe figure", "Unit A", "1.6% annual only",
     "$63.92", "$4,058.92", "30 days (35 if mailed)", ("SF_571",)),
    ("No increase since 1 June 2019 is confirmed by the ledger", "Unit B",
     "11.5% banked + 1.6% = <b>13.1%</b> for an effective date on or before 28 Feb 2027",
     "$412.65", "$3,562.65", "90 days (95 if mailed)", ("SF_BANK", "SF_571")),
    ("Ledger shows increases were taken in some years", "Unit B",
     "<b>Blank</b> — recompute from the actual history", "", "", "Depends on the recomputed total",
     ("SF_BANK",)),
    ("Effective date on or after 1 March 2027", "Both",
     "<b>Blank</b> — the 2027–28 percentage is not announced", "", "", "Depends on the percentage in force",
     ("SF_LI",)),
    ("File #261020 passes in its current form before you serve", "Unit B",
     "Banked and capital-improvement increases capped at a combined 10% a year (proposed, not law)",
     "", "", "Re-check before serving", ("LEGISTAR_261020",)),
]

GAPS = [
    ("What is a 'normal' increase for a rent-controlled unit in this part of the city?",
     "The Rent Board publishes one citywide ceiling and no average, median or neighbourhood figure.", "FR-08", "SF_LI"),
    ("What do comparable units actually rent for here?",
     "No official ZIP-level rent benchmark was located in this pass; private listing averages are not treated as authoritative.", "FR-10", "SF_SPECIAL"),
    ("How often do corporate owners versus individual owners raise rent, and by how much?",
     "No City, state or federal dataset reports increase frequency or size by owner type.", "FR-09", "SF_LI"),
    ("Would a tenant lawyer sign off on this increase?",
     "No independent review has been obtained, and none can be simulated here; the 16-point test is a checklist, not an approval.", "FR-22", "SF_UNLAWFUL"),
]

# --------------------------------------------------------------------- suggestions
# (id, suggestion, problem it solves, impact, effort, anchor source keys)
SUGGESTIONS_LAW = [
    ("SG-01",
     "Add an evidence page that records, per unit and per year, the Housing Inventory filing confirmation and the dated licence screenshot — referenced by record ID only, with the images kept off the public site.",
     "The licence is the precondition most often missed, and it is the one fact a tenant can check about you in seconds on the same portal.",
     "High — it is the difference between an enforceable notice and a refund",
     "Low — one page plus an upload routine outside the repository",
     ("SF_HI", "SF_NONCOMP")),
    ("SG-02",
     "Add a rent-history ledger table for each unit, one row per 12-month period, with unknown years left blank and marked as open.",
     "Every Unit B number on this site is conditional on a history nobody has seen; a ledger turns a conditional figure into a verified one.",
     "High — unlocks the banked calculation and the 30-versus-90-day decision",
     "Low — data entry from documents the owner already holds",
     ("SF_BANK", "SF_UNLAWFUL")),
    ("SG-03",
     "Put a 're-check before service' strip on the licence, units and notice pages that names the three things that move: the annual percentage, File #261020, and the licence record.",
     "The Rent Board added the legislative notice to its rent-increase and banking pages on 9 November 2026, two days before this site's previous research pass; it edits those pages without warning, so a figure verified last week can be stale on the day of service.",
     "High — protects against serving on stale law",
     "Low — static text",
     ("SF_LI", "LEGISTAR_261020")),
    ("SG-04",
     "Publish a model notice as plain text (dollar amount, percentage, effective date, which part is banked and the dates behind each banked amount) plus a proof-of-service log.",
     "The Rent Board and the rules specify the contents; owners most often fail on the breakdown and the service date, not on the maths.",
     "Medium–high — a compliant notice is the deliverable",
     "Low",
     ("SF_LI", "SF_BANK", "SF_RULE4", "LEG_827")),
    ("SG-05",
     "Add a one-page 'uniform treatment memo' template: the dated reason each unit's percentage differs, signed before service.",
     "The site already shows that no rule requires equal increases, so the risk lives in the reason and the record — which is exactly what a memo creates.",
     "Medium — it is the evidence a fair-housing review looks for first",
     "Low",
     ("LEG_12955", "USC_3604")),
    ("SG-06",
     "Add a short section for the languages the Rent Board itself uses for the annual-increase notice (Spanish, Chinese, Filipino, Vietnamese) and mirror those versions here.",
     "The City publishes its own rate notice in five languages; a tenant who cannot read the notice is the tenant most likely to petition.",
     "Medium — reduces disputes, not legal exposure per se",
     "Medium — translation of a fixed text",
     ("SF_571",)),
    ("SG-07",
     "Add an annual calendar page: 1 March Housing Inventory report and Rent Board Fee, January rate announcement, 14 December exemption window, plus a reminder to re-verify this site before any notice.",
     "Three of the five duties on this site are annual dated events; two deadlines already sit inside the current cycle.",
     "Medium — prevents a compliance gap that voids an otherwise lawful increase",
     "Low",
     ("SF_HI", "SF_FEE", "SF_LI")),
    ("SG-08",
     "Move the six archived editions behind one 'editions' index page, each labelled with its research date and a pointer to the corrections list.",
     "Readers currently reach superseded pages by search engine; the corrections are only visible if you already know where to look.",
     "Medium — prevents acting on a superseded figure",
     "Medium — touches every edition, so it needs the integration session",
     ("SF_LI", "ADMIN_373")),
    ("SG-09",
     "Publish the machine-readable data behind the tables (rates, flags, sources) as a JSON file in the repository and link it from the sources register.",
     "Every figure already comes from one official table; a data file makes the next re-verification a diff instead of a re-read.",
     "Medium — faster, auditable re-verification",
     "Low–medium",
     ("SF_571",)),
    ("SG-10",
     "Add an automated weekly job that re-fetches the five sources whose content changes (rate page, banking page, inventory page, noncompliance page, Bill file) and opens an issue when the text differs.",
     "The Rent Board edits these pages without notice, and two of the site's corrections came from exactly that.",
     "Medium–high — the site stops going stale silently",
     "Medium — workflow plus a diff check",
     ("SF_LI", "SF_HI", "SF_NONCOMP", "LEGISTAR_261020")),
    ("SG-11",
     "Say plainly on the dashboard that the Housing Inventory submission is public information, and keep the site's own privacy rule (no address, no occupant identifiers) as a stated policy with the reason.",
     "The City warns that reported information is public; owners who learn that afterwards tend to over-correct and stop reporting accurately.",
     "Medium — informed disclosure and consistent anonymisation",
     "Low — one paragraph",
     ("SF_HI",)),
    ("SG-12",
     "Replace the fixed-date notice planner with a small offline calculator (spreadsheet the owner downloads), rather than adding scripts to the published site.",
     "Static example dates go stale the moment they pass, and a stale deadline can be misread as still open.",
     "Medium — the planner stays correct without JavaScript on the public site",
     "Medium",
     ("LEG_827", "LEG_1013")),
]

SUGGESTIONS_UI = [
    "Add a persistent progress meter — “12 of 14 blocking questions answered” — so the owner can see at a glance whether a decision is defensible yet.",
    "Add a search box and per-page table-of-contents, once the site passes ten pages; today the fastest route is the category grid on the dashboard.",
    "Add print styles and a printable one-page brief of the two unit tables, so the numbers can be taken to the counsellor or the lawyer on paper.",
    "Add a glossary of the five terms that decide everything (base rent, anniversary date, banked increase, licence, effective date), each quoted from the page that defines it.",
    "Add a 'what changed on this site' page generated from the commit log, so a reader can see which figure was corrected and when.",
    "Add a last-reviewed date badge to every table, not just the page footer.",
    "Add a decision log where the owner's choices against the suggestion IDs below are recorded verbatim, so nobody implements an unapproved change.",
    "Consider a robots no-index tag while the site stays public; it limits search-engine indexing but cannot make a public repository private, and that trade-off is the owner's to accept.",
]

SUGGESTIONS_REJECT = [
    ("Ask the Rent Board to pre-approve the annual increase.",
     "No petition exists for it; the annual and banked mechanism is self-executing, and an unnecessary petition invites a rent-history review you may not want yet.",
     "SF_571"),
    ("Publish a market-rent comparison for the units' ZIP code from listing websites.",
     "Listing averages are not official data, and unit-level facts tied to a location could identify the households. Nothing in the rule depends on either.",
     "SF_LI"),
    ("Use a rent-setting algorithm or pricing platform to justify the amount.",
     "San Francisco prohibits selling or using specified algorithmic pricing devices to set rents, and the federal antitrust action against six large landlords was about exactly this practice.",
     "SF_ALGO"),
    ("Round the increase up to the next dollar for tidiness.",
     "The Rent Board states rent increases cannot be rounded up; a tidy number is an unlawful one.",
     "SF_LI"),
    ("Add a reason such as 'market adjustment' or 'new occupant' to the notice.",
     "No reason is required for an annual or banked increase, and an increase attributed to a new occupant is expressly unlawful.",
     "SF_LI"),
    ("Delete the superseded editions to tidy the repository.",
     "The build gate refuses to publish if an edition disappears; the audit trail is what makes the corrections checkable.",
     "ADMIN_373"),
]


def questions():
    blockers_rows = "".join(
        '<tr><td class="nowrap"><b>%s</b></td><td>%s</td><td>%s</td>'
        '<td><span class="badge %s">%s</span></td><td>%s</td>%s</tr>'
        % (qid, ask, why,
           "danger" if "Owner record" in status or "not verifiable" in status else "warn",
           status, where, cell(*keys))
        for qid, ask, why, status, where, keys in BLOCKERS
    )
    answered_rows = "".join(
        '<tr><td>%s</td><td>%s</td><td><span class="badge %s">%s</span></td>%s</tr>'
        % (ask, ans, "ok" if conf in ("Verified",) else "warn", conf, cell(*keys))
        for ask, ans, conf, keys in ANSWERED
    )
    docs_rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td>%s</tr>" % (doc, proves, why, cell(key))
        for doc, proves, why, key in DOCUMENTS
    )
    disc_rows = "".join(
        "<tr><td>%s</td><td>%s</td>%s</tr>" % (act, resolves, cell(key))
        for act, resolves, key in DISCOVERY
    )
    sens_rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>%s</tr>"
        % (scen, unit, ceiling, amt, new, notice, cell(*keys))
        for scen, unit, ceiling, amt, new, notice, keys in SENSITIVITY
    )
    gap_rows = "".join(
        '<tr><td>%s</td><td>%s</td><td><span class="badge warn">%s</span></td>%s</tr>'
        % (q, why, flag, cell(key))
        for q, why, flag, key in GAPS
    )
    body = f"""
<div class="card hero">
  <h1>Open questions — what must be answered before a decision is defensible</h1>
  <p class="lede">The brief asked for a clear list of the questions, the information they
  need and the answers available now. This page is that list. {len(BLOCKERS)} questions block
  a decision; {len(ANSWERED)} are answered from official sources; {len(DOCUMENTS)} documents
  have to be collected; {len(DISCOVERY)} actions will find the missing information;
  {len(GAPS)} questions have no official answer and stay blank.</p>
  <p class="small"><b>Status key.</b> <span class="badge danger">Owner record</span> means no
  public page can answer it — it comes out of your files. <span class="badge warn">Open item</span>
  means the official sources do not settle it and it is published on
  <a href="flagged.html">Flagged for review</a>. <span class="badge ok">Verified</span> means the
  answer below was read off the linked official page on the research date.</p>
</div>

<div class="card alert">
  <h2>A. The blocking questions</h2>
  <p>Serve nothing until every row here is either answered or deliberately accepted as an
  open risk. Each row states the consequence of leaving it blank.</p>
  <table>
    <thead><tr><th style="width:6%">ID</th><th style="width:22%">Question</th>
    <th style="width:24%">What it decides</th><th style="width:13%">Status now</th>
    <th style="width:20%">Where the answer comes from</th><th style="width:15%">Official source</th></tr></thead>
    <tbody>{blockers_rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>B. What research has already settled</h2>
  <table>
    <thead><tr><th style="width:30%">Question</th><th>Answer as it stands</th>
    <th style="width:11%">Confidence</th><th style="width:17%">Official source</th></tr></thead>
    <tbody>{answered_rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>C. Documents to collect — nothing on this site substitutes for them</h2>
  <table>
    <thead><tr><th style="width:26%">Document</th><th style="width:26%">What it proves</th>
    <th>Why it matters here</th><th style="width:17%">Rule it is measured against</th></tr></thead>
    <tbody>{docs_rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>D. How to discover the missing information</h2>
  <p>Each action is a route to a fact, not a workaround. Free counselling exists precisely for
  the coverage and anniversary questions.</p>
  <table>
    <thead><tr><th style="width:40%">Action</th><th>What it resolves</th>
    <th style="width:22%">Official channel</th></tr></thead>
    <tbody>{disc_rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>E. Sensitivity — how each answer changes the number</h2>
  <p class="small">Percentages are official; dollar amounts are arithmetic on base rent only.
  A blank is a value that cannot be computed from what is known, not an oversight.</p>
  <table>
    <thead><tr><th style="width:22%">If the answer is</th><th style="width:8%">Unit</th>
    <th style="width:24%">Lawful ceiling</th><th style="width:10%">Monthly increase</th>
    <th style="width:11%">New base rent</th><th style="width:13%">Notice lead time</th>
    <th style="width:12%">Source</th></tr></thead>
    <tbody>{sens_rows}</tbody>
  </table>
</div>

<div class="card warn">
  <h2>F. Questions no official source answers</h2>
  <p>These stay on the site as blanks with a flag rather than being filled with an estimate.</p>
  <table>
    <thead><tr><th style="width:32%">Question</th><th>Why no answer is published</th>
    <th style="width:12%">Flag</th><th style="width:17%">Nearest official page</th></tr></thead>
    <tbody>{gap_rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>G. The do-not-serve gate</h2>
  <ol class="steps">
    <li><b>Licence confirmed</b> for each unit, current on the intended effective date, with a dated record kept. Source: {src("SF_HI", "sf.gov — Housing Inventory")}</li>
    <li><b>Rent history reconstructed</b> for each unit, with unknown years left blank. Source: {src("SF_BANK", "sf.gov — banked increases")}</li>
    <li><b>Coverage confirmed</b> against the building record, not against the owner's recollection. Source: {src("SF_LAWS", "sf.gov — rental laws")}</li>
    <li><b>Notice drafted</b> with the amount, percentage, effective date and banked breakdown, checked against the percentage in force on the effective date. Source: {src("SF_LI", "sf.gov — rent increases")}</li>
    <li><b>Legislative status re-checked</b> within 48 hours of service if the total exceeds 10%. Source: {src("LEGISTAR_261020", "File #261020")}</li>
    <li><b>Records filed</b> — notice, proof of service, calculation, licence record, and the dated reason the two units differ.</li>
  </ol>
</div>
"""
    return page("pages/questions.html", "Open questions", body,
                "Every question that blocks a rent-increase decision, what information answers it, what is already settled, and the sensitivity of each number.",
                active="pages/questions.html")


def suggestions_block():
    """Sections F-I of ``pages/suggestions.html`` (rendered by ``site_pages_ref.suggestions``).

    A parallel session on 13 November 2026 published sections A-E of that page — decision
    options, preconditions, open questions, presentation ideas and a review protocol.  This
    block contributes the second register the brief asked for: improvement proposals that stay
    marked *Proposed* until the owner accepts an ID, the ideas that should not be adopted, and
    the maintenance procedure.  Nothing in sections A-E is changed, and neither register is
    dropped: the site keeps one suggestions page rather than two competing ones.
    """
    rows = "".join(
        '<tr><td class="nowrap"><b>%s</b></td><td>%s</td><td>%s</td>'
        '<td><span class="badge warn">%s</span></td><td>%s</td><td>%s</td>%s</tr>'
        % (sid, what, problem, "Proposed", impact, effort, cell(*keys))
        for sid, what, problem, impact, effort, keys in SUGGESTIONS_LAW
    )
    reject_rows = "".join(
        "<tr><td>%s</td><td>%s</td>%s</tr>" % (what, why, cell(key))
        for what, why, key in SUGGESTIONS_REJECT
    )
    ui_list = "".join("<li>%s</li>" % s for s in SUGGESTIONS_UI)
    return f"""
<div class="card hero">
  <h2>F. Improvement proposals — awaiting your decision</h2>
  <p>Sections A to E above set out the decision options and the review protocol. This register is
  the other half of the request: proposals for improving <i>the site</i>, each with the problem it
  solves, its impact and its effort. <b>Every row reads <span class="badge warn">Proposed</span>
  and nothing here has been implemented</b> — the site records what was considered so the choice
  stays yours. To decide, reply with the IDs (for example “implement SG-01, SG-02, SG-07; decline
  SG-08”), or mark Accept / Decline / Defer against each row in your own notes.</p>
  <p class="small">Rows in a table carry the official rule the proposal has to stay consistent with;
  the presentation ideas in section I have no legal anchor and are deliberately listed rather than
  tabled. Questions that block the decision itself are on <a href="questions.html">Open questions</a>.</p>
</div>

<div class="card">
  <h2>G. The proposals, row by row</h2>
  <table>
    <thead><tr><th style="width:6%">ID</th><th style="width:24%">Suggestion</th>
    <th style="width:22%">Problem it solves</th><th style="width:10%">Status</th>
    <th style="width:14%">Impact</th><th style="width:12%">Effort</th>
    <th style="width:12%">Official anchor</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>H. Ideas that look tempting and should <i>not</i> be adopted</h2>
  <p>Recorded so that a later session does not “improve” the site into a compliance problem.</p>
  <table>
    <thead><tr><th style="width:34%">Not recommended</th><th>Reason</th>
    <th style="width:20%">Official source</th></tr></thead>
    <tbody>{reject_rows}</tbody>
  </table>
</div>

<div class="card">
  <h2>I. Presentation and tooling (no legal anchor, owner's taste)</h2>
  <ul class="tight">{ui_list}</ul>
</div>

<div class="card">
  <h2>J. How this register is maintained</h2>
  <ul class="tight">
    <li>New proposals take the next free <code>SG-</code> ID and are added to
    <code>tools/site_pages_decide.py</code>; nobody edits a published page by hand, because the
    build regenerates every page from its module.</li>
    <li>An accepted proposal becomes a task on <code>COORDINATION.md</code> carrying its ID, and the
    row above changes to <b>Accepted</b> or <b>Declined</b> with the date. Entries are never deleted,
    so the record shows what was considered and rejected as well as what was built.</li>
    <li>Anything touching shared outputs — the dashboard, the navigation, the table data — is applied
    by the integration session only, after the other tasks are done.</li>
    <li>Before an increase is served, the open items on <a href="questions.html">Open questions</a>
    outrank every proposal here.</li>
  </ul>
  <p class="small">Sources on this page are the official rules each proposal has to stay consistent
  with: {srcs("SF_HI", "SF_BANK", "SF_LI", "LEG_827", "SF_ALGO")}.</p>
</div>
"""
