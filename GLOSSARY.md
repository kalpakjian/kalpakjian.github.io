# GLOSSARY.md — 本站共用詞彙（人／agent／程式碼三方）

> **這份檔案只定義「詞」，不定義「規則」。**
> 寫作規則、品質閘門、上線 checklist 在 [`tools/notes-qa/NOTE_STYLE_CONTRACT.md`](tools/notes-qa/NOTE_STYLE_CONTRACT.md)；
> 工具用法在 [`tools/notes-qa/README.md`](tools/notes-qa/README.md)。需要時再拉進 context，不要在這裡複製一遍。
>
> **為什麼要這份檔案**：同一個東西有兩個名字時，agent 每次都要重新猜你在講什麼。
> 下面的「不要叫它」欄是硬性的：改名 = 改這份檔案 + 一次全站取代，不要就地發明新詞。
>
> **什麼時候要改這份檔案**：新增系列、新增檔案角色、某個詞出現兩種講法時。

---

## 1. 產線詞彙（核心，先記這 12 個）

| 詞 | English | 定義（一句話） | 在哪裡 | 不要叫它 |
|---|---|---|---|---|
| **課節** | lesson | 一個教材單位（一份 PDF／PPTX／notebook 組）→ 產出一份筆記 | `source/<dir>/` | 單元、lesson 檔 |
| **系列** | series | 同一門課的多份筆記（本站：IVDC 13 份、AutoML 3 份） | `source/*-notes/` | 課程（見下）、分類 |
| **課程** | course | **教材本身的內容**（投影片／PDF／notebook 裡寫的東西） | 筆記內文 | ⛔ 原稿、教材、講義 |
| **筆記** | study notes | 本站產出的那兩份檔案（md ＋ html） | `source/<dir>/` | ⛔ 講義、教材 |
| **本筆記** | this note | 指「這份筆記自己」時的固定寫法 | 筆記內文 | ⛔ 本節、本文 |
| **唯一來源** | single source | `<Name>_Study_Notes.md`；html 與 quiz 都由它衍生，改字要三邊同步 | 同上 | 主檔、來源檔 |
| **頁首區塊** | header block | 標題下方那段 `<blockquote>` 出處說明（課程／機構／涵蓋檔案…） | 筆記頁首 | header、前言 |
| **目錄** | TOC | 頁首之後的章節表格，`#` 欄放編號 | 筆記 | index、大綱 |
| **附錄** | appendix | 章節之後的 A–G 區塊（速查表／常見錯誤／實測輸出／一頁精華／互動測驗…） | 筆記末段 | 附註、appendix 區 |
| **互動測驗** | mc-quiz | `mc-quiz.html`，題庫在 `const QUESTIONS` | `source/<dir>/mc-quiz.html` | quiz 頁、測驗頁 |
| **封面** | cover | `source/img/covers/<slug>.png`，走固定 **house style**（深色電影感、同一組基底） | `_covergen/` 產出 | 頭圖、banner 圖 |
| **品質閘門** | quality gate | `tools/notes-qa/qa_notes.ps1`，11 項硬性 + 2 警告，離開碼 0／1 | `tools/notes-qa/` | ⛔ 測試（它是 gate，不是 test suite） |

**兩個容易混的詞**：

- **專題**（`source/coding-agent/`、`source/dhh-rails-world-2026/`）＝ 手寫 HTML 多頁專題，**不是筆記**：沒有 md、沒有 quiz，閘門會自動跳過。
- **貼文**（`source/_posts/*.md`）＝ Hexo 貼文（摘要＋連結），**閘門不檢查**它的內文。

---

## 2. 一個課節 = 四個檔案（＋一張封面）

| 檔案 | 角色 | 必須同步 |
|---|---|---|
| `source/<dir>/index.html` | 網頁（單檔、零外部資源、內嵌圖） | 標題／文字與 md 逐字一致 |
| `source/<dir>/<Name>_Study_Notes.md` | 下載用 Markdown（**唯一來源**） | — |
| `source/<dir>/mc-quiz.html` | 互動測驗 | 題數與 nav 一致 |
| `source/_posts/<slug>.md` | 貼文（摘要＋連結） | 標題／數字一致 |
| `source/img/covers/<slug>.png` | 封面 | 檔名與貼文 slug 相同 |

**命名規則（2026-10-16 決定並驗證）**：**slug = `source/` 目錄名，一律不加後綴**；貼文檔名 = 封面檔名 = slug；frontmatter 的 `index_img` 必須等於 `banner_img`，且為 `/img/covers/<slug>.png`。
原本 IVDC 系列的 `-ivdc` 後綴已在 2026-10-16 全站移除（13 個貼文與封面改名、課程總覽頁的圖片連結同步），**舊網址以 meta refresh 轉址保留**在 `source/<yyyy>/<mm>/<dd>/<old-slug>/index.html`。

**工作目錄（不是產出物，不要當成來源）**：
- `_work/<topic>/` — 產線中途的腳本與暫存（`build_notes.py`、`build_quiz.py`、`verify_*.py`…）
- `_covergen/` — 封面產線（ComfyUI Qwen-Image）＋ `<代號>_chapters/` 章節插圖
- `scaffolds/` — Hexo 範本；`tools/` — 工具（`notes-qa/` 是唯一的閘門正本）

> ⛔ **閘門只能有一份**：`qa_notes.ps1` 的正本在 `tools/notes-qa/`。`_covergen/` 底下若留舊副本，從那裡執行會往上找到錯的層級，**檢查 0 份卻回報通過**（最危險的假通過）。

---

## 3. 系列與產線代號對照

| 產線代號 | 對應筆記（`source/`） | 貼文 slug | 驗證狀態 |
|---|---|---|---|
| `l6` | `huggingface-notes` | `huggingface-notes-ivdc` | 已驗證（`l6_chapters/ch03-why-huggingface`） |
| `l7` | `local-llm-notes` | `local-llm-notes-ivdc` | 已驗證（`l7_chapters/ch03-gguf-quantization`） |
| `l8` | `litellm-notes` | `litellm-notes-ivdc` | 已驗證（`make_cover_l89.py` docstring） |
| `l9` | `streamlit-flask-notes` | `streamlit-flask-notes-ivdc` | 已驗證（同上） |
| `ai_intro` / `cv_intro` / `llm_intro` | `ai-intro-notes` / `cv-intro-notes` / `llm-intro-notes` | `<dir>` | 命名對應（推論） |
| `opencv` / `popular` / `pe` / `rai` / `sf` | `opencv-notes` / `popular-llm-notes` / `prompt-engineering-notes` / `responsible-ai-notes` / `streamlit-flask-notes` | `<dir>` | 命名對應（推論） |
| `local_gpu_ml` / `nn5` | `local-gpu-ml-notes` / `neural-network-notes` | `<dir>` | 命名對應（推論） |
| `automl` / `gen` / `mlmodels` | `automl-notes` / `generalization-notes` / `ml-models-notes` | `<dir>` | 已驗證（目錄與檔名一致） |
| `ed_king_queen` | —（一次性封面） | — | 無對應筆記 |

> `l6`–`l9` 是 IVDC LLM 課程的**課節編號**，課程總覽頁是 `/llm-course/`。
> 其餘代號只在 `_covergen/` 內部使用；**要引用某份筆記時請寫 `source/` 目錄名，不要寫代號**。

---

## 4. 品質閘門的檢查名稱（引用時用這 11 個名字）

硬性（必須 0，離開碼 1）：

| 代號 | 檢查 | 為什麼 |
|---|---|---|
| `banned-wording` | 禁詞 0 次 | 筆記要能獨立閱讀 |
| `page-refs` | 無 `pN` 頁碼 | 讀者手上沒有那份 PDF |
| `anchors` | 頁內 `#id` 全部可解析 | 目錄／交叉引用不會壞 |
| `md-links` | md 的 `](#…)` 在 html 找得到 | md／html 同步 |
| `toc-dup` | 目錄編號不重複 | 版面 |
| `li-balance` | `<li>`／`</li>` 配對 | 版面 |
| `literal-crlf` | md 無字面 `\r\n` | 表格完整性 |
| `heading-parity` | md ↔ html 標題集合相同 | 兩份檔案一致 |
| `header-br` | 頁首區塊 `<br />` ≥ 3 | 網頁不擠成一行 |
| `quiz-json` | `QUESTIONS` 可解析、題數與 nav 一致 | 測驗可用 |
| `quiz-options` | 有 `<li class="opt">` 就必須引用 `q.o[k]` | 少這行＝讀者看不到任何選項 |

警告（只提示，不失敗）：`lone-LF`（孤立 LF）、`di-N-ye`（「第 N 頁」寫法）。

---

## 5. 禁用詞與替代寫法（agent 最常犯）

| 想指的東西 | 要寫 | ⛔ 不要寫 |
|---|---|---|
| 教材本身的內容 | **課程** | 原稿、教材、講義 |
| 這份筆記自己 | **本筆記** | 本節、本文 |
| 筆記的某一節 | 章節名，或「**這一節**」 | 本節 |
| 教材的某頁 | 改寫成內容描述（「課程有兩張投影片內容完全相同」） | `p12`、第 12 頁 |

可保留：篇幅描述（「課程用了四頁講同一件事」）、檔名出處（`lesson67\Open WebUI.pptx`）、內容本身的數字（「20 頁合約的第 18 頁」）。

封面另有 hard rule 4：**motif 不可以描述 house style**（`_covergen/validate_plans.py` 會擋）。

---

## 6. 待對齊（open questions，尚未決定）

1. **互動測驗是附錄 E 還是 F？** 14 份用 **E**（16 份筆記中）；`generalization-notes`、`ml-models-notes` 用 **F**（這兩份另有「附錄 G：答錯題目 → 複習章節對照」）。契約 §3 範本寫的是 E。→ 需要選一個 canonical 並統一。
2. ~~**slug 要不要 `-ivdc` 後綴？**~~ **已決定（2026-10-16）：全站移除。** 13 個貼文與封面改名為 `<dir>`、課程總覽頁（`cv-course`／`llm-course`）的圖片連結同步更新、舊網址以 meta refresh 轉址保留。`AGENT-HEALTH.md` 裡的規則以這裡為準。
3. **`generalization-notes` 目前閘門 FAIL**（2026-10-16 實測）：`原稿` html 67／md 37 次、`教材` 8／5 次、`pN` 16／16 次；另有 1244 處孤立 LF、36 處「第 N 頁」。
4. **`ml-models-notes` 硬性全過**，但 2332 處孤立 LF、106 處「第 N 頁」（警告級）。
5. **頁首區塊不是每份都有**：`llm-intro-notes` 的 `<blockquote>` 不存在（閘門只在區塊存在時檢查）。契約 §3 寫「每份筆記固定格式」與現實不符 → 決定「補齊」或「改成選用」。
6. **閘門是非阻擋的**：`notes-qa.yml` 有 `continue-on-error: true`，所以第 3 點的 FAIL **不會擋部署**，只留在 Actions Step Summary。
7. `ed_king_queen` 在 `_covergen/` 沒有對應筆記（一次性產物）。

> 實測基準：2026-10-16 執行 `pwsh -File tools/notes-qa/qa_notes.ps1` → 檢查 16 份、FAIL 1、警告 5；跳過 `coding-agent`、`dhh-rails-world-2026`（非筆記）。

---

## 7. 維護這份檔案

改詞的流程（三步，缺一不可）：

1. 改這份 `GLOSSARY.md`（先決定 canonical，再動檔案）
2. 全站取代：`pwsh -File tools/notes-qa/yk_replace2.ps1 -ruleFile rules.txt`（規則檔 `pattern@@@replacement`）
3. 標題有動就 `regen_ids.ps1`，然後 **`qa_notes.ps1` 必須 0 失敗**

> 新增一個詞的門檻：**它已經在兩個地方有兩個名字**。不要為了完整而補詞，glossary 變長就沒人讀。
