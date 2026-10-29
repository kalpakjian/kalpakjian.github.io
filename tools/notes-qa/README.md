# tools/notes-qa — 筆記品質工具

新 PDF／新講義要變成筆記時，**用這裡的工具讓第一版就乾淨**，不必像 2026-10 那次回頭大掃除。

## 檔案

| 檔案 | 用途 |
|---|---|
| `NOTE_STYLE_CONTRACT.md` | **寫作契約**：用詞、頁碼、頁首、標題／錨點、表格、測驗、檔案配對、上線 checklist |
| `qa_notes.ps1` | **品質閘門**：11 項硬性檢查 + 2 項警告，離開碼 0／1（可當 CI gate） |
| `check_public_links.py` | **站內連結閘門**：`hexo generate` 之後掃 `public/`，把每個 href／src（含相對路徑與同站絕對網址）解析成檔案，少一個就 exit 1 |
| `remove_legacy_stubs.ps1` | 刪除 15 個 `<slug>-ivdc` 過渡轉址目錄（預定 2026-11-28 執行；`-DryRun` 可先預覽） |
| `regen_ids.ps1` | 由標題文字重生所有 `id`，並同步 md／html 的 `](#…)` 連結 |
| `yk_replace2.ps1` | 規則式批次取代（md＋html＋quiz 同時處理），規則檔格式 `pattern@@@replacement` |
| `fix_toc_dup.ps1` | 移除目錄「編號重複」 |
| `fix_header_br.ps1` | 頁首區塊逐行補 `<br />`（只在句尾或 `課程：` 行斷行） |
| `normalize_crlf.ps1` | 把筆記裡的孤立 LF 正規化為 CRLF（`-DryRun` 可先預覽，不會寫檔） |
| `selftest_tools.py` | **工具回歸測試**：用臨時 fixture 驗證上面每支工具（CI 會在工具變動時自動跑） |

> CI：`.github\workflows\pages.yml`（push 到 `main` 時**先跑閘門，不通過就不部署**）與
> `.github\workflows\notes-qa-tools.yml`（push 動到 `tools/notes-qa/**` 時跑上面的工具回歸測試）。
> `pages.yml` 在 `hexo generate` 之後還會跑 `check_public_links.py`：跨頁連結與破圖
> 不通過就不部署（`qa_notes.ps1` 只看得到單頁，看不到這種錯）。
> 詳見 `NOTE_STYLE_CONTRACT.md` §9–§11。

## 快速用法

```powershell
# 品質閘門（預設檢查 <repo>\source 底下所有筆記）
pwsh -File tools/notes-qa/qa_notes.ps1
pwsh -File tools/notes-qa/qa_notes.ps1 -Quiet                 # 只看總結
pwsh -File tools/notes-qa/qa_notes.ps1 -Root <某個目錄>       # 指定目錄

# 站內連結（先建站，再掃 public/；CI 會在 generate 之後跑同一步）
npx hexo clean ; npx hexo generate
python tools/notes-qa/check_public_links.py                   # 預設 <repo>\public
python tools/notes-qa/check_public_links.py -Root out --quiet  # 只看總結

# 標題改字後重生錨點
pwsh -File tools/notes-qa/regen_ids.ps1

# 批次取代（規則檔 UTF-8，每行 pattern@@@replacement）
pwsh -File tools/notes-qa/yk_replace2.ps1 -ruleFile rules.txt -filter local-llm-notes

# 行尾正規化（先預覽再寫）
pwsh -File tools/notes-qa/normalize_crlf.ps1 -DryRun
pwsh -File tools/notes-qa/normalize_crlf.ps1

# 工具回歸測試（臨時 fixture，不會動到真筆記）
python tools/notes-qa/selftest_tools.py
```

所有腳本都會自動以**自己所在位置**推算 repo 根目錄（`tools/notes-qa` → repo → `source`），
所以整包複製到別台機器也能直接跑。`qa_notes.ps1` 與 `normalize_crlf.ps1` 更進一步
**逐層往上找到 `source` 為止**，因此就算從別的位置執行也不會找錯目錄（也不會「檢查 0 份卻回報通過」）。

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

`qa_selftest/bad-notes/` 是一份**故意有 13 種瑕疵**的假筆記，用來確認閘門還有作用：

```powershell
pwsh -File tools/notes-qa/qa_notes.ps1 -Root tools/notes-qa/qa_selftest
# 預期：FAIL 並列出 13 項，離開碼 1
```
