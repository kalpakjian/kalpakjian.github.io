---
title: Orange AI 視覺化資料探勘 學習筆記：59 頁簡報完整複習 + 60 題 MC 模擬試卷
archive: true   # 已歸入「AutoML 應用證書課程」學習筆記，不列在首頁
date: 2026-10-19 01:30:00
categories:
  - 學習資源
tags:
  - 人工智慧
  - 機器學習
  - AutoML
  - Orange
  - 資料探勘
  - No-Code
  - 學習筆記
index_img: /img/covers/orange-ai-notes.png
banner_img: /img/covers/orange-ai-notes.png
---

我把一份 **59 頁的 Orange AI 簡報**完整重寫成可離線閱讀的學習筆記 —— 從「Widget 是什麼」開始，一路到 **20 個模型元件**、**五種核心監督模型**、**Constant／Stacking／Save-Load Model**，最後把 **Data 面板的 12 個元件**（匯入 4、檢視 4、處理輸出 4）全部收齊。

筆記已發佈成獨立頁面：

**👉 [Orange AI 視覺化資料探勘學習筆記](/orange-ai-notes/)**

<!-- more -->

---

## 這份簡報有一個「陷阱」：12 頁是純圖片

簡報總共 59 頁，但 **p1–p9 與 p17、p43 共 12 頁沒有文字層** —— 它們是 960×540 的**整頁點陣圖**。用任何 PDF 工具抽取，只會得到空白，或一個神祕的字串 `preencoded.png`。

這意味著：**Orange 官方文件截圖（Example Workflows、Widget Catalog、Datasets 說明、20 models 清單、SGD 設定面板）全部在圖裡**。筆記的做法是把這 12 頁**逐頁渲染成圖後判讀**，再寫成文字——所以「20 個模型元件的完整清單」和「SGD 面板的七個預設值」都完整保留了下來。

| PDF 頁 | 內容 | 文字層 |
|---|---|---|
| 1 | `orange DATA MINING 3.40` 封面 | ⚠️ 純圖 |
| 2–5 | Example Workflows（File→Data Table、互動式視覺化，中英各一） | ⚠️ 純圖 |
| 6–7 | Widget Catalog、Datasets 官方說明 | ⚠️ 純圖 |
| 8–9 | **20 models 清單、SGD 設定面板** | ⚠️ 純圖 |
| 10–16 | 五種核心監督模型 | ✅ |
| 17 | 準確度 vs 可解釋性 | ⚠️ 純圖 |
| 18–42 | 模型對比、九種演算法、四個核心元件、安裝 | ✅ |
| 43 | 用 Datasets 載入 Abalone 的截圖 | ⚠️ 純圖 |
| 44–59 | 資料工具箱 12 元件 | ✅ |

---

## 我把 20 個模型元件全部跑了一遍

這是這份筆記跟一般「工具介紹文」最不一樣的地方：**所有數字都是用 Orange 3.40.0 的 Python API 在本機實測的**，不是抄來的。

`Orange.data.Table("iris")`（150 筆 / 4 特徵 / 3 類別），5 折交叉驗證，`random_state=42`：

| 模型 | CA | AUC |
|---|---|---|
| kNN | **0.9667** | 0.9869 |
| Logistic Regression | **0.9667** | **0.9977** |
| Stacking | **0.9667** | 0.9970 |
| SVM / AdaBoost / Calibrated Learner | 0.9600 | 0.9700 / 0.9783 / 0.9968 |
| Gradient Boosting / Neural Network | 0.9533 | 0.9890 / 0.9965 |
| Tree / Random Forest | 0.9467 | 0.9613 / **0.9954** |
| CN2 Rule Induction | 0.8933 | 0.9551 |
| Naive Bayes | 0.8733 | 0.9813 |
| SGD | 0.8333 | 0.8750 |
| **Constant（基準線）** | **0.3333** | **0.5000** |

### 三個值得停下來看的發現

**① `Constant = 0.3333`，正好等於 50/150。**
iris 三類各 50 筆，Constant 永遠猜「最多數類別」，所以準確率就是 1/3；而它的 **AUC = 0.5000**，正是「完全沒有鑑別力」的定義值。原稿那句「**任何機器學習模型都應該先與 Constant 基準比較**」，數字長這樣。

**② 決策樹與隨機森林的 CA 完全相同（都是 0.9467），但 AUC 是 0.9613 對 0.9954。**
只看準確率，你會以為「隨機森林完全沒用」；一看機率品質，森林其實大幅勝出。**這是全篇最容易被忽略的一個考點。**

**③ Stacking 只是「追平」最強的單一成員，沒有超越。**
Logistic Regression 0.9667、SVM 0.9600、Random Forest 0.9533、**Stacking 0.9667**。原稿說 Stacking 能「大幅提升準確率」——那是在**資料量充足、成員差異大**的前提下；iris 只有 150 筆，元學習器沒有足夠資訊去學「該信誰」。

---

## 兩個「跑不動」的元件，比跑得動的更有教學價值

筆記裡最實用的一段，可能是這兩個**失敗案例**：

| 元件 | 失敗訊息 | 原因 |
|---|---|---|
| **Scoring Sheet** | `ValueError: Too many target variable values.` | **計分表只支援二元分類**，iris 有 3 類 |
| **Curve Fit** | `TypeError: CurveFitLearner.__init__() missing 1 required positional argument: 'expression'` | 它**必須**給你一個運算式（例如 `a * CRIM + b * LSTAT + c`） |

而且——把 Scoring Sheet 改用在**二元**資料（內建 `heart_disease`，303 筆）之後，它交出的是這種東西：

| 條件 | 分數 |
|---|---|
| major vessels colored = < 1 | **−5** |
| chest pain = asymptomatic | **+4** |
| thal = reversable defect | **+4** |
| ST by exercise = < 2 | **−4** |
| exerc ind ang = 1 | **+2** |
| （截距） | **+2** |

**20 個候選特徵裡只有 5 個拿到非零分數**，而且**全部是整數**——業務人員拿一張紙、一支筆就能複算。CA 0.8416，打敗 Constant 的 0.5413。

> 這也解釋了一個矛盾點：原稿說評分表的缺點是「需要手動設定權重，主觀性較強」——那是**業界傳統評分卡的做法**；而 Orange 的 `Scoring Sheet` 元件是**自動從資料學出整數配分**的。

---

## 原稿的文字層有 18 個錯字，其中一個是 Orange 官方自己的

簡報的文字層有不少抽取錯誤，照抄就會出錯。筆記做了完整對照表，例如：

| 原稿文字層 | 正確名稱 |
|---|---|
| `cdit Domain` | **Edit Domain** |
| `Cank` | **Rank** |
| `M ySBL` / `Postgre SBL` | **MySQL** / **PostgreSQL** |
| `Csabkimg` | **Stacking** |
| `CH APTEC 1` | **CHAPTER 1** |
| **`Stochastic Gradient Decent`** | **Descent** ← **這是 Orange 介面自己的錯字** |

最後一個最有趣：**Orange 官方的元件名稱真的拼錯了**（正確拼字是 Descent）。如果題目照著介面出，答案就是 `Decent`；如果考英文正確拼字，答案是 `Descent`。**兩個都要知道。**

---

## 18 張章節插圖

全站插圖都是用本機 **Qwen-Image 2.1**（ComfyUI）生成的，沿用本站統一的深藍→青綠電影感風格、**不含任何文字**（文字交給圖說），並以壓縮後的 JPEG base64 內嵌，所以整份筆記仍然是**單一 HTML 檔、零外部資源**。

其中幾張的設計意圖：

| 章節 | 插圖意象 |
|---|---|
| 平台總覽 | 一顆發光橘色核心，周圍環繞著由光纖連起的元件方塊 |
| 範例工作流 | 兩個發光節點之間只有一條筆直的光通道 |
| 互動式視覺化 | 一片光點中，一個發光的選取框罩住其中一區，光流向後方面板 |
| 20 個模型元件 | 二十個發光圖騰方塊整齊排列，中央一塊被暖光標亮 |
| Constant 基準 | 一條貫穿暗色圖表的水平光線，上面插著一面小旗 |
| Stacking | 下層三顆小晶體各自射出光束，匯聚成上層一顆大晶體 |
| Save／Load Model | 一顆發光方塊被封進水晶盒，另一側盒子打開釋出光流 |

---

## 離線也能用

筆記是**單一 HTML 檔、零外部資源**（CSS、語法高亮與 18 張插圖全部內嵌），下載後直接雙擊就能看。

也可以下載原始 Markdown：

**📄 [Orange_AI_Study_Notes.md](/orange-ai-notes/Orange_AI_Study_Notes.md)**

---

## 建議使用順序

1. 先讀 **§1–§3**（Widget／Channel／Workflow ＋ 兩張範例工作流），把 Orange 的「世界觀」建立起來
2. 跳到 **§4** 把 20 個模型元件的名字記熟（附錄 A.3 有速查表）
3. **§6–§10** 是模型知識的主體，配合 **§6.6 的本機實測表**一起看
4. **§11–§13** 是原稿的四個核心元件（Constant／Stacking／Save／Load），**§11.3 的基準線診斷表**務必看懂
5. 考前 10 分鐘只看 **附錄 E 一頁精華**
6. 上場前做 **附錄 F 的 60 題互動測驗**，答錯的照附錄 G 回章節複習

---

*本篇為個人學習筆記整理。*
