# -*- coding: utf-8 -*-
"""rtx30-gpu-unlock-ampere-fact-check（_posts 文章）：4 張內嵌 SVG 圖表。

  圖 1  ampere-three-precision   RTX 3090 Ti 三種精度解鎖前後（不是一律 2×）
  圖 2  ampere-gain-range        各型號 BF16 GEMM 增益範圍（含兩個例外）
  圖 3  ampere-exploit-chain     漏洞利用流程：ROP → PLM → SS0/SS1 → FLR
  圖 4  ampere-workload-split    哪些工作負載受惠、哪些不動

House style 一律走 svglib.py（顏色不要寫死）；標籤一律真正的 <text>，方便 QA 量測。
這是 source/_posts/ 的一般文章，嵌入用同目錄的 embed_rtx30_ampere.py。

svglib 是流程圖引擎、沒有條形圖 helper，所以本檔自帶 hbar_range()：
  一條「槽」代表量程上限，槽內的實心條代表實際值；區間型資料用淺色段 + 深色端點。
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


def hbar_range(s, x0, y, track_len, h, lo, hi, full, colour):
    """槽 + 區間條。回傳 tip_x。

    槽 = 量程上限（0 → full），深色段 = 區間 [lo, hi]，淺色端點 = 單點值。
    """
    s.rect(x0, y, track_len, h, fill=CARD, stroke=C["gray"] + "44", rx=8, sw=1)
    if hi - lo < 0.05:                        # 單一數值 → 淺色短條
        length = max(4.0, track_len * hi / full)
        s.rect(x0, y, length, h, fill=colour + "33", stroke=colour, rx=8)
        return x0 + length
    lo_len = track_len * lo / full
    hi_len = track_len * hi / full
    s.rect(x0 + lo_len, y, hi_len - lo_len, h, fill=colour + "66", stroke=colour, rx=8)
    return x0 + hi_len


# ---------------------------------------------------------------------------
# 圖 1：RTX 3090 Ti 三種精度
# ---------------------------------------------------------------------------
# (精度, Before, After, 階段色)
PREC_ROWS = [
    ("FP16", 87.46, 118.39, "blue"),
    ("BF16", 87.50, 157.41, "teal"),
    ("TF32", 42.58, 82.61, "violet"),
]

P_X0 = 250          # 0 TF/s 基準線
P_FULL = 170.0      # 槽長代表 170 TF/s
P_ROW0 = 170
P_PITCH = 66
P_BARH = 24
P_TRACK = 620


def fig_precision(s):
    """圖 1：同一張 3090 Ti，三種精度解鎖後的增幅並不一樣。"""
    plot_top = P_ROW0 - 12
    plot_bottom = P_ROW0 + len(PREC_ROWS) * P_PITCH - (P_PITCH - P_BARH) + 16

    s.rect(P_X0, plot_top - 32, 22, 12, fill=C["gray"] + "2e",
           stroke=C["gray"] + "88", rx=3, sw=1)
    s.text(P_X0 + 32, plot_top - 22, "解鎖前（stock）", 11.5, MUT)
    s.rect(P_X0 + 150, plot_top - 32, 22, 12, fill=C["teal"] + "66",
           stroke=C["teal"], rx=3)
    s.text(P_X0 + 182, plot_top - 22, "解鎖後", 11.5, MUT)
    s.text(P_X0 + P_TRACK, plot_top - 22, "（TF/s）", 11, MUT, "normal", "end")

    for i, (name, before, after, stage) in enumerate(PREC_ROWS):
        y = P_ROW0 + i * P_PITCH
        col = C[stage]
        s.text(P_X0 - 22, y + 17, name, 14, col, "700", "end")

        # stock 條（淺灰）
        blen = P_TRACK * before / P_FULL
        s.rect(P_X0, y, blen, P_BARH, fill=C["gray"] + "2e", stroke=C["gray"] + "88",
               rx=8, sw=1)
        s.text(P_X0 + blen + 10, y + 17, "%.1f" % before, 12, MUT)

        # unlocked 條（疊在下方一格，實心）
        y2 = y + P_BARH + 4
        alen = P_TRACK * after / P_FULL
        s.rect(P_X0, y2, alen, P_BARH - 2, fill=col + "66", stroke=col, rx=7)
        s.text(P_X0 + alen + 10, y2 + 16, "%.1f" % after, 13, col, "700")
        pct = (after / before - 1.0) * 100.0
        s.text(P_X0 + alen + 62, y2 + 16, "+%.0f%%" % pct, 13, col, "700")

    s.line(P_X0, plot_top, P_X0, plot_bottom, RAIL, 1.5)

    for v in (0, 50, 100, 150):
        x = P_X0 + P_TRACK * v / P_FULL
        s.text(x, plot_bottom + 26, str(v), 11, MUT, "normal", "middle")

    box_y = plot_bottom + 46
    s.rect(48, box_y, 904, 84, fill=CARD2, stroke=C["teal"] + "55", rx=10)
    s.text(68, box_y + 28,
           "BF16 +80%、TF32 +94%，但 FP16 只有 +35%。解鎖不是把每種精度都拉滿，", 13, TXT)
    s.text(68, box_y + 50,
           "而是把每一種精度各自拉到「等效專業卡」的位置——所以別說「一律翻倍」。", 13, TXT)
    s.text(68, box_y + 72,
           "資料來源：README「3090 Ti dense 8192³ GEMM at 450 W, five-sample medians with FP32 accumulation」。",
           11.5, MUT)


# ---------------------------------------------------------------------------
# 圖 2：各型號增益範圍
# ---------------------------------------------------------------------------
# (型號, 晶片, 狀態, 最小 %, 最大 %, 階段色)
GAIN_ROWS = [
    ("RTX 3070", "GA104", "已解鎖", 73, 81, "teal"),
    ("RTX 3060 12GB", "GA106", "已解鎖", 80, 80, "teal"),
    ("RTX 3090 Ti", "GA102", "已解鎖", 68, 80, "teal"),
    ("RTX 3080 10GB", "GA102", "已解鎖", 70, 73, "teal"),
    ("RTX 3080 12GB", "GA102", "已解鎖", 69, 73, "teal"),
    ("RTX 3080 20GB", "GA102", "改裝 20GB", 56, 59, "teal"),
    ("RTX 3090", "GA102", "已解鎖", 25, 67, "teal"),
    ("RTX 3070 Ti", "GA104", "模組未測", 0, 0, "amber"),
    ("RTX 3080 Ti 20GB", "GA102", "維持半速", 0, 0, "rose"),
]

G_X0 = 300
G_FULL = 100.0
G_TRACK = 480
G_ROW0 = 158
G_PITCH = 44
G_BARH = 22


def fig_gain_range(s):
    """圖 2：各型號的 BF16 GEMM 增益區間 + 兩個例外。"""
    plot_top = G_ROW0 - 10
    plot_bottom = G_ROW0 + len(GAIN_ROWS) * G_PITCH - (G_PITCH - G_BARH) + 14

    s.line(G_X0, plot_top, G_X0, plot_bottom, RAIL, 1.5)
    s.text(G_X0 + G_TRACK, plot_top - 22, "BF16 GEMM 增益", 12, C["teal"], "700", "end")

    for i, (model, chip, status, lo, hi, stage) in enumerate(GAIN_ROWS):
        y = G_ROW0 + i * G_PITCH
        col = C[stage]
        s.text(G_X0 - 24, y + 15, model, 13, TXT, "700", "end")
        s.text(G_X0 - 24, y + 30, "%s・%s" % (chip, status), 10.5, MUT, "normal", "end")

        if hi <= 0:
            # 例外：畫一條斜線示意「沒有數據」
            s.rect(G_X0, y + 6, 46, 3, fill=col, rx=1)
            s.text(G_X0 + 62, y + 15, "—", 13, col, "700")
            continue

        tip = hbar_range(s, G_X0, y, G_TRACK, G_BARH, lo, hi, G_FULL, col)
        label = ("+%d%%" % hi) if hi == lo else ("+%d–%d%%" % (lo, hi))
        s.text(tip + 12, y + 16, label, 13, col, "700")

    for v in (0, 25, 50, 75, 100):
        x = G_X0 + G_TRACK * v / G_FULL
        s.text(x, plot_bottom + 26, ("+%d%%" % v) if v else "0%", 11, MUT, "normal", "middle")

    box_y = plot_bottom + 46
    s.rect(48, box_y, 904, 62, fill=CARD2, stroke=C["amber"] + "55", rx=10)
    s.text(68, box_y + 26,
           "兩個例外：RTX 3070 Ti 從未用這個模組測過（同樣的解鎖改用 Windows UEFI 埠成功）；",
           13, TXT)
    s.text(68, box_y + 48,
           "RTX 3080 Ti 20GB OEM 的交易會跑完，但 BF16 仍維持半速——「成功」不等於「有效」。",
           13, MUT)


# ---------------------------------------------------------------------------
# 圖 3：漏洞利用流程
# ---------------------------------------------------------------------------
def fig_exploit_chain(s):
    """圖 3：從開機韌體的緩衝區溢位到全速選擇器的六步。"""
    steps = [
        ("1", "驅動載入韌體", "SEC2 驗簽並啟動 GSP-RM", "blue"),
        ("2", "Booter 緩衝區溢位", "已簽章韌體的 stack overflow", "rose"),
        ("3", "ROP 取得控制流", "以 ROP 堆疊執行任意程式碼", "rose"),
        ("4", "解除寫入保護", "FEAT_OVR_PLM = 0xFFFFFFFF", "amber"),
        ("5", "寫入速率選擇器", "SS0 = 0x88888888 / SS1 = 0x8", "teal"),
        ("6", "FLR 後交還", "未修改的 nvidia 驅動正常綁定", "green"),
    ]
    w, h = 236, 96
    xs = [48, 284, 520, 756]
    top_y, bot_y = 132, 296

    for i, (num, title, detail, stage) in enumerate(steps):
        col = C[stage]
        # 蛇形：上排 1→2→3（左到右），下排 4→5→6（右到左）
        colx = xs[i] if i < 3 else xs[5 - i]
        y = top_y if i < 3 else bot_y
        s.rect(colx, y, w, h, fill=CARD, stroke=col + "66", rx=12)
        s.badge(colx + 30, y + 30, num, col, r=16, size=14)
        s.text(colx + 58, y + 36, title, 14, TXT, "700")
        s.text(colx + 16, y + 68, detail, 11, MUT)

    # 上排 1→2→3
    for i in range(2):
        s.arrow(xs[i] + w, top_y + h / 2.0, xs[i + 1] - 4, top_y + h / 2.0, RAIL)
    # 3→4：右側垂直下折
    s.arrow(xs[2] + w / 2.0, top_y + h, xs[2] + w / 2.0, bot_y - 4, RAIL)
    # 下排 4→5→6（右到左）
    for i in (2, 1):
        s.arrow(xs[i] - 4, bot_y + h / 2.0, xs[i - 1] + w, bot_y + h / 2.0, RAIL)

    box_y = bot_y + h + 30
    s.rect(48, box_y, 904, 62, fill=CARD2, stroke=C["rose"] + "55", rx=10)
    s.text(68, box_y + 26,
           "這是對 GPU 安全處理器的未授權程式碼執行（緩衝區溢位 + ROP），"
           "性質比一般驅動 hack 重一級。", 13, TXT)
    s.text(68, box_y + 48,
           "上游 README 也寫明：若卡上的韌體沒停下來，模組會保留韌體可能仍在使用的 DMA 緩衝區，"
           "必須完全斷電。", 11.5, MUT)


# ---------------------------------------------------------------------------
# 圖 4：哪些工作負載受惠
# ---------------------------------------------------------------------------
# (工作負載, 變化描述, 階段色, 是否受惠)
WORKLOADS = [
    ("LLM prefill", "+14% ～ +66%（依卡與功耗上限）", "teal", True),
    ("FlashAttention", "+47% ～ +68%", "teal", True),
    ("擴散模型（圖片生成）", "明顯受惠", "teal", True),
    ("真實 GEMM 吞吐", "依型號 +25% ～ +81%", "teal", True),
    ("LLM decode（逐 token 生成）", "幾乎不變——瓶頸在記憶體頻寬", "gray", False),
    ("INT8 量化運算", "維持原狀", "gray", False),
    ("4-bit 量化推論", "無增益", "gray", False),
    ("遊戲", "不會變快", "gray", False),
]


def fig_workload(s):
    """圖 4：受惠與不受惠的工作負載分流。"""
    x_left, x_right = 48, 512
    w = 440
    s.rect(x_left, 126, w, 374, fill=CARD2, stroke=C["teal"] + "55", rx=12)
    s.rect(x_right, 126, w, 374, fill=CARD2, stroke=C["gray"] + "44", rx=12)
    s.text(x_left + 20, 156, "會變快", 15, C["teal"], "700")
    s.text(x_right + 20, 156, "不會變快", 15, C["gray"], "700")

    for i, (name, detail, stage, gain) in enumerate(WORKLOADS):
        base = x_left if gain else x_right
        row = i if gain else i - 4
        y = 176 + row * 78
        col = C[stage]
        s.rect(base + 16, y, w - 32, 62, fill=CARD, stroke=col + "55", rx=10)
        s.text(base + 32, y + 26, name, 13.5, TXT, "700")
        s.text(base + 32, y + 48, detail, 11.5, MUT)

    s.text(48, 524,
           "判準只有一句：你的負載有沒有在跑「FP16／BF16 乘、FP32 累加」的矩陣乘法。",
           13.5, TXT)
    s.text(48, 548,
           "有 → 受惠；瓶頸在記憶體頻寬或走 INT8／4-bit → 幾乎沒差。", 13, MUT)


FIGS = [
    ("ampere-three-precision", 1000, 500,
     "RTX 3090 Ti 三種精度解鎖前後對比：BF16 +80%、TF32 +94%，但 FP16 只有 +35%",
     "不是一律兩倍", "同一張 3090 Ti，8192³ dense GEMM、450 W", fig_precision,
     "圖 1：同一張 RTX 3090 Ti 的三種精度——BF16 87.5→157.4、TF32 42.6→82.6，"
     "但 FP16 只從 87.5 到 118.4。解鎖不是把每種精度都拉滿。｜手繪 SVG 圖表"),
    ("ampere-gain-range", 1000, 680,
     "各型號 BF16 GEMM 增益範圍 +25% 到 +81%，以及 3070 Ti 未測、3080 Ti 維持半速兩個例外",
     "各型號的增益區間", "區間來自各使用者自己的量測，功耗上限差異很大", fig_gain_range,
     "圖 2：各型號的 BF16 GEMM 增益區間——RTX 3070 約 +73～81%，"
     "RTX 3090 只有 +25～67%（225 W 上限的卡）；另有兩個例外。｜手繪 SVG 圖表"),
    ("ampere-exploit-chain", 1000, 520,
     "gpu-unlock 的漏洞利用鏈：已簽章 booter 的緩衝區溢位 → ROP → 解除 FEAT_OVR_PLM 寫入保護 "
     "→ 寫入 SS0/SS1 速率選擇器 → PCIe FLR → 未修改的驅動綁定",
     "漏洞利用的六步", "全部發生在 NVIDIA 驅動載入之前", fig_exploit_chain,
     "圖 3：從開機韌體的緩衝區溢位到全速選擇器的六步——ROP 取得控制流後，"
     "只要寫 0xFFFFFFFF 就能解除 SS0/SS1 的寫入保護。｜手繪 SVG 圖表"),
    ("ampere-workload-split", 1000, 570,
     "哪些工作負載受惠（prefill、FlashAttention、擴散模型）與哪些不動（decode、INT8、4-bit、遊戲）",
     "受惠與不受惠", "判準：有沒有在跑 FP16／BF16 乘、FP32 累加的矩陣乘法", fig_workload,
     "圖 4：受惠與不受惠的工作負載分流——prefill 與 FlashAttention 明顯受惠，"
     "decode、INT8、4-bit 量化與遊戲幾乎沒差。｜手繪 SVG 圖表"),
]


def build(slug):
    """回傳指定 slug 的 Svg 物件（embed_rtx30_ampere.py 也用它產生 figure 區塊）。

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
