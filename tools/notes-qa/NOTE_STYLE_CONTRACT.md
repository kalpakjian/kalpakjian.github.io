# 新筆記寫作契約（NOTE STYLE CONTRACT）

> 目的：**新 PDF／新講義轉成筆記時，第一版就是乾淨的**，不需要像這次一樣回頭做全站大掃除。
> 這份契約有兩個部分：**① 寫的時候怎麼寫**（人工／AI 生成時遵守）、**② 產出後自動把關**（`qa_notes.ps1`）。

---

## 0. 為什麼需要它

這次 13 份筆記是「先產出、後清理」——原始稿帶著 `原稿／教材／講義`、頁碼 `pN`、「本節」等痕跡，
所以事後要修 ~2,900 處。**新筆記只要在生成階段就遵守本契約，就不會再產生這些痕跡。**

---

## 1. 產線五階段

| 階段 | 做什麼 | 產出 |
|---|---|---|
| ① 取文 | 從 PDF／PPTX 抽文字與圖，**抽的時候就把頁碼丟掉**（不要寫進草稿） | 純文字草稿 |
| ② 寫稿 | 依本契約寫 **Markdown**（單一來源檔） | `<Name>_Study_Notes.md` |
| ③ 轉檔 | 由 md 產生 **HTML 頁面**（標題→id、目錄、表格）＋ **mc-quiz.html** | `index.html`、`mc-quiz.html` |
| ④ 檢查 | 跑 `qa_notes.ps1`，**必須 0 失敗** | PASS 報告 |
| ⑤ 上線 | `hexo generate` → push → GitHub Actions 部署 | 線上頁面 |

> 重點：**md 是唯一來源**。html 與 quiz 由 md 衍生；之後任何文字修正都要**兩邊同步**（md＋html），
> 否則 ④ 的「標題一致」與「md 連結可解析」會立刻抓到。

---

## 2. 用詞規則（最容易出錯的地方）

| 想指的東西 | 要寫 | 不要寫 |
|---|---|---|
| **課程教材本身**（投影片／PDF／notebook 裡的內容） | **課程**（例：`課程把 12 項原則列成一圈`） | 原稿、教材、講義、本節 |
| **這份筆記自己** | **本筆記**（例：`本筆記補上四個要素`） | 本節、本文 |
| **筆記自己的某個章節** | 直接寫章節名或「**這一節**」（例：`這一節的來源與 §1–§20 不同`） | 本節（會被誤讀成教材的一節） |
| **教材的某頁／某張** | 不要寫頁碼；改寫成內容描述（例：`課程有兩張投影片內容完全相同`） | p12、第 12 頁、第 2、4 頁 |

**三個禁詞（QA 會擋）**：`原稿`、`教材`、`講義`、`本節` → 全部 0 次。

**可以保留的**：
- 篇幅描述：`課程用了四頁講同一件事`、`95 頁的 deck`（這是「為什麼花這麼多篇幅」的依據，不是頁碼引用）
- 檔名出處：`來源：<code>lesson67\Open WebUI.pptx</code>`、頁首的 `涵蓋檔案：…`
- 內容本身的數字：`20 頁合約的第 18 頁`（法律案例，不是教材頁碼）

---

## 3. 頁首區塊（每份筆記固定格式）

Markdown：

```
> 課程：Certificate in Application of Large Language Model (LLM) (Part-time) — Lesson N
> 機構：匯縱專業發展中心（IVDC）
> 涵蓋檔案：`a.ipynb`、`b.py`、`C.pptx`
> 本筆記依課程大綱每一個標題逐一填充內容，並補上定義、參數說明、常見錯誤與考點。
> 所有程式碼與數字都在本機實測（…版本…），實測輸出直接寫進內文。
> ⚠️ **版本時效（YYYY-MM 實查）**：…（完整對照表見 **§x.y**）
> 🖱️ **互動測驗（推薦）**：附錄 E 提供 **60 題線上測驗**（即時計分、進度自動儲存）→ **[開始作答](mc-quiz.html)**
```

HTML 對應：同一段放在 `<blockquote>` 裡，**每一行結尾加 `<br />`**
（否則瀏覽器會把整段擠成一行）。續行（同一句被折行）**不要**加 `<br />`。

---

## 4. 標題／目錄／錨點

- md 的 `##`／`###` 標題文字與 html 的 `<h2>`／`<h3>` 文字**必須逐字相同**（QA 會比對）。
- html 的 `id` 由標題文字自動產生（去標籤、空白→`-`、只留英數與中日韓字）。
  標題改字後**一定要跑** `tools\notes-qa\regen_ids.ps1`，它會重生 id 並同步 md／html 的 `](#…)` 連結。
- 目錄表格：`#` 欄放編號，**連結文字不要再寫一次編號**
  （✅ `| 8 | [Call Azure OpenAI — …](#8-…) |`　❌ `| 8 | [8. Call Azure OpenAI — …](#…) |`）。
- 標題裡的 `<` `>` 佔位符（如 `<供應商>/<模型>`）在 html 必須寫成 `&lt;…&gt;`，否則會被當成標籤吃掉。

---

## 5. 表格

- **不要**出現「頁」「PDF 頁」「教材來源」「對應頁」這種欄位（已全站移除）。
- md 表格**不可**出現字面的 `\r\n`（會讓整張表變成一列）。用批次工具時要寫 `~NL~`，不要寫 `\r\n`。
- 表格前後各留一個空行。

---

## 6. 測驗（mc-quiz.html）

- 題庫放在 `const QUESTIONS = [ … ];`，必須是合法 JSON 陣列，每題有 `q`／`o`／`a`。
- 右上角 nav 的題數文字（`🖱️ 互動測驗（60 題）`）**必須等於**實際題數（QA 會比對）。
- 附錄「互動式線上測驗」標題的題數、正文「附錄 E 提供 60 題」也要同步。

---

## 7. 檔案配對（一個課節 = 四個檔案）

| 檔案 | 角色 | 必須同步 |
|---|---|---|
| `source/<dir>/index.html` | 網頁（單檔、零外部資源、內嵌圖） | ✅ 與 md 標題／文字一致 |
| `source/<dir>/<Name>_Study_Notes.md` | 下載用 Markdown（**唯一來源**） | ✅ |
| `source/<dir>/mc-quiz.html` | 互動測驗 | ✅ 題數與 nav 一致 |
| `source/_posts/<dir>-ivdc.md` | 部落格貼文（摘要 + 連結） | ✅ 標題／數字一致 |

> QA 只把「同時有 `index.html` 與 `*_Study_Notes.md`」的資料夾視為筆記；
> 其他頁面資料夾（`coding-agent`、`dhh-rails-world-2026`…）會自動跳過。

---

## 8. 批次修改工具（事後修正用，也可用在生成階段）

**`tools\notes-qa\yk_replace2.ps1`** — 規則式批次取代（md＋html＋quiz 同時處理）

```
powershell -NoProfile -ExecutionPolicy Bypass -File tools\notes-qa\yk_replace2.ps1 -ruleFile <rules.txt> [-filter <dirName>]
```

規則檔（UTF-8）每行一條，格式 `pattern@@@replacement`：

- `@@@` 分隔樣式與取代字串
- `~NL~` → CRLF、`~LF~` → LF（**取代字串裡**用；樣式裡請直接寫 `\r\n`）
- 樣式是 .NET 正規表達式：**記得轉義** `.` `|` `[` `]` `+` `(` `)`；行錨點用 `(?m)^`
- 腳本本身必須**純 ASCII**（PS 5.1 用 ANSI 讀 .ps1），中日韓字元請放在規則檔裡

其他工具：

| 腳本 | 用途 |
|---|---|
| `regen_ids.ps1` | 由標題文字重生所有 `id`，並同步 md／html 連結 |
| `fix_toc_dup.ps1` | 移除目錄「編號重複」 |
| `fix_header_br.ps1` | 頁首區塊逐行補 `<br />`（只在句尾或 `課程：` 行斷行） |
| `normalize_crlf.ps1` | 把筆記裡的孤立 LF 正規化為 CRLF（`-DryRun` 先預覽、`-Quiet` 只看總結） |
| `qa_notes.ps1` | **品質閘門**（本契約的執行者） |

---

## 9. 品質閘門：`qa_notes.ps1`

```
powershell -NoProfile -ExecutionPolicy Bypass -File tools\notes-qa\qa_notes.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tools\notes-qa\qa_notes.ps1 -Quiet      # 只看總結
powershell -NoProfile -ExecutionPolicy Bypass -File tools\notes-qa\qa_notes.ps1 -Root <dir>  # 指定目錄
```

離開碼：`0` = 全部通過、`1` = 有硬性失敗（可直接當 CI 的 gate）。

> ⛔ **只跑 `tools\notes-qa\` 這一份，不要在別處留副本。**
> 閘門的預設根目錄是「從腳本位置往上找到 `<repo>\source`」，所以正本放在
> `tools\notes-qa\` 才會找到 13 份筆記。`_covergen\` 底下若有舊副本，會發生兩件事：
> ① 它不會跟著正本更新（檢查邏輯過期）；② 從 `_covergen\` 執行時往上找到的層級不對，
> 會**檢查 0 份筆記然後回報通過**（最危險的假通過）。現在的版本已改成找不到就報錯，
> 但正解仍然是只跑正本。

**硬性檢查（必須 0）**

| # | 檢查 | 為什麼 |
|---|---|---|
| 1 | 禁詞 `原稿／教材／講義／本節` | 讓筆記可獨立閱讀 |
| 2 | 頁碼 `pN` | 讀者手上沒有那份 PDF |
| 3 | 頁內錨點全部可解析 | 目錄／交叉引用不會壞 |
| 4 | md 的 `](#…)` 在 html 找得到 | md／html 同步 |
| 5 | 目錄編號不重複 | 版面 |
| 6 | `<li>`／`</li>` 配對 | 版面 |
| 7 | md 無字面 `\r\n` | 表格完整性 |
| 8 | md ↔ html 標題集合相同 | 兩份檔案內容一致 |
| 9 | 頁首區塊有換行（`<br />` ≥ 3） | 網頁上不會擠成一行 |
| 10 | 測驗 JSON 合法、題數與 nav 一致 | 測驗可用 |

**警告（僅提示）**：孤立 LF、`第 N 頁` 這種寫法（可能是合法例子）。

**自我測試樣本**：`tools\notes-qa\qa_selftest\bad-notes\` 是一份**故意有 12 種瑕疵**的假筆記，
用來確認閘門還有效：

```
powershell -NoProfile -ExecutionPolicy Bypass -File tools\notes-qa\qa_notes.ps1 -Root tools/notes-qa/qa_selftest
# 應該 FAIL 並列出 12 項，離開碼 1
```

---

## 10. 新筆記上線前 checklist（8 步）

1. ☐ PDF／PPTX 抽文字時**不帶頁碼**；草稿就寫「課程」不寫「原稿／教材」
2. ☐ 寫 `<Name>_Study_Notes.md`（含頁首區塊、目錄、附錄 A–F）
3. ☐ 產生 `index.html`：標題→`id`、頁首每行 `<br />`、內嵌圖（base64）、零外部資源
4. ☐ 產生 `mc-quiz.html`：`const QUESTIONS` JSON 合法、nav 題數正確
5. ☐ 跑 `regen_ids.ps1`（標題若有改動）
6. ☐ 跑 `qa_notes.ps1` → **必須 0 失敗**
7. ☐ 跑 `npx hexo clean && npx hexo generate` → 無錯誤
8. ☐ push → 等 GitHub Actions `conclusion=success` → 開線上頁面抽查

---

## 11. CI

兩個 workflow 都放在 `.github\workflows\`，**已啟用**，而且**觸發條件刻意不重疊**（不浪費 CI 分鐘數）：

| workflow | 觸發 | 做什麼 | 會擋部署嗎 |
|---|---|---|---|
| `notes-qa.yml` | push 動到 `source/**` | 跑品質閘門**一次**，把結果貼進 Actions 摘要 | 不會（`continue-on-error`） |
| `notes-qa-tools.yml` | push 動到 `tools/notes-qa/**` | 跑 `selftest_tools.py`（工具回歸測試） | 不會（與 `pages.yml` 各自獨立） |

- `notes-qa.yml` 在**同一步**裡跑閘門 → 貼摘要 → 再以閘門的離開碼結束。所以失敗會顯示成紅色的 step，
  但閘門只被執行一次（舊版會跑兩次，浪費 CI 分鐘數）。
- `notes-qa-tools.yml` **故意不設** `continue-on-error`：工具壞掉是真缺陷，值得一個紅燈；
  部署由 `pages.yml` 負責，本來就不受它影響。
- 想停用某一個：直接刪掉 `.github\workflows\` 底下那個檔案即可。

