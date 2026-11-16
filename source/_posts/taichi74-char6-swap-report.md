---
title: 十分鐘太極片換人：127 段、6.6 小時，與白布殘影
date: 2026-11-16 20:00:00
categories:
  - AI 研究筆記
tags:
  - MiniMax-H3
  - Character Swap
  - ComfyUI
  - 影片處理
index_img: /img/covers/taichi74-char6-swap-report.png
banner_img: /img/covers/taichi74-char6-swap-report.png
---

> 一句話結論：把十分鐘的教學片換成人，<strong>真正的難點不是模型，而是「參考圖不能帶場景」和「輸出必須 1536×864」</strong>這兩個看起來無關的參數；兩者錯了，模型就整段重繪，字幕、水印、黑邊全部消失。<br />
> <br />
> 全片 633 秒切成 127 段跑完 6.6 小時後，還有一處白太極袖以半透明殘影留在畫面上——用一個「原片當基準」的洩漏分數把它從 127 段裡挑出來，再單獨重跑那一段。<br />
> <br />
> 以下數字全部是同一台 RTX 4090、同一份 ComfyUI、同一支 H3 Ref2VA ＋角色 LoRA 跑出來的。

## 0. 這次的題目

素材是一支十分鐘的太極教學片：1024×576、24fps、633.125 秒、15195 幀，開頭 4.5 秒是書法字卡（沒有真人），之後是固定機位、單人示範，畫面上有燒錄的黃色字幕與右上角的水印。要把片中的人換成一個虛構角色，<strong>其餘一概不動</strong>：場景、機位、字幕、水印、動作節奏。

| 項目 | 值 |
|---|---|
| 素材 | `taichi74_24fps_1024x576.mp4`，15195 幀 / 633.125 秒 / 無音軌 |
| 角色參考 | 5 張白底角色表（正面、45°、側面、背面、臉部特寫），1024×1024 |
| 換人模型 | MiniMax H3 Ref2VA ＋角色替換 LoRA ＋4 步加速 LoRA ＋TRT VAE |
| 分段 | 127 段（首段 108 幀，其餘 120 幀，末段 87 幀） |
| 每段耗時 | 平均 190 秒（120–285 秒） |
| 全片耗時 | 23856 秒 ≈ 6.6 小時，0 次失敗 |

## 1. 兩個會讓成品報廢的參數

第一次直接用「角色角度圖」當參考——那些圖自帶廢棄工廠、煙霧、光柱。結果不是換人，是<strong>整段重繪</strong>：背景變成工廠、燒錄字幕與水印全部消失、三幀之間姿勢亂跳。用同一段跟原片算 SSIM 才看得出來：

| 版本 | 參考圖 | 輸出尺寸 | SSIM（對原片） |
|---|---|---|---|
| 既有可用基準（另一位角色） | 白底角色表 ×5 | 1536×864 | **0.825** |
| 第一次嘗試 | 自帶工廠背景 ×5 | 1024×576 | 0.593 |
| 改白底參考 | 白底 ×5 | 1024×576 | 0.760 |
| 改白底＋提高解析度 | 白底 ×5 | **1536×864** | **0.823** |
| 只用 2 張參考 | 白底 ×2 | 1536×864 | 0.763 |

<figure>
<img src="/img/taichi74-char6-swap-report/refs-process.jpg" alt="素材與白底角色表：左為自帶場景的參考圖，右為重拍成影棚背景的版本，下排為五個視角" loading="lazy" />
<figcaption>圖 1：左邊是原本的參考圖——人物可用，但背景是廢棄工廠，直接餵給換人模型會把整個場景搬進影片。中間一步是用 Qwen-Image-Edit 重拍成無縫影棚背景，再從同一張臉派生 45°、側面、背面；臉部特寫直接從正面裁切，另外生成會變成另一個人。</figcaption>
</figure>

兩個結論：

<strong>參考圖裡不能有原場景。</strong>模型會把參考圖的背景一起搬進影片。角色表要重拍成「乾淨白底、全身、無道具」——用 Qwen-Image-Edit 的多角度 LoRA 加一句「換成無縫白底攝影棚」就行，5 張約 5 分鐘。

<strong>解析度不能沿用預設。</strong>同一個模型在 1024×576 會「自由發揮」，在 1536×864 才願意守著原片結構；差別不是畫質，是<strong>要不要保留燒錄字幕</strong>。腳本預設值剛好是最差的那個，這一點要先改。


## 2. 分段：127 段 × 5 秒

長片只能切段跑。每段 5 秒（120 幀），但模型要的是 `17n+5` 的幀網格，所以送出去的其實是 124 幀、生成後再 `trim` 回 120 幀，接回去才不會累積誤差。首段（字卡，沒有真人）直接複製原片，不做替換。

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 430" role="img" aria-label="長片換人管線：素材、參考圖、分段、換人、色調匹配、串接" style="width:100%;height:auto;display:block">
<defs><marker id="m2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker></defs>
<rect x="0.75" y="0.75" width="998.5" height="428.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">長片換人管線</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">127 段 × 5 秒；平均 190 秒一段；全程 6.6 小時</text>
<rect x="40" y="120" width="145" height="92" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<circle cx="72" cy="166.0" r="15" fill="#7d8590" opacity="0.92"/>
<text x="72" y="171.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<text x="100" y="163.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">素材</text>
<text x="100" y="184.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1024×576 24fps</text>
<rect x="200" y="120" width="145" height="92" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<circle cx="232" cy="166.0" r="15" fill="#c084fc" opacity="0.92"/>
<text x="232" y="171.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text>
<text x="260" y="163.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">白底角色表</text>
<text x="260" y="184.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5 張 1024²</text>
<rect x="360" y="120" width="145" height="92" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<circle cx="392" cy="166.0" r="15" fill="#58a6ff" opacity="0.92"/>
<text x="392" y="171.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text>
<text x="420" y="163.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">分段</text>
<text x="420" y="184.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">127 × 5 秒</text>
<rect x="520" y="120" width="145" height="92" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<circle cx="552" cy="166.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="552" y="171.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<text x="580" y="163.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">逐段換人</text>
<text x="580" y="184.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1536×864</text>
<rect x="680" y="120" width="145" height="92" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<circle cx="712" cy="166.0" r="15" fill="#fbbf24" opacity="0.92"/>
<text x="712" y="171.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text>
<text x="740" y="163.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">色調匹配</text>
<text x="740" y="184.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">gain / bias</text>
<rect x="840" y="120" width="145" height="92" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<circle cx="872" cy="166.0" r="15" fill="#3fb950" opacity="0.92"/>
<text x="872" y="171.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text>
<text x="900" y="163.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">串接＋音軌</text>
<text x="900" y="184.0" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">15195 幀 633.1s</text>
<path d="M 187 166.0 L 198 166.0" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#m2dd4bf)"/>
<path d="M 347 166.0 L 358 166.0" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#m2dd4bf)"/>
<path d="M 507 166.0 L 518 166.0" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#m2dd4bf)"/>
<path d="M 667 166.0 L 678 166.0" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#m2dd4bf)"/>
<path d="M 827 166.0 L 838 166.0" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#m2dd4bf)"/>
<text x="40" y="258" font-size="16" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">三個會讓成品報廢的參數</text>
<rect x="40" y="280" width="300" height="78" rx="10" fill="#1c2230" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="66" cy="306" r="15" fill="#f472b6" opacity="0.92"/>
<text x="66" y="311.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">!</text>
<text x="88" y="312" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">參考圖不能有原場景</text>
<text x="88" y="336" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">自帶工廠與煙霧的參考圖，模型會整段重繪</text>
<rect x="355" y="280" width="300" height="78" rx="10" fill="#1c2230" stroke="#fbbf2466" stroke-width="1.5"/>
<circle cx="381" cy="306" r="15" fill="#fbbf24" opacity="0.92"/>
<text x="381" y="311.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">!</text>
<text x="403" y="312" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出必須 1536×864</text>
<text x="403" y="336" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1024×576 會被改寫，字幕與水印一起消失</text>
<rect x="670" y="280" width="300" height="78" rx="10" fill="#1c2230" stroke="#58a6ff66" stroke-width="1.5"/>
<circle cx="696" cy="306" r="15" fill="#58a6ff" opacity="0.92"/>
<text x="696" y="311.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">!</text>
<text x="718" y="312" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">尾段用 5 秒窗</text>
<text x="718" y="336" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">短於 5 秒或被併長的段，模型一律重畫</text>
<text x="40" y="400" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">驗收：15195 幀對齊原片、126 個接縫幀差中位數 1.51、逐幀掃黑邊抓出重繪段</text>
</svg>
<figcaption>圖 2：長片換人的六個步驟，以及三個會讓成品報廢的參數。分段與色調匹配是為了「接得回去」，參考圖與解析度是為了「不要被模型重畫」。</figcaption>
</figure>

每段獨立生成完都要<strong>逐段做色調匹配</strong>（per-channel gain/bias，對原片最小平方擬合，強度 0.85）。少了這一步，127 段會一段偏亮一段偏暗，接起來像燈光在跳。

## 3. 收勢尾段：只有 5 秒窗口救得回來

最後 3.6 秒是收勢，人幾乎靜止。這段一開始就被重繪：畫面放大、黑邊消失、字幕不見。可以量得很清楚——左側黑邊的亮度，正常是 17（純黑），重繪後會變成 60 以上（模型把內容填進黑邊）：

| 尾段做法 | 左黑邊亮度 | 結果 |
|---|---|---|
| 3.6 秒直接生成（seed A） | 113 | 重繪 |
| 3.6 秒直接生成（seed B） | 60 | 重繪 |
| 併進前一段，8.6 秒 | 97 | 重繪 |
| 併進前一段，13.6 秒 | 66 | 重繪 |
| <strong>5 秒窗口 628.1→633.1，砍掉前 33 幀</strong> | <strong>17</strong> | 成功 |


## 4. 白布殘影：先在 127 段裡把它找出來

全片跑完、串接、驗收都過了之後，看片的人回報：<strong>8:51 附近手臂上出現原本的白太極袖</strong>。人工看片只能抽查，這種「半透明殘影」又剛好出現在人物很小的全身景，於是改成量化：

對每一段，把<strong>原片</strong>當基準——挑出「原片是白色衣物、而且換人時真的被改動過」的像素，再看這些像素在成品裡<strong>還有多少仍然偏白</strong>。靜止的白牆與地面因為沒被改動，自然被排除；分數 0 代表白衣服被換掉了，接近 1 代表白布殘影原封不動留著。

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 380" role="img" aria-label="白布洩漏分數：全片中位數、正常段、seg_107 修前與修後" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="998.5" height="378.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">白布殘影的量化：洩漏分數</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">分數＝原片白色衣物被換掉的像素中，仍偏白的比例</text>
<rect x="110" y="216.7" width="150" height="83.3" rx="4" fill="#7d8590cc" stroke="#7d8590" stroke-width="1.5"/>
<text x="185.0" y="204.7" font-size="15" fill="#7d8590" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.098</text>
<text x="185.0" y="324" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全片中位數</text>
<rect x="330" y="206.5" width="150" height="93.49999999999999" rx="4" fill="#58a6ffcc" stroke="#58a6ff" stroke-width="1.5"/>
<text x="405.0" y="194.5" font-size="15" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.110</text>
<text x="405.0" y="324" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">正常段 105/106/108</text>
<rect x="550" y="138.5" width="150" height="161.5" rx="4" fill="#f472b6cc" stroke="#f472b6" stroke-width="1.5"/>
<text x="625.0" y="126.5" font-size="15" fill="#f472b6" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.190</text>
<text x="625.0" y="324" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">seg_107 修前</text>
<rect x="770" y="271.1" width="150" height="28.900000000000002" rx="4" fill="#3fb950cc" stroke="#3fb950" stroke-width="1.5"/>
<text x="845.0" y="259.1" font-size="15" fill="#3fb950" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.034</text>
<text x="845.0" y="324" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">seg_107 修後</text>
<path d="M 40 300 L 960 300" fill="none" stroke="#30363d" stroke-width="2"/>
<path d="M 40 172.5 L 960 172.5" fill="none" stroke="#fbbf24" stroke-width="1.6"/>
<text x="960" y="164.5" font-size="11.5" fill="#fbbf24" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">判定門檻 0.15</text>
<text x="40" y="348" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">修前那一段的白布是教練身上的白太極袖；修後改走重繪，白布消失但畫面放大 17%</text>
</svg>
<figcaption>圖 3：以原片為基準的白布洩漏分數。全片中位數 0.098，修前那一段 0.19；重繪後降到 0.034，代價是該 5 秒畫面被放大。</figcaption>
</figure>

127 段全掃（中位數 0.098），只有一段真的中：

| 段 | 平均分數 | 判定 |
|---|---|---|
| seg_107（8:49.5–8:54.5） | **0.19** | 真陽性：白袖＋白褲殘影 |
| seg_028 / seg_026 / seg_046 | 0.21 / 0.20 / 0.19 | 誤報，白色來自過曝水泥地 |
| seg_109 / seg_100 / seg_048 | 0.18 / 0.17 / 0.17 | 誤報 |
| 其餘 120 段 | ≤ 0.15 | 正常 |

分數前 10 名裡有 9 名是誤報，原因全是同一個：<strong>被陽光打到過曝的混凝土地面也是「亮、低飽和」</strong>。所以這個分數只適合當篩選器，最後仍要抽幀目視。

## 5. 修法與代價

那一段要「白布消失」與「畫面尺寸不變」同時成立，實測做不到：

| 做法 | 結果 |
|---|---|
| 換 2 個 seed 重生 | 白布消失，但整段重繪（黑邊亮度 100+，畫面放大 17%） |
| 寫腳本把白布像素重染成膚色 | 第一版蒙版漏掉袖身（無效）；第二版把地面一起染色 |
| 把重繪版縮回原畫框 | 等比縮回：上下多出黑邊、畫面小 14%；非等比：人物縱向拉長 19.5% |
| <strong>採用：重繪版，接受 5 秒放大</strong> | 白布完全消失、水印與黑邊一起消失在該段 |

原因是模型重繪時把鏡頭推近了 17%（水平 1.17×、垂直 1.19×），原片下方約 140 排前景地面在重繪版裡根本不存在，所以補不回來。最後選擇「乾淨」而不是「比例」——這 5 秒當成一次輕微推鏡。

## 6. 驗收：四層都要過

| 檢查 | 方法 | 結果 |
|---|---|---|
| 幀數與時長 | `ffprobe` | 15195 幀 / 633.125 秒，與原片完全一致 |
| 接縫 | 逐幀差分（tblend difference） | 126 個接縫的幀差中位數 **1.51**，全片平均 2.57（接縫比一般幀更平滑） |
| 重繪段 | 逐幀掃左黑邊亮度 | 15195 幀中 126 段為 17–18；僅 seg_107 為已知取捨 |
| 白布殘影 | 洩漏分數 ＋ 抽幀目視 | seg_107 由 0.19 降到 0.034，其餘不動 |
| 音軌 | 從 720p 母帶接回 | AAC 160k，長度與畫面相符 |

## 7. 結論與限制

三個可以帶去下一個任務的結論：

1. <strong>參考圖決定「換成誰」，來源片段決定「演什麼」，解析度決定「模型會不會自己改劇本」。</strong>三者任一錯了，成品都看不出是換人，而是重畫。
2. <strong>每段 5 秒是甜蜜點。</strong>太短（3.6 秒）與太長（8.6、13.6 秒）都會被重繪；要處理片尾這種短尾巴，用 5 秒窗口生成再裁掉重疊部分是唯一穩定的做法。
3. <strong>「有沒有換乾淨」要能量測。</strong>以原片為基準的洩漏分數可以把 127 段縮到 1 段候選，人工只需複核前十名；純靠抽幀看片一定會漏。

已知瑕疵，不打算再修：

- seg_107（8:49.5–8:54.5）：畫面放大約 17%、黑邊與水印消失，作為「推鏡」處理。
- seg_108（8:54.5–8:59.5）：畫面結構正常（SSIM 0.85），但右上角水印被模型抹掉。
- 手、腳、鞋在全身遠景尺度偏軟——原片人物只佔畫面約三分之一高，可用像素本來就不夠。

## 附錄：實際指令

```powershell
# 1) 白底角色表（5 個視角；--scene 換掉原本的工廠背景）
.\python_embeded_nightly\python.exe scripts\_char_angles.py --ref char6_front.png `
  --out char6sheet --angles front,q45r,side90r,back180,face --seed 431001 `
  --scene "Keep the same woman. Plain seamless light grey studio background, full body, no props."

# 2) 127 段換人（背景執行，失敗即停、可續跑）
.\python_embeded_nightly\python.exe scripts\_swap_full_char5.py --plan logs\char6_plan.tsv `
  --out logs\char6_manifest.tsv --tag H3_C6X_ --width 1536 --height 864 --intro `
  --refs char6s_front.png,char6s_q45r.png,char6s_side90r.png,char6s_back180.png,char6s_face.png `
  --prompt-file scripts\_char6_swap_prompt.txt

# 3) 白布殘影：單段評分與全片排名
.\python_embeded_nightly\python.exe scripts\_leak_scan.py input\c5cut_seg_107.mp4 output\video\H3_C6X_seg_107_00001__cc.mp4
powershell -NoProfile -File scripts\_leak_all.ps1      # -> logs\leak_summary.tsv

# 4) 串接（逐段 trim → concat → 接回原音軌）
powershell -NoProfile -File <skill>\scripts\concat_segments.ps1 `
  -Manifest logs\char6_manifest.tsv -Dir output\video `
  -Out output\video\FINAL_taichi74_char6_v3.mp4 -Prefix H3_C6X_
```

模型對「太短」與「太長」都會失敗，只有落在訓練分佈的 5 秒窗口才咬得住畫面。所以尾段是<strong>用一個跨越收勢動作的 5 秒窗口生成，再丟掉與前一段重疊的 1.4 秒</strong>，只取最後 87 幀。
