# Rental Increase Review — Outer Sunset, San Francisco (ZIP 94122)

A verified, source-linked analysis of what two rent-controlled units in a 1940 San Francisco
building may lawfully be charged, how to notify the tenants, and how the increase would fare under
review by a tenant-side advocate or lawyer.

**Live site:** https://kanlerxz87-cyber.github.io/RentincreaseSF3/

---

## What is here

| Path | What it is |
|---|---|
| `index.html` | Dashboard: key numbers, unit snapshot, action plan, findings |
| `executive-summary.html` | One-page decision summary |
| `units.html` | Anonymised unit record and the coverage test |
| `requirements.html` | Federal, state and local rules, one row per rule, each with its source |
| `calculations.html` | The arithmetic, anniversary by anniversary, plus options per unit |
| `notices.html` | Deadlines, required notice contents, model letter, safe/unsafe reasons |
| `fair-housing.html` | Whether to raise one unit or both, and how to document either choice |
| `practice.html` | How institutional owners and individual owners handle increases |
| `review.html` | 15-point tenant-lawyer / ALJ stress test and the consequence of each failure |
| `flagged.html` | **Flagged for review:** unverified values, conflicting official guidance, pending law |
| `sources.html` | Source register (27 official sources) with the passage each one supports |
| `data/ledger.csv` | Machine-readable per-anniversary rent ledger |
| `data/requirements.csv` | Machine-readable rule table |
| `data/sources.json` | Machine-readable source register |
| `research/source-register.md` | Offline copy of the source register, with quotes |
| `tools/build_site.py` | Static site generator (Python 3, no dependencies) |
| `tools/sitedata.py` | All verified data: rates, ledgers, rules, flags, sources |
| `tools/check_site.py` | Link/anchor/source-chip checker used before publishing |
| `COORDINATION.md` | Shared task board for multi-session work on this repo |

## Privacy

Personal identifiers are **not** stored in this repository. Units and tenants appear only as
placeholder labels (`Unit A`, `Unit B`, `Tenant`). The mapping from placeholders to real names is
deliberately kept out of the repo. Dates and dollar amounts are preserved exactly, because the
lawful increase cannot be computed or audited without them. Location is limited to the ZIP code
(94122) and neighbourhood; no street address is published.

## Verification policy

* Every rule, rate and calculation row links to a government source: `sf.gov` (San Francisco Rent
  Board), `sfgov.legistar.com`, `leginfo.legislature.ca.gov`, `oag.ca.gov`, `govinfo.gov`,
  `justice.gov`, `sec.gov`.
* Rates are taken from the Rent Board's own historical table (document 571), not from memory.
* Arithmetic is simple addition of published percentages applied once to base rent — no compounding,
  no rounding up — and is shown in full on the site so it can be re-checked line by line.
* Where a value could not be confirmed from an official source it is **left blank** and recorded on
  `flagged.html`. Nothing is inferred or filled in.
* Verification date: **2026-11-06**. Rates and pending legislation change; re-check before serving
  any notice.

## Open items (see `flagged.html`)

1. Two official Rent Board pages describe the banking threshold differently (12 vs 24 months).
2. A 10% cap on combined banked + capital-improvement increases is pending (Legistar File 261020).
3. The property record (year built, unit count, use) has not been pulled.
4. The Housing Inventory report / rent increase licence status is unknown.
5. No documentary rent history (leases, prior notices, proofs of service) has been supplied.
6. Subsidy (Section 8 / HUD) status is unknown.
7. No ZIP-level market-rent benchmark was retrievable from an official source, so none is presented.

## Rebuild

```bash
python3 tools/build_site.py   # regenerate HTML, data exports and the source register
python3 tools/check_site.py   # verify internal links, anchors and per-row source chips
```

GitHub Pages serves this repository from `main` at the repository root (legacy build, no Jekyll
processing because of `.nojekyll`). No CI is required; the checks above are run before each push.

## Disclaimer

This is an information and audit record, not legal advice. Rent-control coverage, prior rent
history and licensing are not independently verified. Confirm the specific situation with the San
Francisco Rent Board (415-252-4600) and a lawyer before serving any rent-increase notice.
