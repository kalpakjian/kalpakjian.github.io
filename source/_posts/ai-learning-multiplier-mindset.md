---
title: 用 AI 學新技術：拒用者、過度依賴者，還是放大者？——Gregor Ojstersek 的效率化學習法整理
date: 2026-11-01 22:30:00
categories:
  - AI Agent
tags:
  - Gregor Ojstersek
  - Engineering Leadership
  - The Multiplier Mindset
  - AI 學習
  - Codebase Onboarding
  - 跨語言學習
  - Angular
  - Spring Boot
  - Claude Code
  - Plan Mode
  - ADR
  - 事實查核
  - 判斷力
toc: true
index_img: /img/covers/ai-learning-multiplier-mindset.png
banner_img: /img/covers/ai-learning-multiplier-mindset.png
---

> <strong>整理說明</strong>：本篇整理自 Gregor Ojstersek 在 Engineering Leadership 電子報的〈[How to Use AI to Learn Faster](https://newsletter.eng-leadership.com/p/how-to-use-ai-to-learn-faster)〉（2026-10-12），該文是他由 O'Reilly 出版的新書 *The Multiplier Mindset* 其中一章的改寫版。**第一～五節為文章內容整理**；**第六節之後（我的看法、查核註記）是我自己的補充**，兩種內容分開標註。內容版權屬原作者所有，此為學習筆記用途。文中「微軟 PRAISE」一項在原始文章裡查無此詞，查核結果見文末。整理日期 2026-11-01。

## 一句話總結

> **把雜事交給 AI，判斷留給自己。** AI 能不能讓你變強，不看工具，而看你是拿它取代思考，還是拿它放大思考。

作者的核心主張可以拆成兩個動作：

1. **Delegate your busywork, not your judgment calls.**（把雜事外包，不要外包判斷）
2. **Approach new tools with curiosity, not unearned trust.**（對新工具保持好奇，但不要在它證明自己之前就完全相信）

---

## 一、三種工程師：你是哪一種？

作者把使用 AI 的工程師與工程主管分成三類。注意這不是「技術能力」分類，而是**使用方式**分類。

| 類型 | 特徵 | 典型心態／症狀 | 長期結果 |
|---|---|---|---|
| **拒用者**（Refusers） | 完全不用 AI，因為不信任 | 通常較資深：「這套我用了 15 年都很好，為什麼要改？」 | 心態上停止學習，反而被工具演進甩開 |
| **過度依賴者**（Overreliers） | 太依賴 AI，停止批判思考 | 通常較資淺，很熟工具，但產出「很普通」；更糟的是**連產出符不符合團隊標準都不檢查** | Reviewer 得幫他把問題一個一個找出來，比一開始就做對更花時間 |
| **放大者**（Multipliers） | 把 AI 當「放大能力」的工具，不是「取代專業」 | 用 AI 處理重複工作、加快學習、探索更多想法，把時間留給真正需要人判斷的問題 | 影響力最大 |

**為什麼「過度依賴者」比「拒用者」更危險？** 作者的說法很直白：過度依賴的成本會**外部化到 reviewer 身上**。拒用者頂多是自己慢；過度依賴者是把自己的思考成本轉嫁給團隊。

**目標不是「多用 AI」，而是站到第三類。** 判準只有一條：*你交付的東西，你講得出它為什麼長這樣嗎？*

---

## 二、場景一：幾個小時看懂一個新 codebase

作者引用工程師 **Jeff Morhous** 的四步驟（原為兩人合寫的付費客座文章〈How to Use AI to Onboard Into a Codebase Faster〉）。

前提：如果 repo 已有 `CLAUDE.md` 或 `AGENTS.md`，**先讀它們**——那是前人（或過去的 AI）已經整理好的專案心智模型，比重新推導便宜太多。

| # | 步驟 | 具體做法 | 關鍵要求 |
|---|---|---|---|
| 1 | **先看整體** | 沒有 `CLAUDE.md`／`AGENTS.md` 就對 Claude Code 跑 `/init`，請它整理專案最重要的部分 | 這步**用推理能力較強的模型**，多花 token 值得（後續所有步驟都建立在這份理解上） |
| 2 | **畫出架構** | 請 AI 整理主要元件、各自負責範圍、彼此相依關係（目錄職責、執行邊界、依賴圖） | 每一項主張都要**引用實際檔案路徑**，不接受沒有出處的架構描述 |
| 3 | **搞懂測試策略** | 測試放在哪、怎麼組織、最快的本地驗證指令、fixture／mock／test container 的做法、常見失敗模式 | 若專案沒有測試策略，就請 AI 提出一份測試金字塔方案當起點 |
| 4 | **把 App 跑起來** | 要求一條 repo 專屬的 setup 流程：runtime、依賴安裝、環境變數、DB／migration／seed、啟動指令 | 最後要**看到服務真的跑起來**，並用一條關鍵流程做 smoke test 確認正常 |

> **為什麼第 2 步要「引用檔案路徑」？** 因為架構描述是 LLM 最容易編造的地方。要求它標路徑，等於強迫它把答案綁在可驗證的事實上——這是最便宜的一種防幻覺機制。

---

## 三、場景二：從一種語言跨到另一種語言

作者的觀察：越來越多工程師不再綁定單一技術，前後端界線也越來越模糊。

**為什麼跨語言會變快？** 因為你已經有的不是「語法知識」，而是**工程基本功與設計模式**：分層、依賴注入、錯誤處理、測試、併發模型。這些在新語言裡大多**概念相同、語法不同**。AI 幫你補的是語法層，判斷力那一層還是你自己。

**書上的例子（Python 老手 → Java / Spring Boot）流程：**

1. **先自報背景**：告訴 AI「我熟 Python，熟悉 X、Y 概念，沒寫過 Java」。
2. **說明目標專案**：接下來要做一個 Spring Boot 專案，規模多大、要用哪些功能。
3. **在實際工作中問**：遇到看不懂的 code 就請 AI 解釋；寫完請 AI 檢查「哪裡可能寫錯、哪裡不符合這個生態的慣例」。

> **可以加的一步**：要 AI 用「你已經懂的語言」對照說明。例如「這段 Java 的 `@Transactional`，對應到我熟的 Python 是哪個概念？」把新知識釘在舊知識上，記得牢很多。

---

## 四、場景三：邊做邊學，不要一次叫 AI 做完

作者建議：學新框架時，**不要只看教學影片，直接做一個專案**。

以「很熟 React 的人想學 Angular」為例：

1. 用 AI coding 工具的 **Plan Mode** 先規劃專案。
2. **看懂它提出的架構**（而不是直接按下去讓它開工）。
3. 開始問問題，然後**一次只做一小塊**。

> 作者的重點：不要想讓 AI 一次寫完整個專案，然後祈禱它能跑。**既然目標是學習，就不要追求讓 AI 寫最多 code。**

**遇到不認識的寫法時，固定問三題：**

| 問題 | 你在練什麼 |
|---|---|
| 為什麼要這樣寫？ | 理解設計動機，而不是背誦語法 |
| 還有哪些替代做法？ | 建立取捨意識（trade-off），這是資深與資淺的分水嶺 |
| 這個寫法對應到我已經懂的哪個概念？ | 把新知識掛到既有的知識樹上 |

作者說得很清楚：重點是**理解為什麼這段 code 應該存在，以及它會怎麼影響整個系統**。

---

## 五、場景四：把 AI 當成思考夥伴

作者提出四種用法，共同點是：**AI 負責提問與壓力測試，你負責下決定**。

| 用法 | 具體做法 |
|---|---|
| **壓力測試設計** | 把技術規格或架構決策紀錄（ADR）丟給 AI，請它挑戰你的假設、提出替代方案、指出你漏掉什麼 |
| **預演困難對話** | 要跟主管或利害關係人談之前，先把想說的話寫成稿，請 AI 給回饋、修改，然後**大聲練習到自然為止** |
| **把問題講清楚** | 盡可能清楚描述問題再請 AI 提解法。**光是講清楚，你對問題的理解就已經變好**（這是最被低估的收益） |
| **改文章要自己動手** | 請 AI 給修改建議，但**手動套用**——這樣才能想清楚，也能保留自己的口吻 |

作者也引了康威定律（Conway's law）當背景：軟體系統的結構會反映組織的溝通結構。這也解釋了為什麼工程師要解的難題裡，有一大半同時牽涉技術與人——而「預演對話」這一項正是針對人的部分。

---

## 六、我的看法

### 1. AI 能不能幫你變強，看的是用法

同樣是用 AI 寫 Angular，一種人拿到能跑的 code 就收工；另一種人會追問「為什麼要這樣寫」。**三個月後，兩個人的差距會很大。** 差距不在打字速度，而在腦中多出來的那個模型。

### 2. 舊經驗不會消失，會變成你學新東西的基礎

熟 Python 的人學 Java 會比較快，**不是因為 AI，而是因為他已經懂基本功**。AI 幫你處理語法，但判斷 code 好不好，還是要靠你自己。反過來說：基本功越薄，AI 給的加速就越像幻覺。

### 3. 改文章要自己動手

直接按「全部套用」很省事，但文章就不像你寫的了。自己一句一句改，才知道哪些建議適合你、哪些不適合。**寫 code 也一樣：整段貼上能跑，但你不知道它為什麼能跑。**

### 4. 不想成為過度依賴者，最簡單的方法是「能講出 AI 做了什麼」

> AI 寫完之後，你講不出它為什麼這樣寫，就先不要 commit。

這條規則之所以有效，是因為它把抽象的「批判思考」變成一個**可以當場執行的檢查點**：講得出來 → 代表你有 review；講不出來 → 代表你只是轉貼。

### 5.（補充）這套方法其實是「驗證迴路」的學習版

把四個場景換個角度看，它們其實都在做同一件事：**替 AI 的輸出設計驗證迴路**。

| 場景 | 驗證迴路是什麼 |
|---|---|
| 快速看懂 codebase | 把服務真的跑起來 + 要求架構描述附檔案路徑 |
| 跨語言 | 語法錯誤由編譯器抓，慣例問題由你抓 |
| 邊做邊學 | 一次只做一小塊，每塊看懂才往下 |
| 思考夥伴 | 建議由你手動套用、自己大聲練習 |

沒有驗證迴路的 AI 使用，才會退化成人形複製貼上。**「放大者」和「過度依賴者」的差別，本質上就是有沒有驗證迴路。**

---

## 七、查核註記（原始貼文 vs 查證結果）

| 項目 | 查核結果 |
|---|---|
| 原文〈How to Use AI to Learn Faster〉 | **存在**。Engineering Leadership 電子報，2026-10-12 發布，免費閱讀，自述為新書改寫章節 [（原文）](https://newsletter.eng-leadership.com/p/how-to-use-ai-to-learn-faster) |
| 作者 Gregor Ojstersek | 正確，Engineering Leadership 電子報作者 |
| 新書《The Multiplier Mindset》／O'Reilly | **書名、作者、出版社皆正確**。電子書已上架，平裝版當時開放預購；原文自稱「upcoming book」，實際出版時程與貼文說法有些微時間差 [（作者公告）](https://newsletter.eng-leadership.com/p/announcing-my-book-the-multiplier) |
| Jeff Morhous 的四步驟 | **存在**，出自兩人合寫的付費客座文章〈How to Use AI to Onboard Into a Codebase Faster〉（2026-05-10）[（文章）](https://newsletter.eng-leadership.com/p/how-to-use-ai-to-onboard-into-a-codebase)。原文四步為：`/init` 取得全貌、畫架構地圖、找出測試策略、把程式跑起來——與本文第二節一致 |
| 「微軟 PRAISE」 | **查無此詞**。原始文章全文沒有出現「PRAISE」；arXiv 檢索 `"PRAISE" AND "code review"` 為 0 筆，Microsoft Research 站內搜尋亦無此框架。**請把這句視為未經證實的說法**；若引用自其他來源，建議先取得原連結再寫進文章 |

> 這一段的用意和上次查 IBM STAIR「幻覺少 65 倍」一樣：**轉述最容易被加油添醋的地方，通常是「引用了一個聽起來很權威的專有名詞」**。文章主體的四個場景經得起查，但最後那句「微軟 PRAISE」目前找不到出處。

---

## 八、一頁備忘（可直接貼在螢幕旁）

```text
1. 雜事外包，判斷不要外包。
2. 新 codebase：/init → 架構（附路徑）→ 測試策略 → 真的把它跑起來。
3. 跨語言：自報背景 → 說明專案 → 請 AI 用「我熟的語言」對照。
4. 學框架：Plan Mode 先規劃 → 看懂架構 → 一次只做一小塊。
5. 看到不懂的寫法，問三題：為什麼？還有別的做法嗎？對應到我懂的什麼？
6. 思考夥伴：壓力測試、預演對話、把問題講清楚、自己動手改。
7. Commit 前自問：我講得出這段 code 為什麼長這樣嗎？講不出來就先不要 commit。
```

---

## 參考資料

- Gregor Ojstersek,〈How to Use AI to Learn Faster〉, *Engineering Leadership*, 2026-10-12 — https://newsletter.eng-leadership.com/p/how-to-use-ai-to-learn-faster
- Gregor Ojstersek & Jeff Morhous,〈How to Use AI to Onboard Into a Codebase Faster〉（付費）, *Engineering Leadership*, 2026-05-10 — https://newsletter.eng-leadership.com/p/how-to-use-ai-to-onboard-into-a-codebase
- Gregor Ojstersek,〈"The Multiplier Mindset" E-Book Is Out, and Book Pre-Orders Are Open!〉 — https://newsletter.eng-leadership.com/p/announcing-my-book-the-multiplier
- Hexo 官方文件, Front-matter — https://hexo.io/docs/front-matter
