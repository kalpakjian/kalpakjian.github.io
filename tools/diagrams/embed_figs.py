# -*- coding: utf-8 -*-
"""Generic "replace an ASCII code block with an inline SVG figure" tool.

For notes that have NO build script (opencv-notes, streamlit-flask-notes, ...)
the md and the html are maintained in parallel, so both must be edited and kept
in sync (the QA gate checks heading parity between the two).

art_index counts "real" diagrams only: fenced blocks whose box-drawing chars are
just decorative separators inside a copy-pasteable code block are skipped, using
the same judgement as inventory.py (so `python inventory.py <note>` and this
tool's art#N always refer to the same block).

Usage:
    python embed_figs.py <note-dir> <plan.json>

plan.json:
[
  {"marker": "distinctive text inside the ASCII block",
   "svg":    "C:/.../figure.svg",
   "caption": "圖 1：..."}
]
"""
import html as htmllib
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

REPO = r"C:\Users\princ\blog"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inventory import is_code_block  # noqa: E402  (same directory)


def responsive(svg):
    """Keep viewBox, drop fixed pixel size, add a responsive style if missing."""
    m = re.match(r"<svg\b[^>]*>", svg)
    tag = re.sub(r'\s(width|height)="[^"]*"', "", m.group(0))
    if "style=" not in tag:
        tag = tag.replace(">", ' style="width:100%;height:auto;display:block">', 1)
    return tag + svg[m.end():]


def figure(svg, caption, marker):
    return ('<!-- %s -->\n<figure style="margin:20px 0;padding:14px 12px;'
            'background:#0d1117;border:1px solid #222b36;border-radius:12px;'
            'text-align:center;-webkit-print-color-adjust:exact;'
            'print-color-adjust:exact">\n' % marker + svg + "\n"
            '<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;'
            'line-height:1.65;text-align:left">' + caption + '</figcaption>\n'
            '</figure>\n<!-- /%s -->' % marker)


BOX = "┌─┐│└┘├┤┬┴┼╔╗╚╝║═"


def _has_art(body):
    return sum(1 for ch in body if ch in BOX) >= 8


def _md_spans(text):
    lines = text.split("\n")
    spans, i = [], 0
    while i < len(lines):
        if lines[i].lstrip().startswith("```"):
            a, b = i, i + 1
            while b < len(lines) and not lines[b].lstrip().startswith("```"):
                b += 1
            spans.append((a, b))
            i = b + 1
        else:
            i += 1
    return lines, spans


def replace_md(text, n, fig):
    """Replace the n-th fenced block that is a real diagram (not decorative art)."""
    lines, spans = _md_spans(text)
    k = 0
    for a, b in spans:
        body = "\n".join(lines[a + 1:b])
        if _has_art(body) and not is_code_block(body):
            k += 1
            if k == n:
                return "\n".join(lines[:a] + [fig] + lines[b + 1:])
    raise SystemExit("md: no art block #%d found" % n)


def _html_spans(text):
    spans = [(m.start(), m.end()) for m in
             re.finditer(r'<div class="codehilite">.*?</div>', text, re.S)]
    spans += [(m.start(), m.end()) for m in
              re.finditer(r"<pre>.*?</pre>", text, re.S)]
    spans = sorted(set(spans))
    merged = []
    for s, e in spans:                      # drop <pre> spans inside codehilite
        if merged and s < merged[-1][1]:
            continue
        merged.append((s, e))
    return merged


def _plain(seg):
    """Rendered code block -> plain text (pygments splits it into spans)."""
    return htmllib.unescape(re.sub(r"<[^>]+>", "", seg))


def replace_html(text, n, fig):
    """Replace the n-th rendered code block that is a real diagram."""
    k = 0
    for s, e in _html_spans(text):
        seg = text[s:e]
        if _has_art(seg) and not is_code_block(_plain(seg)):
            k += 1
            if k == n:
                return text[:s] + fig + text[e:]
    raise SystemExit("html: no art block #%d found" % n)


def main():
    note = sys.argv[1]
    plan = json.load(io.open(sys.argv[2], encoding="utf-8-sig"))
    d = os.path.join(REPO, "source", note)
    md_name = [f for f in os.listdir(d) if f.endswith("_Study_Notes.md")][0]
    md_p = os.path.join(d, md_name)
    html_p = os.path.join(d, "index.html")
    md = io.open(md_p, encoding="utf-8").read()
    html = io.open(html_p, encoding="utf-8").read()
    for i, item in enumerate(sorted(plan, key=lambda x: -x["art_index"]), 1):
        svg = responsive(io.open(item["svg"], encoding="utf-8").read().strip())
        fig = figure(svg, item["caption"], "FIG%d" % item["art_index"])
        md = replace_md(md, item["art_index"], fig)
        html = replace_html(html, item["art_index"], fig)
        print("  [%d/%d] art#%-2d %-30s %s bytes" % (i, len(plan), item["art_index"],
                                                    os.path.basename(item["svg"]),
                                                    format(len(svg.encode()), ",")))
    io.open(md_p, "w", encoding="utf-8", newline="\r\n").write(md)
    io.open(html_p, "w", encoding="utf-8", newline="\r\n").write(html)
    print("replaced %d figure(s) in %s (md + index.html)" % (len(plan), note))


if __name__ == "__main__":
    main()
