---
title: 剖開 11 個主流 coding agent 的原始碼——83 頁論文揭示的 7 個子系統、兩個缺席與 18 條設計建議
date: 2026-10-09 08:00:00
categories:
  - AI Agent
tags:
  - Coding Agent
  - Harness Engineering
  - Claude Code
  - Codex
  - Gemini CLI
  - OpenHands
  - Aider
  - LangChain
  - RAG
  - 論文導讀
  - 架構
toc: true
index_img: https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200
banner_img: https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1600
---

> <strong>整理說明</strong>：本篇整理自 [工程師米奇](https://www.facebook.com/share/p/19Qk38HJkr/) 分享的論文導讀，並對照原始論文補充細節。論文為 Paul Barbaste、Tristan Darrigol、Germain Vu、Tom Wiltberger（Wavestone AI Lab）《Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents — A Source-Code Study of Eleven Systems》，arXiv:2609.00006，2026 年 7 月 15 日提交，正文 83 頁，以 CC BY 4.0 發布。內容版權屬原作者所有，此為學習整理用途。

<!-- more -->

## 一句話總結

> 把 11 個生產級 coding agent 的約 **400 萬行** Python / TypeScript / Rust 原始碼全部讀完之後，作者發現兩件違反直覺的事：<strong>沒有一個</strong>使用 LangChain 這類 agent 框架，也<strong>沒有一個</strong>用向量檢索來找程式碼。整個領域跑在「手寫的 async 迴圈 + 確定性檢索」之上。

論文的中心論點可以濃縮成一句話：**所有 coding agent，從 100 行的研究原型到 112 萬行的產品，都必須在同樣 7 個子系統上做選擇——哪怕那個選擇是「不做」。**

---

## 論文基本資料

| 項目 | 內容 |
| --- | --- |
| 標題 | Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents — A Source-Code Study of Eleven Systems |
| 作者 | Paul Barbaste、Tristan Darrigol、Germain Vu、Tom Wiltberger（Wavestone AI Lab） |
| 編號 | arXiv:2609.00006（cs.SE） |
| 版本 | 2026 年 7 月 15 日提交；為 4 月版本的擴充版（8 → 11 個系統） |
| 篇幅 | 83 頁、7 張圖、18 張表 |
| 語料 | 約 400 萬行原始碼，Python / TypeScript / Rust |
| 授權 | CC BY 4.0 |

論文的產出包含：**7 個標準子系統**的分類法、**29 個**反覆出現的設計模式、**13 條**橫切觀察，以及**18 條**設計建議與一份 90 行的最小可行 harness 範本。

作者特別強調：這篇論文**不做 benchmark、不排名**，它描述並比較這些系統是怎麼被蓋出來的。

---

## 什麼是 harness？

論文的開場定義非常精確：

> **agent = 模型 + harness。** 模型提供智能；harness 負責把智能變成實際的工作——也就是把 LLM 耦合到世界的<strong>那個執行期</strong>。

「harness engineering」這個說法在 **2026 年初**才被命名為一門學科，論文的目標就是給這門年輕學科一份有原始碼依據的參考。

值得注意的是定義裡**沒有「框架」**這個詞。論文的 2.2 節「What a Harness Is Not」刻意把第三方編排函式庫排除在外——這也預告了後面的第一個「缺席」。

### 七個標準子系統

11 個系統無論大小，都實作了同樣 7 個子系統，只是每個子系統的規模天差地遠：

| # | 子系統 | 最小實作（Mini-SWE-Agent） | 最大實作（Codex CLI） |
| --- | --- | --- | --- |
| 1 | **Agent Loop**（代理迴圈） | 線性 `while` 迴圈 | Tokio 非同步狀態機 |
| 2 | **LLM Integration**（模型整合與提示工程） | 單次 LiteLLM 呼叫 | 伺服器下發的「每模型一組」提示資料 |
| 3 | **Tools & Actions**（工具與行動） | 只有一個 `bash` | 25–30 個工具；工具呼叫以 **V8 解譯執行** |
| 4 | **Memory & Context**（記憶與上下文） | 無上限線性歷史 | Agent 自行維護的跨 session 記憶 |
| 5 | **Safety & Permissions**（安全與權限） | 只限制呼叫次數與花費 | 策略規則 + 審批模型 + 覆蓋 3 個 OS 的原生沙箱 |
| 6 | **Orchestration**（多代理編排） | 刻意不做子代理 | 子代理可再派生子代理 |
| 7 | **Extensibility**（擴充面） | 無 | skills / hooks / MCP / 插件生態 |

七個子系統之外，還有兩個**貫穿各子系統的面**：

- **介面層**：人和程式驅動 harness 的介面——終端 UI、IDE 協議（ACP）、HTTP 服務、SDK
- **會話存儲**：對話記錄、持久化、恢復與分叉（fork）

---

## 11 個系統總覽

| 系統 | 語言 | 規模 | 模型供應商 | 工具數 | 沙箱 | 介面 | 一句話特色 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OpenHands | Python | Medium | Multi | 25+ | Docker / Apptainer / remote | Web + CLI + SDK | 資源鎖定的平行工具；可把對手 harness 當 ACP 後端 |
| Aider | Python | Small | Multi | 13 種編輯格式 | 無 | CLI | 語料庫中唯一的「有排序的 repo map」 |
| Claude Code | TypeScript | Large | Anthropic | **43** | 選用式 runtime + worktree | CLI | 延遲載入工具；prompt cache 共享的 fork；別人模仿的標竿 |
| Codex CLI | Rust | Very large | OpenAI | 25–30 | **原生（3 OS）** | CLI / TUI | Agent 維護的跨 session 記憶；工具呼叫以 V8 執行 |
| Gemini CLI | TypeScript | Very large | Google | 35+ | **原生（3 OS）** | CLI / TUI | 模型路由當成 runtime 排程；唯一的 A2A server |
| Mistral Vibe | Python | Small | Mistral+ | 12+ | Worktree 選用 | CLI / TUI | 中介軟體管線式迴圈；rewind 透過 ACP 開放 |
| Mini-SWE-Agent | Python | Tiny | Multi | **1** | Docker+ | CLI | 100 行地板：七個子系統全部最低限度實作 |
| Hermes | Python | Very large | Multi（自有傳輸） | **69** | 6 個可插拔後端 | CLI / TUI / Web + 28 channel | 自我改進的 skill 迴圈；lineage compaction；停止時驗證 |
| Pi | TypeScript | Medium | Multi（35 個 provider） | 7 | 刻意無 | CLI / TUI | 一切都是擴充的核心；session-tree 版本控制 |
| OpenCode | TypeScript | Large | Multi | 17 | 無（改用策略） | Client / Server | 客戶端／伺服器架構；語法感知的指令權限 |
| OpenClaw | TypeScript | Large | Multi | **109+** | 無 | 多 channel | Gateway 委派；每次回覆前先跑 Active-Memory 子代理 |

> **規模定義**：Tiny ≈ 5K 行、Small ≈ 20–40K、Medium ≈ 80–110K、Large ≈ 500K+、Very large ≈ 600K+（Codex 7 月快照約 **1.1M 行 Rust**）。這些數字跨語言與計算慣例不可直接比較，僅用來定位系統在「簡潔 vs 能力」軸上的位置。

---

## 規模差三個數量級，任務完成率卻差不多

這是論文的 **Observation 1**，也是整篇論文最核心的實證：

> 11 個系統在程式碼規模上跨越了**三個數量級**，卻面對相似的任務；而**迴圈的複雜度並不預測 benchmark 表現**。

Mini-SWE-Agent 的極簡線性迴圈，自報成績與 OpenHands 的事件溯源會話引擎落在**同一區間**——儘管後者在迴圈編排上就多寫了好幾個數量級的程式碼。

論文 4 月版列過各家自報的 SWE-bench Verified 成績：

| 系統 | 自報 SWE-bench Verified |
| --- | --- |
| OpenHands | 77.6% |
| Mini-SWE-Agent | 74%+ |
| Claude Code | 72.7% |
| Codex | 69.1% |

7 月版作者把這一列**刪掉了**，理由是這些數字都是自報、用的模型與配置不同、有些還早於現行預設。但結論不變：**「做到能完成任務」的門檻很低。**

### 那大系統的程式碼都花到哪裡去了？

論文的回答：**安全、使用者體驗、擴充能力，以及越來越多的客戶端與傳輸層。**

- OpenCode 去掉測試程式後，約 **五分之三**的程式碼是 TUI、網頁、桌面與 SDK 客戶端，而不是 harness 本身
- Codex 7 月的程式碼裡，有**上十萬行**用在 app-server 傳輸、插件與即時語音層——這些**永遠不會體現在任何 benchmark 上**

換句話說，生產系統的質量，大多花在與「任務完成」正交的事情上。

---

## 兩個缺席（The Two Absences）

這是論文最受關注的發現，作者稱之為「**兩個缺席**」。

### 缺席一：沒有 agent 框架

作者檢查了每個專案的依賴清單，又在原始碼裡搜尋 LangChain、LangGraph、LlamaIndex、AutoGen、CrewAI、Pydantic AI、Genkit、Semantic Kernel、Google ADK 等框架的引用。

結果：在約 400 萬行程式碼裡，**沒有一條 agent 執行路徑用到它們**。連 Gemini CLI 都沒用 Google 自家的 Genkit 與 ADK。

作者在腳註裡寫，他們原本以為至少開源專案會有人用 LangChain；為了找反例查了好幾個星期，包含打包進去的依賴、動態 import 與編譯後的 TypeScript，最後才接受這個結果。

替代方案是各自語言原生的非同步機制**手寫迴圈**：

| 語言 | 機制 |
| --- | --- |
| Python | `asyncio`（`create_task` 等） |
| TypeScript | Promise 與非同步迭代器 |
| Rust | **Tokio** |

工具註冊表都是自己圍繞 **Pydantic / Zod** 這類校驗庫寫的；prompt 模板就是普通的 Markdown、Jinja2 或字串拼接。

### 缺席二：沒有用向量檢索找程式碼

作者搜尋了 Chroma、Pinecone、FAISS、sqlite-vec 等向量庫，以及檔名帶 `embedding`、`rag`、`retrieval` 的檔案與目錄。

結果：**11 個系統裡，0 個**用 embedding 檢索程式碼。

| 系統 | 怎麼找程式碼 |
| --- | --- |
| Claude Code | `ripgrep` 關鍵字搜尋、bash、按需讀檔，自動發現 `CLAUDE.md` |
| Codex | Rust 手寫檔案搜尋；從專案根目錄到當前目錄逐級拼接 `AGENTS.md` |
| Gemini CLI | 內建 `ripgrep` 與 `glob`，自動發現 `GEMINI.md` |
| Aider | 用 **tree-sitter** 提取符號，按 token 預算排序生成 repo map |
| Pi | 自動下載 `ripgrep` 與 `fd` |

Embedding **只出現在對話記憶裡**，不出現在「讀程式碼」這件事上：

- OpenClaw 預設的記憶插件用 `sqlite-vec` 做混合檢索
- Hermes 刻意用 SQLite 全文檢索搜歷史 session，embedding 只在可選插件裡

作者給的解釋：程式碼本身有大量**確定性的結構**——路徑、語言伺服器、語法樹——語義相似度替代不了；而且程式碼每分鐘都在變，embedding 很快就過時。

> ⚠️ 一個常見的誤傳：那條熱門推文說「檢索程式碼都不用 embedding，而是用 ripgrep 和 tree-sitter」，**後半句不太準確**。按論文的表格，大多數系統用的是 ripgrep 一類的關鍵字搜尋，tree-sitter 只在 Aider 的 repo map 等少數地方出現。

---

## 90 天縱向對照：從「趨同」到「模仿」

11 個系統裡有 8 個在 4 月版已分析過。作者**沒有換掉**它們，而是在 7 月重新取了一次原始碼——因此論文裡有一組難得的**受控縱向樣本**：同一批 harness、相隔一季的原始碼差異。

作者總結了四個變化：

### 一、趨同變成了模仿

4 月時各家的相似大多是各自獨立想到的；到 7 月已經能在程式碼裡找到來源：

- **Codex** 原樣採用了 **Claude Code 的 hook 事件名**，以及它的 plan 模式互動；還附了一個 session 與設定的 importer
- **OpenHands** 採用了 Claude Code 的插件清單格式與 `task` 工具的簽名
- **OpenCode** 會直接讀取 `~/.claude/skills` 目錄
- **Hermes** 的原始碼註解裡寫明了哪些設計分別借鑑自 OpenCode、Codex、OpenClaw 與 Goose

### 二、好的設計擴散得很快

| 設計 | 4 月 | 7 月 |
| --- | --- | --- |
| 工具按需載入 | 1 個系統 | **3 個系統** |
| 唯讀 plan 模式 | 2 個系統 | **全部 4 個**廠商產品 |
| 用模型判斷是否放行的審批機制 | Claude Code 1 家 | Claude Code + **Codex 的 Guardian** |

作者的說法是：**在這個領域，一個競爭優勢的半衰期是以「週」計算的。**

### 三、行為規則從 prompt 搬到設定檔

- Codex 新版的模型 prompt 刪掉了「不要提交」「不要過度設計」這類規則，改用**功能開關**控制
- Mistral Vibe 刪掉了「絕不提交」這條硬規則

趨勢很清楚：隨著模型自己學會了這些規範，harness 的治理能力也變強了——**規則正從「模型讀的 prompt」轉移到「平台強制執行的設定」。**

### 四、程式碼量像平台一樣成長

| 系統 | 變化 |
| --- | --- |
| Codex | 一季從約 **62 萬行 → 約 112 萬行** Rust |
| Mistral Vibe | 成長 **77%** |
| Aider | 90 天內僅 **18 個提交**，已進入社區維護狀態 |

### 順帶一提：skill 的採用率超過了 MCP

11 個系統裡 **9 個支援 skill**，**8 個支援 MCP**。打破平局的是 **Pi**——它實作了 skill 標準，同時**明確拒絕 MCP**。


---

## 18 條設計建議中最反直覺的幾條

論文第 16 節把前面的觀察整理成 18 條設計建議，每條都註明依據與已經這麼做的系統。以下是最反直覺的幾條：

| 建議 | 依據 |
| --- | --- |
| **從一個線性 `while` 迴圈開始**，只有同時出現三個以上獨立的輪次策略時，才改成中介軟體管線 | Mini-SWE-Agent 50 行的迴圈自報 74%+ |
| **一開始只給一個 `bash` 工具**，遇到具體問題再加 | 輸出被截斷 → 加讀寫檔；`find` 不好用 → 加 `grep`；整檔重寫太費 token → 加局部替換 |
| **工具超過約 15 個時才做按需載入** | Claude Code 的按需載入讓初始 prompt 減少約 **40%** |
| **不要按行號編輯檔案，要按上下文精確比對** | 模型在行號上的偏差比在上下文比對上更大 |
| **不要給程式碼做向量檢索** | 11 個系統裡 0 個這麼做；真覺得需要，先在測試集上證明它比 `ripgrep` + `tree-sitter` 強 |
| **不要用 LangChain、AutoGen、CrewAI 這類框架做 agent runtime** | 11 個系統裡 0 個這麼做；想要現成起點，用 Claude Agent SDK 這類 **harness SDK** |
| **確認任務裡有能平行探索的階段之前，保持單 agent** | Anthropic 的資料：多 agent 系統的 token 消耗約是普通對話的 **15 倍** |
| **如果支援跳過所有確認的 YOLO 模式，下面要留一層底線** | Hermes 有 12 條硬性規則在 YOLO 模式下依然生效 |
| **不要過度設計卡死偵測，但簡單的上限要有** | Claude Code 和 Codex 都沒有自動卡死偵測；「連續三次相同呼叫就問使用者」十幾行就夠 |

論文最後附了一個約 **90 行的 Python 骨架**，把線性迴圈、中介軟體式策略、四個工具（`bash`、讀、寫、局部替換）、逐級發現 Markdown 上下文檔、以及到閾值自動壓縮放在一起。

作者特別強調：**它不是能直接用的函式庫，而是一個用來複製和改造的起點。**

以下是最小可行 harness 的核心骨架（論點示意，精簡自論文附錄）：

```python
import asyncio

SYSTEM = "You are a coding assistant. Use tools to complete tasks."

async def run_loop(model_fn, tools: dict,
                   max_turns: int = 40, max_cost: float = 5.0):
    """Agent Loop + 其餘六個子系統的最小實作，全在這 40 行裡。"""
    history, turns, cost = [], 0, 0.0

    while turns < max_turns and cost < max_cost:      # Safety: 兩個上限
        response = await model_fn(SYSTEM, history)    # LLM Integration
        history.append({"role": "assistant", **response})

        if response.get("stop_reason") == "end_turn":  # Loop 停止條件
            break

        for call in response.get("tool_calls", []):
            if call["name"] not in tools:              # Safety: 拒絕未知工具
                result = {"error": "unknown tool"}
            else:                                      # Tools & Actions
                result = await tools[call["name"]](**call["args"])
            history.append({"role": "tool",
                            "name": call["name"],
                            "content": result})       # Memory: 線性歷史

        turns += 1
        cost += response.get("usage", {}).get("cost_usd", 0)

    return history
```

生產級的 harness 會在這個骨架上加上：安全深度、context window 管理、編排、擴充面。但**這個骨架本身從不消失**——它是論文分析的全部 11 個系統不變的中心。

這些建議中有一部分與 Anthropic 2024 年 12 月到 2025 年 9 月發表的幾篇 agent 工程文章一致，作者專門列了出來，並坦言分不清這是「大家面對同樣的現實」，還是「大家都讀了這些文章」。

---

## 讀這篇論文要注意的地方

1. **Claude Code 的分析依據一份 3 月流出的原始碼快照。** 作者在表格註解裡寫明了這是他們能拿到的最新原始碼，而 7 月實際發布的版本是 **2.1.206**，可能有差異；Claude Code 後來加的 Mods 等能力，論文裡都沒有。
2. **SWE-bench 成績都是各家自報的**，作者已把它們從對比表裡刪掉，只在腳註裡留作記錄。
3. **工具數量、功能清單、版本號這類資料幾週就會過時。** 相對地，迴圈的分類、7 個子系統的劃分、以及「兩個缺席」這類**結構性結論**目前比較穩定。
4. **論文裡有 3 條 4 月得出的觀察，在 7 月版被新證據推翻後改寫了**——作者選擇就地修訂而非隱瞞。

---

## 對實務者的意義

論文裡最有價值的不是哪一條具體數字，而是**一張地圖**：

> 你在 `CLAUDE.md`、skill、hook、權限規則、子代理上做的每一項配置，都落在這 7 個子系統裡的某一個。

這張圖同時是**除錯分類法**——出問題時先命名子系統，搜尋空間立刻縮小：

| 症狀 | 該看哪個子系統 |
| --- | --- |
| 上下文相關的失敗 | Memory & Context |
| 非預期的工具執行 | Safety & Permissions |
| Session 協調出問題 | Orchestration |
| 工具數量爆炸、prompt 過長 | Tools & Actions（按需載入） |

三條可立即採用的推論：

1. **Skill-first 優於 tool-first。** Skills 採用率超過 MCP，正是因為它把上下文成本處理得優雅——agent 自己推斷何時該用某個 skill，而不是一開始就把所有能力列舉出來。
2. **加能力前先想清楚它在哪個子系統。** 下次猶豫要不要接向量庫、套框架、多拆幾個子代理時，先看看這 11 個系統是怎麼選的。
3. **可以當成可替換後端。** Omnigent 的存在，加上 ACP 在 6 個系統裡取得「harness hosting」這個第三角色，意味著把 Codex CLI 當成可插拔後端已經不是實驗性質——**要可攜性就往 ACP 介面設計，不要綁死 Codex CLI 的細節。**

---

## 結語

論文最後的論點是：**2026 年上半年，coding harness 完成了從「工具」到「平台」的轉身。**

harness 變成可 import 的 SDK，而框架廠商反過來開始出 harness；市集、切換成本工具、企業治理層紛紛出現；agent 可以被當成「一個 OpenAI 相容端點後面的模型」來定址；而第一個 meta-harness（Databricks 的 Omnigent）已經在單一 API 後面編排 11 個廠商 harness（其中半數就在這份語料庫裡），重新實作昂貴的部分、套利專有的部分。

整個領域跑在手寫的非同步迴圈與確定性檢索之上。這**不是限制，而是刻意的工程決策**——被手握全部框架選項、卻一個都沒選的團隊，在約 400 萬行程式碼裡獨立複製了同一件事。

---

## 延伸連結

- 📄 論文原文：[arXiv:2609.00006](https://arxiv.org/abs/2609.00006)｜[HTML 版](https://arxiv.org/html/2609.00006v1)｜[PDF](https://arxiv.org/pdf/2609.00006v1)
- 📝 中文整理版：[拆开 Claude Code、Codex 等 11 个 coding agent（技术栈）](https://jishuzhan.net/article/2107284175783223298)
- 🎬 工程師米奇：[Facebook 專頁](https://www.facebook.com/geekMickey)｜[影片版](https://www.youtube.com/@geekMickey)
- 🏢 作者單位：[Wavestone AI Lab](https://www.wavestone.ai/en/think/ai-lab/)
- 🧩 相關概念：[Omnigent — Databricks 的 meta-harness](https://www.databricks.com/blog/introducing-omnigent-meta-harness-combine-control-and-share-your-agents)

---

> **版權聲明**：本篇文章為論文導讀之學習整理，所有技術內容版權屬論文原作者 Paul Barbaste、Tristan Darrigol、Germain Vu、Tom Wiltberger 及 Wavestone AI Lab 所有（CC BY 4.0）。表格與程式碼範例為根據論文內容重新整理之說明，非原圖原碼。如有錯誤或遺漏，歡迎來信指正。

