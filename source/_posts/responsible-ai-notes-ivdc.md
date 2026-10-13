---
title: Responsible AI 學習筆記：IVDC 課程完整複習 + 60 題 MC 模擬試卷
archive: true   # 已歸入「專題：IVDC電腦視覺課程」，不列在首頁
date: 2026-10-12 18:00:00
categories:
  - 學習資源
tags:
  - 人工智慧
  - Responsible AI
  - 倫理
  - PDPO
  - IVDC
  - 學習筆記
  - 考試
index_img: /img/covers/responsible-ai-notes-ivdc.png
banner_img: /img/covers/responsible-ai-notes-ivdc.png
---

為了準備 IVDC（匯縱專業發展中心）「Certificate in Application of Computer Vision Technology」的考試，我把課程第四份本節《4 IVDC_Responsible AI.pptx》（24 頁）完整重寫成一份可離線閱讀的學習筆記，並額外做了一份 60 題的 MC 模擬試卷。

這一份和前三份（Introduction to AI、Local GPU、Computer Vision、OpenCV）性質不同：**它幾乎沒有程式碼，全部都是觀念、原則與法規**——但正因為如此，考題更容易出「配對題」與「數字題」，反而更需要精確記憶。

筆記已發佈成獨立專題頁面：

**👉 [Responsible AI 學習筆記（考試溫習版）](/responsible-ai-notes/)**

<!-- more -->

---

## 這份筆記包含什麼

依課程大綱每一個標題逐一填充，涵蓋全部 18 個主題：

| 章節 | 主題 |
|---|---|
| 1 | Responsible AI 是什麼（Challenges on AI） |
| 2 | Ethical AI Principles：**12 項倫理原則** |
| 3 | AI Practice Guide：專案生命週期**六個階段** |
| 4 | 電腦視覺的**四大倫理議題**總覽 |
| 5 | Privacy and Surveillance（隱私與監控） |
| 6 | Bias and Discrimination（偏見與歧視） |
| 7 | Data Security and Consent（資料安全與同意） |
| 8 | Accountability and Transparency（問責與透明） |
| 9 | 香港 **PDPO《個人資料（私隱）條例》** |
| 10 | **PDPO 六項保護原則**（DPP1–DPP6） |
| 11–16 | 社會影響五項（公共安全／醫療／就業／不平等／行為） |
| 17–18 | 六項倫理使用建議與結論 |

另外補了 7 個附錄：**名詞與法規速查表**、**常見錯誤與陷阱**、**本節頁面索引對照**、**離線使用與延伸資源**、**一頁精華（考前 10 分鐘）**、**60 題 MC 互動測驗**、**答錯題目 → 複習章節對照**。

---

## 重點：60 題 MC 模擬試卷

因為考試是選擇題形式，我特別做了一份**完整模擬試卷**（附錄 E，**互動網頁版**）：

**🖱️ [開始 60 題線上測驗](/responsible-ai-notes/mc-quiz.html)**

線上版功能：

- **點選答案**即自動計分，並即時顯示得分
- **作答進度自動存在你的瀏覽器**（localStorage）——關掉網頁、隔天再開都能繼續
- 可切換「只顯示未答」或「只顯示答錯」的題目，快速複習
- 按「顯示答案」才揭曉正解與解析，不會一開始就被暴雷
- 需要紙本時，直接在該頁按列印

**試卷設計**

- 60 題單選、滿分 60 分、建議 50 分鐘
- 分十二個區塊（每 5 題一組），依本節章節順序排列
- 答案分佈刻意打散（A/B/C/D 各 15 題），避免整排猜同一個字母
- 每題詳解都附「答錯題目 → 對應複習章節」對照，方便回頭補強

> 出題率最高的考點包括：**12 項**倫理原則與 **6 階段**專案生命週期、四大倫理議題的**英文原名與順序**、人臉辨識的 **without their consent**、偏見的根因 **not diverse or representative**、知情同意的 **informed consent**、自駕車責任的 **developer / manufacturer / user** 與 **black boxes**、**PDPO = Cap. 486、1996 年 12 月 20 日生效、PCPD**、六項原則的「**收、存、用、守、開、查**」、以及「**widening existing** inequalities」（是擴大既有的，不是創造新的）。

---

## 我補上了一個可執行的偏見量測範例

「偏見與歧視」那一頁本節只有兩段文字。我補了一個**本機實測**的 Python 範例，用混淆矩陣算出兩個族群的 FNR／FPR：

```
族群                樣本       FNR       FPR    Accuracy
A（多數族群）         2000     6.0%      4.0%      95.0%
B（少數族群）         2000    12.0%     10.0%      89.0%

機會均等差異 (Equal Opportunity Difference, FNR gap) = 6.0%
```

重點是：**整體準確率看起來 95% 很漂亮，但少數族群「該通過卻被擋下」的機率是多數族群的 2 倍**——這正好對應本節說的「資料集不夠多元或不具代表性」。只報整體準確率會完全掩蓋這個落差。

---

## 離線也能用

筆記是**單一 HTML 檔、零外部資源**（CSS 與語法高亮全部內嵌），下載後直接雙擊就能看，適合考前在沒有網路的環境複習。

也可以下載原始 Markdown：

**📄 [Responsible_AI_Study_Notes.md](/responsible-ai-notes/Responsible_AI_Study_Notes.md)**

---

## 建議使用順序

1. 先讀完第 1–18 節，把附錄 A（名詞與法規速查表）當工具書隨時查
2. **§10 PDPO 六項保護原則**與 **§9 的法規數字**（Cap. 486、1996 年 12 月、PCPD）優先背熟
3. 找個安靜的 50 分鐘，完整做一次**附錄 E 的 60 題線上互動測驗**
4. 考前 10 分鐘只看**附錄 D 一頁精華**

祝考試順利。

---

*本篇為個人學習筆記整理。*
