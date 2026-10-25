---
title: PyTorch 2.14.1+cu132 還能用 ONNX 預編譯加速嗎？MiniMax H3 × ComfyUI TRT-VAE 升級報告
date: 2026-10-15 22:00:00
categories:
  - AI 研究追蹤
tags:
  - ComfyUI
  - MiniMax-H3
  - ONNX
  - TensorRT
  - PyTorch
  - nightly
  - 效能實測
  - Linux
  - Omarchy
  - cuDNN
toc: true
index_img: /img/covers/pytorch-2141-cu132-onnx-trt-upgrade.png
banner_img: /img/covers/pytorch-2141-cu132-onnx-trt-upgrade.png
---

> <strong>一句話結論（2026-10-16 實測更新）</strong>：可以，<code>torch 2.14.1+cu132</code> 不是障礙；而且<strong>舊 engine 其實仍能載入</strong>（TRT 版本、GPU 架構、driver 都沒變），重編只是「便宜的保險」——在 cu132 重編一次只要 <strong>76.8 s</strong>，編完與舊 engine <strong>同速</strong>（warm 12.45 s vs 12.3 s）。
> ⚠️ 原文預期的「回到 <code>ck_trt −51.6%</code> 同級」屬 <strong>torch 2.7.1 舊世代</strong>的數字；cu132 + nightly 世代同條件已到 <strong>12–13 s</strong>，TRT 的相對收益同步收斂到個位數 %。
> 本篇整理自 <a href="https://github.com/kalpakjian/minimax-h3-comfyui">kalpakjian/minimax-h3-comfyui</a> 的實測（RTX 4090 24GB、ComfyUI portable）。
>
> <strong>2026-10-26 補充</strong>：同一套 wheel 搬到 <strong>Linux／Omarchy</strong> 上改用兩個 venv 安裝
> （cu132 stable／cu134 nightly），並量到一個反直覺的結論——
> <strong>效能提升來自驅動更新，不是 wheel 升級</strong>。詳見下文〈在 Linux（Omarchy）上的對應安裝〉。

<!-- more -->

> <strong>更新紀錄</strong>：2026-10-15 初版（升級路徑推演）；2026-10-16 補實測——舊 engine 相容性、cu132 重編（76.8 s）、864×480 與生產量級（1344×768／243 格／6 步）跑分，並修正初版「必須重編」與「−51.6%」兩處說法；2026-10-26 補 **Linux／Omarchy 對應安裝**——同一張卡的兩個 venv（cu132 stable／cu134 nightly）、cuDNN 三路驗證，以及「變快的是驅動、不是 wheel」的實測結論。

## 背景：這個 repo 在做什麼

`minimax-h3-comfyui` 是把 **MiniMax H3（海螺）視頻生成模型**完整跑在 ComfyUI portable 環境下的一套生產配置，含角色置換 LoRA、Turbo 低步數加速、TRT-VAE 加速與原生音頻生成。模型權重（`*.safetensors`、`*.onnx`、`*.engine`）全部 gitignore，本 repo 只收工作流 / 腳本 / 文檔。

關鍵環境（2026-10-16 實測時的狀態；「升級前」列為初版撰寫時的舊值）：

| 項目 | 數值 |
| --- | --- |
| GPU | NVIDIA GeForce RTX 4090 24GB（driver 617.42） |
| ComfyUI | **0.37.0**（portable，`D:\AI\ComfyUI`；初版撰寫時為 0.34.0） |
| 啟動環境 | `python_embeded_nightly\`（nightly 分支，與原 `python_embeded\` 分離，可回退） |
| torch（生產） | **2.16.0.dev20261007+cu132**（CUDA 13.2 nightly，2026-10-08 起為正式生產環境） |
| torch（備援） | 2.14.1+cu132（stable） |
| torch（升級前） | 2.15.0.dev20260903+cu130（CUDA 13.0 nightly） |
| 注意力加速 | `--use-ck-attention` |
| VAE 加速 | TRT **11.2.1.2**（ONNX → engine 預編譯；engine 2026-10-16 於 cu132 重編） |

> ⚠️ 這張表是 **Windows 便攜版**（`D:\AI\ComfyUI`）的環境。同一張 RTX 4090 在 **Linux／Omarchy** 上
> 是另一套安裝（兩個 venv、兩個 cuDNN 版本），見下文〈在 Linux（Omarchy）上的對應安裝〉。

## 核心問題：2.14.1+cu132 能不能沿用 ONNX→TRT？

**答案分兩層（2026-10-16 實測）**：

1. **能不能用 ONNX→TRT？** 能。`MiniMaxH3TRTVAELoader` 在 cu132 下照常載入 `.engine` 出片，沒有 deserialize 失敗。
2. **舊 engine 能不能直接沿用？** **實測可以**——舊 engine（`cu130 + TRT 11.2.1.2` 編的，decoder 4,849,896,724 B）在 cu132 環境**仍可反序列化並跑通**，且與重編後**同速**（warm median 12.3 s vs 12.45 s）。

`TRT_VAE_安裝報告.md` 第六節第 1 點寫的是保守規則：

> engine 是平台專屬：換 GPU（型號/架構）、改 CUDA 版本都要重新編譯，舊 engine 不能跨機移動。

實測補充：engine 真正綁定的是 **TRT 版本 + GPU 架構（sm_89）+ driver**。這次 TRT 仍是 11.2.1.2、GPU/driver 未動，CUDA 13.0→13.2 只是同家族小版本，所以舊 engine 沒有失效。

為什麼可以沿用？三個理由：

1. **ONNX→TRT 跟 torch wheel 版本脫鉤**。torch 只負責 DiT，VAE 解碼走的是 `MiniMaxH3TRTVAELoader` 載入的 `.engine`。
2. **TRT 11.x 就是為 CUDA 13.x 出的**。`pip install --prefer-binary tensorrt` 一樣抓到 `tensorrt_cu13` 系列，CUDA 13.2 屬 13.x 家族，只要 driver 夠新（CUDA 13.x 要 R580+；本機 617.42）就能編。
3. **PyTorch 2.14 / 2.15 / 2.16 沒 breaking 到 `ComfyUI-H3VAE_TRT` 那顆 node**。

> 那還要不要重編？**建議重編**：只要 **76.8 s**，可確保 engine 與當前 TRT/driver 完全對齊，避免日後 TRT 或 driver 更新時才踩雷。

## 做法：把安裝報告 Step 2~5 重跑一次（2026-10-16 實際執行版）

```powershell
# 0. 先確認 driver（CUDA 13.x 要 R580+；本機 617.42）
nvidia-smi

# 1. ONNX 檔留著，不要刪！特別是 4.8GB 那顆
# ComfyUI\models\vae\
#   minimax_h3_vae_decoder.onnx      (1.6MB)
#   minimax_h3_vae_decoder.onnx.data (4.8GB)  <- 刪了就不能重編
#   minimax_h3_vae_encoder.onnx      (361MB)
# 缺檔的話重跑 scripts\_dl_onnx.ps1
# 來源：https://huggingface.co/lihaoyun6/MiniMax-H3-VAE-ONNX

# 2. 裝 TRT（本次實測：兩個環境都已是 11.2.1.2，無需重裝）
python_embeded\python.exe -m pip install --prefer-binary tensorrt
python_embeded\python.exe -c "import tensorrt as trt; print(trt.__version__)"   # -> 11.2.1.2

# 2.5 先備份舊 engine，再卸載模型騰 VRAM（本次實測 22.1 GB -> 1.9 GB，避免編譯 OOM）
#     註：C:\minimax+comfyUI 舊安裝已退役，實際路徑為 D:\AI\ComfyUI
Copy-Item models\vae\minimax_h3_vae_decoder.engine,models\vae\minimax_h3_vae_encoder.engine `
          models\vae\_engine_bak_cu130_20260904\ -Force
Invoke-WebRequest http://127.0.0.1:8188/free -Method POST `
  -Body '{"unload_models":true,"free_memory":true}' -ContentType 'application/json'

# 3. 重編 engine（一次性；本次實測 76.8 s 完成 decoder + encoder）
$env:COMFY_HOST="http://127.0.0.1:8188"
python_embeded\python.exe scripts\_trt_compile.py
# 產生新的 minimax_h3_vae_decoder.engine / encoder.engine，覆蓋舊的
# 記得 delete_onnx_after_compile=False，保留 ONNX 以便日後再重編
```

本次編譯結果（`TRT_VAE_安裝報告.md` 第八節）：

| engine | 舊（2026-09-04, cu130） | 新（2026-10-16, cu132） |
| --- | --- | --- |
| minimax_h3_vae_decoder.engine | 4,849,896,724 B | 4,849,917,284 B |
| minimax_h3_vae_encoder.engine | 362,517,876 B | 362,597,804 B |

`_trt_compile.py` 本質是往 ComfyUI API 丟一個一次性 job：

```json
MiniMaxH3TRTCompilerNode {
  "decoder_onnx": "minimax_h3_vae_decoder.onnx",
  "encoder_onnx": "minimax_h3_vae_encoder.onnx",
  "delete_onnx_after_compile": false
}
```

編完 workflow 不用改，照舊：

- VAE 節點用 `MiniMaxH3TRTVAELoader(decoder=.engine, encoder=None)`（目前只加速解碼）
- 啟動加 `--use-ck-attention`

```powershell
D:\AI\ComfyUI\python_embeded_nightly\python.exe D:\AI\ComfyUI\main.py --listen 127.0.0.1 --port 8188 --use-ck-attention
```

## 實測數據（一）舊世代回顧（2026-09-04；864×480、73 格、4 步、seed 731159）

| # | 配置 | torch | 耗時 | 對比 baseline |
| --- | --- | --- | --- | --- |
| 1 | baseline（原環境） | 2.7.1+cu126 | 1260.6 s | — |
| 2 | \+ `--use-ck-attention` | 2.7.1+cu126 | 1090.5 s | -13.5% |
| 3 | **\+ TRT-VAE** | 2.7.1+cu126 | **610.4 s** | **-51.6%** |
| 4 | 全套（nightly + cu130） | 2.15.0.dev | **40.0 s** | **-96.8%** |

解讀：TRT-VAE 單獨已把整片砍半（解碼段被大幅壓縮）；再疊 nightly torch + CK-Attention 進入 40s 等級。
⚠️ 這張表的 **−51.6%** 是「慢路徑（torch 2.7.1）下解碼占比極高」造成的，**不能直接外推到 cu132 世代**。

## 實測數據（二）cu132 世代（2026-10-16 實測）

**量測方式**：`bench_h3_trt.py`（TRT-VAE）/ `bench_h3_fine.py`（fp16 VAE）/ `bench_h3_prod.py`（生產量級）。
本日起腳本除 `elapsed`（client 端，含排隊與輪詢）外，另記 **`exec`＝server 端 `execution_start`→`execution_success`**（無排隊/輪詢誤差）與 server 的 `pytorch_version`；**每輪換 seed**（否則 ComfyUI 會重用執行快取，測到的是快取值）。

**A. 864×480、73 格、4 步（warm）**

| 配置 | torch | exec（median） | n |
| --- | --- | --- | --- |
| **TRT-VAE（新 cu132 engine）** | 2.16.0.dev20261007+cu132 | **12.45 s**（12.2–12.7） | 4 |
| TRT-VAE（舊 cu130 engine，未重編） | 同上 | 12.3 s（12.1–12.7） | 3 |
| fp16 VAE（無 TRT） | 同上 | 15.75 s（12.9–20.2） | 6 |
| 冷啟動參考（含模型載入） | 同上 | 29.1 s | 1 |

**B. 生產量級：1344×768、243 格、6 步、Turbo v4（warm）**

| 配置 | torch | exec | n |
| --- | --- | --- | --- |
| **TRT-VAE（新 cu132 engine）** | 2.16.0.dev20261007+cu132 | **199.5 s** | 1 |
| fp16 VAE（無 TRT） | 同上 | 200.9 s | 1 |

解讀：

- **cu132 世代整體已很快**：864×480 這級從舊世代的 40 s（cold）再降到 **~12.5 s（warm）/ 29 s（cold）**；生產量級（1344×768／243 格／6 步）**199.5 s**，與 repo 記錄的 ~215 s／10 秒段落同級。
- **生產量級 TRT 與 fp16 幾乎同速**（199.5 s vs 200.9 s，差 0.7%）：243 格／1344×768 的主成本是 DiT 取樣，解碼只佔小段。此時 TRT 的價值是**顯存與路徑穩定**（engine 4.85 GB < fp16 VAE 5.21 GB、解碼不隨 torch 版本變動），不是省時間。
- **小量級 TRT 的相對收益也收斂**：864×480 median 12.45 s vs 15.75 s（−21%）；貼身 interleaved 對照（同一分鐘、只換 VAE 節點）為 12.2 s vs 12.9 s（−5%）。原因同上：解碼已不是瓶頸。
- **仍值得開 TRT**：engine 4.85 GB < fp16 VAE 5.21 GB，24 GB 卡更省顯存；且解碼路徑與 torch 版本脫鉤（換 cu132 照跑就是證明）；生產長片跑起來 VRAM 峰值約 23.5/24.5 GB。
- **離散偏大**：19–20 s 的樣本在 TRT / fp16 兩邊都出現（含一次 TRT 19.2 s），來源是 24 GB 顯存下 DiT / CLIP / VAE 的換入換出，不是 VAE 路徑本身——比較請看 median 並用 interleaved 對照。

## 四個坑（必讀，2026-10-16 更新）

1. **先隔離再升級**：學 repo 原做法，用 `_copy_env.ps1` 把 `python_embeded\` robocopy 成 `python_embeded_nightly\` 再搞；搞壞還能回退（原環境現為 torch 2.14.1+cu132）。
2. **重編前先備份 + 騰 VRAM**：`Copy-Item` 舊 engine 到 `_engine_bak_cu130_20260904\`，再 `POST /free` 卸載模型（實測 22.1 GB → 1.9 GB）。本次 76.8 s 編完、沒有接近 OOM；但生產長片（1344×768、243 格）跑起來 VRAM 會到 23.5/24.5 GB，編譯前務必清乾淨。
3. **`.onnx.data` 絕對不能刪**：decoder 權重 4.8 GB 在其中，刪了就不能重編。
4. **跑分要換 seed**：ComfyUI 會重用上游節點快取（同 seed 重跑會秒回、測到的是快取值）；每輪換 seed，並以 **server 端 `exec`** 為準（`bench_h3_*.py` 已內建輸出 `elapsed` / `exec` / `pytorch_version`）。

其他已知限制：TRT 目前只加速解碼（`encoder=None`）；要連編碼一起加速需另把 encoder 掛上；同 seed 下 TRT 版與 safetensors 版輸出約 PSNR 17–22dB，目視場景一致。

## 在 Linux（Omarchy）上的對應安裝：兩個 venv、兩個 cuDNN

前面整套流程是 **Windows 便攜版**（`D:\AI\ComfyUI` ＋ `python_embeded`）。同一張 RTX 4090
在 Linux／Omarchy 上是**另一套安裝**，而且最後的效能結論有點反直覺。

### 環境

| 項目 | 數值 |
|---|---|
| OS | Omarchy（Arch-based），核心 `7.2.8-9-omarchy` |
| 驅動 | `nvidia-open-dkms` **615.78.08-1**（CUDA UMD **13.4**） |
| Python | 3.12.14（兩個 venv） |
| **stable** | `~/Projects/ComfyUI/.venv`：torch **2.14.1+cu132**、cuDNN **9.24.0.43**、NCCL 2.30.7、triton 3.8.0（6.8 G） |
| **nightly** | `~/Projects/ComfyUI/.venv-nightly`：torch **2.16.0.dev20261025+cu134**、cuDNN **9.26.0.51**、NCCL 2.32.3、triton 3.9.0（12 G） |
| TensorRT | nightly 另含 `tensorrt`／`tensorrt_libs` **11.3.0.99**（cu13 版，選用） |

**為什麼分兩個 venv？** nightly 是 dev 版，本來就會壞。跟 stable 混在同一個環境，
一壞就是整天不能用；分開之後 stable 永遠是已知可用的版本，
nightly 壞掉只影響「試新功能」這件事。

> nightly 多出來的 4.4 G 就是 `tensorrt_libs`——它是**選用**加速路徑，
> `comfy_kitchen` 與 torch 都不宣告依賴它，沒有也不影響一般推理。

### 兩個 Linux 特有的坑

1. **cu12 與 cu13 的 wheel 裝到同一個路徑。**
   `nvidia-*-cu12-*` 與 `nvidia-*-cu13-*` 的 `libnccl.so.2`／`libcudnn.so.9`
   路徑**完全重疊**，後裝者直接覆蓋先裝者——cu12 版蓋掉 cu13 版時症狀是
   `libtorch_cuda.so: undefined symbol: ncclCommResume`，**torch 連 import 都失敗**。
   清掉 **15 個**孤兒 `nvidia_*_cu12-*` dist-info 與 **352 個** cu12 專屬檔案後，套件數 145 → 130。
   更陰險的是：孤兒 dist-info 會讓 `importlib.metadata` 回報 **cuDNN 9.19.0.56**——
   **一個假的版本號，而且不報錯**。
2. **cu132 stable 索引沒有 torchaudio 的 cp312 x86_64 wheel**（248 個 wheel 裡 cp312 只有 aarch64）。
   `uv pip install --upgrade torchaudio` 會**什麼都不做**（uv 認為 `2.11.0+cu130` > `2.11.0`），
   torchaudio 留在 cu130、torch 已升到 cu132 → ComfyUI **一啟動就崩**：
   `RuntimeError: PyTorch has CUDA version 13.2 whereas TorchAudio has CUDA version 13.0`。
   解法是改從 `nightly/cu132` 索引撈 `torchaudio==2.11.0.dev20260902+cu132`，
   並加 `--index-strategy unsafe-best-match`（**同時必須釘住 torch／torchvision 版本**，
   否則會被 nightly 一起帶走）。

> **上游正解**：ComfyUI 的 `origin/master` 已改用自帶的 `comfy/audio.py`，
> `requirements.txt` 裡**完全移除 torchaudio**；本機 checkout 落後 263 個 commit，
> `git pull` 就能根治這個坑。

### cuDNN 要三路交叉驗證

Windows 那邊是「單獨載入 cudnn DLL 問版本會回報 9.26.0，但 torch 實際用 9.24.0」；
Linux 這邊更直接：**cuDNN 9 的 `.so` 裡沒有明文版本字串**，`strings` 只會挖到雜訊。
所以改用三個互相獨立的來源交叉比對：

| 來源 | stable | nightly |
|---|---|---|
| 套件 metadata（`importlib.metadata`） | 9.24.0.43 | 9.26.0.51 |
| **對磁碟上的 `libcudnn.so.9` 直接呼叫 `cudnnGetVersion()`（ctypes，完全不經 torch）** | 9.24.0 | 9.26.0 |
| `torch.backends.cudnn.version()` | 92400 → 9.24.0 | 92600 → 9.26.0 |

三者一致 ＋ `/proc/self/maps` 確認實際載入的是 **venv 內部**的
`nvidia/cudnn/lib/libcudnn_graph.so.9`（不是系統那份），才算通過。

> 唯一能證明「我用的是哪一份」的方式，是**對實際載入的那個檔案問**。

### 效能：真正變快的是驅動，不是 wheel

同一支 `bench_stack.py`（形狀由原始基準檔逆向擬合還原）、同一張卡、同一核心版本：

| 組態 | conv fp32 (ms) | conv fp16 (ms) | conv fp16 ＋ CL (ms) | SDPA (ms) |
|---|---|---|---|---|
| 升級前（cu130 ＋ drv610） | 1.603 | 1.044 | 0.809 | 0.058 |
| A：cu130 ＋ drv615 | **1.421** | **0.979** | **0.731** | 0.057 |
| B：cu132 ＋ drv615 | 1.416 | 0.980 | 0.731 | 0.057 |
| C：cu134 ＋ drv615 | **1.382** | **0.961** | 0.733 | 0.057 |

- **driver 610 → 615**：cuDNN conv fp16 **+6.2%**、channels_last **+9.6%**、fp32 conv **+11.4%**
- **wheel cu130 → cu132**：各項持平（±0.5% 內）

端到端（SD1.5、512×768、20 步、seed 42、中位數 ×3）：cu130 **3.05 s**／cu132 **3.04 s**／cu134 **3.01 s**。
三對組合的輸出逐像素比對，mean abs diff 皆 ≈ 0.32/255、差異 > 2 的像素 ≈ 1.7~1.8%，
幅度完全一致 → **差異純屬 cuDNN kernel 選擇的正常非確定性，演算法輸出沒變**。

> ⚠️ 這組數字**不可與上面 Windows 版的表格相減**：兩邊的基準腳本形狀不同
> （Linux 版的形狀是從原始基準檔逆向擬合出來的），只能各自跟自己的「升級前」比。

### 與 Windows 版的對照

| 面向 | Windows 便攜版 | Linux／Omarchy |
|---|---|---|
| 驅動更新 | NVIDIA 安裝程式 | `pacman` ＋ DKMS 重編核心模組，**升完必須重開機** |
| 環境 | `python_embeded\`（可整包複製） | venv（`uv pip` 管理） |
| 回滾 | `pip install --force-reinstall` | `uv pip install -r rollback/*.freeze.txt` |
| cuDNN 位置 | `torch\lib\cudnn*.dll` | `nvidia/cudnn/lib/libcudnn.so.9` |
| 版本驗證 | `--runtime` 官方 API | metadata ＋ ctypes `cudnnGetVersion()` ＋ torch runtime |
| 環境數 | 1 個（＋ nightly 副本） | 2 個 venv（stable／nightly），各自 22 項審計 |
| 驗證工具 | `check_stack.py` ＋ `bench_gpu.py` | `audit_venv.py` ＋ `verify_stack.sh` ＋ `bench_stack.py` |

> 一句話總結：**同一個「PyTorch 2.14.1＋cu132」的目標，在兩邊的安裝路徑、陷阱與驗證方法完全不同**；
> 能共用的是「先量基線、再升、升完一定要有可重複的完整性審計」這個流程。

## 相關連結

- Repo：<a href="https://github.com/kalpakjian/minimax-h3-comfyui">kalpakjian/minimax-h3-comfyui</a>
- ONNX 來源：<a href="https://huggingface.co/lihaoyun6/MiniMax-H3-VAE-ONNX">lihaoyun6/MiniMax-H3-VAE-ONNX</a>
- 腳本：`scripts/_dl_onnx.ps1`、`_copy_env.ps1`、`_pip_torch_nightly.ps1`、`_pip_trt_nightly.ps1`、`_trt_compile.py`、`bench_h3_trt.py`、`bench_h3_fine.py`、`bench_h3_prod.py`（生產量級 1344×768／243 格／6 步）
- 文檔：`TRT_VAE_安裝報告.md`（第八節＝本次 cu132 重編＋跑分全紀錄）、`H3_TURBO_SETUP.md`
- 同系列文章：<a href="/2026/10/21/ai-stack-auto-update-pipeline/">讓本機 AI 堆疊自己照顧自己（Windows ＋ Linux／Omarchy 雙環境）</a>
- Linux／Omarchy 版驗證腳本（本機 `~/Projects/ai-stack-check/`，尚未開源）：`audit_venv.py`（22 項完整性審計）、`verify_stack.sh`（含 `--full` 煙霧測試與 A/B/C 對照）、`bench_stack.py`、`cleanup_cu12_orphans.py`

---

*本篇為實測紀錄整理，環境：RTX 4090 24GB｜ComfyUI 0.37.0（初版 0.34.0）｜torch 2.14.1+cu132／2.16.0.dev20261007+cu132 升級路徑；2026-10-16 補 cu132 重編與跑分實測；2026-10-26 補 Linux／Omarchy 對應安裝（Omarchy、核心 7.2.8-9-omarchy、驅動 615.78.08、兩個 venv）。*
