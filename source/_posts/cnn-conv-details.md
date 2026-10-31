---
title: "卷積層的運作細節：一個輸出值、多通道、stride／padding、感受野、空洞卷積"
date: 2026-10-30 07:10:00
archive: true   # 獨立圖解文章；入口在 /cv-course/ 第 7–8 節與 /cnn-illustrated/ 附錄 C
categories:
  - 學習資源
tags:
  - CNN
  - 卷積神經網路
  - 深度學習
  - 電腦視覺
  - 圖解
toc: true
index_img: /img/covers/cnn-conv-details.png
banner_img: /img/covers/cnn-conv-details.png
---

> <strong>一句話版本</strong>：卷積層用同一組小 kernel 逐塊掃描——<strong>kernel 決定看什麼、stride 決定掃多快、padding 決定邊界怎麼處理、kernel 的數量決定輸出通道數</strong>。

[上一篇〈圖解 CNN〉](/cnn-illustrated/)把整個網路的資料流走過一遍；這一篇只拆**卷積層本身**，
把四個常在這裡卡住的細節算清楚：一個輸出值到底是怎麼來的、多通道的 kernel 為什麼有深度、
stride／padding 怎麼決定輸出尺寸、感受野與空洞卷積又是怎麼長出來的。

<!-- more -->

**👉 [看完整圖解](/cnn-conv-details/)** ｜ [下載原始 Markdown](/cnn-conv-details/CNN_Conv_Layer_Study_Notes.md)

五張圖全部是手繪內嵌 SVG：單一輸出值的計算、多通道 kernel 的相加、四種 stride/padding 設定、
感受野的同心方框、空洞卷積的取樣間隔。

幾個實測數字（NumPy 2.5.4 / Python 3.15.1，程式與原始輸出在文末附錄）：

- 5×5 輸入 + 3×3 kernel（stride 1、不補邊）→ 特徵圖 `[[8,5,8],[3,10,5],[6,4,5]]`，左上角 8 = 4 + 1 + 3；bias 1 時九格全部 +1
- 多通道：3×3×3 的 kernel 有 **27** 個權重；三個通道分別算出 3、2、−4，相加再加 bias 2 得 **3**
- `3×3、C_in 3 → C_out 64`：1,728 個權重 + 64 個 bias = **1,792** 個參數（與影像大小無關）
- 28×28 輸入配 3×3 kernel：valid **26×26**、same **28×28**、stride 2 補 1 **14×14**、stride 2 不補 **13×13**
- 感受野：四層 3×3、stride 1 → **3 → 5 → 7 → 9**；每層 stride 2 → **3 → 7 → 15 → 31**
- 空洞卷積 d = 2：覆蓋 **5×5** 但只有 9 個權重；28×28 p=0 輸出 **24×24**，p=2 輸出 **28×28**

另外整理了六個常見誤解（kernel 越大越強？輸出通道等於輸入通道？感受野等於輸出尺寸？），
以及一句最常被搞錯的：**通道是在「跨通道加總」那一步消失的，不是被池化掉的**。
