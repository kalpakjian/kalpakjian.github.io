# -*- coding: utf-8 -*-
"""Derive the bold-breakage rule from RENDERED pairs, then verify a regex.

The lesson from writing digest_lint.check_bold three times: reasoning about
CommonMark flanking rules for CJK produced 100+ false positives on posts that
render perfectly. So instead of guessing, this script:

  1. renders a page in a browser
  2. collects every <strong>...</strong> (renders = fine)
  3. collects every surviving literal `**` with its following character
     (renders = broken) and prints the following character
  4. reports which follower characters actually break

The output is the evidence for the rule implemented in digest_lint.S020:
a closer followed by a CJK letter or a full-width mark cannot close.

Usage:
    python tools/ainews/_probe_bold.py public/<path>/index.html
    python tools/ainews/_probe_bold.py --url http://127.0.0.1:4125/<slug>/
"""
import argparse
import collections
import re
import sys


def analyse(html):
    body = html
    m = re.search(r"<article[^>]*>(.*?)</article>", html, re.S)
    if m:
        body = m.group(1)
    body = re.sub(r"<(script|style|code|pre)\b.*?</\1>", " ", body, flags=re.S)

    strongs = re.findall(r"<strong>(.*?)</strong>", body, re.S)
    text = re.sub(r"<[^>]+>", "", body)
    for a, b in (("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&"), ("&quot;", '"')):
        text = text.replace(a, b)

    followers = collections.Counter()
    samples = []
    for m in re.finditer(r"\*\*", text):
        nxt = text[m.end():m.end() + 1]
        followers[nxt] += 1
        if len(samples) < 12:
            samples.append(text[max(0, m.start() - 18):m.end() + 6].replace("\n", " "))
    return len(strongs), followers, samples


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--html")
    g.add_argument("--url")
    args = ap.parse_args()

    if args.html:
        with open(args.html, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
    else:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto(args.url, wait_until="networkidle", timeout=60000)
            html = pg.content()
            b.close()

    strongs, followers, samples = analyse(html)
    print("<strong> rendered : %d" % strongs)
    print("literal '**'     : %d" % sum(followers.values()))
    if followers:
        print("follower chars   :")
        for ch, n in followers.most_common():
            print("    %-6r x%d" % (ch, n))
        print("samples:")
        for s in samples:
            print("    ...%s..." % s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
