# -*- coding: utf-8 -*-
"""Render generated figures to PNG for visual QA.

SVG only counts as correct when it LOOKS correct -- the earlier posts shipped a
chart whose bars silently vanished because a blank line inside <svg> made marked
emit <p>. Unit tests cannot catch that; a screenshot can.

    python tools/ainews/_preview_figures.py tools/ainews/out/<id>/figures.html
"""
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "qa")


def main():
    if len(sys.argv) < 2:
        print("usage: _preview_figures.py <figures.html>", file=sys.stderr)
        return 2
    src = os.path.abspath(sys.argv[1])
    if not os.path.exists(src):
        print("missing: %s" % src, file=sys.stderr)
        return 2
    os.makedirs(OUT, exist_ok=True)

    with open(src, "r", encoding="utf-8") as f:
        html = f.read()
    page_html = ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
                 "<style>body{background:#0b1016;margin:0;padding:24px;"
                 "font-family:'Segoe UI','Microsoft JhengHei',sans-serif}"
                 "figure{max-width:960px}</style></head><body>" + html + "</body></html>")
    tmp = os.path.join(OUT, "_preview.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(page_html)

    written = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1040, "height": 900})
        pg.goto("file:///" + tmp.replace("\\", "/"), wait_until="load")
        figs = pg.query_selector_all("figure")
        print("figures found: %d" % len(figs))
        for i, fig in enumerate(figs, 1):
            path = os.path.join(OUT, "fig%d.png" % i)
            fig.screenshot(path=path)
            written.append(path)
            # a figure whose <svg> has zero <rect> is broken by definition
            rects = fig.evaluate("el => el.querySelectorAll('rect').length")
            texts = fig.evaluate("el => el.querySelectorAll('text').length")
            print("  fig%d: rects=%d texts=%d" % (i, rects, texts))
        b.close()
    for w in written:
        print("wrote:", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
