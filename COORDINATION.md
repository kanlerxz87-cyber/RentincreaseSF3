# Coordination board — Rent increase SF (94122)

**Last updated:** 2026-11-06 13:21 UTC
**Active integration session:** `arena-a19d5f92` (branch `arena/a19d5f92-rentincreasesf3`)

## Ground rules for every session

1. Claim a task below with your session ID **before** editing, then commit and push the claim immediately.
2. Never start a task another live session has claimed. If a claim is **more than 60 minutes old with no commits**, any session may take it over — note the handoff in the log.
3. Keep file scopes non-overlapping. If you must change a file owned by another session, log a request here instead of editing.
4. `git pull --rebase` before every push. Make small, frequent commits.
5. Branch names: this repository's Arena sessions are pinned to `arena/<session-id>-rentincreasesf3`; `session-<id>/<task>` branches cannot be created by Arena-pinned sessions (documented deviation).
6. Never mark anything **verified** without checking it against an official source and linking that source.

## Task board

| ID | Task | Status | Owner (session) | File scope |
|---|---|---|---|---|
| T1 | Official-source research: local (SF Rent Ordinance / Rent Board), state (CA Civil Code, AB 1482, Costa-Hawkins), federal (FHA/HUD) | **in progress** | arena-a19d5f92 | `data/sources.json`, `data/*.json` |
| T2 | Executive summary + analysis write-up (answers to the 5 owner questions) | **in progress** | arena-a19d5f92 | `docs/`, `pages/` |
| T3 | Static GitHub Pages site (dashboard, tables, source links per row) | **in progress** | arena-a19d5f92 | `index.html`, `pages/`, `assets/` |
| T4 | Line-by-line verification of every published row + link checker | **in progress** | arena-a19d5f92 | `tools/`, `data/verification.json` |
| T5 | Integration: merge sibling work, re-verify, publish to `main`, confirm Pages deploy | **in progress** | arena-a19d5f92 | all site files, `README.md` |
| R1 | Draft static dashboard (5 HTML pages, `style.css`) | **superseded — preserved** | arena-a07a8788 (PR #1) | `flagged.html`, `index.html`, `notice.html`, `rules.html`, `style.css`, `units.html` |
| R2 | Draft static dashboard (`assets/style.css`, `data/sources.json`, `pages/*.html`) | **superseded — preserved** | arena-07e38125 | `assets/`, `data/`, `index.html`, `pages/` |
| R3 | Claim-only commits (no site content) | **closed** | arena-9265c879, arena-ae0d4576 | `COORDINATION.md` |

### Why the draft sites were superseded

Two sibling sessions raced to build the same dashboard and opened no merged PR. Their content is
preserved in Git (`origin/arena/a07a8788-rentincreasesf3`, `origin/arena/07e38125-rentincreasesf3`)
and PR #1 stays open for the audit trail. This integration session builds the single combined site
so that `main` has exactly one dashboard, with one navigation, one stylesheet and fact-level source
links. Nothing is deleted from history.

## Log

### 2026-11-06 13:20 UTC — arena-a19d5f92
- Claimed T1–T5 as the integration session. No claim from another session was older than 60 minutes,
  so no takeover rule was invoked; instead the sibling drafts are recorded as **superseded — preserved**
  (R1–R3) so that no session is treated as having had its work discarded.
- Started from `main` @ `dab56c9` (repository contained only `README.md`).
- Scope of published data: anonymized unit labels (Unit 1 / Unit 2), no names, no initials, no street
  address. Dates and amounts are retained per the owner's instruction; the site carries an explicit
  re-identification warning because exact dates + exact amounts + ZIP code are themselves identifying.

## Sources, verification and irregularities

Filled in at T4/T5 completion — see `data/sources.json` (every published row) and the site's
**Flagged for review** page.
