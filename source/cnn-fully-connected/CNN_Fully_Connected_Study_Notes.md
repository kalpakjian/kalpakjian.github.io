# 全連接層的運作：Flatten、Wx + b 與 Softmax

> 系列第四篇。前三篇談卷積與池化（[圖解 CNN](/cnn-illustrated/)、[卷積層的運作細節](/cnn-conv-details/)、[激活函數與池化層](/cnn-activation-pooling/)），<br />這一篇談最後一哩：<strong>把特徵向量變成類別分數的全連接層</strong>，以及接在它後面的 softmax。<br />全連接層的參數量往往是整個網路最大的來源——這一篇會把「為什麼」算給你看。<br />所有數字都是本機用 NumPy 算的（Python 3.15.1 / NumPy 2.5.4），原始輸出在附錄 G。

<!-- CNFC-FIGURE:dense -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 400" role="img" aria-label="全連接層的形狀：3×4 的權重矩陣乘上 4 維輸入再加 3 維 bias，得到 3 個 logits 2.4、1.2、負 0.7"><defs><marker id="arf" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="398.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全連接層＝一次矩陣乘法</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4 個輸入、3 個輸出：W 是 3×4、b 是 3，輸出 3 個 logits</text><text x="60" y="118" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">W（m×n = 3×4）</text><rect x="60" y="130" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="83.0" y="156.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.2</text><rect x="106" y="130" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="129.0" y="156.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.4</text><rect x="152" y="130" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="175.0" y="156.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-0.1</text><rect x="198" y="130" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="221.0" y="156.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.5</text><rect x="60" y="176" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="83.0" y="202.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.7</text><rect x="106" y="176" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="129.0" y="202.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-0.3</text><rect x="152" y="176" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="175.0" y="202.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.2</text><rect x="198" y="176" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="221.0" y="202.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.1</text><rect x="60" y="222" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="83.0" y="248.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-0.5</text><rect x="106" y="222" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="129.0" y="248.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.6</text><rect x="152" y="222" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="175.0" y="248.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.8</text><rect x="198" y="222" width="46" height="46" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="221.0" y="248.96" font-size="11" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-0.2</text><text x="258" y="208" font-size="16" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">·</text><rect x="276" y="130" width="46" height="46" rx="4" fill="#12181f" stroke="#58a6ffaa" stroke-width="1.3"/><text x="299.0" y="158.0" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text><rect x="276" y="176" width="46" height="46" rx="4" fill="#12181f" stroke="#58a6ffaa" stroke-width="1.3"/><text x="299.0" y="204.0" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text><rect x="276" y="222" width="46" height="46" rx="4" fill="#12181f" stroke="#58a6ffaa" stroke-width="1.3"/><text x="299.0" y="250.0" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><rect x="276" y="268" width="46" height="46" rx="4" fill="#12181f" stroke="#58a6ffaa" stroke-width="1.3"/><text x="299.0" y="296.0" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text><text x="299.0" y="120" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">x</text><text x="340" y="208" font-size="16" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">=</text><rect x="356" y="130" width="46" height="46" rx="4" fill="#12181f" stroke="#4ecdc4aa" stroke-width="1.3"/><text x="379.0" y="158.0" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2.4</text><rect x="356" y="176" width="46" height="46" rx="4" fill="#12181f" stroke="#4ecdc4aa" stroke-width="1.3"/><text x="379.0" y="204.0" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.2</text><rect x="356" y="222" width="46" height="46" rx="4" fill="#12181f" stroke="#4ecdc4aa" stroke-width="1.3"/><text x="379.0" y="250.0" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">−0.7</text><text x="379.0" y="120" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Wx</text><text x="424" y="208" font-size="16" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+</text><rect x="440" y="130" width="46" height="46" rx="4" fill="#12181f" stroke="#e0a458aa" stroke-width="1.3"/><text x="463.0" y="158.0" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.1</text><rect x="440" y="176" width="46" height="46" rx="4" fill="#12181f" stroke="#e0a458aa" stroke-width="1.3"/><text x="463.0" y="204.0" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">−0.2</text><rect x="440" y="222" width="46" height="46" rx="4" fill="#12181f" stroke="#e0a458aa" stroke-width="1.3"/><text x="463.0" y="250.0" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.3</text><text x="463.0" y="120" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">b</text><text x="508" y="208" font-size="16" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">=</text><rect x="524" y="130" width="46" height="46" rx="4" fill="#12181f" stroke="#ff7b72aa" stroke-width="1.3"/><text x="547.0" y="158.0" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2.4</text><rect x="524" y="176" width="46" height="46" rx="4" fill="#12181f" stroke="#ff7b72aa" stroke-width="1.3"/><text x="547.0" y="204.0" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.2</text><rect x="524" y="222" width="46" height="46" rx="4" fill="#12181f" stroke="#ff7b72aa" stroke-width="1.3"/><text x="547.0" y="250.0" font-size="13.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">−0.7</text><text x="547.0" y="120" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">logits</text><rect x="620" y="116" width="340" height="140" rx="12" fill="#1c2230" stroke="#4ecdc455" stroke-width="1.4"/><text x="640" y="144" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">z₁ 怎麼來的（第一列 · x + b₁）</text><text x="640" y="172" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.2×2 + 0.4×1 + (−0.1)×0 + 0.5×3</text><text x="640" y="194" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">= 0.4 + 0.4 + 0 + 1.5 = 2.3</text><text x="640" y="218" font-size="12.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2.3 + 0.1 = 2.4</text><text x="640" y="242" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">三列各自做一次，就是 z</text><text x="40" y="336" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每一個輸出都連到全部 4 個輸入：W 有 12 個權重、b 有 3 個，合計 15 個參數。</text><text x="40" y="360" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">z₃ 是負的——logits 可以是任意實數，要經過 softmax 才是機率。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">全連接層就是一次矩陣乘法：W（3×4）乘 x（4）加 b（3）。每個輸出神經元都看得到全部 4 個輸入。</figcaption>
</figure>
<!-- /CNFC-FIGURE:dense -->

## 1. 一句話：矩陣乘法加 bias

```text
z = W x + b
```

| 符號 | 意義 | 形狀 |
|---|---|---|
| `x` | 前一層（展平後）的特徵向量 | `n × 1` |
| `W` | 權重矩陣 | `m × n` |
| `b` | bias | `m × 1` |
| `z` | 輸出 logits | `m × 1` |

逐元素寫出來就是「每個輸入乘以對應權重、全部相加、再加 bias」：

```text
z_j = Σ_i ( w[j, i] × x_i ) + b_j        i = 1..n, j = 1..m
```

「全連接」的意思就在這裡：**每一個輸出 j 都連到每一個輸入 i**，所以 `W` 是一個完整的 `m × n` 矩陣——沒有任何位置被共用。

## 2. 手算一個 4 → 3 的例子

輸入 `x = [2, 1, 0, 3]`，`W` 是 3×4、`b = [0.1, −0.2, 0.3]`：

```text
z₁ = (0.2×2 + 0.4×1 + (−0.1)×0 + 0.5×3) + 0.1
   = 0.4 + 0.4 + 0 + 1.5 + 0.1 = 2.4

z₂ = (0.7×2 + (−0.3)×1 + 0.2×0 + 0.1×3) + (−0.2)
   = 1.4 − 0.3 + 0 + 0.3 − 0.2 = 1.2

z₃ = ((−0.5)×2 + 0.6×1 + 0.8×0 + (−0.2)×3) + 0.3
   = −1.0 + 0.6 + 0 − 0.6 + 0.3 = −0.7
```

所以實測的 logits 是 **`[2.4, 1.2, −0.7]`**。

### 2.1 兩個最容易算錯的地方

| 錯誤 | 後果 |
|---|---|
| 忘了加 bias，或把 bias 加在「整張矩陣」上 | 第一列就少了 0.1；第二、三列會偏掉 0.2／0.3 |
| 把 `W` 的行列方向搞反（用 `x·W` 而不是 `W·x`） | 形狀直接對不上：`(4,)` 乘 `(3,4)` 不合法 |

還有一個常被忽略的事實：**logits 可以是負的**。`z₃ = −0.7` 完全正常，它只是還沒被壓成機率的分數。

### 2.2 這個例子的參數量

`W` 有 3×4 = **12** 個權重，`b` 有 **3** 個，合計 **15** 個參數——而且跟輸入有幾個樣本完全無關。這也是為什麼「同一個全連接層」可以套在任意 batch 上：參數只在 `W` 與 `b`。

## 3. Flatten：只是換形狀

<!-- CNFC-FIGURE:flatten -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 350" role="img" aria-label="7×7×64 的特徵圖展平成 3136 維向量，接 Dense 128 再 Dense 10 加 softmax；展平本身沒有參數"><defs><marker id="arf" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="348.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Flatten：只重排、不運算</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7×7×64 的特徵圖展平成 3136 維；這一步沒有參數</text><rect x="55" y="130" width="96" height="96" rx="6" fill="#12181f" stroke="#4ecdc488" stroke-width="1.4" opacity="0.95"/><text x="103" y="184" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7×7</text><rect x="166" y="130" width="96" height="96" rx="6" fill="#12181f" stroke="#4ecdc488" stroke-width="1.4" opacity="0.95"/><text x="214" y="184" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7×7</text><rect x="277" y="130" width="96" height="96" rx="6" fill="#12181f" stroke="#4ecdc488" stroke-width="1.4" opacity="0.95"/><text x="325" y="184" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7×7</text><text x="55" y="256" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">…共 64 個通道</text><line x1="392" y1="178" x2="430" y2="178" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><text x="411" y="160" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">flatten</text><rect x="436" y="156" width="14" height="44" rx="3" fill="#12181f" stroke="#58a6ff88" stroke-width="1.1"/><rect x="452" y="156" width="14" height="44" rx="3" fill="#12181f" stroke="#58a6ff88" stroke-width="1.1"/><rect x="468" y="156" width="14" height="44" rx="3" fill="#12181f" stroke="#58a6ff88" stroke-width="1.1"/><rect x="484" y="156" width="14" height="44" rx="3" fill="#12181f" stroke="#58a6ff88" stroke-width="1.1"/><rect x="500" y="156" width="14" height="44" rx="3" fill="#12181f" stroke="#58a6ff88" stroke-width="1.1"/><rect x="516" y="156" width="14" height="44" rx="3" fill="#12181f" stroke="#58a6ff88" stroke-width="1.1"/><rect x="532" y="156" width="14" height="44" rx="3" fill="#12181f" stroke="#58a6ff88" stroke-width="1.1"/><rect x="548" y="156" width="14" height="44" rx="3" fill="#12181f" stroke="#58a6ff88" stroke-width="1.1"/><rect x="564" y="156" width="14" height="44" rx="3" fill="#12181f" stroke="#58a6ff88" stroke-width="1.1"/><rect x="580" y="156" width="14" height="44" rx="3" fill="#12181f" stroke="#58a6ff88" stroke-width="1.1"/><rect x="596" y="156" width="14" height="44" rx="3" fill="#12181f" stroke="#58a6ff88" stroke-width="1.1"/><rect x="612" y="156" width="14" height="44" rx="3" fill="#12181f" stroke="#58a6ff88" stroke-width="1.1"/><text x="436" y="148" font-size="11" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3136 維</text><line x1="636" y1="178" x2="668" y2="178" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="672" y="138" width="120" height="80" rx="9" fill="#12181f" stroke="#4ecdc4" stroke-width="1.6"/><text x="732" y="172" font-size="12" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Dense 128</text><text x="732" y="194" font-size="10.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">參數 50,240</text><line x1="798" y1="178" x2="830" y2="178" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="834" y="138" width="136" height="80" rx="9" fill="#12181f" stroke="#ff7b72" stroke-width="1.6"/><text x="902" y="170" font-size="12" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Dense 10</text><text x="902" y="190" font-size="10.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+ softmax</text><text x="40" y="316" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">參數全在兩個 Dense：3136×128 + 128 = 401,536，128×10 + 10 = 1,290。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">Flatten 只重排資料、不做運算；真正花參數的是後面的 Dense。</figcaption>
</figure>
<!-- /CNFC-FIGURE:flatten -->

卷積與池化的輸出是三維張量（`H × W × C`）。全連接層只吃向量，所以中間要插一步 **flatten**：

```text
7 × 7 × 64  →  3136
```

三件要記住的事：

- **flatten 沒有參數**，它只是把 `(7, 7, 64)` 的數字按固定順序攤成 `3136` 個。
- **順序必須固定**：PyTorch 是 channel-major（先 H、再 W、再 C），換框架要確認，否則權重與特徵對不上。
- **flatten 之後，空間關係就沒了**：`3136` 這個向量裡，第 1 個數字與第 2 個數字是鄰居這件事不再被編碼。這是全連接層「表達能力強、但不保留空間結構」的根源。

## 4. 參數量為什麼爆炸

<!-- CNFC-FIGURE:params -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 380" role="img" aria-label="參數量比較：小 CNN 的卷積層共 1248 個參數，全連接層共 50890 個，占 97.6%"><defs><marker id="arf" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="378.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">參數幾乎都在全連接層</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個 MNIST 小 CNN：總計 52,138 個參數，全連接占 50,890（97.6%）</text><text x="340" y="127" font-size="11.5" fill="#e6edf3" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">卷積層（3×3×1→8、3×3×8→16）</text><rect x="360" y="110" width="12.9171974522293" height="24" rx="4" fill="#4ecdc4" stroke="none" stroke-width="1" opacity="0.85"/><text x="382.9171974522293" y="127" font-size="12" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1,248</text><text x="340" y="185" font-size="11.5" fill="#e6edf3" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全連接 784 → 64</text><rect x="360" y="168" width="520.0" height="24" rx="4" fill="#ff7b72" stroke="none" stroke-width="1" opacity="0.85"/><text x="890.0" y="185" font-size="12" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">50,240</text><text x="340" y="243" font-size="11.5" fill="#e6edf3" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全連接 64 → 10</text><rect x="360" y="226" width="6.727707006369426" height="24" rx="4" fill="#e0a458" stroke="none" stroke-width="1" opacity="0.85"/><text x="376.7277070063694" y="243" font-size="12" fill="#e0a458" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">650</text><text x="40" y="320" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">另一組對照：3136 → 128 是 401,536 個參數；同樣輸入直接接 10 類只要 31,370 個（差 12.8 倍）。</text><text x="40" y="344" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全連接是 m×n + m；卷積是 (k×k×C_in + 1)×C_out，與影像大小無關。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">同一個小 CNN：卷積層 1,248 個參數，全連接層 50,890 個——占全部參數 97.6%。</figcaption>
</figure>
<!-- /CNFC-FIGURE:params -->

```text
參數 = m × n（權重） + m（bias）
```

| 這一層 | 參數 |
|---|---|
| 3136 → 128 | 401,408 + 128 = **401,536** |
| 3136 → 10（直接分類） | 31,360 + 10 = 31,370 |
| 784 → 64 | 50,176 + 64 = 50,240 |
| 64 → 10 | 640 + 10 = 650 |
| 128 → 10 | 1,280 + 10 = **1,290** |

把它放進一個完整的小 CNN 看比例（MNIST 版本：兩層卷積 + 784→64→10）：

| 部分 | 參數 | 佔比 |
|---|---|---|
| 卷積層（兩層合計） | 1,248 | 2.4% |
| 全連接層（784→64 與 64→10） | 50,890 | **97.6%** |
| 合計 | 52,138 | 100% |

這就是「CNN 參數少」這句話的真正範圍：**少的是卷積層，不是整個網路**。也因為如此，現代 CNN 會用全域平均池化（GAP）或 `1×1` 卷積取代那個巨大的全連接層（見 §9）。

## 5. Softmax：分數變成機率

<!-- CNFC-FIGURE:softmax -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 420" role="img" aria-label="softmax 把 logits 2.4、1.2、負 0.7 轉成 0.7428、0.2237、0.0335，總和 1.000000"><defs><marker id="arf" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="418.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Softmax：把 logits 變成加總為 1 的機率</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">pⱼ = e^zⱼ / Σ e^z_k；排序不變，總和一定是 1</text><text x="60" y="118" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">logits</text><text x="316" y="118" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">機率</text><text x="60" y="155" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">貓</text><text x="140" y="155" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2.4</text><line x1="240" y1="150" x2="296" y2="150" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="316" y="138" width="341.688" height="24" rx="4" fill="#4ecdc4" stroke="none" stroke-width="1" opacity="0.9"/><text x="667.688" y="155" font-size="12" fill="#4ecdc4" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.7428</text><text x="60" y="201" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">狗</text><text x="140" y="201" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.2</text><line x1="240" y1="196" x2="296" y2="196" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="316" y="184" width="102.902" height="24" rx="4" fill="#58a6ff" stroke="none" stroke-width="1" opacity="0.9"/><text x="428.902" y="201" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.2237</text><text x="60" y="247" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">鳥</text><text x="140" y="247" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">−0.7</text><line x1="240" y1="242" x2="296" y2="242" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="316" y="230" width="15.41" height="24" rx="4" fill="#58a6ff" stroke="none" stroke-width="1" opacity="0.9"/><text x="341.41" y="247" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.0335</text><text x="316" y="300" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.7428 + 0.2237 + 0.0335 = 1.000000</text><rect x="60" y="320" width="880" height="80" rx="12" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.4"/><text x="80" y="348" font-size="12" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">實測兩個性質：① 全部 logits 同時 +100，機率完全不變（平移不變）</text><text x="80" y="374" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">② argmax 不變（2.4 還是最大）；logits 差距 3.10，機率比 22.2 倍</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">softmax 只做兩件事：取指數、除以總和。排序不變，總和一定是 1。</figcaption>
</figure>
<!-- /CNFC-FIGURE:softmax -->

```text
p_j = e^{z_j} / Σ_k e^{z_k}
```

實測（把上一節的 `[2.4, 1.2, −0.7]` 丢進去）：

| 類別 | logit | 機率 |
|---|---|---|
| 貓 | 2.4 | **0.7428** |
| 狗 | 1.2 | 0.2237 |
| 鳥 | −0.7 | 0.0335 |
| 合計 | — | **1.000000** |

> 網路上常看到「logits `[2.4, 1.5, 1.1]` → 機率 `[0.55, 0.22, 0.15]`」這種例子：那三個數字加起來只有 **0.92**，不可能是 softmax 的輸出。要嘛換一組 logits，要嘛重算——這是很常見的抄錯。

### 5.1 三個性質（都實測過）

- **總和一定是 1**：這是除以 `Σ e^{z_k}` 的直接結果。
- **排序不變**：`e^z` 是單調函數，所以 argmax 不會變。推論時直接取 `argmax(logits)` 就好，不一定要算 softmax。
- **平移不變**：所有 logits 同時 `+100`，機率完全不變（實測完全相同）。所以「多加一個對所有類別一樣的 bias」對預測沒有任何影響——bias 有意義的前提是**每個類別各自不同**。

另外，logits 的差距會被指數放大：這個例子 `max − min = 3.10`，對應的機率比是 **22.2 倍**。

## 6. 反向傳播：兩個轉置就結束

全連接層的梯度有現成的形式（`δ = ∂L/∂z` 是上游傳回來的梯度）：

```text
∂L/∂W = δ xᵀ         形狀 (m, 1) × (1, n) = (m, n)   ← 跟 W 一樣大
∂L/∂b = δ            形狀 (m, 1)
∂L/∂x = Wᵀ δ         形狀 (n, m) × (m, 1) = (n, 1)   ← 傳回前一層
```

實測（隨機 `W`、`x`，`δ = [1, −0.5, 0.25, 0, 2]`）：用**中心差分**算出的數值梯度與 `δ xᵀ` **完全一致**（`allclose` 為 True）。這也是為什麼全連接層在框架裡幾乎不需要特別處理——它就是一次外積。

代價是：`∂L/∂W` 跟 `W` 一樣大，所以參數多的地方梯度也大。訓練時記憶體爆掉，通常不是因為特徵圖，而是因為這些大矩陣的梯度。

## 7. 在 CNN 裡的角色：加權投票

<!-- CNFC-FIGURE:vote -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" role="img" aria-label="加權投票：4 個特徵各自對 3 個類別投一票，共 12 條邊、12 個獨立權重"><defs><marker id="arf" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="438.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">把全連接層想成一場加權投票</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">12 條邊就是 12 個獨立權重；線越粗代表票越重，紅色是負票</text><rect x="60" y="110" width="120" height="52" rx="9" fill="#12181f" stroke="#4ecdc4" stroke-width="1.5"/><text x="120" y="142" font-size="12" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">x₁ = 2</text><rect x="60" y="186" width="120" height="52" rx="9" fill="#12181f" stroke="#4ecdc4" stroke-width="1.5"/><text x="120" y="218" font-size="12" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">x₂ = 1</text><rect x="60" y="262" width="120" height="52" rx="9" fill="#12181f" stroke="#4ecdc4" stroke-width="1.5"/><text x="120" y="294" font-size="12" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">x₃ = 0</text><rect x="60" y="338" width="120" height="52" rx="9" fill="#12181f" stroke="#4ecdc4" stroke-width="1.5"/><text x="120" y="370" font-size="12" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">x₄ = 3</text><rect x="760" y="150" width="150" height="56" rx="9" fill="#12181f" stroke="#4ecdc4" stroke-width="1.6"/><text x="835" y="185" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">貓</text><rect x="760" y="234" width="150" height="56" rx="9" fill="#12181f" stroke="#58a6ff" stroke-width="1.6"/><text x="835" y="269" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">狗</text><rect x="760" y="318" width="150" height="56" rx="9" fill="#12181f" stroke="#c084fc" stroke-width="1.6"/><text x="835" y="353" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">鳥</text><line x1="180" y1="136" x2="760" y2="178" stroke="#4ecdc4" stroke-width="1.6" opacity="0.55"/><line x1="180" y1="212" x2="760" y2="178" stroke="#4ecdc4" stroke-width="2.6" opacity="0.55"/><line x1="180" y1="288" x2="760" y2="178" stroke="#ff7b72" stroke-width="1.1" opacity="0.55"/><line x1="180" y1="364" x2="760" y2="178" stroke="#4ecdc4" stroke-width="3.1" opacity="0.55"/><line x1="180" y1="136" x2="760" y2="262" stroke="#4ecdc4" stroke-width="4.1" opacity="0.55"/><line x1="180" y1="212" x2="760" y2="262" stroke="#ff7b72" stroke-width="2.1" opacity="0.55"/><line x1="180" y1="288" x2="760" y2="262" stroke="#4ecdc4" stroke-width="1.6" opacity="0.55"/><line x1="180" y1="364" x2="760" y2="262" stroke="#4ecdc4" stroke-width="1.1" opacity="0.55"/><line x1="180" y1="136" x2="760" y2="346" stroke="#ff7b72" stroke-width="3.1" opacity="0.55"/><line x1="180" y1="212" x2="760" y2="346" stroke="#4ecdc4" stroke-width="3.6" opacity="0.55"/><line x1="180" y1="288" x2="760" y2="346" stroke="#4ecdc4" stroke-width="4.6" opacity="0.55"/><line x1="180" y1="364" x2="760" y2="346" stroke="#ff7b72" stroke-width="1.6" opacity="0.55"/><text x="440" y="410" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">W[j][i] 就是「第 i 個特徵對第 j 個類別的票」（粗細＝|w|，紅＝負票）</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">把全連接層想成一場加權投票：每個特徵對每個類別都有一票，票的輕重就是權重。</figcaption>
</figure>
<!-- /CNFC-FIGURE:vote -->

把 `W` 的每一列讀成「某個類別對所有特徵的評分權重」，整層就很像一場投票：

- 每個特徵 `x_i` 對每個類別 `j` 都有一票，票的輕重是 `w[j, i]`。
- 負權重就是「反對票」：這個特徵越強，該類別的分數越低。
- 總票數（加權和）再加 bias，才是最後的分數。

這也是為什麼全連接層**不保留空間結構**：投票的時候，特徵在哪個位置已經不重要了，重要的是「這個特徵有多強」。對分類來說這正好；對分割、偵測這種需要位置的任務就不行。

## 8. 與卷積層的差別

| 項目 | 卷積層 | 全連接層 |
|---|---|---|
| 連接方式 | 每個輸出只看局部窗口 | 每個輸出看全部輸入 |
| 權重共享 | 有（同一組 kernel 掃全圖） | 沒有（每個位置獨立） |
| 保留空間結構 | 有 | 展平後通常沒有 |
| 參數量 | `(k²·C_in + 1)·C_out`，與影像大小無關 | `m·n + m`，隨特徵維度爆炸 |
| 常見用途 | 提取邊緣、紋理、部件 | 整合特徵、分類／回歸 |

## 9. 現代 CNN 為什麼少用「大 FC」

那個 3136 → 128 的層就是 40 萬個參數，而它前面的卷積可能只有一兩千個。三個常見的替代方案：

| 做法 | 怎麼運作 | 省下什麼 |
|---|---|---|
| 全域平均池化（GAP） | 每個通道平均成 1 個數 → 直接接 `Dense(K)` | `3136×128` 換成 `64×K` |
| `1×1` 卷積 | 在通道維度做線性組合，保留空間維度 | 參數 `C_in×C_out`，且不破壞位置資訊 |
| Dropout | 訓練時隨機丟掉一部分輸入 | 不省參數，但抑制大 FC 的過擬合 |

## 10. 六個常見誤解

| 誤解 | 事實 |
|---|---|
| 全連接層的參數量跟 batch 有關 | 無關，只有 `m·n + m`；batch 只是同時算多筆 |
| logits 就是機率 | logits 可正可負、可大於 1；softmax 之後才是機率 |
| softmax 會改變預測類別 | 不會，它保序；`argmax(logits)` 就等於 `argmax(probs)` |
| flatten 有參數 | 沒有，它只是重排；參數全在下一個 Dense |
| 全連接層一定在最後 | 不一定，也可以夾在中間（例如 VGG 的 classifier 段）；只是現代網路傾向少用 |
| bias 一定有幫助 | 對所有類別加同一個常數不改變 softmax；bias 要「每類不同」才有意義 |

## 附錄 A 速查表

| 想問的事 | 答案 |
|---|---|
| 公式 | `z = Wx + b` |
| 參數量 | `m×n + m` |
| 輸入形狀 | `n`（flatten 後的特徵維度） |
| 輸出形狀 | `m`（類別數或下一層寬度） |
| 7×7×64 展平 | 3,136 |
| 3136 → 128 | 401,536 個參數 |
| softmax | `e^{z_j} / Σ e^{z_k}`，總和 1、保序、平移不變 |
| 梯度 | `∂L/∂W = δxᵀ`、`∂L/∂x = Wᵀδ` |
| 想省參數 | GAP 或 `1×1` 卷積取代大 FC |

## 附錄 B 常見錯誤

1. **忘記加 bias**：`Wx` 與 `Wx + b` 是兩件事。
2. **把 W 的行列搞反**：`W` 是 `m × n`（輸出 × 輸入），不是反過來。
3. **以為 flatten 會正規化**：它不縮放、不標準化，只重排。
4. **softmax 之後又取 log**：交叉熵通常直接吃 logits（`CrossEntropyLoss` 內含 softmax）。
5. **在 softmax 前後搞錯維度**：softmax 要沿「類別」維度做，不是沿 batch。
6. **用 Flatten 接大 Dense 然後說模型很小**：`3136×128` 就 40 萬個參數。

## 附錄 C 延伸閱讀與離線使用

站內：

- [CAM vs Grad-CAM：同一個熱圖，只差權重怎麼來](/cnn-cam-vs-gradcam/)——九個面向的對照與 α 的實測
- [Grad-CAM：用梯度算出模型在看哪裡](/cnn-gradcam/)——七個步驟、ReLU、選層，與 CAM 的等價條件
- [CAM：用 GAP 算出模型在看哪裡](/cnn-cam/)——GAP 之後的分類權重怎麼變成熱圖（含 Grad-CAM）
- [為什麼現代 CNN 常不用全連接層](/cnn-gap-head/)——GAP 分類頭：25,089,000 → 513,000 個參數
- [卷積層 vs 全連接層](/cnn-conv-vs-fc/)——系列總整理：參數、算力與平移特性的對照
- [圖解 CNN：從 5×5 小圖算到類別機率](/cnn-illustrated/)——softmax 的第一個版本
- [卷積層的運作細節](/cnn-conv-details/)——為什麼卷積的參數與影像大小無關
- [激活函數與池化層](/cnn-activation-pooling/)——GAP 與 Flatten 的取捨
- [CNN 學習筆記（Lesson 6）](/cnn-notes/)——LeNet-5 的 61,706 個參數怎麼分布

站外：

- [PyTorch `nn.Linear` 文件](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html)
- [Dive into Deep Learning（繁中）— softmax 迴歸](https://zh.d2l.ai/chapter_linear-networks/softmax-regression.html)

離線：本頁是**單一 HTML 檔、零外部資源**；原始 Markdown 在同一層。

## 附錄 D 一頁精華（考前 10 分鐘）

| # | 記這一條 |
|---|---|
| 1 | 全連接＝`z = Wx + b`，`W` 是 `m×n` |
| 2 | 參數 `m·n + m`；與 batch、與影像大小都無關 |
| 3 | 7×7×64 = 3,136；flatten 沒有參數 |
| 4 | 小 CNN 的參數 97.6% 在全連接層 |
| 5 | softmax：總和 1、保序、平移不變 |
| 6 | 推論可直接 `argmax(logits)` |
| 7 | `∂L/∂W = δxᵀ`、`∂L/∂x = Wᵀδ` |
| 8 | 想省參數：GAP 或 `1×1` 卷積 |

## 附錄 G 實測原始輸出

`verify_cnn_fully_connected.py` 的完整輸出（Python 3.15.1 / NumPy 2.5.4，本機執行）：

```text
------------------------------------------------------------------------
1. z = Wx + b   (4 in, 3 out)
   x: [2. 1. 0. 3.]  W.shape: (3, 4)  b: [ 0.1 -0.2  0.3]
   row-by-row dot product, before bias: [ 2.3  1.4 -1. ]
   z = Wx + b : [ 2.4  1.2 -0.7]
   step by step:
     z1 = (0.2×2 + 0.4×1 + -0.1×0 + 0.5×3) + 0.1 = 2.4000
     z2 = (0.7×2 + -0.3×1 + 0.2×0 + 0.1×3) + -0.2 = 1.2000
     z3 = (-0.5×2 + 0.6×1 + 0.8×0 + -0.2×3) + 0.3 = -0.7000
------------------------------------------------------------------------
2. what the draft's numbers would require
   draft claims z = [2.4, 1.5, 1.1]
   computed     z = [ 2.4  1.2 -0.7]
   difference   : [0.  0.3 1.8]
------------------------------------------------------------------------
3. softmax
   computed z               -> [0.7428 0.2237 0.0335]  sum = 1.000000
   draft z [2.4, 1.5, 1.1]  -> [0.5956 0.2421 0.1623]  sum = 1.000000
   draft claims [0.55, 0.22, 0.15], which sums to 0.92
------------------------------------------------------------------------
4. softmax properties
   shift all logits by +100 -> same probabilities? True
   order preserved? argmax 0 == 0
   max-minus-min of logits: 3.10 -> probability ratio 22.20
------------------------------------------------------------------------
5. parameter counts   params = m*n + m
   3136 -> 128 : 401408 weights + 128 bias = 401536
   3136 ->  10 : 31360 weights + 10 bias = 31370
    784 ->  64 : 50176 weights + 64 bias = 50240
     64 ->  10 : 640 weights + 10 bias = 650
    128 ->  10 : 1280 weights + 10 bias = 1290
   small MNIST CNN: conv total 1248, fc total 50890 -> fc is 97.6% of 52138
------------------------------------------------------------------------
6. flatten does not compute anything
   7x7x64 = 3136 values; 7*7*64 = 3136
   7x7x64 -> 3136, params 0; the same numbers, new shape
------------------------------------------------------------------------
7. backward pass of a fully connected layer
   dL/dW = delta x^T, shape (5, 4)
   dL/dx = W^T delta, shape (4,)
   finite-difference matches delta x^T: True
------------------------------------------------------------------------
8. bias shifts every logit by the same amount
   z (bias 0) : [ 2.3  1.4 -1. ]
   z (bias+1) : [3.3 2.4 0. ]
   softmax(bias 0) : [0.6928 0.2817 0.0256]
   softmax(bias+1) : [0.6928 0.2817 0.0256]
------------------------------------------------------------------------
```

---

*本頁為個人學習筆記整理；圖表為手繪內嵌 SVG，數字全部由附錄 G 的程式算出。*
