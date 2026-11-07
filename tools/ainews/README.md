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
| `detect.py` | 階段 1：判斷哪些訊息是「新的 AINews」；純標準函式庫 | ✅ |
| `seen.json` | **ledger**：以 `messageId` 為 key 的記憶 | ✅（這是站台的記憶） |
| `extract.py` | **階段 2**：mail body → 乾淨、分區的來源文字 | ✅ |
| `extract_new.py` | 階段 2 driver：走 ledger，把 `detected` 的期數抽成 `source.txt` | ✅ |
| `run_ainews_poll.ps1` | 呼叫 detect → 通知（toast／beep）→ 寫 log | ✅ |
| `install_schedule.ps1` | 註冊／移除每 10 分鐘的 Windows 排程 | ✅ |
| `selftest.py` | 13 項階段 1 回歸測試（多數在驗「什麼**不該**觸發」） | ✅ |
| `selftest_extract.py` | 21 項階段 2 回歸測試 | ✅ |
| `stress_extract.py` | 規模壓力測試（105 KB body） | ✅ |
| `_make_large_fixture.py` | 產生結構真實的大 fixture（CI 用） | ✅ |
| `_make_real_fixture.py` | 從真實 Gmail 回應造 fixture（手動、可選） | ✅ |
| `fixtures/sample-payload.json` | 真實的 5 期 metadata | ✅ |
| `fixtures/full-message-sample.json` | 小型結構樣本 | ✅ |
| `fixtures/large-issue.json` | 105 KB 結構壓力樣本（產生檔） | ✅ |
| `out/` | payload 快照、每期 `message.json`／`source.txt`／`extract.json`、log | ❌ gitignore |

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

## 階段 2：抽取正文

```powershell
# agent 抓一封完整信，存成 out/<messageId>/message.json
#   GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID(format="full")  ->  message.json

# 然後（可與輪詢同一支排程一起跑）
python tools/ainews/extract_new.py              # 所有 detected 且還沒抽的
python tools/ainews/extract_new.py --only <id>  # 只做一期
python tools/ainews/extract_new.py --dry-run    # 看看會做什麼
```

輸出（每期一個目錄）：

```
out/<messageId>/
  message.json     ← agent 存的原件（gitignored）
  source.txt       ← 人看的分區純文字（gitignored）
  extract.json     ← 給階段 3 用的結構化資料（gitignored）
```

`extract.json` 的形狀：

```json
{
  "messageId": "...", "subject": "...", "date": "...",
  "lede": "主編導言全文",
  "sections": [
    {"index": 1, "key": "twitter", "title": "AI Twitter Recap",
     "headings": [...], "text": "..."},
    {"index": 2, "key": "reddit_container", "title": "AI Reddit Recap",
     "subsections": [{"title": "/r/LocalLlama + /r/localLLM Recap", "key": "local", "text": "..."}]}
  ],
  "stats": {"sections": 5, "chars": 103902, "words": 11896,
            "headings": 54, "quantities": 590, "chars_by_section": {...}}
}
```

**為什麼要有 `stats`**：階段 5 的降級判斷要用它。「`quantities` 太少」代表這期沒什麼硬數字，寫成長文一定是灌水；「`chars` 暴增」代表可能是別的形式（例如純贊助或公告），不該套同一個模板。

### 抽取器移除的東西（實測）

| 雜訊 | 為什麼要移除 |
|---|---|
| 贊助商整段（`“...“ —`） | 否則 Neo4j / Backblaze 的文案會混進文章 |
| `“AI News for MM/DD-…“` masthead | 那是每期都一樣的刊頭 |
| `View image: (...)` / `Caption:` | 指向 beehiiv CDN 的圖，對導讀沒用 |
| 頁尾「plain text version」 | 純樣板 |
| 零寬字元、單獨 `\r` 行 | 會讓後續的空白行邏輯錯亂 |

保留的：**lede**（主編的導言，那才是敘事）、**所有 recap 區塊**、**空 H2 摺疊後的粗體小標**（例如 `**What happened**`）。

---

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
