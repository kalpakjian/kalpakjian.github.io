# tools/diagrams — 把筆記裡的 ASCII 圖換成內嵌 SVG

**給新對話（或未來的自己）的交接文件。** 照著做就能繼續把剩下的筆記做完，不需要讀完整段對話歷史。

> 政策來源：`tools/notes-qa/NOTE_STYLE_CONTRACT.md` **§12**（圖表一律先做 SVG，不要 ASCII 文字圖）。

---

## 0. 新對話的第一步：先問「還剩什麼」

**不要相信任何寫死的進度清單**（會過期）。跑這支，它會即時掃描 `source/` 給你現況：

```powershell
cd C:\Users\princ\blog\tools\diagrams
python inventory.py
```

輸出範例：

```
無待轉圖區塊: 14 份（含本來就沒有圖的筆記）
   streamlit-flask-notes          (跳過 1 個裝飾性程式碼區塊)
   ...
仍待轉換: 8 份 / 40 個圖區塊
   orange-ai-notes                13 圖
   popular-llm-notes               7 圖
   ...
```

看單一筆記有哪些圖：

```powershell
python inventory.py <note-dir>          # 列出 art#1..art#N（行數／框線數／首行）
python inventory.py <note-dir> 3        # 印出第 3 個圖區塊的原文
```

> ⚠️ **`art#N` 的編號只算「真圖」**（自動排除程式碼區塊裡的裝飾分隔線）。
> 這與 `embed_figs.py` 的 `art_index` 用的是同一套判斷，所以可以直接對照。

---

## 1. 一份筆記的完整流程（六步）

以 `<note>` = 筆記目錄名（例如 `generalization-notes`）為例。

### ① 讀圖 + 查圖號

```powershell
cd C:\Users\princ\blog\tools\diagrams
python inventory.py <note>              # 有哪些圖
python inventory.py <note> 1            # 第 1 張的原文
```

同時查**該筆記現有的最大圖號**（新圖要接著編，否則會撞號）：

```powershell
$h=[System.IO.File]::ReadAllText("C:\Users\princ\blog\source\<note>\index.html")
$mx=0; foreach($m in [regex]::Matches($h,'<figcaption[^>]*>圖 (\d+)')){ if([int]$m.Groups[1].Value -gt $mx){ $mx=[int]$m.Groups[1].Value } }
"下一個圖號 = 圖 $($mx+1)"
```

### ② 寫產生器（放 `figures/`）

複製既有的當範本（它們都是「資料驅動」的，改資料即可）：

| 範本 | 適合的圖型 |
|---|---|
| `figures/gen_misc2.py` | 樹狀面板、階梯圖、決策樹、卡片格 |
| `figures/gen_llmintro.py` | 概念大綱（root + 縮排分支）+ 流程鏈 |
| `figures/gen_misc1.py` | 閘道／分流圖、小決策樹 |
| `figures/gen_streamlit.py` | 多層架構（含容器與內部區塊） |
| `figures/make_opencv_svg.py` | 垂直流程圖 + 平行分支（最早的手寫版，未用 svglib） |

基本骨架：

```python
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from svglib import Svg, C, MUT, TXT, CARD2

def fig_x(s):
    s.box(120, 120, 360, 62, "標題", "副標", "teal")   # 圓角框（置中文字）
    s.card(120, 200, 360, 64, "標題", "副標", "blue", num="1")  # 左徽章 + 左對齊
    s.arrow(300, 182, 300, 198)                        # 線段會自動登記供碰撞自檢
    s.text(48, 430, "一句話說明", 13, MUT)

FIGS = [("slug-name", "<note>", 1, 900, 480, "標題", "副標", fig_x, "圖 N：圖說｜手繪 SVG 圖表")]
```

### ③ 產生 + 兩道自動關卡

```powershell
$env:PYTHONIOENCODING='utf-8'
cd C:\Users\princ\blog\tools\diagrams
python figures\gen_x.py                 # 產生 SVG + 量測用 HTML，並印出碰撞自檢結果
```

**關卡 A：線段碰撞自檢**（`svglib.Svg.check()`，產生時自動跑）

抓「文字壓在線／箭頭上」——這是 Chrome `getBBox()` 的**已知盲區**。
輸出必須是 `OK`；若出現 `COLLISION`，把標籤移開（常見做法：`vlabel()` 把標籤放到線的右側）。

**關卡 B：Chrome `getBBox()` 精準量測**

```powershell
$M='C:\Users\princ\.agents\skills\svg-figure-qa\scripts\measure_text.py'
python $M _m_<slug>.html
# 必須是「0 張有排版問題」且退出碼 0（OVERLAP／CARD／EDGE）
```

**關卡 C（可選，若圖片顯示可用）：放大目視**

```powershell
$S='C:\Users\princ\.agents\skills\svg-figure-qa\scripts\shot_svg.py'
python $S _m_<slug>.html "<aria-label 完整字串>" --out chk.png --scale 2
```

### ④ 寫 plan JSON 並嵌入

`embed_figs.py` 會把「第 N 個真圖區塊」換成內嵌 SVG，**md 與 index.html 同步**。

```python
# 用 Python 寫 plan（不要用 PowerShell 的 Set-Content，它會寫入 BOM）
import io, json
D = r"C:\Users\princ\blog\tools\diagrams\figures\\"
plan = [{"art_index": 1, "svg": D + "slug-name.svg",
         "caption": "圖 N：圖說｜手繪 SVG 圖表"}]
io.open("plan_x.json", "w", encoding="utf-8", newline="\n").write(
    json.dumps(plan, ensure_ascii=False, indent=2))
```

```powershell
cd C:\Users\princ\blog\tools\diagrams
python embed_figs.py <note> plan_x.json
```

> `art_index` 必須與 `inventory.py` 印出的 `art#N` 一致。
> `embed_figs.py` 內部會**由大到小**處理（否則換掉前一個會讓索引位移）。

> **例外：`source/_posts/` 的一般文章**（不是 `source/<note>/` 筆記）
> 沒有 `index.html` 孿生檔、`inventory.py` 也掃不到（它只找 `*_Study_Notes.md`）。
> 這種情況用 `figures/embed_pytoolkit.py` 當範本：錨點用單行字串、以 `<!-- FIGn -->`
> 標記做幂等（重跑就地更新）、保留原本的 CRLF，並套用下面的「陷阱 11」。

### ⑤ 重建 + 品質閘門

**先判斷這份筆記有沒有建置腳本**：

```powershell
Get-ChildItem C:\Users\princ\blog\_covergen -Filter 'build_*_html.py' | Select-Object Name
```

| 情況 | 做法 |
|---|---|
| **有**（例：`build_automl_html.py`） | md 改完後**必須重跑建置腳本**，否則 index.html 下次重建就被覆蓋：<br>`cd C:\Users\princ\blog\_covergen; python build_automl_html.py` |
| **沒有** | md 與 index.html 由 `embed_figs.py` 同步改；QA 閘門會檢查兩者標題一致 |

```powershell
cd C:\Users\princ\blog
powershell -NoProfile -ExecutionPolicy Bypass -File tools\notes-qa\qa_notes.ps1 -Quiet
# 必須「failures = 0」且退出碼 0
npx hexo generate        # 必須無錯誤
```

### ⑥ 上傳 + 驗證

```powershell
git add source/<note>/ ; git commit -m "<note>: convert N ASCII diagrams to hand-drawn SVG" -m "..."
git push origin main
gh run list --limit 1          # 等 Deploy Hexo to GitHub Pages = success
```

線上複驗（新圖真的上線、框線殘留歸零）：

```powershell
$h = (Invoke-WebRequest "https://kalpakjian.github.io/<note>/" -UseBasicParsing).Content
([regex]::Matches($h,'<svg')).Count                    # 應增加
([regex]::Matches($h,'[┌┐└┘│─├┤┬┴┼]')).Count            # 應為 0
```

---

## 2. 陷阱清單（都是實際踩過的）

| # | 陷阱 | 症狀 | 解法 |
|---|---|---|---|
| 1 | **圖號撞號** | 兩張圖都叫「圖 3」 | 先查該筆記最大圖號，接著編 |
| 2 | **有建置腳本的筆記** | 改了 html，下次重建被覆蓋 | 改 md → 重跑 `_covergen\build_<note>_html.py` |
| 3 | **沒有建置腳本** | 只改 md，網頁沒變 | `embed_figs.py` 會同時改 md + html |
| 4 | **裝飾性程式碼區塊** | 把「可複製的指令」變成圖片 | `inventory.py` 會自動排除；`art#N` 只算真圖 |
| 5 | **plan JSON 的 BOM** | `json.load` 炸掉 | 用 Python 寫 plan；`embed_figs.py` 用 `utf-8-sig` 讀 |
| 6 | **art_index 位移** | 換掉第 1 張後找不到第 3 張 | `embed_figs.py` 內建由大到小處理 |
| 7 | **文字壓在線上** | 標籤被箭頭穿過 | 產生時的碰撞自檢會抓；標籤改放線的右側（`vlabel()`） |
| 8 | **文字超出畫布／卡片** | 說明文字被切掉 | Chrome `getBBox()` 會報 `[EDGE]`／`[CARD]`；加寬 canvas 或拆行 |
| 9 | **圖片無法目視** | `media omitted: exceeds size limit` | 靠兩道自動關卡（碰撞自檢 + getBBox）；美觀問題靠設計避開 |
| 10 | **在 `_work/` 放重要檔案** | 被 gitignore、新對話看不到 | 引擎與產生器放 **`tools/diagrams/`**（有版控） |
| 11 | **`_posts` 文章的圖說整段不見** | HTML 裡有 `<figcaption>`，畫面上卻沒有 | Fluid 主題的 `main.css` 有 `.markdown-body figcaption:not(.image-caption){display:none}`。**只有 `_posts` 文章**（會載入主題 CSS）要寫 `<figcaption class="image-caption">`；筆記的單檔 HTML 沒有這個規則，所以以前沒踩到。另外主題的 `.image-caption` 會加 `opacity:.65` 與 `margin:-0.75rem auto 2rem`，要一併覆蓋（`embed_pytoolkit.py` 的 `theme_fix()`） |
| 12 | **`_posts` 文章不能用 `embed_figs.py`** | 腳本找不到 `*_Study_Notes.md` 而中止 | 改用 `figures/embed_pytoolkit.py`：單行錨點 + `<!-- FIGn -->` 幂等 + 保留 CRLF（見 §1 ④ 例外） |

---

## 3. 設計規範（house style）

集中在 `svglib.py`，**新圖不要自己寫死顏色**：

| 項目 | 值 |
|---|---|
| 圖卡底色 / 邊框 | `#0d1117` / `#222b36`，`rx=16` |
| 卡片 | `#161b22`（`CARD`）／`#1c2230`（`CARD2`） |
| 文字 | `#e6edf3`（主）／`#8b949e`（次） |
| 階段色 | `teal #2dd4bf`、`blue #58a6ff`、`amber #fbbf24`、`violet #c084fc`、`green #3fb950`、`rose #f472b6` |
| 字型 | `'Segoe UI','Microsoft JhengHei','Noto Sans TC'`；程式碼用 `'Cascadia Mono',Consolas` |
| 標題 / 副標 | `Svg(w, h, aria, title, subtitle)` 會自動畫在 `y=52` / `y=82` |
| 響應式 | `_wrap()` 已加 `style="width:100%;height:auto;display:block"`（保留 viewBox、不寫死寬高） |
| 圖說 | `<figcaption>`，結尾加「｜手繪 SVG 圖表」 |

**尺寸建議**：寬 900–1000；高依內容（流程圖可到 1200）。留白：左 48、上 106。

---

## 4. 檔案

| 檔案 | 用途 |
|---|---|
| `inventory.py` | **先跑這個**：即時盤點還剩哪些圖；也可列出／印出單一區塊 |
| `svglib.py` | **引擎**：house style、卡片／徽章／匯流排／圖例／elbow、`check()` 碰撞自檢、`save()`／`figure()` |
| `embed_figs.py` | 讀 plan JSON，把第 N 個真圖區塊換成內嵌 SVG（md + html 同步） |
| `figures/gen_*.py` | 各筆記的產生器（資料驅動，改資料即可重用） |
| `figures/plan_*.json` | 各筆記的嵌入計畫（`art_index` + `svg` + `caption`） |
| `figures/gen_pytoolkit.py`＋`figures/embed_pytoolkit.py` | **`_posts` 文章**（python-problem-solving-toolkit）的產生器與嵌入腳本；後者含 `theme_fix()`（見陷阱 11、12） |

> 草稿與中間產物（`_m_*.html` 量測用、`*.png` 截圖）留在 `C:\Users\princ\blog\_work\diagrams\`（gitignored），
> 不進版控。**產生器與計畫則放在本目錄**，因為它們是純文字、小、且可重現——
> 這是刻意偏離 `NOTE_STYLE_CONTRACT` §12「腳本放 `_work/`」的地方，理由是要讓交接與重現可行。

---

## 5. 「這份筆記做完了」的定義

- ☐ `inventory.py <note>` 顯示 **0 個真圖區塊**（剩下的都是自動排除的裝飾性程式碼）
- ☐ 產生時碰撞自檢 **全部 OK**
- ☐ `measure_text.py` **0 張有排版問題**、退出碼 0
- ☐ md 與 index.html 的框線字元殘留 = 0（若為 0 才代表圖都換掉了）
- ☐ 頁面仍為**單檔、零外部資源**（`(src|href)="http` 只允許既有的外部超連結）
- ☐ `qa_notes.ps1` **failures = 0**
- ☐ `npx hexo generate` 無錯誤
- ☐ 已 push，且 GitHub Actions `Deploy Hexo to GitHub Pages` = **success**
- ☐ 線上頁面複驗：SVG 數量增加、框線殘留 = 0
