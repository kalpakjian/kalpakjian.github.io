---
title: MiniMax-H3-Image 對上 Qwen-Image 2.1：同一台 4090 把兩邊跑一遍
date: 2026-11-11 20:00:00
categories:
  - AI 研究札記
tags:
  - MiniMax-H3-Image
  - Qwen-Image 2.1
  - ComfyUI
  - 本地推論
  - 實測
index_img: /img/covers/minimax-h3-image-vs-qwen-image-21.png
banner_img: /img/covers/minimax-h3-image-vs-qwen-image-21.png
---

## 一句話總結

兩邊都能中文寫字、都能文生圖加編輯，但<span> </span><strong>瓶頸完全不同</strong>：MiniMax-H3-Image 是「大圖＋複雜指令」的重型機，33.1B 的 DiT 蒸餾到 6 步，從 4 MP 到 16 MP 幾乎不變慢；Qwen-Image 2.1 是「小、快、迭代」的日常機，7B 的體積換來十秒一版的編輯速度與原生透明底。

<strong>要一次交一張能印刷的大圖，選 H3；要一張圖改十次，選 Qwen。</strong>這句話背後的數字全部是本文在同一台 RTX 4090 上實測出來的，不是引用排行榜。

## 1. 兩邊到底在做什麼

兩個模型都是「一個 checkpoint 同時吃文生圖與圖片編輯」，也都主打中英文字渲染。差別在規模與形狀：

| | <strong>MiniMax-H3-Image</strong> | <strong>Qwen-Image 2.1</strong> |
|---|---|---|
| 視覺主幹 | 33.1B dense DiT、50 層（hidden 5376、56 heads） | 7B、32 層 single-stream DiT |
| 文字編碼器 | Qwen3-VL-32B，取第 50 層 hidden state | Qwen3-VL-8B |
| 取樣 | <strong>6 步、無 CFG</strong>（蒸餾模型） | 20–40 步 |
| 原生輸出 | 4–16 MP：2048²、4096²、5472×3072、6272×2688 | 約 4 MP：2048²、2752×1536 |
| 參考圖上限 | 16 張 | 10 張 |
| 透明底 | 不支援 | <strong>原生 RGBA</strong> |
| 局部編輯 | 只能靠文字描述 | 圈選、塗抹、遮罩 |
| 本機權重 | int8 DiT 19.5 GB ＋ nvfp4 文字編碼器 14.6 GB | int8 DiT 6.8 GB ＋ bf16 文字編碼器 16.3 GB |
| 授權 | MiniMax-H3-Image Community License | Qwen Research License |

值得注意的是：<strong>兩邊的授權都不是 Apache 或 MIT</strong>。H3-Image 走自家社群授權（部分商用需要另外申請書面授權），Qwen 2.1 是研究授權。要商用之前，這一欄比畫質重要。

## 2. 我怎麼測的

同一台機器、同一個 ComfyUI、同一個 sampler，只換模型與必要參數：

| 項目 | 值 |
|---|---|
| GPU | RTX 4090 24 GB |
| ComfyUI | 0.45.0（H3-Image 的原生節點從 0.45.0 才進） |
| Python／torch | 3.11.9／2.16.0.dev+cu132 |
| 權重 | 兩邊都用 Comfy-Org 的 int8 單檔版本 |
| sampler | euler ＋ simple |
| 步數 | H3 固定 6（伺服器只接受 6）；Qwen 20 |
| seed | 42（海報、手錶）、7（編輯） |

三個測試題：一支手錶的微距照、一張「山水之間」的中英雙語海報、以及把前一張手錶改成月光夜景的編輯。每次換模型前都先用 <code>/free</code> 清空 VRAM，避免前一個模型的權重佔著記憶體把數字弄髒——第一次沒清的時候，Qwen 的同一張圖從 49 秒變成 105 秒，差了一倍。

## 3. 速度：差別不在畫質，在瓶頸在哪

<!-- FIG-SPEED -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 350" role="img" aria-label="兩種模型在同一台 RTX 4090 上的實測秒數比較" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="898.5" height="348.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一台 RTX 4090：實測秒數</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ComfyUI 0.45.0、int8 權重、6 步（H3）／20 步（Qwen）、單張輸出，數字為牆鐘時間</text>
<text x="48" y="118" font-size="15" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">文字生圖（T2I）</text>
<text x="48" y="166" font-size="14" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">H3 · 4.2 MP</text>
<rect x="190" y="150" width="116.0" height="22" rx="4" fill="#2dd4bf"/>
<text x="316.0" y="166" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">29.0s</text>
<text x="48" y="214" font-size="14" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">H3 · 16.8 MP</text>
<rect x="190" y="198" width="122.4" height="22" rx="4" fill="#2dd4bf"/>
<text x="322.4" y="214" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">30.6s</text>
<text x="48" y="262" font-size="14" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Qwen 2.1 · 4.2 MP</text>
<rect x="190" y="246" width="196.0" height="22" rx="4" fill="#58a6ff"/>
<text x="396.0" y="262" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">49.0s</text>
<text x="470" y="118" font-size="15" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">編輯（1 張參考圖）· 對數軸</text>
<line x1="612.3" y1="140" x2="612.3" y2="278" stroke="#30363d" stroke-width="1" stroke-dasharray="3 4"/>
<text x="612.3" y="296" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10s</text>
<line x1="672.9" y1="140" x2="672.9" y2="278" stroke="#30363d" stroke-width="1" stroke-dasharray="3 4"/>
<text x="672.9" y="296" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">30s</text>
<line x1="739.4" y1="140" x2="739.4" y2="278" stroke="#30363d" stroke-width="1" stroke-dasharray="3 4"/>
<text x="739.4" y="296" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">100s</text>
<line x1="800.0" y1="140" x2="800.0" y2="278" stroke="#30363d" stroke-width="1" stroke-dasharray="3 4"/>
<text x="800.0" y="296" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">300s</text>
<text x="470" y="166" font-size="14" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Qwen · 1.0 MP</text>
<rect x="600" y="150" width="15.0" height="22" rx="4" fill="#58a6ff"/>
<text x="625.0" y="166" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10.5s</text>
<text x="470" y="214" font-size="14" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">H3 · 1.0 MP</text>
<rect x="600" y="198" width="60.2" height="22" rx="4" fill="#2dd4bf"/>
<text x="670.2" y="214" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">23.8s</text>
<text x="470" y="262" font-size="14" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">H3 · 4.2 MP</text>
<rect x="600" y="246" width="183.8" height="22" rx="4" fill="#fbbf24"/>
<text x="793.8" y="262" font-size="13.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">223.8s</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">兩組放在同一個刻度上會失真，所以編輯那組用對數軸：H3 在 4.2 MP 的編輯要吃 224 秒，而 Qwen 在 1.0 MP 只要 10.5 秒。H3 從 4.2 MP 到 16.8 MP 幾乎不變慢，是這張圖最反直覺的一格。</figcaption>
</figure>
<!-- /FIG-SPEED -->

最反直覺的一格是右上角那條：<strong>H3 從 4.2 MP 畫到 16.8 MP，時間只從 29 秒變成 30.6 秒</strong>。原因是它在 24 GB 的卡上根本是「權重頻寬受限」——每步都要把 19.5 GB 的 int8 權重流一遍，token 變四倍所增加的計算量，反而被這個固定成本蓋掉了。所以對 H3 來說，<strong>解析度幾乎是免費的</strong>，這也解釋了為什麼它敢宣稱原生 16 MP。

Qwen 則是另一種形狀：20 步、每步約 2 秒，7B 的模型跑得很快，但步數多。它的成本是「步數 × 常數」，跟解析度關係比較線性。

| 場景 | H3-Image | Qwen-Image 2.1 |
|---|---|---|
| 文生圖 4.2 MP | 29.0 s | 49.0 s |
| 文生圖 16.8 MP | <strong>30.6 s</strong> | 不支援此原生尺寸 |
| 編輯 1.0 MP（1 張參考圖） | 23.8 s | <strong>10.5 s</strong> |
| 編輯 4.2 MP（1 張參考圖） | 223.8 s | 超過 180 s 仍未完成第一步（手動中斷） |

## 4. 文字渲染：兩邊都寫對字，差在數字

同一個 prompt：一張暖白紙的極簡旅遊海報，大字「山水之間」、下方一行英文「BETWEEN MOUNTAINS AND SEAS」、左下直排年份、右下紅印章。

<figure>
<img src="/img/minimax-h3-image-vs-qwen-image-21/fig-text.jpg" alt="左：MiniMax-H3-Image 的中英雙語海報；右：Qwen-Image 2.1 的同一 prompt 結果" />
<figcaption>圖 2：左為 MiniMax-H3-Image、右為 Qwen-Image 2.1，同一句 prompt、同一 seed。四個繁體字、英文行、印章兩邊都正確，差別在左下角的年份。</figcaption>
</figure>

兩邊都把「山水之間」四個繁體字寫對，英文也一字不差，紅印章的「山」都在正確位置——這在一年前還是做不到的事。真正的分水嶺是<strong>數字</strong>：H3 寫出 <code>2026</code>，Qwen 寫成 <code>2006</code>。

排版品味反而是 Qwen 略勝：它的襯線更細、字距更收斂，看起來像真的平面設計；H3 的字更粗、更像「海報標題」，安全但少了點細節。<strong>但數字錯就是錯</strong>，這種圖直接交件會出事。

實務結論：年份、價格、編號、型號這類「不能錯一個字」的內容，兩邊都要人眼核對；這次 H3 的正確率好一點，但別把校對工作外包給模型。

## 5. 寫實細節：一個聽話，一個懂你要什麼

prompt 同時要求 <code>low angle</code> 與 <code>shallow depth of field</code>，主體是濕板岩上的黃銅懷錶。

<figure>
<img src="/img/minimax-h3-image-vs-qwen-image-21/fig-real.jpg" alt="左：MiniMax-H3-Image 的懷錶微距；右：Qwen-Image 2.1 的同一 prompt 結果" />
<figcaption>圖 3：左為 MiniMax-H3-Image、右為 Qwen-Image 2.1。兩張都符合「低角度、淺景深」，但右邊把景深套到整個主體上，錶面直接糊掉。</figcaption>
</figure>

Qwen <strong>嚴格執行</strong>了那兩個詞：相機貼地、景深極淺，於是只有錶殼邊緣在焦內，錶面全散。H3 則把它讀成「商品微距」——主體立起來、錶面清楚可讀、背景奶油化。

這不是誰畫質好，是<strong>指令遵循的取捨</strong>：Qwen 更像一個照字面執行的助手，你要什麼得自己寫清楚；H3 會替你把意圖補完。反過來說，當你<strong>真的</strong>要極淺景深時，Qwen 給得比 H3 更徹底。

兩邊的共同弱點是細節文字：錶盤上的羅馬數字都有幾處亂掉（<code>IIIA</code>、<code>M</code> 這種），在 4096² 全解析度下看更明顯。

## 6. 編輯：十秒與三分半的差距

同一張來源圖（就是圖 3 左邊那張）、同一句「改成月光夜景」的指令、同一 seed。

<figure>
<img src="/img/minimax-h3-image-vs-qwen-image-21/fig-edit.jpg" alt="左：MiniMax-H3-Image 的月光編輯結果；右：Qwen-Image 2.1 的同一來源圖編輯結果" />
<figcaption>圖 4：左為 MiniMax-H3-Image（4.2 MP，224 秒）、右為 Qwen-Image 2.1（1.0 MP，10.5 秒）。身份都鎖住了，差別在解析度與時間。</figcaption>
</figure>

兩邊都做到了「同一只錶、同一個構圖、只換光線」，身份保持都很好。差別在代價：

- Qwen 在 1.0 MP 只要 <strong>10.5 秒</strong>，這個速度才叫可以迭代。
- H3 在 4.2 MP 要 <strong>224 秒</strong>，因為參考圖加上 19.5 GB 權重把 24 GB 吃滿，每一步都在換頁；把輸出降到 1.0 MP 就回到 <strong>23.8 秒</strong>。
- H3 沒有遮罩概念，局部修改只能靠文字描述；Qwen 可以圈選、塗抹、給遮罩，還能直接生透明底。

如果你想用 H3 做編輯，<strong>把畫布固定在 1.0–1.5 MP</strong>，需要大圖再另外放大。那個 224 秒不是模型慢，是我把畫布開太大。

## 7. 官方說明沒寫、但實測才知道的五件事

1. <strong>解析度幾乎是免費的</strong>——H3 從 4.2 MP 到 16.8 MP 只多 1.6 秒。所以在 24 GB 上沒有理由不直接出大圖，省下來的是「先小圖再放大」那一整條流程（見圖 5）。

2. <strong>24 GB 的甜蜜點是 1 MP 的編輯，不是 4 MP</strong>。兩邊都一樣：超過之後不是變慢，是掉進「權重不停換頁」的地獄。H3 從 24 秒變 224 秒，Qwen 直接卡在第一步跑不完。

3. <strong>參考圖槽位起算不同</strong>。H3 的 <code>MiniMaxH3ImageConditioning</code> 是 0 起算（<code>images.image_0</code>），Qwen 的 <code>TextEncodeQwenImage21</code> 是 1 起算（<code>images.image_1</code>）。用 API 直接打，寫錯不會報錯——它會安靜地當成「沒有參考圖」，你就得到一張普通的文生圖。

4. <strong>H3 的步數沒有自由度</strong>。它蒸餾在 6 步、CFG 固定 1，送 5 步或 8 步會被伺服器直接 400 拒絕，negative prompt 也不接受。Qwen 則是可以調的：20 步 49 秒，官方範例的 40 步大約兩倍時間，品質有沒有值得要看題材。

5. <strong>兩邊的授權都要看清楚</strong>。H3-Image 是 MiniMax 自家的社群授權（部分用途要另外申請書面授權），Qwen 2.1 是研究授權。兩個都不是 Apache，商用前請讀條文而不是讀部落格。

<figure>
<img src="/img/minimax-h3-image-vs-qwen-image-21/fig-16mp.jpg" alt="MiniMax-H3-Image 直接輸出的 4096×4096 懷錶照片" />
<figcaption>圖 5：MiniMax-H3-Image 一次輸出的 4096×4096（16.8 MP），沒有二次放大。板岩紋理、錶圈綠鏽、玻璃上的水珠都是原生細節。</figcaption>
</figure>

## 8. 我的實務結論

| 你要做的事 | 選誰 | 設定 |
|---|---|---|
| 一張要交件／要印刷的大圖 | <strong>H3</strong> | 直接 4096²，6 步，euler＋simple |
| 需要精確中文字與數字的版面 | <strong>H3</strong>（但仍要校對） | 4096²，文字寫在 prompt 裡並逐字核對 |
| 一張圖反覆改光影、改背景 | <strong>Qwen</strong> | 1.0 MP，20 步 |
| 去背、透明底素材 | <strong>Qwen</strong> | 原生 RGBA，prompt 註明透明背景 |
| 局部修一小塊 | <strong>Qwen</strong> | 圈選／遮罩節點 |
| 顯存吃緊、要跟影片模型並存 | <strong>Qwen</strong> | 6.8 GB 對 19.5 GB |

同一台機器上我最後的做法是<strong>兩邊都留著</strong>：H3 負責「出圖」，Qwen 負責「改圖」。兩者權重加起來 26 GB 的磁碟，換到的是不用在單一模型上勉強。

## 9. 資料來源與查證

| 項目 | 連結 | 實查結果 |
|---|---|---|
| H3-Image 官方模型卡 | [MiniMaxAI/MiniMax-H3-Image](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image) | 33.1B、6 步、4–16 MP、社群授權 |
| ComfyUI 單檔權重 | [Comfy-Org/MiniMax-H3-Image](https://huggingface.co/Comfy-Org/MiniMax-H3-Image) | int8 19.54 GB、image VAE 1.09 GB |
| Qwen-Image 2.1 官方模型卡 | [Qwen/Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1) | 7B、32 層、RGBA、研究授權 |
| ComfyUI 官方教學 | [MiniMax-H3-Image tutorial](https://docs.comfy.org/tutorials/image/minimax/minimax-h3-image) | 需要 ComfyUI 0.45.0 以上、範本 0.11.104 以上 |

> <strong>查證說明</strong>：本文所有秒數於 2026-11-11 在本機 RTX 4090 實測，單次量測、每次換模型前清空 VRAM，數字包含模型載入與 VAE 解碼。<br />
> 沒有做的事：只跑了三個 prompt、一個 seed，不是統計結論；Qwen 只測 20 步；H3 的多參考圖（> 2 張）與 21:9 沒有測。<br />
> 會變的東西：套件版本與量化檔隨時會更新，權重檔名以 Comfy-Org 倉庫當下為準。<br />
>
> <strong>封面與圖表</strong>：封面由本機 ComfyUI 的 Qwen-Image 2.1 生成（刻意不含文字，三張候選取其一）；<br />
> 速度圖為手繪內嵌 SVG（對數軸那組有標註）；圖 2 到圖 5 是兩個模型的原始輸出，只做等比縮放與並排，沒有任何修圖。
