# -*- coding: utf-8 -*-
"""rtx3080-12gb-gpu-unlock-guide（_posts 文章）：2 張內嵌 SVG 圖表。

  圖 1  gpuunlock-steps     六步操作流程與兩個判斷分支
  圖 2  gpuunlock-payload   「我的負載會變快嗎」判斷樹

House style 一律走 svglib.py（顏色不要寫死）；標籤一律真正的 <text>，方便 QA 量測。
這是 source/_posts/ 的一般文章，嵌入用同目錄的 embed_gpuunlock_guide.py。

注意：指令字串一律照抄上游 Zagitta/gpu-unlock 的 README。
上游 repo 沒有 diagnostics/ 或 tools/ 目錄（那些是 Ada 分支 gpu-unlock-ada 才有的），
所以本指南的量測步驟改用 issue #62 同款的 torch + cuBLAS，可攜且不依賴額外工具。
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
# 圖 1：操作流程
# ---------------------------------------------------------------------------
# (標題, 說明, 指令／備註)
STEPS = [
    ("確認 PCI ID 在白名單裡", "lspci -Dnn | grep -i nvidia", "應出現 10de:220a"),
    ("安裝套件", "git clone … && cd gpu-unlock && make install", "Arch／Debian／RPM 自動偵測"),
    ("設定核心命令列", "gpu_unlock.targets=0000:03:00.0", "寫進 GRUB 或 systemd-boot"),
    ("完整斷電後冷開機", "切掉 AC 電源、等待約 30 秒再上電", "暖開機不保證提供乾淨韌體狀態"),
    ("驗證是否真的解鎖", "journalctl -k -b | grep gpu_unlock", "要找 gpu_unlock: unlocked"),
    ("量一次自己的負載", "stock 與 unlocked 各量一次，用同一組設定", "同一核心／驅動／binary／功耗上限"),
]

# 旁註 (對應步驟索引, 標題, 第一行, 第二行, 階段色)
NOTES = [
    (0, "不在名單就會被略過",
     "模組只接受 main.c 白名單裡的 ID；",
     "其他型號會被記錄後跳過，不會有任何提示。", "amber"),
    (4, "模組載入成功 ≠ 解鎖成功",
     "必須看到目標卡的 gpu_unlock: unlocked，",
     "且 nvidia-smi 健康、journal 沒有 NVRM: Xid。", "rose"),
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
        s.text(x0 + 54, y + 44, cmd, 10.5, C["blue"], "normal", "start", MONO)
        s.text(x0 + 54, y + 58, note, 10, MUT)
        if i:
            s.arrow(x0 + 28, y - 4, x0 + 28, y - 20 + 0, RAIL)

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
# 圖 2：負載判斷樹
# ---------------------------------------------------------------------------
def fig_payload(s):
    """圖 2：我的負載會變快嗎。"""
    s.rect(48, 122, 904, 58, fill=CARD2, stroke=C["blue"] + "66", rx=12)
    s.text(500, 146, "判斷只有一句", 12, C["blue"], "700", "middle")
    s.text(500, 168,
           "你的負載有沒有在跑「FP16／BF16 乘、FP32 累加」的矩陣乘法？",
           14, TXT, "700", "middle")

    # 左：有 → 會快
    s.rect(48, 212, 440, 190, fill=CARD, stroke=C["teal"] + "66", rx=12)
    s.text(68, 240, "有 → 會變快（+69～73%）", 15, C["teal"], "700")
    for i, (n, d) in enumerate([("LLM prefill", "逐 token 生成之外的預填充"),
                                ("擴散模型／圖片生成", "UNet 與 VAE 的矩陣乘法"),
                                ("FlashAttention", "Issue #60 實測 +47～68%")]):
        y = 258 + i * 46
        s.text(68, y + 16, "・" + n, 12.5, TXT, "700")
        s.text(68, y + 33, "　　" + d, 10.5, MUT)

    # 右：沒有 → 分流
    s.rect(512, 212, 440, 190, fill=CARD, stroke=C["gray"] + "55", rx=12)
    s.text(532, 240, "沒有 → 幾乎沒差", 15, C["gray"], "700")
    for i, (n, d) in enumerate([("純 FP32 運算", "這條路徑本來就沒被鎖"),
                                ("INT8 量化", "維持原狀"),
                                ("4-bit 量化（Ollama 預設）", "實測無增益"),
                                ("LLM 逐 token 生成", "瓶頸在記憶體頻寬，不在算力")]):
        y = 258 + i * 36
        s.text(532, y + 16, "・" + n, 12.5, TXT, "700")
        s.text(532, y + 31, "　　" + d, 10.5, MUT)

    s.arrow(340, 180, 268, 208, C["teal"], 1.8)
    s.arrow(660, 180, 732, 208, C["gray"], 1.8)

    s.rect(48, 424, 904, 84, fill=CARD2, stroke=C["teal"] + "55", rx=10)
    s.text(68, 452,
           "3080 12GB 的實測（Issue #62，8192³ dense GEMM、FP32 累加、350 W 上限）：", 13, TXT)
    s.text(68, 474, "FP16 65.52 → 110.62 TFLOPS（+69%）　·　"
                    "BF16 65.63 → 113.24 TFLOPS（+73%）　·　"
                    "TF32 32.42 → 54.51 TFLOPS（+68%）", 12.5, C["teal"], "700")
    s.text(68, 496,
           "但 3080 的 760 GB/s 記憶體頻寬不會變——decode 瓶頸還在原處。", 12, MUT)

FIGS = [
    ("gpuunlock-steps", 1000, 640,
     "RTX 3080 12GB 解除 gpu-unlock 的六步操作流程：確認 PCI ID、安裝、設定核心命令列、"
     "冷開機、驗證 gpu_unlock: unlocked、量自己的負載",
     "六步操作流程", "旁邊兩個分支是最容易踩到的地方", fig_steps,
     "圖 1：六步操作流程——「不在白名單會被略過」與「模組載入成功不等於解鎖成功」"
     "是兩個最常見的陷阱。｜手繪 SVG 圖表"),
    ("gpuunlock-payload", 1000, 520,
     "解鎖後哪些工作負載會變快：FP16／BF16 乘 FP32 累加的矩陣乘法會快 69% 到 73%，"
     "純 FP32、INT8、4-bit 量化與逐 token 生成幾乎不變",
     "我的負載會變快嗎", "判準只有一句話", fig_payload,
     "圖 2：負載判斷樹——prefill、擴散模型、FlashAttention 會變快；"
     "純 FP32、INT8、4-bit 量化與逐 token 生成幾乎沒差。｜手繪 SVG 圖表"),
]


def build(slug):
    """回傳指定 slug 的 Svg 物件（embed_gpuunlock_guide.py 也用它產生 figure 區塊）。

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
