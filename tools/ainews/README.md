# tools/ainews — 新一期 AINews 的偵測與通知

**範圍**：偵測 → 記錄 → 通知。**不寫稿、不產圖、不發布。**
寫作管線之後再加，這層的前提是先把「什麼算新」定義清楚。

---

## 為什麼不是「每天檢查一次」

AINews 的到達時間**不固定**（UTC，實測）：

| 日期 | 到達時間（UTC） | 台北時間 |
|---|---|---|
| 11-03 | 05:35 | 13:35 |
| 11-04 | 19:18 | 03:18（隔日） |
| 11-05 | 06:24 | 14:24 |
| 11-06 | 10:36 | 18:36 |
| 11-07 | 03:05 | 11:05 |

沒有任何一個「每天幾點」是穩定貼近到達時間的。每天跑一次 → 最壞延遲 **24 小時**；
每 10 分鐘跑一次 → 最壞延遲 **10 分鐘**，而成本是零，因為——

> **寫入的 key 是 Gmail `messageId`，不是時間。**
> 同一期看到第二次是 no-op，所以跑多快都不會重複發文。

這就是「偵測頻率」和「寫入正確性」被拆開的地方，也是整個設計的核心。

---

## 檔案

| 檔案 | 作用 | 進版控 |
|---|---|---|
| `detect.py` | 判斷哪些訊息是「新的 AINews」；純標準函式庫、不做 I/O 以外的網路操作 | ✅ |
| `seen.json` | **ledger**：以 `messageId` 為 key 的記憶 | ✅（這是站台的記憶） |
| `run_ainews_poll.ps1` | 呼叫 detect → 通知（toast／beep）→ 寫 log | ✅ |
| `install_schedule.ps1` | 註冊／移除每 10 分鐘的 Windows 排程 | ✅ |
| `selftest.py` | 13 項回歸測試（多數在驗「什麼**不該**觸發」） | ✅ |
| `fixtures/sample-payload.json` | 真實的 5 期 payload，供離線測試 | ✅ |
| `out/` | payload 快照、`new-issues.jsonl`、`poll.log` | ❌ gitignore |

---

## 用法

```powershell
# 1. 看 ledger
python tools/ainews/detect.py --show

# 2. 用已存的 payload 試跑（不寫 ledger）
pwsh -File tools/ainews/run_ainews_poll.ps1 -PayloadFile tools/ainews/out/payload.json -DryRun

# 3. 真跑（會寫 ledger、跳通知）
pwsh -File tools/ainews/run_ainews_poll.ps1 -PayloadFile tools/ainews/out/payload.json

# 4. 裝排程（每 10 分鐘）
pwsh -File tools/ainews/install_schedule.ps1
pwsh -File tools/ainews/install_schedule.ps1 -Remove

# 5. 測工具本身
python tools/ainews/selftest.py
```

**Exit code**：`0` = 沒有新東西（常態）／`2` = 有新期／`1` = 錯誤。

---

## 兩個階段的接法（重要）

Gmail 的抓取需要 Composio 的 MCP 工具，**批次檔叫不到**。所以流程拆成兩段：

```
① 抓取（agent session，每 10 分鐘或按需）
     GMAIL_FETCH_EMAILS(query="from:lspace@mail.beehiiv.com subject:AINews")
     → 存成 tools/ainews/out/payload.json

② 判斷與通知（Windows 排程，每 10 分鐘，與 ① 解耦）
     run_ainews_poll.ps1 -PayloadFile out/payload.json
```

兩段頻率不同也沒關係：payload 舊了，② 只會回報 `nothing new`。

---

## 判定規則

一則訊息算「新 AINews」，必須同時滿足：

1. `sender` 含 `lspace@mail.beehiiv.com`
2. `subject` 以 `[AINews]` 開頭
3. `messageId` **不在** `seen.json`
4. `source/_posts/ainews-<slug>-zh.md` **不存在**

第 4 條是「冷 ledger 保護」：如果先手寫了文章、`seen.json` 還是空的，這條會避免把舊期再廣播一次。

---

## 已知限制

- **通知只在有登入的互動式 session 顯示**（`-RunLevel Limited`、`-LogonType Interactive`）。鎖定畫面或登出時，toast 不會出現，但 `poll.log` 仍會記錄。
- **沒有重試**：Gmail 抓取失敗時，payload 不會更新，下一輪自然重試。這是刻意設計——狀態越少越好。
- **不做去重之外的語意判斷**：同一期若改標題重發，會被視為新的一期（`messageId` 不同）。
- **`seen.json` 必須進版控**：它是「這期做過了」的唯一記憶。刪掉它，冷啟動時會靠第 4 條規則補救，但手動改過 slug 的期數可能被重播。

---

## 下一步（尚未實作）

| 階段 | 內容 | 觸發條件 |
|---|---|---|
| 2 | 抽取正文 → 正規化，寫 `out/<messageId>/source.txt` | 偵測到新期 |
| 3 | 產生中文導讀草稿（套 `NOTE_STYLE_CONTRACT.md`＋前兩篇結構） | 階段 2 成功 |
| 4 | 產 5 張 SVG ＋ ComfyUI 封面 3 候選 | 階段 3 成功 |
| 5 | 自我檢查 → 通過則 push（全自動），否則開 PR | 階段 4 成功 |

**階段 5 的降級門檻**（全自動發布的前提）：
字數 < 4k 或 > 12k、圖表 < 3 張、有 `unconfirmed`／`rumor` 字樣卻被當成事實、未翻譯英文段落 > 15% —— 任一成立就**不得直接上線**。
