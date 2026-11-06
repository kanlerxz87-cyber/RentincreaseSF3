#!/usr/bin/env python3
"""content.py - all site content, the source register and the flag register.

VERIFICATION DISCIPLINE
  Every factual value published on this site traces to a row in SOURCES below.
  The "method" field records HOW each source was verified:
    "fetched" - the document was retrieved and read directly during research
                on 2026-11-06, and the value quoted here was read off it.
    "ci"      - the URL is an official-source URL recorded for this project;
                its content was NOT independently read in full, so it is
                HTTP-verified by tools/check_links.py in CI and is labelled
                accordingly on the site. It is never used as the sole support
                for a numeric value.
  Any value that could not be confirmed from an official source is left BLANK
  and appears in FLAGS / on the "Flagged for Review" page. Values are never
  inferred, estimated or forecast.
"""

AS_OF = "2026-11-06"

# --------------------------------------------------------------------------
# SOURCE REGISTER
# --------------------------------------------------------------------------
SOURCES = [
    # ---- San Francisco, local ----
    dict(id="S1", juris="Local (SF)", method="fetched",
         title="Current Rates, including Rent Increase, Relocation, Sec. Deposit",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit",
         verifies="Allowable rent increase 1.6% (3/1/2026-2/28/2027), 1.4% (3/1/2025-2/28/2026), "
                  "1.7% (3/1/2024-2/28/2025); security deposit interest 4.2% / 5.0% / 5.2%; "
                  "capital-improvement imputed interest rates 4.1%-4.8%; Rent Board fee amounts that can be banked."),
    dict(id="S2", juris="Local (SF)", method="fetched",
         title="Document 571 - Allowable Annual Increases (complete history, 4/1/1982 - 2/28/2027)",
         pub="SF Rent Board (sf.gov PDF)",
         url="https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf",
         verifies="Every allowable annual increase percentage used in the banking calculations, plus the "
                  "official caution that only ONE of the two 1992-93 rates may be imposed."),
    dict(id="S3", juris="Local (SF)", method="fetched",
         title="Learn about rent increases in San Francisco",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/learn-about-rent-increases-san-francisco",
         verifies="1.6% current AGA; 60%-of-CPI basis; 7% ceiling context; once per 12 months; base rent only; "
                  "no rounding up; 30-day / 90-day notice and +5 days if mailed; contents of the notice; "
                  "use the percentage in effect on the effective date; rent increase license; "
                  "no charge for an additional roommate; FOUR official worked examples used to self-test the calculator."),
    dict(id="S4", juris="Local (SF)", method="fetched",
         title="Banked rent increases",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/information--banked-rent-increases",
         verifies="Banking mechanics: add percentages, do not compound, do not prorate; no limit on how much "
                  "can be banked; banked increases do not expire during a tenancy; new owners may use them; "
                  "they do NOT carry over to a new tenant; partial increases leave the remainder banked; "
                  "notice must state which part is banked; official worked example ($1,300 -> $1,387.10)."),
    dict(id="S5", juris="Local (SF)", method="fetched",
         title="Rent Board Rules and Regulations, Part IV - Rent Increases Not Requiring Approval",
         pub="SF Rent Board (sf.gov) - official regulation text",
         url="https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring",
         verifies="Sec. 4.10 Notice (disclosure of each component; non-conforming increase null and void); "
                  "Sec. 4.12 Banking (CONTROLLING TEXT: 'A full 12 months must have elapsed...'; not compounded; "
                  "not rounded up; half-percent good-faith readjustment; duty to identify the banked portion and dates); "
                  "Sec. 4.15 Effect of Vacancy (the Ordinance does not regulate initial rent for a new tenancy)."),
    dict(id="S6", juris="Local (SF)", method="fetched",
         title="Document 600 - Chapter 37, Residential Rent Stabilization and Arbitration Ordinance (compiled, amended 11/24/2024)",
         pub="City & County of San Francisco (sf.gov PDF)",
         url="https://media.api.sf.gov/documents/600_Ordinance_11-24-24.pdf",
         verifies="Sec. 37.2 definitions (CPI, housing services, rent, rent increases, rental units and exclusions); "
                  "Sec. 37.3(a)(8) petition required for any increase above those permitted; "
                  "Sec. 37.3(a)(9) lead-remediation 10%/12-month cap; Sec. 37.3(a)(11) prohibition on increases for "
                  "additional occupants; Sec. 37.3(b)(1)-(6) mandatory notice contents and 'Nonconforming Rent "
                  "Increases... shall be null and void'; Sec. 37.3(c) subtenant rent limit; Sec. 37.3(d) Costa-Hawkins "
                  "conformance; table of contents confirming Sec. 37.10B Tenant Harassment, Sec. 37.10C Use and Sale of "
                  "Algorithmic Devices Prohibited (Ord. 224-24, eff. 10/14/2024) and Sec. 37.15 Reporting Obligations; Licensing."),
    dict(id="S7", juris="Local (SF)", method="fetched",
         title="Learn about San Francisco rental laws",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/learn-about-san-francisco-rental-laws",
         verifies="Coverage test: units built on or before June 13, 1979 generally have both rent control and eviction "
                  "protection; how to check the building's age; the categories that have eviction protection only; "
                  "the eight categories entirely exempt from the Rent Ordinance; Rent Board counselor line 415-252-4600."),
    dict(id="S8", juris="Local (SF)", method="fetched",
         title="The Rent Board Housing Inventory (rent increase license)",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/rent-board-housing-inventory",
         verifies="All residential owners must report; a rent increase license is generated for tenant-occupied units; "
                  "a current license must be on file BEFORE any annual or banked increase goes into effect; "
                  "the notice is unenforceable without a license on the effective date; annual deadline March 1; "
                  "no monetary penalty for late filing; submitted information is PUBLIC; tenants may search the portal; "
                  "operative 7/1/2022 for non-condo buildings with 10+ units, reporting began 3/1/2023 for condos "
                  "and buildings with fewer than 10 units."),
    dict(id="S9", juris="Local (SF)", method="ci",
         title="Notice of Owner Noncompliance with Housing Inventory",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/notice-of-owner-noncompliance-with-housing-inventory",
         verifies="A rent increase notice that goes into effect while the unit is unlicensed may be null and void "
                  "(and may apply for multiple years); the tenant may be entitled to a refund; the license rules apply "
                  "ONLY to rent-controlled units; tenant remedies (Form 354 petition / Form 361 summary petition)."),
    dict(id="S10", juris="Local (SF)", method="fetched",
         title="The Rent Board Fee",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/rent-board-fee",
         verifies="2026-2027 fee: $59.00 per dwelling unit, $29.50 per guest unit; deadline March 1; 5% late penalty "
                  "per month capped at 15%; owner may recover 50% ($29.50/unit) from a tenant in occupancy as of "
                  "November 1 of the applicable tax year; exemption request window; fee cycle timeline."),
    dict(id="S11", juris="Local (SF)", method="fetched",
         title="Replacement of Roommates",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/information--replacement-roommates",
         verifies="Tenants may generally replace departing roommates even against a lease; the 14-day written "
                  "consent procedure and its time limits; the grounds on which a denial is reasonable (Rules 6.15A, "
                  "6.15B, 6.15D, 6.15E); occupancy limits by bedroom count; 'The landlord may not increase the rent "
                  "for the unit based on the replacement of a departing tenant or the addition of new occupants, even "
                  "if agreed to by the tenant'; market-rate reset only where ALL original tenants have permanently "
                  "vacated and only subtenants who moved in on/after 1/1/1996 remain."),
    dict(id="S12", juris="Local (SF)", method="fetched",
         title="Rent Increases Under Section 6.14 And Costa-Hawkins",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/information--rent-increases-under-section-614-and-costa-hawkins/",
         verifies="Rules & Regs Sec. 6.14: an unlimited increase on remaining occupants when the LAST original "
                  "occupant vacates, and only if a written 6.14 notice was timely served on each subsequent occupant "
                  "(generally 60 days is reasonable); Costa-Hawkins reaches only a lawful SUBTENANT or assignee who did "
                  "not reside there before 1/1/1996; a CO-TENANT is never subject to it regardless of move-in date; "
                  "no petition is required but a tenant may petition alleging an unlawful increase."),
    dict(id="S13", juris="Local (SF)", method="fetched",
         title="Landlord Petitions and Passthroughs",
         pub="SF Rent Board (sf.gov)",
         url="https://sf.gov/landlord-petitions-and-passthroughs",
         verifies="The exhaustive list of above-AGA increase mechanisms: capital improvement passthrough; operating "
                  "and maintenance expense increase; special circumstances / comparable units; Proposition I past rent "
                  "history; utility passthrough; Rules & Regs Sec. 1.21 (no tenant in occupancy); plus the elective "
                  "Sec. 6.14 / Costa-Hawkins determination petition and the lawful-rent determination petition. "
                  "Filing is free; tenants need not pay until the Board approves; approval is retroactive to the "
                  "notice's effective date. Rent Board address: 25 Van Ness Ave, Suite 700."),
    dict(id="S14", juris="Local (SF)", method="fetched",
         title="Tenant petitions",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/information--tenant-petitions",
         verifies="Tenant remedies and forms: 352 decrease in housing services; 353 failure to repair and maintain; "
                  "354 unlawful rent increase / determination of lawful rent; 355-358 passthrough challenges; "
                  "359/360 subtenant claims; 361 tenant summary petition on an invalid notice; 362 wrongful eviction; "
                  "363 financial hardship. Filing is free; matters resolve by mediation or arbitration before an ALJ. "
                  "JURISDICTION: the Rent Board does NOT adjudicate harassment, discrimination, retaliation or "
                  "security deposits - those go to court or another forum."),
    dict(id="S15", juris="Local (SF)", method="ci",
         title="Rent Board Referral Listing (free tenant legal services)",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/information/rent-board-referral-listing",
         verifies="The official list of free tenant-side counselling and legal services a tenant can use to challenge "
                  "an increase (Bay Area Legal Aid, Housing Rights Committee of SF, Eviction Defense Collaborative, "
                  "SF Tenants Union, Causa Justa :: Just Cause, Tenderloin Housing Clinic, Open Door Legal, Advancing "
                  "Justice-Asian Law Caucus, Legal Assistance to the Elderly, Chinatown CDC, SRO Collaboratives, "
                  "Bar Association of SF Justice & Diversity Center / LARC). The Rent Board cannot refer to individual "
                  "attorneys and no lawyer is needed to file a petition."),
    dict(id="S16", juris="Local (SF)", method="fetched",
         title="Allowable rent increases",
         pub="SF Rent Board (sf.gov)",
         url="https://sf.gov/information/allowable-rent-increases",
         verifies="The two inputs to any lawful increase (the published rate and the date of the last increase or "
                  "lease start); the 12-month rule; base rent excludes passthrough charges; parking/storage generally "
                  "IS base rent; increases are never automatic; 30/90-day notice plus 5 days if mailed."),
    dict(id="S17", juris="Local (SF)", method="fetched",
         title="Annual rent increases",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/information--annual-rent-increases",
         verifies="No petition is required to impose an annual allowable increase; landlords cannot round up to the "
                  "nearest dollar; worked calculation ($1,500 x 1.6% = $24)."),
    dict(id="S18", juris="Local (SF)", method="ci",
         title="Report an unlawful rent increase or request a review of your rent history",
         pub="SF Rent Board (sf.gov)",
         url="https://sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history",
         verifies="The tenant-facing entry point for challenging an increase and for obtaining a rent-history "
                  "determination - i.e. the mechanism by which any increase on these units would be scrutinised."),
    dict(id="S19", juris="Local (SF)", method="ci",
         title="Rent Board Forms Center",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/rent-board-forms-forms-center/",
         verifies="Official forms referenced throughout this project (571, 572, 573, 354, 361, 302, 322-331)."),
    dict(id="S20", juris="Local (SF)", method="ci",
         title="Rent Board (department home)",
         pub="SF Rent Board (sf.gov)",
         url="https://www.sf.gov/departments--rent-board/",
         verifies="The administering agency for the San Francisco Rent Ordinance."),
    dict(id="S21", juris="Local (SF)", method="ci",
         title="San Francisco Property Information Map (PIM)",
         pub="SF Dept. of Building Inspection / Planning (sfplanninggis.org)",
         url="https://sfplanninggis.org/PIM/",
         verifies="The tool sf.gov directs owners and tenants to use to establish WHEN A BUILDING WAS BUILT, which "
                  "is the coverage test under the Rent Ordinance."),
    dict(id="S22", juris="Local (SF)", method="ci",
         title="Rent Board Portal (Housing Inventory filing, license lookup, fee payment)",
         pub="SF Rent Board (portal.sfrb.org)",
         url="https://portal.sfrb.org/",
         verifies="Where the Housing Inventory is filed, the rent increase license is generated and looked up, and "
                  "the Rent Board fee is paid."),

    # ---- California, state ----
    dict(id="S23", juris="State (CA)", method="fetched",
         title="Cal. Civil Code Sec. 827 - notice of change in terms of tenancy",
         pub="California Legislative Information (leginfo.legislature.ca.gov)",
         url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827",
         verifies="Sec. 827(b)(2): 30 days' written notice where the proposed increase is 10% or less of the rent "
                  "charged at any time in the prior 12 months, alone or combined with other increases. "
                  "Sec. 827(b)(3)(A): 90 days where it is greater than 10%. Sec. 827(b)(1): service personally or by "
                  "mail under CCP Sec. 1013."),
    dict(id="S24", juris="State (CA)", method="fetched",
         title="Cal. Civil Code Sec. 1947.12 - Tenant Protection Act of 2019 (AB 1482) rent cap",
         pub="California Legislative Information (leginfo.legislature.ca.gov)",
         url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12",
         verifies="Sec. 1947.12(a)(1): cap of 5% plus the percentage change in the cost of living, or 10%, whichever "
                  "is LOWER, over any 12-month period. Sec. 1947.12(d)(3): EXEMPTION for housing subject to local rent "
                  "or price control that restricts annual increases to LESS than subdivision (a) - this is why the SF "
                  "cap, not the state cap, governs these units. Sec. 1947.12(d)(5)(A): the separately-alienable "
                  "(single-family / condo) exemption is UNAVAILABLE to a REIT, a corporation, or an LLC with a "
                  "corporate member. Sec. 1947.12(e): notice per Sec. 827. Sec. 1947.12(g)(1)(A)(iv) and (g)(3)(B): "
                  "the applicable CPI-U is the San Francisco-Oakland-Hayward metropolitan index, measured April to "
                  "April for increases effective on or after August 1."),
    dict(id="S25", juris="State (CA)", method="fetched",
         title="Cal. Civil Code Sec. 1954.53 - Costa-Hawkins: initial rental rate on vacancy",
         pub="California Legislative Information (leginfo.legislature.ca.gov)",
         url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954.53",
         verifies="Sec. 1954.53(a): an owner may establish the INITIAL rental rate on a new tenancy, subject to "
                  "exceptions. Sec. 1954.53(b): subdivision (a) includes RENEWAL of the initial hiring by the same "
                  "tenant/subtenant for the entire period of occupancy AT THE RATE ESTABLISHED FOR THE INITIAL HIRING. "
                  "Sec. 1954.53(d)(2): a market-rate increase reaches only a lawful sublessee or assignee who did not "
                  "reside there before 1/1/1996, and only if the original occupant(s) no longer permanently reside "
                  "there. Sec. 1954.53(d)(3): DOES NOT APPLY to a PARTIAL CHANGE IN OCCUPANCY where one or more "
                  "occupants under the agreement with the owner remains in lawful possession. Sec. 1954.53(f): serious "
                  "uncorrected code violations block the provision. Amended by Stats. 2023, Ch. 767 (AB 1620)."),
    dict(id="S26", juris="State (CA)", method="fetched",
         title="Cal. Civil Code Sec. 1954.52 - Costa-Hawkins: exemptions",
         pub="California Legislative Information (leginfo.legislature.ca.gov)",
         url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954.52",
         verifies="Sec. 1954.52(a): an owner may set initial and all subsequent rents where the unit has a certificate "
                  "of occupancy issued after 2/1/1995, was already exempt on/before 2/1/1995 under a local "
                  "new-construction exemption, or is separately alienable. Sec. 1954.52(d): the section does not apply "
                  "to a unit with serious health, safety, fire or building code violations cited and unabated for six "
                  "months or longer preceding the vacancy. Amended by Stats. 2004, Ch. 568, Sec. 4."),
    dict(id="S27", juris="State (CA)", method="ci",
         title="Cal. Civil Code Sec. 1946.2 - just cause for termination",
         pub="California Legislative Information (leginfo.legislature.ca.gov)",
         url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1946.2",
         verifies="The statewide just-cause requirement that accompanies the AB 1482 rent cap (context only - SF "
                  "Chapter 37 Sec. 37.9 supplies the operative just-cause regime for these units)."),
    dict(id="S28", juris="State (CA)", method="ci",
         title="AB-1482 Tenant Protection Act of 2019 - bill text",
         pub="California Legislative Information (leginfo.legislature.ca.gov)",
         url="https://www.leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=201920200AB1482",
         verifies="Legislative history of the statewide cap and the exemption structure codified at Civ. Code "
                  "Sec. 1946.2 and Sec. 1947.12."),
    dict(id="S29", juris="State (CA)", method="fetched",
         title="Consumer Price Index Table Percentage Changes - All Areas (2025-2026)",
         pub="CA Dept. of Industrial Relations, Office of the Director - Research Unit",
         url="https://www.dir.ca.gov/oprl/CPI/PresentCCPIchange.PDF",
         verifies="CPI-U, San Francisco-Oakland-Hayward, 12-month percentage change: April 2025 = 1.3%; "
                  "August 2025 = 2.5%; October 2025 = unavailable; December 2025 = 3.0%; 2025 annual average = 2.2%; "
                  "February 2026 = 2.5%; April 2026 = 3.8%; June 2026 = 3.8%; August 2026 = 3.4%. "
                  "Last updated 10/15/2026. Used with Civ. Code Sec. 1947.12(g) to compute the statewide cap."),
    dict(id="S30", juris="State (CA)", method="fetched",
         title="California Consumer Price Index (index page, tables and calculator)",
         pub="CA Dept. of Industrial Relations",
         url="https://www.dir.ca.gov/oprl/capriceindex.htm",
         verifies="The official publication point for California CPI data, including the 1955-2026 series and the "
                  "CPI calculator (1989-2026)."),
    dict(id="S31", juris="State (CA)", method="fetched",
         title="Important Notice Regarding the Publication of the California Consumer Price Index (December 16, 2025)",
         pub="CA Dept. of Industrial Relations",
         url="https://www.dir.ca.gov/OPRL/CPI/12-16-2025(CCPI).htm",
         verifies="OFFICIAL EXPLANATION OF A DATA GAP: because of the federal government shutdown in fall 2025, BLS "
                  "could not collect October 2025 reference-period data and will not publish it; DIR therefore did not "
                  "publish the October 2025 California CPI. This is why the SF Rent Board's October-to-October AGA "
                  "methodology could not be run normally for the 2026-27 rate."),
    dict(id="S32", juris="State (CA)", method="ci",
         title="Ballot analysis - local rent control / Costa-Hawkins",
         pub="California Legislative Analyst's Office (lao.ca.gov)",
         url="https://lao.ca.gov/ballot/2022/220574.pdf",
         verifies="The non-partisan fiscal analyst's statement that California courts have held rent control must "
                  "allow landlords a FAIR RATE OF RETURN, and that local rent control cannot set what a landlord "
                  "charges a NEW renter (vacancy decontrol). Used as the policy anchor for 'reasonable'."),
    dict(id="S33", juris="State (CA)", method="fetched",
         title="Housing Discrimination (Fair Employment and Housing Act / California Civil Rights Act)",
         pub="California Civil Rights Department (calcivilrights.ca.gov)",
         url="https://calcivilrights.ca.gov/housing/",
         verifies="The complete list of California protected characteristics in housing (race, colour, ancestry, "
                  "national origin, citizenship, immigration status, primary language, religion, disability, sex and "
                  "gender, sexual orientation, gender identity, gender expression, genetic information, marital "
                  "status, familial status, source of income including a Section 8 voucher, military or veteran "
                  "status, age); protection for association and for perceived characteristics; examples of unlawful "
                  "conduct including RETALIATION; and the free CRD complaint process and remedies."),

    # ---- Federal ----
    dict(id="S34", juris="Federal", method="fetched",
         title="The Fair Housing Act",
         pub="U.S. Department of Justice, Civil Rights Division",
         url="https://www.justice.gov/crt/fair-housing-act-1",
         verifies="The Fair Housing Act, 42 U.S.C. Sec. 3601 et seq., prohibits discrimination by direct providers of "
                  "housing, such as LANDLORDS AND REAL ESTATE COMPANIES, on the basis of race or colour, religion, "
                  "sex, national origin, familial status or disability; individuals may file with HUD or sue in "
                  "federal or state court; DOJ brings pattern-or-practice cases. The page contains no federal rent "
                  "ceiling for private unsubsidised housing."),
    dict(id="S35", juris="Federal", method="ci",
         title="Fair Housing / equal opportunity - file a complaint",
         pub="U.S. Dept. of Housing and Urban Development",
         url="https://www.hud.gov/program_offices/fair_housing_equal_opp",
         verifies="The federal administrative route for a fair-housing complaint referenced by DOJ."),
    dict(id="S36", juris="Federal", method="ci",
         title="Fair Housing Act, 42 U.S.C. ch. 45 (Sec. 3601 et seq.) - statutory text",
         pub="U.S. House of Representatives, Office of the Law Revision Counsel",
         url="https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title42-chapter45&num=0&edition=prelim",
         verifies="The federal statutory text. Recorded to support the negative finding that no federal statute sets "
                  "a rent-increase ceiling for privately owned, unsubsidised residential housing."),

    # ---- Corporate / institutional practice ----
    dict(id="S37", juris="Practice", method="fetched",
         title="Essex Property Trust, Inc. Form 10-K for fiscal year 2025 (filed 2026-02-20, AccNo 0000920522-26-000003)",
         pub="U.S. Securities and Exchange Commission, EDGAR",
         url="https://www.sec.gov/Archives/edgar/data/920522/000092052226000003/0000920522-26-000003-index.htm",
         verifies="Primary SEC filing of a large institutional multifamily owner whose portfolio is concentrated in "
                  "Southern California, the San Francisco Bay Area and Seattle (SIC 6798, Real Estate Investment "
                  "Trusts; CIK 0000920522). Used as the documentary record of how a large corporate owner describes "
                  "rent setting and rent regulation."),
    dict(id="S38", juris="Practice", method="ci",
         title="Essex Property Trust, Inc. / Essex Portfolio LP Form 10-K for fiscal year 2017",
         pub="U.S. Securities and Exchange Commission, EDGAR",
         url="https://www.sec.gov/Archives/edgar/data/920522/000092052218000011/ess-123117x10k.htm",
         verifies="Risk-factor language quoted on the Corporate vs Individual page: rent control or stabilisation laws "
                  "'limit our ability to charge market rents, increase rents, evict tenants or recover increases in "
                  "our operating expenses'; 'substantially all of our apartment leases are for a term of one year or "
                  "less'; increases in real estate taxes 'cannot always be passed through to residents'."),
    dict(id="S40", juris="State (CA)", method="ci",
         title="Cal. Civil Code Sec. 51 - Unruh Civil Rights Act",
         pub="California Legislative Information (leginfo.legislature.ca.gov)",
         url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=51",
         verifies="The right to full and equal accommodations, advantages, facilities, privileges or services in all "
                  "business establishments of every kind whatsoever, regardless of the protected characteristics "
                  "enumerated. Recorded as a further California basis for challenging differential treatment."),
    dict(id="S39", juris="Practice", method="fetched",
         title="EDGAR company filing index - Essex Property Trust, Inc. (CIK 0000920522)",
         pub="U.S. Securities and Exchange Commission, EDGAR",
         url="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000920522&type=10-K&dateb=&owner=include&count=5&output=atom",
         verifies="The complete 10-K filing history for this filer (2017-2026), used to confirm the accession number "
                  "and filing date of the most recent annual report."),
]

SRC = {s["id"]: s for s in SOURCES}


def cite(*ids):
    """Render source citations as a compact linked list."""
    out = []
    for i in ids:
        s = SRC[i]
        tip = (s["title"] + " \u2014 " + s["pub"]).replace('"', "'")
        out.append(f'<a href="{s["url"]}" target="_blank" rel="noopener noreferrer" title="{tip}">{i}</a>')
    return '<span class="srclist">Source: ' + " &middot; ".join(out) + "</span>"


def badge(method):
    if method == "fetched":
        return '<span class="b ok">Verified &ndash; retrieved</span>'
    return '<span class="b info">Official URL &ndash; CI-checked</span>'


# --------------------------------------------------------------------------
# FLAG REGISTER  (published on pages/flagged.html)
# --------------------------------------------------------------------------
FLAGS = [
    dict(id="F1", sev="resolved", area="Repository",
         title="Repository contained no data, no analysis and no site",
         detail="At commit <code>dab56c9</code> the repository held a single file, <code>README.md</code>, containing "
                "one line (<code># RentincreaseSF3</code>) with no trailing newline. There was no data, no source "
                "list, no documentation and no web content. GitHub Pages was already enabled (legacy build, "
                "<code>main</code> branch, root path) but served nothing.",
         action="Resolved by task T10: the entire site was built from scratch and every value was sourced from an "
                "official publisher. Nothing was carried over from the prior state, so there was no legacy data to "
                "reconcile.",
         src=[]),
    dict(id="F2", sev="high", area="Source conflict",
         title="Third-party sites publish a 2026-27 San Francisco allowable increase of 1.7%; the official rate is 1.6%",
         detail="The SF Rent Board's own Current Rates page and document 571 both state <b>1.6%</b> for "
                "3/1/2026-2/28/2027 (and 1.4% for 3/1/2025-2/28/2026). At least one widely circulated third-party "
                "'SF rent control calculator' states the current AGA is <b>1.7%</b> for the same period while also "
                "stating the previous period was 1.4% - an internally inconsistent combination, since the official "
                "1.7% belongs to 3/1/2024-2/28/2025. Another third-party guide states the 2025-26 rate was 1.4% and "
                "separately that a 90-day notice applies 'for increases of 10% or more', whereas the statute sets the "
                "long-notice trigger at <i>greater than</i> 10%.",
         action="1.6% adopted throughout. No third-party figure is used anywhere on this site. If any document you "
                "hold shows 1.7% for the 2026-27 period, treat it as incorrect.",
         src=["S1", "S2", "S23"]),
    dict(id="F3", sev="high", area="Official source conflict",
         title="Two sf.gov pages state DIFFERENT banking maturity rules (12 months vs 24 months)",
         detail="The sf.gov page <i>Banked rent increases</i> states: 'A skipped increase is only banked if at least "
                "<b>24 full months</b> pass without any rent increase. If less than 24 months pass, the skipped "
                "increase is lost.' The sf.gov page <i>Learn about rent increases</i> states in its own worked "
                "example that a skipped increase failed to bank 'because a full <b>12 months</b> has not elapsed'. "
                "The <i>Banked rent increases</i> page then contradicts itself: its own worked example banks the "
                "1.7% that had been available for only 12 months (moved in 8/1/2022, first increase 8/1/2025, "
                "banking both 8/1/2023 at 3.6% and 8/1/2024 at 1.7%).",
         action="Resolved in favour of the <b>controlling regulation</b>: Rent Board Rules and Regulations "
                "Sec. 4.12(a), as published by the Rent Board on sf.gov, reads 'A full <b>12 months</b> must have "
                "elapsed from the date that an annual rent increase, or a portion thereof, could have been imposed "
                "before this banking section becomes applicable.' All calculations here use 12 months. The 24-month "
                "sentence appears to be an error on that page. <b>Because two official pages disagree, confirm the "
                "maturity rule with a Rent Board counselor (415-252-4600) before serving any banked-increase "
                "notice.</b> The calculator in this repository reproduces all four official worked examples exactly "
                "under the 12-month rule, which is strong corroboration.",
         src=["S4", "S5", "S3"]),
    dict(id="F4", sev="high", area="Compliance gate",
         title="Rent increase license status is UNKNOWN for both units - no increase is enforceable without it",
         detail="Under Rent Ordinance Sec. 37.15 and the Rent Board Housing Inventory rules, a current rent increase "
                "license must be on file on the EFFECTIVE DATE of the increase or the entire annual or banked "
                "increase is null and void, regardless of whether the arithmetic was correct. The license status of "
                "these two units was not supplied and is not published anywhere this project can read.",
         action="Left <b>blank</b> on the unit dossiers - not inferred. Before serving any notice: file or refresh "
                "the Housing Inventory at portal.sfrb.org (deadline March 1 each year, late filing is permitted and "
                "carries no monetary penalty) and confirm the license covers the effective date. Note the submitted "
                "information is PUBLIC and includes base rent in $250 increments.",
         src=["S8", "S9", "S6"]),
    dict(id="F5", sev="high", area="Source conflict",
         title="Two sf.gov documents give DIFFERENT operative dates for the Sec. 37.15 licensing requirement",
         detail="The Housing Inventory page states the requirement became operative <b>July 1, 2022</b> for non-condo "
                "buildings with 10 or more units, with reporting beginning <b>March 1, 2023</b> for condominiums and "
                "buildings with fewer than 10 units. An official Rent Board worksheet PDF (document 538) states the "
                "requirement applies to increases effective on or after <b>July 1, 2020</b> for buildings with ten or "
                "more residential units and on or after <b>March 1, 2021</b> for condominiums and buildings with "
                "fewer than ten units.",
         action="Both dates are published here; neither is used to compute anything, because the license is a "
                "present-tense gate that must be satisfied on the effective date of any future increase. Use the "
                "more recent Housing Inventory page for current filing obligations and confirm the historical dates "
                "with the Rent Board before relying on them in any audit of a past increase.",
         src=["S8", "S13"]),
    dict(id="F6", sev="high", area="Legal fact gap",
         title="Unit A had a change in occupants - whether a market-rate reset is available turns on facts not supplied",
         detail="Unit A's original tenancy (began 2025-02-01) had three tenants; the continuing tenancy from "
                "2026-04-01 has two, one of whom is an original tenant and one of whom is new. Two different legal "
                "routes could in principle permit a market-rate reset, and both are unavailable on the facts as "
                "stated: (i) Cal. Civ. Code Sec. 1954.53(d)(3) expressly does NOT apply 'to partial changes in "
                "occupancy... where one or more of the occupants... remains an occupant in lawful possession'; and "
                "(ii) Rules & Regs Sec. 6.14 permits an unlimited increase only when the LAST original occupant "
                "vacates AND a timely written 6.14 notice was served on each subsequent occupant. Whether the new "
                "occupant is a co-tenant (never subject to a Costa-Hawkins reset) or a subtenant, and whether any "
                "6.14 notice was ever served, were not supplied.",
         action="Analysed on the facts as stated: an original occupant remains, so NO market-rate reset is available "
                "and the lawful ceiling stays tied to the $3,995.00 base rent with a February 1 anniversary. The "
                "unresolved sub-questions are recorded here rather than assumed. <b>Do not serve a Sec. 6.14 or "
                "Costa-Hawkins notice on these facts without a written legal opinion.</b>",
         src=["S25", "S12", "S11", "S6"]),
    dict(id="F7", sev="medium", area="Missing input",
         title="Base rent composition was not supplied for either unit",
         detail="The increase must be computed on BASE RENT, which includes housing services such as parking and "
                "storage but EXCLUDES temporary passthroughs and fluctuating charges. Whether the $3,995.00 and "
                "$3,150.00 figures include parking, storage or any passthrough was not stated.",
         action="Left <b>blank</b>; the stated figures were used exactly as supplied and no component was inferred. "
                "If either figure contains a passthrough, the percentages must be re-applied to the corrected base "
                "rent before any notice is served.",
         src=["S3", "S16", "S5"]),
    dict(id="F8", sev="medium", area="Missing input",
         title="No record of prior increases, security-deposit interest or Rent Board fee payments was supplied",
         detail="The calculations assume no increase was ever imposed (Unit A: none since 2025-02-01; Unit B: none "
                "since 2019-06-01) because none was reported. Security-deposit interest must be paid annually "
                "(4.2% for 3/1/2026-2/28/2027) and the Rent Board fee ($59.00 per dwelling unit for 2026-2027) must "
                "be paid by March 1. Compliance with either was not evidenced.",
         action="Prior-increase history treated as EMPTY and flagged; deposit-interest and fee compliance left "
                "<b>blank</b>. A tenant representative will request all three. Assemble the complete rent history "
                "and the payment records before serving notice - the Rent Board can order a determination of lawful "
                "rent on Form 354 and the burden of proving the correct base rent falls on the owner.",
         src=["S1", "S10", "S14", "S18"]),
    dict(id="F9", sev="medium", area="Verification gap",
         title="The building's construction date is owner-reported, not verified against a public record",
         detail="Coverage under the Rent Ordinance turns on the building having been built on or before June 13, "
                "1979. 'Built in 1940' was supplied as a statement, not as a document. A 1940 building would be "
                "covered, but the project cannot verify the year from the material supplied.",
         action="Coverage is presented as PRESUMED, not verified. Confirm on the San Francisco Property Information "
                "Map and, if needed, obtain a Rent Board determination. Also confirm the unit is not separately "
                "alienable (a condominium or single-family dwelling), which would change the analysis under "
                "Sec. 1954.52(a)(3) and Sec. 37.3(d)(1)(A).",
         src=["S7", "S21", "S26"]),
    dict(id="F10", sev="medium", area="Not yet published",
         title="The allowable increase for 3/1/2027-2/28/2028 has not been published",
         detail="Unit B's recommended scenario takes effect 2027-06-01. The banked total of 13.1% is fully verified, "
                "but the annual increase in effect on that date belongs to the period beginning 3/1/2027, which the "
                "Rent Board had not published as of 2026-11-06 (it publishes on or about January 1 each year, "
                "effective March 1).",
         action="Left <b>blank</b> everywhere and never forecast. Unit B's total is published as "
                "'13.1% + [unpublished]'. Re-run <code>python3 tools/calc.py</code> after the Rent Board publishes "
                "the 2027-28 rate and update the AGA table in <code>tools/rentcalc.py</code>.",
         src=["S2", "S1"]),
    dict(id="F11", sev="medium", area="Official document error",
         title="An official Rent Board worked example mislabels which year's rate it is applying",
         detail="On <i>Learn about rent increases</i>, the example 'RENT INCREASE FOR ONE YEAR ON ANNIVERSARY DATE' "
                "says a tenant who moved in 2025-06-01 and is increased on 2026-06-01 gets 'the annual allowable "
                "increase in effect on <b>June 1, 2025</b> is 1.6%'. Per document 571 the rate in effect on "
                "2025-06-01 was 1.4%; the 1.6% rate was in effect on 2026-06-01. The example's RESULT ($1,016.00) is "
                "correct if the rate in effect on the EFFECTIVE date is used, which is also what the same page "
                "instructs ('use the percentage that will be in effect on the date of the increase').",
         action="The engine applies the rate in effect on the EFFECTIVE date and reproduces the official result "
                "($1,016.00) exactly. The mislabelled year is recorded here for transparency; it does not change any "
                "figure published on this site.",
         src=["S3", "S2"]),
    dict(id="F12", sev="medium", area="Federal source unavailable",
         title="The FHFA GSE rent-increase notice requirement could not be confirmed on fhfa.gov",
         detail="Secondary reporting states that FHFA announced on 2024-07-12 that, for new multifamily loans signed "
                "on or after 2025-02-28, Fannie Mae and Freddie Mac loan documents would require a 30-day written "
                "notice of any rent increase, a 30-day notice of lease expiration and a 5-day grace period for late "
                "rent; that implementation was paused to 2025-05-31; and that FHFA then rescinded the directives in "
                "March 2025. Neither the announcement nor the rescission could be confirmed: the fhfa.gov newsroom "
                "URLs returned 'Page Not Found' on 2026-11-06.",
         action="The FHFA item is published as <b>UNVERIFIED</b> and is NOT relied on anywhere in the analysis. It is "
                "immaterial to these two units, which are governed by the San Francisco Rent Ordinance; it would only "
                "matter if the property carried an Enterprise-backed multifamily loan. Confirm the current status "
                "directly with FHFA before relying on it.",
         src=[]),
    dict(id="F13", sev="low", area="Verification gap",
         title="No federal statute sets a rent-increase ceiling for private unsubsidised housing - a negative finding",
         detail="The federal maximum allowable rent increase is left BLANK. This is a negative finding: the Fair "
                "Housing Act (42 U.S.C. Sec. 3601 et seq.) regulates the MANNER in which rent may be set, not its "
                "amount, and federal rent limits attach only to federally assisted housing (for example Section 8 "
                "and HUD-insured programmes) or to programme-specific rules. A negative finding cannot be proved by "
                "citing a document that states it.",
         action="Published as 'No federal ceiling - not applicable', with the Fair Housing Act cited for what federal "
                "law DOES require. Recorded here so the blank cell is understood as deliberate, not as an omission.",
         src=["S34", "S35", "S36"]),
    dict(id="F14", sev="low", area="Privacy control",
         title="All personal information has been removed from the published record",
         detail="Tenant names, unit designations and any identifying detail were supplied for analysis. Publishing "
                "them would defeat the stated privacy requirement, and the Housing Inventory data an owner files with "
                "the Rent Board is itself PUBLIC.",
         action="Unit 1 is published as <b>Unit A</b> and Unit 2 as <b>Unit B</b>. Tenants are published as "
                "pseudonymous identifiers (T-A1 to T-A4, T-B1 to T-B2) with the original-to-current mapping shown "
                "only as role changes, never as names. All dates and all dollar amounts are preserved EXACTLY as "
                "supplied. No street address was supplied and none is published; location is given only as "
                "'San Francisco, CA 94122 (Outer Sunset)'. The mapping between pseudonyms and real identities is "
                "held by the owner and appears nowhere in this repository.",
         src=["S8"]),
    dict(id="F15", sev="low", area="Scope limit",
         title="Sec. 37.8 refund look-back period could not be read from the official compiled ordinance",
         detail="The compiled Chapter 37 PDF published on sf.gov is long, and only its first pages could be parsed "
                "for this project. The table of contents confirms Sec. 37.8 (Arbitration of Rental Increase "
                "Adjustments) exists, and Sec. 37.3(b)(5) ('Nonconforming Rent Increases... shall be null and void') "
                "was read directly. The specific length of the refund look-back an Administrative Law Judge may order "
                "for a null-and-void increase was NOT read from the official text and is therefore not published.",
         action="The exposure is described qualitatively (a non-conforming increase is null and void and overpayments "
                "may be ordered refunded or offset) with no period stated. Obtain the full Sec. 37.8 text before "
                "quantifying look-back exposure.",
         src=["S6"]),
]

# --------------------------------------------------------------------------
# NAVIGATION
# --------------------------------------------------------------------------
NAV = [
    ("Overview", [
        ("index.html", "Dashboard", "root"),
        ("pages/executive-summary.html", "Executive Summary", "sub"),
        ("pages/methodology.html", "Methodology & Verification", "sub"),
    ]),
    ("Governing law", [
        ("pages/law-local.html", "San Francisco (local)", "sub"),
        ("pages/law-state.html", "California (state)", "sub"),
        ("pages/law-federal.html", "Federal", "sub"),
    ]),
    ("Data & findings", [
        ("pages/rates.html", "Official rates & CPI", "sub"),
        ("pages/units.html", "Unit dossiers", "sub"),
        ("pages/scenarios.html", "Increase scenarios", "sub"),
    ]),
    ("Practice & risk", [
        ("pages/notice-guide.html", "Notice procedure & reasons", "sub"),
        ("pages/practices.html", "Corporate vs individual", "sub"),
        ("pages/fair-housing.html", "One unit or both?", "sub"),
        ("pages/red-team.html", "Tenant-advocate red team", "sub"),
    ]),
    ("Assurance", [
        ("pages/sources.html", "Source register", "sub"),
        ("pages/flagged.html", "Flagged for review", "sub"),
        ("pages/audit.html", "Repo audit & log", "sub"),
    ]),
]
