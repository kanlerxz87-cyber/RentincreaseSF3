# Rental Increase Review — SF Outer Sunset (94122)

A sourced review of what a lawful rent increase is for two rent-controlled units in a 1940
two-unit building in San Francisco's Outer Sunset: local, state and federal law; how the increase
is computed and served; how institutional owners and individual owners actually handle it; the
test a tenant-side lawyer would run; and whether raising one unit rather than both creates
discrimination exposure.

**Published site:** https://kanlerxz87-cyber.github.io/RentincreaseSF3/

## What is here

| Path | What it is |
| --- | --- |
| `data/sources.json` | Source register. 54 official documents, each with publisher, URL, tier and the date it was read. |
| `data/findings.json` | The findings registry. 86 rows. Every statement on the site is a row here, and every row names a source key. |
| `build.py` | Generates the site from the two registries. Refuses to build if a row points at an unknown source, a non-HTTPS URL, or a host that is not an official government domain or an SEC filing. |
| `verify.py` | Line-by-line checks on the built output: link resolution, HTML balance, arithmetic recomputation, count consistency, and a personal-information scan. |
| `index.html`, `local.html`, `state.html`, `federal.html`, `practice.html`, `review.html`, `units.html`, `flagged.html`, `sources.html` | Generated pages. Do not edit by hand — they are overwritten. |
| `COORDINATION.md` | Multi-session protocol, task board and log. |

## Build

```sh
python3 build.py     # writes the HTML from data/
python3 verify.py    # checks the result; exits non-zero on any failure
```

No dependencies beyond the Python 3 standard library. No JavaScript framework, no CDN, no
external fonts — the site is a handful of static files served by GitHub Pages.

## The two gates

`build.py` and `verify.py` are the reason the site can be trusted without reading all 86 rows:

- **Provenance.** A row cannot exist without a source. The source must be HTTPS and on an official
  host (`.gov`, `sfgov.org`, `leginfo.legislature.ca.gov`, `law.cornell.edu` for the U.S. Code and
  CFR, or `sec.gov`). A link to a blog, a brokerage calculator or an AI-written explainer fails the
  build, which is how those sources stayed out.
- **Arithmetic.** `verify.py` recomputes both units from the base rents and the Rent Board's
  published percentages using `Decimal` and `ROUND_HALF_UP`, then asserts that the figures printed
  in the tables match, and that the seven yearly allowances on Unit 2 add to 13.1% only when they
  are *added* and not compounded.

Anything unconfirmed is a row with `"status": "unverified"`, is left blank in the tables, and is
republished on `flagged.html`. Nothing was estimated to fill a gap.

## Facts, privacy and what is deliberately absent

Tenants are referred to as P1–P6. Dates and dollar amounts are exactly as supplied. No names,
addresses or unit numbers appear anywhere in the generated output — `verify.py` fails the build if
any of the supplied identifier strings do either.

Two things are deliberately not on the site, because no official source supports them: a
comparison against a "market rent" for a comparable 94122 unit (the Rent Board does not publish one,
HUD fair-market rents answer a different question, and the FY2026 figure did not render), and any
assertion about whether a federal rent cap exists (an absence cannot be proven by citation, so it is
a flagged row rather than a claim).

This is a documented review of published rules, not legal advice.
