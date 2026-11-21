# 第 12 章 · 後端網站開發工作流程

## 1. 後端開發與 IDE

### 1.1 後端開發概述

後端負責應用程式的核心邏輯、資料庫互動與伺服器維護。要提升開發效率，**整合開發環境（IDE）** 是最重要的工具之一：它涵蓋程式編輯、除錯與專案管理。

### 1.2 IDE 的作用

IDE 用於撰寫、除錯與測試程式，提供自動補全、語法高亮、內建版本控制等功能，讓開發者專注於業務邏輯；現代 IDE 多半還支援多語言與框架。

### 1.3 熱門後端 IDE 比較

| IDE | 定位 | 主要特點 | 適合場景 |
| --- | --- | --- | --- |
| **VS Code** | 微軟 2015 推出的輕量、跨平台開源編輯器 | 擴展豐富、內建 Git 與終端、除錯強大 | JS／Node.js 等；初學到資深皆宜 |
| **IntelliJ IDEA** | JetBrains，主打 Java／Kotlin | 智能補全、Spring 等框架支援、重構強 | 企業級 Java、大型專案 |
| **PyCharm** | JetBrains，主打 Python | Python 專屬支援、Django／Flask 整合、資料庫工具、科學運算 | Python 後端、資料分析 |
| **Eclipse** | 老牌開源（IBM 起家） | 多語言、插件生態大、大型專案穩定 | 企業／傳統 Java 專案 |
| **NetBeans** | Oracle 支持、開源 | Java 支援完整、介面簡潔、跨平台 | 教學與中小型 Java 專案 |

- **VS Code**：優點是輕量、快、擴展多、跨平台；缺點是插件多時較慢、大型 Java 專案不如 IntelliJ。
- **IntelliJ IDEA**：優點是 Java 支援強、重構出色；缺點是耗資源、免費版缺企業功能。
- **PyCharm**：優點是緊密整合 Python 框架與資料庫；缺點是免費版功能少、大型專案可能有瓶頸。
- **Eclipse**：優點是免費、多語言、穩定；缺點是介面較舊、學習曲線陡。
- **NetBeans**：優點是介面簡潔、適合新手；缺點是生態不如前兩者、大型專案效能較差。

**雲端 IDE**：如 GitHub Codespaces、AWS Cloud9，直接在瀏覽器開發，免本地設定、利於團隊協作。

### 1.4 選擇 IDE 的考量

語言／框架支援、編譯與除錯功能、插件擴展性、效能與資源佔用、社群支援。全端開發者常選 VS Code；專注 Java 的團隊多選 IntelliJ IDEA。

### 1.5 未來趨勢

IDE 朝 **自動化、雲端化、協作化** 發展；開發者宜持續關注新工具與技術。
## 2. Git 版本控制

### 2.1 版本控制概念

- **是什麼**：記錄檔案的變更歷史，可回溯、比較與協作。
- **重要性**：保存歷史、支援多人協作、可分支實驗、能安全回退。
- **類型**：本地、集中式（如 SVN）、分散式（如 Git）。

### 2.2 Git 簡介

Git 是 **分散式** 版本控制系統（由 Linus Torvalds 於 2005 年開發）。每個克隆都是一份完整倉庫，離線也能操作；相較集中式（SVN）更快、分支更輕量。

### 2.3 安裝 Git

依作業系統從官網安裝（Windows／macOS／Linux），安裝後檢查：

```
git --version
```

### 2.4 Git 配置

```
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global core.editor "vim"
```

`~/.gitconfig` 常見內容：

```
[user]
    name = Your Name
    email = your.email@example.com
[core]
    editor = vim
    autocrlf = input
[alias]
    st = status
    co = checkout
    ci = commit
    br = branch
```

### 2.5 初始化與克隆

```
mkdir myproject && cd myproject
git init                                     # 建立新倉庫（產生 .git）
git clone https://github.com/user/repo.git   # 克隆遠端倉庫
```

### 2.6 基本操作

```
git add filename            # 加入暫存區（git add . 加入全部）
git commit -m "提交信息"     # 提交
git status                  # 查看狀態
git log                     # 查看日誌（--oneline 簡化）
git diff                    # 比較工作目錄與暫存區
git diff --staged           # 比較暫存區與上次提交
```

### 2.7 分支管理

分支讓多人／多功能**並行開發**、隔離風險、便於版本回溯。

```
git checkout -b new-branch      # 建立並切換（= git branch + git checkout）
git checkout branch-name        # 切換分支
git merge branch-name           # 合併到當前分支
git merge --no-ff branch-name   # 保留分支歷史（不快進合併）
```

合併衝突時手動解決，再：

```
git add resolved-file
git commit -m "解決合併衝突"
```

### 2.8 遠端倉庫

```
git remote add origin https://github.com/user/repo.git
git push origin branch-name
git pull origin branch-name
git fetch
```

- **本地 vs 遠端**：本地只存在你的電腦；遠端存在伺服器、多人可存取。本地操作不影響遠端，只有 push 時才更新遠端。
### 2.9 標籤管理

```
git tag tag-name                 # 輕量標籤
git tag -a tag-name -m "描述"     # 附註標籤
git tag                          # 列出所有標籤
git push origin tag-name         # 推送單一標籤
git push origin --tags           # 推送全部標籤
git tag -d tag-name              # 刪除本地標籤
git push origin :refs/tags/tag-name   # 刪除遠端標籤
```

### 2.10 忽略文件（.gitignore）

在倉庫根目錄建立 `.gitignore`：

```
# 忽略所有 .log 文件
*.log
# 忽略 node_modules 目錄
node_modules/
# 忽略特定文件
secret.txt
```

檢查：`git status` 應看不到被忽略的檔案。

### 2.11 撤銷與回滾

```
git checkout -- filename         # 撤銷工作目錄中的修改
git reset HEAD filename          # 撤銷暫存（保留工作目錄修改）
git reset --soft HEAD~1          # 撤銷最近一次提交、保留變更
git reset --hard HEAD~1          # 完全撤銷最近一次提交與變更
git revert commit-hash           # 以新提交回滾特定提交
git commit --amend -m "新訊息"    # 修改最近一次提交訊息
git checkout commit-hash         # 回到某歷史版本（git checkout main 回最新）
```

### 2.12 Stash（暫存工作進度）

```
git stash                 # 保存當前工作進度
git stash list            # 查看列表
git stash apply           # 恢復（保留 stash）
git stash pop             # 恢復並刪除
git stash drop stash@{0}  # 刪除指定
git stash clear           # 刪除全部
```

### 2.13 比較與分析

```
git diff commit1 commit2   # 比較兩個提交
git log -p                 # 顯示每個提交的差異
git blame filename         # 逐行顯示最後修改者
```

二分搜尋問題提交：

```
git bisect start
git bisect bad HEAD
git bisect good commit-hash
# ...Git 自動切換提交，找到後：
git bisect reset
```

### 2.14 其他常用命令

```
git rm filename            # 刪除文件並提交
git rm --cached filename   # 只從暫存區移除（保留工作目錄）
git mv old-filename new-filename   # 移動／重命名
git branch -a              # 列出本地與遠端分支
git diff > patch.patch     # 產生補丁
git apply patch.patch      # 套用補丁
```

### 2.15 常見工作流程

- **Feature 分支**：從主分支切出功能分支 → 開發 → 合併回主分支 → 刪除。

```
git checkout main
git checkout -b new-feature
git add .
git commit -m "添加新功能"
git checkout main
git merge new-feature
git branch -d new-feature
```

- **Git Flow**：使用 `master` 與 `develop`；新功能在 feature 分支開發後併回 develop；發布走 release 分支；緊急修復走 hotfix 分支。
  - 註：GitHub 自 2020 年起新倉庫預設分支名為 `main`，原理相同。

### 2.16 進階技巧

**Git Alias**（寫在 `.gitconfig` 的 `[alias]`）：

```
[alias]
    st = status
    co = checkout
    lg = log --oneline --graph --decorate --all
```

**Git Hooks**：在 `.git/hooks/` 放腳本，於特定事件自動執行（如 `pre-commit`）：

```
#!/bin/sh
# pre-commit hook example
echo "Running pre-commit hook"
./run-tests.sh
```

```
chmod +x .git/hooks/pre-commit
```

**Git Submodules**：把另一個倉庫放進子目錄：

```
git submodule add https://github.com/user/submodule-repo.git path/to/submodule
git submodule init
git submodule update
```

### 2.17 GitHub 與 GitLab

- **GitHub**：全球最大的代碼託管平台，提供 Pull Request、Issues、Actions。
- **GitLab**：功能類似，並內建 CI/CD。

```
git clone https://github.com/username/repository.git
git clone https://gitlab.com/username/repository.git
```

### 2.18 最佳實踐

- **撰寫良好的提交訊息**：標題簡明（不超過 50 字）＋正文說明原因與做法。
- **保持提交歷史簡潔**：用 `git rebase -i HEAD~n` 整理提交。
- **用標籤管理版本**：`git tag v1.0.0` → `git push origin v1.0.0`。

### 2.19 小結

本章介紹後端開發與 IDE 選擇，以及 Git 的完整基礎：配置、初始化、基本操作、分支、遠端、標籤、忽略文件、撤銷與回滾、Stash、比較分析、工作流程、進階技巧與最佳實踐。

## 3. Git 進階操作

### 3.1 分支策略與工作流程

**分支策略**

- **Feature 分支**：開發新功能，完成後併回主／開發分支。
- **Release 分支**：發布前測試與修復，穩定後併入主分支並打標籤。
- **Hotfix 分支**：緊急修復主分支問題，修好後併回主分支與開發分支。

**合併方式**

- **快進（Fast-Forward）**：目標分支是當前分支的直接後續，只移動指標、不產生新提交。
- **三方合併（Three-Way）**：分支歷史分歧時，建立一個合併提交。
- **無快進（No Fast-Forward）**：即使可快進也強制產生合併提交，保留分支歷史。

```
git merge --ff-only branch-name   # 快進
git merge branch-name             # 三方合併
git merge --no-ff branch-name     # 無快進
```

**常見工作流程**

- **Git Flow**：`master` + `develop`；feature → develop；release → 測試後併 master 並打標籤；hotfix → 併回 master 與 develop。

<figure class="fig-svg"><svg viewBox="0 0 860 250" width="100%" role="img" aria-label="Git Flow 分支模型：main、develop、feature、release、hotfix" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><line x1="150" y1="170" x2="820" y2="170" stroke="#2c6fb1" stroke-width="2"/><line x1="150" y1="120" x2="820" y2="120" stroke="#39d0d8" stroke-width="2"/><line x1="200" y1="120" x2="330" y2="70" stroke="#f0a04b" stroke-width="1.8"/><line x1="330" y1="70" x2="420" y2="120" stroke="#f0a04b" stroke-width="1.8"/><line x1="450" y1="120" x2="560" y2="30" stroke="#f0a04b" stroke-width="1.8"/><line x1="560" y1="30" x2="640" y2="170" stroke="#f0a04b" stroke-width="1.8"/><line x1="640" y1="170" x2="760" y2="210" stroke="#f0a04b" stroke-width="1.8"/><line x1="760" y1="210" x2="800" y2="170" stroke="#f0a04b" stroke-width="1.8"/><circle cx="120" cy="170" r="5" fill="#39d0d8"/><circle cx="200" cy="170" r="5" fill="#39d0d8"/><circle cx="420" cy="170" r="5" fill="#39d0d8"/><circle cx="640" cy="170" r="5" fill="#39d0d8"/><circle cx="800" cy="170" r="5" fill="#39d0d8"/><circle cx="120" cy="120" r="5" fill="#7ee787"/><circle cx="200" cy="120" r="5" fill="#7ee787"/><circle cx="420" cy="120" r="5" fill="#7ee787"/><circle cx="560" cy="120" r="5" fill="#7ee787"/><text x="20" y="175" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#e6edf3">master／main</text><text x="20" y="125" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#7ee787">develop</text><text x="212" y="64" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#f0a04b">feature 分支</text><text x="470" y="24" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#f0a04b">release</text><text x="668" y="204" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#f0a04b">hotfix</text></svg><figcaption>圖 3　Git Flow：長期分支 main／develop，短期分支 feature、release、hotfix 各自合併回對應的長期分支。</figcaption></figure>

- **GitHub Flow**：簡化版——從主分支開功能分支 → 提交 → 發 Pull Request → 審查後合併；適合小型專案與持續部署。
- **GitLab Flow**：結合兩者——環境分支（開發／測試／生產）＋功能分支＋合併請求。

Git Flow 工具：

```
brew install git-flow
git flow init
git flow feature start new-feature
git flow feature finish new-feature
git flow release start 1.0.0
git flow release finish 1.0.0
git flow hotfix start 1.0.1
git flow hotfix finish 1.0.1
```

### 3.2 變基（Rebase）

**概念**：把一個分支的提交「重新套用」到另一個分支之上，產生更整潔的線性歷史。

**與合併的差異**

<figure class="fig-svg"><svg viewBox="0 0 860 220" width="100%" role="img" aria-label="Git merge 與 rebase 的歷史差異：合併 commit 對比線性歷史" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><line x1="40" y1="110" x2="380" y2="110" stroke="#2c6fb1" stroke-width="2"/><circle cx="60" cy="110" r="6" fill="#39d0d8"/><circle cx="120" cy="110" r="6" fill="#39d0d8"/><circle cx="300" cy="110" r="6" fill="#39d0d8"/><circle cx="360" cy="110" r="6" fill="#39d0d8"/><path d="M120 110 Q150 170 210 170 Q260 170 300 116" fill="none" stroke="#7ee787" stroke-width="2"/><circle cx="170" cy="170" r="6" fill="#7ee787"/><circle cx="240" cy="170" r="6" fill="#7ee787"/><polygon points="300,96 312,110 300,124 288,110" fill="#0d1117" stroke="#f0a04b" stroke-width="1.4"/><text x="40" y="44" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3">merge：留下一個合併 commit（菱形）</text><text x="176" y="196" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#7ee787">feature 分支</text><line x1="470" y1="110" x2="820" y2="110" stroke="#2c6fb1" stroke-width="2"/><circle cx="500" cy="110" r="6" fill="#39d0d8"/><circle cx="560" cy="110" r="6" fill="#39d0d8"/><circle cx="620" cy="110" r="6" fill="#39d0d8"/><circle cx="680" cy="110" r="6" fill="#39d0d8"/><circle cx="760" cy="110" r="6" fill="#39d0d8"/><path d="M680 104 Q700 60 742 52" fill="none" stroke="#f0a04b" stroke-width="1.6" stroke-dasharray="5 4"/><circle cx="748" cy="52" r="5" fill="none" stroke="#f0a04b" stroke-width="1.6"/><text x="470" y="44" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3">rebase：歷史攤平成一直線</text><text x="590" y="196" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#f0a04b">原 commit 被重寫（虛線）</text></svg><figcaption>圖　merge 會在兩條歷史交會處留下一個合併 commit（菱形）；rebase 則把分支 commit 重寫到目標分支之後，歷史變成一直線。</figcaption></figure>

- 合併 → 產生合併提交，歷史分叉。
- 變基 → 重新套用提交，歷史呈一直線，不產生合併提交。

```
git rebase branch-name      # 基本變基
git rebase -i branch-name   # 交互式（pick / reword / edit / squash / fixup / drop）
git rebase --continue       # 解決衝突後繼續
git rebase --abort          # 中止變基
```

### 3.3 Cherry-pick 與 Reflog

```
git cherry-pick commit-hash     # 把特定提交套用到當前分支
git reflog                      # 查看引用更新歷史
git reset --hard commit-hash    # 用 reflog 找到的提交恢復
```

### 3.4 標籤、Stash 與 Submodule（進階）

```
git show tag-name                 # 查看標籤資訊

git stash push -m "描述"           # 帶描述保存
git stash apply stash@{0}         # 恢復特定進度

git submodule update --remote     # 同步子模組
git rm path/to/submodule          # 移除子模組（再清 .gitmodules 與 .git/modules）
```

### 3.5 Git Hooks 與 Git LFS

**Hooks**：在特定事件（提交、合併、推送）自動執行的腳本；常用 `pre-commit`、`commit-msg`、`pre-push`。

```
#!/bin/sh
# .git/hooks/pre-commit
echo "Running pre-commit hook"
./run-tests.sh
```

```
chmod +x .git/hooks/pre-commit
```

**Git LFS**（大檔案儲存）：

```
git lfs install
git lfs track "*.psd"
git add .gitattributes
git commit -m "Add Git LFS tracking for PSD files"
```

### 3.6 大型倉庫效能

```
git fetch -j4        # 並行抓取
```

搭配淺克隆、partial clone、定期 `git gc` 等，可降低大型倉庫的操作負擔。
## 4. 遠端協作與程式碼託管平台

### 4.1 GitHub

全球最大的代碼託管平台；提供 Pull Request、Issues、Actions 等協作功能。

1. 建立倉庫：登入 → New repository → 輸入名稱與描述、選公開或私有 → Create repository。
2. 發起 Pull Request：推送功能分支 → New pull request → 選目標與來源分支 → 填描述 → Create。

```
git clone https://github.com/username/repository.git
```

### 4.2 GitLab

功能類似 GitHub，並內建 CI/CD。

1. 建立專案：New project → 設定 → Create project。
2. 發起合併請求（Merge Request）：推送功能分支 → Merge Requests → New merge request → Submit。

```
git clone https://gitlab.com/username/repository.git
```

### 4.3 Bitbucket

Atlassian 平台，支援 Git／Mercurial，可與 Jira、Confluence 整合；以 Pull Request 協作。

```
git clone https://bitbucket.org/username/repository.git
```

### 4.4 Pull Request / Merge Request 流程

1. 在功能分支開發並推送。
2. 發起 PR/MR，指定目標分支。
3. 團隊審查、提出建議。
4. 依意見修改並再推送。
5. 通過後合併到主分支。

## 5. Git 圖形化工具與 IDE 整合

### 5.1 圖形化工具（GUI）

| 工具 | 特點 |
| --- | --- |
| **GitKraken** | 界面簡潔，分支管理、代碼審查、衝突解決 |
| **SourceTree** | Atlassian 出品，Windows／macOS，直觀 |
| **GitHub Desktop** | GitHub 官方，簡單易用 |

操作大同小異：開啟後登入 → Clone 倉庫 → 建立分支 → 提交 → 合併分支。

### 5.2 IDE 內建 Git

- **VS Code**：可安裝 GitLens；命令面板（Ctrl/Cmd+Shift+P）輸入 `Git: Clone`／`Git: Create Branch`／`Git: Merge Branch`。
- **IntelliJ IDEA**：歡迎畫面「Get from Version Control」；版本控制面板可 Branch／Commit／Merge。
- **Eclipse**：安裝 EGit 插件；Import → Git → Projects from Git。
## 6. 安全與最佳實踐

### 6.1 使用者認證

使用 SSH 金鑰或 Token 存取遠端；啟用雙重驗證（2FA）。

### 6.2 保護敏感資訊

避免提交密碼／金鑰；用秘密掃描工具找出外洩：

- **GitGuardian**：即時監控與掃描。
- **TruffleHog**：深度掃描歷史。
- **Gitleaks**：

```
brew install gitleaks
gitleaks detect
```

### 6.3 分支保護

限制對主分支的直接推送與強制推送，強制要求審查與狀態檢查。

- **GitHub**：Settings → Branches → Add rule（Require pull request reviews、Require status checks、Include administrators）。
- **GitLab**：Repository → Branches → Protected branches（No one can force push 等）。

### 6.4 程式碼審查

透過 Pull Request／Merge Request 審查，發現問題、統一風格、共享知識。

### 6.5 提交訊息與版本標籤

- 提交訊息：標題（不超過 50 字）＋正文（說明原因與做法）。
- 標籤：`git tag v1.0.0` → `git push origin v1.0.0`。

### 6.6 備份與保護歷史

```
git clone --mirror /path/to/repository /path/to/backup   # 備份
git clone /path/to/backup /path/to/repository            # 還原
```

並在主分支停用強制推送、設定保護規則。

## 7. 持續整合與持續部署（CI/CD）

### 7.1 概念

- **CI（持續整合）**：頻繁合併到主分支並自動建置與測試，及早發現問題。
- **CD（持續部署／交付）**：通過測試後自動部署到生產／預生產環境。

<figure class="fig-svg"><svg viewBox="0 0 860 200" width="100%" role="img" aria-label="CI/CD 管線：push、安裝依賴、測試、建置、部署與監控" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="95" width="130" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="85" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">git push</text><text x="85" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">推送程式碼</text><rect x="180" y="95" width="150" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="255" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">CI：安裝</text><text x="255" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">pip install -r</text><rect x="360" y="95" width="150" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="435" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">CI：測試</text><text x="435" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">manage.py test</text><rect x="540" y="95" width="130" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="605" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">建置</text><text x="605" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">hexo／容器映像</text><rect x="700" y="95" width="140" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="770" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">部署與監控</text><text x="770" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">Pages／K8s</text><line x1="150" y1="126" x2="176" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="330" y1="126" x2="356" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="510" y1="126" x2="536" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="670" y1="126" x2="696" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="182" y="86" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#f0a04b">失敗即中斷</text></svg><figcaption>圖　CI/CD 管線：push 之後自動安裝依賴、跑測試（失敗即中斷），再建置與部署，最後由監控與日誌接手。</figcaption></figure>

### 7.2 GitHub Actions

```
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: '3.14'
      - run: python -m pip install --upgrade pip && pip install -r requirements.txt
      - run: pytest
```

### 7.3 Jenkins Pipeline

```
pipeline {
    agent any
    stages {
        stage('Build')  { steps { sh 'make build' } }
        stage('Test')   { steps { sh 'make test' } }
        stage('Deploy') { steps { sh 'make deploy' } }
    }
}
```

### 7.4 GitLab CI/CD

```
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script: [make build]
test:
  stage: test
  script: [make test]
deploy:
  stage: deploy
  script: [make deploy]
  only: [main]
```

### 7.5 Travis CI（.travis.yml）

```
language: python
python: ['3.14']
install: [pip install -r requirements.txt]
script: [pytest]
deploy:
  provider: script
  script: bash deploy.sh
  on:
    branch: main
```
## 8. 開源專案與團隊協作

### 8.1 開源專案管理

- **README.md**：專案簡介與使用說明。
- **CONTRIBUTING.md**：貢獻指南（如何回報問題、提交程式碼、參與討論）。
- **LICENSE**：授權條款。

### 8.2 團隊協作

- 分支策略（Git Flow／GitHub Flow／GitLab Flow，見第 3.1 節）。
- 程式碼審查（PR／MR）。
- 以 CI 自動測試把關。

### 8.3 貢獻開源

1. 找有興趣的專案，讀 `README.md`／`CONTRIBUTING.md`。
2. 用 Issue 回報問題（附詳細資訊與重現步驟）。
3. Fork → 開功能分支 → 提交 → 發 PR/MR。
4. 參與討論與程式碼審查。

## 9. Git 在雲端的應用（DevOps）

### 9.1 雲計算概述

- **服務模型**：IaaS（虛擬機／儲存／網路）、PaaS（開發與運行平台）、SaaS（直接使用應用）。
- **部署模型**：公有雲、私有雲、混合雲。

### 9.2 基礎設施即程式碼（IaC）

- 將基礎設施設定檔納入 Git 版控。
- 以 CI/CD 自動部署、減少人工失誤。
- 分環境管理（開發／測試／生產）。
- 變更前經審查與審批。

### 9.3 容器化與編排

**Docker**：把應用打包成容器，用 Dockerfile 定義。

```
FROM python:3.14
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

**Kubernetes**：自動管理容器的部署與擴縮，確保高可用。

```
kubectl apply -f deployment.yaml
```

### 9.4 監控與日誌

**Prometheus + Grafana**：指標監控與視覺化。

```
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
```

**ELK（Elasticsearch + Logstash + Kibana）**：日誌收集與分析。

```
input {
  file { path => "/var/log/myapp.log" start_position => "beginning" }
}
output {
  elasticsearch { hosts => ["localhost:9200"] }
}
```

### 9.5 雲資源管理最佳實踐

- **IaC**：版控、自動化部署、分環境管理、變更審查。
- **容器**：小型化容器、自動擴縮、整合 CI/CD、監控與日誌。
- **安全**：身分驗證與授權、資料加密、安全審計、自動化安全測試。

## 10. 總結

本章從後端開發與 IDE 選擇談起，完整走過 Git：設定、基本操作、分支策略與工作流程、變基與進階操作、遠端協作與平台、GUI 工具與 IDE 整合、安全與最佳實踐、CI/CD，最後延伸到雲端 DevOps（IaC、容器與 K8s、監控與日誌）。掌握這些即可在團隊中建立可靠、可維護的後端開發流程。
