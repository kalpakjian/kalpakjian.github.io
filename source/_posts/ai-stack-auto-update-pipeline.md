---
title: 讓本機 AI 堆疊自己照顧自己：Python 3.14 + PyTorch cu132 的自動更新與回滾
date: 2026-10-21 12:00:00
categories:
  - AI
  - 系統自動化
tags:
  - Python
  - PyTorch
  - CUDA
  - transformers
  - Ollama
  - Windows
  - 自動化
  - Hexo
toc: true
index_img: /img/covers/ai-stack-auto-update-pipeline.jpg
banner_img: /img/covers/ai-stack-auto-update-pipeline.jpg
---

![讓本機 AI 堆疊自己照顧自己](/img/covers/ai-stack-auto-update-pipeline.jpg)

> 這篇記錄一套「會自己檢查、自己升級、失敗會自己退回、缺檔會自己補齊」的本機 AI 環境。
>
> 起因很簡單：Python 3.15.0 發布了，但 PyTorch 只出到 `cp314` 的 wheel。
> 如果照「最新穩定版」的直覺升級，`import torch` 會直接失效。
>
> 於是我把「版本檢查」做成一個 skill，再加上 Windows 排程、桌面通知與回滾機制。
>
> **2026-10-22 更新**：補上 cuDNN 檢查（可用性／版本／有沒有完整複製進 CUDA 目錄）、
> 缺檔時用「最高權限按需排程工作」自動補齊，以及升級前後的 GPU 效能基準（`bench_gpu.py`）。

<!-- more -->

## 一、最終環境

| 元件 | 版本 |
|---|---|
| OS | Windows 11 Pro (26220) |
| Python（預設） | **3.14.8** |
| PyTorch | **2.14.1+cu132** |
| torchvision | 0.29.1+cu132 |
| cuDNN | **9.24.0**（隨 torch wheel 內建） |
| torchaudio / torchcodec | 2.11.0 / 0.17.0 |
| transformers | 5.20.2 |
| datasets / accelerate | 5.1.0 / 1.15.0 |
| numpy / pandas | 2.5.4 / 3.0.6 |
| GPU | NVIDIA GeForce RTX 4090 24 GB |
| 驅動 / CUDA UMD | 617.42 / 13.4 |
| Ollama | 0.40.6（21 個模型） |

日常指令：

```powershell
python --version        # Python 3.14.8
py --version            # Python 3.14.8（PY_PYTHON=3.14）
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
# 2.14.1+cu132 True
```

## 二、為什麼是 3.14.8，不是最新的 3.15.0

`python.org` 當時的最新穩定版是 **3.15.0**（2026-10-09），但 PyTorch 2.14.1 的
wheel 檔名只到 `cp314`：

```
torch-2.14.1-cp310-cp310-win_amd64.whl
torch-2.14.1-cp311-cp311-win_amd64.whl
torch-2.14.1-cp312-cp312-win_amd64.whl
torch-2.14.1-cp313-cp313-win_amd64.whl
torch-2.14.1-cp314-cp314-win_amd64.whl   ← 最高
（沒有 cp315）
```

<figure style="margin:1.8rem 0;text-align:center">
  <img src="/img/diagrams/matrix.svg" alt="Python 版本支援矩陣：torch 2.14.1 支援 cp310 到 cp314，cp315 尚未提供" style="width:100%;max-width:960px;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.25)">
  <figcaption style="margin-top:.6rem;color:#64748b;font-size:.9rem">圖 1：Python 版本支援上限。3.14 是目前預設；3.15 因沒有 cp315 wheel 而標為受阻。</figcaption>
</figure>

用 pip 直接問「有沒有更新的」也會得到同樣結論：

```powershell
python -m pip install --dry-run --upgrade --no-deps torch torchvision `
  --index-url https://download.pytorch.org/whl/cu132
# Requirement already satisfied: torch (2.14.1+cu132)
```

所以我把預設 Python 換成 **3.14.8**（3.14 分支最新修補版，含 8 個 CVE 修正）：

- PATH 只保留 `Python314\Scripts`、`Python314`、`Launcher`
- `PY_PYTHON=3.14`，讓 `py` 也預設 3.14（否則 launcher 會挑最高的 3.15）
- 3.15.0 沒有移除，仍可用 `py -3.15` 呼叫

> 一句話：**「最新穩定版」是 Python 的屬性，不是你的環境的屬性。**

## 三、CUDA 版本：目錄存在 ≠ 你能裝

PyTorch 的索引根目錄列出 `cu126`、`cu128`、`cu129`、`cu130`、`cu132`、`cu134`。
如果只看目錄，會以為 `cu134` 是最新。實際探測：

```
cu132: torch-2.14.1+cu132-cp314-cp314-win_amd64.whl → HTTP 200, 1908 MB
cu134: 同檔名 → HTTP 403
cu129: 同檔名 → HTTP 403
```

<figure style="margin:1.8rem 0;text-align:center">
  <img src="/img/diagrams/cuda.svg" alt="CUDA 索引可用性：cu132 是 Windows 最新可用，cu129 與 cu134 沒有 Windows wheel" style="width:100%;max-width:960px;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.25)">
  <figcaption style="margin-top:.6rem;color:#64748b;font-size:.9rem">圖 2：CUDA 索引可用性。目錄存在不代表有 Windows wheel；cu132 才是實際可安裝的最新版本。</figcaption>
</figure>

`cu129` 與 `cu134` 只有 Linux wheel，**Windows 根本沒有檔案**。

所以「最新可用 CUDA」的判定必須是：

1. 解析索引目錄，列出所有 CUDA 索引（`cu126`、`cu128`、`cu132`、`cu134`…）
2. 對每個索引實際 `HEAD` 一個符合「目前 Python + win_amd64」的 wheel
3. 取第一個回 200 的

這也是 `check_stack.py` 裡最重要的一段邏輯。結果：**cu132 才是 Windows 最新可用**。

## 四、四層自動化架構

<figure style="margin:1.8rem 0;text-align:center">
  <img src="/img/diagrams/arch.svg" alt="四層自動化架構：檢查、排程通知、自動升級回滾、按需提權補檔" style="width:100%;max-width:960px;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.25)">
  <figcaption style="margin-top:.6rem;color:#64748b;font-size:.9rem">圖 3：四層自動化架構。檢查層產出 JSON，排程層決定何時通知，升級層負責快照與回滾；第四層是「按需」的最高權限補檔工作。</figcaption>
</figure>

## 五、版本檢查怎麼做到「可信」

| 資料 | 來源 |
|---|---|
| 已安裝版本 | `importlib.metadata`（不匯入套件，快） |
| Python 最新版／EOL | `endoflife.date/api/python.json` |
| 套件最新版 | `pypi.org/pypi/<pkg>/json` |
| torch 最高支援 Python | wheel 檔名的 `cp310`–`cp314` tag |
| 最新可用 CUDA | 索引目錄 + 真實 wheel `HEAD` |
| cuDNN 可用性／版本 | `torch.backends.cudnn.is_available()` / `version()`（`--runtime`） |
| cuDNN 是否完整複製進 CUDA | 比對 `CUDNN\v*` 與 `CUDA\v*` 的 `bin`／`include`／`lib\x64` |
| GPU 效能基準 | `bench_gpu.py`（cuBLAS／cuDNN／HF 基線；`--bench`） |
| Ollama 本機版本 | `localhost:11434/api/version` |
| Ollama 最新版 | GitHub Releases |
| GPU／驅動 | `nvidia-smi` |

### Python 能不能升，怎麼判斷

```python
# 簡化版邏輯
torch_max = max(python tags in latest torch wheels)   # 例：cp310–cp314 → 3.14
if latest_python > torch_max:
    status = f"newer exists (torch max {torch_max})"  # 不建議升
```

### 為什麼輸出全是英文

Windows 主控台在重導向時常用 GBK（cp936）解碼。Python 印中文會變亂碼：

```
[亂碼範例] 1 個 skill...
```

所以腳本輸出固定英文，中文說明放在 `SKILL.md`／`README.md`。這是實際踩過的坑。

## 六、自動更新與回滾

### 流程

<figure style="margin:1.8rem 0;text-align:center">
  <img src="/img/diagrams/flow.svg" alt="自動更新流程：檢查補檔、快照、升級、煙霧測試、pip check、失敗回滾" style="width:100%;max-width:960px;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.25)">
  <figcaption style="margin-top:.6rem;color:#64748b;font-size:.9rem">圖 4：自動更新與回滾流程。先檢查（含 cuDNN）與補檔，再快照、升級、煙霧測試；PASS 保留升級，FAIL 還原快照後再測一次。</figcaption>
</figure>

### 自動升級政策

| 類別 | 套件 | 行為 |
|---|---|---|
| 一般 | transformers、datasets、accelerate、numpy、pandas | ✅ 自動 |
| 音訊 | torchaudio、torchcodec | ✅ 自動（PyPI） |
| PyTorch | torch、torchvision | ✅ 自動，但必須有對應 Python 的 Windows wheel |
| Python | CPython | ❌ 永不（需重裝） |
| Ollama | ollama | ❌ 永不（需重啟服務） |
| CUDA-only | 同版本換 CUDA 索引（如 cu132 → cu134） | ❌ 不自動（1.9 GB） |
| cuDNN | 隨 torch wheel 內建 | ❌ 永不（只有「複製進 CUDA 目錄」要另外顧） |

### 回滾細節

- 只還原**本次有變動**的套件，不是整個環境重裝
- `pip install --force-reinstall --no-deps <name>==<old>`
- torch/torchvision 用**升級前的 CUDA 索引**還原，避免變 CPU 版
- 本次新裝的套件會 `pip uninstall -y`
- 還原後比對 `pip freeze`，有 mismatch → `ROLLBACK_FAILED`
- 退出碼：`0` 成功、`1` 已回滾、`2` 回滾失敗

### cuDNN：檢查、補檔，以及為什麼要提權

cuDNN 跟其他套件不一樣：**它隨 torch wheel 進來**（Windows 在 `torch\lib\cudnn*.dll`），
不能單獨 `pip install --upgrade`。所以檢查分成兩件事：

| 問題 | 怎麼查 | 怎麼修 |
|---|---|---|
| cuDNN 能不能用、版本多少 | `--runtime` 呼叫官方 API，並回報**實際載入的 DLL** | 壞掉就重裝對應索引的 torch wheel |
| 有沒有完整複製進 CUDA 目錄 | 比對 `CUDNN\v*` ↔ `CUDA\v*` 的 `bin`／`include`／`lib\x64` | 缺檔 → 觸發提權工作補齊 |

第二項是「裝新 CUDA／cuDNN 時才會踩到」的坑：**installer 的路徑多一層 CUDA 版本**
（`bin\13.2\x64`、`include\13.2`），照 zip 的寫法打會撈到 0 個檔而**靜默跳過**——
我的 CUDA 13.2 就是這樣漏掉整個 `include`（8 個標頭）。

> 教訓：**「指令沒報錯」不等於「有做事」。** 所以檢查器會把「幾個檔在、幾個檔缺」寫成數字。

### 提權：非提權的排程寫不進 `Program Files`

每日排程是**非提權**執行（`RunLevel: Limited`），所以補檔不能直接在裡面做。
做法是另外註冊一個**最高權限、無觸發**的排程工作，當「按需提權通道」：

```powershell
# 一次性（系統管理員）
powershell -File scripts\register_cudnn_sync_task.ps1 -LogDir "C:\Users\princ\ml-demos\logs"

# 之後非提權的行程就能觸發它（自己啟動自己的工作不會跳 UAC）
schtasks /run /tn "AI Stack cuDNN Sync"
```

檢查器偵測到缺檔 → `--fix-cudnn` 觸發它 → 等它跑完 → **重新掃描**再出報告。
`run_daily.ps1` 的規則是「工作存在就自動帶 `--fix-cudnn`」，所以排程自己就能補檔。

### 升級前後的效能基準（`-Bench`）

```powershell
powershell -File scripts\run_daily.ps1 -AutoUpdate -Bench
```

升級前跑一次、成功後再跑一次，把差異寫進 `auto-update-summary.json` 的 `bench_delta`：

```
Bench: matmul fp16 TFLOPS 185.4->180.1 (-2.9%), conv fp16+CL ms 0.79->0.83 (+5.1%)
```

這樣「新版有沒有變慢」就是一個數字，而不是感覺。

### 實測

**升級：**

```
Auto-update OK: accelerate 1.14.0->1.15.0
Smoke: pass | pip check: pass
```

**強制失敗 → 回滾：**

```
Auto-update FAILED (smoke=forced-fail). Rolling back 1 package(s)...
Rollback completed; post-rollback smoke: pass
result=rolled-back, rollback=success, mismatches={}
accelerate now: 1.14.0
```

**排程端到端：**

```
status = AUTO_UPDATED: accelerate
日誌   = TOAST: toast sent: AI Stack: 1 package(s) auto-updated
next   = 23:00
```


## 七、排程與通知

Windows 工作排程器，每天 23:00（看劇時間，剛好不在電腦前）：

| 項目 | 值 |
|---|---|
| 工作名稱 | `AI Stack Update Check` |
| 觸發 | 每天 23:00 |
| 動作 | `run_daily.ps1 -AutoUpdate` |
| 日誌 | `stack-check-YYYY-MM-DD.log` |
| 狀態 | `OK` / `AUTO_UPDATED: ...` / `ROLLED_BACK: ...` |
| 保留 | 90 天 |

另外註冊了一個**按需**的提權工作，專門補 cuDNN 檔：

| 項目 | 值 |
|---|---|
| 工作名稱 | `AI Stack cuDNN Sync` |
| 權限 | 最高權限（`RunLevel Highest`） |
| 觸發 | 無（按需；由檢查或每日排程觸發，不跳 UAC） |
| 動作 | `sync_cudnn.ps1`：只補缺的檔（幂等，可 `-WhatIf`） |
| 日誌 | `cudnn-sync-YYYY-MM-DD.log`（與每日日誌同目錄） |

有更新時會發 WinRT toast（不用安裝 BurntToast）：

```
AI Stack: 1 package(s) auto-updated
accelerate
Smoke: pass | pip check: pass
```

AppUserModelID 註冊在 HKCU，名稱顯示為 **AI Stack Check**。
若沒看到通知，先檢查專注模式／勿擾與通知設定。

## 八、這套環境的實測性能

| 工作負載 | 數字 |
|---|---|
| DistilBERT 批次情感推論 | **3,243 texts/s**（10,000 筆 3.08 秒） |
| ViT-base 影像分類 | 5.7 ms/張 |
| DistilBERT 微調（2,000 筆、1 epoch） | **2.0 秒**，驗證準確率 **85.2%** |
| Whisper-base 語音轉錄 | **WER 0.0%**、88.7× 即時 |
| Ollama gemma4:12b | **92.1 tok/s**（8 GB VRAM 全卸載） |
| 峰值 VRAM（HF 推論） | 795 MB |

這些數字是在同一台機器、同一套 cu132 環境測的，可作為「升級後有沒有變慢」的基準。

### 現在可以自動重測（`bench_gpu.py`）

2026-10-22 加了 `bench_gpu.py`，把最關鍵的幾項變成可重複執行的基準（同機同環境重測）：

| 項目 | 數字 | 備註 |
|---|---|---|
| DistilBERT SST-2（batch 64） | **3,130 texts/s** | 與上表 3,243 同一水準（±4%） |
| ViT-base 224（batch 1／32） | **5.51**／1.00 ms/張 | 對照上表 5.7 ms（單張延遲） |
| cuBLAS matmul fp16／bf16 | **185.4**／159.5 TFLOPS | |
| cuBLAS matmul fp32（TF32 off → on） | 59.8 → **82.5 TFLOPS** | TF32 +38% |
| cuDNN conv fp16 + `channels_last` | **0.790 ms**（fp32 1.771 ms） | 2.24×，VRAM 656 → 107 MB |
| flash attention（SDPA fp16） | 0.074 ms／116.3 TFLOPS | |
| `cudnn.benchmark` 開關 | 1.836 → 1.836 ms | 固定形狀沒差（autotune 0.03 秒） |

搭配 `auto_update.py --bench`（升級前後各跑一次），就能一眼看出「新版有沒有變慢」。

## 九、踩過的坑

| 坑 | 現象 | 解法 |
|---|---|---|
| HF 快取結構 | `snapshots/<hash>/data/*.parquet`，用 `snapshots/*/` 找不到 | 改用 `**` 遞迴 |
| `nvidia-smi` 欄位改名 | 新版驅動是 `CUDA UMD Version: 13.4`，不是 `CUDA Version` | regex 同時接受兩種 |
| PowerShell 把 git stderr 當錯誤 | `git push` 明明成功，卻顯示紅字 | 用 `git ls-remote` 驗證 SHA |
| 中文輸出亂碼 | Python stdout 是 gbk | 腳本輸出全英文 |
| torchaudio 版本脫鉤 | 最新是 2.11.0，不是 2.14 | 不 pin torch 版本；解碼交給 torchcodec |
| uv 索引落後 | `uv python list` 還看不到 3.15.0 正式版 | 用 python.org 安裝包 |
| cuDNN 只抄了 bin／lib | CUDA 13.2 的 `include` 整批漏掉（8 個標頭） | 檢查器比對 `CUDNN\v*` ↔ `CUDA\v*`，缺檔就警告 |
| installer 的路徑多一層 | 照 zip 的 `include\*` 打 → 撈到 0 個檔、**靜默跳過** | 來源要寫 `include\13.2\*` |
| 提權才能寫 `Program Files` | 非提權的排程補不了檔 | 註冊最高權限的按需工作，用 `schtasks /run` 觸發 |
| 單獨載入 cudnn DLL 問版本 | 回報 9.26.0，但 torch 實際用 9.24.0 | 只信 `--runtime` 的官方 API |
| `.ps1` 存成 UTF-8 無 BOM | PS 5.1 用 ANSI 解讀，中文字元吃掉引號 → 語法錯誤 | `.ps1` 一律存 UTF-8 **with BOM** |
| 對 GB 級檔案做 SHA256 | 補檔腳本跑到超時 | 大檔只比大小，≤64 MB 才雜湊 |

## 十、開源

程式碼已放到公開 repo：

**https://github.com/kalpakjian/ai-stack-update-check**

```
ai-stack-update-check/
├─ README.md
├─ SKILL.md                        # agent skill 定義
├─ LICENSE                         # MIT
├─ docs/                           # README 用的架構／流程圖（SVG）
└─ scripts/
   ├─ check_stack.py               # 版本檢查 + cuDNN 檢查（stdlib only）
   ├─ auto_update.py               # 升級 + 回滾（--bench 可加效能對比）
   ├─ bench_gpu.py                 # GPU 效能基準（cuBLAS／cuDNN／HF 基線）
   ├─ run_daily.ps1                # 排程包裝（-Bench、-FixCudnn）
   ├─ notify.ps1                   # WinRT toast
   ├─ sync_cudnn.ps1               # 提權補檔工作本體
   └─ register_cudnn_sync_task.ps1 # 一次性註冊提權工作
```

最簡單的用法：

```powershell
git clone https://github.com/kalpakjian/ai-stack-update-check.git
cd ai-stack-update-check
python scripts\check_stack.py
```

也可以 agent skill 的形式使用：

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.agents\skills\ai-stack-update-check"
```

## 十一、結論

1. **版本號不等於相容性。** 3.15.0 是最新，但 torch 只到 cp314；真正該看的是 wheel 的 Python 標籤（`cp314`）。
2. **目錄存在不等於能安裝。** `cu134` 有目錄、沒有 Windows 檔；必須對實際 wheel 發請求。
3. **自動化要能回頭。** 沒有快照與回滾的自動升級，是把風險放大，不是省時間。
4. **通知要能被驗證。** 每次 toast 都寫一行 `TOAST:` 進日誌，才知道是「沒更新」還是「通知壞了」。
5. **排程要離線可跑。** `--no-network` 模式讓你在沒網路時仍能看到目前版本。
6. **權限也要能自動化。** 非提權的排程寫不進 `Program Files`；用「一次性註冊的最高權限按需工作」補上，才不會退回人手。
7. **「指令沒報錯」不等於「有做事」。** 漏抄 include 不會報錯，只會少檔——所以要把「幾個在、幾個缺」變成數字。

下一步想做的（部分已完成）：

- ✅ **升級前後的效能基準已自動化**：`bench_gpu.py` ＋ `auto_update.py --bench`，
  把 `bench_delta` 寫進日誌（上面的實測表就是它的輸出）。
- 還沒做：把 **Whisper 轉錄**也納入基準（需要固定的音檔與 WER 參考稿），
  以及把「升級後效能退步 > 5%」做成自動告警。

