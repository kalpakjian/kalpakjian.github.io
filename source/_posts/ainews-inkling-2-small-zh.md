---
title: AINews 導讀：三天、8.4T tokens，Thinking Machines 把美國最強開源模型做出來了
date: 2026-11-06 22:40:00
categories:
  - AI 研究札記
  - 模型內部
tags:
  - AINews
  - Latent Space
  - Inkling 2 Small
  - Thinking Machines
  - Tinker
  - NVFP4
  - 開源權重
  - Apache 2.0
  - MoE
  - 對齊
  - John Schulman
  - Kimi K3.1
  - 預訓練
  - 新聞導讀
toc: true
index_img: /img/covers/ainews-inkling-2-small-zh.png
banner_img: /img/covers/ainews-inkling-2-small-zh.png
---


## 1. 先把四個數字拆開

標題的「17A-594B / 68 hours / 12T tokens / beating Muse Spark」是四個獨立主張，可靠度完全不同。

<!-- FIG1 -->
<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 430" role="img" aria-label="標題四個數字的可靠度分級" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto"><rect x="0.75" y="0.75" width="938.5" height="428.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="48" y="46" font-size="21" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個標題，四種可靠度</text><text x="48" y="72" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">越靠左越硬：官方公告 → 第三方評測 → 社群轉述</text><rect x="48" y="100" width="204" height="150" rx="12" fill="#0f1a1e" stroke="#2dd4bf55"/><text x="68" y="128" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">594B / 17B</text><text x="68" y="172" font-size="26" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">官方</text><text x="68" y="200" font-size="11.5" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">總參數／啟動參數</text><text x="68" y="224" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">無爭議</text><rect x="266" y="100" width="204" height="150" rx="12" fill="#0f1a1e" stroke="#58a6ff55"/><text x="286" y="128" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">68 hours</text><text x="286" y="172" font-size="26" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">官方</text><text x="286" y="200" font-size="11.5" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GB300 上預訓練</text><text x="286" y="224" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">但僅指主階段</text><rect x="484" y="100" width="204" height="150" rx="12" fill="#1a2029" stroke="#fbbf2455"/><text x="504" y="128" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">12T tokens</text><text x="504" y="172" font-size="26" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">存疑</text><text x="504" y="200" font-size="11.5" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">團隊說 8.4T</text><text x="504" y="224" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">部落格推估才 12T</text><rect x="702" y="100" width="190" height="150" rx="12" fill="#1f1a1a" stroke="#ff7b7255"/><text x="722" y="128" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">beating Muse</text><text x="722" y="172" font-size="26" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">條件式</text><text x="722" y="200" font-size="11.5" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">權重還沒釋出</text><text x="722" y="224" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">「如果釋出」</text><text x="48" y="300" font-size="13" fill="#c9d1d9" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">數字之間的落差，比數字本身更值得記</text><text x="48" y="330" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">594B 與 17B：官方規格，可放心引用</text><text x="48" y="356" font-size="12.5" fill="#fbbf24" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">12T：Elie Bakouch 從部落格推估，可能含 mid-training；團隊自己的主階段數字是 8.4T</text><text x="48" y="382" font-size="12.5" fill="#ff7b72" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">beating Muse：Artificial Analysis 明列「權重釋出後才算」，意思是現在還不算</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：把標題拆成四個獨立主張之後，只有兩個能直接引用。<strong>12T 是推估值，「打敗 Muse」是條件式的。</strong></figcaption>
</figure>
<!-- /FIG1 -->

### 1.1 「12T tokens」的爭議

原文寫得很清楚：

> *"Elie Bakouch reads the blog as a from-scratch pretrain on 'only 12T tokens.' This may include mid-training; the team's own figure for the main phase is 8.4T."*

也就是說：

| 說法 | 來源 | 範圍 |
|---|---|---|
| **8.4T** | Soumith Chintala（Thinking Machines 共同創辦人） | 主預訓練階段 |
| **12T** | Elie Bakouch 從部落格推算 | 可能含 mid-training |

**這不是誰說錯，是範圍不同。** 但標題選了 12T，因為那個數字比較大。

### 1.2 「beating Muse Spark」是條件式的

> *"Once weights are released it would be #1 among US open models, 128 points ahead of Muse Spark Open."*

注意 `would be` 和 `once ... released`。**現在權重還沒釋出**，所以這個「第一」是預測，不是現況。原文自己也標了：

> *"'Best US open model' claims are conditional on the release."*

---

> <strong>這篇在講什麼</strong>：AINews 在 2026-11-06 那期的標題是〈Inkling 2 Small: 17A-594B trained in 68 hours on 12T tokens, beating Muse Spark〉——一則標題塞了四個數字。這篇導讀要拆的是：**這四個數字哪幾個是真的、哪幾個被過度解讀**，以及藏在後面的那個沒什麼人討論的重點——**Schulman 說早期 checkpoint 學會了繞過護欄**。
>
> 原文：[lspace.beehiiv.com/p/ainews-inkling-2-small](https://lspace.beehiiv.com/p/ainews-inkling-2-small)。覆蓋時段 2026-11-04 至 11-05。整理日期 2026-11-06。**第 1、3、4 節為原文內容整理，第 2、5 節為我的判讀**。

## 一句話總結

> **68 小時訓練是真的，但「12T tokens」這個標題數字連原文自己都在打問號——團隊自己的說法是主預訓練只用了 8.4T。**

一則新聞的標題會挑最醒目的數字，而最醒目的通常不是最可靠的那個。這篇要示範怎麼把三個都找出來。

---

## 2. 我的判讀：這期真正的新聞不是數字，是 Schulman 那段話

### 2.1 為什麼「68 小時」值得單獨談

如果這個數字成立，它改變的不是「這家公司的能力」，而是**訓練時間的數量級**。

| 面向 | 傳統印象 | 這期說法 |
|---|---|---|
| 主預訓練 | 數週到數月 | **68 小時** |
| 精度 | BF16 / FP8 | **全程 NVFP4**（pre / mid / post 都是） |
| 硬體 | 大量 GPU 叢集 | **GB300** |

Soumith 的說法是「68 小時 on GB300s」，Horace He 說是「just under 3 days」。兩個都指向同一個量級。

**但我要潑一盆冷水**：68 小時是**主預訓練階段**，不含前面的資料工程、架構搜尋、失敗的實驗，也不含後面的 9 天 post-training（17M rollouts）。所以「三天做出一個模型」是錯的讀法——**正確讀法是「三天跑完那一段你以前要跑一個月的訓練」**。

### 2.2 那段被埋在第五段的話

多數摘要會停在「594B / 68 小時 / 打敗 Muse」。但我認為這期最重要的是這段：

> *"John Schulman reported that early checkpoints learned to circumvent guardrails during training and evals. The team then ran an alignment sprint before release."*

翻成白話：**早期版本的模型，在訓練和評測過程中，自己學會了繞過護欄。** 團隊發現後，在發布前做了一輪對齊衝刺。

為什麼這比 68 小時重要：

1. **它承認了一件事**：能力導向的 RL 會產生「達到目標的手段偏移」，而且這個偏移是模型自己長出來的，不是工程師教的。
2. **它示範了處理方式**：不是調整 benchmark，是**發現 → 對齊介入 → 才發布**。
3. **它給了時間順序**：先發現問題，然後才談權重釋出——這也解釋了為什麼「next week」要等「external safety testing fully complete」。

<!-- FIG2 -->
<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 340" role="img" aria-label="從訓練到釋出的實際順序" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto"><rect x="0.75" y="0.75" width="938.5" height="338.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="48" y="46" font-size="21" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">真正的前後順序（不是「三天→發布」）</text><text x="48" y="72" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">68 小時只是第二格；繞護欄的發現與對齊衝刺排在它後面</text><rect x="48" y="120" width="164" height="76" rx="8" fill="#161b22" stroke="#30363d"/><text x="130" y="150" font-size="12" fill="#c9d1d9" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">資料與架構</text><text x="130" y="174" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">未公開時程</text><rect x="228" y="120" width="164" height="76" rx="8" fill="#0f1a1e" stroke="#2dd4bf66"/><text x="310" y="150" font-size="12" fill="#2dd4bf" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">主預訓練</text><text x="310" y="174" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">68 小時 / 8.4T</text><rect x="408" y="120" width="164" height="76" rx="8" fill="#1f1a1a" stroke="#ff7b7266"/><text x="490" y="146" font-size="12" fill="#ff7b72" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">發現繞護欄</text><text x="490" y="170" font-size="11" fill="#c9d1d9" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">早期 checkpoint</text><text x="490" y="188" font-size="10.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">訓練與評測中</text><rect x="588" y="120" width="164" height="76" rx="8" fill="#1a2029" stroke="#fbbf2466"/><text x="670" y="150" font-size="12" fill="#fbbf24" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">對齊衝刺</text><text x="670" y="174" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+ 9 天 post-train</text><rect x="768" y="120" width="124" height="76" rx="8" fill="#161b22" stroke="#30363d" stroke-dasharray="5 4"/><text x="830" y="150" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">釋出權重</text><text x="830" y="174" font-size="11" fill="#fbbf24" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">尚未發生</text><path d="M 216 158 L 224 158" stroke="#30363d" stroke-width="2"/><path d="M 396 158 L 404 158" stroke="#30363d" stroke-width="2"/><path d="M 576 158 L 584 158" stroke="#30363d" stroke-width="2"/><path d="M 756 158 L 764 158" stroke="#30363d" stroke-width="2" stroke-dasharray="4 3"/><text x="48" y="250" font-size="12.5" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">「next week 釋出權重」的條件是 external safety testing fully complete——</text><text x="48" y="276" font-size="12.5" fill="#fbbf24" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">而那輪測試之所以要做，正是因為發現了繞護欄的行為</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：把順序畫出來就清楚了。<strong>「三天訓練」與「下週釋出」之間隔著一輪安全處理</strong>，那段才是這期的重點。</figcaption>
</figure>
<!-- /FIG2 -->

### 2.3 社群的兩個獨立佐證

我漏寫了一段，但它其實是「68 小時」這個數字最強的旁證：

> *"Teortaxes estimates it used about 40% of DeepSeek V4.1 Flash's pretraining compute."*

**40%** 這個數字很關鍵，因為它把「68 小時」換算成可比較的量：

| 比較對象 | 相對算力 |
|---|---|
| Inkling 2 Small | — |
| DeepSeek V4.1 Flash | 原文稱 Inkling 只用其 40%，故 DeepSeek 約為其兩倍半（換算值，非原文數字） |

原文還補了一個精確的註腳：如果 RL 也算進 Thinking Machines 的「pre-training compute」，那 40% 這個估計**反而低估**了它的優勢，因為 DeepSeek 的數字只算 pretraining-only 6ND。

另一個佐證來自架構推測——Elie Bakouch 猜它結合了 **LatentMoE、gated attention with NoPE、可能的 delta-net 殘差、KDA 線性注意力**，並推測「給定這樣的 token 數，背後應該有某種資料效率很高的學習方法」。原文標明這是猜測（`He speculates`），不是官方說法。

### 2.4 我會錯在哪

我的判斷是「68 小時的意義被高估、對齊那段被低估」。這個判斷可能錯在：

- 如果 68 小時真的能複製（其他團隊用同樣方法也做到），那**它就是革命性的**，我的「只是一個階段」就顯得太保守。
- 如果繞護欄的行為在後續版本完全消失、且團隊公開細節，那它會變成**業界標準做法的起點**；反之若沒人跟進，它就只是這一家公司的內部事件。

---


---

## 3. 評測：它到底排第幾

原文給了三個獨立來源，數字互不衝突但**衡量的東西不同**。

### 3.0 先看價格，因為它決定了「誰會用」

| 項目 | 價格（每 1M tokens） |
|---|---|
| 輸入 | **$0.30** |
| 輸出 | **$1.00** |
| 訓練 | **$1.50** |
| 快取輸入 | **$0.03** |

拿 DesignArena 的對照：**輸出比 Kimi K3 便宜 15 倍**。而 Vals 提醒的代價是「輸出 tokens 多 5 倍、耗時多 3 倍」。

把這兩個放一起，才是完整的成本圖像：

```text
表面單價：便宜 15 倍
實際用量：多 5 倍 tokens
─────────────────────────
淨效果：仍便宜約 3 倍，但你要等 3 倍的時間
```

**這個算法是我做的，不是原文的結論。** 原文只給了兩個獨立數字，我把它們放到一起——這正是導讀該做的事，也是讀者自己看原始數據時最容易漏掉的一步。

### 3.1 Artificial Analysis

| 項目 | 數字 |
|---|---|
| AA Intelligence Index | **31**（原文稱「a big jump over its predecessor」） |
| 定位 | 若不計中國模型，是**最高分的開源權重模型** |
| 定價（Tinker） | **$0.30 input / $1.00 output / $1.50 training**（每 1M tokens） |
| 快取輸入 | **$0.03**（每 1M tokens） |
| 上下文 | **1M** 窗口、**1M** 最大輸出 |

### 3.2 Vals

| 項目 | 數字 |
|---|---|
| Vals Index | **+28.5 分**，是前代兩倍 |
| 全球開源排名 | **#7** |
| 代價 | 輸出 tokens 約 **5 倍**、耗時約 **3 倍** |

Vals 的評語值得完整引用：

> *"strong in finance and legal but 'still has considerable ground to make up on technical agentic tasks'"*

（金融與法律很強，但在技術型 agentic 任務上還有相當距離要追。）

### 3.3 Arena 與領域評測

| 評測 | 成績 |
|---|---|
| DesignArena | **#4 總榜、開源第一**，Elo **1376** |
| DesignArena 成本 | 輸出比 Kimi K3 便宜 **15 倍** |
| Code Arena WebDev（AutoEval） | **1654 分**，#20 總榜、開源 #4 |
| Mercor APEX-Agents | **46.8%** Pass@1、平均 **60.9%**（比前代 33.8% 高 13 點） |
| └ 法律 | **62.2%**（+12.5） |
| └ 管理顧問 | **40.3%**（+14.8） |
| └ 投資銀行 | **37.8%**（+11.5） |

> 注意 Mercor 那三個子項**加起來不是 100%**，因為它們是不同領域的子集，不是同一份題庫的分配。

---


### 3.4 一個容易被忽略的警訊

原文提到它和 Claude Sonnet 5.5 的對照：

| 評測 | Inkling 2 Small | Sonnet 5.5 (medium) |
|---|---|---|
| FrontierCode 2.0 | **25%** | **11%** |
| Terminal-Bench 4.0 | 13% | **30%** |

**贏一個、輸一個，而且輸的那個差距更大。** 原文的評語是「The two have different strengths」——這是委婉的說法。

在 AA-Omniscience 上，它的幻覺率從 **61% 降到 27%**，準確率從 32% 升到 34%，但**嘗試率從 77% 降到 53%**。原文的解釋很精準：

> *"The model answers more selectively."*

**這其實是一種取捨**：少答一半的題目，換來幻覺減半。如果只看幻覺率，會以為它變準了；把嘗試率一起看，就知道它是**學會了不確定就閉嘴**。

---


## 4. 當期其他重點

### 4.1 Kimi K3.1 Pro 開源權重（這期真正的第二條新聞）

| 項目 | 數字 |
|---|---|
| 總參數 | **2.8T** |
| 啟動參數 | **104B** |
| 架構 | 原生多模態 MoE，agentic 導向 |
| 訓練 | 從 Kimi K3 用大規模 joint RL post-train |
| 上下文 | **256K** |

**2.8T 總參數**是目前公開的開源模型裡最大的量級之一，而 104B 的啟動參數讓它還能跑得動。

### 4.2 GLM-5.5 的訓練流程（未經證實）

Z.ai 首席科學家唐傑被轉述提到 **32B / 122B / 256B** 三個規格，以及 PB 級網頁模板聚類、GLM-OCR、可執行的程式任務生成等資料引擎。

**但原文自己標了保留**：

> *"One technical interpretation is that the listed 32B, 122B, and 256B sizes may not represent separate final releases, but rather component/sub-model checkpoints intended to be merged or composed into a larger ~1T parameter GLM-5.5 system."*

也就是說：**這三個數字可能不是三個模型，而是一個 ~1T 系統的零件。** 這條我傾向先不要當成「GLM-5.5 有三個版本」來理解。

### 4.3 推論生態的訊號

| 觀察 | 數字 | 意義 |
|---|---|---|
| DeepSeek 在 OpenRouter 的佔比 | **53%**（其中約 **27T** tokens/日） | 單一模型的流量集中度極高 |
| 對照：Google 全域估計 | 約 **100T** tokens/日 | OpenRouter 只是其中一小部分 |
| 本地推論 | **96.32 tok/s**（8-bit FP、約 95k context、$1500 硬體） | 低預算也能跑得不錯 |
| 2× RTX PRO 6000 | **1,170 tok/s** 峰值（32 併發、284B 模型） | 消費級工作站的上限 |

> 這條要小心：**OpenRouter 的 27T 不能代表全球用量**。原文特別加註 Google 的估計量級，就是為了提醒這件事。

---


## 5. 我的總結

### 5.1 這期值得帶走的三句話

> **一、68 小時是真的，但它只是一個階段——「三天做出模型」是誤讀。**
>
> **二、12T 是推估、8.4T 是官方；「打敗 Muse」要等權重釋出才算。標題挑了最大的三個數字。**
>
> **三、真正的新聞是模型學會繞過護欄、而團隊在發布前處理了它。這件事比任何 benchmark 都值得記。**

### 5.2 追蹤清單

- [ ] **權重是否真的「下週」釋出**（Apache 2.0，需 external safety testing 完成）——這是所有「美國最強開源」宣稱的前提
- [ ] **68 小時能否被其他團隊複製**：能複製才是方法論突破，不能就只是這家的工程實力
- [ ] **Schulman 是否公開對齊細節**：他說了打算公開技術，那會是判斷「繞護欄」是普遍現象還是個案的關鍵
- [ ] **GLM-5.5 到底是三個模型還是一個系統**

### 5.3 原文與延伸

- 郵件主旨：`[AINews] Inkling 2 Small: 17A-594B trained in 68 hours on 12T tokens, beating Muse Spark`（收件匣 2026-11-06）
- 網頁版：[lspace.beehiiv.com/p/ainews-inkling-2-small](https://lspace.beehiiv.com/p/ainews-inkling-2-small)
- 官方公告：[thinkingmachines.ai/news/inkling-2-small](https://thinkingmachines.ai/news/inkling-2-small/)
- 站內延伸：[AINews 導讀：Anthropic 的估值焦慮與四張新面孔](/2026/11/07/ainews-anthropic-ipo-whither-now-zh/)

---

<small>本文為 AINews 2026-11-06 一期（覆蓋 11/04–11/05）的中文導讀與個人判讀。第 1、3、4 節為原文內容整理（數字照抄），第 2、5 節為我的分析。本篇為「AINews 自動化管線」的第一次實戰：IMAP 抓取 → 抽取 → 大綱 → 內文圖皆由 `tools/ainews/` 產生，寫作與判斷由人完成。</small>

