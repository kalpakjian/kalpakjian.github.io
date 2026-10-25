---
title: ComfyUI Nvidia VFX Nodes 實測報告：RTX 4090 上「舊放大管線 vs 新 RTX 節點」完整拆解
date: 2026-10-15 08:00:00
categories:
  - AI 研究追蹤
tags:
  - NVIDIA
  - RTX
  - ComfyUI
  - 效能實測
  - 基準測試
  - 超解析度
  - 畫格生成
toc: true
index_img: /img/covers/comfyui-nvidia-vfx-nodes-benchmark.png
banner_img: /img/covers/comfyui-nvidia-vfx-nodes-benchmark.png
---

> <strong>整理說明</strong>：這是一份「跑出來的」實測報告，不是官方文件的中文翻譯。起因是 Comfy-Org 的 <a href="https://github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes">ComfyUI_Nvidia_VFX_Nodes</a> 已經裝在我的 ComfyUI 裡，我想知道它到底比原本用的放大流程快多少，於是設計了三層量測（純 GPU／單幀端到端／批次端到端），把「快多少」拆到看得懂為止。
> 所有數字都是本機實測（RTX 4090、torch 2.14.1+cu132、nvidia-vfx 0.2.0.0／SDK 1.3.0），量測腳本與原始輸出都留在文末附錄，可以自己重跑一次。
> 全文盡量用比喻解釋名詞，不需要先懂 GPU 也能讀完。

<!-- more -->

## 一句話結論

> **這個節點在純運算上比舊的 ESRGAN 放大快約 755 倍，但因為它每次執行都要重新載入一次模型（約 1.2 秒），所以「一幀丟一次」只快 1.24 倍；把畫面改成「一次丟 16～64 幀」，就變成 5.56 倍。**

換成實際專案的說法：同一支 362 幀的影片，舊流程跑完要 **8.7 分鐘**，新節點只要 **1.6 分鐘**。

---

## 這篇在回答什麼問題

我原本的放大流程是這樣的（存在 `upscale04_run.py`）：

```text
載入圖片 → 4x-UltraSharp 放大 4 倍 → 縮回 1536×1536 → 存檔
```

一天 362 張圖，跑完的紀錄是「30 分鐘」。所以當新的 RTX 節點出現時，我第一個問題很單純：

**「它有沒有比較快？快多少？」**

要回答這個問題，不能只說「有」或「沒有」，因為「快」在三種不同的尺度上答案完全不同：

| 尺度 | 問題 | 這次的答案 |
| --- | --- | --- |
| 純運算 | 顯示卡真的算得比較快嗎？ | 快 **755 倍** |
| 端到端（單幀） | 我一張一張丟，實際省多少時間？ | 快 **1.24 倍** |
| 端到端（批次） | 我一次丟一批，實際省多少時間？ | 快 **5.56 倍** |

這三個數字都對，但意義完全不同。下面的章節會一層一層解釋為什麼會這樣。

---

## 先補名詞：不懂也能看懂的版本

如果你對這些名詞不熟，先讀完這一節，後面的數字就會自己說故事。

### ComfyUI 與「節點」

ComfyUI 是一個用「接線」來做 AI 繪圖／影像處理的工具。每個**節點**就像一個小工廠：左邊是輸入、右邊是輸出，你把節點接起來就變成生產線。例如「載入圖片 → 放大 → 存檔」就是三個節點串起來。

<strong>擴充（custom node）</strong>則是別人寫好、額外裝進去的節點包。這次要測的 `ComfyUI_Nvidia_VFX_Nodes` 就是 Comfy-Org 官方做的一包，裡面只有三個節點：

| 節點 | 白話功能 |
| --- | --- |
| **RTX Video Super Resolution** | 把畫面放大（順便除雜訊、去模糊） |
| **RTX Video HDR** | 把一般 SDR 畫面轉成 HDR |
| **RTX Video Frame Generation** | 在兩張相鄰畫面之間「無中生有」補出中間的畫面（做慢動作或提高幀率） |

### 什麼是「超解析度」與 4x-UltraSharp

<strong>超解析度（Super Resolution）</strong>就是「把小的圖變大，而且要變清楚」。最笨的方法是直接把像素放大（會糊、會鋸齒），聰明的做法是用 AI 模型去「猜」缺少的細節。

我原本用的 `4x-UltraSharp` 就是一個 AI 模型，屬於 **ESRGAN** 家族：它一次把圖放大 **4 倍**（768 → 3072），我再用最近鄰法縮回 1536。這條路效果很好，但很吃算力——**這是這次的比較基準**。

### 什麼是「畫格生成」

影片其實是一連串靜止畫面（畫格）快速播放。**畫格生成**就是看著第 1 張和第 2 張，去「推算」出中間那張（像補畫格做慢動作）。它必須理解畫面裡東西往哪個方向移動，所以比單純放大更難。

### 什麼是 nvidia-vfx 與 RTX Video Effects SDK

這三個節點本身**沒有**自己寫 AI 模型，它們是去呼叫 NVIDIA 官方的 **RTX Video Effects SDK**。中間的橋樑是一個叫 `nvidia-vfx` 的 Python 套件（綁定）。

用比喻說：**SDK 是 NVIDIA 提供的專業廚房，`nvidia-vfx` 是廚房的外送窗口，ComfyUI 節點是點菜的服務生。** 這次的效能問題，正好就出在「每點一道菜，廚房都要重新預熱一次」。

### 張量、DLPack：為什麼要「搬資料」

AI 運算裡的圖片不是普通的圖檔，而是一塊**張量（tensor）**——可以想成一疊排好的數字方格。ComfyUI 用 PyTorch 的張量，NVIDIA SDK 用自己格式的記憶體。

**DLPack** 是一套「共用記憶體」的標準，讓兩邊不必把資料複製來複製去就能直接讀同一塊。節點的做法是：把每個畫面搬到 GPU → 轉成 SDK 要的排列方式 → 交給 SDK 算 → 再把結果搬回來。這些搬移本身也要時間，所以下面量測時我會把它算進去。

### 什麼是「基準測試」，為什麼一定要看端到端

<strong>基準測試（benchmark）</strong>就是「固定條件下量時間」。這裡最容易犯的錯是：**只量 GPU 算得多快，卻忽略其他所有開銷。**

真實流程裡，一張圖要經過：讀檔 → 解碼 → 搬上 GPU → 運算 → 搬回 CPU → 編碼 → 寫檔。如果只看「運算」那一格，會得到很漂亮但沒用的數字。所以這份報告量三種：

1. **純 GPU**：只用 CUDA 事件量「效果本身」跑多久（最純粹，但不等於你感受到的速度）
2. **端到端單幀**：一張圖送進 ComfyUI、跑完、存檔，總共幾秒（你「一幀一 prompt」時的真實體驗）
3. **端到端批次**：一次送 16～64 張，總共幾秒（你「批次處理」時的真實體驗）

### 什麼是「輪詢」，為什麼它會讓舊數據量錯

程式要等 ComfyUI 做完，會用**輪詢（polling）**：每隔一段時間去問「好了沒？」

我原本的腳本是 `sleep(5)` 之後才問第一次——也就是**每張圖最少要等 5 秒才會被發現做完了**。這種現象叫**量化誤差**：真實時間可能是 0.5 秒也可能是 4.9 秒，但量到的永遠接近 5 秒。

所以舊紀錄那個「5.03 秒/張」幾乎全是等待造成的假象。這件事在後面的〈修正歷史數據〉一節會用實測數字證明。

---

## 測試環境

| 項目 | 內容 |
| --- | --- |
| GPU | NVIDIA GeForce RTX 4090（24564 MiB） |
| 驅動程式 | 617.42 |
| PyTorch | 2.14.1+cu132（CUDA 13.2，`cuda_available = True`） |
| Python | 3.11.9（ComfyUI 可攜版內建的 `python_embeded`） |
| ComfyUI | 可攜版，位於 `D:\AI\ComfyUI`，服務在 `127.0.0.1:8188` |
| nvidia-vfx | 0.2.0.0（回報 SDK 版本 **1.3.0**） |
| 舊流程模型 | `4x-UltraSharp.pth`（63.9 MB，用 spandrel 0.4.2 載入） |
| 測試素材 | 真實專案素材：362 張 768×768 PNG |
| 輸出尺寸 | 1536×1536（兩種流程完全相同的目標） |

> 附帶一提：這個擴充本來就已經裝好了，只是版本落後上游 21 個 commit。落後的部分只有「節點顯示名稱」從 `RTX TrueHDR` 改成 `RTX Video HDR`，節點 ID 與類別名稱刻意保留不變，所以既有工作流程不會壞。我把它 fast-forward 到最新版再開始測試。

---

## 量測方法：為什麼要分三層

為了避免「只量到好看的那一格」，我讓三層量測各自回答一個問題：

| 層次 | 怎麼量 | 回答的問題 | 為什麼需要它 |
| --- | --- | --- | --- |
| A 單幀端到端 | 同一批圖，**一張一個 prompt**，新舊流程**交錯**執行 10 次 | 我照原本習慣一張一張丟，能省多少？ | 這是「感覺得到」的速度 |
| B 純 GPU | 用 CUDA 事件夾住 `run()`，跑 10 次取平均 | 顯示卡本身算多快？ | 排除所有 I/O 與框架開銷 |
| C 批次端到端 | 一次 prompt 吃 16／64 張 | 改成批次處理能省多少？ | 這才是真實專案該用的方式 |

幾個刻意的設計：

- **交錯執行**：舊、新、舊、新……輪流跑，讓顯示卡溫度與時脈的漂移對兩邊影響相同，避免「後跑的那個剛好比較涼」。
- **先熱身再計時**：正式計時前先各跑一次，把模型載入、SDK 初始化等一次性成本排除在平均值之外。
- **密集輪詢**：等待時每 0.05 秒問一次（不是 5 秒），把量化誤差壓到可忽略。
- **相同素材、相同輸出尺寸**：兩種流程吃同一批 362 張圖，輸出都要求 1536×1536。

---

## 結果 A：純 GPU —— 快 755 倍

先看最純粹的一層。同一張 768×768 的圖，放大到 1536×1536：

| 流程 | 純 GPU 時間 | 等效速度 |
| --- | --- | --- |
| 舊：4x-UltraSharp 放大 4 倍（768 → 3072） | **830.05 ms** | 1.20 張/秒 |
| 舊：最近鄰縮回 1536 | 0.07 ms | 可以忽略 |
| **新：RTX Video Super Resolution（ULTRA）** | **1.10 ms** | **909 張/秒** |
| **差距** | **755 倍** | |

這 830 毫秒對 1.1 毫秒，就是「AI 模型自己算」與「專用影像處理單元算」的差距。**如果只看這一層，你會以為問題解決了。**

但先別急——這裡還藏了一個關鍵數字：**新節點的 `load()` 要 1114 毫秒。** 也就是說，「載入模型」比「實際運算」慢了 **1000 倍**。這就是後面所有故事的主因。

---

## 結果 B：端到端單幀 —— 只快 1.24 倍

同一批圖，一張一個 prompt，交錯執行 10 次：

| 流程 | 平均 | 中位數 | 最快 | 最慢 |
| --- | --- | --- | --- | --- |
| 舊：4x-UltraSharp + 縮圖 | **1.962 秒/張** | 1.960 秒 | 1.843 秒 | 2.094 秒 |
| 新：RTX VSR（ULTRA） | **1.576 秒/張** | 1.591 秒 | 1.419 秒 | 1.728 秒 |
| **差距** | **1.24 倍** | | | |

**為什麼純 GPU 快 755 倍，端到端卻只快 1.24 倍？**

因為「一張圖一個 prompt」時，真正在算圖的時間只佔極小一部分。把新流程那 1.576 秒拆開來看：

| 花在哪 | 時間 | 佔比 |
| --- | --- | --- |
| `load()` 載入 SDK 模型 | **約 1200 ms** | **約 76%** |
| 寫入 PNG 檔（1536×1536） | 約 200 ms | 約 13% |
| 讀取 PNG 檔（768×768） | 約 5 ms | 0.3% |
| 真正運算 | **1.1 ms** | **0.07%** |
| ComfyUI 框架與資料搬移 | 其餘 | 約 10% |

<!-- FIG2 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 450" role="img" aria-label="端到端單幀流程 1.576 秒的時間分解：load() 佔 76%、PNG 寫入 13%、框架搬移 11%，真正運算只有 0.07%" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="998.5" height="448.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">時間花在哪</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">總計 1.576 秒／張</text>
<rect x="48" y="150" width="688.3248730964467" height="46" rx="0" fill="#f472b666" stroke="#f472b6" stroke-width="1"/>
<rect x="736.3248730964467" y="150" width="114.72081218274111" height="46" rx="0" fill="#fbbf2466" stroke="#fbbf24" stroke-width="1"/>
<rect x="851.0456852791879" y="150" width="97.51269035532995" height="46" rx="0" fill="#c084fc66" stroke="#c084fc" stroke-width="1"/>
<rect x="948.5583756345178" y="150" width="3.0" height="46" rx="0" fill="#58a6ff66" stroke="#58a6ff" stroke-width="1"/>
<rect x="951.5583756345178" y="150" width="3.0" height="46" rx="0" fill="#2dd4bf66" stroke="#2dd4bf" stroke-width="1"/>
<rect x="48" y="150" width="904" height="46" rx="8" fill="none" stroke="#30363d" stroke-width="1.5"/>
<text x="48" y="136" font-size="12" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">端到端單幀流程的時間分解（總計 1.576 秒）</text>
<rect x="56" y="224" width="16" height="16" rx="3" fill="#f472b666" stroke="#f472b6" stroke-width="1.5"/>
<text x="84" y="237" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">load() 載入 SDK 模型</text>
<text x="600" y="237" font-size="12.5" fill="#f472b6" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1200 ms</text>
<text x="700" y="237" font-size="12.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">76.14%</text>
<rect x="56" y="254" width="16" height="16" rx="3" fill="#fbbf2466" stroke="#fbbf24" stroke-width="1.5"/>
<text x="84" y="267" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">寫入 PNG 檔（1536×1536）</text>
<text x="600" y="267" font-size="12.5" fill="#fbbf24" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">200 ms</text>
<text x="700" y="267" font-size="12.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">12.69%</text>
<rect x="56" y="284" width="16" height="16" rx="3" fill="#c084fc66" stroke="#c084fc" stroke-width="1.5"/>
<text x="84" y="297" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ComfyUI 框架與資料搬移</text>
<text x="600" y="297" font-size="12.5" fill="#c084fc" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">170 ms</text>
<text x="700" y="297" font-size="12.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10.79%</text>
<rect x="56" y="314" width="16" height="16" rx="3" fill="#58a6ff66" stroke="#58a6ff" stroke-width="1.5"/>
<text x="84" y="327" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">讀取 PNG 檔（768×768）</text>
<text x="600" y="327" font-size="12.5" fill="#58a6ff" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5.0 ms</text>
<text x="700" y="327" font-size="12.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.32%</text>
<rect x="56" y="344" width="16" height="16" rx="3" fill="#2dd4bf66" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="84" y="357" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">真正運算</text>
<text x="600" y="357" font-size="12.5" fill="#2dd4bf" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.1 ms</text>
<text x="700" y="357" font-size="12.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.07%</text>
<text x="600" y="212" font-size="11" fill="#8b949e" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">時間</text>
<text x="700" y="212" font-size="11" fill="#8b949e" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">佔比</text>
<rect x="48" y="400" width="904" height="62" rx="10" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="68" y="426" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">你付了 1.576 秒，只有 0.0011 秒在算圖——真正運算在比例尺上幾乎看不到。</text>
<text x="68" y="448" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">用廚房比喻：專業廚房炒一盤菜只要 0.001 秒，但每次都要先預熱烤箱 1.2 秒、每盤都要裝盤封膜 0.2 秒。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：1.576 秒裡真正在算圖的只有 0.07%——load() 佔 76%，所以單幀流程怎麼批次化才是重點。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG2 -->

換句話說：**你付了 1.5 秒，只有 0.001 秒在算圖。**

用廚房比喻：新的專業廚房炒一盤菜只要 0.001 秒，但每次都要先預熱烤箱 1.2 秒、每盤菜都要裝盤封膜 0.2 秒。**一盤一盤叫，速度完全被預熱與裝盤吃掉。**

---

## 結果 C：端到端批次 —— 快 5.56 倍

既然瓶頸是「每次都要預熱」，解法就是把多張圖塞進同一次執行——**`load()` 一次批次只付一次**。

用 `VHS_LoadImages` 一次載入整個資料夾變成一批畫面，再一次送進節點：

| 情境 | 總時間 | 每張平均 | 等效速度 |
| --- | --- | --- | --- |
| 舊流程，一次 16 張 | 23.05 秒 | **1.441 秒/張** | 0.7 張/秒 |
| 新節點，一次 16 張 | 4.14 秒 | **0.259 秒/張** | 3.9 張/秒 |
| 新節點，一次 64 張 | 13.97 秒 | **0.218 秒/張** | 4.6 張/秒 |
| **批次 16 張的差距** | | **5.56 倍** | |

**同一支 362 幀的專案換算：**

| 做法 | 362 幀預估時間 |
| --- | --- |
| 舊流程（一幀一 prompt，實測 1.962 秒/張） | 約 11.8 分鐘 |
| 新節點（一幀一 prompt，實測 1.576 秒/張） | 約 9.5 分鐘 |
| 新節點（批次 16 張） | **約 1.6 分鐘** |
| 新節點（批次 64 張） | 約 1.3 分鐘 |
| 舊流程的歷史紀錄 | 30 分鐘（但其中約 18 分鐘是空等，見下一節） |

---

<!-- FIG1 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 470" role="img" aria-label="nvidia-vfx 基準測試的三層落差：純 GPU 快 755 倍、端到端批次 5.56 倍、端到端單幀只有 1.24 倍" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="998.5" height="468.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">三層量測的落差</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一件事量三層，結論差 600 倍</text>
<rect x="486.66666666666663" y="162" width="1" height="182" rx="10" fill="#30363d" stroke="#30363d" stroke-width="1.5"/>
<rect x="673.3333333333333" y="162" width="1" height="182" rx="10" fill="#30363d" stroke="#30363d" stroke-width="1.5"/>
<rect x="860.0" y="162" width="1" height="182" rx="10" fill="#30363d" stroke="#30363d" stroke-width="1.5"/>
<text x="300" y="142" font-size="12" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">快幾倍（對數刻度）</text>
<text x="280" y="191" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">純 GPU（只算推論本身）</text>
<text x="280" y="208" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">830.05 ms  →  1.10 ms</text>
<rect x="300" y="176" width="537.2167643041151" height="26" rx="7" fill="#2dd4bf55" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="952" y="195" font-size="14" fill="#2dd4bf" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">755×</text>
<text x="280" y="253" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">端到端批次 16 張</text>
<text x="280" y="270" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.441 秒/張  →  0.259 秒/張</text>
<rect x="300" y="238" width="139.08062776198403" height="26" rx="7" fill="#58a6ff55" stroke="#58a6ff" stroke-width="1.5"/>
<text x="952" y="257" font-size="14" fill="#58a6ff" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5.56×</text>
<text x="280" y="315" font-size="13" fill="#e6edf3" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">端到端單幀（一張一 prompt）</text>
<text x="280" y="332" font-size="10.5" fill="#8b949e" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.962 秒/張  →  1.576 秒/張</text>
<rect x="300" y="300" width="17.438714563617225" height="26" rx="7" fill="#f472b655" stroke="#f472b6" stroke-width="1.5"/>
<text x="952" y="319" font-size="14" fill="#f472b6" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.24×</text>
<text x="300.0" y="370" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1×</text>
<text x="486.66666666666663" y="370" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10×</text>
<text x="673.3333333333333" y="370" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">100×</text>
<text x="860.0" y="370" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1000×</text>
<rect x="48" y="390" width="904" height="62" rx="10" fill="#1c2230" stroke="#f472b655" stroke-width="1.5"/>
<text x="68" y="416" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一件事、三種量法，結論差 600 倍：只量「純 GPU」會以為快 755 倍，</text>
<text x="68" y="438" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">量到端到端只剩 1.24 倍。這就是為什麼基準測試一定要看端到端。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：同一件事量三層的落差——純 GPU 快 755 倍、端到端批次 5.56 倍，但端到端單幀只有 1.24 倍。基準測試一定要看端到端。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG1 -->

## 修正歷史數據：那個「30 分鐘」其實有一半以上在空等

原本的紀錄檔寫著：

```text
frames: 362
  30/362  151s elapsed
  ...
  360/362  1811s elapsed
ALL DONE 362/362 in 30 min, failed=[]
```

362 張、1811 秒，換算 **5.03 秒/張**。看起來很合理，但它是假的。

原因就在輪詢：那支腳本的等待函式是**先睡 5 秒才問第一次**，所以每張圖的帳面時間不可能低於 5 秒。而 5.03 秒只比 5.00 秒多 0.03 秒——這代表**幾乎每一張都是在第一個 5 秒窗口內就做完了**，帳面數字完全被 5 秒的門檻綁住。

我於是用同一批素材、同一個模型、同一台伺服器重新量了一次舊流程（等待改成每 0.05 秒問一次）：

| 量測方式 | 每張時間 | 362 張總計 |
| --- | --- | --- |
| 歷史紀錄（輪詢間隔 5 秒） | 5.03 秒 | 30.2 分鐘 |
| **重新實測（輪詢間隔 0.05 秒）** | **1.962 秒** | **約 11.8 分鐘** |

**也就是說，那 30 分鐘裡大約有 18 分鐘是程式在睡覺，不是顯示卡在工作。**

這件事有兩個結論：

1. **舊紀錄不能當基準**，因為它量的是「輪詢間隔」而不是「運算速度」。
2. **光是修掉輪詢，就能讓同一支腳本從 30 分鐘變成約 12 分鐘**——這比換任何模型都划算。

---

## 附錄級資料：每個效果的完整速度

上面只講了放大。既然三個節點都裝好了，我把其餘效果也用 CUDA 事件量過一輪（純 GPU，每項跑 10 次取平均）。

### RTX Video Super Resolution（依品質模式）

| 模式 | 解析度 | 每張時間 | 等效速度 |
| --- | --- | --- | --- |
| ULTRA | 640×360 → 1280×720 | 0.53 ms | 1875 張/秒 |
| ULTRA | 1280×720 → 1920×1080 | 1.59 ms | 629 張/秒 |
| ULTRA | 1280×720 → 2560×1440 | 1.63 ms | 612 張/秒 |
| ULTRA | 1920×1080 → 3840×2160 | 8.04 ms | 124 張/秒 |
| HIGH | 1280×720 → 1920×1080 | 1.19 ms | 844 張/秒 |
| MEDIUM | 1280×720 → 1920×1080 | 0.66 ms | 1509 張/秒 |
| STREAMING_ULTRA | 1280×720 → 1920×1080 | 1.95 ms | 513 張/秒 |
| DENOISE_MEDIUM | 1280×720（等尺寸） | 6.51 ms | 154 張/秒 |
| HIGHBITRATE_ULTRA | 1280×720 → 1920×1080 | 24.71 ms | 40 張/秒 |
| BICUBIC（非 AI） | 1280×720 → 1920×1080 | 2.88 ms | 347 張/秒 |

幾個值得注意的細節：

- **`MEDIUM` 幾乎是 `ULTRA` 的兩倍速**（0.66 ms 對 1.59 ms），但兩者都遠低於 1 毫秒的感知門檻。也就是說，在批次處理的情境下，**選 ULTRA 幾乎不用付代價**。
- **`HIGHBITRATE_ULTRA` 貴 20 倍**（24.71 ms），它是為「乾淨、高碼率、無損來源」設計的，不該用在一般壓縮過的素材上。
- **`BICUBIC`（傳統內插）竟然比 AI 的 `ULTRA` 慢**（2.88 ms 對 1.59 ms）。這是因為它在同一條管線裡走的是另一段實作，不是「不跑 AI 就比較快」的直覺。
- **`DENOISE_*` 與 `DEBLUR_*` 是等尺寸效果**：它們維持原解析度，只做除雜訊／去模糊。

### RTX Video HDR

| 解析度 | 每張時間 | 等效速度 |
| --- | --- | --- |
| 1280×720 | 0.35 ms | 2891 張/秒 |
| 1920×1080 | 1.00 ms | 997 張/秒 |

### RTX Video Frame Generation（每張生成畫面）

| 模式 | 解析度 | 每張時間 | 等效速度 |
| --- | --- | --- | --- |
| MEDIUM | 1280×720（×2 倍） | 4.22 ms | 237 張/秒 |
| MEDIUM | 1920×1080（×2 倍） | 4.49 ms | 223 張/秒 |
| HIGH | 1920×1080（×2 倍） | 19.80 ms | 51 張/秒 |

> 小提醒：畫格生成只支援 NVIDIA 40 系列以後的顯示卡。這台是 RTX 4090，所以可以跑。

### 各效果的 `load()` 成本（每次執行都要付）

| 效果 | `load()` 時間 |
| --- | --- |
| Video Super Resolution | 1115 ～ 1208 ms |
| 舊流程的 ESRGAN 模型 | 214 ms（但 ComfyUI 會快取，一個批次只需付一次） |

---

## 品質：新的輸出跟舊的有多像

速度快不代表可以用。同一張圖分別用兩種流程放大到 1536×1536 後比對：

| 指標 | 數值 |
| --- | --- |
| 平均亮度（舊／新） | 171.1 / 170.8 |
| 對比（標準差，舊／新） | 24.7 / 24.4 |
| 平均像素差 | 1.42（滿分 255） |
| **PSNR** | **39.35 dB** |

**PSNR 39.35 dB** 代表兩張圖「非常接近但不完全相同」。這是合理的：兩者都是保留細節的放大演算法，但**演算法不同，細節特徵就會不同**（例如紋理、邊緣銳利度、雜訊處理方式）。

也就是說：**在這個素材上，兩者品質屬於同一級別；差距在「風格」而不是「好壞」。** 我保留了一組對照圖（`benchab_old_00001_.png` 與 `benchab_new_00001_.png`）可以自己肉眼比對。

> ⚠️ 但要注意：PSNR 只反映「數值差異」，不反映「主觀好看程度」。真要換流程，建議先拿幾張自己最在意的畫面（例如臉部、文字、細線條）做 A/B 目視比較。

---

## 過程中踩到的坑

這幾個坑都不是「看得出來」的那種，而是會直接讓工作流失敗、錯誤訊息又不太直白的那種。記下來省未來的時間。

### 坑 1：動態選單的 API 格式和平常不一樣

節點的「放大方式」是一個**動態選單**：選「依倍率」時只會出現倍率欄位，選「指定尺寸」時才出現寬高欄位。用網頁介面完全不會有問題，但用程式（API）送 prompt 時格式不同。

**錯誤寫法**（把子欄位包成巢狀物件）：

```json
"resize_type": { "resize_type": "target dimensions", "width": 1536, "height": 1536 }
```

錯誤訊息是：

```text
RTXVideoSuperResolution.execute() missing 1 required positional argument: 'resize_type'
```

**正確寫法**（扁平、用點號分層）：

```json
"resize_type": "target dimensions",
"resize_type.width": 1536,
"resize_type.height": 1536
```

原因是 ComfyUI 內部（`build_nested_inputs()`）會把點號鍵重新組回巢狀結構。同一招也適用於畫格生成的「生成方式」選單（`generation_type`、`generation_type.multiplier`）。

### 坑 2：除雜訊／去模糊模式必須「等尺寸」

`DENOISE_*` 與 `DEBLUR_*` 是**等解析度效果**：它們只除雜訊／去模糊，不負責放大。如果你把輸出尺寸設成別的數字，SDK 會直接拒絕：

```text
nvvfx.NvVFXError: NvVFX_Run failed: An invalid parameter value has been supplied
for this effect+selector (code -7)
```

節點本身有處理這件事（會自動把輸出尺寸改成跟輸入一樣），但如果你自己寫程式呼叫 SDK，就要自己記得。

### 坑 3：輸出尺寸會被取整到 8 的倍數

放大後的尺寸會**對齊到最接近的 8 的倍數**。所以「2 倍」不等於「剛好兩倍」——例如 767 會變成 768。這次的 768 → 1536 剛好都是 8 的倍數，所以沒有影響，但別的尺寸就會差幾個像素。

### 坑 4：節點顯示名稱改過

這個擴充的節點顯示名稱從 `RTX TrueHDR` 改成 `RTX Video HDR`。**節點 ID 與 Python 類別名稱刻意保留**，所以既有工作流程不會壞，但你在介面上找的是舊名字時會找不到。重啟 ComfyUI 之後才會看到新名稱。

### 坑 5：這台機器沒有 ComfyUI Manager

所以擴充的更新要靠手動 `git pull`。另外 `nvidia-vfx` 在 PyPI 上只有原始碼封裝（sdist），安裝時必須用**跟 ComfyUI 同一個 Python 直譯器**：

```bash
"D:\AI\ComfyUI\python_embeded\python.exe" -m pip install -r requirements.txt
```

用錯直譯器（例如系統的 Python）會裝到別的環境，ComfyUI 依然會說 `nvidia-vfx cannot be imported`。

---

## 給自己的建議（依效益排序）

1. **改成批次處理**：一次餵 16～64 幀，不要一幀一個 prompt。單這項就是 **5.56 倍**，而且不需要改任何模型設定。
2. **修掉輪詢間隔**：`sleep(5)` 改成 `sleep(0.05)`。光是這一項，就能讓既有的舊腳本從 30 分鐘降到約 12 分鐘。
3. **減少 PNG 寫檔**：批次處理後，剩下的瓶頸是每張約 0.2 秒的 PNG 編碼。如果不需要逐幀圖檔，改用影片節點（例如 `VHS_VideoCombine`）直接輸出影片，可以再省下這段。
4. **品質模式放心用 `ULTRA`**：它和 `MEDIUM` 的差距只有約 0.9 毫秒，在批次情境下幾乎不用付代價。但**不要**對一般壓縮素材用 `HIGHBITRATE_*`（貴 20 倍）。
5. **除雜訊需求先確認尺寸**：`DENOISE_*`／`DEBLUR_*` 不會放大，要放大就得分兩步做。

---

## 附錄 A：量測腳本

腳本都留在 `C:\Users\princ\AppData\Local\Temp\nvvfx\`，用 ComfyUI 內建的 Python 執行：

```bash
"D:\AI\ComfyUI\python_embeded\python.exe" <腳本>
```

| 腳本 | 做什麼 |
| --- | --- |
| `smoke_test.py` | 三個效果的煙霧測試（確認 SDK 能跑、輸出形狀正確） |
| `bench_ab_server.py` | 層次 A：單幀端到端，新舊流程交錯量測 |
| `bench_effects_gpu.py` | 層次 B：各效果的純 GPU 微基準 |
| `bench_pipeline_gpu.py` | 純 GPU 對照（含 PNG 編解碼與 ESRGAN 本體） |
| `bench_batch_server.py` | 層次 C：批次端到端（16／64 幀） |

腳本裡的環境變數可以調整樣本數：

```bash
set BENCH_FRAMES=10     # 單幀端到端要跑幾張
set BENCH_ITERS=10      # 微基準每項跑幾次
```

---

## 附錄 B：如果要套用到自己的專案

檢查清單：

1. ☐ 確認 GPU 是 RTX 系列，且畫格生成需要 **40 系列以後**
2. ☐ 確認 ComfyUI 用的是 **CUDA 版 PyTorch**（`torch.cuda.is_available()` 要是 `True`）
3. ☐ 用**同一個** Python 直譯器安裝 `nvidia-vfx`
4. ☐ 工作流改成**批次**（用 `VHS_LoadImages` 之類的節點把整個資料夾變成一批）
5. ☐ 確認輸出尺寸是 **8 的倍數**
6. ☐ 除雜訊／去模糊記得**輸出尺寸等於輸入尺寸**
7. ☐ 用程式送 prompt 時，動態選單要用**點號扁平格式**
8. ☐ 量測時把輪詢間隔調小，否則你會量到自己的等待時間

---

## 一句話總結

> **這個節點把「算圖」這件事加速了 755 倍，但流程真正的成本從來就不是算圖——而是模型載入與檔案 I/O。** 所以「換節點」只帶來 1.24 倍，真正該改的是「一次丟一批」，那才是 5.56 倍。

---

*本篇為本機實測紀錄，所有數字皆可依附錄 A 的腳本重現。*



