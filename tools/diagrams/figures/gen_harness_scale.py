# -*- coding: utf-8 -*-
"""harness-engineering-eleven-coding-agents（_posts 文章）：1 張內嵌 SVG 圖表。

  圖 1  harness-scale-ladder   11 個系統的規模階梯：跨三個數量級，完成率卻差不多

House style 一律走 svglib.py（顏色不要寫死）；標籤一律真正的 <text>，方便 QA 量測。
這是 source/_posts/ 的一般文章，嵌入用同目錄的 embed_harness_scale.py。
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

# (階梯名, 行數範圍, 階段色, [(系統, 說明)])
TIERS = [
    ("Tiny", "≈ 5K 行", "teal",
     [("Mini-SWE-Agent", "1 工具")]),
    ("Small", "≈ 20–40K 行", "green",
     [("Mistral Vibe", "12+ 工具"), ("Aider", "13 種格式")]),
    ("Medium", "≈ 80–110K 行", "blue",
     [("OpenHands", "25+ 工具"), ("Pi", "7 工具")]),
    ("Large", "≈ 500K+ 行", "amber",
     [("Claude Code", "43 工具"), ("OpenCode", "17 工具"), ("OpenClaw", "109+ 工具")]),
    ("Very large", "≈ 600K+ 行（Codex 快照約 1.1M 行 Rust）", "rose",
     [("Codex CLI", "25–30 工具"), ("Gemini CLI", "35+ 工具"), ("Hermes", "69 工具")]),
]


def _est_w(s, size):
    """與 svglib 相同的寬度估算，用來決定 chip 寬度。"""
    return sum(size if ord(c) > 0x2E80 else size * 0.52 for c in s)


def fig_ladder(s):
    """圖 1：規模階梯——三個數量級的落差。"""
    row_h, gap = 66, 10
    top = 138

    # 左側的量級括號
    s.line(78, top, 78, top + len(TIERS) * (row_h + gap) - gap, RAIL, 2)
    s.arrow(78, top + len(TIERS) * (row_h + gap) - gap, 78, top + 12, RAIL, 2)
    s.text(78, top - 16, "規模", 12.5, C["teal"], "700", "middle")

    for ti, (tier, locs, stage, systems) in enumerate(TIERS):
        y = top + ti * (row_h + gap)
        col = C[stage]
        s.rect(110, y, 842, row_h, fill=CARD, stroke=col + "55", rx=10)
        s.rect(110, y, 5, row_h, fill=col, rx=2)
        s.text(134, y + 27, tier, 15, col, "700")
        s.text(134, y + 47, locs, 11, MUT)

        x = 380
        for name, detail in systems:
            label = "%s · %s" % (name, detail)
            w = _est_w(label, 11.5) + 26
            s.rect(x, y + 16, w, row_h - 32, fill=col + "22", stroke=col + "88", rx=8)
            s.text(x + 13, y + row_h / 2.0 + 4, label, 11.5, TXT)
            x += w + 12

    box_y = top + len(TIERS) * (row_h + gap) + 14
    s.rect(48, box_y, 904, 84, fill=CARD2, stroke=C["amber"] + "55", rx=10)
    s.text(68, box_y + 28,
           "大系統多寫的那些程式碼，大半不在 harness 上：OpenCode 去掉測試後約五分之三是 TUI、"
           "網頁、桌面與 SDK 客戶端；", 13, TXT)
    s.text(68, box_y + 50,
           "Codex 7 月版有上十萬行花在 app-server 傳輸、插件與即時語音層——"
           "這些永遠不會體現在任何 benchmark 上。", 13, MUT)
    s.text(68, box_y + 72,
           "換句話說：生產系統的品質，大多花在與「任務完成」正交的事情上。", 13, MUT)


FIGS = [
    ("harness-scale-ladder", 1000, 640,
     "11 個 coding agent 系統的規模階梯：從 Tiny 約 5K 行到 Very large 約 600K 行以上，"
     "橫跨三個數量級，但自報任務完成率都落在同一區間",
     "規模階梯", "三個數量級，卻是同一區間的完成率", fig_ladder,
     "圖 1：11 個系統的規模階梯——從 Mini-SWE-Agent 的約 5K 行到 Codex 的約 1.1M 行，"
     "橫跨三個數量級，但「做到能完成任務」的門檻很低。｜手繪 SVG 圖表"),
]


def build(slug):
    """回傳指定 slug 的 Svg 物件（embed_harness_scale.py 也用它產生 figure 區塊）。

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
