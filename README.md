# Rental Increase SF — verified research site

**Live site:** <https://kanlerxz87-cyber.github.io/RentincreaseSF3/>

A static GitHub Pages dashboard answering one owner's questions about raising rent on two units reported as rent-controlled in a San Francisco building reported as built in 1940 (total building size and coverage unverified). The Rent Board notification/licence question comes first, because it decides whether any increase is enforceable at all.

Canonical dashboard table rows link official sources for the governing rule; owner-supplied facts are not thereby verified. Unconfirmed values and limitations are listed on **Flagged for review**. Archived editions still hold 114 table rows without an official source link (measured by `tools/row_source_audit.py`, FR-24) and repeat statements since corrected; they should not be relied on as current advice.

---

## Start here

| Page | What it answers |
|---|---|
| [`index.html`](index.html) — Dashboard | Short answers, key figures, the 9 November 2026 update, category tiles |
| [`pages/executive-summary.html`](pages/executive-summary.html) | Executive summary with the licence question at the forefront |
| [`pages/process.html`](pages/process.html) | Step-by-step licence and notice process, notice-date planner, who to call |
| [`pages/units.html`](pages/units.html) | Unit A and Unit B: every lawful option, with arithmetic |
| [`pages/laws.html`](pages/laws.html) | Local ordinance, California statutes, federal fair housing, full 1982–2027 rate table |
| [`pages/reasonable.html`](pages/reasonable.html) | What "reasonable and normal" can and cannot be measured against |
| [`pages/practice.html`](pages/practice.html) | Corporate vs individual practice, official evidence only |
| [`pages/notice.html`](pages/notice.html) | Required contents, service deadlines, model notice, lawful and unlawful reasons |
| [`pages/review.html`](pages/review.html) | 16-point tenant-lawyer stress test |
| [`pages/questions.html`](pages/questions.html) | Open questions: what must be answered before an amount is chosen, and how to find each answer |
| [`pages/suggestions.html`](pages/suggestions.html) | Site-improvement proposals for owner review — **none implemented**, each with effort, risk and an empty decision field |
| [`pages/discrimination.html`](pages/discrimination.html) | One unit or both units? Fair-housing analysis |
| [`pages/requirements.html`](pages/requirements.html) | Every requirement in the brief, its status and its evidence |
| [`pages/questions.html`](pages/questions.html) | **Open questions**: 14 blocking questions, 12 already settled, the documents to collect, 8 ways to find what is missing, and how each answer changes the number |
| [`pages/suggestions.html`](pages/suggestions.html) | **Suggestions for review**: 12 improvement proposals with impact and effort, all marked *Proposed* — nothing is implemented until an ID is accepted — plus 6 rejected ideas and why |
| [`pages/sources.html`](pages/sources.html) | source register with what each supports |
| [`pages/flagged.html`](pages/flagged.html) | 39 flagged items: unverified, blank, inconsistent or corrected |

Markdown summary: [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md).

## Headline results (verified 13 November 2026 for the licence, notice and pending-law sources; the rest on 11 November 2026)

| Item | Result | Official source |
|---|---|---|
| **State or local law?** | **Local.** The duty to report into the Housing Inventory and hold a rent-increase licence comes from **San Francisco Ordinance No. 265-20** (adopted 2020, effective 18 January 2021), which amended the City's Rent Ordinance. The 2023 date owners cite is the **phase-in**: reporting “will begin on March 1, 2023” for condominiums and buildings with fewer than 10 units. No California statute imposes a rent-board filing or licence; § 1947.12(m)(2) says the state cap is “not intended to expand or limit the authority of local governments”. | [sf.gov — Ordinance 265-20](https://www.sf.gov/news--new-legislation-creates-housing-inventory-and-requires-owners-obtain-license-imposing) · [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) · [Civ. Code § 1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) |
| A pre-condition the site had not listed | **Civ. Code § 1942.4** bars a landlord from issuing “a notice of a rent increase” while substandard conditions that a housing official has flagged in writing stand unabated for more than 35 days without good cause; damages $100–$5,000 plus fees. Added 13 Nov 2026 to the notice, process and summary pages. | [Civ. Code § 1942.4](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.4) |
| Pending legislation, re-checked 13 Nov 2026 | File #261020 status is still **Pending Committee Action** (last recorded action 7 Oct 2026) — not law. | [Legistar](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770) |
| Rent-increase licence for an individual owner of a 1–9 unit building | **Required** — automatic once the Housing Inventory report is filed; must be in effect on the **effective date**; requirement applies from 1 March 2023; 1 March annual deadline; no monetary penalty for late filing | [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) |
| Per-increase approval petition | **Not required** for ordinary annual or banked increases; separate notice-copy filing not established (FR-20) | [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) · [sf.gov — banking](https://www.sf.gov/information--banked-rent-increases) |
| Annual allowance 1 Mar 2026 – 28 Feb 2027 | **1.6%** (1.4% prior year) | [sf.gov](https://www.sf.gov/learn-about-rent-increases-san-francisco) · [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) |
| Unit A, 1 Feb 2027 | **3.0% = $119.85 → $4,114.85** (1.6% annual + 1.4% banked), 30 days' notice; 1.6% = $63.92 is the fallback | [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) · [banking](https://www.sf.gov/information--banked-rent-increases) |
| Unit B (conditional on no increase since 2019) | **10.0% = $315.00 → $3,465.00** illustrative, not an established normal rate; **13.1% = $412.65 → $3,562.65** is the conditional maximum **for an effective date on or before 28 February 2027** (and 7-year banked floor on 1 June 2027 before the unannounced 2027–28 rate), 90 days' notice | [banking](https://www.sf.gov/information--banked-rent-increases) · [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) |
| Notice | 30 days if ≤10%, 90 days if >10%; +5 days by mail in California | [Civ. Code § 827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) · [CCP § 1013](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1013) |
| State cap | 8.8% for the San Francisco area from 1 Aug 2026; **not governing** because the local cap is lower | [oag.ca.gov](https://oag.ca.gov/rentcaps) · [Civ. Code § 1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) |
| Federal | Fair housing prohibits discriminatory rental terms; federal program rules may also apply | [42 U.S.C. § 3604](https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm) |
| Pending | File #261020 would cap banked + capital-improvement increases at 10%/yr; **Pending Committee Action**; Rent Board posted a 9 Nov 2026 notice | [Legistar](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770) |

## Privacy

Tenant and owner names are replaced with **Tenant A–F**. Dates and dollar amounts are unchanged. The ZIP code, neighbourhood and street address are **not published** — unit-level facts plus a location would identify the tenants, and the rules cited apply citywide with no ZIP-level variant. Source registers and the internal working files are not linked from the site.

## Build and verification

The site is generated from Python modules so that content and checks share one source of truth. `pages/questions.html` and `pages/suggestions.html` come from `tools/site_pages_decide.py`:

```bash
python3 tools/build_dashboard.py     # writes assets/style.css, index.html, pages/*.html
                                     # (content lives in tools/site_pages_core.py, site_pages_rules.py,
                                     #  site_pages_ref.py and site_pages_decide.py; sources in site_layout.py)
python3 tools/verify_core_site.py    # gate for the canonical site
python3 tools/audit_site.py          # whole-repo link/anchor + canonical row-source audit
python3 tools/row_source_audit.py    # every table row on every page: official link or counted exception
python3 verify_site.py               # dashboard edition (preserved)
python3 tools/check_site.py          # review edition (preserved)
python3 tools/verify_edition.py      # audit/ + verified/ editions (preserved)
```

`tools/verify_core_site.py` fails the build if: any internal link or anchor is broken; any table row lacks a link to an official domain (sf.gov, portal.sfrb.org, sfgov.legistar.com, leginfo.legislature.ca.gov, codelibrary.amlegal.com, oag.ca.gov, calcivilrights.ca.gov, govinfo.gov, justice.gov, hud.gov, ecfr.gov); any row's cell count disagrees with its header; any tenant initial, ZIP code, neighbourhood or street address appears; any published figure fails its arithmetic or notice-date assertion; a `<script>` element appears; or a prior edition has been deleted.

CI runs the same commands on every push and pull request (`.github/workflows/site-checks.yml`), and fails if the committed HTML differs from a fresh build.

## Preservation of earlier editions

Earlier editions remain online unchanged for audit: `docs/` (verification edition), `dashboard/` (dashboard edition), `review/` (audit-trail edition), `audit/` (consolidated audit), `verified/` (verified guide). They are **not** the canonical pages and are not linked from the main navigation. Where they disagree with the current pages, the corrections are listed on `pages/flagged.html` (FR-15).

## Coordination

Parallel-session task board, claims, merge and deploy records: [`COORDINATION.md`](COORDINATION.md).

**Not legal advice.** Confirm with the SF Rent Board counselling line (415-252-4600) and a California lawyer before serving any notice.

## Independent verification edition — `verification/` (10 November 2026)

A second, self-contained pass re-fetched **every** official source cited on this site and re-ran the
arithmetic from the published percentages. It confirms every headline figure here. It is published as
its own edition so that the canonical pages above were not rewritten:

**Start at [`verification/index.html`](verification/index.html)** — overview · [executive summary](verification/executive-summary.html) ·
[licence and process](verification/license.html) · [laws and caps](verification/laws.html) ·
[units and arithmetic](verification/units.html) · [notice and reasons](verification/notice.html) ·
[tenant-lawyer test](verification/tenant-review.html) · [owner practice](verification/practice.html) ·
[flags F-11…F-23](verification/flagged.html) · [source register](verification/sources.html)

What it adds:

- **The `13.1%` Unit B figure is a floor, not the June 2027 ceiling** (now reflected in the canonical pages as "maximum for an effective date on or before 28 February 2027", FR-17). It is the balance banked to
  June 2026. An increase effective 1 June 2027 must also use the allowance in effect on that date
  (1 Mar 2027 – 29 Feb 2028), which the Rent Board has not published — so no June 2027 maximum can be
  stated yet. ([sf.gov — rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco))
- **The 7% in Admin. Code §37.3 is a ceiling on the formula, not an available increase.** The published
  allowance (1.6%) governs. ([§37.3](https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_admin/0-0-0-70881))
- **The Rent Board Fee is a separate obligation from the rent-increase licence** — $59.00 per dwelling
  unit for 2026-27, due 1 March, 5% monthly penalty capped at 15%, 50% recoverable from tenants,
  exemption window closing 14 December 2026. No official page links the fee to the licence either way,
  so that question is published as open (F-15), not inferred.
  ([sf.gov — Rent Board Fee](https://www.sf.gov/rent-board-fee))
- **Security-deposit interest of 4.2%** (1 Mar 2026 – 28 Feb 2027) is a separate annual duty that does
  not consume a rent allowance.
- **The §6.14 / last-original-occupant rule is narrower than "vacancy resets rent"** — it reaches
  *subtenants* only after the **last** original occupant permanently vacates, and depends on a written
  §6.14 notice served in time. The Rent Board says §6.14 notices can apply to subsequent co-tenants; its Costa-Hawkins discussion distinguishes co-tenants from subtenants. Obtain legal advice.
  ([sf.gov — §6.14 and Costa-Hawkins](https://www.sf.gov/information--rent-increases-under-section-614-and-costa-hawkins))

Gate: `python3 tools/check_v2.py` — 212 data rows (210 with an official source, 2 blank and flagged),
every internal link and anchor resolving, anonymisation, and the arithmetic recomputed from the
published percentages. The personal-data detectors are imported from `tools/privacy_scan.py`, so no
script in this repository spells out the values it protects.
