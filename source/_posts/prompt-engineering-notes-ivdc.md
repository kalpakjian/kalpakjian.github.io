---
title: Prompt Engineering 學習筆記：IVDC Lesson 5 完整複習 + 60 題 MC 模擬試卷
archive: true   # 已歸入「IVDC LLM 課程」學習筆記，不列在首頁
date: 2026-10-13 10:20:00
categories:
  - 學習資源
tags:
  - 人工智慧
  - LLM
  - Prompt Engineering
  - Chain-of-Thought
  - Tree-of-Thoughts
  - ReAct
  - RAG
  - IVDC
  - 學習筆記
  - 考試
index_img: /img/covers/prompt-engineering-notes-ivdc.png
banner_img: /img/covers/prompt-engineering-notes-ivdc.png
---

為了準備 IVDC（匯縱專業發展中心）「Certificate in Application of Large Language Model (LLM)」的考試，我把課程第五份課程《9 IVDC_Prompt_Engineering (adjusted).pdf》（**92 頁**）完整重寫成一份可離線閱讀的學習筆記，並額外做了一份 60 題的 MC 模擬試卷。

筆記已發佈成獨立頁面：

**👉 [Prompt Engineering 學習筆記（考試溫習版）](/prompt-engineering-notes/)**

<!-- more -->

---

## 這一份是「方法論大全」：92 頁、38 個章節、30 多種技術

Lesson 3 講的是「LLM 是什麼、怎麼運作」；Lesson 5 講的是「**怎麼跟它講話**」。
課程把數十種提示技術收斂成**七大類**，我把每一類底下的每一種技術都展開成一章，
每一章都保留`Classroom Exercise`（**同一題目、有／沒有用該技術**的成對示範），
並補上可以直接複製的 prompt 範本。

---

## 這份筆記包含什麼

| 章節 | 主題 |
|---|---|
| §1–§6 | 課程先修與目標、prompt 與 prompt engineering 的定義、第一個範例、**prompt 四大要素**、temperature 與 top_p |
| §7 | **六大任務**：摘要／問答／分類／角色扮演／程式生成／推理（各一組完整 prompt 範本） |
| §8 | **七大類技術地圖**（全份索引） |
| §9–§11 | 基礎技術：Zero-Shot／Few-Shot（In-Context Learning）／Clear Instructions |
| §12–§15 | 上下文與角色：System／Role／Contextual／Markdown Prompting |
| §16–§19 | 推理與規劃：CoT／Tabular CoT／Skeleton-of-Thought／Step-Back |
| §20–§23 | 進階編排：Least-to-Most／Tree-of-Thoughts／Interactive ToT／Self-Generated ICL |
| §24–§29 | 專業與前沿：Constitutional AI／Perspective-Taking／Analogical／Multi-Modal／Persona Consistency／Predictive |
| §30–§32 | 知識與工具：Generate Knowledge Prompting／PAL／ReAct |
| §33–§34 | 工具與應用：Tools & IDEs、LLM + 外部工具三元件、Data-Augmented Generation |
| §35–§38 | 安全與對齊：Model Safety、Prompt Injection／Leaking／Jailbreaking、RLHF |

另外補了 7 個附錄：**Prompt 元素與參數速查表**、**常見錯誤與陷阱**、**課程頁面索引對照**、
**離線執行／安裝提示**、**一頁精華（考前 10 分鐘）**、**60 題 MC 互動測驗**、**答錯題目 → 複習章節對照**。

---

## 重點：60 題 MC 模擬試卷

**🖱️ [開始 60 題線上測驗](/prompt-engineering-notes/mc-quiz.html)**

- 60 題單選、滿分 60 分、建議 75 分鐘
- 分四個部分、依課程章節順序排列
- 答案分佈刻意打散（A/B/C/D 各 15 題）
- 點選即時計分、進度存在 localStorage、可切換「只看未答／只看答錯」

> 出題率最高的考點包括：**prompt 是名詞／prompt engineering 是動詞**、
> **四大要素中哪一個在課程範例裡缺席（Context）**、
> **temperature／top_p：精確就調低、多樣就調高**、
> **few-shot 的別名是 In-Context Learning，且不改權重**、
> **「The sky is ___」在 zero-shot 答 Blue、在 few-shot 答 gas**、
> **Clear Instructions 的六要素（Task／Format／Length／Tone／Constraints／Context）**、
> **system 管規則、role 管身分**、
> **CoT 的三句觸發語**、**SoT 骨架 3–10 點**、
> **ToT 多了 search／backtracking、iToT 多了每輪回饋**、
> **PAL 把計算外包給 Python、ReAct 會呼叫外部工具**、
> **Generate Knowledge 取信心最高的預測**、
> **LLM + 外部工具的三個元件（Agent／Tool／LLM）**、
> **Prompt Injection／Leaking／Jailbreaking 三者的差別**，
> 以及**三大安全問題與 RLHF（Claude／ChatGPT）**。

---

## 最容易混淆的幾組技術

這份筆記花了整整一個附錄（B.2）在做「易混淆技術對照」——因為技術太多，考試最愛考「差在哪」：

| 常被混淆的一對 | 一句話記法 |
|---|---|
| CoT ↔ Least-to-Most | CoT 對**同一題**逐步推理；Least-to-Most **拆成多個子問題** |
| CoT ↔ SoT | CoT 是**一條鏈**；SoT 是**先骨架、後展開** |
| CoT ↔ PAL | PAL 把求解**外包給 Python 直譯器** |
| CoT ↔ ReAct | ReAct **會對外檢索與行動** |
| Step-Back ↔ Least-to-Most | Step-Back 往**上**抽原則；Least-to-Most 往**下**拆子問題 |
| Role ↔ Persona Consistency | Role 是**單次指派**；Persona 是**跨多次維持不變** |
| CAI ↔ RLHF | CAI 在**推論時**依規則約束；RLHF 在**訓練時**內化偏好 |

---

## 離線也能用

筆記是**單一 HTML 檔、零外部資源**（CSS、語法高亮、38 張章節插圖全部內嵌），下載後直接雙擊就能看，適合考前在沒有網路的環境複習。

也可以下載原始 Markdown：

**📄 [Prompt_Engineering_Study_Notes.md](/prompt-engineering-notes/Prompt_Engineering_Study_Notes.md)**

---

## 建議使用順序

1. 先讀完 §1–§8（定義、要素、參數、六大任務、七大類地圖），建立整體座標
2. 再依七大類順序讀 §9–§32，**每一章都動手把範本貼進任何一個聊天模型試一次**
3. 優先背熟：**§5 四大要素**、**§8 七大類**、**§11 六要素與弱／強對照**、**§16–§22 的推理技術差別**
4. 最後讀 §33–§38（應用與安全），並把**附錄 B.2 的對照表**抄一遍
5. 找個安靜的 75 分鐘，完整做一次**附錄 E 的 60 題線上互動測驗**
6. 考前 10 分鐘只看**附錄 D 一頁精華**

祝考試順利。

---

*本篇為個人學習筆記整理。*
