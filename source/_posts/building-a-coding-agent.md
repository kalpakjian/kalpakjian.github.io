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
  - MCP
  - Ollama
  - 開源工具
  - Python
toc: true
index_img: /img/covers/building-a-coding-agent.png
banner_img: /img/covers/building-a-coding-agent.png
---

> <strong>整理說明</strong>：本文的起點是 Geoffrey Huntley〈Replaced〉一文引發的爭論——「2026 年的資深工程師應該能重建 Claude Code 這類最基本的 agent」——以及 Shopify CEO Tobi Lütke 把 AI 使用納入績效與資源分配考量的內部備忘錄。前半先把那句話「合理」與「過頭」的部分分開；後半把它落地成一份可以照著做的實作指南：六個零件、一個迴圈，以及一支約 90 行、真的能跑起來的 Python 骨架。文章後段再拿 <a href="https://cline.bot/cli">Cline CLI</a> 這個開源 harness 當對照組，看同一組零件在生產級產品上長成什麼樣子。相關論點與連結見文末「參考來源」。

<!-- more -->

## 一句話總結

> 做一個 coding agent，難的從來不是模型，而是<strong>context 管理、工具權限、驗證迴路與失敗恢復</strong>。把這四件事做對，你就已經做出 Claude Code 的核心骨架——模型只是隨時可以換掉的零件。

換個說法：<strong>agent = 模型 + harness</strong>。模型提供智能，harness（外殼）負責把智能變成真實世界裡的工作。這篇文章講的是 harness。

但反過來也要說清楚：<strong>harness 完整，並不保證等於強 agent</strong>。像 Cline CLI 這樣功能齊全的開源 harness，能給你 agent 的骨架、工具、審批與自動化，卻不能給你判斷力——它的智能上限，等於<strong>你接的模型</strong>加上<strong>你設計的驗證迴路</strong>。這是第八節要展開的對照。

---

## 先把那句話拆開：哪部分合理，哪部分過頭

Huntley 的原意並不是「每個人都要複製 Anthropic 的產品」。他指出的是你應該懂 agent 的基本構成：

- 讀取專案檔案與程式碼
- 呼叫 shell、測試、git 等工具
- 維持任務上下文
- 根據錯誤結果迭代修正
- 在適當時機停下來交給人審查

換言之，重點是<strong>能設計與駕馭工作迴路</strong>，而不是只會在 IDE 裡按「Accept suggestion」。至於「做不出 Claude Code 就不算資深」這種講法，當成警號與練習目標可以，當成資格判定就過頭了：

| 說法 | 合理程度 | 判斷 |
| --- | --- | --- |
| 工程師應理解 context window、tokenization、工具呼叫與 agent 迴圈 | 高 | 這是現代 AI 工程的基本素養 |
| 應該有可展示的 AI 實作專案 | 高 | 比只會聊天式使用 AI 更有說服力 |
| 應能自己建立小型 coding agent | 中高 | 對後端、平台、自動化、AI 工具工程師特別有價值 |
| 做不出 Claude Code 就不是資深工程師 | 低到中 | 過度絕對；資深價值還包括系統設計、維運、安全、領域知識與團隊協作 |
| 用 AI 兩週完成過去 50 萬的專案 | 需保留 | 可能發生，但高度依賴專案類型、既有程式碼、測試與人類監督 |

Tobi Lütke 的立場則更接近管理層面的要求：AI 不再只是個人效率工具，而是影響招聘、資源分配與績效評估的工作方式。但這也不等於「所有工程師都必須造一個 Claude Code」，Shopify 的要求更接近「必須主動、熟練地將 AI 納入日常工作」。

<div class="callout">
  <div class="callout-title">本文的立場</div>
  <p>「資深工程師要能重建 Claude Code」適合當成<strong>練習目標</strong>，不適合當成<strong>資格判定</strong>。真正會被淘汰的不是「沒有自己寫 Claude Code」的人，而是仍然只用 AI 複製貼上、無法設計驗證、也不願承擔工程責任的人。</p>
</div>

---

## 一、一個 coding agent 只有六個零件

不管是一百行的研究原型，還是百萬行的產品，拆開來都是同樣六個零件。前五個是**內層 agent**（Claude Code 本體），第六個加上「規格檔 + 每輪單一任務」就是**外層 Ralph 迴圈**。

這不是紙上分類。市面上已經有把六個零件全部做出來的成品——例如 <a href="https://cline.bot/cli">Cline CLI</a>。第八節會拿它逐一對照，看同一組零件在生產級規模上長成什麼樣子。

| # | 零件 | 作用 | 對應文章中的說法 |
| --- | --- | --- | --- |
| 1 | **模型（policy）** | 決策：下一步做什麼 | 可替換，本地或 API 皆可 |
| 2 | **工具（action space）** | 它能對世界做什麼 | 讀檔、shell、測試、git |
| 3 | **迴圈（control loop）** | 決策 → 執行 → 觀察 → 再決策 | 「設計與駕馭工作迴路」 |
| 4 | **Context 管理器** | 決定模型每一輪看到什麼 | 維持任務上下文 |
| 5 | **護欄（guardrails）** | 沙箱、白名單、步數上限、人工批准 | 「適當時機停下來交給人」 |
| 6 | **驗證器（verifier）** | 測試／lint／type check／git diff | 「根據錯誤結果迭代修正」 |

<div class="callout">
  <div class="callout-title">最容易被忽略的一點</div>
  <p>第 6 個零件不是選配。<strong>「完成」的定義必須是可驗證的</strong>——測試綠燈、型別檢查通過、diff 符合預期——而不是模型說「我做完了」。這是整套設計的靈魂，也是業餘作品與工程級 harness 的分界線。</p>
</div>

---

## 二、資料流：一句話講完

```
目標 ──▶ [ system prompt + 工具 schema + 當前狀態 ] ──▶ LLM
          ▲                                              │
          │                                        tool_call
          │                                              ▼
      結果截斷後回饋 ◀── 執行工具（讀檔／改檔／跑測試／git）
          │
          └── 重複，直到：模型宣告完成 ／ 驗證通過 ／ 超過步數 ／ 需要人工批准
```

整個 agent 就是這個 `while` 迴圈。所有複雜度都藏在「括號裡那三件事」：**餵什麼給模型**、**允許它做什麼**、**怎麼判斷它做對了**。

---

## 三、工具設計：不要一開始就給 30 個工具

工具是 agent 的 action space，也是它唯一能改變世界的手段。最小可用集如下：

| 工具 | 關鍵設計點 |
| --- | --- |
| `read_file(path, start, end)` | **帶行號區間**，不要整檔塞進 context |
| `list_files(glob)` | 先讓它知道專案長什麼樣 |
| `grep(pattern, glob)` | 定位比全讀便宜 100 倍 |
| `edit_file(path, old, new)` | **`old` 必須唯一匹配**，否則回報錯誤讓它重試 |
| `write_file(path, content)` | 僅用於建立新檔 |
| `run_shell(cmd, timeout)` | 黑名單 + 逾時 + 輸出截斷 |
| `run_tests()` | 包好的測試指令，agent 不必自己猜 |
| `git_status` / `git_diff` | 讓 agent 看到自己改了什麼 |
| `todo_write` | 把計畫外顯化，防止它亂飄 |

`edit_file` 的「`old` 必須唯一匹配」是 Claude Code 風格精準 patch 的核心。若同一段文字出現兩次，工具應該**拒絕執行並回報出現次數**，而不是猜一個位置改下去——這樣才不會產生無法 review 的巨大 diff。

每一個工具都要有：**JSON schema、權限等級、逾時、輸出上限、人類可讀的錯誤訊息**。錯誤訊息寫得好，等於免費提升 agent 的成功率。

---

## 四、Context 管理：真正的難點

Context 不是「把東西都塞進去」，而是**每一輪重新組裝**：

```
[ system  ]  角色 + 工具使用規則 + 安全紅線
[ project ]  專案規則檔（類 CLAUDE.md）：怎麼跑測試、禁止改哪些目錄
[ task    ]  本輪唯一任務 + 驗收條件            ← 每輪重新注入（乾淨 context）
[ state   ]  當前 todo + 最近一次錯誤 + git diff
[ history ]  舊輪次壓縮成摘要，工具輸出只留頭尾
```

三個鐵則：

1. **工具輸出一定要截斷**——保留開頭與結尾，中間省略。一次 `npm test` 的完整輸出就足以吃掉半個視窗。
2. **檔案用 grep 定位 + 區間讀取**，不要整份讀進來。
3. **超過預算就摘要舊輪次**，但「目標與驗收條件」永遠不能被摘要掉。

<div class="callout">
  <div class="callout-title">這就是 Ralph 所謂的「乾淨 context」</div>
  <p>Ralph 迴圈常被形容成一種神秘框架，但它技術上只是在做一件事：<strong>每一輪都把 agent 的 context 清空重建，只留下目標、規格與驗收條件</strong>，讓它從 git 紀錄、進度檔與測試結果重新認識自己的處境。這不是魔法，是 context 管理策略。</p>
</div>

---

## 五、護欄：沒有這一層，就不要讓它自動跑

這是絕大多數人跳過、然後付出代價的一層。

- **路徑白名單**：任何解析後落在 workspace 之外的路徑直接拒絕（防 `../../` 逃逸）。
- **危險指令黑名單**：`rm -rf`、`git push --force`、`curl | sh`、磁碟格式化等 → 攔截並要求人工執行。
- **三重硬上限**：步數、token、單指令時間。三者都要有，否則就是一個無限迴圈燒錢機。
- **動工前先快照**：`git commit` 或 `git stash`，讓「回滾」是一個指令，而不是一場災難。
- **dry-run 模式**：寫入與刪除類工具先印出 diff 給人看，確認後才落地。

生產級 harness 也是這樣設計的：Cline CLI 預設就是<strong>逐步審批</strong>——每一處檔案修改與指令執行都要你點頭，diff 攤在眼前；auto-approve 可以開，但那是你主動交出的權限，不是預設值。這種「預設安全、主動放權」的順序，值得直接抄進自己的骨架。

<div class="callout">
  <div class="callout-title">順序很重要</div>
  <p>護欄要在「讓它自動跑」<strong>之前</strong>做完，不是在出事之後補。這也是 Ralph 迴圈被誤解的地方——「無人值守自動完成軟體」是過度簡化的說法；實務上它仍需要人類做規格設計、code review、架構判斷與安全把關。</p>
</div>

---

## 六、驗證迴路：測試就是 agent 的煞車系統

每次改動後自動串成 pipeline：

```
格式化 → lint → type check → 單元測試 → （可選）整合測試
```

失敗時，把 **stderr + `git diff`** 當作下一輪的 context 餵回去。如此一來，agent 不需要「聰明」，它只需要**會看紅字**。

沒有測試的 agent，得到的不是生產力，而是高產能的破壞者——它會在幾分鐘內產生你花一整天才能 review 完的程式碼，而其中沒有任何一處被驗證過。

---

## 七、最小可跑的 Python 骨架

以下假設使用 OpenAI 相容 API（Ollama、vLLM 或雲端皆可），約 90 行就能跑起來。它已經包含前面講的六個零件中的五個：模型、工具、迴圈、context 截斷、護欄。

```python
# mini_agent.py  —  最小 coding agent
import os, pathlib, subprocess, json
from openai import OpenAI

ROOT = pathlib.Path.cwd().resolve()
MODEL = os.getenv("MODEL", "qwen2.5-coder:7b")
MAX_STEPS, MAX_OUT = 25, 6000
BLOCK = ("rm -rf", "git push", "shutdown", "mkfs", "curl | sh")

client = OpenAI(base_url=os.getenv("BASE_URL", "http://localhost:11434/v1"),
                api_key=os.getenv("API_KEY", "not-needed"))

# ---------- 工具 ----------
def _safe(p: str) -> pathlib.Path:
    fp = (ROOT / p).resolve()
    if fp != ROOT and ROOT not in fp.parents:
        raise ValueError(f"拒絕存取 workspace 外的路徑: {p}")
    return fp

def read_file(path: str, start: int = 1, end: int = 200) -> str:
    lines = _safe(path).read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(f"{i}\t{l}" for i, l in enumerate(lines[start-1:end], start))

def grep(pattern: str, glob: str = "**/*") -> str:
    hits = []
    for p in ROOT.glob(glob):
        if not p.is_file() or ".git" in p.parts:
            continue
        for i, l in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if pattern in l:
                hits.append(f"{p.relative_to(ROOT)}:{i}: {l.strip()}")
    return "\n".join(hits[:200]) or "(無符合)"

def edit_file(path: str, old: str, new: str) -> str:
    fp = _safe(path); text = fp.read_text(encoding="utf-8")
    if text.count(old) != 1:
        return f"ERROR: old 必須唯一匹配，實際出現 {text.count(old)} 次，請提供更長的片段"
    fp.write_text(text.replace(old, new), encoding="utf-8")
    return f"OK: 已修改 {path}"

def run_shell(cmd: str, timeout: int = 60) -> str:
    if any(b in cmd for b in BLOCK):
        return "ERROR: 指令被安全規則攔截，需人工執行"
    try:
        r = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True,
                           text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return f"ERROR: 逾時 {timeout}s"
    return f"exit={r.returncode}\n{r.stdout[-MAX_OUT:]}\n{r.stderr[-MAX_OUT:]}"

REGISTRY = {"read_file": read_file, "grep": grep,
            "edit_file": edit_file, "run_shell": run_shell}

SCHEMA = [
    {"type": "function", "function": {"name": "read_file", "parameters": {
        "type": "object", "properties": {"path": {"type": "string"},
        "start": {"type": "integer"}, "end": {"type": "integer"}},
        "required": ["path"]}}},
    {"type": "function", "function": {"name": "grep", "parameters": {
        "type": "object", "properties": {"pattern": {"type": "string"}},
        "required": ["pattern"]}}},
    {"type": "function", "function": {"name": "edit_file", "parameters": {
        "type": "object", "properties": {"path": {"type": "string"},
        "old": {"type": "string"}, "new": {"type": "string"}},
        "required": ["path", "old", "new"]}}},
    {"type": "function", "function": {"name": "run_shell", "parameters": {
        "type": "object", "properties": {"cmd": {"type": "string"}},
        "required": ["cmd"]}}},
]

# ---------- 迴圈 ----------
def agent(goal: str):
    msgs = [
        {"role": "system", "content": (
            "你是 coding agent。規則：\n"
            "1. 先用 grep 定位，再 read_file 讀區間，不要整檔讀。\n"
            "2. 修改用 edit_file 做最小 patch。\n"
            "3. 改完必須執行測試驗證，看到綠燈才算完成。\n"
            "4. 不要捏造結果，只回報工具輸出的事實。")},
        {"role": "user", "content": goal},
    ]
    for step in range(1, MAX_STEPS + 1):
        r = client.chat.completions.create(model=MODEL, messages=msgs, tools=SCHEMA)
        m = r.choices[0].message
        msgs.append(m.model_dump(exclude_none=True))
        if not m.tool_calls:
            return f"[step {step}] 完成：{m.content}"
        for tc in m.tool_calls:
            fn = REGISTRY[tc.function.name]
            args = json.loads(tc.function.arguments or "{}")
            try:
                out = fn(**args)
            except Exception as e:
                out = f"ERROR: {type(e).__name__}: {e}"
            print(f"[step {step}] {tc.function.name}({args}) -> {str(out)[:200]}")
            msgs.append({"role": "tool", "tool_call_id": tc.id, "content": str(out)})
    return "已達步數上限，交回人工審查。"

if __name__ == "__main__":
    import sys
    print(agent(sys.argv[1]))
```

執行方式（以 Ollama 為例，需支援 tool calling 的模型）：

```powershell
ollama pull qwen2.5-coder:7b
$env:MODEL="qwen2.5-coder:7b"; $env:BASE_URL="http://localhost:11434/v1"
python mini_agent.py "幫我找出 utils.py 裡的 bug 並修好，修完跑 pytest 驗證"
```

<div class="callout">
  <div class="callout-title">假設與限制</div>
  <p>這份骨架假設端點支援 OpenAI tool-calling 格式。若你的本地模型不支援 <code>tools</code>，就把工具描述寫進 system prompt，改成「要求模型輸出 JSON → 自行解析」的土砲做法，<strong>其餘架構完全不變</strong>。這也正好說明了一件事：模型是可替換的零件，harness 才是你的作品。</p>
</div>

---

## 八、生產級對照：Cline CLI 把同一組零件做到什麼程度

前面七節你手上已經有一個 90 行、能跑的最小版本。現在把鏡頭拉遠，看一個已經上線的開源 harness 把同一組零件做到什麼程度——**Cline CLI**。

Cline 原本以 VS Code 擴充聞名；CLI 2.0 之後，它把同一套 agent runtime 帶進終端機，支援 headless、CI／CD、script 與管線使用。用 Huntley 那套標準看，它大約落在：

> **一個可直接使用、可自訂、可接本地模型的通用 coding agent harness**——能力接近 Claude Code，但設計哲學更偏「開放模型選擇 ＋ 明確審批」。

它已經具備 agent 的核心迴路：

- 讀取專案結構與相關檔案，建立任務 context
- 建立、修改、刪除檔案，並以 diff 呈現變更
- 執行 shell 指令，即時觀察 stdout／stderr
- 根據 linter、compiler、測試輸出除錯並重試
- 透過 MCP 接資料庫、API、瀏覽器、基礎設施等外部工具
- 支援 Plan／Act：先規劃，確認後才執行

所以它不是「會建議程式碼的工具」，而是能<strong>自己完成一連串工程動作</strong>的 agent。

### 同一組零件，兩種規模

| # | 零件 | 你的 90 行版本 | Cline CLI |
| --- | --- | --- | --- |
| 1 | 模型 | 一個 OpenAI 相容端點 | 幾乎任意：雲端 API、OpenAI-compatible endpoint、Ollama／LM Studio 本地模型 |
| 2 | 工具 | 四個（`read_file`／`grep`／`edit_file`／`run_shell`） | 檔案增刪改（diff 呈現）、shell、MCP servers、SDK 自訂工具與 lifecycle hooks |
| 3 | 迴圈 | 單層 `while`，25 步上限 | 完整 agent runtime，另可放進 cron／CI／script，stdin／stdout 可串接 Unix 工具 |
| 4 | Context | 手動截斷工具輸出 | Plan／Act、checkpoint、task 狀態 |
| 5 | 護欄 | 路徑白名單、指令黑名單、步數上限 | 預設逐步審批（可開 auto-approve），diff 可見 |
| 6 | 驗證器 | 你自己指定的測試指令 | 讀 linter／compiler／測試輸出後自行重試 |

看完這張表，最該注意到的不是「它工具比較多」，而是：你的四個工具只是它工具層的一個**子集**。真正的差距在<strong>零件 4 與 5 的成熟度</strong>，以及<strong>零件 1 可替換的廣度</strong>——這三格，才是「能跑」與「能上線」之間的距離。

### 能力盤點

| 能力 | Cline CLI 的程度 |
| --- | --- |
| 單一任務自主完成 | 強：可讀檔、改檔、跑指令、依錯誤修正 |
| 人類控制 | 強：預設可逐步批准檔案修改與指令；也可開 auto-approve |
| 模型自由度 | 很強：支援多家 API、OpenAI-compatible endpoint、Ollama／LM Studio 等本地模型 |
| 工具擴充 | 強：MCP servers、SDK、自訂工具與 lifecycle hooks |
| 自動化整合 | 強：可放進 cron、CI、script，stdin／stdout 可串接 Unix 工具 |
| 多 agent 協作 | 中等偏新：Cline Kanban 可平行跑多個 agent，各自用獨立 git worktree |
| 長任務記憶與 context 管理 | 中等：有 Plan／Act、checkpoint、task 狀態，但複雜長跑任務仍很依賴規格與人工拆解 |

這張表裡最誠實的一格是<strong>最後一格</strong>。Context 管理是公認最難的零件，連生產級產品都還在做「中等」——你在第四節看到的那三個鐵則（截斷輸出、grep 定位、摘要舊輪次），就是這個難題的最小解。

### 和 Claude Code 的定位差異

| 面向 | Cline CLI | Claude Code |
| --- | --- | --- |
| 定位 | 開源、可自選模型的 agent harness | Anthropic 官方、深度整合 Claude 模型的終端 agent |
| 模型 | 幾乎任意：雲端 API、本地 Ollama／LM Studio | 主要鎖定 Claude 模型 |
| 使用介面 | VS Code／JetBrains／CLI／SDK，IDE 體驗特別強 | 終端機原生體驗 |
| 控制方式 | 預設逐步審批，diff 可見，適合想保留控制權的人 | 也有審批與權限機制，但整體更偏流暢的終端工作流 |
| 多 agent | Kanban 平行任務、git worktree 隔離 | Agent Teams／sub-agents 較成熟 |
| 適合誰 | 想用本地模型、控制成本、重視開放性與可審查性的人 | 想要最少設定、追求 Claude 生態最佳整合的人 |

這張表的目的不是排名。它們在光譜上位置不同：**Cline 把選擇權交給你**（模型、成本、審批粒度），**Claude Code 把整合度做到最高**。要選哪一邊，取決於你更在意「可替換」還是「少設定」。

### 真正的上限：harness 能力 ≠ 實際表現

Cline CLI 的 agent 能力要分兩層看：

1. **Harness 能力**：已經很完整——檔案操作、shell、MCP、Plan／Act、審批、headless 執行。
2. **實際表現**：主要由你接的模型決定。接 Claude Opus／Sonnet 時可接近 Claude Code；接較小或較弱的本地模型時，規劃、長 context、工具呼叫與除錯能力會明顯下降。

<div class="callout">
  <div class="callout-title">這正是本文的核心論點</div>
  <p><strong>Cline 是很好的 harness，但不保證等於強 agent。</strong>它給你 agent 的骨架；模型、rules、MCP 工具、測試與任務拆解，才決定它能走多遠。反過來說——這也正是為什麼本文花七節講 harness：骨架是你唯一能控制的部分。</p>
</div>

### 如果你想親手驗證 Huntley 那句話

以本地模型、開源、可自訂與成本控制為優先，Cline CLI 比 Claude Code 更適合當主要實驗平台：

- 用 Ollama／LM Studio 接本地模型，測試**不同模型在同一個 harness** 下的表現差異——這是理解「模型是可替換零件」最快的實驗
- 用 MCP 把 PDF／OCR、檔案整理、Git、Python 腳本接進工作流
- 在 CLI 或 CI 中跑重複性任務：批次整理文件、生成測試、檢查專案結構
- 用 Plan／Act 與逐步審批，配合「先理解底層、再逐步放手」的節奏

但要<strong>真正理解</strong> harness，建議再往下讀一層：它的 tool-call 格式、system prompt、context 組裝與 auto-approve 邏輯。最有效的練習，是用它的 SDK 寫一個只有「讀檔、寫檔、跑 Python、跑測試」四個工具的迷你版——那其實就是本文第七節那份骨架，只是換成 SDK 的形狀。

### 一句話評價

> **Cline CLI 是「開源、模型自由、可審查」的 Claude Code 替代品；作為 agent harness 已達生產可用級，但它的智能上限等於你所選的模型，加上你設計的驗證迴路。**

<div class="callout">
  <div class="callout-title">換個角度看這張對照表</div>
  <p>如果你只想「用」agent，Cline CLI 可以現在就裝。但如果你想「懂」agent，這張表反而是一份<strong>閱讀清單</strong>：零件 4 的 checkpoint 怎麼存、零件 5 的 auto-approve 規則怎麼寫、零件 2 的 MCP 工具怎麼註冊。把這幾處讀完，你就不是在猜 harness 在做什麼，而是在驗證它。</p>
</div>

---

## 九、漸進式里程碑：不要一次做完

| 階段 | 目標 | 驗收標準 |
| --- | --- | --- |
| M1 | 唯讀 agent：`list_files` / `grep` / `read_file` | 能正確回答「這個 bug 在哪個檔哪一行」 |
| M2 | 加上 `edit_file` + `git_diff` | 能改一個函式且 diff 乾淨 |
| M3 | 加上 `run_shell` + 測試驗證迴路 | 測試紅燈能自行修正到綠燈 |
| M4 | Context 壓縮 + todo 外顯化 | 連續 20 步不爆 context |
| M5 | 護欄：路徑白名單、黑名單、dry-run、批准點 | 嘗試 `../` 與 `rm -rf` 被正確攔截 |
| M6 | 外層 Ralph loop：規格檔 + 每輪單一任務 + 進度檔 | 無人干預下完成一個小型規格 |

<div class="callout">
  <div class="callout-title">鐵則</div>
  <p><strong>M5 沒做完就不要進 M6。</strong>這是絕大多數人踩的坑——先讓它自動跑，出事後才想補護欄，順序完全相反。</p>
</div>

---

## 十、內層 agent vs 外層 Ralph 迴圈

這兩個名詞常被混用，但職責完全不同：

| | 內層 agent | 外層 Ralph 迴圈 |
| --- | --- | --- |
| 單位 | 一個任務內的一步 | 一整個任務／一輪迭代 |
| Context | 累積當前工作狀態 | **每輪清空重建** |
| 記憶 | 對話歷史 | git log + 進度檔 + 規格檔 |
| 終止條件 | 測試通過 | 規格的所有驗收條件通過 |
| 誰負責 | 模型 | **你（規格設計者）** |

外層迴圈本質上就是：

```python
while not spec_satisfied():
    spawn(agent, next_smallest_task)
    verify()      # 測試 / lint / type check
    commit()      # 讓下一輪能從 git 讀到自己的成果
```

所以「Ralph 不是框架，而是把工程師的角色從逐行寫程式，搬到規格設計與驗證」這個說法，在技術上是站得住的。它把工程師的職責重新排序成四件事：

1. 寫清楚規格與驗收條件
2. 設計可自動驗證的測試
3. 控制 agent 的執行範圍與風險
4. 審查、整合並修正產出

---

## 十一、常見陷阱

1. **一開始就想做 multi-agent 或自主規劃** → 先讓單一 agent 跑得穩。
2. **沒有測試就讓它自動跑** → 你得到的不是生產力，是高產能的破壞者。
3. **工具輸出直接灌進 context** → 兩輪就爆掉，模型注意力也被稀釋。
4. **用整檔覆寫代替精準 patch** → 每次修改都產生巨大 diff，無法 review、無法回滾。
5. **沒有步數與 token 上限** → 一個迴圈燒掉一整天的額度。
6. **沒有 git 快照** → 失敗時無法恢復，只能手動收拾。
7. **把「模型說完成」當成完成** → 唯一的完成定義是驗證器綠燈。

---

## 結語：一個比較健康的資深標準

如果要把 Huntley 的說法改寫成一句可以真正拿來自我要求的話，我會這樣寫：

> 一位 2026 年的資深工程師，應該能<strong>安全地</strong>將 AI agent 整合進真實工程流程，並能判斷何時該信任它、何時必須介入。

具體能力包括：

- 能把模糊需求轉成可驗證的規格
- 能設計測試、型別檢查與 CI，作為 agent 的煞車系統
- 能評估不同模型、harness 與 token 成本
- 能審查 AI 產生的架構與安全風險
- 能教團隊建立可重複的 AI 工作流

回到實作層面：**做一個 coding agent，就是做一個「有嚴格工具介面、有預算限制的 context 管理器，外面套一層可驗證的迴圈」。** 把 context 預算、工具權限、驗證與回滾做對，你就已經做出 Claude Code 的核心骨架，也才真的符合那個「能設計與駕馭工作迴路」的標準。

而 Cline CLI 正好從另一個方向證明了同一件事：它把六個零件都做到了生產級，所以你<strong>不需要從零造一個</strong>；但如果你不清楚那六個零件在做什麼，你也就無法判斷它的輸出該不該信、該在哪一步插手。**harness 可以下載，判斷力不行。**

延伸閱讀：本站另一篇〈[剖開 11 個主流 coding agent 的原始碼](/2026/10/09/harness-engineering-eleven-coding-agents/)〉整理了 11 個生產級系統的 7 個標準子系統與 18 條設計建議，可以當作本文的架構對照表。

---

## 參考來源

- Geoffrey Huntley, 〈Replaced〉：<https://ghuntley.com/replaced/>
- Geoffrey Huntley, 〈Ralph Wiggum as a software engineer〉（Ralph 迴圈）：<https://ghuntley.com/loop/>
- snarktank/ralph（Ralph 實作）：<https://github.com/snarktank/ralph>
- Tobi Lütke 的 Shopify AI 內部備忘錄整理：<https://www.thefoundersreport.com/tobi-lutke-shopify-ai-mandate-public-memo>
- Codacy Blog, 〈What Everyone Gets Wrong About the Ralph Loop〉：<https://blog.codacy.com/what-everyone-gets-wrong-about-the-ralph-loop>

**Cline CLI（第八節對照對象）**

- Cline 官方網站：<https://cline.bot/>
- Cline CLI 產品頁：<https://cline.bot/cli>
- Cline 原始碼（GitHub）：<https://github.com/cline/cline>
- Cline CLI 官方文件：<https://docs.cline.bot/usage/cli-overview>
- 〈Cline vs Claude Code〉（Morph）：<https://www.morphllm.com/comparisons/cline-vs-claude-code>
- 〈Best Open-Source AI Coding Tools 2026〉（Frontman）：<https://frontman.sh/blog/best-open-source-ai-coding-tools-2026/>
- 〈Cline Guide〉（DeployHQ）：<https://www.deployhq.com/guides/cline>
- 〈Claude Code vs Cline〉（CodePick）：<https://codepick.dev/zh/compare/claude-code-vs-cline/>

> 本文為學習整理用途，程式碼骨架為原創示例，可直接取用修改。內容觀點部分來自上述來源，版權屬原作者所有。
