---
title: MeanFlow 白話版：一步生成的關鍵是平均速度，而 JVP 是它的門票
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

先講一個畫面。想像你被丟進一團濃霧，手上有一台裝置，每按一次它就告訴你「此刻該往哪走、走多快」。你照著走一小段，再按一次、再走一小段……霧散了，你剛好站在目的地。

這就是現在主流生成模型（diffusion、flow matching）在做的事：<strong>每一小步都問一次方向</strong>，問 50 次、250 次，圖才慢慢浮出來。

MeanFlow 換了一個問法：<strong>不問「此刻往哪走」，改問「從這裡到終點，整段路的平均往哪走、多快」</strong>。知道平均，理論上一步就能到。

這篇是讀論文之後的筆記。第一次寫的時候我把好幾件事講錯了，逐式核對才改過來，所以下面每個專有名詞都會先解釋清楚，公式也會翻成白話再寫一次。

<!-- more -->

> <strong>一句話結論</strong>：MeanFlow 把取樣從「問很多次」變成「問一次」，而且還保得住 guidance；但它的關鍵不是省步數，而是<strong>換掉學習目標</strong>——從瞬時速度改成整段的平均速度，代價是訓練時要多算一個 JVP。<br />
> 如果你只記一件事：<strong>它不是把 diffusion 加速，而是換一個問題來問</strong>。<br />

> <strong>2026-11-24 改寫</strong>：整篇改成白話版、補上名詞表與 JVP 的白話解釋；技術結論與數字不變。<br />

## 0. 這篇適合誰

- 知道 diffusion 大概是在「去噪」，但沒推過公式
- 聽過 flow matching，卻說不出它跟 diffusion 差在哪
- 看論文時被 JVP、平均速度、consistency 這些字一句話帶過，心裡沒底

那就照順序讀。如果你只想要結論，跳到 §7（一步到底差多少）與 §9（車機／機器人怎麼用）。

## 1. 名詞先落地

後面每一節都會用到這些字。先掃一眼，讀到再回頭查也可以。

### 1.1 先懂這九個

| 名詞 | 白話解釋 | 在這篇的角色 |
|---|---|---|
| 資料分佈 | 「所有真實圖片長什麼樣子」的整體形狀，不是某一張圖 | 生成的終點 |
| 噪聲 z1 | 純隨機的起點，通常取高斯分佈 | 生成的起點 |
| 資料 z0 | 目標樣本。論文慣例是 <strong>t = 1 在噪聲端、t = 0 在資料端</strong> | 終點 |
| 速度場 v(z, t) | 在每個位置、每個時刻都插一支箭頭，告訴你「往哪走、走多快」。想像風場 | 傳統 flow matching 學的東西 |
| ODE（常微分方程） | 「照著箭頭走」的規則。沿箭頭一小步一小步走完＝積分 | 取樣過程 |
| 步數／NFE | NFE 是網路被呼叫幾次。步數 50 就是叫 50 次，延遲大致成正比 | 為什麼想要一步 |
| Flow Matching | 不學去噪，直接學箭頭。把真圖與噪聲連一條直線，箭頭就是這條線的方向 | 對照組 |
| Diffusion（DDPM） | 反過來學「怎麼一點一點拿掉噪聲」。噪聲排程是彎的，所以步數多 | 對照組 |
| FID | 比較生成圖與真圖的統計距離，越低越像。3 左右人眼已經很難分 | 品質指標 |

### 1.2 再懂這十一個

| 名詞 | 白話解釋 | 在這篇的角色 |
|---|---|---|
| 平均速度 u(z, r, t) | 從時刻 r 走到時刻 t 這段路的平均箭頭＝位移 ÷ 時間長度 | MeanFlow 學的東西 |
| 恆等式（identity） | 不管網路長怎樣都必須成立的數學關係。用它把「算不出來的積分」換成「算得出來的微分」 | 訓練的核心 |
| 偏導數 vs 全導數 | 偏導數：站在原地、只讓時間流逝看到的變化。全導數：跟著粒子一起跑看到的變化（位置也在變） | 差一個位置項 |
| 雅可比矩陣（Jacobian） | 一個函數對所有輸入的偏導，排成一張表 | JVP 的一半 |
| JVP | 雅可比 × 一個方向向量＝「沿這個方向走，輸出變多快」。實務上就是「時間動、位置也跟著動」的合併效果 | 訓練必須算 |
| forward-mode AD | 沿著「輸入方向」傳導的自動微分，成本約等於一次前向 | JVP 怎麼算 |
| stop-gradient | 把某項當成常數，梯度不穿過去，用來避免二階導 | 讓目標不要抖 |
| 蒸餾（distillation） | 先練一個多步的老師，再讓一步的學生模仿它。MeanFlow 不需要 | 它贏在哪 |
| consistency／shortcut 模型 | 前者要求「同一條軌跡上各時刻的輸出都指向同一個終點」；後者學「從任何時刻直接跳到終點」的捷徑。兩者都靠外加約束硬拉 | 它的親戚 |
| CFG（無分類器引導） | 把「有條件」與「無條件」的預測外插，讓結果更貼提示詞；代價是兩次前向 | 一步模型的陷阱 |
| action chunk／receding horizon | 一次輸出未來 K 步動作；只執行前幾步就重看、重規劃 | 機器人場景 |

## 2. 為什麼非得走很多步？

白話版：<strong>箭頭不是直的</strong>。

你照著當下的箭頭走一小段，位置變了，而新位置上的箭頭方向又不一樣了——所以你必須停下來重問。路越彎，重問的次數越多；路越直，就可以跨大步。

論文裡那個「路有多彎」的量叫曲率。實務上有個容易搞錯的推論：很多人以為「flow 是連續的、diffusion 是不連續的，所以 flow 步數少」。不對。兩者都能寫成連續時間的 ODE；真正的差別在<strong>路徑形狀</strong>——diffusion 常見的噪聲排程（VP／VE）讓速度場比較「硬」，彎得厲害；flow matching 用線性插值把真圖和噪聲直接連直線，路比較直，Euler 這種笨方法同樣步數下誤差更小。

所謂「笨方法」就是：站在原地看箭頭，往前跨一小步，再看一次。數學上叫 Euler 法，是 ODE 求解器裡最簡單的一種。它需要的次數，就決定了 NFE，也就決定了延遲。

## 3. MeanFlow 的招式：改問「平均速度」

傳統 flow matching 學的是 v(z, t)：<strong>此刻</strong>這支箭頭。
MeanFlow 學的是 u(z, r, t)：<strong>從時刻 r 到時刻 t，整段路平均下來</strong>的那支箭頭。

定義沒什麼玄機，就是國中的「平均速率」：

```text
論文式 4    (t − r) · u(z, r, t) = ∫ v(z_s, s) ds      （s 從 r 積到 t）
```

白話讀法：<strong>（時間長度）×（平均速度）＝ 整段位移</strong>。右邊那個積分就是「把路上每一瞬間的箭頭全部加起來」。

有了平均值，你就不必一小步一小步走：

```text
取樣公式    z_r = z_t − (t − r) · u(z_t, r, t)
一步版本    z0  = z1 − u(z1, 0, 1)
```

白話讀法：<strong>終點 ＝ 起點 −（時間長度）×（平均速度）</strong>。就是「起點 + 平均速度 × 時間 = 終點」那條公式，只是方向相反。

這裡要小心中文語感：不是「把多步硬壓成一步」的近似，而是<strong>換了一個學習目標</strong>。目標換了，一步取樣才是它的自然結果，而不是硬湊出來的。

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
<figcaption>圖 1：左邊是 flow matching 的做法——沿路徑積分瞬時速度，步數換精度也換延遲；右邊是 MeanFlow——直接預測整段的平均速度。下方是它必須滿足的恆等式，其中 D u 要靠 JVP 計算。</figcaption>
</figure>

## 4. 關鍵那一招：把「算不出來的積分」換成「算得出來的微分」

訓練時最尷尬的地方在這裡：定義裡有一個積分，但我們根本不知道整條路長什麼樣，怎麼算？

論文用大一微積分解決：<strong>對定義兩邊微分，積分就消失了</strong>。三步而已。

```text
① 兩邊乘開            (t − r) · u = ∫ v ds
② 對 t 微分（r 當常數）   u + (t − r) · du/dt = v
③ 移項               u = v − (t − r) · du/dt        ← 論文式 6
```

第 ② 步用了兩個基本工具：左邊是乘法律（product rule），右邊是微積分基本定理（微分和積分互相抵消，只剩端點那一項）。翻成白話：

> 平均箭頭 ＝ 此刻的箭頭 −（區間長度）×（平均箭頭正在改變的速度）<br />

這條關係就叫 MeanFlow Identity。它為什麼好用？因為右邊<strong>只需要此刻的 v，以及 u 的導數</strong>，完全不必知道整條路——積分在推導過程中被消掉了。原本「要算整段路」的難題，變成「要算某一點的導數」。

## 5. 為什麼會冒出 JVP 這個字

剩下最後一塊：du/dt 到底是哪種導數？

它<strong>不是</strong>「站在原地、只讓時間流逝」看到的變化（那叫偏導數），而是<strong>跟著粒子一起跑</strong>看到的變化——因為粒子自己也在移動。所以要用連鎖律，把兩份變化加起來：

```text
論文式 8    du/dt（全導數） = (du/dz) · v + du/dt（偏導數那一份）
```

換句話說，u 會不會變，取決於兩件事：時間前進了、而且位置被 v 帶著移動了。把 u 對 (z, r, t) 的所有偏導排成一張表（雅可比矩陣），乘上「這次往哪動」的向量 (v, 0, 1)——<strong>這個乘法就是 JVP</strong>（Jacobian-vector product，雅可比向量積）。

三個常見誤解先釘住，免得後面算錯：

1. <strong>JVP 不是多一次反向傳播</strong>。它是 forward-mode AD（沿輸入方向傳導），成本量級接近一次前向。target 之所以要 stop-gradient，正是為了不做二次反傳。
2. <strong>不是雙頭輸出</strong>。uθ 是同一個網路、同一個場，只是多吃了 r 與 t 兩個時間座標；r = t 時它就退化成瞬時速度 v。
3. <strong>「r 那一項乘 0」有前提</strong>。只有在 r 與 t 互相獨立時才成立；若取樣時讓 r 依賴 t，Leibniz 規則要多補一項 −v(z_r, r)·dr/dt。論文腳註有寫，抄公式最常漏這一行。

## 6. 訓練時到底在算什麼

三個式子，一行一行讀：

```text
論文式 10   u_target = v − (t − r) · ( v · duθ/dz + duθ/dt )
論文式  9   L(θ) = E ‖ uθ(z, r, t) − sg(u_target) ‖²
```

- 唯一的「標準答案」是 v，而 v 很好拿：flow matching 把真圖和噪聲連成一條直線，這條線的方向就是 v。
- 括號那項是<strong>網路自己的導數</strong>（等於自己的 JVP）。所以這是自我一致的訓練：教網路去滿足它自己必須滿足的關係。
- sg 是 stop-gradient：把 target 當常數，梯度不穿過去。不加這個，就等於要對雅可比再求一次導（二階），成本會爆。

程式長這樣（示意，沒有對照官方 repo）：

```python
def meanflow_loss(net, z, r, t, v):                        # v 由 flow matching 的直線直接算
    pred = net(z, r, t)                                    # uθ
    _, du = torch.func.jvp(net, (z, r, t), (v, 0.0, 1.0))  # JVP，切向量 (v, 0, 1)
    target = v - (t - r) * du
    return ((pred - target.detach()) ** 2).mean()          # detach() 就是 stop-gradient
```

論文附錄做過破壞性實驗：<strong>JVP 算錯，訓練就直接沒有可用結果</strong>。所以它不是實作細節，是主體。

## 7. 一步到底差多少（別被「一步」兩個字騙）

同一個 benchmark（ImageNet 256×256）：

| 模型 | 取樣 NFE | FID（越低越好） |
|---|---|---|
| MeanFlow MF-XL | 1 | <strong>3.43</strong> |
| MeanFlow（更長訓練） | 2 | <strong>2.20</strong> |
| Shortcut-XL | 1 | 10.60 |
| iCT-XL | 1 | 34.24 |
| IMM-XL（標 1-step，但含 guidance） | 2 | 7.77 |
| DiT-XL | 250（含 guidance 500） | 2.27 |
| SiT-XL | 250（含 guidance 500） | 2.06 |

怎麼讀這張表：

1. 一步把「從零訓練的一步模型」與多步強權之間的差距，從約 5 倍壓到<strong>大約 1 分</strong>——是拉近，不是追平。
2. 給它第二次評估（2-NFE）就到 2.20，幾乎貼上 DiT／SiT，而那些模型每張圖要花兩個數量級的算力。
3. 注意 IMM-XL 那列：它標「1-step」，但含 guidance 所以實際跑 2-NFE。這正是 §1.2 提過的陷阱——<strong>問一步模型，要問「含 guidance 幾 NFE」</strong>。

MeanFlow 怎麼避開這個陷阱？它把 guidance 直接寫進要學的場裡：

```text
v_cfg(z, t | c) = ω · v(z, t | c) + (1 − ω) · v(z, t)
```

再對 v_cfg 套同一套恆等式。於是「一步」和「貼提示詞」可以同時成立，不會偷偷變成兩次前向。

## 8. 四個常見誤解（這篇想拆掉的那幾個）

| 常見說法 | 問題在哪 |
|---|---|
| 「flow 連續、diffusion 不連續，所以 flow 步數少」 | 兩者都是連續時間上的 ODE；差別是路徑彎不彎（§2） |
| 「MeanFlow 就是 flow matching 換個 loss」 | 錯在「換個」二字：真正多出來的是 JVP 那條訓練管線與它的穩定性問題 |
| 「一步生成＝多步品質」 | 差約 1 分；要追平得多給一次評估（2-NFE 2.20） |
| 「已有研究去掉 JVP，所以影像模型也行」 | 那個研究是 <strong>IntMeanFlow</strong>，做的是語音：用教師的瞬時速度在區間上近似平均速度（積分速度蒸餾），去掉 JVP 與 self-bootstrap，報的是 1-NFE 語譜、3-NFE 文字轉語譜。沒有 ImageNet 對照；而「區間拆分」是 MeanFlow 自己 few-step 取樣的做法，跟免 JVP 無關 |

## 9. 車機與機器人：把評估順序倒過來

1. <strong>先量 baseline，再決定要不要一步</strong>。10–30 Hz 控制下，如果 policy 網路本身只有幾百萬參數，flow matching 配 4 步 Euler 可能已經在毫秒級；此時瓶頸通常在視覺 encoder 與前後處理，一步的邊際收益接近零。
2. <strong>務實路徑</strong>：flow matching → 逐步減步數（8 → 4 → 2）→ 真的卡在延遲，再上 MeanFlow 或 shortcut。你們的示範資料量遠小於 ImageNet，JVP 帶來的不穩定風險要先用小規模實驗驗過。
3. <strong>最該補進評估表的不是 FID，而是失敗可偵測性</strong>。一步生成少了中間那條軌跡，出錯時沒有逐步收斂的訊號可看，OOD 偵測與 fallback 反而更難做。
4. action chunk 那套（一次輸出未來 K 步、只執行前幾步、重看再規劃）跟 MeanFlow 無關，是 Diffusion Policy／flow policy 本來就有的做法；一步生成只是把「產生這段 chunk」的延遲壓低。

## 10. 查證

| 項目 | 連結 | 核到什麼 |
|---|---|---|
| MeanFlow 論文 | [2505.13447](https://arxiv.org/abs/2505.13447) | Geng、Deng、Bai、Kolter、He，2025-05；1-NFE FID 3.43，from scratch |
| 第一作者導讀 | [CMU CSD PhD Blog](https://www.cs.cmu.edu/~csd-phd-blog/2026/mean-flows/) | 2026-09-03；§7 的對照數字與 JVP 成本說法出自此處 |
| IntMeanFlow | [2510.07979](https://arxiv.org/abs/2510.07979) | 2025-10，cs.SD；積分速度蒸餾，1-NFE 語譜 |
| 官方實作 | [Gsunshine/meanflow](https://github.com/Gsunshine/meanflow) | NeurIPS 2025 oral；本文程式碼未對照此 repo |

> <strong>查證說明</strong>：式 4、6、8、9、10 於 2026-11-24 直接讀 arXiv HTML 版逐式核對；FID 全是論文與作者導讀的自報值，我<strong>沒有重跑</strong>。<br />
> 「Tesla 車機介面採用 MeanFlow」找不到可靠公開來源，本文不採信。<br />
>
> <strong>封面與圖表</strong>：封面由本機 ComfyUI 的 Qwen-Image 生成（刻意不含文字）；圖表為手繪內嵌 SVG。<br />
