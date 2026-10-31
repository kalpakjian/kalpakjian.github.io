---
archive: true   # 已歸入 /cnn/ 專題目錄，不列在首頁
title: CNN I：機器怎麼「看」？從視覺皮層到 LeNet-5 的 61,750 個參數
date: 2026-10-27 14:30:00
categories:
  - AI
  - 技術筆記
tags:
  - CNN
  - 卷積神經網絡
  - 電腦視覺
  - LeNet-5
  - 參數共享
  - 感受野
  - 反向傳播
  - 深度學習
  - Qwen-Image
toc: true
index_img: /img/covers/cnn-1-convnet-neon.png
banner_img: /img/covers/cnn-1-convnet-neon-banner.png
---

> 📚 這篇文章已歸入主題目錄：[CNN 專題](/cnn/)（九篇圖解系列、課程筆記與實驗都在那裡）。

> <strong>整理說明</strong>：這是我上「卷積神經網絡（CNN）I」的課後筆記。36 頁課程簡報講的是很標準的一條線：影像為什麼是數字、視覺皮層的四層抽象、卷積的三條規則、LeNet-5、以及卷積的反向傳播。簡報本身有幾個數字我算不回去（1080×1080×3 的向量長度、86 億神經元的連線總數、LeNet-5 的參數總數），我把它們全部重算一次，列在 <a href="#errata">第 9 節</a>。文中每一個參數量與乘加次數都是我逐層手算、再寫程式覆核的；插圖是自己畫的 SVG（霓虹風），封面是本地 ComfyUI 跑 Qwen-Image 2.1 生成的。

<!-- more -->

## 先講結論

1. **影像不是「圖」，是一個 `H×W×C` 的整數陣列。** 1080p 彩色圖就是 3,499,200 個 `0–255` 的數字。把它攤平丟進全連接層，第一層就要 3.5×10⁹ 個參數（fp32 約 14 GB）—— 而且完全丟掉了「誰跟誰相鄰」。
2. **CNN 的全部主張只有一句話：不要把相鄰的像素拆散。** 用一個小窗口（濾波器）掃過整張圖，同一組權重在所有位置重複使用。
3. **「參數共享」不是為了省空間而已，它是一種假設**：同一種特徵無論出現在哪個位置都該被同一個偵測器認出來。這個假設讓樣本效率變好，也讓網路具有平移等變性。
4. **LeNet-5 只有 61,750 個參數**（1998 年，32×32 手寫數字）。同樣的輸入若要接一層 1,024→1,000 的全連接層，需要 1,025,000 個參數，是整張 LeNet-5 的 16.6 倍，而且什麼都還沒開始學。
5. **卷積的梯度還是卷積**：`∂L/∂W = X ⊛ G`、`∂L/∂X = G ⊛ rot180(W)`。權重共享的意思就是「所有位置的梯度要加總回同一組權重」。

| 這一講的四個模組 | 內容 |
| --- | --- |
| 1. 場景理解與物件辨識 | 錯覺、影像即數字、視覺皮層、抽象層 |
| 2. 古典機器視覺基礎 | 空間結構、patch、濾波器、卷積、特徵圖 |
| 3. CNN 基礎 | de novo 特徵學習、參數共享、LeNet-5、卷積反傳 |
| 4. 應用 | 語義分割、人臉、自駕、上色、超解析、醫學、基因組（本講只點名，未展開） |

## 1. 電腦「看」到的東西：一個三維整數陣列

一張 RGB 影像就是三個 `H×W` 的矩陣疊起來，每個元素是 `0–255` 的整數：

```
1080 × 1080 × 3  =  3,499,200 個數字   （彩色）
1080 × 1080      =  1,166,400 個數字   （灰階）
```

<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 480" role="img" aria-label="左邊 6×6 的像素值矩陣，經 flatten 攤平成右邊長達數百萬維的向量" style="width:100%;height:auto;display:block">
<defs>
<filter id="f1-glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="f1-soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="11" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="f1-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#1a2331" stroke-width="1"/></pattern>
<marker id="f1-arw-2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="478.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<rect x="0.75" y="0.75" width="958.5" height="478.5" rx="16" fill="url(#f1-grid)" opacity="0.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">一張圖就是一串數字</text>
<text x="48" y="80" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">像素是 0–255 的整數；RGB 圖是 H×W×3 的三維陣列</text>
<rect x="60.0" y="122.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="79.0" y="145.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">12</text>
<rect x="101.0" y="122.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="120.0" y="145.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">12</text>
<rect x="142.0" y="122.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="161.0" y="145.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">14</text>
<rect x="183.0" y="122.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="202.0" y="145.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">16</text>
<rect x="224.0" y="122.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="243.0" y="145.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">12</text>
<rect x="265.0" y="122.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="284.0" y="145.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">10</text>
<rect x="60.0" y="163.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="79.0" y="186.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">10</text>
<rect x="101.0" y="163.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="120.0" y="186.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">14</text>
<rect x="142.0" y="163.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="161.0" y="186.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">18</text>
<rect x="183.0" y="163.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="202.0" y="186.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">22</text>
<rect x="224.0" y="163.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="243.0" y="186.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">15</text>
<rect x="265.0" y="163.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="284.0" y="186.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">11</text>
<rect x="60.0" y="204.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="79.0" y="227.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">16</text>
<rect x="101.0" y="204.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="120.0" y="227.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">20</text>
<rect x="142.0" y="204.0" width="38.0" height="38.0" rx="5" fill="#f472b6" opacity="1.0" stroke="#22d3ee55" stroke-width="1" filter="url(#f1-glow)"/>
<text x="161.0" y="227.0" font-size="11.5" fill="#04141a" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">210</text>
<rect x="183.0" y="204.0" width="38.0" height="38.0" rx="5" fill="#22d3ee" opacity="1.0" stroke="#22d3ee55" stroke-width="1" filter="url(#f1-glow)"/>
<text x="202.0" y="227.0" font-size="11.5" fill="#04141a" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">230</text>
<rect x="224.0" y="204.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="243.0" y="227.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">24</text>
<rect x="265.0" y="204.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="284.0" y="227.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">12</text>
<rect x="60.0" y="245.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="79.0" y="268.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">12</text>
<rect x="101.0" y="245.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="120.0" y="268.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">18</text>
<rect x="142.0" y="245.0" width="38.0" height="38.0" rx="5" fill="#22d3ee" opacity="1.0" stroke="#22d3ee55" stroke-width="1" filter="url(#f1-glow)"/>
<text x="161.0" y="268.0" font-size="11.5" fill="#04141a" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">200</text>
<rect x="183.0" y="245.0" width="38.0" height="38.0" rx="5" fill="#f472b6" opacity="1.0" stroke="#22d3ee55" stroke-width="1" filter="url(#f1-glow)"/>
<text x="202.0" y="268.0" font-size="11.5" fill="#04141a" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">240</text>
<rect x="224.0" y="245.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="243.0" y="268.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">20</text>
<rect x="265.0" y="245.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="284.0" y="268.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">14</text>
<rect x="60.0" y="286.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="79.0" y="309.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">11</text>
<rect x="101.0" y="286.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="120.0" y="309.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">13</text>
<rect x="142.0" y="286.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="161.0" y="309.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">16</text>
<rect x="183.0" y="286.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="202.0" y="309.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">18</text>
<rect x="224.0" y="286.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="243.0" y="309.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">15</text>
<rect x="265.0" y="286.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="284.0" y="309.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">10</text>
<rect x="60.0" y="327.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="79.0" y="350.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">10</text>
<rect x="101.0" y="327.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="120.0" y="350.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">11</text>
<rect x="142.0" y="327.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="161.0" y="350.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">12</text>
<rect x="183.0" y="327.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="202.0" y="350.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">13</text>
<rect x="224.0" y="327.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="243.0" y="350.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">12</text>
<rect x="265.0" y="327.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="284.0" y="350.0" font-size="11.5" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">11</text>
<text x="60.0" y="388.0" font-size="12.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">6×6 示意（真實是 1080×1080×3）</text>
<text x="60.0" y="110.0" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">像素值</text>
<path d="M 332.0 222.0 L 430.0 222.0" fill="none" stroke="#2dd4bf" stroke-width="2.2" marker-end="url(#f1-arw-2dd4bf)"/>
<text x="381.0" y="210.0" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">flatten</text>
<rect x="452.0" y="206.0" width="452.0" height="32.0" rx="5" fill="#0f1a24" opacity="1.0" stroke="#22d3ee66" stroke-width="1.2"/>
<path d="M 452.0 210.0 L 452.0 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 459.4 210.0 L 459.4 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 466.8 210.0 L 466.8 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 474.2 210.0 L 474.2 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 481.6 210.0 L 481.6 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 489.0 210.0 L 489.0 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 496.4 210.0 L 496.4 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 503.8 210.0 L 503.8 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 511.2 210.0 L 511.2 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 518.6 210.0 L 518.6 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 526.0 210.0 L 526.0 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 533.4 210.0 L 533.4 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 540.8 210.0 L 540.8 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 548.2 210.0 L 548.2 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 555.6 210.0 L 555.6 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 563.0 210.0 L 563.0 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 570.4 210.0 L 570.4 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 577.8 210.0 L 577.8 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 585.2 210.0 L 585.2 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 592.6 210.0 L 592.6 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 600.0 210.0 L 600.0 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 607.4 210.0 L 607.4 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 614.8 210.0 L 614.8 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 622.2 210.0 L 622.2 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 629.6 210.0 L 629.6 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 637.0 210.0 L 637.0 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 644.4 210.0 L 644.4 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 651.8 210.0 L 651.8 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 659.2 210.0 L 659.2 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 666.6 210.0 L 666.6 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 674.0 210.0 L 674.0 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 681.4 210.0 L 681.4 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 688.8 210.0 L 688.8 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 696.2 210.0 L 696.2 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 703.6 210.0 L 703.6 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 711.0 210.0 L 711.0 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 718.4 210.0 L 718.4 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 725.8 210.0 L 725.8 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 733.2 210.0 L 733.2 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 740.6 210.0 L 740.6 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 748.0 210.0 L 748.0 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 755.4 210.0 L 755.4 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 762.8 210.0 L 762.8 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 770.2 210.0 L 770.2 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 777.6 210.0 L 777.6 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 785.0 210.0 L 785.0 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 792.4 210.0 L 792.4 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.55"/>
<path d="M 799.8 210.0 L 799.8 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.5270833333333333"/>
<path d="M 807.2 210.0 L 807.2 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.5041666666666667"/>
<path d="M 814.6 210.0 L 814.6 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.48125000000000007"/>
<path d="M 822.0 210.0 L 822.0 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.45833333333333337"/>
<path d="M 829.4 210.0 L 829.4 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.4354166666666667"/>
<path d="M 836.8 210.0 L 836.8 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.41250000000000003"/>
<path d="M 844.2 210.0 L 844.2 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.38958333333333334"/>
<path d="M 851.6 210.0 L 851.6 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.36666666666666675"/>
<path d="M 859.0 210.0 L 859.0 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.34375"/>
<path d="M 866.4 210.0 L 866.4 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.3208333333333333"/>
<path d="M 873.8 210.0 L 873.8 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.2979166666666667"/>
<path d="M 881.2 210.0 L 881.2 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.275"/>
<path d="M 888.6 210.0 L 888.6 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.2520833333333334"/>
<path d="M 896.0 210.0 L 896.0 234.0" fill="none" stroke="#22d3ee" stroke-width="1.2" opacity="0.22916666666666666"/>
<text x="900.0" y="194.0" font-size="13" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">3,499,200 維</text>
<text x="452.0" y="260.0" font-size="12.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">灰階 1080² = 1,166,400 維；RGB 再 ×3</text>
<text x="900.0" y="260.0" font-size="12" fill="#5d6b7d" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">0  1  2  …  255</text>
<path d="M 48.0 400.0 L 912.0 400.0" fill="none" stroke="#222b36" stroke-width="1.2" opacity="1.0"/>
<text x="48.0" y="430.0" font-size="14.5" fill="#fbbf24" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">攤平之後，「誰跟誰相鄰」這個資訊就不見了 —— 這正是 CNN 存在的理由。</text>
<text x="48.0" y="456.0" font-size="12.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">1080×1080×3 的圖只要接一層 1,000 單元的全連接層，就要 3.5×10⁹ 個參數（fp32 ≈ 14 GB）。</text>
</svg>
</figure>


把這個陣列 `flatten` 成一個向量，就得到一個長度 350 萬的輸入。問題是：**攤平的動作本身就是一種破壞**。原本 `(i, j)` 與 `(i, j+1)` 是鄰居，攤平之後它們只是索引 `k` 與 `k+1`，而神經網路沒有任何機制知道「相鄰」意味著什麼——除非你讓它從資料裡學，而那是非常沒效率的學法。

代價可以算出來：

```
輸入 3,499,200 維，接一層 1,000 單元的全連接層
參數 = 3,499,200 × 1,000 + 1,000 ≈ 3.50 × 10⁹
記憶體 = 3.50 × 10⁹ × 4 bytes ≈ 14.0 GB   （fp32，只有第一層）
```

14 GB 只夠放第一層的權重，而且這個網路對「貓往右移 10 個像素」毫無概念。所以簡報的那句結論其實是整堂課的動機：**利用影像的空間結構，學 patch，再把 patch 疊起來。**

## 2. 這不是比喻：視覺皮層本來就是分層的

CNN 的設計不是憑空發明，是照著視覺皮層畫的。課程簡報把皮層分成四段，每一段負責的「特徵」很清楚：

| 階段 | 全名 | 對什麼有反應 | 對應的網路層 |
| --- | --- | --- | --- |
| LGN | 外側膝狀體 | 小點、中心—環繞 | 輸入 / 第一層 |
| V1 | 初級視覺皮層 | 方向、視差、部分顏色 | Conv 1（邊緣） |
| V4 | 視覺皮層 V4 | 顏色、基本形狀、曲率 | Conv 2–3（紋理、部件） |
| VTC | 腹側顳葉皮層 | 複雜特徵、臉、物件 | FC（整體判別） |

<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 500" role="img" aria-label="左欄是 LGN、V1、V4、VTC 四層視覺皮層，右欄是 Conv1、Conv2、Conv3、FC，中間以約等號連接" style="width:100%;height:auto;display:block">
<defs>
<filter id="f2-glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="f2-soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="11" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="f2-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#1a2331" stroke-width="1"/></pattern>
<marker id="f2-arw-2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="498.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<rect x="0.75" y="0.75" width="958.5" height="498.5" rx="16" fill="url(#f2-grid)" opacity="0.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">眼睛和大腦：同一個階梯的兩種說法</text>
<text x="48" y="80" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">皮層的四層抽象 ↔ CNN 的四層特徵；這不只是比喻，是 LeNet 的設計來源</text>
<text x="96.0" y="112.0" font-size="13.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">生物視覺皮層</text>
<text x="864.0" y="112.0" font-size="13.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">CNN 的層</text>
<text x="480.0" y="112.0" font-size="13" fill="#8b949e" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">同一件事</text>
<rect x="60.0" y="130.0" width="300.0" height="58.0" rx="10" fill="#0f1720" opacity="1.0" stroke="#5d6b7d88" stroke-width="1.5"/>
<text x="78.0" y="156.0" font-size="16" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">LGN</text>
<text x="140.0" y="156.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">外側膝狀體</text>
<text x="78.0" y="175.0" font-size="12" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">小點、中心—環繞</text>
<circle cx="318" cy="153.0" r="2.6" fill="#5d6b7d"/><circle cx="330" cy="147.0" r="2.6" fill="#5d6b7d"/><circle cx="342" cy="155.0" r="2.6" fill="#5d6b7d"/><circle cx="324" cy="167.0" r="2.6" fill="#5d6b7d"/><circle cx="338" cy="168.0" r="2.6" fill="#5d6b7d"/><rect x="600.0" y="130.0" width="300.0" height="58.0" rx="10" fill="#0f1720" opacity="1.0" stroke="#22d3ee88" stroke-width="1.5" filter="url(#f2-glow)"/>
<text x="618.0" y="156.0" font-size="16" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">Conv 1</text>
<text x="700.0" y="156.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">3×3 / 5×5</text>
<text x="618.0" y="175.0" font-size="12" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">邊緣、暗點</text>
<circle cx="858" cy="153.0" r="2.6" fill="#22d3ee"/><circle cx="870" cy="147.0" r="2.6" fill="#22d3ee"/><circle cx="882" cy="155.0" r="2.6" fill="#22d3ee"/><circle cx="864" cy="167.0" r="2.6" fill="#22d3ee"/><circle cx="878" cy="168.0" r="2.6" fill="#22d3ee"/><path d="M 378.0 159.0 L 456.0 159.0" fill="none" stroke="#5d6b7d" stroke-width="1.6" opacity="0.75" stroke-dasharray="7 5"/>
<path d="M 504.0 159.0 L 588.0 159.0" fill="none" stroke="#5d6b7d" stroke-width="1.6" opacity="0.75" stroke-dasharray="7 5"/>
<text x="480.0" y="167.0" font-size="24" fill="#e6edf3" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">≈</text>
<rect x="60.0" y="202.0" width="300.0" height="58.0" rx="10" fill="#0f1720" opacity="1.0" stroke="#22d3ee88" stroke-width="1.5" filter="url(#f2-glow)"/>
<text x="78.0" y="228.0" font-size="16" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">V1</text>
<text x="140.0" y="228.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">初級視覺皮層</text>
<text x="78.0" y="247.0" font-size="12" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">方向、視差、部分顏色</text>
<path d="M 319 231.0 L 341 231.0" stroke="#22d3ee" stroke-width="2.6" fill="none" transform="rotate(-25 330 231.0)"/><path d="M 319 231.0 L 341 231.0" stroke="#22d3ee" stroke-width="2.6" fill="none" transform="rotate(0 330 231.0)"/><path d="M 319 231.0 L 341 231.0" stroke="#22d3ee" stroke-width="2.6" fill="none" transform="rotate(25 330 231.0)"/><rect x="600.0" y="202.0" width="300.0" height="58.0" rx="10" fill="#0f1720" opacity="1.0" stroke="#a78bfa88" stroke-width="1.5" filter="url(#f2-glow)"/>
<text x="618.0" y="228.0" font-size="16" fill="#a78bfa" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">Conv 2</text>
<text x="700.0" y="228.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">3×3 堆疊</text>
<text x="618.0" y="247.0" font-size="12" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">紋理、轉角</text>
<path d="M 859 231.0 L 881 231.0" stroke="#a78bfa" stroke-width="2.6" fill="none" transform="rotate(-25 870 231.0)"/><path d="M 859 231.0 L 881 231.0" stroke="#a78bfa" stroke-width="2.6" fill="none" transform="rotate(0 870 231.0)"/><path d="M 859 231.0 L 881 231.0" stroke="#a78bfa" stroke-width="2.6" fill="none" transform="rotate(25 870 231.0)"/><path d="M 378.0 231.0 L 456.0 231.0" fill="none" stroke="#22d3ee" stroke-width="1.6" opacity="0.75" stroke-dasharray="7 5"/>
<path d="M 504.0 231.0 L 588.0 231.0" fill="none" stroke="#22d3ee" stroke-width="1.6" opacity="0.75" stroke-dasharray="7 5"/>
<text x="480.0" y="239.0" font-size="24" fill="#e6edf3" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">≈</text>
<rect x="60.0" y="274.0" width="300.0" height="58.0" rx="10" fill="#0f1720" opacity="1.0" stroke="#a78bfa88" stroke-width="1.5" filter="url(#f2-glow)"/>
<text x="78.0" y="300.0" font-size="16" fill="#a78bfa" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">V4</text>
<text x="140.0" y="300.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">視覺皮層 V4</text>
<text x="78.0" y="319.0" font-size="12" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">顏色、基本形狀、曲率</text>
<path d="M 313 308.0 Q 322 288.0 330 300.0 Q 338 312.0 347 297.0" fill="none" stroke="#a78bfa" stroke-width="2.6"/><circle cx="330" cy="312.0" r="3.2" fill="#a78bfa" opacity="0.8"/><rect x="600.0" y="274.0" width="300.0" height="58.0" rx="10" fill="#0f1720" opacity="1.0" stroke="#f472b688" stroke-width="1.5" filter="url(#f2-glow)"/>
<text x="618.0" y="300.0" font-size="16" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">Conv 3</text>
<text x="700.0" y="300.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">3×3 堆疊</text>
<text x="618.0" y="319.0" font-size="12" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">部件：眼、耳、鼻</text>
<path d="M 853 308.0 Q 862 288.0 870 300.0 Q 878 312.0 887 297.0" fill="none" stroke="#f472b6" stroke-width="2.6"/><circle cx="870" cy="312.0" r="3.2" fill="#f472b6" opacity="0.8"/><path d="M 378.0 303.0 L 456.0 303.0" fill="none" stroke="#a78bfa" stroke-width="1.6" opacity="0.75" stroke-dasharray="7 5"/>
<path d="M 504.0 303.0 L 588.0 303.0" fill="none" stroke="#a78bfa" stroke-width="1.6" opacity="0.75" stroke-dasharray="7 5"/>
<text x="480.0" y="311.0" font-size="24" fill="#e6edf3" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">≈</text>
<rect x="60.0" y="346.0" width="300.0" height="58.0" rx="10" fill="#0f1720" opacity="1.0" stroke="#f472b688" stroke-width="1.5" filter="url(#f2-glow)"/>
<text x="78.0" y="372.0" font-size="16" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">VTC</text>
<text x="140.0" y="372.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">腹側顳葉皮層</text>
<text x="78.0" y="391.0" font-size="12" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">複雜特徵、臉、物件</text>
<circle cx="330" cy="375.0" r="15" fill="none" stroke="#f472b6" stroke-width="2.2"/><circle cx="325" cy="371.0" r="2.2" fill="#f472b6"/><circle cx="335" cy="371.0" r="2.2" fill="#f472b6"/><path d="M 324 381.0 Q 330 386.0 336 381.0" fill="none" stroke="#f472b6" stroke-width="2"/><rect x="600.0" y="346.0" width="300.0" height="58.0" rx="10" fill="#0f1720" opacity="1.0" stroke="#fbbf2488" stroke-width="1.5" filter="url(#f2-glow)"/>
<text x="618.0" y="372.0" font-size="16" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">FC</text>
<text x="700.0" y="372.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">全連接 + softmax</text>
<text x="618.0" y="391.0" font-size="12" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">整體判別</text>
<circle cx="870" cy="375.0" r="15" fill="none" stroke="#fbbf24" stroke-width="2.2"/><circle cx="865" cy="371.0" r="2.2" fill="#fbbf24"/><circle cx="875" cy="371.0" r="2.2" fill="#fbbf24"/><path d="M 864 381.0 Q 870 386.0 876 381.0" fill="none" stroke="#fbbf24" stroke-width="2"/><path d="M 378.0 375.0 L 456.0 375.0" fill="none" stroke="#f472b6" stroke-width="1.6" opacity="0.75" stroke-dasharray="7 5"/>
<path d="M 504.0 375.0 L 588.0 375.0" fill="none" stroke="#f472b6" stroke-width="1.6" opacity="0.75" stroke-dasharray="7 5"/>
<text x="480.0" y="383.0" font-size="24" fill="#e6edf3" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">≈</text>
<text x="48.0" y="470.0" font-size="13.5" fill="#fbbf24" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">關鍵不是「像不像」，而是兩邊都做了同一件事：把簡單單元疊成複雜單元，而且每一層只看局部。</text>
</svg>
</figure>


皮層的計算單元是神經元，而神經元做的事，就是一組加權和加一個閾值：

```
z = Σᵢ wᵢ·xᵢ + b        前激活
a = f(z)                 激活（超過閾值才「放電」）
```

| 生物 | 類比 |
| --- | --- |
| 樹突接收、突觸強度 | `wᵢ·xᵢ` |
| 靜息電位 / 閾值 | 偏置 `b` |
| 全或無的動作電位 | 階梯函數（尖銳非線性） |

三個值得記住的數字與性質：弱刺激會被忽略（所以每一層都需要**非線性**）；人腦約 86×10⁹ 個神經元、每個接約 10⁴ 個突觸；聽覺皮層若接到視覺訊號，可以學會「看」—— 同一套電路可以換用途，這是簡報說「general learning machine」的意思，也是 CNN 能從影像搬到聲音、基因序列的原因。

但簡報自己也補了一句很誠實的話：**這不是通用學習，只是對我們這個世界調得很好。**

## 3. 卷積：把窗口壓在每個 patch 上

如果全連接的問題是「每個位置都有自己的權重」，解法就是把權重共用。做法很直白：

1. 把輸入的一個 patch 接到下一層的**一個**神經元（它只「看」得到這塊）；
2. 用同一個窗口滑過整張圖；
3. 用多個濾波器抓不同的特徵。

這三條就是簡報列出的特徵提取三規則：**用一組權重（濾波器）抽局部特徵 → 用多個濾波器抽不同特徵 → 空間上共享每個濾波器的參數。**

<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 560" role="img" aria-label="5×5 輸入、3×3 濾波器、步長 1，得到 3×3 特徵圖；左上角的值是 −8" style="width:100%;height:auto;display:block">
<defs>
<filter id="f3-glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="f3-soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="11" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="f3-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#1a2331" stroke-width="1"/></pattern>
<marker id="f3-arw-2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker><marker id="f3-arw-f472b6" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#f472b6"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="558.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<rect x="0.75" y="0.75" width="958.5" height="558.5" rx="16" fill="url(#f3-grid)" opacity="0.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">卷積：把 9 個權重壓在每個 patch 上</text>
<text x="48" y="80" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一組權重滑過全圖 —— 這就是「參數共享」，也是 CNN 便宜的原因</text>
<text x="52.0" y="136.0" font-size="13.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">輸入 5×5</text>
<rect x="52.0" y="150.0" width="44.0" height="44.0" rx="5" fill="#12303c" opacity="1.0" stroke="#22d3ee99" stroke-width="1"/>
<text x="74.0" y="177.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">1</text>
<rect x="98.0" y="150.0" width="44.0" height="44.0" rx="5" fill="#12303c" opacity="1.0" stroke="#22d3ee99" stroke-width="1"/>
<text x="120.0" y="177.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">2</text>
<rect x="144.0" y="150.0" width="44.0" height="44.0" rx="5" fill="#12303c" opacity="1.0" stroke="#22d3ee99" stroke-width="1"/>
<text x="166.0" y="177.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">3</text>
<rect x="190.0" y="150.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="212.0" y="177.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">0</text>
<rect x="236.0" y="150.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="258.0" y="177.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">1</text>
<rect x="52.0" y="196.0" width="44.0" height="44.0" rx="5" fill="#12303c" opacity="1.0" stroke="#22d3ee99" stroke-width="1"/>
<text x="74.0" y="223.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">4</text>
<rect x="98.0" y="196.0" width="44.0" height="44.0" rx="5" fill="#12303c" opacity="1.0" stroke="#22d3ee99" stroke-width="1"/>
<text x="120.0" y="223.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">5</text>
<rect x="144.0" y="196.0" width="44.0" height="44.0" rx="5" fill="#12303c" opacity="1.0" stroke="#22d3ee99" stroke-width="1"/>
<text x="166.0" y="223.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">6</text>
<rect x="190.0" y="196.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="212.0" y="223.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">1</text>
<rect x="236.0" y="196.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="258.0" y="223.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">0</text>
<rect x="52.0" y="242.0" width="44.0" height="44.0" rx="5" fill="#12303c" opacity="1.0" stroke="#22d3ee99" stroke-width="1"/>
<text x="74.0" y="269.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">7</text>
<rect x="98.0" y="242.0" width="44.0" height="44.0" rx="5" fill="#12303c" opacity="1.0" stroke="#22d3ee99" stroke-width="1"/>
<text x="120.0" y="269.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">8</text>
<rect x="144.0" y="242.0" width="44.0" height="44.0" rx="5" fill="#12303c" opacity="1.0" stroke="#22d3ee99" stroke-width="1"/>
<text x="166.0" y="269.0" font-size="15" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">9</text>
<rect x="190.0" y="242.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="212.0" y="269.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">2</text>
<rect x="236.0" y="242.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="258.0" y="269.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">1</text>
<rect x="52.0" y="288.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="74.0" y="315.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">1</text>
<rect x="98.0" y="288.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="120.0" y="315.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">2</text>
<rect x="144.0" y="288.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="166.0" y="315.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">3</text>
<rect x="190.0" y="288.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="212.0" y="315.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">4</text>
<rect x="236.0" y="288.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="258.0" y="315.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">5</text>
<rect x="52.0" y="334.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="74.0" y="361.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">0</text>
<rect x="98.0" y="334.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="120.0" y="361.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">1</text>
<rect x="144.0" y="334.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="166.0" y="361.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">2</text>
<rect x="190.0" y="334.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="212.0" y="361.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">3</text>
<rect x="236.0" y="334.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="258.0" y="361.0" font-size="15" fill="#6b7889" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">4</text>
<rect x="48.0" y="146.0" width="144.0" height="144.0" rx="7" fill="none" opacity="1.0" stroke="#f472b6" stroke-width="2.4" filter="url(#f3-glow)"/>
<text x="322.0" y="136.0" font-size="13.5" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">濾波器 3×3（9 個權重）</text>
<rect x="322.0" y="150.0" width="38.0" height="38.0" rx="5" fill="#3a1024" opacity="1.0" stroke="#f472b6aa" stroke-width="1.2"/>
<text x="341.0" y="174.0" font-size="14" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">1</text>
<rect x="363.0" y="150.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#243244" stroke-width="1.2"/>
<text x="382.0" y="174.0" font-size="14" fill="#4a5768" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">0</text>
<rect x="404.0" y="150.0" width="38.0" height="38.0" rx="5" fill="#3a1024" opacity="1.0" stroke="#f472b6aa" stroke-width="1.2"/>
<text x="423.0" y="174.0" font-size="14" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">−1</text>
<rect x="322.0" y="191.0" width="38.0" height="38.0" rx="5" fill="#3a1024" opacity="1.0" stroke="#f472b6aa" stroke-width="1.2"/>
<text x="341.0" y="215.0" font-size="14" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">2</text>
<rect x="363.0" y="191.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#243244" stroke-width="1.2"/>
<text x="382.0" y="215.0" font-size="14" fill="#4a5768" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">0</text>
<rect x="404.0" y="191.0" width="38.0" height="38.0" rx="5" fill="#3a1024" opacity="1.0" stroke="#f472b6aa" stroke-width="1.2"/>
<text x="423.0" y="215.0" font-size="14" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">-2</text>
<rect x="322.0" y="232.0" width="38.0" height="38.0" rx="5" fill="#3a1024" opacity="1.0" stroke="#f472b6aa" stroke-width="1.2"/>
<text x="341.0" y="256.0" font-size="14" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">1</text>
<rect x="363.0" y="232.0" width="38.0" height="38.0" rx="5" fill="#141d29" opacity="1.0" stroke="#243244" stroke-width="1.2"/>
<text x="382.0" y="256.0" font-size="14" fill="#4a5768" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">0</text>
<rect x="404.0" y="232.0" width="38.0" height="38.0" rx="5" fill="#3a1024" opacity="1.0" stroke="#f472b6aa" stroke-width="1.2"/>
<text x="423.0" y="256.0" font-size="14" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">−1</text>
<path d="M 300.0 232.0 L 316.0 232.0" fill="none" stroke="#f472b6" stroke-width="2" marker-end="url(#f3-arw-f472b6)"/>
<path d="M 452.0 232.0 L 508.0 232.0" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#f3-arw-2dd4bf)"/>
<text x="520.0" y="136.0" font-size="13.5" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">特徵圖 3×3</text>
<rect x="520.0" y="150.0" width="44.0" height="44.0" rx="5" fill="#0f2b36" opacity="1.0" stroke="#22d3ee" stroke-width="2.2" filter="url(#f3-glow)"/>
<text x="542.0" y="177.0" font-size="15" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">-8</text>
<rect x="566.0" y="150.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="588.0" y="177.0" font-size="15" fill="#8b9aab" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">16</text>
<rect x="612.0" y="150.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="634.0" y="177.0" font-size="15" fill="#8b9aab" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">22</text>
<rect x="520.0" y="196.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="542.0" y="223.0" font-size="15" fill="#8b9aab" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">6</text>
<rect x="566.0" y="196.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="588.0" y="223.0" font-size="15" fill="#8b9aab" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">14</text>
<rect x="612.0" y="196.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="634.0" y="223.0" font-size="15" fill="#8b9aab" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">20</text>
<rect x="520.0" y="242.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="542.0" y="269.0" font-size="15" fill="#8b9aab" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">-8</text>
<rect x="566.0" y="242.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="588.0" y="269.0" font-size="15" fill="#8b9aab" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">0</text>
<rect x="612.0" y="242.0" width="44.0" height="44.0" rx="5" fill="#111a24" opacity="1.0" stroke="#1e2a38" stroke-width="1"/>
<text x="634.0" y="269.0" font-size="15" fill="#8b9aab" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">2</text>
<text x="520.0" y="306.0" font-size="12" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">同一組權重，9 個位置 → 81 次乘加</text>
<rect x="48.0" y="390.0" width="864.0" height="138.0" rx="12" fill="#0b1017" opacity="1.0" stroke="#f472b644" stroke-width="1.2"/>
<text x="70.0" y="420.0" font-size="13.5" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">左上角那一格是怎麼算出來的</text>
<text x="72.0" y="448.0" font-size="12.5" fill="#9fb0c0" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">1·1  +  2·0  +  3·(−1)   =   1 + 0 − 3</text>
<text x="72.0" y="468.0" font-size="12.5" fill="#9fb0c0" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">4·2  +  5·0  +  6·(−2)   =   8 + 0 − 12</text>
<text x="72.0" y="488.0" font-size="12.5" fill="#9fb0c0" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">7·1  +  8·0  +  9·(−1)   =   7 + 0 − 9</text>
<path d="M 470.0 436.0 L 470.0 494.0" fill="none" stroke="#222b36" stroke-width="1.2" opacity="1.0"/>
<text x="492.0" y="448.0" font-size="15" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">相加 = −8</text>
<text x="492.0" y="472.0" font-size="12" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">−8 幾乎是黑的：這裡沒有右緣</text>
<text x="492.0" y="494.0" font-size="12" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">16、22 才亮：強烈的垂直邊</text>
<text x="72.0" y="512.0" font-size="12.5" fill="#fbbf24" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">9 個權重 + 1 個偏置 = 10 個參數；乘加 9 位置 × 9 = 81 次。</text>
</svg>
</figure>


數學上就是逐元素相乘再相加：

```
Z[i, j] = b + Σ_{u=0}^{F-1} Σ_{v=0}^{F-1}  X[i·S + u, j·S + v] · W[u, v]
```

圖 3 用的是 5×5 輸入、3×3 濾波器、步長 1，左上角那一格：

```
1·1 + 2·0 + 3·(−1) + 4·2 + 5·0 + 6·(−2) + 7·1 + 8·0 + 9·(−1) = −8
```

−8 幾乎是黑的：這個位置沒有「右緣」。同一組權重掃到右邊的 `2 3 0 / 5 6 1 / 8 9 2` 時得到 16、再往右是 22 —— 亮起來的位置就是垂直邊。

> 一個容易被忽略的術語細節：深度學習講的「卷積」其實是**互相關**（cross-correlation），沒有把核翻轉 180°。對「學出來的」核沒有差別（網路會自己學成翻轉後的版本），但手推梯度時要記得這件事。

能用 9 個數字編碼的視覺原語，其實就是這幾種：

| 用途 | 濾波器 | 效果 |
| --- | --- | --- |
| 水平差分 | `1 −1` | 找垂直邊界 |
| Sobel-x | `−1 0 1 / −2 0 2 / −1 0 1` | 平滑後的垂直邊 |
| Sobel-y | `−1 −2 −1 / 0 0 0 / 1 2 1` | 水平邊 |
| 銳化 | `0 −1 0 / −1 5 −1 / 0 −1 0` | 原圖 + Laplacian |
| 模糊 | 3×3 全 1，除以 9 | 局部平均 |

課堂簡報第 25 頁的四格（原圖 / 銳化 / 邊緣 / 強邊緣）就是同一張照片換不同核的結果。CNN 做的事，是**把這些核從資料裡學出來**，而不是由人挑。

## 4. 步長與填充：一條公式吃掉所有尺寸問題

```
out = ⌊(N + 2P − F) / S⌋ + 1
```

記住這一條，LeNet-5 的每一層都能自己驗算：

| N | F | P | S | out | 名稱 |
| --- | --- | --- | --- | --- | --- |
| 32 | 5 | 0 | 1 | 28 | LeNet C1（valid） |
| 28 | 2 | 0 | 2 | 14 | LeNet S2（池化） |
| 32 | 3 | 1 | 1 | 32 | same（P = (F−1)/2） |
| 32 | 3 | 1 | 2 | 16 | same + stride 2 |

<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 570" role="img" aria-label="三格並排：valid 8→6、same 補一圈 0 後 10→8、stride 2 8→3" style="width:100%;height:auto;display:block">
<defs>
<filter id="f4-glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="f4-soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="11" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="f4-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#1a2331" stroke-width="1"/></pattern>
<marker id="f4-arw-2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="568.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<rect x="0.75" y="0.75" width="958.5" height="568.5" rx="16" fill="url(#f4-grid)" opacity="0.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">步長與填充：一條公式管三種情形</text>
<text x="48" y="80" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">out = ⌊(N + 2P − F) / S⌋ + 1 —— 記住這條，LeNet-5 的每一層都能自己驗算</text>
<rect x="48.0" y="110.0" width="272.0" height="430.0" rx="12" fill="#0b1017" opacity="1.0" stroke="#22d3ee3d" stroke-width="1.2"/>
<text x="68.0" y="142.0" font-size="15" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">VALID</text>
<text x="68.0" y="163.0" font-size="12" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">P = 0, S = 1</text>
<rect x="136.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="148.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="160.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="172.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="184.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="196.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="208.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="220.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="136.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="148.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="160.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="172.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="184.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="196.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="208.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="220.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="136.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="148.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="160.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="172.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="184.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="196.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="208.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="220.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="136.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="148.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="160.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="172.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="184.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="196.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="208.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="220.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="136.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="148.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="160.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="172.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="184.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="196.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="208.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="220.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="136.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="148.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="160.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="172.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="184.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="196.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="208.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="220.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="136.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="148.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="160.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="172.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="184.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="196.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="208.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="220.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="136.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="148.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="160.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="172.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="184.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="196.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="208.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="220.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="135.5" y="185.0" width="37.0" height="37.0" rx="3" fill="none" opacity="1.0" stroke="#22d3ee" stroke-width="2.2" filter="url(#f4-glow)"/>
<text x="68.0" y="332.0" font-size="12" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">輸出 6×6</text>
<rect x="145.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="158.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="171.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="184.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="197.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="210.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="145.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="158.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="171.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="184.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="197.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="210.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="145.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="158.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="171.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="184.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="197.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="210.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="145.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="158.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="171.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="184.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="197.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="210.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="145.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="158.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="171.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="184.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="197.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="210.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="145.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="158.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="171.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="184.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="197.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<rect x="210.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#22d3ee77" stroke-width="0.8"/>
<text x="68.0" y="494.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">8×8 直接掃，邊角掃不到</text>
<text x="68.0" y="518.0" font-size="12" fill="#9fb0c0" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">⌊(8 + 2·0 − 3)/1⌋ + 1 = 6</text>
<rect x="344.0" y="110.0" width="272.0" height="430.0" rx="12" fill="#0b1017" opacity="1.0" stroke="#a3e6353d" stroke-width="1.2"/>
<text x="364.0" y="142.0" font-size="15" fill="#a3e635" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">SAME</text>
<text x="364.0" y="163.0" font-size="12" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">P = 1, S = 1</text>
<rect x="420.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="432.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="444.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="456.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="468.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="480.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="492.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="504.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="516.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="528.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="420.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="432.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="444.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="456.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="468.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="480.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="492.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="504.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="516.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="528.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="420.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="432.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="444.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="456.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="468.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="480.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="492.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="504.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="516.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="528.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="420.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="432.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="444.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="456.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="468.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="480.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="492.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="504.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="516.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="528.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="420.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="432.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="444.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="456.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="468.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="480.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="492.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="504.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="516.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="528.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="420.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="432.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="444.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="456.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="468.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="480.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="492.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="504.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="516.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="528.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="420.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="432.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="444.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="456.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="468.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="480.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="492.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="504.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="516.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="528.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="420.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="432.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="444.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="456.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="468.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="480.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="492.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="504.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="516.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="528.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="420.5" y="282.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="432.5" y="282.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="444.5" y="282.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="456.5" y="282.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="468.5" y="282.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="480.5" y="282.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="492.5" y="282.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="504.5" y="282.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="516.5" y="282.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="528.5" y="282.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="420.5" y="294.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="432.5" y="294.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="444.5" y="294.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="456.5" y="294.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="468.5" y="294.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="480.5" y="294.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="492.5" y="294.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="504.5" y="294.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="516.5" y="294.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="528.5" y="294.0" width="11.0" height="11.0" rx="2" fill="#123a33" opacity="1.0" stroke="#a3e63566" stroke-width="1.0"/>
<rect x="419.5" y="185.0" width="37.0" height="37.0" rx="3" fill="none" opacity="1.0" stroke="#a3e635" stroke-width="2.2" filter="url(#f4-glow)"/>
<text x="364.0" y="332.0" font-size="12" fill="#a3e635" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">輸出 8×8</text>
<rect x="428.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="441.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="454.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="467.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="480.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="493.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="506.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="519.5" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="428.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="441.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="454.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="467.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="480.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="493.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="506.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="519.5" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="428.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="441.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="454.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="467.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="480.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="493.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="506.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="519.5" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="428.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="441.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="454.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="467.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="480.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="493.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="506.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="519.5" y="383.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="428.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="441.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="454.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="467.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="480.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="493.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="506.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="519.5" y="396.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="428.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="441.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="454.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="467.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="480.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="493.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="506.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="519.5" y="409.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="428.5" y="422.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="441.5" y="422.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="454.5" y="422.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="467.5" y="422.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="480.5" y="422.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="493.5" y="422.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="506.5" y="422.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="519.5" y="422.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="428.5" y="435.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="441.5" y="435.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="454.5" y="435.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="467.5" y="435.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="480.5" y="435.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="493.5" y="435.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="506.5" y="435.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<rect x="519.5" y="435.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#a3e63577" stroke-width="0.8"/>
<text x="364.0" y="494.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">外圍補一圈 0 → 10×10</text>
<text x="364.0" y="518.0" font-size="12" fill="#9fb0c0" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">⌊(8 + 2·1 − 3)/1⌋ + 1 = 8</text>
<rect x="640.0" y="110.0" width="272.0" height="430.0" rx="12" fill="#0b1017" opacity="1.0" stroke="#fbbf243d" stroke-width="1.2"/>
<text x="660.0" y="142.0" font-size="15" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">STRIDE 2</text>
<text x="660.0" y="163.0" font-size="12" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">P = 0, S = 2</text>
<rect x="728.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="740.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="752.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="764.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="776.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="788.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="800.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="812.5" y="186.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="728.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="740.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="752.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="764.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="776.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="788.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="800.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="812.5" y="198.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="728.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="740.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="752.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="764.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="776.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="788.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="800.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="812.5" y="210.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="728.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="740.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="752.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="764.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="776.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="788.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="800.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="812.5" y="222.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="728.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="740.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="752.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="764.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="776.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="788.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="800.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="812.5" y="234.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="728.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="740.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="752.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="764.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="776.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="788.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="800.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="812.5" y="246.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="728.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="740.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="752.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="764.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="776.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="788.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="800.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="812.5" y="258.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="728.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="740.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="752.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="764.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="776.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="788.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="800.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="812.5" y="270.0" width="11.0" height="11.0" rx="2" fill="#1b2836" opacity="1.0" stroke="#2b3d50" stroke-width="0.9"/>
<rect x="727.5" y="185.0" width="37.0" height="37.0" rx="3" fill="none" opacity="1.0" stroke="#fbbf24" stroke-width="2.2" filter="url(#f4-glow)"/>
<text x="728.5" y="298.0" font-size="10.5" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">每步跳 2 格 →</text>
<text x="660.0" y="332.0" font-size="12" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">輸出 3×3</text>
<rect x="757.0" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#fbbf2477" stroke-width="0.8"/>
<rect x="770.0" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#fbbf2477" stroke-width="0.8"/>
<rect x="783.0" y="344.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#fbbf2477" stroke-width="0.8"/>
<rect x="757.0" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#fbbf2477" stroke-width="0.8"/>
<rect x="770.0" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#fbbf2477" stroke-width="0.8"/>
<rect x="783.0" y="357.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#fbbf2477" stroke-width="0.8"/>
<rect x="757.0" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#fbbf2477" stroke-width="0.8"/>
<rect x="770.0" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#fbbf2477" stroke-width="0.8"/>
<rect x="783.0" y="370.0" width="12.0" height="12.0" rx="2" fill="#1a2836" opacity="1.0" stroke="#fbbf2477" stroke-width="0.8"/>
<text x="660.0" y="494.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">隔一格掃，尺寸砍半</text>
<text x="660.0" y="518.0" font-size="12" fill="#9fb0c0" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">⌊(8 + 2·0 − 3)/2⌋ + 1 = 3</text>
<text x="48.0" y="562.0" font-size="1" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0"></text>
</svg>
</figure>



## 5. 為什麼要參數共享：30,900 倍不是形容詞

把同一件事用兩種方式做一次，差距有多大：

| | 全連接 | 卷積 |
| --- | --- | --- |
| 輸出單元 | 28·28·6 = 4,704 | 4,704 |
| 每個單元的輸入 | 1,024（整張圖） | 25（一個 5×5 patch） |
| **權重** | 1,024 × 4,704 = **4,816,896** | (25 + 1) × 6 = **156** |

差了 **30,900 倍**。而且不是「省一點」，是**贏在另一個數量級**：

<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" role="img" aria-label="長條圖比較全連接與卷積的參數量：32×32 影像差 30,900 倍，224×224 影像差 2.6 億倍" style="width:100%;height:auto;display:block">
<defs>
<filter id="f5-glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="f5-soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="11" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="f5-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#1a2331" stroke-width="1"/></pattern>
<marker id="f5-arw-fbbf24" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#fbbf24"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="518.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<rect x="0.75" y="0.75" width="958.5" height="518.5" rx="16" fill="url(#f5-grid)" opacity="0.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一件事，兩種代價：參數差 3 萬倍到 2.6 億倍</text>
<text x="48" y="80" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">對數刻度；「卷積贏」不是贏一點點，是贏在另一個數量級上</text>
<text x="230.0" y="122.0" font-size="12" fill="#8b949e" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">參數量（對數刻度）</text>
<text x="48.0" y="168.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="0.9">32×32×1 → 4,704 個輸出</text>
<text x="218.0" y="195.0" font-size="13" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">全連接</text>
<rect x="230.0" y="176.0" width="304.4" height="28.0" rx="6" fill="#fbbf242e" opacity="1.0" stroke="#fbbf24" stroke-width="1.4"/>
<text x="242.0" y="195.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">4.82e+06</text>
<text x="242.0" y="211.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">1,024 × 4,704</text>
<text x="218.0" y="239.0" font-size="13" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">卷積 5×5</text>
<rect x="230.0" y="220.0" width="12.6" height="28.0" rx="6" fill="#22d3ee2e" opacity="1.0" stroke="#22d3ee" stroke-width="1.4" filter="url(#f5-glow)"/>
<text x="252.6" y="239.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">156</text>
<text x="252.6" y="255.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">(25 + 1) × 6</text>
<text x="48.0" y="312.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="0.9">224×224×3 → 222×222×64</text>
<text x="218.0" y="339.0" font-size="13" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">全連接</text>
<rect x="230.0" y="320.0" width="629.0" height="28.0" rx="6" fill="#fbbf242e" opacity="1.0" stroke="#fbbf24" stroke-width="1.4"/>
<text x="242.0" y="339.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">4.75e+11</text>
<text x="242.0" y="355.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">150,528 × 3,153,216</text>
<text x="218.0" y="383.0" font-size="13" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">卷積 3×3</text>
<rect x="230.0" y="364.0" width="81.5" height="28.0" rx="6" fill="#22d3ee2e" opacity="1.0" stroke="#22d3ee" stroke-width="1.4" filter="url(#f5-glow)"/>
<text x="321.5" y="383.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">1,792</text>
<text x="321.5" y="399.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">(27 + 1) × 64</text>
<rect x="560.0" y="204.0" width="200.0" height="32.0" rx="8" fill="#1a1220" opacity="1.0" stroke="#f472b688" stroke-width="1.2"/>
<text x="660.0" y="225.0" font-size="14" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">÷ 30,900</text>
<rect x="560.0" y="348.0" width="200.0" height="32.0" rx="8" fill="#1a1220" opacity="1.0" stroke="#f472b688" stroke-width="1.2"/>
<text x="660.0" y="369.0" font-size="14" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">÷ 2.6 × 10⁸</text>
<path d="M 230.0 440.0 L 880.0 440.0" fill="none" stroke="#222b36" stroke-width="1.2" opacity="1.0"/>
<path d="M 230.0 440.0 L 230.0 445.0" fill="none" stroke="#3a4757" stroke-width="1.1" opacity="1.0"/>
<text x="230.0" y="460.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">10²</text>
<path d="M 360.0 440.0 L 360.0 445.0" fill="none" stroke="#3a4757" stroke-width="1.1" opacity="1.0"/>
<text x="360.0" y="460.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">10⁴</text>
<path d="M 490.0 440.0 L 490.0 445.0" fill="none" stroke="#3a4757" stroke-width="1.1" opacity="1.0"/>
<text x="490.0" y="460.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">10⁶</text>
<path d="M 620.0 440.0 L 620.0 445.0" fill="none" stroke="#3a4757" stroke-width="1.1" opacity="1.0"/>
<text x="620.0" y="460.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">10⁸</text>
<path d="M 750.0 440.0 L 750.0 445.0" fill="none" stroke="#3a4757" stroke-width="1.1" opacity="1.0"/>
<text x="750.0" y="460.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">10¹⁰</text>
<path d="M 880.0 440.0 L 880.0 445.0" fill="none" stroke="#3a4757" stroke-width="1.1" opacity="1.0"/>
<text x="880.0" y="460.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">10¹²</text>
<text x="48.0" y="496.0" font-size="12.5" fill="#fbbf24" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">「卷積贏」的真正原因：參數量只看濾波器（F²·C_in·C_out），與影像尺寸無關；全連接則隨像素數線性爆炸。</text>
</svg>
</figure>


到了 224×224 的彩色輸入，差距變成 4.75×10¹¹ 對 1,792（**2.6 億倍**）。原因很簡單：

```
卷積參數 = (F·F·C_in + 1) · C_out        ← 只跟濾波器大小與通道數有關
全連接參數 = (n_in + 1) · n_out          ← 隨像素數線性爆炸
```

**影像變大，卷積的參數不變。** 這是 CNN 能處理高解析度影像的根本原因。

順帶一個常被搞混的點：卷積給的是**平移等變**（equivariance，輸入平移 → 特徵圖跟著平移），不是**平移不變**（invariance）。要不變，得靠池化或全域池化把位置資訊壓掉。簡報沒有細分這兩個詞，但考試很愛問。

## 6. LeNet-5：61,750 個參數，五層，1998 年

LeNet-5（LeCun, Bottou, Bengio & Haffner, 1998）是「梯度學習做文件辨識」那篇論文的網路，也是我們今天用 CNN 的方式的起點：它第一次用**學出來的濾波器**取代手工特徵。

<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 500" role="img" aria-label="LeNet-5 的八層架構，從 32×32×1 到 10 類輸出，各層尺寸與參數量" style="width:100%;height:auto;display:block">
<defs>
<filter id="f6-glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="f6-soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="11" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="f6-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#1a2331" stroke-width="1"/></pattern>
<marker id="f6-arw-22d3ee" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#22d3ee"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="498.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<rect x="0.75" y="0.75" width="958.5" height="498.5" rx="16" fill="url(#f6-grid)" opacity="0.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">LeNet-5：整張網路只有 61,750 個參數</text>
<text x="48" y="80" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1998 年，LeCun 等人；深度學習第一次用「學出來的濾波器」取代手工特徵</text>
<rect x="48.0" y="168.0" width="67.0" height="108.0" rx="6" fill="#101a26" opacity="1.0" stroke="#5d6b7dcc" stroke-width="1.6"/>
<text x="81.5" y="227.0" font-size="20" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="0.85" text-anchor="middle">0</text>
<text x="81.5" y="156.0" font-size="11" fill="#5d6b7d" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">輸入</text>
<text x="81.5" y="296.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">32×32×1</text>
<text x="81.5" y="330.0" font-size="10" fill="#5d6b7d" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">--</text>
<path d="M 118.0 222.0 L 165.3 222.0" fill="none" stroke="#42536b" stroke-width="1.6" marker-end="url(#f6-arw-42536b)"/>
<rect x="173.3" y="164.0" width="96.0" height="108.0" rx="6" fill="none" opacity="1.0" stroke="#22d3ee3a" stroke-width="1"/>
<rect x="169.3" y="168.0" width="96.0" height="108.0" rx="6" fill="#101a26" opacity="1.0" stroke="#22d3eecc" stroke-width="1.6" filter="url(#f6-glow)"/>
<text x="217.3" y="227.0" font-size="20" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="0.85" text-anchor="middle">1</text>
<text x="217.3" y="156.0" font-size="11" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">Conv 5×5</text>
<text x="217.3" y="296.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">28×28×6</text>
<text x="217.3" y="314.0" font-size="11" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">156</text>
<text x="217.3" y="330.0" font-size="10" fill="#5d6b7d" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">s1</text>
<path d="M 268.3 222.0 L 315.6 222.0" fill="none" stroke="#42536b" stroke-width="1.6" marker-end="url(#f6-arw-42536b)"/>
<rect x="323.6" y="164.0" width="69.0" height="108.0" rx="6" fill="none" opacity="1.0" stroke="#a78bfa3a" stroke-width="1"/>
<rect x="319.6" y="168.0" width="69.0" height="108.0" rx="6" fill="#101a26" opacity="1.0" stroke="#a78bfacc" stroke-width="1.6"/>
<text x="354.1" y="227.0" font-size="20" fill="#a78bfa" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="0.85" text-anchor="middle">2</text>
<text x="354.1" y="156.0" font-size="11" fill="#a78bfa" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">AvgPool</text>
<text x="354.1" y="296.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">14×14×6</text>
<text x="354.1" y="314.0" font-size="11" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">12</text>
<text x="354.1" y="330.0" font-size="10" fill="#5d6b7d" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">f2 s2</text>
<path d="M 391.6 222.0 L 438.9 222.0" fill="none" stroke="#42536b" stroke-width="1.6" marker-end="url(#f6-arw-42536b)"/>
<rect x="450.9" y="160.0" width="74.0" height="108.0" rx="6" fill="none" opacity="1.0" stroke="#22d3ee3a" stroke-width="1"/>
<rect x="446.9" y="164.0" width="74.0" height="108.0" rx="6" fill="none" opacity="1.0" stroke="#22d3ee3a" stroke-width="1"/>
<rect x="442.9" y="168.0" width="74.0" height="108.0" rx="6" fill="#101a26" opacity="1.0" stroke="#22d3eecc" stroke-width="1.6" filter="url(#f6-glow)"/>
<text x="479.9" y="227.0" font-size="20" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="0.85" text-anchor="middle">3</text>
<text x="479.9" y="156.0" font-size="11" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">Conv 5×5</text>
<text x="479.9" y="296.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">10×10×16</text>
<text x="479.9" y="314.0" font-size="11" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">2,416</text>
<text x="479.9" y="330.0" font-size="10" fill="#5d6b7d" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">s1</text>
<path d="M 519.9 222.0 L 567.1 222.0" fill="none" stroke="#42536b" stroke-width="1.6" marker-end="url(#f6-arw-42536b)"/>
<rect x="579.1" y="160.0" width="56.0" height="108.0" rx="6" fill="none" opacity="1.0" stroke="#a78bfa3a" stroke-width="1"/>
<rect x="575.1" y="164.0" width="56.0" height="108.0" rx="6" fill="none" opacity="1.0" stroke="#a78bfa3a" stroke-width="1"/>
<rect x="571.1" y="168.0" width="56.0" height="108.0" rx="6" fill="#101a26" opacity="1.0" stroke="#a78bfacc" stroke-width="1.6"/>
<text x="599.1" y="227.0" font-size="20" fill="#a78bfa" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="0.85" text-anchor="middle">4</text>
<text x="599.1" y="156.0" font-size="11" fill="#a78bfa" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">AvgPool</text>
<text x="599.1" y="296.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">5×5×16</text>
<text x="599.1" y="314.0" font-size="11" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">32</text>
<text x="599.1" y="330.0" font-size="10" fill="#5d6b7d" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">f2 s2</text>
<path d="M 630.1 222.0 L 677.4 222.0" fill="none" stroke="#42536b" stroke-width="1.6" marker-end="url(#f6-arw-42536b)"/>
<rect x="693.4" y="156.0" width="45.0" height="108.0" rx="6" fill="none" opacity="1.0" stroke="#22d3ee3a" stroke-width="1"/>
<rect x="689.4" y="160.0" width="45.0" height="108.0" rx="6" fill="none" opacity="1.0" stroke="#22d3ee3a" stroke-width="1"/>
<rect x="685.4" y="164.0" width="45.0" height="108.0" rx="6" fill="none" opacity="1.0" stroke="#22d3ee3a" stroke-width="1"/>
<rect x="681.4" y="168.0" width="45.0" height="108.0" rx="6" fill="#101a26" opacity="1.0" stroke="#22d3eecc" stroke-width="1.6" filter="url(#f6-glow)"/>
<text x="703.9" y="227.0" font-size="20" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="0.85" text-anchor="middle">5</text>
<text x="703.9" y="156.0" font-size="11" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">Conv 5×5</text>
<text x="703.9" y="296.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">1×1×120</text>
<text x="703.9" y="314.0" font-size="11" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">48,120</text>
<text x="703.9" y="330.0" font-size="10" fill="#5d6b7d" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">≡ FC</text>
<path d="M 729.4 222.0 L 776.7 222.0" fill="none" stroke="#42536b" stroke-width="1.6" marker-end="url(#f6-arw-42536b)"/>
<rect x="780.7" y="168.0" width="43.0" height="108.0" rx="6" fill="#101a26" opacity="1.0" stroke="#fbbf24cc" stroke-width="1.6"/>
<text x="802.2" y="227.0" font-size="20" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="0.85" text-anchor="middle">6</text>
<text x="802.2" y="156.0" font-size="11" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">FC</text>
<text x="802.2" y="296.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">84</text>
<text x="802.2" y="314.0" font-size="11" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">10,164</text>
<path d="M 826.7 222.0 L 874.0 222.0" fill="none" stroke="#42536b" stroke-width="1.6" marker-end="url(#f6-arw-42536b)"/>
<rect x="878.0" y="168.0" width="34.0" height="108.0" rx="6" fill="#101a26" opacity="1.0" stroke="#fbbf24cc" stroke-width="1.6"/>
<text x="895.0" y="227.0" font-size="20" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="0.85" text-anchor="middle">7</text>
<text x="895.0" y="156.0" font-size="11" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">FC</text>
<text x="895.0" y="296.0" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">10</text>
<text x="895.0" y="314.0" font-size="11" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">850</text>
<text x="895.0" y="330.0" font-size="10" fill="#5d6b7d" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">softmax</text>
<rect x="48.0" y="400.0" width="864.0" height="74.0" rx="10" fill="#0b1017" opacity="1.0" stroke="#22d3ee33" stroke-width="1.2"/>
<text x="60.0" y="428.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">參數總數</text>
<text x="60.0" y="452.0" font-size="19" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">61,750</text>
<text x="60.0" y="468.0" font-size="9.5" fill="#5d6b7d" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">≈ 60K（講義寫 60K）</text>
<text x="276.0" y="428.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">乘加 / 一張圖</text>
<text x="276.0" y="452.0" font-size="19" fill="#a78bfa" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">422,824</text>
<text x="276.0" y="468.0" font-size="9.5" fill="#5d6b7d" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">conv 與 FC 全部加總</text>
<text x="492.0" y="428.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">感受野</text>
<text x="492.0" y="452.0" font-size="19" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">32×32</text>
<text x="492.0" y="468.0" font-size="9.5" fill="#5d6b7d" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">最後一層看到整張輸入</text>
<text x="708.0" y="428.0" font-size="11.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">對照：一層 FC</text>
<text x="708.0" y="452.0" font-size="19" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">1,025,000</text>
<text x="708.0" y="468.0" font-size="9.5" fill="#5d6b7d" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">1,024 → 1,000 單元</text>
</svg>
</figure>


| # | 層 | 核 | 步長 | 輸出 | 參數 | 乘加 / 張 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 輸入 | — | — | 32×32×1 | 0 | — |
| 1 | C1 卷積 | 5×5 ×6 | 1 | 28×28×6 | (25·1+1)·6 = **156** | 117,600 |
| 2 | S2 平均池化 | 2×2 | 2 | 14×14×6 | 2·6 = **12** | 4,704 |
| 3 | C3 卷積 | 5×5 ×16 | 1 | 10×10×16 | (25·6+1)·16 = **2,416** | 240,000 |
| 4 | S4 平均池化 | 2×2 | 2 | 5×5×16 | 2·16 = **32** | 1,600 |
| 5 | C5 卷積（圖上標 FC） | 5×5 ×120 | 1 | 1×1×120 | (25·16+1)·120 = **48,120** | 48,000 |
| 6 | F6 全連接 | — | — | 84 | (120+1)·84 = **10,164** | 10,080 |
| 7 | 輸出 | — | — | 10 | (84+1)·10 = **850** | 840 |
| | **合計** | | | | **61,750** | **422,824** |

三個細節：

- **第 5 層寫成 FC，其實是卷積**。進來的是 5×5×16，用 5×5 的核剛好壓成 1×1×120 —— 當核的大小等於整個輸入體積時，卷積就等價於全連接。`(25·16+1)·120 = 48,120`，跟「400 → 120 的全連接層」算出來一模一樣。
- **越深，`N_H、N_W` 越小，`N_C` 越大**：32→28→14→10→5→1，同時 1→6→16→120。解析度換通道數，是 CNN 的通用節奏。
- 原始網路用 **sigmoid / tanh**，平均池化還帶可訓練係數。max pooling 與 ReLU 是後來的東西。

### 感受野：為什麼最後一層剛好看到整張圖

感受野的遞推只有兩行：

```
r_out = r_in + (k − 1) · j_in
j_out = j_in · S
```

| 層 | k | s | 感受野 r | 跳距 j |
| --- | --- | --- | --- | --- |
| C1 | 5 | 1 | 1 + 4·1 = **5** | 1 |
| S2 | 2 | 2 | 5 + 1·1 = **6** | 2 |
| C3 | 5 | 1 | 6 + 4·2 = **14** | 2 |
| S4 | 2 | 2 | 14 + 1·2 = **16** | 4 |
| C5 | 5 | 1 | 16 + 4·4 = **32** | 4 |

<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 470" role="img" aria-label="32×32 輸入上疊出五個同心方框，代表 C1 到 C5 各層的感受野" style="width:100%;height:auto;display:block">
<defs>
<filter id="f7-glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="f7-soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="11" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="f7-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#1a2331" stroke-width="1"/></pattern>
<marker id="f7-arw-22d3ee" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#22d3ee"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="468.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<rect x="0.75" y="0.75" width="958.5" height="468.5" rx="16" fill="url(#f7-grid)" opacity="0.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">感受野：5 → 6 → 14 → 16 → 32</text>
<text x="48" y="80" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">r_out = r_in + (k − 1)·j_in，j_out = j_in·S；每層只看局部，疊起來就看到全部</text>
<path d="M 120.0 130.0 L 120.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 130.0 L 408.0 130.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 129.0 130.0 L 129.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 139.0 L 408.0 139.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 138.0 130.0 L 138.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 148.0 L 408.0 148.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 147.0 130.0 L 147.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 157.0 L 408.0 157.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 156.0 130.0 L 156.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 166.0 L 408.0 166.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 165.0 130.0 L 165.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 175.0 L 408.0 175.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 174.0 130.0 L 174.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 184.0 L 408.0 184.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 183.0 130.0 L 183.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 193.0 L 408.0 193.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 192.0 130.0 L 192.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 202.0 L 408.0 202.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 201.0 130.0 L 201.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 211.0 L 408.0 211.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 210.0 130.0 L 210.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 220.0 L 408.0 220.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 219.0 130.0 L 219.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 229.0 L 408.0 229.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 228.0 130.0 L 228.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 238.0 L 408.0 238.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 237.0 130.0 L 237.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 247.0 L 408.0 247.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 246.0 130.0 L 246.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 256.0 L 408.0 256.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 255.0 130.0 L 255.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 265.0 L 408.0 265.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 264.0 130.0 L 264.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 274.0 L 408.0 274.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 273.0 130.0 L 273.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 283.0 L 408.0 283.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 282.0 130.0 L 282.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 292.0 L 408.0 292.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 291.0 130.0 L 291.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 301.0 L 408.0 301.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 300.0 130.0 L 300.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 310.0 L 408.0 310.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 309.0 130.0 L 309.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 319.0 L 408.0 319.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 318.0 130.0 L 318.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 328.0 L 408.0 328.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 327.0 130.0 L 327.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 337.0 L 408.0 337.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 336.0 130.0 L 336.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 346.0 L 408.0 346.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 345.0 130.0 L 345.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 355.0 L 408.0 355.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 354.0 130.0 L 354.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 364.0 L 408.0 364.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 363.0 130.0 L 363.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 373.0 L 408.0 373.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 372.0 130.0 L 372.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 382.0 L 408.0 382.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 381.0 130.0 L 381.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 391.0 L 408.0 391.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 390.0 130.0 L 390.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 400.0 L 408.0 400.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 399.0 130.0 L 399.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 409.0 L 408.0 409.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 408.0 130.0 L 408.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<path d="M 120.0 418.0 L 408.0 418.0" fill="none" stroke="#1b2634" stroke-width="0.7" opacity="1.0"/>
<rect x="120.0" y="130.0" width="288.0" height="288.0" rx="2" fill="none" opacity="1.0" stroke="#2b3d50" stroke-width="1"/>
<rect x="119.0" y="129.0" width="47.0" height="47.0" rx="3" fill="none" opacity="1.0" stroke="#22d3ee" stroke-width="1.6" filter="url(#f7-glow)"/>
<rect x="119.0" y="129.0" width="56.0" height="56.0" rx="3" fill="none" opacity="1.0" stroke="#2dd4bf" stroke-width="1.6" filter="url(#f7-glow)"/>
<rect x="119.0" y="129.0" width="128.0" height="128.0" rx="3" fill="none" opacity="1.0" stroke="#a78bfa" stroke-width="1.6" filter="url(#f7-glow)"/>
<rect x="119.0" y="129.0" width="146.0" height="146.0" rx="3" fill="none" opacity="1.0" stroke="#a3e635" stroke-width="1.6" filter="url(#f7-glow)"/>
<rect x="119.0" y="129.0" width="290.0" height="290.0" rx="3" fill="none" opacity="1.0" stroke="#f472b6" stroke-width="2.4" filter="url(#f7-glow)"/>
<text x="120.0" y="120.0" font-size="12" fill="#8b949e" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">32×32 輸入</text>
<text x="470.0" y="132.0" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">各層的感受野（換算成輸入像素）</text>
<rect x="470.0" y="162.0" width="12.0" height="12.0" rx="3" fill="#22d3ee" opacity="1.0" filter="url(#f7-glow)"/>
<text x="492.0" y="173.0" font-size="13" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">C1</text>
<text x="546.0" y="173.0" font-size="12" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">conv 5×5, s1</text>
<text x="696.0" y="173.0" font-size="12.5" fill="#e6edf3" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">1 + 4·1 = 5</text>
<rect x="470.0" y="208.0" width="12.0" height="12.0" rx="3" fill="#2dd4bf" opacity="1.0" filter="url(#f7-glow)"/>
<text x="492.0" y="219.0" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">S2</text>
<text x="546.0" y="219.0" font-size="12" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">pool 2×2, s2</text>
<text x="696.0" y="219.0" font-size="12.5" fill="#e6edf3" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">5 + 1·1 = 6（j=2）</text>
<rect x="470.0" y="254.0" width="12.0" height="12.0" rx="3" fill="#a78bfa" opacity="1.0" filter="url(#f7-glow)"/>
<text x="492.0" y="265.0" font-size="13" fill="#a78bfa" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">C3</text>
<text x="546.0" y="265.0" font-size="12" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">conv 5×5, s1</text>
<text x="696.0" y="265.0" font-size="12.5" fill="#e6edf3" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">6 + 4·2 = 14</text>
<rect x="470.0" y="300.0" width="12.0" height="12.0" rx="3" fill="#a3e635" opacity="1.0" filter="url(#f7-glow)"/>
<text x="492.0" y="311.0" font-size="13" fill="#a3e635" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">S4</text>
<text x="546.0" y="311.0" font-size="12" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">pool 2×2, s2</text>
<text x="696.0" y="311.0" font-size="12.5" fill="#e6edf3" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">14 + 1·2 = 16（j=4）</text>
<rect x="470.0" y="346.0" width="12.0" height="12.0" rx="3" fill="#f472b6" opacity="1.0" filter="url(#f7-glow)"/>
<text x="492.0" y="357.0" font-size="13" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">C5</text>
<text x="546.0" y="357.0" font-size="12" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">conv 5×5, s1</text>
<text x="696.0" y="357.0" font-size="12.5" fill="#e6edf3" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">16 + 4·4 = 32</text>
<path d="M 470.0 396.0 L 912.0 396.0" fill="none" stroke="#222b36" stroke-width="1.1" opacity="1.0"/>
<text x="470.0" y="422.0" font-size="12.5" fill="#fbbf24" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">C5 的感受野剛好等於整張輸入 —— 不是巧合，是設計目標：</text>
<text x="470.0" y="444.0" font-size="12.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">1×1×120 要能代表「整張圖」，所以前面的堆疊必須把視野撐滿。</text>
</svg>
</figure>


C5 的感受野正好是 **32×32 = 整張輸入**。這不是巧合：如果最後一層的 1×1×120 要能代表「整張圖」，前面所有層的感受野就必須剛好撐滿。LeNet-5 的層數與核大小，是被這個目標反推出來的。

## 7. 反傳：梯度也是卷積

記 `Z = X ⊛ W`，上游梯度 `G = ∂L/∂Z`：

```
∂L/∂W[c_out, c, u, v] = Σ_{i,j} G[i,j,c_out] · X[c, i·S+u, j·S+v]     → X ⊛ G
∂L/∂b[c_out]         = Σ_{i,j} G[i,j,c_out]
∂L/∂X[c, p, q]       = Σ G[i,j,c_out] · W[c_out, c, u, v]             → G ⊛ rot180(W)，full
```

<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 470" role="img" aria-label="前向 X 卷積 W 得到 Z；反向時 ∂L/∂W 是 X 與 G 的卷積，∂L/∂X 是 G 與翻轉後 W 的卷積" style="width:100%;height:auto;display:block">
<defs>
<filter id="f8-glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="f8-soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="11" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="f8-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#1a2331" stroke-width="1"/></pattern>
<marker id="f8-arw-22d3ee" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#22d3ee"/></marker><marker id="f8-arw-f472b6" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#f472b6"/></marker><marker id="f8-arw-2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker><marker id="f8-arw-a78bfa" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#a78bfa"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="468.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<rect x="0.75" y="0.75" width="958.5" height="468.5" rx="16" fill="url(#f8-grid)" opacity="0.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">反傳：卷積的梯度，還是卷積</text>
<text x="48" y="80" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Z = X ⊛ W；把上游梯度記成 G = ∂L/∂Z，三條路各自是一條卷積</text>
<rect x="70.0" y="150.0" width="118.0" height="76.0" rx="10" fill="#101a26" opacity="1.0" stroke="#2dd4bf" stroke-width="1.8" filter="url(#f8-glow)"/>
<text x="129.0" y="188.0" font-size="17" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">X</text>
<text x="129.0" y="208.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">輸入</text>
<rect x="330.0" y="150.0" width="118.0" height="76.0" rx="10" fill="#101a26" opacity="1.0" stroke="#22d3ee" stroke-width="1.8" filter="url(#f8-glow)"/>
<text x="389.0" y="188.0" font-size="17" fill="#22d3ee" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">Z = X ⊛ W</text>
<text x="389.0" y="208.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">特徵圖</text>
<rect x="646.0" y="150.0" width="118.0" height="76.0" rx="10" fill="#101a26" opacity="1.0" stroke="#fbbf24" stroke-width="1.8" filter="url(#f8-glow)"/>
<text x="705.0" y="188.0" font-size="17" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">L</text>
<text x="705.0" y="208.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">損失</text>
<path d="M 190.0 188.0 L 328.0 188.0" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#f8-arw-2dd4bf)"/>
<text x="259.0" y="178.0" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">⊛ W</text>
<path d="M 450.0 188.0 L 644.0 188.0" fill="none" stroke="#22d3ee" stroke-width="2" marker-end="url(#f8-arw-22d3ee)"/>
<text x="547.0" y="178.0" font-size="12" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">前向</text>
<rect x="330.0" y="62.0" width="118.0" height="62.0" rx="10" fill="#2a1020" opacity="1.0" stroke="#f472b6" stroke-width="1.8" filter="url(#f8-glow)"/>
<text x="389.0" y="90.0" font-size="17" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">W</text>
<text x="389.0" y="110.0" font-size="10.5" fill="#c79ab0" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">濾波器</text>
<path d="M 389.0 148.0 L 389.0 126.0" fill="none" stroke="#f472b6" stroke-width="1.6" marker-end="url(#f8-arw-f472b6)"/>
<rect x="646.0" y="300.0" width="118.0" height="62.0" rx="10" fill="#132030" opacity="1.0" stroke="#a78bfa" stroke-width="1.8" filter="url(#f8-glow)"/>
<text x="705.0" y="328.0" font-size="14" fill="#a78bfa" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">G = ∂L/∂Z</text>
<text x="705.0" y="348.0" font-size="10.5" fill="#a99bd0" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">上游梯度</text>
<path d="M 705.0 226.0 L 705.0 296.0" fill="none" stroke="#a78bfa" stroke-width="2" marker-end="url(#f8-arw-a78bfa)"/>
<path d="M 646.0 316.0 L 454.0 100.0" fill="none" stroke="#f472b6" stroke-width="2" marker-end="url(#f8-arw-f472b6)" stroke-dasharray="6 5"/>
<text x="436.0" y="254.0" font-size="12.5" fill="#f472b6" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">∂L/∂W = X ⊛ G</text>
<path d="M 646.0 340.0 L 196.0 232.0" fill="none" stroke="#2dd4bf" stroke-width="2" marker-end="url(#f8-arw-2dd4bf)" stroke-dasharray="6 5"/>
<text x="392.0" y="322.0" font-size="12.5" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="middle">∂L/∂X = G ⊛ rot180(W)</text>
<rect x="48.0" y="372.0" width="864.0" height="76.0" rx="10" fill="#0b1017" opacity="1.0" stroke="#222b36" stroke-width="1.1"/>
<text x="70.0" y="398.0" font-size="12" fill="#9fb0c0" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">權重梯度是卷積：卷積對 W 是線性的，而且同一組 W 被所有位置共用，所以每個位置的梯度要「加總」回同一個 W。</text>
<text x="70.0" y="420.0" font-size="12" fill="#9fb0c0" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">輸入梯度要 padding：每個像素貢獻了好幾個輸出位置，回傳時必須把重疊部分疊起來（full convolution，步長 S）。</text>
<text x="70.0" y="440.0" font-size="12" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">∂L/∂b = Σ G：偏置對每個位置都一樣，梯度就是所有位置加起來。</text>
</svg>
</figure>


三個推論，考試很愛考：

1. **權重梯度是「輸入」與「輸出梯度」的卷積**。因為權重共享，所有位置的梯度會加總回同一組 `W`—— 這就是為什麼 `∂L/∂W` 是一條卷積而不是逐點的乘積。
2. **輸入梯度需要 padding**：一個像素貢獻了好幾個輸出位置，回傳時必須把重疊部分疊起來（full convolution，步長 S）。這也是為什麼 `∂L/∂X` 用得到 `rot180(W)`。
3. **邊界收到的梯度比較弱**：補的 0 不貢獻梯度。

池化的梯度只做路由：max 把梯度整包給 argmax 的位置，avg 平均分給窗口內每個像素（`G/k²`）。


## 8. 簡報只點名、沒有展開的那一塊：九個應用

第 4 個模組列了九個應用（語義分割、人臉、自駕、上色、場景優化、超解析、醫學、生物、基因組），但整份簡報在反傳那頁就結束了 —— 這九個其實只出現在目錄上。我把它們整理成一張圖，並標上各自用到 CNN 的哪個部位：

<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 640" role="img" aria-label="九宮格列出簡報點名的九個 CNN 應用：語義分割、人臉、自駕、上色、場景優化、超解析、醫學、生物、基因組" style="width:100%;height:auto;display:block">
<defs>
<filter id="f9-glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="f9-soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="11" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="f9-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#1a2331" stroke-width="1"/></pattern>
<marker id="f9-arw-22d3ee" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#22d3ee"/></marker><marker id="f9-arw-a78bfa" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#a78bfa"/></marker><marker id="f9-arw-f472b6" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#f472b6"/></marker><marker id="f9-arw-fbbf24" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#fbbf24"/></marker><marker id="f9-arw-a3e635" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#a3e635"/></marker><marker id="f9-arw-2dd4bf" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker></defs>
<rect x="0.75" y="0.75" width="958.5" height="638.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<rect x="0.75" y="0.75" width="958.5" height="638.5" rx="16" fill="url(#f9-grid)" opacity="0.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">第 4 個模組：同一個積木，九種用途</text>
<text x="48" y="80" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">(Conv+ReLU+Pool)×N + FC —— 換的是資料與損失函數，不是架構</text>
<rect x="48.0" y="112.0" width="272.0" height="150.0" rx="12" fill="#0d1621" opacity="1.0" stroke="#22d3ee55" stroke-width="1.3"/>
<rect x="73" y="141" width="42" height="42" rx="4" fill="none" stroke="#22d3ee" stroke-width="1.8" opacity="0.55"/><path d="M73 164 L88 153 L98 165 L115 154 L115 183 L73 183 Z" fill="#22d3ee" opacity="0.32"/><path d="M73 164 L88 153 L98 165 L115 154" fill="none" stroke="#22d3ee" stroke-width="2"/><text x="132.0" y="156.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">語義分割</text>
<text x="132.0" y="176.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">逐像素分類：</text>
<text x="68.0" y="216.0" font-size="10.5" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">H×W×C → H×W×classes</text>
<path d="M 68.0 232.0 L 300.0 232.0" fill="none" stroke="#222b36" stroke-width="1" opacity="1.0"/>
<text x="68.0" y="250.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">第 4 模組</text>
<text x="300.0" y="250.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">#1</text>
<rect x="344.0" y="112.0" width="272.0" height="150.0" rx="12" fill="#0d1621" opacity="1.0" stroke="#a78bfa55" stroke-width="1.3"/>
<circle cx="390" cy="162" r="13" fill="none" stroke="#a78bfa" stroke-width="1.8"/><circle cx="385.5" cy="158" r="1.9" fill="#a78bfa"/><circle cx="394.5" cy="158" r="1.9" fill="#a78bfa"/><path d="M385 167 Q390 172 395 167" fill="none" stroke="#a78bfa" stroke-width="1.7"/><path d="M364 136 l7 0 M364 136 l0 7" fill="none" stroke="#a78bfa" stroke-width="2" opacity="0.8"/><path d="M416 136 l-7 0 M416 136 l0 7" fill="none" stroke="#a78bfa" stroke-width="2" opacity="0.8"/><path d="M364 188 l7 0 M364 188 l0 -7" fill="none" stroke="#a78bfa" stroke-width="2" opacity="0.8"/><path d="M416 188 l-7 0 M416 188 l0 7" fill="none" stroke="#a78bfa" stroke-width="2" opacity="0.8"/><text x="428.0" y="156.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">人臉偵測 / 識別</text>
<text x="428.0" y="176.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">偵測＝錨框；識別＝嵌入＋度量學習</text>
<text x="364.0" y="216.0" font-size="10.5" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">偵測＝錨框；識別＝嵌入＋度量學習</text>
<path d="M 364.0 232.0 L 596.0 232.0" fill="none" stroke="#222b36" stroke-width="1" opacity="1.0"/>
<text x="364.0" y="250.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">第 4 模組</text>
<text x="596.0" y="250.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">#2</text>
<rect x="640.0" y="112.0" width="272.0" height="150.0" rx="12" fill="#0d1621" opacity="1.0" stroke="#f472b655" stroke-width="1.3"/>
<path d="M665 183 L680 141 L692 141 L707 183" fill="none" stroke="#f472b6" stroke-width="1.6" opacity="0.6"/><path d="M686 146 L686 159 M686 167 L686 179" stroke="#f472b6" stroke-width="2" stroke-dasharray="4 4"/><rect x="678" y="161" width="16" height="10" rx="2" fill="none" stroke="#f472b6" stroke-width="1.8"/><text x="724.0" y="156.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">自動駕駛</text>
<text x="724.0" y="176.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">即時偵測＋分割＋深度</text>
<text x="660.0" y="216.0" font-size="10.5" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">即時偵測＋分割＋深度</text>
<path d="M 660.0 232.0 L 892.0 232.0" fill="none" stroke="#222b36" stroke-width="1" opacity="1.0"/>
<text x="660.0" y="250.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">第 4 模組</text>
<text x="892.0" y="250.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">#3</text>
<rect x="48.0" y="286.0" width="272.0" height="150.0" rx="12" fill="#0d1621" opacity="1.0" stroke="#fbbf2455" stroke-width="1.3"/>
<circle cx="94" cy="336" r="21" fill="#fbbf24" opacity="0.18"/><path d="M94 315 A 21 21 0 0 0 94 357 Z" fill="#3a4550"/><path d="M94 315 A 21 21 0 0 1 94 357 Z" fill="#fbbf24" opacity="0.85"/><circle cx="94" cy="336" r="21" fill="none" stroke="#fbbf24" stroke-width="1.6"/><path d="M94 315 L94 357" stroke="#fbbf24" stroke-width="1.4" opacity="0.7"/><text x="132.0" y="330.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">影像上色</text>
<text x="132.0" y="350.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">L → a, b 通道迴歸</text>
<text x="68.0" y="390.0" font-size="10.5" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">L → a, b 通道迴歸</text>
<path d="M 68.0 406.0 L 300.0 406.0" fill="none" stroke="#222b36" stroke-width="1" opacity="1.0"/>
<text x="68.0" y="424.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">第 4 模組</text>
<text x="300.0" y="424.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">#4</text>
<rect x="344.0" y="286.0" width="272.0" height="150.0" rx="12" fill="#0d1621" opacity="1.0" stroke="#a3e63555" stroke-width="1.3"/>
<path d="M369 325 L411 325" stroke="#a3e635" stroke-width="1.6" opacity="0.55"/><circle cx="383" cy="325" r="4" fill="#a3e635"/><path d="M369 336 L411 336" stroke="#a3e635" stroke-width="1.6" opacity="0.55"/><circle cx="395" cy="336" r="4" fill="#a3e635"/><path d="M369 347 L411 347" stroke="#a3e635" stroke-width="1.6" opacity="0.55"/><circle cx="388" cy="347" r="4" fill="#a3e635"/><text x="428.0" y="330.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">場景／照片優化</text>
<text x="428.0" y="350.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">反傳進「影像」，不只調權重</text>
<text x="364.0" y="390.0" font-size="10.5" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">反傳進「影像」，不只調權重</text>
<path d="M 364.0 406.0 L 596.0 406.0" fill="none" stroke="#222b36" stroke-width="1" opacity="1.0"/>
<text x="364.0" y="424.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">第 4 模組</text>
<text x="596.0" y="424.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">#5</text>
<rect x="640.0" y="286.0" width="272.0" height="150.0" rx="12" fill="#0d1621" opacity="1.0" stroke="#2dd4bf55" stroke-width="1.3"/>
<rect x="665" y="338" width="11" height="11" rx="2" fill="none" stroke="#2dd4bf" stroke-width="1.6" opacity="0.6"/><rect x="687" y="330" width="20" height="20" rx="3" fill="none" stroke="#2dd4bf" stroke-width="2"/><path d="M678 342 L684 335" stroke="#2dd4bf" stroke-width="1.6" marker-end="url(#f9-arw-2dd4bf)"/><text x="724.0" y="330.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">超解析（放大）</text>
<text x="724.0" y="350.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">轉置卷積／sub-pixel 上採樣</text>
<text x="660.0" y="390.0" font-size="10.5" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">轉置卷積／sub-pixel 上採樣</text>
<path d="M 660.0 406.0 L 892.0 406.0" fill="none" stroke="#222b36" stroke-width="1" opacity="1.0"/>
<text x="660.0" y="424.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">第 4 模組</text>
<text x="892.0" y="424.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">#6</text>
<rect x="48.0" y="460.0" width="272.0" height="150.0" rx="12" fill="#0d1621" opacity="1.0" stroke="#f472b655" stroke-width="1.3"/>
<rect x="71" y="489" width="46" height="42" rx="5" fill="none" stroke="#f472b6" stroke-width="1.4" opacity="0.5"/><path d="M73 510 L87 510 L91 499 L96 521 L100 506 L103 510 L115 510" fill="none" stroke="#f472b6" stroke-width="2"/><text x="132.0" y="504.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">醫學影像</text>
<text x="132.0" y="524.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">X 光、CT、MRI（常為 3D）</text>
<text x="68.0" y="564.0" font-size="10.5" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">X 光、CT、MRI（常為 3D）</text>
<path d="M 68.0 580.0 L 300.0 580.0" fill="none" stroke="#222b36" stroke-width="1" opacity="1.0"/>
<text x="68.0" y="598.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">第 4 模組</text>
<text x="300.0" y="598.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">#7</text>
<rect x="344.0" y="460.0" width="272.0" height="150.0" rx="12" fill="#0d1621" opacity="1.0" stroke="#a78bfa55" stroke-width="1.3"/>
<circle cx="390" cy="510" r="21" fill="#a78bfa" opacity="0.10"/><circle cx="390" cy="510" r="21" fill="none" stroke="#a78bfa" stroke-width="1.8"/><circle cx="386" cy="507" r="5" fill="none" stroke="#a78bfa" stroke-width="1.5"/><circle cx="396" cy="506" r="1.9" fill="#a78bfa"/><circle cx="397" cy="516" r="1.9" fill="#a78bfa"/><circle cx="388" cy="518" r="1.9" fill="#a78bfa"/><circle cx="382" cy="512" r="1.9" fill="#a78bfa"/><text x="428.0" y="504.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">生物影像</text>
<text x="428.0" y="524.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">顯微鏡、細胞分割、連接體</text>
<text x="364.0" y="564.0" font-size="10.5" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">顯微鏡、細胞分割、連接體</text>
<path d="M 364.0 580.0 L 596.0 580.0" fill="none" stroke="#222b36" stroke-width="1" opacity="1.0"/>
<text x="364.0" y="598.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">第 4 模組</text>
<text x="596.0" y="598.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">#8</text>
<rect x="640.0" y="460.0" width="272.0" height="150.0" rx="12" fill="#0d1621" opacity="1.0" stroke="#22d3ee55" stroke-width="1.3"/>
<path d="M677 489 C699 502 673 518 695 531" fill="none" stroke="#22d3ee" stroke-width="2"/><path d="M695 489 C673 502 699 518 677 531" fill="none" stroke="#22d3ee" stroke-width="2" opacity="0.75"/><path d="M682.64 497 L689.36 497" stroke="#22d3ee" stroke-width="1.3" opacity="0.6"/><path d="M680.68 504 L691.32 504" stroke="#22d3ee" stroke-width="1.3" opacity="0.6"/><path d="M679.0 510 L693.0 510" stroke="#22d3ee" stroke-width="1.3" opacity="0.6"/><path d="M680.68 516 L691.32 516" stroke="#22d3ee" stroke-width="1.3" opacity="0.6"/><path d="M682.64 523 L689.36 523" stroke="#22d3ee" stroke-width="1.3" opacity="0.6"/><text x="724.0" y="504.0" font-size="14.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">基因組</text>
<text x="724.0" y="524.0" font-size="10.5" fill="#8b949e" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">一維卷積掃 DNA／染色質軌跡</text>
<text x="660.0" y="564.0" font-size="10.5" fill="#9aa7b6" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">一維卷積掃 DNA／染色質軌跡</text>
<path d="M 660.0 580.0 L 892.0 580.0" fill="none" stroke="#222b36" stroke-width="1" opacity="1.0"/>
<text x="660.0" y="598.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">第 4 模組</text>
<text x="892.0" y="598.0" font-size="9.5" fill="#4d5a6b" font-weight="400" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0" text-anchor="end">#9</text>
<text x="48.0" y="616.0" font-size="12" fill="#fbbf24" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif" opacity="1.0">九個任務共用同一個前處理器 —— 這就是「一個架構重複使用」的意思；代價是每個任務都要自己的標註資料。</text>
</svg>
</figure>


三個值得補上的觀察：

**一、能共用是因為歸納偏置一樣。** 局部性（每個濾波器只看一個 patch）＋平移等變（同一個濾波器掃全圖），這兩個假設在自然影像、醫學影像、顯微鏡影像、甚至 DNA 序列的「局部模體」上都成立，所以同一組積木可以直接搬。真正不能搬的是 **1D/3D 的維度約定**：基因組要一維卷積、CT 要三維卷積，但卷積的定義本身沒變。

**二、差異幾乎都在「輸出頭」與損失函數，不在骨幹。**

| 任務 | 輸出頭 | 損失 |
| --- | --- | --- |
| 分類 / 識別 | softmax over classes（或嵌入向量） | 交叉熵 / triplet、center loss |
| 語義分割 | 每個像素一組類別 | 逐像素交叉熵 + Dice |
| 偵測 | 框迴歸 + 物件性分數 | smooth L1 + 物件性 BCE |
| 上色 | 兩個通道 `a, b` | L1 / L2（或對抗損失） |
| 超解析 | 高解析像素 | L1 + 感知 / 對抗損失 |
| 場景 / 照片優化 | **輸入本身**（要優化的是像素，不是權重） | 任務定義的目標函數 |

最後那一列是很容易被忽略的用法：把網路固定住，反傳到**影像**而不是權重 —— 這就是「用 CNN 調整照片／場景」的意思，也是對抗樣本與特徵視覺化（Grad-CAM、deep dream）的共同機制。

**三、代價是標註，不是算力。** 九個任務裡，分類只要一個標籤；分割要逐像素遮罩；醫學影像還要放射科醫師。這也是為什麼預訓練骨幹 + 少量微調會變成常態 —— 骨幹學到的邊緣、紋理、部件，在九個任務之間是可以轉移的。

<a id="errata"></a>

## 9. 我在簡報上抓到的七個錯

這一段是我重算時的副產品。不是要挑剔，而是這些數字如果照抄，考試或報告會出事：

| # | 頁 | 簡報寫的 | 正確 / 說明 |
| --- | --- | --- | --- |
| 1 | 9 | 1080×1080×3 的圖是「1,166,400 維」 | `1080² = 1,166,400` 是**灰階**；RGB 是 `3,499,200`。同一頁同時寫了 `×3` 與灰階的數字。 |
| 2 | 12 | 86 億神經元 → 「1 quadrillion (10¹²) 條連線」 | `86×10⁹ × 10⁴ = 8.6×10¹⁴`，約 0.86 quadrillion。`10¹²` 是**一兆**，級數與單位對不上（乘積對，標籤錯）。 |
| 3 | 35 | LeNet-5「只有 60K 參數」 | 逐層加起來是 **61,750**（四捨五入可以說 60K，但不是 60,000）。 |
| 4 | 34 | 第 5 層標成 `FC` | 它是 5×5 卷積，把 5×5×16 壓成 1×1×120。數值上等價於 FC，但概念上是卷積。 |
| 5 | 19 | 「每 2 個像素移動一次」 | 那就是 **stride = 2**；整份簡報到第 34 頁才第一次出現「步長」這個詞。 |
| 6 | 1 | 版權頁「2015年X月」 | 樣板殘留（`X` 沒填）；其餘每一頁都是 **2026年2月**。 |
| 7 | 20 / 22 | 兩頁同名「Fully Connected Neural Network」 | 22 是 20 的插圖，中間夾了一頁特徵示意（21），順序錯位。 |

另外兩個「說得比較鬆」的地方，答題時最好講精確：

- **「卷積」**在深度學習其實是互相關（不翻轉核）。翻不翻轉對學出來的權重沒影響，但對訊號處理的性質、以及手推梯度有影響。
- **池化不是可學習的**（現代意義上）。LeNet-5 的平均池化帶可訓練的縮放與偏置係數，所以它的參數量有時會被算得比「純池化」多一些。

## 10. 一頁公式表

```
影像
  H×W×C，值 0–255        1080² = 1,166,400 ；1080²×3 = 3,499,200

卷積輸出尺寸
  out = ⌊(N + 2P − F)/S⌋ + 1
  same，S=1：P = (F−1)/2 ；full：P = F−1

參數量
  卷積：(F·F·C_in + 1) · C_out
  全連接：(n_in + 1) · n_out
  池化：0（可訓練平均池化則每張特徵圖 2 個）

計算量（乘加）
  卷積：H_out · W_out · C_out · F·F · C_in
  全連接：n_in · n_out

感受野
  r_out = r_in + (k−1)·j_in ，j_out = j_in·S ，r₀ = j₀ = 1

反傳（Z = X ⊛ W，G = ∂L/∂Z）
  ∂L/∂W = X ⊛ G                    ← 所有位置加總回同一組權重
  ∂L/∂b = Σ G
  ∂L/∂X = G ⊛ rot180(W)，stride S，補到 full

標準積木
  (Conv → ReLU → Pool) × N → Flatten → FC × M → softmax
```

## 11. 如果只記三件事

1. **卷積 = 局部連接 + 參數共享。** 前者讓你只看鄰居，後者讓你不用為每個位置重新學一次。兩個加起來，才會有「參數量與影像大小無關」這個性質。
2. **深度不是為了更深，是為了更大的感受野。** LeNet-5 把 5→6→14→16→32 疊到剛好等於輸入尺寸，這是一個可以被反推的設計目標，不是玄學。
3. **梯度也是卷積。** 因為權重共享，`∂L/∂W` 要把所有位置的貢獻加起來；因為一個像素貢獻多個輸出，`∂L/∂X` 要把重疊疊起來。

## 12. 參考與素材

- LeCun, Bottou, Bengio & Haffner, *Gradient-Based Learning Applied to Document Recognition*, 1998 —— LeNet-5 原始論文。
- Goodfellow, Bengio & Courville, *Deep Learning*, 2016 —— 簡報第 26 頁的邊緣核示意出自此。
- Lee et al., ICML 2009 —— 「從資料學出特徵階層」的視覺化。
- 「卷積神經網絡 I」課程簡報（36 頁）。
- 本文的 9 張插圖是用 Python 產生、全部純 SVG（無點陣圖），霓虹配色沿用站上的 `#22d3ee` / `#f472b6`；封面由本地 ComfyUI 的 Qwen-Image 2.1 生成，無外部 API。

> 這一講只到「卷積的反向傳播」為止，第 4 個模組（語義分割、人臉、自駕、上色、超解析、醫學、基因組）只點名沒有展開 —— 我在第 8 節補了一張總覽，真正展開應該是下一講 CNN II 的事。


