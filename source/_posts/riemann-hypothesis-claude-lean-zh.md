---
title: 黎曼猜想被證了，然後呢？1,700 萬行的證明與 13 個洞
date: 2026-11-25 20:00:00
categories:
  - AI 研究札記
tags:
  - 黎曼猜想
  - Lean
  - 形式化驗證
index_img: /img/covers/riemann-hypothesis-claude-lean-zh.png
banner_img: /img/covers/riemann-hypothesis-claude-lean-zh.png
---

一句話：黎曼猜想這次不是「有人宣稱」，是已經被機器驗到沒得吵了；但「懂」這件事，進度條還停在十三個洞。

> <strong>30 秒結論</strong>：<br />
> 一、驗證程度遠超「初步檢查」：175,187 個模組全部編譯、五個主定理只依賴三個標準公理、61.5 GB 的 proof export 被 Lean 官方 kernel（單執行緒 48 小時）、paranoid kernel 與三個獨立 kernel 接受，其中兩個還附有「相對於集合論不可能接受假證明」的形式化證明。而且證的不只 RH，還包含 Dirichlet L 函數的 GRH。<br />
> 二、「25 萬頁」是作者自己說是玩笑的數字；「1700 萬行」是真的，但它不是「證明的長度」，是編譯產物。<br />
> 三、真正的缺口不是頁數，是 <strong>13 條還沒證的假設</strong>。目前人類版最前線是 Rubinstein 的 265 頁工作草案，它把最難的部分指回 Lean 碼。<br />

## 背景：Lean 與 Mathlib，用蓋房子理解

Lean 是互動式定理證明器（interactive theorem prover），也是一門純函式程式語言。它的核心是一個「什麼都不做、只檢查證明項」的 kernel；tactic 產生的每個證明項都要回到 kernel 再檢查一次，所以<strong>就算 tactic 有 bug，也不會危及整體健全性</strong>。這是它敢被用在數學上的理由。

常見的比喻是這樣：

| 對象 | 類比 |
|---|---|
| 數學定理 | 要蓋的房子 |
| 數學證明 | 施工圖與施工紀錄 |
| Lean | 檢查每一根樑、每一條接縫是否合規的驗收系統 |
| Mathlib | 已驗收、可重複使用的建材庫 |
| AI（Claude） | 協助起草施工圖的助手 |

你只會寫三種東西：定義（質數是什麼、zeta 函數是什麼）、定理（n 為質數則只有 1 與 n 兩個正因數）、證明（一連串 Lean 能檢查的步驟）。一旦 Lean 說成立，任何人在同一套邏輯基礎下都能重跑檢查，不必信任作者的判斷。

Mathlib 是它的共享數學庫：代數、分析、拓撲、機率、電腦科學都有，上百萬行已形式化的內容。你不必從零證明加法、極限、群論或實數的性質，直接引用已驗收的結果。

一個淺白例子。想證「每個偶數都是兩個奇數之和」，人類會寫：設 n 為偶數，則 n = 2k；取 1 與 n−1，兩者皆為奇數，故得證。Lean 會追問：偶數的定義是什麼、奇數的定義是什麼、為何 n−1 是奇數、「取」這個動作是否合法。缺一步就報錯。

但 Lean 不保證三件事：<strong>你形式化的命題與數學家心中的敘述一致</strong>、<strong>證明背後的想法人類看得懂</strong>、<strong>社群已完成傳統的同儕審查</strong>。這次專案對第一點做了特別處理——Mathlib 的 `RiemannHypothesis` 由 Lean 與數論專家審過，再用兩個獨立工具（Comparator、con-leche 的 `--compare`）確認作者證的定理與它逐字相同。至於第二、三點，正是下面第 4、5 節在講的洞。

## 1. 先把「驗過了」講清楚

2026 年 11 月 20 日，Anthropic 的數學家 Levent Alpöge 發佈了一份 Lean 函式庫：175,187 個檔案、約 1,700 萬行，只直接依賴 Mathlib。隔天，Lean FRO 與 Mathlib Initiative 發聯合聲明，用詞是「full confidence」，並列出四條理由：敘述正確、能編譯、證的是對的敘述、證明有效。

這四句話背後的實際動作，比多數報導寫得硬：

| 檢查 | 工具 | 結果 |
|---|---|---|
| 全模組編譯 | Lean / Mathlib v4.33.1 | 175,187 個，0 error |
| 公理稽核 | `#print axioms` | 只有 `propext`、`Classical.choice`、`Quot.sound` |
| 沙盒重編譯 | bubblewrap，無網路、唯讀原始碼 | 導出的 export 與發佈版<strong>逐 byte 相同</strong>（61,570,595,788 bytes） |
| kernel 重播 | leanchecker | 175,187 / 175,187；單執行緒 48 小時，峰值 82.6 GiB |
| paranoid kernel | leanchecker-paranoid | 通過；單執行緒 72 小時 20 分，98.8 GiB |
| 獨立 kernel | nanoda（Rust，另有人重寫） | 接受；80 執行緒 27 分 42 秒 |
| 敘述比對 | Comparator 與 con-leche `--compare` | 與 Mathlib 的 `RiemannHypothesis` 完全一致 |

最關鍵的設計是「inert export」：被檢查的不是 Lean 原始碼，而是編譯後匯出的純證明物件。原始碼裡就算藏了惡意程式碼，也碰不到檢查器。con-leche 與 con-ron 另附形式化證明，說明它們相對於集合論不可能接受假證明，這是專門用來堵「Lean 的邏輯本身有 bug」那條路。

所以「對不對」這一層，數學界已經不太吵了。吵的是另一件事，見第 4 節。

<!-- FIG-B -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 660" role="img" aria-label="驗證信任鏈：原始碼、inert export、四個 kernel、敘述比對" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker><marker id="mfbbf2499" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#fbbf2499"/></marker></defs>
<rect x="0.75" y="0.75" width="898.5" height="658.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">四個 kernel、一個 inert export、三個公理</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每一層的存在，都是為了讓下一層不必信任上一層</text>
<rect x="60" y="118" width="620" height="64" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="370.0" y="148.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">① Lean 原始碼（175,187 檔）</text>
<text x="370.0" y="170.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">沙盒重編譯：無網路、來源唯讀</text>
<rect x="60" y="212" width="620" height="64" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="370.0" y="242.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">② inert export（61,570,595,788 bytes）</text>
<text x="370.0" y="264.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只含五個定理的依賴閉包；原始碼碰不到檢查器</text>
<rect x="60" y="306" width="620" height="168" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="76" y="330" font-size="13.5" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">③ 四個 kernel 各檢一次同一份 export</text>
<rect x="76" y="348" width="284" height="52" rx="10" fill="#1c2230" stroke="#c084fc66" stroke-width="1.5"/>
<text x="218.0" y="372.0" font-size="13.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Lean 官方 kernel</text>
<text x="218.0" y="394.0" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">48 h 03 m／82.6 GiB</text>
<rect x="376" y="348" width="284" height="52" rx="10" fill="#1c2230" stroke="#c084fc66" stroke-width="1.5"/>
<text x="518.0" y="372.0" font-size="13.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">paranoid kernel</text>
<text x="518.0" y="394.0" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">72 h 20 m／98.8 GiB</text>
<rect x="76" y="410" width="284" height="52" rx="10" fill="#1c2230" stroke="#c084fc66" stroke-width="1.5"/>
<text x="218.0" y="434.0" font-size="13.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">nanoda（Rust）</text>
<text x="218.0" y="456.0" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">27 m 42 s／80 執行緒</text>
<rect x="376" y="410" width="284" height="52" rx="10" fill="#1c2230" stroke="#c084fc66" stroke-width="1.5"/>
<text x="518.0" y="434.0" font-size="13.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">con-leche ＋ con-ron</text>
<text x="518.0" y="456.0" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">附健全性形式證明</text>
<rect x="60" y="496" width="620" height="66" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<text x="370.0" y="527.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">④ 敘述比對：證的定理 ＝ Mathlib 的 RiemannHypothesis</text>
<text x="370.0" y="549.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Comparator、con-leche --compare；兩個獨立實作</text>
<path d="M 370 182 L 370 210" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 370 276 L 370 304" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 370 474 L 370 494" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="712" y="306" width="148" height="256" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="786" y="334" font-size="13" fill="#8b949e" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全篇只依賴</text>
<text x="786" y="366" font-size="11.5" fill="#fbbf24" text-anchor="middle" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">propext</text>
<text x="786" y="392" font-size="11.5" fill="#fbbf24" text-anchor="middle" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">Classical.choice</text>
<text x="786" y="418" font-size="11.5" fill="#fbbf24" text-anchor="middle" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">Quot.sound</text>
<text x="786" y="470" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">沒有</text>
<text x="786" y="490" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Lean core 以外</text>
<text x="786" y="510" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">的任何公理</text>
<path d="M 710 505 L 686 525" fill="none" stroke="#fbbf2499" stroke-width="1.5" marker-end="url(#mfbbf2499)"/>
<text x="60" y="600" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">被檢查的不是原始碼，是匯出後的證明物件；所以「程式碼裡藏了什麼」不影響結論。</text>
<text x="60" y="626" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">三個公理是 Lean 的標準公理，不是作者自己加的假設。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：驗證的四層。被檢查的是 export 而不是原始碼，所以「程式碼裡藏了什麼」碰不到結論；四個 kernel 裡有兩個附健全性形式證明，專門用來堵「Lean 的邏輯本身有 bug」。</figcaption>
</figure>
<!-- /FIG-B -->


## 2. 五個要打折的數字

| 常見說法 | 實際情況 |
|---|---|
| 證明寫成人話有 25 萬頁 | Alpöge 隔天在 X 上說那個數字是玩笑（「I find big numbers extremely hilarious」）；不過他同時形容自己產出的 paper 版是「travesty of slop」。頁數不可引用，行數可以 |
| 困擾數學界 166 年 | 1859 到 2026 是 167 年，Nature 也寫 167 |
| 100 萬美元懸賞快發了 | Clay 的規則是：須發表於世界公認的審稿期刊，且<strong>發表兩年後</strong>才進評審程序。這是規則問題，與 AI 無關 |
| 這是唯一的證明 | 同一天，Masullo 的全人類、無 AI 證明由 Vakil 以「hurried announcement」名義貼出 |
| Anthropic 官方宣佈 | 是 Alpöge 的個人貼文，時間在 Anthropic 那斯達克上市（11/19）後一天。他自己說「The precise timing is horrible」 |

補一個正向的數字：從發佈到社群完成稽核，只有兩天，參與者超過 200 人。

## 3. 1,700 萬行不是「證明的長度」

念數學的人都有一種經驗：一個證明五行，看完突然懂了，想拍桌子。於是很自然會問：25 萬頁的證明，還 elegant 嗎？

這個問題的量尺拿錯了。<strong>Lean 檔案不是文章，是編譯產物。</strong>形式化時，每個 tactic 的中間狀態都會被攤平寫出來，一份三頁的論文常常變成幾千行。問 Lean 檔有幾行，接近問 gcc 編出來的機器碼有幾行。

有個細節很能說明這份東西的性質：175,187 個模組裡，有一個模組的 .olean 每次編譯不完全相同。原因是 `BBtop.eq_1` 這個自動生成的等式引理，Lean 會拿「第一個用到它的定理」的 bound variable 名字去命名，並行編譯時可能拿到不同名字。這是 Lean issue #15498，v4.36.0 修掉。kernel 檢查不看名字，所以不影響正確性；但它提醒你，手上這東西是被當<strong>程式碼</strong>在審的，不是被當文章在讀的。


<!-- FIG-A -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 620" role="img" aria-label="壓縮金字塔：從 1,700 萬行 Lean 到一句話" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="898.5" height="618.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個證明，五種長度</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每一層都是上一層的壓縮；只有最下面那層是人能讀的</text>
<text x="60" y="108" font-size="13" fill="#8b949e" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">機器那一側（可檢查）</text>
<text x="760" y="108" font-size="13" fill="#8b949e" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">這一步做了什麼</text>
<rect x="60" y="126" width="640" height="64" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="76" y="155.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1,700 萬行 Lean</text>
<text x="76" y="176.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">175,187 個檔案，只依賴 Mathlib</text>
<text x="760" y="210" font-size="15.5" fill="#2dd4bf" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">↓ 編譯</text>
<rect x="60" y="220" width="540" height="64" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="76" y="249.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">61.5 GB proof export</text>
<text x="76" y="270.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1,484,729 個宣告：五個定理的依賴閉包</text>
<text x="760" y="304" font-size="15.5" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">↓ 匯出</text>
<rect x="60" y="314" width="430" height="64" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="76" y="343.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">13 條假設</text>
<text x="76" y="364.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">主不等式 (M) 的歸約，沒有一條被獨立證明</text>
<text x="760" y="398" font-size="15.5" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">↓ 歸約</text>
<rect x="60" y="408" width="320" height="64" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="76" y="437.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">265 頁人類版</text>
<text x="76" y="458.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Rubinstein v2，古典解析數論的語言</text>
<text x="760" y="492" font-size="15.5" fill="#c084fc" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">↓ 翻譯</text>
<rect x="60" y="502" width="230" height="64" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<text x="76" y="531.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一句話：√X 鏈</text>
<text x="76" y="552.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Stepanov 方法 ＋ theta lift 鏈</text>
<text x="60" y="596" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">長度往下遞減，理解沒有自動往上——最後一行就是第 6 節那句話的候選。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：同一個證明的五種長度。每一層都是上一層的壓縮，但只有最下面那層是人能讀的——這就是「1,700 萬行」不能直接換算成「證明有多長」的原因。</figcaption>
</figure>
<!-- /FIG-A -->

所以「17M 行 vs 五行」不是兩份證明的長度比較。真正的問題是：有沒有人類長度的版本？答案是「有第一版，但有洞」。

## 4. 缺口的真正大小：13 個洞

Waterloo 的 Michael Rubinstein 在 11 月 21 日放了 164 頁，22 日更新到 265 頁。標題很直白：把 RH 這件事，對黎曼 zeta 函數解釋一遍。寫法是古典解析數論的語言，不是 Lean。

但它不是完整的證明。它做的是：從一個主不等式 (M) 推出 RH，然後把 (M) 歸約成 <strong>13 條用古典語言寫下的假設</strong>，並註明哪幾條由 Lean 開發提供。13 條裡沒有一條被獨立證明。(M) 這一段在稿子裡是空的，第 I.12 節列出還缺什麼。

<!-- FIG-D -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 610" role="img" aria-label="歸約圖：黎曼猜想被歸約成十三條未證假設" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker><marker id="m2dd4bfbb" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bfbb"/></marker></defs>
<rect x="0.75" y="0.75" width="898.5" height="608.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">缺口不是頁數，是十三條沒人證過的假設</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Rubinstein 的 265 頁人類版做到的，就是把 RH 搬成這樣一張圖</text>
<rect x="330" y="118" width="240" height="58" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<text x="450.0" y="152.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">黎曼猜想 RH</text>
<path d="M 450 176 L 450 204" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="280" y="206" width="340" height="64" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="450.0" y="236.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">主不等式 (M)</text>
<text x="450.0" y="258.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">加權質數冪和的估計；稿中這段是空的</text>
<path d="M 450 270 L 450 296" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="71.0" y="306" width="98" height="50" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="120.0" y="336.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<rect x="181.0" y="306" width="98" height="50" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="230.0" y="336.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text>
<rect x="291.0" y="306" width="98" height="50" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="340.0" y="336.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text>
<rect x="401.0" y="306" width="98" height="50" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="450.0" y="336.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<rect x="511.0" y="306" width="98" height="50" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="560.0" y="336.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text>
<rect x="621.0" y="306" width="98" height="50" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="670.0" y="336.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text>
<rect x="731.0" y="306" width="98" height="50" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="780.0" y="336.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7</text>
<rect x="126.0" y="368" width="98" height="50" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="175.0" y="398.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text>
<rect x="236.0" y="368" width="98" height="50" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="285.0" y="398.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">9</text>
<rect x="346.0" y="368" width="98" height="50" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="395.0" y="398.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10</text>
<rect x="456.0" y="368" width="98" height="50" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="505.0" y="398.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">11</text>
<rect x="566.0" y="368" width="98" height="50" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="615.0" y="398.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">12</text>
<rect x="676.0" y="368" width="98" height="50" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="725.0" y="398.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">13</text>
<rect x="170" y="452" width="560" height="60" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="450.0" y="480.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Lean 開發（175,187 檔）</text>
<text x="450.0" y="502.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">其中幾條由它提供；哪幾條見 §I.12</text>
<path d="M 300 450 L 300 426" fill="none" stroke="#2dd4bfbb" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#m2dd4bfbb)"/>
<path d="M 450 450 L 450 426" fill="none" stroke="#2dd4bfbb" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#m2dd4bfbb)"/>
<path d="M 600 450 L 600 426" fill="none" stroke="#2dd4bfbb" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#m2dd4bfbb)"/>
<text x="450" y="548" font-size="13" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">十三條裡沒有一條被獨立證明；本文也沒有逐條評估它們的內容。</text>
<text x="450" y="574" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">能確定的是：最難的部分目前仍然指向機器。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 4：缺口不是頁數，是十三條假設。RH 被搬成 (M)，(M) 被搬成十三條古典語言的假設；其中幾條由 Lean 開發提供，哪幾條看 §I.12。</figcaption>
</figure>
<!-- /FIG-D -->


換句話說，目前的人話翻譯，是把最難的部分指回機器。這就是玄奘困境的精確版本：譯文有了，但譯文裡有十三處寫著「原文如此」。

值得一提的是進度也不是零：v2 把建構的物件、把 (M) 歸約到編號假設的過程、還有最簡單的 lemniscate（雙紐線）情形<strong>整段算完</strong>，都補上了。從 11/20 到 11/22，三天。1976 年四色定理之後，數學家花了幾十年才等到能讀的版本。

## 5. 玄奘的比喻要修一個地方

原本的想像很自然：AI 用機器語言寫出又長又硬的原文，人讀懂、拆小、寫回人話。所以會有一批數學家，花一輩子翻譯 AI 的證明。

這件事有一半已經發生了，而且比想像快。但要修的是分工：<strong>翻譯的人也在用 AI。</strong>

Rubinstein 那份 265 頁，自己註明是「with Claude, Codex and Gemini as an aid」寫成的。倫敦 Queen Mary 的 Abhishek Saha 用 OpenAI 的模型把 Lean 片段壓成研討會單頁海報，他估最終可以壓到 10,000 頁以下、甚至 1,000 頁。

<!-- FIG-E -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 400" role="img" aria-label="三天時間軸：發佈、認證、兩個版本的人類版、報導" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="898.5" height="398.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">五天，機器那一側就結束了</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">人類那一側從 11/21 才開始，目前還停在十三個洞</text>
<path d="M 110 200 L 790 200" fill="none" stroke="#30363d" stroke-width="2"/>
<circle cx="110.0" cy="200" r="7" fill="#2dd4bf"/>
<text x="110.0" y="138" font-size="13" fill="#2dd4bf" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">11/20</text>
<text x="110.0" y="160" font-size="12.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">發佈 1,700 萬行</text>
<text x="110.0" y="178" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Lean 檔</text>
<circle cx="246.0" cy="200" r="7" fill="#58a6ff"/>
<text x="246.0" y="230" font-size="13" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">11/21</text>
<text x="246.0" y="252" font-size="12.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FRO ＋ Mathlib</text>
<text x="246.0" y="270" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">full confidence</text>
<circle cx="382.0" cy="200" r="7" fill="#c084fc"/>
<text x="382.0" y="138" font-size="13" fill="#c084fc" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">11/21</text>
<text x="382.0" y="160" font-size="12.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">人類版 v1</text>
<text x="382.0" y="178" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">164 頁，有洞</text>
<circle cx="518.0" cy="200" r="7" fill="#c084fc"/>
<text x="518.0" y="230" font-size="13" fill="#c084fc" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">11/22</text>
<text x="518.0" y="252" font-size="12.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">人類版 v2</text>
<text x="518.0" y="270" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">265 頁，13 個洞</text>
<circle cx="654.0" cy="200" r="7" fill="#fbbf24"/>
<text x="654.0" y="138" font-size="13" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">11/22–23</text>
<text x="654.0" y="160" font-size="12.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">paranoid kernel</text>
<text x="654.0" y="178" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">72 h 跑完</text>
<circle cx="790.0" cy="200" r="7" fill="#7d8590"/>
<text x="790.0" y="230" font-size="13" fill="#7d8590" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">11/24</text>
<text x="790.0" y="252" font-size="12.5" fill="#e6edf3" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">WIRED 報導</text>
<text x="790.0" y="270" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">「alien」</text>
<path d="M 110 316 L 790 316" fill="none" stroke="#7d8590" stroke-width="1.6"/>
<path d="M 790 316 L 808 316" fill="none" stroke="#7d8590" stroke-width="1.6" marker-end="url(#m7d8590)"/>
<text x="110" y="342" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">人類理解：仍在 13 個洞</text>
<text x="808" y="342" font-size="12" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">未完成</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 5：五天，機器那一側就結束了。人類那一側從 11/21 才開始，還在十三個洞。</figcaption>
</figure>
<!-- /FIG-E -->


所以不是「AI 寫、人翻譯」的兩段式，而是 AI 寫、AI 初譯、人決定哪一段值得讀。人退到的位置不是第二線，是<strong>編輯台</strong>。這比「人退到第二線」更奇怪，也更值得注意：判斷力變成稀缺資源，而判斷力恰好是最難外包的那一種。

## 6. 目前最接近「拍桌子」的一句話

Alpöge 自己的輪廓是這樣：這是 <strong>Stepanov 方法</strong>的後代。

有限體上，Weil 與 Deligne 證了曲線版的 RH。Stepanov 在 1969 年（後來由 Bombieri 簡化）給了更初等的路：造一個輔助多項式，讓它在要數的點上高重數消失，高重數逼出強估計，而強估計就是 RH 在講的事。重數靠微分來量；整數上沒有微分，所以這條路一百年過不去。

他的想法是：用一串 <strong>theta lift</strong> 冒充重數。走過一串 totally definite unitary groups，每一步賺一個重數單位。對長度 X 的 von Mangoldt 和，鏈長約 <strong>√X</strong>。他自己的說法是：事後看，很難想像它還能是別的。

<!-- FIG-C -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" role="img" aria-label="Stepanov 方法的兩欄對照：有限體靠微分，整數靠 theta lift 鏈" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="898.5" height="598.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個想法，換一種東西來充當「重數」</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">左邊是已證的有限體版，右邊是 Alpöge 搬到整數上的做法</text>
<rect x="60" y="118" width="380" height="372" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="76" y="146" font-size="14" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">有限體上（1940s 已證）</text>
<rect x="470" y="118" width="370" height="372" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="486" y="146" font-size="14" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">整數上（一百年過不去）</text>
<rect x="76" y="166" width="348" height="64" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="250.0" y="196.0" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">曲線 C / F_q</text>
<text x="250.0" y="218.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只有有限個點，可以逐點數</text>
<rect x="486" y="166" width="338" height="64" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="655.0" y="196.0" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Z 上沒有微分</text>
<text x="655.0" y="218.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">重數無從量起 — 這就是卡住的地方</text>
<rect x="76" y="242" width="348" height="64" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="250.0" y="272.0" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輔助多項式 f</text>
<text x="250.0" y="294.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">在要數的點 P 上重數 m 消失</text>
<rect x="486" y="242" width="338" height="64" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="655.0" y="272.0" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">替代：theta lift 鏈</text>
<text x="655.0" y="294.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">U(X0) → U(X1) → … → U(Xm)</text>
<rect x="76" y="318" width="348" height="64" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="250.0" y="348.0" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">有微分 → 重數可量</text>
<text x="250.0" y="370.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">f 的第 k 階導數不為零的次數</text>
<rect x="486" y="318" width="338" height="64" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="655.0" y="348.0" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每一步 +1 重數</text>
<text x="655.0" y="370.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">用一個 unitary group 換一次「微分」</text>
<rect x="76" y="394" width="348" height="64" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="250.0" y="424.0" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">得到估計</text>
<text x="250.0" y="446.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Weil／Deligne；Stepanov 的初等版</text>
<rect x="486" y="394" width="338" height="64" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="655.0" y="424.0" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">對長度 X 的 von Mangoldt 和</text>
<text x="655.0" y="446.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">鏈長 m ≈ √X；重數另外算</text>
<text x="450" y="522" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">差異只有一處：重數這一步，左邊用微分，右邊用一串 theta lift。</text>
<text x="450" y="548" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">示意圖。每一步是一個 unitary group，鏈長 ≈ √X 與重數是兩個量，不要合併讀。</text>
<text x="450" y="574" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Alpöge 自己的說法：這是 Stepanov 方法的後代，「事後看很難想像它還能是別的」。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 3：Stepanov 方法的兩欄對照。差別只有一處——重數這一步用什麼換。示意圖；鏈長與重數是兩個量，不要合併讀。</figcaption>
</figure>
<!-- /FIG-C -->


配料清單長得嚇人：Stepanov 式行列式、Bost slope inequality、用 Behrend 構造挑的 Iwasawa tower、relative trace formula、Gan–Gross–Prasad periods、seesaw identities、Rallis 的 theta lift、Chowla–Selberg 公式、Weyl 與 Siegel 的 mass 計算、弱化版的 Vandiver 猜想；時間軸最後一條（11/16）只寫了「GRH」兩個字。

Terence Tao 的初步評價是：這個策略動用了 Langlands 計畫與算術幾何的全力。Saha 說得更直：「我不覺得這種證明會從人類手上出現過……幾乎是外星人的。」

但這裡要老實標一個出處差異：<strong>上面這段「為什麼」，是作者對機器的回溯敘述，不是機器本身。</strong>他明說部分段落是轉述 Claude 的摘要、可能「make zero sense」，真正的論證是 Lean 碼。也就是說，「拍桌子的那句話」目前還是二手貨——這是它最誠實的狀態。

## 7. 統計的直覺，在這裡不適用

學統計的人看到「電腦已經驗過十兆個例子」，很自然會說：夠了吧。十兆筆都對，早就該下結論。

但 1,700 萬行 Lean 不是十兆個樣本，是一份<strong>推導</strong>。每一步都是從前提推到結論，不是抽樣。所以「十兆跟無限比還是零」這個焦慮，在這裡不成立——差別不是有限對無限，而是<strong>驗證對理解</strong>。

Lean 給的是驗證，而且是很強的驗證：三個 kernel、兩個獨立實作、其中兩個還附健全性證明、沙箱重現、逐 byte 比對。但「理解」不在 kernel 的規格裡。驗證器只回答「這個敘述是否從這三個公理推得出來」，它不回答「為什麼會這樣」。

Lean FRO 那份公告的最後一句，其實自己承認了這一點：「We look forward to all the activity in the mathematical community that will help explain the new ideas in this proof.」他們很清楚自己交出去的是什麼：一個沒有縫的答案，還沒有人話的解釋。

## 8. 我的實務結論

如果你只帶走一件事：這次人類第一次拿到「確定為真、但為什麼還沒有人講清楚」的東西，而第一份試圖解釋它的 265 頁，也是 AI 幫忙寫的。

按目的分：

- <strong>想理解</strong>：讀 Rubinstein 的 265 頁（古典解析數論語言），不要讀 1,700 萬行。但要知道它把最難的部分外包回 Lean。
- <strong>想自己驗</strong>：MIT 的 Sutherland 把腳本、log、export 都放出來了，包含 paranoid kernel 與 byte 級重現；照跑一次大約要兩天機器時間與 80 GB 記憶體。
- <strong>想引用</strong>：可以引「已驗證的敘述」（RH 與 Dirichlet L 的 GRH），可以引「13 條假設」。不要引「25 萬頁」，那是玩笑。
- <strong>想押時間</strong>：Clay 要審稿期刊發表加上兩年，所以 2028 年底之前不會有結果；若人類版先補完 13 個洞，獎金歸屬會變得很複雜。

至於 elegant：我猜會回來，但不會以「同一個證明變短」的形式回來。四色定理的經驗是，簡化不是把原本的證明壓縮，而是換一套想法重講一次。這次要換的那套想法，可能還要等下一輪 AI 與人一起找。

## 9. 一手來源

| 項目 | 連結 | 查證結果 |
|---|---|---|
| Lean FRO 與 Mathlib 聯合聲明 | [leanprover-community.github.io](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) | 四條標準、inert export、con-leche/con-ron 的健全性證明 |
| MIT 驗證總表（Andrew Sutherland） | [math.mit.edu/~drew/grh](https://math.mit.edu/~drew/grh/) | 175,187 模組、48h03m／82.6 GiB、export 61,570,595,788 bytes、不確定模組說明 |
| 人類版工作草案（Rubinstein） | [math.uwaterloo.ca/~mrubinst](https://math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/) | 265 頁 v2、(M) 歸約為 13 條假設、§I.12 待補清單 |
| Alpöge 原始說明 | [alpo.ge/remark.pdf](https://alpo.ge/remark.pdf) | 11/20 發佈；Stepanov ＋ theta lift 鏈、√X |
| Nature 報導 | [nature.com](https://www.nature.com/articles/d41586-026-03812-7) | 同日 Masullo 全人類證明、Maynard 評語、167 年 |
| WIRED 報導 | [wired.com](https://www.wired.com/story/ai-solved-maths-most-famous-problem/) | 「250,000 頁是玩笑」、Saha 的 10,000 頁估計、「alien」評語 |
| The Guardian 報導 | [theguardian.com](https://www.theguardian.com/technology/2026/nov/21/anthropic-riemann-hypothesis-solved-claude-ai) | 六週、兩組織獨立驗證、Anthropic 上市時序 |

> <strong>查證說明</strong>：以上數字於 2026-11-25 直接讀取一手頁面。<br />
> 會變的東西：MIT 頁面持續更新（`lake comparator` 那一輪當時還在跑）、Rubinstein 的稿子是 working draft、Verification log 每天有新條目。<br />
> 沒實測的東西：我沒有自己重跑 kernel 檢查（需要 80 GB 記憶體與兩天），也沒有讀完 265 頁稿子；13 條假設的具體內容我沒有逐條評估。<br />
>
> <strong>封面</strong>：由本機 ComfyUI 的 Qwen-Image 2.1 生成（刻意不含文字），三個種子出候選後挑一張。
