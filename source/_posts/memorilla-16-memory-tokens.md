---
title: '只有 16 個 token 的長期記憶：細讀 Memorilla，把整份語料壓進「16 個軟 token」'
date: 2026-11-08 09:30:00
categories:
  - 論文導讀
  - 技術筆記
tags:
  - Memorilla
  - 長期記憶
  - Memory Tokens
  - soft prompt
  - 潛在壓縮
  - RAG
  - Mem0
  - MemoRAG
  - Perceiver
  - Qwen3
  - arXiv
toc: true
index_img: /img/covers/memorilla-16-memory-tokens.png
banner_img: /img/covers/memorilla-16-memory-tokens.png
---

社群上流傳一句話：**「AI 只需要 16 個 token，就能擁有長期記憶。」**

這句話出自 2026 年 10 月掛上 arXiv 的論文 *Memorilla: Latent Semantic Memory for LLMs*（史丹佛 SNAP 實驗室，Jure Leskovec 在作者群裡）。數字是真的：NarrativeQA 上一本書 67,385 個 token 的內容，被壓成 16 個 token 之後模型照樣答得出來。但「擁有長期記憶」這五個字，比論文實際證明的事多了一些。

本筆記把這篇論文拆開重講一遍：**它到底怎麼做的、16 個 token 從哪來、八個基準分別贏在哪輸在哪、以及那張「740 ms vs 19,932 ms」的表到底在量什麼**。所有數字都對回原文（v3, 2026-11-03）。

<!-- more -->

> **一句話總結**：Memorilla 沒有讓模型「記住」更多，它是把「每次要給模型看多少文字」這個問題，換成「每次要給模型看哪一種媒介」——從文字換成 16 個向量。真正的貢獻在**介面**，不在容量。

<!-- TOC-CARD -->
<div class="callout">
  <div class="callout-title">🧭 這篇怎麼讀（四段，可以跳）</div>
  <p>三分鐘版本：<a href="#三十秒結論"><strong>三十秒結論</strong></a> → <a href="#三、十六個-token-到底是什麼"><strong>§3 十六個 token 到底是什麼</strong></a> → <a href="#六、判讀四張表：別只看平均值"><strong>§6 判讀四張表</strong></a>。</p>
  <ul>
    <li>想懂機制：<a href="#三、十六個-token-到底是什麼">§3</a>（圖 2）、<a href="#四、三段式訓練：為什麼要先學「改寫」">§4</a></li>
    <li>想懂數字：<a href="#五、八個基準逐一對帳">§5</a>、<a href="#六、判讀四張表：別只看平均值">§6</a>（圖 3）</li>
    <li>想懂成本：<a href="#七、成本：不是變快，是不會爆">§7</a>（圖 4）</li>
    <li>想懂邊界：<a href="#九、它做不到的四件事">§9</a>、<a href="#十、所以「16-個-token」意味著什麼">§10</a></li>
  </ul>
</div>
<!-- /TOC-CARD -->

## 三十秒結論

| 問題 | 一句話回答 |
|---|---|
| **這是什麼** | 一套「記憶系統」，把整份文件庫壓成固定數量（預設 16 個）的查詢相關向量，直接餵給**凍結**的 LLM |
| **模型有被改嗎** | 沒有。Decoder 是原封不動的 Qwen3-8B；只訓練中間 194.1M 參數的 memory module |
| **16 個 token 是什麼** | 不是文字，是 16 個 d 維向量，直接寫進 decoder 的 **input embedding 空間** |
| **贏在哪** | 八個基準幾何平均 **49.68**（次佳的 xRAG 41.92），八個基準都在 Pareto 前緣 |
| **輸在哪** | PubMedQA **59.00 vs 全上下文 67.00**；需要逐字實體的問題（who／which）輸給 RAG |
| **最大的數字** | FactKG 上 16 個 token 贏過讀完全部事實的 80.43（84.33），token 少 **108×** |
| **最該看的表** | 不是準確率，是 Table 14：語料翻倍時端到端 **740 → 739 ms**，全上下文 **749 → 19,932 ms** |
| **可以用了嗎** | 還不行。研究釋出（GitHub／Hugging Face adapter），月齡、無第三方複現、無 API |

<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 480" role="img" aria-label="圖 1：傳統 RAG 與 Memorilla 的資料流對照：RAG 把 k 段原文貼進 prompt，Memorilla 只注入 16 個 soft token" style="width:100%;height:auto;display:block">
<defs><marker id="mfbbf24" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#fbbf24"/></marker><marker id="m2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="478.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩種記憶介面：給你多少文字，還是給你哪一種媒介</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">左：檢索 → 貼進 prompt → 解碼；右：編碼一次 → 查詢時讀取 → 注入解碼器</text>
<text x="48" y="118" font-size="16" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">傳統 RAG：把「文字」塞進 context</text>
<rect x="48" y="138" width="400" height="56" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="62" y="164.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">① 檢索 retrieve</text>
<text x="62" y="186.0" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">cosine 相似度挑 top-k 段落</text>
<rect x="48" y="214" width="400" height="56" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="62" y="240.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">② 貼進 prompt</text>
<text x="62" y="262.0" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">k 段原文 → prefill 隨 k 線性成長</text>
<rect x="48" y="290" width="400" height="56" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="62" y="316.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">③ 解碼 decode</text>
<text x="62" y="338.0" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">32k 上限；爆掉就得上 YaRN</text>
<path d="M 248 194 L 248 212" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#mfbbf24)"/>
<path d="M 248 270 L 248 288" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#mfbbf24)"/>
<text x="48" y="382" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">成本：每次查詢都要重讀 k 段文字，k 越大越慢。</text>
<text x="48" y="406" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">弱點：選到哪一段就只能看到哪一段（selection 的天花板）。</text>
<path d="M 486 130 L 486 420" fill="none" stroke="#222b36" stroke-width="2"/>
<text x="486" y="118" font-size="15" fill="#8b949e" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">vs</text>
<text x="524" y="118" font-size="16" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Memorilla：把「資訊」放進 embedding 空間</text>
<rect x="524" y="138" width="410" height="56" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="538" y="164.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">① 編碼一次</text>
<text x="538" y="186.0" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每份文件 → 1 個可重用向量（5 KB）</text>
<rect x="524" y="214" width="410" height="56" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="538" y="240.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">② 查詢時讀取</text>
<text x="538" y="262.0" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">16 個 slot 對「問題＋整份語料」做 cross-attention</text>
<rect x="524" y="290" width="410" height="56" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="538" y="316.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">③ 注入解碼器</text>
<text x="538" y="338.0" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">16 個 soft token 寫進 input embedding</text>
<path d="M 729 194 L 729 212" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#m2dd4bf)"/>
<path d="M 729 270 L 729 288" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#m2dd4bf)"/>
<text x="524" y="382" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">成本：永遠只給 decoder 16 個 token，語料變大延遲幾乎不動。</text>
<text x="524" y="406" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">前提：decoder 完全凍結，只訓練中間那個 memory module。</text>
<text x="48" y="452" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一句話：RAG 換「給多少文字」，Memorilla 換「給哪一種媒介」。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：傳統 RAG 與 Memorilla 的資料流對照。左邊把 k 段原文貼進 prompt，右邊只注入 16 個 soft token，decoder 全程凍結。</figcaption>
</figure>

## 一、先講清楚它在跟誰比

論文把對手分成幾類，這個分類本身就是導讀重點，因為 Memorilla 的位置卡在中間：

| 類別 | 代表 | 做法 | 卡在哪 |
|---|---|---|---|
| **代理式記憶** | MemGPT、Mem0、A-MEM | 把過去互動整理成摘要／結構化紀錄 | 最後還是把「選中的文字」放進 context |
| **檢索增強** | MemoRAG、RAG-50 | 用全域記憶引導檢索，挑 top-k 段落 | 繼承「選錯就沒了」的天花板 |
| **潛在壓縮** | ICAE、IC-Former、AutoCompressors、ComMer | 文件 → 少量 soft token | token 是**離線**算好的，同一組 token 服務所有問題 |
| **單文件版** | xRAG | 有考慮查詢相關性 | 只壓**一份**檢索到的文件 |
| **狀態型** | LongMem、MemoryLLM、Cartridges | 存 hidden state 或 KV | 記憶綁死一個模型，得訓練 LLM 或另一個快取 |

原文對缺口的描述很精準：**「還沒有一個系統，能直接把查詢相關的資訊，從文件 embedding 檢索進一個凍結 LLM 的 input embedding 空間。」**

這句話有三個關鍵字，剛好對應三個設計決定：

1. **直接**（不再經過文字）→ 所以能突破「選到哪段就只能看哪段」
2. **查詢相關**（token 隨問題變）→ 所以不是離線壓縮那一路
3. **凍結**（decoder 不動）→ 所以能力不會被訓練洗掉，記憶庫也能換模型帶著走

## 二、機制：三個步驟，兩個路徑

<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 452" role="img" aria-label="圖 2：16 個 memory token 的產生流程：學到的初始向量 → 問題殘差 → 對全部文件 cross-attention → 寫進凍結解碼器的 input embedding" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker><marker id="m58a6ff" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#58a6ff"/></marker><marker id="m2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="450.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">16 個 token 是怎麼生出來的</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">三段式：slot 初始化 → 查詢調節 → 文件檢索（Perceiver 式 latent array）</text>
<rect x="48" y="120" width="250" height="66" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="62" y="151.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">① 文件編碼</text>
<text x="62" y="173.0" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每份文件 1 個向量</text>
<rect x="48" y="206" width="250" height="66" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="62" y="237.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">② 文件庫</text>
<text x="62" y="259.0" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">200 份 ≈ 1 MB</text>
<rect x="48" y="300" width="250" height="66" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="62" y="331.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">③ 問題</text>
<text x="62" y="353.0" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">編碼成 1 個向量</text>
<rect x="352" y="108" width="300" height="272" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="502" y="136" font-size="14" fill="#2dd4bf" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">記憶槽（固定 16 個）</text>
<rect x="378" y="156" width="248" height="38" rx="8" fill="#1c2230" stroke="#2dd4bf44" stroke-width="1.5"/>
<text x="502" y="180" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">學到的初始向量 k₁ … k₁₆</text>
<rect x="378" y="210" width="248" height="38" rx="8" fill="#1c2230" stroke="#2dd4bf44" stroke-width="1.5"/>
<text x="502" y="234" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">＋問題殘差 → 每個槽各自不同</text>
<rect x="378" y="264" width="248" height="38" rx="8" fill="#1c2230" stroke="#2dd4bf44" stroke-width="1.5"/>
<text x="502" y="288" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">cross-attention ×N 讀全部文件</text>
<rect x="378" y="318" width="248" height="38" rx="8" fill="#1c2230" stroke="#2dd4bf44" stroke-width="1.5"/>
<text x="502" y="342" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出：16 × d 的 soft token</text>
<path d="M 298 153 L 376 168" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 298 239 L 376 190" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 298 333 L 376 300" fill="none" stroke="#58a6ff" stroke-width="2" marker-end="url(#m58a6ff)"/>
<rect x="700" y="108" width="250" height="272" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="825" y="136" font-size="14" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">凍結的 Qwen3-8B</text>
<text x="825" y="170" font-size="13" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">input embedding 空間</text>
<rect x="722" y="190" width="206" height="46" rx="8" fill="#0d1117" stroke="#58a6ff44" stroke-width="1.5"/>
<text x="825" y="211" font-size="13" fill="#2dd4bf" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">16 個 soft token</text>
<text x="825" y="229" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">（不是文字，是向量）</text>
<rect x="722" y="248" width="206" height="46" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>
<text x="825" y="269" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">使用者的問題</text>
<text x="825" y="287" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">純文字 token</text>
<path d="M 652 244 L 720 226" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#m2dd4bf)"/>
<text x="825" y="330" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">問題 token 與 16 個 soft token</text>
<text x="825" y="348" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">在 embedding 層串接後一起送進</text>
<text x="825" y="366" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">32 層 Transformer（權重不動）</text>
<text x="48" y="404" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">關鍵：解碼器權重一個都沒動（凍結）；被訓練的只有中間 194.1M 參數的 memory module。</text>
<text x="48" y="428" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">所以「16」是輸出預算，不是壓縮率的上限——它是一個可以調的旋鈕（見 §五 ablation）。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：16 個 memory token 的產生流程。學到的初始向量先被問題調節，再對全部文件做 cross-attention，最後以向量形式寫進凍結解碼器的 input embedding 空間。</figcaption>
</figure>

整個系統可以想成一條**寫入路徑**加一條**讀取路徑**，這個分法在 §7 的成本分析裡會再出現一次。

### 寫入路徑（每份文件付一次）

一份文件（一個對話 session、一個書章）交給**凍結的 encoder**（預設 Qwen3-Embedding-4B），變成**一個向量** $e_d$。文件庫就是一堆這種向量。原文算過大小：200 份文件約 **1 MB**，每份 **5 KB**。

這一點很重要——它跟一般的稠密檢索索引用的是**同一個物件**，所以寫入成本是「共用」而不是「額外」。

### 讀取路徑（每次查詢付一次）

給定問題 $q$，先編碼成 $e_q$，然後一個可訓練的記憶模組輸出**固定 $K$ 個**向量：

$$M(q) = \mathrm{MemoryModule}\left(e_q,\ \{e_d\}_{d=1}^{N}\right) \in \mathbb{R}^{K \times d_{\text{LLM}}}$$

這 $K$ 列就是 memory tokens。它們不是文字 token，而是**直接落在 decoder 的 input embedding 空間**裡，跟使用者打字的向量排在一起送進去。論文寫得很白：不論文件庫多大，模組「永遠只貢獻 $K$ 個 token」。

## 三、十六個 token 到底是什麼

這是整篇最容易誤解的地方，值得拆到最細。記憶模組是三段式（原文 §2.2），設計借自 **Perceiver 的 latent array**。

### 階段 1：記憶槽初始化

先準備 $K$ 個**學到的**初始向量 $k_1,\dots,k_K$，所有文件庫、所有查詢共用同一組。這一步定下了「輸出預算」：之後不管輸入多大，輸出永遠是 $K$ 列；不同初始值讓每個槽可以各自負責不同種類的資訊。

### 階段 2：查詢調節（query conditioning）

讓這些槽去 attend 問題向量：$h_i = k_i + \mathrm{Attn}(k_i,\ e_q)$。

因為 $e_q$ 只有**一個**向量，它給所有槽的是**同一個**更新量；靠殘差連接，槽與槽原本的差異被保留下來。結果是：**每個槽都更貼近這個問題，但仍保有各自的個性。**

這一步就是它與「離線壓縮」分道揚鑣的地方——同一份文件庫，換一個問題，出來的 16 個向量就不一樣。

### 階段 3：文件檢索（document retrieval）

調節過的槽再對**全部**文件 embedding 做 cross-attention（$N$ 個 block，Perceiver 式）。因為是對整個文件庫做注意力、而不是挑 top-k，所以它是「一次讀完全部、但只留下 $K$ 個摘要」。

### 所以「16」是什麼、不是什麼

| 常見誤解 | 實際上 |
|---|---|
| 16 是壓縮率上限 | ❌ 它是**輸出預算**；壓縮率是「文件 token 數 ÷ 16」，NarrativeQA 上是 67,385 ÷ 16 ≈ **4,211×** |
| 16 是模型自己算出來的結論 | ❌ 是**超參數**。§6.4 的 ablation 顯示 8→16 有差、16→128 幾乎沒差（四項變動 < 1 分） |
| 16 代表「記住 16 件事」 | ❌ 單一 token 不是一件事；它是分散式表示，論文自己也說它擅長「關係」、不擅長「逐字」 |
| 這 16 個 token 是文字 | ❌ 不是文字，是向量。decode 它得不到任何句子 |

還有一個容易漏掉的細節：TextWorld 代理任務用的是 **8 個** token，不是 16。所以「16」連論文自己都沒當成定律。

## 四、三段式訓練：為什麼要先學「改寫」

只訓練記憶模組（decoder 與 encoder 都凍結），但訓練分成三個課程階段，順序不能亂：

| 階段 | 資料 | 學什麼 | 規模 |
|---|---|---|---|
| **① 通用初始化** | 英文維基百科改寫重建 | 在固定預算下「保住足夠資訊讓凍結模型改寫出來」 | 198 萬筆 |
| **② 多樣任務** | 閱讀理解、開放域 QA、摘要共 10 個資料集 | 不同來源結構 → 該從同一份表示裡回想什麼 | 134 萬筆 |
| **③ 領域微調** | 八個評測基準的訓練集混合 | 貼近評測分布（PMv2、PV4 另外多跑幾輪） | — |

第一階段為什麼是「改寫」而不是「問答」？因為它要驗證的是**保真度**：如果 16 個向量漏掉關鍵細節，凍結的模型就寫不出接近原意的改寫。這是一個不需要標註答案、又能直接量測「有沒有漏」的目標。

第二階段才是「教它挑重點」。第三階段已經是在考題上微調了——這一點在讀數字時要記得（見 §5 末的提醒）。

## 五、八個基準逐一對帳

論文跑八個基準，全部用**同一個凍結的 Qwen3-8B decoder**，所以這張表比一般的論文表格乾淨：

| 類別 | 基準 | 量什麼 |
|---|---|---|
| 個人化 | PersonaMem-v2（PMv2） | 跨多輪對話累積的使用者偏好 |
| 個人化 | PersonalizationV4（PV4） | 跨使用者寫作歷史整合 |
| 個人化 | LaMP-4／LaMP-7 | 個人化標題／摘要生成 |
| 長文件 QA | NarrativeQA | 整本書問答 |
| 長文件 QA | TriviaQA | 長文件事實問答 |
| 知識密集 | FactKG | 多實體關係事實查核 |
| 知識密集 | PubMedQA | 生醫文獻問答 |

### 贏的地方

| 基準 | Memorilla | 最強對手 | 備註 |
|---|---|---|---|
| **FactKG（acc）** | **84.33** | 80.43（全上下文） | 同樣答案，token 少 108× |
| **PMv2（acc）** | **44.60** | 30.90（xRAG） | 全上下文只有 27.92，且用了 1,974 倍 token |
| **幾何平均** | **49.68** | 41.92（xRAG）／40.75（LLMLingua-2）／38.02（Mem0） | 八個基準平均 |

PMv2 那個數字最值得停下來看：**44.60 vs 27.92**，而全上下文用了將近兩千倍的 token。這不是「同樣的答案換個講法」，而是**換了一個答案**——原文的說法是 "a different answer"。

### 輸的地方（原文自己列的）

| 基準 | Memorilla | 對手 | 差距 |
|---|---|---|---|
| PubMedQA（acc） | 59.00 | 69.00（LLMLingua-2）／67.00（全上下文） | **−8 到 −10** |
| NarrativeQA（ROUGE-L） | 19.31 | 20.51（MemoRAG） | −1.20 |
| PV4（acc） | 66.65 | 67.88（Mem0） | −1.23 |

PubMedQA 的落後很誠實，而且有解釋：醫療問題常常需要**精確的事實片段**（劑量、基因名、統計數字），而壓縮擅長的是**整體結構**。這一條在 §8 有更細的證據，也是論文自己承認的限制。

## 六、判讀四張表：別只看平均值

### 6.1 換個疑問詞，勝負就換人

Figure 4 把 NarrativeQA 按**問題的第一個字**分類，結果非常乾淨：

| 問題類型 | 誰贏 | 差距 |
|---|---|---|
| **why**（為什麼） | Memorilla | **+4.91** ROUGE-L |
| **how**（如何） | Memorilla | **+7.02** |
| who（誰） | RAG-50 | +3.45 |
| which（哪一個） | RAG-50 | +2.93 |

原文的解釋很直白：**壓縮保留全域結構（因果、敘事），檢索保留逐字表徵（實體名稱）**。所以你問「這段關係最後為什麼破裂」，記憶贏；你問「那個角色叫什麼名字」，檢索贏。

這代表**平均分數對這兩類問題幾乎沒有意義**，因為它們是互補的。Figure 5 甚至算了「兩者聯集」的上界：每個基準上，聯集都高於任何單一方法。FactKG 上 15.9% 的題目只有 Memorilla 答對、10.0% 只有 RAG 答對；PMv2 則是 27.1% vs 9.2%。

### 6.2 事實越多，記憶越贏

FactKG 的優勢隨**實體數量**單調擴大：1 個實體時 +4.23pp，4 個以上時 **+7.59pp**。而 RAG-50 在串接事實從 1 條變成 4 條時，分數從 78.73 掉到 **51.75**，Memorilla 則一直待在 80–89。

原因不難想：**一次讀完全部**的表示可以把跨文件的關係一起編碼；而檢索一旦需要跨多份文件推理，就會出現「檢索不到的證據」。

### 6.3 兩邊都答錯的題目長什麼樣

原文也檢查了「兩邊都錯」的題目：

- **PV4**：很多題需要把散落各處的事實**串起來**，所以剩下的錯誤是「組合」而不是「找不到」。
- **FactKG**：兩邊都錯的題目裡 **89.5% 是真敘述**（被判成假），而兩邊都對的題目裡真敘述只占 28.7%——這是**決策門檻校準**問題，不是證據不足。

判讀時記住：**它測的是「檢索＋注入」這條管線，不是推理能力。**

### 6.4 「16」的 ablation：8→16 有感，16→128 幾乎沒感

| 對照 | 發現 |
|---|---|
| 訓練時 $K$：8 → 16 → 128 | 四項變動 < 1 分；**PMv2 與 PV4 反而下降**，所以全篇固定 $K=16$ |
| 推論時砍 token | PMv2 到 4 個都還在「閉卷水準」（26.58 vs 25.64），**到 16 才跳上 44.60** |
| 換 encoder：4B → 8B | 每項變動 ≤ 1.3；PubMedQA 的 +3.00 只等於 100 題裡的 3 題 |
| 凍結 vs LoRA | rank-130 LoRA（268.4M 參數）每一項主指標都輸給 Memorilla（194.1M）；拔掉真實文件後 FactKG 掉 5.93 |

最後一列是最有說服力的：**把文件換成假的，分數就崩了**。這證明功勞來自「庫裡的證據」，不是「記憶模組本身適配了這個任務」。

> 同一列也提醒你：§5 的數字是**領域微調過的**（第三階段就是在這八個基準的訓練集上訓練）。所以「贏過全上下文」要理解成「在相同訓練條件下贏」，不是「零樣本就能贏」。

<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" role="img" aria-label="圖 3：八個基準的 token 數與分數取捨：Memorilla 落在每個基準的 Pareto 前緣，16 個 token 就拿到幾何平均 49.68" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="958.5" height="518.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">為什麼「16 個 token」值得在意</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">橫軸是每查詢文件 token 數（對數），縱軸是主指標分數</text>
<path d="M 130 400 L 820 400" fill="none" stroke="#8b949e" stroke-width="1"/>
<path d="M 130 400 L 130 150" fill="none" stroke="#8b949e" stroke-width="1"/>
<path d="M 130.0 400 L 130.0 406" fill="none" stroke="#8b949e" stroke-width="1"/>
<text x="130.0" y="424" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<path d="M 268.0 400 L 268.0 406" fill="none" stroke="#8b949e" stroke-width="1"/>
<text x="268.0" y="424" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10</text>
<path d="M 406.0 400 L 406.0 406" fill="none" stroke="#8b949e" stroke-width="1"/>
<text x="406.0" y="424" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">100</text>
<path d="M 544.0 400 L 544.0 406" fill="none" stroke="#8b949e" stroke-width="1"/>
<text x="544.0" y="424" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1k</text>
<path d="M 682.0 400 L 682.0 406" fill="none" stroke="#8b949e" stroke-width="1"/>
<text x="682.0" y="424" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10k</text>
<path d="M 820.0 400 L 820.0 406" fill="none" stroke="#8b949e" stroke-width="1"/>
<text x="820.0" y="424" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">32k</text>
<text x="96" y="426" font-size="12" fill="#8b949e" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">文件 token</text>
<text x="100" y="142" font-size="12" fill="#8b949e" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">分數</text>
<circle cx="785.5" cy="275.0" r="7.5" fill="#fbbf24"/>
<text x="773.5" y="257.0" font-size="12.5" fill="#fbbf24" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全上下文 full context</text>
<circle cx="557.8" cy="245.0" r="7.5" fill="#c084fc"/>
<text x="547.8" y="229.0" font-size="12.5" fill="#c084fc" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">MemoRAG</text>
<circle cx="557.8" cy="310.0" r="7.5" fill="#7d8590"/>
<text x="549.8" y="336.0" font-size="12.5" fill="#7d8590" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RAG-50</text>
<circle cx="364.6" cy="262.5" r="7.5" fill="#f472b6"/>
<text x="376.6" y="250.5" font-size="12.5" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">xRAG / LLMLingua-2</text>
<circle cx="364.6" cy="330.0" r="7.5" fill="#7d8590"/>
<text x="376.6" y="348.0" font-size="12.5" fill="#7d8590" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Mem0</text>
<circle cx="157.6" cy="200.0" r="7.5" fill="#2dd4bf"/>
<text x="171.6" y="188.0" font-size="12.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Memorilla（16 tok）</text>
<text x="48" y="470" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">幾何平均分數：Memorilla 49.68｜xRAG 41.92｜LLMLingua-2 40.75｜Mem0 38.02。</text>
<text x="48" y="494" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">相對全上下文少 394× token、相對 RAG-50 少 113×、相對 MemoRAG 少 49×。左上角才是我們真正想要的角落。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 3：每查詢文件 token 數（對數軸）與分數的取捨。Memorilla 在 16 個 token 就取得幾何平均 49.68，其餘方法要嘛 token 更多、要嘛分數更低。</figcaption>
</figure>

## 七、成本：不是變快，是不會爆

論文 Appendix F 的 Table 14 是整篇最被低估的部分。設定：**單張 H100-80GB、batch size 1、bf16、greedy、max_new_tokens=32、每份文件 250 token**，量 5 次取中位數（先熱身 2 次）。語料從 200 份長到 400 份：

| 路徑 | 項目 | 200 份 | 400 份 | 成長 |
|---|---|---|---|---|
| 寫入 | 文件編碼 | 22.92 ms | 2,588.84 ms | 線性 |
| 寫入 | 每份文件儲存 | 5 KB | 5 KB | 不變 |
| 讀取 | Memory module forward | 2.01 ms | 1.96 ms | **−0.06 ms** |
| 讀取 | CPU→GPU 搬移 | 0.014 ms | 0.060 ms | 占延遲 < 0.04% |
| 讀取 | **Memorilla 端到端** | **740 ms** | **739 ms** | **−1.9 ms** |
| 讀取 | **Full Context 端到端** | **749 ms** | **19,932 ms** | **+19,184 ms** |

兩個重點：

1. **語料翻倍，Memorilla 的端到端還快了 1.9 ms。** 它讀的是固定 16 個 token，多出來的文件只影響那一次 cross-attention（2 ms 那個量級），decoder 的負擔完全沒變。絕對延遲由**解碼**主導，所以「單次查詢不會更快」——740 ms 與 749 ms 幾乎一樣。
2. **全上下文直接撞牆。** 400 份文件是 128,064 個 context token，早就超過強制的 32,768 上限，只能開 YaRN（factor 4）。19,932 ms 裡有很大一部分是這個代價。

還有一個順手的數字：PV4 上如果把文件留在 KV cache，是 50,455 個 document token × 144 KiB/token（Qwen3-8B bf16）≈ **6.9 GiB**；而記憶庫是 200 個 2,560 維向量，**小 7,266 倍**。

所以真正的賣點不是「更快」，而是：**服務成本不隨語料膨脹**。這對「使用者的歷史一直在長」的助理型應用才是關鍵——你的 context 不會有一天突然裝不下。

<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" role="img" aria-label="圖 4：服務成本隨語料成長：Memorilla 端到端 740 → 739 ms，full context 749 → 19,932 ms" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="958.5" height="538.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">省的不是算力，是「不會爆掉」</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">左：寫入路徑；右：讀取路徑（H100-80GB, batch 1, bf16）</text>
<text x="48" y="118" font-size="15" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">寫入路徑（每份文件只付一次）</text>
<rect x="48" y="140" width="400" height="58" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="64" y="164" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">文件編碼 200 → 400 份</text>
<text x="64" y="184" font-size="12.5" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">22.92 → 2,588.84 ms</text>
<text x="432" y="175" font-size="12" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">線性成長</text>
<rect x="48" y="212" width="400" height="58" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<text x="64" y="236" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每份文件儲存</text>
<text x="64" y="256" font-size="12.5" fill="#3fb950" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5 KB → 5 KB</text>
<text x="432" y="247" font-size="12" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不變</text>
<rect x="48" y="284" width="400" height="58" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="64" y="308" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">kv cache 對照（PV4）</text>
<text x="64" y="328" font-size="12.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6.9 GiB</text>
<text x="432" y="319" font-size="12" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">記憶庫小 7,266×</text>
<rect x="48" y="356" width="400" height="58" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="64" y="380" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 寫入成本與 RAG 共用</text>
<text x="64" y="400" font-size="12.5" fill="#7d8590" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一次索引，多次查詢</text>
<text x="432" y="391" font-size="12" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不是額外開銷</text>
<path d="M 486 110 L 486 470" fill="none" stroke="#222b36" stroke-width="2"/>
<text x="524" y="118" font-size="15" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">讀取路徑（每次查詢都付）</text>
<rect x="524" y="140" width="400" height="64" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<text x="540" y="163" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Memory module forward</text>
<text x="540" y="184" font-size="13.5" fill="#3fb950" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2.01 ms → 1.96 ms</text>
<text x="908" y="184" font-size="11.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">語料翻倍還更快</text>
<rect x="524" y="216" width="400" height="64" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<text x="540" y="239" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">CPU → GPU 搬移</text>
<text x="540" y="260" font-size="13.5" fill="#3fb950" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.014 → 0.060 ms</text>
<text x="908" y="260" font-size="11.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">占延遲 &lt; 0.04%</text>
<rect x="524" y="292" width="400" height="64" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="540" y="315" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Memorilla 端到端</text>
<text x="540" y="336" font-size="13.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">740 ms → 739 ms</text>
<text x="908" y="336" font-size="11.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">幾乎不動</text>
<rect x="524" y="368" width="400" height="64" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="540" y="391" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Full Context 端到端</text>
<text x="540" y="412" font-size="13.5" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">749 ms → 19,932 ms</text>
<text x="908" y="412" font-size="11.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">爆 32k，得開 YaRN</text>
<text x="48" y="508" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同機實測（H100-80GB、batch 1、bf16、max_new_tokens=32）：好處不是單次查詢更快，而是「服務成本不隨語料膨脹」。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 4：語料從 200 份長到 400 份時的服務成本。Memorilla 端到端幾乎不動（740→739 ms），全上下文則從 749 ms 漲到 19,932 ms 並撞上 32k 上限。</figcaption>
</figure>

## 八、它到底學到了什麼

這一節回答「16 個向量怎麼可能夠」。論文個案研究（Figure 6）挑了一個例子：使用者一句泛泛的提問，字面上跟「缺鐵性貧血」毫無重疊，但 Memorilla 從記憶裡把這段病史拉出來，答對了。

| 能力 | 證據 |
|---|---|
| **跨文件關係** | FactKG 優勢隨實體數單調上升（+4.23pp → +7.59pp） |
| **語意而非字面** | PMv2 個案：問題與相關記憶**沒有詞彙重疊**，仍被取用 |
| **關係而非逐字** | 概念題（why／how）贏，實體題（who／which）輸 |
| **可組合性** | FactKG 串接 1→4 條事實：RAG 78.73→51.75，Memorilla 維持 80–89 |

反過來，它**不擅長**的東西也很一致：**精細事實**。原文的解釋是 encoder 從來沒有為了「壓縮」而訓練過（Qwen3-Embedding 是做檢索用的），所以細節在寫入那一步就已經掉了。

## 九、它做不到的四件事

導讀不該只講優點。以下四點，原文寫在 Limitations，或是從實驗設計可以推出來：

| 做不到 | 依據 |
|---|---|
| **精細事實會掉** | PubMedQA −8；原文："can lose fine-grained factual details" |
| **不能跟 RAG 互換** | FactKG 15.9%／PMv2 27.1% 是「只有記憶才會」的題目，聯集才是上界 |
| **跨模型家族未驗證** | 全篇都是 Qwen encoder + Qwen decoder，換家族是 future work |
| **不是產品** | 沒有 API、沒有託管服務；八個基準的表沒有第三方複現過 |

還有一條是從實驗設定推出來的：**每個基準都有自己的訓練階段**。這在學術上完全正常，但如果你的用途是「拿來就用」，這個「每個任務都要重新訓一輪」的前置成本要先算進去。

要自己動手的路徑大概是：`snap-stanford/memorilla` 上有五個訓練好的記憶 adapter（`memory.pt`，三個訓練階段各一、個人化兩個），全部對應原封不動的 Qwen3-8B；專案頁在 `memory.stanford.edu`。

## 十、所以「16 個 token」意味著什麼

回到開頭那句話。拆完之後我會這樣改寫：

> **不是「AI 用 16 個 token 記住了一切」，而是「給凍結模型的東西，可以不是文字」。**

這個轉向的意義有三層：

1. **它把「context 不夠長」重新定義成「介面選錯了」。** 過去兩年大家在比 context window 長度，Memorilla 的立場是：與其買更大的窗戶，不如換一種窗戶。
2. **它讓記憶變成可攜的。** 記憶庫裡只有向量（每份 5 KB），decoder 完全沒被動過。換模型不用重練記憶——這是 KV cache 派系做不到的。
3. **但它也示範了壓縮的代價是「選擇性」。** 要全域結構，就會掉逐字細節；要 why／how，就會輸 who／which。原文最誠實的一句其實是：最好的下一步是**混合**——用潛在記憶抓全域結構、用文字檢索抓精確實體。

如果要把這篇放進你的技術地圖，我的建議是：**把它當「RAG 的鄰居」，不是「RAG 的替代品」。** 它證明了 soft token 這條路在個人化與知識密集問答上真的有競爭力（而且在 token 預算上碾壓），但在需要精確字串、需要出處引用、需要可稽核的場合，它現在還贏不了檢索。

<!-- FOOT-CARD -->
<div class="callout">
  <div class="callout-title">📎 出處與可重現性</div>
  <ul>
    <li><strong>論文</strong>：<em>Memorilla: Latent Semantic Memory for LLMs</em>，arXiv:2610.21375（v1 2026-10-15，v3 2026-11-03）</li>
    <li><strong>作者</strong>：Adibvafa Fallahpour、Parsa Idehpour、Vignesh Kothapalli、Nikita Mounier、Shirley Wu、Shayan Pardis、Jure Leskovec（Stanford／Toronto／Vector／UPenn／MIT）</li>
    <li><strong>專案頁</strong>：<a href="https://memory.stanford.edu/">memory.stanford.edu</a>｜<strong>程式碼</strong>：<code>snap-stanford/memorilla</code></li>
    <li><strong>數字來源</strong>：本文與附錄（Table 14、Figure 4／5／9／10／11／12、§2.2、§2.6、§7、附錄 E）；沒有另行換算或四捨五入成好看的形式</li>
    <li><strong>引述慣例</strong>：英文短句（"a different answer"、"can lose fine-grained factual details"）為原文照錄</li>
  </ul>
</div>
<!-- /FOOT-CARD -->
