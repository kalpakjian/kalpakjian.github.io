---
title: Claude 用三天搬上 AMD GPU：CUDA 護城河裂了多大一條縫？
date: 2026-11-16 21:20:00
categories:
  - AI 研究札記
tags:
  - Claude
  - Anthropic
  - AMD
  - CUDA
  - ROCm
  - MI355X
  - GPU kernel
  - 導讀
index_img: /img/covers/mythos-amd-mi355x-cuda-moat-zh.png
banner_img: /img/covers/mythos-amd-mi355x-cuda-moat-zh.png
---

2026 年 11 月 10 日，Anthropic 向 SEC 遞交 S-1/A；隔天，他們的 IPO 路演影片上線。影片裏「Approach to compute」那一章由共同創辦人兼 Chief Compute Officer Tom Brown 主講，內容比財報數字有趣：他說 Anthropic 現在同時在四種晶片上訓練與服務 Claude——AWS Trainium、Google TPU、NVIDIA GPU、AMD GPU——並把它們當成同一個可替換的算力池。最刺眼的一句是：今年第一次用 AMD GPU，讓自家的前沿模型 Mythos 動手，<strong>三天</strong>就把 Claude 跑起來，Claude 自己移植或重寫了近 100% 的 GPU kernel。

有一支粵語科技評論影片把這件事講得更白：CUDA 到底是什麼、為什麼「搬過去」這麼難、如果連 CUDA 都不用又會怎樣（他自己試過 Vulkan 那條路，卡住了）。這篇把影片的三個論點、我對回一手來源之後的落差，以及「CUDA 護城河到底裂了多少」整理在一起。

<!-- more -->

> <strong>一句話總結</strong>：三天搬完的是「一個模型、一個階段（prefill）」的 bring-up，不是整套 serving stack 搬家。<br />
> 真正鬆動的是「人類手寫 kernel」這一層；編譯器、通訊庫與多年調優還在原地。<br />
> 影片的技術直覺大致正確，但那兩個關鍵數字目前只有 Anthropic 自己的說法，沒有第三方重現。

## 三十秒結論

| 問題 | 一句話回答 |
|---|---|
| **這是什麼事** | Anthropic IPO 路演影片裏，Tom Brown 說今年首次用 AMD GPU，交給自家前沿模型 Mythos 移植，三天跑起 Claude，Claude 自己寫或移植了近 100% 的 kernel |
| **三天搬的到底是什麼** | 一個模型、只有 prompt processing（prefill）那一段，在 AMD MI355X 跑到「可用水平」 |
| **以前要多久** | 數十名工程師、6 到 12 個月（Anthropic 自己的對比） |
| **誰受益** | 不想被單一供應商鎖死的 operator；以及 AMD——MI355X 已有部署，MI450／Helios 第一 GW 排 2027 上半年 |
| **最大的不確定** | 沒有技術報告、沒有第三方重現；數字出自一份賣股票的投資人簡報 |
| **CUDA 護城河還寬嗎** | 硬體與編譯器沒變；先鬆的是「人類手寫 kernel 的經驗」這一層 |

## 一、先把名詞排好

影片花了不少時間解釋「CUDA 是什麼」，因為大部分人只會說「NVIDIA 厲害是因為 CUDA」，卻答不出 CUDA 到底是什麼。這張表可以直接拿去回答老闆：

| 名詞 | 一句話 | 在這次事件的位置 |
|---|---|---|
| CUDA | NVIDIA 的 GPU 程式設計平台：編譯器、數學函式庫、執行環境、profiler | 大家原本都綁在這裏 |
| GPU kernel | 一支丟給 GPU 上萬個 thread 平行執行的函式 | 這次「近 100% 由 Claude 寫」的東西 |
| prefill（prompt processing） | 把整段 prompt 一次算完，順便生出 KV cache | <strong>三天搬完的就是這一段</strong> |
| decode | 逐個 token 生成答案，每一步都要重讀權重與 cache | 這次沒搬，腳註也沒提 |
| ROCm／HIP | AMD 的 CUDA 對應物；HIP 讓 CUDA 程式碼比較好改寫 | 移植的目的地 |
| CANN | 華為昇騰的對應物 | 影片順帶提到，與這次事件無關 |

## 二、這次到底搬了什麼

<!-- FIG1 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 470" role="img" aria-label="一次請求的兩段路：prefill 與 decode，三天只搬完左邊那半" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="938.5" height="468.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一次請求其實是兩段路，三天搬完的只有左邊那半</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">prefill 吃算力、decode 吃記憶體頻寬；兩者的移植難度不是同一個量級</text>
<rect x="48" y="120" width="400" height="120" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="248.0" y="178.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Prefill 提示處理</text>
<text x="248.0" y="200.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">整段 prompt 一次算完，算力密集</text>
<rect x="492" y="120" width="400" height="120" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="692.0" y="178.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Decode 逐 token 生成</text>
<text x="692.0" y="200.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每步只生 1 個 token，頻寬密集</text>
<path d="M 452 180 L 486 180" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<circle cx="410" cy="152" r="21" fill="#2dd4bf" opacity="0.92"/>
<text x="410" y="156.56" font-size="12" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3天</text>
<text x="56" y="286" font-size="14" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">• Mythos 在 MI355X 上把 Claude 跑起來</text>
<text x="56" y="314" font-size="14" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">• 移植或重寫近 100% 的 GPU kernel</text>
<text x="56" y="342" font-size="14" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">• 官方說法：幾乎沒有人類介入</text>
<text x="500" y="286" font-size="14" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">• 這次不在此範圍：腳註沒提</text>
<text x="500" y="314" font-size="14" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">• 延遲與記憶體頻寬的戰場</text>
<text x="500" y="342" font-size="14" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">• vLLM／SGLang 調優最花時間的地方</text>
<text x="48" y="400" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">腳註原文：這些數字指「Anthropic 某個模型在 AMD MI355X 上的 prompt processing」。</text>
<text x="48" y="428" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">也就是說：三天是一個模型、一個階段的 bring-up，不是整套 serving stack 搬家。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：一次請求其實是兩段路。<strong>這次三天搬完的只有左邊那半</strong>——prefill 是大量矩陣乘，decode 才是記憶體頻寬與通訊的戰場。</figcaption>
</figure>
<!-- /FIG1 -->

影片把「Prompt Processing（提示處理）」和「逐個 token 生成」分成兩個階段講，這個切法剛好就是這次事件的邊界。前者要一次讀完整段 prompt，做的事情是大量的矩陣乘——算力密集、kernel 種類少、每個 kernel 都很大；後者每一步只算一個 token，時間幾乎全花在搬運權重與 KV cache，屬於記憶體頻寬密集。兩邊要調的東西完全不一樣。

所以「三天」這個數字，先別急着當成 CUDA 的死亡證明。一份對回原始材料的整理（llms.blog）指出，Anthropic 那張效能圖的腳註寫得很清楚：數字指「Anthropic 某個模型在 AMD MI355X 上的 prompt processing」。The Decoder 的報導也照抄了同一句。<strong>一個模型、一個階段</strong>，就是這三個字的全部範圍。

> <strong>白話說</strong>：這不是「把 Claude 整套搬去 AMD」，是「把 Claude 最像傳統 HPC 的那一段搬過去，然後量它有多快」。

## 三、三天 vs 六到十二個月

<!-- FIG2 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 386" role="img" aria-label="同一件事的兩種成本：數十人六到十二個月，對上一個模型三天" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="938.5" height="384.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一件事的兩種成本</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">AI 吃掉的主要是「沒有人做過」那一段，不是驗收與量測那一段</text>
<rect x="48" y="118" width="360" height="158" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="68" y="156" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">傳統做法（2025 以前）</text>
<text x="68" y="190" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">數十名工程師</text>
<text x="68" y="218" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6–12 個月</text>
<text x="68" y="246" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">逐個 kernel 手寫、手調、對數值</text>
<rect x="532" y="118" width="360" height="158" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="552" y="156" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2026 這次（Anthropic 自述）</text>
<text x="552" y="190" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1 個前沿模型（Mythos）</text>
<text x="552" y="218" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3 天</text>
<text x="552" y="246" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">近 100% kernel 由 Claude 寫或移植</text>
<text x="444" y="176" font-size="12.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一件事</text>
<path d="M 420 200 L 528 200" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<text x="48" y="320" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">邊界一：腳註只涵蓋一個模型的 prompt processing，decode 與整個 serving stack 不在內。</text>
<text x="48" y="350" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">邊界二：「近 100% kernel」不等於 100% 系統——通訊、並行切分、數值驗證仍要人。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：同一件事的兩種成本。傳統要數十人、6 到 12 個月；這次是一個模型、三天。但腳註的範圍只到一個模型的 prompt processing，decode 與整套 serving stack 不在內。</figcaption>
</figure>
<!-- /FIG2 -->

為什麼 AI 這次真的幫得上忙？因為 kernel 這種東西有三個特性：範圍小、有標準答案、可以自動對帳。你讓模型寫一支 attention kernel，正確與否不是靠人看一眼，而是拿 CPU 上的參考實作跑一次數值比對；慢了也不是靠感覺，而是 profiler 出數字。這正是 AI 最擅長的那種任務——<strong>有 oracle 的重複勞動</strong>。

人類的角色因此從「寫」變成「驗收」：確認數值在容許誤差內、看 profiler 找出誰在等資料、決定 VRAM 裏的張量要怎麼擺。影片裏那位講者提到的正是這一步——資料搬運與擺放往往比運算本身更決定效能。

把這件事放回 Anthropic 的整體策略，才看得出他們為什麼肯花力氣搬：四種晶片是同一個池，不是四套互不相干的系統。

<!-- FIG3 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 430" role="img" aria-label="四種晶片被當成同一個可替換的算力池" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="938.5" height="428.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">四種晶片，一個可替換的算力池</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Brown 的原話：早期押注多晶片，現在「incredibly good at it」</text>
<rect x="48" y="120" width="252" height="56" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="66" y="144" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">AWS Trainium</text>
<text x="66" y="164" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">自研訓練晶片</text>
<path d="M 300 148 L 420 148" fill="none" stroke="#7d8590" stroke-width="2"/>
<rect x="48" y="186" width="252" height="56" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="66" y="210" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Google TPU</text>
<text x="66" y="230" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">自研訓練／推論</text>
<path d="M 300 214 L 420 214" fill="none" stroke="#7d8590" stroke-width="2"/>
<rect x="48" y="252" width="252" height="56" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<text x="66" y="276" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">NVIDIA GPU</text>
<text x="66" y="296" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">CUDA 生態最成熟</text>
<path d="M 300 280 L 420 280" fill="none" stroke="#7d8590" stroke-width="2"/>
<rect x="48" y="318" width="252" height="56" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="66" y="342" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">AMD GPU</text>
<text x="66" y="362" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">MI355X 已在服役</text>
<path d="M 300 346 L 420 346" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 420 148 L 420 346" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 420 240 L 550 240" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="556" y="140" width="336" height="200" rx="10" fill="#1c2230" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="576" y="178" font-size="16" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">可替換的算力池</text>
<text x="576" y="210" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">研究、訓練、推論都往池裡丟</text>
<text x="576" y="236" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一份工作落在哪張卡</text>
<text x="576" y="262" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">由價格、供給與成熟度決定</text>
<text x="48" y="402" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">注意：這是路演中的自述，不是第三方審計過的容量分配。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 3：Anthropic 自述的算力分配方式——四種晶片進同一個池，工作按價格、供給與成熟度分派。這句話是「值得搬」的前提，但它同樣是路演中的自述。</figcaption>
</figure>
<!-- /FIG3 -->

## 四、影片沒說、但我覺得更重要的七件事

先看一張圖，再讀下面七點——這七件事其實可以縮成一句：<strong>AI 吃掉的是最內圈那一格，不是外面那一圈</strong>。

<!-- FIG4 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 430" role="img" aria-label="近 100% kernel 只吃掉最內層，外面四層還是人的工作" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="938.5" height="428.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">「近 100% kernel」只吃掉最內層那一格</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">kernel 是最內圈；往外每一層，剛好是 ROCm 這幾年真正卡住的地方</text>
<rect x="48" y="124" width="232" height="232" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="68" y="172" font-size="16" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GPU kernel</text>
<text x="68" y="202" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Claude 寫或移植</text>
<text x="68" y="230" font-size="14" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">近 100%</text>
<text x="68" y="272" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">矩陣乘、attention、</text>
<text x="68" y="294" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">softmax、layernorm</text>
<text x="68" y="330" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">範圍小、有標準答案</text>
<rect x="320" y="124" width="572" height="52" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.5"/>
<text x="340" y="146" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">通訊與集體運算</text>
<text x="340" y="165" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">NCCL（NVIDIA）對 RCCL（AMD）</text>
<rect x="320" y="184" width="572" height="52" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.5"/>
<text x="340" y="206" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">平行切分</text>
<text x="340" y="225" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">TP／EP、資料擺放、topology</text>
<rect x="320" y="244" width="572" height="52" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.5"/>
<text x="340" y="266" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">KV cache 與 batching</text>
<text x="340" y="285" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">paged attention、量化、連續批次</text>
<rect x="320" y="304" width="572" height="52" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.5"/>
<text x="340" y="326" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">驗證與 profiler</text>
<text x="340" y="345" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">數值對帳、尾延遲回歸、瓶頸定位</text>
<text x="48" y="398" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">所以「三天搬完」之後還有一整個 2027 要搬：右邊四格沒有一格是叫 AI 寫 kernel 就會自己好的。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 4：把「近 100% kernel」放回它真正的範圍。左邊那一格是 Claude 這次的成果，右邊四格是 2027 年還要人做的事——這也是我把「三天」讀成 bring-up 而不是 production parity 的理由。</figcaption>
</figure>
<!-- /FIG4 -->

1. <strong>「近 100% 的 kernel」不等於 100% 的系統。</strong>kernel 只是最內層那一塊。往外一層是通訊（NVIDIA 用 NCCL，AMD 是 RCCL）、張量平行與專家平行的切分方式、KV cache 的擺放與 paged attention、量化 kernel、kernel 啟動開銷（CUDA Graph 那類）、以及最不起眼的數值一致性驗證與 profiler 工具鏈。這些沒有一項是「叫 AI 寫一支 kernel」能順手解決的，卻正好是 ROCm 這幾年真正卡住的地方。
2. <strong>三天是 bring-up，不是 production parity。</strong>公開資料裏沒有每 token 成本、沒有尾延遲、沒有「搬完之後跑一個月」的效能回歸。bring-up 的意思是「跑得起來、數字看起來合理」；能不能拿它去服務客戶，是另一份試卷。
3. <strong>這件事的動機不中立。</strong>Anthropic 正在 IPO，AMD 正在賣卡，而動手的是 Anthropic 自家的前沿模型。等於「自家 AI 幫自家省下移植成本，順便講給投資人聽」。不用懷疑它造假——The Decoder 也明說這些數字沒有獨立驗證——但要記得它是一份銷售文件裏的數據。
4. <strong>錢的條款比三天的故事硬得多。</strong>AMD 在 2026 年 7 月 22 日的新聞稿寫得很具體：Anthropic 將部署最多 <strong>2 GW</strong> 的 Instinct MI450 系列 GPU（MI455X 加 EPYC "Venice" 加 Pensando 網路加 ROCm），裝在 Helios 機櫃，<strong>第一 GW 2027 上半年</strong>開始；AMD 同時承諾最多 <strong>50 億美元</strong>的策略投資。同一份新聞稿還有一句常被漏掉：雙方要用 Claude「加速 ROCm 軟體開發」——這其實是自證，ROCm 還需要被加速。
5. <strong>NVIDIA 也在同一張股東名冊上。</strong>2025 年 11 月起，NVIDIA 承諾最多 100 億美元投資 Anthropic；S-1/A 另外提到一筆 260 億美元的條件式私募，多家科技公司在 IPO 價格上認購。所以影片那句「NVIDIA 這次你還不死？」是很好的標題，不是結論——它現在是 Anthropic 的股東之一。
6. <strong>影片那個 Vulkan 對照組要小心讀。</strong>講者說他在 RTX 5090 上用 llama.cpp 跑一個 27B 模型，Vulkan 是 49 tok/s、CUDA 是 52 tok/s。這組數字我查不到一手 benchmark 出處，只能當成單機實驗；而且它量的是 decode，跟這次的 prefill 不是同一件事。技術直覺（Vulkan 可以當跨廠商的底層）是對的，但「差 6% 而已」不能推廣到資料中心。
7. <strong>真正的難關是 decode。</strong>prefill 好搬，因為它就是一大堆大矩陣乘，數學形狀乾淨；decode 牽涉 KV cache 管理、跨卡 all-reduce、continuous batching 的排程，全是軟硬體耦合最深的縫。這也是為什麼「三天」的新聞價值很高，實務價值要等下一集。

## 五、我的實務結論

在決定「現在搬不搬」之前，先把時間軸攤開——三天的新聞落在哪一格，會直接改變你該做的事。

<!-- FIG5 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 400" role="img" aria-label="把新聞放回時間軸：三天只是中間一站，2027 上半年才是硬指標" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="758.5" height="398.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">把新聞放回時間軸</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">三天不是起點；真正要等的是 2027 上半年的第一 GW</text>
<path d="M 196 140 L 196 320" fill="none" stroke="#30363d" stroke-width="2"/>
<text x="176" y="145" font-size="13.5" fill="#7d8590" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2025-11</text>
<circle cx="196" cy="140" r="6" fill="#7d8590"/>
<text x="220" y="145" font-size="13.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">NVIDIA 承諾最多 100 億美元投資（450 億微軟交易的一部分）</text>
<text x="176" y="205" font-size="13.5" fill="#fbbf24" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2026-07-22</text>
<circle cx="196" cy="200" r="6" fill="#fbbf24"/>
<text x="220" y="205" font-size="13.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">AMD 公告：最多 2 GW MI450／Helios、策略投資最多 50 億美元</text>
<text x="176" y="265" font-size="13.5" fill="#2dd4bf" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2026-11-10</text>
<circle cx="196" cy="260" r="6" fill="#2dd4bf"/>
<text x="220" y="265" font-size="13.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">S-1/A 遞交；隔日路演：「三天把 Claude 搬上 MI355X」</text>
<text x="176" y="325" font-size="13.5" fill="#58a6ff" font-weight="700" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2027 H1</text>
<circle cx="196" cy="320" r="6" fill="#58a6ff"/>
<text x="220" y="325" font-size="13.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">第一 GW MI450 才開始部署（Helios 機櫃）</text>
<text x="48" y="372" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">來源：AMD 投資者關係新聞稿（2026-07-22）、S-1/A（2026-11-10）、The Decoder、llms.blog。</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 5：把新聞放回時間軸。三天只是中間一站；硬指標是 2027 上半年第一 GW 才開始部署。</figcaption>
</figure>
<!-- /FIG5 -->

| 情境 | 我會怎麼做 |
|---|---|
| 手上是自建推論服務 | <strong>先搬 prefill、後搬 decode</strong>：prefill 批次大、GEMM 密集、對延遲不敏感，是風險最低的第一塊；decode 留到有時間做尾延遲回歸再談 |
| 要把「移植」交給 AI | 先把任務寫成可測形式：CPU 參考實作、數值容許誤差、profiler 腳本。沒有 oracle 的任務，AI 只會寫出看起來對的 kernel |
| 判斷值不值得搬 | 只認三個數：每 token 成本、尾延遲、正確性回歸通過率。三個都量了才叫搬完，其他都是 bring-up |
| 要不要現在就談換卡 | 可以開始談，但硬指標在 2027 上半年——MI450／Helios 第一 GW 那時才真正上線，現在的新聞是提前定價 |
| 給老闆的一句話 | 影片那句「你叫我不用 CUDA，我情願不做」其實最誠實：工具鏈與人的習慣就是成本，而 AI 這次削掉的是其中「沒有人做過」的那一段 |

## 六、影片與延伸

| 項目 | 來源 | 實查結果 |
|---|---|---|
| 四種晶片、一個算力池 | Simon Willison 的逐字稿 | 「We train and serve Claude now across all four major chip families」，點名 AWS Trainium、Google TPU、NVIDIA、AMD |
| 三天、幾乎無人介入 | 同上（Tom Brown 原話） | 「It got Claude running on AMD in just three days, with basically no human intervention. Claude ported or wrote almost 100% of the kernels.」 |
| 三天到底涵蓋什麼 | The Decoder 圖片說明、llms.blog | 「The figures refer to prompt processing of an Anthropic model on AMD MI355X GPUs」——一個模型、一個階段 |
| MI450 兩 GW 與 50 億美元 | [AMD 新聞稿（2026-07-22）](https://ir.amd.com/news-events/press-releases/detail/1292/amd-and-anthropic-announce-strategic-partnership-to-deploy-up-to-2-gigawatts-of-amd-instinct-mi450-series-gpus) | 最多 2 GW、第一 GW 2027 H1、MI455X 加 Helios、策略投資最多 50 億美元 |
| NVIDIA 的 100 億與 260 億私募 | [The Decoder](https://the-decoder.com/anthropic-says-ai-is-eroding-nvidias-cuda-lead-cutting-an-amd-chip-switch-from-months-to-three-days/) | 2025/11 起最多 100 億；S-1/A（2026-11-10）另有 260 億條件式私募 |
| IPO 價格區間 | [llms.blog](https://www.llms.blog/posts/anthropic-mythos-claude-amd-gpus-three-days) | 每股 70 至 78 美元，中位 74；AMD 約認購 25 億、NVIDIA 約 100 億 |
| Vulkan 49 對 52 tok/s | 影片講者的自述 | ⚠️ 查無一手 benchmark；影片自承是個人實驗，且量的是 decode |

影片：[《【科技專題】Claude 部分運算移植到 AMD 晶片 ⧸ NVIDIA CUDA 護城河有多穩？》](https://www.youtube.com/watch?v=b-JoK-EpIBw)（19 分 31 秒，粵語）。本文引用的說話內容由本機 Whisper large-v3 轉錄，因此專有名詞會有發音誤差——逐字稿裏的 `KUDA` 就是 CUDA、`ROCKHAM` 是 ROCm、`Enfopic` 是 Anthropic。

> <strong>查證說明</strong>：本文數字於 2026-11-16 直接讀取一手或近一手來源（AMD 投資者關係新聞稿、Anthropic S-1/A 的二手引述、Simon Willison 的逐字稿節錄、The Decoder）。<br />
> 三天與「近 100% kernel」是 Anthropic 在路演中的自述，沒有第三方重現；<br />
> Vulkan 對 CUDA 的速度對比只有影片講者的自述，我沒有重跑。<br />
> <br />
> <strong>封面與圖表</strong>：封面由本機 ComfyUI 的 Qwen-Image 2.1 生成（刻意不含文字）；<br />
> 兩張圖表為手繪內嵌 SVG——含中文標籤的圖表交給 AI 生圖會爛成方塊。
