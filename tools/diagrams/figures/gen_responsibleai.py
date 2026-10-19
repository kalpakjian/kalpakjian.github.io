# -*- coding: utf-8 -*-
"""responsible-ai-notes: 2 ASCII blocks -> SVG.

  art#1  §0    全書大綱樹（為什麼做／怎麼做／四大議題／香港法規／社會影響）
  art#2  §18.4 全書收束：三分支匯流成結論
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

# (level, text, stage) -- stage colours only the five/six main branches
ROWS = [
    (0, "為什麼要做　—　Challenges on AI：不透明、偏誤、隱私、問責、就業衝擊", "teal"),
    (0, "怎麼做", "blue"),
    (1, "① Ethical AI Principles（12 項倫理原則）", None),
    (1, "② AI Practice Guide（6 階段專案生命週期）", None),
    (0, "電腦視覺的四大倫理議題", "amber"),
    (1, "Privacy and Surveillance　隱私與監控（人臉辨識、無同意追蹤）", None),
    (1, "Bias and Discrimination　偏見與歧視（資料不具代表性）", None),
    (1, "Data Security and Consent　資料安全與同意（外洩、不知情蒐集）", None),
    (1, "Accountability and Transparency　問責與透明（黑箱、責任歸屬）", None),
    (0, "香港法規", "violet"),
    (1, "PDPO《個人資料（私隱）條例》Cap. 486，1996/12/20 生效", None),
    (2, "六項保護原則 DPP1–DPP6（收集／保留／使用／保安／開放／查閱更正）", None),
    (0, "社會影響", "green"),
    (1, "正面：提升公共安全、改善醫療服務", None),
    (1, "挑戰：就業與勞動力變化、社會不平等、對人類行為的影響", None),
    (0, "六項倫理使用建議　＋　結論：創新與倫理責任必須平衡", "rose"),
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
    outline_panel(s, 48, 106, 904, 590, "Responsible AI（負責任的 AI）", ROWS)
    s.text(48, 736, "六個主分支（為什麼做／怎麼做／四大議題／香港法規／社會影響／結論）；"
                    "縮排細項是考點關鍵字，考前照這棵樹往下唸即可。", 13, MUT)


def fig_summary(s):
    s.box(310, 110, 280, 54, "Responsible AI", None, "teal")
    cards = [
        ("為什麼要做", "Challenges on AI", "不透明、偏誤、隱私、問責、就業衝擊", "teal"),
        ("怎麼做", "12 項倫理原則", "＋ AI Practice Guide（6 階段）", "blue"),
        ("做了什麼", "社會影響", "正面效益 vs 就業與不平等", "amber"),
    ]
    xs = [48, 322, 596]
    for (title, l1, l2, stage), x in zip(cards, xs):
        s.rect(x, 200, 256, 96, fill=CARD2, stroke=C[stage] + "66", rx=12)
        s.text(x + 20, 234, title, 15.5, C[stage], "700")
        s.text(x + 20, 262, l1, 12.5, TXT)
        s.text(x + 20, 284, l2, 11.5, MUT)

    s.bus_out((450, 164), [(176, 200), (450, 200), (724, 200)])
    s.bus_in([(176, 296), (450, 296), (724, 296)], (450, 340))

    s.box(170, 340, 560, 56, "四大倫理議題　＋　香港 PDPO 六原則", None, "violet", tsize=14.5)
    s.arrow(450, 396, 450, 426)
    s.box(170, 428, 560, 56, "六項建議　→　結論：創新與倫理責任必須平衡", None, "rose", tsize=14.5)

    s.text(48, 524, "三條分支各自展開，最後匯流成一句話：創新與倫理責任必須平衡。", 13, MUT)


FIGS = [
    ("responsibleai-outline", "responsible-ai-notes", 1, 1000, 770,
     "Responsible AI：全書大綱樹", "六個主分支與各自的考點關鍵字", fig_outline,
     "圖 19：全書大綱樹——為什麼要做（Challenges on AI）、怎麼做（12 項原則＋6 階段）、"
     "四大倫理議題、香港 PDPO、社會影響，收在「創新與倫理責任必須平衡」。｜手繪 SVG 圖表"),
    ("responsibleai-summary", "responsible-ai-notes", 2, 900, 540,
     "全書收束：一張圖看完", "三個手段分支匯流成一個結論", fig_summary,
     "圖 20：全書收束——為什麼做／怎麼做／做了什麼三分支，匯流到「四大倫理議題＋PDPO 六原則」，"
     "再收成六項建議與結論。｜手繪 SVG 圖表"),
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
