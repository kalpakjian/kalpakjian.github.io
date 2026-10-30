# Grad-CAM：用梯度算出模型在看哪裡

> 系列第八篇。上一篇（[CAM](/cnn-cam/)）講 GAP 讓「分類權重」可以乘回特徵圖；但那個方法要求末端是 GAP + Linear。<br /><strong>Grad-CAM 把權重換成「梯度」</strong>，於是幾乎任何 CNN 都能算——不必改架構、不必重訓。<br />這篇把七個步驟、手算例子、ReLU 的作用、選層與上採樣都算一次。<br />所有數字都是本機用 NumPy 算的（Python 3.15.1 / NumPy 2.5.4），原始輸出在附錄 G。

<!-- CNGC-FIGURE:flow -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 380" role="img" aria-label="Grad-CAM 的七個步驟：前向取得特徵圖、選類別、反向求梯度、對梯度取平均得到 alpha、加權疊加、ReLU、上採樣疊圖"><defs><marker id="argc" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="378.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Grad-CAM 的七個步驟</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">前六步都在特徵圖上算；只有最後一步是為了畫出來</text><rect x="36" y="116" width="120" height="92" rx="9" fill="#12181f" stroke="#4ecdc488" stroke-width="1.4"/><text x="50" y="142" font-size="11.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.</text><text x="70" y="142" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">前向</text><text x="96" y="176" font-size="9.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">A¹…Aᴷ</text><line x1="158" y1="162" x2="169" y2="162" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="172" y="116" width="120" height="92" rx="9" fill="#12181f" stroke="#4ecdc488" stroke-width="1.4"/><text x="186" y="142" font-size="11.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2.</text><text x="206" y="142" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">選類別</text><text x="232" y="176" font-size="9.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">yᶜ</text><line x1="294" y1="162" x2="305" y2="162" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="308" y="116" width="120" height="92" rx="9" fill="#12181f" stroke="#58a6ff88" stroke-width="1.4"/><text x="322" y="142" font-size="11.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3.</text><text x="342" y="142" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">反向</text><text x="368" y="176" font-size="9.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">∂yᶜ/∂Aᵏ</text><line x1="430" y1="162" x2="441" y2="162" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="444" y="116" width="120" height="92" rx="9" fill="#12181f" stroke="#e0a45888" stroke-width="1.4"/><text x="458" y="142" font-size="11.5" fill="#e0a458" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4.</text><text x="478" y="142" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">梯度平均</text><text x="504" y="176" font-size="9.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">αᵏᶜ</text><line x1="566" y1="162" x2="577" y2="162" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="580" y="116" width="120" height="92" rx="9" fill="#12181f" stroke="#e0a45888" stroke-width="1.4"/><text x="594" y="142" font-size="11.5" fill="#e0a458" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5.</text><text x="614" y="142" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">加權疊加</text><text x="640" y="176" font-size="9.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Lᶜ</text><line x1="702" y1="162" x2="713" y2="162" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="716" y="116" width="120" height="92" rx="9" fill="#12181f" stroke="#c084fc88" stroke-width="1.4"/><text x="730" y="142" font-size="11.5" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6.</text><text x="750" y="142" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ReLU</text><text x="776" y="176" font-size="9.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只留正</text><line x1="838" y1="162" x2="849" y2="162" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><rect x="852" y="116" width="120" height="92" rx="9" fill="#12181f" stroke="#ff7b7288" stroke-width="1.4"/><text x="866" y="142" font-size="11.5" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7.</text><text x="886" y="142" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">上採樣</text><text x="912" y="176" font-size="9.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">224×224</text><rect x="36" y="232" width="928" height="96" rx="12" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.4"/><text x="56" y="260" font-size="12" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">公式：α[k, c] = (1/Z) ΣΣ ∂yᶜ/∂Aᵏ(i, j)　　Lᶜ = ReLU( Σ_k α[k, c] · Aᵏ )</text><text x="56" y="288" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Z = H×W；ReLU 之後只留下「支持這個類別」的區域。</text><text x="56" y="312" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">跟 CAM 的差別只有權重來源：一個拿線性層的 w，一個拿梯度的平均。</text><text x="40" y="356" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">成本：多一次反向傳播；好處：不必改架構、不必重訓。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">七個步驟裡，只有「反向傳播」這一步比 CAM 多了成本；換來的是不必改架構。</figcaption>
</figure>
<!-- /CNGC-FIGURE:flow -->

## 1. 一句話

```text
α[k, c] = (1/Z) ΣΣ ∂yᶜ / ∂Aᵏ(i, j)          Z = H × W
Lᶜ      = ReLU( Σ_k α[k, c] · Aᵏ )           熱圖，再上採樣回原圖
```

和 CAM 只差一行：**權重不是讀線性層，而是把梯度平均起來**。

## 2. 為什麼用梯度，而不是權重

| | CAM | Grad-CAM |
|---|---|---|
| 權重 `α` 從哪來 | `Linear(K → C)` 的 `w[k, c]` | 梯度對空間取平均 |
| 對架構的要求 | 末端必須是 GAP + Linear | 只要「能對該層做前向與反向」 |
| 既有模型 | 通常要改架構、重訓 | 直接可用 |
| 額外成本 | 一次前向 | 前向 + 一次反向 |

梯度問的問題不一樣：**「這個位置的激活再多一點，該類別分數會上升多少？」**
所以它不需要知道分類器長什麼樣子——這是它通用的原因。

## 3. 七個步驟

1. **前向傳播**，把目標層的特徵圖 `A¹ … Aᴷ` 留下來（`K × H × W`）。
2. **選類別** `c`，取它的 logit `yᶜ`。
3. **反向傳播**，算 `∂yᶜ/∂Aᵏ`——每個通道一張 `H × W` 的梯度圖。
4. **對梯度做 GAP**：`α[k, c] = mean(∂yᶜ/∂Aᵏ)`，得到 `K` 個權重。
5. **加權疊加**：`Lᶜ = Σ_k α[k, c] · Aᵏ`。
6. **ReLU**：`Lᶜ = max(Lᶜ, 0)`，只留支持該類別的區域。
7. **上採樣**回原圖尺寸，正規化 + colormap，半透明疊上去。

### 3.1 為什麼用 logit，不用 softmax 機率

softmax 是單調但**飽和**的：機率接近 1 或 0 時梯度會變得非常小（`p(1−p)`），反向傳播容易變成一片零。用 softmax 前的 logit 就沒有這個問題。真的要對「機率」求導也可以，但要多做一次鏈式法則，實務上少見。

## 4. 手算一次

<!-- CNGC-FIGURE:math -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 380" role="img" aria-label="Grad-CAM 手算：梯度圖平均得到 alpha 0.25、0.1、負 0.2，加權疊加得 2.6、負 0.3、2.1、0.2，ReLU 後只剩三格"><defs><marker id="argc" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="378.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">手算一次：梯度圖 → 權重 → 加權疊加</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">三張 2×2 特徵圖、三張梯度圖；α 是梯度圖的平均</text><text x="50" y="108" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">∂y/∂A1</text><rect x="50" y="118" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="72.0" y="143.6" font-size="10" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.2</text><rect x="94" y="118" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="116.0" y="143.6" font-size="10" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.4</text><rect x="50" y="162" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="72.0" y="187.6" font-size="10" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.1</text><rect x="94" y="162" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="116.0" y="187.6" font-size="10" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.3</text><text x="94" y="220" font-size="11.5" fill="#4ecdc4" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">α₁ = 0.25</text><text x="200" y="108" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">∂y/∂A2</text><rect x="200" y="118" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="222.0" y="143.6" font-size="10" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.1</text><rect x="244" y="118" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="266.0" y="143.6" font-size="10" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.1</text><rect x="200" y="162" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="222.0" y="187.6" font-size="10" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.1</text><rect x="244" y="162" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="266.0" y="187.6" font-size="10" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.1</text><text x="244" y="220" font-size="11.5" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">α₂ = 0.10</text><text x="350" y="108" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">∂y/∂A3</text><rect x="350" y="118" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="372.0" y="143.6" font-size="10" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-0.2</text><rect x="394" y="118" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="416.0" y="143.6" font-size="10" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-0.2</text><rect x="350" y="162" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="372.0" y="187.6" font-size="10" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-0.2</text><rect x="394" y="162" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="416.0" y="187.6" font-size="10" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-0.2</text><text x="394" y="220" font-size="11.5" fill="#c084fc" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">α₃ = −0.20</text><text x="500" y="108" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">L = Σ α · A</text><rect x="500" y="118" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="522.0" y="143.42" font-size="9.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2.6</text><rect x="544" y="118" width="44" height="44" rx="4" fill="#e0a45826" stroke="#e0a458" stroke-width="1.6"/><text x="566.0" y="143.42" font-size="9.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-0.3</text><rect x="500" y="162" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="522.0" y="187.42" font-size="9.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2.1</text><rect x="544" y="162" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="566.0" y="187.42" font-size="9.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.2</text><text x="544" y="220" font-size="10.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">加權疊加</text><line x1="556" y1="140" x2="596" y2="140" stroke="#8b949e" stroke-width="1.5" marker-end="url(#ar)"/><text x="700" y="108" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ReLU(L)</text><rect x="660" y="118" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="682.0" y="143.42" font-size="9.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2.6</text><rect x="704" y="118" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="726.0" y="143.42" font-size="9.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.0</text><rect x="660" y="162" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="682.0" y="187.42" font-size="9.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2.1</text><rect x="704" y="162" width="44" height="44" rx="4" fill="#12181f" stroke="#30363d" stroke-width="0.9" opacity="0.85"/><text x="726.0" y="187.42" font-size="9.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.2</text><text x="704" y="220" font-size="10.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">負值清掉</text><rect x="50" y="252" width="900" height="104" rx="12" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.4"/><text x="70" y="280" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">① α₁ = (0.2 + 0.4 + 0.1 + 0.3) / 4 = 0.25　② L(0,0) = 0.25×10 + 0.1×1 − 0.2×0 = 2.6</text><text x="70" y="306" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">③ L(0,1) = 0.25×0 + 0.1×1 − 0.2×2 = −0.3 → ReLU 後變 0（4 格去掉 1 格）</text><text x="70" y="334" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一組特徵圖改用 CAM 的權重 0.8 / 0.1 / −0.2，熱圖會是 8.1 / −0.3 / 6.5 / 1.3——兩張圖不一樣。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">梯度的平均是權重、梯度本身不是：同一組特徵圖，CAM 用 0.8、Grad-CAM 用 0.25，熱圖就不一樣。</figcaption>
</figure>
<!-- /CNGC-FIGURE:math -->

三張 2×2 特徵圖（沿用上一篇的例子），以及「狗」類別對它們的梯度：

```text
∂y/∂A¹ = [[0.2, 0.4], [0.1, 0.3]]   →  α₁ = (0.2+0.4+0.1+0.3)/4 = 0.25
∂y/∂A² = [[0.1, 0.1], [0.1, 0.1]]   →  α₂ = 0.10
∂y/∂A³ = [[−0.2, −0.2], [−0.2, −0.2]] → α₃ = −0.20
```

加權疊加：

```text
L = 0.25·A¹ + 0.10·A² − 0.20·A³
  = [[2.6, −0.3],
     [2.1,  0.2]]
```

驗算兩格：

```text
(0,0) = 0.25×10 + 0.1×1 − 0.2×0 = 2.6
(0,1) = 0.25×0  + 0.1×1 − 0.2×2 = −0.3
```

ReLU 之後 `[[2.6, 0], [2.1, 0.2]]`——4 格去掉 1 格。

> 同一組特徵圖，若改用 CAM 的權重（0.8 / 0.1 / −0.2），熱圖會是 `[[8.1, −0.3], [6.5, 1.3]]`。
> 兩張圖**不一樣**：`α` 是梯度的平均，`w` 是分類器的係數，只有在「純 GAP + Linear」時兩者才成比例（見 §9）。

## 5. ReLU 為什麼不能省

`L` 可以是負的：那代表「這個位置越強，反而越**不利**於該類別」。熱圖要回答的是「哪裡支持它」，所以：

- 不加 ReLU：色階被負值拉開，真正的證據區域看起來不亮。
- 加 ReLU：只保留正向貢獻，負值一律 0。

實測這個小例子：4 格裡有 1 格是負的（−0.3），ReLU 後被清掉。

## 6. 選哪一層

<!-- CNGC-FIGURE:layer -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" role="img" aria-label="選哪一層做 Grad-CAM：早期 56×56 解析度高但語意淺、中期 28×28、最後 7×7 語意強但要放大 32 倍"><defs><marker id="argc" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="358.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">要拿哪一層做 Grad-CAM？</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個模型、同一張影像，換一層就是另一張熱圖</text><rect x="60" y="100" width="250" height="200" rx="10" fill="#12181f" stroke="#4ecdc488" stroke-width="1.4" opacity="0.6"/><text x="76" y="126" font-size="12" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">早期 conv</text><text x="76" y="148" font-size="11" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">56×56×64</text><rect x="76" y="162" width="96.0" height="96.0" rx="2" fill="#4ecdc414" stroke="#4ecdc4" stroke-width="1.2"/><line x1="82.0" y1="162" x2="82.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="168.0" x2="172.0" y2="168.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="88.0" y1="162" x2="88.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="174.0" x2="172.0" y2="174.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="94.0" y1="162" x2="94.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="180.0" x2="172.0" y2="180.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="100.0" y1="162" x2="100.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="186.0" x2="172.0" y2="186.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="106.0" y1="162" x2="106.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="192.0" x2="172.0" y2="192.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="112.0" y1="162" x2="112.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="198.0" x2="172.0" y2="198.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="118.0" y1="162" x2="118.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="204.0" x2="172.0" y2="204.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="124.0" y1="162" x2="124.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="210.0" x2="172.0" y2="210.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="130.0" y1="162" x2="130.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="216.0" x2="172.0" y2="216.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="136.0" y1="162" x2="136.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="222.0" x2="172.0" y2="222.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="142.0" y1="162" x2="142.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="228.0" x2="172.0" y2="228.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="148.0" y1="162" x2="148.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="234.0" x2="172.0" y2="234.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="154.0" y1="162" x2="154.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="240.0" x2="172.0" y2="240.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="160.0" y1="162" x2="160.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="246.0" x2="172.0" y2="246.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="166.0" y1="162" x2="166.0" y2="258.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><line x1="76" y1="252.0" x2="172.0" y2="252.0" stroke="#4ecdc4" stroke-width="0.6" opacity="0.5"/><text x="188" y="214" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">熱圖</text><text x="188" y="236" font-size="10.5" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">上採樣 ×4</text><text x="76" y="286" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">細節清楚，看到的是邊緣、紋理</text><rect x="360" y="100" width="250" height="200" rx="10" fill="#12181f" stroke="#58a6ff88" stroke-width="1.4" opacity="0.6"/><text x="376" y="126" font-size="12" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">中期 conv</text><text x="376" y="148" font-size="11" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">28×28×128</text><rect x="376" y="162" width="96.0" height="96.0" rx="2" fill="#58a6ff14" stroke="#58a6ff" stroke-width="1.2"/><line x1="385.6" y1="162" x2="385.6" y2="258.0" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="376" y1="171.6" x2="472.0" y2="171.6" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="395.2" y1="162" x2="395.2" y2="258.0" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="376" y1="181.2" x2="472.0" y2="181.2" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="404.8" y1="162" x2="404.8" y2="258.0" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="376" y1="190.8" x2="472.0" y2="190.8" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="414.4" y1="162" x2="414.4" y2="258.0" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="376" y1="200.4" x2="472.0" y2="200.4" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="424.0" y1="162" x2="424.0" y2="258.0" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="376" y1="210.0" x2="472.0" y2="210.0" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="433.6" y1="162" x2="433.6" y2="258.0" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="376" y1="219.6" x2="472.0" y2="219.6" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="443.2" y1="162" x2="443.2" y2="258.0" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="376" y1="229.2" x2="472.0" y2="229.2" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="452.8" y1="162" x2="452.8" y2="258.0" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="376" y1="238.8" x2="472.0" y2="238.8" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="462.4" y1="162" x2="462.4" y2="258.0" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><line x1="376" y1="248.4" x2="472.0" y2="248.4" stroke="#58a6ff" stroke-width="0.6" opacity="0.5"/><text x="488" y="214" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">熱圖</text><text x="488" y="236" font-size="10.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">上採樣 ×8</text><text x="376" y="286" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">折衷：部件層級</text><rect x="660" y="100" width="250" height="200" rx="10" fill="#12181f" stroke="#ff7b7288" stroke-width="1.4" opacity="0.6"/><text x="676" y="126" font-size="12" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">最後 conv</text><text x="676" y="148" font-size="11" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7×7×512</text><rect x="676" y="162" width="96.0" height="96.0" rx="2" fill="#ff7b7214" stroke="#ff7b72" stroke-width="1.2"/><line x1="689.7142857142857" y1="162" x2="689.7142857142857" y2="258.0" stroke="#ff7b72" stroke-width="0.6" opacity="0.5"/><line x1="676" y1="175.71428571428572" x2="772.0" y2="175.71428571428572" stroke="#ff7b72" stroke-width="0.6" opacity="0.5"/><line x1="703.4285714285714" y1="162" x2="703.4285714285714" y2="258.0" stroke="#ff7b72" stroke-width="0.6" opacity="0.5"/><line x1="676" y1="189.42857142857142" x2="772.0" y2="189.42857142857142" stroke="#ff7b72" stroke-width="0.6" opacity="0.5"/><line x1="717.1428571428571" y1="162" x2="717.1428571428571" y2="258.0" stroke="#ff7b72" stroke-width="0.6" opacity="0.5"/><line x1="676" y1="203.14285714285714" x2="772.0" y2="203.14285714285714" stroke="#ff7b72" stroke-width="0.6" opacity="0.5"/><line x1="730.8571428571429" y1="162" x2="730.8571428571429" y2="258.0" stroke="#ff7b72" stroke-width="0.6" opacity="0.5"/><line x1="676" y1="216.85714285714286" x2="772.0" y2="216.85714285714286" stroke="#ff7b72" stroke-width="0.6" opacity="0.5"/><line x1="744.5714285714286" y1="162" x2="744.5714285714286" y2="258.0" stroke="#ff7b72" stroke-width="0.6" opacity="0.5"/><line x1="676" y1="230.57142857142856" x2="772.0" y2="230.57142857142856" stroke="#ff7b72" stroke-width="0.6" opacity="0.5"/><line x1="758.2857142857143" y1="162" x2="758.2857142857143" y2="258.0" stroke="#ff7b72" stroke-width="0.6" opacity="0.5"/><line x1="676" y1="244.28571428571428" x2="772.0" y2="244.28571428571428" stroke="#ff7b72" stroke-width="0.6" opacity="0.5"/><text x="788" y="214" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">熱圖</text><text x="788" y="236" font-size="10.5" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">上採樣 ×32</text><text x="676" y="286" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">語意最強，但只有 49 格</text><text x="40" y="332" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">論文預設用最後一層卷積：仍保留空間資訊，又已經是高階語意；要更細的位置時往前一兩層（解析度換語意）。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">越後面語意越強、解析度越低；論文預設用最後一層，需要細節時才往前一層。</figcaption>
</figure>
<!-- /CNGC-FIGURE:layer -->

| 層 | 特徵圖 | 熱圖解析度 | 上採樣倍率 | 適合 |
|---|---|---|---|---|
| 早期 conv | 56×56×64 | 56×56 | ×4 | 想看細一點的位置（邊緣、紋理） |
| 中期 conv | 28×28×128 | 28×28 | ×8 | 折衷：部件層級 |
| 最後 conv | 7×7×512 | 7×7 | ×32 | 語意最強（論文預設） |

解析度與語意是反比的：越後面越「懂」，但格子越少。論文預設用最後一層卷積，因為它同時具備「還是空間排列」與「已是高階語意」兩個條件。

## 7. 上採樣與視覺化

```text
7×7（49 個值）→ 雙線性插值 → 224×224（50,176 像素）→ min-max 正規化 → colormap → 疊圖
```

三件事要提醒：

- **放大不會產生資訊**：49 個值放大到 5 萬個像素，只是插值。
- **正規化要用 min-max**：熱圖的絕對數值沒有意義（跟 logit 同量級），可視化時只看相對大小。
- **colormap 只是著色**：JET／viridis 不影響數值，但 JET 的「紅＝高」比較符合直覺（論文用 JET）。

## 8. 與 CAM 的差別（一張表）

| 項目 | CAM | Grad-CAM |
|---|---|---|
| 權重 | `w[k, c]`（GAP 後線性層） | `α[k, c]`（梯度平均） |
| 需要 GAP | 必須 | 不必 |
| 需要改架構／重訓 | 常需要 | 不需要 |
| ReLU | 通常不需要 | 必要 |
| 適用範圍 | 受限於末端結構 | 分類、VQA、captioning…幾乎都行 |
| 成本 | 一次前向 | 前向 + 一次反向 |

## 9. 一個可以驗證的關係

**純 GAP + Linear 的網路**（中間沒有其他層）：

```text
∂yᶜ/∂Aᵏ(i, j) = w[k, c] / (H·W)     （對位置是常數）
α[k, c]        = w[k, c] / (H·W)
Grad-CAM       = ReLU( CAMᶜ / (H·W) )
```

實測（K=5、7×7、C=3）：`Grad-CAM` 與 `ReLU(CAM/(H·W))` 的最大差 **8.89e-18**。所以在這種架構上，兩張圖其實是同一張——差的只是一個常數與 ReLU。

**一旦中間插了東西，等式就破**。實測在 GAP 前加一個 ReLU：

```text
α = mean(∂y/∂A) = [0.0645, −0.0137, 0.0125]
w / (H·W)       = [0.0938, −0.0438, 0.0250]      ← 不一樣了
```

（用中心差分驗證過解析梯度，最大差 4.38e-11。）差別來自 ReLU 把負的激活遮掉了：`∂y/∂A = w/(H·W) · 1[A > 0]`。這正是 Grad-CAM 存在的理由——**它不假設分類器具體長什麼樣子**。

## 10. 熱圖怎麼讀：它說「哪裡」，不說「為什麼」

<!-- CNGC-FIGURE:shortcut -->
<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 430" role="img" aria-label="熱圖只說模型看哪裡：兩張圖都可能答對，但一張看狗、一張看背景草地，後者代表模型學到捷徑"><defs><marker id="argc" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#8b949e"/></marker></defs><rect x="0.75" y="0.75" width="998.5" height="428.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">熱圖漂亮，不代表模型學對了</text><text x="40" y="72" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一題「黃金獵犬」，兩種模型都能答對，但看的東西不一樣</text><rect x="60" y="96" width="400" height="230" rx="12" fill="#12181f" stroke="#4ecdc488" stroke-width="1.4" opacity="0.6"/><text x="76" y="122" font-size="12" fill="#4ecdc4" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">模型 A：看狗</text><rect x="222" y="242" width="34" height="34" rx="3" fill="#4ecdc444" stroke="#4ecdc4" stroke-width="1.2"/><rect x="256" y="276" width="34" height="34" rx="3" fill="#4ecdc444" stroke="#4ecdc4" stroke-width="1.2"/><rect x="290" y="242" width="34" height="34" rx="3" fill="#4ecdc444" stroke="#4ecdc4" stroke-width="1.2"/><rect x="256" y="310" width="34" height="34" rx="3" fill="#4ecdc444" stroke="#4ecdc4" stroke-width="1.2"/><rect x="120" y="140" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="154" y="140" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="188" y="140" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="222" y="140" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="256" y="140" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="290" y="140" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="120" y="174" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="154" y="174" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="188" y="174" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="222" y="174" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="256" y="174" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="290" y="174" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="120" y="208" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="154" y="208" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="188" y="208" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="222" y="208" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="256" y="208" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="290" y="208" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="120" y="242" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="154" y="242" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="188" y="242" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="222" y="242" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="256" y="242" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="290" y="242" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="120" y="276" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="154" y="276" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="188" y="276" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="222" y="276" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="256" y="276" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="290" y="276" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="120" y="310" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="154" y="310" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="188" y="310" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="222" y="310" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="256" y="310" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="290" y="310" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><text x="76" y="300" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">高亮在頭與身體</text><rect x="520" y="96" width="400" height="230" rx="12" fill="#12181f" stroke="#ff7b7288" stroke-width="1.4" opacity="0.6"/><text x="536" y="122" font-size="12" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">模型 B：看背景草地</text><rect x="580" y="140" width="34" height="34" rx="3" fill="#ff7b7244" stroke="#ff7b72" stroke-width="1.2"/><rect x="614" y="174" width="34" height="34" rx="3" fill="#ff7b7244" stroke="#ff7b72" stroke-width="1.2"/><rect x="648" y="140" width="34" height="34" rx="3" fill="#ff7b7244" stroke="#ff7b72" stroke-width="1.2"/><rect x="682" y="174" width="34" height="34" rx="3" fill="#ff7b7244" stroke="#ff7b72" stroke-width="1.2"/><rect x="580" y="140" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="614" y="140" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="648" y="140" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="682" y="140" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="716" y="140" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="750" y="140" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="580" y="174" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="614" y="174" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="648" y="174" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="682" y="174" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="716" y="174" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="750" y="174" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="580" y="208" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="614" y="208" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="648" y="208" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="682" y="208" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="716" y="208" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="750" y="208" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="580" y="242" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="614" y="242" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="648" y="242" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="682" y="242" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="716" y="242" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="750" y="242" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="580" y="276" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="614" y="276" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="648" y="276" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="682" y="276" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="716" y="276" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="750" y="276" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="580" y="310" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="614" y="310" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="648" y="310" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="682" y="310" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="716" y="310" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><rect x="750" y="310" width="34" height="34" rx="3" fill="none" stroke="#30363d" stroke-width="0.7" opacity="0.4"/><text x="536" y="300" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">高亮在右下角草地</text><rect x="60" y="344" width="890" height="70" rx="12" fill="#1c2230" stroke="#e0a45855" stroke-width="1.4"/><text x="80" y="370" font-size="12" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩張熱圖都在說「我看這裡」，但只有 A 的答案有道理。</text><text x="80" y="396" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">亮在背景＝捷徑特徵（shortcut learning）；這時要換資料、做遮擋測試（occlusion），不能只看準確率。</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">熱圖漂亮不代表模型學對：亮在背景草地就是典型的捷徑特徵（shortcut learning）。</figcaption>
</figure>
<!-- /CNGC-FIGURE:shortcut -->

同一題「黃金獵犬」，兩個模型都答對：

- **模型 A**：高亮在頭與身體 → 看起來合理。
- **模型 B**：高亮在右下角的草地 → 典型的**捷徑特徵**（圖片裡有草地才出現狗）。

熱圖能做的：幫你發現「模型看的不是你想的地方」。熱圖不能做的：證明模型「推理正確」。
要抓捷徑，通常還要配遮擋測試（把高亮區域遮掉看信心掉多少）、換背景測試、或看多張圖的共同模式。

## 11. 六個常見誤解

| 誤解 | 事實 |
|---|---|
| Grad-CAM 需要 GAP | 不需要；它只需要能算梯度 |
| 它可以證明模型正確 | 它只顯示「看哪裡」，看錯地方也能答對（§10） |
| 熱圖數值有絕對意義 | 只有相對大小有意義，顯示前一定要正規化 |
| 用 softmax 機率比較好 | 飽和後梯度極小；論文用 softmax 前的 logit |
| 層數越深越好 | 越深語意越強但解析度越低；要細節得往前一層 |
| Grad-CAM 等於 CAM | 在純 GAP + Linear 時等價（實測差 8.89e-18），其他情況不同 |

## 附錄 A 速查表

| 想問的事 | 答案 |
|---|---|
| 權重 | `α[k,c] = mean(∂yᶜ/∂Aᵏ)` |
| 熱圖 | `ReLU(Σ_k α[k,c] · Aᵏ)` |
| `Z` | `H × W`（梯度平均的分母） |
| 為何 ReLU | 只留支持該類別的區域 |
| 為何用 logit | softmax 飽和、梯度太小 |
| 層的選擇 | 最後一層卷積（語意）或往前一層（解析度） |
| 上採樣 | 7×7 → 224×224（×32，雙線性） |
| 與 CAM 的關係 | 純 GAP + Linear 時 `Grad-CAM = ReLU(CAM/(H·W))` |
| 成本 | 前向 + 一次反向 |

> 九個面向的完整對照、以及「α 隨影像改變」的實測與但書，見 [CAM vs Grad-CAM](/cnn-cam-vs-gradcam/)。

## 附錄 B 常見錯誤

1. **對 prob 取梯度卻忘了鏈式法則**：`∂p/∂A = p(1−p)·∂y/∂A`，容易誤判。
2. **忘了 ReLU**：負值把色階吃掉，證據區看起來不亮。
3. **對整個 batch 的梯度取平均**：要逐張算。
4. **把熱圖 upsample 後當遮罩做分割**：它是證據分佈，不是像素級標註。
5. **在 `requires_grad=False` 的模型上跑**：要記得打開梯度、且別包 `no_grad`。
6. **只挑一張「好看」的熱圖**：要看多張、看錯誤樣本，才有資訊。

## 附錄 C 延伸閱讀與離線使用

站內：

- [CAM：用 GAP 算出模型在看哪裡](/cnn-cam/)——CAM 的推導與手算，Grad-CAM 的前身
- [GAP 是什麼？](/cnn-gap-head/)——GAP 與分類頭
- [卷積層 vs 全連接層](/cnn-conv-vs-fc/)——為什麼大 FC 讓權重對不回特徵圖
- [全連接層的運作](/cnn-fully-connected/)——`Wx + b` 與 softmax
- [圖解 CNN](/cnn-illustrated/)——整體資料流

站外：

- [Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization](https://arxiv.org/abs/1610.02391)
- [PyTorch `torch.autograd.grad` 文件](https://pytorch.org/docs/stable/generated/torch.autograd.grad.html)

離線：本頁是**單一 HTML 檔、零外部資源**；原始 Markdown 在同一層。

## 附錄 D 一頁精華（考前 10 分鐘）

| # | 記這一條 |
|---|---|
| 1 | `α[k,c] = mean(∂yᶜ/∂Aᵏ)`、`Lᶜ = ReLU(Σ α A)` |
| 2 | 用 logit 不用 softmax（飽和、梯度小） |
| 3 | ReLU 只留支持該類別的區域 |
| 4 | 7×7 熱圖 → 224×224（×32、雙線性、min-max、colormap） |
| 5 | 純 GAP + Linear：`Grad-CAM = ReLU(CAM/(H·W))`（實測 8.89e-18） |
| 6 | 中間插 ReLU 後 `α ≠ w/(H·W)`（實測 0.0645 vs 0.0938） |
| 7 | 成本：多一次反向；好處：不必改架構 |
| 8 | 熱圖說「哪裡」，不證明「看對」 |

## 附錄 G 實測原始輸出

`verify_cnn_gradcam.py` 的完整輸出（Python 3.15.1 / NumPy 2.5.4，本機執行）：

```text
------------------------------------------------------------------------
1. step 4: average the gradient of each map -> alpha
   d y / d A1 = [[0.2, 0.4], [0.1, 0.3]]   ->  alpha1 = 0.2500
   d y / d A2 = [[0.1, 0.1], [0.1, 0.1]]   ->  alpha2 = 0.1000
   d y / d A3 = [[-0.2, -0.2], [-0.2, -0.2]]   ->  alpha3 = -0.2000
------------------------------------------------------------------------
2. step 5-6: weighted sum, then ReLU
   L = 0.25*A1 + 0.1*A2 - 0.2*A3 =
 [[ 2.6 -0.3]
 [ 2.1  0.2]]
   ReLU(L) =
 [[2.6 0. ]
 [2.1 0.2]]
   cells removed by ReLU: 1 of 4
------------------------------------------------------------------------
3. same maps, CAM weights instead of gradients (page 7)
   CAM  = 0.8*A1 + 0.1*A2 - 0.2*A3 =
 [[ 8.1 -0.3]
 [ 6.5  1.3]]
   mean(CAM) = 3.900   (the class logit, from page 7)
   CAM vs Grad-CAM differ because alpha != w: [0.25, 0.1, -0.2] vs [0.8, 0.1, -0.2]
------------------------------------------------------------------------
4. the gradient is not always w: put a ReLU before the GAP
   model: A -> ReLU -> GAP -> Linear,  y = 0.7866
   analytic vs finite difference: True (max diff 4.38e-11)
   alpha = mean gradient = [ 0.0645 -0.0137  0.0125]
   w / (H*W)             = [ 0.0938 -0.0438  0.025 ]
   -> equal only where ReLU passes everything
------------------------------------------------------------------------
5. pure GAP + Linear: Grad-CAM collapses onto CAM
   logits: [-0.5657 -0.5422 -0.8016]
   mean(CAM) by class: [-0.5657 -0.5422 -0.8016]
   identity max abs diff: 1.11e-16
   Grad-CAM == ReLU(CAM/(H*W))? True (max diff 8.89e-18)
------------------------------------------------------------------------
6. what the upsample does
   7x7 = 49 values -> bilinear to 224x224 = 50,176 pixels (x32 each side)
   scaling: min-max to 0-1, then a colormap; no new information is created
------------------------------------------------------------------------
7. picking a layer: replay the same idea at three depths
   early conv 56x56x64  -> heat map 56x56, upsample x4
   mid   conv 28x28x128 -> heat map 28x28, upsample x8
   last  conv  7x 7x512 -> heat map  7x 7, upsample x32
------------------------------------------------------------------------
```

---

*本頁為個人學習筆記整理；圖表為手繪內嵌 SVG，數字全部由附錄 G 的程式算出。*
