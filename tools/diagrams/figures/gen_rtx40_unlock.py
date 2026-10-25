# -*- coding: utf-8 -*-
"""rtx40-tensor-unlock-fact-check（_posts 文章）：3 張內嵌 SVG 圖表。

  圖 1  rtx40-throughput-gap   「2 倍指令率」與「實際 GEMM 增益」的落差
  圖 2  rtx40-gemm-by-shape    同一個解鎖，六種矩陣形狀的實際增幅
  圖 3  rtx40-whitelist        模組只認這 4 個裝置 ID（白名單）

House style 一律走 svglib.py（顏色不要寫死）；標籤一律真正的 <text>，方便 QA 量測。
這是 source/_posts/ 的一般文章（沒有 index.html 孿生檔），所以嵌入用同目錄的
embed_rtx40_unlock.py，而不是 tools/diagrams/embed_figs.py（後者只吃 source/<note>/ 筆記）。

svglib 是流程圖引擎、沒有條形圖 helper，所以本檔自帶一個小工具：
  hbar_track()  一條「槽」代表量程上限，槽內的實心條代表實際值
                （接近 0 的值仍看得出「幾乎等於 0」，不會被畫成長條而誤導）
  水平軸與基準線走 s.line()，所以文字壓線會被 svglib.check() 抓到。
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
# 圖 1：指令率 2.00× 與真實 GEMM 增益的落差
# ---------------------------------------------------------------------------
# (名稱, 副說明, 增幅 %, 階段色)
GAP_ROWS = [
    ("FP16／BF16 → FP32 指令發射率", "最底層的指令率，也就是媒體說的「翻倍」", 100.0, "teal"),
    ("cuBLAS GEMM 4096³ FP16", "真實矩陣乘法最好的一格", 34.4, "blue"),
    ("cuBLAS GEMM 1024³ BF16", "小矩陣、換一種精度", 19.6, "blue"),
    ("cuBLAS GEMM 8192³ BF16", "換個矩陣形狀又是另一個數字", 16.0, "blue"),
    ("cuBLAS GEMM 4096³ BF16", "這一組完全沒有變化，暖開機重測還倒退", -0.5, "rose"),
    ("E4M3 FP8 CUTLASS GEMM", "專案自己公布的數字：+0.3%", 0.3, "gray"),
]

GAP_X0 = 330          # 0% 基準線
GAP_TRACK = 560       # 槽長 = +100%
GAP_ROW0 = 150
GAP_PITCH = 52
GAP_BARH = 28


def hbar_track(s, x0, y, track_len, h, pct, colour):
    """畫一條量程槽 + 實際值條。回傳 (tip_x, bar_left)。

    槽 = 量程上限（0% → 100%），實心條 = 實際值。
    負值畫在基準線左側；|值| 極小時仍保留一段可見的最小長度，
    讀者一眼看出「幾乎等於 0」，而不是把槽畫滿。
    """
    s.rect(x0, y, track_len, h, fill=CARD, stroke=C["gray"] + "44", rx=8, sw=1)
    if pct >= 0:
        length = max(3.0, track_len * pct / 100.0)
        s.rect(x0, y, length, h, fill=colour + "55", stroke=colour, rx=8)
        return x0 + length, x0
    length = max(3.0, track_len * (-pct) / 100.0)
    s.rect(x0 - length, y, length, h, fill=colour + "55", stroke=colour, rx=8)
    return x0 - length, x0 - length


def fig_gap(s):
    """圖 1：媒體的「翻倍」對上真實的 cuBLAS 增益。"""
    plot_top = GAP_ROW0
    plot_bottom = GAP_ROW0 + len(GAP_ROWS) * GAP_PITCH - (GAP_PITCH - GAP_BARH) + 10

    s.line(GAP_X0, plot_top - 4, GAP_X0, plot_bottom, RAIL, 1.5)
    s.text(GAP_X0 + GAP_TRACK, plot_top - 12, "「翻倍」+100%", 11.5, C["teal"], "700", "middle")

    for i, (name, sub, pct, stage) in enumerate(GAP_ROWS):
        y = GAP_ROW0 + i * GAP_PITCH
        col = C[stage]
        s.text(300, y + 15, name, 13, TXT, "700", "end")
        s.text(300, y + 32, sub, 11.5, MUT, "normal", "end")

        tip, _left = hbar_track(s, GAP_X0, y, GAP_TRACK, GAP_BARH, pct, col)
        label = ("+" if pct >= 0 else "-") + ("%.1f%%" % abs(pct))
        if pct < 0:
            # 負值條在基準線左側；標籤放右側並加 ▼，避免壓到左邊的名稱欄
            s.text(GAP_X0 + 12, y + 19, "▼ " + label, 13.5, col, "700")
        else:
            s.text(tip + 10, y + 19, label, 13.5, col, "700")

    for pct in (0, 25, 50, 75, 100):
        x = GAP_X0 + GAP_TRACK * pct / 100.0
        s.text(x, plot_bottom + 24, ("+%d%%" % pct) if pct else "0%", 11, MUT, "normal", "middle")

    box_y = plot_bottom + 40
    s.rect(48, box_y, 904, 88, fill=CARD2, stroke=C["teal"] + "55", rx=10)
    s.text(68, box_y + 28,
           "媒體說的「翻倍」＝ 最上面那根（指令發射率）。真實 cuBLAS 增益只有 +12% ～ +34%。",
           13, TXT)
    s.text(68, box_y + 50,
           "INT8、INT4、dp4a、純 FP32 完全沒有變化；FP8 幾乎等於 0。", 13, TXT)
    s.text(68, box_y + 72,
           "限速器確實拆掉了，但變速箱齒比、輪胎抓地力、限速牌都沒變。", 13, MUT)
# ---------------------------------------------------------------------------
# 圖 2：六種矩陣形狀的實際增幅
# ---------------------------------------------------------------------------
# (群組名, 群組副標, 型別, stock, unlocked, 階段色)
SHAPE_ROWS = [
    ("1024³", "小矩陣", "FP16", 107.546, 127.948, "blue"),
    ("1024³", "小矩陣", "BF16", 127.100, 151.968, "violet"),
    ("4096³", "中矩陣", "FP16", 153.234, 205.956, "blue"),
    ("4096³", "中矩陣", "BF16", 153.418, 152.720, "rose"),
    ("8192³", "大矩陣", "FP16", 168.675, 188.891, "blue"),
    ("8192³", "大矩陣", "BF16", 166.197, 192.744, "violet"),
]
GROUPS = ("1024³", "4096³", "8192³")

SH_X0 = 240           # 0% 基准線
SH_TRACK = 620        # 槽長 = +40%
SH_FULL = 40.0
SH_GROUPS = [170, 290, 410]
SH_PITCH = 44
SH_BARH = 26


def fig_shapes(s):
    """圖 2：同一個解鎖，六種矩陣形狀的實際增幅（含一組倒退）。"""
    plot_top = 148
    plot_bottom = 490

    s.line(SH_X0, plot_top, SH_X0, plot_bottom, RAIL, 1.5)

    for gi, grp_y in enumerate(SH_GROUPS):
        if gi:
            s.line(48, grp_y - 22, 952, grp_y - 22, "#30363d", 1.2)
        rows = [r for r in SHAPE_ROWS if r[0] == GROUPS[gi]]
        gname, gsub = rows[0][0], rows[0][1]
        mid = grp_y + (len(rows) * SH_PITCH - (SH_PITCH - SH_BARH)) / 2.0
        s.text(48, mid - 2, gname, 15, TXT, "700")
        s.text(48, mid + 16, gsub, 11, MUT)

        for ri, (_g, _gs, dtype, stock, unlocked, stage) in enumerate(rows):
            y = grp_y + ri * SH_PITCH
            col = C[stage]
            s.text(120, y + 18, dtype, 12.5, col, "700")

            pct = (unlocked / stock - 1.0) * 100.0
            tip, _left = hbar_track(s, SH_X0, y, SH_TRACK, SH_BARH, pct, col)
            label = ("+" if pct >= 0 else "-") + ("%.1f%%" % abs(pct))
            if pct < 0:
                s.text(SH_X0 + 12, y + 18, "▼ " + label, 13, col, "700")
            else:
                s.text(tip + 10, y + 18, label, 13, col, "700")
            s.text(120, y + 34, "%.1f→%.1f" % (stock, unlocked), 10.5, MUT)

    for pct in (0, 10, 20, 30, 40):
        x = SH_X0 + SH_TRACK * pct / SH_FULL
        s.text(x, plot_bottom + 24, ("+%d%%" % pct) if pct else "0%", 11, MUT, "normal", "middle")

    s.rect(48, 532, 904, 52, fill=CARD2, stroke=C["rose"] + "55", rx=10)
    s.text(68, 554,
           "同一個解鎖，增益卻從 +34.4% 掉到 -0.5%：矩陣形狀決定一切。", 13, TXT)
    s.text(68, 572,
           "所以別拿 README 裡的單一數字當結論——請用自己的工作負載量一次。", 13, MUT)


# ---------------------------------------------------------------------------
# 圖 3：白名單（原始碼 arch_610.h）
# ---------------------------------------------------------------------------
# (裝置 ID, 型號, 晶片, 狀態, 狀態色, 需求第 1 行, 需求第 2 行)
WHITELIST = [
    ("10de:2684", "RTX 4090", "AD102", "正式路徑", "teal",
     "只需 gpu_unlock.targets=", ""),
    ("10de:2685", "RTX 4090 D", "AD102", "實驗性", "amber",
     "+ rtx4090d_experimental=1", ""),
    ("10de:2705", "RTX 4070 Ti SUPER", "AD103", "實驗性・單卡", "amber",
     "+ ad103_experimental=1", "+ 單一完整 PCI 位址"),
    ("10de:2805", "RTX 4060 Ti 16GB", "AD106", "實驗性・單卡", "amber",
     "+ ad106_experimental=1", "+ 單一完整 PCI 位址"),
]


def fig_whitelist(s):
    """圖 3：模組只認這 4 個裝置 ID，其餘直接略過。"""
    s.box(48, 126, 904, 50, "白名單只有這四個 Ada 裝置 ID",
          "直接來自 kernel/gpu_unlock/arch_610.h，不是行銷文案", "teal")

    card_w, card_h = 216, 158
    xs = [48, 284, 520, 756]
    s.bus_out((500, 176), [(x + card_w / 2.0, 206) for x in xs], RAIL, stub=16)

    for x, (pid, model, die, status, stage, req1, req2) in zip(xs, WHITELIST):
        col = C[stage]
        s.rect(x, 206, card_w, card_h, fill=CARD, stroke=col + "66", rx=10)
        s.text(x + 14, 234, pid, 12.5, col, "700", "start", MONO)
        s.text(x + 14, 262, model, 15, TXT, "700")
        s.text(x + 14, 282, die, 11.5, MUT)
        s.rect(x + 12, 296, 104, 26, fill=col + "22", stroke=col, rx=6)
        s.text(x + 64, 314, status, 12, col, "700", "middle")
        s.text(x + 14, 344, req1, 10.5, MUT, "normal", "start", MONO)
        if req2:
            s.text(x + 14, 358, req2, 10.5, MUT, "normal", "start", MONO)

    s.rect(48, 392, 904, 60, fill=CARD2, stroke=C["rose"] + "55", rx=10)
    s.text(68, 418, "targets=all 永遠不會選中 2705 與 2805 —— 實驗型號必須指定單一 PCI 位址。",
           13, TXT)
    s.text(68, 440, "你的卡不在白名單裡 → 模組會直接略過它，不會跳任何警告。", 13, MUT)

    s.text(48, 486, "4070 Ti SUPER 有兩種晶片：0x2705 是 AD103（本專案支援）、0x2689 是 AD104（不支援）。",
           12.5, MUT)
    s.text(48, 508, "4060 Ti 16GB 實機常回報 0x2803 而非 0x2805，一樣會被略過。", 12.5, MUT)


FIGS = [
    ("rtx40-throughput-gap", 1000, 600,
     "解鎖後的增幅落差：指令發射率 +100%，但真實 cuBLAS GEMM 只有 +12% 到 +34%",
     "翻倍到實際的落差",
     "同一張 RTX 4090 解鎖後，相對原本（stock）的增幅", fig_gap,
     "圖 1：媒體說的「翻倍」對上真實的 cuBLAS 增益——最上面那根是指令發射率（+100%），"
     "底下的真實矩陣乘法只有 +12% ～ +34%，FP8 幾乎等於 0。｜手繪 SVG 圖表"),
    ("rtx40-gemm-by-shape", 1000, 600,
     "RTX 4090 六組 cuBLAS GEMM 配對實測的增幅：從 +34.4% 到 -0.5%，依矩陣形狀而變",
     "六種形狀的實際增幅",
     "同一個解鎖，六種矩陣形狀的實際增幅（數字為 cuBLAS GEMM 中位吞吐 TF/s）", fig_shapes,
     "圖 2：六組 cuBLAS GEMM 的實際增幅——同一個解鎖，增益卻從 +34.4% 掉到 -0.5%；"
     "矩陣形狀決定一切，別拿單一數字當結論。｜手繪 SVG 圖表"),
    ("rtx40-whitelist", 1000, 530,
     "gpu_unlock 模組的裝置白名單：只有 RTX 4090、4090 D、4070 Ti SUPER、4060 Ti 16GB 四個 ID",
     "裝置白名單只有四個 ID",
     "直接來自 kernel/gpu_unlock/arch_610.h，不是行銷文案", fig_whitelist,
     "圖 3：模組只認這四個裝置 ID——後兩者還要實驗旗標與單一 PCI 位址；"
     "不在名單裡的卡會被直接略過，不會跳警告。｜手繪 SVG 圖表"),
]


def build(slug):
    """回傳指定 slug 的 Svg 物件（embed_rtx40_unlock.py 也用它產生 figure 區塊）。

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
