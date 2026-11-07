# COORDINATION.md — Shared Task Board

Maintained by all parallel sessions. Newest log entries at the bottom. A task marked `needs review`
is published on the site's Flagged for Review page and does not block anything. Shared outputs
(table data, site index/navigation) may only be changed by the final integration session once all
other tasks are done; cross-session file edits are logged here as requests instead.

## Session registry

| Session | Branch | Outcome |
|---|---|---|
| `arena/07e38125-rentincreasesf3` | `arena/07e38125-rentincreasesf3` | PR #2 **merged** 2026-11-06T13:20:09Z (merge commit `61b5b7a`). Built the root GitHub Pages site (`index.html`, `pages/`, `assets/`, `data/sources.json`). Task 5 left "in progress" with no deploy record. |
| `arena/ae0d4576-rentincreasesf3` | `arena/ae0d4576-rentincreasesf3` | PR #3 **merged** 2026-11-06T13:23:22Z (`996aa82`). Built the **extended verification edition** under `docs/` (11 pages, cents-exact math, banking analysis, license requirement, sources & verification register, repo review). Deployed & verified live 2026-11-06 (root + `/docs/` HTTP 200). |
| `arena/edaa9740-rentincreasesf3` | `arena/edaa9740-rentincreasesf3` | PR #9 (this session). Built the **dashboard edition** under `dashboard/` (10 pages). add/add conflict in this file resolved by combining boards; privacy scrub of location applied site-wide as integration step (see log). |

## Reconciliation note — 2026-11-06 (add/add conflict resolution)

Both sessions independently created `COORDINATION.md` on 2026-11-06 (neither existed on `main` when
this session started; `main` was a bare README at that time). While this session was mid-work,
`git pull --rebase` found `origin/main` had advanced to `61b5b7a` (PR #2 merged). Result: `add/add`
conflict in this file. **Resolution: nothing discarded.** This file combines both boards — the
07e38125 board is preserved verbatim below, this session's board and log follow it. No file owned by
the other session was edited; findings are logged as requests below.

GitHub Pages: configured `main` `/`, status `building` at 2026-11-06T13:22Z. This session's `docs/`
edition is purely additive (`docs/*` paths did not exist on `main`) and does not change how Pages
serves the root site.

## Irregularities logged by `arena/ae0d4576` (requests — files NOT edited)

1. `pages/units.html` / `pages/flagged.html`: Unit 1 "next increase may not take effect before 12 months" implies waiting until after Apr 1, 2027. **Incorrect** — the rent-increase anniversary follows the Feb 1, 2025 lease start; it remains February 1. See `docs/unit-1.html` (FR-05 in `docs/flagged-for-review.html`).
2. `pages/flagged.html` item 3: banked increases described as "capped at 3 years' worth." **Incorrect** — SF banking is additive, unlimited, since April 1, 1982 (official: [sf.gov — banked rent increases](https://sf.gov/information/banked-rent-increases)).
3. Entire 07e38125 site is silent on (a) **banked increases** (Unit 1: +1.4% available Feb 1, 2027; Unit 2, if never raised: **11.5% → $3,512.25**, or 13.1% → $3,562.65 on Jun 1, 2027, >10% ⇒ 90-day notice), and (b) the **rent increase license** requirement (Housing Inventory report, due March 1; license must be in effect on the effective date or the increase is unenforceable; 1–9 unit buildings since Mar 1, 2023) — [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory).
4. leginfo URLs with trailing period (e.g., `sectionNum=827.`) may 404; `https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827` is the working form.
5. `pages/executive-summary.html` & `pages/process.html`: "90 days only if combined increases exceed 10% — not the case here" is right for allowable-only increases but incomplete for any banked Unit 2 catch-up (>10% ⇒ 90 days).
6. `index.html`/`pages/*.html` footers reference branch `arena/07e38125-rentincreasesf3` after merge — stale text.
7. PR #2 merged before its own COORDINATION.md task 5 (deploy confirmation + PR record) was completed — this session records deployment verification after its own merge.
8. This session's independent verification independently confirmed all of 07e38125's headline figures (1.4% / 1.6% / 8.8% / 30-90 day / Costa-Hawkins exemption logic / coverage cutoff) against the same official sources — no factual disagreement beyond the items above.

**Request to repo owner / `arena/07e38125`:** apply fixes 1–6 in a follow-up commit, or reply here to authorize this session to apply them. Flagged items do not block either site.

---

## Task board — `arena/ae0d4576` (this session)

| # | Task | Status | File scope |
|---|------|--------|------------|
| 1 | Create COORDINATION.md | done (merged w/ 07e38125 board) | COORDINATION.md |
| 2 | Research: SF Rent Ordinance coverage, allowable increases 1982–2027, banking, license | done | docs/ (analysis embedded); verification listed below |
| 3 | Research: CA law — AB 1482, Civ. Code 827, CCP 1013, Costa-Hawkins, FEHA | done | docs/ |
| 4 | Research: corporate vs individual landlord practice; notice mechanics; one-vs-both-units discrimination analysis | done | docs/market-practice.html, docs/notice-and-reasons.html, docs/tenant-review.html |
| 5 | Anonymize personal data; compute Unit 1 / Unit 2 scenarios (cents-exact) | done | docs/unit-1.html, docs/unit-2.html, docs/executive-summary.html |
| 6 | Build static site (dashboard + subpages, source-linked tables, Flagged for Review) | done | docs/** |
| 7 | Final integration: branch conflict resolved, PR → main, Pages deploy confirmed, PR + deploy recorded | done | COORDINATION.md |

Sources (all accessed 2026-11-06): sf.gov (571 Allowable Annual Increases 26-27; 2026–27/2025–26/2023–24 announcements; Learn about rent increases; Banked rent increases; Housing Inventory; §37.3; rental laws; AB 1482 explainer; forms center; Rent Board archives 2019/2023/2024); leginfo.legislature.ca.gov (Civ. Code §827, §1954.53, AB 1482 bill, SB 567 bill); calcivilrights.ca.gov/housing; hud.gov/reporthousingdiscrimination; sfgov.org/services/discrimination-complaints; media.api.sf.gov (SF Analysis of Impediments 2020–2025); Furman Center 2025; Harvard JCHS 2023/2024. Full register with dates: `docs/sources.html`.

Verification performed: every table row on this session's site either links an official source fetched on 2026-11-06 or is flagged on `docs/flagged-for-review.html` (17 items — FR-17 added 2026-11-06; blocking: FR-01 Unit 2 increase history, FR-02 coverage/exemptions, FR-06 license, FR-14 voucher status). Cents-exact math recomputed programmatically. HTML parsed tag-balanced; internal links checked against the filesystem; anonymization sweep (occupant initials/names must not appear) passed.

Irregularities found in this session's own work / repo: README was a 17-byte stub missing trailing newline (rewritten); repo had no site/CI/Pages config (fixed via `docs/` + Pages); repo had no license (owner decision — logged); duplicate-work conflict with PR #2 (this file).

## Task board — `arena/487d8c3e` (this session)

Claimed 2026-11-07; branch == main at 25e1e5f (four editions merged). Scope: (a) foreground the Rent Board / rent-increase licence process in the executive summary with a step-by-step answer for an individual (non-corporate) owner and official links; (b) re-verify every figure in all four editions against official sources (sf.gov, leginfo, govinfo, calcivilrights.ca.gov, sfgov.legistar.com); (c) fix irregularities flagged in this file; (d) keep anonymisation (no tenant initials/names, no unit ZIP code, no neighborhood name; dates and amounts unchanged); (e) ensure every table row carries an official source link or is blank + flagged; (f) final integration: PR from this branch to main, merge, confirm GitHub Pages deploy, record PR link + merge result here.

| # | Task | Status | File scope | Notes |
|---|------|--------|------------|-------|
| T1 | Claim tasks + sync branch | done | COORDINATION.md | claim pushed 2026-11-07 (commit 1d3eaf3) |
| T2 | Verify rent-board licence/notice process (individual owner) vs official sf.gov sources | done | EXECUTIVE_SUMMARY.md, pages/process.html, pages/executive-summary.html | license foregrounded at front of executive summary; Step 1 in process page |
| T3 | Re-verify rates 1.4%/1.6%, banking, AB 1482, Civ. 827, Costa-Hawkins, coverage cutoff | done | pages/*, data/sources.json | every figure re-fetched from sf.gov / leginfo on 2026-11-07; trailing-period leginfo URLs fixed |
| T4 | PII scrub re-scan (initials, unit ZIP, neighborhood) + anonymisation sweep | done | all public files | scan clean across pages/, dashboard/, docs/, review/, README, COORDINATION.md, EXECUTIVE_SUMMARY.md |
| T5 | Fix irregularities (items 1–2, 5–6 logged by ae0d4576) within this session's scope | done | pages/units.html, pages/flagged.html, pages/laws.html, data/sources.json | Unit 1 anniversary fixed to Feb 1 (not Apr 1); banking "3-year cap" error removed; leginfo URLs fixed; dashboard/docs/review editions NOT edited (cross-session rule) |
| T6 | Final integration: build check, no broken links, PR → main, merge, Pages deploy confirmed, record here | done | all | PR #15 merged as b64b6d7; Pages build for b64b6d7 `built` 2026-11-07T20:51:29Z, no errors |

## Log — `arena/487d8c3e` (UTC)

- 2026-11-07 — Session started; branch identical to main at 25e1e5f (PR #11 merged). Claimed T1–T6 per user request; claim pushed (commit 1d3eaf3).
- 2026-11-07 — Verified official sources: sf.gov "Learn about rent increases" (1.6% for 3/1/2026–2/28/2027; 30/90-day notice; license before increase takes effect; 24-month banking condition; additional-occupant ban; worked examples), sf.gov "Rent Board Housing Inventory" (report required; license auto-generated; 1–9 unit buildings since 3/1/2023; license in effect on effective date; portal.sfrb.org), sf.gov "Banked rent increases" (banked since 4/1/1982; added not compounded; no limit; no expiry during tenancy), sf.gov Form 571 PDF, leginfo Civ. Code §827 (30/90 days, combined 12-month measure), leginfo Civ. Code §1947.12 (AB 1482; (d)(3) local-control exemption), sf.gov news Ordinance 265-20 (license requirement), sfgov.legistar.com File 261020 (pending, not law). All fetches 2026-11-07.
- 2026-11-07 — Applied fixes within session scope: pages/executive-summary.html rewritten with license question at the forefront + 6-step process + per-unit table + tenant-lawyer scrutiny list; pages/process.html license made Step 1 + uniform-practice step; pages/units.html Unit 1 anniversary corrected to Feb 1, 2025 lease start (4/1/2026 is continuing tenancy, not a vacancy); pages/flagged.html banking-cap error removed (unlimited since 4/1/1982) + Unit 1 timing corrected; pages/laws.html trailing-period leginfo URLs fixed to working form; data/sources.json trailing periods fixed, branch field updated, Housing Inventory + license sources added; EXECUTIVE_SUMMARY.md rewritten to mirror the page with license at the forefront. COORDINATION.md PII literal strings rephrased so the PII scan passes.
- 2026-11-07 — Verification: verify_site.py (dashboard) ALL CHECKS PASSED; one-off check over pages/ + root + all editions (internal links, every table row carries a source link, PII scan, cents-exact math: 3995×1.016=4058.92, 3995×1.03=4114.85, 3150×1.131=3562.65, banked sums 11.5%/13.1%) ALL CHECKS PASSED.
- 2026-11-07 — Committing fixes and pushing; then PR arena/487d8c3e-rentincreasesf3 → main, merge, confirm GitHub Pages deploy, record PR link + merge result below.
- 2026-11-07 — Rebased onto origin/main (1cfea10, PR #14 merge) after PR #15 showed CONFLICTING; resolved EXECUTIVE_SUMMARY.md conflict by keeping the license-at-forefront detail and folding in PR #14's cautions (public Housing Inventory filings under penalty of perjury; free counseling is not a guaranteed lawyer for every dispute; no blanket equal-increase requirement; annual-first as risk management). No other session's work discarded.
- 2026-11-07 — PR #15 `arena/487d8c3e-rentincreasesf3` → `main` **MERGED** as merge commit `b64b6d79dc89bbf31f9991f833947c3e186246b2` (gh pr merge 15 --merge, no approval wait). PR URL: https://github.com/kanlerxz87-cyber/RentincreaseSF3/pull/15
- 2026-11-07 — GitHub Pages build for b64b6d7 created 2026-11-07T20:51:29Z, status **built** with no errors (verified via gh api). Live site verified serving the merged content: `/pages/executive-summary.html` (license question at the forefront, 6-step process with official links, per-unit table) and `/pages/units.html` (corrected Feb 1, 2025 Unit 1 anniversary; flagged conditional Unit 2 figures) both HTTP 200 with correct content. All four editions remain live under `/`, `/docs/`, `/dashboard/`, `/review/`.
- 2026-11-07 — Final verification re-run after merge: verify_site.py ALL CHECKS PASSED; pages/ + root + all editions check (internal links, per-row source links, PII scan, cents-exact math) ALL CHECKS PASSED. Flagged irregularities remain published on the Flagged for Review pages and do not block the merge.

## Log — `arena/ae0d4576` (UTC)

- 2026-11-06T13:05Z — Session started; only README.md on `main`; created this board; claimed tasks 1–7 (no other session visible at start).
- 2026-11-06T13:10Z — Verified official sources (sf.gov, leginfo, HUD, CRD); computed scenarios; built docs/ site (11 pages); anonymization sweep passed; internal-link/tag checks passed.
- 2026-11-06T13:19Z — Committed site (e35ef54) and pushed claim (e77b27a). `git pull --rebase`: `origin/main` advanced to `61b5b7a` (PR #2, parallel session). **add/add conflict in COORDINATION.md** — resolved by combining both boards; no side discarded; no files of the other session edited.
- 2026-11-06T13:25Z — Irregularities in PR #2's site logged above as requests (not edited). This session's `docs/` becomes the additive "full verification edition"; README links both editions.
- 2026-11-06T13:19Z — PR #3 opened (`arena/ae0d4576-rentincreasesf3` → `main`): full verification edition + README + this reconciliation.
- 2026-11-06T13:23:22Z — PR #3 **merged** as merge commit `996aa82e35b8889599f6ba632d04a35914ab103b`. Files added: `docs/**` (11 pages + assets), `README.md` rewrite. No other session's files touched.
- 2026-11-06T13:23:24Z — GitHub Pages build `1346386076` created for `996aa82`; status `built` at 2026-11-06T13:27:03Z (duration 219,959 ms). Prior build `1346379363` for `61b5b7a` was `built` at 13:22:43Z.
- 2026-11-06T13:30Z — Deploy verified live: root site `https://kanlerxz87-cyber.github.io/RentincreaseSF3/` (HTTP 200, PR #2 content) and full verification edition `https://kanlerxz87-cyber.github.io/RentincreaseSF3/docs/index.html` (HTTP 200 — dashboard, KPIs, cross-link banner). No broken build, no deploy failure, nothing to retry.
- 2026-11-06 — PR merge record, Pages deploy confirmation, and both-edition status recorded via this follow-up PR.
- 2026-11-06T13:31Z — THIRD session `arena/64380530` merged PR #5 (`92732f5`, 13:29:50Z): `review/` edition + `tools/` + `research/` + `EXECUTIVE_SUMMARY.md` + root `index.html`/README links + `.nojekyll`; README/COORDINATION updated there too.
- 2026-11-06T13:33Z — Pages builds for `5d3065f` (13:28:40Z→errored 13:29:53Z) and `92732f5` (13:29:52Z→errored 13:30:25Z) both report generic "Page build failed."; prior builds `61b5b7a` and `996aa82` succeeded. `92732f5` carries `.nojekyll` yet still failed ⇒ cause is platform-side or reason not exposed via API (only "Page build failed."; token cannot call `POST /pages/builds` — HTTP 403). Live site continues to serve `996aa82` (HTTP 200 verified). Each push triggers a retry; this session’s next commit doubles as a retry; failures and successes are recorded here. Third-party context (not this repo) shows the same generic error reported across repos since Oct 2026 — treated as a GitHub-side incident until disproven by a green build.
- 2026-11-06T13:33:44Z — PR #6 **merged** as merge commit `86c870d4a9bdbefb8f7dcd0e08091175d5e2418e` (FR-17 + build-incident log). GitHub Pages build for `86c870d` **`built`** 2026-11-06T13:37:13Z (duration 208,501 ms). The two failures (`5d3065f`, `92732f5`) are recorded as a transient platform-side incident (both ~duration 0, errors generic, `.nojekyll` present in one of them; same generic error reported across unrelated repos since Oct 2026). Live site verified serving `86c870d`: `/` (200), `/docs/flagged-for-review.html` (200, FR-17 present), `/review/` (200). Nothing else to fix on this repo's side; if a future build fails again, retry by push before assuming content breakage.
- 2026-11-06T13:35Z — Cross-verified third session’s “F3” finding against the official record: **SF Legistar File #261020** — Ordinance; status **Pending Committee Action** (Land Use and Transportation Committee); introduced 9/15/2026 (sponsors Sauter, Chan, Mahmood); “banked rent increases and capital improvement rent increases … may not increase a tenant’s rent by more than a total of 10% per year, for the next three years”; Youth Commission response 10/7/2026; no final action; **not law**. Added to this session’s site as **FR-17** (flagged pending item, not applied), to executive summary, legal framework (L-13), unit-2 roadmap, sources register, and README. Not reflected in any computed figure — those remain lawful today under current law.

---

## Prior board (verbatim) — `arena/07e38125`

# COORDINATION.md — Shared Task Board

Session: `arena/07e38125-rentincreasesf3` (branch `arena/07e38125-rentincreasesf3`)

## Tasks

| # | Task | Status | Owner session | Files |
|---|------|--------|---------------|-------|
| 1 | Research & verify SF/CA rent-increase law from official sources | done | arena/07e38125-rentincreasesf3 | `data/sources.json` |
| 2 | Executive summary (anonymized) | done | arena/07e38125-rentincreasesf3 | `pages/executive-summary.html` |
| 3 | Build GitHub Pages site (landing + subpages, tables w/ source links) | done | arena/07e38125-rentincreasesf3 | `index.html`, `pages/*.html`, `assets/style.css` |
| 4 | Flagged-for-review page (unverified/irregular items) | done | arena/07e38125-rentincreasesf3 | `pages/flagged.html` |
| 5 | Final integration: verify data line by line, build check, publish to Pages, PR + merge | in progress | arena/07e38125-rentincreasesf3 | all |

## Log
- 2026-11-06: Session started. Repo contained only README.md. COORDINATION.md created. Single-session run: all tasks claimed by this session to avoid conflicts.
- 2026-11-06: Research verified from official sources: sf.gov (1.4% for 3/1/25-2/28/26; 1.6% for 3/1/26-2/28/27; notice 30/90 days; AB 1482 summary; tenant petitions; free legal help), leginfo.legislature.ca.gov (Civ. Code 827, 1947.12, 1954.51), hud.gov, ecfr.gov. Site built as static HTML; every table row carries an official source link; unverifiable items left blank and listed on Flagged for Review page.
- 2026-11-06: PR link and merge result to be recorded here after Pages deploy.


---

## Task board — `arena/64380530` (session `arena/64380530-rentincreasesf3`)

Claimed 2026-11-06 on a repo that (at claim time) held only `README.md`; `main` later advanced to the
two existing editions while this session was building. **Nothing was discarded:** this edition was moved
from the repo root into `review/` before merging, so no file owned by `arena/07e38125` (root site,
`pages/`, `assets/`) or `arena/ae0d4576` (`docs/`) was overwritten.

| # | Task | Status | File scope | Notes |
|---|---|---|---|---|
| 1 | Board + claim | done | `COORDINATION.md` | Claim committed and pushed before work started |
| 2 | Verify SF Rent Ordinance (rates, banking, licence, notice, petitions, eviction, §37.10C) | done | `review/`, `tools/sitedata.py` | 15 sf.gov Rent Board pages/documents + ordinance PDF + Legistar |
| 3 | Verify CA law (Civ. 827, 1942.5, 1947.12, 1954.52; Gov. 12955; AG rent-cap table) | done | `review/` | leginfo primary text + oag.ca.gov |
| 4 | Verify federal law + corporate practice (42 U.S.C. 3604; DOJ RealPage; SEC filing index) | done | `review/` | govinfo, justice.gov, sec.gov |
| 5 | Per-unit ledger, cents-exact, both banking readings | done | `review/calculations.html`, `review/data/ledger.csv` | See Flags F1, F3 |
| 6 | Build dashboard + 10 subpages, source-linked tables, Flagged for Review | done | `review/**` | `tools/build_site.py` |
| 7 | Automated link/anchor/source-chip checks; local HTTP check (13 paths × 200) | done | `tools/check_site.py` | 0 broken links, 0 rows without a source |
| 8 | Integration: merge `main` into this branch, resolve add/add conflicts, PR → `main`, merge, verify Pages | done | `main` | PR #5, see below |

### Verification performed (this session)

Full record: `research/verification-log.md` (27 numbered assertions, each with the official source used and
the cross-check) and `research/source-register.md` (27 sources with quoted passages). Highlights:

- All rates read from the Rent Board's own table (document 571) and cross-checked against the Rent Board
  news release, the "Current Rates" page and the California Attorney General's local-cap chart.
- All arithmetic recomputed in Python from published percentages only: simple addition, applied once to
  base rent, cents preserved, nothing compounded or rounded up.
- All notice deadlines recomputed from the statutory periods (30/90 days, +5 if mailed).
- Every rule cited to statute text or the ordinance PDF; no commentary relied on.
- Not confirmable → left blank and published: ZIP-level market benchmark (F9).

### Irregularities logged (published on `review/flagged.html`)

1. **F1 (High) — banking threshold conflict.** Rent Board Rule 4.12(a) as published on sf.gov still says
   "a full 12 months"; the current "Banked rent increases" page and the "irregular periods" page require
   **24 full months** without any increase. Both readings are computed; the fallback options
   (Unit A 1.6%, Unit B 10%) are lawful either way.
2. **F2 (Medium) — official worked-example typo** on sf.gov (1.6% attributed to 1 June 2025).
3. **F3 (High) — pending ordinance.** Legistar File 261020 would cap combined banked + capital-improvement
   increases at 10%/yr for three years; status "30 Day Rule", introduced 2026-09-15, **not law** on
   2026-11-06. Not applied; re-check before serving any banked notice.
4. **F4 — Unit A anniversary ambiguity** after the 2026-04-01 renewal (1 Feb vs 1 Apr). Same 3.0% either
   way; the earliest effective date differs.
5. **F5–F8 — documentation gaps:** rent history, property record (1940 / two units), rent increase
   licence, subsidy status.
6. **F9 — market benchmark** not retrievable from an official source; left blank.

### Response to `arena/ae0d4576`'s requests 1–6

No files of that session were edited (per the board's rule for cross-session changes). The points are
consistent with this edition's verification and are handled here instead:

- Request 1 (Unit 1 anniversary ≠ April): confirmed — the anniversary follows the 1 Feb 2025 lease start;
  this edition uses 1 Feb 2027 and flags the residual ambiguity as F4.
- Request 2 (banking not capped at three years): confirmed — no cap on banked amounts; treated as
  "no limit" here, with the **pending** 10% cap logged as F3 so it is not mistaken for law.
- Request 3 (banked increases + licence): both are core to this edition (`review/calculations.html`,
  `review/notices.html`, `review/requirements.html`), and the 11.5% / 13.1% figures were independently
  recomputed to the cent ($362.25 / $412.65 on $3,150).
- Request 4 (leginfo URLs with trailing periods 404): confirmed; every leginfo URL on this site omits the
  trailing period and was fetched successfully on 2026-11-06.
- Requests 5–6 (90-day notice for a banked catch-up; stale branch in footers): the 90-day rule is applied
  throughout, and this edition's footers carry no branch reference.

### PR / deploy record — this session

- PR: [#5](https://github.com/kanlerxz87-cyber/RentincreaseSF3/pull/5) — "Verified rental-increase review
  site (San Francisco (location withheld)) with source-linked analysis", branch
  `arena/64380530-rentincreasesf3` → `main`.
- Merge conflict: `COORDINATION.md` (add/add) and `README.md` (content) only, because `main` had advanced
  with the two earlier editions. Resolved by preserving both prior editions verbatim and appending this
  session's board and README row; this edition was relocated to `review/` first, so no shared file was
  overwritten.
- Merge result: **merged into `main` without waiting for approval** after the pre-publish checks passed
  (0 broken internal links/anchors, every table row source-chipped, 13 paths × HTTP 200 locally).
- GitHub Pages: source `main` / root, build type `legacy`; live edition at
  <https://kanlerxz87-cyber.github.io/RentincreaseSF3/review/>. Deploy verification is recorded in the
  follow-up commit/PR.

---

## Task board — `arena/edaa9740` (session `arena/edaa9740-rentincreasesf3`)

Claimed 2026-11-06 after reading this board (created it first when the file did not exist — same
independent-creation situation as the earlier sessions; **resolved without discarding anything**: this
section is appended to the combined board above, and the 07e38125 / ae0d4576 / 64380530 records are
preserved verbatim). This session's edition lives entirely under `dashboard/` (moved there before
merging, mirroring the `review/` pattern, so no file owned by any other session was overwritten).

| # | Task | Status | File scope | Notes |
|---|------|--------|------------|-------|
| T1 | Create COORDINATION.md, claim tasks | done | COORDINATION.md | Claim pushed before work started (commit `64a06d8`) |
| T2 | Research: SF Rent Board rates, banking, petitions, notices, license | done | dashboard/** | 15+ sf.gov pages/PDFs fetched 2026-11-06 |
| T3 | Research: CA law — AB 1482, Civ. Code § 827, Costa-Hawkins § 1954.53 | done | dashboard/** | leginfo primary text fetched |
| T4 | Research: federal law + fair housing + free SF tenant legal services | done | dashboard/** | govinfo 42 U.S.C. § 3604 fetched verbatim |
| T5 | Research: corporate vs individual practices (flag if no official source) | done | dashboard/market-practices.html | Official findings only; gap flagged F-5 |
| T6 | Build GitHub Pages site (landing + 9 subpages, source-linked tables) | done | dashboard/** | 10 pages, shared nav verified |
| T7 | Line-by-line verification; blanks + flags for unverified | done | dashboard/flagged.html | 8 flags F-1…F-8 published |
| T8 | Integration: re-verify combined data, build + broken-link check | done | verify_site.py | ALL CHECKS PASSED (see below) |
| T9 | PR → main → merge → Pages deploy → record | done | COORDINATION.md | See “PR / deploy record” below |

### Sources & verification — `arena/edaa9740` (all retrieved 2026-11-06)

Full register with URLs: `dashboard/sources.html` (S1–S22). Official: sf.gov / SF Rent Board
(Current Rates; Learn about rent increases; Banked rent increases; Form 571 rate table; rental laws;
AB 1482 explainer; Housing Inventory; Topics 301/322/323; tenant resources; discrimination page;
forms center; annual statistical report FY22-23; evictions page); leginfo (Civ. Code § 827, § 1954.53,
AB 1482); U.S. GPO (42 U.S.C. § 3604); CRS R49015. Two non-government sources labeled and excluded
from verified tables (academic working paper; EDC FAQ).

Verification performed: rates cross-checked across sf.gov Current Rates ↔ Form 571 (1.6/1.4/1.7 agree);
notice periods cross-checked sf.gov ↔ statute (30/90 days agree); every dashboard table row carries an
official source link (script-enforced); math asserted in code (3995×1.016=4058.92; 3995×1.030=4114.85;
3150×1.131=3562.65; banked sums 11.5%/13.1%); internal links/anchors checked; PII scan (initials, ZIP,
district, street patterns) enforced across `dashboard/`, `pages/`, `docs/`, `review/`, README and this
file by `verify_site.py`.

### Irregularities — `arena/edaa9740` (published as F-1…F-8 on `dashboard/flagged.html`)

F-1 Unit B rent history not provided → 13.1%/$3,562.65 conditional · F-2 2027-28 rate unpublished →
blank row · F-3 address-level coverage check pending (location internal) · F-4 banking 24-month vs
12-month wording between official pages (reconciled; identical results here — corroborates 64380530's
F1) · F-5 no official corporate-vs-individual dataset (CRS: research “largely nonexistent”) ·
F-6 occupancy-continuity/no-vacancy assumption · F-7 property facts as provided · F-8 Unit A rent
unchanged since 4/1/2026 assumed.

### Log — `arena/edaa9740` (UTC)

- 2026-11-06 — Session started; repo held only a 17-byte README; created this board; claimed T1–T9; claim pushed (`64a06d8`).
- 2026-11-06 — Research verified from official sources; dashboard edition built (10 pages + CSS); `verify_site.py` added; all checks green (`7d086eb`, `10b0c15`).
- 2026-11-06 — PR #9 opened. Pre-merge check: `main` had advanced (PRs #4–#7, three editions on `main`). **Conflicts: add/add `COORDINATION.md`, content `README.md`.** Resolution: this edition relocated to `dashboard/` first (zero overlap); COORDINATION = main's full board + this section appended; README = main's content + this edition's row added. Nothing from any other session discarded; no other session's edition files edited in the merge commit.
- 2026-11-06 — **Integration privacy action (user instruction: location is internal-only, privacy top priority):** site-wide scrub of the neighborhood/ZIP from published pages and shared files (`index.html`, `README.md`, `pages/`, `docs/`, `review/`, `research/`) — text-only replacement (location → “withheld”), **no dates, amounts or findings changed**; logged in the commit message.
- 2026-11-06 — Combined re-verification: `verify_site.py` (this session) + `tools/check_site.py` (64380530) run over the merged tree.

### PR / deploy record — `arena/edaa9740`

- PR: [#9](https://github.com/kanlerxz87-cyber/RentincreaseSF3/pull/9) — `arena/edaa9740-rentincreasesf3` → `main`.
- Merge conflict: `COORDINATION.md` (add/add) + `README.md` (content) because `main` advanced with three
  editions while this session worked. Resolved by relocating this edition to `dashboard/` first, then
  combining both boards/READMEs — nothing discarded (see log above).
- Rebase incident: a habitual `git pull --rebase` after the merge attempt to linearize the merge onto the
  session's own (older) upstream; it stopped on the first replayed commit, was **aborted intact** (`git
  rebase --abort`), verified fast-forward-safe (`origin/main` and session remote both ancestors of HEAD),
  and pushed without rebase. No commits lost, no history rewritten.
- Merge: **MERGED** as merge commit `e421746` at 2026-11-06T14:05:45Z (gh `pr merge 9 --merge`, no approval wait).
- GitHub Pages: source `main` / root, legacy build + `.nojekyll`. Build for `e421746` → **`built`**
  (duration 247,599 ms, no errors). Live URLs verified by retrieval 2026-11-06:
  root `https://kanlerxz87-cyber.github.io/RentincreaseSF3/` (privacy-scrubbed landing, all four editions linked),
  `…/dashboard/` (this session's edition, renders with all key figures),
  `…/docs/` and `…/review/` (other sessions' editions intact and live).
- Post-merge additions carried by follow-up record PR
  [#10](https://github.com/kanlerxz87-cyber/RentincreaseSF3/pull/10) — **MERGED** 2026-11-06T14:14:30Z as
  `2ea0b03`; Pages build for `2ea0b03` **`built`** (200,051 ms, no errors): dashboard flag **F-9**
  (Legistar File #261020, verified directly on sfgov.legistar.com: Pending Committee Action, not law),
  root landing “one of four” wording + stale-branch footer fix, docs stat-strip de-duplication.
  Live re-verified after `2ea0b03`: root, `/dashboard/` (F-9 visible), `/docs/`, `/review/`.

## Integration audit — arena/649a1fa8-rentincreasesf3 (2026-11-07)

| Task | Status | Owner | Scope |
|---|---|---|---|
| Consolidate front-door summary, source recheck and disclose legacy disagreements | done | arena/649a1fa8 | index.html, EXECUTIVE_SUMMARY.md, audit/**, tools/audit_site.py, README.md |
| Final integration / tests / PR / Pages deployment | done | arena/649a1fa8 | COORDINATION.md |

All preceding claims are completed; legacy editions will be preserved as archived research, not silently certified. This is the final integration session. Arena requires this assigned branch; no additional session branch is created. Official-page retrieval failures will be flagged, not represented as successful verification. Existing property inputs are owner-reported, not independently verified. Claim committed and pushed before implementation.

- Integration scope clarification: all prior sessions are finished. Final integration additionally applies a non-destructive archive-warning banner to `pages/*.html`, `docs/*.html`, `review/*.html`, `dashboard/*.html`; underlying research is preserved. This is necessary because conflicting editions were previously presented as equally verified advice. Canonical findings are under root + `audit/`; source rows checked against official pages retrieved 2026-11-07.

### Audit results — 2026-11-07 / arena/649a1fa8

- Source recheck: 13 official sources retrieved/read (full URLs, dates and per-source verification in `audit/sources.json` and `audit/sources.html`). SF Housing Inventory and FAQ redirect, annual guidance, banking, Form 571 PDF, coverage, AB 1482, petitions, Civil Code §§827/1942.5, CRD, HUD, City tenant resources and Legistar 261020. No private property record verified.
- Failed/unsuitable retrievals: attempted `reports--current-allowable-rent-increases` failed; `tenant-right-counsel` returned an official Not Found page. Excluded, replaced by working official sources; disclosed F11.
- Canonical findings: individual-owner license requirement; effective-date vs service-date distinction; no ordinary annual/banked approval petition; 1.6% annual-only conditional calculations; fair-housing/retaliation review; owner behavior not established. Prior 10%/13.1% recommendations withdrawn, not certified. Property inputs preserved separately, verified property fields blank. Pending proposal is Pending Committee Action, no enactment shown. No future-rate inference.
- Published irregularities F01–F11 on `audit/flagged.html`: property facts, history, licenses, banking wording/year-label errors, pending proposal, future rate, behavior/market gaps, subsidy/lease status, legacy conflicting recommendations, privacy/public filings, failed retrievals. All are needs review and do not block publication; they do prevent a notice-ready legal determination.
- Tests: `python tools/audit_site.py` PASS (43 HTML files internal links/anchors; 6 canonical pages official domain per data row; 5 Decimal scenarios; archive labels and privacy patterns); `python verify_site.py` PASS; `python tools/check_site.py` no broken links/anchors. These do not verify every external legacy link or certify legality. Canonical source contents were read manually via retrieval, not inferred from live links.
- Integration adds `.github/workflows/site-checks.yml` to run these offline checks on PRs/main. Scope claimed by this final integration session; no active ownership overlap.
- Task statuses: canonical research/site/testing done; F01–F11 needs review (published); PR/merge/deploy in progress.
- PR opened: https://github.com/kanlerxz87-cyber/RentincreaseSF3/pull/12. Initial GitHub check run 42412688335 passed all three scripts. Updated checkout/setup-python actions to Node 24 versions after GitHub emitted a Node 20 deprecation warning; rerun required before merge.

### Final publication record — arena/649a1fa8

- PR [#12](https://github.com/kanlerxz87-cyber/RentincreaseSF3/pull/12) merged **2026-11-07T20:47:36Z**, merge commit `71895b76d68a97ad7e646f966a92a34a09da6f9d`, using `gh pr merge 12 --merge`; no approval wait.
- Final premerge CI run **42412724226 succeeded**; postmerge Site checks **42412747278 succeeded**.
- GitHub Pages build **1349912433** for that exact merge commit is **built**, error message null. Pages workflow [42412746663](https://github.com/kanlerxz87-cyber/RentincreaseSF3/actions/runs/42412746663) build/deploy/report all succeeded.
- Live retrieval confirmed the new license-first summary at https://kanlerxz87-cyber.github.io/RentincreaseSF3/ and all F01–F11 rows at https://kanlerxz87-cyber.github.io/RentincreaseSF3/audit/flagged.html on 2026-11-07. Returned titles/content match the new canonical edition, not the prior cached landing.
- All integration tasks done. F01–F11 remain **needs review**, publicly documented and nonblocking for publication, not resolved property/legal facts. No tenant notices or government submissions performed.
- Deployment workflow emitted a Node runtime warning for GitHub-managed legacy Pages upload-artifact; deployment nevertheless succeeded. Our own verification workflow uses Node 24 actions. No broken-site or failed check remains.

---

## Integration review — `arena/081a63a0-rentincreasesf3`

| Task | Status | Owner | File scope |
|---|---|---|---|
| Review existing editions, official sources, privacy and reconcile material inconsistencies; test and publish | done | `arena/081a63a0-rentincreasesf3` | `COORDINATION.md`, `index.html`, `pages/**`, `docs/**`, `review/**`, `dashboard/**`, `assets/**`, `README.md`, `EXECUTIVE_SUMMARY.md`, verification tooling as necessary |

2026-11-07 — The previous root integration claim has been inactive for over 60 minutes; taking over integration, preserving earlier work. Fixed Arena branch name takes precedence over requested session branch pattern. Existing independent editions and prior records will be retained unless corrections are needed.

### Integration verification — 2026-11-07

- Status: **done, pending PR and deploy record**. User-supplied tenancy dates and rents are explicitly owner-reported, not officially verified. Current lawful rent, coverage, license and history remain blank and flagged. No tenant attorney has reviewed the proposal.
- Verified the Rent Board's [Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) and [portal](https://portal.sfrb.org/) directly: the annual/banked license is required on the effective date, reporting is annual, free, and includes public information. Obtaining it before service is precautionary, not stated as the legal deadline. Ordinary banking does not require an approval petition: [banking](https://www.sf.gov/information/banked-rent-increases).
- Checked [Rent Board current rate](https://www.sf.gov/news--annual-rent-increase-3126-22827-announced), [official rate history](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf), [rent increase guidance](https://www.sf.gov/learn-about-rent-increases-san-francisco), [coverage](https://www.sf.gov/learn-about-san-francisco-rental-laws), [section 37.3](https://www.sf.gov/information/sec-373-rent-limitations), [capital improvement petitions](https://www.sf.gov/information--capital-improvement-petitions), [Civil Code 827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827), [AB 1482](https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482), [California fair housing](https://calcivilrights.ca.gov/housing/), [HUD guidance](https://www.hud.gov/sites/dfiles/PIH/documents/HCV_Guidebook-Chapter_Fair-Housing_April-2025.pdf), [tenant resources](https://www.sf.gov/tenant-and-landlord-resources), and [fee](https://www.sf.gov/rent-board-fee-link). 1.6% calculations separately checked using Decimal.
- Flagged [proposed File 261020](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770) as pending on direct review. [Rule 4.12](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring) and the Rent Board banking page use different timing language; exact application flagged for counselor review. Earlier categorical findings including a three-year banking cap, 2026 lease change resetting the anniversary, indiscriminate same-unit increases, and unconditional banked dollar totals were not supported.
- Reconciled formerly conflicting editions into the root dashboard. Legacy HTML paths redirect to relevant reviewed pages; earlier HTML remains in Git history, and prior machine-readable/research files are historical rather than a current source of advice. Do not rerun the superseded generator. Added `tools/verify_integrated.py`: 38 HTML files, local links, redirects and row-level official source links pass; illustrative arithmetic and public-site location scan pass; `git diff --check` passes. Local root and executive pages returned HTTP 200. Individual official pages above were directly fetched; automated external link availability is not tested due to network restrictions, and checks cannot prove legal accuracy.
- Initial push note: the session remote branch did not yet exist, so the first `git pull --rebase` against it failed; rebased against `origin/main` before the initial push. No conflict occurred.

- 2026-11-07 conflict reconciliation: while this session worked, PRs #12 and #13 merged another integration session's canonical root and `audit/` site. The two integration scopes overlapped despite separate claims being invisible on the original checkout. `git merge origin/main` conflicted in COORDINATION.md, README, summary, and legacy site pages. Resolution preserves the other session's complete current site, workflow, archived editions, README and executive summary; both coordination sections are retained. This session's superseded redirect/dashboard implementation remains in this branch's prior commit history, not deployed. Rather than overwrite parallel work, this session limits its final change to the fee/portal clarification and validation below.
