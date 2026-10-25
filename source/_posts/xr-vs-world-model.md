---
title: XR 建模與世界模型：三種做出 3D 的方式，以及「理解」才是關鍵
date: 2026-10-26 15:30:00
categories:
  - AI 研究札記
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

![XR 建模與世界模型：三種做出 3D 的方式，以及「理解」才是關鍵](/img/covers/xr-vs-world-model.png)

> **XR 建模**和**物理 AI／世界模型**是兩條不同的技術路線，而且差別不在「做不做 3D」，
> 而在**做出來的是「模型」還是「理解」**。
>
> 這篇的核心論點只有一句：**世界模型不是用來重建場景的，是用來理解場景的。**
> 人看圖，AI 看特徵向量；把特徵向量解碼回圖片，只是為了讓人類能看懂並監督，
> 對 AI 自己的推理並不必要。
>
> 底下會先把「做出 3D」的三種方式分清楚——物理引擎建模、360 圖像縫合、4D Gaussian Splatting——
> 再說明為什麼世界模型走的是第三條，以及它真正要驗證的東西是什麼。
>
> 全文資料截至 2026-10-26，所有連結皆已逐一實測可存取。

<!-- more -->

## 一、「做出 3D」其實有三種方式

<!-- FIG1 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 700" role="img" aria-label="三種「做出 3D」的方式：物理引擎、360 縫合、4DGS｜世界模型走的是第三條" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="938.5" height="698.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">三種「做出 3D」的方式：物理引擎、360 縫合、4DGS</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">世界模型走的是第三條</text>
<rect x="48" y="118" width="264" height="330" rx="12" fill="#1c2230" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="68" y="152" font-size="15.5" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">物理引擎建模</text>
<text x="68" y="180" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">優點</text>
<text x="68" y="204" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・自帶力學方程、材質參數</text>
<text x="68" y="226" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・可自由走動、物件可互動</text>
<text x="68" y="264" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">代價</text>
<text x="68" y="288" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・仿真環境 ≠ 真實場景</text>
<text x="68" y="310" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・機器人因此才有 sim2real 問題</text>
<rect x="340" y="118" width="264" height="330" rx="12" fill="#1c2230" stroke="#f472b666" stroke-width="1.5"/>
<text x="360" y="152" font-size="15.5" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">360 圖像縫合 ＋ 視覺錯位</text>
<text x="360" y="180" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">優點</text>
<text x="360" y="204" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・就是拍到什麼就是什麼</text>
<text x="360" y="226" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・視覺上最接近真實</text>
<text x="360" y="264" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">代價</text>
<text x="360" y="288" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・只能看到全景相機走過的路徑</text>
<text x="360" y="310" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・離開拍攝路徑就沒東西看</text>
<rect x="632" y="118" width="264" height="330" rx="12" fill="#1c2230" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="652" y="152" font-size="15.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4D Gaussian Splatting</text>
<text x="652" y="180" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">優點</text>
<text x="652" y="204" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・把真實拍攝還原得像建模</text>
<text x="652" y="226" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・可自由走動，不受相機路徑侷限</text>
<text x="652" y="264" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">代價</text>
<text x="652" y="288" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・靠的是「場景理解」而非真建模</text>
<text x="652" y="310" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">・仍需物理引擎接手碰撞與互動</text>
<text x="48" y="482" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">世界模型走的是第三條：</text>
<text x="48" y="508" font-size="13.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">比仿真環境真實（直接來自真實拍攝），又不被相機路線侷限（AI 能想像沒走過的路）。</text>
<text x="48" y="534" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">但它產出的仍是「理解」——不是手算的力學結果，也不是像素級重建。</text>
<rect x="48" y="566" width="848" height="108" rx="12" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="72" y="598" font-size="14.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">為什麼 4DGS 和 360 縫合不是同一個東西</text>
<text x="72" y="624" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">360 縫合把多張照片拼成一張全景圖，畫面裡沒有深度，也沒有「這裡本來可能是什麼」。</text>
<text x="72" y="648" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4DGS 從多視角觀測學出一個可從新視角渲染的 3D 表徵，</text>
<text x="72" y="670" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">因此相機沒走過的路也可以渲染——那是從「場景理解」生出來的，不是拼圖補的。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：物理引擎建模、360 圖像縫合與 4D Gaussian Splatting 三種做 3D 的方式及其取捨｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG1 -->

談 XR 的時候，「建模」這個詞其實混了三件不同的事。它們的取捨完全不一樣，
而世界模型走的是第三種。

### 1.1 物理引擎建模

用遊戲引擎或專用模擬器搭出場景：自帶力學方程、材質參數、碰撞模型。
優點是**可自由走動、物件之間真的會互動**——你推杯子，杯子會照物理規則移動。

代價是**仿真環境不等於真實場景**。摩擦係數、接觸力、材料變形、光照、感測雜訊、
控制延遲，這些在真實世界裡的樣子，引擎裡都得靠人手工調參逼近。

這個差距有個非常具體的後果：**機器人之所以有 sim2real 問題，就是因為這個差距還沒被抹平。**
如果仿真環境夠真實，在仿真裡訓練的機器人早該直接突破部署了——事實上沒有，
所以差距依然存在，所有研究都在想辦法縮小它。

### 1.2 360 圖像縫合 ＋ 視覺錯位

另一條路是把多張照片縫成一張全景圖，再靠視覺錯位（stereo disparity）製造立體感。
優點是**畫面裡就是真實世界**，拍到什麼就是什麼。

代價是**你只能看到全景相機走過的路徑**。相機沒去過的地方，畫面上就沒有東西；
使用者移動時，視差也只能在拍攝當下的那幾個視角之間插值。

### 1.3 4D Gaussian Splatting

第三條路是從多視角觀測學出一個可從新視角渲染、且隨時間變化的 3D 場景表徵。

它跟 360 縫合**完全不是一個東西**：縫合是把照片拼成一張圖，畫面裡沒有深度、
也沒有「這裡本來可能是什麼」；4DGS 學到的是一個 3D 表徵，
所以**相機沒走過的路線也能渲染出來**。

它跟物理引擎建模也不同：物理引擎的場景是「算出來的」，4DGS 的場景是「從真實拍攝還原的」，
後者比前者真實。

### 1.4 世界模型走的是第三條

把三者的取捨排開來，世界模型的位置就清楚了：

| | 物理引擎建模 | 360 縫合 ＋ 視覺錯位 | 4DGS |
|---|---|---|---|
| 能不能自由走動 | 可以 | 不行，受相機路徑侷限 | 可以 |
| 內容有多真實 | 仿真，與真實有差距 | 就是真實 | 比仿真真實，來自真實拍攝 |
| 背後是什麼 | 手寫的力學方程 | 多張照片的拼接 | 從觀測學到的 3D 表徵 |

**世界模型要的是第三欄**——比仿真真實，又不受相機路線侷限，自由度高。
但關鍵在於：4DGS 靠的是「場景理解」，不是真的在建模。
它輸出的是從理解生出來的結果，不是手算的力學結果，也不是像素級重建。

這個取捨不是只有學術界在講。NVIDIA 的 DRIVE Sim 在 2022 年就明講：

> "Building scenes out of real-world data greatly reduces the sim-to-real gap."

而到了 2026 年，這條路線已經有完整系統了：NVIDIA Research 的 **SimFoundry**
把一段真實世界的影片自動變成可互動的模擬環境，作者名單裡有 Li Fei-Fei。
它用 3D Gaussian Splat 重建背景、用 2D-to-3D 生成模型補出物件 mesh，
最後在物理模擬器裡標註物理參數組成場景。實測結果：

- 用它重建的場景評估真實世界的 policy，**平均 Pearson 相關係數 0.911**
- 僅用模擬資料訓練的 policy，直接零樣本搬到真實世界，成功率 **100%**；
  換成真實世界才見過的物件，降到 **92%**
- 加上少量真實資料共同訓練，13 項任務的表現從 **28% 提升到 46%**
---

## 二、核心不是「重建」，是「理解」

<!-- FIG2 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 600" role="img" aria-label="人類看圖，AI 看特徵向量｜解碼只是為了讓人類能看懂並監督" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="938.5" height="598.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">人類看圖，AI 看特徵向量</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">解碼只是為了讓人類能看懂並監督</text>
<rect x="48" y="116" width="396" height="268" rx="14" fill="#1c2230" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="74" y="152" font-size="17" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">人類</text>
<text x="74" y="178" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">看的是圖本身</text>
<rect x="74" y="196" width="344" height="52" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="246.0" y="220.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">影像</text>
<text x="246.0" y="242.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">眼睛收到的光子</text>
<path d="M 246 252 L 246 274" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="74" y="278" width="344" height="52" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="246.0" y="302.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">場景</text>
<text x="246.0" y="324.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">杯子在那裡、可以拿起來</text>
<text x="74" y="362" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">看得懂，所以能判斷對不對。</text>
<rect x="480" y="116" width="396" height="268" rx="14" fill="#1c2230" stroke="#c084fc66" stroke-width="1.5"/>
<text x="506" y="152" font-size="17" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">AI</text>
<text x="506" y="178" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">看的是特徵向量</text>
<rect x="506" y="196" width="344" height="52" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="678.0" y="220.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">影像</text>
<text x="678.0" y="242.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">輸入的原始訊號</text>
<path d="M 678 252 L 678 274" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="506" y="278" width="344" height="52" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="678.0" y="302.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">特徵向量</text>
<text x="678.0" y="324.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">人看不懂，但那是 AI 的「理解」</text>
<text x="506" y="362" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">看不懂，但那是它做決策依據的東西。</text>
<rect x="48" y="412" width="828" height="150" rx="12" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="72" y="444" font-size="15" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">解碼器：唯一的目的，是讓人類能看懂並監督</text>
<text x="72" y="470" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">特徵向量 → 解碼回影像或文字，人類才能確認 AI 的理解跟自己的理解有沒有對齊。</text>
<text x="72" y="496" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">對 AI 本身而言，解碼是多餘的——它推理時用的是特徵空間，不是像素。</text>
<text x="72" y="528" font-size="13.5" fill="#fbbf24" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">所以 Yann LeCun 走隱式世界模型：人類幹嘛看懂？AI 看懂就好。</text>
<text x="72" y="552" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">AMI 論文：JEPA「在表徵空間做預測，讓編碼器能濾掉對任務無關的特徵」。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：人類看圖而 AI 看特徵向量，解碼器的唯一用途是讓人類能監督｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG2 -->

### 2.1 人類看圖，AI 看特徵向量

人類拿到一張影像，會直接看見場景：杯子在那裡、手可以碰到它、推一下它會往前動。

AI 不太一樣。影像進去之後會被編碼成一串特徵向量——
**那串向量才是 AI 對這張圖的「理解」**，而不是像素本身。
像素是給人看的，特徵向量是給機器用的。

那如果人看不懂特徵向量怎麼辦？解碼回來就好了。**但解碼的目的不是讓 AI 更強，
而是讓人類能看懂並監督**——確認 AI 的理解跟自己的理解有沒有對齊，
好去分析、去設計、去修正。

所以 Yann LeCun 走隱式世界模型的邏輯就很清楚：**人類幹嘛看懂？AI 看懂就好。**
解碼是給人用的接口，不是模型推理的必要步驟。

這在論文裡是明文的。〈Introduction to Latent Variable Energy-Based Models〉
（AMI，Dawid 與 LeCun，arXiv:2306.02572，後續發表於 *J. Stat. Mech.* 2024 104011）
在介紹 JEPA 時寫道：

> "Secondly, JEPAs make predictions in the **representation space**, allowing encoders to **remove irrelevant data features** for the task at hand."

在表徵空間做預測，讓編碼器能濾掉對任務無關的特徵——這就是「不預測像素」的完整理由。
同一篇論文把這種能力稱為 common sense，定義得很精確：

> "the ability to use models of the world to fill in information about the world that is unavailable from perception or memory (e.g., **to predict the future**)"

不是重建眼前有的東西，而是**補上感知與記憶拿不到的那部分資訊**。

### 2.2 所以要驗證的是「未來」，不是「場景」

這個區分有很實際的後果：**驗證一個世界模型，驗的不是它能不能重建場景，
而是它能不能正確預測出「未來場景」而且沒有幻覺。**

Meta 在 2025 年 6 月隨 V-JEPA 2 一併釋出三個物理推理基準，
就是照這個標準設計的：

- **IntPhys 2**：用遊戲引擎生成「物理被違反」的事件對，要模型指出哪一段發生違例
- **MVPBench**：最小差異影片對，專門對付語言模型的捷徑解讀
- **CausalVQA**：因果問答，含反事實、預測與規劃三類

結果：**人類在這三項都有 85%–95% 的準確率，而包括 V-JEPA 2 在內的頂尖模型與人類有顯著差距。**
IntPhys 2 上「current video models are at or close to chance」。

如果驗證標準是「能不能重建場景」，這些模型早就滿分通過了——
它們生成漂亮、連貫的影片比誰都強。**它們缺的正是那條鴻溝。**

V-JEPA 2 的做法也印證了這點：1.2B 參數，**超過 100 萬小時影片**做無動作預訓練，
再用**僅 62 小時機器人資料**做動作條件化訓練。它不是去重建場景，
而是在 latent space 裡讓預測器想像候選動作的後果並評分，再用 model-predictive control 每步重規劃。
**對新物體、新環境的取放任務成功率 65%–80%。**

V-JEPA 論文本身也明言，訓練過程「without the use of pretrained image encoders,
text, negative examples, **reconstruction**, or other sources of supervision」。

### 2.3 跟人類一樣：預判是在腦中想像的

人類預測未來，也不是真的拿著物理引擎去算方程。
看到一杯水傾倒過來，你是在腦中想像它會怎麼倒——那個「想像」也不是像素級重建，
更不是力學模擬，而是一個足以讓你做出反應的內部狀態。

AI 的情況完全一樣：它真正的輸出也是特徵向量。
人類想看到渲染結果，所以讓 AI 把特徵向量解碼出來做端到端輸出——
但那是給人看的，不是它推理時用的東西。

**世界模型的真正對象是「理解」，不是「模型」。**
一個世界模型可以完全沒有物理引擎、沒有 3D 表徵、沒有解碼器，
只要它內部有一個準確預測未來的狀態，那它就是世界模型。
反過來，一個重建得pixel-perfect 但預測不了因果的系統，再精確也不是世界模型。

---

## 三、兩個分支，兩種驗證方式

<!-- FIG3 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 620" role="img" aria-label="世界模型的兩個分支：因果理解與場景理解｜各自的驗證方式，以及融合的門檻" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker><marker id="mc084fc" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#c084fc"/></marker><marker id="m2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker></defs>
<rect x="0.75" y="0.75" width="938.5" height="618.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">世界模型的兩個分支：因果理解與場景理解</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">各自的驗證方式，以及融合的門檻</text>
<rect x="48" y="116" width="404" height="268" rx="14" fill="#1c2230" stroke="#c084fc66" stroke-width="1.5"/>
<text x="74" y="152" font-size="17" fill="#c084fc" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">分支一：因果理解</text>
<text x="74" y="178" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">AI 知道手去碰杯子，杯子會往前動</text>
<rect x="74" y="196" width="352" height="52" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="250.0" y="220.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">動作 a</text>
<text x="250.0" y="242.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">推一下、抓起來、放開</text>
<path d="M 250 252 L 250 274" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="74" y="278" width="352" height="52" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="250.0" y="302.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">預測的未來狀態</text>
<text x="250.0" y="324.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">還沒發生的事</text>
<text x="74" y="362" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">驗證：能不能正確預測未來，而沒有幻覺。</text>
<rect x="468" y="116" width="428" height="268" rx="14" fill="#1c2230" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="494" y="152" font-size="17" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">分支二：場景理解</text>
<text x="494" y="178" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">AI 知道相機沒走過的那條路長什麼樣</text>
<rect x="494" y="196" width="376" height="52" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="682.0" y="220.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">目前位置與已見場景</text>
<text x="682.0" y="242.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">從多視角觀測學到的表徵</text>
<path d="M 682 252 L 682 274" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="494" y="278" width="376" height="52" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="682.0" y="302.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">沒拍過的路線</text>
<text x="682.0" y="324.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">新視角、新區域</text>
<text x="494" y="362" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">驗證：相機沒拍到的路線，能不能正確想像出來。</text>
<path d="M 252 392 L 252 424" fill="none" stroke="#c084fc" stroke-width="3" marker-end="url(#mc084fc)"/>
<path d="M 682 392 L 682 424" fill="none" stroke="#2dd4bf" stroke-width="3" marker-end="url(#m2dd4bf)"/>
<text x="266" y="414" font-size="12" fill="#c084fc" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">因果</text>
<text x="696" y="414" font-size="12" fill="#2dd4bf" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">場景</text>
<rect x="48" y="428" width="848" height="168" rx="12" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<text x="72" y="460" font-size="16" fill="#3fb950" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">成熟條件：兩者融合，而且沒有幻覺、兩者不衝突</text>
<text x="72" y="490" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只懂因果 → 會推得動杯子，但不知道杯子長什麼樣、擺在哪裡。</text>
<text x="72" y="514" font-size="13" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只懂場景 → 知道場景長什麼樣，但不知道推一下會怎樣。</text>
<text x="72" y="544" font-size="13.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩者融合後，AI 依當前位置同時想像出場景與因果，才算真正成熟的理解。</text>
<text x="72" y="574" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">「沒有幻覺」與「不衝突」是門檻：預測得漂亮但物理錯，或場景對但因果打架，都還沒到位。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 3：因果理解與場景理解兩分支的驗證方式，以及兩者融合的成熟條件｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG3 -->

世界模型要回答的問題其實有兩個，兩者驗證的東西完全不同。

### 3.1 分支一：因果理解

**AI 知道手去碰杯子，杯子會往前動。**

這是物理反應與因果關係的理解——不是場景長什麼樣，而是**做了某個動作之後會怎樣**。
形式上就是一個預測函數：

\[ \hat{s}_{t+1} = f(s_t, a_t) \]

其中 $s_t$ 是目前狀態或其潛在表徵，$a_t$ 是動作，$\hat{s}_{t+1}$ 是對未來狀態的預測。

**驗證方式：能不能正確預測出「還沒發生的事」，而且沒有幻覺。**
這一點李飛飛在分類學裡講得很直白：

> "Generative simulators introduce a new risk on top of that: AI-generated geometry can look correct while containing self-intersections or wrong scale that produce nonsensical physics."

這就是隱式模擬器最危險的地方——**視覺正確、物理錯誤，而且不會以崩潰的形式提示你。**

### 3.2 分支二：場景理解

**AI 知道相機沒走過的那條路長什麼樣。**

這一分支不談物理與因果，而是要建立 3D 場景的內部表徵，
讓 AI 能在**沒有拍到過**的地方推論出合理的樣子。

**驗證方式：相機沒拍到的路線，AI 能不能正確想像出來。**

這裡 4DGS 的價值就清楚了：它之所以能渲染相機沒走過的路，
不是因為它「建模」了，而是因為它從多視角觀測學到的表徵裡，
**已經包含了對場景結構的推論能力**。

### 3.3 融合：成熟條件

單有任一分支都不夠：

- **只懂因果** → 會推得動杯子，但不知道杯子長什麼樣、擺在哪裡
- **只懂場景** → 知道場景長什麼樣，但不知道推一下會怎樣

AI 依當前位置**同時想像出場景與因果**，才是完整的理解。

但融合還不夠，**成熟還需要兩個額外條件**：

1. **沒有幻覺**——預測得漂亮但物理錯，不算
2. **兩者不衝突**——場景對但因果打架，同樣不算

這兩點是硬門檻，不是修辭。

### 3.4 李飛飛的三種功能，對應到這個架構

她在〈A Functional Taxonomy of World Models〉裡把世界模型拆成三種功能，
這三種其實正好可以用上面的框架來定位：

- **Renderer**：輸出給人看的像素，重視視覺保真度
- **Simulator**：輸出幾何、物理與動力學上可信的 state，供人和程式共同計算與互動
- **Planner**：輸入觀測與目標，輸出動作，閉合感知—行動迴路

她自己的定位是：

> "Of the three categories, the simulator gets the least public attention, and is the most consequential of the three."

以及她指出的最終形態：

> "**The logical endpoint is a unified world model**: one foundation model that can render photorealistic views, produce physically accurate structure, and plan action sequences, switching between output modalities depending on what the downstream consumer needs."

以及那個至今未解的張力：

> "The data picture is uneven, with renderers awash in internet video while simulators and planners face acute shortages of 3D assets and robot demonstrations. Optimizing for visual beauty can sacrifice the precision a robot or a high-fidelity simulation needs. **Reconciling these tensions inside a single architecture is the defining open problem in world model research today.**"

這句話正好點出融合的困難所在：渲染器泡在網際網路影片裡，
模擬器與規劃器卻面臨 3D 資產與機器人示範的急迫短缺。
---

## 四、2026 年的現況：三件事把這個框架推到了實證階段

### 4.1 World Labs 併入 AMD

2026 年 9 月 28 日，World Labs 簽署最終協議併入 AMD，交易預計 2026 年底前完成（需監管批准）。
Fei-Fei Li 將擔任 AMD **Executive Vice President and Chief Scientist**，直接向 Lisa Su 匯報；
Justin Johnson 與 Ben Mildenhall 留任，持續帶領 World Labs 團隊。
官方給出的理由是「scaling our efforts, scaling our reach, and **getting closer to the hardware**」。

這件事本身就是「世界模型走到硬體層」的訊號：**模型的瓶頸已經不在算法，而在算力、延遲與部署形態。**

> [World Labs is Joining AMD](https://www.worldlabs.ai/blog/amd-announcement) ｜
> [Fei-Fei Li：To Seek a Newer World](https://drfeifei.substack.com/p/worldlabs-joining-amd)

### 4.2 新一代 Atlas：從重建走向想像

2026 年 9 月 1 日，World Labs 發布新一代 **Atlas**——一個**多模態自迴歸 diffusion transformer**，
從零預訓練，原生處理 text、images、video、3D，所有輸入被編碼進共享的 **spatial context**。
關鍵設計是「每張參考影像都被錨定在空間中的 3D 位置」。

四類任務裡，最能說明本文框架的是兩項：

- **Camera-Controlled Generation**：精準的相機幾何作為**原生輸入型別**（非文字提示），
  從一張到六張參考圖生成最高 1 分鐘、1440p 的影片；
  官方說明是「match the content and geometry of the input images, smoothly extrapolating beyond them
  to **imagine parts of the scene not visible in the inputs**」
- **Space-Time Simulation**：從影片建模時空，支援機器人的 Real-to-Sim 工作流

另外 **Spatial Reconstruction** 在 pointmap error 基準上超越 VGGT-Ω、Depth Anything 3、
MapAnything、π³ 等專職重建模型（平均 8.6，優於次佳的 9.7）。

這裡有個值得注意的細節：新一代 Atlas 的架構是**生成模型**而不是重建模型。
它的輸出是從理解生出來的結果——這正好印證第一節的結論：
**它不是在做建模，是在做理解。**

> [Atlas: A World Model for Spatial Intelligence](https://www.worldlabs.ai/blog/atlas)

### 4.3 R2S2R：驗證的是「能不能預測真實效能」

2026 年 7 月 21 日 World Labs 併購機器人與模擬公司 SceniX；7 月 28 日發表
**R2S2R（Real-to-sim-to-real）** 成果。做法是：把真實任務重建為互動式模擬，
然後系統性變換外觀、物件配置、雜物、**物理參數**、機器人狀態與相機視角，產生數千個變體。

報告的結果：

- **零真實世界訓練資料**學會複雜操作任務
- **模擬能預測真實效能**：跨 policy 架構、跨 checkpoint，模擬評測**保留真實世界的效能排名**，
  追蹤改進與停滯，並重現相同的成功／失敗空間分佈。
  每個 checkpoint 跑 2,000 次模擬（1,000 ID + 1,000 OOD）對照 100 次真實試驗（50 ID + 50 OOD）
- **失敗模式對齊**：不只重現最終的成功標籤，
  連「接近失敗邊界時的行為與結果」都在模擬與真實中一致出現

注意這三項驗證的**都不是重建品質**，而是「對未來的預測準不準」以及「預測與真實是否一致」。
而且失敗模式能對齊這件事，只有在模型真的學到了因果與動力學時才會發生——
渲染得再像，失敗的時機與型態也不會對得上。

原文也直接回扣那篇分類學：「In our taxonomy of world models, we called the simulator
**the linchpin**」——模擬器是樞紐。

> [World Labs Acquires SceniX](https://www.worldlabs.ai/blog/scenix) ｜
> [Building Worlds That Train Robots](https://www.worldlabs.ai/blog/real-to-sim-to-real)

用視覺美感最佳化，會犧牲機器人或高保真模擬所需的精度。

**融合不是技術上的必然，而是尚未被解決的張力。**

> [A Functional Taxonomy of World Models](https://drfeifei.substack.com/p/a-functional-taxonomy-of-world-models)

> [Introduction to Latent Variable Energy-Based Models](https://arxiv.org/abs/2306.02572) ｜
> [I-JEPA](https://arxiv.org/abs/2301.08243) ｜ [V-JEPA](https://arxiv.org/abs/2404.08471) ｜
> [Introducing the V-JEPA 2 world model](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/)

---

## 五、成熟之後，XR 會變成什麼

### 5.1 世界模型成熟後能成就 XR，XR 成就不了世界模型

這是整篇文章最實際的結論，也是兩條路線最不對稱的地方。

**世界模型能成就 XR**，因為一旦 AI 真的擁有因果理解與場景理解，
XR 內容的生產方式就整個改變：

- 不需要先建模再渲染，而是**由理解直接生出結果**
- 使用者往前走，系統即時「想像」出還沒看到的部分，而不是播放預先算好的動畫
- 互動結果是**動作條件化**的——同一個場景，推一下和拉一下，結果不同

而 **XR 成就不了世界模型**，因為 XR 產生的資料只有「看見什麼」，
沒有「做了什麼之後會怎樣」。掃描重建能給你很精確的幾何，
但給不了你「推一下杯子它會怎麼動」。

資料可以流動，但能力的缺口補不上。**這是技術路線的差異，不是投入程度的差異。**

### 5.2 已經在發生的基礎建設

兩件事說明這條路不是空想：

**Spark 2.0**（2026 年 4 月）是 3DGS renderer，跑在 THREE.js / WebGL2 上，
**在任何有瀏覽器的裝置執行，包括 iOS、Android 與 VR**。
它的 Level-of-Detail 系統會隨著使用者在世界中移動，自動調整 3DGS 細節層級並從網路串流所需資料；
新的 `.RAD` 檔案格式支援漸進式精緻化；
virtual splat paging 則讓**固定的 GPU 記憶體配置**就能走訪「無限」大小的 splat 世界。
實例包括：Starspeed 在瀏覽器直接串流**逾 1 億 splats** 的公里級科幻環境；
以及另一個 4,000 萬 splats 的實景掃描專案，在手機上順暢執行且**相容 Quest 與 Vision Pro**。

**World API**（2026 年 1 月）：從文字、單張影像、多圖組、360° 全景或影片生成可瀏覽的 3D 世界，
可直接在瀏覽器渲染，或匯入下游工具。在機器人與模擬領域，
這些世界可直接整合進 **NVIDIA Isaac Sim、MuJoCo、RoboSuite** 等現代模擬器。

還有一個細節值得注意：Marble 的實際輸出把視覺與物理**刻意分開**——
splat 有 SPZ 與 PLY 兩種（約 200 萬與 50 萬 splats），
mesh 則分為 **Collider Mesh**（GLB，10–20 萬三角形，官方措辭是「optimized for simple physics calculations」）
與 HQ Mesh（約 60 萬–100 萬三角形，含貼圖或頂點色）。

**collider mesh 是給物理引擎用的粗略碰撞體，不是高精度幾何。**
這個設計本身就說明一件事：視覺保真與物理可用是兩件不同的事，
而生成式模型產出的東西，要真的拿來做互動，物理那一層仍然得交給專業的物理引擎。

> [Streaming 3DGS worlds on the web](https://www.worldlabs.ai/blog/spark-2.0) ｜
> [Announcing the World API](https://www.worldlabs.ai/blog/announcing-the-world-api) ｜
> [Marble: A Multimodal World Model](https://www.worldlabs.ai/blog/marble-world-model) ｜
> [Export file specs](https://docs.worldlabs.ai/marble/export/specs)

---

## 六、一句話總結

**XR 是「把世界呈現給人」，世界模型是「把世界變成 AI 可預測、可規劃的內部狀態」。
4DGS 是後者可用的空間表徵之一，但它本身不是世界模型——
因為它輸出的是理解，不是建模。**

而 2026 年最重要的兩件事，恰好各佔這句話的一半：
**AMD 收下 World Labs**，說明世界模型已經緊密到需要與硬體垂直整合；
**R2S2R 用 2,000 次模擬預測 100 次真實試驗的 policy 排名**，
說明「可規劃的內部狀態」第一次真的開始兌現。

成熟的世界模型，是**因果理解與場景理解的融合**，而且沒有幻覺、兩者不衝突。

---

## 七、引用說明與勘誤

### 7.1 第五節與第四節的幾點是本文歸納

第三節那五項條件、第四節的分支架構，都是綜合上述框架與各節證據後的歸納，
並非任一單一原文的 checklist。

〈A Functional Taxonomy of World Models〉的實際結構是：
POMDP 迴路 → 三種功能（Renderer／Simulator／Planner）→ 為何 simulation 是 linchpin →
三者邊界消融 → 統一世界模型的最終形態，加上資料不對稱的挑戰。

### 7.2 「物理引擎 vs 學出來的模擬器」的出處

這個對比在第三節，其依據是 Fei-Fei Li 在同一篇分類學裡的這句：

> "Generative simulators introduce a new risk on top of that: AI-generated geometry can look correct while containing self-intersections or wrong scale that produce nonsensical physics."

### 7.3 Atlas 這條線的版本差異

`worldlabs.ai/blog/atlas` 現已指向 2026-09-01 發布的新一代 Atlas
（多模態自迴歸 diffusion transformer）。2025 年版的重點是單張圖生成 3D 場景，
與現在的架構不同——引用時需留意所指的是哪一版。

「輸出 splats 與 collider mesh」這件事屬於 Marble，其實際輸出格式見第五節。

### 7.4 一個容易誤植的 arXiv 編號

V-JEPA 論文（*Revisiting Feature Prediction for Learning Visual Representations from Video*）
的 arXiv 編號是 **2404.08471**，搜尋時容易誤植成 2404.08485——
後者是另一篇無關的數值分析論文。

另註：〈A Path Towards Autonomous Machine Intelligence〉的 arXiv 版本
標題為 *Introduction to Latent Variable Energy-Based Models*，
作者是 **Anna Dawid 與 Yann LeCun**（arXiv:2306.02572，2023-06-05，
後續發表於 *J. Stat. Mech.* 2024 104011），不是 LeCun 獨著。

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
- **Yann LeCun / Anna Dawid**：[Introduction to Latent Variable Energy-Based Models: A Path Towards Autonomous Machine Intelligence](https://arxiv.org/abs/2306.02572)
- **NVIDIA Research**：[SimFoundry](https://research.nvidia.com/labs/gear/simfoundry/) ｜
  [Reconstructing the Real World in DRIVE Sim With AI](https://blogs.nvidia.com/blog/drive-sim-neural-reconstruction-engine/)


這正是「用真實拍攝重建模擬，比從零建構的模擬更接近真實」這件事的量化版本。

> [SimFoundry: Modular and Automated Scene Generation for Policy Learning and Evaluation](https://research.nvidia.com/labs/gear/simfoundry/) ｜
> [Reconstructing the Real World in DRIVE Sim With AI](https://blogs.nvidia.com/blog/drive-sim-neural-reconstruction-engine/)
