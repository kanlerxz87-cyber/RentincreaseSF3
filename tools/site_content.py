#!/usr/bin/env python3
"""Content and source register for the consolidated edition (final integration, 2026-11-10).

Every value in this file was read from, or computed from, an official source fetched on
2026-11-10. Sources are declared once in SRC so that a typo in a URL is impossible and so
that every table row can be forced to carry at least one official link.

Privacy: no tenant name, initial, street address, ZIP code or neighbourhood name appears
here or in anything generated from it. Placeholders only. Dates and amounts are unchanged.
"""

from decimal import Decimal, ROUND_HALF_UP

# --------------------------------------------------------------------------------------
# Official source register. key -> (short label, url, official?)
# "official" means: a government or legislatively-published primary source.
# --------------------------------------------------------------------------------------
SRC = {
    # --- San Francisco Rent Board / sf.gov --------------------------------------------
    "rates": ("sf.gov — Learn about rent increases", "https://www.sf.gov/learn-about-rent-increases-san-francisco", True),
    "bank": ("sf.gov — Banked rent increases", "https://www.sf.gov/information/banked-rent-increases", True),
    "multiyear": ("sf.gov — Annual rent increase for multiple years", "https://www.sf.gov/information/annual-rent-increase-multiple-years", True),
    "irregular": ("sf.gov — Increasing rents during irregular periods", "https://www.sf.gov/information--increasing-rents-during-irregular-periods", True),
    "inventory": ("sf.gov — Rent Board Housing Inventory", "https://www.sf.gov/rent-board-housing-inventory", True),
    "noncompliance": ("sf.gov — Notice of Owner Noncompliance", "https://www.sf.gov/notice-of-owner-noncompliance-with-housing-inventory", True),
    "s3715": ("Admin. Code §37.15 (sf.gov)", "https://www.sf.gov/information/sec-3715-reporting-obligations-licensing", True),
    "s373": ("Admin. Code §37.3 (sf.gov)", "https://www.sf.gov/information/sec-373-rent-limitations", True),
    "s3710b": ("Admin. Code §37.10B — tenant harassment (sf.gov)", "https://www.sf.gov/information/sec-3710b-tenant-harassment", True),
    "s3710c": ("Admin. Code §37.10C — algorithmic devices (sf.gov)", "https://www.sf.gov/information/sec-3710c-use-and-sale-algorithmic-devices-prohibited", True),
    "ordinance": ("sf.gov — The Rent Ordinance (index & full PDF)", "https://www.sf.gov/reports--rent-ordinance", True),
    "laws": ("sf.gov — Learn about San Francisco rental laws", "https://www.sf.gov/learn-about-san-francisco-rental-laws", True),
    "petitions": ("sf.gov — Tenant Petitions", "https://www.sf.gov/tenant-petitions", True),
    "unlawful": ("sf.gov — Report an unlawful rent increase", "https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history", True),
    "resources": ("sf.gov — Tenant and Landlord Resources", "https://www.sf.gov/tenant-and-landlord-resources", True),
    "s614": ("sf.gov — Rent increases under §6.14 and Costa-Hawkins", "https://www.sf.gov/information--rent-increases-under-section-614-and-costa-hawkins", True),
    "announce": ("sf.gov — 1.6% increase for 3/1/26–2/28/27 announced", "https://www.sf.gov/news--annual-rent-increase-3126-22827-announced", True),
    "form571": ("Rent Board Form 571 — allowable increases 1982–2027 (PDF)", "https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf", True),
    "portal": ("sf.gov / Rent Board Portal", "https://portal.sfrb.org/", True),
    "discrim": ("sf.gov — Get help for discrimination in housing", "https://www.sf.gov/information--get-help-discrimination-housing", True),
    "legistar": ("Legistar File #261020 — pending 10%/yr cap (not law)", "https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770", True),

    # --- California statutes & statewide guidance -------------------------------------
    "civ827": ("Civ. Code §827", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827", True),
    "civ1942_5": ("Civ. Code §1942.5 (retaliation)", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5", True),
    "civ1947_12": ("Civ. Code §1947.12 (Tenant Protection Act, AB 1482)", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12", True),
    "civ1954_53": ("Civ. Code §1954.53 (Costa-Hawkins)", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954.53", True),
    "ccp1013": ("Code Civ. Proc. §1013", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1013", True),
    "gov12955": ("Gov. Code §12955 (FEHA — housing discrimination)", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=12955", True),
    "oag": ("California Attorney General — limits on rent increases", "https://oag.ca.gov/rentcaps", True),
    "crd": ("California Civil Rights Department — housing discrimination", "https://calcivilrights.ca.gov/housing/", True),

    # --- Federal ----------------------------------------------------------------------
    "fha": ("42 U.S.C. §3604 (Fair Housing Act)", "https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm", True),
}

# Hosts accepted as "official" by the row-citation check.
OFFICIAL_HOSTS = {
    "sf.gov", "www.sf.gov", "media.api.sf.gov", "portal.sfrb.org", "sfgov.legistar.com",
    "leginfo.legislature.ca.gov", "oag.ca.gov", "calcivilrights.ca.gov", "govinfo.gov",
    "legislature.ca.gov", "ccsf.gov",
}

# --------------------------------------------------------------------------------------
# Verified facts. `src` on each fact is the proof.
# --------------------------------------------------------------------------------------
FACTS = [
    # id, statement, sources, status
    ("L-01", "The SF Rent Ordinance (Administrative Code Ch. 37) covers rent control and eviction protection for many units built on or before June 13, 1979. A 1940 two-unit building is therefore presumptively covered; both units are treated as covered here.", ["laws"], "verified"),
    ("L-02", "The allowable annual increase is 60% of the published CPI change, set each March 1, and in no event more than 7%.", ["s373", "form571"], "verified"),
    ("L-03", "The allowable annual increase effective 3/1/2026–2/28/2027 is 1.6%; the prior year, 3/1/2025–2/28/2026, was 1.4%.", ["rates", "announce", "form571"], "verified"),
    ("L-04", "An increase may be imposed once every 12 months. The first increase is available 12 months after the tenancy began; once imposed, the effective date becomes the anniversary date.", ["rates"], "verified"),
    ("L-05", "Increases are calculated on base rent only, must not be rounded up, and must not be compounded. Parking or storage rent is generally part of base rent; passthroughs are not.", ["rates", "bank"], "verified"),
    ("L-06", "30 days' written notice if the increase is 10% or less (alone or combined with other increases in the prior 12 months); 90 days if more than 10%. If served by mail, add 5 calendar days.", ["civ827", "ccp1013", "rates"], "verified"),
    ("L-07", "The notice should state the dollar amount, the percentage, the effective date, and — for a banked increase — which part is banked. Use the rate in effect on the effective date, not the service date.", ["rates", "bank"], "verified"),
    ("L-08", "Banked increases are additive, never compounded, have no cap back to April 1, 1982, do not expire during a tenancy, may be used by a new owner, and do not carry over to a new tenant.", ["bank"], "verified"),
    ("L-09", "No petition or per-increase approval by the Rent Board is required for an annual or banked increase; the Rent Board's role is the Housing Inventory licence, not approval of the amount.", ["bank", "multiyear", "inventory"], "verified"),
    ("L-10", "All owners of residential property must report into the Rent Board Housing Inventory by March 1 each year. For 1–9 unit buildings and condominiums reporting began March 1, 2023; for 10+ unit buildings it began July 1, 2022.", ["inventory", "s3715", "noncompliance"], "verified"),
    ("L-11", "Reporting a tenant-occupied unit generates a rent-increase licence automatically; there is no separate application. The licence must be current on the effective date of the increase.", ["inventory", "s3715"], "verified"),
    ("L-12", "If the owner has not substantially complied with reporting, the licence is suspended; a tenant is not obligated to pay the increase for months during the suspension. A notice that takes effect while unlicensed may be null and void for multiple years.", ["s3715", "noncompliance"], "verified"),
    ("L-13", "The Rent Board may notify tenants when an owner is not in compliance, and a tenant may file an Unlawful Rent Increase Petition at no charge, with no time limit for filing.", ["noncompliance", "unlawful"], "verified"),
    ("L-14", "A landlord may not charge additional rent because an additional occupant moved into a unit with an existing tenant, even if the lease provides for it.", ["rates"], "verified"),
    ("L-15", "§6.14 allows an unlimited (market) increase when the last original occupant vacates, if the owner timely served a written 6.14 notice on each subsequent occupant; about 60 days is generally considered reasonable. Under Costa-Hawkins a co-tenant is not subject to such an increase regardless of when the co-tenant moved in.", ["s614", "civ1954_53"], "verified"),
    ("L-16", "Costa-Hawkins / AB 1482 initial-rent reset requires that no tenant from the prior tenancy remains in lawful possession. A co-tenant with an agreement with the landlord is not a new tenancy for that purpose.", ["civ1947_12", "civ1954_53", "s614"], "verified"),
    ("L-17", "AB 1482 caps increases at 5% + CPI, maximum 10%, but does not apply to housing under a local ordinance that restricts increases to a lower amount. SF's 1.6% is lower, so the state cap does not govern these units.", ["civ1947_12", "oag"], "verified"),
    ("L-18", "For a non-covered unit in the SF metro area the AB 1482 ceiling would be 8.8% for an increase starting 8/1/2026–7/31/2027. This figure is context only and is not lawful to charge on a covered unit.", ["oag"], "verified"),
    ("L-19", "There is no federal rent ceiling. Federal law prohibits discriminating in the terms or conditions of a rental because of race, colour, religion, sex, familial status, national origin, or disability.", ["fha"], "verified"),
    ("L-20", "California law makes it unlawful to discriminate in housing because of race, colour, religion, sex, gender identity, gender expression, sexual orientation, marital status, national origin, ancestry, familial status, source of income, disability, veteran or military status, or genetic information.", ["gov12955", "crd"], "verified"),
    ("L-21", "A landlord may not increase rent in retaliation for a tenant's habitability complaint, and may not increase rent or decrease services to retaliate against a tenant who organised or exercised rights.", ["civ1942_5"], "verified"),
    ("L-22", "Tenant harassment is prohibited, and evidence of bad faith may include a rent increase substantially in excess of market rates for comparable units, or one within six months of an attempt to recover possession.", ["s3710b"], "verified"),
    ("L-23", "Landlords may not use or sell algorithmic rent-setting devices for SF residential units (effective October 14, 2024).", ["s3710c"], "verified"),
    ("L-24", "The Rent Board does not adjudicate harassment, discrimination or retaliation claims; those go to the Human Rights Commission, the Civil Rights Department, HUD, or court.", ["petitions", "discrim"], "verified"),
    ("L-25", "Legistar File #261020 would cap combined banked and capital-improvement increases at 10% per year for three years, applying to banked increases noticed on or after September 15, 2026. Status: Pending Committee Action — not enacted.", ["legistar", "rates"], "verified"),
    ("L-26", "Free tenant help is available: Rent Board counselling at 415-252-4600, and free legal help for tenants with eviction court papers from the Eviction Defense Collaborative at 415-659-9184.", ["resources", "laws"], "verified"),
]

# --------------------------------------------------------------------------------------
# Rate history, exactly as published on Form 571 (26-27 edition).
# --------------------------------------------------------------------------------------
RATES = [
    ("3/1/2026 – 2/28/2027", "1.6"),
    ("3/1/2025 – 2/28/2026", "1.4"),
    ("3/1/2024 – 2/28/2025", "1.7"),
    ("3/1/2023 – 2/29/2024", "3.6"),
    ("3/1/2022 – 2/28/2023", "2.3"),
    ("3/1/2021 – 2/28/2022", "0.7"),
    ("3/1/2020 – 2/28/2021", "1.8"),
    ("3/1/2019 – 2/29/2020", "2.6"),
]


def money(d):
    return "${:,.2f}".format(Decimal(d))


def pct(d):
    return "{}%".format(Decimal(d).normalize())


def increase(base, rate):
    """Dollar increase and new rent for base rent `base` at `rate` (a percentage string)."""
    b = Decimal(str(base))
    r = Decimal(str(rate)) / Decimal(100)
    inc = (b * r).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return inc, b + inc


# --------------------------------------------------------------------------------------
# Unit facts, anonymised. Dates and amounts unchanged.
# --------------------------------------------------------------------------------------
UNIT1 = {
    "label": "Unit 1",
    "start": "1 February 2025",
    "base": "3995",
    "base_fmt": "$3,995.00",
    "anniversary": "1 February",
    "status": "Continuing tenancy: one original tenant (Tenant A) remains; a new occupant (Tenant D) was added on 1 April 2026 at the same rent. Not a vacancy.",
    "first_available": "1 February 2026 (1.4% for the 3/1/2025–2/28/2026 rate year) — not imposed",
    "next": "1 February 2027",
}

UNIT2 = {
    "label": "Unit 2",
    "start": "1 June 2019",
    "base": "3150",
    "base_fmt": "$3,150.00",
    "anniversary": "1 June",
    "status": "Continuing tenancy: Tenant B and Tenant C, unchanged since 2019. No increase is stated to have been imposed since the tenancy began.",
    "first_available": "1 June 2020 (1.8%) — no increase is stated to have been imposed",
    "next": "1 June 2027 on the anniversary, or an earlier date at least 12 months after the last increase",
}

# Unit 1 arithmetic
U1_16 = increase(3995, "1.6")            # single current year at 1 Feb 2027
U1_30 = increase(3995, "3.0")            # 1.4 banked + 1.6 (12-month reading only)
# Unit 2 arithmetic
U2_16 = increase(3150, "1.6")            # conservative single year
U2_101 = increase(3150, "10.1")          # banked 2020–2024 (24-month reading) + 1.6
U2_117 = increase(3150, "11.7")
U2_115 = increase(3150, "11.5")          # banked 2020–2025 only
U2_131 = increase(3150, "13.1")          # banked 2020–2025 + current 1.6
U2_100 = increase(3150, "10.0")          # recommended phased

# Arithmetic assertions — the build fails loudly rather than publishing bad numbers.
assert U1_16 == (Decimal("63.92"), Decimal("4058.92"))
assert U1_30 == (Decimal("119.85"), Decimal("4114.85"))
assert U2_16 == (Decimal("50.40"), Decimal("3200.40"))
assert U2_100 == (Decimal("315.00"), Decimal("3465.00"))
assert U2_101 == (Decimal("318.15"), Decimal("3468.15"))
assert U2_117 == (Decimal("368.55"), Decimal("3518.55"))
assert U2_115 == (Decimal("362.25"), Decimal("3512.25"))
assert U2_131 == (Decimal("412.65"), Decimal("3562.65"))
assert round(sum(Decimal(x) for x in ["1.8", "0.7", "2.3", "3.6", "1.7", "1.4"]), 1) == Decimal("11.5")
assert round(sum(Decimal(x) for x in ["1.8", "0.7", "2.3", "3.6", "1.7"]), 1) == Decimal("10.1")
assert Decimal("1.8") + Decimal("0.7") + Decimal("2.3") + Decimal("3.6") + Decimal("1.7") + Decimal("1.6") == Decimal("11.7")
assert Decimal("11.5") + Decimal("1.6") == Decimal("13.1")
assert Decimal("10.1") + Decimal("1.6") == Decimal("11.7")

# --------------------------------------------------------------------------------------
# Flagged-for-review register. Every entry has an official source link.
# --------------------------------------------------------------------------------------
FLAGS = [
    ("F-01", "High",
     "Pending ordinance could cap a banked catch-up at 10%",
     "Legistar File #261020 would limit combined banked and capital-improvement increases to 10% per year for three years, and sf.gov states it would apply to banked increases <strong>noticed on or after 15 September 2026</strong> — that is, to a notice served today. It is not enacted (status: Pending Committee Action), so the 13.1% figure remains lawful today, but a >10% notice served now could be reduced retroactively if it passes.",
     "Recommended action: keep the increase at or below 10% until the file's final action is known. Check the Legistar record before serving any banked notice.",
     ["legistar", "rates", "bank"]),
    ("F-02", "High",
     "The Rent Board's banking threshold is internally inconsistent: 24 months vs 12 months",
     "The 'Banked rent increases' page states a skipped increase is banked only if <strong>at least 24 full months</strong> pass without any increase. But the worked example on the same page (tenancy 1 Aug 2022, first increase 1 Aug 2025) allows 5.3% = 3.6% + 1.7%, which requires only a <strong>12-month</strong> gap for the later year; the 'multiple years' page likewise uses 12 months; the 'irregular periods' page states the 12-month test expressly. Both readings are published here, with the lower figure recommended.",
     "Closing this needs written confirmation from a Rent Board counsellor (415-252-4600). It changes Unit 1 by 1.4% and Unit 2 by 1.4%.",
     ["bank", "multiyear", "irregular", "form571"]),
    ("F-03", "High",
     "Unit 2 rent history not evidenced",
     "No ledger, lease or prior notice was supplied. Every Unit 2 figure above assumes <strong>no increase since 1 June 2019</strong>. If any increase was imposed, the banked total is lower and the anniversary date is different.",
     "Action: assemble the full rent ledger 2019–present before serving any Unit 2 notice.",
     ["bank", "form571"]),
    ("F-04", "Medium",
     "No official ZIP-level or neighbourhood rent benchmark exists",
     "The owner asked what is normal for the unit's specific ZIP code. Neither HUD, Census, the Rent Board nor the Attorney General publishes a lawful-or-market benchmark at ZIP level. The value is therefore left <strong>blank</strong>, not estimated. The lawful ceiling is citywide and does not vary by ZIP, so no conclusion depends on it.",
     "If a market comparison is wanted, pull HUD Fair Market Rents for the San Francisco metro area directly and record the retrieval date.",
     ["oag", "form571"]),
    ("F-05", "Medium",
     "Housing Inventory / licence status unknown",
     "No reporting history or licence confirmation was supplied. Without a licence current on the effective date, the increase is unenforceable no matter how correct the arithmetic is.",
     "Action: check the property in the Rent Board Portal and file the Housing Inventory if not already done.",
     ["inventory", "noncompliant" if False else "noncompliance", "portal"]),
    ("F-06", "Medium",
     "Subsidy status unknown",
     "Neither unit is stated to be voucher-assisted. If either were, the subsidy programme's own rent-setting rules can displace the ordinance arithmetic.",
     "Action: confirm with the tenant or the housing authority before assuming the 1.6% / banked figures apply.",
     ["civ1947_12", "laws"]),
    ("F-07", "Medium",
     "No official dataset compares corporate and individual owner increase rates",
     "The question 'how do big corporations handle increases vs individual owners' cannot be answered from an official source. Publicly verifiable elements are limited to the ordinance (same rules for everyone), the ban on algorithmic rent-setting devices, and the bulk-upload route for 5+ unit properties. Anything beyond that would be inference, so it is left out.",
     "Left blank rather than inferred. Would be closed by an official Rent Board statistical report giving increases by owner type.",
     ["s3710c", "inventory", "ordinance"]),
    ("F-08", "Low",
     "Building age and unit count are owner-reported",
     "Coverage turns on the certificate of occupancy date, not the build year. 1940 is well before 13 June 1979 and a two-unit building is not a single-family dwelling, so coverage is very likely — but the document itself was not produced.",
     "Action: confirm the certificate of occupancy date on the Planning Property Information Map, or ask a Rent Board counsellor.",
     ["laws"],),
    ("F-09", "Low",
     "Prior editions of this site disagreed with each other",
     "Six earlier editions are preserved in the repository. One stated that banked increases were capped at three years (incorrect — there is no cap), one used 1 April as the Unit 1 anniversary (the anniversary follows the 1 February 2025 tenancy start), one cited a 'Step 0' that does not exist on the page it linked to, and none addressed §6.14 / Costa-Hawkins for Unit 1. This edition supersedes them; they are kept for provenance only.",
     "No action needed. Recorded so that an older page found in a search result is not mistaken for current.",
     ["bank", "s614"]),
]

# Requirement checklist (each line traceable to a FACT id and therefore a source).
REQUIREMENTS = [
    ("R-01", "Confirm the units are covered by the Rent Ordinance", "Certificate of occupancy before 13 June 1979; not a single-family dwelling", "L-01", ["laws"]),
    ("R-02", "Report both units into the Rent Board Housing Inventory", "By 1 March each year; 1–9 unit buildings reporting began 1 March 2023", "L-10", ["inventory", "s3715"]),
    ("R-03", "Confirm a rent-increase licence is current on the effective date", "Generated automatically after reporting an occupied unit; no separate application", "L-11", ["inventory", "s3715"]),
    ("R-04", "Calculate on base rent only, at the rate in effect on the effective date", "1.6% for 3/1/2026–2/28/2027; no rounding up; no compounding", "L-03, L-05", ["rates", "form571"]),
    ("R-05", "Respect the 12-month interval and the anniversary date", "One increase per 12 months; a late increase resets the anniversary", "L-04", ["rates"]),
    ("R-06", "Serve written notice with the required content", "30 days if ≤10%; 90 days if >10%; +5 days if mailed; dollar, percentage, date, banked breakdown", "L-06, L-07", ["civ827", "ccp1013", "bank"]),
    ("R-07", "Keep the reason lawful and the policy uniform", "No discriminatory reason; no retaliation; no charge for an added occupant", "L-14, L-20, L-21", ["gov12955", "civ1942_5", "rates"]),
    ("R-08", "Do not use algorithmic rent-setting software", "Prohibited for SF residential units since 14 October 2024", "L-23", ["s3710c"]),
    ("R-09", "Re-check the pending ordinance before serving a banked notice over 10%", "File #261020, Pending Committee Action — not law", "L-25", ["legistar"]),
    ("R-10", "Keep records of every notice and proof of service", "Needed to answer an Unlawful Rent Increase Petition, which has no filing deadline", "L-13", ["unlawful", "noncompliance"]),
]
