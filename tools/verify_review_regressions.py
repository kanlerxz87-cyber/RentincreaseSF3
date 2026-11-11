"""Guard against specific unsupported assertions found in the 2026-11-11 review.

This is a regression check, not a substitute for legal or source review.
"""
from pathlib import Path

pages = {name: Path(name).read_text(encoding='utf-8') for name in (
    'index.html', 'pages/executive-summary.html', 'pages/process.html',
    'pages/units.html', 'pages/flagged.html', 'pages/review.html', 'pages/laws.html')}
assert 'total number of units in the building is unverified' in pages['index.html']
assert '11.5% banked' in pages['index.html'] and 'annual component is distinct' in pages['index.html']
assert 'No one can guarantee a tenant lawyer' in pages['pages/executive-summary.html']
assert 'do not require an approval petition' in pages['pages/laws.html'] or 'different petition and worksheet rules' in pages['pages/laws.html']
assert all(flag in pages['pages/flagged.html'] for flag in ('FR-18', 'FR-19', 'FR-20'))
for name, text in pages.items():
    assert 'This is a 2-unit building' not in text, name
    assert 'Do not increase rent within 180 days' not in text, name
    assert 'If the percentage, base rent, licence, notice period, service and motive are all documented, yes' not in text, name
print('Current-review regression checks passed (not legal advice).')
