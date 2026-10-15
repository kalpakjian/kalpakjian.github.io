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
toc: true
index_img: /img/covers/pytorch-2141-cu132-onnx-trt-upgrade.png
banner_img: /img/covers/pytorch-2141-cu132-onnx-trt-upgrade.png
---

> <strong>一句話結論</strong>：可以，<code>torch 2.14.1+cu132</code> 不是障礙，但舊的 <code>.engine</code> 不能直接沿用——換 CUDA 版本必須重編一次，編完速度回到 <code>ck_trt -51.6%</code> 同級甚至更好。
> 本篇整理自 <a href="https://github.com/kalpakjian/minimax-h3-comfyui">kalpakjian/minimax-h3-comfyui</a> 的實測（RTX 4090 24GB、ComfyUI 0.34.0 portable）。

<!-- more -->

## 背景：這個 repo 在做什麼

`minimax-h3-comfyui` 是把 **MiniMax H3（海螺）視頻生成模型**完整跑在 ComfyUI portable 環境下的一套生產配置，含角色置換 LoRA、Turbo 低步數加速、TRT-VAE 加速與原生音頻生成。模型權重（`*.safetensors`、`*.onnx`、`*.engine`）全部 gitignore，本 repo 只收工作流 / 腳本 / 文檔。

關鍵環境（升級前）：

| 項目 | 數值 |
| --- | --- |
| GPU | NVIDIA GeForce RTX 4090 24GB |
| ComfyUI | 0.34.0（portable，`D:\AI\ComfyUI`） |
| 啟動環境 | `python_embeded_nightly\`（nightly 分支，與原 `python_embeded\` 分離，可回退） |
| torch（舊） | 2.15.0.dev20260903+cu130（CUDA 13.0 nightly） |
| torch（新） | **2.14.1+cu132**（CUDA 13.2） |
| 注意力加速 | `--use-ck-attention` |
| VAE 加速 | TRT（TensorRT 11.2，ONNX → engine 預編譯） |

## 核心問題：2.14.1+cu132 能不能沿用 ONNX→TRT？

答案：**可以，但要重編 engine**。`TRT_VAE_安裝報告.md` 第六節第 1 點早就寫死：

> engine 是平台專屬：換 GPU（型號/架構）、改 CUDA 版本都要重新編譯，舊 engine 不能跨機移動。

你現在正是這個情況：舊 engine 是 `cu130 + TRT 11.2.1.2` 編出來的（decoder 約 4.6GB），新環境是 CUDA 13.2。

為什麼可以沿用？三個理由：

1. **ONNX→TRT 跟 torch wheel 版本脫鉤**。torch 只負責 DiT，VAE 解碼走的是 `MiniMaxH3TRTVAELoader` 載入的 `.engine`。
2. **TRT 11.x 就是為 CUDA 13.x 出的**。新環境 `pip install --prefer-binary tensorrt` 一樣抓到 `tensorrt_cu13` 系列，CUDA 13.2 屬 13.x 家族，只要 driver 夠新（CUDA 13.x 要 R580+）就能編。
3. **PyTorch 2.14 / 2.15 沒 breaking 到 `ComfyUI-H3VAE_TRT` 那顆 node**。

## 做法：把安裝報告 Step 2~5 重跑一次

```powershell
# 0. 先確認 driver（CUDA 13.x 要 R580+）
nvidia-smi

# 1. ONNX 檔留著，不要刪！特別是 4.8GB 那顆
# ComfyUI\models\vae\
#   minimax_h3_vae_decoder.onnx      (1.6MB)
#   minimax_h3_vae_decoder.onnx.data (4.8GB)  <- 刪了就不能重編
#   minimax_h3_vae_encoder.onnx      (361MB)
# 缺檔的話重跑 scripts\_dl_onnx.ps1
# 來源：https://huggingface.co/lihaoyun6/MiniMax-H3-VAE-ONNX

# 2. 在 2.14.1+cu132 的 python_embeded 裝 TRT
python_embeded\python.exe -m pip install --prefer-binary tensorrt
python_embeded\python.exe -c "import tensorrt as trt; print(trt.__version__)"
# 預期 11.x（舊環境實錄：11.2.1.2，含 tensorrt_cu13 系列）

# 3. 重編 engine（一次性，會吃大量 VRAM，4090 上 decoder 編了幾分鐘）
$env:COMFY_HOST="http://127.0.0.1:8188"
python_embeded\python.exe scripts\_trt_compile.py
# 產生新的 minimax_h3_vae_decoder.engine / encoder.engine，覆蓋舊的
# 記得 delete_onnx_after_compile=False，保留 ONNX 以便日後再重編
```

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

## 實測數據回顧（同條件：864×480、73 格、4 步、seed 731159）

| # | 配置 | torch | 耗時 | 對比 baseline |
| --- | --- | --- | --- | --- |
| 1 | baseline（原環境） | 2.7.1+cu126 | 1260.6 s | — |
| 2 | \+ `--use-ck-attention` | 2.7.1+cu126 | 1090.5 s | -13.5% |
| 3 | **\+ TRT-VAE** | 2.7.1+cu126 | **610.4 s** | **-51.6%** |
| 4 | 全套（nightly + cu130） | 2.15.0.dev | **40.0 s** | **-96.8%** |

解讀：TRT-VAE 單獨已把整片砍半（解碼段被大幅壓縮）；再疊 nightly torch + CK-Attention 進入 40s 等級。cu132 重編後預期回到第 3 級以上。

## 兩個坑（必讀）

1. **先隔離再升級**：學 repo 原做法，用 `_copy_env.ps1` 把 `python_embeded\` robocopy 成 `python_embeded_nightly\` 再搞，2.14.1 搞壞還能回退到 2.7.1。
2. **首次編譯吃資源**：decoder engine 約 4.6GB，編譯時接近 OOM，要關掉其他佔 VRAM 的東西，留 6~8GB 空間。`.onnx.data` 絕對不能刪。

其他已知限制：TRT 目前只加速解碼（`encoder=None`）；要連編碼一起加速需另把 encoder 掛上；同 seed 下 TRT 版與 safetensors 版輸出約 PSNR 17–22dB，目視場景一致。

## 相關連結

- Repo：<a href="https://github.com/kalpakjian/minimax-h3-comfyui">kalpakjian/minimax-h3-comfyui</a>
- ONNX 來源：<a href="https://huggingface.co/lihaoyun6/MiniMax-H3-VAE-ONNX">lihaoyun6/MiniMax-H3-VAE-ONNX</a>
- 腳本：`scripts/_dl_onnx.ps1`、`_pip_torch_nightly.ps1`、`_pip_trt_nightly.ps1`、`_trt_compile.py`、`bench_h3_trt.py`
- 文檔：`TRT_VAE_安裝報告.md`、`H3_TURBO_SETUP.md`

---

*本篇為實測紀錄整理，環境：RTX 4090 24GB｜ComfyUI 0.34.0｜torch 2.14.1+cu132 升級路徑。*
