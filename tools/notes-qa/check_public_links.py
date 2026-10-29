# -*- coding: utf-8 -*-
"""Check that every internal link in the generated site resolves to a file.

qa_notes.ps1 only looks inside one page (href="#id"); it cannot see a link that
points at another page or at a permalink. That gap shipped two real 404s:
/2026/10/29/cnn-2-experiments/ was linked from the notes before the post existed,
and the first CI build of that post landed on /2026/10/28/... because the runner
formatted permalinks in UTC while _config.yml parsed dates in Asia/Taipei.

So this runs AFTER `hexo generate`, over public/:

    python tools/notes-qa/check_public_links.py            # <repo>/public
    python tools/notes-qa/check_public_links.py -Root out  # any build dir

It resolves every href/src (root-relative, relative, and absolute URLs on the
site host) to a path in the build, maps "/dir/" to "dir/index.html", and exits 1
if anything is missing. External hosts, mailto:, tel:, javascript:, data: and
pure "#fragment" values are skipped.

Pure stdlib, ASCII source, no hardcoded paths: the default root is found by
walking up from this file until a directory with public/ (or source/) shows up,
the same way qa_notes.ps1 finds source/.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit

SITE_HOST = "kalpakjian.github.io"
BASE = "https://" + SITE_HOST + "/"
ATTR = re.compile(r"""(?:href|src)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)
SKIP_PREFIX = ("mailto:", "tel:", "javascript:", "data:", "sms:", "#")


def find_root(explicit: str | None) -> str:
    if explicit:
        return os.path.abspath(explicit)
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        for name in ("public", "source"):
            cand = os.path.join(d, name)
            if os.path.isdir(cand):
                return cand
        parent = os.path.dirname(d)
        if parent == d:
            raise SystemExit("cannot find a public/ (or source/) directory above "
                             + os.path.dirname(os.path.abspath(__file__))
                             + " - pass -Root explicitly")
        d = parent


def resolve(root: str, page_rel: str, value: str) -> str | None:
    """Return the filesystem path a link should hit, or None when not ours."""
    value = value.strip()
    if not value or value.lower().startswith(SKIP_PREFIX):
        return None
    page_url = BASE + page_rel.replace(os.sep, "/")
    parts = urlsplit(urljoin(page_url, value))
    if parts.scheme not in ("http", "https") or parts.netloc != SITE_HOST:
        return None                      # external site, leave it alone
    path = unquote(parts.path)
    if not path:
        return None                      # "?q=1" style, same page
    rel = path.lstrip("/")
    target = os.path.normpath(os.path.join(root, rel.replace("/", os.sep)))
    if not (target + os.sep).startswith(root + os.sep):
        return None                      # escapes the build dir; not our business
    if path.endswith("/") or not os.path.splitext(rel)[1]:
        if os.path.isdir(target):
            target = os.path.join(target, "index.html")
    return target


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-Root", "--root", default=None,
                    help="build directory to scan (default: <repo>/public)")
    ap.add_argument("--quiet", action="store_true", help="summary only")
    ap.add_argument("--limit", type=int, default=40,
                    help="stop listing after N broken links (default 40)")
    args = ap.parse_args()

    root = find_root(args.root)
    pages = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for fn in sorted(filenames):
            if fn.endswith(".html"):
                pages.append(os.path.join(dirpath, fn))
    if not pages:
        print("no .html files under {0} - refusing to report a pass".format(root))
        return 1

    broken = []
    checked = 0
    for page in pages:
        page_rel = os.path.relpath(page, root)
        with open(page, encoding="utf-8", errors="replace") as fh:
            html = fh.read()
        seen = set()
        for m in ATTR.finditer(html):
            value = m.group(1) if m.group(1) is not None else m.group(2)
            # hexo writes href="{url}" placeholders into some theme templates
            if value in seen:
                continue
            seen.add(value)
            target = resolve(root, page_rel, value)
            if target is None:
                continue
            checked += 1
            if not os.path.exists(target):
                broken.append((page_rel.replace(os.sep, "/"), value))

    if not args.quiet:
        for page, value in broken[:args.limit]:
            print("BROKEN  {0}  ->  {1}".format(page, value))
        if len(broken) > args.limit:
            print("... {0} more".format(len(broken) - args.limit))

    print("pages scanned = {0}   internal links = {1}   broken = {2}".format(
        len(pages), checked, len(broken)))
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
