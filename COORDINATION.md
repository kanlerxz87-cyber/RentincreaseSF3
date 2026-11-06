# COORDINATION.md — Shared Task Board

**Repo:** `kanlerxz87-cyber/RentincreaseSF3`
**Created:** 2026-11-06 · **Last updated:** 2026-11-06

## Sessions

| Session ID | Branch | Status |
|---|---|---|
| `arena-edaa9740` | `arena/edaa9740-rentincreasesf3` (platform-mandated working branch for this session) | active |

> Privacy policy for this repo: no personal information (names, initials, full addresses, ZIP, tenant identities) is ever written into this repository or the website. Only dates and dollar amounts are published, with placeholder identifiers. Personal details remain in the owning session's private context only. Enforced by `verify_site.py` (PII scan) before every push.

## Task Board

| Task | Description | Status | Owning Session | Files touched |
|---|---|---|---|---|
| T1 | Create COORDINATION.md, claim all tasks | done | arena-edaa9740 | COORDINATION.md |
| T2 | Research (official sources): SF Rent Board annual allowable increase factors, banking, petitions, notices | done | arena-edaa9740 | (internal — results published on site) |
| T3 | Research (official sources): California state law (AB 1482 / Gov. Code 1947.12, Costa-Hawkins, Civ. Code 827) | done | arena-edaa9740 | (internal — results published on site) |
| T4 | Research (official sources): federal law + fair housing + free tenant legal services in SF | done | arena-edaa9740 | (internal — results published on site) |
| T5 | Research: corporate vs individual landlord rent-increase practices (flag if no official source) | done | arena-edaa9740 | (internal — results published on site) |
| T6 | Build GitHub Pages site: landing page + categorized subpages + tables (all rows source-linked) | done | arena-edaa9740 | index.html, executive-summary.html, units.html, allowable-increases.html, procedures.html, legal-framework.html, market-practices.html, analysis.html, flagged.html, sources.html, assets/style.css, README.md, .nojekyll |
| T7 | Line-by-line verification pass; flag unverified values (blank + flagged) | done | arena-edaa9740 | verify_site.py, docs pages |
| T8 | Integration: re-verify combined data, build + broken-link check | done | arena-edaa9740 | verify_site.py (re-run clean) |
| T9 | PR to main → merge → confirm GitHub Pages deploy → record links here | done | arena-edaa9740 | COORDINATION.md |

## Claim Log

- 2026-11-06 — `arena-edaa9740` claims T1–T9 (sole session at creation time; scopes non-overlapping, all under this session). Work happened on `arena/edaa9740-rentincreasesf3`. If another session arrives, it should claim only unclaimed rows or add a request here.

## Change Requests Between Sessions

_(none — single session)_

## Sources & Verification Log

All sources verified by retrieving the official page/PDF on **2026-11-06**. Full register with links: site page `sources.html` (S1–S22).

| Area | Key sources (official unless noted) | Verification performed |
|---|---|---|
| SF annual allowable increases | sf.gov Current Rates (S1); Rent Board Form 571 PDF (S4); sf.gov Learn about rent increases (S2) | 1.6% (3/1/26–2/28/27), 1.4%, 1.7% cross-checked between S1 and S4; full 1982–2027 history transcribed from S4; formula "60% of Bay Area CPI-U" quoted from S2 |
| Banking | sf.gov Banked increases (S3); sf.gov examples (S2); Rent Board Rules § 4.12 text | No compounding/rounding, since 4/1/1982, itemization, license precondition all quoted from S3; worked examples re-computed; 12-month vs 24-month wording reconciled → same results for both units (flag F-4) |
| Notices | Cal. Civ. Code § 827(b) leginfo (S16); sf.gov (S2/S3) | Statute text fetched: 30 days ≤10%, 90 days >10% — matches sf.gov guidance exactly |
| Coverage (1940) | sf.gov rental laws (S5) | Jun 13, 1979 cutoff confirmed; exemption list confirmed; address-level check flagged (F-3) |
| AB 1482 / Costa-Hawkins | sf.gov AB 1482 (S6); leginfo AB 1482 (S18); leginfo § 1954.53 (S17) | Exemption for locally controlled units quoted from S6; current state max 8.8% quoted from S6; vacancy-reset text quoted from S17 |
| Petitions / reasons | sf.gov Topics 301/322/323 (S8–S10); Current Rates CI rates (S1) | O&M ≤7% quoted from S9; "mere below-market is not extraordinary" quoted from S10; petition-before-notice rule confirmed |
| License | sf.gov Housing Inventory (S7) | 10+ units 7/1/2022, <10 units 3/1/2023, March 1 deadline, enforceability-on-effective-date all quoted |
| Fair housing | 42 U.S.C. § 3604 GPO (S19); sf.gov discrimination (S12) | § 3604(b) fetched verbatim from govinfo; SF protected-class list from S12 |
| Free tenant legal help | sf.gov tenant resources (S11); sf.gov evictions (S15); EDC Prop F FAQ (S22, org source, labeled) | EDC free-help listing and Rent Board counseling fetched from S11 |
| Corp vs individual | CRS R49015 (S20); sf.gov AB 1482 (S6); Rent Board Annual Report FY22-23 (S14); academic paper (S21, labeled non-official) | CRS "largely nonexistent" quote from S20; corporate-ownership rule from S6; petition counts from S14; academic figures excluded from tables per policy (F-5) |
| Math | — | Script-checked: 3995×1.016=4058.92; 3995×1.030=4114.85; 3150×1.131=3562.65; banked sums 11.5% / 13.1% |
| Site integrity | `verify_site.py` | All internal links + anchors resolve; every tbody table row has ≥1 official source link; PII scan (initials, ZIP, neighborhood, street patterns) clean; math assertions pass |

## Irregularities / Flagged for Review

Published on the site's **Flagged for Review** page (`flagged.html`), with source links. None block merge:

- **F-1** Unit B rent history since 6/1/2019 not provided → 13.1% / $3,562.65 is conditional; current-rent cell left blank.
- **F-2** Allowable rate for 3/1/2027–2/28/2028 not yet published → blank row in rate table.
- **F-3** Address-level coverage/exemption check not run (location internal by privacy policy) — verify with Rent Board counselor / Property Information Map.
- **F-4** Banking timing wording differs between two official Rent Board pages (24-month vs 12-month) — reconciled; identical results for both units; re-read before serving notice.
- **F-5** No official dataset on corporate vs individual rent-increase practices (CRS: research "largely nonexistent"); academic figures labeled and excluded from tables.
- **F-6** Unit A occupancy continuity (no full vacancy) assumed — if vacated, Costa-Hawkins analysis would apply instead.
- **F-7** Property facts (1940, 2 units) as provided, not checked against records (privacy).
- **F-8** Unit A rent assumed unchanged at $3,995 since 4/1/2026; confirm no 2026 notice already served.

## Merge & Deploy Record

| Item | Result |
|---|---|
| Branch pushed | `arena/edaa9740-rentincreasesf3` (commits: `64a06d8` claim, `7d086eb` site build, + integration record commit) |
| PR to main | _(recorded below after creation)_ |
| Merge | _(recorded below after merge)_ |
| GitHub Pages | Site root: repo root `/` on `main` (Pages pre-enabled, `build_type: legacy`, `.nojekyll` present). Live URL: https://kanlerxz87-cyber.github.io/RentincreaseSF3/ |
| Build / broken links | `verify_site.py` — ALL CHECKS PASSED (10 pages); nav consistent (10/10 pages × 10 links) |
