# CNN 2：卷積神經網路（二）學習筆記

> 「CNN 1」講機器怎麼看與卷積的數學；「CNN 2」講**一個可訓練的分類 CNN 長什麼樣**：
> 局部連接、輸出體積、ReLU、池化、空洞卷積，最後把模型組起來、看它在真實任務上的樣子。
> 本筆記另外把課程的模型**真的跑起來**，用六組設定與三個平台驗證課堂上的說法。
> 只想看結論的話，可直接跳到 §12；完整實驗紀錄在另一篇專題。

<!-- CNN2-FIGURE:overview -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 165" role="img" aria-label="CNN 分類網路架構：Input → Conv 32 → Pool → Conv 64 → Pool → Flatten → Dense 1024 → Softmax 10 類"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect fill="#0d1117"/><text x="20" y="30" fill="#e0a458" font-size="12.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">前五層學特徵，後三層做分類</text><rect x="20" y="60" width="96" height="56" rx="7" fill="none" stroke="#4ecdc4" stroke-width="1.6"/><text x="68.0" y="84.0" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Input</text><text x="68.0" y="101.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">影像</text><line x1="116" y1="88.0" x2="129" y2="88.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="132" y="60" width="96" height="56" rx="7" fill="none" stroke="#4ecdc4" stroke-width="1.6"/><text x="180.0" y="84.0" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Conv 32</text><text x="180.0" y="101.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3×3+ReLU</text><line x1="228" y1="88.0" x2="241" y2="88.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="244" y="60" width="96" height="56" rx="7" fill="none" stroke="#4ecdc4" stroke-width="1.6"/><text x="292.0" y="84.0" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Pool</text><text x="292.0" y="101.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2×2</text><line x1="340" y1="88.0" x2="353" y2="88.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="356" y="60" width="96" height="56" rx="7" fill="none" stroke="#4ecdc4" stroke-width="1.6"/><text x="404.0" y="84.0" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Conv 64</text><text x="404.0" y="101.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3×3+ReLU</text><line x1="452" y1="88.0" x2="465" y2="88.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="468" y="60" width="96" height="56" rx="7" fill="none" stroke="#4ecdc4" stroke-width="1.6"/><text x="516.0" y="84.0" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Pool</text><text x="516.0" y="101.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2×2</text><line x1="564" y1="88.0" x2="577" y2="88.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="580" y="60" width="96" height="56" rx="7" fill="none" stroke="#e0a458" stroke-width="1.6"/><text x="628.0" y="84.0" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Flatten</text><text x="628.0" y="101.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 向量</text><line x1="676" y1="88.0" x2="689" y2="88.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="692" y="60" width="96" height="56" rx="7" fill="none" stroke="#e0a458" stroke-width="1.6"/><text x="740.0" y="84.0" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Dense</text><text x="740.0" y="101.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1024+ReLU</text><line x1="788" y1="88.0" x2="801" y2="88.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="804" y="60" width="96" height="56" rx="7" fill="none" stroke="#ff7b72" stroke-width="1.6"/><text x="852.0" y="84.0" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Softmax</text><text x="852.0" y="101.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10 類</text><text x="20" y="146" fill="#8b949e" font-size="11.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">可訓練的權重只在 Conv 與 Dense；Pool 與 Softmax 沒有參數</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">整個分類網路：前五層抽特徵，後三層把特徵變成類別分數；可訓練的參數只在 Conv 與 Dense。</figcaption>
</figure>
<!-- /CNN2-FIGURE:overview -->

## 0. 30 秒總複習（考前最後掃描）

```
一張影像 → [Conv → ReLU → Pool] × N → Flatten → Dense → Softmax → 類別機率
             ↑ 濾波器權重全部由資料學出來，同一組權重滑過整張圖
```

| 想問的事 | 一句話答案 |
|---|---|
| 卷積層的 depth 由什麼決定 | **濾波器數量**，不是輸入通道數 |
| 輸出面積怎麼算 | `O = (N + 2P − F)/S + 1` |
| 池化有參數嗎 | 沒有，只降維、不學習 |
| ReLU 死掉會怎樣 | 梯度恆 0，權重永不再更新 |
| 全連接層為什麼貴 | 參數量 ≈ 特徵維度 × 神經元數，佔全模型九成以上 |

## 1. 一個影像分類 CNN 的全貌

輸入影像 → 兩層卷積（各自接池化）→ 攤平 → 兩層全連接 → softmax。

| 階段 | 做的事 | 學到的東西 |
|---|---|---|
| 卷積層 | 用濾波器掃過影像，產生特徵圖 | 邊緣、紋理、部件、物件結構 |
| 池化層 | 在鄰域內取最大或平均 | 去掉「位置」這種不必要的細節 |
| 全連接層 | 把特徵向量映射到類別分數 | 類別之間的界線 |

## 2. 表徵學習：低層、中層、高層

<!-- CNN2-FIGURE:hierarchy -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 165" role="img" aria-label="表徵學習的三層階梯：低層學邊緣與暗斑，中層組合出眼睛、耳朵、鼻子，高層才有臉部結構"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect fill="#0d1117"/><rect x="30" y="36" width="230" height="80" rx="9" fill="none" stroke="#4ecdc4" stroke-width="1.8"/><text x="46" y="62" fill="#4ecdc4" font-size="12.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">低層</text><text x="46" y="92" fill="#e6edf3" font-size="14" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">邊緣、暗斑</text><rect x="280" y="36" width="230" height="80" rx="9" fill="none" stroke="#58a6ff" stroke-width="1.8"/><text x="296" y="62" fill="#58a6ff" font-size="12.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">中層</text><text x="296" y="92" fill="#e6edf3" font-size="14" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">眼睛、耳朵、鼻子</text><rect x="530" y="36" width="230" height="80" rx="9" fill="none" stroke="#e0a458" stroke-width="1.8"/><text x="546" y="62" fill="#e0a458" font-size="12.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">高層</text><text x="546" y="92" fill="#e6edf3" font-size="14" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">臉部結構</text><line x1="262" y1="76" x2="276" y2="76" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><line x1="512" y1="76" x2="526" y2="76" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><text x="30" y="146" fill="#8b949e" font-size="11.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">沒有人教它「眼睛長什麼樣」——三層都是訓練時順手學出來的</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">表徵學習的階層：第一層看到邊緣，第二層組合出部件，第三層才有物件結構。</figcaption>
</figure>
<!-- /CNN2-FIGURE:hierarchy -->

| 深度 | 學到的東西 | 層級 |
|---|---|---|
| 第一層卷積 | 邊緣、暗斑 | 低層 |
| 第二層卷積 | 眼睛、耳朵、鼻子 | 中層 |
| 第三層卷積 | 臉部結構 | 高層 |

三層都不是人工設計的，而是**從資料裡學出來的**（de novo feature learning）：
沒有人告訴網路「眼睛是圓的」，它只是在最小化分類誤差時，順手把有用的部件學了出來。

- **階層**：低層幾何原語 → 中層部件 → 高層物件結構，愈深愈抽象。
- **參數共享**：同一組濾波器滑過整張圖，這是 CNN 比全連接網路省下大量參數的原因。

## 3. 分類三步曲：卷積 → 非線性 → 池化

| 步驟 | 作用 | Keras |
|---|---|---|
| 卷積 | 套用濾波器，產生特徵圖 | `tf.keras.layers.Conv2D` |
| 非線性 | 通常用 ReLU | `activation="relu"` |
| 池化 | 對每張特徵圖降採樣 | `tf.keras.layers.MaxPool2D` |

訓練時被更新的只有**濾波器的權重**；池化沒有參數，卷積的「滑動」本身也沒有參數。

## 4. 卷積層的局部連接

<!-- CNN2-FIGURE:local -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 215" role="img" aria-label="卷積層的局部連接：3×3 濾波器滑過 6×6 輸入的一小塊 patch，同一組權重滑遍全圖"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect fill="#0d1117"/><rect x="30" y="26" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="56" y="26" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="82" y="26" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="108" y="26" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="134" y="26" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="160" y="26" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="30" y="52" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="56" y="52" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="82" y="52" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="108" y="52" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="134" y="52" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="160" y="52" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="30" y="78" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="56" y="78" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="82" y="78" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="108" y="78" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="134" y="78" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="160" y="78" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="30" y="104" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="56" y="104" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="82" y="104" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="108" y="104" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="134" y="104" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="160" y="104" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="30" y="130" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="56" y="130" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="82" y="130" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="108" y="130" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="134" y="130" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="160" y="130" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="30" y="156" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="56" y="156" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="82" y="156" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="108" y="156" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="134" y="156" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="160" y="156" width="26" height="26" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="56" y="52" width="26" height="26" fill="#e0a458" opacity="0.3"/><rect x="82" y="52" width="26" height="26" fill="#e0a458" opacity="0.3"/><rect x="56" y="78" width="26" height="26" fill="#e0a458" opacity="0.3"/><rect x="82" y="78" width="26" height="26" fill="#e0a458" opacity="0.3"/><text x="30" y="19" fill="#8b949e" font-size="11.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸入 6×6</text><rect x="56" y="52" width="52" height="52" fill="none" stroke="#e0a458" stroke-width="2.2"/><line x1="196" y1="88" x2="240" y2="88" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="244" y="58" width="140" height="58" rx="7" fill="none" stroke="#4ecdc4" stroke-width="1.6"/><text x="314.0" y="83.0" fill="#e6edf3" font-size="12.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一個神經元</text><text x="314.0" y="100.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">加權和 + bias</text><line x1="388" y1="88" x2="424" y2="88" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="428" y="68" width="52" height="38" rx="7" fill="none" stroke="#58a6ff" stroke-width="1.6"/><text x="454.0" y="92.0" fill="#e6edf3" font-size="12.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ReLU</text><line x1="484" y1="88" x2="520" y2="88" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="524" y="58" width="156" height="58" rx="7" fill="none" stroke="#e0a458" stroke-width="1.6"/><text x="602.0" y="83.0" fill="#e6edf3" font-size="12.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">特徵圖 1 格</text><text x="602.0" y="100.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一組權重滑遍全圖</text><text x="30" y="200" fill="#8b949e" font-size="11.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3×3 濾波器 = 9 個權重，走到哪裡都同一組</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">局部連接：一個神經元只讀一小塊 patch，同一組權重滑過整張圖就是參數共享。</figcaption>
</figure>
<!-- /CNN2-FIGURE:local -->

每個神經元只「看」輸入的一小塊 patch：取 patch 內的輸入 → 加權和 → 加 bias → 過非線性。

為什麼不直接用全連接？

- **參數量**：28×28 影像接 1024 個神經元要 78 萬個權重；卷積用 32 個 3×3 濾波器只要 320 個。
- **空間結構**：全連接把影像攤成一條向量，位置資訊被抹掉；卷積保留「誰在誰旁邊」。

## 5. 輸出體積、stride、感受野

<!-- CNN2-FIGURE:volume -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 660 195" role="img" aria-label="輸出體積與步幅：6×6 輸入、3×3 核、stride 2 得到 3×3 輸出，depth 等於濾波器數量"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect fill="#0d1117"/><rect x="24" y="30" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="48" y="30" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="72" y="30" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="96" y="30" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="120" y="30" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="144" y="30" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="24" y="54" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="48" y="54" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="72" y="54" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="96" y="54" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="120" y="54" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="144" y="54" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="24" y="78" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="48" y="78" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="72" y="78" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="96" y="78" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="120" y="78" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="144" y="78" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="24" y="102" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="48" y="102" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="72" y="102" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="96" y="102" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="120" y="102" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="144" y="102" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="24" y="126" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="48" y="126" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="72" y="126" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="96" y="126" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="120" y="126" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="144" y="126" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="24" y="150" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="48" y="150" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="72" y="150" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="96" y="150" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="120" y="150" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="144" y="150" width="24" height="24" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="24" y="30" width="24" height="24" fill="#4ecdc4" opacity="0.3"/><rect x="72" y="30" width="24" height="24" fill="#4ecdc4" opacity="0.3"/><rect x="24" y="78" width="24" height="24" fill="#4ecdc4" opacity="0.3"/><rect x="72" y="78" width="24" height="24" fill="#4ecdc4" opacity="0.3"/><rect x="24" y="126" width="24" height="24" fill="#4ecdc4" opacity="0.3"/><rect x="72" y="126" width="24" height="24" fill="#4ecdc4" opacity="0.3"/><text x="24" y="23" fill="#8b949e" font-size="11.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸入 6×6，k=3、s=2</text><line x1="192" y1="102" x2="226" y2="102" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="230" y="42" width="24" height="24" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.5"/><rect x="254" y="42" width="24" height="24" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.5"/><rect x="278" y="42" width="24" height="24" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.5"/><rect x="230" y="66" width="24" height="24" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.5"/><rect x="254" y="66" width="24" height="24" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.5"/><rect x="278" y="66" width="24" height="24" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.5"/><rect x="230" y="90" width="24" height="24" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.5"/><rect x="254" y="90" width="24" height="24" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.5"/><rect x="278" y="90" width="24" height="24" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.5"/><text x="230" y="35" fill="#8b949e" font-size="11.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出 3×3</text><rect x="340" y="34" width="300" height="60" rx="7" fill="none" stroke="#e0a458" stroke-width="1.6"/><text x="490.0" y="69.0" fill="#e6edf3" font-size="15" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">O = (N + 2P − F) / S + 1</text><text x="340" y="120" fill="#4ecdc4" font-size="12" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">depth（d）= 濾波器數量，不是輸入通道數</text><text x="230" y="152" fill="#8b949e" font-size="11.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每一格 = 一個濾波器在該位置的輸出</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">輸出體積與步幅。depth 由濾波器數量決定，面積由公式算。</figcaption>
</figure>
<!-- /CNN2-FIGURE:volume -->

- **輸出體積** `h × w × d`：`d` 就是**濾波器數量**。
- **stride**：每次移動幾格；變大 → 輸出變小、計算變便宜。
- **感受野**：輸出節點在輸入影像上「路徑連到」的區域，層層堆疊會變大。

```
O = (N + 2P − F) / S + 1
```

以課程的模型、輸入 28×28、3×3 核、stride 1、不填充為例：
`28 → 26 → pool 13 → 11 → pool 5 → Flatten 5×5×64 = 1600 維`（實測一致，見 §10 的層表）。

<!-- CNN2-FIGURE:shapes -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 210" role="img" aria-label="張量形狀階梯：28×28×1 經 Conv 變 26×26×32、Pool 變 13×13×32、再 Conv 變 11×11×64、Pool 變 5×5×64，Flatten 後 1600 維"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect fill="#0d1117"/><text x="40" y="32" fill="#e0a458" font-size="13" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個模型，張量一路縮小：28×28×1 → 1600 維</text><rect x="40" y="74" width="100" height="54" rx="8" fill="none" stroke="#4ecdc4" stroke-width="1.6"/><text x="90.0" y="106.0" fill="#e6edf3" font-size="12.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">28×28×1</text><line x1="140" y1="101.0" x2="188" y2="101.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><text x="166.0" y="62" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Conv 3×3</text><rect x="192" y="74" width="100" height="54" rx="8" fill="none" stroke="#4ecdc4" stroke-width="1.6"/><text x="242.0" y="106.0" fill="#e6edf3" font-size="12.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">26×26×32</text><line x1="292" y1="101.0" x2="340" y2="101.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><text x="318.0" y="62" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Pool 2×2</text><rect x="344" y="74" width="100" height="54" rx="8" fill="none" stroke="#58a6ff" stroke-width="1.6"/><text x="394.0" y="106.0" fill="#e6edf3" font-size="12.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">13×13×32</text><line x1="444" y1="101.0" x2="492" y2="101.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><text x="470.0" y="62" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Conv 3×3</text><rect x="496" y="74" width="100" height="54" rx="8" fill="none" stroke="#4ecdc4" stroke-width="1.6"/><text x="546.0" y="106.0" fill="#e6edf3" font-size="12.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">11×11×64</text><line x1="596" y1="101.0" x2="644" y2="101.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><text x="622.0" y="62" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Pool 2×2</text><rect x="648" y="74" width="100" height="54" rx="8" fill="none" stroke="#58a6ff" stroke-width="1.6"/><text x="698.0" y="106.0" fill="#e6edf3" font-size="12.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5×5×64</text><line x1="748" y1="101.0" x2="796" y2="101.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><text x="774.0" y="62" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Flatten</text><rect x="800" y="74" width="100" height="54" rx="8" fill="none" stroke="#e0a458" stroke-width="1.6"/><text x="850.0" y="106.0" fill="#e6edf3" font-size="12.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1600 維</text><text x="40" y="178" fill="#8b949e" font-size="11.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">卷積只改 channel 數（= 濾波器數量），池化只砍面積，Flatten 只攤平。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">課程模型的張量形狀：28×28×1 → 26×26×32 → 13×13×32 → 11×11×64 → 5×5×64 → 1600 維。</figcaption>
</figure>
<!-- /CNN2-FIGURE:shapes -->

## 6. 非線性：ReLU 與「死掉的」神經元

每層卷積之後都要接非線性，否則多層疊起來仍是**一個線性變換**：

```
f(x) = max(0, x)
```

課程留了兩個問題，答案比公式重要：

| 問題 | 答案 |
|---|---|
| 什麼時候會「反向傳播穿過」ReLU？ | 這次 forward 輸入為正時梯度照原樣傳回；輸入 ≤ 0 時梯度是 0，這條路徑這次不更新 |
| 一旦它「死掉」會怎樣？ | bias 被推到很負、對所有輸入都輸出 0，梯度永遠是 0，權重永遠不動 |

**很容易答錯的地方：把「稀疏」當成「死亡」。** ReLU 輸出本來就有一半左右是 0；
真正的死亡要看「**同一個濾波器對所有輸入都輸出 0**」。本筆記兩個都量了：

| 指標 | 意義 | 實測（MNIST，5 輪） |
|---|---|---|
| 零激活比例 | 所有激活值裡為 0 的比例 | 50.6%（健康） |
| 死濾波器比例 | 對每個輸入都輸出 0 的濾波器比例 | 0.0% |

## 7. 池化：降維與空間不變性

<!-- CNN2-FIGURE:pool -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 630 150" role="img" aria-label="2×2 最大池化：4×4 輸入取每個鄰域的最大值，降成 2×2 輸出且沒有參數"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect fill="#0d1117"/><rect x="30" y="30" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="58" y="30" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="86" y="30" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="114" y="30" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="30" y="58" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="58" y="58" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="86" y="58" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="114" y="58" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="30" y="86" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="58" y="86" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="86" y="86" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="114" y="86" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="30" y="114" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="58" y="114" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="86" y="114" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="114" y="114" width="28" height="28" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><text x="30" y="23" fill="#8b949e" font-size="11.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸入 4×4</text><text x="44.0" y="48" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><text x="72.0" y="48" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><text x="100.0" y="48" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><text x="128.0" y="48" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="44.0" y="76" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text><text x="72.0" y="76" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text><text x="100.0" y="76" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><text x="128.0" y="76" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><text x="44.0" y="104" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="72.0" y="104" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><text x="100.0" y="104" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text><text x="128.0" y="104" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text><text x="44.0" y="132" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><text x="72.0" y="132" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><text x="100.0" y="132" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><text x="128.0" y="132" fill="#e6edf3" font-size="12" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text><rect x="30" y="30" width="56" height="56" fill="none" stroke="#e0a458" stroke-width="2"/><rect x="86" y="30" width="56" height="56" fill="none" stroke="#e0a458" stroke-width="2"/><rect x="30" y="86" width="56" height="56" fill="none" stroke="#e0a458" stroke-width="2"/><rect x="86" y="86" width="56" height="56" fill="none" stroke="#e0a458" stroke-width="2"/><line x1="158" y1="86" x2="196" y2="86" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="200" y="58" width="28" height="28" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.5"/><rect x="228" y="58" width="28" height="28" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.5"/><rect x="200" y="86" width="28" height="28" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.5"/><rect x="228" y="86" width="28" height="28" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.5"/><text x="200" y="51" fill="#8b949e" font-size="11.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出 2×2</text><text x="214.0" y="76" fill="#e0a458" font-size="13" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text><text x="242.0" y="76" fill="#e0a458" font-size="13" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><text x="214.0" y="104" fill="#e0a458" font-size="13" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><text x="242.0" y="104" fill="#e0a458" font-size="13" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text><rect x="310" y="34" width="300" height="58" rx="7" fill="none" stroke="#58a6ff" stroke-width="1.6"/><text x="460.0" y="59.0" fill="#e6edf3" font-size="14" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">面積 ÷ 4、參數 0 個</text><text x="460.0" y="76.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">鄰域內平移，輸出可能不變</text><text x="310" y="128" fill="#8b949e" font-size="11.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">代價：只知道「這區有」，不知道在哪個像素</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">最大池化：2×2 取最大，面積變四分之一，而且沒有參數可學。</figcaption>
</figure>
<!-- /CNN2-FIGURE:pool -->

兩種最常見：**最大池化**與**平均池化**。好處是降維與空間不變；代價是**放棄精確的空間位置**。

- padding 可以是 `SAME` 或 `VALID`，輸出尺寸不同。
- 張量順序是 `[batch, height, width, channels]`。
- 池化**沒有可學習參數**，反向傳播時只把梯度「路由」回最大值的位置。

## 8. 空洞卷積（dilated convolution）

在濾波器元素之間插入 `d − 1` 個洞，等效核變成 `k_eff = k + (k − 1)(d − 1)`，**參數數量不變**、
感受野變大。語意分割（DeepLab 系列）特別愛用：要保留解析度、又需要全域資訊。

## 9. 從特徵到類別機率

**CONV + POOL 輸出高階特徵，全連接層用它做分類，輸出表示為「屬於某一類的機率」**：

```
ŷ_i = exp(z_i) / Σ_j exp(z_j)
```

實作上的小選擇：one-hot 標籤配 `categorical_crossentropy`，整數標籤配
`sparse_categorical_crossentropy`（本筆記的腳本用後者，省記憶體）。

## 10. 把模型組起來（含三個必改的錯）

```python
import tensorflow as tf

def generate_model(input_shape=(28, 28, 1), n_classes=10):
    return tf.keras.Sequential([
        tf.keras.Input(shape=input_shape),
        tf.keras.layers.Conv2D(32, kernel_size=3, activation="relu"),
        tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
        tf.keras.layers.Conv2D(64, kernel_size=3, activation="relu"),
        tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(1024, activation="relu"),
        tf.keras.layers.Dense(n_classes, activation="softmax"),
    ])
```

課程印出來的版本有三個地方會**直接報錯**：

| # | 寫法 | 問題 | 改法 |
|---|---|---|---|
| 1 | `activation='relu’` | 彎引號（U+2019）不是合法字串引號 → `SyntaxError` | 改直引號 `"relu"` |
| 2 | `Conv2D(32, filter_size=3, ...)` | Keras 沒有 `filter_size` | `kernel_size=3` |
| 3 | `Sequential([Conv2D(...)])` 直接開頭 | Keras 3 要求先知道輸入形狀 | 加 `tf.keras.Input(shape=...)` |

`MaxPool2D` 是 `MaxPooling2D` 的別名，可照用；`Dense(1024)` 對 10 類偏大
（佔全模型 98.9% 參數），實務上會加 dropout 或縮小。

實測層形狀（MNIST，28×28×1）：

| 層 | 輸出形狀 | 參數 |
|---|---|---|
| Conv2D(32, 3×3) | (None, 26, 26, 32) | 320 |
| MaxPool2D(2, 2) | (None, 13, 13, 32) | 0 |
| Conv2D(64, 3×3) | (None, 11, 11, 64) | 18,496 |
| MaxPool2D(2, 2) | (None, 5, 5, 64) | 0 |
| Flatten | (None, 1600) | 0 |
| Dense(1024) | (None, 1024) | 1,639,424 |
| Dense(10, softmax) | (None, 10) | 10,250 |
| **合計** | | **1,668,490** |

<!-- CNN2-FIGURE:params -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 250" role="img" aria-label="參數量分佈：1,668,490 個參數中 Dense(1024) 佔 1,639,424（98.2%），Conv 層共 18,816（1.1%），輸出層 10,250（0.6%）"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect fill="#0d1117"/><text x="40" y="30" fill="#e0a458" font-size="13" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1,668,490 個參數，98.2% 集中在 Flatten 之後</text><rect x="40.00" y="56" width="805.72" height="44" rx="3" fill="#e0a458" opacity="0.85"/><rect x="845.72" y="56" width="9.25" height="44" rx="0" fill="#4ecdc4" opacity="0.85"/><rect x="854.96" y="56" width="5.04" height="44" rx="0" fill="#58a6ff" opacity="0.85"/><rect x="40" y="56" width="820" height="44" rx="1" fill="none" stroke="#8b949e" stroke-width="0.8" opacity="0.5"/><rect x="40" y="138" width="12" height="12" rx="3" fill="#e0a458" opacity="0.85"/><text x="62" y="148" fill="#e6edf3" font-size="12.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Dense(1024)  1,639,424（98.2%）</text><rect x="40" y="168" width="12" height="12" rx="3" fill="#4ecdc4" opacity="0.85"/><text x="62" y="178" fill="#e6edf3" font-size="12.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Conv 32 + Conv 64  18,816（1.1%）</text><rect x="40" y="198" width="12" height="12" rx="3" fill="#58a6ff" opacity="0.85"/><text x="62" y="208" fill="#e6edf3" font-size="12.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Dense(10, softmax)  10,250（0.6%）</text><text x="40" y="238" fill="#8b949e" font-size="11.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">MaxPool / Flatten：0 個參數</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">參數量分佈：98.2% 集中在 Flatten 之後的 Dense(1024)，卷積層本身只佔 1.1%。</figcaption>
</figure>
<!-- /CNN2-FIGURE:params -->

- 參數**九成八集中在攤平後的全連接層**——這就是「全連接參數爆炸」的實證。
- 換成 CIFAR-10（32×32×3）同架構：攤平後 6×6×64 = 2304 維，總參數 2,389,962。

## 11. 應用版圖：一個架構，換一個頭

<!-- CNN2-FIGURE:tasks -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 470 220" role="img" aria-label="同一個卷積 backbone 接四種任務頭：分類、分割、上色、控制"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect fill="#0d1117"/><rect x="24" y="64" width="150" height="62" rx="7" fill="none" stroke="#4ecdc4" stroke-width="1.6"/><text x="99.0" y="91.0" fill="#e6edf3" font-size="12.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">卷積 backbone</text><text x="99.0" y="108.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一組特徵抽取器</text><line x1="178" y1="95" x2="216" y2="31.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="220" y="12" width="190" height="38" rx="7" fill="none" stroke="#e0a458" stroke-width="1.6"/><text x="315.0" y="27.0" fill="#e6edf3" font-size="11.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">分類 head</text><text x="315.0" y="44.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全連接 + softmax</text><line x1="178" y1="95" x2="216" y2="77.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="220" y="58" width="190" height="38" rx="7" fill="none" stroke="#58a6ff" stroke-width="1.6"/><text x="315.0" y="73.0" fill="#e6edf3" font-size="11.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">分割 head</text><text x="315.0" y="90.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全卷積 + 轉置卷積</text><line x1="178" y1="95" x2="216" y2="123.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="220" y="104" width="190" height="38" rx="7" fill="none" stroke="#e0a458" stroke-width="1.6"/><text x="315.0" y="119.0" fill="#e6edf3" font-size="11.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">上色 head</text><text x="315.0" y="136.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2 個色度通道</text><line x1="178" y1="95" x2="216" y2="169.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#a)"/><rect x="220" y="150" width="190" height="38" rx="7" fill="none" stroke="#58a6ff" stroke-width="1.6"/><text x="315.0" y="165.0" fill="#e6edf3" font-size="11.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">控制 head</text><text x="315.0" y="182.0" fill="#8b949e" font-size="10.5" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">方向盤、油門</text><text x="24" y="210" fill="#8b949e" font-size="11.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">換頭就換任務：分割、上色、超解析、端到端控制都是這樣組出來的</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">同一個 backbone、換一個頭，就是另一個任務。</figcaption>
</figure>
<!-- /CNN2-FIGURE:tasks -->

| 任務 | 頭長什麼樣 | 課程的例子 |
|---|---|---|
| 分類 | 全連接 + softmax | 影像分類 |
| 偵測 | 邊界框 + 類別 | 人臉偵測、自駕 |
| 語意分割 | **全卷積**，輸出同尺寸 | FCN、腦腫瘤、瘧疾 |
| 逐像素回歸 | 輸出 2 個色度通道 | 黑白上色 |
| 影像到影像 | 卷積 + 轉置卷積 | 超解析、後製優化 |
| 端到端控制 | 回歸方向盤與油門 | 自動駕駛 |

- **FCN** 拿掉全連接，才能輸出「跟輸入一樣大」的標籤圖；上採樣用 `Conv2DTranspose`。
- **自駕**的輸入是相機 + GPS，輸出是控制指令，**端到端訓練、不需人手標註**。
- **醫療**除了分割圖還輸出**不確定性圖**：不只要答案，還要說出哪裡不確定。
- **DeepBind** 把 DNA 序列當一維影像卷積，說明局部模式 + 權重共享不限於影像。

## 12. 實測：六組設定、三個平台

完整紀錄（33 組 run、跨平台配對、五個被逐項測掉的假設）在
[CNN II 實驗紀錄：33 組 run、三個平台，把 0.80 推到 0.96](/2026/10/29/cnn-2-experiments/)；這裡只留結論。

| 設定 | CIFAR-10 測試準確率 |
|---|---|
| 課程的架構（20 輪） | 0.80 |
| 加上 dropout 0.3 | 0.81 |
| 換成小型 VGG（6 層卷積 + BN） | 0.89 |
| 小型 VGG + cutout，200 輪 | 0.94 |
| **ResNet-18 + cutout，200 輪** | **0.96** |

<!-- CNN2-FIGURE:accuracy -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 300" role="img" aria-label="CIFAR-10 準確率階梯：課程架構 0.80、加 dropout 0.81、小型 VGG 0.89、VGG+cutout 0.94、ResNet-18+cutout 0.96"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect fill="#0d1117"/><text x="30" y="30" fill="#e0a458" font-size="13" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一份資料：換架構與排程，0.80 → 0.96</text><line x1="210.0" y1="52" x2="210.0" y2="262" stroke="#8b949e" stroke-width="0.8" opacity="0.22"/><text x="210.0" y="284" fill="#8b949e" font-size="11" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.70</text><line x1="426.7" y1="52" x2="426.7" y2="262" stroke="#8b949e" stroke-width="0.8" opacity="0.22"/><text x="426.66666666666686" y="284" fill="#8b949e" font-size="11" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.80</text><line x1="643.3" y1="52" x2="643.3" y2="262" stroke="#8b949e" stroke-width="0.8" opacity="0.22"/><text x="643.3333333333334" y="284" fill="#8b949e" font-size="11" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.90</text><line x1="860.0" y1="52" x2="860.0" y2="262" stroke="#8b949e" stroke-width="0.8" opacity="0.22"/><text x="860.0" y="284" fill="#8b949e" font-size="11" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.00</text><rect x="210" y="67" width="216.7" height="22" rx="4" fill="#4ecdc4" opacity="0.85"/><text x="198" y="82" fill="#e6edf3" font-size="11.5" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">課程的架構（20 輪）</text><text x="436.66666666666686" y="82" fill="#4ecdc4" font-size="12.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.80</text><rect x="210" y="107" width="238.3" height="22" rx="4" fill="#4ecdc4" opacity="0.85"/><text x="198" y="122" fill="#e6edf3" font-size="11.5" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">加上 dropout 0.3</text><text x="458.3333333333335" y="122" fill="#4ecdc4" font-size="12.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.81</text><rect x="210" y="147" width="411.7" height="22" rx="4" fill="#e0a458" opacity="0.85"/><text x="198" y="162" fill="#e6edf3" font-size="11.5" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">小型 VGG（6 層卷積 + BN）</text><text x="631.6666666666667" y="162" fill="#e0a458" font-size="12.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.89</text><rect x="210" y="187" width="520.0" height="22" rx="4" fill="#e0a458" opacity="0.85"/><text x="198" y="202" fill="#e6edf3" font-size="11.5" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">VGG + cutout（200 輪）</text><text x="739.9999999999999" y="202" fill="#e0a458" font-size="12.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.94</text><rect x="210" y="227" width="563.3" height="22" rx="4" fill="#ff7b72" opacity="0.85"/><text x="198" y="242" fill="#e6edf3" font-size="11.5" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ResNet-18 + cutout（200 輪）</text><text x="783.3333333333333" y="242" fill="#ff7b72" font-size="12.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.96</text><line x1="210" y1="52" x2="210" y2="262" stroke="#8b949e" stroke-width="1"/><text x="30" y="284" fill="#8b949e" font-size="10.5" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">橫軸從 0.70 起</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">六組設定的 CIFAR-10 測試準確率；換架構與長排程把 0.80 推到 0.96（橫軸從 0.70 起）。</figcaption>
</figure>
<!-- /CNN2-FIGURE:accuracy -->

1. **課程的模型 20 輪上限約 0.80**；換成有 BatchNorm 與 `padding="same"` 的 VGG 立刻多 9 個百分點
   ——關鍵是深度與歸一化，不是參數量（VGG 參數反而更少）。
2. **200 輪長排程拉到 0.96**，最後 30 輪的學習率收尾貢獻 2–4 個百分點。
3. **難類排序完全沒變**：貓 < 狗 < 鳥 → 難度來自資料，不是訓練技巧。

環境上的順帶結論：TensorFlow 在 Windows 拿不到 GPU（2.11 起沒有原生 CUDA），GPU 那幾組用 PyTorch；
同一份程式搬到 Linux 的 TensorFlow 上，數字落在 ±2 pp 內。

## 附錄 A：名詞速查

| 英文 | 中文 | 一句話 |
|---|---|---|
| convolution | 卷積 | 濾波器滑過輸入做加權和 |
| filter / kernel | 濾波器／卷積核 | 可學習的權重小矩陣 |
| feature map | 特徵圖 | 一個濾波器的輸出 |
| stride | 步幅 | 濾波器每次移動的格數 |
| padding（SAME／VALID） | 填充 | SAME 保住尺寸、VALID 不填充 |
| receptive field | 感受野 | 節點在輸入上看到的區域 |
| pooling | 池化 | 鄰域取最大或平均，降維 |
| dilation | 空洞率 | 濾波器元素之間插入間隔 |
| de novo feature learning | 從零學特徵 | 特徵是訓練出來的，不是人工設計 |
| dying ReLU | ReLU 死亡 | 單元恆輸出 0、梯度恆 0 |

## 附錄 B：常見陷阱

| 陷阱 | 正確說法 |
|---|---|
| 「depth 由輸入通道決定」 | 由**濾波器數量**決定；輸入通道只影響每個濾波器的深度 |
| 「池化是為了學特徵」 | 池化沒有參數，只降維與提供空間不變性 |
| 「ReLU 一半是 0 就是死了」 | 那是稀疏；死亡要看「對所有輸入都輸出 0」 |
| 「參數越多越準」 | 對照實驗裡參數更少的 VGG 反而高 9 個百分點 |
| 「卷積就是數學上的卷積」 | 實務用的是互相關（核不翻轉），對學出來的核沒差別 |
| 「20 輪沒進步就是到頂」 | 通常只是學習率還沒收尾 |

## 附錄 C：一頁精華（考前 10 分鐘）

1. 分類三步曲：**卷積 → 非線性 → 池化**，權重只在卷積與全連接層。
2. `O = (N + 2P − F)/S + 1`；`d` 是濾波器數量。
3. 池化：無參數、降維、空間不變、放棄精確位置。
4. ReLU：`max(0, x)`；死亡 = 梯度恆 0。
5. 參數九成八在攤平後的全連接層。
6. FCN 用 `Conv2DTranspose` 上採樣，才能輸出同尺寸標籤圖。
7. 難類排序（貓 < 狗 < 鳥）在四種設定下都一樣。

## 附錄 D：互動測驗（60 題）

> **60 題單選、滿分 60 分、建議 60 分鐘。**
> 測驗以**互動網頁**形式提供（點選即時計分、進度自動儲存）；本筆記**不重複收錄題目**。

**👉 [開始 60 題線上測驗](mc-quiz.html)**

線上版功能：

- **點選答案**即自動計分，並即時顯示得分
- **作答進度自動存在你的瀏覽器**（localStorage）—— 關掉網頁、隔天再開都能繼續
- 可切換「只顯示未答」或「只顯示答錯」的題目，快速複習
- 按「顯示答案」才揭曉正解與解析，不會一開始就被暴雷

| 分數 | 程度 | 建議 |
|---|---|---|
| 54–60 | 優異 | 直接看附錄 C 一頁精華即可上場 |
| 45–53 | 良好 | 複習錯題所屬章節 |
| 36–44 | 及格邊緣 | 重讀主要章節 + 附錄 A |
| 0–35 | 需加強 | 整份筆記重讀一遍，再重做本卷 |

*本篇為個人學習筆記整理，課程內容版權屬匯縱專業發展中心（IVDC）所有。*

