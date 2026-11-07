# -*- coding: utf-8 -*-
"""Check figure text does not overflow its box, using the browser's own metrics.

Why: several rounds of "look at the screenshot" were wasted on guesses. The
browser already knows every text width (getBBox), so compare them against the
figure edges and the bar column instead of eyeballing.

    python tools/ainews/_check_fig_layout.py tools/ainews/out/<id>/figures.html
"""
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "qa")

JS = """() => {
  const res = [];
  document.querySelectorAll('figure svg').forEach((svg, i) => {
    const vb = svg.getAttribute('viewBox').split(' ').map(Number);
    const W = vb[2], H = vb[3];
    const bad = [];
    // 1) any text leaving the canvas
    svg.querySelectorAll('text').forEach(t => {
      const b = t.getBBox();
      if (b.x < -1 || b.y < -1 || b.x + b.width > W + 1 || b.y + b.height > H + 1) {
        bad.push({kind: 'canvas', text: t.textContent.slice(0, 26),
                  x1: Math.round(b.x), x2: Math.round(b.x + b.width)});
      }
    });
    // 2) any text crossing a card/panel right edge (cards are the filled rects
    //    taller than 40 and wider than 80 -- the KPI/bar panels)
    const cards = [];
    svg.querySelectorAll('rect').forEach(r => {
      const w = +r.getAttribute('width'), h = +r.getAttribute('height');
      const x = +r.getAttribute('x'), y = +r.getAttribute('y');
      if (w > 80 && h > 40) cards.push({x, y, w, h});
    });
    svg.querySelectorAll('text').forEach(t => {
      const b = t.getBBox();
      for (const c of cards) {
        const insideY = b.y + b.height > c.y && b.y < c.y + c.h;
        const insideX = b.x >= c.x - 2 && b.x < c.x + c.w;
        if (insideY && insideX && b.x + b.width > c.x + c.w - 6) {
          bad.push({kind: 'card', text: t.textContent.slice(0, 26),
                    x2: Math.round(b.x + b.width), edge: Math.round(c.x + c.w)});
        }
      }
    });
    // de-duplicate by text+kind
    const seen = new Set(), uniq = [];
    for (const x of bad) {
      const k = x.kind + x.text;
      if (!seen.has(k)) { seen.add(k); uniq.push(x); }
    }
    res.push({idx: i + 1, W: W, H: H, overflow: uniq});
  });
  return res;
}"""


def main():
    if len(sys.argv) < 2:
        print("usage: _check_fig_layout.py <figures.html>", file=sys.stderr)
        return 2
    src = os.path.abspath(sys.argv[1])
    with open(src, "r", encoding="utf-8") as f:
        html = f.read()
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(OUT, "_layout.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html><html><head><meta charset='utf-8'><style>"
                "body{background:#0d1117;margin:0;padding:10px}</style></head><body>"
                + html + "</body></html>")

    fails = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1040, "height": 1000})
        pg.goto("file:///" + tmp.replace("\\", "/"), wait_until="load")
        for row in pg.evaluate(JS):
            if row["overflow"]:
                fails += 1
                print("fig%d (%dx%d): %d text(s) overflow"
                      % (row["idx"], row["W"], row["H"], len(row["overflow"])))
                for o in row["overflow"][:4]:
                    if o.get("kind") == "card":
                        print("    [card] %-24r right=%s edge=%s"
                              % (o["text"], o["x2"], o["edge"]))
                    else:
                        print("    [canvas] %-24r x1=%s x2=%s"
                              % (o["text"], o["x1"], o["x2"]))
            else:
                print("fig%d (%dx%d): ok" % (row["idx"], row["W"], row["H"]))
        b.close()
    print("\n%s" % ("LAYOUT OK" if not fails else "%d figure(s) overflow" % fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
