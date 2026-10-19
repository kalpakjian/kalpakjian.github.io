# -*- coding: utf-8 -*-
"""prompt-engineering-notes: 3 ASCII blocks -> SVG.

  art#1  §0    全課大綱（四個 Part）＋「一句話選技術」對照
  art#2  §31.3 PAL 流程（題目 -> 產生程式 -> 執行 -> 可信答案）
  art#3  §32.3 ReAct 迴圈（Thought -> Action -> Observation -> 再一輪）
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from svglib import Svg, C, MUT, TXT, CARD2  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAIL = "#30363d"

PARTS = [
    (0, "Part 1　基礎：prompt 元素 → 解碼參數 → 六大任務 → 七大類技術", "teal"),
    (1, "基礎技術：Zero-Shot／Few-Shot／Clear Instructions", None),
    (1, "上下文與角色：System／Role／Contextual／Markdown", None),
    (1, "推理與規劃：CoT／TCoT／SoT／Step-Back", None),
    (0, "Part 2　進階：Least-to-Most／ToT／iToT／SG-ICL", "blue"),
    (1, "專業與前沿：CAI／Perspective-Taking／Analogical／Multi-Modal／"
        "Persona Consistency／Predictive", None),
    (1, "知識與工具：Generate Knowledge／PAL／ReAct", None),
    (0, "Part 3　工具與應用：Tools & IDEs／LLM + 外部工具／Data-Augmented Generation", "amber"),
    (0, "Part 4　結論與未來：Model Safety／Prompt Injection·Leaking·Jailbreaking／RLHF", "violet"),
]

PICKS = [
    ("要「格式穩定」", "Clear Instructions、Markdown、System Prompting", "teal"),
    ("要「算得對」", "CoT、TCoT、PAL（把計算交給 Python）", "blue"),
    ("要「大綱先行」", "SoT（Skeleton-of-Thought）", "amber"),
    ("要「先想通則再解題」", "Step-Back、Least-to-Most", "violet"),
    ("要「多路探索再選」", "ToT、iToT（思維樹／交錯思維樹）", "green"),
    ("要「有憑據、能查證」", "Generate Knowledge、ReAct、DAG", "rose"),
    ("要「安全、合規」", "CAI、System Prompting 的安全界線", "teal"),
]


def outline_panel(s, x, y, w, h, root, rows, pitch=32, top=84):
    """Bordered panel: root line + a rail/indent tree supporting 3 levels."""
    s.rect(x, y, w, h, fill=CARD2, stroke="#2a6f68", rx=14)
    s.text(x + 28, y + 42, root, 18, TXT, "700")
    rail, sub, sub2 = x + 52, x + 108, x + 164
    ys = [y + top + i * pitch for i in range(len(rows))]
    s.line(rail, ys[0] - 6, rail, ys[-1] - 6, RAIL, 1.5)
    for i, (lvl, txt, stage) in enumerate(rows):
        sy = ys[i] - 6
        if lvl == 0:
            s.line(rail, sy, rail + 14, sy, RAIL, 1.5)
            s.text(rail + 20, ys[i], txt, 13.5, C[stage] if stage else TXT, "700")
        elif lvl == 1:
            s.line(sub, ys[i - 1] - 6 + 10, sub, sy, RAIL, 1.5)
            s.line(sub, sy, sub + 14, sy, RAIL, 1.5)
            s.text(sub + 20, ys[i], txt, 12.5, TXT)
        else:
            s.line(sub2, ys[i - 1] - 6 + 10, sub2, sy, RAIL, 1.5)
            s.line(sub2, sy, sub2 + 14, sy, RAIL, 1.5)
            s.text(sub2 + 20, ys[i], txt, 12, MUT)


def fig_outline(s):
    outline_panel(s, 48, 106, 904, 366, "一堂課的四個 Part（課程分章）", PARTS)

    s.text(48, 522, "一句話選技術：先問你要什麼", 16, TXT, "700")
    for i, (title, detail, stage) in enumerate(PICKS):
        col, row = i % 2, i // 2
        x, y = 48 + col * 462, 542 + row * 62
        s.rect(x, y, 442, 54, fill=CARD2, stroke=C[stage] + "66", rx=10)
        s.text(x + 16, y + 22, title, 13.5, C[stage], "700")
        s.text(x + 16, y + 42, "→ " + detail, 11.5, MUT)

    s.text(48, 822, "上半是課程的四個 Part；下半是「一句話選技術」——"
                    "先問你要什麼，再挑對應的技術。", 13, MUT)


def fig_pal(s):
    steps = [
        ("自然語言題目", "problem", "teal"),
        ("LLM 產生 Python 程式", "中間推理步驟", "blue"),
        ("Python 執行", "得到數值結果", "violet"),
    ]
    xs = [48, 320, 592]
    for (label, sub, stage), x in zip(steps, xs):
        s.box(x, 140, 220, 84, label, sub, stage, tsize=14)
    s.arrow(272, 182, 316, 182)
    s.arrow(544, 182, 588, 182)

    s.arrow(702, 226, 702, 260)
    s.box(562, 262, 280, 60, "最終答案", "可信的計算", "green")

    s.text(48, 356, "CoT 用文字算數（可能算錯）；PAL 只負責把題目翻成程式，"
                    "把「算」外包給 Python 直譯器。", 13, MUT)


def fig_react(s):
    steps = [
        ("Thought", "推理：我現在需要知道什麼？", "teal"),
        ("Action", "行動：去查 / 去算 / 去呼叫工具", "blue"),
        ("Observation", "觀察：工具回傳了什麼？", "violet"),
    ]
    ys = [140, 240, 340]
    for (label, sub, stage), y in zip(steps, ys):
        s.box(120, y, 560, 64, label, sub, stage, tsize=15)
    s.arrow(400, 204, 400, 238)
    s.arrow(400, 304, 400, 338)

    s.line(680, 372, 800, 372)
    s.line(800, 372, 800, 172)
    s.arrow(800, 172, 684, 172)
    s.text(740, 362, "還沒答完就再一輪", 12, MUT, "normal", "middle")

    s.arrow(400, 404, 400, 440)
    s.text(412, 428, "答完了", 12, C["green"], "700")
    s.box(240, 444, 320, 56, "Final Answer", "把 Observation 整理成最終回答", "green")

    s.text(48, 540, "ReAct 把「推理」與「行動」交錯起來：每一輪都先想、再查、再看結果，"
                    "直到能回答為止。", 13, MUT)


FIGS = [
    ("prompteng-outline", "prompt-engineering-notes", 1, 1000, 850,
     "Prompt Engineering：全課大綱", "四個 Part 與「一句話選技術」對照表", fig_outline,
     "圖 39：全課大綱——Part 1 基礎／Part 2 進階／Part 3 工具與應用／Part 4 結論與未來，"
     "以及「先問你要什麼，再挑技術」的七條對照。｜手繪 SVG 圖表"),
    ("prompteng-pal", "prompt-engineering-notes", 2, 900, 380,
     "PAL：把計算外包給 Python", "模型只負責翻譯題目，算術交給直譯器", fig_pal,
     "圖 40：PAL 流程——自然語言題目 → LLM 產生 Python 程式（中間推理步驟）→ "
     "Python 執行得到數值 → 可信的最終答案。｜手繪 SVG 圖表"),
    ("prompteng-react", "prompt-engineering-notes", 3, 900, 560,
     "ReAct：推理與行動交錯的迴圈", "Thought → Action → Observation，直到答得出來", fig_react,
     "圖 41：ReAct 迴圈——Thought（我需要知道什麼）→ Action（去查／去算）→ "
     "Observation（工具回傳什麼），還沒答完就再一輪，答完了才輸出 Final Answer。｜手繪 SVG 圖表"),
]

if __name__ == "__main__":
    for slug, note, art, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-30s %-24s art#%d %dx%d  %s"
              % (slug + ".svg", note, art, w, h,
                 "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))
