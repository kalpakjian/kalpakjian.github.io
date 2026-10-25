# -*- coding: utf-8 -*-
"""rtx4090-gpu-unlock-guide（_posts 文章）：3 張內嵌 SVG 圖表。

  圖 1  rtx4090-steps        4090 的六步操作流程（不需要實驗旗標）
  圖 2  rtx4090-two-layers   指令發射率 2× vs 真實 cuBLAS GEMM 12～34%
  圖 3  rtx4090-payload      負載分流：量化權重等於沒加速

House style 一律走 svglib.py（顏色不要寫死）；標籤一律真正的 <text>，方便 QA 量測。
這是 source/_posts/ 的一般文章，嵌入用同目錄的 embed_rtx4090_guide.py。

指令字串一律照抄上游 JustAResearcher/gpu-unlock-ada 的 QUICKSTART.md 與 README.md。
注意 Ada 分支與 Ampere 上游的差異：Ada 沒有 resume 模組參數、沒有 Ampere 的 tools/，
但多了 diagnostics/bench 的指令率探針與 tools/read_sm_rates.py 的唯讀讀回。
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
# 圖 1：六步流程
# ---------------------------------------------------------------------------
# (標題, 指令, 備註)
STEPS = [
    ("確認白名單並取得位址", "python3 tools/print_boot_option.py",
     "唯讀工具，會直接印出要用的那行"),
    ("安裝套件", "git clone … && cd gpu-unlock-ada && make install",
     "Arch／Debian／RPM 自動偵測"),
    ("設定核心命令列", "gpu_unlock.targets=0000:03:00.0",
     "4090 只要這一項，不需要實驗旗標"),
    ("完整斷電後冷開機", "切掉 AC 電源、等約 30 秒再上電",
     "暖開機不保證提供乾淨韌體狀態"),
    ("驗證是否真的解鎖", "journalctl -k -b | grep gpu_unlock",
     "要找 gpu_unlock: unlocked"),
    ("讀回速率並量自己的負載", "python3 tools/read_sm_rates.py --expect-uuid …",
     "唯讀，不寫暫存器、不重置"),
]

NOTES = [
    (0, "4090 是唯一不用實驗旗標的",
     "4070 Ti SUPER 與 4060 Ti 16GB 還要加",
     "ad103／ad106_experimental=1 這類旗標。", "teal"),
    (4, "模組載入成功 ≠ 解鎖成功",
     "必須看到目標卡的 gpu_unlock: unlocked，且 nvidia-smi 健康、",
     "journal 裡沒有 NVRM: Xid。", "rose"),
]


def fig_steps(s):
    """圖 1：六步操作流程。"""
    x0, bw = 48, 556
    y0, pitch, bh = 126, 84, 64

    for i, (title, cmd, note) in enumerate(STEPS):
        y = y0 + i * pitch
        col = C["teal"]
        s.rect(x0, y, bw, bh, fill=CARD, stroke=col + "55", rx=10)
        s.badge(x0 + 28, y + bh / 2.0, str(i + 1), col, r=15, size=13)
        s.text(x0 + 54, y + 24, title, 13.5, TXT, "700")
        s.text(x0 + 54, y + 44, cmd, 10, C["blue"], "normal", "start", MONO)
        s.text(x0 + 54, y + 58, note, 10, MUT)
        if i:
            s.arrow(x0 + 28, y - 4, x0 + 28, y - 20, RAIL)

    nx, nw = 636, 316
    for idx, title, line1, line2, stage in NOTES:
        y = y0 + idx * pitch
        col = C[stage]
        s.rect(nx, y, nw, bh + 14, fill=CARD2, stroke=col + "66", rx=10)
        s.text(nx + 16, y + 26, title, 12.5, col, "700")
        s.text(nx + 16, y + 48, line1, 10.5, MUT)
        s.text(nx + 16, y + 64, line2, 10.5, MUT)
        s.arrow(x0 + bw + 4, y + bh / 2.0, nx - 4, y + bh / 2.0, col, 1.5)

# ---------------------------------------------------------------------------
# 圖 2：指令發射率 vs 真實 GEMM
# ---------------------------------------------------------------------------
# (項目, 數值, 比值, 階段色)  —— 指令發射率
ISSUE_ROWS = [
    ("FP16 / FP32 累加", "160.4 → 320.4 TF/s", 1.998, "teal"),
    ("BF16 / FP32 累加", "159.7 → 320.2 TF/s", 2.005, "teal"),
    ("TF32 / FP32 累加", "80.1 → 159.5 TF/s", 1.990, "teal"),
]

# (形狀, 比值)  —— 真實 cuBLAS GEMM
GEMM_ROWS = [
    ("4096³ FP16", 1.344),
    ("1024³ BF16", 1.196),
    ("1024³ FP16", 1.190),
    ("8192³ BF16", 1.160),
    ("8192³ FP16", 1.120),
    ("4096³ BF16", 0.995),
]


def fig_two_layers(s):
    """圖 2：2 倍是指令發射率；真實 GEMM 只有 12～34%。"""
    s.rect(48, 118, 440, 330, fill=CARD2, stroke=C["teal"] + "55", rx=12)
    s.text(68, 148, "指令發射率（register-resident）", 14, C["teal"], "700")
    s.text(68, 170, "最底層的指令率——媒體說的「翻倍」是這一層", 11, MUT)
    for i, (name, raw, ratio, stage) in enumerate(ISSUE_ROWS):
        y = 192 + i * 44
        col = C[stage]
        s.text(68, y + 14, name, 11.5, TXT, "700")
        s.text(68, y + 30, raw, 10.5, MUT)
        s.rect(300, y + 2, 170, 20, fill=col + "55", stroke=col, rx=6)
        s.text(466, y + 17, "%.2f×" % ratio, 12.5, col, "700", "end")

    s.rect(512, 118, 440, 330, fill=CARD2, stroke=C["blue"] + "55", rx=12)
    s.text(532, 148, "真實 cuBLAS GEMM", 14, C["blue"], "700")
    s.text(532, 170, "這才是「你的程式會不會變快」", 11, MUT)
    for i, (name, ratio) in enumerate(GEMM_ROWS):
        y = 192 + i * 40
        col = C["rose"] if ratio < 1.0 else C["blue"]
        s.text(532, y + 13, name, 11.5, TXT, "700")
        w = max(4.0, 150.0 * (ratio - 0.9) / 0.5)
        s.rect(700, y + 1, w, 18, fill=col + "55", stroke=col, rx=5)
        s.text(932, y + 14, "%.3f×" % ratio, 12, col, "700", "end")

    s.rect(48, 462, 904, 82, fill=CARD, stroke=C["amber"] + "55", rx=10)
    s.text(68, 488,
           "完全沒有變化的路徑：FP16 搭 FP16 累加、INT8、unsigned INT4、dp4a、純 FP32。", 13, TXT)
    s.text(68, 510,
           "真實 GEMM 的增益依矩陣形狀而變：4096³ BF16 是 0.995×（等於沒變），"
           "同一次暖開機重測還慢了 8.2%。", 13, MUT)
    s.text(68, 534,
           "資料來源：docs/evidence/rtx4090-pr1-matched/README.md（獨立使用者配對實測，450 W 上限）。",
           11.5, MUT)


# ---------------------------------------------------------------------------
# 圖 3：負載分流
# ---------------------------------------------------------------------------
def fig_payload(s):
    """圖 3：量化權重等於沒加速。"""
    s.rect(48, 122, 904, 58, fill=CARD2, stroke=C["blue"] + "66", rx=12)
    s.text(500, 146, "關鍵分水嶺", 12, C["blue"], "700", "middle")
    s.text(500, 168,
           "權重是 FP16／BF16（而且累加走 FP32）嗎？", 14, TXT, "700", "middle")

    s.rect(48, 212, 440, 176, fill=CARD, stroke=C["teal"] + "66", rx=12)
    s.text(68, 240, "是 → 會變快（真實 GEMM +12～34%）", 14, C["teal"], "700")
    for i, (n, d) in enumerate([("LLM prefill", "prompt 一次算完的那段"),
                                ("擴散模型／圖片生成", "UNet 與 VAE 的矩陣乘法"),
                                ("FP16／BF16 的訓練", "反向傳播也是矩陣乘法")]):
        y = 258 + i * 44
        s.text(68, y + 15, "・" + n, 12.5, TXT, "700")
        s.text(68, y + 31, "　　" + d, 10.5, MUT)

    s.rect(512, 212, 440, 176, fill=CARD, stroke=C["gray"] + "55", rx=12)
    s.text(532, 240, "不是 → 幾乎沒差", 14, C["gray"], "700")
    for i, (n, d) in enumerate([("INT8／4-bit／3-bit 量化權重", "Issue #17：3-bit MoE IQ3_S 實測 0.983×"),
                                ("純 FP32 運算", "這條路徑本來就沒被鎖"),
                                ("逐 token 生成（decode）", "瓶頸在記憶體頻寬")]):
        y = 258 + i * 44
        s.text(532, y + 15, "・" + n, 12.5, TXT, "700")
        s.text(532, y + 31, "　　" + d, 10.5, MUT)

    s.arrow(340, 180, 268, 208, C["teal"], 1.8)
    s.arrow(660, 180, 732, 208, C["gray"], 1.8)

    s.rect(48, 404, 904, 84, fill=CARD2, stroke=C["rose"] + "55", rx=10)
    s.text(68, 430,
           "最容易被忽略的一句：Issue #17 的實測者用 3-bit MoE（IQ3_S）跑 8K prefill，", 13, TXT)
    s.text(68, 452,
           "得到的比值是 0.983×——完全沒有加速。原文寫得很直接：", 13, MUT)
    s.text(68, 476,
           "「The 2x lands only on FP16/BF16 weights with FP32 accumulation.」", 13,
           C["rose"], "700")
FIGS = [
    ("rtx4090-steps", 1000, 640,
     "RTX 4090 解除 gpu-unlock 的六步操作流程：確認白名單、安裝、設定核心命令列、冷開機、"
     "驗證 gpu_unlock: unlocked、讀回速率並量自己的負載",
     "六步操作流程", "4090 是唯一不需要實驗旗標的", fig_steps,
     "圖 1：六步操作流程——4090 只需 gpu_unlock.targets 一項（4070 Ti SUPER 與 4060 Ti "
     "還要實驗旗標），而「模組載入成功」不等於「解鎖成功」。｜手繪 SVG 圖表"),
    ("rtx4090-two-layers", 1000, 560,
     "RTX 4090 的兩層數字：指令發射率接近 2 倍，但真實 cuBLAS GEMM 只有 +12% 到 +34%，"
     "4096³ BF16 甚至是 0.995×",
     "兩層數字", "指令率 ≠ 你的程式", fig_two_layers,
     "圖 2：左邊是指令發射率（媒體說的「翻倍」），右邊是真實 cuBLAS GEMM——"
     "12% 到 34%，而且 4096³ BF16 等於沒變。｜手繪 SVG 圖表"),
    ("rtx4090-payload", 1000, 500,
     "RTX 4090 解鎖後哪些負載會變快：FP16／BF16 權重搭配 FP32 累加會，"
     "而 INT8、4-bit、3-bit 量化權重不會——Issue #17 實測 3-bit MoE 為 0.983×",
     "我的負載會變快嗎", "分水嶺在權重精度", fig_payload,
     "圖 3：負載分流的分水嶺在權重精度——量化權重（3-bit MoE 實測 0.983×）"
     "完全吃不到解鎖帶來的加速。｜手繪 SVG 圖表"),
]


def build(slug):
    """回傳指定 slug 的 Svg 物件（embed_rtx4090_guide.py 也用它產生 figure 區塊）。

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

