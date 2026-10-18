---
title: Azure ML AutoML 實作全紀錄：從建立算力到 REST 端點，bank 流失預測六步走完
date: 2026-10-18 22:00:00
categories:
  - 學習資源
tags:
  - 人工智慧
  - AutoML
  - 機器學習
  - Azure
  - 實作
  - 學習筆記
index_img: /img/covers/azure-automl-bank-churn-walkthrough.png
banner_img: /img/covers/azure-automl-bank-churn-walkthrough.png
---

AutoML 課程的單元三講 Azure ML Studio，把整條價值鏈收斂成一句話：**資料註冊 → 雲端算力訓練 → 自動選演算法 → 部署成 REST API**。但「知道有這四件事」和「真的把它跑完一次」是兩件不同的事——尤其在雲端，**每一個欄位都對應到一筆帳單**。

這篇把一次完整的實作走完，六個步驟從建立算力一路做到 Consume 分頁。所有數字都是畫面上實際顯示的值，不是範例值。

**這次實作的環境**

| 項目 | 值 |
|---|---|
| 工作區 | `Practice`（City University of Hong Kong - Student） |
| 訂閱 | Azure for Students |
| 地區 | `germanywestcentral` |
| 資料 | `bank_marketing_train.csv`（81.38 KiB） |
| 任務 | Classification，目標欄位 `y (String)` |
| 結果 | **VotingEnsemble，AUC weighted 0.87459** |

**端到端資料流**：`Data（training）→ Compute（AutoML 叢集）→ Automated ML（prediction 工作）→ Endpoints（practice-zmrf）`

## 流程總覽

| # | 步驟 | 畫面字幕 |
|---|---|---|
| 1 | 建立計算叢集 | 點擊"Compute"並點擊"+New"／選擇"Standard_DS11_v2" |
| 2 | 建立數據資產（上傳 CSV） | 點擊"Data"並點擊"+Create"／Type: Tabular／上傳訓練資料集 |
| 3 | 設定 AutoML 任務 | 點擊"Automated ML"並點擊"+New Automated ML Job"／選擇"Classification"和訓練資料集／Target column: y (String) |
| 4 | 設定限制與終止條件 | Experiment timeout: 30／點選Enable early termination／選擇"Computer cluster" |
| 5 | 啟動與監控訓練 | （此段無字幕）→ 點擊最佳模型 |
| 6 | 部署與取用 | 點擊"Deploy"並點擊"Real-time endpoint"／選擇"Standard_DS1_v2"／點擊"Endpoint"／Deployment完成後,點擊"Consume" |

AutoML 任務的精靈左側固定六步：`Training method → Basic settings → Task type & data → Task settings → Compute → Review`。

## Step 1｜建立計算叢集

![Azure ML Studio 的 Compute 頁面](/img/azure-automl-bank-churn-walkthrough/01_t0001_compute_page.png)

![選擇 Standard_DS11_v2](/img/azure-automl-bank-churn-walkthrough/02_t0005_ds11v2.png)

![Configure Settings：節點數與閒置縮放](/img/azure-automl-bank-churn-walkthrough/02b_t0010_configure_settings.png)

左側選單 **Compute** → **Compute clusters** 分頁 → **+ New**，然後在 **Virtual Machine** 步驟選規格，按 **Next** 進到 **Configure Settings** 設定節點數。

| 項目 | 實測值 |
|---|---|
| 地區 | `germanywestcentral` |
| 選定規格 | **Standard_DS11_v2**（2 cores、14 GB RAM、28 GB storage） |
| 類別／用途 | Memory optimized／"Development on Notebooks (or other IDE) and light weight testing" |
| 單價 | **$0.17/hr** |
| 最小節點 | **0** |
| 最大節點 | **1** |
| 閒置縮放 | **120 秒** |
| Enable SSH access | 關閉 |

同一個畫面上還列出其他可選規格，方便比價：

| 規格 | 類別 | 資源 | 單價 |
|---|---|---|---|
| Standard_DS11_v2 | Memory optimized | 2 cores／14 GB／28 GB | $0.17/hr |
| Standard_DS3_v2 | General purpose | 4 cores／14 GB／28 GB | $0.27/hr |
| Standard_E4ds_v? | Memory optimized | 4 cores／32 GB | $0.35/hr |

**最小節點為什麼要設 0**：叢集閒置時會縮到 0 個節點，只有真的在訓練時才計費。這裡設 **0/1** 而不是常見範例的 0/2——實測證明**單一節點就足以跑完這個練習**，多開只是多花錢。

## Step 2｜建立數據資產（上傳 CSV）

![Data 頁面與 + Create](/img/azure-automl-bank-churn-walkthrough/03_t0025_data_create.png)

![設定名稱與型別](/img/azure-automl-bank-churn-walkthrough/04_t0030_tabular.png)

![選擇檔案或資料夾](/img/azure-automl-bank-churn-walkthrough/05_t0043_upload_dataset.png)

左側選單 **Data** → **+ Create**，在 **Data type** 填名稱、型別選 **Tabular**，再依序走完 `Data source → Destination storage type → File or folder selection → Settings → Schema → Review`。

| 項目 | 實測值 |
|---|---|
| 資料資產名稱 | **`training`** |
| 資產型別 | **Table (mltable)**（Dataset type：Tabular） |
| 實際檔名 | **`bank_marketing_train.csv`** |
| 檔案數／總大小 | 1 個／**81.38 KiB** |
| 資料存放區 | `workspaceblobstore` |
| 相對路徑 | `UI/2026-07-31_015418_UTC/bank_marketing_train.csv` |
| 建立時間 | 2026-07-31 09:54 AM |

> 💡 這個步驟進行到一半時，畫面右上跳出 **`Compute "AutoML" provisioning succeeded`**——代表 Step 1 建立的叢集才剛佈建完成。**最小節點設 0 並不等於不用等**，第一次啟用叢集仍要花時間。

## Step 3｜設定 AutoML 任務

![Automated ML 與剛建好的資料資產](/img/azure-automl-bank-churn-walkthrough/06_t0064_automl_new.png)

![選擇任務類型與訓練資料](/img/azure-automl-bank-churn-walkthrough/07_t0077_classification.png)

![目標欄位 y (String)](/img/azure-automl-bank-churn-walkthrough/08_t0082_target_y.png)

左側選單 **Automated ML** → **+ New Automated ML Job**。**Training method** 選 **Classification**、**Basic settings** 填工作與實驗名稱，然後在 **Task type & data** 選定資料，最後在 **Task settings** 指定目標欄位。

| 項目 | 實測值 |
|---|---|
| 任務類型 | **Classification** |
| 訓練資料 | `training`（Table） |
| 目標欄位 | **`y (String)`** |
| 主要指標 | **AUC weighted** |
| 特徵化 | Auto |
| 實驗名稱 | **`bank`** |
| 最終工作名稱 | **`prediction`** |
| Validation type | Automatic |
| Test data | None |

**目標欄位是字串**：畫面上顯示的是 `y (String)`——分類任務的標籤**不必先轉成 0/1**，平台會自己處理。

> ⚠️ **命名踩雷**：Basic settings 的 Job name 欄位當時填了 `predci`，下方立刻出現紅字 **「Job name must be unique across the workspace.」**。工作名稱在同一個工作區內**不能重複**，最終這個工作叫 `prediction`。

## Step 4｜設定限制與終止條件

![Limits：Experiment timeout 與 Enable early termination](/img/azure-automl-bank-churn-walkthrough/09_t0088_limits_timeout.png)

![Compute：選擇 Compute cluster](/img/azure-automl-bank-churn-walkthrough/10_t0092_compute_cluster.png)

在 **Task settings** 頁展開 **Limits**，設定 **Experiment timeout (minutes) = `30`** 並勾選 **Enable early termination**；其餘限制欄位（total trials、max concurrent trials、max nodes、metric score threshold）全部留白，交給平台自動決定。接著在 **Compute** 頁把計算類型設為 **Compute cluster**。

| 項目 | 實測值 |
|---|---|
| Experiment timeout | **30 分鐘** |
| Enable early termination | **已勾選** ✅ |
| Max nodes／total trials／concurrent trials／metric score threshold | 未填（留白） |
| 計算類型 | **Compute cluster** |
| VM 規格 | `Standard_DS3_v2`（4 cores／14 GB RAM／28 GB storage／$0.27/hr） |
| 執行個體數 | **1** |

**Early termination 在省什麼**：AutoML 會同時嘗試多組演算法與前處理組合，若某一組的表現明顯落後當前最佳者就提前中止，把算力留給有希望的組合。搭配 `Experiment timeout = 30 分鐘` 當作整場實驗的硬上限。

## Step 5｜啟動與監控訓練

![工作剛建立，狀態 Not started](/img/azure-automl-bank-churn-walkthrough/11_t0100_job_notstarted.png)

![訓練執行中，Running featurization](/img/azure-automl-bank-churn-walkthrough/12_t0108_job_running.png)

![完成並檢視最佳模型](/img/azure-automl-bank-churn-walkthrough/13_t0118_best_model.png)

精靈最後一步 **Review** 送出後，工作狀態會依序變化：**Not started** → **Running**（畫面顯示 `Running featurization`）→ **Completed**。完成後進 **Models + child jobs** 點開最佳模型。

| 項目 | 實測值 |
|---|---|
| 工作名稱 | **`prediction`** |
| 實驗 | **`bank`** |
| 建立／開始時間 | 2026-07-31 09:56 AM |
| **Duration** | **38 分 15.16 秒** |
| **Compute duration** | **38 分 15.16 秒** |
| 計算目標 | `AutoML` |
| 輸入 | `training_data`／`training:1` |
| 輸出 | `best_model`／`azureml_prediction_34_output_mlflow_log_model_236457051:1` |
| 最佳模型 | **`yellow_map_kk23yvm3`** |
| 演算法 | **VotingEnsemble** |
| **AUC weighted** | **0.87459** |
| Sampling | **100.00%** |
| 註冊模型 | `prediction34:1` |

完成後畫面上掛著一則警告：

> `Warning: Experiment timeout reached, hence experiment stopped. Current experiment timeout: 0 hour(s) 30 minute(s)`

**這裡有一個值得記下來的數字落差**：timeout 設 **30 分鐘**，但工作的 Duration 是 **38 分 15.16 秒**才結束。**不要把 timeout 當成「保證總時長」**——它比較像「時間到就喊停」的煞車，實際結束時間會更晚，排程時要留餘裕。

## Step 6｜部署與取用

![Model 頁籤與 Deploy 選單](/img/azure-automl-bank-churn-walkthrough/14_t0120_deploy_realtime.png)

![部署設定面板](/img/azure-automl-bank-churn-walkthrough/15_t0124_vm_ds1v2.png)

![送出部署](/img/azure-automl-bank-churn-walkthrough/16_t0130_completed_auc.png)

![Endpoints 清單](/img/azure-automl-bank-churn-walkthrough/17_t0136_endpoint.png)

![Consume 分頁的取用資訊](/img/azure-automl-bank-churn-walkthrough/18_t0143_consume.png)

在最佳模型的 **Model** 頁籤點 **Deploy ▾** → **Real-time endpoint**，填好部署面板後按 **Deploy**。之後到左側 **Endpoints** → **Real-time endpoints**，等端點出現再點進去。

| 項目 | 實測值 |
|---|---|
| 端點名稱 | **`practice-zmrf`** |
| 部署名稱 | **`prediction34-1`** |
| 部署 VM | **`Standard_D2as_v4`**（2 Cores／8 GB RAM／16 GB Disk／$0.10/hr） |
| Instance count | 面板初值 **3** → 後段畫面顯示 **1** |
| REST 端點 | `https://practice-zmrf.germanywestcentral.inference.ml.azure.com/score` |
| 驗證方式 | Primary key／Secondary key（可 Regenerate） |
| 取用範例 | **JavaScript／Python／C#／JSON** 四種 |
| 端點分頁 | Real-time endpoints／Batch endpoints／Azure OpenAI／Serverless endpoints |

**部署時跳出的配額警告**：

> `Not enough quota available for Standard_D2as_v4. Current usage/limit: 0/4. Additional requested: 8 (20% more quota than expected may be needed for redundancy purposes on some SKUs)`

學生訂閱的配額是有限的，**選 VM 之前最好先確認配額**，否則會卡在部署階段。

> ⚠️ **一處畫面與字幕不一致，我照實記錄**：這一步的字幕寫 **選擇"Standard_DS1_v2"**，但同一時刻部署面板上的 Virtual machine 欄位顯示的是 **`Standard_D2as_v4`**（並附上述配額警告），最後部署用的也是 `Standard_D2as_v4`。我無法從畫面判斷中途是否換過規格，所以兩種資訊都保留。

**Consume 分頁才是交付的終點**：部署完成不等於結束。`practice-zmrf` 的 **Consume** 頁籤給了 REST 網址、Primary／Secondary key，以及 JavaScript／Python／C#／JSON 四種語言的呼叫範例——這才是「把模型變成別人可以呼叫的服務」的那一步。

## 實測值 vs 課程範例值

把這次跑出來的數字，和 [AutoML 學習筆記](/automl-notes/) 裡單元三的六步流程對照：

| 項目 | 課程範例值 | 本次實測 |
|---|---|---|
| 最大節點 | 2 | **1** |
| 計算叢集 VM | Standard_DS11_v2 | **Standard_DS11_v2**（一致） |
| AutoML 任務 VM | 未載明 | **Standard_DS3_v2**、instances 1 |
| 實驗名稱 | `bank-churn-prediction` | **`bank`** |
| 工作名稱 | 未載明 | **`prediction`** |
| 資料資產名稱 | `Bank_Marketing_Data` | **`training`** |
| 實際檔名 | 未載明 | **`bank_marketing_train.csv`** |
| Early termination | 未提及 | **已勾選**＋timeout 30 分 |
| 訓練耗時 | 約 15–30 分鐘 | **38 分 15.16 秒**（timeout 觸發停止） |
| 最佳模型／分數 | 只說「看 AUC_weighted」 | **VotingEnsemble／AUC 0.87459／Sampling 100%** |
| 端點名稱 | `bank-churn-api` | **`practice-zmrf`** |
| 部署 VM | 未載明 | **`Standard_D2as_v4`** |
| 部署尾段 | 到「取 REST 網址與金鑰」 | 多了 **Consume 分頁**（四種語言範例） |

**六步骨架完全吻合**；差別在於**每一步的具體設定值**，以及兩個課程範例沒有展開的環節：**Early termination** 與 **Consume 分頁**。另外耗時一項要特別注意——課程估 15–30 分鐘，這次實際跑了 38 分。

## 六個容易踩到的點

1. **timeout 不是「保證總時長」**——設 30 分鐘，實際 38 分 15.16 秒才結束。
2. **最小節點設 0 不等於不用等**——叢集首次啟用仍要佈建時間。
3. **學生訂閱有配額上限**——部署時就可能因為配額不足而卡住，選 VM 前先確認。
4. **目標欄位可以是字串**——`y (String)` 直接用，不必先轉 0/1。
5. **工作名稱必須全域唯一**——同一工作區內撞名會直接跳驗證錯誤。
6. **端點清單有延遲**——剛部署完進 Endpoints 可能還是空的，稍等才會出現。

## 這份紀錄是怎麼來的

這次的素材是一段 **2 分 26 秒的螢幕錄影**，但有一個特殊狀況：**影片沒有音軌**（AAC 2 kb/s、`-91 dB` 數位靜音），所以不能用語音辨識產生字幕。畫面上那些指示文字是**燒錄在畫面裡的繁體中文**，於是我改用 OCR 取字幕：

1. 以 ffmpeg 抽出畫格 → PP-OCRv4 偵測文字框
2. 用**字高**當篩選條件（燒錄字幕約 42 px、介面文字 ≤26 px），把字幕從密密麻麻的入口網站文字裡挑出來
3. OCR 對筆畫複雜的字（例如 `擊`、`並`）會誤判，所以**逐條目視核對後人工訂正**
4. 再用較低的門檻重掃全部畫格並逐一檢查，確認**沒有漏掉任何字幕**

**限制**：文章裡的敘述是依「畫面 + 字幕」重建的操作脈絡，**不是原始旁白**（影片沒有旁白）；步驟順序是從畫面推斷的；截圖時間戳精度約 ±0.25 秒。

## 相關筆記

- [AutoML 學習筆記（四單元完整版）](/automl-notes/)——單元三就是這條 Azure ML 價值鏈
- [H2O AutoML 實作](/h2o-automl-notes/)——另一條開源路線的端到端實作
- [用 TPOT 預測無人機訂單成交率](/2026/10/18/redix-tpot-sales-prediction/)——本機版的自動化建模，對照雲端版的差異
