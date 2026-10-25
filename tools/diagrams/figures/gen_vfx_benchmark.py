# -*- coding: utf-8 -*-
"""comfyui-nvidia-vfx-nodes-benchmark（_posts 文章）：2 張內嵌 SVG 圖表。

  圖 1  vfx-three-layers      三層量測的落差：純 GPU 755 倍 vs 端到端 1.24 倍
  圖 2  vfx-time-breakdown    端到端 1.576 秒的時間花在哪

House style 一律走 svglib.py（顏色不要寫死）；標籤一律真正的 <text>，方便 QA 量測。
這是 source/_posts/ 的一般文章，嵌入用同目錄的 embed_vfx_benchmark.py。
"""
import math
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
# 圖 1：三層量測的落差（對數刻度）
# ---------------------------------------------------------------------------
# (情境, 原始時間說明, 倍數, 階段色)
LAYER_ROWS = [
    ("純 GPU（只算推論本身）", "830.05 ms  →  1.10 ms", 755.0, "teal"),
    ("端到端批次 16 張", "1.441 秒/張  →  0.259 秒/張", 5.56, "blue"),
    ("端到端單幀（一張一 prompt）", "1.962 秒/張  →  1.576 秒/張", 1.24, "rose"),
]

L_X0 = 300          # 1× 位置
L_TRACK = 560       # 1× → 1000×
L_ROW0 = 176
L_PITCH = 62
L_BARH = 26
L_MAX = 1000.0


def lx(v):
    """對數刻度：1× → 0，1000× → 滿格。"""
    return L_X0 + L_TRACK * math.log10(max(v, 1.0)) / math.log10(L_MAX)


def fig_layers(s):
    """圖 1：同一件事量三層，結論差 600 倍。"""
    plot_top = L_ROW0 - 14
    plot_bottom = L_ROW0 + len(LAYER_ROWS) * L_PITCH - (L_PITCH - L_BARH) + 18

    # 格線用細矩形畫（視覺上與線相同），避免與數值標籤交錯
    for v in (10, 100, 1000):
        x = lx(v)
        s.rect(x, plot_top, 1, plot_bottom - plot_top, fill="#30363d")

    s.text(L_X0, plot_top - 20, "快幾倍（對數刻度）", 12, C["teal"], "700")

    for i, (name, raw, factor, stage) in enumerate(LAYER_ROWS):
        y = L_ROW0 + i * L_PITCH
        col = C[stage]
        s.text(280, y + 15, name, 13, TXT, "700", "end")
        s.text(280, y + 32, raw, 10.5, MUT, "normal", "end")

        tip = lx(factor)
        s.rect(L_X0, y, max(4.0, tip - L_X0), L_BARH, fill=col + "55",
               stroke=col, rx=7)
        # 數值放固定右欄，避免與格線交錯
        s.text(952, y + 19, ("%.2f×" % factor) if factor < 100 else ("%d×" % factor),
               14, col, "700", "end")

    for v in (1, 10, 100, 1000):
        s.text(lx(v), plot_bottom + 26, ("%d×" % v) if v > 1 else "1×",
               11, MUT, "normal", "middle")

    box_y = plot_bottom + 46
    s.rect(48, box_y, 904, 62, fill=CARD2, stroke=C["rose"] + "55", rx=10)
    s.text(68, box_y + 26,
           "同一件事、三種量法，結論差 600 倍：只量「純 GPU」會以為快 755 倍，", 13, TXT)
    s.text(68, box_y + 48,
           "量到端到端只剩 1.24 倍。這就是為什麼基準測試一定要看端到端。", 13, MUT)


# ---------------------------------------------------------------------------
# 圖 2：端到端 1.576 秒的時間分解
# ---------------------------------------------------------------------------
# (項目, 毫秒, 階段色)
BREAKDOWN = [
    ("load() 載入 SDK 模型", 1200.0, "rose"),
    ("寫入 PNG 檔（1536×1536）", 200.0, "amber"),
    ("ComfyUI 框架與資料搬移", 170.0, "violet"),
    ("讀取 PNG 檔（768×768）", 5.0, "blue"),
    ("真正運算", 1.1, "teal"),
]
TOTAL_MS = 1576.0


def fig_breakdown(s):
    """圖 2：1.576 秒裡，真正在算圖的只有 0.07%。"""
    bar_x, bar_w = 48, 904
    bar_y, bar_h = 150, 46

    x = bar_x
    for name, ms, stage in BREAKDOWN:
        w = max(3.0, bar_w * ms / TOTAL_MS)
        col = C[stage]
        s.rect(x, bar_y, w, bar_h, fill=col + "66", stroke=col, rx=0, sw=1)
        x += w
    s.rect(bar_x, bar_y, bar_w, bar_h, fill="none", stroke="#30363d", rx=8, sw=1.5)

    s.text(48, bar_y - 14, "端到端單幀流程的時間分解（總計 1.576 秒）", 12, C["teal"], "700")

    # 圖例：色塊 + 項目 + 時間 + 佔比
    ly = bar_y + bar_h + 38
    for i, (name, ms, stage) in enumerate(BREAKDOWN):
        y = ly + i * 30
        col = C[stage]
        s.rect(56, y - 10, 16, 16, fill=col + "66", stroke=col, rx=3, sw=1.5)
        s.text(84, y + 3, name, 12.5, TXT)
        s.text(600, y + 3, ("%.1f ms" % ms) if ms < 10 else ("%.0f ms" % ms),
               12.5, col, "700", "end")
        s.text(700, y + 3, "%.2f%%" % (ms / TOTAL_MS * 100.0), 12.5, MUT, "normal", "end")
    s.text(600, ly - 22, "時間", 11, MUT, "700", "end")
    s.text(700, ly - 22, "佔比", 11, MUT, "700", "end")

    box_y = ly + len(BREAKDOWN) * 30 + 16
    s.rect(48, box_y, 904, 62, fill=CARD2, stroke=C["teal"] + "55", rx=10)
    s.text(68, box_y + 26,
           "你付了 1.576 秒，只有 0.0011 秒在算圖——真正運算在比例尺上幾乎看不到。", 13, TXT)
    s.text(68, box_y + 48,
           "用廚房比喻：專業廚房炒一盤菜只要 0.001 秒，但每次都要先預熱烤箱 1.2 秒、"
           "每盤都要裝盤封膜 0.2 秒。", 13, MUT)

FIGS = [
    ("vfx-three-layers", 1000, 470,
     "nvidia-vfx 基準測試的三層落差：純 GPU 快 755 倍、端到端批次 5.56 倍、端到端單幀只有 1.24 倍",
     "三層量測的落差", "同一件事量三層，結論差 600 倍", fig_layers,
     "圖 1：同一件事量三層的落差——純 GPU 快 755 倍、端到端批次 5.56 倍，"
     "但端到端單幀只有 1.24 倍。基準測試一定要看端到端。｜手繪 SVG 圖表"),
    ("vfx-time-breakdown", 1000, 450,
     "端到端單幀流程 1.576 秒的時間分解：load() 佔 76%、PNG 寫入 13%、框架搬移 11%，真正運算只有 0.07%",
     "時間花在哪", "總計 1.576 秒／張", fig_breakdown,
     "圖 2：1.576 秒裡真正在算圖的只有 0.07%——load() 佔 76%，"
     "所以單幀流程怎麼批次化才是重點。｜手繪 SVG 圖表"),
]


def build(slug):
    """回傳指定 slug 的 Svg 物件（embed_vfx_benchmark.py 也用它產生 figure 區塊）。

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
