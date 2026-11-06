#!/usr/bin/env python3
"""Verification report.

Prints every number published on the site and ASSERTS that the calculation
engine reproduces the SF Rent Board's own worked examples exactly. If any
assertion fails, the site must not be published.

Run:  python3 tools/calc.py
"""
import json
import os
import sys
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rentcalc
from rentcalc import (AGA, aga_on, money, add_days, sub_days, scenario, stats)  # noqa: E402

TODAY = date(2026, 11, 6)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(f"Analysis date (UTC): {TODAY.isoformat()}")

# ---------------------------------------------------------------------------
# SELF-TEST 1 - official example from
# https://www.sf.gov/learn-about-rent-increases-san-francisco
# "A tenant moved in on June 1, 2023, at an initial base rent of $1,000.00 and
#  the owner wants to increase the tenant's rent for the first time on
#  June 1, 2026 ... total allowable rent increase is 4.7% (3.1% banked + 1.6%
#  annual) ... new base rent is $1,047.00"
# ---------------------------------------------------------------------------
c1 = scenario("SELF-TEST 1: Rent Board example, increase on the anniversary",
              Decimal("1000.00"), date(2023, 6, 1), date(2026, 6, 1))
print()

rentcalc.show(c1)
assert c1["banked"] == Decimal("3.1"), c1["banked"]
assert c1["current_aga"] == Decimal("1.6")
assert c1["total"] == Decimal("4.7")
assert c1["amount"] == Decimal("47.00")
assert c1["new_rent"] == Decimal("1047.00")
print("  >> MATCHES the official Rent Board worked example exactly.")

# ---------------------------------------------------------------------------
# SELF-TEST 2 - official example, same page, "WITH NEW ANNIVERSARY DATE"
# "...the owner did not 'bank' the 1.4% increase from June 1, 2025 ... The 1.4%
#  rent increase is permanently lost due to the change in anniversary date ...
#  new base rent is $1,033.00"
# ---------------------------------------------------------------------------
c2 = scenario("SELF-TEST 2: Rent Board example, changed anniversary date",
              Decimal("1000.00"), date(2023, 6, 1), date(2026, 5, 1))
print()
rentcalc.show(c2)
assert c2["banked"] == Decimal("1.7")
assert c2["total"] == Decimal("3.3")
assert c2["amount"] == Decimal("33.00")
assert c2["new_rent"] == Decimal("1033.00")
print("  >> MATCHES the official Rent Board worked example exactly.")

# ---------------------------------------------------------------------------
# SELF-TEST 3 - official example from
# https://www.sf.gov/information--banked-rent-increases
# "moved in on August 1, 2022 at an initial base rent of $1,300.00 ... first
#  increase on August 1, 2025 ... 5.3% banked (3.6% + 1.7%) ... + 1.4% annual
#  = 6.7% ... $1,300.00 x .067 = $87.10 ... new base rent is $1,387.10"
# ---------------------------------------------------------------------------
c3 = scenario("SELF-TEST 3: Rent Board banked-increase example",
              Decimal("1300.00"), date(2022, 8, 1), date(2025, 8, 1))
print()
rentcalc.show(c3)
assert c3["banked"] == Decimal("5.3")
assert c3["total"] == Decimal("6.7")
assert c3["amount"] == Decimal("87.10")
assert c3["new_rent"] == Decimal("1387.10")
print("  >> MATCHES the official Rent Board worked example exactly.")

# ---------------------------------------------------------------------------
# SELF-TEST 4 - official example from
# https://www.sf.gov/learn-about-rent-increases-san-francisco
# "A tenant moved in on June 1, 2025, at an initial base rent of $1,000.00 ...
#  increase for June 1, 2026 ... new base rent is $1,016.00"
# ---------------------------------------------------------------------------
c4 = scenario("SELF-TEST 4: Rent Board single-year example",
              Decimal("1000.00"), date(2025, 6, 1), date(2026, 6, 1))
print()
rentcalc.show(c4)
assert c4["banked"] == Decimal("0")
assert c4["total"] == Decimal("1.6")
assert c4["amount"] == Decimal("16.00")
assert c4["new_rent"] == Decimal("1016.00")
print("  >> MATCHES the official Rent Board worked example exactly.")

# ---------------------------------------------------------------------------
# UNIT A - anonymized. Base rent $3,995.00, tenancy began 2025-02-01.
# ---------------------------------------------------------------------------
A_BASE, A_ANNIV = Decimal("3995.00"), date(2025, 2, 1)
print("\n" + "#" * 78)
print("# UNIT A  (base rent $3,995.00; tenancy began 2025-02-01; anniversary Feb 1)")
print("#" * 78)

A1 = scenario("UNIT A / S1 - RECOMMENDED: increase on the anniversary date",
              A_BASE, A_ANNIV, date(2027, 2, 1))
A2 = scenario("UNIT A / S2 - earliest increase serviceable today (30-day notice)",
              A_BASE, A_ANNIV, add_days(TODAY, 30),
              "the 1.4% available 2026-02-01 has not matured -> permanently "
              "forfeited because the anniversary date changes (R4)")
for s in (A1, A2):
    print()
    rentcalc.show(s)

A3_total = Decimal("1.6")
A3_amt = money(A_BASE * A3_total / Decimal(100))
print("\nUNIT A / S3 - PARTIAL increase on the anniversary (2027-02-01)")
print("  sf.gov / Rule 4.12: a landlord does not have to impose the maximum;")
print("  any unused portion stays banked and does not expire during the tenancy.")
print(f"  impose 1.6% only      ${A3_amt:,.2f}  -> new base ${A_BASE + A3_amt:,.2f}")
print("  1.4% remains banked")
print(f"  notice 30 days -> serve on/before {sub_days(date(2027,2,1),30)} "
      f"({sub_days(date(2027,2,1),35)} if mailed)")

assert A1["total"] == Decimal("3.0") and A1["amount"] == Decimal("119.85")
assert A1["new_rent"] == Decimal("4114.85")
assert A2["total"] == Decimal("1.6") and A2["amount"] == Decimal("63.92")
assert A2["new_rent"] == Decimal("4058.92")
assert A3_amt == Decimal("63.92")

# ---------------------------------------------------------------------------
# UNIT B - anonymized. Base rent $3,150.00, tenancy began 2019-06-01.
# ---------------------------------------------------------------------------
B_BASE, B_ANNIV = Decimal("3150.00"), date(2019, 6, 1)
print("\n" + "#" * 78)
print("# UNIT B  (base rent $3,150.00; tenancy began 2019-06-01; anniversary Jun 1)")
print("#" * 78)

B1 = scenario("UNIT B / S1 - RECOMMENDED: increase on the anniversary date",
              B_BASE, B_ANNIV, date(2027, 6, 1),
              "the AGA for the period beginning 2027-03-01 is NOT YET PUBLISHED; "
              "it is added on top of the 13.1% and is left blank - never inferred")
B2 = scenario("UNIT B / S2 - earliest increase serviceable today (90-day notice)",
              B_BASE, B_ANNIV, add_days(TODAY, 90),
              "the 1.6% available 2026-06-01 has not matured -> permanently "
              "forfeited because the anniversary date changes (R4)")
for s in (B1, B2):
    print()
    rentcalc.show(s)

assert B1["banked"] == Decimal("13.1") and B1["aga_published"] is False
assert B1["amount"] == Decimal("412.65") and B1["new_rent"] == Decimal("3562.65")
assert B2["banked"] == Decimal("11.5") and B2["current_aga"] == Decimal("1.6")
assert B2["total"] == Decimal("13.1") and B2["amount"] == Decimal("412.65")
assert B2["new_rent"] == Decimal("3562.65")

# ---------------------------------------------------------------------------
# Descriptive statistics - the "what is normal" evidence base
# ---------------------------------------------------------------------------
recent = [p for s, e, p in AGA if s >= date(2019, 3, 1)]
# exclude the split 3/1/92-12/7/92 and 12/8/92-2/28/93 pair: document 571
# cautions that only ONE of those two may be imposed for that year.
allv = [p for s, e, p in AGA if s not in (date(1992, 3, 1), date(1992, 12, 8))]
sr, sa = stats(recent), stats(allv)
print("\n" + "=" * 78)
print(f"AGA 3/1/2019-3/1/2026  n={sr['n']}  mean={sr['mean']:.4f}%  "
      f"median={sr['median']}%  min={sr['min']}%  max={sr['max']}%")
print(f"AGA 4/1/1982-3/1/2026  n={sa['n']}  mean={sa['mean']:.4f}%  "
      f"median={sa['median']}%  min={sa['min']}%  max={sa['max']}%")

print("\nAB 1482 statewide cap - Cal. Civ. Code Sec. 1947.12(a)(1): 5% + CPI, max 10%")
print("  CPI-U SF-Oakland-Hayward 12-mo change, April 2026 = 3.8% (CA DIR, official)")
print("  -> cap for increases effective 8/1/2026-7/31/2027 = 5.0% + 3.8% = 8.8%")
print("  CPI-U SF-Oakland-Hayward 12-mo change, April 2025 = 1.3% (CA DIR, official)")
print("  -> cap for increases effective 8/1/2025-7/31/2026 = 5.0% + 1.3% = 6.3%")
print("  Sec. 1947.12(d)(3) EXEMPTS housing under a local ordinance with a lower cap.")
print("  SF cap 1.6% < 8.8%  ->  the AB 1482 cap does NOT govern these two units.")

out = {
    "analysis_date": TODAY.isoformat(),
    "unit_a": {
        "base": "3995.00", "anniversary": A_ANNIV.isoformat(),
        "s1": {"effective": A1["effective"].isoformat(), "banked": str(A1["banked"]),
               "current_aga": str(A1["current_aga"]), "total": str(A1["total"]),
               "amount": str(A1["amount"]), "new_rent": str(A1["new_rent"]),
               "notice_days": A1["notice_hand"][0],
               "serve_by": A1["notice_hand"][1].isoformat(),
               "serve_by_mailed": A1["notice_mail"][1].isoformat()},
        "s2": {"effective": A2["effective"].isoformat(), "banked": str(A2["banked"]),
               "current_aga": str(A2["current_aga"]), "total": str(A2["total"]),
               "amount": str(A2["amount"]), "new_rent": str(A2["new_rent"]),
               "notice_days": A2["notice_hand"][0],
               "serve_by": A2["notice_hand"][1].isoformat(),
               "serve_by_mailed": A2["notice_mail"][1].isoformat()},
        "s3": {"effective": "2027-02-01", "total": str(A3_total),
               "amount": str(A3_amt), "new_rent": str(A_BASE + A3_amt)},
    },
    "unit_b": {
        "base": "3150.00", "anniversary": B_ANNIV.isoformat(),
        "s1": {"effective": B1["effective"].isoformat(), "banked": str(B1["banked"]),
               "current_aga": None, "total_known": str(B1["total"]),
               "amount_known": str(B1["amount"]), "new_rent_known": str(B1["new_rent"]),
               "notice_days": B1["notice_hand"][0],
               "serve_by": B1["notice_hand"][1].isoformat(),
               "serve_by_mailed": B1["notice_mail"][1].isoformat(),
               "detail": [[a.isoformat(), str(p) if p is not None else None, st]
                          for a, p, st, _ in B1["rows"]]},
        "s2": {"effective": B2["effective"].isoformat(), "banked": str(B2["banked"]),
               "current_aga": str(B2["current_aga"]), "total": str(B2["total"]),
               "amount": str(B2["amount"]), "new_rent": str(B2["new_rent"]),
               "notice_days": B2["notice_hand"][0],
               "serve_by": B2["notice_hand"][1].isoformat(),
               "serve_by_mailed": B2["notice_mail"][1].isoformat(),
               "detail": [[a.isoformat(), str(p) if p is not None else None, st]
                          for a, p, st, _ in B2["rows"]]},
    },
    "stats": {"recent": {k: str(v) for k, v in sr.items()},
              "all": {k: str(v) for k, v in sa.items()}},
    "ab1482": {"cap_2025_26": "6.3%", "cap_2026_27": "8.8%",
               "cpi_apr_2025": "1.3%", "cpi_apr_2026": "3.8%",
               "applies": False},
}
with open(os.path.join(ROOT, "data", "_calc.json"), "w") as f:
    json.dump(out, f, indent=2)

print("\nALL ASSERTIONS PASSED - every published number is reproducible.")
print("Wrote data/_calc.json")
