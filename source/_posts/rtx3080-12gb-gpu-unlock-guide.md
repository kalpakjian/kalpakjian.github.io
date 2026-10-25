---
title: RTX 3080 12GB 解除 gpu-unlock 操作筆記：從確認 PCI ID 到量自己的負載
date: 2026-10-25 21:10:00
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
  - 工具設計
hide_from_home: true
toc: true
index_img: /img/covers/rtx3080-12gb-gpu-unlock-guide.png
banner_img: /img/covers/rtx3080-12gb-gpu-unlock-guide.png
---

> <strong>整理說明</strong>：這是給 <strong>RTX 3080 12GB</strong> 這張特定卡的操作筆記。資料來源是上游專案 <a href="https://github.com/Zagitta/gpu-unlock">Zagitta/gpu-unlock</a> 的 README、原始碼白名單、Issue #62（該型號的完整相容性回報），以及 <a href="https://github.com/impacifist/Windows-GPU-UNLOCK">impacifist/Windows-GPU-UNLOCK</a> 的硬體相容性文件。所有指令都照抄上游，沒有多加任何我自己發明的步驟。

<!-- more -->

## 先講結論

**這張卡可以，而且有同型號的完整實測。** 但有兩件事要先講清楚：

1. **會不會變快，取決於你的負載有沒有在跑 FP16／BF16 乘 FP32 累加的矩陣乘法。** 純 FP32、INT8、4-bit 量化、逐 token 生成——這四種幾乎沒有變化。
2. **上游 README 的「Tested cards」表漏列了 3080 12GB**（`220a` 在整份 README 出現 0 次），但 [Issue #62](https://github.com/Zagitta/gpu-unlock/issues/62) 的回報相當完整，而且作者用的就是和你一樣的思路：**先看這張卡在不在白名單裡，再看自己的負載吃不吃這條路徑。**

實測數據（Issue #62，技嘉 RTX 3080 12 GB、原廠未改、Arch、kernel 7.1.9、驅動 610.57.04 open、350 W 上限、8192³ dense GEMM、FP32 累加、五次取樣中位數）：

| 精度 | 解鎖前 | 解鎖後 | 增益 |
| --- | ---: | ---: | ---: |
| FP16 | 65.52 TFLOPS | 110.62 TFLOPS | **+69%** |
| BF16 | 65.63 TFLOPS | 113.24 TFLOPS | **+73%** |
| TF32 | 32.42 TFLOPS | 54.51 TFLOPS | **+68%** |

## 這張卡在白名單裡嗎：在

上游 `kernel/gpu_unlock/main.c` 的白名單開頭是這樣註解的：

> GA102, GA103, GA104 and GA106 GPU functions in pci.ids, excluding audio functions and the professional (GL) parts, **which already run BF16 at full rate**. GA103 and GA106 also exclude mobile parts.

GA102 的那一段：

```c
/* GA102 */
0x2200, 0x2203, 0x2204, 0x2205, 0x2206, 0x2207, 0x2208, 0x220a,
0x220d, 0x2216, 0x222b, 0x222f,
```

**`0x220a` 就在裡面**——那就是 RTX 3080 12GB。順帶注意那句註解：專業卡（GL parts）被排除，正因為它們**本來就以全速跑 BF16**。這就是整件事的起點。

> 有個容易混淆的點：**「RTX 3080 12GB」和「3080 改成 12GB 記憶體」是兩回事。** Issue #62 的那張是原廠 12GB（回報裡明寫 *Is the card modified? Stock*）；改裝成 20GB 的 3080 是另一張卡、另一個回報（#10、#15，+56～59%）。上游 README 裡寫的是「RTX 3080 20 GB (memory upgrade)」。

## 六步操作流程

<!-- FIG1 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 640" role="img" aria-label="RTX 3080 12GB 解除 gpu-unlock 的六步操作流程：確認 PCI ID、安裝、設定核心命令列、冷開機、驗證 gpu_unlock: unlocked、量自己的負載" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker><marker id="mfbbf24" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#fbbf24"/></marker><marker id="mf472b6" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#f472b6"/></marker></defs>
<rect x="0.75" y="0.75" width="998.5" height="638.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">六步操作流程</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">旁邊兩個分支是最容易踩到的地方</text>
<rect x="48" y="126" width="556" height="64" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<circle cx="76" cy="158.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="76" y="162.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<text x="102" y="150" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">確認 PCI ID 在白名單裡</text>
<text x="102" y="170" font-size="10.5" fill="#58a6ff" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">lspci -Dnn | grep -i nvidia</text>
<text x="102" y="184" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">應出現 10de:220a</text>
<rect x="48" y="210" width="556" height="64" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<circle cx="76" cy="242.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="76" y="246.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text>
<text x="102" y="234" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">安裝套件</text>
<text x="102" y="254" font-size="10.5" fill="#58a6ff" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">git clone … &amp;&amp; cd gpu-unlock &amp;&amp; make install</text>
<text x="102" y="268" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Arch／Debian／RPM 自動偵測</text>
<path d="M 76 206 L 76 190" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="294" width="556" height="64" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<circle cx="76" cy="326.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="76" y="330.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text>
<text x="102" y="318" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">設定核心命令列</text>
<text x="102" y="338" font-size="10.5" fill="#58a6ff" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">gpu_unlock.targets=0000:03:00.0</text>
<text x="102" y="352" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">寫進 GRUB 或 systemd-boot</text>
<path d="M 76 290 L 76 274" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="378" width="556" height="64" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<circle cx="76" cy="410.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="76" y="414.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<text x="102" y="402" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">完整斷電後冷開機</text>
<text x="102" y="422" font-size="10.5" fill="#58a6ff" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">切掉 AC 電源、等待約 30 秒再上電</text>
<text x="102" y="436" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">暖開機不保證提供乾淨韌體狀態</text>
<path d="M 76 374 L 76 358" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="462" width="556" height="64" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<circle cx="76" cy="494.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="76" y="498.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text>
<text x="102" y="486" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">驗證是否真的解鎖</text>
<text x="102" y="506" font-size="10.5" fill="#58a6ff" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">journalctl -k -b | grep gpu_unlock</text>
<text x="102" y="520" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">要找 gpu_unlock: unlocked</text>
<path d="M 76 458 L 76 442" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="546" width="556" height="64" rx="10" fill="#161b22" stroke="#2dd4bf55" stroke-width="1.5"/>
<circle cx="76" cy="578.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="76" y="582.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text>
<text x="102" y="570" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">量一次自己的負載</text>
<text x="102" y="590" font-size="10.5" fill="#58a6ff" font-family="'Cascadia Mono',Consolas,'Courier New',monospace">stock 與 unlocked 各量一次，用同一組設定</text>
<text x="102" y="604" font-size="10" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一核心／驅動／binary／功耗上限</text>
<path d="M 76 542 L 76 526" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="636" y="126" width="316" height="78" rx="10" fill="#1c2230" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="652" y="152" font-size="12.5" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不在名單就會被略過</text>
<text x="652" y="174" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">模組只接受 main.c 白名單裡的 ID；</text>
<text x="652" y="190" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">其他型號會被記錄後跳過，不會有任何提示。</text>
<path d="M 608 158.0 L 632 158.0" fill="none" stroke="#fbbf24" stroke-width="1.5" marker-end="url(#mfbbf24)"/>
<rect x="636" y="462" width="316" height="78" rx="10" fill="#1c2230" stroke="#f472b666" stroke-width="1.5"/>
<text x="652" y="488" font-size="12.5" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">模組載入成功 ≠ 解鎖成功</text>
<text x="652" y="510" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">必須看到目標卡的 gpu_unlock: unlocked，</text>
<text x="652" y="526" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">且 nvidia-smi 健康、journal 沒有 NVRM: Xid。</text>
<path d="M 608 494.0 L 632 494.0" fill="none" stroke="#f472b6" stroke-width="1.5" marker-end="url(#mf472b6)"/>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：六步操作流程——「不在白名單會被略過」與「模組載入成功不等於解鎖成功」是兩個最常見的陷阱。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG1 -->


下面是每一步的細節。

### 步驟 0：確認 PCI ID

```sh
lspci -Dnn | grep -i nvidia
```

你要找的是這一行的 PCI ID 欄：

```
0000:03:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA102 [GeForce RTX 3080 12GB] [10de:220a] (rev a1)
```

**注意兩件事：**

- **`10de:220a` 才是 12GB 這張。** `10de:2206` 是 3080 10GB（或改裝 20GB），`10de:2204` 是 3090，`10de:2203` 是 3090 Ti。搞錯型號是這件事最常見的第一步錯誤。
- **左邊那個 `0000:03:00.0` 就是你等一下要填進核心命令列的位址**（用 `lspci -D` 的完整格式，不要用 `lspci` 沒加 `-D` 的短格式）。

如果你的 ID 不在白名單裡，**模組會直接略過這張卡，而且不會跳任何警告**。上游 README 寫得很清楚：*"An entry that is not a GA102/GA103/GA104/GA106 card, including `all` mixed with addresses, is logged and ignored."*

### 步驟 1：安裝

```sh
git clone https://github.com/Zagitta/gpu-unlock
cd gpu-unlock
make install
```

`make install` 會讀 `/etc/os-release` 自動判斷發行版（Arch／Debian／Ubuntu／Fedora／RHEL／CentOS），選對的安裝路徑。也可以手動指定：

```sh
make install-arch   # makepkg -sif
make install-deb    # apt-get build-dep, dpkg-buildpackage, apt-get install
make install-rpm    # dnf builddep, rpmbuild, dnf install
```

建置過程會下載**雜湊釘死的** NVIDIA 610.43.03 輸入並在本地產生韌體；套件裡不含任何 NVIDIA 二進位檔的散佈副本。

需要 root 與核心標頭檔。`make install` 會問你 sudo 密碼。

### 步驟 2：設定核心命令列

模組**什麼都不做，除非你用核心命令列明確開啟它**。上游 README 寫：*"The module does nothing unless the kernel command line opts in."*

```text
gpu_unlock.targets=all                          # 每一張未綁定的 GA102/GA103/GA104/GA106
gpu_unlock.targets=0000:21:00.0                 # 只這幾張
gpu_unlock.targets=0000:21:00.0,0000:22:00.0    # 逗號分隔
```

**建議一開始就用單一完整位址**，不要用 `all`。理由在下一步會講。

依你的開機程式選一種寫法：

| 開機程式 | 做法 |
| --- | --- |
| GRUB（Debian／Ubuntu／Mint） | 在 `/etc/default/grub` 的 `GRUB_CMDLINE_LINUX_DEFAULT` **既有引號內**加上去，然後 `sudo update-grub` |
| GRUB（Arch／CachyOS） | 同樣編輯，然後 `sudo grub-mkconfig -o /boot/grub/grub.cfg` |
| Fedora／RHEL | `sudo grubby --update-kernel=ALL --args="gpu_unlock.targets=0000:03:00.0"` |
| systemd-boot | 在對應 entry 的 `options` 行追加（`bootctl status` 會告訴你位置） |
| UKI／自動生成 entry | 加到 `/etc/kernel/cmdline`，然後重新產生開機映像（例如 mkinitcpio UKI 用 `sudo mkinitcpio -P`） |

> **如果你的 initramfs 裡沒有 `nvidia`，`gpu_unlock` 會排在最後，但仍然早於從根檔案系統載入的 `nvidia`**——這是上游刻意設計的。

### 步驟 3：冷開機（這步最容易被忽略）

**第一次嘗試必須完整斷電。** 上游 README 的原話：

> **Power the machine off and start it again for the first attempt.** The module needs a card whose firmware state is fresh before NVIDIA loads. A warm reboot is not guaranteed to provide that state.

具體做法（上游的說法是「切掉 AC 電源、等約 30 秒」）：

1. 正常關機
2. **切掉 AC 電源**（拔插頭或關電源排插）
3. 等約 30 秒
4. 再上電開機

為什麼這麼嚴格：晶片上有一個 **WPR2** 標記。冷開機會把它清成 `0`，模組才願意跑交易；如果 WPR2 還留著，**模組會拒絕重跑**並記錄原因。

**例外**：實測的 2705 與 2805 在暖開機時 WPR2 會自己回零，所以解鎖成功。但這是「該卡的行為」，**不是保證**——其他板卡不保證。Issue #23 記錄過非冷開機造成的 `-ETIMEDOUT`，而且那個情況下 **GPU 會變成 nvidia 驅動不能用**。

### 步驟 4：驗證

```sh
journalctl -k -b | grep gpu_unlock
lspci -nnk -s 0000:03:00.0
```

成功的樣子長這樣（取自 Issue #62 的實際日誌）：

```text
gpu_unlock: ROM chain: pos=0x0 data=0x52494350 bytes=65024 type=0x0 last=0
gpu_unlock: ROM expansion: base=0xfe00 ext=0x24600 adjust=0x14800
gpu_unlock: FWSEC descriptor: offset=0x4128c ROM_bytes=1048576 header=0x4ac0301
gpu_unlock: FWSEC geometry: image_off=0x41738 size=0xea00 imem=0xe200 ...
gpu_unlock: FWSEC signature selection: versions=0x7 fuse_version=2 sig_bytes=384
pci 0000:2d:00.0: gpu_unlock: unlocked
```

**判準只有一個：`gpu_unlock: unlocked` 而且是「你的那張卡」。** 上游 README 特別強調：*"A loaded module or successful modprobe return alone does not prove an unlock"*——模組載入成功、`modprobe` 回傳 0，**都不算**。

同時確認三件事：

```sh
nvidia-smi                                    # 顯示正常
journalctl -k -b | grep -i xid                 # 應該沒有 NVRM: Xid
```

> **畫面會黑一下是正常的。** 上游說明：顯示卡的韌體 framebuffer 會在重置前被移除，所以 *"Its screen is blank from that reset until `nvidia-drm` takes over."*

### 步驟 5：量自己的負載

見下方〈怎麼量才不會騙自己〉一節。

## 我的負載會變快嗎

<!-- FIG2 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 520" role="img" aria-label="解鎖後哪些工作負載會變快：FP16／BF16 乘 FP32 累加的矩陣乘法會快 69% 到 73%，純 FP32、INT8、4-bit 量化與逐 token 生成幾乎不變" style="width:100%;height:auto;display:block">
<defs><marker id="m2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="998.5" height="518.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">我的負載會變快嗎</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">判準只有一句話</text>
<rect x="48" y="122" width="904" height="58" rx="12" fill="#1c2230" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="500" y="146" font-size="12" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">判斷只有一句</text>
<text x="500" y="168" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">你的負載有沒有在跑「FP16／BF16 乘、FP32 累加」的矩陣乘法？</text>
<rect x="48" y="212" width="440" height="190" rx="12" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="68" y="240" font-size="15" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">有 → 會變快（+69～73%）</text>
<text x="68" y="274" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・LLM prefill</text>
<text x="68" y="291" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">　　逐 token 生成之外的預填充</text>
<text x="68" y="320" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・擴散模型／圖片生成</text>
<text x="68" y="337" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">　　UNet 與 VAE 的矩陣乘法</text>
<text x="68" y="366" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・FlashAttention</text>
<text x="68" y="383" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">　　Issue #60 實測 +47～68%</text>
<rect x="512" y="212" width="440" height="190" rx="12" fill="#161b22" stroke="#7d859055" stroke-width="1.5"/>
<text x="532" y="240" font-size="15" fill="#7d8590" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">沒有 → 幾乎沒差</text>
<text x="532" y="274" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・純 FP32 運算</text>
<text x="532" y="289" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">　　這條路徑本來就沒被鎖</text>
<text x="532" y="310" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・INT8 量化</text>
<text x="532" y="325" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">　　維持原狀</text>
<text x="532" y="346" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・4-bit 量化（Ollama 預設）</text>
<text x="532" y="361" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">　　實測無增益</text>
<text x="532" y="382" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・LLM 逐 token 生成</text>
<text x="532" y="397" font-size="10.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">　　瓶頸在記憶體頻寬，不在算力</text>
<path d="M 340 180 L 268 208" fill="none" stroke="#2dd4bf" stroke-width="1.8" marker-end="url(#m2dd4bf)"/>
<path d="M 660 180 L 732 208" fill="none" stroke="#7d8590" stroke-width="1.8" marker-end="url(#m7d8590)"/>
<rect x="48" y="424" width="904" height="84" rx="10" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="68" y="452" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3080 12GB 的實測（Issue #62，8192³ dense GEMM、FP32 累加、350 W 上限）：</text>
<text x="68" y="474" font-size="12.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FP16 65.52 → 110.62 TFLOPS（+69%）　·　BF16 65.63 → 113.24 TFLOPS（+73%）　·　TF32 32.42 → 54.51 TFLOPS（+68%）</text>
<text x="68" y="496" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">但 3080 的 760 GB/s 記憶體頻寬不會變——decode 瓶頸還在原處。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：負載判斷樹——prefill、擴散模型、FlashAttention 會變快；純 FP32、INT8、4-bit 量化與逐 token 生成幾乎沒差。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG2 -->


| 你的用法 | 預期 | 理由 |
| --- | --- | --- |
| LLM **prefill**（預填充，一次處理整段 prompt） | **+69～73%** | 這是純矩陣乘法，正好吃滿解鎖後的 FP16／BF16 速率 |
| 擴散模型／圖片生成（UNet、VAE） | 明顯受惠 | 同上，大量矩陣乘法 |
| FlashAttention | +47～68%（Issue #60 實測） | 注意力核心是矩陣乘法 |
| 純 FP32 運算 | 幾乎沒差 | 這條路徑本來就沒被鎖 |
| INT8 量化 | 不變 | 走的是 INT8 張量路徑，模組不動它 |
| 4-bit 量化（Ollama 預設的 Q4／Q5） | **無增益** | Issue #60 實測確認 |
| LLM **逐 token 生成**（decode） | 幾乎不變 | 瓶頸在 760 GB/s 記憶體頻寬，不在算力 |
| 遊戲 | 不會變快 | 遊戲不走 FP16／BF16 累加這條路徑 |

> <strong>白話說</strong>：解鎖是把「引擎檔位」從半速推回全速。你的變速箱齒比、路面、限速牌都沒變——所以只有「出力就是瓶頸」的負載會感受到差異。**逐 token 生成卡在記憶體頻寬上，跟引擎多強無關。**

## 常見坑（都有 issue 編號可查）

| 症狀 | 原因 | 解法 | 出處 |
| --- | --- | --- | --- |
| `-EBUSY`，解鎖失敗 | initramfs 裡 `nvidia.ko` 比 `gpu_unlock` 先綁卡 | 確認 drop-in 有正確安裝、`nvidia` 在 initramfs 裡、`gpu_unlock` 排在它前面 | #11 |
| 模組根本沒載入 | Debian 套件沒附 dracut drop-in（Ubuntu 25.10+ 受影響） | 檢查 `/usr/lib/dracut/dracut.conf.d/gpu-unlock.conf` 是否存在 | #54 |
| 模組永遠不會載入 | initramfs-tools drop-in 寫成了無法解析的名稱 | 確認 drop-in 內容的名稱正確 | #29 |
| 所有卡都被拒絕 | 主機板韌體留著 bus mastering | 模組會先清掉 BME 再驗證有沒有清乾淨（Supermicro X11 尤其明顯） | #5 |
| `-ETIMEDOUT`，而且 **GPU 變成 nvidia 驅動不能用** | 非冷開機 | **必須冷開機**；這次失敗後要完全斷電再試 | #23 |
| 解鎖失敗，外接 3090 | Thunderbolt 外接盒 | 需要先讓外接盒完成授權 | #38、#51 |
| `-110` / `firmware load failed (-2)` | GA106／GA104 的 LHR 變體 | 已知有問題的型號，暫時避開 | #21、#67 |

另外兩個上游特意提醒的點：

- **不要用 `softdep nvidia pre:`**。上游 README 解釋：kmod 只會讀到**第一條** `softdep nvidia`，其他套件的規則（`nvidia-utils`、`gddr6_hwmon`）會安靜地蓋掉它，或反過來蓋掉它們的。
- **`targets=all` 會連同所有未綁定的 GA10x 卡一起選**，包含你可能不想動的那張。README 建議：*"On a multi-GPU host, identify the exact intended card; do not use `targets=all` for an Ada test."*

### 關於 suspend

上游 README 說明：Suspend to RAM 會讓卡斷電，**速度選擇器會被重置**；喚醒後模組會在 `nvidia` 恢復卡片之前重新解鎖一次，這會讓 resume 多花約 1 秒。保留供電的 suspend to idle 則不會重置。

不想要這個行為可以關掉：

```text
gpu_unlock.resume=0
```

或寫入 `/sys/module/gpu_unlock/parameters/resume`。**Hibernate 不在支援範圍內。**

## 回滾

三種層級，從輕到重：

| 想做的事 | 做法 |
| --- | --- |
| 只停用這一次開機 | 在開機程式的編輯畫面把 `gpu_unlock.targets=` 刪掉 |
| 永久停用 | 從核心命令列移除 `gpu_unlock.targets=`，重新產生開機映像 |
| 連套件一起移除 | 移除套件（模組與 initramfs drop-in 都會被移除） |

> **重要：如果交易沒有乾淨收尾，要「完全斷電」而不是重開機。** 上游 README：*"If the firmware on a card never stops, the module logs it and keeps the DMA buffers that firmware may still use until the next power off. **Power off before trying again.**"*

## 風險與界線

這不是「一般驅動更新」等級的操作。要很清楚自己在做什麼：

- **這是對 GPU 安全處理器的未授權程式碼執行**（緩衝區溢位 + ROP），跑的是自製 payload，和 NVIDIA 簽章韌體共用同一顆 GPU。
- **開源社群專案，沒有任何保固**，也沒有「萬一燒了怎麼辦」的答案。上游 README 直接寫 *"It is provided AS IS without warranty"*。
- **上游自己也會修正文件與程式碼不一致的地方**（例如 `arch_610.h` 的註解曾長期寫著 AD106「untested on silicon」，但 `docs/` 已經有實測報告）。引用時以 `docs/` 為準並註明版本。
- **NVIDIA 有強烈動機修掉這個漏洞**（它打的正是已簽章 booter 的溢位）。所以「更新驅動不用重打補丁」是站在短期使用的角度；長期來看這個方案可能被上游改動作廢。
- **韌體資產釘在 NVIDIA 610.43.03**。NVIDIA 改版資產就得重新產生；每次核心更新也要重編模組、重建 initramfs。
- **上游沒有做過長期穩定性測試**，也沒有涵蓋遊戲、ComfyUI、hibernate resume。

**因此我的建議是**：先在一台你隨時可以重裝的機器上做，保留一個正常開機項，不要拿主力機或商用 SLA 主機先試。

## 怎麼量才不會騙自己

解鎖後最容易犯的錯，是**只量一個狀態就下結論**。上游的配對實測方法（同系列 Ada 分支的 `docs/testing.md` 有完整版）要求下面幾件事。

### 先收集 stock 基線，再解鎖

在**還沒解鎖**的正常開機下先量一次，並把這些東西記下來：

```sh
uname -r                                   # 核心版本
cat /proc/cmdline                          # 當下的核心命令列
nvidia-smi --query-gpu=uuid,name,pci.bus_id,driver_version,power.limit --format=csv
```

再記下你的 benchmark **二進位檔的雜湊**，確保兩次跑的是同一個程式：

```sh
sha256sum build/matched-bench/gemm_bench > build/matched-bench/SHA256SUMS
```

### 鎖住所有變因

解鎖後再量一次，必須保持完全一致：

- **同一張卡**（用 `nvidia-smi --query-gpu=uuid` 取得 UUID，並用 `export CUDA_VISIBLE_DEVICES=<UUID>` 固定住）
- **同一個核心、同一個驅動、同一組 binary、同一個功耗上限、同一個時脈策略**
- 記錄當時桌面是否開著、有沒有其他背景負載

### 採樣時脈與功耗

```sh
nvidia-smi --query-gpu=clocks.sm,temperature.gpu,power.draw \
  --format=csv -lms 100 > telemetry.csv
```

上游提醒：這種短暫取樣**不能證明**最大板載功耗、長期散熱或電氣安全。

### 一個可以直接跑的量測腳本

Issue #62 的作者就是用最朴素的方式量的——cuBLAS GEMM，五次取樣中位數。這個版本可以直接用：

```python
# bench_gemm.py —— stock / unlocked 兩次跑，輸出可比對的 JSON
import json, os, statistics, time
import torch

N = int(os.environ.get("N", "8192"))
ROUNDS = int(os.environ.get("ROUNDS", "5"))
WARMUP = int(os.environ.get("WARMUP", "3"))

def run(dtype):
    a = torch.randn(N, N, device="cuda", dtype=torch.float16)
    b = torch.randn(N, N, device="cuda", dtype=torch.float16)
    for _ in range(WARMUP):
        a @ b
    torch.cuda.synchronize()
    samples = []
    for _ in range(ROUNDS):
        t0 = time.perf_counter()
        a @ b
        torch.cuda.synchronize()
        samples.append(time.perf_counter() - t0)
    return statistics.median(samples)

out = {"N": N, "gpu": torch.cuda.get_device_name(0)}
for name, dt in (("fp16", torch.float16), ("bf16", torch.bfloat16)):
    t = run(dt)
    out[name + "_median_s"] = t
    out[name + "_tflops"] = 2 * N ** 3 / t / 1e12
print(json.dumps(out, indent=2, ensure_ascii=False))
```

跑法（**先在 stock 開機跑一次存檔，解鎖後用同一個指令再跑一次**）：

```sh
python bench_gemm.py | tee stock.json
# ... 解鎖、重開機 ...
python bench_gemm.py | tee unlocked.json
```

### 報告時要分開講

上游的原則是三個層級不能混：

1. **指令發射率**（最底層，用 register-resident probe 量）
2. **GEMM 中位吞吐**（cuBLAS，真實的矩陣乘法）
3. **應用端到端吞吐**（你的實際工作負載）

而且**要把沒變化甚至變慢的案例也一起列出**。Issue #25 就是好例子：vLLM prefill +33%、decode flat、並附 8 小時混合負載穩定性記錄。

> **順帶一提**：如果你想要上游那種「讀回速率選擇器」的唯讀工具，注意 **`tools/read_sm_rates.py` 與 `diagnostics/` 目錄只存在於 Ada 分支**（`gpu-unlock-ada`），**上游 Ampere repo 沒有**。所以上面這個 torch/cuBLAS 腳本才是可攜的做法。

## 延伸閱讀

- 上游專案：[github.com/Zagitta/gpu-unlock](https://github.com/Zagitta/gpu-unlock)（4.3k stars，v1.0.0）
- 你的卡型的完整相容性回報：[Issue #62](https://github.com/Zagitta/gpu-unlock/issues/62)
- 漏洞機制完整分析：[docs/How Ampere was unlocked.md](https://github.com/Zagitta/gpu-unlock/blob/main/docs/How Ampere was unlocked.md)
- Windows 路線的硬體相容性（目前只有 3090 FE 與 3070 Ti 兩個 profile）：[docs/COMPATIBILITY.en.md](https://github.com/impacifist/Windows-GPU-UNLOCK/blob/main/docs/COMPATIBILITY.en.md)
- 同系列的查核文章：
  - [RTX 30 系 gpu-unlock 事實查核](https://kalpakjian.github.io/2026/10/25/rtx30-gpu-unlock-ampere-fact-check/)——「翻倍」與「全系列」兩句話都不成立的理由
  - [RTX 40 系 Tensor 解鎖事實查核](https://kalpakjian.github.io/2026/10/25/rtx40-tensor-unlock-fact-check/)——2× 指令率 vs 12～34% 實際 GEMM 增益

---

> **一句話收尾**：這張 3080 12GB 在白名單裡、有同型號的實測、預期增益約 +69～73%。但值不值得做，取決於你跑的是不是 FP16／BF16 的矩陣乘法——**如果你的負載是 4-bit 量化推論，這件事對你等於零。**
