# -*- coding: utf-8 -*-
"""圖解 CNN: build the eight inline SVG figures for source/cnn-illustrated/.

    python gen_figs.py        # writes figs/<slug>.svg and prints the caption map

Every label is a real <text> element (contract §12). Coordinates are constants,
repeated cells come from matrix_g() so a number never drifts from its cell.
Numbers come from verify_numbers.py (run it first).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cnn-illustrated")

BG, CELL = "#0d1117", "#12181f"
INK, DIM, LINE = "#e6edf3", "#8b949e", "#30363d"
TEAL, BLUE, AMBER, ROSE, VIOLET = "#4ecdc4", "#58a6ff", "#e0a458", "#ff7b72", "#c084fc"
FONT = "'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif"

DEFS = ('<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="%s"/></marker></defs>' % DIM)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(slug, w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'role="img" aria-label="%s">%s<rect x="0.75" y="0.75" width="%s" '
            'height="%s" rx="16" fill="%s" stroke="#222b36" stroke-width="1.5"/>%s</svg>'
            % (w, h, esc(ARIA[slug]), DEFS, w - 1.5, h - 1.5, BG, body))


def text(x, y, s, size=13, fill=INK, weight="normal", anchor="start"):
    a = ' text-anchor="%s"' % anchor if anchor != "start" else ""
    w = ' font-weight="%s"' % weight if weight != "normal" else ""
    return ('<text x="%s" y="%s" font-size="%s" fill="%s"%s%s font-family="%s">%s</text>'
            % (x, y, size, fill, w, a, FONT, esc(s)))


def rect(x, y, w, h, stroke=LINE, fill="none", rx=8, sw=1.4, opacity=None):
    o = ' opacity="%s"' % opacity if opacity is not None else ""
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" '
            'stroke-width="%s"%s/>' % (x, y, w, h, rx, fill, stroke, sw, o))


def arrow(x1, y1, x2, y2, colour=DIM):
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.5" '
            'marker-end="url(#ar)"/>' % (x1, y1, x2, y2, colour))


def matrix_g(x, y, cell, m, size=13.5, colour=AMBER, tint=(), tint_fill=None,
             base=CELL, sw=0.9, radius=4):
    """Grid of cells, one <text> per number. tinted cells get colour + fill."""
    out = []
    for r, row in enumerate(m):
        for c, val in enumerate(row):
            px, py = x + c * cell, y + r * cell
            if (r, c) in tint:
                out.append(rect(px, py, cell, cell, stroke=colour, rx=radius, sw=1.6,
                                fill=tint_fill or (colour + "26")))
            else:
                out.append(rect(px, py, cell, cell, stroke=LINE, rx=radius, sw=sw,
                                fill=base, opacity=0.85))
            out.append(text(px + cell / 2, py + cell / 2 + size * 0.36, str(val),
                            size, INK, "normal", "middle"))
    return "".join(out)


def empty_grid(x, y, cell, n, colour=LINE, sw=0.9, opacity=0.75):
    out = []
    for r in range(n):
        for c in range(n):
            out.append(rect(x + c * cell, y + r * cell, cell, cell, stroke=colour,
                            rx=3, sw=sw, fill="none", opacity=opacity))
    return "".join(out)


IMG5 = [[1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 1, 1],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0]]
KER = [[1, 0, 1],
       [0, 1, 0],
       [1, 0, 1]]
FMAP = [[4, 3, 4],
        [2, 4, 3],
        [2, 3, 4]]

ARIA = {
    "pipeline": "一個影像分類 CNN 的資料流：輸入 28×28×1 → Conv+ReLU 16 → Pool → Conv+ReLU 32 → Pool → Flatten 1568 維 → Dense+Softmax → 10 個類別機率，前段重複 N 次抽特徵，後段做分類",
    "conv": "卷積運算：3×3 核心在 5×5 影像上滑動，左上角 3×3 區塊與核心逐元素相乘再相加得到 4，整張輸出為 3×3 特徵圖",
    "hyper": "三種卷積設定對輸出尺寸的影響：不補邊 5×5 得 3×3、補一圈邊得 5×5、步幅 2 得 2×2",
    "multi": "多個濾波器：同一張 5×5 輸入分別用垂直邊緣、斜線、斑塊三個核心，得到三張 3×3 特徵圖，疊成三通道再送進下一層",
    "relu": "ReLU 激活函數：輸入負值全部變成 0，正值原樣保留；右側是折線圖 y = max(0, x)",
    "pool": "2×2 最大池化與平均池化：4×4 輸入切成四塊，最大池化取 6、8、4、9，平均池化取 3.75、5.25、2.5、3.75",
    "head": "分類頭：7×7×16 攤平成 784 維，接 64 個神經元，再由 softmax 把 logits 4.2、1.3、0.4 變成 0.9282、0.0511、0.0208 的機率",
    "mnist": "MNIST 小 CNN 的形狀階梯：28×28×1 → 28×28×8 → 14×14×8 → 14×14×16 → 7×7×16 → 784 維 → 64 維 → 10 個類別",
    "concept-arch": "概念架構：輸入 224×224×3 一路縮到 14×14×256 再攤平，最後由 Dense 加 softmax 給出貓 0.93、狗 0.05、鳥 0.02",
    "tasks": "同一張圖的三種任務：分類輸出一個標籤、偵測輸出框加類別、分割輸出逐像素遮罩",
}

CAPTIONS = {
    "pipeline": "整個分類網路：前段（卷積 → ReLU → 池化）重複 N 次抽特徵，後段攤平後接全連接層與 softmax；可訓練的參數只在 Conv 與 Dense。",
    "conv": "一個 3×3 核心在 5×5 影像上滑動。左上角那一格是九組乘積相加得到的 4；同一組 9 個權重會被每個位置重用。",
    "hyper": "同樣的 5×5 輸入、同樣的 3×3 核心，只改 padding 與 stride，輸出大小就完全不同——這就是 `O = (N + 2P − F) / S + 1` 的全部內容。",
    "multi": "一層用三個核心就得到三張特徵圖（三通道）。下一層的核心會同時讀這三個通道，所以「組合」是在通道維度上發生的。",
    "relu": "ReLU 只做一件事：把負的丟掉。沒有它，再多層卷積疊起來仍然等於一層線性變換。",
    "pool": "池化把 2×2 壓成一格：最大池化留下最強響應，平均池化留下平均亮度；兩者都沒有可訓練參數。",
    "head": "分類頭的工作：把攤平後的特徵向量壓成 10 個分數（logits），再用 softmax 轉成加總為 1 的機率。",
    "mnist": "一個能跑 MNIST 的小 CNN 的形狀階梯：卷積改通道數、池化砍面積、Flatten 只負責攤平、Dense 才做判斷。",
    "concept-arch": "概念架構的常見畫法：方塊高度就是解析度，一路變小、通道一路變多，最後才接決策頭。",
    "tasks": "同一張圖餵進同一個骨幹，換一個輸出頭就是另一個任務：分類只看有沒有、偵測要位置、分割要每個像素。",
}



def fig_pipeline():
    """Input -> (Conv+ReLU -> Pool) xN -> Flatten -> Dense -> softmax."""
    steps = [("輸入影像", "28×28×1", TEAL),
             ("Conv+ReLU", "3×3 ×16", TEAL),
             ("Pool 2×2", "14×14×16", BLUE),
             ("Conv+ReLU", "3×3 ×32", TEAL),
             ("Pool 2×2", "7×7×32", BLUE),
             ("Flatten", "1,568 維", AMBER),
             ("Dense", "128 + softmax", AMBER),
             ("類別機率", "10 個數字", ROSE)]
    w, gap, x0, y0, bh = 96, 26, 44, 104, 64
    body = [text(40, 44, "一個影像分類 CNN 的資料流", 20, INK, "700"),
            text(40, 70, "前段抽特徵，後段做判斷；中間那兩個 Pool 讓面積一路砍半", 13, DIM)]
    xs = []
    for i, (label, sub, colour) in enumerate(steps):
        x = x0 + i * (w + gap)
        xs.append(x)
        body.append(rect(x, y0, w, bh, stroke=colour, sw=1.6, fill=CELL, opacity=0.9))
        body.append(text(x + w / 2, y0 + 30, label, 12, INK, "700", "middle"))
        body.append(text(x + w / 2, y0 + 49, sub, 10, DIM, "normal", "middle"))
        if i < len(steps) - 1:
            body.append(arrow(x + w + 3, y0 + bh / 2, x + w + gap - 5, y0 + bh / 2))
    a0, a1 = xs[1], xs[4] + w
    b0, b1 = xs[5], xs[7] + w
    for (s, e, lab) in ((a0, a1, "特徵抽取：重複 N 次（卷積 → ReLU → 池化）"),
                        (b0, b1, "分類頭")):
        body.append('<line x1="%s" y1="96" x2="%s" y2="96" stroke="%s" '
                    'stroke-width="1"/>' % (s, e, LINE))
        body.append(text((s + e) / 2, 88, lab, 11, DIM, "normal", "middle"))
    body.append(text(40, 212, "同一組 filter 滑過整張圖（參數共享）→ 參數量與影像大小無關；"
                                "池化只降維，沒有可學的參數。", 12, DIM))
    return svg("pipeline", 1000, 250, "".join(body))


def fig_conv():
    """The worked example: 5x5 image, 3x3 kernel, 3x3 feature map."""
    body = [text(40, 44, "卷積：逐元素相乘再相加", 20, INK, "700"),
            text(40, 72, "3×3 核心滑過 5×5 影像，每一步在特徵圖上留下一個數字", 13, DIM)]

    body.append(text(60, 126, "輸入影像 5×5", 13, INK, "700"))
    body.append(text(356, 126, "3×3 核心", 13, INK, "700"))
    body.append(text(532, 126, "特徵圖 3×3", 13, INK, "700"))

    patch = [(r, c) for r in range(3) for c in range(3)]
    body.append(matrix_g(60, 140, 46, IMG5, 14, AMBER, patch))
    body.append(rect(60, 140, 138, 138, stroke=AMBER, sw=2.4, rx=6))
    body.append(matrix_g(356, 140, 40, KER, 13.5, BLUE, patch, base="#161b22"))
    body.append(matrix_g(532, 140, 44, FMAP, 13.5, AMBER, [(0, 0)]))

    body.append(arrow(294, 200, 346, 200))
    body.append(arrow(482, 206, 524, 206))
    body.append(text(700, 180, "每一步都用同一組 9 個權重", 11.5, DIM))
    body.append(text(700, 202, "→ 參數量與影像大小無關", 11.5, DIM))

    body.append(rect(48, 396, 904, 96, stroke=BLUE + "55", fill="#1c2230", rx=12))
    body.append(text(68, 424, "特徵圖左上角那一格怎麼算出來？", 13.5, INK, "700"))
    body.append(text(68, 452,
                     "1×1 + 0×1 + 1×1  ＋  0×0 + 1×1 + 0×1  ＋  1×0 + 0×0 + 1×1  =  4",
                     13, AMBER, "700"))
    body.append(text(68, 476, "九組乘積全部相加 = 一格；換到下一個位置，同樣九個權重再算一次。",
                     12, DIM))
    body.append(text(48, 528, "輸出尺寸（不補邊、步幅 1）：(5 − 3) / 1 + 1 = 3 → 3×3", 12, DIM))
    return svg("conv", 1000, 560, "".join(body))



def fig_hyper():
    """Same input, same kernel, three padding/stride settings."""
    cards = [("不補邊（valid）", "(5 − 3) / 1 + 1 = 3", 3, TEAL, "邊角像素只被掃到 1 次"),
             ("補一圈邊（same）", "(5 + 2 − 3) / 1 + 1 = 5", 5, BLUE, "邊界用 0 補，輸出不縮小"),
             ("步幅 2（stride 2）", "(5 − 3) / 2 + 1 = 2", 2, AMBER, "一次跳 2 格，資訊少一半")]
    body = [text(40, 44, "同樣的輸入，換 padding 與 stride 就換輸出尺寸", 20, INK, "700"),
            text(40, 72, "唯一要記的公式：O = (N + 2P − F) / S + 1", 13, DIM)]
    for i, (name, formula, n_out, colour, note) in enumerate(cards):
        cx = 30 + i * 320
        body.append(rect(cx, 96, 300, 176, stroke=colour + "88", sw=1.5, fill=CELL,
                         opacity=0.9))
        body.append(text(cx + 16, 124, name, 12.5, colour, "700"))
        body.append(text(cx + 16, 148, formula, 11.5, DIM))
        body.append(empty_grid(cx + 16, 170, 12, 5, LINE))
        body.append(arrow(cx + 82, 200, cx + 108, 200, colour))
        oy = 200 - n_out * 12 / 2
        body.append(empty_grid(cx + 112, oy, 12, n_out, colour, 1.1, 1))
        body.append(text(cx + 182, 205, "輸出 %d×%d" % (n_out, n_out), 11.5, INK))
        body.append(text(cx + 16, 252, note, 10.5, DIM))
    body.append(text(30, 312, "N 輸入邊長、F 核邊長、P 補幾圈、S 步幅；除不盡就往下取整（floor）。",
                     12.5, DIM))
    return svg("hyper", 1000, 340, "".join(body))


def fig_multi():
    """One 5x5 input, three kernels, three maps, stacked into three channels."""
    rows = [("垂直邊緣", TEAL, [[-2, 0, 2], [-3, -2, 2], [-3, -1, 2]]),
            ("斜線", BLUE, [[0, 0, 0], [0, -1, 0], [-2, -1, 2]]),
            ("斑塊", VIOLET, [[2, 0, 2], [-2, 1, 0], [-2, 1, 2]])]
    body = [text(40, 44, "多個 filter：一層產生多張特徵圖", 20, INK, "700"),
            text(40, 72, "三個核心各自掃過同一張 5×5 影像，得到三張 3×3 特徵圖（三通道）",
                 13, DIM)]
    body.append(text(40, 136, "輸入 5×5×1", 12.5, INK, "700"))
    body.append(matrix_g(40, 150, 40, IMG5, 13, TEAL, ()))
    body.append(text(140, 366, "同一張影像", 11, DIM, "normal", "middle"))

    ys = [96, 200, 304]
    body.append('<line x1="268" y1="141" x2="268" y2="349" stroke="%s" stroke-width="1.4"/>'
                % LINE)
    body.append('<line x1="240" y1="250" x2="268" y2="250" stroke="%s" stroke-width="1.4"/>'
                % LINE)
    allc = [(r, c) for r in range(3) for c in range(3)]
    for i, (name, colour, fmap) in enumerate(rows):
        y = ys[i]
        body.append('<line x1="268" y1="%s" x2="294" y2="%s" stroke="%s" '
                    'stroke-width="1.4"/>' % (y + 45, y + 45, LINE))
        body.append(matrix_g(300, y, 30, KER, 11, colour, allc, base="#161b22"))
        body.append(arrow(394, y + 45, 418, y + 45))
        body.append(matrix_g(424, y, 30, fmap, 11, colour, ()))
        body.append(text(522, y + 49, name, 11.5, colour, "700"))
        body.append('<line x1="576" y1="%s" x2="588" y2="%s" stroke="%s" '
                    'stroke-width="1.2"/>' % (y + 45, y + 45, LINE))
    body.append('<line x1="588" y1="141" x2="588" y2="349" stroke="%s" stroke-width="1.4"/>'
                % LINE)
    body.append(arrow(588, 245, 628, 245))
    body.append(text(640, 158, "疊成 3 通道", 12, INK, "700"))
    for i in range(3):
        body.append(rect(640, 170 + i * 54, 150, 46, stroke=LINE, sw=1.2, fill=CELL,
                         rx=6, opacity=0.9))
        body.append(text(652, 170 + i * 54 + 28, "特徵圖 %d" % (i + 1), 11, DIM))
    body.append(text(40, 412, "下一層的核心會同時讀這 3 個通道 → C_in = 3；"
                              "參數量 (F·F·C_in + 1) · C_out。", 12, DIM))
    return svg("multi", 1000, 440, "".join(body))



def fig_relu():
    """Left: five numbers in and out. Right: the curve."""
    pairs = [("-3", "0", False), ("-1", "0", False), ("-0.25", "0", False),
             ("0.5", "0.5", True), ("2", "2", True)]
    body = [text(40, 44, "ReLU：把負的丟掉，正的放行", 20, INK, "700"),
            text(40, 72, "沒有這個非線性，疊再多層卷積仍然只等於一層線性變換", 13, DIM)]
    body.append(text(60, 108, "輸入 x", 11.5, DIM))
    body.append(text(206, 108, "輸出 max(0, x)", 11.5, DIM))
    for i, (vin, vout, keep) in enumerate(pairs):
        y = 140 + i * 30
        body.append(text(130, y, vin, 13, TEAL if keep else ROSE, "normal", "end"))
        body.append(text(168, y, "→", 13, DIM, "normal", "middle"))
        body.append(text(206, y, vout, 13, INK if keep else DIM,
                         "700" if keep else "normal"))
    body.append(text(60, 312, "負值一律變 0，正值原樣通過。", 11.5, DIM))

    # ---- curve: domain -4..4 -> x 380..860, y 0..4 -> 250..98
    px = lambda v: 620 + v * 60
    py = lambda v: 250 - v * 38
    body.append(text(380, 112, "折線圖：y = max(0, x)", 12.5, INK, "700"))
    body.append('<line x1="370" y1="250" x2="880" y2="250" stroke="%s" stroke-width="1"/>'
                % DIM)
    body.append('<line x1="620" y1="96" x2="620" y2="304" stroke="%s" stroke-width="1"/>'
                % DIM)
    body.append('<polyline points="%s,%s %s,%s %s,%s" fill="none" stroke="%s" '
                'stroke-width="2.6" stroke-linejoin="round"/>'
                % (px(-4), py(0), px(0), py(0), px(4), py(4), TEAL))
    for v in (-4, 0, 4):
        body.append(text(px(v), 270, str(v), 11, DIM, "normal", "middle"))
    for v in (2, 4):
        body.append(text(608, py(v) + 4, str(v), 11, DIM, "normal", "end"))
    body.append(text(876, 268, "x", 11.5, DIM, "normal", "end"))
    body.append(text(632, 92, "y", 11.5, DIM))
    body.append(text(470, 226, "負值區間全為 0", 11, ROSE))
    body.append(text(724, 150, "斜率 1", 11, TEAL))
    return svg("relu", 900, 340, "".join(body))


def fig_pool():
    """4x4 input, four 2x2 windows, max and average output."""
    m = [[1, 3, 2, 4],
         [5, 6, 7, 8],
         [3, 2, 1, 0],
         [1, 4, 9, 5]]
    quads = [(0, 0, TEAL), (0, 1, BLUE), (1, 0, VIOLET), (1, 1, AMBER)]
    maxes = [[6, 8], [4, 9]]
    avgs = [[3.75, 5.25], [2.5, 3.75]]
    allc = [(0, 0), (0, 1), (1, 0), (1, 1)]
    rings = [(1, 1), (3, 1), (1, 3), (2, 2)]      # global (col, row) of each window max
    body = [text(40, 44, "池化：把每個小區塊壓成一格", 20, INK, "700"),
            text(40, 72, "2×2 視窗、步幅 2：面積剩 1/4，而且沒有任何可訓練參數", 13, DIM)]
    body.append(text(60, 106, "輸入 4×4", 12.5, INK, "700"))
    for (r, c, colour) in quads:
        sub = [[m[r * 2][c * 2], m[r * 2][c * 2 + 1]],
               [m[r * 2 + 1][c * 2], m[r * 2 + 1][c * 2 + 1]]]
        body.append(matrix_g(60 + c * 104, 120 + r * 104, 52, sub, 14, colour, allc))
    for (col, row) in rings:
        body.append(rect(60 + col * 52, 120 + row * 52, 52, 52, stroke=INK, sw=1.8,
                         rx=3))
    body.append(arrow(276, 224, 340, 224))
    body.append(text(308, 202, "取最大", 11.5, DIM, "normal", "middle"))
    body.append(text(350, 152, "最大池化 2×2", 12, TEAL, "700"))
    body.append(matrix_g(350, 168, 56, maxes, 15, TEAL, ()))
    body.append(text(350, 300, "留最強響應", 11.5, DIM))
    body.append(text(530, 228, "或", 12, DIM, "normal", "middle"))
    body.append(text(600, 152, "平均池化 2×2", 12, BLUE, "700"))
    body.append(matrix_g(600, 168, 56, avgs, 12, BLUE, ()))
    body.append(text(600, 300, "留平均亮度", 11.5, DIM))
    body.append(text(40, 352, "最大池化保留紋理與邊緣，平均池化保留整體亮度；兩者都不從資料學東西。",
                     12, DIM))
    return svg("pool", 1000, 380, "".join(body))



def fig_head():
    """Flatten -> Dense -> softmax probabilities (numbers from verify_numbers.py)."""
    probs = [("狗", 0.9282), ("貓", 0.0511), ("鳥", 0.0208)]
    body = [text(40, 44, "分類頭：攤平 → 全連接 → softmax", 20, INK, "700"),
            text(40, 72, "前面抽到的特徵在這裡被壓成「每個類別一個分數」，再轉成機率", 13, DIM)]
    body.append(text(60, 136, "Flatten：7×7×16 = 784 維", 12, INK, "700"))
    for i in range(12):
        body.append(rect(60 + i * 20, 150, 18, 18, stroke=LINE, sw=1, fill=CELL, rx=3,
                         opacity=0.9))
    body.append(text(306, 165, "…", 14, DIM))
    body.append(arrow(322, 159, 352, 159))
    body.append(rect(356, 124, 110, 72, stroke=TEAL, sw=1.6, fill=CELL, rx=8))
    body.append(text(411, 154, "Dense 64", 12, INK, "700", "middle"))
    body.append(text(411, 174, "+ ReLU", 10.5, DIM, "normal", "middle"))
    body.append(arrow(472, 159, 502, 159))
    body.append(text(540, 112, "softmax → 每個類別的機率", 12, INK, "700"))
    for i, (name, p) in enumerate(probs):
        y = 150 + i * 36
        body.append(text(600, y + 5, name, 13, INK, "700", "end"))
        body.append(rect(612, y - 9, max(p * 280, 4), 20, stroke="none",
                         fill=TEAL if i == 0 else BLUE, rx=3, sw=1, opacity=0.9))
        body.append(text(620 + max(p * 280, 4), y + 5, "%.4f" % p, 12,
                         TEAL if i == 0 else DIM))
    body.append(text(612, 262, "0.9282 + 0.0511 + 0.0208 = 1.0000", 11.5, DIM))
    body.append(text(40, 320, "logits [4.2, 1.3, 0.4] 只是分數；softmax 才把它變成"
                                "加總為 1 的機率，預測結果取最大那一格。", 12, DIM))
    return svg("head", 1000, 360, "".join(body))


def fig_mnist():
    """Shape ladder for a small MNIST CNN."""
    chips = [("28×28×1", "輸入", TEAL), ("28×28×8", "卷積", TEAL),
             ("14×14×8", "池化", BLUE), ("14×14×16", "卷積", TEAL),
             ("7×7×16", "池化", BLUE), ("784 維", "攤平", AMBER),
             ("64 維", "全連接", AMBER), ("10 維", "softmax", ROSE)]
    ops = ["Conv", "Pool", "Conv", "Pool", "Flatten", "Dense", "Softmax"]
    w, gap, x0, y0, ch = 88, 30, 40, 104, 56
    body = [text(40, 44, "一個能跑 MNIST 的小 CNN", 20, INK, "700"),
            text(40, 72, "形狀一路變小、通道一路變多，最後交出 10 個數字", 13, DIM)]
    for i, (shape, role, colour) in enumerate(chips):
        x = x0 + i * (w + gap)
        body.append(rect(x, y0, w, ch, stroke=colour, sw=1.6, fill=CELL, rx=8,
                         opacity=0.9))
        body.append(text(x + w / 2, y0 + 34, shape, 11.5, INK, "700", "middle"))
        body.append(text(x + w / 2, y0 + 74, role, 10, DIM, "normal", "middle"))
        if i < len(ops):
            body.append(arrow(x + w + 3, y0 + ch / 2, x + w + gap - 5, y0 + ch / 2))
            body.append(text(x + w + gap / 2, 94, ops[i], 9.5, DIM, "normal", "middle"))
    body.append(text(40, 226, "卷積改通道數（filter 數量）、池化砍面積、Flatten 只攤平、"
                              "Dense 才做判斷。", 12, DIM))
    body.append(text(40, 250, "光第一層全連接（784 → 64）就有 50,240 個參數，"
                              "比兩個卷積層加起來的 1,248 個多 40 倍。", 12, DIM))
    return svg("mnist", 1000, 300, "".join(body))


def fig_concept_arch():
    """The classic 'conceptual architecture' picture: shrinking maps, then a head."""
    slabs = [("輸入", "224×224×3", 160, TEAL),
             ("Conv+ReLU", "112×112×64", 134, TEAL),
             ("Pool", "56×56×64", 110, BLUE),
             ("Conv+ReLU", "28×28×256", 86, TEAL),
             ("Pool", "14×14×256", 62, BLUE),
             ("Flatten", "25,088", 40, AMBER)]
    body = [text(40, 44, "概念架構：一路變小，最後才做決定", 20, INK, "700"),
            text(40, 72, "每個方塊的「高度」就是空間解析度；通道數正好相反，一路變多", 13, DIM)]
    base, x0, w, gap = 320, 50, 96, 32
    for i, (name, shape, h, colour) in enumerate(slabs):
        x = x0 + i * (w + gap)
        body.append(rect(x, base - h, w, h, stroke=colour + "aa", sw=1.4, fill=CELL,
                         rx=6, opacity=0.95))
        for k in range(1, 4):
            body.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
                        'stroke-width="0.7" opacity="0.35"/>'
                        % (x, base - h + k * h / 4, x + w, base - h + k * h / 4, colour))
        body.append(text(x + w / 2, base + 22, shape, 9.5, INK, "normal", "middle"))
        body.append(text(x + w / 2, base + 40, name, 9.5, DIM, "normal", "middle"))
        if i < len(slabs) - 1:
            body.append(arrow(x + w + 3, base - h / 2, x + w + gap - 5, base - h / 2))
    body.append('<line x1="78" y1="96" x2="640" y2="96" stroke="%s" stroke-width="1"/>'
                % TEAL)
    body.append(text(359, 88, "特徵抽取：Conv → ReLU → Pool（重複 N 次）", 11, TEAL, "700",
                     "middle"))
    body.append('<line x1="806" y1="96" x2="976" y2="96" stroke="%s" stroke-width="1"/>'
                % AMBER)
    body.append(text(891, 88, "決策", 11, AMBER, "700", "middle"))
    # head
    body.append(rect(806, 180, 170, 140, stroke=ROSE + "99", sw=1.4, fill=CELL, rx=10))
    body.append(text(822, 206, "Dense → softmax", 11, ROSE, "700"))
    for i, (name, p) in enumerate((("貓", 0.93), ("狗", 0.05), ("鳥", 0.02))):
        y = 226 + i * 26
        body.append(text(822, y + 10, name, 10, DIM))
        body.append(rect(846, y, max(p * 80, 3), 16, stroke="none", fill=ROSE, rx=3,
                         sw=1, opacity=0.8))
        body.append(text(852 + max(p * 80, 3), y + 11, "%.2f" % p, 9.5, DIM))
    body.append(arrow(790, 250, 802, 250))
    body.append(text(50, 386, "同一張圖，換掉最後那一段（決策頭）就是另一個任務——見下圖。", 12, DIM))
    return svg("concept-arch", 1000, 410, "".join(body))


def fig_tasks():
    panels = [("分類", "這張圖是什麼？", "一個標籤", "1 個類別機率", TEAL, "cell"),
              ("偵測", "物件在哪裡？", "框 + 類別", "K × (x, y, w, h, 類別)", AMBER, "box"),
              ("分割", "每個像素是什麼？", "逐像素遮罩", "H × W × 類別", VIOLET, "mask")]
    body = [text(40, 44, "同一張圖，三種答案", 20, INK, "700"),
            text(40, 72, "骨幹可以完全一樣；差別在「輸出頭」與「損失函數」", 13, DIM)]
    for i, (name, question, out, shape, colour, mode) in enumerate(panels):
        x = 30 + i * 318
        body.append(rect(x, 96, 300, 250, stroke=colour + "88", sw=1.4, fill=CELL,
                         rx=12, opacity=0.6))
        body.append(text(x + 16, 122, name, 13, colour, "700"))
        body.append(text(x + 66, 122, question, 10.5, DIM))
        gx, gy, cell = x + 20, 140, 26
        for r in range(6):
            for c in range(6):
                fill = CELL
                if mode == "mask" and (r in (2, 3) and c in (2, 3, 4)):
                    fill = VIOLET + "55"
                body.append(rect(gx + c * cell, gy + r * cell, cell, cell, stroke=LINE,
                                 sw=0.8, fill=fill, rx=2))
        if mode == "box":
            body.append(rect(gx + 1 * cell, gy + 1 * cell, 3 * cell, 3 * cell,
                             stroke=AMBER, sw=2, rx=2))
        body.append(arrow(gx + 6 * cell + 4, gy + 78, gx + 6 * cell + 34, gy + 78))
        body.append(text(x + 210, gy + 50, out, 10.5, INK, "700", "middle"))
        body.append(text(x + 210, gy + 72, "輸出", 9.5, DIM, "normal", "middle"))
        body.append(text(x + 210, gy + 92, shape, 9, colour, "normal", "middle"))
        body.append(text(x + 16, 288, "標籤" if mode == "cell" else
                         ("座標 + 標籤" if mode == "box" else "像素級標註"), 10, DIM))
        body.append(text(x + 16, 312, {"cell": "只看「有沒有」",
                                       "box": "還要「在哪裡」",
                                       "mask": "每個位置都要"}[mode], 10.5, colour))
    body.append(text(40, 384, "這也是為什麼分類可以用 GAP 收尾，而偵測／分割必須保留空間維度。",
                     12, DIM))
    return svg("tasks", 1000, 410, "".join(body))


FIGS = {"pipeline": fig_pipeline, "conv": fig_conv, "hyper": fig_hyper,
        "multi": fig_multi, "relu": fig_relu, "pool": fig_pool,
        "head": fig_head, "mnist": fig_mnist,
        "concept-arch": fig_concept_arch, "tasks": fig_tasks}


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug in FIGS:
        path = os.path.join(OUT, slug + ".svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(FIGS[slug]())
        print("wrote", path)
    print("\nCAPTIONS / ARIA ready for", len(CAPTIONS), "figures")


if __name__ == "__main__":
    main()
