# CNN（卷積神經網路）學習筆記（考試溫習版）

---

**同場加映**：這是「學習筆記＋測驗」體系；同一堂課另有一篇**課後深度筆記**
（9 張霓虹 SVG 插圖＋簡報勘誤表）→ [CNN I：機器怎麼「看」？從視覺皮層到 LeNet-5](/2026/10/27/cnn-1-convnet-neon/)

**🧪 配套實作（可跑，不用 Colab）**：padding／stride 九種組合、手工濾波器 vs 訓練出來的濾波器、從零用 NumPy 寫 Conv2D → [Lab 1 原始碼與說明](https://github.com/kalpakjian/cnn-course-demo/tree/main/labs/lab1-conv)

**📐 跨課速查**：輸出尺寸、參數速算、術語、陷阱、一頁精華 → [/cnn-cheatsheet/](/cnn-cheatsheet/)

## 0. 30 秒總複習（考前最後掃描）

```
機器看圖的完整路線：

影像（數值矩陣）→ 局部特徵（一組權重滑過影像）→ 特徵圖（通道↑、空間尺寸↓）
                → 層層堆疊（邊緣→部件→物件）→ 全連接層 → 類別機率

CNN 的三個關鍵字：
  局部性（locality）  每個神經元只看影像的一小塊
  重用（sharing）     同一組權重用於影像的所有位置
  階層（hierarchy）  越深的層代表的概念越抽象

卷積層的四個必備數字：
  輸出尺寸  O = (N + 2P − F) / stride + 1
  參數數    (F × F × C_in × C_out) + C_out
  乘加次數  H_out × W_out × C_out × F × F × C_in
  感受野    r_out = r_in + (k − 1) · j_in
```

| 你會用到的東西 | 一句話記法 |
|---|---|
| 影像 | 二維數值矩陣；RGB 是 3 個通道，灰階是 1 個 |
| 核心 / 濾鏡（kernel / filter） | 一組權重；**逐元素相乘再相加** |
| 特徵圖（feature map） | 一個核心在整張影像上的回應圖；多個核心 = 多個通道 |
| 填補（padding） | 在影像四周補 0，避免邊界被削掉 |
| 步幅（stride） | 核心每次滑動幾格；stride 2 = 尺寸大約減半 |
| 輸出尺寸 | `O = (N + 2P − F) / stride + 1` |
| 感受野 | `r_out = r_in + (k − 1) · j_in`（配 `j_out = j_in · S`） |
| 參數共享 | 參數量只跟「核心大小 × 通道數」有關，**與影像大小無關** |
| LeNet-5 | `conv → pool → conv → pool → FC → FC → output`，約 6 萬個參數 |

---

## 1. 場景理解與物件辨識：機器（與人）怎麼「看」

### 1.1 你看到什麼？又是怎麼看到的？

人看一張圖幾乎是零成本：一眼就認出是誰、是哪個場景、發生什麼事。課程用這個反差開場，
問兩個問題：

| 問題 | 答案 |
|---|---|
| **你看見什麼？** | 物件、人物、場景、情緒、關係 |
| **你是怎麼看見的？** | 這才是機器要學的東西 |

課程點出視覺辨識挑戰的兩個特徵：

- **錯覺揭露了基本元素** —— 錯覺不是雜訊，是大腦「用簡單規則組合特徵」的證據；
  能解釋錯覺，就掌握了大腦用的是哪些基本元素。
- **錯覺也揭露了互相衝突的資訊** —— 同一個場景的線索常常互相矛盾，
  大腦必須自己決定相信哪一個。

所以「機器能不能學會看」不是玄學題目：**人類的視覺迴路是已知的**
（視覺皮層的分層就是一層層的抽象），可以拿來當設計藍圖。

### 1.2 機器「看見」的東西：影像就是數字

課程先做一個 jarring 的對照：一張人臉照片，人一眼認出是誰；
機器看到的是**一張數字表**。

| 項目 | 內容 |
|---|---|
| 影像的本質 | 一個矩陣，元素是像素的強度值 |
| 灰階值域 | `[0, 255]`（0 = 黑，255 = 白） |
| 一張 1080×1080 灰階圖 | `1080 × 1080 = 1,166,400` 個數值 |
| 同一張 RGB 圖 | `1080 × 1080 × 3 = 3,499,200` 個數值（3 個通道） |

然後課程提出那個關鍵問題：**「能不能直接對這個 1,166,400 長的向量做分類？」**

答案是 **不行**（No）。理由不是「維度太高」而已，而是：

1. **參數量爆炸** —— 1,166,400 個輸入接一個隱藏單元就要一百多萬個權重，
   資料量不夠，一定過擬合。
2. **丟掉了空間資訊** —— 把影像攤平成一個向量之後，
   「這個像素在左上方 3 個位置」這種資訊完全消失，
   模型無從知道哪些像素是鄰居、哪些構成一個邊。
3. **平移不變性無從建立** —— 同一隻貓左移一格，攤平後的向量完全不同，
   但它還是同一隻貓。

所以正確的做法是課程給的那三步：

> **利用影像的空間結構 → 學習 patch（影像塊）→ 把它們層層堆疊起來。**

這三句就是整個 CNN 的設計綱領。CNN 不是憑空冒出來的，它是為了回答
「怎麼讓機器利用空間結構」而生的。

> **考點**：影像 = 數值矩陣（值域 0–255）；不能直接對攤平向量分類，
> 必須利用空間結構、學 patch、層層建構。

### 1.3 經典機器視覺的根源：人腦與動物腦的視覺皮層

#### 1.3.1 靈感來源：視覺皮層

課程指出，CNN 的設計藍圖不是憑空發明的，而是**從人與動物的視覺皮層抄來的**：

- **神經元是分層的**：像素 → 邊緣 → 形狀 → 基本元素 → 場景。
- 舉例：**第 4 層會對「具有特定傾斜角度的條帶、對比的邊界」產生反應。**

「分層」這件事是關鍵：
大腦不是把整張影像攤平送進一個大網路，而是**一層一層抽稀、抽象化**。
CNN 的深層做的事與之同構。

#### 1.3.2 原語：神經元與動作電位

課程把生物神經元拆成幾個動作，作為神經網路單元的設計依據：

| 生物機制 | 說明 | 對應到人工神經網路 |
|---|---|---|
| 化學物質在樹突連結上累積 | 訊號是「累加」出來的 | 輸入加權求和 |
| 突觸前軸突 → 突觸後樹突 → 細胞體 | 訊號有方向、有傳遞順序 | 層與層的前向傳播 |
| 每個神經元接收許多樹突的訊號 | 多輸入、可加總 | 多個輸入加權求和 |
| **超過閾值就發火** | 全有全無的門檻 | **激勵函數的非線性** |
| 軸突再把訊號送給下游神經元 | 輸出傳給下一層 | 層與層之間的連線 |
| **弱刺激被忽略** | 小於門檻就沒反應 | 激勵函數的門檻行為 |

兩個特別值得記的關鍵字：

- **Sufficiently strong cross activation threshold** —— 必須**足夠強的跨節點活化**
  超過門檻才發火。
- **Non-linearity within each neuronal level** —— **每一層內部都有非線性**。
  沒有非線性，堆再多層也還是一個線性映射。

#### 1.3.3 神經元連成迴路：湧現、學習、記憶

> **Neurons connected into circuits (neural networks): emergent properties, learning, memory**

把神經元接成迴路之後，出現了**單個神經元沒有的性質（emergent properties）**：
學習、記憶。

而且是靠「**簡單的原語，排列成簡單、重複、而且極其巨大的網路**」做到的。
課程給的規模數字：

| 項目 | 數量 |
|---|---|
| 神經元數 | **86 billion**（860 億） |
| 每個神經元連到 | 約 **10,000** 個神經元 |
| 總連線數 | `86×10⁹ × 10⁴ ≈ 8.6×10¹⁴`（**近千兆量級**） |

一個 860 億個零件組成的系統，沒有中央控制器，
只靠「簡單原語 + 重複堆疊 + 局部規則」就長出了學習與記憶 ——
這正是深度學習最讓人震撼的地方。

#### 1.3.4 抽象層次：複雜概念由簡單部分組成

課程把視覺皮層的抽象層次整理成一張對照表：

| 腦區 | 負責處理 | 對應到網路的哪一層 |
|---|---|---|
| **LGN** | 小點（small dots） | 輸入 / 第一層 |
| **V1** | 方向（orientation）、視差（disparity）、部分顏色 | Conv 1（邊緣） |
| **V4** | 顏色、基本形狀、2D/3D、曲率（curvature） | Conv 2–3（紋理、部件） |
| **VTC** | 複雜特徵（臉部、物件） | FC（整體判別） |

<!-- CNN-FIGURE:cnn-cortex-layers -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 460" role="img" aria-label="視覺皮層的分層抽象" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="898.5" height="458.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">視覺皮層的分層抽象</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">LGN → V1 → V4 → VTC：越深越抽象</text>
<text x="48" y="122" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">越往深處 → 代表的概念越抽象</text>
<rect x="48" y="142" width="188" height="196" rx="12" fill="#1c2230" stroke="#7d859055" stroke-width="1.5"/>
<circle cx="78" cy="176" r="22" fill="#7d8590" opacity="0.92"/>
<text x="78" y="181.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">LGN</text>
<text x="110" y="172" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">外側膝狀體</text>
<text x="110" y="192" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">層級 1 / 4</text>
<text x="66" y="238" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">· 小點（small dots）</text>
<text x="66" y="264" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">· 亮度與對比的初步編碼</text>
<path d="M 238 240.0 L 252 240.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="256" y="142" width="188" height="196" rx="12" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<circle cx="286" cy="176" r="22" fill="#2dd4bf" opacity="0.92"/>
<text x="286" y="181.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">V1</text>
<text x="318" y="172" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">初級視覺皮層</text>
<text x="318" y="192" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">層級 2 / 4</text>
<text x="274" y="238" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">· 方向（orientation）</text>
<text x="274" y="264" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">· 視差（disparity）</text>
<text x="274" y="290" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">· 部分顏色資訊</text>
<path d="M 446 240.0 L 460 240.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="464" y="142" width="188" height="196" rx="12" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.5"/>
<circle cx="494" cy="176" r="22" fill="#58a6ff" opacity="0.92"/>
<text x="494" y="181.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">V4</text>
<text x="526" y="172" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">中級視覺皮層</text>
<text x="526" y="192" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">層級 3 / 4</text>
<text x="482" y="238" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">· 顏色、基本形狀</text>
<text x="482" y="264" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">· 2D / 3D、深淺</text>
<text x="482" y="290" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">· 曲率（curvature）</text>
<path d="M 654 240.0 L 668 240.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="672" y="142" width="188" height="196" rx="12" fill="#1c2230" stroke="#c084fc55" stroke-width="1.5"/>
<circle cx="702" cy="176" r="22" fill="#c084fc" opacity="0.92"/>
<text x="702" y="181.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">VTC</text>
<text x="734" y="172" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">高階視覺皮層</text>
<text x="734" y="192" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">層級 4 / 4</text>
<text x="690" y="238" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">· 複雜特徵</text>
<text x="690" y="264" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">· 臉部、物件、整體形狀</text>
<rect x="48" y="366" width="804" height="52" rx="10" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="68" y="398" font-size="13.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">複雜概念由簡單部分組成 —— 階層式抽象讓「邊緣」一步步長成「場景」</text>
<text x="48" y="442" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">早期皮層的神經連線本身就編碼了視覺概念的基本元素；同一套迴路被聽覺、嗅覺、味覺、觸覺重用。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：視覺皮層的四個層級。LGN 只看小點，V1 處理方向與視差，V4 處理顏色與基本形狀，VTC 處理複雜特徵——「複雜概念由簡單部分組成」的階層式抽象。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /CNN-FIGURE:cnn-cortex-layers -->

一句話總結：**複雜概念由簡單部分組成（Complex concepts from simple parts, hierarchy）**。
這和第 2.3 節的「車 = 輪子 + 車牌 + 頭燈」是同一個原理，
只不過大腦的組合規則是演化出來的，CNN 的組合規則是**學出來的**。

#### 1.3.5 通用「學習機器」，被廣泛重用

課程的最後一個觀察，是人腦的**硬體擴張**（hardware expansion）：

| 觀察 | 說明 |
|---|---|
| 人類大腦近期的膨脹，重用的是**相對簡單但通用**的學習架構 | 不是為每個新能力重新造一套硬體 |
| 聽覺、味覺、嗅覺、視覺、觸覺**共用相似的學習架構** | 一套通用學習機器，五個感官 |
| 視覺皮層、動作皮層、聽覺皮層的迴路**可以互換** | 互通性高 |
| 把視覺訊號送進聽覺皮層，**聽覺皮層會學會「看」** | 迴路可塑性 |
| 某個區域受傷後，**任務會轉移到未受傷的區域** | 彈性重組 |
| 不是完全通用，但**對我們這個世界調適得很好** | — |
| 人類把這套迴路**挪用**到許多新應用上 | 語言、數學、工具… |
| 任何一個 *homo sapiens* 都能學會現代任務（不到 7 萬年） | — |

**ML primitives not too different from animals: more to come?**
（機器學習的原語跟動物差不了多少 —— 還有更多等著發生？）

這是整堂課最深的一個收尾：CNN 之所以長成今天這樣，
不是因為工程師湊巧想到的，而是因為**它抄了大腦最有效的設計**：
分層抽象、局部連接、重用參數、門檻式非線性。

> **考點**：視覺皮層層級 LGN → V1 → V4 → VTC；
> 「複雜概念由簡單部分組成」；每一層內部都有非線性；
> 同一套迴路被五感重用、可互換。

---

## 2. 經典機器視覺的基礎：特徵、場景、濾鏡、卷積

### 2.1 影像辨識的空間結構

在卷積出現之前，機器視覺的做法是「**手工設計特徵**」：先想辦法從影像中
抽出有意義的量（邊緣、角點、紋理），再交給分類器。

課程先用最直覺的模型說明「空間結構」長什麼樣：

- **輸入**：2D 影像，也就是一個像素值陣列。
- **想法（Idea）**：把輸入的**一塊區域（patch）**接到隱藏層的一個神經元。
  這個神經元只「看到」這一塊的值，看不到其他任何地方。

接著課程把問題推到底：**「怎麼對這個 patch 加權，才能偵測到特定特徵？」**

答案就是**卷積（convolution）**，而卷積的定義式只是三個動作：

1. 拿一組權重（一個 **filter / 核心**）套在影像的 `4×4` 區塊上 —— 這是 16 個權重。
2. 把**同一組**權重套到下一個 `4×4` 區塊。
3. 每次**平移 2 個像素**換下一個區塊。

課程點破這件事的本質：**這個「一塊一塊貼過去」的操作就是卷積。**

而卷積層做的事，正是三句話：

| # | 卷積層做的事 | 為什麼重要 |
|---|---|---|
| 1 | 套一組權重（一個 filter）來擷取**局部特徵** | 每個神經元只看得到局部，參數量因此可控 |
| 2 | 用**多個 filter** 擷取**不同的**特徵 | 每個 filter 學到一種「回應型態」，堆成多個通道 |
| 3 | **在空間上共享（spatially share）**每個 filter 的參數 | 參數量與影像大小**無關** —— 這是最大的一個優勢 |

第 3 點是整個 CNN 的樞紐。若不共享參數，每個位置都要一組獨立權重，
就退回全連接網路的爆炸。

### 2.2 全連接神經網路為什麼不夠用

把影像攤平成向量、接上普通的神經網路（全連接），會遇到三個問題：

| 問題 | 說明 |
|---|---|
| **每個隱藏單元都看到整張圖** | 參數量爆炸 |
| **沒有空間資訊** | 攤平後的像素向量分不清誰是誰的鄰居 |
| **參數量太多 → 容易過擬合** | 一百多萬個權重配上幾千張圖，一定死 |

用一個具體數字把落差說清楚（32×32 灰階影像接 120 個隱藏單元）：

- 全連接：`1024 × 120 + 120 = 123,000` 個權重
- 卷積（5×5、1 個通道）：`5 × 5 × 1 = 25` 個權重
- **相差 4,920 倍**

但這個數字還不夠狠。**直接拿 LeNet-5 的第一層來比**，同一個輸出、同一個容量：

| | 全連接 | 卷積 |
|---|---|---|
| 輸出單元數 | `28×28×6 = 4,704` | `4,704`（相同） |
| 每個單元的輸入 | **1,024**（整張圖） | **25**（一個 5×5 patch） |
| 權重數 | `1024 × 4,704 = 4,816,896` | `(25 + 1) × 6 = 156` |
| **差距** | | **30,878 倍** |

換成現代的輸入，差距會更誇張（`224×224×3 → 222×222×64` 那一層）：

| | 全連接 | 卷積 |
|---|---|---|
| 權重數 | `150,529 × 3,153,216 = 4.75×10¹¹` | `(27 + 1) × 64 = 1,792` |
| **差距** | | **2.65×10⁸（2.6 億倍）** |

原因是兩條公式的根本差異：

```text
卷積參數   = (F·F·C_in + 1) · C_out      ← 只跟核心大小與通道數有關
全連接參數 = (n_in + 1) · n_out          ← 隨像素數線性爆炸
```

**影像變大，卷積的參數不變** —— 這是 CNN 能處理高解析度影像的根本原因。

而且卷積只拿 156 個權重就保留了「哪個位置有什麼反應」的資訊；
全連接花 481 萬個權重買到的卻是一張失去空間結構的向量。

<!-- CNN-FIGURE:cnn-fc-vs-conv -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 460" role="img" aria-label="全連接 vs 卷積" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="898.5" height="458.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全連接 vs 卷積</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">參數量與空間資訊的差距</text>
<rect x="48" y="118" width="390" height="244" rx="12" fill="#1c2230" stroke="#f472b655" stroke-width="1.5"/>
<text x="68" y="148" font-size="15.5" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全連接神經網路</text>
<text x="68" y="172" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每個隱藏單元都連到全部輸入</text>
<text x="100" y="190" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸入</text>
<text x="195" y="190" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">隱藏</text>
<text x="290" y="190" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出</text>
<path d="M 108 212 L 187 212" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 212 L 187 238" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 212 L 187 264" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 212 L 187 290" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 238 L 187 212" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 238 L 187 238" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 238 L 187 264" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 238 L 187 290" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 264 L 187 212" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 264 L 187 238" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 264 L 187 264" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 264 L 187 290" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 290 L 187 212" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 290 L 187 238" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 290 L 187 264" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 108 290 L 187 290" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 203 212 L 282 225" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 203 212 L 282 251" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 203 212 L 282 277" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 203 238 L 282 225" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 203 238 L 282 251" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 203 238 L 282 277" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 203 264 L 282 225" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 203 264 L 282 251" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 203 264 L 282 277" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 203 290 L 282 225" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 203 290 L 282 251" fill="none" stroke="#3a4450" stroke-width="1"/>
<path d="M 203 290 L 282 277" fill="none" stroke="#3a4450" stroke-width="1"/>
<circle cx="100" cy="212" r="8" fill="#f472b6" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="100" cy="238" r="8" fill="#f472b6" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="100" cy="264" r="8" fill="#f472b6" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="100" cy="290" r="8" fill="#f472b6" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="195" cy="212" r="8" fill="#f472b6" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="195" cy="238" r="8" fill="#f472b6" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="195" cy="264" r="8" fill="#f472b6" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="195" cy="290" r="8" fill="#f472b6" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="290" cy="225" r="8" fill="#f472b6" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="290" cy="251" r="8" fill="#f472b6" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="290" cy="277" r="8" fill="#f472b6" stroke="#f472b666" stroke-width="1.5"/>
<text x="68" y="318" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">權重數 = 1024 × 120 + 120</text>
<text x="68" y="340" font-size="13" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">= 123,000 個</text>
<rect x="462" y="118" width="390" height="244" rx="12" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="482" y="148" font-size="15.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">卷積層</text>
<text x="482" y="172" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一組權重滑過整張圖</text>
<text x="564" y="190" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4×4 影像</text>
<rect x="520" y="206" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="542" y="206" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="564" y="206" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="586" y="206" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="520" y="228" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="542" y="228" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="564" y="228" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="586" y="228" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="520" y="250" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="542" y="250" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="564" y="250" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="586" y="250" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="520" y="272" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="542" y="272" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="564" y="272" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="586" y="272" width="22" height="22" rx="3" fill="#12181f" stroke="#7d8590" stroke-width="1"/>
<rect x="520" y="206" width="66" height="66" rx="4" fill="#2dd4bf22" stroke="#2dd4bfcc" stroke-width="2"/>
<path d="M 618 250 L 676 250" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="686" y="206" width="88" height="88" rx="8" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="730" y="255" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">特徵圖</text>
<text x="482" y="318" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">權重數 = 5 × 5 × 1</text>
<text x="482" y="340" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">= 25 個</text>
<rect x="48" y="382" width="804" height="58" rx="10" fill="#1c2230" stroke="#fbbf2455" stroke-width="1.5"/>
<text x="68" y="408" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同樣的輸入、同一層的容量：123,000 個權重 vs 25 個權重 → 相差 4,920 倍</text>
<text x="68" y="430" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">而且全連接沒有「哪裡」的概念 —— 捲平後的像素向量丟掉了空間資訊。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 3：同一個 32×32 灰階影像接一層 120 個單元，全連接要 123,000 個權重，卷積只要 25 個，相差 4,920 倍；而且全連接會丟掉空間資訊。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /CNN-FIGURE:cnn-fc-vs-conv -->

> **考點**：全連接的問題是「參數太多 + 沒有空間資訊」；
> 卷積用**局部連接 + 參數共享**同時解決兩者。

### 2.3 高階特徵偵測

知道怎麼抽局部特徵之後，下一個問題是：**抽出來的特徵，要怎麼對應到「物件」？**

課程的做法是「**為每一個影像類別找出它的關鍵特徵**」（key features）：

| 影像類別 | 關鍵特徵 |
|---|---|
| 車 | 輪子、車牌、頭燈 |
| 建築物 | 門、窗、階梯 |
| 人臉 | 鼻、眼、嘴 |

這正是**高階特徵偵測（High Level Feature Detection）**的思路：
一個物件是由一組可辨識的部件組成的。

這張表也直接說明了為什麼需要**階層**：
「輪子」本身是低階特徵（弧線、圓形邊緣），
「車」則是由輪子 + 車牌 + 頭燈組合出來的高階特徵。
CNN 的深層做的事，就是**讓機器自己學會這種組合關係**，
而不是由人寫死「車 = 輪子 + 車牌 + 頭燈」。

> **考點**：高階特徵偵測＝用部件組合出物件；
> 「邊緣→部件→物件」的階層正是 CNN 深層的意義。

### 2.4 卷積與濾鏡

#### 2.4.1 卷積運算：逐元素相乘再相加

課程把卷積定義得非常直白：**「Convolution operation is element wise multiply and add」**。

拆成三步：

1. 取影像上的一塊 `F × F` 區塊（patch）。
2. 拿一個 `F × F` 的**核心**（filter）與它**逐元素相乘**。
3. 把這 `F × F` 個乘積**全部相加**，得到**一個數字** —— 這就是特徵圖的一格。

用課程的例子走一遍：核心是

```text
1 0 1
0 1 0
1 0 1
```

影像左上角的 `3×3` 區塊是

```text
1 1 1
0 1 1
0 0 1
```

逐元素相乘再相加：

```text
(1×1 + 0×1 + 1×1) + (0×0 + 1×1 + 0×1) + (1×0 + 0×0 + 1×1) = 4
```

這一格就是特徵圖左上角的 **4**。

<!-- CNN-FIGURE:cnn-conv-sliding -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 552" role="img" aria-label="卷積：核心滑過影像" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="898.5" height="550.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">卷積：核心滑過影像</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">逐元素相乘再相加，產生特徵圖</text>
<rect x="60" y="168" width="120" height="120" rx="6" fill="#fbbf2422" stroke="#fbbf24cc" stroke-width="2"/>
<rect x="60" y="168" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="80.0" y="194.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="100" y="168" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="120.0" y="194.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="140" y="168" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="160.0" y="194.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="180" y="168" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="200.0" y="194.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="220" y="168" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="240.0" y="194.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="60" y="208" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="80.0" y="234.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="100" y="208" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="120.0" y="234.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="140" y="208" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="160.0" y="234.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="180" y="208" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="200.0" y="234.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="220" y="208" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="240.0" y="234.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="60" y="248" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="80.0" y="274.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="100" y="248" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="120.0" y="274.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="140" y="248" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="160.0" y="274.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="180" y="248" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="200.0" y="274.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="220" y="248" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="240.0" y="274.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="60" y="288" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="80.0" y="314.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="100" y="288" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="120.0" y="314.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="140" y="288" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="160.0" y="314.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="180" y="288" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="200.0" y="314.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="220" y="288" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="240.0" y="314.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="60" y="328" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="80.0" y="354.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="100" y="328" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="120.0" y="354.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="140" y="328" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="160.0" y="354.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="180" y="328" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="200.0" y="354.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="220" y="328" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="240.0" y="354.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="60" y="168" width="120" height="120" rx="6" fill="none" stroke="#fbbf24cc" stroke-width="2.5"/>
<text x="60" y="152" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸入影像 5×5</text>
<text x="60" y="394" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">框起來 = 核心要看的 3×3 區塊</text>
<rect x="372" y="188" width="40" height="40" rx="4" fill="#fbbf241a" stroke="#fbbf246666" stroke-width="1"/>
<text x="392.0" y="214.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="412" y="188" width="40" height="40" rx="4" fill="#fbbf241a" stroke="#fbbf246666" stroke-width="1"/>
<text x="432.0" y="214.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="452" y="188" width="40" height="40" rx="4" fill="#fbbf241a" stroke="#fbbf246666" stroke-width="1"/>
<text x="472.0" y="214.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="372" y="228" width="40" height="40" rx="4" fill="#fbbf241a" stroke="#fbbf246666" stroke-width="1"/>
<text x="392.0" y="254.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="412" y="228" width="40" height="40" rx="4" fill="#fbbf241a" stroke="#fbbf246666" stroke-width="1"/>
<text x="432.0" y="254.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="452" y="228" width="40" height="40" rx="4" fill="#fbbf241a" stroke="#fbbf246666" stroke-width="1"/>
<text x="472.0" y="254.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="372" y="268" width="40" height="40" rx="4" fill="#fbbf241a" stroke="#fbbf246666" stroke-width="1"/>
<text x="392.0" y="294.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="412" y="268" width="40" height="40" rx="4" fill="#fbbf241a" stroke="#fbbf246666" stroke-width="1"/>
<text x="432.0" y="294.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="452" y="268" width="40" height="40" rx="4" fill="#fbbf241a" stroke="#fbbf246666" stroke-width="1"/>
<text x="472.0" y="294.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<text x="372" y="172" font-size="13.5" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">濾鏡 / 核心 3×3</text>
<rect x="690" y="188" width="40" height="40" rx="4" fill="#f472b633" stroke="#fbbf2466" stroke-width="2"/>
<text x="710.0" y="214.4" font-size="13.5" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<rect x="730" y="188" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="750.0" y="214.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text>
<rect x="770" y="188" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="790.0" y="214.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<rect x="690" y="228" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="710.0" y="254.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text>
<rect x="730" y="228" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="750.0" y="254.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<rect x="770" y="228" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="790.0" y="254.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text>
<rect x="690" y="268" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="710.0" y="294.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text>
<rect x="730" y="268" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="750.0" y="294.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text>
<rect x="770" y="268" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="790.0" y="294.4" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<text x="690" y="172" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">特徵圖 3×3</text>
<path d="M 285 250 L 360 250" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<text x="322" y="236" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">逐元素相乘</text>
<path d="M 500 250 L 678 250" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<text x="589" y="236" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全部相加 = 一格</text>
<rect x="48" y="392" width="804" height="118" rx="12" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.5"/>
<text x="68" y="420" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">特徵圖左上角那一格怎麼算出來？</text>
<text x="68" y="448" font-size="13.5" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">(1×1 + 0×1 + 1×1) + (0×0 + 1×1 + 0×1) + (1×0 + 0×0 + 1×1) = 4</text>
<text x="68" y="476" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一組 9 個權重在每個位置重用 → 參數量與影像大小無關，這正是卷積相對全連接最大的優勢。</text>
<text x="48" y="534" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出尺寸（valid，stride=1）：(N − F) / stride + 1 = (5 − 3) / 1 + 1 = 3</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：3×3 核心在 5×5 影像上滑動。左上角那一格示範了完整的計算：九組乘積相加得到 4。同一組權重在每個位置重用。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /CNN-FIGURE:cnn-conv-sliding -->

用 NumPy 實作（**本機實測**，輸出即下方程式）：

```python
import numpy as np

def conv2d(x, k, stride=1, pad=0):
    """x: (H, W, C_in)；k: (C_out, F, F, C_in)；回傳 (H_out, W_out, C_out)。"""
    H, W, C_in = x.shape
    F = k.shape[1]
    if pad:
        x = np.pad(x, ((pad, pad), (pad, pad), (0, 0)))
    Ho = (x.shape[0] - F) // stride + 1
    Wo = (x.shape[1] - F) // stride + 1
    out = np.zeros((Ho, Wo, k.shape[0]))
    for f in range(k.shape[0]):
        for i in range(F):
            for j in range(F):
                win = x[i:i + Ho * stride:stride, j:j + Wo * stride:stride, :]
                out[:, :, f] += np.sum(win * k[f, i, j, :], axis=2)
    return out

IMAGE = np.array([[1, 1, 1, 0, 0],
                   [0, 1, 1, 1, 0],
                   [0, 0, 1, 1, 1],
                   [0, 0, 1, 1, 0],
                   [0, 1, 1, 0, 0]], dtype=float)
KERNEL = np.array([[1, 0, 1],
                   [0, 1, 0],
                   [1, 0, 1]], dtype=float)

feat = conv2d(IMAGE[:, :, None], KERNEL[None, :, :, None])
print(feat.shape)          # (3, 3, 1)
print(feat[:, :, 0].astype(int))
```

**實測輸出**：

```text
(3, 3, 1)
[[4 3 4]
 [2 4 3]
 [2 3 4]]
```

#### 2.4.2 產生特徵圖

一個核心掃過整張影像，就得到一張**特徵圖（feature map）**：
它的每個位置記錄「這個核心在這個位置的反應有多強」。

- 用 **N 個核心** → 得到 **N 個通道**的特徵圖。
- 邊緣偵測、銳化、模糊……都是「換一組核心」而已。

課程用同一張照片配四組核心示範：

| 核心 | 矩陣 | 效果 |
|---|---|---|
| Sharpen（銳化） | `0 −1 0 / −1 5 −1 / 0 −1 0` | 強化對比，看起來更銳利 |
| Edge Detect（邊緣偵測） | `0 1 0 / 1 −4 1 / 0 1 0` | 只留下輪廓 |
| "Strong" Edge Detect（強邊緣） | `−1 −2 −1 / 0 0 0 / 1 2 1` | 方向性更強的邊緣 |

其中 Sharpen 與 Edge Detect 正是 2×2 Sobel 算子的經典寫法；
「強邊緣」那組則是 Sobel 的橫向 + 縱向合成。

**「為什麼銳化核心中間是 5？」** 這是最高頻的考點：
中心權重 `5 = 1 + 4×1`，其中 `1` 是「原圖不變」，`4×1` 是「四鄰居各貢獻一次」，
等於把原圖加上四鄰居的差分 → 差分越大（邊緣）輸出越大。
所以銳化核心**不改變影像的整體亮度**（權重總和 `5 − 4 = 1`）。

同理，邊緣偵測核心 `0 1 0 / 1 −4 1 / 0 1 0` 的權重總和是 `0`，
代表**平坦區域的輸出為 0**（只留下變化量）—— 這是判斷一組核心在做什麼的通用技巧。

#### 2.4.3 一個簡單的模式：邊緣

課程用最簡單的 `1 × 2` 核心示範邊緣偵測（Goodfellow 2016）：

```text
1  -1
```

它做的事就是「**右邊減左邊**」：相鄰兩格差異越大，輸出絕對值越大 → 邊緣。

原理非常直覺：邊緣 = 亮度劇烈變化的地方。這個 `1 −1` 就是「差分」本身。
把核心放大到 `3×3` 並在兩個方向都做差分，就得到 Sobel 算子。

#### 2.4.4 簡單核心 / 濾鏡總表

| 操作 | 核心 | 說明 |
|---|---|---|
| Identity（恆等） | `0 0 0 / 0 1 0 / 0 0 0` | 原樣輸出 |
| Edge detection | `1 0 −1 / 0 0 0 / −1 0 1` | 對角差分 |
| Edge detection | `0 1 0 / 1 −4 1 / 0 1 0` | Sobel（拉普拉斯型） |
| Edge detection | `−1 −1 −1 / −1 8 −1 / −1 −1 −1` | 拉普拉斯型，權重總和 0 |
| Sharpen（銳化） | `0 −1 0 / −1 5 −1 / 0 −1 0` | 權重總和 1，不改亮度 |
| Box blur（方框模糊） | `1/9 × [1 1 1 / 1 1 1 / 1 1 1]` | 所有權重等於平均值 |
| Gaussian blur（高斯模糊） | `1/16 × [1 2 1 / 2 4 2 / 1 2 1]` | 中間權重更大，更接近人類視覺 |

**一組核心的恆等式**：`輸出 = 核心 ⊛ 影像`。
若核心權重總和為 `1`，影像的整體亮度不變（模糊、銳化都是這類）；
若總和為 `0`，平坦區被消掉，只留下變化（邊緣偵測都是這類）。

> **考點**：卷積 = **逐元素相乘再相加**；一個核心 → 一張特徵圖；
> 權重總和 1 → 不改亮度，總和 0 → 只留變化。

---
## 3. CNN 的基礎：LeNet、從零學特徵、參數共享

### 3.1 從零學習視覺特徵

到這裡為止，特徵都是**人手工設計**的（邊緣核心、部件清單）。
課程提出的關鍵想法是：

> **Key idea: learn hierarchy of features directly from the data**
> （rather than hand-engineering them）
也就是 **de novo（從零學起）**。差別在哪裡？

| | 傳統機器視覺 | CNN（de novo） |
|---|---|---|
| 特徵從哪來 | **人寫死**（我決定什麼叫邊緣、什麼叫輪子） | **機器從資料學** |
| 階層 | 人設計好幾層 | 模型自己學出幾層 |
| 怎麼知道哪個特徵有用 | 靠經驗與試錯 | 靠**反向傳播**把有用的權留下來 |
| 適應新領域 | 要重新設計 | 重新訓練就好 |

課程給的實證（Lee+ ICML 2009）是一張三段圖，顯示模型學到的特徵有明顯的階層：

| 階層 | 學到的東西 |
|---|---|
| 低階特徵（Low level） | **邊緣、暗點**（edges, dark spots） |
| 中階特徵（Mid level） | **眼睛、耳朵、鼻子**（eyes, ears, nose） |
| 高階特徵（High level） | **面部結構**（facial structure） |

<!-- CNN-FIGURE:cnn-feature-hierarchy -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 456" role="img" aria-label="從零學特徵：特徵階層" style="width:100%;height:auto;display:block">
<defs><marker id="mfbbf24" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#fbbf24"/></marker></defs>
<rect x="0.75" y="0.75" width="898.5" height="454.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">從零學特徵：特徵階層</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">低階 → 中階 → 高階，全部由卷積權重自動學得</text>
<rect x="48" y="132" width="260" height="250" rx="12" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="66" y="162" font-size="15" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">低階特徵</text>
<text x="66" y="184" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Low level</text>
<rect x="118" y="198" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="148" y="198" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="178" y="198" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="208" y="198" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="118" y="228" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="148" y="228" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="178" y="228" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="208" y="228" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="118" y="258" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="148" y="258" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="178" y="258" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="208" y="258" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="118" y="288" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="148" y="288" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="178" y="288" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="208" y="288" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<text x="66" y="344" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">邊緣、暗點</text>
<text x="66" y="368" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">edges, dark spots</text>
<rect x="340" y="132" width="260" height="250" rx="12" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.5"/>
<text x="358" y="162" font-size="15" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">中階特徵</text>
<text x="358" y="184" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Mid level</text>
<rect x="410" y="198" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="440" y="198" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="470" y="198" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="500" y="198" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="410" y="228" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="440" y="228" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="470" y="228" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="500" y="228" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="410" y="258" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="440" y="258" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="470" y="258" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="500" y="258" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="410" y="288" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="440" y="288" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="470" y="288" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="500" y="288" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<text x="358" y="344" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">眼睛、耳朵、鼻子</text>
<text x="358" y="368" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">eyes, ears, nose</text>
<rect x="632" y="132" width="260" height="250" rx="12" fill="#1c2230" stroke="#c084fc55" stroke-width="1.5"/>
<text x="650" y="162" font-size="15" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">高階特徵</text>
<text x="650" y="184" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">High level</text>
<rect x="702" y="198" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="732" y="198" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="762" y="198" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="792" y="198" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="702" y="228" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="732" y="228" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="762" y="228" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="792" y="228" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="702" y="258" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="732" y="258" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="762" y="258" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="792" y="258" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="702" y="288" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<rect x="732" y="288" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="762" y="288" width="30" height="30" rx="2" fill="#0d1117" stroke="#7d8590" stroke-width="0.6"/>
<rect x="792" y="288" width="30" height="30" rx="2" fill="#8b949e" stroke="#7d8590" stroke-width="0.6"/>
<text x="650" y="344" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">面部結構</text>
<text x="650" y="368" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">facial structure</text>
<path d="M 48 414 L 852 414" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#mfbbf24)"/>
<text x="48" y="406" font-size="13" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">抽象程度 ↑　特徵由影像自己學出來，不是人手工設計的</text>
<text x="48" y="438" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">以上三層特徵皆由同一組卷積權重自動學得 —— 這就是「de novo（從零學起）」的關鍵。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 4：低階特徵是邊緣與暗點，中階是眼睛、耳朵、鼻子，高階是面部結構——這一層層的特徵不是人手寫的，而是模型直接從資料裡學出來的。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /CNN-FIGURE:cnn-feature-hierarchy -->

這張圖有兩層意義：

1. **階層是自動浮現的** —— 沒有人告訴模型「第二層應該學眼睛」，
   它是因為那樣組合對分類任務有用，反向傳播才把它保留下來。
2. **低階特徵跟任務無關** —— 邊緣在任何自然影像裡都有用，
   所以模型在邊緣偵測、分類、分割各種任務上學到的第一層都很像。

> **考點**：de novo = **特徵階層直接從資料學出來**；
> 低階（邊緣）→ 中階（眼耳鼻）→ 高階（面部結構）。
### 3.2 關鍵想法：重用參數

第二個關鍵想法是**參數共享（parameter sharing）**。

課程的說法：**「Convolution shares parameters」**，
並用一個具體例子帶過：在一張 `5×5` 的影像上做 `3×3` 卷積。

| | 參數共享（卷積） | 不共享（全連接） |
|---|---|---|
| 權重數 | `3 × 3 × 1 = 9` | `9 × 9 = 81`（每個位置一組） |
| 每個位置看到什麼 | 同一組 9 個權重 | 自己的 9 個權重 |
| 影像變大 | 參數量**不變** | 參數量跟著變大 |

重點不在省了多少參數，而在於**語意**：共享意味著
「邊緣是邊緣，不管它出現在影像的哪個角落」——
這正是**平移等變（translation equivariance）**的來源，也是 CNN 能學到「物體在哪都長一樣」的原因。

> **一個術語陷阱（考試很愛問）**：卷積給的是**平移等變**，不是**平移不變**。
>
> | 詞 | 意思 | 誰提供 |
> |---|---|---|
> | **平移等變**（equivariance） | 輸入右移 1 格 → **特徵圖也右移 1 格** | 參數共享（卷積本身） |
> | **平移不變**（invariance） | 輸入右移 1 格 → **特徵不變** | 再加上**池化**（尤其全域池化） |
>
> 簡報只提「參數共享讓特徵跟物件位置無關」，是日常說法；
> 嚴格講，卷積只是把位移「一起帶著走」，**不變**要靠池化把位置資訊壓掉。
> 全連接層 + Softmax 之所以能做到分類，正是因為它前面有池化。

### 3.3 用卷積擷取特徵

課程把這一段的結論收斂成三行（和 2.1 呼應，但這裡強調的是**學**出來的）：

1. **Apply a set of weights – a filter – to extract local features**
   套一組權重（一個 filter）擷取**局部**特徵。
2. **Use multiple filters to extract different features**
   用**多個** filter 擷取**不同的**特徵。
3. **Spatially share parameters of each filter**
   在空間上**共享**每個 filter 的參數。

三行合起來就是一個卷積層的完整定義。
第一、二行決定「**學什麼**」，第三行決定「**怎麼學得省**」。

在架構上，一個卷積層的輸出形狀是：

```text
輸出高度 = (輸入高度 + 2P − F) / stride + 1
輸出寬度 = (輸入寬度 + 2P − F) / stride + 1
輸出通道 = 核心的個數
```

**本機實測**（用 `numpy` 2.5.4、Python 3.15）：

```python
def out_size(n, f, p, s):
    return (n + 2 * p - f) // s + 1

for name, n, f, p, s, expect in [
        ("conv1", 32, 5, 0, 1, 28),
        ("pool1", 28, 2, 0, 2, 14),
        ("conv2", 14, 5, 0, 1, 10),
        ("pool2", 10, 2, 0, 2, 5)]:
    o = out_size(n, f, p, s)
    print("%-6s N=%2d F=%d P=%d s=%d -> O=%2d  (期望 %2d) %s"
          % (name, n, f, p, s, o, expect, "OK" if o == expect else "MISMATCH"))
```

**實測輸出**：

```text
conv1  N=32 F=5 P=0 s=1 -> O=28  (期望 28) OK
pool1  N=28 F=2 P=0 s=2 -> O=14  (期望 14) OK
conv2  N=14 F=5 P=0 s=1 -> O=10  (期望 10) OK
pool2  N=10 F=2 P=0 s=2 -> O= 5  (期望  5) OK
```

> **考點**：輸出尺寸公式 `O = (N + 2P − F) / stride + 1`；
> `P` 為 0 是 valid，`P = (F−1)/2`（F 為奇數）是 same。

### 3.4 LeNet-5

#### 3.4.1 這是誰做的、解決什麼問題

| 項目 | 內容 |
|---|---|
| 論文 | *Gradient Based Learning Applied To Document Recognition* |
| 作者 | Y. LeCun、L. Bottou、Y. Bengio、P. Haffner |
| 年份 | 1998 |
| 影響 | **確立了今天我們使用 CNN 的方式**；取代了手工特徵擷取 |

LeNet-5 是 CNN 的里程碑：它證明「**捲積 + 池化 + 全連接**」這個組合
可以在真實資料（手寫數字、郵政字碼）上訓練成功，而且**不需要手工設計特徵**。

#### 3.4.2 架構與張量尺寸

<!-- CNN-FIGURE:cnn-lenet5 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 458" role="img" aria-label="LeNet-5 架構" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="898.5" height="456.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">LeNet-5 架構</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">conv → pool → conv → pool → FC → FC → output</text>
<rect x="48" y="126" width="142" height="78" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="119.0" y="163.0" font-size="14.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Input</text>
<text x="119.0" y="185.0" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">32×32×1</text>
<path d="M 194 165.0 L 204 165.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="210" y="126" width="142" height="78" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="281.0" y="163.0" font-size="14.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">conv 5×5</text>
<text x="281.0" y="185.0" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">s=1 → 28×28×6</text>
<path d="M 356 165.0 L 366 165.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="372" y="126" width="142" height="78" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="443.0" y="163.0" font-size="14.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">avg pool</text>
<text x="443.0" y="185.0" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">f=2, s=2 → 14×14×6</text>
<path d="M 518 165.0 L 528 165.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="534" y="126" width="142" height="78" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="605.0" y="163.0" font-size="14.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">conv 5×5</text>
<text x="605.0" y="185.0" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">s=1 → 10×10×16</text>
<path d="M 680 165.0 L 690 165.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="696" y="126" width="142" height="78" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="767.0" y="163.0" font-size="14.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">avg pool</text>
<text x="767.0" y="185.0" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">f=2, s=2 → 5×5×16</text>
<rect x="48" y="288" width="150" height="78" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="123.0" y="325.0" font-size="14.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FC</text>
<text x="123.0" y="347.0" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">120 個單元</text>
<path d="M 202 327.0 L 216 327.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="220" y="288" width="150" height="78" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="295.0" y="325.0" font-size="14.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FC</text>
<text x="295.0" y="347.0" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">84 個單元</text>
<path d="M 374 327.0 L 388 327.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="392" y="288" width="150" height="78" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<text x="467.0" y="325.0" font-size="14.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Output</text>
<text x="467.0" y="347.0" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10 類（0–9）</text>
<path d="M 767.0 204 L 767.0 252" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 767.0 252 L 123 252" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 123 252 L 123 284" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="596" y="278" width="256" height="96" rx="10" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.5"/>
<text x="616" y="302" font-size="13" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出尺寸公式</text>
<text x="616" y="328" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">O = (N + 2P − F) / stride + 1</text>
<text x="616" y="350" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">N 輸入尺寸｜P 填補｜F 核心大小</text>
<text x="48" y="416" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">整體結構：conv → pool → conv → pool → FC → FC → output；越深層 H（高）↓、W（寬）↓、C（通道）↑。</text>
<text x="48" y="440" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">LeNet-5 全網只有約 6 萬個參數（60K），早期就能在手寫數字上訓練成功。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 5：LeNet-5 的每一層與張量尺寸。輸出尺寸一律套用 O = (N + 2P − F) / stride + 1。全網約 6 萬個參數。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /CNN-FIGURE:cnn-lenet5 -->

逐層拆解：

| 層 | 運算 | 參數 | 輸出尺寸 | 乘加次數 |
|---|---|---|---|---|
| Input | — | — | `32 × 32 × 1` | — |
| conv1 | `5×5, s=1` | `5×5×1×6 + 6 = 156` | `28 × 28 × 6` | 117,600 |
| avg pool1 | `f=2, s=2` | `6 × 2 = 12`（可訓練） | `14 × 14 × 6` | 4,704 |
| conv2 | `5×5, s=1` | `5×5×6×16 + 16 = 2,416` | `10 × 10 × 16` | 240,000 |
| avg pool2 | `f=2, s=2` | `16 × 2 = 32`（可訓練） | `5 × 5 × 16` | 1,600 |
| FC1 | — | `400×120 + 120 = 48,120` | `120` | 48,000 |
| FC2 | — | `120×84 + 84 = 10,164` | `84` | 10,080 |
| Output | — | `84×10 + 10 = 850` | `10` 類 | 840 |

**參數量合計 = 61,750（約 6 萬，課堂上說的「60K」）**，
**乘加次數合計 = 422,824**，其中 97% 以上的參數集中在兩個全連接層。

乘加次數的算法：**卷積層 `H_out × W_out × C_out × F × F × C_in`**，
**全連接層 `n_in × n_out`**。把參數與乘加分開看很重要 ——
參數量決定「要存多少權重」，乘加次數決定「要算多久」，
兩者對深度的代價是不同方向。

這裡有一個容易算錯的地方，值得單獨講：

| 算法 | 結果 | 差別在哪 |
|---|---|---|
| 只算卷積 + 全連接 | **61,706** | 把兩個池化層當成「沒有參數」 |
| 加上**可訓練**的平均池化 | **61,750** | 原版 LeNet-5 的平均池化**每張特徵圖有 2 個**可學參數（縮放 α 與偏置 β） |

`6 × 2 + 16 × 2 = 44`，`61,706 + 44 = 61,750`。
**原版 LeNet-5（LeCun 等人 1998）的平均池化是可訓練的**，
所以嚴格算原論文架構時是 61,750；今天的框架裡池化一律沒有權重，
所以照今天的慣例算就是 61,706。兩個數字都對，答題時講清楚用哪個慣例即可。

> **考點**：LeNet-5 的結構是 `conv→pool→conv→pool→FC→FC→output`；
> 池化用的是 **avg pool（平均池化）**；越深層 H↓、W↓、**C↑**；
> 參數量 61,750（含可訓練池化）／61,706（不含）。

#### 3.4.3 感受野：為什麼最後一層剛好看到整張圖

「感受野（receptive field）」＝ 一個神經元實際看得到的**輸入範圍**大小。
這是卷積網路最常被問、也最容易被答錯的進階題目。遞推只有兩行：

```text
r_out = r_in + (k − 1) · j_in      ← 感受野大小
j_out = j_in · S                  ← 跳距（相鄰神經元間隔幾格）
```

其中 `r_in` 是輸入端的感受野、`j_in` 是輸入端的跳距，起始值 `r₀ = j₀ = 1`。

**本機實測**（逐層套用上面兩行，Python 3.15）：

| 層 | k | s | 感受野 r | 跳距 j |
|---|---|---|---|---|
| 輸入 | — | — | 1 | 1 |
| C1 | 5 | 1 | `1 + 4×1 = ` **5** | 1 |
| S2 | 2 | 2 | `5 + 1×1 = ` **6** | 2 |
| C3 | 5 | 1 | `6 + 4×2 = ` **14** | 2 |
| S4 | 2 | 2 | `14 + 1×2 = ` **16** | 4 |
| C5 | 5 | 1 | `16 + 4×4 = ` **32** | 4 |

**C5 的感受野正好是 32×32 —— 整張輸入。**

這不是巧合，而是**反推出來的設計**：如果最後那層的 `1×1×120` 要能代表「整張圖」，
前面所有層的感受野就必須剛好撐滿 32。LeNet-5 的層數與核心大小，
是被「讓最後一層看見整張圖」這個目標逼出來的 —— 深度不是玄學，是有理由的。

> **考點**：感受野遞推 `r_out = r_in + (k−1)·j_in`、`j_out = j_in·S`；
> LeNet-5 的 C5 感受野 = 32 = 整張輸入。

#### 3.4.4 整體性質

課程給的三個重點：

1. **Only 60K parameters** —— 只有約 6 萬個參數，
   在 1998 年的硬體上就能訓練，這是它能落地的關鍵。
2. **越深層：`H↓, W↓, C↑`** —— 空間尺寸變小、通道數變多。
   這是一個**資訊瓶頸**：影像被「壓縮」成越來越少、但每個位置描述得越來越豐富的位置。
3. **Different filters look at different channels** —— 不同的 filter 負責不同的通道。

還有兩條容易被忽略的細節：

- **激勵函數用的是 Sigmoid 和 Tanh**（不是現在的 ReLU）。
  這是時代背景：當時還沒有 ReLU。
- **池化用的是平均池化（average pooling）**，不是現在常見的最大池化。
  平均池化可導、沒有「只挑最大值」的資訊損失，比較適合當年的反向傳播。

再補一個「圖上寫 FC、原論文其實是卷積」的細節：
上表把第 5 層標成 FC，是**照課堂投影片的畫法**。
但在 LeCun 等人 1998 年的原論文裡，第 5 層 C5 是一個 `5×5` 的**卷積**，
它把 `5×5×16` 壓成 `1×1×120`；後面第 6、7 層才是真正的全連接。
**數值上兩者等價**（`5×5×16 = 400` 個輸入接 120 個單元），
但「概念上是卷積」這個說法更能點出卷積層的好處：
**參數共享**。答題時照課堂說 FC 即可，被追問再補上這一層。

> **考點**：LeNet-5 = 6 萬參數、avg pool、Sigmoid/Tanh（非 ReLU）、
> `H↓ W↓ C↑` 的深層結構。

### 3.5 卷積的反向傳播

卷積層的權重也要靠梯度下降學，那 `∂E/∂W` 怎麼算？

課程用一個乾淨的對稱結構說明：

```text
前向：  O        = Convolution(X, F)
反向：  ∂E/∂F    = Convolution(X, ∂E/∂O)
```

**關鍵洞察：反向傳播用的還是卷積。** 只是角色互換了：

| 角色 | 前向 | 反向 |
|---|---|---|
| 「影像」 | `X`（輸入） | `∂E/∂O`（對輸出的梯度） |
| 「核心」 | `F`（權重） | `∂E/∂F`（對權重的梯度） |
| 運算 | 卷積 | **卷積** |

<!-- CNN-FIGURE:cnn-backprop-conv -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 552" role="img" aria-label="卷積的前向與反向傳播" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="898.5" height="550.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">卷積的前向與反向傳播</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">反向用的仍然是卷積，只是換了角色</text>
<rect x="48" y="104" width="804" height="190" rx="12" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.5"/>
<text x="68" y="132" font-size="14" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">前向傳播：O = Convolution(X, F)</text>
<rect x="80" y="158" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="96.0" y="179.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="112" y="158" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="128.0" y="179.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text>
<rect x="144" y="158" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="160.0" y="179.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text>
<rect x="80" y="190" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="96.0" y="211.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<rect x="112" y="190" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="128.0" y="211.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text>
<rect x="144" y="190" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="160.0" y="211.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text>
<rect x="80" y="222" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="96.0" y="243.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7</text>
<rect x="112" y="222" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="128.0" y="243.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text>
<rect x="144" y="222" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="160.0" y="243.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">9</text>
<text x="80" y="272" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">X（輸入 3×3）</text>
<rect x="284" y="174" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="300.0" y="195.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="316" y="174" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="332.0" y="195.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="284" y="206" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="300.0" y="227.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="316" y="206" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="332.0" y="227.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<text x="284" y="256" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">F（核心 2×2）</text>
<rect x="644" y="174" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="660.0" y="195.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text>
<rect x="676" y="174" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="692.0" y="195.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text>
<rect x="644" y="206" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="660.0" y="227.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">12</text>
<rect x="676" y="206" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="692.0" y="227.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">14</text>
<text x="644" y="256" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">O（輸出 2×2）</text>
<path d="M 184 206 L 276 206" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 356 206 L 636 206" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<text x="496" y="194" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">把 X 與 F 逐元素相乘後相加</text>
<rect x="48" y="316" width="804" height="190" rx="12" fill="#1c2230" stroke="#f472b655" stroke-width="1.5"/>
<text x="68" y="344" font-size="14" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">反向傳播：∂E/∂F = Convolution(X, ∂E/∂O)</text>
<rect x="80" y="370" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="96.0" y="391.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="112" y="370" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="128.0" y="391.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text>
<rect x="144" y="370" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="160.0" y="391.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text>
<rect x="80" y="402" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="96.0" y="423.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<rect x="112" y="402" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="128.0" y="423.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text>
<rect x="144" y="402" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="160.0" y="423.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text>
<rect x="80" y="434" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="96.0" y="455.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7</text>
<rect x="112" y="434" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="128.0" y="455.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text>
<rect x="144" y="434" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="160.0" y="455.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">9</text>
<text x="80" y="484" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">X（輸入 3×3）</text>
<rect x="284" y="386" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="300.0" y="407.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="316" y="386" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="332.0" y="407.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="284" y="418" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="300.0" y="439.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<rect x="316" y="418" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="332.0" y="439.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<text x="284" y="468" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">∂E/∂O（梯度 2×2）</text>
<rect x="644" y="386" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="660.0" y="407.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">12</text>
<rect x="676" y="386" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="692.0" y="407.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">16</text>
<rect x="644" y="418" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="660.0" y="439.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">24</text>
<rect x="676" y="418" width="32" height="32" rx="4" fill="#12181f" stroke="#30363d66" stroke-width="1"/>
<text x="692.0" y="439.12" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">28</text>
<text x="644" y="468" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">∂E/∂F（權重梯度 2×2）</text>
<path d="M 184 418 L 276 418" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 356 418 L 636 418" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<text x="496" y="406" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個卷積運算，換成「梯度」當角色</text>
<text x="48" y="532" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">重點：卷積層的反向傳播用的還是卷積 —— 把「對輸入的梯度」當成輸入、把「對權重的梯度」當成輸出。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 6：前向用 X 與 F 卷積得到 O；反向則把「對輸出的梯度」與 X 卷積，得到「對權重的梯度」。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /CNN-FIGURE:cnn-backprop-conv -->

原因在數學上很清楚：`∂O/∂F` 這個偏導數的分子結構
和 `∂O/∂X` 幾乎一樣 —— 都是「把另一個陣列**翻轉**後做卷積」。
所以「反向的卷積」其實是**互相關（cross-correlation）**，
實作上直接用同一個卷積函式、把陣列翻轉即可。

除了權重梯度，還有一條**輸入梯度**，考試也常問：

```text
前向：  O          = Convolution(X, F)
反向：  ∂E/∂F      = Convolution(X, ∂E/∂O)      ← 權重梯度
        ∂E/∂X      = Convolution(∂E/∂O, rot180(F))  ← 輸入梯度，要 full padding
```

`∂E/∂X` 需要 **full padding**（把核翻轉後補到「全」卷積），
因為**一個輸入像素會同時貢獻到多個輸出位置**，回傳時必須把重疊的部分疊起來。
連帶地，**影像邊界補的 0 不貢獻梯度** → 邊界的梯度比中間弱。

**池化的梯度只做路由**：

| 池化 | 梯度怎麼走 |
|---|---|
| max pool | 整包梯度給窗口內 **argmax** 的那個位置，其餘為 0 |
| avg pool | 平均分給窗口內每個像素（每格 `G/k²`） |

用 NumPy 實作並做**數值梯度檢查**（finite-difference gradient check）：

```python
def conv2d_bwd(x, k, dout, stride=1, pad=0):
    """回傳 (dx, dw)。x:(H,W,Cin) k:(Cout,F,F,Cin) dout:(Ho,Wo,Cout)。"""
    H, W, Cin = x.shape
    F = k.shape[1]
    if pad:
        x = np.pad(x, ((pad, pad), (pad, pad), (0, 0)))
    Ho = (x.shape[0] - F) // stride + 1
    Wo = (x.shape[1] - F) // stride + 1
    dx = np.zeros_like(x)
    dw = np.zeros_like(k)
    for f in range(k.shape[0]):
        for i in range(F):
            for j in range(F):
                win = x[i:i + Ho * stride:stride, j:j + Wo * stride:stride, :]
                dw[f, i, j, :] = np.sum(win * dout[:, :, f:f + 1], axis=(0, 1))
                dx[i:i + Ho * stride:stride, j:j + Wo * stride:stride, :] += (
                    dout[:, :, f:f + 1] * k[f, i, j, :])
    return dx, dw
```

**實測輸出**（隨機權重，與中心差分比對）：

```text
dw 最大相對誤差 = 6.707e-10  (門檻 1e-6)  PASS
```

> 這個檢查是所有深度學習框架都會做的自我驗證：
> 解析梯度必須跟「把權重微微加一點、看看loss 變多少」算出來的數值梯度一致。

> **考點**：卷積的反向傳播**用的仍然是卷積**；
> `∂E/∂F = Convolution(X, ∂E/∂O)`。

---
### 3.6 CNN 的形式化架構

課程給了一個非常簡潔的正式描述：

```text
CNN = representations + classifier

representations = (Conv + ReLU + Pool) × N layers
classifier      = Fully-connected
```

把它拆成兩個角色，就懂了一個 CNN 的全部：

| 區段 | 組成 | 角色 | 對應到本筆記 |
|---|---|---|---|
| **特徵擷取器**（representations） | `(Conv + ReLU + Pool) × N` | 把原始像素變成高階特徵 | §2.4、§3.1、§3.4 |
| **分類器**（classifier） | `Fully-connected` | 把特徵圖攤平後接全連接層，做機率輸出 | §2.2、§3.4.2 |

兩個關鍵觀察：

1. **ReLU 在每一層之後**，不是最後才加。卷積本身是線性的，
   沒有 ReLU 堆再多層仍然只是一個線性映射。
2. **池化放在卷積之後**，負責把空間尺寸壓小，讓後面的層能看得更「全域」。
   這也解釋了為什麼 LeNet-5 是 `conv→pool` 而不是 `pool→conv`。

> **考點**：**CNN = (Conv + ReLU + Pool) × N + 全連接層**；
> 前段是特徵擷取器，尾端是分類器。

---

## 4. CNN 的應用：一般架構與龐大威力

### 4.1 同一套架構，換資料就換任務

CNN 最令人吃驚的地方是**通用性**：架構本身幾乎不用改，
換資料、換標籤定義，就能做完全不同的事。

課程列出的應用版圖：

| 領域 | 具體任務 | CNN 在做的事 |
|---|---|---|
| **語意分割**（semantic segmentation） | 每個像素都給一個類別 | 全卷積化：輸出與輸入同尺寸，取代最後的全連接層 |
| **人臉偵測與辨識** | 找出臉在哪、是不是同一個人 | 共享權重的特徵讓「不同姿勢的同一張臉」有相近的特徵向量 |
| **自駕**（self-driving） | 辨識車道、行人、車輛、號誌 | 多任務共用一個 backbone |
| **影像上色**（image colorization） | 灰階 → 彩色 | 把「顏色」當成要預測的輸出通道 |
| **圖片／場景最佳化** | 自動修圖、增強、去雜訊 | 卷積就是可學習的濾鏡 |
| **影像放大**（up-scaling） | 超解析（super-resolution） | 先學低階特徵，再重建高階細節 |
| **醫學** | 腫瘤分割、輔助診斷 | 與分割結合，標出病灶 |
| **生物學** | 細胞、蛋白質結構分析 | 同樣是「找形狀」 |
| **基因體**（genomics） | 從 DNA 序列預測基因表現、疾病風險 | **把 DNA 序列當成 1D 影像**，用 1D 卷積掃過序列 |

最後一項特別值得注意：CNN 的核心概念是
「**用一個小核心掃過一串資料，學出局部模式**」。
DNA 序列正好符合這個形狀 —— A/T/G/C 四個字母就是 4 個通道，
「一個核心滑過序列」和「一個核心滑過影像」是同一個運算。

#### 4.1.1 九個應用的差異幾乎都在「輸出頭」

上表九個應用，用的骨幹其實是同一套。**真正不一樣的是最後那個輸出頭，
以及配合的損失函數**：

| 任務 | 輸出頭 | 損失 |
|---|---|---|
| 分類 / 識別 | 對類別做 softmax（或輸出嵌入向量） | 交叉熵、triplet、center loss |
| 語意分割 | 每個像素一組類別 | 逐像素交叉熵 + Dice |
| 偵測 | 框回歸 + 物件性分數 | smooth L1 + 物件性 BCE |
| 上色 | 兩個通道 `a, b` | L1 / L2（或對抗損失） |
| 超解析 | 高解析像素 | L1 + 感知／對抗損失 |
| 場景 / 照片優化 | **輸入本身**（要優化的是像素，不是權重） | 任務定義的目標函數 |

最後那一列最容易被忽略：**把網路固定住，反傳到「影像」而不是權重** ——
這就是「用 CNN 調整照片／場景」的意思，
也是**對抗樣本**與**特徵視覺化（Grad-CAM、deep dream）**的共同機制。

#### 4.1.2 為什麼能共用？因為歸納偏置一樣

| 共同前提 | 在哪些領域成立 |
|---|---|
| **局部性**：每個濾波器只看一個 patch | 自然影像、醫學影像、顯微鏡影像、DNA 序列的「局部模體」 |
| **平移等變**：同一個濾波器掃全圖 | 同上 |

所以同一組積木可以直接搬。真正不能搬的是**維度約定**：
基因體要一維卷積、CT 要三維卷積，但卷積的定義本身沒變。

#### 4.1.3 真正的代價是標註，不是算力

九個任務裡，分類只要一個標籤；分割要逐像素遮罩；醫學影像還要放射科醫師。
這也是為什麼「預訓練骨幹 + 少量微調」會變成常態 ——
骨幹學到的邊緣、紋理、部件，在九個任務之間是**可以轉移**的。

### 4.2 「龐大威力」的來源

把整堂課的主線收束成一句話：

> **架構只有三個零件 —— 局部連接、參數共享、層層堆疊 ——
> 但組合出來的東西足夠通用，通用到同一套架構可以橫跨分類、分割、
> 偵測、生成、醫療與基因體。**

這三個零件各自解決一個問題：

| 零件 | 解決的問題 |
|---|---|
| **局部連接** | 參數量爆炸、失去空間資訊 |
| **參數共享** | 參數量隨影像大小成長、無法學到平移不變性 |
| **層層堆疊** | 無法表示「複雜概念由簡單部分組成」 |

而 §1.3 的那張視覺皮層對照表說明：**這三個零件不是人類發明的**，
是大腦用了幾億年的設計。CNN 的「龐大威力」，本质上是
**把一個已知可行的通用學習架構，套用到了影像上**。

> **考點**：CNN 的一般架構 = `(Conv+ReLU+Pool)×N + 全連接`；
> 應用橫跨分割、偵測、辨識、上色、放大、醫療、生物、基因體。

---

## 附錄 A：卷積與 CNN 速查表

> **已移至跨課速查**（與 CNN 2 合訂，唯一維護版）：
> [術語對照](/cnn-cheatsheet/#terms)｜[尺寸與參數速算](/cnn-cheatsheet/#params)｜[經典核心速查](/cnn-cheatsheet/#kernels)。
> 本課專屬的內容（LeNet-5、感受野、反向傳播）仍在 §3，速查表的數字與 §3 一致。

## 附錄 B：常見錯誤與陷阱

> **已移至跨課速查**：[常見陷阱總表](/cnn-cheatsheet/#traps)（兩課合併，含 CNN 2 的 ReLU／池化陷阱）。

## 附錄 C：課程標題 → 本筆記章節對照

| 課程標題 | 本筆記章節 |
|---|---|
| Convolutional Neural Networks (CNNs) — 1. Scene understanding and object recognition | §1 |
| 1a. What do you see, and how? | §1.1、§1.2 |
| 1b. Classical machine vision roots in study of human/animal brains | §1.3 |
| Inspiration: human/animal visual cortex | §1.3.1 |
| Primitives: Neurons & action potentials | §1.3.2、§1.3.3 |
| Abstraction layers: edges, bars, directions, shapes, objects, scenes | §1.3.4 |
| General "learning machine", reused widely | §1.3.5 |
| 2. Classical machine vision foundations: features, scenes, filters, convolution | §2 |
| 2a. Spatial structure for image recognition | §2.1、§2.2、§2.3 |
| Using Spatial Structure | §2.1 |
| Feature Extraction with Convolution | §2.1、§3.3 |
| Fully Connected Neural Network | §2.2 |
| High Level Feature Detection | §2.3 |
| 2b. Convolutions and filters | §2.4 |
| Convolution operation is element wise multiply and add | §2.4.1 |
| Producing Feature Maps | §2.4.2 |
| A simple pattern: Edges | §2.4.3 |
| Simple Kernels / Filters | §2.4.4 |
| 3. CNN foundations: LeNet, de novo feature learning, parameter sharing | §3 |
| 3a. Learning Visual Features de novo | §3.1 |
| Key idea: learn hierarchy of features directly from the data | §3.1 |
| Key idea: re-use parameters | §3.2 |
| LeNet-5 | §3.4 |
| Backpropagation of convolution | §3.5 |
| CNN formalization: representations (Conv+ReLU+Pool)*N layers + Fully-connected | §3.6 |
| 4. CNN applications: General architecture, enormous power | §4 |

---

## 附錄 D：離線執行／安裝提示

這一課**不需要安裝任何框架**就能學完：卷積就是一個乘加迴圈。
以下提示是為了讓你想動手時不被環境卡住。

### D.1 只用 NumPy（最輕，零安裝風險）

本筆記所有程式碼只用 `numpy`，**不需要 PyTorch / TensorFlow**：

```powershell
python -m pip install numpy
python -c "import numpy; print(numpy.__version__)"
```

> 本機實測環境：**Python 3.15 + numpy 2.5.4**（Windows）。

### D.2 想用 PyTorch 對照同一組數字

```powershell
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
```

驗證安裝：

```python
import torch
print(torch.__version__)
```

PyTorch 的 `torch.nn.functional.conv2d` 接受 `(N, C, H, W)` 的張量，
**通道在最前面**，跟本筆記寫的 `(H, W, C)` 順序相反 —— 這是最容易踩到的坑。

```python
import torch
import torch.nn.functional as F

x = torch.tensor([[[[1.0]], [[1.0]], [[1.0]],
                   [[0.0]], [[1.0]], [[1.0]],
                   [[0.0]], [[0.0]], [[1.0]]]])   # (1, 1, 3, 3)
k = torch.tensor([[[[1.0, 0.0, 1.0]],
                   [[0.0, 1.0, 0.0]],
                   [[1.0, 0.0, 1.0]]]])             # (1, 1, 3, 3)
print(F.conv2d(x, k).shape)      # torch.Size([1, 1, 1, 1])
```

### D.3 沒有網路時怎麼辦

- 本筆記的 **HTML 頁面是單一檔案、零外部資源**，下載後可直接雙擊離線開啟。
- 所有圖表都是**內嵌 SVG**（不是外部圖片），縮放不失真、離線可看。
- 60 題測驗是**純前端互動頁**，進度存在瀏覽器 localStorage，離線一樣能作答。

### D.4 常見環境問題

| 症狀 | 原因 | 處理 |
|---|---|---|
| `ModuleNotFoundError: numpy` | 沒裝 | `python -m pip install numpy` |
| 中文印出來是亂碼 | PowerShell 不是 UTF-8 | 先設 `$env:PYTHONIOENCODING='utf-8'` |
| `torch` 裝完卻匯入失敗 | CPU / CUDA 版本不匹配 | 指定 `--index-url .../whl/cpu` |
| 卷積結果形狀對不上 | PyTorch 是 `(N,C,H,W)`、本筆記是 `(H,W,C)` | 記得 `permute` |
| 讀檔驗證時看到假的「標籤不平衡」 | PowerShell 5.1 用 ANSI 解碼 UTF-8 | 用 `[System.IO.File]::ReadAllText('<絕對路徑>')` |

---

## 附錄 E：一頁精華（考前 10 分鐘）

> **已移至跨課速查**：[一頁精華](/cnn-cheatsheet/#onepage)（CNN 1＋CNN 2 合訂，考前 10 分鐘版）。
> 本課的 30 秒版仍在 §0。

## 附錄 F：互動式線上測驗（60 題）

> **60 題單選、滿分 60 分、建議 75 分鐘。**
> 測驗以**互動網頁**形式提供（點選即時計分、進度自動儲存）；本筆記**不重複收錄題目**。

### F.1 開始測驗

**👉 [開始 60 題線上測驗](mc-quiz.html)**

線上版功能：

- **點選答案**即自動計分，並即時顯示得分
- **作答進度自動存在你的瀏覽器**（localStorage）—— 關掉網頁、隔天再開都能繼續
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
| 54–60 | 優異 | 直接看[一頁精華](/cnn-cheatsheet/#onepage)即可上場 |
| 45–53 | 良好 | 複習錯題所屬章節 |
| 36–44 | 及格邊緣 | 重讀主要章節 + [術語對照](/cnn-cheatsheet/#terms) |
| 0–35 | 需加強 | 整份筆記重讀一遍，再重做本卷 |

> 答錯的題目請對照下方〈附錄 G：互動測驗答錯題目 → 複習章節對照〉回到對應章節複習。

---

## 附錄 H：簡報勘誤表（7 處）

這一份講的 36 頁簡報裡，有幾個數字照抄會出事。
下面每一條我都**重新回原始簡報逐字核對過**（本機用 PyMuPDF 抽出文字比對），
也把「正確值怎麼來」一併寫上，考試被追問時可以直接答。

| # | 簡報寫的 | 問題 | 正確值 |
|---|---|---|---|
| 1 | 同一頁既寫「1080×1080×3 for an RGB image」，又寫「the **1,166,400**-long image vector」 | `1080² = 1,166,400` 是**灰階**；RGB 要再乘 3 | 灰階 1,166,400；RGB **3,499,200** |
| 2 | 「86 billion neurons, each connects to 10k neurons, **1 quadrillion (10¹²)** connections」 | 乘積對，但**級數標錯**：`10¹²` 是「一兆」，不是一 quadrillion | `86×10⁹ × 10⁴ = 8.6×10¹⁴`（約 **0.86 quadrillion**） |
| 3 | 「Only **60K** parameters」 | 四捨五入可以說 60K，但**不是 60,000** | 逐層加總 **61,750**（含可訓練平均池化）／**61,706**（不含） |
| 4 | 架構圖把第 5 層標成 `FC` | 原論文（LeCun 等 1998）裡 C5 其實是 `5×5` **卷積**，把 `5×5×16` 壓成 `1×1×120` | 數值等價（`400→120`），**概念上是卷積**、有參數共享 |
| 5 | 用「Shift by 2 pixels for next patch」描述，卻沒有說這叫 stride | 「stride」一詞雖最早出現在目錄，但**正式定義與公式直到架構圖那頁才出現** | 那就是 **stride = 2**；`O = (N + 2P − F)/S + 1` |
| 6 | 版權頁寫「©版權所有(**2015年X**月)」 | 母版**佔位字串沒填**（`X` 不是年份） | 其餘每一頁都是 **2026 年 2 月** |
| 7 | 有兩頁標題都叫「Fully Connected Neural Network」 | 中間夾了一頁別的標題，**順序錯位** | 兩頁不是同一件事：一頁講全連接的缺點，一頁是它的插圖 |

另外兩個「說得比較鬆」的地方，答題時講精確一點會比較安全：

- **「卷積」在深度學習其實是互相關**（不把核翻轉 180°）。
  對「學出來的」核沒有差別，但手推梯度時要記得這件事。
- **池化在現代意義下不可學習**；但原版 LeNet-5 的平均池化帶可訓練的
  縮放與偏置係數，所以它的參數量會比「純池化」多出 44 個（見 §3.4.2）。

> **這張表的用法**：考前如果有時間，把第 1、2、3 條再看一遍就夠了 ——
> 這三個數字最常被引用，也最常被引用錯。

---

## 附錄 G：互動測驗答錯題目 → 複習章節對照

| 答錯題號 | 建議複習章節 |
|---|---|
| 1–8 | §1.2 影像就是數字、§1.3.2 神經元與動作電位 |
| 9–14 | §1.3.4 視覺皮層抽象層次、§1.3.5 通用學習機器 |
| 15–20 | §2.1 空間結構、§2.2 全連接的限制 |
| 21–28 | §2.4.1 卷積運算、§2.4.2 特徵圖 |
| 29–34 | §2.4.3 邊緣、§2.4.4 經典核心總表、[核心速查](/cnn-cheatsheet/#kernels) |
| 35–40 | §3.1 de novo 特徵學習、§3.2 參數共享（**平移等變 vs 不變**） |
| 41–46 | §3.3 輸出尺寸公式、[參數速算](/cnn-cheatsheet/#params) |
| 47–53 | §3.4 LeNet-5、§3.4.3 感受野、[參數速算](/cnn-cheatsheet/#params) |
| 54–57 | §3.5 卷積的反向傳播（∂E/∂F 與 ∂E/∂X） |
| 58–60 | §3.6 形式化架構、§4 應用、[陷阱總表](/cnn-cheatsheet/#traps)、**附錄 H 勘誤表** |

> 答錯第 35–40 題 → 多半是把「平移等變」與「平移不變」搞混了，
> 回 §3.2 看一下那張對照表。
> 答錯第 47–53 題 → 多半是感受野沒背，見 §3.4.3。

---

*本篇為個人學習筆記整理，內容為個人理解與重點摘錄。*
