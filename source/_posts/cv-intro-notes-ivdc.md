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

另外補了 7 個附錄：**名詞速查表**、**常見錯誤與陷阱**、**教材頁面索引對照**、**延伸資源與離線提示**、**一頁精華（考前 10 分鐘）**、**60 題 MC 互動測驗**、**答錯題目 → 複習章節對照**。

---

## 重點：60 題 MC 模擬試卷

因為考試可能是選擇題形式，我特別做了一份**完整計時模擬試卷**（附錄 F，**互動網頁版**）：

**🖱️ [開始 60 題線上測驗](/cv-intro-notes/mc-quiz.html)**

線上版功能：

- **點選答案**即自動計分，並即時顯示得分
- **作答進度自動存在你的瀏覽器**（localStorage）——關掉網頁、隔天再開都能繼續
- 可切換「只顯示未答」或「只顯示答錯」的題目，快速複習
- 按「顯示答案」才揭曉正解與解析，不會一開始就被暴雷
- 需要紙本時，直接在該頁按列印

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
2. 找個安靜的 75 分鐘，完整做一次**附錄 F 的 60 題線上互動測驗**
3. 考前 10 分鐘只看**附錄 E 一頁精華**

祝考試順利。

---

*本篇為個人學習筆記整理，教材內容版權屬匯縱專業發展中心（IVDC）所有。*
