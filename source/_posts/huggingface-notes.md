---
title: Hugging Face for LLM 學習筆記（Lesson 6）
date: 2026-10-13 15:40:00
tags:
  - LLM
  - Hugging Face
  - Transformers
  - Tokenizer
  - PEFT
  - LoRA
  - QLoRA
  - 學習筆記
  - Python
categories:
  - AI
  - 學習筆記
cover: /img/covers/huggingface-notes.png
banner_img: /img/covers/huggingface-notes.png
index_img: /img/covers/huggingface-notes.png
archive: true
---

![Hugging Face for LLM 學習筆記](/img/covers/huggingface-notes.png)

「Certificate in Application of Large Language Model (LLM)」**Lesson 6 — Hugging Face for LLM** 的完整學習筆記。

這一課的主題是：**「模型從哪裡來、怎麼用、怎麼改、怎麼放上線」**。Hugging Face 不訓練最強的大模型，但它幾乎是所有開源模型流通的必經之路——Llama、Mistral、Qwen、Gemma 發布時第一個落地的倉庫都在這裡。

<!-- more -->

## 這份筆記有什麼

- **逐節重寫**。
- **生態系三層架構**（全課骨架）：**① Hub → ② Core ML Libraries → ③ Inference & Deployment**
- **Hub 四件套**：Model Hub（300k+）／Dataset Hub／**Spaces**／文件與版控
- **三種 Tokenizer 深入對比**（課程用 **10 頁**講這個，考題最密集）：
  - **WordPiece**：`##` 標記、**最大似然**合併、BERT 系、**需要空白前處理**
  - **BPE**：byte-level、**貪婪**合併最頻繁對、GPT 系、**永不出現 `<unk>`**
  - **SentencePiece**：`▁` 標記、BPE 或 **Unigram**、T5／LLaMA、**不需空白前處理**
- **微調技術**：**PEFT = LoRA／QLoRA／Adapters**
  - LoRA 公式 **`W' = W + A × B`**，凍結 `W` 只訓練 `A`、`B`
  - QLoRA = LoRA ＋ **4-bit（NF4 ＋ double quantization）**，adapter 仍維持 16-bit
  - **Adapter 是概念，LoRA／QLoRA 是它的實作**
- **部署工具鏈**：Accelerate／Optimum／**TGI**／**Inference Endpoints**／**Safetensors**／`huggingface_hub`／Model Cards
- **三個 Lab 逐格拆解**：`HF_transformer.ipynb`（11 格）、`HF_LLM.ipynb`、`HF_dataset.ipynb`
- **43 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **60 題互動 MC 測驗**（點選即時計分、進度自動存 localStorage）
- **所有程式碼與數字都在本機實測**（Python 3.11.15／transformers 5.17.0／datasets 5.0.0／peft 0.19.1／RTX 4090 24 GB），實測輸出直接寫進內文

## 章節

| # | 章節 |
|---|------|
| 1 | 課程地圖：Lesson 6 在教什麼 |
| 2 | 前置知識：Transformer 與「三種輸入」的世界 |
| 3 | 為什麼需要 Hugging Face |
| 4 | What is Hugging Face? |
| 5 | Ecosystem Overview：三層架構 |
| 6 | Hugging Face Hub |
| 7 | Model Hub |
| 8 | Dataset Hub |
| 9 | Spaces：免費的 Demo 託管 |
| 10 | Transformers Library |
| 11 | Transformers 的實際介面 |
| 12 | Datasets Library |
| 13 | Streaming Access：不落地就能讀 |
| 14 | Automatic Caching |
| 15 | Built-in Preprocessing：`map()`／`filter()`／`shuffle()` |
| 16 | Tokenizers：Rust 實作的四種分詞器 |
| 17 | WordPiece（BERT 系） |
| 18 | BPE（GPT 系） |
| 19 | SentencePiece（T5／LLaMA） |
| 20 | 四種 Tokenizer 對照總表與選用 |
| 21 | Diffusers |
| 22 | PEFT |
| 23 | LoRA |
| 24 | QLoRA |
| 25 | Adapters |
| 26 | Accelerate |
| 27 | Optimum |
| 28 | Text Generation Inference（TGI） |
| 29 | Inference Endpoints |
| 30 | Safetensors |
| 31 | `huggingface_hub` SDK |
| 32 | Model Cards |
| 33 | Use Cases |
| 34 | Summary |
| 35 | Hands-On：三個 Lab 總覽 |
| 36 | `HF_transformer.ipynb` 逐格拆解 |
| 37 | ⚠️ `HF_transformer.ipynb` 的三個缺陷 |
| 38 | `HF_LLM.ipynb` 逐格拆解 |
| 39 | ⚠️ `HF_LLM.ipynb` 的兩個缺陷 |
| 40 | `HF_dataset.ipynb` 逐格拆解 |
| 41 | ⚠️ `HF_dataset.ipynb`：教 Streaming 卻不用 Streaming |
| 42 | 本機實測總表（真實數據） |
| 43 | 考試重點整理 |

另有 **7 個附錄**：指令與 API 速查表、常見錯誤與陷阱、離線執行／安裝提示、一頁精華（考前 10 分鐘）、60 題 MC 互動測驗、答錯題目 → 複習章節

---

## 重點：60 題 MC 模擬試卷

**🖱️ [開始 60 題線上測驗](/huggingface-notes/mc-quiz.html)**

- 60 題單選、滿分 60 分、建議 75 分鐘
- 分五個部分各 12 題：生態系／Transformers 與 Datasets／**三種 Tokenizer**／**PEFT 與微調**／部署與 Lab
- 答案分佈刻意打散（A/B/C/D 各 15 題）
- 點選即時計分、進度存 localStorage、可切換「只看未答／只看答錯」

> 出題率最高的考點包括：**`##` = WordPiece、`▁` = SentencePiece、byte-level = BPE**、
> **BPE 是貪婪合併、WordPiece 是最大似然合併**、
> **SentencePiece 不需空白前處理**、
> **LoRA 公式 `W' = W + A × B`**、
> **QLoRA 全名是 Quantized Low-Rank Adaptation（不是 Low Rank）**、
> **LoRA 讓「總」參數變多但「可訓練」參數暴減**、
> **`safetensors` 屬於第 ③ 層（不是第 ② 層）**，
> 以及**串流回傳 `IterableDataset`、不能用 `len()` 或索引**。

---


## ⚠️ 這份筆記最有價值的部分：14 個實作陷阱

| 位置 | 缺陷 |
|---|---|
| **章節標題** | **`Adaptors`**（應為 `Adapters`），且同頁內文寫 `An Adapter is…`——標題與內文自己不一致 |
| **章節標題** | **`QLoRA (Low Rank Adaptation)`**——直接複製 LoRA 的展開；正確是 **Quantized** Low-Rank Adaptation |
| **ALBERT 那兩處** | **ALBERT 同時被列在 WordPiece 與 SentencePiece 底下**，兩頁互相矛盾（實際上用的是 SentencePiece） |
| **這兩頁** | `Text Generation Inference` 出現 **`• •` 空項目符號** |
| **這兩頁** | 標題寫 `Huggingface_hub SDK`（實際套件名是全小寫 `huggingface_hub`） |
| **`HF_LLM.ipynb`** | **`target_modules=["c_attn"]` 只對 GPT-2 有效**——換成 Llama／Qwen 直接 **`ValueError`** |
| **`HF_LLM.ipynb`** | **只數參數、完全沒有 forward／backward**，卻把「套上 LoRA」當成「微調完成」 |
| **`HF_transformer.ipynb`** | 註解說 `Google's DeiT model`，**程式實際載入 ViT** |
| **`HF_transformer.ipynb`** | **熱連結新聞站 CDN 的裁切圖**（862×485），預測明顯失敗（**12.9%**）卻**不加任何說明** |
| **`HF_transformer.ipynb`** | markdown 說用 `facebook/wav2vec2-base-960h`，**程式用的是 AST**；且把分類輸出說成「Text tokens」 |
| **`HF_dataset.ipynb`** | **Tiny ImageNet 已按類別排序**，「找魚」迴圈其實只跑了 3 次就 break |
| **`LoRA.txt`** | `matrices` 拼成 **`matrics`**（與 Lesson 7 §32 是同一個檔案、同一個錯字） |

### 三個最嚴重的缺陷

#### ① `target_modules=["c_attn"]` 不可攜

`c_attn` 是 **GPT-2 專屬**的模組名（`Conv1D` 型別）。本機實測套在 **Llama 架構**上：

```
ValueError: Target modules {'c_attn'} not found in the base model.
```

| 寫法 | 可訓練參數 | trainable% | Llama 上能跑嗎 |
|---|---|---|---|
| `["c_attn"]` | 147,456 | 0.1797% | ❌ |
| **`"all-linear"`（建議）** | 589,824 | 0.7149% | ✅ |

#### ② `peft` 因為 `torchaudio` 而完全無法匯入

錯誤訊息是 `ModuleNotFoundError: Could not import module 'BloomPreTrainedModel'`——**完全誤導**。
完整根因鏈：

```
torch 2.14.1+cu132  vs  torchaudio 2.11.0+cu130    ← CUDA 13.2 vs 13.0
   ↓ torchaudio/_extension/utils.py  _check_cuda_version() → RuntimeError
transformers/audio_utils.py:58   if is_torchaudio_available(): import torchaudio
   ↓ 拖垮 transformers 的 lazy-import（BloomPreTrainedModel）
peft/utils/constants.py:16   from transformers import BloomPreTrainedModel
   ↓
peft 完全無法匯入 —— 即使你根本不用音訊
```

**關鍵**：`is_torchaudio_available()` 檢查的是「套件有沒有**安裝**」（metadata），
**不是「能不能 import 成功」**。所以「裝了但壞掉」最致命。

**解法**：`pip uninstall -y torchaudio` → `peft` **立刻恢復**（實測 `0.19.1`）。

> ⚠️ **補充查證**：**torchaudio 沒有 2.14.1，也沒有任何 cu132 建置**——
> `pip index versions torchaudio` 最新只到 **2.11.0**，而 `download.pytorch.org/whl/cu132/torchaudio/`
> 最高只到 **2.2.0**。也就是說 **torch 與 torchaudio 的版本號已經脫鉤**：
> `torch` 走到 2.14.1（有 cu132），`torchaudio` 停在 2.11.0（CUDA 建置最高只到 13.0）。
>
> 所以 `torch 2.14.1+cu132` 配 `torchaudio 2.11.0+cu130` **不是「裝錯」，而是「只能這樣裝」**。
> 想兩邊都對，唯一的路是把 **torch 降回 `2.14.1+cu130`**（torch 確實有 cu130 建置）。

#### ③ 課程用兩頁教 Streaming，三個 Lab 一次都沒用

| 做法 | 取得第 1 筆 | 再取 200 筆 | 快取增量 |
|---|---|---|---|
| 完整下載（舊寫法） | **12.58 秒** | — | **+235 MB** |
| **串流 `streaming=True`** | 6.162 秒 | **0.002 秒** | **0 MB** |

而且**串流回傳的是 `IterableDataset`**——不能用 `len()`、不能索引、不能用 `select()`。

---

## ⚠️ 過時資訊更正（2026-10 實查）

除了課程本身的問題，其他網路教學裡還有一批**已過時的資訊**。我把每一項都查證後更正：

| # | 原本寫的 | **實查結果** | 位置 |
|---|---|---|---|
| 1 | Model Hub「**300k+ models**」 | **`2M+` models**（約 **6.7 倍**）；Datasets 也已是 **`500k+`** | §7.4 |
| 2 | `hf cache scan` | ❌ **這個子指令不存在**；正確是 **`hf cache list`**（`prune`／`rm`／`verify`） | §31.3 |
| 3 | `hf` 只有 4 個子指令 | 實際 **25+ 個**（`models`／`datasets`／`spaces`／`endpoints`／`jobs`／`repos`／`collections`／`webhooks`／`buckets`／`sync`／`cp`…） | §31.3 |
| 4 | `huggingface_hub` 1.24.0（暗示最新） | **最新已是 2.2.0**（跨大版本）；`hf` 自己會提示要更新 | §31.4 |
| 5 | `transformers` 5.17.0 | 最新 **5.19.0** | §42.1 |
| 6 | `datasets` 5.0.0 | 最新 **5.1.0** | §42.1 |
| 7 | `peft` 0.19.1 | 最新 **0.21.2** | §42.1 |
| 8 | `torchaudio` 有 cu132 版 | ❌ **沒有**——最高只到 **2.11.0+cu130** | §39.2 |

### 最重要的兩項

**① Model Hub 的模型數差了近一個數量級**

```
課程（撰寫時）  : 300k+ models
2026-10 實查       : 2M+ models      ← 約 6.7 倍
                    500k+ datasets
```

> **考試怎麼答？** 題目問「課程說有多少模型」→ **答 300k+**（考的是課程）。
> 但你要知道**實際已經超過 200 萬**。

**② `hf cache scan` 是錯的指令**

`hf cache` 的實際子指令只有四個：**`list`（別名 `ls`）／`prune`／`rm`／`verify`**。
網路上常看到的 `hf cache scan` **不存在**。

```bash
hf cache list       # ✅ 列出快取
hf cache scan       # ❌ 沒有這個子指令
```

### 版本對照（本機實測 vs 最新）

| 套件 | 本機實測 | 最新 | 落後 |
|---|---|---|---|
| torch | 2.14.1+cu132 | 2.14.1 | ✅ |
| transformers | 5.17.0 | 5.19.0 | ⚠️ |
| datasets | 5.0.0 | 5.1.0 | ⚠️ |
| peft | 0.19.1 | 0.21.2 | ⚠️ |
| safetensors | 0.8.0 | 0.8.0 | ✅ |
| **huggingface_hub** | **1.24.0** | **2.2.0** | ❌ **跨大版本** |

> 💡 **本筆記的實測數字是「可重現」的，不是「最新」的。**
> 要完全重現，請鎖定「本機實測」欄的版號（附錄 C 有完整的 `pip install` 指令）。

---

## 本機實測的真實數字

| 項目 | 實測值 |
|---|---|
| LoRA（distilgpt2, r=8）trainable | **147,456** |
| LoRA all params | **82,060,032** |
| **trainable%** | **0.1797%** |
| 總參數變化 | **+147,456（變多！）** |
| forward ＋ backward | **0.035 秒** |
| `google/vit-base-patch16-224` 載入 | **16.0 秒** |
| ViT 模型類別 | **`ViTForImageClassification`**（不是 DeiT） |
| 裁切圖的預測 | **`book jacket 12.9%`**（失敗） |
| AST 音訊分類 | **`Ding 55.9%`**（與課程 56% 一致） |
| wav2vec2 ASR 對同一段正弦 | **`{'text': ''}`**（空字串） |
| AG News | **120,000 筆、4 類** |
| Tiny ImageNet（clean） | **98,179 筆** |
| 快取增量 | **1.9 MB → 237.0 MB** |

> ✅ **三個 Lab 的技術內容全部可複現**——數字在本機一字不差。

---

## 離線也能用

筆記是**單一 HTML 檔、零外部資源**（CSS、語法高亮、公式 SVG、43 張章節插圖全部內嵌），下載後直接雙擊就能看。

也可以下載原始 Markdown：

**📄 [HuggingFace_Study_Notes.md](/huggingface-notes/HuggingFace_Study_Notes.md)**

---

## 建議使用順序

1. 先讀 §1–§5（定位與三層架構），建立整體座標
2. 讀 §6–§11（Hub 與 Transformers Library）
3. 讀 §12–§15（Datasets：Streaming／Caching／Preprocessing）——**這三節課程講了但 Lab 沒做**
4. **重點複習 §16–§20（三種 Tokenizer）**，這是考題最密集的區域
5. 讀 §21–§25（Diffusers、PEFT、LoRA、QLoRA、Adapters）
6. 讀 §26–§34（部署工具鏈與收尾）
7. 進 Lab：§36–§41，**邊讀邊對照缺陷**
8. 找個安靜的 75 分鐘，完整做一次**附錄 E 的 60 題線上互動測驗**
9. 考前 10 分鐘只看**附錄 D 一頁精華**

祝考試順利。

---

*本篇為個人學習筆記整理。*

