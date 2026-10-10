---
title: 從零打造一個 coding agent：六個零件、一個迴圈，與 Ralph 迴圈真正的位置
date: 2026-10-11 12:00:00
categories:
  - AI Agent
tags:
  - Coding Agent
  - Agent Loop
  - Ralph Loop
  - Context Engineering
  - Claude Code
  - Geoffrey Huntley
  - Tobi Lütke
  - 工具設計
  - 驗證迴路
  - 護欄
  - 本地 LLM
  - Cline
  - Pi
  - MCP
  - Ollama
  - TypeScript
  - 擴展性
  - 實測
  - 開源工具
  - Python
toc: true
index_img: /img/covers/building-a-coding-agent.png
banner_img: /img/covers/building-a-coding-agent.png
---

> <strong>整理說明</strong>：這篇原本是單篇長文，內容已經長到不適合當一篇文章讀。現在它已經升級成一份<strong>八章專題</strong>——每個章節有自己的插圖、自己的目錄，並可以獨立連結。本文保留為<strong>導讀與索引</strong>；完整內容請見 <a href="/coding-agent/"><strong>專題：從零打造一個 coding agent</strong></a>。

<!-- more -->

## 一句話總結

> 做一個 coding agent，難的從來不是模型，而是<strong>context 管理、工具權限、驗證迴路與失敗恢復</strong>。把這四件事做對，你就已經做出 Claude Code 的核心骨架——模型只是隨時可以換掉的零件。

換個說法：<strong>agent = 模型 + harness</strong>。模型提供智能，harness（外殼）負責把智能變成真實世界裡的工作。

但反過來也要說清楚：<strong>harness 完整，並不保證等於強 agent</strong>。像 Cline CLI 這樣功能齊全的開源 harness，能給你 agent 的骨架、工具、審批與自動化，卻不能給你判斷力——它的智能上限，等於<strong>你接的模型</strong>加上<strong>你設計的驗證迴路</strong>。

---

## 👉 完整內容：[專題：從零打造一個 coding agent](/coding-agent/)

> **八章導覽**：建議照順序讀——前三章把零件拆開並寫出骨架，中三章拿兩個開源 harness 當對照組並實測，最後兩章把它接回你的工作流。

| # | 章節 | 內容 |
|:---:|---|---|
| **01** | [一個 coding agent 只有六個零件](/coding-agent/ch01-six-parts.html) | 把那句爭論拆成合理與過頭兩半；六個零件與資料流 |
| **02** | [工具設計與 Context 管理](/coding-agent/ch02-tools-context.html) | 不要一開始就給 30 個工具；三個鐵則與 Ralph 的「乾淨 context」 |
| **03** | [護欄、驗證迴路與 90 行骨架](/coding-agent/ch03-guardrails-verify.html) | 沒有護欄就不要讓它自動跑；附完整可跑的 Python 骨架 |
| **04** | [Cline CLI：把六個零件做到生產級](/coding-agent/ch04-cline.html) | 逐格對照你的 90 行版本；harness 能力 ≠ 實際表現 |
| **05** | [Pi：把核心拆到最小](/coding-agent/ch05-pi.html) | 預設四個原子工具；極簡是雙面刃 |
| **06** | [一手實測：把 Pi 接上本地模型](/coding-agent/ch06-experiment.html) | 八次執行、三個模型、三種 thinking 等級、一組削 prompt 對照 |
| **07** | [里程碑、Ralph 迴圈與常見陷阱](/coding-agent/ch07-workflow.html) | M1～M6 的順序本身就是護欄；七個最常見的坑 |
| **08** | [一個比較健康的資深標準](/coding-agent/ch08-standard.html) | 五項具體能力與全篇參考來源 |

---

## 這份專題的核心論點

1. **agent = 模型 + harness**。模型提供智能，harness 負責把智能變成真實世界裡的工作。
2. 任何 coding agent 拆開都是**六個零件**：模型、工具、迴圈、Context 管理器、護欄、驗證器。前五個是內層 agent，第六個加上「規格檔 + 每輪單一任務」就是外層 Ralph 迴圈。
3. 第 6 個零件**不是選配**——「完成」的定義必須是可驗證的，而不是模型說「我做完了」。
4. **harness 完整 ≠ 強 agent**。Cline CLI 把六個零件做到生產級，Pi 把核心拆到只剩四個原子工具；兩者證明同一件事：**harness 可以下載，判斷力不行。**
5. 這些都可以被量測：同一個 harness、同一個任務，**8B 模型的輸出是 27B 的 12.3 倍**；而 prompt 快取狀態的影響（冷 29.5s／暖 10.1s）比模型參數還大。

---

## 為什麼要改成專題

原文有 13 節、兩張大對照表、一支 90 行的程式碼、八次實測的完整數據。當一篇文章同時要當「觀點評論」與「實作手冊」時，兩邊都會被犧牲：想快速看論點的人被表格淹沒，想照著做的人又找不到章節。

拆成專題之後：

- **每一章有自己的插圖**，先看圖就知道這章在講什麼
- **每一章有自己的目錄**，可以直接跳到想看的段落
- **章節之間有上一章／下一章**，可以當成一條學習路徑照順序走
- **延伸連結可以指到特定章節**，而不是「那篇長文裡的某一段」

如果你只有五分鐘，先讀 [第 1 章](/coding-agent/ch01-six-parts.html) 的六個零件表；如果你打算動手做，直接從 [第 3 章](/coding-agent/ch03-guardrails-verify.html) 的骨架開始抄。
