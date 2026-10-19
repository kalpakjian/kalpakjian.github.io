# -*- coding: utf-8 -*-
"""cv-intro-notes (2 diagrams) + automl-notes (2 diagrams)."""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import Svg, C, MUT, TXT, CARD2  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAIL = "#30363d"


def tree_panel(s, x, y, w, h, root, rows, rail=52, sub=86):
    """A panel holding a root line plus a rail/indent tree (rows = [(level, text)])."""
    s.rect(x, y, w, h, fill=CARD2, stroke="#2a6f68", rx=14)
    s.text(x + 28, y + 42, root, 17, TXT, "700")
    ys = [y + 84 + i * 36 for i in range(len(rows))]
    s.line(x + rail, ys[0] - 6, x + rail, ys[-1] - 6, RAIL, 1.5)
    for i, (lvl, txt) in enumerate(rows):
        sy = ys[i] - 6
        if lvl == 0:
            s.line(x + rail, sy, x + rail + 14, sy, RAIL, 1.5)
            s.text(x + rail + 20, ys[i], txt, 13.5, TXT)
        else:
            s.line(x + sub, ys[i - 1] - 6 + 10, x + sub, sy, RAIL, 1.5)
            s.line(x + sub, sy, x + sub + 14, sy, RAIL, 1.5)
            s.text(x + sub + 20, ys[i], txt, 12.5, MUT)
    return ys


def fig_cv_tree(s):
    tree_panel(s, 48, 106, 904, 372, "電腦視覺（Computer Vision）", [
        (0, "商業應用：零售、安防、工業檢測、醫療、自駕、農業…"),
        (0, "2024 世界機器人大會：超現實圍棋博弈（人機對弈展示）"),
        (0, "核心技術：CNN（卷積神經網路）"),
        (1, "定義：處理「網格狀資料」（影像、音訊）的神經網路"),
        (1, "關鍵：卷積層自動學習「階層式特徵」（由低階到高階）"),
        (1, "架構：encoder（多個逐漸變窄的 block 堆疊 →「deep」）"),
        (1, "核心思想：參數重用（parameter sharing）"),
    ])


def fig_cv_ladder(s):
    s.line(90, 150, 90, 440, RAIL, 1.5)
    s.arrow(90, 412, 90, 440, "#7d8590")
    s.text(22, 152, "低階", 13, C["teal"], "700")
    s.text(22, 442, "高階", 13, C["amber"], "700")
    stages = [
        ("輸入影像", "原始像素", "gray"),
        ("低階特徵", "邊緣、線條、角點", "teal"),
        ("中階特徵", "紋理、圓形、局部形狀", "blue"),
        ("高階特徵", "眼睛、車輪、人臉等「物件部件」", "violet"),
        ("整體", "可辨識的物件類別", "amber"),
    ]
    for i, (t, d, st) in enumerate(stages):
        bx, by = 120 + i * 30, 120 + i * 70
        s.box(bx, by, 560, 54, t, d, st, tsize=15, dsize=12)
        if i < len(stages) - 1:
            s.arrow(bx + 40, by + 54, bx + 40, by + 68, C[st])


def fig_automl_decision(s):
    s.box(60, 150, 230, 56, "問題是「分類」嗎？", None, "teal", tsize=14.5)
    s.box(360, 84, 210, 56, "數據平衡嗎？", None, "blue", tsize=14.5)
    s.box(360, 246, 210, 56, "看 RMSE（或 R²）", None, "amber", tsize=14.5)
    s.box(660, 36, 200, 46, "用 Accuracy", None, "green", tsize=14)
    s.box(660, 116, 200, 46, "用 AUC", None, "rose", tsize=14)
    for y in (112, 274):
        s.line(290, 178, 325, 178, RAIL)
        s.line(325, 178, 325, y, RAIL)
        s.arrow(325, y, 358, y, RAIL)
    for y in (59, 139):
        s.line(570, 112, 615, 112, RAIL)
        s.line(615, 112, 615, y, RAIL)
        s.arrow(615, y, 658, y, RAIL)
    s.text(296, 170, "是", 12.5, C["teal"], "700")
    s.text(332, 214, "否（迴歸）", 12.5, C["amber"], "700")
    s.text(668, 58, "平衡", 12, C["green"], "700")
    s.text(668, 138, "不平衡", 12, C["rose"], "700")
def topic_card(s, x, y, w, h, num, title, lines, stage):
    s.rect(x, y, w, h, fill=CARD2, stroke=C[stage] + "66", rx=12)
    s.badge(x + 34, y + 34, num, C[stage], r=15, size=13)
    s.text(x + 60, y + 39, title, 14.5, TXT, "700")
    for i, ln in enumerate(lines):
        s.text(x + 60, y + 64 + i * 21, ln, 11.5, MUT)


def fig_automl_skeleton(s):
    cards = [
        ("1", "為什麼需要 AutoML",
         ["傳統 ML 三痛點：流程繁瑣、耗時費力、高度依賴專家",
          "AutoML 三突破：全自動化、高效能、低門檻"], "teal"),
        ("2", "自動化的兩個關鍵動作",
         ["Auto Imputation：自動填缺失值",
          "Auto Encoding：自動轉類別特徵"], "teal"),
        ("3", "負責任 AI 六大原則",
         ["公 · 可 · 隱 · 包 · 透 · 問",
          "公平性／可靠性與安全性／隱私與保障",
          "包容性／透明度／問責制"], "blue"),
        ("4", "任務類型",
         ["問「會不會」＝ 分類（用 AUC）",
          "問「多少」＝ 迴歸（用 RMSE / R²）"], "blue"),
        ("5", "三個指標的陷阱",
         ["Accuracy：不平衡資料會騙人",
          "AUC：0.5 = 瞎猜，1.0 = 完美",
          "RMSE：對離群值極敏感（誤差先平方）"], "amber"),
        ("6", "三個實作平台",
         ["無代碼：Teachable Machine（示範級）",
          "企業雲端：Azure ML Studio（Data → Compute）",
          "開源：Colab + TPOT（遺傳演算法搜尋 Pipeline）"], "violet"),
        ("7", "TPOT 的兩個旋鈕",
         ["generations：演化幾代",
          "population_size：每代幾個模型",
          "導出：print(tpot.fitted_pipeline_)"], "rose"),
    ]
    for i, (num, title, lines, st) in enumerate(cards):
        col, row = i % 2, i // 2
        topic_card(s, 48 + col * 462, 120 + row * 116, 430, 104,
                   num, title, lines, st)
    s.text(48, 604, "整門課的骨架：先懂痛點與倫理，再分任務類型挑指標，最後在三個平台上實作。", 13, MUT)


FIGS = [
    ("cv-cnn-tree", "cv-intro-notes", 1, 1000, 500,
     "電腦視覺與 CNN：一頁看懂", "應用場景、關鍵技術與四個核心觀念", fig_cv_tree,
     "圖 1：電腦視覺的三個分支——應用場景、世界機器人大會案例，以及核心技術 CNN 的四個觀念。"
     "｜手繪 SVG 圖表"),
    ("cv-feature-ladder", "cv-intro-notes", 2, 900, 520,
     "CNN 學到的階層式特徵", "從邊緣到物件：網路越深，看到的東西越抽象", fig_cv_ladder,
     "圖 2：階層式特徵——低階看到邊緣與角點，中階組出紋理與形狀，"
     "高階才認得出眼睛、車輪等物件部件。｜手繪 SVG 圖表"),
    ("automl-metric-decision", "automl-notes", 1, 900, 370,
     "指標怎麼挑：兩個問題就問完", "先問任務類型，再問資料平衡嗎", fig_automl_decision,
     "圖 14：指標決策樹——分類再看資料是否平衡（平衡用 Accuracy、不平衡用 AUC），"
     "迴歸直接看 RMSE 或 R²。｜手繪 SVG 圖表"),
    ("automl-course-skeleton", "automl-notes", 2, 1000, 640,
     "AutoML 應用證書：全課程骨架", "七個主題，一張圖看完", fig_automl_skeleton,
     "圖 15：課程骨架——從「為什麼需要 AutoML」到「TPOT 的兩個旋鈕」，"
     "七個主題各自的重點與產出。｜手繪 SVG 圖表"),
]

if __name__ == "__main__":
    for slug, note, art, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-28s %-18s art#%d %dx%d  %s"
              % (slug + ".svg", note, art, w, h,
                 "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s through text %s" % (seg, box))
