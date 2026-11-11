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
| 34 | Unit B 13.1% = banked balance to 1 Jun 2026; floor, not the June 2027 ceiling (2027–28 allowance unpublished) | Form 571 PDF + sf.gov — rent increases | Match; canonical pages/units.html row relabelled by PR #27 as "Combined for an effective date on or before 28 Feb 2027" + blank 2027–28 row (adopted on rebase; the same correction) |
| 35 | Unit A 1.4% bankable on either official reading of the banking rule (24-month page rule vs 12-month worked example); 3.0% = 1.6% + 1.4% supportable | Form 571 PDF; sf.gov — Banked rent increases | Match; conflict already published as FR-03 |

Gates re-run 2026-11-10 after the edits: `tools/verify_core_site.py` (14 pages, 41 tables, 329 rows,
920 links) ALL CHECKS PASSED; `tools/check_v2.py` (verification edition, 212 rows) ALL CHECKS PASSED;
`verify_site.py`, `tools/check_site.py`, `tools/verify_edition.py`, `tools/audit_site.py`,
`tools/privacy_scan.py` all pass. Both builders are idempotent (fresh rebuild produces no further
changes). `tools/check_v2.py` was added to the CI workflow (it existed but was not wired in).

Irregularities found in this pass: none new. Prior flags (FR-01..FR-16, F-1..F-23) remain open and
published on the flagged pages; they do not block the merge.

---

# Re-verification pass — 2026-11-11

Session `arena/e00aaa27-rentincreasesf3`. Every source in the canonical 28-source register was fetched again on 11 November 2026 and compared with the published text. All headline figures matched; the only change required was the notice-date planner (one day later, the first reachable >10% date moves from 8 Feb to 9 Feb 2027). 11 November is Veterans Day — sf.gov carried a "City offices will be closed on Wednesday, November 11" banner — so no Rent Board counselling was available that day; nothing on the site depends on a same-day call.

| # | Assertion on the site | Source fetched 2026-11-11 | Result |
|---|---|---|---|
| 36 | Rent-increase licence: all owners must report into the Housing Inventory; licence auto-generated for tenant-occupied units; must be in effect on the effective date or the notice is not enforceable; 1 March deadline; no monetary penalty for late filing; 1–9 unit buildings from 1 March 2023; individuals covered the same as corporations | sf.gov — The Rent Board Housing Inventory; Rent Board Portal (portal.sfrb.org) | Match — Portal confirms "Obtain a License to increase rents for tenants covered by Rent Control" |
| 37 | Unlicensed increase "may be null and void (this may apply for multiple years)"; tenant "may be entitled to a rent refund"; Form 516C / Form 518 routes; paper filing fallback | sf.gov — Notice of Owner Noncompliance with Housing Inventory | Match |
| 38 | Annual allowable increase 1.6% for 3/1/2026–2/28/2027 (60% of Bay Area CPI); base rent only; no rounding up; anniversary rules; additional-occupant ban; 9 Nov 2026 File #261020 notice | sf.gov — Learn about rent increases (both chunks, incl. the 12-month-test worked example) | Match — FR-03 wording conflict with the banking page persists, still published |
| 39 | Full 1982–2027 rate table; Unit B banked sum 1.8+0.7+2.3+3.6+1.7+1.4 = 11.5%; +1.6% = 13.1% | Form 571 PDF (sf.gov document 34344) | Match — recomputed: $3,995×1.6%=$63.92→$4,058.92; $3,995×3.0%=$119.85→$4,114.85; $3,150×10%=$315.00→$3,465.00; $3,150×11.5%=$362.25→$3,512.25; $3,150×13.1%=$412.65→$3,562.65 |
| 40 | Banking: 24-full-month condition, additive not compounded, no cap back to 1 Apr 1982, no expiry, prior-owner transfer, no carry-over to a new tenant, notice must state the banked part; multi-year increases need no petition | sf.gov — Banked rent increases; sf.gov — Annual rent increase for multiple years | Match |
| 41 | Coverage: units built on or before 13 June 1979 generally have rent control + eviction protection; counsellor 415-252-4600 | sf.gov — Learn about San Francisco rental laws | Match (1940 building presumptively covered; building record itself remains owner-reported, FR-flagged) |
| 42 | Notice: 30 days if ≤10%, 90 days if >10% of rent charged at any time in prior 12 months, alone or combined; personal delivery or mail | Cal. Civ. Code § 827 (leginfo) | Match |
| 43 | Mail adds 5 days in California (10 out of state, 20 outside US, 2 court days overnight) | Cal. Code Civ. Proc. § 1013 (leginfo) | Match |
| 44 | AB 1482 cap 5%+CPI max 10%; local-ordinance exemption §1947.12(d)(3); SF-area maximum 8.8% for increases starting 8/1/26–7/31/27; local 1.6% governs | Cal. Civ. Code § 1947.12 (leginfo); oag.ca.gov/rentcaps | Match |
| 45 | Costa-Hawkins initial rent for a new tenancy; §6.14 unlimited increase only after last original occupant vacates, never against a co-tenant | Cal. Civ. Code § 1954.53 (leginfo); sf.gov — §6.14 and Costa-Hawkins | Match |
| 46 | Retaliation bar 180 days; tenant-organising protection | Cal. Civ. Code § 1942.5 (leginfo) | Match |
| 47 | FEHA protected characteristics; CRD housing enforcement; federal Fair Housing Act §3604 (no federal rent ceiling) | Cal. Gov. Code § 12955 (leginfo); calcivilrights.ca.gov/housing; 42 U.S.C. § 3604 (govinfo) | Match |
| 48 | Tenant petitions free, no filing deadline, ALJ hearing, no lawyer needed; Rent Board does not adjudicate discrimination/harassment/retaliation; landlord petitions before notice; long-standing below-market rent is not an extraordinary circumstance; algorithmic devices banned (§37.10C, 14 Oct 2024); DOJ suit against six large landlords (7 Jan 2025) | sf.gov — Tenant petitions; sf.gov — Report an unlawful rent increase; sf.gov — Landlord petitions and passthroughs; sf.gov — Special circumstances petitions; sf.gov — algorithmic devices news; justice.gov press release 25-21 | Match |
| 49 | Admin. Code §37.3 (60% of CPI, 7% formula cap, banking, licence) | codelibrary.amlegal.com §37.3 (2026 S-96 current) | Match |
| 50 | File #261020: 10%/yr cap on banked + capital-improvement increases for three years; status Pending Committee Action; introduced 9/15/2026; Land Use and Transportation Committee; no final action | sfgov.legistar.com File #261020 | Match — unchanged since 10 Nov; still not law |
| 51 | Rent Board Fee separate from licence: $59.00/dwelling unit 2026–27, due 1 March, 5%/mo penalty capped 15%, 50% ($29.50) recoverable, exemption deadline 14 Dec 2026 | sf.gov — The Rent Board Fee | Match |
| 52 | Notice-date planner from 11 Nov 2026: earliest >10% effective date 9 Feb 2027 (serve by 11 Nov, mail by 6 Nov — passed); 15 Feb 2027 serve by 17 Nov / mail by 12 Nov; 1 Feb 2027 ≤10% serve by 2 Jan 2027 / mail by 28 Dec 2026 | Date arithmetic recomputed in Python from Civ. Code §827 + CCP §1013 lead times | Updated — canonical planner, EXECUTIVE_SUMMARY.md and verify_core_site.py assertions rolled forward one day |

Irregularities found in this pass: (1) the 10 Nov planner's "first date reachable" row expired at end of 10 Nov — fixed by the roll-forward above; (2) open PRs #35 (stray-text fix already landed on main via PR #34 — redundant), #33 (strict-reading banking rows — substantive alternative published as FR-03 context, not merged here), #20 (superseded by PR #21 rebuild) remain open and untouched, belonging to other sessions; (3) no new substantive irregularity — all rates, the licence rule and the pending-ordinance status are unchanged.

---

# Independent confirmation pass — 2026-11-11

Session `arena/8f87abd1-rentincreasesf3`. Branch == `main` at `5c976c4` (PR #36 merged 2026-11-10T06:10:15Z).
This pass changed **no canonical content and no published figure**. It re-ran every automated gate on the
merged tree, corroborated the headline facts against public web results (this sandbox's egress is limited
to github.com / api.github.com / codeload.github.com / npm and PyPI hosts, so sf.gov and leginfo cannot be
fetched from here — the 2026-11-10 direct fetches recorded above remain the official-source record), and
reviewed the open pull requests.

| # | Assertion | Check performed 2026-11-11 | Result |
|---|---|---|---|
| 53 | Allowable increase 1.6% for 3/1/2026–2/28/2027 (prior year 1.4%) | Web search corroboration (multiple independent secondary outlets + the Rent Board announcement referenced in them); matches Form 571 figures published on the site | Consistent |
| 54 | AB 1482 San Francisco area cap 8.8% for increases starting 1 Aug 2026 – 31 Jul 2027; local cap governs where lower | Web search corroboration | Consistent |
| 55 | Rent Board licence: all owners must report into the Housing Inventory; licence auto-generated for tenant-occupied units; must be in effect on the effective date or the increase is not enforceable; 1–9 unit buildings since 1 Mar 2023 | Web search corroboration; matches sf.gov pages re-fetched directly 2026-11-10 (Verification log, rows 28–35) | Consistent |
| 56 | sf.gov notice posted 2026-11-09 — File #261020, ≤10%/yr combined banked + capital-improvement increases, not enacted, would apply to banked increases noticed on/after 2026-09-15, status Pending Committee Action | Web search corroboration (notice reproduced by multiple outlets; Legistar unchanged per 2026-11-10 direct read); matches site treatment | Consistent |
| 57 | Canonical site build is idempotent; all 7 gates pass on the merged tree | `privacy_scan.py` PASS (107 files); `build_dashboard.py` fresh (no diff); `verify_core_site.py` PASS (14 pages / 41 tables / 341 rows / 976 links); `audit_site.py` PASS (70 files); `verify_site.py`, `tools/check_site.py`, `tools/verify_edition.py`, `tools/check_v2.py` PASS | PASS |
| 58 | Live deployment of `5c976c4` | GitHub Pages build status checked via API (see PR record in COORDINATION.md); sandbox cannot fetch github.io directly (egress allowlist) | See deploy record |

Arithmetic independently recomputed from the published percentages (unchanged): 3,995.00 × 1.6% = 63.92 →
4,058.92; 3,995.00 × 3.0% = 119.85 → 4,114.85; 3,150.00 × 1.6% = 50.40 → 3,200.40; 3,150.00 × 11.5% =
362.25 → 3,512.25; 3,150.00 × 13.1% = 412.65 → 3,562.65; 3,150.00 × 10.0% = 315.00 → 3,465.00. Banked sums:
1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 = 11.5; 11.5 + 1.6 = 13.1. All match the published pages.

Irregularities found in this pass: one stale metadata field — `data/sources.json` `branch` named a merged
branch (`arena/487d8c3e-rentincreasesf3`); corrected to `main`. No content, percentage, dollar amount, date
or source URL was changed. Open pull requests reviewed and **not merged** (see COORDINATION.md session
section): #1 and #8 (superseded first editions), #20 (substance already on `main`; only a `data/sources.json`
addition outstanding, owner to rebase), #33 (overlaps FR-17 corrections merged in PRs #27/#34 — needs owner
rebase onto `main`), #35 (stray-text fix; stray text is absent from `main` — superseded by PR #34).

### Independent confirmation — session `arena/0dea38fc` (2026-11-11)

| # | Assertion | Check | Result |
|---|---|---|---|
| 59 | All 7 gates pass on merged tree | privacy_scan PASS; verify_core PASS (14 pages/41 tables/350 rows/988 links); audit PASS (70 files); verify_site, check_site, verify_edition, check_v2 PASS | PASS |
| 60 | Headline arithmetic | 3995×1.016=4058.92; 3995×1.03=4114.85; 3150×1.10=3465.00; 3150×1.131=3562.65 (recomputed) | Consistent |
| 61 | 1.6% (2026-27), licence requirement incl. individual 1-9 unit owners, §827 30/90-day, AB 1482 8.8% SF-area | Web-search corroboration against sf.gov/leginfo/oag reporting 2026-11-11; matches direct fetches by prior sessions | Consistent |

No content changes; flagged items FR-01…FR-25 remain published and non-blocking.

---

## Direct re-fetch pass — 2026-11-11, session `arena/beba4d31-rentincreasesf3`

Method: this sandbox has live egress to sf.gov, leginfo.legislature.ca.gov, oag.ca.gov, govinfo.gov,
justice.gov, codelibrary.amlegal.com and sfgov.legistar.com, so every headline source was fetched and read
in full again (not paraphrased from a search result). Rows 62–77.

| # | Assertion on the site | Source fetched and read in this pass | Result |
|---|---|---|---|
| 62 | Allowable increase **1.6%** for 3/1/2026–2/28/2027; prior year **1.4%**; formula 60% of Bay Area CPI | `sf.gov/learn-about-rent-increases-san-francisco` ("The allowed rent increase percentage in San Francisco is 1.6%. The percentage is effective March 1, 2026 through February 28, 2027.") | Confirmed verbatim |
| 63 | Complete rate table 1982–2027, 46 rows | Document **571** PDF (`sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf`), full table parsed | **5 row end-dates were wrong and the 12/8/92 row was missing** → corrected, FR-26. All percentages were already correct |
| 64 | Notice 30 days ≤10%, 90 days >10%, combined with other increases in the prior 12 months | Civ. Code § 827(b)(2)–(3) full text | Confirmed verbatim |
| 65 | +5 calendar days for mail within California; 10 outside; 2 court days overnight; mailed copy needs a date/place notation | CCP § 1013(a)–(d) full text | Confirmed verbatim |
| 66 | Banking: 24-full-month condition on the banked-increases page; no limit; no expiry; not compounded; not prorated; partial increases bankable; no carry-over to a new tenant | `sf.gov/information--banked-rent-increases` | Confirmed verbatim; the 12-month wording of Rule 4.12(a) also still stands → FR-03 remains an open irregularity |
| 67 | Rule 4.12(b): the banked portion and its dates must be given, and failure "shall not render the increase null and void" | Rent Board Rules Part IV (Rule 4.10 and Rule 4.12) on sf.gov | Confirmed verbatim |
| 68 | Licence: all owners must report; licence auto-generated for tenant-occupied units; must be in effect **on the effective date**; 1 March annual deadline; no monetary penalty; reporting is free; licence need not accompany the notice | `sf.gov/rent-board-housing-inventory` | Confirmed verbatim |
| 69 | Unlicensed notice "may be null and void (this may apply for multiple years)"; tenant "may be entitled to a rent refund"; Forms 516C / 518 | `sf.gov/notice-of-owner-noncompliance-with-housing-inventory` | Confirmed verbatim |
| 70 | Rent Board Fee is separate: **$59.00** per dwelling unit 2026-27, due 1 March, 5% monthly penalty capped at 15%, 50% = **$29.50** recoverable, 2027 exemption window closes **14 December 2026** | `sf.gov/rent-board-fee` | Confirmed verbatim |
| 71 | No petition for ordinary annual/banked increases; six petition types listed | Form 571 ("without filing a petition at the Rent Board") and `sf.gov/landlord-petitions-and-passthroughs` | Confirmed |
| 72 | § 37.3(a)(1) 60%-of-CPI formula with a 7% ceiling and the § 37.15 licence condition; (a)(2) banking since 1 April 1982; (a)(8) petition above the allowance; (a)(10) voucher rules; (a)(11)(A)–(C) additional occupants; (b)(1)–(5) notice breakdown and null-and-void rule; (d)(2)(B) partial-occupancy carve-out | San Francisco Administrative Code § 37.3, full section text (American Legal) | Confirmed; subsection numbering matches the site |
| 73 | § 6.14 / Costa-Hawkins: unlimited increase only when the **last** original occupant vacates; a co-tenant is never subject to it; 6.14 notice "generally sixty days is considered reasonable" | `sf.gov/information--rent-increases-under-section-614-and-costa-hawkins` | Confirmed; the site's partial-occupancy conclusion is consistent |
| 74 | Special-circumstances petition: "The mere fact that a long-standing tenant is paying significantly less than market rent is not considered an extraordinary circumstance" | `sf.gov/information/topic-no-323-...` (served this pass from `.../information--special-circumstances-petitions-based-rents-comparable-units`) | Confirmed verbatim |
| 75 | AB 1482 cap **8.8%** for the San Francisco area from 1 Aug 2026; local cap controls where lower (§ 1947.12(d)(3)); new-tenancy initial rate allowed (§ 1947.12(b)) | `oag.ca.gov/rentcaps` table and Civ. Code § 1947.12 full text | Confirmed verbatim |
| 76 | FEHA protected characteristics (incl. source of income, gender identity/expression, military status, genetic information) and FHA § 3604(b) terms-and-conditions language | Gov. Code § 12955 full text; 42 U.S.C. § 3604 (govinfo, U.S. Code 2023) | Confirmed verbatim |
| 77 | File #261020: introduced 9/15/2026, "Pending Committee Action", 10%/yr combined banked + capital-improvement cap for three years; Rent Board posted a 9 Nov 2026 notice that it "has not been enacted and is subject to change" | `sfgov.legistar.com` File #261020 detail page; both Rent Board pages | Confirmed verbatim |

Also re-read and confirmed in this pass: `sf.gov/learn-about-san-francisco-rental-laws` (13 June 1979
coverage threshold and the exemption list), `sf.gov/tenant-petitions` ("we do not adjudicate ... harassment,
discrimination and retaliation"), the Rent Board's 16 Oct 2024 algorithmic-device release (§ 37.10C,
effective 14 October 2024), and the DOJ release of 7 January 2025 (six landlords, more than 1.3 million
units, 43 states and DC).

Arithmetic re-computed in this pass and unchanged: 3,995.00 × 1.6% = 63.92 → 4,058.92; × 3.0% = 119.85 →
4,114.85; × 1.4% = 55.93 → 4,050.93; 3,150.00 × 1.6% = 50.40 → 3,200.40; × 10.0% = 315.00 → 3,465.00;
× 11.5% = 362.25 → 3,512.25; × 13.1% = 412.65 → 3,562.65. Banked sum 1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 =
11.5; + 1.6 = 13.1. Notice dates re-checked: 1 Feb 2027 − 30 = 2 Jan 2027; − 35 = 28 Dec 2026; 1 Feb 2027 −
90 = 3 Nov 2026.

### Irregularities found in this pass

1. **Rate table (corrected, FR-26).** On `pages/laws.html` five rows carried an end date that does not
   match document 571 — 3/1/12–**2/29/13**, 3/1/04–**2/29/05** and 3/1/00–**2/29/01** (29 February in
   non-leap years), 3/1/96–**2/29/97** (same), and 3/1/95–**2/28/96** (28 February in a leap year) — and
   the Board's separate **12/8/92 – 2/28/93 (1.6%)** row was missing, so 45 rows were shown where the PDF
   has 46. Percentages were all correct. Fixed in `tools/site_pages_rules.py`; a new build gate,
   `check_rate_table()` in `tools/verify_core_site.py`, compares all 46 published rows against the PDF
   transcription in order and fails the build on any drift (proved by reverting one date and watching it fail).
2. **Hard-coded flag count.** The requirements table said "25 flags published" as fixed text while the
   flagged page counted dynamically, so the two would disagree as soon as a flag was added. Both now read
   the list length (26 after FR-26).
3. No figure, percentage, dollar amount, statutory quotation or notice date on the canonical pages was
   found to be wrong. FR-01 … FR-25 remain as published; FR-03 (12-month vs 24-month banking wording),
   FR-05 (2027–28 rate unpublished), FR-06 (File #261020 not law), FR-11 (signature not specified), FR-13
   (voucher status), FR-14/FR-18 (building record), FR-20 (separate notice-copy filing) and FR-22/FR-23
   (no tenant-lawyer approval; no actual records) stay open and cannot be closed from official sources.

### Sources that could not be re-fetched in this pass

`calcivilrights.ca.gov` and `hud.gov` were not reachable from this sandbox on 2026-11-11 (connection
refused, not a 404). Both were fetched directly by earlier sessions and their content is quoted on the
site; the rule they support (FEHA administrative complaints; HUD complaints) is also established by
Gov. Code § 12955 and 42 U.S.C. § 3604, which were re-read this pass. No published claim depends on the
unreachable pages alone.
