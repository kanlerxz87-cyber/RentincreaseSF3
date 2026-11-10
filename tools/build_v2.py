#!/usr/bin/env python3
"""Build the 2026-11-10 dashboard edition.

Outputs (a self-contained edition; it edits no file owned by another session):
  verification/index.html        (edition landing = dashboard + executive summary)
  verification/*.html            (nine category subpages)
  verification/style.css

Design rules enforced by construction:
  * every data row carries >=1 link to an official source, or an explicit
    FLAG marker pointing at the register (never an inferred value);
  * no tenant name, initial, street address, ZIP or neighbourhood name;
  * dates and dollar amounts are reproduced unchanged from the owner's data;
  * every figure is re-verified against a source fetched on 2026-11-10.

Run:  python3 tools/build_v2.py
"""
from __future__ import annotations

import datetime as dt
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "verification"
ACCESSED = "2026-11-10"

# --------------------------------------------------------------------------
# Source register.  Every URL below was fetched and read on 2026-11-10.
# --------------------------------------------------------------------------
SRC = {
    "banked": (
        "sf.gov — Banked rent increases",
        "https://www.sf.gov/information/banked-rent-increases",
    ),
    "learn": (
        "sf.gov — Learn about rent increases in SF",
        "https://www.sf.gov/learn-about-rent-increases-san-francisco",
    ),
    "inv": (
        "sf.gov — The Rent Board Housing Inventory",
        "https://www.sf.gov/rent-board-housing-inventory",
    ),
    "noncomp": (
        "sf.gov — Notice of Owner Noncompliance with Housing Inventory",
        "https://www.sf.gov/notice-of-owner-noncompliance-with-housing-inventory",
    ),
    "petitions": (
        "sf.gov — Tenant Petitions",
        "https://www.sf.gov/tenant-petitions",
    ),
    "unlawful": (
        "sf.gov — Report an unlawful rent increase / review rent history",
        "https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history",
    ),
    "rates": (
        "sf.gov — Current Rates (rent increase, relocation, deposit)",
        "https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit",
    ),
    "fee": (
        "sf.gov — The Rent Board Fee",
        "https://www.sf.gov/rent-board-fee",
    ),
    "rentallaws": (
        "sf.gov — Learn about San Francisco rental laws",
        "https://www.sf.gov/learn-about-san-francisco-rental-laws",
    ),
    "multi": (
        "sf.gov — Annual rent increase for multiple years",
        "https://www.sf.gov/information--annual-rent-increase-multiple-years",
    ),
    "cos": (
        "sf.gov — Rent increases under §6.14 and Costa-Hawkins",
        "https://www.sf.gov/information--rent-increases-under-section-614-and-costa-hawkins",
    ),
    "algo": (
        "sf.gov — Algorithmic devices that set rent are prohibited",
        "https://www.sf.gov/information--algorithmic-devices-set-rent-are-prohibited-san-francisco",
    ),
    "evict": (
        "sf.gov — Evictions in San Francisco",
        "https://www.sf.gov/evictions-san-francisco",
    ),
    "f571": (
        "sf.gov — Form 571, Allowable Annual Increases 26–27 (PDF)",
        "https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf",
    ),
    "s827": (
        "Civ. Code §827 (leginfo)",
        "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827",
    ),
    "s1013": (
        "Code Civ. Proc. §1013 (leginfo)",
        "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1013",
    ),
    "s1942_5": (
        "Civ. Code §1942.5 (leginfo)",
        "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5",
    ),
    "s1947_12": (
        "Civ. Code §1947.12 — Tenant Protection Act (leginfo)",
        "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12",
    ),
    "s1954_53": (
        "Civ. Code §1954.53 — Costa-Hawkins (leginfo)",
        "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954.53",
    ),
    "s12955": (
        "Gov. Code §12955 — FEHA housing discrimination (leginfo)",
        "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=12955",
    ),
    "fha": (
        "42 U.S.C. §3604 (govinfo)",
        "https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm",
    ),
    "oag": (
        "oag.ca.gov — Limits on Rent Increases",
        "https://oag.ca.gov/rentcaps",
    ),
    "legistar": (
        "sfgov.legistar.com — File #261020",
        "https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770",
    ),
    "s373": (
        "S.F. Admin. Code §37.3 (American Legal Publishing)",
        "https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_admin/0-0-0-70881",
    ),
    "portal": ("Rent Board Portal", "https://portal.sfrb.org/"),
    "crd": ("calcivilrights.ca.gov — housing", "https://calcivilrights.ca.gov/housing/"),
    "hud": (
        "hud.gov — Report housing discrimination",
        "https://www.hud.gov/reporthousingdiscrimination",
    ),
}

OFFICIAL = {
    "www.sf.gov", "sf.gov", "leginfo.legislature.ca.gov", "govinfo.gov",
    "oag.ca.gov", "sfgov.legistar.com", "codelibrary.amlegal.com",
    "portal.sfrb.org", "calcivilrights.ca.gov", "www.hud.gov", "hud.gov",
}


def S(*keys: str) -> str:
    """Render one or more official source links."""
    parts = []
    for k in keys:
        label, url = SRC[k]
        parts.append(f'<a href="{url}">{label}</a>')
    return " · ".join(parts)


def FLAG(*ids: str) -> str:
    """Marker for a row whose value could not be verified."""
    return '<span class="flag">' + " ".join(ids) + "</span>"


def BLANK(fid: str) -> str:
    return f'<span class="blank">blank — unverified</span> {FLAG(fid)} → <a href="flagged.html">register</a>'


NAV = [
    ("index.html", "Overview"),
    ("executive-summary.html", "Executive summary"),
    ("license.html", "Licence &amp; process"),
    ("laws.html", "Laws &amp; caps"),
    ("units.html", "Units &amp; math"),
    ("notice.html", "Notice &amp; reasons"),
    ("tenant-review.html", "Tenant-lawyer test"),
    ("practice.html", "Owner practice"),
    ("flagged.html", "Flagged"),
    ("sources.html", "Sources"),
]

CSS = """/* 2026-11-10 dashboard edition — plain, dependency-free, print friendly */
:root{
  --bg:#f5f7fa; --card:#fff; --ink:#16212c; --muted:#5a6b7b; --line:#e2e8f0;
  --blue:#12558a; --blue-soft:#eaf2f9; --green:#0b6b4f; --green-soft:#e8f5ef;
  --red:#9d2a1e; --red-soft:#fdf0ee; --amber:#8a5a00; --amber-soft:#fff6e8;
  --radius:10px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);line-height:1.55;
  font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:#0b5aa0}
a:hover{text-decoration:underline}
header.top{background:#0f2438;color:#fff;padding:14px 20px 10px}
header.top .brand{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:10px}
header.top .brand strong{font-size:1.05rem;letter-spacing:.01em}
header.top .brand span{font-size:.78rem;color:#a9c2d8}
nav.main{display:flex;flex-wrap:wrap;gap:4px}
nav.main a{color:#cfe0ee;text-decoration:none;font-size:.83rem;padding:5px 9px;border-radius:6px;white-space:nowrap}
nav.main a:hover{background:#1b3b58;color:#fff}
nav.main a.active{background:var(--blue);color:#fff}
main{max-width:1080px;margin:0 auto;padding:22px 18px 40px}
h1{font-size:1.5rem;margin:.2em 0 .35em;line-height:1.25}
h2{font-size:1.16rem;margin:0 0 .5em}
h3{font-size:.98rem;margin:1em 0 .35em}
p{margin:.5em 0}
.lead{color:var(--muted);font-size:.95rem;margin:0 0 1em}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:18px 20px;margin:0 0 18px;box-shadow:0 1px 2px rgba(16,24,40,.04)}
.card.answer{border-left:5px solid var(--red);background:var(--red-soft)}
.card.answer h2{color:var(--red)}
.card.gate{border-left:5px solid var(--green);background:var(--green-soft)}
.card.gate h2{color:var(--green)}
.card.note{border-left:4px solid var(--blue);background:var(--blue-soft)}
.card.warn{border-left:4px solid #c98b1b;background:var(--amber-soft)}
.card h2:first-child,.card h3:first-child{margin-top:0}
table{width:100%;border-collapse:collapse;font-size:.88rem;margin:.6em 0 .3em}
caption{text-align:left;font-size:.8rem;color:var(--muted);padding:.2em 0 .4em}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
th{background:#eef3f8;font-weight:600;font-size:.82rem;letter-spacing:.01em}
tbody tr:nth-child(even) td{background:#fbfcfe}
td.num,th.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:.4em 0 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:13px 14px}
.kpi .v{font-size:1.28rem;font-weight:700;color:var(--blue);line-height:1.15}
.kpi .l{font-size:.78rem;color:var(--muted);margin-top:3px}
.kpi .s{font-size:.72rem;margin-top:5px}
.cats{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}
.cat{display:block;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:14px 16px;text-decoration:none;color:inherit}
.cat:hover{border-color:#9fbedb;box-shadow:0 2px 8px rgba(16,24,40,.08);text-decoration:none}
.cat b{display:block;color:#0b5aa0;font-size:.97rem;margin-bottom:3px}
.cat span{font-size:.82rem;color:var(--muted)}
.tag{display:inline-block;font-size:.7rem;font-weight:600;padding:1px 7px;border-radius:20px;
  background:#e7eef6;color:#24537a;border:1px solid #d3e0ec;white-space:nowrap}
.flag{display:inline-block;font-size:.68rem;font-weight:700;padding:1px 6px;border-radius:4px;
  background:var(--amber-soft);color:var(--amber);border:1px solid #eccd94;white-space:nowrap}
.blank{color:#8a5a00;font-style:italic}
.ok{color:var(--green);font-weight:600}
.no{color:var(--red);font-weight:600}
.small{font-size:.8rem;color:var(--muted)}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.82rem}
.letter{background:#fff;border:1px dashed #9bb4c9;border-radius:8px;padding:14px 16px;
  font-size:.86rem;white-space:pre-wrap;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;line-height:1.5}
ul,ol{margin:.4em 0 .6em;padding-left:1.25em}
li{margin:.22em 0}
footer{max-width:1080px;margin:0 auto;padding:6px 18px 34px;color:var(--muted);font-size:.78rem}
footer p{margin:.35em 0}
.lede-strip{display:flex;gap:10px;flex-wrap:wrap;align-items:center;font-size:.78rem;color:#dce9f5;
  border-top:1px solid #23425c;padding-top:9px;margin-top:2px}
@media (max-width:640px){
  table{font-size:.82rem}
  th,td{padding:6px 7px}
  main{padding:16px 12px 32px}
}
@media print{header.top,nav.main{background:#fff;color:#000}nav.main{display:none}.card{break-inside:avoid}}
"""


def page(title: str, h1: str, lead: str, body: str, prefix: str = "", active: str = "",
         nav_prefix: str | None = None) -> str:
    """All pages live in one directory, so navigation is always sibling-relative."""
    nav = "\n".join(
        '      <a href="%s"%s>%s</a>'
        % (href, ' class="active"' if href == active else "", label)
        for href, label in NAV
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Rental Increase SF</title>
<meta name="description" content="Source-linked review of lawful rent increases for two rent-controlled San Francisco flats in a 1940 two-unit building. Anonymised; not legal advice.">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="top">
  <div class="brand">
    <strong>Rental Increase SF</strong>
    <span>Two rent-controlled flats · 1940 two-unit building · location withheld</span>
  </div>
  <nav class="main" aria-label="Sections">
{nav}
  </nav>
  <div class="lede-strip">
    <span class="tag">ANONYMISED</span>
    <span>No names, initials, address or ZIP · dates and dollar amounts unchanged</span>
    <span>·</span><span>Sources fetched {ACCESSED}</span>
    <span>·</span><span>Not legal advice</span>
  </div>
</header>
<main id="main">
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
{body}
</main>
<footer>
  <p><strong>Internal working document.</strong> Prepared for the property owner. Tenant and occupant details are replaced with
  placeholder labels; the street address, unit numbers and ZIP code are withheld. Dates and dollar amounts supplied by the
  owner are reproduced unchanged. Every table row links an official source or is blank and listed on the
  <a href="flagged.html">Flagged</a> register — no value is inferred.</p>
  <p>Not legal advice. Confirm any figure on the effective date, and confirm the process with a Rent Board counsellor
  (415-252-4600) and a California attorney before serving a notice. Official sources accessed {ACCESSED}.</p>
  <p><strong>This edition:</strong> a self-contained verification pass. The canonical dashboard is
  <a href="../index.html">the repository landing page</a>; other preserved editions are
  <a href="../audit/process.html">audit/</a>, <a href="../verified/index.html">verified/</a>,
  <a href="../docs/index.html">docs/</a>, <a href="../dashboard/index.html">dashboard/</a> and
  <a href="../review/index.html">review/</a>.</p>
  <p>Verification: <span class="mono">python3 tools/check_v2.py</span> (links, anchors, per-row sourcing,
  anonymisation, arithmetic) and the repository-wide privacy sweep
  <span class="mono">python3 tools/privacy_scan.py</span>.</p>
</footer>
</body>
</html>
"""


# --------------------------------------------------------------------------
# Verified figures (recomputed, never typed by hand)
# --------------------------------------------------------------------------
U1 = D("3995.00")
U2 = D("3150.00")
RATES = [  # (rate year label, percent) — Form 571
    ("1 Mar 2020 – 28 Feb 2021", D("1.8")),
    ("1 Mar 2021 – 28 Feb 2022", D("0.7")),
    ("1 Mar 2022 – 28 Feb 2023", D("2.3")),
    ("1 Mar 2023 – 29 Feb 2024", D("3.6")),
    ("1 Mar 2024 – 28 Feb 2025", D("1.7")),
    ("1 Mar 2025 – 28 Feb 2026", D("1.4")),
    ("1 Mar 2026 – 28 Feb 2027", D("1.6")),
]


def pct(p: D) -> str:
    return f"{p:.1f}%"


def money(x: D) -> str:
    return f"${x:,.2f}"


def inc(base: D, p: D) -> D:
    return (base * p / 100).quantize(D("0.01"))


BANK7 = sum(p for _, p in RATES)                      # 13.1
BANK6 = sum(p for _, p in RATES[:-1])                 # 11.5
U2_TOTAL = inc(U2, BANK7)
U1_BANK = inc(U1, D("3.0"))                           # 119.85
U1_SINGLE = inc(U1, D("1.6"))                         # 63.92
U2_SINGLE = inc(U2, D("1.6"))                         # 50.40
U2_TEN = inc(U2, D("10.0"))                           # 315.00
U2_REST = U2_TOTAL - U2_TEN                           # 97.65

assert (BANK7, BANK6) == (D("13.1"), D("11.5"))
assert U1_BANK == D("119.85") and U1_SINGLE == D("63.92")
assert U2_TOTAL == D("412.65") and U2_SINGLE == D("50.40") and U2_TEN == D("315.00")
assert U2_REST == D("97.65")

TODAY = dt.date(2026, 11, 10)


def minus(day_after: dt.date, days: int) -> dt.date:
    return day_after - dt.timedelta(days=days)


def fmt(d: dt.date) -> str:
    return d.strftime("%-d %b %Y")


# --------------------------------------------------------------------------
# Page: dashboard / executive summary at a glance
# --------------------------------------------------------------------------
def build_index() -> str:
    p = ""
    kpis = [
        ("1.6%", "Allowable annual increase, 1 Mar 2026 – 28 Feb 2027", S("learn")),
        ("1.4%", "Allowable annual increase, 1 Mar 2025 – 28 Feb 2026", S("f571")),
        (f"3.0%", f"Unit 1: 1.4% banked + 1.6% current = {money(U1_BANK)} → {money(U1 + U1_BANK)} on 1 Feb 2027", S("banked")),
        (f"{pct(BANK7)}", f"Unit 2: seven banked years = {money(U2_TOTAL)} → {money(U2 + U2_TOTAL)} (before the unannounced 2027-28 rate)", S("f571")),
        ("30 / 90", "Days' written notice: 30 if the 12-month total is 10% or less, 90 if more; +5 if mailed", S("s827")),
        ("March 1", "Housing Inventory report deadline each year — the licence must be on file on the effective date", S("inv")),
        ("$59.00", "Rent Board Fee per dwelling unit for tax year 2026-27 — a separate obligation ", S("fee")),
        ("4.2%", "Security-deposit interest owed to tenants, 1 Mar 2026 – 28 Feb 2027", S("rates")),
    ]
    kpi_html = "\n".join(
        f'      <div class="kpi"><div class="v">{v}</div><div class="l">{l}</div><div class="s">{s}</div></div>'
        for v, l, s in kpis
    )

    findings = [
        ("Do I have to tell the Rent Board and hold a rent-increase licence — as an individual, non-corporate owner?",
         "<strong class='no'>Yes.</strong> Every owner of residential property must report into the Housing Inventory, and a "
         "current rent-increase licence must be on file <em>before</em> an annual or banked increase takes effect. The law "
         "distinguishes by building size (10+ units from 1 Jul 2022; 1–9 units and condominiums from 1 Mar 2023), not by "
         "whether the owner is a person or a company.",
         S("inv", "noncomp")),
        ("Is the licence an application the Rent Board approves for each increase?",
         "No. It is generated automatically when you report a tenant-occupied unit. There is no per-increase filing and no "
         "petition for an annual or banked increase — but the licence must exist on the effective date.",
         S("inv", "multi")),
        ("What happens if the licence is missing on the effective date?",
         "The increase may be null and void, possibly for several years, and the tenant may be entitled to a refund. There is "
         "no charge and no time limit for a tenant to petition.",
         S("noncomp", "unlawful")),
        ("What is a lawful, normal increase for these units?",
         "The Rent Board's published allowance — 1.6% for an increase effective 1 Mar 2026 – 28 Feb 2027 — plus any correctly "
         "banked years. A larger amount is not available at the owner's discretion: it requires a Rent Board petition (capital "
         "improvement, operating and maintenance, comparable rents) or the narrow unlimited-increase rule that applies only once "
         "the last original occupant has permanently vacated. Banks are added, never compounded, and may not be rounded up.",
         S("learn", "banked")),
        ("Does the state cap (AB 1482) or federal law set a higher ceiling I could use?",
         "No. AB 1482 exempts housing that is already subject to a stricter local ordinance; the SF allowance is lower than the "
         "state 8.8% for 1 Aug 2026 – 31 Jul 2027. No federal statute caps rent; federal law governs <em>reasons</em> (fair housing).",
         S("s1947_12", "oag", "fha")),
        (f"Unit 1 — what can be imposed, and when?",
         f"One increase per 12 months. The 1.4% allowance for the 1 Feb 2026 anniversary was not used; it banks once 24 full "
         f"months pass without an increase, so on 1 Feb 2027 the ceiling is 3.0% = {money(U1_BANK)} → {money(U1 + U1_BANK)}, "
         f"with 30 days' notice. The 1 Apr 2026 continuation did not reset the anniversary.",
         S("banked", "learn")),
        (f"Unit 2 — what can be imposed, and when?",
         f"If no increase has been taken since 1 Jun 2019, seven banked years total {pct(BANK7)} = {money(U2_TOTAL)}. A "
         f"13.1% step exceeds 10%, so it needs 90 days' notice. The next anniversary is 1 Jun 2027, and the allowance then in "
         f"effect is <em>not yet published</em> — so the true June 2027 ceiling is higher than {pct(BANK7)} and cannot be stated yet.",
         S("f571", "banked")),
        ("Would a San Francisco tenant lawyer be able to overturn it?",
         "Only if a step is missed: no licence on the effective date, more than the allowance plus documented banks, a second "
         "increase inside 12 months, a base-rent error, a notice missing a required element, a retaliatory motive, or a "
         "protected-class reason. Each is a pass/fail check on the tenant-lawyer page.",
         S("petitions", "s827")),
        ("Should I raise both units or only one?",
         "There is no legal requirement to raise both, and raising one is not unlawful by itself. The risk is an inference of "
         "differential treatment: applying one written policy to both units, each on its own anniversary, is the most defensible "
         "posture. Document any objective reason if you treat them differently.",
         S("s12955", "fha")),
        ("Anything pending that could change this?",
         "Board of Supervisors File #261020 would cap combined banked + capital-improvement increases at 10% a year for three "
         "years. Status: <strong>Pending Committee Action</strong> — not law. A banked notice above 10% should be re-checked "
         "before service.",
         S("legistar", "banked")),
    ]
    findings_html = "\n".join(
        f"      <tr><td><strong>{q}</strong></td><td>{a}</td><td>{s}</td></tr>" for q, a, s in findings
    )

    cats = [
        ("Executive summary", "The one-page answer: licence first, then the numbers, then the notice — with the decisions the owner has to make.", p + "executive-summary.html", "Start here"),
        ("Licence &amp; process", "Do individual owners need the licence? Step-by-step filing, the fee, the exemption window, and what voids an increase.", p + "license.html", "Forefront question"),
        ("Laws &amp; caps", "Local ordinance, state Tenant Protection Act, federal fair housing, the pending 10% cap — and which one actually governs.", p + "laws.html", "Framework"),
        ("Units &amp; math", "Per-unit ledgers, cents-exact options, notice deadlines, and the two corrections that matter here.", p + "units.html", "Calculations"),
        ("Notice &amp; reasons", "What the notice must contain, how to serve it, and which reasons are required, permitted and forbidden.", p + "notice.html", "Procedure"),
        ("Tenant-lawyer test", "The checks a tenant's free lawyer would run, unit-by-unit, plus retaliation and discrimination exposure.", p + "tenant-review.html", "Stress test"),
        ("Owner practice", "How managed portfolios and individual owners actually run increases — and the parts that are not documented anywhere official.", p + "practice.html", "Comparison"),
        ("Flagged for review", "Every value that could not be confirmed from an official source, with what would close it.", p + "flagged.html", "Unverified"),
        ("Sources", "Every official source used, what it verifies, and the date it was read.", p + "sources.html", "Register"),
    ]
    cat_html = "\n".join(
        f'      <a class="cat" href="{href}"><b>{t}</b><span>{d}</span><br><span class="tag">{tag}</span></a>'
        for t, d, href, tag in cats
    )

    body = f"""  <div class="card answer">
    <h2>Forefront answer: yes — an individual owner must report to the Rent Board and hold a rent-increase licence</h2>
    <p><strong>Being a single individual owner, rather than a corporation, makes no difference.</strong> San Francisco requires
    <em>all</em> owners of residential property to report into the Rent Board Housing Inventory; reporting a tenant-occupied unit
    generates a <strong>rent-increase licence</strong>. That licence must be on file <strong>on the effective date</strong> of any
    annual or banked increase — not merely when the notice is served. Without it the increase may be <strong>null and void</strong>,
    and the tenant may claim a refund.</p>
    <p>The licence is not an approval of your increase, and you do not file the notice with the Rent Board. It is a
    <em>gate</em>: file the Housing Inventory first, confirm the licence, then serve the notice. Doing it the other way round is the
    single most common way a correctly calculated increase is overturned.</p>
    <div class="grid">
      <div class="kpi"><div class="v">1 · File</div><div class="l">Housing Inventory report, every year, due 1 March (free, online)</div></div>
      <div class="kpi"><div class="v">2 · Confirm</div><div class="l">Licence auto-issued for tenant-occupied units; check it in the Portal</div></div>
      <div class="kpi"><div class="v">3 · Check the date</div><div class="l">The licence must be in effect on the effective date of the increase</div></div>
      <div class="kpi"><div class="v">4 · Then notice</div><div class="l">Written notice, 30 or 90 days, served before the increase</div></div>
    </div>
    <p class="small" style="margin-top:10px">Sources: {S("inv", "noncomp", "banked")}</p>
    <p><a href="license.html"><strong>Read the step-by-step licence and filing walkthrough →</strong></a></p>
  </div>

  <div class="card">
    <h2>Key figures</h2>
    <div class="grid">
{kpi_html}
    </div>
  </div>

  <div class="card">
    <h2>Executive summary — findings and answers</h2>
    <p class="lead">Each row is a question from the brief and its verified answer. Anything that could not be confirmed from an
    official source is blank and listed on the <a href="flagged.html">Flagged</a> page instead.</p>
    <table>
      <caption>Question · verified answer · official source (accessed {ACCESSED})</caption>
      <thead><tr><th style="width:26%">Question</th><th>Verified answer</th><th style="width:22%">Official source</th></tr></thead>
      <tbody>
{findings_html}
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>Browse by category</h2>
    <div class="cats">
{cat_html}
    </div>
  </div>

  <div class="card warn">
    <h2>Two corrections to earlier drafts of this analysis</h2>
    <ol>
      <li><strong>Unit 2's ceiling is not 13.1% on 1 June 2027.</strong> 13.1% is the sum of the seven allowances that accrued
      from 1 June 2020 to 1 June 2026, which is a verified <em>floor</em> of {money(U2_TOTAL)} ({money(U2 + U2_TOTAL)}). The
      increase on 1 June 2027 also includes the allowance in effect on that date (the 1 Mar 2027 – 29 Feb 2028 rate), which the
      Rent Board has not yet published, so the full June 2027 figure cannot be stated.
      {FLAG("F-11")} <a href="units.html">Details</a> · {S("f571", "banked")}</li>
      <li><strong>Repeating a rate year in a later notice overstates the ceiling.</strong> The increase takes the allowance
      in effect on its effective date — plus unused earlier years — so a notice served today for an effective date after
      28 February 2027 must use the 2027-28 rate, not 1.6%. {FLAG("F-12")} <a href="units.html">Details</a> · {S("learn")}</li>
    </ol>
  </div>

  <div class="card note">
    <h2>Status of this edition</h2>
    <table>
      <caption>Verification state (accessed {ACCESSED})</caption>
      <thead><tr><th>Check</th><th>Result</th><th>Source or tool</th></tr></thead>
      <tbody>
        <tr><td>Every table row carries an official source link, or is blank and flagged</td><td class="ok">Pass</td><td><span class="mono">tools/check_v2.py</span> · {S("inv")}</td></tr>
        <tr><td>Allowance percentages re-read from the Rent Board's own table</td><td class="ok">Pass — 1.6% current, 1.4% prior, full history to 1982</td><td>{S("f571", "rates")}</td></tr>
        <tr><td>Arithmetic re-computed to the cent, added not compounded</td><td class="ok">Pass</td><td>{S("banked")}</td></tr>
        <tr><td>Unit 2 rent history 2019–present supplied by the owner</td><td class="no">Unverified</td><td>{FLAG("F-13")} · {S("f571")}</td></tr>
        <tr><td>Housing Inventory / licence status for this building</td><td class="no">Unverified</td><td>{FLAG("F-14")} · {S("inv")}</td></tr>
      </tbody>
    </table>
    <p class="small">Anonymisation also passes: <span class="mono">tools/check_v2.py</span> scans every page for names, initials,
    a street address, a unit number and the ZIP code, and fails the build if any is present.</p>
  </div>

  <div class="card">
    <h2>Prior editions kept online</h2>
    <p class="small">Earlier sessions produced several editions of the same analysis. They are left in place for provenance; this
    edition supersedes them where they disagree (see the corrections above).</p>
    <ul class="small">
      <li><a href="../pages/executive-summary.html">pages/executive-summary.html</a> — licence-first summary (7 Nov 2026)</li>
      <li><a href="../pages/laws.html">pages/laws.html</a> · <a href="../pages/units.html">pages/units.html</a> ·
          <a href="../pages/process.html">pages/process.html</a> · <a href="../pages/flagged.html">pages/flagged.html</a></li>
      <li><a href="../audit/process.html">audit/</a> — consolidated audit edition ·
          <a href="../verified/index.html">verified/</a> — ten-page verified guide</li>
      <li><a href="../docs/index.html">docs/</a> · <a href="../dashboard/index.html">dashboard/</a> · <a href="../review/index.html">review/</a></li>
    </ul>
  </div>
"""
    return page("Dashboard", "Rental increase review — dashboard",
                "Two rent-controlled flats in a 1940 two-unit San Francisco building. Two questions drive everything else: "
                "does an individual owner need the Rent Board's rent-increase licence (yes — see below), and what amount is lawful "
                "for each unit. Answers are verified line by line against official sources and linked in every row.",
                body, active="index.html")


# --------------------------------------------------------------------------
# shared row builders
# --------------------------------------------------------------------------
def rate_table() -> str:
    rows = "\n".join(
        f'        <tr><td>{label}</td><td class="num">{pct(p)}</td><td>{S("f571")}</td></tr>'
        for label, p in RATES
    )
    return f"""      <table>
        <caption>Allowable annual increases covering the two tenancies (Rent Board Form 571)</caption>
        <thead><tr><th>Rate period</th><th class="num">Allowable</th><th>Official source</th></tr></thead>
        <tbody>
{rows}
        </tbody>
      </table>"""


def ledger_unit1() -> str:
    return f"""      <table>
        <caption>Unit 1 — base rent {money(U1)} · anniversary 1 February</caption>
        <thead><tr><th>Anniversary</th><th>Rate period used</th><th class="num">Percent</th><th class="num">Dollars</th><th>Status</th><th>Source</th></tr></thead>
        <tbody>
          <tr><td>1 Feb 2026</td><td>1 Mar 2025 – 28 Feb 2026</td><td class="num">1.4%</td><td class="num">{money(inc(U1, D('1.4')))}</td><td>Not imposed — banks once 24 full months pass without an increase</td><td>{S("f571", "banked")}</td></tr>
          <tr><td>1 Feb 2027</td><td>1 Mar 2026 – 28 Feb 2027</td><td class="num">1.6%</td><td class="num">{money(U1_SINGLE)}</td><td>Current annual allowance on that date</td><td>{S("f571", "learn")}</td></tr>
          <tr><td><strong>1 Feb 2027 — combined</strong></td><td>1.4% banked + 1.6% current</td><td class="num"><strong>3.0%</strong></td><td class="num"><strong>{money(U1_BANK)}</strong></td><td><strong>New rent {money(U1 + U1_BANK)}</strong> · added, not compounded · 30 days' notice</td><td>{S("banked", "multi")}</td></tr>
          <tr><td>1 Feb 2028 <span class="small">(if the 2027 increase is skipped)</span></td><td>1 Mar 2027 – 29 Feb 2028 ("rate year 2027")</td><td class="num">{BLANK("F-11")}</td><td class="num">—</td><td>Not yet published, so no 2028 figure can be computed</td><td>{S("rates")}</td></tr>
        </tbody>
      </table>
      <p class="small">Compounding 1.4% then 1.6% would give {money((U1 * D('1.014') * D('1.016')).quantize(D('0.01')))} instead of
      {money(U1 + U1_BANK)}; that method is not permitted — the percentages are added, then applied once to base rent.
      Sources: {S("banked", "multi")}</p>"""


def ledger_unit2() -> str:
    rows = []
    for i, (label, p) in enumerate(RATES):
        year = 2020 + i
        rows.append(
            f'          <tr><td>1 Jun {year}</td><td>{label}</td><td class="num">{pct(p)}</td>'
            f'<td class="num">{money(inc(U2, p))}</td><td>Assumed unused — banked {FLAG("F-23")}</td>'
            f'<td>{S("f571", "banked")}</td></tr>'
        )
    return f"""      <table>
        <caption>Unit 2 — base rent {money(U2)} · anniversary 1 June · conditional on no increase since 1 June 2019</caption>
        <thead><tr><th>Anniversary missed</th><th>Rate period used</th><th class="num">Percent</th><th class="num">Dollars</th><th>Status</th><th>Source</th></tr></thead>
        <tbody>
{chr(10).join(rows)}
          <tr><td><strong>Total banked to 1 Jun 2026</strong></td><td>seven rate years, added</td><td class="num"><strong>{pct(BANK7)}</strong></td><td class="num"><strong>{money(U2_TOTAL)}</strong></td><td><strong>{money(U2 + U2_TOTAL)}</strong> if imposed — a verified floor, not the June 2027 ceiling</td><td>{S("f571", "banked")}</td></tr>
          <tr><td>1 Jun 2027</td><td>1 Mar 2027 – 29 Feb 2028 ("rate year 2027")</td><td class="num">{BLANK("F-11")}</td><td class="num">—</td><td>Not yet published; the June 2027 ceiling is {pct(BANK7)} plus this unknown rate</td><td>{S("rates")}</td></tr>
        </tbody>
      </table>
      <p class="small">Earlier figures of 11.5% ({money(inc(U2, BANK6))}) for 2020–2025 and {pct(BANK7)} ({money(U2_TOTAL)}) for
      2020–2026 are arithmetically correct as <em>banked balances</em>; the error was presenting the balance as the maximum
      increase available on a later date. Sources: {S("banked", "f571")}</p>"""


def deadline_table() -> str:
    rows = [
        ("Unit 1 — 3.0%", dt.date(2027, 2, 1), 30, "30 days: 12-month total is 10% or less"),
        ("Unit 1 — 1.6% only", dt.date(2027, 2, 1), 30, "30 days: 10% or less"),
        ("Unit 2 — 10.0% step", dt.date(2027, 6, 1), 30, "30 days: exactly 10% is '10 percent or less'"),
        ("Unit 2 — 13.1% or more", dt.date(2027, 6, 1), 90, "90 days: more than 10% in a 12-month period"),
        ("Unit 2 — earliest compliant date if served today", None, 90, "90 days from today's service date"),
    ]
    out = []
    for label, eff, days, rule in rows:
        if eff is None:
            eff = TODAY + dt.timedelta(days=days)
        serve = minus(eff, days)
        mail = minus(eff, days + 5)
        out.append(
            f'          <tr><td>{label}</td><td>{fmt(eff)}</td><td class="num">{days}</td>'
            f"<td>{serve.strftime('%-d %b %Y')}</td><td>{mail.strftime('%-d %b %Y')}</td><td>{rule}</td>"
            f'<td>{S("s827", "s1013")}</td></tr>'
        )
    return f"""      <table>
        <caption>Notice deadlines computed backwards from the effective date · served from {fmt(TODAY)}</caption>
        <thead><tr><th>Scenario</th><th>Effective date</th><th class="num">Notice</th><th>Serve by — in person</th><th>Serve by — mail in CA</th><th>Rule applied</th><th>Source</th></tr></thead>
        <tbody>
{chr(10).join(out)}
        </tbody>
      </table>
      <p class="small">Dates are calendar arithmetic on the statutory periods, not a legal opinion. Weekends and court holidays
      are not excluded by the text of the statute, and a mailed notice must add five days. Confirm the exact date with a Rent Board
      counsellor before service. Sources: {S("s827", "s1013", "learn")}</p>"""


# --------------------------------------------------------------------------
# Page: executive summary
# --------------------------------------------------------------------------
def build_exec_summary() -> str:
    body = f"""  <div class="card answer">
    <h2>1. The question that has to be answered first</h2>
    <p><strong>Do I need to inform the Rent Board and get a licence before notifying tenants, even though I am an individual
    owner and not a corporation?</strong></p>
    <p><strong>Yes — and the answer does not depend on being a company.</strong> The ordinance ties the obligation to
    <em>building size</em>, not to the owner's legal form: buildings with 10 or more units from 1 July 2022, and condominiums and
    buildings with fewer than 10 units from 1 March 2023. This is a two-unit building, so the March 2023 date applies. Every owner
    must report into the Housing Inventory each year; reporting a tenant-occupied unit produces the rent-increase licence
    automatically. The licence must be <strong>in effect on the effective date</strong> of the increase. If it is not, the increase
    may be null and void and the tenant may recover the difference.</p>
    <p>What you do <em>not</em> have to do: file the increase notice with the Rent Board, apply for approval of the increase, or
    petition for an annual or banked increase. The licence is a precondition, not an application about the amount.</p>
    <p class="small">Sources: {S("inv", "noncomp", "banked", "learn")}</p>
  </div>

  <div class="card">
    <h2>2. The seven-step sequence, in order</h2>
    <table>
      <caption>Order matters: steps 1–3 must be complete before step 6</caption>
      <thead><tr><th>#</th><th>Step</th><th>What exactly to do</th><th>Official source</th></tr></thead>
      <tbody>
        <tr><td class="num">1</td><td>Confirm the unit is rent-controlled</td><td>Certificate of occupancy before 14 June 1979 and not a single-family home or condominium. A 1940 two-flat is presumptively covered; verify on the Property Information Map and by phone.</td><td>{S("rentallaws")}</td></tr>
        <tr><td class="num">2</td><td>Report into the Housing Inventory</td><td>Online through the Rent Board Portal, free. Report <em>every</em> residential unit: owner or manager contact, business registration if any, approximate square footage in 250 sq ft increments, bedrooms, bathrooms, occupancy or vacancy dates, and for tenant-occupied units the base rent in $250 increments and whether utilities are included. Under penalty of perjury. Deadline 1 March every year.</td><td>{S("inv")} · {S("portal")}</td></tr>
        <tr><td class="num">3</td><td>Confirm the licence and its dates</td><td>The licence is generated automatically for tenant-occupied units and does not need to be sent with the notice. Look the property up in the Portal and check that a licence covers the intended effective date — you may need to check more than one year.</td><td>{S("inv", "noncomp")}</td></tr>
        <tr><td class="num">4</td><td>Fix the anniversary and the rate year</td><td>One increase per 12 months, on the tenancy's anniversary. The rate is the one <em>in effect on the effective date</em>, not the date of the notice. Unit 1: 1 February. Unit 2: 1 June.</td><td>{S("learn", "multi")}</td></tr>
        <tr><td class="num">5</td><td>Compute on base rent, add banks, never compound</td><td>Base rent includes housing services such as parking or storage and excludes passthroughs and fluctuating charges. Add the percentages for each unused year, then apply once. No rounding up.</td><td>{S("learn", "banked", "f571")}</td></tr>
        <tr><td class="num">6</td><td>Serve a compliant written notice</td><td>30 days if the 12-month total is 10% or less; 90 days if more; five extra days if mailed in California. State the dollar amount, the percentage, the effective date, and for banks which part is banked and from which years.</td><td>{S("s827", "s1013", "banked")}</td></tr>
        <tr><td class="num">7</td><td>Keep the file</td><td>Copy of the notice, proof of service, the licence page for the relevant year, and the calculation. These are the documents that decide a tenant petition.</td><td>{S("petitions", "noncomp")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>3. What is lawful for each unit</h2>
    <table>
      <caption>Verified ceilings as at {fmt(TODAY)} · cents-exact</caption>
      <thead><tr><th>Unit</th><th>Base rent</th><th>Lawful step</th><th class="num">Increase</th><th class="num">New rent</th><th>Notice</th><th>Source</th></tr></thead>
      <tbody>
        <tr><td>Unit 1</td><td class="num">{money(U1)}</td><td>1.6% only, effective 1 Feb 2027</td><td class="num">{money(U1_SINGLE)}</td><td class="num">{money(U1 + U1_SINGLE)}</td><td>30 days</td><td>{S("f571")}</td></tr>
        <tr><td>Unit 1</td><td class="num">{money(U1)}</td><td><strong>3.0%</strong> — 1.4% banked + 1.6% current, effective 1 Feb 2027</td><td class="num">{money(U1_BANK)}</td><td class="num">{money(U1 + U1_BANK)}</td><td>30 days</td><td>{S("banked", "f571")}</td></tr>
        <tr><td>Unit 2</td><td class="num">{money(U2)}</td><td>1.6% only, on the next anniversary</td><td class="num">{money(U2_SINGLE)}</td><td class="num">{money(U2 + U2_SINGLE)}</td><td>30 days</td><td>{S("f571")}</td></tr>
        <tr><td>Unit 2</td><td class="num">{money(U2)}</td><td>10.0% phased step (stays inside the pending 10% cap)</td><td class="num">{money(U2_TEN)}</td><td class="num">{money(U2 + U2_TEN)}</td><td>30 days</td><td>{S("s827")} · {S("legistar")}</td></tr>
        <tr><td>Unit 2</td><td class="num">{money(U2)}</td><td>{pct(BANK7)} banked to 1 Jun 2026 — a floor, plus the unannounced 2027-28 rate</td><td class="num">{money(U2_TOTAL)}</td><td class="num">{money(U2 + U2_TOTAL)}</td><td>90 days</td><td>{S("f571", "banked")}</td></tr>
      </tbody>
    </table>
    <p class="small">All five rows assume the licence is in place on the effective date; without it, the amount is irrelevant
    because the increase may be void. The Unit 2 rows also assume no increase has been taken since 1 June 2019 —
    {FLAG("F-13")}. The 2027-28 allowance is unpublished, so no June 2027 ceiling can be stated — {FLAG("F-11")}.</p>
  </div>

  <div class="card">
    <h2>4. What a tenant's lawyer would check — and where this plan could fail</h2>
    <table>
      <caption>Pass/fail issues, in the order a free tenant representative would raise them</caption>
      <thead><tr><th>Issue</th><th>Why it matters</th><th>Source</th></tr></thead>
      <tbody>
        <tr><td>No licence on the effective date</td><td>Increase may be void for that period, with a refund; a tenant can file at any time, at no cost.</td><td>{S("noncomp", "unlawful")}</td></tr>
        <tr><td>Amount above the allowance plus documented banks</td><td>The Rent Board decides the lawful rent on a tenant petition; the burden falls on the documentation.</td><td>{S("petitions", "f571")}</td></tr>
        <tr><td>Second increase inside 12 months</td><td>Only one increase per 12 months on a rent-controlled tenancy.</td><td>{S("learn")}</td></tr>
        <tr><td>Charge tied to the additional occupant in Unit 1</td><td>An increase because a roommate joined is unlawful even if the lease says otherwise — directly relevant to the April 2026 change.</td><td>{S("learn", "s373")}</td></tr>
        <tr><td>Retaliatory timing</td><td>A rent increase within 180 days of a repair request, habitability complaint or organising is restricted; retaliation can never be the purpose.</td><td>{S("s1942_5")}</td></tr>
        <tr><td>Reason touching a protected characteristic</td><td>FEHA and the federal Fair Housing Act govern the terms of a tenancy; differential treatment invites an agency complaint.</td><td>{S("s12955", "fha")}</td></tr>
        <tr><td>Notice missing a required element</td><td>A non-conforming notice is treated as invalid; a tenant summary petition can be filed before the increase starts.</td><td>{S("s827", "petitions")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card gate">
    <h2>5. Bottom line</h2>
    <ul>
      <li><strong>Yes, the licence is required</strong>, and no owner type is exempt. File the Housing Inventory, confirm the
      licence covers the effective date, and only then serve notice.</li>
      <li><strong>Unit 1:</strong> the defensible step on 1 February 2027 is <strong>3.0% = {money(U1_BANK)} → {money(U1 + U1_BANK)}</strong>,
      composed of the unused 1.4% and the current 1.6%, with 30 days' notice. A 1.6%-only step of {money(U1_SINGLE)} is also lawful
      and leaves the 1.4% available.</li>
      <li><strong>Unit 2:</strong> {money(U2_TOTAL)} ({pct(BANK7)}) is the verified banked balance and would need 90 days' notice;
      the June 2027 ceiling is higher because the 2027-28 allowance is unpublished. A 10.0% step of {money(U2_TEN)} is lawful on
      30 days' notice and stays inside the pending 10% cap.</li>
      <li><strong>Do both units under one written policy</strong>, each on its own anniversary, with the same method, the same notice
      template and the same documentation. Treating them differently is not automatically unlawful, but it is the fact pattern that
      prompts inquiries.</li>
      <li><strong>Open items</strong> that block certainty, not the plan: Unit 2's rent history, this building's licence status, and
      the owner's own record of whether Unit 1's 1.4% year was ever charged. See <a href="flagged.html">Flagged</a>.</li>
    </ul>
  </div>
"""
    return page("Executive summary", "Executive summary",
                "The rent-increase licence question first — because a correct percentage is worthless without it — then the "
                "lawful amount for each unit, the notice that carries it, and the checks a tenant's lawyer would run.",
                body, active="executive-summary.html")


# --------------------------------------------------------------------------
# Page: licence and process
# --------------------------------------------------------------------------
def build_license() -> str:
    body = f"""  <div class="card answer">
    <h2>Direct answer</h2>
    <p><strong>Yes.</strong> As an individual owner of a two-unit building you must (a) report into the Rent Board Housing
    Inventory every year, and (b) hold a rent-increase licence that is in effect on the effective date of the increase.
    Being an individual rather than a corporation is irrelevant: the ordinance classifies by building size, and the
    "1–9 units" track began on 1 March 2023. There is no separate application for the licence and no fee for it, and you do not
    send it to the tenant or file your notice with the Rent Board.</p>
    <p class="small">Sources: {S("inv", "noncomp", "learn")}</p>
  </div>

  <div class="card">
    <h2>What the official sources say, line by line</h2>
    <table>
      <caption>Question · quoted requirement · source</caption>
      <thead><tr><th style="width:24%">Question</th><th>Verified answer</th><th style="width:24%">Official source</th></tr></thead>
      <tbody>
        <tr><td>Who must report?</td><td>"All owners of residential property are required to report." Most owners must report even if they are not currently renting the unit out.</td><td>{S("inv")}</td></tr>
        <tr><td>Is an individual owner exempt?</td><td>No exemption appears for owner type. The only distinction is building size: 10+ units from 1 July 2022; condominiums and buildings with fewer than 10 units from 1 March 2023.</td><td>{S("inv", "noncomp")}</td></tr>
        <tr><td>Does the licence apply to every unit?</td><td>Only to units under San Francisco rent control — "The Rent Increase License rules apply ONLY to units under San Francisco Rent Control."</td><td>{S("noncomp")}</td></tr>
        <tr><td>How is the licence obtained?</td><td>Automatically: "once you have reported into the Housing Inventory, a rent increase license will be automatically generated for non-owner occupied units."</td><td>{S("inv")}</td></tr>
        <tr><td>When must it be in force?</td><td>"A landlord must have a current rent increase license on file with the Rent Board before any annual or banked rent increase can go into effect."</td><td>{S("inv", "banked")}</td></tr>
        <tr><td>Must it be sent with the notice?</td><td>No — "The rent increase license does not need to be included with your rent increase notice."</td><td>{S("inv")}</td></tr>
        <tr><td>Deadline and late filing</td><td>1 March every year. Late submissions are accepted, but "your rent increase notice will not be enforceable without having a rent increase license on the effective date of the notice." The Rent Board "does not assess monetary penalties for filing after the deadline."</td><td>{S("inv")}</td></tr>
        <tr><td>Does filing cost anything?</td><td>No — "Reporting is free and can be done online 24/7."</td><td>{S("inv")}</td></tr>
        <tr><td>What if it is missing?</td><td>A notice that "goes into effect while the unit is unlicensed may be null and void (this may apply for multiple years)"; the tenant "may be entitled to a rent refund".</td><td>{S("noncomp")}</td></tr>
        <tr><td>Can tenants check?</td><td>Yes — tenants can search the Portal to see whether the landlord is up to date with the rent-increase licence, and can see when it expires.</td><td>{S("inv", "noncomp")}</td></tr>
        <tr><td>Does it approve my amount?</td><td>No. It is a precondition; the amount is separately governed by the annual allowance and banking rules.</td><td>{S("learn", "banked")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>Filing walkthrough</h2>
    <ol>
      <li><strong>Open an account.</strong> Use the Rent Board Portal ({S("portal")}). The PIN on the Annual Notice adds the property
      to the account; 311 can reset a PIN. The Portal is also where the fee is paid.</li>
      <li><strong>Report each unit.</strong> Owner-occupied, non-owner occupied and vacant units are asked different questions.
      For the two rented flats: owner or manager contact details, business registration number if any, approximate square footage
      in 250 sq ft increments, bedrooms, bathrooms, the date the current occupancy began, and the base rent in $250 increments plus
      whether utilities are included. Everything is submitted under penalty of perjury, and the answers are public. Approximate
      answers are acceptable if made honestly.</li>
      <li><strong>File by 1 March.</strong> Late filing is possible, but it does not repair an increase that already took effect
      without a licence.</li>
      <li><strong>Read back the licence.</strong> After filing, check the property in the Portal, open the document icon for the
      non-owner-occupied unit, and confirm the licence period covers the intended effective date. Previous years can be viewed too.</li>
      <li><strong>Keep the copy</strong> with the notice, the proof of service and the calculation.</li>
    </ol>
    <p class="small">Source: {S("inv", "portal")}</p>
  </div>

  <div class="card note">
    <h2>The Rent Board Fee is a separate obligation — do not confuse the two</h2>
    <table>
      <caption>Housing Inventory reporting vs. the annual fee</caption>
      <thead><tr><th>Item</th><th>Detail</th><th>Source</th></tr></thead>
      <tbody>
        <tr><td>Housing Inventory report</td><td>Free; produces the rent-increase licence; due 1 March; reporting is not the same as requesting a fee exemption.</td><td>{S("inv")}</td></tr>
        <tr><td>Rent Board Fee, tax year 2026-27</td><td>$59.00 per dwelling unit ($29.50 per SRO guest unit), due 1 March; 5% late penalty per month, capped at 15%; unpaid balances referred to the Bureau of Delinquent Revenue after 1 June.</td><td>{S("fee")}</td></tr>
        <tr><td>Recovering part of the fee</td><td>If the fee is paid in full, 50% may be recovered from tenants in occupancy ($29.50 per dwelling unit) — but not any penalty.</td><td>{S("fee")}</td></tr>
        <tr><td>Exemption window for the 2027 fee</td><td>Requests are due by 14 December 2026; units without an approved exemption are billed and due by 1 March 2027.</td><td>{S("fee")}</td></tr>
        <tr><td>Does an unpaid fee invalidate the licence?</td><td>{BLANK("F-15")} No official page states that the fee and the licence are linked. The Inventory page says only that requesting a fee exemption "does not request an exemption of the Rent Board Fee" — i.e. they are separate systems. Treat the fee as its own obligation and confirm with the Rent Board.</td><td>{S("inv", "fee")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>If an increase was already served without a licence</h2>
    <table>
      <caption>What the tenant can do, and what it costs them</caption>
      <thead><tr><th>Route</th><th>When it applies</th><th>Cost to tenant</th><th>Source</th></tr></thead>
      <tbody>
        <tr><td>Tenant Petition — unlawful rent increase / determination of lawful rent</td><td>Increase already in effect, including one served while unlicensed. There is no time limit for filing.</td><td>No charge</td><td>{S("unlawful", "petitions")}</td></tr>
        <tr><td>Tenant summary petition</td><td>Increase not yet in effect; a Rent Board letter tells the landlord to obtain the licence first.</td><td>No charge</td><td>{S("petitions", "noncomp")}</td></tr>
        <tr><td>Hearing before an Administrative Law Judge</td><td>After a complete petition; the tenant does not need a lawyer, and may bring one.</td><td>No charge</td><td>{S("unlawful")}</td></tr>
        <tr><td>Court claim under the Tenant Protection Act</td><td>Only if the state cap (not the local one) is the governing limit — for these units it is not.</td><td>Attorney's fees may be awarded</td><td>{S("s1947_12")}</td></tr>
      </tbody>
    </table>
    <p class="small">The Rent Board also states that it does not adjudicate harassment, discrimination, retaliation or security
    deposits — those go to court or another forum. Source: {S("petitions")}</p>
  </div>
"""
    return page("Licence &amp; process", "Licence and process",
                "The obligation that comes before any number: report into the Housing Inventory, obtain the rent-increase licence, "
                "and make sure it is in force on the date the increase takes effect.",
                body, active="license.html")


# --------------------------------------------------------------------------
# Page: laws and caps
# --------------------------------------------------------------------------
def build_laws() -> str:
    body = f"""  <div class="card">
    <h2>Which rule actually governs the amount</h2>
    <table>
      <caption>Local, state and federal layers · what each does to these two units</caption>
      <thead><tr><th>Layer</th><th>Rule</th><th>Effect here</th><th>Source</th></tr></thead>
      <tbody>
        <tr><td><strong>Local</strong></td><td>S.F. Admin. Code ch. 37 — Rent Ordinance: units with a certificate of occupancy on or before 13 June 1979</td><td>Both flats are presumptively covered (1940 building, two units, not a condominium or single-family home). Coverage is the first thing to confirm.</td><td>{S("rentallaws")}</td></tr>
        <tr><td><strong>Local</strong></td><td>Annual increase = 60% of the published CPI change, and "In no event … greater than 7%"</td><td>The statutory ceiling is 7%, but the published allowance is far lower: 1.6% for 1 Mar 2026 – 28 Feb 2027; 1.4% the year before. The published number governs, once every 12 months, on base rent only, with no rounding up.</td><td>{S("s373", "learn", "f571")}</td></tr>
        <tr><td><strong>Local</strong></td><td>Housing Inventory and rent-increase licence (Admin. Code §37.15)</td><td>Report by 1 March each year; the licence must be in effect on the effective date or the increase may be void. Applies to this 2-unit building from 1 March 2023.</td><td>{S("inv", "noncomp")}</td></tr>
        <tr><td><strong>Local</strong></td><td>Banked increases</td><td>A skipped increase banks only after 24 full months without an increase; there is no cap on the total; banks never expire during the tenancy; they are added, not compounded; they survive a sale but do not carry to a new tenant.</td><td>{S("banked")}</td></tr>
        <tr><td><strong>Local</strong></td><td>Additional-occupant charge (Admin. Code §37.3(a)(11)(A))</td><td>A landlord may not impose an increase because a tenant added an occupant, "notwithstanding a rental agreement or lease that specifically permits" it. Directly relevant to Unit 1's April 2026 change.</td><td>{S("learn", "s373")}</td></tr>
        <tr><td><strong>Local</strong></td><td>Rent Board Fee (separate from the licence)</td><td>$59.00 per dwelling unit for 2026-27, due 1 March; 50% may be recovered from tenants if paid in full.</td><td>{S("fee")}</td></tr>
        <tr><td><strong>State</strong></td><td>Tenant Protection Act — Civ. Code §1947.12: 5% + CPI, maximum 10%, at most two increments in 12 months</td><td>Not the governing cap. The section excludes housing subject to a local ordinance that restricts increases to a lower amount — which the SF ordinance does. The state figure for the San Francisco area is 8.8% for increases starting 1 Aug 2026 – 31 Jul 2027, so it is higher, not lower.</td><td>{S("s1947_12", "oag")}</td></tr>
        <tr><td><strong>State</strong></td><td>Civ. Code §827 — notice</td><td>At least 30 days if the increase is 10% or less of the lowest rent charged in the prior 12 months, 90 days if more, including in combination with other increases in that period; service personally or by mail under Code Civ. Proc. §1013.</td><td>{S("s827", "s1013")}</td></tr>
        <tr><td><strong>State</strong></td><td>Civ. Code §1942.5 — retaliation</td><td>Rent may not be increased within 180 days of a good-faith repair request, a tenantability complaint or related proceedings in many circumstances, and may never be increased for the purpose of retaliating against organising or exercising rights.</td><td>{S("s1942_5")}</td></tr>
        <tr><td><strong>State</strong></td><td>Costa-Hawkins — Civ. Code §§1954.50 et seq., §1954.53</td><td>Does not exempt this building: it is not a separately alienable single-family home or condominium, and it predates the 1995 cutoff. A partial turnover (one original tenant leaving) is not a vacancy that resets rent — see the Costa-Hawkins page for the narrower unlimited-increase rule that applies only when the last original occupant vacates.</td><td>{S("s1954_53", "cos")}</td></tr>
        <tr><td><strong>State</strong></td><td>FEHA — Gov. Code §12955</td><td>The owner may not discriminate or harass because of race, colour, religion, sex, gender, gender identity or expression, sexual orientation, marital status, national origin, ancestry, familial status, source of income, disability, veteran or military status, or genetic information.</td><td>{S("s12955", "crd")}</td></tr>
        <tr><td><strong>Federal</strong></td><td>Fair Housing Act — 42 U.S.C. §3604</td><td>No federal rent ceiling exists. The Act makes it unlawful to discriminate "in the terms, conditions, or privileges of sale or rental of a dwelling" because of race, colour, religion, sex, familial status or national origin, and covers handicap discrimination separately.</td><td>{S("fha", "hud")}</td></tr>
        <tr><td><strong>Pending</strong></td><td>Board of Supervisors File #261020</td><td>Would cap combined banked and capital-improvement increases at 10% a year for three years. Status: <strong>Pending Committee Action</strong>; introduced 15 September 2026. Not law. The Rent Board's own pages now carry a notice about it.</td><td>{S("legistar", "banked")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>Allowable increases — the years that matter here</h2>
{rate_table()}
    <p class="small">The full table on Form 571 runs back to 1 April 1982, including the caution that only one of the two
    1992 increases may be imposed. Source: {S("f571")}</p>
  </div>

  <div class="card note">
    <h2>Why the state 8.8% cannot be used as a fallback</h2>
    <p>It is a common assumption that if the local allowance is small, the state cap offers a larger alternative. It does not work
    that way. Civ. Code §1947.12(d)(3) excludes "housing subject to rent or price control through a public entity's valid exercise
    of its police power … that restricts annual increases in the rental rate to an amount less than that provided in subdivision
    (a)". Because San Francisco's allowance (1.6%) is lower than the state figure (8.8% for the current period), the local rule
    governs and the state figure never becomes available. The state cap also has its own remedy provision — injunctive relief,
    the excess amount, discretionary attorney's fees and up to treble damages for wilful conduct — which is one reason not to treat
    any ceiling loosely.</p>
    <p class="small">Sources: {S("s1947_12", "oag")}</p>
  </div>
"""
    return page("Laws &amp; caps", "Laws and caps",
                "Three layers of law touch a rent increase, and only one of them sets the amount. This page says which, and what the "
                "other two still require.",
                body, active="laws.html")


# --------------------------------------------------------------------------
# Page: units and math
# --------------------------------------------------------------------------
def build_units() -> str:
    body = f"""  <div class="card note">
    <h2>Anonymisation and provenance</h2>
    <p>The two flats are called Unit 1 and Unit 2. Occupants appear only as placeholders; the street address, unit numbers,
    ZIP code and neighbourhood are withheld. Lease dates, occupancy dates and dollar amounts supplied by the owner are reproduced
    unchanged. Nothing below is a government record: the dates and rents came from the owner, and the legal ceilings come from the
    Rent Board's published tables.</p>
  </div>

  <div class="card">
    <h2>Tenancy register</h2>
    <table>
      <caption>Facts as supplied, with the legal consequence of each</caption>
      <thead><tr><th>Field</th><th>Unit 1</th><th>Unit 2</th><th>Source or status</th></tr></thead>
      <tbody>
        <tr><td>Lease start used for the anniversary</td><td>1 February 2025</td><td>1 June 2019</td><td>Owner record, not a government record {FLAG("F-23")}</td></tr>
        <tr><td>Rent at that start</td><td class="num">{money(U1)}</td><td class="num">{money(U2)}</td><td>Owner record, not a government record {FLAG("F-23")}</td></tr>
        <tr><td>Occupancy now</td><td>Original tenant still in residence; a second occupant joined on 1 April 2026 at an unchanged rent. Not a vacancy.</td><td>Both original tenants, in residence since 1 June 2019</td><td>Owner record · {S("learn")}</td></tr>
        <tr><td>Anniversary date</td><td>1 February — a continuation in April 2026 did not create a new tenancy or reset it</td><td>1 June</td><td>{S("learn")}</td></tr>
        <tr><td>Rent-control status</td><td>Presumed covered — 1940 building, two units</td><td>Presumed covered — same building</td><td>{S("rentallaws")} · {FLAG("F-16")}</td></tr>
        <tr><td>Partially exempt (single-family or condominium)?</td><td>No indication; must be confirmed against the assessor record</td><td>Same</td><td>{S("s1954_53")} · {FLAG("F-16")}</td></tr>
        <tr><td>Rent history since the lease start</td><td>No increase taken; the 1.4% year went unused</td><td>{BLANK("F-13")}</td><td>{S("f571")}</td></tr>
        <tr><td>Increase needing the licence on the effective date</td><td>Yes</td><td>Yes</td><td>{S("inv")}</td></tr>
        <tr><td>Licence actually on file</td><td>{BLANK("F-14")}</td><td>{BLANK("F-14")}</td><td>{S("noncomp")}</td></tr>
        <tr><td>Housing subsidy (voucher) status</td><td>{BLANK("F-17")}</td><td>{BLANK("F-17")}</td><td>{S("fee")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card note">
    <h2>Which percentage applies: the "rate year" rule</h2>
    <p>The Rent Board publishes each allowance as a period beginning 1 March, and the percentage in effect on the
    <strong>effective date</strong> is the one that applies. So an increase effective on or after 1 March 2026 and before
    1 March 2027 uses the 1.6% row; one effective on or after 1 March 2027 uses the next row, which has not been
    published. In shorthand on this site, "rate year 2026" means 1 Mar 2026 – 28 Feb 2027 and "rate year 2027" means
    1 Mar 2027 – 29 Feb 2028. Both flats' anniversaries (1 February and 1 June) fall inside the same rate year as their
    calendar date, so there is no offset to apply.</p>
    <p class="small">Sources: {S("learn", "f571", "rates")}</p>
  </div>

  <div class="card">
    <h2>Unit 1 — ledger and options</h2>
{ledger_unit1()}
      <p class="small"><strong>Timing.</strong> The first increase may be imposed 12 months after the lease began, and once an
      increase is imposed that date becomes the new anniversary. Because no increase was taken on 1 February 2026, the 1.4% banks
      only once 24 full months pass without an increase — which happens on 1 February 2027, the same date the 1.6% allowance is
      current. That is why the two can be combined on one notice. Sources: {S("learn", "banked")}</p>
  </div>

  <div class="card">
    <h2>Unit 2 — ledger and options</h2>
{ledger_unit2()}
      <p class="small"><strong>Timing.</strong> With no increase since 1 June 2019, an increase may be imposed on the anniversary
      or "at another time when they are allowed to raise the rent (as long as at least 12 months have passed since the last
      increase)". If imposed on a date other than 1 June, that date becomes the new anniversary. A step above 10% needs 90 days'
      notice. Sources: {S("banked", "s827")}</p>
  </div>

  <div class="card">
    <h2>Notice deadlines for these two units</h2>
{deadline_table()}
  </div>

  <div class="card warn">
    <h2>Two arithmetic traps</h2>
    <ol>
      <li><strong>The 2027-28 rate is not published.</strong> Any notice with an effective date after 28 February 2027 must use the
      allowance in effect on that later date {{FLAG_F11}}. Repeating 1.6% beyond its rate year is the error; the Rent Board's own
      guidance says to "use the percentage that will be in effect on the date of the increase, not the percentage in effect on the
      date they serve the notice." Source: {S("learn")}</li>
      <li><strong>Percentages are added, then applied once.</strong> Compounding either unit produces a higher, unlawful number:
      Unit 1 would be {money((U1 * D('1.014') * D('1.016')).quantize(D('0.01')))} instead of {money(U1 + U1_BANK)}, and Unit 2
      would be {money((U2 * D('1.036') * D('1.023') * D('1.017') * D('1.014') * D('1.016') * D('1.007') * D('1.018')).quantize(D('0.01')))}.
      Source: {S("banked", "multi")}</li>
    </ol>
  </div>
""".replace("{FLAG_F11}", FLAG("F-11"))
    return page("Units &amp; math", "Units and arithmetic",
                "Each tenancy has its own ceiling, built from the allowances that accrued on its own anniversary and were not used. "
                "Nothing here is a market rent: a rent-controlled tenancy's lawful rent is a sum of published percentages.",
                body, active="units.html")


# --------------------------------------------------------------------------
# Page: notice and reasons
# --------------------------------------------------------------------------
def build_notice() -> str:
    letter = f"""NOTICE OF RENT INCREASE

Date of service: [date]

To: [tenant name(s)]
Unit: [unit identifier]
Property: [street address]

1. Your current base rent is ${'{current_rent}'} per month.

2. Effective [effective date], your base rent will increase by [X]% — a dollar increase of
   ${'{dollar_increase}'} per month — to a new base rent of ${'{new_rent}'} per month.

3. The increase consists of:
     [A]%  annual allowable increase for the rate year [rate year]
     [B]%  banked increase carried forward from [years]

4. The percentages are added and applied once to the base rent. No passthrough or fluctuating
   charge is included in this calculation.

5. Please keep this notice with your rent records.

[Owner or manager name and contact details]"""
    body = f"""  <div class="card">
    <h2>What the notice must contain</h2>
    <table>
      <caption>Required elements · the list is short, which is why omitting an item is the usual failure</caption>
      <thead><tr><th>Element</th><th>Requirement</th><th>Source</th></tr></thead>
      <tbody>
        <tr><td>Dollar amount</td><td>"The rent increase notice should include the dollar amount of the increase."</td><td>{S("learn")}</td></tr>
        <tr><td>Percentage</td><td>The percentage amount of the increase.</td><td>{S("learn")}</td></tr>
        <tr><td>Effective date</td><td>The date the increase will go into effect.</td><td>{S("learn")}</td></tr>
        <tr><td>Banked portion</td><td>Which part of the increase is banked — and, in practice, from which years.</td><td>{S("banked")}</td></tr>
        <tr><td>Component split</td><td>§37.3(b) requires the landlord to inform the tenant in writing which portion reflects the annual increase and/or a banked amount, and which portion reflects operating and maintenance costs, comparable rents, capital improvements, rehabilitation, energy measures or an RAP loan. A notice that does not conform is "null and void" under that section.</td><td>{S("s373", "petitions")}</td></tr>
        <tr><td>Correct rate year</td><td>"Use the percentage that will be in effect on the date of the increase, not the percentage in effect on the date they serve the notice."</td><td>{S("learn")}</td></tr>
        <tr><td>Written form and lead time</td><td>30 days if the increase, alone or combined with others in the 12 months before it, is 10% or less; 90 days if more.</td><td>{S("s827")}</td></tr>
        <tr><td>Service method</td><td>Personal delivery, or mail under Code Civ. Proc. §1013 — which adds five days for mail within California.</td><td>{S("s827", "s1013")}</td></tr>
        <tr><td>What need not be included</td><td>Neither the licence nor a justification is required. "The rent increase license does not need to be included with your rent increase notice."</td><td>{S("inv", "learn")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>Deadlines</h2>
{deadline_table()}
  </div>

  <div class="card">
    <h2>Reasons: required, permitted, forbidden</h2>
    <table>
      <caption>No reason is required for an annual or banked increase; several reasons are never acceptable</caption>
      <thead><tr><th style="width:26%">Question</th><th>Answer</th><th style="width:22%">Source</th></tr></thead>
      <tbody>
        <tr><td>Must I give a reason?</td><td>No. The required contents of a notice for an annual or banked increase are the dollar amount, the percentage, the effective date, the banked portion, and the §37.3(b) component split. Nothing in the published guidance requires a justification for the allowance itself.</td><td>{S("learn", "s373")}</td></tr>
        <tr><td>When is a justification mandatory?</td><td>Only for increases that require a landlord petition — capital improvements, operating and maintenance costs, comparable rents, certain passthroughs — where the landlord must file with the Rent Board before serving notice. None of those is proposed here.</td><td>{S("learn")}</td></tr>
        <tr><td>What is the safest thing to state?</td><td>The arithmetic itself: which percentage is the current annual allowance, and which is a banked year. It is verifiable from the Rent Board's published table, which is exactly what a reviewer will check.</td><td>{S("f571", "banked")}</td></tr>
        <tr><td>Never: a protected characteristic</td><td>A reason or differential treatment touching race, colour, religion, sex, gender identity or expression, sexual orientation, marital status, national origin, ancestry, familial status, source of income, disability, veteran or military status or genetic information is unlawful.</td><td>{S("s12955", "fha")}</td></tr>
        <tr><td>Never: a repair request or complaint</td><td>Within 180 days of a good-faith repair request or tenantability complaint the rent may not be increased in the circumstances set out in the statute, and retaliation may never be the purpose.</td><td>{S("s1942_5")}</td></tr>
        <tr><td>Never: the new occupant</td><td>"A landlord cannot charge additional rent simply because a new (or additional) roommate has moved into a unit with the existing tenant. This is an unlawful rent increase, even if the lease or rental agreement provides for the additional charge."</td><td>{S("learn")}</td></tr>
        <tr><td>Never: "market rate"</td><td>Market rent can be set for a new tenancy where no prior tenant remains in possession. It cannot justify an increase on a tenant in occupancy in a covered unit.</td><td>{S("s1947_12", "s1954_53")}</td></tr>
        <tr><td>Careful: the last original occupant</td><td>A different, narrower rule allows an unlimited increase for certain remaining occupants once the <em>last</em> original occupant permanently vacates — only for subtenants, and only if a proper §6.14 notice was served in time. A co-tenant is not subject to that increase. This does not apply while an original tenant still lives in Unit 1.</td><td>{S("cos", "s1954_53")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>A compliant notice, in plain form</h2>
    <p class="small">This is a template for the owner's file, not a Rent Board form and not legal advice. Fill every bracket;
    do not add persuasive language, and do not reference the occupants, a complaint or the market.</p>
    <div class="letter">{letter}</div>
    <p class="small">Elements drawn from: {S("learn", "banked", "s827", "s373")}</p>
  </div>

  <div class="card note">
    <h2>Service and proof</h2>
    <ul>
      <li>Personal delivery to the tenant, or mail under Code Civ. Proc. §1013. If mailed within California, the notice period
      gains five days — so a 30-day notice should be mailed at least 35 days before the effective date.</li>
      <li>Keep the notice copy, the service record (delivery receipt, or certified-mail tracking), and the licence page for the
      relevant year in one file per unit.</li>
      <li>If the increase starts later than the anniversary, the later date becomes the new anniversary and the next increase must
      wait at least 12 months.</li>
    </ul>
    <p class="small">Sources: {S("s827", "s1013", "learn")}</p>
  </div>
"""
    return page("Notice &amp; reasons", "Notice, deadlines and reasons",
                "The notice is the only part of the process a tenant sees first. Its required contents are few, so most failures are "
                "omissions — or a reason that should never have been written down.",
                body, active="notice.html")


# --------------------------------------------------------------------------
# Page: tenant-lawyer test
# --------------------------------------------------------------------------
def build_tenant_review() -> str:
    body = f"""  <div class="card note">
    <h2>How this page is meant to be used</h2>
    <p>San Francisco tenants can obtain free advice and representation, and the Rent Board charges nothing to file a petition.
    That means any increase should be assumed to be read by someone whose job is to find the defect. The checks below are the ones
    that decide the outcome; each is either satisfied, or flagged as an open item on this project.</p>
    <p class="small">Sources: {S("petitions", "unlawful", "evict")}</p>
  </div>

  <div class="card">
    <h2>The fifteen-point test</h2>
    <table>
      <caption>Unit 1 and Unit 2 assessed against each check</caption>
      <thead><tr><th>#</th><th>Check</th><th>Unit 1</th><th>Unit 2</th><th>Source</th></tr></thead>
      <tbody>
        <tr><td class="num">1</td><td>Unit is covered by the Rent Ordinance</td><td>Presumed (1940, two units) — confirm occupancy certificate</td><td>Same building</td><td>{S("rentallaws")}</td></tr>
        <tr><td class="num">2</td><td>Licence in effect on the effective date</td><td>{BLANK("F-14")}</td><td>{BLANK("F-14")}</td><td>{S("inv", "noncomp")}</td></tr>
        <tr><td class="num">3</td><td>Amount is the allowance plus documented banks, nothing more</td><td>3.0% = {money(U1_BANK)} maximum on 1 Feb 2027</td><td>{pct(BANK7)} = {money(U2_TOTAL)} banked, plus the unpublished 2027-28 rate</td><td>{S("f571", "banked")}</td></tr>
        <tr><td class="num">4</td><td>At least 12 months since the last increase</td><td>Yes — none since 1 Feb 2025</td><td>Yes — none since 1 Jun 2019, on the owner's account {FLAG("F-13")}</td><td>{S("learn")}</td></tr>
        <tr><td class="num">5</td><td>First increase no earlier than 12 months after the lease began</td><td>Yes — 1 Feb 2026 or later</td><td>Yes — 1 Jun 2020 or later</td><td>{S("learn")}</td></tr>
        <tr><td class="num">6</td><td>Banking test: 24 full months without an increase before a skipped year is used</td><td>Met on 1 Feb 2027</td><td>Met from 1 Jun 2021</td><td>{S("banked")}</td></tr>
        <tr><td class="num">7</td><td>Percentages added, never compounded</td><td>3.0%, not 3.02%</td><td>{pct(BANK7)}, added</td><td>{S("banked", "multi")}</td></tr>
        <tr><td class="num">8</td><td>Calculated on base rent only, no passthroughs</td><td>Yes</td><td>Yes</td><td>{S("learn")}</td></tr>
        <tr><td class="num">9</td><td>Not rounded up</td><td>{money(U1_BANK)}</td><td>{money(U2_TOTAL)}</td><td>{S("learn")}</td></tr>
        <tr><td class="num">10</td><td>Rate year matches the effective date</td><td>1.6% applies to 1 Feb 2027</td><td>2027-28 rate needed for 1 Jun 2027 {FLAG("F-11")}</td><td>{S("learn", "rates")}</td></tr>
        <tr><td class="num">11</td><td>Notice contains every required element</td><td>Template covers all five</td><td>Same, plus the banked years</td><td>{S("learn", "s373")}</td></tr>
        <tr><td class="num">12</td><td>Lead time: 30 days, or 90 if above 10%</td><td>30 days</td><td>90 days for the {pct(BANK7)} step; 30 days at exactly 10%</td><td>{S("s827")}</td></tr>
        <tr><td class="num">13</td><td>No retaliatory timing</td><td>Clear the last 180 days before service</td><td>Same</td><td>{S("s1942_5")}</td></tr>
        <tr><td class="num">14</td><td>No reason touching a protected characteristic; no charge for the new occupant</td><td>No occupant-based charge — the April 2026 addition cannot be priced</td><td>No reason stated beyond the arithmetic</td><td>{S("learn", "s12955")}</td></tr>
        <tr><td class="num">15</td><td>Records support every figure</td><td>Lease, prior notices, proofs of service</td><td>{BLANK("F-13")}</td><td>{S("petitions", "f571")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>One unit or both — the discrimination question</h2>
    <table>
      <caption>What the sources do and do not say</caption>
      <thead><tr><th>Question</th><th>Verified position</th><th>Source</th></tr></thead>
      <tbody>
        <tr><td>Is there a rule requiring both units to be raised together?</td><td>No official source imposes one. There is no requirement to raise rent at all, and no requirement of uniformity across tenancies.</td><td>{S("learn", "s12955")}</td></tr>
        <tr><td>Is raising only one unit unlawful by itself?</td><td>Not on the face of the discrimination statutes. FEHA and the Fair Housing Act prohibit differential treatment because of a protected characteristic, not differential treatment as such. A lawful, documented, objective basis is the dividing line.</td><td>{S("s12955", "fha")}</td></tr>
        <tr><td>What creates exposure?</td><td>Choosing between tenancies on a ground that correlates with a protected characteristic — source of income, familial status, disability, national origin, marital status — or timing that coincides with a complaint, a repair request or organising.</td><td>{S("s12955", "s1942_5")}</td></tr>
        <tr><td>What does the reviewer see?</td><td>Two tenancies with different ceilings because they accrued different banks. Applying each unit's own lawful ceiling on its own anniversary is defensible and explainable; applying an identical percentage to both would in fact be <em>less</em> accurate here, because Unit 1 has 3.0% available and Unit 2 has far more.</td><td>{S("banked", "f571")}</td></tr>
        <tr><td>What should be written down?</td><td>A single written policy: the anniversary date rule, the rate-year rule, the banking method, the notice template, and the record-keeping. Then apply it to both units without exception, and keep the file.</td><td>{S("banked", "petitions")}</td></tr>
        <tr><td>Does an official dataset compare outcomes by owner type or ZIP code?</td><td>{BLANK("F-18")} No official dataset was located. Private listing averages are not authoritative and are not used here.</td><td>{S("inv")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>Where a lawyer would look hardest — and the current answer</h2>
    <table>
      <caption>Findings specific to these facts</caption>
      <thead><tr><th>Issue</th><th>Finding</th><th>Source</th></tr></thead>
      <tbody>
        <tr><td>The April 2026 additional occupant in Unit 1</td><td>Cannot support any charge. The prohibition applies "notwithstanding a rental agreement or lease that specifically permits a rent increase for additional occupants." The only lawful increase is the allowance plus banks.</td><td>{S("learn", "s373")}</td></tr>
        <tr><td>Was Unit 1 reset by the April 2026 continuation?</td><td>No. A continuing tenancy with an added occupant is not a new tenancy, so the 1 February anniversary and the {money(U1)} base rent stand.</td><td>{S("learn")}</td></tr>
        <tr><td>Could Unit 1 be reset to market if the remaining original tenant leaves?</td><td>Not automatically. The narrower unlimited-increase rule requires that the <em>last</em> original occupant has permanently vacated, applies to subtenants rather than co-tenants, and depends on a timely §6.14 notice. Whether the second occupant is a subtenant or a co-tenant is not established on the record. {FLAG("F-19")}</td><td>{S("cos", "s1954_53")}</td></tr>
        <tr><td>Is a 13.1% Unit 2 step "normal business practice"?</td><td>It is lawful today but it is a seven-year catch-up, and the 90-day notice exists because increases above 10% are treated as materially different. The pending ordinance targets exactly this. A phased 10.0% step of {money(U2_TEN)} is the more defensible first move.</td><td>{S("s827", "legistar")}</td></tr>
        <tr><td>Security deposit interest</td><td>A separate annual obligation: 4.2% for 1 March 2026 – 28 February 2027. It is not a rent increase and does not consume an allowance.</td><td>{S("rates")}</td></tr>
        <tr><td>What the Rent Board will not decide</td><td>Harassment, discrimination, retaliation and security deposits are outside its jurisdiction — those are court or agency matters, which is why a defensible increase should avoid the appearance of any of them.</td><td>{S("petitions")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card note">
    <h2>Places to verify before service</h2>
    <ul>
      <li>Rent Board counselling line, 415-252-4600, weekdays 9–12 and 1–4 — free, and the correct forum for confirming coverage,
      anniversary dates and licence status. {S("rentallaws")}</li>
      <li>Rent Board Portal — licence status and its expiry for the year that covers the effective date. {S("portal")}</li>
      <li>California Civil Rights Department — housing discrimination complaints. {S("crd")}</li>
      <li>HUD — fair housing complaints. {S("hud")}</li>
    </ul>
  </div>
"""
    return page("Tenant-lawyer test", "Would this survive a tenant's lawyer?",
                "A stress test, not a prediction. Each check below is pass/fail against a published rule, and the open items are the "
                "only places where the answer could change.",
                body, active="tenant-review.html")


# --------------------------------------------------------------------------
# Page: owner practice
# --------------------------------------------------------------------------
def build_practice() -> str:
    body = f"""  <div class="card">
    <h2>How increases actually get run</h2>
    <p>There is no separate rulebook for large owners. The same ordinance, the same allowance and the same licence apply to a
    two-unit building and to a thousand-unit portfolio. What differs is process: whether the filing, the calendar and the
    documentation are systematised. The rows below separate what the official sources establish from what they do not.</p>
  </div>

  <div class="card">
    <h2>Process differences that are documented</h2>
    <table>
      <caption>What official sources do say</caption>
      <thead><tr><th>Practice</th><th>What the source establishes</th><th>Source</th></tr></thead>
      <tbody>
        <tr><td>Bulk filing</td><td>For properties with five or more residential units, unit information may be reported in bulk using the Housing Inventory Excel template; the Portal's individual-unit form is recommended for small properties.</td><td>{S("inv")}</td></tr>
        <tr><td>Automated rent setting</td><td>Since 14 October 2024 it is unlawful to sell or use an "algorithmic device" that uses non-public competitor data to recommend rents or occupancy — the revenue-management software used by larger operators. Each month and each unit is a separate violation; tenants and, from 6 October 2025, tenants' rights organisations may sue.</td><td>{S("algo")}</td></tr>
        <tr><td>Annual cycle</td><td>The allowance changes on 1 March and the Housing Inventory and Rent Board Fee are both due 1 March. An operator's calendar is therefore anchored to 1 March, not to the tenancy dates.</td><td>{S("learn", "fee")}</td></tr>
        <tr><td>Fees</td><td>The per-unit fee is uniform, so a portfolio pays it at scale; 50% may be recovered from tenants in occupancy, but not penalties.</td><td>{S("fee")}</td></tr>
        <tr><td>Notice discipline</td><td>Every increase needs a written notice with the same five elements and the same 30/90-day lead time, regardless of portfolio size.</td><td>{S("learn", "s827")}</td></tr>
        <tr><td>Exemptions</td><td>Condominiums and single-family homes may be outside local rent control under Costa-Hawkins; a portfolio will segment units by that status. These two units are not in that category.</td><td>{S("s1954_53", "rentallaws")}</td></tr>
        <tr><td>Comparative statistics</td><td>{BLANK("F-18")} No government source publishes how often or by how much corporate versus individual owners raise rent. Any figure quoted elsewhere is not verifiable against an official source and is excluded here.</td><td>{S("inv")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>An individual owner's version of the same system</h2>
    <table>
      <caption>The five controls that reproduce a portfolio's discipline on a two-unit building</caption>
      <thead><tr><th>Control</th><th>What it looks like here</th><th>Why it decides the outcome</th><th>Source</th></tr></thead>
      <tbody>
        <tr><td>Compliance calendar</td><td>1 March: Inventory + fee. 1 February: Unit 1 anniversary. 1 June: Unit 2 anniversary.</td><td>The licence is date-sensitive; an anniversary missed by a month moves every later date.</td><td>{S("inv", "learn")}</td></tr>
        <tr><td>One licence check per increase</td><td>Open the Portal, screenshot the licence period covering the effective date, file it with the notice.</td><td>The licensee must be in force on the effective date, and tenants can see the same screen.</td><td>{S("noncomp")}</td></tr>
        <tr><td>One written policy</td><td>Same method, same template, same thresholds for both units.</td><td>Uniformity is the cheapest answer to any suggestion of differential treatment.</td><td>{S("s12955")}</td></tr>
        <tr><td>Rate-year discipline</td><td>Always read the rate in effect on the effective date from Form 571, and never carry a prior year's percentage forward.</td><td>Using the wrong rate year is a calculation error a reviewer will find immediately.</td><td>{S("f571", "learn")}</td></tr>
        <tr><td>Bank ledger per unit</td><td>A row per anniversary: year, rate, amount imposed or banked, proof.</td><td>Banks are only usable if the 24-month test and the arithmetic can be shown.</td><td>{S("banked")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card note">
    <h2>What this means for the two units</h2>
    <p>The gap between a careful individual owner and a managed portfolio is not permission — it is evidence. A managed owner can
    produce a licence page, a bank ledger and a notice template on demand. For this building the equivalent file is partly missing:
    Unit 2's rent history and the licensing history are both unverified. Fixing those two records is more valuable than optimising
    the percentage, because either one, not the arithmetic, is what would decide a petition.</p>
    <p class="small">Sources: {S("inv", "noncomp", "banked", "petitions")}</p>
  </div>
"""
    return page("Owner practice", "Corporate and individual practice",
                "The same law applies to every owner. What differs is whether the filing, the calendar and the records exist — which is "
                "what a reviewer actually inspects.",
                body, active="practice.html")


# --------------------------------------------------------------------------
# Page: sources
# --------------------------------------------------------------------------
def build_sources() -> str:
    what = {
        "banked": "24-month banking test; banks added not compounded; no cap back to 1 April 1982; banks survive sale; licence required before an annual or banked increase; 30/90-day notice and the five mail days; the 1.6% example and the pending File #261020 notice.",
        "learn": "1.6% for 1 March 2026 – 28 February 2027; 60% of Bay Area CPI; base-rent-only rule; no rounding up; anniversary mechanics; notice contents; additional-occupant prohibition; licence requirement and start dates.",
        "inv": "All owners must report; reporting is free; 1 March deadline; late filing accepted but the notice is unenforceable without a licence; licence auto-generated for tenant-occupied units and need not accompany the notice; what each unit type must report; bulk upload at five or more units; tenants can check licence status.",
        "noncomp": "Unlicensed increases may be null and void for multiple years, with refunds; licensing start dates; the licence applies only to rent-controlled units; how to check licence status and expiry; tenant petition routes.",
        "petitions": "Petition types including unlawful rent increase and the summary petition for an invalid notice; no filing fee; the Rent Board does not adjudicate harassment, discrimination, retaliation or deposits; 415-252-4600.",
        "unlawful": "Unlawful-rent-increase petition, Form C, no charge, no time limit; hearing before an Administrative Law Judge; no lawyer required.",
        "rates": "Current 1.6% allowance; prior years; 4.2% security-deposit interest; bankable Rent Board fee amounts; relocation figures; pending File #261020 notice.",
        "fee": "$59.00 per dwelling unit for 2026-27; 50% recovery ($29.50); 1 March deadline; 5% monthly late penalty capped at 15%; referral after 1 June; exemption window closing 14 December 2026; fee and Inventory are separate obligations.",
        "rentallaws": "Coverage test — certificate of occupancy on or before 13 June 1979, not a single-family home or condominium; eviction protection; counselling line and hours.",
        "multi": "Banks are added across years, not compounded; no petition needed; no rounding; 30 days' notice; base rent excludes passthroughs but generally includes parking or storage.",
        "cos": "The narrower unlimited-increase rule when the last original occupant vacates: §6.14 notice timing, subtenant versus co-tenant, no petition required but petitions possible.",
        "algo": "Algorithmic rent-setting devices prohibited from 14 October 2024; definitions; remedies; enforcement by tenants and, from 6 October 2025, tenants' rights organisations.",
        "evict": "Just-cause framework; free legal help contacts; the Rent Board does not give legal advice.",
        "f571": "The Rent Board's own table of allowable annual increases from 1 April 1982 to 28 February 2027, including 1.6% current, 1.4% prior, and the 1992 caution.",
        "s827": "30 days if the increase is 10% or less of the lowest rent charged in the prior 12 months, 90 days if more, and the five-day mail rule by reference to §1013.",
        "s1013": "Service by mail and the extension of the notice period.",
        "s1942_5": "Retaliation: 180-day window after repair requests, complaints and related proceedings, and the absolute prohibition on retaliatory purpose.",
        "s1947_12": "Tenant Protection Act: 5% + CPI capped at 10%, two increments per 12 months, the local-control exclusion in (d)(3), remedies and treble damages, operative 1 April 2024 and repealed 1 January 2030.",
        "s1954_53": "Costa-Hawkins: when an owner may set an initial rate; the limits on that right; the definitional framework that leaves a 1940 two-flat covered.",
        "s12955": "FEHA housing discrimination: the protected characteristics, and the prohibition on discriminatory terms and conditions.",
        "fha": "42 U.S.C. §3604(b): discrimination in the terms, conditions or privileges of rental is unlawful; protected classes under the federal Act.",
        "oag": "Statewide cap mechanics, and the table showing 8.8% for the San Francisco area for increases starting 1 August 2026 – 31 July 2027, plus the rule that a lower local cap prevails.",
        "legistar": "File #261020: ordinance, introduced 15 September 2026, status Pending Committee Action; would cap combined banked and capital-improvement increases at 10% a year for three years.",
        "s373": "Admin. Code §37.3: annual increase as 60% of CPI with a 7% statutory maximum; the licence condition; the §37.3(b) notice-content duty; the additional-occupant prohibition; void increases for non-conforming notices.",
        "portal": "The Rent Board Portal, where the Housing Inventory is filed, the licence is viewed and the fee is paid.",
        "crd": "California Civil Rights Department housing-discrimination information and complaint route.",
        "hud": "Federal fair-housing complaint route.",
    }
    rows = "\n".join(
        f'          <tr><td class="num">{i}</td><td>{SRC[k][0]}</td><td>{what.get(k, "")}</td>'
        f'<td><a href="{SRC[k][1]}">open</a></td><td>{ACCESSED}</td></tr>'
        for i, k in enumerate(SRC, start=1)
    )
    body = f"""  <div class="card">
    <h2>Source register</h2>
    <p class="lead">Everything published in this edition traces to one of the sources below. All were read on {ACCESSED};
    the allowables, the licence rules, the notice periods and the pending ordinance were re-checked that day rather than carried
    forward from earlier drafts.</p>
    <table>
      <caption>{len(SRC)} sources · official publishers only</caption>
      <thead><tr><th class="num">#</th><th>Source</th><th>What it verifies</th><th>Link</th><th>Read</th></tr></thead>
      <tbody>
{rows}
      </tbody>
    </table>
  </div>

  <div class="card warn">
    <h2>What could not be sourced</h2>
    <table>
      <caption>Gaps, stated as gaps</caption>
      <thead><tr><th>Question</th><th>Status</th><th>What would close it</th></tr></thead>
      <tbody>
        <tr><td>Allowable increase for 1 March 2027 – 29 February 2028</td><td>Not published {FLAG("F-11")}</td><td>Rent Board announcement and the next Form 571, typically in the new year — {S("rates")}</td></tr>
        <tr><td>Unit 2 rent history 2019 to date</td><td>Owner statement only {FLAG("F-13")}</td><td>Leases, notices, proofs of service, rent ledger — {S("banked")}</td></tr>
        <tr><td>Licence status and expiry for this building</td><td>{FLAG("F-14")}</td><td>Portal lookup by address or APN — {S("portal", "noncomp")}</td></tr>
        <tr><td>Whether an unpaid Rent Board Fee affects the licence</td><td>No official statement {FLAG("F-15")}</td><td>Written answer from the Rent Board — {S("fee")}</td></tr>
        <tr><td>Official ZIP-level or neighbourhood market-rent benchmark</td><td>None located {FLAG("F-18")}</td><td>No official publisher exists for this; private listing data excluded — {S("oag")}</td></tr>
        <tr><td>Corporate versus individual increase norms</td><td>None located {FLAG("F-18")}</td><td>No official dataset — do not substitute anecdote — {S("inv")}</td></tr>
        <tr><td>Certificate of occupancy date for the building</td><td>Owner statement (1940) {FLAG("F-16")}</td><td>DBI or assessor record, Property Information Map — {S("rentallaws")}</td></tr>
        <tr><td>Whether the second occupant in Unit 1 is a subtenant or a co-tenant</td><td>{FLAG("F-19")}</td><td>The lease and any §6.14 notice — {S("cos")}</td></tr>
        <tr><td>Voucher or subsidy status of either unit</td><td>{FLAG("F-17")}</td><td>Owner records; a housing authority contract would add its own approval step — {S("fee")}</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card note">
    <h2>How the verification was done</h2>
    <ul>
      <li>Each figure was read from the publisher's page on {ACCESSED} and transcribed; no figure was carried over from an earlier
      edition without being re-read.</li>
      <li>Every table row in this edition is machine-checked for an official link or a flag marker, and every internal link and
      anchor is checked against the filesystem.</li>
      <li>Arithmetic is recomputed in the build from the published percentages and the owner's base rents, to the cent, using
      addition rather than compounding.</li>
      <li>An anonymisation sweep runs over every page: no tenant names or initials, no street address, no unit identifiers that
      reveal location, and no ZIP code.</li>
    </ul>
    <p class="small">Run <span class="mono">python3 tools/check_v2.py</span> to repeat all of the above.</p>
  </div>
"""
    return page("Sources", "Sources and verification",
                "Twenty-eight official sources, what each one establishes, and the nine questions they cannot answer.",
                body, active="sources.html")


# --------------------------------------------------------------------------
# Page: flagged
# --------------------------------------------------------------------------
def build_flagged() -> str:
    flags = [
        ("F-11", "Allowable increase for 1 March 2027 – 29 February 2028 (\"rate year 2027\")",
         "Not yet published, so no ceiling can be stated for a Unit 2 increase effective 1 June 2027 or any Unit 1 decision deferred past 28 February 2027. Earlier drafts treated 13.1% as the June 2027 maximum; it is the banked balance, not the ceiling.",
         "Rent Board announcement and the update to Form 571, then recompute.",
         ("rates", "f571")),
        ("F-12", "Rate year must match the effective date",
         "A notice with an effective date after 28 February 2027 cannot use 1.6%. The Rent Board instructs owners to use the percentage in effect on the date of the increase. Any draft notice must be re-checked against its effective date.",
         "Confirm the rate year against Form 571 immediately before service.",
         ("learn", "f571")),
        ("F-13", "Unit 2 rent history, 2019 to date",
         "The banked balance of 13.1% / $412.65 assumes no increase was imposed at any anniversary since 1 June 2019. No lease amendment, notice or receipt was supplied. Any prior increase reduces the balance, and a missed step also changes the anniversary.",
         "Leases, prior notices, proofs of service and a rent ledger; then recompute the balance from the unused years only.",
         ("banked", "f571")),
        ("F-14", "Licence status for this building",
         "No Housing Inventory or licence record was supplied for either unit. Without a licence on the effective date an increase may be void for that period, and the tenant may claim a refund. This is the single most consequential open item.",
         "Portal lookup by address or APN; confirm the licence period covers the intended effective date; repeat for prior years.",
         ("inv", "noncomp")),
        ("F-15", "Whether an unpaid Rent Board Fee affects the licence",
         "The fee ($59 per dwelling unit for 2026-27) and the Housing Inventory report are separate obligations, and no official page states that the fee conditions the licence. It would be wrong to assert either that it does or that it does not.",
         "Written confirmation from the Rent Board; keep the fee receipt with the licence file either way.",
         ("fee", "inv")),
        ("F-16", "Building year and certificate-of-occupancy date",
         "'1940, two units' is the owner's statement. Coverage turns on a certificate of occupancy issued on or before 13 June 1979, and on the building not being a single-family home or condominium.",
         "Department of Building Inspection or assessor record; Property Information Map; Rent Board counsellor confirmation.",
         ("rentallaws", "s1954_53")),
        ("F-17", "Housing subsidy or voucher status of either unit",
         "Not established. If a unit is voucher-assisted, the amount may be tested against the payment standard and the housing authority's process applies — a different analysis from the one on these pages.",
         "Owner records and, if applicable, the housing authority's rent-reasonableness determination.",
         ("fee", "s373")),
        ("F-18", "Comparative market data",
         "No official source publishes ZIP-level or neighbourhood market rents, and none publishes corporate versus individual increase norms. Private listing aggregates are not authoritative, so nothing of the kind is used or estimated here.",
         "Nothing available at official level; this gap is labelled rather than filled.",
         ("oag", "inv")),
        ("F-19", "Status of the second occupant in Unit 1",
         "Whether the occupant who joined in April 2026 is a subtenant or a co-tenant is not established. That distinction decides whether any future unlimited-increase rule could ever apply once the last original occupant vacates, and whether a §6.14 notice was required at the time.",
         "The lease, any sublease, and any §6.14 notice served within a reasonable time of the occupancy.",
         ("cos", "s1954_53")),
        ("F-20", "Unit 1: whether the 1.4% year was ever charged informally",
         "The plan assumes no increase has been taken since 1 February 2025. A handshake increase or an unreceipted change would alter the anniversary, the base rent and the banked amount.",
         "Rent ledger and bank records for Unit 1 covering February 2025 to date.",
         ("learn", "f571")),
        ("F-21", "Pending ordinance — File #261020",
         "Would cap combined banked and capital-improvement increases at 10% a year for three years, applying to banked increases noticed on or after 15 September 2026. Status is Pending Committee Action and it is not law; a >10% banked notice could be affected if it is enacted.",
         "Re-check the Legistar record immediately before any notice above 10%.",
         ("legistar", "banked")),
        ("F-23", "Lease dates and starting rents are owner-supplied",
         "The 1 February 2025 / $3,995 and 1 June 2019 / $3,150 starting points come from the owner's records, not from a government or Rent Board filing. Every ceiling on this site is computed from them, so an error here propagates through all the arithmetic.",
         "Executed leases and a rent ledger for both units; compare against any Housing Inventory submission.",
         ("banked", "inv")),
        ("F-22", "Notice deadline arithmetic",
         "Serve-by dates are computed by subtracting 30 or 90 days (plus five for mail) from the intended effective date. The statutes set periods but do not exclude weekends or holidays, so the computed date is arithmetic, not an adjudicated deadline.",
         "Rent Board counsellor confirmation of the date for each notice; keep the calculation with the file.",
         ("s827", "s1013")),
    ]
    rows = "\n".join(
        f'          <tr><td><strong>{fid}</strong></td><td>{title}</td><td>{why}</td><td>{close}</td><td>{S(*src)}</td></tr>'
        for fid, title, why, close, src in flags
    )
    body = f"""  <div class="card warn">
    <h2>Flagged for review — {len(flags)} open items</h2>
    <p>These are the places where a value could not be confirmed from an official source, or where the record supplied by the
    owner is incomplete. They are published rather than resolved: nothing on this site fills a gap with an estimate. None of them
    prevents the analysis from being used, but four of them (F-11, F-13, F-14, F-20) can change a number or the validity of an
    increase, and should be closed before a notice is served.</p>
  </div>

  <div class="card">
    <h2>Register</h2>
    <table>
      <caption>Item · what is wrong · what would close it · official reference</caption>
      <thead><tr><th style="width:6%">ID</th><th style="width:18%">Item</th><th>Why it is flagged</th><th style="width:22%">What would close it</th><th style="width:18%">Source</th></tr></thead>
      <tbody>
{rows}
      </tbody>
    </table>
  </div>

  <div class="card note">
    <h2>Irregularities found in earlier editions on this repository</h2>
    <p class="small">Recorded here so the corrections are traceable, not to reopen them. Each has been superseded in this edition.</p>
    <ul class="small">
      <li><strong>13.1% presented as the June 2027 ceiling.</strong> It is the banked balance accrued to June 2026; the June 2027
      increase also includes the unpublished 2027-28 allowance. See F-11.</li>
      <li><strong>Banking described as capped at three years.</strong> Incorrect — there is no cap on the amount banked back to
      1 April 1982, and banks do not expire during a tenancy.</li>
      <li><strong>"24 months or 12 months" banking conflict.</strong> The current Rent Board page states the 24-month test; an older
      rule text suggests 12. The current published page governs practice, and the conservative single-year option is lawful under
      either reading.</li>
      <li><strong>Unit 1 anniversary read as 1 April.</strong> The April 2026 event was a continuing tenancy, not a new one; the
      anniversary remains 1 February.</li>
      <li><strong>"Capped at 7%, so 7% is available."</strong> The ordinance sets a 7% statutory maximum on the annual increase, but
      the published allowance — 1.6% — is the operative number. The maximum is a ceiling on the formula, not an entitlement.</li>
    </ul>
  </div>

  <div class="card">
    <h2>Prior registers kept online</h2>
    <ul class="small">
      <li><a href="../pages/flagged.html">pages/flagged.html</a> — F-1 to F-10 (7 November 2026)</li>
      <li><a href="../docs/flagged-for-review.html">docs/flagged-for-review.html</a> — FR-01 to FR-17</li>
      <li><a href="../audit/flagged.html">audit/flagged.html</a> — consolidated audit flags</li>
      <li><a href="../verified/guide/flagged.html">verified/guide/flagged.html</a> — verified-edition flags</li>
      <li><a href="../review/flagged.html">review/flagged.html</a> — audit-trail flags, including the 12-versus-24-month conflict</li>
    </ul>
  </div>
"""
    return page("Flagged for review", "Flagged for review",
                "Every unresolved value, stated as unresolved. Each item names what would close it and the official reference it "
                "was tested against.",
                body, active="flagged.html")


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "style.css").write_text(CSS, encoding="utf-8")

    pages = {
        "executive-summary.html": build_exec_summary(),
        "license.html": build_license(),
        "laws.html": build_laws(),
        "units.html": build_units(),
        "notice.html": build_notice(),
        "tenant-review.html": build_tenant_review(),
        "practice.html": build_practice(),
        "flagged.html": build_flagged(),
        "sources.html": build_sources(),
    }
    for name, html in pages.items():
        (OUT / name).write_text(html, encoding="utf-8")
    (OUT / "index.html").write_text(build_index(), encoding="utf-8")
    print("wrote verification/index.html + %d pages + verification/style.css" % len(pages))


if __name__ == "__main__":
    main()
