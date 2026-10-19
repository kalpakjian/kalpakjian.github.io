# -*- coding: utf-8 -*-
"""Replace the 43-line ASCII pipeline diagram in source/opencv-notes/ with the
hand-drawn SVG figure.

opencv-notes has no build script (its git history is direct edits), so the md
and the html are maintained in parallel -> replace in BOTH, keeping them in sync
(the QA gate verifies heading parity between the two).

  md   : the fenced code block containing the diagram
  html : the <div class="codehilite"><pre>...</pre></div> wrapping it
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

REPO = r"C:\Users\princ\blog"
DIR = os.path.join(REPO, "source", "opencv-notes")
MD = os.path.join(DIR, "OpenCV_Study_Notes.md")
HTML = os.path.join(DIR, "index.html")
SVG = os.path.join(REPO, "_work", "diagrams", "opencv-pipeline.svg")
MARKER = "讀取 cv2.imread"
START = "<!-- OPENCV-FIGURE:pipeline -->"
END = "<!-- /OPENCV-FIGURE -->"

svg = io.open(SVG, encoding="utf-8").read().strip()
m = re.match(r"<svg\b[^>]*>", svg)
tag = re.sub(r'\s(width|height)="[^"]*"', "", m.group(0))
if "style=" not in tag:
    tag = tag.replace(">", ' style="width:100%;height:auto;display:block">', 1)
svg = tag + svg[m.end():]

html_src = io.open(HTML, encoding="utf-8").read()
n_existing = html_src.count("<figure")
num = n_existing + 1
caption = (
    "圖 %d：OpenCV 的 12 步影像處理流程。步驟 4–6 是三條平行路線，其餘是主線；"
    "顏色代表四個階段（輸入／前處理 → 平行處理 → 影像分析 → 特徵與匹配）。" % num
)
fig = (START + "\n"
       '<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;'
       'border:1px solid #222b36;border-radius:12px;text-align:center;'
       '-webkit-print-color-adjust:exact;print-color-adjust:exact">\n'
       + svg + "\n"
       '<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;'
       'line-height:1.65;text-align:left">' + caption + "</figcaption>\n"
       "</figure>\n" + END)
print("existing <figure> in page: %d -> this one is 圖 %d" % (n_existing, num))

# ---- markdown: replace the whole fenced block -----------------------------------
md = io.open(MD, encoding="utf-8").read()
lines = md.split("\n")
mi = next((k for k, l in enumerate(lines) if MARKER in l), None)
if mi is None:
    raise SystemExit("marker not found in md")
a = mi
while a >= 0 and not lines[a].lstrip().startswith("```"):
    a -= 1
b = mi
while b < len(lines) and not lines[b].lstrip().startswith("```"):
    b += 1
print("md block: lines %d..%d (%d lines, fence=%r)"
      % (a + 1, b + 1, b - a - 1, lines[a].strip()))
md2 = "\n".join(lines[:a] + [fig] + lines[b + 1:])
io.open(MD, "w", encoding="utf-8", newline="\r\n").write(md2)

# ---- html: replace the enclosing codehilite div ---------------------------------
h = io.open(HTML, encoding="utf-8").read()
hi = h.find(MARKER)
if hi < 0:
    raise SystemExit("marker not found in html")
d0 = h.rfind('<div class="codehilite">', 0, hi)
if d0 < 0:
    raise SystemExit("codehilite wrapper not found")
d1 = h.find("</div>", hi)
if d1 < 0:
    raise SystemExit("closing div not found")
d1 += len("</div>")
print("html block: %d..%d (%d chars, wrapper=%r)"
      % (d0, d1, d1 - d0, h[d0:d0 + 24]))
h2 = h[:d0] + fig + h[d1:]
io.open(HTML, "w", encoding="utf-8", newline="\r\n").write(h2)

print("\nreplaced in BOTH files")
print("  md   : %s -> %s bytes" % (format(len(md.encode('utf-8')), ","),
                                   format(len(md2.encode('utf-8')), ",")))
print("  html : %s -> %s bytes" % (format(len(h.encode('utf-8')), ","),
                                   format(len(h2.encode('utf-8')), ",")))
print("  svg inlined: %s bytes" % format(len(svg.encode('utf-8')), ","))
