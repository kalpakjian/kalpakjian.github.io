# 卷積層的運作細節：kernel、通道、stride／padding、感受野與空洞卷積

> 前一篇〈[圖解 CNN](/cnn-illustrated/)〉把整個網路的資料流走過一遍；這一篇只拆**卷積層本身**。<br />一個卷積層同時做兩件事：<strong>提取局部模式</strong>，以及<strong>保留「這個模式在哪裡」</strong>。<br />下面每個數字都是本機用 NumPy 算的（Python 3.15.1 / NumPy 2.5.4），程式與原始輸出在附錄 G。<br />沒有互動測驗（附錄 E／F 從缺）；要回頭看全貌請走附錄 C 的連結。

<!-- CNVD-FIGURE:single -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 560" role="img" aria-label="單一輸出值的計算：5×5 輸入左上角 3×3 區塊與 3×3 kernel 逐元素相乘相加得到 8，整張輸出為 3×3 特徵圖"><defs><marker id="ard" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="558.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一個輸出值是怎麼算出來的</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5×5 影像、3×3 kernel、stride 1、不補邊 → 3×3 特徵圖</text><text x="60" y="126" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸入 5×5</text><text x="356" y="126" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">kernel 3×3</text><text x="532" y="126" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出 3×3</text><rect x="60" y="140" width="46" height="46" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="83.0" y="168.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="106" y="140" width="46" height="46" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="129.0" y="168.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><rect x="152" y="140" width="46" height="46" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="175.0" y="168.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><rect x="198" y="140" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="221.0" y="168.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="244" y="140" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="267.0" y="168.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="60" y="186" width="46" height="46" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="83.0" y="214.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="106" y="186" width="46" height="46" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="129.0" y="214.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="152" y="186" width="46" height="46" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="175.0" y="214.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><rect x="198" y="186" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="221.0" y="214.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><rect x="244" y="186" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="267.0" y="214.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="60" y="232" width="46" height="46" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="83.0" y="260.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><rect x="106" y="232" width="46" height="46" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="129.0" y="260.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="152" y="232" width="46" height="46" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="175.0" y="260.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="198" y="232" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="221.0" y="260.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="244" y="232" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="267.0" y="260.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="60" y="278" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="83.0" y="306.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="106" y="278" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="129.0" y="306.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><rect x="152" y="278" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="175.0" y="306.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="198" y="278" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="221.0" y="306.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><rect x="244" y="278" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="267.0" y="306.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="60" y="324" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="83.0" y="352.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="106" y="324" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="129.0" y="352.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="152" y="324" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="175.0" y="352.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="198" y="324" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="221.0" y="352.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><rect x="244" y="324" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="267.0" y="352.04" font-size="14" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="60" y="140" width="138" height="138" rx="6" fill="none" stroke="#e0a458" stroke-width="2.4"/><rect x="356" y="140" width="40" height="40" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="376.0" y="164.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="396" y="140" width="40" height="40" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="416.0" y="164.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="436" y="140" width="40" height="40" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="456.0" y="164.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="356" y="180" width="40" height="40" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="376.0" y="204.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="396" y="180" width="40" height="40" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="416.0" y="204.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="436" y="180" width="40" height="40" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="456.0" y="204.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="356" y="220" width="40" height="40" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="376.0" y="244.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="396" y="220" width="40" height="40" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="416.0" y="244.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="436" y="220" width="40" height="40" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="456.0" y="244.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="532" y="140" width="44" height="44" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="554.0" y="166.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text><rect x="576" y="140" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="598.0" y="166.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text><rect x="620" y="140" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="642.0" y="166.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text><rect x="532" y="184" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="554.0" y="210.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><rect x="576" y="184" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="598.0" y="210.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10</text><rect x="620" y="184" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="642.0" y="210.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text><rect x="532" y="228" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="554.0" y="254.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text><rect x="576" y="228" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="598.0" y="254.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text><rect x="620" y="228" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="642.0" y="254.86" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text><line x1="294" y1="200" x2="346" y2="200" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><line x1="482" y1="206" x2="524" y2="206" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><text x="700" y="176" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">滑一格再算一次：</text><text x="700" y="198" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">共 (5−3+1)² = 9 個位置</text><rect x="48" y="392" width="904" height="108" rx="12" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.4"/><text x="68" y="420" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">左上角那一格：逐元素相乘再相加</text><text x="68" y="448" font-size="12.5" fill="#e0a458" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">(1×1 + 2×0 + 3×1)  ＋  (0×0 + 1×1 + 2×0)  ＋  (2×1 + 0×0 + 1×1)  =  4 + 1 + 3  =  8</text><text x="68" y="476" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">bias 加在整個特徵圖上（這裡 bias = 0）；若 bias = 1，九格全部 +1。</text><text x="48" y="534" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出尺寸：O = ⌊(W − K)/S⌋ + 1 = ⌊(5 − 3)/1⌋ + 1 = 3</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">一個輸出值＝局部區塊與 kernel 逐元素相乘、全部相加，再加上 bias。滑一格就換算下一個值。</figcaption>
</figure>
<!-- /CNVD-FIGURE:single -->

## 1. 卷積層同時做兩件事

| 它做的事 | 靠什麼達成 | 代價 |
|---|---|---|
| 提取局部模式 | 一個小 kernel 只看 `k × k` 的鄰域 | 單層看不到大範圍 |
| 保留空間關係 | 輸出仍是二維網格，每個位置對應原圖的一塊 | 感受野隨層數成長 |
| 省參數 | 同一組權重滑過整張圖（權重共享） | 位置資訊變模糊 |

這三件事是同一組設計的結果，不是三個獨立技巧：**局部連接**讓參數量可控，**權重共享**再把它壓到跟影像大小無關，而「輸出仍是網格」讓下一層還能在空間上滑動。

## 2. 一個輸出值：逐元素相乘、相加、加 bias

### 2.1 手算一次

輸入是一張 5×5 的灰階圖，kernel 是 3×3、步幅 1、不補邊：

```text
輸入 5×5                 kernel 3×3
1 2 3 0 1               1 0 1
0 1 2 3 1               0 1 0
2 0 1 1 0               1 0 1
1 2 0 3 1
0 1 1 2 0
```

左上角的 3×3 區塊是 `[[1,2,3],[0,1,2],[2,0,1]]`，與 kernel 逐元素相乘再相加：

```text
(1×1 + 2×0 + 3×1) + (0×0 + 1×1 + 2×0) + (2×1 + 0×0 + 1×1)
= 4 + 1 + 3
= 8
```

這一格就是特徵圖左上角的 **8**。把 kernel 往右滑一格、再算一次，滑完整張圖（共 `(5 − 3 + 1)² = 9` 個位置）就得到實測的 3×3 特徵圖：

```text
[[ 8,  5,  8],
 [ 3, 10,  5],
 [ 6,  4,  5]]
```

最大值 10 出現在中間：那個位置的 3×3 區塊與 kernel 的「四角 + 中心」樣式最吻合。**特徵圖上的數值大，代表這個位置越像 kernel 想找的模式**——這就是「feature map 可以當偵測器輸出讀」的意思。

### 2.2 bias 的角色

每個輸出通道通常還有一個 bias，它加在整張特徵圖的每一格上：

```text
output[i, j] = Σ (patch × kernel) + bias
```

實測：上面那張特徵圖在 `bias = 1` 時，九格全部 +1（左上角由 8 變 9）。bias 的用途是**平移激活門檻**：同一個 kernel 在偏暗的圖上可能全部算出偏小的值，bias 讓它可以整體抬高或壓低，不必改權重。參數量因此是 `(k × k × C_in + 1) × C_out`，那個 `+1` 就是它。

## 3. 多通道輸入：通道是「加起來」的維度

<!-- CNVD-FIGURE:channels -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 430" role="img" aria-label="多通道卷積：三個輸入通道各配一個 3×3 kernel，分別算出 3、2、負 4，相加再加 bias 2 得到 3，輸出一格"><defs><marker id="ard" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="428.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">多通道：三個通道加起來才是一個值</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">kernel 的深度必須等於輸入通道數；這裡是 3×3×3，共 27 個權重</text><text x="60" y="153" font-size="11.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">通道 1</text><rect x="140" y="104" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="155.0" y="122.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="170" y="104" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="185.0" y="122.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="200" y="104" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="215.0" y="122.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="140" y="134" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="155.0" y="152.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="170" y="134" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="185.0" y="152.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="200" y="134" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="215.0" y="152.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="140" y="164" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="155.0" y="182.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="170" y="164" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="185.0" y="182.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="200" y="164" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="215.0" y="182.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><text x="250" y="148" font-size="15" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">×</text><rect x="268" y="104" width="30" height="30" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="283.0" y="122.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="298" y="104" width="30" height="30" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="313.0" y="122.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="328" y="104" width="30" height="30" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="343.0" y="122.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="268" y="134" width="30" height="30" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="283.0" y="152.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="298" y="134" width="30" height="30" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="313.0" y="152.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="328" y="134" width="30" height="30" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="343.0" y="152.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="268" y="164" width="30" height="30" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="283.0" y="182.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="298" y="164" width="30" height="30" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="313.0" y="182.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="328" y="164" width="30" height="30" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="343.0" y="182.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="378" y="148" font-size="15" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">=</text><text x="400" y="153" font-size="16" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><line x1="428" y1="149" x2="450" y2="149" stroke="#30363d" stroke-width="1.4"/><text x="60" y="249" font-size="11.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">通道 2</text><rect x="140" y="200" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="155.0" y="218.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><rect x="170" y="200" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="185.0" y="218.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="200" y="200" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="215.0" y="218.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="140" y="230" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="155.0" y="248.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="170" y="230" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="185.0" y="248.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="200" y="230" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="215.0" y="248.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><rect x="140" y="260" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="155.0" y="278.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="170" y="260" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="185.0" y="278.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="200" y="260" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="215.0" y="278.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="250" y="244" font-size="15" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">×</text><rect x="268" y="200" width="30" height="30" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="283.0" y="218.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="298" y="200" width="30" height="30" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="313.0" y="218.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="328" y="200" width="30" height="30" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="343.0" y="218.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="268" y="230" width="30" height="30" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="283.0" y="248.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="298" y="230" width="30" height="30" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="313.0" y="248.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="328" y="230" width="30" height="30" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="343.0" y="248.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="268" y="260" width="30" height="30" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="283.0" y="278.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="298" y="260" width="30" height="30" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="313.0" y="278.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="328" y="260" width="30" height="30" rx="4" fill="#58a6ff26" stroke="#58a6ff" stroke-width="1.6"/><text x="343.0" y="278.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><text x="378" y="244" font-size="15" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">=</text><text x="400" y="249" font-size="16" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><line x1="428" y1="245" x2="450" y2="245" stroke="#30363d" stroke-width="1.4"/><text x="60" y="345" font-size="11.5" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">通道 3</text><rect x="140" y="296" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="155.0" y="314.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="170" y="296" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="185.0" y="314.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="200" y="296" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="215.0" y="314.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="140" y="326" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="155.0" y="344.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="170" y="326" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="185.0" y="344.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="200" y="326" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="215.0" y="344.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="140" y="356" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="155.0" y="374.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="170" y="356" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="185.0" y="374.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="200" y="356" width="30" height="30" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="215.0" y="374.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="250" y="340" font-size="15" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">×</text><rect x="268" y="296" width="30" height="30" rx="4" fill="#c084fc26" stroke="#c084fc" stroke-width="1.6"/><text x="283.0" y="314.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="298" y="296" width="30" height="30" rx="4" fill="#c084fc26" stroke="#c084fc" stroke-width="1.6"/><text x="313.0" y="314.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-1</text><rect x="328" y="296" width="30" height="30" rx="4" fill="#c084fc26" stroke="#c084fc" stroke-width="1.6"/><text x="343.0" y="314.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="268" y="326" width="30" height="30" rx="4" fill="#c084fc26" stroke="#c084fc" stroke-width="1.6"/><text x="283.0" y="344.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-1</text><rect x="298" y="326" width="30" height="30" rx="4" fill="#c084fc26" stroke="#c084fc" stroke-width="1.6"/><text x="313.0" y="344.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="328" y="326" width="30" height="30" rx="4" fill="#c084fc26" stroke="#c084fc" stroke-width="1.6"/><text x="343.0" y="344.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-1</text><rect x="268" y="356" width="30" height="30" rx="4" fill="#c084fc26" stroke="#c084fc" stroke-width="1.6"/><text x="283.0" y="374.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="298" y="356" width="30" height="30" rx="4" fill="#c084fc26" stroke="#c084fc" stroke-width="1.6"/><text x="313.0" y="374.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-1</text><rect x="328" y="356" width="30" height="30" rx="4" fill="#c084fc26" stroke="#c084fc" stroke-width="1.6"/><text x="343.0" y="374.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="378" y="340" font-size="15" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">=</text><text x="400" y="345" font-size="16" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">−4</text><line x1="428" y1="341" x2="450" y2="341" stroke="#30363d" stroke-width="1.4"/><line x1="450" y1="149" x2="450" y2="341" stroke="#30363d" stroke-width="1.4"/><line x1="450" y1="245" x2="496" y2="245" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="500" y="190" width="180" height="92" rx="10" fill="#12181f" stroke="#e0a45899" stroke-width="1.5"/><text x="590" y="220" font-size="12.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Σ + bias 2</text><text x="590" y="252" font-size="12.5" fill="#e0a458" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3 + 2 − 4 + 2 = 3</text><line x1="686" y1="236" x2="720" y2="236" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="724" y="190" width="130" height="92" rx="10" fill="#12181f" stroke="#4ecdc499" stroke-width="1.5"/><text x="789" y="220" font-size="12" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出一格</text><text x="789" y="254" font-size="22" fill="#4ecdc4" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><text x="40" y="404" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">這一層若用 64 個 kernel，就有 64 張特徵圖（64 個輸出通道），每張 26×26（28×28 輸入、valid）。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">通道是「加起來」的維度：三個通道各算一份，總和才是一個輸出值；kernel 的深度必須等於輸入通道數。</figcaption>
</figure>
<!-- /CNVD-FIGURE:channels -->

### 3.1 形狀規則

彩色影像是 `H × W × 3`，所以一個 kernel 也必須是 `k × k × 3`——**每個輸入通道配一張 k × k 的子 kernel**。計算時三個通道各自乘加，再把三個結果**相加**，得到「一個」數字。

實測一組（3×3×3 的 kernel、bias = 2）：

| 通道 | 該通道的乘加結果 |
|---|---|
| 通道 1 | 3 |
| 通道 2 | 2 |
| 通道 3 | −4 |
| 小計 | 1 |
| 加 bias 2 | **3** |

所以「通道」在卷積裡是**被加總掉的維度**，不是被保留的維度。保留的是「kernel 的數量」：

```text
輸入   H  × W  × C_in
kernel k  × k  × C_in           ← 深度必須等於 C_in
輸出   H' × W' × C_out          ← C_out = kernel 的數量
```

### 3.2 為什麼 kernel 深度一定等於 C_in

因為要「逐元素相乘」，兩邊形狀必須一致。若輸入是 3 通道而 kernel 只有 3×3×1，那它只看得到其中一個通道，另外兩個通道的資訊就被丟掉了。反過來，**輸出通道數沒有限制**：想要 64 個輸出通道，就用 64 個獨立的 3×3×3 kernel，各自產生一張特徵圖，疊成 64 層。

## 4. 參數量：只跟 kernel 大小與通道數有關

```text
參數 = (k × k × C_in + 1) × C_out
```

實測幾個常見設定：

| 設定 | 權重 | bias | 合計 |
|---|---|---|---|
| 3×3、C_in = 3、C_out = 64 | 1,728 | 64 | **1,792** |
| 3×3、C_in = 3、C_out = 1（單一濾波器） | 27 | 1 | 28 |
| 3×3、C_in = 16、C_out = 32 | 4,608 | 32 | 4,640 |
| 5×5、C_in = 1、C_out = 6（LeNet-5 的 C1） | 150 | 6 | 156 |

兩個推論：

- **參數量與影像大小無關**。同一個 `3×3×3 → 64` 套在 28×28 或 224×224 上，都是 1,792 個參數；變多的是**乘加次數**（每個位置都要算一次）。
- **參數量跟通道數成正比**。`C_in`、`C_out` 各加倍，參數就是四倍。行動網路的瓶頸幾乎都來自這件事，所以才有 depthwise separable convolution。

## 5. stride 與 padding：控制輸出尺寸

<!-- CNVD-FIGURE:sizes -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 340" role="img" aria-label="四種 stride 與 padding 設定的輸出尺寸：28×28 輸入配 3×3 kernel，valid 得 26×26、same 得 28×28、stride 2 補 1 得 14×14、5×5 kernel 補 2 得 28×28"><defs><marker id="ard" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="338.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一張 28×28，四種設定</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">O = ⌊(W + 2P − K) / S⌋ + 1　（除不盡往下取整）</text><rect x="30" y="96" width="220" height="170" rx="8" fill="#12181f" stroke="#4ecdc488" stroke-width="1.5" opacity="0.9"/><text x="44" y="124" font-size="12" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">valid</text><text x="44" y="148" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">(28 − 3)/1 + 1</text><text x="44" y="192" font-size="22" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">26×26</text><text x="44" y="246" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">邊角像素只被掃到 1 次</text><rect x="265" y="96" width="220" height="170" rx="8" fill="#12181f" stroke="#58a6ff88" stroke-width="1.5" opacity="0.9"/><text x="279" y="124" font-size="12" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">same（p = 1）</text><text x="279" y="148" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">(28 + 2 − 3)/1 + 1</text><text x="279" y="192" font-size="22" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">28×28</text><text x="279" y="246" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">尺寸不變，邊界用 0 補</text><rect x="500" y="96" width="220" height="170" rx="8" fill="#12181f" stroke="#e0a45888" stroke-width="1.5" opacity="0.9"/><text x="514" y="124" font-size="12" fill="#e0a458" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">stride 2 + p = 1</text><text x="514" y="148" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">(28 + 2 − 3)/2 + 1</text><text x="514" y="192" font-size="22" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">14×14</text><text x="514" y="246" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一半解析度，常見於降採樣</text><rect x="735" y="96" width="220" height="170" rx="8" fill="#12181f" stroke="#c084fc88" stroke-width="1.5" opacity="0.9"/><text x="749" y="124" font-size="12" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5×5 kernel + p = 2</text><text x="749" y="148" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">(28 + 4 − 5)/1 + 1</text><text x="749" y="192" font-size="22" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">28×28</text><text x="749" y="246" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">大 kernel 也能維持 same</text><text x="40" y="308" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">same 的 padding 由 kernel 決定：K = 3 → P = 1、K = 5 → P = 2；偶數 kernel 湊不出真正的 same。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">同樣的 28×28 輸入，改 stride 與 padding 就是完全不同的輸出尺寸——公式只有一條。</figcaption>
</figure>
<!-- /CNVD-FIGURE:sizes -->

### 5.1 一條公式

```text
O = ⌊(W + 2P − K) / S⌋ + 1
```

| 符號 | 意思 | 常見值 |
|---|---|---|
| `W` | 輸入的寬或高 | 28、32、224 |
| `K` | kernel 邊長 | 3、5、7 |
| `P` | 單側補幾圈 0 | 0、1、2 |
| `S` | 步幅（每次滑幾格） | 1、2 |

實測（28×28 輸入）：

| 設定 | 算式 | 輸出 |
|---|---|---|
| 3×3、S1、P = 0（valid） | (28 − 3)/1 + 1 | 26×26 |
| 3×3、S1、P = 1（same） | (28 + 2 − 3)/1 + 1 | 28×28 |
| 3×3、S2、P = 1 | (28 + 2 − 3)/2 + 1 | 14×14 |
| 3×3、S2、P = 0 | (28 − 3)/2 + 1 | 13×13（除不盡，往下取整） |
| 5×5、S1、P = 2（same） | (28 + 4 − 5)/1 + 1 | 28×28 |

### 5.2 same 的 padding 怎麼決定

要讓輸出等於輸入（`S = 1`），解 `W + 2P − K + 1 = W` 得：

```text
P = (K − 1) / 2
```

所以 K = 3 → P = 1、K = 5 → P = 2、K = 7 → P = 3。**偶數 kernel 湊不出對稱的 same**（P 會是 .5），這就是實務上幾乎只用奇數 kernel 的原因之一。

padding 的另一個作用不是「尺寸」而是「邊界」：不補邊時，影像四角的像素只會被掃到 1 次，中央被掃 9 次，邊界資訊天然吃虧。補零讓邊角至少被多算幾次。

## 6. 感受野：一個輸出看多大範圍

<!-- CNVD-FIGURE:receptive -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 470" role="img" aria-label="感受野成長：9×9 輸入上疊四層 3×3 卷積，第 1 層看 3×3、第 2 層 5×5、第 3 層 7×7、第 4 層 9×9"><defs><marker id="ard" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="468.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">感受野：每疊一層就多看一圈</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">四層 3×3、stride 1 的卷積，最深那一層的一個神經元看得到整張 9×9</text><rect x="60" y="100" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="94" y="100" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="128" y="100" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="162" y="100" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="196" y="100" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="230" y="100" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="264" y="100" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="298" y="100" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="332" y="100" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="60" y="134" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="94" y="134" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="128" y="134" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="162" y="134" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="196" y="134" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="230" y="134" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="264" y="134" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="298" y="134" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="332" y="134" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="60" y="168" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="94" y="168" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="128" y="168" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="162" y="168" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="196" y="168" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="230" y="168" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="264" y="168" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="298" y="168" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="332" y="168" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="60" y="202" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="94" y="202" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="128" y="202" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="162" y="202" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="196" y="202" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="230" y="202" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="264" y="202" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="298" y="202" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="332" y="202" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="60" y="236" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="94" y="236" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="128" y="236" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="162" y="236" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="196" y="236" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="230" y="236" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="264" y="236" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="298" y="236" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="332" y="236" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="60" y="270" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="94" y="270" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="128" y="270" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="162" y="270" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="196" y="270" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="230" y="270" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="264" y="270" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="298" y="270" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="332" y="270" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="60" y="304" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="94" y="304" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="128" y="304" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="162" y="304" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="196" y="304" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="230" y="304" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="264" y="304" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="298" y="304" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="332" y="304" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="60" y="338" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="94" y="338" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="128" y="338" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="162" y="338" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="196" y="338" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="230" y="338" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="264" y="338" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="298" y="338" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="332" y="338" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="60" y="372" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="94" y="372" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="128" y="372" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="162" y="372" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="196" y="372" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="230" y="372" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="264" y="372" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="298" y="372" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="332" y="372" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.45"/><rect x="162" y="202" width="102" height="102" rx="4" fill="#4ecdc41a" stroke="#4ecdc4" stroke-width="2.2"/><rect x="128" y="168" width="170" height="170" rx="4" fill="none" stroke="#58a6ff" stroke-width="2.2"/><rect x="94" y="134" width="238" height="238" rx="4" fill="none" stroke="#c084fc" stroke-width="2.2"/><rect x="60" y="100" width="306" height="306" rx="4" fill="none" stroke="#e0a458" stroke-width="1.6"/><rect x="430" y="119" width="12" height="12" rx="3" fill="#4ecdc444" stroke="#4ecdc4" stroke-width="1.5"/><text x="452" y="130" font-size="12" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">第 1 層：3×3</text><rect x="430" y="163" width="12" height="12" rx="3" fill="#58a6ff44" stroke="#58a6ff" stroke-width="1.5"/><text x="452" y="174" font-size="12" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">第 2 層：5×5</text><rect x="430" y="207" width="12" height="12" rx="3" fill="#c084fc44" stroke="#c084fc" stroke-width="1.5"/><text x="452" y="218" font-size="12" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">第 3 層：7×7</text><rect x="430" y="251" width="12" height="12" rx="3" fill="#e0a45844" stroke="#e0a458" stroke-width="1.5"/><text x="452" y="262" font-size="12" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">第 4 層：9×9</text><text x="430" y="322" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RFₙ = RFₙ₋₁ + (K − 1) × jump</text><text x="430" y="344" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">jump = 前面所有 stride 的乘積</text><text x="60" y="432" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">若每層都 stride 2：3 → 7 → 15 → 31（用解析度換視野，ResNet 之後很常見）</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">感受野隨層數長大：每多一層 3×3、stride 1，就多看到外圍一圈。</figcaption>
</figure>
<!-- /CNVD-FIGURE:receptive -->

單層 3×3 卷積，每個輸出只直接依賴輸入的 3×3；但疊起來之後，深層的神經元會**間接**看到更大的原始區域：

| 層數（每層 3×3、stride 1） | 感受野 |
|---|---|
| 1 層 | 3×3 |
| 2 層 | 5×5 |
| 3 層 | 7×7 |
| 4 層 | 9×9 |

遞推式是

```text
RFₙ = RFₙ₋₁ + (K − 1) × jump         jump = 前面所有 stride 的乘積
```

`stride = 1` 時 `jump` 恆為 1，所以每多一層就多兩圈。**一旦有 stride 2，jump 開始翻倍**：每層 3×3、stride 2 的堆疊，感受野依序是 3 → 7 → 15 → 31，但解析度也一路砍半。這就是「用解析度換視野」的取捨。

順帶一個常被拿來比較的帳：**兩層 3×3 的感受野等於一層 5×5，但參數只要 `2 × 9 = 18`（同通道數），5×5 要 25，而且兩層多了一次非線性**。這是 VGG 之後「小 kernel 疊深」的理由。

## 7. 空洞卷積：不增參數也能擴大視野

<!-- CNVD-FIGURE:dilation -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 430" role="img" aria-label="空洞卷積：3×3 kernel 在 dilation 1 時覆蓋 3×3、dilation 2 時覆蓋 5×5，但兩者都只有 9 個權重"><defs><marker id="ard" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="428.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">空洞卷積：跳著看，視野變大、參數不變</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3×3 kernel、dilation 2 → 有效覆蓋 5×5，但還是只有 9 個權重</text><text x="60" y="118" font-size="12" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">d = 1（一般卷積）</text><rect x="60" y="136" width="40" height="40" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="80.0" y="160.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="100" y="136" width="40" height="40" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="120.0" y="160.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="140" y="136" width="40" height="40" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="160.0" y="160.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="60" y="176" width="40" height="40" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="80.0" y="200.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="100" y="176" width="40" height="40" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="120.0" y="200.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="140" y="176" width="40" height="40" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="160.0" y="200.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="60" y="216" width="40" height="40" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="80.0" y="240.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="100" y="216" width="40" height="40" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="120.0" y="240.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="140" y="216" width="40" height="40" rx="4" fill="#4ecdc426" stroke="#4ecdc4" stroke-width="1.6"/><text x="160.0" y="240.32" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="54" y="130" width="124" height="124" rx="6" fill="none" stroke="#4ecdc466" stroke-width="1.2"/><text x="60" y="280" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">覆蓋 3×3</text><text x="280" y="104" font-size="12" fill="#e0a458" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">d = 2（空洞卷積）</text><rect x="280" y="122" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="320" y="122" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="360" y="122" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="400" y="122" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="440" y="122" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="280" y="162" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="320" y="162" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="360" y="162" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="400" y="162" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="440" y="162" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="280" y="202" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="320" y="202" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="360" y="202" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="400" y="202" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="440" y="202" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="280" y="242" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="320" y="242" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="360" y="242" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="400" y="242" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="440" y="242" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="280" y="282" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="320" y="282" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="360" y="282" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="400" y="282" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="440" y="282" width="40" height="40" rx="3" fill="none" stroke="#30363d" stroke-width="0.8" opacity="0.4"/><rect x="284" y="126" width="32" height="32" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.4"/><text x="300" y="147" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="364" y="126" width="32" height="32" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.4"/><text x="380" y="147" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="444" y="126" width="32" height="32" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.4"/><text x="460" y="147" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="284" y="206" width="32" height="32" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.4"/><text x="300" y="227" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="364" y="206" width="32" height="32" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.4"/><text x="380" y="227" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="444" y="206" width="32" height="32" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.4"/><text x="460" y="227" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="284" y="286" width="32" height="32" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.4"/><text x="300" y="307" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="364" y="286" width="32" height="32" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.4"/><text x="380" y="307" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="444" y="286" width="32" height="32" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.4"/><text x="460" y="307" font-size="12" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="274" y="116" width="204" height="204" rx="6" fill="none" stroke="#e0a45866" stroke-width="1.2"/><text x="280" y="350" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">覆蓋 5×5，同一組 9 個權重</text><text x="540" y="140" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">k_eff = d × (k − 1) + 1 = 2 × 2 + 1 = 5</text><text x="540" y="176" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">28×28 輸入、p = 0 → 輸出 24×24</text><text x="540" y="200" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">28×28 輸入、p = 2 → 輸出 28×28</text><text x="540" y="236" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">代價：跳過的鄰居像素仍然看不到，細節會被略過；</text><text x="540" y="258" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">所以實務上常和一般卷積交錯使用（hybrid）。</text><text x="40" y="404" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">把 d 想成「kernel 元素之間的間隔」；d = 1 就退化成一般卷積。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">空洞卷積用「跳著看」換視野：覆蓋範圍變 5×5，權重還是 9 個。</figcaption>
</figure>
<!-- /CNVD-FIGURE:dilation -->

空洞（擴張）卷積在 kernel 元素之間插入間隔。`k × k` 的 kernel、dilation 為 `d` 時，有效覆蓋範圍是

```text
k_eff = d × (k − 1) + 1
```

| kernel | d | 有效覆蓋 | 權重數 |
|---|---|---|---|
| 3×3 | 1 | 3×3 | 9 |
| 3×3 | 2 | 5×5 | 9 |
| 3×3 | 3 | 7×7 | 9 |
| 3×3 | 4 | 9×9 | 9 |

含 dilation 的完整輸出尺寸公式：

```text
O = ⌊(W + 2P − d(k − 1) − 1) / S⌋ + 1
```

`d = 1` 時就退化成一般卷積。實測（28×28、3×3）：

| d | P | 輸出 |
|---|---|---|
| 1 | 0 | 26×26 |
| 1 | 1 | 28×28 |
| 2 | 0 | 24×24 |
| 2 | 2 | 28×28 |

代價要講清楚：**跳過去的鄰居像素仍然看不到**。d = 2 的 3×3 kernel 只看 5×5 範圍裡間隔著的那 9 格，中間的格子完全沒讀到；所以實務上不會整層都用大 dilation，而是「一般卷積與空洞卷積交錯」（hybrid dilation），或像 DeepLab 那樣堆 1, 2, 4 的組合，讓多個尺度同時被覆蓋。這也是語意分割需要大上下文時的標準做法。

## 8. 一層卷積的完整流程

1. 取一組 `k × k × C_in` 的 kernel（這一層有 `C_out` 組）。
2. 在輸入的空間維度上，以 stride 滑動（是否補邊由 padding 決定）。
3. 每個位置把 kernel 與對應的多通道區塊**逐元素相乘再加總**。
4. 加上 bias。
5. 對每個 kernel 重複 → 得到 `C_out` 張特徵圖。
6. 接非線性（通常是 ReLU）。

值得記住的是第 3 步「加總」的範圍：**跨通道加總、跨位置不加總**。所以輸出仍然是多張二維圖，位置資訊還在；被消掉的是「是哪個輸入通道貢獻的」。

## 9. 六個常見誤解

| 誤解 | 事實 |
|---|---|
| kernel 越大越強 | 兩層 3×3 = 一層 5×5 的感受野，參數 18 vs 25，還多一層非線性 |
| 輸出通道數等於輸入通道數 | 輸出通道數＝kernel 的數量，與 `C_in` 無關 |
| kernel 可以是 3×3×1 去讀彩色圖 | 深度必須等於 `C_in`，否則只看得到一個通道 |
| padding 是補在輸出 | padding 補在輸入邊緣，公式裡要乘 2 |
| stride 越大輸出越大 | 相反：stride 越大，滑的次數越少、輸出越小 |
| 感受野等於輸出尺寸 | 兩件事無關：輸出尺寸看公式，感受野看層數與 stride |

## 附錄 A 速查表

| 想問的事 | 答案 |
|---|---|
| 一個輸出值 | `Σ(patch × kernel) + bias` |
| kernel 深度 | 必須等於 `C_in` |
| 輸出通道數 | kernel 的數量 `C_out` |
| 參數量 | `(k × k × C_in + 1) × C_out` |
| 輸出尺寸 | `O = ⌊(W + 2P − d(k−1) − 1) / S⌋ + 1` |
| same 的 padding | `P = (K − 1) / 2`（只對奇數 K 成立） |
| 感受野 | `RFₙ = RFₙ₋₁ + (K − 1) × jump` |
| 空洞卷積覆蓋範圍 | `d(k − 1) + 1` |
| 通道在哪裡消失 | 在「跨通道加總」那一步，不是被池化掉 |

## 附錄 B 常見錯誤

1. **忘記 bias 也要乘 kernel 數量**：`C_out` 個 kernel 就有 `C_out` 個 bias。
2. **把 padding 寫成 `+P` 而不是 `+2P`**：左右各補一次。
3. **除不盡時四捨五入**：公式是 floor，往下取整。
4. **以為 stride 2 一定會整除**：`(28 − 3)/2 + 1 = 13`，不是 13.5。
5. **把 dilation 當成「kernel 變大」**：權重數量沒變，變的只是取樣間隔。
6. **用 `same` 就以為邊界資訊沒問題**：補的是 0，不是真的鄰居，邊界仍然比中央「看」得少。

## 附錄 C 延伸閱讀與離線使用

站內：

- [CAM vs Grad-CAM：同一個熱圖，只差權重怎麼來](/cnn-cam-vs-gradcam/)——九個面向的對照與 α 的實測
- [Grad-CAM：用梯度算出模型在看哪裡](/cnn-gradcam/)——七個步驟、ReLU、選層，與 CAM 的等價條件
- [CAM：用 GAP 算出模型在看哪裡](/cnn-cam/)——GAP 之後的分類權重怎麼變成熱圖（含 Grad-CAM）
- [為什麼現代 CNN 常不用全連接層](/cnn-gap-head/)——GAP 分類頭：25,089,000 → 513,000 個參數
- [卷積層 vs 全連接層](/cnn-conv-vs-fc/)——系列總整理：參數、算力與平移特性的對照
- [圖解 CNN：從 5×5 小圖算到類別機率](/cnn-illustrated/)——整體資料流、ReLU、池化、softmax
- [激活函數與池化層](/cnn-activation-pooling/)——本篇的續篇：ReLU 家族、Max／Average Pooling、GAP
- [CNN 學習筆記（Lesson 6）](/cnn-notes/)——卷積的數學、LeNet-5、卷積的反向傳播
- [全連接層的運作](/cnn-fully-connected/)——最後一哩：Wx + b、flatten、softmax
- [CNN 2 學習筆記（Lesson 7）](/cnn2-notes/)——輸出體積、stride、感受野、空洞卷積的課堂版本
- [CNN 專題：十個實驗](/cnn-lab/)——把這些層真的訓練起來

站外：

- [Dive into Deep Learning（繁中）— 填充與步幅](https://zh.d2l.ai/chapter_convolutional-neural-networks/padding-and-strides.html)
- [A guide to convolution arithmetic for deep learning（Dumoulin & Visin, 2018）](https://arxiv.org/abs/1603.07285)

離線：本頁是**單一 HTML 檔、零外部資源**；原始 Markdown 在同一層。

## 附錄 D 一頁精華（考前 10 分鐘）

| # | 記這一條 |
|---|---|
| 1 | 一個值＝`Σ(patch × kernel) + bias`，跨通道加總、跨位置不加總 |
| 2 | kernel 深度 = `C_in`；輸出通道 = kernel 數量 |
| 3 | 參數 `(k²·C_in + 1)·C_out`，與影像大小無關 |
| 4 | `O = ⌊(W + 2P − d(k−1) − 1)/S⌋ + 1` |
| 5 | same 的 `P = (K − 1)/2`，所以幾乎只用奇數 kernel |
| 6 | 感受野 `RFₙ = RFₙ₋₁ + (K − 1)·jump`，stride 會讓 jump 翻倍 |
| 7 | 空洞卷積覆蓋 `d(k−1) + 1`，權重不變但細節會被跳過 |

## 附錄 G 實測原始輸出

`verify_cnn_conv_details.py` 的完整輸出（Python 3.15.1 / NumPy 2.5.4，本機執行）：

```text
------------------------------------------------------------------------
1. 5x5 input, 3x3 kernel, stride 1, no padding, bias 0
   input:
 [[1 2 3 0 1]
 [0 1 2 3 1]
 [2 0 1 1 0]
 [1 2 0 3 1]
 [0 1 1 2 0]]
   top-left 3x3:
 [[1 2 3]
 [0 1 2]
 [2 0 1]]
   kernel:
 [[1 0 1]
 [0 1 0]
 [1 0 1]]
   feature map:
 [[ 8  5  8]
 [ 3 10  5]
 [ 6  4  5]]
   top-left cell = 8
   with bias 1  = 9
------------------------------------------------------------------------
2. output size  O = floor((W + 2P - d(k-1) - 1) / S) + 1
   28,3x3,s1,pad0 (valid)       -> 26
   28,3x3,s1,pad1 (same)        -> 28
   28,3x3,s2,pad1               -> 14
   28,5x5,s1,pad2 (same)        -> 28
   28,3x3,s2,pad0               -> 13
------------------------------------------------------------------------
3. dilated kernel footprint  k_eff = d(k-1) + 1
   3x3, d=1 -> footprint 3 (weights still 9)
   3x3, d=2 -> footprint 5 (weights still 9)
   3x3, d=3 -> footprint 7 (weights still 9)
   3x3, d=4 -> footprint 9 (weights still 9)
   28x28, 3x3, d=1, s1, pad0 -> out 26
   28x28, 3x3, d=2, s1, pad0 -> out 24
   28x28, 3x3, d=2, s1, pad2 -> out 28
------------------------------------------------------------------------
4. parameter counts   (k*k*C_in + 1) * C_out
   3x3, C_in=3, C_out=64 -> weights 1728 + bias 64 = 1792
   3x3, C_in=3, C_out=1 -> weights 27 + bias 1 = 28
   3x3, C_in=16, C_out=32 -> weights 4608 + bias 32 = 4640
   5x5, C_in=1, C_out=6 -> weights 150 + bias 6 = 156
------------------------------------------------------------------------
5. receptive field, stacked 3x3 stride 1
   after layer 1: 3 x 3
   after layer 2: 5 x 5
   after layer 3: 7 x 7
   after layer 4: 9 x 9
   same stack, every layer stride 2:
   after layer 1: rf 3, jump 2
   after layer 2: rf 7, jump 4
   after layer 3: rf 15, jump 8
   after layer 4: rf 31, jump 16
------------------------------------------------------------------------
6. multi-channel kernel: 3 channels summed into one value
   per-channel sums: [3, 2, -4] -> total 1 | + bias 2 = 3
------------------------------------------------------------------------
```

---

*本頁為個人學習筆記整理；圖表為手繪內嵌 SVG，數字全部由附錄 G 的程式算出。*
