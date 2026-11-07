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
| `DIGEST_CONTRACT.md` | **階段 3 規格**：骨架、配額、語氣、SVG、該不該寫 | ✅ |
| `digest_lint.py` | 階段 3 閘門：結構 + 數字溯源 | ✅ |
| `brief.py` | **階段 3b**：抽成寫稿大綱（頭條候選／數字清單／未證實／不可寫） | ✅ |
| `figures.py` | **階段 4**：四種固定版型，從大綱生成 inline SVG | ✅ |
| `cover.py` | **階段 4b**：依故事選 motif、產封面候選、安裝 | ✅ |
| `selftest_figures.py` | 22 項階段 4 回歸測試 | ✅ |
| `_check_fig_layout.py` | 用瀏覽器量測文字是否溢出（程式化取代肉眼） | ✅ |
| `_preview_figures.py` | 把 SVG 渲成 PNG 供目視 | ✅ |
| `_check_motifs.py` | 封面 motif 選擇的黃金案例檢查 | ✅ |
| `selftest_brief.py` | 17 項階段 3b 回歸測試 | ✅ |
| `_check_brief_quality.py` | 品質檢查：機器排序 vs 已發布的頭條 | ✅ |
| `check_bold_render.py` | 粗體**實際渲染**檢查（唯一可信） | ✅ |
| `run_ainews_poll.ps1` | 呼叫 detect → 通知（toast／beep）→ 寫 log | ✅ |
| `install_schedule.ps1` | 註冊／移除每 10 分鐘的 Windows 排程 | ✅ |
| `selftest.py` / `selftest_extract.py` / `selftest_lint.py` | 13 + 21 + 11 項回歸測試 | ✅ |
| `stress_extract.py` | 規模壓力測試（105 KB body） | ✅ |
| `_probe_bold.py` | 從渲染結果反推粗體規則（研究用） | ✅ |
| `fixtures/*` | 樣本 payload／結構樣本／壓力樣本 | ✅ |
| `out/` | 每期 `message.json`／`source.txt`／`extract.json`、log | ❌ gitignore |

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

## 階段 4：出圖

```powershell
# 內文圖（決定性：同一份資料 → 同一張圖）
python tools/ainews/figures.py --brief out/<id>/brief.json --out out/<id>

# 版面檢查（用瀏覽器量測，比肉眼可靠）
python tools/ainews/_check_fig_layout.py out/<id>/figures.html

# 封面（需要 ComfyUI；`--no-render` 只產 prompt）
python tools/ainews/cover.py --brief out/<id>/brief.json --slug ainews-x-zh
python tools/ainews/cover.py --slug ainews-x-zh --pick 2
```

### 四種版型，只填資料不改版面

| 版型 | 資料來源 | 什麼時候用 |
|---|---|---|
| `kpi_row` | `number_ledger`（每區塊取一個） | 開頭的四個硬數字 |
| `ranking` | `headline_candidates` 分數 | 展示排序（自己就是一種「我怎麼挑」的說明） |
| `bar_compare` | **同單位**的數字 | 同一則新聞內的量級對比 |
| `delta` | 前後兩個值 | 「改之前 / 改之後」 |

全部沿用 `tools/diagrams/svglib.py`，所以與站上其他內嵌圖同一套配色與字型。

### 三條硬規則（都是踩過才寫下的）

1. **不同單位的數字不進同一張長條圖。** 第一版拿 `594B`（參數）跟 `96.32 tok/s`（吞吐）比長度，
   視覺上很漂亮，**語意上是錯的**。現在依單位分組，只畫最大的同單位那一組，不足 2 條就不畫。
2. **資料不夠就不畫。** 一條長條不是圖表，一張 KPI 卡不是版面。版型回傳 `None`，由上層跳過。
3. **`<svg>` 內不得有空行。** 這是第 2 篇的舊傷：marked 會把圖拆成 `<p>`，瀏覽器隨即丟掉所有
   `<rect>`，整張圖只剩文字。`selftest_figures.py` 的 f6 直接把這條釘住。

### 為什麼版面檢查要寫成程式

我花了三輪「看截圖猜哪裡壞」。後來改成用瀏覽器的 `getBBox()` 量測：

```
fig1 (940x300): 1 text(s) overflow
    [card] '96.32 tokens'  right=678  edge=677
```

**溢出 1px**——螢幕上根本看不出來，但那是真的錯。程式一量就講清楚。
所以 `_check_fig_layout.py` 比 `_preview_figures.py`（截圖）更重要：前者是判準，後者只是給人看的。

### 封面：唯一保留人工閘門的一步

內文圖是決定性的，封面不是。同一個 prompt 跑三次會得到三張不同的圖，而**沒有任何 lint 能判斷
「這張圖的隱喻對不對」**。所以 `cover.py` 只做到「產候選 + 基本檢查（尺寸、檔案大小）」，
安裝（`--pick`）是刻意的第二個指令。

motif 由標題與頭條決定（`money` / `weights` / `model_release` / `agent` / `benchmark` /
`hardware` / `security` / `default`），用 `_check_motifs.py` 對已發布的期數做黃金驗證。

> 這裡也踩過一次：Inkling 那期（開源權重**釋出**）被判成 `weights`（權重**解讀**），
> 因為 `weights` 這個字兩邊都有。修法是檢查順序——「釋出」優先於「解讀」——並收窄後者的詞彙。

---

```powershell
python tools/ainews/brief.py --extract tools/ainews/out/<id>/extract.json --out tools/ainews/out/<id>
```

`extract_new.py` 預設**自動**產生大綱（`--no-brief` 可關）。

產出 `brief.md`（給人看）與 `brief.json`（給程式用），內容是**機器能做的那一半**：

| 區塊 | 內容 | 為什麼有價值 |
|---|---|---|
| `verdict` | 判斷該寫長導讀還是短訊 | 防止把活動宣傳硬寫成 9k 字 |
| `headline_candidates` | 前 6 名頭條，附**計分理由** | 挑頭條不再靠重讀 100KB |
| `number_ledger` | 每區塊的硬數字清單 | 寫稿照抄，不用回頭找 |
| `flagged_claims` | 原文自己標「據稱／未證實」的句子 | 避免把傳言寫成事實 |
| `contradiction_watch` | 同單位多值 | 避免引用錯的那個數字 |
| `do_not_write` | 贊助／活動字串 | 避免廣告文案混進來 |

### 排序規則（可解釋，不靠模型）

```
分數 = 硬數字×3 + 具名實體×2 + 評測名詞×2 + 新穎性×2
```

**「硬數字」必須帶單位**（`594B`、`81.7%`、`96.32 tok/s`），因為裸數字幾乎都是噪音：
日期 `2026-11-06`、表格列號、清單序號。這條是踩過的坑——第一版把日期算成量化指標。

**實體抽取**排除句首大寫詞（`Reaching`、`Post`、`Activity`），只保留重複出現、
含內部大寫、含數字，或在 `KNOWN` 白名單（`Tinker`、`Mythos`、`Anthropic`…）的詞。
不做 NER，但足以把型號與實驗室名挑出來。

### 為什麼大綱不寫任何一句正文

因為「這期值不值得寫、我的主張是什麼」是判斷，不是整理。
大綱只給**材料與提醒**，正文留給人（或留給後續要接的模型，但那是另一個決定）。

---

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
