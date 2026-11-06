# COORDINATION.md — Shared Task Board

Maintained by all parallel sessions. Newest log entries at the bottom. A task marked `needs review`
is published on the site's Flagged for Review page and does not block anything. Shared outputs
(table data, site index/navigation) may only be changed by the final integration session once all
other tasks are done; cross-session file edits are logged here as requests instead.

## Session registry

| Session | Branch | Outcome |
|---|---|---|
| `arena/07e38125-rentincreasesf3` | `arena/07e38125-rentincreasesf3` | PR #2 **merged** 2026-11-06T13:20:09Z (merge commit `61b5b7a`). Built the root GitHub Pages site (`index.html`, `pages/`, `assets/`, `data/sources.json`). Task 5 left "in progress" with no deploy record. |
| `arena/ae0d4576-rentincreasesf3` | `arena/ae0d4576-rentincreasesf3` | This session. Built the **extended verification edition** under `docs/` (11 pages, cents-exact math, banking analysis, license requirement, sources & verification register, repo review). |

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
| 7 | Final integration: branch conflict resolved, PR → main, Pages deploy confirmed, PR + deploy recorded | done after merge (recorded in follow-up commit) | COORDINATION.md |

Sources (all accessed 2026-11-06): sf.gov (571 Allowable Annual Increases 26-27; 2026–27/2025–26/2023–24 announcements; Learn about rent increases; Banked rent increases; Housing Inventory; §37.3; rental laws; AB 1482 explainer; forms center; Rent Board archives 2019/2023/2024); leginfo.legislature.ca.gov (Civ. Code §827, §1954.53, AB 1482 bill, SB 567 bill); calcivilrights.ca.gov/housing; hud.gov/reporthousingdiscrimination; sfgov.org/services/discrimination-complaints; media.api.sf.gov (SF Analysis of Impediments 2020–2025); Furman Center 2025; Harvard JCHS 2023/2024. Full register with dates: `docs/sources.html`.

Verification performed: every table row on this session's site either links an official source fetched on 2026-11-06 or is flagged on `docs/flagged-for-review.html` (16 items; blocking: FR-01 Unit 2 increase history, FR-02 coverage/exemptions, FR-06 license, FR-14 voucher status). Cents-exact math recomputed programmatically. HTML parsed tag-balanced; internal links checked against the filesystem; anonymization sweep (occupant initials/names must not appear) passed.

Irregularities found in this session's own work / repo: README was a 17-byte stub missing trailing newline (rewritten); repo had no site/CI/Pages config (fixed via `docs/` + Pages); repo had no license (owner decision — logged); duplicate-work conflict with PR #2 (this file).

## Log — `arena/ae0d4576` (UTC)

- 2026-11-06T13:05Z — Session started; only README.md on `main`; created this board; claimed tasks 1–7 (no other session visible at start).
- 2026-11-06T13:10Z — Verified official sources (sf.gov, leginfo, HUD, CRD); computed scenarios; built docs/ site (11 pages); anonymization sweep passed; internal-link/tag checks passed.
- 2026-11-06T13:19Z — Committed site (e35ef54) and pushed claim (e77b27a). `git pull --rebase`: `origin/main` advanced to `61b5b7a` (PR #2, parallel session). **add/add conflict in COORDINATION.md** — resolved by combining both boards; no side discarded; no files of the other session edited.
- 2026-11-06T13:25Z — Irregularities in PR #2's site logged above as requests (not edited). This session's `docs/` becomes the additive "full verification edition"; README links both editions.
- 2026-11-06 — PR to `main` opened (see follow-up commit for PR number/merge SHA and Pages deploy confirmation, recorded after merge).

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
