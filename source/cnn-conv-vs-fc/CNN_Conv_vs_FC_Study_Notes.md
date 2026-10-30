# 卷積層 vs 全連接層：一張表、兩個實驗、一個結論

> 系列第五篇，也是收尾。前四篇把每個零件拆開講（[圖解 CNN](/cnn-illustrated/)、[卷積層的運作細節](/cnn-conv-details/)、<br />[激活函數與池化層](/cnn-activation-pooling/)、[全連接層的運作](/cnn-fully-connected/)），這一篇把它們放在一起比。<br />結論先講：<strong>卷積層用「同一組小權重到處找局部特徵」，全連接層用「所有特徵各給一票做最終判斷」。</strong><br />所有數字都是本機用 NumPy 算的（Python 3.15.1 / NumPy 2.5.4），原始輸出在附錄 G。

<!-- CNVF-FIGURE:side-by-side -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 410" role="img" aria-label="同一個 7×7 輸入的兩種接法：左邊卷積用一個 3×3 kernel 掃過 9 個位置共用 9 個權重，右邊全連接把每個輸入連到每個輸出、每條邊一個權重"><defs><marker id="arv" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="408.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一張輸入，兩種接法</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">左：局部連接＋權重共享；右：完全連接，每條邊一個權重</text><rect x="30" y="96" width="420" height="250" rx="12" fill="#12181f" stroke="#4ecdc466" stroke-width="1.4" opacity="0.6"/><text x="50" y="124" font-size="13" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">卷積層</text><text x="50" y="146" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一個 3×3 kernel 掃 9 個位置 → 9 個權重</text><rect x="60" y="164" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="90" y="164" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="120" y="164" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="150" y="164" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="180" y="164" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="210" y="164" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="240" y="164" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="60" y="194" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="90" y="194" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="120" y="194" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="150" y="194" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="180" y="194" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="210" y="194" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="240" y="194" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="60" y="224" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="90" y="224" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="120" y="224" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="150" y="224" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="180" y="224" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="210" y="224" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="240" y="224" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="60" y="254" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="90" y="254" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="120" y="254" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="150" y="254" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="180" y="254" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="210" y="254" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="240" y="254" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="60" y="284" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="90" y="284" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="120" y="284" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="150" y="284" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="180" y="284" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="210" y="284" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="240" y="284" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="60" y="314" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="90" y="314" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="120" y="314" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="150" y="314" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="180" y="314" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="210" y="314" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="240" y="314" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="60" y="344" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="90" y="344" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="120" y="344" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="150" y="344" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="180" y="344" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="210" y="344" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="240" y="344" width="30" height="30" rx="8" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.5"/><rect x="60" y="164" width="90" height="90" rx="4" fill="#e0a4581a" stroke="#e0a458" stroke-width="2.2"/><rect x="150" y="254" width="90" height="90" rx="4" fill="none" stroke="#e0a458" stroke-width="1.6" opacity="0.6"/><text x="105" y="300" font-size="10.5" fill="#e0a458" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一組 9 個權重</text><text x="330" y="210" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7×7 輸入</text><text x="330" y="232" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出 5×5</text><text x="330" y="254" font-size="11.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">參數 9 + 1</text><rect x="500" y="96" width="470" height="250" rx="12" fill="#12181f" stroke="#c084fc66" stroke-width="1.4" opacity="0.6"/><text x="520" y="124" font-size="13" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全連接層</text><text x="520" y="146" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每個輸入連到每個輸出 → 4×3 = 12 條邊</text><circle cx="560" cy="176" r="12" fill="#4ecdc4"/><text x="538" y="180" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">x1</text><circle cx="560" cy="216" r="12" fill="#4ecdc4"/><text x="538" y="220" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">x2</text><circle cx="560" cy="256" r="12" fill="#4ecdc4"/><text x="538" y="260" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">x3</text><circle cx="560" cy="296" r="12" fill="#4ecdc4"/><text x="538" y="300" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">x4</text><circle cx="900" cy="196" r="14" fill="#ff7b72"/><text x="922" y="200" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">z1</text><circle cx="900" cy="246" r="14" fill="#ff7b72"/><text x="922" y="250" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">z2</text><circle cx="900" cy="296" r="14" fill="#ff7b72"/><text x="922" y="300" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">z3</text><line x1="572" y1="176" x2="886" y2="196" stroke="#8b949e" stroke-width="1" opacity="0.45"/><line x1="572" y1="176" x2="886" y2="246" stroke="#8b949e" stroke-width="1" opacity="0.45"/><line x1="572" y1="176" x2="886" y2="296" stroke="#8b949e" stroke-width="1" opacity="0.45"/><line x1="572" y1="216" x2="886" y2="196" stroke="#8b949e" stroke-width="1" opacity="0.45"/><line x1="572" y1="216" x2="886" y2="246" stroke="#8b949e" stroke-width="1" opacity="0.45"/><line x1="572" y1="216" x2="886" y2="296" stroke="#8b949e" stroke-width="1" opacity="0.45"/><line x1="572" y1="256" x2="886" y2="196" stroke="#8b949e" stroke-width="1" opacity="0.45"/><line x1="572" y1="256" x2="886" y2="246" stroke="#8b949e" stroke-width="1" opacity="0.45"/><line x1="572" y1="256" x2="886" y2="296" stroke="#8b949e" stroke-width="1" opacity="0.45"/><line x1="572" y1="296" x2="886" y2="196" stroke="#8b949e" stroke-width="1" opacity="0.45"/><line x1="572" y1="296" x2="886" y2="246" stroke="#8b949e" stroke-width="1" opacity="0.45"/><line x1="572" y1="296" x2="886" y2="296" stroke="#8b949e" stroke-width="1" opacity="0.45"/><text x="730" y="336" font-size="11" fill="#c084fc" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">12 條邊 = 12 個獨立權重</text><text x="40" y="380" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩邊看到的輸入一樣大；差別在「同一個權重要不要重複用」。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">左邊：一個 kernel 掃 9 個位置，只有 9 個權重。右邊：每一條邊都是獨立權重，4×3 就是 12 個。</figcaption>
</figure>
<!-- /CNVF-FIGURE:side-by-side -->

## 1. 一張表看完

| 面向 | 卷積層 | 全連接層 |
|---|---|---|
| 連接方式 | 局部連接：每個輸出只看 kernel 覆蓋的區域 | 完全連接：每個輸出看所有輸入 |
| 權重共享 | 有（同一 kernel 掃全圖） | 沒有（每條邊一個權重） |
| 輸入形式 | 保留 `H × W × C` | 通常要先 flatten |
| 輸出形式 | feature map（有空間排列） | 向量（logits） |
| 參數量 | `(k²·C_in + 1)·C_out`，與影像大小無關 | `m·n + m`，隨特徵維度爆炸 |
| 保留位置關係 | 有 | 展平後通常沒有 |
| 平移特性 | 同一特徵在任何位置都認得 | 每個位置要各自學 |
| 計算量 | 每輸出只有 k² 次乘加（但輸出很多個） | 每輸出 m·n 次乘加 |
| 常見用途 | 邊緣、紋理、部件 | 整合特徵、分類／回歸 |
| 主要超參數 | kernel size、stride、padding、通道數 | 輸入維度、輸出神經元數 |

表裡最容易誤讀的是「計算量」那一列：卷積的**參數**少，但它要在每個位置重算一次，所以**乘加次數不見得少**——這件事 §3 有實測。

## 2. 運算方式：滑動的加權求和 vs 矩陣乘法

卷積層：

```text
y[i, j] = Σ_{a,b,c} w[a, b, c] · x[i+a, j+b, c] + bias
```

同一組 `w` 在每個位置重複使用。全連接層：

```text
z = W x + b            z_j = Σ_i w[j, i] · x_i + b_j
```

差別只有一句話：**卷積的 `w` 在空間上共用，全連接的 `W` 每一格都是自己的**。

## 3. 參數量：同樣的產出，差 61,544 倍

<!-- CNVF-FIGURE:params-log -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 400" role="img" aria-label="參數量對數比較：卷積 320 個、全連接 784 到 128 是 100480 個、全連接 784 到 25088 是 19694080 個"><defs><marker id="arv" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="398.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同樣產出 25,088 個值，參數差 61,544 倍</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">對數刻度（每格 10 倍）；卷積的 320 個參數是含 bias 的總數</text><line x1="420.0" y1="104" x2="420.0" y2="272" stroke="#8b949e" stroke-width="0.8" opacity="0.25"/><text x="420.0" y="292" font-size="10" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10^2</text><line x1="493.2142857142857" y1="104" x2="493.2142857142857" y2="272" stroke="#8b949e" stroke-width="0.8" opacity="0.25"/><text x="493.2142857142857" y="292" font-size="10" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10^3</text><line x1="566.4285714285714" y1="104" x2="566.4285714285714" y2="272" stroke="#8b949e" stroke-width="0.8" opacity="0.25"/><text x="566.4285714285714" y="292" font-size="10" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10^4</text><line x1="639.6428571428571" y1="104" x2="639.6428571428571" y2="272" stroke="#8b949e" stroke-width="0.8" opacity="0.25"/><text x="639.6428571428571" y="292" font-size="10" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10^5</text><line x1="712.8571428571429" y1="104" x2="712.8571428571429" y2="272" stroke="#8b949e" stroke-width="0.8" opacity="0.25"/><text x="712.8571428571429" y="292" font-size="10" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10^6</text><line x1="786.0714285714287" y1="104" x2="786.0714285714287" y2="272" stroke="#8b949e" stroke-width="0.8" opacity="0.25"/><text x="786.0714285714287" y="292" font-size="10" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10^7</text><text x="400" y="129" font-size="11.5" fill="#e6edf3" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">卷積 3×3、C_out 32</text><rect x="420" y="111" width="36.98419484127885" height="26" rx="4" fill="#4ecdc4" stroke="none" stroke-width="1" opacity="0.85"/><text x="466.98419484127885" y="129" font-size="11.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">320</text><text x="400" y="185" font-size="11.5" fill="#e6edf3" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全連接 784 → 128</text><rect x="420" y="167" width="219.79511550378209" height="26" rx="4" fill="#e0a458" stroke="none" stroke-width="1" opacity="0.85"/><text x="649.7951155037821" y="185" font-size="11.5" fill="#e0a458" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">100,480</text><text x="400" y="241" font-size="11.5" fill="#e6edf3" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全連接 784 → 25,088</text><rect x="420" y="223" width="387.62100644238126" height="26" rx="4" fill="#ff7b72" stroke="none" stroke-width="1" opacity="0.85"/><text x="817.6210064423813" y="241" font-size="11.5" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">19,694,080</text><text x="40" y="340" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">算力也差 87 倍：卷積 225,792 次乘加，全連接 19,668,992 次。</text><text x="40" y="364" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">參數少不代表算得少——卷積把權重重複用，所以每個位置都要再算一次。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">換算成「同樣產出 25,088 個值」：卷積 320 個參數，全連接 1,969 萬個——差 61,544 倍（對數刻度，每格 10 倍）。</figcaption>
</figure>
<!-- /CNVF-FIGURE:params-log -->

要比就得比「同樣產出多少個值」。輸入 `28×28×1`，兩邊都產出 `28×28×32 = 25,088` 個值：

| 做法 | 權重 | bias | 合計 |
|---|---|---|---|
| 卷積 3×3、32 個 kernel | 288 | 32 | **320** |
| 全連接 784 → 25,088 | 19,668,992 | 25,088 | **19,694,080** |

**差 61,544 倍**（權重單獨算是 68,295 倍）。

> 常見的比較寫法是「卷積 288 vs 全連接 100,352（784→128）」。兩個數字都對，但**產出量不同**：
> 卷積那 288 個權重產出 25,088 個值，全連接那 100,352 個權重只產出 128 個值。
> 換算成「每個輸出值要幾個權重」：卷積 **0.0115**、全連接 **784**——差四萬倍。

### 3.1 參數少不代表算得少

| | 乘加次數 |
|---|---|
| 卷積：25,088 個輸出 × 9 次 | **225,792** |
| 全連接：25,088 個輸出 × 784 次 | **19,668,992** |

全連接的算力是 87 倍。也就是說，同一個輸出量下，卷積在**參數**上贏六萬倍、在**計算**上贏 87 倍——兩個都不是同一個量級。

## 4. 輸入變大時，只有一邊的參數會長

<!-- CNVF-FIGURE:scaling -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 410" role="img" aria-label="輸入變大時參數怎麼變：全連接每放大一倍邊長就變四倍，卷積維持 320 個不變"><defs><marker id="arv" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="408.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸入變大時，誰的參數跟著長</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全連接 784 → 128 與卷積 3×3 → 32 通道；縱軸是對數</text><line x1="130" y1="270.0" x2="960" y2="270.0" stroke="#8b949e" stroke-width="0.8" opacity="0.22"/><text x="122" y="274.0" font-size="10" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10^3</text><line x1="130" y1="232.5" x2="960" y2="232.5" stroke="#8b949e" stroke-width="0.8" opacity="0.22"/><text x="122" y="236.5" font-size="10" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10^4</text><line x1="130" y1="195.0" x2="960" y2="195.0" stroke="#8b949e" stroke-width="0.8" opacity="0.22"/><text x="122" y="199.0" font-size="10" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10^5</text><line x1="130" y1="157.5" x2="960" y2="157.5" stroke="#8b949e" stroke-width="0.8" opacity="0.22"/><text x="122" y="161.5" font-size="10" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10^6</text><line x1="130" y1="120.0" x2="960" y2="120.0" stroke="#8b949e" stroke-width="0.8" opacity="0.22"/><text x="122" y="124.0" font-size="10" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10^7</text><text x="150" y="322" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">28</text><text x="320" y="322" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">56</text><text x="490" y="322" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">112</text><text x="660" y="322" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">224</text><text x="830" y="322" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">448</text><polyline points="150,194.92201401025798 320,172.3603316870395 490,149.78697617630633 660,127.21070018803141 830,104.63369394395986" fill="none" stroke="#ff7b72" stroke-width="2.4"/><circle cx="150" cy="194.92201401025798" r="4" fill="#ff7b72"/><circle cx="320" cy="172.3603316870395" r="4" fill="#ff7b72"/><circle cx="490" cy="149.78697617630633" r="4" fill="#ff7b72"/><circle cx="660" cy="127.21070018803141" r="4" fill="#ff7b72"/><circle cx="830" cy="104.63369394395986" r="4" fill="#ff7b72"/><text x="836" y="108.63369394395986" font-size="11" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2,569 萬</text><line x1="150" y1="288.55687581300356" x2="830" y2="288.55687581300356" stroke="#4ecdc4" stroke-width="2.4"/><text x="158" y="276.55687581300356" font-size="11" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">卷積 320（不變）</text><text x="520" y="348" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸入邊長（28 → 448）</text><text x="40" y="380" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">28 → 224 讓全連接長成 64 倍；卷積完全不受影響——這就是「卷積能處理高解析度影像」的根本原因。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">輸入邊長從 28 放大到 224，全連接的參數變 64 倍；卷積還是 320 個。</figcaption>
</figure>
<!-- /CNVF-FIGURE:scaling -->

固定「輸出 128 個神經元」，把輸入邊長從 28 放大到 224：

| 輸入邊長 | 全連接 784→128 等比例放大 | 卷積 3×3→32 |
|---|---|---|
| 28 | 100,480 | 320 |
| 56 | 401,536 | 320 |
| 112 | 1,605,760 | 320 |
| 224 | 6,422,656 | 320 |
| 448 | 25,690,240 | 320 |

邊長每變兩倍，全連接就變四倍（面積變四倍）；28 → 224 是 **64 倍**，卷積一個都沒動。
這就是「CNN 能處理高解析度影像」的根本原因，不是因為卷積比較聰明，而是因為它的參數根本不看影像大小。

## 5. 平移特性：一組權重 vs 九套權重

<!-- CNVF-FIGURE:translation -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" role="img" aria-label="平移特性：同一個 3×3 圖樣出現在 5×5 影像的兩個位置，卷積用同一組 9 個權重都偵測得到，全連接要為每個位置各學一套共 81 個權重"><defs><marker id="arv" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="438.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">平移特性：同一個圖樣出現在不同位置</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5×5 輸入、3×3 的圖樣、3×3 的偵測器；兩個位置都用同一組權重</text><rect x="60" y="120" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="100" y="120" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="140" y="120" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="180" y="120" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="220" y="120" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="60" y="160" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="100" y="160" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="140" y="160" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="180" y="160" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="220" y="160" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="60" y="200" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="100" y="200" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="140" y="200" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="180" y="200" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="220" y="200" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="60" y="240" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="100" y="240" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="140" y="240" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="180" y="240" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="220" y="240" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="60" y="280" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="100" y="280" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="140" y="280" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="180" y="280" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="220" y="280" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="60" y="120" width="120" height="120" rx="4" fill="#e0a4581a" stroke="#e0a458" stroke-width="2"/><text x="160" y="344" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">圖樣在 (0, 0)</text><line x1="160" y1="352" x2="160" y2="386" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="270" y="120" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="310" y="120" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="350" y="120" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="390" y="120" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="430" y="120" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="270" y="160" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="310" y="160" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="350" y="160" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="390" y="160" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="430" y="160" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="270" y="200" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="310" y="200" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="350" y="200" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="390" y="200" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="430" y="200" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="270" y="240" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="310" y="240" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="350" y="240" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="390" y="240" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="430" y="240" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="270" y="280" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="310" y="280" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="350" y="280" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="390" y="280" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="430" y="280" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.9" opacity="0.55"/><rect x="350" y="200" width="120" height="120" rx="4" fill="#e0a4581a" stroke="#e0a458" stroke-width="2"/><text x="370" y="344" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">圖樣在 (2, 2)</text><line x1="370" y1="352" x2="370" y2="386" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="480" y="106" width="180" height="96" rx="10" fill="#12181f" stroke="#4ecdc4" stroke-width="1.6"/><text x="570" y="138" font-size="12" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個 kernel</text><text x="570" y="162" font-size="12" fill="#4ecdc4" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">9 個權重</text><text x="570" y="186" font-size="10.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩處都回應 5</text><rect x="690" y="106" width="270" height="210" rx="10" fill="#12181f" stroke="#ff7b7288" stroke-width="1.4"/><text x="710" y="134" font-size="12" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全連接的做法</text><text x="710" y="162" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每個位置一套權重：</text><text x="710" y="186" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">9 個位置 × 9 個權重</text><text x="710" y="212" font-size="12.5" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">= 81 個（9 倍）</text><text x="710" y="244" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">而且每一種位移都要</text><text x="710" y="264" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">在資料裡出現過才學得會</text><text x="40" y="414" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一組權重 → 同一個特徵在任何位置都認得；這就是卷積的平移等變性。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">同一組 9 個權重就能在任何位置偵測到同一個圖樣；全連接得為每個位置準備一套，權重是 9 倍。</figcaption>
</figure>
<!-- /CNVF-FIGURE:translation -->

同一個 3×3 圖樣出現在 5×5 影像的兩個位置（左上 `(0,0)` 與右下 `(2,2)`）：

| 做法 | 需要的權重 | 實測回應 |
|---|---|---|
| 卷積（3×3 kernel，掃 9 個位置） | **9**（共用） | 兩處的最大回應都是 5 |
| 全連接（每個位置一套 3×3） | **81**（9 位置 × 9） | 要每一種位移都在資料裡出現過才學得會 |

9 倍只是這個小例子的比例；位置越多、影像越大，差距就越大。這也是為什麼卷積的**樣本效率**通常比全連接好——同一個特徵只需要被看過一次。

## 6. 在 CNN 裡的分工

```text
影像
→ Conv + ReLU：找邊緣、紋理、局部形狀
→ Pooling：縮小尺寸、保留重要響應
→ Flatten：攤成一維特徵向量
→ FC + ReLU：整合高階特徵
→ FC + Softmax：輸出類別機率
```

前段是**特徵偵測器**（不管貓耳出現在哪都認得），後段是**決策器**（把「有耳朵、有鬍鬚、有圓眼」綜合起來判斷是不是貓）。
兩者不是誰取代誰，而是「先抽特徵、再做決策」的分工。

## 7. 什麼時候用哪一種

| 情境 | 較合適 |
|---|---|
| 影像、影片、聲音頻譜等有網格結構 | 卷積 |
| 需要偵測邊緣、紋理、局部模式 | 卷積 |
| 資料量大、要壓參數與過擬合風險 | 卷積 |
| 已有高階特徵，要整合後分類 | 全連接 |
| 表格資料、特徵之間沒有空間鄰近關係 | 全連接 |
| 需要固定數量的類別分數或回歸值 | 全連接 |

## 8. GAP：現代 CNN 的折衷

全連接層最大的問題是「必須先 flatten」。全域平均池化（GAP）直接對每個通道取平均，把 `7×7×64` 壓成 `64`，再接口袋大小的 `Dense(K)`。

實測（4×4 特徵圖，值 1–16）：

| 做法 | 輸出 | 參數 |
|---|---|---|
| GAP | 1 個數（平均 8.5） | 0 |
| Flatten + FC 16→3 | 3 個數 | 51 |

GAP 的意義不只是省參數，還讓網路**對輸入尺寸不敏感**：換成 8×8 的圖，GAP 之後照樣是 64 維。代價是它只看得到平均，空間細節全丟——所以只適合放在分類頭之前。

## 9. 六個常見誤解

| 誤解 | 事實 |
|---|---|
| 卷積的參數少，所以算得也少 | 參數少，但每個位置都要重算；同輸出量下全連接的乘加次數是 87 倍，卷積仍然很吃算力 |
| 卷積比全連接「更強」 | 兩者解決不同問題；卷積不擅長「把已抽好的特徵整合成決策」 |
| 全連接一定要在最後 | 可以夾在中間（VGG 的 classifier 就是三層 FC），只是現代網路傾向少用 |
| 只要加卷積就能取代全連接 | `1×1` 卷積可以取代一部分，但最後的類別數仍需要某種 `C → K` 的映射 |
| GAP 一定比 Flatten 好 | GAP 丟掉空間資訊；需要定位的任務（分割、偵測）不能只用 GAP |
| 卷積的平移不變性是完美的 | 它是**局部**容忍（2×2 池化擋得住一格位移），不是全域不變 |

## 附錄 A 速查表

| 想問的事 | 答案 |
|---|---|
| 卷積參數 | `(k²·C_in + 1)·C_out`，與影像大小無關 |
| 全連接參數 | `m·n + m` |
| 同產出 25,088 值 | 卷積 320 vs 全連接 19,694,080（61,544 倍） |
| 同產出的乘加 | 225,792 vs 19,668,992（87 倍） |
| 28 → 224 | 全連接 ×64，卷積不變 |
| 平移 | 卷積共用 9 個權重；全連接每個位置一套 |
| 什麼時候用全連接 | 特徵已整合、要做 `C → K` 的映射 |
| 什麼時候用 GAP | 分類頭，且不在意空間位置 |

## 附錄 B 常見錯誤

1. **拿不同產出量的層比參數**：先確認「輸出數量」一樣再比。
2. **以為卷積一定比較省算力**：卷積省的是參數與記憶體，不是乘法次數。
3. **把 flatten 當成免費**：flatten 本身免費，但它後面的 FC 很貴。
4. **在需要位置資訊的任務上用 GAP 收尾**：分割、偵測會直接壞掉。
5. **說卷積「對平移不變」**：它對平移**等變**（特徵跟著移動），池化才帶來局部不變。
6. **忘了 bias**：卷積 `C_out` 個、全連接 `m` 個，數字都要算進去。

## 附錄 C 延伸閱讀與離線使用

站內：

- [CAM vs Grad-CAM：同一個熱圖，只差權重怎麼來](/cnn-cam-vs-gradcam/)——九個面向的對照與 α 的實測
- [Grad-CAM：用梯度算出模型在看哪裡](/cnn-gradcam/)——七個步驟、ReLU、選層，與 CAM 的等價條件
- [CAM：用 GAP 算出模型在看哪裡](/cnn-cam/)——GAP 之後的分類權重怎麼變成熱圖（含 Grad-CAM）
- [為什麼現代 CNN 常不用全連接層](/cnn-gap-head/)——GAP 分類頭：25,089,000 → 513,000 個參數
- [圖解 CNN：從 5×5 小圖算到類別機率](/cnn-illustrated/)——整個資料流
- [卷積層的運作細節](/cnn-conv-details/)——kernel 深度、stride／padding、感受野、空洞卷積
- [激活函數與池化層](/cnn-activation-pooling/)——ReLU 家族、Max／Average Pooling、GAP
- [全連接層的運作](/cnn-fully-connected/)——`Wx + b`、softmax 的三個性質、梯度

站外：

- [Dive into Deep Learning（繁中）— 卷積神經網路](https://zh.d2l.ai/chapter_convolutional-neural-networks/index.html)
- [CS231n：ConvNet 的架構與參數量](https://cs231n.github.io/convolutional-networks/)

離線：本頁是**單一 HTML 檔、零外部資源**；原始 Markdown 在同一層。

## 附錄 D 一頁精華（考前 10 分鐘）

| # | 記這一條 |
|---|---|
| 1 | 卷積＝局部連接＋權重共享；全連接＝完全連接、無共享 |
| 2 | 卷積參數與影像大小無關；全連接隨面積線性成長 |
| 3 | 同產出 25,088 值：320 vs 1,969 萬（61,544 倍） |
| 4 | 同產出的乘加：22.6 萬 vs 1,967 萬（87 倍） |
| 5 | 28 → 224：全連接 ×64，卷積不變 |
| 6 | 平移：卷積 9 個權重 vs 全連接 81 個（位置越多差越多） |
| 7 | GAP：`7×7×64 → 64`，參數 0，取代大 FC |
| 8 | 分工：前段抽特徵、後段做決策 |

## 附錄 G 實測原始輸出

`verify_cnn_conv_vs_fc.py` 的完整輸出（Python 3.15.1 / NumPy 2.5.4，本機執行）：

```text
------------------------------------------------------------------------
1. the same job, two layers: produce 28x28x32 = 25,088 values
   outputs            : 25088
   conv 3x3, C_out 32 : 288 weights + 32 bias = 320
   fc 784 -> 25088    : 19668992 weights + 25088 bias = 19694080
   ratio (total)      : 61544x
   ratio (weights)    : 68295x
------------------------------------------------------------------------
2. the draft's pair (288 vs 100,352) is not apples to apples
   conv 3x3x1x32 weights only : 288  -> keeps 25,088 outputs
   fc 784 -> 128 weights only : 100,352 -> gives 128 outputs
   per-output weights: conv 0.0115, fc 784.0
------------------------------------------------------------------------
3. multiply-accumulates (the compute side)
   conv : 25,088 outputs x 9 taps   = 225792 MACs
   fc   : 25,088 outputs x 784 taps = 19668992 MACs
   fc / conv = 87.1x more compute for 61544x more parameters
------------------------------------------------------------------------
4. scaling with input size (fc  -> 128 outputs, conv 3x3 -> 32 ch)
   side       fc 784-scale    conv params
   28               100480            320
   56               401536            320
   112             1605760            320
   224             6422656            320
   448            25690240            320
   28 -> 224 makes the fc layer 64x bigger, conv stays the same
------------------------------------------------------------------------
5. translation: one 3x3 detector on a 5x5 input (9 positions)
   conv: 9 shared weights detect the pattern anywhere -> 9 weights
   fc  : one weight per (position, pattern cell) -> 9 x 9 = 81 weights
   ratio: 9x
   pattern at (0,0): max response 5 (same kernel everywhere)
   pattern at (2,2): max response 5 (same kernel everywhere)
------------------------------------------------------------------------
6. what the two layers do to the same feature map
   input 4x4:
 [[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]
 [13 14 15 16]]
   global average (GAP) -> 8.5 (1 value, 0 params)
   flatten -> 16 values, then fc 16 -> 3 : params 51
------------------------------------------------------------------------
```

---

*本頁為個人學習筆記整理；圖表為手繪內嵌 SVG，數字全部由附錄 G 的程式算出。*
