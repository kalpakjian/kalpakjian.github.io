---
title: 專題：IVDC 電腦視覺課程筆記
date: 2026-10-10 23:40:00
---

這是 **IVDC（匯縱專業發展中心）「Certificate in Application of Computer Vision Technology (Part-time)」** 課程的學習筆記專題。

我把課程內容逐份整理成**可離線閱讀**的筆記，每一份都附 **60 題互動 MC 測驗**（點選即時計分、進度自動儲存）。

> 以下依**課程官方順序**（Lesson Plan）排列；✅ 已完成，⏳ 尚未製作。

---

## 課程順序總覽

| 課節 | 主題 | 筆記 |
|:---:|---|---|
| **Lesson 1** | Introduction to Generative AI | ✅ [Introduction to AI 學習筆記](/ai-intro-notes/) |
| **Lesson 2** | Using Local GPU for ML | ✅ [Using Local GPU for ML 學習筆記](/local-gpu-ml-notes/) |
| **Lesson 2** | Introduction to Computer Vision and Application | ✅ [Introduction to Computer Vision 學習筆記](/cv-intro-notes/) |
| **Lesson 3** | OpenCV | ✅ [OpenCV 學習筆記](/opencv-notes/) |
| **Lesson 4** | Responsible AI | ✅ [Responsible AI 學習筆記](/responsible-ai-notes/) |
| **Lesson 4** | Test | — |
| **Lesson 5** | Neural Network, Activation Function and Machine Learning | ✅ [Neural Network &amp; ML 學習筆記](/neural-network-notes/) |
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

## 5 · Lesson 4 — Responsible AI

![Responsible AI 學習筆記](/img/covers/responsible-ai-notes-ivdc.png)

- **涵蓋**：Responsible AI 定義與 Challenges on AI、**12 項倫理原則**、AI Practice Guide **6 階段**、四大倫理議題（隱私與監控／偏見與歧視／資料安全與同意／問責與透明）、香港 **PDPO《個人資料（私隱）條例》**（Cap. 486、1996/12/20 生效）與**六項保護原則 DPP1–DPP6**、社會影響五項、六項倫理使用建議與結論
- 附**本機實測**的偏見量測程式（混淆矩陣 → FNR／FPR／Equal Opportunity Difference，多數族群 95% vs 少數族群 89%）
- **👉 [看筆記](/responsible-ai-notes/)** ｜ [互動測驗 60 題](/responsible-ai-notes/mc-quiz.html)

---

## 6 · Lesson 5 — Neural Network, Activation Function and Machine Learning

![Neural Network & ML 學習筆記](/img/covers/neural-network-notes-ivdc.png)

- **涵蓋**：生物神經元（樹突／軸突／突觸／動作電位）、ANN 三層結構與前向／反向傳播、ANN vs DNN 與網路拓撲、激勵函數（**TLU／ReLU／Sigmoid／Softmax**）、問題類型對應、機器學習基本概念與**十個步驟**、Data/AI Landscape、監督式／非監督式學習、混淆矩陣與指標、迴歸、分群
- **特別之處**：教材後半幾乎都是圖（p9–p16、p25–p26、p29–p30 抽不出文字），筆記**把 22 張圖全部重畫成內嵌 SVG**（公式曲線與數字都是算出來的），並額外用 **Qwen-Image 2.1 生成 16 張專屬概念插圖**（同樣內嵌，共 38 張圖）
- **👉 [看筆記](/neural-network-notes/)** ｜ [互動測驗 60 題](/neural-network-notes/mc-quiz.html)

---

## 筆記的共同規格

| 項目 | 說明 |
|---|---|
| 格式 | **單一 HTML 檔、零外部資源**，下載後可離線雙擊開啟 |
| 版面 | 左側固定側邊欄 + **自動產生的巢狀目錄樹**（不會有壞連結） |
| 測驗 | 每份 **60 題互動 MC**：即時計分、進度存 localStorage、可列印 |
| 附錄 | 名詞／指令速查表、常見錯誤與陷阱、一頁精華（考前 10 分鐘） |
| 原始檔 | 每頁都可下載原始 Markdown |
| 來源 | 依課程大綱逐節重寫，並補上考點、指令與實測數據 |

---

*本專題為個人學習筆記整理。*
