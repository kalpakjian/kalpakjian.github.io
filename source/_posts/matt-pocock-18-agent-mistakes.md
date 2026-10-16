---
title: 「Agent 時代，你可能累錯地方了」——Matt Pocock 的 18 條錯誤清單，與一份可量測的自我診斷表
date: 2026-10-16 21:30:00
categories:
  - AI Agent
tags:
  - Matt Pocock
  - Coding Agent
  - Agent Skills
  - Harness Engineering
  - Context Engineering
  - 驗證
  - 自動化檢查
  - 開發流程
  - 自我診斷
toc: true
index_img: /img/covers/matt-pocock-18-agent-mistakes.png
banner_img: /img/covers/matt-pocock-18-agent-mistakes.png
---

> <strong>整理說明</strong>：本文整理自 Matt Pocock 2026-10-13 在 X 發布的貼文「Some mistakes you might be making」[（原始貼文）](https://x.com/mattpocockuk/status/2109973273924579720)，共 18 條。貼文本身沒有分組、沒有編號，<strong>本文的分組與診斷表為我自己的整理</strong>；文中的事實查核引用他的 [skills repo](https://github.com/mattpocock/skills)、[AI Coding Dictionary](https://aicodingdictionary.com)、[Pragmatic Engineer 訪談](https://newsletter.pragmaticengineer.com/p/ai-skills-with-matt-pocock)（2026-09-17）與 v1.3 changelog（2026-10-05）。內容版權屬原作者所有，此為學習整理用途。

<!-- more -->

## 一句話總結

> 跟 coding agent 合作做不好，通常<strong>不是工具的問題，而是力氣放錯地方</strong>。該在前面做的對齊沒做，不該管的執行細節卻一直盯著。真正該投資的是讓 agent 能自己驗證、讓 context 保持乾淨、讓程式碼有一致的語言，然後把人的時間留給架構與策略。

Pocock 自己的說法是：<strong>agent 已經很會做戰術層的事，所以人應該把時間移到戰略層</strong>（他在訪談裡稱之為 strategic coding）。

這份清單最聰明的地方，是它刻意讓<strong>相反的錯誤成對出現</strong>：

- 「你開工前沒有先對齊」↔「你對齊太頻繁、太用力」
- 「自動化 review 做太少」↔「人工 review 做太多」
- 「你花的力氣太多」↔「你想得不夠多」

換句話說：**正確答案不在任何一端**。這不是「更勤勞一點」或「更放手一點」能解決的問題，而是要搞清楚哪些事該花力氣、哪些事該放掉。

---

## 為什麼這份清單值得看

Matt Pocock 是 Total TypeScript 的作者（累計銷售超過 250 萬美元）、現主推 AI Hero 課程，曾在 Vercel 工作。他這一年多專心研究「怎麼跟 coding agent 一起工作」，把每天在用的 agent skills 公開在 GitHub：

| 項目 | 數字（2026-10 查核） |
| --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills) | **293.4k** stars、24.6k forks、545 commits |
| repo 定位 | 「Skills for Real Engineers. Straight from my .agents directory.」 |
| 設計原則 | 刻意做得很**小**、容易改、可組合（"Hack around with them. Make them your own."） |
| 相關訪談 | Pragmatic Engineer《AI Skills with Matt Pocock》2026-09-17（1 小時 35 分） |

他在貼文底下補了兩件事：一是「如果你覺得自己犯了其中幾條，問我怎麼改，我會幫你」；二是附上 <strong>[The AI Coding Dictionary](https://aicodingdictionary.com)</strong>——一份把 AI coding 詞彙用白話定義的字典。**這份字典其實是讀懂清單的前提**，因為清單裡有幾個詞是專有名詞，不是日常用語（見下一節）。

---

## 18 條完整清單

以下為貼文原文順序（原文沒有編號，編號是我加的），英文為原文、中文為我的翻譯：

| # | 原文 | 中文 |
| --- | --- | --- |
| 1 | Your effort level is too high | 你的**推理 effort 檔次**開太高 |
| 2 | Your skills are too long | 你的 skill 太長 |
| 3 | You're not aligning before you start work | 開工前沒有先對齊 |
| 4 | You're aligning too often, and too hard | 對齊太頻繁、太用力 |
| 5 | Your automated checks are too lax | 自動化檢查太鬆 |
| 6 | Your custom tooling is too token-inefficient | 自訂工具太浪費 token |
| 7 | You aren't doing enough automated review | 自動化 review 做太少 |
| 8 | You aren't reviewing previous coding sessions (with an agent) | 沒有用 agent 回顧之前的 session |
| 9 | You're doing too much human review | 人工 review 做太多 |
| 10 | You aren't vibe coding enough prototypes | vibe coding 的 prototype 太少 |
| 11 | Your agent can't verify its own work | agent 無法驗證自己的工作 |
| 12 | You're babysitting the agent too much | 盯 agent 盯太緊 |
| 13 | You've overloaded your global steering files | 全域指示檔塞太多東西 |
| 14 | Your codebase is hard to navigate | codebase 很難找東西 |
| 15 | You aren't building a shared language | 沒有建立共同語言 |
| 16 | Your codebase architecture allows bad tests to be written | 程式架構讓爛測試有機會被寫出來 |
| 17 | You aren't thinking strategically enough | 策略想得不夠 |
| 18 | You aren't thinking enough | 想得不夠多 |

---

## 五組歸納

貼文本身沒有分組，以下五組是我的整理（18 條一條不漏、各歸一組）：

| 組 | 條號 | 一句話 |
| --- | --- | --- |
| 一、你太緊張了 | 1、9、10、12 | 還在用「人盯機器」的老方法 |
| 二、對齊要在對的時機做 | 3、4 | 開始前做重、執行中做輕 |
| 三、驗證才是真正的瓶頸 | 5、7、8、11、16 | 產出越快，驗證越容易卡住 |
| 四、context 是有限資源 | 2、6、13、14 | 當預算管，不是當保險買 |
| 五、人要想得更多，不是更少 | 15、17、18 | 省下的腦力往上一層用 |

### 一、你太緊張了（1、9、10、12）

agent 寫 code 很快。如果每一行都要你親自看過，**你就是整條生產線最慢的那個環節**。該快速試錯的時候，就讓它隨便做幾個 prototype 看看，不用那麼謹慎。

其中第 1 條要小心讀——它講的不是「你太用力」，而是模型的推理預算（見下一節）。

### 二、對齊要在對的時機做（3、4）

「開工前沒有先對齊」會讓 agent 做完一大堆才發現方向錯了；但「對齊太頻繁」又會變成另一種微觀管理，每一步都要確認，agent 根本沒有空間發揮。

Pocock 的意思是：**對齊要在開始前做重一點，執行中做輕一點。** 這其實就是敏捷講的事：規格前置，執行期給團隊自主權。他 repo 裡對應的工具鏈是 `grilling`（agent 一問一答，把決策樹的每個分支問完）→ `to-spec` → `to-tickets`。

### 三、驗證才是真正的瓶頸（5、7、8、11、16）

這是整份清單的重心，五條都在講同一件事：**agent 產出越快，驗證就越容易變成卡住的地方。**

- 如果 agent 沒辦法自己確認做對了沒（11）、測試可以隨便亂寫（16）、檢查又很鬆（5），那不管你請多少人來 review（7）都補不完。
- 第 16 條特別狠：它不是說「測試寫得不好」，而是說**程式架構本身就允許爛測試存在**——把測試品質的問題往上推到設計層去解決。
- 第 8 條把 retrospective 也交給 agent。他 10 月初發布的 v1.3 就加了 `/retro`，作為主流程的最後一步（在 `/code-review` 之後）。

所以人的角色要從「檢查產出」退一步，變成「**設計檢查機制**」。

### 四、context 是有限資源，要當預算管（2、6、13、14）

這四條講的是同一個觀念：**agent 的注意力是有限的。**

很多人以為指示寫越多越安全，結果 `CLAUDE.md` / `AGENTS.md` 越來越肥，agent 反而抓不到重點。他的 skills 之所以刻意做得很小、鼓勵大家自己改（"Hack around with them. Make them your own."），就是這個想法的實踐。第 6 條則是同一個預算觀念用在自訂工具上：工具回傳一大堆 agent 不需要的內容，就是在燒 context。

### 五、人要想得更多，不是更少（15、17、18）

這三條在反駁一種常見誤解：用 agent 就不用動腦了。**恰好相反**——agent 把戰術工作接走之後，人應該把省下來的腦力拿去想更高層次的事情。

「共同語言」指的是**人、agent、程式碼三方要用一致的詞彙**：命名、概念、慣例都要對得上，agent 才不會每次都要重新猜你在講什麼。這也是他為什麼要另外做一份 AI Coding Dictionary。

---

## 三個容易讀錯的地方

把這 18 條轉述成中文時，有三個地方最容易失真，以下是我查核後的版本。

### 1. `effort` 不是「你的力氣」，是「模型的推理預算」

AI Coding Dictionary 對 **Effort** 的定義是：

> A dial for how much reasoning the model does before it answers. More effort spends more output tokens for a better shot at hard problems.

也就是 harness 端（Claude Code 這類工具）的推理檔次設定。所以第 1 條**不是心態問題，是成本與延遲問題**：不是所有任務都值得開最高檔。把它讀成「你太用力了」會讓人去反省態度，但該做的其實是按任務分級。

### 2. `/retro` 是 human-in-the-loop，Pocock 明確反對自動化

v1.3 說明頁裡的原話大意是：多數人問他怎麼把 retro 自動化，**「不要做」**——自動化的 retro 會找到假陽性、一直去修它，然後把你的 repo 帶到不該去的地方。建議的用法是**抽樣幾個 session 跑**，或跑在「agent 做了怪事」的那一場。

而且它改的是**環境而不是程式碼**：機械性的違規會被轉成一條確定性檢查（lint rule、pre-commit hook 或 CI job），`CODING_STANDARDS.md` 只留真正的判斷題。Pocock 對這件事的判準說得很直白：

> A check can fail. A sentence in a Markdown file cannot.（檢查會紅燈，Markdown 裡的一句話不會。）

結果是：**`AGENTS.md` 應該越用越短，不是越用越長。**

### 3. 這不是「18 條都要修」的清單

它是一份**自我診斷表**。如果照 Pocock 自己的優先序排，順序大致是：驗證 → context → 對齊 → 人的節奏 → 戰略。一次修一條，而且修在環境上，不要修在散文上。

---

## 兩端都是錯的：這份清單的設計

貼文發出後，底下有一則回覆被大量轉推（1.1k 讚）來自 @Everlier：

> You are doing too much. You are doing too little. You are doing just enough, but in a wrong way.

**第三句才是重點**，也是 Pocock 那份清單真正在講的事：力氣放錯地方，比用多用少更致命。

---

## 自我診斷表：把 18 條改成「可以量」的問句

清單要能當工具用，關鍵是把每一條改寫成**觀察得到數字**的問句：

| # | 診斷問句 | 該看什麼 |
| --- | --- | --- |
| 1 | 這個任務值得開最高推理檔嗎？ | output token 花費與延遲 vs 任務難度 |
| 2 | 我的 skill／指示檔多長？ | 單檔 token 數（粗估：字元數 ÷ 4） |
| 3 | 開工前有沒有 spec 與 tickets？ | 有沒有「完成」的定義 |
| 4 | 執行中我插手幾次？ | 單一 ticket 內的人工介入次數 |
| 5 | 檢查是確定性的，還是靠人看？ | 有沒有 lint rule／hook／CI job 擋住 |
| 6 | 自訂工具回傳多少沒用的內容？ | 工具輸出佔掉的 context 比例 |
| 7 | 有沒有 agent 審 agent？ | 有沒有 review subagent（standards／spec 分軸） |
| 8 | 上次踩的坑有沒有變成護欄？ | `AGENTS.md` 是變短還是變長 |
| 9 | 我讀的是 diff 還是 summary？ | **讀 summary 不算 review**（字典的定義） |
| 10 | 設計問題有沒有先用 prototype 收斂？ | 有沒有產出可丟棄的成品來討論 |
| 11 | agent 能自己證明做對了嗎？ | 有沒有能在 30 秒內跑紅／跑綠的迴路 |
| 12 | 這個 session 是 AFK 還是 HITL？ | 時間花在盯每一步，還是花在收尾 |
| 13 | 全域指示檔多肥？ | `AGENTS.md`／`CLAUDE.md` 的 token 數 |
| 14 | agent 找得到東西嗎？ | 幾次工具呼叫才找到正確的檔案 |
| 15 | 三方用的是同一套詞嗎？ | 有沒有 `GLOSSARY.md` |
| 16 | 架構允許爛測試存在嗎？ | 有沒有約定的 seam、能否寫出同義反覆的測試 |
| 17 | 我的時間花在哪一層？ | 寫／審程式碼 vs 架構與規格 |
| 18 | 開工前有沒有真的被追問過？ | 決策樹的分支解完了沒 |

---

## 拿我自己的站實測：這份清單長什麼樣

清單最容易變成「讀完覺得有道理」然後就沒有然後。所以我把它套在自己的 Hexo 筆記站上（站上有一套自製的品質閘門：11 項硬性檢查 + 2 項警告）：

| 條 | 我這邊的實測結果 |
| --- | --- |
| 5 自動化檢查太鬆 | 閘門存在，但 `notes-qa.yml` 設了 `continue-on-error: true`——**檢查沒有牙齒** |
| 7 自動化 review 太少 | 沒有 agent 審 agent，也沒有 standards／spec 分軸 |
| 8 沒有回顧 session | 有寫作契約，但沒有 retro 這一步 |
| 13 全域指示檔太肥 | 我**沒量過**——這本身就是答案 |
| 15 沒有共同語言 | 同一個東西有兩個名字：互動測驗在 14 份筆記是「附錄 E」、在 2 份是「附錄 F」；貼文 slug 有的有 `-ivdc` 後綴、有的沒有 |
| 16 架構讓爛測試有機會 | 檢查是文字比對，無法保證 Markdown 與 HTML 的**語意**一致 |

實測結果（2026-10-16 執行閘門）：

- 16 份筆記中 **1 份 FAIL**：禁詞「原稿」在 HTML 出現 67 次、Markdown 37 次，頁碼引用 16 次
- 因為 CI 設了 `continue-on-error`，**這個 FAIL 從來沒有擋下任何一次部署**
- 而這套閘門有 11 項硬性檢查——所以問題從來不是「檢查不夠多」，而是**檢查沒有連到決策**

這正是 Pocock 第 5 條與第 7 條的具體長相：**產出很快，驗證存在，但驗證不痛。** 於是我把這份清單落地成兩份檔案——一份自我診斷表（`AGENT-HEALTH.md`）、一份這個站的共用詞彙表（`GLOSSARY.md`，已放進 repo），讓它變成之後每次工作都能引用的資產，而不是一篇讀完就忘的文章。

---

## 評論與可商榷之處

1. **它告訴你兩端都是錯的，卻沒說中間在哪。** 這部分他留給自己的課程，所以清單本身不能當處方，只能當體檢表。
2. **「多做 prototype」與「檢查不要太鬆」之間有張力。** prototype 階段本來就不該有嚴格檢查；他沒有把兩種模式的邊界畫出來。（字典裡 *Vibe coding* 與 *Prototyping* 是兩種不同的工作模式，不是同一條軸的兩端——這是讀懂第 5 條與第 10 條並存的關鍵。）
3. **「用 agent 回顧 session」很吃 context 管理能力。** 而且他自己就說不要自動化、只能抽樣跑，等於承認它的規模化有上限；小團隊不一定做得起來。
4. **這類清單有倖存者偏差。** 18 條是從**一個人的**工作流歸納出來的。他的 repo 有 293k stars，不代表同一套流程在別的語言、別的遺留系統、別的團隊規模上同樣成立。
5. **轉述時數字最容易失真。** 我看到的二手整理寫「超過 26 萬顆星」，實際查核是 **293.4k**。這種數字一錯，讀者對整份整理的信任就會打折——這本身也是第 5 條的示範。

---

## 一句話帶走

> **agent 時代的瓶頸，從「寫」移到了「驗」。** 所以該投資的不是更多 review，而是讓 agent 自己驗證得了；該清理的不是 agent 的產出，而是它的 context 與你的指示檔。

---

## 延伸連結

- 🐦 原始貼文（18 條）：[Matt Pocock on X](https://x.com/mattpocockuk/status/2109973273924579720)
- 📦 每日在用的 skills repo：[mattpocock/skills](https://github.com/mattpocock/skills)
- 📖 詞彙定義：[The AI Coding Dictionary](https://aicodingdictionary.com)
- 🎙️ 訪談：[AI Skills with Matt Pocock — The Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/ai-skills-with-matt-pocock)（2026-09-17）
- 📝 v1.3 說明（`/retro`、`/pr`、`/implement-spec`、`GLOSSARY.md`）：[AI Hero](https://www.aihero.dev/skills-changelog-v13-implement-spec-pr-retro-and-glossary-md)（2026-10-05）

---

> **版權聲明**：本文為學習整理。18 條清單的內容與文字版權屬 Matt Pocock 所有；五組歸納、診斷表、事實查核與自家站台的實測段落為我自己的整理。如有錯誤或遺漏，歡迎來信指正。

---

