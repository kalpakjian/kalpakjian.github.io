---
title: 用 TPOT 預測無人機訂單成交率：91.8% 的準確率陷阱、特徵重要性與門檻調校
date: 2026-10-18 20:00:00
categories:
  - 學習資源
tags:
  - 人工智慧
  - AutoML
  - TPOT
  - 機器學習
  - 特徵重要性
  - 實作
index_img: /img/covers/redix-tpot-sales-prediction.png
banner_img: /img/covers/redix-tpot-sales-prediction.png
---

AutoML 工具很方便：丟進資料、等幾分鐘、它給你一條「最佳 Pipeline」。但我在 AutoML 課程的第三個實習裡，刻意挑了一份**真實業務形狀**的資料——無人機公司的銷售名單——結果發現：**模型交出來的東西看起來很漂亮，實際上完全不能用**。

這篇文章把那個過程完整記錄下來：一份 500 筆的歷史成交名單、15 筆待預測的潛在客戶，用 TPOT 1.1.0 在本機跑（不用 Colab），一路踩到三個坑：

1. **準確率陷阱**：91.8% 的訂單都會成交，所以「全部猜成交」就有 92% 準確率；
2. **特徵重要性**：TPOT 只給你 Pipeline，不告訴你「為什麼」，解釋性要自己補；
3. **門檻才是決策**：同一條管線，門檻 0.50 會全部猜成交，門檻 0.90 才抓得出漏單。

<!-- more -->

---

## 1. 情境：Redix 無人機的 500 筆歷史名單

Redix 是一家無人機公司，業務想知道「**哪些潛在客戶最後會成交**」。手上的資料長這樣：

| 檔案 | 筆數 | 內容 |
|---|---|---|
| `redix_drone_sales_historical.csv` | **500** | `Record_ID`、`Customer_Segment`、`Web_Pages_Visited`、`Downloaded_Specs`、`Pricing_Page_Time_Sec`、`Industry_Trend_Score`、`Deal_Size_HKD`、**`Target_Closed_Won`**（答案） |
| `redix_drone_sales_prediction.csv` | **15** | 欄位相同，但**沒有答案**——這就是我們要預測的對象 |

客群分三類：`B2G_School`（學校／標案）207 筆、`B2C_Hobbyist`（個人玩家）154 筆、`B2B_Corporate`（企業客戶）139 筆。

![Redix 無人機銷售資料：500 筆歷史名單與 15 筆待預測名單](/img/redix-tpot/ch01-accuracy-trap.jpg)

> 圖：本章插圖由本機 ComfyUI 的 Qwen-Image 2.1 生成（本站 house style，無文字）。

**第一個要記住的數字**：`Target_Closed_Won` 的平均值是 **0.918**——也就是說，這 500 筆裡有 **91.8% 最後都成交了**。這個數字會在下一節變成一個陷阱。

---

## 2. 第一個陷阱：準確率 92%，卻毫無價值

多數人拿到這種題目，第一反應是「用準確率（accuracy）評估」。我們先看看基準線：

| 做法 | 準確率 | 平衡準確率 | ROC-AUC |
|---|---|---|---|
| **A. 全部猜「成交」** | **0.920** | 0.500 | 0.500 |
| B. 邏輯迴歸（`class_weight="balanced"`） | 0.800 | 0.834 | **0.920** |

「全部猜成交」拿到 **92% 準確率**，但它一筆沒成交的都抓不出來——平衡準確率 0.500，等於亂猜。

> **關鍵觀念**：資料不平衡時，accuracy 會被多數類別綁架。這份資料該看的是 **ROC-AUC**（排序能力）與**平衡準確率**（兩類平均）。

這也是我在課程裡反覆強調的事：**選指標比選模型重要**。指標選錯，後面再怎麼調參都是在錯的方向上努力。

---

## 3. 讓 TPOT 自己搜尋管線（本機 6.5 秒跑完）

接著把特徵交給 TPOT（`search_space="linear"`），讓它自己決定「要不要標準化、要不要做特徵選擇、用哪個模型、參數多少」：

```python
from tpot import TPOTClassifier
from tpot_local import local_cluster          # 只綁 127.0.0.1 的安全 dask client

with local_cluster(n_workers=4) as (client, cluster):
    tpot = TPOTClassifier(
        search_space="linear",   # 1.x 的搜尋空間（舊版寫法為 config_dict）
        generations=2,           # 課堂版：繁衍 2 代
        population_size=10,      # 每代 10 個模型
        verbose=3, cv=3, random_state=42,
        n_jobs=4, client=client, scatter=False)
    tpot.fit(X_train.values, y_train.values)
```

**課堂版（2 代 × 10 族群）6.5 秒**就跑完，找到的管線是：

```text
RobustScaler → SelectPercentile(37%) → BaggingClassifier(9 棵樹, 特徵抽樣 28%)
```

測試集 **ROC-AUC 0.877**——比手寫的邏輯迴歸（0.920）還差。這很正常：**小預算的演化搜尋本來就只是在逛空間**。

把預算改成「**時間預算 2 分鐘**」（`--budget 2`，不設 `generations`）後：

| 做法 | 搜尋時間 | ROC-AUC | 平衡準確率（門檻 0.5） | 平衡準確率（門檻 0.9） |
|---|---|---|---|---|
| 基準線：邏輯迴歸（balanced） | < 1 秒 | 0.9198 | 0.8342 | — |
| TPOT 課堂版（2 代 × 10 族群） | **6.5 秒** | 0.8770 | 0.5000（全猜成交） | 0.8125 |
| TPOT 課後挑戰版（`--budget 2`） | 122.4 秒 | **0.9253** | 0.5000 | **0.8614** |

**2 分鐘版本的 ROC-AUC 0.9253 反超了手寫基準線**。這也回答了「AutoML 到底有沒有用」：**有，但要給它足夠的預算**——6.5 秒的結果只是「還沒開始認真搜尋」。

![TPOT 的演化搜尋：管線像樹枝一樣往上長，好的分支越來越亮](/img/redix-tpot/ch02-tpot-evolution.jpg)

---

## 4. 為什麼？特徵重要性要自己補

TPOT 給你一條 Pipeline，但**不會告訴你為什麼**。要解釋，我補了兩層：

**① 置換重要度（Permutation Importance）**——把某個欄位打亂，看 ROC-AUC 掉多少。這是**模型無關**的方法，任何 Pipeline 都能用：

| 特徵 | ROC-AUC 下降 | 影響方向（預測機率變化） |
|---|---|---|
| **Web_Pages_Visited（瀏覽頁數）** | **0.1994** | ↑ 越高越容易成交（+0.119） |
| Pricing_Page_Time_Sec（價格頁停留秒數） | 0.0760 | ↑ 越高越容易成交（+0.095） |
| Downloaded_Specs（下載規格書） | 0.0135 | ↑ 越高越容易成交（+0.103） |
| Industry_Trend_Score（產業趨勢分數） | 0.0000 | – 影響不明顯 |
| Deal_Size_HKD（成交金額） | 0.0000 | ↑（+0.021） |
| 客群（3 個 one-hot 欄位） | 0.0000 | – 影響不明顯 |

**② 對照：手寫邏輯迴歸的勝算比**（方向最好解釋，>1 提高成交機率、<1 降低）：

| 特徵 | 勝算比 | 商業解讀 |
|---|---|---|
| Web_Pages_Visited | **4.14** | 網站逛得越多，需求越明確 |
| Customer_Segment_B2B_Corporate | 3.09 | 企業客戶成交機率較高 |
| Pricing_Page_Time_Sec | 2.20 | 價格頁停留越久＝越接近決策 |
| Industry_Trend_Score | 2.12 | 景氣分數越高越願意採購 |
| Downloaded_Specs | 1.36 | 主動下載規格書＝高意願訊號 |
| Customer_Segment_B2G_School | 0.76 | 學校／標案略低 |
| Customer_Segment_B2C_Hobbyist | 0.47 | 個人玩家成交機率較低 |
| Deal_Size_HKD | **0.34** | **金額越大越不容易成交**（決策鏈長、變數多） |

![Redix 特徵重要性三聯圖：置換重要度、影響方向、邏輯迴歸勝算比](/img/redix-tpot/feature-importance.png)

**兩個值得注意的發現**

1. 兩種方法**都同意「瀏覽頁數」是最關鍵的特徵**（AUC 下降 0.199、勝算比 4.14）——互相印證，可信度高。
2. 但 **TPOT 那條 Bagging 管線把其他特徵的重要性「吃掉」了**：多數欄位顯示 0.0000，因為它內含 `SelectPercentile(37%)` 特徵篩選 ＋ Bagging 隨機抽特徵，其餘欄位在樹的投票裡幾乎沒有貢獻。**線性模型的勝算比反而更能講出商業方向**（例如「金額越大越不易成交」）。

> 這就是「**AutoML 給你效能，解釋性仍要自己補**」——也是白盒（可解釋管線）與黑盒（只看分數）在實務上的差別。

![特徵重要性：一根光柱明顯高於其他——瀏覽頁數就是那根最高的柱子](/img/redix-tpot/ch03-feature-importance.jpg)

---

## 5. 門檻才是商業決策（同一條管線，0.50 與 0.90 差很多）

模型輸出的是「成交機率」，但**幾分以上要當成「會成交」是商業決策，不是模型決策**。

先看同一個 2 分鐘版本管線、同一組機率、只用不同門檻：

| 門檻 | 準確率 | 平衡準確率 | 未成交（漏單）召回率 |
|---|---|---|---|
| 0.50（TPOT 預設） | 0.920 | **0.500** | 0（一筆都沒抓到） |
| 0.90（用訓練集挑） | 0.850 | **0.861** | 0.875（抓到 7/8） |

門檻 0.50 時模型**全部猜成交**；門檻 0.90 才真正抓出漏單。

**那 0.90 是怎麼挑的？** 用**訓練集**掃一遍，取平衡準確率最高的門檻（**絕不能用測試集挑**，那是資料洩漏）：

![門檻調校曲線：訓練集 vs 測試集的平衡準確率，以及未成交的召回率與精確率](/img/redix-tpot/threshold-curve.png)

- **左**：綠實線＝訓練集（用來挑門檻）、藍虛線＝測試集（只用來驗證）。門檻 0.50 時平衡準確率只有 0.50；升到 0.90 時訓練集達到 **0.768**，所以系統挑 0.90。
- **右**：門檻越高，**未成交召回率越高**（越能抓到漏單），但**精確率先升後降**（誤殺變多）——這就是「漏單成本 vs 誤殺成本」的取捨。

**15 筆待預測名單的結果**（門檻 0.90）：

![15 筆待成交名單：成交機率排序與決策門檻線](/img/redix-tpot/predictions-chart.png)

- 綠＝預測成交（≥ 門檻）、紅＝預測未成交（< 門檻）；
- 紅虛線＝決策門檻 0.90、灰點線＝TPOT 預設 0.50；
- **門檻 0.50 → 15 筆全部猜成交；門檻 0.90 → 抓出 5 筆未成交**（2009、2011、2003、2013、2004）；
- 預測成交 10 筆、未成交 5 筆，預測成交金額合計 **1,764,500 HKD**。

> 一句話：**模型給你「排序」，門檻給你「決策」**。門檻高低要依成本訂：漏掉一張大單很貴，多打幾通電話很便宜。

![門檻像一把尺上的游標，決定了哪些訊號被接住、哪些被放掉](/img/redix-tpot/ch04-threshold-tuning.jpg)

---

## 6. TPOT 1.1.0 沒有 `export()` 了：把管線轉回程式碼

舊教材寫 `tpot.export('tpot_best_pipeline.py')`——**這在 1.1.0 已經不存在**。TPOT 1.0.0（2025-02）把 TPOT2 併入並整包重寫，官方 release notes 寫得很清楚：*removed deprecated/experimental features*。

實際跑會直接爆掉：

```text
TypeError: TPOTEstimator.__init__() got an unexpected keyword argument 'verbosity'
AttributeError: 'TPOTClassifier' object has no attribute 'export'
```

所以我自己寫了一個小工具把 `fitted_pipeline_` 轉回程式碼（等效舊版 `export()`）：

```bash
python tpot_export_code.py --joblib redix_best.joblib --out redix_best_pipeline.py
```

產出的檔案（節錄）：

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectPercentile
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Binarizer, RobustScaler

# Average CV score on the training set was: 0.9253
exported_pipeline = Pipeline(steps=[...])

# 固定亂數種子，確保結果可重現
set_param_recursive(exported_pipeline.steps, "random_state", 42)
```

**往返測試（round-trip）**：把這段程式碼重新載入、重新 fit，對 15 筆的預測機率與原管線**完全相同**——所以匯出的程式碼是真的可用，不只是「看起來像」。

![匯出後的管線是一條透明玻璃管路，光從左流到右，每一步都看得見](/img/redix-tpot/ch05-white-box-pipeline.jpg)

---

## 7. 完整實測數據與產出檔案

**環境**（本機，不使用 Colab）：

| 項目 | 值 |
|---|---|
| Python | 3.12（conda 環境 `tpot111_defaults`） |
| TPOT | **1.1.0**（conda-forge 有 1.1.0 套件；本機用 pip 安裝在 conda 環境內） |
| 其他 | scikit-learn 1.9.1、numpy 2.5.4、pandas 3.0.6、xgboost 3.4.1、dask 2026.8.0 |
| GPU | RTX 4090 24GB（本實習其實**用不到 GPU**：TPOT 是「大量小模型」的搜尋，瓶頸在評估條數，不在單次訓練） |

**產出檔案**：

| 檔案 | 內容 |
|---|---|
| `redix_tpot_predictions.csv` | 15 筆預測（標籤＋成交機率） |
| `redix_feature_importance.csv` | 特徵重要性（AUC 下降、標準差、機率變化） |
| `redix_best_pipeline.py` | TPOT 最佳 Pipeline 轉出的程式碼 |
| `redix_best.joblib` | 可直接部署的模型檔 |
| `redix_feature_importance.png` | 特徵重要性三聯圖（本文用圖） |
| `redix_predictions_chart.png` | 15 筆預測與門檻線（本文用圖） |
| `redix_threshold_curve.png` | 門檻調校曲線（本文用圖） |

📄 **可下載**：[一頁 A4 講義（PDF）](/redix-tpot/handout.pdf) —— 把上面四張圖整合成一頁（A4 橫向），可直接列印發給學員或投影講解。

---

## 8. 想自己跑一遍？三個指令

```powershell
# 1) 建環境（conda 預設 channel 的 Python ＋ pip 裝 TPOT）
C:\Users\princ\miniconda3\Scripts\conda.exe create -n tpot111_defaults python=3.12 -y
C:\Users\princ\miniconda3\envs\tpot111_defaults\python.exe -m pip install --upgrade pip "setuptools<81"
C:\Users\princ\miniconda3\envs\tpot111_defaults\python.exe -m pip install tpot

# 2) 跑實習（課堂版 6.5 秒；加 --handout 會連圖表與 A4 講義一起產出）
C:\Users\princ\miniconda3\envs\tpot111_defaults\python.exe redix_tpot_local.py --handout

# 3) 把最佳管線匯出成可讀程式碼
C:\Users\princ\miniconda3\envs\tpot111_defaults\python.exe tpot_export_code.py --joblib redix_best.joblib --out redix_best_pipeline.py
```

> ⚠️ `"setuptools<81"` 不能省：setuptools 81 起移除 `pkg_resources`，而 TPOT 相依的 `stopit` 仍會 import 它。
> ⚠️ 寫成 `.py` 腳本時要加 `if __name__ == "__main__":`，否則 Windows 上的 dask 會報 `No valid workers found`。

---

## 9. 小結：三個可以帶走的觀念

1. **先選對指標，再談模型**。這份資料 91.8% 都會成交，accuracy 92% 卻一無是處——請看 **ROC-AUC** 與**平衡準確率**。
2. **AutoML 給你效能，解釋性要自己補**。TPOT 幫你搜出管線，但「為什麼是這些特徵」要用**置換重要度**＋（線性模型的）**勝算比**自己補上；兩種方法互相印證時，結論才可信。
3. **模型給排序，門檻給決策**。同一條管線，門檻 0.50 全部猜成交、門檻 0.90 抓出 5 筆漏單；而且門檻只能用**訓練集**挑——用測試集挑就是作弊。

最後補一句實務提醒：**AutoML 的「最佳」是有預算前提的**。同一個問題，6.5 秒的最佳管線 ROC-AUC 0.877（輸給手寫基準線），2 分鐘的最佳管線 0.9253（反超）。**你給它多少時間，決定了它能給你多少答案。**
