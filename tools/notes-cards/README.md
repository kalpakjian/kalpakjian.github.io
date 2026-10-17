# tools/notes-cards — AutoML 速記卡產生器

從 `source/automl-notes/summary.html`（精簡版頁面）**一鍵重生**速記卡牌組，輸出到
`source/automl-notes/cards.html`（緊湊版）與 `source/automl-notes/cards-large.html`（大字版）。

卡片內容＝精簡版的每個 `<h2>` 區段；`splits.txt` 可在指定的 `<h3>` 再切一刀，
所以「章節對應卡片」這件事是資料驅動的，精簡版更新後重跑即可同步。

## 檔案

| 檔案 | 用途 |
|---|---|
| `build-cards.ps1` | 產生器：切卡 → 加編號圓標／單元色帶 → 依實測高度分欄打包 → 套模板輸出 |
| `measure-cards.ps1` | 量測器：用 headless Edge 量每張卡在**列印版面**下的真實高度，並數 PDF 頁數 |
| `template.html` | 版型（CSS／單元色／站台導覽／列印按鈕），含 `@@...@@` 佔位符 |
| `splits.txt` | 切卡規則：`區段id|切點h3|新卡標題|原卡改名` |
| `groups.txt` | 圓標／色帶分組：`起始卡號|結束卡號|css類別|標籤文字` |
| `labels.txt` | 模式文案與參數：`模式.鍵=值`（body／title／print／pagehint／alt／pagemargin） |
| `heights-compact.txt`、`heights-large.txt` | 各模式的實測卡片高度（mm，一行一張，供打包使用） |

## 使用（兩段式：先量測、再打包）

```powershell
# 緊湊版（A4 橫向・每頁 3 張・7 頁）
powershell -NoProfile -File tools/notes-cards/build-cards.ps1  -Mode compact -ColMax 198
powershell -NoProfile -File tools/notes-cards/measure-cards.ps1 -Mode compact      # 產生 heights-compact.txt
powershell -NoProfile -File tools/notes-cards/build-cards.ps1  -Mode compact -ColMax 198   # 用真實高度重打包
powershell -NoProfile -File tools/notes-cards/measure-cards.ps1 -Mode compact      # 驗證頁數

# 大字版（A4 橫向・每頁 2 張・10 頁）
powershell -NoProfile -File tools/notes-cards/build-cards.ps1  -Mode large -Pack pairs
powershell -NoProfile -File tools/notes-cards/measure-cards.ps1 -Mode large
```

參數：`-ColMax` 單欄可用高度（mm，A4 橫向＝210 − 2×邊界；邊界 6mm → 198）、
`-ColGap` 卡距（mm，需與 template 的 `.col{gap}` 一致）、`-Pack pairs|masonry`、
`-Out` 輸出檔名。

## 驗證

```powershell
powershell -NoProfile -File tools/notes-qa/qa_notes.ps1   # 必須 failures = 0
```
`measure-cards.ps1` 會回報每張卡高度與 PDF 頁數；頁數＝`ceil(欄數/2)`，即
`build-cards.ps1` 印出的 `sheets=`。

## 注意事項

- 兩支 .ps1 **刻意維持純 ASCII**：Windows PowerShell 5.1 以 ANSI 讀取 .ps1，
  中文放在 UTF-8 資料檔（splits／groups／labels／template）才不會亂碼。
- PowerShell 變數**不分大小寫**：內容變數命名為 `$deck`，避免覆蓋檔名參數 `$Out`。
- 量測需要 Microsoft Edge 或 Chrome（headless）；已加 `--disable-sync` 等旗標避免
  同步程序的 stderr 被 PowerShell 當成終止錯誤。
- `.gitattributes` 要求 `.html` 為 CRLF：提交前可跑 `tools/notes-qa/normalize_crlf.ps1`。
