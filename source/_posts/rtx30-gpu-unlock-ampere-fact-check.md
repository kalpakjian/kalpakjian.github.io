---
title: RTX 30 系 gpu-unlock 事實查核：漏洞是真的，但「翻倍」與「全系列」都不成立
date: 2026-10-25 18:20:00
categories:
  - AI 研究追蹤
tags:
  - 事實查核
  - 白話解說
  - GPU
  - NVIDIA
  - RTX
  - CUDA
  - 開源
  - 實測
  - 效能實測
  - 基準測試
  - Linux
  - Windows
  - 深度學習
hide_from_home: true
toc: true
index_img: /img/covers/rtx30-gpu-unlock-ampere-fact-check.png
banner_img: /img/covers/rtx30-gpu-unlock-ampere-fact-check.png
---

![RTX 30 系 gpu-unlock 事實查核](/img/covers/rtx30-gpu-unlock-ampere-fact-check.png)

> <strong>整理說明</strong>：本文是對「RTX 30 系顯示卡被 NVIDIA 鎖住一半的 AI 運算效能，現在被開源社群解放了」這則流傳說法的查核。查核對象是 GitHub 開源專案 <a href="https://github.com/Zagitta/gpu-unlock">Zagitta/gpu-unlock</a>（4.3k stars）與其技術文件 <code>docs/How Ampere was unlocked.md</code>。所有數字都取自一手來源：專案的 README、原始碼、文件、數十份使用者相容性報告，以及 GitHub Issues／PR 清單，不採用二手轉述。

<!-- more -->

## 一句話總結

> 這是**真實而且技術含量很高**的研究路線——它利用的是**已簽章 NVIDIA 開機韌體的一個緩衝區溢位漏洞**，用 ROP 堆出任意程式碼執行，再把限制張量的「速率選擇器」改寫成專業卡的全速檔位。所有數字都來自實測，連「這不是超頻、不是刷 BIOS、不是改驅動」這種關鍵澄清都對得上。
>
> 但「**一律翻倍**」與「**只有 3060／3070／3080／3090**」這兩句不成立：同一張 RTX 3090 Ti 上，BF16 增幅 +80%、TF32 +94%，**FP16 只有 +35%**；各型號的實測增益落在 **+25% ～ +81%** 之間；而且 **RTX 3070 Ti 從未被這個模組測過**、**RTX 3080 Ti 20GB OEM 解鎖後 BF16 仍維持半速**。

## 用一個比喻講清楚

### 比喻一：這不是「改車」，是「改回出厂時被寫死的檔位」

你的 RTX 3090 是一台引擎很猛的车，但出廠時，行控器裡被寫死一條規則：**Tensor 那條線最多只能跑半速**。專業卡（RTX A 系列）沒有這條規則，售價是數倍起跳。

這個專案做的事，等同於有人研究出**怎麼把行控器裡那條規則改掉**——而且他公開了原始碼、韌體產生流程、完整的漏洞分析文件，以及數十份使用者的實測報告。在消費級硬體上，這種透明程度非常少見。

**但「規則拿掉了」不等於「車從 60 變 200」。**

- 車子的**極限**（引擎排氣量、變速箱齒比、輪胎抓地力）都沒變。
- 而且這次連「極限」都沒變——被改掉的是「引擎的檔位」，不是「引擎本身」。
- 同一台車上，**不同檔位的解鎖效果還不一樣**：有的是全速檔被推開，有的只推開一半。

### 比喻二：門確實打開了，但每種鑰匙開不同的房間

「解鎖」聽起來像「一鍵全開」，實際上更像**打開一棟大樓的總開關，但每個房間的線路不一樣**：

- **同一台 3090 Ti**，BF16 房間的燈全亮了（+80%），TF32 房間也全亮（+94%），但 FP16 房間只亮了一半（+35%）。
- **不同型號**，增益可以差三倍：RTX 3070 約 +73～81%，RTX 3090 只有 +25～67%。
- **有些門根本沒開**：RTX 3070 Ti 從未被這個模組測過；RTX 3080 Ti 20GB OEM 的交易會跑完，但 BF16 燈還是不亮。

### 比喻三：這是利用「門鎖本身的漏洞」

白話說清楚機制——

GPU 開機時有個流程：驅動把加密的韌體交給 GPU 裡的一顆安全處理器（SEC2），SEC2 驗簽、解密、然後在 GSP 上執行。這一整套設計本來是安全的。

但**那顆安全處理器上跑的開機程式（booter）有一個典型的緩衝區溢位**——溢位直接寫進堆疊（stack），攻擊者就能用**ROP（Return-Oriented Programming，把現成指令片段串成任意程式碼）**取得控制流。

拿到控制流之後只做一件事：**把寫入保護的遮罩打開**。原廠預設 `FEAT_OVR_PLM = 0xffffff8f`，其中 `[7:4] = 1000` 表示「只有最高權限層可以寫」，其餘三層全被擋。既然我們已經在最高權限層裡了，把這個值寫成 `0xFFFFFFFF`，速率選擇器就變成驅動程式可以寫了。

> <strong>一句話總結這個比喻</strong>：這不是「破解防盜鎖」的神話，而是「研究出正確的初始化順序，並且把每一步都做成可驗證的」。而且它<b>確實是未授權的程式碼執行</b>——性質比一般驅動 hack 重一級。

## 事實核對速查表

| 流傳說法 | 較準確的說法 | 評估 |
| --- | --- | --- |
| 「把 RTX 30 被鎖一半的 AI 運算效能完整解放出來」 | 解鎖的是 **FP/BF16 FMA 進 FP32 累加**的指令發射率；不是所有運算路徑 | 方向正確，範圍需收斂 |
| 「這不是超頻」 | ✓ 改的是 speed selector 暫存器，不是時脈；專案全程不動功耗上限 | 正確 |
| 「不是刷 BIOS」 | ✓ README：*"It is neither a UEFI application nor a patched NVIDIA driver."* | 正確 |
| 「不是修改驅動程式」 | ✓ 模組在 **initramfs** 裡、於 NVIDIA 驅動綁卡**之前**執行，之後 FLR 再交還 | 正確 |
| 「利用一個已知的漏洞，先把保護暫存器的寫入限制打開」 | ✓ 完全正確：已簽章 booter 的**緩衝區溢位 + ROP**，寫 `FEAT_OVR_PLM = 0xFFFFFFFF` 解除 `SS0/SS1` 的寫入保護 | 精準到寄存器級別 |
| 「RTX 3090 Ti 的 BF16 從 87 TFLOPS 提升到 157 TFLOPS」 | ✓ **數字逐字正確**（87.50 → 157.41，8192³ dense GEMM，450 W，五次取樣中位數） | 正確 |
| 「效能可以差一倍」 | 同一張 3090 Ti 上 **BF16 +80%、TF32 +94%、FP16 只有 +35%**；各型號增益落在 **+25% ～ +81%** | 過度概括 |
| 「只支援 RTX 3060、3070、3080、3090」 | 模組實際接受 `main.c` 裡所有 GA102／GA103／GA104／GA106 ID（數十個）；另有 **RTX 3070 Ti 未測**、**RTX 3080 Ti 20GB OEM 解鎖後仍半速**兩個例外 | 過度簡化 |
| 「只支援 Linux」 | 這個 **kmod** 只支援 Linux；但同一個 exploit 有 **Windows UEFI 實作**，且已有 3070 Ti、3060／3080 Ti 筆電的使用者回報成功 | 需補註 |
| 「遊戲不會變快」 | ✓ 改的是張量指令發射率，遊戲不走這條路徑 | 正確 |
| 「LLM 生成文字因為瓶頸在記憶體頻寬，速度幾乎不變」 | ✓ README 原文：*"LLM decode, which is limited by memory bandwidth, and INT8 work stay about the same."* Issue #25 實測 vLLM prefill +33%、decode flat | 正確 |
| 「Turing 也有類似的鎖，社群有人提出支援請求」 | ✓ 有請求（Issue #30、#97、#64），但**沒有任何 Turing 實作 PR**，且 Turing 沒有 BF16 | 正確（但缺關鍵差異） |

---

## 漏洞利用鏈：六步

上游文件 `docs/How Ampere was unlocked.md` 把整條鏈寫得很完整，甚至附了 mermaid 流程圖：

<!-- FIG3 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 520" role="img" aria-label="gpu-unlock 的漏洞利用鏈：已簽章 booter 的緩衝區溢位 → ROP → 解除 FEAT_OVR_PLM 寫入保護 → 寫入 SS0/SS1 速率選擇器 → PCIe FLR → 未修改的驅動綁定" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="998.5" height="518.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">漏洞利用的六步</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全部發生在 NVIDIA 驅動載入之前</text>
<rect x="48" y="132" width="236" height="96" rx="12" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<circle cx="78" cy="162" r="16" fill="#58a6ff" opacity="0.92"/>
<text x="78" y="167.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<text x="106" y="168" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">驅動載入韌體</text>
<text x="64" y="200" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">SEC2 驗簽並啟動 GSP-RM</text>
<rect x="284" y="132" width="236" height="96" rx="12" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="314" cy="162" r="16" fill="#f472b6" opacity="0.92"/>
<text x="314" y="167.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text>
<text x="342" y="168" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Booter 緩衝區溢位</text>
<text x="300" y="200" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">已簽章韌體的 stack overflow</text>
<rect x="520" y="132" width="236" height="96" rx="12" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="550" cy="162" r="16" fill="#f472b6" opacity="0.92"/>
<text x="550" y="167.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text>
<text x="578" y="168" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ROP 取得控制流</text>
<text x="536" y="200" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">以 ROP 堆疊執行任意程式碼</text>
<rect x="520" y="296" width="236" height="96" rx="12" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<circle cx="550" cy="326" r="16" fill="#fbbf24" opacity="0.92"/>
<text x="550" y="331.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<text x="578" y="332" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">解除寫入保護</text>
<text x="536" y="364" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FEAT_OVR_PLM = 0xFFFFFFFF</text>
<rect x="284" y="296" width="236" height="96" rx="12" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<circle cx="314" cy="326" r="16" fill="#2dd4bf" opacity="0.92"/>
<text x="314" y="331.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text>
<text x="342" y="332" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">寫入速率選擇器</text>
<text x="300" y="364" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">SS0 = 0x88888888 / SS1 = 0x8</text>
<rect x="48" y="296" width="236" height="96" rx="12" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<circle cx="78" cy="326" r="16" fill="#3fb950" opacity="0.92"/>
<text x="78" y="331.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text>
<text x="106" y="332" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FLR 後交還</text>
<text x="64" y="364" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">未修改的 nvidia 驅動正常綁定</text>
<path d="M 284 180.0 L 280 180.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 520 180.0 L 516 180.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 638.0 228 L 638.0 292" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 516 344.0 L 520 344.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 280 344.0 L 284 344.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="422" width="904" height="62" rx="10" fill="#1c2230" stroke="#f472b655" stroke-width="1.5"/>
<text x="68" y="448" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">這是對 GPU 安全處理器的未授權程式碼執行（緩衝區溢位 + ROP），性質比一般驅動 hack 重一級。</text>
<text x="68" y="470" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">上游 README 也寫明：若卡上的韌體沒停下來，模組會保留韌體可能仍在使用的 DMA 緩衝區，必須完全斷電。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 3：從開機韌體的緩衝區溢位到全速選擇器的六步——ROP 取得控制流後，只要寫 0xFFFFFFFF 就能解除 SS0/SS1 的寫入保護。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG3 -->


技術重點整理：

| 項目 | 內容 |
| --- | --- |
| 出發點 | 已簽章 NVIDIA **booter 的緩衝區溢位**，溢位寫進 stack → 可用 **ROP** 取得控制流 |
| 速率選擇器 | `FEAT_OVR_SM_SPD`（SS0）@ `0x0082381c`：8 個 4-bit 欄位；`FEAT_OVR_SM_SPD_1`（SS1）@ `0x00823820`：1 個 4-bit 欄位（IMLA4） |
| 欄位編碼 | bit3 = override enabled；bits2:0 = 速度選擇（`00` = full rate、`01` = 1/2 rate、`10` = 1/4、`11` = 1/8，後兩者未經確認） |
| 原廠預設值 | SS0 = `0x00000001`、SS1 = `0x00000001`（即「半速」） |
| 寫入保護 | `FEAT_OVR_PLM` @ `0x00823804`，GA100／GA102 預設 `0xffffff8f`；`[3:0]` = READ_PROTECTION、`[7:4]` = WRITE_PROTECTION、`[23:8]` = SOURCE_ENABLE |
| 為什麼寫不進去 | 讀 `0x8f` → `[7:4] = 1000`：**只有 L3（heavy-secure 內容）可寫**，L0／L1／L2 全被擋 |
| 解法 | 在 ROP 裡寫 `FEAT_OVR_PLM = 0xFFFFFFFF`，SS0/SS1 立刻變成驅動程式可寫 |
| 目標值 | SS0 = `0x88888888`（8 個欄位全開）、SS1 = `0x8` |
| 收尾 | PCIe **FLR**（功能層級重置），讓未修改的 NVIDIA 驅動接手乾淨的卡 |
| 先驅 | `amoghmunikote/cmpunlocker`（把 8／10 GB 的 CMP 170HX 解鎖成 64／40 GB），曾被 LTT 報導 |

README 還補了一句很關鍵的話：這個做法**不需要**每次 NVIDIA 出新驅動就手動打補丁——因為模組跑在驅動之前，驅動本身完全沒被動過。

## 實測數據：不是一律翻倍

### 同一張 RTX 3090 Ti，三種精度三種命運

README 開頭那張表是整個專案最常被引用的數據（3090 Ti、8192³ dense GEMM、450 W、五次取樣中位數、FP32 累加）：

<!-- FIG1 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" role="img" aria-label="RTX 3090 Ti 三種精度解鎖前後對比：BF16 +80%、TF32 +94%，但 FP16 只有 +35%" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="998.5" height="498.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不是一律兩倍</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一張 3090 Ti，8192³ dense GEMM、450 W</text>
<rect x="250" y="126" width="22" height="12" rx="3" fill="#7d85902e" stroke="#7d859088" stroke-width="1"/>
<text x="282" y="136" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">解鎖前（stock）</text>
<rect x="400" y="126" width="22" height="12" rx="3" fill="#2dd4bf66" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="432" y="136" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">解鎖後</text>
<text x="870" y="136" font-size="11" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">（TF/s）</text>
<text x="228" y="187" font-size="14" fill="#58a6ff" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FP16</text>
<rect x="250" y="170" width="318.9717647058823" height="24" rx="8" fill="#7d85902e" stroke="#7d859088" stroke-width="1"/>
<text x="578.9717647058824" y="187" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">87.5</text>
<rect x="250" y="198" width="431.7752941176471" height="22" rx="7" fill="#58a6ff66" stroke="#58a6ff" stroke-width="1.5"/>
<text x="691.775294117647" y="214" font-size="13" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">118.4</text>
<text x="743.775294117647" y="214" font-size="13" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+35%</text>
<text x="228" y="253" font-size="14" fill="#2dd4bf" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">BF16</text>
<rect x="250" y="236" width="319.11764705882354" height="24" rx="8" fill="#7d85902e" stroke="#7d859088" stroke-width="1"/>
<text x="579.1176470588235" y="253" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">87.5</text>
<rect x="250" y="264" width="574.0835294117647" height="22" rx="7" fill="#2dd4bf66" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="834.0835294117647" y="280" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">157.4</text>
<text x="886.0835294117647" y="280" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+80%</text>
<text x="228" y="319" font-size="14" fill="#c084fc" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">TF32</text>
<rect x="250" y="302" width="155.29176470588234" height="24" rx="8" fill="#7d85902e" stroke="#7d859088" stroke-width="1"/>
<text x="415.2917647058823" y="319" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">42.6</text>
<rect x="250" y="330" width="301.2835294117647" height="22" rx="7" fill="#c084fc66" stroke="#c084fc" stroke-width="1.5"/>
<text x="561.2835294117647" y="346" font-size="13" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">82.6</text>
<text x="613.2835294117647" y="346" font-size="13" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+94%</text>
<path d="M 250 158 L 250 342" fill="none" stroke="#7d8590" stroke-width="1.5"/>
<text x="250.0" y="368" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<text x="432.3529411764706" y="368" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">50</text>
<text x="614.7058823529412" y="368" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">100</text>
<text x="797.0588235294117" y="368" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">150</text>
<rect x="48" y="388" width="904" height="84" rx="10" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="68" y="416" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">BF16 +80%、TF32 +94%，但 FP16 只有 +35%。解鎖不是把每種精度都拉滿，</text>
<text x="68" y="438" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">而是把每一種精度各自拉到「等效專業卡」的位置——所以別說「一律翻倍」。</text>
<text x="68" y="460" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">資料來源：README「3090 Ti dense 8192³ GEMM at 450 W, five-sample medians with FP32 accumulation」。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：同一張 RTX 3090 Ti 的三種精度——BF16 87.5→157.4、TF32 42.6→82.6，但 FP16 只從 87.5 到 118.4。解鎖不是把每種精度都拉滿。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG1 -->


**這是整篇文章最需要拆開的地方。** 流傳版本只引用了 BF16 那一列（87 → 157，確實接近翻倍），但同一張卡上：

- **BF16：87.50 → 157.41 TFLOPS（+80%）**
- **TF32：42.58 → 82.61 TFLOPS（+94%）**
- **FP16：87.46 → 118.39 TFLOPS（+35%）**

> <strong>白話說</strong>：解鎖不是把每一種精度都拉到滿，而是把每一種精度拉到「它對應的等效專業卡」的位置。FP16 之所以只快三成多，是因為它在這條路徑上的等效專業卡本來就比 BF16 低——**打開的是同一道門，但門後面房間的電容量不同**。

### 各型號的實測增益區間

README 的「Tested cards」表把每張卡的使用者回報整理成區間。**其中 RTX 3080 12GB 是本文從 Issue #62 補進來的**——上游 README 至今沒有列這一張卡（`220a` 在整份 README 出現 0 次），但那份回報本身相當完整：

<!-- FIG2 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 680" role="img" aria-label="各型號 BF16 GEMM 增益範圍 +25% 到 +81%，以及 3070 Ti 未測、3080 Ti 維持半速兩個例外" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="998.5" height="678.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">各型號的增益區間</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">區間來自各使用者自己的量測，功耗上限差異很大</text>
<path d="M 300 148 L 300 546" fill="none" stroke="#7d8590" stroke-width="1.5"/>
<text x="780" y="126" font-size="12" fill="#2dd4bf" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">BF16 GEMM 增益</text>
<text x="276" y="173" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 3070</text>
<text x="276" y="188" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GA104・已解鎖</text>
<rect x="300" y="158" width="480" height="22" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="650.4" y="158" width="38.400000000000034" height="22" rx="8" fill="#2dd4bf66" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="700.8" y="174" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+73–81%</text>
<text x="276" y="217" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 3060 12GB</text>
<text x="276" y="232" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GA106・已解鎖</text>
<rect x="300" y="202" width="480" height="22" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="300" y="202" width="384.0" height="22" rx="8" fill="#2dd4bf33" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="696.0" y="218" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+80%</text>
<text x="276" y="261" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 3090 Ti</text>
<text x="276" y="276" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GA102・已解鎖</text>
<rect x="300" y="246" width="480" height="22" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="626.4" y="246" width="57.60000000000002" height="22" rx="8" fill="#2dd4bf66" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="696.0" y="262" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+68–80%</text>
<text x="276" y="305" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 3080 10GB</text>
<text x="276" y="320" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GA102・已解鎖</text>
<rect x="300" y="290" width="480" height="22" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="636.0" y="290" width="14.399999999999977" height="22" rx="8" fill="#2dd4bf66" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="662.4" y="306" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+70–73%</text>
<text x="276" y="349" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 3080 12GB</text>
<text x="276" y="364" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GA102・已解鎖</text>
<rect x="300" y="334" width="480" height="22" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="631.2" y="334" width="19.19999999999999" height="22" rx="8" fill="#2dd4bf66" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="662.4" y="350" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+69–73%</text>
<text x="276" y="393" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 3080 20GB</text>
<text x="276" y="408" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GA102・改裝 20GB</text>
<rect x="300" y="378" width="480" height="22" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="568.8" y="378" width="14.399999999999977" height="22" rx="8" fill="#2dd4bf66" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="595.2" y="394" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+56–59%</text>
<text x="276" y="437" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 3090</text>
<text x="276" y="452" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GA102・已解鎖</text>
<rect x="300" y="422" width="480" height="22" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="420.0" y="422" width="201.60000000000002" height="22" rx="8" fill="#2dd4bf66" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="633.6" y="438" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+25–67%</text>
<text x="276" y="481" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 3070 Ti</text>
<text x="276" y="496" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GA104・模組未測</text>
<rect x="300" y="472" width="46" height="3" rx="1" fill="#fbbf24" stroke="#30363d" stroke-width="1.5"/>
<text x="362" y="481" font-size="13" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">—</text>
<text x="276" y="525" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 3080 Ti 20GB</text>
<text x="276" y="540" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GA102・維持半速</text>
<rect x="300" y="516" width="46" height="3" rx="1" fill="#f472b6" stroke="#30363d" stroke-width="1.5"/>
<text x="362" y="525" font-size="13" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">—</text>
<text x="300.0" y="572" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0%</text>
<text x="420.0" y="572" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+25%</text>
<text x="540.0" y="572" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+50%</text>
<text x="660.0" y="572" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+75%</text>
<text x="780.0" y="572" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+100%</text>
<rect x="48" y="592" width="904" height="62" rx="10" fill="#1c2230" stroke="#fbbf2455" stroke-width="1.5"/>
<text x="68" y="618" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩個例外：RTX 3070 Ti 從未用這個模組測過（同樣的解鎖改用 Windows UEFI 埠成功）；</text>
<text x="68" y="640" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 3080 Ti 20GB OEM 的交易會跑完，但 BF16 仍維持半速——「成功」不等於「有效」。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：各型號的 BF16 GEMM 增益區間——RTX 3070 約 +73～81%，RTX 3090 只有 +25～67%（225 W 上限的卡）；另有兩個例外。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG2 -->

<!-- FIG2 |

Issue #62 的原始數據（技嘉 RTX 3080 12 GB、原廠未改、Arch、kernel 7.1.9、驅動 610.57.04 open、350 W 上限、8192³ dense GEMM、FP32 累加、五次取樣中位數）：

| 精度 | 解鎖前 | 解鎖後 | 增益 |
| --- | ---: | ---: | ---: |
| FP16 | 65.52 TFLOPS | 110.62 TFLOPS | **+69%** |
| BF16 | 65.63 TFLOPS | 113.24 TFLOPS | **+73%** |
| TF32 | 32.42 TFLOPS | 54.51 TFLOPS | **+68%** |

兩個例外特別值得記下：

- **RTX 3070 Ti（`10de:2482`）**：README 寫 *"Not tested with this module (the same unlock worked from a UEFI port on Windows)"*——**這個模組從未在 3070 Ti 上測過**。
- **RTX 3080 Ti 20GB OEM（GA102-250，`10de:2205`）**：Issue #28 回報 *"unlock completes, selector verified held at runtime, but **BF16 rate stays at half speed**"*——交易會成功結束、選擇器也確認寫進去了，**但速率就是沒上去**。這是最值得警惕的一種失敗：**看起來成功，其實沒用**。

另外 README 提醒：這些增益來自各使用者自己的量測，**彼此不可直接比較**，而且**功耗上限影響很大**——最低的 +25% 來自被壓在 225 W 的卡。

### 模組實際接受哪些卡

原始碼 `kernel/gpu_unlock/main.c` 的白名單遠比「四款」多：

| 晶片 | 接受的 PCI ID 數 | 備註 |
| --- | ---: | --- |
| GA102 | 12 | 含 3090 Ti／3090／3080 Ti／3080／3080 12G 等 |
| GA104 | 27 | 含 3070／3070 Ti／3060 Ti／3060 12G 等 |
| GA106 | 10 | 含 3060 12G／3050 等 |
| GA103 | 1（`0x2414`） | README：*"No reports yet"* |

而且 **PR #24 已經在加入 AD103（RTX 4080 SUPER）與 AD106（RTX 4060 Ti 8GB）**，Issue #87 實測 RTX 4070 Ti（`10de:2782`）可用、+83～84% GEMM。**這個專案已經不只是一個「Ampere 專案」了。**

## 工作負載：哪些變快、哪些不動

<!-- FIG4 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 570" role="img" aria-label="哪些工作負載受惠（prefill、FlashAttention、擴散模型）與哪些不動（decode、INT8、4-bit、遊戲）" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="998.5" height="568.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">受惠與不受惠</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">判準：有沒有在跑 FP16／BF16 乘、FP32 累加的矩陣乘法</text>
<rect x="48" y="126" width="440" height="374" rx="12" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<rect x="512" y="126" width="440" height="374" rx="12" fill="#1c2230" stroke="#7d859044" stroke-width="1.5"/>
<text x="68" y="156" font-size="15" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">會變快</text>
<text x="532" y="156" font-size="15" fill="#7d8590" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不會變快</text>
<rect x="64" y="176" width="408" height="62" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="80" y="202" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">LLM prefill</text>
<text x="80" y="224" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+14% ～ +66%（依卡與功耗上限）</text>
<rect x="64" y="254" width="408" height="62" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="80" y="280" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FlashAttention</text>
<text x="80" y="302" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+47% ～ +68%</text>
<rect x="64" y="332" width="408" height="62" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="80" y="358" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">擴散模型（圖片生成）</text>
<text x="80" y="380" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">明顯受惠</text>
<rect x="64" y="410" width="408" height="62" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="80" y="436" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">真實 GEMM 吞吐</text>
<text x="80" y="458" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">依型號 +25% ～ +81%</text>
<rect x="528" y="176" width="408" height="62" rx="10" fill="#161b22" stroke="#7d859055" stroke-width="1.5"/>
<text x="544" y="202" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">LLM decode（逐 token 生成）</text>
<text x="544" y="224" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">幾乎不變——瓶頸在記憶體頻寬</text>
<rect x="528" y="254" width="408" height="62" rx="10" fill="#161b22" stroke="#7d859055" stroke-width="1.5"/>
<text x="544" y="280" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">INT8 量化運算</text>
<text x="544" y="302" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">維持原狀</text>
<rect x="528" y="332" width="408" height="62" rx="10" fill="#161b22" stroke="#7d859055" stroke-width="1.5"/>
<text x="544" y="358" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4-bit 量化推論</text>
<text x="544" y="380" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">無增益</text>
<rect x="528" y="410" width="408" height="62" rx="10" fill="#161b22" stroke="#7d859055" stroke-width="1.5"/>
<text x="544" y="436" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">遊戲</text>
<text x="544" y="458" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不會變快</text>
<text x="48" y="524" font-size="13.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">判準只有一句：你的負載有沒有在跑「FP16／BF16 乘、FP32 累加」的矩陣乘法。</text>
<text x="48" y="548" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">有 → 受惠；瓶頸在記憶體頻寬或走 INT8／4-bit → 幾乎沒差。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 4：受惠與不受惠的工作負載分流——prefill 與 FlashAttention 明顯受惠，decode、INT8、4-bit 量化與遊戲幾乎沒差。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG4 -->


上游 README 的原話把界線畫得很清楚：

> Matrix-heavy work speeds up: **LLM prefill** (+14–66% in #9, #15, #25 and #33), **diffusion and FlashAttention**. **LLM decode, which is limited by memory bandwidth, and INT8 work stay about the same.** The reports that compared outputs found them **bit-identical** before and after.

幾個實測細節值得注意：

- **Issue #25**（RTX 3090）：vLLM prefill **+33%**、decode flat，並有 **8 小時混合負載穩定性**記錄。
- **Issue #60**（Lenovo 3060 12GB）：GEMM 約 2×、**FlashAttention +47～68%**、FP16 LLM prefill +44～53%，但 **Ollama 4-bit 完全沒有增益**。
- **Issue #75**：4× RTX 3090 的 LLM Inference vs LoRA Training 對照（240 W 與 350 W）。
- 多次回報都附上「輸出 bit-identical」的數值驗證。

> <strong>白話說</strong>：判準只有一句——**你的負載有沒有在跑「FP16／BF16 乘、FP32 累加」的矩陣乘法**。有 → 受惠；瓶頸在記憶體頻寬（逐 token 生成）或走 INT8／4-bit 量化 → 幾乎沒差。

## 風險：這一段流傳版本完全沒提

上游 README 對最壞情況寫得很直接：

> If the firmware on a card never stops, the module logs it and **keeps the DMA buffers that firmware may still use until the next power off. Power off before trying again.**

Issues 裡的失敗案例更值得看清楚：

| Issue | 症狀 |
| --- | --- |
| #23（已修） | *"unlock fails with -ETIMEDOUT on non-cold cards and **leaves GPUs unusable by nvidia**"* |
| #21（已修） | GA106（3060 LHR）解鎖失敗：-110，SEC2 unreachable（PRI `0xbadf5620`） |
| #67 | RTX 3060 Ti LHR：*"firmware load failed (-2)"* |
| #11 | initramfs 裡 `nvidia.ko` 比 `gpu_unlock` 先綁卡 → `-EBUSY`，解鎖失敗 |
| #54 | Debian 套件沒裝 dracut drop-in → Ubuntu 25.10+ 上模組根本不在 initramfs |
| #5 | 主機板韌體留著 bus mastering → 全部拒絕解鎖（Supermicro X11 尤其明顯） |
| #38（已修） | Thunderbolt 外接 3090 解鎖失敗 |

而且性質要講清楚：**這是對 GPU 安全處理器的未授權程式碼執行**（緩衝區溢位 + ROP），比一般驅動 hack 重一級。它執行的自製 payload 要與 NVIDIA 簽章韌體共存同一個 GPU，萬一交易沒收尾，後果不是「沒解鎖」而是「卡有問題」。

### 「更新驅動不用補丁」對，但有三個前提

README 原文：*"The benefit of this early kmod driver is that it does not require manual patching each time nvidia releases a new driver version."* ✓ 這句話成立，但：

1. **核心模組要隨核心版本重編**（DKMS 處理），每次核心更新都要重建 initramfs。
2. **NVIDIA 韌體資產釘在 `610.43.03`**（逐檔 SHA-256 檢核）；NVIDIA 改版資產就得重新產生。
3. **反過來說，這個 exploit 打的正是「已簽章 NVIDIA booter 的緩衝區溢位」——NVIDIA 有強烈動機修掉它。** 對用戶是方便，對方案的長期存續卻是風險。

換句話說：「不用每次都補丁」是站在**短期使用**的角度；站在**長期可用**的角度，同一個特性也是它的弱點。

### 什麼時候適合試

| 你的情況 | 建議 |
| --- | --- |
| **RTX 3090／3090 Ti／3080／3070／3060 12GB** | 有最多使用者回報（含 8 小時穩定性記錄），可在自己能還原的 Linux 主機上試 |
| **RTX 3070 Ti** | 這個模組**沒測過**；有使用者改用 Windows UEFI 埠成功（Issue #32） |
| **RTX 3080 Ti 20GB OEM** | 已知會「解鎖成功但維持半速」（Issue #28） |
| **想跑 LLM 推論服務** | 先確認你的負載吃 FP16／BF16 矩陣乘法；4-bit 量化（Ollama 等）**沒有增益**（Issue #60） |
| **拿主力機或商用 SLA 主機** | 不建議；上游有留下 GPU 對驅動不可用的案例 |

## Turing 的狀況：鎖是真的，但路徑不同

**「Turing 也有類似的鎖」這句話成立**，而且有 2018 年的原始佐證。TensorFlow issue #24531（2018-12）：

> The peak FP16 Tensor TFLOPS with FP32 Accumulate is only **43.6%** of NVIDIA Quadro RTX6000. This is very abnormal, **obviously an artificial limit**.

規格數字也對得上（NVIDIA 公布的光階梯）：RTX 2080 Ti 的 FP16 張量搭 FP32 累加是 **53.8 TFLOPS**，搭 FP16 累加是 **107.6**——整整一半；而 Quadro RTX 6000 兩種模式都是全速。**這正是「同一顆晶片、貼上不同的名字、效能差一倍」的原始版本。**

**但有兩個關鍵差異：**

1. **Turing 沒有 BF16、沒有 TF32、沒有 FP8**，也沒有結構化稀疏。它只有「FP16 搭 FP32 累加」這一個維度的半速。
2. **Ampere 這套機制不能直接套用**：`FEAT_OVR_PLM`、`SS0`、`SS1` 這組暫存器是 GA10x 的佈局，Turing 的開機流程與安全處理器架構不同。

**社群確實有請求**——Issue #30「Add turing support」、#97「support turing?」、#64「is there possibility for Nvidia 2000's cards」都還開著。但**目前沒有任何 Turing 實作 PR**：最新的相關 PR 是 #96（GA107 RTX 3050 Laptop）與 #82（AD107 RTX 4060 Laptop），都還在討論中。

所以正確的說法是：**「Turing 的鎖是真的，已經有人提出請求，但還沒有穩定可用的成果。」**

## 這件事跟 RTX 40 有什麼關係

有直接關係——[RTX 40 版的 `gpu-unlock-ada`](https://github.com/JustAResearcher/gpu-unlock-ada) 就是**從這個專案分支出來的**：

| 項目 | `gpu-unlock`（Ampere） | `gpu-unlock-ada`（Ada） |
| --- | --- | --- |
| Linux 模組與打包 | **原點** | 直接沿用 |
| GA102 V67 payload 鏈 | 來自 `WildFlash1st/cmp90hx-unlock` | 同樣沿用 |
| AD102 payload | — | 來自 `TOTORONG/AD103_win_unlocker`（Windows 實驗） |
| 白名單 | GA102／GA103／GA104／GA106 數十個 ID | 精簡到 4 個 Ada ID，且後兩者需實驗旗標 |
| 實測證據 | 數十份使用者相容性報告 | 配對實測報告 + 數值驗證 |

換句話說，**Ampere 版的證據鏈其實更完整**——它有 79 個 open issues、數十份使用者報告、連「解鎖成功但沒用」的失敗案例都公開記錄著。兩邊的取捨剛好相反：Ada 版把範圍收窄、證據做深；Ampere 版範圍放廣、靠社群眾包。

## 查核方法與可重現性

本文**沒有用搜尋摘要**，全部取自一手檔案（存於 `C:\Users\princ\.cache\gpu-unlock-ampere\`）：

| 來源 | 用途 |
| --- | --- |
| `README.md` | 型號表、3090 Ti 三種精度數字、增益區間、LLM prefill／decode 說明 |
| `docs/How Ampere was unlocked.md` | 漏洞機制：緩衝區溢位、ROP、PLM 遮罩位元、SS0／SS1 編碼 |
| `kernel/gpu_unlock/main.c` | 裝置 ID 白名單（GA102 12 個／GA104 27 個／GA106 10 個） |
| `firmware/NOTICE.md` | payload 來源與授權邊界 |
| GitHub Issues API（79 open） | #28（3080 Ti 半速）、#30／#97（Turing）、#25／#60（工作負載）、#11／#54／#5（失敗案例） |
| GitHub PR 清單（14 個） | #24（AD103／AD106）、#41（AD103，已關閉）、#96／#82（跨架構嘗試） |
| TensorFlow issue #24531 | Turing 的 FP32-累加半速佐證 |
| Flopper.io 規格頁 | RTX 2080 Ti 的 53.8／107.6 TFLOPS 對照與 Turing 無 BF16 的確認 |

## 參考資料

- 專案首頁：[github.com/Zagitta/gpu-unlock](https://github.com/Zagitta/gpu-unlock)（v1.0.0，4.3k stars）
- 漏洞分析：[docs/How Ampere was unlocked.md](https://github.com/Zagitta/gpu-unlock/blob/main/docs/How Ampere was unlocked.md)
- 相容性報告表：README 的 [Tested cards](https://github.com/Zagitta/gpu-unlock#tested-cards)
- 先驅專案：[amoghmunikote/cmpunlocker](https://github.com/amoghmunikote/cmpunlocker)
- Ada 版（本系列前篇）：[JustAResearcher/gpu-unlock-ada](https://github.com/JustAResearcher/gpu-unlock-ada)
- 改裝 4080 的 Windows 實驗：[TOTORONG/AD103_win_unlocker](https://huggingface.co/TOTORONG/AD103_win_unlocker)
- Turing 半速的原始討論：[tensorflow/tensorflow#24531](https://github.com/tensorflow/tensorflow/issues/24531)

---

> <strong>最後一話</strong>：值得肯定的不是「RTX 30 被破解」這種口號，而是這個專案把**原始碼、雜湊固定的韌體資產、完整的漏洞分析、以及數十份包含失敗案例的使用者回報**全部放出來了——連「我的實驗只覆蓋一張卡」「這不是應用程式加速」「某張卡解鎖成功但維持半速」這種對自己不利但誠實的句子。
>
> 媒體把這條技術路線壓縮成三個關鍵字，而那三個關鍵字一個都不成立。**研究是真的，標題是假的。**
