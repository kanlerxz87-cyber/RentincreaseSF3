# Rental Increase SF

A static, anonymized, source-linked San Francisco rent-increase research dashboard. Entry point: `index.html`; category pages live in `pages/` and use `assets/style.css`. No build dependencies or client-side requests. The GitHub Pages source is `main` at `/`.

The dashboard distinguishes owner-reported facts from official verification, and illustrative arithmetic from an actual legal entitlement. It does not give legal advice or claim review by a lawyer. Recheck all live rules, licensing, facts, notice requirements, and legislation before acting. **Do not upload private lease records or identifying details to this public repository.**

Prior independent editions at `docs/`, `review/`, and `dashboard/` have been superseded by the unified dashboard because they contained inconsistent or unverified claims. Their HTML URLs route to the relevant current category; older work remains in Git history. The older `tools/build_site.py` generates a superseded edition and must not be used to republish it without reconciliation. See `COORDINATION.md` for the integration and verification record.

Local preview: `python3 -m http.server 8000 --bind 0.0.0.0`. Automated checks: `python3 tools/verify_integrated.py`.
