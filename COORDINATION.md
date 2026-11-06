# COORDINATION — Shared Task Board

Repo: `kanlerxz87-cyber/RentincreaseSF3`
Last updated: 2026-11-06 (UTC)

## Session IDs

| Session | Branch | Status |
| --- | --- | --- |
| `arena-8f9507cf` | `arena/8f9507cf-rentincreasesf3` | active — owns T1–T10 |

> Note on branch naming: the Arena session branch is fixed and may not be renamed, so this session uses
> `arena/8f9507cf-rentincreasesf3` in place of the generic `session-<id>/<task>` convention. File scopes are
> kept non-overlapping as the protocol requires.

## Task board

| # | Task | Status | Owner | Files / scope | Claimed (UTC) | Last commit |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | Scaffold repo, coordination board, site skeleton | **done** | arena-8f9507cf | `COORDINATION.md`, `README.md`, `assets/`, `build.py` | 2026-11-06 13:05 | see log |
| T2 | Verify local law (SF Rent Ordinance Ch. 37, AGA 1.6%, coverage, banking, license) | **done** | arena-8f9507cf | `data/findings.json` §`local` | 2026-11-06 13:05 | see log |
| T3 | Verify California state law (Civ. Code 827, 1947.12/AB 1482, 1954.52 Costa-Hawkins) | **done** | arena-8f9507cf | `data/findings.json` §`state` | 2026-11-06 13:20 | see log |
| T4 | Verify federal layer (Fair Housing Act, no federal rent cap, algorithmic pricing enforcement) | **done** | arena-8f9507cf | `data/findings.json` §`federal` | 2026-11-06 13:20 | see log |
| T5 | Institutional vs. individual owner practice; notice + justification standards | **done** | arena-8f9507cf | `data/findings.json` §`practice` | 2026-11-06 13:30 | see log |
| T6 | Tenant-lawyer review test; one-unit-vs-both-units discrimination analysis | **done** | arena-8f9507cf | `data/findings.json` §`review` | 2026-11-06 13:30 | see log |
| T7 | Unit 1 / Unit 2 worked calculations (no inference; flag unknowns) | **done** | arena-8f9507cf | `data/findings.json` §`units` | 2026-11-06 13:30 | see log |
| T8 | Site build (landing page + category subpages + tables) | **done** | arena-8f9507cf | `build.py`, `*.html`, `assets/` | 2026-11-06 13:38 | see log |
| T9 | Link check + line-by-line verification pass | **done** | arena-8f9507cf | `verify.py` | 2026-11-06 13:44 | see log |
| T10 | Integration: PR to `main`, merge, confirm Pages deploy | **in progress** | arena-8f9507cf | `COORDINATION.md`, repo root | 2026-11-06 13:45 | see log |

No task is claimed by any other session. No claim is stale. No cross-scope requests are open.

## Log

### 2026-11-06 — `arena-8f9507cf`

**13:05** — Read repo at `dab56c9`: only `README.md` (17 bytes). No prior work, no other session claims.
Claimed T1 and T2. Scope: `COORDINATION.md`, `README.md`, `assets/`, `build.py`, `data/findings.json` §`local`.

**13:06** — Registered 45 sources in `data/sources.json` (primary / official-summary / filer tiers, each with
the date read). Every document was retrieved and read directly; no secondary source was allowed into the
register.

**13:20** — Claimed T3 and T4. Completed the state and federal sections (13 and 7 rows). Two findings were
recorded as unverified rather than asserted: that no federal rent cap exists (an absence cannot be proven by
citation), and the HUD FY2026 two-bedroom figure (the value cells on HUD's page did not render).

**13:30** — Claimed T5, T6 and T7. Completed practice (10 rows), review test (16 rows) and worked calculations
(14 rows). Unit 2's seven annual allowances add to 13.1%, i.e. $412.65 on $3,150, and the year-by-year dollar
sum was cross-checked against the single-step figure to prove no compounding. Claimed T8 and started the build.

**13:38** — `build.py` generates 9 pages from the two registries. It refuses to build if a row names an unknown
source, a non-HTTPS URL, or a host that is not an official domain or an SEC filing. 86 findings, 54 sources.

**13:44** — Claimed T9. `verify.py` passes: all internal links resolve, all 54 external links are allow-listed and
registered, HTML balances on all 9 pages, both units recompute to the cent, and no supplied personal identifier
appears in the output.

**13:45** — Claimed T10. Opening the PR to `main`.

**Corrections made during this session** (recorded because they were real defects, not polish):

1. The executive summary first said "six items are unverified". The registry actually holds 3 unverified values
   plus 4 rows whose facts were not supplied. Hardcoded counts in prose drift, so all counts are now computed in
   one place (`build.counts`) and `verify.py` asserts the prose matches. `verify.py` imports the same function, so
   the two scripts cannot disagree about what "flagged" means.
2. `verify.py` first parsed the Unit 2 year list by looking for `%` suffixes, but the row writes the expression as
   `1.8 + 0.7 + …`, so the check silently compared a single number and failed to validate anything. It now parses
   both sides of the `=` and also re-checks the seven-year ladder in U07 against the published rates.
3. `flagged.html` initially conflated "value could not be confirmed" with "fact was not supplied". These need
   different remedies, so items are now grouped into three classes and each class gets its own closure steps.

**Known limitations, published rather than hidden:** 15 of 86 findings carry a caveat. The three that matter most
for a real notice are the licence status of both units (not verified), whether a 1.4% increase was actually served
on Unit 1 in February 2026 (not supplied), and the 2019 rent history behind Unit 2's $3,150 base (not supplied).
Two official Rent Board documents also disagree on the banking waiting period (12 vs 24 months); the conflict is
recorded at `L13` and does not affect the Unit 2 result under either reading.

### Rules in force for this repo

1. Every table row carries a source link to an official/primary source (`.gov`, `sfgov.org`,
   `leginfo.legislature.ca.gov`, `law.cornell.edu` for U.S. Code and CFR, `sec.gov`).
2. Unconfirmed values are left **blank** and marked `UNVERIFIED` — never inferred or filled in.
3. Personal identifying information is never published. Placeholder party codes only (P1–P6), with dates and
   amounts unchanged. `verify.py` fails the build if any supplied identifier string appears in the output.
4. Shared outputs (site navigation, table data) are changed only by the integration session (T10).
