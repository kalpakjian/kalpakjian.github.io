# Introduction to AI 學習筆記（考試溫習版）

> 課程：Certificate in Application of Computer Vision Technology (Part-time)
> 機構：匯縱專業發展中心（IVDC）
> 教材來源：`1 IVDC_Introduction to AI (icebreaking).pptx` → PDF（34 頁）
> 本筆記按 PDF 原稿每一個標題逐一填充內容，並補上定義、參數、常見錯誤、模擬試題。
> 原稿多為投影片圖示，文字較少；本筆記補上「圖示背後的概念」與「考點」，方便理解與應試。
> **附錄 G 另備一份 60 題的 MC 模擬試卷（含答案速查表與逐題詳解）**，適合考前完整計時練習。

---

## 目錄

| # | 章節 | PDF 頁 |
|---|------|--------|
| 1 | [AI 是什麼？定義與兩個取徑](#1-ai-是什麼定義與兩個取徑) | 5–6 |
| 2 | [AI 的子目標（Sub-objectives of AI）](#2-ai-的子目標sub-objectives-of-ai) | 8 |
| 3 | [AI 應用與例子](#3-ai-應用與例子) | 7, 9 |
| 4 | [異常偵測 Anomaly Detection](#4-異常偵測-anomaly-detection) | 10 |
| 5 | [影像／視訊辨識 Image/Video Recognition](#5-影像視訊辨識-imagevideo-recognition) | 11–12 |
| 6 | [人臉辨識 Facial Recognition](#6-人臉辨識-facial-recognition) | 13–15 |
| 7 | [自然語言處理 NLP](#7-自然語言處理-nlp) | 17–20, 22–23, 25–26 |
| 8 | [語音辨識 Speech Recognition](#8-語音辨識-speech-recognition) | 21, 24, 27 |
| 9 | [強化學習 Reinforcement Learning](#9-強化學習-reinforcement-learning) | 29–33 |
| 10 | [生成式 AI Generative AI](#10-生成式-ai-generative-ai) | 34 |
| A | [附錄 A：AI 名詞速查表](#附錄-aai-名詞速查表) | — |
| B | [附錄 B：常見錯誤與陷阱](#附錄-b常見錯誤與陷阱) | — |
| C | [附錄 C：模擬試題（連答案）](#附錄-c模擬試題連答案) | — |
| D | [附錄 D：教材頁面索引對照](#附錄-d教材頁面索引對照) | — |
| E | [附錄 E：延伸資源與離線提示](#附錄-e延伸資源與離線提示) | — |
| F | [附錄 F：一頁精華（考前 10 分鐘）](#附錄-f一頁精華考前-10-分鐘) | — |
| G | [附錄 G：MC 模擬試卷（60 題）](#附錄-gmc-模擬試卷60-題) | — |

---

## 0. 30 秒總複習（考前最後掃描）

```
AI = 具人類式智慧的「機器智慧」
  ├─ 取徑：Human approach（think/act like humans）
  │        Ideal approach（think/act rationally）
  ├─ 子目標：NLP、Navigate、Represent Knowledge、Reasoning、Perception
  └─ 典型應用：
       影像 → Image/Video Recognition → Facial Recognition（Detection→Analysis→Recognition）
       語言 → NLP → Speech Recognition（HMM、cepstral coefficients）
       決策 → Reinforcement Learning（agent、reward、policy）
       生成 → Generative AI（deep learning 生成新內容）
```

| 你會用到的關鍵詞 | 一句話記法 |
|---|---|
| Artificial Intelligence | 機器展現出類人的智慧 |
| Human approach | 像人一樣思考／行動（think/act like humans） |
| Ideal approach | 理性地思考／行動（think/act rationally） |
| Sub-objectives | NLP、Navigate、Represent Knowledge、Reasoning、Perception |
| Facial Recognition | 三步：**Detection → Analysis → Recognition** |
| Faceprint | 把臉部資料轉成數字／點串，如指紋般獨一無二 |
| NLP | 讓機器「講得到、聽得明、理解句子」 |
| HMM | 語音辨識常用模型；10 毫秒為一段的平穩過程假設 |
| Cepstral coefficients | 每 10ms 片段的功率頻譜轉成的實數向量（常 10～32 維） |
| Speech Recognition | 訓練資料偏頗 → 不同族群準確率有差 |
| Reinforcement Learning | Agent 觀察→行動→獎勵/懲罰→學到最佳 policy |
| AlphaGo | DeepMind，擊敗圍棋世界冠軍 Lee Sedol |
| Generative AI | 用深度學習生成新內容（圖、文、樂、影片） |

---

## 1. AI 是什麼？定義與兩個取徑

**Artificial Intelligence（人工智慧）** 的通用理論是：AI 擁有**類人的智慧（human-like intelligence）**，
但本質上是**機器智慧（machine intelligence）** —— 智慧由機器展現，而不是人。

原稿（p5–6）把 AI 的取徑分成兩大類、共四種：

| 取徑 | 思考 | 行動 |
|------|------|------|
| **Human approach**（以人為本） | Systems that **think** like humans（像人一樣思考） | Systems that **act** like humans（像人一樣行動） |
| **Ideal approach**（理想／理性） | Systems that **think** rationally（理性地思考） | Systems that **act** rationally（理性地行動） |

- **Human approach**：模仿人類實際的思考與行為（含人類的偏誤與限制）。
- **Ideal approach**：以「邏輯／理性」為標準，追求最佳解，不一定要像人。

> **考點**：四個象限要能分辨 ——「think like humans / act like humans / think rationally / act rationally」。
> 常見陷阱：把 Human approach 說成「理性」，或把 Ideal approach 說成「像人」。

### 1.1 開場破冰（p2–4）：生活裡的 AI

原稿用生活情境提問：

- 「你喜歡用 App 在餐廳點餐嗎？當中有沒有 AI？」
- 「Can Machines Think more than us?」（機器能比我們想得更多嗎？）

這些是引導思考的暖場題，重點是建立「**AI 已在日常之中**」的認知，並非考點本身。

> **考點**：AI 的定義關鍵詞是「**machine intelligence**」與「**human-like intelligence**」兩者並存。

---

## 2. AI 的子目標（Sub-objectives of AI）

原稿 p8 用一張圖把 AI 拆成 5 個子目標：

| 子目標 | 英文 | 說明 | 例子 |
|--------|------|------|------|
| 自然語言處理 | Natural Language Processing | 讓機器理解／產生人類語言 | 語音助理、翻譯、聊天機械人 |
| 導航 | Navigate | 在環境中定位與規劃路徑 | GPS 導航、自駕車 |
| 知識表示 | Represent Knowledge | 把知識用機器可處理的方式儲存 | 知識圖譜、ontology |
| 推理 | Reasoning | 由已知推導出新結論 | 專家系統、定理證明 |
| 感知 | Perception | 從感測資料理解世界 | 電腦視覺、語音辨識 |

> **考點**：五個子目標要背齊 —— **NLP、Navigate、Represent Knowledge、Reasoning、Perception**。
> 這五者常作為 AI 的分類骨架出現在選擇題。

---

## 3. AI 應用與例子

原稿 p9 把應用分成三大類，逐項列出：

### 3.1 電子商務 E-Commerce

- **個人化購物**（Personalized Shopping）：依瀏覽／購買紀錄推薦商品。
- **AI 助理**（AI-powered Assistants）：客服機械人、購物助手。
- **詐騙防治**（Fraud Prevention）：偵測盜刷信用卡、假評論（fake review）。

### 3.2 教育 Education

- 自動發送個人化訊息給學生（Automating personalized messages to students）。
- 管理招生／註冊（Managing enrollment）。
- 批改作業／文書（Grading paperwork）。

### 3.3 日常生活 Daily life

- **自動駕駛**（Autonomous Vehicles），例如 Tesla。
- **垃圾郵件過濾**（Spam email filters）。
- **人臉辨識**（Facial Recognition），例如 iPhone Face Unlock。
- **GPS 導航**（Navigation by GPS）。

> **考點**：能把例子歸類到正確領域。例如「fake review 偵測」屬 **E-Commerce 的詐騙防治**，
> 「Grading paperwork」屬 **Education**，「Face Unlock」屬 **Daily life 的人臉辨識**。

---

## 4. 異常偵測 Anomaly Detection

原稿 p10 只有標題「Anomaly Detection」與一張示意圖。**異常偵測**是指找出**不符合預期模式**的資料點
（outlier），是 AI 在工業、金融、資安上的核心應用之一。

| 項目 | 內容 |
|------|------|
| 定義 | 從大量資料中找出「罕見、異常、不尋常」的樣本 |
| 目標 | 找出 outlier / novelty，而非把資料分類成既有類別 |
| 常見方法 | 統計方法（z-score、IQR）、距離法（kNN）、密度法（LOF）、孤立森林（Isolation Forest）、Autoencoder 重建誤差 |
| 典型應用 | 信用卡盜刷、工業瑕疵檢測、網路入侵偵測、設備預測性維護、醫療異常 |

> **考點**：異常偵測是**找出少數的異常**，常面對**類別極不平衡**（正常樣本遠多於異常）。
> 因此**準確率（accuracy）不是好指標**，要看 **Precision / Recall / F1**。

---

## 5. 影像／視訊辨識 Image/Video Recognition

原稿 p11–12 的定義重點：

> 機器用**電腦視覺（computer vision）**辨識影像中的人、地、物，**準確度可達或超越人類水準**，
> 而且**速度與效率遠勝人類**。透過複雜的 AI 技術，電腦視覺把影像資料自動化地
> **擷取（extraction）、分析（analysis）、分類（classification）與理解（understanding）**。

### 5.1 影像資料的四種形式（p11）

| # | 形式 | 英文 | 例子 |
|---|------|------|------|
| 1 | 單張影像 | Single images | 一張照片 |
| 2 | 視訊序列 | Video sequences | 連續影格 |
| 3 | 多鏡頭視角 | Views from multiple cameras | 環景、監控多機 |
| 4 | 三維資料 | Three-dimensional data | LiDAR、深度相機、點雲 |

### 5.2 電腦視覺任務（p12）

- 電腦視覺任務 = 辨識並**分類**影像／影片中的各種元素。
- AI 被訓練成：**輸入一張影像 → 輸出描述該影像的屬性（attributes）**。

> **考點**：記住「**輸入影像 → 輸出屬性**」這個介面；以及四種影像資料形式（單張／序列／多鏡頭／3D）。
> 常見混淆：把「多鏡頭視角」與「3D 資料」混為一談 —— 前者是多個 2D 視角，後者是帶深度的 3D 資料。

---

## 6. 人臉辨識 Facial Recognition

原稿 p13–15 是重點章節，明確指出人臉辨識**分三個步驟**：

```
Detection（偵測） → Analysis（分析） → Recognition（辨識）
```

### 6.1 Detection 偵測（p13）

- **定義**：在影像中**找出人臉**的過程。
- 由**電腦視覺**支援，可從「一張含一人或多人」的影像中偵測並找出**個別人臉**。
- 可偵測**正面（front）與側面（side profile）**的臉部資料。

### 6.2 Analysis 分析（p14）

系統接著**分析**人臉影像，**測繪並讀取臉部幾何（face geometry）與表情（facial expressions）**，
找出能把臉與其他物件區分開的**臉部特徵點（facial landmarks）**。通常量測以下項目：

| # | 量測項目 |
|---|----------|
| 1 | 兩眼之間的距離（Distance between the eyes） |
| 2 | 額頭到下巴的距離（Distance from the forehead to the chin） |
| 3 | 鼻子到嘴巴的距離（Distance between the nose and mouth） |
| 4 | 眼窩深度（Depth of the eye sockets） |
| 5 | 顴骨形狀（Shape of the cheekbones） |
| 6 | 嘴唇、耳朵與下巴的輪廓（Contour of the lips, ears, and chin） |

### 6.3 Recognition 辨識（p15）

- 系統把臉部資料轉成一串數字或點，稱為 **faceprint（臉紋）**。
- **每個人的 faceprint 都是獨一無二的，就像指紋（fingerprint）一樣**。
- 這些資料**可以反向使用**，用來**數位重建（digitally reconstruct）**一個人的臉。
- **辨識方式**：比對兩張（或以上）影像中的臉，評估**吻合的可能性（likelihood of a face match）**。
  - 例：比對手機自拍與證件照（駕照、護照）是否為同一人。
  - 也可用來確認「自拍的臉**不在**先前蒐集的人臉集合中」。

> **考點**：三步骤順序 **Detection → Analysis → Recognition** 幾乎必考；
> 「faceprint 像指紋般獨一無二」、「可反向重建人臉」是常考細節。

---

## 7. 自然語言處理 NLP

### 7.1 NLP 要解決的三件事（p17）

原稿用三個問題概括 NLP：

1. **How to speak a language** —— 如何「講」一種語言（語言生成）。
2. **How to understand a language** —— 如何「聽懂」一種語言（語言理解）。
3. **How to make sense out of a sentence** —— 如何從一個句子中「理解出意義」（語意理解）。

> 一句話：NLP 就是讓機器能**講得到、聽得明、理解句子**。

### 7.2 語音辨識的模型：Hidden Markov Model（p18–19）

原稿指出：**大多數現代語音辨識系統依賴 Hidden Markov Model（HMM，隱馬可夫模型）**。

- **核心假設**：一段語音訊號，若用**足夠短的時間尺度**觀察（例如 **10 毫秒**），
  可以合理地近似為一個**平穩過程（stationary process）** ——
  即統計性質**不隨時間改變**的過程。

**HMM 的處理流程（p19）**：

| 步驟 | 內容 |
|------|------|
| 1 | 把語音訊號切成 **10 毫秒** 的片段（fragments） |
| 2 | 計算每個片段的**功率頻譜（power spectrum）**（訊號功率對頻率的關係圖） |
| 3 | 把功率頻譜映射成一個實數向量 → **cepstral coefficients（倒頻譜係數）** |
| 4 | 該向量維度通常很小：**有時低至 10 維**；較精確的系統可達 **32 維或以上** |
| 5 | HMM 的最終輸出 = **這些向量的序列（a sequence of these vectors）** |

> **考點**：記住三個數字與名詞 —— **10 毫秒**、**cepstral coefficients**、**維度 10～32**，
> 以及「HMM 輸出是**向量序列**」。

### 7.3 語意／詞向量（p21，見第 8 節）

原稿 p21 用一組詞示範語意關係：**King、Queen、Man、Woman、Royal**，
並標示兩個語意維度：**Natural Understanding** 與 **Gender**。
這是**詞向量（word embedding）**的經典示意：語意相近的詞在向量空間中距離相近，
並可表現如「King − Man + Woman ≈ Queen」的類比關係（詳見第 8.1 節）。

### 7.4 延伸資源（p26）

- 原稿提供探索 NLP 的官方連結：`https://aka.ms/explore-nlp`

> **考點**：NLP 三個問題（speak / understand / make sense）＋ HMM 假設（10ms 平穩）是本章重點。

---

## 8. 語音辨識 Speech Recognition

### 8.1 語意理解示意（p21）

原稿以 **King / Queen / Man / Woman / Royal** 呈現兩個維度：

| 維度 | 說明 |
|------|------|
| Natural Understanding（自然理解） | 詞的語意關聯強度 |
| Gender（性別） | 詞的性別屬性 |

這正是**詞向量（word embeddings）**的概念：把詞映射到向量空間，
使「語意相近」與「性別」等屬性可用向量運算表達。

### 8.2 訓練資料偏頗問題（p27）——本章最重要

原稿指出語音辨識的一大挑戰是**訓練模型（training model）**：

- **大部分訓練資料需要人手分類（manually classified）**。
- 結果：**高準確率往往只在一小群特定說話者上達成**（而這群人往往正是最有價值的消費者）。

**Speechmatics 的做法與數據**（基於史丹福大學 "Racial Disparities in Speech Recognition" 研究所用的資料集）：

| 系統 | 對非裔美國人（African American）語音的整體準確率 |
|------|--------------------------------------------------|
| **Speechmatics** | **82.8%** |
| Google | 68.6% |
| Amazon | 68.6% |

- Speechmatics 的準確率提升，相當於**減少 45% 的語音辨識錯誤** ——
  以一句平均長度的句子來說，約等於**少錯 3 個字（three words）**。

> **考點**：本章高頻考「**訓練資料偏頗會造成不同族群準確率落差**」，
> 以及數字 **82.8% vs 68.6%**、**45% 錯誤減少 / 約 3 個字**。
> 觀念延伸：這屬於 AI **公平性（fairness）與代表性（representativeness）**議題。

---

## 9. 強化學習 Reinforcement Learning

原稿 p29–33 聚焦「**Reinforcement Learning in Robotic Control and Self-Driving**」
（強化學習在機械人控制與自動駕駛的應用）。

### 9.1 要解決的問題（p29）

在真實世界中「規劃與導航」，需要回答一連串問題：

- 如何在**真實世界**中規劃與導航（plan and navigate in the real world）？
- 如何**定位目的地**（locate the destination）？
- 如何**選路徑**（pick path）？
- 如何**選最短路徑**（pick short path）？
- 如何**避開障礙物**（avoid obstacles）？
- 如何**移動**（move）？

### 9.2 學習系統／代理人（Agent）的運作（p32）——核心考點

> 學習系統在此情境中扮演 **agent（代理人）**，它會：
> 1. **觀察環境**（Observes the environment）
> 2. **選擇並執行動作**（Selects and performs actions）
> 3. **得到獎勵或懲罰**（Get rewards or penalties in return）
> 4. **自己學會**在長期取得最多獎勵的**最佳策略（policy）**

用一句話概括：**Agent 透過與環境互動的「獎勵／懲罰」回饋，自行學出最佳策略（policy）。**

| 元素 | 英文 | 說明 |
|------|------|------|
| 代理人 | Agent | 做決策的學習系統 |
| 環境 | Environment | agent 所處的世界 |
| 動作 | Action | agent 的選擇與行為 |
| 獎勵／懲罰 | Reward / Penalty | 環境給的回饋訊號 |
| 策略 | Policy | agent 學到的「最佳行動準則」 |
| 目標 | Maximize reward over time | 長期累積獎勵最大化（非單步） |

### 9.3 應用例子（p33）

- **機械人學走路**（robots learn how to walk）。
- **DeepMind 的 AlphaGo** —— 擊敗圍棋世界冠軍 **Lee Sedol（李世乭）**。

> **考點**：RL 四步驟（**observe → act → reward/penalty → learn best policy**）幾乎必考；
> 「**AlphaGo + DeepMind + Lee Sedol + Go（圍棋）**」是常考配對。
> 常見混淆：把 RL 與「監督式學習」搞混 —— RL **沒有現成正確答案**，靠獎勵訊號試錯學習。

---

## 10. 生成式 AI Generative AI

原稿 p34 給出定義：

> **Generative AI（生成式 AI）** 指的是人工智慧中專注於**建立能生成新內容的模型或系統**的領域，
> 生成的內容例如**圖像、文字、音樂，甚至影片**。這些模型使用**機器學習技術，特別是深度學習（deep learning）**，
> 從**既有資料**中學習**模式與結構（patterns and structures）**，
> 然後生成與**訓練資料相似的新內容**。

重點拆解：

| 關鍵詞 | 說明 |
|--------|------|
| 生成新內容 | 圖像 / 文字 / 音樂 / 影片 |
| 核心技術 | 機器學習，**特別是深度學習** |
| 學習方式 | 從既有資料學「模式與結構」 |
| 產出特性 | 生成**與訓練資料相似**的新內容 |

> **考點**：定義句中的「**deep learning**」與「**generate new content similar to training data**」是關鍵；
> 生成式 AI ≠ 只能生成圖片，而是**圖／文／樂／影片**皆可。

---

<!-- 以下為附錄 -->

## 附錄 A：AI 名詞速查表

### A.1 核心概念

| 名詞 | 英文 | 一句話說明 |
|------|------|-----------|
| 人工智慧 | Artificial Intelligence (AI) | 機器展現的類人智慧（machine intelligence） |
| 機器智慧 | Machine intelligence | AI 的本質：由機器而非人展現的智慧 |
| 人類取徑 | Human approach | 像人一樣思考／行動 |
| 理想取徑 | Ideal approach | 理性地思考／行動 |
| 電腦視覺 | Computer vision | 讓機器從影像／影片理解世界 |
| 自然語言處理 | NLP | 讓機器講、聽、理解語言 |
| 強化學習 | Reinforcement Learning | 靠獎勵／懲罰學出最佳策略 |
| 生成式 AI | Generative AI | 用深度學習生成新內容 |
| 深度學習 | Deep learning | 以多層類神經網路學習資料的模式 |

### A.2 AI 五個子目標

| 子目標 | 英文 |
|--------|------|
| 自然語言處理 | Natural Language Processing |
| 導航 | Navigate |
| 知識表示 | Represent Knowledge |
| 推理 | Reasoning |
| 感知 | Perception |

### A.3 影像與人臉辨識

| 名詞 | 英文 | 說明 |
|------|------|------|
| 影像／視訊辨識 | Image/Video Recognition | 辨識並分類影像元素，輸入影像→輸出屬性 |
| 人臉辨識 | Facial Recognition | 三步：Detection → Analysis → Recognition |
| 偵測 | Detection | 在影像中找出人臉（含正面／側面） |
| 分析 | Analysis | 讀取臉部幾何與表情，取 facial landmarks |
| 辨識 | Recognition | 比對臉並評估吻合可能性 |
| 臉紋 | Faceprint | 臉部資料轉成的數字／點串，如指紋般獨一無二 |
| 臉部特徵點 | Facial landmarks | 眼距、額到下巴、鼻到嘴、眼窩深度、顴骨、輪廓 |

### A.4 語音與語言

| 名詞 | 英文 | 說明 |
|------|------|------|
| 隱馬可夫模型 | Hidden Markov Model (HMM) | 現代語音辨識常用模型 |
| 平穩過程 | Stationary process | 統計性質不隨時間改變的過程 |
| 功率頻譜 | Power spectrum | 訊號功率對頻率的關係 |
| 倒頻譜係數 | Cepstral coefficients | 功率頻譜映射成的實數向量（約 10～32 維） |
| 詞向量 | Word embedding | 把詞映射到向量空間（King/Queen/Man/Woman） |

### A.5 強化學習

| 名詞 | 英文 | 說明 |
|------|------|------|
| 代理人 | Agent | 做決策的學習系統 |
| 策略 | Policy | 學到的最佳行動準則 |
| 獎勵／懲罰 | Reward / Penalty | 環境給的回饋 |
| 圍棋對局 | AlphaGo vs Lee Sedol | DeepMind 擊敗世界冠軍 |

---

## 附錄 B：常見錯誤與陷阱

### B.1 十大陷阱總表

| # | 陷阱 | 錯誤觀念 | 正確觀念 |
|---|------|---------|---------|
| 1 | AI 取徑混淆 | 「Human approach 是理性的」 | Human = 像人；Ideal = 理性 |
| 2 | AI 子目標漏項 | 只記得 NLP、Perception | 五項：NLP、Navigate、Represent Knowledge、Reasoning、Perception |
| 3 | 人臉辨識步驟順序 | Detection → Recognition → Analysis | **Detection → Analysis → Recognition** |
| 4 | faceprint 性質 | 「每個人可以共用」 | 每人獨一無二，如指紋；可反向重建人臉 |
| 5 | 異常偵測指標 | 「看 accuracy 就好」 | 類別極不平衡 → 看 Precision/Recall/F1 |
| 6 | 影像資料形式 | 把「多鏡頭」當「3D」 | 多鏡頭＝多個 2D 視角；3D＝帶深度資料 |
| 7 | HMM 時間尺度 | 「用 1 秒一段」 | 用 **10 毫秒** 近似為平穩過程 |
| 8 | HMM 輸出 | 「輸出一個向量」 | 輸出**向量的序列**（sequence of vectors） |
| 9 | 語音辨識偏頗 | 「準確率是客觀中立的」 | 訓練資料偏頗 → 不同族群準確率落差 |
| 10 | 強化學習本質 | 「和監督式學習一樣有標準答案」 | 沒有標準答案，靠獎勵／懲罰試錯學出 policy |

### B.2 易混名詞對照

| 名詞 A | 名詞 B | 分辨方式 |
|--------|--------|---------|
| Human approach | Ideal approach | 像人 vs 理性 |
| Think | Act | 內部思考 vs 外部行為 |
| Detection | Recognition | 找出臉 vs 比對身份 |
| NLP | Speech Recognition | 處理語言（文字/語意） vs 處理語音訊號 |
| Generative AI | 一般辨識 AI | 生成新內容 vs 判斷既有內容 |
| Supervised learning | Reinforcement learning | 有標籤答案 vs 靠獎勵訊號 |

---

## 附錄 C：模擬試題（連答案）

### C.1 選擇題（20 題）

1. AI 的本質是？
   - A. 人類智慧
   - B. 機器智慧（machine intelligence）
   - C. 生物智慧
   - D. 群體智慧

2. 「Systems that act rationally」屬於哪個取徑？
   - A. Human approach
   - B. Ideal approach
   - C. Physical approach
   - D. Emotional approach

3. 下列何者**不是** AI 的子目標？
   - A. Natural Language Processing
   - B. Navigate
   - C. Blockchain
   - D. Reasoning

4. 人臉辨識的三個步驟順序是？
   - A. Analysis → Detection → Recognition
   - B. Detection → Recognition → Analysis
   - C. Detection → Analysis → Recognition
   - D. Recognition → Analysis → Detection

5. 「faceprint」的特性是？
   - A. 所有人共用
   - B. 每人獨一無二，如指紋
   - C. 只能儲存無法比對
   - D. 只適用於正面臉

6. 影像資料的「views from multiple cameras」是指？
   - A. 單張影像
   - B. 視訊序列
   - C. 多個 2D 視角
   - D. 三維點雲

7. 現代語音辨識系統最常依賴的模型是？
   - A. CNN
   - B. Hidden Markov Model (HMM)
   - C. Transformer
   - D. Decision Tree

8. HMM 假設語音訊號在足夠短的時間尺度下可近似為？
   - A. 隨機雜訊
   - B. 平穩過程（stationary process）
   - C. 週期訊號
   - D. 線性函數

9. 語音訊號在 HMM 中通常被切成多長的片段？
   - A. 1 毫秒
   - B. 10 毫秒
   - C. 100 毫秒
   - D. 1 秒

10. 每段語音片段的功率頻譜會被映射成？
   - A. 圖片
   - B. cepstral coefficients（實數向量）
   - C. 文字
   - D. 二進位碼

11. HMM 的最終輸出是？
   - A. 單一數值
   - B. 一張圖
   - C. 一串向量的序列
   - D. 一段文字

12. 強化學習中，agent 取得最多獎勵的「最佳策略」稱為？
   - A. Reward
   - B. Policy
   - C. Action
   - D. Environment

13. 下列何者是強化學習的應用？
   - A. AlphaGo 下圍棋
   - B. 垃圾郵件過濾
   - C. 網頁排版
   - D. 檔案壓縮

14. AlphaGo 由哪間公司開發，擊敗哪位世界冠軍？
   - A. Google / Kasparov
   - B. DeepMind / Lee Sedol
   - C. IBM / Kasparov
   - D. OpenAI / Lee Sedol

15. 生成式 AI 生成新內容主要依靠？
   - A. 隨機亂數
   - B. 機器學習，特別是深度學習
   - C. 人工規則手寫
   - D. 資料庫查詢

16. 生成式 AI 可生成的內容**不包含**下列何者？
   - A. 圖像
   - B. 文字
   - C. 音樂
   - D. 以上皆可生成

17. 異常偵測（Anomaly Detection）最常面對的資料特性是？
   - A. 類別完全平衡
   - B. 類別極不平衡
   - C. 全部都是異常
   - D. 沒有標籤

18. 異常偵測評估時，為何不宜只看 accuracy？
   - A. 因為計算太慢
   - B. 因為異常樣本極少，全猜正常也高分
   - C. 因為沒有公式
   - D. 因為需要 GPU

19. Speechmatics 對非裔美國人語音的準確率約為？
   - A. 68.6%
   - B. 82.8%
   - C. 45%
   - D. 95%

20. 「AI 助理、個人化購物、假評論偵測」屬於哪一類應用？
   - A. Education
   - B. Daily life
   - C. E-Commerce
   - D. Healthcare

<details><summary>C.1 答案</summary>

1. **B** 2. **B** 3. **C** 4. **C** 5. **B** 6. **C** 7. **B** 8. **B** 9. **B** 10. **B**
11. **C** 12. **B** 13. **A** 14. **B** 15. **B** 16. **D** 17. **B** 18. **B** 19. **B** 20. **C**

</details>

### C.2 填充題（10 題）

1. AI 的通用理論是：人工智慧擁有 ______ 智慧，但它是 ______ 智慧。
2. Human approach 包含「像人一樣 ______」與「像人一樣 ______」。
3. AI 的五個子目標：NLP、______、Represent Knowledge、______、Perception。
4. 人臉辨識三步：Detection → ______ → ______。
5. 人臉資料轉成的數字／點串稱為 ______，每人獨一無二，如 ______。
6. 現代語音辨識常用 ______（縮寫 ______）模型。
7. 語音訊號被切成 10 毫秒片段後，功率頻譜映射成 ______，其維度常為 ______ 至 32。
8. 強化學習中，agent 觀察 ______、執行動作、得到 ______，再學出最佳 policy。
9. DeepMind 的 ______ 擊敗圍棋世界冠軍 ______。
10. 生成式 AI 使用機器學習，特別是 ______，從既有資料學「模式與結構」。

<details><summary>C.2 答案</summary>

1. 類人（human-like）；機器（machine）
2. 思考（think）；行動（act）
3. Navigate；Reasoning
4. Analysis；Recognition
5. faceprint（臉紋）；指紋（fingerprint）
6. 隱馬可夫模型；HMM
7. cepstral coefficients（倒頻譜係數）；10
8. 環境（environment）；獎勵或懲罰（rewards/penalties）
9. AlphaGo；Lee Sedol（李世乭）
10. 深度學習（deep learning）

</details>

### C.3 簡答題（6 題）

1. 試述 Human approach 與 Ideal approach 的差別。
2. 列出 AI 的五個子目標並各舉一例。
3. 詳述人臉辨識的三個步驟。
4. 說明 HMM 在語音辨識中的處理流程（含時間尺度與輸出）。
5. 為何語音辨識對不同族群的準確率會有落差？如何改善？
6. 強化學習與監督式學習有何本質差異？

<details><summary>C.3 參考答案</summary>

1. **Human approach** 以「像人」為標準（think/act like humans）；**Ideal approach** 以「理性」為標準（think/act rationally），追求最佳解而非模仿人。
2. NLP（語音助理）、Navigate（GPS）、Represent Knowledge（知識圖譜）、Reasoning（專家系統）、Perception（電腦視覺）。
3. **Detection**：用電腦視覺在影像中找出人臉（含正／側面）；**Analysis**：讀取臉部幾何與表情，取 facial landmarks（眼距、額到下巴、鼻到嘴、眼窩深度、顴骨、輪廓）；**Recognition**：轉成 faceprint 並比對，評估吻合可能性。
4. 把語音切成 **10 毫秒** 片段（近似平穩過程）→ 求各片段**功率頻譜** → 映射成 **cepstral coefficients**（約 10～32 維）→ HMM 輸出**向量序列**。
5. 因為**大部分訓練資料需人手分類**，導致模型只在一小群說話者上準確；改善方向是使用**更具代表性的資料集**（如 Speechmatics 做法），使各族群準確率接近（例：非裔美國人語音 82.8% vs 68.6%）。
6. 監督式學習有**正確答案標籤**；強化學習**沒有標準答案**，agent 靠與環境互動得到的**獎勵／懲罰**回饋，試錯學出最大化長期獎勵的 **policy**。

</details>

---

## 附錄 D：教材頁面索引對照

| PDF 頁 | 標題 | 本筆記對應章節 |
|--------|------|---------------|
| 1 | 封面：Introduction to AI | — |
| 2 | 破冰：Do you actually like using an app to order food? | 第 1.1 節 |
| 3 | （圖片） | — |
| 4 | Sharing of Theory and Concepts / Can Machines Think more than us? | 第 1.1 節 |
| 5 | AI General Theory and Concepts | 第 1 節 |
| 6 | AI General Theory and Concepts（四象限） | 第 1 節 |
| 7 | AI Applications and Examples Sharing（章節頁） | 第 3 節 |
| 8 | Sub-objectives of AI | 第 2 節 |
| 9 | AI Applications：E-Commerce / Education / Daily life | 第 3 節 |
| 10 | Anomaly Detection | 第 4 節 |
| 11 | Image/Video Recognition（定義＋四種資料形式） | 第 5.1 節 |
| 12 | Image/Video Recognition（電腦視覺任務） | 第 5.2 節 |
| 13 | Facial Recognition — Detection | 第 6.1 節 |
| 14 | Facial Recognition — Analysis | 第 6.2 節 |
| 15 | Facial Recognition — Recognition | 第 6.3 節 |
| 16 | E channel（圖片） | — |
| 17 | NLP — 三個問題 | 第 7.1 節 |
| 18 | NLP — Hidden Markov Model | 第 7.2 節 |
| 19 | NLP — HMM 流程 | 第 7.2 節 |
| 20 | NLP（圖） | 第 7 節 |
| 21 | Speech Recognition — King/Queen/Man/Woman/Royal | 第 8.1 節 |
| 22 | NLP（圖） | 第 7 節 |
| 23 | NLP（圖） | 第 7 節 |
| 24 | Speech Recognition（圖） | 第 8 節 |
| 25 | NLP（圖） | 第 7 節 |
| 26 | NLP — Explore（aka.ms/explore-nlp） | 第 7.4 節 |
| 27 | Speech Recognition — Speechmatics 數據 | 第 8.2 節 |
| 28 | （圖） | — |
| 29 | Reinforcement Learning — 要解決的問題 | 第 9.1 節 |
| 30 | Reinforcement Learning（圖） | 第 9 節 |
| 31 | Reinforcement Learning（圖） | 第 9 節 |
| 32 | Reinforcement Learning — Agent 四步 | 第 9.2 節 |
| 33 | Reinforcement Learning — 應用（AlphaGo） | 第 9.3 節 |
| 34 | Generative AI — 定義 | 第 10 節 |

> 說明：原稿有多頁為純圖片／示意圖（如 p3、p16、p20、p22–25、p28、p30–31），
> 這些頁面在筆記中對應到所屬章節的概念補充，不另設小節。

---

## 附錄 E：延伸資源與離線提示

### E.1 原稿提供的連結

| 資源 | 連結 |
|------|------|
| 探索 NLP | `https://aka.ms/explore-nlp` |

### E.2 沒有網路時怎麼複習

本筆記本身即為**離線可讀**（Markdown 或單檔 HTML），不依賴任何外部資源。若要自行查找延伸資料：

- 先看本筆記的附錄 A（名詞速查表）與附錄 F（一頁精華）。
- 用附錄 C 的試題自測，把答錯的題目對應回章節重讀。
- 需要圖解時，可用任何繪圖工具自行畫出：AI 子目標圖、人臉辨識三步圖、RL 迴圈圖。

### E.3 觀念延伸（考綱外但常被問）

| 主題 | 一句話 |
|------|--------|
| AI 公平性 | 訓練資料不具代表性 → 各族群表現落差（見 8.2） |
| AI 倫理／隱私 | 人臉資料可反向重建（見 6.3），涉及隱私 |
| 監督式 vs 強化式 | 有標籤 vs 靠獎勵（見附錄 B.2） |

---

## 附錄 F：一頁精華（考前 10 分鐘）

```text
【1. AI 定義】
  AI = 類人智慧(human-like) 但本質是機器智慧(machine intelligence)
  取徑：Human(think/act like humans) | Ideal(think/act rationally)

【2. AI 子目標（5 個）】
  NLP / Navigate / Represent Knowledge / Reasoning / Perception

【3. AI 應用】
  E-Commerce：個人化購物、AI 助理、詐騙防治(假評論)
  Education：個人化訊息、招生管理、批改
  Daily life：自駕(Tesla)、垃圾郵件過濾、人臉辨識(Face Unlock)、GPS

【4. 異常偵測】
  找 outlier；類別極不平衡 → 看 Precision/Recall/F1，不看 accuracy

【5. 影像/視訊辨識】
  輸入影像 → 輸出屬性；資料形式：單張 / 序列 / 多鏡頭 / 3D

【6. 人臉辨識（三步，必考）】
  Detection → Analysis → Recognition
  Analysis 量：眼距、額到下巴、鼻到嘴、眼窩深度、顴骨、唇耳下巴輪廓
  faceprint = 每人獨一無二（如指紋），可反向重建人臉

【7. NLP】
  三件事：speak / understand / make sense
  HMM：語音切 10ms → 功率頻譜 → cepstral coefficients(10~32維) → 向量序列

【8. 語音辨識】
  訓練資料需人手分類 → 族群落差
  Speechmatics 82.8% vs Google/Amazon 68.6%（非裔美國人語音）
  = 錯誤減少 45%（約 3 個字）

【9. 強化學習】
  Agent：observe → act → reward/penalty → 學最佳 policy（最大化長期獎勵）
  應用：機械人學走路、DeepMind AlphaGo 擊敗 Lee Sedol（圍棋）

【10. 生成式 AI】
  用 ML/深度學習，從既有資料學模式與結構 → 生成相似新內容（圖/文/樂/影片）
```

---

## 附錄 G：MC 模擬試卷（60 題）

### G.1 作答說明與應試技巧

- **60 題單選**、滿分 60 分、建議 **75 分鐘**。
- 分三部分：**基礎與 AI 概念（1–20）**、**影像與人臉辨識（21–40）**、**NLP／語音／強化學習／生成式（41–60）**。
- 答案分佈刻意打散（A/B/C/D 各 15 題），避免整排猜同一個字母。
- 建議先做完整份再看答案；答錯的題目請用「逐題詳解」對應回章節重讀。

### G.2 第一部分：基礎與 AI 概念（第 1–20 題）

1. 人工智慧（AI）的本質是？
   - A. 人類智慧
   - B. 機器智慧（machine intelligence）
   - C. 群體智慧
   - D. 生物智慧

2. 「Systems that think like humans」屬於哪個取徑？
   - A. Ideal approach
   - B. Rational approach
   - C. Human approach
   - D. Machine approach

3. 下列何者最能描述 Ideal approach？
   - A. 理性地思考與行動
   - B. 像人一樣思考
   - C. 模仿人類的偏誤
   - D. 只做感知不做推理

4. AI 的子目標共有幾個？
   - A. 3
   - B. 4
   - C. 6
   - D. 5

5. 下列何者**不是** AI 的子目標？
   - A. Navigate
   - B. Perception
   - C. Blockchain
   - D. Reasoning

6. 「偵測假評論（fake review）」屬於哪一類 AI 應用？
   - A. Education
   - B. E-Commerce 的詐騙防治
   - C. Daily life
   - D. Healthcare

7. 「Grading paperwork」屬於哪一類 AI 應用？
   - A. Education
   - B. E-Commerce
   - C. Daily life
   - D. Manufacturing

8. 下列何者屬於 Daily life 的 AI 應用？
   - A. Managing enrollment
   - B. Personalized shopping
   - C. Fraud prevention
   - D. Spam email filters

9. 異常偵測（Anomaly Detection）主要在找？
   - A. 最多的類別
   - B. 平均值
   - C. 不符合預期模式的 outlier
   - D. 最大群組

10. 評估異常偵測模型時，為何不宜只看 accuracy？
    - A. 因為公式太複雜
    - B. 因為異常樣本極少，全猜正常也會很高分
    - C. 因為需要 GPU
    - D. 因為 accuracy 沒有定義

11. 原稿指出電腦視覺辨識的準確度？
    - A. 一定低於人類
    - B. 只能達到人類一半
    - C. 無法比較
    - D. 可達或超越人類水準

12. 原稿列出的影像資料形式共有幾種？
    - A. 4
    - B. 3
    - C. 5
    - D. 2

13. 「Views from multiple cameras」是指？
    - A. 單張影像
    - B. 視訊序列
    - C. 多個 2D 視角
    - D. 三維點雲

14. 下列何者最適合代表「Three-dimensional data」？
    - A. 一張 JPEG
    - B. LiDAR／深度相機的點雲
    - C. 一段 MP4
    - D. 兩台相機的 2D 影像

15. 電腦視覺任務的輸入／輸出介面是？
    - A. 輸入影像 → 輸出描述影像的屬性
    - B. 輸入文字 → 輸出影像
    - C. 輸入聲音 → 輸出文字
    - D. 輸入屬性 → 輸出影像

16. 「Can Machines Think more than us?」在原稿中屬於？
    - A. 期末考題
    - B. 生成式 AI 定義
    - C. 人臉辨識步驟
    - D. 開場破冰引導

17. 「AI-powered Assistants」屬於哪一類應用？
    - A. Education
    - B. E-Commerce
    - C. Daily life
    - D. Agriculture

18. 「Navigation by GPS」屬於哪一類應用？
    - A. E-Commerce
    - B. Education
    - C. Daily life
    - D. Finance

19. AI 子目標「Represent Knowledge」的意思是？
    - A. 把知識用機器可處理的方式表示
    - B. 從感測資料理解世界
    - C. 規劃路徑
    - D. 生成新內容

20. AI 子目標「Reasoning」的意思是？
    - A. 感測環境
    - B. 產生語音
    - C. 儲存影像
    - D. 由已知推導出新結論

---

### G.3 第二部分：影像與人臉辨識（第 21–40 題）

21. 人臉辨識的三個步驟，正確順序是？
    - A. Analysis → Detection → Recognition
    - B. Detection → Recognition → Analysis
    - C. Detection → Analysis → Recognition
    - D. Recognition → Analysis → Detection

22. 「Detection」在人臉辨識中的意思是？
    - A. 在影像中找出人臉
    - B. 比對兩個人的身份
    - C. 生成人臉影像
    - D. 儲存人臉資料庫

23. 原稿指出 Detection 可偵測的臉部資料包含？
    - A. 只有正面
    - B. 只有側面
    - C. 只有戴眼鏡的臉
    - D. 正面與側面

24. 「Analysis」這一步會做什麼？
    - A. 下載人臉圖片
    - B. 讀取臉部幾何與表情
    - C. 刪除人臉資料
    - D. 加密人臉檔案

25. 下列何者**不是**原稿列出的 Analysis 量測項目？
    - A. 兩眼之間的距離
    - B. 顴骨形狀
    - C. 髮色與身高的比例
    - D. 眼窩深度

26. 「眼窩深度」的英文是？
    - A. Depth of the eye sockets
    - B. Distance between the eyes
    - C. Shape of the cheekbones
    - D. Contour of the lips

27. 「faceprint」是什麼？
    - A. 一張列印出來的人臉照片
    - B. 人臉的密碼
    - C. 人臉的英文名稱
    - D. 臉部資料轉成的數字或點串

28. 原稿把 faceprint 比喻為？
    - A. 身分證號
    - B. 指紋（fingerprint）
    - C. 車牌
    - D. 條碼

29. faceprint 資料「反向使用」可以做到？
    - A. 數位重建一個人的臉
    - B. 預測天氣
    - C. 翻譯語言
    - D. 壓縮影片

30. 「Recognition」這一步的核心是？
    - A. 偵測影像中是否有臉
    - B. 分析臉部表情
    - C. 比對兩張（或以上）影像中的臉，評估吻合可能性
    - D. 把人臉轉成 3D 模型

31. 下列何者是人臉辨識的日常應用例子？
    - A. 垃圾郵件過濾
    - B. GPS 導航
    - C. 招生管理
    - D. iPhone Face Unlock

32. 「Video sequences」指的是哪一種影像資料形式？
    - A. 單張影像
    - B. 連續影格（視訊序列）
    - C. 多鏡頭視角
    - D. 三維資料

33. 原稿指出電腦視覺能自動化處理影像資料的哪些面向？
    - A. 擷取、分析、分類與理解
    - B. 上傳、下載、備份、刪除
    - C. 加密、解密、簽章、壓縮
    - D. 列印、掃描、影印、傳真

34. 下列何者屬於「Three-dimensional data」？
    - A. 一張 PNG
    - B. 一段 GIF
    - C. 深度相機的點雲
    - D. 一張身分證照片

35. 人臉辨識最直接對應到 AI 的哪個子目標？
    - A. Navigate
    - B. Reasoning
    - C. Represent Knowledge
    - D. Perception

36. Detection 主要依靠什麼技術在影像中找出人臉？
    - A. 資料庫查詢
    - B. 電腦視覺（computer vision）
    - C. 語音辨識
    - D. 隨機抽樣

37. Analysis 找出能把臉與其他物件區分開的什麼？
    - A. 臉部特徵點（facial landmarks）
    - B. 指紋
    - C. 車牌號碼
    - D. 姓名

38. 「額頭到下巴的距離」英文是？
    - A. Distance between the eyes
    - B. Depth of the eye sockets
    - C. Distance from the forehead to the chin
    - D. Shape of the cheekbones

39. 用自拍比對政府證件照是否為同一人，屬於人臉辨識的哪一步？
    - A. Detection
    - B. Analysis
    - C. Compression
    - D. Recognition

40. 人臉辨識中用來「評估吻合可能性」的步驟是？
    - A. Detection
    - B. Recognition
    - C. Analysis
    - D. Pre-processing

---

### G.4 第三部分：NLP、語音、強化學習、生成式（第 41–60 題）

41. 原稿用哪三件事概括 NLP？
    - A. 講語言、懂語言、理解句子
    - B. 讀、寫、算
    - C. 拍照、剪片、上傳
    - D. 加密、解密、壓縮

42. NLP 中「make sense out of a sentence」指的是？
    - A. 把句子唸出來
    - B. 把句子翻譯成外語
    - C. 從句子理解出意義（語意理解）
    - D. 把句子刪掉

43. 原稿指出大多數現代語音辨識系統依賴？
    - A. Decision Tree
    - B. Hidden Markov Model (HMM)
    - C. K-means
    - D. Random Forest

44. HMM 的關鍵假設是：語音訊號在足夠短的時間尺度下可近似為？
    - A. 週期訊號
    - B. 隨機雜訊
    - C. 線性函數
    - D. 平穩過程（stationary process）

45. HMM 通常把語音訊號切成多長的片段？
    - A. 10 毫秒
    - B. 1 毫秒
    - C. 100 毫秒
    - D. 1 秒

46. 每個語音片段的功率頻譜會被映射成什麼？
    - A. 一張圖片
    - B. 一段文字
    - C. cepstral coefficients（實數向量）
    - D. 一組標籤

47. 原稿提到 cepstral coefficients 向量的維度通常？
    - A. 固定 512 維
    - B. 約 10 至 32 維
    - C. 只有 1 維
    - D. 至少 1024 維

48. HMM 的最終輸出是？
    - A. 單一數字
    - B. 一張頻譜圖
    - C. 一段文字
    - D. 一串向量的序列

49. 原稿以 King / Queen / Man / Woman 示範的概念是？
    - A. 詞向量（word embedding）
    - B. 影像分割
    - C. 物件偵測
    - D. 語音合成

50. Speechmatics 對非裔美國人語音的整體準確率約為？
    - A. 45%
    - B. 68.6%
    - C. 82.8%
    - D. 99%

51. Google 與 Amazon 對非裔美國人語音的準確率約為？
    - A. 82.8%
    - B. 68.6%
    - C. 45%
    - D. 95%

52. Speechmatics 的準確率提升相當於減少多少語音辨識錯誤？
    - A. 10%
    - B. 25%
    - C. 68%
    - D. 45%

53. 原稿指出語音辨識的一大挑戰是？
    - A. 大部分訓練資料需要人手分類，導致代表性不足
    - B. 麥克風太貴
    - C. 語音檔太大
    - D. 沒有數學模型可用

54. 強化學習中，agent 的第一步是？
    - A. 得到獎勵
    - B. 更新策略
    - C. 觀察環境
    - D. 結束任務

55. 強化學習中 agent 學到的「最佳行動準則」稱為？
    - A. Reward
    - B. Policy
    - C. Environment
    - D. Dataset

56. 強化學習的目標是？
    - A. 單步獎勵最大化
    - B. 讓動作越多越好
    - C. 最小化觀察次數
    - D. 長期累積獎勵最大化

57. DeepMind 的 AlphaGo 擊敗了哪位世界冠軍？
    - A. Lee Sedol（李世乭）
    - B. Garry Kasparov
    - C. Magnus Carlsen
    - D. Ke Jie

58. AlphaGo 是哪間公司（團隊）開發的？
    - A. OpenAI
    - B. IBM
    - C. DeepMind
    - D. Microsoft

59. 原稿指出生成式 AI 可以生成下列哪些內容？
    - A. 只能生成圖像
    - B. 圖像、文字、音樂，甚至影片
    - C. 只能生成文字
    - D. 只能生成音樂

60. 生成式 AI 生成新內容主要使用的技術是？
    - A. 人工規則手寫
    - B. 資料庫查詢
    - C. 隨機亂數
    - D. 機器學習，特別是深度學習

---

### G.5 答案速查表

| 題 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 答 | B | C | A | D | C | B | A | D | C | B |

| 題 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 答 | D | A | C | B | A | D | B | C | A | D |

| 題 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|
| 答 | C | A | D | B | C | A | D | B | A | C |

| 題 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|
| 答 | D | B | A | C | D | B | A | C | D | B |

| 題 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|
| 答 | A | C | B | D | A | C | B | D | A | C |

| 題 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 59 | 60 |
|---|---|---|---|---|---|---|---|---|---|---|
| 答 | B | D | A | C | B | D | A | C | B | D |

**分數換算**：每題 1 分，滿分 60 分。答錯題目請對照下方詳解回到章節重讀。

### G.6 逐題詳解

**1. B** —— AI 的通用理論：擁有類人智慧，但本質是**機器智慧**（§1）。
**2. C** —— think like humans 屬 **Human approach**（§1）。
**3. A** —— Ideal approach = 理性地思考與行動（think/act rationally）（§1）。
**4. D** —— 五個：NLP、Navigate、Represent Knowledge、Reasoning、Perception（§2）。
**5. C** —— Blockchain 不是 AI 子目標（§2）。
**6. B** —— 假評論偵測屬 E-Commerce 的 Fraud Prevention（§3.1）。
**7. A** —— Grading paperwork 屬 Education（§3.2）。
**8. D** —— Spam email filters 屬 Daily life（§3.3）。
**9. C** —— 異常偵測找 outlier（§4）。
**10. B** —— 異常極少，全猜正常 accuracy 也高，應看 Precision/Recall/F1（§4）。
**11. D** —— 電腦視覺準確度可達或超越人類（§5）。
**12. A** —— 四種：單張／序列／多鏡頭／3D（§5.1）。
**13. C** —— multiple cameras = 多個 2D 視角（§5.1）。
**14. B** —— 3D data 如 LiDAR／深度相機點雲（§5.1）。
**15. A** —— 輸入影像 → 輸出屬性（§5.2）。
**16. D** —— 屬開場破冰引導（§1.1）。
**17. B** —— AI-powered Assistants 屬 E-Commerce（§3.1）。
**18. C** —— Navigation by GPS 屬 Daily life（§3.3）。
**19. A** —— Represent Knowledge＝把知識用機器可處理方式表示（§2）。
**20. D** —— Reasoning＝由已知推導新結論（§2）。
**21. C** —— Detection → Analysis → Recognition（§6）。
**22. A** —— Detection＝在影像中找出人臉（§6.1）。
**23. D** —— 可偵測正面與側面（§6.1）。
**24. B** —— Analysis 讀取臉部幾何與表情（§6.2）。
**25. C** —— 髮色與身高比例不在量測項目（§6.2）。
**26. A** —— 眼窩深度 = depth of the eye sockets（§6.2）。
**27. D** —— faceprint＝臉部資料轉成的數字／點串（§6.3）。
**28. B** —— 比喻為指紋 fingerprint（§6.3）。
**29. A** —— 可反向數位重建人臉（§6.3）。
**30. C** —— Recognition＝比對臉並評估吻合可能性（§6.3）。

**31. D** —— iPhone Face Unlock 是人臉辨識的日常應用（§3.3／§6）。
**32. B** —— Video sequences＝連續影格（§5.1）。
**33. A** —— 擷取、分析、分類與理解（§5）。
**34. C** —— 深度相機點雲屬 3D 資料（§5.1）。
**35. D** —— 人臉辨識屬 Perception（§2／§6）。
**36. B** —— Detection 由 computer vision 支援（§6.1）。
**37. A** —— Analysis 找 facial landmarks（§6.2）。
**38. C** —— 額到下巴 = distance from the forehead to the chin（§6.2）。
**39. D** —— 自拍比對證件照屬 Recognition（§6.3）。
**40. B** —— 評估吻合可能性＝Recognition（§6.3）。
**41. A** —— NLP 三件事：講、懂、理解句子（§7.1）。
**42. C** —— make sense out of a sentence＝語意理解（§7.1）。
**43. B** —— 現代語音辨識依賴 HMM（§7.2）。
**44. D** —— 近似為平穩過程 stationary process（§7.2）。
**45. A** —— 切成 10 毫秒片段（§7.2）。
**46. C** —— 映射成 cepstral coefficients（§7.2）。
**47. B** —— 維度約 10 至 32（§7.2）。
**48. D** —— 輸出為向量序列（§7.2）。
**49. A** —— King/Queen/Man/Woman 示範 word embedding（§8.1）。
**50. C** —— Speechmatics 準確率 82.8%（§8.2）。
**51. B** —— Google/Amazon 準確率 68.6%（§8.2）。
**52. D** —— 錯誤減少 45%（約 3 個字）（§8.2）。
**53. A** —— 訓練資料需人手分類 → 代表性不足（§8.2）。
**54. C** —— agent 先觀察環境（§9.2）。
**55. B** —— 最佳行動準則＝policy（§9.2）。
**56. D** —— 目標是長期累積獎勵最大化（§9.2）。
**57. A** —— AlphaGo 擊敗 Lee Sedol（李世乭）（§9.3）。
**58. C** —— AlphaGo 由 DeepMind 開發（§9.3）。
**59. B** —— 圖像、文字、音樂，甚至影片（§10）。
**60. D** —— 機器學習，特別是深度學習（§10）。

---

## 附錄 H：答錯題目 → 複習章節對照

| 答錯題號 | 建議複習章節 |
|---|---|
| 1–5 | §1 AI 定義與取徑、§2 子目標 |
| 6–8 | §3 AI 應用分類 |
| 9–10 | §4 異常偵測 |
| 11–15 | §5 影像／視訊辨識 |
| 16–20 | §1.1 破冰、§2 子目標 |
| 21–30 | §6 人臉辨識（三步、faceprint） |
| 31–35 | §3 應用、§5 影像形式、§2 子目標 |
| 36–40 | §6.1–6.3 人臉辨識細節 |
| 41–48 | §7 NLP 與 HMM |
| 49–53 | §8 語音辨識與偏頗議題 |
| 54–58 | §9 強化學習 |
| 59–60 | §10 生成式 AI |

---

*本篇為個人學習筆記整理，教材內容版權屬匯縱專業發展中心（IVDC）所有。*
