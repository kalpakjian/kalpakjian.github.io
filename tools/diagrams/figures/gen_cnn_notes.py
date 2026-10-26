# -*- coding: utf-8 -*-
"""cnn-notes: the hand-drawn SVG figures for the CNN study notes.

Every number that appears inside a figure is COMPUTED here (convolution output,
parameter counts), never hand-copied from the course slides -- so a figure can
never drift away from the code printed in the notes.

  fig#1  S1.2  視覺皮層的分層抽象（LGN -> V1 -> V4 -> VTC）
  fig#2  S2.4  卷積：核心滑過影像 -> 特徵圖（逐元素相乘再相加）
  fig#3  S2.2  全連接 vs 卷積：參數量與空間資訊
  fig#4  S3.1  從零學特徵：低階 -> 中階 -> 高階的特徵階層
  fig#5  S3.4  LeNet-5 架構與輸出尺寸公式
  fig#6  S3.5  卷積的前向與反向傳播
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from svglib import Svg, C, MUT, TXT, CARD, CARD2, LINE    # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(_HERE, "cnn-notes")
RAIL = "#7d8590"

# ---------------------------------------------------------------- 計算（唯一真相）
KERNEL3 = [[1, 0, 1],
           [0, 1, 0],
           [1, 0, 1]]
IMAGE5 = [[1, 1, 1, 0, 0],
          [0, 1, 1, 1, 0],
          [0, 0, 1, 1, 1],
          [0, 0, 1, 1, 0],
          [0, 1, 1, 0, 0]]


def conv2d_valid(img, k):
    """Valid (no padding) 2-D convolution, returns the feature map."""
    R, Cc = len(img), len(img[0])
    kh, kw = len(k), len(k[0])
    out = []
    for r in range(R - kh + 1):
        row = []
        for c in range(Cc - kw + 1):
            row.append(sum(img[r + i][c + j] * k[i][j]
                           for i in range(kh) for j in range(kw)))
        out.append(row)
    return out


FEAT3 = conv2d_valid(IMAGE5, KERNEL3)

# 全連接 vs 卷積的參數量（圖 3）
FC_IN, FC_HID = 32 * 32, 120
FC_PARAMS = FC_IN * FC_HID + FC_HID          # 123,000
CONV_PARAMS = 5 * 5 * 1                       # 25
RATIO = FC_PARAMS // CONV_PARAMS              # 4,920

# LeNet-5 每一層（圖 5）
LENET = [
    ("Input",    "32×32×1",             "gray"),
    ("conv 5×5", "s=1 → 28×28×6",       "blue"),
    ("avg pool", "f=2, s=2 → 14×14×6",  "teal"),
    ("conv 5×5", "s=1 → 10×10×16",      "blue"),
    ("avg pool", "f=2, s=2 → 5×5×16",   "teal"),
]


# ---------------------------------------------------------------- 小工具
def matrix(s, x, y, cell, values, highlight=None, hl_colour=None, label=None,
           label_dy=-14, fill="#12181f", stroke=LINE):
    """畫一個數值矩陣；highlight = (row, col) 會用 hl_colour 框起來。"""
    rows, cols = len(values), len(values[0])
    for r in range(rows):
        for c in range(cols):
            v = values[r][c]
            on = (highlight == (r, c))
            s.rect(x + c * cell, y + r * cell, cell, cell,
                   fill=hl_colour if on else fill,
                   stroke=(C["amber"] if on else stroke) + "66",
                   rx=4, sw=2 if on else 1)
            s.text(x + c * cell + cell / 2, y + r * cell + cell * 0.66, str(v),
                   13.5, C["ink"] if on else TXT, "700" if on else "normal", "middle")
    if label:
        s.text(x, y + label_dy, label, 12.5, MUT)
    return (x + cols * cell, y + rows * cell)


# ---------------------------------------------------------------- 圖 1
def fig_cortex(s):
    s.text(48, 122, "越往深處 → 代表的概念越抽象", 13, MUT)
    cols = [
        ("LGN", "外側膝狀體", ["小點（small dots）", "亮度與對比的初步編碼"], "gray"),
        ("V1", "初級視覺皮層", ["方向（orientation）", "視差（disparity）", "部分顏色資訊"], "teal"),
        ("V4", "中級視覺皮層", ["顏色、基本形狀", "2D / 3D、深淺", "曲率（curvature）"], "blue"),
        ("VTC", "高階視覺皮層", ["複雜特徵", "臉部、物件、整體形狀"], "violet"),
    ]
    w, gap, top, h = 188, 20, 142, 196
    for i, (name, cn, lines, stage) in enumerate(cols):
        x = 48 + i * (w + gap)
        s.rect(x, top, w, h, fill=CARD2, stroke=C[stage] + "55", rx=12)
        s.badge(x + 30, top + 34, name, C[stage], r=22, size=14)
        s.text(x + 62, top + 30, cn, 13, TXT, "700")
        s.text(x + 62, top + 50, "層級 %d / 4" % (i + 1), 11, MUT)
        for j, ln in enumerate(lines):
            s.text(x + 18, top + 96 + j * 26, "· " + ln, 12.5, MUT)
        if i < len(cols) - 1:
            s.arrow(x + w + 2, top + h / 2, x + w + gap - 4, top + h / 2, RAIL)
    s.rect(48, 366, 804, 52, fill=CARD2, stroke=C["teal"] + "55", rx=10)
    s.text(68, 398, "複雜概念由簡單部分組成 —— 階層式抽象讓「邊緣」一步步長成「場景」",
           13.5, TXT)
    s.text(48, 442, "早期皮層的神經連線本身就編碼了視覺概念的基本元素；"
                    "同一套迴路被聽覺、嗅覺、味覺、觸覺重用。", 12.5, MUT)


# ---------------------------------------------------------------- 圖 2
def fig_conv(s):
    cell = 40
    ix, iy = 60, 168
    s.rect(ix, iy, cell * 3, cell * 3, fill=C["amber"] + "22", stroke=C["amber"] + "cc",
           rx=6, sw=2)
    matrix(s, ix, iy, cell, IMAGE5)
    s.rect(ix, iy, cell * 3, cell * 3, fill="none", stroke=C["amber"] + "cc",
           rx=6, sw=2.5)
    s.text(ix, iy - 16, "輸入影像 5×5", 13.5, TXT, "700")
    s.text(ix, iy + cell * 5 + 26, "框起來 = 核心要看的 3×3 區塊", 12, MUT)

    kx, ky = 372, 188
    matrix(s, kx, ky, cell, KERNEL3, fill=C["amber"] + "1a", stroke=C["amber"] + "66")
    s.text(kx, ky - 16, "濾鏡 / 核心 3×3", 13.5, C["amber"], "700")

    ox, oy = 690, 188
    matrix(s, ox, oy, cell, FEAT3, highlight=(0, 0), hl_colour=C["rose"] + "33")
    s.text(ox, oy - 16, "特徵圖 3×3", 13.5, TXT, "700")

    s.arrow(285, 250, 360, 250, RAIL)
    s.text(322, 236, "逐元素相乘", 12, MUT, "normal", "middle")
    s.arrow(500, 250, 678, 250, RAIL)
    s.text(589, 236, "全部相加 = 一格", 12, MUT, "normal", "middle")

    s.rect(48, 392, 804, 118, fill=CARD2, stroke=C["blue"] + "55", rx=12)
    s.text(68, 420, "特徵圖左上角那一格怎麼算出來？", 13.5, TXT, "700")
    s.text(68, 448, "(1×1 + 0×1 + 1×1) + (0×0 + 1×1 + 0×1) + (1×0 + 0×0 + 1×1) = 4",
           13.5, C["amber"], "700")
    s.text(68, 476, "同一組 9 個權重在每個位置重用 → 參數量與影像大小無關，"
                    "這正是卷積相對全連接最大的優勢。", 12.5, MUT)
    s.text(48, 534, "輸出尺寸（valid，stride=1）："
                    "(N − F) / stride + 1 = (5 − 3) / 1 + 1 = 3", 12.5, MUT)


# ---------------------------------------------------------------- 圖 3
def fig_fc_vs_conv(s):
    pw, ph, py = 390, 244, 118
    s.rect(48, py, pw, ph, fill=CARD2, stroke=C["rose"] + "55", rx=12)
    s.text(68, 148, "全連接神經網路", 15.5, C["rose"], "700")
    s.text(68, 172, "每個隱藏單元都連到全部輸入", 12.5, MUT)
    cols = [(100, "輸入"), (195, "隱藏"), (290, "輸出")]
    ys_in = [212, 238, 264, 290]
    ys_out = [225, 251, 277]
    for x, lab in cols:
        s.text(x, 190, lab, 11, MUT, "normal", "middle")
    for y1 in ys_in:
        for y2 in ys_in:
            s.line(108, y1, 187, y2, "#3a4450", 1)
    for y1 in ys_in:
        for y2 in ys_out:
            s.line(203, y1, 282, y2, "#3a4450", 1)
    for x, ys in ((100, ys_in), (195, ys_in), (290, ys_out)):
        for cy in ys:
            s.p.append('<circle cx="%s" cy="%s" r="8" fill="%s" stroke="%s66" '
                       'stroke-width="1.5"/>' % (x, cy, C["rose"], C["rose"]))
    s.text(68, 318, "權重數 = 1024 × 120 + 120", 13, TXT, "700")
    s.text(68, 340, "= %s 個" % format(FC_PARAMS, ","), 13, C["rose"], "700")

    s.rect(462, py, pw, ph, fill=CARD2, stroke=C["teal"] + "55", rx=12)
    s.text(482, 148, "卷積層", 15.5, C["teal"], "700")
    s.text(482, 172, "同一組權重滑過整張圖", 12.5, MUT)
    s.text(564, 190, "4×4 影像", 11, MUT, "normal", "middle")
    for r in range(4):
        for c in range(4):
            s.rect(520 + c * 22, 206 + r * 22, 22, 22, fill="#12181f",
                   stroke=RAIL, rx=3, sw=1)
    s.rect(520, 206, 66, 66, fill=C["teal"] + "22", stroke=C["teal"] + "cc", rx=4, sw=2)
    s.arrow(618, 250, 676, 250, RAIL)
    s.rect(686, 206, 88, 88, fill=CARD, stroke=C["teal"] + "66", rx=8)
    s.text(730, 255, "特徵圖", 13, TXT, "700", "middle")
    s.text(482, 318, "權重數 = 5 × 5 × 1", 13, TXT, "700")
    s.text(482, 340, "= %d 個" % CONV_PARAMS, 13, C["teal"], "700")

    s.rect(48, 382, 804, 58, fill=CARD2, stroke=C["amber"] + "55", rx=10)
    s.text(68, 408, "同樣的輸入、同一層的容量：%s 個權重 vs %d 個權重 → 相差 %s 倍"
           % (format(FC_PARAMS, ","), CONV_PARAMS, format(RATIO, ",")), 13.5, TXT, "700")
    s.text(68, 430, "而且全連接沒有「哪裡」的概念 —— 捲平後的像素向量丟掉了空間資訊。",
           12.5, MUT)


# ---------------------------------------------------------------- 圖 4
def fig_hierarchy(s):
    panels = [
        ("低階特徵", "Low level", ["邊緣、暗點", "edges, dark spots"], "teal"),
        ("中階特徵", "Mid level", ["眼睛、耳朵、鼻子", "eyes, ears, nose"], "blue"),
        ("高階特徵", "High level", ["面部結構", "facial structure"], "violet"),
    ]
    w, gap, top, h = 260, 32, 132, 250
    for i, (name, en, lines, stage) in enumerate(panels):
        x = 48 + i * (w + gap)
        s.rect(x, top, w, h, fill=CARD2, stroke=C[stage] + "55", rx=12)
        s.text(x + 18, top + 30, name, 15, C[stage], "700")
        s.text(x + 18, top + 52, en, 11.5, MUT)
        gx, gy, c = x + 70, top + 66, 30
        for r in range(4):
            for cc in range(4):
                dark = (r * 4 + cc + i * 3) % 3 != 0
                s.rect(gx + cc * c, gy + r * c, c, c,
                       fill=("#0d1117" if dark else "#8b949e"),
                       stroke=RAIL, rx=2, sw=0.6)
        s.text(x + 18, top + 212, lines[0], 13, TXT, "700")
        s.text(x + 18, top + 236, lines[1], 12, MUT)
    s.arrow(48, 414, 852, 414, C["amber"], 2)
    s.text(48, 406, "抽象程度 ↑　特徵由影像自己學出來，不是人手工設計的",
           13, C["amber"], "700")
    s.text(48, 438, "以上三層特徵皆由同一組卷積權重自動學得 —— "
                    "這就是「de novo（從零學起）」的關鍵。", 12.5, MUT)

# ---------------------------------------------------------------- 圖 5
def fig_lenet(s):
    w, gap, top, h = 142, 20, 126, 78
    for i, (label, sub, stage) in enumerate(LENET):
        x = 48 + i * (w + gap)
        s.box(x, top, w, h, label, sub, stage, tsize=14.5, dsize=11)
        if i < len(LENET) - 1:
            s.arrow(x + w + 4, top + h / 2, x + w + gap - 6, top + h / 2, RAIL)
    top2 = 288
    tail = [("FC", "120 個單元", "amber"), ("FC", "84 個單元", "amber"),
            ("Output", "10 類（0–9）", "green")]
    for i, (label, sub, stage) in enumerate(tail):
        x = 48 + i * 172
        s.box(x, top2, 150, h, label, sub, stage, tsize=14.5, dsize=11)
        if i < len(tail) - 1:
            s.arrow(x + 154, top2 + h / 2, x + 168, top2 + h / 2, RAIL)
    last_x = 48 + (len(LENET) - 1) * (w + gap) + w / 2
    s.line(last_x, top + h, last_x, 252, RAIL)
    s.line(last_x, 252, 123, 252, RAIL)
    s.arrow(123, 252, 123, top2 - 4, RAIL)
    s.rect(596, top2 - 10, 256, 96, fill=CARD2, stroke=C["blue"] + "55", rx=10)
    s.text(616, top2 + 14, "輸出尺寸公式", 13, C["blue"], "700")
    s.text(616, top2 + 40, "O = (N + 2P − F) / stride + 1", 14, TXT, "700")
    s.text(616, top2 + 62, "N 輸入尺寸｜P 填補｜F 核心大小", 11, MUT)
    s.text(48, 416, "整體結構：conv → pool → conv → pool → FC → FC → output；"
                    "越深層 H（高）↓、W（寬）↓、C（通道）↑。", 12.5, MUT)
    s.text(48, 440, "LeNet-5 全網只有約 6 萬個參數（60K），"
                    "早期就能在手寫數字上訓練成功。", 12.5, MUT)


# ---------------------------------------------------------------- 圖 6
def fig_backprop(s):
    X = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    F = [[1, 0], [0, 1]]
    O = [[1 + 5, 2 + 6], [4 + 8, 5 + 9]]
    dO = [[1, 0], [0, 1]]
    dF = [[1 * 1 + 2 * 1 + 4 * 1 + 5 * 1, 2 * 1 + 3 * 1 + 5 * 1 + 6 * 1],
          [4 * 1 + 5 * 1 + 7 * 1 + 8 * 1, 5 * 1 + 6 * 1 + 8 * 1 + 9 * 1]]

    s.rect(48, 104, 804, 190, fill=CARD2, stroke=C["blue"] + "55", rx=12)
    s.text(68, 132, "前向傳播：O = Convolution(X, F)", 14, C["blue"], "700")
    matrix(s, 80, 158, 32, X, label="X（輸入 3×3）", label_dy=114)
    matrix(s, 284, 174, 32, F, label="F（核心 2×2）", label_dy=82)
    matrix(s, 644, 174, 32, O, label="O（輸出 2×2）", label_dy=82)
    s.arrow(184, 206, 276, 206, RAIL)
    s.arrow(356, 206, 636, 206, RAIL)
    s.text(496, 194, "把 X 與 F 逐元素相乘後相加", 12, MUT, "normal", "middle")

    s.rect(48, 316, 804, 190, fill=CARD2, stroke=C["rose"] + "55", rx=12)
    s.text(68, 344, "反向傳播：∂E/∂F = Convolution(X, ∂E/∂O)", 14, C["rose"], "700")
    matrix(s, 80, 370, 32, X, label="X（輸入 3×3）", label_dy=114)
    matrix(s, 284, 386, 32, dO, label="∂E/∂O（梯度 2×2）", label_dy=82)
    matrix(s, 644, 386, 32, dF, label="∂E/∂F（權重梯度 2×2）", label_dy=82)
    s.arrow(184, 418, 276, 418, RAIL)
    s.arrow(356, 418, 636, 418, RAIL)
    s.text(496, 406, "同一個卷積運算，換成「梯度」當角色", 12, MUT, "normal", "middle")

    s.text(48, 532, "重點：卷積層的反向傳播用的還是卷積 —— "
                    "把「對輸入的梯度」當成輸入、把「對權重的梯度」當成輸出。", 12.5, MUT)

FIGS = [
    ("cnn-cortex-layers", "cnn-notes", 1, 900, 460,
     "視覺皮層的分層抽象", "LGN → V1 → V4 → VTC：越深越抽象", fig_cortex,
     "圖 1：視覺皮層的四個層級。LGN 只看小點，V1 處理方向與視差，"
     "V4 處理顏色與基本形狀，VTC 處理複雜特徵——"
     "「複雜概念由簡單部分組成」的階層式抽象。｜手繪 SVG 圖表"),
    ("cnn-conv-sliding", "cnn-notes", 2, 900, 552,
     "卷積：核心滑過影像", "逐元素相乘再相加，產生特徵圖", fig_conv,
     "圖 2：3×3 核心在 5×5 影像上滑動。左上角那一格示範了完整的計算："
     "九組乘積相加得到 4。同一組權重在每個位置重用。｜手繪 SVG 圖表"),
    ("cnn-fc-vs-conv", "cnn-notes", 3, 900, 460,
     "全連接 vs 卷積", "參數量與空間資訊的差距", fig_fc_vs_conv,
     "圖 3：同一個 32×32 灰階影像接一層 120 個單元，"
     "全連接要 %s 個權重，卷積只要 %d 個，相差 %s 倍；"
     "而且全連接會丟掉空間資訊。｜手繪 SVG 圖表"
     % (format(FC_PARAMS, ","), CONV_PARAMS, format(RATIO, ","))),
    ("cnn-feature-hierarchy", "cnn-notes", 4, 900, 456,
     "從零學特徵：特徵階層", "低階 → 中階 → 高階，全部由卷積權重自動學得", fig_hierarchy,
     "圖 4：低階特徵是邊緣與暗點，中階是眼睛、耳朵、鼻子，"
     "高階是面部結構——這一層層的特徵不是人手寫的，"
     "而是模型直接從資料裡學出來的。｜手繪 SVG 圖表"),
    ("cnn-lenet5", "cnn-notes", 5, 900, 458,
     "LeNet-5 架構", "conv → pool → conv → pool → FC → FC → output", fig_lenet,
     "圖 5：LeNet-5 的每一層與張量尺寸。"
     "輸出尺寸一律套用 O = (N + 2P − F) / stride + 1。"
     "全網約 6 萬個參數。｜手繪 SVG 圖表"),
    ("cnn-backprop-conv", "cnn-notes", 6, 900, 552,
     "卷積的前向與反向傳播", "反向用的仍然是卷積，只是換了角色", fig_backprop,
     "圖 6：前向用 X 與 F 卷積得到 O；反向則把「對輸出的梯度」"
     "與 X 卷積，得到「對權重的梯度」。｜手繪 SVG 圖表"),
]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for slug, note, art, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        bad = s.check()
        s.save(os.path.join(OUT, slug + ".svg"),
               os.path.join(OUT, "_m_" + slug + ".html"))
        print("wrote %-30s %-12s art#%d %dx%d  %s"
              % (slug + ".svg", note, art, w, h,
                 "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))
    print("\ncomputed: FEAT3 = %s" % FEAT3)
    print("computed: FC_PARAMS = %d, CONV_PARAMS = %d, RATIO = %d"
          % (FC_PARAMS, CONV_PARAMS, RATIO))
