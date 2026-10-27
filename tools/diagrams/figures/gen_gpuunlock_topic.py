# -*- coding: utf-8 -*-
"""gpu-unlock 專題頁（source/gpu-unlock/index.md）：2 張內嵌 SVG 圖表。

  圖 1  gpuunlock-lineage      專案血緣：cmpunlocker → cmp90hx-unlock → gpu-unlock → gpu-unlock-ada，
                                加上 2026-10 冒出來的兩條 Turing 分支，以及 Blackwell 那道牆
  圖 2  gpuunlock-five-posts   五篇文章速查（2026-10-27 新增第 5 篇後重製）

為什麼這裡要有產生器：這個專題頁不是「筆記」（沒有 md／html 孿生檔），
所以 tools/diagrams/embed_figs.py 不吃它；另外兩張圖原本是手寫內嵌的，
改一次內容就要重排整張圖——改成資料驅動之後，改文字只要改這支檔案的常數。

House style 一律走 svglib.py（顏色不要寫死）；標籤一律真正的 <text>，方便 QA 量測。
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from svglib import Svg, C, MUT, TXT, CARD, CARD2, MONO  # noqa: E402

HERE = _HERE


# ---------------------------------------------------------------------------
# 圖 1：專案血緣
# ---------------------------------------------------------------------------
# (專案名, 作者, 說明 1, 說明 2, 階段色)
LINEAGE = [
    ("cmpunlocker", "amoghmunikote",
     "把 8／10 GB 的 CMP 170HX 解鎖成 64／40 GB", "曾被 LTT 報導過的那一支", "gray"),
    ("cmp90hx-unlock", "WildFlash1st",
     "貢獻 GA102 的 V67 payload 鏈", "後來兩邊都沿用同一條鏈", "gray"),
    ("gpu-unlock", "Zagitta",
     "第一個 Linux 核心模組版本", "GA10x 數十個裝置 ID，靠社群眾包", "teal"),
    ("gpu-unlock-ada", "JustAResearcher",
     "移植到 Ada 世代（RTX 40）", "白名單精簡到 4 個 ID，證據做成配對實測", "teal"),
]
LIN_X, LIN_W, LIN_H = 48, 330, 68
LIN_Y0, LIN_PITCH = 132, 76

# 兩條 Turing 分支（2026-10 各自另起爐灶）
TURING = [
    ("turing-unlock", "nlzy", "2026-10-24 · 2080 Ti 22GB"),
    ("KohakUnlock", "KohakuBlueleaf", "2026-10-25 · Leadtek TU102 雙卡"),
]

# 右欄：兩個 Linux 模組的關鍵差異（標籤, Ampere 側, Ada 側）
COMPARE = [
    ("涵蓋範圍", "GA102／103／104／106 數十個 ID", "僅 4 個 Ada ID"),
    ("實驗旗標", "4070 Ti SUPER 需實驗旗標", "4090 只要 targets 一項"),
    ("診斷工具", "沒有診斷工具", "有唯讀讀回與指令率探針"),
    ("證據策略", "靠社群眾包相容性報告", "配對實測＋數值驗證＋遙測"),
]


def fig_lineage(s):
    """圖 1：專案血緣 + Turing 分支 + Blackwell 那道牆。"""
    # 左欄：四個 repo 的鏈
    for i, (name, author, d1, d2, stage) in enumerate(LINEAGE):
        y = LIN_Y0 + i * LIN_PITCH
        col = C[stage]
        s.rect(LIN_X, y, LIN_W, LIN_H, fill=CARD, stroke=col + "66", rx=10)
        s.text(LIN_X + 16, y + 26, name, 13.5, col, "700", font=MONO)
        s.text(LIN_X + LIN_W - 16, y + 26, author, 10.5, MUT, "normal", "end")
        s.text(LIN_X + 16, y + 46, d1, 10.5, MUT)
        s.text(LIN_X + 16, y + 60, d2, 10.5, MUT)
        if i < len(LINEAGE) - 1:
            s.arrow(LIN_X + LIN_W / 2, y + LIN_H, LIN_X + LIN_W / 2, y + LIN_PITCH,
                    "#7d8590", 2)

    # 左欄下方：兩條 Turing 分支（獨立的群組框）
    s.rect(LIN_X, 444, LIN_W, 132, fill=CARD2, stroke=C["violet"] + "55", rx=10)
    s.text(LIN_X + 16, 466, "Turing 分支（2026-10 各自另起爐灶）", 11.5, C["violet"], "700")
    for j, (name, author, note) in enumerate(TURING):
        by = 476 + j * 48
        s.rect(LIN_X + 16, by, LIN_W - 32, 44, fill=CARD, stroke=C["violet"] + "55", rx=6)
        s.text(LIN_X + 30, by + 17, name, 12, C["violet"], "700", font=MONO)
        s.text(LIN_X + LIN_W - 30, by + 17, author, 9.5, MUT, "normal", "end")
        s.text(LIN_X + 30, by + 33, note, 9.5, MUT)
    s.text(LIN_X, 598, "Turing 那兩條與 Ada 版同源（V67 溢位鏈），但各自獨立發展。",
           11, MUT)

    # 右欄：兩個 Linux 模組的關鍵差異
    s.rect(420, 132, 532, 348, fill=CARD2, stroke=C["blue"] + "55", rx=14)
    s.text(440, 160, "兩個 Linux 模組的關鍵差異", 14, C["blue"], "700")
    s.text(440, 182, "同一個 exploit，不同的涵蓋範圍與證據策略", 11, MUT)
    for i, (label, amp, ada) in enumerate(COMPARE):
        y = 202 + i * 56
        s.rect(436, y, 250, 44, fill=CARD, stroke=C["amber"] + "55", rx=8)
        s.rect(694, y, 242, 44, fill=CARD, stroke=C["amber"] + "55", rx=8)
        s.text(448, y + 18, "gpu-unlock", 10, MUT)
        s.text(448, y + 35, amp, 11, TXT, "700")
        s.text(706, y + 18, "gpu-unlock-ada", 10, MUT)
        s.text(706, y + 35, ada, 11, TXT, "700")
        s.text(440, y - 8, label, 9.5, C["gray"], "700")
    s.text(440, 442, "共同的根：已簽章 NVIDIA booter 的緩衝區溢位 + ROP", 12,
           C["rose"], "700")
    s.text(440, 462, "解開 FEAT_OVR_PLM 的寫入保護後，寫 SS0／SS1 即可改成全速", 10.5, MUT)

    # 底部：Windows 旁支 + Blackwell 那道牆
    s.rect(48, 616, 904, 88, fill=CARD2, stroke=C["teal"] + "55", rx=10)
    s.text(68, 642,
           "Windows 那條線是旁支：TOTORONG/AD103_win_unlocker 的 UEFI 實驗提供 AD102 payload；",
           13, TXT)
    s.text(68, 664,
           "impacifist/Windows-GPU-UNLOCK 則把它做成獨立的 Windows 工具。",
           13, MUT)
    s.text(68, 686,
           "Blackwell 沒有分支——維護者 2026-10-26 公開回覆「The short answer is no」：不是還沒做，是寫不進去。",
           13, C["rose"], "700")


# ---------------------------------------------------------------------------
# 圖 2：五篇文章速查
# ---------------------------------------------------------------------------
# (階段, 標題, 對象, 關鍵數字, 一句話結論, 階段色)
POSTS = [
    ("事實查核", "RTX 30 系 gpu-unlock", "對象：GA10x 數十個 ID",
     "關鍵數字：BF16 +25～81%", "「一律翻倍」不成立；各型號差三倍", "blue"),
    ("事實查核", "RTX 40 系 Tensor 解鎖", "對象：4 個 Ada ID",
     "關鍵數字：指令率 2×、GEMM +12～34%", "「全系列」不成立；FP8 幾乎沒變", "blue"),
    ("操作筆記", "RTX 3080 12GB", "對象：10de:220a",
     "關鍵數字：FP16 +69%、BF16 +73%", "只吃 FP16／BF16 矩陣乘法", "teal"),
    ("操作筆記", "RTX 4090", "對象：10de:2684",
     "關鍵數字：指令率 1.998×", "不用實驗旗標；量化權重吃不到", "teal"),
]
POST_X = (48, 512)
POST_W = 440
POST_H = 160
POST_Y = (126, 300)
POST5_Y = 474
POST5_H = 116


def _post_card(s, x, y, w, h, stage, title, obj, num, line, stage_col):
    col = C[stage_col]
    s.rect(x, y, w, h, fill=CARD, stroke=col + "66", rx=12)
    s.rect(x, y, 6, h, rx=3, fill=col, stroke="#30363d", sw=1.5)
    tx = x + 22
    s.text(tx, y + 28, stage, 10.5, col, "700")
    s.text(tx, y + 52, title, 15, TXT, "700")
    s.text(tx, y + 74, obj, 11, MUT)
    s.text(tx, y + 96, num, 11.5, col, "700")
    s.line(tx, y + 108, x + w - 22, y + 108, "#30363d", 1.2)
    s.text(tx, y + 130, line, 11.5, TXT)
    s.text(tx, y + 150, "→ 讀這篇", 11, col, "700")


def fig_posts(s):
    """圖 2：五篇文章速查。"""
    for i, (stage, title, obj, num, line, col) in enumerate(POSTS):
        x = POST_X[i % 2]
        y = POST_Y[i // 2]
        _post_card(s, x, y, POST_W, POST_H, stage, title, obj, num, line, col)

    # 第 5 篇：滿版卡片
    x, y, w, h = POST_X[0], POST5_Y, 904, POST5_H
    col = C["rose"]
    s.rect(x, y, w, h, fill=CARD, stroke=col + "66", rx=12)
    s.rect(x, y, 6, h, rx=3, fill=col, stroke="#30363d", sw=1.5)
    s.text(x + 22, y + 28, "事實查核 · 2026-10-27 新增", 10.5, col, "700")
    s.text(x + 22, y + 52, "RTX 50 系 Blackwell 解鎖", 15, TXT, "700")
    s.text(x + 22, y + 74,
           "對象：Blackwell 全系（GB20x）　·　關鍵數字：fmla32 = 3（1/8 速），主機寫入被丟棄",
           11, MUT)
    s.line(x + 22, y + 86, x + w - 22, y + 86, "#30363d", 1.2)
    s.text(x + 22, y + 106,
           "維護者 2026-10-26 公開回覆「The short answer is no」——不是「還沒人做」，是「寫不進去」",
           11.5, TXT)

    # 底部：共同結論
    s.rect(48, 606, 904, 92, fill=CARD2, stroke=C["amber"] + "55", rx=10)
    s.text(68, 632, "五篇的共同結論：解鎖是真的，媒體的關鍵字是假的。", 13.5, TXT, "700")
    s.text(68, 654, "① 「全系列」不成立——白名單只有少數型號；連下一代（Blackwell）都解不動",
           12, MUT)
    s.text(68, 672, "② 「翻倍」是指令發射率；真實 GEMM 只有 +12～81%", 12, MUT)
    s.text(68, 690, "③ 「所有 AI 負載都變快」不成立——INT8／4-bit／3-bit 量化完全沒變",
           12, MUT)


FIGS = [
    ("gpuunlock-lineage", 1000, 724,
     "gpu-unlock 專案血緣：從 cmpunlocker 到 cmp90hx-unlock、gpu-unlock、gpu-unlock-ada，加上 2026-10 的兩條 Turing 分支，以及 Blackwell 那道牆",
     "專案血緣",
     "同一個 exploit，兩種做法；Blackwell 沒有分支",
     fig_lineage,
     "圖 1：專案血緣——共同的根都是已簽章 NVIDIA booter 的緩衝區溢位；"
     "2026-10 新增兩條 Turing 分支，而 Blackwell 那一格是空的。｜手繪 SVG 圖表"),
    ("gpuunlock-five-posts", 1000, 718,
     "gpu-unlock 專題五篇文章速查：兩篇事實查核、兩篇分卡型操作筆記，以及 2026-10-27 新增的 Blackwell 查核",
     "五篇速查",
     "先看哪一篇？",
     fig_posts,
     "圖 2：五篇文章速查——兩篇事實查核負責「打破關鍵字」，兩篇操作筆記負責「照著做」，"
     "第五篇解釋為什麼下一代解不動。｜手繪 SVG 圖表"),
]


def build(slug):
    """回傳指定 slug 的 Svg 物件（embed_gpuunlock_topic.py 也用它產生 figure 區塊）。"""
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

