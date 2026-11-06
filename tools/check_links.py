#!/usr/bin/env python3
"""check_links.py - verify every link in the generated site.

Internal links (href/src pointing at files in this repository) must resolve to a
real file. External links are requested and classified:

    ok          HTTP 200-399 (redirects are followed)      -> pass
    not_found   HTTP 404 or 410                            -> FAIL (a dead link)
    blocked     HTTP 401/403/405/429 or 5xx after retries   -> warn (server refused
                the request; the URL is recorded, not treated as dead)
    error       DNS, TLS or timeout failure after retries   -> warn

A 403 is not evidence that a page is gone - several .gov hosts and the SEC block
non-browser clients. Those sources are separately marked "fetched" in the source
register because their content was retrieved and read directly during research,
which is stronger evidence than a status code. Only 404/410 and broken internal
links fail the build.

Usage:
    python3 tools/check_links.py                  # internal + external
    python3 tools/check_links.py --offline        # internal only
    python3 tools/check_links.py --json PATH      # also write a machine-readable report
    python3 tools/check_links.py --strict         # treat blocked/error as failures too

Exit status is non-zero on failure so it can gate a deployment.
When GITHUB_ACTIONS is set, findings are emitted as workflow annotations.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlsplit, urlunsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HREF = re.compile(r"""(?:href|src)\s*=\s*["']([^"'#]+?)["']""", re.I)

BROWSER_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
# SEC asks for a declared contact in the User-Agent; see sec.gov/os/accessing-edgar-data
SEC_UA = "RentincreaseSF3 research contact@example.com"

NOT_FOUND = (404, 410)
BLOCKED = (401, 403, 405, 407, 429, 500, 501, 502, 503, 504, 505)


def annotate(level, message, title=""):
    if os.environ.get("GITHUB_ACTIONS") == "true":
        msg = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        ttl = title.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::{level} title={ttl}::{msg}" if ttl else f"::{level}::{msg}")


def collect():
    targets = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [x for x in dirnames if x not in (".git", "__pycache__", "node_modules")]
        for fn in sorted(filenames):
            if not fn.lower().endswith((".html", ".htm")):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT)
            with open(full, encoding="utf-8") as f:
                text = f.read()
            for raw in HREF.findall(text):
                raw = raw.strip()
                if not raw or raw.startswith(("mailto:", "tel:", "javascript:", "data:")):
                    continue
                targets.append((rel, raw))
    return targets


def classify_href(rel_from, href):
    parts = urlsplit(href)
    if parts.scheme in ("http", "https"):
        return "external", urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))
    if parts.netloc:
        return "external", href
    target = os.path.normpath(os.path.join(os.path.dirname(os.path.join(ROOT, rel_from)), href))
    if not os.path.exists(target):
        return "broken", href
    if os.path.isdir(target):
        return "broken", href + " (directory - GitHub Pages needs an index.html)"
    return "ok", href


def _ua_for(url):
    return SEC_UA if "sec.gov" in url else BROWSER_UA


def _fetch_once(url, method):
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": _ua_for(url),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.geturl()


def fetch(url, attempts=3):
    """Return (status, classification). status is an int or 'ERR:<reason>'."""
    result = None
    for i in range(attempts):
        for method in ("GET", "HEAD"):
            try:
                status, _final = _fetch_once(url, method)
                return status, "ok" if 200 <= status < 400 else "other"
            except urllib.error.HTTPError as exc:
                result = (exc.code, "not_found" if exc.code in NOT_FOUND else
                          ("blocked" if exc.code in BLOCKED else "other"))
                if exc.code in (403, 405, 429, 501) and method == "GET":
                    continue          # retry with HEAD
                if exc.code in (429, 500, 502, 503, 504):
                    break             # transient - back off and retry the whole thing
                return result
            except Exception as exc:  # noqa: BLE001
                result = ("ERR:" + type(exc).__name__ + ": " + str(exc)[:140], "error")
                break
        if result and result[1] in ("not_found", "blocked", "other"):
            return result
        time.sleep(2 * (i + 1))
    return result or ("ERR:unknown", "error")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="check internal links only")
    ap.add_argument("--strict", action="store_true", help="also fail on blocked/error responses")
    ap.add_argument("--json", metavar="PATH", help="write a machine-readable report")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    targets = collect()
    if not targets:
        print("No HTML files found - run tools/build_site.py first.")
        return 2

    internal_bad, external = [], {}
    for rel_from, href in targets:
        kind, resolved = classify_href(rel_from, href)
        if kind == "external":
            external.setdefault(resolved, set()).add(rel_from)
        elif kind == "broken":
            internal_bad.append((rel_from, href, resolved))

    n_ext = sum(len(v) for v in external.values())
    print(f"Scanned {len(targets)} link references.")
    print(f"  internal references: {len(targets) - n_ext}")
    print(f"  distinct external URLs: {len(external)}")

    hard_fail = []
    if internal_bad:
        print(f"\nBROKEN INTERNAL LINKS ({len(internal_bad)}):")
        for rel_from, href, msg in internal_bad:
            print(f"  {rel_from} -> {href}   {msg}")
            annotate("error", f"{rel_from} -> {href}", "Broken internal link")
            hard_fail.append(("internal", rel_from, href, msg))
    else:
        print("\nInternal links: all resolve.")

    results = {}
    if not args.offline and external:
        print(f"\nRequesting {len(external)} external URLs...")
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futs = {pool.submit(fetch, u): u for u in external}
            for fut in futs:
                u = futs[fut]
                try:
                    results[u] = fut.result()
                except Exception as exc:  # noqa: BLE001
                    results[u] = ("ERR:" + type(exc).__name__, "error")
        counts = {}
        for u, (status, cls) in sorted(results.items()):
            counts[cls] = counts.get(cls, 0) + 1
            ok = cls == "ok"
            if not ok:
                print(f"  [{cls.upper():9}] {status}  {u}")
                print(f"               referenced by: {', '.join(sorted(external[u]))}")
                if cls == "not_found":
                    annotate("error", f"HTTP {status} {u} (referenced by "
                             f"{', '.join(sorted(external[u]))})", "Dead external link")
                    hard_fail.append(("external-404", ", ".join(sorted(external[u])), u, str(status)))
                else:
                    annotate("warning", f"{status} {u} - server refused the automated request; "
                             f"the source content was verified by direct retrieval during research "
                             f"where the register marks it 'fetched'.", "External link not machine-checkable")
                    if args.strict:
                        hard_fail.append(("external-" + cls, ", ".join(sorted(external[u])), u, str(status)))
        print("\nExternal summary: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    elif args.offline:
        print("\n--offline: external HTTP status not checked (run without --offline, or in CI).")

    if args.json:
        out = args.json if os.path.isabs(args.json) else os.path.join(ROOT, args.json)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w") as f:
            json.dump({
                "link_references_scanned": len(targets),
                "distinct_external_urls": len(external),
                "internal_broken": len(internal_bad),
                "external_results": {u: {"status": str(s), "classification": c}
                                     for u, (s, c) in sorted(results.items())},
                "referenced_by": {u: sorted(v) for u, v in sorted(external.items())},
                "failures": hard_fail,
            }, f, indent=2)
        print("Wrote", os.path.relpath(out, ROOT))

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as f:
            f.write("## Link check\n\n")
            f.write(f"- link references scanned: **{len(targets)}**\n")
            f.write(f"- distinct external URLs: **{len(external)}**\n")
            f.write(f"- broken internal links: **{len(internal_bad)}**\n")
            if results:
                counts = {}
                for _u, (_s, c) in results.items():
                    counts[c] = counts.get(c, 0) + 1
                f.write("- external: " + ", ".join(f"**{k}** {v}" for k, v in sorted(counts.items())) + "\n")
                bad = [(u, s, c) for u, (s, c) in sorted(results.items()) if c != "ok"]
                if bad:
                    f.write("\n| URL | status | class |\n|---|---|---|\n")
                    for u, s, c in bad:
                        f.write(f"| {u} | {s} | {c} |\n")
            f.write(f"\n**Result: {'FAIL' if hard_fail else 'PASS'}**\n")

    if hard_fail:
        print(f"\nRESULT: FAIL - {len(hard_fail)} dead link(s).")
        return 1
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
