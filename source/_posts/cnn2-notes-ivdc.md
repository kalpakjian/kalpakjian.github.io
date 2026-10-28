---
title: "CNN 2：卷積神經網路（二）學習筆記 — 從局部連接、ReLU、池化到 33 組實測"
date: 2026-10-29 03:30:00
categories:
  - 學習資源
tags:
  - CNN
  - 深度學習
  - PyTorch
  - TensorFlow
  - 電腦視覺
index_img: /img/covers/cnn2-notes.png
banner_img: /img/covers/cnn2-notes.png
---

第二堂 CNN 把「一個可訓練的分類網路」從頭組起來：局部連接、輸出體積與步幅、
ReLU 的兩個經典問題、池化的降維與空間不變性、空洞卷積，最後用十行程式把模型寫出來。

我把課程那份程式碼真的跑起來，並往上加了三層對照（換架構、換正則化、換裝置），
累積 33 組實驗。幾個關鍵數字：

- 課程的模型在 CIFAR-10、20 輪的準確率約 **0.80**；換成小型 VGG 立刻到 **0.89**（參數反而更少）
- 200 輪長排程把 VGG + cutout 推到 **0.94**、ResNet-18 到 **0.96**
- dropout 只買到「train/val 差距減半」，準確率幾乎沒動
- 難類排序（貓 &lt; 狗 &lt; 鳥）在四種設定下完全沒變

課程那份程式碼另外有三個會直接報錯的地方（彎引號、`filter_size`、缺 `Input`），
筆記裡有一張勘誤表，以及修正後可直接執行的版本。

<!-- more -->

**👉 [看完整筆記](/cnn2-notes/)** ｜ [互動測驗 60 題](/cnn2-notes/mc-quiz.html)

延伸：[CNN 1 筆記](/cnn-notes/)（卷積的數學與 LeNet-5）、
[CNN 專題：十個實驗與三次被推翻的假設](/cnn-lab/)（實驗全紀錄）。
