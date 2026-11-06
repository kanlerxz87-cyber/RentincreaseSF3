"""Verified data for the Rental Increase Review site.

Every record that states a legal rule or a published rate carries a `src` key that maps to
an entry in SOURCES below. Anything that could not be confirmed from an official source is
left blank and listed in FLAGS instead of being filled in.

Verification date: 2026-11-06 (America/Los_Angeles).
All sources are government publications (sf.gov / sfgov.legistar.com / *.ca.gov /
*.house.gov / justice.gov) or primary statute text.
"""

VERIFIED_ON = "2026-11-06"

# ---------------------------------------------------------------------------
# SOURCES  (key -> dict)
# ---------------------------------------------------------------------------
SOURCES = {
    "S1": {
        "title": "Annual Rent Increase for 3/1/26 - 2/28/27 Announced",
        "publisher": "San Francisco Rent Board (sf.gov, news)",
        "url": "https://www.sf.gov/news--annual-rent-increase-3126-22827-announced",
        "supports": "Allowable annual increase is 1.6% for 3/1/2026-2/28/2027 and was 1.4% for 3/1/2025-2/28/2026; the $2,000 worked example.",
        "quote": "For rent-controlled units, the annual allowable increase amount effective March 1, 2026 through February 28, 2027 is 1.6%. ... The annual allowable increase amount effective March 1, 2025 through February 28, 2026 is 1.4%.",
    },
    "S2": {
        "title": "Learn about rent increases in San Francisco",
        "publisher": "San Francisco Rent Board (sf.gov)",
        "url": "https://www.sf.gov/learn-about-rent-increases-san-francisco",
        "supports": "60%-of-CPI formula, 12-month rule/anniversary date, rent increase license, base-rent-only rule, no rounding up, 30/90-day notice, prohibition on charging more for additional occupants, multi-year worked examples.",
        "quote": "A landlord can impose the first annual increase 12 months after the date the tenant's lease began. ... A landlord cannot charge additional rent simply because a new (or additional) roommate has moved into a unit with the existing tenant. This is an unlawful rent increase, even if the lease or rental agreement provides for the additional charge.",
    },
    "S3": {
        "title": "Banked rent increases",
        "publisher": "San Francisco Rent Board (sf.gov)",
        "url": "https://www.sf.gov/information--banked-rent-increases",
        "supports": "Definition of banking; the 24-month condition; no cap on banked amount; banked increases do not expire during a tenancy; partial increases bank the remainder; notice must identify the banked portion and its dates; no compounding.",
        "quote": "A skipped increase is only banked if at least 24 full months pass without any rent increase. If less than 24 months pass, the skipped increase is lost and cannot be imposed at a later date. ... There is no limit on how much can be banked. ... Banked increases do not expire during a tenancy.",
    },
    "S4": {
        "title": "571 Allowable Annual Increases (complete list, 1982-2027)",
        "publisher": "San Francisco Rent Board (sf.gov document)",
        "url": "https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf",
        "supports": "Historical table of allowable annual increases used for every banked-year calculation on this site.",
        "quote": "3/1/26-2/28/27 1.6%; 3/1/25-2/28/26 1.4%; 3/1/24-2/28/25 1.7%; 3/1/23-2/29/24 3.6%; 3/1/22-2/28/23 2.3%; 3/1/21-2/28/22 0.7%; 3/1/20-2/28/21 1.8%; 3/1/19-2/29/20 2.6%",
    },
    "S5": {
        "title": "Learn about San Francisco rental laws",
        "publisher": "San Francisco Rent Board (sf.gov)",
        "url": "https://www.sf.gov/learn-about-san-francisco-rental-laws/",
        "supports": "Coverage threshold of June 13, 1979; list of units with eviction protection only, and units wholly exempt from the Rent Ordinance.",
        "quote": "Many residential units built on or before June 13, 1979 have both rent control and eviction protection. ... If your unit was built before June 14, 1979, and is not used as a single family dwelling, it may have both.",
    },
    "S6": {
        "title": "The Rent Board Housing Inventory",
        "publisher": "San Francisco Rent Board (sf.gov)",
        "url": "https://www.sf.gov/rent-board-housing-inventory",
        "supports": "Annual reporting deadline of March 1; a rent increase license is generated for non-owner-occupied units; a notice is unenforceable without a license on the effective date.",
        "quote": "A landlord must have a current rent increase license on file with the Rent Board before any annual or banked rent increase can go into effect. ... your rent increase notice will not be enforceable without having a rent increase license on the effective date of the notice.",
    },
    "S7": {
        "title": "Current Rates, including Rent Increase, Relocation, Sec. Deposit",
        "publisher": "San Francisco Rent Board (sf.gov)",
        "url": "https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit",
        "supports": "Current 1.6% rate page for 3/1/2026-2/28/2027 plus prior two years; security-deposit interest rate; relocation amounts (context only).",
        "quote": "Allowable Rent Increase: 1.6% for March 1, 2026 - February 28, 2027",
    },
    "S8": {
        "title": "Annual rent increase for multiple years",
        "publisher": "San Francisco Rent Board (sf.gov)",
        "url": "https://www.sf.gov/information--annual-rent-increase-multiple-years",
        "supports": "How several years of allowable increases are added (not compounded) when two or more years have passed since the last increase; no petition required; no rounding up.",
        "quote": "In these situations, landlords may increase rent by adding up the allowable increases during that time period. ... Increases cannot be compounded.",
    },
    "S9": {
        "title": "Increasing rents during irregular periods",
        "publisher": "San Francisco Rent Board (sf.gov)",
        "url": "https://www.sf.gov/information--increasing-rents-during-irregular-periods",
        "supports": "Off-anniversary increases: at 12-24 months only the current annual increase is available; at 24 months or more the earlier periods may be added. Anniversary date definition.",
        "quote": "Your anniversary date is either: (1) The day and month of the last time your landlord increased your rent; or (2) The day and month your lease began (this applies if your landlord has never increased your rent).",
    },
    "S10": {
        "title": "Tenant Petitions",
        "publisher": "San Francisco Rent Board (sf.gov)",
        "url": "https://www.sf.gov/tenant-petitions",
        "supports": "Tenant may file a petition at no charge, including an unlawful-rent-increase claim; the Rent Board does not adjudicate harassment, discrimination or retaliation.",
        "quote": "There is no charge for filing the petition. ... we do not adjudicate issues that are not related to the amount of rent charged, such as harassment, discrimination and retaliation.",
    },
    "S11": {
        "title": "Report an unlawful rent increase or request a review of your rent history",
        "publisher": "San Francisco Rent Board (sf.gov)",
        "url": "https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history",
        "supports": "Tenant Petition Form 516C; no time limit for filing; arbitration hearing before a Rent Board Administrative Law Judge; written decision with appeal.",
        "quote": "There is no charge for filing the petition. There is no time limit for filing a petition.",
    },
    "S12": {
        "title": "Evictions in San Francisco",
        "publisher": "San Francisco Rent Board (sf.gov)",
        "url": "https://www.sf.gov/evictions-san-francisco",
        "supports": "Just-cause framework, and the free legal help available to tenants through the Eviction Defense Collaborative.",
        "quote": "If you are a tenant, and you receive an Unlawful Detainer Summons and Complaint, you should contact the Eviction Defense Collaborative at 415-659-9184 for free legal help.",
    },
    "S13": {
        "title": "Rent Ordinance (Administrative Code Chapter 37) - Sec. 37.3, as amended by Ordinance 248-24",
        "publisher": "City and County of San Francisco (media.api.sf.gov document)",
        "url": "https://media.api.sf.gov/documents/600_Ordinance_11-24-24.pdf",
        "supports": "Primary ordinance text for rent limitations (37.3(a)(1)), notice contents (37.3(b)), and the prohibition on increases for additional occupants (37.3(a)(11)).",
        "quote": "37.3(a)(1) Annual Rent Increase. On March 1 of each year, the Board shall publish the increase in the CPI for the preceding 12 months ... A landlord may impose annually a rent increase which does not exceed a tenant's base rent by more than 60% of said published increase. In no event, however, shall the allowable annual increase be greater than 7%.",
    },
    "S14": {
        "title": "Rent Board Rules and Regulations: Part IV - Rent Increases Not Requiring Approval by the Rent Board (Rules 4.10, 4.12)",
        "publisher": "San Francisco Rent Board (sf.gov)",
        "url": "https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring",
        "supports": "Rule 4.10 written-notice content for annual/banked increases; Rule 4.12 banking (accumulation, no compounding, no rounding up, banked-portion disclosure). Rule text still reads 'a full 12 months' - see Flag F1.",
        "quote": "Rule 4.12(a) ... Banked increases shall not be compounded and shall not be rounded up ... Rule 4.12(b) ... inform the tenant ... which portion of the rent increase reflects banked amount, and ... the dates upon which said banked amount is based.",
    },
    "S15": {
        "title": "California Civil Code section 827",
        "publisher": "California Legislative Information (leginfo.legislature.ca.gov)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827",
        "supports": "State notice rule for rent increases: 30 days if 10% or less, 90 days if more than 10%, measured against the rent charged at any time in the prior 12 months; service personally or by mail under CCP 1013.",
        "quote": "(2) If the proposed rent increase for that tenant is 10 percent or less ... the notice shall be delivered at least 30 days before the effective date ... (3)(A) If the proposed rent increase ... is greater than 10 percent ... the notice shall be delivered at least 90 days before the effective date.",
    },
    "S16": {
        "title": "California Civil Code section 1947.12 (Tenant Protection Act / AB 1482)",
        "publisher": "California Legislative Information",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12",
        "supports": "Statewide cap of 5% + CPI (max 10%), and the exemption in subdivision (d)(3) for housing subject to a local ordinance that restricts annual increases to a lower amount.",
        "quote": "(d) This section shall not apply to the following residential real properties: ... (3) Housing subject to rent or price control through a public entity's valid exercise of its police power ... that restricts annual increases in the rental rate to an amount less than that provided in subdivision (a).",
    },
    "S17": {
        "title": "California Civil Code section 1954.52 (Costa-Hawkins Rental Housing Act)",
        "publisher": "California Legislative Information",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954.52",
        "supports": "An owner may establish the initial rent for a new tenancy where no tenant from the prior tenancy remains (vacancy decontrol); buildings with a certificate of occupancy after 1 Feb 1995 are outside local rent caps.",
        "quote": "Notwithstanding any other provision of law, an owner of residential real property may establish the initial and all subsequent rental rates for a dwelling or a unit about which any of the following is true: (1) It has a certificate of occupancy issued after February 1, 1995.",
    },
    "S18": {
        "title": "California Civil Code section 1942.5 (retaliation)",
        "publisher": "California Legislative Information",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5",
        "supports": "A landlord may not increase rent in retaliation for a tenant's repair complaints or protected organizing, including during the 180 days after protected activity.",
        "quote": "If the lessor retaliates against the lessee because of the exercise by the lessee of the lessee's rights ... the lessor may not ... increase the rent ... within 180 days of any of the following ...",
    },
    "S19": {
        "title": "California Government Code section 12955 (housing discrimination)",
        "publisher": "California Legislative Information",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=12955",
        "supports": "State law listing the protected characteristics for housing (race, color, religion, sex, gender identity, sexual orientation, marital status, national origin, ancestry, familial status, source of income, disability, veteran/military status, genetic information).",
        "quote": "It shall be unlawful: (a) For the owner of any housing accommodation to discriminate against or harass any person because of the race, color, religion, sex, gender, gender identity, gender expression, sexual orientation, marital status, national origin, ancestry, familial status, source of income, disability, veteran or military status, or genetic information of that person.",
    },
    "S20": {
        "title": "42 U.S.C. section 3604 (Fair Housing Act)",
        "publisher": "U.S. Government Publishing Office (govinfo.gov)",
        "url": "https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm",
        "supports": "Federal prohibition on discrimination in the terms, conditions or privileges of a rental because of race, color, religion, sex, familial status or national origin (plus handicap in subsection (f)).",
        "quote": "(b) To discriminate against any person in the terms, conditions, or privileges of sale or rental of a dwelling, or in the provision of services or facilities in connection therewith, because of race, color, religion, sex, familial status, or national origin.",
    },
    "S21": {
        "title": "Limits on Rent Increases",
        "publisher": "California Department of Justice, Office of the Attorney General (oag.ca.gov)",
        "url": "https://oag.ca.gov/rentcaps",
        "supports": "Statewide AB 1482 caps by region (San Francisco area 6.3% for increases starting 8/1/25-7/31/26 and 8.8% for 8/1/26-7/31/27) and the local-cap row for San Francisco: 60% of CPI, 1.6% for 3/1/26-2/28/27, banking allowed.",
        "quote": "City and County of San Francisco ... one increase of up to 60% of the change in CPI ... 1.6% ... 3/1/26 - 2/28/27 ... Landlords may bank increases and add them to a later general increase.",
    },
    "S22": {
        "title": "Legistar File 261020 - Administrative Code - Cap On Rent Increases for Rent-Controlled Units",
        "publisher": "City and County of San Francisco, Board of Supervisors (sfgov.legistar.com)",
        "url": "https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770",
        "supports": "Pending (not enacted) ordinance to limit combined banked + capital-improvement rent increases to 10% per year for three years. Status shown as '30 Day Rule'; introduced 9/15/2026.",
        "quote": "File #: 261020 ... Ordinance amending the Administrative Code to provide that banked rent increases and capital improvement rent increases for rent-controlled units may not increase a tenant's rent by more than a total of 10% per year, for the next three years;",
    },
    "S23": {
        "title": "New law prohibits algorithmic devices used to set rents in San Francisco",
        "publisher": "San Francisco Rent Board (sf.gov, news)",
        "url": "https://www.sf.gov/news--new-law-prohibits-algorithmic-devices-used-set-rents-san-francisco",
        "supports": "Section 37.10C of the Rent Ordinance (effective 14 October 2024) bans selling or using algorithmic devices to set rents or manage occupancy for residential units in San Francisco.",
        "quote": "Legislation adding Section 37.10C to the Rent Ordinance went into effect on October 14, 2024. The law prohibits the sale or use of algorithmic devices to set rents or manage occupancy levels for residential units in San Francisco.",
    },
    "S24": {
        "title": "Justice Department Requires RealPage to End the Sharing of Competitively Sensitive Information and Alignment of Pricing Among Competitors",
        "publisher": "U.S. Department of Justice, Office of Public Affairs",
        "url": "https://www.justice.gov/opa/pr/justice-department-requires-realpage-end-sharing-competitively-sensitive-information-and",
        "supports": "Federal antitrust enforcement over algorithmic rent pricing used by large rental operators (proposed settlement filed 24 November 2025).",
        "quote": "RealPage's revenue management software has relied on nonpublic, competitively sensitive information shared by landlords to set rental prices. RealPage's software has also included features designed to limit rental price decreases and otherwise align pricing among competitors.",
    },
    "S25": {
        "title": "Form 1007 - Notice to Tenant (references the Tenant Right to Counsel Program)",
        "publisher": "San Francisco Rent Board (sf.gov document)",
        "url": "https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag%5B74%5D.pdf",
        "supports": "Confirms that San Francisco tenants facing eviction have access to the City-funded Tenant Right to Counsel Program and free intake through the Eviction Defense Collaborative.",
        "quote": "You are eligible for free assistance through the Tenant Right to Counsel Program. For intake, please contact the Eviction Defense Collaborative by phone at (415) 659-9184 ...",
    },
    "S26": {
        "title": "Form 571 (Spanish) - Aumentos de la renta permitidos 26-27",
        "publisher": "San Francisco Rent Board (sf.gov document)",
        "url": "https://www.sf.gov/documents/34343/571_Allowable_Annual_Increases_26-27_Spanish_1.26.pdf.pdf",
        "supports": "Spanish-language version of the allowable-increase table; confirm the same 1.6% figure for tenant notices in Spanish.",
        "quote": "1.6% - 3/1/26 - 2/28/27",
    },
    "S27": {
        "title": "Essex Property Trust, Inc. Form 10-K for fiscal year 2025 (SEC EDGAR filing index)",
        "publisher": "U.S. Securities and Exchange Commission (sec.gov)",
        "url": "https://www.sec.gov/Archives/edgar/data/920522/000092052226000003/0000920522-26-000003-index.htm",
        "supports": "Listed only as a primary disclosure for manual review of how a large, San Francisco-headquartered apartment REIT describes rent regulation. Not relied on for any statement on this site.",
        "quote": "(Filing index: Form 10-K, filed 2026-02-20, period of report 2025-12-31.)",
    },
}

# ---------------------------------------------------------------------------
# UNITS (anonymized)
# ---------------------------------------------------------------------------
UNITS = [
    {
        "id": "A",
        "label": "Unit A (\"Unit 1\" in the owner's records)",
        "type": "Rent-controlled, pre-1979 multi-unit building (per owner: built 1940)",
        "tenancy_start": "2025-02-01",
        "base_rent": 3995.00,
        "base_rent_since": "2025-02-01 (unchanged at the 2026-04-01 renewal)",
        "occupants_now": "2 (one original tenant since 2025-02-01, plus one co-tenant added 2026-04-01)",
        "history_note": "Initial lease named three tenants. On 2026-04-01 a new lease was signed with one of the original tenants still in place and one added co-tenant, at the same $3,995 rent.",
    },
    {
        "id": "B",
        "label": "Unit B (\"Unit 2\" in the owner's records)",
        "type": "Rent-controlled, pre-1979 multi-unit building (per owner: built 1940)",
        "tenancy_start": "2019-06-01",
        "base_rent": 3150.00,
        "base_rent_since": "2019-06-01 (no increase recorded since)",
        "occupants_now": "2 (both in place since 2019-06-01)",
        "history_note": "No change in tenants, rent or lease terms supplied for 2019-2026.",
    },
]

# ---------------------------------------------------------------------------
# HISTORICAL ALLOWABLE INCREASES (S4) - used for all banked math
# ---------------------------------------------------------------------------
AGA_HISTORY = [
    ("3/1/2026 - 2/28/2027", 1.6, "S4"),
    ("3/1/2025 - 2/28/2026", 1.4, "S4"),
    ("3/1/2024 - 2/28/2025", 1.7, "S4"),
    ("3/1/2023 - 2/29/2024", 3.6, "S4"),
    ("3/1/2022 - 2/28/2023", 2.3, "S4"),
    ("3/1/2021 - 2/28/2022", 0.7, "S4"),
    ("3/1/2020 - 2/28/2021", 1.8, "S4"),
    ("3/1/2019 - 2/29/2020", 2.6, "S4"),
]

# ---------------------------------------------------------------------------
# LEDGERS: one row per anniversary date on which an annual increase became available
# ---------------------------------------------------------------------------
LEDGER_A = [
    # anniversary, rate period in effect on that date, rate %, base rent, dollars, status, source
    ("2026-02-01", "3/1/2025 - 2/28/2026", 1.4, "available - not imposed", "S2, S4"),
    ("2027-02-01", "3/1/2026 - 2/28/2027", 1.6, "available (current annual)", "S2, S4"),
]

LEDGER_B = [
    ("2020-06-01", "3/1/2020 - 2/28/2021", 1.8, "skipped -> banked", "S3, S4"),
    ("2021-06-01", "3/1/2021 - 2/28/2022", 0.7, "skipped -> banked", "S3, S4"),
    ("2022-06-01", "3/1/2022 - 2/28/2023", 2.3, "skipped -> banked", "S3, S4"),
    ("2023-06-01", "3/1/2023 - 2/29/2024", 3.6, "skipped -> banked", "S3, S4"),
    ("2024-06-01", "3/1/2024 - 2/28/2025", 1.7, "skipped -> banked", "S3, S4"),
    ("2025-06-01", "3/1/2025 - 2/28/2026", 1.4, "skipped -> banked", "S3, S4"),
    ("2026-06-01", "3/1/2026 - 2/28/2027", 1.6, "skipped -> banked", "S3, S4"),
]

# ---------------------------------------------------------------------------
# RECOMMENDATION SCENARIOS
# ---------------------------------------------------------------------------
SCENARIOS_A = [
    {"name": "A1 - Annual increase only (1.6%)",
     "pct": 1.6, "dollars": 63.92, "new_rent": 4058.92,
     "notice": "30 days", "effective": "2027-02-01",
     "note": "Lawful under every reading of the banking rule. Leaves the 1.4% (and later banked amounts) in the bank.",
     "src": "S1, S2"},
    {"name": "A2 - Banked 1.4% + current 1.6% (3.0%) - recommended",
     "pct": 3.0, "dollars": 119.85, "new_rent": 4114.85,
     "notice": "30 days (increase is under 10%)", "effective": "2027-02-01",
     "note": "24 months without any increase have passed on 2027-02-01, so both available years may be added (S3, S8, S9). Keeps the 1 February anniversary.",
     "src": "S3, S8, S9"},
]

SCENARIOS_B = [
    {"name": "B1 - Annual increase only (1.6%)",
     "pct": 1.6, "dollars": 50.40, "new_rent": 3200.40,
     "notice": "30 days", "effective": "2026-12-06 or later",
     "note": "Lowest-friction option; the remaining 11.5% stays banked and does not expire (S3).",
     "src": "S1, S3"},
    {"name": "B2 - Phased catch-up at 10.0% - recommended for review",
     "pct": 10.0, "dollars": 315.00, "new_rent": 3465.00,
     "notice": "30 days (10% or less)", "effective": "2026-12-06 or later",
     "note": "Stays inside the 10% threshold that pending File 261020 would impose on banked increases, and preserves $97.65 (3.1%) in the bank.",
     "src": "S15, S22, S3"},
    {"name": "B3 - Full banked + current (13.1%)",
     "pct": 13.1, "dollars": 412.65, "new_rent": 3562.65,
     "notice": "90 days (increase exceeds 10%)", "effective": "2027-02-04 earliest if served 2026-11-06",
     "note": "Lawful today on the official guidance, but exposed to the pending 10% cap and is the type of increase most likely to draw a tenant petition.",
     "src": "S3, S8, S9, S15, S22"},
]

# ---------------------------------------------------------------------------
# REQUIREMENTS (federal / state / local)
# ---------------------------------------------------------------------------
REQUIREMENTS = [
    # layer, requirement, what it means for these two units, source
    ("Federal", "No federal rent-ceiling statute was found in the housing chapter of the U.S. Code (42 U.S.C. ch. 45).",
     "Nothing in federal law authorises a higher increase than San Francisco allows. The federal rule that does reach an increase decision is the Fair Housing Act.",
     "S20"),
    ("Federal", "Fair Housing Act, 42 U.S.C. 3604(b): no discrimination in the terms or conditions of a rental.",
     "A rent increase applied on a protected basis is unlawful even where the dollar amount is otherwise allowed. The increase terms must be set on lawful, documented grounds.",
     "S20"),
    ("Federal", "Federal antitrust enforcement over algorithmic rent-setting (DOJ v. RealPage).",
     "Do not use revenue-management or algorithmic pricing tools to set or raise rent on these units; San Francisco separately bans them (see local rows).",
     "S24, S23"),
    ("Federal", "Housing-subsidy rules (HUD / Housing Choice Voucher) - applicability not established.",
     "If either unit is voucher-assisted, the rent-increase rules differ. This has NOT been verified; flagged F7.",
     "S13"),
    ("State", "Civil Code 827: written notice of a rent increase.",
     "30 days' notice if the increase is 10% or less; 90 days if more than 10% (alone or combined with other increases in the prior 12 months). Add 5 days if served by mail.",
     "S15"),
    ("State", "Civil Code 1947.12 (AB 1482): statewide cap of 5% + CPI, max 10%.",
     "Does NOT set the ceiling here: subdivision (d)(3) exempts housing covered by a local ordinance that restricts increases to a lower amount. The state cap would be 8.8% for increases starting 8/1/2026-7/31/2027 - far above the local 1.6%.",
     "S16, S21"),
    ("State", "Civil Code 1954.52 (Costa-Hawkins): vacancy decontrol.",
     "The owner may set a new initial rent only when no tenant from the prior tenancy remains. Because an original Unit A tenant remained on 2026-04-01, that renewal was not a vacancy and did not reset the rent.",
     "S17, S13"),
    ("State", "Civil Code 1942.5: no retaliatory rent increase.",
     "No increase may be imposed in retaliation for repair complaints, habitability complaints or tenant organising (180-day presumption period).",
     "S18"),
    ("State", "Government Code 12955: state housing discrimination law.",
     "Rent terms may not differ on the basis of a protected characteristic, including source of income and familial status.",
     "S19"),
    ("Local", "Admin. Code 37.3(a)(1): annual increase = 60% of the prior year's CPI change, capped at 7%.",
     "The Rent Board published 1.6% for 3/1/2026-2/28/2027 and 1.4% for 3/1/2025-2/28/2026. That is the lawful annual ceiling on base rent.",
     "S13, S1, S4"),
    ("Local", "Coverage: units built on or before 13 June 1979 in a multi-unit building.",
     "Both units are stated to be in a 1940 building, so both are inside the Ordinance (verification of the property record is flagged F6).",
     "S5"),
    ("Local", "One increase every 12 months; anniversary date.",
     "The first increase may be imposed 12 months after the lease began; after that, at least 12 months apart. An increase imposed later sets a new anniversary date.",
     "S2, S9"),
    ("Local", "Banking: an unused increase may be taken later.",
     "A skipped increase is banked only if at least 24 full months pass without any rent increase; banked percentages are added, never compounded, and may not be rounded up. There is no cap and banked amounts do not expire during the tenancy.",
     "S3, S8, S14"),
    ("Local", "Rent increase license / Housing Inventory.",
     "The unit must be reported to the Rent Board Housing Inventory (deadline March 1 each year) and a current rent increase license must exist on the effective date, or the notice is unenforceable.",
     "S6, S2"),
    ("Local", "Increase is calculated on base rent only.",
     "Apply the percentage to base rent (including parking/storage if part of base rent); exclude temporary passthroughs and fluctuating charges. Do not round up to the nearest dollar.",
     "S2, S14"),
    ("Local", "Notice content: annual portion, banked portion and the dates it is based on.",
     "The notice must state the dollar amount, the percentage, the effective date, which part is banked and the dates of the banked years (Rule 4.10 / 37.3(b)).",
     "S13, S14, S3"),
    ("Local", "No increase solely because an additional occupant moved in.",
     "The 2026-04-01 addition of a co-tenant to Unit A cannot support any extra rent, even if a lease clause says otherwise.",
     "S2, S13"),
    ("Local", "Tenant challenge: petition for unlawful rent increase, no fee, no time limit.",
     "Any increase can be reviewed by a Rent Board Administrative Law Judge; a defective increase can be reduced or voided. Build the file accordingly.",
     "S10, S11"),
    ("Local", "Tenant legal help.",
     "Tenants have access to free Rent Board counseling and, in eviction proceedings, the City-funded Tenant Right to Counsel Program (Eviction Defense Collaborative intake).",
     "S12, S25"),
    ("Local", "Section 37.10C: algorithmic rent-setting devices banned.",
     "No pricing software may be used to set these rents; a tenant or the City Attorney may sue.",
     "S23"),
    ("Local", "Pending: File 261020, 10% cap on combined banked + capital-improvement increases.",
     "Introduced 2026-09-15, status '30 Day Rule' - not law as of 2026-11-06. Any banked plan must be re-checked before notice is served.",
     "S22"),
]

# ---------------------------------------------------------------------------
# FLAGS
# ---------------------------------------------------------------------------
FLAGS = [
    ("F1", "High", "Banking threshold: two official descriptions (12 vs 24 months).",
     "Rent Board Rule 4.12(a), as published on sf.gov, still reads 'A full 12 months must have elapsed...'. The current Rent Board page 'Banked rent increases' says a skipped increase is banked only if 'at least 24 full months pass without any rent increase', and the 'irregular periods' page allows stacking only from 24 months. The worked example on 'Learn about rent increases' uses 12 months.",
     "Calculations here use the 24-month reading (the dedicated banking page plus the irregular-periods page), and each scenario also shows the 1.6%-only fallback, which is lawful under either reading. Confirm in writing with a Rent Board counselor before serving a banked notice.",
     "S3, S9, S14, S2"),
    ("F2", "Medium", "Official worked-example typo.",
     "On 'Learn about rent increases in San Francisco', the first worked example says 'the annual allowable increase in effect on June 1, 2025 is 1.6%'. The 1.6% rate is in effect 3/1/2026-2/28/2027; 1.4% was in effect on 6/1/2025. The multi-year examples on the same page are internally consistent.",
     "Treated as a typo. The percentage used for an increase is the one in effect on the effective date of the increase, which is also what the same official page states in its 'Giving notice' section.",
     "S2"),
    ("F3", "High", "Pending 10% cap ordinance (File 261020).",
     "Legistar File 261020 would cap combined banked + capital-improvement increases at 10% per year for three years. Status on 2026-11-06: '30 Day Rule', introduced 2026-09-15, in the Land Use and Transportation Committee; no final action shown. Press reports say a vote was expected in November or December 2026 and that the cap would apply to banked increases issued on or after 15 September 2026.",
     "Not applied as law. Re-check the Legistar file before serving any notice above 10%; scenario B2 (10.0%) stays compliant either way.",
     "S22"),
    ("F4", "Medium", "Anniversary date for Unit A after the 2026-04-01 renewal.",
     "The Rent Board defines the anniversary date as the month/day of the last increase, or of the lease start if there has never been an increase. It is not explicit whether a renewal signed while an original tenant remains moves the date from 1 February to 1 April.",
     "Both readings produce the same 3.0% result for an increase effective in 2027 (1.4% + 1.6% are available either way), but the earliest lawful effective date differs (1 Feb 2027 vs 1 Apr 2027). Confirm with the Rent Board.",
     "S9, S2, S17"),
    ("F5", "High", "No documentary history of prior notices or increases.",
     "The owner supplied the tenancy start dates and current rents. No prior rent-increase notices, leases, registration records or rent receipts were provided, so the lawful base rent for each unit has not been reconstructed from documents.",
     "All arithmetic starts from the stated rents. Before serving notice, assemble the file: original lease, every increase notice, proof of service, and the Housing Inventory record.",
     "S11, S6"),
    ("F6", "Medium", "Property record not verified (year built, unit count, use).",
     "Coverage depends on the building being a multi-unit residential building with a certificate of occupancy on or before 13 June 1979 (owner states 1940), and not a single-family dwelling or condo held in a way that triggers an exemption.",
     "Verify on the Planning Property Information Map and the Assessor's parcel record, and keep a printout in the file. If coverage failed, AB 1482 would apply instead (8.8% for the current state year).",
     "S5, S21"),
    ("F7", "Medium", "Rent increase license / Housing Inventory status unknown.",
     "No Housing Inventory submission or rent increase license was supplied. Without a current license on the effective date the increase is unenforceable, regardless of correct arithmetic.",
     "Check the Rent Board portal, submit the Housing Inventory report if needed, and attach the license confirmation to the file.",
     "S6"),
    ("F8", "Medium", "Subsidy status unknown (Section 8 / HUD).",
     "Neither unit is stated to be voucher-assisted. If it were, the Rent Ordinance limits on annual increases can be displaced by the subsidy programme's own rent-setting rules.",
     "Confirm with the tenants' assistance programme before assuming the 1.6% / banked calculation applies.",
     "S13"),
    ("F9", "Low", "Market-rent benchmark not verified.",
     "No official market-rent figure for ZIP 94122 is published at a ZIP level by HUD or Census in a form that could be retrieved here (HUD's FMR lookup and the Census API were not accessible during this session), so no comparison to market rent is presented.",
     "Left blank rather than estimated. If a market benchmark is wanted, pull the HUD FY2027 Fair Market Rent for the San Francisco HUD Metro FMR Area directly from huduser.gov and record it with its retrieval date.",
     "S21"),
    ("F10", "Low", "PR/pages record and cross-session coordination.",
     "This repository had no other session claims when the work started; the board in COORDINATION.md records this session as owner of all scopes and as the final integration session.",
     "See COORDINATION.md for the PR link and merge result.",
     "S27"),
]

# ---------------------------------------------------------------------------
# TENANT-LAWYER STRESS TEST
# ---------------------------------------------------------------------------
STRESS_TEST = [
    ("C1", "Is the unit covered by the Rent Ordinance?", "Building on or before 13 June 1979, multi-unit residential, not a single-family home or exempt condo; no substantial-rehabilitation or subsidy exemption.", "S5, S13"),
    ("C2", "Is there a current rent increase license on the effective date?", "Housing Inventory report filed; license visible in the Rent Board portal on the effective date of the increase.", "S6"),
    ("C3", "Is the percentage within the published allowable increase?", "The rate in effect on the effective date is applied to base rent; the notice cites the Rent Board document 571 rate period.", "S1, S4"),
    ("C4", "Is the arithmetic exact - no compounding, no rounding up?", "Percentages added, then applied once to base rent; cents kept; no rounding to the nearest dollar.", "S2, S3, S8"),
    ("C5", "Are banked years correctly dated and within the 24-month rule?", "At least 24 full months without any increase; each banked year identified with its date and rate; only years that could have been imposed after 1 April 1982.", "S3, S9"),
    ("C6", "Has at least 12 months passed since the last increase?", "Compare the effective date with the prior increase (or lease start) and keep a copy of the prior notice.", "S2, S9"),
    ("C7", "Is the notice period long enough?", "30 days for 10% or less; 90 days for more than 10%; 5 extra days if mailed. Start counting from the day after service.", "S15, S2"),
    ("C8", "Does the notice contain every required element?", "Dollar amount, percentage, effective date, which part is annual and which is banked, the dates of the banked years, and how the increase was calculated.", "S13, S14, S3"),
    ("C9", "Is service documented?", "Personal delivery or mail per CCP 1013; keep the proof of service affidavit and a copy of the notice.", "S15"),
    ("C10", "Is any part of the increase for an additional occupant?", "None. A co-tenant moving in cannot generate rent, even under a lease clause permitting it.", "S2, S13"),
    ("C11", "Is the increase free of retaliation?", "No complaint, repair request, inspection, petition or organising activity in the 180 days before service - or, if there was, a documented independent reason and consistent treatment.", "S18"),
    ("C12", "Is the increase free of discrimination?", "Same rule applied to both units; no protected characteristic correlates with the difference; written criteria recorded before the increase.", "S19, S20"),
    ("C13", "Are other charges kept separate?", "Passthroughs (water bond, general obligation bond, Rent Board fee share, utility) are separate line items with their own requirements, not folded into the annual increase.", "S2, S14"),
    ("C14", "Would the file survive a tenant petition?", "Lease, prior notices, proof of service, license, rate printout, and the calculation worksheet are all in one folder (the Rent Board requires no fee and imposes no time limit on petitions).", "S10, S11"),
    ("C15", "Is the tenant told how to question the increase?", "Notice or covering letter states that the tenant may contact the Rent Board (415-252-4600) and may file a petition at no charge.", "S10, S11"),
]

# ---------------------------------------------------------------------------
# NOTICE TEMPLATE (placeholders only)
# ---------------------------------------------------------------------------
NOTICE_ELEMENTS = [
    ("Dollar amount of the increase", "New base rent and the dollar increase per month, in figures and words.", "S2, S13"),
    ("Percentage of the increase", "The percentage applied, and the rate period it comes from (for example 1.6% for 3/1/2026-2/28/2027).", "S1, S2"),
    ("Effective date", "The first day the new rent is due, at least 12 months after the last increase or lease start.", "S2, S9"),
    ("Which part is annual and which part is banked", "Break out the current annual portion and each banked year separately.", "S14, S3"),
    ("Dates the banked amount is based on", "The anniversary date of each banked year and its percentage.", "S14, S3"),
    ("Calculation on base rent only", "Show base rent x percentage; exclude passthroughs and fluctuating charges.", "S2"),
    ("No rounding up", "Keep the exact cent amount.", "S2, S3"),
    ("Tenant's right to question the increase", "Rent Board counseling line and the no-fee tenant petition route.", "S10, S11"),
]
