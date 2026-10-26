# -*- coding: utf-8 -*-
"""flashmap-bf16-losslessness（_posts 文章）：2 張內嵌 SVG 圖表。

  圖 1  flashmap-bf16-quant-grid   真實 gap 與 bf16 可表示的格點
  圖 2  flashmap-bf16-two-shapes   逐字解碼 vs 區塊驗證：同一前綴、兩種捨入

這篇是 source/_posts/ 的一般文章（沒有 index.html 孿生檔），所以嵌入步驟用同目錄的
embed_flashmap_bf16.py，而不是 tools/diagrams/embed_figs.py（後者只吃 source/<note>/）。

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


def _panel(s, x, y, w, h, stage, title, sub=None):
    """外框面板（標題在左上角），沿用 svglib 的配色常數。"""
    s.rect(x, y, w, h, fill=CARD2, stroke=C[stage] + "55", rx=14)
    s.text(x + 20, y + 30, title, 16, TXT, "700")
    if sub:
        s.text(x + 20, y + 52, sub, 12.5, MUT)


def fig_quant_grid(s):
    """圖 1：真實 gap（fp32）與 bf16 量到的格點。

    三列都是 8B 上實際量到的分歧點（真值 → bf16 的讀數），不是示意。
    """
    X0, X1, VMAX = 372.0, 884.0, 0.5
    def px(v):
        return X0 + (X1 - X0) * v / VMAX

    ticks = [(0.0, "0"), (0.125, "0.125"), (0.25, "0.25"),
             (0.375, "0.375"), (0.5, "0.5")]

    s.text(48, 112, "每一列都是 8B 上真實量到的分歧點：圓點是真的差距，方塊是 bf16 的讀數。",
           13, MUT)

    # 刻度尺
    s.line(X0, 430, X1, 430, RAIL, 1.5)
    for v, lab in ticks:
        x = px(v)
        s.line(x, 136, x, 430, "#30363d", 1.2)
        s.text(x, 452, lab, 12.5, MUT, "normal", "middle")

    rows = [
        (176, "真值 0.06002", "第 1 題驗證誤差 0.123", 0.06002, 0.0,
         "量到 0.00000", "完全平手", "rose"),
        (286, "真值 0.24197", "第 2 題驗證誤差 0.184", 0.24197, 0.25,
         "量到 0.25000", "吸附到格點", "amber"),
        (396, "真值 0.32040", "第 7 題驗證誤差 0.476", 0.32040, 0.25,
         "量到 0.25000", "吸附到格點", "amber"),
    ]

    for y, tl, td, v_true, v_meas, mlab, mtag, stage in rows:
        s.card(48, y - 33, 270, 66, tl, td, "teal")
        sx, mx = px(v_true), px(v_meas)
        # 真實值 → 量到的值（差距太小就不畫箭頭，以免和標記黏在一起）
        if abs(mx - sx) > 20:
            s.arrow(sx, y, mx, y, C[stage])
        s.p.append('<circle cx="%s" cy="%s" r="7.5" fill="%s"/>' % (sx, y, C["teal"]))
        # 空心方環：和圓點重疊時看得出「已經落在格點上」
        s.rect(mx - 8, y - 8, 16, 16, fill="none", stroke=C[stage], rx=3, sw=2.2)
        # 讀數標籤（靠邊時改對齊方向，避免超出畫布）
        if mx < X1 - 150:
            s.text(mx + 16, y - 12, mlab, 13, TXT, "700")
            s.text(mx + 16, y + 22, mtag, 11.5, MUT)
        else:
            s.text(mx - 16, y - 12, mlab, 13, TXT, "700", "end")
            s.text(mx - 16, y + 22, mtag, 11.5, MUT, "normal", "end")

    s.text(48, 492, "bf16 在這個 logit 量級只分辨得出 0.125 的差距；真值 0.060 於是被壓成 0。",
           13.5, C["rose"])
    s.text(48, 514, "8 個分歧點裡有 7 個的真實 gap 小於一個 bf16 ULP（最大也只有 0.32）。",
           13.5, MUT)



def _outcome(s, x, y, w, h, stage, name, line1, line2):
    """結果框：標籤 + 數字 + 一句結論。"""
    s.rect(x, y, w, h, fill=CARD, stroke=C[stage] + "66", rx=12)
    s.text(x + 20, y + 30, name, 16, C[stage], "700")
    s.text(x + 20, y + 56, line1, 13, TXT)
    s.text(x + 20, y + 80, line2, 13, MUT)


def fig_two_shapes(s):
    """圖 2：逐字解碼 vs 區塊驗證 —— 同一個前綴、兩種捨入。"""
    # ---- 左：逐字解碼 ----
    _panel(s, 48, 120, 430, 210, "blue", "逐字解碼 generate()", "每一步只算 1 個位置")
    for i in range(4):
        cx = 84 + i * 92
        s.rect(cx, 210, 54, 46, fill=CARD, stroke=C["blue"] + "66", rx=8)
        s.text(cx + 27, 237, str(i + 1), 14, TXT, "700", "middle")
        if i < 3:
            s.arrow(cx + 61, 233, cx + 85, 233, RAIL, 1.6)
    s.text(68, 300, "512 個 token 就是 512 次前向", 12.5, MUT)

    # ---- 右：區塊驗證 ----
    _panel(s, 510, 120, 422, 210, "teal", "區塊驗證 spec_generate()",
           "一次算 17 個位置（anchor + 16 個 draft）")
    for i in range(17):
        cx = 530 + i * 20
        st = C["rose"] if i == 0 else C["teal"]
        s.rect(cx, 210, 18, 46, fill=CARD, stroke=st + "88", rx=4, sw=1.2)
    s.text(530, 300, "第 1 格是 anchor，其餘 16 格是 draft", 12.5, MUT)

    # ---- 匯流 ----
    s.arrow(263, 332, 263, 352, RAIL)
    s.arrow(721, 332, 721, 352, RAIL)
    s.box(48, 356, 884, 62, "同一個前綴、同一份權重",
          "兩個形狀算的是同一個函數，只是 GEMM 的形狀不同 → 捨入順序不同",
          "violet", tsize=16, dsize=12.5)

    # ---- 兩種精度下的結果 ----
    s.arrow(263, 420, 263, 444, RAIL)
    s.arrow(721, 420, 721, 444, RAIL)
    _outcome(s, 48, 448, 430, 108, "rose", "bfloat16",
             "gap = +0.125 / −0.125 / +0.250",
             "→ 同一題，三種形狀給出兩種答案")
    _outcome(s, 510, 448, 422, 108, "teal", "float32",
             "形狀間差異 ≤ 5.7e−05",
             "→ 同一題，三種形狀給出同一個答案")

    s.text(48, 588, "上表 id 10 的實測：bf16 的 gap 隨形狀變號，argmax 就跟著翻轉。",
           13.5, C["rose"])
    s.text(48, 610, "fp32 下同一個前綴的差距固定在 −0.11644 附近，三種形狀都選同一個字。",
           13.5, MUT)


FIGS = [
    ("flashmap-bf16-quant-grid", 960, 540,
     "bf16 的量化格點：真實差距 0.060、0.242、0.320 被壓成 0.000 與 0.250",
     "真值 vs bf16 的讀數", fig_quant_grid,
     "圖 1：真實 gap（圓點）與 bf16 量到的格點（方環）——三列都是 8B 上實際量到的分歧點，"
     "0.060 被壓成完全平手。｜手繪 SVG 圖表"),
    ("flashmap-bf16-two-shapes", 980, 630,
     "逐字解碼與區塊驗證：同一前綴、兩種捨入，bf16 下 argmax 會翻轉，fp32 下不會",
     "1 個位置 vs 17 個位置", fig_two_shapes,
     "圖 2：<code>generate()</code> 一步算 1 個位置，FlashMap 的驗證一次算 17 個位置。"
     "數學等價、捨入不同：bf16 下 argmax 翻轉，fp32 下三種形狀一致。｜手繪 SVG 圖表"),
]

# 圖內標題（畫在 y=52）必須短，否則 25px 會超出圖卡右緣；完整描述留在 aria 與圖說。
TITLES = {
    "flashmap-bf16-quant-grid": "bf16 的量化格點",
    "flashmap-bf16-two-shapes": "同一前綴、兩種捨入",
}


def build(slug):
    """回傳指定 slug 的 Svg 物件（embed_flashmap_bf16.py 也用它產生 figure 區塊）。"""
    for s_slug, w, h, aria, sub, fn, _cap in FIGS:
        if s_slug == slug:
            s = Svg(w, h, aria, TITLES.get(s_slug, aria), sub)
            fn(s)
            return s
    raise SystemExit("unknown slug: %s" % slug)


def main():
    for slug, w, h, aria, sub, fn, _cap in FIGS:
        s = build(slug)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-34s %dx%d  %s"
              % (slug + ".svg", w, h, "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))


if __name__ == "__main__":
    main()

