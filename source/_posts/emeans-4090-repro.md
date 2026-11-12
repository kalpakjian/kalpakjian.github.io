---
title: e-means 重現：RTX 4090 上 1.4 輪追上 25 輪，以及那個 45 倍的條件
date: 2026-11-12 20:00:00
categories:
  - AI 研究札記
tags:
  - e-means
  - FAISS
  - k-means
  - RTX 4090
  - 重現實驗
  - 效能基準
index_img: /img/covers/emeans-4090-repro.png
banner_img: /img/covers/emeans-4090-repro.png
---

## 一句話總結

Meta FAIR 的 e-means（FAISS 1.16 起內建的 `faiss.contrib.e_means`）可以在 24 GB 的 RTX 4090 上完整重現：70 個（資料集, 種子）組合全部在 <strong>1.4–2.8 輪</strong>追上 Flash-KMeans 跑 25 次迭代的誤差，wall-clock 加速 <strong>10.3–46.9 倍</strong>（七個資料集/規模的中位數 13.8–42.2 倍）。

但那句「最高 45 倍」有前提：它是 Meta 自報、分母是 <strong>H100 上的 Flash-KMeans 0.3.1</strong>、而且是端到端 wall-clock。「e-means 對任何 k-means 都快 45 倍」不是這篇的意思，也不是我量到的。

## 1. e-means 在做什麼

Lloyd k-means 每一輪都要把全部資料重新指派到最近的中心，再依全部指派重算質心；資料一大，完整掃描就是瓶頸。e-means 改成 mini-batch：每批只取少量向量，用指數移動平均（EMA）把「群集收到的向量總和」與「樣本數」混進舊統計量，質心就是兩者相除。

<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 440" role="img" aria-label="圖 1：七個資料集與規模的中位數 wall-clock 加速倍率，虛線帶是論文宣稱的 10 到 45 倍" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="958.5" height="438.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="48" font-size="24" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">中位數加速倍率：七格全部落在論文宣稱的 10–45 倍帶內</text>
<text x="48" y="76" font-size="14" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">RTX 4090、Triton backend、每格 10 個種子；分母是同一張卡上的 Flash-KMeans 0.3.1 跑 25 次迭代</text>
<rect x="378" y="104" width="448" height="284" fill="#2dd4bf14" stroke="#2dd4bf66" stroke-width="1.2" stroke-dasharray="5 4"/>
<text x="378" y="98" font-size="12.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">論文宣稱 10–45×</text>
<line x1="250" y1="388" x2="250" y2="112" stroke="#222b36" stroke-width="1.5"/>
<line x1="250" y1="388" x2="890" y2="388" stroke="#222b36" stroke-width="1.5"/>
<line x1="378" y1="388" x2="378" y2="384" stroke="#30363d" stroke-width="1"/>
<text x="378" y="406" font-size="12" fill="#6e7681" text-anchor="middle" font-family="'Segoe UI',sans-serif">10</text>
<line x1="506" y1="388" x2="506" y2="384" stroke="#30363d" stroke-width="1"/>
<text x="506" y="406" font-size="12" fill="#6e7681" text-anchor="middle" font-family="'Segoe UI',sans-serif">20</text>
<line x1="634" y1="388" x2="634" y2="384" stroke="#30363d" stroke-width="1"/>
<text x="634" y="406" font-size="12" fill="#6e7681" text-anchor="middle" font-family="'Segoe UI',sans-serif">30</text>
<line x1="762" y1="388" x2="762" y2="384" stroke="#30363d" stroke-width="1"/>
<text x="762" y="406" font-size="12" fill="#6e7681" text-anchor="middle" font-family="'Segoe UI',sans-serif">40</text>
<line x1="890" y1="388" x2="890" y2="384" stroke="#30363d" stroke-width="1"/>
<text x="890" y="406" font-size="12" fill="#6e7681" text-anchor="middle" font-family="'Segoe UI',sans-serif">50×</text>
<text x="240" y="135" font-size="13.5" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI',sans-serif">deep1b-1M</text>
<rect x="250" y="121" width="177.9" height="18" rx="4" fill="#2dd4bf" opacity="0.85"/>
<text x="435.9" y="135" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI',sans-serif">13.9×</text>
<text x="240" y="175" font-size="13.5" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI',sans-serif">dino10b-1M</text>
<rect x="250" y="161" width="540.2" height="18" rx="4" fill="#fbbf24" opacity="0.9"/>
<text x="798.2" y="175" font-size="12.5" fill="#0d1117" font-weight="700" font-family="'Segoe UI',sans-serif">42.2×</text>
<text x="240" y="215" font-size="13.5" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI',sans-serif">spacev-1M</text>
<rect x="250" y="201" width="252.2" height="18" rx="4" fill="#2dd4bf" opacity="0.85"/>
<text x="510.2" y="215" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI',sans-serif">19.7×</text>
<text x="240" y="255" font-size="13.5" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI',sans-serif">fb-ssnpp-1M</text>
<rect x="250" y="241" width="304.6" height="18" rx="4" fill="#2dd4bf" opacity="0.85"/>
<text x="562.6" y="255" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI',sans-serif">23.8×</text>
<text x="240" y="295" font-size="13.5" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI',sans-serif">deep1b-10M</text>
## 2. 我怎麼跑（以及為什麼要改兩行）
官方提供了重現腳本 `benchs/e_means/paper_bench.py`，計時協定相當嚴格：每次 run 開一個新 process、
未計時的 warm-up、兩個方法在同一個 job 同一張卡、同一個 float64 scorer。我沒有重寫 benchmark，
而是直接用官方腳本——只改了一個地方。
問題是官方腳本<strong>兩處把 assignment backend 寫死成 CuTe</strong>（`paper_xb.run_emeans` 與
`paper_bench.fig3_emeans`）。CuTe kernel 只針對 SM90（H100／H200）調校，4090 是 SM89，
第一次 assignment 就會失敗。把那一行改成讀環境變數 `XB_BACKEND`（預設 `auto`）之後，
H100 上仍解析成 CuTe、4090 上解析成 Triton，其餘協定一行沒動。
| 項目 | 設定 |
|---|---|
| 顯卡 | RTX 4090（SM89, 24 GB） |
| e-means backend | Triton（`assignment_backend=auto` 在 SM89 上解析的結果） |
| baseline | Flash-KMeans 0.3.1（論文指定的版本，寫死不容替換） |
| 群集數 k | 1M 用 16384、10M 用 65536（論文的 `k_for`，不是手寫 benchmark 常見的 1024／4096） |
| 環境 | torch 2.15.0+cu132、triton 3.9.0、faiss-cpu 1.16.0、Python 3.14 |
| 資料 | 官方 1M 前綴 4.5 GB ＋ 10M 前綴 21.7 GB，逐檔 fingerprint 校驗 |
## 3. 結果
| 資料集 | 種子 | 追上 25 輪所需輪數（中位） | 範圍 | 中位加速 |
|---|---|---|---|---|
| deep1b-1M | 10/10 | 1.8 | 1.6–2.2 | 13.9× |
| dino10b-1M | 10/10 | 2.0 | 1.8–2.2 | 42.2× |
| spacev-1M | 10/10 | 2.2 | 2.0–2.6 | 19.7× |
| fb-ssnpp-1M | 10/10 | 1.4 | 1.4 | 23.8× |
| deep1b-10M | 10/10 | 2.2 | 1.4–2.8 | 13.8× |
| spacev-10M | 10/10 | 2.2 | 2.0–2.4 | 21.8× |
| fb-ssnpp-10M | 10/10 | 1.6 | 1.4–1.8 | 23.5× |
70 個種子全部 cross。逐種子極值：輪數 1.4–2.8、加速 10.28–46.85 倍。
## 4. 那個「45 倍」要加的條件
三件事會讓這個數字被誤讀，我把它們一起寫進了 repo 的分析檔：
1. <strong>分母是特定的 baseline</strong>：Flash-KMeans 0.3.1、H100、端到端 wall-clock。同一張 4090 上，七個資料集的中位倍率就從 13.8 倍到 42.2 倍，差三倍。
2. <strong>1.4–2.6 輪是「追平 25 輪所需的輪數」，不是固定預算。</strong> 70 個種子裡有一個到 2.8 輪；而且規模一變小，結論會反轉。
3. <strong>論文是 preprint、數據由作者自報</strong>，沒有同儕審查，也不是對 k-means 生態的橫向評比。
小規模會反轉，這點我在同一台機器上量過（CPU、`NumpyEmeans` 對上 `faiss.Kmeans`、都不做 subsample）：
| n | d | k | e-means | Lloyd | 誰好 |
|---|---|---|---|---|---|
| 50k | 64 | 256 | 2 輪 → loss 132.07（0.13 s） | 25 輪 → 125.58（0.44 s） | Lloyd 較好 |
| 500k | 96 | 256 | 2 輪 → loss 127.29（1.36 s） | 25 輪 → 128.00（5.83 s） | e-means 較好，時間少 4.3 倍 |
第一列就是反例：群集數不多、資料分離良好時，Lloyd 幾乎一步到位，e-means 的 EMA 反而落後。
所以比較誠實的說法是：<strong>在大規模 embedding 分群上，e-means 有機會用約十分之一的輪數達到
25 輪 Lloyd 的品質，並在適合的 GPU 負載上帶來 10–45 倍加速。</strong>
<rect x="250" y="281" width="176.6" height="18" rx="4" fill="#2dd4bf" opacity="0.85"/>
<text x="434.6" y="295" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI',sans-serif">13.8×</text>
<text x="240" y="335" font-size="13.5" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI',sans-serif">spacev-10M</text>
<rect x="250" y="321" width="279" height="18" rx="4" fill="#2dd4bf" opacity="0.85"/>
<text x="537" y="335" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI',sans-serif">21.8×</text>
<text x="240" y="375" font-size="13.5" fill="#c9d1d9" text-anchor="end" font-family="'Segoe UI',sans-serif">fb-ssnpp-10M</text>
<rect x="250" y="361" width="300.8" height="18" rx="4" fill="#2dd4bf" opacity="0.85"/>
<text x="558.8" y="375" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI',sans-serif">23.5×</text>
<text x="48" y="428" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">DINOv3 1M 那格最高（42.2×），但同一張卡上 DEEP* 只有 13.9×——倍率是資料集與硬體共同決定的量。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：七個資料集／規模的中位數加速倍率（各 10 個種子）。灰綠色虛線帶是論文宣稱的 10–45 倍；七格全在帶內，但帶內分佈很寬，DINOv3 1M 幾乎頂到上限。</figcaption>
</figure>

## 5. 我查證到的三件事（比倍率更有用）

1. <strong>二手整理的兩個數字是錯的。</strong>「DINO10B＝10 億筆、約 105 萬群集」——官方是 100 億筆、1024 維、k 約 1670 萬（`--n 10_000_000_000 --k $((1<<24))`）。另一個「779 GPU-hours、32 台機器」與官方重現指令差約 35 倍：README 的 10B 指令是 `--launch 8`、實測 9762.65 秒（3 輪），約 22 GPU-hours。
2. <strong>baseline 不是 bit-exact，也不需要是。</strong>我們的 Flash-KMeans@25 test error 與論文在 H100 上的每個種子值差 1e-4 到 4e-3（相對）——FP16 累加順序、Triton 在 SM89 的 tile 選擇、torch 版本都不同。反過來，Faiss CPU 那一臂是可重現的（差 1.2e-4 到 1.4e-4），所以驗證資料切分與 k 要用 CPU 臂。
3. <strong>倍率是硬體相依量。</strong>Flash-KMeans@25 在 4090 上比 H100 慢 2.4 倍（DEEP* 1M）到 14 倍（DINOv3 1M，1024 維）。分子與分母不是同一個比例退化，所以這張卡上的倍率比論文高一些，不代表 e-means 在 H100 上也有同樣的倍率。

## 6. 實務結論

- 值得用：資料量大、群集數多、完整 Lloyd 掃描很貴（向量檢索、去重、RAG 索引）。
- 不必用：數十萬筆、群集數少、或資料本身分離良好——Lloyd 本來就快，收益會消失甚至反轉。
- 要引用 45 倍，請連「H100 ＋ Flash-KMeans 0.3.1」一起寫，否則那個數字沒有意義。
- 想自己重跑：1M 全表（4 資料集 × 10 種子）在 4090 上實測約 15 分鐘；真正的成本在 Faiss CPU 的Figure 3（每個面板每個種子約 7 分鐘）。repo 內含 preflight、patch、報告產生器與完整原始 JSON。

## 7. 來源與查證

| 項目 | 網址 | 實查結果 |
|---|---|---|
| 論文 | [arXiv:2611.09501](https://arxiv.org/abs/2611.09501) | 2026-11-06 投稿；摘要寫「1.4 to 2.6 epochs」「10-45x」 |
| 專案頁 | [e-means.github.io](https://e-means.github.io/) | 互動 demo；更新公式與我讀到的程式碼一致 |
| 官方重現腳本 | [faiss/benchs/e_means](https://github.com/facebookresearch/faiss/tree/v1.16.0/benchs/e_means) | v1.16.0（2026-11-10）已含 `faiss.contrib.e_means` |
| 我的重現 repo | [emeans-4090-repro](https://github.com/kalpakjian/emeans-4090-repro) | 456 筆 run 記錄、70 筆 crossing 記錄都在 `results/` |
| 分析檔 | [ANALYSIS.md](https://github.com/kalpakjian/emeans-4090-repro/blob/main/ANALYSIS.md) | 條件、baseline 忠實度、兩個錯誤二手數字 |

> <strong>查證說明</strong>：本文所有倍率於 2026-11-12 在本機 RTX 4090 實跑，原始 JSON 在 repo 的 `results/`；<br /> > 論文的絕對秒數沒有重現（需要 H100 ＋ CuTe），`dino10b-10M`（光 bf16 就 20.5 GB）與 100M 規模也未跑，標為未驗證。<br /> > <strong>封面與圖表</strong>：封面由本機 ComfyUI 的 Qwen-Image 2.1 生成（刻意不含文字）；圖 1 為手繪內嵌 SVG，數字取自實跑結果。
