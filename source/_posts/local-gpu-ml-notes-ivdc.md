---
title: Using Local GPU for Machine Learning 學習筆記：IVDC 課程完整複習 + 60 題 MC 模擬試卷
date: 2026-10-10 23:00:00
categories:
  - 學習資源
tags:
  - GPU
  - CUDA
  - cuDNN
  - PyTorch
  - IVDC
  - 學習筆記
index_img: /img/covers/local-gpu-ml-notes-ivdc.png
banner_img: /img/covers/local-gpu-ml-notes-ivdc.png
---

最近為了準備 IVDC（匯縱專業發展中心）「Certificate in Application of Computer Vision Technology」的考試，我把課程教材《IVDC_Using Local GPU for ML.pptx》（26 頁）完整重寫成一份可離線閱讀的學習筆記，並額外做了一份 60 題的 MC 模擬試卷。

筆記已發佈成獨立專題頁面：

**👉 [Using Local GPU for ML 學習筆記（考試溫習版）](/local-gpu-ml-notes/)**

<!-- more -->

---

## 這份筆記包含什麼

按 PDF 原稿的每一個標題逐一填充，涵蓋全部 20 個步驟：

| 章節 | 主題 |
|---|---|
| 1–2 | Nvidia 驅動、Visual Studio C++（MSVC） |
| 3–5 | Anaconda、Anaconda Prompt、Anaconda PATH |
| 6–8 | 確認 CUDA 版本、CUDA Toolkit |
| 9–11 | cuDNN、複製 bin / lib / include 到 CUDA |
| 12 | 檢查環境變數（`CUDA_PATH`） |
| 13–14 | Visual Studio Code、Git |
| 15 | 安裝 PyTorch（GPU 版） |
| 16–18 | VS Code 選 Interpreter、Bash Shell、官方 Python |
| 19 | **Check GPU（PyTorch 程式碼）** |
| 20 | 補 PATH |

另外補了 8 個附錄：**指令速查表**、**常見錯誤與陷阱**、**模擬試題**、**教材頁面索引對照**、**離線安裝提示**、**一頁精華（考前 10 分鐘）**、**60 題 MC 模擬試卷**、**答錯題目 → 複習章節對照**。

---

## 原稿幾乎全是截圖，筆記補上「指令與驗證」

這份教材是 PowerPoint 匯出的 PDF，**幾乎每頁都是安裝精靈的截圖**（只有第 25 頁有程式碼）。
筆記把每一步補上「**目的、要做什麼、用什麼指令、如何驗證**」，讓沒有截圖也能照著做。

**本機實測環境（Windows）**：

```text
GPU       NVIDIA GeForce RTX 4090 (24564 MiB)
驅動      617.42（CUDA UMD 13.4）
CUDA      nvcc release 13.4 (V13.4.92)
PyTorch   2.14.1+cu132（cuda_available = True, device_count = 1）
conda     24.9.2
git       2.53.0.windows.2
```

---

## 重點：60 題 MC 模擬試卷

因為考試可能是選擇題形式，我特別做了一份**完整計時模擬試卷**（附錄 G）：

| 資源 | 連結 |
|---|---|
| 📝 60 題試卷（不附答案，先做再看） | [開始作答](/local-gpu-ml-notes/#附錄-gmc-模擬試卷60-題) |
| ✅ 答案速查表（6×10 網格，方便自我評分） | [對答案](/local-gpu-ml-notes/#g5-答案速查表) |
| 💡 逐題詳解（說明為何正確、其他選項錯在哪） | [看詳解](/local-gpu-ml-notes/#g6-逐題詳解) |
| 🖱️ 互動測驗版（即時計分、進度自動儲存） | [前往測驗](/local-gpu-ml-notes/mc-quiz.html) |

**試卷設計**

- 60 題單選、滿分 60 分、建議 75 分鐘
- 分三部分：安裝前置與環境（1–20）、CUDA 與 cuDNN（21–40）、工具／PyTorch 與排錯（41–60）
- 答案分佈刻意打散（A/B/C/D 各 15 題），避免整排猜同一個字母
- 每題詳解都附「答錯題目 → 對應複習章節」對照，方便回頭補強

> 出題率最高的考點包括：**安裝順序**（驅動 → 編譯器/Anaconda → CUDA/cuDNN → PyTorch）、**`nvidia-smi` 與 `nvcc --version` 的差別**（驅動上限 vs 實際 Toolkit）、**cuDNN 要複製 `bin` + `include` + `lib\x64` 三份**、**Anaconda PATH 要含 `Scripts` 與 `Library\bin`**、**PyTorch 的 `+cuXXX` 才是 GPU 版**、以及 **`torch.cuda.is_available()` 回 `True` 才算成功**。

---

## 離線也能用

筆記是**單一 HTML 檔、零外部資源**（CSS 與語法高亮全部內嵌），下載後直接雙擊就能看，適合考前在沒有網路的環境複習。

也可以下載原始 Markdown：

**📄 [Using_Local_GPU_for_ML_Study_Notes.md](/local-gpu-ml-notes/Using_Local_GPU_for_ML_Study_Notes.md)**

---

## 建議使用順序

1. 先讀完第 1–20 節，把附錄 A（指令速查表）當工具書隨時查
2. 做附錄 C 的 36 題（隨讀隨測，每題下方有摺疊答案）
3. 找個安靜的 75 分鐘，完整做一次**附錄 G 的 60 題模擬試卷**（或用互動測驗版）
4. 考前 10 分鐘只看**附錄 F 一頁精華**

祝考試順利。

---

*本篇為個人學習筆記整理，教材內容版權屬匯縱專業發展中心（IVDC）所有。*
