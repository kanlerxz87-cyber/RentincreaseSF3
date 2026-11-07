# RentincreaseSF3

**Verified analysis of lawful, reasonable and normal rental increases** for a rent-controlled, two-unit
residential building constructed in **1940** in San Francisco (specific location withheld for
privacy — all cited rules apply citywide). Personal information anonymized; dates and dollar amounts preserved.

## Live site (GitHub Pages: `main` / root)

**Root landing + core pages:** <https://kanlerxz87-cyber.github.io/RentincreaseSF3/>
→ [Dashboard](https://kanlerxz87-cyber.github.io/RentincreaseSF3/) · [Executive Summary](https://kanlerxz87-cyber.github.io/RentincreaseSF3/pages/executive-summary.html) · [Units](https://kanlerxz87-cyber.github.io/RentincreaseSF3/pages/units.html) · [Laws & Caps](https://kanlerxz87-cyber.github.io/RentincreaseSF3/pages/laws.html) · [Process & Notice](https://kanlerxz87-cyber.github.io/RentincreaseSF3/pages/process.html) · [Flagged for Review](https://kanlerxz87-cyber.github.io/RentincreaseSF3/pages/flagged.html)

The **forefront of the Executive Summary** answers the owner's #1 question step-by-step: *Do I, as an individual owner (not a corporation), still need to inform the Rent Board and get a license before notifying tenants?* **Yes — every owner must.** See the [Executive Summary](https://kanlerxz87-cyber.github.io/RentincreaseSF3/pages/executive-summary.html) forefront table and the 7-step checklist on the [Dashboard](https://kanlerxz87-cyber.github.io/RentincreaseSF3/).

- **Not legal advice.** Consult SF Rent Board counselors **415-252-4600** and a California attorney before acting.
- **Watch item:** SF Legistar File #261020 (pending, **not law** as of 2026-11-07) would cap combined banked + capital-improvement increases at 10%/yr for three years — re-check before serving any banked notice >10%.
- **Source policy:** every table row cites an official source (sf.gov, leginfo.legislature.ca.gov, govinfo.gov, hud.gov, ecfr.gov, sfgov.legistar.com) or is flagged — never guessed. See each edition's Flagged for Review page.

## Detailed markdown summary

The one-page research record is in [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md) — same forefront (license steps first), same cents-exact figures, fully source-linked. It mirrors the site's Executive Summary and is the file to share with a landlord attorney.

## Four independently verified editions (all live, all anonymized)

| Edition | URL | What it is |
|---|---|---|
| **Core site — integrated forefront** (PR #2 + this PR #12) | <https://kanlerxz87-cyber.github.io/RentincreaseSF3/> | Landing dashboard with forefront license Q&A (7 steps), stats, quick answers; 5 subpages with source-linked tables (units, laws, process, flagged) |
| **Full verification edition** (PR #3) | <https://kanlerxz87-cyber.github.io/RentincreaseSF3/docs/> | Deeper verification: cents-exact banking (Unit 2: up to 11.5%/13.1%), Housing Inventory license, full 1982–2027 rate table, FHA/FEHA analysis, 17-item flagged register, 27-source register |
| **Dashboard edition** (PR #9) | <https://kanlerxz87-cyber.github.io/RentincreaseSF3/dashboard/> | 10-page dashboard with full rate table, worked Unit A/B calculations, step-by-step notice procedure, legal framework, market practices, one-vs-both analysis, 22-source register |
| **Audit-trail edition** (PR #5) | <https://kanlerxz87-cyber.github.io/RentincreaseSF3/review/> | Per-anniversary ledger, 21-row rule table, notice deadline planner + model letter, 15-point tenant-lawyer test, 27-assertion verification log |

All editions are static HTML; occupant names/initials never appear; dates and dollar amounts unchanged.

## Headline results (independently recomputed, cents-exact)

Annual cap **1.6%** for 3/1/2026–2/28/2027 (1.4% prior year) — [sf.gov — 1.6% announcement](https://www.sf.gov/news--annual-rent-increase-3126-22827-announced); Unit 1 **3.0% = $119.85 → $4,114.85** on 1 Feb 2027 (1.4% banked + 1.6% current; anniversary Feb 1); Unit 2 **up to 13.1% = $412.65 → $3,562.65** if never increased since Jun 1, 2019 (conditional — rent history must verify), with 10% phased option while File #261020 is pending. License must be in effect on effective date — [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory).

## Verification

- Site builds as static HTML (no build step; `.nojekyll` present).
- `verify_site.py` — internal links, per-row source chips, PII scan, and math checks: **ALL CHECKS PASSED** (2026-11-07).
- `tools/check_site.py` — 11 review-edition pages + external links: **No broken internal links or anchors.**

See [`COORDINATION.md`](COORDINATION.md) for the parallel-session task board, source registers, and deployment record.

## Coordination

Parallel work is coordinated via [`COORDINATION.md`](COORDINATION.md) — claim tasks there before editing; shared outputs (index, navigation) are changed only by the final integration session. This session (arena/b4324bac) is the **forefront integration** that puts the license Q&A first across the core site while preserving all prior editions.
