---
title: 手寫 Ridge vs TPOT AutoML：同一份房價資料，AutoML 花 12 分鐘換到什麼？
date: 2026-10-18 23:00:00
categories:
  - 學習資源
tags:
  - 人工智慧
  - AutoML
  - TPOT
  - 機器學習
  - 迴歸
  - 雜訊底線
  - 實作
  - 資料分析
  - 學習筆記
index_img: /img/covers/house-price-ridge-vs-tpot.png
banner_img: /img/covers/house-price-ridge-vs-tpot.png
---

上一篇（銀行行銷名單）裡，AutoML 是**贏**的那一方：TPOT 花 5 分鐘，把 ROC-AUC 從 0.8125 拉到 0.8683。這篇要講相反的故事——同一套方法、同一把尺，這次 **AutoML 花了 11.8 分鐘、試了 390 條管線，最後跟手寫的 Ridge 打平**。

房價資料是迴歸題（不是分類），所以這個對照還多了一件事可以做：**先量出資料本身的「雜訊底線」**。一旦知道天花板在哪，你就能判斷 AutoML 到底是在「找更好的模型」，還是在「同一塊高原上採樣」。

本文用 500 筆成交紀錄訓練、預測 100 間房，兩條路線都跑完，然後放在同一把尺上量：**RepeatedKFold 5×4 = 20 折、RMSE（USD）**。

<!-- more -->

---

## 1. 情境：500 筆成交紀錄，要估 100 間房的價格

| 檔案 | 筆數 | 內容 |
|---|---|---|
| `house_price_regression_500.csv` | 500 | 8 個欄位 ＋ **`house_price_usd`**（答案） |
| `house_price_predict_100.csv` | 100 | 欄位相同，要預測的對象（其中 `predicted_house_price_usd` 已預先填好，見第 4 節） |

8 個欄位：`bedrooms`、`bathrooms`、`area_sqft`、`year_built`、`neighborhood`（rural／suburban／urban）、`condition_score`（4–10）、`garage_spaces`（0–3）、`renovated`（yes／no）。

目標值：平均 **536,576 USD**、中位數 529,000、範圍 136,000–934,000。**所有價格都是 1,000 的倍數**（四捨五入過的整數），這個細節後面會用到。

---

## 2. 手寫路線第一步：先量天花板，不要先挑模型

大多數人拿到資料的第一件事是「跑幾個模型看看」。我先做的是反過來的事：**量這個題目最好能到哪**。

做法很簡單——用全部 8 個欄位做一次普通最小平方（OLS），看殘差有多大：

| 檢查 | 實測 |
|---|---|
| OLS 樣本內 R² | **0.972952** |
| 殘差標準差 σ | **25,263 USD** |
| 殘差最大絕對值 | 75,877 USD |

**這個 25,263 就是雜訊底線。** 它代表「即使模型完美學到背後的真實關係，在這種雜訊水準下，對新資料的 RMSE 也不可能明顯低於 25,263」。後面所有模型都要跟這個數字比，而不是跟 0 比。

特徵與目標的相關（數值欄）：

| 欄位 | 與房價的相關 |
|---|---|
| `area_sqft` | **0.9199** |
| `bedrooms` | 0.8858 |
| `bathrooms` | 0.7576 |
| `garage_spaces` | 0.7087 |
| `condition_score` | 0.3576 |
| `year_built` | 0.3444 |

`neighborhood` 與 `renovated` 的平均房價幾乎沒有差異（rural 527,639／suburban 548,777／urban 528,253；renovated yes 537,349／no 531,400）——**單看平均數會以為這兩欄沒用**，但迴歸把它們的邊際效果找了出來（見第 7 節的係數）。

![房價分析的六格診斷儀表板](/img/house-price-ridge-vs-tpot/eda-dashboard.png)

> 這張六格圖是手寫路線實際跑出來的產出：價格分布、out-of-fold 的實際 vs 預測、殘差結構、11 條候選管線的 CV RMSE、置換重要度、以及 100 筆預測的價格 vs 面積。

---

## 3. 手寫路線第二步：11 條候選管線，放在同一把尺上

固定協定：**RepeatedKFold（5 折 × 4 次 = 20 折）**，指標 **RMSE（USD）**。兩組特徵都試——「原始 8 欄」與「加了衍生特徵的 14 欄」（房齡、每房面積、面積×屋況、是否新房、是否大房…）。

| 特徵組 | 模型 | CV RMSE | 標準差 |
|---|---|---|---|
| 原始 | **Ridge** | **25,696** | 2,154 |
| 原始 | 線性迴歸（OLS） | 25,697 | 2,143 |
| 原始 | Lasso／ElasticNet | 25,708 | 2,126 |
| 衍生 | Ridge | 25,830 | 2,090 |
| 衍生 | 梯度提升 | 30,626 | 1,892 |
| 原始 | 梯度提升 | 31,042 | 2,203 |
| 衍生 | 直方圖梯度提升 | 32,766 | 2,306 |
| 原始 | 隨機森林 | 37,125 | 2,294 |
| 原始 | kNN（k=15） | 41,474 | 3,512 |
| 原始 | 決策樹 | 48,901 | 3,540 |
| — | 基準線（猜平均值） | 153,441 | 7,308 |

三個結論：

1. **線性模型完勝樹模型。** Ridge 25,696 vs 隨機森林 37,125——差距 45%。這不是「樹不夠強」，是這份資料的關係**本來就是線性的**。
2. **Ridge 微勝 OLS（差 1 USD，統計上等價）**：正則化在這裡只是把係數壓穩，沒有改變結論。
3. **我做的特徵工程反而變差**（25,830 vs 25,696）。加了 6 個衍生欄位後，多出來的自由度開始吃雜訊——**這是「先量天花板」的另一個好處：你會知道何時該停止加特徵**。

![11 條候選管線的交叉驗證 RMSE，以及雜訊底線](/img/house-price-ridge-vs-tpot/model-comparison.png)

> 紅虛線是第 2 節量出來的雜訊底線 **25,263**。Ridge 的 25,696 只比它高 **1.7%**——也就是說，**這條線以上的空間幾乎都被雜訊佔滿了**，模型再好也只能貼著這條線跑。

---

## 4. 手寫路線第三步：檢查那 100 筆的「答案欄位」

預測檔裡有一個已經填好的欄位 `predicted_house_price_usd`。手寫路線的第三步不是用它，而是先問：**這欄到底是什麼？**

把它拿去對自己的特徵做一次 OLS：

| 檢查 | 實測 |
|---|---|
| R² | **0.999995** |
| 殘差標準差 | **285 USD** |
| 殘差最大絕對值 | 552 USD |

R² 幾乎是 1、殘差只有 285——**這個欄位不是某個模型的預測，而是一條「沒有雜訊的價格公式」**（殘差 285 只是它被四捨五入到 1,000 的結果）。

這件事有兩個用途：

1. **訓練檔的目標值 = 同一條公式 ＋ 雜訊**（σ ≈ 25,263）。所以我們知道了資料的生成方式：線性公式 ＋ 雜訊 ＋ 四捨五入。
2. **它變成一把「額外的尺」**：既然它是無雜訊的真公式，就可以拿來量「哪個模型把公式學得更準」——這是 CV 分數看不出來的東西（第 8.2 節會用到）。

---

## 5. TPOT 路線：先把 API 對齊，再開跑

TPOT 1.1.0 是重寫版（TPOT2 併入），**參數名字跟 0.12.x 不一樣**，直接照舊教材打會在建構時就爆掉：

| 0.12.x 寫法 | 1.1.0 寫法 | 說明 |
|---|---|---|
| `config_dict="default"` | `search_space="linear"` | 1.1.0 內建模板：`linear`／`graph`／`graph_light`／`light`／`mdr` |
| `scoring="neg_mean_squared_error"` | `scorers=["neg_mean_squared_error"]` | 可多目標（清單 ＋ `scorers_weights`） |
| `verbosity=2` | `verbose=2` | 改名 |
| `client=` 傳給 `fit()` | `client=` 傳給**建構子** | `fit()` 只吃 `(X, y)` |
| `tpot.export()` | **已移除** | 得自己把 `fitted_pipeline_` 轉回程式碼 |

這次的設定：

```python
from tpot import TPOTRegressor
from distributed import Client          # 執行緒式 client：不 spawn 子行程，避開 Windows 的坑

client = Client(processes=False, n_workers=1, threads_per_worker=4)
tpot = TPOTRegressor(
    search_space="linear",
    scorers=["neg_mean_squared_error"], scorers_weights=[1],
    cv=5, generations=15, population_size=30,
    max_time_mins=10, max_eval_time_mins=2,
    n_jobs=1, verbose=2, client=client, random_state=42,
)
tpot.fit(X, y)      # 11 欄 one-hot、500 筆
```

實測：**11.8 分鐘、13 代、390 條管線**（每代 30 條 × 13 代 = 390，完全吻合）。

**為什麼會超過 10 分鐘？** TPOT 的預算**只在世代邊界檢查**：第 12 代在 9 分 28 秒結束、第 13 代又跑了 2 分 20 秒才停，所以最後是 11.8 分鐘。每代耗時從 42 秒一路爬到 80 秒——因為後期的候選越來越複雜。

**每條管線的評估成本**：390 條 × 5 折 = 1,950 次擬合 ≈ 0.36 秒/次。有趣的是**冠軍自己只要 0.15 秒/次擬合**——時間是花在它試過又丟掉的重候選（樹集成、MLP、含內層 5 折的堆疊）上。

---

## 6. TPOT 找到什麼：5 步的堆疊式集成

```text
StandardScaler
  → VarianceThreshold(threshold=0.055151661558)
  → FeatureUnion( 原始 11 欄 ∪ 三個 out-of-fold 估計器 )
        其中三個估計器分別是：
          LinearSVR(C=3234.995, epsilon=0.000306)
          MLPRegressor(hidden_layer_sizes=[41], alpha=0.000669, early_stopping=True)
          LinearSVR(C=9124.029, epsilon=0.000758)
        （每一個都自帶內層 KFold(5) 的 cross_val_predict → 真正的 stacking）
  → ARDRegression(alpha_1=1.716e-06, alpha_2=2.988e-06, threshold_lambda=35455)
```

這條管線做了三件手寫路線沒做的事：**特徵篩選**（VarianceThreshold）、**堆疊集成**（把兩個 LinearSVR 與一個神經網路的 out-of-fold 預測當新特徵）、以及**稀疏貝氏迴歸**（ARDRegression，會把沒用的係數自動壓到 0）。

![兩條路線的管線對照](/img/house-price-ridge-vs-tpot/two-pipelines.png)

> 一個細節值得記：**它花了 11.8 分鐘，只為了把 Ridge 的 25,696 變成 25,700**（後面第 7 節）。AutoML 的搜尋空間允許很複雜的結構，它也真的找到了一個很複雜的結構——但這份資料不需要。

---

## 7. 同一把尺：兩條路線的對照

| 指標 | 手寫 Ridge | TPOT AutoML |
|---|---|---|
| CV RMSE（20 折） | **25,696 ± 2,154** | 25,700 ± 2,139 |
| 10 折 out-of-fold R² | 0.9719 | 0.9719 |
| 10 折 OOF RMSE／MAE／MAPE | 25,716／20,874／4.33% | 25,717／20,870／4.33% |
| 管線步數 | 2 步 | 5 步（含堆疊） |
| 係數／參數 | 11 個 | 3 個基底學習器 ＋ 1 個 meta 學習器 |
| 搜尋時間 | **0 秒** | **11.8 分鐘（390 條管線）** |

**配對檢定**（同一組 20 折，逐折比較）：

| 檢定 | 統計量 | p 值 |
|---|---|---|
| 配對 t 檢定 | t = +0.401 | **0.6932** |
| Wilcoxon 符號秩檢定 | W = 84.0 | 0.4524 |

平均每折只差 **+4 USD**（95% 信賴區間 −17 ～ +26）——**統計上完全無法區分**。

對 100 筆待預測物件的預測：

| 比較 | 數值 |
|---|---|
| 兩條路線預測的相關係數 | **0.99999** |
| 平均差 | 452 USD（0.09%） |
| 最大差 | 1,363 USD |
| 四捨五入到 1,000 後完全相同的筆數 | **55 / 100** |

![兩條路線對 100 筆的預測一致度](/img/house-price-ridge-vs-tpot/ridge-vs-tpot.png)

> 這張圖是本文最重要的一張：**左圖的點幾乎貼在對角線上**。兩條路線（一條 0 秒、一條 11.8 分鐘）在 100 筆上給出幾乎相同的答案。

---

## 8. 三個發現

### 8.1 AutoML 沒有贏，但也沒輸——它證明了「不需要贏」

11.8 分鐘、390 條管線、5 步堆疊集成，換到的是**統計上等於 0 的改善**。這個結果不是 AutoML 不好，而是**這份資料的關係是線性的**：AutoML 的價值在「探索你没想到的結構」，而這裡沒有結構可探索。

換句話說：**AutoML 幫你確認了「不需要更複雜的模型」**。這個確認有價值（不然你可能會一直懷疑「是不是該試試 XGBoost？」），只是它的價格是 12 分鐘。

### 8.2 TPOT 唯一贏的地方：它把「公式」學得更準

用第 4 節那把額外的尺（無雜訊公式）來量：

| 模型 | 與無雜訊公式的平均絕對誤差 | 最大誤差 |
|---|---|---|
| 手寫 Ridge | 701 USD | 2,060 USD |
| **TPOT** | **350 USD** | **876 USD** |

TPOT 的誤差是 Ridge 的**一半**。原因是它用了堆疊 ＋ 稀疏貝氏迴歸（ARDRegression），把係數估計得更穩——**它在「估計真實公式」這件事上確實比較準**。

但注意：**這個優勢完全被雜訊吃掉了**。因為真實房價 = 公式 ＋ σ≈25,263 的雜訊，把公式估得更準 350 USD，在 25,263 的雜訊面前等於沒有差別。這是一個很典型的陷阱：**用「還原真函數」的角度看，AutoML 贏；用「預測真實房價」的角度看，兩者平手。你的目標是哪一個，決定了這個優勢值不值得。**

![誰更貼近背後的價格公式](/img/house-price-ridge-vs-tpot/given-recovery.png)

### 8.3 贏家詛咒：TPOT 的內部分數不能當準確率用

TPOT 自己回報的樣本內 R² 是 **0.972950**——但那是「390 條管線在同一組 5 折上取最小值」的結果，**必然偏樂觀**。我用獨立協定重評，得到的是 25,700（≈ R² 0.9719）。

| 分數 | 值 | 性質 |
|---|---|---|
| TPOT 內部 5 折（選冠軍用） | 偏樂觀 | 390 條取最小值 → 贏家詛咒 |
| 獨立 RepeatedKFold 20 折 | 25,700 | 誠實可比較 |
| 手寫 Ridge（同一協定） | 25,696 | 誠實可比較 |

**「AutoML 回報的分數」和「AutoML 的真實水準」是兩個不同的數字。** 要比較，一定要用同一組、且不是它自己拿來選冠軍的那組 fold。

---

## 9. 成本：12 分鐘買到什麼？以及「預算該給多久」

| 項目 | 手寫 Ridge | TPOT AutoML |
|---|---|---|
| 你的時間 | 約 30 分鐘（含 EDA、量底線、比較 11 條管線） | 約 2 分鐘（寫 20 行）＋ **11.8 分鐘等機器** |
| 機器時間 | **< 1 秒** | **709.5 秒** |
| 額外產出 | 係數（可解釋）、置換重要度、診斷圖 | 管線物件、390 條的搜尋紀錄 |
| 額外要自己補的 | — | 解釋性、殘差診斷、預測區間、穩健性檢查 |

**預算怎麼定才合理？** 這次我用 10 分鐘，理由是：

1. **先量雜訊底線**（第 2 節的 25,263）→ 知道「最好能到哪」，就不會盲目加預算。
2. **預算要能容納足夠的世代數**。這個資料每代成本 ≈ `population_size × 每次評估成本` = 30 × 1.8 秒 ≈ 55 秒，10 分鐘 ≈ **13 代**（實測吻合）。3 分鐘只有 3 代，演化還沒開始累積選擇效果；1 小時則只是在同一塊高原上多採樣 2,000 次。
3. **想「達標就停」的話**，TPOT 沒有「分數達到 X 就停」的參數——它只有 `generations`、`max_time_mins`、`max_eval_time_mins` 與 `early_stop`（**連續 N 代沒進步**才停，預設關閉）。要做「達標停」得自己用 `warm_start=True` 切段跑，而且**要用獨立的 CV 判斷是否達標**，不能用它自己的內部分數。

> 這次的實證：`early_stop=5` 沒有開，所以它把預算用完；如果開了，大概在第 1–2 代（就已經到 25,7xx）之後就會自己收工——**結果一樣，時間省一半以上**。

---

## 10. 這次順手踩到的三個坑（都修好了）

### 10.1 我自己的錯：程式碼貼錯位置，變成死碼

第一版腳本把「存檔區塊」貼進了 `thread_client()` 函式的 `return` **之後**——Python 不報錯，那段程式只是永遠不會執行。症狀是：搜尋跑完、預測 CSV 也寫出來了，但**模型檔和報告沒出現**，而且**沒有任何錯誤訊息**（exit code 還是 0）。

> 教訓：**「沒有錯誤」不等於「有執行」**。長時間執行的流程，要在最貴的步驟結束後**立刻存檔**（我後來改成 TPOT 一跑完就先存一份 checkpoint），而不是等到最後。

### 10.2 TPOT 1.1.0 的 API 改名（第 5 節的表）

`scoring`→`scorers`、`verbosity`→`verbose`、`config_dict`→`search_space`、`client` 要傳給建構子、`tpot.export()` 被移除。而且 `TPOTRegressor.__init__` 收到不認識的參數時，**錯誤會在 `fit()` 才爆**（`TypeError: TPOTEstimator.__init__() got an unexpected keyword argument 'scoring'`）——不是在建構的時候，這讓排查多花了一點時間。

### 10.3 自製轉碼工具的 bug：`KFold` 沒有被 import

TPOT 1.0 之後沒有 `export()`，所以用本站既有的 `tpot_export_code.py` 把 `fitted_pipeline_` 轉回可執行的 Python。轉出來的檔案一執行就 `NameError: name 'KFold' is not defined`——原因是：

```text
repr 裡出現：EstimatorTransformer(cross_val_predict_cv=KFold(...), ...)
                ↑ 但 KFold 不是「估計器」，_iter_estimators() 走訪不到它
                  → 產生 import 時就漏掉了
```

修法是在工具的 `_import_lines()` 旁邊加一張 `_EXTRA_SYMBOLS` 對照表（`KFold`、`StratifiedKFold`、`ShuffleSplit`… → `sklearn.model_selection`），掃描 repr 補上缺少的 import。

**修完一定要做往返測試**：重新匯出的 `house_price_tpot_pipeline.py` 拿去跑，100 筆預測與原管線**完全相同（最大差 0 USD）**。

```text
reload 模型 → 預測：max |reloaded - in-memory| = 0.00e+00 USD
執行匯出的 .py → 預測：100 / 100 筆完全相同
```

> 另外提醒：`house_price_tpot_model.joblib` **必須在裝有 TPOT 的環境載入**（它會 unpickle `tpot.builtin_modules` 的類別），用一般環境開會出現 `No module named 'pkg_resources'` 之類的錯誤。

---

## 11. 什麼時候該用哪條路？

| 情境 | 建議 | 理由 |
|---|---|---|
| 你要**解釋**每個欄位的效果、要跟主管報告係數 | 手寫線性／Ridge | 11 個係數就能講完；AutoML 的堆疊管線沒有這種直覺 |
| 你要**最快知道「這份資料的天花板」** | 手寫 OLS 先量殘差 σ | 30 秒就能知道有沒有戲，不用等 AutoML |
| 資料欄位很多（數十～數百）、你**不確定該用哪個模型家族** | AutoML | 這正是它省時間的地方（前一篇銀行名單就是這個情境） |
| 關係**可能非線性／有交互作用**，而你不知道怎麼造特徵 | AutoML | 它的搜尋空間包含特徵篩選、堆疊、非線性模型 |
| 資料關係**已經確定是線性**（或你已量出雜訊底線） | 手寫 | 這次的實證：AutoML 12 分鐘換到 +4 USD（p = 0.69） |
| 你要**上線**、要控制延遲與可維護性 | 手寫 | 2 步管線 vs 5 步堆疊（含內層 5 折 CV）的維運成本差很多 |

**一句話**：AutoML 的價值不是「一定比較準」，而是「**用機器時間換你的探索時間**」。當探索空間真的有東西可找（欄位多、關係複雜），這筆交易划算；當關係本來就簡單，你付的是機器的 12 分鐘，換到的是**「確認不需要更複雜」**這個資訊——值不值，取決於你原本會不會繼續懷疑。

---

## 12. 完整實測數據與產出檔案

**環境**：Python 3.11.16 ｜ TPOT 1.1.0 ｜ scikit-learn 1.9.1 ｜ numpy 2.4.6 ｜ pandas 3.0.6 ｜ dask-distributed 2026.8.0 ｜ Windows 本機（`C:\Users\princ\venvs\tpot111`，不用 Colab）

**關鍵數字一覽**

| 數字 | 值 |
|---|---|
| 訓練／預測筆數 | 500／100 |
| 雜訊底線（OLS 殘差 σ） | 25,263 USD |
| 手寫 Ridge CV RMSE | 25,696 ± 2,154 |
| TPOT CV RMSE | 25,700 ± 2,139 |
| 配對 t 檢定 p 值 | 0.6932 |
| TPOT 搜尋 | 11.8 分鐘／13 代／390 條管線 |
| TPOT 預測平均房價 | 568,454 USD（訓練平均 536,576） |
| 價格級距分布（100 筆） | budget 10／entry 24／mid 23／upper 26／premium 17 |

**產出檔案**（全部在 `C:\Users\princ\OneDrive\Documents`）

| 類型 | 內容 |
|---|---|
| CSV | `house_price_predictions.csv`（Ridge，100 筆 × 18 欄）、`house_price_tpot_predictions.csv`（TPOT，100 筆 × 19 欄，含兩條路線並列與差異） |
| TXT | `house_price_report.txt`（手寫路線完整報告）、`house_price_tpot_report.txt`（TPOT 執行報告）、`house_price_ridge_vs_tpot.txt`（對照報告） |
| PNG | [六格診斷儀表板](/img/house-price-ridge-vs-tpot/eda-dashboard.png)、[11 條管線 CV 對照](/img/house-price-ridge-vs-tpot/model-comparison.png)、[管線對照圖](/img/house-price-ridge-vs-tpot/two-pipelines.png)、[預測一致度](/img/house-price-ridge-vs-tpot/ridge-vs-tpot.png)、[公式還原度](/img/house-price-ridge-vs-tpot/given-recovery.png) |
| PY | `house_price_model.py`（手寫路線，可重跑）、`house_price_tpot.py`（TPOT 路線，可用環境變數調 `TPOT_MINUTES`／`TPOT_GENS`／`TPOT_POP`／`TPOT_SPACE`）、`house_price_tpot_pipeline.py`（匯出的可執行管線，往返測試 PASS） |
| JOBLIB | `house_price_model.joblib`、`house_price_tpot_model.joblib`（需 TPOT 環境載入） |

---

## 13. 小結：四個可以帶走的觀念

**1. 先量天花板，再挑模型。**
30 秒的 OLS 殘差 σ（25,263）就告訴你這個題目的極限。有了它，你才知道 25,696 是「已經到頂」而不是「還有很多空間」——**沒有這條線，你會以為 AutoML 的 25,700 是「還沒搜到更好的」。**

**2. AutoML 的「最佳」是有預算前提的最佳。**
390 條管線、13 代、11.8 分鐘，最後贏手寫 4 USD（p = 0.69）。它的搜尋空間允許複雜結構，也真的找到複雜結構（5 步堆疊集成），但**這份資料不需要**。AutoML 不是魔法，它是在你給的空間與預算裡搜尋。

**3. AutoML 回報的分數 ≠ AutoML 的真實水準。**
內部 5 折是「390 條取最小值」，必然偏樂觀。要比較，就用同一組、不是它用來選冠軍的 fold（本文用 RepeatedKFold 5×4）。

**4. 「還原真函數」與「預測真實值」是兩個不同的目標。**
TPOT 把背後的價格公式學得更準（誤差 350 vs 701 USD），但真實房價有 σ≈25,263 的雜訊，這個優勢完全被吃掉。**如果你的目標是預測（含雜訊的）真實價格，兩條路線平手；如果你要的是估計真實關係（例如估價模型的係數、政策模擬），AutoML 這一勝才有意義。**

**最後一個數字**：這份資料裡，**光用面積一個欄位就能解釋 84.6% 的變異**（`corr = 0.9199`，平方後 0.846）。11 條候選管線、390 條 TPOT 管線，最後都只是在同一條線附近晃動——**天花板不是模型決定的，是資料決定的。**

