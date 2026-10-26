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


def fig_verify_loop(s):
    """圖 2：一輪的形狀 —— draft 提議 → target 一次驗證 17 個位置 → 接受 k 個 + 1 bonus。"""
    s.text(48, 112, "每一輪都是一樣的形狀；差別只在這一輪接受了幾個 draft。", 13, MUT)

    stages = [
        (60, "前綴", "prompt + 已接受的 token", "blue"),
        (282, "draft 猜 16 個", "由 drafter 產生，可能全錯", "violet"),
        (504, "target 驗證", "一次前向 17 個位置", "teal"),
        (726, "commit", "接受前 k 個 + 1 個 bonus", "green"),
    ]
    for i, (x, t, d, st) in enumerate(stages):
        s.card(x, 140, 180, 96, t, d, st)
        if i < len(stages) - 1:
            s.arrow(x + 184, 188, x + 216, 188, RAIL)

    # 回圈：commit → 下一輪的前綴
    s.line(816, 236, 816, 302, RAIL)
    s.line(816, 302, 150, 302, RAIL)
    s.arrow(150, 302, 150, 240, RAIL)
    s.text(480, 292, "下一輪", 12.5, MUT, "normal", "middle")

    # 某一輪的驗證結果（示意）
    s.text(48, 336, "某一輪的驗證結果（示意：接受 6 個）", 12.5, MUT)
    for i in range(17):
        cx = 120 + i * 42
        if i < 6:
            st, fill = C["green"], CARD
        elif i == 6:
            st, fill = C["rose"], CARD2
        else:
            st, fill = C["gray"], CARD
        s.rect(cx, 350, 38, 52, fill=fill, stroke=st + "99", rx=6, sw=1.4)
    s.text(120, 428, "綠：接受", 12.5, C["green"])
    s.text(240, 428, "紅：第一個不符 → 改寫成 target 的 argmax", 12.5, C["rose"])
    s.text(660, 428, "灰：本輪作廢", 12.5, MUT)

    s.text(48, 470, "自我檢查：9/9 題通過（單題最多 479 個 token）—— 每個 commit 都等於它自己那一輪的 argmax。",
           13, MUT)
    s.text(48, 492, "所以送出的每一個 token 都是 target 自己的選擇；不一致只可能來自數值。",
           13, C["teal"])


def fig_tie_fork(s):
    """圖 4：同一個前綴、一個平手、三條不同的路。"""
    s.text(48, 112, "第 2 題：分歧點之前的 token 完全相同，只有索引 2 這一個位置不同。", 13, MUT)

    s.box(300, 140, 360, 60, "同一個前綴", "分歧點之前的 token 逐一相同", "violet")
    s.line(480, 200, 480, 240, RAIL)
    s.line(176, 240, 784, 240, RAIL)
    s.text(500, 228, "bf16 的 gap = 0.00000（完全平手）", 12.5, C["rose"])

    arms = [
        (36, "HF generate()", "217 tokens", "Let's solve this step…", "rose"),
        (340, "HF spec_generate()", "155 tokens", "Let's break this down…", "teal"),
        (644, "vLLM baseline", "155 tokens", "Let's break this down…", "blue"),
    ]
    for x, name, n, head, st in arms:
        s.arrow(x + 140, 240, x + 140, 268, RAIL)
        s.rect(x, 270, 280, 110, fill=CARD, stroke=C[st] + "66", rx=12)
        s.text(x + 20, 300, name, 15, C[st], "700")
        s.text(x + 20, 334, n, 19, TXT, "700")
        s.text(x + 20, 362, head, 12, MUT, font="'Cascadia Mono',Consolas,monospace")

    s.text(48, 420, "三個執行在分歧點之前一模一樣；vLLM 與 FlashMap 各自 tie-break 到「break」，",
           13, MUT)
    s.text(48, 442, "HF 的 generate() 落到「solve」—— 之後整段 155 / 217 個 token 就分岔了。",
           13, MUT)
    s.text(48, 474, "「長度差很多」看起來像嚴重錯誤，其實只是一次硬幣的正反面。", 13.5, C["rose"])


def fig_metrics(s):
    """圖 5：同一份 /metrics，兩種解析方式。"""
    s.text(48, 112, "同一個 /metrics 回應、兩種認家族名的方式；差別只在「怎麼比對名稱」。", 13, MUT)

    s.rect(48, 150, 330, 120, fill=CARD2, stroke=C["teal"] + "55", rx=12)
    s.text(68, 182, "正確：精確比對完整家族名", 15, C["teal"], "700")
    s.text(68, 210, "只取以 _total 結尾的家族", 12.5, MUT)
    s.text(68, 236, "accepted 2475 / drafts 626 / draft 10016", 12, TXT)
    for x, lab, val in [(400, "γ", "4.954"), (572, "草稿接受率", "24.71%"),
                        (744, "每步 draft", "16.0 個")]:
        s.rect(x, 162, 164, 96, fill=CARD, stroke=C["teal"] + "66", rx=10)
        s.text(x + 16, 196, lab, 12.5, MUT)
        s.text(x + 16, 232, val, 20, TXT, "700")

    s.rect(48, 300, 330, 120, fill=CARD2, stroke=C["rose"] + "55", rx=12)
    s.text(68, 332, "錯誤：substring 比對", 15, C["rose"], "700")
    s.text(68, 360, "命中 _created（Unix 時間戳 1.79e9）", 12.5, MUT)
    s.text(68, 384, "與 16 個 _per_pos_ 家族一起加總", 12.5, MUT)
    for x, lab, val in [(400, "被加進去的", "1.79e9"), (572, "家族數", "18 個"),
                        (744, "算出來的", "17.0")]:
        s.rect(x, 312, 164, 96, fill=CARD, stroke=C["rose"] + "66", rx=10)
        s.text(x + 16, 346, lab, 12.5, MUT)
        s.text(x + 16, 382, val, 20, C["rose"] if x == 744 else TXT, "700")

    s.text(48, 450, "「接受率 17.0」大於 1 就是最直接的警訊：分母被不相關的家族污染了。",
           13.5, C["rose"])
    s.text(48, 472, "修正後 γ = 4.954、接受率 24.71%、每步 16.0 個 draft token，與 vLLM 的 log 對帳一致。",
           13, MUT)

FIGS = [
    ("flashmap-bf16-quant-grid", 960, 540,
     "bf16 的量化格點：真實差距 0.060、0.242、0.320 被壓成 0.000 與 0.250",
     "真值 vs bf16 的讀數", fig_quant_grid,
     "圖 1：真實 gap（圓點）與 bf16 量到的格點（方環）——三列都是 8B 上實際量到的分歧點，"
     "0.060 被壓成完全平手。｜手繪 SVG 圖表"),
    ("flashmap-bf16-verify-loop", 960, 540,
     "一輪推測解碼的形狀：前綴、draft 猜 16 個、target 一次驗證 17 個位置、接受 k 個加 1 個 bonus",
     "draft → 驗證 → commit", fig_verify_loop,
     "圖 2：一輪的形狀——draft 先猜 16 個，target 一次驗證 17 個位置（anchor + 16 drafts），"
     "接受前 k 個再補一個 bonus；紅格是第一個不符、改寫成 target 的 argmax，之後全部作廢。"
     "｜手繪 SVG 圖表"),
    ("flashmap-bf16-two-shapes", 980, 630,
     "逐字解碼與區塊驗證：同一前綴、兩種捨入，bf16 下 argmax 會翻轉，fp32 下不會",
     "1 個位置 vs 17 個位置", fig_two_shapes,
     "圖 3：<code>generate()</code> 一步算 1 個位置，FlashMap 的驗證一次算 17 個位置。"
     "數學等價、捨入不同：bf16 下 argmax 翻轉，fp32 下三種形狀一致。｜手繪 SVG 圖表"),
    ("flashmap-bf16-tie-fork", 960, 520,
     "同一個前綴、一個 bf16 平手，三條執行給出 217 與 155 兩種長度",
     "同一個前綴，三種結局", fig_tie_fork,
     "圖 4：第 2 題的分歧——三者在前綴上完全相同，索引 2 的 bf16 gap 恰好是 0.00000，"
     "vLLM 與 FlashMap 各自 tie-break 到「break」，HF 的 <code>generate()</code> 落到「solve」。"
     "｜手繪 SVG 圖表"),
    ("flashmap-bf16-metrics", 960, 500,
     "同一份 metrics 回應的兩種解析：精確比對家族名得到 γ 4.954，substring 比對得到接受率 17.0",
     "精確比對 vs substring", fig_metrics,
     "圖 5：上排是修正後的正確解析（γ 4.954、接受率 24.71%、每步 16.0 個 draft token）；"
     "下排是 substring 比對的後果——把 <code>_created</code> 的 Unix 時間戳與 16 個 "
     "<code>_per_pos_</code> 家族一起加進來，算出大於 1 的「接受率 17.0」。｜手繪 SVG 圖表"),
]

# 圖內標題（畫在 y=52）必須短，否則 25px 會超出圖卡右緣；完整描述留在 aria 與圖說。
TITLES = {
    "flashmap-bf16-quant-grid": "bf16 的量化格點",
    "flashmap-bf16-verify-loop": "一輪的形狀",
    "flashmap-bf16-two-shapes": "同一前綴、兩種捨入",
    "flashmap-bf16-tie-fork": "一個平手，三條路",
    "flashmap-bf16-metrics": "指標是怎麼算錯的",
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

