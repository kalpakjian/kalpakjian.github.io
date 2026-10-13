---
title: Popular LLM Models 學習筆記（IVDC Lesson 2）
date: 2026-10-13 13:20:00
tags:
  - LLM
  - Generative AI
  - RAG
  - IVDC
  - 學習筆記
categories:
  - AI
  - 學習筆記
cover: /img/covers/popular-llm-notes-ivdc.png
banner_img: /img/covers/popular-llm-notes-ivdc.png
index_img: /img/covers/popular-llm-notes-ivdc.png
archive: true
---

![Popular LLM Models 學習筆記](/img/covers/popular-llm-notes-ivdc.png)

IVDC「Certificate in Application of Large Language Model (LLM)」**Lesson 2 — Popular LLM Models** 的完整學習筆記。

這一課把「生成式 AI 家族」拆成三條主線：**有哪些產品**（Popular LLM）、**原理對照**（Predictive AI vs Generative AI）、以及**知識要放在哪裡**（LLM vs RAG）。原稿 77 頁，其中約 30 頁是純截圖，筆記逐頁補上可考的內容。

<!-- more -->

## 這份筆記有什麼

- **原稿 77 頁逐頁重寫**，33 個章節 + 7 個附錄，順序與原稿一致
- **四支 Lab 全部在本機實測**（Python 3.11.15／torch 2.14.1+cu132／transformers 5.17.0／RTX 4090），真實輸出直接寫進內文
- 九個對話式生成式 AI 逐一拆解：ChatGPT／Gemini／Copilot／Llama／Grok／Perplexity／Kimi／Tongyi／DeepSeek
- GAN 與 Diffusion 的訓練機制完整展開（含「判別器 50% 準確率才是收斂」這個反直覺考點）
- **33 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **60 題互動 MC 測驗**（點選即時計分、進度自動存 localStorage）

## 章節

| # | 章節 | PDF 頁 |
|---|------|--------|
| 1 | 課程地圖：這份教材的三條主線 | p2 |
| 2 | 什麼是生成式 AI | p3 |
| 3 | 熱門 LLM 總覽：六個對話式生成式 AI | p4–6 |
| 4 | ChatGPT：介面與用途 | p7–10 |
| 5 | ChatGPT 的智慧從哪來：RLHF、獎勵模型與 PPO | p11–13 |
| 6 | Gemini | p14 |
| 7 | ChatGPT Prompt 範例 | p15 |
| 8 | Copilot | p16 |
| 9 | Meta／Llama | p17 |
| 10 | Grok | p18 |
| 11 | Perplexity：AI 搜尋引擎 | p19 |
| 12 | 中國熱門 LLM：Kimi、通義、DeepSeek | p20–23 |
| 13 | 在本機使用 DeepSeek | p24 |
| 14 | 第三方多模型聚合 App | p25 |
| 15 | 生成式 AI 偵測器 | p26 |
| 16 | Predictive AI vs Generative AI：主題地圖 | p27 |
| 17 | Predictive AI 深入：資料、模型與應用 | p28 |
| 18 | Predictive AI 的五步流程 | p29 |
| 19 | Generative AI 深入：定義與核心技術 | p30–31 |
| 20 | Generative AI 的運作方式與生成流程 | p32–33 |
| 21 | 對照總表：Predictive AI vs Generative AI | p34 |
| 22 | AI → ML → DL → Generative AI 的層次，與 AIGC | p35–36 |
| 23 | GAN 基礎概念 | p37–40 |
| 24 | GAN 的底層技術與演算法 | p41–52 |
| 25 | Diffusion Model | p53–58 |
| 26 | GAN vs Diffusion，與其他生成模型 | p59–62 |
| 27 | Hybrid AI Systems | p63–65 |
| 28 | 真實世界應用：醫療、電商、招聘 | p66–68 |
| 29 | RAG：檢索增強生成與 AnythingLLM | p70–71 |
| 30 | LLM vs RAG：比較、強弱與使用時機 | p72–74 |
| 31 | 更多 ChatGPT：Hinton 的推理題 | p75 |
| 32 | 程式範例索引與本機實測總表 | p69, p76 |
| 33 | 考試重點整理 | 整理 |

另有 **7 個附錄**：名詞與架構速查表、常見錯誤與陷阱、教材頁面索引對照、離線執行／安裝提示、一頁精華（考前 10 分鐘）、60 題 MC 互動測驗、答錯題目 → 複習章節對照。

---

## 重點：60 題 MC 模擬試卷

**🖱️ [開始 60 題線上測驗](/popular-llm-notes/mc-quiz.html)**

- 60 題單選、滿分 60 分、建議 75 分鐘
- 分四個部分、依原稿頁碼順序排列
- 答案分佈刻意打散（A/B/C/D 各 15 題）
- 點選即時計分、進度存在 localStorage、可切換「只看未答／只看答錯」

> 出題率最高的考點包括：**GPT 三個字母的展開**、
> **RLHF 三階段（SFT → Reward Model → PPO）**、
> **AI ⊃ ML ⊃ DL ⊃ Generative AI**、
> **GAN 判別器降到 50% 才是收斂**、
> **Diffusion 只有 Reverse 需要訓練**、
> **RAG 不訓練任何模型權重**、
> **LLM 可離線／RAG 不可離線**，
> 以及**原稿 SD 的預設值 20 步 / guidance 7.5**。

---

## ⚠️ 本機實測抓到的兩個原稿缺陷

| 原稿寫法 | 實測結果 |
|---|---|
| `generator(prompt, max_length=50, ...)`（`RAG.ipynb`） | ❌ prompt 已 153 token → `ValueError`，要改 **`max_new_tokens=50`** |
| 「SD 生成 may take **30-60 seconds**」 | 本機 RTX 4090 只要 **0.61 秒**（原稿數字是 Colab T4 的體感） |

還有一個環境陷阱：本機 `torchaudio`（CUDA 13.0）與 `torch`（CUDA 13.2）版本不符，
會讓**所有** transformers 模型載不進來（連 `from transformers import pipeline` 都失敗）——
筆記附錄 B 有完整的根因鏈與三種解法。

---

## 本機實測的真實數字

| 項目 | 實測值 |
|---|---|
| `distilgpt2` 參數量 | **81.9 M** |
| 文字生成（temp 0.7） | **0.18 s** / 10 tokens |
| SD 1.5 U-Net 參數量 | **859.5 M** |
| SD 生成（512×512，20 步） | **0.61 s**（峰值 VRAM **5.13 GB**） |
| RAG 嵌入維度（distilbert-base） | **768** |
| RAG 檢索相似度 | **0.6573 / 0.7357**（檢索正確） |
| 房價預測 MAE / R² | **$11,227.31** / **1.00**（資料是線性公式生成的） |

---

## 離線也能用

筆記是**單一 HTML 檔、零外部資源**（CSS、語法高亮、33 張章節插圖全部內嵌），下載後直接雙擊就能看。

也可以下載原始 Markdown：

**📄 [Popular_LLM_Study_Notes.md](/popular-llm-notes/Popular_LLM_Study_Notes.md)**

---

## 建議使用順序

1. 先讀 §1–§3，把三大主線與九個產品記牢
2. 讀 §4–§5（ChatGPT 與 RLHF），這是原理題最集中的地方
3. §6–§15 用「誰做的／屬於哪一類」的方式快速掃過
4. 精讀 §16–§22（預測 vs 生成的原理對照）
5. 精讀 §23–§26（GAN 與 Diffusion 的訓練機制）
6. 讀 §29–§30（RAG 與 LLM vs RAG），並動手跑一次附錄 D 的最小 RAG
7. 找個安靜的 75 分鐘，完整做一次**附錄 F 的 60 題線上互動測驗**
8. 考前 10 分鐘只看**附錄 E 一頁精華**

祝考試順利。

---

*本篇為個人學習筆記整理，教材內容版權屬匯縱專業發展中心（IVDC）所有。*
