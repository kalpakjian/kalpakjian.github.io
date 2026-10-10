---
title: OpenCV 電腦視覺學習筆記：IVDC 課程完整複習 + 60 題 MC 模擬試卷
date: 2026-10-07 09:00:00
categories:
  - 學習資源
tags:
  - OpenCV
  - 電腦視覺
  - IVDC
  - 學習筆記
  - 考試
index_img: /img/covers/opencv-notes-ivdc.png
banner_img: /img/covers/opencv-notes-ivdc.png
---

最近為了準備 IVDC（匯縱專業發展中心）「Certificate in Application of Computer Vision Technology」的考試，我把課程教材《3 IVDC OpenCV.pdf》的 29 頁內容完整重寫成一份可離線閱讀的學習筆記，並額外做了一份 60 題的 MC 模擬試卷。

筆記已發佈成獨立專題頁面：

**👉 [OpenCV 學習筆記（考試溫習版）](/opencv-notes/)**

<!-- more -->

---

## 這份筆記包含什麼

按 PDF 原稿的每一個標題逐一填充，涵蓋全部 15 節課程內容：

| 章節 | 主題 |
|---|---|
| 1–2 | What is OpenCV? / OpenCV Applications |
| 3–4 | Color Spaces / Color Space Conversion |
| 5 | Image Pre-processing |
| 6 | Matrix Operations |
| 7 | Drawing Functions |
| 8 | Transformations |
| 9 | Filtering Techniques |
| 10 | Edge Detection |
| 11–12 | Feature Extraction / Feature Matching |
| 13 | Real-World Projects |
| 14 | OpenCV Programming Examples（教材第 16–28 頁的程式範例） |
| 15 | Summary |

另外補了 6 個附錄：**API 速查表**、**常見錯誤與陷阱**、**模擬試題**、**教材頁面索引對照**、**離線執行提示**、**一頁精華（考前 10 分鐘）**。

---

## 重點：60 題 MC 模擬試卷

因為考試可能是選擇題形式，我特別做了一份**完整計時模擬試卷**（附錄 G，**互動網頁版**）：

**🖱️ [開始 60 題線上測驗](/opencv-notes/mc-quiz.html)**

線上版功能：

- **點選答案**即自動計分，並即時顯示得分
- **作答進度自動存在你的瀏覽器**（localStorage）——關掉網頁、隔天再開都能繼續
- 可切換「只顯示未答」或「只顯示答錯」的題目，快速複習
- 按「顯示答案」才揭曉正解與解析，不會一開始就被暴雷
- 需要紙本時，直接在該頁按列印

**試卷設計**

- 60 題單選、滿分 60 分、建議 75 分鐘
- 分三部分：基礎與色彩空間（1–20）、前處理／矩陣／繪圖／變換（21–40）、濾波／邊緣／特徵／匹配／專案（41–60）
- 答案分佈刻意打散（A 16 / B 13 / C 17 / D 14），避免整排猜同一個字母
- 每題詳解都附「答錯題目 → 對應複習章節」對照，方便回頭補強

> 出題率最高的考點包括：OpenCV 讀入是 **BGR**、`resize` 的 dsize 是 **(寬, 高)**、ROI 切片先 **Y** 後 **X**、kernel 必須是**正奇數**、`thickness = -1` 代表**填滿**、`uint8` 相加會**溢位回繞**、開運算 = 先侵蝕再膨脹、Canny 只吃單通道 8-bit、ORB 配 **Hamming** 距離、RANSAC 用來**剔除 outliers**。

---

## 所有程式碼都實測過

筆記裡的 25 段程式碼全部在本機跑過，環境是：

```text
OpenCV     5.0.0
NumPy      2.4.6
Matplotlib 3.11.2
```

幾個和教材對得上的實測數字：ORB 偵測到 **493** 個關鍵點、描述子形狀 **(493, 32)**、Canny 得到 **3157** 個邊緣像素、ORB + BFMatcher 在 45° 旋轉後仍有 **280** 組匹配。

---

## 離線也能用

筆記是**單一 HTML 檔、零外部資源**（CSS 與語法高亮全部內嵌），下載後直接雙擊就能看，適合考前在沒有網路的環境複習。

也可以下載原始 Markdown：

**📄 [OpenCV_Study_Notes.md](/opencv-notes/OpenCV_Study_Notes.md)**

---

## 建議使用順序

1. 先讀完第 1–15 節，把附錄 A（API 速查表）當工具書隨時查
2. 做附錄 C 的 43 題（隨讀隨測，每題下方有摺疊答案）
3. 找個安靜的 75 分鐘，完整做一次**附錄 G 的 60 題模擬試卷**
4. 考前 10 分鐘只看**附錄 F 一頁精華**

祝考試順利。

---

*本篇為個人學習筆記整理，教材內容版權屬匯縱專業發展中心（IVDC）所有。*
