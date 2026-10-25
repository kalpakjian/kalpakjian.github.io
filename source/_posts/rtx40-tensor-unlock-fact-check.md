---
title: RTX 40 系 Tensor 解鎖事實查核：全系列、翻倍、Windows 一鍵用，三個關鍵字都不成立
date: 2026-10-25 15:30:00
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
toc: true
index_img: /img/covers/rtx40-tensor-unlock-fact-check.png
banner_img: /img/covers/rtx40-tensor-unlock-fact-check.png
---

![RTX 40 系 Tensor 解鎖事實查核](/img/covers/rtx40-tensor-unlock-fact-check.png)

> <strong>整理說明</strong>：本文是對「RTX 40 系被破解、Tensor 算力翻倍、Windows 也能用」這則流傳報導的查核。查核對象是 GitHub 開源專案 <a href="https://github.com/JustAResearcher/gpu-unlock-ada">JustAResearcher/gpu-unlock-ada</a> v1.1.1 與 Hugging Face 的 <a href="https://huggingface.co/TOTORONG/AD103_win_unlocker">TOTORONG/AD103_win_unlocker</a>。所有數字都取自一手來源：專案的原始碼（<code>arch_610.h</code>、<code>main.c</code>、<code>unlock_610.c</code>）、README、<code>docs/</code> 實測報告與 <code>evidence/</code> 配對實測資料，以及 GitHub Issues 與 Hugging Face model card，不採用二手轉述。

<!-- more -->

## 一句話總結

> 這是一條**真實而且技術含量很高**的研究路線，原始碼、韌體產生流程、雜湊固定的資產、配對實測、數值驗證、公開的限制聲明全都齊備，值得肯定。但媒體口耳相傳的三個關鍵字——「全系列」、「所有 AI 負載翻倍」、「Windows 一鍵可用」——**一個都不成立**。現階段只有 RTX 4090 有較完整的公開證據，而且「2 倍」指的是最底層的<strong>指令發射率</strong>，實際跑 cuBLAS GEMM 大約只快 <strong>12–34%</strong>。

## 用一個比喻講清楚

### 比喻一：這不是「升級」，是「拆限速器」

你的 RTX 4090 是一台引擎輸出很猛的车，但出廠時，行控器裡被寫死了一條限制：**Tensor 那一條線最多只能跑半速**。專業卡（RTX A 系列）沒有這條限制，售價卻是數倍起跳。

這個開源專案做的事，等同於有人真的研究出怎麼把那條限制從行控器裡改掉——而且他把原始碼、韌體產生流程、實測報告全部公開了。在消費級硬體上，這種程度的研究透明度非常少見。

**但「限速器拆掉了」不等於「車從 60 變 200」。**

- 車子的**極限**（引擎排氣量、變速箱齒比、輪胎抓地力）都沒變。
- 媒體說的「2 倍」，指的是**引擎每單位時間能吐出的動力**（指令發射率），不是**車在路上的實際速度**。
- 實際能跑多快，還要看**變速箱齒比**（對應矩陣形狀）、**路面狀況**（對應負載型態）、**限速牌**（對應功耗上限）。

這就是為什麼實測下來，cuBLAS GEMM 只快 12–34%，而不是 2 倍。同理，媒體說的「所有 AI 工作負載都翻倍」——**不是**，因為 INT8、INT4、`dp4a`、純 FP32 這些運算路徑完全沒有變化。

### 比喻二：不是「更耗電」，是「同樣的電跑更多里程」

媒體常說「效能提升必然伴隨更多功耗」。但配對實測的遙測不支持這句：同一張卡、同一個 450 W 功耗上限，功耗從 **307.67 W** 變成 **308.59 W**，幾乎沒差；4070 Ti SUPER 更是在**同一個 240 W 上限**下 FP16 直接翻倍。

原因很單純：**這些卡本來就被功耗上限壓住**。你把引擎限速拆掉，它不是「多吃燃料」，而是「在同樣油耗下跑得更快」——這是**效率**提升，不是**耗能**提升。

真正該擔心的是別的兩件事：持續 100% 負載下的散熱與供電裕度，以及這套玩法**幾乎完全缺乏長期穩定性資料**。

### 比喻三：「白名單只有四張卡」

專案原始碼裡有一份裝置 ID 白名單，可以理解成「這把鑰匙只開這四扇門」：

| 裝置 ID | 對應卡 | 狀態 |
| --- | --- | --- |
| `0x2684` | RTX 4090 | 正式路徑 |
| `0x2685` | RTX 4090 D | 實驗性旗標 |
| `0x2705` | RTX 4070 Ti SUPER（AD103） | 實驗性，單卡驗證 |
| `0x2805` | RTX 4060 Ti 16GB（AD106） | 實驗性，單卡驗證 |

而且後兩者還要**指定單一 PCI 位址**並開啟對應的實驗旗標，`targets=all` 永遠不會選中它們。**你的卡不在名單裡，模組就會直接略過它**，不會有任何提示。

## 事實核對速查表

| 流傳說法 | 較準確的說法 | 評估 |
| --- | --- | --- |
| 「RTX 40 全系列（4090 到 4060 Ti）都能解鎖」 | 原始碼白名單只有 4 個 Ada 裝置 ID；4070 Ti SUPER 與 4060 Ti 需實驗旗標 + 單一 PCI 位址 | 過度延伸 |
| 「Tensor 算力翻倍」 | 翻倍的是 **register-resident 指令發射率**（FP16/BF16/TF32 搭 FP32 累加）；實際 cuBLAS GEMM 中位吞吐只快 **12–34%**，4096³ BF16 無變化 | 數字對、含義錯 |
| 「所有 AI 工作負載都變快」 | INT8、unsigned INT4、`dp4a`、純 FP32、FP16 搭 FP16 累加**都沒有變化**；FP8 配對實測僅 +0.3% | 過度延伸 |
| 「RTX 4080 / 4080 SUPER 也能用」 | 不在白名單；Hugging Face 的是一張**改裝成 32GB 的非 SUPER 4080**（AD103）實驗，EFI 釘在特定 ROM hash，換卡可能被拒 | 不成立 |
| 「Windows 一鍵解鎖所有 RTX 40」 | 兩個彼此獨立的單卡實驗（HF 改裝 4080、repo 內 MSI 4070 Ti AD104），都不散佈可攜二進位、都只適用單一板型 | 不成立 |
| 「效能提升必然更耗電」 | 固定 450 W 上限下功耗 307.67 → 308.59 W；4070 Ti SUPER 在同一個 240 W 上限下 FP16 翻倍 | 與實測相反 |
| 「這是假的／是陰謀論」 | 是真的開源專案：原始碼、雜湊固定的韌體資產、配對實測、數值驗證、公開的限制聲明都齊備 | 過度懷疑 |

## 它到底做了什麼（白話版）

三個步驟，沒有什麼神祕的魔改：

1. **在開機早期、驅動還沒接手前，先把 GPU 從「睡眼惺忪」叫醒並改設定。**
   具體做法是載入一個 Linux 核心模組（放在 initramfs 裡），在 NVIDIA 官方驅動綁定卡片之前執行一段 GPU 韌體交易。
2. **改寫 SM 的「速度選擇器」。**
   專案把 `SS0` 寫成 `0x88888888`、`SS1` 寫成 `0x8`，等於把「Tensor 跑半速」這個檔位改成「全速」。整個過程還需要先確認三個權限暫存器寫入成功、payload 完成標記正確、SEC2 真的停下來，模組才敢宣稱成功。
3. **做一次 PCIe FLR（功能層級重置）**，讓 NVIDIA 驅動接手一張乾淨的卡。

> <strong>白話說</strong>：這不是「破解防盜鎖」這種神話，而是「研究出正確的初始化順序，並且把每一步都做成可驗證的」。上游甚至自己在 NOTICE 裡寫明：<em>重現 payload 位元組本身，並不等於已經建立那些執行期結果與安全性</em>——這句自省相當誠實。

## 誇大關鍵字一：「RTX 40 全系列都能解鎖」

權威依據是專案自己的原始碼，不是新聞稿：

```c
/* kernel/gpu_unlock/arch_610.h */
/* Exact experimental AD103 canary; other Ada IDs are not admitted. */
#define GU_AD103_RTX_4070_TI_SUPER 0x2705u
/* Exact experimental AD106 target, untested on silicon. */
#define GU_AD106_RTX_4060_TI_16GB   0x2805u
/* RTX 4090 D uses the AD102 firmware path; gated as experimental. */
#define GU_AD102_RTX_4090_D         0x2685u
```

模組的 `module_param` 說明寫得更直白：

```c
MODULE_PARM_DESC(ad103_experimental,
  "permit only the exact 10de:2705 AD103 canary with a single explicit PCI address");
MODULE_PARM_DESC(ad106_experimental,
  "permit only the exact 10de:2805 AD106 target with a single explicit PCI address; untested on silicon");
```

<!-- FIG3 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 530" role="img" aria-label="gpu_unlock 模組的裝置白名單：只有 RTX 4090、4090 D、4070 Ti SUPER、4060 Ti 16GB 四個 ID" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="998.5" height="528.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">裝置白名單只有四個 ID</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">直接來自 kernel/gpu_unlock/arch_610.h，不是行銷文案</text>
<rect x="48" y="126" width="904" height="50" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="500.0" y="149.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">白名單只有這四個 Ada 裝置 ID</text>
<text x="500.0" y="171.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">直接來自 kernel/gpu_unlock/arch_610.h，不是行銷文案</text>
<path d="M 500 176 L 500 190" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 156.0 190 L 864.0 190" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 156.0 190 L 156.0 204" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 392.0 190 L 392.0 204" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 628.0 190 L 628.0 204" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 864.0 190 L 864.0 204" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="206" width="216" height="158" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="62" y="234" font-size="12.5" fill="#2dd4bf" font-weight="700" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">10de:2684</text>
<text x="62" y="262" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 4090</text>
<text x="62" y="282" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">AD102</text>
<rect x="60" y="296" width="104" height="26" rx="6" fill="#2dd4bf22" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="112" y="314" font-size="12" fill="#2dd4bf" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">正式路徑</text>
<text x="62" y="344" font-size="10.5" fill="#8b949e" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">只需 gpu_unlock.targets=</text>
<rect x="284" y="206" width="216" height="158" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="298" y="234" font-size="12.5" fill="#fbbf24" font-weight="700" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">10de:2685</text>
<text x="298" y="262" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 4090 D</text>
<text x="298" y="282" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">AD102</text>
<rect x="296" y="296" width="104" height="26" rx="6" fill="#fbbf2422" stroke="#fbbf24" stroke-width="1.5"/>
<text x="348" y="314" font-size="12" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">實驗性</text>
<text x="298" y="344" font-size="10.5" fill="#8b949e" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">+ rtx4090d_experimental=1</text>
<rect x="520" y="206" width="216" height="158" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="534" y="234" font-size="12.5" fill="#fbbf24" font-weight="700" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">10de:2705</text>
<text x="534" y="262" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 4070 Ti SUPER</text>
<text x="534" y="282" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">AD103</text>
<rect x="532" y="296" width="104" height="26" rx="6" fill="#fbbf2422" stroke="#fbbf24" stroke-width="1.5"/>
<text x="584" y="314" font-size="12" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">實驗性・單卡</text>
<text x="534" y="344" font-size="10.5" fill="#8b949e" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">+ ad103_experimental=1</text>
<text x="534" y="358" font-size="10.5" fill="#8b949e" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">+ 單一完整 PCI 位址</text>
<rect x="756" y="206" width="216" height="158" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="770" y="234" font-size="12.5" fill="#fbbf24" font-weight="700" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">10de:2805</text>
<text x="770" y="262" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 4060 Ti 16GB</text>
<text x="770" y="282" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">AD106</text>
<rect x="768" y="296" width="104" height="26" rx="6" fill="#fbbf2422" stroke="#fbbf24" stroke-width="1.5"/>
<text x="820" y="314" font-size="12" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">實驗性・單卡</text>
<text x="770" y="344" font-size="10.5" fill="#8b949e" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">+ ad106_experimental=1</text>
<text x="770" y="358" font-size="10.5" fill="#8b949e" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">+ 單一完整 PCI 位址</text>
<rect x="48" y="392" width="904" height="60" rx="10" fill="#1c2230" stroke="#f472b655" stroke-width="1.5"/>
<text x="68" y="418" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">targets=all 永遠不會選中 2705 與 2805 —— 實驗型號必須指定單一 PCI 位址。</text>
<text x="68" y="440" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">你的卡不在白名單裡 → 模組會直接略過它，不會跳任何警告。</text>
<text x="48" y="486" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4070 Ti SUPER 有兩種晶片：0x2705 是 AD103（本專案支援）、0x2689 是 AD104（不支援）。</text>
<text x="48" y="508" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4060 Ti 16GB 實機常回報 0x2803 而非 0x2805，一樣會被略過。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 3：模組只認這四個裝置 ID——後兩者還要實驗旗標與單一 PCI 位址；不在名單裡的卡會被直接略過，不會跳警告。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG3 -->

也就是說：**「全系列」這句話連原始碼都不用翻譯就自我否定**。實驗型號還額外要求單一 PCI 位址，`targets=all` 永不選中它們——這是刻意的設計，目的是避免使用者不知情就對多張卡下指令。

補充一個容易誤會的點：這個專案**並非純 Ada 專案**。`targets=all` 會連同上游 `Zagitta/gpu-unlock` 的 GA102／GA104／GA103／GA106 一起選（上游曾回報 RTX 3090 成功），只是本次查核焦點在 40 系。

## 誇大關鍵字二：「所有 AI 工作負載都翻倍」

這是最需要拆開的一個說法，因為它把三種不同的數字混在一起了。

<!-- FIG1 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" role="img" aria-label="解鎖後的增幅落差：指令發射率 +100%，但真實 cuBLAS GEMM 只有 +12% 到 +34%" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="998.5" height="598.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">翻倍到實際的落差</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一張 RTX 4090 解鎖後，相對原本（stock）的增幅</text>
<path d="M 330 146 L 330 448" fill="none" stroke="#7d8590" stroke-width="1.5"/>
<text x="886" y="136" font-size="11.5" fill="#2dd4bf" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">「翻倍」+100%</text>
<text x="300" y="165" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FP16／BF16 → FP32 指令發射率</text>
<text x="300" y="182" font-size="11.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">最底層的指令率，也就是媒體說的「翻倍」</text>
<rect x="330" y="150" width="560" height="28" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="330" y="150" width="560.0" height="28" rx="8" fill="#2dd4bf55" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="900.0" y="169" font-size="13.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+100.0%</text>
<text x="300" y="217" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">cuBLAS GEMM 4096³ FP16</text>
<text x="300" y="234" font-size="11.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">真實矩陣乘法最好的一格</text>
<rect x="330" y="202" width="560" height="28" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="330" y="202" width="192.64" height="28" rx="8" fill="#58a6ff55" stroke="#58a6ff" stroke-width="1.5"/>
<text x="532.64" y="221" font-size="13.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+34.4%</text>
<text x="300" y="269" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">cuBLAS GEMM 1024³ BF16</text>
<text x="300" y="286" font-size="11.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">小矩陣、換一種精度</text>
<rect x="330" y="254" width="560" height="28" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="330" y="254" width="109.76" height="28" rx="8" fill="#58a6ff55" stroke="#58a6ff" stroke-width="1.5"/>
<text x="449.76" y="273" font-size="13.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+19.6%</text>
<text x="300" y="321" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">cuBLAS GEMM 8192³ BF16</text>
<text x="300" y="338" font-size="11.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">換個矩陣形狀又是另一個數字</text>
<rect x="330" y="306" width="560" height="28" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="330" y="306" width="89.6" height="28" rx="8" fill="#58a6ff55" stroke="#58a6ff" stroke-width="1.5"/>
<text x="429.6" y="325" font-size="13.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+16.0%</text>
<text x="300" y="373" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">cuBLAS GEMM 4096³ BF16</text>
<text x="300" y="390" font-size="11.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">這一組完全沒有變化，暖開機重測還倒退</text>
<rect x="330" y="358" width="560" height="28" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="326.0" y="358" width="4.0" height="28" rx="8" fill="#f472b655" stroke="#f472b6" stroke-width="1.5"/>
<text x="342" y="377" font-size="13.5" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">▼ -0.5%</text>
<text x="300" y="425" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">E4M3 FP8 CUTLASS GEMM</text>
<text x="300" y="442" font-size="11.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">專案自己公布的數字：+0.3%</text>
<rect x="330" y="410" width="560" height="28" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="330" y="410" width="4.0" height="28" rx="8" fill="#7d859055" stroke="#7d8590" stroke-width="1.5"/>
<text x="344.0" y="429" font-size="13.5" fill="#7d8590" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+0.3%</text>
<text x="330.0" y="472" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0%</text>
<text x="470.0" y="472" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+25%</text>
<text x="610.0" y="472" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+50%</text>
<text x="750.0" y="472" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+75%</text>
<text x="890.0" y="472" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+100%</text>
<rect x="48" y="488" width="904" height="88" rx="10" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="68" y="516" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">媒體說的「翻倍」＝ 最上面那根（指令發射率）。真實 cuBLAS 增益只有 +12% ～ +34%。</text>
<text x="68" y="538" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">INT8、INT4、dp4a、純 FP32 完全沒有變化；FP8 幾乎等於 0。</text>
<text x="68" y="560" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">限速器確實拆掉了，但變速箱齒比、輪胎抓地力、限速牌都沒變。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：媒體說的「翻倍」對上真實的 cuBLAS 增益——最上面那根是指令發射率（+100%），底下的真實矩陣乘法只有 +12% ～ +34%，FP8 幾乎等於 0。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG1 -->

### 第一層：指令發射率（確實接近 2 倍）

RTX 4090 的配對實測（`docs/evidence/rtx4090-pr1-matched/README.md`），同一張卡、同一個核心與驅動、同一個 450 W 上限、桌面維持運作：

| 模式 | Stock | Unlocked | 比值 |
| --- | ---: | ---: | ---: |
| FP16 / FP32 累加 | 160.4 TF/s | 320.4 TF/s | 1.998× |
| BF16 / FP32 累加 | 159.7 TF/s | 320.2 TF/s | 2.005× |
| TF32 / FP32 累加 | 80.138 TF/s | 159.453 TF/s | 1.990× |
| FP16 / FP16 累加 | 320.6 TF/s | 320.4 TF/s | 0.999× |
| INT8 / INT32 累加 | 641.1 TOP/s | 640.3 TOP/s | 0.999× |
| unsigned INT4 / INT32 | 1273.218 TOP/s | 1273.675 TOP/s | 1.000× |
| `dp4a` | 159.1 TOP/s | 159.1 TOP/s | 1.000× |
| 純 FP32 `ffma` | 76.4 TF/s | 76.3 TF/s | 0.999× |

**會翻倍的是 FP16、BF16、TF32 搭配 FP32 累加**；其餘全部維持原狀。

專案自己在 README 裡就把這層講得很清楚：

> These are instruction throughput measurements, **not application speedups**.

### 第二層：真實 cuBLAS GEMM（只快 12–34%）

這才是「你的程式會不會變快」的答案：

| N | 型別 | Stock TF/s | Unlocked TF/s | 比值 |
| --- | --- | ---: | ---: | ---: |
| 1024 | FP16 | 107.546 | 127.948 | 1.190× |
| 1024 | BF16 | 127.100 | 151.968 | 1.196× |
| 4096 | FP16 | 153.234 | 205.956 | 1.344× |
| 4096 | BF16 | 153.418 | 152.720 | **0.995×（無變化）** |
| 8192 | FP16 | 168.675 | 188.891 | 1.120× |
| 8192 | BF16 | 166.197 | 192.744 | 1.160× |

README 原文：「Real cuBLAS GEMM median throughput varied by shape: FP16 gained 12–34%, BF16 gained 16–20% at two shapes and was essentially unchanged at 4096³. These are one matched run pair with the desktop active, not whole-application speedups or an extended stability test.」

**而且在同一份報告的暖開機重複測試中，4096³ BF16 還比原始 stock 慢 8.2%。**

<!-- FIG2 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" role="img" aria-label="RTX 4090 六組 cuBLAS GEMM 配對實測的增幅：從 +34.4% 到 -0.5%，依矩陣形狀而變" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="998.5" height="598.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">六種形狀的實際增幅</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個解鎖，六種矩陣形狀的實際增幅（數字為 cuBLAS GEMM 中位吞吐 TF/s）</text>
<path d="M 240 148 L 240 490" fill="none" stroke="#7d8590" stroke-width="1.5"/>
<text x="48" y="203.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1024³</text>
<text x="48" y="221.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">小矩陣</text>
<text x="120" y="188" font-size="12.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FP16</text>
<rect x="240" y="170" width="620" height="26" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="240" y="170" width="117.61701969389837" height="26" rx="8" fill="#58a6ff55" stroke="#58a6ff" stroke-width="1.5"/>
<text x="367.6170196938984" y="188" font-size="13" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+19.0%</text>
<text x="120" y="204" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">107.5→127.9</text>
<text x="120" y="232" font-size="12.5" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">BF16</text>
<rect x="240" y="214" width="620" height="26" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="240" y="214" width="121.30731707317067" height="26" rx="8" fill="#c084fc55" stroke="#c084fc" stroke-width="1.5"/>
<text x="371.3073170731707" y="232" font-size="13" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+19.6%</text>
<text x="120" y="248" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">127.1→152.0</text>
<path d="M 48 268 L 952 268" fill="none" stroke="#30363d" stroke-width="1.2"/>
<text x="48" y="323.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4096³</text>
<text x="48" y="341.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">中矩陣</text>
<text x="120" y="308" font-size="12.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FP16</text>
<rect x="240" y="290" width="620" height="26" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="240" y="290" width="213.3184541289791" height="26" rx="8" fill="#58a6ff55" stroke="#58a6ff" stroke-width="1.5"/>
<text x="463.3184541289791" y="308" font-size="13" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+34.4%</text>
<text x="120" y="324" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">153.2→206.0</text>
<text x="120" y="352" font-size="12.5" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">BF16</text>
<rect x="240" y="334" width="620" height="26" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="236.0" y="334" width="4.0" height="26" rx="8" fill="#f472b655" stroke="#f472b6" stroke-width="1.5"/>
<text x="252" y="352" font-size="13" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">▼ -0.5%</text>
<text x="120" y="368" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">153.4→152.7</text>
<path d="M 48 388 L 952 388" fill="none" stroke="#30363d" stroke-width="1.2"/>
<text x="48" y="443.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8192³</text>
<text x="48" y="461.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">大矩陣</text>
<text x="120" y="428" font-size="12.5" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FP16</text>
<rect x="240" y="410" width="620" height="26" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="240" y="410" width="74.30810730695111" height="26" rx="8" fill="#58a6ff55" stroke="#58a6ff" stroke-width="1.5"/>
<text x="324.3081073069511" y="428" font-size="13" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+12.0%</text>
<text x="120" y="444" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">168.7→188.9</text>
<text x="120" y="472" font-size="12.5" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">BF16</text>
<rect x="240" y="454" width="620" height="26" rx="8" fill="#161b22" stroke="#7d859044" stroke-width="1"/>
<rect x="240" y="454" width="99.03391757973965" height="26" rx="8" fill="#c084fc55" stroke="#c084fc" stroke-width="1.5"/>
<text x="349.03391757973964" y="472" font-size="13" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+16.0%</text>
<text x="120" y="488" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">166.2→192.7</text>
<text x="240.0" y="514" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0%</text>
<text x="395.0" y="514" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+10%</text>
<text x="550.0" y="514" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+20%</text>
<text x="705.0" y="514" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+30%</text>
<text x="860.0" y="514" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">+40%</text>
<rect x="48" y="532" width="904" height="52" rx="10" fill="#1c2230" stroke="#f472b655" stroke-width="1.5"/>
<text x="68" y="554" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個解鎖，增益卻從 +34.4% 掉到 -0.5%：矩陣形狀決定一切。</text>
<text x="68" y="572" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">所以別拿 README 裡的單一數字當結論——請用自己的工作負載量一次。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：六組 cuBLAS GEMM 的實際增幅——同一個解鎖，增益卻從 +34.4% 掉到 -0.5%；矩陣形狀決定一切，別拿單一數字當結論。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG2 -->

> <strong>白話說</strong>：把限速器拆掉，引擎的出力上限從半速變全速了。但你的變速箱齒比、輪胎抓地力、路面都沒變，所以實際跑起來只快一成到三成多，某些齒比甚至幾乎沒反應，還可能倒退。這一點直接打掉了「所有 AI 工作負載都翻倍」的說法。

### 第三層：FP8（幾乎沒動）

專案自己公布的配對實測（4070 Ti SUPER，E4M3 FP8/FP32 CUTLASS GEMM）：

> A matched, verified E4M3 FP8/FP32 CUTLASS GEMM measured **59.326 TF/s stock → 59.495 TF/s unlocked** on this card, a **0.3%** difference. This single GEMM did not show a meaningful FP8 gain; other FP8 kernels remain untested.

**這是關鍵的反擊點**：媒體說 FP8「大幅提升」，而專案**自己**就寫明只有 0.3%。原始碼沒有隱瞞這件事，反而是二手報導自己加戲。引用第一手來源比引用第三方整理更有力。

## 誇大關鍵字三：「Windows 一鍵解鎖所有 RTX 40」

Windows 路徑**不是只有一個**資料點，但**兩個都不是通用工具**。

### 路線 A：Hugging Face 的 `AD103_win_unlocker`（改裝 4080）

model card 開頭就自我限定得很清楚：

> This is a compute-selector modification case on **one non-SUPER RTX 4080 AD103 modified to 32GB, not a 4080 SUPER**.

它的量測結果確實漂亮（WSL2、PyTorch 2.8.0+cu128 / CUDA 12.8、320 W 上限、32760 MiB）：

| GEMM N | 類型 | Baseline TFLOPS | Unlocked TFLOPS | 提升 |
| --- | --- | ---: | ---: | ---: |
| 4096 | FP32 | 34.55 | 35.07 | 1.52% |
| 4096 | FP16 → FP32 | 91.54 | 182.80 | **99.71%** |
| 4096 | BF16 → FP32 | 91.91 | 184.49 | **100.73%** |
| 8192 | FP32 | 33.42 | 33.69 | 0.80% |
| 8192 | FP16 → FP32 | 97.77 | 156.28 | 59.85% |
| 8192 | BF16 → FP32 | 97.76 | 167.64 | 71.48% |

但同一張 model card 也寫明了限制：

> The distributed EFI is pinned to `10de:2704` / `10de:1795` and a **specific ROM hash**. Another card with the same product name **may be rejected**. Editing identity/hash constants alone is **not a validated port**.
>
> No DLSS, RT, FP8 or application-level LLM speedup is claimed.

而且它的數值正確性只做到「抽樣的 FP64 比對 + 輸出 NaN/Inf 全掃」，model card 自己註明 **not exhaustive numerical or long-term stability certification**。

> <strong>白話說</strong>：這把鑰匙是**照著那一張卡的指紋配的**。同型號的另一張卡，指紋不同，開不了鎖。改掉識別碼不等於就配好了新鑰匙。

### 路線 B：repo 內建的 Windows AD104 移植（Latence.app 貢獻）

這是很多人會漏掉的一塊——`windows/ad104-msi/` 就在主 repo 裡，而且有實測數據：

> MSI RTX 4070 Ti（`10de:2782` / `1462:5132`）、MSI Z490 / MS-7C75 BIOS A.E0、i9-10850K、Windows build 26200.9168、NVIDIA 616.56

| cuBLAS 4096² GEMM | Stock TFLOP/s | After TFLOP/s | 變化 |
| --- | ---: | ---: | ---: |
| FP32 pedantic | 30.23 | 30.53 | +1.0% |
| FP16/FP32 | 84.08 | 151.43 | **+80.1%** |
| BF16/FP32 | 84.03 | 148.25 | **+76.4%** |

但 README 同樣把話說死：

> It is tied to **one captured MSI Z490 profile**; it **does not add AD104 admission to the Linux module**.
>
> **No firmware/Windows/ROM binaries or automatic boot installer are distributed.** No portable EFI binary is distributed.

操作方式是：自備 FAT32 USB、停用 Secure Boot（因為 EFI 沒簽章）、開機選 USB、按 `U` 鍵觸發交易、**沒有自動安裝、沒有自動重試、沒有失敗回滾**。

> <strong>白話說</strong>：Windows 這條路確實有人走通了，而且數據不難看。但你要自己備齊零件、照著一台特定的主機設定手動組裝。中間任何一步不對，結果就是開不了機——**這不是「一鍵」**。

### Windows 側的正確結論

兩個**彼此獨立**的單卡實驗（改裝 4080 與 MSI 4070 Ti AD104），兩者都是單卡單板型、都不通用、都不提供可攜的一鍵工具。這比「Windows 根本沒得用」精確得多，也比「Windows 一鍵可用」誠實得多。

## 各型號的公開證據總表

| 型號 | 專案狀態 | 已公開結果 | 證據強度 |
| --- | --- | --- | --- |
| **RTX 4090**（AD102, `10de:2684`） | 正式路徑 | 指令發射率 FP16/BF16→FP32 約 2×（165.6 → 331.6 TF/s）；實際 cuBLAS GEMM **僅 12–34%** | **最完整**：獨立第三方配對實測、數值驗證、遙測齊備 |
| **RTX 4070 Ti SUPER**（AD103, `10de:2705`） | 實驗性，需單一 PCI 位址 + `gpu_unlock.ad103_experimental=1` | 240 W 下 95.0 → 189.9 TF/s；TF32 1.99×；FP8 +0.3%；INT8 維持 379.5 TOP/s | 單卡；數值驗證通過；無長時間穩定性測試 |
| **RTX 4060 Ti 16GB**（AD106, `10de:2805`） | 實驗性，需單一 PCI 位址 + `gpu_unlock.ad106_experimental=1` | 單卡單次冷開機通過所有門檻、rate getter 轉全速；**沒有同卡 stock 對照** | **弱**：唯一沒有任何前後對照數據的型號 |
| **RTX 4090 D**（AD102, `10de:2685`） | 實驗性旗標 | 未公布效能數據 | 最低 |
| **RTX 4080 / 4080 SUPER** | **不支援** | — | 不在白名單；Issue #18 未獲回覆 |
| **Windows AD104**（MSI 4070 Ti `10de:2782`） | 單板型手動 UEFI 移植 | cuBLAS FP16/FP32 +80.1%、BF16/FP32 +76.4% | 單卡單板型；不散佈二進位；需停 Secure Boot |

另外，專案 README 自己引用的獨立使用者配對實測（revision `8855e7b`，Linux `7.2.11-arch1-1`，NVIDIA `615.78.08`，同一個 450 W 上限）量到 **160.4 → 320.4 TF/s**（FP16/FP32）與 **159.7 → 320.2 TF/s**（BF16/FP32），與專案自己的 165.6 → 331.6 數據一致——**這是本專案證據鏈最紮實的一環**。

## 查核過程中額外發現的三個問題

這三點不在一般報導裡，但對想自己動手的人很重要。

### 1. 晶片標示：4070 Ti SUPER 是 AD103，不是 AD104

坊間常把這張卡標成 AD104，但專案原始碼定義的是 AD103（`0x2705`）。專案 Issue #3 明確澄清：

> RTX 4070 Ti SUPER, device ID `10de:2689`. The repo's experimental 4070 Ti SUPER target is `10de:2705`. My card is a different die: **2689 is AD104, 2705 is AD103**.

同一款 4070 Ti SUPER 存在兩種晶片版本，**專案只收 AD103**。而專案裡的「AD104」指的是另一件事——Windows 那條 `windows/ad104-msi/` 移植（MSI 4070 Ti `10de:2782`）。把兩者混為一談會直接導致選錯路徑。

### 2. 4060 Ti 16GB 的 PCI ID 對不上

Issue #22 的實測回報：

> GPU: GeForce RTX 4060 Ti (AD106), PCI ID `10de:2803` rev a1 … VRAM: 16380 MiB
> In `kernel/gpu_unlock` the AD106 path is keyed to `GU_AD106_RTX_4060_TI_16GB (0x2805)` … so as far as I can tell the module would skip this card.

**實務上很多 4060 Ti 16GB 回報的是 `0x2803`，模組會直接略過。** 也就是說「4060 Ti 16GB 支援」這句話，連能不能被辨識都不保證。

### 3. 上游自己的程式碼註解與文件不一致

`arch_610.h`、`unlock_610.c` 與 `main.c` 的 `ad106_experimental` 說明**至今仍寫著 `untested on silicon`**，但 `docs/ada-2805-report.md`（2026-10-24）已經記錄了單卡實測通過。

這不是本文要挑作者的毛病，而是提醒讀者：**引用時請以 `docs/` 的報告為準並註明版本**，`arch_610.h` 的註解在 1.1.1 裡落後了。專案自己也定義了三層驗證等級（`docs/testing.md`）：主機回歸測試通過 ≠ 韌體交易真的跑過 ≠ 應用程式會變快——**三者不能互相替代**。

## 關於功耗：媒體說法與實測恰好相反

媒體版本常說「解除限速後效能提升，必然伴隨更高功耗與散熱壓力」。前半句在直覺上合理，但這份配對實測的遙測不支持：

| 量測項目 | Stock | Unlocked |
| --- | --- | --- |
| SM clock 範圍 | 2655–2670 MHz | 2610–2670 MHz |
| GPU 溫度範圍 | 50–68 °C | 54–73 °C |
| 最大功耗取樣 | 307.67 W | 308.59 W |

配對條件是同一張卡、同一個核心、同一個驅動、同一個 450 W 功耗上限、取樣間隔約 100 ms。**功耗幾乎沒動，溫度略升 6 °C**。

更關鍵的佐證在 4070 Ti SUPER：**在完全相同的 240 W 功耗上限下**，FP16 指令速率從 95.0 直接翻到 189.9 TF/s。

> <strong>白話說</strong>：車子本來就被「限速牌」壓在 60 檔（功耗上限）。你把引擎的電子限速拆掉，它不會「多吃油」，因為油箱和引擎出力都被同一個上限管著——你得到的是**每公升跑更多公里**。真正會變差的是「長時間全油門時的散熱與供電裕度」，以及**你完全沒有長期穩定性資料**這件事。

順帶把另一個常見誤解講清楚：「驅動／CUDA 更新後就會失效」也過度概括了。韌體資產是釘在 NVIDIA **610.43.03**（並逐檔 SHA-256 檢核），而解鎖交易在 `580.178.04`、`595.99.02`、`615.78.08`、`616.56` 多個驅動版本上都正常運作。真正需要重做的是：**核心模組隨核心版本重新編譯、initramfs 重新生成**（Linux 端每次核心更新都要做）。

## 風險與建議

### 風險是真的，但理由要精確

上游的 model card 寫得很直接：

> You assume the risk of deciding to use and run this software. **Boot failure, loss of display, data corruption, hardware damage** and other losses are possible. It is provided AS IS without warranty.

技術上會碰到的東西：initramfs 內的核心模組、UEFI／開機項、Secure Boot、PCIe FLR、底層暫存器寫入。這不是「一般驅動更新」等級的操作。

另外幾個容易踩到的實務陷阱：

- **首次嘗試必須完整切斷 AC 電源再開機。** 暖開機不保證提供乾淨的韌體狀態。專案的 `WPR2` 標記若為高，模組會**拒絕重跑**交易（實測 2705 暖開機可通過，其他板卡不保證）。
- **不要在冷開機嘗試前跑 `nvidia-smi`、CUDA、NVML 或 `nvidia-modprobe`**，它們可能用名字把 NVIDIA 驅動載進來，模組就沒機會了。README 明說：一般 modprobe blacklist 擋不住這種明確指名載入。
- **「模組載入成功」不等於解鎖成功。** 必須看到**目標卡**的 `gpu_unlock: unlocked`，加上健康的 `nvidia-smi` 與 rate readback。
- **顯示交接與多卡運作不在 RTX 4090 的驗證範圍內**，README 明確標註。
- Linux 端如果 Secure Boot 是開的，可以用 MOK 本機金鑰簽署模組來處理（2805 報告即用此法）；**需要停用 Secure Boot 的是 Windows 端那支未簽章的 EFI**。兩件事常被混為一談。

### 如果你真的要試

| 你的情況 | 建議 |
| --- | --- |
| **RTX 4090** | 唯一公開證據較完整的對象。仍應在**可還原的 Linux 測試機**上做：保留一個正常開機項、先收集 stock 基線（同一核心／驅動／binary／功耗上限）、再比對解鎖後的結果 |
| **RTX 4070 Ti SUPER** | 視為實驗性單卡路徑。必須確認你的卡是 **`10de:2705`（AD103）**，並用 `gpu_unlock.targets=<單一 PCI 位址>` + `gpu_unlock.ad103_experimental=1` |
| **RTX 4060 Ti 16GB** | 證據最弱的一條。**先確認 PCI ID 是 `0x2805` 而不是 `0x2803`**，而且要知道目前**根本沒有同卡 stock 對照數據** |
| **RTX 4080 / 4080 SUPER** | 不支援。HF 那個是改裝 32 GB 的非 SUPER 4080，不能直接套用 |
| **Windows 使用者** | 兩條路都是單板型手動流程，需要 USB 開機、停 Secure Boot、手動組裝資產，**沒有自動安裝與自動回滾** |

**不建議**拿主力工作機、雙系統日常機、或任何有商用 SLA 的機器直接嘗試。

## 給不同身份的讀者

- **只看新聞的讀者**：這件事是真的技術路線，值得知道；但如果你的決策會依賴「快 2 倍」這個前提，請記得實際 GEMM 增益是 12–34%。
- **有 4090 想知道值不值得試**：可以試，但先在測試機上跑自己的 GEMM 基準比較，不要用 README 的數字做決策。專案自己的測試指南（`docs/testing.md`）就是教人怎麼收集 stock 與 unlocked 兩組配對資料。
- **有 4070 Ti SUPER 或 4060 Ti**：先確認 PCI ID，再確認你的負載型態是否吃得到 FP16/BF16 的矩陣運算。跑 transformer 的 prefill 或大矩陣乘法可能明顯受益；跑 INT8 量化推論、影像生成或遊戲，**幾乎確定沒有變化**。
- **做 AI 推論服務的**：請特別注意本專案**沒有任何**代表性推論或訓練工作負載的量測資料，`docs/testing.md` 把它列為「後續仍待補的測試」。
- **看到「RTX 40 被破解」標題就轉發的**：本文的核心是——**研究方向是真的，媒體標題是假的**。兩者可以同時成立。

## 查核方法與可重現性

本文**沒有用搜尋摘要**，全部數字直接取自一手檔案：

| 來源 | 用途 |
| --- | --- |
| `kernel/gpu_unlock/arch_610.h` | 裝置 ID 白名單（權威） |
| `kernel/gpu_unlock/main.c` | 實驗旗標參數定義與 `targets` 語意 |
| `kernel/gpu_unlock/unlock_610.c` | Ada 路徑判定與註解 |
| `README.md` | 型號清單、旗標用法、效能數字、Windows 貢獻段落 |
| `QUICKSTART.md` | 冷開機要求、旗標用法、回滾步驟 |
| `docs/release-1.1.1.md` | TF32／INT4 對照數據 |
| `docs/ada-2805-report.md` | 4060 Ti 單卡實測、**無 stock 對照**的聲明 |
| `docs/evidence/rtx4090-pr1-matched/README.md` | 4090 配對實測：指令率、GEMM、遙測、暖開機重複測試 |
| `docs/ad104-windows-latence-app.md` | Windows AD104 實測 |
| `docs/testing.md` | 三層驗證分級定義 |
| `firmware/NOTICE.md` | payload 來源與「重現位元組不等於執行期結果」的自省聲明 |
| GitHub Issues API | #3（AD103/AD104）、#18（4080 SUPER）、#22（`0x2803` vs `0x2805`） |
| Hugging Face model card | 改裝 4080 的量測、EFI 釘選限制、風險聲明 |

查核時另發現上游 `arch_610.h` 的註解仍寫 AD106「untested on silicon」，與 `docs/ada-2805-report.md` 已記錄的單卡實測不一致——這是上游 1.1.1 文件更新落後，引用時建議以 `docs/` 報告為準並註明版本。

## 參考資料

- 專案首頁：[github.com/JustAResearcher/gpu-unlock-ada](https://github.com/JustAResearcher/gpu-unlock-ada)（v1.1.1）
- 快速開始：[QUICKSTART.md](https://github.com/JustAResearcher/gpu-unlock-ada/blob/main/QUICKSTART.md)
- 4090 配對實測：[docs/evidence/rtx4090-pr1-matched/README.md](https://github.com/JustAResearcher/gpu-unlock-ada/tree/main/docs/evidence/rtx4090-pr1-matched)
- 4070 Ti SUPER 報告：[docs/ada-2705-report.md](https://github.com/JustAResearcher/gpu-unlock-ada/blob/main/docs/ada-2705-report.md)
- 4060 Ti 報告：[docs/ada-2805-report.md](https://github.com/JustAResearcher/gpu-unlock-ada/blob/main/docs/ada-2805-report.md)
- Windows AD104 移植：[windows/ad104-msi/README.md](https://github.com/JustAResearcher/gpu-unlock-ada/tree/main/windows/ad104-msi)
- 韌體出處聲明：[firmware/NOTICE.md](https://github.com/JustAResearcher/gpu-unlock-ada/blob/main/firmware/NOTICE.md)
- Hugging Face 改裝 4080 實驗：[TOTORONG/AD103_win_unlocker](https://huggingface.co/TOTORONG/AD103_win_unlocker)
- 上游 Ampere 專案：[Zagitta/gpu-unlock](https://github.com/Zagitta/gpu-unlock)

---

> <strong>最後一話</strong>：真正值得肯定的不是「RTX 40 被破解」這種口號，而是這個專案把**原始碼、雜湊固定的韌體資產、可重現的產生流程、配對實測、數值驗證、以及公開的限制與失敗聲明**全都放出來了——包括「我的實驗只覆蓋一張卡」「這不是應用程式加速」「FP8 幾乎沒變」這種對自己不利但誠實的句子。
>
> 媒體把這條技術路線壓縮成三個關鍵字，而那三個關鍵字一個都不成立。**研究是真的，標題是假的。**
