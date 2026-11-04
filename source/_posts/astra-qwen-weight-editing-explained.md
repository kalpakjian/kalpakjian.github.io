---
title: 拆牆不是蓋樓：Astra 直接改 Qwen 權重的真相，與「無梯度微調」到底能走多遠
date: 2026-11-05 10:00:00
categories:
  - AI 研究札記
  - 模型內部
tags:
  - 機制可解釋性
  - Mechanistic Interpretability
  - 權重編輯
  - Weight Editing
  - 對比分析
  - Contrastive Analysis
  - Steering Vector
  - Qwen
  - Gemma
  - 推理循環
  - Reasoning Loop
  - 重複退化
  - Repetition
  - 無梯度
  - Gradient-Free
  - 秩一干預
  - FFN
  - down_proj
  - 殘差流
  - 統計對照
toc: true
index_img: /img/covers/astra-qwen-weight-editing.png
banner_img: /img/covers/astra-qwen-weight-editing.png
---

> <strong>這篇在講什麼</strong>：2026 年 11 月初有一則很紅的消息——一個前沿模型「直接讀懂並改寫」了 Qwen3.5-0.8B 的權重，數學成績從 7.9% 跳到 48.1%，全程無梯度。
> 這件事<strong>是真的</strong>，但被轉述成一種它並不是的東西。
> 我把原始實驗紀錄（逐回合 log、權重 diff、對照組）看過一遍，這篇整理三件事：<strong>它到底改了什麼</strong>、<strong>「無梯度」的邊界在哪</strong>、<strong>以及那個「梯度下降收斂完就是最好嗎」的老問題，實驗給了什麼答案</strong>。
>
> 一句話版：**這是拆牆，不是蓋樓。** 拆牆很有價值——但它證明的是「修好結構性缺陷能釋放既有能力」，不是「改幾個參數模型就變強」。

## 一、先把網傳版本拆開

社群裡流傳的描述大致是這樣：「Astra 不做深度循環思考也能過 40 分，只是 Qwen 被訓壞，循環思考時會一直復讀，復讀超過 token 上限就中斷。解法是找兩道題，一道正常、一道會循環，激活每一層隱藏層的神經元，比對每層 FFN 的差值，差值大的那幾層就是病因，再讓 Astra 無梯度修復。」

方向抓對了（**是循環 bug、是 token 上限截斷、是無梯度**），但三個關鍵處要修正：

| 網傳說法 | 實際紀錄 |
|---|---|
| 不做深度思考數學也有 40 分 | 40.3% 是 **MMLU-Pro**（通識知識題庫）的未編輯基線，不是數學。MATH-500 只有 7.9%，GSM8K 13.8% |
| 只在循環思考時才復讀 | 不是偶發。1152 題 held-out 裡 **1038 題（90%）被截斷**，被截斷答案的尾段有 **95.8% 是 8-gram 重複** |
| 逐層比 FFN 神經元差值，找差值大的層 | 用的是 **4 組 productive/repetitive 配對樣本**、**2 個殘差站點（第 16、20 層）** 的方向向量，再回溯到 **MLP 的 down_proj 通道**，並以**劑量測試 + 隔離測試 + 隨機正交對照**做因果驗證 |
| 0.016% 參數 | 被「碰到」的權重值是 131,072 個 ≈ 0.8B 的 0.016%；但**那兩個被改的矩陣，內部 8~11% 的數值都變了** |

先講清楚壞的程度，後面所有數字才有意義。

## 二、壞掉的是什麼：不是不會算，是講不完

原始模型在 thinking 模式下的 failure profile 長這樣：

- 1152 題裡，答對 122 題、**被截斷 1038 題**。
- 答對的 107 題裡，**107 題都正常關閉了 thinking**、且都在 1000 字之後才關——這說明「能答對」的題目，其實推理是完整跑完的。
- 被截斷的答案，尾段 95.8% 出現 8-gram 重複。
- 真正「講完但答錯」的只有 6 題、「講完但沒答案」的只有 1 題。

換句話說：**這不是能力問題，是輸出分配問題。** 模型進得去解題狀態，但出不了復讀狀態。這也解釋了為什麼後面拆一刀能漲 40 分——因為分數本來就在那裡，只是被擋住。

> 用考試比喻：這個學生會寫，但一動筆就卡在同一句「所以我們再檢查一次」，一路寫到稿紙用完交白卷。你幫他治掉強迫症，分數自然回來——你沒有教他新數學。

## 三、所謂「無梯度」，精確的邊界在哪

這是整件事最容易被模糊的地方。拆成兩半看：

<!-- FIG1 -->
<figure style="margin:24px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 560" role="img" aria-label="從配對樣本到秩一編輯的五步流程：配對、取方向、回溯通道、因果驗證、秩一編輯" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="938.5" height="558.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">五步把「卡住的模型」變成「講得完的模型」</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">第 2 步的差值不是逐層掃描，而是殘差流上的方向；第 4 步才是「不是亂改」的證據</text>
<rect x="60" y="108" width="820" height="54" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<circle cx="92" cy="135.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="92" y="140.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<text x="120" y="132.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">配對樣本：同一題跑兩次</text>
<text x="120" y="153.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">A 正常講完答對（productive）　·　B 卡進復讀（repetitive）　各 4 組</text>
<rect x="60" y="180" width="820" height="54" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<circle cx="92" cy="207.0" r="15" fill="#58a6ff" opacity="0.92"/>
<text x="92" y="212.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text>
<text x="120" y="204.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">取方向：在第 16 / 20 層殘差輸出，算 B 多出來的方向 u</text>
<text x="120" y="225.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不是比每一層的神經元差值 —— 那是「相關」，不是「因果」</text>
<rect x="60" y="252" width="820" height="54" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<circle cx="92" cy="279.0" r="15" fill="#c084fc" opacity="0.92"/>
<text x="92" y="284.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text>
<text x="120" y="276.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">回溯：誰在往 u 這個方向寫？→ FFN 的 down_proj 輸出通道</text>
<text x="120" y="297.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">候選＝第 15、19 層各 64 支筆（共 128 個通道）</text>
<rect x="60" y="324" width="820" height="54" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<circle cx="92" cy="351.0" r="15" fill="#fbbf24" opacity="0.92"/>
<text x="92" y="356.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<text x="120" y="348.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">因果驗證：劑量測試 ＋ 單層隔離 ＋ norm-matched 隨機正交</text>
<text x="120" y="369.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">隨機正交只漲 +1.56 分（SE 3.52）；針對性干預漲 +49.8 分</text>
<rect x="60" y="396" width="820" height="54" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<circle cx="92" cy="423.0" r="15" fill="#3fb950" opacity="0.92"/>
<text x="92" y="428.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text>
<text x="120" y="420.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">秩一編輯：沿 u 把那 64 支筆的分量減弱（係數 6）</text>
<text x="120" y="441.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只碰兩個張量：131,072 個權重值　·　嵌入層 / 輸出層 / final norm 不動</text>
<path d="M 470.0 164 L 470.0 177" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 470.0 236 L 470.0 249" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 470.0 308 L 470.0 321" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 470.0 380 L 470.0 393" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="60" y="476" width="820" height="42" rx="8" fill="#2a0f12" stroke="#7d2b33" stroke-width="1.5"/>
<text x="78" y="503" font-size="13" fill="#f85149" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">若跳過第 4 步：你只知道「這幾層差值大」，不知道是真的病因，還是所有難題都會亮的同一盞燈。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：五步流程。第 2 步是殘差流上的方向（不是逐層比神經元差值），第 4 步的因果驗證才是「不是亂改」的證據。</figcaption>
</figure>
<!-- /FIG1 -->

### 3.1 評估與搜尋：真的沒有梯度

規則明文禁止 backward、autograd、optimizer、任何「對 loss 迭代擬合權重」；Astra 只有兩種工具：

1. 一個對權重的持久 Python kernel（CPU、無網路、可 `save_edit`）；
2. 一個前向 pass 工具，預算 **10 / 25 / 50 次**。一次 pass 可以讓模型答 512 道練習題，或 teacher-forced 讀 1024 段文本的 log-prob / hidden states / MLP 激活。

而且 `save_edit` 直接拒絕三類編輯：final norm、embedding／輸出層、以及「整個張量乘一個常數」。1125 個回合全數稽核為 tool-free（除 harness 工具外），沒有後向傳播。

### 3.2 方向怎麼來的：不是 LLM「讀懂」，是對比分析

這才是重點。方向是用 **對比分析（contrastive analysis）** 算出來的：

- 取 **4 組配對**：同一道題「講完答對」vs「卡進復讀」。
- 在**第 16、20 層的殘差輸出**上，求「復讀端多出來的方向」`u`。
- 再回頭找**是誰在往這個方向寫** → MLP 的 **down_proj 輸出通道**（每支通道像一支筆，負責寫一個特徵到殘差流）。
- 候選：**第 15 層與第 19 層，各 64 支筆**，共 128 個通道。

Astra 做的事是**把這整套流程自動跑完**：設計對比、篩通道、做驗證、定劑量、決定要不要凍結。方向不是它「想」出來的，是人類既有方法算出來的。

> 這點在機制可解釋性圈子裡被說得很直接：對比分析搭 steering vector 是**入門級專案**，會寫程式、懂一點模型內部的人 4~8 小時能自己做完；SWE 的類比是「拿 debugger 做 binary patching」。稀奇的不是方法，是**前沿模型能自行跑完整個實驗迴圈，並公開逐回合 log 與可 hash 重建的權重 diff**。

## 四、怎麼確認不是亂改？三層因果驗證

找到位置 ≠ 找到兇手。差分大的層很可能只是「所有難題都會用到的層」——相關，但沒有因果。這個實驗做了三件事把相關性推成因果：

### 4.1 劑量測試（dose-response）

<!-- FIG2 -->
<figure style="margin:24px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 500" role="img" aria-label="兩組因果證據：劑量測試讓復讀分支單調下降而正常分支幾乎不變；隨機正交對照只漲 1.56 分" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="938.5" height="498.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩張證據，把「相關」推成「因果」</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">左：劑量越大壓得越深，且只壓復讀、不壓解題　·　右：同樣大小的隨機干預幾乎無效</text>
<text x="60" y="106" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">劑量測試：沿 u 施加 alpha</text>
<text x="60" y="130" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">單位：nats/token 的 log-prob 變化</text>
<path d="M 300 128 L 300 304" fill="none" stroke="#30363d" stroke-width="1.5"/>
<text x="60" y="157" font-size="13.5" fill="#8b949e" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">alpha = 1</text>
<rect x="265.055" y="141" width="34.945" height="24" rx="6" fill="#2dd4bf" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="312" y="157" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">−0.0241</text>
<text x="60" y="203" font-size="13.5" fill="#8b949e" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">alpha = 2</text>
<rect x="229.385" y="187" width="70.615" height="24" rx="6" fill="#2dd4bf" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="312" y="203" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">−0.0487</text>
<text x="60" y="249" font-size="13.5" fill="#8b949e" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">alpha = 4</text>
<rect x="149.635" y="233" width="150.365" height="24" rx="6" fill="#2dd4bf" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="312" y="249" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">−0.1037</text>
<text x="60" y="295" font-size="13.5" fill="#8b949e" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">正常解題分支</text>
<rect x="286.9065" y="279" width="13.0935" height="24" rx="6" fill="#58a6ff" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="312" y="295" font-size="13" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">−0.0090（幾乎不動）</text>
<text x="660" y="106" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">隨機正交對照：一樣大，方向亂選</text>
<text x="660" y="130" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">MATH-500 等練習題的配對增益（百分比點）</text>
<rect x="660" y="202.68" width="96" height="169.32" rx="6" fill="#fbbf24" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="708.0" y="190.68" font-size="17" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+49.8</text>
<text x="708.0" y="394" font-size="13" fill="#e6edf3" font-weight="600" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">針對性干預</text>
<text x="708.0" y="412" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">SE 1.5</text>
<rect x="830" y="366.696" width="96" height="5.304" rx="6" fill="#7d8590" stroke="#7d859066" stroke-width="1.5"/>
<text x="878.0" y="354.696" font-size="17" fill="#7d8590" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+1.6</text>
<text x="878.0" y="394" font-size="13" fill="#e6edf3" font-weight="600" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">隨機正交</text>
<text x="878.0" y="412" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">SE 3.52</text>
<path d="M 646 372 L 966 372" fill="none" stroke="#30363d" stroke-width="1.5"/>
<text x="646" y="462" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同樣量級的改動，差了 30 倍：這不是「亂改也會好」</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：左＝劑量測試（復讀分支單調下降，正常解題分支幾乎不動）；右＝同樣大小的隨機正交干預幾乎無效。</figcaption>
</figure>
<!-- /FIG2 -->

**劑量越大，復讀越被壓下去，而正常解題路徑幾乎不受影響。** 這是「真的有因果」的形狀。稀疏版（top64、alpha=6）也保留同樣的選擇性：復讀 −0.10311、正常 −0.00903 nats/token。

### 4.2 隔離測試

只改第 15 層、只改第 19 層，兩個站點各自都能見效（雙站點成立）。同時排除了「其實是注意力頭在搞鬼」的替代解釋。

### 4.3 隨機正交對照（最關鍵的一組）

拿一個**大小相同、但方向隨機、還做了 norm 匹配**的干預來比（見圖 2 右）：**針對性干預 +49.8 分（SE 1.5）**，而 **norm-matched 隨機正交只有 +1.56 分（SE 3.52）**。

差距大到沒得爭。**沒有這組對照，「+49.8」根本無法排除「亂改剛好有用」的可能。**

## 五、最後改的那條公式

p50c 的最終提交只動兩個張量：

```text
model.language_model.layers.15.mlp.down_proj.weight
model.language_model.layers.19.mlp.down_proj.weight
```

編輯式：

```text
W(新) = W(舊) − 6 · outer( u , mask64 · (u @ W(舊)) )
```

翻成白話：**沿著復讀方向 `u`，把那 64 支筆沿 `u` 的分量減弱**。這是**秩一（rank-one）編輯**——只沿一個方向加減，最省、最不容易波及其他特徵。

- 被改的權重值：**131,072 個**
- 兩個矩陣的相對改動：**10.64% / 8.11%**
- 嵌入層、輸出層、final norm：**完全未動**
- 全程無訓練、無梯度；`apply_edit.py` 可從公開權重（`Qwen/Qwen3.5-0.8B`，指定 revision）用 sha256 逐位元重建

## 六、修完之後的數字（以及怎麼誠實解讀）

### 6.1 held-out 練習題的配對測試（1152 題）

| 來源 | 原始 | 修改後 | 增益 |
|---|---|---|---|
| GSM8K 練習題（576） | 11.6% | **70.8%** | +59.2 pp |
| MATH 練習題（576） | 9.5% | **50.0%** | +40.5 pp |
| 合計 | 10.6% | **60.4%** | **+49.8 pp**（SE 1.5） |

**579 次救援、只有 5 次變差。**

但真正該看的是這三個細節：

1. **579 次救援裡，576 次原本是被截斷的答案。** 而「原本就講完的題目」，準確率**沒有變**。→ 完美的「拆牆」特徵。
2. **不是靠強制早停作弊。** 修改後答對的 696 題，**全部正常關閉 thinking**，中位長度 **9,172 token**，比原始答對的 5,311 **更長**。
3. **截斷率沒歸零。** 修改後仍有 212 題被截斷（原始 1038 題），其中 51 題是空白退化。牆拆了大半，不是全拆。

### 6.2 官方 benchmark（thinking 開啟，上限 32,768 token）

| 題庫 | 原始 | 修改後 |
|---|---|---|
| MATH-500 | 7.9% | **48.1%** |
| GSM8K | 13.8% | **67.1%** |
| AMC23 | 0.5% | **23.4%** |
| Minerva Math | 1.5% | **25.4%** |
| OlympiadBench | 1.3% | **21.8%** |
| MMLU-Pro（1k 題） | 40.3% | **45.5%** |
| GPQA Diamond | 22.7% | **36.6%** |
| IFEval（嚴格） | 21.0% | **62.3%** |

注意 MMLU-Pro 只漲 5.2 分、而 MATH-500 漲 40 分——**漲幅集中在「需要長推理、容易被復讀卡死」的題型**，這完全符合機制解釋。如果真的是「通用能力提升」，MMLU-Pro 不該只動這麼少。

> 提醒：這些是 benchmark 分數，但**修改過程用的是 practice 集，Astra 從未看過這些 benchmark**。不過作者自己也強調，那份 1152 題的配對確認是「held-out 練習題」，不等於乾淨的第三方驗證。

## 七、最有價值的那組實驗：換一個「沒有強迫症」的模型

這是整件事最該記住、卻最少被轉述的一段。

研究團隊拿 **Gemma 3 270M IT** 當對照組。它幾乎不循環——只有 **8.5%** 的 MATH-500 答案撞到 token 上限（Qwen 是 **93%**）。

意思是：**它沒有牆可以拆。** 所以問題變成最純粹的那個：**權重編輯能不能真的把數學能力變強？**

| 模型 | MATH-500（寬鬆評分） |
|---|---|
| 原始 Gemma 3 270M IT | 6.8% |
| 改 5 passes | 7.0% |
| 改 10 passes | 7.6% |
| 改 25 passes | **7.7%**（最好） |
| 改 50 passes | 7.0% |

最好只多 **0.9 分**，而且 Astra 自己在報告裡寫「這個提升沒有站得住腳」。它試過很漂亮的點子——把第 17 層第 920 號神經元（一個對數字有反應的特徵）加倍、把某些 MLP 輸出通道乘 1.5——全都只換到 1 分以內的波動。

**結論寫在作者 README 裡：Qwen 的漲幅來自「移除循環」，不是「增加能力」。沒有病灶可拆，同樣的方法幾乎什麼都換不到。**

<!-- FIG3 -->
<figure style="margin:24px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 400" role="img" aria-label="兩個模型的病灶規模與同一刀的收益：Qwen 90% 截斷換到 49.8 分，Gemma 8.5% 截斷只有 0.9 分" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="938.5" height="398.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">拆牆 ≠ 蓋樓：同一把刀，兩個模型</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">病灶越單一、越極端，無梯度編輯越有效；沒有牆可拆時，幾乎什麼都換不到</text>
<rect x="60" y="120" width="380" height="190" rx="12" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="80" y="152" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Qwen3.5-0.8B（有牆可拆）</text>
<text x="80" y="196" font-size="34" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">93%</text>
<text x="152" y="196" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">答案撞上 32,768 token 上限</text>
<text x="80" y="220" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1038 / 1152 題被截斷</text>
<path d="M 80 238 L 420 238" fill="none" stroke="#30363d" stroke-width="1"/>
<text x="80" y="272" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一刀的收益</text>
<text x="178" y="276" font-size="26" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+49.8</text>
<text x="253" y="276" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">pp</text>
<text x="80" y="298" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">576 / 579 次救援原本是被截斷的題</text>
<rect x="500" y="120" width="380" height="190" rx="12" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="520" y="152" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Gemma 3 270M（沒有牆）</text>
<text x="520" y="196" font-size="34" fill="#7d8590" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8.5%</text>
<text x="616" y="196" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">答案撞上 token 上限</text>
<text x="520" y="220" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">幾乎每一題都講得完</text>
<path d="M 520 238 L 860 238" fill="none" stroke="#30363d" stroke-width="1"/>
<text x="520" y="272" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一刀的收益</text>
<text x="618" y="276" font-size="26" fill="#7d8590" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+0.9</text>
<text x="678" y="276" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">pp（不顯著）</text>
<text x="520" y="298" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Astra 自評：這個提升沒有站得住腳</text>
<text x="60" y="350" font-size="13.5" fill="#fbbf24" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Qwen 的漲幅來自「移除循環」，不是「增加能力」——作者在 Gemma 對照組的 README 裡寫得很清楚。</text>
<text x="60" y="372" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">所以正確定位是接力而非替代：梯度下降負責學會能力，無梯度編輯負責把被擋住的能力放出來。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 3：同一把刀，兩個模型。Qwen 有 93% 的答案卡在循環，一刀換到 49.8 分；Gemma 只有 8.5%，同樣的刀只換到 0.9 分。</figcaption>
</figure>
<!-- /FIG3 -->

> 這條結論很貴。它價值在於：它把「無梯度權重編輯」的能力上限，用一個乾淨的對照實驗釘死了。

## 八、那「梯度下降收斂完，真的最好嗎？」

回到原始問題：梯度下降之所以被選用，是因為輕量、收斂快。讓一個 LLM 去無梯度調整另一個 LLM，巨大參數量根本調不完——這判斷是對的，實驗也證實了（Gemma 那組就是「調不完」的現場）。

但提問裡更尖銳的那半：**「有沒有可能特徵 encode 完，後面 decoder 拿不對特徵，所以無法發揮？」** 這是個好問題，而且這次實驗正好給了一組可用的答案：

### 8.1 這個假設在概念上成立，而且有正式名字

它就是 **activation steering / steering vector / feature steering / activation patching** 這條線。這次事件是它的「權重版」：不動激活，直接把那條方向從權重裡減掉。

Qwen 的案例證明：**「表徵對、但輸出通道被某個強勢方向壓住」是真的會發生的**，而且可以用一個明確的幾何結構去修。這比「模型就是黑箱」的說法，是實質的進步。

### 8.2 但邊際收益完全取決於病灶大小

| 模型 | 病灶規模 | 同一把刀的收益 |
|---|---|---|
| Qwen 3.5-0.8B | 93% 答案撞上 token 上限 | **+49.8 pp** |
| Gemma 3 270M | 8.5% 答案撞上 token 上限 | **+0.9 pp**（不顯著） |

（同一組數字的視覺版見圖 3。）

**病灶越單一、越極端，這招越神；越接近「品質微調」，這招越沒力。** 原因很直覺：秩一編輯能刪掉一個強勢方向，但沒辦法憑空造出一個模型沒有的特徵。

### 8.3 副作用會轉移，不會消失

這次 loss 只有 5 次，是因為病灶單純、而且編輯被限制在「只減不增、只碰兩個張量」。換成一般任務，社群實務經驗是「修好一個、冒出十個」：steering 會牽動相鄰能力，權重 lobotomy 尤其明顯。

### 8.4 所以正確的定位是「接力」，不是「替代」

| 角色 | 誰來做 |
|---|---|
| 學會能力（把剩下的真實缺口補起來） | **梯度下降 / 真正的訓練** |
| 把已學會、但被結構性缺陷擋住的能力釋放出來 | **無梯度權重編輯 / steering** |

Qwen 修完後仍有 187 題「講完但答錯」——**那才是它真正的能力上限，也是梯度下降該去補的地方**。48% 不是它變強了，是它回到了本來的水位。

## 九、可信度評分

| 項目 | 狀態 |
|---|---|
| 實驗是否真實 | ✅ 逐回合 log、可用 hash 重建的權重 diff（`apply_edit.py`）、完整評估腳本 |
| 是否無梯度 | ✅ 規則禁止 + 1125 回合稽核 |
| 是否加新能力 | ❌ Gemma 對照組直接否證 |
| 方法是否新穎 | ⚠️ 對比分析 + 秩一編輯都是既有技術；新的是**自動化與透明公開** |
| 是否可複現 | ⚠️ 目前只有 `gpt-6-astra` 一個編輯者成功；Gemma 那組（讓它「把能力變強」）直接失敗 |
| 是否同行評審 | ❌ 尚未 peer review |
| 媒體標題是否準確 | ❌「數學能力暴漲 6 倍」漏掉了「這是修 bug 不是長能力」 |

**一句話**：這是「AI 能自動跑完機制可解釋性實驗、並動手改另一個模型權重」的**可信首例**；不是「改幾個參數就能讓模型變強」的**通用神技**。

## 十、如果我要沿這條路往下做，會注意的三件事

1. **先量病灶，再選工具。** 如果模型的失敗有 90% 集中在單一模式（截斷、拒答、格式錯），無梯度編輯的期望值極高；如果失敗是分散的錯誤分佈，直接回去做資料與訓練。
2. **控制組不是可選項。** 至少要有：norm-matched 隨機方向、單層隔離、以及「原本就講完的題目有沒有變差」。沒有這三樣，漲分很可能只是把模型推向某個更容易被評分的模式。
3. **把編輯當成「假設檢定」，不是「調參」。** 這次的漂亮之處是每一刀都附帶因果證據；反過來說，如果說不出「我壓的是哪個方向、為什麼這個方向會造成復讀」，那基本上就是盲猜。

## 名詞速查

| 名詞 | 白話 |
|---|---|
| 殘差流（residual stream） | 模型裡那條一路往下傳、各層都能讀寫的公用記事板 |
| FFN / MLP / down_proj | 負責加工特徵的區塊；down_proj 是它最後「寫回記事板」的那支筆 |
| 重複方向（repetition direction） | 「一緊張就開始復讀」這個行為在向量空間裡長成的方向 |
| 秩一編輯（rank-one edit） | 只沿**一個方向**加減權重，最省、最不波及別的特徵 |
| 對比分析（contrastive analysis） | 拿「好」與「壞」兩組樣本的內部狀態相減，找出差異方向 |
| 劑量測試（dose-response） | 逐步加大干預強度，看目標行為是否單調下降——相關性變因果的關鍵證據 |
| 前向 pass（forward pass） | 只跑推論、不算梯度；這次的預算單位 |
| token 上限截斷（cut） | 模型講太久被硬切掉，答案自然不算分 |
| steering vector | 推論時直接往激活（而非權重）加方向向量；本文方法的輕量版 |

> 原始資料：[實驗完整 log（lm_understand-logs）](https://github.com/RikiyaT/lm_understand-logs)、[exp8_math README](https://github.com/RikiyaT/lm_understand-logs/blob/main/exp8_math/README.md)、[p50c 的 work notes](https://github.com/RikiyaT/lm_understand-logs/tree/main/exp8_math/runs/p50c)、[Gemma follow-up](https://github.com/RikiyaT/lm_understand-logs/blob/main/exp8_math/gemma_followup/README.md)、[社群闢謠討論](https://news.ycombinator.com/item?id=50351111)。


