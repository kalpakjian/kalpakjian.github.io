---
title: 電腦視覺課程 學習筆記總覽
date: 2026-10-10 23:40:00
---

## 1 · Lesson 1 — Introduction to Generative AI

![Introduction to AI 學習筆記](/img/covers/ai-intro-notes.png)

- **涵蓋**：AI 定義與兩個取徑（Human／Ideal）、AI 子目標、商業應用、異常偵測、影像／視訊辨識、人臉辨識、NLP（HMM 與 cepstral coefficients）、語音辨識、強化學習、生成式 AI
- **👉 [看筆記](/ai-intro-notes/)** ｜ [互動測驗 60 題](/ai-intro-notes/mc-quiz.html)

---

## 2 · Lesson 2 — Using Local GPU for ML

![Using Local GPU for ML 學習筆記](/img/covers/local-gpu-ml-notes.png)

- **涵蓋**：Nvidia 驅動 → Visual Studio C++ → Anaconda → Anaconda PATH → CUDA Toolkit → cuDNN（含複製 bin／lib／include）→ 環境變數 → VS Code／Git → PyTorch → GPU 驗證
- 附**本機實測數據**（RTX 4090 / 驅動 617.42 / CUDA 13.4 / PyTorch 2.14.1+cu132）
- **👉 [看筆記](/local-gpu-ml-notes/)** ｜ [互動測驗 60 題](/local-gpu-ml-notes/mc-quiz.html)

---

## 3 · Lesson 2 — Introduction to Computer Vision and Application

![Introduction to Computer Vision 學習筆記](/img/covers/cv-intro-notes.png)

- **涵蓋**：電腦視覺商業案例（零售／安防／工業／醫療／自駕／農業）、2024 世界機器人大會、CNN 定義、State-of-the-art 與 encoder、**參數重用**、CNN 基本概念與影像辨識
- **👉 [看筆記](/cv-intro-notes/)** ｜ [互動測驗 60 題](/cv-intro-notes/mc-quiz.html)

---

## 4 · Lesson 3 — OpenCV

![OpenCV 學習筆記](/img/covers/opencv-notes.png)

- **涵蓋**：OpenCV 全 15 節（色彩空間、前處理、矩陣運算、繪圖函式、幾何變換、濾波、邊緣偵測、特徵擷取與匹配、實務專案），**所有程式碼皆本機實測**
- **👉 [看筆記](/opencv-notes/)** ｜ [互動測驗 60 題](/opencv-notes/mc-quiz.html)

---

## 5 · Lesson 4 — Responsible AI

![Responsible AI 學習筆記](/img/covers/responsible-ai-notes.png)

- **涵蓋**：Responsible AI 定義與 Challenges on AI、**12 項倫理原則**、AI Practice Guide **6 階段**、四大倫理議題（隱私與監控／偏見與歧視／資料安全與同意／問責與透明）、香港 **PDPO《個人資料（私隱）條例》**（Cap. 486、1996/12/20 生效）與**六項保護原則 DPP1–DPP6**、社會影響五項、六項倫理使用建議與結論
- 附**本機實測**的偏見量測程式（混淆矩陣 → FNR／FPR／Equal Opportunity Difference，多數族群 95% vs 少數族群 89%）
- **👉 [看筆記](/responsible-ai-notes/)** ｜ [互動測驗 60 題](/responsible-ai-notes/mc-quiz.html)

---

## 6 · Lesson 5 — Neural Network, Activation Function and Machine Learning

![Neural Network & ML 學習筆記](/img/covers/neural-network-notes.png)

- **涵蓋**：生物神經元（樹突／軸突／突觸／動作電位）、ANN 三層結構與前向／反向傳播、ANN vs DNN 與網路拓撲、激勵函數（**TLU／ReLU／Sigmoid／Softmax**）、問題類型對應、機器學習基本概念與**十個步驟**、Data/AI Landscape、監督式／非監督式學習、混淆矩陣與指標、迴歸、分群
- **特別之處**：後半段幾乎都是圖，筆記**把 22 張圖全部重畫成內嵌 SVG**（公式曲線與數字都是算出來的），並額外用 **Qwen-Image 2.1 生成 16 張專屬概念插圖**（同樣內嵌，共 38 張圖）
- **👉 [看筆記](/neural-network-notes/)** ｜ [互動測驗 60 題](/neural-network-notes/mc-quiz.html)

---

## 7 · Lesson 6 — Convolutional Neural Network (CNN) 1

![CNN 學習筆記](/img/covers/cnn-notes.png)

- **涵蓋**：場景理解與物件辨識、**視覺皮層的分層抽象**（LGN→V1→V4→VTC）、神經元與動作電位、**空間結構與滑動視窗**、卷積＝**逐元素相乘再相加**、特徵圖、**銳化／邊緣偵測／模糊**等經典核心、**de novo 特徵階層**、**參數共享**、**LeNet-5**（架構、張量尺寸、參數數）、**卷積的反向傳播**、CNN 的形式化架構與應用版圖
- **特別之處**：6 張圖表全部做成**內嵌 SVG**（卷積滑動、視覺皮層、全連接 vs 卷積、特徵階層、LeNet-5 架構、反向傳播），**所有數字都在本機實測**（卷積輸出、輸出尺寸公式、LeNet-5 參數數、梯度檢查）
- **👉 [看筆記](/cnn-notes/)** ｜ [互動測驗 60 題](/cnn-notes/mc-quiz.html)
- **延伸**：同一堂課的**課後深度筆記**（9 張霓虹 SVG 插圖＋簡報勘誤表）→ [CNN I：機器怎麼「看」？](/2026/10/27/cnn-1-convnet-neon/) ｜ 把卷積從一張 5×5 小圖重算一遍 → [圖解 CNN](/cnn-illustrated/)

---

## 8 · Lesson 7 — CNN 2

![CNN 2 學習筆記](/img/covers/cnn2-notes.png)

- **涵蓋**：局部連接與參數共享、輸出體積 / stride / 感受野、ReLU 的兩個經典問題（何時回傳梯度、單元死亡）、池化的降維與空間不變性、空洞卷積、softmax、用 `tf.keras.Sequential` 組模型
- **特別之處**：課程示範碼有三個會直接報錯的寫法（彎引號、`filter_size`、缺 `Input`），筆記 §10 附勘誤表與修正後可直接執行的版本；另外量到「零激活 50.6% 但死濾波器 0%」，把「稀疏」與「死亡」分開
- **👉 [看筆記](/cnn2-notes/)** ｜ [互動測驗 49 題](/cnn2-notes/mc-quiz.html)
- **延伸**：簡報那段範例程式碼的 33 組實驗（與課程內容無關）→ [CNN II 實驗紀錄](/2026/10/29/cnn-2-experiments/) ｜ 卷積 / ReLU / 池化 / softmax 的圖解版 → [圖解 CNN](/cnn-illustrated/) ｜ 只拆卷積層（kernel 深度、stride、感受野、空洞）→ [卷積層的運作細節](/cnn-conv-details/) ｜ ReLU 與池化的細節 → [激活函數與池化層](/cnn-activation-pooling/) ｜ 最後一哩的全連接層與 softmax → [全連接層的運作](/cnn-fully-connected/) ｜ 兩者對照總整理 → [卷積層 vs 全連接層](/cnn-conv-vs-fc/) ｜ 為什麼現代 CNN 改用 GAP 頭 → [分類頭與 GAP](/cnn-gap-head/) ｜ GAP 怎麼變成熱圖 → [CAM](/cnn-cam/)

---

## 9 · Lesson 9 — Practical Application for Implementation and Demo

![Teachable Machine 實作學習筆記](/img/covers/cv-practical-notes.png)

- **涵蓋**：Teachable Machine（**Gather → Train → Export**）、圖像／聲音／姿勢三類專案、TensorFlow.js 與 TensorFlow 的關係、香蕉四類例子（含 `No banana`）、**本機訓練**（不上傳、不可切換分頁）、預覽與匯出（TF.js／TF／TF Lite）、機器學習的限制（**圖像只是像素規律**）、三個失敗案例（兩隻香蕉／換背景 **100 % → ≈60 %**／圖畫仍判 `Ripe` **≈88 %**）、穩健度三因素（樣本量與多樣性、背景與光線、方向），以及示範項目**「機械蛇（Teachable Machine + p5.js）」**
- **特別之處**：把簡報 19 頁整理成 **22 節結構化筆記**，附 12 條自我檢測題、關鍵詞表、網址與程式碼速查表、溫習清單
- **👉 [看筆記](/2026/10/28/cv-practical-teachable-machine-notes/)**

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

*本頁為個人學習筆記整理。*

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
| **Lesson 6** | Convolutional Neural Network (CNN) 1 | ✅ [CNN 學習筆記](/cnn-notes/) |
| **Lesson 7** | CNN 2 | ✅ [CNN 2 學習筆記](/cnn2-notes/) |
| **Lesson 8** | Tensorflow and Pytorch for Object Detection and CNN | ⏳ 待補 |
| **Lesson 9** | Practical Application for Implementation and Demo | ✅ [Teachable Machine 實作筆記](/2026/10/28/cv-practical-teachable-machine-notes/) |
| **Lesson 10** | Exam | — |
