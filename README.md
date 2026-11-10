# Rent Increase SF — review of two rent-controlled flats

**Live site:** <https://kanlerxz87-cyber.github.io/RentincreaseSF3/>

A source-linked review of what rent increases are lawful for two rent-controlled flats in a 1940
two-unit San Francisco building, what process the Rent Board requires of an **individual** owner, and
what a San Francisco tenant's lawyer would test. Every table row links an official source or is blank
and listed on the Flagged page — no value is estimated.

> **Not legal advice.** Confirm any figure on its effective date and confirm the process with a Rent
> Board counsellor (415-252-4600) and a California attorney before serving a notice.

## The front-page answer

**Yes — an individual owner must report to the Rent Board and hold a rent-increase licence.** Being a
person rather than a corporation makes no difference: the ordinance distinguishes by building size
(10+ units from 1 July 2022; 1–9 units and condominiums from 1 March 2023). The licence is generated
automatically from the annual Housing Inventory report and must be **in effect on the effective date**
of the increase, or the increase may be null and void. You do not file the notice with the Rent Board
and there is no per-increase application or petition for an annual or banked increase.

## This edition (10 November 2026)

| Path | What it is |
|---|---|
| `index.html` | Landing dashboard — the licence answer first, key figures, executive-summary table, category navigation, corrections, verification status |
| `pages/v2/executive-summary.html` | The one-page answer, 7-step sequence, lawful amounts per unit, tenant-lawyer risk list, bottom line |
| `pages/v2/license.html` | The licence and process in detail — who reports, how, deadlines, the separate Rent Board Fee, remedies |
| `pages/v2/laws.html` | Local ordinance, state Tenant Protection Act, federal fair housing, the pending 10% cap, and which rule governs |
| `pages/v2/units.html` | Per-unit ledgers, cents-exact options, notice deadlines, the rate-year rule, the two arithmetic traps |
| `pages/v2/notice.html` | Notice content, deadlines, reasons required / permitted / forbidden, a compliant template, service and proof |
| `pages/v2/tenant-review.html` | Fifteen-point stress test, the one-unit-or-both analysis, where a lawyer would look hardest |
| `pages/v2/practice.html` | Corporate versus individual practice — what official sources establish, and what they do not |
| `pages/v2/flagged.html` | Thirteen flagged items with what would close each, plus irregularities found in earlier editions |
| `pages/v2/sources.html` | Source register: 28 official sources, what each verifies, date read, and the gaps |
| `EXECUTIVE_SUMMARY.md` | The executive summary in Markdown |

## Headline figures (verified 10 November 2026)

| Item | Result | Source |
|---|---|---|
| Allowable annual increase, 1 Mar 2026 – 28 Feb 2027 | **1.6%** (prior year 1.4%) | [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) · [sf.gov](https://www.sf.gov/learn-about-rent-increases-san-francisco) |
| Allowable increase, 1 Mar 2027 – 29 Feb 2028 | **not yet published** — flagged | [sf.gov — Current Rates](https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit) |
| Rent-increase licence | Required of **all** owners; auto-generated from the annual Housing Inventory report; due 1 March; must be in effect on the effective date | [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) |
| Unit 1 | **3.0% = $119.85 → $4,114.85** effective 1 Feb 2027 (1.4% banked + 1.6% current), 30 days' notice; 1.6%-only alternative = $63.92 → $4,058.92 | [sf.gov — Banked](https://www.sf.gov/information/banked-rent-increases) · [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) |
| Unit 2 | **13.1% = $412.65 → $3,562.65** is the banked balance to Jun 2026 — a floor, not the June 2027 ceiling; 90 days' notice. **10.0% = $315.00 → $3,465.00** is a lawful phased step on 30 days' notice | [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) · [Civ. Code §827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) |
| State cap (Tenant Protection Act) | 8.8% for the SF area, 1 Aug 2026 – 31 Jul 2027 — **does not govern**; the local allowance is lower and the statute exempts stricter local control | [Civ. Code §1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) · [oag.ca.gov](https://oag.ca.gov/rentcaps) |
| Federal | No rent ceiling; the Fair Housing Act governs reasons | [42 U.S.C. §3604](https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm) |
| Pending | File #261020 would cap banked + capital-improvement increases at 10%/yr for three years — **Pending Committee Action, not law** | [Legistar](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770) |

## Corrections made in this edition

1. **Unit 2: 13.1% is not the June 2027 ceiling.** It is the banked balance accrued to June 2026. The
   June 2027 increase also includes the 2027-28 allowance, which is unpublished, so the ceiling cannot
   be stated yet.
2. **Rate year must match the effective date.** A notice effective after 28 February 2027 cannot use
   1.6%; the Rent Board instructs owners to use the rate in effect on the effective date.
3. Banking has **no three-year cap** — it reaches back to 1 April 1982 and never expires during a tenancy.
4. Unit 1's anniversary is **1 February**; the April 2026 continuation did not reset it.

## Verification

```bash
python3 tools/build_v2.py     # regenerate index.html, pages/v2/*, assets/v2.css
python3 tools/check_v2.py     # this edition: links, anchors, per-row sourcing, anonymisation, arithmetic
python3 verify_site.py        # dashboard edition
python3 tools/check_site.py   # review edition
python3 tools/verify_edition.py  # verified edition
python3 tools/audit_site.py   # whole repository
```

All pass on 2026-11-10. The site is plain HTML and CSS — no build step, no JavaScript, `.nojekyll`
present, served from `main` at the repository root.

## Privacy

No tenant names or initials, no street address, no unit numbers, no ZIP code and no neighbourhood name
appear anywhere in the published site. Occupants are described only as placeholders; the two flats are
"Unit 1" and "Unit 2". Lease dates, occupancy dates and dollar amounts are reproduced unchanged. The
privacy sweep is enforced by `tools/check_v2.py`, which fails the build if any identifier appears.

## Earlier editions, kept online

`pages/*.html` (7 Nov 2026 licence-first summary), `audit/` (consolidated audit), `verified/` (ten-page
verified guide), `docs/`, `dashboard/`, `review/`. They are preserved for provenance; where they
disagree with this edition, the corrections above apply.

## Coordination

Parallel agent sessions coordinate through [`COORDINATION.md`](COORDINATION.md) — task board, claims,
file scopes, and the merge/deploy record.
