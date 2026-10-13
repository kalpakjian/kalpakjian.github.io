---
title: LiteLLM 學習筆記（IVDC Lesson 8）
date: 2026-10-13 11:40:00
tags:
  - LLM
  - LiteLLM
  - IVDC
  - 學習筆記
  - Python
categories:
  - AI
  - 學習筆記
cover: /img/covers/litellm-notes-ivdc.png
banner_img: /img/covers/litellm-notes-ivdc.png
index_img: /img/covers/litellm-notes-ivdc.png
archive: true
---

![LiteLLM 學習筆記](/img/covers/litellm-notes-ivdc.png)

IVDC「Certificate in Application of Large Language Model (LLM)」**Lesson 8 — LiteLLM** 的完整學習筆記。

LiteLLM 解決的問題很單純：**N 個供應商 × M 個應用 = N×M 套整合程式碼**。它把所有供應商收斂成**同一個 `completion()`**，輸入輸出都是 OpenAI 的 chat 格式。教材寫「50+ LLM APIs」，本機實測 litellm 1.91.2 已有 **146 個供應商**。

<!-- more -->

## 這份筆記有什麼

- **教材 18 格 notebook ＋ `lite.py` 逐格／逐行重寫**
- **所有程式碼都在本機實測**（litellm 1.91.2／openai 2.24.0／Python 3.11.15／Ollama `smollm`），實測輸出直接寫進內文
- 五大供應商呼叫逐一拆解：ChatGPT／Claude-2／llama2 on Replicate／Command-Nightly／Azure OpenAI
- **23 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **68 題互動 MC 測驗**（點選即時計分、進度自動存 localStorage）
- **課堂教材 `IVDC_LiteLLM.pptx`（11 頁）已整併**為 §21 ＋ 附錄 G：LLM Gateway 概念、虛擬金鑰／RBAC、多租戶成本治理、真實架構（Postgres／MCP），以及教材自己列出的限制

## 章節

| # | 章節 |
|---|------|
| 1 | 什麼是 LiteLLM：一個介面，146 個供應商 |
| 2 | 安裝與設定 |
| 3 | API Key 管理 |
| 4 | Call chatGPT — 最小可用範例 |
| 5 | Call Claude-2 — 第二個供應商，同一段程式 |
| 6 | Call llama2 on replicate — 開源模型走 Replicate |
| 7 | Call Command-Nightly — Cohere |
| 8 | Call Azure OpenAI — `azure/` 前綴與 deployment-id |
| 9 | 本機模型：Ollama（`lite.py` 逐行） |
| 10 | 模型命名規則與供應商前綴總表 |
| 11 | `completion()` 的統一 I/O 契約 |
| 12 | `messages` 的三種角色 |
| 13 | 常用參數速查 |
| 14 | 串流輸出 `stream=True` |
| 15 | 錯誤處理與例外類別 |
| 16 | 能力查詢：`supports_*` |
| 17 | Token 計數 `token_counter()` |
| 18 | 成本追蹤 `completion_cost()` 與內建成本表 |
| 19 | 進階：Router、Fallbacks 與重試 |
| 20 | LiteLLM Proxy |
| 21 | LiteLLM 作為 LLM Gateway：企業級治理與架構 |
| 22 | 本機實測總表（真實數據） |
| 23 | 考試重點整理 |

另有 **8 個附錄**：API 速查表、常見錯誤與陷阱、離線執行／安裝提示、一頁精華（考前 10 分鐘）、68 題 MC 互動測驗、答錯題目 → 複習章節對照、。

---

## 重點：60 題 MC 模擬試卷

**🖱️ [開始 68 題線上測驗](/litellm-notes/mc-quiz.html)**

- 68 題單選、滿分 68 分、建議 85 分鐘
- 分五個部分、依教材 notebook 格號順序排列（第 61–68 題是 §21 教材概念題組）
- 答案分佈刻意打散（A/B/C/D 各 17 題）
- 點選即時計分、進度存在 localStorage、可切換「只看未答／只看答錯」

> 出題率最高的考點包括：**`<供應商>/<模型>` 只認第一個斜線**、
> **本機模型一定要 `api_base`（Ollama 預設 11434）**、
> **Azure 的 `model=` 放的是部署名稱不是模型名**、
> **回應物件 `object` 恆為 `chat.completion`**、
> **串流時欄位從 `.message.content` 變 `.delta.content`**、
> **例外沿用 openai 階層**、
> **`completion_cost()` 對本機模型回 0.0**、
> **`supports_*()` 回 False 可能只是表裡查不到**，
> 以及**教材 `claude-2` 在 1.91.2 已必須加前綴**。

---

## ⚠️ 教材 vs 現行版本：三個落差

這份筆記最有價值的地方，是**把「教材當時正確、現在已失效」的寫法標出來**：

| 寫法 | litellm 1.91.2 實況 |
|---|---|
| `completion(model="claude-2", ...)` | ❌ `BadRequestError`，需改 `anthropic/claude-2` |
| 「50+ LLM APIs」 | 現為 **146** 個 provider |
| 用 `OpenAIObject` 描述回應 | 現為 LiteLLM 的 **`ModelResponse`** |

通則：**`<供應商>/<模型>` 永遠安全；省略前綴只在 LiteLLM 內建了推斷規則時才有效。**

> **補充（課堂教材）**：同一件事，教材寫的是「**100+** different LLM providers」。
> 所以三個數字並存——notebook 的 **50+**、教材的 **100+**、本機實測的 **146**。
> 它們分別代表三個時間點，考試出現任何一個都要認得。

---

## 本機實測的真實數字

| 項目 | 實測值 |
|---|---|
| `litellm.provider_list` | **146** 個供應商 |
| `litellm.model_cost` | **4069** 個模型 |
| 本機 `smollm` 非串流 | **14.59 s** |
| 本機 `smollm` 串流 | **8.09 s**（首塊 **3.38 s**） |
| `get_max_tokens("gpt-3.5-turbo")` | **4096** |
| `completion_cost()`（本機） | **0.0** |

---

## 離線也能用

筆記是**單一 HTML 檔、零外部資源**（CSS、語法高亮、23 張章節插圖全部內嵌），下載後直接雙擊就能看。

**LiteLLM + Ollama 是這課唯一能完全離線跑起來的組合** —— 不需要任何 API key。

也可以下載原始 Markdown：

**📄 [LiteLLM_Study_Notes.md](/litellm-notes/LiteLLM_Study_Notes.md)**

---

## 建議使用順序

1. 先讀 §1–§3（定位、安裝、金鑰），建立整體座標
2. 再依教材順序讀 §4–§8，**每個供應商範例都動手跑一次**
3. 讀 §9（`lite.py`），把 `api_base` 與 `temperature=0` 的意義弄懂
4. 優先背熟：**§10 命名規則**、**§11 I/O 契約**、**§14 串流**、**§15 例外**
5. 讀 §16–§20（能力、token、成本、Router、Proxy）
6. 讀 §21（LLM Gateway）—— 這節來自**課堂教材**，是 notebook 完全沒有的架構視角
7. 找個安靜的 85 分鐘，完整做一次**附錄 E 的 68 題線上互動測驗**
8. 考前 10 分鐘只看**附錄 D 一頁精華**

祝考試順利。

---

*本篇為個人學習筆記整理。*
