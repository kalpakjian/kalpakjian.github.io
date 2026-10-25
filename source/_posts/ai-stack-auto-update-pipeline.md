---
title: 讓本機 AI 堆疊自己照顧自己：Python 3.14 + PyTorch cu132 的自動更新與回滾｜Linux／Omarchy 實戰篇
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
  - Linux
  - Omarchy
  - Arch
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
>
> **2026-10-26 更新**：同一套堆疊搬到 Linux（Omarchy／Arch）上重做一次——驅動 610.57.04 → 615.78.08、
> torch 升到 cu132／cu134、兩個 venv（stable ＋ nightly）各自驗證 cuDNN，並新增 `audit_venv.py`（22 項完整性審計）。
> **新章節 §十** 記錄 Linux 版的安裝、三個 Windows 沒有的坑，以及一個反直覺的結論：
> **真正讓效能變快的是驅動更新，不是 wheel 升級。**
>
> **2026-10-26 補完**：Linux 版的腳本已**開源**到 `ai-stack-update-check` 的 `scripts/linux/`，
> 並接上 **systemd user timer ＋ 桌面通知**（每日 23:00）；
> ComfyUI 落後的 263 個 commit 也補齊了（上游移除 torchaudio 的坑根治）；
> 至於「移除 nightly 的 `tensorrt_libs` 回收 4.4 G」——**實測後改成只裁掉用不到的資源檔**，
> 因為 nightly 其實在跑 H3 TRT-VAE，整包移除會弄壞工作流。細節見 §十。

<!-- more -->

## 一、最終環境

### Windows 11（自動更新管線本體）

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

### Linux／Omarchy（2026-10-26 新增，同一張 RTX 4090）

| 元件 | 版本 |
|---|---|
| OS | **Omarchy**（Arch-based），核心 `7.2.8-9-omarchy` |
| 驅動 | `nvidia-open-dkms` **615.78.08-1**（CUDA UMD **13.4**） |
| Python | **3.12.14**（兩個 venv 都是 3.12） |
| torch（stable） | **2.14.1+cu132** |
| torch（nightly） | **2.16.0.dev20261025+cu134** |
| cuDNN | stable **9.24.0.43**／nightly **9.26.0.51** |
| 環境 | `~/Projects/ComfyUI/.venv`（6.9 G）、`~/Projects/ComfyUI/.venv-nightly`（12 G → 裁切後 8.4 G，見 §十） |

Linux 版的安裝過程、踩坑、審計與實測見 **§十**。

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

> 上面 11 個坑是 Windows 版的。Linux 版有**三個形態完全不同的坑**（wheel 路徑互相覆蓋、
> torchaudio 缺 cp312 wheel、`uv pip` 的索引策略），見 **§十**。

## 十、在 Linux（Omarchy）上：同一套堆疊的另一個戰場

### 為什麼要再做一次

Windows 那套是**便攜版**：整個 Python 環境跟 ComfyUI 一起放進 `D:\AI\ComfyUI`，
用工作排程器每天檢查。Linux／Omarchy 這台是**系統級**環境：套件由 `pacman` 管、
GPU 由核心模組管、Python 環境用 `uv` 管成 venv。

兩邊的失敗模式完全不同，所以整套流程必須**重做一次**，而不是把 Windows 的腳本搬過去。

| 面向 | Windows 11 | Linux／Omarchy |
|---|---|---|
| 驅動來源 | NVIDIA 安裝程式（`.exe`） | `pacman`：`nvidia-open-dkms` 615.78.08-1 |
| 核心 | Windows 內建 | `linux-omarchy` 7.2.8-9-omarchy |
| Python 環境 | 便攜版 `python_embeded\` | venv：`~/Projects/ComfyUI/.venv`（stable）、`~/Projects/ComfyUI/.venv-nightly`（nightly） |
| 安裝工具 | `pip` | `uv pip`（索引策略不同，見〈坑 3〉） |
| cuDNN 檔案 | `torch\lib\cudnn*.dll` | `nvidia/cudnn/lib/libcudnn.so.9` |
| 回滾 | `pip install --force-reinstall` | `uv pip install -r rollback/*.freeze.txt` |
| 排程 | 工作排程器 + WinRT toast | systemd user timer + `notify-send`（已接） |

### 驅動升級：Linux 走的是套件管理

這是整個升級裡**最關鍵、也最反直覺**的一段。

```bash
# 升級前
kernel            7.2.5-3-omarchy
nvidia-open-dkms  610.57.04
CUDA UMD          13.3

# 升級後（omarchy update / pacman -Syu，然後重開機）
kernel            7.2.8-9-omarchy
nvidia-open-dkms  615.78.08-1
CUDA UMD          13.4
```

Linux 上不需要「下載驅動安裝程式」：`nvidia-open-dkms` 會跟著核心一起重建模組。
**但開 DKMS 一定會重編核心模組**，所以升完核心必須重開機，才會真正換到新驅動；
中途 `nvidia-smi` 還顯示舊版，就是模組還沒換。

> 教訓：**Linux 上「更新套件」與「更新驅動」是同一件事**，
> 沒有安裝精靈可以慢慢按，也沒有「記得重開機」提示——忘記重開就會以為沒升成。

### 兩個 venv：stable ＋ nightly

| | stable | nightly |
|---|---|---|
| 路徑 | `~/Projects/ComfyUI/.venv` | `~/Projects/ComfyUI/.venv-nightly` |
| torch | **2.14.1+cu132** | **2.16.0.dev20261025+cu134** |
| torchvision | 0.29.1+cu132 | 0.30.0.dev20261025+cu134 |
| torchaudio | 2.11.0.dev20260902+cu132 | 2.11.0.dev20261025+cu134 |
| triton | 3.8.0 | 3.9.0 |
| NCCL | 2.30.7 | 2.32.3 |
| cuDNN | **9.24.0.43** | **9.26.0.51** |
| 套件數 | 130 | 140 |
| 磁碟 | 6.9 G | 12 G（裁切後 8.4 G） |

**為什麼要兩個？** nightly 是 dev 版，本來就會壞。把它跟 stable 放同一個 venv，
一壞就是整天不能用；分成兩個之後，stable 永遠是已知可用的版本，
nightly 壞掉只影響「試新功能」這件事。

> nightly 多出來的 4.4 G 是 `tensorrt_libs` 11.3.0.99（cu13 版，升級前就存在），
> 屬於**選用**加速路徑：`comfy_kitchen` 與 torch 都不宣告依賴它，沒有也不影響一般推理。
> 不需要 TensorRT 的話可以整包移除。

**但「整包移除」在這台機器上是錯的**——nightly 正是跑 MiniMax H3 TRT-VAE 的環境
（`run_nightly.sh` 明確用 `.venv-nightly/bin/python` 啟動，兩個 `.engine` 也在 `models/vae/`）。
真正該做的是**只裁掉永遠不會被載入的資源檔**：NVIDIA 的 wheel 把**所有** GPU 架構的
builder resource，連同 **Windows 專用**的那 8 個 blob，一起塞進 `tensorrt_libs/`：

| 檔案群 | 大小 | RTX 4090（sm_89）需不需要 |
|---|---|---|
| `libnvinfer_builder_resource_sm89.so` | 180 MiB | 要 |
| `libnvinfer_builder_resource_ptx.so` | 230 MiB | 要（PTX JIT fallback） |
| `..._sm75/80/86/90/100/120.so` | 1.41 GiB | 不要 |
| `..._win_*.so`（8 個） | 1.81 GiB | 不要（Windows 專用） |
| `libnvinfer.so` / `_plugin.so` / `_onnxparser.so` | 0.71 GiB | 要 |

搬走 14 個檔案＝回收 **3.29 GiB**（nightly 12 G → 8.4 G），`sm89` 與 `ptx` 留著。
驗證不是「感覺沒事」而是三關都過：ONNX → engine 編譯 OK、
`minimax_h3_vae_encoder.engine` 與 `minimax_h3_vae_decoder.engine` 反序列化 OK、
ComfyUI 實機煙霧測試 `exit=0` 且 `ComfyUI-H3VAE_TRT` 自訂節點正常載入。
`RECORD` 不動，所以 `uv pip check` 依然全綠。

### 三個 Linux 特有的坑

#### 坑 1：cu12 與 cu13 的 wheel 裝到**同一個路徑**

這是最兇狠的一個坑，也是卡最久的一個。

`nvidia-*-cu12-*` 與 `nvidia-*-cu13-*` 這兩套 wheel，安裝路徑**完全重疊**：

```
nvidia/nccl/lib/libnccl.so.2
nvidia/cudnn/lib/libcudnn.so.9
nvidia/nvshmem/lib/libnvshmem_host.so.3
```

pip／uv 不會知道兩邊是不同套件——**後裝者直接覆蓋先裝者**。症狀有兩種：

| 症狀 | 原因 |
|---|---|
| `libtorch_cuda.so: undefined symbol: ncclCommResume` | cu12 版 `libnccl.so.2` 覆蓋了 cu13 版 → **torch 連 import 都失敗** |
| `importlib.metadata` 回報 cuDNN **9.19.0.56** | 殘留 15 個孤兒 `nvidia_*_cu12-*` dist-info 被 metadata 掃到 → **版本是假的** |

第二種最陰險：**它不會報錯**，只會安靜地給你一個錯的版本號，
讓你以為 cuDNN 沒裝對、到處找問題。

清理方式（`cleanup_cu12_orphans.py`）：

- 刪掉 **15 個**孤兒 `nvidia_*_cu12-*` dist-info
- 刪掉 **352 個**只屬於 cu12 的檔案
- 對 4 個路徑重疊的套件（cudnn／cusparselt／nccl／nvshmem）從 cu132 index **強制重裝**，確保 cu13 版本在位

結果：套件數 **145 → 130**，NCCL 符號齊全，`uv pip check` 通過。

> 教訓：**Linux 上 pip 的「已安裝」是一個檔案系統狀態，不是一個資料庫**。
> 兩個索引的同名套件共存過一次，就永遠要懷疑它。

#### 坑 2：stable 索引沒有 torchaudio 的 cp312 wheel

`https://download.pytorch.org/whl/cu132/torchaudio/` 底下 248 個 wheel，
**cp312 只有 `2.2.0-linux_aarch64`**——沒有 x86_64。

連鎖反應：

```bash
uv pip install --upgrade torchaudio
# 什麼都沒發生：uv 認為 2.11.0+cu130 > 2.11.0（+cu130 是本機版本號）
```

torchaudio 留在 cu130，而 torch 已經升到 cu132 → ComfyUI **一啟動就崩**：

```
RuntimeError: PyTorch has CUDA version 13.2 whereas TorchAudio has CUDA version 13.0
```

觸發點是 `comfy/ldm/lightricks/vae/audio_vae.py` 的**硬 import torchaudio**
（本機 checkout 共 5 處硬 import）。

解法是改從 nightly 索引撈：

```bash
uv pip install --python .venv/bin/python \
  torch==2.14.1+cu132 torchvision==0.29.1+cu132 torchaudio==2.11.0.dev20260902+cu132 \
  --index-url https://download.pytorch.org/whl/nightly/cu132 \
  --extra-index-url https://download.pytorch.org/whl/cu132 \
  --index-strategy unsafe-best-match
```

> ⚠️ `--index-strategy unsafe-best-match` 會打破「單一索引一致性」保護，
> **必須同時釘住 torch／torchvision 的版本**，否則會被 nightly 一起帶走。

**上游正解**：ComfyUI 的 `origin/master` 已改用自帶的 `comfy/audio.py`
（MelSpectrogram／resample），`requirements.txt` 裡**只剩 torch／torchsde／torchvision，torchaudio 整條被移除**。
本機 checkout 落後 263 個 commit，`git pull` 就能根治這個坑。

> ✅ **2026-10-26 實作完成**：落後的 263 個 commit 已補齊（`a78a22e` → `fe298e4`），
> 上游移除 torchaudio 的 commit 是 `b16023b "Remove torchaudio dependency. (#16457)"`，
> 拉下來之後 `requirements.txt` 確實沒有 torchaudio、`comfy/audio.py` 確實存在。
> 順帶發現上游把 `comfy-aimdo` 從 0.5.3 提到 0.6.0、`comfy-kitchen` 0.2.34 → 0.2.40，
> 舊版 `comfy_aimdo` 沒有 `storage` 子模組，ComfyUI 會直接起不來——
> 所以 `git pull` 之後**還要**把這幾個套件升級，但**不能**讓 pip 順手動到 torch。
> 用 `uv pip install --dry-run` 先看清楚會動到什麼，再只升該升的：

```bash
uv pip install --dry-run --python .venv/bin/python \
  comfyui-frontend-package==1.57.1 comfyui-workflow-templates==0.11.96 \
  comfyui-embedded-docs==0.5.14 comfy-kitchen==0.2.40 comfy-aimdo==0.6.0
# → Would uninstall 8 packages / Would install 9 packages
#   （torch、torchvision、numpy 全都不在名單裡）
```

#### 坑 3：`uv pip` 的「first index wins」

pip 與 uv 的索引策略不同：uv 預設**第一個有該套件的索引就贏**，
不像 pip 會把多個索引的版本集合起來比較。所以：

- 想從 cu132 stable 拿 torch、又要從 cu132 nightly 拿 torchaudio → 必須 `--index-strategy unsafe-best-match`
- 用了 unsafe 之後 → **必須自己釘版本號**，因為保護已經沒了

> 一句話：**uv 比較嚴格，pip 比較寬鬆；嚴格的那個要你手動補釘版本。**

### cuDNN 版本要三路交叉驗證

Windows 那邊踩過的坑是「單獨載入 cudnn DLL 問版本，回報 9.26.0 但 torch 實際用 9.24.0」。
Linux 這邊更直接：**cuDNN 9 的 `.so` 檔裡沒有任何明文版本字串**，`strings` 只會挖到雜訊。

所以我改用三個互相獨立的來源交叉比對：

| 來源 | 做法 | stable | nightly |
|---|---|---|---|
| 套件 metadata | `importlib.metadata.version("nvidia-cudnn-cu13")` | 9.24.0.43 | 9.26.0.51 |
| **磁碟上的 `.so`** | `ctypes` 直接對 `libcudnn.so.9` 呼叫 `cudnnGetVersion()`（**完全不經 torch**） | 9.24.0 | 9.26.0 |
| torch 執行期 | `torch.backends.cudnn.version()` | 92400 → 9.24.0 | 92600 → 9.26.0 |

三者一致才算通過。再加上 `/proc/self/maps` 確認實際載入的是
**venv 內部**的 `nvidia/cudnn/lib/libcudnn_graph.so.9`，不是系統那份。

> 為什麼要這樣麻煩？因為「版本號」在 Linux 上可能是 metadata 的謊言（坑 1），
> 也可能是 runtime 的謊言（Windows 那邊的 DLL 坑）。
> 唯一能證明「我用的是哪一份」的方式，是**對實際載入的那個檔案問**。

### `audit_venv.py`：22 項完整性審計

Windows 版的 `check_stack.py` 檢查的是「有沒有新版本」；
Linux 版的 `audit_venv.py` 檢查的是「**現在這個環境到底完不完整**」——
因為坑 1、坑 2 都屬於「沒報錯但其實壞掉」的類型。

7 組共 22 項，兩個 venv 都是 **0 failed / 0 warnings → PASS**：

| 檢查組 | 內容 | stable | nightly |
|---|---|---|---|
| ① 核心套件 | torch／torchvision／torchaudio／triton 版本與 CUDA 一致性 | 2.14.1 / 0.29.1 / 2.11.0.dev20260902 / 3.8.0 | 2.16.0.dev20261025 / 0.30.0.dev20261025 / 2.11.0.dev20261025 / 3.9.0 |
| ② cu12／cu13 一致性 | 4 個 cu13 套件，無 cu12 殘留 | OK | OK |
| ③ 安裝完整性 | RECORD 齊全／無孤兒 dist-info／無 cu12-cu13 檔案歸屬衝突 | OK | OK |
| ④ **cuDNN 正確性** | metadata ↔ 磁碟 `.so` ↔ torch runtime 三方一致 ＋ 載入來源 | 9.24.0 | 9.26.0 |
| ⑤ NCCL | 符號完整 ＋ 載入來源 ＋ 版本 | 2.30.7 | 2.32.3 |
| ⑥ 功能測試 | fp16 matmul／cuDNN conv 數值正確性／SDPA／torch.compile／tv.ops.nms／torchaudio | conv max abs err 0.00191 | 0.00192 |
| ⑦ 相容性 | `uv pip check` | 130 packages OK | 140 packages OK |

ComfyUI 煙霧測試（`main.py --quick-test-for-ci`）兩個環境都是 **exit=0、0 個自訂節點匯入失敗**。

> 這個審計器的價值在於：**它是「沒有壞掉」的證明**。
> 升級之後不跑它，你永遠不知道坑 1 有沒有在你下次 `pip install` 時復發。

### 效能實測：真正變快的是**驅動**，不是 wheel

這是整個 Linux 版最值得記錄的結論，而且**跟直覺相反**。

同一支腳本 `bench_stack.py`（形狀由原始基準檔逆向擬合還原），
在**同一張卡、同一個核心版本**下做了 A/B/C 三組：

| 組態 | fp16 matmul (TFLOPS) | tf32 on | bf16 | conv fp32 (ms) | conv fp16 (ms) | conv fp16 + CL (ms) | SDPA (ms) |
|---|---|---|---|---|---|---|---|
| 升級前（cu130 + drv610） | 156.4 | 80.7 | 161.1 | 1.603 | 1.044 | 0.809 | 0.058 |
| A：cu130 ＋ **drv615** | 156.6 | 80.9 | 161.7 | **1.421** | **0.979** | **0.731** | 0.057 |
| B：cu132 ＋ drv615 | 156.2 | 80.6 | 161.5 | 1.416 | 0.980 | 0.731 | 0.057 |
| C：cu134 ＋ drv615 | 147.5 | 80.8 | 161.5 | **1.382** | **0.961** | 0.733 | 0.057 |

結論拆成兩句：

1. **driver 更新（升級前→A）**：cuDNN conv fp16 **+6.2%**、channels_last **+9.6%**、fp32 conv **+11.4%**
2. **wheel 升級（A→B）**：各項持平（±0.5% 內）——**cu132 相對 cu130 幾乎沒有差別**

端到端也一致（SD1.5、512×768、20 步、seed 42、中位數 ×3）：

| 組態 | 生成時間 | vs cu130 |
|---|---|---|
| cu130 | 3.05 s | — |
| cu132 | 3.04 s | −0.3% |
| cu134 | 3.01 s | −1.3% |

三對組合的輸出逐像素比對，mean abs diff 皆 ≈ 0.32/255、差異 > 2 的像素 ≈ 1.7~1.8%，
幅度完全一致 → **差異純屬 cuDNN kernel 選擇的正常非確定性，演算法輸出沒變**。

> **為什麼會這樣？** CUDA runtime 與 cuDNN 真正吃效能的那段是跑在 **driver 提供的核心碼**裡。
> wheel 換版本只換了前端 API 與部分 kernel，而 conv kernel 的選擇與排程是 driver 層的東西。
> 所以升 driver 的收益遠大於升 wheel。

> ⚠️ **跨平台的數字不要直接相減**：Windows 版的 `bench_gpu.py` 與 Linux 版的 `bench_stack.py`
> 用的形狀不同（Linux 版的形狀是從原始基準檔逆向擬合出來的），
> 兩邊的絕對值不能互比，只能各自跟自己的「升級前」比。

### 兩條必須記住的量測紀律

1. **基準腳本不可並行**：三個 bench 同時跑會搶同一張 GPU，數字失真（SDPA 0.058 → 0.212 ms）。
   必須**逐一循序**執行。
2. **換 seed**：ComfyUI 會重用上游節點的執行快取，同 seed 重跑會秒回，測到的是快取值。

### 每日排程：systemd user timer ＋ 桌面通知

Windows 那套是「工作排程器 ＋ WinRT toast」；Linux 端用 **systemd user timer**
（**user** scope：不用 root 權限，桌面通知一定送得到，日誌留在自己的家目錄）：

```bash
cd scripts/linux
./install_systemd_user.sh                            # 安裝 unit + enable --now
systemctl --user start ai-stack-check.service         # 立刻跑一次
systemctl --user list-timers ai-stack-check.timer --no-pager
journalctl --user -u ai-stack-check.service -n 50 --no-pager
```

| 項目 | 值 |
|---|---|
| Unit | `ai-stack-check.service` ＋ `ai-stack-check.timer`（user scope） |
| 觸發時間 | 每天 23:00（`RandomizedDelaySec=300`） |
| 補跑 | `Persistent=true`：當時電腦關著，開機後會補跑一次 |
| 日誌 | `~/.local/state/ai-stack-update-check/stack-check-YYYY-MM-DD.log`（保留 90 天） |
| 狀態檔 | 同目錄 `stack-check-status.txt`（`OK`／`UPDATES: …`／`PROBLEM: …`） |
| 桌面通知 | `notify-send`（沒有 session bus 時退回寫 journal，不會讓排程整個失敗） |
| 登出也要跑 | `sudo loginctl enable-linger "$USER"` |

每日流程是：堆疊檢查（`check_stack.py --runtime --json`）→ 兩個 venv 各跑一次
22 項稽核 → 寫日誌與狀態檔 → 送通知。實測 `systemctl --user start` 回
`status=0/SUCCESS`，通知訊號也真的送到 D-Bus（`member=Notify`）。

**Linux 這邊刻意不做自動升級。** Windows 的 `run_daily.ps1 -AutoUpdate` 沒有對應功能，
而且不該有：

| Linux 的風險 | 後果 |
|---|---|
| `pacman` 是 rolling release | partial upgrade 會直接把系統弄壞 |
| NVIDIA 驅動是 DKMS 套件 | 升級後**一定要重開機**才會換到新模組 |
| cu12／cu13 wheel 共用安裝路徑 | `pip` 會覆寫掉另一個 venv 需要的 `.so` |
| torch nightly 本身就是 dev 版 | 一個 nightly 壞掉就少一個可用環境 |

所以 Linux 只做「檢查 ＋ 通知」，升級留給人決定。

### 已補完的部分（2026-10-26 更新）

上次列的「還沒做」清單，現在都補上了——但其中一件的**做法跟當初預期不同**：

| 原待辦 | 現在的結果 |
|---|---|
| Linux 腳本開源 | ✅ 已收進 `ai-stack-update-check` 的 `scripts/linux/`：`audit_venv.py`、`verify_stack.sh`、`bench_stack.py`、`compare.py`、`cleanup_cu12_orphans.py`，外加新寫的 `trim_tensorrt_resources.py` |
| 接 systemd timer ＋ 桌面通知 | ✅ `ai-stack-check.service` ＋ `.timer`（user scope），實測跑通 |
| `git pull` ComfyUI | ✅ 落後的 263 個 commit 補齊，`comfy-aimdo` 等 5 個套件也升到上游指定版本（torch 未被動到） |
| 移除 nightly 的 `tensorrt_libs`（回收 4.4 G） | ⚠️ **沒有整包移除**——nightly 其實在跑 H3 TRT-VAE。改成**只裁掉永遠不會被載入的架構資源檔**，回收 **3.29 GiB** |

還沒做的只剩一件：

- Python 3.15 遷移：cu132／cu134 已有 cp315 wheel，建議排在 wheel 升級之後。

## 十一、開源

程式碼已放到公開 repo：

**https://github.com/kalpakjian/ai-stack-update-check**

```
ai-stack-update-check/
├─ README.md
├─ SKILL.md                        # agent skill 定義
├─ LICENSE                         # MIT
├─ docs/                           # README 用的架構／流程圖（SVG）
└─ scripts/
   ├─ check_stack.py               # 版本檢查 + cuDNN 檢查（stdlib only；Windows／Linux 共用）
   ├─ auto_update.py               # 升級 + 回滾（--bench 可加效能對比）
   ├─ bench_gpu.py                 # GPU 效能基準（cuBLAS／cuDNN／HF 基線）
   ├─ run_daily.ps1                # 排程包裝（-Bench、-FixCudnn）
   ├─ notify.ps1                   # WinRT toast
   ├─ sync_cudnn.ps1               # 提權補檔工作本體
   ├─ register_cudnn_sync_task.ps1 # 一次性註冊提權工作
   └─ linux/                       # ★ Linux／Omarchy 版（2026-10-26 新增）
      ├─ run_daily.sh              # 每日檢查 + 各 venv 稽核 + 日誌 + 通知
      ├─ notify.sh                 # notify-send 桌面通知
      ├─ install_systemd_user.sh   # 安裝 systemd user timer
      ├─ verify_stack.sh           # 驅動／CUDA／雙 venv／功能測試（--full 加煙霧測試）
      ├─ audit_venv.py             # 單一 venv 的 22 項完整性稽核
      ├─ bench_stack.py            # 可重現的 GPU 基準（輸出 JSON）
      ├─ compare.py                # 多份基準 JSON 對照表
      ├─ cleanup_cu12_orphans.py   # 清孤兒 nvidia_*_cu12-* dist-info
      └─ trim_tensorrt_resources.py # 裁掉用不到的 TensorRT 架構資源檔
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

> `check_stack.py` 是 **Windows／Linux 共用**的：它自己判斷平台，
> Windows 探 `win_amd64` wheel、Linux 探 `manylinux_2_28_x86_64`；
> Linux 還多報三列系統層資訊——NVIDIA 驅動**套件版本**對照**目前實際載入的驅動版本**
> （兩者不同就是還沒重開機）、正在跑的 kernel、以及 `pacman` 上可升級的套件。
> Linux 的每日排程用 systemd user timer，見 **§十〈每日排程〉**。

## 十二、結論

1. **版本號不等於相容性。** 3.15.0 是最新，但 torch 只到 cp314；真正該看的是 wheel 的 Python 標籤（`cp314`）。
2. **目錄存在不等於能安裝。** `cu134` 有目錄、沒有 Windows 檔；必須對實際 wheel 發請求。
3. **自動化要能回頭。** 沒有快照與回滾的自動升級，是把風險放大，不是省時間。
4. **通知要能被驗證。** 每次 toast 都寫一行 `TOAST:` 進日誌，才知道是「沒更新」還是「通知壞了」。
5. **排程要離線可跑。** `--no-network` 模式讓你在沒網路時仍能看到目前版本。
6. **權限也要能自動化。** 非提權的排程寫不進 `Program Files`；用「一次性註冊的最高權限按需工作」補上，才不會退回人手。
7. **「指令沒報錯」不等於「有做事」。** 漏抄 include 不會報錯，只會少檔——所以要把「幾個在、幾個缺」變成數字。
8. **Linux 上的套件狀態是檔案系統事實，不是一個資料庫。** 兩個 CUDA 索引的同名 wheel 會覆蓋彼此，
   而孤兒 dist-info 會讓 `importlib.metadata` 報一個**假的** cuDNN 版本——不報錯，只會騙你。
9. **版本要三路交叉驗證。** 套件 metadata、對磁碟上的 `.so` 直接問、torch 執行期回報，
   三者一致才算數。Windows 的 DLL 坑與 Linux 的 dist-info 坑，是「單一來源會騙你」的兩個變體。
10. **效能瓶頸可能在 driver，不在 wheel。** 同一張卡、同一核心版本下，
    driver 610→615 帶來 cuDNN conv +6~11%，而 cu130→cu132 的 wheel 升級落在 ±0.5% 內。
    所以升級前先量「driver 變了會怎樣」，再決定要不要換 wheel。

下一步想做的（部分已完成）：

- ✅ **升級前後的效能基準已自動化**：`bench_gpu.py` ＋ `auto_update.py --bench`，
  把 `bench_delta` 寫進日誌（上面的實測表就是它的輸出）。
- 還沒做：把 **Whisper 轉錄**也納入基準（需要固定的音檔與 WER 參考稿），
  以及把「升級後效能退步 > 5%」做成自動告警。
- ✅ **Linux／Omarchy 版已建立**：驅動 615.78.08 ＋ 兩個 venv（cu132 stable／cu134 nightly），
  `audit_venv.py` 的 22 項審計兩邊皆 PASS（見 §十）。
- ✅ **Linux 版已開源並接上排程**：`scripts/linux/` 收進 `ai-stack-update-check`，
  systemd user timer（每日 23:00、`Persistent=true`）＋ `notify-send` 桌面通知已實測跑通。
- ✅ **上游坑已根治**：ComfyUI 落後的 263 個 commit 補齊，上游移除 torchaudio 的改動落地。
- 還沒做：**Python 3.15 遷移**（cu132／cu134 已有 cp315 wheel，建議排在 wheel 升級之後）。

