# -*- coding: utf-8 -*-
"""Generate an SVG for the OpenCV 12-step image-processing pipeline.

Replaces the 43-line ASCII box-drawing diagram in source/opencv-notes/.
Data-driven: STEPS drives the layout, so cards are never hand-positioned twice.

Emits stacking-style artefacts:
    opencv-pipeline.svg      the figure
    _measure_opencv.html     wrapper for svg-figure-qa/measure_text.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
SVG_OUT = os.path.join(HERE, "opencv-pipeline.svg")
HTML_OUT = os.path.join(HERE, "_measure_opencv.html")
ARIA = "OpenCV 12 步影像處理流程"

W, H = 900, 1170
BG, CARD, CARD2 = "#0d1117", "#161b22", "#1c2230"
LINE, TXT, MUT = "#30363d", "#e6edf3", "#8b949e"
FONT = "'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif"
MONO = "'Cascadia Mono',Consolas,'Courier New',monospace"

STAGE = {
    "in":   ("#2dd4bf", "#0f3d38", "輸入／前處理"),
    "par":  ("#58a6ff", "#12294a", "平行處理"),
    "ana":  ("#fbbf24", "#3d2f08", "影像分析"),
    "feat": ("#c084fc", "#2e1a45", "特徵與匹配"),
}

# (number, stage, title, detail)
STEPS = [
    ("1", "in", "讀取　cv2.imread()", "得到 BGR 的 NumPy 矩陣"),
    ("2", "in", "色彩空間　cvtColor()", "BGR → RGB / Gray / HSV / LAB"),
    ("3", "in", "前處理", "resize → blur → threshold"),
    ("7", "ana", "濾波", "Gaussian / Median / Bilateral / Morphology"),
    ("8", "ana", "邊緣　Canny()", "Canny 邊緣偵測"),
    ("9", "ana", "輪廓 / 邊界框", "findContours → boundingRect"),
    ("10", "feat", "特徵　ORB_create()", "keypoints + descriptors"),
    ("11", "feat", "匹配　BFMatcher", "+ Lowe ratio test"),
    ("12", "feat", "Homography + RANSAC", "→ 辨識 / 拼接 / AR"),
]
BRANCH = [
    ("4", "par", "矩陣運算", "ROI / 遮罩 / 混合"),
    ("5", "par", "繪圖標註", "line / rect / text"),
    ("6", "par", "幾何變換", "warpAffine / Perspective"),
]

CARD_X, CARD_W, CARD_H = 150, 600, 64
MAIN_CX = CARD_X + CARD_W / 2
PITCH = 82
Y_TOP = 120
BR_X, BR_W, BR_H = 90, 220, 84
BR_XS = [BR_X, BR_X + BR_W + 30, BR_X + 2 * (BR_W + 30)]
BR_CX = [x + BR_W / 2 for x in BR_XS]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=15, fill=TXT, weight="normal", anchor="start", font=FONT):
    a = ' text-anchor="%s"' % anchor if anchor != "start" else ""
    w = ' font-weight="%s"' % weight if weight != "normal" else ""
    return ('<text x="%s" y="%s" font-size="%s" fill="%s"%s%s font-family="%s">%s</text>'
            % (x, y, size, fill, w, a, font, esc(s)))


def rect(x, y, w, h, fill=CARD, stroke=LINE, rx=10, sw=1.5):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"/>' % (x, y, w, h, rx, fill, stroke, sw))


def arrow(x1, y1, x2, y2, marker, stroke, width=2):
    return ('<path d="M %s %s L %s %s" fill="none" stroke="%s" stroke-width="%s" '
            'marker-end="url(#%s)"/>' % (x1, y1, x2, y2, stroke, width, marker))


def main_card(num, stage, title, detail, y):
    col, _, _ = STAGE[stage]
    o = [rect(CARD_X, y, CARD_W, CARD_H, fill=CARD, stroke=col + "66", rx=10)]
    o.append('<circle cx="%s" cy="%s" r="15" fill="%s" opacity="0.92"/>'
             % (CARD_X + 32, y + CARD_H / 2, col))
    o.append(text(CARD_X + 32, y + CARD_H / 2 + 5.5, num, 14, "#08141a", "700", "middle"))
    o.append(text(CARD_X + 60, y + 27, title, 15.5, TXT, "700"))
    o.append(text(CARD_X + 60, y + 48, detail, 12, MUT))
    return o


p = []
p.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" '
         'aria-label="%s" style="width:100%%;height:auto;display:block">' % (W, H, esc(ARIA)))
p.append('<defs>')
for k, (col, _, _) in STAGE.items():
    p.append('<marker id="a%s" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" '
             'markerHeight="6" orient="auto-start-reverse">'
             '<path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker>' % (k, col))
p.append('<marker id="agray" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" '
         'markerHeight="6" orient="auto-start-reverse">'
         '<path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker>')
p.append('</defs>')
p.append(rect(0.75, 0.75, W - 1.5, H - 1.5, fill=BG, stroke="#222b36", rx=16))
p.append(text(48, 52, "OpenCV 影像處理 12 步流程", 25, TXT, "700"))
p.append(text(48, 82, "從讀取到 Homography：每一步用哪個 API、拿到什麼產出", 14.5, MUT))

# --- 1-3: input / preprocessing -------------------------------------------------
ys = [Y_TOP + i * PITCH for i in range(3)]
for (num, stage, title, detail), y in zip(STEPS[:3], ys):
    p.extend(main_card(num, stage, title, detail, y))
for i in range(2):
    p.append(arrow(MAIN_CX, ys[i] + CARD_H, MAIN_CX, ys[i + 1] - 2, "ain", "#7d8590"))

# --- 4-6: three parallel branches ------------------------------------------------
BR_Y = ys[2] + CARD_H + 48
p.append('<path d="M %s %s L %s %s" fill="none" stroke="#7d8590" stroke-width="2"/>'
         % (MAIN_CX, ys[2] + CARD_H, MAIN_CX, BR_Y - 24))
p.append('<path d="M %s %s L %s %s" fill="none" stroke="#7d8590" stroke-width="2"/>'
         % (BR_CX[0], BR_Y - 24, BR_CX[-1], BR_Y - 24))
for cx in BR_CX:
    p.append(arrow(cx, BR_Y - 24, cx, BR_Y - 2, "apar", "#7d8590"))
for (num, stage, title, detail), x, cx in zip(BRANCH, BR_XS, BR_CX):
    col, _, _ = STAGE[stage]
    p.append(rect(x, BR_Y, BR_W, BR_H, fill=CARD2, stroke=col + "66", rx=10))
    p.append('<circle cx="%s" cy="%s" r="13" fill="%s" opacity="0.92"/>'
             % (x + 24, BR_Y + 24, col))
    p.append(text(x + 24, BR_Y + 29, num, 12.5, "#08141a", "700", "middle"))
    p.append(text(x + 44, BR_Y + 30, title, 14.5, TXT, "700"))
    p.append(text(x + 16, BR_Y + 60, detail, 11.5, MUT))

# --- merge back, then 7-12 -------------------------------------------------------
MG_Y = BR_Y + BR_H + 24
for cx in BR_CX:
    p.append('<path d="M %s %s L %s %s" fill="none" stroke="#7d8590" stroke-width="2"/>'
             % (cx, BR_Y + BR_H, cx, MG_Y))
p.append('<path d="M %s %s L %s %s" fill="none" stroke="#7d8590" stroke-width="2"/>'
         % (BR_CX[0], MG_Y, BR_CX[-1], MG_Y))
y7 = MG_Y + 36
p.append(arrow(MAIN_CX, MG_Y, MAIN_CX, y7 - 2, "aana", "#7d8590"))
ys2 = [y7 + i * PITCH for i in range(6)]
for (num, stage, title, detail), y in zip(STEPS[3:], ys2):
    p.extend(main_card(num, stage, title, detail, y))
for i in range(5):
    col = STAGE[STEPS[3 + i + 1][1]][0]
    p.append(arrow(MAIN_CX, ys2[i] + CARD_H, MAIN_CX, ys2[i + 1] - 2, "a" + STEPS[3 + i + 1][1], col))

# --- legend + footnote -----------------------------------------------------------
LEG_Y = ys2[-1] + CARD_H + 46
for i, k in enumerate(("in", "par", "ana", "feat")):
    col, _, label = STAGE[k]
    lx = 48 + i * 215
    p.append('<circle cx="%s" cy="%s" r="7" fill="%s"/>' % (lx + 7, LEG_Y - 4, col))
    p.append(text(lx + 22, LEG_Y, label, 13, MUT))
p.append(text(48, LEG_Y + 42, "步驟 4–6 是三條平行路線：影像可以只做其中一項，也可以依序組合。", 13, MUT))
p.append('</svg>')

svg = "\n".join(p)
io.open(SVG_OUT, "w", encoding="utf-8", newline="\n").write(svg)
print("wrote %s (%s bytes, %d text elements)"
      % (SVG_OUT, format(len(svg.encode("utf-8")), ","), svg.count("<text")))
print("canvas %dx%d, bottom of last card = %d" % (W, H, ys2[-1] + CARD_H))

html = ('<!DOCTYPE html>\n<html lang="zh-Hant"><head><meta charset="utf-8">'
        '<title>measure</title><style>body{background:#0d1117;margin:0;padding:20px}'
        'svg{display:block}</style></head><body>\n' + svg + '\n</body></html>\n')
io.open(HTML_OUT, "w", encoding="utf-8", newline="\n").write(html)
print("wrote %s" % HTML_OUT)
