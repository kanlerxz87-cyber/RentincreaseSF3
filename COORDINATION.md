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

## Concurrent session claim
# Coordination board

| Task | Status | Owner | File scope |
|---|---|---|---|
| Official-source research, privacy-safe site, integration and publication | in progress | arena-a07a8788 | COORDINATION.md, README.md, site files, GitHub Pages configuration |

The Arena session branch is fixed at `arena/a07a8788-rentincreasesf3`; this session cannot create or switch to a `session-*` branch. No prior claims were present when this board was created.

- Concurrent sessions claimed work before either board was visible. Main received PR #2; this rebase preserves both boards. Integration conflict requires review.

## Concurrent integration record
## Integration record — 2026-11-06
- Static site and official-source research completed by arena-a07a8788; no other claims were present. Source links and fact-level caveats appear in each table row.
- Checked the [2026–27 Rent Board announcement](https://www.sf.gov/news--annual-rent-increase-3126-22827-announced), [annual increases and notice](https://www.sf.gov/learn-about-rent-increases-san-francisco), [banking](https://www.sf.gov/information--banked-rent-increases), [coverage](https://www.sf.gov/learn-about-san-francisco-rental-laws), [roommates](https://www.sf.gov/information--replacement-roommates), [state cap](https://oag.ca.gov/news/press-releases/attorney-general-bonta-shares-updated-resources-statewide-and-local-rent), [state notice law](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=827&lawCode=CIV), and [fair housing](https://calcivilrights.ca.gov/housing/). Private facts cannot be independently verified from these sources.
- Local HTML links and the presence of an official source in each data row were checked programmatically; static site requires no build. Illustrative arithmetic checked. The city annual examples contain apparent date errors; the site's review page flags these, as well as unverified coverage, current rent, rent history, license, occupancy, privacy and lack of counsel review.
- Publication and PR outcome pending. The remote session branch did not exist for the initial pull; rebased from main before initial push instead.

| Task | Status | Owner | File scope |
|---|---|---|---|
| Official-source research, privacy-safe site, integration and publication | needs review | arena-a07a8788 | COORDINATION.md, README.md, HTML pages, style.css |

- Rebase conflict: another session merged PR #2 while both sessions worked from the initially empty repository. Both boards were retained. That session owns index.html and pages/*.html; its index was retained, and its pages were not modified. Request: correct the unsupported assertion that the April 2026 roommate change resets Unit 1 timing, the unconditional coverage/base-rent assertions, and missing official links in private-fact table rows. Do not treat those pages as legally verified until reviewed. The complementary root-level pages remain unintegrated pending that work.
