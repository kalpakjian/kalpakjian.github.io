---
title: 在 Windows x64 原生跑 Nemotron 3.5 Super 120B-A12B：strata-nemotron 編譯紀錄、實測數字與兩個對不上的地方
date: 2026-10-28 10:30:00
categories:
  - 技術筆記
tags:
  - 人工智慧
  - NVIDIA
  - Nemotron
  - Strata
  - NVFP4
  - MoE
  - 本地 LLM
  - Windows
  - 原生編譯
  - 效能實測
  - 基準測試
  - Blackwell
toc: true
index_img: /img/covers/strata-nemotron-windows-x64.png
banner_img: /img/covers/strata-nemotron-windows-x64.png
---

> <strong>整理說明</strong>：這篇不是官方文件的中文翻譯，而是「一條社群供應鏈」的查核紀錄。整條鏈有四層：NVIDIA 的原生模型 → Cudecnik 的 NVFP4 GGUF 重打包 → Cudila 的 <code>strata-nemotron</code> 引擎分支 → dseditor 的 Windows x64 原生編譯版。四層都查過原始出處，數字全部標明是誰量的、在哪台機器量的。
> 文中的效能數字出自 Windows Release 頁的實測段（RTX 5090 32 GB、96 GB DDR5-4800、i5-13500、Windows 11），以及 Hugging Face 模型卡的完整曲線表（Linux 端）。<strong>本機（RTX 4090、63.7 GB RAM）跑不動這套</strong>，原因寫在第五節，所以這篇不會假裝是親測。
> 另外，兩份官方文件之間有兩個數字對不上（96 與 118 t/s、1,475 與 2,368 t/s），第二節直接把這件事攤開講。

<!-- more -->

## 三十秒結論

- <strong>Nemotron 3.5 Super VL 120B-A12B</strong> 是一顆 120B 總參數、12B 活躍參數的 MoE（外加 Mamba2 層與視覺塔），權重是 NVFP4，原生支援圖片輸入。
- 社群把它接到 <code>Strata</code> 這個「把專家丟到 RAM、只把常用的放 VRAM」的引擎上，<strong>單張 RTX 5090 就能跑</strong>，而且 Windows 有社群編好的原生 x64 版，不用 WSL、不用 Linux。
- 硬體門檻很硬：<strong>只支援 Blackwell（sm_120，RTX 50 系列）</strong>、建議 96 GB RAM（64 GB 確定不夠）、驅動 580+、磁碟 72 GB（要讀圖再加 1.7 GB）。
- 速度大約是「4K 提示前填充 1,475 tok/s、解碼 96 tok/s、中文對話 77 tok/s、讀一張 3,369 token 的照片 19 秒」，第一次載入 211 秒。
- 真正的價值不在跑分，而在<strong>授權</strong>：引擎 MIT、權重 OpenMDW-1.1，完全離線，對「不能碰中國大陸模型」的場合是一條可走的路。
- 但它<strong>不適合當併發服務</strong>：這整套的前提是「一張卡、一個使用者、把整個 PC 的記憶體當資源池」。

## 一、先把「為什麼要換模型」講清楚

最近社群在傳 Qwen 系列模型在某些提示下會回傳帶有阿里巴巴字樣的內容。這類回報有幾個特徵：<strong>偶發、與提示的領域高度相關、很難穩定重現</strong>——要在沙盒裡反覆試很多次才偶爾出現一次。它不是「每次都會」，也不是「所有版本都有」。

我自己的判斷是<strong>不換</strong>：我拿小模型寫程式都是很窄的特定用途，跟傳出問題的內容領域完全不相干，換掉的成本比風險高。Claude 給的建議也是同一件事——先確認你的用途是否真的落在風險區，而不是看到新聞就整批換掉。

但有一條線是硬的：<strong>政府機關與受監管的採購案，不能使用中國大陸的模型</strong>，這跟技術好坏無關，是規範問題。於是就出現一個很現實的撞牆場景：

> 你很酷地說「我要用比較便宜的硬體來佈署 Strata」——預算過了、卡也買了、機器架好了，然後採購說這顆模型的來源不能用。

這篇就是那條替代路線的紀錄。順帶一句：以「沒有併發」為前提的本地部署，其實不太適合直接拿去搭服務；公部門要的是「服務化」，不是「一台電腦上跑一個聊天框」。

## 二、這個組合到底是哪四層

先把責任歸屬分清楚，出問題才知道去哪裡問：

| 層 | 專案 | 角色 | 授權 |
| --- | --- | --- | --- |
| ① 模型 | <code>nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-NVFP4</code> | NVIDIA 原生的 NVFP4 權重、chat template、推理模式、視覺塔 | OpenMDW-1.1 |
| ② 權重重打包 | <code>Cudecnik/Nemotron-3.5-Super-120B-A12B-NVFP4-Strata-Blackwell</code> | 把權重轉成 ggml 的 NVFP4、切成兩個 shard，保留 MTP 區塊 | 跟隨 ③ |
| ③ 引擎 | <code>Cudila/Strata</code>（分支 <code>strata-nemotron</code>） | 把 63 GB 專家放進 page-locked RAM、VRAM 當快取、FP4 tensor core 跑前填充 | MIT（Strata 本體） |
| ④ Windows 編譯 | <code>dseditor/Strata</code>，Release <code>windows-nemotron-v1</code> | MSVC + CUDA 13.4 原生 x64 版、安裝腳本 | 引擎 MIT／模型 OpenMDW-1.1 |

兩個關鍵事實：

1. <strong>權重是「無損重打包」</strong>。路由專家用的是 NVIDIA 原本的 NVFP4 數值，只是換成 ggml 的 <code>NVFP4</code> 型別（type 40）重新排列，沒有再量化一次；Mamba 投影層的 FP8 → NVFP4 則用與 ModelOpt 相同的區塊尺度搜尋（最小 MSE，而不是 amax/6 四捨五入），在專家上的相對誤差 0.0812，對照 ModelOpt 的 0.0813。
2. <strong>MTP 頭被保留</strong>。那個 1.6 GB 的多 token 預測區塊不是裝飾：32K 提示時解碼從 109 拉到 186 t/s（fast 模式），從 52 拉到 130（precise 模式）。很多量化版會把它砍掉，這版沒有。

檔案有兩個 shard，合計 71.6 GB：

| 檔案 | 內容 |
| --- | --- |
| <code>Nemotron-3.5-Super-120B-A12B-NVFP4-00001-of-00002.gguf</code> | 44.3 GB，metadata 與 423 個 tensor |
| <code>Nemotron-3.5-Super-120B-A12B-NVFP4-00002-of-00002.gguf</code> | 27.3 GB，其餘 766 個，含 embeddings、<code>lm_head</code>、MTP 區塊 |

1189 個 tensor 的型別分布是 BF16 88、F32 824、NVFP4 244、Q8_0 33。視覺塔<strong>不在</strong>這兩個檔裡，是另外接 Unsloth 的 <code>mmproj-BF16.gguf</code>。

### 為什麼非 Blackwell 不可

這不是「沒測過」，是「指令集不存在」。引擎的 GEMM kernel 用的是 Blackwell 才有的 FP4 tensor-core 指令（<code>mma … kind::mxf4nvf4.block_scale</code>，NVFP4 × NVFP4 帶原生 scale），編譯目標是 <code>sm_120a</code>。RTX 40／30 系列與 AMD 沒有這組指令，跑不起來——不是慢，是不會動。

## 三、硬體門檻：三個「剛好」疊在一起

| 項目 | 需求 | 為什麼 |
| --- | --- | --- |
| GPU | RTX 50 系列（sm_120） | FP4 tensor core 指令，<code>sm_120a</code> 編譯 |
| VRAM | 16 GB 起（32 GB 舒服） | 只放「最常用的幾千個專家」快取 + KV/MTP |
| RAM | <strong>96 GB 建議；64 GB 確定不夠</strong> | 專家 arena 是 59 GiB 的 page-locked 記憶體，不能換出 |
| 驅動 | 580 以上（CUDA 13） | 引擎連結 <code>cublas64_13.dll</code> / <code>cublasLt64_13.dll</code> |
| 磁碟 | 72 GB（讀圖再 +1.7 GB） | 兩個 shard + mmproj，可續傳下載 |

模型卡里有一段很誠實的記憶體帳：page-locked 的專家 arena 是 59 GiB、<strong>不可置換</strong>；在 128 GB 的機器上整支程式峰值 resident 到 105 GiB（含 page cache，可被核心丟掉）；對話快取再加約 4.3 GB（8 × 165 MB + 3000 MiB）。原文寫「96 GB 大概夠，但沒試過；64 GB 不夠，arena 自己就放不進去了」。

有趣的地方在這裡：<strong>Windows Release 頁的實測機器就是 96 GB</strong>，而且跑起來了。所以「96 GB 沒試過」這個空白，已經被另一個作者的 5090 補上了——這也是我建議回報社群的原因，比貼文更能幫到下一個人。

## 四、實測數字

### 4.1 Windows 原生版的實測（4K 提示）

| 指標 | 數值 |
| --- | --- |
| 第一次載入（從磁碟） | 211 秒 |
| 之後每次啟動 | 1～4 分鐘 |
| 前填充（4K 提示） | 1,475 tok/s |
| 解碼（4K、MTP、fast） | 96 tok/s |
| 專家命中率（伺服器端） | 96% |
| 中文對話 | 77 tok/s |
| 讀圖 | 3,369 token 的照片，19 秒完成且描述正確 |

測試機：RTX 5090 32 GB、96 GB DDR5-4800、i5-13500、Windows 11。中文比英文慢是正常的——同一段語意，中文字元吃掉的 token 數不一樣，77 與 96 的差距大致落在這個範圍。

### 4.2 模型卡的完整曲線（提示長度越長，解碼越快）

這張表是 Linux 端量的，但它是唯一有「百 K 到百萬 context」的完整資料，值得單獨看：

| 解碼 | MTP + fast | MTP + precise | 無 MTP + fast | 無 MTP + precise |
| --- | ---: | ---: | ---: | ---: |
| 4K 提示 | 118 | 88 | 96 | 52 |
| 32K | <strong>186</strong> | 130 | 109 | 52 |
| 128K | 165 | 85 | 95 | 50 |
| 256K | 138 | 85 | 79 | 44 |
| 512K | 107 | 69 | 65 | 41 |
| 1M | 111 | 80 | 47 | 31 |

前填充則是另一條曲線：

| 前填充 | MTP 開 | MTP 關 |
| --- | ---: | ---: |
| 4K | 2,368 | 2,295 |
| 32K | <strong>9,610</strong> | 9,390 |
| 128K | 8,894 | 9,047 |
| 256K | 7,313 | 7,339 |
| 512K | 5,094 | 5,095 |
| 1M | 3,090（339 秒） | 3,142 |

同權重的 llama.cpp 在 4K 只有 19.4 tok/s，差距約 6 倍。這個倍數主要來自兩件事：專家留在 page-locked RAM 而不是每次從 mmap 抓、以及 MTP 一次驗多個候選 token。

### 4.3 兩個對不上的地方

| 項目 | Windows Release 頁 | HF 模型卡（4K 列） | 落差 |
| --- | ---: | ---: | --- |
| 解碼 | 96（標「MTP, fast」） | 118（MTP+fast）／96（<strong>無</strong> MTP+fast） | 96 剛好等於「MTP 關掉」 |
| 前填充 | 1,475 | 2,368 | −38% |

第一列的解釋空間不大：模型卡裡 96 這個數字對應的是<strong>沒有 MTP</strong> 的 fast 模式，118 才是有 MTP。所以 Windows 那次的 96，要嘛 MTP 沒真的生效，要嘛量測時把 MTP 關了而備註沒改。兩種都比「Windows 比 Linux 慢 19%」更可能。

第二列的 38% 落差比較可能是<strong>真的平台差異</strong>，可列出的原因有三個，但我沒有實測，只能列出來：

1. Windows 能鎖定的 page-locked RAM 上限遠低於實體記憶體，專家快取的有效命中率會掉；
2. 這版用 <code>STRATA_PORTABLE=ON</code> 編譯（AVX2 baseline、靜態 MSVC runtime），不是 <code>-march=native</code>；
3. 「4K 提示」兩邊的定義可能不同（是否含 tokenize、是否含暖機）。

結論很簡單：<strong>不要把兩張表混著引用</strong>。要對外報數字，就報同一台機器、同一個模式下量到的。

### 4.4 fast 與 precise 的取捨

兩者只差一件事：快取失誤且路由權重很低時要怎麼辦。

| 模式 | 參數 | 行為 | 代價 |
| --- | --- | --- | --- |
| fast | <code>--skip-w 0.4 --prefetch 0</code> | 直接跳過那個專家 | 困惑度 ×1.091 |
| precise | <code>--skip-w 0.4 --prefetch 1</code> | 先預取下一層可能用到的專家，少跳一點 | 困惑度 ×1.008，速度約 −27% |

換句話說，<strong>fast 模式省下來的速度，是用 9% 的困惑度換的</strong>。寫程式、要精準的場合我會選 precise；純聊天、要手感就選 fast。這個 trade-off 原文沒有藏，值得按讚。

## 五、我這台跑不動：RTX 4090 的現實

寫這篇的機器是 RTX 4090、63.7 GB DDR5-6400、i7-13700K。兩項都不合：

| 條件 | 需求 | 本機 | 結果 |
| --- | --- | --- | --- |
| GPU 架構 | sm_120（Blackwell） | sm_89（Ada） | 缺 FP4 tensor core 指令，引擎不會啟動 |
| RAM | 96 GB 建議 | 63.7 GB | 連 59 GiB 的專家 arena 都放不進去 |
| 磁碟 | 72 GB | C: 623 GB 可用 | 唯一合格的一項 |

所以這台機器上跑著的還是原本的 <code>Qwen3.8-Flash-Next</code>（Strata 的 <code>Strata-data</code> 安裝、IQ2_XS）。這也是為什麼本文的數字全部標明出處：<strong>我沒有辦法在自己的機器上重跑一次</strong>，能做的只有把四層來源的數字對齊、把矛盾挑出來。

如果你要在同一台機器上並存兩套，有兩件事要先知道：

1. Nemotron 版是<strong>獨立資料夾、獨立 <code>models\</code></strong>，不會動到原本的 Qwen 安裝；
2. 兩邊預設都用 <code>8080</code>，同時開一定撞。啟動時加 <code>--port</code> 分開。

## 六、Windows 原生編譯：改了什麼

這一段是整篇最有價值的部分，因為它決定了「這東西到底是不是真原生」。從 Release 頁的說明可以還原出四類問題：

| 類別 | 症狀 | 處理 |
| --- | --- | --- |
| 巨集衝突 | Windows 標頭檔的 <code>IN</code> / <code>OUT</code> 與 <code>nemo_model.cpp</code> 裡的同名識別字打架 | 改名，不動標頭 |
| POSIX 依賴 | <code>unistd.h</code>、<code>setenv</code>、<code>SIGPIPE</code> 在 MSVC 不存在 | <code>unistd.h</code> → <code>io.h</code>、<code>setenv</code> → <code>_putenv_s</code>、移除 SIGPIPE 處理 |
| page-locked 上限 | Windows 可鎖定的實體記憶體遠低於機器總量，專家把它吃光後，影像 buffer 直接失敗（<code>no page-locked memory for the image rows</code>） | 影像列改為退回 pageable 記憶體，而不是直接失敗 |
| 工具鏈 | 需要 CUDA 13 的 FP4 支援 | VS 2022 Build Tools（MSVC 14.42）+ CUDA 13.4 |

編譯設定是 <code>STRATA_PORTABLE=ON</code>：AVX2 當基準、靜態連結 MSVC runtime，所以不要求使用者裝 Visual C++ 可轉散發套件；<code>cublas64_13.dll</code> 與 <code>cublasLt64_13.dll</code> 隨包附上，它們是 NVIDIA 的 CUDA 可轉散發元件。

> <strong>白話說</strong>：「原生」不是把 Linux 版包一層 WSL，而是同一份 C++ 原始碼用 MSVC 重編，並把 POSIX 依賴一條一條換掉。那三個 POSIX 依賴（<code>unistd.h</code>、<code>setenv</code>、<code>SIGPIPE</code>）幾乎是每個「從 Linux 移植到 Windows」的專案都會撞到的同一組，改起來不難，但要有人願意改。

## 七、安裝：三條路徑

### 7.1 一鍵版（推薦）

1. 到 Release 頁下載 <code>strata-nemotron-windows-x64.zip</code>，解壓到一個有約 75 GB 空間的磁碟；
2. 雙擊 <code>START-NEMOTRON.bat</code>。

第一次執行它會依序做這些事，中間任何一步失敗都可以再雙擊一次接關：

- 檢查機器（RTX 50 系列、驅動 580+、RAM、磁碟），不合格就<strong>在下載前</strong>停下，不會白吃 72 GB 流量；
- 沒有 Python 就為目前使用者安裝 Python 3.12，並在資料夾內建私有 <code>.venv</code>；
- 下載 Windows 引擎（450 MB）；
- 詢問是否要圖片輸入，然後從 Hugging Face 下載模型到 <code>models\</code>（72 GB，可續傳；讀圖再加 1.7 GB 的 <code>mmproj-BF16.gguf</code>）；
- 解出 tokenizer、啟動伺服器、模型載入完成後自動開 <code>http://127.0.0.1:8080/</code>。

之後每次啟動只做最後一步，載入約 1～4 分鐘。

### 7.2 常用參數

```bat
START-NEMOTRON.bat --no-images            :: 不下載、不啟用視覺（省 1.7 GB）
START-NEMOTRON.bat --port 8081            :: 換 port（跟既有 Strata 並存時必用）
START-NEMOTRON.bat --no-open              :: 不要自動開瀏覽器
```

### 7.3 手動版（已經有引擎或想自己控）

把 Release 解壓到資料夾，兩個 shard 與 <code>mmproj-BF16.gguf</code> 放進 <code>models\</code>，再跑 <code>tools\windows\</code> 底下的啟動腳本（實際檔名以 zip 內容為準；Release 說明在網頁上被截斷，看起來像 <code>run-nemotron.bat</code>）。

### 7.4 接 OpenAI 客戶端

伺服器是 OpenAI 相容的，端點在 <code>http://127.0.0.1:8080/v1</code>。模型名稱不要硬寫，先問一次：

```bash
curl -s http://127.0.0.1:8080/v1/models
```

拿到 id 之後，任何吃 <code>base_url</code> 的工具都能接（Continue、Cline、LiteLLM、Open WebUI 都行）。因為是單機單卡，<strong>併發請求會互搶專家快取</strong>，實務上當成「一次一個人用」比較實際。

## 八、驗收清單

換模型最怕兩件事：換了之後偷偷變笨，或是根本沒生效。這幾項可以五分鐘驗完：

| 檢查 | 怎麼做 | 合格標準 |
| --- | --- | --- |
| 身分 | 問「你是誰、哪家公司訓練的」 | 回答 NVIDIA／Nemotron，<strong>不會</strong>冒出 Qwen 或阿里巴巴 |
| 思考 | 問一題需要多步推理的（例：兩個條件的排班） | 看得到推理段落，不是只有結論 |
| 視覺 | 丟一張有文字的截圖，要求逐字讀出 | 文字正確，且回應時間量級合理（本文機器 19 秒／3,369 token） |
| 中文 | 一段 300 字中文，要求摘要 | 用詞自然、不混簡體、不中英夾雜 |
| 長文 | 貼 3 萬字文件問細節 | 前填充不超時，答案指到正確段落 |
| 速度 | 同一段提示連跑三次 | 變異不大；若掉到十幾 t/s，多半是專家沒鎖進記憶體 |

最後一項特別重要：這套引擎的效能<strong>完全取決於專家命中率</strong>。命中率 96% 時是 96 t/s，命中率掉到一半就會變成兩位數以下的災難。所以「第一次跑很慢」通常不是模型問題，是記憶體被別的東西佔走、page-locked 鎖不進去。

## 九、限制與不適合的場景

原文自己列的限制，加上我認為該補的：

- <strong>影片還不行</strong>。圖片可以（走 Unsloth 的 mmproj + 修過的 RADIO 位置表），影片尚未支援。
- <strong>只有一次性的單機量測</strong>。原文寫得很清楚：表格是「一台機器、一張卡、每個設定跑一次」，增益遠大於 8～12% 的 run-to-run 變異，但那不是信賴區間。
- <strong>沒有下游評測</strong>。除了 25 題的抽查，只有 wikitext 的困惑度（相對 checkpoint ×1.016）。也就是說「中文變好還是變差」這種問題，這份資料<strong>答不了</strong>。
- <strong>24 GB 那列是模擬的</strong>（<code>--vram-limit-mib</code>），16 GB 那組（5080／5070 Ti／5060 Ti 16G + 128 GB RAM）也是模擬出來的 58～93 t/s。真機驗證還沒有。
- <strong>不適合當多人服務</strong>。整個設計是「一張卡 + 一整台 PC 的記憶體」，兩人以上同時用就會互相踢快取。要服務化，該看的是 vLLM／TensorRT-LLM 那條路，而不是這條。

還有一個很少人提的點：<strong>1M context 是「讀得進去」，不等於「記得住」</strong>。前填充 3,090 t/s 讓 1M 文件 339 秒讀完，但長 context 的檢索品質是模型能力問題，不是引擎問題。實際上我建議把長文件切成 32K～128K 的段落，命中率與品質都會好很多。

## 十、授權：這一節才是重點

| 元件 | 授權 | 對採購的意義 |
| --- | --- | --- |
| 引擎（Strata 與其分支） | MIT | 可商用、可修改、可閉源散布 |
| 權重（Nemotron 3.5 Super VL） | OpenMDW-1.1 | 開放模型授權，需保留授權與標註 |
| 量化重打包 | 跟隨權重 | 上面兩個 shard 屬衍生散布 |
| llama.cpp / ggml 元件 | MIT | 與 Strata 相同陣營 |

對「政府機關不能用中國大陸模型」這個場景，這條路的價值有三個：

1. <strong>來源可追溯</strong>：NVIDIA 訓練、NVIDIA 模型卡、NVIDIA 授權條款，沒有轉手；
2. <strong>完全離線</strong>：下載完就是本機檔案，推論不連外，沒有「回傳到哪裡」的問題；
3. <strong>硬體是消費級</strong>：不用買 A100/H100，一張 5090 + 96 GB RAM 就能展示。

但醜話要說在前面：<strong>OpenMDW 不是「隨便用」</strong>，它仍有標註與使用條款；而且真正的採購案要看的還有資料落地、模型卡裡的偏誤與安全說明、以及誰負責更新。這些都不是「換一顆模型」能解決的，所以我前面才說：與其爭模型，不如先把<strong>服務化</strong>這件事想清楚。

## 十一、參考資料

- 引擎（Windows 原生 Release）：<https://github.com/dseditor/Strata/releases>
- 引擎上游分支：<https://github.com/Cudila/Strata>（<code>strata-nemotron</code>）
- 權重（NVFP4 GGUF）：<https://huggingface.co/Cudecnik/Nemotron-3.5-Super-120B-A12B-NVFP4-Strata-Blackwell>
- NVIDIA 原生模型卡：<https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-NVFP4>
- 視覺投影（mmproj）：<https://huggingface.co/unsloth/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-GGUF>
- Strata 本體：<https://github.com/Niko1221/Strata>
- 授權全文：<https://openmdw.ai/license/1-1/>

> <strong>最後提醒</strong>：本文的效能數字來自兩個不同作者、兩台不同機器、兩套不同作業系統，唯一共同的硬體是 RTX 5090。要拿去寫採購規格之前，請在<strong>你自己的機器上</strong>重跑一次第八節的驗收清單——尤其是專家命中率與「你是誰」這兩項，它們比任何跑分都更能說明這套系統有沒有真的在工作。


