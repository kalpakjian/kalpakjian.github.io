# -*- coding: utf-8 -*-
"""generalization-notes: 2 ASCII blocks -> SVG.

  art#1  §2.2 複雜度光譜（太簡單 ─ 剛剛好 ─ 太複雜）
  art#2  §9.2 診斷決策流程（先量測 -> 三種結果）
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from svglib import Svg, C, MUT, TXT, CARD2  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAIL = "#7d8590"


def fig_spectrum(s):
    s.text(48, 120, "模型複雜度（由左至右遞增）", 12.5, MUT)
    s.arrow(70, 132, 838, 132, RAIL)

    zones = [
        ("太簡單", "欠擬合", "blue",
         ["訓練與測試都差（例：0.61 / 0.58）",
          "落差小：兩邊都沒學好",
          "解法：提高複雜度、加特徵",
          "　　　降低正則化"]),
        ("剛剛好", "甜點區（泛化最佳）", "green",
         ["測試誤差最低（實測 degree=2）",
          "訓練 1.580／測試 2.005",
          "落差小、兩邊都好",
          "想再推一點：集成學習"]),
        ("太複雜", "過擬合", "rose",
         ["訓練極好（常接近 100%）",
          "落差大（例：0.99 / 0.62）",
          "解法：加資料、正則化、早停",
          "　　　集成"]),
    ]
    for i, (head, name, stage, lines) in enumerate(zones):
        x = 66 + i * 259
        s.box(x, 150, 250, 52, head, None, stage, tsize=16)
        s.rect(x, 218, 250, 172, fill=CARD2, stroke=C[stage] + "66", rx=12)
        s.text(x + 16, 250, name, 14.5, TXT, "700")
        for j, ln in enumerate(lines):
            s.text(x + 16, 280 + j * 25, ln, 11.5, MUT)

    s.text(48, 424, "兩邊都差＝欠擬合；兩邊都好但落差大＝過擬合；中間測試誤差最低的那一段才是甜點區。",
           13, MUT)


def fig_diagnose(s):
    s.box(48, 110, 360, 58, "① 先量測（§5）", "訓練分數 vs 交叉驗證分數", "teal")

    rows = [
        ("1", "落差大（如 0.99 / 0.62）　→　過擬合（§3）",
         "解法：① 加資料　② 正則化　③ 早停　④ 集成", "rose"),
        ("2", "都差且落差小（如 0.61 / 0.58）　→　欠擬合（§4）",
         "解法：提高複雜度、加特徵、降低正則化", "blue"),
        ("3", "都好（如 0.97 / 0.95）　→　泛化良好",
         "想再推一點：集成學習、更多資料", "green"),
    ]
    ys = [200 + i * 90 for i in range(3)]
    s.line(100, 168, 100, ys[-1] + 36, RAIL, 2)
    for (num, title, detail, stage), y in zip(rows, ys):
        s.line(100, y + 36, 158, y + 36, RAIL, 2)
        s.card(160, y, 690, 72, title, detail, stage, num=num)

    s.text(48, 500, "診斷的第一步永遠是「先看落差」：落差大＝過擬合；落差小又兩邊都差＝欠擬合；"
                    "兩邊都好＝泛化良好。", 13, MUT)


FIGS = [
    ("generalization-spectrum", "generalization-notes", 1, 900, 450,
     "模型複雜度光譜：不是二選一", "左邊太簡單、右邊太複雜，中間才是甜點區", fig_spectrum,
     "圖 10：複雜度光譜——欠擬合（兩邊都差）、甜點區（測試誤差最低）、過擬合（落差大）"
     "各自的症狀與解法方向。｜手繪 SVG 圖表"),
    ("generalization-diagnosis", "generalization-notes", 2, 900, 520,
     "診斷決策流程：把整節課串起來", "先量測訓練分數與交叉驗證分數，再看落差", fig_diagnose,
     "圖 11：診斷決策流程——落差大＝過擬合（加資料／正則化／早停／集成）；落差小又兩邊都差"
     "＝欠擬合（提高複雜度、加特徵）；兩邊都好＝泛化良好。｜手繪 SVG 圖表"),
]

if __name__ == "__main__":
    for slug, note, art, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-30s %-22s art#%d %dx%d  %s"
              % (slug + ".svg", note, art, w, h,
                 "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))
