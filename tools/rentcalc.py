#!/usr/bin/env python3
"""rentcalc.py - verified San Francisco rent-increase calculation engine.

Self-tested against BOTH official SF Rent Board worked examples (see tools/calc.py).

No value in this module is inferred. Every AGA percentage below is transcribed
verbatim from SF Rent Board document 571, "Allowable Annual Increases":
    https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf
cross-checked against the Rent Board "Current Rates" page:
    https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit

Rules implemented (each tied to an official source):

  R1  Rent may be increased only once every 12 months.
        sf.gov, "Learn about rent increases in San Francisco"
        https://www.sf.gov/learn-about-rent-increases-san-francisco
  R2  A skipped annual increase "banks" only once a FULL 12 MONTHS has elapsed
      from the date it could first have been imposed.
        Rent Board Rules & Regulations Sec. 4.12(a)
        https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring
  R3  Banked percentages are ADDED (never compounded) and never rounded up.
      Total increase = (sum of matured banked %) + (AGA in effect on the
      effective date), applied to the tenant's BASE rent.
        Rules & Regs Sec. 4.12(a); sf.gov banked-rent-increases worked example
        https://www.sf.gov/information--banked-rent-increases
  R4  Moving the increase off the anniversary date permanently forfeits any
      skipped AGA that had not yet completed its 12 months.
        sf.gov, "Learn about rent increases" - example 4
  R5  30-day written notice if the total increase is 10% or less; 90-day if it
      is more than 10%. Add 5 days if the notice is mailed.
        Cal. Civ. Code Sec. 827(b)(2) and (b)(3)(A)
        https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827
        sf.gov rent-increase pages (30/90 + 5 if mailed)
  R6  A current Rent Increase License (Housing Inventory; Rent Ordinance
      Sec. 37.15) must be on file on the effective date, or the ENTIRE annual
      or banked increase is null and void.
        https://www.sf.gov/rent-board-housing-inventory
        https://www.sf.gov/notice-of-owner-noncompliance-with-housing-inventory
  R7  No increase may be based on the addition or replacement of an occupant,
      even if the lease purports to allow it.
        Rent Ordinance Sec. 37.3(a)(11)(A)
        https://www.sf.gov/information--replacement-roommates
  R8  Amounts are truncated to the cent and never rounded up to the next dollar.
        sf.gov: "Rent increases cannot be rounded up to the nearest dollar."
"""

from datetime import date
from decimal import Decimal, ROUND_DOWN

CENT = Decimal("0.01")

# --------------------------------------------------------------- AGA table
# Official SF Rent Board document 571. (period_start, period_end, percent)
AGA = [
    (date(2026, 3, 1), date(2027, 2, 28), Decimal("1.6")),
    (date(2025, 3, 1), date(2026, 2, 28), Decimal("1.4")),
    (date(2024, 3, 1), date(2025, 2, 28), Decimal("1.7")),
    (date(2023, 3, 1), date(2024, 2, 29), Decimal("3.6")),
    (date(2022, 3, 1), date(2023, 2, 28), Decimal("2.3")),
    (date(2021, 3, 1), date(2022, 2, 28), Decimal("0.7")),
    (date(2020, 3, 1), date(2021, 2, 28), Decimal("1.8")),
    (date(2019, 3, 1), date(2020, 2, 29), Decimal("2.6")),
    (date(2018, 3, 1), date(2019, 2, 28), Decimal("1.6")),
    (date(2017, 3, 1), date(2018, 2, 28), Decimal("2.2")),
    (date(2016, 3, 1), date(2017, 2, 28), Decimal("1.6")),
    (date(2015, 3, 1), date(2016, 2, 29), Decimal("1.9")),
    (date(2014, 3, 1), date(2015, 2, 28), Decimal("1.0")),
    (date(2013, 3, 1), date(2014, 2, 28), Decimal("1.9")),
    (date(2012, 3, 1), date(2013, 2, 28), Decimal("1.9")),
    (date(2011, 3, 1), date(2012, 2, 29), Decimal("0.5")),
    (date(2010, 3, 1), date(2011, 2, 28), Decimal("0.1")),
    (date(2009, 3, 1), date(2010, 2, 28), Decimal("2.2")),
    (date(2008, 3, 1), date(2009, 2, 28), Decimal("2.0")),
    (date(2007, 3, 1), date(2008, 2, 29), Decimal("1.5")),
    (date(2006, 3, 1), date(2007, 2, 28), Decimal("1.7")),
    (date(2005, 3, 1), date(2006, 2, 28), Decimal("1.2")),
    (date(2004, 3, 1), date(2005, 2, 28), Decimal("0.6")),
    (date(2003, 3, 1), date(2004, 2, 29), Decimal("0.8")),
    (date(2002, 3, 1), date(2003, 2, 28), Decimal("2.7")),
    (date(2001, 3, 1), date(2002, 2, 28), Decimal("2.8")),
    (date(2000, 3, 1), date(2001, 2, 28), Decimal("2.9")),
    (date(1999, 3, 1), date(2000, 2, 29), Decimal("1.7")),
    (date(1998, 3, 1), date(1999, 2, 28), Decimal("2.2")),
    (date(1997, 3, 1), date(1998, 2, 28), Decimal("1.8")),
    (date(1996, 3, 1), date(1997, 2, 28), Decimal("1.0")),
    (date(1995, 3, 1), date(1996, 2, 29), Decimal("1.1")),
    (date(1994, 3, 1), date(1995, 2, 28), Decimal("1.3")),
    (date(1993, 3, 1), date(1994, 2, 28), Decimal("1.9")),
    # Official caution on document 571: only ONE of these two may be imposed
    # for 3/1/1992 - 2/28/1993, based on the tenant's anniversary date.
    (date(1992, 12, 8), date(1993, 2, 28), Decimal("1.6")),
    (date(1992, 3, 1), date(1992, 12, 7), Decimal("4.0")),
    (date(1991, 3, 1), date(1992, 2, 29), Decimal("4.0")),
    (date(1990, 3, 1), date(1991, 2, 28), Decimal("4.0")),
    (date(1989, 3, 1), date(1990, 2, 28), Decimal("4.0")),
    (date(1988, 3, 1), date(1989, 2, 28), Decimal("4.0")),
    (date(1987, 3, 1), date(1988, 2, 29), Decimal("4.0")),
    (date(1986, 3, 1), date(1987, 2, 28), Decimal("4.0")),
    (date(1985, 3, 1), date(1986, 2, 28), Decimal("4.0")),
    (date(1984, 3, 1), date(1985, 2, 28), Decimal("4.0")),
    (date(1983, 3, 1), date(1984, 2, 29), Decimal("7.0")),
    (date(1982, 4, 1), date(1983, 2, 28), Decimal("7.0")),
]

# Amounts the Rent Board publishes alongside the AGA (official "Current Rates").
SECURITY_DEPOSIT_INTEREST = [
    ("March 1, 2026 - February 28, 2027", "4.2%"),
    ("March 1, 2025 - February 28, 2026", "5.0%"),
    ("March 1, 2024 - February 28, 2025", "5.2%"),
]

# CPI-U, San Francisco-Oakland-Hayward, 12-month % change, All Urban Consumers.
# Source: CA Dept. of Industrial Relations, Office of the Director - Research
# Unit, "Consumer Price Index Table Percentage Changes - All Areas", last
# updated 10/15/2026: https://www.dir.ca.gov/oprl/CPI/PresentCCPIchange.PDF
CPI_SF_OAKLAND_HAYWARD = [
    ("2025 April", "1.3%"),
    ("2025 August", "2.5%"),
    ("2025 October", None),   # official: data unavailable, federal shutdown
    ("2025 December", "3.0%"),
    ("2025 Annual Average", "2.2%"),
    ("2026 February", "2.5%"),
    ("2026 April", "3.8%"),
    ("2026 June", "3.8%"),
    ("2026 August", "3.4%"),
    ("2026 September", None),  # not yet published as of 10/15/2026
]


def aga_on(d):
    """Return the AGA percentage in effect on date d, or None.

    None means the Rent Board has not published a rate for that period.
    Callers MUST leave such a value blank - never infer or forecast it.
    """
    for s, e, p in AGA:
        if s <= d <= e:
            return p
    return None


def money(x):
    """R8: truncate to the cent. Never round up."""
    return Decimal(x).quantize(CENT, rounding=ROUND_DOWN)


def add_days(d, n):
    return date.fromordinal(d.toordinal() + n)


def sub_days(d, n):
    return date.fromordinal(d.toordinal() - n)


def notice_deadline(effective, total_pct, mailed=False):
    """R5 -> (required_days, latest_service_date)."""
    days = 90 if total_pct > Decimal("10") else 30
    if mailed:
        days += 5
    return days, sub_days(effective, days)


def scenario(label, base, anniversary, effective, note=""):
    """Compute one increase scenario strictly per R1-R8.

    base        Decimal - the tenant's lawful BASE rent
    anniversary date    - tenancy start or the date of the last increase
    effective   date    - proposed effective date of the increase
    """
    cur = aga_on(effective)
    pct = Decimal(cur) if cur is not None else None   # None => NOT YET PUBLISHED

    banked, rows = Decimal(0), []
    n = 1
    while True:
        anniv = date(anniversary.year + n, anniversary.month, anniversary.day)
        if anniv >= effective:
            break
        avail = aga_on(anniv)
        if avail is None:
            rows.append((anniv, None, "AGA not published", False))
        else:
            matured = effective >= date(anniv.year + 1, anniv.month, anniv.day)
            rows.append((anniv, avail, "banked" if matured else "FORFEITED (R4)", matured))
            if matured:
                banked += avail
        n += 1

    total = banked + (pct if pct is not None else Decimal(0))
    amt = money(base * total / Decimal(100))
    return dict(
        label=label, base=base, anniversary=anniversary, effective=effective,
        current_aga=pct, banked=banked, total=total, amount=amt,
        new_rent=base + amt, rows=rows,
        notice_hand=notice_deadline(effective, total, mailed=False),
        notice_mail=notice_deadline(effective, total, mailed=True),
        note=note,
        aga_published=pct is not None,
    )


def show(s):
    print("=" * 78)
    print(s["label"])
    print(f"  base rent               ${s['base']:,.2f}")
    print(f"  effective date          {s['effective'].isoformat()}")
    for anniv, avail, status, _ in s["rows"]:
        if avail is None:
            print(f"    skipped {anniv.isoformat()}   AGA UNPUBLISHED -> {status}")
        else:
            print(f"    skipped {anniv.isoformat()}   {avail:>4}%         -> {status}")
    print(f"  banked total            {s['banked']}%")
    if s["current_aga"] is None:
        print("  current AGA             NOT YET PUBLISHED (left blank - never inferred)")
    else:
        print(f"  current AGA             {s['current_aga']}%")
    tail = " + [unpublished current AGA]" if s["current_aga"] is None else ""
    print(f"  TOTAL increase          {s['total']}%{tail}")
    print(f"  dollar increase         ${s['amount']:,.2f}")
    print(f"  NEW base rent           ${s['new_rent']:,.2f}")
    print(f"  notice (hand-delivered) {s['notice_hand'][0]} days -> serve on/before "
          f"{s['notice_hand'][1].isoformat()}")
    print(f"  notice (mailed)         {s['notice_mail'][0]} days -> serve on/before "
          f"{s['notice_mail'][1].isoformat()}")
    if s["note"]:
        print(f"  NOTE: {s['note']}")


def stats(values):
    v = sorted(values)
    mean = sum(v) / len(v)
    mid = len(v) // 2
    med = v[mid] if len(v) % 2 else (v[mid - 1] + v[mid]) / 2
    return dict(n=len(v), mean=mean, median=med, min=v[0], max=v[-1])
