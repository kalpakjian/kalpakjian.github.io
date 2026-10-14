---
title: Introduction to LLM 學習筆記：IVDC Lesson 3 完整複習 + 60 題 MC 模擬試卷
archive: true   # 已歸入「專題：IVDC LLM課程」，不列在首頁
date: 2026-10-13 09:10:00
categories:
  - 學習資源
tags:
  - 人工智慧
  - LLM
  - Transformer
  - GPT
  - BERT
  - Tokenizer
  - Embedding
  - IVDC
  - 學習筆記
  - 考試
index_img: /img/covers/llm-intro-notes-ivdc.png
banner_img: /img/covers/llm-intro-notes-ivdc.png
---

為了準備 IVDC（匯縱專業發展中心）「Certificate in Application of Large Language Model (LLM)」的考試，我把課程第三份課程《3 IVDC_Introduction to LLM (adjusted).pdf》（**47 頁**）完整重寫成一份可離線閱讀的學習筆記，並額外做了一份 60 題的 MC 模擬試卷。

筆記已發佈成獨立專題頁面：

**👉 [Introduction to LLM 學習筆記（考試溫習版）](/llm-intro-notes/)**

<!-- more -->

---

## 這一份的難度比前幾份高：課程有 21 頁「沒有文字」

打開 PDF 只看得到圖或程式碼截圖。

如果只靠 PDF 的文字抽取，**會漏掉將近一半的課程**。所以這份筆記做了兩件額外的事：

1. **把關鍵圖重畫成 12 張內嵌 SVG**（預訓練／微調流程、Transformer 架構、self-attention 權重、
   BERT vs GPT、GPT-3 規模、自迴歸迴圈、滑動視窗、DataLoader 的 x/y、embedding 查表、輸入管線…）
2. **把後半的程式碼在本機實測**（PyTorch 2.14.1+cu132、tiktoken GPT-2），把真實輸出貼進筆記

---

## 這份筆記包含什麼

按 的每一個標題逐一填充，共 **30 個章節**：

| 章節 | 主題 |
|---|---|
| §1–§4 | LLM 的定義與「Large」的兩層意義、與早期 NLP 的差別、應用、客製化 LLM（BloombergGPT） |
| §5–§6 | 預訓練 vs 微調、指令微調 vs 分類微調 |
| §7–§9 | Transformer 的 encoder／decoder、self-attention、BERT vs GPT（含 zero-shot／few-shot） |
| §10–§16 | GPT 訓練資料集、token、預訓練成本（$4.6M）、自迴歸、GPT-3（96 層 / 175 B） |
| §17–§19 | 生成過程、Building an LLM、word embedding |
| §20–§24 | **實作**：分詞正則、vocabulary 與 token ID、SimpleTokenizer V1/V2、特殊 token、文件邊界 |
| §25–§30 | **實作**：滑動視窗、DataLoader、stride、embedding 查表、位置編碼、完整輸入管線 |

另外補了 7 個附錄：**名詞與架構速查表**、**常見錯誤與陷阱**、**課程頁面索引對照**、**離線執行／安裝提示**、**一頁精華（考前 10 分鐘）**、**60 題 MC 互動測驗**、**答錯題目 → 複習章節對照**。

---

## 重點：60 題 MC 模擬試卷

**🖱️ [開始 60 題線上測驗](/llm-intro-notes/mc-quiz.html)**

- 60 題單選、滿分 60 分、建議 50 分鐘
- 分四個部分、依課程章節順序排列
- 答案分佈刻意打散（A/B/C/D 各 15 題）
- 點選即時計分、進度存在 localStorage、可切換「只看未答／只看答錯」

> 出題率最高的考點包括：**「Large」同時指參數量與資料量**、
> **早期 NLP 是「特定任務」vs LLM 是「廣泛通用」**、
> **指令微調 = instruction＋answer、分類微調 = text＋class label**、
> **BERT = encoder + masked word prediction**、**GPT = decoder + 生成**、
> **Twitter 用 BERT 偵測 toxic content**、
> **zero-shot = 完全不給範例／few-shot = 最少量範例**、
> **GPT-3 預訓練成本 $4.6 million（cloud computing credits）**、
> **原始 transformer 6 層 vs GPT-3 96 層 / 175 B**、
> **`<|endoftext|>` = 文件邊界、`<|unk|>` = 未知詞**、
> **embedding 是查表（token ID 5 → 第 6 列，0-based）**、
> **positional embedding 是「加」上去且維度必須相同**，
> 以及**輸入管線五步驟的順序**。

---

## 後半的程式碼我全部跑過一遍

後半段是「動手建 LLM 的輸入管線」，全部都是程式碼截圖。我把每一段都實作並實測：

| 主題 | 本機實測結果 |
|---|---|
| 分詞（`re.split`） | `"Hello, world. Is this-- a test?"` → **10 個 token** |
| 建 vocabulary | `sorted(set(tokens))` → **size 15**，`"The cat sat"` → `[2, 4, 11]` |
| SimpleTokenizerV1 | 遇 OOV 直接 **KeyError: 'Hello'**（這就是 V2 要解決的問題） |
| SimpleTokenizerV2 | 加兩個特殊 token → size **15 → 17**；`<|endoftext|>`=15、`<|unk|>`=16 |
| 滑動視窗 | `max_length=4, stride=1` → **2 個樣本**；x=[2,4,11,9]、y=[4,11,9,13] |
| DataLoader | batch x/y 形狀皆為 **(2,4)** |
| Embedding | token ID 5 的向量 **等於權重矩陣第 6 列**（`True`） |
| 位置編碼 | 同一 token 在不同位置 → token embedding 相同、**加上位置編碼後就不同** |
| GPT-2 分詞器 | `"Hello, world!"` → `[15496, 11, 995, 0]`（**4 個 token**，符合「單詞數＋標點數」） |

---

## 離線也能用

筆記是**單一 HTML 檔、零外部資源**（CSS、語法高亮、SVG 圖表、章節插圖全部內嵌），下載後直接雙擊就能看，適合考前在沒有網路的環境複習。

也可以下載原始 Markdown：

**📄 [Introduction_to_LLM_Study_Notes.md](/llm-intro-notes/Introduction_to_LLM_Study_Notes.md)**

---

## 建議使用順序

1. 先讀完 §1–§18（觀念），把附錄 A（名詞與架構速查表）當工具書隨時查
2. 再讀 §19–§30（實作），並**自己跑一次**附錄 C 的程式碼
3. 優先背熟：**§9 BERT vs GPT 對照表**、**§16 的兩個數字**、**§30 的五步驟順序**
4. 找個安靜的 50 分鐘，完整做一次**附錄 E 的 60 題線上互動測驗**
5. 考前 10 分鐘只看**附錄 D 一頁精華**

祝考試順利。

---

*本篇為個人學習筆記整理。*
