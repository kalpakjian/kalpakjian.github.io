# -*- coding: utf-8 -*-
"""rtx50-blackwell-unlock-fact-check（_posts 文章）：2 張內嵌 SVG 圖表。

  圖 1  rtx50-blackwell-gate   Ada（暫存器可寫）vs Blackwell（熔絲決定、寫入被丟棄）
  圖 2  rtx50-blackwell-rate   速率檔位對照：Ada 的 1/2 速 vs Blackwell 的 1/8 速

House style 一律走 svglib.py（顏色不要寫死）；標籤一律真正的 <text>，方便 QA 量測。
這是 source/_posts/ 的一般文章（沒有 index.html 孿生檔），所以嵌入用同目錄的
embed_rtx50_blackwell.py，而不是 tools/diagrams/embed_figs.py（後者只吃 source/<note>/ 筆記）。

所有數字都有一手來源（見文章「查核方法與可重現性」一節）：
  - Ada 欄位：gpu-unlock-ada 的 read_sm_rates.py 配對讀值（4090 配對實測）
  - Blackwell 欄位：AndrewCTF 在 GB202（10de:2b85）、ElXreno 在 GB203M（10de:2c18）的讀值
  - 速率編碼定義：NVIDIA 開源核心模組 ctrl2080gr.h
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
# 圖 1：兩條鏈的對照（Ada 可寫暫存器 / Blackwell 寫不進去）
# ---------------------------------------------------------------------------
ADA_ROWS = [
    ("SEC2 BooterLoad（Falcon）", "已公開，可載入 payload"),
    ("緩衝區溢位 → ROP", "打開 FEAT_OVR_PLM 寫入保護"),
    ("主機寫入 SS0 / SS1", "寫得進去，讀回值變成 0"),
    ("fmla32：1 → 0", "1/2 速 → 全速"),
]
BW_ROWS = [
    ("沒有 Falcon SEC2 booter", "改用 FSP（NV-RISCV）當根信任"),
    ("GFW / FMC / GSP 全加密", "開源模組查無 Blackwell booter"),
    ("主機寫入 SS0 / SS1 / PLM", "讀回完全不變——無聲丟棄"),
    ("fmla32：3（熔絲決定）", "1/8 速，比 Ada 更嚴"),
]
ADA_NOTE = ("booter 明文是公開的，payload 可以照著寫",
            "SEC2 上跑的是簽章韌體，攻擊面在它自己的溢位")
BW_NOTE = ("開源模組對 Blackwell 的 booter 函式是回傳 NULL 的 stub",
           "熔絲改了會讓卡 refuse to post，不是「沒反應」而是開不了機")

GATE_ROW0 = 180
GATE_PITCH = 72        # box 58 + arrow 14
GATE_BOXH = 58


def fig_gate(s):
    """圖 1：同一組暫存器，兩種結局。"""
    panels = (
        (48, "teal", "Ada · RTX 4090（實測可解鎖）", ADA_ROWS, ADA_NOTE),
        (512, "rose", "Blackwell · RTX 5090（寫不進去）", BW_ROWS, BW_NOTE),
    )
    for px, stage, head, rows, note in panels:
        col = C[stage]
        s.rect(px, 126, 440, 420, fill=CARD2, stroke=col + "55", rx=12)
        s.text(px + 24, 158, head, 15, col, "700")
        bx = px + 24
        for i, (title, detail) in enumerate(rows):
            by = GATE_ROW0 + i * GATE_PITCH
            s.box(bx, by, 392, GATE_BOXH, title, detail,
                  stage=stage, align="start", tsize=13.5, dsize=11)
            if i < len(rows) - 1:
                s.arrow(bx + 196, by + GATE_BOXH, bx + 196, by + GATE_PITCH, col, 2)
        s.text(px + 24, 486, note[0], 11.5, MUT)
        s.text(px + 24, 506, note[1], 11.5, MUT)

    s.rect(48, 566, 904, 74, fill=CARD2, stroke=C["amber"] + "55", rx=10)
    s.text(68, 592, "兩件事同時成立：暫存器還在、閘門關著。", 13.5, TXT, "700")
    s.text(68, 614,
           "差異不在「有沒有人做」，而在「寫不進去」——寫入階梯讀回完全不變，連 FLR 都不會發生。",
           13, TXT)
    # ---------------------------------------------------------------------------
# 圖 2：速率檔位對照
# ---------------------------------------------------------------------------
# (欄位, 說明, Ada stock, Ada 解鎖後, Blackwell 5090, 是否為受限欄位)
RATE_ROWS = [
    ("fmla32", "FP16 乘、FP32 累加", "1 → 1/2 速", "0 → 全速", "3 → 1/8 速", True),
    ("imla2", "INT 模式", "1 → 1/2 速", "0 → 全速", "3 → 1/8 速", True),
    ("imla4", "INT 模式", "1 → 1/2 速", "0 → 全速", "3 → 1/8 速", True),
    ("imla1", "INT 模式", "—", "—", "3 → 1/8 速", True),
    ("fmla16", "FP16 乘、FP16 累加", "—", "—", "0 → 本來就全速", False),
]

RATE_X = (48, 318, 528, 738)     # label / Ada stock / Ada unlocked / Blackwell
RATE_W = (270, 200, 200, 214)
RATE_ROW0 = 144
RATE_PITCH = 34
RATE_ROWH = 28


def _cell(s, x, y, w, h, txt, colour=None, bold=False):
    if colour:
        s.rect(x, y, w, h, fill=colour + "22", stroke=colour + "99", rx=6, sw=1)
        s.text(x + w / 2, y + h / 2 + 4.5, txt, 12.5, colour,
               "700" if bold else "normal", "middle")
    else:
        s.rect(x, y, w, h, fill=CARD, stroke="#7d859044", rx=6, sw=1)
        s.text(x + w / 2, y + h / 2 + 4.5, txt, 12.5, MUT, "normal", "middle")


def fig_rate(s):
    """圖 2：Ada 的 1/2 速 vs Blackwell 的 1/8 速。"""
    heads = ("速率欄位", "Ada · RTX 4090 stock", "Ada · RTX 4090 解鎖後", "Blackwell · RTX 5090")
    head_col = (MUT, C["teal"], C["teal"], C["rose"])
    for i, (head, col) in enumerate(zip(heads, head_col)):
        s.text(RATE_X[i], 128, head, 12.5, col, "700")

    for r, (field, desc, ada_s, ada_u, bw, capped) in enumerate(RATE_ROWS):
        y = RATE_ROW0 + r * RATE_PITCH
        s.rect(RATE_X[0], y, RATE_W[0], RATE_ROWH, fill=CARD2,
               stroke="#30363d", rx=6, sw=1)
        s.text(RATE_X[0] + 14, y + 19, field, 13, TXT, "700")
        s.text(RATE_X[0] + 96, y + 19, desc, 11.5, MUT)
        _cell(s, RATE_X[1], y, RATE_W[1], RATE_ROWH, ada_s,
              C["amber"] if (capped and ada_s != "—") else None)
        _cell(s, RATE_X[2], y, RATE_W[2], RATE_ROWH, ada_u,
              C["teal"] if (capped and ada_u != "—") else None)
        _cell(s, RATE_X[3], y, RATE_W[3], RATE_ROWH, bw,
              C["rose"] if (capped and bw != "—") else None)

    s.rect(48, 336, 904, 76, fill=CARD2, stroke=C["amber"] + "55", rx=10)
    s.text(68, 362, "速率編碼（NVIDIA 開源核心模組 ctrl2080gr.h）", 13.5, TXT, "700")
    s.text(68, 386,
           "FMLA32_FULL_SPEED = 0 ｜ REDUCED_SPEED_1_2 = 1 ｜ REDUCED_SPEED_1_4 = 2 ｜ REDUCED_SPEED_1_8 = 3",
           12, TXT, font=MONO)
    s.text(68, 404,
           "「1/2 速」在 Ada 已經是極限；Blackwell 的「3」是 1/8 速——限得更深，而且連欄位集合都變了。",
           12.5, MUT)

    s.rect(48, 428, 904, 76, fill=CARD2, stroke=C["rose"] + "55", rx=10)
    s.text(68, 454, "所以「解鎖後衝上 420 TFLOPS」有兩層問題", 13.5, TXT, "700")
    s.text(68, 478,
           "① 419 TFLOPS 是白皮書的 FP16 累加峰值，不是 FP32 累加；後者只有 209.5。",
           12.5, TXT)
    s.text(68, 496,
           "② 就算解鎖成功，實測 FP16 累加也只有 324.6 TFLOPS——峰值規格本來就量不到。",
           12.5, MUT)

    s.text(48, 534,
           "Ada 欄位取自 gpu-unlock-ada 的 read_sm_rates.py 配對讀值；Blackwell 欄位取自 AndrewCTF（GB202）與 ElXreno（GB203M）的讀值。",
           12, MUT)


FIGS = [
    ("rtx50-blackwell-gate", 1000, 660,
     "Ada 與 Blackwell 的解鎖鏈對照：Ada 的主機寫入可以改變暫存器讀值，Blackwell 的寫入被無聲丟棄，速率改由熔絲決定",
     "同一組暫存器，兩種結局",
     "Ada 靠主機寫入解鎖；Blackwell 的速率改由熔絲決定，寫進去也沒用",
     fig_gate,
     "圖 1：兩條鏈的對照——Ada 的寫入會改變讀值，Blackwell 的寫入被無聲丟棄；"
     "差異不在「有沒有人做」，而在「寫不進去」。｜手繪 SVG 圖表"),
    ("rtx50-blackwell-rate", 1000, 570,
     "速率檔位對照：Ada 的 fmla32 是 1（1/2 速），Blackwell 是 3（1/8 速），而且 imla1 也被限速",
     "Ada 的 1/2 速 vs Blackwell 的 1/8 速",
     "同一組速率欄位，兩代的限速深度與受影響欄位都不一樣",
     fig_rate,
     "圖 2：速率檔位對照——Ada 的 fmla32 是 1（1/2 速）、Blackwell 是 3（1/8 速），"
     "連 Ada 沒有限速的 imla1 也被鎖住。｜手繪 SVG 圖表"),
]


def build(slug):
    """回傳指定 slug 的 Svg 物件（embed_rtx50_blackwell.py 也用它產生 figure 區塊）。"""
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
