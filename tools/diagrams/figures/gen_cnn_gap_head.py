# -*- coding: utf-8 -*-
"""cnn-gap-head: build the four figures for the GAP-vs-FC-head page."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cnn-gap-head")
sys.path.insert(0, HERE)

from gen_cnn_illustrated import (  # noqa: E402
    BG, CELL, INK, DIM, LINE, TEAL, BLUE, AMBER, ROSE, VIOLET,
    esc, text, rect, arrow, matrix_g, empty_grid)

DEFS = ('<defs><marker id="arg" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="%s"/></marker></defs>' % DIM)

ARIA = {
    "heads": "兩種分類頭：7×7×512 展平後接 1000 類全連接是 25,089,000 個參數；先做 GAP 壓成 512 再接 1000 類只要 513,000 個",
    "share": "分類頭占整個模型參數的比例：VGG16 89.4%、MobileNetV2 36.7%、ResNet-50 8.0%",
    "input-size": "輸入尺寸自由：7×7、8×8、14×14 三種特徵圖經過 GAP 都是 512 維，展平則變成 25088、32768、100352 維",
    "shift": "平移穩健性：同一張特徵圖橫移一格，GAP 的輸出完全不變（25.0），展平後 49 個位置全部改變",
    "gap-mechanics": "GAP 的機制：4×4 的通道 1 平均成 8.5，其餘通道各自平均，輸出 1×1×C；逐通道互不相干",
    "cam": "GAP 的權重就是 CAM 的權重：三個通道各乘上類別權重後相加成 5×5 熱圖，而它的空間平均剛好等於該類別的 logit",
    "vgg16": "VGG16 逐階段參數：五個卷積階段共 14,714,688（10.6%），三層全連接共 123,642,856（89.4%），總計 138,357,544",
}

CAPTIONS = {
    "heads": "同一張 7×7×512 特徵圖：展平再接 1000 類要 2,509 萬個參數；先 GAP 壓成 512 維再分類只要 51.3 萬——差 48.9 倍。",
    "share": "分類頭占模型總參數的比例。VGG16 有 89.4% 的參數在最後三層全連接；MobileNetV2 是 36.7%；ResNet-50 只剩 8.0%。",
    "input-size": "GAP 的輸出長度只取決於通道數，所以同一個分類頭可以吃不同大小的特徵圖；展平則會直接對不上。",
    "shift": "同一張特徵圖往右移一格：GAP 的輸出一個小數點都沒變，展平後的向量 49 個位置全部換了。",
    "gap-mechanics": "4×4 的通道平均成 8.5，512 個通道各做一次就是 512 維；GAP 沒有權重也沒有 bias。",
    "cam": "通道權重乘上特徵圖相加就是 CAM；而它的空間平均正好等於 GAP + Linear 算出的 logit。",
    "vgg16": "VGG16 的參數分佈：卷積骨幹只佔 10.6%，其餘 89.4% 都在最後三層全連接；光是 25,088 到 4,096 那層就 1.03 億。",
}


def svg(slug, w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'role="img" aria-label="%s">%s<rect x="0.75" y="0.75" width="%s" '
            'height="%s" rx="16" fill="%s" stroke="#222b36" stroke-width="1.5"/>%s</svg>'
            % (w, h, esc(ARIA[slug]), DEFS, w - 1.5, h - 1.5, BG, body))


def fig_heads():
    body = [text(40, 44, "兩種分類頭，差 48.9 倍", 20, INK, "700"),
            text(40, 72, "同樣從 7×7×512 的特徵圖出發，輸出 1000 類", 13, DIM)]

    def pipeline(x0, colour, label, names, note, total, tail):
        out = [rect(x0 - 20, 96, 460, 250, stroke=colour + "77", sw=1.4, fill=CELL,
                    rx=12, opacity=0.7),
               text(x0, 124, label, 12.5, colour, "700")]
        for k, (head, sub) in enumerate(names):
            x = x0 + k * 150
            out.append(rect(x, 150, 124, 56, stroke=colour + "aa", sw=1.4, fill=CELL,
                            rx=8))
            out.append(text(x + 62, 174, head, 11.5, INK, "700", "middle"))
            if sub:
                out.append(text(x + 62, 192, sub, 10, DIM, "normal", "middle"))
            if k < len(names) - 1:
                out.append(arrow(x + 127, 178, x + 147, 178))
        out.append(text(x0, 250, note, 11.5, DIM))
        out.append(text(x0, 276, total, 16, colour, "700"))
        out.append(text(x0, 310, tail, 10.5, DIM))
        return "".join(out)

    body.append(pipeline(50, ROSE, "舊寫法：Flatten + 大 FC",
                         [("7×7×512", ""), ("Flatten", "25,088 維"),
                          ("FC 1000", "")],
                         "參數：25,088 × 1000 + 1000", "= 25,089,000",
                         "權重集中在最沒有空間結構的那一層"))
    body.append(pipeline(530, TEAL, "新寫法：GAP + 小 FC",
                         [("7×7×512", ""), ("GAP", "512 維"), ("FC 1000", "")],
                         "參數：512 × 1000 + 1000", "= 513,000",
                         "GAP 自己 0 個參數，只做平均"))
    body.append(text(40, 384, "兩邊的輸出完全一樣（1000 個 logits），差別只在「先壓縮還是先展平」。",
                     12, DIM))
    return svg("heads", 1000, 410, "".join(body))


def fig_share():
    rows = [("VGG16", 89.4, 123642856, 138357544, ROSE),
            ("MobileNetV2", 36.7, 1281000, 3487816, AMBER),
            ("ResNet-50", 8.0, 2049000, 25557032, TEAL)]
    x0, x1 = 300, 820
    body = [text(40, 44, "分類頭占整個模型多少參數", 20, INK, "700"),
            text(40, 72, "同一件事在三種架構上的比例；括號是分類頭 / 全部參數", 13, DIM)]
    for i, (name, pct, head, total, colour) in enumerate(rows):
        y = 130 + i * 74
        body.append(text(280, y + 6, name, 12, INK, "normal", "end"))
        body.append(rect(x0, y - 14, max(pct / 100.0 * (x1 - x0), 4), 28, stroke="none",
                         fill=colour, rx=4, sw=1, opacity=0.85))
        body.append(text(x0 + max(pct / 100.0 * (x1 - x0), 4) + 10, y + 6,
                         "%.1f%%" % pct, 12.5, colour, "700"))
        body.append(text(280, y + 28, "({:,} / {:,})".format(head, total), 10, DIM,
                         "normal", "end"))
    body.append(text(40, 366, "VGG16 的 89.4% 幾乎都卡在 4096×4096 那兩層；"
                               "換成 GAP 頭之後，同一個骨幹的分類頭會掉到 1% 等級。", 12, DIM))
    return svg("share", 1000, 400, "".join(body))


def fig_input_size():
    body = [text(40, 44, "GAP 讓分類頭與輸入尺寸脫鉤", 20, INK, "700"),
            text(40, 72, "同樣的骨幹、同樣的分類頭，換一張大一點的特徵圖會怎樣", 13, DIM)]
    sizes = [("7×7×512", 110), ("8×8×512", 182), ("14×14×512", 254)]
    for k, (name, y) in enumerate(sizes):
        body.append(rect(50, y, 140, 52, stroke=TEAL + "aa", sw=1.4, fill=CELL, rx=8))
        body.append(text(120, y + 32, name, 11.5, INK, "700", "middle"))
        body.append(arrow(194, y + 26, 236, y + 26, TEAL))
        body.append(rect(240, y, 90, 52, stroke=TEAL, sw=1.4, fill=CELL, rx=7))
        body.append(text(285, y + 32, "GAP", 11.5, TEAL, "700", "middle"))
        body.append('<line x1="333" y1="%s" x2="392" y2="%s" stroke="%s" '
                    'stroke-width="1.2"/>' % (y + 26, y + 26, LINE))
    body.append('<line x1="392" y1="136" x2="392" y2="280" stroke="%s" stroke-width="1.2"/>'
                % LINE)
    body.append(arrow(392, 208, 432, 208, TEAL))
    body.append(rect(436, 148, 150, 120, stroke=TEAL, sw=1.6, fill=CELL, rx=9))
    body.append(text(511, 190, "512 維", 14, TEAL, "700", "middle"))
    body.append(text(511, 214, "三種尺寸", 10.5, DIM, "normal", "middle"))
    body.append(text(511, 236, "輸出完全相同", 10.5, DIM, "normal", "middle"))
    body.append(arrow(590, 208, 632, 208, TEAL))
    body.append(rect(636, 168, 210, 80, stroke=TEAL, sw=1.6, fill=CELL, rx=9))
    body.append(text(741, 198, "Linear(512 → 1000)", 12, INK, "700", "middle"))
    body.append(text(741, 222, "一個分類頭吃三種尺寸", 10, DIM, "normal", "middle"))
    body.append(rect(50, 296, 900, 84, stroke=ROSE + "77", sw=1.4, fill=CELL, rx=10))
    body.append(text(70, 322, "改成展平：25,088 / 32,768 / 100,352 —— 長度跟著尺寸變", 12,
                     ROSE, "700"))
    body.append(text(70, 348, "同一個 Linear(25,088 → 1000) 只能接第一種；換解析度就得換分類頭，"
                               "權重全部重來。", 11.5, DIM))
    body.append(text(40, 404, "GAP 的輸出長度只取決於通道數 C；展平的長度是 H×W×C。", 12, DIM))
    return svg("input-size", 1000, 420, "".join(body))


def fig_shift():
    m = [[1, 2, 3, 4, 5, 6, 7],
         [8, 9, 10, 11, 12, 13, 14],
         [15, 16, 17, 18, 19, 20, 21],
         [22, 23, 24, 25, 26, 27, 28],
         [29, 30, 31, 32, 33, 34, 35],
         [36, 37, 38, 39, 40, 41, 42],
         [43, 44, 45, 46, 47, 48, 49]]
    rolled = [row[-1:] + row[:-1] for row in m]
    body = [text(40, 44, "把特徵圖往右移一格，兩種頭的差別", 20, INK, "700"),
            text(40, 72, "同一組數字、同樣的通道；只差在「有沒有保留位置」", 13, DIM)]
    body.append(text(70, 108, "原始", 11.5, DIM))
    body.append(matrix_g(60, 120, 26, m, 9, TEAL, ()))
    body.append(text(330, 108, "右移一格", 11.5, DIM))
    body.append(matrix_g(320, 120, 26, rolled, 9, BLUE, ()))
    body.append(rect(560, 118, 400, 96, stroke=TEAL, sw=1.4, fill=CELL, rx=9))
    body.append(text(580, 146, "GAP：25.0 → 25.0", 12.5, TEAL, "700"))
    body.append(text(580, 172, "差 0.0（平均與位置無關）", 11, DIM))
    body.append(text(580, 196, "唯一不變的摘要", 10.5, DIM))
    body.append(rect(560, 236, 400, 96, stroke=ROSE, sw=1.4, fill=CELL, rx=9))
    body.append(text(580, 264, "Flatten：49 個位置全部改變", 12.5, ROSE, "700"))
    body.append(text(580, 290, "L2 距離 17.15；FC 必須重新學", 11, DIM))
    body.append(text(580, 314, "位移越多，權重越難學", 10.5, DIM))
    body.append(text(60, 330, "這就是「GAP 讓模型不必死記位置」的意思——", 12, DIM))
    body.append(text(60, 352, "它只問「這個通道整體有多強」。", 12, DIM))
    body.append(text(60, 386, "代價：需要精確位置的任務（偵測、分割）不能只用 GAP。", 12, DIM))
    return svg("shift", 1000, 410, "".join(body))


def fig_gap_mechanics():
    body = [text(40, 44, "GAP 就是每個通道各自取平均", 20, INK, "700"),
            text(40, 72, "H×W×C 的每一張特徵圖 → 一個數；通道數不變、寬高都變 1", 13, DIM)]
    body.append(text(60, 112, "通道 1（4×4）", 11.5, DIM))
    body.append(matrix_g(60, 124, 40, [[1, 2, 3, 4], [5, 6, 7, 8],
                                       [9, 10, 11, 12], [13, 14, 15, 16]], 11, TEAL, ()))
    body.append(text(60, 306, "平均 = 136 ÷ 16 = 8.5", 12, TEAL, "700"))
    body.append(text(60, 330, "其餘 511 個通道各做一次", 11, DIM))
    body.append(arrow(250, 210, 320, 210))
    body.append(text(285, 190, "GAP", 11.5, TEAL, "700", "middle"))
    body.append(text(285, 232, "0 參數", 10, DIM, "normal", "middle"))
    body.append(rect(330, 120, 210, 170, stroke=TEAL + "77", sw=1.4, fill=CELL, rx=10))
    body.append(text(435, 148, "1 × 1 × C", 12, INK, "700", "middle"))
    vals = [("8.50", TEAL), ("0.42", BLUE), ("0.11", VIOLET)]
    for i, (v, colour) in enumerate(vals):
        y = 166 + i * 36
        body.append(rect(370, y, 130, 30, stroke=colour + "aa", sw=1.2, fill=CELL, rx=5))
        body.append(text(435, y + 21, v, 12, colour, "700", "middle"))
    body.append(text(435, 282, "⋮（共 512 個）", 10, DIM, "normal", "middle"))
    body.append(rect(580, 120, 380, 170, stroke=BLUE + "55", fill="#1c2230", rx=12))
    body.append(text(600, 148, "逐通道、互不相干", 12, INK, "700"))
    body.append(text(600, 176, "第 c 個通道只看第 c 張圖：", 11.5, DIM))
    body.append(text(600, 200, "GAP_c = (1 / H·W) ΣΣ x[i, j, c]", 11.5, INK))
    body.append(text(600, 230, "實測：逐通道迴圈 = mean(dim=(1,2))", 11, DIM))
    body.append(text(600, 252, "若對整個張量取平均 → 只剩一個數，", 11, DIM))
    body.append(text(600, 272, "通道資訊就沒了", 11, DIM))
    body.append(text(40, 372, "這就是「H×W×C 壓成 C 維」的全部內容：C 次平均，沒有權重、沒有 bias。",
                     12, DIM))
    return svg("gap-mechanics", 1000, 400, "".join(body))


def fig_cam():
    W = [("0.9", TEAL), ("0.2", BLUE), ("−0.6", VIOLET)]
    body = [text(40, 44, "GAP 的權重，就是 CAM 的權重", 20, INK, "700"),
            text(40, 72, "分類頭的每一列 w[k] ，就是「類別 k 對每個通道的重視程度」", 13, DIM)]
    for i in range(3):
        y = 106 + i * 74
        body.append(text(60, y + 18, "通道 %d" % (i + 1), 10.5, DIM))
        body.append(empty_grid(60, y + 26, 18, 5, LINE, 0.7, 0.45))
        body.append(text(200, y + 70, "w = " + W[i][0], 11.5, W[i][1], "700"))
    body.append(arrow(270, 210, 330, 210))
    body.append(text(300, 190, "加權相加", 10.5, DIM, "normal", "middle"))
    body.append(rect(336, 120, 190, 168, stroke=AMBER + "88", sw=1.4, fill=CELL, rx=10))
    body.append(text(431, 148, "CAM（貓）", 12, INK, "700", "middle"))
    body.append(empty_grid(371, 162, 20, 5, AMBER, 0.8, 0.9))
    body.append(text(431, 274, "5×5 的類別熱圖", 10, DIM, "normal", "middle"))
    body.append(rect(560, 120, 400, 96, stroke=TEAL, sw=1.4, fill=CELL, rx=10))
    body.append(text(580, 148, "logit(貓) = Σ_c w_c × GAP(A_c)", 12, INK, "700"))
    body.append(text(580, 176, "= CAM(貓) 的空間平均", 12, TEAL, "700"))
    body.append(text(580, 200, "實測最大差 2.22e-16（浮點誤差）", 10.5, DIM))
    body.append(rect(560, 232, 400, 84, stroke=ROSE + "77", sw=1.4, fill=CELL, rx=10))
    body.append(text(580, 260, "反過來：把 CAM 放大回原圖尺寸，", 11.5, INK))
    body.append(text(580, 284, "就是「模型在看哪裡」的熱圖", 11.5, DIM))
    body.append(text(40, 356, "所以 GAP 不是把資訊丟掉而已：它讓「通道權重」直接變成可視化的空間權重。",
                     12, DIM))
    return svg("cam", 1000, 390, "".join(body))


def fig_vgg16():
    blocks = [("conv1 ×2", "112×112×64", "38,720", TEAL),
              ("conv2 ×2", "56×56×128", "221,440", TEAL),
              ("conv3 ×3", "28×28×256", "1,475,328", TEAL),
              ("conv4 ×3", "14×14×512", "5,899,776", TEAL),
              ("conv5 ×3", "7×7×512", "7,079,424", TEAL),
              ("FC 4096", "25,088→4,096", "102,764,544", ROSE),
              ("FC 4096", "4,096→4,096", "16,781,312", ROSE),
              ("FC 1000", "4,096→1,000", "4,097,000", ROSE)]
    body = [text(40, 44, "VGG16：89.4% 的參數都在最後三層", 20, INK, "700"),
            text(40, 72, "同一張 224×224×3 的圖；每塊下面的數字是那一階段的參數量", 13, DIM)]
    w, gap, x0, y0, bh = 108, 14, 22, 118, 88
    for i, (name, shape, params, colour) in enumerate(blocks):
        x = x0 + i * (w + gap)
        body.append(rect(x, y0, w, bh, stroke=colour + "aa", sw=1.5, fill=CELL, rx=8,
                         opacity=0.95))
        body.append(text(x + w / 2, y0 + 24, name, 10.5, colour, "700", "middle"))
        body.append(text(x + w / 2, y0 + 48, shape, 9.5, INK, "normal", "middle"))
        body.append(text(x + w / 2, y0 + 70, params, 9, DIM, "normal", "middle"))
        if i < len(blocks) - 1:
            body.append(arrow(x + w + 1, y0 + bh / 2, x + w + gap - 3, y0 + bh / 2))
    # brackets
    body.append('<line x1="22" y1="104" x2="618" y2="104" stroke="%s" stroke-width="1"/>'
                % TEAL)
    body.append(text(320, 96, "卷積骨幹 14,714,688（10.6%）", 11, TEAL, "700", "middle"))
    body.append('<line x1="646" y1="104" x2="976" y2="104" stroke="%s" stroke-width="1"/>'
                % ROSE)
    body.append(text(811, 96, "分類頭 123,642,856（89.4%）", 11, ROSE, "700", "middle"))
    # share bar
    body.append(rect(22, 254, 960, 30, stroke=LINE, sw=1, fill="#161b22", rx=4))
    body.append(rect(22, 254, 102, 30, stroke="none", fill=TEAL, rx=4, sw=1,
                     opacity=0.85))
    body.append(rect(124, 254, 858, 30, stroke="none", fill=ROSE, rx=4, sw=1,
                     opacity=0.85))
    body.append(text(73, 274, "10.6%", 11, "#08141a", "700", "middle"))
    body.append(text(553, 274, "89.4%（123,642,856）", 11, "#08141a", "700", "middle"))
    body.append(rect(22, 306, 960, 78, stroke=BLUE + "55", fill="#1c2230", rx=10))
    body.append(text(42, 334, "光是 25,088 → 4,096 那一層就 102,764,544 個參數", 12, INK))
    body.append(text(42, 360, "—— 比整個卷積骨幹（14,714,688）的 6.9 倍還多，"
                               "而且它丢掉所有空間結構。", 11.5, DIM))
    body.append(text(22, 416, "把這三層換成 GAP + Linear(512→1000)，"
                               "分類頭會從 1.24 億降到 51.3 萬。", 12, DIM))
    return svg("vgg16", 1000, 440, "".join(body))


FIGS = {"heads": fig_heads, "share": fig_share, "input-size": fig_input_size,
        "shift": fig_shift, "gap-mechanics": fig_gap_mechanics, "cam": fig_cam,
        "vgg16": fig_vgg16}


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


