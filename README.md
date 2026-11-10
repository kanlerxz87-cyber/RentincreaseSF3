# San Francisco Rent Increase Review

**Live site:** <https://kanlerxz87-cyber.github.io/RentincreaseSF3/>
**Executive summary:** [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md) · **Flagged for review:**
[live page](https://kanlerxz87-cyber.github.io/RentincreaseSF3/site/flagged.html)

A verified, source-linked review of what two rent-controlled units in a two-unit 1940 San Francisco building may
lawfully be charged, how to serve the notice, and what a tenant-side lawyer would test. Built for an individual
owner who has never dealt with the Rent Board.

**Every figure traces to an official source fetched on 10 November 2026.** Nothing is drawn from law-firm
summaries, landlord associations, advocacy explainers or news coverage. Values that no official source supports are
left blank and listed on the Flagged for review page rather than estimated.

---

## The answer, first

**An individual owner, not a corporation, still has to report to the Rent Board and hold a rent-increase licence.**
But you do **not** need the Board's approval of the amount, and you do **not** file the increase notice with it.

1. **Report into the Housing Inventory by 1 March every year.**
   [sf.gov](https://www.sf.gov/rent-board-housing-inventory) · [Admin. Code §37.15](https://www.sf.gov/information/sec-3715-reporting-obligations-licensing)
2. **Have a current licence on the effective date.** It is generated automatically when you report an occupied
   unit — no separate application, no fee. Without it the increase is unenforceable and the tenant need not pay it.

Order: **report → confirm the licence → serve the notice.** The licence is restored only *prospectively* if you
catch up later.

## Headline figures

| Item | Result | Source |
|---|---|---|
| Allowable increase 3/1/2026 – 2/28/2027 | **1.6%** (1.4% the prior year) | [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) · [announcement](https://www.sf.gov/news--annual-rent-increase-3126-22827-announced) |
| Unit 1 ($3,995, tenancy 1 Feb 2025) | **1.6% = $63.92 → $4,058.92** on 1 Feb 2027; **3.0% = $119.85 → $4,114.85** if the 1.4% is treated as banked | [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) |
| Unit 2 ($3,150, tenancy 1 Jun 2019) | **1.6% = $50.40**; up to **13.1% = $412.65 → $3,562.65**; **recommended phased 10.0% = $315.00 → $3,465.00** | [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) |
| Notice | 30 days if ≤10%, **90 days if >10%**; **+5 days if mailed** | [Civ. Code §827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) · [CCP §1013](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1013) |
| State cap (AB 1482) | 8.8% for this metro area — **does not apply**, because the local cap is lower | [Civ. Code §1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) · [CA AG](https://oag.ca.gov/rentcaps) |
| Federal | No rent ceiling; only the ban on discriminatory terms | [42 U.S.C. §3604](https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm) |

## Site map

| Page | Contents |
|---|---|
| [`site/index.html`](site/index.html) | Dashboard — the licence answer, key figures, and every unit option |
| [`site/executive-summary.html`](site/executive-summary.html) | The whole file in one page |
| [`site/process.html`](site/process.html) | Nine steps from coverage check to served notice |
| [`site/units.html`](site/units.html) | Both units, every lawful option to the cent |
| [`site/laws.html`](site/laws.html) | 26 verified propositions; local, state and federal layers |
| [`site/reasonable.html`](site/reasonable.html) | What "reasonable and normal" means; corporate vs individual practice |
| [`site/notice.html`](site/notice.html) | Notice requirements, a model notice, lawful and unlawful reasons |
| [`site/review.html`](site/review.html) | The nine checks a tenant-side lawyer would apply; one unit or both |
| [`site/sources.html`](site/sources.html) | Every source, with URL and retrieval date |
| [`site/flagged.html`](site/flagged.html) | The nine unverified, disputed or not-yet-law items |

## Privacy

No tenant name or initial, no street address, no ZIP code and no neighbourhood name appears in any published page
**or in any tracked file** — the location was supplied as internal information and this repository is public. Tenant
placeholders are used throughout. **Dates and dollar amounts are unchanged**, as instructed. No cited rule varies by
ZIP code: the Rent Ordinance is citywide.

A privacy pattern check runs in CI and fails the build on any match.

## Verification

```bash
python3 tools/build_consolidated.py    # regenerate site/ and the root landing page
python3 tools/verify_consolidated.py   # links, anchors, per-row official citation, privacy, maths
python3 tools/audit_site.py            # repository-wide link/anchor and privacy sweep
python3 verify_site.py                 # dashboard edition checks
python3 tools/check_site.py            # review edition checks
python3 tools/verify_edition.py        # verified edition checks
```

All six pass as of 10 November 2026. The build asserts every cents-exact result, so a wrong figure fails the build
rather than reaching a page. The row checker treats a table row without an official source link as an **error**, not
a warning.

Site is plain HTML and one stylesheet — no JavaScript, no build step, no external assets, `.nojekyll` present, so
GitHub Pages serves it directly from the repository root.

## Repository layout

| Path | What it is |
|---|---|
| `index.html`, `site/` | **Current edition** (10 November 2026). Root `index.html` is the landing dashboard; `site/` holds the categorized subpages. Both are generated by `tools/build_consolidated.py` so they cannot drift apart. |
| `EXECUTIVE_SUMMARY.md` | The standalone executive summary |
| `docs/`, `dashboard/`, `review/`, `audit/`, `verified/`, `pages/` | **Superseded** editions from earlier sessions, kept for provenance. They contain known errors; see F-09 on the Flagged page. |
| `tools/` | Site generator, content/source register, and the verification scripts |
| `COORDINATION.md` | Parallel-session task board, claims, and the PR/deploy record |

## Scope and limits

Not legal advice. Property facts (build year, unit count, rent history) are owner-reported and not
government-certified. Confirm coverage with a Rent Board counsellor on **415-252-4600** and have a California
attorney review any notice before it is served.
