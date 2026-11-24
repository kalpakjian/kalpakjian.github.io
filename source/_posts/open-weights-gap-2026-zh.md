---
title: open-weights-gap-2026-zh
date: 2026-11-24 20:00:00
categories:
  - 學習資源
tags:
  - 人工智慧
  - 機器學習
  - 學習筆記
---

一句話：「最難的代理式工程現在由閉源領先」有硬證據；「開放權重永遠追不上」沒有。中間那幾個最常被引用的數字（12 分、13 分、12 倍），我一個一個回到一手來源重算，結論是三個都要打折。

> <strong>30 秒結論</strong>：<br />
> 一、差距是真的，但「12 分」有一半是時間差——最佳開放權重 Kimi K3.1 Pro 在 10 月 27 日那天<strong>權重還沒釋出</strong>；11 月 4 日上架後，Artificial Analysis 自己的說法是差距回到 3 分。<br />
> 二、「釋出權重的模型只有 13 分」對不上帳：現行榜單是 33 分（DeepSeek V4.1 Flash 1017）。真正難看的是代理式程式設計，FrontierCode 2.0 上 28% 對 46%。<br />
> 三、閉源靠 AI 自我加速有初步證據（1.9 倍，區間 1.5–2.8 倍），但「員工自報 12 倍」和「模型能力每幾個月翻倍」不是同一件事，前者是民調、後者是另一套量測。<br />

## 1. 查證總表

| 影片主張 | 判定 | 一手依據 |
|---|---|---|
| 開放權重落後擴大 | <strong>站得住，但口徑要拆</strong> | AA v5：差距 3 分 → 12 分，但最佳開放模型當天權重未釋出；11/4 釋出後 AA 預期回到 3 分 |
| 公開榜單高分可能含特化／污染 | <strong>站得住</strong> | AA v5 有 60% 題目改用私有題庫或保留答案；FrontierCode 2.0 的 132 題維持私有 |
| Anthropic 內部研發加速 | <strong>站得住，但區間很寬</strong> | METR：1.9 倍（95% CI 1.5–2.8）；換一條連結函數可從 1.1 倍到 2.9 倍 |
| 員工自報 12 倍生產力 | <strong>不能當產出數字</strong> | 同一機構的實測是 18% 提速（CI −38%～+9%）；349 人調查中位數 1.4–2 倍 |
| 算力成長 1.5–2 倍 vs 2–4 倍 | <strong>查不到一手來源</strong> | 找不到可公開驗證的統一口徑，方向可能對、數字不能引用 |
| 開源永遠追不上 | <strong>過度推論</strong> | 這是推測，不是量測；且 2026 年已有 46 分的開放權重模型 |

## 2. 差距是真的，但那 12 分的組成要拆開

<!-- FIGURE -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 520" role="img" aria-label="Intelligence Index v5 長條圖：閉源前四名與開放權重最高分之間差 12 分" style="width:100%;height:auto;display:block">
<defs><marker id="mfbbf24" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#fbbf24"/></marker></defs>
<rect x="0.75" y="0.75" width="898.5" height="518.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Intelligence Index v5：前四名閉源，第五名才輪到開放權重</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Artificial Analysis，2026-10-27 公布；括號為 effort 設定</text>
<path d="M 330 118 L 330 452" fill="none" stroke="#30363d" stroke-width="1.5"/>
<path d="M 490.0 452 L 490.0 458" fill="none" stroke="#30363d" stroke-width="1"/>
<text x="490.0" y="474" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">20</text>
<path d="M 650.0 452 L 650.0 458" fill="none" stroke="#30363d" stroke-width="1"/>
<text x="650.0" y="474" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">40</text>
<path d="M 810.0 452 L 810.0 458" fill="none" stroke="#30363d" stroke-width="1"/>
<text x="810.0" y="474" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">60</text>
<text x="314" y="145" font-size="14" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Claude Opus 5.5 (max)</text>
<rect x="330" y="129.0" width="464.0" height="22" rx="4" fill="#58a6ff" stroke="none" stroke-width="1.5"/>
<text x="804.0" y="145" font-size="14" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">58</text>
<text x="314" y="183" font-size="14" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GPT-6 Astra (max)</text>
<rect x="330" y="167.0" width="456.0" height="22" rx="4" fill="#58a6ff" stroke="none" stroke-width="1.5"/>
<text x="796.0" y="183" font-size="14" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">57</text>
<text x="314" y="221" font-size="14" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GPT-6.1 Sol (max)</text>
<rect x="330" y="205.0" width="440.0" height="22" rx="4" fill="#58a6ff" stroke="none" stroke-width="1.5"/>
<text x="780.0" y="221" font-size="14" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">55</text>
<text x="314" y="259" font-size="14" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Gemini 4 Argon (high)</text>
<rect x="330" y="243.0" width="400.0" height="22" rx="4" fill="#58a6ff" stroke="none" stroke-width="1.5"/>
<text x="740.0" y="259" font-size="14" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">50</text>
<text x="314" y="297" font-size="14" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Kimi K3.1 Pro</text>
<rect x="330" y="281.0" width="368.0" height="22" rx="4" fill="#2dd4bf" stroke="none" stroke-width="1.5"/>
<text x="708.0" y="297" font-size="14" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">46</text>
<text x="314" y="335" font-size="14" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Claude Haiku 5.5 (max)</text>
<rect x="330" y="319.0" width="288.0" height="22" rx="4" fill="#58a6ff" stroke="none" stroke-width="1.5"/>
<text x="628.0" y="335" font-size="14" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">36</text>
<text x="314" y="373" font-size="14" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">DeepSeek V4.1 Flash 1017 (max)</text>
<rect x="330" y="357.0" width="256.0" height="22" rx="4" fill="#2dd4bf" stroke="none" stroke-width="1.5"/>
<text x="596.0" y="373" font-size="14" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">32</text>
<text x="314" y="411" font-size="14" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GLM-5.3 (max)</text>
<rect x="330" y="395.0" width="256.0" height="22" rx="4" fill="#2dd4bf" stroke="none" stroke-width="1.5"/>
<text x="596.0" y="411" font-size="14" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">32</text>
<path d="M 698.0 118 L 698.0 452" fill="none" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="688.0" y="118" font-size="12" fill="#2dd4bf" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">最佳開放權重 46</text>
<path d="M 702 108 L 792 108" fill="none" stroke="#fbbf24" stroke-width="1.5" marker-end="url(#mfbbf24)"/>
<path d="M 792 108 L 702 108" fill="none" stroke="#fbbf24" stroke-width="1.5" marker-end="url(#mfbbf24)"/>
<text x="747" y="100" font-size="12" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">12 分</text>
<circle cx="55" cy="496" r="7" fill="#58a6ff"/>
<text x="70" y="500" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">閉源</text>
<circle cx="205" cy="496" r="7" fill="#2dd4bf"/>
<text x="220" y="500" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">開放權重</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：同一份 v5 快照（2026-10-27 公布）。藍色為閉源、綠色為開放權重；虛線是當天最佳開放權重 46 分，與領先者差 12 分——但這 12 分裡有一半是時間差：Kimi K3.1 Pro 的權重 11 月 4 日才上架，Artificial Analysis 預期差距會回到 3 分。</figcaption>
</figure>
<!-- /FIGURE -->

Artificial Analysis 在 10 月 27 日把 Intelligence Index 升到 v5，同時把「刷題」風險下降了一級：新版的 60% 分數來自私有題庫或保留答案的題目，新增的 FrontierCode 2.0 是 Cognition 的私人程式碼基準——132 個真實開源儲存庫任務，評分方式是「維護者會不會 merge 這個修改」，任務本身不對外公布以避免污染（[AA v5 公告](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v5)）。這一點確實支持影片的說法：公開題庫的分數，愈來愈不能當成工程能力的代理指標。

但同一份公告裡那句「差距從 3 分擴大到 12 分」，原文寫得很清楚：

> The open weights gap widens from 3 points to 12: Kimi K3.1 Pro (weights not yet released) is the top open weights model at 46. Among released weights, DeepSeek V4.1 Flash 1017 (max) and GLM-5.3 (max) lead at 32.

也就是兩個不同的東西被壓進同一句話：

- <strong>46 分那一格是「能力已到、權重未到」</strong>。Kimi K3.1 Pro 在 10 月 23 日上線時，AA 的標題就是「一旦權重釋出，它會是最高分的開放權重模型，與閉源的差距會從 12 分縮到 3 分」（[AA 發布文](https://artificialanalysis.ai/articles/kimi-k3-1-pro-launch-benchmarks)）。
- <strong>32 分那一格才是「真的拿得到」的現況</strong>：已釋出權重裡最強的 DeepSeek V4.1 Flash 1017 與 GLM-5.3，26 分落後，而且低於 Claude Haiku 5.5 的 36 分。

Kimi 的權重在 11 月 4 日如約上架：96 個 safetensors 分片、1.56 TB、2.8T 總參數／104B 激活、MXFP4 量化感知訓練，可直接 vLLM／SGLang 跑（[ArtificialWatch 的當日核對](https://artificialwatch.com/wire/kimi-k3-1-pro-open-weights-out)）。授權是 Kimi K3 授權改名：可自由使用、修改、微調、再散布，但如果「把模型存取當服務賣」且任何 12 個月營收超過 2,000 萬美元，需另外簽約；月活超過 1 億或月營收超過 2,000 萬美元要在產品顯著位置標示名稱。

所以比較準確的說法是：<strong>「開放權重落後 3 分」和「落後 26 分」同時為真，差別在你算的是哪一天、哪一個發布節奏。</strong>把 12 分當成「產業結構性落後」的證據，是把發布時差讀成了能力時差。

## 3. 「13 分」與「多數開放權重低於 10 分」對不上帳

我照這個說法去查，查不到 13 分這個數。現行開放權重榜（Intelligence Index v5.0.1，2026-11-24 讀取）是這樣：

| 模型 | 分數 | 規模 | 備註 |
|---|---|---|---|
| Kimi K3.1 Pro | 46 | 2.8T／104B 激活 | 權重 11/4 釋出 |
| Tencent Hy4 | 35 | 774B／50.2B | 權重已釋出 |
| DeepSeek V4.1 Flash 1017 (Max) | 33 | 552B／16B | 權重已釋出 |
| GLM-5.3 (Max) | 32 | 753B／40B | 權重已釋出 |
| Inkling 2 Small | 31 | 594B／17B | 權重已釋出 |
| MiMo-V2.6-Pro | 30 | 1T／42B | 權重已釋出 |
| Ling 3.1 Flash 1019 | 30 | 560B／25B | 權重已釋出 |

（來源：[AA 開放權重比較頁](https://artificialanalysis.ai/models/open-source)）前七名全部在 30 分以上，「多數低於 10 分」不成立。那個 13 分可能是把某個舊版分數、某個非 max effort 的變體、或別家榜單的分數混進來了——這種數字一旦被影片引用就很難追，我建議直接標成「來源不明」。


### 3.1 真正該看的是代理式程式設計

分數平均會被稀釋，把鏡頭拉近到 FrontierCode 2.0 就清楚多了：Claude Opus 5.5 (max) 46%，GPT-6 Astra、GPT-6.1 Terra、Claude Sonnet 5.5 都是 42%，而開放權重最高的 DeepSeek V4.1 Flash 1017 (max) 是 28%——<strong>差 18 個百分點，不到人家的三分之二</strong>。

另一個側面：ArtificialWatch 把各家榜單做中位數排名後，Kimi K3.1 Pro 總榜第 11／44，但<strong>程式設計分榜只排第 21／45，還落後另外四個開放模型</strong>（[ArtificialWatch](https://artificialwatch.com/wire/kimi-k3-1-pro-open-weights-out)）。開放權重的強項在知識工作與部分科學推理，弱的正好是「多檔案、長跨度、要交付」的那種任務——也就是影片講的那種工作。

所以我不會反駁影片的核心判斷。我要反駁的是它的<strong>推論方向</strong>：從「這一季代理式工程落後」跳到「永遠追不上」，中間缺了至少三件事的證據（見第 5、6 節）。

## 4. 榜單可不可信：AA 自己先講了，但還有另一種不可比

影片對「刷題」的懷疑，AA 用行動承認了：v5 有六成題目是私有或保留答案，FrontierCode 2.0 的 132 題不對外公布、attempt 只要有一個 blocking check 掛掉就 0 分、每題跑三次、跑在自家的 Stirrup harness 上。這是目前能看到最接近「實戰」的評測設計。

但同一份 v5 也示範了另一種不可比，而且這一點影片沒提：

| 同一個模型，不同 effort | 分數 | 每題成本 |
|---|---|---|
| Claude Opus 5.5（low） | 35 | $0.98 |
| Claude Opus 5.5（max） | 58 | $10.04 |
| Claude Sonnet 5.5（low → max） | 差 29 分（v4.3 時是 20 分） | — |
| GPT-6.1 Sol（低 → 高 effort） | 差 20 分（v4.3 時是 10 分） | — |

再加上 v5 的題目更吃 token：中位數從每題 35k 輸出 token 漲到 59k，而四個 agentic 評測佔了 55% 的權重、約 90% 的 token。意思是，<strong>現在榜上的「分數」是「模型能力 × 你願意燒多少推論算力」的合成量</strong>，不是單純的能力刻度。這對「開源能不能追上」是好消息也是壞消息：壞消息是閉源可以用算力換分數；好消息是同一招開源也能用，只是貴。

## 5. 自我加速：1.9 倍站得住，「AI 造 AI 飛輪」還沒到

METR 在 11 月 5 日公布的 Anthropic 評估，是目前最紮實的一份：

- 以 Anthropic 內部的 AECI（Epoch Capabilities Index 的內部版）估計，2025 年 10 月之後的能力成長速度是之前（2024-03～2025-10）的 <strong>1.9 倍，95% 信賴區間 1.5–2.8</strong>，換算成「過去一年走了大約兩年的歷史進度」。
- 約 <strong>80%</strong> 的加速「可能」歸因於 Anthropic 大量用 AI 做研發，但 METR 同時說「有相當大的不確定性，其他原因在 2025 年底可能也扮演重要角色」。
- 換一條統計連結函數，同一個估計可以從 <strong>1.1 倍</strong>（cloglog，區間 0.8–1.5，等於「沒有加速」）<strong>到 2.9 倍</strong>（log-log）；Anthropic 自己 Haiku 5.5 系統卡的數字是 1.7 倍。

（[METR 2026-11-05 評估](https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/)、[逐項敏感度整理](https://gautamparab.com/writing/twelve-by-poll-one-point-nine-by-benchmark/)）

還有一個關鍵限制：<strong>這份報告裡「最有資訊量」的證據，大部分被 Anthropic 塗黑了</strong>，理由是「避免加速其他 AI 開發者」。METR 自己寫道，這讓公眾無法自行判斷，只能「比理想狀況更依賴 METR 的判斷」。

然後是 11 月 20 日那份能力更新，把兩件事分得很清楚：

- 時間跨度（模型能獨立完成多長的任務）大約 <strong>每 3.61 個月翻一倍</strong>（95% CI 2.08–4.94）；在「程式碼可驗證」的子集上甚至是 1.65 個月。照這個斜率外推，2027 年 7 月會摸到 200 小時。
- 但同一份報告也說，<strong>完全自主的貢獻「目前還不是整體進展的主要來源，未來可能才是」</strong>；而且模型已經在自家的程式與最佳化任務上「通常匹敵或超越熟練人類」——這正是為什麼「人＋AI」的飛輪已經轉得起來：轉的是人指揮 AI，不是 AI 自己指揮 AI。

（[METR 2026-11-20](https://metr.org/blog/2026-11-20-q4-2026-capability-update/)）

我的讀法：<strong>飛輪在轉，但驅動它的是人＋AI 的組合，不是「AI 自動造出更強 AI」的閉環。</strong>把 1.9 倍講成不可逆的指數失控，是把「有加速」讀成「已失控」。

## 6. 「12 倍」是民調，不是量測

這是整支影片最容易被記住、也最容易誤導的數字。把它和同一批機構的量測結果排在一起就很清楚：

| 來源 | 問法／方法 | 數字 |
|---|---|---|
| 實驗室內部自報 | 問員工「AI 讓你快幾倍」 | 12 倍（非代表性樣本；該段多數證據被塗黑） |
| METR 田野實驗（2025 年初） | 16 位資深開源開發者、246 個真實 issue、隨機分配 | AI 讓任務<strong>多花 19%</strong> 時間（CI +2%～+39%） |
| METR 田野實驗（2026 年初，同一批人） | 同一群人換用當年最新工具 | <strong>快 18%</strong>（CI −38%～+9%，跨零） |
| METR 問卷（2026 年，349 人） | 自報「工作價值」變化 | 中位數 <strong>1.4–2 倍</strong> |
| METR 問卷（同上） | 自報「速度」變化 | 中位數 <strong>3 倍</strong> |

（[2026-02-24 實驗改版說明](https://metr.org/blog/2026-02-24-uplift-update/)、[2026-05-11 問卷](https://metr.org/blog/2026-05-11-ai-usage-survey/)）

同一個機構在這份問卷裡直接寫了：受試者「平均把 AI 對自己工作時間的影響<strong>高估了 40 個百分點</strong>」；自報數字「不一定有現實基礎」。而 2025 年那個 19% 變慢的結果，METR 自己也標註「已過時，不代表現在的模型」——所以兩邊都不能拿來當定論，只能拿來看<strong>量測方式</strong>。

還有一個常被混淆的東西：Anthropic 說 2026 年第二季「每位貢獻者每天 merge 的程式碼量是 2021–2024 年的 8 倍」。這是<strong>程式行數</strong>，不是研究產出。METR 的 Thomas Kwa 用生產函數換算後認為「研究員個人產出很可能超過 2 倍」，但他同時列出三個打折理由：AI 寫的程式可能比人類囉唆 2 倍以上、很多新增程式是「以前根本不會寫的低價值程式」、以及研究員可能在寫不影響研究的東西（vibe coding 很好玩）。同一段還引用 Anthropic 自己 Mythos 系統卡的說法：整體 R&D uplift <strong>「well short of」2 倍</strong>（[Kwa 的推算，2026-07-08](https://metr.org/notes/2026-07-08-anthropic-researcher-uplift/)）。

所以「12 倍」最合理的定位是：<strong>某個自我選擇群體對某些任務的主觀感受，屬於「鬆散證據」，不能換算成「研發週期縮短 12 倍」。</strong>連實驗室自己的系統卡都寫「遠低於 2 倍」，這個 12 倍的數字在文章裡就不該出現在論證主線上。

## 7. 算力那條，我查不到一手來源

影片說閉源實驗室的算力成長是 1.5–2 倍、而開源 2–4 倍（或反過來），我沒找到可公開驗證的統一口徑——不同來源比的可能是訓練 FLOP、可能是 GPU 採購、可能是資本支出，混在一起就變成不可查的數字。方向（閉源比較敢燒、開源要省）大概沒錯，但這種等級的數字我會標成「未經證實」，不寫進結論。

## 8. 成本才是開放權重現在的主場

影片把「省訂閱費」講成陷阱，這在<strong>交付型工程</strong>上我同意；但同一份 v5 的價格表也提醒另一件事：

| 模型 | 分數 | 每題成本 |
|---|---|---|
| Claude Opus 5.5 (max) | 58 | $10.04 |
| GPT-6 Astra (max) | 57 | $6.24 |
| GPT-6.1 Sol (max) | 55 | $1.27 |
| GPT-6.1 Terra (max) | — | $0.96（前十名最便宜）|
| Claude Fable 5.1 (max) | — | $13.04（前十名最貴）|

前十名的每題成本差 13 倍以上；GPT-6.1 Sol 只差 Opus 5.5 四分，成本約八分之一。這說明「閉源一定比較划算」也不成立——<strong>同一個陣營內的價差，比兩個陣營的價差還大</strong>。真正該做的不是選陣營，而是按任務風險分配。

### 8.1 我會怎麼配

- <strong>高風險、長跨度、多檔案、要交付</strong>：用當下最強的閉源代理模型，搭配人工審查、測試、版本控制與可回滾。這裡省錢一定賠回去。
- <strong>高頻、低風險、可自動驗證</strong>：分類、抽取、格式轉換、批次改寫、文件摘要——用 30 分級的開放權重模型（單價差一個數量級）就夠，錯了機器會抓。
- <strong>私有資料、合規、離線</strong>：開放權重的價值不是「追平最強」，而是可控部署、資料主權、可微調與議價能力。這一塊閉源模型永遠不會贏。
- <strong>任何代理式編碼</strong>：不要只看榜單。用自己的 20–30 個代表性任務建一個會輪替的小評測，追蹤一次通過率、平均修改輪數、測試覆蓋、回歸率、每任務成本。榜單只能告訴你「該先試誰」，不能告訴你「誰在你的 repo 上不會壞」。

## 9. 我修正後的結論

原本那句話——「為了省訂閱費退回次級工具，最後在效率與品質上賠回去」——在複雜交付型工程上，2026 年 11 月的證據支持它。但更精確的版本是：

<strong>頂尖閉源模型現在在最難的代理式工程上領先，而且這個領先可能因為「人＋AI」的研發飛輪而持續；開放權重模型未必永遠追不上，但短期內已經不適合當「以省錢為目的、直接取代最強閉源」的主力。它的戰場是私有部署、資料主權、成本敏感的工作負載、可微調的專用模型，以及不被單一 API 鎖定的基礎設施。</strong>

判斷一個「開源已死」的論述，我只問三件事：差距是用哪一天的 snapshot 量的？領先的那一方有沒有把權重釋出？加速的證據是量測還是民調？這三題沒答完，結論就只是情緒。

## 10. 來源

| 項目 | 連結 | 實查結果（2026-11-24） |
|---|---|---|
| Intelligence Index v5 | [artificialanalysis.ai](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v5) | 60% 私有題；Opus 5.5 58、Astra 57、Sol 55；Kimi 46、DeepSeek／GLM 32；差距 3→12 分 |
| Kimi K3.1 Pro 發布 | [artificialanalysis.ai](https://artificialanalysis.ai/articles/kimi-k3-1-pro-launch-benchmarks) | 55 分（舊版 index）、第 4 名；權重釋出後差距回到 3 分 |
| 開放權重榜 | [artificialanalysis.ai/models/open-source](https://artificialanalysis.ai/models/open-source) | 46／35／33／32／31／30／30，v5.0.1 |
| Kimi 權重上架與授權 | [artificialwatch.com](https://artificialwatch.com/wire/kimi-k3-1-pro-open-weights-out) | 11/4 上架、1.56 TB、$2,000 萬 MaaS 條款 |
| Anthropic 研發加速評估 | [metr.org](https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/) | 1.9 倍（1.5–2.8）；≈80% 歸因 AI；多數證據被塗黑 |
| 2026 Q4 能力更新 | [metr.org](https://metr.org/blog/2026-11-20-q4-2026-capability-update/) | 時間跨度 3.61 個月翻倍；自主貢獻尚非主因 |
| 開發者生產力實驗 | [metr.org](https://metr.org/blog/2026-02-24-uplift-update/) | 19% 變慢 → 同一批人 18% 變快（CI 跨零） |
| 技術工作者問卷 | [metr.org](https://metr.org/blog/2026-05-11-ai-usage-survey/) | 中位數 1.4–2 倍（價值）／3 倍（速度）；高估 40 個百分點 |
| 8 倍程式碼的換算 | [metr.org](https://metr.org/notes/2026-07-08-anthropic-researcher-uplift/) | LoC 8 倍；系統卡稱整體 uplift「遠低於 2 倍」 |
| 1.9 倍的敏感度分析 | [gautamparab.com](https://gautamparab.com/writing/twelve-by-poll-one-point-nine-by-benchmark/) | 連結函數 1.1–2.9 倍；與 12 倍民調的落差 |

> <strong>查證說明</strong>：以上數字於 2026-11-24 直接讀取一手頁面。我沒有拿到影片本身的連結，所以檢驗的是「可查證的具體數字主張」，不是影片的完整論證結構。<br />
> 會變的東西：榜單分數（改版就會跳）、開放權重模型的名次（每週都可能換）、Kimi 的授權條款（$2,000 萬門檻可能調整）。<br />
> 沒實測的東西：我沒有在 FrontierCode 2.0 上跑過任何模型，也沒有重現 METR 的統計；第 5、6 節的評論是對公開數字的解讀，不是獨立複驗。<br />
>
> <strong>封面與圖表</strong>：封面由本機 ComfyUI 的 Qwen-Image 2.1 生成（刻意不含文字）；圖 1 是手繪內嵌 SVG——分數要精確，交給 AI 生圖只會爛成方塊。
