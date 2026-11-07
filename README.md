# Current consolidated site — November 7, 2026

**Start here:** https://kanlerxz87-cyber.github.io/RentincreaseSF3/

The landing page is now the canonical executive summary, with categorized subpages under `audit/`.
Read `EXECUTIVE_SUMMARY.md` for the text version. Individual-owner license requirements come first.
All property facts are owner-reported, not government-certified. Missing verified values are blank;
conditional calculations are not lawful-rent determinations. See `audit/flagged.html`.

Earlier editions below are **archived research** and may disagree. Historical verification claims
and source logs below describe prior sessions, not a fresh certification. Unsupported catch-up
recommendations in the former standalone summary are withdrawn. Automated checks:
`python tools/audit_site.py`, `python verify_site.py`, `python tools/check_site.py`.

---

## Historical README (preserved)

# RentincreaseSF3

Source-verified analysis of **lawful, reasonable and normal rent increases** for two rent-controlled flats in
one **1940 two-unit building in San Francisco** (specific location withheld for privacy — every cited rule
applies citywide).

**Live site: <https://kanlerxz87-cyber.github.io/RentincreaseSF3/>**

- **Not legal advice.** Confirm with a San Francisco Rent Board counselor, 415-252-4600, before serving any notice.
- **Privacy:** no tenant names or initials, no street address, no ZIP code. Dates and dollar amounts are unchanged.
- **Sourcing rule:** every table row links an official source, or is explicitly marked blank / flagged / analysis.
  Nothing is estimated. Where two official sources disagree, both are published (see the Flagged page).

## What is here

| Path | What it is |
|---|---|
| `index.html` + `guide/` | **The verified edition** — dashboard landing page and nine category subpages (executive summary, license & process, units & math, rates 1982–2027, notice & reasons, laws, “is it reasonable?”, flagged for review, sources) |
| `tools/verify_edition.py` | Pre-publish check: internal links and anchors, one citation per data row, privacy sweep, no remote code |
| `EXECUTIVE_SUMMARY.md` | The executive summary in Markdown |
| `COORDINATION.md` | Cross-session task board, claims, merge and deploy records |
| `docs/`, `dashboard/`, `review/` | Earlier editions, live and unchanged (linked from the Sources page) |
| `pages/` | The 6 November 2026 core edition, retained for provenance and marked **superseded** — it contains known errors |

## Headline findings (verified 7 November 2026)

| Item | Result | Source |
|---|---|---|
| Annual allowance 1 Mar 2026 – 28 Feb 2027 | **1.6%** (1.4% prior year) | sf.gov announcement; Rent Board document 571 |
| Rent increase license | **Required, including for an individual owner of a 1–9 unit building.** Generated automatically from the Housing Inventory report; reporting began 1 Mar 2023 for these buildings; deadline 1 Mar each year; the increase is unenforceable without it on the effective date | sf.gov — Rent Board Housing Inventory; Admin. Code § 37.3(a)(1) |
| Must the increase notice itself be filed? | **No** — annual and banked increases need no petition | sf.gov — multiple years; banking |
| Unit 1 | **3.0% = $119.85 → $4,114.85** effective 1 Feb 2027 (1.4% banked + 1.6% current), 30-day notice | Rent Board document 571 |
| Unit 2 | **13.1% = $412.65 → $3,562.65** maximum (seven banked years), 90-day notice; **recommended 10.0% = $315.00 → $3,465.00** | Rent Board document 571; Legistar File 261020 (pending, not law) |
| State cap (AB 1482) | 8.8% for 1 Aug 2026 – 31 Jul 2027 — displaced here because the local cap is lower (Civ. Code § 1947.12(d)(3)) | oag.ca.gov; sf.gov |
| Federal law | No federal rent ceiling; the Fair Housing Act governs the reasons | 42 U.S.C. § 3604 |
| Pending | File 261020 would cap banked + capital-improvement increases at 10%/year for three years; status **Pending Committee Action** — not law | sfgov.legistar.com |

## Run the checks

```bash
python3 tools/verify_edition.py     # links, anchors, per-row citations, privacy, no remote code
```

The site is plain HTML + one stylesheet, with no JavaScript, no fonts and no tracking, so it builds on GitHub
Pages without a build step (`.nojekyll` is present).
