---
title: Inkling 2 Mini 在本機跑起來了：25 tok/s、假的 1M context，還有官方 build 認不到你的 4090
date: 2026-11-23 21:40:00
categories:
  - AI 研究札記
tags:
  - Inkling 2 Mini
  - Thinking Machines Lab
  - llama.cpp
  - RTX 4090
  - 本地推論
  - MoE
  - 量化
  - Artificial Analysis
  - Unsloth
index_img: /img/covers/inkling-2-mini-4090-local-zh.png
banner_img: /img/covers/inkling-2-mini-4090-local-zh.png
---

社群上那則貼文本來只打算掃過去：一個 26B 的模型「打贏 GPT-6 Luna、MiniMax-M3、Claude Haiku 5.5」，「在你的 16GB 筆電上跑」，「支援 1M context」，「SWE-bench Pro (Hard) 77.9%」。這種組合通常九成是流量農場在講不存在的東西。

實際查了之後：<strong>模型是真的</strong>。`unsloth/Inkling-2-Mini-GGUF` 寫稿當下有 80 萬次下載、879 個讚（隔天已翻到 129 萬／1,046），權重來自 Thinking Machines Lab、Apache 2.0，2026 年 11 月釋出。但貼文把三件事縫在一起：真的模型、挑過的對照組、以及一句會讓你買錯機器的硬體建議。以下是把它真的跑在 RTX 4090 上的完整紀錄——所有數字都是本機實測，或回到一手來源查證。

<!-- more -->

> <strong>一句話總結</strong>：Inkling 2 Mini 在 4090 上跑得動、答案也正確，但生成只有 25 tok/s、prefill 136 tok/s，而且 32K context 就吃掉 23.0／24.5 GB VRAM——<strong>1M context 在單張 24GB 卡上不存在</strong>。<br />
> 它值得下載來驗一次，但不值得留在硬碟裡。<br />

> <strong>2026-11-24 02:00 更新</strong>：Unsloth 於 11/23 深夜重新上傳了全部量化檔（主線 llama.cpp 現在也載得進去）、換掉 dspark draft 模型、宣稱解碼快 1.9×，並修掉 Q8_0 KV cache 佔用比 F16 還多的 bug。本文補上這些變動，以及兩項我自己重跑的實測（§5、§6）。<br />
>
> <strong>2026-11-24 02:30 增修</strong>：補上「這顆模型到底該用在哪」的完整判斷（§8），結論是<strong>沒有明確使用時機</strong>——同級每一項都排第二，唯一獨佔的 1M context 在單張 24 GB 上拿不到。<br />

## 三十秒結論

| 問題 | 一句話回答 |
|---|---|
| 這是什麼 | Thinking Machines Lab 的 26B MoE（5.4B active），looped transformer，文字＋影像輸入，Apache 2.0 |
| 貼文哪部分是真的 | 參數、架構、1M context、48.2% DeepSWE v1.1、77.9% SWE-bench Pro v2 都對得上 |
| 實測速度（4090 / Q4_K_XL） | 生成 <strong>25 tok/s</strong>、prefill <strong>136 tok/s</strong> |
| 記憶體 | 32K context 用掉 23,169／24,564 MiB，剩 1.4 GB |
| 16GB 筆電能不能跑 | 只能跑 1–2 bit（9–11 GB）；官方建議的 4-bit 要 17.6 GB |
| 貼文哪裡誤導 | 「打贏 Claude Haiku 5.5」只在 Haiku 調到 low effort 時成立（20 vs 19） |
| 值不值得接進 coding agent | 不建議：prefill 136 tok/s，三萬 token 的 repo 要 3.7 分鐘才開始吐字 |
| 那什麼時候該用它 | <strong>幾乎沒有</strong>：同級每一項都排第二，唯一獨佔的 1M context 在本地拿不到（見 §8） |

## 一、先驗貨：貼文哪裡真、哪裡灌水

| 貼文宣稱 | 查證結果 |
|---|---|
| 26B | ✅ HF 回報 26,070,390,272 參數；Unsloth 文件寫 26.4B，同一件事 |
| 5.4B active MoE | ✅ 模型卡、Unsloth、Artificial Analysis 三邊一致 |
| looped transformer | ✅ 模型卡原文：「built on a Looped Transformers variant」 |
| 支援 1M context | ✅ 規格成立。能不能用是另一件事，見 §2 |
| 48.2% DeepSWE v1.1 | ✅ 數字無誤，但來源是廠商自報（模型卡），不是第三方重跑 |
| 77.9% SWE-bench Pro (Hard) | ⚠️ 精確名稱是 <strong>SWE-bench Pro v2 (Hard)</strong>；同樣是自報數字 |
| 打贏 GPT-6 Luna Low | ✅ 20 vs 10 分——但比的是 Luna 最省的 low 檔，Luna max 是 28 分 |
| 打贏 Claude Haiku 5.5 | ❌ 沒說哪個 effort。Haiku low 是 19（輸 1 分），medium 25、max 36 都贏 |
| 打贏 MiniMax-M3 | ✅ 20 vs 19，贏 1 分（M3 是 428B 總參數、23B active 的巨獸） |
| 跑在 16GB 筆電 | ⚠️ 只有 1–2 bit 量化塞得進去，品質會掉；4-bit 需要 17–18 GB |
| ready for Unsloth + llama.cpp | ✅ 11/23 更新後<strong>連主線 llama.cpp 也載得進去</strong>；但文件裡的 cuda12 portable 仍會認不到 CUDA 13 的機器（見 §2） |
| 真正的強項 | 文件／圖表數值讀取、GUI 元素定位——但 GUI 那項我複現不出官方數字（見 §5、§6） |

補一個貼文沒說的：模型卡上那兩個 coding 分數很漂亮，但 Artificial Analysis 獨立跑出來的 Terminal-Bench 4.0 只有 <strong>5.6%</strong>，跟 Qwen3.8-27B 同分。自報與第三方之間那道縫，一直是本地模型評測最大的變數。

## 二、實際跑起來，卡在兩個地方

### 坑一：官方給的 cuda12 build 認不到你的卡

照 Unsloth 文件的指令抓 `windows-x64-cuda12-portable`，解壓、跑 `--list-devices`：

```text
Available devices:
  (none)
```

原因是那包預期 `cudart64_12.dll` 與 `cublas64_12.dll`，而這台機器裝的是 CUDA 13.2／13.4，只有 `cudart64_13.dll`。換成同一個 release 的 `windows-x64-cuda13-portable` 之後：

```text
Available devices:
  CUDA0: NVIDIA GeForce RTX 4090 (24563 MiB, 23036 MiB free)
```

這件事值得記下來：<strong>llama.cpp 的 CUDA 版本要對上你機器上的 toolkit，不是對上驅動</strong>。驅動很新不代表 CUDA 12 的 build 會動。

補記（11/24）：官方已重新上傳全部量化檔，「主線 llama.cpp 現在也載得進去」。所以這個坑只在兩種情況還會踩到——沿用舊 revision 的檔案，或照文件抓 cuda12 portable。

### 坑二：1M context 是規格，不是可用長度

32K context 跑起來就吃掉 23.0 GB，只剩 1.4 GB。1M context 的 KV cache 是這個的三十倍量級——在單張 24GB 卡上不是「慢」，是「不存在」。要真的用長 context，得換硬體或換模型。

## 三、實測數據

| 項目 | 實測值 |
|---|---|
| 量化檔 | UD-Q4_K_XL，16.41 GiB（17.63 GB） |
| 下載 | 5 分 37 秒，峰值 50 MB/s |
| 載入 | 47 秒（首次）／10 秒（OS 檔案快取命中） |
| 生成速度 | 25.1 tok/s（短輸出）→ 21.2 tok/s（900 token 長輸出） |
| Prefill | 136 tok/s（2,302 token 花 16.9 秒） |
| VRAM | 23,169／24,564 MiB |
| GPU | 利用率 94–100%、功耗 133–136 W、溫度 45 °C |
| 正確性 | 兩題 Python 小測（字串反轉、回文判斷）都一次到位 |

<!-- FIG1 -->
<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 420" role="img" aria-label="Inkling 2 Mini 在 RTX 4090 上的實測：VRAM 預算 23.0/24.5 GB，生成 25 tok/s，prefill 136 tok/s" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto"><rect x="0.75" y="0.75" width="938.5" height="418.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="48" y="46" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">實測：VRAM 預算與吞吐</text><text x="48" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Inkling 2 Mini UD-Q4_K_XL　·　llama.cpp b12588　·　32K context　·　RTX 4090 24 GB</text><text x="48" y="112" font-size="14" fill="#c9d1d9" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">VRAM 23,169 / 24,564 MiB</text><text x="830" y="112" font-size="12" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">剩 1.4 GB</text><rect x="110" y="126" width="517" height="42" rx="6" fill="#1f6f68" stroke="#2dd4bf" stroke-width="1.5"/><rect x="627" y="126" width="162" height="42" rx="6" fill="#6b5218" stroke="#fbbf24" stroke-width="1.5"/><rect x="789" y="126" width="41" height="42" rx="6" fill="#21262d" stroke="#30363d" stroke-width="1.5"/><text x="368" y="153" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">權重 17.6 GB</text><text x="708" y="153" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">KV 5.4 GB</text><text x="110" y="190" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="470" y="190" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">12 GB</text><text x="830" y="190" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">24 GB</text><line x1="48" y1="214" x2="892" y2="214" stroke="#222b36" stroke-width="1"/><text x="48" y="248" font-size="14" fill="#c9d1d9" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">吞吐 tok/s</text><text x="290" y="286" font-size="13" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">生成</text><rect x="300" y="266" width="70" height="28" rx="5" fill="#2dd4bf"/><text x="382" y="286" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">25.1</text><text x="290" y="330" font-size="13" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">prefill</text><rect x="300" y="310" width="382" height="28" rx="5" fill="#fbbf24"/><text x="694" y="330" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">136.3</text><text x="48" y="378" font-size="13" fill="#fbbf24" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GPU 利用率 94–100%，功耗卻只有 134 W（4090 額定 450 W）</text><text x="48" y="400" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 卡在記憶體頻寬與 kernel 效率，不是算力不足；沒有任何啟動參數能救</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：32K context 就把 24 GB 吃掉九成四——<strong>1M context 在這張卡上是規格，不是可用長度</strong>。吞吐端則出現矛盾訊號：GPU 忙線 100% 卻只吃 134 W，代表瓶頸在資料搬運而非運算。</figcaption>
</figure>
<!-- /FIG1 -->

## 四、為什麼只有 25 tok/s

25 tok/s 對一張 4090 來說偏低。原本估的是 60–100 tok/s（依 5.4B active 的經驗值），實測差了兩倍以上，所以往下查了兩件事。

<strong>第一，確認沒有層掉到 CPU。</strong>VRAM 用掉 23.0 GB，權重 17.6 GB 全在卡上，nvidia-smi 顯示 100% 利用率——不是 offload 造成的。

<strong>第二，看功耗。</strong>這是關鍵：利用率 94–100%，功耗只有 133–136 W，而 4090 額定 450 W。滿載的算力工作會把功耗推到 300 W 以上；停在 134 W 代表 GPU 大部分時間在等資料，不是在算。官方文件給了答案：<strong>第 6–17 層會重複跑三次</strong>。所以一個 token 不是走 26 層，而是走「12 層 × 3 遍」，等效計算量遠高於 5.4B active 給人的印象，再疊上 MoE 的專家權重搬運。<strong>5.4B active 省的是記憶體，不是時間</strong>——而且官方沒有提供推論時可調的 loop 次數，這個旋鈕你轉不到。

另一個要標明的變數：上面所有數字來自 build b12588（11/20）。官方現在推 b12649，宣稱解碼比主線 llama.cpp 快 <strong>1.9×</strong>，但測試卡是 B200／RTX PRO 6000／A100，<strong>沒有 4090 的數據</strong>。所以「1.9×」用在你這張卡上是未證實的，25 tok/s 也可能已經過時。

也試了官方附的投機解碼（`dspark` draft 模型，`--spec-type draft-dspark`）：

| 設定 | 生成速度 | 接受率 | 平均接受長度 |
|---|---|---|---|
| 無 draft | 25.1 tok/s | — | — |
| dspark（384 MB 舊版）＋ n_max=3 | 23.8 tok/s | 44–46% | 2.33–2.37 |

<strong>當時是負收益</strong>：接受率不到一半，draft 的額外開銷蓋過省下的步數，還多佔 VRAM，所以移除了。

但這個結論要打折。11/23 深夜官方把 draft 換成 <strong>481 MB 新版</strong>（舊檔改名 `..._Q8_0_Old.gguf`），建議參數也從 `n_max=3` 改成 `n_max=2`。我測的是舊版＋舊參數，<strong>新版沒測</strong>——所以「dspark 無效」只在舊版成立，別當成定論。

## 五、它的強項到底在哪：分項對照

AA 的綜合分只給一個數字，看不出擅長什麼。官方文件另外放了一張五模型分項表（Inkling 2 Mini／Gemma 4 31B／Muse Glimmer／Qwen3.8-27B／Nemotron 3.5 Super VL），把 Inkling 贏的與輸的分開看，輪廓就出來了。

贏的：

| 基準 | Inkling 2 Mini | Qwen3.8-27B | Gemma 4 31B | 測什麼 |
|---|---|---|---|---|
| ScreenSpot Pro | <strong>76.5%</strong>／87.7% | 57.6% | 5.9% | 截圖上找可點元素 |
| JobBench | <strong>49.6%</strong> | 33.4% | 8.2% | 端到端任務完成 |
| LongBench v2 | <strong>66.9%</strong> | 52.3% | 52.9% | 長文檢索問答 |
| DeepSearchQA | <strong>85.3%</strong> | 79.7% | 61.7% | 多跳搜尋推理 |
| OmniDocBench v1.6 | <strong>92.8%</strong> | 91.5% | 82.5% | 文件版面與表格 |
| Chartography | 22.1%／<strong>72.5%</strong> | 12.2%／52.1% | 12.0%／11.8% | 圖表理解 |
| ARC-AGI v2 | <strong>49.3%</strong> | 42.4% | – | 抽象推理 |

輸的：

| 基準 | Inkling 2 Mini | Qwen3.8-27B | 測什麼 |
|---|---|---|---|
| GDPVal-AA v2.1 | 1319 | <strong>1427</strong> | 產出價值的專業工作 |
| AutomationBench-AA | 41.8% | <strong>48.2%</strong> | 自動化流程 |
| AA-Omniscience 非幻覺 | 63.4% | <strong>71.4%</strong> | 不知道時會不會編 |
| Terminal Bench v2.1 | 71.6% | <strong>73.0%</strong> | 終端機任務 |
| MMMU Pro | 74.9% | <strong>76.3%</strong> | 學術級視覺推理 |
| HLE-Diamond | 15.2% | <strong>15.3%</strong> | 博士級難題（兩個都很低） |

三句話讀完：<strong>它是「看畫面」與「讀文件」的模型，不是「寫程式」與「講知識」的模型</strong>。贏的每一項都和視覺、版面、長文有關；輸的每一項都和產出品質、工具鏈自動化、以及「不確定時閉嘴」有關。最後那項對寫技術文章的人特別要記：非幻覺 63.4% 意味著它比其他小模型更敢編。

⚠️ 這整張表是廠商自報（同一個來源也給出 77.9% 的 SWE-bench Pro），我沒有重跑這些基準。§6 是我自己補的兩項小測，剛好用來檢查這張表的可信度。

## 六、我補測了它的兩個招牌能力

<strong>測試一：讀圖上的數值。</strong>加上 610 MB 的 `mmproj-F16.gguf` 之後（VRAM 20,440 MiB @16K context），拿本文的圖 1 問它六個問題：生成吞吐、prefill 吞吐、權重佔用、功耗、總 VRAM、哪個條比較長。

結果 <strong>6/6 全對</strong>（25.1、136.3、17.6、134、23,169、prefill）。這與 OmniDocBench 92.8% 的方向一致——但要看清楚它做對的是「讀圖上的印刷數字」，那是 OCR，不是圖表推理。不要拿這個去推論它能看懂趨勢。

<strong>測試二：GUI 元素定位。</strong>做一張座標完全已知的 1920×1080 介面（4 個側欄文字項、3 個工具列色塊按鈕、1 個列尾小按鈕），每個目標問一次「點這裡」，座標落在 bbox 內算命中。

| 測試 | 命中率 |
|---|---|
| 1080p，像素座標 | <strong>2–4／8</strong> |
| 1080p，0–1000 正規化座標 | 1／8 |
| 3840×2160，像素座標 | 1／8 |

成敗模式非常乾淨：<strong>三個大色塊按鈕全中，誤差在 3 px 內</strong>（答 `960,61`，真值 `960,62`）；側欄文字列與那個小按鈕全滅，還吐出 `3,-27`、`1920,1080` 這種角落亂數。換成 0–1000 正規化反而更差，所以不是座標慣例的問題。

也就是說：<strong>它看得到圖、也算得出座標，但在「密集文字與小目標裡挑對那一個」這件事上很弱</strong>——而這正是 ScreenSpot-Pro 的考題設計。官方 76.5% 這個數字，我在本地複現不出來。

兩個限制必須寫在前面：樣本只有 8 題（差一題就是 12.5%），畫面是我合成的，而且<strong>沒有對照組</strong>——沒有拿一個已知 GUI 能力強的模型跑同一組題目，所以「模型弱」與「我的題目刁」還沒辦法分離。

## 七、Artificial Analysis 那 20 分要怎麼讀

貼文的「打贏」全部建立在同一個技巧上：拿別人最省的模式來比。

| 模型 | AA Intelligence Index | 備註 |
|---|---|---|
| Inkling 2 Mini | <strong>20</strong> | 同級（≤40B 開源）16 個模型裡第 2 名，不是榜首 |
| GPT-6 Luna | max 28／high 21／medium 18／low <strong>10</strong> | 貼文比的是 low |
| Claude Haiku 5.5 | max 36／high 30／medium <strong>25</strong>／low <strong>19</strong> | 貼文沒說哪一檔；預設是 medium |
| MiniMax-M3 | 19 | 428B 總參數、23B active |
| 全站最高 | Claude Fable 5.2 (max) 65 | 開源最高是 Kimi K3.1 Pro 46 |

三個觀察：

1. <strong>20 分在同級裡確實不錯</strong>（中位數 10），但它是「小模型冠軍」，不是「冠軍」。放到全站排行，20 分在上面一大票模型之下。
2. <strong>對 Haiku 的比較站不住腳</strong>。Haiku 5.5 在任何一個非 low 的檔位都贏 Inkling，而 medium 才是它的預設。
3. <strong>它很囉唆</strong>。AA 量到它在 Intelligence Index 上吐了 1.61 億 output token，是中位數（8,570 萬）的兩倍。這解釋了為什麼單題成本 $0.59 不算貴——是量太大。

## 八、那什麼時候該用它？——答案是：幾乎不用

前七節把強項、弱項、速度、記憶體都量過了，最後只剩一個問題：什麼情況下它是最佳解？把規格跟同分數的對手攤平，答案不太好看。

| 維度 | Inkling 2 Mini | Qwen3.8-27B | 誰贏 |
|---|---|---|---|
| 授權 | Apache 2.0 | Apache 2.0 | 平手 |
| 輸入模態 | 文字＋影像 | 文字＋影像＋<strong>影片</strong> | Qwen |
| Context | <strong>1M</strong> | 256k | Inkling（但只在 API 上成立） |
| AA 綜合分 | 20 | 20 | 平手 |
| Active 參數／token | <strong>5.4B</strong> | 27B dense | 名義上 Inkling，本地實測反而慢（§4） |
| 本地生成速度 | 25 tok/s | 未測 | 待測 |

攤完只剩兩個真正的差異點，而且兩個都不屬於「在自己電腦上跑」的人：

1. <strong>1M context</strong>：單張 24 GB 只到 32K，這個優勢只有透過它的 API 才拿得到。
2. <strong>5.4B active</strong>：對「用自有 GPU 做高併發服務」的人來說每 token 成本更低；但 looped 架構把這個優勢吃掉了，而你不是在跑服務。

<strong>所以結論是：它沒有明確的使用時機。</strong>

「同級第二」聽起來體面，翻成白話就是「除了第一名，沒有理由選它」。它在幾乎每一欄都得補一句「但是」——但是 1M 只在 API、但是速度要靠新 build、但是 GUI 那 76.5% 我複現不出來、但是非幻覺比 Qwen 低 8 個百分點。<strong>需要這麼多「但是」的模型，就是沒有 niche。</strong>

而且這不只是我一個人的量測問題：它自報的兩個招牌長處（SWE-bench Pro 77.9%、ScreenSpot Pro 76.5%）在我能驗的範圍內都往下掉，唯一穩住的是「讀文件上的字」（實測 6/6）——而那一項，專門的 OCR 模型做得比它更快更省。

### 我會改口的三個條件

都寫成可驗證的，不是空話：

1. 你需要在<strong>單一開源權重</strong>模型上吃 1M context。本地做不到，所以這句話實際上等於「你要用它的 API」。
2. 你在<strong>自有 GPU 上做高併發的多模態服務</strong>，每 token 成本比單次延遲重要。
3. 你要<strong>研究或微調 looped transformer</strong>（同一份權重、不同深度的實驗）——那它是目前少數的開源素材。

三個都不是「一張 4090、做 OCR、寫技術筆記」的人。

### 對應到我自己的用法

- <strong>守尾門與判斷</strong>：維持 Qwen3.8-27B。同分、非幻覺高 8 個百分點、能吃的模態還多一種、同樣是 Apache 2.0。
- <strong>文件結構重建</strong>：用 OCR 的行框自己算（行距 → 斷段、縮排 → 清單、行高 → 標題），別讓 LLM 從純文字猜。這一步跟用哪顆模型無關，效益卻最大。
- <strong>想看它一眼</strong>：下載 17.6 GB 要五分鐘，刪掉要五秒。我最後就是刪掉了——留 17 GB 在硬碟裡給一顆「每項第二」的模型不划算。

如果只帶走一句：<strong>那則貼文真正的價值，是讓你真的去下載了一次，然後發現自己不需要它。</strong>

## 九、來源與延伸

| 實體 | 連結 | 實查結果 |
|---|---|---|
| GGUF 權重 | [unsloth/Inkling-2-Mini-GGUF](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) | 26.07B 參數、Apache 2.0、約 80 萬下載 |
| 官方跑法文件 | [Unsloth: Run Inkling 2 Mini](https://unsloth.ai/docs/models/inkling-2-mini) | 記憶體分級表、dspark 參數、looped-layer 需求 |
| 模型評測 | [AA: Inkling 2 Mini](https://artificialanalysis.ai/models/inkling-2-mini) | 20 分、5.4B active、1M context、$0.15／$0.50 |
| 全站排行 | [AA: Model Leaderboard](https://artificialanalysis.ai/models) | Index v5.0.1，榜首 65 分 |
| 11/23 更新紀錄 | [Unsloth 文件的 23rd November Update](https://unsloth.ai/docs/models/inkling-2-mini) | 1.9× 解碼加速、主線 llama.cpp 相容、Q8_0 KV cache 修正 |
| 分項基準表 | 同上文件 Benchmarks 區塊 | 五模型對照，廠商自報 |

> <strong>查證說明</strong>：本文效能數字為 2026-11-23 在本機（RTX 4090 24 GB／i7-13700K／64 GB RAM）實測，llama.cpp b12588-mix-c0c3de8（CUDA 13 portable）＋ UD-Q4_K_XL；§6 的視覺測試於 11-24 凌晨用同一份權重加 `mmproj-F16` 重跑。<br />
> 分數與價格於 11-23／11-24 讀取 Artificial Analysis 模型頁，該站榜單每週更新，數字會漂。<br />
> §5 的分項對照表是廠商自報；模型卡的 DeepSWE v1.1 與 SWE-bench Pro v2 我沒有重跑，只做轉述並標明來源性質。<br />
> §6 的 GUI 定位只有 8 題、單一合成畫面、且無對照組，只能當哨兵不能當結論。<br />
> §8 的規格對照於 11-24 02:30 直接讀 Qwen3.8-27B 的模型頁（Apache 2.0、256k、文字＋影像＋影片、AA 20 分），不是憑印象。<br />
> 未測：tool calling、長 context 下的品質衰減、新版 dspark（481 MB）、以及 b12649 的 1.9× 是否適用於 4090。<br />
>
> <strong>封面與圖表</strong>：封面由本機 ComfyUI 的 Qwen-Image 2.1 生成（刻意不含文字）；<br />
> 圖 1 為手繪內嵌 SVG——含中文標籤的圖表交給 AI 生圖會爛成方塊。
