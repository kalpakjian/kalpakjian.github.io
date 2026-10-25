---
title: RTX 4090 解除 gpu-unlock 操作筆記：不用實驗旗標，但「2 倍」要打折
date: 2026-10-25 22:30:00
categories:
  - 技術筆記
tags:
  - GPU
  - NVIDIA
  - RTX
  - CUDA
  - Linux
  - 開源
  - 實作
  - 效能實測
  - 基準測試
  - PyTorch
  - 深度學習
toc: true
index_img: /img/covers/rtx4090-gpu-unlock-guide.png
banner_img: /img/covers/rtx4090-gpu-unlock-guide.png
---

> <strong>整理說明</strong>：這是給 <strong>RTX 4090</strong> 這張特定卡的操作筆記。資料來源是上游專案 <a href="https://github.com/JustAResearcher/gpu-unlock-ada">JustAResearcher/gpu-unlock-ada</a> v1.1.1 的 QUICKSTART、README、<code>docs/testing.md</code>、<code>docs/evidence/rtx4090-pr1-matched/</code>，以及 Issue #17 的 4090 實測回報。所有指令都照抄上游，沒有多加任何我自己發明的步驟。

<!-- more -->

## 先講結論

**4090 是整個生態系裡最簡單、最有保障的一條路。** 三個原因：

1. **它是唯一不需要實驗旗標的目標。** 4070 Ti SUPER 與 4060 Ti 16GB 還要加 `ad103_experimental=1`／`ad106_experimental=1`，而且 `targets=all` 永遠不會選中它們。4090 只要 `gpu_unlock.targets=<位址>` 一項。
2. **它是證據鏈最完整的一個。** 有獨立的配對實測報告（stock／unlocked 同一張卡、同一核心、同一驅動、同一 450 W 上限）、六組種子數值驗證、時脈／溫度／功耗遙測，以及一個改裝 48GB 版的實測回報。
3. **它有真正能讀回驗證的工具。** `tools/read_sm_rates.py` 用 NVIDIA 公開的 RM getter 讀出速率選擇器，解鎖後 `fmla32` 會從 `1`（半速）變成 `0`（全速）——這是「確認真的解鎖了」最直接的證據。

**但有一件事要先打折：媒體說的「2 倍」是指令發射率，不是你的程式快 2 倍。**

| 層級 | 4090 實測 | 比值 |
| --- | --- | ---: |
| FP16 → FP32 累加 指令發射率 | 160.4 → 320.4 TF/s | 1.998× |
| BF16 → FP32 累加 指令發射率 | 159.7 → 320.2 TF/s | 2.005× |
| TF32 → FP32 累加 指令發射率 | 80.1 → 159.5 TF/s | 1.990× |
| **真實 cuBLAS GEMM（最佳，4096³ FP16）** | 153.2 → 206.0 TF/s | **1.344×** |
| **真實 cuBLAS GEMM（4096³ BF16）** | 153.4 → 152.7 TF/s | **0.995×（等於沒變）** |

所以你的預期應該是：**真實矩陣乘法大約快 12～34%**，而不是兩倍。

## 這張卡在白名單裡，而且不用旗標

Ada 分支 `kernel/gpu_unlock/arch_610.h` 的白名單只有四個 ID：

```c
#define GU_AD103_RTX_4070_TI_SUPER 0x2705u   /* 實驗性 */
#define GU_AD106_RTX_4060_TI_16GB   0x2805u   /* 實驗性 */
#define GU_AD102_RTX_4090_D         0x2685u   /* 實驗性 */
```

而 `0x2684`（你的 RTX 4090）**由既有的允許清單直接選中**，不需要任何額外旗標。模組參數只有四個：

```c
gpu_unlock.targets              # "all" 或逗號分隔的 PCI 位址
gpu_unlock.ad103_experimental   # 只允許 10de:2705，必須單一明確位址
gpu_unlock.ad106_experimental   # 只允許 10de:2805，必須單一明確位址
gpu_unlock.rtx4090d_experimental # 實驗性的 10de:2685
```

> **注意 Ada 分支沒有 `resume` 這個模組參數**（Ampere 上游 `Zagitta/gpu-unlock` 才有）。如果你在網路上看到 `gpu_unlock.resume=0`，那是 Ampere 版的指令，Ada 版沒有這個開關。

## 六步操作流程

<!-- FIG1 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 640" role="img" aria-label="RTX 4090 解除 gpu-unlock 的六步操作流程：確認白名單、安裝、設定核心命令列、冷開機、驗證 gpu_unlock: unlocked、讀回速率並量自己的負載" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker><marker id="m2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker><marker id="mf472b6" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#f472b6"/></marker></defs>
<rect x="0.75" y="0.75" width="998.5" height="638.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">六步操作流程</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4090 是唯一不需要實驗旗標的</text>
<rect x="48" y="126" width="556" height="64" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<circle cx="76" cy="158.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="76" y="162.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<text x="102" y="150" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">確認白名單並取得位址</text>
<text x="102" y="170" font-size="10" fill="#58a6ff" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">python3 tools/print_boot_option.py</text>
<text x="102" y="184" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">唯讀工具，會直接印出要用的那行</text>
<rect x="48" y="210" width="556" height="64" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<circle cx="76" cy="242.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="76" y="246.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text>
<text x="102" y="234" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">安裝套件</text>
<text x="102" y="254" font-size="10" fill="#58a6ff" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">git clone … &amp;&amp; cd gpu-unlock-ada &amp;&amp; make install</text>
<text x="102" y="268" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Arch／Debian／RPM 自動偵測</text>
<path d="M 76 206 L 76 190" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="294" width="556" height="64" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<circle cx="76" cy="326.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="76" y="330.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text>
<text x="102" y="318" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">設定核心命令列</text>
<text x="102" y="338" font-size="10" fill="#58a6ff" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">gpu_unlock.targets=0000:03:00.0</text>
<text x="102" y="352" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4090 只要這一項，不需要實驗旗標</text>
<path d="M 76 290 L 76 274" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="378" width="556" height="64" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<circle cx="76" cy="410.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="76" y="414.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<text x="102" y="402" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">完整斷電後冷開機</text>
<text x="102" y="422" font-size="10" fill="#58a6ff" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">切掉 AC 電源、等約 30 秒再上電</text>
<text x="102" y="436" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">暖開機不保證提供乾淨韌體狀態</text>
<path d="M 76 374 L 76 358" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="462" width="556" height="64" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<circle cx="76" cy="494.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="76" y="498.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text>
<text x="102" y="486" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">驗證是否真的解鎖</text>
<text x="102" y="506" font-size="10" fill="#58a6ff" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">journalctl -k -b | grep gpu_unlock</text>
<text x="102" y="520" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">要找 gpu_unlock: unlocked</text>
<path d="M 76 458 L 76 442" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="546" width="556" height="64" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<circle cx="76" cy="578.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="76" y="582.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text>
<text x="102" y="570" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">讀回速率並量自己的負載</text>
<text x="102" y="590" font-size="10" fill="#58a6ff" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">python3 tools/read_sm_rates.py --expect-uuid …</text>
<text x="102" y="604" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">唯讀，不寫暫存器、不重置</text>
<path d="M 76 542 L 76 526" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="636" y="126" width="316" height="78" rx="10" fill="#1c2230" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="652" y="152" font-size="12.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4090 是唯一不用實驗旗標的</text>
<text x="652" y="174" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4070 Ti SUPER 與 4060 Ti 16GB 還要加</text>
<text x="652" y="190" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ad103／ad106_experimental=1 這類旗標。</text>
<path d="M 608 158.0 L 632 158.0" fill="none" stroke="#2dd4bf" stroke-width="1.5" marker-end="url(#m2dd4bf)"/>
<rect x="636" y="462" width="316" height="78" rx="10" fill="#1c2230" stroke="#f472b666" stroke-width="1.5"/>
<text x="652" y="488" font-size="12.5" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">模組載入成功 ≠ 解鎖成功</text>
<text x="652" y="510" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">必須看到目標卡的 gpu_unlock: unlocked，且 nvidia-smi 健康、</text>
<text x="652" y="526" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">journal 裡沒有 NVRM: Xid。</text>
<path d="M 608 494.0 L 632 494.0" fill="none" stroke="#f472b6" stroke-width="1.5" marker-end="url(#mf472b6)"/>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：六步操作流程——4090 只需 gpu_unlock.targets 一項（4070 Ti SUPER 與 4060 Ti 還要實驗旗標），而「模組載入成功」不等於「解鎖成功」。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG1 -->


下面是每一步的細節。

### 步驟 0：用唯讀工具取得位址

Ada 分支附了一支很好用的唯讀工具，它會直接印出你要填的那一行：

```sh
python3 tools/print_boot_option.py
```

輸出長這樣：

```text
RTX 4090 at 0000:03:00.0 [10de:2684]:
gpu_unlock.targets=0000:03:00.0
```

它的比對邏輯是 `\[10de:(2684|2685|2705|2805)\]`，而且**完全不動主機狀態**。

如果它印出 *"No supported RTX 4090 (10de:2684) … was found"*，代表你的卡不在白名單裡——常見原因是 4090 D（`0x2685`，需要 `rtx4090d_experimental=1`）或改裝卡。

### 步驟 1：安裝

```sh
git clone https://github.com/JustAResearcher/gpu-unlock-ada.git
cd gpu-unlock-ada
make install
```

`make install` 會偵測發行版（Arch／Debian／Ubuntu／Fedora／RHEL／CentOS）。也可以指定：

```sh
make install-arch   # makepkg -sif
make install-deb    # apt-get build-dep, dpkg-buildpackage, apt-get install
make install-rpm    # dnf builddep, rpmbuild, dnf install
```

建置會下載**雜湊釘死的** NVIDIA 610.43.03 輸入並在本地產生韌體資產；套件本身不含 NVIDIA 韌體的散佈副本。

### 步驟 2：設定核心命令列

把步驟 0 印出來的那一行加進你的開機程式：

| 開機程式 | 做法 |
| --- | --- |
| GRUB（Debian／Ubuntu） | 在 `/etc/default/grub` 的 `GRUB_CMDLINE_LINUX_DEFAULT` **既有引號內**追加，然後 `sudo update-grub` |
| GRUB（Arch） | 同樣編輯，然後 `sudo grub-mkconfig -o /boot/grub/grub.cfg` |
| Fedora／RHEL | `sudo grubby --update-kernel=ALL --args="gpu_unlock.targets=0000:03:00.0"` |
| systemd-boot | 在對應 entry 的 `options` 行追加（`bootctl status` 會顯示位置） |
| UKI | 加到 `/etc/kernel/cmdline`，再重新產生開機映像 |

> **單卡主機用 `targets=all` 也行**（4090 會被選中），但上游建議明確寫位址：*"an explicit address is useful when selecting one RTX 4090"*。第一次測試用明確位址比較安全。

### 步驟 3：冷開機

上游 QUICKSTART 的步驟 4 原文：

> Shut down cleanly. **Cut AC power to the machine, wait about 30 seconds, then restore power** and start it. This gives the first test a fresh card state.

理由是晶片上的 **WPR2** 標記：冷開機會把它清成 `0`，模組才願意跑交易。**暖開機不保證提供乾淨狀態**，上游說得很直接：*"A warm reboot is not guaranteed to provide that state."*

### 步驟 4：驗證

```sh
journalctl -k -b --no-pager | grep -E 'gpu_unlock: unlocked|gpu_unlock: unlock failed|post-FLR SEC2'
nvidia-smi
```

**判準：必須看到目標卡的 `gpu_unlock: unlocked`。** 上游 README 特別強調：*"A loaded module or successful modprobe return alone does not prove an unlock."*

### 步驟 5：讀回速率（這是 4090 專屬的優勢）

```sh
python3 tools/read_sm_rates.py --expect-uuid GPU-PASTE-YOUR-EXACT-UUID
```

這支工具的自我描述：

> Read current SM issue-rate selectors using NVIDIA's public RM getter. **No BAR mapping, register write, firmware upload, reset, CUDA context or kernel.** ABI: NVIDIA open-gpu-kernel-modules 610.43.03.

解鎖前後的差異就是 `fmla32` 從 `1`（半速）變成 `0`（全速）。這比「我感覺好像變快了」可靠得多。

> **前置條件**：它走的是 **open GPU kernel modules** 的 ABI（`ctrl2080gr.h`、`cl0080.h`）。如果你用的是專有驅動分支，這支工具可能不能用。

## 兩層數字：2 倍是指令率，不是你的程式

<!-- FIG2 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 560" role="img" aria-label="RTX 4090 的兩層數字：指令發射率接近 2 倍，但真實 cuBLAS GEMM 只有 +12% 到 +34%，4096³ BF16 甚至是 0.995×" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="998.5" height="558.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩層數字</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">指令率 ≠ 你的程式</text>
<rect x="48" y="118" width="440" height="330" rx="12" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="68" y="148" font-size="14" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">指令發射率（register-resident）</text>
<text x="68" y="170" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">最底層的指令率——媒體說的「翻倍」是這一層</text>
<text x="68" y="206" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FP16 / FP32 累加</text>
<text x="68" y="222" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">160.4 → 320.4 TF/s</text>
<rect x="300" y="194" width="170" height="20" rx="6" fill="#2dd4bf55" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="466" y="209" font-size="12.5" fill="#2dd4bf" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2.00×</text>
<text x="68" y="250" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">BF16 / FP32 累加</text>
<text x="68" y="266" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">159.7 → 320.2 TF/s</text>
<rect x="300" y="238" width="170" height="20" rx="6" fill="#2dd4bf55" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="466" y="253" font-size="12.5" fill="#2dd4bf" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2.00×</text>
<text x="68" y="294" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">TF32 / FP32 累加</text>
<text x="68" y="310" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">80.1 → 159.5 TF/s</text>
<rect x="300" y="282" width="170" height="20" rx="6" fill="#2dd4bf55" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="466" y="297" font-size="12.5" fill="#2dd4bf" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.99×</text>
<rect x="512" y="118" width="440" height="330" rx="12" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.5"/>
<text x="532" y="148" font-size="14" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">真實 cuBLAS GEMM</text>
<text x="532" y="170" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">這才是「你的程式會不會變快」</text>
<text x="532" y="205" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4096³ FP16</text>
<rect x="700" y="193" width="133.20000000000002" height="18" rx="5" fill="#58a6ff55" stroke="#58a6ff" stroke-width="1.5"/>
<text x="932" y="206" font-size="12" fill="#58a6ff" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.344×</text>
<text x="532" y="245" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1024³ BF16</text>
<rect x="700" y="233" width="88.79999999999998" height="18" rx="5" fill="#58a6ff55" stroke="#58a6ff" stroke-width="1.5"/>
<text x="932" y="246" font-size="12" fill="#58a6ff" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.196×</text>
<text x="532" y="285" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1024³ FP16</text>
<rect x="700" y="273" width="86.99999999999997" height="18" rx="5" fill="#58a6ff55" stroke="#58a6ff" stroke-width="1.5"/>
<text x="932" y="286" font-size="12" fill="#58a6ff" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.190×</text>
<text x="532" y="325" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8192³ BF16</text>
<rect x="700" y="313" width="77.99999999999997" height="18" rx="5" fill="#58a6ff55" stroke="#58a6ff" stroke-width="1.5"/>
<text x="932" y="326" font-size="12" fill="#58a6ff" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.160×</text>
<text x="532" y="365" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8192³ FP16</text>
<rect x="700" y="353" width="66.00000000000003" height="18" rx="5" fill="#58a6ff55" stroke="#58a6ff" stroke-width="1.5"/>
<text x="932" y="366" font-size="12" fill="#58a6ff" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.120×</text>
<text x="532" y="405" font-size="11.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4096³ BF16</text>
<rect x="700" y="393" width="28.499999999999993" height="18" rx="5" fill="#f472b655" stroke="#f472b6" stroke-width="1.5"/>
<text x="932" y="406" font-size="12" fill="#f472b6" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.995×</text>
<rect x="48" y="462" width="904" height="82" rx="10" fill="#161b22" stroke="#fbbf2455" stroke-width="1.5"/>
<text x="68" y="488" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">完全沒有變化的路徑：FP16 搭 FP16 累加、INT8、unsigned INT4、dp4a、純 FP32。</text>
<text x="68" y="510" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">真實 GEMM 的增益依矩陣形狀而變：4096³ BF16 是 0.995×（等於沒變），同一次暖開機重測還慢了 8.2%。</text>
<text x="68" y="534" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">資料來源：docs/evidence/rtx4090-pr1-matched/README.md（獨立使用者配對實測，450 W 上限）。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：左邊是指令發射率（媒體說的「翻倍」），右邊是真實 cuBLAS GEMM——12% 到 34%，而且 4096³ BF16 等於沒變。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG2 -->


這是整篇最重要的一段。配對實測（`docs/evidence/rtx4090-pr1-matched/README.md`）的條件是：同一張卡、同一個核心 `7.2.11-arch1-1`、同一個驅動 `615.78.08`、同一個 CUDA `13.4.92`、同一個 450 W 上限、桌面維持運作。

**第一層：指令發射率接近 2×**

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

**第二層：真實 cuBLAS GEMM 只有 12～34%**

| N | 型別 | Stock | Unlocked | 比值 |
| --- | --- | ---: | ---: | ---: |
| 4096 | FP16 | 153.234 | 205.956 | 1.344× |
| 1024 | BF16 | 127.100 | 151.968 | 1.196× |
| 1024 | FP16 | 107.546 | 127.948 | 1.190× |
| 8192 | BF16 | 166.197 | 192.744 | 1.160× |
| 8192 | FP16 | 168.675 | 188.891 | 1.120× |
| 4096 | BF16 | 153.418 | 152.720 | **0.995×** |

README 原文：*"Real cuBLAS GEMM median throughput varied by shape: FP16 gained 12–34%, BF16 gained 16–20% at two shapes and was essentially unchanged at 4096³. These are one matched run pair with the desktop active, not whole-application speedups or an extended stability test."*

而且在暖開機的重複測試中，4096³ BF16 **比原始 stock 還慢 8.2%**。

> <strong>白話說</strong>：限速器確實拆掉了，但變速箱齒比、輪胎抓地力、限速牌都沒變——所以實際只快一成到三成多，某些齒比甚至幾乎沒反應。

## 你的負載吃得到嗎

<!-- FIG3 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" role="img" aria-label="RTX 4090 解鎖後哪些負載會變快：FP16／BF16 權重搭配 FP32 累加會，而 INT8、4-bit、3-bit 量化權重不會——Issue #17 實測 3-bit MoE 為 0.983×" style="width:100%;height:auto;display:block">
<defs><marker id="m2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="998.5" height="498.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">我的負載會變快嗎</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">分水嶺在權重精度</text>
<rect x="48" y="122" width="904" height="58" rx="12" fill="#1c2230" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="500" y="146" font-size="12" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">關鍵分水嶺</text>
<text x="500" y="168" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">權重是 FP16／BF16（而且累加走 FP32）嗎？</text>
<rect x="48" y="212" width="440" height="176" rx="12" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="68" y="240" font-size="14" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">是 → 會變快（真實 GEMM +12～34%）</text>
<text x="68" y="273" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・LLM prefill</text>
<text x="68" y="289" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">　　prompt 一次算完的那段</text>
<text x="68" y="317" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・擴散模型／圖片生成</text>
<text x="68" y="333" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">　　UNet 與 VAE 的矩陣乘法</text>
<text x="68" y="361" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・FP16／BF16 的訓練</text>
<text x="68" y="377" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">　　反向傳播也是矩陣乘法</text>
<rect x="512" y="212" width="440" height="176" rx="12" fill="#161b22" stroke="#7d859055" stroke-width="1.5"/>
<text x="532" y="240" font-size="14" fill="#7d8590" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不是 → 幾乎沒差</text>
<text x="532" y="273" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・INT8／4-bit／3-bit 量化權重</text>
<text x="532" y="289" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">　　Issue #17：3-bit MoE IQ3_S 實測 0.983×</text>
<text x="532" y="317" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・純 FP32 運算</text>
<text x="532" y="333" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">　　這條路徑本來就沒被鎖</text>
<text x="532" y="361" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・逐 token 生成（decode）</text>
<text x="532" y="377" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">　　瓶頸在記憶體頻寬</text>
<path d="M 340 180 L 268 208" fill="none" stroke="#2dd4bf" stroke-width="1.8" marker-end="url(#m2dd4bf)"/>
<path d="M 660 180 L 732 208" fill="none" stroke="#7d8590" stroke-width="1.8" marker-end="url(#m7d8590)"/>
<rect x="48" y="404" width="904" height="84" rx="10" fill="#1c2230" stroke="#f472b655" stroke-width="1.5"/>
<text x="68" y="430" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">最容易被忽略的一句：Issue #17 的實測者用 3-bit MoE（IQ3_S）跑 8K prefill，</text>
<text x="68" y="452" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">得到的比值是 0.983×——完全沒有加速。原文寫得很直接：</text>
<text x="68" y="476" font-size="13" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">「The 2x lands only on FP16/BF16 weights with FP32 accumulation.」</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 3：負載分流的分水嶺在權重精度——量化權重（3-bit MoE 實測 0.983×）完全吃不到解鎖帶來的加速。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG3 -->


| 你的用法 | 預期 | 理由 |
| --- | --- | --- |
| LLM **prefill**（FP16／BF16 權重） | **+12～34%** | 這是純矩陣乘法，正好吃滿解鎖後的速率 |
| 擴散模型／圖片生成（FP16） | 明顯受惠 | UNet 與 VAE 都是矩陣乘法 |
| FlashAttention | 受惠 | 注意力核心是矩陣乘法 |
| FP16／BF16 的訓練 | 受惠 | 反向傳播也是矩陣乘法 |
| **INT8／4-bit／3-bit 量化權重** | **幾乎沒差** | 見下方 Issue #17 的實測 |
| 純 FP32 運算 | 幾乎沒差 | 這條路徑本來就沒被鎖 |
| LLM **逐 token 生成**（decode） | 幾乎不變 | 瓶頸在 909 GB/s 記憶體頻寬，不在算力 |
| 遊戲 | 不會變快 | 遊戲不走 FP16／BF16 累加這條路徑 |

### Issue #17 的一句話，可能是整份文件裡最重要的一句

Issue #17 的實測者用的是**中國市場改裝成 48 GB 的 4090**（AD102、`10de:2684`、VBIOS `95.02.3C.00.02`、Ubuntu 26.04、核心 `7.0.0-38-generic`、NVIDIA `610.57.04` open kernel modules、v1.1.1），結果是：

- `gpu_unlock: unlocked`
- RM getter `fmla32/imla2/imla4` 從 `1` 變 `0`
- FP16/FP32 **164.9 → 328.9 TF/s（1.995×）**、BF16/FP32 **164.8 → 328.7**
- INT8／`dp4a`／scalar 不變、30 分鐘負載後 **零 Xid**、六組種子數值完全精確

但他同時寫了這段警告，值得逐字讀：

> **Worth knowing before you try it on a quantized model:** on our workload (**3-bit MoE, IQ3_S**) it gave **no speedup at all** — 8K prefill **0.983×**. The 2x lands only on FP16/BF16 weights with FP32 accumulation.

**如果你跑的是量化權重（Ollama 常見的 Q4／Q5、EXL2、或 3-bit MoE），這件事對你幾乎等於零。**

## 功耗與穩定性：實際數字比想像溫和

配對實測的遙測（取樣間隔約 100 ms）：

| 量測 | Stock | Unlocked |
| --- | --- | --- |
| SM clock 範圍 | 2655–2670 MHz | 2610–2670 MHz |
| GPU 溫度範圍 | 50–68 °C | 54–73 °C |
| 最大功耗取樣 | 307.67 W | 308.59 W |

**功耗幾乎沒變。** 原因是 4090 本來就被 450 W 上限壓住，解除速率限制後吃掉的是既有功耗預算——這是**效率**提升，不是耗電提升。

但真正該擔心的是別的：

- **上游只做了一組配對、沒有長時間穩定性測試。** Issue #17 的實測者跑了約 30 分鐘零 Xid，這是目前公開資料裡最長的負載記錄。
- **顯示交接與多卡運作不在 RTX 4090 的驗證範圍內。** 上游 README 明確標註：*"Display handoff and multi-card operation were not part of the RTX 4090 validation."* 如果你的 4090 是顯示卡而且主機有多張卡，這是未知的部分。
- **暖開機可能不提供乾淨狀態**，模組會「安全地拒絕」——那不是壞掉，只是沒解鎖。

## 常見坑

| 症狀 | 原因 | 解法 |
| --- | --- | --- |
| 模組根本沒載入 | 用了自訂 initramfs 設定（`-c` 或 preset `_config` 不讀 drop-in） | 手動把 `gpu_unlock` 加到 `MODULES` 裡、放在 `nvidia` 前面 |
| `-EBUSY` | initramfs 裡 `nvidia.ko` 比 `gpu_unlock` 先綁卡 | 確認 drop-in 有正確安裝 |
| 沒有 `gpu_unlock: unlocked` | 非冷開機、WPR2 還留著 | 完全斷電 30 秒後重開 |
| `read_sm_rates.py` 跑不動 | 用的是專有驅動分支 | 這支工具需要 **open GPU kernel modules** 的 ABI |
| 核心更新後模組不見 | initramfs 沒有重建 | 每次核心更新都要重建 initramfs（映像需指向重建後的版本） |

另外兩件上游特意提醒的事：

- **不要用 `softdep nvidia pre:`**。上游解釋：kmod 只會讀到**第一條** `softdep nvidia`，其他套件的規則會安靜地蓋掉它。
- **交易沒收尾時要完全斷電，而不是 `rmmod`。** 上游 README：*"If the firmware on a card never stops, the module logs it and keeps the DMA buffers that firmware may still use until the next power off. **Power off before trying again.**"*

## 回滾

| 想做的事 | 做法 |
| --- | --- |
| 只停用這一次開機 | 在開機程式的編輯畫面把 `gpu_unlock.targets=` 刪掉 |
| 永久停用 | 從核心命令列移除 `gpu_unlock.targets=`，重新產生開機映像 |
| 連套件一起移除 | 移除套件（模組與 initramfs drop-in 都會被移除） |

**隨時保留一個未修改的開機項**。上游的實測做法就是把正常項留著，需要時從開機選單切回去。

## 用官方流程做一次配對量測

Ada 分支的 `diagnostics/bench/` 是整套生態系裡最完整的量測工具（**Ampere 上游沒有這個目錄**）。`docs/testing.md` 定義了三層驗證：

| 層級 | 檢查什麼 | 現有證據 |
| --- | --- | --- |
| 主機回歸測試 | 資產釘選、拒絕／回收路徑、模擬交易 | 29 項測試通過；八個 C 元件通過 ASan/UBSan |
| 實際開機與驅動交接 | 指定卡的交易完成、NVIDIA 初始化、rate getter 改變 | 獨立使用者跑 `8855e7b`，核心 `7.2.11-arch1-1`，驅動 `615.78.08` |
| 工作負載檢查 | 兩種狀態下的數值與吞吐 | 六組種子 FP16/BF16 數值、六個大型 cuBLAS GEMM、指令／對照探針；一組配對 |

### 指令發射率探針

這是量「最底層那層」的官方工具：

```sh
nvcc -ptx -arch=sm_89 -O3 -std=c++17 \
  -o tensor_modes_issue_sm89.ptx diagnostics/bench/tensor_modes_issue.cu
ptxas -arch=sm_89 -O3 -o tensor_modes_issue_sm89.cubin \
  tensor_modes_issue_sm89.ptx
sha256sum tensor_modes_issue_sm89.cubin
python3 diagnostics/bench/tensor_modes_driver_runner.py \
  tensor_modes_issue_sm89.cubin \
  --sha256 PASTE-THE-CUBIN-SHA256 \
  --expect-uuid GPU-PASTE-YOUR-EXACT-UUID \
  --expect-power-limit 450
```

它會量 FP16/FP32、TF32/FP32 與 unsigned INT4/INT32 三種 `mma.sync` 指令發射率，跑 20,000 次迭代三次，並檢查每個模式的 270,336 個輸出格全部等於預期值。**要求 exact UUID、功耗上限與 cubin SHA-256**，這樣換一張卡或換一個 binary 就不會靜靜地混進配對比較。

### 數值正確性檢查

```sh
nvcc -O3 -arch=sm_89 -std=c++17 -o validate_gemm \
  diagnostics/bench/validate_gemm.cu -lcublas
```

用 cuBLAS 對 CPU 參考值，三組種子 FP16／BF16 輸入，方形、長方形與非 tile 對齊三種形狀，輸入值都是精確的二進位小數。

> **它能證明什麼、不能證明什麼**：上游說得很清楚——*"All-one inputs check the exercised arithmetic path but do not validate general numeric accuracy or predict application speedup."* 也就是說它證明「算對了」，不證明「你的應用會變快」。

### 採樣遙測

```sh
nvidia-smi --query-gpu=clocks.sm,temperature.gpu,power.draw \
  --format=csv -lms 100 > telemetry.csv
```

上游提醒：這種短暫取樣**不能證明**最大板載功耗、長期散熱或電氣安全。

### 報告時要分開講

三個層級不能混，而且**要把沒變化甚至變慢的案例也一起列出**（4096³ BF16 的 0.995× 與暖開機重測的 −8.2% 就是最典型的兩個）。

## 風險與界線

- **這是對 GPU 安全處理器的未授權程式碼執行**（緩衝區溢位 + ROP），跑的是自製 payload，和 NVIDIA 簽章韌體共用同一顆 GPU。
- **開源社群專案，沒有保固。** 上游 model card 對 Windows 那條路寫的是 *"Boot failure, loss of display, data corruption, hardware damage and other losses are possible. It is provided AS IS without warranty."*
- **上游自己也會修正文件與程式碼不一致的地方**（例如 `arch_610.h` 的 AD106 註解曾長期寫著 `untested on silicon`，但 `docs/` 已有實測報告）。引用時以 `docs/` 為準並註明版本。
- **NVIDIA 有強烈動機修掉這個漏洞**（它打的正是已簽章 booter 的溢位）。「更新驅動不用重打補丁」是站在短期使用的角度；長期來看這個方案可能被上游改動作廢。
- **韌體資產釘在 NVIDIA 610.43.03**；每次核心更新都要重編模組、重建 initramfs。
- **上游沒有做過長期穩定性測試**，也沒有涵蓋遊戲、ComfyUI、hibernate resume。

**建議**：先在一台你隨時可以重裝的機器上做，保留一個正常開機項，不要拿主力機或商用 SLA 主機先試。

## 延伸閱讀

- 上游專案：[github.com/JustAResearcher/gpu-unlock-ada](https://github.com/JustAResearcher/gpu-unlock-ada)（v1.1.1）
- 快速開始：[QUICKSTART.md](https://github.com/JustAResearcher/gpu-unlock-ada/blob/main/QUICKSTART.md)
- 4090 配對實測：[docs/evidence/rtx4090-pr1-matched/README.md](https://github.com/JustAResearcher/gpu-unlock-ada/tree/main/docs/evidence/rtx4090-pr1-matched)
- 測試流程：[docs/testing.md](https://github.com/JustAResearcher/gpu-unlock-ada/blob/main/docs/testing.md)
- 指令率探針：[diagnostics/bench/README.md](https://github.com/JustAResearcher/gpu-unlock-ada/blob/main/diagnostics/bench/README.md)
- Issue #17（4090 實測，含量化模型的反例）：[連結](https://github.com/JustAResearcher/gpu-unlock-ada/issues/17)
- 同系列的查核文章：
  - [RTX 40 系 Tensor 解鎖事實查核](https://kalpakjian.github.io/2026/10/25/rtx40-tensor-unlock-fact-check/)——全系列、翻倍、Windows 一鍵用三個關鍵字都不成立的理由
  - [RTX 30 系 gpu-unlock 事實查核](https://kalpakjian.github.io/2026/10/25/rtx30-gpu-unlock-ampere-fact-check/)——Ampere 上游的完整版
  - [RTX 3080 12GB 解除 gpu-unlock 操作筆記](https://kalpakjian.github.io/2026/10/25/rtx3080-12gb-gpu-unlock-guide/)——同一套流程的 Ampere 版

---

> **一句話收尾**：4090 是這條路上最穩的一張卡——不用實驗旗標、有配對實測、有唯讀讀回工具。但**「2 倍」是指令發射率，真實 GEMM 只有 12～34%**，而且**量化權重（3-bit MoE 實測 0.983×）幾乎吃不到任何好處**。先確認你跑的是 FP16／BF16，再決定要不要動手。
