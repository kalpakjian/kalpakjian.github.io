---
title: 專題：IVDC 電腦視覺課程筆記
date: 2026-10-10 23:40:00
---

這是 **IVDC（匯縱專業發展中心）「Certificate in Application of Computer Vision Technology (Part-time)」** 課程的學習筆記專題。

我把課程教材（PowerPoint 匯出的 PDF）逐份重寫成**可離線閱讀**的筆記，每一份都附 **60 題互動 MC 測驗**（點選即時計分、進度自動儲存）。

> 以下依**課程官方順序**（Lesson Plan）排列；✅ 已完成，⏳ 尚未製作。

---

## 課程順序總覽

| 課節 | 主題 | 筆記 |
|:---:|---|---|
| **Lesson 1** | Introduction to Generative AI | ✅ [Introduction to AI 學習筆記](/ai-intro-notes/) |
| **Lesson 2** | Using Local GPU for ML | ✅ [Using Local GPU for ML 學習筆記](/local-gpu-ml-notes/) |
| **Lesson 2** | Introduction to Computer Vision and Application | ✅ [Introduction to Computer Vision 學習筆記](/cv-intro-notes/) |
| **Lesson 3** | OpenCV | ✅ [OpenCV 學習筆記](/opencv-notes/) |
| **Lesson 4** | Responsible AI | ⏳ 待補 |
| **Lesson 4** | Test | — |
| **Lesson 5** | Neural Network, Activation Function and Machine Learning | ⏳ 待補 |
| **Lesson 6** | Convolutional Neural Network (CNN) 1 | ⏳ 待補 |
| **Lesson 7** | CNN 2 | ⏳ 待補 |
| **Lesson 8** | Tensorflow and Pytorch for Object Detection and CNN | ⏳ 待補 |
| **Lesson 9** | Practical Application for Implementation and Demo | ⏳ 待補 |
| **Lesson 10** | Exam | — |

---

## 1 · Lesson 1 — Introduction to Generative AI

![Introduction to AI 學習筆記](/img/covers/ai-intro-notes-ivdc.png)

- **涵蓋**：AI 定義與兩個取徑（Human／Ideal）、AI 子目標、商業應用、異常偵測、影像／視訊辨識、人臉辨識、NLP（HMM 與 cepstral coefficients）、語音辨識、強化學習、生成式 AI
- **👉 [看筆記](/ai-intro-notes/)** ｜ [互動測驗 60 題](/ai-intro-notes/mc-quiz.html)

---

## 2 · Lesson 2 — Using Local GPU for ML

![Using Local GPU for ML 學習筆記](/img/covers/local-gpu-ml-notes-ivdc.png)

- **涵蓋**：Nvidia 驅動 → Visual Studio C++ → Anaconda → Anaconda PATH → CUDA Toolkit → cuDNN（含複製 bin／lib／include）→ 環境變數 → VS Code／Git → PyTorch → GPU 驗證
- 附**本機實測數據**（RTX 4090 / 驅動 617.42 / CUDA 13.4 / PyTorch 2.14.1+cu132）
- **👉 [看筆記](/local-gpu-ml-notes/)** ｜ [互動測驗 60 題](/local-gpu-ml-notes/mc-quiz.html)

---

## 3 · Lesson 2 — Introduction to Computer Vision and Application

![Introduction to Computer Vision 學習筆記](/img/covers/cv-intro-notes-ivdc.png)

- **涵蓋**：電腦視覺商業案例（零售／安防／工業／醫療／自駕／農業）、2024 世界機器人大會、CNN 定義、State-of-the-art 與 encoder、**參數重用**、CNN 基本概念與影像辨識
- **👉 [看筆記](/cv-intro-notes/)** ｜ [互動測驗 60 題](/cv-intro-notes/mc-quiz.html)

---

## 4 · Lesson 3 — OpenCV

![OpenCV 學習筆記](/img/covers/opencv-notes-ivdc.png)

- **涵蓋**：OpenCV 全 15 節（色彩空間、前處理、矩陣運算、繪圖函式、幾何變換、濾波、邊緣偵測、特徵擷取與匹配、實務專案），**所有程式碼皆本機實測**
- **👉 [看筆記](/opencv-notes/)** ｜ [互動測驗 60 題](/opencv-notes/mc-quiz.html)

---

## 筆記的共同規格

| 項目 | 說明 |
|---|---|
| 格式 | **單一 HTML 檔、零外部資源**，下載後可離線雙擊開啟 |
| 版面 | 左側固定側邊欄 + **自動產生的巢狀目錄樹**（不會有壞連結） |
| 測驗 | 每份 **60 題互動 MC**：即時計分、進度存 localStorage、可列印 |
| 附錄 | 名詞／指令速查表、常見錯誤與陷阱、教材頁面索引對照、一頁精華（考前 10 分鐘） |
| 原始檔 | 每頁都可下載原始 Markdown |
| 來源 | 忠實對照原稿每一個標題逐節重寫，並補上考點、指令與實測數據 |

---

*教材內容版權屬匯縱專業發展中心（IVDC）所有；本專題僅為個人學習筆記整理。*
