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

實際查了之後：<strong>模型是真的</strong>。`unsloth/Inkling-2-Mini-GGUF` 有 80 萬次下載、879 個讚，權重來自 Thinking Machines Lab、Apache 2.0，2026 年 11 月釋出。但貼文把三件事縫在一起：真的模型、挑過的對照組、以及一句會讓你買錯機器的硬體建議。以下是把它真的跑在 RTX 4090 上的完整紀錄——所有數字都是本機實測，或回到一手來源查證。

<!-- more -->

> <strong>一句話總結</strong>：Inkling 2 Mini 在 4090 上跑得動、答案也正確，但生成只有 25 tok/s、prefill 136 tok/s，而且 32K context 就吃掉 23.0／24.5 GB VRAM——<strong>1M context 在單張 24GB 卡上不存在</strong>。<br />
> 它是一顆值得下載來玩的模型，不是貼文說的那個「16GB 筆電就能跑」的東西。<br />

## 三十秒結論

| 問題 | 一句話回答 |
|---|---|
| 這是什麼 | Thinking Machines Lab 的 26B MoE（5.4B active），looped transformer，文字＋影像輸入，Apache 2.0 |
| 貼文哪部分是真的 | 參數、架構、1M context、48.2% DeepSWE v1.1、77.9% SWE-bench Pro v2 都對得上 |
| 實測速度（4090 / Q4_K_XL） | 生成 <strong>25 tok/s</strong>、prefill <strong>136 tok/s</strong> |
| 記憶體 | 32K context 用掉 23,169／24,564 MiB，剩 1.4 GB |
| 16GB 筆電能不能跑 | 只能跑 1–2 bit（9–11 GB）；官方建議的 4-bit 要 17.6 GB |
| 貼文哪裡誤導 | 「打贏 Claude Haiku 5.5」只在 Haiku 調到 low effort 時成立（20 vs 19） |
| 直不值得接進 coding agent | 不建議：prefill 136 tok/s，三萬 token 的 repo 要 3.7 分鐘才開始吐字 |

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
| ready for Unsloth + llama.cpp | ✅ 但要 Unsloth 自己的 llama.cpp build，主線認不得這個架構 |

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

<strong>第二，看功耗。</strong>這是關鍵：利用率 94–100%，功耗只有 133–136 W，而 4090 額定 450 W。滿載的算力工作會把功耗推到 300 W 以上；停在 134 W 代表 GPU 大部分時間在等資料，不是在算。合理的解釋是 looped transformer 每個 token 要重複過層，加上 MoE 的專家權重搬運，讓有效 FLOPs 遠高於「5.4B active」這個數字給人的印象。

也試了官方附的投機解碼（`dspark`，383.6 MB 的 draft 模型，`--spec-type draft-dspark`）：

| 設定 | 生成速度 | 接受率 | 平均接受長度 |
|---|---|---|---|
| 無 draft | 25.1 tok/s | — | — |
| dspark n_max=3 | 23.8 tok/s | 44–46% | 2.33–2.37 |

<strong>投機解碼在這裡是負收益</strong>：接受率不到一半，draft 的額外開銷蓋過省下的步數，而且多佔 VRAM。已經移除，回到乾淨配置。

## 五、Artificial Analysis 那 20 分要怎麼讀

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

## 六、我的實務結論

- <strong>想自己跑一顆 26B 來玩</strong>：可以，`UD-Q4_K_XL` ＋ 32K context ＋ CUDA 13 的 build，不要開 dspark。下載 16.4 GB，五分鐘的事。
- <strong>想接進 coding agent 當主力</strong>：不建議。prefill 136 tok/s 意味著每次重讀三萬 token 的 repo 要 3.7 分鐘，生成 25 tok/s 再疊上去，那個等待會把你逼回雲端 API。
- <strong>衝著 1M context 來的</strong>：換硬體。單張 24 GB 只能到 32K 左右。
- <strong>想讓它看圖</strong>：再抓 610 MB 的 `mmproj-F16.gguf`，多一個 `--mmproj` 參數。這輪沒測影像品質。
- <strong>貼文真正的價值</strong>：它讓你真的去下載了。它的數字要自己驗——尤其是「16GB 筆電」和「打贏 Claude Haiku 5.5」這兩句。

## 七、來源與延伸

| 實體 | 連結 | 實查結果 |
|---|---|---|
| GGUF 權重 | [unsloth/Inkling-2-Mini-GGUF](https://huggingface.co/unsloth/Inkling-2-Mini-GGUF) | 26.07B 參數、Apache 2.0、約 80 萬下載 |
| 官方跑法文件 | [Unsloth: Run Inkling 2 Mini](https://unsloth.ai/docs/models/inkling-2-mini) | 記憶體分級表、dspark 參數、looped-layer 需求 |
| 模型評測 | [AA: Inkling 2 Mini](https://artificialanalysis.ai/models/inkling-2-mini) | 20 分、5.4B active、1M context、$0.15／$0.50 |
| 全站排行 | [AA: Model Leaderboard](https://artificialanalysis.ai/models) | Index v5.0.1，榜首 65 分 |

> <strong>查證說明</strong>：本文所有效能數字為 2026-11-23 在本機（RTX 4090 24 GB／i7-13700K／64 GB RAM）實測，llama.cpp b12588-mix-c0c3de8（CUDA 13 portable）＋ UD-Q4_K_XL。<br />
> 分數與價格於同日讀取 Artificial Analysis 模型頁，該站榜單每週更新，數字會漂。<br />
> 模型卡自報的 DeepSWE v1.1 與 SWE-bench Pro v2 沒有重跑，本文只做轉述並標明其來源性質。<br />
> 未測：tool calling、影像輸入、長 context 下的品質衰減。<br />
>
> <strong>封面與圖表</strong>：封面由本機 ComfyUI 的 Qwen-Image 2.1 生成（刻意不含文字）；<br />
> 圖 1 為手繪內嵌 SVG——含中文標籤的圖表交給 AI 生圖會爛成方塊。
