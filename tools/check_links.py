#!/usr/bin/env python3
"""check_links.py - verify every link in the generated site.

Internal links (href/src pointing at files in this repository) must resolve to a
real file. External links must return HTTP 200 (or 200/301/302 followed to 200).

Usage:
    python3 tools/check_links.py             # internal + external (needs network)
    python3 tools/check_links.py --offline   # internal only
    python3 tools/check_links.py --json out.json

Exit status is non-zero if any link fails, so it can gate a deployment.
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
UA = ("Mozilla/5.0 (compatible; RentincreaseSF3-linkcheck/1.0; "
      "+https://github.com/kanlerxz87-cyber/RentincreaseSF3)")


def collect():
    targets = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [x for x in dirnames if x not in (".git", "__pycache__", "node_modules")]
        for fn in filenames:
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


def check_local(rel_from, href):
    parts = urlsplit(href)
    if parts.scheme in ("http", "https"):
        return "external", urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))
    if parts.netloc:
        return "external", href
    target = os.path.normpath(os.path.join(os.path.dirname(os.path.join(ROOT, rel_from)), href))
    if not os.path.exists(target):
        return "broken-local", href
    if os.path.isdir(target):
        return "broken-local", href + " (is a directory; GitHub Pages needs index.html)"
    return "ok-local", href


def fetch(url, attempts=3):
    """Return (status, final_url). Follows redirects, retries GET on 405/403/501
    and retries transient network errors."""
    for i in range(attempts):
        status, final = _fetch_once(url)
        if isinstance(status, int) or not str(status).startswith("ERR:URLError"):
            return status, final
        time.sleep(2 * (i + 1))
    return status, final


def _fetch_once(url):
    last = None
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={
                "User-Agent": UA, "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status, r.geturl()
        except urllib.error.HTTPError as exc:
            last = (exc.code, url)
            if exc.code in (403, 405, 501) and method == "HEAD":
                continue
            return exc.code, url
        except Exception as exc:  # noqa: BLE001 - network failure is a finding
            last = ("ERR:" + type(exc).__name__ + ": " + str(exc)[:120], url)
    return last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="check internal links only")
    ap.add_argument("--json", metavar="PATH", help="also write a machine-readable report")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    targets = collect()
    if not targets:
        print("No HTML files found - run tools/build_site.py first.")
        return 2

    internal, external = [], {}
    for rel_from, href in targets:
        kind, resolved = check_local(rel_from, href)
        if kind == "external":
            external.setdefault(resolved, []).append(rel_from)
        elif kind == "broken-local":
            internal.append((rel_from, href, resolved))

    print(f"Scanned {len(targets)} link references across the site.")
    print(f"  internal link references checked: {len(targets) - sum(len(v) for v in external.values())}")
    print(f"  distinct external URLs: {len(external)}")

    failures = []
    if internal:
        print(f"\nBROKEN INTERNAL LINKS ({len(internal)}):")
        for rel_from, href, msg in internal:
            print(f"  {rel_from} -> {href}   {msg}")
            failures.append(("internal", rel_from, href, msg))
    else:
        print("\nInternal links: all resolve.")

    results = {}
    if not args.offline and external:
        print(f"\nChecking {len(external)} external URLs (this needs network)...")
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futs = {pool.submit(fetch, u): u for u in external}
            for fut, url in futs.items():
                status, final = fut.result()
                results[url] = status
        bad = {u: s for u, s in results.items() if not (isinstance(s, int) and 200 <= s < 400)}
        for u in sorted(results):
            s = results[u]
            mark = "OK " if isinstance(s, int) and 200 <= s < 400 else "FAIL"
            if mark == "FAIL" or os.environ.get("VERBOSE"):
                print(f"  [{mark}] {s}  {u}")
                print(f"         referenced by: {', '.join(sorted(set(external[u])))}")
        if bad:
            print(f"\nFAILED EXTERNAL LINKS ({len(bad)}):")
            for u, s in sorted(bad.items()):
                failures.append(("external", ", ".join(sorted(set(external[u]))), u, str(s)))
        else:
            print(f"\nExternal links: all {len(external)} resolve.")
    elif args.offline:
        print("\n--offline: external link HTTP status not checked (run without --offline, or in CI).")

    if args.json:
        out = os.path.join(ROOT, args.json) if not os.path.isabs(args.json) else args.json
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w") as f:
            json.dump({"checked": len(targets), "distinct_external": len(external),
                       "external_status": {k: str(v) for k, v in results.items()},
                       "failures": failures}, f, indent=2)
        print("Wrote", os.path.relpath(out, ROOT))

    if failures:
        print(f"\nRESULT: FAIL - {len(failures)} broken link(s).")
        return 1
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
