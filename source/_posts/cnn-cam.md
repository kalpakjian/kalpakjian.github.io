---
title: "CAM：用 GAP 把「模型在看哪裡」算成一張熱圖"
date: 2026-10-30 10:40:00
archive: true   # 獨立圖解文章；入口在 /cv-course/ 第 7–8 節與 /cnn-gap-head/ 的 §8
categories:
  - 學習資源
tags:
  - CNN
  - 卷積神經網路
  - 深度學習
  - 電腦視覺
  - GAP
  - CAM
  - 可解釋性
  - 圖解
toc: true
index_img: /img/covers/cnn-cam.png
banner_img: /img/covers/cnn-cam.png
---

> <strong>一句話版本</strong>：GAP 把每張 feature map 壓成一個數，於是分類層的權重 `w[k, c]` 只綁一個通道——把它乘回那張圖再加總，就得到 CAM，也就是「模型在看哪裡」。

系列第七篇。上一篇（[GAP 是什麼](/cnn-gap-head/)）講 GAP 怎麼把特徵圖壓成一個數；這一篇講它附帶的禮物：
**因為「一張特徵圖 ↔ 一個數」這個對應，分類權重可以直接乘回特徵圖，變成一張熱圖。**

<!-- more -->

**👉 [看完整圖解](/cnn-cam/)** ｜ [下載原始 Markdown](/cnn-cam/CNN_CAM_Study_Notes.md)

四張圖：CAM 的網路結構（GAP 是那座橋）、三張 2×2 特徵圖的手算例子、五個步驟、CAM vs Grad-CAM。

實測數字（NumPy 2.5.4 / Python 3.15.1，程式與原始輸出在文末附錄）：

- **手算**：`A₁=[[10,0],[8,2]]`、`A₂=[[1,1],[1,1]]`、`A₃=[[0,2],[0,2]]`，權重 `0.8 / 0.1 / −0.2`
  → `CAM = [[8.1, −0.3], [6.5, 1.3]]`，平均 **3.9** = logit
- **恆等式**：`mean(CAM_c) = logit_c − bias_c`。隨機網路（K=6、7×7、C=4）實測最大差 **4.44e-16**；`bias = 0.5` 時 logit 4.40、mean(CAM) 3.90 ✓
- **為什麼一定要 GAP**：K=6、7×7、C=4 時，GAP 頭 **6** 個權重 vs 展平頭 **1,176** 個（196 倍），而且展平頭那些權重**綁的是像素不是通道**，定義上做不出 CAM
- **Grad-CAM**：在純 GAP＋Linear 的網路上，`α = w/(H·W)`、`Grad-CAM = ReLU(CAM/(H·W))`，實測最大差 **5.64e-18**——兩者是同一張圖

本篇也把幾個常見的誤解寫清楚：熱圖的**平均**才對到 logit（不是總和）、負值代表反對證據（不是 bug）、
以及熱圖只說「哪裡」不說「為什麼」。
