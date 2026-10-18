---
title: AutoML 應用證書課程 學習筆記總覽
date: 2026-10-16 21:30:00
---

<div style="border:2px solid #c0392b;background:#fff8f7;border-radius:10px;padding:14px 18px;margin:0 0 26px;">
  <p style="margin:0 0 6px;font-weight:700;color:#c0392b;font-size:1.05em;">📌 置頂：AutoML 速記卡（20 張・手機／平板版・依考試重要性排序）</p>
  <p style="margin:0 0 10px;">§1–§13 每章一張，加上附錄 A–F 與總複習卡；<strong>已依考試重要性排序</strong>（必考核心 → 高頻 → 基礎 → 實用），每張卡都有<strong>編號圓標</strong>與<strong>單元色帶</strong>（單元一～四、總結、附錄、總複習共 7 色），並附目錄可跳卡。</p>
  <p style="margin:0;">
    <a href="/automl-notes/cards.html" style="display:inline-block;padding:6px 14px;background:#c0392b;color:#fff;border-radius:6px;text-decoration:none;font-weight:700;">→ 速記卡（手機／平板版）</a>
    <a href="/automl-notes/summary.html" style="display:inline-block;padding:6px 14px;margin:6px 0 0 8px;border:1px solid #c0392b;color:#c0392b;border-radius:6px;text-decoration:none;font-weight:700;">精簡版（一頁式）</a>
    <a href="/automl-notes/cards-print.html" style="display:inline-block;padding:6px 14px;margin:6px 0 0 8px;border:1px solid #c0392b;color:#c0392b;border-radius:6px;text-decoration:none;font-weight:700;">列印版（每頁 3 張）</a>
  </p>
</div>

## 1 · AutoML 應用證書（單元一至單元四）

![AutoML 應用證書 學習筆記](/img/covers/automl-notes.png)

- **涵蓋**：四個單元、**100 頁**、**20 個實習個案**——三條主線一路展開：
  - **概念線**：傳統 ML 三大痛點（流程繁瑣／耗時費力／高度依賴專家）→ AutoML 三大突破（全自動化／高效能／低門檻），以及兩個關鍵自動化動作（**Auto Imputation** 填缺失值、**Auto Encoding** 轉類別特徵）
  - **倫理線**：微軟**負責任 AI 六大原則**（公 · 可 · 隱 · 包 · 透 · 問）→ 銀行自動審批系統的完整風險評估工作坊（敏感特徵標記、定期檢測門檻 **5%**、人工複核邊界值 **600–650 分**、Human-in-the-loop）
  - **技術線**：分類 vs 迴歸的判斷口訣 → 三個評估指標的陷阱（**Accuracy 在不平衡資料會騙人、AUC 的 0.5 等於瞎猜、RMSE 對離群值極敏感**）→ 三個實作平台（Teachable Machine → Azure ML Studio → Colab + TPOT）
- **特別之處**：課程有 **60 頁是 SmartArt 圖表**，一般工具讀取只會得到「一個圖形、零段文字」。筆記直接解析圖表底層資料，把每一頁的三個操作步驟完整還原成可搜尋的條列文字
- 另有 **13 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/automl-notes/)** ｜ [互動測驗 60 題](/automl-notes/mc-quiz.html) ｜ [速記卡 20 張](/automl-notes/cards.html)

---

## 2 · 泛化能力（Generalization Capability）

![泛化能力 學習筆記](/img/covers/generalization-notes.png)

- **定位**：AutoML 課程的**延伸課節**，教材為獨立一份 **10 頁**簡報（⚠️ **p1 是課節封面頁，正文自 p2 起算**）
- **核心命題**：泛化能力 = 模型對**未見過的新數據**的適應與預測能力；**訓練集表現好 ≠ 真正聰明**
- **三條主線**：
  - **診斷線**：過擬合（訓練極好／測試很差）vs. 欠擬合（兩邊都差）——**成因相反、解法也相反**
  - **量測線**：訓練／驗證／測試三集分工（**測試集只能用一次**）＋ **K 折交叉驗證**（常用 K=5、10）
  - **處方線**：**四大提升策略**——① 擴充訓練數據 → ② 正則化技術 → ③ 架構與早停控制 → ④ 集成學習
- **特別之處**：每個結論都附**本機實測數字**（Python 3.11.15 / scikit-learn 1.9.1）——
  - 複雜度光譜的最佳點是 degree=2（測試 RMSE **2.005**），degree=15 過擬合飆到 **5.131**
  - 資料量由 10 → 160 筆，驗證 RMSE 從 **251,532** 收斂到 **2.566**（訓練誤差反而上升）
  - 早停少跑 45% 迭代，測試準確率反而由 0.8392 升到 **0.8951**
  - 隨機森林 **0.9860** 勝過單一決策樹 0.9510
- **兩個「過頭」陷阱**（高頻考點）：資料增強 ±2 px（0.9428）與正則化 `alpha=10000` **都比不做更差**
- 另有 **9 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/generalization-notes/)** ｜ [互動測驗 60 題](/generalization-notes/mc-quiz.html)

---

## 3 · 機器學習模型速查（25 個模型）

![機器學習模型速查 學習筆記](/img/covers/ml-models-notes.png)

- **定位**：本課程的**模型速查卡**——教材為獨立一份 **25 頁**簡報（⚠️ **沒有封面頁**，25 頁全部是正文，所以 §1 = PDF 第 1 頁）
- **形式**：每一頁就是一張**模型卡**，固定五格——🧩 原理 → ✨ 優點 → ⚠️ 缺點 → 🎯 應用 → 核心公式
- **25 個模型一次收齊**（依原稿順序）：
  - **Bagging**：隨機森林、Extra Trees
  - **Boosting**：LightGBM、XGBoost、梯度提升、AdaBoost
  - **樹與規則**：決策樹、CN2 規則歸納
  - **線性與距離**：線性迴歸、邏輯迴歸、SVM、PLS、kNN
  - **機率**：單純貝氏、校準學習器
  - **最佳化與網路**：SGD、神經網路
  - **集成策略**：堆疊法（Stacking）
  - **前處理與特徵工程**：MaxAbsScaler、SelectFromModel + 多層 FeatureUnion
  - **基準與可解釋**：Constant 常數模型、計分表
  - **函數擬合與工程落地**：曲線擬合、儲存模型、載入模型
- **特別之處**：**每一章都有本機實測數字**（Python 3.11.15 / scikit-learn 1.9.1 / lightgbm 4.7.0 / xgboost 3.2.0，固定 `random_state=42`），原始輸出全文收錄於附錄 D。其中 **4 個結果與直覺相反**，也是考題最愛出的地方：
  - 對**本來就校準得不錯**的隨機森林再校準，Brier 反而由 0.0359 變差到 **0.0399**
  - **Extra Trees 反而略勝**隨機森林（RMSE 52.041 vs 52.964）而且快約 40%
  - 梯度提升學習率由 0.05 開到 0.5，訓練 RMSE 掉到 0.582（幾乎背下資料），測試卻由 54.768 升到 **62.757**
  - **Stacking（0.9591）輸給最強的單一成員** SVC（0.9766）
- 另有 **25 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/ml-models-notes/)** ｜ [互動測驗 60 題](/ml-models-notes/mc-quiz.html)

---

## 4 · H2O AutoML 實作（開源 H2O-3 端到端演練）

![H2O AutoML 實作 學習筆記](/img/covers/h2o-automl-notes.png)

- **定位**：AutoML 系列的**開源實作課節**，教材為獨立一份 **38 頁**簡報（⚠️ 幾乎都是截圖型頁面，關鍵內容在圖中，需要逐張判讀）
- **五個階段**：環境建置（H2O-3 + Flow）→ 資料匯入與解析（Import／Parse／Ticker 設 Enum）→ Run AutoML（Leaderboard 依 RMSE 挑模型）→ 模型匯出與 Python **遞迴預測** → Excel 樞紐分析圖
- **核心價值**：這是一條**完全免費、資料不離開本機**的生產線，而且補上前面兩份筆記沒有的「**訓練完之後怎麼用**」——把模型匯出、用程式呼叫、畫成圖
- **特別之處**：把課程「一句指令 + 一張截圖」背後的原因全部補齊，包括五個最容易卡住的地方：
  - **Java 版本**：H2O 只支援 **Java 8–17**；Java 23 的繞道參數只是略過版本檢查，不是真的支援
  - **`Ticker` 必須設成 Enum**：否則模型會把股票代號當成數量
  - **Import ≠ Parse**：前者只是搬進記憶體，後者才是讀懂格式並產生 `.hex`
  - **`overwrite: false`**：同路徑第二次匯出會失敗
  - **`h2o.jar` 的終端機不能關**：它正在跑 Flow 的後台伺服器
- **最值得看的一段**：遞迴預測（`Close_Lag1` ← 上一列的 `predict_Close`）。因為特徵只有 `Close_Lag1` 與 `Month`，模型會**收斂成固定的 12 個月週期** —— 2025／2026／2027 年 1 月的預測值幾乎完全相同（`53.2405`），正好證明它只學到季節性與均值回歸，而不是趨勢
- 另有 **6 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/h2o-automl-notes/)**

---

## 5 · 最新機器學習的教科書（DM2155）導讀

![最新機器學習的教科書導讀 學習筆記](/img/covers/ml-textbook-notes.png)

- **定位**：AutoML 系列的**橋樑書導讀**，教材為獨立一份 **12 頁**簡報（⚠️ **第 1 頁是封面頁，正文自第 2 頁起算**；且**整份沒有文字層**——12 頁全部是 1376×768 全頁 JPEG，只能逐頁判讀）
- **核心命題**：學不會機器學習不是努力問題，而是**課程的難度與學習者當前能力嚴重脫節**；解法不是硬啃原文書，而是先找到一本正確的**「過渡教科書」（橋樑書）**
- **三條主線**：
  - **診斷線**：三個症狀——缺乏穩固的數學與理論基礎知識／課程難度與學習者當前能力嚴重脫節／跳躍式的公式推導與艱澀的學術語言
  - **方法線**：**公式與程式碼 1:1 對應** ＋ **全視化 Jupyter Notebook**（網頁編寫／圖文筆記／即時執行／視覺結果）
  - **藍圖線**：**10 個節點分三階段**——Ch 1-4 地基（環境整備 → Python 基礎 → 資料視覺化 → 必備數學）、Ch 5-6 監督學習（線性回歸 → 模型評估 → 分類問題）、Ch 7-9 深度學習與無監督（神經網路入門 → 深度學習應用 → 無監督學習）
- **特別之處**：簡報的兩個技術主張都附**本機實測數字**（Python 3.11.15 / numpy 2.4.6 / scikit-learn 1.9.1 / PyTorch 2.14.1；本機**無 TensorFlow**，故以 numpy 1:1 重建公式語意）——
  - 公式逐項對得上：資料項 **0.7771559204**、正則項 **0.0652024658**（與 TF 語意差異 < 1e-12）；解析梯度 vs 數值梯度最大差 **5.597e-11**
  - MNIST 四步架構的測試準確率 **0.9489 → 0.9667 → 0.9778 → 0.9800**（淨 +0.0311），但四步的**訓練**準確率**全部是 1.0000**——單看訓練分數完全分不出差別
  - ⚠️ 高頻考點：`tf.nn.l2_loss(w)` **自帶 1/2**，所以 `lambda * tf.nn.l2_loss(w)` 對應的正是 λ/2 · ‖w‖²，**不要再自己除 2**
- 另有 **11 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/ml-textbook-notes/)** ｜ [互動測驗 60 題](/ml-textbook-notes/mc-quiz.html)

---

## 6 · 評估指標與 K-Means 聚類（單元二延伸）

![評估指標與 K-Means 聚類 學習筆記](/img/covers/automl-unit2-extra-notes.png)

- **定位**：AutoML 單元二的**延伸課節**，教材為獨立一份 **20 頁**簡報（⚠️ **整份都是正文、沒有封面頁**，所以 §1 就是第一個標題）
- **核心命題**：把「評估指標」與「K-Means 聚類」這兩塊最容易被死背的內容，**推導到數學定義層級**——每個指標都從混淆矩陣長出來，K-Means 的每一步都在最小化同一個目標函式
- **兩條主線**：
  - **指標線**：混淆矩陣四格 → Accuracy（在不平衡資料會騙人）→ Precision（怕 FP）→ Recall（怕 FN）→ F1（調和平均）→ 回歸三兄弟 MAE / RMSE / R²
  - **聚類線**：非監督式學習的本質（高內聚、低耦合）→ K-Means 五步循環（選 K → 初始化 → 分配 → 更新 → 收斂）
- **特別之處**：所有結論都附**本機實測數字**（Python 3.11.15 / scikit-learn 1.9.1 / numpy 2.4.6，固定 `random_state`，原始輸出全文收錄於附錄 G）——
  - 10,000 個細胞、10 個癌，全猜健康 → Accuracy **0.999000** 但 Recall **0.000000**
  - 門檻 0.5→3.5：Precision 由 0.0286 升到 1.0000，Recall 由 0.9000 掉到 0.1000；F1 最高落在門檻 **2.5**（0.3467）
  - `[5,3,4]` 與 `[1,1,10]` 的 MAE **都是 4.0000**，RMSE 卻由 **4.0825** 跳到 **5.8310**
  - R² 可以是負的：完美 **1.000000**、全猜平均 **0.000000**、比平均更糟 **−1.132762**
  - 手肘法與輪廓係數同時指向 **K=4**（inertia 降幅由 1569.9 崩到 19.5；輪廓係數 0.8756 最高）
  - K-Means 不做特徵縮放時，群內身高標準差由真實的 3 公分**膨脹到約 10 公分**
  - `max_iter=5` 不會報錯，只是停在 inertia **4892.0**（正常收斂為 **4389.2**）
- **三個高頻考點**：inertia 隨 K **單調遞減**（不能選最小值）、歐幾里得距離**必須先做特徵縮放**、`n_iter_ < max_iter` 才算真的收斂
- 另有 **14 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/automl-unit2-extra-notes/)** ｜ [互動測驗 60 題](/automl-unit2-extra-notes/mc-quiz.html)

---

## 7 · 線性迴歸入門：用一條直線看懂關係（統計入門）

![線性迴歸入門 學習筆記](/img/covers/linear-regression-notes.png)

- **定位**：AutoML 系列的**統計入門**課節，教材為獨立一份 **12 頁**簡報（另附 12 頁備忘稿；⚠️ **第 1 頁是課節封面頁，正文自第 2 頁起算**，所以 §1 對應課程第 2 頁）
- **核心命題**：用**一條直線**把整件事講完——先建立直覺、再拆解符號、然後代數字、最後講風險；不要求先會微積分
- **四段推進**：
  - **直覺段**：兩個生活例子（氣溫與冰淇淋、讀書時數與成績）→ 線性迴歸的一句話定義
  - **符號段**：一行公式四個角色（x 輸入／y 輸出／a 斜率／b 截距）→ 斜率管方向與陡度、截距管起點
  - **實作段**：示意模型 y = 5x + 50 → 讀 4 小時預測 70 分 → 殘差 → 最小平方法三步
  - **風險段**：相關不等於因果、避免過度外推、彎曲關係別硬套
- **特別之處**：課程把**所有公式都做成圖片**，文字層只留說明文字（抽取時會出現「　是輸入」這種缺口），筆記已逐張開圖還原成 LaTeX；12 頁備忘稿內容完整，已逐頁摘要進各章節
- **本機實測**（Python 3.11.15 / numpy 2.4.6 / scikit-learn 1.9.1，原始輸出全文收錄於附錄 G）：
  - 電腦從同一組點學回 a = **5.0000**、b = **50.0000**（最大還原誤差 0.00e+00）——這就是「a、b 是從資料學出來的」
  - 三條候選線 SSE = 14.0／51.0／87.0，最小平方法挑出的那條 **12.3000**（比課程那條更低）
  - 殘差 [10, -10] 直接相加 = **0.0**（看似完美），平方後 = **200.0**；大誤差被放大 **50 倍**
  - 同一個模型丟 x = 20 → **150 分**（外推的荒謬）；只用 x = 3..8 配線，截距估成 **48.1238**（真實 50.0）
  - 對 y = x² 硬套直線 R² = **0.0000**，改用二次曲線 **1.0000**
- **三個高頻考點**：a = 0 只代表「此線性模型」的預測不隨 x 改變、殘差是「實際值 − 預測值」、資料未涵蓋 x = 0 時 b 只是數學交點
- 另有 **11 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/linear-regression-notes/)** ｜ [互動測驗 60 題](/linear-regression-notes/mc-quiz.html)

---

## 8 · 用 TPOT 預測無人機訂單成交率（開源 AutoML 實作延伸）

![用 TPOT 預測無人機訂單成交率](/img/covers/redix-tpot-sales-prediction.png)

- **定位**：單元四（開源 AutoML／TPOT）的**實作延伸**——用一份真實業務形狀的資料（**500 筆歷史成交名單 ＋ 15 筆待預測**）把 TPOT 走完整流程；形式是**部落格文章**（不是單檔筆記頁）
- **核心命題**：AutoML 交出的「最佳 Pipeline」看起來漂亮，但**指標選錯、解釋沒補、門檻沒調**，就完全不能用
- **三個教學重點**：
  - **準確率陷阱**：91.8% 的訂單都會成交 → 「全部猜成交」就有 **92% 準確率**，卻一筆漏單都抓不到（平衡準確率 0.500）
  - **解釋性要自己補**：置換重要度（模型無關）＋ 勝算比（線性模型）互相印證——兩者都指向**瀏覽頁數**最關鍵；但 TPOT 的 Bagging 管線把其他特徵的重要性「吃掉」了（多數顯示 0.0000）
  - **門檻才是決策**：同一條管線、同一組機率，門檻 **0.50 全部猜成交**、門檻 **0.90 抓出 5 筆未成交**；而且門檻只能用**訓練集**挑（用測試集挑＝作弊）
- **本機實測**（Python 3.12 / **TPOT 1.1.0** / scikit-learn 1.9.1 / 安全 dask client，不用 Colab）：
  - 課堂版（2 代 × 10 族群）**6.5 秒**：ROC-AUC **0.8770**（輸給手寫邏輯迴歸 0.9198）
  - 課後挑戰版（`--budget 2`）**122.4 秒**：ROC-AUC **0.9253**（反超基準線）、平衡準確率 **0.8614**
  - 門檻調校：0.50 → 平衡準確率 0.5000；**0.90 → 0.8614**（未成交召回 7/8）
  - 15 筆預測：成交 10 筆／未成交 5 筆，預測成交金額 **1,764,500 HKD**
  - TPOT 1.1.0 **已移除 `tpot.export()`** → 自製轉碼工具，**往返測試 PASS**（重建後 15 筆機率完全相同）
- **附圖**：1 張封面 ＋ **5 張 Qwen-Image 2.1 插圖** ＋ 3 張實跑圖表（特徵重要性三聯圖／預測結果／門檻調校）
- **👉 [看文章](/2026/10/18/redix-tpot-sales-prediction/)** ｜ [下載一頁 A4 講義（PDF）](/redix-tpot/handout.pdf)

---

## 9 · Azure ML AutoML 實作全紀錄（雲端平台實作延伸）

![Azure ML AutoML 實作全紀錄](/img/covers/azure-automl-bank-churn-walkthrough.png)

- **定位**：單元三（Azure AutoML 雲端平台實戰）的**實作延伸**——把單元三的六步價值鏈在 Azure ML Studio 上真的走完一次；形式是**部落格文章**（不是單檔筆記頁）
- **核心命題**：**知道有「資料註冊 → 雲端算力 → 自動選演算法 → 部署成 REST API」這四件事，和真的把它跑完一次，是兩件不同的事**——尤其在雲端，每一個欄位都對應一筆帳單
- **三個教學重點**：
  - **成本控制**：叢集設**最小節點 0／最大節點 1**（不是常見範例的 0/2），實測證明**單一節點足以跑完**；但**設 0 不等於不用等**，首次啟用仍要佈建時間
  - **timeout 不是「保證總時長」**：設 **30 分鐘**，實際 Duration **38 分 15.16 秒**才結束（畫面附 timeout 警告）——排程要留餘裕
  - **部署尾段多一步**：**Consume 分頁才是交付終點**——REST 網址 ＋ Primary／Secondary key ＋ JavaScript／Python／C#／JSON 四種呼叫範例
- **畫面實測**（工作區 `Practice`／`germanywestcentral`／Azure for Students）：
  - 計算叢集 **Standard_DS11_v2**（2 cores／14 GB／$0.17/hr）、最小 0／最大 1、閒置縮放 **120 秒**
  - 資料資產 `training`／**`bank_marketing_train.csv`**（**81.38 KiB**）、存放區 `workspaceblobstore`
  - 任務 **Classification**、目標欄位 **`y (String)`**（標籤不必先轉 0/1）、任務 VM `Standard_DS3_v2`、instances 1
  - **Enable early termination 已勾選** ＋ `Experiment timeout = 30`（其餘限制欄位留白）
  - 最佳模型 **VotingEnsemble**、**AUC weighted 0.87459**、Sampling **100.00%**
  - 端點 **`practice-zmrf`**、部署 VM `Standard_D2as_v4`（$0.10/hr）；部署時出現配額警告 `Current usage/limit: 0/4`
- **附圖**：1 張封面 ＋ **19 張操作截圖**（六個步驟逐步，含實測值對照表）
- **👉 [看文章](/2026/10/18/azure-automl-bank-churn-walkthrough/)**

---

## 10 · 手寫 Ridge vs TPOT：房價迴歸的對照（迴歸題實作延伸）

![手寫 Ridge vs TPOT AutoML：同一份房價資料](/img/covers/house-price-ridge-vs-tpot.png)

- **定位**：單元四（開源 AutoML：TPOT）的**迴歸題實作延伸**——前一篇（Redix）是分類題、AutoML 贏；這一篇刻意挑**迴歸題**，而且**先量出資料的雜訊底線**，再用同一把尺看 AutoML 到底換到什麼
- **核心命題**：**AutoML 的「最佳」是有預算前提的最佳**——500 筆房價、100 筆待預測，TPOT 花 11.8 分鐘搜了 390 條管線，最後與手寫 Ridge **打平**（p = 0.6932）
- **三個教學重點**：
  - **先量天花板**：OLS 殘差 σ = **25,263 USD** 就是這個題目的極限；Ridge 的 25,696 只比它高 **1.7%** → 搜尋再多也只是在同一塊高原上採樣
  - **線性完勝樹**：11 條候選管線裡 Ridge **25,696** 打敗隨機森林 37,125（差 45%）——**關係本來就是線性的**，AutoML 的價值在「有東西可探索」時才成立
  - **贏家詛咒**：TPOT 內部 5 折（390 條取最小值）必然偏樂觀；要用**獨立協定**（RepeatedKFold 5×4）重評才是 25,700
- **本機實測**（Python 3.11.16 ／ **TPOT 1.1.0** ／ scikit-learn 1.9.1 ／ 執行緒式 dask client，不用 Colab）：
  - 手寫 Ridge：CV RMSE **25,696 ± 2,154**、10 折 OOF R² **0.9719**、MAE 20,874、MAPE 4.33%
  - TPOT：CV RMSE **25,700 ± 2,139**、**11.8 分鐘／13 代／390 條管線**、5 步堆疊集成（VarianceThreshold → FeatureUnion(原始 11 欄 ∪ LinearSVR ∪ MLPRegressor(41) ∪ LinearSVR) → ARDRegression）
  - 配對檢定：t = +0.401、**p = 0.6932**（Wilcoxon p = 0.4524）；100 筆預測相關係數 **0.99999**、平均差 452 USD（最大 1,363 USD）
  - 對「無雜訊公式」欄位：TPOT 誤差 **350 USD** vs Ridge 701 USD——**公式學得更準，但優勢被雜訊吃掉**
  - TPOT 1.1.0 API 差異（`scorers`／`search_space`／`verbose`／`client` 位置）＋ **`tpot.export()` 已移除** → 自製轉碼工具修掉 `KFold` 未 import 的 bug，**往返測試 PASS**（100/100 筆完全相同）
- **附圖**：1 張封面（Qwen-Image 2.1）＋ **6 張章節插圖**（Qwen-Image 2.1，house style 無文字）＋ **5 張實跑圖表**（六格診斷儀表板／11 條管線 CV 對照＋雜訊底線／兩條路線管線對照／預測一致度／公式還原度）
- **👉 [看文章](/2026/10/18/house-price-ridge-vs-tpot/)**

---

## 11 · Orange AI 視覺化資料探勘（No-Code 工具實作）

![Orange AI 視覺化資料探勘 學習筆記](/img/covers/orange-ai-notes.png)

- **定位**：AutoML 系列的**視覺化 No-Code 工具**課節，教材為獨立一份 **59 頁**簡報（⚠️ **第 1 頁是封面頁，正文自第 2 頁起算**；且 **12 頁是「純圖片頁」**——p1–p9 與 p17、p43 沒有文字層，全部是 960×540 整頁點陣圖，用任何工具抽取只會得到空白或 `preencoded.png`，筆記已逐頁渲染判讀）
- **核心命題**：**不寫一行程式碼，也能把資料探勘做完** —— 用拖拉 Widget、接 Channel 的方式，把「資料匯入 → 檢視探索 → 處理 → 建模 → 評估 → 輸出」整條流程拼出來
- **三條主線**：
  - **平台線**：Widget（元件）＋ Channel（通道）＝ Workflow（`.ows`）；**Data 面板 12 元件（4+4+4）**、**Model 面板 20 元件**
  - **模型線**：五種核心監督模型（CN2／kNN／決策樹／隨機森林／梯度提升）＋ 九種入門演算法（SVM／線性迴歸／邏輯迴歸／樸素貝氏／評分表／AdaBoost／PLS／Curve Fit／神經網絡／SGD）
  - **元件線**：四個核心模型元件 —— **Constant（基準）→ Stacking（整合）→ Save Model → Load Model**
- **特別之處**：這是本站**第一次把「GUI 工具」本身當成考科**來整理——所有數字都用 **Orange 3.40.0 的 Python API** 在本機跑出來（`Orange.data.Table("iris")` 等），不是抄課本的
- **本機實測**（Windows / Python **3.11.16** / **Orange 3.40.0** / scikit-learn **1.9.1**，全部 `random_state=42`，原始輸出全文收錄於附錄 D）：
  - **把 20 個元件全部跑一遍**：kNN **0.9667**｜邏輯迴歸 **0.9667**｜Stacking **0.9667**｜SVM／AdaBoost／Calibrated **0.9600**｜梯度提升／神經網路 **0.9533**｜決策樹／隨機森林 **0.9467**｜CN2 **0.8933**｜樸素貝氏 **0.8733**｜SGD **0.8333**｜**Constant 0.3333**
  - **Constant = 0.3333 正好等於 50/150，AUC = 0.5000** —— 這就是「基準線」的實體
  - **最反直覺的一組**：決策樹與隨機森林 **CA 完全相同（0.9467）**，但 **AUC 是 0.9613 → 0.9954** —— 只看準確率會誤判「森林沒用」
  - **Stacking（0.9667）只追平最強的單一成員**，沒有超越 —— 與其他筆記的結論一致：整合不是萬靈丹
  - **CN2 真的把 15 條 IF–THEN 規則印出來**（最後一條是 `IF TRUE THEN …` 的預設規則）
  - **評分表只支援二元分類**：拿 3 類的 iris 會直接報 `ValueError: Too many target variable values.`；改用 `heart_disease` 後 **CA 0.8416 vs Constant 0.5413**，而且**只用 5 個整數配分**（可手算）
  - **Save／Load Model**：`.pkcls` 約 **179 KB**，載入後預測與原模型**完全一致**
  - **迴歸**（housing）：線性 **RMSE 4.8467 / R² 0.7217**｜PLS（2 成分）**5.0814 / 0.6941**｜Curve Fit **6.2289 / 0.5404**
- **另外收錄**：原稿文字層的 **18 個錯字對照表**（`cdit Domain`＝Edit Domain、`Cank`＝Rank、`M ySBL`＝MySQL、`Csabkimg`＝Stacking…，還有 **Orange 官方自己把 Descent 拼成 `Decent`**）
- 另有 **18 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/orange-ai-notes/)** ｜ [互動測驗 60 題](/orange-ai-notes/mc-quiz.html)

---

## 筆記的共同規格

| 項目 | 說明 |
|---|---|
| 格式 | **單一 HTML 檔、零外部資源**，下載後可離線雙擊開啟 |
| 版面 | 左側固定側邊欄 + **自動產生的巢狀目錄樹**（不會有壞連結） |
| 測驗 | **60 題互動 MC**：即時計分、進度存 localStorage、可列印 |
| 附錄 | 名詞速查表、常見錯誤與陷阱、Prompt 範本集、一頁精華（考前 10 分鐘） |
| 原始檔 | 每頁都可下載原始 Markdown |
| 來源 | 依課程大綱逐節重寫，並補上考點、指令與實測數據 |

---

## 課程單元總覽

| 單元 | 主題 | 主要工具 | 筆記 |
|:---:|---|---|---|
| **一** | AutoML 基礎與 AI 倫理 | Excel、ChatGPT／Copilot、Kaggle | ✅ [AutoML 學習筆記](/automl-notes/) |
| **二** | 核心算法與模型評估 | Teachable Machine、TF Playground、Excel | ✅ 同上 |
| **三** | Azure AutoML 雲端平台實戰 | Azure Machine Learning Studio | ✅ 同上 |
| **四** | 開源 AutoML 工具與綜合應用 | Google Colab、Python、TPOT | ✅ 同上 |
| **延伸** | 泛化能力（Generalization Capability） | Python、scikit-learn、numpy | ✅ [泛化能力筆記](/generalization-notes/) |
| **延伸** | 評估指標與 K-Means 聚類（單元二延伸） | Python、scikit-learn、numpy、StandardScaler | ✅ [評估指標與 K-Means 筆記](/automl-unit2-extra-notes/) |
| **速查** | 機器學習模型速查（25 個模型卡） | Python、scikit-learn、LightGBM、XGBoost | ✅ [模型速查筆記](/ml-models-notes/) |
| **開源實作** | H2O AutoML 實作（H2O-3 + Flow 端到端） | H2O-3、Flow、Python、pandas、Excel | ✅ [H2O AutoML 筆記](/h2o-automl-notes/) |
| **導讀** | 《最新機器學習的教科書》DM2155 導讀（橋樑書：基礎數學 ＋ Python 實作） | Python、Jupyter、Keras、TensorFlow | ✅ [導讀筆記](/ml-textbook-notes/) |
| **統計入門** | 線性迴歸入門：用一條直線看懂關係（四個角色 → 斜率／截距 → 殘差 → 最小平方法） | Python、numpy、scikit-learn | ✅ [線性迴歸入門筆記](/linear-regression-notes/) |
| **實作延伸** | 用 TPOT 預測無人機訂單成交率（準確率陷阱 → 特徵重要性 → 門檻調校） | Python、TPOT 1.1.0、scikit-learn、dask | ✅ [Redix TPOT 文章](/2026/10/18/redix-tpot-sales-prediction/) ｜ [A4 講義 PDF](/redix-tpot/handout.pdf) |
| **實作延伸** | Azure ML AutoML 實作全紀錄（建立算力 → 資料註冊 → 訓練 → 部署 REST 端點） | Azure Machine Learning Studio、Azure for Students | ✅ [Azure ML AutoML 文章](/2026/10/18/azure-automl-bank-churn-walkthrough/) |
| **實作延伸** | 手寫 Ridge vs TPOT AutoML：房價迴歸對照（雜訊底線 → 11 條候選管線 → 390 條 TPOT 管線） | Python、TPOT 1.1.0、scikit-learn、dask | ✅ [房價 Ridge vs TPOT 文章](/2026/10/18/house-price-ridge-vs-tpot/) |
| **No-Code 工具** | Orange AI 視覺化資料探勘（Widget／Channel → 20 個模型元件 → Constant／Stacking／Save-Load） | Orange 3.40、Python（Orange API） | ✅ [Orange AI 筆記](/orange-ai-notes/) |

---

*本頁為個人學習筆記整理。*
