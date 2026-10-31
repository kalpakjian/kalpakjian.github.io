# 激活函數與池化層：ReLU 家族與下採樣

> 系列第三篇。前兩篇談卷積本身（[圖解 CNN](/cnn-illustrated/)、[卷積層的運作細節](/cnn-conv-details/)），<br />這一篇只談接在卷積後面的兩層：<strong>激活函數</strong>（把線性結果轉成非線性）與 <strong>池化</strong>（下採樣）。<br />兩者都<strong>沒有可學習的參數</strong>：激活函數是固定的逐元素函數，池化只決定「怎麼掃」。<br />所有數字都是本機用 NumPy 算的（Python 3.15.1 / NumPy 2.5.4），原始輸出在附錄 G。

<!-- CNPA-FIGURE:relu-variants -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 400" role="img" aria-label="三個激活函數的折線圖：ReLU 在負區間為 0、Leaky ReLU 帶小斜率、GELU 是平滑曲線；左側是同一組輸入的實際輸出值"><defs><marker id="ara" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="398.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ReLU 與它的三個變體</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">差別全在負區間：ReLU 直接壓成 0，Leaky 留小斜率，GELU 平滑過渡</text><text x="60" y="116" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸入 x</text><text x="150" y="116" font-size="11.5" fill="#4ecdc4" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ReLU</text><text x="250" y="116" font-size="11.5" fill="#e0a458" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Leaky(0.1)</text><text x="60" y="146" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-3</text><text x="150" y="146" font-size="12.5" fill="#4ecdc4" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="250" y="146" font-size="12.5" fill="#e0a458" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">−0.30</text><text x="60" y="176" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-1</text><text x="150" y="176" font-size="12.5" fill="#4ecdc4" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="250" y="176" font-size="12.5" fill="#e0a458" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">−0.10</text><text x="60" y="206" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="150" y="206" font-size="12.5" fill="#4ecdc4" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="250" y="206" font-size="12.5" fill="#e0a458" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="60" y="236" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.5</text><text x="150" y="236" font-size="12.5" fill="#4ecdc4" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.5</text><text x="250" y="236" font-size="12.5" fill="#e0a458" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.50</text><text x="60" y="266" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><text x="150" y="266" font-size="12.5" fill="#4ecdc4" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><text x="250" y="266" font-size="12.5" fill="#e0a458" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2.00</text><text x="60" y="330" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GELU 不是折線：x = −1 時是 −0.1588，</text><text x="60" y="352" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">x = 0.5 時是 0.3457（實測）。</text><text x="430" y="100" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">三個函數疊在一起</text><line x1="420" y1="250" x2="813.0" y2="250" stroke="#8b949e" stroke-width="1"/><line x1="560" y1="96" x2="560" y2="316" stroke="#8b949e" stroke-width="1"/><polyline points="340,250 560,250 780,90" fill="none" stroke="#4ecdc4" stroke-width="2.6" stroke-linejoin="round"/><polyline points="340,266.0 780,90" fill="none" stroke="#e0a458" stroke-width="2.2" stroke-linejoin="round"/><polyline points="340.0,250.0 353.8,250.0 367.5,250.0 381.2,250.1 395.0,250.1 408.8,250.3 422.5,250.6 436.2,251.1 450.0,251.8 463.8,252.8 477.5,254.0 491.2,255.3 505.0,256.4 518.8,256.8 532.5,256.2 546.2,254.0 560.0,250.0 573.8,244.0 587.5,236.2 601.2,226.8 615.0,216.4 628.8,205.3 642.5,194.0 656.2,182.8 670.0,171.8 683.8,161.1 697.5,150.6 711.2,140.3 725.0,130.1 738.8,120.1 752.5,110.0 766.2,100.0 780.0,90.0" fill="none" stroke="#c084fc" stroke-width="2" stroke-dasharray="5 3"/><text x="340" y="270" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-4</text><text x="560" y="270" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="780" y="270" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text><text x="792" y="94" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text><text x="568" y="108" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">y</text><rect x="740" y="300" width="12" height="12" rx="3" fill="#4ecdc444" stroke="#4ecdc4" stroke-width="1.5"/><text x="760" y="311" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ReLU</text><rect x="740" y="330" width="12" height="12" rx="3" fill="#e0a45844" stroke="#e0a458" stroke-width="1.5"/><text x="760" y="341" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Leaky ReLU</text><rect x="880" y="300" width="12" height="12" rx="3" fill="#c084fc44" stroke="#c084fc" stroke-width="1.5"/><text x="900" y="311" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GELU</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">ReLU 把負的整段壓成 0；Leaky ReLU 留一點斜率；GELU 則是平滑版本。三者在正區間幾乎一樣。</figcaption>
</figure>
<!-- /CNPA-FIGURE:relu-variants -->

## 1. 這兩層都不學參數

| 層 | 主要目的 | 可學習參數 | 改變通道數 | 改變寬高 |
|---|---|---|---|---|
| 卷積層 | 提取局部特徵 | 有（kernel＋bias） | 會（由 kernel 數量決定） | 視 stride／padding |
| 激活函數 | 加入非線性 | **無** | 不會 | 不會 |
| 池化層 | 縮小空間尺寸、摘要 | **無** | 不會 | 通常縮小 |

順序幾乎固定是 **Conv → ReLU → Pool**。理由很直接：卷積是線性的，先把非線性補上，再把解析度降下來；如果先池化，等於在還沒判斷「哪裡有東西」之前就先丟掉一半解析度。

## 2. ReLU：定義與實測

```text
ReLU(x) = max(0, x)
```

規則只有一條：正數原樣保留，負數變成 0。實測（同一組輸入）：

| x | −3 | −1 | 0 | 0.5 | 2 |
|---|---|---|---|---|---|
| ReLU(x) | 0 | 0 | 0 | 0.5 | 2 |
| Leaky ReLU(0.1) | −0.30 | −0.10 | 0 | 0.50 | 2.00 |
| GELU | −0.0036 | −0.1588 | 0 | 0.3457 | 1.9546 |

### 2.1 為什麼一定要有非線性

卷積是「乘權重、相加、加 bias」，整條都是線性的。若兩層之間沒有非線性，兩層就等價於一層：把 `W₂(W₁x + b₁) + b₂` 展開，得到 `(W₂W₁)x + (W₂b₁ + b₂)`——還是同一個線性映射。

實測（隨機的 W₁、W₂、b₁、b₂，兩層 vs 一層合併後的結果）：**最大差異 4.44e-16**，也就是浮點誤差等級的「完全相等」。所以沒有非線性的深層網路，深度是假的：再多層也只能畫直線邊界。

### 2.2 四個特性

| 特性 | 說明 | 代價 |
|---|---|---|
| 計算簡單 | 只需比較 0 | 幾乎不佔時間 |
| 稀疏激活 | 負值全變 0，部分單元不激活 | 表徵容量少一半 |
| 緩解梯度消失 | 正區間梯度恆為 1 | 負區間梯度恆為 0 |
| 可能死亡 | 對**所有輸入**都輸出 0 時就永遠不再更新 | 那顆神經元等於報廢 |

「稀疏」有多稀疏？把標準常態 `N(0,1)` 的 1000×1000 特徵圖過 ReLU，實測 **50.0%** 的格子是 0。這不是 bug，是設計：一半的單元對這張圖「沒意見」。

### 2.3 三個變體

| 函數 | 負區間 | 為什麼存在 |
|---|---|---|
| Leaky ReLU | `0.01x` 或 `0.1x` | 給負區間一條細縫，梯度不會完全斷掉 |
| PReLU | `ax`，`a` 是可學參數 | 讓斜率自己學（所以它**有**參數） |
| GELU | 平滑地壓向 0 | Transformer 系列的預設；負值小幅保留 |

注意 **PReLU 是這一節唯一的例外**：它的 `a` 是學出來的，所以嚴格說它「有參數」。ReLU、Leaky ReLU、GELU 都是固定函數。

### 2.4 死亡 ReLU：怎麼判定，不是「有沒有輸出 0」

判定標準是「**對所有輸入**都輸出 0」，不是「這張圖輸出 0」。實測：一個 256 維輸入、512 筆樣本的單一神經元，最大投影是 **51.08**；bias 設 0 或 25.54 時都還有輸出（最大 51.08／25.54），但 bias 一旦到 **52.08**，全部 512 筆都變成 0——這才是真的死了。

差別在於梯度：`x < 0` 時 ReLU 的梯度是 0，權重收不到更新訊號；一旦某顆單元對整個資料集都落在負區間，它就再也沒有機會被救回來。

## 3. 池化：逐通道的下採樣

<!-- CNPA-FIGURE:maxpool -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 400" role="img" aria-label="最大池化：4×4 特徵圖切成四個 2×2 窗口，各取最大值 6、8、3、4，輸出 2×2，數值由 16 個減為 4 個"><defs><marker id="ara" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="398.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">最大池化：每個窗口只留冠軍</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4×4 特徵圖、2×2 窗口、步幅 2 → 2×2 輸出；通道之間互不相干</text><text x="60" y="112" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸入 4×4</text><rect x="60" y="126" width="52" height="52" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="86.0" y="157.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="112" y="126" width="52" height="52" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="138.0" y="157.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="60" y="178" width="52" height="52" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="86.0" y="209.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text><rect x="112" y="178" width="52" height="52" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="138.0" y="209.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text><rect x="164" y="126" width="52" height="52" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="190.0" y="157.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><rect x="216" y="126" width="52" height="52" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="242.0" y="157.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text><rect x="164" y="178" width="52" height="52" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="190.0" y="209.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7</text><rect x="216" y="178" width="52" height="52" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="242.0" y="209.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text><rect x="60" y="230" width="52" height="52" rx="4" fill="#c084fc26" stroke="#c084fc" stroke-width="1.6"/><text x="86.0" y="261.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><rect x="112" y="230" width="52" height="52" rx="4" fill="#c084fc26" stroke="#c084fc" stroke-width="1.6"/><text x="138.0" y="261.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><rect x="60" y="282" width="52" height="52" rx="4" fill="#c084fc26" stroke="#c084fc" stroke-width="1.6"/><text x="86.0" y="313.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="112" y="282" width="52" height="52" rx="4" fill="#c084fc26" stroke="#c084fc" stroke-width="1.6"/><text x="138.0" y="313.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><rect x="164" y="230" width="52" height="52" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="190.0" y="261.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="216" y="230" width="52" height="52" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="242.0" y="261.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="164" y="282" width="52" height="52" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="190.0" y="313.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><rect x="216" y="282" width="52" height="52" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="242.0" y="313.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text><rect x="112" y="178" width="52" height="52" rx="3" fill="none" stroke="#e6edf3" stroke-width="1.8"/><rect x="216" y="178" width="52" height="52" rx="3" fill="none" stroke="#e6edf3" stroke-width="1.8"/><rect x="112" y="230" width="52" height="52" rx="3" fill="none" stroke="#e6edf3" stroke-width="1.8"/><rect x="216" y="282" width="52" height="52" rx="3" fill="none" stroke="#e6edf3" stroke-width="1.8"/><line x1="276" y1="230" x2="340" y2="230" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><text x="308" y="208" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">取最大</text><text x="350" y="158" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出 2×2</text><rect x="350" y="174" width="56" height="56" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="378.0" y="207.76" font-size="16" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text><rect x="406" y="174" width="56" height="56" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="434.0" y="207.76" font-size="16" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text><rect x="350" y="230" width="56" height="56" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="378.0" y="263.76" font-size="16" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><rect x="406" y="230" width="56" height="56" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="434.0" y="263.76" font-size="16" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text><text x="350" y="306" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">16 個值 → 4 個值（−75%）</text><text x="560" y="176" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每個通道各自池化：</text><text x="560" y="200" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">32 通道進、32 通道出</text><text x="560" y="236" font-size="12" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">參數 0 個</text><text x="560" y="268" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">反向傳播時，梯度只回給</text><text x="560" y="288" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每個窗口裡「最大值」那一格</text><text x="40" y="372" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">白色方框＝每個窗口的冠軍。池化不做加權，所以沒有東西要學。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">最大池化只留下每個窗口的冠軍。16 個值變 4 個（少 75%），但最強的響應一個都沒丟。</figcaption>
</figure>
<!-- /CNPA-FIGURE:maxpool -->

池化把特徵圖切成小窗口，每個窗口壓成一個值。最常見的設定是 `2×2` 窗口、步幅 2，所以寬與高各縮小一半；**通道數不變**，因為池化是**逐通道獨立**做的——第 1 個通道只用第 1 個通道的數字，不會跟別通道混在一起。

### 3.1 Max 與 Average 的差別

```text
Max Pooling     y[i, j] = max(x[a, b])            a, b ∈ window(i, j)
Average Pooling y[i, j] = mean(x[a, b])           a, b ∈ window(i, j)
```

拿同一個窗口試：`[[2, 7], [1, 5]]` →

| 做法 | 結果 |
|---|---|
| Max Pooling | **7** |
| Average Pooling | (2 + 7 + 1 + 5) / 4 = **3.75** |

Max 保留「這個區域裡最強的響應有多強」；Average 保留「整體强度」。影像分類的中段幾乎都用 Max（要的是「有沒有」），而網路末端常用 GAP（要的是「整體平均」）。

### 3.2 實測：16 個值怎麼變成 4 個

輸入 4×4、`2×2` 窗口、步幅 2：

```text
[[1, 1, 2, 4],
 [5, 6, 7, 8],
 [3, 2, 1, 0],
 [1, 2, 3, 4]]
```

四個窗口的冠軍（位置由實測標出）與輸出：

```text
winner (1,1)=6   winner (1,3)=8       輸出 2×2
winner (2,0)=3   winner (3,3)=4       [[6, 8],
                                       [3, 4]]
```

同一張圖改用平均池化 → `[[3.25, 5.25], [2.0, 2.0]]`。數值由 16 個變 4 個（**少 75%**），但 max 版把每個區域最強的那一格完整留下來。

### 3.3 輸出尺寸：三種設定

<!-- CNPA-FIGURE:pool-configs -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 380" role="img" aria-label="三種池化設定的輸出尺寸：2×2 步幅 2 得 2×2、2×2 步幅 1 重疊得 3×3、3×3 步幅 2 補 1 得 2×2"><defs><marker id="ara" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="378.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一張 4×4，三種池化設定</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">O = ⌊(W − k + 2p) / s⌋ + 1</text><rect x="30" y="96" width="300" height="214" rx="8" fill="#12181f" stroke="#4ecdc488" stroke-width="1.5" opacity="0.9"/><text x="46" y="122" font-size="12.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2×2、步幅 2</text><text x="46" y="146" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">(4 − 2)/2 + 1 = 2</text><rect x="46" y="164" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="66.0" y="189.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text><rect x="86" y="164" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="106.0" y="189.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text><rect x="46" y="204" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="66.0" y="229.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><rect x="86" y="204" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="106.0" y="229.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text><text x="146" y="202" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 2×2</text><text x="46" y="290" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不重疊，最常見的設定</text><rect x="350" y="96" width="300" height="214" rx="8" fill="#12181f" stroke="#58a6ff88" stroke-width="1.5" opacity="0.9"/><text x="366" y="122" font-size="12.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2×2、步幅 1</text><text x="366" y="146" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">(4 − 2)/1 + 1 = 3</text><rect x="366" y="164" width="34" height="34" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="383.0" y="185.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text><rect x="400" y="164" width="34" height="34" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="417.0" y="185.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7</text><rect x="434" y="164" width="34" height="34" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="451.0" y="185.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text><rect x="366" y="198" width="34" height="34" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="383.0" y="219.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text><rect x="400" y="198" width="34" height="34" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="417.0" y="219.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7</text><rect x="434" y="198" width="34" height="34" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="451.0" y="219.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text><rect x="366" y="232" width="34" height="34" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="383.0" y="253.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><rect x="400" y="232" width="34" height="34" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="417.0" y="253.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><rect x="434" y="232" width="34" height="34" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="451.0" y="253.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text><text x="488" y="202" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 3×3</text><text x="366" y="290" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">窗口重疊，輸出變大</text><rect x="670" y="96" width="300" height="214" rx="8" fill="#12181f" stroke="#e0a45888" stroke-width="1.5" opacity="0.9"/><text x="686" y="122" font-size="12.5" fill="#e0a458" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3×3、步幅 2、補 1</text><text x="686" y="146" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">(4 + 2 − 3)/2 + 1 = 2</text><rect x="686" y="164" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="706.0" y="189.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text><rect x="726" y="164" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="746.0" y="189.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text><rect x="686" y="204" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="706.0" y="229.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text><rect x="726" y="204" width="40" height="40" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="746.0" y="229.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text><text x="786" y="202" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 2×2</text><text x="686" y="290" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">補邊用 −∞，不會被選到</text><text x="40" y="348" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">池化沒有可學的參數，只有「怎麼掃」的設定；預設是 2×2、步幅 2。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">同樣的 4×4 特徵圖，三種設定給出三種輸出尺寸；步幅 1 會讓窗口重疊，步幅 2 不重疊。</figcaption>
</figure>
<!-- /CNPA-FIGURE:pool-configs -->

```text
O = ⌊(W − k + 2p) / s⌋ + 1
```

實測（同一張 4×4）：

| 設定 | 算式 | 輸出 |
|---|---|---|
| 2×2、步幅 2、不補邊 | (4 − 2)/2 + 1 | 2×2 |
| 2×2、步幅 1、不補邊 | (4 − 2)/1 + 1 | 3×3（窗口重疊） |
| 3×3、步幅 2、補 1 | (4 + 2 − 3)/2 + 1 | 2×2 |

步幅 1 的版本輸出 `[[6,7,8],[6,7,8],[3,3,4]]`——最大值會在多個窗口裡重複出現，這就是「重疊池化」。實務上很少用，因為它省下的解析度不多，計算量卻變大。

補邊要特別注意：**Max Pooling 的補邊預設不是 0，而是 −∞**（PyTorch 的 `MaxPool2d` 就是這樣）。若補 0，一個全負數的窗口會憑空冒出 0 這個假最大值。

### 3.4 反向傳播：梯度只回給冠軍

Max Pooling 沒有任何參數，但它**有梯度**——只是分配方式很特別：每個窗口的上游梯度，全部回給「當初選中的那一格」，其他格收到 0。

實測（上游梯度 `[[1,2],[3,4]]`，對應 4×4 輸入）：

```text
grad on input =
[[0, 0, 0, 0],
 [0, 1, 0, 2],
 [3, 0, 0, 0],
 [0, 0, 0, 4]]
```

總和守恆（10 = 10），而且用中心差分做數值梯度檢查的結果**完全一致**（`allclose` 為 True）。這也解釋了 Max Pooling 的一個副作用：梯度只走一條路，其他位置永遠收不到訊號。

## 4. 全域平均池化（GAP）

<!-- CNPA-FIGURE:gap -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 420" role="img" aria-label="全域平均池化：三個 7×7 的特徵圖各自平均成一個數字，得到長度 512 的向量，沒有任何參數"><defs><marker id="ara" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="418.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全域平均池化（GAP）：每個通道壓成一個數</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7×7×512 → 512；沒有參數，輸出長度就等於通道數</text><text x="60" y="149" font-size="11.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">通道 1</text><rect x="140" y="104" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="166" y="104" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="192" y="104" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="218" y="104" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="244" y="104" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="270" y="104" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="296" y="104" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="140" y="130" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="166" y="130" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="192" y="130" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="218" y="130" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="244" y="130" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="270" y="130" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="296" y="130" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="140" y="156" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="166" y="156" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="192" y="156" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="218" y="156" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="244" y="156" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="270" y="156" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="296" y="156" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="140" y="182" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="166" y="182" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="192" y="182" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="218" y="182" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="244" y="182" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="270" y="182" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="296" y="182" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="140" y="208" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="166" y="208" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="192" y="208" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="218" y="208" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="244" y="208" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="270" y="208" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="296" y="208" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="140" y="234" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="166" y="234" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="192" y="234" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="218" y="234" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="244" y="234" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="270" y="234" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="296" y="234" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="140" y="260" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="166" y="260" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="192" y="260" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="218" y="260" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="244" y="260" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="270" y="260" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><rect x="296" y="260" width="26" height="26" rx="3" fill="none" stroke="#4ecdc4" stroke-width="0.8" opacity="0.55"/><line x1="330" y1="195" x2="372" y2="195" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><text x="388" y="200" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">平均</text><rect x="440" y="160" width="92" height="70" rx="8" fill="#12181f" stroke="#4ecdc499" stroke-width="1.4"/><text x="486" y="204" font-size="16" fill="#4ecdc4" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.42</text><text x="60" y="235" font-size="11.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">通道 2</text><rect x="140" y="190" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="166" y="190" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="192" y="190" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="218" y="190" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="244" y="190" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="270" y="190" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="296" y="190" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="140" y="216" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="166" y="216" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="192" y="216" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="218" y="216" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="244" y="216" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="270" y="216" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="296" y="216" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="140" y="242" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="166" y="242" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="192" y="242" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="218" y="242" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="244" y="242" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="270" y="242" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="296" y="242" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="140" y="268" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="166" y="268" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="192" y="268" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="218" y="268" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="244" y="268" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="270" y="268" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="296" y="268" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="140" y="294" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="166" y="294" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="192" y="294" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="218" y="294" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="244" y="294" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="270" y="294" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="296" y="294" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="140" y="320" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="166" y="320" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="192" y="320" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="218" y="320" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="244" y="320" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="270" y="320" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="296" y="320" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="140" y="346" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="166" y="346" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="192" y="346" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="218" y="346" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="244" y="346" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="270" y="346" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><rect x="296" y="346" width="26" height="26" rx="3" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.55"/><line x1="330" y1="281" x2="372" y2="281" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><text x="388" y="286" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">平均</text><rect x="440" y="246" width="92" height="70" rx="8" fill="#12181f" stroke="#58a6ff99" stroke-width="1.4"/><text x="486" y="290" font-size="16" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.11</text><text x="60" y="321" font-size="11.5" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">通道 3</text><rect x="140" y="276" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="166" y="276" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="192" y="276" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="218" y="276" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="244" y="276" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="270" y="276" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="296" y="276" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="140" y="302" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="166" y="302" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="192" y="302" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="218" y="302" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="244" y="302" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="270" y="302" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="296" y="302" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="140" y="328" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="166" y="328" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="192" y="328" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="218" y="328" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="244" y="328" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="270" y="328" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="296" y="328" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="140" y="354" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="166" y="354" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="192" y="354" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="218" y="354" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="244" y="354" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="270" y="354" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="296" y="354" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="140" y="380" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="166" y="380" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="192" y="380" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="218" y="380" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="244" y="380" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="270" y="380" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="296" y="380" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="140" y="406" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="166" y="406" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="192" y="406" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="218" y="406" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="244" y="406" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="270" y="406" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="296" y="406" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="140" y="432" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="166" y="432" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="192" y="432" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="218" y="432" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="244" y="432" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="270" y="432" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><rect x="296" y="432" width="26" height="26" rx="3" fill="none" stroke="#c084fc" stroke-width="0.8" opacity="0.55"/><line x1="330" y1="367" x2="372" y2="367" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><text x="388" y="372" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">平均</text><rect x="440" y="332" width="92" height="70" rx="8" fill="#12181f" stroke="#c084fc99" stroke-width="1.4"/><text x="486" y="376" font-size="16" fill="#c084fc" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.87</text><text x="140" y="392" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7×7 = 49 個數字平均成 1 個；512 個通道就是 512 個數字</text><text x="560" y="130" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GAP 之後接一個 Dense(10)，</text><text x="560" y="152" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">參數只有 5,120 + 10 = 5,130 個。</text><text x="560" y="190" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同樣的頭若先 Flatten（7×7×512 = 25,088）</text><text x="560" y="212" font-size="12" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">再接 Dense(10)，就是 250,890 個參數。</text><text x="560" y="250" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GAP 也讓輸入尺寸自由：換成 8×8 的圖，</text><text x="560" y="270" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出照樣是 512 維，網路不必改。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">GAP 把每個通道壓成一個數字：參數 0，輸出長度就等於通道數，常用來取代 Flatten + 全連接。</figcaption>
</figure>
<!-- /CNPA-FIGURE:gap -->

GAP 是池化的極端版本：窗口就是整張特徵圖，每個通道平均成一個數字。`7×7×512` → `512`。

它常被用來取代「Flatten + 全連接」：

| 做法 | 進 Dense(10) 的維度 | 參數量 |
|---|---|---|
| Flatten | 7×7×512 = 25,088 | 25,088 × 10 + 10 = **250,890** |
| GAP | 512 | 512 × 10 + 10 = **5,130** |

差了 48 倍，而且 GAP 讓網路對輸入尺寸不再敏感：換成 8×8 的圖，輸出照樣是 512 維。代價是它只看得到「每張圖的平均」，空間細節全部丟掉——所以它只適合放在分類頭之前，不適合放在中段。

## 5. 一個 block 的形狀流

<!-- CNPA-FIGURE:block -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 350" role="img" aria-label="一個 CNN block 的形狀流：32×32×3 經 Conv 3×3 32 個 filter 補 1 得到 32×32×32、ReLU 不變、MaxPool 2×2 步幅 2 得到 16×16×32"><defs><marker id="ara" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="348.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一個 block：Conv → ReLU → Pool</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">形狀只在 Conv 與 Pool 改變；參數只有 Conv 有</text><rect x="45" y="104" width="190" height="66" rx="10" fill="#12181f" stroke="#4ecdc4" stroke-width="1.6" opacity="0.9"/><text x="140.0" y="144" font-size="11.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸入</text><text x="140.0" y="204" font-size="12" fill="#4ecdc4" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">32 × 32 × 3</text><text x="140.0" y="226" font-size="10.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">參數 —</text><line x1="241" y1="137.0" x2="275" y2="137.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="283" y="104" width="190" height="66" rx="10" fill="#12181f" stroke="#4ecdc4" stroke-width="1.6" opacity="0.9"/><text x="378.0" y="144" font-size="11.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Conv 3×3、32 filters、補 1</text><text x="378.0" y="204" font-size="12" fill="#4ecdc4" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">32 × 32 × 32</text><text x="378.0" y="226" font-size="10.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">參數 896</text><line x1="479" y1="137.0" x2="513" y2="137.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="521" y="104" width="190" height="66" rx="10" fill="#12181f" stroke="#58a6ff" stroke-width="1.6" opacity="0.9"/><text x="616.0" y="144" font-size="11.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ReLU</text><text x="616.0" y="204" font-size="12" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">32 × 32 × 32</text><text x="616.0" y="226" font-size="10.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">參數 0</text><line x1="717" y1="137.0" x2="751" y2="137.0" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="759" y="104" width="190" height="66" rx="10" fill="#12181f" stroke="#e0a458" stroke-width="1.6" opacity="0.9"/><text x="854.0" y="144" font-size="11.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">MaxPool 2×2、stride 2</text><text x="854.0" y="204" font-size="12" fill="#e0a458" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">16 × 16 × 32</text><text x="854.0" y="226" font-size="10.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">參數 0</text><text x="45" y="292" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個 block 疊三次：32×32 → 16×16 → 8×8 → 4×4，通道 3 → 32 → 64 → 128。</text><text x="45" y="316" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">解析度一路砍、通道一路加，這是 CNN 的固定節奏。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">一個 block 的三層：只有 Conv 有參數（896 個），ReLU 與 Pool 都是 0 個。</figcaption>
</figure>
<!-- /CNPA-FIGURE:block -->

```text
32×32×3
→ Conv 3×3、32 filters、padding 1   → 32×32×32   （參數 (27+1)×32 = 896）
→ ReLU                             → 32×32×32   （參數 0）
→ MaxPool 2×2、stride 2             → 16×16×32   （參數 0）
```

三個數字要記住：**Conv 改通道數、Pool 砍面積、ReLU 什麼都不改**。同一組 block 疊三次，形狀就是 `32 → 16 → 8 → 4`、通道 `3 → 32 → 64 → 128`——解析度一路砍、通道一路加，這是 CNN 的固定節奏。

## 6. 三層對照

| 項目 | 卷積層 | ReLU | 池化層 |
|---|---|---|---|
| 主要目的 | 提取局部特徵 | 加入非線性 | 縮小尺寸、摘要特徵 |
| 可學習參數 | 有（kernel + bias） | 無 | 無（PReLU 例外） |
| 改變通道數 | 會，由 kernel 數量決定 | 不會 | 不會 |
| 改變寬高 | 看 stride／padding | 不會 | 通常縮小 |
| 反向傳播 | 對權重求導 | 遮罩（<0 給 0） | 把梯度回給冠軍 |
| 常見位置 | 主體 | 卷積後 | 卷積＋ReLU 後 |

## 7. 六個常見誤解

| 誤解 | 事實 |
|---|---|
| 激活函數有參數 | ReLU／Leaky ReLU／GELU 都沒有；只有 PReLU 的斜率是學的 |
| 池化會改變通道數 | 不會，池化是逐通道做的；改通道數是卷積的工作 |
| Max Pooling 沒有梯度 | 它有梯度，只是全部回給每個窗口的冠軍 |
| 池化補邊補 0 | Max Pooling 補 −∞，否則全負窗口會冒出假的 0 |
| ReLU 死了＝這張圖輸出 0 | 要看**對所有輸入**是否都 0；單張圖輸出 0 很正常 |
| 池化一定比卷積省 | 池化省參數，但 stride 2 的卷積可以做到同樣的降尺寸、還順便學特徵 |

## 附錄 A 速查表

| 想問的事 | 答案 |
|---|---|
| ReLU 公式 | `max(0, x)` |
| ReLU 的梯度 | `x > 0` 為 1，`x < 0` 為 0（`x = 0` 慣例取 0） |
| ReLU 後大約幾成是 0 | 標準常態輸入下約 50%（實測 50.0%） |
| 怎麼判定死亡 | 對所有輸入都輸出 0，不是單張圖 |
| 池化公式（max） | 窗口內取最大值 |
| 池化公式（avg） | 窗口內取平均 |
| 池化輸出尺寸 | `O = ⌊(W − k + 2p)/s⌋ + 1` |
| 2×2、步幅 2 | `W/2`（28 → 14、32 → 16） |
| Max Pooling 補邊值 | −∞（不是 0） |
| GAP | 每個通道平均成一個數，參數 0 |

## 附錄 B 常見錯誤

1. **把 ReLU 當成「歸一化」**：它只切掉負值，不做縮放。
2. **在池化前後搞錯通道順序**：`(N, C, H, W)` 池化只動 H、W。
3. **對全負特徵圖補 0 再 max pool**：會憑空產生 0，要用 −∞。
4. **以為池化能取代卷積降採樣**：可以，但 stride 2 的卷積會多學一組權重，性質不同。
5. **用 Flatten 接大 Dense 卻說「參數不多」**：`7×7×512 → 10` 就是 25 萬個參數。
6. **對 Leaky ReLU 的負斜率期待太高**：0.01 只是讓梯度不完全斷，不是讓負值變重要。

## 附錄 C 延伸閱讀與離線使用

站內：

- [CAM vs Grad-CAM：同一個熱圖，只差權重怎麼來](/cnn-cam-vs-gradcam/)——九個面向的對照與 α 的實測
- [Grad-CAM：用梯度算出模型在看哪裡](/cnn-gradcam/)——七個步驟、ReLU、選層，與 CAM 的等價條件
- [CAM：用 GAP 算出模型在看哪裡](/cnn-cam/)——GAP 之後的分類權重怎麼變成熱圖（含 Grad-CAM）
- [為什麼現代 CNN 常不用全連接層](/cnn-gap-head/)——GAP 分類頭：25,089,000 → 513,000 個參數
- [卷積層 vs 全連接層](/cnn-conv-vs-fc/)——系列總整理：參數、算力與平移特性的對照
- [圖解 CNN：從 5×5 小圖算到類別機率](/cnn-illustrated/)——整體資料流與 softmax
- [卷積層的運作細節](/cnn-conv-details/)——kernel 深度、stride／padding、感受野、空洞卷積
- [全連接層的運作](/cnn-fully-connected/)——本篇的續篇：Wx + b、flatten、softmax、加權投票
- [CNN 2 學習筆記（Lesson 7）](/cnn2-notes/)——ReLU 的兩個經典問題、池化的空間不變性
- [CNN 學習筆記（Lesson 6）](/cnn-notes/)——卷積的數學與 LeNet-5

站外：

- [Dive into Deep Learning（繁中）— 池化層](https://zh.d2l.ai/chapter_convolutional-neural-networks/pooling.html)
- [PyTorch `MaxPool2d` 文件](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)

離線：本頁是**單一 HTML 檔、零外部資源**；原始 Markdown 在同一層。

## 附錄 D 一頁精華（考前 10 分鐘）

| # | 記這一條 |
|---|---|
| 1 | ReLU = `max(0, x)`，梯度正區間 1、負區間 0 |
| 2 | 沒有非線性，多層等於一層（實測差異 4.44e-16） |
| 3 | ReLU 後約一半是 0；死亡要看「對所有輸入都 0」 |
| 4 | 池化逐通道、無參數；2×2 步幅 2 → 邊長砍半 |
| 5 | Max 取冠軍、Average 取平均；補邊用 −∞ |
| 6 | Max Pooling 的梯度只回給冠軍 |
| 7 | GAP：`7×7×512 → 512`，參數 0，取代 Flatten |
| 8 | 一個 block：Conv 改通道、Pool 砍面積、ReLU 不改形狀 |

## 附錄 G 實測原始輸出

`verify_cnn_activation_pooling.py` 的完整輸出（Python 3.15.1 / NumPy 2.5.4，本機執行）：

```text
------------------------------------------------------------------------
1. ReLU and its variants on the same input [-3.  -1.   0.   0.5  2. ]
   ReLU      : [0.  0.  0.  0.5 2. ]
   Leaky 0.1 : [-0.3 -0.1  0.   0.5  2. ]
   Leaky 0.01: [-0.03 -0.01  0.    0.5   2.  ]
   GELU      : [-0.0036 -0.1588  0.      0.3457  1.9546]
   x= -3.0  relu=0.000  leaky=-0.300  gelu=-0.0036
   x= -1.0  relu=0.000  leaky=-0.100  gelu=-0.1588
   x= -0.1  relu=0.000  leaky=-0.010  gelu=-0.0460
   x=  0.1  relu=0.100  leaky=0.100  gelu=0.0540
   x=  3.0  relu=3.000  leaky=3.000  gelu=2.9964
------------------------------------------------------------------------
2. two linear layers == one linear layer
   max |deep - flat| = 4.440892098500626e-16
------------------------------------------------------------------------
3. how sparse is a ReLU feature map?  (N(0,1) input, 1000x1000)
   zeros after ReLU: 50.0%
   zeros, standard normal: 50.0% (theory 50%)
------------------------------------------------------------------------
4. a dead unit: bias so negative that every input is clipped
   max projection over 512 samples: 51.08
   bias     0.00 -> all outputs zero? False  (max 51.08)
   bias    25.54 -> all outputs zero? False  (max 25.54)
   bias    52.08 -> all outputs zero? True   (max -1.00)
------------------------------------------------------------------------
5. pooling, the example used on the page
   input:
 [[1 1 2 4]
 [5 6 7 8]
 [3 2 1 0]
 [1 2 3 4]]
   2x2 max, stride 2 ->
 [[6 8]
 [3 4]]
   winners (row,col): [[(1, 1), (1, 3)], [(2, 0), (3, 3)]]
   average pooling  -> [3.25, 5.25, 2.0, 2.0]
   values 16 -> 4, reduction 75%
   one window [2 7; 1 5]: max 7, avg 3.75
------------------------------------------------------------------------
6. pooling output size  O = floor((W - k + 2p)/s) + 1
   4, k2, s2, pad0            -> 2
   4, k2, s1, pad0 (overlap)  -> 3
   4, k3, s2, pad1            -> 2
   28, k2, s2, pad0           -> 14
   7, k7, s1, pad0 (global)   -> 1
   overlap pooling on the 4x4 map ->
 [[6 7 8]
 [6 7 8]
 [3 3 4]]
   k3 s2 pad1 (pad with -inf) ->
 [[6 8]
 [6 8]]
------------------------------------------------------------------------
7. max-pool backward: the gradient only goes to the winner
   upstream grad:
 [[1. 2.]
 [3. 4.]]
   grad on the input map:
 [[0 0 0 0]
 [0 1 0 2]
 [3 0 0 0]
 [0 0 0 4]]
   sum preserved: 10.0 == 10.0
   finite-difference grad matches routed grad: True
------------------------------------------------------------------------
8. one CNN block, shape by shape (the example on the page)
   input            32 x 32 x 3
   Conv 3x3 x32 pad1  32 x 32 x 32  params (27+1)*32 = 896
   ReLU             32 x 32 x 32   params 0
   MaxPool 2x2 s2   16 x 16 x 32   params 0
   GAP on 7x7x512 -> 512           params 0
------------------------------------------------------------------------
```

---

*本頁為個人學習筆記整理；圖表為手繪內嵌 SVG，數字全部由附錄 G 的程式算出。*
