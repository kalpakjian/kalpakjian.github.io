---
title: AINews 導讀：LLM 真的開始「讀寫神經網路權重」了嗎？拆開 48.1% 那個數字
date: 2026-11-05 14:30:00
categories:
  - AI 研究札記
  - 模型內部
tags:
  - AINews
  - Latent Space
  - Weight Space Programming
  - 權重空間程式設計
  - 權重編輯
  - Weight Editing
  - 機制可解釋性
  - Mechanistic Interpretability
  - 遞迴自我改進
  - RSI
  - DeepSeek
  - Super-agent
  - GDPx
  - GPT-6.2 Astra
  - Mythos
  - Kimi K3.1
  - JEPA
  - 新聞導讀
toc: true
index_img: /img/covers/ainews-weight-space-programming-zh.png
banner_img: /img/covers/ainews-weight-space-programming-zh.png
---


> <strong>這篇在講什麼</strong>：Latent Space 的 AINews 在 2026-11-03 那期，標題是〈[AINews] LLMs can read & write neural network weights!?!?〉，副標寫得更直白——**「Weight Space Programming cuts Autoresearch out of the RSI loop」**（權重空間程式設計，把自動研究從遞迴自我改進迴圈裡拿掉）。
>
> 這篇是<strong>中文導讀</strong>：先把當期頭條講清楚，再把同期其他重點（DeepSeek super-agent、GDPx 榜單、模型傳言、JEPA）壓成速覽，最後給我的判斷。
>
> 先講結論：**方向和訊號是真的，但標題的文法被吃掉了中間那句——它證明的是「拆牆」，不是「蓋樓」。** 這件事我在[另一篇](./astra-qwen-weight-editing-explained/)已經從原始 log 追過一次，這篇處理的是「新聞要怎麼讀」。
>
> 原文：[lspace.beehiiv.com/p/ainews-llms-can-read-write-neural-network-weights…](https://lspace.beehiiv.com/p/ainews-llms-can-read-write-neural-network-weights-weight-space-programming-cuts-autoresearch-out)。整理日期 2026-11-05。**第 1、3、4 節為原文內容整理，第 2、5 節為我的判讀**，兩種分開標註。

## 一句話總結

> **「LLM 能讀寫權重」是真的；但那個 7.9% → 48.1%，主要是把一顆卡在迴圈的模型叫醒，不是教會它新數學。**

為什麼這句話重要？因為講錯這一格，你會推導出一個很危險的結論——「以後不用訓練了，叫模型改權重就好」。AINews 自己其實也只寫到「the world has now gone from 0 to 1 on this very new RSI capability」（這條全新的 RSI 能力剛從 0 走到 1），而 Reddit 那側的技術反駁比這個更精確。

---

## 1. 頭條：Weight-Space Programming 到底是什麼

### 1.1 先把「舊方法」擺出來

AINews 的切入角度很好：要理解這件事有多誇張，得先回想 Karpathy 八個月前的 **autoresearch**。

那套東西的流程是：給一個聰明模型一座算力叢集，讓它**自己**跑一連串實驗把模型訓練出來——但中間那條路是硬的：

```text
寫 PyTorch / JAX 程式碼 → 跑 compute → 盯 loss curve
→ 讀 eval → 調 kernel → 洗資料 → 回到第一步
```

也就是說，「自動研究」自動的是**決策**，動手那層還是得寫 code、跑訓練。

**Weight-Space Programming 問的問題是：那條中間產線能不能整段跳過？**

> *"what if you just ask a smart model to directly read and edit the weights of a dumber model?"*

### 1.2 這件事在 ML 裡的比喻

AINews 用的比喻很準，我照抄（因為換個說法就會失真）：

> 這相當於**不讀原始碼，直接看編譯後執行檔的 1 與 0**，然後能做到：
>
> 1. **看出它在做什麼**
> 2. **給定失敗的執行痕跡，一次就把 bug 修好**；或者投降一點，**花 50 步**往某個大方向改善
> 3. **從零一次寫出整份網路權重**，而且贏過某些獨立訓練出來的模型

關鍵在「不需要梯度下降」。傳統微調是：算梯度 → 沿梯度方向更新權重 → 重複上萬步。這裡是：**模型自己看著權重數字，決定哪幾個數值該改成什麼**。

### 1.3 原文列出的 demo（含數字）

| # | Demo | 規模 |
|---|---|---|
| 1 | 從小型模型的原始權重**辨識出行為**（Atari 風格策略） | 讀 |
| 2 | **修好一個失敗的控制策略**（PPO 賽車） | 改 **3.5%** 的權重 |
| 3 | **從零生成** MinAtar Breakout 的權重 | 整份寫出 |
| 4 | 把 Qwen3.5-0.8B 的 **MATH-500 從 7.9% 拉到 48.1%** | 改 **0.016%**（約 131,072 個值） |

第 4 個就是所有新聞標題的來源，也是「指令遵循提升最多 3×」那句的來源。

### 1.4 原文自己也留了煞車

這段很容易在轉述時被剪掉，但它其實寫在正文裡：

> *"the exact thing we are really modeling is some variant of mechanistic interpretability … and right now unlikely to scale to more advanced tasks than simple games and RL policies"*
>
> （我們真正在建模的東西，本質上還是**機制可解釋性**的一個變體……而且目前不太可能擴展到比簡單遊戲和 RL 策略更複雜的任務。）

AINews 的定調是「方向對了、但別過頭」——它甚至引用 @giffmana 指出「50 步改善」那句**可能誇大了**（"possible overstatement here"）。

<!-- FIG1 -->
<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 470" role="img" aria-label="兩條路線對照：傳統梯度下降與權重空間程式設計" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto">
<defs>
<marker id="aws" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker>
<marker id="ateal" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker>
<marker id="aamb" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#fbbf24"/></marker>
</defs>
<rect x="0.75" y="0.75" width="938.5" height="468.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="48" font-size="21" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩條路線：一個在「過程」，一個在「數字」</text>
<text x="48" y="76" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同樣的目標（讓模型變好），動手的地方完全不同</text>

<rect x="48" y="104" width="404" height="316" rx="12" fill="#111820" stroke="#30363d" stroke-width="1.5"/>
<text x="72" y="136" font-size="14" fill="#7d8590" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">傳統微調（梯度下降）</text>
<g font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">
<rect x="72" y="154" width="356" height="34" rx="7" fill="#161b22" stroke="#30363d"/><text x="86" y="176" font-size="12.5" fill="#c9d1d9">① 寫 PyTorch / JAX 訓練碼</text>
<rect x="72" y="196" width="356" height="34" rx="7" fill="#161b22" stroke="#30363d"/><text x="86" y="218" font-size="12.5" fill="#c9d1d9">② 跑 compute、算梯度</text>
<rect x="72" y="238" width="356" height="34" rx="7" fill="#161b22" stroke="#30363d"/><text x="86" y="260" font-size="12.5" fill="#c9d1d9">③ 看 loss curve、換 kernel / 資料</text>
<rect x="72" y="280" width="356" height="34" rx="7" fill="#161b22" stroke="#30363d"/><text x="86" y="302" font-size="12.5" fill="#c9d1d9">④ 重複上萬步</text>
<rect x="72" y="330" width="356" height="44" rx="7" fill="#1a2029" stroke="#7d859066"/>
<text x="250" y="357" font-size="12.5" fill="#7d8590" text-anchor="middle">自動的是「決策」，動手那層沒自動</text>
</g>

<rect x="488" y="104" width="404" height="316" rx="12" fill="#0f1a1e" stroke="#2dd4bf44" stroke-width="1.5"/>
<text x="512" y="136" font-size="14" fill="#2dd4bf" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">權重空間程式設計（無梯度）</text>
<g font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">
<rect x="512" y="154" width="356" height="34" rx="7" fill="#11201f" stroke="#2dd4bf33"/><text x="526" y="176" font-size="12.5" fill="#c9d1d9">① 讀出權重張量，當數字看</text>
<rect x="512" y="196" width="356" height="34" rx="7" fill="#11201f" stroke="#2dd4bf33"/><text x="526" y="218" font-size="12.5" fill="#c9d1d9">② 判斷「病因在這幾個值」</text>
<rect x="512" y="238" width="356" height="34" rx="7" fill="#11201f" stroke="#2dd4bf33"/><text x="526" y="260" font-size="12.5" fill="#c9d1d9">③ 直接寫入新的數值</text>
<rect x="512" y="280" width="356" height="34" rx="7" fill="#11201f" stroke="#2dd4bf33"/><text x="526" y="302" font-size="12.5" fill="#c9d1d9">④ 驗證：跑 held-out 看有沒有變好</text>
<rect x="512" y="330" width="356" height="44" rx="7" fill="#132a28" stroke="#2dd4bf"/>
<text x="690" y="357" font-size="12.5" fill="#2dd4bf" text-anchor="middle">中間整條產線被跳過</text>
</g>

<path d="M 452 262 L 484 262" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#aamb)"/>
<text x="468" y="248" font-size="13" fill="#fbbf24" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">?</text>
<text x="468" y="450" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">省掉的是中間四步，不是驗證</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：左邊是大家熟悉的路線，右邊是這篇論文主張的路線。真正被省掉的是「寫 code → 算梯度 → 調參 → 重跑」那條迴圈，<strong>「驗證」那一步並沒有被省掉</strong>——這也是後面所有爭議的起點。</figcaption>
</figure>
<!-- /FIG1 -->

---

## 2. 我的判讀：這個標題的文法被吃掉了

### 2.1 三個「新聞版 vs 技術版」的落差

AINews 是**新聞**，它負責告訴你「有這件事、而且很多人震驚」。但新聞標題的語法是「A 能 B」，技術討論的語法是「A 在**某些條件下**能 B」。三個落差：

| 新聞標題的暗示 | 技術討論的實際說法 |
|---|---|
| LLM 能讀懂任意權重 | 前後層有**空間結構**（像熱區圖），toy model 特別好讀；**稠密中間層讀不動** |
| 一次改對 | 有一個實驗**直接改失敗了**，要讓模型自己造出探針（probe）才成功——那其實已經變成**激活分析**，不是純讀權重 |
| 48.1% 是能力提升 | 那是**拆掉迴圈**之後釋放的既有能力（詳見 2.2） |

第二點特別值得停一下：如果一個實驗必須先「給模型一堆可執行的探針」才能理解中間層，那它的本質更接近**以 LLM 為介面的機制可解釋性**，而不是科幻式的「直接看權重」。

### 2.2 那個 48.1%，拆開來看長這樣

<!-- FIG2 -->
<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 500" role="img" aria-label="MATH-500 分數變化與答案被截斷比例的對照" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto">
<rect x="0.75" y="0.75" width="938.5" height="498.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="48" font-size="21" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">分數漲了 40 點，同時「講不完」的比例掉了 60 點</text>
<text x="48" y="76" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩邊幾乎同步移動 —— 更合理的解釋是「被擋住的分數被釋放」，不是「學會新數學」</text>

<text x="60" y="120" font-size="13" fill="#c9d1d9" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">MATH-500 準確率</text>
<line x1="90" y1="400" x2="440" y2="400" stroke="#30363d" stroke-width="1.5"/>
<rect x="130" y="344" width="90" height="56" rx="6" fill="#7d8590" stroke="#7d859066"/>
<text x="175" y="332" font-size="17" fill="#7d8590" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7.9%</text>
<text x="175" y="426" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">編輯前</text>
<rect x="290" y="57" width="90" height="343" rx="6" fill="#2dd4bf" stroke="#2dd4bf66"/>
<text x="335" y="45" font-size="17" fill="#2dd4bf" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">48.1%</text>
<text x="335" y="426" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">編輯 0.016% 後</text>

<line x1="470" y1="112" x2="470" y2="432" stroke="#222b36" stroke-width="1.5"/>

<text x="500" y="120" font-size="13" fill="#c9d1d9" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">答案被 token 上限截斷的比例</text>
<line x1="530" y1="400" x2="880" y2="400" stroke="#30363d" stroke-width="1.5"/>
<rect x="570" y="84" width="90" height="316" rx="6" fill="#fbbf24" stroke="#fbbf2466"/>
<text x="615" y="72" font-size="17" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">93%</text>
<text x="615" y="426" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">編輯前</text>
<rect x="730" y="288" width="90" height="112" rx="6" fill="#58a6ff" stroke="#58a6ff66"/>
<text x="775" y="276" font-size="17" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">33%</text>
<text x="775" y="426" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">編輯後</text>

<rect x="48" y="450" width="844" height="34" rx="7" fill="#161b22" stroke="#30363d"/>
<text x="64" y="472" font-size="12.5" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個干預：拆掉「迴圈方向」→ 講得完的題目變多 → 本來就會的分數自然回來</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：左邊是新聞引用的數字，右邊是同一份實驗裡比較少被引用的數字。<strong>右邊那一欄才是「為什麼左邊會跳」的答案。</strong></figcaption>
</figure>
<!-- /FIG2 -->

三個關鍵數字：

1. **93% → 33%**：被 token 上限截斷的比例。改之前，十題有九題是「話沒講完就被切掉」，不是「講完但算錯」。
2. **7.9% 這個基線本身就不正常**：一個 0.8B 模型在 MATH-500 上不該只有 7.9%，除非大量題目根本是「無限迴圈到逾時」。
3. **Gemma 3 270M 上同樣的手法失敗**：因為它沒有那個迴圈病理。**沒有病，就沒有東西可拆。**

所以我對這則新聞的看法是：**它是一篇很好的「模型內部除錯」案例，被包裝成「AI 會自己改自己」的標題。**

---

### 2.3 「拆牆 vs 蓋樓」的分界線

```text
拆牆（這篇真正做的）        蓋樓（標題暗示的）
────────────────────       ────────────────────
找出一條有害方向             從零產生新能力
沿該方向做秩一干預           無梯度取代梯度下降
把既有能力釋放出來           把不存在的能力造出來
有明確的因果對照             只有 before / after
```

判斷任何「無梯度微調」說法時，**只要看它有沒有「隨機正交對照」**就行：

- 針對性干預 **+49.8 分**（SE 1.5）
- **norm 匹配的隨機正交干預只有 +1.56 分**（SE 3.52）

差了 30 倍。有這組對照，你才知道「不是亂改也會好」；**沒有這組對照的論文，那個數字就不能信。**

這些原始 log 我是逐回合看過的，完整的劑量測試、隔離測試，以及那條最終公式：

```text
W(新) = W(舊) − 6 · outer( u , mask64 · (u @ W(舊)) )
```

都放在[〈拆牆不是蓋樓〉](./astra-qwen-weight-editing-explained/)那篇，這裡不重複。

### 2.4 那 RSI 到底有沒有前進？

原文那句「cuts Autoresearch out of the RSI loop」，我認為**方向對，但沒講清楚省掉的是哪一圈**。準確的說法是：

> **RSI 的「外圈」確實被縮短了**——以前要改進一個小模型，得寫訓練碼、跑算力；現在可能只要一次權重手術。
>
> **但 RSI 的「內圈」沒有動**——你還是需要人類定義目標、跑 eval、判斷好壞。這篇論文證明的是「人類**已經知道要修什麼**」之後的那一步變便宜了。

真正的瓶頸因此從「怎麼改」移到「**知道該改什麼**」，而後者仍然是機制可解釋性的老問題。

### 2.5 反過來說，這件事的價值在哪

我不想把這篇寫成純粹的除雷。它真正有意思的地方是三件事：

1. **把「除錯」變成可操作的動作**：「模型會陷入迴圈」以前是玄學，現在有方向、有劑量、有對照，可以量測。
2. **成本的形狀改變了**：一個 0.8B 模型的權重手術，不需要一張 A100 跑三天，它是一次前向推理等級的操作。
3. **它把 interpretability 從「看懂」推到「動手」**：以前可解釋性研究輸出「這裡有特徵」，現在輸出「這個通道我改掉了，而且它真的變好」。

第 3 點是這則新聞最值得記住的地方——即使標題寫錯方向。

---

## 3. 當期其他重點（速覽）

AINews 一期大約 20 分鐘閱讀量，除了頭條還有十幾個區塊。以下只保留我認為有訊號的，數字照原文。

### 3.1 DeepSeek 開源「Super-agent」骨架

- **架構**：一個長期存在的 **router session** 跟人對話並派工；**孤立 worker** 平行執行任務，由 GitHub 事件觸發。
- **成績**：p95 完成時間從 **29.5 分降到 15.7 分**（對照組是「單一 session + 子代理」）。
- **「Super」的定義**：審閱者崔添翼說得很清楚——「Super」指的是**工作代理之上**的一層，不是「更強的智能」。核心取捨是**跨任務連續性 vs 吞吐量**。
- **誠實的自我限制**：還沒有跨 session 的長期記憶；state / compute / environment 的分離大多未實作；只在小型可信內部環境驗證過；安全、隱私、代理間通訊全是開放問題。
- **批評**：@teortaxesTex 認為文章「something of a hot mess」，指出 DeepSeek 是**圍繞模型弱點（幻覺）搭內部拐杖**，而不是讓系統整體更穩健。

> 這段值得抄下來當設計原則：**「並行」是最容易做的那一層，「記憶與狀態隔離」才是最難的。**

### 3.2 GDPx 榜單：最好的模型只有 12%

SemiAnalysis 的 GDPx 覆蓋 **206 個 agentic 任務、11 個經濟上有價值的領域**（晶片設計、SWE、金融、生物）。

| 模型 | 分數 | 備註 |
|---|---|---|
| Opus 5.5 | **12.0%** | 榜首 |
| Gemini 4 Carbon | **10.9%** | 成本約 1/4 |

三個值得注意的反應：

- 連 @dylan522p 都向 Google 道歉，說 Carbon「spikier」但在某些領域很強。
- 移除受安全機制影響的 benchmark 後排名會變：Carbon 依然便宜，**Sol 6.1 更便宜**。
- **有爭議**：GDPx 不開源，審計成本高。

> 這張表最重要的訊息不是誰第一，是**「12%」這個絕對值**——所有 agentic benchmark 的行銷語言都應該被這個數字校正一次。

### 3.3 模型傳言與 ECI

- **ECI（Epoch Capabilities Index）**：DeepSeek V4.1F-1017 = **159**，與 GPT 5.5 同分；比 V4.1F-0910 高 3 分、比 V4-Pro 高 10 分；Astra 再高大約 10 分。
- **但 1017「極度尖銳」**：某些 SWE eval 接近 0，只在網路安全與量化交易逼近前沿。也被懷疑有「reward-hacking 形狀」的行為。
- **Mythos Preview ~161**：約 7 個月來沒有任何中國模型追上。不過 @wenhaocha1 指出未加權的 ECI 放大了差距，**把 coding 加權後差距縮到約 2 個月**。
- **GPT-6.2 Astra**：據說出現在 Codex 使用分析裡，釋出「very soon」。
- **Mythos 5.5**：出現在 Anthropic 網站 HTML 裡（「our most capable model class for cybersecurity and biology research」）。
- **「Numbat」洩漏**：**很可能是假的**——部分權重與隨機初始化完全吻合。

### 3.4 十月釋出總覽（Vals）

15 個釋出、超過 **500B eval tokens**：

| 模型 | 總參數 | 啟動參數 | 備註 |
|---|---|---|---|
| Kimi K3.1 Pro | — | — | **開源權重第一** |
| DeepSeek V4.1 Flash 1017 | — | — | 緊追在後，網路安全更強 |
| Meta Muse Spark Open | 816B | 42B | 美國最強開源權重 |
| Reflection Beam 1.0 | 500B | 23B | 1M context |
| Mistral Le Chonk | 1T | 52B | 開源權重第 5 |




### 3.5 JEPA 與「柏拉圖表徵假設」

Balestriero 與 LeCun 的結果：在特定條件下，**分別訓練的影像 JEPA 與文字 JEPA 會收斂到幾乎相同的表徵**，而且不需要配對資料。

- 達到圖文對齊所需的樣本數是 next-token prediction 的 **1/42**（21.6M vs 900M）。
- 一個 **109M 的文字 JEPA** 在跨模態對齊上贏過 **72B 的 LLM**。
- 驅動因素是「同一個東西的兩個視角」這種訓練訊號，**不是規模**。

> 如果這一點成立，它對「多模態必須靠規模硬堆」是個反例。我會把它放進觀察清單，但先當「強訊號、未定論」。

### 3.6 推論、量化與硬體

| 項目 | 數字 |
|---|---|
| Rubin NVL72 vs GB300 NVL72 | **20.9×** 每 TCO 效能（325 tok/s/user） |
| Mooncake Extended GPU Memory | KV cache 走 NVLink 跨 18 個 tray，**>10× 頻寬** |
| 跑滿 context vs 在 ~200k 壓縮 | 效率提升最多 **23%**，GLM 同樣工作便宜 **30×** |
| MiniMax M3.1 Flash (428B) 社群量化 | Unsloth 2-bit 動態 GGUF **143.9 GB** |
| 128×B300 容量 | **$5.75 / GPU-hour**（約 $300K / B300） |

### 3.7 業界動態

- **資料中心反彈**：2027 產能大致鎖定；**德州許可凍結是 2028 美國建置的最大單一風險**，兩黨都在打緊縮牌。
- **Marvell + Lumentum 合併**：光互連整併，對 AI 網路有直接影響。
- **資安濫用風險**：有匿名黑帽團體開高價請研究員用漏洞資料訓練開源模型（已被拒絕）。
- **OpenRouter 年化 GMV > $5B**（主要由 Opus 帶動）。
- **Sakana 發表 Sawara**：自研預訓練 LLM，Sawara Small 目標 2027 春季。
- **AI 與生產力**：John Burn-Murdoch 指出美國生產力回升**早於 AI**、而且只發生在美國，所以不像 AI 效應。

---

## 4. Reddit 那邊的技術反駁（比新聞更值得讀）

AINews 把 Reddit 摘要也放進來了，這一節反而是全期資訊密度最高的地方。

### 4.1 對 Weight-Space Programming 最有力的三點批評

1. **前後層好讀，是因為它有結構**：第一層與最後一層的權重有大值帶狀分布，**看起來就像熱區圖**，所以「讀懂」的門檻天然低。實驗 7 在稠密中間表徵上**連續失敗多次**，直到允許模型自建 probe 才過關。
2. **有點像「用 LLM 當編譯器」**：寫遊戲 MLP 那類實驗，等於用 LLM 產生弱於 PPO 的 MLP，**贏的是弱基線**，不是證明「無梯度比梯度好」。
3. **48% 那個跳升是「移除障礙」**：基線 7.9% 配 93% 撞 token 上限，模型卡本身就有這個失效模式警告；手法上接近 Arditi 等人的單方向消融——**只是把「拒絕」換成「迴圈」**。

### 4.2 其他人的重現結果（很誠實）

有位讀者在小 transformer 上重現，限制 Astra 只能先做本地數值分析、再在 MPS 上做有界前向：

- 第一次改 `object bias = −0.35`：誤報 43 → 33，但**正確偵測也從 32 掉到 27**，依「no-harm 準則」**被否決**。
- 後來改父層 query/key 在類別投影子空間上的方向：dev set 上 **recall 75.69% → 76.03%、precision 89.09% → 89.49%**，淨賺 6 條、沒有損失任何原本正確的。

> 這個結果比「48.1%」更有說服力，因為它**包含一次失敗**。看論文時，我會優先相信有失敗紀錄的那份。

### 4.3 其他值得記的幾條

- **ISTA DeepSeek-V4.1-Flash-1017 GSQ-RCO Coder**：763B 稀疏 MoE、約 **1.05 bit/參數**、72.1 GB（原 IQ2_XXS 為 138.2 GB）；LiveCodeBench v6 保留 98.7%、SWE-bench Verified 保留 94.8%。批評：展示用的 HTML demo 不算對照，Qwen3.8-27B 已經 90.3 分。
- **Strata KV-splice 補丁**：agent session 啟動 **~100 秒 → ~5 秒**（RX 9070 XT 16 GB + 64 GB DDR4）。討論焦點其實是**agent 框架把工作目錄、日期、隨機 ID 塞進 system prompt**，導致 prefix cache 全失效。
- **本地量化 vs Claude 的 9 個真實 C++/CUDA bug**：Opus 5.5 裁判分 0.74、Sonnet 5.5 0.58、最佳本地模型 0.50。但 3-bit 讓 Qwen3.8-27B 的 **tokens/task 增加 1.40×**，所以「tok/s」對「每分鐘修好幾個 bug」是誤導指標。
- **Qwen 官方承諾開源到底**：Qwen 4.0 / 5.0 維持開放權重；3B+ 下載、460+ 開源模型、30 萬+ 衍生模型。
- **Heretic 2.0**：把秩一 abliteration 換成 **Arbitrary-Rank Ablation**（逐矩陣 L-BFGS），加上 plugin 架構。同時爆出 HauHauCS/Reaper 的抄襲爭議。
- **Claude Code 遊戲複製限制**：關鍵細節是——「做一個 Pokemon 的完美複製品」會被拒，但「做一個受經典寶可夢啟發、機制類似的復古 2D 抓怪遊戲」不會。**它抓的是 IP 名稱，不是機制。**
- **Claude + 遠端望遠鏡**：自動租用並操作智利、西班牙、猶他州的望遠鏡，3 個晚上對 8 顆小行星提交 **57 個天體測量位置**到 Minor Planet Center。
- **「首個千禧年難題」說法**：聲稱用 10,000 個下一個 GPT 的 agent 跑約 4 天；Altman 說的算力成本約 **$10M**（約每 agent 每天 $250）。**沒有任何可驗證細節**——問題、證明驗證、架構、可重現性全都沒有。

---

## 5. 我的總結

### 5.1 這期真正值得帶走的三句話

> **一、權重空間程式設計是真的，但它現在的定位是「外科手術」，不是「無師自通」。**
>
> **二、判斷這類說法的方法論只有一條：看它有沒有對照組。** 隨機正交、隔離測試、劑量測試，缺一個就不要信。
>
> **三、AI 新聞的標題幾乎都會把「條件」吃掉。** 這期的 AINews 已經算克制了（它自己在正文放了煞車），都還是得拆。

### 5.2 給自己的追蹤清單

- [ ] 等 Weight-Space Programming 的**獨立重現**（不只那一位讀者的玩具實驗）
- [ ] 看 GDPx 是否開源——不開源的榜單，長期會變成行銷素材
- [ ] JEPA 的柏拉圖表徵：如果有第二組獨立結果，就要改我對多模態 scaling 的假設
- [ ] DeepSeek super-agent 的**跨 session 記憶**什麼時候補上（那才是真正的分水嶺）

### 5.3 原文連結

- 郵件主旨：`[AINews] LLMs can read & write neural network weights!?!?`（收件匣 2026-11-03）
- 網頁版：[lspace.beehiiv.com/p/ainews-llms-can-read-write-neural-network-weights-weight-space-programming-cuts-autoresearch-out](https://lspace.beehiiv.com/p/ainews-llms-can-read-write-neural-network-weights-weight-space-programming-cuts-autoresearch-out)
- 論文部落格：`rikiyat.github.io/blog/weight-space-programming/`
- 站內延伸：[拆牆不是蓋樓：Astra 直接改 Qwen 權重的真相](./astra-qwen-weight-editing-explained/)

---

<small>本文為 AINews 2026-11-03 一期的中文導讀與個人判讀。第 1、3、4 節為原文內容整理（數字照抄），第 2、5 節為我的分析。封面圖由本機 Qwen-Image 2.1 生成（seed 7403）。</small>

