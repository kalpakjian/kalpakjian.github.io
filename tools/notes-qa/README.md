# tools/notes-qa — 筆記品質工具

新 PDF／新講義要變成筆記時，**用這裡的工具讓第一版就乾淨**，不必像 2026-10 那次回頭大掃除。

## 檔案

| 檔案 | 用途 |
|---|---|
| `NOTE_STYLE_CONTRACT.md` | **寫作契約**：用詞、頁碼、頁首、標題／錨點、表格、測驗、檔案配對、上線 checklist |
| `qa_notes.ps1` | **品質閘門**：10 項硬性檢查 + 2 項警告，離開碼 0／1（可當 CI gate） |
| `regen_ids.ps1` | 由標題文字重生所有 `id`，並同步 md／html 的 `](#…)` 連結 |
| `yk_replace2.ps1` | 規則式批次取代（md＋html＋quiz 同時處理），規則檔格式 `pattern@@@replacement` |
| `fix_toc_dup.ps1` | 移除目錄「編號重複」 |
| `fix_header_br.ps1` | 頁首區塊逐行補 `<br />`（只在句尾或 `課程：` 行斷行） |
| `notes-qa.yml` | 選用的 CI workflow（非阻擋式，push 後自動跑 QA 並貼摘要） |

## 快速用法

```powershell
# 品質閘門（預設檢查 <repo>\source 底下所有筆記）
pwsh -File tools/notes-qa/qa_notes.ps1
pwsh -File tools/notes-qa/qa_notes.ps1 -Quiet                 # 只看總結
pwsh -File tools/notes-qa/qa_notes.ps1 -Root <某個目錄>       # 指定目錄

# 標題改字後重生錨點
pwsh -File tools/notes-qa/regen_ids.ps1

# 批次取代（規則檔 UTF-8，每行 pattern@@@replacement）
pwsh -File tools/notes-qa/yk_replace2.ps1 -ruleFile rules.txt -filter local-llm-notes
```

所有腳本都會自動以**自己所在位置**推算 repo 根目錄（`tools/notes-qa` → repo → `source`），
所以整包複製到別台機器也能直接跑。

> 腳本本身維持**純 ASCII**（Windows PowerShell 5.1 用 ANSI 讀 `.ps1`），
> 中日韓字元一律放在規則檔／資料檔裡。

## 啟用 CI（選用）

```powershell
Copy-Item tools/notes-qa/notes-qa.yml .github/workflows/notes-qa.yml
git add .github/workflows/notes-qa.yml ; git commit -m "ci: add notes QA"; git push
```

它與 `pages.yml`（部署）**分開**，且 `continue-on-error: true`，所以**永遠不會擋部署**，
只在 Actions 頁面與 Step Summary 留下檢查結果。

## 自我測試

`qa_selftest/bad-notes/` 是一份**故意有 12 種瑕疵**的假筆記，用來確認閘門還有作用：

```powershell
pwsh -File tools/notes-qa/qa_notes.ps1 -Root tools/notes-qa/qa_selftest
# 預期：FAIL 並列出 12 項，離開碼 1
```
