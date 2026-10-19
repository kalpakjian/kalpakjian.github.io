---
title: AutoML 專區｜筆記總入口
date: 2026-10-19 22:00:00
---

本站所有 **AutoML** 相關內容集中在這一頁：兩套完整課程、單篇實作對照，以及工具與基礎筆記。
**選單只留這一個入口**；各課程的完整總覽頁仍保留在原網址。

---

## 1 · 兩套完整課程

### ① AutoML 十課（自編・原理為主體）★ 建議從這裡開始

![AutoML 十課 學習筆記](/img/covers/automl-principles-notes.png)

- **10 課 × 約 3 小時**，主體講**原理**，實作只用來**證明原理**；雲端只講概念、**完全沒有介面操作指南**
- **單檔離線 HTML**：十課 ＋ 附錄同一頁，左側目錄跳轉、可列印
- **10 張資料驅動的原理圖**（純 SVG，共約 76 KB，可離線）
- 附錄獨立並標明保鮮期：環境建置、**問題記錄簿（15 筆實測踩坑）**、版本變更對照、指令速查、實測數據表
- 每一課的示範都在本機實跑過，關鍵數字直接寫進內文

**👉 [看筆記](/automl-principles-notes/)** ｜ [圖表總覽](/automl-principles-notes/figures.html) ｜ [速記卡](/automl-principles-notes/cards.html) ｜ [課程總覽](/automl-principles-course/)

### ② AutoML 應用證書課程（ERB・操作導向）

- 來源：100 頁主課程 ＋ 33 頁補充課程；四個單元、20 個實習個案
- 三條工具路線：無代碼（Teachable Machine／TensorFlow Playground）、企業雲端（Azure ML Studio）、開源程式化（Colab ＋ TPOT）
- 含負責任 AI 六大原則、數據漂移監控、模型解釋性儀表板

**👉 [課程總覽](/automl-course/)** ｜ [四單元完整複習 ＋ 60 題 MC](/2026/10/16/automl-notes/) ｜ [單元二補充筆記](/2026/10/17/automl-unit2-extra-notes/)

> **兩套怎麼選**：想**動手做完整流程**（含雲端介面）→ 選 ②；想**懂原理、可長期沿用**（不受版本改版影響）→ 選 ①。

---

## 2 · 單篇實作與對照

| 主題 | 一句話 | 連結 |
|---|---|---|
| 手寫模型 vs TPOT（銀行行銷） | 同一份資料，差別到底在哪 | [閱讀](/2026/10/18/bank-marketing-tpot-vs-handmade/) |
| 手寫 Ridge vs TPOT（房價） | AutoML 花 12 分鐘換到什麼 | [閱讀](/2026/10/18/house-price-ridge-vs-tpot/) |
| TPOT 預測無人機成交率 | 91.8% 的準確率陷阱、特徵重要性與門檻調校 | [閱讀](/2026/10/18/redix-tpot-sales-prediction/) |
| Azure ML AutoML 全紀錄 | 從建立算力到 REST 端點，六步走完 | [閱讀](/2026/10/18/azure-automl-bank-churn-walkthrough/) |
| H2O AutoML 實作 | 38 頁走完一條完全免費的 AutoML 生產線 | [閱讀](/2026/10/16/h2o-automl-notes/) |

---

## 3 · 工具、指標與基礎

| 主題 | 內容 | 連結 |
|---|---|---|
| RMSE 與迴歸模型評估 | 修正兩個技術錯誤，並補上 30 題 MC | [閱讀](/2026/10/19/rmse-notes/) |
| 什麼是 TPOT | 基因演算法、Colab 實作與 60 題模擬試卷 | [閱讀](/2026/10/19/tpot-notes/) |
| 評估指標與 K-Means 聚類 | 從混淆矩陣到群內誤差最小化 | [閱讀](/2026/10/17/automl-unit2-extra-notes/) |
| 線性迴歸入門 | 從四個角色到最小平方法 | [閱讀](/2026/10/17/linear-regression-notes/) |
| 25 個機器學習模型速查 | 隨機森林／XGBoost／LightGBM… | [閱讀](/2026/10/16/ml-models-notes/) |
| 泛化能力（延伸課節） | 過擬合與正則化 | [閱讀](/2026/10/16/generalization-notes/) |
| Orange AI 視覺化資料探勘 | 59 頁簡報完整複習 ＋ 60 題 MC | [閱讀](/2026/10/19/orange-ai-notes/) |

---

## 4 · 建議閱讀路徑

| 你的目標 | 建議順序 |
|---|---|
| **完全新手** | [線性迴歸入門](/2026/10/17/linear-regression-notes/) → [25 個模型速查](/2026/10/16/ml-models-notes/) → [AutoML 十課](/automl-principles-notes/) 第 1～4 課 |
| **要考證書／複習** | [應用證書課程總覽](/automl-course/) → [四單元完整複習 ＋ 60 題 MC](/2026/10/16/automl-notes/) → [單元二補充](/2026/10/17/automl-unit2-extra-notes/) → [泛化能力](/2026/10/16/generalization-notes/) |
| **要動手實作** | [AutoML 十課](/automl-principles-notes/) 第 4～7 課（含洩漏檢查與搜尋預算）→ [什麼是 TPOT](/2026/10/19/tpot-notes/) → [手寫 vs TPOT 對照](/2026/10/18/bank-marketing-tpot-vs-handmade/) → [Redix 成交率實戰](/2026/10/18/redix-tpot-sales-prediction/) |
| **要上雲端** | [Azure ML AutoML 全紀錄](/2026/10/18/azure-automl-bank-churn-walkthrough/) → [AutoML 十課](/automl-principles-notes/) 第 8 課（雲端取捨與成本） |
| **想換工具** | [H2O AutoML 實作](/2026/10/16/h2o-automl-notes/) ｜ [Orange AI](/2026/10/19/orange-ai-notes/) → [AutoML 十課](/automl-principles-notes/) 第 7 課（引擎比較原理） |

---

## 5 · 一句話導覽

- **指標算錯只會誤導自己；資料洩漏會讓整個專案白做。** → [十課第 2～4 課](/automl-principles-notes/#L04)
- **CV 分數是拿來「選」的，不是拿來「信」的。** → [十課第 5 課](/automl-principles-notes/#L05)
- **搜尋工具是過程，管線才是產品。** → [十課第 6 課](/automl-principles-notes/#L06)
- **雲端買的是「可治理的算力」，不是更好的模型。** → [十課第 8 課](/automl-principles-notes/#L08)
