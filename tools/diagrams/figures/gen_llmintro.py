# -*- coding: utf-8 -*-
"""llm-intro-notes: the LLM concept outline -> a styled tree panel + a pipeline chain."""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
sys.path.insert(0, os.path.dirname(_HERE))   # 上一層：svglib.py 在這裡
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


def fig_scale(s):
    """參數量的三級階梯（原本是 5 行 ASCII 圖）。"""
    s.rect(150, 122, 250, 56, fill=CARD2, stroke=C["gray"] + "66", rx=10)
    s.text(168, 156, "傳統機器學習模型", 14.5, TXT, "700")
    s.line(400, 150, 424, 150, RAIL, 1.6)
    s.text(436, 156, "數千 ~ 數百萬個參數", 13.5, MUT)

    s.rect(150, 214, 250, 56, fill=CARD2, stroke=C["blue"] + "66", rx=10)
    s.text(168, 248, "早期 NLP 神經網路", 14.5, TXT, "700")
    s.line(400, 242, 424, 242, RAIL, 1.6)
    s.text(436, 248, "數百萬 ~ 數億個參數", 13.5, MUT)

    s.rect(150, 306, 250, 56, fill=CARD2, stroke=C["violet"] + "77", rx=10)
    s.text(168, 340, "LLM（GPT-3 級）", 14.5, TXT, "700")
    s.line(400, 334, 424, 334, RAIL, 1.6)
    s.text(436, 340, "數千億個參數（175 B）＋ 兆級 token 的訓練資料", 13.5, TXT)

    # 層間的下降箭頭
    s.arrow(275, 178, 275, 210, RAIL)
    s.arrow(275, 270, 275, 302, RAIL)

    # 左側：規模成長的量尺
    s.line(104, 150, 104, 336, C["amber"], 2)
    s.arrow(104, 336, 104, 362, C["amber"], 2)
    s.text(48, 134, "參數量", 12.5, C["amber"], "700")
    s.text(48, 386, "每往下一級，規模再翻幾個數量級", 12, MUT)

    s.text(48, 418, "從數百萬到數千億，跨越四個數量級 —— 這就是「Large」兩個字的來源；"
                    "但參數量只是結果，真正拉開差距的是 transformer 架構與海量訓練資料。",
           12.5, MUT)


FIGS = [
    ("llm-concept-tree", "llm-intro-notes", 1, 1000, 600,
     "LLM 是什麼：一頁看懂", "定義、來由、訓練、架構、流派與輸入管線", fig_llm,
     "圖 43：LLM 的概念全貌——七個主分支與兩則補充，最後是從文字到模型主層的輸入管線。"
     "｜手繪 SVG 圖表"),
    ("llm-scale-ladder", "llm-intro-notes", 2, 900, 440,
     "參數量的三級階梯", "每往下一級，規模再翻幾個數量級", fig_scale,
     "圖 44：參數量一路長上去——傳統機器學習模型數千到數百萬、早期 NLP 神經網路數百萬到數億、"
     "LLM（GPT-3 級）數千億（175 B）＋兆級 token 的訓練資料，跨越四個數量級。｜手繪 SVG 圖表"),
]

if __name__ == "__main__":
    for slug, note, art, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-26s %-20s art#%d %dx%d  %s"
              % (slug + ".svg", note, art, w, h,
                 "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s through text %s" % (seg, box))
