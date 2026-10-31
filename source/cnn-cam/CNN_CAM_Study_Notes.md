# CAM：用 GAP 把「模型在看哪裡」算出來

> 系列第七篇。上一篇（[GAP 是什麼](/cnn-gap-head/)）講 GAP 怎麼把特徵圖壓成一個數；這一篇講它附帶的一個禮物：<br /><strong>因為 GAP 把「一張特徵圖」對應到「一個數」，分類層的權重就可以直接乘回那張圖，變成一張熱圖。</strong><br />這就是 CAM（Class Activation Mapping）：<strong>訊號一路線性，所以「分類權重」與「空間位置」可以相乘。</strong><br />所有數字都是本機用 NumPy 算的（Python 3.15.1 / NumPy 2.5.4），原始輸出在附錄 G。

<!-- CNCM-FIGURE:cam-pipeline -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" role="img" aria-label="CAM 的網路結構：卷積到 K 張 7×7 特徵圖，GAP 成 K 個數，最後 Linear(K→C) 的權重 w 再回頭加權那 K 張圖，得到類別熱圖"><defs><marker id="arc" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="358.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">CAM 的網路結構：GAP 是那座橋</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只有「GAP + Linear」的頭，才能讓分類權重乾淨地對應回單一張特徵圖</text><rect x="40" y="104" width="110" height="62" rx="8" fill="#12181f" stroke="#4ecdc4aa" stroke-width="1.4"/><text x="95.0" y="130" font-size="11.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">影像</text><text x="95.0" y="151.0" font-size="9.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">224×224×3</text><line x1="154" y1="135" x2="186" y2="135" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="190" y="104" width="120" height="62" rx="8" fill="#12181f" stroke="#4ecdc4aa" stroke-width="1.4"/><text x="250.0" y="130" font-size="11.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">卷積堆疊</text><text x="250.0" y="151.0" font-size="9.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 7×7×K</text><line x1="314" y1="135" x2="346" y2="135" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="350" y="96" width="150" height="140" rx="10" fill="#12181f" stroke="#58a6ff99" stroke-width="1.4"/><text x="425" y="120" font-size="10.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">最後一層特徵圖</text><rect x="366" y="132" width="118" height="96" rx="5" fill="none" stroke="#58a6ff66" stroke-width="1.1"/><rect x="374" y="138" width="118" height="96" rx="5" fill="none" stroke="#58a6ff66" stroke-width="1.1"/><rect x="382" y="144" width="118" height="96" rx="5" fill="none" stroke="#58a6ff66" stroke-width="1.1"/><text x="425" y="226" font-size="10" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">A₁ … A_K（各 7×7）</text><line x1="504" y1="166" x2="536" y2="166" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="540" y="132" width="110" height="68" rx="8" fill="#12181f" stroke="#e0a458aa" stroke-width="1.4"/><text x="595.0" y="158" font-size="11.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GAP</text><text x="595.0" y="182.0" font-size="9.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">K 個數</text><line x1="654" y1="166" x2="686" y2="166" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="690" y="132" width="130" height="68" rx="8" fill="#12181f" stroke="#e0a458aa" stroke-width="1.4"/><text x="755.0" y="158" font-size="11.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Linear</text><text x="755.0" y="182.0" font-size="9.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">K → C</text><line x1="824" y1="166" x2="856" y2="166" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="860" y="132" width="110" height="68" rx="8" fill="#12181f" stroke="#ff7b72aa" stroke-width="1.4"/><text x="915.0" y="158" font-size="11.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">softmax</text><text x="915.0" y="182.0" font-size="9.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">C 個機率</text><path d="M 755 206 C 755 268, 425 268, 425 240" fill="none" stroke="#c084fc" stroke-width="1.6" stroke-dasharray="6 4" marker-end="url(#arc)"/><text x="590" y="292" font-size="11.5" fill="#c084fc" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">w[k, c] 回頭加權每張 A_k</text><text x="40" y="330" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">CAM_k(x, y) = Σ_k w[k, c] · A_k(x, y)；再上採樣回 224×224 就是熱圖。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">CAM 的橋樑就是 GAP：每個 F_k 只對應一張 A_k，所以線性層的權重 w 可以直接乘回 A_k。</figcaption>
</figure>
<!-- /CNCM-FIGURE:cam-pipeline -->

## 1. 一句話：GAP 是那座橋

```text
CAM_c(x, y) = Σ_k w[k, c] · A_k(x, y)
```

- `A_k`：最後一層卷積的第 `k` 張特徵圖（`H × W`）
- `w[k, c]`：分類層裡「第 `k` 個通道對類別 `c`」的權重
- `CAM_c`：一張 `H × W` 的熱圖，值越大代表那個位置越支持類別 `c`

關鍵在於 `w[k, c]` 這個權重**只綁一個通道**，不是綁某個像素。這件事只有 GAP 之後才成立。

## 2. 網路結構的要求

CAM 原版要求的末端長這樣：

```text
影像 → 卷積層 → 最後一層特徵圖 H × W × K
     → GAP → K 個數
     → Linear(K → C)
     → Softmax → C 個機率
```

| 符號 | 意思 | 典型值 |
|---|---|---|
| `K` | 最後一層卷積的通道數 | 512 或 1024 |
| `C` | 類別數 | 1,000 |
| `H × W` | 特徵圖的空間尺寸 | 7 × 7（224 輸入、32 倍降採樣） |

`K` 這個數字很關鍵：它同時是「GAP 輸出向量的長度」與「熱圖要疊的張數」。`C` 則是分類層的列數——所以分類權重矩陣是 `K × C`，每一**列**就是一個類別對所有通道的重視程度。

## 3. 數學關係：logit 就是 CAM 的平均

分類層對類別 `c` 的 logit：

```text
y_c = Σ_k w[k, c] · F_k + b_c          F_k = GAP(A_k) = (1 / H·W) Σ_x Σ_y A_k(x, y)
```

把 `F_k` 展開：

```text
y_c = Σ_k w[k, c] · (1 / H·W) ΣΣ A_k(x, y) + b_c
    = (1 / H·W) ΣΣ ( Σ_k w[k, c] · A_k(x, y) ) + b_c
    = (1 / H·W) ΣΣ CAM_c(x, y) + b_c
```

也就是：

```text
mean(CAM_c) = y_c − b_c
```

**類別分數＝熱圖的空間平均（再平移 bias）**。這正是 CAM 能「定位」的原因：把一個純量拆成每個位置的貢獻。

實測兩次：

| 情況 | 結果 |
|---|---|
| 手算例子（3 張 2×2） | logit 3.9，mean(CAM) 3.9 ✓ |
| 隨機網路（K=6、7×7、C=4） | 四類的 logit 與 mean(CAM) **最大差 4.44e-16** |

有 bias 時要記得扣掉：`bias = 0.5` → logit 4.40、mean(CAM) 3.90 = logit − bias ✓。所以嚴格說是「logit 減 bias 等於 CAM 平均」，而 bias 不影響熱圖的形狀。

## 4. 手算一個 CAM

<!-- CNCM-FIGURE:cam-worked -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 400" role="img" aria-label="三張 2×2 特徵圖與權重 0.8、0.1、負 0.2 加權相加，得到 CAM 8.1、負 0.3、6.5、1.3，平均 3.9 正好等於該類別的 logit"><defs><marker id="arc" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="398.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">手算一個 CAM：三張 2×2 特徵圖</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">權重 0.8 / 0.1 / −0.2；GAP 之後是 5 / 1 / 1，logit = 3.9</text><text x="50" y="112" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">A1</text><rect x="50" y="122" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="76.0" y="152.68" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10</text><rect x="102" y="122" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="128.0" y="152.68" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="50" y="174" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="76.0" y="204.68" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text><rect x="102" y="174" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="128.0" y="204.68" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><text x="102" y="262" font-size="13" fill="#4ecdc4" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">× 0.8</text><text x="102" y="286" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">F₁ = 5</text><text x="218" y="112" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">A2</text><rect x="218" y="122" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="244.0" y="152.68" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="270" y="122" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="296.0" y="152.68" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="218" y="174" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="244.0" y="204.68" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="270" y="174" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="296.0" y="204.68" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><text x="270" y="262" font-size="13" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">× 0.1</text><text x="270" y="286" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">F₂ = 1</text><text x="386" y="112" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">A3</text><rect x="386" y="122" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="412.0" y="152.68" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="438" y="122" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="464.0" y="152.68" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><rect x="386" y="174" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="412.0" y="204.68" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="438" y="174" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="464.0" y="204.68" font-size="13" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><text x="438" y="262" font-size="13" fill="#c084fc" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">× −0.2</text><text x="438" y="286" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">F₃ = 1</text><line x1="556" y1="196" x2="592" y2="196" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><text x="574" y="176" font-size="10.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">加權相加</text><text x="640" y="112" font-size="12" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">CAM（狗）</text><rect x="588" y="122" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="614.0" y="152.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8.1</text><rect x="640" y="122" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="666.0" y="152.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-0.3</text><rect x="588" y="174" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="614.0" y="204.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6.5</text><rect x="640" y="174" width="52" height="52" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="666.0" y="204.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.3</text><text x="640" y="262" font-size="12" fill="#e0a458" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">平均 = 15.6 / 4 = 3.9</text><text x="640" y="286" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">= 該類別的 logit</text><rect x="50" y="318" width="890" height="66" rx="12" fill="#1c2230" stroke="#4ecdc455" stroke-width="1.4"/><text x="70" y="344" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">logit = 0.8×5 + 0.1×1 + (−0.2)×1 = 3.9，而 CAM 的四格平均也是 3.9——這就是 GAP 給的橋。</text><text x="70" y="368" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">左上角 8.1 最大：模型認為那個位置最支持「狗」。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">手算例子：三張 2×2 特徵圖加權相加成 CAM，四個位置 8.1 / −0.3 / 6.5 / 1.3，平均剛好是 logit 3.9。</figcaption>
</figure>
<!-- /CNCM-FIGURE:cam-worked -->

三張 2×2 的特徵圖，權重 `0.8 / 0.1 / −0.2`：

```text
A₁ = [[10, 0], [8, 2]]      F₁ = 5
A₂ = [[1, 1], [1, 1]]       F₂ = 1
A₃ = [[0, 2], [0, 2]]       F₃ = 1

logit = 0.8×5 + 0.1×1 + (−0.2)×1 = 3.9
```

逐位置加權相加：

```text
CAM = 0.8·A₁ + 0.1·A₂ − 0.2·A₃
    = [[8.1,  −0.3],
       [6.5,   1.3]]
```

驗算兩格：

```text
左上 (1,1) = 0.8(10) + 0.1(1) − 0.2(0) = 8.1
右上 (1,2) = 0.8(0)  + 0.1(1) − 0.2(2) = −0.3
```

四格平均 `(8.1 − 0.3 + 6.5 + 1.3) / 4 = 3.9` —— 正好是 logit。

模型會說「左上角最支持狗」（8.1 最大），「右上角反對」（−0.3 最小）。**負值不是 bug**：它代表那個位置的特徵組合對這個類別是負貢獻。

## 5. 五個步驟

<!-- CNCM-FIGURE:cam-steps -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 390" role="img" aria-label="CAM 的五個步驟：取出最後一層特徵圖、GAP、讀線性層權重、加權相加、上採樣回原圖尺寸"><defs><marker id="arc" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="388.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">五個步驟，只有最後一步是為了「看」</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">前四步都是線性運算；上採樣只是把 7×7 放大到看得出來的尺寸</text><rect x="44" y="120" width="160" height="110" rx="10" fill="#12181f" stroke="#4ecdc488" stroke-width="1.5"/><circle cx="74" cy="146" r="15" fill="#4ecdc4"/><text x="74" y="152" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><text x="100" y="152" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">取特徵圖</text><text x="62" y="196" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">A₁…A_K，7×7</text><line x1="207" y1="175" x2="226" y2="175" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="230" y="120" width="160" height="110" rx="10" fill="#12181f" stroke="#e0a45888" stroke-width="1.5"/><circle cx="260" cy="146" r="15" fill="#e0a458"/><text x="260" y="152" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><text x="286" y="152" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GAP</text><text x="248" y="196" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">F₁…F_K，K 個數</text><line x1="393" y1="175" x2="412" y2="175" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="416" y="120" width="160" height="110" rx="10" fill="#12181f" stroke="#58a6ff88" stroke-width="1.5"/><circle cx="446" cy="146" r="15" fill="#58a6ff"/><text x="446" y="152" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><text x="472" y="152" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">讀權重</text><text x="434" y="196" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">w[k, c]，K 個</text><line x1="579" y1="175" x2="598" y2="175" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="602" y="120" width="160" height="110" rx="10" fill="#12181f" stroke="#c084fc88" stroke-width="1.5"/><circle cx="632" cy="146" r="15" fill="#c084fc"/><text x="632" y="152" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text><text x="658" y="152" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">加權相加</text><text x="620" y="196" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">CAM，7×7</text><line x1="765" y1="175" x2="784" y2="175" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="788" y="120" width="160" height="110" rx="10" fill="#12181f" stroke="#ff7b7288" stroke-width="1.5"/><circle cx="818" cy="146" r="15" fill="#ff7b72"/><text x="818" y="152" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text><text x="844" y="152" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">上採樣</text><text x="806" y="196" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">224×224 熱圖</text><rect x="44" y="268" width="912" height="96" rx="12" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.4"/><text x="64" y="296" font-size="12" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">為什麼第 3 步需要 GAP：F_k 只對應一張 A_k，所以 w[k, c] 可以直接乘回 A_k。</text><text x="64" y="322" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">若換成 Flatten + 大 FC，每個權重綁的是「某個像素 × 某個通道」，無法還原成一張圖。</text><text x="64" y="346" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">實測：K=6、7×7、C=4 時，GAP 頭 6 個權重 vs 展平頭 1,176 個（196 倍）。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">五個步驟裡只有第 5 步（上採樣）是為了「看得出來」；前四步都是純線性運算。</figcaption>
</figure>
<!-- /CNCM-FIGURE:cam-steps -->

1. **前向傳播**，把最後一層卷積的 `A_1 … A_K` 留下來（`7 × 7 × K`）。
2. **GAP**：每張壓成一個數，得到 `F_1 … F_K`。
3. **讀權重**：從 `Linear(K → C)` 取出目標類別那一列的 `w[1, c] … w[K, c]`。
4. **加權相加**：`CAM_c = Σ_k w[k, c] · A_k`，得到一張 `7 × 7`。
5. **上採樣**回 `224 × 224`，疊到原圖上。

第 5 步只是為了「看得出來」：`7×7` 的熱圖直接看是一格一格的，所以用雙線性插值放大 32 倍。放大不會產生新資訊——它只是把 49 個數字攤開。

## 6. 為什麼一定要 GAP

| 末端 | 一列權重綁的是什麼 | 能不能變成熱圖 |
|---|---|---|
| GAP + `Linear(K → C)` | 一個**通道**（一張特徵圖） | 可以，`w[k, c]` 直接乘 `A_k` |
| Flatten + `Linear(H·W·K → C)` | 一個**像素 × 通道** | 不行，權重散在 `H×W` 個位置上，無法還原成一張圖 |

實測規模差距（`K = 6`、`7×7`、`C = 4`）：

```text
GAP 頭     : 6 個權重      （每通道每類別一個）
Flatten 頭 : 1,176 個權重  （每像素每通道每類別一個）→ 196 倍
```

而且那 1,176 個權重**結構上就不對應任何一張特徵圖**——這不是「比較難算」，是「定義上做不到」。所以傳統 CAM 要求模型末端必須有 GAP；既有模型若沒有，就得改架構重訓。

## 7. Grad-CAM：用梯度取代權重

<!-- CNCM-FIGURE:gradcam -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 420" role="img" aria-label="CAM 與 Grad-CAM 的差別：CAM 用 GAP 之後的線性權重，Grad-CAM 用 logit 對特徵圖的梯度平均；在純 GAP＋Linear 的網路上兩者只差一個常數與 ReLU"><defs><marker id="arc" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="418.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">CAM vs Grad-CAM</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一個用「線性層的權重」，一個用「梯度」；後者不必有 GAP</text><rect x="30" y="96" width="460" height="220" rx="12" fill="#12181f" stroke="#4ecdc477" stroke-width="1.4" opacity="0.6"/><text x="50" y="124" font-size="12.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">CAM（原版）</text><text x="50" y="152" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">w[k, c]：GAP 後線性層的權重</text><text x="50" y="178" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">要求：末端必須是 GAP + Linear</text><text x="50" y="204" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">優點：一次前向就能算、可解釋性強</text><text x="50" y="230" font-size="11.5" fill="#ff7b72" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">缺點：既有模型要改架構重訓</text><text x="50" y="264" font-size="12" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">CAM_c = Σ_k w[k,c] · A_k</text><text x="50" y="290" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">（本頁手算例子：8.1 / −0.3 / 6.5 / 1.3）</text><rect x="510" y="96" width="460" height="220" rx="12" fill="#12181f" stroke="#c084fc77" stroke-width="1.4" opacity="0.6"/><text x="530" y="124" font-size="12.5" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Grad-CAM（2017）</text><text x="530" y="152" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">α[k, c] = (1/HW) ΣΣ ∂y_c/∂A_k</text><text x="530" y="178" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">要求：只要能算梯度（幾乎所有 CNN）</text><text x="530" y="204" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">優點：不必改架構、可套用既有模型</text><text x="530" y="230" font-size="11.5" fill="#e0a458" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">缺點：要多一次反向傳播</text><text x="530" y="264" font-size="12" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">M_c = ReLU( Σ_k α[k,c] · A_k )</text><text x="530" y="290" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ReLU 是因為我們只關心「支持」的證據</text><rect x="30" y="330" width="940" height="74" rx="12" fill="#1c2230" stroke="#e0a45855" stroke-width="1.4"/><text x="50" y="356" font-size="12" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">實測（純 GAP + Linear 的網路）：α = w / (H·W)，於是 Grad-CAM = ReLU(CAM / (H·W))。</text><text x="50" y="382" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">最大差 5.64e-18 —— 在這種架構上，兩張圖其實是同一張。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">Grad-CAM 用梯度取代權重，所以不必有 GAP；但在純 GAP＋Linear 的網路上，兩者算出來是同一張圖。</figcaption>
</figure>
<!-- /CNCM-FIGURE:gradcam -->

```text
α[k, c] = (1 / H·W) ΣΣ ∂y_c / ∂A_k(x, y)          每張特徵圖的平均梯度
M_c     = ReLU( Σ_k α[k, c] · A_k )               熱圖（只保留正貢獻）
```

| 項目 | 原始 CAM | Grad-CAM |
|---|---|---|
| 需要 GAP | 必須 | 不需要 |
| 權重來源 | `Linear` 層的 `w[k, c]` | logit 對 `A_k` 的梯度平均 |
| 架構限制 | 要改末端並重訓 | 幾乎任何 CNN 都能用 |
| 額外成本 | 一次前向 | 前向 + 一次反向 |

**一個可以實測的關係**：如果網路真的是「GAP + Linear」，那

```text
∂y_c / ∂A_k(x, y) = w[k, c] / (H·W)      （對位置是常數）
α[k, c]           = w[k, c] / (H·W)
M_c               = ReLU( CAM_c / (H·W) )
```

實測（K=6、7×7、C=4）：`α` 與 `w/(H·W)` 完全相等，`M_c` 與 `ReLU(CAM/(H·W))` 的最大差 **5.64e-18**。

也就是說：**在純 GAP + Linear 的網路上，Grad-CAM 與 CAM 是同一張圖**（差一個正規化常數和 ReLU）。只有在中間插了其他層（ReLU、BN、再多一層卷積）之後，梯度才會與權重分道揚鑣——那時 Grad-CAM 仍然可用，CAM 就不行了。

## 8. 實務上的六個注意

| 注意 | 為什麼 |
|---|---|
| 只反映**最後一層** | 熱圖解析度 = 最後特徵圖的解析度（`224 → 7×7`，放大 32 倍） |
| 上採樣用雙線性 | 最近鄰會出現方塊；雙線性比較平滑，但也更「模糊」 |
| 負值要處理 | 顯示時通常 `ReLU` 或做 min-max 正規化，否則色階被負值吃掉 |
| 多類別要逐類算 | CAM 是「一個類別一張圖」，不是一張通用圖 |
| bias 不影響形狀 | `mean(CAM) = logit − bias`，bias 只是整體平移 |
| 熱圖不是因果 | 高值只代表「這裡的證據支持該類」，不代表模型「用了」它 |

## 9. 六個常見誤解

| 誤解 | 事實 |
|---|---|
| CAM 需要額外訓練一個模型 | 不用，它只是把既有權重乘回特徵圖 |
| CAM 可以用在任何 CNN | 原版不行，必須末端是 GAP + Linear（Grad-CAM 才通用） |
| 熱圖數值加起來等於 logit | 是**平均**等於 logit − bias，不是總和 |
| 熱圖越大代表越準 | 它只反映「模型看哪裡」，不代表答案對；模型可能看錯地方還答對 |
| 上採樣可以恢復細節 | 不能，`7×7` 就只有 49 個值 |
| Grad-CAM 一定比 CAM 好 | 在 GAP + Linear 的網路上兩者等價；Grad-CAM 的價值是「通用」 |

## 附錄 A 速查表

| 想問的事 | 答案 |
|---|---|
| CAM 公式 | `Σ_k w[k,c] · A_k(x,y)` |
| 需要的架構 | 卷積 → GAP → `Linear(K → C)` → softmax |
| 熱圖尺寸 | 最後特徵圖的 `H × W`，再上採樣 |
| 與 logit 的關係 | `mean(CAM_c) = y_c − b_c` |
| 權重從哪拿 | `Linear` 的權重矩陣，第 `c` 列 |
| Grad-CAM 的權重 | `α[k,c] = mean(∂y_c/∂A_k)` |
| 純 GAP + Linear 時 | `Grad-CAM = ReLU(CAM / (H·W))`（實測差 5.64e-18） |
| Flatten 頭能不能做 CAM | 不能，權重不綁單一通道 |

## 附錄 B 常見錯誤

1. **把 `A_k` 當成「已經 softmax 的機率圖」**：它是卷積輸出，值可正可負。
2. **忘記扣 bias**：`mean(CAM)` 對到的是 `logit − bias`。
3. **拿錯權重**：要取「目標類別那一列」，不是整張矩陣。
4. **在 ReLU 之後才取特徵圖**：文獻用的是最後一層卷積的**線性輸出**，取到激活後的圖會偏掉。
5. **上採樣後直接當遮罩用**：熱圖是證據分佈，不是分割結果。
6. **以為熱圖解釋了「為什麼」**：它只顯示「哪裡」，原因仍要另外驗證。

## 附錄 C 延伸閱讀與離線使用

站內：

- [GAP 是什麼？](/cnn-gap-head/)——GAP 的定義、與一般平均池化的差別、CAM 的橋
- [卷積層 vs 全連接層](/cnn-conv-vs-fc/)——為什麼大 FC 會讓權重對不回特徵圖
- [全連接層的運作](/cnn-fully-connected/)——`Wx + b` 與 softmax
- [激活函數與池化層](/cnn-activation-pooling/)——池化與 GAP 的取捨
- [圖解 CNN](/cnn-illustrated/)——整體資料流

站外：

- [Learning Deep Features for Discriminative Localization（CAM, CVPR 2016）](https://arxiv.org/abs/1512.04150)
- [Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization](https://arxiv.org/abs/1610.02391)

離線：本頁是**單一 HTML 檔、零外部資源**；原始 Markdown 在同一層。

## 附錄 D 一頁精華（考前 10 分鐘）

| # | 記這一條 |
|---|---|
| 1 | `CAM_c = Σ_k w[k,c] · A_k`，`w` 來自 GAP 後的 Linear |
| 2 | `mean(CAM_c) = logit_c − bias_c`（實測差 4.44e-16） |
| 3 | 原版 CAM 要求末端是 GAP + Linear；Flatten 頭做不到 |
| 4 | 熱圖解析度 = 最後特徵圖（`7×7`），上採樣 32 倍顯示 |
| 5 | 手算：`[[8.1, −0.3], [6.5, 1.3]]`，平均 3.9 = logit |
| 6 | Grad-CAM：`α = mean(梯度)`、`ReLU` 後加權 |
| 7 | 純 GAP + Linear 時 `Grad-CAM = ReLU(CAM/(H·W))` |
| 8 | 熱圖說「哪裡」，不說「為什麼」，也不保證答案對 |

## 附錄 E 互動測驗（30 題）

**🖱️ [開始作答](mc-quiz.html)**　即時計分、作答進度存在瀏覽器（localStorage）、
可切換「只看未答／只看答錯」，按「顯示答案」才揭曉答案與解析。

題目涵蓋本頁的實測數字與常見誤解，每題都附一句解析，答錯時可以直接對回上面的章節。

## 附錄 G 實測原始輸出

`verify_cnn_cam.py` 的完整輸出（Python 3.15.1 / NumPy 2.5.4，本機執行）：

```text
------------------------------------------------------------------------
1. the worked example on the page (3 maps, 2x2)
   A1 = [[10.0, 0.0], [8.0, 2.0]]  ->  F1 = 5.00
   A2 = [[1.0, 1.0], [1.0, 1.0]]  ->  F2 = 1.00
   A3 = [[0.0, 2.0], [0.0, 2.0]]  ->  F3 = 1.00
   w = [ 0.8  0.1 -0.2]
   logit = w1F1 + w2F2 + w3F3 = 3.90
------------------------------------------------------------------------
2. the CAM for the same example
   M = 0.8A1 + 0.1A2 - 0.2A3 =
 [[ 8.1 -0.3]
 [ 6.5  1.3]]
   corner (1,1) = 0.8*10 + 0.1*1 - 0.2*0   = 8.1
   corner (1,2) = 0.8*0  + 0.1*1 - 0.2*2   = -0.3
   mean(CAM)   = 3.9000   == logit 3.9000  ->  True
   argmax of CAM is at (0, 0)
------------------------------------------------------------------------
3. with a bias the identity is logit - bias = mean(CAM)
   bias 0.5 -> logit 4.40, mean(CAM) 3.90, logit-bias 3.90
------------------------------------------------------------------------
4. identity check on a random net (K=6, H=W=7, C=4)
   logits: [ 1.7521 -0.4246  1.5358  0.7722]
   mean(CAM) per class: [ 1.7521 -0.4246  1.5358  0.7722]
   max abs difference: 4.44e-16
   CAM shape (4, 7, 7) -> upsample to the input size for display
------------------------------------------------------------------------
5. Grad-CAM on a pure GAP+Linear net
   d y_c / d A_k(x,y) = w[k,c] / (H*W)
   alpha (Grad-CAM weights) == w/(H*W)?  True
   Grad-CAM map == ReLU(CAM / (H*W))?  True
   max abs difference: 5.64e-18
------------------------------------------------------------------------
6. why CAM needs GAP: flatten + FC has no per-map weight
   GAP + Linear : 6 weights, one per (channel, class)
   Flatten + FC : 1176 weights, one per (pixel, channel, class)
   ratio: 196x more weights, and none of them maps back to a single feature map
------------------------------------------------------------------------
7. CAM resolution
   input 224x224 -> last conv 7x7 -> CAM 7x7 (upsample x32 to the input)
   input 128x128 -> last conv 4x4 -> CAM 4x4 (upsample x32 to the input)
   input 32x32 -> last conv 1x1 -> CAM 1x1 (upsample x32 to the input)
------------------------------------------------------------------------
```

---

*本頁為個人學習筆記整理；圖表為手繪內嵌 SVG，數字全部由附錄 G 的程式算出。*
