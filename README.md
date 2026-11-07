# Current consolidated site — November 7, 2026

**Start here:** https://kanlerxz87-cyber.github.io/RentincreaseSF3/

The landing page is now the canonical **forefront executive summary** (Rent Board license question first, 7-step checklist, cents-exact figures) with categorized subpages under `pages/` (corrected forefront integration) and the consolidated audit under `audit/`. Read `EXECUTIVE_SUMMARY.md` for the markdown version. Individual-owner license requirements come first. All property facts are owner-reported, not government-certified. Missing verified values are blank; conditional calculations are not lawful-rent determinations. See `pages/flagged.html` and `audit/flagged.html`.

> **Forefront answer preserved:** Yes — individual owners need the rent-increase license too (no exemption). See the forefront card on the landing page and `EXECUTIVE_SUMMARY.md` §1.

- **Live site:** <https://kanlerxz87-cyber.github.io/RentincreaseSF3/> — Executive Summary, Units, Laws & Caps, Process & Notice, Flagged for Review
- **Not legal advice.** Confirm with SF Rent Board counselors **415-252-4600** before serving any notice.
- **Privacy:** no tenant names or initials, no street address, no ZIP. Dates and dollar amounts unchanged.
- **Sourcing rule:** every table row links an official source (sf.gov, leginfo, govinfo, hud.gov, ecfr.gov, sfgov.legistar.com) or is flagged — nothing inferred. Where two official sources disagree, both are published (see Flagged pages).

## All live editions (GitHub Pages — `main` / root)

| Path | What it is | Status |
|---|---|---|
| `index.html` + `pages/` | **Canonical forefront edition** — landing dashboard with forefront license Q&A (7 steps), stats, quick answers; 5 subpages (executive summary, units, laws & caps, process & notice, flagged). Corrected in this PR (forefront integration): anniversary Feb 1 fix, banking not capped at 3 yrs, license Step 0, source links per row. | Verified 2026-11-07 |
| `audit/` | **Consolidated audit edition** (Nov 7) — 6 pages: process & notice, units & calculations, tenant-lawyer review, flagged for review (12 items), sources & audit with per-row citations & privacy sweep | Verified 2026-11-07 |
| `verified/` | **Verified guide (10 pages)** — full 1982–2027 rate table, cents-exact ledgers (Unit 1 3.0% = $119.85; Unit 2 up to 13.1% = $412.65), notice planner + model letter, tenant-lawyer test, 32-source register | Verified 2026-11-07 |
| `docs/` | Full verification edition — deeper banking, FHA/FEHA, 17-item flagged, 27-source register | Verified prior, preserved |
| `dashboard/` | Dashboard edition — 10 pages, 1982–2027 table, worked calculations, legal framework, 22 sources | Verified prior, preserved |
| `review/` | Audit-trail edition — per-anniversary ledger, 21-row rule table, 15-point test, 27-assertion log | Verified prior, preserved |
| `EXECUTIVE_SUMMARY.md` | Executive summary in Markdown (forefront license Q&A first) | Verified 2026-11-07 |
| `tools/verify_edition.py` + `verify_site.py` + `tools/check_site.py` | Pre-publish checks: internal links/anchors, per-row citations, privacy sweep, math, no remote code | Checks pass |

## Headline findings (verified 7 November 2026)

| Item | Result | Source |
|---|---|---|
| Annual allowance 3/1/2026 – 2/28/2027 | **1.6%** (1.4% prior year) | [sf.gov announcement](https://www.sf.gov/news--annual-rent-increase-3126-22827-announced); [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) |
| Rent increase license | **Required, including for an individual owner of a 1–9 unit building.** Generated automatically from Housing Inventory report; reporting began Mar 1, 2023 for these buildings; deadline Mar 1 yearly; increase void without it on effective date | [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory); Admin. Code §37.15 |
| Must the increase notice itself be filed with the Rent Board? | **No** — annual and banked increases need no petition; the license is not a per-increase approval | [sf.gov — rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco); [sf.gov — banking](https://www.sf.gov/information/banked-rent-increases) |
| Unit 1 | **3.0% = $119.85 → $4,114.85** effective Feb 1, 2027 (1.4% banked + 1.6% current), 30-day notice (95 if mailed); fallback 1.6% = $63.92 → $4,058.92 | [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) |
| Unit 2 | **Up to 13.1% = $412.65 → $3,562.65** maximum (seven banked years), 90-day notice; **recommended phased 10.0% = $315.00 → $3,465.00** (stays lawful if pending 10%/yr cap passes) — conditional on zero prior increases | [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf); [Legistar #261020](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770) (pending, not law) |
| State cap AB 1482 | 8.8% for Aug 1, 2026 – Jul 31, 2027 — **not governing** because local cap is lower (Civ. Code §1947.12(d)(3)) | [oag.ca.gov](https://oag.ca.gov/rentcaps); [sf.gov AB 1482](https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482) |
| Federal | No federal rent ceiling; Fair Housing Act governs reasons | [42 U.S.C. §3604](https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm) |
| Pending | File #261020 would cap banked + capital-improvement increases at 10%/yr for 3 years; status **Pending Committee Action** — not law | [sfgov.legistar.com](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770) |

## Verification

```bash
python3 verify_site.py          # core site + dashboard: links, per-row citations, PII, math
python3 tools/check_site.py     # review edition: links/anchors
python3 tools/verify_edition.py # audit/verified: links, citations, privacy, no remote code
python3 tools/audit_site.py     # consolidated audit sweep
```

All four checks **pass** on 2026-11-07. The site is plain HTML + CSS, no JS build step, `.nojekyll` present, builds on GitHub Pages.

## Historical note (preserved)

Earlier editions (`docs/`, `dashboard/`, `review/`) remain live and unchanged. The prior standalone summary's unsupported catch-up recommendation is withdrawn in the current pages — see `audit/flagged.html` F-5 and `pages/flagged.html` F-5. Historical verification claims and source logs below describe prior sessions, not a fresh certification for the current landing; they are preserved in `COORDINATION.md`.

Parallel-session coordination: see [`COORDINATION.md`](COORDINATION.md) — cross-session task board, claims, merge and deploy records.

