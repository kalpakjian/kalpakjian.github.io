# -*- coding: utf-8 -*-
"""gpu-unlock 專題頁：2 張內嵌 SVG 圖表。

  圖 1  dossier-lineage   專案血緣：從 CMP 170HX 到 Ada 分支，以及兩個 Linux 模組的差異
  圖 2  dossier-map       四篇文章速查：類型、對象、關鍵數字、一句話結論

House style 一律走 svglib.py（顏色不要寫死）；標籤一律真正的 <text>，方便 QA 量測。
這是 source/gpu-unlock/index.md 專題頁（Hexo 渲染），嵌入用同目錄的 embed_dossier.py。
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from svglib import Svg, C, MUT, TXT, CARD, CARD2, MONO  # noqa: E402

HERE = _HERE
RAIL = "#7d8590"

# ---------------------------------------------------------------------------
# 圖 1：專案血緣
# ---------------------------------------------------------------------------
# (名稱, 誰做的, 說明第一行, 說明第二行)
LINEAGE = [
    ("cmpunlocker", "amoghmunikote",
     "把 8／10 GB 的 CMP 170HX 解鎖成 64／40 GB",
     "曾被 LTT 報導過的那一支"),
    ("cmp90hx-unlock", "WildFlash1st",
     "貢獻 GA102 的 V67 鏈",
     "Ada 版沿用同一條鏈"),
    ("gpu-unlock", "Zagitta",
     "第一個 Linux 核心模組版本",
     "GA10x 數十個裝置 ID，靠社群眾包"),
    ("gpu-unlock-ada", "JustAResearcher",
     "本專題主軸；白名單 4 個 Ada ID",
     "後兩者需實驗旗標，證據做成配對實測"),
]

# (左欄＝gpu-unlock, 右欄＝gpu-unlock-ada, 階段色)
COMPARE_ROWS = [
    ("GA102／103／104／106 數十個 ID", "僅 4 個 Ada ID", "teal"),
    ("4070 Ti SUPER 需實驗旗標", "4090 只要 targets 一項", "teal"),
    ("沒有診斷工具", "有唯讀讀回與指令率探針", "amber"),
    ("靠社群眾包相容性報告", "配對實測＋數值驗證＋遙測", "amber"),
]


def fig_lineage(s):
    """圖 1：專案血緣與兩個 Linux 模組的差異。"""
    x0, w, h = 48, 330, 70
    for i, (name, who, l1, l2) in enumerate(LINEAGE):
        yy = 132 + i * 88
        col = C["teal"] if i >= 2 else C["gray"]
        s.rect(x0, yy, w, h, fill=CARD, stroke=col + "66", rx=10)
        s.text(x0 + 16, yy + 26, name, 13.5, col, "700", "start", MONO)
        s.text(x0 + w - 16, yy + 26, who, 10.5, MUT, "normal", "end")
        s.text(x0 + 16, yy + 46, l1, 10.5, MUT)
        s.text(x0 + 16, yy + 60, l2, 10.5, MUT)
        if i:
            s.arrow(x0 + w / 2.0, yy - 18, x0 + w / 2.0, yy - 4, RAIL)

    rx, rw = 420, 532
    s.rect(rx, 132, rw, 338, fill=CARD2, stroke=C["blue"] + "55", rx=14)
    s.text(rx + 20, 160, "兩個 Linux 模組的關鍵差異", 14, C["blue"], "700")
    s.text(rx + 20, 182, "同一個 exploit，不同的涵蓋範圍與證據策略", 11, MUT)

    for i, (left, right, stage) in enumerate(COMPARE_ROWS):
        yy = 202 + i * 54
        col = C[stage]
        s.rect(rx + 16, yy, 250, 44, fill=CARD, stroke=col + "55", rx=8)
        s.rect(rx + 274, yy, 242, 44, fill=CARD, stroke=col + "55", rx=8)
        s.text(rx + 28, yy + 18, "gpu-unlock", 10, MUT)
        s.text(rx + 28, yy + 35, left, 11, TXT, "700")
        s.text(rx + 286, yy + 18, "gpu-unlock-ada", 10, MUT)
        s.text(rx + 286, yy + 35, right, 11, TXT, "700")

    s.text(rx + 20, 432, "共同的根：已簽章 NVIDIA booter 的緩衝區溢位 + ROP", 12, C["rose"], "700")
    s.text(rx + 20, 452, "解開 FEAT_OVR_PLM 的寫入保護後，寫 SS0／SS1 即可改成全速", 10.5, MUT)

    s.rect(48, 486, 904, 62, fill=CARD2, stroke=C["teal"] + "55", rx=10)
    s.text(68, 512,
           "Windows 那條線是旁支：TOTORONG/AD103_win_unlocker 的 UEFI 實驗提供 AD102 payload，", 13, TXT)
    s.text(68, 534,
           "Ada 版把它整進 Linux 模組；impacifist/Windows-GPU-UNLOCK 則把它做成獨立的 Windows 工具。",
           13, MUT)

# ---------------------------------------------------------------------------
# 圖 2：四篇文章速查
# ---------------------------------------------------------------------------
# (類型, 標題, 對象, 關鍵數字, 一句話結論, 階段色)
ARTICLES = [
    ("事實查核", "RTX 30 系 gpu-unlock",
     "GA10x 數十個 ID",
     "BF16 +25～81%",
     "「一律翻倍」不成立；各型號差三倍", "blue"),
    ("事實查核", "RTX 40 系 Tensor 解鎖",
     "4 個 Ada ID",
     "指令率 2×、GEMM +12～34%",
     "「全系列」不成立；FP8 幾乎沒變", "blue"),
    ("操作筆記", "RTX 3080 12GB",
     "10de:220a",
     "FP16 +69%、BF16 +73%",
     "只吃 FP16／BF16 矩陣乘法", "teal"),
    ("操作筆記", "RTX 4090",
     "10de:2684",
     "指令率 1.998×",
     "不用實驗旗標；量化權重吃不到", "teal"),
]


def fig_map(s):
    """圖 2：四篇文章速查卡。"""
    cw, ch = 440, 178
    xs = [48, 512]
    ys = [132, 330]
    for i, (kind, title, target, number, gist, stage) in enumerate(ARTICLES):
        x = xs[i % 2]
        y = ys[i // 2]
        col = C[stage]
        s.rect(x, y, cw, ch, fill=CARD, stroke=col + "66", rx=12)
        s.rect(x, y, 6, ch, fill=col, rx=3)
        s.text(x + 22, y + 28, kind, 10.5, col, "700")
        s.text(x + 22, y + 52, title, 15, TXT, "700")
        s.text(x + 22, y + 74, "對象：" + target, 11, MUT)
        s.text(x + 22, y + 96, "關鍵數字：" + number, 11.5, col, "700")
        s.line(x + 22, y + 110, x + cw - 22, y + 110, "#30363d", 1.2)
        s.text(x + 22, y + 134, gist, 11.5, TXT)
        s.text(x + 22, y + 156, "→ 讀這篇", 11, col, "700")

    s.rect(48, 524, 904, 92, fill=CARD2, stroke=C["amber"] + "55", rx=10)
    s.text(68, 546, "四篇的共同結論：解鎖是真的，媒體的關鍵字是假的。", 13.5, TXT, "700")
    s.text(68, 568,
           "① 「全系列」不成立——白名單只有少數型號", 12, MUT)
    s.text(68, 586,
           "② 「翻倍」是指令發射率；真實 GEMM 只有 +12～81%", 12, MUT)
    s.text(68, 604,
           "③ 「所有 AI 負載都變快」不成立——INT8／4-bit／3-bit 量化完全沒變", 12, MUT)


FIGS = [
    ("dossier-lineage", 1000, 568,
     "gpu-unlock 專案血緣：從 cmpunlocker 到 cmp90hx-unlock、gpu-unlock、gpu-unlock-ada，"
     "以及 Windows 那條旁支，兩個 Linux 模組在涵蓋範圍與證據策略上的關鍵差異",
     "專案血緣", "同一個 exploit，兩種做法", fig_lineage,
     "圖 1：專案血緣——共同的根都是已簽章 NVIDIA booter 的緩衝區溢位；"
     "Ampere 版走「廣範圍、靠社群眾包」，Ada 版走「窄範圍、做配對實測」。｜手繪 SVG 圖表"),
    ("dossier-map", 1000, 620,
     "gpu-unlock 專題四篇文章速查：兩篇事實查核與兩篇分卡型操作筆記，"
     "各自對象、關鍵數字與一句話結論",
     "四篇速查", "先看哪一篇？", fig_map,
     "圖 2：四篇文章速查——兩篇事實查核負責「打破關鍵字」，"
     "兩篇操作筆記負責「照著做」。｜手繪 SVG 圖表"),
]


def build(slug):
    """回傳指定 slug 的 Svg 物件（embed_dossier.py 也用它產生 figure 區塊）。

    aria（給螢幕閱讀器）與可見標題分開：aria 要詳盡，可見標題必須短，
    否則 25px 的標題會超出畫布右緣（measure_text.py 會報 [EDGE]）。
    """
    for s_slug, w, h, aria, title, sub, fn, _cap in FIGS:
        if s_slug == slug:
            s = Svg(w, h, aria, title, sub)
            fn(s)
            return s
    raise SystemExit("unknown slug: %s" % slug)


def main():
    for slug, w, h, aria, title, sub, fn, _cap in FIGS:
        s = build(slug)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-40s %dx%d  %s"
              % (slug + ".svg", w, h, "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))


if __name__ == "__main__":
    main()

