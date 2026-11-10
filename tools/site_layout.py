"""Shared layout, source registry and helpers for the canonical root site.

Every external source used by the site is registered here exactly once, so the
verification script can check that (a) each row of a data table cites a source
from this registry and (b) every registry entry is an official domain.
"""

# ---------------------------------------------------------------- source registry
OFFICIAL_DOMAINS = (
    "sf.gov",
    "sfgov.org",
    "portal.sfrb.org",
    "sfgov.legistar.com",
    "leginfo.legislature.ca.gov",
    "codelibrary.amlegal.com",
    "oag.ca.gov",
    "calcivilrights.ca.gov",
    "govinfo.gov",
    "justice.gov",
    "hud.gov",
    "ecfr.gov",
)

SRC = {
    # --- San Francisco Rent Board / City and County of San Francisco
    "SF_LI": ("sf.gov — Learn about rent increases in San Francisco",
              "https://www.sf.gov/learn-about-rent-increases-san-francisco"),
    "SF_BANK": ("sf.gov — Banked rent increases",
                "https://www.sf.gov/information--banked-rent-increases"),
    "SF_HI": ("sf.gov — The Rent Board Housing Inventory",
              "https://www.sf.gov/rent-board-housing-inventory"),
    "SF_NONCOMP": ("sf.gov — Notice of Owner Noncompliance with Housing Inventory",
                   "https://www.sf.gov/notice-of-owner-noncompliance-with-housing-inventory"),
    "SF_LAWS": ("sf.gov — Learn about San Francisco rental laws",
                "https://www.sf.gov/learn-about-san-francisco-rental-laws"),
    "SF_571": ("sf.gov — Form 571, allowable annual increases 3/1/26–2/28/27 (PDF)",
               "https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf"),
    "SF_MULTI": ("sf.gov — Annual rent increase for multiple years",
                 "https://www.sf.gov/information/annual-rent-increase-multiple-years"),
    "SF_TENPET": ("sf.gov — Tenant petitions",
                  "https://www.sf.gov/tenant-petitions"),
    "SF_UNLAWFUL": ("sf.gov — Report an unlawful rent increase / review your rent history",
                    "https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history"),
    "SF_LANDPET": ("sf.gov — Landlord petitions and passthroughs",
                   "https://www.sf.gov/landlord-petitions-and-passthroughs"),
    "SF_SPECIAL": ("sf.gov — Special circumstances petitions based on rents for comparable units",
                   "https://www.sf.gov/information/topic-no-323-special-circumstances-petitions-based-rents-comparable-units"),
    "SF_ALGO": ("sf.gov — New law prohibits algorithmic devices used to set rents in San Francisco",
                "https://www.sf.gov/news--new-law-prohibits-algorithmic-devices-used-set-rents-san-francisco"),
    "SF_COUNSEL": ("sf.gov — Rent Board counselling line 415-252-4600",
                   "https://www.sf.gov/learn-about-san-francisco-rental-laws"),
    "SF_FEE": ("sf.gov — The Rent Board Fee",
               "https://www.sf.gov/rent-board-fee"),
    "SF_614": ("sf.gov — Rent increases under Section 6.14 and Costa-Hawkins",
               "https://www.sf.gov/information--rent-increases-under-section-614-and-costa-hawkins"),
    "SF_PORTAL": ("Rent Board Portal (Housing Inventory / licence look-up)",
                  "https://portal.sfrb.org/"),
    "ADMIN_373": ("SF Administrative Code § 37.3 — Rent Limitations (American Legal)",
                  "https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_admin/0-0-0-70881"),
    "LEGISTAR_261020": ("sfgov.legistar.com — File #261020, cap on rent increases for rent-controlled units",
                        "https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770"),
    # --- California
    "LEG_827": ("Cal. Civ. Code § 827 — notice to change terms of tenancy",
                "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827"),
    "LEG_1947": ("Cal. Civ. Code § 1947.12 — Tenant Protection Act rent cap",
                 "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12"),
    "LEG_1954": ("Cal. Civ. Code § 1954.53 — Costa-Hawkins Rental Housing Act",
                 "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954.53"),
    "LEG_1942": ("Cal. Civ. Code § 1942.5 — retaliation prohibited",
                 "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5"),
    "LEG_1013": ("Cal. Code Civ. Proc. § 1013 — service by mail extension",
                 "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=1013"),
    "LEG_12955": ("Cal. Gov. Code § 12955 — FEHA housing discrimination",
                  "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=12955"),
    "OAG": ("California Attorney General — Limits on rent increases",
            "https://oag.ca.gov/rentcaps"),
    "CRD": ("California Civil Rights Department — Housing discrimination",
            "https://calcivilrights.ca.gov/housing/"),
    # --- Federal
    "USC_3604": ("42 U.S.C. § 3604 — Fair Housing Act (govinfo, U.S. Code 2023)",
                 "https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap45-subchapI-sec3604.htm"),
    "DOJ_ALGO": ("U.S. DOJ — suit against six large landlords over algorithmic pricing (7 Jan 2025)",
                 "https://www.justice.gov/archives/opa/pr/justice-department-sues-six-large-landlords-algorithmic-pricing-scheme-harms-millions"),
}

OFFICIAL_URLS = {v[1] for v in SRC.values()}

# Two sources live outside the registry because they are the same page under a
# different City URL; register the canonical form used in citations.
EXTRA_OFFICIAL = {
    "https://sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history",
    "https://www.sf.gov/information--banked-rent-increases",
}
OFFICIAL_URLS |= EXTRA_OFFICIAL


def src(key, label=None):
    """Return an inline source link for registry entry `key`."""
    title, url = SRC[key]
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label or title)


def srcs(*keys):
    return " · ".join(src(k) for k in keys)


def cell(*keys):
    """A source table-cell (keeps checker simple: exactly one link per source column)."""
    return '<td class="srccell">%s</td>' % " · ".join(src(k) for k in keys)


# ---------------------------------------------------------------- page chrome
CSS = """:root{--bg:#f5f7fa;--card:#fff;--ink:#15202b;--muted:#5a6b7d;--accent:#155e9c;
--accent2:#0b4f86;--border:#e2e8f0;--warnbg:#fff7e8;--warnbd:#e8b45a;--ok:#0f6b3f;
--dangerbg:#fdf1ee;--dangerbd:#c8503c;--radius:12px}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);line-height:1.6;
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
-webkit-font-smoothing:antialiased}
header{background:#132433;color:#fff;padding:14px 22px}
header .headrow{max-width:1180px;margin:0 auto;display:flex;flex-wrap:wrap;
align-items:center;gap:14px}
header .brand{font-size:1rem;font-weight:650;letter-spacing:.2px}
header .brand span{font-weight:400;color:#a9c2d8;font-size:.8rem;display:block}
header nav{display:flex;flex-wrap:wrap;gap:4px;margin-left:auto}
header nav a{color:#cfe0ef;text-decoration:none;font-size:.82rem;padding:6px 9px;
border-radius:7px;white-space:nowrap}
header nav a:hover{background:#22415c;color:#fff}
header nav a.active{background:var(--accent);color:#fff}
main{max-width:1180px;margin:0 auto;padding:22px 18px 40px}
h1{font-size:1.5rem;margin:0 0 6px}
h2{font-size:1.15rem;margin:0 0 10px}
h3{font-size:.98rem;margin:18px 0 6px}
p{margin:.5em 0}
.lede{color:var(--muted);font-size:.95rem;margin:0 0 18px}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);
padding:20px 22px;margin-bottom:16px;box-shadow:0 1px 2px rgba(16,24,40,.04)}
.card.tight{padding:14px 16px}
.hero{border-left:5px solid var(--accent)}
.alert{border-left:5px solid var(--dangerbd);background:var(--dangerbg)}
.warn{border-left:5px solid var(--warnbd);background:var(--warnbg)}
.ok{border-left:5px solid var(--ok);background:#eef8f2}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.stat{background:#fbfdff;border:1px solid var(--border);border-radius:10px;padding:13px 14px}
.stat .num{font-size:1.32rem;font-weight:700;color:var(--accent2);line-height:1.2}
.stat .lbl{font-size:.78rem;color:var(--muted);margin-top:3px}
table{width:100%;border-collapse:collapse;font-size:.86rem;margin:8px 0 4px;
display:block;overflow-x:auto}
th,td{border:1px solid var(--border);padding:8px 10px;text-align:left;vertical-align:top}
th{background:#eef4fa;font-weight:650;font-size:.8rem;text-transform:uppercase;
letter-spacing:.03em;color:#33475b}
tr:nth-child(even) td{background:#fbfcfe}
td.srccell{font-size:.78rem;min-width:190px}
td.srccell a{display:inline-block;margin-bottom:2px}
a{color:var(--accent)}
a:hover{color:var(--accent2)}
.small{font-size:.79rem;color:var(--muted)}
.tiny{font-size:.72rem;color:var(--muted)}
.badge{display:inline-block;background:#e8f1fa;color:var(--accent2);border-radius:20px;
padding:1px 9px;font-size:.72rem;font-weight:650;white-space:nowrap}
.badge.warn{background:#fdf0d9;color:#8a5500}
.badge.danger{background:#fbe3de;color:#9b2c1a}
.badge.ok{background:#ddf1e6;color:#0f6b3f}
.steps{list-style:none;padding:0;margin:8px 0;counter-reset:s}
.steps>li{position:relative;padding:10px 0 10px 44px;border-bottom:1px solid var(--border);
counter-increment:s}
.steps>li:last-child{border-bottom:0}
.steps>li::before{content:counter(s);position:absolute;left:0;top:9px;width:28px;height:28px;
border-radius:50%;background:var(--accent);color:#fff;text-align:center;line-height:28px;
font-size:.82rem;font-weight:700}
.steps li b{display:block;margin-bottom:2px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:8px 22px;
margin:6px 0 2px;font-size:.87rem}
.facts div{border-bottom:1px dotted var(--border);padding:4px 0}
.facts span{color:var(--muted)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(255px,1fr));gap:12px}
.cards a.tile{display:block;text-decoration:none;color:inherit;background:#fbfdff;
border:1px solid var(--border);border-radius:10px;padding:14px 16px}
.cards a.tile:hover{border-color:var(--accent);box-shadow:0 2px 6px rgba(21,94,156,.12)}
.cards .tile b{display:block;color:var(--accent2);margin-bottom:3px;font-size:.92rem}
.cards .tile span{font-size:.79rem;color:var(--muted)}
footer{max-width:1180px;margin:0 auto;padding:0 18px 34px;color:var(--muted);font-size:.78rem}
footer .allpages{background:#fff;border:1px solid var(--border);border-radius:var(--radius);
padding:14px 16px;margin-bottom:14px}
footer .allpages a{margin-right:12px;display:inline-block;font-size:.79rem}
.quote{background:#f7fafc;border-left:3px solid #b9c9da;padding:8px 12px;margin:8px 0;
font-size:.85rem;color:#33475b}
ul.tight{margin:.35em 0 .35em 1.1em;padding:0}
ul.tight li{margin:.2em 0}
.nowrap{white-space:nowrap}
"""

NAV = [
    ("index.html", "Dashboard"),
    ("pages/executive-summary.html", "Summary"),
    ("pages/process.html", "Licence &amp; process"),
    ("pages/units.html", "Units &amp; maths"),
    ("pages/laws.html", "Rules &amp; caps"),
    ("pages/practice.html", "Market practice"),
    ("pages/notice.html", "Notice &amp; reasons"),
    ("pages/review.html", "Tenant-lawyer test"),
    ("pages/flagged.html", "Flagged"),
]

ALL_PAGES = [
    ("index.html", "Dashboard"),
    ("pages/executive-summary.html", "Executive summary"),
    ("pages/process.html", "Licence &amp; process (step by step)"),
    ("pages/units.html", "Units &amp; maths"),
    ("pages/laws.html", "Rules &amp; caps (local, state, federal)"),
    ("pages/reasonable.html", "Reasonable &amp; normal increases"),
    ("pages/practice.html", "Corporate vs individual practice"),
    ("pages/notice.html", "Notice, service &amp; reasons"),
    ("pages/review.html", "Tenant-lawyer stress test"),
    ("pages/discrimination.html", "One unit or both units?"),
    ("pages/requirements.html", "Requirements checklist"),
    ("pages/sources.html", "Sources &amp; verification register"),
    ("pages/flagged.html", "Flagged for review"),
]


def page(filename, title, body, desc="", active=None):
    """Render a full page. `filename` is repo-relative (index.html or pages/x.html)."""
    depth = 0 if "/" not in filename else 1
    up = "../" if depth else ""
    if active is None:
        active = filename
    nav = "".join(
        '<a href="%s%s"%s>%s</a>' % (up, href, ' class="active"' if href == active else "", label)
        for href, label in NAV
    )
    allp = "".join('<a href="%s%s">%s</a>' % (up, href, label) for href, label in ALL_PAGES)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Rental Increase SF</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<header>
  <div class="headrow">
    <div class="brand">Rental Increase SF<span>Verified research dashboard · San Francisco rent-controlled units</span></div>
    <nav>{nav}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="allpages"><b>All pages:</b><br>{allp}</div>
  <p><b>Independent verification edition:</b> a second pass that re-fetched every official source and re-ran the arithmetic, published separately so this page set was not rewritten — <a href="{up}verification/index.html">open the verification edition (10 November 2026)</a>. Earlier editions are preserved for audit in <code>docs/</code>, <code>dashboard/</code>, <code>review/</code>, <code>audit/</code> and <code>verified/</code>.</p>
  <p><b>Privacy:</b> all tenant and owner identifying details are replaced with placeholder labels (Tenant A–F). Dates and dollar amounts are unchanged. The specific ZIP code, neighbourhood and street address are withheld, because unit-level facts plus a location would identify the tenants; the rules cited apply citywide and do not vary by ZIP. Source registers are internal only.</p>
  <p><b>Not legal advice.</b> Every figure here is either quoted from an official source (linked in the row) or calculated from an official percentage and an owner-reported base rent; where a value could not be confirmed it is left blank and listed on the <a href="{up}pages/flagged.html">Flagged for review</a> page. Confirm anything you intend to rely on with the SF Rent Board counselling line (415-252-4600) and a California lawyer.</p>
  <p>Research pass and source retrieval: <b>10 November 2026</b>. Content verified line by line against the linked official pages on that date.</p>
</footer>
</body>
</html>
"""
