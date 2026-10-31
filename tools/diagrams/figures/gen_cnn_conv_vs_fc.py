# -*- coding: utf-8 -*-
"""cnn-conv-vs-fc: build the four comparison figures."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cnn-conv-vs-fc")
sys.path.insert(0, HERE)

from gen_cnn_illustrated import (  # noqa: E402
    BG, CELL, INK, DIM, LINE, TEAL, BLUE, AMBER, ROSE, VIOLET,
    esc, text, rect, arrow, matrix_g, empty_grid)

DEFS = ('<defs><marker id="arv" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="%s"/></marker></defs>' % DIM)

ARIA = {
    "side-by-side": "同一個 7×7 輸入的兩種接法：左邊卷積用一個 3×3 kernel 掃過 9 個位置共用 9 個權重，右邊全連接把每個輸入連到每個輸出、每條邊一個權重",
    "params-log": "參數量對數比較：卷積 320 個、全連接 784 到 128 是 100480 個、全連接 784 到 25088 是 19694080 個",
    "scaling": "輸入變大時參數怎麼變：全連接每放大一倍邊長就變四倍，卷積維持 320 個不變",
    "translation": "平移特性：同一個 3×3 圖樣出現在 5×5 影像的兩個位置，卷積用同一組 9 個權重都偵測得到，全連接要為每個位置各學一套共 81 個權重",
}

CAPTIONS = {
    "side-by-side": "左邊：一個 kernel 掃 9 個位置，只有 9 個權重。右邊：每一條邊都是獨立權重，4×3 就是 12 個。",
    "params-log": "換算成「同樣產出 25,088 個值」：卷積 320 個參數，全連接 1,969 萬個——差 61,544 倍（對數刻度，每格 10 倍）。",
    "scaling": "輸入邊長從 28 放大到 224，全連接的參數變 64 倍；卷積還是 320 個。",
    "translation": "同一組 9 個權重就能在任何位置偵測到同一個圖樣；全連接得為每個位置準備一套，權重是 9 倍。",
}


def svg(slug, w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'role="img" aria-label="%s">%s<rect x="0.75" y="0.75" width="%s" '
            'height="%s" rx="16" fill="%s" stroke="#222b36" stroke-width="1.5"/>%s</svg>'
            % (w, h, esc(ARIA[slug]), DEFS, w - 1.5, h - 1.5, BG, body))


def fig_side_by_side():
    body = [text(40, 44, "同一張輸入，兩種接法", 20, INK, "700"),
            text(40, 72, "左：局部連接＋權重共享；右：完全連接，每條邊一個權重", 13, DIM)]
    # ---- left: convolution
    body.append(rect(30, 96, 420, 250, stroke=TEAL + "66", sw=1.4, fill=CELL, rx=12,
                     opacity=0.6))
    body.append(text(50, 124, "卷積層", 13, TEAL, "700"))
    body.append(text(50, 146, "一個 3×3 kernel 掃 9 個位置 → 9 個權重", 11, DIM))
    for i in range(7):
        for j in range(7):
            body.append(rect(60 + j * 30, 164 + i * 30, 30, 30, stroke=LINE, sw=0.8,
                             fill="none", opacity=0.5))
    body.append(rect(60, 164, 90, 90, stroke=AMBER, sw=2.2, rx=4, fill=AMBER + "1a"))
    body.append(rect(150, 254, 90, 90, stroke=AMBER, sw=1.6, rx=4, fill="none",
                     opacity=0.6))
    body.append(text(105, 300, "同一組 9 個權重", 10.5, AMBER, "700", "middle"))
    body.append(text(330, 210, "7×7 輸入", 11.5, DIM))
    body.append(text(330, 232, "輸出 5×5", 11.5, DIM))
    body.append(text(330, 254, "參數 9 + 1", 11.5, TEAL, "700"))
    # ---- right: fully connected
    body.append(rect(500, 96, 470, 250, stroke=VIOLET + "66", sw=1.4, fill=CELL, rx=12,
                     opacity=0.6))
    body.append(text(520, 124, "全連接層", 13, VIOLET, "700"))
    body.append(text(520, 146, "每個輸入連到每個輸出 → 4×3 = 12 條邊", 11, DIM))
    fy = [176, 216, 256, 296]
    cy = [196, 246, 296]
    for i in range(4):
        body.append('<circle cx="560" cy="%s" r="12" fill="%s"/>' % (fy[i], TEAL))
        body.append(text(538, fy[i] + 4, "x%d" % (i + 1), 10.5, DIM, "normal", "end"))
    for j in range(3):
        body.append('<circle cx="900" cy="%s" r="14" fill="%s"/>' % (cy[j], ROSE))
        body.append(text(922, cy[j] + 4, "z%d" % (j + 1), 10.5, DIM))
    for i in range(4):
        for j in range(3):
            body.append('<line x1="572" y1="%s" x2="886" y2="%s" stroke="%s" '
                        'stroke-width="1" opacity="0.45"/>' % (fy[i], cy[j], DIM))
    body.append(text(730, 336, "12 條邊 = 12 個獨立權重", 11, VIOLET, "700", "middle"))
    body.append(text(40, 380, "兩邊看到的輸入一樣大；差別在「同一個權重要不要重複用」。", 12, DIM))
    return svg("side-by-side", 1000, 410, "".join(body))


def fig_params_log():
    rows = [("卷積 3×3、C_out 32", 320, TEAL),
            ("全連接 784 → 128", 100480, AMBER),
            ("全連接 784 → 25,088", 19694080, ROSE)]
    x0, x1 = 420, 830
    lo, hi = 2.0, 7.6
    body = [text(40, 44, "同樣產出 25,088 個值，參數差 61,544 倍", 20, INK, "700"),
            text(40, 72, "對數刻度（每格 10 倍）；卷積的 320 個參數是含 bias 的總數", 13, DIM)]

    def px(v):
        return x0 + (math.log10(v) - lo) / (hi - lo) * (x1 - x0)
    for e in range(2, 8):
        body.append('<line x1="%s" y1="104" x2="%s" y2="272" stroke="%s" '
                    'stroke-width="0.8" opacity="0.25"/>' % (px(10 ** e), px(10 ** e),
                                                              DIM))
        body.append(text(px(10 ** e), 292, "10^%d" % e, 10, DIM, "normal", "middle"))
    for i, (name, val, colour) in enumerate(rows):
        y = 124 + i * 56
        body.append(text(400, y + 5, name, 11.5, INK, "normal", "end"))
        body.append(rect(x0, y - 13, max(px(val) - x0, 3), 26, stroke="none", fill=colour,
                         rx=4, sw=1, opacity=0.85))
        body.append(text(px(val) + 10, y + 5, "{:,}".format(val), 11.5, colour, "700"))
    body.append(text(40, 340, "算力也差 87 倍：卷積 225,792 次乘加，全連接 19,668,992 次。",
                     12, DIM))
    body.append(text(40, 364, "參數少不代表算得少——卷積把權重重複用，所以每個位置都要再算一次。",
                     12, DIM))
    return svg("params-log", 1000, 400, "".join(body))



def fig_scaling():
    sides = [28, 56, 112, 224, 448]
    fc = [(s * s) * 128 + 128 for s in sides]
    conv = 320
    x0, dx = 150, 170
    lo, hi = 2.2, 7.8

    def px(i):
        return x0 + i * dx

    def py(v):
        return 300 - (math.log10(v) - lo) / (hi - lo) * 210
    body = [text(40, 44, "輸入變大時，誰的參數跟著長", 20, INK, "700"),
            text(40, 72, "全連接 784 → 128 與卷積 3×3 → 32 通道；縱軸是對數", 13, DIM)]
    for e in range(3, 8):
        body.append('<line x1="130" y1="%s" x2="960" y2="%s" stroke="%s" '
                    'stroke-width="0.8" opacity="0.22"/>' % (py(10 ** e), py(10 ** e),
                                                              DIM))
        body.append(text(122, py(10 ** e) + 4, "10^%d" % e, 10, DIM, "normal", "end"))
    for i, s in enumerate(sides):
        body.append(text(px(i), 322, str(s), 11, DIM, "normal", "middle"))
    pts_fc = " ".join("%s,%s" % (px(i), py(v)) for i, v in enumerate(fc))
    body.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.4"/>'
                % (pts_fc, ROSE))
    for i, v in enumerate(fc):
        body.append('<circle cx="%s" cy="%s" r="4" fill="%s"/>' % (px(i), py(v), ROSE))
    body.append(text(px(4) + 6, py(fc[-1]) + 4, "2,569 萬", 11, ROSE, "700"))
    body.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="2.4"/>'
                % (px(0), py(conv), px(4), py(conv), TEAL))
    body.append(text(px(0) + 8, py(conv) - 12, "卷積 320（不變）", 11, TEAL, "700"))
    body.append(text(520, 348, "輸入邊長（28 → 448）", 11.5, DIM, "normal", "middle"))
    body.append(text(40, 380, "28 → 224 讓全連接長成 64 倍；卷積完全不受影響——"
                               "這就是「卷積能處理高解析度影像」的根本原因。", 12, DIM))
    return svg("scaling", 1000, 410, "".join(body))


def fig_translation():
    imgs = [(0, 0), (2, 2)]
    body = [text(40, 44, "平移特性：同一個圖樣出現在不同位置", 20, INK, "700"),
            text(40, 72, "5×5 輸入、3×3 的圖樣、3×3 的偵測器；兩個位置都用同一組權重",
                 13, DIM)]
    for k, (r, c) in enumerate(imgs):
        x = 60 + k * 210
        body.append(empty_grid(x, 120, 40, 5, LINE, 0.9, 0.55))
        body.append(rect(x + c * 40, 120 + r * 40, 120, 120, stroke=AMBER, sw=2, rx=4,
                         fill=AMBER + "1a"))
        body.append(text(x + 100, 344, "圖樣在 (%d, %d)" % (r, c), 11, DIM, "normal",
                         "middle"))
        body.append(arrow(x + 100, 352, x + 100, 386))
    body.append(rect(480, 106, 180, 96, stroke=TEAL, sw=1.6, fill=CELL, rx=10))
    body.append(text(570, 138, "同一個 kernel", 12, INK, "700", "middle"))
    body.append(text(570, 162, "9 個權重", 12, TEAL, "700", "middle"))
    body.append(text(570, 186, "兩處都回應 5", 10.5, DIM, "normal", "middle"))
    body.append(rect(690, 106, 270, 210, stroke=ROSE + "88", sw=1.4, fill=CELL, rx=10))
    body.append(text(710, 134, "全連接的做法", 12, ROSE, "700"))
    body.append(text(710, 162, "每個位置一套權重：", 11.5, INK))
    body.append(text(710, 186, "9 個位置 × 9 個權重", 11.5, INK))
    body.append(text(710, 212, "= 81 個（9 倍）", 12.5, ROSE, "700"))
    body.append(text(710, 244, "而且每一種位移都要", 11, DIM))
    body.append(text(710, 264, "在資料裡出現過才學得會", 11, DIM))
    body.append(text(40, 414, "同一組權重 → 同一個特徵在任何位置都認得；"
                               "這就是卷積的平移等變性。", 12, DIM))
    return svg("translation", 1000, 440, "".join(body))


FIGS = {"side-by-side": fig_side_by_side, "params-log": fig_params_log,
        "scaling": fig_scaling, "translation": fig_translation}


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug in FIGS:
        path = os.path.join(OUT, slug + ".svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(FIGS[slug]())
        print("wrote", path)
    print("\nfigures:", len(CAPTIONS))


if __name__ == "__main__":
    main()
