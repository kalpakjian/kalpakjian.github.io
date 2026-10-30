---
title: RTX 50 系 Blackwell 解鎖事實查核：暫存器還在、寫不進去 —— 「5090 解鎖後 420 TFLOPS」是怎麼來的
date: 2026-10-27 09:30:00
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
  - 深度學習
hide_from_home: true   # 專題子頁：不列首頁（歸檔／分類／標籤照常）
toc: true
index_img: /img/covers/rtx50-blackwell-unlock-fact-check.png
banner_img: /img/covers/rtx50-blackwell-unlock-fact-check.png
---

![RTX 50 系 Blackwell 解鎖事實查核](/img/covers/rtx50-blackwell-unlock-fact-check.png)

> <strong>整理說明</strong>：本文是對「RTX 5090 破解方案應該很快出來，解鎖後 AI 算力可衝上 420 TFLOPS 以上」這則流傳說法的查核。查核對象是 <a href="https://github.com/JustAResearcher/gpu-unlock-ada/issues/12">gpu-unlock-ada Issue #12「work on 5090?」</a> 的完整討論串（2026-10-25 開啟、10-26 由專案維護者關閉，合計 17 則留言）、NVIDIA 開源核心模組 <code>ctrl2080gr.h</code> 的速率編碼定義，以及 NVIDIA RTX Blackwell 架構白皮書的 Tensor 規格。本文**沒有用搜尋摘要**，所有數字都取自上述一手來源；媒體轉述的部分會明確標示出處層級。

<!-- more -->

## 一句話總結

> 「RTX 5090 的解鎖方案應該很快出來」是**推測**，不是消息。負責 Ada 版專案的維護者已在 2026-10-26 公開回答「不行」：Blackwell 上暫存器還在，但**主機寫進去的值會被丟棄**，速率改由<strong>熔絲（fuse）</strong>決定，而且沒有公開的 SEC2 booter 可供 payload 執行。那個「420 TFLOPS」不是任何人測出來的數字，而是把 NVIDIA 白皮書裡「FP16 累加」的規格直接套到「FP32 累加」的路徑上。

## 用一個比喻講清楚

### 比喻一：不是「門還沒開」，是「門根本沒有鎖孔」

Ampere 與 Ada 的解鎖之所以能成立，是因為那顆安全處理器上的開機程式（booter）有緩衝區溢位，攻擊者能用 ROP 取得控制流，然後把寫入保護遮罩 `FEAT_OVR_PLM` 打開，速率選擇器 `SS0`／`SS1` 就變成可寫。

**Blackwell 上這些位址一個都沒搬走，但寫進去的東西不會留下。**

ElXreno 在 GB203M（RTX 5090 Laptop，`10de:2c18`）上做的 pre-bind 唯讀傾印與寫入階梯測試，結果是：

```text
寫入階梯（pre-bind、冷開機）：
  SS0 = 0x88888888   → 讀回不變
  SS1 = 0x8          → 讀回不變
  FEAT_OVR_PLM = 0xffffffff → 讀回不變
```

連 FLR 都沒有觸發，因為什麼都沒黏住。**門牌、門框、鎖孔全都在原位，但這扇門後面接的是保險箱的熔絲——主機端寫進去的值會被丟進碎紙機。**

### 比喻二：這次不是「半速」，是「八分之一速」

這是本次查核最值得記下來的一個數字。

NVIDIA 開源核心模組 `ctrl2080gr.h` 把速率欄位定義得很清楚：

```c
#define NV2080_CTRL_GR_GET_SM_ISSUE_RATE_MODIFIER_FMLA32_FULL_SPEED        (0x0U)
#define NV2080_CTRL_GR_GET_SM_ISSUE_RATE_MODIFIER_FMLA32_REDUCED_SPEED_1_2 (0x1U)
#define NV2080_CTRL_GR_GET_SM_ISSUE_RATE_MODIFIER_FMLA32_REDUCED_SPEED_1_4 (0x2U)
#define NV2080_CTRL_GR_GET_SM_ISSUE_RATE_MODIFIER_FMLA32_REDUCED_SPEED_1_8 (0x3U)
```

**Ada（RTX 4090）stock 的 `fmla32` 是 1，也就是 1/2 速；Blackwell（RTX 5090）是 3，也就是 1/8 速。** 而且 Blackwell 連 Ada 根本沒有限速的 `imla1`、`imla4` 也變成了 3。

換句話說：**Blackwell 不是「把 Ada 的鎖調深一點」，而是換了機制。** 就算有一天寫入能成功，收益也跟 Ada 版完全不是同一個數學問題。

### 比喻三：安全處理器換人住了

整條 exploit 鏈的入口，是 GPU 裡那顆 **Falcon** 安全處理器上開機程式的緩衝區溢位。

GalladeGuy 在討論串最後補上了關鍵背景：**從 Hopper 開始，Falcon 不再是根信任，改由 Foundation Security Processor（FSP）擔任**，基於 NV-RISCV，部分韌體用 Ada SPARK 以 assurance level silver 形式化驗證。**消費級 Blackwell 也在此列，而且完全沒有使用 Falcon。**

為 Falcon 設計的 exploit，在這個前提下不是「難一點」，而是**前提消失**。

## 事實核對速查表

| 流傳說法 | 較準確的說法 | 評估 |
| --- | --- | --- |
| 「RTX 5090 解鎖後 AI 算力可衝上 420 TFLOPS 以上」 | 419 TFLOPS 是白皮書的 **FP16 累加**峰值；同一張卡的 **FP32 累加**只有 209.5。而目前沒有任何方法能讓 FP32 累加跑到全速 | **純推測** |
| 「破解方案應該很快出來」 | 專案維護者 2026-10-26 公開回覆 *"The short answer is no"*，並以「不在計劃之內」關閉 issue | **不成立** |
| 「暫存器都在，只是還沒有人做而已」 | 暫存器確實在 Ada 的**同一組位址**，但寫入階梯實測顯示**讀回完全不變**；速率由熔絲決定 | **不成立** |
| 「換一條 payload 就能沿用」 | 開源模組對 Blackwell 解析到的 booter 函式是**回傳 NULL 的 stub**；Linux／Windows 模組與多個版本分支都查無 Blackwell Falcon SEC2 booter | **不成立** |
| 「Ada 那套寫法直接照抄」 | `FEAT_READOUT_1` 在 Blackwell 上**不能用 Ada 的解碼器讀**：欄位位置差一格，還出現超出定義範圍的值 | **不成立** |
| 「至少可以先解 FP16」 | 速率表顯示 `fmla16` 在 5090 上**本來就是全速**（0），不需要解；被限速的是 `fmla32` 與三個 INT 模式 | **前提有誤** |
| 「RTX 40／30 的解鎖成果不受影響」 | 完全不受影響——那兩篇查核的結論一樣成立 | **成立** |

## 誇大關鍵字一：「420 TFLOPS」這個數字是怎麼來的

NVIDIA 的 RTX Blackwell 架構白皮書（規格頁可交叉核對）：

| 顯示卡 | FP16 累加 | FP32 累加 | 比例 |
| --- | ---: | ---: | --- |
| RTX 5090 | 419.1 TFLOPS | 209.5 TFLOPS | 剛好一半 |
| RTX 4090 | 330.3 TFLOPS | 165.2 TFLOPS | 剛好一半 |

（皆為非稀疏／dense 數字。）

所以「解鎖後可衝上 420 TFLOPS 以上」這個說法，是**把 419 當成解鎖後的目標值**。但 GeForce 被限速的是 **FP32 累加**那條路徑，解鎖要提升的正是它——換句話說，正確的目標應該寫成「**從 209.5 變成 419**」，而不是「419」。

而目前**沒有任何已證實方法**能讓 RTX 5090 的 FP32 累加達到全速。

還有一層更基本的問題：**就算有一天解鎖成功，419 這個數字也量不到。** AndrewCTF 在 GB202 上的實測矩陣乘法是 **324.6 TFLOPS（FP16 累加）對 217.5 TFLOPS（FP32 累加）**——白皮書的 419 是峰值規格，在真實負載下本來就達不到。「解鎖後衝上 420」把一個峰值規格當成解鎖後的保證值，是雙重高估。

## 誇大關鍵字二：「暫存器都在，只是還沒有人做」

ElXreno 在 GB203M 上做的 pre-bind 唯讀傾印，是目前最完整的一份 Blackwell 暫存器快照：

```text
PMC_BOOT_0        0x00000000 = 0x1b3000a1
FEAT_OVR_PLM      0x00823804 = 0xfffffb8f   (未開；AD102 stock 是 0xffffff8f)
FUSE_SS_DP        0x00820224 = 0
FUSE_SS_FFMA      0x0082059c = 0
FUSE_SS_FMLA16    0x008207d4 = 0
FUSE_SS_FMLA32    0x008207d8 = 3
FUSE_SS_IMLA0..4  0x008207dc..ec = 0, 3, 3, 0, 3
FEAT_READOUT_1    0x00823818 = 0x00c36180
FEAT_OVR_SM_SS0   0x0082381c = 0x02000000 (另一次冷開機是 0x12000000，bit28 會變)
FEAT_OVR_SM_SS1   0x00823820 = 0x00002004
SM_ISSUE_RATE     0x00504204 = 0x00000005
GFW falcon CPUCTL 0x00110100 = 0xbadf4100 (pre-bind 不可存取，沒有 SEC2 那條路)
```

這份傾印有四件事值得逐條讀：

1. **整塊暫存器在 Blackwell 上仍然活著，位址也沒有搬。** 要移植工具的人不用重新找位址——這是唯一一個「好消息」，但它幫不上解鎖。
2. **寫入階梯全部無效。** `SS0`、`SS1`、`FEAT_OVR_PLM` 寫完讀回完全不變。ElXreno 的原話是「Exactly the Ampere/Ada『writing there just does nothing』behavior」，並下了結論：**「The unlock for GB20x will be an FSP/FMC bug, not a register move.」**
3. **`FUSE_SS_*` 這組字就是限速的來源。** `FMLA32 = 3`、`IMLA1/IMLA2/IMLA4 = 3`，而 `DP`、`FFMA`、`FMLA16`、`IMLA0`、`IMLA3` 都是 0。ElXreno 特別指出：**限速資料和暫存器都在 Ada 工具預期的位置，缺的只是權限。**
4. **`FEAT_READOUT_1` 不能用 Ada 的解碼器讀。** 朴素的 9×3-bit 解碼 `0x00c36180` 得到 `0 0 6 0 6 6 0 6 0`——`6` 超出 `ctrl2080gr.h` 的定義範圍，而且非零欄位的位置與熔絲值**差一格**。也就是說，即使寫進去了，讀回也不會用 Ada 的方式確認成功。

<!-- FIG1 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 660" role="img" aria-label="Ada 與 Blackwell 的解鎖鏈對照：Ada 的主機寫入可以改變暫存器讀值，Blackwell 的寫入被無聲丟棄，速率改由熔絲決定" style="width:100%;height:auto;display:block">
<defs><marker id="m2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker><marker id="mf472b6" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#f472b6"/></marker></defs>
<rect x="0.75" y="0.75" width="998.5" height="658.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一組暫存器，兩種結局</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Ada 靠主機寫入解鎖；Blackwell 的速率改由熔絲決定，寫進去也沒用</text>
<rect x="48" y="126" width="440" height="420" rx="12" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="72" y="158" font-size="15" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Ada · RTX 4090（實測可解鎖）</text>
<rect x="72" y="180" width="392" height="58" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="86" y="207.0" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">SEC2 BooterLoad（Falcon）</text>
<text x="86" y="229.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">已公開，可載入 payload</text>
<path d="M 268 238 L 268 252" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#m2dd4bf)"/>
<rect x="72" y="252" width="392" height="58" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="86" y="279.0" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">緩衝區溢位 → ROP</text>
<text x="86" y="301.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">打開 FEAT_OVR_PLM 寫入保護</text>
<path d="M 268 310 L 268 324" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#m2dd4bf)"/>
<rect x="72" y="324" width="392" height="58" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="86" y="351.0" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">主機寫入 SS0 / SS1</text>
<text x="86" y="373.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">寫得進去，讀回值變成 0</text>
<path d="M 268 382 L 268 396" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#m2dd4bf)"/>
<rect x="72" y="396" width="392" height="58" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="86" y="423.0" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">fmla32：1 → 0</text>
<text x="86" y="445.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1/2 速 → 全速</text>
<text x="72" y="486" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">booter 明文是公開的，payload 可以照著寫</text>
<text x="72" y="506" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">SEC2 上跑的是簽章韌體，攻擊面在它自己的溢位</text>
<rect x="512" y="126" width="440" height="420" rx="12" fill="#1c2230" stroke="#f472b655" stroke-width="1.5"/>
<text x="536" y="158" font-size="15" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Blackwell · RTX 5090（寫不進去）</text>
<rect x="536" y="180" width="392" height="58" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="550" y="207.0" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">沒有 Falcon SEC2 booter</text>
<text x="550" y="229.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">改用 FSP（NV-RISCV）當根信任</text>
<path d="M 732 238 L 732 252" fill="none" stroke="#f472b6" stroke-width="2" marker-end="url(#mf472b6)"/>
<rect x="536" y="252" width="392" height="58" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="550" y="279.0" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GFW / FMC / GSP 全加密</text>
<text x="550" y="301.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">開源模組查無 Blackwell booter</text>
<path d="M 732 310 L 732 324" fill="none" stroke="#f472b6" stroke-width="2" marker-end="url(#mf472b6)"/>
<rect x="536" y="324" width="392" height="58" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="550" y="351.0" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">主機寫入 SS0 / SS1 / PLM</text>
<text x="550" y="373.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">讀回完全不變——無聲丟棄</text>
<path d="M 732 382 L 732 396" fill="none" stroke="#f472b6" stroke-width="2" marker-end="url(#mf472b6)"/>
<rect x="536" y="396" width="392" height="58" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="550" y="423.0" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">fmla32：3（熔絲決定）</text>
<text x="550" y="445.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1/8 速，比 Ada 更嚴</text>
<text x="536" y="486" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">開源模組對 Blackwell 的 booter 函式是回傳 NULL 的 stub</text>
<text x="536" y="506" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">熔絲改了會讓卡 refuse to post，不是「沒反應」而是開不了機</text>
<rect x="48" y="566" width="904" height="74" rx="10" fill="#1c2230" stroke="#fbbf2455" stroke-width="1.5"/>
<text x="68" y="592" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩件事同時成立：暫存器還在、閘門關著。</text>
<text x="68" y="614" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">差異不在「有沒有人做」，而在「寫不進去」——寫入階梯讀回完全不變，連 FLR 都不會發生。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：兩條鏈的對照——Ada 的寫入會改變讀值，Blackwell 的寫入被無聲丟棄；差異不在「有沒有人做」，而在「寫不進去」。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG1 -->

## 誇大關鍵字三：「換一條 payload 就能沿用」

整條 exploit 鏈的入口，是 Falcon SEC2 上的 `BooterLoad` 容器。**Blackwell 沒有這條路。**

NVIDIA 開源發布 `BooterLoadUcode` 給 TU102、TU116、GA100、GA102、AD102；**Blackwell 改發 `GspRmBoot_GB202` 與 `ConcatenatedFMC_GB202`**。在開源模組裡，每一顆晶片（含 Blackwell）的 per-chip dispatch 都解析到 `kgspGetBinArchiveBooterLoadUcode_80f438`——而它在開源標頭裡是**回傳 NULL 的 stub**。

isma-is-dev 把關閉式模組那邊也清點完了，結論相當乾脆：

- Windows 621.01 確實帶了兩個大小像 booter 的 Falcon image（60,928 與 57,600 bytes），而且各自有一個 debug twin，其 AES 控制值出現 11 次與 15 次——看起來正是公開測試金鑰能開的那兩個。
- **但它們不是 Blackwell 的。** 621.01 對應開源模組的 615 分支，那個分支的生成陣列把每個 booter 與來源路徑都寫明了；比對結果是 57,600 bytes 那個**逐位元組就是 AD102 的 booter**，60,928 bytes 那個是 GA102 的。
- **Linux 610.43.03 模組、Windows 610.88 模組、Windows 621.01 模組，以及 610.43.03 與 615.78.08 兩個原始碼分支，都沒有公開 Blackwell 的 Falcon SEC2 booter。**
- 而且 Blackwell 的 GFW、FMC、GSP boot image **全部是加密的**——所以 Blackwell payload 不可能是「移植一份 Ada payload」，它必須繞著 FSP 或 GFW 重建，而且要在真實 Blackwell 卡上驗證。

AndrewCTF 另補了一條韌體層的觀察：**Blackwell 的韌體目錄裡完全沒有 `booter_load` 檔**（Ampere 與 Ada 都有 `booter_load` 與 `booter_unload` 兩份），只有 `bootloader` 與新的 `fmc`；而 `bootloader` 是 GA102 `booter_load` 的 **3.3 倍大**。

## 速率檔位：這次不是「半速」，是「八分之一速」

<!-- FIG2 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 570" role="img" aria-label="速率檔位對照：Ada 的 fmla32 是 1（1/2 速），Blackwell 是 3（1/8 速），而且 imla1 也被限速" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="998.5" height="568.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Ada 的 1/2 速 vs Blackwell 的 1/8 速</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一組速率欄位，兩代的限速深度與受影響欄位都不一樣</text>
<text x="48" y="128" font-size="12.5" fill="#8b949e" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">速率欄位</text>
<text x="318" y="128" font-size="12.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Ada · RTX 4090 stock</text>
<text x="528" y="128" font-size="12.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Ada · RTX 4090 解鎖後</text>
<text x="738" y="128" font-size="12.5" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Blackwell · RTX 5090</text>
<rect x="48" y="144" width="270" height="28" rx="6" fill="#1c2230" stroke="#30363d" stroke-width="1"/>
<text x="62" y="163" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">fmla32</text>
<text x="144" y="163" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FP16 乘、FP32 累加</text>
<rect x="318" y="144" width="200" height="28" rx="6" fill="#fbbf2422" stroke="#fbbf2499" stroke-width="1"/>
<text x="418.0" y="162.5" font-size="12.5" fill="#fbbf24" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1 → 1/2 速</text>
<rect x="528" y="144" width="200" height="28" rx="6" fill="#2dd4bf22" stroke="#2dd4bf99" stroke-width="1"/>
<text x="628.0" y="162.5" font-size="12.5" fill="#2dd4bf" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0 → 全速</text>
<rect x="738" y="144" width="214" height="28" rx="6" fill="#f472b622" stroke="#f472b699" stroke-width="1"/>
<text x="845.0" y="162.5" font-size="12.5" fill="#f472b6" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3 → 1/8 速</text>
<rect x="48" y="178" width="270" height="28" rx="6" fill="#1c2230" stroke="#30363d" stroke-width="1"/>
<text x="62" y="197" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">imla2</text>
<text x="144" y="197" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">INT 模式</text>
<rect x="318" y="178" width="200" height="28" rx="6" fill="#fbbf2422" stroke="#fbbf2499" stroke-width="1"/>
<text x="418.0" y="196.5" font-size="12.5" fill="#fbbf24" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1 → 1/2 速</text>
<rect x="528" y="178" width="200" height="28" rx="6" fill="#2dd4bf22" stroke="#2dd4bf99" stroke-width="1"/>
<text x="628.0" y="196.5" font-size="12.5" fill="#2dd4bf" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0 → 全速</text>
<rect x="738" y="178" width="214" height="28" rx="6" fill="#f472b622" stroke="#f472b699" stroke-width="1"/>
<text x="845.0" y="196.5" font-size="12.5" fill="#f472b6" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3 → 1/8 速</text>
<rect x="48" y="212" width="270" height="28" rx="6" fill="#1c2230" stroke="#30363d" stroke-width="1"/>
<text x="62" y="231" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">imla4</text>
<text x="144" y="231" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">INT 模式</text>
<rect x="318" y="212" width="200" height="28" rx="6" fill="#fbbf2422" stroke="#fbbf2499" stroke-width="1"/>
<text x="418.0" y="230.5" font-size="12.5" fill="#fbbf24" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1 → 1/2 速</text>
<rect x="528" y="212" width="200" height="28" rx="6" fill="#2dd4bf22" stroke="#2dd4bf99" stroke-width="1"/>
<text x="628.0" y="230.5" font-size="12.5" fill="#2dd4bf" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0 → 全速</text>
<rect x="738" y="212" width="214" height="28" rx="6" fill="#f472b622" stroke="#f472b699" stroke-width="1"/>
<text x="845.0" y="230.5" font-size="12.5" fill="#f472b6" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3 → 1/8 速</text>
<rect x="48" y="246" width="270" height="28" rx="6" fill="#1c2230" stroke="#30363d" stroke-width="1"/>
<text x="62" y="265" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">imla1</text>
<text x="144" y="265" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">INT 模式</text>
<rect x="318" y="246" width="200" height="28" rx="6" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<text x="418.0" y="264.5" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">—</text>
<rect x="528" y="246" width="200" height="28" rx="6" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<text x="628.0" y="264.5" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">—</text>
<rect x="738" y="246" width="214" height="28" rx="6" fill="#f472b622" stroke="#f472b699" stroke-width="1"/>
<text x="845.0" y="264.5" font-size="12.5" fill="#f472b6" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3 → 1/8 速</text>
<rect x="48" y="280" width="270" height="28" rx="6" fill="#1c2230" stroke="#30363d" stroke-width="1"/>
<text x="62" y="299" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">fmla16</text>
<text x="144" y="299" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FP16 乘、FP16 累加</text>
<rect x="318" y="280" width="200" height="28" rx="6" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<text x="418.0" y="298.5" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">—</text>
<rect x="528" y="280" width="200" height="28" rx="6" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<text x="628.0" y="298.5" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">—</text>
<rect x="738" y="280" width="214" height="28" rx="6" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<text x="845.0" y="298.5" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0 → 本來就全速</text>
<rect x="48" y="336" width="904" height="76" rx="10" fill="#1c2230" stroke="#fbbf2455" stroke-width="1.5"/>
<text x="68" y="362" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">速率編碼（NVIDIA 開源核心模組 ctrl2080gr.h）</text>
<text x="68" y="386" font-size="12" fill="#e6edf3" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">FMLA32_FULL_SPEED = 0 ｜ REDUCED_SPEED_1_2 = 1 ｜ REDUCED_SPEED_1_4 = 2 ｜ REDUCED_SPEED_1_8 = 3</text>
<text x="68" y="404" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">「1/2 速」在 Ada 已經是極限；Blackwell 的「3」是 1/8 速——限得更深，而且連欄位集合都變了。</text>
<rect x="48" y="428" width="904" height="76" rx="10" fill="#1c2230" stroke="#f472b655" stroke-width="1.5"/>
<text x="68" y="454" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">所以「解鎖後衝上 420 TFLOPS」有兩層問題</text>
<text x="68" y="478" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">① 419 TFLOPS 是白皮書的 FP16 累加峰值，不是 FP32 累加；後者只有 209.5。</text>
<text x="68" y="496" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">② 就算解鎖成功，實測 FP16 累加也只有 324.6 TFLOPS——峰值規格本來就量不到。</text>
<text x="48" y="534" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Ada 欄位取自 gpu-unlock-ada 的 read_sm_rates.py 配對讀值；Blackwell 欄位取自 AndrewCTF（GB202）與 ElXreno（GB203M）的讀值。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：速率檔位對照——Ada 的 fmla32 是 1（1/2 速）、Blackwell 是 3（1/8 速），連 Ada 沒有限速的 imla1 也被鎖住。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG2 -->

把 Ada 與 Blackwell 的速率讀值並排看，差別比想像中更遠：

| 速率欄位 | 意義 | Ada · RTX 4090（stock） | Ada · RTX 4090（解鎖後） | Blackwell · RTX 5090 |
| --- | --- | --- | --- | --- |
| `fmla32` | FP16 乘、FP32 累加 | 1（1/2 速） | 0（全速） | **3（1/8 速）** |
| `imla2` | INT 模式 | 1（1/2 速） | 0（全速） | **3（1/8 速）** |
| `imla4` | INT 模式 | 1（1/2 速） | 0（全速） | **3（1/8 速）** |
| `imla1` | INT 模式 | — | — | **3（1/8 速）** |
| `fmla16` | FP16 乘、FP16 累加 | — | — | 0（**本來就全速**） |

（Ada 欄位取自 `gpu-unlock-ada` 的 `read_sm_rates.py` 配對讀值；Blackwell 欄位取自 AndrewCTF 在 GB202、ElXreno 在 GB203M 的讀值。）

這張表解釋了兩件事：

1. **Blackwell 的限速比 Ada 深一階**，而且受影響的欄位更多（`imla1` 在 Ada 沒有限速，在 Blackwell 被鎖成 1/8 速）。
2. **「FP16 被解鎖」這個說法本身有問題。** `fmla16` 在 5090 上本來就是 0（全速），本來就不需要解。AndrewCTF 在 2026-10-26 說的 *"FP16 bypass should work, I'll be committing it. FP32 is a work in progress"*——指的是「**FP16 乘、FP32 累加**」那條路徑，不是 FP16 本身。這個措辭很容易被讀成「5090 的 FP16 被鎖了、之後會解開」。

## 各型號狀態總表

| 型號 | 晶片 | 狀態 | 目前證據 |
| --- | --- | --- | --- |
| **RTX 5090** | GB202（`10de:2b85`） | **無法解鎖** | RM 速率表（`fmla32 = 3`）、熔絲讀值、寫入階梯讀回完全不變 |
| **RTX 5090 Laptop** | GB203M（`10de:2c18`） | **無法解鎖** | pre-bind 暫存器傾印、寫入階梯讀回完全不變、`FEAT_READOUT_1` 解碼方式不同 |
| **RTX 5090D 等中國市場型號** | GB20x | 同屬世代，無公開方法 | 同上；與出口管制無關，是架構層面的限制 |
| **Blackwell 全系** | gb100／gb102／gb202／gb203／gb205／gb206／gb207 | **沒有任何 `booter_load` 檔** | 韌體目錄盤點：只有 `bootloader` 與 `fmc` |

## 風險與界線

### 熔絲這條路看起來是致命的，不是無害的

這是 Blackwell 與前兩代最要命的一點差異。

Panchovix 在討論串裡的實測回報：

> Blackwell isn't unlocked at the moment, it seems it reads the information from a fuse, and if you edit the values from the flags that live there and try to boot, **the card will refuse to post** (easy to revert). Is not like Ada or before.

ElXreno 也特別加了警語：相對於「寫進去沒反應」，**熔絲改動在 Blackwell 上看起來是 fatal 而非 inert**。

換句話說：在 Ada 與 Ampere 上，寫錯暫存器頂多是「沒解鎖」；在 Blackwell 上碰熔絲，**有可能把卡弄成開不了機的狀態**。ElXreno 因此建議，若要試就只試那條**易失性**的 SS／PLM 階梯——那個寫完下次冷開機就復原。

AndrewCTF 則指出電壓故障注入（voltage glitching）可能是寫入熔絲的一條路，但「最大的問題是熔絲」，而且他找到的是**三個**熔絲，「Software might not be possible」。

### 授權條款

NVIDIA GeForce 驅動程式授權條款第 2.6 條原文：

> You may not **bypass, disable, or circumvent** any technical limitation, encryption, security, digital rights management or authentication mechanism in the SOFTWARE.

這是明文。至於「在驅動程式載入前執行的核心模組」算不算 circumvent，目前沒有任何判例或官方說明；截至本文撰寫，**NVIDIA 未對這批開源專案公開表態**。

### 其他風險

- **硬體損壞。** Turing 分支的 `nlzy/turing-unlock` 把警告放在 README 最上方：*"Tensor cores draw very high power. Unlocking them to full speed may damage your hardware."* Ampere 分支的 4090 配對實測則記錄了峰值功耗的變化（詳見 [RTX 40 系查核](/2026/10/25/rtx40-tensor-unlock-fact-check/)）。
- **二手市場效應。** VideoCardz 指 RTX 3090 與 4090 本身就因 24GB 記憶體受 AI 用家青睞，解鎖後算力再提升，可能讓它們在二手市場更搶手——對遊戲玩家未必是好事。
- **不要為了「試看看」就去改熔絲。** 從目前的證據看，Blackwell 上的熔絲路徑既沒有公開工具、也沒有已知可逆保證，這正是它「看起來致命」的原因。

## 給不同身份的讀者

- **只想知道能不能解**：不能。現階段沒有任何方法，而且**不是「沒人做」，是「寫不進去」**。這個差別很重要——後者意味著它不會像 Ada 那樣在一兩個月內突然出現。
- **手上是 4090 或 3090**：解鎖依然有效，[RTX 40](/2026/10/25/rtx40-tensor-unlock-fact-check/) 與 [RTX 30](/2026/10/25/rtx30-gpu-unlock-ampere-fact-check/) 兩篇查核的結論一點都沒變。而且現在多了一個具體好處：討論串裡有人說得很直白——*"my unlocked 4090 now trains faster than my 5090"*。在 Blackwell 的 FP32 累加只有 1/8 速的前提下，這不是比喻。
- **正在評估買 5090**：`fmla32 = 3` 這件事會不會影響你，判準跟前兩篇完全一樣——**你的負載有沒有在跑「FP16／BF16 乘、FP32 累加」的矩陣乘法**。有，就吃得到差異；只有 INT8／INT4／FP8 量化或逐 token 生成，那 1/8 速與 1/2 速對你幾乎無差。
- **開發者想跟進**：目前公開的兩個開門方向是 (a) GB20x booter 明文，或 NVIDIA 的公開 AES-128-ECB 測試金鑰；(b) FSP／GFW 這條新的攻擊面。isma-is-dev 的 fork 已經做到「辨識出 Blackwell 卡、帶原因拒絕、離成功差一個輸入」，而且他公開了 payload 產生流程：`find_gadgets.py` 能用位元組特徵自動找到六個 gadget，在 AD102 上驗證到與已公布位址逐位元組相符。**這代表未來若拿到 Blackwell booter 明文，payload 那一段是機械化的——真正缺的只有那份明文。**
- **看到「5090 被破解」標題就轉發的**：本文的核心是——**「420 TFLOPS」是一個被推算出來的目標，不是測得的結果**。

## 查核方法與可重現性

本文**沒有用搜尋摘要**，所有數字直接取自一手來源：

| 來源 | 用途 |
| --- | --- |
| `gpu-unlock-ada` Issue #12（17 則留言） | GB202／GB203M 偵察、速率編碼、寫入階梯、booter 清點、維護者的關閉結論 |
| NVIDIA 開源核心模組 `ctrl2080gr.h` | `NV2080_CTRL_GR_GET_SM_ISSUE_RATE_MODIFIER_FMLA32_*` 的速率編碼定義（0／1／2／3） |
| Linux 核心文件 `gpu/nova/core/fsp.html` | FSP 取代 Falcon 作為根信任的架構事實 |
| NVIDIA RTX Blackwell 架構白皮書 | 5090／4090 的 Tensor 規格（FP16 累加 vs FP32 累加） |
| 規格頁交叉核對 | 419.1／209.5 TFLOPS 與「dense」標示 |
| `gpu-unlock-ada` 的 `read_sm_rates.py` 配對讀值 | Ada 欄位（`fmla32`／`imla2`／`imla4` 由 1 變 0） |

媒體轉述的部分（媒體把 209.5 與 419 並列引用、宣稱「解鎖方案很快出來」）在文中已標明為**推算**，不作為證據。

## 參考資料

- 討論串（本文主要來源）：[gpu-unlock-ada Issue #12「work on 5090?」](https://github.com/JustAResearcher/gpu-unlock-ada/issues/12)
- 專案首頁：[github.com/JustAResearcher/gpu-unlock-ada](https://github.com/JustAResearcher/gpu-unlock-ada)
- NVIDIA 開源核心模組：[github.com/NVIDIA/open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules)
- Blackwell 白皮書：[nvidia-rtx-blackwell-gpu-architecture.pdf](https://images.nvidia.com/aem-dam/Solutions/geforce/blackwell/nvidia-rtx-blackwell-gpu-architecture.pdf)
- FSP 架構文件：[docs.kernel.org/gpu/nova/core/fsp.html](https://docs.kernel.org/gpu/nova/core/fsp.html)
- 同系列查核文章：
  - [RTX 40 系 Tensor 解鎖事實查核](/2026/10/25/rtx40-tensor-unlock-fact-check/)——全系列、翻倍、Windows 一鍵用三個關鍵字都不成立的理由
  - [RTX 30 系 gpu-unlock 事實查核](/2026/10/25/rtx30-gpu-unlock-ampere-fact-check/)——Ampere 上游的完整版，含 Turing 世代的兩條新路線
  - [RTX 4090 解除 gpu-unlock 操作筆記](/2026/10/25/rtx4090-gpu-unlock-guide/)——Ada 路徑的完整動手流程
  - [RTX 3080 12GB 解除 gpu-unlock 操作筆記](/2026/10/25/rtx3080-12gb-gpu-unlock-guide/)——Ampere 路徑的完整動手流程

---

> <strong>最後一話</strong>：值得肯定的不是「RTX 5090 被破解」這種口號——這一次根本沒有發生。值得肯定的是 Issue #12 裡那幾位把一手偵察攤開來講的人：只讀探測、暫存器傾印、寫入階梯、韌體佈局盤點、bindata 清點，每一項都附上可重現的指令與位址；連「熔絲改了會讓卡 refuse to post」這種對自己不利、對動手者不利的警告都寫在留言裡。
>
> 這個討論串示範了一件很值得學的事：**「這條路走不通」的證據，和「這條路走得通」的證據同樣有價值。** 而媒體版本把整件事壓縮成一句「破解方案應該很快出來」，連那個「420 TFLOPS」是從哪個規格數字倒推出來的都沒講。**研究是真的，這次的標題是假的。**



