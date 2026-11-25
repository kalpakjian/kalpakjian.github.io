---
title: MeanFlow 不是「flow 一步就好」：平均速度場、JVP，與車機該先量的 baseline
date: 2026-11-24 20:00:00
categories:
  - AI 研究札記
tags:
  - MeanFlow
  - Flow Matching
  - Diffusion
  - JVP
  - 一步生成
  - 機器人
  - 車機
  - 論文導讀
index_img: /img/covers/meanflow-average-velocity-jvp-zh.png
banner_img: /img/covers/meanflow-average-velocity-jvp-zh.png
---

「這個方向對，但四個技術表述都要改。」——這篇是討論 MeanFlow 之後留下的修正版。

我最初的版本把 MeanFlow 說成「flow matching 本來就可以一步」，也把 diffusion 講成「不連續」。讀完論文與它的訓練介面之後，這兩句都得改寫。真正的重點不是步數，而是<strong>學習目標被換掉了</strong>：從瞬時速度 v 換成區間平均速度 u。而這個替換無法只靠修改 loss 完成——訓練時必須對網路<strong>自己的輸出</strong>算 Jacobian-vector product（JVP）。

<!-- more -->

> <strong>一句話結論</strong>：MeanFlow 把取樣壓到 1 次前向（1-NFE）而且仍保留 classifier-free guidance，但那不是「flow 一步就好」，而是要求網路自我一致地滿足平均／瞬時速度的恆等式；代價落在訓練的 JVP，不在推論。<br />
> 對車機與機器人，真正的門檻不是 FID，而是少了中間步之後，失敗變得更難偵測。<br />

> <strong>2026-11-24 補充</strong>：新增 §8，補上「一步 vs 多步到底差多少」的 FID 對照（1-NFE 3.43、2-NFE 2.20、SiT-XL 2.06），以及三個容易被抄錯的細節（JVP 是 forward-mode、同一個場而非雙頭輸出、IntMeanFlow 是語音任務）。<br />

## 三十秒結論

| 問題 | 一句話回答 |
|---|---|
| MeanFlow 是什麼 | flow matching 的推廣：學的是區間平均速度 u，不是瞬時速度 v |
| 憑什麼一步 | u 直接對應整段位移，z0 = z1 − (t − r)·u |
| 代價在哪 | loss 的 target 含網路自己的 JVP；論文實測算錯就直接沒有結果 |
| 1-NFE 品質 | ImageNet 256×256、from scratch：FID 3.43（論文自報） |
| 車機／機器人 | 省的是去噪迭代；先量 baseline 延遲，別一開始就付 JVP 的工程成本 |

## 1. 我原本講錯的四件事

| 我原本的說法 | 較精確的版本 |
|---|---|
| Diffusion 是「噪點 − denoise = 新圖」，多步重複去噪 | 從噪聲出發、反覆估計並移除噪聲；DDPM 預設多步，但蒸餾、consistency、shortcut 類方法同樣能大幅減步 |
| Flow 是連續、Diffusion 是不連續 | 兩者都把生成視為連續機率路徑上的 ODE；差別在參數化與訓練目標，不是連續 vs 不連續 |
| MeanFlow 直接學「起點到終點的平均速度」就一步完成 | 方向對，但機制是<strong>必須滿足恆等式</strong>，不是單純回歸一個積分值 |
| Flow matching 就是 MeanFlow | 不是：一般 conditional flow matching 學瞬時速度、推理仍要積分；MeanFlow 是設計成可一步取樣的變體，且在 r → t 時退化成 v |

第三列值得修得這麼細，因為它決定你的工程成本：如果只是「換個 target」，那任何 flow 模型改一改都能一步；實際上你要多一條 forward-mode AD 的訓練管線。

## 2. 真正的那一步：MeanFlow Identity

把生成想成從噪聲 z1 走到資料 z0 的一條機率路徑，瞬時速度的積分就是位移；平均速度則定義成「位移 ÷ 時間間隔」：

```text
論文式 4      (t − r) · u(z, r, t) = ∫ v(z_s, s) ds      （對 s 從 r 積到 t）
論文式 6      u(z, r, t) = v(z, t) − (t − r) · D u       ← 對 t 微分後得到的恆等式
論文式 8      D u = v(z, t) · du/dz + du/dt              ← 全導數展開
```

式 8 的 D u 就是 Jacobian-vector product：把 u 對 (z, r, t) 的雅可比矩陣乘上切向量 (v, 0, 1)。論文用 `torch.func.jvp`／`jax.jvp` 算它。附錄的破壞性實驗顯示：<strong>JVP 算錯，整個訓練就沒有可用結果</strong>——這是這套方法唯一不能省的工程步驟。

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 430" role="img" aria-label="兩種學法對照：flow matching 學瞬時速度需沿路徑積分多步，MeanFlow 學平均速度一次前向到位；下方為 MeanFlow Identity 與 JVP 計算" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">
<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker></defs>
<rect x="0.75" y="0.75" width="938.5" height="428.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="44" font-size="20" font-weight="700" fill="#e6edf3">同一條路徑，兩種學法</text>
<text x="48" y="70" font-size="13" fill="#8b949e">瞬時速度 v 要沿路徑積分很多小步；平均速度 u 一次跳到終點</text>
<line x1="486" y1="96" x2="486" y2="272" stroke="#30363d" stroke-width="1.5" stroke-dasharray="6 6"/>
<text x="60" y="112" font-size="14" font-weight="600" fill="#c9d1d9">① v：多步積分（flow matching）</text>
<text x="512" y="112" font-size="14" font-weight="600" fill="#c9d1d9">② u：一步生成（MeanFlow）</text>
<text x="255" y="142" font-size="12" fill="#8b949e" text-anchor="middle">沿著路徑，一小步一小步積分</text>
<path d="M80,190 C 150,132 210,248 280,182 C 330,136 390,168 430,190" fill="none" stroke="#8b949e" stroke-width="2"/>
<circle cx="80" cy="190" r="5" fill="#2dd4bf"/>
<circle cx="430" cy="190" r="5" fill="#fbbf24"/>
<text x="80" y="222" font-size="12" fill="#8b949e" text-anchor="middle">z1 噪聲</text>
<text x="430" y="222" font-size="12" fill="#8b949e" text-anchor="middle">z0 資料</text>
<text x="255" y="262" font-size="12" fill="#6e7681" text-anchor="middle">步數越多，通常越穩也越慢</text>
<line x1="540" y1="190" x2="846" y2="190" stroke="#2dd4bf" stroke-width="4" marker-end="url(#ah)"/>
<circle cx="532" cy="190" r="5" fill="#2dd4bf"/>
<circle cx="856" cy="190" r="5" fill="#fbbf24"/>
<text x="532" y="222" font-size="12" fill="#8b949e" text-anchor="middle">z1 噪聲</text>
<text x="856" y="222" font-size="12" fill="#8b949e" text-anchor="middle">z0 資料</text>
<text x="694" y="168" font-size="13" fill="#e6edf3" text-anchor="middle">u(z, r, t) × (t − r)</text>
<text x="694" y="262" font-size="12" fill="#6e7681" text-anchor="middle">1 次前向 = 1-NFE（仍可含 guidance）</text>
<rect x="48" y="296" width="844" height="104" rx="12" fill="#161b22" stroke="#30363d" stroke-width="1.5"/>
<text x="68" y="324" font-size="13" fill="#8b949e">MeanFlow Identity（論文式 6 與式 8；D 為全導數）</text>
<text x="68" y="356" font-size="16" font-weight="600" fill="#e6edf3">u = v − (t − r) · D u</text>
<text x="68" y="384" font-size="13" fill="#8b949e">D u = v · du/dz + du/dt　（以 forward-mode AD 的 JVP 計算；算錯就訓練不出來）</text>
</svg>
<figcaption>圖 1：左邊是 flow matching 的做法——沿路徑積分瞬時速度，步數換精度也換延遲；右邊是 MeanFlow 的做法——直接預測整段的平均速度。下方是它必須滿足的恆等式，其中 D u 要靠 JVP 計算。</figcaption>
</figure>

## 3. 訓練目標長什麼樣

```text
論文式 10     u_target = v − (t − r) · ( v · duθ/dz + duθ/dt )
論文式  9     L(θ) = E ‖ uθ(z, r, t) − sg(u_target) ‖²
```

三個實務含義：

1. 唯一的 ground-truth 訊號是瞬時速度 v（由 conditional flow matching 直接採樣得到），<strong>不需要真的去算積分</strong>。
2. target 裡放的是<strong>網路自己的導數</strong>再套 stop-gradient，避免二次反傳——所以它同時是迴歸也是自洽約束。
3. 這解釋了論文為什麼能宣稱 self-contained：不用預訓練、不用蒸餾、不用 curriculum。

示意寫法（未對照官方實作，jvp 的切向量需含 r 分量 0）：

```python
def meanflow_loss(net, z, r, t, v):                     # v 來自 CFM 的條件速度
    pred = net(z, r, t)                                 # uθ
    _, du = torch.func.jvp(net, (z, r, t), (v, 0.0, 1.0))   # 式 8 的 JVP
    target = v - (t - r) * du
    return ((pred - target.detach()) ** 2).mean()       # stop-grad，不做二次反傳
```

## 4. 我還會再修的兩處

第一，區分「誰比較少步」的不是連續性，而是<strong>路徑彎曲度</strong>。VP／VE 噪聲排程讓速度場比較「硬」，Euler 的誤差沿曲率累積；線性插值的 CFM 路徑比較直，同樣步數下誤差更小。而 diffusion 只要能寫成連續時間的 SDE／ODE，「不連續」就只存在於離散實作這一層。

第二，MeanFlow 不是 flow matching 的平行物，而是<strong>嚴格推廣</strong>：r → t 時 u(z, t, t) 退化成 v(z, t)，一般 flow matching 是 r = t 的特例。論文 ablation 那節的標題就叫「From Flow Matching to Mean Flows」。

## 5. CFG 不會讓 NFE 變兩倍

一步模型最常見的隱形陷阱是 guidance：取樣時跑兩次前向（有條件／無條件）就變成 2-NFE，「一步」名存實亡。MeanFlow 的作法是把 guidance 寫進<strong>ground-truth 場</strong>：

```text
v_cfg(z, t | c) = ω · v(z, t | c) + (1 − ω) · v(z, t)
```

再對 v_cfg 套同一套恆等式，於是 1-NFE 與 guidance 可以同時成立。這點直接影響延遲預算：評估任何「一步」方法時，要問的應該是「含 guidance 幾 NFE」。

## 6. 車機與機器人：把評估順序倒過來

1. <strong>先量 baseline，再決定要不要一步</strong>。10–30 Hz 控制下，如果 policy 網路本身只有幾 M 參數，flow matching 配 4 步 Euler 可能已經在毫秒級；此時瓶頸通常在視覺 encoder 與前後處理，一步的邊際收益接近零。
2. <strong>務實路徑</strong>：flow matching → 逐步減步數（8 → 4 → 2）→ 真的卡在延遲再上 MeanFlow 或 shortcut 類方法。你們的示範資料量遠小於 ImageNet 級別，JVP 帶來的不穩定風險要先用小規模 ablation 驗過。
3. <strong>最該補進評估表的不是 FID，而是失敗可偵測性</strong>。一步生成消掉了中間步這條軌跡，出錯時沒有逐步收斂的訊號可看，OOD 偵測與 fallback 反而更難做——對無人系統與車端，這比省下 20 ms 更貴。
4. action chunk 的思路本身與 MeanFlow 無關：先輸出未來 K 個 control step、執行前幾步、取得新觀測再重規劃（receding horizon），這是 Diffusion Policy／flow policy 既有的做法；一步生成只是把「產生這段 chunk」的延遲壓低。

## 7. 查證

| 項目 | 連結 | 我核到什麼 |
|---|---|---|
| MeanFlow 論文 | [2505.13447](https://arxiv.org/abs/2505.13447) | Geng、Deng、Bai、Kolter、He（CMU／MIT），2025-05；1-NFE FID 3.43，ImageNet 256×256，from scratch |
| Action-to-Action Flow Matching | [2602.07322](https://arxiv.org/abs/2602.07322) | 確實存在；對應「以上一個動作為起點、而非純高斯噪聲」的路線 |
| action chunk／receding horizon 的來源 | [2505.22094](https://arxiv.org/abs/2505.22094) | 我沒有逐段核對；這個做法在機器人模仿學習裡是通例 |
| 第一作者本人的導讀 | [CMU CSD PhD Blog](https://www.cs.cmu.edu/~csd-phd-blog/2026/mean-flows/) | 2026-09-03，Zhengyang Geng；§8 的 FID 對照與「JVP 成本」說法出自此處 |
| IntMeanFlow（去 JVP 的語音版本） | [2510.07979](https://arxiv.org/abs/2510.07979) | 2025-10，cs.SD；積分速度蒸餾，token→spectrogram 1-NFE、text→spectrogram 3-NFE |
| 官方實作 | [Gsunshine/meanflow](https://github.com/Gsunshine/meanflow) | 論文為 NeurIPS 2025 oral；本文示意程式碼未對照此 repo |

> <strong>查證說明</strong>：本文的式 4、6、8、9、10 於 2026-11-24 直接讀取 arXiv HTML 版逐式核對；FID 3.43 是論文自報數字，我<strong>沒有重跑</strong>。<br />
> 「Tesla 車機介面採用 MeanFlow」我找不到可靠公開來源，本文不採信。<br />
>
> <strong>封面與圖表</strong>：封面由本機 ComfyUI 的 Qwen-Image 生成（刻意不含文字）；圖表為手繪內嵌 SVG——含中文標籤的圖表交給 AI 生圖會爛成方塊。<br />

## 8. 補充：一步到底差多少，與三個容易抄錯的細節

先把「一步等於多步」這個印象修掉。同一個 benchmark（ImageNet 256×256）上：

| 模型 | 取樣 NFE | FID（越低越好） |
|---|---|---|
| MeanFlow MF-XL | 1 | <strong>3.43</strong> |
| MeanFlow（更長訓練） | 2 | <strong>2.20</strong> |
| Shortcut-XL | 1 | 10.60 |
| iCT-XL | 1 | 34.24 |
| IMM-XL（1-step 但含 guidance） | 2 | 7.77 |
| DiT-XL | 250（含 guidance 500） | 2.27 |
| SiT-XL | 250（含 guidance 500） | 2.06 |

正確的結論是：一步把「從零訓練的一步模型」與多步強權之間的差距，從約 5 倍壓到<strong>大約 1 分</strong>；給它第二次評估就到 2.20，幾乎貼上花了兩個數量級算力的 DiT／SiT。IMM-XL 那一列同時驗證了 §5 的判準——它的「1-step」其實是 2-NFE，因為 guidance 吃掉了另一次前向。

### 8.1 三個容易被抄錯的細節

1. <strong>JVP 不是多一次 backward</strong>。它是 forward-mode AD 的切線傳播，成本量級接近一次前向；target 之所以要 stop-gradient，正是為了不做二次反傳。有些轉述寫成「多一次反向」，拿去估訓練預算是會估錯的。
2. <strong>不是雙頭輸出</strong>。uθ 是同一個場，在 (z, r, t) 上求值；r = t 時它就是瞬時速度 v。沒有第二個 head、也沒有兩個 loss，只是多吃了兩個時間座標。
3. <strong>對 r 的偏導項乘 0 這件事有前提</strong>。它成立只在 r 與 t 互相獨立時；若取樣時讓 r 依賴 t，Leibniz 規則會補上 −v(z_r, r)·dr/dt 這一項。論文腳註 1 有寫，但抄公式時最常被省略。

### 8.2 「去 JVP」的後續研究只解決了一半

常被拿來說「JVP 可以省掉」的是 IntMeanFlow（語音 TTS）：用教師模型的瞬時速度在區間上近似平均速度，即積分速度蒸餾，同時去掉 JVP 與 self-bootstrap，理由寫得很清楚——JVP 吃 GPU 記憶體、self-bootstrap 讓訓練不穩。它報的是 token→spectrogram 1-NFE、text→spectrogram 3-NFE。

兩件事要分開看：那是<strong>語音</strong>任務，沒有 ImageNet 對照；而「區間拆分」不是它的方法，是 MeanFlow 自己在取樣時把 [0,1] 切成多段換品質的 few-step 做法，跟降低 JVP 需求無關。把這條線讀成「影像模型也有通用免 JVP 方案」，就會高估目前的成熟度。
