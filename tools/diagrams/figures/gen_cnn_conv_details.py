# -*- coding: utf-8 -*-
"""cnn-conv-details: build the five inline SVG figures for the conv-layer page.

    python gen_cnn_conv_details.py     # writes cnn-conv-details/*.svg

Shares the primitives of gen_cnn_illustrated (same house style), numbers come
from verify_cnn_conv_details.py.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cnn-conv-details")
sys.path.insert(0, HERE)

from gen_cnn_illustrated import (  # noqa: E402
    BG, CELL, INK, DIM, LINE, TEAL, BLUE, AMBER, ROSE, VIOLET,
    esc, text, rect, arrow, matrix_g, empty_grid)

DEFS = ('<defs><marker id="ard" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="%s"/></marker></defs>' % DIM)

ARIA = {
    "single": "單一輸出值的計算：5×5 輸入左上角 3×3 區塊與 3×3 kernel 逐元素相乘相加得到 8，整張輸出為 3×3 特徵圖",
    "channels": "多通道卷積：三個輸入通道各配一個 3×3 kernel，分別算出 3、2、負 4，相加再加 bias 2 得到 3，輸出一格",
    "sizes": "四種 stride 與 padding 設定的輸出尺寸：28×28 輸入配 3×3 kernel，valid 得 26×26、same 得 28×28、stride 2 補 1 得 14×14、5×5 kernel 補 2 得 28×28",
    "receptive": "感受野成長：9×9 輸入上疊四層 3×3 卷積，第 1 層看 3×3、第 2 層 5×5、第 3 層 7×7、第 4 層 9×9",
    "dilation": "空洞卷積：3×3 kernel 在 dilation 1 時覆蓋 3×3、dilation 2 時覆蓋 5×5，但兩者都只有 9 個權重",
}

CAPTIONS = {
    "single": "一個輸出值＝局部區塊與 kernel 逐元素相乘、全部相加，再加上 bias。滑一格就換算下一個值。",
    "channels": "通道是「加起來」的維度：三個通道各算一份，總和才是一個輸出值；kernel 的深度必須等於輸入通道數。",
    "sizes": "同樣的 28×28 輸入，改 stride 與 padding 就是完全不同的輸出尺寸——公式只有一條。",
    "receptive": "感受野隨層數長大：每多一層 3×3、stride 1，就多看到外圍一圈。",
    "dilation": "空洞卷積用「跳著看」換視野：覆蓋範圍變 5×5，權重還是 9 個。",
}


def svg(slug, w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'role="img" aria-label="%s">%s<rect x="0.75" y="0.75" width="%s" '
            'height="%s" rx="16" fill="%s" stroke="#222b36" stroke-width="1.5"/>%s</svg>'
            % (w, h, esc(ARIA[slug]), DEFS, w - 1.5, h - 1.5, BG, body))


IMG5 = [[1, 2, 3, 0, 1],
        [0, 1, 2, 3, 1],
        [2, 0, 1, 1, 0],
        [1, 2, 0, 3, 1],
        [0, 1, 1, 2, 0]]
KER = [[1, 0, 1],
       [0, 1, 0],
       [1, 0, 1]]
FMAP = [[8, 5, 8],
        [3, 10, 5],
        [6, 4, 5]]


def fig_single():
    body = [text(40, 44, "一個輸出值是怎麼算出來的", 20, INK, "700"),
            text(40, 72, "5×5 影像、3×3 kernel、stride 1、不補邊 → 3×3 特徵圖", 13, DIM)]
    body.append(text(60, 126, "輸入 5×5", 13, INK, "700"))
    body.append(text(356, 126, "kernel 3×3", 13, INK, "700"))
    body.append(text(532, 126, "輸出 3×3", 13, INK, "700"))
    patch = [(r, c) for r in range(3) for c in range(3)]
    body.append(matrix_g(60, 140, 46, IMG5, 14, AMBER, patch))
    body.append(rect(60, 140, 138, 138, stroke=AMBER, sw=2.4, rx=6))
    body.append(matrix_g(356, 140, 40, KER, 13.5, BLUE, patch, base="#161b22"))
    body.append(matrix_g(532, 140, 44, FMAP, 13.5, AMBER, [(0, 0)]))
    body.append(arrow(294, 200, 346, 200))
    body.append(arrow(482, 206, 524, 206))
    body.append(text(700, 176, "滑一格再算一次：", 11.5, DIM))
    body.append(text(700, 198, "共 (5−3+1)² = 9 個位置", 11.5, DIM))
    body.append(rect(48, 392, 904, 108, stroke=BLUE + "55", fill="#1c2230", rx=12))
    body.append(text(68, 420, "左上角那一格：逐元素相乘再相加", 13.5, INK, "700"))
    body.append(text(68, 448,
                     "(1×1 + 2×0 + 3×1)  ＋  (0×0 + 1×1 + 2×0)  ＋  (2×1 + 0×0 + 1×1)"
                     "  =  4 + 1 + 3  =  8", 12.5, AMBER, "700"))
    body.append(text(68, 476, "bias 加在整個特徵圖上（這裡 bias = 0）；若 bias = 1，九格全部 +1。",
                     12, DIM))
    body.append(text(48, 534, "輸出尺寸：O = ⌊(W − K)/S⌋ + 1 = ⌊(5 − 3)/1⌋ + 1 = 3", 12, DIM))
    return svg("single", 1000, 560, "".join(body))


def fig_channels():
    rows = [("通道 1", TEAL, [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
             [[0, 1, 0], [0, 1, 0], [0, 1, 0]], "3"),
            ("通道 2", BLUE, [[2, 0, 1], [1, 0, 2], [0, 1, 0]],
             [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "2"),
            ("通道 3", VIOLET, [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
             [[0, -1, 0], [-1, 0, -1], [0, -1, 0]], "−4")]
    body = [text(40, 44, "多通道：三個通道加起來才是一個值", 20, INK, "700"),
            text(40, 72, "kernel 的深度必須等於輸入通道數；這裡是 3×3×3，共 27 個權重", 13, DIM)]
    ys = [104, 200, 296]
    allc = [(r, c) for r in range(3) for c in range(3)]
    for i, (name, colour, ch, ker, val) in enumerate(rows):
        y = ys[i]
        body.append(text(60, y + 49, name, 11.5, colour, "700"))
        body.append(matrix_g(140, y, 30, ch, 11, colour, ()))
        body.append(text(250, y + 44, "×", 15, DIM, "normal", "middle"))
        body.append(matrix_g(268, y, 30, ker, 11, colour, allc, base="#161b22"))
        body.append(text(378, y + 44, "=", 15, DIM, "normal", "middle"))
        body.append(text(400, y + 49, val, 16, colour, "700"))
        body.append('<line x1="428" y1="%s" x2="450" y2="%s" stroke="%s" '
                    'stroke-width="1.4"/>' % (y + 45, y + 45, LINE))
    body.append('<line x1="450" y1="149" x2="450" y2="341" stroke="%s" stroke-width="1.4"/>'
                % LINE)
    body.append(arrow(450, 245, 496, 245))
    body.append(rect(500, 190, 180, 92, stroke=AMBER + "99", sw=1.5, fill=CELL, rx=10))
    body.append(text(590, 220, "Σ + bias 2", 12.5, INK, "700", "middle"))
    body.append(text(590, 252, "3 + 2 − 4 + 2 = 3", 12.5, AMBER, "700", "middle"))
    body.append(arrow(686, 236, 720, 236))
    body.append(rect(724, 190, 130, 92, stroke=TEAL + "99", sw=1.5, fill=CELL, rx=10))
    body.append(text(789, 220, "輸出一格", 12, INK, "700", "middle"))
    body.append(text(789, 254, "3", 22, TEAL, "700", "middle"))
    body.append(text(40, 404, "這一層若用 64 個 kernel，就有 64 張特徵圖（64 個輸出通道），"
                               "每張 26×26（28×28 輸入、valid）。", 12, DIM))
    return svg("channels", 1000, 430, "".join(body))



def fig_sizes():
    cards = [("valid", "(28 − 3)/1 + 1", "26×26", TEAL, "邊角像素只被掃到 1 次"),
             ("same（p = 1）", "(28 + 2 − 3)/1 + 1", "28×28", BLUE,
              "尺寸不變，邊界用 0 補"),
             ("stride 2 + p = 1", "(28 + 2 − 3)/2 + 1", "14×14", AMBER,
              "一半解析度，常見於降採樣"),
             ("5×5 kernel + p = 2", "(28 + 4 − 5)/1 + 1", "28×28", VIOLET,
              "大 kernel 也能維持 same")]
    body = [text(40, 44, "同一張 28×28，四種設定", 20, INK, "700"),
            text(40, 72, "O = ⌊(W + 2P − K) / S⌋ + 1　（除不盡往下取整）", 13, DIM)]
    for i, (name, formula, result, colour, note) in enumerate(cards):
        cx = 30 + i * 235
        body.append(rect(cx, 96, 220, 170, stroke=colour + "88", sw=1.5, fill=CELL,
                         opacity=0.9))
        body.append(text(cx + 14, 124, name, 12, colour, "700"))
        body.append(text(cx + 14, 148, formula, 10.5, DIM))
        body.append(text(cx + 14, 192, result, 22, INK, "700"))
        body.append(text(cx + 14, 246, note, 10, DIM))
    body.append(text(40, 308, "same 的 padding 由 kernel 決定：K = 3 → P = 1、K = 5 → P = 2；"
                              "偶數 kernel 湊不出真正的 same。", 12, DIM))
    return svg("sizes", 1000, 340, "".join(body))


def fig_receptive():
    cell, n = 34, 9
    x0, y0 = 60, 100
    body = [text(40, 44, "感受野：每疊一層就多看一圈", 20, INK, "700"),
            text(40, 72, "四層 3×3、stride 1 的卷積，最深那一層的一個神經元看得到整張 9×9",
                 13, DIM)]
    body.append(empty_grid(x0, y0, cell, n, LINE, 0.8, 0.45))
    layers = [("第 1 層", 3, TEAL), ("第 2 層", 5, BLUE),
              ("第 3 層", 7, VIOLET), ("第 4 層", 9, AMBER)]
    for name, size, colour in layers:
        off = (n - size) // 2 * cell
        body.append(rect(x0 + off, y0 + off, size * cell, size * cell, stroke=colour,
                         sw=2.2 if size < 9 else 1.6, rx=4,
                         fill=(colour + "1a") if size == 3 else "none"))
    lx = 430
    for i, (name, size, colour) in enumerate(layers):
        y = 130 + i * 44
        body.append(rect(lx, y - 11, 12, 12, stroke=colour, sw=1.5, fill=colour + "44",
                         rx=3))
        body.append(text(lx + 22, y, "%s：%d×%d" % (name, size, size), 12, INK))
    body.append(text(lx, 322, "RFₙ = RFₙ₋₁ + (K − 1) × jump", 12, DIM))
    body.append(text(lx, 344, "jump = 前面所有 stride 的乘積", 12, DIM))
    body.append(text(60, 432, "若每層都 stride 2：3 → 7 → 15 → 31"
                               "（用解析度換視野，ResNet 之後很常見）", 12, DIM))
    return svg("receptive", 1000, 470, "".join(body))


def fig_dilation():
    body = [text(40, 44, "空洞卷積：跳著看，視野變大、參數不變", 20, INK, "700"),
            text(40, 72, "3×3 kernel、dilation 2 → 有效覆蓋 5×5，但還是只有 9 個權重", 13, DIM)]
    body.append(text(60, 118, "d = 1（一般卷積）", 12, TEAL, "700"))
    allc = [(r, c) for r in range(3) for c in range(3)]
    ones = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    body.append(matrix_g(60, 136, 40, ones, 12, TEAL, allc))
    body.append(rect(54, 130, 124, 124, stroke=TEAL + "66", sw=1.2, rx=6))
    body.append(text(60, 280, "覆蓋 3×3", 11.5, DIM))

    body.append(text(280, 104, "d = 2（空洞卷積）", 12, AMBER, "700"))
    body.append(empty_grid(280, 122, 40, 5, LINE, 0.8, 0.4))
    for r in range(0, 5, 2):
        for c in range(0, 5, 2):
            px, py = 280 + c * 40 + 4, 122 + r * 40 + 4
            body.append(rect(px, py, 32, 32, stroke=AMBER, sw=1.4, fill=AMBER + "26",
                             rx=4))
            body.append(text(px + 16, py + 21, "1", 12, INK, "normal", "middle"))
    body.append(rect(274, 116, 204, 204, stroke=AMBER + "66", sw=1.2, rx=6))
    body.append(text(280, 350, "覆蓋 5×5，同一組 9 個權重", 11.5, DIM))

    body.append(text(540, 140, "k_eff = d × (k − 1) + 1 = 2 × 2 + 1 = 5", 12.5, INK, "700"))
    body.append(text(540, 176, "28×28 輸入、p = 0 → 輸出 24×24", 12, DIM))
    body.append(text(540, 200, "28×28 輸入、p = 2 → 輸出 28×28", 12, DIM))
    body.append(text(540, 236, "代價：跳過的鄰居像素仍然看不到，細節會被略過；", 11.5, DIM))
    body.append(text(540, 258, "所以實務上常和一般卷積交錯使用（hybrid）。", 11.5, DIM))
    body.append(text(40, 404, "把 d 想成「kernel 元素之間的間隔」；d = 1 就退化成一般卷積。",
                     12, DIM))
    return svg("dilation", 1000, 430, "".join(body))


FIGS = {"single": fig_single, "channels": fig_channels, "sizes": fig_sizes,
        "receptive": fig_receptive, "dilation": fig_dilation}


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
