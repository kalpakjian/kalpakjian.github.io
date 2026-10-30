---
title: "全連接層的運作：Wx + b、Flatten、參數量為什麼爆炸、Softmax 的三個性質"
date: 2026-10-30 08:40:00
archive: true   # 獨立圖解文章；入口在 /cv-course/ 第 7–8 節與前三篇的附錄 C
categories:
  - 學習資源
tags:
  - CNN
  - 卷積神經網路
  - 深度學習
  - 電腦視覺
  - 圖解
toc: true
index_img: /img/covers/cnn-fully-connected.png
banner_img: /img/covers/cnn-fully-connected.png
---

> <strong>一句話版本</strong>：全連接層就是<strong>一次矩陣乘法加 bias</strong>（`z = Wx + b`），把 CNN 學到的特徵「加權投票」成類別分數；softmax 再把分數變成加總為 1 的機率。

系列第四篇，也是最後一哩。前三篇談卷積與池化（[圖解 CNN](/cnn-illustrated/)、[卷積層的運作細節](/cnn-conv-details/)、[激活函數與池化層](/cnn-activation-pooling/)），
這一篇談把特徵向量變成類別分數的那一層——順便把「為什麼 CNN 的參數幾乎都在這裡」算清楚。

<!-- more -->

**👉 [看完整圖解](/cnn-fully-connected/)** ｜ [下載原始 Markdown](/cnn-fully-connected/CNN_Fully_Connected_Study_Notes.md)

五張圖全部是手繪內嵌 SVG：`Wx + b` 的矩陣佈局、Flatten 的形狀流、參數量長條圖、
softmax 的機率條、以及最後那張「加權投票」示意。

幾個實測數字（NumPy 2.5.4 / Python 3.15.1，程式與原始輸出在文末附錄）：

- 4 輸入 3 輸出的手算例子：`z = [2.4, 1.2, −0.7]`（logits 可以是負的）
- 這個小層的參數量：`W` 12 個 + `b` 3 個 = **15**
- `7×7×64 → 3136`，flatten **沒有參數**
- `3136 → 128` 是 **401,536** 個參數；同一個小 CNN 的卷積層只有 **1,248** 個，全連接占全部參數 **97.6%**
- softmax 實測：`[2.4, 1.2, −0.7] → [0.7428, 0.2237, 0.0335]`，總和 **1.000000**
- softmax 三個性質都驗過：總和 1、保序（argmax 不變）、**平移不變**（全部 logits +100，機率完全相同）
- 梯度 `∂L/∂W = δxᵀ`、`∂L/∂x = Wᵀδ`，中心差分檢查**完全一致**

順帶一個常在網路上看到的錯誤：`[2.4, 1.5, 1.1]` 這組 logits 算出來的 `z₂`、`z₃` 其實是 **1.2** 與 **−0.7**；
而「`[2.4, 1.5, 1.1]` → `[0.55, 0.22, 0.15]`」那組機率加起來只有 **0.92**，不可能是 softmax 的輸出。
