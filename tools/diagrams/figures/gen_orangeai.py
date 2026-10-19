# -*- coding: utf-8 -*-
"""orange-ai-notes: 13 ASCII blocks -> SVG.

  art#1  §2.4  特徵 X 與目標 y（什麼是「標記」）
  art#2  §3.3  決策樹對切點有多敏感（2.45 vs 2.50）
  art#3  §4.1  準確度 vs 可解釋性（本機實測 CA）
  art#4  §4.3  選模型的四組問答（決策流程）
  art#5  §5.1  SVM 在最大化什麼（間隔 / 支持向量）
  art#6  §5.3  sigmoid 函數與 S 形曲線
  art#7  §6.1  貝氏定理與「樸素」兩個字
  art#8  §8.4  Constant 元件的工作流
  art#9  §9.1  Stacking 的兩層架構
  art#10 §10.2 Load Model 的四個步驟
  art#11 §10.3 Save / Load 的完整閉環（訓練 vs 推論）
  art#12 §11.3 四個元件串成一條完整流程（考試畫圖題）
  art#13 §12.4 Orange 與 TPOT 的先後關係
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from svglib import Svg, C, MUT, TXT, CARD2, MONO  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAIL = "#7d8590"
DASH = "#30363d"


def dot(s, x, y, colour, r=7, square=False):
    if square:
        s.p.append('<rect x="%s" y="%s" width="%s" height="%s" rx="2" fill="%s"/>'
                   % (x - r, y - r, 2 * r, 2 * r, colour))
    else:
        s.p.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (x, y, r, colour))


def dashed(s, x1, y1, x2, y2, colour=RAIL):
    s.p.append('<path d="M %s %s L %s %s" stroke="%s" stroke-width="1.5" '
               'stroke-dasharray="7 6" fill="none"/>' % (x1, y1, x2, y2, colour))


def table(s, x, y, col_ws, headers, rows, hh=42, rh=38, stage="teal"):
    w, h = sum(col_ws), hh + rh * len(rows)
    s.rect(x, y, w, h, fill="#0d1117", stroke=C[stage] + "66", rx=10)
    s.line(x, y + hh, x + w, y + hh, C[stage] + "66", 1.5)
    cx = x
    for cw in col_ws[:-1]:
        cx += cw
        s.line(cx, y, cx, y + h, DASH, 1)
    for i in range(1, len(rows)):
        s.line(x, y + hh + i * rh, x + w, y + hh + i * rh, DASH, 1)
    cx = x
    for cw, hd in zip(col_ws, headers):
        s.text(cx + cw / 2, y + hh / 2 + 5, hd, 12.5, C[stage], "700", "middle")
        cx += cw
    for r, row in enumerate(rows):
        cx = x
        for cw, cell in zip(col_ws, row):
            s.text(cx + cw / 2, y + hh + r * rh + rh / 2 + 5, cell, 12, TXT,
                   "normal", "middle")
            cx += cw


def outline_panel(s, x, y, w, h, root, rows, pitch=36, top=84):
    """Bordered panel: root line + a rail/indent tree supporting 3 levels."""
    s.rect(x, y, w, h, fill=CARD2, stroke="#2a6f68", rx=14)
    s.text(x + 28, y + 42, root, 18, TXT, "700")
    rail, sub, sub2 = x + 52, x + 108, x + 164
    ys = [y + top + i * pitch for i in range(len(rows))]
    s.line(rail, ys[0] - 6, rail, ys[-1] - 6, DASH, 1.5)
    for i, (lvl, txt, stage) in enumerate(rows):
        sy = ys[i] - 6
        if lvl == 0:
            s.line(rail, sy, rail + 14, sy, DASH, 1.5)
            s.text(rail + 20, ys[i], txt, 13.5, C[stage] if stage else TXT, "700")
        elif lvl == 1:
            s.line(sub, ys[i - 1] - 6 + 10, sub, sy, DASH, 1.5)
            s.line(sub, sy, sub + 14, sy, DASH, 1.5)
            s.text(sub + 20, ys[i], txt, 12.5, TXT)
        else:
            s.line(sub2, ys[i - 1] - 6 + 10, sub2, sy, DASH, 1.5)
            s.line(sub2, sy, sub2 + 14, sy, DASH, 1.5)
            s.text(sub2 + 20, ys[i], txt, 12, MUT)


def fig_xy(s):
    s.text(255, 150, "特徵（features / independent variables）", 13, MUT, "700", "middle")
    table(s, 90, 170, [110, 110, 110], ["花萼長", "花萼寬", "花瓣長"],
          [["5.1", "3.5", "1.4"], ["7.0", "3.2", "4.7"]], stage="teal")
    s.text(430, 226, "…", 18, MUT, "700", "middle")
    s.text(660, 150, "目標（target）", 13, MUT, "700", "middle")
    table(s, 560, 170, [200], ["品種"], [["setosa"], ["versicolor"]], stage="amber")
    s.text(775, 245, "← 這就是「標記」", 12, C["amber"], "700")
    s.text(255, 340, "（X：模型看得到的）", 12.5, MUT, "normal", "middle")
    s.text(660, 340, "（y：模型要學著猜的）", 12.5, MUT, "normal", "middle")
    s.text(48, 400, "有標記＝每一列都有正確答案（y），模型才有東西可以學；"
                    "這跟「監督／非監督」是同一件事的兩種說法。", 13, MUT)


def fig_tree_sensitive(s):
    for x0, cut, leaves in ((60, "2.45", True), (490, "2.50", False)):
        s.rect(x0, 150, 320, 48, fill=CARD2, stroke=C["teal"] + "66", rx=10)
        s.text(x0 + 160, 180, "petal length ≤ %s ?" % cut, 14, TXT, "700", "middle")
        if leaves:
            s.box(x0 + 10, 250, 130, 44, "setosa", None, "green", tsize=13)
            s.box(x0 + 170, 250, 150, 56, "petal width ≤ 1.75 ?", None, "blue", tsize=11.5)
            s.bus_out((x0 + 160, 198), [(x0 + 75, 250), (x0 + 245, 250)])
            s.text(x0 + 80, 218, "是", 11.5, C["green"], "700")
            s.text(x0 + 250, 218, "否", 11.5, C["blue"], "700")
            s.bus_out((x0 + 245, 306), [(x0 + 175, 360), (x0 + 315, 360)])
            s.text(x0 + 180, 328, "是", 11.5, MUT)
            s.text(x0 + 320, 328, "否", 11.5, MUT)
            s.box(x0 + 110, 360, 130, 44, "versicolor", None, "violet", tsize=12)
            s.box(x0 + 250, 360, 130, 44, "virginica", None, "rose", tsize=12)
        else:
            s.box(x0 + 10, 250, 130, 44, "setosa", None, "green", tsize=13)
            s.box(x0 + 170, 250, 130, 44, "…", None, "gray", tsize=13)
            s.bus_out((x0 + 160, 198), [(x0 + 75, 250), (x0 + 235, 250)])
            s.text(x0 + 80, 218, "是", 11.5, C["green"], "700")
            s.text(x0 + 240, 218, "否", 11.5, MUT, "700")
    s.text(48, 450, "換一個切點（2.45 → 2.50）整棵樹就長得不一樣——這就是「高變異數」，"
                    "也是隨機森林要存在的原因。", 13, MUT)



ACCURACY = [
    (175, [("kNN (0.9667)", 250), ("邏輯迴歸 (0.9667)", 520), ("Stacking (0.9667)", 790)]),
    (233, [("SVM (0.9600)", 250), ("AdaBoost (0.9600)", 520), ("Calibrated (0.9600)", 790)]),
    (291, [("梯度提升 (0.9533)", 385), ("神經網路 (0.9533)", 650)]),
    (349, [("隨機森林 (0.9467)", 385), ("決策樹 (0.9467)", 790)]),
    (407, [("CN2 規則 (0.8933)", 790)]),
    (465, [("樸素貝氏 (0.8733)", 650)]),
    (523, [("SGD (0.8333)", 520)]),
]

Q4 = [
    (0, "是　→　需要「文字規則」嗎？", "teal"),
    (1, "是　→　CN2 規則歸納", None),
    (1, "否　→　決策樹（還能看圖）", None),
    (0, "否　→　資料量大嗎？", "blue"),
    (1, "小（< 幾千筆）→　kNN 或 決策樹", None),
    (1, "大　→　在乎準確度？", None),
    (2, "是　→　隨機森林（快一點）或 梯度提升（準一點）", None),
    (2, "否　→　邏輯迴歸（快、穩、可解釋）", None),
]


def fig_accuracy(s):
    s.text(48, 128, "準確度（CA，本機實測）", 13, MUT, "700")
    s.arrow(150, 220, 150, 156, RAIL)
    s.text(140, 180, "高", 12.5, MUT, "normal", "end")
    s.text(140, 550, "低", 12.5, MUT, "normal", "end")
    s.arrow(150, 560, 866, 560, RAIL)
    s.text(170, 586, "低", 12.5, MUT)
    s.text(846, 586, "高", 12.5, MUT, "normal", "end")
    s.text(866, 610, "可解釋性", 13, MUT, "700", "end")
    for y, items in ACCURACY:
        for label, x in items:
            dot(s, x, y, C["blue"])
            s.text(x, y - 13, label, 12, TXT, "normal", "middle")
    s.text(48, 634, "左邊＝黑箱、右邊＝白箱：（神經網路／SVM／隨機森林）在左，"
                    "（CN2 規則／決策樹／計分表）在右。", 13, MUT)


def fig_q4(s):
    outline_panel(s, 48, 106, 904, 362, "需要能解釋？", Q4)
    s.text(48, 508, "兩條規則會重疊：資料量小與資源有限時，課程都推 kNN 與 CN2——"
                    "但實測的 SGD 只有 0.8333，輕量不等於準。", 13, MUT)


def fig_svm(s):
    for x, y in ((180, 150), (250, 138), (320, 152), (400, 140), (470, 152)):
        dot(s, x, y, C["teal"])
    for x, y in ((200, 350), (270, 362), (340, 348), (420, 360), (490, 348)):
        dot(s, x, y, C["rose"], square=True)
    dot(s, 260, 205, C["teal"], r=10)
    dot(s, 400, 205, C["teal"], r=10)
    dot(s, 300, 295, C["rose"], r=10, square=True)
    dot(s, 440, 295, C["rose"], r=10, square=True)

    dashed(s, 100, 205, 640, 205)
    dashed(s, 100, 295, 640, 295)
    s.line(100, 250, 640, 250, TXT, 2.5)
    s.text(660, 209, "← 間隔上緣（margin）", 12, MUT)
    s.text(660, 255, "← 決策邊界（超平面）", 12, TXT, "700")
    s.text(660, 299, "← 間隔下緣", 12, MUT)
    s.text(660, 340, "SVM 要讓上下兩條虛線", 12, MUT)
    s.text(660, 360, "之間的距離最大化", 12, MUT)
    s.text(48, 400, "● 類別 A　　■ 類別 B　　— 決策邊界　　- - 間隔（margin）"
                    "　　◎ 支持向量（離邊界最近的點）", 12.5, MUT)
    s.text(48, 434, "真正決定這條線的只有支持向量——其他點移開一點都不影響結果。", 13, MUT)


def fig_sigmoid(s):
    s.text(80, 200, "σ(z)  =", 17, TXT, "700", "start", MONO)
    s.text(300, 178, "1", 15, TXT, "normal", "middle", MONO)
    s.line(250, 192, 350, 192, TXT, 1.5)
    s.text(300, 222, "1 + e^(−z)", 15, TXT, "normal", "middle", MONO)
    s.text(80, 270, "z = w₀ + w₁x₁ + … + wₚxₚ", 14, MUT, "normal", "start", MONO)

    x0, x1, y0, y1 = 520, 866, 200, 400
    pts = []
    for i in range(121):
        z = -6 + 12 * i / 120.0
        sig = 1 / (1 + pow(2.718281828, -z))
        pts.append("%.1f,%.1f" % (x0 + (x1 - x0) * i / 120.0, y1 - (y1 - y0) * sig))
    s.p.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.5"/>'
               % (" ".join(pts), C["blue"]))
    s.arrow(520, 400, 520, 196, RAIL)
    s.arrow(520, 400, 872, 400, RAIL)
    for val, y in (("1.0", 204), ("0.5", 300), ("0.0", 396)):
        s.text(510, y + 5, val, 12, MUT, "normal", "end")
    s.text(540, 424, "負很多（機率→0）", 11.5, MUT)
    s.text(690, 424, "0", 11.5, MUT, "normal", "middle")
    s.text(830, 424, "正很多（機率→1）", 11.5, MUT, "normal", "middle")
    dashed(s, 520, 300, 690, 300)
    s.text(540, 322, "z = 0 → 機率 0.5", 11.5, C["blue"], "700")
    s.text(48, 490, "S 形曲線把任意實數壓到 0～1 之間；z = 0 時機率正好 0.5，"
                    "那就是分類門檻。", 13, MUT)


def fig_bayes(s):
    s.text(100, 210, "P(A | B)  =", 17, TXT, "700", "start", MONO)
    s.text(420, 182, "P(B | A) · P(A)", 15, TXT, "normal", "middle", MONO)
    s.line(340, 196, 500, 196, TXT, 1.5)
    s.text(420, 228, "P(B)", 15, TXT, "normal", "middle", MONO)

    s.text(100, 300, "換成分類的語言：", 13.5, MUT, "700")
    s.text(100, 348, "P(類別 | 特徵)", 16, TXT, "700", "start", MONO)
    s.text(300, 348, "∝", 16, TXT, "700", "start", MONO)
    s.text(336, 348, "P(類別)", 16, TXT, "700", "start", MONO)
    s.text(452, 348, "×", 16, TXT, "700", "start", MONO)
    s.text(488, 348, "Π P(特徵ᵢ | 類別)", 16, TXT, "700", "start", MONO)

    for cx, label in ((203, "後驗機率"), (376, "先驗機率"),
                      (640, "似然（每個特徵各自算，然後相乘）")):
        s.arrow(cx, 372, cx, 356, RAIL)
        s.text(cx, 394, label, 12, MUT, "normal", "middle")
    s.text(48, 440, "「樸素」＝假設每個特徵彼此獨立，所以可以把所有似然直接相乘。", 13, MUT)



def fig_constant(s):
    s.box(60, 180, 180, 70, "File", "（資料集）", "teal", tsize=14)
    s.arrow(244, 215, 296, 215)
    s.text(271, 205, "拖入資料集", 11.5, MUT, "normal", "middle")
    s.box(300, 180, 180, 70, "Constant", "（基準）", "amber", tsize=14)
    s.arrow(484, 215, 536, 215)
    s.text(511, 205, "連接", 11.5, MUT, "normal", "middle")
    s.box(540, 180, 200, 70, "Test and Score", None, "blue", tsize=14)
    s.line(390, 250, 390, 310, RAIL, 2)
    s.arrow(390, 310, 536, 310)
    s.box(540, 280, 200, 60, "Predictions", None, "green", tsize=14)
    s.text(752, 219, "← 先量基準線", 12, C["blue"], "700")
    s.text(752, 315, "← 查看預測結果", 12, C["green"], "700")
    s.text(48, 400, "Constant 是最笨的模型（永遠猜最常見的類別）——用它當基準線，"
                    "才知道其他模型有沒有真的學到東西。", 13, MUT)


def fig_stacking(s):
    s.box(48, 254, 140, 56, "原始資料 X", None, "teal", tsize=13.5)
    s.line(188, 282, 206, 282, RAIL, 2)
    s.line(206, 182, 206, 382, RAIL, 2)
    names = [("基礎學習器 1", "Logistic"), ("基礎學習器 2", "RandomForest"),
             ("基礎學習器 3", "SVM")]
    for i, (t, d) in enumerate(names):
        y = 150 + i * 100
        s.arrow(206, y + 32, 228, y + 32, RAIL)
        s.box(230, y, 260, 64, t, d, "blue", tsize=14)
        s.line(490, y + 32, 510, y + 32, RAIL, 2)
    s.line(510, 182, 510, 382, RAIL, 2)
    s.arrow(510, 282, 536, 282, RAIL)
    s.box(540, 250, 220, 64, "元學習器", "Logistic（Level-1）", "violet", tsize=14)
    s.arrow(764, 282, 830, 282, RAIL)
    s.text(797, 272, "最終預測", 12, MUT, "normal", "middle")
    s.text(206, 430, "↑ 第 1 層（Level-0）", 12.5, MUT)
    s.text(510, 430, "↑ 第 2 層（Level-1）", 12.5, MUT)
    s.text(48, 480, "基礎學習器的預測結果會被當成「新特徵」，餵給第二層的元學習器做最終決策。",
           13, MUT)


def fig_loadmodel(s):
    steps = [("① Load Model", "拖入元件", "teal"), ("② .pkcls / .pkreg", "選擇模型", "blue"),
             ("③ 新資料（File）", "連接資料", "violet"), ("④ Predictions", "查看預測", "green")]
    for i, (title, sub, stage) in enumerate(steps):
        x = 48 + i * 210
        s.box(x, 190, 180, 80, title, sub, stage, tsize=13.5)
        if i < 3:
            s.arrow(x + 184, 230, x + 206, 230)
    s.text(48, 340, "順序不能顛倒：先選模型檔，再接資料——這四個標籤就是課程標在圖上的操作順序。",
           13, MUT)



def fig_saveload(s):
    s.rect(48, 140, 490, 300, fill=CARD2, stroke=C["teal"] + "66", rx=14)
    s.text(76, 172, "訓練階段（做一次）", 14.5, C["teal"], "700")
    s.box(64, 190, 110, 46, "File", None, "teal", tsize=13)
    s.arrow(178, 213, 192, 213)
    s.box(196, 190, 130, 46, "Preprocess", None, "blue", tsize=13)
    s.arrow(330, 213, 344, 213)
    s.box(348, 190, 150, 46, "模型元件", None, "violet", tsize=13)
    s.line(423, 236, 423, 248, RAIL, 2)
    s.line(235, 248, 423, 248, RAIL, 2)
    s.arrow(235, 248, 235, 261, RAIL)
    s.arrow(423, 248, 423, 261, RAIL)
    s.box(140, 265, 190, 46, "Test and Score（評估）", None, "blue", tsize=12)
    s.box(348, 265, 150, 46, "Save Model", None, "amber", tsize=13)
    s.arrow(423, 311, 423, 336, RAIL)
    s.box(348, 340, 150, 46, ".pkcls", None, "green", tsize=13)

    s.rect(566, 140, 286, 300, fill=CARD2, stroke=C["rose"] + "66", rx=14)
    s.text(594, 172, "推論階段（做很多次）", 14.5, C["rose"], "700")
    s.box(594, 190, 230, 46, "File（新資料）", None, "teal", tsize=13)
    s.arrow(709, 236, 709, 261, RAIL)
    s.box(594, 265, 230, 46, "Load Model", None, "violet", tsize=13)
    s.text(600, 254, "◀ .pkcls", 11.5, C["green"])
    s.arrow(709, 311, 709, 336, RAIL)
    s.box(594, 340, 230, 46, "Predictions（預測結果）", None, "green", tsize=12.5)

    s.text(48, 480, "訓練一次可能要幾小時，推論只要幾毫秒——這就是課程那句"
                    "「完全無需重新訓練」的價值。", 13, MUT)


def fig_examflow(s):
    s.box(60, 150, 160, 56, "File", "（資料）", "teal", tsize=13.5)
    s.arrow(224, 178, 266, 178)
    s.box(270, 150, 180, 56, "Constant", "（基準）", "amber", tsize=13.5)
    s.arrow(454, 178, 496, 178)
    s.box(500, 150, 200, 56, "Test and Score", None, "blue", tsize=13.5)
    s.text(712, 183, "← 先量基準線", 12, C["blue"], "700")

    s.box(270, 260, 180, 56, "Stacking", "（基礎＋元）", "violet", tsize=13.5)
    s.line(454, 288, 600, 288, RAIL, 2)
    s.arrow(600, 288, 600, 210, RAIL)
    s.text(614, 240, "← 再量整合後的提升", 12, C["violet"], "700")

    s.arrow(360, 316, 360, 348, RAIL)
    s.box(270, 350, 180, 56, "Save Model", None, "amber", tsize=13.5)
    s.line(454, 378, 525, 378, RAIL, 2)
    s.line(525, 378, 525, 426, RAIL, 2)
    s.arrow(525, 426, 525, 448, RAIL)
    s.text(534, 400, "model.pkcls", 12, C["green"], "700", "start", MONO)

    s.box(240, 450, 160, 56, "File（新）", None, "teal", tsize=13.5)
    s.arrow(404, 478, 436, 478)
    s.box(440, 450, 170, 56, "Load Model", None, "violet", tsize=13.5)
    s.arrow(614, 478, 646, 478)
    s.box(650, 450, 170, 56, "Predictions", None, "green", tsize=13.5)

    s.text(48, 560, "考試畫圖題的標準答案：Constant 先量基準線，Stacking 再量提升，"
                    "最後 Save Model → Load Model → Predictions。", 13, MUT)


def fig_deploy(s):
    """§13.8 部署流程（原文只有 7 個框線字元，inventory 的 art# 看不到）。"""
    s.box(300, 120, 300, 54, "訓練（GUI 或腳本）", None, "teal", tsize=14)
    s.arrow(450, 174, 450, 204)
    s.box(240, 208, 220, 54, "Save Model", None, "amber", tsize=14)
    s.arrow(464, 235, 514, 235)
    s.box(520, 208, 220, 54, "model.pkcls", None, "green", tsize=14)
    s.arrow(350, 262, 350, 294)
    s.text(366, 285, "↑ 把「模型 ＋ domain」一起序列化", 12, MUT)
    s.box(180, 298, 340, 54, "新的行程：Load Model（或 pickle.load）", None, "violet", tsize=13)
    s.arrow(350, 352, 350, 384)
    s.box(150, 388, 400, 54, "接一批「只有特徵、沒有答案」的新資料", None, "blue", tsize=13)
    s.arrow(554, 415, 604, 415)
    s.box(610, 388, 200, 54, "預測結果", None, "rose", tsize=14)
    s.text(48, 480, "Orange 沒有 REST API——官方路線就是 Save Model 存檔，"
                    "再在新行程裡 Load Model 接資料預測。", 13, MUT)


def fig_orange_tpot(s):
    panels = [
        ("Orange：探索、理解、建立 Constant 基準", "決定「這題該用哪一個指標衡量」", "teal"),
        ("TPOT：在你定義好的空間裡搜出最佳管線", "把搜尋空間交給演化演算法", "violet"),
        ("Orange：把結果拉回來，用視覺化檢查", "「這個模型是不是在胡說」", "teal"),
    ]
    for i, (title, sub, stage) in enumerate(panels):
        y = 150 + i * 150
        s.rect(140, y, 620, 90, fill=CARD2, stroke=C[stage] + "66", rx=12)
        s.text(170, y + 40, title, 15, C[stage], "700")
        s.text(170, y + 68, sub, 12.5, MUT)
        if i < 2:
            s.arrow(450, y + 90, 450, y + 144, RAIL)
    s.text(466, 272, "你已經知道要解什麼問題了", 12, MUT)
    s.text(466, 422, "拿到一條候選管線", 12, MUT)
    s.text(48, 580, "Orange 在上游幫你省下的時間，比 TPOT 在下游多榨出的分數更值錢。", 13, MUT)



FIGS = [
    ("orangeai-xy", "orange-ai-notes", 1, 900, 440,
     "特徵 X 與目標 y：什麼是「標記」", "每一列都有正確答案，才叫有標記", fig_xy,
     "圖 14：X 與 y——左邊是模型看得到的特徵表，右邊是模型要學著猜的品種（這就是「標記」）。"
     "｜手繪 SVG 圖表"),
    ("orangeai-tree-sensitive", "orange-ai-notes", 2, 900, 480,
     "決策樹對切點有多敏感", "2.45 改成 2.50，整棵樹就長得不一樣", fig_tree_sensitive,
     "圖 15：同一份鳶尾花資料，切點從 2.45 改成 2.50 就長出不同的樹——這就是高變異數，"
     "也是隨機森林存在的理由。｜手繪 SVG 圖表"),
    ("orangeai-accuracy", "orange-ai-notes", 3, 900, 660,
     "準確度 vs 可解釋性", "本機實測 CA：越準的越像黑箱", fig_accuracy,
     "圖 16：準確度（CA）與可解釋性的取捨——kNN／邏輯迴歸／Stacking 並列 0.9667，"
     "而 CN2 規則（0.8933）與樸素貝氏（0.8733）可解釋但沒那麼準。｜手繪 SVG 圖表"),
    ("orangeai-q4", "orange-ai-notes", 4, 1000, 540,
     "選模型的四組問答", "需要能解釋？資料量大嗎？在乎準確度？", fig_q4,
     "圖 17：決策流程——先問需不需要解釋（要文字規則用 CN2、只要看得懂用決策樹），"
     "再問資料量與準確度（隨機森林／梯度提升／邏輯迴歸）。｜手繪 SVG 圖表"),
    ("orangeai-svm", "orange-ai-notes", 5, 900, 460,
     "SVM 在最大化什麼", "決策邊界兩側各留一條間隔，把它撐到最寬", fig_svm,
     "圖 18：SVM 的間隔——決策邊界（超平面）上下各一條虛線，SVM 要讓兩條虛線的距離最大化；"
     "真正決定這條線的只有支持向量。｜手繪 SVG 圖表"),
    ("orangeai-sigmoid", "orange-ai-notes", 6, 900, 520,
     "sigmoid：S 形曲線", "σ(z) = 1 / (1 + e^(−z))，輸出直接當機率", fig_sigmoid,
     "圖 19：邏輯迴歸的核心——sigmoid 把任意實數壓到 0～1；z = 0 時機率正好 0.5，"
     "那就是分類門檻。｜手繪 SVG 圖表"),
    ("orangeai-bayes", "orange-ai-notes", 7, 900, 460,
     "貝氏定理與「樸素」兩個字", "後驗 ∝ 先驗 × 似然", fig_bayes,
     "圖 20：貝氏定理——分類版本是「後驗機率 ∝ 先驗機率 × 似然」；"
     "「樸素」指假設每個特徵彼此獨立，所以似然可以直接相乘。｜手繪 SVG 圖表"),
    ("orangeai-constant", "orange-ai-notes", 8, 900, 440,
     "Constant：最笨的基準線", "先知道「什麼都不學」能拿幾分", fig_constant,
     "圖 21：Constant 的工作流——File 接 Constant 再分頭接 Test and Score（先量基準線）"
     "與 Predictions（查看預測結果）。｜手繪 SVG 圖表"),
    ("orangeai-stacking", "orange-ai-notes", 9, 900, 520,
     "Stacking 的兩層架構", "基礎學習器的預測，變成元學習器的新特徵", fig_stacking,
     "圖 22：Stacking——第 1 層是三個基礎學習器（Logistic／RandomForest／SVM），"
     "它們的預測當成新特徵，交給第 2 層的元學習器做最終預測。｜手繪 SVG 圖表"),
    ("orangeai-loadmodel", "orange-ai-notes", 10, 900, 380,
     "Load Model 的四個步驟", "拖入元件 → 選擇模型 → 連接資料 → 查看預測", fig_loadmodel,
     "圖 23：Load Model——① 拖入元件、② 選 .pkcls／.pkreg、③ 接上新資料、④ 看 Predictions；"
     "順序不能顛倒。｜手繪 SVG 圖表"),
    ("orangeai-saveload", "orange-ai-notes", 11, 900, 520,
     "Save / Load 的完整閉環", "訓練做一次、推論做很多次", fig_saveload,
     "圖 24：完整閉環——訓練階段（File → Preprocess → 模型元件 → Save Model → .pkcls）"
     "與推論階段（File → Load Model → Predictions），所以推論完全不需要重新訓練。"
     "｜手繪 SVG 圖表"),
    ("orangeai-examflow", "orange-ai-notes", 12, 900, 620,
     "四個元件串成一條完整流程", "考試畫圖題的標準答案", fig_examflow,
     "圖 25：考試畫圖題——File 先接 Constant 量基準線，Stacking 再量整合後的提升，"
     "Save Model 存成 model.pkcls，最後用 Load Model 載入並輸出 Predictions。｜手繪 SVG 圖表"),
    ("orangeai-orange-tpot", "orange-ai-notes", 13, 900, 620,
     "Orange 與 TPOT：不是二選一，是有先後", "上游省下的時間比下游多榨的分數更值錢",
     fig_orange_tpot,
     "圖 26：先後關係——Orange 先探索並建立 Constant 基準（決定用哪個指標），"
     "TPOT 再在定義好的空間裡搜出最佳管線，最後拉回 Orange 用視覺化檢查。｜手繪 SVG 圖表"),
    # §13.8 的部署流程只有 7 個框線字元，inventory.py 的 art# 看不到它，
    # 所以這張由 _work/diagrams/embed_orange_deploy.py 直接定點替換（art 記為 0）。
    ("orangeai-deploy", "orange-ai-notes", 0, 900, 520,
     "部署：Save Model → .pkcls → 自己包一層服務",
     "Orange 沒有 REST API，官方路線就是存檔再載入", fig_deploy,
     "圖 27：部署流程——訓練完成後 Save Model 序列化出 model.pkcls（模型＋domain），"
     "在新行程裡 Load Model 接一批只有特徵的新資料，得到預測結果。｜手繪 SVG 圖表"),
]

if __name__ == "__main__":
    for slug, note, art, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-28s %-18s art#%-2d %dx%d  %s"
              % (slug + ".svg", note, art, w, h,
                 "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))
