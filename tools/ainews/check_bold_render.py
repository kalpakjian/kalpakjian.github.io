# -*- coding: utf-8 -*-
"""Check whether `**...**` actually rendered as <strong> in the built site.

Motivation: every regex heuristic I wrote for "CJK bold does not flank" produced
false positives on posts that render perfectly (the published weight-space post
has `**「並行」…**` and `**（SE 1.5）` in its tables, both fine). Guessing at
CommonMark flanking rules from the source text is the wrong tool.

The right tool is the built HTML: if the text between the asterisks is wrapped
in <strong>, it rendered. If the literal "**" survives in the rendered
paragraph text, it did not. This script does that check in a real browser, so
the gate agrees with the reader instead of with my regex.

Usage:
    pwsh ... hexo server -p 4126
    python tools/ainews/check_bold_render.py --url http://127.0.0.1:4126/<post>/
    python tools/ainews/check_bold_render.py --html public/<path>/index.html

Exit 0 = no literal asterisks in body text, 1 = found some, 2 = cannot run.
"""
import argparse
import re
import sys


def check_html(html):
    """Strip tags, then look for surviving literal `**` in body prose."""
    body = html
    m = re.search(r"<article[^>]*>(.*?)</article>", html, re.S) or \
        re.search(r'<div class="post-content[^"]*"[^>]*>(.*?)</div>\s*</div>', html, re.S)
    if m:
        body = m.group(1)
    # remove script/style/code blocks: asterisks there are intentional
    body = re.sub(r"<(script|style|code|pre)\b.*?</\1>", " ", body, flags=re.S)
    text = re.sub(r"<[^>]+>", "", body)
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    hits = re.findall(r".{0,12}\*\*.{0,12}", text)
    strongs = len(re.findall(r"<strong\b", body))
    return hits, strongs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--url")
    g.add_argument("--html")
    args = ap.parse_args(argv)

    if args.html:
        with open(args.html, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
    else:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("SKIP: playwright not installed", file=sys.stderr)
            return 2
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto(args.url, wait_until="networkidle", timeout=45000)
            html = pg.content()
            b.close()

    hits, strongs = check_html(html)
    print("rendered <strong> tags: %d" % strongs)
    print("literal '**' left in text: %d" % len(hits))
    for h in hits[:10]:
        print("   ...%s..." % h.replace("\n", " "))
    return 0 if not hits else 1


if __name__ == "__main__":
    sys.exit(main())
