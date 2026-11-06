# Verification log

Date of verification: **2026-11-06**. Method: every figure and rule used on the site was fetched from a
government source during this session, read directly, and then cross-checked against at least one
independent official source where one exists. The quoted passage for each source is reproduced in
`source-register.md` and on `sources.html`.

## Line-by-line checks

| # | Assertion on the site | How it was verified | Result |
|---|---|---|---|
| 1 | Annual allowable increase is 1.6% for 3/1/2026–2/28/2027 | Rent Board news release; Rent Board "Current Rates" page; Rent Board "Learn about rent increases" page; document 571 | Consistent across four official pages |
| 2 | Prior year was 1.4% (3/1/2025–2/28/2026) | Same four pages | Consistent |
| 3 | Historical rates 2019–2024 (2.6, 1.8, 0.7, 2.3, 3.6, 1.7) | Document 571 (complete 1982–2027 table) | Read from the official table, not memory |
| 4 | Formula is 60% of prior-year Bay Area CPI, capped at 7% | Ordinance §37.3(a)(1) text; Rent Board page; Attorney General local-cap chart | Consistent |
| 5 | San Francisco's cap displaces AB 1482 | Civil Code §1947.12(d)(3) text; Attorney General chart (state 8.8% vs local 1.6%) | Consistent |
| 6 | Coverage threshold is 13 June 1979 | Rent Board "Learn about San Francisco rental laws"; Attorney General chart | Consistent |
| 7 | Vacancy decontrol requires that no prior tenant remains | Civil Code §1947.12(b); Costa-Hawkins §1954.52; ordinance §37.3(d) | Consistent |
| 8 | Additional occupants cannot generate rent | Rent Board "Learn about rent increases" (plain language); ordinance §37.3(a)(11) (ordinance PDF) | Consistent |
| 9 | 12-month rule and anniversary-date definition | Rent Board "Learn about rent increases"; "Increasing rents during irregular periods" | Consistent |
| 10 | Banked increases: 24-month condition, no cap, no expiry, partial increases | Rent Board "Banked rent increases" page; "irregular periods" page; Rule 4.12 | **Conflict**: Rule 4.12(a) still reads 12 months. Logged as F1 |
| 11 | Multi-year increases are added, not compounded, and not rounded | Rent Board "Annual rent increase for multiple years"; "Banked rent increases"; Rule 4.12(a) | Consistent |
| 12 | Rent increase licence required; licence must exist on the effective date | Rent Board Housing Inventory page; "Learn about rent increases" | Consistent |
| 13 | Notice: 30 days for ≤10%, 90 days for >10%, +5 if mailed | Civil Code §827(b)(2)–(3); Rent Board pages; Rule 4.10 | Consistent |
| 14 | Notice must break out annual vs banked and the banked dates | Ordinance §37.3(b); Rule 4.10(a); Rule 4.12(b); Rent Board "Banked rent increases" | Consistent |
| 15 | Tenant may petition at no cost, with no time limit; harassment/discrimination not adjudicated there | Rent Board "Tenant Petitions"; "Report an unlawful rent increase" | Consistent |
| 16 | Tenant right to counsel / free legal help | Rent Board "Evictions in San Francisco"; Rent Board Form 1007 text | Consistent |
| 17 | Retaliation prohibited, 180-day presumption | Civil Code §1942.5(a) | Verified from statute |
| 18 | Protected characteristics | Gov. Code §12955(a); 42 U.S.C. §3604(b) | Verified from statute |
| 19 | Algorithmic rent-setting devices banned in SF | Rent Board news release (Ordinance §37.10C, effective 14 Oct 2024) | Verified |
| 20 | Federal antitrust enforcement over algorithmic pricing | DOJ press release, 24 Nov 2025 | Verified |
| 21 | 10% cap on banked + capital-improvement increases is pending, not law | Legistar File 261020 (introduced 9/15/2026, status "30 Day Rule") | Verified as pending only; logged as F3 |
| 22 | Unit A arithmetic: 1.4% + 1.6% = 3.0%; $3,995 × 3.0% = $119.85 | Recomputed by hand and in Python; matches the Rent Board's own multi-year method | Verified |
| 23 | Unit B arithmetic: 13.1%; $3,150 × 13.1% = $412.65 | Recomputed by hand and in Python; cross-checked against the Board's 6.7% worked example method | Verified |
| 24 | Notice deadlines (2 Jan 2027 / 28 Dec 2026 / 30 Nov 2026 / 25 Nov 2026) | Date arithmetic in Python, applying 30/35 and 90/95 day periods | Recomputed |
| 25 | Market rent for the property's ZIP (withheld) | HUD FMR lookup and Census API returned no usable official figure during the session | **Not verified — left blank (F9)** |
| 26 | Year built 1940, two units | Owner statement only | **Not verified (F6)** |
| 27 | Prior rent history for both units | Owner statement only | **Not verified (F5)** |

## Re-check procedure before serving a notice

1. Re-read the Rent Board's current-rate page and document 571 (the rate changes every 1 March).
2. Re-read Legistar File 261020 for enactment status.
3. Confirm the licence is live in the Rent Board portal on the date the increase takes effect.
4. Recompute the increase in cents; confirm no compounding and no rounding.
5. Confirm the notice period against Civil Code §827 for the total increase actually being served.

## Automated checks

`tools/check_site.py` verifies that every internal link and anchor resolves, that every external link is
https, that each data-table row carries at least one source chip, and that no placeholder text remains.
Output at publish time: 11 pages, 1 external link (SEC EDGAR, provided for manual review only), 0 broken
internal links or anchors, 0 rows without a source chip.
