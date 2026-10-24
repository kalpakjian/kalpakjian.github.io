---
title: MOSS-Image 5B vs Qwen-Image 2.1：同機實測比較（耗時、VRAM、文字渲染、功能對照）
date: 2026-10-24 09:30:00
categories:
  - 技術筆記
tags:
  - 人工智慧
  - MOSS-Image
  - Qwen-Image
  - ComfyUI
  - LoRA
  - 效能實測
  - 基準測試
index_img: /img/covers/moss-vs-qwen-image.png
banner_img: /img/covers/moss-vs-qwen-image.png
toc: true
---
# MOSS-Image 5B vs Qwen-Image 2.1：同機實測比較

Qwen-Image 2.1 是 2026-10-23 這天 ComfyUI 內建的另一個原生模型，本機剛好兩套都有，
於是直接用**同一台機器、同一個 seed、同一組提示詞**逐張對打，
共跑了 18 次（3 提示詞 × 2 模型 × 3 解析度）。

## 一、規格對照

| | MOSS-Image 5B | Qwen-Image 2.1 |
| --- | --- | --- |
| 發布 | 2026-10（OpenMOSS / MOSI.AI） | 2026（Alibaba Qwen 團隊） |
| 參數量 | **5B** | **20B** |
| 架構 | 單流 DiT（single-stream），Muon optimizer 訓練 | MMDiT |
| Text encoder | `qwen3.5_9b` int8（9.08 GiB） | `qwen3vl_8b`（本機 bf16 16.33 GiB） |
| VAE | `flux2-vae_small`（0.23 GiB） | `qwen_image_2.1_vae_bf16`（0.63 GiB，**4 通道含 alpha**） |
| 官方取樣 | ≥50 步 / CFG 3 / shift 5 / Euler + sgm_uniform / SLG skip layer 22 | 25 步 / CFG 1 / Euler + simple / 內建 shift |
| 負向提示詞 | 需要（官方建議 5 個負向詞） | **不需要**（CFG 1.0，positive=negative） |
| 推薦像素量 | 1M / 1.5M / 2M | 原生 2K（2048×2048） |
| 外推範圍 | 0.25M～4M（實測可到 6.55M） | 原生 2K（實測可到 6.55M） |
| 獨有能力 | **JSON Layout 精準控制**、**色／深控制 adapter** | **生成＋編輯同一權重**、多圖參考(16)、**alpha 透明背景**、PE 自動改寫、官方加速 LoRA |
| ComfyUI 支援 | v0.42.0 起原生內建（2026-10-16 合併） | 原生內建，另有 `TextEncodeQwenImage21` / `QwenImage21Cache` 等專用節點 |
| 授權 | Apache-2.0 | Apache-2.0 |

> 兩邊都是 Apache-2.0，都能在 ComfyUI 原生跑，
> 都有 LoRA 生態（KohakuMossTrainer／DiffSynth）。

## 二、關鍵數據：耗時與 VRAM

| 解析度 | 像素量 | MOSS-Image 5B | Qwen-Image 2.1 | 倍數 |
| --- | --- | --- | --- | --- |
| 1024×1024 | 1.05 MP | **19.4 秒** | **11.3～12.1 秒** | 1.6～1.7× |
| 2048×2048 | 4.19 MP | **80.9～85.6 秒** | **29.8～32.2 秒** | 2.6～2.7× |
| 2560×2560 | 6.55 MP | **152.4～162.1 秒** | **50.1～55.6 秒** | 2.8～3.0× |

![MOSS-Image 5B vs Qwen-Image 2.1 完整實測數據表](/img/moss-vs-qwen-image/08_moss_vs_qwen_table.jpg)

**Qwen-Image 2.1 全面更快，而且像素量越大差距越明顯。**
原因很單純：MOSS 官方要求 ≥50 步、而且 `SkipLayerGuidanceDiTSimple` 是 *two-pass sampling*
（負向分支要額外跑一次，官方也提醒 SLG 會強制 eager execution）；
Qwen-Image 2.1 官方範本用 25 步，而且它是**原生 2K**，不需要外推。

峰值 VRAM 則是 MOSS 比較省（text encoder 用 int8 的 `qwen3.5_9b` 9.08 GiB，
Qwen 用 `qwen3vl_8b`，本機是 bf16 版 16.33 GiB）：

| 解析度 | MOSS-Image 5B | Qwen-Image 2.1 |
| --- | --- | --- |
| 1024×1024 | 15.4～21.4 GiB | 23.0～23.1 GiB |
| 2048×2048 | 19.7～21.9 GiB | 23.1～23.2 GiB |
| 2560×2560 | 22.5～23.1 GiB | 23.1～23.2 GiB |

## 三、文字渲染：兩個模型幾乎打平

![中文文字渲染海報對比：左 MOSS-Image 5B，右 Qwen-Image 2.1](/img/moss-vs-qwen-image/05_moss_vs_qwen_cntext.jpg)

提示詞是「一張咖啡店宣傳海報，頂部有中文標題『城市漫遊』，下方有英文副標題『CITY WALK』」。

**兩個模型的主標題「城市漫遊」和副標題「CITY WALK」都渲染完美、筆畫正確。**
差別在版面風格：MOSS 排版層次豐富、插畫有配色材質，偏「成品海報」；
Qwen 留白大、線稿乾淨，偏「設計稿／簡報模板」。

> ⚠️ 但**兩個模型的小字都是亂碼**——MOSS 的頂部小字是 `PA AJOIDO`、
> Qwen 的底部中文小字是 `良祝益迎何泡` 這類無意義字。
> 「大字正確、小字崩掉」是兩者共同的弱點。

![英文招牌文字對比：左 MOSS-Image 5B，右 Qwen-Image 2.1](/img/moss-vs-qwen-image/06_moss_vs_qwen_entext.jpg)

英文招牌同樣是平手：**兩個模型都把 "MOSS & BEAN" 渲染得完全正確**，連 `&` 符號都對。
MOSS 是藍調時刻＋暖色店光、資訊量較大；Qwen 是更深的夜色、氣氛更收斂。

![寫實室內場景對比：左 MOSS-Image 5B，右 Qwen-Image 2.1](/img/moss-vs-qwen-image/07_moss_vs_qwen_photo.jpg)

寫實場景的風格差異是**系統性的**：MOSS 偏「敘事性構圖」（元素多、像有人住過），
Qwen 偏「乾淨商業視覺」（元素少、接近商品攝影）。

## 四、各項能力對照

> ✅＝本機實測通過　⚠️＝實測有落差　📄＝僅官方文件記載

| 能力 | MOSS-Image 5B | Qwen-Image 2.1 |
| --- | --- | --- |
| 中英文大標題渲染 | ✅ 實測完美 | ✅ 實測完美 |
| 密集小字 | ❌ 亂碼 | ❌ 亂碼 |
| **JSON Layout 精準控制** | ✅ **獨有**，bbox 實測精準命中 | ❌ |
| **色／深控制 adapter** | ✅ **獨有**（`MOSSImageControl` 節點） | ❌ |
| **圖像編輯 / 局部編輯** | ❌ | ✅ 實測可用（**須用 `<image1>`**） |
| **多圖參考** | ❌ | ✅ 實測可用（最多 16 張） |
| **Alpha 透明背景** | ❌ | ⚠️ 有 4 通道但實測去背效果有限 |
| **Prompt 自動改寫** | ❌ | ✅ 實測可用（對文字渲染特別有價值） |
| KV cache 加速 | ❌ | ✅ 記憶體吃緊時快 25%（一般情況無差異） |
| 蒸餾加速 LoRA | 官方「進行中」（社群有 4 步 adapter） | ✅ 官方 Turbo LoRA 8 步快 4.5×；社群 Lightning 4 步快 8.1× |
| **LoRA 訓練** | ✅ **官方第一方支援**（6.20 GiB 實測可跑） | 📄 社群支援 |
| 省 VRAM | ✅ | ❌（實測吃滿 23.2 GiB） |

## 五、實測驗證的獨有能力

### 5.1 MOSS 的 JSON Layout 精準控制

— 指定 bbox 後，文字與物件**精確落在指定位置**：

![MOSS-Image JSON Layout 實測：標題 EXPLORE 在上方、山峰插畫在下方中央](/img/moss-vs-qwen-image/09_moss_layout.jpg)

用的是官方 README 的 Python API 寫法（layout JSON 直接當 prompt 傳）：

```json
{"summary":{"caption":"A minimalist travel poster with a cream background, a blue mountain illustration, and the title EXPLORE at the top."},
 "items":[{"label":"text","caption":"Large dark-blue uppercase title centered at the top.","text":"EXPLORE","bbox":[-472,-308,-348,308]},
          {"label":"object","caption":"A flat blue mountain illustration in the lower center.","bbox":[-256,-205,410,205]}],
 "bbox_coord_space":"abs_centralized","bbox_format":"yxyx"}
```

> ⚠️ 順帶踩到一個坑：**`MOSSImageLayoutPrompt` 節點在 API 模式下不能用**。
> 它的 `element` 是 ARRAY 型、驗證時要對元素取 hash（dict 不可 hash），
> 而正確來源 `CreateBoundingBoxes` 的 `editor_state` 是 `BOUNDING_BOXES` socketless widget、
> 必須由畫布節點連線進來，但沒有任何節點輸出這個型別。
> **解法就是上面那段 JSON**（官方 README 也是這樣建議的）。

### 5.2 Qwen 的圖像編輯

— 保留原圖的房間、窗戶、陽光、植物、床，只換掉桌子：

![Qwen-Image 2.1 圖像編輯實測](/img/moss-vs-qwen-image/10_qwen_edit.jpg)

> ⚠️ **指令必須用 `<image1>` 明確指涉參考圖。**
> 第一次測試沒寫 `<image1>`，模型直接把它當一般 t2i 重新生成了一張新圖（連房間都換了）。
> 加上 `<image1>` 之後才真的做到「只改指定部位、其餘保留」。

### 5.3 Qwen 的多圖參考

— 同時餵兩張圖，融合它們的配色與紋理：

![Qwen-Image 2.1 多圖參考實測](/img/moss-vs-qwen-image/11_qwen_multiref.jpg)

`TextEncodeQwenImage21` 的 `images` 用 dict 格式（最多 16 張）：

```json
"images": {"image_1": ["4", 0], "image_2": ["5", 0]}
```

### 5.4 Qwen 的 Alpha 通道

：

| 測試 | 輸出模式 | 完全透明 | 半透明 | 完全不透明 |
| --- | --- | --- | --- | --- |
| 一般 t2i（prompt 寫 transparent background） | **RGBA** | 0.0% | 1.3% | 98.7% |
| 官方去背做法（編輯 +「output a PNG image」） | **RGBA** | 0.0% | 6.7% | 93.3% |

VAE 確實解出 4 通道（輸出檔是 RGBA），但**一般 t2i 不會給你透明背景**，
只是多了一個幾乎全滿的 alpha 通道。官方 `background_removal` 範本的做法是
「編輯 + 指示輸出 PNG」，透明背景是**模型生成進 alpha 通道**、不是事後抠图；
實測背景乾淨時有改善，但**沒有到完全透明**、主體邊緣也不是乾淨 alpha。
**真的要乾淨去背，rembg 這類傳統工具仍然更可靠。**

### 5.5 Qwen 的 Prompt 自動改寫

Prompt 自動改寫（Prompt Enhancer）✅ — 對文字渲染幫助最大**

輸入只有六個字 `a cafe poster`，PE 模型會改寫成一份完整的結構化海報概念書
（配色、邊框、主標題字樣、插畫描述都寫好），再餵給影像模型：

![Prompt 自動改寫對比](/img/moss-vs-qwen-image/12_pe_compare.jpg)

| | 標題 | 畫面 |
| --- | --- | --- |
| 原始 prompt 直接生成 | `BIRON H TREE`（亂碼） | 構圖雜亂 |
| **PE 改寫後** | `GOOD COFFEE, Good Day`（正確） | 專業海報，含插畫與菜單板 |
| PE thinking 模式 | `BREWED Goodness` + `COZY CUPS COFFEE · PASTRIES · GOOD VIBES` | 更精緻 |

**為什麼值得特別提**：PE 把「想渲染的文案」明確寫進 prompt，模型就不會自己亂猜要寫什麼字。
**要出帶字的海報，PE 是最快的改善手段** — 比換模型有效得多。
實測 18.8～22.0 秒（含 PE 模型載入與改寫），PE text encoder 本身要 **8.82 GiB**。

### 5.6 MOSS 的色／深控制 adapter

MOSS-Image 的色／深控制 adapter — 真的能鎖位置**

![MOSS 色／深控制對比](/img/moss-vs-qwen-image/15_moss_control_compare.jpg)

`MOSSImageControl` 節點 + `moss-control.safetensors`（299 MB，**社群版** `darask0`）。
給定**色域圖**（每個區域一個純色，顏色只是 ID）+ **深度圖**（灰階，近＝白）之後：

| 設定 | 耗時 | 結果 |
| --- | --- | --- |
| 無控制（`strength=0`） | 13.6 秒 | 正常真人 |
| **控制到 50%** | 20.5 秒 | **3D 人偶精確出現在指定位置** |
| **控制到 100%** | 13.4 秒 | 人偶佔據更大版面 |

> ⚠️ 實測重現了 adapter README 明載的「mannequin look」限制 ——
> 餵 3D 人偶的深度圖，輸出會帶出人偶的表面質感。
> README 建議 `end_percent=0.5` 並**搭配 region prompts**（每個顏色一句描述），
> 才會變成「地圖上那個位置的真實人物」。這點我還沒測。

## 六、加速功能實測

### 6.1 Qwen 加速 LoRA：官方 Turbo 8 步 / 社群 Lightning 4 步

官方 Turbo LoRA — 4.5 倍加速，品質穩**

![加速 LoRA 對比](/img/moss-vs-qwen-image/14_turbo_compare.jpg)

| 設定 | 步數 | 耗時 | 加速比 | LoRA 大小 | 性質 |
| --- | --- | --- | --- | --- | --- |
| 無 LoRA（官方推薦） | 25 | 12.2 秒 | 1× | — | — |
| **官方 Turbo LoRA** | 8 | **2.7 秒** | **4.5×** | 871 MB | ✅ 官方（`Comfy-Org`） |
| **社群 Lightning LoRA** | 4 | **1.5 秒** | **8.1×** | 64 MB | ⚠️ 社群（`lightx2v`） |

想要官方出品就選 Turbo LoRA（8 步）；要极致速度就選社群 Lightning（4 步，只 64 MB）。
**兩者都要用 `LoraLoaderModelOnly` + `cfg 1` + `euler`/`simple`。**

4 步快速出圖（Lightning LoRA）✅ — 3.3 倍加速，品質還不輸**

![Lightning 4 步 LoRA 對比](/img/moss-vs-qwen-image/13_lightning_compare.jpg)

| 設定 | 耗時 | 品質 |
| --- | --- | --- |
| 官方 25 步 | 4.9 秒 | 正常 |
| **Lightning LoRA + 4 步** | **1.5 秒** | ✅ 細節豐富，不輸 25 步 |
| 只有 4 步（無 LoRA） | 1.2 秒 | ❌ **明顯糊掉** |

**LoRA 才是讓 4 步可行的關鍵** — 單純把 steps 砍到 4 不會有效果，
base 模型需要的是對應的蒸餾排程。LoRA 只有 **64 MB**。

### 6.2 Qwen KV cache

KV cache ⚠️ 可用，但 24GB 卡上沒有速度差異**

`QwenImage21Cache` 有 `device`（auto/gpu/cpu/off）與 `dtype`（default/int8/int4），
官方說 `off` 會「每步重算 prefix，是排除 cache 影響的方法」。
實測五種設定：**4.5～4.9 秒**，差異在雜訊範圍內。

節點 tooltip 寫的是「quantization **potentially speeds up edit workflows when memory starved**」
—— 這是**記憶體吃緊時的解法**，不是速度優化。
24GB 卡跑 1024² 單張參考圖本來就不缺記憶體，所以看不出來。
**在 24GB 卡上這個節點可以先不用管。**

KV cache 的真正條件 — 記憶體吃緊時快 25%**

| 情境 | `device=off` | `device=auto` | 差異 |
| --- | --- | --- | --- |
| 1024² + 1 張參考圖 | 4.5 秒 | 4.6 秒 | 無 |
| **2048² + 8 張參考圖** | **31.2 秒** | **23.3 秒** | **快 25%** |

節點 tooltip 說的「speeds up edit workflows **when memory starved**」完全準確。
批次做多參考圖編輯時記得開 `device=auto`；出一兩張小圖可以先不管。

> **一句話：**
> **Qwen-Image 2.1 是「什麼都能做、而且快」的成熟產品；**
> **MOSS-Image 5B 是「小、便宜、而且能精準控制版面」的基底模型。**
>
> 文字渲染實測幾乎打平，真正的分野在功能邊界：
> Qwen 有編輯、多圖參考、PE 改寫與官方加速 LoRA，
> MOSS 有 layout、色／深控制與官方 LoRA 訓練生。

完整數據與重現方式見 repo 的 [COMPARISON.md](https://github.com/kalpakjian/moss-image-comfyui/blob/main/COMPARISON.md)，
一頁速查版在 [DECISION.md](https://github.com/kalpakjian/moss-image-comfyui/blob/main/DECISION.md)。

## 七、選用速查表

| 你的狀況 | 選 | 實測依據 |
| --- | --- | --- |
| 要**改**一張既有的圖（換物件、改局部） | **Qwen** | ✅ 實測可用（須用 `<image1>`） |
| 要**多張參考**（風格圖 + 主體圖） | **Qwen** | ✅ 實測可用，image_1 / image_2 同時餵入 |
| 要**透明背景 PNG** | **Qwen** | ⚠️ 有 alpha 通道但去背效果有限，乾淨去背仍需 rembg |
| 要**把文字放到指定位置** | **MOSS** | ✅ JSON Layout 實測 bbox 精準命中 |
| 要**按 3D 模型擺位**出圖 | **MOSS** | ✅ 色／深控制實測能鎖位置與姿態 |
| 要**練自己的 LoRA**（尤其真人） | **MOSS** | ✅ 官方第一方工具，6.20 GiB 實測可跑 |
| 顯卡 **< 24GB** | **MOSS** | 實測 15.4～23.1 GiB vs Qwen 23.0～23.2 GiB |
| 日常出圖、**量大** | **Qwen** | 快 1.6～3.0 倍；加官方 Turbo LoRA 再快 4.5 倍 |
| 要出**帶字的海報** | **Qwen + PE 改寫** | 實測差異最明顯（亂碼標題 → 正確標題） |
| 只是要一張**寫實照片 / 中文大標題** | **Qwen** | 實測畫質打平，選快的即可 |

> **一句話總結**
>
> **Qwen-Image 2.1 是「什麼都能做、而且快」的成熟產品；**
> **MOSS-Image 5B 是「小、便宜、而且能精準控制版面」的基底模型。**
>
> 文字渲染實測幾乎打平，真正的分野在功能邊界：
> Qwen 有編輯、多圖參考、PE 改寫與官方加速 LoRA；
> MOSS 有 layout、色／深控制與官方 LoRA 訓練生。

## 八、方法與限制

**方法**

- 同一台 **RTX 4090 24GB**、同一套 **ComfyUI 0.42.5**、同一個 seed（42）、同一組提示詞
- 每個模型都用**自己官方推薦的取樣參數**（MOSS 50 步/CFG 3/shift 5/SLG 22；
  Qwen 25 步/CFG 1/Euler+simple）
- 每次生成前呼叫 `/free` 卸載模型，避免 ComfyUI 節點快取造成假數據
- 耗時取伺服器端 `execution_start` → `execution_success` 的時間戳；
  VRAM 由背景執行緒輪詢 `nvidia-smi` 取峰值
- 對打總量：**18 次**（3 提示詞 × 2 模型 × 3 解析度）+ 11 次獨有能力／加速功能驗證

**限制**

- 只測了 SFT 版的 MOSS-Image（Base 版另有實測）
- 本機 Qwen-Image 2.1 的 text encoder 用 **bf16** 版（16.33 GiB），官方範本用 int8，VRAM 數字會更低
- 視覺比較是**主觀判讀**，非盲測或量化指標
- 未測 ControlNet / 角色一致性 / LoRA 品質
- Qwen 的完整版 Turbo 模型未實測（只測了 Turbo LoRA）
- MOSS 的 4 步 adapter 未實測（需自訂節點 + bf16 權重）
- MOSS 控制 adapter 是**社群作品**，且未搭配 region prompts 測試

**可重現資源**

- 完整數據與踩坑：[COMPARISON.md](https://github.com/kalpakjian/moss-image-comfyui/blob/main/COMPARISON.md)
- 一頁速查卡：[DECISION.md](https://github.com/kalpakjian/moss-image-comfyui/blob/main/DECISION.md)
- MOSS 安裝篇：[MOSS-Image 5B 安裝與實測](https://kalpakjian.github.io/2026/10/23/moss-image-5b-notes/)
