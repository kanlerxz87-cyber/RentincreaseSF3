"""Rules, practice, reasonable-and-normal, notice, tenant review, discrimination."""
from site_layout import src, srcs, cell, page

# ------------------------------------------------------------------ laws
RATES = [
    ("3/1/26 – 2/28/27", "1.6%", True), ("3/1/25 – 2/28/26", "1.4%", False),
    ("3/1/24 – 2/28/25", "1.7%", False), ("3/1/23 – 2/29/24", "3.6%", False),
    ("3/1/22 – 2/28/23", "2.3%", False), ("3/1/21 – 2/28/22", "0.7%", False),
    ("3/1/20 – 2/28/21", "1.8%", False), ("3/1/19 – 2/29/20", "2.6%", False),
    ("3/1/18 – 2/28/19", "1.6%", False), ("3/1/17 – 2/28/18", "2.2%", False),
    ("3/1/16 – 2/28/17", "1.6%", False), ("3/1/15 – 2/29/16", "1.9%", False),
    ("3/1/14 – 2/28/15", "1.0%", False), ("3/1/13 – 2/28/14", "1.9%", False),
    ("3/1/12 – 2/29/13", "1.9%", False), ("3/1/11 – 2/29/12", "0.5%", False),
    ("3/1/10 – 2/28/11", "0.1%", False), ("3/1/09 – 2/28/10", "2.2%", False),
    ("3/1/08 – 2/28/09", "2.0%", False), ("3/1/07 – 2/29/08", "1.5%", False),
    ("3/1/06 – 2/28/07", "1.7%", False), ("3/1/05 – 2/28/06", "1.2%", False),
    ("3/1/04 – 2/29/05", "0.6%", False), ("3/1/03 – 2/29/04", "0.8%", False),
    ("3/1/02 – 2/28/03", "2.7%", False), ("3/1/01 – 2/28/02", "2.8%", False),
    ("3/1/00 – 2/29/01", "2.9%", False), ("3/1/99 – 2/29/00", "1.7%", False),
    ("3/1/98 – 2/28/99", "2.2%", False), ("3/1/97 – 2/28/98", "1.8%", False),
    ("3/1/96 – 2/29/97", "1.0%", False), ("3/1/95 – 2/28/96", "1.1%", False),
    ("3/1/94 – 2/28/95", "1.3%", False), ("3/1/93 – 2/28/94", "1.9%", False),
    ("12/8/92 – 2/28/93", "1.6%", False), ("3/1/92 – 12/7/92", "4.0%", False),
    ("3/1/91 – 2/29/92", "4.0%", False), ("3/1/90 – 2/28/91", "4.0%", False),
    ("3/1/89 – 2/28/90", "4.0%", False), ("3/1/88 – 2/28/89", "4.0%", False),
    ("3/1/87 – 2/29/88", "4.0%", False), ("3/1/86 – 2/28/87", "4.0%", False),
    ("3/1/85 – 2/28/86", "4.0%", False), ("3/1/84 – 2/29/85", "4.0%", False),
    ("3/1/83 – 2/29/84", "7.0%", False), ("4/1/82 – 2/28/83", "7.0%", False),
]


def laws():
    rows = "".join(
        '<tr><td>%s</td><td>%s%s</td>%s</tr>' % (
            period, pct, ' <span class="badge">in force now</span>' if now else "", cell("SF_571"))
        for period, pct, now in RATES
    )
    body = f"""
<div class="card">
  <h1>Rules &amp; caps — local, state and federal</h1>
  <p class="lede">What actually limits these two units, layer by layer, and the complete official rate table back to 1982.</p>
</div>

<div class="card">
  <h2>Local — San Francisco Rent Ordinance</h2>
  <table>
    <thead><tr><th style="width:23%">Rule</th><th>What it provides</th><th style="width:20%">Official source</th></tr></thead>
    <tbody>
      <tr><td>Coverage</td><td>Many residential units built on or before <b>13 June 1979</b> have both rent control and eviction protection. Exclusions include most single-family homes and condominiums, units built after that date, substantially rehabilitated units and units regulated by another agency.</td>{cell("SF_LAWS")}</tr>
      <tr><td>Annual allowance</td><td><b>1.6%</b> for 1 March 2026 – 28 February 2027; the Rent Board recalculates it each year on 1 March, based on 60% of the rise in Bay Area CPI.</td>{cell("SF_LI", "SF_571")}</tr>
      <tr><td>Frequency</td><td>Once every 12 months; the first increase may be imposed 12 months after the lease began; the effective date then becomes the tenant's anniversary date.</td>{cell("SF_LI")}</tr>
      <tr><td>Base for the calculation</td><td>Base rent only, including housing services such as parking or storage; excluding temporary passthroughs and fluctuating charges. No rounding up.</td>{cell("SF_LI")}</tr>
      <tr><td>Banking</td><td>Skipped increases may be banked subject to the Rent Board's conditions, added together (never compounded), unlimited back to 1 April 1982, non-expiring during the tenancy, transferable from a prior owner, never transferable to a new tenant.</td>{cell("SF_BANK", "SF_MULTI")}</tr>
      <tr><td>Licence precondition</td><td>A rent-increase licence must be held on the effective date of any annual or banked increase (1 March 2023 onwards for 1–9 unit buildings and condominiums). An increase taking effect while unlicensed may be <b>null and void</b> (even across multiple years) and may entitle the tenant to a refund.</td>{cell("SF_HI", "SF_NONCOMP", "ADMIN_373")}</tr>
      <tr><td>Rent Board Fee (separate)</td><td>Annual per-unit fee — <b>$59.00 per dwelling unit</b> for 2026–27, due 1 March (5% monthly late penalty up to 15%; 50% = $29.50 recoverable from tenants in occupancy as of 1 November; 2027 exemption deadline 14 December 2026). Separate from the free Housing Inventory report.</td>{cell("SF_FEE", "SF_HI")}</tr>
      <tr><td>Notice</td><td>30 days' written notice; 90 days if the increase is more than 10%; +5 days if mailed; the notice must state the dollar amount, the percentage, the effective date and which portion reflects the annual increase and/or any banked amount (§ 37.3(b)(1)); nonconforming increases are <b>null and void</b> (§ 37.3(b)(5)).</td>{cell("SF_LI", "SF_BANK", "ADMIN_373")}</tr>
      <tr><td>Additional occupants &amp; partial turnover</td><td>Under § 37.3(a)(11)(A), a landlord cannot charge more rent solely because an additional occupant joined an existing tenancy, notwithstanding any lease clause. Under § 37.3(d)(2)(B) and Rule § 6.14, unlimited market resets do <i>not</i> apply to partial occupancy changes while any original occupant remains in lawful possession (and Costa-Hawkins never applies to a co-tenant with a landlord agreement).</td>{cell("ADMIN_373", "SF_614", "SF_LI")}</tr>
      <tr><td>Ordinance subsections (§ 37.3)</td><td>Codified at Administrative Code § 37.3: <b>§ 37.3(a)(1)</b> annual CPI formula (60% of CPI, 7% formula ceiling, § 37.15 licence); <b>§ 37.3(a)(2)</b> banking since 1 Apr 1982; <b>§ 37.3(a)(8)</b> arbitration petition above annual/banked; <b>§ 37.3(a)(10)</b> voucher payment-standard rules; <b>§ 37.3(a)(11)</b> additional occupants; <b>§ 37.3(b)(1)&amp;(5)</b> written breakdown &amp; null-and-void rule; <b>§ 37.3(d)</b> Costa-Hawkins &amp; partial occupancy changes.</td>{cell("ADMIN_373")}</tr>
      <tr><td>Beyond the annual amount</td><td>Certain capital improvement, operating and maintenance, and comparable-rent increases require petitions. Utility and bond passthroughs have different petition and worksheet rules; consult the specific procedure before notice.</td>{cell("SF_LANDPET")}</tr>
      <tr><td>Pending (not law)</td><td>File #261020 would cap combined banked + capital-improvement increases at 10% per year for three years; status <b>Pending Committee Action</b>. The Rent Board's 9 Nov 2026 notice says it would apply to banked increases noticed on or after 15 Sep 2026 <i>if enacted</i>.</td>{cell("LEGISTAR_261020", "SF_LI")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>State — California</h2>
  <table>
    <thead><tr><th style="width:23%">Rule</th><th>What it provides</th><th style="width:20%">Official source</th></tr></thead>
    <tbody>
      <tr><td>Tenant Protection Act (AB 1482) cap</td><td>5% + change in cost of living, capped at 10% per 12 months; for the San Francisco area the published maximum is <b>8.8%</b> for increases starting 1 Aug 2026 – 31 Jul 2027.</td>{cell("LEG_1947", "OAG")}</tr>
      <tr><td>Does AB 1482 govern these units?</td><td><b>No.</b> The statute does not apply to housing subject to a local rent control ordinance that restricts annual increases to <i>less</i> than the state amount. San Francisco's 1.6% is less than 8.8%, so the local cap controls.</td>{cell("LEG_1947")}</tr>
      <tr><td>New tenancy</td><td>For a new tenancy in which no prior tenant remains in possession, the owner may set the initial rental rate; the cap applies to later increases.</td>{cell("LEG_1947", "LEG_1954")}</tr>
      <tr><td>Costa-Hawkins</td><td>An owner may establish the initial rental rate for a dwelling, subject to listed exceptions (including subsidised tenancies and terminations aimed at evading rent control).</td>{cell("LEG_1954")}</tr>
      <tr><td>Notice to change terms</td><td>30 days if the increase is 10% or less of the rent charged at any time in the prior 12 months (alone or combined); 90 days if more; delivery in person or by mail under CCP § 1013.</td>{cell("LEG_827")}</tr>
      <tr><td>Service by mail</td><td>Any statutory notice period is extended by <b>5 calendar days</b> when both mailing and address are in California; 10 days if either is outside California.</td>{cell("LEG_1013")}</tr>
      <tr><td>Retaliation</td><td>Retaliation after a qualifying habitability complaint is prohibited subject to statutory conditions; § 1942.5(a) addresses a 180-day period. The separate tenant-rights and organising protection in § 1942.5(d) is not limited to that window.</td>{cell("LEG_1942")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>Federal</h2>
  <table>
    <thead><tr><th style="width:23%">Rule</th><th>What it provides</th><th style="width:20%">Official source</th></tr></thead>
    <tbody>
      <tr><td>Federal fair housing</td><td>The Fair Housing Act prohibits discriminatory rental terms. Federal subsidy or program rules may impose additional restrictions; subsidy status is unverified.</td>{cell("USC_3604")}</tr>
      <tr><td>Fair Housing Act</td><td>Unlawful to discriminate in the terms, conditions or privileges of a rental because of race, colour, religion, sex, familial status, national origin or disability — which covers how a rent increase is applied.</td>{cell("USC_3604")}</tr>
      <tr><td>State fair housing overlay</td><td>FEHA is broader: it adds ancestry, marital status, source of income (including a Section 8 voucher), gender identity and expression, military status, genetic information and age, and prohibits harassment.</td>{cell("LEG_12955", "CRD")}</tr>
      <tr><td>Where complaints go</td><td>The Rent Board does <b>not</b> adjudicate harassment, discrimination or retaliation; those go to the Civil Rights Department or HUD / the courts.</td>{cell("SF_TENPET", "CRD")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>Complete allowable annual increase table, 1982 – 2027</h2>
  <p class="small">Transcribed from the Rent Board's own document 571 (the same table the Board publishes each March). Every row's source is the PDF.</p>
  <table>
    <thead><tr><th style="width:28%">Period</th><th>Allowable annual increase</th><th style="width:22%">Official source</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <p class="small">Note on 1992–93: only one of the two 1992 increases may be imposed for the period 1 March 1992 – 28 February 1993, depending on the tenant's anniversary date or date of last increase (footnote in document 571).</p>
</div>
"""
    return page("pages/laws.html", "Rules &amp; caps", body,
                "Local ordinance, California statutes and federal fair housing rules that govern these rent increases, plus the full 1982-2027 rate table.")


# ------------------------------------------------------------------ reasonable
def reasonable():
    body = f"""
<div class="card">
  <h1>Reasonable &amp; normal increases</h1>
  <p class="lede">What “reasonable” and “normal” can and cannot be measured against, using only official sources — including the parts where no official answer exists.</p>
</div>

<div class="card warn">
  <h2>The honest headline</h2>
  <p><b>No official source defines a “reasonable” or “normal” rent increase for a rent-controlled San Francisco unit.</b> There is a <i>lawful maximum</i>, which is the Rent Board percentage plus any properly banked amounts. There is no official benchmark of what owners actually charge, no ZIP-code or neighbourhood rate, and no published citywide statistic comparing corporate with individual owners. Other authorized increases or passthroughs have their own petition and worksheet rules; some do not require an approval petition.</p>
  <table>
    <thead><tr><th style="width:30%">Question</th><th>Verified answer</th><th style="width:22%">Source</th></tr></thead>
    <tbody>
      <tr><td>Is there an official definition of a “reasonable” increase?</td><td><b>No.</b> The Rent Board publishes a maximum allowable percentage and the rules for using it; it does not publish a reasonableness standard for annual increases.</td>{cell("SF_LI", "ADMIN_373")}</tr>
      <tr><td>Is there an official “normal” or average increase?</td><td><b>No published figure.</b> Left blank rather than estimated (FR-08).</td>{cell("SF_LI")}</tr>
      <tr><td>Is there a different rate for a particular ZIP code?</td><td><b>No.</b> The allowable percentage is set once per year and applies citywide; there is no ZIP-level or neighbourhood variant.</td>{cell("SF_LI", "SF_571")}</tr>
      <tr><td>What is the practical benchmark then?</td><td>The lawful ceiling itself: <b>1.6%</b> for dates through 28 February 2027, plus banked amounts. It is a ceiling, not proof an increase is typical, fair, or lawful in a particular case; notice, licence, retaliation and other rules also apply.</td>{cell("SF_571", "SF_BANK")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>The only official routes above the annual percentage</h2>
  <table>
    <thead><tr><th style="width:24%">Route</th><th>What the Rent Board requires</th><th>Fit for these units</th><th style="width:19%">Source</th></tr></thead>
    <tbody>
      <tr><td>Banked annual increases</td><td>Skipped annual percentages added together; no Rent Board approval; must be calculated correctly.</td><td><b>Conditional</b> — Unit B's 11.5% and Unit A's 1.4% are illustrations that require verified history and eligibility.</td>{cell("SF_BANK")}</tr>
      <tr><td>Capital improvement passthrough</td><td>Petition filed before the notice; documented improvement costs; tenant hardship rules apply.</td><td>Only if qualifying work was done — no such work is reported here.</td>{cell("SF_LANDPET")}</tr>
      <tr><td>Operating and maintenance increase</td><td>Petition; documented cost increases.</td><td>No cost data reported; not established here.</td>{cell("SF_LANDPET")}</tr>
      <tr><td>Comparable rents (special circumstances)</td><td>Petition showing the rent is significantly below comparable units <i>because of extraordinary circumstances</i>. “The mere fact that a long-standing tenant is paying significantly less than market rent is not considered an extraordinary circumstance.”</td><td><b>Unlikely on the reported facts</b> — Unit B's gap is described as long-standing occupancy, not an extraordinary circumstance.</td>{cell("SF_SPECIAL")}</tr>
      <tr><td>Utility, bond and similar passthroughs</td><td>Rules vary: bond passthroughs and some utilities do not require approval petitions; utility calculation worksheets must be filed before notice.</td><td>Not applicable on the facts reported.</td>{cell("SF_LANDPET")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>How to document a proposed increase for review</h2>
  <p class="small">These are documentation practices, not legal requirements. Each rests on a rule in the table beside it.</p>
  <table>
    <thead><tr><th style="width:30%">Practice</th><th>Why it helps</th><th style="width:20%">Rule it rests on</th></tr></thead>
    <tbody>
      <tr><td>Use the exact published percentage, with the calculation shown to the cent</td><td>Helps reviewers check the calculation against the allowance; it does not establish overall compliance.</td>{cell("SF_571", "SF_UNLAWFUL")}</tr>
      <tr><td>Take the annual increase every year rather than accumulating</td><td>Each skipped year adds a banking question; the 24-month / 12-month wording is not uniform across pages (FR-03).</td>{cell("SF_BANK", "SF_LI")}</tr>
      <tr><td>Serve the notice with the licence already in force</td><td>The licence is a precondition on the effective date, not the notice date.</td>{cell("SF_HI")}</tr>
      <tr><td>Apply the same method to both units, and record why the amounts differ</td><td>Differences then rest on objective facts (base rent, lease date, skipped years) rather than on the tenant.</td>{cell("LEG_12955", "USC_3604")}</tr>
      <tr><td>Keep a dated rent-history file per unit</td><td>Banked amounts must be provable; tenants may petition for a determination of lawful rent at any time.</td>{cell("SF_UNLAWFUL", "SF_BANK")}</tr>
      <tr><td>Avoid any increase within 180 days of a repair request or complaint</td><td>Retaliatory increases are separately unlawful.</td>{cell("LEG_1942")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>What this means for the two units</h2>
  <table>
    <thead><tr><th>Unit</th><th>Illustrative options — not an official normal</th><th>Conditions and limitations</th><th style="width:18%">Source</th></tr></thead>
    <tbody>
      <tr><td>Unit A</td><td><b>1.6% ($63.92)</b> is the smaller annual-only option; 3.0% ($119.85) includes a disputed banked component</td><td>For a 1 February 2027 effective date only, subject to coverage, rent history, timing, licence and notice; confirm the banked component with the Rent Board.</td>{cell("SF_571", "SF_BANK")}</tr>
      <tr><td>Unit B</td><td><b>1.6% ($50.40)</b> is the smaller annual-only option; 10.0% ($315.00) and 13.1% ($412.65) are conditional catch-up illustrations</td><td>If the complete ledger confirms six skipped years, they add to 11.5%, plus the 1.6% annual in force to 28 Feb 2027; 10% is an illustrative choice, not an official typical increase. Verify prior increases, other charges and the final proposed law; a partial unused allowance may be bankable.</td>{cell("SF_BANK", "LEGISTAR_261020")}</tr>
      <tr><td>Unit B at market rent</td><td><b>Blank</b></td><td>Market rent cannot be reached by an annual increase; the Rent Board states that a long-standing below-market rent is not itself an extraordinary circumstance, and vacancy resetting is only available in a genuinely new tenancy.</td>{cell("SF_SPECIAL", "SF_LI")}</tr>
    </tbody>
  </table>
</div>
"""
    return page("pages/reasonable.html", "Reasonable &amp; normal", body,
                "What the law treats as reasonable and normal for a San Francisco rent increase, and which benchmarks do not officially exist.")


# ------------------------------------------------------------------ practice
def practice():
    body = f"""
<div class="card">
  <h1>How increases are actually handled: corporations vs individual owners</h1>
  <p class="lede">Only what official sources say. Where no official evidence exists, the row is left blank and flagged.</p>
</div>

<div class="card">
  <h2>Large / corporate owners</h2>
  <table>
    <thead><tr><th style="width:24%">Practice</th><th>Official evidence</th><th style="width:20%">Source</th></tr></thead>
    <tbody>
      <tr><td>Setting rent at turnover</td><td>The Rent Board states there is “no limit on how much rent a landlord may first charge a tenant when renting an empty unit that is covered by rent control”; state law likewise lets an owner set the initial rate for a new tenancy where no prior tenant remains.</td>{cell("SF_LI", "LEG_1947", "LEG_1954")}</tr>
      <tr><td>Renewal pricing with shared data / algorithms</td><td>San Francisco prohibits the sale or use of “algorithmic devices” to set rents or manage occupancy for residential units (Rent Ordinance § 37.10C, effective 14 October 2024); a tenant or the City Attorney may sue.</td>{cell("SF_ALGO")}</tr>
      <tr><td>Federal antitrust exposure</td><td>The U.S. Department of Justice sued six of the largest landlords (operating more than 1.3 million units) over sharing competitively sensitive data and using common pricing algorithms, and filed a proposed consent decree with one of them.</td>{cell("DOJ_ALGO")}</tr>
      <tr><td>Whether corporate owners take the annual allowance or rely on turnover</td><td><b>Blank — no official dataset reports the frequency or size of increases by owner type.</b> Flagged (FR-09).</td>{cell("SF_LI")}</tr>
      <tr><td>Professional management of the licensing step</td><td>Housing Inventory reports require an owner <i>or</i> property-manager business contact, and changes must be updated within 30 days — the mechanism larger operators use to keep licences current.</td>{cell("SF_HI")}</tr>
    </tbody>
  </table>
  <p class="small">Practical takeaway: the well-documented corporate advantage is <b>turnover</b> — resetting to market between tenancies — plus compliance infrastructure. It is not an ability to raise an existing tenant's rent above the ordinance.</p>
</div>

<div class="card">
  <h2>Individual owners</h2>
  <table>
    <thead><tr><th style="width:24%">Practice</th><th>Official evidence</th><th style="width:20%">Source</th></tr></thead>
    <tbody>
      <tr><td>Take the annual allowance, once every 12 months</td><td>“A landlord can only increase a tenant's rent by a certain percentage once every 12 months”; no petition is required for the annual amount.</td>{cell("SF_LI", "SF_571")}</tr>
      <tr><td>Bank skipped years</td><td>Skipped increases may be saved and added later, subject to the banking conditions; no Rent Board approval, but the calculation must be right.</td>{cell("SF_BANK")}</tr>
      <tr><td>Report and licence</td><td>One free Housing Inventory report per unit per year; the licence follows automatically; no separate application.</td>{cell("SF_HI", "SF_PORTAL")}</tr>
      <tr><td>Free official help</td><td>Rent Board counsellors answer by phone on weekdays; the arbitration process for a tenant petition is designed so that no one needs an attorney.</td>{cell("SF_COUNSEL", "SF_UNLAWFUL")}</tr>
      <tr><td>Outside help for larger increases</td><td>Petition-based increases (capital improvement, operating and maintenance, comparable rents) require forms and supporting documentation; the Rent Board advises talking to a counsellor before filing a comparable-rent petition.</td>{cell("SF_LANDPET", "SF_SPECIAL")}</tr>
      <tr><td>Whether individual owners raise rent less often than corporations</td><td><b>Blank — no official data.</b> Flagged (FR-09).</td>{cell("SF_LI")}</tr>
    </tbody>
  </table>
</div>

<div class="card warn">
  <h2>Where the two converge</h2>
  <p>Both corporate managers and individual owners work from the same ceiling: the annual percentage, plus properly banked amounts, plus any petition-based passthrough. Available official sources document some operators' algorithmic pricing and turnover pricing, but do not establish what is typical for either owner group. A tenant may challenge an increase through the same free petition process.</p>
  <p class="small">Sources: {srcs("SF_LI", "SF_BANK", "SF_UNLAWFUL", "SF_ALGO")}</p>
</div>
"""
    return page("pages/practice.html", "Market practice", body,
                "Official evidence on how corporate and individual San Francisco landlords handle rent increases, with gaps flagged.")


# ------------------------------------------------------------------ notice
def notice():
    body = f"""
<div class="card">
  <h1>Notice, service &amp; reasons</h1>
  <p class="lede">Exactly what the notice must say, how it must be delivered, and which reasons are lawful — with model wording you can adapt.</p>
</div>

<div class="card">
  <h2>Required contents</h2>
  <table>
    <thead><tr><th style="width:24%">Element</th><th>Requirement</th><th style="width:20%">Official source</th></tr></thead>
    <tbody>
      <tr><td>Dollar amount of the increase</td><td>State the amount in dollars.</td>{cell("SF_LI", "SF_BANK")}</tr>
      <tr><td>Percentage</td><td>State the percentage; for banked amounts the percentages are added, not compounded.</td>{cell("SF_LI", "SF_BANK")}</tr>
      <tr><td>Effective date</td><td>State the date the increase takes effect; it becomes the new anniversary date.</td>{cell("SF_LI")}</tr>
      <tr><td>Banked breakdown</td><td>If any part is banked, state in writing the annual and banked portions and the dates underlying the banked amount. Rule § 4.12(b) specifies that omission of the banked dates does not itself make the increase null and void.</td>{cell("SF_BANK", "ADMIN_373", "SF_RULE4")}</tr>
      <tr><td>Correct rate version</td><td>Use the percentage in effect on the effective date, not the date the notice is served.</td>{cell("SF_LI")}</tr>
      <tr><td>Licence</td><td>The licence must exist, but it does not have to be attached to the notice.</td>{cell("SF_HI")}</tr>
      <tr><td>Signature / identification</td><td><b>Blank — not specified</b> in the Rent Board's published notice guidance. Flagged (FR-11).</td>{cell("SF_LI")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>Delivery and timing</h2>
  <table>
    <thead><tr><th style="width:26%">Method</th><th>Lead time</th><th style="width:22%">Official source</th></tr></thead>
    <tbody>
      <tr><td>Personal delivery, increase 10% or less</td><td>At least <b>30 days</b> before the effective date.</td>{cell("LEG_827")}</tr>
      <tr><td>Personal delivery, increase more than 10%</td><td>At least <b>90 days</b> before the effective date (alone or combined with other increases in the prior 12 months).</td>{cell("LEG_827")}</tr>
      <tr><td>Mail within California</td><td>Add <b>5 calendar days</b> to the notice period, i.e. 35 or 95 days.</td>{cell("LEG_1013", "LEG_827")}</tr>
      <tr><td>Mail outside California</td><td>Add 10 calendar days.</td>{cell("LEG_1013")}</tr>
      <tr><td>Express / overnight</td><td>Add 2 court days (statutory overnight-delivery extension).</td>{cell("LEG_1013")}</tr>
      <tr><td>Proof of service</td><td>Keep the delivery receipt or the certificate/notation of mailing; the statute requires the mailed copy to record the date and place of mailing or carry an affidavit/certificate.</td>{cell("LEG_1013")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>Model notice (adapt; verify amounts before serving)</h2>
  <div class="quote">
    <b>NOTICE OF RENT INCREASE</b><br>
    Date: [date served]<br>
    To: [Tenant name(s)], [unit]<br>
    From: [Owner name and contact for habitability issues]<br><br>
    Under San Francisco Administrative Code § 37.3 and California Civil Code § 827, your monthly base rent will increase as follows.<br><br>
    • Current base rent: $[amount]<br>
    • Amount of increase: $[amount]<br>
    • Percentage of increase: [x]% consisting of [y]% annual allowable increase (allowable rate for the period covering the effective date) and [z]% banked increase based on [list each applicable anniversary date and rate]<br>
    • New base rent: $[amount]<br>
    • Effective date: [date]<br><br>
    The increase is 10% or less / more than 10% of the rent charged during the 12 months before the effective date, so [30 / 90] days' written notice is given. [If served by mail: an additional 5 days is provided under Code of Civil Procedure § 1013.]<br><br>
    The unit's rent is controlled by the San Francisco Rent Ordinance. Signed: [Owner]
  </div>
  <p class="small">This wording follows the elements the Rent Board lists for an annual or banked increase. It is a drafting aid, not legal advice: {srcs("SF_LI", "SF_BANK", "LEG_827", "ADMIN_373", "SF_RULE4")}</p>
</div>

<div class="card">
  <h2>Reasons — what is required, permitted and prohibited</h2>
  <table>
    <thead><tr><th style="width:26%">Situation</th><th>Position</th><th style="width:22%">Official source</th></tr></thead>
    <tbody>
      <tr><td>Do I have to give a reason for an annual increase?</td><td><b>No.</b> The annual and banked increases may be imposed without a petition and without any stated justification; the notice elements are amount, percentage, date and banked part.</td>{cell("SF_LI", "SF_571")}</tr>
      <tr><td>Reasons that are lawful</td><td>The lawful allowance published by the Rent Board; recovery of previously skipped (banked) annual increases; and, separately by petition, documented capital improvements, operating and maintenance costs, or comparable-rent circumstances.</td>{cell("SF_BANK", "SF_LANDPET")}</tr>
      <tr><td>Reasons that are unlawful</td><td>Retaliation for a repair request, habitability complaint or tenant organising (with distinct statutory conditions and time rules); any difference based on a protected characteristic; charging more because an additional occupant moved in.</td>{cell("LEG_1942", "LEG_12955", "SF_LI")}</tr>
      <tr><td>“Market rent” as a reason</td><td>Not a basis for an annual increase. The Rent Board states a long-standing tenant paying less than market is not, by itself, an extraordinary circumstance justifying a comparable-rent increase.</td>{cell("SF_SPECIAL")}</tr>
      <tr><td>“My costs went up” as a reason</td><td>Only through an operating-and-maintenance petition with documentation — not as an add-on to the annual notice.</td>{cell("SF_LANDPET")}</tr>
      <tr><td>“I want both units to be the same”</td><td>Not a lawful basis in itself; equalising rents is achieved only through each unit's own lawful allowance and banking.</td>{cell("ADMIN_373", "SF_LI")}</tr>
    </tbody>
  </table>
</div>
"""
    return page("pages/notice.html", "Notice &amp; reasons", body,
                "Required notice contents, delivery deadlines including the mail extension, model wording and which reasons are lawful.")


# ------------------------------------------------------------------ review
CHECKS = [
    ("1", "Is the unit covered by the Rent Ordinance?", "The 1940 construction year and rent-control status are owner-reported. Building unit count, unit type, and exemptions require confirmation.", "SF_LAWS"),
    ("2", "Is the increase within the annual allowable percentage?", "1.6% for an effective date through 28 February 2027; the published figure, not an older year's.", "SF_571"),
    ("3", "Is the percentage the one in effect on the effective date?", "Notice served in Dec/Jan must still quote 1.6%, because the increase takes effect before 1 March 2027.", "SF_LI"),
    ("4", "Was the calculation done on base rent only?", "Exclude passthroughs and fluctuating charges; include parking/storage if part of base rent.", "SF_LI"),
    ("5", "Was anything rounded up?", "No rounding to the nearest dollar.", "SF_LI"),
    ("6", "Is the banked amount properly established?", "Each skipped year identified with its percentage; added, not compounded; the banking conditions met.", "SF_BANK"),
    ("7", "Has at least 12 months passed since the last increase or the lease start?", "Unit A: 1 Feb 2027. Unit B: any date after 1 June 2020, on the reported history.", "SF_LI"),
    ("8", "Would the increase create a new anniversary date, and is that acceptable?", "Any effective date becomes the new anniversary date; a later increase may be lost if the date shifts.", "SF_LI"),
    ("9", "Was a rent-increase licence in force on the effective date?", "Check the Rent Board Portal and keep a screenshot with the date.", "SF_HI"),
    ("10", "Was the Housing Inventory report filed for the correct year?", "Deadline 1 March each year; late filing is allowed but must precede the effective date.", "SF_HI"),
    ("11", "Is the notice period correct (30 or 90 days)?", "10% or less ⇒ 30 days; more than 10% ⇒ 90 days; +5 if mailed within California.", "LEG_827"),
    ("12", "Was service documented?", "Personal delivery receipt, or a mailed copy with the date and place of mailing / certificate of mailing.", "LEG_1013"),
    ("13", "Does the notice state amount, percentage, date and banked part?", "Unverified: no actual notice was provided. Check the annual and banked portions and dates underlying any banked amounts.", "SF_BANK"),
    ("14", "Is there any retaliation issue?", "Unknown. Review complaint and organising history, motive, timing, and statutory conditions; retaliation protections also extend beyond the 180-day provision.", "LEG_1942"),
    ("15", "Is there any protected-characteristic issue?", "The amount must not vary because of race, colour, religion, sex, familial status, national origin, disability, source of income or the other FEHA grounds.", "LEG_12955"),
    ("16", "Is the differential between the two units explainable from the file?", "Different base rents and different lease dates explain the different dollar amounts; the method is identical.", "USC_3604"),
]


def review():
    rows = "".join(
        '<tr><td><b>%s</b></td><td>%s</td><td>%s</td>%s</tr>' % (n, q, how, cell(k))
        for n, q, how, k in CHECKS
    )
    body = f"""
<div class="card">
  <h1>The tenant-lawyer stress test</h1>
  <p class="lede">Sixteen checks to help prepare for tenant-side review. They are not exhaustive, and documentation cannot guarantee that a lawyer, Rent Board or court will approve an increase.</p>
</div>

<div class="card">
  <h2>How a tenant can challenge an increase</h2>
  <p>A San Francisco tenant can challenge any increase by filing a Tenant Petition (Form 516C, box C) asking the Rent Board to find the increase unlawful or to determine the lawful rent. Filing is free, there is no filing deadline, and the matter can proceed to an arbitration hearing before a Rent Board Administrative Law Judge; the process is designed so that no one needs an attorney. Separately, discrimination and retaliation claims go to the Civil Rights Department, HUD or court rather than the Rent Board.</p>
  <p class="small">Sources: {srcs("SF_UNLAWFUL", "SF_TENPET", "CRD")}</p>
</div>

<div class="card">
  <h2>The sixteen checks</h2>
  <table>
    <thead><tr><th style="width:5%">#</th><th style="width:34%">What the reviewer asks</th><th>How this file answers it</th><th style="width:19%">Rule</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>

<div class="card ok">
  <h2>Illustrative calculations — not a compliance determination</h2>
  <table>
    <thead><tr><th>Unit and option</th><th>Calculation only</th><th>Key checks still to be confirmed</th><th style="width:18%">Source</th></tr></thead>
    <tbody>
      <tr><td>Unit A, 3.0% on 1 Feb 2027</td><td>3.0% of $3,995 = $119.85</td><td>Actual rent history, anniversary, coverage, licence, service, any complaints, and motive</td>{cell("SF_HI", "SF_LI")}</tr>
      <tr><td>Unit B, 10.0%</td><td>10% of $3,150 = $315.00</td><td>Actual rent history, coverage, licence, service, any complaints, motive and legislation</td>{cell("SF_BANK", "SF_HI")}</tr>
      <tr><td>Unit B, 13.1%</td><td>13.1% of $3,150 = $412.65</td><td>All checks above, and the pending File #261020 proposal; its proposed application depends on the notice date</td>{cell("SF_BANK", "LEGISTAR_261020")}</tr>
    </tbody>
  </table>
  <p class="small">Arithmetic alone does not verify the lease, notice, service, motive or other facts. Open questions are on the <a href="flagged.html">Flagged</a> page.</p>
</div>

<div class="card">
  <h2>What would actually get an increase overturned</h2>
  <table>
    <thead><tr><th style="width:30%">Failure mode</th><th>Consequence</th><th style="width:20%">Source</th></tr></thead>
    <tbody>
      <tr><td>No licence on the effective date</td><td>The notice is not enforceable, may be null and void (potentially across multiple years), and exposes the owner to a Tenant Summary Petition (Form 518) before the effective date or an Unlawful Rent Increase Petition / refund claim (Form 516C) after.</td>{cell("SF_HI", "SF_NONCOMP", "ADMIN_373")}</tr>
      <tr><td>Percentage above the allowance (or banked amount wrongly computed)</td><td>Unlawful rent increase; the lawful rent can be determined and overpayments addressed in the petition process.</td>{cell("SF_UNLAWFUL")}</tr>
      <tr><td>Too little notice</td><td>The increase cannot take effect on the stated date; the notice is defective for that date.</td>{cell("LEG_827")}</tr>
      <tr><td>Retaliatory increase following a repair request or complaint</td><td>California law prohibits retaliation subject to statutory conditions; timing alone does not establish motive, and protection can extend beyond 180 days. Seek legal advice.</td>{cell("LEG_1942")}</tr>
      <tr><td>Increase that varies by protected characteristic</td><td>Fair-housing complaint at the Civil Rights Department, HUD or court.</td>{cell("LEG_12955", "CRD")}</tr>
      <tr><td>Extra charge because an occupant joined</td><td>Unlawful rent increase.</td>{cell("SF_LI")}</tr>
      <tr><td>Notice that is defective on its face (wrong amount, percentage, date or notice period)</td><td>The Rent Board lists a <b>Tenant Summary Petition based on receipt of an invalid notice of rent increase</b> among the claims a tenant can file, in addition to the standard unlawful-rent-increase petition. Both are free.</td>{cell("SF_TENPET")}</tr>
    </tbody>
  </table>
</div>
"""
    return page("pages/review.html", "Tenant-lawyer test", body,
                "Sixteen-point stress test a San Francisco tenant-side reviewer would apply to a rent increase notice.")


# ------------------------------------------------------------------ discrimination
def discrimination():
    body = f"""
<div class="card">
  <h1>One unit or both units?</h1>
  <p class="lede">The discrimination question, answered from the statutes and the enforcement routes — and separated from what the Rent Board does and does not decide.</p>
</div>

<div class="card hero">
  <h2>Answer</h2>
  <p><b>There is no legal requirement to raise rent on both units, and no official guidance says a selective increase is unlawful in itself.</b> What the law prohibits is treating a tenant differently <i>because of</i> a protected characteristic, or increasing rent as retaliation. The two units have different reported starting rents and lease dates; their complete histories and lawful maxima are unverified — so neither identical percentages nor identical dollar amounts are automatically required; no official data establishes what is normal. The control that matters is a written, dated, objective rationale per unit, applied consistently.</p>
</div>

<div class="card">
  <h2>The rules that actually apply</h2>
  <table>
    <thead><tr><th style="width:26%">Rule</th><th>What it prohibits or permits</th><th style="width:21%">Official source</th></tr></thead>
    <tbody>
      <tr><td>FEHA — Gov. Code § 12955(a)</td><td>Unlawful for an owner to discriminate against or harass a person because of race, colour, religion, sex, gender, gender identity or expression, sexual orientation, marital status, national origin, ancestry, familial status, <b>source of income</b>, disability, veteran or military status, or genetic information.</td>{cell("LEG_12955")}</tr>
      <tr><td>Federal Fair Housing Act — 42 U.S.C. § 3604(b)</td><td>Unlawful to discriminate “in the terms, conditions, or privileges of sale or rental of a dwelling” because of race, colour, religion, sex, familial status, national origin or disability.</td>{cell("USC_3604")}</tr>
      <tr><td>FEHA coverage and remedies</td><td>Applies to landlords, management companies and screening firms; covers refusal to rent, discriminatory terms, and retaliation; complaints go to the Civil Rights Department.</td>{cell("CRD")}</tr>
      <tr><td>Retaliation — Civ. Code § 1942.5</td><td>Prohibits retaliatory increases in specified circumstances, including certain habitability complaints in the 180-day provision; the separate organising and tenant-rights provision is not limited to that period.</td>{cell("LEG_1942")}</tr>
      <tr><td>Rent Board jurisdiction</td><td>The Rent Board decides rent-amount issues; it states that it does <b>not</b> adjudicate harassment, discrimination or retaliation.</td>{cell("SF_TENPET")}</tr>
      <tr><td>Is a uniform increase required?</td><td><b>No official source imposes one.</b> Nothing in the ordinance or the fair-housing statutes requires identical treatment of different tenancies, and nothing forbids different lawful maximums. Flagged as an absence of authority rather than a rule (FR-12).</td>{cell("ADMIN_373", "LEG_12955")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>Risk comparison for this file</h2>
  <table>
    <thead><tr><th style="width:22%">Approach</th><th>Exposure</th><th>What an enforcer would look for</th><th style="width:19%">Source</th></tr></thead>
    <tbody>
      <tr><td>Raise both units at their own lawful maximum</td><td><b>Lowest.</b> Both increases rest on the same public method and the same licence.</td><td>Only whether each calculation and notice is correct.</td>{cell("SF_LI", "SF_BANK")}</tr>
      <tr><td>Raise only Unit A or only Unit B</td><td><b>Low, if documented.</b> Selective timing is lawful where the reason is objective (lease anniversary, skipped years, licence timing).</td><td>Whether the excluded tenant shares a protected characteristic with the included one, or had recently complained about conditions.</td>{cell("LEG_12955", "LEG_1942")}</tr>
      <tr><td>Raise one unit above its lawful maximum to “catch up”</td><td><b>High.</b> That is an unlawful increase regardless of the other unit.</td><td>Whether the percentage exceeds the published allowance or a banking condition fails.</td>{cell("SF_UNLAWFUL")}</tr>
      <tr><td>Raise rent after a repair request or habitability complaint</td><td><b>Potentially high.</b> Timing warrants scrutiny; retaliatory purpose and statutory conditions matter, including outside 180 days.</td><td>The dates of any repair request, complaint or inspection relative to the increase.</td>{cell("LEG_1942")}</tr>
      <tr><td>Explain a difference by “market rent”</td><td><b>Not a defence.</b> The Rent Board expressly treats a long-standing below-market rent as insufficient for a comparable-rent increase.</td><td>Whether the file relies on market comparisons instead of the published allowance.</td>{cell("SF_SPECIAL")}</tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h2>Documentation protocol (recommended, not a legal requirement)</h2>
  <ol class="steps">
    <li><b>Write one page per unit.</b> Lease start, base rent, every increase or skip, the licence status on the planned effective date, and the arithmetic.</li>
    <li><b>Use one method for both.</b> Same notice template, same source (Form 571), same calculation sheet, whatever the amount.</li>
    <li><b>Record the objective reason for the date.</b> “Anniversary falls on 1 February 2027” and “six skipped annual increases 2020–2025” are objective; “the tenant is difficult” is not.</li>
    <li><b>Check the 180-day window.</b> Search the maintenance log and any complaints before setting an effective date.</li>
    <li><b>Keep the licence evidence.</b> Screenshot of the Portal showing the licence current on the effective date.</li>
    <li><b>If either tenant asks why the other's increase differs,</b> answer with the calculation sheet — base rent and skipped years, not the tenant.</li>
  </ol>
  <p class="small">Basis: {srcs("SF_LI", "SF_BANK", "SF_HI", "LEG_1942", "LEG_12955")}</p>
</div>
"""
    return page("pages/discrimination.html", "One unit or both?", body,
                "Fair-housing analysis of raising rent on one unit versus both units, with the statutes and enforcement routes.")
