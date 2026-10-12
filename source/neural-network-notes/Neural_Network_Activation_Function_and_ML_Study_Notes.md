# Neural Network, Activation Function and Machine Learning 學習筆記（考試溫習版）

> 課程：Certificate in Application of Computer Vision Technology (Part-time)
> 機構：匯縱專業發展中心（IVDC）
> 教材來源：`5 IVDC_Neural Network, Activation Function and Machine Learning.pptx` → PDF（30 頁）
> 本筆記按 PDF 原稿每一個標題逐一填充內容，並補上定義、公式、關鍵數字、常見錯誤與考點。
> 原稿後半大量使用投影片圖示（p9–p16、p25–p26、p29–p30 幾乎沒有可抽取的文字），本筆記為這些圖**重繪了 22 張更清楚的插圖**（全部是內嵌 SVG，離線也能看），並補上圖示背後的概念。
> 🖱️ **互動測驗（推薦）**：附錄 F 提供 **60 題線上測驗**（即時計分、進度自動儲存）→ **[開始作答](mc-quiz.html)**

---

| # | 章節 | PDF 頁 |
|---|------|--------|
| 0 | [0. 30 秒總複習（考前最後掃描）](#0-30-秒總複習考前最後掃描) | — |
| 1 | [1. 教材與課程資訊（PDF p1）](#1-教材與課程資訊pdf-p1) | 1 |
| 2 | [2. Neural Network：AI 基本原則與生物神經元（PDF p2–p3）](#2-neural-networkai-基本原則與生物神經元pdf-p2p3) | 2–3 |
| 3 | [3. Neural Network：神經網路的組成（PDF p4）](#3-neural-network神經網路的組成pdf-p4) | 4 |
| 4 | [4. Artificial Neural Network：三層結構與傳播方向（PDF p5）](#4-artificial-neural-network三層結構與傳播方向pdf-p5) | 5 |
| 5 | [5. Artificial Neural Network：ANN 與 DNN 的定義（PDF p6）](#5-artificial-neural-networkann-與-dnn-的定義pdf-p6) | 6 |
| 6 | [6. Deep Neural Network：網路拓撲 Network Topology（PDF p7）](#6-deep-neural-network網路拓撲-network-topologypdf-p7) | 7 |
| 7 | [7. Activation Function：激勵函數是什麼（PDF p8）](#7-activation-function激勵函數是什麼pdf-p8) | 8 |
| 8 | [8. Threshold Logic Unit（TLU）（PDF p9–p10）](#8-threshold-logic-unittlupdf-p9p10) | 9–10 |
| 9 | [9. Rectified Linear Units（ReLU）（PDF p11–p12）](#9-rectified-linear-unitsrelupdf-p11p12) | 11–12 |
| 10 | [10. Sigmoid Function（PDF p13–p14）](#10-sigmoid-functionpdf-p13p14) | 13–14 |
| 11 | [11. Softmax Function（PDF p15–p16）](#11-softmax-functionpdf-p15p16) | 15–16 |
| 12 | [12. 問題類型與激勵函數的對應（PDF p17）](#12-問題類型與激勵函數的對應pdf-p17) | 17 |
| 13 | [13. Machine Learning：Analytics and Machine Learning（PDF p18）](#13-machine-learninganalytics-and-machine-learningpdf-p18) | 18 |
| 14 | [14. Machine Learning：基本概念 Basic Concepts（PDF p19）](#14-machine-learning基本概念-basic-conceptspdf-p19) | 19 |
| 15 | [15. 機器學習解決方案的十個步驟 Ten Steps（PDF p20）](#15-機器學習解決方案的十個步驟-ten-stepspdf-p20) | 20 |
| 16 | [16. Machine Learning：The Data/AI Landscape（PDF p21）](#16-machine-learningthe-dataai-landscapepdf-p21) | 21 |
| 17 | [17. Machine Learning：Types 機器學習的類型（PDF p22、p24、p27）](#17-machine-learningtypes-機器學習的類型pdf-p22p24p27) | 22、p24、p27 |
| 18 | [18. 監督式學習 Supervised Learning（PDF p23）](#18-監督式學習-supervised-learningpdf-p23) | 23 |
| 19 | [19. 監督式學習實例：分類與迴歸（PDF p25–p26）](#19-監督式學習實例分類與迴歸pdf-p25p26) | 25–26 |
| 20 | [20. 非監督式學習 Unsupervised Learning（PDF p28）](#20-非監督式學習-unsupervised-learningpdf-p28) | 28 |
| 21 | [21. Clustering：分群的兩個距離目標（PDF p29）](#21-clustering分群的兩個距離目標pdf-p29) | 29 |
| 22 | [22. Clustering：分群實例（PDF p30）](#22-clustering分群實例pdf-p30) | 30 |
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
【上半場】神經網路
生物神經元：樹突收訊 → 細胞體加總 → 超過閾值才發火（全有全無）→ 軸突送出
        ↓ 換成數學
人工神經元：a = Σwᵢxᵢ + b  →  激勵函數 f(a)  →  y
        ↓ 串成網路
輸入層 → 隱藏層（可多層）→ 輸出層
前向傳播 feed-forward 算答案；反向傳播 back propagation 改權重
隱藏層 > 2 層就叫 DNN（deep），專門處理複雜的模式辨識

【激勵函數四兄弟】
TLU      階梯    y = 1 if a ≥ θ else 0    不可微 → 只能切直線（解不了 XOR）
ReLU     f(a) = max(0, a)                 隱藏層首選：快、正區間梯度固定為 1
Sigmoid  σ(a) = 1/(1+e⁻ᵃ)                 壓到 (0,1) → 二元分類／機率
Softmax  pᵢ = e^zᵢ / Σⱼe^zⱼ               加總為 1 → 多類別分類

【下半場】機器學習
問題 → 分類（二元／多類別／多標籤）或 迴歸（連續數值）
十步：定義問題 → 定指標 → 取資料 → 清理合併 → 選演算法 → 訓練驗證 → 測試 → 部署 → 執行頻率 → 更新頻率
三條分類軸：Human Supervision?（監督式／非監督式／強化式）
            Learn Incrementally?（批次學習／增量學習）
            How they generalize?（基於實例／基於模型）
監督式：有標籤 {(x₁,y₁)…(xₙ,yₙ)} → 分類、迴歸
非監督式：沒標籤 {x₁…xₙ} → 分群（群內距離 ↓、群間距離 ↑）
分類看 Accuracy／Precision／Recall／F1；迴歸看 MAE／MSE／R²
```

| 關鍵詞 | 一句話記法 |
|---|---|
| Soma / dendrite / axon / synapse | 細胞體 / 樹突 / 軸突 / 突觸 |
| Action potential | 全有全無的電脈衝；過閾值才發火，沒有「部分發火」 |
| Neuron | 把輸入值通過函數再輸出結果 |
| Weight | 神經元之間傳遞的數值（可學習參數） |
| Feed-forward | 訊號由輸入層往輸出層傳 |
| Back Propagation | 誤差由輸出層往輸入層回傳，用來更新權重 |
| ANN | 人工神經網路（淺層，用於簡單任務） |
| DNN | 深度神經網路（> 2 個隱藏層，複雜模式辨識） |
| Activation function | 神經元內的數學規則，負責加入非線性 |
| TLU | 閾值邏輯單元，輸出只有 0 / 1 |
| ReLU | `max(0, a)`，隱藏層的預設選擇 |
| Sigmoid | `1/(1+e⁻ᵃ)`，把值壓到 (0, 1) |
| Softmax | 一組分數 → 一組機率（總和為 1） |
| Labeled / Unlabeled | 有標籤（監督式）／沒標籤（非監督式） |
| Classification / Regression | 輸出類別／輸出數值 |
| Clustering | 分群：群內距離最小、群間距離最大 |
| Confusion matrix | TP / FP / FN / TN 四格，所有分類指標的來源 |
| MAE / MSE / R² | 迴歸的評估指標（不是 Accuracy） |

---

## 1. 教材與課程資訊（PDF p1）

<!-- p: 1 -->

原稿封面（p1）三行文字：

```
Certificate in Application of Computer Vision
Technology (Part-time)
Neural Network, Activation Function and Machine Learning
```

| 項目 | 內容 |
|---|---|
| 課程 | Certificate in Application of Computer Vision Technology (Part-time) |
| 機構 | 匯縱專業發展中心（IVDC） |
| 本節主題 | Neural Network, Activation Function and Machine Learning |
| 教材頁數 | 30 頁（PowerPoint 匯出 PDF） |

### 1.1 本節在整個課程的位置

本節是課程的 **Lesson 5**，前面幾節分別是 Introduction to Generative AI、Using Local GPU for ML、
Introduction to Computer Vision、OpenCV；後面接的是 **CNN 1、CNN 2、TensorFlow/PyTorch 物件偵測**。

也就是說：這一節是「**CNN 的前置知識**」——先把神經元、激勵函數、機器學習的分類搞清楚，
下一節才能理解卷積層為什麼長那樣。

### 1.2 本節的兩大主題

| 主題 | 對應 PDF 頁 | 一句話說明 |
|---|---|---|
| **神經網路與激勵函數** | p2–p17 | 從生物神經元出發，到四種激勵函數（TLU / ReLU / Sigmoid / Softmax），最後說明「什麼問題該用哪一個」 |
| **機器學習** | p18–p30 | 機器學習的基本概念、解決方案的十個步驟、類型（監督式／非監督式／強化式）、分類與迴歸實例、分群 |

> **考點**：講到「激勵函數」時，一定要能說出它**加在哪裡**（神經元的加權總和之後）、
> 以及它**為什麼必要**（引入非線性）。這兩點是本節最常被考的核心。

---

## 2. Neural Network：AI 基本原則與生物神經元（PDF p2–p3）

<!-- p: 2–3 -->

原稿 p2、p3 的標題都是「**Neural Network — AI Basic Principles: Artificial Neural Network**」，
但內容其實是**先講生物神經元**，再用它當作人工神經網路的靈感來源。

### 2.1 生物神經元的構造（p2）

| 構造 | 英文 | 說明（原稿敘述） |
|---|---|---|
| 細胞體 | cell body / **soma** | 內含**細胞核**（cell nucleus） |
| 樹突 | **dendrites** | 由細胞體分岔出去的纖維，負責**接收**訊號 |
| 軸突 | **axon** | 一條較長的纖維，負責**送出**訊號 |
| 突觸 | **synapses** | 神經元之間的接點；一個神經元可與 **10 到 100,000** 個其他神經元連接 |
| 訊號傳遞 | — | 訊號透過複雜的**電化學反應**（electrochemical reaction）在神經元之間傳播 |

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 430" width="100%" style="max-width:760px;height:auto" role="img" aria-label="生物神經元與人工神經元的對應關係"><defs><marker id="ar-nb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><rect x="14" y="12" width="732" height="196" rx="8" fill="#ffffff" stroke="#d8dee4" stroke-width="1"/><text x="30" y="34" font-size="14" fill="#c0392b" text-anchor="start" font-weight="bold">① 生物神經元（biological neuron）</text><polyline points="352,92 300,62 272,44" fill="none" stroke="#d97706" stroke-width="2.4"/><polyline points="344,84 306,96 286,78" fill="none" stroke="#d97706" stroke-width="2.4"/><polyline points="342,120 300,130 268,150" fill="none" stroke="#d97706" stroke-width="2.4"/><polyline points="352,142 322,168 292,184" fill="none" stroke="#d97706" stroke-width="2.4"/><polyline points="366,66 356,40 338,22" fill="none" stroke="#d97706" stroke-width="2.4"/><circle cx="392" cy="122" r="46" fill="#fef3c7" stroke="#d97706" stroke-width="2.6"/><circle cx="392" cy="122" r="18" fill="#d97706" stroke="#d97706" stroke-width="1.5" opacity="0.45"/><line x1="438" y1="122" x2="604" y2="122" stroke="#57606a" stroke-width="5"/><line x1="604" y1="122" x2="654" y2="96" stroke="#57606a" stroke-width="2.4"/><line x1="604" y1="122" x2="654" y2="122" stroke="#57606a" stroke-width="2.4"/><line x1="604" y1="122" x2="654" y2="148" stroke="#57606a" stroke-width="2.4"/><circle cx="660" cy="96" r="5" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="660" cy="122" r="5" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="660" cy="148" r="5" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="440" cy="122" r="6" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><text x="150" y="40" font-size="13" fill="#d97706" text-anchor="start" font-weight="bold">樹突 dendrites</text><text x="322" y="198" font-size="13" fill="#d97706" text-anchor="start" font-weight="bold">細胞體 soma</text><text x="408" y="156" font-size="12" fill="#d97706" text-anchor="start" font-weight="normal">（細胞核 nucleus）</text><text x="496" y="112" font-size="13" fill="#57606a" text-anchor="start" font-weight="bold">軸突 axon</text><text x="672" y="96" font-size="13" fill="#6f42c1" text-anchor="start" font-weight="bold">突觸 synapse</text><text x="676" y="168" font-size="12" fill="#6f42c1" text-anchor="start" font-weight="normal">輸出訊號</text><text x="150" y="176" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">動作電位 action potential：</text><text x="150" y="194" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">越過閾值才全部發火，沒有「部分發火」</text><rect x="14" y="222" width="732" height="194" rx="8" fill="#ffffff" stroke="#d8dee4" stroke-width="1"/><text x="30" y="244" font-size="14" fill="#c0392b" text-anchor="start" font-weight="bold">② 人工神經元（artificial neuron）——把上面每個零件換成數學</text><circle cx="90" cy="268" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="273" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>1</sub></text><line x1="107" y1="268" x2="216" y2="308.56" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-nb)"/><text x="160" y="262" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>1</sub></text><circle cx="90" cy="320" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="325" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>2</sub></text><line x1="107" y1="320" x2="216" y2="320.0" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-nb)"/><text x="160" y="314" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>2</sub></text><circle cx="90" cy="372" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="377" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>3</sub></text><line x1="107" y1="372" x2="216" y2="331.44" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-nb)"/><text x="160" y="366" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>3</sub></text><text x="90" y="404" font-size="12" fill="#2c6fb1" text-anchor="middle" font-weight="normal">inputs 輸入</text><text x="160" y="296" font-size="12" fill="#2c6fb1" text-anchor="start" font-weight="normal">weights 權重</text><circle cx="246" cy="320" r="30" fill="#ffffff" stroke="#2c6fb1" stroke-width="2.2"/><text x="246" y="328" font-size="22" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">Σ</text><line x1="278" y1="320" x2="342" y2="320" stroke="#57606a" stroke-width="1.8" marker-end="url(#ar-nb)"/><text x="310" y="302" font-size="13" fill="#57606a" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">a = Σ w<sub>i</sub>x<sub>i</sub> + b</text><circle cx="376" cy="320" r="30" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="2.2"/><text x="376" y="327" font-size="20" fill="#ffffff" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">f</text><text x="376" y="372" font-size="12" fill="#2c6fb1" text-anchor="middle" font-weight="normal">activation 激勵函數</text><line x1="408" y1="320" x2="552" y2="320" stroke="#57606a" stroke-width="1.8" marker-end="url(#ar-nb)"/><text x="562" y="326" font-size="16" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">y</text><text x="562" y="350" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">output 輸出</text><text x="30" y="268" font-size="12.5" fill="#0f766e" text-anchor="start" font-weight="bold">對應：樹突→輸入 x｜突觸→權重 w｜細胞體→Σ wᵢxᵢ + b｜軸突輸出→f(a)</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 1：<b>生物神經元 ↔ 人工神經元的對應</b>（原稿 p4 圖）。生物神經元把「樹突收到的訊號 × 突觸強度」加總，超過閾值才沿軸突發火；人工神經元把同一件事寫成 <code>a = Σwᵢxᵢ + b</code>，再交給激勵函數 f 決定輸出。</figcaption>
</figure>

### 2.2 動作電位：全有全無（p3）

- 傳遞訊號時，神經元會產生一種**全有全無（all-or-nothing）**的電化學脈衝，稱為
  **動作電位（action potential）**。
- 一旦細胞達到某個**閾值（threshold）**，動作電位就會**發火（fire）**，把訊號沿著軸突送出。
- 動作電位**只有發生與不發生兩種**，**沒有「部分發火」**這種事。
- 這些訊號在**短期**控制腦的活動，也促成神經元連結的**長期改變**。
- 原稿的結論：**這些機制被認為是腦中學習的基礎**。

> **考點（超常考）**：
> 1. 哪個構造負責**接收**？→ 樹突（dendrites）。
> 2. 哪個構造負責**送出**？→ 軸突（axon）。
> 3. 神經元之間在哪裡連接？→ 突觸（synapses）。
> 4. 動作電位的特性？→ **全有全無**，達閾值才發火，**沒有部分發火**。
> 5. 「學習」在生物層面指的是什麼？→ 神經元連結的長期改變。

### 2.3 為什麼要先講生物神經元

人工神經網路的每一個零件，都能對應到生物神經元的一個部位——
這也是「**Artificial** Neural Network」這個名字的由來：**借結構、不借化學**。
下一節（p4）就會把這個對應關係寫成「神經元」與「權重」兩個名詞。

---

## 3. Neural Network：神經網路的組成（PDF p4）

<!-- p: 4 -->

原稿 p4 用兩條列點定義神經網路由什麼組成：

| 組成 | 原稿說明 | 白話 |
|---|---|---|
| **Neurons** 神經元 | Neurons which pass input values through functions and output the result | 神經元把**輸入值通過函數**，再輸出結果 |
| **Weights** 權重 | Weights which carry values between neurons | 權重負責在神經元**之間傳遞數值** |

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 240" width="100%" style="max-width:760px;height:auto" role="img" aria-label="單一人工神經元的數學流程"><defs><marker id="ar-nm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><text x="30" y="34" font-size="14" fill="#c0392b" text-anchor="start" font-weight="bold">一個神經元＝「加權總和」＋「激勵函數」兩個步驟</text><circle cx="90" cy="100" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="105" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>1</sub></text><line x1="107" y1="100" x2="214" y2="139.0" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-nm)"/><text x="158" y="92" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>1</sub></text><circle cx="90" cy="150" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="155" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>2</sub></text><line x1="107" y1="150" x2="214" y2="150.0" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-nm)"/><text x="158" y="142" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>2</sub></text><circle cx="90" cy="200" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="205" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>3</sub></text><line x1="107" y1="200" x2="214" y2="161.0" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-nm)"/><text x="158" y="192" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>3</sub></text><text x="90" y="228" font-size="12" fill="#2c6fb1" text-anchor="middle" font-weight="normal">輸入 inputs</text><circle cx="246" cy="150" r="30" fill="#ffffff" stroke="#2c6fb1" stroke-width="2.2"/><text x="246" y="158" font-size="22" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">Σ</text><line x1="278" y1="150" x2="336" y2="150" stroke="#57606a" stroke-width="1.8" marker-end="url(#ar-nm)"/><text x="307" y="132" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">a</text><circle cx="370" cy="150" r="30" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="2.2"/><text x="370" y="157" font-size="20" fill="#ffffff" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">f</text><line x1="402" y1="150" x2="500" y2="150" stroke="#57606a" stroke-width="1.8" marker-end="url(#ar-nm)"/><text x="512" y="156" font-size="16" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">y</text><text x="246" y="214" font-size="14" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">加權總和 a = Σ w<sub>i</sub>x<sub>i</sub> + b</text><text x="370" y="214" font-size="14" fill="#2c6fb1" text-anchor="middle" font-weight="normal">激勵 f(a)</text><text x="512" y="214" font-size="13" fill="#57606a" text-anchor="middle" font-weight="normal">輸出</text><text x="556" y="70" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">b = bias 偏置（可學習的門檻）</text><text x="556" y="94" font-size="12.5" fill="#c0392b" text-anchor="start" font-weight="normal">少了 f，整網路就只是線性模型；</text><text x="556" y="114" font-size="12.5" fill="#c0392b" text-anchor="start" font-weight="normal">f 帶來非線性，才學得動複雜圖形。</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 4：<b>神經元內部的兩步驟</b>。先做加權總和（含 bias）得到 a，再交給激勵函數 f 產生輸出 y。激勵函數是整個網路「非線性」的來源——若沒有它，再多層也只是等價於一層線性轉換。</figcaption>
</figure>

### 3.1 一個神經元到底算了什麼

把上圖拆成兩個步驟，這是最重要的心智模型：

| 步驟 | 數學式 | 意義 |
|---|---|---|
| ① 加權總和 | `a = Σᵢ wᵢxᵢ + b` | 把每個輸入乘上它的權重後相加，再加上偏置 b |
| ② 激勵函數 | `y = f(a)` | 把加權總和交給 f，決定這個神經元要輸出什麼 |

- **權重 w 是「可學習」的參數**：訓練的過程就是在調整這些 w（以及 b）。
- **b 是 bias（偏置）**：可以想成「可調整的門檻」，讓神經元不一定要在輸入全為 0 時才輸出 0。
- 若沒有步驟 ②（或 ② 是線性的），多層網路在數學上等價於**一層**線性轉換——
  這正是「激勵函數必須是非線性」的理由（第 7 節會再展開）。

> **考點**：原稿把「神經元」定義成「把輸入值通過函數後輸出」，把「權重」定義成
> 「在神經元之間傳遞的數值」。考試常考這兩個定義的配對，別把權重說成「儲存資料的地方」。

---

## 4. Artificial Neural Network：三層結構與傳播方向（PDF p5）

<!-- p: 5 -->

原稿 p5 只有五個詞（其餘都是圖）：**Input Layer、Hidden Layer、Output Layer、Feed-forward、Back Propagation**。

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 430" width="100%" style="max-width:760px;height:auto" role="img" aria-label="人工神經網路的三層結構與前向／反向傳播"><defs><marker id="ar-an" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><line x1="110" y1="140" x2="360" y2="96" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="140" x2="360" y2="150" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="140" x2="360" y2="204" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="140" x2="360" y2="258" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="140" x2="360" y2="312" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="200" x2="360" y2="96" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="200" x2="360" y2="150" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="200" x2="360" y2="204" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="200" x2="360" y2="258" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="200" x2="360" y2="312" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="260" x2="360" y2="96" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="260" x2="360" y2="150" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="260" x2="360" y2="204" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="260" x2="360" y2="258" stroke="#d8dee4" stroke-width="1"/><line x1="110" y1="260" x2="360" y2="312" stroke="#d8dee4" stroke-width="1"/><line x1="360" y1="96" x2="610" y2="180" stroke="#d8dee4" stroke-width="1"/><line x1="360" y1="96" x2="610" y2="240" stroke="#d8dee4" stroke-width="1"/><line x1="360" y1="150" x2="610" y2="180" stroke="#d8dee4" stroke-width="1"/><line x1="360" y1="150" x2="610" y2="240" stroke="#d8dee4" stroke-width="1"/><line x1="360" y1="204" x2="610" y2="180" stroke="#d8dee4" stroke-width="1"/><line x1="360" y1="204" x2="610" y2="240" stroke="#d8dee4" stroke-width="1"/><line x1="360" y1="258" x2="610" y2="180" stroke="#d8dee4" stroke-width="1"/><line x1="360" y1="258" x2="610" y2="240" stroke="#d8dee4" stroke-width="1"/><line x1="360" y1="312" x2="610" y2="180" stroke="#d8dee4" stroke-width="1"/><line x1="360" y1="312" x2="610" y2="240" stroke="#d8dee4" stroke-width="1"/><circle cx="110" cy="140" r="20" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="2"/><circle cx="110" cy="200" r="20" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="2"/><circle cx="110" cy="260" r="20" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="2"/><circle cx="360" cy="96" r="20" fill="#fef3c7" stroke="#d97706" stroke-width="2"/><circle cx="360" cy="150" r="20" fill="#fef3c7" stroke="#d97706" stroke-width="2"/><circle cx="360" cy="204" r="20" fill="#fef3c7" stroke="#d97706" stroke-width="2"/><circle cx="360" cy="258" r="20" fill="#fef3c7" stroke="#d97706" stroke-width="2"/><circle cx="360" cy="312" r="20" fill="#fef3c7" stroke="#d97706" stroke-width="2"/><circle cx="610" cy="180" r="20" fill="#c0392b" stroke="#c0392b" stroke-width="2"/><circle cx="610" cy="240" r="20" fill="#c0392b" stroke="#c0392b" stroke-width="2"/><text x="360" y="28" font-size="14" fill="#1a7f37" text-anchor="middle" font-weight="bold">Feed-forward 前向傳播</text><line x1="140" y1="44" x2="580" y2="44" stroke="#1a7f37" stroke-width="2.4" marker-end="url(#ar-an)"/><text x="360" y="342" font-size="14" fill="#6f42c1" text-anchor="middle" font-weight="bold">Back Propagation 反向傳播</text><line x1="580" y1="354" x2="140" y2="354" stroke="#6f42c1" stroke-width="2.4" marker-end="url(#ar-an)"/><text x="110" y="392" font-size="14" fill="#2c6fb1" text-anchor="middle" font-weight="bold">Input Layer</text><text x="110" y="412" font-size="12" fill="#2c6fb1" text-anchor="middle" font-weight="normal">輸入層</text><text x="360" y="392" font-size="14" fill="#d97706" text-anchor="middle" font-weight="bold">Hidden Layer</text><text x="360" y="412" font-size="12" fill="#d97706" text-anchor="middle" font-weight="normal">隱藏層（可多層）</text><text x="610" y="392" font-size="14" fill="#c0392b" text-anchor="middle" font-weight="bold">Output Layer</text><text x="610" y="412" font-size="12" fill="#c0392b" text-anchor="middle" font-weight="normal">輸出層</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 2：<b>ANN 的三層結構</b>（原稿 p5）。藍＝輸入層、黃＝隱藏層、紅＝輸出層；訊號<b>由左往右</b>傳（Feed-forward），誤差<b>由右往左</b>回傳以更新權重（Back Propagation）。層與層之間是「全連接」，每一條線都是一個可學習的權重。</figcaption>
</figure>

### 4.1 三層結構

| 層 | 英文 | 角色 |
|---|---|---|
| 輸入層 | **Input Layer** | 接收原始特徵（例如一張圖的像素值） |
| 隱藏層 | **Hidden Layer** | 做特徵轉換；**可以有好多層**，層數越多網路越「深」 |
| 輸出層 | **Output Layer** | 產生最後的答案（類別機率或數值） |

### 4.2 兩個傳播方向（一定要分清楚）

| 名稱 | 方向 | 做什麼 |
|---|---|---|
| **Feed-forward** 前向傳播 | 輸入 → 輸出 | 把資料往前算，得到預測值 |
| **Back Propagation** 反向傳播 | 輸出 → 輸入 | 用「預測與答案的誤差」回頭調整每一層的權重 |

一個完整的訓練循環是：**前向傳播算答案 → 算誤差 → 反向傳播改權重 → 再前向傳播**，
反覆很多次（每一輪叫一個 epoch）。

> **考點**：
> - 「用誤差來更新權重」的是 **Back Propagation（反向傳播）**，不是 Feed-forward。
> - 前向傳播的方向是 **輸入層 → 隱藏層 → 輸出層**。
> - 隱藏層的數量決定網路「深不深」；輸入層與輸出層的數量則由問題決定
>   （例如 3 類別分類 → 輸出層 3 個神經元）。

---

## 5. Artificial Neural Network：ANN 與 DNN 的定義（PDF p6）

<!-- p: 6 -->

原稿 p6 給出兩個正式定義，這一頁是**必背**：

### 5.1 ANN（Artificial Neural Network，人工神經網路）

> An Artificial Neural Network is a **computational model inspired by the structure and functioning
> of biological neural networks**. It consists of **interconnected nodes (artificial neurons) organized
> into layers**, and it **can learn from data to make predictions or decisions**.

中文重點：

- 是一種**計算模型**，靈感來自**生物神經網路的結構與運作方式**。
- 由**互相連接的節點（人工神經元）**組成，並且**分層排列**。
- 能**從資料中學習**，用來做**預測或決策**。

### 5.2 DNN（Deep Neural Network，深度神經網路）

> A Deep Neural Network is a type of neural network that has **multiple hidden layers**, allowing it to
> learn **complex patterns and representations** from input data. It is called "deep" because of its
> **depth, with more than two hidden layers**. Deep neural networks have been successful in various
> domains, such as **computer vision and natural language processing**.

中文重點：

- 是神經網路的**一種**（DNN 屬於 ANN）。
- 具備**多個隱藏層**，能學到**複雜的模式與表徵**。
- 「deep」指的是**深度**：**隱藏層超過兩層**（more than two hidden layers）。
- 已成功應用於**電腦視覺**與**自然語言處理（NLP）**等領域。

### 5.3 兩者比較

| 比較項 | ANN | DNN |
|---|---|---|
| 隱藏層數 | 少（1～2 層） | **> 2 層** |
| 別名 | 淺層網路（shallow） | 深度網路（deep） |
| 能力 | 學簡單的關係 | 學複雜的模式與表徵 |
| 典型應用 | 表格資料、簡單分類 | 影像辨識、語音、NLP |

> **考點（必考）**：
> 1. 「deep」的判斷標準 → **隱藏層多於兩層**（不是「資料很多」、也不是「神經元很多」）。
> 2. DNN 成功應用的兩個代表領域 → **computer vision** 與 **natural language processing**。
> 3. ANN 的定義關鍵字 → **inspired by biological neural networks**、**organized into layers**、
>    **learn from data to make predictions or decisions**。

---

## 6. Deep Neural Network：網路拓撲 Network Topology（PDF p7）

<!-- p: 7 -->

原稿 p7 的標題是「**Deep Neural Network — AI Basic Principles: Network Topology**」，
文字只有一句（其餘是兩張網路圖）：

> ANNs are relatively **shallow** and are used for **simpler tasks**, while DNNs are characterized by
> their **depth** and are employed for **complex pattern recognition tasks**.

中文：

> ANN 相對**淺**，用於**較簡單的任務**；DNN 的特徵是**深度**，用於**複雜的模式辨識任務**。

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 330" width="100%" style="max-width:760px;height:auto" role="img" aria-label="淺層 ANN 與深層 DNN 的拓撲比較"><defs><marker id="ar-dn" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><rect x="20" y="46" width="320" height="240" rx="8" fill="#ffffff" stroke="#d8dee4" stroke-width="1"/><text x="180" y="74" font-size="14" fill="#2c6fb1" text-anchor="middle" font-weight="bold">ANN（shallow）</text><line x1="90" y1="140" x2="230" y2="120" stroke="#d8dee4" stroke-width="1"/><line x1="90" y1="140" x2="230" y2="165" stroke="#d8dee4" stroke-width="1"/><line x1="90" y1="140" x2="230" y2="210" stroke="#d8dee4" stroke-width="1"/><line x1="90" y1="140" x2="230" y2="255" stroke="#d8dee4" stroke-width="1"/><line x1="90" y1="190" x2="230" y2="120" stroke="#d8dee4" stroke-width="1"/><line x1="90" y1="190" x2="230" y2="165" stroke="#d8dee4" stroke-width="1"/><line x1="90" y1="190" x2="230" y2="210" stroke="#d8dee4" stroke-width="1"/><line x1="90" y1="190" x2="230" y2="255" stroke="#d8dee4" stroke-width="1"/><line x1="90" y1="240" x2="230" y2="120" stroke="#d8dee4" stroke-width="1"/><line x1="90" y1="240" x2="230" y2="165" stroke="#d8dee4" stroke-width="1"/><line x1="90" y1="240" x2="230" y2="210" stroke="#d8dee4" stroke-width="1"/><line x1="90" y1="240" x2="230" y2="255" stroke="#d8dee4" stroke-width="1"/><line x1="230" y1="120" x2="300" y2="190" stroke="#d8dee4" stroke-width="1"/><line x1="230" y1="165" x2="300" y2="190" stroke="#d8dee4" stroke-width="1"/><line x1="230" y1="210" x2="300" y2="190" stroke="#d8dee4" stroke-width="1"/><line x1="230" y1="255" x2="300" y2="190" stroke="#d8dee4" stroke-width="1"/><circle cx="90" cy="140" r="14" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.6"/><circle cx="90" cy="190" r="14" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.6"/><circle cx="90" cy="240" r="14" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.6"/><circle cx="230" cy="120" r="14" fill="#fef3c7" stroke="#d97706" stroke-width="1.6"/><circle cx="230" cy="165" r="14" fill="#fef3c7" stroke="#d97706" stroke-width="1.6"/><circle cx="230" cy="210" r="14" fill="#fef3c7" stroke="#d97706" stroke-width="1.6"/><circle cx="230" cy="255" r="14" fill="#fef3c7" stroke="#d97706" stroke-width="1.6"/><circle cx="300" cy="190" r="14" fill="#c0392b" stroke="#c0392b" stroke-width="1.6"/><text x="180" y="274" font-size="12.5" fill="#57606a" text-anchor="middle" font-weight="normal">隱藏層少、參數少 → 較簡單的任務</text><rect x="420" y="46" width="320" height="240" rx="8" fill="#ffffff" stroke="#d8dee4" stroke-width="1"/><text x="580" y="74" font-size="14" fill="#c0392b" text-anchor="middle" font-weight="bold">DNN（deep）</text><line x1="450" y1="80.0" x2="500" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="80.0" x2="500" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="80.0" x2="500" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="80.0" x2="500" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="80.0" x2="500" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="136.66666666666666" x2="500" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="136.66666666666666" x2="500" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="136.66666666666666" x2="500" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="136.66666666666666" x2="500" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="136.66666666666666" x2="500" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="193.33333333333334" x2="500" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="193.33333333333334" x2="500" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="193.33333333333334" x2="500" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="193.33333333333334" x2="500" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="193.33333333333334" x2="500" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="250.0" x2="500" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="250.0" x2="500" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="250.0" x2="500" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="250.0" x2="500" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="450" y1="250.0" x2="500" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="80.0" x2="550" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="80.0" x2="550" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="80.0" x2="550" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="80.0" x2="550" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="80.0" x2="550" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="122.5" x2="550" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="122.5" x2="550" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="122.5" x2="550" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="122.5" x2="550" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="122.5" x2="550" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="165.0" x2="550" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="165.0" x2="550" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="165.0" x2="550" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="165.0" x2="550" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="165.0" x2="550" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="207.5" x2="550" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="207.5" x2="550" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="207.5" x2="550" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="207.5" x2="550" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="207.5" x2="550" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="250.0" x2="550" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="250.0" x2="550" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="250.0" x2="550" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="250.0" x2="550" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="500" y1="250.0" x2="550" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="80.0" x2="600" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="80.0" x2="600" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="80.0" x2="600" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="80.0" x2="600" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="80.0" x2="600" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="122.5" x2="600" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="122.5" x2="600" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="122.5" x2="600" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="122.5" x2="600" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="122.5" x2="600" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="165.0" x2="600" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="165.0" x2="600" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="165.0" x2="600" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="165.0" x2="600" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="165.0" x2="600" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="207.5" x2="600" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="207.5" x2="600" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="207.5" x2="600" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="207.5" x2="600" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="207.5" x2="600" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="250.0" x2="600" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="250.0" x2="600" y2="122.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="250.0" x2="600" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="250.0" x2="600" y2="207.5" stroke="#d8dee4" stroke-width="0.7"/><line x1="550" y1="250.0" x2="600" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="80.0" x2="650" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="80.0" x2="650" y2="136.66666666666666" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="80.0" x2="650" y2="193.33333333333334" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="80.0" x2="650" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="122.5" x2="650" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="122.5" x2="650" y2="136.66666666666666" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="122.5" x2="650" y2="193.33333333333334" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="122.5" x2="650" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="165.0" x2="650" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="165.0" x2="650" y2="136.66666666666666" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="165.0" x2="650" y2="193.33333333333334" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="165.0" x2="650" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="207.5" x2="650" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="207.5" x2="650" y2="136.66666666666666" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="207.5" x2="650" y2="193.33333333333334" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="207.5" x2="650" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="250.0" x2="650" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="250.0" x2="650" y2="136.66666666666666" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="250.0" x2="650" y2="193.33333333333334" stroke="#d8dee4" stroke-width="0.7"/><line x1="600" y1="250.0" x2="650" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="650" y1="80.0" x2="700" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="650" y1="80.0" x2="700" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="650" y1="80.0" x2="700" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="650" y1="136.66666666666666" x2="700" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="650" y1="136.66666666666666" x2="700" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="650" y1="136.66666666666666" x2="700" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="650" y1="193.33333333333334" x2="700" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="650" y1="193.33333333333334" x2="700" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="650" y1="193.33333333333334" x2="700" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="650" y1="250.0" x2="700" y2="80.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="650" y1="250.0" x2="700" y2="165.0" stroke="#d8dee4" stroke-width="0.7"/><line x1="650" y1="250.0" x2="700" y2="250.0" stroke="#d8dee4" stroke-width="0.7"/><circle cx="450" cy="80.0" r="8" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="450" cy="136.66666666666666" r="8" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="450" cy="193.33333333333334" r="8" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="450" cy="250.0" r="8" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="500" cy="80.0" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="500" cy="122.5" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="500" cy="165.0" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="500" cy="207.5" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="500" cy="250.0" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="550" cy="80.0" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="550" cy="122.5" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="550" cy="165.0" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="550" cy="207.5" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="550" cy="250.0" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="600" cy="80.0" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="600" cy="122.5" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="600" cy="165.0" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="600" cy="207.5" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="600" cy="250.0" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="650" cy="80.0" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="650" cy="136.66666666666666" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="650" cy="193.33333333333334" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="650" cy="250.0" r="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.2"/><circle cx="700" cy="80.0" r="8" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="700" cy="165.0" r="8" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="700" cy="250.0" r="8" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><text x="580" y="274" font-size="12.5" fill="#57606a" text-anchor="middle" font-weight="normal">深（多個隱藏層）→ 複雜模式辨識</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 3：<b>網路拓撲（Network Topology）</b>（原稿 p7）。左：淺層 ANN，隱藏層少、參數少，適合較簡單的任務；右：DNN 有多個隱藏層，逐層堆疊出複雜表徵，適合電腦視覺、語音、NLP 這類複雜的模式辨識。</figcaption>
</figure>

### 6.1 什麼是「網路拓撲（Network Topology）」

**拓撲**指的是網路的「形狀」——也就是：

| 拓撲要素 | 說明 |
|---|---|
| 層數（depth） | 有幾個隱藏層；越多層越深 |
| 每層的神經元數（width） | 每個隱藏層有多寬 |
| 連接方式 | 全連接（fully connected）、卷積、循環… |
| 激勵函數 | 每一層用什麼 f（見第 7 節之後） |

「網路拓撲」就是在描述這個骨架；**同樣的資料，換拓撲就是換模型**。

### 6.2 為什麼「深」有用

- 淺層網路：只能學到比較簡單的關係（例如用幾個特徵畫一條分界線）。
- 深層網路：**逐層堆疊出階層式的表徵**——以影像為例，前面的層學到邊緣與顏色，
  中間的層組合成紋理與局部形狀，後面的層才認得出「貓」或「車」。
- 這也是為什麼 CNN（卷積神經網路）幾乎都是 deep 的架構。

> **考點**：
> - 「相對淺、簡單任務」→ **ANN**；「深、複雜模式辨識」→ **DNN**。
> - Network Topology 談的是**網路的結構**（層數、寬度、連接方式），不是資料的形狀。

---

## 7. Activation Function：激勵函數是什麼（PDF p8）

<!-- p: 8 -->

原稿 p8 用一段話定義激勵函數（原文照錄）：

> An activation function is a **math rule** used in a neural network. It **sits inside a neuron**.
> It takes the **total input numbers, adds them up**, and **decides if the neuron should turn on or
> send data ahead**. It adds a twist called **non-linearity** so the network can **learn hard patterns**.

中文拆解：

| 原稿說法 | 意義 |
|---|---|
| a **math rule** used in a neural network | 它是一條**數學規則** |
| **sits inside a neuron** | 它**位於神經元內部**（不是在外面） |
| takes the total input numbers, **adds them up** | 把輸入的數字**加總**起來 |
| **decides if the neuron should turn on or send data ahead** | 決定這個神經元**要不要開啟／要不要把資料往下送** |
| adds a twist called **non-linearity** | 加入一個叫做**非線性**的轉折 |
| so the network can **learn hard patterns** | 讓網路能**學困難的模式** |

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 480" width="100%" style="max-width:760px;height:auto" role="img" aria-label="四種常見激勵函數的圖形總覽"><defs><marker id="ar-ao" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><rect x="20" y="60" width="340" height="190" rx="8" fill="#ffffff" stroke="#d8dee4" stroke-width="1"/><rect x="400" y="60" width="340" height="190" rx="8" fill="#ffffff" stroke="#d8dee4" stroke-width="1"/><rect x="20" y="280" width="340" height="190" rx="8" fill="#ffffff" stroke="#d8dee4" stroke-width="1"/><rect x="400" y="280" width="340" height="190" rx="8" fill="#ffffff" stroke="#d8dee4" stroke-width="1"/><line x1="53.0" y1="115.0" x2="287.0" y2="115.0" stroke="#d8dee4" stroke-width="1" stroke-dasharray="4 4"/><line x1="170" y1="205" x2="288" y2="205" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-ao)"/><line x1="170" y1="205" x2="170" y2="109" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-ao)"/><text x="296" y="221" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">a</text><text x="156" y="105" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">y</text><polyline points="53.0,205.0 170.0,205.0 170.0,115.0 287.0,115.0" fill="none" stroke="#2c6fb1" stroke-width="3"/><text x="190" y="84" font-size="13.5" fill="#2c6fb1" text-anchor="middle" font-weight="bold">① TLU 階梯 step</text><text x="190" y="240" font-size="12" fill="#57606a" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">y = 1 if a ≥ θ else 0</text><line x1="550" y1="205" x2="668" y2="205" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-ao)"/><line x1="550" y1="205" x2="550" y2="109" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-ao)"/><text x="676" y="221" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">a</text><text x="536" y="105" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">y</text><polyline points="442.0,205.0 550.0,205.0 649.0,117.0" fill="none" stroke="#c0392b" stroke-width="3"/><text x="570" y="84" font-size="13.5" fill="#c0392b" text-anchor="middle" font-weight="bold">② ReLU</text><text x="570" y="240" font-size="12" fill="#57606a" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">f(a) = max(0, a)</text><line x1="29.599999999999994" y1="430.0" x2="310.4" y2="430.0" stroke="#d8dee4" stroke-width="1" stroke-dasharray="4 4"/><line x1="29.599999999999994" y1="300.0" x2="310.4" y2="300.0" stroke="#d8dee4" stroke-width="1" stroke-dasharray="4 4"/><line x1="170" y1="430" x2="292" y2="430" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-ao)"/><line x1="170" y1="430" x2="170" y2="310" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-ao)"/><text x="300" y="446" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">a</text><text x="156" y="306" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">σ(a)</text><polyline points="29.60,429.29 31.36,429.24 33.11,429.19 34.87,429.13 36.62,429.08 38.38,429.01 40.13,428.95 41.88,428.88 43.64,428.80 45.39,428.73 47.15,428.64 48.90,428.55 50.66,428.45 52.41,428.35 54.17,428.24 55.92,428.13 57.68,428.00 59.43,427.87 61.19,427.73 62.94,427.58 64.70,427.42 66.45,427.25 68.21,427.07 69.97,426.88 71.72,426.67 73.47,426.46 75.23,426.23 76.98,425.98 78.74,425.72 80.50,425.44 82.25,425.15 84.00,424.83 85.76,424.50 87.52,424.15 89.27,423.78 91.02,423.38 92.78,422.96 94.53,422.51 96.29,422.04 98.05,421.54 99.80,421.01 101.55,420.45 103.31,419.86 105.06,419.24 106.82,418.58 108.57,417.88 110.33,417.15 112.09,416.38 113.84,415.56 115.59,414.71 117.35,413.81 119.10,412.86 120.86,411.87 122.62,410.84 124.37,409.75 126.12,408.61 127.88,407.43 129.64,406.19 131.39,404.90 133.14,403.55 134.90,402.16 136.66,400.71 138.41,399.21 140.17,397.66 141.92,396.05 143.67,394.39 145.43,392.69 147.19,390.94 148.94,389.14 150.69,387.30 152.45,385.41 154.21,383.49 155.96,381.53 157.72,379.54 159.47,377.52 161.22,375.47 162.98,373.40 164.74,371.32 166.49,369.22 168.24,367.11 170.00,365.00 171.75,362.89 173.51,360.78 175.27,358.68 177.02,356.60 178.78,354.53 180.53,352.48 182.28,350.46 184.04,348.47 185.79,346.51 187.55,344.59 189.31,342.70 191.06,340.86 192.81,339.06 194.57,337.31 196.32,335.61 198.08,333.95 199.84,332.34 201.59,330.79 203.34,329.29 205.10,327.84 206.86,326.45 208.61,325.10 210.37,323.81 212.12,322.57 213.88,321.39 215.63,320.25 217.38,319.16 219.14,318.13 220.90,317.14 222.65,316.19 224.41,315.29 226.16,314.44 227.92,313.62 229.67,312.85 231.42,312.12 233.18,311.42 234.94,310.76 236.69,310.14 238.45,309.55 240.20,308.99 241.95,308.46 243.71,307.96 245.47,307.49 247.22,307.04 248.97,306.62 250.73,306.22 252.48,305.85 254.24,305.50 256.00,305.17 257.75,304.85 259.50,304.56 261.26,304.28 263.01,304.02 264.77,303.77 266.52,303.54 268.28,303.33 270.03,303.12 271.79,302.93 273.55,302.75 275.30,302.58 277.06,302.42 278.81,302.27 280.56,302.13 282.32,302.00 284.08,301.87 285.83,301.76 287.58,301.65 289.34,301.55 291.10,301.45 292.85,301.36 294.61,301.27 296.36,301.20 298.12,301.12 299.87,301.05 301.62,300.99 303.38,300.92 305.13,300.87 306.89,300.81 308.64,300.76 310.40,300.71" fill="none" stroke="#6f42c1" stroke-width="3" stroke-linecap="round"/><text x="190" y="304" font-size="13.5" fill="#6f42c1" text-anchor="middle" font-weight="bold">③ Sigmoid</text><text x="190" y="460" font-size="12" fill="#57606a" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">σ(a) = 1 / (1 + e⁻ᵃ)</text><line x1="480" y1="445" x2="580" y2="445" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-ao)"/><line x1="480" y1="445" x2="480" y2="337" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-ao)"/><text x="588" y="461" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">a</text><text x="466" y="333" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">eᵃ</text><polyline points="405.00,441.28 406.29,441.19 407.59,441.11 408.88,441.03 410.18,440.94 411.47,440.85 412.76,440.76 414.06,440.67 415.35,440.57 416.64,440.48 417.94,440.38 419.23,440.28 420.52,440.18 421.82,440.07 423.11,439.96 424.41,439.85 425.70,439.74 426.99,439.63 428.29,439.51 429.58,439.39 430.88,439.27 432.17,439.14 433.46,439.01 434.76,438.88 436.05,438.75 437.34,438.61 438.64,438.48 439.93,438.33 441.23,438.19 442.52,438.04 443.81,437.89 445.11,437.73 446.40,437.57 447.69,437.41 448.99,437.25 450.28,437.08 451.57,436.91 452.87,436.73 454.16,436.55 455.46,436.36 456.75,436.18 458.04,435.98 459.34,435.79 460.63,435.59 461.93,435.38 463.22,435.17 464.51,434.96 465.81,434.74 467.10,434.51 468.39,434.29 469.69,434.05 470.98,433.81 472.27,433.57 473.57,433.32 474.86,433.07 476.16,432.81 477.45,432.54 478.74,432.27 480.04,431.99 481.33,431.71 482.62,431.42 483.92,431.12 485.21,430.82 486.51,430.51 487.80,430.20 489.09,429.87 490.39,429.54 491.68,429.21 492.98,428.86 494.27,428.51 495.56,428.15 496.86,427.78 498.15,427.41 499.44,427.02 500.74,426.63 502.03,426.23 503.32,425.82 504.62,425.41 505.91,424.98 507.21,424.54 508.50,424.10 509.79,423.64 511.09,423.17 512.38,422.70 513.67,422.21 514.97,421.72 516.26,421.21 517.56,420.69 518.85,420.16 520.14,419.62 521.44,419.07 522.73,418.50 524.02,417.92 525.32,417.33 526.61,416.73 527.91,416.11 529.20,415.48 530.49,414.84 531.79,414.18 533.08,413.51 534.38,412.82 535.67,412.12 536.96,411.41 538.26,410.67 539.55,409.93 540.84,409.16 542.14,408.38 543.43,407.58 544.73,406.77 546.02,405.93 547.31,405.08 548.61,404.21 549.90,403.32 551.19,402.41 552.49,401.49 553.78,400.54 555.08,399.57 556.37,398.58 557.66,397.57 558.96,396.53 560.25,395.48 561.54,394.40 562.84,393.29 564.13,392.17 565.42,391.02 566.72,389.84 568.01,388.64 569.31,387.41 570.60,386.15 571.89,384.87 573.19,383.56 574.48,382.22 575.77,380.85 577.07,379.45 578.36,378.02 579.66,376.56 580.95,375.07 582.24,373.55 583.54,371.99 584.83,370.40 586.12,368.77 587.42,367.11 588.71,365.42 590.01,363.68 591.30,361.91 592.59,360.10 593.89,358.25 595.18,356.36 596.48,354.42 597.77,352.45 599.06,350.43 600.36,348.37 601.65,346.26 602.94,344.11 604.24,341.91 605.53,339.67 606.83,337.37 608.12,335.02 609.41,332.63 610.71,330.18 612.00,327.67" fill="none" stroke="#d97706" stroke-width="3" stroke-linecap="round"/><text x="570" y="304" font-size="13.5" fill="#d97706" text-anchor="middle" font-weight="bold">④ Softmax 的分子 eᵃ</text><text x="570" y="460" font-size="12" fill="#57606a" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">pᵢ = e^zᵢ / Σⱼ e^zⱼ</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 13：<b>四種常見激勵函數總覽</b>。① 階梯（TLU）：不可微，僅適合早期感知機；② ReLU：隱藏層首選，快且不易梯度消失；③ Sigmoid：把值壓到 (0,1)，用於二元分類輸出；④ Softmax 的指數分子：放大差距並保證為正，用於多類別輸出。</figcaption>
</figure>

### 7.1 激勵函數的四大作用

| 作用 | 說明 |
|---|---|
| ① 決定輸出 | 把加權總和 a 轉成這個神經元實際的輸出 y |
| ② 引入非線性 | **最重要**：沒有它，多層網路等價於一層線性模型 |
| ③ 控制輸出範圍 | 例如 Sigmoid 壓到 (0,1)、ReLU 壓到 [0, ∞) |
| ④ 影響訓練 | 可不可微、梯度會不會消失，直接決定網路能不能訓練得動 |

### 7.2 本節會學到的四種激勵函數（先看總表）

| 激勵函數 | 公式 | 輸出範圍 | 用在哪裡 | 備註 |
|---|---|---|---|---|
| **TLU**（階梯） | `y = 1 if a ≥ θ else 0` | {0, 1} | 早期感知機 | 不可微，解不了 XOR |
| **ReLU** | `f(a) = max(0, a)` | [0, ∞) | **隱藏層**（預設） | 快、正區間梯度固定 1 |
| **Sigmoid** | `σ(a) = 1/(1+e⁻ᵃ)` | (0, 1) | 二元分類的**輸出層** | 兩端飽和 → 梯度消失 |
| **Softmax** | `pᵢ = e^zᵢ / Σⱼ e^zⱼ` | (0, 1) 且總和 1 | **多類別分類的輸出層** | 輸出可視為機率分布 |

> **考點**：
> - 激勵函數位於**神經元內部**，處理的是「加權總和之後」的值。
> - 它存在的**關鍵理由是引入非線性**（non-linearity），讓網路能學 hard patterns。
> - 若把激勵函數拿掉，整個深層網路會退化成**線性模型**。

---

## 8. Threshold Logic Unit（TLU）（PDF p9–p10）

<!-- p: 9–10 -->

原稿 p9 是結構圖、p10 是圖形，兩頁合起來才完整。

### 8.1 TLU 的結構（p9）

p9 的圖上標示了四個部位：**inputs（輸入）、weights（權重）、activation（激勵）、output（輸出）**，
並寫出兩條式子：

```
a = Σ(i=1..n) wᵢ xᵢ
y = 1 if a ≥ θ
    0 if a < θ
```

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 300" width="100%" style="max-width:760px;height:auto" role="img" aria-label="Threshold Logic Unit 的結構"><defs><marker id="ar-tl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><text x="30" y="34" font-size="14" fill="#c0392b" text-anchor="start" font-weight="bold">TLU：最早的「會學習的神經元」（McCulloch–Pitts / Rosenblatt 感知機）</text><circle cx="90" cy="110" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="115" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>1</sub></text><line x1="107" y1="110" x2="214" y2="149.0" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-tl)"/><text x="158" y="102" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>1</sub></text><circle cx="90" cy="160" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="165" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>2</sub></text><line x1="107" y1="160" x2="214" y2="160.0" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-tl)"/><text x="158" y="152" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>2</sub></text><circle cx="90" cy="210" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="215" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>3</sub></text><line x1="107" y1="210" x2="214" y2="171.0" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-tl)"/><text x="158" y="202" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>3</sub></text><text x="90" y="244" font-size="12" fill="#2c6fb1" text-anchor="middle" font-weight="normal">輸入 features</text><circle cx="246" cy="160" r="30" fill="#ffffff" stroke="#2c6fb1" stroke-width="2.2"/><text x="246" y="168" font-size="22" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">Σ</text><line x1="278" y1="160" x2="336" y2="160" stroke="#57606a" stroke-width="1.8" marker-end="url(#ar-tl)"/><text x="307" y="142" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">a</text><rect x="340" y="122" width="150" height="76" rx="6" fill="#ffffff" stroke="#d97706" stroke-width="2"/><polyline points="352,176 400,176 400,144 476,144" fill="none" stroke="#d97706" stroke-width="2.6"/><text x="415" y="118" font-size="12" fill="#d97706" text-anchor="middle" font-weight="bold">step 階梯函數</text><text x="415" y="214" font-size="12" fill="#d97706" text-anchor="middle" font-weight="normal">θ = threshold 閾值</text><line x1="492" y1="160" x2="556" y2="160" stroke="#57606a" stroke-width="1.8" marker-end="url(#ar-tl)"/><text x="566" y="166" font-size="15" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">y ∈ {0, 1}</text><text x="566" y="190" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">只有「開／關」兩態</text><text x="30" y="282" font-size="13" fill="#0f766e" text-anchor="start" font-weight="normal">y = 1 if Σwᵢxᵢ + b ≥ θ, else 0　→　線性決策邊界：把輸入空間切一半（能解 AND / OR，不能解 XOR）</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 5：<b>Threshold Logic Unit（TLU）</b>（原稿 p9）。加權總和超過閾值 θ 才輸出 1，否則輸出 0；它只能畫出一條直線決策邊界，所以能解 AND／OR，解不了 XOR（這正是多層網路與非線性激勵函數存在的理由）。</figcaption>
</figure>

| 符號 | 意義 |
|---|---|
| `x₁ … xₙ` | n 個輸入（特徵） |
| `w₁ … wₙ` | 對應的權重 |
| `a` | 加權總和（有些教材寫成 net 或 z） |
| `θ`（theta） | **threshold 閾值** |
| `y` | 輸出，只有 **0 或 1** 兩種 |

### 8.2 TLU 的激勵函數圖形（p10）

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 320" width="100%" style="max-width:760px;height:auto" role="img" aria-label="TLU 的階梯函數圖形"><defs><marker id="ar-tg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><line x1="340" y1="82.0" x2="340" y2="256" stroke="#d8dee4" stroke-width="1" stroke-dasharray="4 4"/><line x1="184.20000000000002" y1="250" x2="184.20000000000002" y2="100.0" stroke="#d8dee4" stroke-width="1" stroke-dasharray="4 4"/><line x1="184.20000000000002" y1="130" x2="569.6" y2="130" stroke="#d8dee4" stroke-width="1" stroke-dasharray="4 4"/><line x1="340" y1="250" x2="600" y2="250" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-tg)"/><line x1="340" y1="250" x2="340" y2="74" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-tg)"/><text x="608" y="266" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">a</text><text x="326" y="70" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">y</text><polyline points="184.20000000000002,250 340.0,250 340.0,130 569.6,130" fill="none" stroke="#c0392b" stroke-width="3.4"/><circle cx="340.0" cy="250" r="4.5" fill="#ffffff" stroke="#c0392b" stroke-width="2.4"/><circle cx="340.0" cy="130" r="4.5" fill="#c0392b" stroke="#c0392b" stroke-width="2.4"/><text x="340.0" y="272" font-size="15" fill="#24292f" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">θ</text><text x="315.4" y="136" font-size="14" fill="#c0392b" text-anchor="end" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">1</text><text x="315.4" y="256" font-size="14" fill="#c0392b" text-anchor="end" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">0</text><text x="184.20000000000002" y="276" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">未達閾值 → 0</text><text x="372.8" y="116" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">達到閾值 → 1</text><text x="560" y="70" font-size="13" fill="#57606a" text-anchor="start" font-weight="normal">TLU 的輸出只有 0 與 1，</text><text x="560" y="90" font-size="13" fill="#57606a" text-anchor="start" font-weight="normal">在 θ 處「跳」上去（不連續、</text><text x="560" y="110" font-size="13" fill="#57606a" text-anchor="start" font-weight="normal">不可微分）。</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 6：<b>TLU 的階梯函數（step function）</b>（原稿 p10）。輸出非 0 即 1，在閾值 θ 處不連續且不可微分——這讓「梯度下降」無法直接使用，因而後續發展出 Sigmoid、ReLU 等可微的激勵函數。</figcaption>
</figure>

原稿 p10 只畫了 y 對 a 的圖（一個**階梯**：a 未達 θ 時 y = 0，達到 θ 時跳到 1）。

### 8.3 TLU 的歷史與限制

- TLU 是**最早能「學習」的神經元模型**：McCulloch–Pitts 神經元（1943）提出雛形，
  Rosenblatt 的**感知機（Perceptron, 1958）**把它變成可訓練的演算法。
- **限制一：不可微**。階梯函數在 θ 處不連續，梯度不是 0 就是不存在，
  因此**無法直接使用梯度下降**。
- **限制二：只能解線性可分的問題**。TLU 畫出的是一條**直線決策邊界**：
  能解 AND、OR，但**解不了 XOR**（這是 1969 年 Minsky 與 Papert 指出的著名瓶頸）。

> **考點**：
> 1. TLU 的輸出只有 **0 與 1**（非黑即白），不是機率。
> 2. TLU 的兩個致命傷：**不可微**、**只能線性分割（解不了 XOR）**。
> 3. 也因為這兩個限制，才有後面的 Sigmoid（可微）與多層網路（非線性）的發展。

---

## 9. Rectified Linear Units（ReLU）（PDF p11–p12）

<!-- p: 11–12 -->

原稿 p11 是結構圖、p12 是圖形。

### 9.1 ReLU 的結構（p11）

p11 的圖與 TLU 幾乎一樣（inputs → weights → activation → output），但式子換成：

```
a = Σ(i=1..n) wᵢ xᵢ
y = a = Σ(i=1..n) wᵢ xᵢ
```

原稿把 y 直接寫成 a（也就是**正值原樣通過**）。標準寫法就是：

```
f(a) = max(0, a)
```

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 300" width="100%" style="max-width:760px;height:auto" role="img" aria-label="ReLU 神經元結構"><defs><marker id="ar-rl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><text x="30" y="34" font-size="14" fill="#c0392b" text-anchor="start" font-weight="bold">ReLU：目前深度網路最常用的激勵函數（計算快、不易梯度消失）</text><circle cx="90" cy="110" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="115" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>1</sub></text><line x1="107" y1="110" x2="214" y2="149.0" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-rl)"/><text x="158" y="102" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>1</sub></text><circle cx="90" cy="160" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="165" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>2</sub></text><line x1="107" y1="160" x2="214" y2="160.0" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-rl)"/><text x="158" y="152" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>2</sub></text><circle cx="90" cy="210" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="215" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>3</sub></text><line x1="107" y1="210" x2="214" y2="171.0" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-rl)"/><text x="158" y="202" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>3</sub></text><text x="90" y="244" font-size="12" fill="#2c6fb1" text-anchor="middle" font-weight="normal">輸入 features</text><circle cx="246" cy="160" r="30" fill="#ffffff" stroke="#2c6fb1" stroke-width="2.2"/><text x="246" y="168" font-size="22" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">Σ</text><line x1="278" y1="160" x2="336" y2="160" stroke="#57606a" stroke-width="1.8" marker-end="url(#ar-rl)"/><text x="307" y="142" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">a</text><rect x="340" y="122" width="150" height="76" rx="6" fill="#ffffff" stroke="#c0392b" stroke-width="2"/><polyline points="352,176 415,176 476,144" fill="none" stroke="#c0392b" stroke-width="2.8"/><text x="415" y="118" font-size="12" fill="#c0392b" text-anchor="middle" font-weight="bold">ReLU（hinge）</text><text x="415" y="214" font-size="13" fill="#c0392b" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">max(0, a)</text><line x1="492" y1="160" x2="556" y2="160" stroke="#57606a" stroke-width="1.8" marker-end="url(#ar-rl)"/><text x="566" y="166" font-size="15" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">y ≥ 0</text><text x="566" y="190" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">負值一律歸 0</text><text x="30" y="282" font-size="13" fill="#0f766e" text-anchor="start" font-weight="normal">f(a) = max(0, a)　→　優點：只做比較、運算極快，正區間梯度固定為 1（不會梯度消失）；缺點：負區間梯度為 0，可能出現 dead neuron</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 7：<b>ReLU 神經元</b>（原稿 p11）。輸出 <code>y = max(0, a)</code>：負的加權總和一律壓成 0，正的則原樣通過。運算只是「比較」所以極快，且正區間梯度恆為 1，是深層網路能訓練得動的關鍵之一。</figcaption>
</figure>

| 情況 | 輸出 | 說明 |
|---|---|---|
| `a ≥ 0` | `y = a` | 原樣通過（斜率 1） |
| `a < 0` | `y = 0` | 直接壓成 0（「整流」） |

### 9.2 ReLU 的圖形（p12）

原稿 p12 畫了兩張圖對照：一張是**線性**（一條斜直線），一張是 **ReLU**（0 的左半壓平、右半斜上去）。

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 360" width="100%" style="max-width:760px;height:auto" role="img" aria-label="線性激勵與 ReLU 的圖形比較"><defs><marker id="ar-rg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><rect x="74.0" y="99.0" width="232.0" height="232.0" rx="4" fill="#ffffff" stroke="#eaeef2" stroke-width="1"/><line x1="190" y1="215" x2="306.0" y2="215" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-rg)"/><line x1="190" y1="215" x2="190" y2="99.0" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-rg)"/><text x="314.0" y="231" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">a</text><text x="176" y="95.0" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">f(a)</text><text x="82.0" y="323.0" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">−2</text><text x="298.0" y="323.0" font-size="12" fill="#57606a" text-anchor="end" font-weight="normal">2</text><rect x="454.0" y="99.0" width="232.0" height="232.0" rx="4" fill="#ffffff" stroke="#eaeef2" stroke-width="1"/><line x1="570" y1="215" x2="686.0" y2="215" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-rg)"/><line x1="570" y1="215" x2="570" y2="99.0" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-rg)"/><text x="694.0" y="231" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">a</text><text x="556" y="95.0" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">f(a)</text><text x="462.0" y="323.0" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">−2</text><text x="678.0" y="323.0" font-size="12" fill="#57606a" text-anchor="end" font-weight="normal">2</text><text x="190" y="58" font-size="14" fill="#2c6fb1" text-anchor="middle" font-weight="bold">① 線性激勵 f(a) = a</text><line x1="74.0" y1="331.0" x2="306.0" y2="99.0" stroke="#2c6fb1" stroke-width="3.2"/><text x="190" y="340" font-size="12.5" fill="#57606a" text-anchor="middle" font-weight="normal">整條斜直線：疊再多層仍等價於一層線性轉換</text><text x="570" y="58" font-size="14" fill="#c0392b" text-anchor="middle" font-weight="bold">② ReLU f(a) = max(0, a)</text><polyline points="454.0,215 570,215 686.0,99.0" fill="none" stroke="#c0392b" stroke-width="3.2"/><text x="470.0" y="200" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">全部壓成 0</text><text x="610" y="150" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">原樣通過（斜率 1）</text><text x="570" y="340" font-size="12.5" fill="#57606a" text-anchor="middle" font-weight="normal">在 0 折彎 → 非線性，這是深度網路能擬合複雜函數的關鍵</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 8：<b>線性激勵 vs ReLU</b>（原稿 p12）。線性激勵是一條直線，多層堆疊後仍只是線性；ReLU 在 0 處折彎，把輸入空間切成兩個行為不同的區域，因此能逼近非線性函數。</figcaption>
</figure>

### 9.3 為什麼 ReLU 成為主流

| 優點 | 說明 |
|---|---|
| 計算極快 | 只做一次比較（`max`），不像 Sigmoid 要算指數 |
| 不會梯度消失（正區間） | 正區間的導數固定是 **1**，誤差可以穩定往回傳 |
| 稀疏性 | 負值輸出 0，讓網路只啟動部分神經元，效率更好 |

| 缺點 | 說明 |
|---|---|
| Dead neuron（神經元死亡） | 若某神經元的加權總和長期為負，梯度永遠是 0，它就再也不會被更新 |
| 輸出無上界 | 輸出可以是任意大的正數（不像 Sigmoid 有界） |

> **考點**：
> 1. ReLU 的公式是 **`max(0, a)`**；負值歸零、正值原樣通過。
> 2. ReLU 的導數在正區間是 **1**（不是 0），所以不會梯度消失。
> 3. 「Dead neuron」是 ReLU 的典型問題，原因就是**負區間梯度為 0**。

---

## 10. Sigmoid Function（PDF p13–p14）

<!-- p: 13–14 -->

### 10.1 Sigmoid 的結構（p13）

p13 的圖上標示：inputs / weights / activation / output，並寫出兩條式子：

```
a = Σ(i=0 (or 1) .. n) wᵢ xᵢ
y = σ(a) = 1 / (1 + e⁻ᵃ)
```

（`i = 0 (or 1)` 指的是：偏置項有時從 0 開始編號，有時從 1 開始，兩種寫法都有人用。）

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 300" width="100%" style="max-width:760px;height:auto" role="img" aria-label="Sigmoid 神經元結構"><defs><marker id="ar-sg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><text x="30" y="34" font-size="14" fill="#c0392b" text-anchor="start" font-weight="bold">Sigmoid：把任意實數壓縮到 (0, 1)，可當成「機率」</text><circle cx="90" cy="110" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="115" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>1</sub></text><line x1="107" y1="110" x2="214" y2="149.0" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-sg)"/><text x="158" y="102" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>1</sub></text><circle cx="90" cy="160" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="165" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>2</sub></text><line x1="107" y1="160" x2="214" y2="160.0" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-sg)"/><text x="158" y="152" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>2</sub></text><circle cx="90" cy="210" r="15" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="90" y="215" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x<sub>3</sub></text><line x1="107" y1="210" x2="214" y2="171.0" stroke="#2c6fb1" stroke-width="1.6" marker-end="url(#ar-sg)"/><text x="158" y="202" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">w<sub>3</sub></text><text x="90" y="244" font-size="12" fill="#2c6fb1" text-anchor="middle" font-weight="normal">輸入 features</text><circle cx="246" cy="160" r="30" fill="#ffffff" stroke="#2c6fb1" stroke-width="2.2"/><text x="246" y="168" font-size="22" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">Σ</text><line x1="278" y1="160" x2="336" y2="160" stroke="#57606a" stroke-width="1.8" marker-end="url(#ar-sg)"/><text x="307" y="142" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">a</text><rect x="340" y="122" width="150" height="76" rx="6" fill="#ffffff" stroke="#6f42c1" stroke-width="2"/><polyline points="354,180 368,172 388,160 415,140 445,128 476,122" fill="none" stroke="#6f42c1" stroke-width="2.8"/><text x="415" y="118" font-size="12" fill="#6f42c1" text-anchor="middle" font-weight="bold">S 型曲線</text><text x="415" y="214" font-size="13" fill="#6f42c1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">1 / (1 + e⁻ᵃ)</text><line x1="492" y1="160" x2="556" y2="160" stroke="#57606a" stroke-width="1.8" marker-end="url(#ar-sg)"/><text x="566" y="166" font-size="15" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">y ∈ (0, 1)</text><text x="566" y="190" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">可解讀為機率</text><text x="30" y="282" font-size="13" fill="#0f766e" text-anchor="start" font-weight="normal">σ(a) = 1 / (1 + e⁻ᵃ)　→　平滑、處處可微分（可做梯度下降）；但兩端飽和、梯度趨近 0，深層網路易梯度消失，故隱藏層多用 ReLU</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 9：<b>Sigmoid 神經元</b>（原稿 p13）。把加權總和 a 壓進 (0, 1) 區間，輸出可解讀為機率；曲線平滑可微，但輸入很大或很小時梯度趨近 0，這是深層網路改用 ReLU 的主因。</figcaption>
</figure>

### 10.2 Sigmoid 的圖形（p14）

原稿 p14 同時放了 **Sigmoid** 與 **Softmax** 兩張圖（頁面上標題就是這兩行）。

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 350" width="100%" style="max-width:760px;height:auto" role="img" aria-label="Sigmoid 函數圖形"><defs><marker id="ar-sgg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><line x1="34.0" y1="255.0" x2="566.0" y2="255.0" stroke="#d8dee4" stroke-width="1" stroke-dasharray="4 4"/><line x1="34.0" y1="105.0" x2="566.0" y2="105.0" stroke="#d8dee4" stroke-width="1" stroke-dasharray="4 4"/><line x1="300" y1="255" x2="535" y2="255" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-sgg)"/><line x1="300" y1="255" x2="300" y2="95" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-sgg)"/><text x="543" y="271" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">a</text><text x="286" y="91" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">σ(a)</text><polyline points="64.40,254.70 67.34,254.67 70.29,254.65 73.23,254.62 76.18,254.59 79.12,254.55 82.07,254.52 85.01,254.48 87.96,254.44 90.90,254.39 93.85,254.34 96.79,254.29 99.74,254.23 102.69,254.17 105.63,254.10 108.58,254.03 111.52,253.96 114.46,253.87 117.41,253.78 120.35,253.68 123.30,253.58 126.25,253.47 129.19,253.34 132.13,253.21 135.08,253.07 138.03,252.92 140.97,252.75 143.91,252.57 146.86,252.38 149.81,252.17 152.75,251.95 155.69,251.71 158.64,251.45 161.59,251.17 164.53,250.87 167.47,250.55 170.42,250.20 173.37,249.83 176.31,249.43 179.25,249.00 182.20,248.53 185.14,248.04 188.09,247.50 191.04,246.93 193.98,246.32 196.92,245.66 199.87,244.96 202.81,244.21 205.76,243.41 208.71,242.55 211.65,241.64 214.59,240.67 217.54,239.63 220.48,238.53 223.43,237.35 226.38,236.11 229.32,234.79 232.27,233.40 235.21,231.93 238.15,230.37 241.10,228.74 244.04,227.02 246.99,225.21 249.94,223.31 252.88,221.33 255.82,219.27 258.77,217.12 261.72,214.88 264.66,212.56 267.61,210.16 270.55,207.69 273.50,205.14 276.44,202.53 279.38,199.86 282.33,197.13 285.27,194.35 288.22,191.53 291.17,188.68 294.11,185.80 297.06,182.90 300.00,180.00 302.94,177.10 305.89,174.20 308.83,171.32 311.78,168.47 314.73,165.65 317.67,162.87 320.62,160.14 323.56,157.47 326.50,154.86 329.45,152.31 332.39,149.84 335.34,147.44 338.29,145.12 341.23,142.88 344.17,140.73 347.12,138.67 350.06,136.69 353.01,134.79 355.96,132.98 358.90,131.26 361.85,129.63 364.79,128.07 367.74,126.60 370.68,125.21 373.62,123.89 376.57,122.65 379.51,121.47 382.46,120.37 385.41,119.33 388.35,118.36 391.30,117.45 394.24,116.59 397.19,115.79 400.13,115.04 403.07,114.34 406.02,113.68 408.96,113.07 411.91,112.50 414.86,111.96 417.80,111.47 420.75,111.00 423.69,110.57 426.63,110.17 429.58,109.80 432.52,109.45 435.47,109.13 438.41,108.83 441.36,108.55 444.31,108.29 447.25,108.05 450.19,107.83 453.14,107.62 456.09,107.43 459.03,107.25 461.98,107.08 464.92,106.93 467.87,106.79 470.81,106.66 473.75,106.53 476.70,106.42 479.64,106.32 482.59,106.22 485.53,106.13 488.48,106.04 491.43,105.97 494.37,105.90 497.31,105.83 500.26,105.77 503.21,105.71 506.15,105.66 509.10,105.61 512.04,105.56 514.99,105.52 517.93,105.48 520.88,105.45 523.82,105.41 526.76,105.38 529.71,105.35 532.66,105.33 535.60,105.30" fill="none" stroke="#6f42c1" stroke-width="3.4" stroke-linecap="round"/><text x="40.0" y="97.0" font-size="13" fill="#57606a" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">1</text><text x="40.0" y="247.0" font-size="13" fill="#57606a" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">0</text><line x1="300.0" y1="255.0" x2="300.0" y2="180.0" stroke="#d8dee4" stroke-width="1" stroke-dasharray="3 3"/><line x1="300.0" y1="180.0" x2="34.0" y2="180.0" stroke="#d8dee4" stroke-width="1" stroke-dasharray="3 3"/><circle cx="300.0" cy="180.0" r="5" fill="#ffffff" stroke="#6f42c1" stroke-width="2.4"/><text x="308.0" y="172.0" font-size="12.5" fill="#6f42c1" text-anchor="start" font-weight="normal">σ(0) = 0.5</text><text x="300.0" y="275" font-size="13" fill="#57606a" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">0</text><text x="560" y="96" font-size="13" fill="#57606a" text-anchor="start" font-weight="normal">輸出永遠落在 0 與 1 之間</text><text x="560" y="116" font-size="13" fill="#57606a" text-anchor="start" font-weight="normal">→ 可直接當作「是／否」的機率</text><text x="560" y="150" font-size="13" fill="#57606a" text-anchor="start" font-weight="normal">中間段近似線性、好訓練；</text><text x="560" y="170" font-size="13" fill="#57606a" text-anchor="start" font-weight="normal">兩端飽和（梯度≈0）→ 梯度消失</text><text x="560" y="204" font-size="13" fill="#57606a" text-anchor="start" font-weight="normal">用於：二元分類的輸出層、</text><text x="560" y="224" font-size="13" fill="#57606a" text-anchor="start" font-weight="normal">早期網路的隱藏層</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 10：<b>Sigmoid 函數圖形</b>（原稿 p14）。輸入 0 時輸出 0.5；往兩端分別趨近 1 與 0，但永遠不會到達，所以梯度在兩端幾乎為 0。這條曲線就是把「分數」變成「機率」的標準工具。</figcaption>
</figure>

### 10.3 Sigmoid 的特性與用途

| 特性 | 說明 |
|---|---|
| 輸出範圍 | **(0, 1)**——永遠不會是 0 或 1，但可以無限接近 |
| `σ(0) = 0.5` | 輸入 0 時輸出正好一半，常被當成決策門檻 |
| 可微 | 處處平滑可微分，所以可以用梯度下降訓練 |
| 導數形式漂亮 | `σ'(a) = σ(a)·(1 − σ(a))`，好算 |
| 兩端飽和 | 輸入很大或很小時，導數趨近 **0** → **梯度消失（vanishing gradient）** |

**常見用途**：

- **二元分類的輸出層**：輸出值可直接解讀為「是」的機率（> 0.5 判為正類）。
- 早期網路的隱藏層，或需要輸出被限制在 (0, 1) 的場合（例如閘門、注意力權重）。
- **不適合**當深層網路的隱藏層：兩端飽和會讓梯度消失，訓練不動 → 改用 ReLU。

> **考點**：
> 1. Sigmoid 的值域是 **(0, 1)**，`σ(0) = 0.5`。
> 2. 它的主要缺點是**梯度消失**（兩端飽和），不是「輸出不是機率」。
> 3. 二元分類的輸出層用 **Sigmoid**；多類別用 **Softmax**。

---

## 11. Softmax Function（PDF p15–p16）

<!-- p: 15–16 -->

### 11.1 Softmax 的結構（p15）

p15 的圖把「一組輸入」通過 activation 後，得到**一組輸出**（不是單一個 y），
代表它處理的是**多類別**的輸出層。

```
pᵢ = e^zᵢ / Σⱼ e^zⱼ        （i = 1 … K，K 是類別數）
```

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 380" width="100%" style="max-width:760px;height:auto" role="img" aria-label="Softmax 的計算流程與輸出機率"><defs><marker id="ar-sm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><text x="30" y="34" font-size="14" fill="#c0392b" text-anchor="start" font-weight="bold">Softmax：把「一組分數（logits）」轉成「一組加總為 1 的機率」——多類別分類的標準輸出層</text><circle cx="70" cy="108" r="17" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="70" y="113" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">z<sub>1</sub></text><text x="70" y="82" font-size="12" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">2.0</text><line x1="89" y1="108" x2="146" y2="108" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-sm)"/><rect x="150" y="86" width="92" height="44" rx="6" fill="#ffffff" stroke="#d97706" stroke-width="1.8"/><text x="196" y="113" font-size="13" fill="#d97706" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">exp</text><line x1="244" y1="108" x2="296" y2="108" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-sm)"/><rect x="300" y="86" width="150" height="44" rx="6" fill="#ffffff" stroke="#6f42c1" stroke-width="1.8"/><text x="375" y="113" font-size="13" fill="#6f42c1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">÷ Σ<sub>j</sub> e<sup>z<sub>j</sub></sup></text><line x1="452" y1="108" x2="500" y2="108" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-sm)"/><text x="510" y="114" font-size="15" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">p<sub>1</sub> = 0.659</text><circle cx="70" cy="170" r="17" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="70" y="175" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">z<sub>2</sub></text><text x="70" y="144" font-size="12" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">1.0</text><line x1="89" y1="170" x2="146" y2="170" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-sm)"/><rect x="150" y="148" width="92" height="44" rx="6" fill="#ffffff" stroke="#d97706" stroke-width="1.8"/><text x="196" y="175" font-size="13" fill="#d97706" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">exp</text><line x1="244" y1="170" x2="296" y2="170" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-sm)"/><rect x="300" y="148" width="150" height="44" rx="6" fill="#ffffff" stroke="#6f42c1" stroke-width="1.8"/><text x="375" y="175" font-size="13" fill="#6f42c1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">÷ Σ<sub>j</sub> e<sup>z<sub>j</sub></sup></text><line x1="452" y1="170" x2="500" y2="170" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-sm)"/><text x="510" y="176" font-size="15" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">p<sub>2</sub> = 0.242</text><circle cx="70" cy="232" r="17" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="70" y="237" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">z<sub>3</sub></text><text x="70" y="206" font-size="12" fill="#2c6fb1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">0.1</text><line x1="89" y1="232" x2="146" y2="232" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-sm)"/><rect x="150" y="210" width="92" height="44" rx="6" fill="#ffffff" stroke="#d97706" stroke-width="1.8"/><text x="196" y="237" font-size="13" fill="#d97706" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">exp</text><line x1="244" y1="232" x2="296" y2="232" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-sm)"/><rect x="300" y="210" width="150" height="44" rx="6" fill="#ffffff" stroke="#6f42c1" stroke-width="1.8"/><text x="375" y="237" font-size="13" fill="#6f42c1" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">÷ Σ<sub>j</sub> e<sup>z<sub>j</sub></sup></text><line x1="452" y1="232" x2="500" y2="232" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-sm)"/><text x="510" y="238" font-size="15" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">p<sub>3</sub> = 0.099</text><text x="150" y="322" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">① 取指數：讓所有值變成正數，並放大差異</text><text x="300" y="344" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">② 正規化：除以總和，使 Σp = 1（可視為機率分布）</text><line x1="620" y1="270" x2="620" y2="100" stroke="#57606a" stroke-width="1.6"/><rect x="632" y="164.56" width="30" height="105.44" rx="6" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1"/><text x="647" y="290" font-size="11.5" fill="#57606a" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">0.659</text><rect x="676" y="231.28" width="30" height="38.72" rx="6" fill="#d97706" stroke="#d97706" stroke-width="1"/><text x="691" y="290" font-size="11.5" fill="#57606a" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">0.242</text><rect x="720" y="254.16" width="30" height="15.84" rx="6" fill="#c0392b" stroke="#c0392b" stroke-width="1"/><text x="735" y="290" font-size="11.5" fill="#57606a" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">0.099</text><text x="676" y="84" font-size="12.5" fill="#57606a" text-anchor="middle" font-weight="bold">輸出機率分布</text><text x="676" y="306" font-size="12" fill="#1a7f37" text-anchor="middle" font-weight="bold">Σ = 1.000</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 11：<b>Softmax 的計算流程</b>（原稿 p15、p16）。以 logits <code>z = [2.0, 1.0, 0.1]</code> 為例：先取指數 <code>e^z = [7.389, 2.718, 1.105]</code>，總和 11.213，再各自除以總和得到 <code>p = [0.659, 0.242, 0.099]</code>（和為 1）。最大值 0.659 對應的類別就是預測結果。</figcaption>
</figure>

### 11.2 Softmax 的圖形（p16）

原稿 p16 畫的是 y 對 a 的曲線——就是**指數函數**的形狀（Softmax 的分子 e^z 決定了它的行為）。

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 380" width="100%" style="max-width:760px;height:auto" role="img" aria-label="指數函數與線性函數的比較"><defs><marker id="ar-smg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><line x1="250" y1="300" x2="440" y2="300" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-smg)"/><line x1="250" y1="300" x2="250" y2="20" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-smg)"/><text x="448" y="316" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">a</text><text x="236" y="16" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif"></text><polyline points="82.00,348.00 84.10,347.40 86.20,346.80 88.30,346.20 90.40,345.60 92.50,345.00 94.60,344.40 96.70,343.80 98.80,343.20 100.90,342.60 103.00,342.00 105.10,341.40 107.20,340.80 109.30,340.20 111.40,339.60 113.50,339.00 115.60,338.40 117.70,337.80 119.80,337.20 121.90,336.60 124.00,336.00 126.10,335.40 128.20,334.80 130.30,334.20 132.40,333.60 134.50,333.00 136.60,332.40 138.70,331.80 140.80,331.20 142.90,330.60 145.00,330.00 147.10,329.40 149.20,328.80 151.30,328.20 153.40,327.60 155.50,327.00 157.60,326.40 159.70,325.80 161.80,325.20 163.90,324.60 166.00,324.00 168.10,323.40 170.20,322.80 172.30,322.20 174.40,321.60 176.50,321.00 178.60,320.40 180.70,319.80 182.80,319.20 184.90,318.60 187.00,318.00 189.10,317.40 191.20,316.80 193.30,316.20 195.40,315.60 197.50,315.00 199.60,314.40 201.70,313.80 203.80,313.20 205.90,312.60 208.00,312.00 210.10,311.40 212.20,310.80 214.30,310.20 216.40,309.60 218.50,309.00 220.60,308.40 222.70,307.80 224.80,307.20 226.90,306.60 229.00,306.00 231.10,305.40 233.20,304.80 235.30,304.20 237.40,303.60 239.50,303.00 241.60,302.40 243.70,301.80 245.80,301.20 247.90,300.60 250.00,300.00 252.10,299.40 254.20,298.80 256.30,298.20 258.40,297.60 260.50,297.00 262.60,296.40 264.70,295.80 266.80,295.20 268.90,294.60 271.00,294.00 273.10,293.40 275.20,292.80 277.30,292.20 279.40,291.60 281.50,291.00 283.60,290.40 285.70,289.80 287.80,289.20 289.90,288.60 292.00,288.00 294.10,287.40 296.20,286.80 298.30,286.20 300.40,285.60 302.50,285.00 304.60,284.40 306.70,283.80 308.80,283.20 310.90,282.60 313.00,282.00 315.10,281.40 317.20,280.80 319.30,280.20 321.40,279.60 323.50,279.00 325.60,278.40 327.70,277.80 329.80,277.20 331.90,276.60 334.00,276.00 336.10,275.40 338.20,274.80 340.30,274.20 342.40,273.60 344.50,273.00 346.60,272.40 348.70,271.80 350.80,271.20 352.90,270.60 355.00,270.00 357.10,269.40 359.20,268.80 361.30,268.20 363.40,267.60 365.50,267.00 367.60,266.40 369.70,265.80 371.80,265.20 373.90,264.60 376.00,264.00 378.10,263.40 380.20,262.80 382.30,262.20 384.40,261.60 386.50,261.00 388.60,260.40 390.70,259.80 392.80,259.20 394.90,258.60 397.00,258.00 399.10,257.40 401.20,256.80 403.30,256.20 405.40,255.60 407.50,255.00 409.60,254.40 411.70,253.80 413.80,253.20 415.90,252.60 418.00,252.00" fill="none" stroke="#2c6fb1" stroke-width="2.4" stroke-linecap="round"/><polyline points="82.00,298.19 84.10,298.13 86.20,298.07 88.30,298.01 90.40,297.95 92.50,297.89 94.60,297.83 96.70,297.76 98.80,297.69 100.90,297.62 103.00,297.55 105.10,297.48 107.20,297.40 109.30,297.32 111.40,297.24 113.50,297.15 115.60,297.07 117.70,296.98 119.80,296.89 121.90,296.79 124.00,296.69 126.10,296.59 128.20,296.49 130.30,296.38 132.40,296.27 134.50,296.16 136.60,296.04 138.70,295.92 140.80,295.80 142.90,295.67 145.00,295.54 147.10,295.40 149.20,295.26 151.30,295.12 153.40,294.97 155.50,294.82 157.60,294.66 159.70,294.49 161.80,294.33 163.90,294.15 166.00,293.98 168.10,293.79 170.20,293.60 172.30,293.41 174.40,293.21 176.50,293.00 178.60,292.79 180.70,292.57 182.80,292.34 184.90,292.11 187.00,291.87 189.10,291.62 191.20,291.37 193.30,291.10 195.40,290.83 197.50,290.55 199.60,290.26 201.70,289.97 203.80,289.66 205.90,289.35 208.00,289.02 210.10,288.69 212.20,288.35 214.30,287.99 216.40,287.62 218.50,287.25 220.60,286.86 222.70,286.46 224.80,286.05 226.90,285.62 229.00,285.18 231.10,284.73 233.20,284.27 235.30,283.79 237.40,283.29 239.50,282.79 241.60,282.26 243.70,281.72 245.80,281.16 247.90,280.59 250.00,280.00 252.10,279.39 254.20,278.76 256.30,278.12 258.40,277.45 260.50,276.76 262.60,276.06 264.70,275.33 266.80,274.58 268.90,273.80 271.00,273.00 273.10,272.18 275.20,271.33 277.30,270.46 279.40,269.56 281.50,268.63 283.60,267.68 285.70,266.69 287.80,265.68 289.90,264.63 292.00,263.56 294.10,262.45 296.20,261.30 298.30,260.13 300.40,258.91 302.50,257.66 304.60,256.37 306.70,255.04 308.80,253.67 310.90,252.26 313.00,250.81 315.10,249.31 317.20,247.77 319.30,246.18 321.40,244.54 323.50,242.85 325.60,241.11 327.70,239.31 329.80,237.46 331.90,235.56 334.00,233.60 336.10,231.58 338.20,229.49 340.30,227.34 342.40,225.13 344.50,222.85 346.60,220.50 348.70,218.08 350.80,215.59 352.90,213.02 355.00,210.37 357.10,207.64 359.20,204.82 361.30,201.93 363.40,198.94 365.50,195.86 367.60,192.69 369.70,189.42 371.80,186.05 373.90,182.58 376.00,179.01 378.10,175.32 380.20,171.53 382.30,167.61 384.40,163.58 386.50,159.43 388.60,155.15 390.70,150.73 392.80,146.19 394.90,141.50 397.00,136.68 399.10,131.70 401.20,126.58 403.30,121.30 405.40,115.85 407.50,110.25 409.60,104.47 411.70,98.51 413.80,92.38 415.90,86.05 418.00,79.54" fill="none" stroke="#c0392b" stroke-width="3.2" stroke-linecap="round"/><text x="92.0" y="340.0" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="normal">線性 f(a) = a</text><text x="313.0" y="236.807937776861" font-size="13" fill="#c0392b" text-anchor="start" font-weight="normal">指數 eᵃ</text><text x="250.0" y="320" font-size="13" fill="#57606a" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">0</text><text x="560" y="90" font-size="14" fill="#c0392b" text-anchor="start" font-weight="bold">為什麼 Softmax 用 eᵃ？</text><text x="560" y="118" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">1. 恆為正 → 才能當機率</text><text x="560" y="140" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">2. 差距被放大 → 大的更大、小的更小，</text><text x="560" y="160" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">　 模型會更「有自信」</text><text x="560" y="182" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">3. 處處可微 → 可反向傳播訓練</text><text x="560" y="216" font-size="12.5" fill="#0f766e" text-anchor="start" font-weight="normal">注意：Softmax 對所有 logits 平移不變</text><text x="560" y="236" font-size="12.5" fill="#0f766e" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">softmax(z) = softmax(z − c)</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 12：<b>指數 vs 線性</b>（原稿 p16）。Softmax 的分子用指數函數：一來保證所有輸出為正，二來把分數差距指數放大，讓最大者明顯勝出；而且指數處處可微，才能用反向傳播訓練。</figcaption>
</figure>

### 11.3 Softmax 為什麼長這樣

| 設計 | 原因 |
|---|---|
| 分子取 **指數 e^z** | ① 保證所有輸出為**正**；② 把差距**指數放大**，讓大的更大、模型更「有自信」 |
| 除以**總和** | 讓所有輸出**加總為 1**，成為合法的**機率分布** |
| 取 `argmax` | 機率最大的那一類就是預測結果（注意：訓練時用機率，預測時通常只取最大） |
| 平移不變性 | `softmax(z) = softmax(z − c)`；實作時常先減去最大值以避免指數溢位 |

**計算範例**（以 z = [2.0, 1.0, 0.1] 為例）：

| 步驟 | 數值 |
|---|---|
| logits `z` | 2.0 / 1.0 / 0.1 |
| `e^z` | 7.389 / 2.718 / 1.105（總和 11.213） |
| 除以總和 | **0.659 / 0.242 / 0.099**（總和 1.000） |
| 預測 | 第 1 類（機率最高 0.659） |

### 11.4 Sigmoid vs Softmax（別搞混）

| 比較 | Sigmoid | Softmax |
|---|---|---|
| 適用 | **二元**分類 | **多類別**分類 |
| 輸出個數 | 1 個（其餘類別機率 = 1 − p） | K 個（每個類別一個） |
| 輸出總和 | 不固定 | **一定等於 1** |
| 公式 | `1/(1+e⁻ᵃ)` | `e^zᵢ / Σⱼe^zⱼ` |
| 關係 | Softmax 在 K = 2 時，會退化為 Sigmoid 的形式 | — |

> **考點**：
> 1. Softmax 的輸出**加總為 1**，這是它與 Sigmoid 最大的差別。
> 2. 多類別**互斥**（只能選一個）→ Softmax；多標籤（可同時成立）→ 每個標籤各一個 Sigmoid。
> 3. 實作上為避免 `exp` 溢位，會先減去 logits 的最大值（不影響結果）。

---

## 12. 問題類型與激勵函數的對應（PDF p17）

<!-- p: 17 -->

原稿 p17 是一張**樹狀圖**，把「問題」一路拆到「該用哪個激勵函數」。
這頁只有名詞、沒有句子，但它是整個上半場的**總結**：

```
Problem
 ├─ Classification
 │    ├─ Binary Classification      → TLU
 │    ├─ Multiclass Classification  → Softmax
 │    └─ Multilabel Classification  → Sigmoid
 └─ Regression                     → ReLU
```

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 430" width="100%" style="max-width:760px;height:auto" role="img" aria-label="問題類型與激勵函數的對應"><defs><marker id="ar-pm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><rect x="300" y="14" width="160" height="46" rx="6" fill="#dbeafe" stroke="#2c6fb1" stroke-width="2"/><text x="380" y="42" font-size="14" fill="#2c6fb1" text-anchor="middle" font-weight="bold">問題 Problem</text><line x1="380" y1="60" x2="200" y2="108" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-pm)"/><line x1="380" y1="60" x2="560" y2="108" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-pm)"/><rect x="120" y="108" width="160" height="46" rx="6" fill="#dbeafe" stroke="#2c6fb1" stroke-width="2"/><text x="200" y="130" font-size="13.5" fill="#2c6fb1" text-anchor="middle" font-weight="bold">Classification</text><text x="200" y="147" font-size="11.5" fill="#2c6fb1" text-anchor="middle" font-weight="normal">分類（輸出類別）</text><rect x="480" y="108" width="160" height="46" rx="6" fill="#e8f6ec" stroke="#1a7f37" stroke-width="2"/><text x="560" y="130" font-size="13.5" fill="#1a7f37" text-anchor="middle" font-weight="bold">Regression</text><text x="560" y="147" font-size="11.5" fill="#1a7f37" text-anchor="middle" font-weight="normal">迴歸（輸出數值）</text><line x1="200" y1="154" x2="94" y2="202" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-pm)"/><rect x="40" y="202" width="108" height="44" rx="6" fill="#ffffff" stroke="#2c6fb1" stroke-width="1.6"/><text x="94" y="229" font-size="11.5" fill="#2c6fb1" text-anchor="middle" font-weight="normal">Binary 二元</text><line x1="200" y1="154" x2="214" y2="202" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-pm)"/><rect x="160" y="202" width="108" height="44" rx="6" fill="#ffffff" stroke="#2c6fb1" stroke-width="1.6"/><text x="214" y="229" font-size="11.5" fill="#2c6fb1" text-anchor="middle" font-weight="normal">Multiclass 多類</text><line x1="200" y1="154" x2="334" y2="202" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-pm)"/><rect x="280" y="202" width="108" height="44" rx="6" fill="#ffffff" stroke="#2c6fb1" stroke-width="1.6"/><text x="334" y="229" font-size="11.5" fill="#2c6fb1" text-anchor="middle" font-weight="normal">Multilabel 多標籤</text><line x1="560" y1="154" x2="560" y2="202" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-pm)"/><rect x="496" y="202" width="128" height="44" rx="6" fill="#ffffff" stroke="#1a7f37" stroke-width="1.6"/><text x="560" y="229" font-size="11.5" fill="#1a7f37" text-anchor="middle" font-weight="normal">預測連續數值</text><line x1="94" y1="246" x2="94" y2="292" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-pm)"/><rect x="36" y="292" width="116" height="44" rx="6" fill="#ffffff" stroke="#6f42c1" stroke-width="1.8"/><text x="94" y="319" font-size="12.5" fill="#6f42c1" text-anchor="middle" font-weight="bold" font-family="Cambria Math,Georgia,'Times New Roman',serif">Sigmoid</text><line x1="214" y1="246" x2="214" y2="292" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-pm)"/><rect x="156" y="292" width="116" height="44" rx="6" fill="#ffffff" stroke="#d97706" stroke-width="1.8"/><text x="214" y="319" font-size="12.5" fill="#d97706" text-anchor="middle" font-weight="bold" font-family="Cambria Math,Georgia,'Times New Roman',serif">Softmax</text><line x1="334" y1="246" x2="334" y2="292" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-pm)"/><rect x="276" y="292" width="116" height="44" rx="6" fill="#ffffff" stroke="#6f42c1" stroke-width="1.8"/><text x="334" y="319" font-size="12.5" fill="#6f42c1" text-anchor="middle" font-weight="bold" font-family="Cambria Math,Georgia,'Times New Roman',serif">Sigmoid × N</text><line x1="560" y1="246" x2="560" y2="292" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-pm)"/><rect x="502" y="292" width="116" height="44" rx="6" fill="#ffffff" stroke="#c0392b" stroke-width="1.8"/><text x="560" y="319" font-size="12.5" fill="#c0392b" text-anchor="middle" font-weight="bold" font-family="Cambria Math,Georgia,'Times New Roman',serif">ReLU / Linear</text><text x="30" y="366" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">選法：二元 → 1 個輸出 + Sigmoid；多類別互斥 → Softmax（各類機率加總為 1）；多標籤可同時成立 → 每個標籤各自一個 Sigmoid；</text><text x="30" y="388" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">迴歸 → 輸出連續值，用 ReLU 或線性（不要用 Sigmoid，會把大數值壓扁）。迴歸模型看 MAE / MSE / R²，分類模型看 Accuracy / Precision / Recall / F1。</text><text x="30" y="414" font-size="12.5" fill="#0f766e" text-anchor="start" font-weight="bold">※ 激勵函數的選擇是「輸出層」的事；隱藏層預設用 ReLU。</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 14：<b>問題類型 → 激勵函數的對應</b>（原稿 p17）。原稿把「問題 → 分類／迴歸 → 二元／多類別／多標籤」與 TLU／Sigmoid／Softmax／ReLU 對起來；判斷順序是：先看輸出是類別還是數值，再看類別是否互斥。</figcaption>
</figure>

### 12.1 三種分類的差別（一定要分清楚）

| 類型 | 中文 | 例子 | 輸出層設計 |
|---|---|---|---|
| **Binary Classification** | 二元分類 | 這封 email 是不是垃圾信？ | **1 個**輸出神經元 + **Sigmoid** |
| **Multiclass Classification** | 多類別分類 | 這張圖是貓、狗還是鳥？（**只能選一個**） | **K 個**輸出 + **Softmax** |
| **Multilabel Classification** | 多標籤分類 | 這張照片有「人」也有「車」（**可同時成立**） | **每個標籤各一個** Sigmoid |

### 12.2 迴歸（Regression）

- 輸出的是**連續數值**（房價、溫度、銷售量），不是類別。
- 輸出層通常用 **ReLU** 或**線性**（等同不用激勵函數），
  **不要用 Sigmoid**——它會把大數值壓縮到 (0,1)，讓模型無法輸出正確的量級。
- 評估指標是 **MAE / MSE / R²**，不是 Accuracy。

> **考點（高頻）**：
> 1. 二元分類 → **Sigmoid**；多類別互斥 → **Softmax**；多標籤 → **Sigmoid（每標籤一個）**。
> 2. 迴歸 → **ReLU／線性**，且用 MAE／MSE 評估。
> 3. 判斷順序：**先看輸出是「類別」還是「數值」→ 再看類別是否互斥**。

---

## 13. Machine Learning：Analytics and Machine Learning（PDF p18）

<!-- p: 18 -->

原稿 p18 是「機器學習」這半場的**目錄頁**，列出三個主題：

| # | 原稿條列 | 中文 | 對應頁 |
|---|---|---|---|
| 1 | Basic Concepts of Machine Learning | 機器學習的基本概念 | p19–p22 |
| 2 | Principles and Examples of Supervised Learning | 監督式學習的原理與實例 | p23、p25–p26 |
| 3 | Principles and Examples of Unsupervised Learning | 非監督式學習的原理與實例 | p28–p30 |

### 13.1 為什麼分析（Analytics）與機器學習要放在一起講

| 概念 | 差別 |
|---|---|
| **Analytics（分析）** | 用資料回答「**發生什麼事、為什麼**」：統計、報表、視覺化、儀表板 |
| **Machine Learning（機器學習）** | 用資料回答「**接下來會怎樣**」：建立**可預測**的模型 |

兩者是同一條線的兩端：分析幫你**理解資料**（探索、找特徵、找異常），
機器學習幫你**把理解變成可自動化的預測**。
所以實務上一定是先分析、再建模——這也呼應第 15 節的十個步驟。

> **考點**：原稿把機器學習分成**三大主題**（基本概念／監督式／非監督式）；
> 本節後面所有頁面都掛在這三個主題底下，考試問「某頁屬於哪個主題」時可以據此判斷。

---

## 14. Machine Learning：基本概念 Basic Concepts（PDF p19）

<!-- p: 19 -->

原稿 p19 只有標題與一張圖（無文字），圖在說明機器學習的**基本概念**：
**從資料中找出「輸入」與「輸出」之間的關係，建立可預測的模型。**

### 14.1 機器學習 vs 傳統程式設計

|  | 傳統程式設計 | 機器學習 |
|---|---|---|
| 輸入 | 資料 + **規則（人寫的）** | 資料 + **答案（標籤）** |
| 產出 | 答案 | **規則／模型（自己學的）** |
| 例子 | 寫 if-else 判斷垃圾信 | 給一萬封已標記的信，讓模型自己找出規則 |

傳統程式設計是「**規則 → 答案**」；機器學習是「**資料＋答案 → 規則**」。
這也是為什麼機器學習需要**大量且正確的資料**。

### 14.2 三個一定會出現的名詞

| 名詞 | 英文 | 說明 |
|---|---|---|
| 特徵 | **feature** | 用來預測的輸入變數（x），例如花瓣長度 |
| 標籤／目標 | **label / target** | 要預測的答案（y），例如品種、房價 |
| 模型 | **model** | 學到的「輸入 → 輸出」關係，例如 `f(x) = 35 + 1.5x` |

### 14.3 機器學習的兩種典型任務（本節後面會展開）

- **分類（Classification）**：輸出是**類別**（垃圾／非垃圾、貓／狗／鳥）。
- **迴歸（Regression）**：輸出是**數值**（價格、溫度、銷量）。

> **考點**：機器學習的核心是「**從資料中找關係**」而不是「人把規則寫死」；
> feature 是輸入、label 是答案，這兩個名詞會在後面每一頁反覆出現。

---

## 15. 機器學習解決方案的十個步驟 Ten Steps（PDF p20）

<!-- p: 20 -->

原稿 p20 的標題是「**Ten Steps to a Machine Learning Solution**」，列出十個步驟（原文照錄，
中文為筆者翻譯）：

| # | 原文 | 中文 |
|---|---|---|
| 1 | Define problem statement—gather available data | 定義問題陳述——蒐集可用資料 |
| 2 | Identify target variables and measure of predictive accuracy | 找出**目標變數**與**預測準確度的衡量方式** |
| 3 | Measure data or select from readily available datasets—when external data such as census data can provide context | 量測資料，或從現成資料集中選用——必要時加入外部資料（例如人口普查資料提供背景） |
| 4 | Clean and join datasets | 清理並**合併**資料集 |
| 5 | Select the algorithm that will best help analyze the defined problem statement | 選擇最能分析此問題的**演算法** |
| 6 | Train and validate the model | **訓練並驗證**模型 |
| 7 | Test the model | **測試**模型 |
| 8 | Deploy the model for use | **部署**模型上線使用 |
| 9 | Determine execution frequency | 決定**執行頻率** |
| 10 | Identify frequency of model update—set the interval at which the model should be updated or executed again | 決定**模型更新頻率**——設定多久要重新訓練或再執行一次 |

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 430" width="100%" style="max-width:760px;height:auto" role="img" aria-label="機器學習解決方案的十個步驟"><defs><marker id="ar-ms" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><text x="20" y="26" font-size="13.5" fill="#c0392b" text-anchor="start" font-weight="bold">Ten Steps to a Machine Learning Solution（原稿列出的十步）</text><text x="20" y="46" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">左欄：把問題變成資料　│　右欄：把資料變成可用的模型</text><rect x="20" y="62" width="348" height="62" rx="6" fill="#ffffff" stroke="#2c6fb1" stroke-width="1.6"/><circle cx="46" cy="93" r="15" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><text x="46" y="98" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="bold">1</text><text x="70" y="86" font-size="11.5" fill="#24292f" text-anchor="start" font-weight="bold">Define problem statement—gather available data</text><text x="70" y="104" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">定義問題陳述，並蒐集可用資料</text><rect x="20" y="134" width="348" height="62" rx="6" fill="#ffffff" stroke="#2c6fb1" stroke-width="1.6"/><circle cx="46" cy="165" r="15" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><text x="46" y="170" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="bold">2</text><text x="70" y="158" font-size="11.5" fill="#24292f" text-anchor="start" font-weight="bold">Identify target variables and measure of predictive accuracy</text><text x="70" y="176" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">決定目標變數與「預測準確度」的衡量方式</text><rect x="20" y="206" width="348" height="62" rx="6" fill="#ffffff" stroke="#2c6fb1" stroke-width="1.6"/><circle cx="46" cy="237" r="15" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><text x="46" y="242" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="bold">3</text><text x="70" y="230" font-size="11.5" fill="#24292f" text-anchor="start" font-weight="bold">Measure data or select from readily available datasets</text><text x="70" y="248" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">量測資料，或選用現成資料集（必要時加入外部資料，如人口普查資料提供背景）</text><rect x="20" y="278" width="348" height="62" rx="6" fill="#ffffff" stroke="#2c6fb1" stroke-width="1.6"/><circle cx="46" cy="309" r="15" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><text x="46" y="314" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="bold">4</text><text x="70" y="302" font-size="11.5" fill="#24292f" text-anchor="start" font-weight="bold">Clean and join datasets</text><text x="70" y="320" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">清理並合併資料集</text><rect x="20" y="350" width="348" height="62" rx="6" fill="#ffffff" stroke="#2c6fb1" stroke-width="1.6"/><circle cx="46" cy="381" r="15" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><text x="46" y="386" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="bold">5</text><text x="70" y="374" font-size="11.5" fill="#24292f" text-anchor="start" font-weight="bold">Select the algorithm that will best help analyze the problem</text><text x="70" y="392" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">選擇最適合分析此問題的演算法</text><rect x="392" y="62" width="348" height="62" rx="6" fill="#ffffff" stroke="#1a7f37" stroke-width="1.6"/><circle cx="418" cy="93" r="15" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><text x="418" y="98" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="bold">6</text><text x="442" y="86" font-size="11.5" fill="#24292f" text-anchor="start" font-weight="bold">Train and validate the model</text><text x="442" y="104" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">訓練並驗證模型</text><rect x="392" y="134" width="348" height="62" rx="6" fill="#ffffff" stroke="#1a7f37" stroke-width="1.6"/><circle cx="418" cy="165" r="15" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><text x="418" y="170" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="bold">7</text><text x="442" y="158" font-size="11.5" fill="#24292f" text-anchor="start" font-weight="bold">Test the model</text><text x="442" y="176" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">測試模型</text><rect x="392" y="206" width="348" height="62" rx="6" fill="#ffffff" stroke="#1a7f37" stroke-width="1.6"/><circle cx="418" cy="237" r="15" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><text x="418" y="242" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="bold">8</text><text x="442" y="230" font-size="11.5" fill="#24292f" text-anchor="start" font-weight="bold">Deploy the model for use</text><text x="442" y="248" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">部署模型上線使用</text><rect x="392" y="278" width="348" height="62" rx="6" fill="#ffffff" stroke="#1a7f37" stroke-width="1.6"/><circle cx="418" cy="309" r="15" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><text x="418" y="314" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="bold">9</text><text x="442" y="302" font-size="11.5" fill="#24292f" text-anchor="start" font-weight="bold">Determine execution frequency</text><text x="442" y="320" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">決定執行頻率</text><rect x="392" y="350" width="348" height="62" rx="6" fill="#ffffff" stroke="#1a7f37" stroke-width="1.6"/><circle cx="418" cy="381" r="15" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><text x="418" y="386" font-size="14" fill="#ffffff" text-anchor="middle" font-weight="bold">10</text><text x="442" y="374" font-size="11.5" fill="#24292f" text-anchor="start" font-weight="bold">Identify frequency of model update</text><text x="442" y="392" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">決定模型更新頻率——設定多久要重新訓練或再執行一次</text><text x="194" y="424" font-size="12" fill="#2c6fb1" text-anchor="middle" font-weight="bold">①–⑤ 準備階段：問題 → 指標 → 資料 → 清理 → 選演算法</text><text x="566" y="424" font-size="12" fill="#1a7f37" text-anchor="middle" font-weight="bold">⑥–⑩ 執行階段：訓練 → 測試 → 部署 → 監控 → 更新</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 15：<b>機器學習解決方案的十個步驟</b>（原稿 p20）。原稿強調這是一條「流程」而不是單一步驟：問題定義與指標（步驟 1–2）若做錯，後面再好的模型也救不回來；而部署之後的<b>執行頻率與更新頻率</b>（步驟 9–10）常被忽略，卻是模型能否長期維持準確的關鍵。</figcaption>
</figure>

### 15.1 十步可以分成四個階段

| 階段 | 步驟 | 重點 |
|---|---|---|
| **定義** | 1–2 | 問題與指標；**指標決定後面所有取捨** |
| **資料** | 3–4 | 取得、清理、合併（實務上最花時間的一步） |
| **建模** | 5–7 | 選演算法 → 訓練／驗證 → 測試 |
| **上線** | 8–10 | 部署 → 決定執行頻率 → 決定更新頻率 |

### 15.2 三個最容易被忽略的重點

1. **步驟 2 先定指標**：沒有先定義「怎樣叫準」，後面無法比較模型好壞。
2. **步驟 6 的 train/validate 與步驟 7 的 test 是兩件事**：
   驗證集用來調參數，測試集**只能用一次**，用來報告最終表現。
3. **步驟 9、10 是「維運」**：模型上線後會**漂移（drift）**，所以必須決定多久跑一次、
   多久重訓一次——這是很多專案失敗的地方。

> **考點（必背順序）**：
> 定義問題 → 定目標變數與指標 → 取資料 → 清理合併 → 選演算法 → 訓練驗證 → 測試 → 部署 → 執行頻率 → 更新頻率。
> 特別注意**「驗證」和「測試」是分開的兩個步驟**，且最後兩步與「頻率」有關。

---

## 16. Machine Learning：The Data/AI Landscape（PDF p21）

<!-- p: 21 -->

原稿 p21 只有標題與一張圖（無文字），圖在說明**資料與 AI 的範疇關係**。

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 470" width="100%" style="max-width:760px;height:auto" role="img" aria-label="資料與 AI 的範疇關係"><defs><marker id="ar-ai" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><circle cx="300" cy="235" r="200" fill="#dbeafe" stroke="#2c6fb1" stroke-width="2" opacity="0.55"/><circle cx="300" cy="235" r="150" fill="#fef3c7" stroke="#d97706" stroke-width="2" opacity="0.65"/><circle cx="300" cy="235" r="100" fill="#e8f6ec" stroke="#1a7f37" stroke-width="2" opacity="0.7"/><text x="300" y="59" font-size="13.5" fill="#2c6fb1" text-anchor="middle" font-weight="bold">Artificial Intelligence 人工智慧</text><text x="300" y="109" font-size="13.5" fill="#d97706" text-anchor="middle" font-weight="bold">Machine Learning 機器學習</text><text x="300" y="159" font-size="13.5" fill="#1a7f37" text-anchor="middle" font-weight="bold">Deep Learning 深度學習</text><text x="300" y="201" font-size="12" fill="#1a7f37" text-anchor="middle" font-weight="normal">CNN / RNN / Transformer</text><text x="300" y="221" font-size="12" fill="#1a7f37" text-anchor="middle" font-weight="normal">需要大量資料 + GPU</text><text x="300" y="353" font-size="12" fill="#d97706" text-anchor="middle" font-weight="normal">SVM、決策樹、隨機森林、k-means</text><text x="300" y="373" font-size="11.5" fill="#d97706" text-anchor="middle" font-weight="normal">（特徵多由人工設計）</text><text x="300" y="407" font-size="12" fill="#2c6fb1" text-anchor="middle" font-weight="normal">專家系統、規則式推理</text><rect x="520" y="60" width="224" height="350" rx="8" fill="#ffffff" stroke="#d8dee4" stroke-width="1.6"/><text x="536" y="86" font-size="13" fill="#c0392b" text-anchor="start" font-weight="bold">旁邊的三個常混淆名詞</text><text x="536" y="116" font-size="12.5" fill="#2c6fb1" text-anchor="start" font-weight="bold">Data Science 資料科學</text><text x="536" y="136" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">跨領域方法：統計 + 程式 +</text><text x="536" y="154" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">領域知識，重點在「從資料得到洞見」</text><text x="536" y="186" font-size="12.5" fill="#d97706" text-anchor="start" font-weight="bold">Data Mining 資料探勘</text><text x="536" y="206" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">從大量資料中找出未知的模式，</text><text x="536" y="224" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">例如分群（k-means）就是常見手法</text><text x="536" y="256" font-size="12.5" fill="#1a7f37" text-anchor="start" font-weight="bold">Big Data 大數據</text><text x="536" y="276" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">資料量大／速度快到傳統工具</text><text x="536" y="294" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">處理不了，需要分散式運算</text><text x="536" y="330" font-size="12" fill="#0f766e" text-anchor="start" font-weight="bold">關係：大數據是原料 →</text><text x="536" y="350" font-size="12" fill="#0f766e" text-anchor="start" font-weight="bold">資料科學是方法 →</text><text x="536" y="370" font-size="12" fill="#0f766e" text-anchor="start" font-weight="bold">機器學習／AI 是產出</text><text x="536" y="398" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">深度學習只是機器學習的一個子集</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 16：<b>The Data/AI Landscape</b>（原稿 p21）。由外而內是「人工智慧 ⊃ 機器學習 ⊃ 深度學習」；右側把常被混用的資料科學、資料探勘、大數據分開說明。考試常問「深度學習屬於誰的子集」→ 答案是機器學習（而機器學習屬於 AI）。</figcaption>
</figure>

### 16.1 三個同心圓（由大到小）

| 層級 | 內容 | 說明 |
|---|---|---|
| **AI 人工智慧** | 最外圈 | 任何讓機器表現出「像人一樣智慧」的技術，包含**專家系統、規則式推理** |
| **ML 機器學習** | 中間圈 | AI 的一個子集：**不靠人寫規則，而是從資料學**（SVM、決策樹、隨機森林、k-means） |
| **DL 深度學習** | 最內圈 | ML 的一個子集：用**多層神經網路**（CNN、RNN、Transformer）自動學特徵 |

關係可以寫成：**AI ⊃ Machine Learning ⊃ Deep Learning**。

### 16.2 旁邊三個常被混淆的名詞

| 名詞 | 定義 | 與 ML 的關係 |
|---|---|---|
| **Data Science 資料科學** | 跨領域方法：統計 + 程式 + 領域知識，目標是**從資料得到洞見** | 範圍比 ML 廣；ML 是資料科學常用的工具之一 |
| **Data Mining 資料探勘** | 從大量資料中**找出未知的模式** | 常被視為 ML／統計方法的應用；分群（k-means）就是典型手法 |
| **Big Data 大數據** | 資料量大／速度快到傳統工具處理不了，需要分散式運算 | 是**原料**，不是方法 |

一句話記法：**大數據是原料 → 資料科學是方法 → 機器學習／AI 是產出**。

> **考點（超常考）**：
> 1. 「深度學習」是哪一層的子集？→ **機器學習**（而機器學習又屬於 AI）。
> 2. 「AI 一定等於機器學習」是**錯**的：早期的專家系統屬於 AI 但不屬於 ML。
> 3. 分群（k-means）通常被歸在**非監督式學習**，也是**資料探勘**的常見手法。

---

## 17. Machine Learning：Types 機器學習的類型（PDF p22、p24、p27）

<!-- p: 22、p24、p27 -->

原稿有三頁（p22、p24、p27）標題完全相同，都是「**Machine Learning — Types**」的同一張圖：
差別在於 **p24、p27 的版本多了「Classification」與「Regression」兩個子項**。

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 480" width="100%" style="max-width:760px;height:auto" role="img" aria-label="機器學習的類型與三個分類軸"><defs><marker id="ar-mt" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><rect x="300" y="12" width="160" height="44" rx="6" fill="#dbeafe" stroke="#2c6fb1" stroke-width="2"/><text x="380" y="40" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="bold">Machine Learning</text><line x1="380" y1="56" x2="380" y2="84" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-mt)"/><rect x="285" y="84" width="190" height="42" rx="6" fill="#ffffff" stroke="#6f42c1" stroke-width="1.8"/><text x="380" y="110" font-size="13" fill="#6f42c1" text-anchor="middle" font-weight="bold">Human Supervision?</text><line x1="380" y1="126" x2="120" y2="164" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-mt)"/><rect x="35" y="164" width="170" height="46" rx="6" fill="#dbeafe" stroke="#2c6fb1" stroke-width="1.8"/><text x="120" y="192" font-size="12.5" fill="#2c6fb1" text-anchor="middle" font-weight="bold">Supervised 監督式</text><line x1="380" y1="126" x2="380" y2="164" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-mt)"/><rect x="295" y="164" width="170" height="46" rx="6" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/><text x="380" y="192" font-size="12.5" fill="#d97706" text-anchor="middle" font-weight="bold">Unsupervised 非監督式</text><line x1="380" y1="126" x2="640" y2="164" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-mt)"/><rect x="555" y="164" width="170" height="46" rx="6" fill="#e8f6ec" stroke="#1a7f37" stroke-width="1.8"/><text x="640" y="192" font-size="12.5" fill="#1a7f37" text-anchor="middle" font-weight="bold">Reinforcement 強化式</text><line x1="120" y1="210" x2="70" y2="244" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-mt)"/><rect x="20.0" y="244" width="100" height="40" rx="6" fill="#ffffff" stroke="#57606a" stroke-width="1.4"/><text x="70" y="269" font-size="11.5" fill="#24292f" text-anchor="middle" font-weight="normal">Classification</text><line x1="120" y1="210" x2="170" y2="244" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-mt)"/><rect x="120.0" y="244" width="100" height="40" rx="6" fill="#ffffff" stroke="#57606a" stroke-width="1.4"/><text x="170" y="269" font-size="11.5" fill="#24292f" text-anchor="middle" font-weight="normal">Regression</text><line x1="380" y1="210" x2="380" y2="244" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-mt)"/><rect x="315.0" y="244" width="130" height="40" rx="6" fill="#ffffff" stroke="#57606a" stroke-width="1.4"/><text x="380" y="269" font-size="11.5" fill="#24292f" text-anchor="middle" font-weight="normal">Clustering</text><line x1="640" y1="210" x2="640" y2="244" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-mt)"/><rect x="570.0" y="244" width="140" height="40" rx="6" fill="#ffffff" stroke="#57606a" stroke-width="1.4"/><text x="640" y="269" font-size="11.5" fill="#24292f" text-anchor="middle" font-weight="normal">Reward / 試錯</text><line x1="170" y1="300" x2="520" y2="300" stroke="#d8dee4" stroke-width="1.2" stroke-dasharray="4 4"/><line x1="120" y1="284" x2="120" y2="300" stroke="#d8dee4" stroke-width="1.2" stroke-dasharray="4 4"/><line x1="380" y1="284" x2="380" y2="300" stroke="#d8dee4" stroke-width="1.2" stroke-dasharray="4 4"/><line x1="640" y1="284" x2="640" y2="300" stroke="#d8dee4" stroke-width="1.2" stroke-dasharray="4 4"/><line x1="170" y1="300" x2="170" y2="322" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-mt)"/><rect x="60.0" y="322" width="220" height="42" rx="6" fill="#ffffff" stroke="#6f42c1" stroke-width="1.8"/><text x="170" y="348" font-size="13" fill="#6f42c1" text-anchor="middle" font-weight="bold">Learn Incrementally?</text><line x1="520" y1="300" x2="520" y2="322" stroke="#57606a" stroke-width="1.4" marker-end="url(#ar-mt)"/><rect x="410.0" y="322" width="220" height="42" rx="6" fill="#ffffff" stroke="#6f42c1" stroke-width="1.8"/><text x="520" y="348" font-size="13" fill="#6f42c1" text-anchor="middle" font-weight="bold">How they generalize?</text><text x="30" y="392" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">① Human Supervision?（有無人類監督）→ 監督式：有標籤 {(x₁,y₁)…}；非監督式：只有特徵 {x₁…}；強化式：靠環境給的獎勵試錯。</text><text x="30" y="414" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">② Learn Incrementally?（是否增量學習）→ 批次學習：一次用全部資料訓練；增量／線上學習：資料分批進來、模型持續更新。</text><text x="30" y="436" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">③ How they generalize?（如何泛化）→ 基於實例（記住樣本、比相似度，如 k-NN） vs 基於模型（學出參數，如線性迴歸、神經網路）。</text><text x="30" y="464" font-size="12" fill="#0f766e" text-anchor="start" font-weight="bold">※ 原稿 p22 / p24 / p27 是同一張圖的三個版本：p24、p27 補上了 Supervised 底下的 Classification 與 Regression。</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 17：<b>Machine Learning – Types</b>（原稿 p22、p24、p27）。原稿用三個問題把機器學習分類：<b>Human Supervision?</b>（監督式／非監督式／強化式）、<b>Learn Incrementally?</b>、<b>How they generalize?</b>；並在監督式底下再分成 Classification（分類）與 Regression（迴歸）。</figcaption>
</figure>

### 17.1 第一條軸：Human Supervision?（有沒有人的監督）

| 類型 | 資料 | 學習方式 | 典型任務 |
|---|---|---|---|
| **Supervised** 監督式 | **有標籤** `{(x₁,y₁)…(xₙ,yₙ)}` | 學「輸入 → 標籤」的對應 | 分類、迴歸 |
| **Unsupervised** 非監督式 | **沒有標籤** `{x₁…xₙ}` | 自己從特徵找結構 | 分群、降維 |
| **Reinforcement** 強化式 | 沒有標準答案，有**獎勵** | 在環境中**試錯**，最大化累積獎勵 | 遊戲 AI、機器人控制 |

### 17.2 第二條軸：Learn Incrementally?（是否增量學習）

| 類型 | 說明 |
|---|---|
| **批次學習（batch）** | 一次用**全部**資料訓練一個模型；新資料來了要重新訓練 |
| **增量／線上學習（incremental / online）** | 資料**分批**進來，模型**持續更新**；適合資料流、即時系統 |

### 17.3 第三條軸：How they generalize?（如何泛化）

| 類型 | 說明 | 例子 |
|---|---|---|
| **基於實例（instance-based）** | 把訓練樣本**記住**，預測時找最相似的樣本 | k-NN（最近鄰） |
| **基於模型（model-based）** | 從資料中學出**參數／結構**，之後只留模型 | 線性迴歸、神經網路 |

> **考點**：
> 1. 三個分類軸的問句要背起來：**Human Supervision? / Learn Incrementally? / How they generalize?**
> 2. 「有標籤」= 監督式；「沒標籤」= 非監督式；「靠獎勵試錯」= 強化式。
> 3. p24 與 p27 比 p22 多的是 **Classification / Regression**（掛在 Supervised 底下）。

---

## 18. 監督式學習 Supervised Learning（PDF p23）

<!-- p: 23 -->

原稿 p23 的標題（同時也是定義）是：

> **Supervised Learning: labeled observations {(x₁, y₁), … (xₙ, yₙ)}**

條列內容：

| 原稿 | 中文 |
|---|---|
| Labels (teach) algorithm to learn **mapping from observations to labels** | 標籤**教**演算法學會「從觀察值到標籤」的**對應關係** |
| Examples: **Classification** (SVMs, Neural Nets, Decision Trees, Nearest Neighbors) | 例子：**分類**（支援向量機、神經網路、決策樹、最近鄰） |
| **Regression** (Linear Regression, Neural Nets) | **迴歸**（線性迴歸、神經網路） |

頁面下方的「**Learning Strategy**」指的是：監督式學習的策略就是**用已知答案的資料去學對應**。

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 360" width="100%" style="max-width:760px;height:auto" role="img" aria-label="監督式學習與非監督式學習的差別"><defs><marker id="ar-su" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><rect x="16" y="16" width="354" height="300" rx="8" fill="#ffffff" stroke="#2c6fb1" stroke-width="1.6"/><text x="193" y="44" font-size="13" fill="#2c6fb1" text-anchor="middle" font-weight="bold">Supervised 監督式：labeled observations</text><text x="193" y="64" font-size="12" fill="#57606a" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">{(x₁, y₁), …, (xₙ, yₙ)}　有答案可以對</text><line x1="52" y1="296" x2="330" y2="104" stroke="#c0392b" stroke-width="2" stroke-dasharray="6 5"/><circle cx="70" cy="150" r="8" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.4"/><circle cx="100" cy="118" r="8" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.4"/><circle cx="130" cy="168" r="8" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.4"/><circle cx="86" cy="190" r="8" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.4"/><circle cx="146" cy="138" r="8" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.4"/><rect x="223" y="255" width="14" height="14" rx="2" fill="#c0392b" stroke="#c0392b" stroke-width="1.4"/><rect x="265" y="285" width="14" height="14" rx="2" fill="#c0392b" stroke="#c0392b" stroke-width="1.4"/><rect x="293" y="233" width="14" height="14" rx="2" fill="#c0392b" stroke="#c0392b" stroke-width="1.4"/><rect x="243" y="219" width="14" height="14" rx="2" fill="#c0392b" stroke="#c0392b" stroke-width="1.4"/><rect x="299" y="279" width="14" height="14" rx="2" fill="#c0392b" stroke="#c0392b" stroke-width="1.4"/><text x="60" y="110" font-size="12" fill="#2c6fb1" text-anchor="start" font-weight="bold">類別 A</text><text x="272" y="318" font-size="12" fill="#c0392b" text-anchor="start" font-weight="bold">類別 B</text><text x="240" y="130" font-size="11.5" fill="#c0392b" text-anchor="start" font-weight="normal">學出決策邊界</text><text x="193" y="306" font-size="11.5" fill="#2c6fb1" text-anchor="middle" font-weight="normal">有標籤 → 學「輸入到標籤的對應」</text><rect x="390" y="16" width="354" height="300" rx="8" fill="#ffffff" stroke="#d97706" stroke-width="1.6"/><text x="567" y="44" font-size="13" fill="#d97706" text-anchor="middle" font-weight="bold">Unsupervised 非監督式：unlabeled observations</text><text x="567" y="64" font-size="12" fill="#57606a" text-anchor="middle" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">{x₁, …, xₙ}　只有特徵，沒有答案</text><circle cx="440" cy="130" r="8" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.4"/><circle cx="468" cy="112" r="8" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.4"/><circle cx="496" cy="148" r="8" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.4"/><circle cx="452" cy="156" r="8" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.4"/><circle cx="440" cy="130" r="13" fill="#ffffff" stroke="#1a7f37" stroke-width="2"/><text x="435" y="135" font-size="13" fill="#1a7f37" text-anchor="middle" font-weight="bold">×</text><circle cx="592" cy="258" r="8" fill="#d97706" stroke="#d97706" stroke-width="1.4"/><circle cx="624" cy="284" r="8" fill="#d97706" stroke="#d97706" stroke-width="1.4"/><circle cx="654" cy="244" r="8" fill="#d97706" stroke="#d97706" stroke-width="1.4"/><circle cx="600" cy="232" r="8" fill="#d97706" stroke="#d97706" stroke-width="1.4"/><circle cx="592" cy="258" r="13" fill="#ffffff" stroke="#d97706" stroke-width="2"/><text x="587" y="263" font-size="13" fill="#d97706" text-anchor="middle" font-weight="bold">×</text><circle cx="686" cy="132" r="8" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.4"/><circle cx="712" cy="154" r="8" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.4"/><circle cx="668" cy="168" r="8" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.4"/><circle cx="686" cy="132" r="13" fill="#ffffff" stroke="#6f42c1" stroke-width="2"/><text x="681" y="137" font-size="13" fill="#6f42c1" text-anchor="middle" font-weight="bold">×</text><text x="430" y="200" font-size="11.5" fill="#1a7f37" text-anchor="start" font-weight="normal">自己找出群組（分群）</text><text x="610" y="210" font-size="11.5" fill="#d97706" text-anchor="start" font-weight="normal">也可能只是前處理</text><text x="567" y="306" font-size="11.5" fill="#d97706" text-anchor="middle" font-weight="normal">沒有標籤 → 只能從特徵本身找結構</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 18：<b>監督式 vs 非監督式</b>（原稿 p23、p28）。監督式有標籤，演算法學的是「從輸入到標籤的對應」，因此可以做分類與迴歸；非監督式只有特徵，演算法必須自己找出結構（例如分群），它可以是目的本身（探索隱藏模式），也可以是監督式任務的前處理。</figcaption>
</figure>

### 18.1 監督式的資料長什麼樣子

| 符號 | 意義 |
|---|---|
| `xᵢ` | 第 i 筆的**特徵**（觀察值 observation） |
| `yᵢ` | 第 i 筆的**標籤**（答案 label） |
| `{(x₁,y₁)…(xₙ,yₙ)}` | n 筆「有答案」的訓練資料 |

### 18.2 監督式的兩大任務與常見演算法

| 任務 | 輸出 | 常見演算法（原稿點名） |
|---|---|---|
| **Classification** 分類 | 類別 | **SVM**、**Neural Nets**、**Decision Trees**、**Nearest Neighbors** |
| **Regression** 迴歸 | 連續數值 | **Linear Regression**、**Neural Nets** |

> **考點**：
> 1. 監督式學習的資料形式是 **`{(x₁,y₁)…(xₙ,yₙ)}`**（成對、有標籤）。
> 2. 原稿點名的分類演算法：**SVM、Neural Nets、Decision Trees、Nearest Neighbors**；
>    迴歸演算法：**Linear Regression、Neural Nets**（**神經網路兩邊都有**，是可分類也可迴歸的萬用工具）。
> 3. 「Learning Strategy」= 用標籤教演算法學會 **mapping from observations to labels**。

---

## 19. 監督式學習實例：分類與迴歸（PDF p25–p26）

<!-- p: 25–26 -->

原稿 p25、p26 是**兩張全圖的頁面**（PDF 抽不出任何文字），分別示範監督式學習的兩個實例：
p25 是**分類**（混淆矩陣＋門檻），p26 是**迴歸**（一條擬合直線與預測值）。

### 19.1 分類實例：混淆矩陣（p25）

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 520" width="100%" style="max-width:760px;height:auto" role="img" aria-label="混淆矩陣與門檻示意"><defs><marker id="ar-cm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><text x="30" y="30" font-size="14" fill="#c0392b" text-anchor="start" font-weight="bold">分類結果的四種情況：混淆矩陣（Confusion Matrix）</text><text x="231.0" y="80" font-size="12.5" fill="#57606a" text-anchor="middle" font-weight="bold">預測 Positive</text><text x="353.0" y="80" font-size="12.5" fill="#57606a" text-anchor="middle" font-weight="bold">預測 Negative</text><text x="158" y="128" font-size="12.5" fill="#57606a" text-anchor="end" font-weight="bold">實際 Positive</text><text x="158" y="190" font-size="12.5" fill="#57606a" text-anchor="end" font-weight="bold">實際 Negative</text><rect x="170" y="92" width="122" height="62" rx="4" fill="#e8f6ec" stroke="#1a7f37" stroke-width="1.8"/><text x="231.0" y="118" font-size="12.5" fill="#1a7f37" text-anchor="middle" font-weight="bold">TP 真陽性</text><text x="231.0" y="142" font-size="17" fill="#24292f" text-anchor="middle" font-weight="bold">126</text><rect x="292" y="92" width="122" height="62" rx="4" fill="#fdeaea" stroke="#c0392b" stroke-width="1.8"/><text x="353.0" y="118" font-size="12.5" fill="#c0392b" text-anchor="middle" font-weight="bold">FP 偽陽性</text><text x="353.0" y="142" font-size="17" fill="#24292f" text-anchor="middle" font-weight="bold">21</text><rect x="170" y="154" width="122" height="62" rx="4" fill="#fdeaea" stroke="#c0392b" stroke-width="1.8"/><text x="231.0" y="180" font-size="12.5" fill="#c0392b" text-anchor="middle" font-weight="bold">FN 偽陰性</text><text x="231.0" y="204" font-size="17" fill="#24292f" text-anchor="middle" font-weight="bold">7</text><rect x="292" y="154" width="122" height="62" rx="4" fill="#e8f6ec" stroke="#1a7f37" stroke-width="1.8"/><text x="353.0" y="180" font-size="12.5" fill="#1a7f37" text-anchor="middle" font-weight="bold">TN 真陰性</text><text x="353.0" y="204" font-size="17" fill="#24292f" text-anchor="middle" font-weight="bold">119</text><text x="292" y="238" font-size="12.5" fill="#0f766e" text-anchor="middle" font-weight="bold">總樣本 = 126 + 21 + 7 + 119 = 273</text><rect x="440" y="74" width="300" height="200" rx="8" fill="#ffffff" stroke="#2c6fb1" stroke-width="1.6"/><text x="456" y="100" font-size="13" fill="#2c6fb1" text-anchor="start" font-weight="bold">由此算出的五個指標</text><text x="456" y="128" font-size="12.5" fill="#1a7f37" text-anchor="start" font-weight="bold">Accuracy 準確率</text><text x="724" y="128" font-size="12.5" fill="#57606a" text-anchor="end" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">(126+119) / 273 = 89.74%</text><text x="456" y="157" font-size="12.5" fill="#2c6fb1" text-anchor="start" font-weight="bold">Precision 精確率</text><text x="724" y="157" font-size="12.5" fill="#57606a" text-anchor="end" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">126 / (126+21) = 85.71%</text><text x="456" y="186" font-size="12.5" fill="#d97706" text-anchor="start" font-weight="bold">Recall 召回率</text><text x="724" y="186" font-size="12.5" fill="#57606a" text-anchor="end" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">126 / (126+7) = 94.74%</text><text x="456" y="215" font-size="12.5" fill="#6f42c1" text-anchor="start" font-weight="bold">F1-score</text><text x="724" y="215" font-size="12.5" fill="#57606a" text-anchor="end" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">2PR/(P+R) = 0.900</text><text x="456" y="244" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="bold">Specificity 特異度</text><text x="724" y="244" font-size="12.5" fill="#57606a" text-anchor="end" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">119 / (119+21) = 85.00%</text><text x="30" y="302" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">門檻（threshold）怎麼移動，四格數字就跟著變——同一個模型，換門檻就換一組指標</text><line x1="80" y1="450" x2="730" y2="450" stroke="#57606a" stroke-width="1.8" marker-end="url(#ar-cm)"/><line x1="460" y1="348" x2="460" y2="496" stroke="#c0392b" stroke-width="2.2" stroke-dasharray="6 5"/><text x="460" y="340" font-size="12.5" fill="#c0392b" text-anchor="middle" font-weight="bold">threshold 門檻 = 0.5</text><text x="80" y="470" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">模型輸出機率小 →</text><text x="730" y="470" font-size="12" fill="#57606a" text-anchor="end" font-weight="normal">→ 大</text><circle cx="170" cy="405" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="240" cy="405" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="300" cy="405" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="390" cy="405" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="440" cy="405" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="100" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="135" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="175" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="215" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="255" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="295" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="335" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="370" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="405" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="445" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="490" cy="405" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="520" cy="405" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="552" cy="405" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="585" cy="405" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="615" cy="405" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="648" cy="405" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="688" cy="405" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="722" cy="405" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="478" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="502" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="528" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="556" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="582" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="608" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="636" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="662" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="695" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><circle cx="726" cy="478" r="5.5" fill="#2c6fb1" stroke="#2c6fb1" stroke-width="1.2"/><text x="200" y="384" font-size="11.5" fill="#c0392b" text-anchor="middle" font-weight="normal">FN 漏抓 = 7（實際是 Positive，卻被分成 Negative）</text><text x="250" y="502" font-size="11.5" fill="#2c6fb1" text-anchor="middle" font-weight="normal">TN 正確排除 = 119</text><text x="600" y="384" font-size="11.5" fill="#1a7f37" text-anchor="middle" font-weight="normal">TP 正確命中 = 126</text><text x="600" y="502" font-size="11.5" fill="#d97706" text-anchor="middle" font-weight="normal">FP 誤報 = 21（實際是 Negative，卻被分成 Positive）</text><text x="360" y="348" font-size="11.5" fill="#57606a" text-anchor="middle" font-weight="normal">● 紅色 = 實際 Positive　● 藍色 = 實際 Negative（示意圖，數量非等比例）</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 19：<b>混淆矩陣與門檻</b>（原稿 p25）。原稿的 2×2 表格就是 TP=126、FP=21、FN=7、TN=119（總共 273 筆）；四格數字可直接推出 Accuracy 89.74%、Precision 85.71%、Recall 94.74%、F1 0.900、Specificity 85.00%。下圖說明：<b>移動門檻</b>會同時改變 FN 與 FP，所以「要少漏抓」還是「要少誤報」是取捨，不是模型好壞。</figcaption>
</figure>

原稿的 2×2 表格數字是：**TP = 126、FP = 21、FN = 7、TN = 119**（總共 273 筆）。

| 縮寫 | 全名 | 中文 | 意義 |
|---|---|---|---|
| **TP** | True Positive | 真陽性 | 實際是正類，模型也說是正類 → **猜對** |
| **FP** | False Positive | 偽陽性 | 實際是負類，模型卻說是正類 → **誤報** |
| **FN** | False Negative | 偽陰性 | 實際是正類，模型卻說是負類 → **漏抓** |
| **TN** | True Negative | 真陰性 | 實際是負類，模型也說是負類 → **正確排除** |

由這四格算出的五個指標（**本筆記已用 Python 逐一驗算**）：

| 指標 | 公式 | 代入 | 結果 |
|---|---|---|---|
| **Accuracy 準確率** | (TP+TN) / 全部 | (126+119) / 273 | **89.74%** |
| **Precision 精確率** | TP / (TP+FP) | 126 / 147 | **85.71%** |
| **Recall 召回率** | TP / (TP+FN) | 126 / 133 | **94.74%** |
| **F1-score** | 2PR / (P+R) | 2×0.8571×0.9474 / 1.8045 | **0.900** |
| **Specificity 特異度** | TN / (TN+FP) | 119 / 140 | **85.00%** |

**口訣**：

- **Precision 看「預測為正的裡面有多少是真的」**（分母是**預測**的橫列／直行）→ 別誤報。
- **Recall 看「實際為正的裡面抓到多少」**（分母是**實際**的那一列／行）→ 別漏抓。
- **Accuracy 只看總體對的比例**，因此在**類別極不平衡**時會騙人
  （例如 99% 都是負類，全猜負類也有 99% 準確率，但 Recall = 0）。

### 19.2 門檻（threshold）的取捨

上圖下半部說明：模型輸出的是**機率**，要**自己選一個門檻**（例如 0.5）才變成類別。

| 把門檻調**高** | 把門檻調**低** |
|---|---|
| 更少被判為正類 → **FP 減少、FN 增加** | 更多被判為正類 → **FN 減少、FP 增加** |
| Precision 上升、Recall 下降 | Recall 上升、Precision 下降 |

所以選門檻要看**任務代價**：

- **寧可誤報、不可漏抓**（癌症篩檢、詐欺偵測、瑕疵檢測）→ **門檻調低**，追求高 **Recall**。
- **誤報代價很高**（把正常信件丟進垃圾桶、把正常客戶擋掉）→ **門檻調高**，追求高 **Precision**。

### 19.3 迴歸實例：`f(x) = 35 + 1.5x`（p26）

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 440" width="100%" style="max-width:760px;height:auto" role="img" aria-label="迴歸：找出輸入與數值輸出的關係"><defs><marker id="ar-rg2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><text x="30" y="30" font-size="14" fill="#c0392b" text-anchor="start" font-weight="bold">迴歸（Regression）：輸出是「連續數值」，模型學的是一條關係式</text><line x1="80.0" y1="380.0" x2="80.0" y2="70.0" stroke="#eaeef2" stroke-width="1"/><line x1="200.0" y1="380.0" x2="200.0" y2="70.0" stroke="#eaeef2" stroke-width="1"/><line x1="320.0" y1="380.0" x2="320.0" y2="70.0" stroke="#eaeef2" stroke-width="1"/><line x1="440.0" y1="380.0" x2="440.0" y2="70.0" stroke="#eaeef2" stroke-width="1"/><line x1="560.0" y1="380.0" x2="560.0" y2="70.0" stroke="#eaeef2" stroke-width="1"/><line x1="680.0" y1="380.0" x2="680.0" y2="70.0" stroke="#eaeef2" stroke-width="1"/><line x1="80.0" y1="380.0" x2="680.0" y2="380.0" stroke="#eaeef2" stroke-width="1"/><line x1="80.0" y1="302.5" x2="680.0" y2="302.5" stroke="#eaeef2" stroke-width="1"/><line x1="80.0" y1="225.0" x2="680.0" y2="225.0" stroke="#eaeef2" stroke-width="1"/><line x1="80.0" y1="147.5" x2="680.0" y2="147.5" stroke="#eaeef2" stroke-width="1"/><line x1="80.0" y1="70.0" x2="680.0" y2="70.0" stroke="#eaeef2" stroke-width="1"/><line x1="80" y1="380" x2="680" y2="380" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-rg2)"/><line x1="80" y1="380" x2="80" y2="80" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-rg2)"/><text x="688" y="396" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">x（特徵）</text><text x="66" y="76" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">y（目標值）</text><polyline points="80.00,325.75 83.75,324.30 87.50,322.84 91.25,321.39 95.00,319.94 98.75,318.48 102.50,317.03 106.25,315.58 110.00,314.12 113.75,312.67 117.50,311.22 121.25,309.77 125.00,308.31 128.75,306.86 132.50,305.41 136.25,303.95 140.00,302.50 143.75,301.05 147.50,299.59 151.25,298.14 155.00,296.69 158.75,295.23 162.50,293.78 166.25,292.33 170.00,290.88 173.75,289.42 177.50,287.97 181.25,286.52 185.00,285.06 188.75,283.61 192.50,282.16 196.25,280.70 200.00,279.25 203.75,277.80 207.50,276.34 211.25,274.89 215.00,273.44 218.75,271.98 222.50,270.53 226.25,269.08 230.00,267.62 233.75,266.17 237.50,264.72 241.25,263.27 245.00,261.81 248.75,260.36 252.50,258.91 256.25,257.45 260.00,256.00 263.75,254.55 267.50,253.09 271.25,251.64 275.00,250.19 278.75,248.73 282.50,247.28 286.25,245.83 290.00,244.38 293.75,242.92 297.50,241.47 301.25,240.02 305.00,238.56 308.75,237.11 312.50,235.66 316.25,234.20 320.00,232.75 323.75,231.30 327.50,229.84 331.25,228.39 335.00,226.94 338.75,225.48 342.50,224.03 346.25,222.58 350.00,221.12 353.75,219.67 357.50,218.22 361.25,216.77 365.00,215.31 368.75,213.86 372.50,212.41 376.25,210.95 380.00,209.50 383.75,208.05 387.50,206.59 391.25,205.14 395.00,203.69 398.75,202.23 402.50,200.78 406.25,199.33 410.00,197.88 413.75,196.42 417.50,194.97 421.25,193.52 425.00,192.06 428.75,190.61 432.50,189.16 436.25,187.70 440.00,186.25 443.75,184.80 447.50,183.34 451.25,181.89 455.00,180.44 458.75,178.98 462.50,177.53 466.25,176.08 470.00,174.62 473.75,173.17 477.50,171.72 481.25,170.27 485.00,168.81 488.75,167.36 492.50,165.91 496.25,164.45 500.00,163.00 503.75,161.55 507.50,160.09 511.25,158.64 515.00,157.19 518.75,155.73 522.50,154.28 526.25,152.83 530.00,151.38 533.75,149.92 537.50,148.47 541.25,147.02 545.00,145.56 548.75,144.11 552.50,142.66 556.25,141.20 560.00,139.75 563.75,138.30 567.50,136.84 571.25,135.39 575.00,133.94 578.75,132.48 582.50,131.03 586.25,129.58 590.00,128.12 593.75,126.67 597.50,125.22 601.25,123.77 605.00,122.31 608.75,120.86 612.50,119.41 616.25,117.95 620.00,116.50 623.75,115.05 627.50,113.59 631.25,112.14 635.00,110.69 638.75,109.23 642.50,107.78 646.25,106.33 650.00,104.88 653.75,103.42 657.50,101.97 661.25,100.52 665.00,99.06 668.75,97.61 672.50,96.16 676.25,94.70 680.00,93.25" fill="none" stroke="#2c6fb1" stroke-width="3.2" stroke-linecap="round"/><circle cx="170.0" cy="290.1" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="212.0" cy="274.6" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="260.0" cy="252.89999999999998" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="308.0" cy="243.6" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="350.0" cy="220.35" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="392.0" cy="209.5" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="440.0" cy="184.7" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="488.0" cy="173.85" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="530.0" cy="149.04999999999998" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="572.0" cy="139.75" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><circle cx="620.0" cy="113.39999999999998" r="5.5" fill="#c0392b" stroke="#c0392b" stroke-width="1.2"/><text x="104.0" y="91.69999999999999" font-size="15" fill="#2c6fb1" text-anchor="start" font-weight="bold" font-family="Cambria Math,Georgia,'Times New Roman',serif">f(x) = 35 + 1.5x</text><text x="104.0" y="113.39999999999998" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">斜率 1.5 = 每多 1 單位 x，y 增加 1.5</text><text x="104.0" y="132.0" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal">截距 35 = x 為 0 時的基準值</text><text x="428.0" y="287.0" font-size="12" fill="#c0392b" text-anchor="start" font-weight="normal">● 訓練資料（觀察值）</text><text x="428.0" y="308.7" font-size="12" fill="#2c6fb1" text-anchor="start" font-weight="normal">— 學到的模型（最佳擬合線）</text><rect x="556" y="60" width="190" height="250" rx="8" fill="#ffffff" stroke="#1a7f37" stroke-width="1.6"/><text x="568" y="84" font-size="12.5" fill="#1a7f37" text-anchor="start" font-weight="bold">驗證：代入模型算預測值</text><text x="568" y="114" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x = 54</text><text x="636" y="114" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">35 + 1.5×54</text><text x="736" y="114" font-size="13" fill="#24292f" text-anchor="end" font-weight="bold" font-family="Cambria Math,Georgia,'Times New Roman',serif">= 116</text><text x="568" y="148" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x = 62</text><text x="636" y="148" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">35 + 1.5×62</text><text x="736" y="148" font-size="13" fill="#24292f" text-anchor="end" font-weight="bold" font-family="Cambria Math,Georgia,'Times New Roman',serif">= 128</text><text x="568" y="182" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x = 68</text><text x="636" y="182" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">35 + 1.5×68</text><text x="736" y="182" font-size="13" fill="#24292f" text-anchor="end" font-weight="bold" font-family="Cambria Math,Georgia,'Times New Roman',serif">= 137</text><text x="568" y="216" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x = 74</text><text x="636" y="216" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">35 + 1.5×74</text><text x="736" y="216" font-size="13" fill="#24292f" text-anchor="end" font-weight="bold" font-family="Cambria Math,Georgia,'Times New Roman',serif">= 146</text><text x="568" y="250" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">x = 80</text><text x="636" y="250" font-size="12" fill="#57606a" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">35 + 1.5×80</text><text x="736" y="250" font-size="13" fill="#24292f" text-anchor="end" font-weight="bold" font-family="Cambria Math,Georgia,'Times New Roman',serif">= 155</text><text x="568" y="296" font-size="12" fill="#0f766e" text-anchor="start" font-weight="bold">誤差越小越好：MAE / MSE / R²</text><text x="30" y="420" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">迴歸的輸出是數字（房價、溫度、銷量），所以不能用 Sigmoid 把值壓進 0～1；評估用 MAE／MSE／R²，而不是 Accuracy。</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 20：<b>迴歸範例</b>（原稿 p26）。模型 <code>f(x) = 35 + 1.5x</code>：把 x = 54／62／68／74／80 代入，得到預測值 116／128／137／146／155，再與實際值比較算出誤差。迴歸的輸出是連續數值，所以指標用 MAE／MSE／R²，而不是分類用的 Accuracy。</figcaption>
</figure>

原稿 p26 的圖示範：用訓練資料學出一條直線，再把新的 x 代入求預測值。

| 輸入 x | 計算 | 預測值 |
|---|---|---|
| 54 | 35 + 1.5 × 54 | **116** |
| 62 | 35 + 1.5 × 62 | **128** |
| 68 | 35 + 1.5 × 68 | **137** |
| 74 | 35 + 1.5 × 74 | **146** |
| 80 | 35 + 1.5 × 80 | **155** |

**模型怎麼讀**：

- **截距 35**：x = 0 時的基準值（bias）。
- **斜率 1.5**：x 每增加 1 個單位，預測值增加 1.5 —— 這就是「學到的關係」。
- 預測值與實際值的差就是**誤差**；迴歸的評估指標是 **MAE（平均絕對誤差）**、
  **MSE（均方誤差）**、**R²（決定係數）**，而**不是** Accuracy。

> **考點（這一頁很愛考計算）**：
> 1. 看到「準確率 89.74%」要能反推 → (126+119)/273。
> 2. Precision 的分母是 **(TP+FP)**；Recall 的分母是 **(TP+FN)**——**別抄反**。
> 3. 迴歸評估用 **MAE / MSE / R²**；分類評估用 **Accuracy / Precision / Recall / F1**。
> 4. 代入題型：`f(x) = 35 + 1.5x`，x = 80 → **155**。

---

## 20. 非監督式學習 Unsupervised Learning（PDF p28）

<!-- p: 28 -->

原稿 p28 的標題（同時也是定義）是：

> **Unsupervised Learning: unlabeled observations {x₁, …, xₙ}**

條列內容（原文照錄 + 翻譯）：

| 原稿 | 中文 |
|---|---|
| Learning algorithm must **identify patterns from features alone** | 學習演算法必須**只從特徵本身**找出模式（沒有答案可對） |
| Can be the **goal inside itself** (discover hidden patterns, exploratory analysis) | 可以**本身就是目的**：發現隱藏的模式、做探索式分析 |
| Can be **means to an end** (pre-processing for supervised task) | 也可以是**手段**：當作監督式任務的**前處理** |
| Examples: **Clustering** | 例子：**分群** |

### 20.1 與監督式學習的對照

| 比較 | Supervised 監督式 | Unsupervised 非監督式 |
|---|---|---|
| 資料 | `{(x₁,y₁)…(xₙ,yₙ)}`（**有標籤**） | `{x₁…xₙ}`（**只有特徵**） |
| 學什麼 | 輸入 → 標籤的對應 | 資料本身的**結構／模式** |
| 典型任務 | 分類、迴歸 | **分群**、降維、異常偵測 |
| 有沒有標準答案 | 有（可以算 Accuracy） | **沒有**（只能靠人解讀結果） |

### 20.2 非監督式的兩種用途

1. **本身就是目的**：探索式分析——例如先分群看看資料自然分成幾類、找出異常樣本。
2. **當作前處理**：先用非監督式方法把資料整理好（分群、降維、找特徵），
   再交給監督式模型訓練。例如先用 k-means 產生「群編號」當成新特徵。

> **考點**：
> 1. 非監督式的資料形式是 **`{x₁, …, xₙ}`**（**沒有 y**）。
> 2. 原稿點出的兩個用途：**goal inside itself** 與 **means to an end（前處理）**。
> 3. 原稿在非監督式下列出的代表方法是 **Clustering（分群）**。

---

## 21. Clustering：分群的兩個距離目標（PDF p29）

<!-- p: 29 -->

原稿 p29 沒有任何句子，只有四段重複的標註文字：

```
Intracluster distances are minimized
Intercluster distances are maximized
```

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 380" width="100%" style="max-width:760px;height:auto" role="img" aria-label="分群的兩個距離目標"><defs><marker id="ar-cl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><text x="30" y="30" font-size="14" fill="#c0392b" text-anchor="start" font-weight="bold">分群的目標：群內越緊密越好、群間越遠越好</text><circle cx="165" cy="130" r="68" fill="#ffffff" stroke="#1a7f37" stroke-width="1.4" opacity="0.55"/><circle cx="120" cy="104" r="6" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><circle cx="150" cy="96" r="6" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><circle cx="196" cy="108" r="6" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><circle cx="214" cy="140" r="6" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><circle cx="170" cy="158" r="6" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><circle cx="132" cy="142" r="6" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><circle cx="165" cy="130" r="12" fill="#ffffff" stroke="#1a7f37" stroke-width="2.2"/><text x="160" y="135" font-size="13" fill="#1a7f37" text-anchor="middle" font-weight="bold">×</text><circle cx="300" cy="262" r="68" fill="#ffffff" stroke="#d97706" stroke-width="1.4" opacity="0.55"/><circle cx="258" cy="240" r="6" fill="#d97706" stroke="#d97706" stroke-width="1.2"/><circle cx="286" cy="226" r="6" fill="#d97706" stroke="#d97706" stroke-width="1.2"/><circle cx="330" cy="236" r="6" fill="#d97706" stroke="#d97706" stroke-width="1.2"/><circle cx="344" cy="266" r="6" fill="#d97706" stroke="#d97706" stroke-width="1.2"/><circle cx="312" cy="292" r="6" fill="#d97706" stroke="#d97706" stroke-width="1.2"/><circle cx="268" cy="280" r="6" fill="#d97706" stroke="#d97706" stroke-width="1.2"/><circle cx="300" cy="262" r="12" fill="#ffffff" stroke="#d97706" stroke-width="2.2"/><text x="295" y="267" font-size="13" fill="#d97706" text-anchor="middle" font-weight="bold">×</text><circle cx="590" cy="152" r="68" fill="#ffffff" stroke="#6f42c1" stroke-width="1.4" opacity="0.55"/><circle cx="548" cy="128" r="6" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="578" cy="112" r="6" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="624" cy="126" r="6" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="640" cy="158" r="6" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="600" cy="184" r="6" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="556" cy="168" r="6" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="590" cy="152" r="12" fill="#ffffff" stroke="#6f42c1" stroke-width="2.2"/><text x="585" y="157" font-size="13" fill="#6f42c1" text-anchor="middle" font-weight="bold">×</text><line x1="120" y1="104" x2="214" y2="140" stroke="#c0392b" stroke-width="2.4" stroke-dasharray="5 4"/><text x="96" y="96" font-size="11.5" fill="#c0392b" text-anchor="start" font-weight="bold">intra-cluster distance</text><text x="96" y="82" font-size="11.5" fill="#c0392b" text-anchor="start" font-weight="normal">（群內距離）最小化</text><line x1="214" y1="140" x2="258" y2="240" stroke="#c0392b" stroke-width="2.4" stroke-dasharray="5 4"/><text x="640" y="128" font-size="11.5" fill="#c0392b" text-anchor="start" font-weight="bold">intra-cluster distance</text><text x="640" y="114" font-size="11.5" fill="#c0392b" text-anchor="start" font-weight="normal">（群內距離）最小化</text><line x1="165" y1="130" x2="300" y2="262" stroke="#2c6fb1" stroke-width="2.6" marker-end="url(#ar-cl)"/><text x="238" y="190" font-size="12" fill="#2c6fb1" text-anchor="start" font-weight="bold">inter-cluster distance</text><text x="238" y="208" font-size="12" fill="#2c6fb1" text-anchor="start" font-weight="normal">（群間距離）最大化</text><line x1="300" y1="262" x2="590" y2="152" stroke="#2c6fb1" stroke-width="2.6" marker-end="url(#ar-cl)"/><line x1="165" y1="130" x2="590" y2="152" stroke="#2c6fb1" stroke-width="2" stroke-dasharray="4 4" marker-end="url(#ar-cl)"/><text x="470" y="268" font-size="12" fill="#2c6fb1" text-anchor="start" font-weight="normal">同一個群的中心越遠越好</text><text x="30" y="340" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">k-means 的作法：先隨機挑 k 個中心 → 把每個點指派給最近的中心 → 重算各群中心 → 反覆迭代；它最小化的目標就是「群內距離平方和」（inertia）。</text><text x="30" y="364" font-size="12.5" fill="#57606a" text-anchor="start" font-weight="normal">k 要自己決定（elbow method 看 inertia 轉折）；k-means 假設群是球形且大小相近，對離群值敏感。</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 21：<b>分群的兩個距離</b>（原稿 p29）。原稿只寫了兩句：intracluster distances are minimized、intercluster distances are maximized。白話就是：<b>同一群的點要盡量靠近，不同群的點要盡量分開</b>；k-means 就是在最小化群內距離平方和。</figcaption>
</figure>

### 21.1 兩句話的真正意思

| 名詞 | 中文 | 目標 |
|---|---|---|
| **Intracluster distance** | 群**內**距離 | **最小化（minimized）**——同一群的點越靠近越好 |
| **Intercluster distance** | 群**間**距離 | **最大化（maximized）**——不同群的中心越遠越好 |

一句話：**「同群要緊、異群要遠」**。

### 21.2 k-means 怎麼做到這件事

k-means 是最常見的分群演算法，步驟是：

1. 決定 **k**（要分幾群），隨機挑 k 個中心點（centroid）。
2. **指派**：把每個資料點分給**最近**的中心。
3. **更新**：把每個群的中心重算成該群所有點的平均。
4. **重複** 2–3 直到中心不再移動（或達到最大迭代次數）。

它真正在最小化的目標函數叫 **inertia（群內距離平方和）**：

```
inertia = Σ (每個點到它所屬群中心的距離²)
```

**inertia 越小，代表同一群越緊密**——這就是「intracluster distances are minimized」。

### 21.3 使用 k-means 的三個實務注意事項

| 注意事項 | 說明 |
|---|---|
| **k 要自己決定** | 常用 **elbow method（手肘法）**：把 k 從 1 往上畫 inertia，找曲線轉折（手肘）的位置 |
| **對尺度敏感** | 特徵單位差很多時（例如公分 vs 元），必須先**標準化** |
| **對離群值敏感** | 因為中心是「平均值」，一個極端值會把中心拉走；形狀假設是**球形且大小相近** |

> **考點**：
> 1. 背下這兩句：**intracluster distances are minimized / intercluster distances are maximized**。
> 2. k-means 的目標函數是 **inertia（群內距離平方和）**。
> 3. k-means 屬於**非監督式學習**，而且**k 需要人先指定**。

---

## 22. Clustering：分群實例（PDF p30）

<!-- p: 30 -->

原稿 p30 只有「**Clustering**」一個字，其餘是圖：用花朵的量測資料（經典的鳶尾花 iris 資料集）
示範「沒有品種標籤也能把花分成幾群」。

<figure style="margin:20px 0;padding:14px 12px;background:#f6f8fa;border:1px solid #d8dee4;border-radius:10px;text-align:center">
<svg viewBox="0 0 760 420" width="100%" style="max-width:760px;height:auto" role="img" aria-label="花萼花瓣資料的分群結果"><defs><marker id="ar-km" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#57606a"/></marker></defs><text x="30" y="30" font-size="14" fill="#c0392b" text-anchor="start" font-weight="bold">Clustering：沒有品種標籤，只靠量測值把花分成 3 群</text><line x1="144.0" y1="372.0" x2="144.0" y2="78.0" stroke="#eaeef2" stroke-width="1"/><line x1="192.0" y1="372.0" x2="192.0" y2="78.0" stroke="#eaeef2" stroke-width="1"/><line x1="240.0" y1="372.0" x2="240.0" y2="78.0" stroke="#eaeef2" stroke-width="1"/><line x1="288.0" y1="372.0" x2="288.0" y2="78.0" stroke="#eaeef2" stroke-width="1"/><line x1="336.0" y1="372.0" x2="336.0" y2="78.0" stroke="#eaeef2" stroke-width="1"/><line x1="96.0" y1="330.0" x2="345.6" y2="330.0" stroke="#eaeef2" stroke-width="1"/><line x1="96.0" y1="288.0" x2="345.6" y2="288.0" stroke="#eaeef2" stroke-width="1"/><line x1="96.0" y1="246.0" x2="345.6" y2="246.0" stroke="#eaeef2" stroke-width="1"/><line x1="96.0" y1="204.0" x2="345.6" y2="204.0" stroke="#eaeef2" stroke-width="1"/><line x1="96.0" y1="162.0" x2="345.6" y2="162.0" stroke="#eaeef2" stroke-width="1"/><line x1="96.0" y1="120.0" x2="345.6" y2="120.0" stroke="#eaeef2" stroke-width="1"/><line x1="96.0" y1="78.0" x2="345.6" y2="78.0" stroke="#eaeef2" stroke-width="1"/><line x1="96" y1="372" x2="350" y2="372" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-km)"/><line x1="96" y1="372" x2="96" y2="78" stroke="#57606a" stroke-width="1.6" marker-end="url(#ar-km)"/><text x="358" y="388" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">petal width</text><text x="82" y="74" font-size="14" fill="#57606a" text-anchor="middle" font-weight="normal" font-style="italic" font-family="Cambria Math,Georgia,'Times New Roman',serif">petal length</text><circle cx="117.12" cy="309.0" r="34" fill="#ffffff" stroke="#1a7f37" stroke-width="1.2" opacity="0.5"/><circle cx="110.4" cy="313.2" r="6" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><circle cx="115.2" cy="309.0" r="6" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><circle cx="120.0" cy="317.4" r="6" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><circle cx="124.8" cy="304.8" r="6" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><circle cx="113.28" cy="300.6" r="6" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><circle cx="117.12" cy="309.0" r="11" fill="#ffffff" stroke="#1a7f37" stroke-width="2.2"/><text x="113.12" y="313.0" font-size="12" fill="#1a7f37" text-anchor="middle" font-weight="bold">×</text><text x="131.12" y="295.0" font-size="11.5" fill="#1a7f37" text-anchor="start" font-weight="bold">cluster 0</text><circle cx="210.24" cy="190.56" r="34" fill="#ffffff" stroke="#d97706" stroke-width="1.2" opacity="0.5"/><circle cx="192.0" cy="204.0" r="6" fill="#d97706" stroke="#d97706" stroke-width="1.2"/><circle cx="211.2" cy="191.4" r="6" fill="#d97706" stroke="#d97706" stroke-width="1.2"/><circle cx="220.8" cy="183.0" r="6" fill="#d97706" stroke="#d97706" stroke-width="1.2"/><circle cx="201.60000000000002" cy="195.6" r="6" fill="#d97706" stroke="#d97706" stroke-width="1.2"/><circle cx="225.60000000000002" cy="178.8" r="6" fill="#d97706" stroke="#d97706" stroke-width="1.2"/><circle cx="210.24" cy="190.56" r="11" fill="#ffffff" stroke="#d97706" stroke-width="2.2"/><text x="206.24" y="194.56" font-size="12" fill="#d97706" text-anchor="middle" font-weight="bold">×</text><text x="224.24" y="176.56" font-size="11.5" fill="#d97706" text-anchor="start" font-weight="bold">cluster 1</text><circle cx="291.84000000000003" cy="119.16000000000003" r="34" fill="#ffffff" stroke="#6f42c1" stroke-width="1.2" opacity="0.5"/><circle cx="268.8" cy="141.0" r="6" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="288.0" cy="120.0" r="6" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="307.20000000000005" cy="107.40000000000003" r="6" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="278.4" cy="128.4" r="6" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="316.79999999999995" cy="99.0" r="6" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><circle cx="291.84000000000003" cy="119.16000000000003" r="11" fill="#ffffff" stroke="#6f42c1" stroke-width="2.2"/><text x="287.84000000000003" y="123.16000000000003" font-size="12" fill="#6f42c1" text-anchor="middle" font-weight="bold">×</text><text x="305.84000000000003" y="105.16000000000003" font-size="11.5" fill="#6f42c1" text-anchor="start" font-weight="bold">cluster 2</text><text x="96" y="404" font-size="11.5" fill="#57606a" text-anchor="start" font-weight="normal">橫軸 petal width、縱軸 petal length；× 是各群中心（centroid）</text><rect x="420" y="62" width="320" height="300" rx="8" fill="#ffffff" stroke="#d8dee4" stroke-width="1.6"/><text x="434" y="88" font-size="12.5" fill="#2c6fb1" text-anchor="start" font-weight="bold">原始資料（未標籤的觀察值）</text><text x="436" y="118" font-size="11" fill="#57606a" text-anchor="start" font-weight="bold">sepal</text><text x="436" y="132" font-size="11" fill="#57606a" text-anchor="start" font-weight="bold">length</text><text x="496" y="118" font-size="11" fill="#57606a" text-anchor="start" font-weight="bold">sepal</text><text x="496" y="132" font-size="11" fill="#57606a" text-anchor="start" font-weight="bold">width</text><text x="556" y="118" font-size="11" fill="#57606a" text-anchor="start" font-weight="bold">petal</text><text x="556" y="132" font-size="11" fill="#57606a" text-anchor="start" font-weight="bold">length</text><text x="616" y="118" font-size="11" fill="#57606a" text-anchor="start" font-weight="bold">petal</text><text x="616" y="132" font-size="11" fill="#57606a" text-anchor="start" font-weight="bold">width</text><text x="682" y="118" font-size="11" fill="#57606a" text-anchor="start" font-weight="bold">k-means</text><text x="682" y="132" font-size="11" fill="#57606a" text-anchor="start" font-weight="bold">群</text><text x="436" y="162" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">5.1</text><text x="496" y="162" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">3.5</text><text x="556" y="162" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">1.4</text><text x="616" y="162" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">0.2</text><circle cx="690" cy="158" r="11" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><text x="690" y="162" font-size="11.5" fill="#ffffff" text-anchor="middle" font-weight="bold">0</text><text x="436" y="196" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">4.9</text><text x="496" y="196" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">3.0</text><text x="556" y="196" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">1.4</text><text x="616" y="196" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">0.2</text><circle cx="690" cy="192" r="11" fill="#1a7f37" stroke="#1a7f37" stroke-width="1.2"/><text x="690" y="196" font-size="11.5" fill="#ffffff" text-anchor="middle" font-weight="bold">0</text><text x="436" y="230" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">7.0</text><text x="496" y="230" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">3.2</text><text x="556" y="230" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">4.7</text><text x="616" y="230" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">1.4</text><circle cx="690" cy="226" r="11" fill="#d97706" stroke="#d97706" stroke-width="1.2"/><text x="690" y="230" font-size="11.5" fill="#ffffff" text-anchor="middle" font-weight="bold">1</text><text x="436" y="264" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">6.4</text><text x="496" y="264" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">3.2</text><text x="556" y="264" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">4.5</text><text x="616" y="264" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">1.5</text><circle cx="690" cy="260" r="11" fill="#d97706" stroke="#d97706" stroke-width="1.2"/><text x="690" y="264" font-size="11.5" fill="#ffffff" text-anchor="middle" font-weight="bold">1</text><text x="436" y="298" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">6.3</text><text x="496" y="298" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">3.3</text><text x="556" y="298" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">6.0</text><text x="616" y="298" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">2.5</text><circle cx="690" cy="294" r="11" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><text x="690" y="298" font-size="11.5" fill="#ffffff" text-anchor="middle" font-weight="bold">2</text><text x="436" y="332" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">5.8</text><text x="496" y="332" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">2.7</text><text x="556" y="332" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">5.1</text><text x="616" y="332" font-size="12" fill="#24292f" text-anchor="start" font-weight="normal" font-family="Cambria Math,Georgia,'Times New Roman',serif">1.9</text><circle cx="690" cy="328" r="11" fill="#6f42c1" stroke="#6f42c1" stroke-width="1.2"/><text x="690" y="332" font-size="11.5" fill="#ffffff" text-anchor="middle" font-weight="bold">2</text><text x="434" y="384" font-size="11.5" fill="#0f766e" text-anchor="start" font-weight="normal">k = 3 是自己選的；結果與真實品種高度一致，</text><text x="434" y="402" font-size="11.5" fill="#0f766e" text-anchor="start" font-weight="normal">但演算法全程沒看到品種標籤。</text></svg>
<figcaption style="font-size:13.5px;color:#57606a;margin-top:10px;line-height:1.65;text-align:left">圖 22：<b>Clustering 範例</b>（原稿 p30）。用經典的鳶尾花（iris）資料：4 個量測特徵、沒有任何品種標籤，k-means 分成 3 群後，與真實品種大致吻合。要注意：非監督式學習的「群」不是標準答案，它只是資料結構的呈現，仍需要人來解讀。</figcaption>
</figure>

### 22.1 這個例子在示範什麼

| 面向 | 內容 |
|---|---|
| 資料 | 每朵花有 4 個量測值：sepal length、sepal width、**petal length**、**petal width** |
| 標籤 | **沒有**——品種（setosa / versicolor / virginica）不提供給演算法 |
| 方法 | 對特徵做 **k-means 分群**（這裡 k = 3） |
| 結果 | 演算法自己找出 3 群，與真實品種大致吻合 |

### 22.2 為什麼這個例子重要

1. **它證明了「特徵本身就有結構」**：就算沒有答案，資料自然會聚成幾團。
2. **它示範了非監督式的價值**：先分群 → 再由人來解讀每一群代表什麼（探索式分析）。
3. **它也是監督式任務的前處理**：把「群編號」當成新特徵，再餵給分類器。

### 22.3 要小心的地方

- 分群結果**不是標準答案**：k 選 2 或 4 就會得到不同的群；
  演算法只保證「同群緊、異群遠」，不保證「每一群等於一個真實類別」。
- 真實資料裡群常常是**重疊**的（本圖中 cluster 1 與 cluster 2 就比較靠近），
  所以「分群」通常要搭配**領域知識**才能解讀。

> **考點**：
> 1. 分群範例屬於**非監督式學習**，因為**沒有使用標籤**。
> 2. k-means 的 k 是**人為指定**的參數，不是演算法自己決定的。
> 3. 分群的結果需要**人來解讀**，不像分類可以直接算 Accuracy。

---

## 附錄 A：名詞速查表

### A.1 神經網路結構

| 名詞 | 英文 | 一句話 |
|---|---|---|
| 細胞體 | soma / cell body | 含細胞核，負責整合訊號 |
| 樹突 | dendrites | 接收訊號 |
| 軸突 | axon | 送出訊號 |
| 突觸 | synapses | 神經元之間的接點（一個神經元可連 10～100,000 個） |
| 動作電位 | action potential | 全有全無的脈衝；達閾值才發火，**沒有部分發火** |
| 人工神經元 | artificial neuron | 把輸入通過函數後輸出 |
| 權重 | weight | 神經元之間傳遞的數值（可學習） |
| 偏置 | bias | 加在加權總和上的可學習常數 |
| 輸入層 | input layer | 接收特徵 |
| 隱藏層 | hidden layer | 做特徵轉換；越多層越「深」 |
| 輸出層 | output layer | 產生最後答案 |
| 前向傳播 | feed-forward | 輸入 → 輸出 |
| 反向傳播 | back propagation | 用誤差回頭更新權重 |
| ANN | Artificial Neural Network | 人工神經網路（淺層、簡單任務） |
| DNN | Deep Neural Network | 深度網路（**> 2 個隱藏層**、複雜模式辨識） |
| 網路拓撲 | network topology | 網路的形狀：層數、寬度、連接方式 |

### A.2 激勵函數

| 名詞 | 公式 | 值域 | 用途 |
|---|---|---|---|
| TLU | `y = 1 if a ≥ θ else 0` | {0, 1} | 早期感知機；不可微 |
| ReLU | `max(0, a)` | [0, ∞) | 隱藏層預設 |
| Sigmoid | `1/(1+e⁻ᵃ)` | (0, 1) | 二元分類輸出層 |
| Softmax | `e^zᵢ / Σⱼe^zⱼ` | (0,1)、總和 1 | 多類別分類輸出層 |
| 閾值 | threshold θ | — | TLU 的門檻 |
| 非線性 | non-linearity | — | 激勵函數存在的核心理由 |
| 梯度消失 | vanishing gradient | — | Sigmoid 兩端飽和造成的問題 |

### A.3 機器學習

| 名詞 | 英文 | 一句話 |
|---|---|---|
| 特徵 / 標籤 | feature / label | 輸入 x / 答案 y |
| 監督式 | supervised | 有標籤 `{(xᵢ,yᵢ)}` |
| 非監督式 | unsupervised | 沒標籤 `{xᵢ}` |
| 強化式 | reinforcement | 靠獎勵試錯 |
| 分類 / 迴歸 | classification / regression | 輸出類別 / 輸出數值 |
| 二元／多類別／多標籤 | binary / multiclass / multilabel | Sigmoid / Softmax / 多個 Sigmoid |
| 分群 | clustering | 非監督式；同群緊、異群遠 |
| 慣性 | inertia | k-means 最小化的群內距離平方和 |
| 手肘法 | elbow method | 用 inertia 轉折挑 k |
| 資料科學／探勘／大數據 | data science / mining / big data | 方法 / 找模式 / 原料 |

### A.4 評估指標

| 指標 | 公式 | 用在哪 |
|---|---|---|
| Accuracy | (TP+TN) / 全部 | 分類（類別平衡時） |
| Precision | TP / (TP+FP) | 分類（怕誤報） |
| Recall | TP / (TP+FN) | 分類（怕漏抓） |
| F1 | 2PR / (P+R) | 分類（P、R 的折衷） |
| Specificity | TN / (TN+FP) | 分類（負類抓得準不準） |
| MAE / MSE / R² | — | **迴歸** |

---

## 附錄 B：常見錯誤與陷阱

### B.1 十大陷阱總表

| # | 陷阱 | 錯誤寫法／想法 | 正確寫法／想法 |
|---|---|---|---|
| 1 | **Deep 的判斷標準** | 「資料很多就是 deep」 | **隱藏層 > 2 層**才是 deep |
| 2 | **激勵函數的位置** | 「接在網路外面」 | 位於**神經元內部**，處理加權總和後的 a |
| 3 | **拿掉激勵函數** | 「只是少一個步驟」 | 多層網路會**退化成線性模型** |
| 4 | **Sigmoid vs Softmax** | 「多類別用 Sigmoid」 | 多類別**互斥**用 **Softmax**；多標籤才用多個 Sigmoid |
| 5 | **ReLU 梯度** | 「ReLU 到處梯度都是 1」 | **正區間**梯度 1；**負區間**梯度 0（可能 dead neuron） |
| 6 | **TLU 的輸出** | 「輸出機率」 | 只有 **0 / 1**，且**不可微**、解不了 XOR |
| 7 | **Precision / Recall 分母抄反** | Precision = TP/(TP+FN) | **Precision = TP/(TP+FP)**；**Recall = TP/(TP+FN)** |
| 8 | **門檻與指標的關係** | 「門檻不影響指標」 | 門檻 ↓ → Recall ↑、FP ↑；門檻 ↑ → Precision ↑、FN ↑ |
| 9 | **迴歸用 Accuracy** | 「用準確率評估房價預測」 | 迴歸用 **MAE / MSE / R²** |
| 10 | **k-means 的 k** | 「演算法自己會決定 k」 | **k 要人指定**（常用 elbow method 挑） |

### B.2 三個容易混淆的對照

| 容易混淆 | 分清楚的方法 |
|---|---|
| **驗證（validate） vs 測試（test）** | 驗證集用來**調參數**（可重複用）；測試集**只用一次**，用來報告最終表現 |
| **前向傳播 vs 反向傳播** | 前向＝算答案；反向＝用誤差**改權重** |
| **監督式 vs 非監督式** | 看**有沒有標籤**（有沒有 y），不是看演算法名字 |

---

## 附錄 C：教材頁面索引對照

| PDF 頁 | 原稿標題／內容 | 本筆記對應章節 |
|:---:|---|---|
| 1 | 封面：Neural Network, Activation Function and Machine Learning | §1 |
| 2 | Neural Network — AI Basic Principles（生物神經元構造） | §2.1 |
| 3 | Neural Network — AI Basic Principles（動作電位、學習） | §2.2 |
| 4 | Neural Network（neurons / weights + 圖） | §3 |
| 5 | Artificial Neural Network（三層 + feed-forward / back propagation） | §4 |
| 6 | Artificial Neural Network — ANN and DNN（定義） | §5 |
| 7 | Deep Neural Network — Network Topology | §6 |
| 8 | Activation Function（定義） | §7 |
| 9 | Threshold Logic Unit (TLU)（結構圖） | §8.1 |
| 10 | TLU -activation（圖形） | §8.2 |
| 11 | Rectified Linear Units (ReLU)（結構圖） | §9.1 |
| 12 | ReLU -activation（圖形） | §9.2 |
| 13 | Sigmoid Function（結構圖） | §10.1 |
| 14 | Sigmoid -activation / Softmax -activation（圖形） | §10.2 |
| 15 | Softmax Function（結構圖） | §11.1 |
| 16 | Softmax Function（圖形） | §11.2 |
| 17 | Problem → Classification / Regression → TLU / Softmax / Sigmoid / ReLU | §12 |
| 18 | Machine Learning — Analytics and Machine Learning（三個主題） | §13 |
| 19 | Machine Learning — Basic Concepts（圖） | §14 |
| 20 | Ten Steps to a Machine Learning Solution | §15 |
| 21 | The Data/AI Landscape（圖） | §16 |
| 22 | Machine Learning - Types（三個問句） | §17 |
| 23 | Supervised Learning: labeled observations（Learning Strategy） | §18 |
| 24 | Machine Learning - Types（加上 Classification / Regression） | §17 |
| 25 | 分類實例（混淆矩陣、門檻；全圖、無文字） | §19.1–19.2 |
| 26 | 迴歸實例（f(x) = 35 + 1.5x；全圖、無文字） | §19.3 |
| 27 | Machine Learning - Types（與 p24 相同） | §17 |
| 28 | Unsupervised Learning: unlabeled observations（Learning Strategy） | §20 |
| 29 | Intracluster / intercluster distances（圖） | §21 |
| 30 | Clustering（花朵分群圖） | §22 |

> **使用方式**：考試若遇到「原稿第 N 頁在講什麼」的題目，直接查這張表。
> p25、p26、p29、p30 是**純圖頁**（PDF 抽不出文字），本筆記已重繪為圖 19–22。

---

## 附錄 D：延伸資源與離線提示

### D.1 這份筆記怎麼離線用

| 檔案 | 用途 |
|---|---|
| `index.html` | **單一檔案**的完整筆記；下載後雙擊即可用瀏覽器開啟，**不需要網路** |
| `Neural_Network_Activation_Function_and_ML_Study_Notes.md` | 原始 Markdown，方便自己改、自己加註 |
| `mc-quiz.html` | 60 題互動測驗（同一個資料夾，離線可用） |

本筆記的所有插圖都是**內嵌 SVG**（向量圖），所以：

- 沒有連外圖片、沒有外部字型、沒有 CDN → **飛航模式也能看**。
- 放大不會模糊（向量圖），列印也清楚。

### D.2 插圖是怎麼產生的（可重現）

22 張插圖由一支小程式產生（純標準庫、無第三方套件）：

```text
python diagrams.py notes_src.md output.md     # 把 {{DIAGRAM:key}} 換成內嵌 SVG
python check_md.py output.md                  # 檢查 SVG 是否合法、有無壞掉的標記
```

- 曲線（Sigmoid、指數）與數值（Softmax 機率、混淆矩陣指標、迴歸預測值）都是**算出來的**，
  不是手繪猜的。
- 產生的 SVG 用 XML 解析器逐張驗證過（22/22 合法），且**沒有任何外部 URL**。

### D.3 本筆記補充資料的來源（用於交叉查核，非原稿內容）

| 主題 | 查核來源 |
|---|---|
| 混淆矩陣與 Precision / Recall / F1 定義 | Wikipedia「Confusion matrix」「Precision and recall」 |
| k-means、inertia、elbow method | scikit-learn 官方文件（Clustering 章節） |
| AI / ML / DL 的從屬關係、資料科學與大數據 | 業界常見定義（Dataversity 等資料管理媒體） |
| 「Ten Steps to a Machine Learning Solution」 | Dataversity 的十步版本（與原稿條列一致） |
| 激勵函數的公式與值域 | 大學課程講義（Northeastern 等）與標準教科書 |
| TLU / 感知機 / XOR 限制的歷史 | Wikipedia「Perceptron」「Artificial neuron」 |
| Softmax 的定義與平移不變性 | Wikipedia「Softmax function」 |

> 註：原稿未標註參考文獻，以上僅為筆者為確保正確性所做的交叉查核；
> **考試請以原稿與講師說明為準**。

---

## 附錄 E：一頁精華（考前 10 分鐘）

```text
========== 1. 生物 → 人工 ==========
樹突（收）→ 細胞體（加總）→ 過閾值才發火（全有全無、沒有部分發火）→ 軸突（送）→ 突觸
對應到人工：輸入 x → a = Σwᵢxᵢ + b → f(a) → y
神經網路的兩個零件：Neurons（把輸入通過函數後輸出）、Weights（神經元之間傳遞的數值）

========== 2. 網路結構 ==========
Input Layer → Hidden Layer（可多層）→ Output Layer
Feed-forward：輸入往輸出算答案
Back Propagation：誤差由輸出往輸入回傳，用來更新權重
ANN：淺、簡單任務        DNN：> 2 個隱藏層、複雜模式辨識（CV / NLP）
Network Topology = 網路的形狀（層數、寬度、連接方式）

========== 3. 激勵函數 ==========
定義：神經元內部的數學規則；把輸入加總後決定要不要送出；加入「非線性」讓網路能學難的模式
TLU     y = 1 if a ≥ θ else 0   輸出 {0,1}，不可微，解不了 XOR
ReLU    f(a) = max(0, a)        隱藏層預設；正區間梯度 1；負區間 0（dead neuron）
Sigmoid σ(a) = 1/(1+e⁻ᵃ)        輸出 (0,1)，σ(0)=0.5；兩端飽和 → 梯度消失
Softmax pᵢ = e^zᵢ/Σⱼe^zⱼ        輸出總和 = 1，多類別分類
範例：z=[2.0,1.0,0.1] → e^z=[7.389,2.718,1.105]（總和 11.213）→ p=[0.659,0.242,0.099]

========== 4. 問題 → 激勵函數 ==========
Classification ─┬─ Binary      → 1 個輸出 + Sigmoid
                 ├─ Multiclass  → K 個輸出 + Softmax（互斥）
                 └─ Multilabel  → 每個標籤一個 Sigmoid
Regression → ReLU / 線性（輸出連續數值；用 MAE / MSE / R² 評估）

========== 5. 機器學習 ==========
十步：定義問題 → 定目標變數與指標 → 取資料 → 清理合併 → 選演算法
      → 訓練並驗證 → 測試 → 部署 → 決定執行頻率 → 決定更新頻率
三條軸：Human Supervision?（監督 / 非監督 / 強化）
        Learn Incrementally?（批次 / 增量）
        How they generalize?（基於實例 / 基於模型）
AI ⊃ Machine Learning ⊃ Deep Learning（大數據是原料、資料科學是方法）

========== 6. 監督式 vs 非監督式 ==========
監督式：{(x₁,y₁)…(xₙ,yₙ)} 有標籤 → Classification（SVM / NN / 決策樹 / k-NN）
                                               Regression（線性迴歸 / NN）
非監督式：{x₁…xₙ} 沒標籤 → Clustering；可以是目的本身，也可以是前處理

========== 7. 混淆矩陣（p25 的數字）==========
TP=126  FP=21  FN=7  TN=119（總 273）
Accuracy  = (126+119)/273 = 89.74%
Precision = 126/(126+21)  = 85.71%   ← 分母是「預測為正」
Recall    = 126/(126+7)   = 94.74%   ← 分母是「實際為正」
F1 = 2PR/(P+R) = 0.900      Specificity = 119/140 = 85.00%
門檻 ↓ → Recall ↑ / FP ↑；門檻 ↑ → Precision ↑ / FN ↑

========== 8. 迴歸（p26 的模型）==========
f(x) = 35 + 1.5x  →  x=54→116、62→128、68→137、74→146、80→155

========== 9. 分群 ==========
intracluster distances are MINIMIZED（同群要緊）
intercluster distances are MAXIMIZED（異群要遠）
k-means：挑 k 個中心 → 指派最近的點 → 重算中心 → 迭代；最小化 inertia
k 要人決定（elbow method）；對尺度與離群值敏感
```

---

## 附錄 F：互動式線上測驗（60 題）

> **60 題單選、滿分 60 分、建議 45 分鐘。**
> 測驗以**互動網頁**形式提供（點選即時計分、進度自動儲存）；本筆記**不重複收錄題目**。

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
| 第一輪 | 0–25 分鐘 | 快速作答有把握的題目，不確定先標記跳過 |
| 第二輪 | 25–40 分鐘 | 回頭處理標記的難題 |
| 第三輪 | 40–45 分鐘 | 檢查有沒有漏答 |

### F.3 評分參考

| 分數 | 程度 | 建議 |
|---|---|---|
| 54–60 | 優異 | 直接看附錄 E 一頁精華即可上場 |
| 45–53 | 良好 | 複習錯題所屬章節 |
| 36–44 | 及格邊緣 | 重讀主要章節 + 附錄 A |
| 0–35 | 需加強 | 整份筆記重讀一遍，再重做本卷 |

> 答錯的題目請對照下方〈附錄 G〉回到對應章節複習。

---

## 附錄 G：互動測驗答錯題目 → 複習章節對照

| 答錯題號 | 主題 | 建議複習章節 |
|---|---|---|
| 1–6 | 生物神經元、動作電位、神經元與權重的定義 | §2、§3 |
| 7–12 | 三層結構、前向／反向傳播 | §4 |
| 13–18 | ANN / DNN 定義、deep 的判斷、網路拓撲 | §5、§6 |
| 19–24 | 激勵函數的定義、位置與非線性 | §7 |
| 25–30 | TLU 的公式、輸出範圍與限制 | §8 |
| 31–35 | ReLU 的公式、梯度、dead neuron | §9 |
| 36–40 | Sigmoid 的公式、值域、梯度消失 | §10 |
| 41–45 | Softmax 的公式、總和為 1、Sigmoid vs Softmax | §11 |
| 46–48 | 問題類型 → 激勵函數的選擇 | §12 |
| 49–52 | 十個步驟、三條分類軸、監督式／非監督式 | §13–§18、§20 |
| 53–57 | 混淆矩陣與 Accuracy / Precision / Recall / F1 | §19.1 |
| 58–60 | 迴歸指標、分群的兩個距離、k-means | §19.3、§21、§22 |

---

*本篇為個人學習筆記整理，教材內容版權屬匯縱專業發展中心（IVDC）所有。*









