# -*- coding: utf-8 -*-
"""cnn-fully-connected: build the five inline SVG figures."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cnn-fully-connected")
sys.path.insert(0, HERE)

from gen_cnn_illustrated import (  # noqa: E402
    BG, CELL, INK, DIM, LINE, TEAL, BLUE, AMBER, ROSE, VIOLET,
    esc, text, rect, arrow, matrix_g, empty_grid)

DEFS = ('<defs><marker id="arf" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="%s"/></marker></defs>' % DIM)

ARIA = {
    "dense": "全連接層的形狀：3×4 的權重矩陣乘上 4 維輸入再加 3 維 bias，得到 3 個 logits 2.4、1.2、負 0.7",
    "flatten": "7×7×64 的特徵圖展平成 3136 維向量，接 Dense 128 再 Dense 10 加 softmax；展平本身沒有參數",
    "params": "參數量比較：小 CNN 的卷積層共 1248 個參數，全連接層共 50890 個，占 97.6%",
    "softmax": "softmax 把 logits 2.4、1.2、負 0.7 轉成 0.7428、0.2237、0.0335，總和 1.000000",
    "vote": "加權投票：4 個特徵各自對 3 個類別投一票，共 12 條邊、12 個獨立權重",
}

CAPTIONS = {
    "dense": "全連接層就是一次矩陣乘法：W（3×4）乘 x（4）加 b（3）。每個輸出神經元都看得到全部 4 個輸入。",
    "flatten": "Flatten 只重排資料、不做運算；真正花參數的是後面的 Dense。",
    "params": "同一個小 CNN：卷積層 1,248 個參數，全連接層 50,890 個——占全部參數 97.6%。",
    "softmax": "softmax 只做兩件事：取指數、除以總和。排序不變，總和一定是 1。",
    "vote": "把全連接層想成一場加權投票：每個特徵對每個類別都有一票，票的輕重就是權重。",
}


def svg(slug, w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'role="img" aria-label="%s">%s<rect x="0.75" y="0.75" width="%s" '
            'height="%s" rx="16" fill="%s" stroke="#222b36" stroke-width="1.5"/>%s</svg>'
            % (w, h, esc(ARIA[slug]), DEFS, w - 1.5, h - 1.5, BG, body))


def col(x, y, cell, vals, colour, label=None):
    """A vertical vector of numbers."""
    out = []
    for i, v in enumerate(vals):
        out.append(rect(x, y + i * cell, cell, cell, stroke=colour + "aa", sw=1.3,
                        fill=CELL, rx=4))
        out.append(text(x + cell / 2, y + i * cell + cell / 2 + 5, str(v), 13.5, INK,
                        "normal", "middle"))
    if label:
        out.append(text(x + cell / 2, y - 10, label, 11.5, DIM, "normal", "middle"))
    return "".join(out)


def fig_dense():
    body = [text(40, 44, "全連接層＝一次矩陣乘法", 20, INK, "700"),
            text(40, 72, "4 個輸入、3 個輸出：W 是 3×4、b 是 3，輸出 3 個 logits", 13, DIM)]
    body.append(text(60, 118, "W（m×n = 3×4）", 11.5, DIM))
    body.append(matrix_g(60, 130, 46, [[0.2, 0.4, -0.1, 0.5],
                                       [0.7, -0.3, 0.2, 0.1],
                                       [-0.5, 0.6, 0.8, -0.2]], 11, TEAL, ()))
    body.append(text(258, 208, "·", 16, DIM, "normal", "middle"))
    body.append(col(276, 130, 46, ["2", "1", "0", "3"], BLUE, "x"))
    body.append(text(340, 208, "=", 16, DIM, "normal", "middle"))
    body.append(col(356, 130, 46, ["2.4", "1.2", "−0.7"], TEAL, "Wx"))
    body.append(text(424, 208, "+", 16, DIM, "normal", "middle"))
    body.append(col(440, 130, 46, ["0.1", "−0.2", "0.3"], AMBER, "b"))
    body.append(text(508, 208, "=", 16, DIM, "normal", "middle"))
    body.append(col(524, 130, 46, ["2.4", "1.2", "−0.7"], ROSE, "logits"))
    body.append(rect(620, 116, 340, 140, stroke=TEAL + "55", fill="#1c2230", rx=12))
    body.append(text(640, 144, "z₁ 怎麼來的（第一列 · x + b₁）", 12, INK, "700"))
    body.append(text(640, 172, "0.2×2 + 0.4×1 + (−0.1)×0 + 0.5×3", 11.5, DIM))
    body.append(text(640, 194, "= 0.4 + 0.4 + 0 + 1.5 = 2.3", 11.5, DIM))
    body.append(text(640, 218, "2.3 + 0.1 = 2.4", 12.5, TEAL, "700"))
    body.append(text(640, 242, "三列各自做一次，就是 z", 11, DIM))
    body.append(text(40, 336, "每一個輸出都連到全部 4 個輸入：W 有 12 個權重、"
                               "b 有 3 個，合計 15 個參數。", 12, DIM))
    body.append(text(40, 360, "z₃ 是負的——logits 可以是任意實數，"
                               "要經過 softmax 才是機率。", 12, DIM))
    return svg("dense", 1000, 400, "".join(body))


def fig_flatten():
    body = [text(40, 44, "Flatten：只重排、不運算", 20, INK, "700"),
            text(40, 72, "7×7×64 的特徵圖展平成 3136 維；這一步沒有參數", 13, DIM)]
    for i in range(3):
        x = 55 + i * 111
        body.append(rect(x, 130, 96, 96, stroke=TEAL + "88", sw=1.4, fill=CELL, rx=6,
                         opacity=0.95))
        body.append(text(x + 48, 184, "7×7", 12, DIM, "normal", "middle"))
    body.append(text(55, 256, "…共 64 個通道", 11.5, DIM))
    body.append(arrow(392, 178, 430, 178))
    body.append(text(411, 160, "flatten", 11, DIM, "normal", "middle"))
    for i in range(12):
        body.append(rect(436 + i * 16, 156, 14, 44, stroke=BLUE + "88", sw=1.1,
                         fill=CELL, rx=3))
    body.append(text(436, 148, "3136 維", 11, BLUE, "700"))
    body.append(arrow(636, 178, 668, 178))
    body.append(rect(672, 138, 120, 80, stroke=TEAL, sw=1.6, fill=CELL, rx=9))
    body.append(text(732, 172, "Dense 128", 12, INK, "700", "middle"))
    body.append(text(732, 194, "參數 50,240", 10.5, DIM, "normal", "middle"))
    body.append(arrow(798, 178, 830, 178))
    body.append(rect(834, 138, 136, 80, stroke=ROSE, sw=1.6, fill=CELL, rx=9))
    body.append(text(902, 170, "Dense 10", 12, INK, "700", "middle"))
    body.append(text(902, 190, "+ softmax", 10.5, DIM, "normal", "middle"))
    body.append(text(40, 316, "參數全在兩個 Dense：3136×128 + 128 = 401,536，"
                               "128×10 + 10 = 1,290。", 12, DIM))
    return svg("flatten", 1000, 350, "".join(body))


def fig_params():
    rows = [("卷積層（3×3×1→8、3×3×8→16）", 1248, TEAL),
            ("全連接 784 → 64", 50240, ROSE),
            ("全連接 64 → 10", 650, AMBER)]
    body = [text(40, 44, "參數幾乎都在全連接層", 20, INK, "700"),
            text(40, 72, "同一個 MNIST 小 CNN：總計 52,138 個參數，全連接占 50,890（97.6%）",
                 13, DIM)]
    x0, x1 = 360, 880
    scale = (x1 - x0) / 50240.0
    for i, (name, val, colour) in enumerate(rows):
        y = 122 + i * 58
        body.append(text(340, y + 5, name, 11.5, INK, "normal", "end"))
        body.append(rect(x0, y - 12, max(val * scale, 3), 24, stroke="none",
                         fill=colour, rx=4, sw=1, opacity=0.85))
        body.append(text(x0 + max(val * scale, 3) + 10, y + 5, "{:,}".format(val), 12,
                         colour, "700"))
    body.append(text(40, 320, "另一組對照：3136 → 128 是 401,536 個參數；"
                               "同樣輸入直接接 10 類只要 31,370 個（差 12.8 倍）。", 12, DIM))
    body.append(text(40, 344, "全連接是 m×n + m；卷積是 (k×k×C_in + 1)×C_out，"
                               "與影像大小無關。", 12, DIM))
    return svg("params", 1000, 380, "".join(body))


def fig_softmax():
    probs = [("貓", 0.7428, "2.4"), ("狗", 0.2237, "1.2"), ("鳥", 0.0335, "−0.7")]
    body = [text(40, 44, "Softmax：把 logits 變成加總為 1 的機率", 20, INK, "700"),
            text(40, 72, "pⱼ = e^zⱼ / Σ e^z_k；排序不變，總和一定是 1", 13, DIM)]
    body.append(text(60, 118, "logits", 11.5, DIM))
    body.append(text(316, 118, "機率", 11.5, DIM))
    for i, (name, p, z) in enumerate(probs):
        y = 150 + i * 46
        body.append(text(60, y + 5, name, 12.5, INK, "700"))
        body.append(text(140, y + 5, z, 12.5, DIM))
        body.append(arrow(240, y, 296, y))
        body.append(rect(316, y - 12, max(p * 460, 4), 24, stroke="none",
                         fill=TEAL if i == 0 else BLUE, rx=4, sw=1, opacity=0.9))
        body.append(text(326 + max(p * 460, 4), y + 5, "%.4f" % p, 12,
                         TEAL if i == 0 else DIM))
    body.append(text(316, 300, "0.7428 + 0.2237 + 0.0335 = 1.000000", 12, DIM))
    body.append(rect(60, 320, 880, 80, stroke=BLUE + "55", fill="#1c2230", rx=12))
    body.append(text(80, 348, "實測兩個性質：① 全部 logits 同時 +100，機率完全不變"
                               "（平移不變）", 12, INK))
    body.append(text(80, 374, "② argmax 不變（2.4 還是最大）；logits 差距 3.10，"
                               "機率比 22.2 倍", 12, DIM))
    return svg("softmax", 1000, 420, "".join(body))


def fig_vote():
    feats = [("x₁ = 2", TEAL), ("x₂ = 1", TEAL), ("x₃ = 0", TEAL), ("x₄ = 3", TEAL)]
    classes = [("貓", TEAL), ("狗", BLUE), ("鳥", VIOLET)]
    W = [[0.2, 0.4, -0.1, 0.5],
         [0.7, -0.3, 0.2, 0.1],
         [-0.5, 0.6, 0.8, -0.2]]
    body = [text(40, 44, "把全連接層想成一場加權投票", 20, INK, "700"),
            text(40, 72, "12 條邊就是 12 個獨立權重；線越粗代表票越重，紅色是負票", 13, DIM)]
    fy = [110, 186, 262, 338]
    cy = [150, 234, 318]
    for i, (name, colour) in enumerate(feats):
        body.append(rect(60, fy[i], 120, 52, stroke=colour, sw=1.5, fill=CELL, rx=9))
        body.append(text(120, fy[i] + 32, name, 12, INK, "700", "middle"))
    for j, (name, colour) in enumerate(classes):
        body.append(rect(760, cy[j], 150, 56, stroke=colour, sw=1.6, fill=CELL, rx=9))
        body.append(text(835, cy[j] + 35, name, 14, INK, "700", "middle"))
    for j in range(3):
        for i in range(4):
            w = W[j][i]
            body.append('<line x1="180" y1="%s" x2="760" y2="%s" stroke="%s" '
                        'stroke-width="%.1f" opacity="0.55"/>'
                        % (fy[i] + 26, cy[j] + 28, TEAL if w > 0 else ROSE,
                           0.6 + abs(w) * 5))
    body.append(text(440, 410, "W[j][i] 就是「第 i 個特徵對第 j 個類別的票」"
                               "（粗細＝|w|，紅＝負票）", 12, DIM))
    return svg("vote", 1000, 440, "".join(body))


FIGS = {"dense": fig_dense, "flatten": fig_flatten, "params": fig_params,
        "softmax": fig_softmax, "vote": fig_vote}


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
