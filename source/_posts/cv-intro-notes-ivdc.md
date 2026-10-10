---
title: Introduction to Computer Vision 學習筆記：IVDC 課程完整複習 + 60 題 MC 模擬試卷
date: 2026-10-10 22:00:00
categories:
  - 學習資源
tags:
  - 電腦視覺
  - Computer Vision
  - CNN
  - IVDC
  - 學習筆記
  - 考試
index_img: /img/covers/cv-intro-notes-ivdc.png
banner_img: /img/covers/cv-intro-notes-ivdc.png
---

最近為了準備 IVDC（匯縱專業發展中心）「Certificate in Application of Computer Vision Technology」的考試，我把課程第二份教材《2 IVDC_Introduction to Computer Vision and Application.pptx》（12 頁）完整重寫成一份可離線閱讀的學習筆記，並額外做了一份 60 題的 MC 模擬試卷。

筆記已發佈成獨立專題頁面：

**👉 [Introduction to Computer Vision 學習筆記（考試溫習版）](/cv-intro-notes/)**

<!-- more -->

---

## 這份筆記包含什麼

按 PDF 原稿的每一個標題逐一填充，涵蓋全部 6 個主題：

| 章節 | 主題 |
|---|---|
| 1 | 商業領域的真實案例（Real Case Examples in Commercial Sectors） |
| 2 | 中國大陸與香港的最新 AI 技術（2024 世界機器人大會） |
| 3 | 卷積神經網路 CNN 是什麼（grid-like structure） |
| 4 | CNN 為何是頂尖方法（State-of-the-art / encoder / deep） |
| 5 | 關鍵概念：參數重用（re-use parameters，3×3 卷積在 5×5 影像） |
| 6 | CNN 基本概念與影像辨識（卷積／池化／全連接／Softmax） |

另外補了 8 個附錄：**名詞速查表**、**常見錯誤與陷阱**、**模擬試題**、**教材頁面索引對照**、**延伸資源與離線提示**、**一頁精華（考前 10 分鐘）**、**60 題 MC 模擬試卷**、**答錯題目 → 複習章節對照**。

---

## 重點：60 題 MC 模擬試卷

因為考試可能是選擇題形式，我特別做了一份**完整計時模擬試卷**（附錄 G）：

| 資源 | 連結 |
|---|---|
| 📝 60 題試卷（不附答案，先做再看） | [開始作答](/cv-intro-notes/#附錄-gmc-模擬試卷60-題) |
| ✅ 答案速查表（6×10 網格，方便自我評分） | [對答案](/cv-intro-notes/#g5-答案速查表) |
| 💡 逐題詳解（說明為何正確、其他選項錯在哪） | [看詳解](/cv-intro-notes/#g6-逐題詳解) |
| 🖱️ 互動測驗版（即時計分、進度自動儲存） | [前往測驗](/cv-intro-notes/mc-quiz.html) |

**試卷設計**

- 60 題單選、滿分 60 分、建議 75 分鐘
- 分三部分：電腦視覺與商業應用（1–20）、CNN 定義與架構（21–40）、卷積／參數重用與綜合（41–60）
- 答案分佈刻意打散（A/B/C/D 各 15 題），避免整排猜同一個字母
- 每題詳解都附「答錯題目 → 對應複習章節」對照，方便回頭補強

> 出題率最高的考點包括：CV 的六大商業應用分類（零售／安防／工業／醫療／自駕／農業）、ANPR ＝ **物件偵測 + OCR**、2024 世界機器人大會的**超現實圍棋博弈**、CNN 定義的兩個關鍵詞 **grid-like structure** 與 **hierarchical representations**、**「deep」＝ 許多逐漸變窄的 block 堆疊**、CNN 的核心思想 **參數重用（shares parameters）**、**5×5 影像經 3×3 卷積得 3×3**、以及 CNN 三大特性（**局部連接、參數共享、平移不變性**）。

---

## 原稿多為投影片，筆記補上了「圖背後的概念」

這份教材是 PowerPoint 匯出的 PDF，多頁只有示意圖（商業案例照片、CNN 架構圖、卷積示意圖）。
筆記除了忠實保留原稿文字，還補上每張圖背後的**定義、公式與考點**，讓沒有圖也能讀懂、能應試。

---

## 離線也能用

筆記是**單一 HTML 檔、零外部資源**（CSS 與語法高亮全部內嵌），下載後直接雙擊就能看，適合考前在沒有網路的環境複習。

也可以下載原始 Markdown：

**📄 [Introduction_to_CV_Study_Notes.md](/cv-intro-notes/Introduction_to_CV_Study_Notes.md)**

---

## 建議使用順序

1. 先讀完第 1–6 節，把附錄 A（名詞速查表）當工具書隨時查
2. 做附錄 C 的 36 題（隨讀隨測，每題下方有摺疊答案）
3. 找個安靜的 75 分鐘，完整做一次**附錄 G 的 60 題模擬試卷**（或用互動測驗版）
4. 考前 10 分鐘只看**附錄 F 一頁精華**

祝考試順利。

---

*本篇為個人學習筆記整理，教材內容版權屬匯縱專業發展中心（IVDC）所有。*
