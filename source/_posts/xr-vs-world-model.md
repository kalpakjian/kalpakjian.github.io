---
title: XR 建模與世界模型：兩條路線，一個交會點
date: 2026-10-26 15:30:00
categories:
  - AI 碼研究札記
tags:
  - 世界模型
  - World Model
  - XR
  - VR
  - AR
  - 3D Gaussian Splatting
  - 4DGS
  - NeRF
  - 物理 AI
  - 具身智能
  - 機器人
  - sim2real
  - NVIDIA
  - JEPA
  - 數位孿生
toc: true
math: true
index_img: /img/covers/xr-vs-world-model.png
banner_img: /img/covers/xr-vs-world-model.png
---

![XR 建模與世界模型：兩條路線，一個交會點](/img/covers/xr-vs-world-model.png)

> **XR 建模／3D 重建**和**物理 AI／世界模型**不是同一件事。
> 但「世界模型成熟後成就 XR，而不是 XR 成就世界模型」這句要稍作修正——
> 兩者更像是**互相供給資料與應用場景，但技術目標不同**。
>
> 這篇把兩條路線的核心判斷、關鍵文獻與 2026 年的最新進展攤開來比，
> 並標出每一個論述所依據的一手來源——包括三處**引用錯配**的更正。
>
> 全文資料截至 2026-10-26，所有連結皆已逐一實測可存取。

<!-- more -->

## 零、兩個必須先更新的前提

在展開比較之前，有兩個前提得先更新，否則後面的比較會建立在過時的假設上。

### 1. World Labs 已併入 AMD

2026 年 9 月 28 日，World Labs 簽署最終協議併入 AMD，交易預計 2026 年底前完成（需監管批准）。
Fei-Fei Li 將擔任 AMD **Executive Vice President and Chief Scientist**，直接向 Lisa Su 匯報；
Justin Johnson 與 Ben Mildenhall 留任，持續帶領 World Labs 團隊，並入 AMD 組成前沿研究組織。
官方給出的理由是「scaling our efforts, scaling our reach, and **getting closer to the hardware**」。

這不是財報附註裡的枝節。它意味著「World Labs vs Meta」不再是兩家前沿實驗室的路線之爭，
而是**硬體垂直整合（AMD）vs 純模型路線（Meta）**的張力——而這個張力恰好印證本文的核心論點：
世界模型的瓶頸已經不在算法，而在算力、延遲與部署形態。

> [World Labs is Joining AMD](https://www.worldlabs.ai/blog/amd-announcement) ｜
> [Fei-Fei Li：To Seek a Newer World](https://drfeifei.substack.com/p/worldlabs-joining-amd)

### 2. 世界模型這條線的戰場已經從「渲染」移到「模擬」

李飛飛自己的分類學把世界模型拆成三種功能：**Renderer**（輸出給人看的像素，重視視覺保真度）、
**Simulator**（輸出幾何、物理與動力學上可信的 state，供人和程式共同計算與互動）、
**Planner**（輸入觀測與目標，輸出動作，閉合感知—行動迴路）。
而她在同一篇裡明確指出三者之間的現實分工：

> "The renderer is by far the most commercially mature… Yet renderers optimize for visual plausibility rather than physical accuracy, and that ceiling matters. Their outputs are beautiful, but they cannot be trusted to design a building or train a robot."

以及她對模擬器的定位：

> "Of the three categories, the simulator gets the least public attention, and is the most consequential of the three."

這解釋了一個常被忽略的事實：**世界模型的定義邊界，本質上是在「模擬」這一支上劃定的**，
---

## 一、兩條技術路線

<!-- FIG1 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 700" role="img" aria-label="XR 建模／重建 vs 世界模型：兩條路線的完整對照｜同一個世界，兩種不同的契約與評準" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="938.5" height="698.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">XR 建模／重建 vs 世界模型：兩條路線的完整對照</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個世界，兩種不同的契約與評準</text>
<rect x="48" y="106" width="416" height="470" rx="14" fill="#1c2230" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="76" y="146" font-size="18" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">XR 建模／3D 重建</text>
<text x="76" y="172" font-size="12.5" fill="#2dd4bf" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">把世界呈現給人</text>
<text x="76" y="200" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">核心目標</text>
<text x="76" y="222" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">讓人類在裝置中看到、走進、</text>
<text x="76" y="242" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">操作一個可信的 3D 空間</text>
<text x="76" y="274" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">資料來源</text>
<text x="76" y="296" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">360 相機、LiDAR、深度相機、</text>
<text x="76" y="316" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">CAD、遊戲引擎資產</text>
<text x="76" y="348" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出</text>
<text x="76" y="370" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全景影像、mesh、點雲、</text>
<text x="76" y="390" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Gaussian Splat、碰撞體、材質</text>
<text x="76" y="422" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">評估標準</text>
<text x="76" y="444" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">視覺一致性、幾何準確度、延遲、</text>
<text x="76" y="464" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">舒適度、互動穩定性</text>
<text x="76" y="494" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">典型用途</text>
<text x="76" y="516" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">VR／AR、數位孿生、遊戲、培訓</text>
<text x="76" y="548" font-size="12.5" fill="#2dd4bf" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">重建是手段，不是世界模型的定義</text>
<rect x="496" y="106" width="416" height="470" rx="14" fill="#1c2230" stroke="#c084fc66" stroke-width="1.5"/>
<text x="524" y="146" font-size="18" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">世界模型／物理 AI</text>
<text x="524" y="172" font-size="12.5" fill="#c084fc" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">把世界變成 AI 可預測的狀態</text>
<text x="524" y="200" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">核心目標</text>
<text x="524" y="222" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">讓 AI 在內部預測：若採取某動作，</text>
<text x="524" y="242" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">世界會怎樣變化</text>
<text x="524" y="274" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">資料來源</text>
<text x="524" y="296" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">影片、機器人操作軌跡、</text>
<text x="524" y="316" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">感測器狀態、模擬環境</text>
<text x="524" y="348" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出</text>
<text x="524" y="370" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">潛在狀態、未來觀測、動作後結果、</text>
<text x="524" y="390" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">可規劃的策略</text>
<text x="524" y="422" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">評估標準</text>
<text x="524" y="444" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">因果正確性、長時程預測、少幻覺、</text>
<text x="524" y="464" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">任務成功率、sim2real 遷移</text>
<text x="524" y="494" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">典型用途</text>
<text x="524" y="516" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">機器人、自動駕駛、具身智能、規劃</text>
<text x="524" y="548" font-size="12.5" fill="#c084fc" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">預測未來（動作→結果）才是核心</text>
<path d="M 480 130 L 480 552" fill="none" stroke="#30363d" stroke-width="1.5"/>
<text x="480" y="596" font-size="13.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">技術目標不同，卻互供資料與場景</text>
<text x="48" y="640" font-size="13.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4D Gaussian Splatting 是世界模型可用的空間表徵之一，</text>
<text x="48" y="662" font-size="13.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">但 4DGS 本身不是世界模型——重建場景是手段，預測未來才是定義。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：兩條技術路線的目標、資料來源、輸出與評估標準｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG1 -->

| 面向 | XR 建模／360 內容 | 世界模型／物理 AI |
|---|---|---|
| 核心目標 | 讓人類在裝置中「看到、走進、操作」一個可信的 3D 空間 | 讓 AI 在內部預測「若採取某動作，世界會怎樣變化」 |
| 資料來源 | 360 相機、LiDAR、深度相機、CAD、遊戲引擎資產 | 影片、機器人操作軌跡、感測器狀態、模擬環境 |
| 輸出 | 全景影像、mesh、點雲、Gaussian Splat、碰撞體、材質 | 潛在狀態、未來觀測、動作後結果、可規劃的策略 |
| 評估標準 | 視覺一致性、幾何準確度、延遲、舒適度、互動穩定性 | 因果正確性、長時程預測、少幻覺、任務成功率、sim2real 遷移 |
| 典型用途 | VR／AR、數位孿生、遊戲、培訓、遠端協作 | 機器人、自動駕駛、具身智能、規劃與控制 |

360 縫合本質上是把既有拍攝視點拼成可觀看的全景；即使加上立體視差，使用者的移動仍大致受拍攝路徑或重建品質限制。
4D Gaussian Splatting 則是從多視角觀測學習一個可從新視角渲染、且可隨時間變化的場景表徵，
因此確實比傳統全景縫合更接近「可自由漫遊的 3D 場景」。

這裡有一個容易被忽略的實作細節，說明「重建」與「模擬」的分界不是抽象概念。
以 Marble 的實際輸出格式為例：splat 有 SPZ 與 PLY 兩種，各自提供約 200 萬與 50 萬 splats 的解析度；
mesh 則分為 **Collider Mesh**（GLB，10–20 萬三角形，官方措辭是「optimized for simple physics calculations」）
與 HQ Mesh（約 60 萬–100 萬三角形，含貼圖或頂點色）。
注意 collider mesh 的定位——它是給物理引擎用的**粗略**碰撞體，不是高精度幾何。
這個「視覺保真（splat／HQ mesh）與物理可用（collider mesh）分離」的設計，正是上面那條分類的工程實現。

> [Marble: A Multimodal World Model](https://www.worldlabs.ai/blog/marble-world-model) ｜
> [Export file specs](https://docs.worldlabs.ai/marble/export/specs)

---

<!-- FIG2 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 730" role="img" aria-label="世界模型的三種功能：Renderer、Simulator、Planner｜三者都是 POMDP 迴路的投影，但契約不同" style="width:100%;height:auto;display:block">
<defs><marker id="m2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker><marker id="mfbbf24" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#fbbf24"/></marker><marker id="m58a6ff" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#58a6ff"/></marker><marker id="mc084fc" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#c084fc"/></marker><marker id="m3fb950" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#3fb950"/></marker></defs>
<rect x="0.75" y="0.75" width="938.5" height="728.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">世界模型的三種功能：Renderer、Simulator、Planner</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">三者都是 POMDP 迴路的投影，但契約不同</text>
<text x="48" y="118" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">POMDP 迴路：三者都是這個迴路的不同投影</text>
<rect x="48" y="138" width="176" height="58" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="136.0" y="165.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Agent</text>
<text x="136.0" y="187.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">人、機器人、軟體</text>
<path d="M 228 167 L 300 167" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#m2dd4bf)"/>
<rect x="304" y="138" width="176" height="58" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="392.0" y="165.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Action</text>
<text x="392.0" y="187.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">動作改變世界</text>
<path d="M 484 167 L 556 167" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#mfbbf24)"/>
<rect x="560" y="138" width="176" height="58" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="648.0" y="165.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">State</text>
<text x="648.0" y="187.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">完整但不可見的現實</text>
<path d="M 648 200 L 648 226" fill="none" stroke="#58a6ff" stroke-width="2" marker-end="url(#m58a6ff)"/>
<rect x="560" y="230" width="176" height="58" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="648.0" y="257.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Observation</text>
<text x="648.0" y="279.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">光子、感測器、像素</text>
<path d="M 556 259 L 484 259" fill="none" stroke="#c084fc" stroke-width="2" marker-end="url(#mc084fc)"/>
<rect x="304" y="230" width="176" height="58" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<text x="392.0" y="257.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Policy</text>
<text x="392.0" y="279.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">由觀測決定下一步</text>
<path d="M 300 259 L 228 259" fill="none" stroke="#3fb950" stroke-width="2" marker-end="url(#m3fb950)"/>
<path d="M 136 230 L 136 200" fill="none" stroke="#3fb950" stroke-width="2" marker-end="url(#m3fb950)"/>
<text x="480" y="312" font-size="13" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">世界模型 = 學會預測這條迴路上的一環</text>
<text x="48" y="356" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">三種功能：契約（contract）不同</text>
<rect x="48" y="374" width="268" height="214" rx="12" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="72" y="406" font-size="16" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Renderer</text>
<text x="72" y="430" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出給人看的像素</text>
<text x="72" y="456" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">契約：視覺保真度</text>
<text x="72" y="484" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">最商業化、最受關注</text>
<text x="72" y="506" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">但為視覺可信最佳化，</text>
<text x="72" y="526" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">無法用來訓練機器人</text>
<text x="72" y="564" font-size="12" fill="#2dd4bf" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">例子：影片生成模型、Genie 3、RTFM</text>
<rect x="332" y="374" width="268" height="214" rx="12" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="356" y="406" font-size="16" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Simulator</text>
<text x="356" y="430" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出可信的 state</text>
<text x="356" y="456" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">契約：結構與物理保真</text>
<text x="356" y="484" font-size="12.5" fill="#fbbf24" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">最少人注意，卻最具後果</text>
<text x="356" y="506" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同時服務兩種消費者：</text>
<text x="356" y="526" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">人類專業與程式（RL、控制器）</text>
<text x="356" y="564" font-size="12" fill="#fbbf24" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">例子：Marble 的 collider mesh + 物理引擎</text>
<rect x="616" y="374" width="268" height="214" rx="12" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="640" y="406" font-size="16" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Planner</text>
<text x="640" y="430" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸出動作</text>
<text x="640" y="456" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">契約：動作是否正確</text>
<text x="640" y="484" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">最迷人、也最初期</text>
<text x="640" y="506" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">閉合感知—行動迴路</text>
<text x="640" y="526" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">多數 demo 仍受限於實驗室</text>
<text x="640" y="564" font-size="12" fill="#c084fc" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">例子：VLA、世界行動模型（WAM）</text>
<rect x="48" y="610" width="836" height="92" rx="12" fill="#1c2230" stroke="#3fb95066" stroke-width="1.5"/>
<text x="72" y="640" font-size="15" fill="#3fb950" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">模擬器是樞紐（the linchpin）</text>
<text x="72" y="664" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">語言是世界抽象，像素是世界投影，而幾何、物理與動力學才是世界本身。</text>
<text x="72" y="686" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只學會渲染或只學會規劃的模型，兩樣都做不來。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：POMDP 迴路與世界模型的三種功能，模擬器是樞紐｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG2 -->

## 二、你說的「因果理解」是關鍵

世界模型的重點不是「把場景重建得很漂亮」，而是學到一個函數：

$$\hat{s}_{t+1} = f(s_t, a_t)$$

其中 $s_t$ 是目前狀態或其潛在表徵，$a_t$ 是動作，$\hat{s}_{t+1}$ 是對未來狀態的預測。
對機器人來說，這正是「我推杯子，杯子會怎樣移動；我夾不住，會不會滑落」的內部模擬能力。

Yann LeCun 的 JEPA 路線正是你描述的「AI 看特徵向量」：它不強迫模型逐像素重建畫面，
而是在 latent space 中預測未來觀測的表徵，藉此避開紋理、光影等對決策未必重要的細節，
把容量留給結構、物件關係與動態。JEPA 的技術細節可參考 I-JEPA（arXiv:2301.08243）與
V-JEPA（arXiv:2404.08471），其中 V-JEPA 明言其訓練「without the use of pretrained image encoders,
text, negative examples, **reconstruction**, or other sources of supervision」——
不重建，正是它能學到結構性物理直覺的原因。

所以可以這樣說：

- **重建場景**是手段之一，不是世界模型的定義。
- **預測未來**、尤其是「動作—結果」的因果關係，才是世界模型的核心。
- **渲染出人類可看的畫面**只是必要時的解碼介面，用於人類檢查、監督、除錯或內容呈現。

這個「三段式」不只是概念分類，它有可量化的後果。Meta 在 2025 年 6 月隨 V-JEPA 2 一併釋出
三個物理推理基準：IntPhys 2（用遊戲引擎生成「物理被違反」的事件對，要求模型辨識哪段影片發生違例）、
MVPBench（最小差異影片對，專門對付語言模型的捷徑解讀）、
CausalVQA（因果問答，含反事實、預測與規劃三類）。結果是：
**人類在這三項都有 85%–95% 的準確率，而包括 V-JEPA 2 在內的頂尖模型則與人類有顯著差距**。
IntPhys 2 上「current video models are at or close to chance」。

---

## 三、李飛飛那邊不是單純 4DGS

李飛飛與 World Labs 的定位是 **spatial intelligence**：從文字、圖像、影片或空間草圖生成可探索的 3D 環境。
但「Atlas 可從單張圖生成新視角與 3D 幾何，並轉成 3D Gaussian splats」這個描述需要更新——
它對應的是 2025 年的舊版能力。

**2026 年 9 月 1 日發布的新一代 Atlas** 是一個**多模態自迴歸 diffusion transformer**，
從零預訓練，原生處理 text、images、video、3D，所有輸入被編碼進共享的 **spatial context**。
關鍵設計是「每張參考影像都被錨定在空間中的 3D 位置」——這正是「渲染只是解碼介面」的架構化表達。
四類任務：

- **Camera-Controlled Generation**：精準的相機幾何作為**原生輸入型別**（非文字提示），
  從一張到六張參考圖生成最高 1 分鐘、1440p 的影片；能生成參考圖未見的背面與場景延伸
- **Spatial Reconstruction**：從單張到數十張影像重建真實場景，輸出新視角影像與明確 3D；
  在 pointmap error 基準上超越 VGGT-Ω、Depth Anything 3、MapAnything、π³ 等專職重建模型
  （平均 8.6，優於次佳的 9.7）
- **Space-Time Simulation**：從影片建模時空，支援機器人的 Real-to-Sim 工作流
- **Image Generation**：從文字生成影像與 **360° 全景**

值得注意的是，Atlas 目前僅向選定的合作夥伴開放早期存取，將驅動未來版本的 Marble。

> [Atlas: A World Model for Spatial Intelligence](https://www.worldlabs.ai/blog/atlas)

而在她們自己的功能分類裡，世界模型被拆成三種功能：

- **Renderer**：輸出給人看的像素，重視視覺保真度。
- **Simulator**：輸出幾何、物理與動力學上可信的 state，可供程式計算與互動。
- **Planner**：根據觀測與目標輸出動作，閉合「感知—行動」迴路。

Marble 這類系統會輸出 Gaussian splats，也會輸出 collision mesh，讓物理引擎可以接手；
這說明它不是把 4DGS 當終點，而是把它當作通往可模擬、可交互世界的表示層。

---

## 四、世界模型如何跨過 sim2real

如果物理引擎模擬已經完全等同真實世界，機器人在模擬中學到的策略就能直接搬到現實，
但現實中有摩擦、接觸力、材料變形、感測雜訊、光照、控制延遲與未建模自由度。

物理引擎是**顯式**的模擬器：它有手寫的力學方程、材質參數、碰撞模型，
錯誤會以 NaN、穿透、爆炸等**可觀測的方式**暴露出來。
世界模型是**學出來的**模擬器：它沒有權威的物理方程，
錯誤表現為幻覺、長時程誤差累積、罕見事件失真與反事實推論不足。
它的危險不在於崩潰，而在於**自信地給出一個看起來合理但物理上錯誤的未來**。

這個差別在生成式模擬器上變得格外尖銳。李飛飛自己的診斷是：

> "Generative simulators introduce a new risk on top of that: AI-generated geometry can look correct while containing self-intersections or wrong scale that produce nonsensical physics."

這正是「隱式且可能有誤的模擬器」最精確的表述——**視覺正確、物理錯誤**，
而且錯誤不會以崩潰的形式提示你。

那麼誰已經跨過去了？2026 年 7 月 21 日 World Labs 併購機器人與模擬公司 SceniX；
7 月 28 日發表 **R2S2R（Real-to-sim-to-real）** 成果。做法是：把真實任務重建為互動式模擬，
然後系統性變換外觀、物件配置、雜物、**物理參數**、機器人狀態與相機視角，產生數千個變體。
報告的結果是：

- **零真實世界訓練資料**學會複雜操作任務
- **模擬能預測真實效能**：跨 policy 架構、跨 checkpoint，模擬評測**保留真實世界的效能排名**，
  追蹤改進與停滯，並重現相同的成功／失敗空間分佈。
---

## 五、「1＋2 融合」的修正

你說成熟世界模型是「因果理解＋場景理解」融合，這個方向合理。
更精確地說，成熟系統至少要同時具備（**以下為筆者歸納，非任一原文的 checklist**）：

1. **空間一致性**：新視角、遮擋、幾何與物件位置不會亂掉。
2. **動態因果一致性**：推、抓、放、碰撞、重力、摩擦等結果合理。
3. **動作條件化**：同一場景在不同動作下產生不同且可驗證的未來。
4. **不確定性處理**：知道「我不知道」，而不是硬生成一個看似合理但錯誤的未來。
5. **可規劃性**：預測結果能回饋給策略，讓機器人選出更好的動作。

李飛飛的分類學為這份清單提供了官方背書中的**第 3 點**，並且給出了更精確的表述：

> "Every level is moving from passive output to interactive system, with renderers becoming **action-conditioned**, simulators generating worlds that are more controllable and editable, and planners deliberating rather than just reacting."

以及她指出的最終形態：

> "**The logical endpoint is a unified world model**: one foundation model that can render photorealistic views, produce physically accurate structure, and plan action sequences, switching between output modalities depending on what the downstream consumer needs."

但她也點明了這條路徑的**未解難題**，這段值得完整保留：

> "The data picture is uneven, with renderers awash in internet video while simulators and planners face acute shortages of 3D assets and robot demonstrations. Optimizing for visual beauty can sacrifice the precision a robot or a high-fidelity simulation needs. **Reconciling these tensions inside a single architecture is the defining open problem in world model research today.**"

換句話說，「融合」不是技術上的必然，而是**尚未被解決的張力**。
渲染器泡在網際網路影片裡，模擬器與規劃器卻面臨 3D 資產與機器人示範的急迫短缺；
用視覺美感最佳化，會犧牲機器人或高保真模擬所需的精度。
「1＋2 融合」的樂觀，應該配上這個不確定性。

---

## 六、XR 與世界模型的關係

<!-- FIG3 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 720" role="img" aria-label="XR 與世界模型：雙向饋送與短期交會點｜互供資料與場景，技術目標不同" style="width:100%;height:auto;display:block">
<defs><marker id="m2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker><marker id="mc084fc" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#c084fc"/></marker><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="938.5" height="718.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">XR 與世界模型：雙向饋送與短期交會點</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">互供資料與場景，技術目標不同</text>
<rect x="48" y="116" width="380" height="250" rx="14" fill="#1c2230" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="74" y="152" font-size="17" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">XR 成就世界模型</text>
<text x="74" y="176" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">資料與場景的來源</text>
<rect x="74" y="194" width="328" height="46" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="90" y="214.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">VR／AR 與遙操作</text>
<text x="90" y="235.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">帶位姿、深度、互動標記的資料</text>
<rect x="74" y="248" width="328" height="46" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="90" y="268.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">掃描重建與數位孿生</text>
<text x="90" y="289.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">大量真實空間的對應關係</text>
<rect x="74" y="302" width="328" height="46" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<text x="90" y="322.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">人類在其中的操作</text>
<text x="90" y="343.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">動作—結果對的天然來源</text>
<rect x="488" y="116" width="380" height="250" rx="14" fill="#1c2230" stroke="#c084fc66" stroke-width="1.5"/>
<text x="514" y="152" font-size="17" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">世界模型成就 XR</text>
<text x="514" y="176" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">即時想像與互動結果</text>
<rect x="514" y="194" width="328" height="46" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="530" y="214.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">即時想像物件反應</text>
<text x="530" y="235.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不只渲染預先建好的場景</text>
<rect x="514" y="248" width="328" height="46" rx="10" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<text x="530" y="268.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">填補未拍攝區域</text>
<text x="530" y="289.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">生成一致的新視角</text>
<rect x="514" y="302" width="328" height="46" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="530" y="322.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">互動結果可驗證</text>
<text x="530" y="343.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">動作條件化的未來</text>
<path d="M 432 200 L 484 200" fill="none" stroke="#2dd4bf" stroke-width="3" marker-end="url(#m2dd4bf)"/>
<path d="M 484 282 L 432 282" fill="none" stroke="#c084fc" stroke-width="3" marker-end="url(#mc084fc)"/>
<text x="458" y="180" font-size="11.5" fill="#2dd4bf" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">資料</text>
<text x="458" y="306" font-size="11.5" fill="#c084fc" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">模型</text>
<text x="48" y="412" font-size="16" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">短期最實際的交會點：三層分工</text>
<text x="48" y="436" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">不是誰取代誰，而是各自負責一層</text>
<rect x="48" y="452" width="268" height="92" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="64" y="495.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">視覺與幾何底座</text>
<text x="64" y="516.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4DGS／NeRF 類重建</text>
<rect x="330" y="452" width="268" height="92" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="346" y="495.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">可控接觸與碰撞</text>
<text x="346" y="516.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">物理引擎（碰撞體、材質）</text>
<rect x="612" y="452" width="268" height="92" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="628" y="495.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">真實動態與長時程</text>
<text x="628" y="516.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">世界模型補足預測</text>
<path d="M 320 498 L 326 498" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 602 498 L 608 498" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="566" width="836" height="132" rx="12" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="72" y="596" font-size="14.5" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2026 年已落地：Spark 2.0（世界模型 → XR 的箭頭）</text>
<text x="72" y="622" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3DGS renderer，跑在 THREE.js / WebGL2，任何瀏覽器裝置（含 iOS、Android、VR）</text>
<text x="72" y="644" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Level-of-Detail 系統隨移動調整細節並串流；.RAD 格式支援漸進式精緻化</text>
<text x="72" y="666" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">固定 GPU 記憶體即可走訪「無限」splat 世界；實例逾 1 億 splats，</text>
<text x="72" y="688" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">實景掃描 4,000 萬 splats 在手機順暢，且相容 Quest 與 Vision Pro</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 3：XR 與世界模型的雙向饋送，以及三層分工的交會點｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG3 -->

不是單向的「世界模型成就 XR」：

- **XR 成就世界模型**：VR／AR、機器人遙操作、掃描重建與數位孿生會產生大量帶位姿、深度、互動標記的資料；
  這些是訓練空間與因果世界模型的重要燃料。
- **世界模型成就 XR**：未來 XR 不只渲染預先建好的場景，
  而能根據使用者動作即時「想像」物件反應、填補未拍攝區域、生成一致的新視角與互動結果。

**短期最實際的交會點**：4DGS／NeRF 類重建提供視覺與幾何底座，
物理引擎提供可控的接觸與碰撞，世界模型負責補足真實動態與長時程預測。

這個交會點已經不是概念，而是有具體工程形態的產品。**Spark 2.0**（2026 年 4 月）是 3DGS renderer，
跑在 THREE.js / WebGL2 上，**在任何有瀏覽器的裝置執行，包括 iOS、Android 與 VR**。
它的 Level-of-Detail 系統會隨著你在世界中移動，自動調整 3DGS 細節層級並從網路串流所需資料；
新的 `.RAD` 檔案格式支援漸進式精緻化；
virtual splat paging 則讓**固定的 GPU 記憶體配置**就能走訪「無限」大小的 splat 世界。
實例包括：Starspeed 在瀏覽器直接串流**逾 1 億 splats** 的公里級科幻環境；
以及另一個 4,000 萬 splats 的實景掃描專案，在手機上順暢執行且**相容 Quest 與 Vision Pro**。

這就是「XR 建模」那一列的輸出，正在被世界模型的消費端直接驅動。
**世界模型成就 XR** 這條箭頭，現在有了產品級的證據。

另一端則是 **World API**（2026 年 1 月）：從文字、單張影像、多圖組、360° 全景或影片生成可瀏覽的 3D 世界，
可直接在瀏覽器渲染，或匯入下游工具。在機器人與模擬領域，這些世界可直接整合進
**NVIDIA Isaac Sim、MuJoCo、RoboSuite** 等現代模擬器——
亦即「世界模型產生的場景 → 物理引擎接手 → 機器人策略訓練」這條鏈路，已經是可用 API 呼叫的產品。

> [Streaming 3DGS worlds on the web](https://www.worldlabs.ai/blog/spark-2.0) ｜
> [Announcing the World API](https://www.worldlabs.ai/blog/announcing-the-world-api)

---

## 七、一句話總結

**XR 是「把世界呈現給人」，世界模型是「把世界變成 AI 可預測、可規劃的內部狀態」；
4DGS 是後者可用的空間表徵之一，但不是世界模型本身。**

而 2026 年最重要的兩件事，恰好各佔這句話的一半：**AMD 收下 World Labs**，
說明世界模型已經緊密到需要與硬體垂直整合；
**R2S2R 用 2,000 次模擬預測 100 次真實試驗的 policy 排名**，
說明「可規劃的內部狀態」第一次真的開始兌現。

---

## 八、引用更正：三處需要說明的地方

這篇在整理一手來源時，發現流通版本裡有三處引用與原文不符，列出來供讀者判斷：

1. **「成熟系統五項條件」並非李飛飛原文的 checklist。**
   該篇〈A Functional Taxonomy of World Models〉的實際結構是
   POMDP 迴路 → 三種功能 → 為何 simulation 是 linchpin → 邊界消融 → 統一世界模型 + 資料不對稱，
   全文沒有編號清單，也沒有「spatial consistency」「uncertainty」這類字眼。
   本文第五節的五點是筆者綜合歸納，已明確標註。

2. **「物理引擎 vs 學出來的模擬器」這個對比不出自 Ying Wen 那篇。**
   〈What Is a World Model Modeling?〉的核心框架是 Tri-World Model
   （W1 Interactive Objective World / W2 Subjective World Model / W3 External Knowledge World）
   與 CCC（Capability Compounding Coefficient），主張「prediction is only the first step」，
   真正難的是決定哪些未來資訊該保留、哪些該丟棄。
   本文的「隱式模擬器可能出錯」改掛 Fei-Fei Li 原句（AI 生成幾何 self-intersection／尺度錯誤），
   論點不變但來源正確。

3. **`worldlabs.ai/blog/atlas` 現已指向 2026-09-01 的新一代 Atlas**，
   不是 2025 年那版「單圖生成 3D 並轉 Gaussian splats」的描述。
   「輸出 splats 與 collider mesh」這件事屬於 Marble，其實際輸出格式見第一節。

另附：V-JEPA 論文的正確 arXiv 編號是 **2404.08471**（不是 2404.08485，後者是無關的數值分析論文）。

---

### 引用來源

- **World Labs**：[World Labs is Joining AMD](https://www.worldlabs.ai/blog/amd-announcement) ｜
  [To Seek a Newer World](https://drfeifei.substack.com/p/worldlabs-joining-amd) ｜
  [Atlas](https://www.worldlabs.ai/blog/atlas) ｜
  [Marble](https://www.worldlabs.ai/blog/marble-world-model) ｜
  [Export file specs](https://docs.worldlabs.ai/marble/export/specs) ｜
  [Building Worlds That Train Robots](https://www.worldlabs.ai/blog/real-to-sim-to-real) ｜
  [World Labs Acquires SceniX](https://www.worldlabs.ai/blog/scenix) ｜
  [Spark 2.0](https://www.worldlabs.ai/blog/spark-2.0) ｜
  [World API](https://www.worldlabs.ai/blog/announcing-the-world-api)
- **Fei-Fei Li**：[A Functional Taxonomy of World Models](https://drfeifei.substack.com/p/a-functional-taxonomy-of-world-models)
- **Meta**：[V-JEPA 2 and new benchmarks for physical reasoning](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/) ｜
  [I-JEPA](https://arxiv.org/abs/2301.08243) ｜ [V-JEPA](https://arxiv.org/abs/2404.08471)
- **Yann LeCun**：[A Path Towards Autonomous Machine Intelligence](https://openreview.net/pdf?id=BZ5a1r-kVsf)
- **Ying Wen**：[What Is a World Model Modeling?](https://yingwen.io/en/blog/what-is-a-world-model-modeling/)

  每個 checkpoint 跑 2,000 次模擬（1,000 ID + 1,000 OOD）對照 100 次真實試驗（50 ID + 50 OOD）
- **失敗模式對齊**：不只重現最終的成功標籤，
  連「接近失敗邊界時的行為與結果」都在模擬與真實中一致出現

而且原文直接回扣那篇分類學：「In our taxonomy of world models, we called the simulator
**the linchpin**」——模擬器是樞紐。

> [World Labs Acquires SceniX](https://www.worldlabs.ai/blog/scenix) ｜
> [Building Worlds That Train Robots](https://www.worldlabs.ai/blog/real-to-sim-to-real)

另一條線上的對照組是 V-JEPA 2：1.2B 參數，**超過 100 萬小時影片**做無動作預訓練，
再用**僅 62 小時機器人資料**做動作條件化訓練，便可用於零樣本規劃。
方法是在 latent space 裡讓預測器想像候選動作的後果並評分，再用 model-predictive control 每步重規劃。
**對新物體、新環境的取放任務成功率 65%–80%**，且不需要針對特定機器人與部署環境的訓練資料。

> [Introducing the V-JEPA 2 world model](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/)

這組數據比任何論證都更清楚地說明：**「能生成漂亮、連貫的影片」與「理解世界如何回應動作」之間，
隔著一道至今未被跨越的鴻溝。** 整個世界模型領域的存在理由，就是為了填這道溝。

> [Introducing the V-JEPA 2 world model and new benchmarks for physical reasoning](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/) ｜
> [I-JEPA](https://arxiv.org/abs/2301.08243) ｜ [V-JEPA](https://arxiv.org/abs/2404.08471) ｜
> [A Path Towards Autonomous Machine Intelligence](https://openreview.net/pdf?id=BZ5a1r-kVsf)

而不是在渲染這一支上。「世界模型成就 XR」之所以成立，恰恰因為它先在機器人模擬這個非 XR 的場景裡
被逼出真實的因果與物理精度，然後那份精度反過來餵給 XR。

> [A Functional Taxonomy of World Models](https://drfeifei.substack.com/p/a-functional-taxonomy-of-world-models)
