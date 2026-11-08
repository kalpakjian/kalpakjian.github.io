# -*- coding: utf-8 -*-
"""Memorilla 導讀文的 4 張內嵌 SVG（house style 由 svglib 提供）。

用法：python gen_memorilla_guide.py
產物：_m_<slug>.svg / _m_<slug>.html（量測用），不進版控。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))          # tools/diagrams
from svglib import Svg, C, MUT, TXT                 # noqa: E402

OUT = HERE


def fig_rag_vs_memory(s):
    s.text(48, 118, "傳統 RAG：把「文字」塞進 context", 16, C["amber"], "700")
    s.box(48, 138, 400, 56, "① 檢索 retrieve", "cosine 相似度挑 top-k 段落", "amber", align="start")
    s.box(48, 214, 400, 56, "② 貼進 prompt", "k 段原文 → prefill 隨 k 線性成長", "amber", align="start")
    s.box(48, 290, 400, 56, "③ 解碼 decode", "32k 上限；爆掉就得上 YaRN", "amber", align="start")
    s.arrow(248, 194, 248, 212, C["amber"])
    s.arrow(248, 270, 248, 288, C["amber"])
    s.text(48, 382, "成本：每次查詢都要重讀 k 段文字，k 越大越慢。", 13, MUT)
    s.text(48, 406, "弱點：選到哪一段就只能看到哪一段（selection 的天花板）。", 13, MUT)

    s.line(486, 130, 486, 420, "#222b36")
    s.text(486, 118, "vs", 15, MUT, "700", "middle")

    s.text(524, 118, "Memorilla：把「資訊」放進 embedding 空間", 16, C["teal"], "700")
    s.box(524, 138, 410, 56, "① 編碼一次", "每份文件 → 1 個可重用向量（5 KB）", "teal", align="start")
    s.box(524, 214, 410, 56, "② 查詢時讀取", "16 個 slot 對「問題＋整份語料」做 cross-attention", "teal", align="start")
    s.box(524, 290, 410, 56, "③ 注入解碼器", "16 個 soft token 寫進 input embedding", "teal", align="start")
    s.arrow(729, 194, 729, 212, C["teal"])
    s.arrow(729, 270, 729, 288, C["teal"])
    s.text(524, 382, "成本：永遠只給 decoder 16 個 token，語料變大延遲幾乎不動。", 13, MUT)
    s.text(524, 406, "前提：decoder 完全凍結，只訓練中間那個 memory module。", 13, MUT)

    s.text(48, 452, "一句話：RAG 換「給多少文字」，Memorilla 換「給哪一種媒介」。", 14, TXT, "700")


def fig_16_tokens(s):
    s.box(48, 120, 250, 66, "① 文件編碼", "每份文件 1 個向量", "gray", align="start")
    s.box(48, 206, 250, 66, "② 文件庫", "200 份 ≈ 1 MB", "gray", align="start")
    s.box(48, 300, 250, 66, "③ 問題", "編碼成 1 個向量", "blue", align="start")

    s.rect(352, 108, 300, 272, fill="#161b22", stroke="#2dd4bf66")
    s.text(502, 136, "記憶槽（固定 16 個）", 14, C["teal"], "700", "middle")
    slots = ["學到的初始向量 k₁ … k₁₆",
             "＋問題殘差 → 每個槽各自不同",
             "cross-attention ×N 讀全部文件",
             "輸出：16 × d 的 soft token"]
    for i, lab in enumerate(slots):
        y = 156 + i * 54
        s.rect(378, y, 248, 38, fill="#1c2230", stroke="#2dd4bf44", rx=8)
        s.text(502, y + 24, lab, 12.5, MUT, "normal", "middle")
    s.arrow(298, 153, 376, 168)
    s.arrow(298, 239, 376, 190, C["gray"])
    s.arrow(298, 333, 376, 300, C["blue"])

    s.rect(700, 108, 250, 272, fill="#161b22", stroke="#58a6ff66")
    s.text(825, 136, "凍結的 Qwen3-8B", 14, C["blue"], "700", "middle")
    s.text(825, 170, "input embedding 空間", 13, MUT, "normal", "middle")
    s.rect(722, 190, 206, 46, fill="#0d1117", stroke="#58a6ff44", rx=8)
    s.text(825, 211, "16 個 soft token", 13, C["teal"], "700", "middle")
    s.text(825, 229, "（不是文字，是向量）", 11.5, MUT, "normal", "middle")
    s.rect(722, 248, 206, 46, fill="#0d1117", stroke="#30363d", rx=8)
    s.text(825, 269, "使用者的問題", 13, TXT, "700", "middle")
    s.text(825, 287, "純文字 token", 11.5, MUT, "normal", "middle")
    s.arrow(652, 244, 720, 226, C["teal"])
    s.text(825, 330, "問題 token 與 16 個 soft token", 11.5, MUT, "normal", "middle")
    s.text(825, 348, "在 embedding 層串接後一起送進", 11.5, MUT, "normal", "middle")
    s.text(825, 366, "32 層 Transformer（權重不動）", 11.5, MUT, "normal", "middle")

    s.text(48, 404, "關鍵：解碼器權重一個都沒動（凍結）；被訓練的只有中間 194.1M 參數的 memory module。", 13.5, TXT, "700")
    s.text(48, 428, "所以「16」是輸出預算，不是壓縮率的上限——它是一個可以調的旋鈕（見 §五 ablation）。", 13, MUT)


def fig_tradeoff(s):
    x0, y0, w, h = 130, 400, 690, 250
    s.line(x0, y0, x0 + w, y0, MUT, 1)
    s.line(x0, y0, x0, y0 - h, MUT, 1)
    for i, lab in enumerate(["1", "10", "100", "1k", "10k", "32k"]):
        x = x0 + i * (w / 5.0)
        s.line(x, y0, x, y0 + 6, MUT, 1)
        s.text(x, y0 + 24, lab, 12, MUT, "normal", "middle")
    s.text(x0 - 34, y0 + 26, "文件 token", 12, MUT, "700", "end")
    s.text(x0 - 30, y0 - h - 8, "分數", 12, MUT, "700", "end")

    pts = [
        ("全上下文 full context", 0.95, 0.50, C["amber"], -12, -18),
        ("MemoRAG", 0.62, 0.62, C["violet"], -10, -16),
        ("RAG-50", 0.62, 0.36, C["gray"], -8, 26),
        ("xRAG / LLMLingua-2", 0.34, 0.55, C["rose"], 12, -12),
        ("Mem0", 0.34, 0.28, C["gray"], 12, 18),
        ("Memorilla（16 tok）", 0.04, 0.80, C["teal"], 14, -12),
    ]
    for (lab, fx, fy, col, dx, dy) in pts:
        cx = x0 + fx * w
        cy = y0 - fy * h
        s.p.append('<circle cx="%.1f" cy="%.1f" r="7.5" fill="%s"/>' % (cx, cy, col))
        anchor = "start" if dx >= 0 else "end"
        s.text(cx + dx, cy + dy, lab, 12.5, col, "700", anchor)

    s.text(48, 470, "幾何平均分數：Memorilla 49.68｜xRAG 41.92｜LLMLingua-2 40.75｜Mem0 38.02。", 13.5, TXT, "700")
    s.text(48, 494, "相對全上下文少 394× token、相對 RAG-50 少 113×、相對 MemoRAG 少 49×。左上角才是我們真正想要的角落。", 12.5, MUT)


def fig_serving(s):
    s.text(48, 118, "寫入路徑（每份文件只付一次）", 15, C["blue"], "700")
    rows = [("文件編碼 200 → 400 份", "22.92 → 2,588.84 ms", "線性成長", C["amber"]),
            ("每份文件儲存", "5 KB → 5 KB", "不變", C["green"]),
            ("kv cache 對照（PV4）", "6.9 GiB", "記憶庫小 7,266×", C["blue"]),
            ("→ 寫入成本與 RAG 共用", "一次索引，多次查詢", "不是額外開銷", C["gray"])]
    y = 140
    for (a, b, c, col) in rows:
        s.rect(48, y, 400, 58, fill="#161b22", stroke=col + "66", rx=10)
        s.text(64, y + 24, a, 13, TXT, "700")
        s.text(64, y + 44, b, 12.5, col, "700")
        s.text(432, y + 35, c, 12, MUT, "normal", "end")
        y += 72

    s.line(486, 110, 486, 470, "#222b36")
    s.text(524, 118, "讀取路徑（每次查詢都付）", 15, C["teal"], "700")
    cards = [("Memory module forward", "2.01 ms → 1.96 ms", "語料翻倍還更快", C["green"]),
             ("CPU → GPU 搬移", "0.014 → 0.060 ms", "占延遲 < 0.04%", C["green"]),
             ("Memorilla 端到端", "740 ms → 739 ms", "幾乎不動", C["teal"]),
             ("Full Context 端到端", "749 ms → 19,932 ms", "爆 32k，得開 YaRN", C["rose"])]
    y = 140
    for (a, b, c, col) in cards:
        s.rect(524, y, 400, 64, fill="#161b22", stroke=col + "66", rx=10)
        s.text(540, y + 23, a, 13, TXT, "700")
        s.text(540, y + 44, b, 13.5, col, "700")
        s.text(908, y + 44, c, 11.5, MUT, "normal", "end")
        y += 76

    s.text(48, 508, "同機實測（H100-80GB、batch 1、bf16、max_new_tokens=32）：好處不是單次查詢更快，而是「服務成本不隨語料膨脹」。", 12.5, MUT)


FIGS = [
    ("memorilla-fig1", 960, 480,
     "圖 1：傳統 RAG 與 Memorilla 的資料流對照：RAG 把 k 段原文貼進 prompt，Memorilla 只注入 16 個 soft token",
     "兩種記憶介面：給你多少文字，還是給你哪一種媒介",
     "左：檢索 → 貼進 prompt → 解碼；右：編碼一次 → 查詢時讀取 → 注入解碼器", fig_rag_vs_memory),
    ("memorilla-fig2", 960, 452,
     "圖 2：16 個 memory token 的產生流程：學到的初始向量 → 問題殘差 → 對全部文件 cross-attention → 寫進凍結解碼器的 input embedding",
     "16 個 token 是怎麼生出來的",
     "三段式：slot 初始化 → 查詢調節 → 文件檢索（Perceiver 式 latent array）", fig_16_tokens),
    ("memorilla-fig3", 960, 520,
     "圖 3：八個基準的 token 數與分數取捨：Memorilla 落在每個基準的 Pareto 前緣，16 個 token 就拿到幾何平均 49.68",
     "為什麼「16 個 token」值得在意",
     "橫軸是每查詢文件 token 數（對數），縱軸是主指標分數", fig_tradeoff),
    ("memorilla-fig4", 960, 540,
     "圖 4：服務成本隨語料成長：Memorilla 端到端 740 → 739 ms，full context 749 → 19,932 ms",
     "省的不是算力，是「不會爆掉」",
     "左：寫入路徑；右：讀取路徑（H100-80GB, batch 1, bf16）", fig_serving),
]

if __name__ == "__main__":
    for (slug, w, h, aria, title, sub, fn) in FIGS:
        s = Svg(w, h, aria, title, sub)
        fn(s)
        bad = s.check()
        print("%-18s %s" % (slug, "OK" if not bad else "COLLISION x%d" % len(bad)))
        for b in bad[:5]:
            print("    ", b)
        s.save(os.path.join(OUT, "_m_%s.svg" % slug),
               os.path.join(OUT, "_m_%s.html" % slug))
    print("done")



