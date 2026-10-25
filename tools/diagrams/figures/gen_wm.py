# -*- coding: utf-8 -*-
"""xr-vs-world-model（_posts 文章）：3 張內嵌 SVG 圖表。

  圖 1  wm-two-routes        XR 建模／重建  vs  世界模型／物理 AI
  圖 2  wm-three-functions   Renderer / Simulator / Planner，模擬器是樞紐
  圖 3  wm-bidirectional     XR ↔ 世界模型的雙向饋送迴路

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


def fig_two_routes(s):
    """圖 1：兩條技術路線的目標／資料／輸出／評準對照。"""
    # ---- 左欄 ----
    s.rect(48, 106, 416, 470, fill=CARD2, stroke=C["teal"] + "66", rx=14)
    s.text(76, 146, "XR 建模／3D 重建", 18, TXT, "700")
    s.text(76, 172, "把世界呈現給人", 12.5, C["teal"])
    s.text(76, 200, "核心目標", 12, MUT)
    s.text(76, 222, "讓人類在裝置中看到、走進、", 13, TXT)
    s.text(76, 242, "操作一個可信的 3D 空間", 13, TXT)
    s.text(76, 274, "資料來源", 12, MUT)
    s.text(76, 296, "360 相機、LiDAR、深度相機、", 13, TXT)
    s.text(76, 316, "CAD、遊戲引擎資產", 13, TXT)
    s.text(76, 348, "輸出", 12, MUT)
    s.text(76, 370, "全景影像、mesh、點雲、", 13, TXT)
    s.text(76, 390, "Gaussian Splat、碰撞體、材質", 13, TXT)
    s.text(76, 422, "評估標準", 12, MUT)
    s.text(76, 444, "視覺一致性、幾何準確度、延遲、", 13, TXT)
    s.text(76, 464, "舒適度、互動穩定性", 13, TXT)
    s.text(76, 494, "典型用途", 12, MUT)
    s.text(76, 516, "VR／AR、數位孿生、遊戲、培訓", 13, TXT)
    s.text(76, 548, "重建是手段，不是世界模型的定義", 12.5, C["teal"])

    # ---- 右欄 ----
    s.rect(496, 106, 416, 470, fill=CARD2, stroke=C["violet"] + "66", rx=14)
    s.text(524, 146, "世界模型／物理 AI", 18, TXT, "700")
    s.text(524, 172, "把世界變成 AI 可預測的狀態", 12.5, C["violet"])
    s.text(524, 200, "核心目標", 12, MUT)
    s.text(524, 222, "讓 AI 在內部預測：若採取某動作，", 13, TXT)
    s.text(524, 242, "世界會怎樣變化", 13, TXT)
    s.text(524, 274, "資料來源", 12, MUT)
    s.text(524, 296, "影片、機器人操作軌跡、", 13, TXT)
    s.text(524, 316, "感測器狀態、模擬環境", 13, TXT)
    s.text(524, 348, "輸出", 12, MUT)
    s.text(524, 370, "潛在狀態、未來觀測、動作後結果、", 13, TXT)
    s.text(524, 390, "可規劃的策略", 13, TXT)
    s.text(524, 422, "評估標準", 12, MUT)
    s.text(524, 444, "因果正確性、長時程預測、少幻覺、", 13, TXT)
    s.text(524, 464, "任務成功率、sim2real 遷移", 13, TXT)
    s.text(524, 494, "典型用途", 12, MUT)
    s.text(524, 516, "機器人、自動駕駛、具身智能、規劃", 13, TXT)
    s.text(524, 548, "預測未來（動作→結果）才是核心", 12.5, C["violet"])

    # ---- 中間分界 ----
    s.line(480, 130, 480, 552, "#30363d", 1.5)
    s.text(480, 596, "技術目標不同，卻互供資料與場景", 13.5, MUT, "normal", "middle")

    # ---- 底部 ----
    s.text(48, 640, "4D Gaussian Splatting 是世界模型可用的空間表徵之一，", 13.5, TXT)
    s.text(48, 662, "但 4DGS 本身不是世界模型——重建場景是手段，預測未來才是定義。", 13.5, TXT)


def fig_three_functions(s):
    """圖 2：Renderer / Simulator / Planner，以及模擬器為何是樞紐。"""
    # ---- POMDP 迴路（上方）----
    s.text(48, 118, "POMDP 迴路：三者都是這個迴路的不同投影", 13.5, MUT)

    s.box(48, 138, 176, 58, "Agent", "人、機器人、軟體", "teal")
    s.arrow(228, 167, 300, 167, C["teal"])
    s.box(304, 138, 176, 58, "Action", "動作改變世界", "amber")
    s.arrow(484, 167, 556, 167, C["amber"])
    s.box(560, 138, 176, 58, "State", "完整但不可見的現實", "blue")
    s.arrow(648, 200, 648, 226, C["blue"])
    s.box(560, 230, 176, 58, "Observation", "光子、感測器、像素", "violet")
    s.arrow(556, 259, 484, 259, C["violet"])
    s.box(304, 230, 176, 58, "Policy", "由觀測決定下一步", "green")
    s.arrow(300, 259, 228, 259, C["green"])
    s.arrow(136, 230, 136, 200, C["green"])
    s.text(480, 312, "世界模型 = 學會預測這條迴路上的一環", 13, MUT, "normal", "middle")

    # ---- 三種功能 ----
    s.text(48, 356, "三種功能：契約（contract）不同", 15, TXT, "700")

    s.rect(48, 374, 268, 214, fill=CARD, stroke=C["teal"] + "66", rx=12)
    s.text(72, 406, "Renderer", 16, C["teal"], "700")
    s.text(72, 430, "輸出給人看的像素", 12.5, TXT)
    s.text(72, 456, "契約：視覺保真度", 12.5, MUT)
    s.text(72, 484, "最商業化、最受關注", 12.5, MUT)
    s.text(72, 506, "但為視覺可信最佳化，", 12.5, MUT)
    s.text(72, 526, "無法用來訓練機器人", 12.5, MUT)
    s.text(72, 564, "例子：影片生成模型、Genie 3、RTFM", 12, C["teal"])

    s.rect(332, 374, 268, 214, fill=CARD, stroke=C["amber"] + "66", rx=12)
    s.text(356, 406, "Simulator", 16, C["amber"], "700")
    s.text(356, 430, "輸出可信的 state", 12.5, TXT)
    s.text(356, 456, "契約：結構與物理保真", 12.5, MUT)
    s.text(356, 484, "最少人注意，卻最具後果", 12.5, C["amber"])
    s.text(356, 506, "同時服務兩種消費者：", 12.5, MUT)
    s.text(356, 526, "人類專業與程式（RL、控制器）", 12.5, MUT)
    s.text(356, 564, "例子：Marble 的 collider mesh + 物理引擎", 12, C["amber"])

    s.rect(616, 374, 268, 214, fill=CARD, stroke=C["violet"] + "66", rx=12)
    s.text(640, 406, "Planner", 16, C["violet"], "700")
    s.text(640, 430, "輸出動作", 12.5, TXT)
    s.text(640, 456, "契約：動作是否正確", 12.5, MUT)
    s.text(640, 484, "最迷人、也最初期", 12.5, MUT)
    s.text(640, 506, "閉合感知—行動迴路", 12.5, MUT)
    s.text(640, 526, "多數 demo 仍受限於實驗室", 12.5, MUT)
    s.text(640, 564, "例子：VLA、世界行動模型（WAM）", 12, C["violet"])

    # ---- 結論帶 ----
    s.rect(48, 610, 836, 92, fill=CARD2, stroke=C["green"] + "66", rx=12)
    s.text(72, 640, "模擬器是樞紐（the linchpin）", 15, C["green"], "700")
    s.text(72, 664, "語言是世界抽象，像素是世界投影，而幾何、物理與動力學才是世界本身。", 13, TXT)
    s.text(72, 686, "只學會渲染或只學會規劃的模型，兩樣都做不來。", 13, TXT)
def fig_bidirectional(s):
    """圖 3：XR 與世界模型的雙向饋送，以及短期交會點。"""
    # ---- 左：XR 成就世界模型 ----
    s.rect(48, 116, 380, 250, fill=CARD2, stroke=C["teal"] + "66", rx=14)
    s.text(74, 152, "XR 成就世界模型", 17, C["teal"], "700")
    s.text(74, 176, "資料與場景的來源", 12.5, MUT)
    s.card(74, 194, 328, 46, "VR／AR 與遙操作", "帶位姿、深度、互動標記的資料", "teal")
    s.card(74, 248, 328, 46, "掃描重建與數位孿生", "大量真實空間的對應關係", "blue")
    s.card(74, 302, 328, 46, "人類在其中的操作", "動作—結果對的天然來源", "green")

    # ---- 右：世界模型成就 XR ----
    s.rect(488, 116, 380, 250, fill=CARD2, stroke=C["violet"] + "66", rx=14)
    s.text(514, 152, "世界模型成就 XR", 17, C["violet"], "700")
    s.text(514, 176, "即時想像與互動結果", 12.5, MUT)
    s.card(514, 194, 328, 46, "即時想像物件反應", "不只渲染預先建好的場景", "violet")
    s.card(514, 248, 328, 46, "填補未拍攝區域", "生成一致的新視角", "rose")
    s.card(514, 302, 328, 46, "互動結果可驗證", "動作條件化的未來", "amber")

    # ---- 中間雙向箭頭 ----
    s.arrow(432, 200, 484, 200, C["teal"], 3)
    s.arrow(484, 282, 432, 282, C["violet"], 3)
    s.text(458, 180, "資料", 11.5, C["teal"], "normal", "middle")
    s.text(458, 306, "模型", 11.5, C["violet"], "normal", "middle")

    # ---- 短期交會點 ----
    s.text(48, 412, "短期最實際的交會點：三層分工", 16, TXT, "700")
    s.text(48, 436, "不是誰取代誰，而是各自負責一層", 12.5, MUT)

    s.card(48, 452, 268, 92, "視覺與幾何底座", "4DGS／NeRF 類重建", "teal")
    s.card(330, 452, 268, 92, "可控接觸與碰撞", "物理引擎（碰撞體、材質）", "amber")
    s.card(612, 452, 268, 92, "真實動態與長時程", "世界模型補足預測", "violet")

    s.arrow(320, 498, 326, 498, RAIL)
    s.arrow(602, 498, 608, 498, RAIL)

    # ---- 產品級證據 ----
    s.rect(48, 566, 836, 132, fill=CARD, stroke=C["amber"] + "66", rx=12)
    s.text(72, 596, "2026 年已落地：Spark 2.0（世界模型 → XR 的箭頭）", 14.5, C["amber"], "700")
    s.text(72, 622, "3DGS renderer，跑在 THREE.js / WebGL2，任何瀏覽器裝置（含 iOS、Android、VR）", 13, TXT)
    s.text(72, 644, "Level-of-Detail 系統隨移動調整細節並串流；.RAD 格式支援漸進式精緻化", 13, TXT)
    s.text(72, 666, "固定 GPU 記憶體即可走訪「無限」splat 世界；實例逾 1 億 splats，", 13, TXT)
    s.text(72, 688, "實景掃描 4,000 萬 splats 在手機順暢，且相容 Quest 與 Vision Pro", 13, TXT)


FIGS = [
    ("wm-two-routes", "xr-vs-world-model", 1, 940, 700,
     "XR 建模／重建 vs 世界模型：兩條路線的完整對照",
     "同一個世界，兩種不同的契約與評準",
     fig_two_routes,
     "圖 1：兩條技術路線的目標、資料來源、輸出與評估標準｜手繪 SVG 圖表"),
    ("wm-three-functions", "xr-vs-world-model", 2, 940, 730,
     "世界模型的三種功能：Renderer、Simulator、Planner",
     "三者都是 POMDP 迴路的投影，但契約不同",
     fig_three_functions,
     "圖 2：POMDP 迴路與世界模型的三種功能，模擬器是樞紐｜手繪 SVG 圖表"),
    ("wm-bidirectional", "xr-vs-world-model", 3, 940, 720,
     "XR 與世界模型：雙向饋送與短期交會點",
     "互供資料與場景，技術目標不同",
     fig_bidirectional,
     "圖 3：XR 與世界模型的雙向饋送，以及三層分工的交會點｜手繪 SVG 圖表"),
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
