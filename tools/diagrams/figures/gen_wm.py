# -*- coding: utf-8 -*-
"""xr-vs-world-model（_posts 文章）：3 張內嵌 SVG 圖表。

  圖 1  wm-three-3d          三種「做出 3D」的方式：物理引擎建模 / 360 縫合 / 4DGS
  圖 2  wm-human-vs-ai       人類看圖、AI 看特徵向量；解碼只是為了讓人類能監督
  圖 3  wm-two-branches      因果理解與場景理解兩分支的驗證方式，以及 1＋2 融合

這篇是 source/_posts/ 的一般文章（沒有 index.html 孿生檔），所以嵌入步驟用同目錄的
embed_wm.py，而不是 tools/diagrams/embed_figs.py（後者只吃 source/<note>/ 筆記）。

House style 一律走 svglib.py（顏色不要寫死）；標籤一律真正的 <text>，方便 QA 量測。
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from svglib import Svg, C, MUT, TXT, CARD, CARD2  # noqa: E402

HERE = _HERE
RAIL = "#7d8590"


def fig_three_3d(s):
    """圖 1：三種做出 3D 的方式，各有各的取捨。"""
    cols = [
        (48, "物理引擎建模", "amber",
         ["自帶力學方程、材質參數", "可自由走動、物件可互動"],
         ["仿真環境 ≠ 真實場景", "機器人因此才有 sim2real 問題"]),
        (340, "360 圖像縫合 ＋ 視覺錯位", "rose",
         ["就是拍到什麼就是什麼", "視覺上最接近真實"],
         ["只能看到全景相機走過的路徑", "離開拍攝路徑就沒東西看"]),
        (632, "4D Gaussian Splatting", "teal",
         ["把真實拍攝還原得像建模", "可自由走動，不受相機路徑侷限"],
         ["靠的是「場景理解」而非真建模", "仍需物理引擎接手碰撞與互動"]),
    ]
    for x, title, col, pros, cons in cols:
        s.rect(x, 118, 264, 330, fill=CARD2, stroke=C[col] + "66", rx=12)
        s.text(x + 20, 152, title, 15.5, C[col], "700")
        s.text(x + 20, 180, "優點", 12, MUT)
        for i, p in enumerate(pros):
            s.text(x + 20, 204 + i * 22, "・" + p, 12.5, TXT)
        s.text(x + 20, 264, "代價", 12, MUT)
        for i, c in enumerate(cons):
            s.text(x + 20, 288 + i * 22, "・" + c, 12.5, MUT)

    s.text(48, 482, "世界模型走的是第三條：", 15, TXT, "700")
    s.text(48, 508, "比仿真環境真實（直接來自真實拍攝），又不被相機路線侷限（AI 能想像沒走過的路）。", 13.5, TXT)
    s.text(48, 534, "但它產出的仍是「理解」——不是手算的力學結果，也不是像素級重建。", 13.5, MUT)

    s.rect(48, 566, 848, 108, fill=CARD, stroke=C["teal"] + "66", rx=12)
    s.text(72, 598, "為什麼 4DGS 和 360 縫合不是同一個東西", 14.5, C["teal"], "700")
    s.text(72, 624, "360 縫合把多張照片拼成一張全景圖，畫面裡沒有深度，也沒有「這裡本來可能是什麼」。", 13, TXT)
    s.text(72, 648, "4DGS 從多視角觀測學出一個可從新視角渲染的 3D 表徵，", 13, TXT)
    s.text(72, 670, "因此相機沒走過的路也可以渲染——那是從「場景理解」生出來的，不是拼圖補的。", 13, TXT)

def fig_human_vs_ai(s):
    """圖 2：人類看圖，AI 看特徵向量；解碼只為讓人類能監督。"""
    # 左：人類
    s.rect(48, 116, 396, 268, fill=CARD2, stroke=C["teal"] + "66", rx=14)
    s.text(74, 152, "人類", 17, C["teal"], "700")
    s.text(74, 178, "看的是圖本身", 12.5, MUT)
    s.box(74, 196, 344, 52, "影像", "眼睛收到的光子", "teal")
    s.arrow(246, 252, 246, 274, RAIL)
    s.box(74, 278, 344, 52, "場景", "杯子在那裡、可以拿起來", "blue")
    s.text(74, 362, "看得懂，所以能判斷對不對。", 12.5, MUT)

    # 右：AI
    s.rect(480, 116, 396, 268, fill=CARD2, stroke=C["violet"] + "66", rx=14)
    s.text(506, 152, "AI", 17, C["violet"], "700")
    s.text(506, 178, "看的是特徵向量", 12.5, MUT)
    s.box(506, 196, 344, 52, "影像", "輸入的原始訊號", "teal")
    s.arrow(678, 252, 678, 274, RAIL)
    s.box(506, 278, 344, 52, "特徵向量", "人看不懂，但那是 AI 的「理解」", "violet")
    s.text(506, 362, "看不懂，但那是它做決策依據的東西。", 12.5, MUT)

    # 解碼器
    s.rect(48, 412, 828, 150, fill=CARD, stroke=C["amber"] + "66", rx=12)
    s.text(72, 444, "解碼器：唯一的目的，是讓人類能看懂並監督", 15, C["amber"], "700")
    s.text(72, 470, "特徵向量 → 解碼回影像或文字，人類才能確認 AI 的理解跟自己的理解有沒有對齊。", 13, TXT)
    s.text(72, 496, "對 AI 本身而言，解碼是多餘的——它推理時用的是特徵空間，不是像素。", 13, TXT)
    s.text(72, 528, "所以 Yann LeCun 走隱式世界模型：人類幹嘛看懂？AI 看懂就好。", 13.5, C["amber"])
    s.text(72, 552, "AMI 論文：JEPA「在表徵空間做預測，讓編碼器能濾掉對任務無關的特徵」。", 12.5, MUT)

def fig_two_branches(s):
    """圖 3：因果理解與場景理解兩分支，各自的驗證方式，以及融合條件。"""
    s.rect(48, 116, 404, 268, fill=CARD2, stroke=C["violet"] + "66", rx=14)
    s.text(74, 152, "分支一：因果理解", 17, C["violet"], "700")
    s.text(74, 178, "AI 知道手去碰杯子，杯子會往前動", 12.5, MUT)
    s.box(74, 196, 352, 52, "動作 a", "推一下、抓起來、放開", "amber")
    s.arrow(250, 252, 250, 274, RAIL)
    s.box(74, 278, 352, 52, "預測的未來狀態", "還沒發生的事", "violet")
    s.text(74, 362, "驗證：能不能正確預測未來，而沒有幻覺。", 12.5, TXT)

    s.rect(468, 116, 428, 268, fill=CARD2, stroke=C["teal"] + "66", rx=14)
    s.text(494, 152, "分支二：場景理解", 17, C["teal"], "700")
    s.text(494, 178, "AI 知道相機沒走過的那條路長什麼樣", 12.5, MUT)
    s.box(494, 196, 376, 52, "目前位置與已見場景", "從多視角觀測學到的表徵", "blue")
    s.arrow(682, 252, 682, 274, RAIL)
    s.box(494, 278, 376, 52, "沒拍過的路線", "新視角、新區域", "teal")
    s.text(494, 362, "驗證：相機沒拍到的路線，能不能正確想像出來。", 12.5, TXT)

    s.arrow(252, 392, 252, 424, C["violet"], 3)
    s.arrow(682, 392, 682, 424, C["teal"], 3)
    s.text(266, 414, "因果", 12, C["violet"])
    s.text(696, 414, "場景", 12, C["teal"])

    s.rect(48, 428, 848, 168, fill=CARD, stroke=C["green"] + "66", rx=12)
    s.text(72, 460, "成熟條件：兩者融合，而且沒有幻覺、兩者不衝突", 16, C["green"], "700")
    s.text(72, 490, "只懂因果 → 會推得動杯子，但不知道杯子長什麼樣、擺在哪裡。", 13, TXT)
    s.text(72, 514, "只懂場景 → 知道場景長什麼樣，但不知道推一下會怎樣。", 13, TXT)
    s.text(72, 544, "兩者融合後，AI 依當前位置同時想像出場景與因果，才算真正成熟的理解。", 13.5, TXT)
    s.text(72, 574, "「沒有幻覺」與「不衝突」是門檻：預測得漂亮但物理錯，或場景對但因果打架，都還沒到位。", 12.5, MUT)


def fig_capability_matrix(s):
    """圖 4：三種做 3D 的方式，各自能驗證什麼、不能驗證什麼。

    This is the sharpest version of the argument: the table in the article
    says what each approach *is*; this says what each approach can be
    *held to*.
    """
    cols = [
        ("物理引擎建模", "amber",
         ["物理正確性", "與真實的差距"],
         "沒有「未來」可驗證：\n場景是從零算的，\n不是你推算出來的"),
        ("360 縫合 ＋ 視覺錯位", "rose",
         ["看見的部分是否真實"],
         "相機沒走過的路線\n沒有答案——這是它的\n能力邊界，不是缺陷"),
        ("4DGS 與世界模型", "teal",
         ["相機沒拍過的路線\n能不能被想像出來"],
         "推一下杯子會怎樣？\n這要靠因果理解，\n不是靠場景表徵"),
    ]

    x0, y0 = 48, 156
    colw = 264
    for i, (name, col, can, cannot) in enumerate(cols):
        x = x0 + i * (colw + 18)
        hot = (col == "teal")
        s.rect(x, y0 - 52, colw, 44, fill=CARD2,
               stroke=C[col] + ("99" if hot else "66"), rx=10)
        s.text(x + colw / 2, y0 - 24, name, 14, C[col], "700", "middle")

        s.text(x + 18, y0 + 20, "能驗證", 12, MUT)
        for k, ln in enumerate(can):
            s.text(x + 18, y0 + 44 + k * 20, ln, 12.5,
                   C[col] if hot else TXT, "700" if hot else "normal")

        s.text(x + 18, y0 + 108, "不能驗證", 12, MUT)
        for k, ln in enumerate(cannot.split("\n")):
            s.text(x + 18, y0 + 132 + k * 20, ln, 12, MUT)

    ybot = y0 + 226
    s.rect(x0, ybot, 848, 104, fill=CARD, stroke=C["teal"] + "66", rx=12)
    s.text(x0 + 24, ybot + 32, "三種方式各自能證明的東西不同，缺的那一塊誰也補不上", 14.5,
           C["teal"], "700")
    s.text(x0 + 24, ybot + 58,
           "物理引擎證明物理對，360 縫合證明拍到的部分真，4DGS 證明沒拍到的地方能想像。",
           13, TXT)
    s.text(x0 + 24, ybot + 82,
           "但「推一下杯子會怎樣」只有因果理解能回答——這就是第三欄和第三節分支一的差別。",
           12.5, MUT)


def fig_2026_timeline(s):
    """圖 5：2026 年三件事的時序與它們各自證實了什麼。"""
    items = [
        ("7/21", "併購 SceniX", "把機器人與模擬\n拉進同一條線", "violet"),
        ("7/28", "R2S2R 成果", "模擬能預測真實\npolicy 排名", "amber"),
        ("9/01", "新一代 Atlas", "從重建走向\n想像未看見的場景", "teal"),
        ("9/28", "併入 AMD", "世界模型與硬體\n垂直整合", "green"),
    ]

    y = 210
    # Draw the rail in segments that stop short of the badges, so the line
    # never runs through a circle.
    xs = [120 + i * 246 for i in range(4)]
    for i in range(3):
        s.line(xs[i] + 22, y, xs[i + 1] - 22, y, "#30363d", 3)

    for i, (date, title, body, col) in enumerate(items):
        x = xs[i]
        s.badge(x, y, str(i + 1), C[col], 17, 14)
        s.text(x, y - 46, date, 15, C[col], "700", "middle")
        s.text(x, y - 22, title, 14, TXT, "700", "middle")
        for k, ln in enumerate(body.split("\n")):
            s.text(x, y + 34 + k * 20, ln, 12, MUT, "normal", "middle")

    s.rect(48, 330, 848, 196, fill=CARD2, stroke=C["teal"] + "66", rx=12)
    s.text(72, 364, "四件事合起來指向同一件事", 15.5, C["teal"], "700")
    s.text(72, 394,
           "1. 模擬器是樞紐：從真實任務重建模擬，再用它預測真實世界的 policy 表現。", 13, TXT)
    s.text(72, 420,
           "2. 驗證的是「未來」而不是「場景」——2,000 次模擬預測 100 次真實試驗的排名。", 13, TXT)
    s.text(72, 446,
           "3. 產出的是想像：Atlas 能生成參考圖中不可見的場景，不是重建看見的部分。", 13, TXT)
    s.text(72, 472,
           "4. 瓶頸轉移到硬體：模型與算力的關係，決定了世界模型能走多遠。", 13, TXT)
    s.text(72, 504,
           "四件事都不是在證明「重建得更像」，而是在證明「預測得更準」。",
           13, C["teal"], "700")


FIGS = [
    ("wm-three-3d", "xr-vs-world-model", 1, 940, 700,
     "三種「做出 3D」的方式：物理引擎、360 縫合、4DGS",
     "世界模型走的是第三條",
     fig_three_3d,
     "圖 1：物理引擎建模、360 圖像縫合與 4D Gaussian Splatting 三種做 3D 的方式及其取捨｜手繪 SVG 圖表"),
    ("wm-human-vs-ai", "xr-vs-world-model", 2, 940, 600,
     "人類看圖，AI 看特徵向量",
     "解碼只是為了讓人類能看懂並監督",
     fig_human_vs_ai,
     "圖 2：人類看圖而 AI 看特徵向量，解碼器的唯一用途是讓人類能監督｜手繪 SVG 圖表"),
    ("wm-two-branches", "xr-vs-world-model", 3, 940, 620,
     "世界模型的兩個分支：因果理解與場景理解",
     "各自的驗證方式，以及融合的門檻",
     fig_two_branches,
     "圖 3：因果理解與場景理解兩分支的驗證方式，以及兩者融合的成熟條件｜手繪 SVG 圖表"),
    ("wm-capability-matrix", "xr-vs-world-model", 4, 940, 500,
     "三種做 3D 的方式，各自能驗證什麼",
     "缺的那一塊誰也補不上",
     fig_capability_matrix,
     "圖 4：物理引擎、360 縫合與 4DGS 各自能驗證與不能驗證的部分｜手繪 SVG 圖表"),
    ("wm-2026-timeline", "xr-vs-world-model", 5, 940, 560,
     "2026 年：四件事把框架推到了實證階段",
     "沒有一件是在證明重建得更像",
     fig_2026_timeline,
     "圖 5：2026 年 SceniX 併購、R2S2R、新一代 Atlas 與併入 AMD 的時序｜手繪 SVG 圖表"),
]


def build(slug):
    for s, _n, _i, w, h, title, sub, fn, _cap in FIGS:
        if s == slug:
            svg = Svg(w, h, "%s｜%s" % (title, sub), title, sub)
            fn(svg)
            out = os.path.join(HERE, slug + ".svg")
            svg.save(out, os.path.join(r"C:\Users\princ\blog\_work\diagrams",
                                      "_m_%s.html" % slug))
            bad = svg.check()
            if bad:
                print("COLLISION in %s: %d" % (slug, len(bad)))
                for b in bad:
                    print("   ", b)
            else:
                print("OK %s -> %s" % (slug, out))
            return svg
    raise KeyError(slug)


if __name__ == "__main__":
    for _slug, _n, _i, _w, _h, _t, _sub, _fn, _c in FIGS:
        build(_slug)
