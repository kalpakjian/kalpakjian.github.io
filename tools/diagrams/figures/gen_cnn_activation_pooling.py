# -*- coding: utf-8 -*-
"""cnn-activation-pooling: build the five inline SVG figures.

    python gen_cnn_activation_pooling.py     # writes cnn-activation-pooling/*.svg
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cnn-activation-pooling")
sys.path.insert(0, HERE)

from gen_cnn_illustrated import (  # noqa: E402
    BG, CELL, INK, DIM, LINE, TEAL, BLUE, AMBER, ROSE, VIOLET,
    esc, text, rect, arrow, matrix_g, empty_grid)

DEFS = ('<defs><marker id="ara" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="%s"/></marker></defs>' % DIM)

ARIA = {
    "relu-variants": "三個激活函數的折線圖：ReLU 在負區間為 0、Leaky ReLU 帶小斜率、GELU 是平滑曲線；左側是同一組輸入的實際輸出值",
    "maxpool": "最大池化：4×4 特徵圖切成四個 2×2 窗口，各取最大值 6、8、3、4，輸出 2×2，數值由 16 個減為 4 個",
    "pool-configs": "三種池化設定的輸出尺寸：2×2 步幅 2 得 2×2、2×2 步幅 1 重疊得 3×3、3×3 步幅 2 補 1 得 2×2",
    "gap": "全域平均池化：三個 7×7 的特徵圖各自平均成一個數字，得到長度 512 的向量，沒有任何參數",
    "block": "一個 CNN block 的形狀流：32×32×3 經 Conv 3×3 32 個 filter 補 1 得到 32×32×32、ReLU 不變、MaxPool 2×2 步幅 2 得到 16×16×32",
}

CAPTIONS = {
    "relu-variants": "ReLU 把負的整段壓成 0；Leaky ReLU 留一點斜率；GELU 則是平滑版本。三者在正區間幾乎一樣。",
    "maxpool": "最大池化只留下每個窗口的冠軍。16 個值變 4 個（少 75%），但最強的響應一個都沒丟。",
    "pool-configs": "同樣的 4×4 特徵圖，三種設定給出三種輸出尺寸；步幅 1 會讓窗口重疊，步幅 2 不重疊。",
    "gap": "GAP 把每個通道壓成一個數字：參數 0，輸出長度就等於通道數，常用來取代 Flatten + 全連接。",
    "block": "一個 block 的三層：只有 Conv 有參數（896 個），ReLU 與 Pool 都是 0 個。",
}


def svg(slug, w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'role="img" aria-label="%s">%s<rect x="0.75" y="0.75" width="%s" '
            'height="%s" rx="16" fill="%s" stroke="#222b36" stroke-width="1.5"/>%s</svg>'
            % (w, h, esc(ARIA[slug]), DEFS, w - 1.5, h - 1.5, BG, body))



def fig_relu_variants():
    """Left: a value table. Right: the three curves over x in [-4, 4]."""
    rows = [("-3", "0", "−0.30"), ("-1", "0", "−0.10"),
            ("0", "0", "0"), ("0.5", "0.5", "0.50"), ("2", "2", "2.00")]
    body = [text(40, 44, "ReLU 與它的三個變體", 20, INK, "700"),
            text(40, 72, "差別全在負區間：ReLU 直接壓成 0，Leaky 留小斜率，GELU 平滑過渡",
                 13, DIM)]
    body.append(text(60, 116, "輸入 x", 11.5, DIM))
    body.append(text(150, 116, "ReLU", 11.5, TEAL))
    body.append(text(250, 116, "Leaky(0.1)", 11.5, AMBER))
    for i, (x, r, lk) in enumerate(rows):
        y = 146 + i * 30
        body.append(text(60, y, x, 12.5, INK))
        body.append(text(150, y, r, 12.5, TEAL))
        body.append(text(250, y, lk, 12.5, AMBER))
    body.append(text(60, 330, "GELU 不是折線：x = −1 時是 −0.1588，", 11.5, DIM))
    body.append(text(60, 352, "x = 0.5 時是 0.3457（實測）。", 11.5, DIM))

    def px(v):
        return 560 + v * 55

    def py(v):
        return 250 - v * 40
    body.append(text(430, 100, "三個函數疊在一起", 12.5, INK, "700"))
    body.append('<line x1="420" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1"/>'
                % (py(0), px(4.6), py(0), DIM))
    body.append('<line x1="%s" y1="96" x2="%s" y2="316" stroke="%s" stroke-width="1"/>'
                % (px(0), px(0), DIM))
    body.append('<polyline points="%s,%s %s,%s %s,%s" fill="none" stroke="%s" '
                'stroke-width="2.6" stroke-linejoin="round"/>'
                % (px(-4), py(0), px(0), py(0), px(4), py(4), TEAL))
    body.append('<polyline points="%s,%s %s,%s" fill="none" stroke="%s" '
                'stroke-width="2.2" stroke-linejoin="round"/>'
                % (px(-4), py(-0.4), px(4), py(4), AMBER))
    pts = []
    for i in range(33):
        v = -4 + i * 0.25
        g = 0.5 * v * (1 + math.tanh(math.sqrt(2 / math.pi) * (v + 0.044715 * v ** 3)))
        pts.append("%.1f,%.1f" % (px(v), py(g)))
    body.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2" '
                'stroke-dasharray="5 3"/>' % (" ".join(pts), VIOLET))
    for v in (-4, 0, 4):
        body.append(text(px(v), py(0) + 20, str(v), 11, DIM, "normal", "middle"))
    body.append(text(px(4) + 12, py(4) + 4, "4", 11, DIM))
    body.append(text(px(0) + 8, 108, "y", 11.5, DIM))
    body.append(rect(740, 300, 12, 12, stroke=TEAL, sw=1.5, fill=TEAL + "44", rx=3))
    body.append(text(760, 311, "ReLU", 11, DIM))
    body.append(rect(740, 330, 12, 12, stroke=AMBER, sw=1.5, fill=AMBER + "44", rx=3))
    body.append(text(760, 341, "Leaky ReLU", 11, DIM))
    body.append(rect(880, 300, 12, 12, stroke=VIOLET, sw=1.5, fill=VIOLET + "44", rx=3))
    body.append(text(900, 311, "GELU", 11, DIM))
    return svg("relu-variants", 1000, 400, "".join(body))


def fig_maxpool():
    m = [[1, 1, 2, 4],
         [5, 6, 7, 8],
         [3, 2, 1, 0],
         [1, 2, 3, 4]]
    quads = [(0, 0, TEAL), (0, 1, BLUE), (1, 0, VIOLET), (1, 1, AMBER)]
    out = [[6, 8], [3, 4]]
    winners = [(1, 1), (3, 1), (1, 2), (3, 3)]   # global (col,row) of each winner
    body = [text(40, 44, "最大池化：每個窗口只留冠軍", 20, INK, "700"),
            text(40, 72, "4×4 特徵圖、2×2 窗口、步幅 2 → 2×2 輸出；通道之間互不相干", 13, DIM)]
    body.append(text(60, 112, "輸入 4×4", 13, INK, "700"))
    allc = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for (r, c, colour) in quads:
        sub = [[m[r * 2][c * 2], m[r * 2][c * 2 + 1]],
               [m[r * 2 + 1][c * 2], m[r * 2 + 1][c * 2 + 1]]]
        body.append(matrix_g(60 + c * 104, 126 + r * 104, 52, sub, 14, colour, allc))
    for (col, row) in winners:
        body.append(rect(60 + col * 52, 126 + row * 52, 52, 52, stroke=INK, sw=1.8, rx=3))
    body.append(arrow(276, 230, 340, 230))
    body.append(text(308, 208, "取最大", 11.5, DIM, "normal", "middle"))
    body.append(text(350, 158, "輸出 2×2", 13, INK, "700"))
    body.append(matrix_g(350, 174, 56, out, 16, TEAL, ()))
    body.append(text(350, 306, "16 個值 → 4 個值（−75%）", 11.5, DIM))
    body.append(text(560, 176, "每個通道各自池化：", 12, DIM))
    body.append(text(560, 200, "32 通道進、32 通道出", 12, INK, "700"))
    body.append(text(560, 236, "參數 0 個", 12, TEAL, "700"))
    body.append(text(560, 268, "反向傳播時，梯度只回給", 11.5, DIM))
    body.append(text(560, 288, "每個窗口裡「最大值」那一格", 11.5, DIM))
    body.append(text(40, 372, "白色方框＝每個窗口的冠軍。池化不做加權，所以沒有東西要學。", 12, DIM))
    return svg("maxpool", 1000, 400, "".join(body))



def fig_pool_configs():
    """Same 4x4 map, three pooling settings."""
    cards = [("2×2、步幅 2", "(4 − 2)/2 + 1 = 2", [[6, 8], [3, 4]], "2×2", TEAL,
              "不重疊，最常見的設定"),
             ("2×2、步幅 1", "(4 − 2)/1 + 1 = 3", [[6, 7, 8], [6, 7, 8], [3, 3, 4]], "3×3",
              BLUE, "窗口重疊，輸出變大"),
             ("3×3、步幅 2、補 1", "(4 + 2 − 3)/2 + 1 = 2", [[6, 8], [6, 8]], "2×2", AMBER,
              "補邊用 −∞，不會被選到")]
    body = [text(40, 44, "同一張 4×4，三種池化設定", 20, INK, "700"),
            text(40, 72, "O = ⌊(W − k + 2p) / s⌋ + 1", 13, DIM)]
    for i, (name, formula, out, size, colour, note) in enumerate(cards):
        cx = 30 + i * 320
        body.append(rect(cx, 96, 300, 214, stroke=colour + "88", sw=1.5, fill=CELL,
                         opacity=0.9))
        body.append(text(cx + 16, 122, name, 12.5, colour, "700"))
        body.append(text(cx + 16, 146, formula, 11, DIM))
        cell = 40 if len(out) <= 2 else 34
        body.append(matrix_g(cx + 16, 164, cell, out, 12 if cell == 34 else 14, colour, ()))
        body.append(text(cx + 24 + len(out) * cell + 12, 202, "→ " + size, 12, INK, "700"))
        body.append(text(cx + 16, 290, note, 10.5, DIM))
    body.append(text(40, 348, "池化沒有可學的參數，只有「怎麼掃」的設定；"
                               "預設是 2×2、步幅 2。", 12, DIM))
    return svg("pool-configs", 1000, 380, "".join(body))


def fig_gap():
    body = [text(40, 44, "全域平均池化（GAP）：每個通道壓成一個數", 20, INK, "700"),
            text(40, 72, "7×7×512 → 512；沒有參數，輸出長度就等於通道數", 13, DIM)]
    ys = [104, 190, 276]
    names = [("通道 1", TEAL, "0.42"), ("通道 2", BLUE, "0.11"), ("通道 3", VIOLET, "0.87")]
    for i, (name, colour, val) in enumerate(names):
        y = ys[i]
        body.append(text(60, y + 45, name, 11.5, colour, "700"))
        body.append(empty_grid(140, y, 26, 7, colour, 0.8, 0.55))
        body.append(arrow(330, y + 91, 372, y + 91))
        body.append(text(388, y + 96, "平均", 11, DIM))
        body.append(rect(440, y + 56, 92, 70, stroke=colour + "99", sw=1.4, fill=CELL,
                         rx=8))
        body.append(text(486, y + 100, val, 16, colour, "700", "middle"))
    body.append(text(140, 392, "7×7 = 49 個數字平均成 1 個；512 個通道就是 512 個數字", 12, DIM))
    body.append(text(560, 130, "GAP 之後接一個 Dense(10)，", 12, DIM))
    body.append(text(560, 152, "參數只有 5,120 + 10 = 5,130 個。", 12, INK, "700"))
    body.append(text(560, 190, "同樣的頭若先 Flatten（7×7×512 = 25,088）", 12, DIM))
    body.append(text(560, 212, "再接 Dense(10)，就是 250,890 個參數。", 12, ROSE, "700"))
    body.append(text(560, 250, "GAP 也讓輸入尺寸自由：換成 8×8 的圖，", 11.5, DIM))
    body.append(text(560, 270, "輸出照樣是 512 維，網路不必改。", 11.5, DIM))
    return svg("gap", 1000, 420, "".join(body))


def fig_block():
    steps = [("輸入", "32 × 32 × 3", TEAL, "—"),
             ("Conv 3×3、32 filters、補 1", "32 × 32 × 32", TEAL, "896"),
             ("ReLU", "32 × 32 × 32", BLUE, "0"),
             ("MaxPool 2×2、stride 2", "16 × 16 × 32", AMBER, "0")]
    body = [text(40, 44, "一個 block：Conv → ReLU → Pool", 20, INK, "700"),
            text(40, 72, "形狀只在 Conv 與 Pool 改變；參數只有 Conv 有", 13, DIM)]
    w, gap, x0, y0, bh = 190, 48, 45, 104, 66
    for i, (label, shape, colour, params) in enumerate(steps):
        x = x0 + i * (w + gap)
        body.append(rect(x, y0, w, bh, stroke=colour, sw=1.6, fill=CELL, rx=10,
                         opacity=0.9))
        body.append(text(x + w / 2, y0 + 40, label, 11.5, INK, "700", "middle"))
        body.append(text(x + w / 2, y0 + 100, shape, 12, colour, "700", "middle"))
        body.append(text(x + w / 2, y0 + 122, "參數 " + params, 10.5, DIM, "normal",
                         "middle"))
        if i < len(steps) - 1:
            body.append(arrow(x + w + 6, y0 + bh / 2, x + w + gap - 8, y0 + bh / 2))
    body.append(text(45, 292, "同一個 block 疊三次：32×32 → 16×16 → 8×8 → 4×4，"
                               "通道 3 → 32 → 64 → 128。", 12, DIM))
    body.append(text(45, 316, "解析度一路砍、通道一路加，這是 CNN 的固定節奏。", 12, DIM))
    return svg("block", 1000, 350, "".join(body))


FIGS = {"relu-variants": fig_relu_variants, "maxpool": fig_maxpool,
        "pool-configs": fig_pool_configs, "gap": fig_gap, "block": fig_block}


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
