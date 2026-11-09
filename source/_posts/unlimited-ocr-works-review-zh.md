---
title: '評測 Unlimited-OCR：百度把 DeepSeek-OCR 的 KV cache 釘死了，「一次掃完幾十頁」是真的'
date: 2026-11-09 23:45:00
categories:
  - AI 研究札記
  - 技術筆記
tags:
  - Unlimited-OCR
  - Baidu
  - 百度
  - OCR
  - DeepSeek-OCR
  - R-SWA
  - KV cache
  - 長文檔解析
  - OmniDocBench
  - 開源權重
  - MIT
  - arXiv
toc: true
index_img: /img/covers/unlimited-ocr-works-review-zh.png
banner_img: /img/covers/unlimited-ocr-works-review-zh.png
---

社群上又瘋傳一篇 LinkedIn 貼文：「中國開發者又領先時代了 💀 百度剛丟出一個 3B 的 OCR 模型，一次能掃幾十頁文件、KV cache 不隨輸出膨脹、完全免費 MIT 開源」，後面還附了一個中間帶空格的連結（`huggingface. co/baidu/Unlimited-OCR`——這是 LinkedIn 規避站外連結降觸及的標準手法）。

照經驗，這種格式十之八九是流量農場在講不存在的模型。這次實際去查：**repo 是真的、論文是真的，連 DeepSeek-OCR 作者本人都跑到 Hugging Face 論文頁留言「Cool！」**。但「剛發佈」是假的——模型五個月前就出了，而且已經有第二代。以下是把模型卡、兩篇 arXiv 論文、GitHub 上 63 個 open issues 全部對過一遍之後的完整評測，所有數字都對回原始來源。

<!-- more -->

> **一句話總結**：Unlimited-OCR 把「長文檔 OCR」真正推進了一個檔位——解碼全程 KV cache 恆定有 kernel 層級的硬數據撐腰，OmniDocBench 93.23 也確實贏過 DeepSeek-OCR；但它是**長程解析特化**的武器，圖表、小語種、單頁輕量場景都不是它的戰場，而且 Hugging Face 端的後處理程式碼還藏了一個 `eval()` 安全隱患。

## 三十秒結論

| 問題 | 一句話回答 |
|---|---|
| **這是什麼** | 百度以 DeepSeek-OCR 為底改造的端到端 OCR：沿用其高壓縮視覺編碼器，把 3B MoE decoder 的注意力層全部換成 R-SWA（v1）／SR-SWA（v2） |
| **核心賣點** | 解碼全程 **KV cache 恆定**，不隨輸出長度膨脹 → 單次 forward 掃完數十頁（v1），v2 更到百頁級 |
| **最硬的數字** | OmniDocBench v1.5 總分 **93.23 vs DeepSeek-OCR 87.01**；v2 在百頁規模每步解碼比 Full Attention 快 **7.0×** |
| **最大弱點** | 圖表理解（第三方 ParseBench 的 chart 項只有 **1.34/100**）、希伯來／阿拉伯文會產生幻覺 token、每頁比 Tesseract 慢 8–19× |
| **安全性** | ⚠️ HF 端座標後處理用 `eval()` 執行模型輸出的字串（issue #115），惡意文件圖片理論上可注入程式碼；另有 2 個 critical security issue（#113） |
| **授權** | MIT，權重與程式全開，可商用 |
| **誰該用** | 長 PDF／合約／整本書的批次解析 → 直接上 **v2**；單頁發票收據的大量輕量處理 → 留在 PaddleOCR／Tesseract |

<!-- TOC-CARD -->
<div class="callout">
  <div class="callout-title">🧭 這篇怎麼讀</div>
  <p>三分鐘版本：<a href="#三十秒結論"><strong>三十秒結論</strong></a> → <a href="#二、技術核心：R-SWA-怎麼把-KV-cache-釘死"><strong>§2 技術核心</strong></a> → <a href="#七、評分卡"><strong>§7 評分卡</strong></a>。</p>
  <ul>
    <li>想驗證貼文真偽：<a href="#一、先驗貨：那則貼文哪裡真、哪裡灌水">§1</a></li>
    <li>想懂機制：<a href="#二、技術核心：R-SWA-怎麼把-KV-cache-釘死">§2</a>（圖 1）、<a href="#三、版本地圖：你該裝的是-v2">§3</a></li>
    <li>想看數字：<a href="#四、基準對帳：官方-vs-第三方">§4</a></li>
    <li>想看實測災情：<a href="#五、63-個-open-issues-告訴你的事">§5</a>、<a href="#六、部署與硬體">§6</a></li>
  </ul>
</div>
<!-- /TOC-CARD -->

## 一、先驗貨：那則貼文哪裡真、哪裡灌水

| 貼文宣稱 | 查證結果 |
|---|---|
| 3B 參數 | ✅ BF16 權重共 3,336,106,240 參數（約 6.7 GB） |
| 一次掃幾十頁 | ✅ 論文原文：「transcribe dozens of pages of documents in a single forward pass under a standard maximum length of 32K」 |
| KV cache 不隨生成 token 增長 | ✅ 這正是論文的核心貢獻 R-SWA，不是行銷話術 |
| 免費、開放權重、MIT | ✅ repo 標示 `license: mit`，含 LICENSE 檔，不設 gated |
| 「剛發佈」 | ❌ v1 於 **2026/06/22** 發表（貼文流傳時已五個月），v2 也已於 **2026/10/27** 釋出 |
| 來源連結 | ⚠️ 連結中間的空格是 LinkedIn 流量手法，但 repo 本身確實存在：5.4M 下載、31k GitHub stars |

補一個有趣的細節：論文標題 *Unlimited OCR Works* 是在捏他《Fate/stay night》的 "Unlimited Blade Works"，Hugging Face 論文頁的最高讚留言就是整段英文詠唱改編（"Pixels are my body, and tokens are my blood..."）。百度 ERNIE 團隊的宅度，認證通過。

## 二、技術核心：R-SWA 怎麼把 KV cache 釘死

**問題**：端到端 OCR 拿 LLM 當 decoder，輸出的每個 token 都會在 KV cache 裡留下一筆。文件越長，cache 越肥，注意力計算量也跟著線性成長——於是模型「越抄越慢」，跟人類抄寫時效率不變的特性完全相反。

**作法**：保留 DeepSeek-OCR 的 DeepEncoder（把整頁高解析影像壓成極少量視覺 token），把 decoder 的所有注意力層換成 **R-SWA（Reference Sliding Window Attention）**。每個生成中的 token 只能看兩類東西：

1. **全部 reference token**——視覺 token 與 prompt，永遠可見、永不逐出；
2. **前 128 個輸出 token**——一個固定大小的滑動窗口，舊的輸出隨窗口前進被逐出 cache。

於是 cache 大小 = reference（固定，取決於輸入頁數）+ 128（常數），**與輸出長度完全無關**。和 vanilla SWA 的關鍵差異在於：reference token 不參與狀態轉移，視覺資訊不會隨窗口滑動被「漸進式模糊」掉。訓練方式是從 DeepSeek-OCR checkpoint 續訓：約 200 萬筆文件 OCR 樣本、4,000 步，編碼器凍結、只訓 LLM。

硬數據在 kernel 層：論文量測 Flash Attention v3 的**單次 kernel 呼叫耗時**，DeepSeek-OCR 隨解碼步數持續上升（後段還有 KV cache 對齊造成的尖峰），Unlimited-OCR 則全程貼底平坦：

<!-- FIG1 -->
<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 420" role="img" aria-label="注意力 kernel 單次呼叫耗時：DeepSeek-OCR 隨解碼步數上升，Unlimited-OCR 平坦" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto"><rect x="0.75" y="0.75" width="938.5" height="418.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="48" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">注意力 kernel 單次呼叫耗時 vs 解碼步數</text><text x="48" y="68" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">概念圖，依據論文 §3.4.3 kernel study 的曲線描述重繪（越低、越平越好）</text><line x1="90" y1="340" x2="890" y2="340" stroke="#30363d" stroke-width="1.5"/><line x1="90" y1="100" x2="90" y2="340" stroke="#30363d" stroke-width="1.5"/><line x1="90" y1="280" x2="890" y2="280" stroke="#21262d" stroke-width="1" stroke-dasharray="4 4"/><line x1="90" y1="220" x2="890" y2="220" stroke="#21262d" stroke-width="1" stroke-dasharray="4 4"/><line x1="90" y1="160" x2="890" y2="160" stroke="#21262d" stroke-width="1" stroke-dasharray="4 4"/><text x="880" y="362" font-size="12" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">decode step → 6,000</text><text x="60" y="110" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">µs</text><path d="M 110 322 C 300 300, 500 250, 700 190 L 760 175 L 780 128 L 800 168 C 830 155, 860 140, 880 132" fill="none" stroke="#fbbf24" stroke-width="3" stroke-linecap="round"/><path d="M 110 328 C 350 326, 600 325, 880 324" fill="none" stroke="#2dd4bf" stroke-width="3" stroke-linecap="round"/><rect x="600" y="88" width="270" height="58" rx="10" fill="#161b22" stroke="#30363d"/><line x1="616" y1="108" x2="652" y2="108" stroke="#fbbf24" stroke-width="3" stroke-linecap="round"/><text x="662" y="112" font-size="12.5" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">DeepSeek-OCR（full attention）</text><line x1="616" y1="132" x2="652" y2="132" stroke="#2dd4bf" stroke-width="3" stroke-linecap="round"/><text x="662" y="136" font-size="12.5" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Unlimited-OCR（R-SWA）</text><text x="790" y="116" font-size="11" fill="#fbbf24" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">cache 對齊尖峰</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：同樣的輸入，DeepSeek-OCR 的注意力成本隨輸出變長而上升；R-SWA 因為 cache 被封頂，<strong>第 6,000 個 token 和第 1 個 token 的解碼成本一樣</strong>。</figcaption>
</figure>
<!-- /FIG1 -->

## 三、版本地圖：你該裝的是 v2

| | **v1**（2026/06/22） | **v2**（2026/10/27） |
|---|---|---|
| 注意力機制 | R-SWA：reference 全看、輸出只看 128 | **SR-SWA**（Sparse R-SWA）：連 reference 也限量，只聚焦「正在抄寫的頁面」 |
| 每步解碼成本 | 恆定，但 **prefill 仍隨頁數增長** | 恆定，**與文件總長無關** |
| 實用規模 | 數十頁／32K 上限 | 百頁級，官方稱「unlimited-horizon」（展示整本書單次請求掃完） |
| 百頁規模速度 | baseline | 比 Full Attention 快 **7.0×**、比 v1 的 R-SWA 快 **5.6×** |
| 基準 | OmniDocBench 93.23 | 官方稱 MPDocBench 與新基準 **MarathonDocBench**（百頁級）端到端 SOTA |
| 服務生態 | transformers／vLLM | SGLang（`<PAGE>` token＋每頁輸出上限 20k token 的頁面守衛） |

v1 論文自己很誠實：「still has a finite context length, and the prefill grows as pages are added」——也就是說 v1 的「unlimited」有名無實，頁數一多，prefill 的成本與記憶體照樣爆炸。v2 的 SR-SWA 把 reference token 也加上固定容量上限，才補上這最後一塊。作者群把這稱作「OCR 3.0 時代」：pipeline 切片（1.0）→ 端到端單頁（2.0）→ 無限長度單次解析（3.0）。

## 四、基準對帳：官方 vs 第三方

**官方數字（v1 論文）**：OmniDocBench v1.5 總分 **93.23**，對 DeepSeek-OCR 的 **87.01**，淨贏 6.22 分。長程自測（自家挑選的小說／文件／論文，按頁數分組）：

| 頁數 | Edit distance ↓ | Distinct-35 ↑ | 判讀 |
|---|---|---|---|
| 20 | 0.0572 | — | 很穩 |
| 40+ | 0.1069 | 96.90% | 誤差接近翻倍，但**沒有崩壞成重複迴圈**（Distinct-35 維持高檔）；作者歸因於小字難辨 |

兩個必須打的折扣：

1. **沒有消融實驗**（alphaXiv 的評論點出）：+6.22 分是「續訓 200 萬筆資料」與「換 R-SWA」的混合效果，論文沒有提供「同樣續訓但保留原始注意力」的對照組，所以增益不能全記在 R-SWA 頭上。
2. **第三方成績單很普通**：Hugging Face 上有一筆未驗證的 ParseBench 提交——Mean 46.17、Text Content 86.81、Layout 71.52、Table 70.21，而 **Chart 只有 1.34/100**。ParseBench 本身偏 RAG 抽取場景、且非官方提交，參考價值有限，但「圖表理解是短板」這個訊號與 issue 區的回報一致。

## 五、63 個 open issues 告訴你的事

模型卡不會寫的，issue 區會。把 63 個 open issues 歸納成六類災情：

| 類別 | 代表 issue | 嚴重度 |
|---|---|---|
| **重複／退化迴圈** | llama.cpp 下無限重複（#82）；vLLM 掃專利 ST.25 序列時數字變異循環（#84）；v2 在 GB10／SM121 上 SGLang 從第一個 token 就退化（#114） | 🔴 |
| **安全隱患** | HF 端座標後處理用 `eval()` 執行模型輸出的字串——惡意文件圖片理論上可注入 Python（#115）；另有 2 個 critical security issue（#113） | 🔴 |
| **小語種翻車** | 希伯來文輸出幻覺 token（#90）；阿拉伯文解析問題與 arafix 討論（#89、#95） | 🟠 |
| **絕對速度慢** | R&D 團隊實測每頁比 Tesseract 慢 **8–19×**，輕量 ingestion pipeline 直接放棄（#100） | 🟠 |
| **工程品質** | infer.py 輸入驗證在模型載入後才跑、全部失敗也 exit 0、子目錄檔名碰撞（#102–#105）；多頁分隔符不穩（#107） | 🟡 |
| **邊緣場景** | 旋轉文字漏行且多生出假行（#79）；Apple Silicon MPS 中途崩潰、CPU 要手動拔掉寫死的 `.cuda()`（#81） | 🟡 |

值得注意的是維護活躍度不差（31k stars、issue 有官方回覆、vLLM／SGLang／ms-swift 社群都進場支援），但**上生產前請先把 #115 的 `eval()` 拔掉**，並對輸出加上 n-gram 重複守衛（官方推論範例其實有內建 `NoRepeatNGram`，記得開）。

## 六、部署與硬體

- **權重**：BF16 約 6.7 GB，一張 RTX 4090 24 GB 綽綽有餘，社群也有 GGUF 量化可跑更小的卡。
- **生態**：transformers（v1）／vLLM（v1）／SGLang（v2）／ms-swift 微調／ModelScope／Baidu Cloud，Hugging Face Spaces 有官方 demo 可免裝先玩。
- **Python 版本坑**：官方只測過 **Python 3.12 + torch 2.10 + CUDA 12.9**。系統若是最新的 Python 3.15，直接裝大概率踩 wheel 相容性的坑——老實開一個 3.12 的 venv。
- **Windows 本機**：transformers 路線可行（純 PyTorch）；vLLM／SGLang 建議走 WSL2 或 Linux 主機。

## 七、評分卡

| 面向 | 分數 | 一句話 |
|---|---|---|
| 長文檔／多頁解析 | ⭐ 9.5 | 核心賣點，開源同級無對手，v2 已到百頁級 |
| 單頁精度 | 8 | OmniDocBench 93.23 優秀，但圖表是弱項 |
| 記憶體效率設計 | 9 | 恆定 KV cache 有 kernel 數據背書；v1 的 prefill 仍隨頁數長，v2 才補平 |
| 絕對速度 | 6 | 比傳統 OCR 慢一個數量級，吃 GPU |
| 多語言覆蓋 | 6 | 中英文強；希伯來／阿拉伯文有回報災情 |
| 部署生態 | 8.5 | vLLM／SGLang／GGUF／ms-swift／雲端全齊 |
| 工程品質與安全 | 6 | 63 個 open issues、`eval()` 後處理是實打實的隱患 |
| 授權與成本 | 10 | MIT、權重全開、可商用 |

**綜合：8/10。**

## 八、結論

Unlimited-OCR 是少見「LinkedIn 貼文沒有誇大核心技術」的案例：恆定 KV cache 不是 PPT 名詞，而是有 kernel 層量測撐腰的架構改動，v2 更把 v1 僅存的天花板（prefill 隨頁數增長）也拆掉了。對「長 PDF、合約、整本書一次掃完」這類需求，它是目前開源界唯一認真作答的方案，MIT 授權沒有藉口不用。

但請記住它的邊界：**單頁輕量場景**（發票、收據、截圖）留給 PaddleOCR／Tesseract，性價比差一個數量級；**圖表密集**的文件它不是強項；**小語種**先小規模驗證再說；上生產前處理掉 `eval()` 與重複守衛。選對戰場，它確實對得起「Unlimited」這個中二的名字。

---

**來源**

- 模型：[huggingface.co/baidu/Unlimited-OCR](https://huggingface.co/baidu/Unlimited-OCR)（v1）、[huggingface.co/baidu/Unlimited-OCR-2](https://huggingface.co/baidu/Unlimited-OCR-2)（v2）
- 論文：[arXiv:2606.23050 — Unlimited OCR Works](https://arxiv.org/abs/2606.23050)、[arXiv:2610.39308 — Unlimited OCR Works 2](https://arxiv.org/abs/2610.39308)
- 程式碼與 issue 區：[github.com/baidu/Unlimited-OCR](https://github.com/baidu/Unlimited-OCR)
- 第三方評論：[alphaXiv 頁面](https://www.alphaxiv.org/abs/2606.23050)（消融實驗質疑）、Hugging Face 未驗證 ParseBench 提交
