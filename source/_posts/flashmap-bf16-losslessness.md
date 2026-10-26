---
title: FlashMap 推測解碼的「無損」為什麼驗不過？—— 8/12 不一致是 bf16 的浮點並列，換 fp32 就 12/12
date: 2026-10-26 09:30:00
categories:
  - AI
  - 技術筆記
tags:
  - FlashMap
  - 推測解碼
  - Speculative Decoding
  - vLLM
  - bfloat16
  - float32
  - 數值精度
  - PyTorch
  - transformers
  - Qwen3
  - GPU
  - 效能實測
  - 基準測試
toc: true
index_img: /img/covers/flashmap-bf16-losslessness.png
banner_img: /img/covers/flashmap-bf16-losslessness-banner.png
---

> <strong>整理說明</strong>：這是我在 RTX 4090 上重現 <a href="https://github.com/j-shen/FlashMap">FlashMap</a> 推測解碼時遇到的一個「看起來像 bug、其實不是 bug」的案例。第一輪實驗回報無損性檢查 <strong>8/12 不一致</strong>，差點讓我把它當成演算法缺陷記錄下來；追下去之後發現，問題全部出在 <code>bf16</code> 的浮點解析度，以及我自己量測腳本裡的三個錯誤。所有數字都來自本機實測，腳本與原始輸出放在 <a href="https://github.com/kalpakjian/flashmap-local-bench">kalpakjian/flashmap-local-bench</a> 的 <code>lab/</code>。

<!-- more -->

## 先講結論

**FlashMap 在 temperature=0 下是無損的。** 同一份程式、同一組題目、同一個 drafter，只改精度：

| 精度 | 無損性判定 | 逐 token 完全相同 | 平均接受長度 γ |
| --- | --- | ---: | ---: |
| `bfloat16` | **失敗** | **3 / 12** | 6.001 |
| `float32` | **通過** | **12 / 12** | 6.112 |

γ 幾乎沒變（6.001 → 6.112），也就是說<strong>加速效果與精度無關</strong>，只有「逐位元相同」這一項對精度敏感。這個形狀本身就很有提示性：壞掉的不是演算法，是量尺。

三句話總結原因：

1. 模型選下一個字，靠的是「比大小」。當兩個候選字的分數<strong>幾乎一樣</strong>時，`bf16` 會把它們壓成同一個數字，於是「選哪個」變成丟銅板。
2. 分歧點上量到的分數差，全部落在 `bf16` 的量化格點上（`0.0`、`±0.125`、`±0.25`、`±0.5`）—— 在 4B 模型上，9 個分歧點有 <strong>6 個差距恰好是 0</strong>，是真的位元完全相同。
3. 在 `float32` 下，同樣的位置有 0.001～0.33 的真實差距，排序穩定，兩個執行就收斂到同一串 token。

## 一、這裡其實有兩種「無損」，不是同一件事

推測解碼講「無損」，通常混用了兩個不同強度的定義：

| 層級 | 要求 | 在 bf16 下做得到嗎 |
| --- | --- | --- |
| **演算法層無損** | 送出的每個 token 都等於 target 在該位置的 `argmax` | 可以，這是演算法保證的 |
| **實作層逐位元相同** | `torch.equal(基準, 推測)`，字串／id 完全一致 | **做不到**，因為兩種前向形狀的捨入不同 |

上游的 `examples/benchmark.py` 自己就印了這段免責聲明，很多人（包括第一輪的我）讀過去就忘了：

```text
In bfloat16 the target's batched verification pass and its token-by-token decoding round
differently, so the two can part where the target's top two logits tie to within bfloat16
precision. Run with --dtype float32 for an exact check.
```

問題在於：我的 `acceptance.py` 拿第二種標準當第一種來判，而且一開始還<strong>只比解碼後的字串</strong>（`decode(skip_special_tokens=True)` 加 `.strip()`），連 EOS 與空白差異都會被吃掉。上游比的是 token id，我比的是「看起來像不像」—— 這是第一個該修的地方。

## 二、bf16 到底有多粗

`bf16` 只有 8 個 mantissa bit。換算成這個模型實際的 logit 量級：

| logit 量級 | 相鄰可表示值的間距（ULP） |
| ---: | ---: |
| 1 ~ 2 | 0.0039 |
| 8 ~ 16 | 0.0625 |
| 16 ~ 32 | 0.125 |

模型最後一層的 logit 大約在 15～25 之間，所以**能分辨的最小差距是 0.125**。而實測出來的真實差距是 0.06～0.33 —— <strong>好幾個關鍵位置根本低於雜訊底</strong>。

實測結果非常乾淨。把「基準」與「FlashMap」第一次分歧的那個位置找出來，計算同一個前綴上兩個候選字的 logit 差：

| 模型 | 分歧點數 | 量到的 gap |
| --- | ---: | --- |
| Qwen3-8B | 8 | `0.0`、`+0.25`、`−0.25`、`+0.25`、`−0.25`、`−0.25`、`+0.125`、`−0.5` |
| Qwen3-4B | 9 | `0.0` × 6、`+0.25`、`+0.125`、`−0.125` |

沒有一個是「任意實數」—— 全部是量化格點，4B 甚至有 <strong>6/9 是 0</strong>。當差距是 0 時，`argmax` 回傳的是「索引較小者」，也就是<strong>任何實作細節都能翻轉它</strong>：GEMM 的 tile 形狀、reduction 順序、KV cache 的拼接方式、批次大小。

> **注意**：這裡說的「好幾個位置」不是隨機分布。它是一個<strong>必然會遇到</strong>的現象：模型在 512 個 token 的生成過程中，本來就會經過一些高熵、兩個候選字勢均力敵的位置；`bf16` 的任務就是把「勢均力敵」變成「完全平手」。

<!-- FIG1 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" role="img" aria-label="bf16 的量化格點：真實差距 0.060、0.242、0.320 被壓成 0.000 與 0.250" style="width:100%;height:auto;display:block">
<defs><marker id="mf472b6" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#f472b6"/></marker><marker id="mfbbf24" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#fbbf24"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="538.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">bf16 的量化格點</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">真值 vs bf16 的讀數</text>
<text x="48" y="112" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每一列都是 8B 上真實量到的分歧點：圓點是真的差距，方塊是 bf16 的讀數。</text>
<path d="M 372.0 430 L 884.0 430" fill="none" stroke="#7d8590" stroke-width="1.5"/>
<path d="M 372.0 136 L 372.0 430" fill="none" stroke="#30363d" stroke-width="1.2"/>
<text x="372.0" y="452" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text>
<path d="M 500.0 136 L 500.0 430" fill="none" stroke="#30363d" stroke-width="1.2"/>
<text x="500.0" y="452" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.125</text>
<path d="M 628.0 136 L 628.0 430" fill="none" stroke="#30363d" stroke-width="1.2"/>
<text x="628.0" y="452" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.25</text>
<path d="M 756.0 136 L 756.0 430" fill="none" stroke="#30363d" stroke-width="1.2"/>
<text x="756.0" y="452" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.375</text>
<path d="M 884.0 136 L 884.0 430" fill="none" stroke="#30363d" stroke-width="1.2"/>
<text x="884.0" y="452" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0.5</text>
<rect x="48" y="143" width="270" height="66" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="64" y="173.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">真值 0.06002</text>
<text x="64" y="194.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">第 1 題驗證誤差 0.123</text>
<path d="M 433.46048 176 L 372.0 176" fill="none" stroke="#f472b6" stroke-width="2" marker-end="url(#mf472b6)"/>
<circle cx="433.46048" cy="176" r="7.5" fill="#2dd4bf"/>
<rect x="364.0" y="168" width="16" height="16" rx="3" fill="none" stroke="#f472b6" stroke-width="2.2"/>
<text x="388.0" y="164" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">量到 0.00000</text>
<text x="388.0" y="198" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">完全平手</text>
<rect x="48" y="253" width="270" height="66" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="64" y="283.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">真值 0.24197</text>
<text x="64" y="304.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">第 2 題驗證誤差 0.184</text>
<circle cx="619.77728" cy="286" r="7.5" fill="#2dd4bf"/>
<rect x="620.0" y="278" width="16" height="16" rx="3" fill="none" stroke="#fbbf24" stroke-width="2.2"/>
<text x="644.0" y="274" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">量到 0.25000</text>
<text x="644.0" y="308" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">吸附到格點</text>
<rect x="48" y="363" width="270" height="66" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="64" y="393.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">真值 0.32040</text>
<text x="64" y="414.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">第 7 題驗證誤差 0.476</text>
<path d="M 700.0896 396 L 628.0 396" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#mfbbf24)"/>
<circle cx="700.0896" cy="396" r="7.5" fill="#2dd4bf"/>
<rect x="620.0" y="388" width="16" height="16" rx="3" fill="none" stroke="#fbbf24" stroke-width="2.2"/>
<text x="644.0" y="384" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">量到 0.25000</text>
<text x="644.0" y="418" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">吸附到格點</text>
<text x="48" y="492" font-size="13.5" fill="#f472b6" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">bf16 在這個 logit 量級只分辨得出 0.125 的差距；真值 0.060 於是被壓成 0。</text>
<text x="48" y="514" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8 個分歧點裡有 7 個的真實 gap 小於一個 bf16 ULP（最大也只有 0.32）。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：真實 gap（圓點）與 bf16 量到的格點（方環）——三列都是 8B 上實際量到的分歧點，0.060 被壓成完全平手。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG1 -->

## 三、四個實驗，把責任釘死在精度上

懷疑「有 bug」的時候，最有效的做法不是讀程式碼，而是<strong>一次只改一個變因</strong>，看哪一個變因能讓現象消失。以下四個實驗的程式都在 `lab/` 目錄，可以直接重跑。

### 3.1 唯一變因：把精度換掉

8B 的 `float32` 權重要 32 GiB，超過 RTX 4090 的 24 GiB，所以完整的 A/B 用最小的同構模型對 `Qwen/Qwen3-4B` + `j-shen/FlashMap-Qwen3-4B` 來做：

```bash
TARGET_MODEL=Qwen/Qwen3-4B DRAFT_MODEL=j-shen/FlashMap-Qwen3-4B \
  python acceptance.py --dtype bfloat16 --out results_acceptance_step1_4b_bfloat16.json
TARGET_MODEL=Qwen/Qwen3-4B DRAFT_MODEL=j-shen/FlashMap-Qwen3-4B \
  python acceptance.py --dtype float32 --out results_acceptance_step1_4b_float32.json
```

結果就是開頭那張表：`bf16` 3/12，`fp32` **12/12**。同一份程式、同一組題目、同一個 drafter。

順帶一個交叉驗證：`acceptance.py` 與另一支完全獨立的 `pass4_bf16_shape.py` 是兩個獨立行程、drafter 噪聲各自抽取，但對 12 題給出<strong>完全相同</strong>的 `base_tokens`、`spec_tokens`、`first_diff`。所以不一致<strong>不是隨機性</strong>造成的。

> 補充：每輪「接受幾個 draft」會隨噪聲改變，所以 `round` / `offset` 這種內部結構不穩定；但**送出的 token 序列是穩定的**。這也是為什麼判準要放在「送出的 token」而不是「內部執行細節」。

### 3.2 演算法層：FlashMap 送的到底是不是 target 的 argmax

這一項是整個結論的基礎。我在 target 上掛 forward hook，把 `spec_generate` 裡每一次前向的 logits 全部錄下來，然後逐一檢查<strong>每一個送出的 token 是否等於它自己那一輪驗證的 `argmax`</strong>（不是「大致上」，是逐位元比對）：

| 檢查項目 | 結果 |
| --- | --- |
| 逐 token 自我檢查（每題驗證 129～479 個 token） | **9 / 9 題全部通過** |
| 錄到的前向次數 = 1（prefill）+ 輪數 | 9 / 9 |
| fp32 真實 gap 小於 1 個 bf16 ULP | **8 / 9** |
| fp32 真實 gap ≤ bf16 對同一 logit 的評測誤差 | **8 / 9** |
| fp32 的 argmax 等於 <strong>FlashMap</strong> 的 token | 7 / 9 |
| fp32 的 argmax 等於<strong>基準</strong>的 token | 2 / 9 |

<!-- FIG2 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" role="img" aria-label="一輪推測解碼的形狀：前綴、draft 猜 16 個、target 一次驗證 17 個位置、接受 k 個加 1 個 bonus" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="538.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一輪的形狀</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">draft → 驗證 → commit</text>
<text x="48" y="112" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每一輪都是一樣的形狀；差別只在這一輪接受了幾個 draft。</text>
<rect x="60" y="140" width="180" height="96" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="76" y="185.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">前綴</text>
<text x="76" y="206.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">prompt + 已接受的 token</text>
<path d="M 244 188 L 276 188" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="282" y="140" width="180" height="96" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="298" y="185.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">draft 猜 16 個</text>
<text x="298" y="206.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">由 drafter 產生，可能全錯</text>
<path d="M 466 188 L 498 188" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="504" y="140" width="180" height="96" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="520" y="185.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">target 驗證</text>
<text x="520" y="206.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一次前向 17 個位置</text>
<path d="M 688 188 L 720 188" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="726" y="140" width="180" height="96" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<text x="742" y="185.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">commit</text>
<text x="742" y="206.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">接受前 k 個 + 1 個 bonus</text>
<path d="M 816 236 L 816 302" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 816 302 L 150 302" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 150 302 L 150 240" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<text x="480" y="292" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">下一輪</text>
<text x="48" y="336" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">某一輪的驗證結果（示意：接受 6 個）</text>
<rect x="120" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#3fb95099" stroke-width="1.4"/>
<rect x="162" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#3fb95099" stroke-width="1.4"/>
<rect x="204" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#3fb95099" stroke-width="1.4"/>
<rect x="246" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#3fb95099" stroke-width="1.4"/>
<rect x="288" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#3fb95099" stroke-width="1.4"/>
<rect x="330" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#3fb95099" stroke-width="1.4"/>
<rect x="372" y="350" width="38" height="52" rx="6" fill="#1c2230" stroke="#f472b699" stroke-width="1.4"/>
<rect x="414" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#7d859099" stroke-width="1.4"/>
<rect x="456" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#7d859099" stroke-width="1.4"/>
<rect x="498" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#7d859099" stroke-width="1.4"/>
<rect x="540" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#7d859099" stroke-width="1.4"/>
<rect x="582" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#7d859099" stroke-width="1.4"/>
<rect x="624" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#7d859099" stroke-width="1.4"/>
<rect x="666" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#7d859099" stroke-width="1.4"/>
<rect x="708" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#7d859099" stroke-width="1.4"/>
<rect x="750" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#7d859099" stroke-width="1.4"/>
<rect x="792" y="350" width="38" height="52" rx="6" fill="#161b22" stroke="#7d859099" stroke-width="1.4"/>
<text x="120" y="428" font-size="12.5" fill="#3fb950" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">綠：接受</text>
<text x="240" y="428" font-size="12.5" fill="#f472b6" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">紅：第一個不符 → 改寫成 target 的 argmax</text>
<text x="660" y="428" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">灰：本輪作廢</text>
<text x="48" y="470" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">自我檢查：9/9 題通過（單題最多 479 個 token）—— 每個 commit 都等於它自己那一輪的 argmax。</text>
<text x="48" y="492" font-size="13" fill="#2dd4bf" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">所以送出的每一個 token 都是 target 自己的選擇；不一致只可能來自數值。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：一輪的形狀——draft 先猜 16 個，target 一次驗證 17 個位置（anchor + 16 drafts），接受前 k 個再補一個 bonus；紅格是第一個不符、改寫成 target 的 argmax，之後全部作廢。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG2 -->

既然每個 token 都是 target 的 argmax，那不一致就只可能來自「兩邊算出來的 argmax 不一樣」—— 也就是數值本身，而不是演算法。

> **踩坑紀錄**：這支檢查一開始怎麼跑都是 `False`，原因是索引映射差了 1。`spec[0]` 來自 prefill 那一次前向，驗證區塊的第 0 個位置對應的是 `spec[1]` 而不是 `spec[0]`。我實測了三種位移：`shift=0` 是 0/128，**`shift=+1` 是 128/128**。修正後才是上面那個 9/9。

### 3.3 前向形狀：一次看 17 個位置，還是一次看 1 個

FlashMap 的驗證是「一次前向處理 17 個位置」（anchor + 16 個 draft token），而 `generate()` 是一步一個位置。兩者數學等價，但 `bf16` 下 GEMM 的 row 數不同，累加順序就不同。

我在同一批分歧前綴上，用三種形狀算同一個 next-token 分布：`k=0` 一次吃下整個前綴、`k=1` 只算最後 1 個位置（等於逐字解碼）、`k=16` 最後 16 個位置一起算（等於驗證區塊）：

| id | bf16 k=0 | bf16 k=1 | bf16 k=16 | bf16 翻轉 | fp32 k=0 | fp32 k=1 | fp32 k=16 | fp32 形狀間散佈 |
| ---: | ---: | ---: | ---: | :---: | ---: | ---: | ---: | ---: |
| 3 | 0.00000 | +0.25000 | 0.00000 | – | +0.00119 | +0.00121 | +0.00121 | 1.5e−05 |
| 7 | 0.00000 | −0.25000 | −0.25000 | – | −0.05742 | −0.05744 | −0.05744 | 1.9e−05 |
| **10** | **+0.12500** | **−0.12500** | **+0.25000** | **是** | −0.11644 | −0.11645 | −0.11646 | 1.9e−05 |
| **11** | **−0.12500** | **−0.12500** | **+0.25000** | **是** | −0.33107 | −0.33112 | −0.33112 | 5.7e−05 |

`bf16` 下正負號會隨形狀改變（id 10、11），argmax 就翻轉；`fp32` 下三種形狀的差異只有 7.6e−06～5.7e−05，<strong>零次翻轉</strong>。

**「形狀會改變答案」這件事只在 bf16 發生，fp32 下完全消失。** 這也正好解釋了上游那句警語。

<!-- FIG3 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 630" role="img" aria-label="逐字解碼與區塊驗證：同一前綴、兩種捨入，bf16 下 argmax 會翻轉，fp32 下不會" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="978.5" height="628.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一前綴、兩種捨入</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1 個位置 vs 17 個位置</text>
<rect x="48" y="120" width="430" height="210" rx="14" fill="#1c2230" stroke="#58a6ff55" stroke-width="1.5"/>
<text x="68" y="150" font-size="16" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">逐字解碼 generate()</text>
<text x="68" y="172" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每一步只算 1 個位置</text>
<rect x="84" y="210" width="54" height="46" rx="8" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="111" y="237" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<path d="M 145 233 L 169 233" fill="none" stroke="#7d8590" stroke-width="1.6" marker-end="url(#m7d8590)"/>
<rect x="176" y="210" width="54" height="46" rx="8" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="203" y="237" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text>
<path d="M 237 233 L 261 233" fill="none" stroke="#7d8590" stroke-width="1.6" marker-end="url(#m7d8590)"/>
<rect x="268" y="210" width="54" height="46" rx="8" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="295" y="237" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text>
<path d="M 329 233 L 353 233" fill="none" stroke="#7d8590" stroke-width="1.6" marker-end="url(#m7d8590)"/>
<rect x="360" y="210" width="54" height="46" rx="8" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="387" y="237" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<text x="68" y="300" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">512 個 token 就是 512 次前向</text>
<rect x="510" y="120" width="422" height="210" rx="14" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="530" y="150" font-size="16" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">區塊驗證 spec_generate()</text>
<text x="530" y="172" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一次算 17 個位置（anchor + 16 個 draft）</text>
<rect x="530" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#f472b688" stroke-width="1.2"/>
<rect x="550" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="570" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="590" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="610" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="630" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="650" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="670" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="690" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="710" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="730" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="750" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="770" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="790" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="810" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="830" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<rect x="850" y="210" width="18" height="46" rx="4" fill="#161b22" stroke="#2dd4bf88" stroke-width="1.2"/>
<text x="530" y="300" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">第 1 格是 anchor，其餘 16 格是 draft</text>
<path d="M 263 332 L 263 352" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 721 332 L 721 352" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="356" width="884" height="62" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="490.0" y="385.0" font-size="16" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個前綴、同一份權重</text>
<text x="490.0" y="407.0" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩個形狀算的是同一個函數，只是 GEMM 的形狀不同 → 捨入順序不同</text>
<path d="M 263 420 L 263 444" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 721 420 L 721 444" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="448" width="430" height="108" rx="12" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="68" y="478" font-size="16" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">bfloat16</text>
<text x="68" y="504" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">gap = +0.125 / −0.125 / +0.250</text>
<text x="68" y="528" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 同一題，三種形狀給出兩種答案</text>
<rect x="510" y="448" width="422" height="108" rx="12" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="530" y="478" font-size="16" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">float32</text>
<text x="530" y="504" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">形狀間差異 ≤ 5.7e−05</text>
<text x="530" y="528" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 同一題，三種形狀給出同一個答案</text>
<text x="48" y="588" font-size="13.5" fill="#f472b6" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">上表 id 10 的實測：bf16 的 gap 隨形狀變號，argmax 就跟著翻轉。</text>
<text x="48" y="610" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">fp32 下同一個前綴的差距固定在 −0.11644 附近，三種形狀都選同一個字。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 3：<code>generate()</code> 一步算 1 個位置，FlashMap 的驗證一次算 17 個位置。數學等價、捨入不同：bf16 下 argmax 翻轉，fp32 下三種形狀一致。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG3 -->

### 3.4 那 8B 的真值呢？搬到 CPU 去算

8B 的 `float32` 在 24 GiB 的卡上放不下，但我們其實<strong>不需要整個生成流程</strong>—— 只需要「每個分歧點上算一次前向」。於是把 8B 的 `float32` 前向放到 CPU（32 GiB 記憶體放得下），GPU 只負責用 `bf16` 找出共享前綴：

| id | fp32 真實 gap | bf16 ULP | bf16 評測誤差 | gap ÷ 誤差 | fp32 選的是誰 |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 0.06002 | 0.2500 | 0.12346 | 0.49 | 基準 |
| 2 | 0.24197 | 0.2500 | 0.18433 | 1.31 | 基準 |
| 4 | 0.14489 | 0.2500 | 0.13975 | 1.04 | **FlashMap** |
| 5 | 0.17644 | 0.2500 | 0.21383 | 0.83 | 基準 |
| 6 | 0.18819 | 0.2500 | 0.35210 | 0.53 | **FlashMap** |
| 7 | 0.32040 | 0.2500 | 0.47569 | 0.67 | **FlashMap** |
| 8 | 0.09659 | 0.1250 | 0.04613 | 2.09 | 基準 |
| 9 | 0.06565 | 0.2500 | 0.21906 | 0.30 | **FlashMap** |

兩件事值得注意：

1. **8 個分歧點裡有 7 個的真實 gap 小於一個 bf16 ULP**，最大也只有 0.32。gap 與「bf16 對同一個 logit 的評測誤差」比值的中位數約 0.75 —— 訊號與雜訊同量級。
2. **fp32 真值選中 FlashMap 的 token 4 次、選中基準的 token 4 次。** 五五波。

第二點很重要，需要誠實說：**這不是「FlashMap 比較準」的故事**。在這些位置上，基準自己也沒有還原出 `fp32` 的答案 —— 因為 <strong>bf16 下的基準本身就不是唯一的</strong>。正確的結論是「在 bf16 下這個比較沒有意義」。

## 四、順手結案：HF 算出 217 字、vLLM 算出 155 字，是誰錯了？

追查過程中撞到一個更迷惑人的現象：同一題、同一個 8B 模型、同樣 temperature=0，三種跑法給出兩種答案。

| 執行方式 | 第 2 題的 token 數 | 第 2 題的開頭 |
| --- | ---: | --- |
| HuggingFace `generate()`（bf16） | 217 | `Let's solve this step by step.` |
| HuggingFace `spec_generate()`（bf16） | 155 | `Let's break this down step by step:` |
| vLLM server 基準（bf16） | 155 | `Let's break this down step by step:` |

一開始我懷疑是 prompt 或 chat template 不一致。用 2×2 把「基準呼叫方式」的兩種差異各自拆開來測：傳不傳 `attention_mask`、要不要明確傳 `temperature=1.0` 蓋掉模型 `generation_config` 裡的 `0.6`：

| 變體 | 與上游式基準的 token 完全相同數（8B / 4B，bf16） |
| --- | ---: |
| lab 式（傳 mask、不傳 temperature） | 12 / 12 |
| 只加 mask | 12 / 12 |
| 只留 generation_config 的 0.6 | 12 / 12 |

**三種寫法一字不差。** 也就是說呼叫簽章在數值上是惰性的；prompt 的 token 也與 vLLM 回報的 `prompt_tokens` 完全一致（連那個多餘的 `add_generation_tokens=False` 都是 token-identical）。

真正的解釋很樸素：那三個執行<strong>在分歧點之前的 token 完全一樣</strong>，分歧發生在索引 2，而那個位置的 bf16 gap 恰好是 <strong>0.00000</strong>。vLLM 與 FlashMap 各自用不同的 kernel，剛好 tie-break 到同一邊；HF 的 `generate()` 落到另一邊 —— 然後整段 217 / 155 個 token 就完全不同了。

> 一個字翻盤，後面幾十個字就全變了。這也是為什麼「長度差很多」看起來像嚴重錯誤，實際上只是<strong>一次硬幣的正反面</strong>。

<!-- FIG4 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" role="img" aria-label="同一個前綴、一個 bf16 平手，三條執行給出 217 與 155 兩種長度" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="518.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一個平手，三條路</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個前綴，三種結局</text>
<text x="48" y="112" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">第 2 題：分歧點之前的 token 完全相同，只有索引 2 這一個位置不同。</text>
<rect x="300" y="140" width="360" height="60" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="480.0" y="168.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個前綴</text>
<text x="480.0" y="190.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">分歧點之前的 token 逐一相同</text>
<path d="M 480 200 L 480 240" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 176 240 L 784 240" fill="none" stroke="#7d8590" stroke-width="2"/>
<text x="500" y="228" font-size="12.5" fill="#f472b6" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">bf16 的 gap = 0.00000（完全平手）</text>
<path d="M 176 240 L 176 268" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="36" y="270" width="280" height="110" rx="12" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="56" y="300" font-size="15" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">HF generate()</text>
<text x="56" y="334" font-size="19" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">217 tokens</text>
<text x="56" y="362" font-size="12" fill="#8b949e" font-family="'Cascadia Mono',Consolas,monospace">Let's solve this step…</text>
<path d="M 480 240 L 480 268" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="340" y="270" width="280" height="110" rx="12" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="360" y="300" font-size="15" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">HF spec_generate()</text>
<text x="360" y="334" font-size="19" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">155 tokens</text>
<text x="360" y="362" font-size="12" fill="#8b949e" font-family="'Cascadia Mono',Consolas,monospace">Let's break this down…</text>
<path d="M 784 240 L 784 268" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="644" y="270" width="280" height="110" rx="12" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="664" y="300" font-size="15" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">vLLM baseline</text>
<text x="664" y="334" font-size="19" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">155 tokens</text>
<text x="664" y="362" font-size="12" fill="#8b949e" font-family="'Cascadia Mono',Consolas,monospace">Let's break this down…</text>
<text x="48" y="420" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">三個執行在分歧點之前一模一樣；vLLM 與 FlashMap 各自 tie-break 到「break」，</text>
<text x="48" y="442" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">HF 的 generate() 落到「solve」—— 之後整段 155 / 217 個 token 就分岔了。</text>
<text x="48" y="474" font-size="13.5" fill="#f472b6" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">「長度差很多」看起來像嚴重錯誤，其實只是一次硬幣的正反面。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 4：第 2 題的分歧——三者在前綴上完全相同，索引 2 的 bf16 gap 恰好是 0.00000，vLLM 與 FlashMap 各自 tie-break 到「break」，HF 的 <code>generate()</code> 落到「solve」。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG4 -->

## 五、真正壞掉的是我的量測工具

追查過程中修掉四個會直接誤導結論的 bug：

| 位置 | 症狀 | 原因 | 修法 |
| --- | --- | --- | --- |
| `bench.py` 解析 `/metrics` | 算出「草稿接受率 **17.0**」（>1，物理上不可能） | 用 substring 比對家族名，把 `_created`（Unix 時間戳，約 1.79e9）與 16 個 `_per_pos_` 家族一起加總 | 改成精確比對完整家族名，並依 vLLM v1 語義計算 |
| `bench.py` spec-decode 統計 | 根本沒有 γ | 從未讀 `spec_decode_num_drafts` / `num_accepted_tokens` | 補上 `spec_decode_stats()`，並與 vLLM 自己的 log 對帳 |
| `acceptance.py` 無損性判準 | 拿字串相等當成無損 | `skip_special_tokens=True` + `.strip()` 會吃掉 EOS 與空白差異 | 改成比 token id（上游 `torch.equal` 的作法），另存 `lossless_prefix_ok` / `spec_overshoot` |
| `setup.sh` | 安裝步驟直接失敗 | 傳了不存在的 `--workdir` 參數 | 移除該參數 |

<!-- FIG5 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 500" role="img" aria-label="同一份 metrics 回應的兩種解析：精確比對家族名得到 γ 4.954，substring 比對得到接受率 17.0" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="958.5" height="498.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">指標是怎麼算錯的</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">精確比對 vs substring</text>
<text x="48" y="112" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個 /metrics 回應、兩種認家族名的方式；差別只在「怎麼比對名稱」。</text>
<rect x="48" y="150" width="330" height="120" rx="12" fill="#1c2230" stroke="#2dd4bf55" stroke-width="1.5"/>
<text x="68" y="182" font-size="15" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">正確：精確比對完整家族名</text>
<text x="68" y="210" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只取以 _total 結尾的家族</text>
<text x="68" y="236" font-size="12" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">accepted 2475 / drafts 626 / draft 10016</text>
<rect x="400" y="162" width="164" height="96" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="416" y="196" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">γ</text>
<text x="416" y="232" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4.954</text>
<rect x="572" y="162" width="164" height="96" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="588" y="196" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">草稿接受率</text>
<text x="588" y="232" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">24.71%</text>
<rect x="744" y="162" width="164" height="96" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="760" y="196" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每步 draft</text>
<text x="760" y="232" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">16.0 個</text>
<rect x="48" y="300" width="330" height="120" rx="12" fill="#1c2230" stroke="#f472b655" stroke-width="1.5"/>
<text x="68" y="332" font-size="15" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">錯誤：substring 比對</text>
<text x="68" y="360" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">命中 _created（Unix 時間戳 1.79e9）</text>
<text x="68" y="384" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">與 16 個 _per_pos_ 家族一起加總</text>
<rect x="400" y="312" width="164" height="96" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="416" y="346" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">被加進去的</text>
<text x="416" y="382" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.79e9</text>
<rect x="572" y="312" width="164" height="96" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="588" y="346" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">家族數</text>
<text x="588" y="382" font-size="20" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">18 個</text>
<rect x="744" y="312" width="164" height="96" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="760" y="346" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">算出來的</text>
<text x="760" y="382" font-size="20" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">17.0</text>
<text x="48" y="450" font-size="13.5" fill="#f472b6" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">「接受率 17.0」大於 1 就是最直接的警訊：分母被不相關的家族污染了。</text>
<text x="48" y="472" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">修正後 γ = 4.954、接受率 24.71%、每步 16.0 個 draft token，與 vLLM 的 log 對帳一致。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 5：上排是修正後的正確解析（γ 4.954、接受率 24.71%、每步 16.0 個 draft token）；下排是 substring 比對的後果——把 <code>_created</code> 的 Unix 時間戳與 16 個 <code>_per_pos_</code> 家族一起加進來，算出大於 1 的「接受率 17.0」。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG5 -->

修正後，γ 與接受率終於對得上 vLLM 自己印出的統計：

```text
SpecDecoding metrics: Mean acceptance length: 6.26, Accepted throughput: 176.97 tokens/s,
  Drafted throughput: 538.21 tokens/s, Accepted: 2136 tokens, Drafted: 6496 tokens,
  Per-position acceptance rate: 0.877, 0.771, 0.640, ..., Avg Draft acceptance rate: 32.9%
```

這裡有個容易誤判的地方：vLLM 的 `SpecDecodingLogging` 每次輸出後就 `reset()`，
所以上面那行是**最後一個回報區間**的數字；而 Prometheus 的 `_total` 是**整場累計**
（accepted 2475 / drafts 626 / draft tokens 10016）。兩個都對，只是分母不同：

- <strong>γ = 1 + 2475 / 626 = 4.954</strong>（每個 target forward 送出的 token 數）
- <strong>接受率 = 2475 / 10016 = 24.71%</strong>（被接受的 draft 佔全部 draft 的比例）
- <strong>每步草擬 16.0 個 token</strong>（10016 / 626）

我一開始拿「最後區間的 6.26」去對「累計的 γ」，才會覺得怎麼算都不對。

## 六、修正後的端到端數字

重跑 Phase 2（vLLM 0.31.0、Qwen3-8B + FlashMap-Qwen3-8B、concurrency=1、temperature=0）：

| 領域 | 基準 tok/s | FlashMap tok/s | 加速比 |
| --- | ---: | ---: | ---: |
| 數學 | 54.0 | 379.4 | **7.03×** |
| 程式 | 56.2 | 265.5 | **4.72×** |
| 聊天 | 55.3 | 131.4 | **2.37×** |
| **整體** | 55.2 | 235.8 | **4.27×** |

γ = 4.954、草稿接受率 24.71%。同引擎、同 kernel 下比對 baseline 與 FlashMap 的輸出：完整字串相同 4/12、前 120 字相同 9/12，其餘差異來自驗證 pass 衝過 `max_tokens`（上游文件明載）以及同樣的並列現象。

## 七、必須誠實標記的限制

1. **8B 的 fp32 端到端 A/B 做不到。** 8B 的 fp32 權重是 32 GiB，超過 24 GiB。所以完整 A/B 在 4B 上做，8B 只用「單點前向」在 CPU 上取真值。這是取捨，不是遺漏。
2. **不能宣稱「FlashMap 在 bf16 下比較準」。** 8B 是 4:4、4B 是 7:2，並不系統性偏向哪一邊。
3. **只有 12 題。** 「並列」是隨機事件，換一組題目會得到不同的 mismatch 題號，但機制不變。判準必須是「gap 是否落在 bf16 解析度內」，而不是「哪幾題不同」。
4. **只測 temperature=0、concurrency=1。** 批次服務與 T>0 的分布一致性都未驗證（論文作者也把批次列為未評估）。

## 八、想自己重跑

```bash
git clone https://github.com/kalpakjian/flashmap-local-bench.git
cd flashmap-local-bench/lab
bash setup.sh          # 建立 venv、安裝 vllm 0.31.0 + flashmap、下載模型

python selftest.py     # 不需 GPU 的邏輯自測（含 metric 解析的回歸測試）

# 嚴格無損性檢查（fp32）：預期 12/12
TARGET_MODEL=Qwen/Qwen3-4B DRAFT_MODEL=j-shen/FlashMap-Qwen3-4B \
  python acceptance.py --dtype float32

# 機制驗證
python pass3_bf16_proof.py --out results_pass3.json          # 共享前綴真值 + 逐 token 自我檢查
python pass6_block_shape.py --dtype bfloat16 --out p6.json   # 1 個位置 vs 17 個位置
python pass6_block_shape.py --dtype float32 --ctx-from p6.json --out p6_fp32.json

python bench.py        # Phase 2 端到端 + report.md
```

完整的量測表、每一列的原始數字、以及「白話版」都在 repo 的 `lab/FINDINGS.md` 與 `lab/FINDINGS-easy.md`。

## 九、這件事的通用教訓

> **當「無損」的判定依賴浮點相等時，先問一句：這個精度下，答案唯不唯一？**

推測解碼不是特例。任何「兩條等價但形狀不同的計算路徑」都會遇到同一件事：只要你用 `bf16` 當基準，就會在少數高熵位置得到不一致，而那些不一致<strong>不代表任何一條路徑有錯</strong>。要嘛改用 `fp32` 驗，要嘛把判準從「逐位元相等」換成「是否等於真值的 argmax，且差距在解析度之內」。

我最後留下來的實務做法是三條：

1. **驗無損用 fp32**，不然你量到的是捨入，不是演算法。
2. **比 token id，不要比字串**，否則 EOS 與空白差異會被靜默吃掉。
3. **報告裡要寫清楚「哪一種無損」**，因為這兩種在 `bf16` 下<strong>必然</strong>給出不同答案。


