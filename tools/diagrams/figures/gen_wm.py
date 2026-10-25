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
