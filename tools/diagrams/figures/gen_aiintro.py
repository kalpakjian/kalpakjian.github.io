# -*- coding: utf-8 -*-
"""ai-intro-notes: 把 ASCII 的「AI = 具人類式智慧的機器智慧」樹狀圖換成內嵌 SVG。

ASCII 原文（art#1）：
    AI = 具人類式智慧的「機器智慧」
      ├─ 取徑：Human approach（think/act like humans）
      │        Ideal approach（think/act rationally）
      ├─ 子目標：NLP、Navigate、Represent Knowledge、Reasoning、Perception
      └─ 典型應用：
           影像 → Image/Video Recognition → Facial Recognition（Detection→Analysis→Recognition）
           語言 → NLP → Speech Recognition（HMM、cepstral coefficients）
           決策 → Reinforcement Learning（agent、reward、policy）
           生成 → Generative AI（deep learning 生成新內容）
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from svglib import Svg, C, MUT, TXT, CARD2    # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAIL = "#30363d"

# (標題, 顏色, [子項...])
GROUPS = [
    ("取徑", "teal", [
        "Human approach（think/act like humans）",
        "Ideal approach（think/act rationally）",
    ]),
    ("子目標", "blue", [
        "NLP、Navigate、Represent Knowledge、Reasoning、Perception",
    ]),
    ("典型應用", "amber", [
        "影像 → Image/Video Recognition → Facial Recognition（Detection→Analysis→Recognition）",
        "語言 → NLP → Speech Recognition（HMM、cepstral coefficients）",
        "決策 → Reinforcement Learning（agent、reward、policy）",
        "生成 → Generative AI（deep learning 生成新內容）",
    ]),
]


def fig_ai_tree(s):
    s.rect(48, 100, 804, 470, fill=CARD2, stroke="#2a6f68", rx=14)
    s.text(76, 142, "AI = 具人類式智慧的「機器智慧」", 17, TXT, "700")

    rail, sub = 100, 158
    # 先算好每列的 y；parent 記的是「父節點在 rows 裡的索引」
    rows = []                      # (level, text, stage, y, parent_index)
    parents = []                   # 每個群組的父節點索引
    y = 190
    for label, stage, leaves in GROUPS:
        parents.append(len(rows))
        rows.append((0, label, stage, y, len(rows)))
        y += 34
        for lf in leaves:
            rows.append((1, lf, None, y, parents[-1]))
            y += 30
        y += 14

    # 主幹
    s.line(rail, rows[0][3] - 6, rail, rows[-1][3] - 6, RAIL, 1.5)
    # 每個 level-0 群組自己的子軌
    for gi, parent in enumerate(parents):
        idxs = [i for i, r in enumerate(rows) if r[4] == parent and r[0] == 1]
        if idxs:
            s.line(sub, rows[idxs[0]][3] - 6 + 10, sub, rows[idxs[-1]][3] - 6,
                   RAIL, 1.5)

    for i, (lvl, txt, stage, ry, parent) in enumerate(rows):
        sy = ry - 6
        if lvl == 0:
            s.line(rail, sy, rail + 14, sy, RAIL, 1.5)
            s.text(rail + 20, ry, txt, 14, C[stage], "700")
        else:
            s.line(sub, sy, sub + 14, sy, RAIL, 1.5)
            s.text(sub + 20, ry, txt, 11.5, TXT)

    s.text(48, 600, "三個層次：為什麼做（取徑）、要做成什麼（子目標）、"
                    "以及實際拿來幹嘛（典型應用）。", 13, MUT)


FIGS = [
    ("ai-intro-tree", "ai-intro-notes", 1, 900, 620,
     "AI 是什麼：一棵樹看完", "取徑、子目標與典型應用", fig_ai_tree,
     "圖 11：AI 的三個層次——取徑（Human／Ideal）、子目標（NLP、Navigate、"
     "Represent Knowledge、Reasoning、Perception），以及四個典型應用"
     "（影像辨識、語言、決策、生成）。｜手繪 SVG 圖表"),
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
