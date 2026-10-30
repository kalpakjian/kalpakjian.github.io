# CAM vs Grad-CAM：同一個熱圖，兩種權重

> 系列第九篇。前兩篇分別講了 [CAM](/cnn-cam/) 與 [Grad-CAM](/cnn-gradcam/) 的完整流程；這一篇只做一件事：<strong>把兩者並排比較</strong>。<br />結論先講：<strong>公式一樣，差別只在「那 K 個權重怎麼來」</strong>——一個是訓練好的參數，一個是推論時算的梯度。<br />所有數字都是本機用 NumPy 算的（Python 3.15.1 / NumPy 2.5.4），原始輸出在附錄 G。<br />如果你只記得一句：<strong>CAM 的權重是模型的常識，Grad-CAM 的權重是這張圖的判斷。</strong>

<!-- CNCG-FIGURE:formula -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 380" role="img" aria-label="兩個公式並排：CAM 用訓練好的權重 w 乘特徵圖，Grad-CAM 用梯度平均 alpha 乘特徵圖，兩者只差在那 K 個數字怎麼來"><defs><marker id="arcg" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="378.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個式子，只差那 K 個數字</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩者都是「加權疊加特徵圖，再 ReLU」；差別在權重怎麼來</text><rect x="30" y="96" width="450" height="210" rx="12" fill="#12181f" stroke="#4ecdc477" stroke-width="1.4" opacity="0.6"/><text x="50" y="124" font-size="13" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">原始 CAM</text><text x="50" y="156" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">L = ReLU( Σ_k  w[k, c] · A_k )</text><text x="50" y="186" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">w[k, c]：Linear(K → C) 的權重</text><text x="50" y="210" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">訓練時學好、存在模型裡</text><text x="50" y="240" font-size="11.5" fill="#ff7b72" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">前提：最後一層卷積後面接 GAP</text><text x="50" y="272" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 一次前向 + 查表就能畫</text><rect x="520" y="96" width="450" height="210" rx="12" fill="#12181f" stroke="#c084fc77" stroke-width="1.4" opacity="0.6"/><text x="540" y="124" font-size="13" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Grad-CAM</text><text x="540" y="156" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">L = ReLU( Σ_k  α[k, c] · A_k )</text><text x="540" y="186" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">α[k, c] = mean( ∂yᶜ / ∂A_k )</text><text x="540" y="210" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">推論時對這張影像算出來的</text><text x="540" y="240" font-size="11.5" fill="#4ecdc4" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">前提：只要該層能反向傳播</text><text x="540" y="272" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 每個類別多一次反向</text><path d="M 480 200 L 512 200" stroke="#8b949e" stroke-width="1.6" marker-end="url(#arcg)"/><text x="496" y="190" font-size="10" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">換</text><text x="40" y="344" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一句話：CAM 的權重是「模型的常識」，Grad-CAM 的權重是「這張圖的即時判斷」。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">同一個式子，只差在那 K 個數字是「學來的」還是「當場算的」。</figcaption>
</figure>
<!-- /CNCG-FIGURE:formula -->

## 1. 公式對照

```text
原始 CAM    L(x, y) = ReLU( Σ_k  w[k, c] · A_k(x, y) )
Grad-CAM    L(x, y) = ReLU( Σ_k  α[k, c] · A_k(x, y) )

w[k, c]  = Linear(K → C) 的權重              ← 訓練時學好，存在模型裡
α[k, c]  = (1/Z) ΣΣ ∂yᶜ / ∂A_k(i, j)         ← 推論時對這張影像算
```

兩者的「疊加 + ReLU + 上採樣」完全一樣；差異只有那個純量。

## 2. 九個面向的差異

| 面向 | 原始 CAM | Grad-CAM |
|---|---|---|
| 權重來源 | 線性分類層的訓練權重 `w[k, c]` | 梯度對空間取平均 `α[k, c]` |
| 權重隨影像變嗎 | **不變**（同一模型同一類別固定） | **通常會變**（見 §6 的但書） |
| 需要 GAP | **必須** | 不必 |
| 需要改架構 | 沒有 GAP 就要改並重訓 | 只要該層可反向 |
| 可選層 | 只能是 GAP 前那一層 | 任一卷積層 |
| 適用模型 | 「Conv → GAP → Linear」 | 幾乎任何可微 CNN |
| 成本 | 1 次前向 + 查表 | 1 次前向 + 每類別 1 次反向 |
| ReLU | 常用（論文本體沒有強制） | 必要 |
| 熱圖解析度 | 所選層的 `H × W`（通常 7×7） | 同左 |

## 3. 為什麼 CAM 一定要 GAP

```text
F_k = (1 / H·W) ΣΣ A_k(x, y)              ← GAP 的定義
yᶜ  = Σ_k w[k, c] · F_k + b_c             ← 分類層
    = (1 / H·W) ΣΣ ( Σ_k w[k, c] · A_k(x, y) ) + b_c
    = mean( CAM_c ) + b_c
```

因為 `F_k` **只對應一張** `A_k`，`w[k, c]` 才可以直接乘回 `A_k`。
換成 `Conv → Flatten → FC`，每個權重綁的是「某個像素 × 某個通道」，就拆不回一張圖了。

## 4. 為什麼 Grad-CAM 更通用

梯度問的是另一個問題：

> 「第 k 張特徵圖**在這張影像的這個位置**再強一點，類別分數會上升多少？」

它不需要知道分類器的形狀，只需要該層可微。所以：

| 架構 | CAM | Grad-CAM |
|---|---|---|
| `Conv → GAP → Linear` | 可以 | 可以 |
| `Conv → Flatten → FC` | **不行** | 可以 |
| `Conv → 1×1 conv → GAP → Linear` | **不行**（多了一層） | 可以 |
| ResNet／DenseNet（線性頭） | 要看頭 | 可以 |

## 5. 直觀例子：#37 那張特徵圖

假設最後一層有 512 張特徵圖，要解釋「狗」：

| | CAM | Grad-CAM |
|---|---|---|
| 第 37 張的權重 | `w[37, 狗] = 0.80`（固定的參數） | `α[37, 狗] = 0.90`（這張圖算出來的） |
| 換一張圖 | 還是 0.80 | 可能變 0.60 或 1.20 |
| 換一個類別 | 換另一列（`w[37, 貓]`） | 重新反傳一次 |

「固定 vs 即時」是兩者最直覺的差別。

## 6. 但「α 隨影像改變」要加條件

<!-- CNCG-FIGURE:per-image -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 430" role="img" aria-label="同一組分類權重 w，對兩張不同影像：純 GAP 加 Linear 的模型 alpha 完全不變，中間有 ReLU 時 alpha 才隨影像改變"><defs><marker id="arcg" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="428.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">α 真的「隨影像改變」嗎？實測</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一組分類權重，換一張影像，權重會變嗎？答案取決於中間有沒有非線性</text><rect x="40" y="96" width="250" height="120" rx="10" fill="#12181f" stroke="#4ecdc488" stroke-width="1.4"/><text x="56" y="120" font-size="11" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">分類層權重 w（固定）</text><text x="56" y="148" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">w[1, 狗] = 1.20</text><text x="56" y="172" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">w[2, 狗] = −0.50</text><text x="56" y="196" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">w[3, 狗] = 0.80</text><line x1="296" y1="156" x2="336" y2="156" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="340" y="96" width="210" height="120" rx="10" fill="#12181f" stroke="#58a6ff88" stroke-width="1.4"/><text x="356" y="120" font-size="11" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">影像 A</text><text x="356" y="148" font-size="10.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">α = [0.019, −0.018, 0.025]</text><text x="356" y="176" font-size="9.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">（純 GAP 時：0.075 / −0.031 / 0.05）</text><text x="356" y="200" font-size="9.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4×4 → H·W = 16</text><rect x="340" y="232" width="210" height="120" rx="10" fill="#12181f" stroke="#c084fc88" stroke-width="1.4"/><text x="356" y="256" font-size="11" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">影像 B</text><text x="356" y="284" font-size="10.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">α = [0.038, −0.014, 0.031]</text><text x="356" y="312" font-size="9.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">（純 GAP 時：同一組數字）</text><text x="356" y="336" font-size="9.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">α 只在這裡不同</text><rect x="580" y="96" width="390" height="256" rx="12" fill="#12181f" stroke="#e0a45877" stroke-width="1.4"/><text x="600" y="122" font-size="12" fill="#e0a458" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩種情況要分清楚</text><text x="600" y="152" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">① 純 GAP + Linear（沒有中間層）</text><text x="616" y="176" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">α = w / (H·W) → 每張圖都一樣</text><text x="616" y="198" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">這時 Grad-CAM 就等於 CAM</text><text x="600" y="232" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">② 中間有 ReLU（真實網路）</text><text x="616" y="256" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">∂y/∂A = w/(H·W) · 1[A &gt; 0]</text><text x="616" y="278" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">正值比例隨影像變 → α 也變</text><text x="616" y="300" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">影像 A 的正值比例 0.25 / 0.56 / 0.50</text><text x="616" y="320" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">影像 B 的正值比例 0.50 / 0.44 / 0.62</text><text x="40" y="400" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">所以「Grad-CAM 的權重隨影像改變」這句話要加條件：在 CAM 適用的那種純線性末端上，它其實不變。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">實測：純 GAP + Linear 時 α 與影像無關（等於 w/(H·W)）；加了 ReLU 之後 α 才隨影像變。</figcaption>
</figure>
<!-- /CNCG-FIGURE:per-image -->

這件事值得實測，因為它有一個很容易被講錯的邊界：**在 CAM 適用的那種末端（純 GAP + Linear）上，α 其實也不隨影像改變**。

```text
∂yᶜ / ∂A_k(i, j) = w[k, c] / (H·W)          （對位置是常數）
α[k, c]          = w[k, c] / (H·W)           ← 跟影像是哪張無關
```

實測（3 個通道、4×4、兩張不同影像）：兩張圖的 `α(dog)` 都是 `[0.075, −0.0312, 0.05]`。
在這種網路上，Grad-CAM 與 CAM 是同一張圖（差一個 `1/(H·W)` 的尺度）。

**一旦中間有非線性**（真實網路幾乎都有），等式就破：

```text
∂yᶜ / ∂A_k(i, j) = w[k, c] / (H·W) · 1[ A_k(i, j) > 0 ]
α[k, c]          = w[k, c] / (H·W) · （該通道的正值比例）
```

正值比例隨影像變，`α` 就變。實測：

| 影像 | 各通道正值比例 | `α(dog)` |
|---|---|---|
| A | 0.25 / 0.56 / 0.50 | `[0.0188, −0.0176, 0.0250]` |
| B | 0.50 / 0.44 / 0.62 | `[0.0375, −0.0137, 0.0312]` |

所以精確的說法是：**Grad-CAM 的權重是「對這張圖算的」，只有在網路真的把它變成影像相關的函數時，數值才會隨影像變。** 這也是為什麼 Grad-CAM 在真實模型上比 CAM 更「影像特定」——但它不是魔法，不是因為叫 Grad 就一定比較聰明。

## 7. 各自的限制

<!-- CNCG-FIGURE:cost -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 450" role="img" aria-label="成本與能力對照：CAM 一次前向就能算、但需要 GAP 架構；Grad-CAM 每個類別要一次反向，幾乎任何 CNN 都能用"><defs><marker id="arcg" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="448.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">能力與成本：換到什麼</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一張熱圖，CAM 便宜但挑架構；Grad-CAM 通用但要多做反向</text><text x="60" y="108" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">架構</text><text x="520" y="108" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">CAM</text><text x="700" y="108" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Grad-CAM</text><text x="60" y="140" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Conv → GAP → Linear</text><text x="520" y="140" font-size="11.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">可以</text><text x="700" y="140" font-size="11.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">可以</text><text x="60" y="182" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Conv → Flatten → FC</text><text x="520" y="182" font-size="11.5" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不行</text><text x="700" y="182" font-size="11.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">可以</text><text x="60" y="224" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Conv → 1×1 conv → GAP → Linear</text><text x="520" y="224" font-size="11.5" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不行</text><text x="700" y="224" font-size="11.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">可以</text><text x="60" y="266" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ResNet / DenseNet（線性頭）</text><text x="520" y="266" font-size="11.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">要看頭</text><text x="700" y="266" font-size="11.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">可以</text><rect x="40" y="320" width="920" height="84" rx="12" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.4"/><text x="60" y="348" font-size="12" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">成本：CAM = 1 次前向 + 查表；Grad-CAM = 1 次前向 + 每個類別 1 次反向。</text><text x="60" y="374" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1000 類全部畫一輪 = 1,000 次反向，所以實務上只挑 1–3 個類別看。</text><text x="40" y="420" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">這也是 Grad-CAM 常被拿來做除錯而不是即時監控的原因。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">能力換成本：Grad-CAM 通用，但每解釋一個類別就要一次反向傳播。</figcaption>
</figure>
<!-- /CNCG-FIGURE:cost -->

| 方法 | 限制 |
|---|---|
| 原始 CAM | 必須有 GAP；只能解釋特定架構；沒有 GAP 就得改架構重訓 |
| Grad-CAM | 解析度受限於所選層（7×7／14×14）；每個通道只有一個全域權重；對梯度飽和與雜訊敏感；每類別一次反向 |

後續的改良大致沿著這三個弱點：

| 變體 | 改什麼 |
|---|---|
| Grad-CAM++ | 用梯度的二階資訊做像素級加權，多物件與定位更穩 |
| XGrad-CAM | 把權重換成「梯度 × 激活」的正規化版本，對飽和較不敏感 |
| Score-CAM | 完全不用梯度，改用遮罩後的分数變化（更慢但更穩） |
| HiResCAM | 用元素級梯度，避免多個位置共用同一個權重 |

成本上還有一個實務數字：**1,000 類全部畫一輪就是 1,000 次反向傳播**，所以日常只挑 1–3 個類別看。

## 8. 六個常見誤解

| 誤解 | 事實 |
|---|---|
| Grad-CAM 比較準，所以熱图比較可信 | 兩者都只說「哪裡」，不證明「看對」 |
| α 一定隨影像改變 | 純 GAP + Linear 時 α = w/(H·W)，與影像無關（§6） |
| CAM 一定比 Grad-CAM 差 | 在它適用的架構上兩者等價；CAM 還更便宜 |
| Grad-CAM 不需要 GAP，所以也不需要分類頭 | 還是需要一個可微的分類頭算 `yᶜ` |
| 熱圖解析度越高越好 | 越高的層語意越淺；要看任務挑層 |
| 兩個方法可以互換使用 | 架構不合時 CAM 根本算不出來，不是「效果差一點」 |

## 附錄 A 速查表

| 想問的事 | 答案 |
|---|---|
| 兩者的共同點 | 都是 `ReLU(Σ 權重 × 特徵圖)` |
| CAM 的權重 | 線性分類層的 `w[k, c]`（訓練參數） |
| Grad-CAM 的權重 | `α[k, c] = mean(∂yᶜ/∂A_k)` |
| CAM 的硬性要求 | 末端必須是 GAP + Linear |
| Grad-CAM 的要求 | 該層可反向傳播 |
| 純 GAP + Linear 時 | `α = w/(H·W)`，兩者等價 |
| 有非線性時 | `α = w/(H·W) × 正值比例` → 隨影像變 |
| 成本 | CAM：1 前向；Grad-CAM：1 前向 + 每類 1 反向 |
| 熱圖解析度 | 所選層的 `H × W`（通常 7×7） |
| 兩者都不能做的 | 證明模型「看對」 |

## 附錄 B 常見錯誤

1. **把 `α` 當成「這張圖的權重」卻在純線性網路上驗證**：那裡 `α` 是常數。
2. **在 CAM 的架構上硬比較兩種方法**：會得到幾乎一樣的圖（本來就等價）。
3. **對 softmax 機率取梯度**：飽和後梯度太小，熱圖會糊掉。
4. **忘記 ReLU**：負值把色階吃掉。
5. **拿不同層的熱圖互相比**：解析度與語意都不同，不是同一把尺。
6. **只用準確率驗證解釋**：熱圖要配遮擋測試、換背景測試才有意義。

## 附錄 C 延伸閱讀與離線使用

站內：

- [CAM：用 GAP 算出模型在看哪裡](/cnn-cam/)——CAM 的推導與 2×2 手算
- [Grad-CAM：用梯度算出模型在看哪裡](/cnn-gradcam/)——七個步驟、ReLU、選層
- [GAP 是什麼？](/cnn-gap-head/)——GAP 與分類頭
- [卷積層 vs 全連接層](/cnn-conv-vs-fc/)——為什麼大 FC 讓權重對不回特徵圖
- [圖解 CNN](/cnn-illustrated/)——整體資料流

站外：

- [Grad-CAM 原論文](https://arxiv.org/abs/1610.02391)
- [Learning Deep Features for Discriminative Localization（CAM）](https://arxiv.org/abs/1512.04150)

離線：本頁是**單一 HTML 檔、零外部資源**；原始 Markdown 在同一層。

## 附錄 D 一頁精華（考前 10 分鐘）

| # | 記這一條 |
|---|---|
| 1 | 公式一樣，只差在 `w`（學來的）與 `α`（算出來的） |
| 2 | CAM 必須有 GAP，因為 `F_k` 只對應一張 `A_k` |
| 3 | Grad-CAM 只要能反向；架構不用改 |
| 4 | 純 GAP + Linear：`α = w/(H·W)` → 兩者等價、也與影像無關 |
| 5 | 有非線性：`α = w/(H·W) × 正值比例` → 隨影像變 |
| 6 | 成本：CAM 1 前向；Grad-CAM 1 前向 + 每類 1 反向 |
| 7 | 解析度都受限於所選層（7×7／14×14） |
| 8 | 兩者都只說「哪裡」，不證明「看對」 |

## 附錄 G 實測原始輸出

`verify_cnn_cam_vs_gradcam.py` 的完整輸出（Python 3.15.1 / NumPy 2.5.4，本機執行）：

```text
------------------------------------------------------------------------
1. same formula, different weight
   CAM      : L = ReLU( sum_k w[k,c]  * A_k )     w  = trained weights
   Grad-CAM : L = ReLU( sum_k a[k,c]  * A_k )     a  = mean of gradients
   the only difference is how the K numbers are obtained
------------------------------------------------------------------------
2. a pure GAP+Linear model: alpha does NOT depend on the image
   classifier weights w (fixed, learned once):
     dog : [ 1.2 -0.5  0.8]    cat : [-0.7  0.9  0.3]
   d y_c / d A_k(i,j) = w[k,c] / (H*W) for every cell
     alpha(dog) = [ 0.075  -0.0312  0.05  ]   <- same for image A and image B
   image A is different from image B: True
   but alpha is identical for both (pure GAP+Linear).
------------------------------------------------------------------------
3. put a ReLU before the GAP -> alpha becomes image-specific
   d y_c / d A_k(i,j) = w[k,c]/(H*W) * 1[A_k(i,j) > 0]
   image A: positive share per channel [0.25 0.56 0.5 ] -> alpha(dog) [ 0.0188 -0.0176  0.025 ]
   image B: positive share per channel [0.5  0.44 0.62] -> alpha(dog) [ 0.0375 -0.0137  0.0312]
   w/(H*W) claimed by the pure model: [ 0.075  -0.0312  0.05  ]
------------------------------------------------------------------------
4. the #37 example from the page
   feature map #37 of a 512-channel layer
   CAM      : w[37, dog] = 0.80  (a stored parameter, same for every image)
   Grad-CAM : alpha[37, dog] = 0.90 on this image, 0.60 on another, 1.20 on a third
------------------------------------------------------------------------
5. what each method can explain (architecture checklist)
   architecture                           CAM                    Grad-CAM
   Conv -> GAP -> Linear                  yes                    yes
   Conv -> Flatten -> FC                  no                     yes
   Conv -> 1x1 conv -> GAP -> Linear      no                     yes
   ResNet / DenseNet with a linear head   partly (needs the GAP head) yes
------------------------------------------------------------------------
6. cost per explanation
   CAM      : 1 forward, then a matrix lookup      (no backward pass)
   Grad-CAM : 1 forward + 1 backward per class
   Grad-CAM over    1 classes:    1 backward passes
   Grad-CAM over 1000 classes: 1000 backward passes
------------------------------------------------------------------------
```

---

*本頁為個人學習筆記整理；圖表為手繪內嵌 SVG，數字全部由附錄 G 的程式算出。*
