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

> **Correction to the two records above (session `arena/488b115e`, 2026-11-11).** The `arena/beba4d31`
> gate and FR-26 still transcribed the 1984–85 period as ending 29 February 1985; Form 571 publishes
> `3/1/84 – 2/28/85`, and both the table and the transcription are now corrected. Its statement that the
> table "showed 45 rows" and lacked the separate `12/8/92 – 2/28/93` row was also re-checked against the
> pre-correction HTML at `a12419d`: the page published **46** rows including that row. The defects were
> the six end-dates, not the row count. Nothing from either record was deleted; a calendar-parsing gate was
> added so an impossible date cannot pass even if it is copied into both the table and its transcription.

# Independent line-by-line verification pass — 2026-11-11 (session `arena/488b115e-rentincreasesf3`)

Branch == `main` at `a12419d` (PR #47 merged). Unlike the pass above, **this sandbox could fetch the
official pages directly** (`fetch_page` reached sf.gov, leginfo.legislature.ca.gov, sfgov.legistar.com,
oag.ca.gov, codelibrary.amlegal.com and justice.gov on 2026-11-11), so every row below is a direct
re-read of the official page or document, not a secondary corroboration. Two published defects were
found and corrected; everything else matched.

| # | Assertion published on the site | Direct check performed 2026-11-11 | Result |
|---|---|---|---|
| 78 | Allowable annual increase 1.6% for 3/1/2026–2/28/2027; 1.4% for 3/1/2025–2/28/2026 | [sf.gov — Learn about rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) ("The allowed rent increase percentage in San Francisco is 1.6% … effective March 1, 2026 through February 28, 2027"; worked examples use 1.4% for 1 June 2025); [Form 571 PDF](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) parsed from the PDF text | Consistent |
| 79 | Complete 1982–2027 rate table: 46 rows, each with its official period and percentage | Form 571 PDF text compared **row by row, programmatically**, against `RATES` in `tools/site_pages_rules.py` | **6 defects found and fixed** — see irregularities 1 and 2 |
| 80 | Licence: all owners report into the Housing Inventory; licence auto-generated for tenant-occupied units; must be in effect on the **effective date**; 1 March annual deadline; 1–9 units and condominiums from 1 March 2023 (10+ units from 1 July 2022); no monetary penalty for late filing; licence need not accompany the notice; reporting does not obtain a Rent Board Fee exemption | [sf.gov — The Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) read in full | Consistent (each quoted phrase appears on the page) |
| 81 | Banking: 24-month condition; no cap; no expiry during the tenancy; prior-owner transfer; no carry-over to a new tenant; additive, never compounded or prorated; may be combined with the annual increase; notice must state the banked part | [sf.gov — Banked rent increases](https://www.sf.gov/information--banked-rent-increases) read in full | Consistent |
| 82 | Rule § 4.12(b): omitting the banked dates "shall not render the increase null and void" (so the notice defect is not automatically fatal) | [Part IV Rules §§ 4.10–4.12](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring) § 4.12(b) read verbatim; § 4.10(b) also read (nonconforming notice void "unless the amount requested equals no more than the allowable annual and banked rent increase(s)") | Consistent |
| 83 | Rent Board Fee is separate from the licence: $59.00 per dwelling unit for 2026–27, due 1 March, 5% monthly penalty capped at 15%, 50% ($29.50) recoverable, 2027 exemption window closes 14 December 2026 | [sf.gov — The Rent Board Fee](https://www.sf.gov/rent-board-fee) read in full | Consistent |
| 84 | Unlicensed increase may be "null and void (this may apply for multiple years)", tenant "may be entitled to a rent refund", Form 516C after the effective date and Form 518 before it | [sf.gov — Notice of Owner Noncompliance with Housing Inventory](https://www.sf.gov/notice-of-owner-noncompliance-with-housing-inventory) read in full | Consistent |
| 85 | AB 1482 statewide cap 8.8% for the San Francisco area 1 Aug 2026 – 31 Jul 2027 (6.3% the year before); local caps displace it where lower; San Francisco row: one increase of up to 60% of CPI, 1.6% for 3/1/26–2/28/27, banking allowed | [oag.ca.gov — Limits on Rent Increases](https://oag.ca.gov/rentcaps), both the statewide table and the San Francisco County row | Consistent |
| 86 | File #261020 status "Pending Committee Action", introduced 15 September 2026, Land Use and Transportation Committee, 10%/yr proposed cap on combined banked + capital-improvement increases | [Legistar File #261020](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770) read directly (status, title, history "ASSIGNED UNDER 30 DAY RULE") | Consistent |
| 87 | § 37.3(a)(1): 60% of the published CPI change, 7% ceiling, and the licence under § 37.15; § 37.3(a)(2) banking since 1 April 1982 | [SF Admin. Code § 37.3](https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_admin/0-0-0-70881) § 37.3(a)(1)–(2) read verbatim | Consistent |
| 88 | AB 1482 does not govern where a local ordinance restricts increases to a lower amount; Costa-Hawkins does not reach a partial change of occupancy while an original occupant remains | [Civ. Code § 1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) (d)(3) and [§ 1954.53](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954.53) (d)(2)–(3) read verbatim | Consistent |
| 89 | Notice: 30 days if ≤10%, 90 days if >10%, measured against the rent charged at any time in the prior 12 months, in person or by mail under CCP § 1013 | [Civ. Code § 827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) (b)(1)–(3) read verbatim | Consistent |
| 90 | Coverage: units built on or before 13 June 1979 generally have rent control and eviction protection; single-family dwellings and most condominiums excluded; full list of wholly exempt units | [sf.gov — Learn about San Francisco rental laws](https://www.sf.gov/learn-about-san-francisco-rental-laws) read in full | Consistent |
| 91 | Special-circumstances (comparable-rent) petition: "The mere fact that a long-standing tenant is paying significantly less than market rent is not considered an extraordinary circumstance"; petition must be filed before the notice | [sf.gov — Special Circumstances Petitions](https://www.sf.gov/information--special-circumstances-petitions-based-rents-comparable-units) read in full | Consistent |
| 92 | DOJ suit against six large landlords over algorithmic pricing, filed/announced 7 January 2025 | [justice.gov press release 25-21](https://www.justice.gov/archives/opa/pr/justice-department-sues-six-large-landlords-algorithmic-pricing-scheme-harms-millions) read directly | Consistent |
| 93 | Notice-date planner arithmetic: 1 Feb 2027 −30 d = 2 Jan 2027 (−35 d = 28 Dec 2026); −90 d = 3 Nov 2026 (−95 d = 29 Oct 2026); 8 Feb 2027 −90 d = 10 Nov 2026; 14 Feb 2027 −90 d = 16 Nov 2026 (−95 d = 11 Nov 2026) | Recomputed in `verify_core_site.py` and re-checked by hand | Consistent |
| 94 | Every published dollar figure: 3,995 × 1.6% = 63.92 → 4,058.92; 3,995 × 3.0% = 119.85 → 4,114.85; 3,150 × 1.6% = 50.40 → 3,200.40; 11.5% = 362.25 → 3,512.25; 13.1% = 412.65 → 3,562.65; 10.0% = 315.00 → 3,465.00; banked sum 1.8+0.7+2.3+3.6+1.7+1.4 = 11.5 and +1.6 = 13.1 | Recomputed from the published percentages (no rounding up) | Consistent |
| 95 | Build idempotent; all gates pass after the corrections | `build_dashboard.py` re-run twice (no diff), then `privacy_scan.py` (108 files), `verify_core_site.py` (14 pages / 41 tables / 350 rows / 988 links), `audit_site.py`, `verify_site.py`, `check_site.py`, `verify_edition.py`, `check_v2.py`, `verify_review_regressions.py` | PASS |

## Irregularities found in this pass

1. **Five impossible end-dates in the 1982–2027 rate table (fixed).** `RATES` ended five periods on
   29 February of a year that is not a leap year, and therefore disagreed with Form 571:
   `3/1/84 – 2/29/85 → 2/28/85`, `3/1/96 – 2/29/97 → 2/28/97`, `3/1/00 – 2/29/01 → 2/28/01`,
   `3/1/04 – 2/29/05 → 2/28/05`, `3/1/12 – 2/29/13 → 2/28/13`. Percentages were correct throughout.
2. **One missing leap day (fixed).** `3/1/95 – 2/28/96` should be `3/1/95 – 2/29/96` (1996 is a leap
   year; Form 571 publishes 29 February), which had produced a one-day gap in the official sequence.
   All 46 rows now match Form 571 on both period and percentage.
3. **Flag list published out of numeric order (fixed).** `pages/flagged.html` rendered `FR-16` then
   `FR-21…FR-25` then `FR-17…FR-20`, which is hard to review. The page now sorts flags numerically; no
   flag text, status or count (25) changed.
4. **Regression guards added** so neither class of error can return: `verify_core_site.py` now parses
   every rate period (rejecting impossible dates), requires the periods to be contiguous and
   descending, and requires flag IDs on the Flagged page to be unique and ascending.
5. Nothing else failed. No percentage, dollar amount, notice period, source URL or privacy control
   changed; the total flag count remains 25, and FR-15 now records the rate-table correction.
---

## Pass 2026-11-11 — session `arena/96aa0f4f-rentincreasesf3` (direct fetches, not web search)

Unlike the other 11 November passes, this session's sandbox could open the official pages directly,
so each row below records what was read on the page itself on 2026-11-11.

| # | Assertion | Check performed 2026-11-11 | Result |
|---|---|---|---|
| 96 | Allowable increase 1.6% for 3/1/2026–2/28/2027, "60% of the increase in the Consumer Price Index for All Urban Consumers in the Bay Area"; once every 12 months; licence required before annual/banked increases; 30-day notice, 90-day if >10%, +5 days if mailed; notice states amount, percentage, effective date | Fetched `sf.gov/learn-about-rent-increases-san-francisco` directly (both chunks) | Confirmed verbatim |
| 97 | Rate table: 1.6% (3/1/26–2/28/27), 1.4% (25–26), 1.7% (24–25), 3.6% (23–24), 2.3% (22–23), 0.7% (21–22), 1.8% (20–21), back to 7.0% (4/1/82–2/28/83); "may increase the tenant's base rent once every 12 months … without filing a petition at the Rent Board" | Fetched the Form 571 PDF directly | Confirmed — every percentage used on this site matches the published table |
| 98 | Banking: no cap, additive not compounded, back to 1 Apr 1982, does not expire during a tenancy, survives a sale, does not carry to a new tenant; licence required "Effective July 1, 2022 (or March 1, 2023 for condominiums and buildings with 1-9 residential units)"; notice must also state "which part of the increase is banked" | Fetched `sf.gov/information--banked-rent-increases` directly | Confirmed verbatim |
| 99 | Licence: "All owners of residential property are required to report"; "Property owners who have tenants will receive a rent increase license after the submission"; licence "automatically generated for non-owner occupied units"; must be on file "before any annual or banked rent increase can go into effect"; "will not be enforceable without having a rent increase license on the effective date of the notice"; 1 July 2022 for 10+ unit non-condo buildings, 1 March 2023 for condominiums and buildings with fewer than 10 units; 1 March annual deadline; "does not assess monetary penalties for filing after the deadline"; licence need not accompany the notice | Fetched `sf.gov/rent-board-housing-inventory` directly | Confirmed verbatim — the answer to the brief's foremost question |
| 100 | Rent Board Fee is separate: $59.00 per dwelling unit / $29.50 per guest unit for 2026-27; 50% recoverable ($29.50 / $14.75); due 1 March; 5% monthly penalty capped at 15%; 2027 exemption deadline 14 December 2026; a fee exemption request does not satisfy Housing Inventory reporting | Fetched `sf.gov/rent-board-fee` directly | Confirmed verbatim |
| 101 | AB 1482 cap for the San Francisco Area is 8.8% for increases starting 1 Aug 2026 – 31 Jul 2027 (6.3% for the prior year); "If the rent increase cap set by your city or county results in a lower increase … then the local rule will apply" | Fetched `oag.ca.gov/rentcaps` directly | Confirmed — the state figure does not govern here |
| 102 | Notice periods: § 827(b)(2) — increase "10 percent or less" ⇒ at least 30 days; § 827(b)(3)(A) — "greater than 10 percent" ⇒ at least 90 days; measured against rent charged at any time in the 12 months before the effective date, alone or combined; service personally or by mail under CCP § 1013 | Fetched `leginfo … lawCode=CIV&sectionNum=827` directly | Confirmed verbatim |
| 103 | File #261020 (Administrative Code – Cap On Rent Increases for Rent-Controlled Units): Type Ordinance, Status **Pending Committee Action**, introduced 9/15/2026, in control of the Land Use and Transportation Committee, no final action, no enactment date; sponsors Sauter, Chan, Mahmood; 4 history rows, latest 10/7/2026 Youth Commission response | Fetched the Legistar file page directly | Confirmed — still not law on 11 Nov 2026 |
| 104 | Multiple-year increases: add the allowable percentages, "Increases cannot be compounded", "Landlords are not required to file a petition with the City", no rounding up, at least 30 days' notice (35 if mailed), base rent only | Fetched `sf.gov/information--annual-rent-increase-multiple-years` directly | Confirmed; its worked example adds the current anniversary year's percentage into the total, which is how 13.1% is composed |
| 105 | The 12-month banking wording quoted on the executive summary is genuine official text | Fetched chunk 2 of the rent-increases page: "a full 12 months has not elapsed between the date it first became available on June 1, 2025, and the date of the rent increase on May 1, 2026 … permanently lost" | Confirmed verbatim |
| 106 | 11 November 2026 is a federal holiday (Veterans Day) | Fetched `opm.gov` Federal Holidays: 2026 table lists "Wednesday, November 11 — Veterans Day" (5 U.S.C. 6103) | Confirmed; USPS service that day not verified (FR-26) |
| 107 | Every published figure and notice date recomputed | Python: 3,995×1.6% = 63.92 → 4,058.92; ×3.0% = 119.85 → 4,114.85; 3,150×1.6% = 50.40 → 3,200.40; ×10% = 315.00 → 3,465.00; ×11.5% = 362.25 → 3,512.25; ×13.1% = 412.65 → 3,562.65; 1.8+0.7+2.3+3.6+1.7+1.4 = 11.5; +1.6 = 13.1. Planner: 1 Feb 2027 −30 = 2 Jan 2027, −35 = 28 Dec 2026, −90 = 3 Nov 2026, −95 = 29 Oct 2026; 8 Feb 2027 −90 = 10 Nov 2026, −95 = 5 Nov 2026; 14 Feb 2027 −90 = 16 Nov 2026, −95 = 11 Nov 2026 | All published values correct |
| 108 | Elapsed time from the 1 June 2025 skipped increase to a 1 February 2027 effective date | Python month arithmetic | **20 months, not 12** — the published cell was wrong and has been corrected |
| 109 | Gates on the merged tree `a12419d` before any edit | All 9 scripts run | All PASS; `verify_core_site.py` reported 14 pages / 41 tables / 350 rows / 988 links; after this pass's corrections: 351 rows / 990 links |

### Irregularities found by `arena/96aa0f4f` (all corrected or flagged in this pass)

1. **Wrong elapsed time in a data row.** `pages/units.html` described the 1 June 2025 skipped increase as
   "Skipped — banked (12 months elapsed by Feb 2027)". 1 June 2025 → 1 February 2027 is **20 months**.
   Corrected to state the official test (a full 12 months elapsed on 1 June 2026) with the rent-increases
   page added as the row's third source.
2. **Stale planner deadline presented as open.** The 8 February 2027 row showed "Serve in person by
   10 November 2026" with no "passed" badge, although that date is before the site's own research-pass
   date. Badged as passed. `tools/verify_core_site.py` now fails the build if any planner deadline on or
   before the research-pass date is unmarked (proved by running it against the pre-fix page: 2 failures).
3. **Mail-by deadline falling on a federal holiday.** The 14 February 2027 row's last mailing day is
   11 November 2026 — Veterans Day, a federal holiday per OPM. Published as **FR-26** (unverified: no
   official USPS source was reachable in this session) and annotated in the planner with the OPM link.
4. **Stale date in the markdown summary.** `EXECUTIVE_SUMMARY.md` still said "Notice-date arithmetic
   (from 10 November 2026)" and offered 10 November service as a live example. Rolled to 11 November 2026;
   the earliest date a >10% increase served on 11 November 2026 can reach is 9 February 2027.
5. **FR-03 reasoning was asserted, not shown.** It claimed "neither wording changes Unit B's total"
   without saying why. Rewritten to show the arithmetic under both published readings (24 months without
   any increase elapsed on 1 June 2021; every skipped year was >12 months old by 1 February 2027) and to
   name the third reading that is *not* in either text (which would give 10.1% banked by 1 February 2027).
6. **Hardcoded flag counts.** Adding FR-26 made the literals "25 flags published" (`pages/requirements.html`)
   and "25 flagged items" (`README.md`) stale. Updated to 26, and `tools/verify_core_site.py` now fails the
   build if any literal count disagrees with `len(FLAGS)` (proved by temporarily setting README back to 25).
7. **Two domain allowlists, not one.** `tools/audit_site.py` keeps its own `DOMAINS` set separate from
   `site_layout.OFFICIAL_DOMAINS`; adding a new official domain to one silently breaks the other. Both were
   updated for `opm.gov`. Worth unifying in a future pass.
8. **Unmerged PRs overlapping this pass's files:** #45 (`arena/3cb4d5e1`, no claim recorded in this file),
   #35 and #33 (both noted as superseded / needing rebase by earlier sessions). Left untouched; whoever
   resumes them must rebase onto current `main` or they will revert these corrections.

# Final verification + integration pass — 2026-11-11

Session `arena/6d04c026-rentincreasesf3`. Branch branched from `main` at `a12419d` (PR #47 merged).
Unlike the 2026-11-11 confirmation pass recorded above, **this session's `fetch_page` tool reaches
sf.gov, leginfo, oag.ca.gov, govinfo, justice.gov, hud.gov, ecfr.gov, sfgov.legistar.com and
codelibrary.amlegal.com directly**, so every official source cited on the canonical site was fetched
and read again on 11 November 2026 — not corroborated indirectly. All 36 distinct external URLs on the
canonical site plus `data/sources.json` were retrieved; 35 resolved and supported the claims attached
to them, and one was a 404 (row 115).

| # | Assertion | Official source fetched 2026-11-11 | Result |
|---|---|---|---|
| 110 | "All owners of residential property are required to report"; licence generated for tenant-occupied units; licence must be in effect on the **effective date** or the notice "will not be enforceable"; deadline 1 March annually; no monetary penalty for late filing; contact changes within 30 days; licence "does not need to be included with your rent increase notice"; reporting is free | [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) | Confirmed verbatim |
| 111 | Licence start dates: 1 Jul 2022 for units (other than condominiums) in buildings of 10+ units; 1 Mar 2023 for condominiums and buildings with fewer than 10 units. Rule turns on building size, **not** on whether the owner is an individual or a corporation | [Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) · [Ordinance 265-20](https://www.sf.gov/news--new-legislation-creates-housing-inventory-and-requires-owners-obtain-license-imposing) | Confirmed — answers the owner's individual-vs-corporation question |
| 112 | Unlicensed notice "may be null and void (this may apply for multiple years)"; tenant "may be entitled to a rent refund"; Form 516C / Form 518; 415-252-4600, 9–12 and 1–4; **licence not required "in some situations where the original occupant(s) no longer live in the unit"** | [Notice of Owner Noncompliance](https://www.sf.gov/notice-of-owner-noncompliance-with-housing-inventory) | Confirmed; carve-out added as FR-29(b) |
| 113 | Licence "will be **suspended** for the period of noncompliance" if the owner does not report | [Ordinance 265-20](https://www.sf.gov/news--new-legislation-creates-housing-inventory-and-requires-owners-obtain-license-imposing) | Confirmed — new (FR-29(a)) |
| 114 | Allowable increase 1.6% (3/1/2026–2/28/2027), prior year 1.4%; 60% of Bay Area CPI; base rent only incl. housing services, excl. passthroughs; no rounding up; first increase 12 months after lease start; anniversary rules; 30/90-day notice; +5 days if mailed; no extra charge for an additional occupant | [Learn about rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) · [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) · [1.6% announcement](https://www.sf.gov/news--annual-rent-increase-3126-22827-announced) · [current rates](https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit) | Confirmed |
| 115 | Full 1982–2027 rate table used for every banked-year figure; security-deposit interest 4.2% | [Form 571 PDF](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) · [current rates](https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit) | Confirmed. Every anniversary rate used for Unit A and Unit B re-read off the table: 1.8 / 0.7 / 2.3 / 3.6 / 1.7 / 1.4 / 1.6 |
| 116 | Banking: no cap back to 1 Apr 1982; additive not compounded; no expiry during a tenancy; does not carry to a new tenant; new owners may use prior owners' balances; notice must identify the banked part; **"A skipped increase is only banked if at least 24 full months pass without any rent increase"** | [Banked rent increases](https://www.sf.gov/information--banked-rent-increases) | Confirmed, including the 24-month sentence |
| 117 | **Rules & Regulations § 4.12(a)**: "A full **12 months** must have elapsed from the date that an annual rent increase, or a portion thereof, could have been imposed before this banking section becomes applicable"; banked amounts not compounded, not rounded up; **"This banked amount may only be given at the time of an annual increase"** | [Rules Part IV](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring) | Confirmed — third official text; FR-03 updated, FR-27 added |
| 118 | **Rules & Regulations § 4.12(b)**: banked portion + "the dates upon which said banked amount is based" must be disclosed, but "failure to include such information **shall not render the increase null and void**"; **§ 4.10(b)** voids a non-conforming increase unless within allowable annual + banked amounts (½-of-1% good-faith readjustment) | [Rules Part IV](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring) | Confirmed — FR-28 added |
| 119 | Civ. Code § 827(b)(2)–(3): 30 days if the increase is ≤10% of rent charged at any time in the prior 12 months alone or combined; 90 days if greater; service by personal delivery or mail under CCP § 1013 | [Civ. Code § 827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) | Confirmed |
| 120 | CCP § 1013(a): +5 calendar days in California, +10 if either place is outside California but inside the US, **+20 if outside the United States** | [CCP § 1013](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1013) | Confirmed |
| 121 | AB 1482 / Civ. Code § 1947.12: 5% + CPI capped at 10%; **§ 1947.12(d)(3) exempts housing already under a local ordinance restricting annual increases to less than that**; SF-area figure 8.8% (5% + 3.8% CPI) for 1 Aug 2026 – 31 Jul 2027; Rent Board states it "does NOT apply for units under the rent increase limitations of the San Francisco Rent Ordinance" | [Civ. Code § 1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) · [oag.ca.gov](https://oag.ca.gov/rentcaps) · [Rent Board AB 1482](https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482) | Confirmed — state cap is displaced, local 1.6% governs |
| 122 | Civ. Code § 1942.5: 180-day retaliation window for the five listed triggers; **§ 1942.5(d) prohibits retaliatory increases for tenant organizing with no 180-day limit**; § 1942.5(b) once per 12 months | [Civ. Code § 1942.5](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5) | Confirmed — the site's hedged wording is correct |
| 123 | Gov. Code § 12955 FEHA list (incl. source of income, veteran/military status, genetic information) and 42 U.S.C. § 3604(b) (terms/conditions/privileges of rental; § 3604(f) disability) | [Gov. Code § 12955](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=12955) · [42 U.S.C. § 3604](https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm) | Confirmed |
| 124 | File #261020: status **Pending Committee Action**, introduced 9/15/2026, in the Land Use and Transportation Committee, title caps banked + capital-improvement increases at 10%/yr for three years; Rent Board's 9 Nov 2026 notice (not enacted; would apply to banked increases noticed on/after 15 Sep 2026) | [Legistar](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770) · [rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) | Confirmed |
| 125 | § 6.14 / Costa-Hawkins: "A 6.14 notice can be served on any subsequent occupant, whether the subsequent occupant is a subtenant or a co-tenant"; but under Costa-Hawkins "a co-tenant, as opposed to a subtenant, is not subject to such a rent increase, regardless of when the co-tenant moved in"; unlimited increase only when the **last** original occupant vacates | [§ 6.14 / Costa-Hawkins](https://www.sf.gov/information--rent-increases-under-section-614-and-costa-hawkins) | Confirmed — Unit A has a remaining original occupant, so no market-rate reset |
| 126 | Only six landlord petition types require filing before notice; annual and banked are not among them; Rent Board "do[es] not adjudicate issues ... such as harassment, discrimination and retaliation" | [Landlord petitions](https://www.sf.gov/landlord-petitions-and-passthroughs) · [Tenant petitions](https://www.sf.gov/tenant-petitions) | Confirmed |
| 127 | Tenant petition: no charge, no time limit, box C, ALJ hearing, "designed so that no one needs an attorney"; Eviction Defense Collaborative 415-659-9184 | [Unlawful rent increase](https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history) · [evictions](https://www.sf.gov/evictions-san-francisco) | Confirmed |
| 128 | Rent Board Fee $59.00 per dwelling unit 2026–27; $29.50 guest unit; 50% recoverable; 1 March deadline; 5%/month to 15% cap; 2027 exemption window closes 14 Dec 2026 | [Rent Board Fee](https://www.sf.gov/rent-board-fee) | Confirmed |
| 129 | Coverage: built on or before 13 June 1979; not a single-family dwelling; most condos exempt from rent control | [SF rental laws](https://www.sf.gov/learn-about-san-francisco-rental-laws) · [About Rent Board](https://sf.gov/departments/rent-board/about) (Rent Ordinance enacted 13 June 1979) | Confirmed |
| 130 | Algorithmic devices banned (Ordinance § 37.10C, effective 14 Oct 2024); DOJ antitrust suit against six landlords filed 7 Jan 2025 | [sf.gov](https://www.sf.gov/news--new-law-prohibits-algorithmic-devices-used-set-rents-san-francisco) · [DOJ](https://www.justice.gov/archives/opa/pr/justice-department-sues-six-large-landlords-algorithmic-pricing-scheme-harms-millions) | Confirmed |
| 131 | Special-circumstances/comparable-rent petition: "The mere fact that a long-standing tenant is paying significantly less than market rent is not considered an extraordinary circumstance"; notice served before the petition is void | [Topic 323](https://www.sf.gov/information/topic-no-323-special-circumstances-petitions-based-rents-comparable-units) (redirects to the live sf.gov page) | Confirmed |
| 132 | Portal: owners "Obtain a License to increase rents for tenants covered by Rent Control"; tenants can "View status of landlord's current License to increase rent for a unit" | [portal.sfrb.org](https://portal.sfrb.org/) | Confirmed |

## Correction made in this pass (row 115 — the one failure)

| # | Item | Finding | Action |
|---|---|---|---|
| 133 | Federal voucher source link | `https://www.ecfr.gov/current/title-24/subtitle-B/chapter-II/subchapter-B/part-982/subpart-M` returns **HTTP 404** ("We were unable to find the content you requested on that date"). Part 982 is in **Chapter IX** (Office of Assistant Secretary for Public and Indian Housing), not Chapter II, and there is no Subpart M matching the claim. The provision the register described — Section 8 rent reasonableness — is **24 CFR § 982.507 "Rent to owner: Reasonable rent"**, in **Subpart K** | Corrected in `data/sources.json`; published on the site as FR-26 and cited on the units page |

## Arithmetic recomputed in this pass (unchanged from the published pages)

Unit A: 3,995.00 × 1.6% = 63.92 → 4,058.92 · 3,995.00 × 3.0% = 119.85 → 4,114.85 · 119.85 × 12 = 1,438.20
Unit B: 3,150.00 × 1.6% = 50.40 → 3,200.40 · × 10.0% = 315.00 → 3,465.00 · × 11.5% = 362.25 → 3,512.25 ·
× 13.1% = 412.65 → 3,562.65 · 412.65 × 12 = 4,951.80. Banked sums 1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 = 11.5;
11.5 + 1.6 = 13.1. All match.

## Notes (not defects)

- Every sf.gov page fetched on 11 Nov 2026 displayed the banner "City offices will be closed on
  Wednesday, November 11 for Veterans Day" — the Rent Board counselling line (415-252-4600) is closed
  today. Recorded for operational planning only; not published as a dated site fact.
- `https://www.hud.gov/program_offices/fair_housing_equal_opp` (in the internal register only, not in
  the canonical page registry) now redirects to HUD's "Contact FHEO" page. It resolves and is official;
  no figure depends on it.
- `https://www.sf.gov/information/topic-no-323-...` redirects to
  `https://www.sf.gov/information--special-circumstances-petitions-based-rents-comparable-units`. Resolves.
- The Rent Board's own banking worked example (tenant 8/1/2022, first increase 8/1/2025, banking **both**
  8/1/2023 and 8/1/2024) cannot be reconciled with a strict per-anniversary reading of the 24-month
  sentence. This is why FR-03 keeps both readings published rather than picking one.

---

## Session `arena/10fc30b0-rentincreasesf3` — direct reads and whole-site row audit (2026-11-11)

Every page below was fetched directly in this session on 11 Nov 2026 and read against the statement
in the second column. Row numbers continue from 133.

| # | Statement checked | Result | Official source |
|---|---|---|---|
| 134 | "All owners of residential property are required to report"; licence generated automatically for non-owner-occupied units; must be current "on the effective date of the notice"; deadline 1 March; no monetary penalty for late filing; contact changes within 30 days | Confirmed verbatim | <https://www.sf.gov/rent-board-housing-inventory> |
| 135 | Housing Inventory submissions are public (name and business contact information, square footage, bedrooms, bathrooms, 12-month vacancy/occupancy history); Portal account needs "the PIN number on your Annual Notice" | Confirmed verbatim — **not previously on the canonical site**; added (FR-34) | <https://www.sf.gov/rent-board-housing-inventory> |
| 136 | 1.6% for 1 Mar 2026 – 28 Feb 2027; notice of 9 Nov 2026 on File No. 261020; 30/90-day notice plus 5 days if mailed; first increase 12 months after the lease began | Confirmed verbatim | <https://www.sf.gov/learn-about-rent-increases-san-francisco> |
| 137 | Worked examples on the same page: example 1 says 1.6% was "in effect on June 1, 2025"; example 4 quotes June 1, 2026 for a May 1, 2026 increase | **Date slips in the official text** (Form 571: 1.4% on June 1, 2025). Arithmetic of each example is right. Published as FR-32 | <https://www.sf.gov/learn-about-rent-increases-san-francisco> |
| 138 | Banking: 24-full-months sentence; no limit; no expiry during the tenancy; not compounded or prorated; notice must say which part is banked | Confirmed verbatim. One sentence of the worked example says 1.4% was "in effect on August 1, 2024" (Form 571: 1.7%) — FR-32 | <https://www.sf.gov/information--banked-rent-increases> |
| 139 | All 46 periods and percentages, 4/1/82 – 2/28/27 | Compared by script with every period/percentage pair on all 71 published pages (122 pairs). One mismatch, in `docs/legal-framework.html` (3/1/88 – 2/29/88), corrected to 2/28/89 | <https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf> |
| 140 | Unlicensed notice "may be null and void (this may apply for multiple years)"; tenant "may be entitled to a rent refund"; start dates 1 July 2022 / 1 March 2023; Forms 516C and 518 | Confirmed verbatim | <https://www.sf.gov/notice-of-owner-noncompliance-with-housing-inventory> |
| 141 | Fee $59.00 per dwelling unit for 2026–27; 50% ($29.50) recoverable from tenants in occupancy on 1 November; 5% monthly penalty to 15%; exemption deadline 14 December 2026 | Confirmed verbatim. The page does not say whether an unpaid fee affects the licence — FR-33 | <https://www.sf.gov/rent-board-fee> |
| 142 | Rule § 4.12(a) "A full 12 months must have elapsed…"; § 4.12(b) banked portion and dates; § 4.10(a)–(b) | Confirmed verbatim | <https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring> |
| 143 | File #261020: Ordinance, introduced 9/15/2026, status Pending Committee Action, Land Use and Transportation Committee, no enactment date; latest history entry 10/7/2026 | Confirmed | <https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770> |
| 144 | Civ. Code § 827(b)(2)–(3): 30 days at 10% or less, 90 days above, measured over the prior 12 months; CCP § 1013(a): five calendar days for mail within California | Confirmed verbatim | <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827> · <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1013> |
| 145 | Civ. Code § 1942.5(a) 180-day provision and (d); § 1947.12(a) and (d)(3); Gov. Code § 12955(a) list of protected characteristics; 42 U.S.C. § 3604(a)–(b), (f) | Confirmed verbatim | <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5> · <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12> · <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=12955> · <https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm> |
| 146 | State cap for the San Francisco area: 6.3% (8/1/25 – 7/31/26), 8.8% (8/1/26 – 7/31/27); the lower local cap applies | Confirmed | <https://oag.ca.gov/rentcaps> |
| 147 | Tenant petitions are free with no time limit; the Rent Board does not adjudicate harassment, discrimination or retaliation; six landlord petition types; § 6.14 / Costa-Hawkins co-tenant wording | Confirmed verbatim | <https://www.sf.gov/tenant-petitions> · <https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history> · <https://www.sf.gov/landlord-petitions-and-passthroughs> · <https://www.sf.gov/information--rent-increases-under-section-614-and-costa-hawkins> |
| 148 | Every table row on every published page carries an official link | **Not true of the preserved editions.** 276 of 1,386 rows lacked one before this pass; 114 of 1,050 preserved rows after it; canonical pages 348 of 348. Published as FR-24; enforced by `tools/row_source_audit.py` | (repository check) |

Not fetched in this session, so not re-verified by it: Administrative Code § 37.3 on American Legal,
the algorithmic-devices pages, the Department of Justice release, HUD and eCFR pages, the Civil
Rights Department subpages beyond the housing landing page, and the non-official research cited only
in `docs/` and `dashboard/`.

## Re-verification pass — 2026-11-13 (session `arena/fd7ed99e`)

A fresh line-by-line re-check of the time-sensitive official facts the canonical site depends on, run on
13 November 2026 (two days after the 11 Nov 2026 pass). Every source below was fetched and read directly
on that date. **Result: every load-bearing fact is unchanged; no figure on the canonical site required
correction.** The 11 November 2026 research-pass date is retained because it remains the date of the
comprehensive line-by-line pass; this entry records the additional confirmation.

| # | Claim on the canonical site | Official source re-fetched 2026-11-13 | Result |
|---|---|---|---|
| 1 | Allowable annual increase is **1.6%**, effective 1 Mar 2026 – 28 Feb 2027 (60% of Bay Area CPI) | [sf.gov — Learn about rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) | **Confirmed.** "The allowed rent increase percentage in San Francisco is 1.6%. The percentage is effective March 1, 2026 through February 28, 2027." |
| 2 | A **rent-increase licence** is required before imposing annual/banked increases; obtained automatically by reporting into the Housing Inventory; effective 1 Jul 2022 (1 Mar 2023 for condos and 1–9 unit buildings) | [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) · [sf.gov — Learn about rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) | **Confirmed.** "A landlord must get a rent increase license before imposing annual allowable and/or banked rent increases." Licence "automatically generated for non-owner occupied units"; must be current "before any annual or banked rent increase can go into effect". |
| 3 | The licence must be in effect on the **effective date**; reporting is free; annual deadline 1 March; no monetary penalty for late filing | [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) | **Confirmed.** "your rent increase notice will not be enforceable without having a rent increase license on the effective date of the notice"; "The Rent Board does not assess monetary penalties for filing after the deadline." |
| 4 | Banking: a skipped increase is banked only if **at least 24 full months** pass without any rent increase; no cap back to 1 Apr 1982; additive, not compounded | [sf.gov — Banked rent increases](https://www.sf.gov/information--banked-rent-increases) | **Confirmed.** "A skipped increase is only banked if at least 24 full months pass without any rent increase." "There is no limit on how much can be banked." (The three-texts discrepancy is already published as FR-03; the binding Rule § 4.12(a) uses a 12-month test.) |
| 5 | Notice: **30 days** if the increase is ≤10%, **90 days** if >10%; **+5 days** if mailed | [sf.gov — Learn about rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) · [Cal. Civ. Code § 827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) | **Confirmed.** § 827(b)(2)–(3) states the 30/90-day thresholds; the sf.gov page adds the 5-day mail extension. |
| 6 | State cap: **8.8%** for the San Francisco area for increases starting 8/1/26–7/31/27; the local cap governs because it is lower | [oag.ca.gov — Limits on rent increases](https://oag.ca.gov/rentcaps) | **Confirmed.** San Francisco Area row: 8.8% for "Increase starts between 8/1/26 and 7/31/27". |
| 7 | File #261020 would cap banked + capital-improvement increases at **10%/yr for three years**; status **Pending Committee Action**; not law | [sfgov.legistar.com — File #261020](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770) · [sf.gov — 9 Nov 2026 notice](https://www.sf.gov/learn-about-rent-increases-san-francisco) | **Confirmed.** Legistar: Status "Pending Committee Action"; Introduced 9/15/2026; in control Land Use and Transportation Committee. sf.gov: "This legislation has not been enacted and is subject to change." |

**Conclusion:** the canonical site is current and accurate as of 13 November 2026. This session therefore
adds no factual correction; its deliverable is the user-requested dedicated **Suggestions & decision-path**
page (S1) plus final integration (I1).

## Pass of 13 November 2026 — session `arena/a53557bb-rentincreasesf3`

Independent re-fetch of the sources that carry the forefront answer and every computed figure,
plus the new open-questions page and the second proposals register merged into the suggestions page.

| # | Assertion | Official page read on 13 Nov 2026 | Result |
|---|---|---|---|
| 149 | Annual allowable increase **1.6%** for 1 Mar 2026 – 28 Feb 2027; prior year 1.4% | [sf.gov — Learn about rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) | Confirmed verbatim; also confirms 60% of Bay Area CPI basis, base-rent-only rule, no round-up, 12-month anniversary rule, 30/90-day notice, +5 days by mail, notice contents, additional-occupant prohibition, vacancy pricing |
| 150 | Full historical rate table used for banking (1.8 / 0.7 / 2.3 / 3.6 / 1.7 / 1.4 / 1.6) | [Form 571 (PDF)](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) | All 46 published periods re-read; Unit B banked 11.5% and total 13.1% reproduce exactly |
| 151 | Banking requires **24 full months** without an increase (page text) and the worked example applies a **12-month** test | [sf.gov — Banked rent increases](https://www.sf.gov/information--banked-rent-increases) · [sf.gov — Learn about rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) | Both texts re-read; divergence remains published as FR-03; Unit A's 1.4% banks under either reading |
| 152 | Licence is **local** law: Ordinance No. 265-20, effective 18 Jan 2021; reporting from 1 Mar 2023 for condominiums and buildings with fewer than 10 units; licence suspended for noncompliance | [sf.gov — new legislation creates a housing inventory](https://www.sf.gov/news--new-legislation-creates-housing-inventory-and-requires-owners-obtain-license-imposing) | Confirmed verbatim — no state agency filing anywhere in the text |
| 153 | All owners must report; licence auto-generated for non-owner-occupied units; annual update due 1 March; late filing has no monetary penalty; submitted information is public | [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) | Confirmed; “The information entered in the housing inventory submission is public” newly noted → SG-11 |
| 154 | Unlicensed increase: notice “may be null and void (this may apply for multiple years)”, tenant “may be entitled to a rent refund”; licence **not** required for § 6.14 / Costa-Hawkins situations or passthroughs; how to check licence by address/APN | [sf.gov — Notice of Owner Noncompliance](https://www.sf.gov/notice-of-owner-noncompliance-with-housing-inventory) | Confirmed; the carve-out boundary published as **FR-36** |
| 155 | Six increase types need a Rent Board petition **before** the notice; petitions are free; owner may petition for a determination of lawful rent with complete rent history | [sf.gov — Landlord petitions and passthroughs](https://www.sf.gov/landlord-petitions-and-passthroughs) | Confirmed — this is the only “apply to the Rent Board” route for an increase |
| 156 | § 6.14 permits an unlimited increase on remaining occupants only with a timely written notice (about 60 days) to each subsequent occupant; co-tenants are outside the Costa-Hawkins route | [sf.gov — Rent increases under Section 6.14 and Costa-Hawkins](https://www.sf.gov/information--rent-increases-under-section-614-and-costa-hawkins) | Confirmed — governs whether Unit A's 2026 occupant change ever opens that door (FR-21) |
| 157 | Rent Board Fee **$59.00** per dwelling unit 2026–27, due 1 March, 5%/month penalty capped at 15%, 50% ($29.50) recoverable, exemption window closes 14 Dec 2026 | [sf.gov — The Rent Board Fee](https://www.sf.gov/rent-board-fee) | Confirmed verbatim |
| 158 | Tenant challenge: unlawful-rent-increase petition (Form 516C + Form C), **no time limit** for filing, ALJ hearing, no lawyer needed; Rent Board does not hear discrimination, harassment, retaliation or deposit claims | [sf.gov — Report an unlawful rent increase](https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history) · [sf.gov — Tenant petitions](https://www.sf.gov/tenant-petitions) | Confirmed |
| 159 | Civ. Code § 827(b)(2)–(3): 30 days at ≤10%, 90 days at >10%, measured against the lowest rent in the prior 12 months; § 827 applies to periodic tenancies | [leginfo — Civ. Code § 827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) | Confirmed; fixed-term-lease question published as **Q-03** |
| 160 | Civ. Code § 1947.12: 5% + CPI capped at 10%; (d)(3) local-ordinance exemption; (d)(5)(B) written exemption notice required of a non-corporate owner of a separately alienable unit; (d)(6) owner-occupied two-unit structure exemption | [leginfo — Civ. Code § 1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) | Confirmed; exemption-notice duty added to the state-law answer on the open-questions page |
| 161 | State cap for the San Francisco area **8.8%** for increases starting 1 Aug 2026 – 31 Jul 2027 (6.3% for 1 Aug 2025 – 31 Jul 2026) | [oag.ca.gov — Limits on rent increases](https://oag.ca.gov/rentcaps) | Confirmed; local cap lower, so local rule governs |
| 162 | File #261020 status | [SF Legistar](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770) | **Pending Committee Action**, no final action, last entry 7 Oct 2026 — not law; FR-06 stands |
| 163 | Coverage cutoff: units built on or before 13 June 1979; exemptions list; counsellor line | [sf.gov — Learn about San Francisco rental laws](https://www.sf.gov/learn-about-san-francisco-rental-laws) | Confirmed; owner-reported 1940 date still not checked against a City record (FR-14) |

### Irregularities and new items from this pass

| # | Finding | Disposition |
|---|---|---|
| 164 | Whether an out-of-date occupancy entry in the Housing Inventory affects a licence already issued for the year is nowhere stated | Published as **FR-35**; the corrective action is on the open-questions page (Q-01, Q-11) |
| 165 | The licence duty (“before any annual or banked rent increase”) and the carve-out (“not required … for passthroughs”) are two official statements whose boundary is undefined | Published as **FR-33**; this site keeps the conservative reading |
| 166 | The City publishes its Housing Inventory submission as **public information** | Not previously stated on the site; added as suggestion **SG-11** (privacy policy should be explicit, not implicit) |
| 167 | The state cap page cites “Civil Code section 1974.12” in two link labels — a typographical error on the Attorney General's own page; the target section number is 1947.12 | Noted; the site links the correct section. No change to any figure |
| 168 | Six superseded editions remain published side by side (`docs/`, `dashboard/`, `review/`, `audit/`, `verified/`, `verification/`) with corrections visible only on the canonical flagged page | Kept as required by the build gate; consolidated behind one editions index as **SG-08** for the owner's decision |