# Verification log

Date of verification: **2026-11-06**. Method: every figure and rule used on the site was fetched from a
government source during this session, read directly, and then cross-checked against at least one
independent official source where one exists. The quoted passage for each source is reproduced in
`source-register.md` and on `sources.html`.

## Line-by-line checks

| # | Assertion on the site | How it was verified | Result |
|---|---|---|---|
| 1 | Annual allowable increase is 1.6% for 3/1/2026–2/28/2027 | Rent Board news release; Rent Board "Current Rates" page; Rent Board "Learn about rent increases" page; document 571 | Consistent across four official pages |
| 2 | Prior year was 1.4% (3/1/2025–2/28/2026) | Same four pages | Consistent |
| 3 | Historical rates 2019–2024 (2.6, 1.8, 0.7, 2.3, 3.6, 1.7) | Document 571 (complete 1982–2027 table) | Read from the official table, not memory |
| 4 | Formula is 60% of prior-year Bay Area CPI, capped at 7% | Ordinance §37.3(a)(1) text; Rent Board page; Attorney General local-cap chart | Consistent |
| 5 | San Francisco's cap displaces AB 1482 | Civil Code §1947.12(d)(3) text; Attorney General chart (state 8.8% vs local 1.6%) | Consistent |
| 6 | Coverage threshold is 13 June 1979 | Rent Board "Learn about San Francisco rental laws"; Attorney General chart | Consistent |
| 7 | Vacancy decontrol requires that no prior tenant remains | Civil Code §1947.12(b); Costa-Hawkins §1954.52; ordinance §37.3(d) | Consistent |
| 8 | Additional occupants cannot generate rent | Rent Board "Learn about rent increases" (plain language); ordinance §37.3(a)(11) (ordinance PDF) | Consistent |
| 9 | 12-month rule and anniversary-date definition | Rent Board "Learn about rent increases"; "Increasing rents during irregular periods" | Consistent |
| 10 | Banked increases: 24-month condition, no cap, no expiry, partial increases | Rent Board "Banked rent increases" page; "irregular periods" page; Rule 4.12 | **Conflict**: Rule 4.12(a) still reads 12 months. Logged as F1 |
| 11 | Multi-year increases are added, not compounded, and not rounded | Rent Board "Annual rent increase for multiple years"; "Banked rent increases"; Rule 4.12(a) | Consistent |
| 12 | Rent increase licence required; licence must exist on the effective date | Rent Board Housing Inventory page; "Learn about rent increases" | Consistent |
| 13 | Notice: 30 days for ≤10%, 90 days for >10%, +5 if mailed | Civil Code §827(b)(2)–(3); Rent Board pages; Rule 4.10 | Consistent |
| 14 | Notice must break out annual vs banked and the banked dates | Ordinance §37.3(b); Rule 4.10(a); Rule 4.12(b); Rent Board "Banked rent increases" | Consistent |
| 15 | Tenant may petition at no cost, with no time limit; harassment/discrimination not adjudicated there | Rent Board "Tenant Petitions"; "Report an unlawful rent increase" | Consistent |
| 16 | Tenant right to counsel / free legal help | Rent Board "Evictions in San Francisco"; Rent Board Form 1007 text | Consistent |
| 17 | Retaliation prohibited, 180-day presumption | Civil Code §1942.5(a) | Verified from statute |
| 18 | Protected characteristics | Gov. Code §12955(a); 42 U.S.C. §3604(b) | Verified from statute |
| 19 | Algorithmic rent-setting devices banned in SF | Rent Board news release (Ordinance §37.10C, effective 14 Oct 2024) | Verified |
| 20 | Federal antitrust enforcement over algorithmic pricing | DOJ press release, 24 Nov 2025 | Verified |
| 21 | 10% cap on banked + capital-improvement increases is pending, not law | Legistar File 261020 (introduced 9/15/2026, status "30 Day Rule") | Verified as pending only; logged as F3 |
| 22 | Unit A arithmetic: 1.4% + 1.6% = 3.0%; $3,995 × 3.0% = $119.85 | Recomputed by hand and in Python; matches the Rent Board's own multi-year method | Verified |
| 23 | Unit B arithmetic: 13.1%; $3,150 × 13.1% = $412.65 | Recomputed by hand and in Python; cross-checked against the Board's 6.7% worked example method | Verified |
| 24 | Notice deadlines (2 Jan 2027 / 28 Dec 2026 / 30 Nov 2026 / 25 Nov 2026) | Date arithmetic in Python, applying 30/35 and 90/95 day periods | Recomputed |
| 25 | Market rent for the property's ZIP (withheld) | HUD FMR lookup and Census API returned no usable official figure during the session | **Not verified — left blank (F9)** |
| 26 | Year built 1940, two units | Owner statement only | **Not verified (F6)** |
| 27 | Prior rent history for both units | Owner statement only | **Not verified (F5)** |

## Re-check procedure before serving a notice

1. Re-read the Rent Board's current-rate page and document 571 (the rate changes every 1 March).
2. Re-read Legistar File 261020 for enactment status.
3. Confirm the licence is live in the Rent Board portal on the date the increase takes effect.
4. Recompute the increase in cents; confirm no compounding and no rounding.
5. Confirm the notice period against Civil Code §827 for the total increase actually being served.

## Automated checks

`tools/check_site.py` verifies that every internal link and anchor resolves, that every external link is
https, that each data-table row carries at least one source chip, and that no placeholder text remains.
Output at publish time: 11 pages, 1 external link (SEC EDGAR, provided for manual review only), 0 broken
internal links or anchors, 0 rows without a source chip.

---

# Session `arena/76fd1699` — re-fetch pass, 2026-11-10

Method: every load-bearing source was fetched again on 10 November 2026 and the quoted wording was
compared with what the published pages say. Only sources actually re-read in this pass are listed;
nothing was carried over from memory or from an earlier session's notes.

| # | Source re-fetched (10 Nov 2026) | Wording confirmed in this pass | Affects |
|---|---|---|---|
| 1 | [Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) | "All owners of residential property are required to report"; licence generated automatically; deadline 1 March; "will not be enforceable without having a rent increase license on the effective date of the notice"; 1 March 2023 start for 1–9 unit buildings | Dashboard Q&A, process step 2–3, exec summary §1 |
| 2 | [Notice of Owner Noncompliance](https://www.sf.gov/notice-of-owner-noncompliance-with-housing-inventory) | "may be null and void (this may apply for multiple years)"; tenant "may be entitled to a rent refund"; Tenant Summary Petition while the increase has not taken effect; licence look-up in the Portal | **New** — closes FR-16; strengthens dashboard, exec summary, process page |
| 3 | [Learn about rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) | 1.6% for 1 Mar 2026 – 28 Feb 2027; 9 Nov 2026 notice on File #261020; 30/90-day notice; use the percentage in effect on the effective date; no rounding; additional-occupant prohibition; "no limit on how much rent a landlord may first charge" | Whole site; pending-law section |
| 4 | [Banked rent increases](https://www.sf.gov/information--banked-rent-increases) | 24-full-month condition; no cap since 1 Apr 1982; no expiry; added, not compounded; notice must say "which part of the increase is banked" | Units page, FR-03 |
| 5 | [Annual rent increase for multiple years](https://www.sf.gov/information--annual-rent-increase-multiple-years) | Additive method; no petition; no rounding; base rent only; "35-days if sent by mail" (= 30 + 5) | Units page, notice page |
| 6 | [Form 571 (PDF)](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) | Full table 4/1/82–2/28/27: 2020 1.8, 2021 0.7, 2022 2.3, 2023 3.6, 2024 1.7, 2025 1.4, 2026 1.6 | Every percentage on the site |
| 7 | [Learn about SF rental laws](https://www.sf.gov/learn-about-san-francisco-rental-laws) | 13 June 1979 coverage line; single-family/condo partial exemption; counsellor 415-252-4600 | Coverage row, footer |
| 8 | [Tenant Petitions](https://www.sf.gov/tenant-petitions) | Free filing; unlawful-rent-increase petition; **Tenant Summary Petition based on receipt of an invalid notice**; Board does not adjudicate harassment, discrimination or retaliation | Review page (new row), discrimination page |
| 9 | [Civ. Code § 827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) | 30 days if ≤10% of "the rental amount charged … at any time during the 12 months before the effective date"; 90 days if more; §1013 applies to mailed service | Notice page, planner |
| 10 | [Civ. Code § 1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) | (d)(3) exempts housing under local rent control that "restricts annual increases … to an amount less than" the state formula | State-law layer |
| 11 | [Attorney General — rent caps](https://oag.ca.gov/rentcaps) | San Francisco area 8.8% for increases starting 8/1/26–7/31/27; local cap governs where lower | State-law layer |
| 12 | [Legistar File #261020](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770) | Status **Pending Committee Action**; introduced 9/15/2026; history shows referral and Youth Commission response only, no final action | Pending-law section, FR-06 |

Arithmetic re-run in this pass (cents): 3,995 × 1.6% = 63.92 → 4,058.92; 3,995 × 3.0% = 119.85 →
4,114.85; 3,150 × 1.6% = 50.40 → 3,200.40; 3,150 × 11.5% = 362.25 → 3,512.25; 3,150 × 13.1% =
412.65 → 3,562.65. Banked sums re-added from the official table: 1.8+0.7+2.3+3.6+1.7+1.4 = 11.5;
11.5 + 1.6 = 13.1.

Two corrections resulted: FR-16 (the stronger noncompliance wording is now quoted, closing the scope
limit) and FR-17 (13.1% is the maximum only for an effective date on or before 28 February 2027, and
a blank row now records that the 2027–28 percentage is unpublished).
# Re-verification pass — 2026-11-10

Session `arena/45eea2b7-rentincreasesf3`. The canonical site (index.html + pages/) and the
verification edition were re-read line by line against official sources fetched again today. Every
headline figure below was fetched from the linked source on 2026-11-10 and matched the published text.

| # | Assertion on the site | Source fetched 2026-11-10 | Result |
|---|---|---|---|
| 28 | Annual allowable increase 1.6% for 3/1/2026–2/28/2027 | sf.gov — Learn about rent increases; Form 571 PDF | Match |
| 29 | Prior-year rates 1.4% (25–26), 1.7% (24–25), 3.6% (23–24), 2.3% (22–23), 0.7% (21–22), 1.8% (20–21) | Form 571 PDF rate table | Match (Unit B banked arithmetic 1.8+0.7+2.3+3.6+1.7+1.4+1.6 = 13.1%) |
| 30 | Banking: additive not compounded, no cap back to 1 Apr 1982, no expiry during tenancy, no carry-over to a new tenant, notice must state the banked part | sf.gov — Banked rent increases | Match |
| 31 | Rent-increase licence: report into the Housing Inventory; licence auto-generated for non-owner-occupied units; must be in effect on the effective date or the increase is not enforceable; 1 March deadline; no monetary penalty for late filing; requirement applies to 1–9 unit buildings from 1 March 2023 | sf.gov — Housing Inventory | Match |
| 32 | Notice: 30 days ≤10%, 90 days >10%, +5 if mailed; percentage in effect on the effective date | Civ. Code § 827 (leginfo) | Match |
| 33 | File #261020: caps banked + capital-improvement increases at 10%/yr for three years; status "Pending Committee Action"; introduced 9/15/2026; Land Use and Transportation Committee | sfgov.legistar.com | Match; sf.gov 9 Nov 2026 notice confirms it is not enacted and would apply to banked increases noticed on or after 15 Sep 2026 |
| 34 | Unit B 13.1% = banked balance to 1 Jun 2026; floor, not the June 2027 ceiling (2027–28 allowance unpublished) | Form 571 PDF + sf.gov — rent increases | Match; canonical pages/units.html row relabelled accordingly |
| 35 | Unit A 1.4% bankable on either official reading of the banking rule (24-month page rule vs 12-month worked example); 3.0% = 1.6% + 1.4% supportable | Form 571 PDF; sf.gov — Banked rent increases | Match; conflict already published as FR-03 |

Gates re-run 2026-11-10 after the edits: `tools/verify_core_site.py` (14 pages, 41 tables, 329 rows,
920 links) ALL CHECKS PASSED; `tools/check_v2.py` (verification edition, 212 rows) ALL CHECKS PASSED;
`verify_site.py`, `tools/check_site.py`, `tools/verify_edition.py`, `tools/audit_site.py`,
`tools/privacy_scan.py` all pass. Both builders are idempotent (fresh rebuild produces no further
changes). `tools/check_v2.py` was added to the CI workflow (it existed but was not wired in).

Irregularities found in this pass: none new. Prior flags (FR-01..FR-16, F-1..F-23) remain open and
published on the flagged pages; they do not block the merge.
