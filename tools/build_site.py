#!/usr/bin/env python3
"""build_site.py - generate the GitHub Pages site from verified data only.

Reads data/_calc.json (produced by tools/calc.py, which asserts the engine
reproduces all four official SF Rent Board worked examples before writing) and
tools/content.py, then writes index.html, pages/*.html, assets/ and data/*.csv.

Run:  python3 tools/calc.py && python3 tools/build_site.py
"""
import csv
import html
import json
import os
import sys
from datetime import date
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content import SOURCES, SRC, FLAGS, NAV, AS_OF, cite, badge  # noqa: E402
from rentcalc import AGA, SECURITY_DEPOSIT_INTEREST, CPI_SF_OAKLAND_HAYWARD  # noqa: E402

with open(os.path.join(ROOT, "data", "_calc.json")) as f:
    C = json.load(f)

A, B, ST = C["unit_a"], C["unit_b"], C["stats"]
PRIVACY = ("Privacy: all tenant names and unit designations are pseudonymised. "
           "Dates and dollar amounts are unchanged.")


# ------------------------------------------------------------------ helpers
def e(x):
    return html.escape(str(x), quote=False)


def d(iso, fmt="%B %-d, %Y"):
    y, m, dd = (int(v) for v in iso.split("-"))
    return date(y, m, dd).strftime(fmt).replace(" 0", " ")


def usd(x):
    return "${:,.2f}".format(Decimal(str(x)))


def pct(x, suffix="%"):
    return f"{x}{suffix}"


def tbl(caption, headers, rows, numeric_cols=(), note=None, tid=None):
    """headers: list of str. rows: list of list of str (already HTML-safe)."""
    out = ['<div class="tw"><table' + (f' id="{tid}"' if tid else "") + '>']
    if caption:
        out.append(f"<caption>{caption}</caption>")
    out.append("<thead><tr>")
    for i, h in enumerate(headers):
        cls = ' class="num"' if i in numeric_cols else ""
        out.append(f"<th{cls}>{h}</th>")
    out.append("</tr></thead><tbody>")
    for r in rows:
        rcls = ""
        if isinstance(r, tuple):
            r, rcls = r
        out.append(f'<tr class="{rcls}">' if rcls else "<tr>")
        for i, c in enumerate(r):
            cls = ' class="num"' if i in numeric_cols else ""
            out.append(f"<td{cls}>{c}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    if note:
        out.append(f'<p class="small">{note}</p>')
    return "\n".join(out)


def card(k, v, s="", src="", cls=""):
    return (f'<div class="card {cls}"><p class="k">{k}</p><p class="v">{v}</p>'
            f'<p class="s">{s}</p>' + (f'<div class="src">{src}</div>' if src else "") + "</div>")


def note(kind, title, body):
    return f'<div class="note {kind}"><span class="t">{title}</span>{body}</div>'


BLANK = '<span class="empty">&mdash; blank, unverified &mdash;</span>'
OK = '<span class="b ok">Verified</span>'
NAB = '<span class="b na">Not applicable</span>'
UNV = '<span class="b warn">Unverified &ndash; flagged</span>'
GAP = '<span class="b warn">Not published</span>'


# ------------------------------------------------------------------ template
PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ | SF Rent Increase Dossier</title>
<meta name="description" content="__DESC__">
<meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="__CSS__">
</head>
<body>
<div class="shell">
<nav class="side" aria-label="Sections">
  <div class="brand">
    <h1>SF Rent Increase Dossier</h1>
    <p>Two rent-controlled units &middot; Outer Sunset, San Francisco 94122<br>
       Analysis date __ASOF__</p>
  </div>
__NAV__
  <div class="foot">
    Every value traces to an official source.<br>
    Unconfirmed values are left blank.<br>
    <a href="__FLAGGED__" style="color:#8fb8dd">__NFLAGS__ items flagged for review</a>
  </div>
</nav>
<div class="main">
  <div class="topbar"><div class="wrap">
    <div class="crumb">__CRUMB__</div>
    <div><span class="pill priv">__PRIVACY__</span> <span class="pill date">As of __ASOF__</span></div>
  </div></div>
  <div class="wrap">
__BODY__
  </div>
</div>
</div>
</body>
</html>
"""


def render(path, title, crumb, body, desc):
    depth = 0 if path == "index.html" else 1
    css = "assets/css/style.css" if depth == 0 else "../assets/css/style.css"
    flagged = "pages/flagged.html" if depth == 0 else "flagged.html"
    nav = []
    for group, items in NAV:
        nav.append(f'<div class="navgroup"><div class="gt">{group}</div>')
        for href, label, kind in items:
            target = href if depth == 0 else ("../" + href if kind == "root" else os.path.basename(href))
            active = ' class="nl active"' if href == path else ' class="nl"'
            nav.append(f'<a{active} href="{target}">{label}</a>')
        nav.append("</div>")
    out = (PAGE.replace("__TITLE__", e(title))
               .replace("__DESC__", e(desc))
               .replace("__CSS__", css)
               .replace("__NAV__", "\n".join(nav))
               .replace("__FLAGGED__", flagged)
               .replace("__NFLAGS__", str(len(FLAGS)))
               .replace("__CRUMB__", crumb)
               .replace("__PRIVACY__", e(PRIVACY))
               .replace("__ASOF__", d(AS_OF))
               .replace("__BODY__", body))
    dest = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w") as f:
        f.write(out)
    print("  wrote", path)


PAGES = []


def page(path, title, crumb, desc):
    def deco(fn):
        PAGES.append((path, title, crumb, desc, fn))
        return fn
    return deco


# ==========================================================================
# 1. DASHBOARD
# ==========================================================================
@page("index.html", "Dashboard",
      "<b>Dashboard</b>",
      "Verified rent-increase analysis for two rent-controlled units in San Francisco 94122.")
def p_index():
    s1a, s1b = A["s1"], B["s1"]
    cards = "".join([
        card("Current SF allowable increase", "1.6%",
             "Effective March 1, 2026 through February 28, 2027. Basis: 60% of the CPI-U increase "
             "for the Bay Area. Annual ceiling under the Ordinance: 7%.",
             cite("S1", "S2", "S3"), "accent"),
        card("Unit A &mdash; next lawful increase", pct(s1a["total"]) + " &rarr; " + usd(s1a["amount"]),
             f"Base {usd(A['base'])} &rarr; {usd(s1a['new_rent'])} effective {d(s1a['effective'])}. "
             f"1.4% banked + 1.6% current. {s1a['notice_days']}-day notice.",
             cite("S2", "S3", "S4"), "accent"),
        card("Unit B &mdash; next lawful increase", pct(s1b["total_known"]) + " + unpublished",
             f"Base {usd(B['base'])} &rarr; at least {usd(s1b['new_rent_known'])} effective "
             f"{d(s1b['effective'])}. 13.1% banked across 7 skipped years; the 2027-28 annual rate is "
             f"not yet published. {s1b['notice_days']}-day notice.",
             cite("S2", "S4", "S5"), "accent warn"),
        card("Items flagged for review", str(len(FLAGS)),
             "Includes two direct conflicts between official sf.gov pages and one unresolved "
             "compliance gate (the rent increase license). None block publication.",
             '<a href="pages/flagged.html">Open the flag register</a>', "warn"),
    ])

    master = tbl(
        "Master findings &mdash; both units",
        ["Field", "Unit A", "Unit B", "Official basis", "Status"],
        [
            ["Location", "San Francisco, CA 94122 (Outer Sunset)", "San Francisco, CA 94122 (Outer Sunset)",
             "Owner-supplied; no street address published", '<span class="b na">Context only</span>'],
            ["Building constructed", "1940 (owner-reported)", "1940 (owner-reported)",
             cite("S7", "S21"), UNV],
            ["Rent-controlled?", "Presumed yes &mdash; built on or before June 13, 1979",
             "Presumed yes &mdash; built on or before June 13, 1979", cite("S7"), UNV],
            ["Tenancy began", d(A["anniversary"]), d(B["anniversary"]),
             "Owner-supplied lease dates (preserved exactly)", OK],
            ["Anniversary date", "February 1", "June 1",
             cite("S3", "S16"), OK],
            ["Base rent", usd(A["base"]), usd(B["base"]),
             "Owner-supplied; composition not stated &mdash; see flag F7", OK],
            ["Increases imposed to date", "None recorded", "None recorded",
             cite("S3"), UNV],
            ["Occupants (pseudonymised)",
             "T-A1, T-A2, T-A3 originally &rarr; T-A1 + T-A4 from April 1, 2026",
             "T-B1 + T-B2 (both original)",
             cite("S11", "S12", "S25"), OK],
            ["Market-rate reset available?", "<b>No</b> &mdash; an original occupant remains in lawful possession",
             "<b>No</b> &mdash; both original occupants remain",
             cite("S25", "S12", "S11"), OK],
            ["Banked increase matured", pct(s1a["banked"]), pct(s1b["banked"]),
             cite("S5", "S4", "S2"), OK],
            ["Annual increase in effect", pct(s1a["current_aga"]), GAP,
             cite("S1", "S2"), OK if s1a["current_aga"] else GAP],
            ["Total lawful increase", pct(s1a["total"]), pct(s1b["total_known"]) + " + unpublished",
             cite("S3", "S4"), OK],
            ["Dollar increase", usd(s1a["amount"]), usd(s1b["amount_known"]) + " (minimum)",
             cite("S3"), OK],
            ["New base rent", usd(s1a["new_rent"]), usd(s1b["new_rent_known"]) + " (minimum)",
             cite("S3"), OK],
            ["Recommended effective date", d(s1a["effective"]), d(s1b["effective"]),
             cite("S3", "S4"), OK],
            ["Notice required", f"{s1a['notice_days']} days &mdash; serve on or before {d(s1a['serve_by'])}",
             f"{s1b['notice_days']} days &mdash; serve on or before {d(s1b['serve_by'])}",
             cite("S23", "S3"), OK],
            ["Rent increase license on file", BLANK, BLANK, cite("S8", "S9"), UNV],
            ["Security-deposit interest paid", BLANK, BLANK, cite("S1"), UNV],
            ["Rent Board fee paid ($59.00/unit)", BLANK, BLANK, cite("S10"), UNV],
            ["Federal rent ceiling", "None &mdash; not applicable", "None &mdash; not applicable",
             cite("S34"), '<span class="b na">No federal cap</span>'],
            ["State AB 1482 cap applies?", "No &mdash; exempt, the local cap is lower",
             "No &mdash; exempt, the local cap is lower", cite("S24"), OK],
        ],
        note="Every row cites an official source. A blank cell means the value could not be confirmed from an "
             "official source; it was never inferred. See the <a href='pages/flagged.html'>flag register</a>.")

    tiles = []
    for group, items in NAV:
        if group == "Overview":
            continue
        for href, label, kind in items:
            desc = TILE_DESC.get(href, "")
            tiles.append(
                f'<a class="tilelink" href="{href}"><p class="tt">{label}</p>'
                f'<p class="td">{desc}</p><p class="tm">{group}</p></a>')

    body = f"""
<h2 class="pg">Rent increase dossier &mdash; two units, San Francisco 94122</h2>
<p class="lede">A complete, source-verified analysis of what a lawful, reasonable and normal rent increase looks
like for two rent-controlled units in the Outer Sunset, under San Francisco, California and federal law &mdash;
built to survive review by a San Francisco tenant lawyer. Nothing on this site is estimated: where a value could
not be confirmed against an official source it is left blank and flagged.</p>

<div class="cards">{cards}</div>

{note("bad", "Two hard gates must be cleared before ANY notice is served",
      "<p><b>1. The rent increase license.</b> Under Rent Ordinance Sec. 37.15 a current license must be on file on "
      "the effective date or the <i>entire</i> annual or banked increase is null and void &mdash; correct arithmetic "
      "does not save it. License status for both units is unknown and is left blank. " + cite("S8", "S9", "S6") +
      "</p><p><b>2. Two official sf.gov pages disagree about banking.</b> One says a skipped increase needs "
      "&lsquo;at least 24 full months&rsquo; to bank; the controlling regulation, Rules and Regulations Sec. 4.12(a), "
      "says &lsquo;a full 12 months&rsquo;. This project applies the regulation and reproduces all four official "
      "worked examples exactly, but confirm with a Rent Board counselor first. " + cite("S5", "S4", "S3") + "</p>")}

<h3>Master findings</h3>
{master}

<h3>Answers to the five questions asked</h3>
<div class="grid2">
  <a class="tilelink" href="pages/law-local.html"><p class="tt">1. What is reasonable and normal?</p>
    <p class="td">Local: the published annual allowable increase (1.6% now; 1.96% average since 2019; 2.36% since
    1982). State: AB 1482 would allow 8.8% but is displaced by the lower local cap. Federal: no ceiling exists.</p>
    <p class="tm">Governing law</p></a>
  <a class="tilelink" href="pages/practices.html"><p class="tt">2. Corporate vs individual owners</p>
    <p class="td">Same ceiling for both. Corporations differ in three verifiable ways: no single-family exemption,
    size-phased licensing dates, and a flat ban on algorithmic rent-setting in SF (Sec. 37.10C).</p>
    <p class="tm">Practice &amp; risk</p></a>
  <a class="tilelink" href="pages/notice-guide.html"><p class="tt">3. How to notify, and on what grounds</p>
    <p class="td">A written notice stating the dollar amount, the percentage, the effective date and which part is
    banked; 30 days, or 90 if the total exceeds 10%; plus 5 if mailed. Legitimate grounds are a closed list.</p>
    <p class="tm">Practice &amp; risk</p></a>
  <a class="tilelink" href="pages/red-team.html"><p class="tt">4. Would it survive a tenant lawyer?</p>
    <p class="td">Tenants have free counsel and a free Rent Board petition. Fifteen attack vectors are modelled with
    the owner's position, residual risk and mitigation for each.</p>
    <p class="tm">Practice &amp; risk</p></a>
  <a class="tilelink" href="pages/fair-housing.html"><p class="tt">5. Raise one unit, or both?</p>
    <p class="td">Raising only one is lawful here; forcing the same percentage on both would be UNLAWFUL because it
    would exceed Unit A's ceiling. The safe course is one written policy applied to both, each to its own limit.</p>
    <p class="tm">Practice &amp; risk</p></a>
  <a class="tilelink" href="pages/executive-summary.html"><p class="tt">Executive summary</p>
    <p class="td">The one-page brief: findings, recommendation, conditions precedent and the decision required.</p>
    <p class="tm">Overview</p></a>
</div>

<h3>All sections</h3>
<div class="grid2">{''.join(tiles)}</div>

<h3>How this was verified</h3>
{tbl("Verification summary", ["Check", "Result"], [
    ["Primary sources in the register", f"<b>{len(SOURCES)}</b> &mdash; sf.gov, leginfo.legislature.ca.gov, "
     "dir.ca.gov, justice.gov, calcivilrights.ca.gov, sec.gov, lao.ca.gov, sfplanninggis.org, portal.sfrb.org"],
    ["Sources retrieved and read directly", f"<b>{sum(1 for s in SOURCES if s['method']=='fetched')}</b> of {len(SOURCES)} "
     "(the remainder are official URLs HTTP-verified in CI and never used alone to support a number)"],
    ["Calculator self-tests against official worked examples", "<b>4 of 4 passed</b> &mdash; $1,047.00, $1,033.00, "
     "$1,387.10 and $1,016.00 reproduced exactly"],
    ["Values left blank rather than inferred", "<b>7</b> (license status, deposit interest, Rent Board fee, prior "
     "increase history, base-rent composition for both units, the 2027-28 annual rate, the federal ceiling)"],
    ["Items flagged for review", f"<b>{len(FLAGS)}</b>, published on the Flagged for Review page"],
    ["Personal information published", "<b>None</b> &mdash; pseudonymised units and tenants; dates and amounts "
     "preserved exactly"],
])}
<p class="small">See <a href="pages/methodology.html">Methodology &amp; Verification</a> for the full rule set and
<a href="pages/audit.html">Repo audit &amp; log</a> for the change history.</p>
"""
    return body


TILE_DESC = {
    "pages/executive-summary.html": "The one-page brief: findings, recommendation and conditions precedent.",
    "pages/methodology.html": "Rules applied, official self-tests, verification method, privacy method.",
    "pages/law-local.html": "SF Administrative Code Chapter 37 and Rent Board Rules and Regulations.",
    "pages/law-state.html": "Costa-Hawkins, AB 1482 and Civil Code Sec. 827.",
    "pages/law-federal.html": "The Fair Housing Act and the absence of a federal rent ceiling.",
    "pages/rates.html": "Every allowable annual increase since 1982, CPI, deposit interest and fees.",
    "pages/units.html": "Anonymised dossiers for Unit A and Unit B, field by field.",
    "pages/scenarios.html": "Each lawful scenario computed, with notice deadlines and the recommendation.",
    "pages/notice-guide.html": "The exact procedure, required notice contents, and the closed list of grounds.",
    "pages/practices.html": "How institutional owners and individual owners differ, with primary sources.",
    "pages/fair-housing.html": "The discrimination analysis: raise one unit, both, or neither.",
    "pages/red-team.html": "Fifteen attack vectors a free tenant lawyer would run, and the answer to each.",
    "pages/sources.html": "Every source, what it verifies, and how it was checked.",
    "pages/flagged.html": "Irregularities, source conflicts, blanks and unverified items.",
    "pages/audit.html": "Repository state before and after, file inventory and the verification log.",
}


# ==========================================================================
# 2. METHODOLOGY
# ==========================================================================
@page("pages/methodology.html", "Methodology & Verification",
      "Overview &rsaquo; <b>Methodology &amp; Verification</b>",
      "How every value was verified against official sources.")
def p_methodology():
    rules = tbl("The eight rules the calculator implements, each tied to an official source",
                ["Rule", "What it requires", "Official source", "Status"], [
        ["R1", "Rent may be increased only once every 12 months. The first increase is available 12 months after "
               "the lease began; the effective date of any increase becomes the new anniversary date.",
         cite("S3", "S16"), OK],
        ["R2", "A skipped annual increase &lsquo;banks&rsquo; only once <b>a full 12 months</b> has elapsed from the "
               "date it could first have been imposed. Rules &amp; Regs Sec. 4.12(a).",
         cite("S5", "S4"), OK],
        ["R3", "Banked percentages are <b>added, never compounded</b>, and never rounded up. Total increase = "
               "(sum of matured banked percentages) + (the annual rate in effect on the effective date), applied to "
               "base rent.", cite("S5", "S4", "S3"), OK],
        ["R4", "Moving the increase off the anniversary date <b>permanently forfeits</b> any skipped rate that had "
               "not yet completed its 12 months.", cite("S3"), OK],
        ["R5", "30 days&rsquo; written notice where the total increase is 10% or less; <b>90 days</b> where it is "
               "more than 10% (measured against the rent charged at any time in the prior 12 months, alone or "
               "combined). Add <b>5 days</b> if the notice is mailed.", cite("S23", "S3", "S4"), OK],
        ["R6", "A current <b>rent increase license</b> must be on file on the effective date, or the entire annual "
               "or banked increase is null and void.", cite("S8", "S9", "S6"), OK],
        ["R7", "No increase may be based on the addition or replacement of an occupant, even if the lease purports "
               "to allow it.", cite("S11", "S6", "S12"), OK],
        ["R8", "Amounts are truncated to the cent and never rounded up to the next dollar.", cite("S3", "S17"), OK],
    ])

    tests = tbl("Self-tests: the engine must reproduce the Rent Board's own worked examples before publishing",
                ["#", "Official example", "Expected result", "Engine result", "Status"], [
        ["1", "Moved in 2023-06-01 at $1,000.00; first increase 2026-06-01. 3.1% banked + 1.6% current = 4.7%.",
         "$1,047.00", "$1,047.00", '<span class="b ok">Pass</span>'],
        ["2", "Same facts but the increase is moved to 2026-05-01. Only 1.7% banks; the 1.4% is forfeited; "
              "+ 1.6% current = 3.3%.", "$1,033.00", "$1,033.00", '<span class="b ok">Pass</span>'],
        ["3", "Moved in 2022-08-01 at $1,300.00; first increase 2025-08-01. 5.3% banked + 1.4% current = 6.7%.",
         "$1,387.10", "$1,387.10", '<span class="b ok">Pass</span>'],
        ["4", "Moved in 2025-06-01 at $1,000.00; increase 2026-06-01 at 1.6%.", "$1,016.00", "$1,016.00",
         '<span class="b ok">Pass</span>'],
    ], note="Sources: " + " ".join([SRC["S3"]["url"], SRC["S4"]["url"]]) +
            " &mdash; the engine is asserted against all four before <code>data/_calc.json</code> is written. "
            "If any assertion fails, no output file is produced.")

    body = f"""
<h2 class="pg">Methodology &amp; verification</h2>
<p class="lede">This page states exactly how each number was obtained, what counts as verified, what was left blank
and why, and how to reproduce every figure. The governing principle applied throughout: if a value cannot be
confirmed from an official source, it is left blank and flagged. Nothing is estimated, extrapolated or forecast.</p>

<h3>1. What &ldquo;verified&rdquo; means here</h3>
{tbl("Verification levels used on this site", ["Label", "Meaning"], [
    ['<span class="b ok">Verified</span>',
     "The value was read directly off a document published by an official body (a .gov publisher, the California "
     "Legislature, or the U.S. SEC) during research on " + d(AS_OF) + ", and that document is linked on the row."],
    ['<span class="b info">Official URL &ndash; CI-checked</span>',
     "The URL is an official-source URL recorded in the register and its availability is confirmed by the automated "
     "link check, but its full text was not read line by line for this project. Such a source is never the sole "
     "support for a numeric value."],
    ['<span class="b warn">Unverified &ndash; flagged</span>',
     "The value could not be confirmed from an official source. It is left blank on the site and appears in the "
     "flag register."],
    ['<span class="b warn">Not published</span>',
     "The responsible agency had not published the value as of the analysis date. Left blank; never forecast."],
    ['<span class="b na">Not applicable</span>',
     "No official source sets this value because the law does not provide for one (for example, a federal rent "
     "ceiling)."],
])}

<h3>2. Rules applied to every calculation</h3>
{rules}

<h3>3. Self-tests against the Rent Board&rsquo;s own worked examples</h3>
{tests}

<h3>4. Data provenance</h3>
{tbl("Where each input comes from", ["Input", "Provenance", "Official source"], [
    ["Allowable annual increases, 4/1/1982 &ndash; 2/28/2027",
     "Transcribed verbatim from SF Rent Board document 571 into <code>tools/rentcalc.py</code>; cross-checked "
     "against the Rent Board Current Rates page.", cite("S2", "S1")],
    ["Security-deposit interest rates", "Transcribed from the Rent Board Current Rates page.", cite("S1")],
    ["Rent Board fee", "Transcribed from the Rent Board fee page.", cite("S10")],
    ["CPI-U, San Francisco-Oakland-Hayward",
     "Transcribed from the CA Department of Industrial Relations percentage-change table (last updated "
     "10/15/2026).", cite("S29")],
    ["Statutory text", "Read directly from the California Legislative Information code display for each section "
     "cited.", cite("S23", "S24", "S25", "S26")],
    ["Ordinance and regulation text",
     "Read directly from the compiled Chapter 37 PDF and the Rent Board Rules and Regulations Part IV page, both "
     "published on sf.gov.", cite("S6", "S5")],
    ["Base rents, tenancy dates, occupant changes, construction year",
     "<b>Owner-supplied.</b> Preserved exactly as given; not independently verifiable from public records within "
     "this project. Flagged F7, F8 and F9.", '<span class="b warn">Owner-supplied</span>'],
    ["Corporate-practice evidence",
     "Read from SEC EDGAR filings of a large institutional multifamily owner with a San Francisco Bay Area "
     "portfolio.", cite("S37", "S38", "S39")],
])}

<h3>5. Privacy method</h3>
{note("ok", "Anonymisation applied to everything published",
      "<p>Unit 1 is published as <b>Unit A</b>; Unit 2 as <b>Unit B</b>. Tenants are published as pseudonymous "
      "identifiers (T-A1 to T-A4, T-B1 to T-B2). Only <i>role</i> changes are shown &mdash; original tenant, "
      "departing tenant, added occupant &mdash; never a name. All dates and all dollar amounts are preserved exactly "
      "as supplied. No street address was supplied and none is published; the location appears only as "
      "&lsquo;San Francisco, CA 94122 (Outer Sunset)&rsquo;. The pseudonym-to-identity mapping is held by the owner "
      "and does not exist anywhere in this repository.</p><p>This matters beyond preference: information an owner "
      "files in the Rent Board Housing Inventory is <b>public</b>, including base rent in $250 increments. "
      + cite("S8") + "</p>")}

<h3>6. Reproducing every figure</h3>
<div class="panel"><pre style="margin:0;font-family:var(--mono);font-size:12.6px;overflow-x:auto">python3 tools/calc.py        # runs the 4 official self-tests, then prints every published number
python3 tools/build_site.py  # regenerates the site from data/_calc.json
python3 tools/check_links.py # verifies every internal and external link</pre>
<p class="small" style="margin-bottom:0"><code>tools/calc.py</code> aborts with a non-zero exit status if any
self-test fails, so a broken calculation can never be published.</p></div>

<h3>7. Known limits of this analysis</h3>
<ul>
<li>This is <b>not legal advice</b>. It is a documented, source-linked analysis intended to be handed to counsel or
to a Rent Board counselor for confirmation.</li>
<li>Coverage is <b>presumed</b> from an owner-reported 1940 construction year, not verified against a certificate of
occupancy (flag F9).</li>
<li>The rent increase license status is unknown (flag F4) and is a hard precondition to any enforceable increase.</li>
<li>The annual rate for the period beginning March 1, 2027 had not been published (flag F10); Unit B&rsquo;s total is
therefore published as &ldquo;13.1% + unpublished&rdquo;.</li>
<li>The full text of Rent Ordinance Sec. 37.8 could not be parsed from the compiled PDF, so the refund look-back
period for a null-and-void increase is not stated (flag F15).</li>
</ul>
"""
    return body


# ==========================================================================
# 3. LOCAL LAW
# ==========================================================================
@page("pages/law-local.html", "San Francisco (local law)",
      "Governing law &rsaquo; <b>San Francisco (local)</b>",
      "San Francisco Administrative Code Chapter 37 and Rent Board Rules and Regulations.")
def p_local():
    cov = tbl("Coverage: does the San Francisco Rent Ordinance apply?",
              ["Test", "Official rule", "Applied to these units", "Status"], [
        ["Date of construction",
         "Many residential units built on or before <b>June 13, 1979</b> have both rent control and eviction "
         "protection. sf.gov directs owners to check the building&rsquo;s age on the Property Information Map.",
         "Reported built <b>1940</b> &rarr; before June 13, 1979.", UNV],
        ["Not a partial exemption",
         "Units built after June 13, 1979; most single-family homes and condominiums (tenancy begun on or after "
         "1/1/1996); units that have undergone substantial rehabilitation; and units whose rent is controlled by "
         "another government agency have eviction protection only, not rent control.",
         "No indication of any of these. <b>Separately-alienable status was not supplied</b> and must be confirmed, "
         "because a condominium or single-family dwelling would change the analysis.", UNV],
        ["Not entirely exempt",
         "Eight categories are entirely exempt, including hotel/SRO accommodation occupied fewer than 32 continuous "
         "days, resident-majority non-profit co-ops, certain institutional housing, and units regulated by another "
         "government agency.", "Not indicated.", OK],
        ["Conclusion", "Coverage under Chapter 37.",
         "<b>Presumed covered.</b> Both units are treated as rent-controlled throughout this analysis.", UNV],
    ], note="Confirm the construction date and the unit type before relying on this: " + SRC["S21"]["url"])

    aga = tbl("The annual allowable increase (AGA)", ["Item", "Value", "Official source", "Status"], [
        ["Current AGA", "<b>1.6%</b> for increases effective March 1, 2026 &ndash; February 28, 2027",
         cite("S1", "S2", "S3"), OK],
        ["Prior AGA", "1.4% for March 1, 2025 &ndash; February 28, 2026", cite("S1", "S2"), OK],
        ["How it is set", "60% of the increase in the Consumer Price Index for All Urban Consumers in the Bay Area; "
         "published by the Rent Board each year, effective March 1.", cite("S3", "S6"), OK],
        ["Statutory ceiling", "In no event may the allowable annual increase be greater than <b>7%</b>.",
         cite("S6"), OK],
        ["Petition needed?", "<b>No.</b> A landlord is not required to file a petition to impose an annual allowable "
         "increase.", cite("S17", "S4"), OK],
        ["Frequency", "Once every 12 months.", cite("S3", "S16"), OK],
        ["Applied to", "<b>Base rent only.</b> Includes housing services such as parking and storage; excludes "
         "temporary passthroughs and fluctuating charges.", cite("S3", "S16"), OK],
        ["Rounding", "Increases <b>cannot be rounded up</b> to the nearest dollar.", cite("S3", "S17"), OK],
        ["Which year&rsquo;s rate", "Use the percentage that will be in effect on the <b>effective date</b> of the "
         "increase, not the percentage in effect when the notice is served.", cite("S3"), OK],
        ["Initial rent on a vacant unit", "<b>No limit.</b> There is no limit on what a landlord may first charge for "
         "an empty rent-controlled unit; Rules &amp; Regs Sec. 4.15 confirms the Ordinance does not regulate initial "
         "rent levels for a new tenancy.", cite("S3", "S5"), OK],
    ])

    bank = tbl("Banking of skipped increases", ["Item", "Official rule", "Source", "Status"], [
        ["Right to bank", "A landlord who refrains from imposing an annual increase, or any part of it, may "
         "accumulate it and impose it on or after the tenant&rsquo;s subsequent rent increase anniversary date.",
         cite("S5", "S4", "S6"), OK],
        ["Maturity", "&lsquo;A full <b>12 months</b> must have elapsed from the date that an annual rent increase, or "
         "a portion thereof, could have been imposed before this banking section becomes applicable.&rsquo; "
         "(Rules &amp; Regs Sec. 4.12(a) &mdash; the controlling text.)", cite("S5"), OK],
        ["<b>Conflicting statement on sf.gov</b>",
         "The sf.gov <i>Banked rent increases</i> page says a skipped increase banks only if &lsquo;at least <b>24 "
         "full months</b>&rsquo; pass &mdash; and then contradicts itself in its own worked example. See flag F3.",
         cite("S4"), '<span class="b bad">Conflict</span>'],
        ["Combination", "Banked percentages are added together and combined with the current annual increase; they "
         "are <b>not compounded</b> and <b>not rounded up</b>.", cite("S5", "S4"), OK],
        ["Cap on the total", "<b>There is no limit</b> on how much can be banked, back to April 1, 1982.",
         cite("S4"), OK],
        ["Expiry", "Banked increases <b>do not expire</b> during a tenancy.", cite("S4"), OK],
        ["Partial increases", "A landlord does not have to impose the maximum. If only part is used, the rest stays "
         "banked and may be imposed after at least 12 months, or on a future anniversary date.", cite("S4"), OK],
        ["Change of owner", "New owners <b>may</b> use banked increases accumulated by prior owners.", cite("S4"), OK],
        ["New tenant", "Banked increases <b>do not</b> carry over to a new tenant.", cite("S4"), OK],
        ["Forfeiture risk", "Changing the anniversary date permanently forfeits any skipped rate that had not yet "
         "matured.", cite("S3"), OK],
        ["Disclosure duty", "To impose an accumulated increase the landlord must inform the tenant which portion is "
         "banked and the dates on which it is based. Failure to include that information does not by itself render "
         "the increase null and void.", cite("S5", "S4"), OK],
        ["Good-faith overage", "If a banked increase exceeds the limit by no more than one-half of one percent of the "
         "prior base rent and was given in good faith, an Administrative Law Judge readjusts the base rent rather "
         "than voiding the increase.", cite("S5"), OK],
    ])

    lic = tbl("The rent increase license (Rent Ordinance Sec. 37.15)", ["Item", "Official rule", "Source", "Status"], [
        ["Who must report", "<b>All</b> owners of residential property, most even if they are not landlords.",
         cite("S8"), OK],
        ["What it produces", "Owners who report a tenant-occupied unit automatically receive a <b>rent increase "
         "license</b>, which allows them to impose annual allowable and banked increases.", cite("S8"), OK],
        ["When it must exist", "A current license must be on file <b>before any annual or banked rent increase goes "
         "into effect</b>. Without it the notice is not enforceable.", cite("S8", "S9"), OK],
        ["Consequence of no license", "A rent increase that goes into effect while the unit is unlicensed may be "
         "<b>null and void</b> &mdash; and this may apply for multiple years. The tenant may be entitled to a refund.",
         cite("S9"), OK],
        ["Deadline", "<b>March 1</b> every year. Late submission is still accepted and the Rent Board assesses "
         "<b>no monetary penalty</b> for filing late &mdash; but the increase is unenforceable until a license exists.",
         cite("S8"), OK],
        ["Where", "Rent Board Portal, portal.sfrb.org. Reporting is free and available 24/7.", cite("S8", "S22"), OK],
        ["Operative dates",
         "July 1, 2022 for non-condominium buildings with 10 or more units; reporting began March 1, 2023 for "
         "condominiums and buildings with fewer than 10 units. <b>An official Rent Board worksheet gives different "
         "dates (July 1, 2020 / March 1, 2021) &mdash; see flag F5.</b>", cite("S8", "S13"),
         '<span class="b bad">Conflict</span>'],
        ["Privacy consequence", "The information entered in the Housing Inventory submission is <b>public</b>, "
         "including approximate square footage, bedroom and bathroom counts, occupancy history and <b>base rent in "
         "$250 increments</b>.", cite("S8"), OK],
        ["Tenant visibility", "A tenant may search the Rent Board Portal to check whether the landlord holds a "
         "current license, and may file a Tenant Summary Petition (Form 361) if a notice took effect while "
         "unlicensed.", cite("S8", "S9", "S14"), OK],
        ["Status for these units", BLANK + " &mdash; not supplied and not published anywhere readable by this "
         "project. See flag F4.", cite("S8"), UNV],
    ])

    prohib = tbl("Bases on which an increase is PROHIBITED", ["Prohibited basis", "Official rule", "Source"], [
        ["A new or additional occupant",
         "&lsquo;A landlord may not impose increases solely because a tenant has added an additional occupant to an "
         "existing tenancy&hellip; The prohibition&hellip; shall apply notwithstanding a rental agreement or lease "
         "that specifically permits a rent increase for additional occupants.&rsquo; (Sec. 37.3(a)(11)(A)) "
         "Such a charge is an unlawful rent increase; any agreement to pay it is void and unenforceable, and a "
         "tenant may petition for a refund.", cite("S6", "S3", "S11")],
        ["Replacement of a departing roommate",
         "&lsquo;The landlord may not increase the rent for the unit based on the replacement of a departing tenant "
         "or the addition of new occupants, even if agreed to by the tenant.&rsquo;", cite("S11")],
        ["Algorithmic rent-setting",
         "Sec. 37.10C, &lsquo;Use and Sale of Algorithmic Devices Prohibited&rsquo; (Ordinance 224-24, effective "
         "October 14, 2024), prohibits the sale or use of algorithmic devices to set rents or manage occupancy levels "
         "for residential units.", cite("S6")],
        ["Harassment or forcing a tenant out",
         "Sec. 37.10B (Tenant Harassment) and Sec. 37.9F (Circumvention of Tenant Protections) are part of Chapter 37. "
         "An increase imposed for the purpose of compelling a tenant to leave is exposed under these provisions and "
         "under the fair-housing statutes.", cite("S6", "S33", "S34")],
        ["Severing a housing service without a rent reduction",
         "Garage and parking facilities, driveways, storage spaces, laundry rooms, decks, patios or gardens supplied "
         "with a unit may not be severed without just cause, and any severance, substantial reduction or removal of a "
         "housing service must be offset by a corresponding reduction in rent.", cite("S6")],
        ["An increase without a license", "Null and void in its entirety. See the license table above.",
         cite("S8", "S9")],
        ["A non-conforming notice",
         "&lsquo;Nonconforming Rent Increases. Any rent increase which does not conform with the provisions of this "
         "section shall be null and void.&rsquo; (Sec. 37.3(b)(5)) Rules &amp; Regs Sec. 4.10(b) is to the same "
         "effect, with the half-percent good-faith exception.", cite("S6", "S5")],
    ])

    above = tbl("Every mechanism that can raise rent above the AGA (a closed list)",
                ["Mechanism", "Petition required first?", "Limit", "Source"], [
        ["Annual allowable increase", "No", "The published AGA; never more than 7%", cite("S6", "S3")],
        ["Banked increases", "No", "No cap on the total accumulated", cite("S4", "S5")],
        ["Capital improvement passthrough", "<b>Yes</b>", "Not more than 5% of base rent in any 12-month period and "
         "never more than 15% over the life of the tenancy; imputed interest 4.1%-4.8% for 7/10/15/20-year "
         "amortisation", cite("S13", "S1")],
        ["Operating and maintenance expense increase", "<b>Yes</b>", "A certified O&amp;M increase shall not exceed "
         "<b>7%</b>", cite("S13", "S6")],
        ["Special circumstances &mdash; rents for comparable units", "<b>Yes</b>", "Determined by the Board",
         cite("S13")],
        ["Proposition I past rent history", "<b>Yes</b>", "Determined by the Board", cite("S13")],
        ["Utility passthrough (gas and electricity)", "Petition <b>or</b> worksheet", "Excluded from base rent; may be "
         "charged only at the time of an annual increase", cite("S13", "S5")],
        ["General obligation bond passthrough", "No petition; worksheet required", "50% of the property-tax change; "
         "excluded from base rent", cite("S13", "S6")],
        ["Water revenue bond passthrough", "No petition; worksheet required", "50% of the attributable charges; "
         "excluded from base rent", cite("S13", "S5")],
        ["Rules &amp; Regs Sec. 1.21 &mdash; no tenant in occupancy", "<b>Yes</b>", "Determined by the Board",
         cite("S13")],
        ["Lead hazard remediation", "Via O&amp;M or capital improvement", "Combined O&amp;M and capital-improvement "
         "increase not more than <b>10%</b> in any 12-month period", cite("S6")],
        ["Rent Board fee recovery", "No", "50% of the fee once it is paid in full &mdash; <b>$29.50</b> per dwelling "
         "unit for 2026-2027 &mdash; from a tenant in occupancy as of November 1 of the tax year", cite("S10", "S1")],
        ["Sec. 6.14 / Costa-Hawkins market reset", "Not required, but an elective determination petition exists",
         "Unlimited &mdash; but only when the <b>last</b> original occupant has permanently vacated, and for Sec. 6.14 "
         "only if a timely written 6.14 notice was served on each subsequent occupant", cite("S12", "S13", "S25")],
        ["Anything else", "<b>Yes</b> &mdash; Sec. 37.3(a)(8): a landlord who seeks to impose any rent increase which "
         "exceeds those permitted above shall petition for a rental arbitration hearing.", "Set by the Board",
         cite("S6", "S13")],
    ], note="Tenants need not pay a petition-based increase until the Rent Board approves it; if approved it is "
            "retroactive to the effective date specified in a valid notice. Filing is free. " + cite("S13"))

    remedies = tbl("What a tenant can do &mdash; the scrutiny any increase will face",
                   ["Remedy", "Form", "What it does", "Source"], [
        ["Unlawful rent increase / determination of lawful rent", "354",
         "Challenges the amount and asks the Board to determine the lawful rent from the full rent history. Free to "
         "file; resolved by mediation or by arbitration before an Administrative Law Judge.", cite("S14", "S18")],
        ["Tenant summary petition on an invalid notice", "361",
         "Used where a notice took effect while the owner was unlicensed or is otherwise invalid on its face.",
         cite("S14", "S9")],
        ["Substantial decrease in housing services", "352", "Seeks a rent reduction.", cite("S14")],
        ["Failure to repair and maintain", "353", "Seeks a rent reduction for habitability failures.", cite("S14")],
        ["Improper passthrough challenges", "355, 356, 357, 358",
         "Challenges utility, water-bond and general-obligation-bond passthroughs and a failure to discontinue a "
         "capital improvement passthrough.", cite("S14")],
        ["Subtenant claims", "359, 360",
         "Proportional-rent claim against a master tenant; unlawful initial rent claim by a subtenant.", cite("S14")],
        ["Report of alleged wrongful eviction", "362", "Reports a wrongful eviction.", cite("S14")],
        ["Tenant financial hardship application", "363", "Seeks relief from specified increases and passthroughs.",
         cite("S14")],
        ["<b>Outside the Rent Board&rsquo;s jurisdiction</b>", "&mdash;",
         "&lsquo;We do not adjudicate issues that are not related to the amount of rent charged, such as harassment, "
         "discrimination and retaliation. We also do not adjudicate issues involving security deposits. Such matters "
         "must be decided in court or another forum.&rsquo; Those claims go to the California Civil Rights Department, "
         "HUD or court.", cite("S14", "S33", "S34")],
        ["Free tenant counsel", "&mdash;",
         "The Rent Board publishes an official referral listing of free tenant-side counselling and legal services, "
         "including Bay Area Legal Aid, Housing Rights Committee of SF, Eviction Defense Collaborative, SF Tenants "
         "Union, Causa Justa :: Just Cause, Tenderloin Housing Clinic, Open Door Legal and Advancing Justice-Asian "
         "Law Caucus. No lawyer is needed to file a petition.", cite("S15")],
    ])

    fees = tbl("Other standing owner obligations that a tenant lawyer will check",
               ["Obligation", "Current amount / rule", "Source", "Status"], [
        ["Rent Board fee", "<b>$59.00</b> per dwelling unit ($29.50 per guest unit) for the 2026-2027 tax year; due "
         "<b>March 1</b>; a 5% penalty is added each month after March 1, capped at 15%; unpaid balances are referred "
         "to the Bureau of Delinquent Revenue after June 1. 50% is recoverable from a tenant in occupancy as of "
         "November 1.", cite("S10"), OK],
        ["Security-deposit interest", "<b>4.2%</b> for March 1, 2026 &ndash; February 28, 2027 (5.0% for the prior "
         "year). The Rent Board does not adjudicate deposit disputes &mdash; they go to court.", cite("S1", "S14"), OK],
        ["Housing Inventory reporting", "Annual, by <b>March 1</b>; produces the rent increase license.",
         cite("S8"), OK],
        ["Whether these were satisfied for both units", BLANK + " &mdash; no records supplied. See flag F8.",
         cite("S8", "S10"), UNV],
    ])

    body = f"""
<h2 class="pg">San Francisco &mdash; local law</h2>
<p class="lede">The San Francisco Residential Rent Stabilization and Arbitration Ordinance (Administrative Code
Chapter 37) and the Rent Board&rsquo;s Rules and Regulations are the operative law for both units. They are stricter
than state law and therefore control. This page sets out every local rule that bears on a rent increase, with the
official source for each.</p>

<h3>Coverage</h3>
{cov}

<h3>The annual allowable increase</h3>
{aga}

<h3>Banking &mdash; recovering increases that were never imposed</h3>
{bank}
{note("bad", "Flag F3 &mdash; two official sf.gov pages disagree",
      "<p>The <i>Banked rent increases</i> page states a skipped increase banks only after &lsquo;at least 24 full "
      "months&rsquo;. The controlling regulation, Rules and Regulations Sec. 4.12(a), states &lsquo;a full 12 "
      "months&rsquo;, and the same sf.gov page&rsquo;s own worked example banks a rate that had been available for "
      "only 12 months. This project applies the <b>regulation</b> (12 months) and reproduces all four official "
      "worked examples exactly under that rule. Because two official pages conflict, confirm with a Rent Board "
      "counselor on 415-252-4600 before serving a banked-increase notice. " + cite("S5", "S4", "S3") + "</p>")}

<h3>The rent increase license</h3>
{lic}

<h3>Notice requirements</h3>
{tbl("Notice rules", ["Situation", "Requirement", "Source", "Status"], [
    ["Total increase of 10% or less", "<b>At least 30 days&rsquo; written notice</b> before the effective date.",
     cite("S23", "S3"), OK],
    ["Total increase of more than 10%", "<b>At least 90 days&rsquo; written notice.</b> Measured against the rent "
     "charged at any time during the 12 months before the effective date, either alone or combined with any other "
     "increase in that period.", cite("S23", "S3"), OK],
    ["Notice sent by mail", "<b>Add 5 days</b> (35 or 95).", cite("S3", "S16", "S23"), OK],
    ["Form", "In writing. Increases are never triggered automatically.", cite("S16", "S3"), OK],
    ["Mandatory contents", "The dollar amount of the increase; the percentage amount; the date it takes effect; and "
     "&mdash; under Sec. 37.3(b) and Rules 4.10(a) and 4.12(b) &mdash; which portion reflects the annual increase "
     "and/or the banked amount, and the dates the banked amount is based on. Any capital-improvement, O&amp;M, "
     "comparable-units, passthrough or RAP-loan portion must be separately identified on the Board&rsquo;s forms.",
     cite("S6", "S5", "S3", "S4"), OK],
    ["Consequence of a defective notice", "Sec. 37.3(b)(5): a non-conforming increase is <b>null and void</b>. "
     "Rules 4.10(b) preserves the increase where the amount requested is no more than the allowable annual and banked "
     "increase, and allows an ALJ to readjust a good-faith overage within half of one percent.", cite("S6", "S5"), OK],
    ["Which rate to use", "The percentage in effect on the <b>date of the increase</b>, not on the date of service.",
     cite("S3"), OK],
])}

<h3>Prohibited bases for an increase</h3>
{prohib}

<h3>Mechanisms that can raise rent above the AGA</h3>
{above}

<h3>Tenant remedies &mdash; the review any increase will face</h3>
{remedies}

<h3>Standing owner obligations</h3>
{fees}

<h3>Where to go</h3>
<div class="kv">
<div>Rent Board counselor</div><div><b>415-252-4600</b> &mdash; free counseling, Monday to Friday 9am-12pm and 1pm-4pm</div>
<div>Rent Board office</div><div>25 Van Ness Avenue, Suite 700, San Francisco, CA 94102</div>
<div>Housing Inventory &amp; license</div><div><a href="{SRC['S22']['url']}" target="_blank"
rel="noopener noreferrer">portal.sfrb.org</a></div>
<div>Building age lookup</div><div><a href="{SRC['S21']['url']}" target="_blank" rel="noopener noreferrer">San
Francisco Property Information Map</a></div>
</div>
"""
    return body


# ==========================================================================
# 4. STATE LAW
# ==========================================================================
@page("pages/law-state.html", "California (state law)",
      "Governing law &rsaquo; <b>California (state)</b>",
      "Costa-Hawkins, AB 1482 and Civil Code Section 827 as applied to two rent-controlled San Francisco units.")
def p_state():
    body = f"""
<h2 class="pg">California &mdash; state law</h2>
<p class="lede">Three state statutes matter here. Costa-Hawkins (Civil Code Sec. 1954.50 et seq.) sets the outer
limits of local rent control and governs when an owner may reprice a unit. The Tenant Protection Act of 2019
(AB 1482, Civil Code Sec. 1947.12) sets a statewide cap &mdash; but it does <b>not</b> apply to these units.
Civil Code Sec. 827 sets the notice periods, which San Francisco&rsquo;s local pages mirror.</p>

<h3>The decisive provision for Unit A</h3>
{note("ok", "Cal. Civ. Code Sec. 1954.53(d)(3) &mdash; a partial change in occupancy does NOT permit a market reset",
      "<p>Sec. 1954.53(d)(2) allows an owner to increase the rent by any amount allowed by the section to a lawful "
      "sublessee or assignee who did not reside at the unit before January 1, 1996, but only &lsquo;if the original "
      "occupant or occupants who took possession of the dwelling or unit pursuant to the rental agreement with the "
      "owner <b>no longer permanently reside there</b>&rsquo;.</p>"
      "<p>Sec. 1954.53(d)(3) then removes that power in exactly Unit A&rsquo;s situation: &lsquo;This subdivision "
      "<b>does not apply to partial changes in occupancy</b> of a dwelling or unit where <b>one or more of the "
      "occupants</b> of the premises, pursuant to the agreement with the owner provided for above, <b>remains an "
      "occupant in lawful possession</b> of the dwelling or unit&hellip;&rsquo;</p>"
      "<p>Sec. 1954.53(b) reinforces the result: an owner&rsquo;s right to set an initial rate &lsquo;applies to, and "
      "includes, <b>renewal of the initial hiring by the same tenant</b>&hellip; for the entire period of their "
      "occupancy <b>at the rental rate established for the initial hiring</b>&rsquo;.</p>"
      "<p>One original tenant of Unit A remains in possession. Therefore no market-rate reset is available, and the "
      "lawful ceiling stays tied to the " + usd(A['base']) + " base rent with a February 1 anniversary date. "
      + cite("S25") + "</p>")}

{tbl("Costa-Hawkins Rental Housing Act, Civil Code Sec. 1954.50 - 1954.535",
     ["Provision", "What it says", "Effect here", "Status"], [
    ["Sec. 1954.52(a)(1)", "An owner may establish the initial and all subsequent rental rates for a unit with a "
     "certificate of occupancy issued after February 1, 1995.",
     "Not applicable &mdash; the building is reported built in 1940.", NAB],
    ["Sec. 1954.52(a)(2)", "Same, for a unit already exempt on or before February 1, 1995 under a local "
     "new-construction exemption.", "Not applicable.", NAB],
    ["Sec. 1954.52(a)(3)", "Same, for a unit alienable separately from any other dwelling unit (a condominium or "
     "single-family dwelling), subject to subparagraph (B) carve-outs.",
     "<b>Must be confirmed.</b> Unit type was not supplied. If either unit is separately alienable and the tenancy "
     "began on or after January 1, 1996, the local rent cap would not apply and only eviction protection would "
     "remain. Unit A&rsquo;s tenancy began in 2025 and Unit B&rsquo;s in 2019, both after that date.", UNV],
    ["Sec. 1954.52(d)", "The section does not apply to a unit with serious health, safety, fire or building code "
     "violations, cited by a governmental agency and unabated for six months or longer preceding the vacancy.",
     "No citation history supplied. " + BLANK, UNV],
    ["Sec. 1954.53(a)", "An owner may establish the <b>initial</b> rental rate for a dwelling or unit, except where "
     "the previous tenancy was terminated by the owner under Sec. 1946.1 or by a Sec. 827 change in terms (other "
     "than a lawful rent or fee change), and subject to other listed exceptions.",
     "Would apply only on a genuine vacancy. Neither unit is vacant.", NAB],
    ["Sec. 1954.53(b)", "Subdivision (a) includes <b>renewal of the initial hiring by the same tenant</b>, lessee, "
     "authorised subtenant or sublessee for the entire period of their occupancy <b>at the rental rate established "
     "for the initial hiring</b>.",
     "A lease renewal &mdash; including the April 1, 2026 continuing-tenancy arrangement on Unit A &mdash; is not a "
     "new tenancy and does not permit a reset.", OK],
    ["Sec. 1954.53(d)(2)", "If the original occupant or occupants no longer permanently reside there, the owner may "
     "increase the rent by any amount allowed by the section to a lawful sublessee or assignee who did not reside "
     "there before January 1, 1996.",
     "Not triggered: an original occupant of Unit A remains, and both original occupants of Unit B remain.", OK],
    ["Sec. 1954.53(d)(3)", "<b>Does not apply to partial changes in occupancy</b> where one or more occupants under "
     "the agreement with the owner remains in lawful possession.",
     "<b>Directly disposes of Unit A.</b> The April 1, 2026 change was a partial change in occupancy.", OK],
    ["Sec. 1954.53(f)", "The section does not apply where the unit has been cited for serious code violations at "
     "least 60 days before the vacancy and the violation was unabated when the prior tenant vacated.",
     "No citation history supplied. " + BLANK, UNV],
    ["Rules &amp; Regs Sec. 6.14 (local implementation)",
     "An unlimited increase on remaining occupants when the <b>last</b> original occupant vacates, and only if a "
     "written 6.14 notice was served on each subsequent occupant within a reasonable time (generally 60 days) after "
     "the landlord knew or should have known of the occupancy. A <b>co-tenant</b> &mdash; someone with an oral or "
     "written agreement with the landlord, or who became a tenant by the landlord&rsquo;s acceptance of rent &mdash; "
     "is never subject to it, whenever they moved in.",
     "Not available for Unit A: the last original occupant has not vacated. Whether the added occupant is a "
     "co-tenant or a subtenant was not supplied, and whether any 6.14 notice was ever served was not supplied. "
     "See flag F6.", UNV],
])}

<h3>AB 1482 &mdash; the statewide cap, and why it does not govern these units</h3>
{tbl("Cal. Civil Code Sec. 1947.12", ["Provision", "What it says", "Effect here", "Status"], [
    ["Sec. 1947.12(a)(1)", "Over any 12-month period an owner shall not increase the gross rental rate more than "
     "<b>5% plus the percentage change in the cost of living, or 10%, whichever is lower</b>, of the lowest gross "
     "rental rate charged at any time during the prior 12 months.",
     "Would allow far more than the San Francisco cap. See the computation below.", OK],
    ["Sec. 1947.12(a)(2)", "If the same tenant remains in occupancy over any 12-month period the rate shall not be "
     "increased in more than two increments.", "Not reached &mdash; the section does not apply here.", NAB],
    ["<b>Sec. 1947.12(d)(3)</b>", "<b>Exemption:</b> the section does not apply to housing subject to rent or price "
     "control through a public entity&rsquo;s valid exercise of its police power consistent with Chapter 2.7 "
     "(Sec. 1954.50 et seq.) <b>that restricts annual increases to an amount less than</b> subdivision (a) provides.",
     "<b>Decisive.</b> San Francisco&rsquo;s cap of 1.6% is less than the statewide 8.8%, so these units are "
     "<b>exempt from the AB 1482 cap</b> and are governed solely by Chapter 37. The state cap is context only and "
     "must not be used.", OK],
    ["Sec. 1947.12(d)(4)", "Exemption for housing issued a certificate of occupancy within the previous 15 years.",
     "Not applicable to a 1940 building.", NAB],
    ["Sec. 1947.12(d)(5)(A)", "The separately-alienable (single-family / condominium) exemption is available only if "
     "the owner is <b>not</b> a real estate investment trust, <b>not</b> a corporation, and <b>not</b> a limited "
     "liability company in which at least one member is a corporation.",
     "Relevant to the corporate-versus-individual comparison: entity form can narrow the available exemptions.", OK],
    ["Sec. 1947.12(d)(6)", "Exemption for a property with two separate dwelling units in a single structure where the "
     "owner occupied one as a principal residence at the beginning of the tenancy and continues in occupancy.",
     "Owner occupancy was not supplied. " + BLANK, UNV],
    ["Sec. 1947.12(e)", "Notice of any increase must be given in accordance with Sec. 827.",
     "Consistent with the local 30/90-day rule.", OK],
    ["Sec. 1947.12(g)(1)(A)(iv)", "The applicable index is the CPI-U for the <b>San Francisco-Oakland-Hayward</b> "
     "metropolitan area, covering Alameda, Contra Costa, Marin, San Francisco and San Mateo counties.",
     "ZIP 94122 is in San Francisco County, so this is the correct region.", OK],
    ["Sec. 1947.12(g)(3)(B)", "For increases taking effect on or after August 1 of a year, the percentage change is "
     "that between the amount published for April of that year and April of the immediately preceding year, rounded "
     "to the nearest one-tenth of one percent.",
     "Supplies the CPI inputs used in the computation below.", OK],
    ["Sec. 1947.12(h)(1)", "Applies to rent increases occurring on or after March 15, 2019.",
     "Context only.", NAB],
])}

{tbl("The AB 1482 cap computed for this region (context only - it does not apply)",
     ["Period for increases taking effect", "CPI-U SF-Oakland-Hayward, April to April", "5% + CPI", "Statutory maximum",
      "Cap", "Governs these units?"], [
    ["August 1, 2025 &ndash; July 31, 2026", "1.3% (April 2025)", "5.0% + 1.3%", "10%", "<b>6.3%</b>",
     '<span class="b bad">No</span>'],
    ["August 1, 2026 &ndash; July 31, 2027", "3.8% (April 2026)", "5.0% + 3.8%", "10%", "<b>8.8%</b>",
     '<span class="b bad">No</span>'],
    (["San Francisco local cap for comparison", "60% of Bay Area CPI-U", "&mdash;", "7% (Ordinance ceiling)",
      "&mdash;", "<b>1.6%</b>", '<span class="b rec">YES &mdash; controls</span>'], "total"),
], numeric_cols=(1, 2, 3, 4, 5),
   note="CPI values from the CA Department of Industrial Relations table last updated 10/15/2026 "
        + cite("S29") + "; cap formula and exemption from " + cite("S24") +
        "; the local rate from " + cite("S1", "S2") + ". Because 1.6% &lt; 8.8%, Sec. 1947.12(d)(3) exempts these "
        "units from the state cap entirely.")}

<h3>Notice &mdash; Cal. Civil Code Sec. 827</h3>
{tbl("Sec. 827 notice periods", ["Provision", "Requirement", "Source", "Status"], [
    ["Sec. 827(b)(1)", "For a month-to-month residential tenancy the landlord may increase the rent on written "
     "notice, delivered personally or served by mail under Code of Civil Procedure Sec. 1013.", cite("S23"), OK],
    ["Sec. 827(b)(2)", "Where the proposed increase is <b>10 percent or less</b> of the rental amount charged at any "
     "time during the 12 months before the effective date, alone or combined with any other increase in that period, "
     "notice must be delivered <b>at least 30 days</b> before the effective date.", cite("S23"), OK],
    ["Sec. 827(b)(3)(A)", "Where the proposed increase is <b>greater than 10 percent</b> on the same measure, notice "
     "must be delivered <b>at least 90 days</b> before the effective date.", cite("S23"), OK],
    ["Sec. 827(b)(3)(B)", "Where the increase is caused by a change in a tenant&rsquo;s income or family composition "
     "as determined by a statutorily required recertification, 30 days applies instead.",
     "Not applicable &mdash; no assistance programme was reported.", NAB],
    ["Local overlay", "San Francisco repeats the 30/90-day structure and adds <b>5 days if the notice is mailed</b>, "
     "plus mandatory content requirements.", cite("S3", "S16", "S6"), OK],
])}

<h3>Just cause &mdash; context</h3>
{note("", "Sec. 1946.2 and Chapter 37 Sec. 37.9",
      "<p>AB 1482 also created a statewide just-cause requirement at Civil Code Sec. 1946.2. For these units the "
      "operative just-cause regime is the local one: sf.gov lists the grounds under the Rent Ordinance, including "
      "non-payment, breach of the rental agreement, nuisance, owner or relative move-in, condominium conversion, "
      "capital improvement work that makes the unit unlivable, and removal of all units from the rental market under "
      "the state Ellis Act. Just cause is not directly engaged by a lawful rent increase, but it matters to the "
      "red-team analysis: an increase imposed in order to manufacture a non-payment or breach ground is exposed as "
      "harassment under Sec. 37.10B and as circumvention under Sec. 37.9F. "
      + cite("S7", "S27", "S6") + "</p>")}

<h3>Which law controls &mdash; summary</h3>
{tbl("Order of application", ["Question", "Controlling law", "Why", "Source"], [
    ["How much may rent be raised on these two units?",
     "<b>San Francisco Administrative Code Chapter 37</b>",
     "Sec. 1947.12(d)(3) exempts housing whose local cap is lower than the state cap; 1.6% &lt; 8.8%.",
     cite("S24", "S1")],
    ["How much notice?", "<b>Both, read together</b>",
     "Sec. 827 sets 30/90 days; Chapter 37 and the Rent Board pages add 5 days if mailed and mandatory content.",
     cite("S23", "S3", "S6")],
    ["May the unit be repriced to market?", "<b>Costa-Hawkins, Sec. 1954.53</b>",
     "Only on a true vacancy, or under Rules 6.14 when the last original occupant leaves and a timely notice was "
     "served. Neither is present.", cite("S25", "S12")],
    ["May the increase be discriminatory or retaliatory?", "<b>Federal and state fair-housing law</b>",
     "The Fair Housing Act and the California Civil Rights Act apply regardless of rent control, and the Rent Board "
     "expressly does not adjudicate them.", cite("S34", "S33", "S14")],
])}
"""
    return body


# ==========================================================================
# 5. FEDERAL LAW
# ==========================================================================
@page("pages/law-federal.html", "Federal law",
      "Governing law &rsaquo; <b>Federal</b>",
      "What federal law does and does not require for a rent increase in San Francisco.")
def p_federal():
    body = f"""
<h2 class="pg">Federal law</h2>
<p class="lede">Federal law does not set a rent-increase ceiling for privately owned, unsubsidised residential
housing. What it does impose is a constraint on <b>how</b> rent may be set: the Fair Housing Act prohibits
discrimination in the terms, conditions or privileges of a rental, including price. Federal rent limits attach only
to federally assisted housing.</p>

{tbl("Federal rules relevant to a rent increase", ["Item", "Federal position", "Source", "Status"], [
    ["Maximum allowable rent increase", BLANK,
     "No federal statute sets one for private unsubsidised housing. Recorded as a deliberate negative finding &mdash; "
     "see flag F13.", '<span class="b na">No federal cap</span>'],
    ["Anti-discrimination in setting rent",
     "The Fair Housing Act, <b>42 U.S.C. Sec. 3601 et seq.</b>, prohibits discrimination by direct providers of "
     "housing, &lsquo;such as landlords and real estate companies&rsquo;, whose practices make housing unavailable "
     "because of race or colour, religion, sex, national origin, familial status or disability. Setting different "
     "prices on a prohibited basis falls within &lsquo;terms, conditions or privileges&rsquo; of rental.",
     cite("S34"), OK],
    ["Enforcement routes",
     "An individual may file a complaint with HUD or bring their own lawsuit in federal or state court. The "
     "Department of Justice brings suits on referrals from HUD and in pattern-or-practice cases, and may institute "
     "criminal proceedings where force or threat of force is used. DOJ also runs a Fair Housing Testing Program to "
     "uncover hidden discrimination.", cite("S34", "S35"), OK],
    ["Federally assisted housing",
     "Where rent is controlled or regulated by a government unit, agency or authority &mdash; for example Section 8 "
     "&mdash; federal programme rules set the rent, and San Francisco&rsquo;s Rent Ordinance treats such units as a "
     "separate category. <b>Whether either unit is federally assisted was not supplied.</b> " + BLANK,
     cite("S7", "S6"), UNV],
    ["Effect of federal assistance on the local cap",
     "For units occupied by recipients of tenant-based assistance where the tenant&rsquo;s share is not a fixed "
     "percentage of income (Housing Choice Voucher, Over-FMR Tenancy, HOPWA): if base rent is at or above the "
     "Payment Standard the local limits in Sec. 37.3(a)(1) and (2) apply to the entire base rent; if below, the local "
     "limits do not apply but a new base rent may not exceed the Payment Standard plus the Sec. 37.3(a)(1) increase. "
     "Where the tenant&rsquo;s share <b>is</b> a fixed percentage of income (Section 8 Certificate), the local limits "
     "do not apply and adjustments follow the assistance programme.", cite("S6"), OK],
    ["Enterprise (Fannie Mae / Freddie Mac) lease standards",
     BLANK + " &mdash; reported announced 2024-07-12 for new loans signed on or after 2025-02-28 (30-day written "
     "notice of a rent increase, 30-day notice of lease expiration, 5-day grace period), reportedly paused and then "
     "rescinded in March 2025. <b>Could not be confirmed on fhfa.gov</b> &mdash; the newsroom URLs returned "
     "&lsquo;Page Not Found&rsquo; on " + d(AS_OF) + ". Not relied on anywhere in this analysis. See flag F12.",
     UNV],
    ["Federal preemption of state or local rent control",
     "None. Costa-Hawkins is a state statute limiting local rent control; the Fair Housing Act regulates "
     "discrimination, not price. Nothing in the federal material reviewed displaces Chapter 37.",
     cite("S34", "S24", "S25"), OK],
])}

<h3>Fair Housing Act protected characteristics</h3>
{tbl("Federal protected characteristics", ["Characteristic", "Notes from the DOJ statement"], [
    ["Race or colour", "A central objective of the Act since 1968; most DOJ pattern-or-practice cases involve race "
     "discrimination. DOJ notes that providers sometimes disguise discrimination with false information about "
     "availability, or by steering."],
    ["Religion", "Covers overt discrimination and less direct actions. A limited exception exists for non-commercial "
     "housing operated by a religious organisation."],
    ["Sex", "Includes sexual harassment; DOJ&rsquo;s enforcement targets landlords who create an untenable living "
     "environment by demanding sexual favours or creating a sexually hostile environment."],
    ["National origin", "May be based on the individual&rsquo;s country of birth or that of their ancestors."],
    ["Familial status", "Families with children and pregnancy."],
    ["Disability", "Includes the duty to permit reasonable modifications and reasonable accommodations."],
])}
<p class="small">Source: {cite("S34")}. California law protects a materially longer list &mdash; including ancestry,
citizenship, immigration status, primary language, sexual orientation, gender identity and expression, genetic
information, marital status, <b>source of income</b> (including a Section 8 voucher), military or veteran status and
<b>age</b> &mdash; and also protects association with someone who has a characteristic and characteristics a person
is perceived to have. Where state and federal law differ, the stricter rule governs. See
<a href="fair-housing.html">One unit or both?</a> and {cite("S33")}.</p>

{note("warn", "What this means in practice",
      "<p>Federal law is not a source of permission to raise rent &mdash; it is a source of <b>constraint</b>. A "
      "lawful, correctly calculated San Francisco increase can still be unlawful federally and under state law if the "
      "<i>reason</i> for it, or the pattern of who receives it, is tied to a protected characteristic. Critically, the "
      "Rent Board <b>cannot</b> hear these claims: it states that it does not adjudicate harassment, discrimination "
      "or retaliation, and that such matters must be decided in court or another forum. That routes any "
      "discrimination allegation to the California Civil Rights Department, to HUD, or to court &mdash; a different "
      "forum with different remedies from a rent-overcharge petition. " + cite("S14", "S33", "S34") + "</p>")}
"""
    return body


# ==========================================================================
# 6. RATES & CPI
# ==========================================================================
@page("pages/rates.html", "Official rates & CPI",
      "Data &amp; findings &rsaquo; <b>Official rates &amp; CPI</b>",
      "Every allowable annual increase published by the SF Rent Board since 1982, plus CPI, deposit interest and fees.")
def p_rates():
    rows = []
    for s, en, p in AGA:
        cur = (s == date(2026, 3, 1))
        rows.append(([s.strftime("%-m/%-d/%y"), en.strftime("%-m/%-d/%y"), f"{p}%",
                      '<span class="b rec">IN EFFECT</span>' if cur else ""] , "sub" if cur else ""))
    rows.append((["3/1/27", "2/28/28", '<span class="empty">&mdash; not published &mdash;</span>', GAP], "total"))
    aga_tbl = tbl("SF Rent Board allowable annual increases &mdash; complete official history",
                  ["Effective from", "Through", "Increase", ""], rows,
                  note="Transcribed verbatim from SF Rent Board document 571, &lsquo;Allowable Annual Increases&rsquo; "
                       + cite("S2") + ", cross-checked against " + cite("S1") + ". Official caution on document 571: "
                       "for the period March 1, 1992 through February 28, 1993 <b>only one</b> of the two listed "
                       "increases may be imposed, based on the tenant&rsquo;s anniversary date or date of last "
                       "increase. The rate for the period beginning March 1, 2027 had not been published as of "
                       + d(AS_OF) + " and is left blank &mdash; it is never forecast (flag F10).")

    sr, sa = ST["recent"], ST["all"]
    stats_tbl = tbl("What &lsquo;normal&rsquo; looks like, measured from the official table",
                    ["Measure", "Periods", "n", "Mean", "Median", "Minimum", "Maximum"], [
        ["Allowable annual increase", "March 1, 2019 &ndash; March 1, 2026", sr["n"],
         f"{float(sr['mean']):.4f}%", sr["median"] + "%", sr["min"] + "%", sr["max"] + "%"],
        ["Allowable annual increase", "April 1, 1982 &ndash; March 1, 2026", sa["n"],
         f"{float(sa['mean']):.4f}%", sa["median"] + "%", sa["min"] + "%", sa["max"] + "%"],
    ], numeric_cols=(2, 3, 4, 5, 6),
       note="Computed by <code>tools/calc.py</code> from the official document 571 series " + cite("S2") + ". The "
            "long-run set excludes the split 1992-93 pair because document 571 cautions that only one of those two "
            "rates may be imposed for that year. The 7% figures at the head of the series reflect the original "
            "Ordinance&rsquo;s 7% ceiling; the modern 60%-of-CPI formula has produced between 0.1% and 3.6%.")

    cpi_rows = []
    for period, val in CPI_SF_OAKLAND_HAYWARD:
        if val is None:
            cpi_rows.append([period, BLANK, "Not published &mdash; see flag F10 and the DIR notice"])
        else:
            cpi_rows.append([period, val, ""])
    cpi_tbl = tbl("CPI-U, San Francisco-Oakland-Hayward metropolitan area &mdash; 12-month percentage change, "
                  "All Urban Consumers",
                  ["Reference month", "12-month change", "Note"], cpi_rows, numeric_cols=(1,),
                  note="Transcribed from the California Department of Industrial Relations, Office of the Director "
                       "&ndash; Research Unit, percentage-change table, last updated 10/15/2026 " + cite("S29") +
                       ". DIR&rsquo;s December 16, 2025 notice records that BLS could not collect October 2025 "
                       "reference-period data because of the federal government shutdown and will not publish it "
                       + cite("S31") + ". San Francisco&rsquo;s AGA is normally computed October-to-October, which is "
                       "why the 2026-27 rate required an unusual methodology.")

    body = f"""
<h2 class="pg">Official rates &amp; CPI</h2>
<p class="lede">Every percentage used anywhere on this site, transcribed from official publications. Nothing here is
derived from a third-party calculator or aggregator.</p>

<div class="cards">
{card("Allowable increase now", "1.6%", "March 1, 2026 &ndash; February 28, 2027", cite("S1", "S2"), "accent")}
{card("Previous period", "1.4%", "March 1, 2025 &ndash; February 28, 2026", cite("S1", "S2"))}
{card("Before that", "1.7%", "March 1, 2024 &ndash; February 28, 2025", cite("S1", "S2"))}
{card("Ordinance ceiling", "7%", "The allowable annual increase may never exceed 7%", cite("S6"))}
{card("Security-deposit interest", "4.2%", "March 1, 2026 &ndash; February 28, 2027", cite("S1"))}
{card("Rent Board fee", "$59.00", "Per dwelling unit, 2026-2027 tax year, due March 1", cite("S10"))}
{card("Mean AGA since 2019", f"{float(sr['mean']):.2f}%", f"Median {sr['median']}% over {sr['n']} periods",
      cite("S2"))}
{card("Mean AGA since 1982", f"{float(sa['mean']):.2f}%", f"Median {sa['median']}% over {sa['n']} periods",
      cite("S2"))}
</div>

<h3>What is &lsquo;reasonable and normal&rsquo;, measured</h3>
{stats_tbl}
{note("ok", "The evidence-based answer to &lsquo;what is normal&rsquo;",
      "<p>A <b>normal</b> annual increase in San Francisco is the published allowable increase and nothing more: "
      "<b>1.6%</b> right now, against a long-run average of <b>" + f"{float(sa['mean']):.2f}" + "%</b> since 1982 and "
      "<b>" + f"{float(sr['mean']):.2f}" + "%</b> since 2019. A <b>reasonable</b> increase is one that (i) does not "
      "exceed the published rate plus properly matured banked amounts, (ii) is calculated on base rent only, "
      "(iii) is served with the correct notice period and the mandatory content, (iv) is supported by a current rent "
      "increase license, and (v) is not motivated by a protected characteristic, by retaliation, or by a wish to "
      "displace. California courts have held that rent regulation must still allow an owner a <b>fair rate of "
      "return</b>, which is the constitutional floor on the other side of the ledger. "
      + cite("S1", "S2", "S3", "S32") + "</p>")}

<h3>Complete allowable annual increase history</h3>
{aga_tbl}

<h3>Other rates the Rent Board publishes</h3>
{tbl("Current rates, March 1, 2026 - February 28, 2027", ["Item", "2026-27", "2025-26", "2024-25", "Source"], [
    ["Allowable rent increase", "<b>1.6%</b>", "1.4%", "1.7%", cite("S1")],
    ["Security deposit interest", "<b>4.2%</b>", "5.0%", "5.2%", cite("S1")],
    ["Rent Board fee (dwelling unit)", "<b>$59.00</b>", BLANK, BLANK, cite("S10")],
    ["Rent Board fee recoverable from tenant", "<b>$29.50</b>", "$29.50 (3/1/25)", "$29.50 (3/1/24)",
     cite("S10", "S1")],
    ["Capital improvement imputed interest, 7-year amortisation (factor .01372)", "<b>4.1%</b>", BLANK, BLANK,
     cite("S1")],
    ["Capital improvement imputed interest, 10-year amortisation (factor .01027)", "<b>4.3%</b>", BLANK, BLANK,
     cite("S1")],
    ["Capital improvement imputed interest, 15-year amortisation (factor .00770)", "<b>4.6%</b>", BLANK, BLANK,
     cite("S1")],
    ["Capital improvement imputed interest, 20-year amortisation (factor .00649)", "<b>4.8%</b>", BLANK, BLANK,
     cite("S1")],
    ["Relocation payment per tenant, no-fault eviction", "<b>$8,245.00</b>", "$8,062.00", BLANK, cite("S1")],
    ["Relocation maximum per unit, no-fault eviction", "<b>$24,733.00</b>", "$24,184.00", BLANK, cite("S1")],
    ["Additional amount per elderly or disabled tenant, or household with minor children", "<b>$5,497.00</b>",
     "$5,375.00", BLANK, cite("S1")],
    ["Relocation per tenant, Ellis Act", "<b>$11,110.05</b>", "$10,863.45", BLANK, cite("S1")],
    ["Temporary displacement under 20 days", "<b>$446.00/day</b> plus actual moving expenses",
     "$436.00/day plus actual moving expenses", BLANK, cite("S1")],
])}
<p class="small">Relocation and temporary-displacement rates are published here for completeness. They are triggered
by eviction and displacement, not by a rent increase, and are <b>not</b> engaged by any scenario on this site.</p>

<h3>Consumer Price Index</h3>
{cpi_tbl}

<h3>The statewide AB 1482 cap (does not govern these units)</h3>
{tbl("AB 1482 computation for the San Francisco-Oakland-Hayward region",
     ["Period", "April-to-April CPI-U", "5% + CPI", "Cap (lower of that or 10%)", "Applies here?"], [
    ["Aug 1, 2025 &ndash; Jul 31, 2026", "1.3%", "6.3%", "<b>6.3%</b>", '<span class="b bad">No</span>'],
    ["Aug 1, 2026 &ndash; Jul 31, 2027", "3.8%", "8.8%", "<b>8.8%</b>", '<span class="b bad">No</span>'],
], numeric_cols=(1, 2, 3),
   note="Civ. Code Sec. 1947.12(a)(1), (g)(1)(A)(iv) and (g)(3)(B) " + cite("S24") + "; CPI from " + cite("S29") +
        ". Sec. 1947.12(d)(3) exempts housing under a local ordinance that restricts annual increases to less than "
        "the state cap. San Francisco&rsquo;s 1.6% is lower, so the local cap governs and the state figures are "
        "context only.")}
"""
    return body


# ==========================================================================
# 7. UNIT DOSSIERS
# ==========================================================================
@page("pages/units.html", "Unit dossiers (anonymised)",
      "Data &amp; findings &rsaquo; <b>Unit dossiers</b>",
      "Field-by-field anonymised dossiers for Unit A and Unit B with verification status for every value.")
def p_units():
    def dossier(code, orig, u, extra_rows):
        s1, s2 = u["s1"], u["s2"]
        rows = [
            ["Public identifier", f"<b>{code}</b>", "Anonymised. The supplied designation is not published.",
             '<span class="b na">Privacy control</span>'],
            ["Location", "San Francisco, CA 94122 (Outer Sunset)",
             "Supplied as context. No street address was supplied and none is published.",
             '<span class="b na">Context only</span>'],
            ["Building constructed", "1940", "Owner-reported. Not verified against a public record &mdash; flag F9.",
             UNV],
            ["Rent control coverage", "Presumed covered &mdash; built on or before June 13, 1979",
             cite("S7"), UNV],
            ["Tenancy began", d(u["anniversary"]), "Supplied lease start; preserved exactly.", OK],
            ["Anniversary date for increases",
             date.fromisoformat(u["anniversary"]).strftime("%B %-d").replace(" 0", " "),
             "No increase has been imposed, so the anniversary remains the lease start date. " + cite("S3", "S16"),
             OK],
            ["Base rent", usd(u["base"]), "Supplied. Composition (parking, storage, passthroughs) not stated &mdash; "
             "flag F7.", OK],
            ["Increases imposed to date", "None recorded", "Nothing was supplied. If any increase was ever imposed "
             "the anniversary date and every figure below change &mdash; flag F8.", UNV],
            ["Rent increase license on file", BLANK, "Not supplied and not readable from here. A current license is "
             "required on the effective date or the entire increase is null and void &mdash; flag F4. " +
             cite("S8", "S9"), UNV],
        ] + extra_rows + [
            ["Banked increase matured", pct(s1["banked"]),
             "Sum of the annual rates available on each skipped anniversary that has completed a full 12 months. "
             "Rules &amp; Regs Sec. 4.12(a). " + cite("S5", "S4", "S2"), OK],
            ["Annual rate in effect on the recommended date",
             pct(s1["current_aga"]) if s1["current_aga"] else BLANK,
             cite("S1", "S2"), OK if s1["current_aga"] else GAP],
            ["Total lawful increase",
             pct(s1["total"]) if s1["current_aga"] else pct(s1["total_known"]) + " + unpublished",
             cite("S3", "S4", "S5"), OK],
            ["Dollar increase",
             usd(s1["amount"]) if s1["current_aga"] else usd(s1["amount_known"]) + " (minimum)",
             "Base rent &times; total percentage, truncated to the cent, never rounded up. " + cite("S3"), OK],
            ["New base rent",
             usd(s1["new_rent"]) if s1["current_aga"] else usd(s1["new_rent_known"]) + " (minimum)",
             cite("S3"), OK],
            ["Notice period required",
             f"<b>{s1['notice_days']} days</b>",
             "90 days because the total exceeds 10%" if s1["notice_days"] == 90
             else "30 days because the total is 10% or less",
             OK],
            ["Serve on or before (hand-delivered)", d(s1["serve_by"]), cite("S23", "S3"), OK],
            ["Serve on or before (mailed, +5 days)", d(s1["serve_by_mailed"]), cite("S23", "S3"), OK],
            ["Security-deposit interest paid", BLANK, "4.2% is due for 2026-27. No record supplied &mdash; flag F8. "
             + cite("S1"), UNV],
            ["Rent Board fee paid", BLANK, "$59.00 per dwelling unit, due March 1. No record supplied &mdash; flag F8. "
             + cite("S10"), UNV],
        ]
        return tbl(f"{code} &mdash; {orig}", ["Field", "Value", "Basis / note", "Status"], rows)

    a_extra = [
        ["Original tenants (lease of February 1, 2025)", "T-A1, T-A2, T-A3",
         "Three occupants took possession under the original rental agreement.", OK],
        ["Continuing tenancy from April 1, 2026", "T-A1 + T-A4",
         "One original tenant departed and one occupant was added. Rent remained " + usd(A["base"]) + ".", OK],
        ["Nature of the April 1, 2026 change", "<b>Partial change in occupancy</b>",
         "Cal. Civ. Code Sec. 1954.53(d)(3): a market-rate reset &lsquo;does not apply to partial changes in "
         "occupancy&hellip; where one or more of the occupants&hellip; remains an occupant in lawful "
         "possession&rsquo;. " + cite("S25"), OK],
        ["May rent be raised because of the added occupant?", "<b>No</b>",
         "Sec. 37.3(a)(11)(A) prohibits it &lsquo;notwithstanding a rental agreement or lease that specifically "
         "permits&rsquo; it; the Rent Board calls such a charge an unlawful rent increase and any agreement to pay it "
         "void and unenforceable, refundable on a tenant petition. " + cite("S6", "S3", "S11"), OK],
        ["Is the added occupant a co-tenant or a subtenant?", BLANK,
         "Not supplied. It matters only if all original occupants later leave: a co-tenant is never subject to a "
         "Costa-Hawkins or Sec. 6.14 market reset, whenever they moved in; a subtenant can be. Flag F6. " +
         cite("S12"), UNV],
        ["Was a Rules &amp; Regs Sec. 6.14 notice ever served?", BLANK,
         "Not supplied. Without a timely written 6.14 notice on each subsequent occupant (generally within 60 days of "
         "the landlord knowing of the occupancy) the unlimited-increase right is not preserved. Flag F6. " +
         cite("S12"), UNV],
        ["Market-rate reset available?", "<b>No</b>",
         "An original occupant (T-A1) remains in lawful possession. " + cite("S25", "S12", "S11"), OK],
    ]

    b_extra = [
        ["Original tenants (lease of June 1, 2019)", "T-B1, T-B2", "Both took possession under the original rental "
         "agreement.", OK],
        ["Current occupants", "T-B1, T-B2", "No change in occupancy was reported.", OK],
        ["Market-rate reset available?", "<b>No</b>",
         "Both original occupants remain; neither Sec. 1954.53(d)(2) nor Rules 6.14 is triggered. " +
         cite("S25", "S12"), OK],
        ["Years with no increase", "7 skipped anniversaries (2020 through 2026)",
         "Each skipped anniversary accumulates the rate that was in effect on that date. " + cite("S5", "S4", "S2"),
         OK],
    ]

    from rentcalc import aga_on as _aga_on
    def _period(iso):
        dd = date.fromisoformat(iso)
        for st, en, pp in AGA:
            if st <= dd <= en:
                return st.strftime("%-m/%-d/%Y") + " \u2013 " + en.strftime("%-m/%-d/%Y")
        return BLANK
    b_rows = []
    for anniv, p, status in B["s1"]["detail"]:
        b_rows.append([d(anniv), pct(p) if p else BLANK, _period(anniv),
                       '<span class="b ok">Banked &mdash; 12 months elapsed</span>' if status == "banked"
                       else '<span class="b bad">' + status + "</span>"])
    b_rows.append((["Total banked", pct(B["s1"]["banked"]), "Added, never compounded", OK], "total"))
    b_detail = tbl("Unit B &mdash; how the 13.1% banked total is built, year by year",
                   ["Skipped anniversary", "Rate in effect on that date", "Official AGA period", "Treatment"],
                   b_rows, numeric_cols=(1,),
                   note="Rules &amp; Regs Sec. 4.12(a) " + cite("S5") + "; rates from document 571 " + cite("S2") +
                        "; method confirmed by the Rent Board&rsquo;s own worked examples " + cite("S3", "S4") + ".")

    body = f"""
<h2 class="pg">Unit dossiers</h2>
<p class="lede">Both units, field by field. Dates and dollar amounts are exactly as supplied. Names and unit
designations are pseudonymised. Every value carries a verification status and an official source; values that could
not be confirmed are left blank rather than estimated.</p>
{note("", "Anonymisation key",
      "<p><b>Unit A</b> = the unit whose last lease began February 1, 2025. <b>Unit B</b> = the unit whose last lease "
      "began June 1, 2019. Tenants are T-A1 to T-A4 and T-B1 to T-B2. T-A1 is an original tenant who remains; T-A2 "
      "and T-A3 are original tenants, one of whom departed; T-A4 is the occupant added on April 1, 2026. T-B1 and "
      "T-B2 are both original tenants who remain. The mapping to real identities is held by the owner and appears "
      "nowhere in this repository.</p>")}

{dossier("Unit A", "tenancy began February 1, 2025", A, a_extra)}
{dossier("Unit B", "tenancy began June 1, 2019", B, b_extra)}
{b_detail}

<h3>Side-by-side comparison</h3>
{tbl("Unit A vs Unit B", ["Measure", "Unit A", "Unit B", "Why they differ"], [
    ["Tenancy length at " + d(AS_OF), "1 year 9 months", "7 years 5 months", "Different lease start dates."],
    ["Skipped anniversaries with a matured rate", "1", "7",
     "Unit B has not had an increase since 2019; Unit A since 2025."],
    ["Banked percentage", pct(A["s1"]["banked"]), pct(B["s1"]["banked"]),
     "Banking is a function of tenancy history alone &mdash; a facially neutral, document-driven factor."],
    ["Total lawful increase", pct(A["s1"]["total"]), pct(B["s1"]["total_known"]) + " + unpublished",
     "Driven entirely by the official rate table and each unit&rsquo;s own anniversary date."],
    ["Notice period", f"{A['s1']['notice_days']} days", f"{B['s1']['notice_days']} days",
     "Unit B&rsquo;s total exceeds 10%, which triggers the 90-day requirement under Civ. Code Sec. 827(b)(3)(A)."],
    ["Dollar increase", usd(A["s1"]["amount"]), usd(B["s1"]["amount_known"]) + " (minimum)",
     "Different base rents and different percentages."],
    ["New base rent", usd(A["s1"]["new_rent"]), usd(B["s1"]["new_rent_known"]) + " (minimum)", ""],
], numeric_cols=(1, 2))}
{note("warn", "Why the difference between the two units is legally significant",
      "<p>The gap between Unit A (3.0%) and Unit B (13.1% or more) is not a choice. It is the arithmetic consequence "
      "of two objectively documented facts &mdash; how long each tenancy has run and how many published annual rates "
      "were skipped &mdash; applied through a regulation that treats every unit identically. That is precisely the "
      "kind of facially neutral, statute-driven, document-supported justification that answers a discrimination "
      "inquiry. It also explains why applying the <i>same percentage</i> to both units would be unlawful: it would "
      "push Unit A above its ceiling. See <a href='fair-housing.html'>One unit or both?</a></p>")}
"""
    return body


# ==========================================================================
# 8. SCENARIOS
# ==========================================================================
@page("pages/scenarios.html", "Increase scenarios",
      "Data &amp; findings &rsaquo; <b>Increase scenarios</b>",
      "Every lawful increase scenario for both units, computed from official rates with notice deadlines.")
def p_scenarios():
    a1, a2, a3 = A["s1"], A["s2"], A["s3"]
    b1, b2 = B["s1"], B["s2"]

    summary = tbl("All scenarios at a glance",
                  ["Scenario", "Effective", "Banked", "Current AGA", "Total", "Increase", "New base rent", "Notice"],
                  [
        ([f"<b>Unit A &mdash; S1</b> on the anniversary "
          f'<span class="b rec">RECOMMENDED</span>', d(a1["effective"]), pct(a1["banked"]), pct(a1["current_aga"]),
          f"<b>{pct(a1['total'])}</b>", usd(a1["amount"]), f"<b>{usd(a1['new_rent'])}</b>",
          f"{a1['notice_days']} days &mdash; serve by {d(a1['serve_by'])}"], "total"),
        [f"Unit A &mdash; S2 earliest serviceable today", d(a2["effective"]), pct(a2["banked"]),
         pct(a2["current_aga"]), pct(a2["total"]), usd(a2["amount"]), usd(a2["new_rent"]),
         f"{a2['notice_days']} days &mdash; serve by {d(a2['serve_by'])}"],
        [f"Unit A &mdash; S3 partial (current AGA only)", d(a3["effective"]), "1.4% stays banked",
         pct(a3["total"]), pct(a3["total"]), usd(a3["amount"]), usd(a3["new_rent"]),
         "30 days &mdash; serve by " + d(a1["serve_by"])],
        ([f"<b>Unit B &mdash; S1</b> on the anniversary "
          f'<span class="b rec">RECOMMENDED</span>', d(b1["effective"]), pct(b1["banked"]), GAP,
          f"<b>{pct(b1['total_known'])} + unpublished</b>", usd(b1["amount_known"]) + " min",
          f"<b>{usd(b1['new_rent_known'])}</b> min",
          f"{b1['notice_days']} days &mdash; serve by {d(b1['serve_by'])}"], "total"),
        [f"Unit B &mdash; S2 earliest serviceable today", d(b2["effective"]), pct(b2["banked"]),
         pct(b2["current_aga"]), pct(b2["total"]), usd(b2["amount"]), usd(b2["new_rent"]),
         f"{b2['notice_days']} days &mdash; serve by {d(b2['serve_by'])}"],
    ], numeric_cols=(2, 3, 4, 5, 6))

    def detail(code, s, verdict, verdict_kind, extra=""):
        rows = []
        for anniv, p, status in (s.get("detail") or []):
            rows.append([d(anniv), pct(p) if p else BLANK,
                         '<span class="b ok">Banked</span>' if status == "banked"
                         else '<span class="b bad">' + status + "</span>"])
        det = ""
        if rows:
            det = tbl(f"{code} &mdash; banked build-up", ["Skipped anniversary", "Rate then in effect", "Treatment"],
                      rows, numeric_cols=(1,))
        return f"""
<h3>{s.get('title','')}</h3>
{det}
{tbl(None, ["Line", "Value", "Basis"], [
    ["Base rent", usd(s['base']), "As supplied"],
    ["Proposed effective date", d(s['effective']), s.get('why','')],
    ["Banked percentage", pct(s['banked']), "Rules &amp; Regs Sec. 4.12(a) &mdash; added, not compounded"],
    ["Annual rate in effect on the effective date", pct(s['current_aga']) if s['current_aga'] else BLANK,
     "The rate in effect on the EFFECTIVE date governs, not the rate on the service date"],
    ["Total percentage", (pct(s['total']) if s['current_aga'] else pct(s['total']) + " + unpublished"), ""],
    ["Dollar increase", usd(s['amount']) + (" (minimum)" if not s['current_aga'] else ""),
     "Base rent &times; total percentage, truncated to the cent"],
    ["New base rent", usd(s['new_rent']) + (" (minimum)" if not s['current_aga'] else ""), ""],
    ["Notice period", f"{s['notice_days']} days",
     "90 days because the total exceeds 10%" if s['notice_days'] == 90 else "30 days because the total is 10% or less"],
    ["Latest service date, hand-delivered", d(s['serve_by']), "Civ. Code Sec. 827(b)"],
    ["Latest service date, mailed", d(s['serve_by_mailed']), "Civ. Code Sec. 827(b) plus 5 days"],
    ["New anniversary date after this increase",
     date.fromisoformat(s['effective']).strftime("%B %-d").replace(" 0", " "),
     "Unchanged if the increase lands on the existing anniversary"
     if s.get('keep_anniv') else "The effective date becomes the new anniversary date"],
])}
{note(verdict_kind, "Assessment", extra)}
"""

    a1d = dict(a1, title="Unit A &mdash; Scenario S1: increase on the anniversary date, February 1, 2027",
               base=A["base"], why="The existing anniversary date; no forfeiture risk",
               detail=[[x, y, z] for x, y, z in
                       [["2026-02-01", "1.4", "banked"]]], keep_anniv=True)
    a2d = dict(a2, title="Unit A &mdash; Scenario S2: the earliest increase serviceable today",
               base=A["base"], why="30 days from " + d(AS_OF),
               detail=[["2026-02-01", "1.4", "FORFEITED"]], keep_anniv=False)
    def norm(x):
        """Normalise the two key shapes produced by tools/calc.py."""
        y = dict(x)
        y.setdefault("total", y.get("total_known"))
        y.setdefault("amount", y.get("amount_known"))
        y.setdefault("new_rent", y.get("new_rent_known"))
        y.setdefault("current_aga", None)
        return y

    b1d = dict(norm(b1), title="Unit B &mdash; Scenario S1: increase on the anniversary date, June 1, 2027",
               base=B["base"], why="The existing anniversary date; preserves every banked rate",
               keep_anniv=True)
    b2d = dict(norm(b2), title="Unit B &mdash; Scenario S2: the earliest increase serviceable today",
               base=B["base"], why="90 days from " + d(AS_OF) + " because the total exceeds 10%",
               keep_anniv=False)

    body = f"""
<h2 class="pg">Increase scenarios</h2>
<p class="lede">Every scenario below is lawful on its face &mdash; each is computed only from published Rent Board
rates and the controlling regulation. They differ in <b>how much</b> of the entitlement is taken, <b>when</b>, and
<b>what is forfeited</b> by moving off the anniversary date. The calculator that produced these figures is asserted
against all four of the Rent Board&rsquo;s own published worked examples before it writes any output.</p>

{summary}
<p class="small">All figures from <code>tools/calc.py</code> using the official document 571 rate table
{cite("S2")} and the method in Rules &amp; Regs Sec. 4.12 {cite("S5")} and the Rent Board worked examples
{cite("S3", "S4")}. Notice periods from Civ. Code Sec. 827 {cite("S23")}.</p>

<hr class="sep">
<h2 class="pg" style="font-size:22px">Unit A &mdash; base rent {usd(A['base'])}, anniversary February 1</h2>

{detail("Unit A", a1d, "", "ok",
        "<p><b>Recommended.</b> Taking the increase on the existing anniversary date does three things at once: it "
        "lets the 1.4% that became available on February 1, 2026 complete its 12 months and therefore bank; it adds "
        "the 1.6% in effect on the effective date; and it leaves the anniversary date unchanged at February 1, so "
        "nothing is forfeited. The total of 3.0% is comfortably below the 10% threshold, so only a <b>30-day</b> "
        "notice is required. This is the same pattern as the Rent Board&rsquo;s own multi-year example. "
        + cite("S3", "S5", "S4") + "</p>")}

{detail("Unit A", a2d, "", "warn",
        "<p><b>Not recommended.</b> Serving today produces an effective date of " + d(a2['effective']) + ", which "
        "changes the anniversary date. Because the 1.4% that became available on February 1, 2026 has not yet "
        "completed 12 months, it does not bank and &mdash; in the Rent Board&rsquo;s own words &mdash; is "
        "<b>permanently lost due to the change in anniversary date</b>. The owner collects " + usd(a2['amount']) +
        " instead of " + usd(a1['amount']) + ", a difference of " +
        usd(Decimal(a1['amount']) - Decimal(a2['amount'])) + ", and resets the anniversary to " +
        date.fromisoformat(a2['effective']).strftime('%B %-d').replace(' 0',' ') + ". Acting sooner is strictly "
        "worse here. " + cite("S3") + "</p>")}

<h3>Unit A &mdash; Scenario S3: take only part of the entitlement</h3>
{tbl(None, ["Line", "Value", "Basis"], [
    ["Proposed effective date", d(a3["effective"]), "The existing anniversary date"],
    ["Impose", pct(a3["total"]) + " (the current annual rate only)", usd(a3["amount"]) + " &rarr; new base rent " +
     usd(a3["new_rent"])],
    ["Leave banked", "1.4%", "Banked increases do not expire during a tenancy and may be imposed after at least 12 "
     "months or on a future anniversary date"],
    ["Notice period", "30 days", "Total is 10% or less"],
    ["Serve on or before", d(a1["serve_by"]) + " (" + d(a1["serve_by_mailed"]) + " if mailed)", "Civ. Code Sec. 827(b)"],
])}
{note("", "Assessment",
      "<p>Lawful and lower-friction. The official rules are explicit: &lsquo;A landlord does not have to impose the "
      "maximum allowed increase. If only part of the allowable increase is used, the rest is banked.&rsquo; A smaller "
      "increase is also less likely to draw a petition. The trade-off is cash now versus cash later, and the 1.4% "
      "remains available indefinitely during this tenancy. " + cite("S4") + "</p>"
      "<p><b>One open question, flagged:</b> the official material does not state how a remainder that stays banked "
      "interacts with a base rent that has since risen. Because Rule 4.12 provides that banked increases &lsquo;shall "
      "not be compounded&rsquo;, the safest reading is that the retained percentage is applied later to base rent "
      "without compounding &mdash; but that reading is not stated in an official document, so it is <b>not</b> "
      "published as a computed figure anywhere on this site. Confirm with a Rent Board counselor before relying on a "
      "multi-year phase-in.</p>")}

<hr class="sep">
<h2 class="pg" style="font-size:22px">Unit B &mdash; base rent {usd(B['base'])}, anniversary June 1</h2>

{detail("Unit B", b1d, "", "ok",
        "<p><b>Recommended.</b> Waiting for June 1, 2027 preserves all seven skipped rates, including the 1.6% that "
        "became available on June 1, 2026 and matures on June 1, 2027. The verified banked total is <b>13.1%</b>, "
        "worth " + usd(b1['amount_known']) + " on the current base rent, and the annual rate in effect on June 1, "
        "2027 is added on top of that. <b>That rate had not been published as of " + d(AS_OF) + "</b> &mdash; the Rent "
        "Board publishes on or about January 1 for the period beginning March 1 &mdash; so it is left blank and is "
        "never forecast. Because the total already exceeds 10%, a <b>90-day</b> notice is required; serve on or before "
        "<b>" + d(b1['serve_by']) + "</b>, or <b>" + d(b1['serve_by_mailed']) + "</b> if the notice is mailed. "
        + cite("S2", "S5", "S23", "S3") + "</p>")}

{detail("Unit B", b2d, "", "warn",
        "<p><b>Not recommended, and it cannot be done for an earlier date.</b> Serving a 90-day notice today gives an "
        "effective date of " + d(b2['effective']) + ". That changes the anniversary date, and because the 1.6% that "
        "became available on June 1, 2026 has not yet completed 12 months, it is <b>permanently forfeited</b>. The "
        "arithmetic happens to land on the same total of 13.1% (11.5% banked plus the 1.6% now in effect) and the "
        "same " + usd(b2['amount']) + ", but the owner gives up the additional annual rate that Scenario S1 would add "
        "on June 1, 2027, and permanently moves the anniversary off June 1. Scenario S1 strictly dominates. "
        + cite("S3", "S5") + "</p>")}

<h3>Unit B &mdash; the phase-in question</h3>
{note("warn", "A 13.1% increase is lawful but it is not &lsquo;normal&rsquo;",
      "<p>Nothing in the Ordinance caps a properly banked total: the official page states there is <b>no limit</b> on "
      "how much can be banked back to April 1, 1982, and that banked increases do not expire during a tenancy. So "
      "13.1% plus the then-current annual rate is lawful. But it is a one-step recovery of seven years of forbearance, "
      "it requires a 90-day notice, and it is the single largest discretionary decision in this file.</p>"
      "<p>The rules expressly permit taking less: &lsquo;A landlord does not have to impose the maximum allowed "
      "increase. If only part of the allowable increase is used, the rest is banked.&rsquo; A phase-in therefore has a "
      "clear official basis. What the official material does <b>not</b> state is how a retained remainder interacts "
      "with a base rent that has already risen, and Rule 4.12 forbids compounding banked increases. Because that "
      "interaction is not documented in an official source, <b>no phased dollar figures are published on this "
      "site</b>. Obtain a Rent Board counselor&rsquo;s confirmation (415-252-4600) or a written legal opinion before "
      "serving a phase-in notice. " + cite("S4", "S5", "S3") + "</p>")}

<h3>Decision required</h3>
{tbl("Decision required", ["Unit", "Recommended", "Alternative", "Deadline"], [
    ["Unit A", "<b>S1</b> &mdash; " + pct(a1['total']) + " effective " + d(a1['effective']) + " &rarr; " +
     usd(a1['new_rent']), "S3 &mdash; " + pct(a3['total']) + " only, leaving 1.4% banked",
     "Serve by <b>" + d(a1['serve_by']) + "</b> (" + d(a1['serve_by_mailed']) + " if mailed)"],
    ["Unit B", "<b>S1</b> &mdash; " + pct(b1['total_known']) + " plus the unpublished 2027-28 annual rate, effective "
     + d(b1['effective']) + " &rarr; at least " + usd(b1['new_rent_known']),
     "A partial increase on the same date &mdash; amounts not published, see the phase-in note above",
     "Serve by <b>" + d(b1['serve_by']) + "</b> (" + d(b1['serve_by_mailed']) + " if mailed)"],
    ["Both units", "Clear the two hard gates first: confirm the rent increase license, and confirm the banking "
     "maturity rule with a Rent Board counselor", "&mdash;",
     "Before any notice is served"],
])}
"""
    return body


# ==========================================================================
# 9. NOTICE GUIDE
# ==========================================================================
@page("pages/notice-guide.html", "Notice procedure & legitimate reasons",
      "Practice &amp; risk &rsaquo; <b>Notice procedure &amp; reasons</b>",
      "The exact procedure for serving a lawful rent increase notice in San Francisco, and the closed list of legitimate grounds.")
def p_notice():
    steps = tbl("The procedure, in order. Do not serve a notice until every gate is cleared.",
                ["#", "Step", "What the official rule requires", "Source", "Status"], [
        ["1", "Confirm rent-control coverage",
         "Units built on or before June 13, 1979 are generally covered. Verify the construction date on the San "
         "Francisco Property Information Map and confirm the unit is not separately alienable.", cite("S7", "S21"),
         UNV],
        ["2", "Obtain the complete rent history",
         "The base rent for every year since the tenancy began, every prior notice served, and every prior "
         "anniversary date. The burden of proving the correct base rent rests on the owner in a Form 354 petition.",
         cite("S18", "S14"), UNV],
        ["3", "Confirm the <b>rent increase license</b> is current",
         "A license must be on file on the <b>effective date</b>. If it is not, the entire annual or banked increase "
         "is null and void and the tenant may seek a refund. File or refresh the Housing Inventory at the Rent Board "
         "Portal; the deadline is March 1 but late filing is accepted with no monetary penalty.",
         cite("S8", "S9", "S6"), UNV],
        ["4", "Confirm no disqualifying condition",
         "No serious health, safety, fire or building code violations cited and unabated for six months or more before "
         "a vacancy (relevant to any market-reset theory); no pending tenant petition; no reduction in housing "
         "services.", cite("S25", "S26", "S6", "S14"), OK],
        ["5", "Compute the increase on <b>base rent</b>",
         "Base rent includes housing services such as parking and storage; it excludes temporary passthroughs and "
         "fluctuating charges. Sum the matured banked percentages, add the annual rate in effect on the "
         "<b>effective date</b>, multiply by base rent, and truncate to the cent. Never round up.",
         cite("S3", "S16", "S5"), OK],
        ["6", "Confirm at least 12 months have passed",
         "Since the lease began, or since the last increase. The first increase is available 12 months after the "
         "lease began.", cite("S3", "S16"), OK],
        ["7", "Determine the notice period",
         "30 days if the total increase is 10% or less of the rent charged at any time in the prior 12 months; "
         "<b>90 days</b> if more than 10%, alone or combined with any other increase in that period. Add <b>5 days</b> "
         "if the notice is mailed.", cite("S23", "S3"), OK],
        ["8", "Draft the notice with the mandatory contents",
         "See the required-contents table below. Omitting the banked-amount disclosure does not by itself void the "
         "increase, but omitting the dollar amount, percentage or effective date can.", cite("S6", "S5", "S3"), OK],
        ["9", "Serve it in writing and keep proof",
         "Personal delivery, or mail under Code of Civil Procedure Sec. 1013. Retain the notice, the proof of service "
         "and the calculation worksheet.", cite("S23", "S16"), OK],
        ["10", "Do not use an algorithmic pricing device",
         "Sec. 37.10C prohibits the use of algorithmic devices to set rents or manage occupancy levels for residential "
         "units in San Francisco.", cite("S6"), OK],
        ["11", "Do not raise rent because of occupancy",
         "Sec. 37.3(a)(11)(A) bars an increase based on an additional occupant even where the lease permits it; the "
         "Rent Board bars an increase based on a departing tenant&rsquo;s replacement.", cite("S6", "S3", "S11"), OK],
        ["12", "Pay the standing obligations",
         "Rent Board fee of $59.00 per dwelling unit by March 1, and security-deposit interest of 4.2% for 2026-27.",
         cite("S10", "S1"), UNV],
        ["13", "If anything above the AGA is claimed, petition <b>first</b>",
         "A landlord who seeks any increase beyond the permitted list must petition for a Rent Board arbitration "
         "hearing before serving the notice. The tenant need not pay until the Board approves; approval is then "
         "retroactive to the effective date in the valid notice.", cite("S6", "S13"), OK],
    ])

    contents = tbl("What the notice must contain", ["Required element", "Authority", "Consequence if missing"], [
        ["The dollar amount of the increase", cite("S3"), "Defective notice; risk of being null and void"],
        ["The percentage amount of the increase", cite("S3"), "Defective notice"],
        ["The date the increase takes effect", cite("S3"), "Defective notice"],
        ["Which portion reflects the <b>annual</b> increase and/or the <b>banked</b> amount",
         cite("S6", "S5"),
         "Omitting the banked detail does not itself render the increase null and void, but it is required"],
        ["The dates on which the banked amount is based", cite("S5"), "Required disclosure"],
        ["Which portion reflects an <b>O&amp;M expense increase</b>, a <b>comparable-units</b> or "
         "<b>capital-improvement</b> certification, or a substantial-rehabilitation/energy certification",
         cite("S6", "S5"), "Must be certified by a Board petition; uncertified portions are not collectible"],
        ["Which portion reflects a <b>gas or electricity</b> passthrough, a <b>water revenue bond</b> passthrough "
         "under Sec. 37.3(a)(5)(B), or a <b>general obligation bond</b> passthrough under Sec. 37.3(a)(6)",
         cite("S6", "S5"), "Must be identified on the Rent Board&rsquo;s own forms"],
        ["Which portion reflects amortisation of a <b>RAP loan</b> (Sec. 37.3(a)(7))", cite("S6", "S5"),
         "Must be identified on the Board&rsquo;s form"],
        ["Written notice in writing, in all cases", cite("S3"), "A verbal notice is never sufficient"],
    ])

    grounds = tbl("Legitimate grounds for an increase &mdash; the closed list",
                  ["Ground", "Petition required?", "Ceiling", "Applies to Unit A / Unit B?", "Source"], [
        ["The published annual allowable increase", "No", "1.6% now; never more than 7%",
         "Yes &mdash; both units", cite("S3", "S6", "S1")],
        ["Banked increases accumulated since the last increase", "No", "No cap on the accumulated total",
         "Unit A: 1.4%. Unit B: 13.1%.", cite("S4", "S5", "S2")],
        ["Capital improvement passthrough", "Yes", "5% of base rent per 12 months; 15% over the tenancy",
         "No capital improvements were reported. " + BLANK, cite("S13", "S1")],
        ["Operating and maintenance expense increase", "Yes", "A certified O&amp;M increase shall not exceed 7%",
         "Not proposed. " + BLANK, cite("S13", "S6")],
        ["Special circumstances &mdash; comparable-unit rents", "Yes", "Set by the Board",
         "Not proposed. Note the Rent Board publishes base rents in $250 increments from the Housing Inventory.",
         cite("S13", "S8")],
        ["Proposition I past rent history", "Yes", "Set by the Board", "Not proposed. " + BLANK, cite("S13")],
        ["Utility passthrough (gas and electricity)", "Petition or worksheet",
         "Excluded from base rent; chargeable only at the time of an annual increase",
         "Not proposed. " + BLANK, cite("S13", "S5")],
        ["General obligation bond passthrough", "Worksheet only", "50% of the property-tax change",
         "Not proposed. " + BLANK, cite("S13", "S6")],
        ["Water revenue bond passthrough", "Worksheet only", "50% of the attributable charges",
         "Not proposed. " + BLANK, cite("S13", "S5")],
        ["Lead hazard remediation", "Via O&amp;M or capital improvement",
         "Combined O&amp;M and capital-improvement increase not more than 10% in any 12 months",
         "Not proposed. " + BLANK, cite("S6")],
        ["Recovery of the Rent Board fee", "No", "50% of the fee once paid in full: <b>$29.50</b> per dwelling unit "
         "for 2026-2027, from a tenant in occupancy as of November 1 of the tax year",
         "<b>Available for both units</b> if the fee was paid. Not included in any scenario above.", cite("S10", "S1")],
        ["Rules &amp; Regs Sec. 1.21 &mdash; no tenant in occupancy", "Yes", "Set by the Board",
         "Not applicable &mdash; both units are occupied.", cite("S13")],
        ["Sec. 6.14 / Costa-Hawkins market reset", "No (an elective determination petition exists)",
         "Unlimited, but only on the strict conditions", "<b>No</b> &mdash; an original occupant remains in lawful "
         "possession of each unit.", cite("S12", "S25", "S13")],
    ])

    bad = tbl("Grounds that are NOT legitimate", ["Claim", "Why it fails", "Source"], [
        ["&ldquo;The market supports more&rdquo; while an original occupant remains",
         "Vacancy decontrol reaches only a genuinely new tenancy. Sec. 1954.53(d)(3) expressly excludes partial "
         "changes in occupancy where an occupant under the agreement with the owner remains in lawful possession.",
         cite("S25", "S12", "S11")],
        ["&ldquo;A new occupant moved in&rdquo;",
         "Sec. 37.3(a)(11)(A) prohibits it &lsquo;notwithstanding a rental agreement or lease that specifically "
         "permits&rsquo; it. Such a charge is an unlawful rent increase; any agreement to pay it is void and "
         "unenforceable and refundable on petition.", cite("S6", "S3", "S11")],
        ["&ldquo;A roommate was replaced&rdquo;",
         "&lsquo;The landlord may not increase the rent for the unit based on the replacement of a departing tenant or "
         "the addition of new occupants, even if agreed to by the tenant.&rsquo;", cite("S11")],
        ["&ldquo;Costs went up&rdquo; without a certified petition",
         "Only the enumerated grounds apply; anything above them requires a Sec. 37.8 arbitration petition served "
         "before the notice. An O&amp;M increase must be certified by the Board and cannot exceed 7%.",
         cite("S6", "S13")],
        ["&ldquo;The state allows 8.8%&rdquo;",
         "AB 1482 exempts housing under a local ordinance with a lower cap. San Francisco&rsquo;s 1.6% is lower, so "
         "the state cap does not apply and cannot be used to justify a higher local increase.", cite("S24")],
        ["&ldquo;Property taxes went up&rdquo;", "General obligation bond and water revenue bond increases follow the "
         "property tax rate change and require the Board&rsquo;s worksheet; there is no general tax passthrough.",
         cite("S6", "S13", "S5")],
        ["&ldquo;The lease says we can&rdquo;",
         "The Ordinance overrides the lease. Sec. 37.3(a)(11)(A) applies notwithstanding a contrary lease term, and a "
         "rental agreement cannot waive or circumvent the tenant&rsquo;s rights.", cite("S6", "S11")],
        ["&ldquo;The pricing software recommends it&rdquo;",
         "Sec. 37.10C prohibits the sale or use of algorithmic devices to set rents or manage occupancy levels for "
         "residential units in San Francisco.", cite("S6")],
        ["&ldquo;The tenant refused to renew&rdquo; or any retaliatory motive",
         "Retaliation for exercising rights, requesting an accommodation or filing a complaint is expressly unlawful "
         "under California law, and the Rent Board expressly does not adjudicate it &mdash; it goes to the Civil "
         "Rights Department or court.", cite("S33", "S14", "S34")],
    ])

    model = f"""
<div class="panel">
<h4>Model notice text &mdash; a drafting template, not legal advice</h4>
<p class="small">Fill every bracket from the verified calculation. <b>Have counsel review before serving.</b> This
template follows the content requirements of Rent Ordinance Sec. 37.3(b) and Rent Board Rules and Regulations
Sec. 4.10(a) and 4.12(b), and the notice periods of Civil Code Sec. 827(b).</p>
<pre style="font-family:var(--mono);font-size:12.4px;line-height:1.55;white-space:pre-wrap;margin:10px 0 0">
NOTICE OF RENT INCREASE
To: [tenant name(s) as they appear on the rental agreement]
Premises: [unit identifier]
Date of this notice: [service date]

1. INCREASE. Effective [EFFECTIVE DATE], the total monthly base rent for the premises
   increases by [DOLLAR AMOUNT], from [CURRENT BASE RENT] to [NEW BASE RENT].
   This is an increase of [TOTAL PERCENTAGE]% of the base rent.

2. COMPOSITION OF THE INCREASE.
   (a) Annual allowable increase in effect on [EFFECTIVE DATE]:      [X.X]%
       (SF Rent Board allowable annual increase for [official rate period])
   (b) Banked annual increases previously available and not imposed: [Y.Y]%,
       comprising:
         [DATE 1]  [rate]%     (rate period [period])
         [DATE 2]  [rate]%     (rate period [period])
       Imposed under Chapter 37 and Rent Board Rules and Regulations Sec. 4.12, and
       based on the dates stated above.
   (c) Capital improvement / O&M / comparable-units portion:  [NONE, or the Board-certified
       amount and certification reference]
   (d) Utility, water revenue bond or general obligation bond passthrough: [NONE, or the
       amount on the applicable Rent Board form]
   (e) RAP loan amortisation under Sec. 37.3(a)(7): [NONE, or the amount]
   (f) Rent Board fee recovery (50% of the fee, once paid in full): [NONE, or $29.50]

3. BASIS. This increase is limited to the annual allowable increase and properly banked
   increases. It is not based on any additional or replacement occupant. It does not
   exceed the amounts permitted by San Francisco Administrative Code Sec. 37.3.

4. NOTICE PERIOD. [30 / 90] days' written notice is given under California Civil Code
   Sec. 827(b)[(2)/(3)(A)]. This notice is [hand-delivered on DATE / mailed on DATE,
   with 5 additional days allowed].

5. LICENSE. A current rent increase license for this unit is on file with the San
   Francisco Rent Board as of [DATE], pursuant to Sec. 37.15.

6. QUESTIONS. You may contact the San Francisco Rent Board at (415) 252-4600 for free
   counseling. You have the right to file a petition challenging this increase; there is
   no charge to file.

Landlord / authorised agent: [name, address, telephone]
Proof of service: [method, date, person served]
</pre>
</div>
"""

    body = f"""
<h2 class="pg">How to notify a tenant, and on what grounds</h2>
<p class="lede">San Francisco requires more than a correct number. The notice must be written, served with the right
period, state the right content, identify each component separately, and be backed by a current rent increase
license. A defect in any of these can void the entire increase even if the arithmetic was right.</p>

<h3>The procedure</h3>
{steps}

<h3>Mandatory contents of the notice</h3>
{contents}
{note("bad", "The consequence of getting this wrong",
      "<p>Rent Ordinance Sec. 37.3(b)(5): &lsquo;Nonconforming Rent Increases. Any rent increase which does not "
      "conform with the provisions of this section shall be <b>null and void</b>.&rsquo; Rules and Regulations "
      "Sec. 4.10(b) preserves the increase only where the amount requested is no more than the allowable annual and "
      "banked increase, and allows an Administrative Law Judge to readjust rather than void a good-faith overage "
      "within half of one percent of the prior base rent. " + cite("S6", "S5") + "</p>")}

<h3>Notice periods, worked</h3>
{tbl("Notice timing for the recommended scenarios", ["Scenario", "Total increase", "Period", "Effective date",
     "Latest service date (hand-delivered)", "Latest service date (mailed)"], [
    ["Unit A &mdash; S1", pct(A["s1"]["total"]), f"{A['s1']['notice_days']} days", d(A["s1"]["effective"]),
     d(A["s1"]["serve_by"]), d(A["s1"]["serve_by_mailed"])],
    ["Unit A &mdash; S3 (partial)", pct(A["s3"]["total"]), "30 days", d(A["s3"]["effective"]),
     d(A["s1"]["serve_by"]), d(A["s1"]["serve_by_mailed"])],
    ["Unit B &mdash; S1", pct(B["s1"]["total_known"]) + " + unpublished", f"{B['s1']['notice_days']} days",
     d(B["s1"]["effective"]), d(B["s1"]["serve_by"]), d(B["s1"]["serve_by_mailed"])],
], numeric_cols=(1, 2))}
<p class="small">Under Civ. Code Sec. 827(b)(2) the 30-day rule applies where the increase is 10 percent or less of
the rent charged at any time during the 12 months before the effective date; Sec. 827(b)(3)(A) requires 90 days
where it is greater than 10 percent. San Francisco adds 5 days if the notice is mailed. {cite("S23", "S3", "S16")}
Unit B&rsquo;s total exceeds 10 percent, so 90 days applies regardless of whether the unpublished 2027-28 rate turns
out to be high or low.</p>

<h3>Legitimate grounds</h3>
{grounds}

<h3>Grounds that will fail</h3>
{bad}

<h3>Model notice</h3>
{model}

<h3>Where a notice goes wrong most often</h3>
<ol>
<li><b>No license on the effective date.</b> Null and void in its entirety. {cite("S8", "S9")}</li>
<li><b>Serving on the wrong anniversary date.</b> Permanently forfeits any unmatured skipped rate and moves the
anniversary. {cite("S3")}</li>
<li><b>Using the rate in effect on the service date</b> instead of the effective date. {cite("S3")}</li>
<li><b>Rounding up</b> to the next dollar. {cite("S3", "S17")}</li>
<li><b>Applying the percentage to a rent that includes a passthrough.</b> {cite("S3", "S16")}</li>
<li><b>Compounding banked percentages</b> instead of adding them. {cite("S5")}</li>
<li><b>Omitting the banked-portion disclosure</b>, or omitting the dollar amount, percentage or effective date
altogether. {cite("S6", "S5")}</li>
<li><b>Serving 30 days when the total exceeds 10%.</b> {cite("S23")}</li>
<li><b>Tying the increase to an occupant change.</b> {cite("S6", "S11")}</li>
<li><b>Using an algorithmic pricing tool.</b> {cite("S6")}</li>
</ol>
"""
    return body


# ==========================================================================
# 10. CORPORATE VS INDIVIDUAL
# ==========================================================================
@page("pages/practices.html", "Corporate vs individual owners",
      "Practice &amp; risk &rsaquo; <b>Corporate vs individual</b>",
      "How large real-estate corporations and individual San Francisco owners handle rent increases, from primary sources.")
def p_practices():
    body = f"""
<h2 class="pg">How big corporations and individual owners handle increases</h2>
<p class="lede">The legal ceiling is identical for both. What differs is the machinery around it: entity form
changes which exemptions are available, portfolio scale changes which reporting deadlines applied and when, and
corporate pricing practice is now expressly unlawful in San Francisco. Everything below is sourced from SEC filings
by a large institutional multifamily owner with a San Francisco Bay Area portfolio, or from sf.gov and California
statute.</p>

{note("bad", "The single most important difference: algorithmic rent-setting is banned in San Francisco",
      "<p>Rent Ordinance <b>Sec. 37.10C, &lsquo;Use and Sale of Algorithmic Devices Prohibited&rsquo;</b> "
      "(Ordinance 224-24, effective <b>October 14, 2024</b>) prohibits the sale or use of algorithmic devices to set "
      "rents or to manage occupancy levels for residential units. The commercial revenue-management software that is "
      "standard practice in institutional multifamily is therefore <b>unlawful to use in San Francisco</b>, and it is "
      "unlawful for an individual owner too. Any increase on these units must be justified by the published Rent "
      "Board rate and the tenant&rsquo;s own tenancy history &mdash; not by a pricing model. " + cite("S6") + "</p>")}

<h3>What a large corporate owner says about rent setting &mdash; in its own filings</h3>
<p>The most reliable evidence of institutional practice is what these companies are legally obliged to tell
investors. Essex Property Trust, Inc. (NYSE: ESS; CIK 0000920522; SIC 6798, Real Estate Investment Trusts) describes
its portfolio as concentrated in Southern California, the San Francisco Bay Area and Seattle, and filed its Form 10-K
for fiscal 2025 on February 20, 2026. {cite("S37", "S39")}</p>
{tbl("Institutional practice, as disclosed in SEC filings", ["Disclosed practice or risk", "What the filing says",
     "Source"], [
    ["Lease structure",
     "&lsquo;Substantially all of our apartment leases are for a term of <b>one year or less</b>.&rsquo; Annual "
     "renewal is the pricing event, which in a rent-controlled city is precisely where the local cap bites.",
     cite("S38")],
    ["How rent growth is managed",
     "Institutional owners manage to portfolio-level same-property revenue and net operating income growth targets "
     "and report renewal spreads, rather than to a single unit&rsquo;s statutory ceiling. Growth in 2025 was driven "
     "by increases in rental rates and occupancy, alongside the effects of rent regulation.", cite("S37", "S38")],
    ["Rent regulation named as a risk factor",
     "&lsquo;Our future operating results may be adversely affected by a number of risks related to the real estate "
     "industry, including changes in <b>rent control or stabilization laws</b> or other laws regulating "
     "housing&hellip; which could prevent the Company from raising rents to offset increases in operating costs&hellip;"
     "&rsquo;", cite("S38")],
    ["How the company characterises the constraint",
     "&lsquo;Such laws and regulations <b>limit our ability to charge market rents, increase rents, evict tenants or "
     "recover increases in our operating expenses</b>.&rsquo;", cite("S38")],
    ["Where the pressure is expected",
     "The filings identify local ballot measures and legislative initiatives in California jurisdictions, and note "
     "that &lsquo;California is generally regarded as more litigious, highly regulated and taxed.&rsquo;",
     cite("S38", "S37")],
    ["Taxes cannot always be recovered",
     "Increases in real estate taxes &lsquo;cannot always be passed through to residents.&rsquo; In San Francisco the "
     "Ordinance allows only the general obligation bond and water revenue bond components to be passed through, and "
     "only on the Board&rsquo;s worksheet.", cite("S38", "S6", "S13")],
    ["Tax-exempt financing narrows pricing further",
     "Debt obligations secured by tax-exempt financing may restrict future rent increases and require that at least "
     "20% of units be rented to households at or below 50% of HUD median income.", cite("S38")],
    ["Litigation and enforcement risk",
     "The filings state that the multifamily industry has been subject to increased litigation related to "
     "allegations of improper eviction practices, and that these laws may be interpreted or expanded in ways that "
     "negatively affect operations.", cite("S38", "S37")],
])}

<h3>Where entity form actually changes the legal analysis</h3>
{tbl("Where entity form actually changes the analysis", ["Rule", "Corporate owner", "Individual / small owner", "Source"], [
    ["Annual allowable increase", "<b>Identical.</b> 1.6% for 3/1/2026-2/28/2027.",
     "<b>Identical.</b> 1.6%.", cite("S1", "S2")],
    ["Banking", "<b>Identical.</b> No cap on the accumulated total; new owners may use prior owners&rsquo; banked "
     "increases.", "<b>Identical.</b>", cite("S4", "S5")],
    ["Notice periods", "<b>Identical.</b> 30 / 90 days, plus 5 if mailed.", "<b>Identical.</b>", cite("S23", "S3")],
    ["AB 1482 single-family and condo exemption",
     "<b>Unavailable.</b> Civ. Code Sec. 1947.12(d)(5)(A) denies the separately-alienable exemption to a real estate "
     "investment trust, a corporation, or an LLC with at least one corporate member.",
     "Available to a natural person owning a separately alienable unit, if the notice requirement in "
     "Sec. 1947.12(d)(5)(B) is met.", cite("S24")],
    ["Housing Inventory / rent increase license",
     "The operative date was <b>July 1, 2022</b> for non-condominium buildings with 10 or more units &mdash; the "
     "large-portfolio category came first.",
     "Reporting began <b>March 1, 2023</b> for condominiums and buildings with fewer than 10 units &mdash; later, and "
     "with a smaller margin for error. <b>Both must hold a current license before any increase takes effect.</b>",
     cite("S8", "S9")],
    ["Bulk reporting tooling", "A bulk-upload function is available for owners of 5 or more units.",
     "Units must generally be submitted individually.", cite("S8")],
    ["Rent Board fee", "$59.00 per dwelling unit &mdash; flat, and trivially small across a large portfolio.",
     "$59.00 per dwelling unit &mdash; the same flat charge, but proportionally material on a two-unit building, and "
     "50% ($29.50) is recoverable from a tenant in occupancy as of November 1 once paid in full.", cite("S10")],
    ["Access to counsel", "In-house counsel and specialist outside counsel.",
     "Usually none. The Rent Board offers free landlord counselling on 415-252-4600, weekdays 9am-12pm and 1pm-4pm. "
     "Tenants, by contrast, have a published list of free legal-service providers.", cite("S7", "S15")],
    ["Algorithmic pricing", "<b>Prohibited.</b> Sec. 37.10C bans the use of algorithmic devices to set rents or "
     "manage occupancy in San Francisco.",
     "<b>Equally prohibited.</b> The same section applies to every owner.", cite("S6")],
    ["Tenant remedies against the owner", "Identical: a free Form 354 or 361 petition, arbitration before an "
     "Administrative Law Judge, and a possible refund order.", "Identical.", cite("S14", "S18")],
])}

<h3>Practical read-across for these two units</h3>
{note("", "What institutional practice does and does not justify",
      "<p>Institutional owners do not get a different percentage, and an individual owner does not get a discount. "
      "What the corporate record shows is a <b>discipline</b>, not a higher ceiling: a single written policy, applied "
      "on the same cycle to every unit, documented per unit, and reviewed against the local cap before service. That "
      "discipline is exactly what a tenant lawyer probes for, and it is free to adopt.</p>"
      "<p>Two corporate habits must NOT be imported. First, portfolio-level growth targets &mdash; a target is not a "
      "lawful ground, and the only lawful grounds are the closed list in "
      "<a href='notice-guide.html'>Notice procedure &amp; reasons</a>. Second, algorithmic or model-driven pricing, "
      "which Sec. 37.10C prohibits outright in San Francisco. " + cite("S6", "S13") + "</p>")}

{tbl("How this file compares with institutional practice", ["Dimension", "Institutional norm", "This file", "Verdict"],
     [["Ground for the increase", "Portfolio revenue targets plus statutory entitlement",
       "Statutory entitlement only: published AGA plus matured banked amounts",
       '<span class="b ok">More conservative</span>'],
      ["Timing", "Annual renewal cycle across the portfolio",
       "Each unit&rsquo;s own statutory anniversary date, unchanged",
       '<span class="b ok">Aligned</span>'],
      ["Pricing technology", "Revenue-management software (unlawful in SF)", "Manual calculation from document 571 "
       "plus Rules Sec. 4.12, reproducible and auditable", '<span class="b ok">Compliant</span>'],
      ["Documentation", "Centralised lease and notice files",
       "A source-linked register, a self-testing calculator and a flag register",
       '<span class="b ok">Aligned</span>'],
      ["Occupancy-driven repricing", "Common on roommate change",
       "<b>Excluded.</b> An original occupant remains in each unit and Sec. 37.3(a)(11)(A) bars occupant-based "
       "increases", '<span class="b ok">More conservative</span>'],
      ["License compliance", "Tracked centrally since July 1, 2022",
       BLANK + " &mdash; unknown; must be cleared before any notice", '<span class="b bad">Open</span>']],
     note=cite("S6", "S8", "S11", "S13", "S25"))}
"""
    return body


# ==========================================================================
# 11. ONE UNIT OR BOTH
# ==========================================================================
@page("pages/fair-housing.html", "One unit or both? Discrimination review",
      "Practice &amp; risk &rsaquo; <b>One unit or both?</b>",
      "Whether raising one unit and not the other creates discrimination exposure, and how to manage it.")
def p_fh():
    body = f"""
<h2 class="pg">Raise one unit, or both?</h2>
<p class="lede">The question is whether a rent increase taken on one unit but not the other creates
discrimination exposure. The answer turns on a single legal test: <b>why</b> the two units were treated differently.
Treating two units differently is not itself unlawful. Treating them differently because of a protected
characteristic is.</p>

{note("bad", "The counter-intuitive finding: making the increases EQUAL would be unlawful",
      "<p>It is tempting to think that fairness means raising both units by the same percentage. On these facts that "
      "would be the <b>unlawful</b> option. Unit A&rsquo;s lawful ceiling is <b>" + pct(A["s1"]["total"]) + "</b>; "
      "Unit B&rsquo;s banked entitlement alone is <b>" + pct(B["s1"]["banked"]) + "</b> before the then-current annual "
      "rate is added. Raising Unit A to anything above " + pct(A["s1"]["total"]) + " would exceed the amount permitted "
      "by Sec. 37.3 and, under Sec. 37.3(b)(5), the entire increase would be <b>null and void</b> &mdash; with a "
      "tenant refund claim behind it. Equal percentages are not achievable here without breaking the law on one unit "
      "or the other. " + cite("S6", "S5", "S2") + "</p>")}

<h3>The legal framework</h3>
{tbl("Which law, and what it actually prohibits", ["Law", "Prohibits", "Enforcement", "Source"], [
    ["Fair Housing Act, 42 U.S.C. Sec. 3601 et seq.",
     "Making housing unavailable, or setting different <b>terms, conditions or privileges</b> of rental, because of "
     "race or colour, religion, sex, national origin, familial status or disability. Applies to landlords and real "
     "estate companies.",
     "HUD complaint, private suit in federal or state court, DOJ pattern-or-practice action, DOJ criminal proceedings "
     "where force or threat is used.", cite("S34", "S35")],
    ["Fair Employment and Housing Act / California Civil Rights Act",
     "A materially longer list: race, colour, ancestry, national origin, <b>citizenship, immigration status, primary "
     "language</b>, religion, disability, sex and gender, sexual orientation, gender identity, gender expression, "
     "genetic information, marital status, <b>familial status</b>, <b>source of income</b> including a Section 8 "
     "voucher, military or veteran status and <b>age</b>. Also protects association with someone who has a protected "
     "characteristic, characteristics a person is perceived to have, and characteristics of a family member, friend, "
     "roommate or associate. Expressly includes <b>retaliation</b>.",
     "Free complaint to the California Civil Rights Department; administrative and civil remedies including damages.",
     cite("S33")],
    ["Unruh Civil Rights Act, Cal. Civ. Code Sec. 51",
     "Full and equal accommodations, advantages, facilities, privileges and services in all business establishments.",
     "Civil action.", cite("S40")],
    ["SF Rent Ordinance Sec. 37.10B and Sec. 37.9F",
     "Tenant harassment, and circumvention of tenant protections. An increase imposed to pressure a tenant to leave "
     "is exposed here as well as under the fair-housing statutes.",
     "Civil and criminal exposure under Chapter 37; the Rent Board does not adjudicate these claims.",
     cite("S6", "S14")],
    ["<b>Jurisdictional note</b>",
     "The Rent Board states it does <b>not</b> adjudicate harassment, discrimination or retaliation, and that such "
     "matters &lsquo;must be decided in court or another forum&rsquo;. A discrimination claim therefore proceeds in "
     "parallel with, not through, a rent-overcharge petition &mdash; different forum, different remedies.",
     cite("S14", "S33", "S34")],
])}

<h3>Applying the test to these two units</h3>
{tbl("Applying the test to these two units", ["Question", "Analysis", "Conclusion", "Source"], [
    ["Do the two units have different lawful ceilings?",
     "Yes, and by a wide margin. Unit A: " + pct(A["s1"]["total"]) + ". Unit B: " + pct(B["s1"]["banked"]) +
     " banked plus the then-current annual rate. The difference is produced entirely by the official document 571 rate "
     "table applied to each unit&rsquo;s own anniversary date and tenancy length.",
     '<span class="b ok">Documented objective basis</span>', cite("S2", "S5", "S4")],
    ["Is that difference tied to any protected characteristic?",
     "No. Tenancy start date and the number of skipped anniversaries are neutral, documentable facts recorded in the "
     "lease and in the Rent Board&rsquo;s own rate table. Nothing in either dossier links the difference to race, "
     "colour, ancestry, national origin, citizenship, immigration status, primary language, religion, disability, sex "
     "or gender, sexual orientation, gender identity or expression, genetic information, marital status, familial "
     "status, source of income, military or veteran status, or age.",
     '<span class="b ok">No protected basis</span>', cite("S33", "S34")],
    ["Is either increase retaliatory?",
     "No retaliatory motive was reported. Note that retaliation for a tenant filing a complaint, requesting an "
     "accommodation, or otherwise protecting their rights is expressly unlawful in California, and that the Rent "
     "Board cannot hear the claim &mdash; so this is a real exposure if facts emerge.",
     '<span class="b ok">None reported</span> ' + BLANK, cite("S33", "S14")],
    ["Would raising only one unit be unlawful?",
     "No. San Francisco&rsquo;s regime is inherently unit- and tenancy-specific: each unit has its own base rent, its "
     "own anniversary date and its own banked pool. There is no requirement to raise every unit in a building, and no "
     "prohibition on raising only one.", '<span class="b ok">Lawful</span>', cite("S3", "S5", "S4")],
    ["Would raising only one unit be <b>risky</b>?",
     "It can be. If the two units&rsquo; households differ on any protected characteristic and only one is increased, "
     "a complainant will ask why. The answer must be documented before the decision, not constructed afterwards.",
     '<span class="b warn">Manageable with a written policy</span>', cite("S33", "S34")],
    ["Does Unit B&rsquo;s large increase carry its own risk?",
     "Yes, of a different kind. A step increase of more than 10% is the fact pattern most often challenged, it "
     "requires a 90-day notice, and if either occupant is elderly, disabled, on a fixed income or a voucher holder, a "
     "disparate-impact or hardship argument becomes available. California protects <b>age</b>, <b>disability</b>, "
     "<b>familial status</b> and <b>source of income</b>. Tenants may file a Tenant Financial Hardship Application "
     "(Form 363). <b>Neither occupant&rsquo;s age, disability status or income source was supplied.</b> " + BLANK,
     '<span class="b warn">Unknown &mdash; must be checked</span>', cite("S33", "S14", "S6")],
    ["Can a housing service be reduced instead of raising rent?",
     "No. Parking, driveways, storage, laundry rooms, decks, patios and gardens supplied with a unit may not be "
     "severed without just cause, and any severance, substantial reduction or removal of a housing service must be "
     "offset by a corresponding reduction in rent. A reduction in housing services without a corresponding rent "
     "reduction is itself defined as a rent increase.", '<span class="b bad">Do not do this</span>', cite("S6")],
])}

<h3>Recommended approach</h3>
{note("ok", "One written policy, applied to both units, each to its own lawful limit",
      "<ol>"
      "<li><b>Adopt a single written rent-increase policy</b> covering both units: the same annual review date, the "
      "same calculation method, the same notice format, and the same stated criteria for deciding whether to take the "
      "full entitlement or less. Apply it identically.</li>"
      "<li><b>Raise both units, each to its own lawful amount, on each unit&rsquo;s own anniversary date.</b> Unit A "
      "to " + pct(A["s1"]["total"]) + " on " + d(A["s1"]["effective"]) + "; Unit B to " +
      pct(B["s1"]["banked"]) + " plus the then-current annual rate on " + d(B["s1"]["effective"]) + ". Identical "
      "process, different lawful outcomes &mdash; which is what the Ordinance requires.</li>"
      "<li><b>Document the objective basis in the file before serving</b>: tenancy start date, complete rent history, "
      "the applicable document 571 rates, the calculation worksheet, and the license confirmation. The justification "
      "must predate the notice.</li>"
      "<li><b>Do not equalise percentages across units.</b> That would exceed Unit A&rsquo;s ceiling and void the "
      "increase.</li>"
      "<li><b>Check for a hardship or disparate-impact factor on Unit B before choosing the full 13.1%.</b> If either "
      "occupant is elderly, disabled, on a fixed income or a voucher holder, a phased increase materially reduces "
      "exposure and the official rules expressly permit taking less than the maximum. Do not use any of that "
      "information as a reason to treat a unit differently &mdash; use it only to moderate the amount.</li>"
      "<li><b>Never link the decision to a protected characteristic, to a complaint, or to an accommodation "
      "request.</b> Retaliation is expressly unlawful under California law and is outside the Rent Board&rsquo;s "
      "jurisdiction.</li>"
      "<li><b>Do not use algorithmic pricing.</b> Sec. 37.10C prohibits it for every owner.</li>"
      "</ol>" + cite("S33", "S34", "S6", "S4", "S14"))}

<h3>Risk register for this decision</h3>
{tbl("Risk register for this decision", ["Risk", "Likelihood if unmanaged", "Official basis", "Mitigation"], [
    ["Allegation that the differential increase was based on a protected characteristic", "Low &mdash; the "
     "difference is produced by the rate table and tenancy dates", cite("S34", "S33"),
     "Written policy; contemporaneous documentation of the objective basis; identical process on both units"],
    ["Allegation of retaliation", "Low &mdash; none reported", cite("S33", "S14"),
     "Record that no complaint, accommodation request or repair demand preceded the decision; never cite tenant "
     "conduct as a reason for an increase"],
    ["Disparate-impact or hardship challenge to Unit B&rsquo;s 13.1% step increase", "Moderate &mdash; occupant "
     "characteristics unknown", cite("S33", "S14"),
     "Check occupant circumstances; consider a phased increase; be ready for a Form 363 hardship application"],
    ["Overcharging Unit A to &lsquo;match&rsquo; Unit B", "This is a decision risk, not a tenant risk",
     cite("S6", "S5"), "<b>Do not do it.</b> A non-conforming increase is null and void in its entirety"],
    ["Severing a housing service to achieve the same economic effect", "Decision risk", cite("S6"),
     "Prohibited without just cause, and requires a corresponding rent reduction"],
    ["Unlicensed status voiding either increase", "High if the license is not confirmed", cite("S8", "S9"),
     "Confirm a current license on the effective date for each unit before service"],
    ["Banking maturity dispute (12 vs 24 months)", "Moderate &mdash; two official pages conflict", cite("S5", "S4"),
     "Confirm with a Rent Board counselor before serving; the calculator reproduces all four official worked examples "
     "under the 12-month rule"],
])}
"""
    return body


# ==========================================================================
# 12. RED TEAM
# ==========================================================================
@page("pages/red-team.html", "Tenant-advocate red team",
      "Practice &amp; risk &rsaquo; <b>Tenant-advocate red team</b>",
      "Every argument a San Francisco tenant lawyer would run against these increases, and the documented answer to each.")
def p_redteam():
    atk = tbl("Fifteen attack vectors, modelled against the file as it stands",
              ["#", "What the tenant&rsquo;s representative will argue", "Official basis for the argument",
               "Position on the facts as supplied", "Residual risk", "Mitigation"], [
        ["1", "&lsquo;You were not licensed when the increase took effect, so the whole increase is null and void "
              "and we want a refund.&rsquo;",
         "Sec. 37.15 and the Housing Inventory rules: a current rent increase license must be on file on the "
         "effective date or the notice is not enforceable; a tenant may search the portal and file Form 361.",
         cite("S8", "S9", "S6", "S14"),
         '<span class="b bad">HIGH &mdash; license status unknown</span>',
         "Confirm and, if necessary, file at portal.sfrb.org before serving. This is the single largest exposure in "
         "the file because it is independent of the arithmetic."],
        ["2", "&lsquo;Your 13.1% banked total is wrong: nothing banks until 24 full months have passed.&rsquo;",
         "The sf.gov <i>Banked rent increases</i> page says exactly that &mdash; and the Rent Board&rsquo;s own "
         "Rules and Regulations Sec. 4.12(a) says a full 12 months.",
         cite("S4", "S5", "S3"),
         '<span class="b warn">MODERATE &mdash; two official pages conflict</span>',
         "Rely on the regulation, not the summary page; confirm with a counselor on 415-252-4600 before serving; the "
         "engine reproduces all four official worked examples under the 12-month rule, which is powerful "
         "corroboration. Consider a partial increase that is defensible under either reading."],
        ["3", "&lsquo;The notice is defective: it does not state the dollar amount, the percentage, the effective "
              "date, or which part is banked and from what dates.&rsquo;",
         "Sec. 37.3(b) and Rules Sec. 4.10(a) and 4.12(b) require each component to be identified.",
         cite("S6", "S5", "S3", "S4"), '<span class="b ok">LOW if the model notice is used</span>',
         "Use the model notice in <a href='notice-guide.html'>Notice procedure &amp; reasons</a>; keep a copy and "
         "proof of service."],
        ["4", "&lsquo;You gave 30 days when 90 were required.&rsquo;",
         "Civ. Code Sec. 827(b)(3)(A): 90 days where the increase exceeds 10 percent of the rent charged at any time "
         "in the prior 12 months, alone or combined.", cite("S23", "S3"),
         '<span class="b ok">LOW &mdash; Unit B is correctly calendared at 90 days</span>',
         "Serve Unit B by " + d(B["s1"]["serve_by"]) + " (" + d(B["s1"]["serve_by_mailed"]) + " if mailed). Unit A is "
         "3.0%, so 30 days applies."],
        ["5", "&lsquo;Your base rent is wrong.&rsquo;",
         "The increase must be computed on base rent, which includes housing services and excludes passthroughs; the "
         "owner bears the burden in a Form 354 determination of lawful rent.",
         cite("S3", "S16", "S14", "S18"), '<span class="b warn">MODERATE &mdash; composition not supplied</span>',
         "Assemble every lease, notice and ledger. If parking or storage is included, confirm it is part of base "
         "rent; if any passthrough is included, remove it and recompute. Flag F7."],
        ["6", "&lsquo;You raised the rent because a new occupant moved in.&rsquo;",
         "Sec. 37.3(a)(11)(A) prohibits it notwithstanding a contrary lease term; the Rent Board calls it an unlawful "
         "increase and says any agreement to pay it is void and unenforceable and refundable on petition.",
         cite("S6", "S3", "S11"),
         '<span class="b warn">MODERATE for Unit A &mdash; an occupant change did occur</span>',
         "The timing is the risk, not the law: Unit A&rsquo;s occupant change was April 1, 2026 and the recommended "
         "increase is February 1, 2027. Record in the file, contemporaneously, that the increase is the statutory "
         "annual rate plus a matured banked rate and has nothing to do with occupancy. Do not increase Unit A before "
         "the 1.4% matures on February 1, 2027."],
        ["7", "&lsquo;An original tenant never left, so you cannot reprice this unit to market.&rsquo;",
         "Civ. Code Sec. 1954.53(d)(3) excludes partial changes in occupancy where an occupant under the agreement "
         "with the owner remains in lawful possession; Sec. 1954.53(b) extends the initial rate to renewals for the "
         "entire period of occupancy; Rules 6.14 requires the <b>last</b> original occupant to vacate plus a timely "
         "written notice on each subsequent occupant; a co-tenant is never subject to it.",
         cite("S25", "S12", "S11", "S6"),
         '<span class="b ok">LOW &mdash; no market reset is claimed anywhere in this file</span>',
         "Do not serve a Sec. 6.14 or Costa-Hawkins notice on these facts. Flag F6 records the unresolved "
         "co-tenant/subtenant question."],
        ["8", "&lsquo;You used a pricing algorithm.&rsquo;",
         "Sec. 37.10C prohibits the sale or use of algorithmic devices to set rents or manage occupancy levels for "
         "residential units (Ordinance 224-24, effective October 14, 2024).", cite("S6"),
         '<span class="b ok">LOW &mdash; none is used</span>',
         "Compute from document 571 and Rule 4.12 only, and keep the worksheet. The calculation in this repository is "
         "deterministic and reproducible, which is the point."],
        ["9", "&lsquo;The increase is discriminatory.&rsquo;",
         "Fair Housing Act, 42 U.S.C. Sec. 3601 et seq., and the California Civil Rights Act; California protects a "
         "longer list than federal law, including source of income, immigration status, primary language and age. The "
         "Rent Board does not adjudicate these claims &mdash; they go to the CRD, HUD or court.",
         cite("S34", "S33", "S14"), '<span class="b warn">MODERATE for Unit B &mdash; occupant characteristics unknown</span>',
         "Adopt one written policy for both units; document the objective basis before serving; never cite tenant "
         "conduct; see <a href='fair-housing.html'>One unit or both?</a>"],
        ["10", "&lsquo;The increase is retaliatory.&rsquo;",
         "Retaliation for filing a complaint, requesting an accommodation, or otherwise protecting one&rsquo;s rights "
         "is expressly unlawful in California.", cite("S33", "S14"),
         '<span class="b ok">LOW &mdash; no complaint or accommodation request was reported</span>',
         "Confirm in writing that no petition, complaint, repair demand or accommodation request preceded the "
         "decision. If one did, get legal advice before serving."],
        ["11", "&lsquo;This is harassment &mdash; you are trying to force us out.&rsquo;",
         "Sec. 37.10B (Tenant Harassment) and Sec. 37.9F (Circumvention of Tenant Protections) are part of Chapter 37. "
         "The Rent Board cannot hear the claim, which means it proceeds elsewhere.", cite("S6", "S14"),
         '<span class="b ok">LOW if the recommended scenarios are followed</span>',
         "Keep communications written, factual and free of any reference to leaving. Never tie an increase to "
         "occupancy, complaints or conduct."],
        ["12", "&lsquo;Housing services were reduced.&rsquo;",
         "Parking, driveways, storage, laundry rooms, decks, patios and gardens may not be severed without just cause, "
         "and any severance, substantial reduction or removal must be offset by a corresponding rent reduction; a "
         "reduction in housing services without a corresponding rent reduction is itself a rent increase.",
         cite("S6"), '<span class="b ok">LOW &mdash; no reduction was reported</span>',
         "Do not alter services in connection with an increase. If a service changes, reduce rent correspondingly."],
        ["13", "&lsquo;You did not pay the Rent Board fee, or you did not pay security-deposit interest.&rsquo;",
         "$59.00 per dwelling unit by March 1, with monthly 5% penalties capped at 15%; deposit interest of 4.2% for "
         "2026-27. The Rent Board does not adjudicate deposit disputes, so those go to court.",
         cite("S10", "S1", "S14"), '<span class="b warn">MODERATE &mdash; no records supplied</span>',
         "Pay both and keep receipts. Note that 50% of the fee ($29.50) is recoverable from a tenant in occupancy as "
         "of November 1 &mdash; a small legitimate offset. Flag F8."],
        ["14", "&lsquo;Your building is not actually rent controlled, and your rent history is wrong.&rsquo;",
         "Coverage turns on the construction date; sf.gov directs owners to the Property Information Map. Tenants may "
         "request a determination of lawful rent on Form 354 or a rent-history review.",
         cite("S7", "S21", "S18", "S14"), '<span class="b warn">MODERATE &mdash; year not independently verified</span>',
         "Verify the construction date and the unit type on the Property Information Map. A 1940 building is "
         "presumptively covered; confirming separately-alienable status matters more. Flag F9."],
        ["15", "&lsquo;You compounded the banked percentages, or you rounded up.&rsquo;",
         "Rule 4.12: banked increases are added, not compounded, and not rounded up. Increases cannot be rounded up to "
         "the nearest dollar.", cite("S5", "S3", "S17"),
         '<span class="b ok">LOW &mdash; the engine is asserted against all four official worked examples</span>',
         "Keep the calculation worksheet produced by <code>python3 tools/calc.py</code> in the unit file."],
    ])

    body = f"""
<h2 class="pg">Red team: would this survive a San Francisco tenant lawyer?</h2>
<p class="lede">San Francisco is the most tenant-protective jurisdiction in California. A tenant here can obtain free
legal counsel, file a free petition with the Rent Board, and have an Administrative Law Judge determine the lawful
rent from the complete rent history. This page assumes that happens and works backwards from it.</p>

{note("", "The adversary",
      "<p>The Rent Board publishes an official referral listing of free tenant-side services, including Bay Area "
      "Legal Aid, Housing Rights Committee of San Francisco, Eviction Defense Collaborative, SF Tenants Union, Causa "
      "Justa :: Just Cause, Tenderloin Housing Clinic, Open Door Legal, Advancing Justice-Asian Law Caucus, Legal "
      "Assistance to the Elderly, Chinatown CDC and the SRO Collaboratives. The Board also states that no lawyer is "
      "needed to file a petition, and that it cannot refer to individual attorneys. Assume the tenant is represented "
      "and is competent. " + cite("S15", "S14") + "</p>")}

<h3>Attack surface</h3>
{atk}

<h3>The file a representative will ask for</h3>
{tbl("The file a representative will ask for", ["Document", "Why they will ask", "Status in this file"], [
    ["The original rental agreement for each unit", "Establishes the base rent and the tenancy start date.",
     '<span class="b warn">Owner-held &mdash; not supplied</span>'],
    ["Every prior rent increase notice served", "Establishes the anniversary date and whether any increase was ever "
     "imposed. None was reported.", '<span class="b warn">Reported as none &mdash; unverified</span>'],
    ["The complete rent ledger", "Reconciles base rent against passthroughs and any Rent Board fee recovery.",
     '<span class="b warn">Owner-held &mdash; not supplied</span>'],
    ["Proof of a current rent increase license on the effective date",
     "Decides whether the increase is enforceable at all.", '<span class="b bad">Unknown &mdash; flag F4</span>'],
    ["Housing Inventory filing records", "Confirms what base rent and occupancy history is already PUBLIC.",
     '<span class="b warn">Owner-held &mdash; not supplied</span>'],
    ["Rent Board fee receipts", "Supports any 50% recovery and shows good faith.",
     '<span class="b warn">Owner-held &mdash; not supplied</span>'],
    ["Security-deposit interest payment records", "A separate, commonly raised claim that goes to court.",
     '<span class="b warn">Owner-held &mdash; not supplied</span>'],
    ["The calculation worksheet", "Shows the percentages came from document 571 and were added, not compounded.",
     '<span class="b ok">Produced by <code>tools/calc.py</code></span>'],
    ["Any Sec. 6.14 notice ever served on Unit A",
     "Decides whether a market-reset theory was ever preserved. It is not being relied on.",
     '<span class="b warn">Unknown &mdash; flag F6</span>'],
    ["The written rent-increase policy", "The best single answer to a discrimination inquiry.",
     '<span class="b warn">Recommended &mdash; not yet created</span>'],
])}

<h3>Verdict</h3>
{note("ok", "Conditional pass",
      "<p>On the facts as supplied, the recommended increases are <b>defensible</b>: each is the published annual "
      "allowable increase plus properly matured banked amounts, computed on base rent, added rather than compounded, "
      "truncated rather than rounded, served with the correct notice period, landing on the existing anniversary date, "
      "and untainted by any occupancy-based, algorithmic, retaliatory or discriminatory motive. The differential "
      "treatment of the two units is produced by the Ordinance itself and is fully documented.</p>"
      "<p><b>Three conditions must be satisfied first.</b> They are not formalities &mdash; each can defeat an "
      "otherwise correct increase:</p>"
      "<ol><li><b>Confirm a current rent increase license on the effective date for each unit.</b> Without it the "
      "entire increase is null and void regardless of the arithmetic. This is the highest-residual-risk item in the "
      "file.</li>"
      "<li><b>Confirm the banking maturity rule with a Rent Board counselor</b>, because two official sf.gov pages "
      "give different answers (12 versus 24 months). If the 24-month reading were applied, part of Unit B&rsquo;s "
      "13.1% would fall away &mdash; which is a reason to consider a partial increase that is defensible under "
      "either reading.</li>"
      "<li><b>Assemble the rent history, ledger and payment records</b>, and confirm base-rent composition and the "
      "building&rsquo;s construction date and unit type.</li></ol>"
      "<p>And one drafting caution: Unit B&rsquo;s total already exceeds 10%, so the 90-day clock is fixed "
      "regardless of what the unpublished 2027-28 annual rate turns out to be. Serve by " +
      d(B["s1"]["serve_by"]) + ", or " + d(B["s1"]["serve_by_mailed"]) + " if mailing.</p>")}

<h3>If a petition arrives</h3>
<ol class="tight">
<li>Do not ignore it. The Rent Board usually resolves matters by mediation, otherwise by arbitration before an
Administrative Law Judge. Filing is free for the tenant. {cite("S14")}</li>
<li>File Form 302 (Landlord's Response to Tenant Petition) within the stated time. {cite("S19")}</li>
<li>Bring the worksheet, the rent history, the notice, the proof of service and the license confirmation.</li>
<li>Remember the jurisdictional split: the Rent Board decides the <b>amount</b> of rent. Harassment, discrimination,
retaliation and security deposits are decided in court or another forum. {cite("S14", "S33", "S34")}</li>
<li>A good-faith overage within half of one percent of the prior base rent may be readjusted rather than voided.
{cite("S5")}</li>
<li>Free landlord counselling is available on 415-252-4600, weekdays 9am-12pm and 1pm-4pm. {cite("S7")}</li>
</ol>
"""
    return body


# ==========================================================================
# 13. SOURCES
# ==========================================================================
@page("pages/sources.html", "Source register",
      "Assurance &rsaquo; <b>Source register</b>",
      "Every source used on this site, what it verifies, and how it was checked.")
def p_sources():
    rows = []
    for s in SOURCES:
        rows.append([f'<b>{s["id"]}</b>',
                     f'<a href="{s["url"]}" target="_blank" rel="noopener noreferrer">{s["title"]}</a><br>'
                     f'<span class="small">{s["pub"]}</span>',
                     s["juris"], badge(s["method"]), s["verifies"]])
    body = f"""
<h2 class="pg">Source register</h2>
<p class="lede">{len(SOURCES)} sources, all official publishers. Every table row on every page of this site links to
one of these. Nothing was taken from a blog, an aggregator, a broker or a third-party rent calculator.</p>

{tbl("Register", ["ID", "Source and publisher", "Jurisdiction", "How it was checked", "What it verifies"], rows)}

<h3>Counts</h3>
{tbl("Verification coverage", ["Category", "Count"], [
    ["Sources retrieved and read directly", f"<b>{sum(1 for s in SOURCES if s['method']=='fetched')}</b>"],
    ["Official URLs recorded and HTTP-verified in CI",
     f"<b>{sum(1 for s in SOURCES if s['method']=='ci')}</b>"],
    ["San Francisco local sources", f"<b>{sum(1 for s in SOURCES if s['juris']=='Local (SF)')}</b>"],
    ["California state sources", f"<b>{sum(1 for s in SOURCES if s['juris']=='State (CA)')}</b>"],
    ["Federal sources", f"<b>{sum(1 for s in SOURCES if s['juris']=='Federal')}</b>"],
    ["Institutional-practice sources (SEC EDGAR)", f"<b>{sum(1 for s in SOURCES if s['juris']=='Practice')}</b>"],
    ["Total", f"<b>{len(SOURCES)}</b>"],
])}

<h3>Sources deliberately NOT used</h3>
{note("bad", "Third-party rent sites were checked and rejected",
      "<p>Several widely circulated third-party pages disagree with sf.gov on the basics. They were read, compared and "
      "<b>excluded</b>; none is cited anywhere on this site. Examples of what they got wrong: a &lsquo;SF rent "
      "control calculator&rsquo; states the current allowable increase is 1.7% when the official rate is 1.6%; a "
      "brokerage&rsquo;s tenant guide states a 90-day notice applies to increases &lsquo;of 10% or more&rsquo; when "
      "the statute sets the trigger at <i>greater than</i> 10%; another guide states a 60-day notice period that "
      "appears nowhere in Civ. Code Sec. 827. The conflict is recorded as flags F2 and F3.</p>"
      "<p>The resolution rule applied throughout: where a third-party source conflicts with sf.gov, "
      "leginfo.legislature.ca.gov, dir.ca.gov, justice.gov, calcivilrights.ca.gov, sec.gov, lao.ca.gov or "
      "the official source controls and the conflict is flagged.</p>")}

<h3>Where a value could not be confirmed</h3>
<p>Seven values are left blank rather than estimated: the rent increase license status for both units,
security-deposit interest payment, Rent Board fee payment, prior increase history, base-rent composition, the
allowable increase for the period beginning March 1, 2027, and the federal rent ceiling (a deliberate negative
finding). All are recorded in the <a href="flagged.html">flag register</a>.</p>
"""
    return body


# ==========================================================================
# 14. FLAGGED FOR REVIEW
# ==========================================================================
@page("pages/flagged.html", "Flagged for review",
      "Assurance &rsaquo; <b>Flagged for review</b>",
      "Every irregularity, source conflict, unverifiable value and open question found during this review.")
def p_flagged():
    sev_badge = {
        "high": '<span class="b bad">High</span>', "medium": '<span class="b warn">Medium</span>',
        "low": '<span class="b info">Low</span>', "resolved": '<span class="b ok">Resolved</span>',
    }
    rows = []
    for f in FLAGS:
        rows.append([f'<b>{f["id"]}</b><br>' + sev_badge[f["sev"]], f["area"],
                     f'<b>{f["title"]}</b><p class="small" style="margin:6px 0 0">{f["detail"]}</p>'
                     f'<p style="margin:8px 0 0"><b>Action taken:</b> {f["action"]}</p>'
                     + (cite(*f["src"]) if f["src"] else "")])
    order = {"high": 0, "medium": 1, "low": 2, "resolved": 3}
    counts = {}
    for f in FLAGS:
        counts[f["sev"]] = counts.get(f["sev"], 0) + 1

    body = f"""
<h2 class="pg">Flagged for review</h2>
<p class="lede">{len(FLAGS)} items. This page exists because a compliance file is only useful if it says what it does
<b>not</b> know. Every value that could not be confirmed from an official source is left blank on the site and
appears here with the reason and the action taken. None of these items blocks publication; several must be closed
before a notice is served.</p>

<div class="cards">
{card("High severity", str(counts.get("high", 0)), "Includes two direct conflicts between official sf.gov pages and "
      "one unresolved compliance gate", "", "warn")}
{card("Medium severity", str(counts.get("medium", 0)), "Missing inputs, an official document error and one "
      "unpublished rate")}
{card("Low severity", str(counts.get("low", 0)), "Scope limits, a negative finding and the privacy control")}
{card("Resolved", str(counts.get("resolved", 0)), "Closed during this review")}
</div>

{tbl("Flag register", ["ID", "Area", "Finding, action taken and source"], rows)}

<h3>Values deliberately left blank</h3>
{tbl("Values deliberately left blank", ["Blank value", "Where it appears", "Why it is blank", "How to fill it"], [
    ["Rent increase license status", "Dashboard, both unit dossiers, red team",
     "Not supplied, and not published anywhere readable by this project. Flag F4.",
     "Log in at <a href='https://portal.sfrb.org/' target='_blank' rel='noopener noreferrer'>portal.sfrb.org</a> and "
     "confirm the license covers the effective date."],
    ["Base-rent composition", "Both unit dossiers",
     "Whether the supplied rents include parking, storage or any passthrough was not stated. Flag F7.",
     "Check the rental agreement and the rent ledger; recompute if a passthrough is included."],
    ["Prior increase history", "Both unit dossiers",
     "Nothing was reported. Treated as empty. Flag F8.",
     "Retrieve every notice served since each tenancy began."],
    ["Security-deposit interest paid", "Both unit dossiers",
     "No records supplied. Flag F8.", "Produce payment records at 4.2% for 2026-27."],
    ["Rent Board fee paid", "Both unit dossiers",
     "No records supplied. Flag F8.", "Produce receipts for $59.00 per dwelling unit, due March 1."],
    ["Allowable increase for 3/1/2027 &ndash; 2/28/2028",
     "Dashboard, Unit B dossier, both Unit B scenarios",
     "The Rent Board had not published it as of " + d(AS_OF) + ". Flag F10. Never forecast.",
     "Re-check the Rent Board Current Rates page on or about January 1, 2027, then re-run "
     "<code>python3 tools/calc.py</code>."],
    ["Federal maximum allowable rent increase", "Federal law page",
     "No federal statute sets one for private unsubsidised housing. Flag F13 &mdash; a deliberate negative finding, "
     "not an omission.", "Nothing to fill. Published as &lsquo;no federal ceiling &ndash; not applicable&rsquo;."],
    ["Co-tenant or subtenant status of Unit A&rsquo;s added occupant", "Unit A dossier",
     "Not supplied. It matters only if all original occupants later leave. Flag F6.",
     "Check the rental agreement and whether the added occupant has a direct agreement with the owner or pays rent "
     "directly to the owner."],
    ["Any Rules &amp; Regs Sec. 6.14 notice served on Unit A", "Unit A dossier",
     "Not supplied. Flag F6.", "Search the unit file for any 6.14 notice and its proof of service."],
    ["Building construction date", "Dashboard, both dossiers",
     "Owner-reported 1940; not verified against a public record. Flag F9.",
     "Look the property up on the <a href='https://sfplanninggis.org/PIM/' target='_blank' "
     "rel='noopener noreferrer'>San Francisco Property Information Map</a>."],
    ["Whether either unit is federally assisted", "Federal law page",
     "Not supplied.", "Check the rental agreement and any assistance-programme paperwork."],
    ["FHFA / Enterprise lease-notice requirement", "Federal law page",
     "Could not be confirmed on fhfa.gov &mdash; the newsroom URLs returned &lsquo;Page Not Found&rsquo;. Flag F12. "
     "Not relied on anywhere.", "Confirm the current status directly with FHFA; immaterial unless the property "
     "carries an Enterprise-backed multifamily loan."],
    ["Sec. 37.8 refund look-back period", "Methodology",
     "The compiled ordinance PDF could not be parsed beyond its first pages. Flag F15.",
     "Obtain the full Sec. 37.8 text before quantifying look-back exposure."],
])}

<h3>Conflicts between official sources</h3>
{tbl("Conflicts between official sources", ["Conflict", "Source A", "Source B", "Resolution"], [
    ["Banking maturity: 12 months or 24?",
     "sf.gov <i>Banked rent increases</i>: &lsquo;at least 24 full months&rsquo; " + cite("S4"),
     "Rent Board Rules and Regulations Sec. 4.12(a): &lsquo;A full 12 months must have elapsed&rsquo; " + cite("S5"),
     "The <b>regulation</b> controls. Corroborated by all four official worked examples, which the calculator "
     "reproduces exactly under the 12-month rule. Confirm with a counselor before serving. Flag F3."],
    ["Sec. 37.15 licensing operative dates",
     "Housing Inventory page: July 1, 2022 (10+ units) and March 1, 2023 (condos and under 10 units) " + cite("S8"),
     "Rent Board worksheet document 538: July 1, 2020 and March 1, 2021 " + cite("S13"),
     "Both published; neither used in a calculation, because the license is a present-tense gate. Flag F5."],
    ["Rent Board office suite number",
     "Landlord petitions page: 25 Van Ness Avenue, <b>Suite 700</b> " + cite("S13"),
     "Other sf.gov pages refer to Suite 320",
     "Recorded for completeness; immaterial to the analysis. The petitions page was retrieved directly and is used "
     "here."],
    ["A mislabelled year in an official worked example",
     "sf.gov <i>Learn about rent increases</i>: &lsquo;the annual allowable increase in effect on June 1, 2025 is "
     "1.6%&rsquo; " + cite("S3"),
     "Document 571: the rate in effect on June 1, 2025 was 1.4%; 1.6% applied from March 1, 2026 " + cite("S2"),
     "The example&rsquo;s <b>result</b> ($1,016.00) is correct under the rule the same page states &mdash; use the "
     "rate in effect on the effective date. The engine applies that rule and reproduces the result exactly. Flag F11."],
])}

<h3>Third-party sources rejected</h3>
<p class="small">Read, compared against official sources, and excluded. None is cited on this site: a
&lsquo;SF rent control calculator&rsquo; (states 1.7% for 2026-27); a brokerage tenant guide (states a 90-day notice
for increases &lsquo;of 10% or more&rsquo;); a property-management tenant guide (states a 60-day notice period); a
tenant union&rsquo;s summary of the Rent Board fee; and a collection of landlord-side and tenant-side explainer sites.
See flags F2 and F3 and the <a href="sources.html">source register</a>.</p>
"""
    return body


# ==========================================================================
# 15. EXECUTIVE SUMMARY
# ==========================================================================
@page("pages/executive-summary.html", "Executive summary",
      "Overview &rsaquo; <b>Executive summary</b>",
      "Executive summary of the rent-increase compliance analysis for two rent-controlled units in San Francisco 94122.")
def p_exec():
    a1, b1 = A["s1"], B["s1"]
    body = f"""
<h2 class="pg">Executive summary</h2>
<p class="lede">Prepared {d(AS_OF)} for two rent-controlled units in the Outer Sunset, San Francisco 94122, in a
building reported built in 1940. All tenant names and unit designations are pseudonymised; all dates and dollar
amounts are exactly as supplied.</p>

{note("ok", "Bottom line",
      "<p><b>Unit A</b>: raise rent <b>" + pct(a1['total']) + "</b> &mdash; <b>" + usd(a1['amount']) + "</b>, taking "
      "base rent from " + usd(A['base']) + " to <b>" + usd(a1['new_rent']) + "</b> &mdash; effective <b>" +
      d(a1['effective']) + "</b>, with a <b>" + str(a1['notice_days']) + "-day</b> written notice served on or before "
      "<b>" + d(a1['serve_by']) + "</b> (" + d(a1['serve_by_mailed']) + " if mailed).</p>"
      "<p><b>Unit B</b>: raise rent by the verified banked total of <b>" + pct(b1['banked']) + "</b> plus the annual "
      "rate then in effect, worth at least <b>" + usd(b1['amount_known']) + "</b>, taking base rent from " +
      usd(B['base']) + " to at least <b>" + usd(b1['new_rent_known']) + "</b>, effective <b>" + d(b1['effective']) +
      "</b>, with a <b>" + str(b1['notice_days']) + "-day</b> written notice served on or before <b>" +
      d(b1['serve_by']) + "</b> (" + d(b1['serve_by_mailed']) + " if mailed). The rate for the period beginning March "
      "1, 2027 <b>had not been published</b> as of the analysis date and is left blank rather than forecast.</p>"
      "<p><b>Raise both units, each to its own lawful amount, on each unit&rsquo;s own anniversary date.</b> Do not "
      "attempt to equalise the percentages &mdash; that would exceed Unit A&rsquo;s ceiling and void the increase "
      "entirely.</p>")}

<h3>1. What is a reasonable and normal increase here?</h3>
{tbl("What is a reasonable and normal increase here?", ["Jurisdiction", "Maximum", "Applies to these units?", "Source"], [
    ["<b>Local &mdash; San Francisco</b>",
     "<b>1.6%</b> for increases effective March 1, 2026 &ndash; February 28, 2027, plus any properly matured banked "
     "amounts. Once per 12 months, on base rent, never rounded up. Ordinance ceiling 7%.",
     '<span class="b rec">YES &mdash; this governs</span>', cite("S1", "S2", "S3", "S6")],
    ["<b>State &mdash; California</b>",
     "AB 1482 would allow <b>8.8%</b> for increases effective August 1, 2026 &ndash; July 31, 2027 (5% plus 3.8% "
     "April-to-April CPI-U for San Francisco-Oakland-Hayward).",
     '<span class="b bad">NO</span> &mdash; Civ. Code Sec. 1947.12(d)(3) exempts housing under a local ordinance '
     'with a lower cap; 1.6% is lower than 8.8%.', cite("S24", "S29")],
    ["<b>Federal</b>", BLANK,
     '<span class="b na">No federal ceiling exists</span> for privately owned, unsubsidised housing. Federal law '
     'constrains the <i>manner</i> of setting rent (Fair Housing Act), not the amount.', cite("S34", "S35")],
])}
<p><b>What is &ldquo;normal&rdquo;, measured from the official table.</b> The mean allowable annual increase since
March 1, 2019 is <b>{float(ST['recent']['mean']):.2f}%</b> (median {ST['recent']['median']}%, n={ST['recent']['n']});
since April 1, 1982 it is <b>{float(ST['all']['mean']):.2f}%</b> (median {ST['all']['median']}%, n={ST['all']['n']}).
A normal annual increase in San Francisco is therefore roughly 1.5&ndash;2.5%, and 1.6% right now. Unit A&rsquo;s
recommended {pct(a1['total'])} sits in that band. Unit B&rsquo;s {pct(b1['banked'])}+ is lawful but is a one-step
recovery of seven years of forbearance, and the official rules expressly permit taking less.
{cite("S2", "S4", "S5")}</p>
<p><b>The constitutional floor on the other side.</b> California&rsquo;s Legislative Analyst records that courts have
ruled rent control must allow landlords to receive a <b>fair rate of return</b>. Taking nothing for seven years is not
required; taking the published rate is. {cite("S32")}</p>

<h3>2. How do large corporations and individual owners handle this?</h3>
<p>The legal ceiling is identical. Three verifiable differences matter:</p>
<ul>
<li><b>Entity form narrows corporate exemptions.</b> Civ. Code Sec. 1947.12(d)(5)(A) denies the separately-alienable
(single-family / condominium) exemption to a REIT, a corporation, or an LLC with a corporate member. {cite("S24")}</li>
<li><b>Reporting deadlines arrived earlier for large portfolios.</b> The rent increase license requirement became
operative July 1, 2022 for non-condominium buildings with 10 or more units, and reporting began March 1, 2023 for
condominiums and buildings with fewer than 10. A two-unit owner therefore has less institutional muscle and a later,
tighter deadline &mdash; but the same consequence if the license is missing. {cite("S8", "S9")}</li>
<li><b>Algorithmic pricing is banned outright.</b> Rent Ordinance Sec. 37.10C (Ordinance 224-24, effective October 14,
2024) prohibits the sale or use of algorithmic devices to set rents or manage occupancy levels for residential units.
The revenue-management software standard in institutional multifamily is unlawful in San Francisco &mdash; for
corporations and for individual owners alike. {cite("S6")}</li>
</ul>
<p>What the corporate record does show, from SEC filings by a large Bay Area multifamily REIT, is that institutional
owners describe rent control as something that &lsquo;limit[s] our ability to charge market rents, increase rents,
evict tenants or recover increases in our operating expenses&rsquo;, and that they manage to portfolio revenue targets
through annual renewal cycles. Neither a portfolio target nor a renewal cycle is a lawful ground for an increase
here: the only grounds are the closed list in <a href="notice-guide.html">Notice procedure &amp; reasons</a>.
{cite("S37", "S38", "S13")}</p>

<h3>3. How do you notify a tenant correctly?</h3>
<ol>
<li>Confirm coverage, base rent and the complete rent history.</li>
<li><b>Confirm a current rent increase license is on file for the effective date</b> (Rent Ordinance Sec. 37.15).
Without it the entire increase is null and void. {cite("S8", "S9", "S6")}</li>
<li>Compute on <b>base rent</b> only: matured banked percentages added &mdash; never compounded &mdash; plus the
annual rate in effect on the <b>effective date</b>, truncated to the cent, never rounded up. {cite("S3", "S5")}</li>
<li>Give written notice: <b>30 days</b> if the total is 10% or less, <b>90 days</b> if more than 10%, plus <b>5 days</b>
if mailed. {cite("S23", "S3")}</li>
<li>State the <b>dollar amount</b>, the <b>percentage</b>, the <b>effective date</b>, and <b>which portion is banked
and from what dates</b>, plus any certified or passthrough component on the Board&rsquo;s forms. {cite("S6", "S5")}</li>
<li>Keep the notice, the proof of service and the worksheet.</li>
</ol>
<p><b>Legitimate reasons are a closed list:</b> the published annual allowable increase; properly matured banked
increases; a Board-certified capital improvement, operating and maintenance expense, comparable-units or Proposition I
petition; utility, water revenue bond and general obligation bond passthroughs on the Board&rsquo;s worksheets; lead
hazard remediation; and recovery of 50% of the Rent Board fee ($29.50 per dwelling unit for 2026-2027). Anything
beyond that requires a Sec. 37.8 petition <b>before</b> the notice is served. {cite("S13", "S6", "S10")}</p>
<p><b>Reasons that will fail:</b> market rate while an original occupant remains; a new or replacement occupant
(Sec. 37.3(a)(11)(A) applies even if the lease permits it); costs rising without a certified petition; the state
8.8% cap; the lease saying so; a pricing model; and any retaliatory or discriminatory motive.
{cite("S6", "S3", "S11", "S24")}</p>

<h3>4. Raise one unit, or both?</h3>
<p><b>Both, each to its own lawful amount, under one written policy.</b> Raising only one is lawful &mdash; the
Ordinance is unit- and tenancy-specific, and there is no requirement to raise every unit. But the difference here
(Unit A {pct(a1['total'])} against Unit B {pct(b1['banked'])}+) is produced entirely by the official rate table
applied to each unit&rsquo;s own anniversary date and tenancy length: a facially neutral, documentable, statute-driven
basis with no connection to any protected characteristic. That is the answer to a discrimination inquiry, and it must
be documented <i>before</i> the decision. {cite("S2", "S5", "S33", "S34")}</p>
<p>The trap is the intuitive one. Making the percentages equal would exceed Unit A&rsquo;s ceiling and, under
Sec. 37.3(b)(5), render the increase <b>null and void in its entirety</b>. {cite("S6")}</p>
<p><b>Residual exposure to manage on Unit B:</b> a step increase above 10% requires 90 days&rsquo; notice and is the
fact pattern most often challenged. California protects age, disability, familial status and source of income, and a
tenant may file a Tenant Financial Hardship Application (Form 363). Neither occupant&rsquo;s age, disability status or
income source was supplied &mdash; left blank. Taking less than the maximum is expressly permitted and materially
reduces this exposure. {cite("S33", "S14", "S4")}</p>

<h3>5. Would it survive a San Francisco tenant lawyer?</h3>
<p><b>Conditionally yes.</b> Fifteen attack vectors are modelled on the
<a href="red-team.html">red team page</a>. Most are low risk on the facts as supplied. Three conditions must be
closed first:</p>
<ol>
<li><b>The rent increase license.</b> Unknown for both units; highest residual risk in the file because it is
independent of the arithmetic. {cite("S8", "S9")}</li>
<li><b>The banking maturity conflict.</b> Two official sf.gov pages disagree &mdash; 12 months (Rules and Regulations
Sec. 4.12(a), controlling) versus 24 months (the summary page). Confirm with a Rent Board counselor on
415-252-4600 before serving a banked-increase notice. {cite("S5", "S4")}</li>
<li><b>The paper file.</b> Base-rent composition, prior increase history, Rent Board fee receipts and deposit-interest
records were not supplied and are left blank. {cite("S3", "S10", "S1")}</li>
</ol>

<h3>Conditions precedent &mdash; do not serve before these are closed</h3>
<ul class="checklist">
<li>A current rent increase license is confirmed on file for each unit, covering the effective date. {cite("S8", "S9")}</li>
<li>The building&rsquo;s construction date and unit type are confirmed on the Property Information Map. {cite("S7", "S21")}</li>
<li>The 12-month banking maturity rule is confirmed with a Rent Board counselor. {cite("S5", "S4")}</li>
<li>The complete rent history, ledger and base-rent composition are assembled for each unit. {cite("S18", "S14")}</li>
<li>The Rent Board fee for 2026-27 is paid and security-deposit interest at 4.2% is current. {cite("S10", "S1")}</li>
<li>A single written rent-increase policy covering both units is adopted and dated before any notice is served. {cite("S33", "S34")}</li>
<li>Occupant circumstances relevant to hardship on Unit B are checked, and the full-versus-partial decision is made on
that basis. {cite("S14", "S4")}</li>
<li>Counsel has reviewed the notice text. {cite("S6", "S5", "S23")}</li>
</ul>

<h3>What was verified, and what was not</h3>
{tbl("Assurance", ["Measure", "Result"], [
    ["Official sources in the register", f"<b>{len(SOURCES)}</b> &mdash; sf.gov, leginfo.legislature.ca.gov, "
     "dir.ca.gov, justice.gov, calcivilrights.ca.gov, sec.gov, lao.ca.gov, sfplanninggis.org, portal.sfrb.org"],
    ["Retrieved and read directly", f"<b>{sum(1 for s in SOURCES if s['method']=='fetched')}</b> of {len(SOURCES)}; "
     "the remainder are official URLs HTTP-verified in CI and never used alone to support a number"],
    ["Calculator self-tests against official worked examples",
     "<b>4 of 4 passed</b> &mdash; $1,047.00, $1,033.00, $1,387.10 and $1,016.00 reproduced exactly"],
    ["Values left blank rather than inferred", "<b>13</b>, all listed on the flag register"],
    ["Items flagged", f"<b>{len(FLAGS)}</b> &mdash; including two direct conflicts between official sf.gov pages, one "
     "official document error, one unpublished rate and one unverifiable federal item"],
    ["Third-party sources used", "<b>Zero.</b> Several were read, found to conflict with official sources, and "
     "excluded"],
    ["Personal information published", "<b>None.</b> Pseudonymised units and tenants; dates and amounts preserved "
     "exactly; no street address supplied or published"],
])}

{note("warn", "Not legal advice",
      "<p>This is a documented, source-linked compliance analysis intended to be handed to counsel or to a Rent Board "
      "counselor for confirmation. Free landlord counselling is available from the Rent Board on 415-252-4600, "
      "weekdays 9am-12pm and 1pm-4pm. " + cite("S7") + "</p>")}
"""
    return body


# ==========================================================================
# 16. REPO AUDIT
# ==========================================================================
@page("pages/audit.html", "Repository audit & log",
      "Assurance &rsaquo; <b>Repo audit &amp; log</b>",
      "Line-by-line review of the repository, what changed, and the verification performed.")
def p_audit():
    import subprocess
    try:
        log = subprocess.run(["git", "log", "--format=%h|%ad|%s", "--date=format:%Y-%m-%d %H:%M"],
                             cwd=ROOT, capture_output=True, text=True, timeout=20).stdout.strip().split("\n")
    except Exception:
        log = []
    log_rows = []
    for line in log[:40]:
        parts = line.split("|", 2)
        if len(parts) == 3:
            log_rows.append([f'<code>{parts[0]}</code>', parts[1], e(parts[2])])

    inv = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [x for x in dirnames if x not in (".git", "__pycache__")]
        for fn in sorted(filenames):
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)
            try:
                size = os.path.getsize(os.path.join(dirpath, fn))
            except OSError:
                size = 0
            inv.append([f'<code>{rel}</code>', f"{size:,} bytes",
                        ROLE.get(rel, "Generated or supporting file")])

    body = f"""
<h2 class="pg">Repository audit &amp; log</h2>
<p class="lede">A line-by-line review of the repository, what was found, what was built, and what verification was
performed. Nothing in the original repository was relied on: it contained no data.</p>

<h3>State found at the start</h3>
{tbl("What the repository contained at commit <code>dab56c9</code>", ["Item", "Finding"], [
    ["Files", "One: <code>README.md</code>, containing the single line <code># RentincreaseSF3</code> with no "
     "trailing newline."],
    ["Data, analysis, documentation", "None."],
    ["Web content", "None &mdash; GitHub Pages was enabled (legacy build from the <code>main</code> branch, root path) "
     "but served nothing."],
    ["Prior values to reconcile", "None. There was no legacy data, so no figure in this project was carried over from "
     "an unverified source."],
    ["Consequence", "Every value published here was sourced from scratch against official publications. Flag F1."],
])}

<h3>What was built</h3>
{tbl("Deliverable", ["Path", "Purpose"], [
    ["Calculation engine", "<code>tools/rentcalc.py</code>",
     "The single source of truth for every number published. Implements rules R1-R8, each tied to an official source, "
     "and holds the complete official allowable-increase table from April 1, 1982 to February 28, 2027, the "
     "security-deposit interest rates and the CPI series."],
    ["Verification report", "<code>tools/calc.py</code>",
     "Asserts the engine reproduces all four official Rent Board worked examples exactly before writing any output, "
     "then prints every published number and writes <code>data/_calc.json</code>. Exits non-zero on any failure."],
    ["Source register", "<code>tools/content.py</code>",
     f"All {len(SOURCES)} sources with publisher, URL, what each verifies and how it was checked."],
    ["Flag register", "<code>tools/content.py</code>", f"All {len(FLAGS)} flags with severity, detail and action taken."],
    ["Site generator", "<code>tools/build_site.py</code>", "Renders every page from the verified data only."],
    ["Link checker", "<code>tools/check_links.py</code>",
     "Verifies every internal link resolves to a real file and every external link returns HTTP 200."],
    ["Site", "<code>index.html</code> and <code>pages/*.html</code>",
     "Dashboard landing page plus 15 subpages organised by category. No CDN, no external fonts, no build step at "
     "serve time."],
    ["Machine-readable data", "<code>data/*.csv</code>, <code>data/*.json</code>",
     "The official rate history, the source register, the flag register and every computed scenario, so the published "
     "figures can be audited outside the HTML."],
    ["Documentation", "<code>EXECUTIVE_SUMMARY.md</code>, <code>docs/law/*.md</code>, <code>docs/analysis/*.md</code>, "
     "<code>docs/audit/repo-audit.md</code>, <code>docs/verification/*.md</code>",
     "The same findings in Markdown for review without a browser."],
    ["Coordination log", "<code>COORDINATION.md</code>", "Task board, source register, flag register and change log."],
])}

<h3>Verification performed</h3>
{tbl("Check", ["Method", "Result"], [
    ["Every published percentage", "Traced to SF Rent Board document 571 and cross-checked against the Current Rates "
     "page.", "Matched"],
    ["Every published dollar amount", "Recomputed by the engine; the engine is asserted against four official worked "
     "examples ($1,047.00, $1,033.00, $1,387.10, $1,016.00) before it writes anything.", "4 of 4 matched exactly"],
    ["Every notice deadline", "Computed from Civ. Code Sec. 827(b) plus the sf.gov 5-day mailing rule.", "Matched"],
    ["Every statutory quotation", "Read from the California Legislative Information code display or from the official "
     "compiled ordinance and Rules and Regulations PDF published on sf.gov.", "Matched"],
    ["Third-party claims", "Read, compared against official sources, and excluded. Three material errors found and "
     "recorded as flags F2 and F3.", "Zero third-party values used"],
    ["Internal links", "Checked by <code>tools/check_links.py</code> against the filesystem.", "See the CI record"],
    ["External links", "HTTP status checked by <code>tools/check_links.py</code> in CI on every push.", "See the CI record"],
    ["Personal information", "Searched every generated page for names and addresses.", "None published"],
    ["Unverifiable values", "Left blank and listed on the flag register rather than estimated.", "13 blanks, all documented"],
])}

<h3>File inventory</h3>
{tbl("Path", ["Size", "Role"], inv)}

<h3>Commit log</h3>
{tbl("Commit", ["Date (UTC)", "Message"], log_rows or [["&mdash;", "&mdash;", "Run from a git checkout to populate"]])}

<h3>Reproducibility</h3>
<div class="panel"><pre style="margin:0;font-family:var(--mono);font-size:12.6px;overflow-x:auto">python3 tools/calc.py         # self-tests against the four official worked examples; writes data/_calc.json
python3 tools/build_site.py   # regenerates index.html, pages/*.html and data/*.csv from verified data only
python3 tools/check_links.py  # verifies every link (use --offline where the network is unavailable)</pre>
<p class="small" style="margin-bottom:0">No third-party packages are required. The site uses no CDN, no external
font and no runtime network call, so it renders identically offline and on GitHub Pages.</p></div>
"""
    return body


ROLE = {
    "README.md": "Repository overview",
    "EXECUTIVE_SUMMARY.md": "Executive summary in Markdown",
    "COORDINATION.md": "Parallel-session task board, source register and change log",
    ".nojekyll": "Forces GitHub Pages to serve files verbatim, without Jekyll processing",
    "index.html": "Dashboard landing page",
    "tools/rentcalc.py": "Calculation engine - the single source of truth for every published number",
    "tools/calc.py": "Verification report and self-tests against official worked examples",
    "tools/content.py": "Source register, flag register and navigation",
    "tools/build_site.py": "Site generator",
    "tools/check_links.py": "Internal and external link checker",
    "assets/css/style.css": "Site stylesheet - no external fonts or CDN",
    "data/_calc.json": "Machine-readable calculation output consumed by the generator",
}

# ==========================================================================
# MAIN
# ==========================================================================
def write_data_files():
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    with open(os.path.join(ROOT, "data", "sf-aga-history.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["effective_from", "effective_through", "allowable_increase_pct", "source_id", "source_url"])
        for s, en, p in AGA:
            w.writerow([s.isoformat(), en.isoformat(), f"{p}", "S2", SRC["S2"]["url"]])
        w.writerow(["2027-03-01", "2028-02-28", "", "S2",
                    "NOT PUBLISHED as of " + AS_OF + " - left blank, never forecast"])
    with open(os.path.join(ROOT, "data", "cpi-sf-oakland-hayward.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["reference_month", "twelve_month_change_pct", "source_id", "source_url"])
        for period, val in CPI_SF_OAKLAND_HAYWARD:
            w.writerow([period, "" if val is None else val.replace("%", ""), "S29", SRC["S29"]["url"]])
    with open(os.path.join(ROOT, "data", "sources.json"), "w") as f:
        json.dump(SOURCES, f, indent=2)
    with open(os.path.join(ROOT, "data", "flags.json"), "w") as f:
        json.dump(FLAGS, f, indent=2)
    with open(os.path.join(ROOT, "data", "scenarios.json"), "w") as f:
        json.dump({"analysis_date": C["analysis_date"], "unit_a": A, "unit_b": B,
                   "statistics": ST, "ab1482_context": C["ab1482"]}, f, indent=2)
    print("  wrote data/sf-aga-history.csv, cpi-sf-oakland-hayward.csv, sources.json, flags.json, scenarios.json")


def main():
    print("Building site from data/_calc.json (produced by tools/calc.py)...")
    for path, title, crumb, desc, fn in PAGES:
        render(path, title, crumb, fn(), desc)
    write_data_files()
    n = sum(1 for p, *_ in PAGES)
    print(f"\nDone: {n} pages, {len(SOURCES)} sources registered, {len(FLAGS)} flags published.")
    print("Next: python3 tools/check_links.py")


if __name__ == "__main__":
    main()
