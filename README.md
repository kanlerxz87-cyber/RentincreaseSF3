# Rental Increase SF — verified research site

**Live site:** <https://kanlerxz87-cyber.github.io/RentincreaseSF3/>

A static GitHub Pages dashboard answering one owner's questions about raising rent on two rent-controlled units in a two-unit San Francisco building (built 1940). The Rent Board notification/licence question comes first, because it decides whether any increase is enforceable at all.

Every table row links an official source. Where an official value does not exist, the cell is left blank and the item is published on the **Flagged for review** page rather than guessed.

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
| [`pages/discrimination.html`](pages/discrimination.html) | One unit or both units? Fair-housing analysis |
| [`pages/requirements.html`](pages/requirements.html) | Every requirement in the brief, its status and its evidence |
| [`pages/sources.html`](pages/sources.html) | 25-source register with what each supports |
| [`pages/flagged.html`](pages/flagged.html) | 16 flagged items: unverified, blank, inconsistent or corrected |

Markdown summary: [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md).

## Headline results (verified 10 November 2026)

| Item | Result | Official source |
|---|---|---|
| Rent-increase licence for an individual owner of a 1–9 unit building | **Required** — automatic once the Housing Inventory report is filed; must be in effect on the **effective date**; requirement applies from 1 March 2023; 1 March annual deadline; no monetary penalty for late filing | [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) |
| Per-increase application or notice filing | **Not required** for annual or banked increases | [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) · [sf.gov — banking](https://www.sf.gov/information--banked-rent-increases) |
| Annual allowance 1 Mar 2026 – 28 Feb 2027 | **1.6%** (1.4% prior year) | [sf.gov](https://www.sf.gov/learn-about-rent-increases-san-francisco) · [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) |
| Unit A, 1 Feb 2027 | **3.0% = $119.85 → $4,114.85** (1.6% annual + 1.4% banked), 30 days' notice; 1.6% = $63.92 is the fallback | [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) · [banking](https://www.sf.gov/information--banked-rent-increases) |
| Unit B (conditional on no increase since 2019) | **10.0% = $315.00 → $3,465.00** recommended; **13.1% = $412.65 → $3,562.65** is the maximum, 90 days' notice | [banking](https://www.sf.gov/information--banked-rent-increases) · [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) |
| Notice | 30 days if ≤10%, 90 days if >10%; +5 days by mail in California | [Civ. Code § 827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) · [CCP § 1013](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1013) |
| State cap | 8.8% for the San Francisco area from 1 Aug 2026; **not governing** because the local cap is lower | [oag.ca.gov](https://oag.ca.gov/rentcaps) · [Civ. Code § 1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) |
| Federal | No rent ceiling; fair housing governs the reasons | [42 U.S.C. § 3604](https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm) |
| Pending | File #261020 would cap banked + capital-improvement increases at 10%/yr; **Pending Committee Action**; Rent Board posted a 9 Nov 2026 notice | [Legistar](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770) |

## Privacy

Tenant and owner names are replaced with **Tenant A–D**. Dates and dollar amounts are unchanged. The ZIP code, neighbourhood and street address are **not published** — unit-level facts plus a location would identify the tenants, and the rules cited apply citywide with no ZIP-level variant. Source registers and the internal working files are not linked from the site.

## Build and verification

The site is generated from Python modules so that content and checks share one source of truth:

```bash
python3 tools/build_dashboard.py     # writes assets/style.css, index.html, pages/*.html
python3 tools/verify_core_site.py    # gate for the canonical site
python3 tools/audit_site.py          # whole-repo link/anchor + canonical row-source audit
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

---

## Consolidated review edition (verified 10 November 2026)

A second, additive edition lives under `site/` — ten categorized pages generated from a single
source register, with a stricter gate than the canonical site. The canonical root site above is unchanged;
a link banner on the root page points here.

| Page | Contents |
|---|---|
| [`site/index.html`](site/index.html) | Dashboard — the licence answer first, key figures, every unit option |
| [`site/executive-summary.html`](site/executive-summary.html) | The whole file in one page |
| [`site/process.html`](site/process.html) | Nine steps from coverage check to served notice |
| [`site/units.html`](site/units.html) | Both units, every lawful option to the cent |
| [`site/laws.html`](site/laws.html) | 26 verified propositions; local, state and federal layers; 1982–2027 rate table |
| [`site/reasonable.html`](site/reasonable.html) | What "reasonable and normal" means; corporate vs individual practice |
| [`site/notice.html`](site/notice.html) | Notice requirements, model notice, lawful vs unlawful reasons |
| [`site/review.html`](site/review.html) | The nine checks a tenant-side lawyer would apply; one unit or both |
| [`site/sources.html`](site/sources.html) | Every source, with URL and retrieval date |
| [`site/flagged.html`](site/flagged.html) | Nine unverified, disputed or not-yet-law items |

`CONSOLIDATED_REVIEW.md` is the standalone long-form version of the same review.

```bash
python3 tools/build_consolidated.py     # regenerate site/
python3 tools/verify_consolidated.py    # links, anchors, per-row official citation, privacy, maths
python3 tools/link_consolidated.py      # add/refresh the banner on the root page (idempotent)
```

The consolidated gate differs from the canonical gate in three ways: a table row with **no official
source link is an error, not a warning**; every cents-exact result is asserted at build time, so a wrong
figure fails the build; and every external link must also appear in the source register.
