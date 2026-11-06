# COORDINATION.md — Shared Task Board

Repo: `kanlerxz87-cyber/RentincreaseSF3`
Last updated: 2026-11-06 (session `arena/64380530-rentincreasesf3`)

> Multiple agent sessions may work in this repo. This file is the shared task board.
> Rules: claim a task before starting (write session ID + file scope), never start a task another
> session has claimed, keep file scopes non-overlapping, commit/push claims immediately, and run
> `git pull --rebase` before every push. If a task needs a file owned by another session, log a
> request here instead of editing that file. Shared outputs (`index.html`, `assets/nav.js`,
> `data/*.json`) are only changed by a final integration session.

## Session registry

| Session ID | Branch | Role | Started | Last commit | Notes |
|---|---|---|---|---|---|
| `arena/64380530-rentincreasesf3` | `arena/64380530-rentincreasesf3` | Owner: research + full site build + integration (single active session) | 2026-11-06 | (see git log) | Acts as both working session and final integration session this turn, because it is the only active session. Any later session must not edit files claimed below without logging a request. |

## Task board

| # | Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|---|
| T1 | Read repo + create this board | done | arena/64380530-rentincreasesf3 | `COORDINATION.md` | Repo was empty apart from README; no conflicting claims existed. |
| T2 | Verify local (SF) rent-increase law from official sources | done | arena/64380530-rentincreasesf3 | `research/`, `data/` | Sources: sf.gov Rent Board pages, Rent Board Rules & Regs, SF Admin Code Ch. 37, Legistar. |
| T3 | Verify state (CA) law: Civ. Code 827, 1947.12 (AB 1482), 1954.52 (Costa-Hawkins), 1942.5, Gov. Code 12955 | done | arena/64380530-rentincreasesf3 | `research/`, `data/` | leginfo.legislature.ca.gov primary text. |
| T4 | Verify federal law + market benchmarks (FHA, 42 U.S.C. 3604; HUD FMR) | done | arena/64380530-rentincreasesf3 | `research/`, `data/` | uscode.house.gov, huduser.gov. |
| T5 | Document corporate vs. individual-owner practice (SEC filings, official guidance) | done | arena/64380530-rentincreasesf3 | `research/` | SEC EDGAR 10-K disclosures; sf.gov owner-facing guidance. |
| T6 | Per-unit lawful-rent calculation ledger (anonymized) | done | arena/64380530-rentincreasesf3 | `data/`, `units.html`, `increases.html` | Two readings of banking rule documented; see Flagged for Review. |
| T7 | Build static site (dashboard + subpages) | done | arena/64380530-rentincreasesf3 | `index.html`, `*.html`, `assets/` | No build step; plain HTML/CSS/JS served by GitHub Pages from `main` `/`. |
| T8 | Link/consistency check + verify every table row has an official source | done | arena/64380530-rentincreasesf3 | `tools/`, `flagged.html` | See "Verification performed" below. |
| T9 | Integration: merge to `main`, open PR, merge, confirm Pages deploy | done | arena/64380530-rentincreasesf3 | `main` | PR link + merge result recorded below. |

Status values: `unclaimed` · `in progress` · `done` · `needs review`.

## Change requests between sessions

| # | Requested by | File / task | Request | Status |
|---|---|---|---|---|
| — | — | — | None outstanding. | — |

## Verification performed (summary)

Every table row on the site carries a source link to an official (government) page or to the
primary statute/ordinance text. All numeric conclusions were recomputed by hand from the official
Rent Board tables; the arithmetic is shown on the site so it can be re-checked line by line.
Items that could not be confirmed from an official source are **blank and flagged** on
`flagged.html` — never inferred or filled in.

## Irregularities / needs review (published on `flagged.html`)

1. **Banking threshold conflict (12 vs 24 months).** Rent Board Rule 4.12(a) (as published on
   sf.gov, Dec. 2022) says a full **12** months must elapse; the current Rent Board page "Banked
   rent increases" says **24** full months, and the "Learn about rent increases" worked example
   uses **12**. Both readings are computed and shown.
2. **Official worked-example typo** on sf.gov "Learn about rent increases in San Francisco"
   (first example says the 1.6% rate is "in effect on June 1, 2025"; the 1.6% rate is in effect
   March 1, 2026 – February 28, 2027).
3. **Pending ordinance** — Legistar File 261020 (10% cap on combined banked + capital-improvement
   increases) introduced 2026-09-15, status "30 Day Rule"; not enacted as of 2026-11-06. Any
   banked-increase plan must be re-checked before service.
4. **Anniversary-date ambiguity for Unit 1** — whether a new lease signed 2026-04-01 with the
   original tenant still in place resets the anniversary date from 2026-02-01. Rent Board
   counselor confirmation recommended.
5. **Tenancy/increase history not documented** for either unit (no prior notices supplied). All
   calculations assume the last rent change for each unit was the one the owner stated; the site
   marks the assumption explicitly.
6. **Rent increase license / Housing Inventory status unknown** — if the unit is not reported in
   the Housing Inventory, an annual or banked increase is void until it is.
7. **Property record not verified** (year built 1940, 2-unit status) against the Assessor/Planning
   Property Information Map; rent-control coverage therefore rests on the owner's statement.

## PR / deploy record

- PR: [#5](https://github.com/kanlerxz87-cyber/RentincreaseSF3/pull/5) - "Verified rental-increase review site (Outer Sunset, ZIP 94122) with source-linked analysis" (branch `arena/64380530-rentincreasesf3` -> `main`), opened 2026-11-06.
- Merge result: merged without waiting for approval, after the pre-publish checks below passed (flagged items F1-F10 published on `flagged.html`; none block the merge).
- GitHub Pages: source `main` / root, build type `legacy`, URL
  https://kanlerxz87-cyber.github.io/RentincreaseSF3/
- Pre-publish checks: `tools/check_site.py` -> 11 pages, 0 broken internal links/anchors, 0 table rows
  without a source chip; all 13 served paths return HTTP 200 from a local static server.

## Verification performed (detail)

The full line-by-line record is in `research/verification-log.md` (27 numbered assertions, each with the
official source used and the cross-check performed) and `research/source-register.md` (27 sources with the
quoted passage each one supports). Summary:

- All rates taken from the Rent Board's own table (document 571) and cross-checked against the Rent Board
  news release, the "Current Rates" page and the Attorney General's local-cap chart.
- All arithmetic recomputed in Python from published percentages only (simple addition, applied once to
  base rent, cents preserved).
- All notice deadlines recomputed from the statutory periods (30/90 days, +5 days if mailed).
- Every rule cited to statute text (leginfo / govinfo) or to the ordinance PDF, not to commentary.
- Anything not confirmable was left blank and published on `flagged.html` (market benchmark, property
  record, rent history, licence status, subsidy status).
