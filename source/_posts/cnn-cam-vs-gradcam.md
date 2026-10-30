---
title: "CAM vs Grad-CAM：同一個熱圖，只差權重怎麼來"
date: 2026-10-30 12:00:00
archive: true   # 獨立圖解文章；入口在 /cv-course/ 第 7–8 節與 CAM／Grad-CAM 兩篇
categories:
  - 學習資源
tags:
  - CNN
  - 卷積神經網路
  - 深度學習
  - 電腦視覺
  - 可解釋性
  - Grad-CAM
  - 圖解
toc: true
index_img: /img/covers/cnn-cam-vs-gradcam.png
banner_img: /img/covers/cnn-cam-vs-gradcam.png
---

> <strong>一句話版本</strong>：兩者的熱圖公式一模一樣，差別只在「那 K 個權重是訓練好的參數，還是推論時算的梯度」。

系列第九篇。前面分別寫了 [CAM](/cnn-cam/) 與 [Grad-CAM](/cnn-gradcam/) 的完整流程；這一篇只做對照：
**九個面向的差異、為什麼 CAM 一定要 GAP、以及「α 隨影像改變」這句話的但書。**

<!-- more -->

**👉 [看完整圖解](/cnn-cam-vs-gradcam/)** ｜ [下載原始 Markdown](/cnn-cam-vs-gradcam/CNN_CAM_vs_GradCAM_Study_Notes.md)

三張圖：公式並排、固定權重 vs 即時權重的實測、以及能力與成本。

實測數字（NumPy 2.5.4 / Python 3.15.1，程式與原始輸出在文末附錄）：

- **共同點**：`ReLU(Σ 權重 × 特徵圖)`；差異只有 `w[k,c]`（學來的）與 `α[k,c]`（算的）
- **純 GAP + Linear**：`α = w/(H·W)` → 兩張不同影像的 `α` **完全相同**（實測 `[0.075, −0.0312, 0.05]`），此時 Grad-CAM 就等於 CAM
- **中間有 ReLU**：`α = w/(H·W) × 正值比例` → 才隨影像變（影像 A `[0.0188, −0.0176, 0.0250]` vs 影像 B `[0.0375, −0.0137, 0.0312]`）
- **架構清單**：`Conv → Flatten → FC` 與 `Conv → 1×1 conv → GAP → Linear` 都只有 Grad-CAM 做得到
- **成本**：CAM 一次前向；Grad-CAM 每解釋一個類別多一次反向（1000 類全畫 = 1,000 次反向）

其中第二點是這篇最想講清楚的地方：網路上常說「Grad-CAM 的權重隨影像改變」，
但在**CAM 適用的那種末端**上它其實不變——那個性質來自網路裡的非線性，不是來自「Grad」這個字。
