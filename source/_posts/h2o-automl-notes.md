---
title: H2O AutoML 實作 學習筆記：38 頁走完一條完全免費的 AutoML 生產線
archive: true   # 已歸入「AutoML 應用證書課程」學習筆記，不列在首頁
date: 2026-10-16 21:30:00
categories:
  - 學習資源
tags:
  - 人工智慧
  - AutoML
  - 機器學習
  - H2O
  - Flow
  - Python
  - 學習筆記
index_img: /img/covers/h2o-automl-notes.png
banner_img: /img/covers/h2o-automl-notes.png
---

我把一份 38 頁的 **H2O AutoML** 實作課程完整重寫成可離線閱讀的學習筆記 —— 從下載 H2O-3、用 Flow 匯入資料、Run AutoML 訓練、匯出模型，到用 Python 做**遞迴預測**，最後在 Excel 畫出**港股 2024–2027 走勢圖**。

筆記已發佈成獨立頁面：

**👉 [H2O AutoML 實作學習筆記](/h2o-automl-notes/)**

<!-- more -->

---

## 為什麼值得看：這是一條「真的跑得完」的生產線

前面的 AutoML 筆記談的是**雲端平台**（Azure ML Studio）與**程式化搜尋**（TPOT）。這一份補上第三條路線：**H2O-3 開源平台 + Flow 網頁介面** —— 完全免費、資料不離開本機，而且多了一段「訓練完之後怎麼用」的完整落地流程。

| 階段 | 主題 | 關鍵產出 |
|---|---|---|
| A | 下載 H2O-3 → 啟動伺服器 → 開啟 Flow | `h2o.jar`、`localhost:54321` |
| B | Import Files → Parse → Ticker 設為 Enum | `monthly_training_set.hex` |
| C | Run AutoML → Build Model → Leaderboard | 最佳模型（Stacked Ensemble） |
| D | Export Model → 撰寫 `stock_prediction.py` | `trend_2024_2027.csv` |
| E | Excel 樞紐分析圖 → 關閉伺服器 | 港股走勢圖 |

---

## 課程沒寫、但一定會卡住的五個地方

簡報是「一句指令 + 一張截圖」的形式，操作很直覺，但**出錯時不會告訴你為什麼**。筆記把每一處都補上原因：

1. **Java 版本**：H2O 只支援 **Java 8–17**。Java 23 會直接噴 `Only Java versions 8-17 are supported`，課堂的繞道參數 `-Dsys.ai.h2o.debug.allowJavaVersions=23` 只是**略過版本檢查**，不是真的支援。
2. **`Ticker` 一定要設成 Enum**：留著 Numeric 的話，模型會以為「3320 比 941 大 3 倍多」。
3. **Import ≠ Parse**：Import 只是把檔案搬進記憶體，**Parse 才是真正讀懂它**（切欄、判型別、產生 `.hex`）。
4. **`overwrite: false` 的陷阱**：同一個路徑匯出第二次會失敗。
5. **`h2o.jar` 的那個終端機不能關**：它正在跑 Flow 的後台伺服器，關掉＝伺服器消失。

---

## 最值得看的一段：遞迴預測與「12 個月週期」

程式把**這個月的預測值**當成**下個月的輸入**（`Close_Lag1` ← 上一列的 `predict_Close`），一路推到 2027 年。因為特徵只有 `Close_Lag1` 與 `Month`，遞迴幾輪之後模型會**收斂成固定的年度循環** —— 2025、2026、2027 年 1 月的預測值幾乎完全相同（`53.2405`）。

這正好是一個很好的教材級示範：**它證明模型只學到了季節性與均值回歸，而不是趨勢**。筆記裡把這個現象、以及「為什麼日期欄一定要忽略」都寫清楚了。

---

## 六張章節插圖

全站插圖都是用本機 **Qwen-Image 2.1**（ComfyUI）生成的，沿用本站統一的深藍→青綠電影感風格、**不含任何文字**（文字交給圖說），並以壓縮後的 JPEG base64 內嵌，所以整份筆記仍然是**單一 HTML 檔、零外部資源**。

其中幾張的設計意圖：

| 章節 | 插圖意象 |
|---|---|
| 總覽 | 五個站點串成一條發光的生產線 |
| 環境建置 | 雲端降下資料，落在一顆電路板上的水滴核心（H₂O） |
| 資料匯入 | 原始資料列穿過漏斗，重組成一個六角結晶塊（`.hex`） |
| Run AutoML | 大量模型沿著軌道賽跑，冠軍站上頒獎台戴上皇冠 |
| 匯出與預測 | 模型方塊被抬出瀏覽器視窗，接著進入一圈圈的遞迴鏈 |
| 視覺化 | 三條走勢線壓在十二格的光柵上 |

---

## 離線也能用

筆記是**單一 HTML 檔、零外部資源**（CSS、語法高亮與 6 張插圖全部內嵌），下載後直接雙擊就能看。

也可以下載原始 Markdown：

**📄 [H2O_AutoML_Study_Notes.md](/h2o-automl-notes/H2O_AutoML_Study_Notes.md)**

---

## 建議使用順序

1. 先照階段 A 把 H2O 跑起來（確認 `localhost:54321` 打得開）
2. 階段 B–C 跟著點，重點看 **Enum** 與 `max_runtime_secs: 300` 這兩處
3. 階段 D 把匯出的模型路徑填進 `model_path`，觀察 `Close_Lag1` 與上一列 `predict_Close` 的關係
4. 階段 E 畫完圖後，別忘了把伺服器關掉（`Admin ▾ → Shut Down`）

---

*本篇為個人學習筆記整理。*
