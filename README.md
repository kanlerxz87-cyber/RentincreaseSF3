# RentincreaseSF3

**Analysis of lawful, reasonable, and normal rental increases** for a rent-controlled, two-unit
residential building constructed in **1940** in San Francisco's Outer Sunset (ZIP 94122).

## Three live editions (GitHub Pages), all anonymized

| Edition | URL | What it is |
|---|---|---|
| **Core site** (merged via [PR #2](https://github.com/kanlerxz87-cyber/RentincreaseSF3/pull/2)) | <https://kanlerxz87-cyber.github.io/RentincreaseSF3/> | Landing dashboard, executive summary, units, laws & caps, process & notice, flagged-for-review |
| **Full verification edition** (PR #3) | <https://kanlerxz87-cyber.github.io/RentincreaseSF3/docs/> | Same subject, deeper verification: cents-exact math incl. **banked increases** (Unit 2: up to 11.5%/13.1%), Housing Inventory **rent-increase license** requirement, full 1982–2027 SF rate table, FHA/FEHA/SF discrimination analysis, corporate vs. individual landlord research, sources & verification register, repo review, 17-item flagged register |
| **Third edition — audit trail** (PR #5) | <https://kanlerxz87-cyber.github.io/RentincreaseSF3/review/> | Independent rebuild with a per-anniversary ledger (cents-exact), 21-row federal/state/local rule table, notice deadline planner with a model letter, one-unit-or-both fair-housing matrix, 15-point tenant-lawyer stress test, 27-source register with quoted passages, and a 27-assertion verification log (`research/verification-log.md`). Also flags the **12-vs-24-month banking conflict** between official Rent Board pages |

Both are static HTML, anonymized: occupant names/initials never appear; dates and dollar amounts are unchanged.

- **Not legal advice.** Consult the SF Rent Board (415-252-4600) and a California attorney before acting.
- **Watch item:** SF Legistar File #261020 (pending, **not law** as of 2026-11-06) would cap combined banked + capital-improvement increases at 10%/yr for three years — re-check before serving any banked notice.
- **Source policy:** every table row cites an official source (sf.gov, leginfo.legislature.ca.gov,
  hud.gov, calcivilrights.ca.gov) or is flagged — never guessed. See each edition's Flagged for Review page.

Parallel-session coordination: see `COORDINATION.md`. The full verification edition supersedes nothing;
it complements the core site and logs cross-session findings instead of editing its files.


## Third edition (PR #5) — how it differs

Lives entirely under `review/` (plus `review/data/`, `research/`, `tools/`), so it does not touch the
root site or `docs/`.

- `review/index.html` — dashboard. Subpages: executive summary, units & coverage, rules & limits,
  calculations, notices, one-unit-or-both, owner practice, tenant-lawyer test, flagged for review, sources.
- `review/data/ledger.csv`, `review/data/requirements.csv`, `review/data/sources.json` — machine-readable.
- `research/verification-log.md` — 27 numbered assertions, each with the official source used and the
  cross-check performed. `research/source-register.md` — 27 sources with the quoted passage each supports.
- `tools/build_site.py` / `tools/sitedata.py` — static generator (Python 3, no dependencies);
  `tools/check_site.py` — link, anchor and per-row source-chip checker run before every push.

Headline results (unchanged in substance, independently recomputed): annual cap **1.6%** for
3/1/2026–2/28/2027 (1.4% prior year); Unit 1 **3.0% = $119.85 → $4,114.85** on 1 Feb 2027 (1.4% banked
+ 1.6% current); Unit 2 **13.1% = $412.65 → $3,562.65** (seven banked years) with a recommended 10%
($315.00) phased option while the 10% banked-increase cap (Legistar File 261020) is pending.

Anonymisation: no occupant names or initials, no street address. Dates and amounts preserved.
