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
| ③ 轉檔 | 由 md 產生 **HTML 頁面**（標題→id、目錄、表格、**圖表內嵌 SVG**，見 §12）＋ **mc-quiz.html** | `index.html`、`mc-quiz.html` |
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

## 3. 頁首資訊（兩個載體，別搞混）

頁首資訊有**兩個不同的載體**，寫在不同地方、管不同的事（2026-10-16 清查 16 份筆記後定案）：

| 載體 | 在哪裡 | 內容 | 規定 |
|---|---|---|---|
| **副標 `<div class="sub">`** | 只在 `index.html`（md 沒有這一層） | 課程＋課節，例：`IVDC · Certificate in Application of Large Language Model (LLM)`<br>`Lesson 3 · Introduction to LLM` | **每一份都要有內容**（不要留空） |
| **頁首區塊 `> 課程：…`** | md 的標題下方（html 對應 `<blockquote>`） | 課程／機構／涵蓋檔案／實測環境／測驗連結 | **選用、系列制**：目前只有 AutoML 系列（`automl-notes`、`generalization-notes`、`ml-models-notes`）採用；LLM／CV 系列用副標代替 |

Markdown 頁首區塊（**採用時**的格式）：

```
> 課程：Certificate in Application of Large Language Model (LLM) (Part-time) — Lesson N
> 機構：匯縱專業發展中心（IVDC）
> 涵蓋檔案：`a.ipynb`、`b.py`、`C.pptx`
> 本筆記依課程大綱每一個標題逐一填充內容，並補上定義、參數說明、常見錯誤與考點。
> 所有程式碼與數字都在本機實測（…版本…），實測輸出直接寫進內文。
> ⚠️ **版本時效（YYYY-MM 實查）**：…（完整對照表見 **§x.y**）
> 🖱️ **互動測驗（推薦）**：附錄 E 提供 **60 題線上測驗**（即時計分、進度自動儲存）→ **[開始作答](mc-quiz.html)**
```

HTML 對應：同一段放在 `<blockquote>` 裡，**每一行結尾加 `<br />`**，最後一行不用
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
| 11 | 產生 `<li class="opt">` 選項列的測驗，必須同時引用選項陣列（`q.o[k]`） | 少這一行時每個選項都渲染成空的 `<li>`，讀者**完全看不到選項**（本站曾有 12 份測驗如此上線） |

> ✅ **第 9 項已於 2026-10-16 接上（原本是休眠的檢查）**：判斷方式改為「跳過 `<div class="sub">…</div>` 與 `<hr>` 之後，
> 再找第一個 `<blockquote>`」，所以現在每一頁都會真的被檢查。當天就是因為它是休眠的，`generalization-notes`
> 才漏掉 5 個 `<br />`（網頁上擠成一整段）而沒人發現；修好後已用「拿掉全部 `<br />` → 閘門 FAIL」實測過。
> 適用範圍：只有真的放了頁首區塊的筆記會被檢查（目前是 3 份 AutoML 系列）；沒有頁首區塊的頁面
> （第一個 `<blockquote>` 前面還有目錄等內容）會自動跳過。
> 要停用：把這一項從 `qa_notes.ps1` 移除，並在本檔同步刪掉。

**警告（僅提示）**：孤立 LF、`第 N 頁` 這種寫法（可能是合法例子）。

> 換行符號：`.gitattributes` 已把 `*.md`／`*.html` 設為 `text eol=crlf`，所以簽出（含 CI 的 Linux runner）
> 一律是 CRLF，CI 不會再對這些檔案發 lone-LF 警告。本機若出現 LF 檔（例如 ComfyUI／外部工具寫出來的），
> 跑 `normalize_crlf.ps1` 修；`-DryRun` 可先預覽。

**自我測試樣本**：`tools\notes-qa\qa_selftest\bad-notes\` 是一份**故意有 13 種瑕疵**的假筆記，
用來確認閘門還有效：

```
powershell -NoProfile -ExecutionPolicy Bypass -File tools\notes-qa\qa_notes.ps1 -Root tools/notes-qa/qa_selftest
# 應該 FAIL 並列出 13 項，離開碼 1
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

閘門已經**接上部署**：`pages.yml` 的第一個 job 就是品質閘門，`build` 與 `deploy` 都 `needs` 它——
**閘門不通過就不會部署**。

| workflow | 觸發 | 做什麼 | 會擋部署嗎 |
|---|---|---|---|
| `pages.yml` | push 到 `main`（任何變更） | ① 跑品質閘門（結果貼進 Actions 摘要）→ ② `hexo generate` → ③ 部署 Pages | **會**（job `qa` 失敗就停在第一步） |
| `notes-qa-tools.yml` | push 動到 `tools/notes-qa/**` | 跑 `selftest_tools.py`（工具回歸測試） | 不會（工具壞掉給紅燈，但不擋部署） |

- 閘門在 `pages.yml` 裡**只被執行一次**：跑完 → 貼摘要 → 以閘門的離開碼結束該 job。
- 舊的 `notes-qa.yml`（`continue-on-error: true`，永遠不會擋部署）**已移除**——
  那正是「檢查存在、但驗證不痛」的寫照，留著只會製造綠燈假象。
- 想讓某次修補繞過閘門：**不要**用 `continue-on-error`；正解是修好筆記。
  真的非繞不可時，才暫時把 job `qa` 從 `needs` 拿掉，並在 commit 訊息說明原因與還原時間。
- 想停用 `notes-qa-tools.yml`：直接刪掉 `.github\workflows\` 底下那個檔案即可。

---

## 12. 圖表：一律先做 SVG（不要 ASCII 文字圖）

**規則**：筆記裡的**圖表**——流程圖、架構圖、時序圖、關係圖、示意圖——
一律做成**內嵌 SVG**，每一個標籤都是真正的 `<text>` 元素。
⛔ **不要再交 `┌─┐│└┘▼→` 這種用框線字元拼出來的文字圖。**

| | ASCII 文字圖 | 內嵌 SVG |
|---|---|---|
| 對齊 | 靠等寬字元硬湊，中英混排一定歪 | 座標精準，永遠對齊 |
| 文字 | 不能選取、不能搜尋，螢幕閱讀器讀不到 | 可選取／可搜尋／有 `aria-label` |
| 縮放 | 放大就散掉，列印／存 PDF 會走位 | 向量，任意尺寸都清晰 |
| 表達力 | 只有框線與箭頭 | 可顏色分層、圓角卡片、徽章、圖例 |
| 維護 | 改一個字就要重排整張圖 | 產生器腳本改常數即可重出 |

### 12.1 兩種圖、兩條產線（不要用錯）

| 圖的性質 | 用什麼 | 理由 |
|---|---|---|
| **有文字標籤的圖表**（流程圖、架構圖、關係圖…） | **手繪 SVG**（見 12.2） | 文字必須精準；AI 生圖的 CJK 字形會爛成方塊／鬼畫符 |
| **情境插圖／封面**（無文字，只負責意境） | Qwen-Image 2.1（ComfyUI，`qwen-image-illustrations`） | 意境與氛圍是它的強項；文字一律交給 `<figcaption>` |

⛔ **絕對不要**叫 AI 生圖去畫「有中文標籤的流程圖」——兩邊的長處會同時落空。
✅ 封面插圖本身**不含文字**，這是刻意的（見 `qwen-image-illustrations` 硬規則 2）。

### 12.2 SVG 圖表產線（四步，缺一不可）

| 步驟 | 做什麼 | 工具 |
|---|---|---|
| ① 產生 | 寫**產生器腳本**（Python）輸出 SVG：座標抽成常數、重複卡片用迴圈 | 腳本放 `_work/` 或 `_covergen/`（gitignored） |
| ② 量測 | Chrome `getBBox()` 量文字邊界，抓 `[OVERLAP]`／`[CARD]`／`[EDGE]` | `svg-figure-qa/scripts/measure_text.py`，**必須 0 問題且退出碼 0** |
| ③ 目視 | **2× 放大**逐張看「文字有沒有壓到圖形」 | `svg-figure-qa/scripts/shot_svg.py --scale 2` |
| ④ 內嵌 | 直接寫進 `index.html`（build time），維持**單檔、零外部資源** | 該筆記的 `build_*.py` |

**硬規則**：

- ⛔ 量文字邊界**只信 `getBBox()`**，不要用「字數 × 平均字寬」估算——中文全形、上下標、`text-anchor` 都會讓估算失準
- ⛔ **量測通過不等於完成**：②③ 缺一不可。文字壓在圓／線／方框上時，`getBBox()` 永遠看不到（這是已知盲區）
- ⛔ SVG 裡**不可**出現 HTML 標籤（`<sub>`／`<sup>`／`<span>`），上下標要用 `<tspan dy="…" font-size="0.72em">`，否則整張 SVG 會崩成流動文字
- ⛔ 一次只改一件事：**修排版不動顏色、換主題不動座標**，否則無法判斷缺陷是新是舊
- ✅ 深色圖卡自帶底色 `#0d1117` + `print-color-adjust:exact`，列印／存 PDF 才不會變回白底
- ✅ 每張圖給**唯一**的 `aria-label`：量測工具靠它定位，螢幕閱讀器也靠它
- ✅ 圖說放 `<figcaption>`（含「Qwen-Image 2.1 生成插圖」等出處），不要把說明塞進圖裡

### 12.3 這一項**不進**品質閘門（刻意的）

2026-10-26 重查（`tools/diagrams/inventory.py` 實跑）：**ASCII 圖已全部清空** ——
24 份筆記裡 **0 張**待轉（`ai-intro-notes` 圖 11、`llm-intro-notes` 圖 44、
`local-llm-notes` 圖 46、`tpot-notes` 圖 19 已升級成內嵌 SVG；
`neural-network-notes` 判定為「一頁精華」文字區塊，**刻意不轉**，理由見下）。

剩下會被框線字元「誤報」但**不該轉**的兩類，工具已能自動排除：

| 類別 | 樣子 | 為什麼不轉 |
|---|---|---|
| 程式碼區塊的裝飾分隔線 | `# ── 啟動 H2O 伺服器 ──` | 轉成圖會破壞可複製的指令 |
| 「一頁精華／30 秒速查」文字區塊 | `========== 4. 問題 → 激勵函數 ==========` 這種分段 | 它是**散文速查表**不是圖；而且裡面那棵小樹在正文已有完整 SVG（`neural-network-notes` 圖 39），整塊轉成 SVG 是降級 |

> ⚠️ `inventory.py` 的 `MIN_BOX` 從 8 降到 6：真正的樹狀圖最少只用 6 個框線字元，
> 門檻 8 會**漏報**那 4 張小圖（都是關鍵的樹狀／對照圖）。

- 所以這條是**寫作慣例**，靠人與 AI 在產線階段遵守，**不寫成 `qa_notes.ps1` 的硬性檢查**——
  硬性禁止會讓閘門在多份筆記上一次全紅，把真正的缺陷訊號淹掉。
- **既有 ASCII 圖不強制回溯**：已上線且驗證過的頁面維持原樣，不為了換圖去動已驗證的內容。
- **但**：① 新筆記的圖表、② 任何被改到的舊圖，**一律升級成 SVG**。
- 要批次升級時**一張一張做**（每張都要走完 12.2 的 ②③），不要一次改很多張——
  修圖是迭代，改 A 很容易壓出 B。

### 12.4 上線前 checklist（圖表部分）

1. ☐ 這張圖是**圖表**（有文字標籤）還是**插圖**（無文字意境）？前者走 SVG，後者走 Qwen-Image
2. ☐ 產生器腳本放 `_work/`／`_covergen/`（不進版控），只把 SVG 內嵌進頁面
3. ☐ `measure_text.py` → **0 問題、退出碼 0**
4. ☐ `shot_svg.py --scale 2` → 逐張目視（標籤沒壓到節點／線／框、圖例沒被蓋住）
5. ☐ 頁面重新產生後**再量一次**（修圖是迭代，不是一次到位）
6. ☐ 頁面仍是**單檔、零外部資源**（SVG 內嵌、無 `<img src="http…">`）

---

## 13. 粗體標記：`**` 不能直接接中文字

`markdown` 的粗體靠 CommonMark 的 **flanking** 規則配對：`**粗體**` 的結尾 `**` 必須是
right-flanking、開頭的 `**` 必須是 left-flanking。**中文字旁邊這兩條很容易同時不成立**：

| 寫法 | 為什麼壞 | 畫面 |
| --- | --- | --- |
| `速率改由**（fuse）**決定` | 結尾 `**` 前面是標點、後面緊接中文字 → 不是 right-flanking → **收不了尾** | 讀者看到字面的 `**（fuse）**` |
| `但**「2 倍」是…**，` | 開頭 `**` 後面是標點、前面是中文字 → 不是 left-flanking → **開不了頭** | 整段配對錯位，粗體跑到別的地方 |

**這不是罕見個案**：2026-10-27 全站掃描（`tools/notes-qa/check_cjk_bold.js`）量到 **23 個檔案 / 88 行**
受影響，而且多數已經上線多年——粗體在那裡**從來就沒有生效過**，只是中文讀者不容易一眼看出來。

**修法**：那一段改用 HTML 標籤，不要靠 `**` 硬配對。

```markdown
速率改由<strong>熔絲（fuse）</strong>決定
但<strong>「2 倍」是指令發射率，真實 GEMM 只有 12～34%</strong>，而且…
```

站上本來就在 blockquote 用 `<strong>整理說明</strong>`、`<strong>白話說</strong>`，
所以這是既有寫法，不是新花樣。

**檢查方式**（唯讀、不改檔）：

```powershell
node tools/notes-qa/check_cjk_bold.js              # 掃全站
node tools/notes-qa/check_cjk_bold.js <某個.md>    # 只掃某幾個
```

**這一項同樣不進品質閘門**（理由同 §12.3）：硬性檢查會讓 23 個檔案一起紅燈，
把真正的缺陷訊號淹掉。寫稿時靠人與 AI 遵守，交付前跑一次這支工具確認。


