---
title: MOSS-Image 5B 實測筆記：直出 4MP、6GB 訓練 LoRA（Windows / ComfyUI）
date: 2026-10-23 21:30:00
categories:
  - 技術筆記
tags:
  - 人工智慧
  - MOSS-Image
  - ComfyUI
  - LoRA
  - 影像生成
  - KohakuMossTrainer
  - 實作
index_img: /img/covers/moss-image-5b-notes.png
banner_img: /img/covers/moss-image-5b-notes.png
---

> **實測機器：** RTX 4090 24GB ｜ Windows 11 ｜ ComfyUI 0.42.5 ｜ torch 2.16.0.dev+cu132
> 從模型釋出到訓練出一顆能用的 LoRA，全部自己跑一遍的紀錄。


> **一句話總結：** MOSS-Image 是 2026-10 由 OpenMOSS 釋出的 5B 參數 DiT 基底模型，
> 中英文文字渲染與 Layout 控制都很強。實測在 24GB 卡上能**直出 4.19 MP（2048×2048，84 秒）**，
> 連官方外推上限之外的 6.55 MP 都跑得動；配合 KohakuMossTrainer 練 LoRA，
> **峰值 VRAM 只有 6.20 GiB**，跟官方講的「6GB 起步」完全吻合。

## 一、這次做了什麼

MOSS-Image 剛釋出沒幾天，ComfyUI 的原生支援更是 2026-10-16 才合併進去。
於是決定從零跑一遍完整流程，把每一個數字都自己驗證：

- 把 ComfyUI 從 **0.37.0 升到 0.42.5**（原生支援在 v0.42.0 起才內建）
- 下載 MOSS-Image 的 ComfyUI 格式權重（19.39 GiB）並跑通生成
- 驗證**直出 4MP 與 6MP** 是否真的可行
- 裝 KohakuMossTrainer，用 **6 GB 級 VRAM** 真的訓練一顆 LoRA 出來
- 把 LoRA 裝回 ComfyUI 驗證風格有沒有學進去
- 順手把本機既有的 **Qwen-Image 2.1** 拉出來對打，跑了 18 次逐張比較
- 過程中抓到一個會讓人publish出**假數字**的坑（ComfyUI 節點快取），順手更正了先前的數據

完整可重現的腳本與工作流程已開源：
[github.com/kalpakjian/moss-image-comfyui](https://github.com/kalpakjian/moss-image-comfyui)。

## 二、直出 4MP：官方說法 v.s. 實測

官方 USERGUIDE 的說法是：推薦輸出 **1M～2M 像素**，
模型**可以外推**到 0.25M（512×512）到 **4M（約 2K）**。
注意「外推」與「推薦」是兩件事，所以直接拿來實測：

| 解析度 | 像素量 | 實測耗時 | 說明 |
| --- | --- | --- | --- |
| 1024×1024 | 1.05 MP | 19.4 秒 | 官方推薦區間 |
| 2048×2048 | **4.19 MP** | **84.1 秒** | 官方外推上限（≈2K） |
| 2560×2560 | **6.55 MP** | **147.5 秒** | 超出官方外推上限，**實測仍可** |

取樣參數一律照官方推薦：**50 steps、CFG 3、shift 5、Euler + sgm_uniform**，
加上負向分支跳過 layer 22（`SkipLayerGuidanceDiTSimple`）。

![同構圖同鏡位、100% 裁切放大比較。1.05 MP 明顯較軟，4.19 MP 相框與燈罩細節清楚，6.55 MP 葉片與相框內的畫都銳利可辨。](/img/moss-image-5b-notes/01_resolution_compare.jpg)

同構圖、同鏡位、100% 裁切放大比較，差異很明顯：
1.05 MP 明顯偏軟，4.19 MP 的相框與燈罩細節已經清楚，
6.55 MP 連葉片脈絡與相框裡那幅畫都銳利可辨。
**而且三張都沒有出現手指或肢體變形**——這點對「擴張解析度就崩」的疑慮是個正面回應。

![MOSS-Image-SFT 在 2048×2048（4.19 MP）直出的原圖](/img/moss-image-5b-notes/04_sft_2048_sample.jpg)

上面這張是 2048×2048 直出的原圖（點擊可看原始尺寸）。

> **實務提醒：** 尺寸必須是 **16 的倍數**，否則 Python API 直接報錯。
> 另外 4MP 以上的耗時是線性成長的（像素量 4 倍 → 耗時約 28 倍），
> 4.19 MP 已經要一分半鐘了，日常出圖還是 1024～1536 最實用。

## 三、Base 與 SFT 到底差在哪

官方把 MOSS-Image 分成兩個版本，用途不同：

- **Base**：未經後訓練，完整保留訓練資訊 → 官方明講是**留給大家 train LoRA 用**的
- **SFT**：後訓練過 → 直接生成用的版本

同 seed、同提示詞實測，兩者差異一目了然：

![MOSS-Image-Base（上）與 MOSS-Image-SFT（下），同 seed 同提示詞。SFT 是構圖完整、光影成熟的成片；Base 明顯素樁得多。](/img/moss-image-5b-notes/02_base_vs_sft.jpg)

SFT 出來的是構圖完整、光影成熟的「成片」；
Base 明顯素樁得多，物件少、鋪陳隨意。
這正好對應官方定位——**Base 不是不好用，是留給你改的**。
所以「生成用 SFT、訓練用 Base」這個建議，是有實作依據的，不是口耳相傳。

## 四、6GB 訓練 LoRA：真的跑完了

這是整個流程裡最關鍵的一環。用
[KohakuMossTrainer](https://github.com/KohakuBlueleaf/KohakuMossTrainer)
（Windows 原生支援）從 Base 訓練一顆 LoHa adapter：

| 項目 | 實測值 |
| --- | --- |
| 環境 | Windows 11 / Python 3.12.13 / torch **2.14.1+cu130** |
| Kernel | triton-windows 3.8.0 + TileLang 0.1.15（自動調校，`missing: nothing`） |
| 演算法 | LyCORIS **LoHa** rank 8，252 modules |
| 步數 | 150 steps × 2 張圖/步 |
| 速度 | **5.0 秒/步**（首步 28.9 秒含 kernel 預熱） |
| **峰值 VRAM** | **6.20 GiB** allocated / 8.24 reserved / 裝置總用量 10.0 GiB |
| loss | step1 0.27 → step40 0.2203（最低）→ step150 0.2893 |
| 結果 | `ok=True, samples=300, nonfinite=0, skipped=0` |

> **官方說的「6 GB cards 可訓練」不是保守宣稱。**
> 本機實測峰值 6.20 GiB，數字完全對得上。

訓練資料是 16 張由 MOSS-Image 自己生成的「暖色午後光線居家工作室」風格圖
（每張配同名 `.txt` caption）。重點是 **LoRA 要學的是風格不是某一張圖**：
提示詞共享風格詞（光線、色調、質感），只在主體上變化（桌子、椅子、工作台⋯）。

訓練完的 adapter 丟進 `models\loras\`，重啟 ComfyUI 就出現在
`LoraLoader` 選單裡。用**沒在訓練資料裡**的提示詞驗證：

![左＝Base、右＝套上 KohakuMossTrainer 訓練的 LoRA。暖色午後光線的風格確實被學進去了。](/img/moss-image-5b-notes/03_lora_compare.jpg)

閣樓工坊從冷灰雜物變成溫暖琥珀色調；
工作室那組從冷灰白轉為溫暖黃綠、對比更柔。
**風格確實被學進去了。**

## 五、ComfyUI 版本判斷：這是最容易踩的坑
## 六、其他踩坑

### 訓練時務必關掉 ComfyUI
它會佔住約 11 GB VRAM，導致 LoHa kernel 自動調校階段連續 OOM。
關掉後 VRAM 從 18.8 GB 降到 7.2 GB，調校就正常了。

### 節點接法不可照搬 ModelSamplingSD3
官方明確警告：原生 MOSS-Image 模型的 timestep multiplier 與 SD3 不同。
要調 shift 請用 `ModelSamplingAuraFlow`（multiplier 1）。

```
UNETLoader
  └─ ModelSamplingAuraFlow(shift=5)
       └─ SkipLayerGuidanceDiTSimple(single_layers="22")
            └─ KSampler(Euler / sgm_uniform / CFG 3 / 50 steps)
```

### --steps 必須大於 warmup
`kohakumoss-config new train --steps 100` 會被設定檢查擋下：

```
SCHEDULE warmup=100 >= its end 100 (STEPS): the schedule never leaves warmup
```

用 `--steps 150` 即可。

### Windows 只有 spawn，step 1 會等
DataLoader worker 逐個重新 import 訓練器與 kernel 模組，
官方量測 4 workers 時 step 1 要等約 46 秒，之後每步約 5 秒。
**不是卡住，是正常的。**

### PowerShell 把 git 的正常輸出當錯誤
`git checkout` 會把 `Note: switching to ...` 寫到 stderr，
PowerShell 當成錯誤讓腳本提前中斷，看起來像「指令沒生效」。
用 `cmd /c` 包裝繞開。

### Windows 保留名稱 nul 會讓 git 卡住
`D:\AI\ComfyUI\nul` 這種檔名 git 刪不掉，
導致 `git stash push` 無法清理工作區，後續 checkout／cherry-pick 全部連鎖失敗。
用 `cmd /c "del \\?\D:\AI\ComfyUI\nul"` 解決。

### git add 整個目錄會把素材拖進 index
如果資料夾裡混了 45 GB 的影片／影格，`git add scripts/` 會全部納入暫存區，
暫存區與 .git 直接暴增數十 GB。用副檔名白名單精準挑檔。

### ComfyUI 的節點快取會讓耗時量測失真
ComfyUI 會依**節點輸入**做執行快取。若整條工作流程（模型、seed、prompt、steps…全部相同）
之前跑過，就會直接回傳上次的結果、不重新取樣。

實測踩到的坑：先跑了一份 smoke test（seed 42 / 1024×1024 / SFT），
之後批次測試又用**逐字相同**的工作流程檔（只差 `client_id`），
結果量到 **3.0 秒**——但同一份工作流程重新跑其實要 **19.4 秒**。

**怎麼避免：**量測前先呼叫 `/free` 讓模型卸載（重載模型會使快取失效），
或每次量測都換 seed。
驗證方式：把同一份 workflow 連跑兩次，第二次會異常地快 → 就是命中快取。
這也是本 repo 的對打腳本 `scripts/head_to_head.py` 每次生成前都呼叫 `/free` 的原因。

## 七、附帶實測：MOSS-Image vs Qwen-Image 2.1

Qwen-Image 2.1 是 2026-10-23 這天 ComfyUI 內建的另一個原生模型，本機剛好兩套都有，
於是直接用**同一台機器、同一個 seed、同一組提示詞**逐張對打，
共跑了 18 次（3 提示詞 × 2 模型 × 3 解析度）。

| 解析度 | 像素量 | MOSS-Image 5B | Qwen-Image 2.1 | 倍數 |
| --- | --- | --- | --- | --- |
| 1024×1024 | 1.05 MP | **19.4 秒** | **11.3～12.1 秒** | 1.6～1.7× |
| 2048×2048 | 4.19 MP | **80.9～85.6 秒** | **29.8～32.2 秒** | 2.6～2.7× |
| 2560×2560 | 6.55 MP | **152.4～162.1 秒** | **50.1～55.6 秒** | 2.8～3.0× |

![MOSS-Image 5B vs Qwen-Image 2.1 完整實測數據表](/img/moss-image-5b-notes/08_moss_vs_qwen_table.jpg)

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

### 文字渲染：兩個模型幾乎打平

![中文文字渲染海報對比：左 MOSS-Image 5B，右 Qwen-Image 2.1](/img/moss-image-5b-notes/05_moss_vs_qwen_cntext.jpg)

提示詞是「一張咖啡店宣傳海報，頂部有中文標題『城市漫遊』，下方有英文副標題『CITY WALK』」。

**兩個模型的主標題「城市漫遊」和副標題「CITY WALK」都渲染完美、筆畫正確。**
差別在版面風格：MOSS 排版層次豐富、插畫有配色材質，偏「成品海報」；
Qwen 留白大、線稿乾淨，偏「設計稿／簡報模板」。

> ⚠️ 但**兩個模型的小字都是亂碼**——MOSS 的頂部小字是 `PA AJOIDO`、
> Qwen 的底部中文小字是 `良祝益迎何泡` 這類無意義字。
> 「大字正確、小字崩掉」是兩者共同的弱點。

![英文招牌文字對比：左 MOSS-Image 5B，右 Qwen-Image 2.1](/img/moss-image-5b-notes/06_moss_vs_qwen_entext.jpg)

英文招牌同樣是平手：**兩個模型都把 "MOSS & BEAN" 渲染得完全正確**，連 `&` 符號都對。
MOSS 是藍調時刻＋暖色店光、資訊量較大；Qwen 是更深的夜色、氣氛更收斂。

![寫實室內場景對比：左 MOSS-Image 5B，右 Qwen-Image 2.1](/img/moss-image-5b-notes/07_moss_vs_qwen_photo.jpg)

寫實場景的風格差異是**系統性的**：MOSS 偏「敘事性構圖」（元素多、像有人住過），
Qwen 偏「乾淨商業視覺」（元素少、接近商品攝影）。

### 真正的分歧在功能邊界

| 能力 | MOSS-Image 5B | Qwen-Image 2.1 |
| --- | --- | --- |
| 中英文大標題渲染 | ✅ 實測完美 | ✅ 實測完美 |
| 密集小字 | ❌ 亂碼 | ❌ 亂碼 |
| **JSON Layout 精準控制** | ✅ **獨有** | ❌ |
| **圖像編輯 / 局部編輯** | ❌ | ✅ **原生**（同一份權重） |
| **多圖參考** | ❌ | ✅ 最多 16 張 |
| **Alpha 透明背景** | ❌ | ⚠️ 有 4 通道但實測去背效果有限 |
| KV cache 加速 | ❌ | ✅ `QwenImage21Cache` |
| **LoRA 訓練** | ✅ **官方第一方支援**（6 GB 起步） | ✅ 社群支援 |
| 省 VRAM | ✅ | ❌（實測吃滿 23.2 GiB） |

### 三項獨有能力我也實測了

原本只有官方文件記載的能力，我把它們都跑了一遍，結果有兩點跟文件說的不完全一樣。

**MOSS 的 JSON Layout 精準控制 ✅** — 指定 bbox 後，文字與物件**精確落在指定位置**：

![MOSS-Image JSON Layout 實測：標題 EXPLORE 在上方、山峰插畫在下方中央](/img/moss-image-5b-notes/09_moss_layout.jpg)

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

**Qwen 的圖像編輯 ✅** — 保留原圖的房間、窗戶、陽光、植物、床，只換掉桌子：

![Qwen-Image 2.1 圖像編輯實測](/img/moss-image-5b-notes/10_qwen_edit.jpg)

> ⚠️ **指令必須用 `<image1>` 明確指涉參考圖。**
> 第一次測試沒寫 `<image1>`，模型直接把它當一般 t2i 重新生成了一張新圖（連房間都換了）。
> 加上 `<image1>` 之後才真的做到「只改指定部位、其餘保留」。

**Qwen 的多圖參考 ✅** — 同時餵兩張圖，融合它們的配色與紋理：

![Qwen-Image 2.1 多圖參考實測](/img/moss-image-5b-notes/11_qwen_multiref.jpg)

`TextEncodeQwenImage21` 的 `images` 用 dict 格式（最多 16 張）：

```json
"images": {"image_1": ["4", 0], "image_2": ["5", 0]}
```

**Qwen 的 Alpha 通道 ⚠️ 有，但別被「支援 alpha」四個字誤導**：

| 測試 | 輸出模式 | 完全透明 | 半透明 | 完全不透明 |
| --- | --- | --- | --- | --- |
| 一般 t2i（prompt 寫 transparent background） | **RGBA** | 0.0% | 1.3% | 98.7% |
| 官方去背做法（編輯 +「output a PNG image」） | **RGBA** | 0.0% | 6.7% | 93.3% |

VAE 確實解出 4 通道（輸出檔是 RGBA），但**一般 t2i 不會給你透明背景**，
只是多了一個幾乎全滿的 alpha 通道。官方 `background_removal` 範本的做法是
「編輯 + 指示輸出 PNG」，透明背景是**模型生成進 alpha 通道**、不是事後抠图；
實測背景乾淨時有改善，但**沒有到完全透明**、主體邊緣也不是乾淨 alpha。
**真的要乾淨去背，rembg 這類傳統工具仍然更可靠。**

### 再補三項加速／增強功能，都實測了

官方文件還提了三個「加速／增強」功能，我一併實測，**結論跟直覺差異不小**。

**① Prompt 自動改寫（Prompt Enhancer）✅ — 對文字渲染幫助最大**

輸入只有六個字 `a cafe poster`，PE 模型會改寫成一份完整的結構化海報概念書
（配色、邊框、主標題字樣、插畫描述都寫好），再餵給影像模型：

![Prompt 自動改寫對比](/img/moss-image-5b-notes/12_pe_compare.jpg)

| | 標題 | 畫面 |
| --- | --- | --- |
| 原始 prompt 直接生成 | `BIRON H TREE`（亂碼） | 構圖雜亂 |
| **PE 改寫後** | `GOOD COFFEE, Good Day`（正確） | 專業海報，含插畫與菜單板 |
| PE thinking 模式 | `BREWED Goodness` + `COZY CUPS COFFEE · PASTRIES · GOOD VIBES` | 更精緻 |

**為什麼值得特別提**：PE 把「想渲染的文案」明確寫進 prompt，模型就不會自己亂猜要寫什麼字。
**要出帶字的海報，PE 是最快的改善手段** — 比換模型有效得多。
實測 18.8～22.0 秒（含 PE 模型載入與改寫），PE text encoder 本身要 **8.82 GiB**。

**② 4 步快速出圖（Lightning LoRA）✅ — 3.3 倍加速，品質還不輸**

![Lightning 4 步 LoRA 對比](/img/moss-image-5b-notes/13_lightning_compare.jpg)

| 設定 | 耗時 | 品質 |
| --- | --- | --- |
| 官方 25 步 | 4.9 秒 | 正常 |
| **Lightning LoRA + 4 步** | **1.5 秒** | ✅ 細節豐富，不輸 25 步 |
| 只有 4 步（無 LoRA） | 1.2 秒 | ❌ **明顯糊掉** |

**LoRA 才是讓 4 步可行的關鍵** — 單純把 steps 砍到 4 不會有效果，
base 模型需要的是對應的蒸餾排程。LoRA 只有 **64 MB**。

**③ KV cache ⚠️ 可用，但 24GB 卡上沒有速度差異**

`QwenImage21Cache` 有 `device`（auto/gpu/cpu/off）與 `dtype`（default/int8/int4），
官方說 `off` 會「每步重算 prefix，是排除 cache 影響的方法」。
實測五種設定：**4.5～4.9 秒**，差異在雜訊範圍內。

節點 tooltip 寫的是「quantization **potentially speeds up edit workflows when memory starved**」
—— 這是**記憶體吃緊時的解法**，不是速度優化。
24GB 卡跑 1024² 單張參考圖本來就不缺記憶體，所以看不出來。
**在 24GB 卡上這個節點可以先不用管。**

> **一句話：**
> **Qwen-Image 2.1 是「什麼都能做、而且快」的成熟產品；**
> **MOSS-Image 5B 是「小、便宜、而且能精準控制版面」的基底模型。**
>
> 文字渲染實測幾乎打平，真正的分野在功能邊界：
> Qwen 有編輯、多圖參考與 PE 改寫，MOSS 有 layout 與官方 LoRA 生態。

完整數據與重現方式見 repo 的 [COMPARISON.md](https://github.com/kalpakjian/moss-image-comfyui/blob/main/COMPARISON.md)，
一頁速查版在 [DECISION.md](https://github.com/kalpakjian/moss-image-comfyui/blob/main/DECISION.md)。

## 八、把權重吃進 VRAM 的實際數字

| 檔案 | 大小 | 用途 |
| --- | --- | --- |
| `moss_image_sft_int8_convrot` | 5.04 GiB | 生成用 DiT |
| `moss_image_base_int8_convrot` | 5.04 GiB | 訓練用 DiT |
| `qwen3.5_9b_int8_convrot` | 9.08 GiB | 文字編碼器 |
| `flux2-vae_small` | 0.23 GiB | VAE |

選 **int8_convrot** 而不是 bf16，是因為它對應 ComfyUI 的
`comfy_kitchen` CUDA backend（sm89+）：int8 的 DiT 只要 5.04 GiB，
bf16 要 9.46 GiB，在 24GB 卡上差距很大（文字編碼器還要 9.08 GiB）。
共 19.39 GiB，實測 401 秒下載完畢。

## 九、接下來

這次練的 LoRA 是**泛用風格**，不是人物 LoRA。
你真正想做的應該是「用自己的照片練一顆人物 LoRA」——
流程完全一樣，把照片放進資料集、配好 caption、跑同樣的指令就好。

但有兩點要提醒：

- 人物 LoRA 會學到你的臉，**權重別隨意外傳**
- LoRA 的泛化能力取決於資料集的多樣性，16 張同風格圖適合學風格，
  學人像建議 30～50 張不同角度、光線、表情的照片

> **可重現資源：**
> [github.com/kalpakjian/moss-image-comfyui](https://github.com/kalpakjian/moss-image-comfyui)
>
> 內含工作流程產生器、LoRA 訓練全流程、三種對比圖工具，以及完整踩坑紀錄。
> 另附一顆以合成資料訓練的示範 LoRA（Release v1.0）供驗證環境用。


MOSS-Image 的 README 到今天（10/23）還寫著「v0.41.3 尚未包含此支援」，
但那是 **10/19 的寫作時點**。實際情況：

| 版本 | 是否含 MOSS-Image 原生支援 |
| --- | --- |
| v0.41.3 | ❌ |
| **v0.42.0 起** | ✅ 正式版已內建 |
| v0.42.5（當時最新） | ✅ |

用 git 祖先關係驗證最準：

```
git -C <ComfyUI> fetch upstream master --tags
foreach ($t in @('v0.41.3','v0.42.0','v0.42.5')) {
  git -C <ComfyUI> merge-base --is-ancestor e087d8f6 $t
  "$t : $(if($LASTEXITCODE -eq 0){'HAS MOSS'}else{'no'})"
}
```

> **不要停在 v0.42.0。** v0.42.1 的 release notes 是
> 「Fix some crashing issues a few users experienced when running the MOSS image template workflow」
> ——原生支援剛併入時 MOSS 範本會 crash，v0.42.1 才修好。
