---
title: "CNN 2：卷積神經網路（二）學習筆記 — 從局部連接、ReLU、池化到可執行的實作"
date: 2026-10-29 03:30:00
archive: true   # 已歸入「電腦視覺課程」學習筆記（/cv-course/ 第 8 節），不列在首頁
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

筆記裡另外收了幾件「課堂上不會特別講、一動手就會撞到」的事：

- 課程示範碼有三個會直接報錯的寫法（彎引號、`filter_size`、缺 `Input`），附勘誤表與修正後可直接執行的版本
- 輸出尺寸靠 `(N + 2P − F)/S + 1` 一行算完；參數量九成八集中在攤平後的全連接層
- 「零激活 50.6%」與「死濾波器 0%」是兩件事——稀疏是常態，死亡要看是否**對所有輸入**都輸出 0

<!-- more -->

**👉 [看完整筆記](/cnn2-notes/)** ｜ [互動測驗 49 題](/cnn2-notes/mc-quiz.html)

延伸：[CNN 1 筆記](/cnn-notes/)（卷積的數學與 LeNet-5）、
[CNN II 實驗紀錄](/2026/10/29/cnn-2-experiments/)（簡報那段範例程式碼的 33 組 run，與課程內容無關）、
[CNN 專題：十個實驗，和三次被推翻的假設](/cnn-lab/)（CNN I 的 MNIST 專題）。

