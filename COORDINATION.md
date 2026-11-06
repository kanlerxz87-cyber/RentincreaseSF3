# COORDINATION.md — Shared Task Board

Repository: `kanlerxz87-cyber/RentincreaseSF3`
Purpose: Collect, organize, analyze and publish a rent-increase compliance dossier for two
rent-controlled units in San Francisco (Outer Sunset, ZIP 94122), with a GitHub Pages site.

## How to use this board

1. Read this file before starting any work.
2. Claim a task by writing your **session ID** and **file scope** in the row below.
3. `git commit` + `git push` the claim **immediately**, before editing any files.
4. Never start a task another session has claimed.
5. Keep scopes non-overlapping. One branch per session/task: `session-<id>/<task>`.
6. Small, frequent commits. `git pull --rebase` before every push.
7. On conflict: stop, resolve without discarding the other session's work, log it here.
8. `needs review` = published on the **Flagged for Review** page; it does **not** block anything.
9. Nothing is marked `verified` unless it was checked against an official source **and** that
   source is linked here.
10. Shared outputs (combined table data, site `index.html`, navigation) are edited **only** by the
    final integration session (T12), after all other tasks are done.
11. Stale claims: if a session crashed or its claim is >60 min old with no commits, another session
    may take over — note the handoff in the log below.

## Session registry

| Session ID | Branch | Role | Status |
| --- | --- | --- | --- |
| `session-9d958fa3` | `arena/9d958fa3-rentincreasesf3` | All tasks T1–T12 (single-session run; also acts as the final integration session) | active |

## Task board

| ID | Task | Status | Owner | Files in scope |
| --- | --- | --- | --- | --- |
| T1 | Repo audit & baseline (inventory, git state, Pages config) | done | session-9d958fa3 | `docs/audit/repo-audit.md` |
| T2 | Research & verify **San Francisco local law** (Rent Ordinance Ch. 37, Rent Board AGA rates, notice, license, banking) | done | session-9d958fa3 | `docs/law/local-sf.md`, `data/sf-aga-history.csv` |
| T3 | Research & verify **California state law** (Costa-Hawkins, AB 1482, Civ. Code §827, DIR CPI) | done | session-9d958fa3 | `docs/law/state-ca.md` |
| T4 | Research & verify **Federal law** (Fair Housing Act, absence of federal rent control, HUD) | done | session-9d958fa3 | `docs/law/federal.md` |
| T5 | Anonymize unit data + compute lawful maximum increases (Unit A / Unit B) | done | session-9d958fa3 | `data/units.csv`, `docs/analysis/unit-calculations.md` |
| T6 | Discrimination analysis: raise one unit vs both; fair-housing checklist | done | session-9d958fa3 | `docs/analysis/discrimination-review.md` |
| T7 | Corporate vs individual landlord practice comparison | done | session-9d958fa3 | `docs/analysis/practice-comparison.md` |
| T8 | Tenant-advocate red-team review checklist (would it survive an SF tenant lawyer?) | done | session-9d958fa3 | `docs/analysis/red-team-review.md` |
| T9 | Executive summary | done | session-9d958fa3 | `docs/executive-summary.md`, `EXECUTIVE_SUMMARY.md` |
| T10 | Site build (clean dashboard landing page + categorized subpages, tables with source links) | done | session-9d958fa3 | `index.html`, `assets/`, `pages/` |
| T11 | Verification pass: every table row has an official source link; no broken links; no inferred values | done | session-9d958fa3 | `docs/verification/link-check.md`, `tools/check_links.py` |
| T12 | Final integration: merge, re-verify combined data, build check, PR → `main`, merge, confirm Pages deploy | done | session-9d958fa3 | (integration only) |

## Verified source register (official / primary only)

Every value published on the site must trace to a row in this register.

| # | Source | Publisher | URL | What it verifies | Retrieved |
| --- | --- | --- | --- | --- | --- |
| S1 | Current Rates, including Rent Increase, Relocation, Sec. Deposit | SF Rent Board (sf.gov) | https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit | Allowable rent increase 1.6% (3/1/2026–2/28/2027); 1.4% (3/1/2025–2/28/2026); 1.7% (3/1/2024–2/28/2025); security deposit interest 4.2% / 5.0% | 2026-11-06 |
| S2 | 571 Allowable Annual Increases (all years) | SF Rent Board (sf.gov PDF) | https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf | Full historical AGA table back to 1982 — needed for banked-increase math | 2026-11-06 |
| S3 | Learn about rent increases in San Francisco | SF Rent Board (sf.gov) | https://www.sf.gov/learn-about-rent-increases-san-francisco | 30-day / 90-day notice, +5 days if mailed, base rent only, no rounding up, once per 12 months, rent increase license | 2026-11-06 |
| S4 | Allowable rent increases | SF Rent Board (sf.gov) | https://sf.gov/information/allowable-rent-increases | Anniversary date rule; passthroughs excluded from base rent | 2026-11-06 |
| S5 | Annual rent increases | SF Rent Board (sf.gov) | https://www.sf.gov/information--annual-rent-increases | Worked calculation example; no petition required for annual increases | 2026-11-06 |
| S6 | Banked Increases (Rent Board Rules & Regs / Fact Sheet) | SF Rent Board (sf.gov) | https://www.sf.gov/information--banked-increases | Banking of unused annual increases | 2026-11-06 |
| S7 | San Francisco Administrative Code, Chapter 37 (Residential Rent Stabilization & Arbitration Ordinance) | City & County of SF | https://www.sf.gov/departments--rent-board/ (ordinance text) | Statutory basis of rent control; §37.2A annual increases; §37.3A | 2026-11-06 |
| S8 | Costa-Hawkins Rental Housing Act, Cal. Civ. Code §§1954.50–1954.535 | CA Legislative Information | https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=CIV&division=3.&title=5.&part=4.&chapter=2.7&article= | Vacancy decontrol; preemption limits | 2026-11-06 |
| S9 | Tenant Protection Act of 2019 (AB 1482), Cal. Civ. Code §1947.12 | CA Legislative Information | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12 | Statewide 5% + CPI cap, max 10%; exemption for units under stricter local ordinance | 2026-11-06 |
| S10 | Cal. Civ. Code §827 (notice of change in terms of tenancy) | CA Legislative Information | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827 | 30-day / 90-day statutory notice | 2026-11-06 |
| S11 | Cal. Civ. Code §1946.2 (just cause) | CA Legislative Information | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1946.2 | Statewide just cause eviction | 2026-11-06 |
| S12 | CA Dept. of Industrial Relations — Consumer Price Index | State of CA DIR | https://www.dir.ca.gov/dlse/CPI.html | Regional CPI used for the AB 1482 cap | 2026-11-06 |
| S13 | Fair Housing Act, 42 U.S.C. §§3601–3619 | U.S. Dept. of Justice / HUD | https://www.justice.gov/crt/fair-housing-act-1 | Federal anti-discrimination in housing | 2026-11-06 |
| S14 | HUD — Fair Housing / Rent regulation | U.S. HUD | https://www.hud.gov/program_offices/fair_housing_equal_opp | Federal scope: no federal rent control for private unsubsidized housing | 2026-11-06 |
| S15 | CA Civil Rights Department — Housing Discrimination | State of CA CRD | https://calcivilrights.ca.gov/housing/ | State FEHA/Civil Rights Act housing protections + free complaint process | 2026-11-06 |
| S16 | SF Human Rights Commission / SF Fair Housing | City & County of SF | https://sf-hrc.org/ | Local fair housing enforcement | 2026-11-06 |

## Irregularities / needs-review log

Tracked on the site's **Flagged for Review** page (`pages/flagged.html`). Summary:

| # | Item | Type | Disposition |
| --- | --- | --- | --- |
| F1 | Repo contained only a bare `README.md` with a single line and no trailing newline; no data, no site, no CI. | Repo irregularity | Resolved by T10 (site built from scratch). |
| F2 | Third-party sites report conflicting 2026–27 SF AGA (1.6% vs 1.7%). | Source conflict | 1.6% adopted — official sf.gov (S1). Conflicting sources listed on Flagged page. |
| F3 | Unit 2 has no recorded increases since 6/1/2019 → large banked amount; requires a **rent increase license** (Housing Inventory) before any increase can take effect. | Compliance gate | Flagged: license status UNKNOWN, left blank, not inferred. |
| F4 | Unit 1 had a roommate change (one original tenant departed, one added). Whether Costa-Hawkins vacancy decontrol was triggered depends on whether **all** original occupants vacated. | Legal fact gap | Flagged: not resolved; analysis shows both branches. |
| F5 | Base rent composition (parking/storage/passthroughs) not supplied for either unit. | Missing input | Left blank; not inferred. |
| F6 | No security-deposit interest compliance record supplied. | Missing input | Flagged (SF requires annual interest payment). |
| F7 | Building "built in 1940" is user-supplied; certificate-of-occupancy date is the legal test. | Verification gap | Flagged: needs Assessor-Recorder / DBI record. |
| F8 | Tenant names, unit designations and exact street address withheld/anonymized per privacy requirement. | Privacy control | Unit 1 → **Unit A**, Unit 2 → **Unit B**; tenants → pseudonymous IDs. |

## Change log

| Timestamp (UTC) | Session | Entry |
| --- | --- | --- |
| 2026-11-06 | session-9d958fa3 | Board created. Claimed T1–T12 (single-session run, non-overlapping scopes). Repo audited: only `README.md` present. GitHub Pages already enabled (legacy build, `main` branch, root path) → site root = `index.html`. |
| 2026-11-06 | session-9d958fa3 | S1 verified by direct fetch of sf.gov Rent Board "Current Rates" page. AGA 1.6% (3/1/2026–2/28/2027), 1.4% (3/1/2025–2/28/2026), 1.7% (3/1/2024–2/28/2025). |
