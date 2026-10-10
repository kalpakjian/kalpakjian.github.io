# Introduction to Computer Vision and Application 學習筆記（考試溫習版）

> 課程：Certificate in Application of Computer Vision Technology (Part-time)
> 機構：匯縱專業發展中心（IVDC）
> 教材來源：`2 IVDC_Introduction to Computer Vision and Application.pptx` → PDF（12 頁）
> 本筆記按 PDF 原稿每一個標題逐一填充內容，並補上定義、關鍵數字、常見錯誤、模擬試題。
> 原稿多為投影片圖示，文字較少；本筆記補上「圖示背後的概念」與「考點」，方便理解與應試。
> 🖱️ **互動測驗（推薦）**：附錄 F 提供 **60 題線上測驗**（即時計分、進度自動儲存）→ **[開始作答](mc-quiz.html)**

---

## 目錄

| # | 章節 | PDF 頁 |
|---|------|--------|
| 1 | [商業領域的真實案例（Real Case Examples）](#1-商業領域的真實案例real-case-examples) | 2–6 |
| 2 | [中國大陸與香港的最新 AI 技術](#2-中國大陸與香港的最新-ai-技術) | 7 |
| 3 | [卷積神經網路 CNN 是什麼](#3-卷積神經網路-cnn-是什麼) | 8 |
| 4 | [CNN 為何是頂尖方法（State-of-the-art）](#4-cnn-為何是頂尖方法state-of-the-art) | 9 |
| 5 | [關鍵概念：參數重用（re-use parameters）](#5-關鍵概念參數重用re-use-parameters) | 10 |
| 6 | [CNN 基本概念與影像辨識](#6-cnn-基本概念與影像辨識) | 11–12 |
| A | [附錄 A：名詞速查表](#附錄-a名詞速查表) | — |
| B | [附錄 B：常見錯誤與陷阱](#附錄-b常見錯誤與陷阱) | — |
| C | [附錄 C：教材頁面索引對照](#附錄-c教材頁面索引對照) | — |
| D | [附錄 D：延伸資源與離線提示](#附錄-d延伸資源與離線提示) | — |
| E | [附錄 E：一頁精華（考前 10 分鐘）](#附錄-e一頁精華考前-10-分鐘) | — |
| F | [附錄 F：互動式線上測驗（60 題）](#附錄-f互動式線上測驗60-題) | — |
| G | [附錄 G：互動測驗答錯題目 → 複習章節對照](#附錄-g互動測驗答錯題目--複習章節對照) | — |

---

## 0. 30 秒總複習（考前最後掃描）

```
電腦視覺（Computer Vision）
  ├─ 商業應用：零售、安防、工業檢測、醫療、自駕、農業…
  ├─ 2024 世界機器人大會：超現實圍棋博弈（人機對弈展示）
  └─ 核心技術：CNN（卷積神經網路）
        ├─ 定義：處理「網格狀資料」（影像、音訊）的神經網路
        ├─ 關鍵：卷積層自動學習「階層式特徵」（由低階到高階）
        ├─ 架構：encoder（多個逐漸變窄的 block 堆疊 →「deep」）
        └─ 核心思想：參數重用（parameter sharing）
```

| 你會用到的關鍵詞 | 一句話記法 |
|---|---|
| Computer Vision | 讓機器「看懂」影像與影片 |
| Commercial sectors | 零售、安防、工業、醫療、自駕等真實案例 |
| World Robot Conference | 2024 世界機器人大會（超現實圍棋博弈） |
| CNN | 卷積神經網路，專為**網格狀資料**設計 |
| Grid-like structure | 影像（像素網格）、音訊（時頻網格） |
| Convolutional layer | 自動學習階層式表徵、抽取特徵 |
| Hierarchical representations | 低階邊緣 → 中階紋理 → 高階物件 |
| Encoder | 由多個 block 堆疊，負責學統計模式 |
| Deep | 許多「逐漸變窄」的 block 堆疊而成 |
| Parameter sharing | 同一組卷積核在整張影像上重複使用（參數重用） |
| 3×3 convolution on 5×5 image | 經典示範：小核掃過大圖，共享權重 |
| State-of-the-art | 目前最佳方法；影像／影片辨識的骨幹 |

---

## 1. 商業領域的真實案例（Real Case Examples）

原稿 p2–6 標題為「**Real Case Examples in Commercial Sectors**」，逐頁以**圖片**展示電腦視覺在
商業領域的實際應用（原稿文字極少，以下補上每類應用的技術與案例）。

### 1.1 電腦視覺在商業上的六大類應用

| 領域 | 典型應用 | 背後的 CV 技術 |
|------|----------|----------------|
| 零售 Retail | 人流統計、貨架缺貨偵測、無人商店、顧客行為分析 | 物件偵測、人體追蹤、影像分類 |
| 安防／監控 Security | 人臉辨識門禁、異常行為偵測、車牌辨識（ANPR） | 人臉辨識、動作辨識、OCR |
| 工業／製造 Industry | 瑕疵檢測（defect detection）、尺寸量測、自動分揀 | 影像分割、模板匹配、異常偵測 |
| 醫療 Medical | 醫學影像判讀（X 光／CT／MRI）、病灶標註 | 影像分類、語意分割 |
| 交通／自駕 Autonomous | 車道線偵測、行人偵測、交通號誌辨識 | 物件偵測、語意分割、光流 |
| 農業 Agriculture | 病蟲害辨識、果實成熟度分級、無人機巡田 | 影像分類、物件偵測 |

### 1.2 為什麼商業上要用電腦視覺

- **速度與一致性**：機器可 24 小時不間斷，且判斷標準一致（不會疲勞、不會情緒波動）。
- **準確度**：在特定任務上可達或超越人類水準（例如瑕疵檢測）。
- **成本**：長期可取代大量重複性的目視檢查人力。
- **可量化**：所有判斷都有數據紀錄，便於追溯與改善。

> **考點**：能判斷「某案例屬於哪一類商業應用」。例如：
> **無人商店** → 零售；**車牌辨識** → 安防；**瑕疵檢測** → 工業；**X 光判讀** → 醫療；
> **車道線偵測** → 自駕；**果實分級** → 農業。

---

## 2. 中國大陸與香港的最新 AI 技術

原稿 p7 標題為「**Latest AI technologies in Mainland China and Hong Kong**」，
並以「**Furthermore**」帶出一個具體例子：

> **世界机器人大会：超现实围棋博弈 2024 World Robot Conference: Hyper-realistic Go Match**

### 2.1 世界機器人大會（World Robot Conference, WRC）

- 在**中國北京**舉行的年度機器人與 AI 盛會，展示最新機器人與人工智慧技術。
- 2024 年的展示包含「**超現實圍棋博弈**」（Hyper-realistic Go Match）——
  由**人形機器人**與人（或機器人之間）對弈圍棋，展示感知、決策與精細動作控制能力。

### 2.2 圍棋為什麼是 AI 的經典試金石

| 項目 | 說明 |
|------|------|
| 複雜度 | 圍棋的合法局面數遠超西洋棋，**無法用暴力搜尋**窮舉 |
| 2016 里程碑 | DeepMind 的 **AlphaGo** 擊敗世界冠軍 **Lee Sedol（李世乭）** |
| 2017 | **AlphaGo Zero** 只靠自我對弈（self-play）就能超越人類 |
| 2018+ | 機械手臂 + 視覺系統讓「實體」機器人也能下棋（感知 + 控制） |

> **考點**：記住「**2024 World Robot Conference**」與「**Hyper-realistic Go Match**」的對應；
> 以及中國大陸／香港是 AI 與機器人技術的重要發展與展示地區。

---

## 3. 卷積神經網路 CNN 是什麼

原稿 p8 給出定義（**AI Basic Principles – Convolutional Neural Network**）：

> **Convolutional Neural Network (CNN)** 是一種**專門為處理與分析「網格狀結構」（grid-like structure）
> 資料**（例如**影像**或**音訊**）而設計的神經網路。
> 它使用**卷積層（convolutional layers）**來自動學習**階層式表徵（hierarchical representations）**
> 並從輸入資料中**抽取特徵（extract features）**。

### 3.1 定義拆解

| 關鍵詞 | 英文 | 說明 |
|--------|------|------|
| 網格狀結構 | grid-like structure | 影像＝像素的 2D 網格；音訊＝時頻的 2D 網格 |
| 卷積層 | convolutional layer | CNN 的核心運算層，負責掃描與抽特徵 |
| 階層式表徵 | hierarchical representations | 由低階到高階的特徵層次 |
| 抽取特徵 | extract features | 不需人工設計特徵，模型自己學 |

### 3.2 什麼是「階層式」特徵

```
輸入影像
  └─ 低階特徵：邊緣、線條、角點
        └─ 中階特徵：紋理、圓形、局部形狀
              └─ 高階特徵：眼睛、車輪、人臉等「物件部件」
                    └─ 整體：可辨識的物件類別
```

> **考點**：CNN 定義的兩個關鍵字是「**grid-like structure**」與「**hierarchical representations**」；
> 常見陷阱：把 CNN 說成「只能處理影像」——原稿明講也包含**音訊**等網格狀資料。

---

## 4. CNN 為何是頂尖方法（State-of-the-art）

原稿 p9 標題為「**CNN**」，內容是「**AI Basic Principles – Convolutional Neural Network**」的延伸：

> - **State-of-the-art methods** —— 使用**神經網路**來辨識影像與影片。
> - 適合影像辨識的**深度學習架構**，都是基於 **CNN 的各種變體（variations）**。
> - 一切從 **encoder** 開始：encoder 是**由一層層「block」組成的模組**，
>   負責學習**影像像素中與待預測標籤相對應的統計模式**。
> - 高效能的 encoder 設計，會把**許多「逐漸變窄（narrowing）」的 block 堆疊起來**，
>   這正是「**深度神經網路（deep neural networks）**」中「**deep**」的由來。

### 4.1 三個重點拆解

| 重點 | 說明 |
|------|------|
| 主流方法 | 影像／影片辨識的 SOTA 都是**神經網路**，且幾乎都是 **CNN 的變體** |
| Encoder 的角色 | 學習**像素 → 標籤**之間的統計模式（即「抽特徵」） |
| 「Deep」的由來 | **許多 narrowing blocks 堆疊**，層數越深、表徵越抽象 |

### 4.2 為什麼要「逐漸變窄（narrowing）」

```
輸入影像 (H×W×3)
  → block 1  (較大空間、較少通道)   例如 224×224×64
  → block 2  (空間變小、通道變多)   例如 112×112×128
  → block 3                         例如  56×56×256
  → ...  空間持續縮小、通道持續增加（語意更抽象）
  → 最後 → 分類器 → 標籤
```

- **空間維度變小**：把區域資訊「壓縮」成更抽象的概念。
- **通道維度變大**：用更多「特徵圖」表達更豐富的語意。

> **考點**：「**deep** 的定義＝許多逐漸變窄的 block 堆疊」、「encoder 學的是**像素與標籤之間的統計模式**」。

---

## 5. 關鍵概念：參數重用（re-use parameters）

原稿 p10 只有三行，但這是 CNN 的**核心思想**：

> - **Key idea: re-use parameters**（關鍵思想：參數重用）
> - **Convolution shares parameters**（卷積會共享參數）
> - **Example: 3×3 convolution on a 5×5 image**（範例：在 5×5 影像上做 3×3 卷積）

### 5.1 什麼是「參數重用／共享」

同一個**卷積核（kernel／filter）**在整張影像上**滑動**，每個位置都用**同一組權重**計算。
換句話說：**一組參數，全圖共用**。

| 對比 | 全連接層（Fully Connected） | 卷積層（Convolution） |
|------|---------------------------|----------------------|
| 參數數量 | 每個輸入像素 → 每個輸出都要一組權重（**極多**） | 只用**一個小核**的權重（**極少**） |
| 位置概念 | 沒有（打平成一維） | 保留**空間相鄰關係** |
| 平移不變性 | 無 | **有**（同一特徵出現在哪都認得） |

### 5.2 範例：5×5 影像 + 3×3 卷積核

```
5×5 輸入影像            3×3 卷積核（9 個權重，全圖共用）
1 2 3 0 1              1 0 1
0 1 2 3 1              0 1 0
1 0 1 2 0              1 0 1
2 1 0 1 2
0 1 2 1 0
```

- 卷積核在影像上**逐格滑動**（stride＝1），每停一格就把重疊區域做**逐元素相乘再相加**。
- 輸出尺寸（無 padding、stride＝1）：**5 − 3 + 1 = 3** → 得到 **3×3** 的特徵圖。
- 整個過程**只用 9 個權重**（外加 1 個 bias），這就是「參數重用」的威力。

| 參數 | 公式（無 padding） |
|------|-------------------|
| 輸出邊長 | `(W − K) / S + 1`（W＝輸入邊長、K＝核邊長、S＝stride） |
| 本例 | `(5 − 3) / 1 + 1 = 3` |

> **考點**：CNN 的關鍵思想是「**re-use parameters / share parameters**」；
> 能算出 5×5 影像經 3×3 卷積（stride 1、無 padding）得到 **3×3**。
> 常見陷阱：誤以為卷積核每個位置都換一組權重（那是全連接層的做法）。

---

## 6. CNN 基本概念與影像辨識

原稿 p11–12 標題為「**Basic Concepts of CNN**」：

> - p11：**AI Basic Principles – Image Recognition by CNN** →「**What is CNN?**」
> - p12：**AI Basic Principles – Convolutional Neural Network**

### 6.1 CNN 的基本組成

| 元件 | 英文 | 作用 |
|------|------|------|
| 卷積層 | Convolutional layer | 用卷積核抽特徵（共享參數） |
| 激活函數 | Activation（ReLU） | 加入非線性（負值歸零） |
| 池化層 | Pooling（Max / Average） | 降採樣、縮小尺寸、保留主要特徵 |
| 全連接層 | Fully Connected | 把特徵整合成最終分類 |
| Softmax | Softmax | 輸出各類別機率 |

### 6.2 一張圖走完 CNN（影像辨識流程）

```
輸入影像 → [卷積 → ReLU → 池化] × N → 展平 → 全連接 → Softmax → 類別機率
             ↑ 抽特徵（低階→高階）              ↑ 分類
```

### 6.3 為什麼 CNN 特別適合影像

1. **局部連接（local connectivity）**：鄰近像素關係最強，卷積只看局部。
2. **參數共享（parameter sharing）**：同一特徵在影像各處都能被偵測到。
3. **平移不變性（translation invariance）**：物件左右移動仍能辨識。
4. **階層式特徵（hierarchy）**：自動從邊緣學到物件。

> **考點**：CNN 的三大特性 —— **局部連接、參數共享、平移不變性**；
> 能排出「卷積 → ReLU → 池化 → … → 全連接 → Softmax」的順序。

---

## 附錄 A：名詞速查表

### A.1 電腦視覺與應用

| 名詞 | 英文 | 一句話說明 |
|------|------|-----------|
| 電腦視覺 | Computer Vision (CV) | 讓機器從影像／影片理解世界 |
| 商業領域 | Commercial sectors | 零售、安防、工業、醫療、自駕、農業等 |
| 車牌辨識 | ANPR | 物件偵測 + OCR 讀出車牌 |
| 瑕疵檢測 | Defect detection | 工業上找出產品外觀異常 |
| 世界機器人大會 | World Robot Conference | 2024 展示「超現實圍棋博弈」 |
| 超現實圍棋博弈 | Hyper-realistic Go Match | 人形機器人下圍棋的展示 |

### A.2 CNN 核心

| 名詞 | 英文 | 說明 |
|------|------|------|
| 卷積神經網路 | Convolutional Neural Network (CNN) | 專為**網格狀資料**設計的神經網路 |
| 網格狀結構 | Grid-like structure | 影像（像素網格）、音訊（時頻網格） |
| 卷積層 | Convolutional layer | 自動學習階層式表徵、抽取特徵 |
| 階層式表徵 | Hierarchical representations | 低階邊緣 → 中階紋理 → 高階物件 |
| 卷積核 | Kernel / Filter | 滑動的小權重窗（如 3×3） |
| 參數重用 | Re-use / share parameters | 同一組權重全圖共用（CNN 核心思想） |
| 編碼器 | Encoder | 由多個 block 堆疊，學像素↔標籤的統計模式 |
| 深度 | Deep | 許多「逐漸變窄」的 block 堆疊而成 |
| 池化 | Pooling | 降採樣（Max / Average） |
| 全連接層 | Fully Connected (FC) | 整合特徵做最終分類 |
| 激活函數 | Activation (ReLU) | 加入非線性 |

### A.3 卷積輸出尺寸公式

| 項目 | 公式 |
|------|------|
| 輸出邊長（無 padding） | `(W − K) / S + 1` |
| 5×5 影像 + 3×3 核 + stride 1 | `(5 − 3)/1 + 1 = 3` → 3×3 |

---

## 附錄 B：常見錯誤與陷阱

### B.1 十大陷阱總表

| # | 陷阱 | 錯誤觀念 | 正確觀念 |
|---|------|---------|---------|
| 1 | CNN 適用範圍 | 「CNN 只能處理影像」 | 也能處理**音訊**等**網格狀資料** |
| 2 | CNN 的目的 | 「CNN 是為了壓縮圖片」 | CNN 是為了**抽取特徵、做辨識** |
| 3 | 參數共享 | 「每個位置用不同權重」 | 卷積**共享同一組權重**（全連接層才不共享） |
| 4 | 「Deep」的意思 | 「Deep 指圖片很大」 | Deep 指**許多 narrowing block 堆疊** |
| 5 | Encoder 的作用 | 「encoder 負責分類」 | encoder 負責**學特徵**（像素↔標籤的統計模式） |
| 6 | 卷積輸出尺寸 | 「5×5 過 3×3 得 5×5」 | 無 padding、stride 1 → **3×3** |
| 7 | 特徵層級 | 「一次就學到物件」 | 是**階層式**：邊緣→紋理→部件→物件 |
| 8 | 池化的作用 | 「池化會增加參數」 | 池化**沒有參數**，只是降採樣 |
| 9 | 圍棋的難點 | 「圍棋靠暴力搜尋即可」 | 局面數太大，**無法窮舉**，需學習型方法 |
| 10 | SOTA 架構 | 「影像辨識都用全連接網路」 | SOTA 幾乎都是 **CNN 及其變體** |

### B.2 易混名詞對照

| 名詞 A | 名詞 B | 分辨方式 |
|--------|--------|---------|
| 卷積層 | 全連接層 | 共享參數 / 不共享；保留空間 / 打平 |
| 卷積 | 池化 | 抽特徵（有參數） / 降採樣（無參數） |
| 電腦視覺 | 影像處理 | 理解語意 / 只做像素層操作 |
| Encoder | 分類器 | 學特徵 / 出標籤 |
| CNN | RNN | 網格狀空間資料 / 序列資料 |

---

## 附錄 C：教材頁面索引對照

| PDF 頁 | 標題 | 本筆記對應章節 |
|--------|------|---------------|
| 1 | 封面：Introduction to Computer Vision and Application | — |
| 2 | Real Case Examples in Commercial Sectors（Computer Vision） | 第 1 節 |
| 3 | Real Case Examples in Commercial Sectors（圖） | 第 1 節 |
| 4 | Real Case Examples in Commercial Sectors（圖） | 第 1 節 |
| 5 | Computer Vision（圖） | 第 1 節 |
| 6 | Computer Vision（圖） | 第 1 節 |
| 7 | Latest AI technologies in Mainland China and Hong Kong / Furthermore（世界機器人大會） | 第 2 節 |
| 8 | CNN — AI Basic Principles – Convolutional Neural Network（定義） | 第 3 節 |
| 9 | CNN — State-of-the-art methods / Encoder | 第 4 節 |
| 10 | Key idea: re-use parameters（3×3 convolution on 5×5 image） | 第 5 節 |
| 11 | Basic Concepts of CNN — Image Recognition by CNN（What is CNN?） | 第 6 節 |
| 12 | Basic Concepts of CNN — AI Basic Principles – Convolutional Neural Network | 第 6 節 |

> 說明：原稿第 2–6 頁多為**圖片**（商業案例展示），第 11–12 頁亦以圖示說明 CNN 基本概念；
> 這些頁面在筆記中對應到所屬章節的概念補充，不另設小節。

---

## 附錄 D：延伸資源與離線提示

### D.1 沒有網路時怎麼複習

本筆記本身即為**離線可讀**（Markdown 或單檔 HTML），不依賴任何外部資源。

- 先看附錄 A（名詞速查表）與附錄 E（一頁精華）。
- 用附錄 F 的線上互動測驗自測，答錯的題目對應回章節重讀。
- 需要圖解時，可自行畫出：**CNN 階層式特徵圖**、**3×3 卷積在 5×5 影像上滑動的示意**、
  **卷積 → ReLU → 池化 → 全連接 → Softmax 流程圖**。

### D.2 觀念延伸（考綱外但常被問）

| 主題 | 一句話 |
|------|--------|
| CNN 的變體 | LeNet、AlexNet、VGG、ResNet、MobileNet 等，皆為 CNN 家族 |
| 為何「參數共享」重要 | 大幅降低參數量，讓模型能處理高解析度影像且不易過擬合 |
| 資料增強 | 旋轉／翻轉／裁切可提升 CNN 對位置變化的穩健性 |
| 與傳統 CV 的差異 | 傳統需人工設計特徵（SIFT/HOG）；CNN 自動學特徵 |

---

## 附錄 E：一頁精華（考前 10 分鐘）

```text
【1. 商業案例（Real Case Examples in Commercial Sectors）】
  零售：人流統計、無人商店（物件偵測＋追蹤）
  安防：人臉辨識門禁、車牌辨識 ANPR（人臉＋OCR）
  工業：瑕疵檢測（影像分割＋異常偵測）
  醫療：X 光／CT 判讀（影像分類、語意分割）
  自駕：車道線／行人偵測（物件偵測＋光流）
  農業：病蟲害、果實分級（分類＋偵測）

【2. 最新 AI 技術（中國大陸／香港）】
  2024 World Robot Conference：Hyper-realistic Go Match（超現實圍棋博弈）
  圍棋 = AI 試金石（局面數太大，無法窮舉）；AlphaGo 2016 擊敗 Lee Sedol

【3. CNN 定義（必背）】
  Convolutional Neural Network = 專為「網格狀結構(grid-like)」資料
  （影像、音訊）設計的神經網路；用卷積層自動學「階層式表徵」並抽特徵

【4. 為何 SOTA（State-of-the-art）】
  影像/影片辨識的主流 = 神經網路，且幾乎都是 CNN 變體
  從 encoder 開始 → 學「像素 ↔ 標籤」的統計模式
  「deep」= 許多「逐漸變窄(narrowing)」的 block 堆疊

【5. 關鍵思想：參數重用（re-use parameters）】
  Convolution shares parameters（卷積共享參數，全圖共用同一組權重）
  例：3×3 convolution on 5×5 image → 輸出 (5−3)/1+1 = 3 → 3×3
  好處：參數少、保留空間關係、平移不變性

【6. CNN 基本概念 / 影像辨識】
  流程：輸入影像 → [卷積 → ReLU → 池化]×N → 展平 → 全連接 → Softmax → 類別
  三大特性：局部連接、參數共享、平移不變性
  階層式特徵：邊緣 → 紋理 → 部件 → 物件
```

---

## 附錄 F：互動式線上測驗（60 題）

> **60 題單選、滿分 60 分、建議 75 分鐘。**
> 測驗以**互動網頁**形式提供（點選即時計分、進度自動儲存）；本筆記**不再收錄非互動的紙本題目**，避免與線上版重複。

### F.1 開始測驗

**👉 [開始 60 題線上測驗](mc-quiz.html)**

線上版功能：

- **點選答案**即自動計分，並即時顯示得分
- **作答進度自動存在你的瀏覽器**（localStorage）——關掉網頁、隔天再開都能繼續
- 可切換「只顯示未答」或「只顯示答錯」的題目，快速複習
- 按「顯示答案」才揭曉正解與解析，不會一開始就被暴雷
- 需要紙本時，直接在該頁按列印即可

### F.2 時間分配建議

| 階段 | 時間 | 做什麼 |
|---|---|---|
| 第一輪 | 0–40 分鐘 | 快速作答有把握的題目，不確定先標記跳過 |
| 第二輪 | 40–65 分鐘 | 回頭處理標記的難題 |
| 第三輪 | 65–75 分鐘 | 檢查有沒有漏答 |

### F.3 評分參考

| 分數 | 程度 | 建議 |
|---|---|---|
| 54–60 | 優異 | 直接看附錄 E 一頁精華即可上場 |
| 45–53 | 良好 | 複習錯題所屬章節 |
| 36–44 | 及格邊緣 | 重讀主要章節 + 附錄 A |
| 0–35 | 需加強 | 整份筆記重讀一遍，再重做本卷 |

> 答錯的題目請對照〈附錄 G：互動測驗答錯題目 → 複習章節對照〉回到對應章節複習。

---

## 附錄 G：互動測驗答錯題目 → 複習章節對照

| 答錯題號 | 建議複習章節 |
|---|---|
| 1–5 | §1 商業案例（CV 定義與分類） |
| 6–10 | §1.1 六大應用、§2 世界機器人大會 |
| 11–15 | §1.2 為何用 CV、§2.2 AlphaGo |
| 16–20 | §1.1 應用對照、§1.2 一致性 |
| 21–26 | §3 CNN 定義與階層式表徵 |
| 27–32 | §4 SOTA、encoder、deep |
| 33–40 | §6 CNN 元件與三大特性 |
| 41–45 | §5 參數重用、卷積輸出尺寸 |
| 46–50 | §5.1 卷積 vs 全連接、stride / padding |
| 51–55 | §3.2 特徵階層、附錄 D.2 觀念延伸 |
| 56–60 | 附錄 D.2 CNN 變體、過擬合、§3.1 網格資料 |

---

*本篇為個人學習筆記整理，教材內容版權屬匯縱專業發展中心（IVDC）所有。*
