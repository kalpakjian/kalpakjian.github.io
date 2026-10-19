# -*- coding: utf-8 -*-
"""llm-intro-notes: the LLM concept outline -> a styled tree panel + a pipeline chain."""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import Svg, C, MUT, TXT, CARD2  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAIL = "#30363d"

ROWS = [
    (0, "定義：為了「理解、生成、回應」人類文字而設計的神經網路"),
    (1, "「Large」有兩層意思：參數量（tens / hundreds of billions）＋ 訓練資料量"),
    (0, "與早期 NLP 的差別：早期為「單一特定任務」而設計；LLM 跨任務通用"),
    (0, "成功的兩個原因：① transformer 架構　② 海量訓練資料"),
    (0, "訓練兩階段：pretraining（大而雜）→ finetuning（小而專）"),
    (1, "兩種微調：instruction-finetuning／classification finetuning"),
    (0, "架構：encoder（讀懂輸入）＋ decoder（生成輸出）＋ self-attention"),
    (0, "兩大流派：BERT（encoder、遮字填空、分類）／ GPT（decoder、生成、自迴歸）"),
]
PIPE = ["文字", "tokenize", "token ID", "embedding", "＋positional embedding", "LLM 主層"]


def fig_llm(s):
    s.rect(48, 106, 904, 366, fill=CARD2, stroke="#2a6f68", rx=14)
    s.text(76, 148, "LLM = Large Language Model（大型語言模型）", 18, TXT, "700")

    rail, sub = 100, 134
    ys = [190 + i * 36 for i in range(len(ROWS))]
    s.line(rail, ys[0] - 6, rail, ys[-1] - 6, RAIL, 1.5)
    for i, (lvl, txt) in enumerate(ROWS):
        sy = ys[i] - 6
        if lvl == 0:
            s.line(rail, sy, rail + 14, sy, RAIL, 1.5)
            s.text(rail + 20, ys[i], txt, 13.5, TXT)
        else:
            s.line(sub, ys[i - 1] - 6 + 10, sub, sy, RAIL, 1.5)
            s.line(sub, sy, sub + 14, sy, RAIL, 1.5)
            s.text(sub + 20, ys[i], txt, 12.5, MUT)

    s.text(76, 506, "輸入處理管線", 13.5, TXT, "700")
    x = 76
    for i, p in enumerate(PIPE):
        w = s._est_w(p, 12.5) + 26
        s.rect(x, 524, w, 38, fill="#0d1117", stroke=C["teal"] + "66", rx=19)
        s.text(x + w / 2, 548, p, 12.5, C["teal"], "700", "middle")
        if i < len(PIPE) - 1:
            s.arrow(x + w + 4, 543, x + w + 32, 543, C["teal"])
        x += w + 36


FIGS = [
    ("llm-concept-tree", "llm-intro-notes", 1, 1000, 600,
     "LLM 是什麼：一頁看懂", "定義、來由、訓練、架構、流派與輸入管線",
     "圖 43：LLM 的概念全貌——七個主分支與兩則補充，最後是從文字到模型主層的輸入管線。"
     "｜手繪 SVG 圖表"),
]

if __name__ == "__main__":
    for slug, note, art, w, h, title, sub, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fig_llm(s)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-26s %-20s art#%d %dx%d  %s"
              % (slug + ".svg", note, art, w, h,
                 "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s through text %s" % (seg, box))
