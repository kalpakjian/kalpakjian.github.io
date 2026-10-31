---
title: "激活函數與池化層：ReLU 家族、Max／Average Pooling 與 GAP"
date: 2026-10-30 08:00:00
archive: true   # 獨立圖解文章；入口在 /cv-course/ 第 7–8 節與兩篇前作的附錄 C
categories:
  - 學習資源
tags:
  - CNN
  - 卷積神經網路
  - 深度學習
  - 電腦視覺
  - 圖解
toc: true
index_img: /img/covers/cnn-activation-pooling.png
banner_img: /img/covers/cnn-activation-pooling.png
---

> <strong>一句話版本</strong>：ReLU 決定「哪些特徵響應要留下」，池化決定「在多大範圍內留下最強或平均的響應」；<strong>兩者都沒有可學習的參數</strong>。

系列第三篇。前兩篇談卷積本身（[圖解 CNN](/cnn-illustrated/)、[卷積層的運作細節](/cnn-conv-details/)），
這一篇只談接在卷積後面的兩層：把線性結果轉成非線性的激活函數，以及把解析度降下來的池化。

<!-- more -->

**👉 [看完整圖解](/cnn-activation-pooling/)** ｜ [下載原始 Markdown](/cnn-activation-pooling/CNN_Activation_Pooling_Study_Notes.md)

五張圖全部是手繪內嵌 SVG：ReLU／Leaky ReLU／GELU 的折線、4×4 → 2×2 的最大池化、
三種池化設定的輸出尺寸、GAP、一個 block 的形狀流。

幾個實測數字（NumPy 2.5.4 / Python 3.15.1，程式與原始輸出在文末附錄）：

- **沒有非線性，多層等於一層**：兩層線性與合併成一層的結果，最大差異只有 **4.44e-16**
- ReLU 之後約 **50.0%** 的格子是 0（標準常態 1000×1000 實測）——稀疏是設計，不是 bug
- 「死亡 ReLU」的判定是**對所有輸入都輸出 0**：同一顆神經元 bias 25.54 還活著（最大 25.54），bias 52.08 才是全 0
- 最大池化 4×4 → 2×2：`[[1,1,2,4],[5,6,7,8],[3,2,1,0],[1,2,3,4]]` → `[[6,8],[3,4]]`（16 → 4，少 75%）
- 同一個窗口 `[[2,7],[1,5]]`：Max 取 **7**、Average 取 **3.75**
- Max Pooling 的梯度只回給冠軍：數值梯度檢查與解析版本完全一致，總和守恆
- GAP 取代 Flatten：`7×7×512 → 10` 從 **250,890** 個參數降到 **5,130**

另外補了兩個容易踩的細節：**Max Pooling 補邊是補 −∞（不是 0）**，以及
**池化的反向傳播有梯度、只是全部走一條路**。
