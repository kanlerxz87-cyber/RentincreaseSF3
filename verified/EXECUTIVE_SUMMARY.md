# Executive summary — verified edition (7 November 2026)

This is the executive summary for the **verified edition** published at `verified/`. The repository root keeps the
shared consolidated summary in `EXECUTIVE_SUMMARY.md`; both were reviewed against the same official sources on
7 November 2026 and agree on every headline figure.

---

# Executive summary — rent increases for two San Francisco units

Verified against official sources on **7 November 2026**. Rates and pending legislation change; re-check before
serving any notice. **Not legal advice.** Names, initials, street address and ZIP are withheld; dates and amounts
are reproduced unchanged.

---

## 1. The Rent Board question — first, because it decides whether anything else matters

> *“I read that I need to inform the Rent Board and apply for a license. I am an individual owner, not a
> corporation — do I still need to do that before notifying tenants of a rent increase?”*

**Yes.** Being an individual rather than a corporation changes nothing, and the licence is not something you
apply for — it is generated automatically from your annual Housing Inventory report.

| Question | Official answer | Source |
|---|---|---|
| Must every owner report? | “All owners of residential property are required to report.” “Most owners are required to do this even if you are not a landlord.” | [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) |
| Does a 2-unit building count? | Yes. Reporting began **1 March 2023** “for condominiums and units in buildings with fewer than 10 units.” | [sf.gov](https://www.sf.gov/rent-board-housing-inventory) |
| Separate application or fee? | No. The licence is “automatically generated for non-owner occupied units”; “Reporting is free.” | [sf.gov](https://www.sf.gov/rent-board-housing-inventory) |
| When must it exist? | “before any annual or banked rent increase can go into effect”; without it “your rent increase notice will not be enforceable”. | [sf.gov](https://www.sf.gov/rent-board-housing-inventory) |
| Deadline | **1 March every year**; late filing allowed, no monetary penalty, but the increase stays unenforceable until the licence exists. | [sf.gov](https://www.sf.gov/rent-board-housing-inventory) |
| In the ordinance itself? | § 37.3(a)(1): a landlord who has reported “as set forth in Section 37.15 shall have a license to impose annually a rent increase…”. | [Admin. Code § 37.3](https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_admin/0-0-0-70881) |
| Must I file the increase notice? | **No.** “Landlords are not required to file a petition with the City to impose these types of rent increases”; “Banked increases do not have to be approved by the Rent Board”. | [sf.gov](https://www.sf.gov/information/annual-rent-increase-multiple-years) · [sf.gov](https://www.sf.gov/information/banked-rent-increases) |
| Which increases *do* need a petition? | Only six types (capital improvement, operating & maintenance, comparable rents, Proposition I history, utility passthrough, Rule 1.21) — none is an annual or banked increase. | [sf.gov](https://www.sf.gov/landlord-petitions-and-passthroughs) |
| Is what I submit private? | No — “The information entered in the housing inventory submission is public”, and tenants can look up your licence status on the portal. | [sf.gov](https://www.sf.gov/rent-board-housing-inventory) |

**Steps:** report both units at [portal.sfrb.org](https://portal.sfrb.org/) → confirm a licence was generated for
each tenant-occupied unit → reconstruct each tenancy's anniversary and rent history → compute the ceiling
(add percentages, never compound, base rent only, no rounding up) → check filed legislation → serve the § 827
notice with amount, percentage, effective date and the banked portion → keep the proof of service and the
history. Full walk-through: `verified/guide/license-and-process.html`.

---

## 2. The ceiling, layer by layer

| Layer | Limit | Role here | Source |
|---|---|---|---|
| S.F. Rent Ordinance ch. 37 | 60% of the published CPI change, max 7%; **1.6%** for 1 Mar 2026 – 28 Feb 2027 (1.4% prior year) | **Sets the ceiling** | [§ 37.3(a)(1)](https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_admin/0-0-0-70881) · [doc 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) |
| California TPA / AB 1482 | 5% + CPI or 10%, whichever is lower — **8.8%** for 1 Aug 2026 – 31 Jul 2027; expressly inapplicable where a lower local cap governs (§ 1947.12(d)(3)) | Displaced | [oag.ca.gov](https://oag.ca.gov/rentcaps) · [§ 1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) |
| Federal | No federal rent ceiling; the Fair Housing Act bans discriminatory terms | Governs reasons only | [42 U.S.C. § 3604](https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm) |

---

## 3. What each unit may lawfully be raised to

| | Unit 1 | Unit 2 |
|---|---|---|
| Lease start / anniversary | 1 Feb 2025 → **1 February** | 1 Jun 2019 → **1 June** |
| Current base rent | $3,995.00 | $3,150.00 |
| Unused allowances | 1.4% (1 Feb 2026, banked) + 1.6% (1 Feb 2027) = **3.0%** | 1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 + 1.6 = **13.1%** |
| Maximum lawful | **$119.85 → $4,114.85** | **$412.65 → $3,562.65** |
| Notice | 30 days | 90 days (more than 10%) |

- The 1 April 2026 renewal, at which a second occupant joined a continuing original tenant, is **not a vacancy and
  cannot support extra rent** — “A landlord cannot charge additional rent simply because a new (or additional)
  roommate has moved into a unit with the existing tenant.” ([sf.gov](https://www.sf.gov/learn-about-rent-increases-san-francisco))
- Unit 2's 13.1% is **conditional** on no increase having been taken since 2019; no lease, notice or proof of
  service exists in this file (flag F-2).
- Banking test: Unit 1 has 24 months without an increase by 1 February 2027 and Unit 2 for years, so both pass
  under both the 24-month rule and the 12-month worked example (flag F-1).

---

## 4. Recommendation

| Unit | Increase | Effective | Serve by (in person / by mail) |
|---|---|---|---|
| Unit 1 | **3.0% = $119.85 → $4,114.85** | 1 Feb 2027 | 2 Jan 2027 / 28 Dec 2026 |
| Unit 2 | **10.0% = $315.00 → $3,465.00** (3.1% left banked) | 1 Jun 2027 | 2 May 2027 / 27 Apr 2027 |

- Unit 2 at exactly 10% is “10 percent or less”, so 30 days is the statutory minimum; the full 13.1% needs 90 days
  (serve by 3 Mar 2027, or 26 Feb 2027 by mail).
- A 13.1% increase effective 1 February 2027 is **already out of reach**: 90 days' notice required service by
  3 November 2026 (29 October 2026 if mailed) — flag F-9.
- File 261020 would cap banked + capital-improvement increases at 10%/year for three years. Status on
  7 November 2026: **Pending Committee Action — not law**. It is the reason to take 10% first rather than 13.1%
  in one step ([Legistar](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770)).

---

## 5. Noticing and reasons

- Written notice: 30 days if the increase is 10% or less, 90 days if more, **+5 days if mailed**
  ([Civ. Code § 827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827);
  [CCP § 1013](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1013)).
- The notice must state the dollar amount, the percentage, the effective date and **which part is banked**; § 37.3(b)
  additionally requires each component to be identified
  ([sf.gov](https://www.sf.gov/information/banked-rent-increases) · [§ 37.3(b)](https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_admin/0-0-0-70881)).
- Use the rate in effect on the **effective date**, not on the date of service (sf.gov).
- **No official source requires a reason** for an annual or banked increase — the required contents are an
  exhaustive list on both the sf.gov page and § 37.3(b). Reasons are mandatory only for petition-based increases.
- Reasons that are never permissible: anything tied to a protected characteristic
  ([Gov. Code § 12955](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=12955);
  [42 U.S.C. § 3604](https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm)),
  retaliation within 180 days of a repair request or complaint
  ([Civ. Code § 1942.5](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5)),
  or the arrival of an additional occupant (sf.gov).

---

## 6. One unit or both?

Neither the ordinance nor the cited statutes require identical increases across tenancies: each ceiling is computed
from that tenancy's own base rent, anniversary and history. What is unlawful is a difference that is *because of* a
protected characteristic or retaliatory. Raising one unit alone is not automatically unlawful, but it is the version
that invites inquiry. **Recommended: one written rule — “the published annual allowance plus what this tenancy
accrued” — applied to both units on each anniversary**, with both notices in the same form and each unit's rent
history documented before service. Unit 1 at 3.0% and Unit 2 at 10.0% then differ for a reason that is written down
and verifiable.

---

## 7. Corporate versus individual practice

Institutional practice appears in the official record mainly as the problem the City legislated against:
San Francisco banned algorithmic rent-setting devices in 2024 (§ 37.10C, ordinance findings referring to “as much
as 70% of all rental housing”), and the U.S. Department of Justice sued six of the largest landlords over common
pricing algorithms. No official source quantifies how often large versus small owners take increases, so that
comparison is left blank. The compliance mechanics are identical for both — there is no size exemption.

---

## 8. Flagged for review (12 items; none blocks publication)

1. **F-1 Banking** — the Banking page requires 24 full months; a worked example on another sf.gov page banks after
   12. Both ledgers here pass either way.
2. **F-2 Unit 2 rent history** — unverified; 13.1% is conditional.
3. **F-3** — the 2027–28 allowance is not yet published (blank).
4. **F-4** — Unit 1's anniversary after the April 2026 renewal (1 February used; 3.0% either way).
5. **F-5** — no official ZIP-level market rent exists (blank).
6. **F-6** — no official corporate-versus-individual dataset (qualitative only).
7. **F-7** — building facts are the owner's statement (1940, two units) — not independently verified.
8. **F-8** — rent increase licence status unknown; every recommendation is conditional on it.
9. **F-9** — a 13.1% increase effective 1 February 2027 is already impossible on notice.
10. **F-10** — File 261020 is Pending Committee Action, not “30 Day Rule” as earlier editions stated.
11. **F-11** — housing subsidy status unknown; a voucher changes the ceiling and bars passthroughs.
12. **F-12** — two official worked examples carry rate-year labels that conflict with document 571; 571 controls.

Full detail with sources: `verified/guide/flagged.html`.
Verified against official sources on **7 November 2026**. Rates and pending legislation change; re-check before serving any notice. This is an information record, not legal advice. Personal information is anonymized (placeholder tenant names only); dates and dollar amounts are unchanged.

## 1. THE RENT BOARD QUESTION — READ FIRST (individual / non-corporate owner)

**Short answer: Yes.** Even if you are an individual property owner and not part of a corporation, you must report your units to the San Francisco Rent Board and hold a current rent increase license before any annual or banked rent increase can go into effect. There is **no small-landlord or individual-owner exemption**.

- **Report to the Rent Board.** Every owner of residential property must report each unit into the Rent Board's **Housing Inventory** online through the Rent Board Portal (portal.sfrb.org). Reporting is free, due every **March 1**, and for buildings with 1–9 residential units (like this two-unit building) it applies to rent increases effective on or after **March 1, 2023**. [sf.gov — The Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) · [sf.gov — Ordinance 265-20](https://www.sf.gov/news--new-legislation-creates-housing-inventory-and-requires-owners-obtain-license-imposing)
- **Hold a rent increase license.** Once you report a tenant-occupied unit, a rent increase license is generated automatically. **A landlord must have a current rent increase license on file with the Rent Board before any annual or banked rent increase can go into effect.** The license does not need to be included with the tenant notice, but it must exist on the increase's effective date; without it the increase is null and void. [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) · [sf.gov — Learn about rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco)
- **This is how you "inform the rent board."** The Housing Inventory report is your notification to the Rent Board. The Rent Board does not notify your tenants for you: **you** serve the tenant a written notice yourself (step 4 below), and the increase takes effect only after the notice period runs and the license is in place.

**Privacy note:** Housing Inventory submissions are public and made under penalty of perjury — report true information; placeholder names belong only on the public website, not on statutory filings. [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory)

## 2. Step-by-step process (official sources)

| Step | Action | Official source |
|------|--------|-----------------|
| 1 | Report each tenant-occupied unit into the Rent Board Housing Inventory and confirm a rent increase license exists — required **before** any annual or banked increase takes effect; file by March 1 every year. | [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) |
| 2 | Confirm coverage and the current rate. Building built 1940 (pre-June 13, 1979) ⇒ units covered by the SF Rent Ordinance. Current allowable annual increase: **1.6%** for increases effective 3/1/2026–2/28/2027 (60% of Bay Area CPI), once every 12 months, on base rent only. | [sf.gov — SF rental laws](https://www.sf.gov/learn-about-san-francisco-rental-laws) · [sf.gov — rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) |
| 3 | Calculate on base rent only: base rent × allowable %; include housing services, exclude passthroughs; do not round up. Banked (skipped) years are added, never compounded; a skipped year is banked only after 24 full months without any increase. | [sf.gov — rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) · [sf.gov — Banked rent increases](https://www.sf.gov/information--banked-rent-increases) |
| 4 | Serve written notice to the tenant: **30 days** if the increase is 10% or less; **90 days** if more than 10% (alone or combined with increases in the prior 12 months); +5 days if mailed. Notice must state the dollar amount, percentage, and effective date (and which part is banked, with dates). | [sf.gov — rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) · [Cal. Civ. Code §827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) |
| 5 | The increase takes effect only with a current license on file on the effective date, and at least 12 months after the last increase. | [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) |
| 6 | Apply the same written policy to both units on the same schedule; differences traceable to each unit's own rent history are defensible, arbitrary differences are not. | [sf.gov — discrimination → SF Human Rights Commission](https://www.sf.gov/evictions-san-francisco) · [hud.gov — Fair Housing Act](https://www.hud.gov/program_offices/fair_housing_equal_opp) |

## 3. Applicable ceilings — local, state, federal

| Level | Rule | Value for these units |
|-------|------|----------------------|
| Local — SF Rent Ordinance (Admin. Code Ch. 37) | Covers units in buildings occupied before June 13, 1979; one increase per 12 months; base rent only | **Applies** (1940 building) |
| Local — annual allowable increase | Rent Board rate = 60% of Bay Area CPI change, capped at 7% | **1.4%** (3/1/2025–2/28/2026); **1.6%** (3/1/2026–2/28/2027) |
| Local — banked increases | Skipped annual increases can be saved and added later; added not compounded; no limit; do not expire during the tenancy | Available if 24 months without an increase have passed |
| State — AB 1482 / Civ. Code §1947.12 | Cap = 5% + regional CPI, max 10% per 12 months, but **exempts units already under a stricter local rent-control ordinance** | Not the governing cap (local cap is stricter); state regional cap for reference: 8.8% (8/1/2026–7/31/2027) |
| State — notice, Civ. Code §827 | ≥30 days if ≤10%; ≥90 days if >10%; +5 days if mailed | Applies to both units |
| Federal — 42 U.S.C. §3604 | No federal rent cap; bans discriminatory terms/conditions | Uniform treatment of both units |

Sources: [sf.gov — Current rates](https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit) · [sf.gov — AB 1482](https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482) · [leginfo §1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) · [leginfo §827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) · [govinfo — 42 U.S.C. §3604](https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm) · [Rent Board Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf)

## 4. Bottom-line numbers per unit (anonymized — arithmetic from official rates, not certified lawful rents)

| Unit | Baseline (as provided) | Lawful increase analyzed | New rent | Notice / requirements |
|------|------------------------|--------------------------|----------|----------------------|
| **Unit 1** | Lease start Feb 1, 2025 @ $3,995/mo; continuing tenancy Apr 1, 2026 @ $3,995/mo (one original tenant remains — not a new tenancy, no market reset) | **3.0% = $119.85** effective Feb 1, 2027: 1.4% banked (skipped Feb 1, 2026 anniversary) + 1.6% current annual. Anniversary stays Feb 1. | **$4,114.85**<br>fallback 1.6% = $63.92 → $4,058.92 | License required; **30-day** notice, served by Jan 2, 2027 (Dec 28, 2026 if mailed) |
| **Unit 2** | Lease start June 1, 2019 @ $3,150/mo; rent history since then **not provided** (flagged) | **13.1% = $412.65** only if no increase was ever imposed: 11.5% banked (June 2020–June 2025 anniversaries) + 1.6% current. Otherwise 1.6% = $50.40 → $3,200.40 | **$3,562.65** conditional — flagged<br>or $3,200.40 at 1.6% | License required; **90-day** notice (&gt;10%), served by Nov 30, 2026 (Nov 25, 2026 if mailed); notice must itemize banked years and dates |
| **Unit 2 — recommended** | Same baseline | **10.0% = $315.00** now: lawful today, stays lawful if the pending 10%/yr cap (Legistar File 261020) passes, leaves 3.1% ($97.65) banked — easier to defend than a 13.1% single step | **$3,465.00** | License required; **30-day** notice (10% ≤ 10%) |

Rules applied throughout: percentages added, never compounded; base rent only; nothing rounded up; one increase per 12 months; current rent increase license required on the effective date.

## 5. Raise one unit, or both?

Neither the Rent Ordinance nor fair-housing law requires equal percentage increases, and raising only one unit is not unlawful by itself; equally, uniform increases are not an automatic safe harbor — unlawful treatment arises when a difference is tied to a protected characteristic (Cal. Gov. Code §12955; 42 U.S.C. §3604) or retaliation (Civ. Code §1942.5). The defensible pattern is **one written rule applied to both units on the same schedule**, with each unit's rent history documented before notice is served. Different outcomes that follow from seven skipped years versus two are explainable; applying different rules to similarly placed tenants is what invites discrimination inquiries or lawsuits.

Sources: [leginfo — Gov. Code §12955](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=12955) · [govinfo — 42 U.S.C. §3604](https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm) · [sf.gov — SF Human Rights Commission referral](https://www.sf.gov/evictions-san-francisco)

## 6. Scrutiny readiness — built to pass review by a San Francisco tenant lawyer

San Francisco tenants can obtain free legal help (Eviction Defense Collaborative, 415-659-9184; Rent Board counseling, 415-252-4600) and may file a no-fee tenant petition, including challenging an invalid rent-increase notice. Free counseling is available; it is not a guaranteed free lawyer for every dispute. An increase built this way is designed to pass that review:

- Coverage confirmed (pre-6/13/1979 building) — [sf.gov](https://www.sf.gov/learn-about-san-francisco-rental-laws)
- Current rent increase license on file before the effective date — [sf.gov — Housing Inventory](https://www.sf.gov/rent-board-housing-inventory)
- Correct rate for the effective date; base rent only; no rounding up — [sf.gov](https://www.sf.gov/learn-about-rent-increases-san-francisco)
- Once-per-12-months limit; banked math added not compounded — [sf.gov — banked increases](https://www.sf.gov/information--banked-rent-increases)
- Written 30/90-day notice stating dollar amount, percentage, effective date, banked breakdown — [Civ. Code §827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) · [sf.gov](https://www.sf.gov/information--banked-rent-increases)
- No charge for additional occupants; no reason tied to a protected characteristic, complaint, repair request, or new roommate — [sf.gov](https://www.sf.gov/learn-about-rent-increases-san-francisco)
- Same written policy for both units; differences traceable to rent history — [Gov. Code §12955](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=12955) · [42 U.S.C. §3604](https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm)

Free tenant help: [sf.gov — Tenant Petitions](https://www.sf.gov/tenant-petitions) · [sf.gov — Evictions](https://www.sf.gov/evictions-san-francisco) · [sf.gov — Rent Board](https://sf.gov/departments/rent-board/about) · [California Civil Rights Department](https://calcivilrights.ca.gov/housing/)

## 7. Flagged items (do not block publishing; see pages/flagged.html)

- Unit 2 rent history since June 1, 2019 not provided — the 13.1% figure is conditional on no increase ever having been imposed.
- Certificate-of-occupancy date of the specific building not independently verified (coverage argued from the stated 1940 build).
- Current rent increase license / Housing Inventory status unknown — verify before serving any notice.
- Section 8 / voucher status of tenants unknown (if applicable, federal rent-reasonableness rules and housing-authority approval apply).
- Pending ordinance Legistar File 261020 (10%/yr cap on combined banked + capital-improvement increases) is **not law** — re-check before serving any banked catch-up.
- Rent Board Rule 4.12(a) still says a full 12 months for banking; current sf.gov guidance requires 24 full months. For Unit 1 both readings point to Feb 1, 2027, so the recommended figure is unchanged.
- Coverage/exemptions, subsidy status, lease restrictions, actual increase history, license status and banking eligibility remain unverified.

Personal information is kept internal: tenant names are placeholder labels (Tenant A–F), and the specific address/ZIP/neighborhood are withheld. Dates and dollar amounts are shown exactly as provided because they drive the legal arithmetic. Not legal advice — confirm with the San Francisco Rent Board (415-252-4600) and a California attorney before acting.
