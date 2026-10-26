---
title: Colab 上的 MiniMax H3：把「正確提示組」、Edge TTS 與聲音驅動數字人接成一條能重跑的線
date: 2026-10-26 18:30:00
categories:
  - AI
  - 技術實測
tags:
  - MiniMax-H3
  - ComfyUI
  - Google Colab
  - Edge-TTS
  - 聲音驅動
  - 提示工程
  - sol-attn
  - Triton
  - Colab Pro
  - NVIDIA L4
  - 影片生成
  - 開源
toc: true
index_img: /img/covers/colab-h3-voice-driven.png
banner_img: /img/covers/colab-h3-voice-driven.png
---

> <strong>整理說明</strong>：MiniMax H3 是少數「一次採樣同時出畫面＋立體聲」的影片模型，所以「數字人」這件事其實不需要先做唇形同步——把參考音訊掛進 <code>r2v</code> 的 <code>&lt;Audio 1&gt;</code> 槽，模型就會照著聲音動嘴。這篇把整條線查證過一遍並且實測跑通：<strong>(1)</strong> 先釐清三個容易走錯路的硬事實（PRISM 到底能幹嘛、sol-attn 在哪張卡有效、24GB 該抓哪些權重）；<strong>(2)</strong> 拆解「正確的 H3 提示組」到底長什麼樣——多數數字人工作流亂講話，缺的就是時間碼分鏡與音軌同步指示；<strong>(3)</strong> 示範聲音驅動的關鍵：提示詞裡的時間碼要用 <strong>TTS 音軌的真實長度</strong>回推，不是均分；<strong>(4)</strong> 端到端實測：Edge TTS 繁中 2 句 → <code>r2v</code> → 69.2 秒產出 864×480、帶聲音的 10.1 秒影片。最後把整條線包成開源套件 <a href="https://github.com/kalpakjian/colab-h3">colab-h3</a>，附一份程式碼內嵌、Colab 直接 Run all 的 notebook。
>
> 文中每個權重檔名與大小都經 HuggingFace API 實查；每個節點名稱都對過真實 ComfyUI 的 <code>/object_info</code>；「本機實測」段落全部是 RTX 4090 上的真實輸出（含 <code>ffprobe</code> 與音量數值），Colab 的數字則另標明來源。

<!-- more -->

## 先講結論

1. **Colab 跑 H3 不是玩票，是真的能出片的。** L4 24GB 上抓 0.4MP、10 秒的草稿檔，量測大約 5 分鐘（內含下載與開機）；權重下載約 1 分鐘、ComfyUI 本身約 34 秒。訂閱本來就在付的 Google AI Pro，等於多一台免費 GPU。
2. **但「掛個模型就跑」會踩三個坑**，而且三個都很貴：PRISM 是 **ref2va** 權重（只能做參考主體／參考音訊，不能純文字生成）、sol-attn **吃不到 A100**、24GB 的權重組合必須自己算。
3. **數字人亂講話，八成不是模型的問題，是提示組的問題。** H3 官方範例工作流的提示組固定是四段：風格句 → `Storyboard:` + 時間碼 → `Audio:` 行 → 禁止項。少了時間碼與音軌同步指示，模型只能自由發揮。
4. **聲音驅動的時間軸要從 TTS 出發。** 提示詞裡的 `[0s-4.6s]` 必須是 TTS 音軌的**真實長度**，不是把總長平均切。這一條做完，嘴型自然就對上了。
5. **端到端實測通過**：Edge TTS 繁中 2 句（9.120 秒）→ `r2v` + `ref_audio_0` → 4090 上 **69.2 秒**產出 864×480、24fps、10.125 秒、帶 32kHz 立體聲的 mp4，音軌音量與輸入 TTS 幾乎一致（證明生成的是那把聲音，不是雜訊）。
6. **整條線已包成開源套件**：[colab-h3](https://github.com/kalpakjian/colab-h3)，內含一份程式碼內嵌、Colab 直接 Run all 的 notebook，不用先把檔案推上 GitHub。

## 一、速度實測：Colab 的數字可信

先看一組在 Colab 上的量測（同一台機器、同一組權重）：

| 階段 | 耗時 | 備註 |
|---|---:|---|
| 下載 ComfyUI | 34 秒 | `git clone` + requirements |
| 下載模型組 | 約 1 分鐘 | 含 UNET／CLIP／VAE |
| 生成 0.4MP、10 秒 | 約 5 分鐘 | 端到端，含開機與設定 |

對照本機 4090 的正式接龍產線（1344×768、6 步、約 10 秒一段，每段 180–220 秒），**Colab 上做 0.4MP 草稿檔的單位成本是划算的**。真正的問題不是跑不跑得動，而是「跑得動但接錯線」。

所以這篇的重點放在**接線的正確性**：模型、節點、提示組、TTS 四個環節各有一個不查清楚就會白花的坑。

## 二、三個必須先釐清的事實

### PRISM 是 ref2va，不是 fl2va

`OliviaRossi/Minimax-h3_Singularity-x-10Eros-Max_PRISM` 的模型卡 tags 直接寫著 `MiniMax H3 Merge ref2va`：它是 `WarmBloodAban/Minimax-h3_Singularity` 與 `TenStrip/10Eros-Max`（8-step turbo）的 merge，用自訂的 PRISM 演算法（SVD 分解＋SLERP＋符號衝突仲裁）合併。

| 檔案 | 大小 | 用途 |
|---|---:|---|
| `Minimax-h3_Singularity_x_10Eros-Max_PRISM_fp16.safetensors` | 61.70 GB | 80GB 卡 |
| `Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors` | 18.89 GB | 40GB 卡 |
| `Minimax-h3_Singularity_x_10Eros-Max_PRISM_w6a8.safetensors` | 14.81 GB | **24GB 卡首選** |

**它不能當 t2v/i2v 用。** H3 有兩條不同的權重路線：

- `fl2va`（first/last frame to video+audio）→ 純文字生圖、圖生片、首尾幀
- `ref2va`（reference to video+audio）→ 參考主體、參考音訊、參考影片

而 PRISM 是 **ref2va**。這其實是好事——「聲音驅動的數字人」本來就要走 `r2v`，PRISM 的位置就是這裡；純文字生成另外抓 `fl2va` 就行，兩者不能混用。

### sol-attn 只吃 SM86 以上：L4 可以，A100 不行

`Saganaki22/ComfyUI-sol-attn` 是 NVIDIA Sol-Attn 的 Triton 實作，v0.6.2 明確列出的架構是 **SM86 / SM89 / SM90 / SM100 / SM120 / SM121**。對照一下手上的卡：

| GPU | 架構 | sol-attn | 說明 |
|---|---|---|---|
| RTX 5090 | SM120 | ✅ | 官方測試機 |
| **L4** | **SM89** | **✅** | 指標 1.14–1.44× vs SageAttention，H3 MLP 峰值記憶體 −37% |
| A100 | SM80 | ❌ | 不在清單 → dense fallback，功能正常但沒加速 |
| T4 | SM75 | ❌ | 同上，而且 H3 要 bf16，T4 會慢到不值得 |

所以「L4 掛個 solattn 開心」完全成立；但「燒 A100 下去跑」那段，sol-attn 是插不進去的（它是 kernel 層的架構限制，不是設定問題）。

它提供的四個節點：

| 節點 | 作用 |
|---|---|
| `SolAttentionPatch` | 通用稀疏注意力 patch（MODEL → MODEL） |
| `MiniMaxH3MemoryEfficientSolAttentionPatch` | H3 專用：直接從融合 qkv 投影切視圖，省掉 q/k/v 複製 |
| `MiniMaxH3ScheduledSolAttentionPatch` | 依 sigma 排程的稀疏度 |
| `MiniMaxH3ChunkFeedForward` | 把 token-local FFN 切塊，砍峰值記憶體 |

kernel 的硬條件是 head_dim 128、bf16、無 mask、4D q/k/v——H3 剛好全部符合（56 heads × 128、bf16）。

### 24GB 的權重組合要自己算

H3 的 CLIP 是 Qwen3-VL 32B，這才是真正的體積殺手。官方 `Comfy-Org/MiniMax-H3` 倉庫的實測檔名與大小：

| 用途 | 檔名 | 大小 |
|---|---|---:|
| UNET (t2v/i2v/fl2v) | `minimax_h3_fl2va_pruned_w6a8.safetensors` | **14.89 GB** |
| UNET (t2v/i2v/fl2v) | `minimax_h3_fl2va_pruned_int8_convrot.safetensors` | 19.53 GB |
| UNET (t2v/i2v/fl2v) | `minimax_h3_fl2va_pruned_bf16.safetensors` | 37.46 GB |
| UNET (r2v) | `minimax_h3_ref2va_pruned_w6a8.safetensors` | 14.89 GB |
| CLIP | `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | **14.61 GB** |
| CLIP | `qwen3vl_32b_minimax_h3_int8_convrot.safetensors` | 25.28 GB |
| CLIP | `qwen3vl_32b_minimax_h3_bf16.safetensors` | 47.97 GB |
| Video VAE | `minimax_h3_video_vae_int8_convrot.safetensors` | **2.62 GB** |
| Video VAE | `minimax_h3_video_vae_fp16.safetensors` | 4.85 GB |
| Audio VAE | `minimax_h3_audio_vae_fp32.safetensors` | 0.56 GB |
| Turbo LoRA (fl2v) | `minimax_h3_turbo_v4_step600_ema.safetensors`（`larryvrh/MiniMax-H3-Turbo-Lora`） | 0.73 GB |
| ref2v Turbo LoRA | `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors` | 1.82 GB |

L4 24GB 的正解是 **w6a8 UNET（14.89）＋ 4-bit CLIP（14.61）＋ int8 Video VAE（2.62）＋ Audio VAE（0.56）＝ 32.7GB**。這還是超過 24GB，靠的是 ComfyUI 的權重 streaming ＋ `MiniMaxH3ChunkFeedForward` 分塊 ＋ sol-attn 的峰值記憶體削減，三樣一起才擠得進去。

> 一個容易踩的細節：**CLIPLoader 的 `type` 必須是 `minimax`**（Qwen3-VL），選錯會整個讀不出來。

## 三、「正確的 H3 提示組」長什麼樣

H3 用 Qwen3-VL 做自由提示詞，表面上「寫一句中文丟進去」就能跑——但官方範例工作流的格式其實非常固定。從 `ComfyUI_MiniMaxH3_Director` 附的 `minimax_h3_director_t2v.json` 抽出來的 `global_prompt` 長這樣：

```
Realistic live-action cinematic look: a post-rain dusk metropolis, anamorphic lens,
shallow depth of field, film grain, city volumetric fog, flying-car traffic between towers.

Storyboard:
[0s-2s] High side angle: protagonist sprinting at a roof edge, wind catching their coat.
[2s-3.5s] Leap across the gap between buildings, body stretching mid-air.
[3.5s-5s] Landing and roll, low-angle shot, keep running into fog.

Audio: wind, rapid footsteps, city ambience, low score with accent hits on each leap.
No text, logos or watermarks.
```

拆開看是四個零件，少一個就會退化：

| 零件 | 作用 | 少了會怎樣 |
|---|---|---|
| 風格句 | 主體＋場景＋鏡頭＋景深＋色調＋動態細節 | 畫面風格每次都飄 |
| `Storyboard:` + `[起-訖]` 時間碼 | 把整段切成有邊界的節拍 | **模型自由發揮，動作對不上** |
| `Audio:` 行 | 說清楚聽到什麼、跟畫面什麼關係 | 聲音與畫面各說各話 |
| 禁止項 | 水、字幕、浮水印、換臉 | 常見瑕疵 |

第 2 與第 3 個就是「數字人看起來在亂講話」的主因：**沒有時間碼，模型不知道哪一段該說哪一句；沒有音軌同步指示，模型不知道嘴要跟著 `<Audio 1>` 動。**

寫提示組還有兩個細節：

- **節拍數不要超過 3 個複雜變化**。一段 10 秒塞四個大動作，模型會糊、會跳切。官方節奏是 1–2 個節拍／10 秒。
- **英文優先**。H3 的 CLIP 是 Qwen3-VL，中文讀得懂，但官方測試路徑都是英文；中文台詞的正確位置是走 TTS 進 `<Audio 1>`，不是塞進分鏡描述。

## 四、聲音驅動的正確接法

H3 的 `r2v` 任務有個特別好用的設計：**參考音訊是原生輸入**，不是事後配音。`MiniMaxH3ReferenceToVideo` 的節點定義裡，音訊有三個槽：

| 槽位 | 用途 |
|---|---|
| `ref_audio_0` … `ref_audio_3` | 獨立參考音訊（我們的 TTS 掛這裡） |
| `ref_video_0` … `ref_video_3` | 參考影片（會自動抽軌並掛 `<Audio j>` 標籤） |
| `ref_image_0` … `ref_image_9` | 參考主體圖 |

音訊在提示詞裡就是 `<Audio 1>`、`<Audio 2>` 這樣的標籤。於是完整接法是：

1. **TTS 產出語音**：Edge TTS（微軟線上服務，免費、繁中音色齊）→ ffmpeg 轉 32kHz 單聲道 16-bit wav（H3 音訊 VAE 的原生格式）。
2. **量出每句的真實長度**：wav 的 frame 數 ÷ 採樣率，精確到毫秒。
3. **用真實長度回推分鏡時間碼**：第 1 句 4.608 秒、第 2 句 4.512 秒 → `[0s-4.6s]`、`[4.6s-9.1s]`。這一步是整個聲音驅動的關鍵。
4. **提示組的 Audio 行明寫同步**：`Audio: clear female Mandarin voice, spoken from <Audio 1>, lip movements and jaw synchronized to <Audio 1>, steady face, no extra talking.`
5. **幀數對齊音軌總長**：H3 的幀數必須落在 17k+5 的網格（124 ≈ 5.2 秒、243 ≈ 10.1 秒、362 ≈ 15.1 秒 @24fps），所以按音軌長度換算後要吸附到最近的合法值。

第 3 步如果偷懶改用「平均切」，就會出現很典型的現象：**台詞念完了畫面還在講，或者畫面動作比聲音早半拍**。嘴型對不上，看起來就像「亂講話」。

## 五、端到端實測（本機 RTX 4090）

整條鏈在真實 ComfyUI（0.42.5、torch 2.16.0.dev+cu132）上跑完，指令與數據都留著：

| 項目 | 值 |
|---|---|
| TTS | Edge TTS `zh-TW-HsiaoChenNeural`，2 句 → 4.608s + 4.512s = **9.120s** |
| 時間碼 | `[0s-4.6s]` / `[4.6s-9.1s]`（依真實音軌長度，非均分） |
| UNET | `minimax_h3_ref2va_pruned_int8_convrot.safetensors` |
| LoRA | `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors` |
| CLIP | `qwen3vl_32b_heretic_minimax_h3_nvfp4.safetensors`（type = `minimax`） |
| 任務 | `r2v`，參考音訊掛 `ref_audio_0` |
| 產出 | 864×480、24fps、**10.125 秒**、32kHz 立體聲音軌 |
| 耗時 | **69.2 秒**（243 幀、6 步） |

音軌對照（這是「真的是那把聲音」的證據，不是雜訊）：

| 音訊 | mean volume | max volume |
|---|---:|---:|
| 輸入（TTS） | −19.2 dB | −3.6 dB |
| 輸出（成片） | −18.5 dB | −0.7 dB |

畫面驗證——第一句話時嘴型張開，第二句話時**手真的舉起來指向後方螢幕**（正是提示組裡寫的節拍），身份鎖定不變：

![第一句台詞時：鏡頭正對、嘴型張開說話](/img/colab-h3-voice-driven/frame-2s.png)

![第二句台詞時：右手舉起指向後方螢幕，嘴型同步變化](/img/colab-h3-voice-driven/frame-6s.png)

> 成片與完整提示組在 [colab-h3 的 `examples/`](https://github.com/kalpakjian/colab-h3/tree/main/examples)。

## 六、colab-h3：把這條線包成能重跑的套件

實測完就把它收成一個獨立的客戶端套件（放在 `D:\AI\colab-h3\`，已開源到 [kalpakjian/colab-h3](https://github.com/kalpakjian/colab-h3)）。它**不跑模型**，只做三件事：佈署遠端 ComfyUI、把提示組編對、把聲音驅動的時間軸算準。

| 模組 | 職責 |
|---|---|
| `config.py` | 經 HF API 實查的權重檔名與大小；算力檔案（`l4`／`l4_ref`／`a100`／`t4`…） |
| `prompt_compiler.py` | brief → 官方格式提示組；三種後端：`rule`（離線規則）、`llm`（任何 OpenAI 相容端點或 Gemini）、`director`（直接打 ComfyUI 的提示強化路由） |
| `tts_voice.py` | Edge TTS → 32kHz 單聲道 wav，並回報每句真實長度 |
| `payloads.py` | t2v/i2v/fl2v/r2v 的 ComfyUI API 節點圖；節點沒裝會自動降級並提示 |
| `client.py` | ComfyUI HTTP 客戶端（提交／輪詢／收檔／錯誤診斷） |
| `setup_colab.py` | 冪等安裝；Google Drive 當權重倉庫 |

有兩個設計決定值得講一下：

**算力檔案（profile）把「跑哪張卡」變成一個值。** `l4` 是 864×480、124 幀、Turbo 8 步、w6a8 UNET；`a100` 是 1344×768、124 幀、官方 25 步、int8 UNET。`doctor` 會先偵測 GPU 再建議要哪一個。

**Drive 只是倉庫，執行走本機磁碟。** 下載先落到 `/content/drive/MyDrive/ComfyUI-H3`，再複製一份到 `/content/ComfyUI/models`。因為 Drive 的 FUSE 讀取很慢——直接從 Drive 載入 15GB 的 UNET，會慢到不能忍。

Colab 端有一份 `ComfyUI_H3_Colab.ipynb`：**18 格、每個模組用 `%%writefile` 內嵌**，不需要先把檔案推上 GitHub，開了就 Run all。

## 七、算力與額度：什麼在 L4、什麼要 A100

| profile | 解析度 | 幀數 | 步數 | UNET | 適用情境 |
|---|---|---:|---:|---|---|
| `l4` | 864×480（0.4MP） | 124（5.2s） | 8（Turbo） | `fl2va_pruned_w6a8` | L4 24GB 草稿 |
| `l4_ref` | 864×480 | 124 | 8 | `PRISM_w6a8`（ref2va） | L4 聲音驅動數字人 |
| `l4_ref_turbo` | 864×480 | 124 | 6（Turbo） | `ref2va_pruned_w6a8` | 4 步 turbo 配方 |
| `a100` | 1344×768（1.0MP） | 124 | 25（官方） | `fl2va_pruned_int8_convrot` | A100 40GB 正式 |
| `a100_ref` | 1344×768 | 124 | 25（官方） | `PRISM_int8` | A100 聲音驅動 |
| `t4` | 864×480 | 124 | 8 | `fl2va_pruned_w6a8` | **不建議**（見下） |

實務上的建議節奏：

- **草稿用 L4**：0.4MP、5 秒、Turbo 8 步。先用便宜的卡把故事板與台詞調對，再決定要不要上正式檔。
- **正式檔用 A100**：1344×768 要 33GB 以上的權重與更高的峰值，L4 會很緊；而且 A100 是 SM80，**sol-attn 在上面不生效**。
- **T4 不要碰**：SM75 沒有 sol-attn，H3 要 bf16，等於用最慢的路徑跑最貴的卡。
- **用完記得中斷 runtime**，別讓 VM 掛著吃點數。權重放著不跑也會占著 VM。

Turbo LoRA 的步數建議（來自 `larryvrh/ComfyUI-MiniMax-H3-Turbo` 的說明）：4 步是下限、4–8 步是有效區間、**超過 8 步不會更好還可能過銳**；`strength` 維持 1.0。`low_vram` 開啟會把 LoRA 併進權重，峰值最低，但在量化權重上畫面會偏軟。

## 八、踩過的坑（每一個都省下好幾小時）

| 坑 | 症狀 | 解法 |
|---|---|---|
| **ComfyUI 沒有 `/upload/audio` 端點** | 上傳參考音訊回 HTTP 405 Method Not Allowed | 只有 `/upload/image` 與 `/upload/mask`；音訊必須直接複製進 `input/` 目錄 |
| autogrow 槽的 API 命名 | 不知道該傳 `ref_audio` 還是別的 | 前綴＋索引：`ref_audio_0`、`ref_image_0`、`ref_video_0`、`ref_video_audio_0` |
| Turbo 路徑多了 SigmaShift | 官方 Turbo 範例工作流與本機已驗證的 payload **都沒有** `MiniMaxH3SigmaShift` | Turbo 路徑：UNET → TurboLoRA → BasicScheduler(simple) → TurboSampler；官方 25 步路徑才有 SigmaShift(12, 3) |
| H3 需要新版 ComfyUI | 找不到 `MiniMaxH3ImageToVideo` 節點 | H3 官方節點要 ComfyUI **≥ 0.30.0** |
| 幀數不在網格上 | 採樣異常或長度不對 | 幀數必須是 17k+5（124／141／…／243／362） |
| Drive 直接載模型 | 慢到以為當機 | Drive 當倉庫，執行前複製到本機磁碟 |
| Windows PowerShell 改 UTF-8 原始碼 | 中文全變亂碼、整份檔案壞掉 | PS 5.1 的 `Get-Content` 用 GBK 解碼；要改檔案用編輯器或 Python 本身 |
| `set VAR=value && cmd` | 環境變數尾巴多一個空白，路徑全錯 | `.strip()` 環境變數（`cmd` 會把 `&&` 前的空格吃進值） |

## 九、把 colab-h3 拿來跑

Colab（最快的一條）：

1. 打開 [colab-h3 的 `ComfyUI_H3_Colab.ipynb`](https://github.com/kalpakjian/colab-h3)，在 Colab 選 **Runtime → Run all**。
2. 依序跑完 8 格：環境檢查與掛載 Drive → 寫入套件 → 裝 ComfyUI／節點／權重 → 啟動 → 提示強化 → TTS → 生成 → 存檔。

命令列（本機或 Colab 終端）：

```powershell
cd D:\AI\colab-h3
python -m h3colab.cli doctor                      # GPU / ComfyUI / 節點 / 權重檢查
python -m h3colab.cli setup --profile l4 --download --store drive
python -m h3colab.cli video --script script.txt --profile l4_ref \
    --subject "a Taiwanese news anchor" --scene "a modern studio desk" \
    --beat "the presenter looks straight into the lens and opens her mouth to speak" \
    --beat "she raises one hand and points toward the screen behind her"
```

`--beat` 是**英文視覺描述**、一句對一句對著台詞；台詞本身留在中文，走 TTS 進 `<Audio 1>`。這個分工就是多數數字人工作流缺的那一塊。

自我檢查（不依賴 pytest）：

```powershell
python tests\run_tests.py       # 75 項，含對真實 ComfyUI /object_info 的活體驗證
python tools\verify_notebook.py # notebook 結構 + 內嵌模組與原檔一致
python tools\e2e_local_test.py  # 端到端（需要本機 ComfyUI 在 8188）
```

## 結語：算力是夠的，接線才是瓶頸

「訂閱本來就在付，卡頓拿來跑 ComfyUI」這個經濟模型是成立的——Colab 的 L4 確實能在 5 分鐘內出草稿檔，400 點左右夠用很久，權重放 5TB 雲端硬碟慢慢養也沒問題。

但真正決定能不能用的，是那四個接線細節：**PRISM 是 ref2va、sol-attn 只吃 SM86+、提示組要有時間碼與音軌同步指示、時間軸要從 TTS 的真實長度回推**。這四件事弄對了，數字人就不會「亂講話」；少了任何一件，跑得再快也只是在生產垃圾。

程式碼、權重清單與實測素材都在 [github.com/kalpakjian/colab-h3](https://github.com/kalpakjian/colab-h3)，拿去改成自己的故事板吧。


