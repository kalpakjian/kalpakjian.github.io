---
title: 把舞者換成另一個人：H3 角色替換 LoRA V1.5 的 15 秒極限實測
date: 2026-11-14 20:00:00
categories:
  - AI 研究札記
tags:
  - MiniMax-H3
  - Character Swap
  - LoRA
  - ComfyUI
  - 實測
index_img: /img/covers/h3-character-swap-lora-v15.png
banner_img: /img/covers/h3-character-swap-lora-v15.png
---

## 一句話總結

<strong>這顆 LoRA 換的不是「臉」，是「人＋衣服」</strong>。我拿一段 15 秒、768×768、24fps 的單一連續鏡（白棚、固定機位、無硬切）當素材，把舞者換成參考圖裡的角色：5 秒短片段一次就中，15 秒一次過則時序整組漂掉，切成 3 段各 5 秒可以救回動作，但代價是兩個明顯跳接。

<strong>如果你的需求是「同一個人、只換臉、衣服場景原封不動」，這顆 LoRA 目前做不到</strong>——我試著在提示詞裡保住原片紅裙，結果是換人完全失效，產出還是原本那位短髮舞者。

以下數字都是同一台 RTX 4090、同一個 ComfyUI、同一組權重實測出來的，不是引用模型卡。

## 1. 這顆 adapter 到底接在哪

它不是獨立模型，是掛在 MiniMax H3 <strong>Ref2VA</strong>（reference-to-video + audio）基礎模型上的 LoRA：`<Video 1>` 給表演與場景，`<Picture 1>` 給新角色的身分與服裝，prompt 負責說清楚「換誰」。

| 項目 | 值 |
|---|---|
| Adapter | `h3_character_swap_v1.5.safetensors`（148 MB，strength 1.0） |
| 基礎模型 | `minimax_h3_ref2va_pruned_int8_convrot`（19.53 GB） |
| 文字編碼器 | `qwen3vl_32b_minimax_h3_nvfp4_awq`（14.61 GB） |
| VAE | video int8 2.62 GB ＋ audio fp32 0.56 GB（另接 TRT 引擎 4.5 GB） |
| 加速器 | `minimax_h3_ref2v_turbo_4step_v0.1`（1.82 GB，4 步、無 CFG） |
| 幀數規則 | 17n+5：5 秒 → 124 幀（5.167s）、15 秒 → 362 幀（15.083s） |

V1.5 的權重檔內嵌 metadata 寫著 `h3-character-swap-v2`、`new_v2_optimizer_steps: 2250`，但 `training_info` 只記到 step 1000。模型卡自己也講了「內部名稱與預算保留下來，實際只做了 1000 次更新」——<strong>看到 2250 不要當成訓練量比較大</strong>。我用官方 `SHA256SUMS` 驗過下載檔（`8f2c3c3e…`），大小 155,110,792 bytes 與站上一致。

## 2. 我怎麼測

| 項目 | 值 |
|---|---|
| GPU | RTX 4090 24 GB |
| ComfyUI | nightly ＋ `--use-ck-attention` |
| 素材 | 768×768、24fps、360 幀、15.000s、<strong>無音軌</strong>、單一連續鏡 |
| 參考圖 | 單一角色、乾淨背景、全身 |
| 取樣 | 4 步（turbo 開）、res_multistep／simple |
| 後處理 | 逐幀色調匹配（對原片做最小平方 gain／bias，strength 0.85） |

所有候選都用同一組參數，只換要驗的變因：先跑 V1 與 V1.5 的同 seed A/B（5.167 秒），再跑 15 秒一次過的三個 seed，最後跑 3×5 秒分段版。

<figure>
<img src="/img/h3-character-swap-lora-v15/fig1-sbs.jpg" alt="左：原始 768×768 舞蹈影片；右：同一時間點的換人結果，舞者已被替換成參考圖中的角色" style="width:100%;max-width:1120px;border-radius:12px" />
<figcaption>圖 1：左為原片、右為同一時間點（第 2.5 秒）的換人結果。場景、機位、燈光與舞步都留著，被換掉的只有人——這是這顆 LoRA 最擅長的一格。</figcaption>
</figure>


## 3. V1 對 V1.5：在這顆鏡頭上幾乎打平

同 seed、同參數、只換 LoRA，逐幀平均絕對差（0–255）：

| 幀 | V1 對原片 | V1.5 對原片 | V1 對 V1.5 |
|---|---|---|---|
| 0 | 8.9 | 10.1 | 2.0 |
| 62 | 9.6 | 10.6 | 2.5 |
| 123 | 13.3 | 13.6 | <strong>4.2</strong> |

兩版都把身分換過去了（長棕髮＋參考圖的臉），場景、鏡頭、燈光、地板全部保住，動作也跟得上。差別只有 2–4/255，肉眼在 5 秒版本上分不出來——這跟模型卡寫的「selected comparisons show improvements, not every shot improves」一致。<strong>我只有單 seed、單鏡頭，不足以宣稱 V1.5 更好，只能說在這顆鏡頭上打平。</strong>

代價是服裝變成混合體：參考圖的黑色上衣進來了，原片的紅裙還留著。這是 prompt 寫「outfit 取 `<Picture 1>`」的合理結果，但視覺上就是一隻「上半身換人、下半身沒換」的舞者。

<figure>
<img src="/img/h3-character-swap-lora-v15/fig2-v1-vs-v15.jpg" alt="左：V1 的換人結果；右：V1.5 同 seed 的換人結果，兩者幾乎相同" style="width:100%;max-width:1120px;border-radius:12px" />
<figcaption>圖 2：同 seed、同參數，左 V1、右 V1.5（第 2.5 秒）。兩張的差別只有 2–4/255，肉眼分不出來——這顆鏡頭上兩個版本打平。</figcaption>
</figure>



## 4. 15 秒一次過：動作時序整組漂掉

同樣 768×768，把時長拉到整段 15 秒（362 幀），三個 seed 全部出現同一個症狀：<strong>原片 5 秒的深蹲、8 秒的舉手，生成結果都停在別的姿勢</strong>。紅裙也開始亂：其中一個 seed 變成粉裙，另一個 seed 直接消失只剩比基尼。

| seed | 耗時 | 紅裙 | 動作對位 |
|---|---|---|---|
| 1234567 | 344 s | 變粉裙、中段消失 | 5s／8s 都錯位 |
| 777001 | 300 s | 整段消失 | 部分對位 |
| 777002 | 300 s | 變成半透明粉紗 | 部分對位 |

<figure>
<img src="/img/h3-character-swap-lora-v15/fig3-seeds.jpg" alt="三個 seed 在第 7.5 秒的結果：左為粉裙、中為裙子消失只剩比基尼、右為半透明粉紗" style="width:100%;max-width:1120px;border-radius:12px" />
<figcaption>圖 3：三個 seed 的第 7.5 秒（左 1234567、中 777001、右 777002）。同一句 prompt、同一張參考圖，紅裙分別變成粉裙、直接消失、變成半透明粉紗——15 秒一次過的服裝一致性守不住。</figcaption>
</figure>


我另外用「逐幀動作能量（相鄰幀差的平均值）與原片的相關係數」當粗指標，四個候選落在 +0.05 到 +0.23 之間。<strong>這個指標只反映節奏有多像，不能當動作正確率的證據</strong>——它跟肉眼看到的姿勢對位常常不一致，所以判斷一律以抽幀目視為準。

## 5. 切 3 段各 5 秒：動作對了，接縫跳了

把原片切成 0–5、5–10、10–15 三段（各 120 幀）分別換人，每段輸出取前 120 幀接回去，總長剛好 15.000 秒。效果很直接：<strong>第二段第 0 幀精準命中原片 5 秒的深蹲姿勢</strong>，第 14.5 秒的手臂延伸也對上了。

問題在接縫。整片逐幀幀差的中位數是 1.9、p95 是 5.0，但兩個接縫是 14.8 與 14.2——大約三倍正常運動量：

<!-- FIG-SEAM -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 320" role="img" aria-label="接縫處逐幀幀差：硬切與交叉溶接的比較" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="898.5" height="318.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="50" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">接縫處的逐幀幀差（0–255）</text>
<text x="48" y="79" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">整片 360 幀中位數 1.9、p95 5.0；接縫遠高於此即為可見跳接</text>
<line x1="330" y1="104" x2="330" y2="286" stroke="#30363d" stroke-width="1" stroke-dasharray="3 4"/>
<text x="330" y="304" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">中位數 1.9</text>
<text x="48" y="128" font-size="14" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5.0s 硬切</text>
<rect x="330" y="112" width="416.0" height="22" rx="4" fill="#fbbf24"/>
<text x="754.0" y="128" font-size="13.5" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">14.83</text>
<text x="48" y="170" font-size="14" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10.0s 硬切</text>
<rect x="330" y="154" width="397.0" height="22" rx="4" fill="#fbbf24"/>
<text x="735.0" y="170" font-size="13.5" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">14.17</text>
<text x="48" y="212" font-size="14" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5.0s 溶接 167ms</text>
<rect x="330" y="196" width="117.4" height="22" rx="4" fill="#2dd4bf"/>
<text x="455.4" y="212" font-size="13.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4.19</text>
<text x="48" y="254" font-size="14" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10.0s 溶接 167ms</text>
<rect x="330" y="238" width="91.9" height="22" rx="4" fill="#2dd4bf"/>
<text x="429.9" y="254" font-size="13.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3.28</text>
</svg>
<figcaption style="font-size:13px;color:#8b949e;margin-top:10px;line-height:1.6;font-family:'Segoe UI','Microsoft JhengHei',sans-serif">圖 4：在兩個接縫做 167ms 交叉溶接，幀差從 14.8／14.2 降到 4.2／3.3（落回 p95 以內）。</figcaption>
</figure>

<figure>
<img src="/img/h3-character-swap-lora-v15/fig4-seam.jpg" alt="接縫前後三幀：第 4.6 秒站立、第 5.0 秒突然變成深蹲、第 5.4 秒繼續前傾" style="width:100%;max-width:1120px;border-radius:12px" />
<figcaption>圖 5：第 4.6／5.0／5.4 秒連續三幀。第 5.0 秒那格就是接縫——上一段還站著，下一段直接從深蹲起手，這就是 14.8 的幀差長什麼樣子。</figcaption>
</figure>

溶接把數字壓下來了，但我目視檢查發現更醜的東西：<strong>兩段姿勢差太多時，交叉溶接會出現雙人影殘像</strong>——同一畫格裡兩個身體疊在一起。所以最終交付採硬切，把兩個跳接當剪輯點處理，而不是用溶接假裝連續。

根因是每段生成都會自己「重新錨定」：餵它 5–10 秒的片段，它從自己的起手姿勢開始演，不會從原片第 5 秒那個姿勢接著演。<strong>段越短越準、段越多接縫越多</strong>，這是這條路線的固有限制，不是參數沒調好。

## 6. 想保住原片服裝？換人直接失效

我另外跑了一整輪 3×5 秒，只把 prompt 的服裝句改成「保留原片紅裙、只換臉與頭髮」，其餘不動：

> Keep the replacement character's face, hair and body from `<Picture 1>`, but keep the long red dress the dancer wears in `<Video 1>`.

結果是<strong>三段的換人全部沒有發生</strong>：臉、髮型、身高都還是原本那位舞者，只有紅裙被完整保留。這代表這顆 LoRA 把「身分」與「服裝」綁在一起學，拆開寫會讓它退回「照抄原片」。

要「原片服裝＋新臉」目前只能走別的路（例如先換人再對服裝區域做遮罩替換），單靠一句 prompt 做不到。

## 7. 成本

| 做法 | 解析度／時長 | 耗時 | 備註 |
|---|---|---|---|
| 單段 5 秒 | 768×768／124 幀 | 60–105 s | 第一次含 TRT 引擎載入 |
| 一次過 15 秒 | 768×768／362 幀 | 300–344 s | 4 步、每步約 65 s |
| 3×5 秒分段 | 同上合計 | 約 300 s ＋接縫處理 | 每段 95–100 s |

色調匹配對 362 幀約 3 秒（CPU 的 ffmpeg rawvideo 管線）。

## 8. 交付

| 檔案 | 規格 | 說明 |
|---|---|---|
| `FINAL_swap_v15_seg3x5s.mp4` | 768×768／360 幀／15.000s／無音軌 | 主推：3×5s 分段，動作對位最好 |
| `FINAL_swap_v15_single15s.mp4` | 768×768／358 幀／15.075s | 備選：一次過、無接縫但時序漂 |
| `FINAL_swap_v15_seg3x5s_SBS.mp4` | 1280×640 | 左原片／右換人，方便逐格比對 |

順手修掉兩個會污染數據的管線 bug：

1. 色調匹配階段把 SaveVideo 回傳的 `subfolder` 丟掉了。輸出前綴含 `video/` 時，程式去 `output/` 根目錄找檔找不到，<strong>整個色調匹配被靜默跳過</strong>（KeyError `'streams'`），看起來像「做了匹配、其實沒做」。
2. LoRA 檔名寫死在 payload 裡，換版本要手改 JSON。改成可由 config 覆寫後，V1／V1.5 才能用同一支腳本跑同 seed 對照。

## 結論

<strong>短、連續、單人、固定機位</strong>是這顆 LoRA 的甜蜜點：5 秒、768×768、4 步，一分鐘一支，換人成功率高。一旦拉長到 15 秒，它會自己重寫編舞；切成 5 秒段能救回動作，但你要接受接縫。至於「只換臉不換裝」，現在沒有捷徑。

要玩的話，三個判斷點：參考圖先弄乾淨（單人、全身、純色背景）、prompt 只指定「哪一個人」不要描述外貌、先用 5 秒驗一次再決定要不要拉長。
