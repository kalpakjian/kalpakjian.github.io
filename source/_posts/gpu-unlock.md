---
title: gpu-unlock 專題：NVIDIA 消費級卡那道「半速鎖」，是怎麼被打開的
date: 2026-10-25 23:10:00
permalink: gpu-unlock/
categories:
  - AI
  - 硬體
tags:
  - NVIDIA
  - GPU
  - 硬體解鎖
  - 逆向工程
  - 實測
toc: true
---

## 這個專題在講什麼

2026 年 10 月底，開源社群接連釋出兩個工具，把 NVIDIA 一個存在多年的「半速鎖」打開了——**消費級顯示卡上，FP16／BF16 搭配 FP32 累加的張量指令速率，本來被限制在半速**。解鎖後，這條路徑的速度回到與專業卡（RTX A 系列）相當的檔位。

這不是超頻，不是刷 BIOS，也不是改驅動程式。它的做法是：利用 NVIDIA 開機韌體裡的一個**緩衝區溢位漏洞**，在 GPU 驅動載入之前改寫「速率選擇器」暫存器。

這個專題收錄**五篇**文章：三篇**事實查核**（把媒體口耳相傳的說法逐條比對一手來源），兩篇**分卡型操作筆記**（RTX 3080 12GB 與 RTX 4090 的完整動手流程）。

第三篇查核是 2026-10-27 追加的，它查的是「RTX 5090 的解鎖方案應該很快出來，解鎖後 AI 算力可衝上 420 TFLOPS 以上」——**結論是「不會」，而且不是「還沒人做」，是「寫不進去」**。它同時帶出兩個新東西：社群在 10 月下旬新做的**兩條 Turing 分支**，以及一個必須寫進風險清單的**授權條款**問題。

> <strong>一句話結論</strong>：**這是真的技術路線，證據鏈紮實；但媒體的關鍵字一個都不成立。**「全系列」「翻倍」「所有 AI 負載都變快」「Windows 一鍵可用」「5090 也快能解」——五個都錯。

## 專案血緣：從挖礦卡一路走到 Blackwell 那道牆

<!-- FIG1 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 724" role="img" aria-label="gpu-unlock 專案血緣：從 cmpunlocker 到 cmp90hx-unlock、gpu-unlock、gpu-unlock-ada，加上 2026-10 的兩條 Turing 分支，以及 Blackwell 那道牆" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="998.5" height="722.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">專案血緣</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個 exploit，兩種做法；Blackwell 沒有分支</text>
<rect x="48" y="132" width="330" height="68" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="64" y="158" font-size="13.5" fill="#7d8590" font-weight="700" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">cmpunlocker</text>
<text x="362" y="158" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">amoghmunikote</text>
<text x="64" y="178" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">把 8／10 GB 的 CMP 170HX 解鎖成 64／40 GB</text>
<text x="64" y="192" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">曾被 LTT 報導過的那一支</text>
<path d="M 213.0 200 L 213.0 208" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="208" width="330" height="68" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="64" y="234" font-size="13.5" fill="#7d8590" font-weight="700" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">cmp90hx-unlock</text>
<text x="362" y="234" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">WildFlash1st</text>
<text x="64" y="254" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">貢獻 GA102 的 V67 payload 鏈</text>
<text x="64" y="268" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">後來兩邊都沿用同一條鏈</text>
<path d="M 213.0 276 L 213.0 284" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="284" width="330" height="68" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="64" y="310" font-size="13.5" fill="#2dd4bf" font-weight="700" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">gpu-unlock</text>
<text x="362" y="310" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Zagitta</text>
<text x="64" y="330" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">第一個 Linux 核心模組版本</text>
<text x="64" y="344" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GA10x 數十個裝置 ID，靠社群眾包</text>
<path d="M 213.0 352 L 213.0 360" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="360" width="330" height="68" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="64" y="386" font-size="13.5" fill="#2dd4bf" font-weight="700" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">gpu-unlock-ada</text>
<text x="362" y="386" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">JustAResearcher</text>
<text x="64" y="406" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">移植到 Ada 世代（RTX 40）</text>
<text x="64" y="420" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">白名單精簡到 4 個 ID，證據做成配對實測</text>
<rect x="48" y="444" width="330" height="132" rx="10" fill="#1c2230" stroke="#c084fc55" stroke-width="1.5"/>
<text x="64" y="466" font-size="11.5" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Turing 分支（2026-10 各自另起爐灶）</text>
<rect x="64" y="476" width="298" height="44" rx="6" fill="#161b22" stroke="#c084fc55" stroke-width="1.5"/>
<text x="78" y="493" font-size="12" fill="#c084fc" font-weight="700" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">turing-unlock</text>
<text x="348" y="493" font-size="9.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">nlzy</text>
<text x="78" y="509" font-size="9.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2026-10-24 · 2080 Ti 22GB</text>
<rect x="64" y="524" width="298" height="44" rx="6" fill="#161b22" stroke="#c084fc55" stroke-width="1.5"/>
<text x="78" y="541" font-size="12" fill="#c084fc" font-weight="700" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">KohakUnlock</text>
<text x="348" y="541" font-size="9.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">KohakuBlueleaf</text>
<text x="78" y="557" font-size="9.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2026-10-25 · Leadtek TU102 雙卡</text>
<text x="48" y="598" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Turing 那兩條與 Ada 版同源（V67 溢位鏈），但各自獨立發展。</text>
<rect x="420" y="132" width="532" height="348" rx="14" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.5"/>
<text x="440" y="160" font-size="14" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩個 Linux 模組的關鍵差異</text>
<text x="440" y="182" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個 exploit，不同的涵蓋範圍與證據策略</text>
<rect x="436" y="202" width="250" height="44" rx="8" fill="#161b22" stroke="#fbbf2455" stroke-width="1.5"/>
<rect x="694" y="202" width="242" height="44" rx="8" fill="#161b22" stroke="#fbbf2455" stroke-width="1.5"/>
<text x="448" y="220" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">gpu-unlock</text>
<text x="448" y="237" font-size="11" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GA102／103／104／106 數十個 ID</text>
<text x="706" y="220" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">gpu-unlock-ada</text>
<text x="706" y="237" font-size="11" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">僅 4 個 Ada ID</text>
<text x="440" y="194" font-size="9.5" fill="#7d8590" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">涵蓋範圍</text>
<rect x="436" y="258" width="250" height="44" rx="8" fill="#161b22" stroke="#fbbf2455" stroke-width="1.5"/>
<rect x="694" y="258" width="242" height="44" rx="8" fill="#161b22" stroke="#fbbf2455" stroke-width="1.5"/>
<text x="448" y="276" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">gpu-unlock</text>
<text x="448" y="293" font-size="11" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4070 Ti SUPER 需實驗旗標</text>
<text x="706" y="276" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">gpu-unlock-ada</text>
<text x="706" y="293" font-size="11" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4090 只要 targets 一項</text>
<text x="440" y="250" font-size="9.5" fill="#7d8590" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">實驗旗標</text>
<rect x="436" y="314" width="250" height="44" rx="8" fill="#161b22" stroke="#fbbf2455" stroke-width="1.5"/>
<rect x="694" y="314" width="242" height="44" rx="8" fill="#161b22" stroke="#fbbf2455" stroke-width="1.5"/>
<text x="448" y="332" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">gpu-unlock</text>
<text x="448" y="349" font-size="11" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">沒有診斷工具</text>
<text x="706" y="332" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">gpu-unlock-ada</text>
<text x="706" y="349" font-size="11" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">有唯讀讀回與指令率探針</text>
<text x="440" y="306" font-size="9.5" fill="#7d8590" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">診斷工具</text>
<rect x="436" y="370" width="250" height="44" rx="8" fill="#161b22" stroke="#fbbf2455" stroke-width="1.5"/>
<rect x="694" y="370" width="242" height="44" rx="8" fill="#161b22" stroke="#fbbf2455" stroke-width="1.5"/>
<text x="448" y="388" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">gpu-unlock</text>
<text x="448" y="405" font-size="11" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">靠社群眾包相容性報告</text>
<text x="706" y="388" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">gpu-unlock-ada</text>
<text x="706" y="405" font-size="11" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">配對實測＋數值驗證＋遙測</text>
<text x="440" y="362" font-size="9.5" fill="#7d8590" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">證據策略</text>
<text x="440" y="442" font-size="12" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">共同的根：已簽章 NVIDIA booter 的緩衝區溢位 + ROP</text>
<text x="440" y="462" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">解開 FEAT_OVR_PLM 的寫入保護後，寫 SS0／SS1 即可改成全速</text>
<rect x="48" y="616" width="904" height="88" rx="10" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="68" y="642" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Windows 那條線是旁支：TOTORONG/AD103_win_unlocker 的 UEFI 實驗提供 AD102 payload；</text>
<text x="68" y="664" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">impacifist/Windows-GPU-UNLOCK 則把它做成獨立的 Windows 工具。</text>
<text x="68" y="686" font-size="13" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Blackwell 沒有分支——維護者 2026-10-26 公開回覆「The short answer is no」：不是還沒做，是寫不進去。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：專案血緣——共同的根都是已簽章 NVIDIA booter 的緩衝區溢位；2026-10 新增兩條 Turing 分支，而 Blackwell 那一格是空的。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG1 -->


這條技術路線不是一個人突然想出來的，它是從「解鎖資料中心礦卡」的那條線一步步長出來的：

| 專案 | 貢獻 |
| --- | --- |
| [cmpunlocker](https://github.com/amoghmunikote/cmpunlocker) | 把 8／10 GB 的 CMP 170HX 資料中心礦卡解鎖成 64／40 GB。被 Linus Tech Tips 報導過，是這條線的第一個響亮成果 |
| [cmp90hx-unlock](https://github.com/WildFlash1st/cmp90hx-unlock) | 貢獻 GA102 的 V67 payload 鏈，兩邊後來都沿用 |
| [gpu-unlock](https://github.com/Zagitta/gpu-unlock) | 把它變成**一般消費級卡也能用的 Linux 核心模組**——Ampere 世代的完整版 |
| [gpu-unlock-ada](https://github.com/JustAResearcher/gpu-unlock-ada) | 移植到 Ada 世代（RTX 40），白名單精簡、證據做成配對實測 |
| [nlzy/turing-unlock](https://github.com/nlzy/turing-unlock) | Turing 世代（RTX 20）的一條獨立路線，2026-10-24 才公開；只測過一張 2080 Ti 22GB |
| [KohakuBlueleaf/KohakUnlock](https://github.com/KohakuBlueleaf/KohakUnlock) | Turing 世代的另一條獨立路線，2026-10-25 才公開；兩張 Leadtek TU102，並揭露原始 `mmapeak` 的全零輸入缺陷 |

Windows 那條線是旁支：[TOTORONG/AD103_win_unlocker](https://huggingface.co/TOTORONG/AD103_win_unlocker) 的 UEFI 實驗提供了 AD102 的 payload，Ada 版把它整進 Linux 模組；而 [impacifist/Windows-GPU-UNLOCK](https://github.com/impacifist/Windows-GPU-UNLOCK) 則把它做成獨立的 Windows 工具（但只硬體驗證過 3090 FE 與 3070 Ti 兩個單板型）。

## 為什麼會有這道鎖（白話版）

NVIDIA 長久以來有一個產品區隔的做法：**同一顆晶片，賣給玩家時把 FP16／BF16 的速率鎖成一半，賣給專業用戶時才給全速。**

用一個比喻：你的車引擎很猛，但出廠時行控器裡被寫死一條規則——「某條線最多只能跑半速」。專業版車子沒有這條規則，售價是數倍起跳。

而「鎖」本身在規格表上是**看不出來的**：它藏在 `FEAT_OVR_SM_SPD`（簡稱 SS0）與 `FEAT_OVR_SM_SPD_1`（SS1）這兩個暫存器裡，每個 4-bit 欄位控制一種指令的速率檔位（`00` = 全速、`01` = 半速）。加上「保護層級遮罩」（PLM），驅動程式根本寫不進去。

對照 2018 年 Turing 時代的原始討論（[TensorFlow issue #24531](https://github.com/tensorflow/tensorflow/issues/24531)）：

> The peak FP16 Tensor TFLOPS with FP32 Accumulate is only **43.6%** of NVIDIA Quadro RTX6000. This is very abnormal, **obviously an artificial limit**.

**同一顆晶片、貼上不同的名字、效能差一倍**——這就是這整個專題的起點。

## 漏洞利用是怎麼回事（白話版）

GPU 開機時，驅動程式把加密韌體交給 GPU 裡的一顆安全處理器（SEC2），SEC2 驗簽、解密、然後在 GSP 上執行。這整套設計本來是安全的。

**但那顆安全處理器上跑的開機程式（booter）有一個典型的緩衝區溢位**——溢位直接寫進堆疊，攻擊者就能用 <strong>ROP（Return-Oriented Programming，把現成指令片段串成任意程式碼）</strong>取得控制流。

拿到控制流之後只做一件事：**把寫入保護的遮罩打開**。原廠預設 `FEAT_OVR_PLM = 0xffffff8f`，其中寫入保護位元表示「只有最高權限層可以寫」；既然已經在最高權限層裡，把這個值寫成 `0xFFFFFFFF`，速率選擇器就變成驅動程式可以寫了。目標值是 `SS0 = 0x88888888`、`SS1 = 0x8`。

整條鏈發生在 **NVIDIA 驅動程式載入之前**，所以驅動本身完全沒被動過——這也是為什麼「更新驅動不用重新打補丁」。

> <strong>但請記住它的性質</strong>：這是**對 GPU 安全處理器的未授權程式碼執行**。它比一般驅動 hack 重一級，而且 NVIDIA 有強烈動機修掉它——「更新驅動不用補丁」對用戶是方便，對方案的長期存續卻是風險。

## 五篇文章速查

<!-- FIG2 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 718" role="img" aria-label="gpu-unlock 專題五篇文章速查：兩篇事實查核、兩篇分卡型操作筆記，以及 2026-10-27 新增的 Blackwell 查核" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="998.5" height="716.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">五篇速查</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">先看哪一篇？</text>
<rect x="48" y="126" width="440" height="160" rx="12" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<rect x="48" y="126" width="6" height="160" rx="3" fill="#58a6ff" stroke="#30363d" stroke-width="1.5"/>
<text x="70" y="154" font-size="10.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">事實查核</text>
<text x="70" y="178" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 30 系 gpu-unlock</text>
<text x="70" y="200" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">對象：GA10x 數十個 ID</text>
<text x="70" y="222" font-size="11.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">關鍵數字：BF16 +25～81%</text>
<path d="M 70 234 L 466 234" fill="none" stroke="#30363d" stroke-width="1.2"/>
<text x="70" y="256" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">「一律翻倍」不成立；各型號差三倍</text>
<text x="70" y="276" font-size="11" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 讀這篇</text>
<rect x="512" y="126" width="440" height="160" rx="12" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<rect x="512" y="126" width="6" height="160" rx="3" fill="#58a6ff" stroke="#30363d" stroke-width="1.5"/>
<text x="534" y="154" font-size="10.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">事實查核</text>
<text x="534" y="178" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 40 系 Tensor 解鎖</text>
<text x="534" y="200" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">對象：4 個 Ada ID</text>
<text x="534" y="222" font-size="11.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">關鍵數字：指令率 2×、GEMM +12～34%</text>
<path d="M 534 234 L 930 234" fill="none" stroke="#30363d" stroke-width="1.2"/>
<text x="534" y="256" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">「全系列」不成立；FP8 幾乎沒變</text>
<text x="534" y="276" font-size="11" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 讀這篇</text>
<rect x="48" y="300" width="440" height="160" rx="12" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<rect x="48" y="300" width="6" height="160" rx="3" fill="#2dd4bf" stroke="#30363d" stroke-width="1.5"/>
<text x="70" y="328" font-size="10.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">操作筆記</text>
<text x="70" y="352" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 3080 12GB</text>
<text x="70" y="374" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">對象：10de:220a</text>
<text x="70" y="396" font-size="11.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">關鍵數字：FP16 +69%、BF16 +73%</text>
<path d="M 70 408 L 466 408" fill="none" stroke="#30363d" stroke-width="1.2"/>
<text x="70" y="430" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只吃 FP16／BF16 矩陣乘法</text>
<text x="70" y="450" font-size="11" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 讀這篇</text>
<rect x="512" y="300" width="440" height="160" rx="12" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<rect x="512" y="300" width="6" height="160" rx="3" fill="#2dd4bf" stroke="#30363d" stroke-width="1.5"/>
<text x="534" y="328" font-size="10.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">操作筆記</text>
<text x="534" y="352" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 4090</text>
<text x="534" y="374" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">對象：10de:2684</text>
<text x="534" y="396" font-size="11.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">關鍵數字：指令率 1.998×</text>
<path d="M 534 408 L 930 408" fill="none" stroke="#30363d" stroke-width="1.2"/>
<text x="534" y="430" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不用實驗旗標；量化權重吃不到</text>
<text x="534" y="450" font-size="11" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 讀這篇</text>
<rect x="48" y="474" width="904" height="116" rx="12" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<rect x="48" y="474" width="6" height="116" rx="3" fill="#f472b6" stroke="#30363d" stroke-width="1.5"/>
<text x="70" y="502" font-size="10.5" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">事實查核 · 2026-10-27 新增</text>
<text x="70" y="526" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 50 系 Blackwell 解鎖</text>
<text x="70" y="548" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">對象：Blackwell 全系（GB20x）　·　關鍵數字：fmla32 = 3（1/8 速），主機寫入被丟棄</text>
<path d="M 70 560 L 930 560" fill="none" stroke="#30363d" stroke-width="1.2"/>
<text x="70" y="580" font-size="11.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">維護者 2026-10-26 公開回覆「The short answer is no」——不是「還沒人做」，是「寫不進去」</text>
<rect x="48" y="606" width="904" height="92" rx="10" fill="#1c2230" stroke="#fbbf2455" stroke-width="1.5"/>
<text x="68" y="632" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">五篇的共同結論：解鎖是真的，媒體的關鍵字是假的。</text>
<text x="68" y="654" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">① 「全系列」不成立——白名單只有少數型號；連下一代（Blackwell）都解不動</text>
<text x="68" y="672" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">② 「翻倍」是指令發射率；真實 GEMM 只有 +12～81%</text>
<text x="68" y="690" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">③ 「所有 AI 負載都變快」不成立——INT8／4-bit／3-bit 量化完全沒變</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：五篇文章速查——兩篇事實查核負責「打破關鍵字」，兩篇操作筆記負責「照著做」，第五篇解釋為什麼下一代解不動。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG2 -->


## ① 事實查核 · RTX 30 系 gpu-unlock

![RTX 30 系 gpu-unlock 事實查核](/img/covers/rtx30-gpu-unlock-ampere-fact-check.png)

**→ [讀這篇](/2026/10/25/rtx30-gpu-unlock-ampere-fact-check/)**

查核對象是上游 [Zagitta/gpu-unlock](https://github.com/Zagitta/gpu-unlock)（4.3k stars、79 個 open issues、數十份使用者相容性報告）。

- **成立**：漏洞機制描述精準到寄存器級別；3090 Ti 的 BF16 87 → 157 TFLOPS 數字逐字正確；prefill 受惠、decode 因記憶體頻寬不變——全都對
- **不成立**：「一律翻倍」——同一張 3090 Ti 上 BF16 +80%、TF32 +94%，**FP16 只有 +35%**；各型號增益落在 **+25～81%**
- **兩個例外**：RTX 3070 Ti 從未用這個模組測過；RTX 3080 Ti 20GB OEM「解鎖成功但 BF16 維持半速」

## ② 事實查核 · RTX 40 系 Tensor 解鎖

![RTX 40 系 Tensor 解鎖事實查核](/img/covers/rtx40-tensor-unlock-fact-check.png)

**→ [讀這篇](/2026/10/25/rtx40-tensor-unlock-fact-check/)**

查核對象是 [JustAResearcher/gpu-unlock-ada](https://github.com/JustAResearcher/gpu-unlock-ada) v1.1.1。

- **成立**：不是超頻、不是刷 BIOS、不是改驅動；「全系列」與「Windows 一鍵可用」不成立
- **最關鍵的一個數字**：指令發射率確實 2×，但**真實 cuBLAS GEMM 只有 +12～34%**，而 4096³ BF16 是 **0.995×**（等於沒變）
- **FP8 幾乎沒動**：專案自己公布 +0.3%——**媒體說的「大幅提升」，是二手報導自己加戲**

## ③ 操作筆記 · RTX 3080 12GB

![RTX 3080 12GB 解除 gpu-unlock 操作筆記](/img/covers/rtx3080-12gb-gpu-unlock-guide.png)

**→ [讀這篇](/2026/10/25/rtx3080-12gb-gpu-unlock-guide/)**

Ampere 路徑的完整動手流程：確認 PCI ID（`10de:220a`）→ 安裝 → 設定核心命令列 → **冷開機** → 驗證 `gpu_unlock: unlocked` → 配對量測。

- **有同型號的完整實測**（Issue #62）：FP16 +69%、BF16 +73%、TF32 +68%
- **上游 README 漏列了這張卡**（`220a` 在整份 README 出現 0 次）
- **一份可直接跑的 torch/cuBLAS 量測腳本**，以及 7 筆常見坑（都附 issue 編號）

## ④ 操作筆記 · RTX 4090

![RTX 4090 解除 gpu-unlock 操作筆記](/img/covers/rtx4090-gpu-unlock-guide.png)

**→ [讀這篇](/2026/10/25/rtx4090-gpu-unlock-guide/)**

Ada 路徑的完整動手流程。**4090 是整個生態系裡最簡單、最有保障的一條路**：

- 唯一**不需要實驗旗標**的目標，只要 `gpu_unlock.targets=<位址>`
- 證據鏈最完整：獨立配對實測、六組種子數值驗證、時脈／溫度／功耗遙測
- 有真正能讀回驗證的工具：`tools/read_sm_rates.py` 讀出 `fmla32` 從 `1`（半速）變 `0`（全速）
- **但**：量化權重幾乎吃不到——Issue #17 的實測者用 3-bit MoE（IQ3_S）跑 8K prefill，比值是 **0.983×**

## ⑤ 事實查核 · RTX 50 系 Blackwell 解鎖

![RTX 50 系 Blackwell 解鎖事實查核](/img/covers/rtx50-blackwell-unlock-fact-check.png)

**→ [讀這篇](/2026/10/27/rtx50-blackwell-unlock-fact-check/)**

查核對象是「RTX 5090 破解方案應該很快出來，解鎖後 AI 算力可衝上 420 TFLOPS 以上」這則流傳說法。主要來源是 `gpu-unlock-ada` 的 [Issue #12「work on 5090?」](https://github.com/JustAResearcher/gpu-unlock-ada/issues/12) 全串 17 則留言。

- **結論：不是「還沒人做」，是「寫不進去」**——專案維護者 2026-10-26 親手關掉那串並回覆 *"The short answer is no"*：Blackwell 上暫存器還在 Ada 的同一組位址，但**主機寫進去的值會被丟棄**，速率改由**熔絲**決定
- **「420 TFLOPS」是推算，不是測得**：419 是白皮書的 **FP16 累加**峰值，GeForce 被限速的 **FP32 累加**只有 209.5；而就算解鎖成功，實測也只有 324.6
- **這次不是半速，是八分之一速**：`fmla32` 的速率編碼在 Ada 是 1（1/2 速），在 Blackwell 是 **3（1/8 速）**，連 Ada 沒有限速的 `imla1` 也被鎖住
- **連機制都換了**：從 Hopper 起 Falcon 讓位給 FSP，消費級 Blackwell 完全不用 Falcon——為 Falcon 設計的 exploit 前提直接消失
- **而且閘門關著還不夠**：Blackwell 連 `booter_load` 檔都沒有，開源模組對它的 booter 函式是回傳 NULL 的 stub
- **風險不同**：在 Blackwell 碰熔絲，**卡會 refuse to post**（開不了機），不是像 Ada 那樣「寫了沒反應」

## 五篇的共同結論（速查表）

| 流傳說法 | 較準確的說法 | 出處 |
| --- | --- | --- |
| 「RTX 40／30 全系列都能解鎖」 | 白名單只有少數型號：Ada 版 4 個 ID、Ampere 版數十個 GA10x ID；**連下一代（Blackwell）都解不動** | ①②⑤ |
| 「Tensor 算力翻倍」 | 翻倍的是**指令發射率**；真實 cuBLAS GEMM 只有 +12～81%，某些形狀等於沒變 | ①② |
| 「RTX 5090 解鎖後 AI 算力可衝上 420 TFLOPS」 | 419 是白皮書的 **FP16 累加**峰值，FP32 累加只有 209.5；而且 Blackwell 的 FP32 累加被鎖成 **1/8 速**，主機寫入會被丟棄 | ⑤ |
| 「所有 AI 工作負載都變快」 | INT8、unsigned INT4、`dp4a`、純 FP32 完全不變；**量化權重（4-bit／3-bit）也吃不到** | ①②③④ |
| 「LLM 生成變快」 | 只有 **prefill** 變快；**逐 token 生成**受記憶體頻寬瓶頸限制，幾乎不變 | ①②③④ |
| 「Windows 一鍵可用」 | 兩個彼此獨立的單板型實驗，都不通用、都需手動組裝 | ①② |
| 「Turing 世代沒人做過」 | 2026 年 10 月下旬出了**兩條彼此獨立的實作**：`nlzy/turing-unlock` 與 `KohakuBlueleaf/KohakUnlock`，各自在自己的硬體上驗證過 | ①⑤ |
| 「這是假的／陰謀論」 | 是真的開源專案：原始碼、雜湊固定的韌體資產、配對實測、數值驗證、公開的限制聲明都齊備 | ①②⑤ |
| 「更新驅動不用補丁，所以很安全」 | 驅動不用改，但韌體資產釘在 610.43.03；而且 **NVIDIA 有強烈動機修掉這個漏洞** | ②③④⑤ |

## 風險與界線（五篇共通）

這些操作的共同前提，讀完任何一篇都應該記住：

- **這是對 GPU 安全處理器的未授權程式碼執行**（緩衝區溢位 + ROP），跑的是自製 payload，和 NVIDIA 簽章韌體共用同一顆 GPU。
- **沒有保固。** 上游寫的是 *"Boot failure, loss of display, data corruption, hardware damage and other losses are possible. It is provided AS IS without warranty."*
- **交易沒收尾時要完全斷電**，不能 `rmmod`。上游：模組會保留韌體可能仍在使用的 DMA 緩衝區，直到下次關機。
- **上游沒有做過長期穩定性測試**，也沒有涵蓋遊戲、ComfyUI、hibernate resume。
- **上游的文件與程式碼註解會不同步**（例如 Ada 版 `arch_610.h` 的 AD106 註解曾長期寫著 `untested on silicon`，但 `docs/` 已有實測報告）。引用時以 `docs/` 為準並註明版本。
- **NVIDIA 有強烈動機修掉這個漏洞**（它打的正是已簽章 booter 的溢位）。「更新驅動不用重打補丁」是站在短期使用的角度；長期來看這個方案可能被上游改動作廢。
- **授權條款也是紅燈。** NVIDIA GeForce 驅動程式授權條款第 2.6 條明文禁止 *"bypass, disable, or circumvent any technical limitation… in the SOFTWARE"*。這些工具在驅動程式載入前執行，**算不算 circumvent 沒有任何判例或官方說明**；截至 2026-10-27，NVIDIA 未對這批開源專案公開表態。
- **新一代的失敗模式完全不同。** 在 Ada／Ampere 上寫錯暫存器，頂多是「沒解鎖」；在 **Blackwell 上碰熔絲，卡會 refuse to post（開不了機）**——而且那條路至今連公開工具都沒有。
- **功耗的兩種口徑都要看。** 配對實測的「最大取樣功耗」幾乎沒變（307.67 → 308.59 W），但媒體引用的**峰值功耗**是 313 → 346 W；前者不代表板載峰值與長期散熱，Turing 分支的 README 也直接寫著全速 Tensor 核心可能損壞硬件。

**共同建議**：先在一台你隨時可以重裝的機器上做，保留一個未修改的開機項，不要拿主力機或商用 SLA 主機先試。

## 一手來源

| 來源 | 用途 |
| --- | --- |
| [Zagitta/gpu-unlock](https://github.com/Zagitta/gpu-unlock) | Ampere 上游（v1.0.0） |
| [JustAResearcher/gpu-unlock-ada](https://github.com/JustAResearcher/gpu-unlock-ada) | Ada 版（v1.1.1） |
| [docs/How Ampere was unlocked.md](https://github.com/Zagitta/gpu-unlock/blob/main/docs/How%20Ampere%20was%20unlocked.md) | 漏洞機制完整分析（緩衝區溢位、ROP、PLM 遮罩位元、SS0／SS1 編碼） |
| [docs/evidence/rtx4090-pr1-matched](https://github.com/JustAResearcher/gpu-unlock-ada/tree/main/docs/evidence/rtx4090-pr1-matched) | 4090 配對實測（指令率、GEMM、遙測、暖開機重複測試） |
| [docs/testing.md](https://github.com/JustAResearcher/gpu-unlock-ada/blob/main/docs/testing.md) | 三層驗證分級定義 |
| [TOTORONG/AD103_win_unlocker](https://huggingface.co/TOTORONG/AD103_win_unlocker) | Windows UEFI 實驗（改裝 32 GB 的非 SUPER 4080） |
| [impacifist/Windows-GPU-UNLOCK](https://github.com/impacifist/Windows-GPU-UNLOCK) | Windows 路線（目前只有 3090 FE 與 3070 Ti 兩個硬體驗證 profile） |
| [TensorFlow #24531](https://github.com/tensorflow/tensorflow/issues/24531) | 2018 年 Turing 半速限制的原始佐證 |
| [gpu-unlock-ada Issue #12「work on 5090?」](https://github.com/JustAResearcher/gpu-unlock-ada/issues/12) | Blackwell 的完整偵察與結論（17 則留言，本專題第 5 篇的主要來源） |
| [nlzy/turing-unlock](https://github.com/nlzy/turing-unlock) | Turing 世代的一條獨立實作（2026-10-24） |
| [KohakuBlueleaf/KohakUnlock](https://github.com/KohakuBlueleaf/KohakUnlock) | Turing 世代的另一條獨立實作（2026-10-25），兼 `mmapeak` 全零輸入缺陷的揭露者 |
| [NVIDIA 開源核心模組](https://github.com/NVIDIA/open-gpu-kernel-modules) | `ctrl2080gr.h` 的速率編碼定義（0／1／2／3） |
| [Linux 核心文件 · FSP](https://docs.kernel.org/gpu/nova/core/fsp.html) | FSP 取代 Falcon 作為根信任的架構事實 |
| [NVIDIA GeForce 授權條款](https://www.nvidia.com/en-us/drivers/geforce-license/) | 第 2.6 條「bypass, disable, or circumvent」原文 |

## 相關延伸

- [用 Local GPU 做機器學習 學習筆記](/local-gpu-ml-notes/)——驅動、CUDA、cuDNN、PyTorch 的完整安裝筆記（本專題的操作都建立在這套環境上）
- [comfyui-nvidia-vfx-nodes-benchmark](/2026/10/15/comfyui-nvidia-vfx-nodes-benchmark/)——同一種「基準測試要量到端到端」的教訓：純 GPU 快 755 倍，端到端只有 1.24 倍
- [AI Stack 自動更新管線](/2026/10/21/ai-stack-auto-update-pipeline/)——本機 GPU 環境的維護流程
