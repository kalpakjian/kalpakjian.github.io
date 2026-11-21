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

### 3.1 分支概念
3.1.1 為什麼使用分支？
分支允許開發者在同一個代碼庫中同時開發多個功能或修復多個問題，而不會互相干擾。每個分支都是代碼庫的一個獨立副本，可以自由地進行修改，最後再合併到主分支中。
#### 3.1.2 分支的優勢

1. 並行開發：多個開發者可以在不同分支上同時工作，提高開發效率。
2. 隔離風險：新功能和修復在獨立的分支上開發，不會影響穩定的主分支。
3. 版本控制：可以輕鬆回溯到某一特定分支的狀態，方便進行版本管理。
4. 簡化代碼審查：分支使得代碼審查變得更加簡單和直觀，可以在合併之前檢查和討論代碼變更。

### 3.2 分支操作
#### 3.2.1 創建分支
創建新分支並切換到該分支：
```
git checkout -b new-branch
```
這個命令等同於以下兩個命令的組合：
```
git branch new-branch
git checkout new-branch
```
#### 3.2.2 切換分支
切換到已存在的分支：
```
git checkout branch-name
```
#### 3.2.3 查看分支
查看本地分支：
```
git branch
```
查看所有分支（包括遠程分支）：
```
git branch -a
```
#### 3.2.4 合併分支
將另一個分支的更改合併到當前分支：
```
git merge branch-name
```
#### 3.2.5 解決合併衝突
在合併過程中，可能會遇到衝突，需要手動解決。解決衝突後，使用 git add 添加解決衝突的文件，然後提交：
```
git add resolved-file
```
git commit -m "解決合併衝突"
### 3.3 分支策略
#### 3.3.1 Feature 分支
Feature 分支是專門用於開發新功能的分支。每個新功能在主分支或開發分支上創建一個新的 feature 分支，完成後再合併回主分支或開發分支。
創建 feature 分支：
```
git checkout -b feature/new-feature
```
合併 feature 分支：
```
git checkout main
git merge feature/new-feature
```
#### 3.3.2 Release 分支
Release 分支用於準備發布新版本。在發布新版本之前，會從開發分支創建一個 release 分支，進行最後的測試和修復。
創建 release 分支：
```
git checkout -b release/1.0.0
```
完成測試和修復後，將 release 分支合併到主分支並創建標籤：
```
git checkout main
git merge release/1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
```
最後，將更改合併回開發分支：
```
git checkout develop
git merge release/1.0.0
```
#### 3.3.3 Hotfix 分支
Hotfix 分支用於修復主分支上的緊急問題。從主分支創建一個 hotfix 分支，完成修復後合併回主分支並創建標籤。
創建 hotfix 分支：
```
git checkout -b hotfix/1.0.1
```
完成修復後，將 hotfix 分支合併到主分支並創建標籤：
```
git checkout main
git merge hotfix/1.0.1
git tag -a v1.0.1 -m "Hotfix version 1.0.1"
```
最後，將更改合併回開發分支：
```
git checkout develop
git merge hotfix/1.0.1
```
### 3.4 分支合併策略
#### 3.4.1 快進合併 (Fast-Forward Merge)
當合併目標分支是當前分支的直接後續版本時，可以使用快進合併。這種合併方式不會創建新的提交，直接將指針移動到目標分支。
```
git merge --ff-only branch-name
```
#### 3.4.2 普通合併 (Three-Way Merge)
當合併分支之間有不同的提交記錄時，需要使用三方合併。這種合併方式會創建一個新的合併提交。
```
git merge branch-name
```
3.4.3 無快進合併 (No Fast-Forward Merge)
即使合併可以使用快進合併，也可以強制創建一個新的合併提交，以保留分支的歷史記錄。
```
git merge --no-ff branch-name
```
### 3.5 分支管理工具
3.5.1 Git Flow
Git Flow 是一種工作流程，定義了明確的分支模型和發布管理方法。使用 Git Flow 可以有效管理大型項目的分支和版本。
安裝 Git Flow :
```
brew install git-flow
```
初始化 Git Flow :
```
git flow init
```
使用 Git Flow 創建和管理分支：
```
git flow feature start new-feature
git flow feature finish new-feature
```
3.5.2 GitHub Flow
GitHub Flow 是一種簡化的工作流程，適用於小型項目和持續部署。GitHub Flow 主要使用以下幾個步驟：

1. 在主分支上工作，所有更改都直接提交到主分支。
2. 當需要開發新功能或修復問題時，創建一個新的 feature 分支。
3. 完成工作後，提交更改並發起 Pull Request。
4. 經過代碼審查後，將 Pull Request 合併到主分支。

3.5.3 GitLab Flow
GitLab Flow 結合了 Git Flow 和 GitHub Flow 的優點，提供了靈活的分支管理策略，適用於各種規模的項目。
GitLab Flow 的主要特點包括：

1. 環境分支：為不同的環境（如開發、測試和生產）創建獨立的分支。
2. 功能分支：每個新功能在主分支上創建一個新的功能分支。
3. 合併請求：完成工作後，提交更改並發起合併請求。

### 3.6 分支實戰案例
#### 3.6.1 團隊協作
在團隊協作中，分支管理是關鍵。下面是一個示例工作流程，展示如何使用分支進行協作：

1. 主分支：主分支用於存儲穩定的代碼，所有發布版本都從主分支創建。
2. 開發分支：開發分支用於日常開發，所有新功能和修復都從開發分支創建。
3. 功能分支：每個新功能在開發分支上創建一個新的功能分支。
4. 合併請求：完成工作後，提交更改並發起合併請求。經過代碼審查後，將功能分支合併到開發分支。
5. 釋出分支：在發布新版本之前，從開發分支創建一個釋出分支。進行最後的測試和修復後，將釋出分支合併到主分支並創建標籤。
6. 熱修復分支：如果發現重大錯誤，從主分支創建一個熱修復分支，修復後合併回主分支和開發分支。

#### 3.6.2 開源項目
在開源項目中，分支管理同樣重要。下面是一個示例工作流程，展示如何在開源項目中使用分支：

1. 主分支：主分支

用於存儲穩定的代碼，所有發布版本都從主分支創建。2. 開發分支：開發分支用於日常開發，所有新功能和修復都從開發分支創建。3. 功能分支：每個貢獻者在開發分支上創建一個新的功能分支，進行開發和測試。4. Pull Request：完成工作後，提交更改並發起 Pull Request。經過代碼審查後，將功能分支合併到開發分支。5. 釋出分支：在發布新版本之前，從開發分支創建一個釋出分支。進行最後的測試和修復後，將釋出分支合併到主分支並創建標籤。6. 熱修復分支：如果發現重大錯誤，從主分支創建一個熱修復分支，修復後合併回主分支和開發分支。
### 3.7 分支管理工具和技術
#### 3.7.1 使用圖形化工具進行分支管理
圖形化工具提供了直觀的界面，幫助用戶進行分支管理。以下是一些常用的圖形化工具：
```
GitKraken
```
GitKraken 是一款流行的 Git 圖形化工具，提供簡潔的界面和強大的功能，幫助用戶進行分支管理和代碼審查。

1. 創建分支：點擊界面中的 "Branch" 按鈕，輸入分支名稱。
2. 切換分支：在分支列表中選擇要切換的分支。
3. 合併分支：選擇要合併的分支，點擊 "Merge" 按鈕。
```
SourceTree
```
SourceTree 是 Atlassian 開發的 Git 圖形化工具，適用於 Windows 和 macOS 平臺。它提供了直觀的界面，幫助用戶進行分支管理和代碼審查。

1. 創建分支：點擊界面中的 "Branch" 按鈕，輸入分支名稱。
2. 切換分支：在分支列表中選擇要切換的分支。
3. 合併分支：選擇要合併的分支，點擊 "Merge" 按鈕。
```
GitHub Desktop
```
GitHub Desktop 是 GitHub 官方提供的圖形化工具，適用於 Windows 和 macOS 平臺。它提供了簡單的界面，幫助用戶進行分支管理和代碼審查。

1. 創建分支：點擊界面中的 "Branch" 按鈕，輸入分支名稱。
2. 切換分支：在分支列表中選擇要切換的分支。
3. 合併分支：選擇要合併的分支，點擊 "Merge" 按鈕。

#### 3.7.2 集成開發環境 (IDE) 的分支管理
許多集成開發環境 (IDE) 內置了 Git 支持，提供了強大的分支管理功能。以下是一些常用的 IDE：
```
Visual Studio Code
```
Visual Studio Code 是一款流行的開源代碼編輯器，內置了 Git 支持。

1. 創建分支：在左側源控制面板中，點擊 "Create Branch" 按鈕，輸入分支名稱。
2. 切換分支：在左側源控制面板中，選擇要切換的分支。
3. 合併分支：在命令面板中輸入 Git: Merge Branch，選擇要合併的分支。
```
IntelliJ IDEA
```
IntelliJ IDEA 是 JetBrains 開發的強大 IDE，內置了 Git 支持。

1. $ \underline{\text{創建分支}} $：在版本控制面板中，點擊 "Branch" 按鈕，選擇 "New Branch"，輸入分支名稱。
2. $ \underline{\text{切換分支}} $：在版本控制面板中，選擇要切換的分支。
3. $ \underline{\text{合併分支}} $：在版本控制面板中，點擊 "Branch" 按鈕，選擇 "Merge"，選擇要合併的分支。
```
Eclipse
```
Eclipse 是一款流行的開源 IDE，通過 EGit 插件提供了 Git 支持。

1. $ \underline{\text{創建分支}} $：在版本控制面板中，右鍵點擊倉庫，選擇 "Switch to" -> "New Branch"，輸入分支名稱。
2. $ \underline{\text{切換分支}} $：在版本控制面板中，右鍵點擊倉庫，選擇 "Switch to" -> "Branch"，選擇要切換的分支。
3. $ \underline{\text{合併分支}} $：在版本控制面板中，右鍵點擊倉庫，選擇 "Merge"，選擇要合併的分支。

### 3.8 分支管理的最佳實踐
#### 3.8.1 保持分支命名規範
分支命名應該簡單明瞭，反映出分支的目的和內容。常見的命名規範包括：

1. 功能分支：feature/功能名稱
2. 修復分支：fix/問題描述
3. 釋出分支：release/版本號
4. 熱修復分支：hotfix/問題描述

#### 3.8.2 定期合併和更新分支
為了避免合併衝突和代碼漂移，應定期將主分支的更改合併到開發分支和功能分支。

1. 合併主分支到開發分支：
```
git checkout develop
git pull origin main
```

2. 合併開發分支到功能分支：
```
git checkout feature/new-feature
git pull origin develop
```
#### 3.8.3 小步提交和頻繁提交
保持小步提交和頻繁提交，有助於追蹤變更歷史，便於代碼審查和問題排查。每次提交應該只包含一個邏輯變更，並附上清晰的提交信息。
#### 3.8.4 代碼審查
在合併分支之前，應進行代碼審查。代碼審查有助於發現潛在問題、提高代碼質量和促進知識共享。常見的代碼審查工具包括 GitHub Pull Request、GitLab Merge Request 和 Bitbucket Pull Request。
#### 3.8.5 自動化測試和持續集成
在合併分支之前，應進行自動化測試，確保代碼質量和穩定性。持續集成（CI）工具可以自動運行測試，並在測試通過後自動部署新版本。常見的 CI 工具包括 Jenkins、Travis CI 和 CircleCI。（時代註記：Travis CI 的免費額度自 2021 年大幅收緊，新專案多改用 GitHub Actions 或 GitLab CI；這一節保留是為了理解概念。）
## 小結
本章介紹了 Git 分支管理的基本概念和操作，包括創建、切換、查看、合併和刪除分支。此外，還介紹了常見的分支策略和合併策略，如 Feature 分支、Release 分支、Hotfix 分支、快進合併和無快進合併等。通過分支管理工具和技術，如 Git Flow、GitHub Flow 和 GitLab Flow，可以有效地管理大型項目的分支和版本。最後，介紹了一些分支管理的最佳實踐，如保持分支命名規範、定期合併和更新分支、小步提交和頻繁提交、代碼審查和自動化測試等。
這些內容幫助你掌握了 Git 分支管理的基本使用方法和常見操作，為進一步深入學習和使用 Git 打下了堅實的基礎。
4：遠程倉庫
### 4.1 遠程倉庫概念
4.1.1 什麼是遠程倉庫？
遠程倉庫是託管在服務器上的 Git 倉庫，允許多名開發者通過網絡進行協作開發。遠程倉庫通常託管在平臺如 GitHub、GitLab 或 Bitbucket 上。
#### 4.1.2 本地倉庫與遠程倉庫的區別
本地倉庫僅存儲在開發者的計算機上，而遠程倉庫則存儲在服務器上，可以被多名開發者訪問。本地倉庫的操作不會影響遠程倉庫，只有在推送更改時，遠程倉庫才會更新。
### 4.2 添加遠程倉庫
#### 4.2.1 添加遠程倉庫
將遠程倉庫添加到本地倉庫：
```
git remote add origin https://github.com/username/repository.git
```
#### 4.2.2 查看遠程倉庫
查看當前本地倉庫中配置的遠程倉庫：
```
git remote -v
```
#### 4.2.3 修改遠程倉庫
修改遠程倉庫的 URL：
```
git remote set-url origin https://newurl.com/username/repository.git
```
#### 4.2.4 刪除遠程倉庫
刪除遠程倉庫：
```
git remote remove origin
```
### 4.3 推送更改到遠程倉庫
#### 4.3.1 推送本地分支到遠程倉庫
將本地分支推送到遠程倉庫：
```
git push origin branch-name
```
#### 4.3.2 推送標籤到遠程倉庫
將本地標籤推送到遠程倉庫：
```
git push origin tag-name
```
一次性推送所有標籤：
```
git push origin --tags
```
#### 4.3.3 強制推送
強制將本地分支推送到遠程倉庫，覆蓋遠程分支：
```
git push origin branch-name --force
```
### 4.4 拉取遠程倉庫的更新
#### 4.4.1 拉取遠程分支
從遠程倉庫拉取最新的更改到本地倉庫：
```
git pull origin branch-name
```
#### 4.4.2 合併與重置
拉取遠程分支並合併到當前分支：
```
git pull origin branch-name
```
拉取遠程分支並重置當前分支：
```
git fetch origin
git reset --hard origin/branch-name
```
### 4.5 同步遠程分支
#### 4.5.1 同步本地和遠程分支列表
同步本地和遠程分支列表：
```
git fetch
```
#### 4.5.2 跟蹤遠程分支
創建一個跟蹤遠程分支的新分支：
```
git checkout -b local-branch-name origin/remote-branch-name
```
設置現有的本地分支跟蹤遠程分支：
```
git branch --set-upstream-to=origin/remote-branch-name local-branch-name
```
### 4.6 遠程操作的高級選項
#### 4.6.1 分支重命名
重命名遠程分支：

1. 重命名本地分支：
```
git branch -m old-branch-name new-branch-name
```

2. 刪除遠程分支：
```
git push origin --delete old-branch-name
```

3. 推送重命名後的本地分支：
```
git push origin new-branch-name
```

4. 將新分支設置為跟蹤遠程分支：
```
git branch --set-upstream-to=origin/new-branch-name new-branch-name
```
#### 4.6.2 清理遠程分支
刪除已經合併到主分支的遠程分支：

1. 列出所有分支及其合併狀態：
```
git branch -r --merged
```

2. 刪除已合併的遠程分支：
```
git push origin --delete branch-name
```
#### 4.6.3 從遠程倉庫檢查出特定提交
從遠程倉庫檢查出特定提交：
```
git fetch origin
git checkout commit-hash
```
### 4.7 遠程倉庫的協作工作流程
#### 4.7.1 Fork 工作流程
Fork 工作流程是一種常見的開源項目協作方式。每個貢獻者都會從主倉庫 fork 一個副本，進行修改後，通過 Pull Request 將更改提交回主倉庫。

1. Fork：從主倉庫 fork 一個副本到自己的帳戶。
2. 克隆：將 fork 的倉庫克隆到本地：
```
git clone https://github.com/your-username/repository.git
```

3. 添加遠程倉庫：將主倉庫添加為遠程倉庫：
```
git remote add upstream https://github.com/original-owner/repository.git
```

4. 同步更新：從主倉庫拉取最新更新：
```
git fetch upstream
git merge upstream/main
```

5. 推送更改：將修改推送到自己的遠程倉庫：
```
git push origin branch-name
```

6. 發起 Pull Request：在 GitHub 上發起 Pull Request，請求將更改合併到主倉庫。

#### 4.7.2 Pull Request 工作流程
Pull Request 工作流程適用於團隊協作和開源項目。開發者在功能分支上進行開發，完成後發起 Pull Request，請求將更改合併到主分支。

1. 創建功能分支：從主分支創建功能分支：
```
git checkout -b feature/new-feature
```

2. 進行開發：在功能分支上進行開發並提交更改。
3. 推送功能分支：將功能分支推送到遠程倉庫：
```
git push origin feature/new-feature
```

4. 發起 Pull Request：在平臺上發起 Pull Request，請求將更改合併到主分支。
5. 代碼審查：團隊成員對 Pull Request 進行代碼審查，提出意見和建議。
6. 合併 Pull Request：代碼審查通過後，將 Pull Request 合併到主分支。

### 4.8 遠程倉庫的安全性
#### 4.8.1 設置 SSH 鑰匙
使用 SSH 鑰匙進行身份驗證，提高遠程倉庫的安全性。

1. 生成 SSH 鑰匙：
```
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"
```

2. 添加 SSH 鑰匙到代理：
```
eval "${ssh-agent -s}"
ssh-add ~/.ssh/id_rsa
```

3. 將公鑰添加到 GitHub：在 GitHub 上，打開設定頁面，選擇 "SSH and GPG keys"，點擊 "New SSH key"，將公鑰添加到 GitHub。

#### 4.8.2 設置雙重驗證
啟用雙重驗證，提高帳戶的安全性。

1. 開啟雙重驗證：在 GitHub 上，打開設定頁面，選擇 "Security" -> "Two-factor authentication"，根據提示設置雙重驗證。
2. 使用應用程序驗證碼：下載並安裝雙重驗證應用程序，如 Google Authenticator，掃描二維碼並輸入驗證碼。

### 4.9 遠程倉庫的最佳實踐
#### 4.9.1 定期同步遠程倉庫
定期從遠程倉庫拉取更新，保持本地倉庫與遠程倉庫同步，避免合併衝突。
```
git fetch upstream
git merge upstream/main
```
#### 4.9.2 使用 Pull Request 進行代碼審查
使用 Pull Request 進行代碼審查，確保代碼質量和一致性。代碼審查有助於發現潛在問題、提高代碼質量和促進知識共享。
#### 4.9.3 保持分支命名規範
分支命名應該簡單明瞭，反映出分支的目的和內容。常見的命名規範包括：

1. 功能分支：feature/功能名稱
2. 修復分支：fix/問題描述
3. 釋出分支：release/版本號
4. 熱修復分支：hotfix/問題描述

#### 4.9.4 使用標籤管理版本
使用標籤來標記項目的重要里程碑，如發布新版本。標籤有助於回溯歷史版本，便於版本管理。
創建標籤
```
git tag v1.0.0
```
推送標籤到遠程倉庫
```
git push origin v1.0.0
```
#### 4.9.5 保護分支
在遠程倉庫上保護主分支，限制對主分支的直接推送，確保代碼的穩定性和安全性。可以設置代碼審查、強制拉取最新更新等策略。
## 小結
本章介紹了遠程倉庫的基本概念和操作，包括添加、修改、刪除遠程倉庫，推送和拉取更改，同步遠程分支，以及遠程倉庫的協作工作流程。此外，還介紹了遠程倉庫的安全性設置和最佳實踐，如設置 SSH 鑰匙、雙重驗證、定期同步、使用 Pull Request 進行代碼審查、保持分支命名規範、使用標籤管理版本和保護分支等。這些內容幫助你掌握了遠程倉庫的基本使用方法和常見操作，為進一步深入學習和使用 Git 打下了堅實的基礎。
5: Git 進階操作
### 5.1 變基 (Rebase)
#### 5.1.1 變基的概念
變基 (Rebase) 是 Git 中的一種操作，用於將一個分支的更改重新應用到另一個分支之上。變基的主要目的是為了產生更加整潔、線性的提交歷史。
#### 5.1.2 變基與合併的區別

<figure class="fig-svg"><svg viewBox="0 0 860 220" width="100%" role="img" aria-label="Git merge 與 rebase 的歷史差異：合併 commit 對比線性歷史" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><line x1="40" y1="110" x2="380" y2="110" stroke="#2c6fb1" stroke-width="2"/><circle cx="60" cy="110" r="6" fill="#39d0d8"/><circle cx="120" cy="110" r="6" fill="#39d0d8"/><circle cx="300" cy="110" r="6" fill="#39d0d8"/><circle cx="360" cy="110" r="6" fill="#39d0d8"/><path d="M120 110 Q150 170 210 170 Q260 170 300 116" fill="none" stroke="#7ee787" stroke-width="2"/><circle cx="170" cy="170" r="6" fill="#7ee787"/><circle cx="240" cy="170" r="6" fill="#7ee787"/><polygon points="300,96 312,110 300,124 288,110" fill="#0d1117" stroke="#f0a04b" stroke-width="1.4"/><text x="40" y="44" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3">merge：留下一個合併 commit（菱形）</text><text x="176" y="196" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#7ee787">feature 分支</text><line x1="470" y1="110" x2="820" y2="110" stroke="#2c6fb1" stroke-width="2"/><circle cx="500" cy="110" r="6" fill="#39d0d8"/><circle cx="560" cy="110" r="6" fill="#39d0d8"/><circle cx="620" cy="110" r="6" fill="#39d0d8"/><circle cx="680" cy="110" r="6" fill="#39d0d8"/><circle cx="760" cy="110" r="6" fill="#39d0d8"/><path d="M680 104 Q700 60 742 52" fill="none" stroke="#f0a04b" stroke-width="1.6" stroke-dasharray="5 4"/><circle cx="748" cy="52" r="5" fill="none" stroke="#f0a04b" stroke-width="1.6"/><text x="470" y="44" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3">rebase：歷史攤平成一直線</text><text x="590" y="196" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#f0a04b">原 commit 被重寫（虛線）</text></svg><figcaption>圖　merge 會在兩條歷史交會處留下一個合併 commit（菱形）；rebase 則把分支 commit 重寫到目標分支之後，歷史變成一直線。</figcaption></figure>
變基和合併都是將一個分支的更改應用到另一個分支上，但它們的工作方式不同：

- 合併會創建一個新的合併提交，將兩個分支的歷史合併在一起，這樣提交歷史會呈現分叉狀態。
- 變基則會將一個分支的提交在另一個分支上重新應用，創建一個新的直線型歷史，不會創建合併提交。

#### 5.1.3 使用變基
基本變基操作
將當前分支變基到另一個分支上：
```
git rebase branch-name
```
交互式變基
交互式變基允許用戶在變基過程中對提交進行編輯、合併或重新排序：
```
git rebase -i branch-name
```
在交互式界面中，可以使用以下命令：

- pick：保留該提交
- reword：編輯該提交信息
- edit：暫停變基，以便編輯該提交
- squash：將該提交與前一個提交合併
- fixup：類似 squash，但不保留該提交信息
- drop：丟棄該提交

## 解決變基衝突
在變基過程中，如果遇到衝突，需要手動解決。解決衝突後，使用 git rebase --continue 繼續變基過程：
```
git rebase --continue
```
如果需要中止變基過程，可以使用 git rebase --abort：
```
git rebase --abort
```
### 5.2 標籤 (Tags)
#### 5.2.1 標籤的用途
標籤 (Tag) 用於標記特定的提交點，通常用於標記版本發布點。標籤可以分為輕量標籤 (Lightweight Tag) 和註釋標籤 (Annotated Tag)。
#### 5.2.2 創建輕量標籤
輕量標籤是一個指向特定提交的簡單標籤，不包含額外的元數據：
```
git tag tag-name
```
#### 5.2.3 創建註釋標籤
註釋標籤是一個包含附加信息（如創建者、日期、註釋等）的標籤：
git tag -a tag-name -m "標籤描述"
#### 5.2.4 查看標籤
查看所有標籤：
```
git tag
```
查看特定標籤的信息：
```
git show tag-name
```
#### 5.2.5 刪除標籤
刪除本地標籤：
```
git tag -d tag-name
```
刪除遠程標籤：
```
git push origin :refs/tags/tag-name
```
#### 5.2.6 推送標籤到遠程倉庫
將本地標籤推送到遠程倉庫：
```
git push origin tag-name
```
一次性推送所有標籤：
```
git push origin --tags
```
5.3 Stash
#### 5.3.1 Stash 的概念
Stash 用於暫存當前的工作進度，以便切換到其他分支或進行其他操作後能夠恢復這些進度。這在需要切換分支但不希望提交未完成的工作時特別有用。
#### 5.3.2 保存工作進度
使用 git stash 保存當前的工作進度：
```
git stash
```
使用描述信息保存工作進度：
git stash push -m "描述信息"
#### 5.3.3 查看 Stash 列表
查看已保存的工作進度列表：
```
git stash list
```
#### 5.3.4 恢復工作進度
恢復最近一次保存的工作進度：
```
git stash apply
```
恢復並刪除最近一次保存的工作進度：
```
git stash pop
```
恢復特定的工作進度：
```
git stash apply stash@{0}
```
#### 5.3.5 刪除 Stash
刪除指定的工作進度：
```
git stash drop stash@{0}
```
刪除所有保存的工作進度：
```
git stash clear
```
5.4 Submodule
#### 5.4.1 Submodule 的概念
Submodule 是 Git 倉庫中的子倉庫，用於包含和管理外部依賴。每個 Submodule 都是獨立的 Git 倉庫，可以單獨進行克隆、提交和推送操作。
#### 5.4.2 添加 Submodule
在主倉庫中添加 Submodule：
```
git submodule add https://github.com/username/submodule-repo.git path/to/submodule
```
#### 5.4.3 初始化和更新 Submodule
克隆倉庫後，初始化和更新 Submodule：
```
git submodule init
git submodule update
```
#### 5.4.4 同步 Submodule
更新所有 Submodule 以匹配主倉庫中的配置：
```
git submodule update --remote
```
#### 5.4.5 移除 Submodule

1. 刪除 Submodule 目錄：
```
git rm path/to/submodule
```

2. 刪除 .gitmodules 文件中的相應條目：
```
sed -i '/path/vto/submodule/d'.gitmodules
```

3. 刪除 .git/config 文件中的相應條目：
```
sed -i '/path/vto/submodule/d'.git/config
```

4. 刪除 Submodule 的 Git 目錄：
```
rm -rf .git/modules/path/to/submodule
```
5.5 Cherry-pick
#### 5.5.1 Cherry-pick 的概念
Cherry-pick 是 Git 中的一個操作，用於將特定的提交應用到當前分支。這在需要從一個分支中提取單個提交並應用到另一個分支時特別有用。
#### 5.5.2 使用 Cherry-pick
將特定提交應用到當前分支：
```
git cherry-pick commit-hash
```
5.6 Reflog
#### 5.6.1 Reflog 的概念
Reflog 是 Git 中的一個機制，用於記錄倉庫的所有引用更新歷史。通過 Reflog，可以查看和恢復任何引用的歷史狀態。
#### 5.6.2 查看 Reflog
查看引用更新歷史：
```
git reflog
```
#### 5.6.3 使用 Reflog 恢復提交
使用 Reflog 恢復到特定的提交：
```
git reset --hard commit-hash
```
5.7 Git Hooks
#### 5.7.1 Git Hooks 的概念
Git Hooks 是在特定事件發生時自動執行的腳本。這些事件包括提交、合併、推送等。通過 Git Hooks，可以在這些事件發生時自動執行自定義操作。
#### 5.7.2 常見的 Git Hooks

- pre-commit：在提交之前執行，可以用於代碼檢查和測試。
- commit-msg：在提交信息編輯之後執行，可以用於驗證提交信息格式。
- pre-push：在推送之前執行，可以用於最終的代碼檢查和測試。

#### 5.7.3 配置 Git Hooks
在倉庫的 .git/hooks 目錄中創建 Hook 腳本。例如，創建一個 pre-commit Hook：
```
#!/bin/sh
# pre-commit hook example
echo "Running pre-commit hook"
./run-tests.sh
```
給腳
本添加可執行權限：
```
chmod +x .git/hooks/pre-commit
```
### 5.8 Git 大文件存儲 (Git LFS)
#### 5.8.1 Git LFS 的概念
Git LFS (Large File Storage) 是 Git 的一個擴展，用於管理和存儲大文件。通過 Git LFS，可以將大文件的存儲和版本控制交給專門的 LFS 服務器，減少 Git 倉庫的大小和壓力。
#### 5.8.2 安裝 Git LFS
安裝 Git LFS :
```
git lfs install
```
#### 5.8.3 跟蹤大文件
使用 Git LFS 跟蹤特定類型的大文件：
```
git lfs track "*.psd"
```
將 .gitattributes 文件添加到倉庫：
```
git add .gitattributes
git commit -m "Add Git LFS tracking for PSD files"
```
#### 5.8.4 推送和拉取大文件
Git LFS 會自動處理大文件的推送和拉取操作，與普通的 Git 文件操作一致。
### 5.9 Git 工作流程
#### 5.9.1 Git Flow 工作流程
Git Flow 是一種複雜的工作流程，適用於大型項目，具有嚴格的分支管理策略。

1. 使用主分支 (master) 和開發分支 (develop)。（時代註記：GitHub 自 2020 年起新倉庫預設分支名為 `main`，原理相同。）
2. 每個新功能在 develop 分支上創建一個 feature 分支。
3. 完成功能後，將 feature 分支合併回 develop 分支。
4. 釋出新版本時，從 develop 分支創建一個 release 分支，進行最後的測試和修復。
5. 確認 release 分支穩定後，合併到 master 分支，並創建一個標籤。
6. 如果發現重大錯誤，從 master 分支創建 hotfix 分支，修復後合併回 master 和 develop 分支。

#### 5.9.2 GitHub Flow 工作流程
GitHub Flow 是一種簡化的工作流程，適用於小型項目和持續部署。

1. 在主分支上工作，所有更改都直接提交到主分支。
2. 當需要開發新功能或修復問題時，創建一個新的 feature 分支。
3. 完成工作後，提交更改並發起 Pull Request。
4. 經過代碼審查後，將 Pull Request 合併到主分支。

#### 5.9.3 GitLab Flow 工作流程
GitLab Flow 結合了 Git Flow 和 GitHub Flow 的優點，提供了靈活的分支管理策略，適用於各種規模的項目。

1. 環境分支：為不同的環境（如開發、測試和生產）創建獨立的分支。
2. 功能分支：每個新功能在主分支上創建一個新的功能分支。
3. 合併請求：完成工作後，提交更改並發起合併請求。

### 5.10 Git 進階技巧
#### 5.10.1 使用 Git Alias
Git Alias 是 Git 的別名功能，可以用來簡化命令。
配置 Alias
在 .gitconfig 文件中添加以下內容：
```
[alias]
st = status
co = checkout
ci = commit
br = branch
lg = log --oneline --graph --decorate --all
```
使用別名命令
```
git st
git co branch-name
```
git ci -m "提交信息"
#### 5.10.2 使用 Reflog 恢復丟失的提交
通過 Reflog，可以恢復丟失的提交或分支。
查看引用更新歷史：
```
git reflog
```
恢復到特定的提交：
```
git reset --hard commit-hash
```
## 小結
本章介紹了 Git 的進階操作，包括變基、標籤、Stash、Submodule、Cherry-pick、Reflog、Git Hooks、Git LFS 等。這些進階操作和技巧可以幫助你更加靈活和高效地使用 Git 進行版本控制和項目管理。此外，還介紹了常見的 Git 工作流程，如 Git Flow、GitHub Flow 和 GitLab Flow，這些工作流程可以幫助你在團隊協作中更好地管理分支和版本。最後，介紹了一些 Git 的進階技巧，如使用 Git Alias 和 Reflog 恢復丟失的提交，這些技巧可以讓你更加高效地使用 Git。
6: Git 與工作流程
### 6.1 Git 工作流程概述
6.1.1 什麼是 Git 工作流程？
Git 工作流程是一套使用 Git 進行軟件開發的策略和規則，幫助團隊更有效地協作和管理代碼。不同的工作流程適合不同類型和規模的項目。
6.1.2 為什麼需要 Git 工作流程？
Git 工作流程有助於：

1. 協作開發：允許多名開發者同時對項目進行修改，並有效管理和合併這些修改。
2. 版本控制：管理不同版本的代碼，允許開發者回溯到以前的版本。
3. 代碼質量：通過代碼審查、測試和持續集成，確保代碼質量。
4. 高效管理：提供清晰的分支結構和操作規範，提高工作效率。

### 6.2 Git Flow 工作流程
#### 6.2.1 Git Flow 概述
Git Flow 是由 Vincent Driessen 提出的工作流程，適用於大型項目，具有嚴格的分支管理策略。它使用了多個長期分支和短期分支來管理代碼。
#### 6.2.2 Git Flow 的分支模型

<figure class="fig-svg"><svg viewBox="0 0 860 250" width="100%" role="img" aria-label="Git Flow 分支模型：main、develop、feature、release、hotfix" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><line x1="150" y1="170" x2="820" y2="170" stroke="#2c6fb1" stroke-width="2"/><line x1="150" y1="120" x2="820" y2="120" stroke="#39d0d8" stroke-width="2"/><line x1="200" y1="120" x2="330" y2="70" stroke="#f0a04b" stroke-width="1.8"/><line x1="330" y1="70" x2="420" y2="120" stroke="#f0a04b" stroke-width="1.8"/><line x1="450" y1="120" x2="560" y2="30" stroke="#f0a04b" stroke-width="1.8"/><line x1="560" y1="30" x2="640" y2="170" stroke="#f0a04b" stroke-width="1.8"/><line x1="640" y1="170" x2="760" y2="210" stroke="#f0a04b" stroke-width="1.8"/><line x1="760" y1="210" x2="800" y2="170" stroke="#f0a04b" stroke-width="1.8"/><circle cx="120" cy="170" r="5" fill="#39d0d8"/><circle cx="200" cy="170" r="5" fill="#39d0d8"/><circle cx="420" cy="170" r="5" fill="#39d0d8"/><circle cx="640" cy="170" r="5" fill="#39d0d8"/><circle cx="800" cy="170" r="5" fill="#39d0d8"/><circle cx="120" cy="120" r="5" fill="#7ee787"/><circle cx="200" cy="120" r="5" fill="#7ee787"/><circle cx="420" cy="120" r="5" fill="#7ee787"/><circle cx="560" cy="120" r="5" fill="#7ee787"/><text x="20" y="175" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#e6edf3">master／main</text><text x="20" y="125" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#7ee787">develop</text><text x="212" y="64" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#f0a04b">feature 分支</text><text x="470" y="24" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#f0a04b">release</text><text x="668" y="204" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#f0a04b">hotfix</text></svg><figcaption>圖 3　Git Flow：長期分支 main／develop，短期分支 feature、release、hotfix 各自合併回對應的長期分支。</figcaption></figure>

1. 主分支 (master)：存儲穩定的發布版本，每次發布新版本都會在主分支上創建一個標籤。
2. 開發分支 (develop)：用於進行日常開發，所有新功能和修復都在此分支上進行。
3. 功能分支 (feature)：每個新功能在開發分支上創建一個新的功能分支，完成功能後合併回開發分支。
4. 釋出分支 (release)：在發布新版本之前，從開發分支創建一個釋出分支，進行最後的測試和修復。
5. 熱修復分支 (hotfix)：如果發現重大錯誤，從主分支創建一個熱修復分支，修復後合併回主分支和開發分支。

#### 6.2.3 Git Flow 的工作流程

1. 初始化 Git Flow :
```
git flow init
```

2. 創建功能分支：
```
git flow feature start new-feature
```

3. 完成功能後合併回開發分支：
```
git flow feature finish new-feature
```

4. 創建釋出分支：
```
git flow release start 1.0.0
```

5. 完成測試和修復後合併到主分支並創建標籤：
```
git flow release finish 1.0.0
```

6. 創建熱修復分支：
```
git flow hotfix start 1.0.1
```

7. 完成修復後合併回主分支和開發分支：
```
git flow hotfix finish 1.0.1
```
### 6.3 GitHub Flow 工作流程
#### 6.3.1 GitHub Flow 概述
GitHub Flow 是一種簡化的工作流程，適用於小型項目和持續部署。它強調了簡單性和靈活性，主要使用一個主分支和短期功能分支。
#### 6.3.2 GitHub Flow 的分支模型

1. 主分支（main）：存儲最新的穩定版本，所有變更都直接或間接合併到主分支。
2. 功能分支（feature）：每個新功能或修復在主分支上創建一個新的功能分支，完成後發起 Pull Request。

#### 6.3.3 GitHub Flow 的工作流程

1. 創建功能分支：
```
git checkout -b new-feature
```

2. 提交更改：
```
git add.
```
git commit -m "描述你的更改"

3. 推送功能分支到遠程倉庫：
```
git push origin new-feature
```

4. 發起 Pull Request：在 GitHub 上發起 Pull Request，請求將更改合併到主分支。
5. 代碼審查：團隊成員對 Pull Request 進行代碼審查，提出意見和建議。
6. 合併 Pull Request：代碼審查通過後，將 Pull Request 合併到主分支。
7. 刪除功能分支：
```
git branch -d new-feature
git push origin --delete new-feature
```
### 6.4 GitLab Flow 工作流程
#### 6.4.1 GitLab Flow 概述
GitLab Flow 結合了 Git Flow 和 GitHub Flow 的優點，提供了靈活的分支管理策略，適用於各種規模的項目。它強調了簡單性和持續部署。
#### 6.4.2 GitLab Flow 的分支模型

1. 環境分支：為不同的環境（如開發、測試和生產）創建獨立的分支。
2. 功能分支 (feature)：每個新功能在主分支上創建一個新的功能分支。
3. 合併請求 (Merge Request)：完成工作後，提交更改並發起合併請求。

#### 6.4.3 GitLab Flow 的工作流程

1. 創建功能分支：
```
git checkout -b feature/new-feature
```

2. 提交更改：
```
git add.
```
git commit -m "描述你的更改"

3. 推送功能分支到遠程倉庫：
```
git push origin feature/new-feature
```

4. 發起合併請求：在 GitLab 上發起合併請求，請求將更改合併到目標分支（如開發分支或主分支）。
5. 代碼審查：團隊成員對合併請求進行代碼審查，提出意見和建議。
6. 合併合併請求：代碼審查通過後，將合併請求合併到目標分支。
7. 刪除功能分支：
```
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```
### 6.5 持續集成與持續部署 (CI/CD)
#### 6.5.1 持續集成 (CI)
持續集成 (CI) 是一種軟件開發實踐，開發者頻繁地將代碼更改合併到主分支，每次合併後自動進行構建和測試。CI 的目的是早期發現和修復問題，確保代碼庫始終保持在一個可工作的狀態。
#### 6.5.2 持續部署 (CD)
持續部署 (CD) 是一種軟件發布實踐，將每次通過 CI 測試的代碼更改自動部署到生產環境。CD 的目的是自動化發布過程，確保代碼可以快速、安全地交付給用戶。
#### 6.5.3 使用 Git 進行 CI/CD
配置 CI/CD 工具
選擇並配置 CI/CD 工具，如 Jenkins、Travis CI 或 GitLab CI/CD。
Jenkins 配置示例

1. 安裝 Jenkins 和必要的插件。
2. 創建新的 Jenkins 任務，選擇 “Pipeline”。
3. 配置 Pipeline 腳本：
```
pipeline {
agent any
stages {
stage('Build') {
steps {
sh 'make build'
}
stage('Test') {
steps {
sh 'make test'
}
}
stage('Deploy') {
steps {
sh 'make deploy'
}
}
```
Travis CI 配置示例

1. 創建 .travis.yml 文件：
```
language: python
python:
```

- "3.14"
```
install:
```

- pip install -r requirements.txt
```
script:
```

- pytest
```
deploy:
provider: script
script: bash deploy.sh
on:
branch: main
```
GitLab CI/CD 配置示例

1. 創建 .gitlab-ci.yml 文件：
```
stages:
```

- build
- test
- deploy
```
build:
stage: build
script:
```

- make build
```
test:
stage:
test
script:
```

- make test
```
deploy:
stage: deploy
script:
```

- make deploy
```
only:
```

- main

### 6.6 工作流程的最佳實踐
#### 6.6.1 代碼審查
代碼審查是確保代碼質量和一致性的重要環節。通過 Pull Request 或 Merge Request，團隊成員可以對代碼進行審查，發現潛在問題，提出改進建議。
#### 6.6.2 自動化測試
自動化測試是 CI/CD 的核心部分。編寫單元測試、集成測試和端到端測試，確保每次代碼更改不會引人新問題。
#### 6.6.3 持續交付
持續交付是持續部署的前提，確保每次代碼更改都可以自動部署到預生產環境，進行最後的驗證和測試。
#### 6.6.4 文檔和通信
良好的文檔和溝通是成功協作的關鍵。確保每個開發者都清楚工作流程、分支策略和CI/CD 配置。
## 小結
本章介紹了常見的 Git 工作流程，包括 Git Flow、GitHub Flow 和 GitLab Flow。這些工作流程提供了不同的分支管理策略和操作規範，適用於不同規模和類型的項目。此外，還介紹了持續集成與持續部署（CI/CD）的概念和配置方法，這些實踐可以幫助團隊提高開發效率和代碼質量。最後，介紹了一些工作流程的最佳實踐，如代碼審查、自動化測試、持續交付和良好的文檔與通信。
7: Git 工具與整合
### 7.1 圖形化工具
圖形化工具提供了直觀的界面，幫助用戶更輕鬆地進行 Git 操作。以下是一些常用的圖形化工具。
7.1.1 GitKraken
GitKraken 是一款流行的 Git 圖形化工具，提供簡潔的界面和強大的功能，幫助用戶進行分支管理、代碼審查和衝突解決。
安裝 GitKraken

1. 訪問 GitKraken 官網，下載並安裝適用於你操作系統的版本。
2. 安裝完成後，打開 GitKraken 並登入你的 GitHub、GitLab 或 Bitbucket 帳戶。

## 使用 GitKraken

1. 克隆倉庫：在主界面中，點擊 "Clone a repo" 按鈕，輸入倉庫的 URL 和本地保存路徑。
2. 創建分支：在左側分支列表中，右鍵點擊當前分支，選擇 "Create branch" 並輸入分支名稱。
3. 提交更改：在左側文件列表中，選擇修改的文件，輸入提交信息，點擊 "Commit changes"。
4. 合併分支：在左側分支列表中，拖動目標分支到當前分支，選擇 "Merge branch into current branch"。

7.1.2 SourceTree
SourceTree 是 Atlassian 開發的 Git 圖形化工具，適用於 Windows 和 macOS 平臺。它提供了直觀的界面，幫助用戶進行分支管理和代碼審查。
安裝 SourceTree

1. 訪問 SourceTree 宣網，下載並安裝適用於你操作系統的版本。
2. 安裝完成後，打開 SourceTree 並登入你的 Atlassian 帳戶。

## 使用 SourceTree

1. 克隆倉庫：在主界面中，點擊 "Clone" 按鈕，輸入倉庫的 URL 和本地保存路徑。
2. 創建分支：在分支列表中，右鍵點擊當前分支，選擇 "New Branch" 並輸入分支名稱。
3. 提交更改：在文件列表中，選擇修改的文件，輸入提交信息，點擊 "Commit" 按鈕。
4. 合併分支：在分支列表中，右鍵點擊目標分支，選擇 "Merge" 並選擇當前分支。

7.1.3 GitHub Desktop
GitHub Desktop 是 GitHub 官方提供的圖形化工具，適用於 Windows 和 macOS 平臺。它提供了簡單的界面，幫助用戶進行分支管理和代碼審查。
## 安裝 GitHub Desktop

1. 訪問 GitHub Desktop 官網，下載並安裝適用於你操作系統的版本。
2. 安裝完成後，打開 GitHub Desktop 並登入你的 GitHub 帳戶。

## 使用 GitHub Desktop

1. 克隆倉庫：在主界面中，點擊 "Clone a repository from the Internet" 按鈕，輸入倉庫的 URL 和本地保存路徑。
2. 創建分支：在右上角的分支選擇器中，選擇 "New branch" 並輸入分支名稱。
3. 提交更改：在文件列表中，選擇修改的文件，輸入提交信息，點擊 "Commit to main" 按鈕。
4. 合併分支：在右上角的分支選擇器中，選擇 "Choose a branch to merge into main"，選擇目標分支並點擊 "Merge".

### 7.2 集成開發環境 (IDE)
許多集成開發環境 (IDE) 內置了 Git 支持，提供了強大的分支管理和代碼審查功能。以下是一些常用的 IDE。
7.2.1 Visual Studio Code
Visual Studio Code 是一款流行的開源代碼編輯器，內置了 Git 支持。
安裝 Git 插件

1. 打開 Visual Studio Code。
2. 點擊左側的擴展圖標，搜索 "Git" 並安裝 "GitLens" 插件。

## 使用 Git 功能

1. 克隆倉庫：打開命令面板（Ctrl+Shift+P 或 Cmd+Shift+P），輸入 Git: Clone，輸入倉庫的 URL 和本地保存路徑。
2. 創建分支：打開命令面板，輸入 Git: Create Branch 並輸入分支名稱。
3. 提交更改：在左側源控制面板中，選擇修改的文件，輸入提交信息，點擊 "Commit" 按鈕。
4. 合併分支：打開命令面板，輸入 Git: Merge Branch，選擇目標分支。

7.2.2 IntelliJ IDEA
IntelliJ IDEA 是 JetBrains 開發的強大 IDE，內置了 Git 支持。
## 使用 Git 功能

1. 克隆倉庫：在歡迎界面中，點擊 "Get from Version Control"，輸入倉庫的 URL 和本地保存路徑。
2. 創建分支：在版本控制面板中，點擊 "Branch" 按鈕，選擇 "New Branch" 並輸入分支名稱。
3. 提交更改：在版本控制面板中，選擇修改的文件，輸入提交信息，點擊 "Commit" 按鈕。
4. 合併分支：在版本控制面板中，點擊 "Branch" 按鈕，選擇 "Merge" 並選擇目標分支。

7.2.3 Eclipse
Eclipse 是一款流行的開源 IDE，通過 EGit 插件提供了 Git 支持。
安裝 EGit 插件

1. 打開 Eclipse。
2. 點擊 "Help" 菜單，選擇 "Eclipse Marketplace"。
3. 搜索 "EGit" 並安裝插件。

## 使用 Git 功能

1. 克隆倉庫：在 "File" 菜單中，選擇 "Import" -> "Git" -> "Projects from Git"，輸入倉庫的 URL 和本地保存路徑。
2. 創建分支：在版本控制面板中，右鍵點擊倉庫，選擇 "Switch to" -> "New Branch" 並輸入分支名稱。
3. 提交更改：在版本控制面板中，選擇修改的文件，輸入提交信息，點擊 "Commit" 按鈕。
4. 合併分支：在版本控制面板中，右鍵點擊倉庫，選擇 "Merge"，選擇目標分支。

### 7.3 代碼託管平臺
代碼託管平臺提供了基於 Git 的版本控制服務，幫助開發者更好地協同工作。以下是一些常用的代碼託管平臺。
7.3.1 GitHub
GitHub 是世界上最大的代碼託管平臺，提供基於 Git 的版本控制服務。GitHub 還提供許多協作功能，如 Pull Request、Issues 和 Actions 等。
創建 GitHub 倉庫

1. 登錄 GitHub 帳戶。
2. 點擊 “New repository” 按鈕。
3. 輸入倉庫名稱和描述，選擇公開或私有。
4. 點擊 “Create repository” 按鈕創建倉庫。

克隆 GitHub 倉庫
從 GitHub 克隆倉庫到本地：
```
git clone https://github.com/username/repository.git
```
發起 Pull Request

1. 提交更改並推送到功能分支。
2. 打開 GitHub 倉庫頁面，點擊 “New pull request” 按鈕。
3. 選擇目標分支和功能分支，點擊 “Create pull request” 按鈕。
4. 輸入描述信息，點擊 “Create pull request” 按鈕。

7.3.2 GitLab
GitLab 是另一個流行的代碼託管平臺，提供類似 GitHub 的功能。GitLab 還具有內置的持續集成和持續部署（CI/CD）功能，使得開發、測試和部署流程更加自動化和高效。
創建 GitLab 倉庫

1. 登錄 GitLab 帳戶。
2. 點擊 “New project” 按鈕。
3. 輸入項目名稱和描述，選擇公開或私有。
4. 點擊 “Create project” 按鈕創建項目。

克隆 GitLab 倉庫
從 GitLab 克隆倉庫到本地：
```
git clone https://gitlab.com/username/repository.git
```
發起合併請求

1. 提交更改並推送到功能分支。
2. 打開 GitLab 倉庫頁面，點擊 “Merge Requests” 按鈕。
3. 點擊 “New merge request” 按鈕，選擇目標分支和功能分支。
4. 輸入描述信息，點擊 “Submit merge request” 按鈕。

7.3.3 Bitbucket
Bitbucket 是 Atlassian 提供的代碼託管平臺，支持 Git 和 Mercurial 版本控制系統。Bitbucket 還提供了與其他 Atlassian 工具（如 Jira 和 Confluence）的集成。
## 創建 Bitbucket 倉庫

1. 登錄 Bitbucket 帳戶。
2. 點擊 “Create repository” 按鈕。
3. 輸入倉庫名稱和描述，選擇 Git 或 Mercurial，選擇公開或私有。
4. 點擊 “Create repository” 按鈕創建倉庫。

克隆 Bitbucket 倉庫
從 Bitbucket 克隆倉庫到本地：
```
git clone https://bitbucket.org/username/repository.git
```
發起 Pull Request

1. 提交更改並推送到功能分支。
2. 打開 Bitbucket 倉庫頁面，點擊 “Create pull request” 按鈕。
3. 選擇目標分支和功能分支，輸入描述信息。
4. 點擊 “Create pull request” 按鈕。

### 7.4 Git 的高級技巧
#### 7.4.1 使用 Git Alias
Git Alias 是 Git 的別名功能，可以用來簡化命令。
配置 Alias
在 .gitconfig 文件中添加以下內容：
```
[alias]
st = status
co = checkout
ci = commit
br = branch
lg = log --oneline --graph --decorate --all
```
使用別名命令
```
git st
git co branch-name
```
git ci -m "提交信息"
#### 7.4.2 使用 Reflog 恢復丟失的提交
通過 Reflog，可以恢復丟失的提交或分支。
查看引用更新歷史：
```
git reflog
```
恢復到特定的提交：
```
git reset --hard commit-hash
```
#### 7.4.3 使用 Git Hooks
Git Hooks 是在特定事件發生時自動執行的腳本。這些事件包括提交、合併、推送等。通過 Git Hooks，可以在這些事件發生時自動執行自定義操作。
## 配置 Git Hooks
在倉庫的 .git/hooks 目錄中創建 Hook 腳本。例如，創建一個 pre-commit Hook：
```
#!/bin/sh
# pre-commit hook example
echo "Running pre-commit hook"
./run-tests.sh
```
給腳本添加可執行權限：
```
chmod +x .git/hooks/pre-commit
```
#### 7.4.4 使用 Git Submodules
Git Submodules 是 Git 倉庫中的子倉庫，適用於包含外部依賴的情況。
添加 Submodule
在主倉庫中添加 Submodule：
```
git submodule add https://github.com/username/submodule-repo.git path/to/submodule
```
初始化和更新 Submodule
克隆倉庫後，初始化和更新 Submodule：
```
git submodule init
git submodule update
```
#### 7.4.5 使用 Git LFS
Git LFS (Large File Storage) 是 Git 的一個擴展，用於管理和存儲大文件。通過 Git LFS，可以將大文件的存儲和版本控制交給專門的 LFS 服務器，減少 Git 倉庫的大小和壓力。
安裝 Git LFS
安裝 Git LFS :
```
git lfs install
```
跟蹤大文件
使用 Git LFS 跟蹤特定類型的大文件：
```
git lfs track "*.psd"
```
將 .gitattributes 文件添加到倉庫：
```
git add .gitattributes
git commit -m "Add Git LFS tracking for PSD files"
```
### 7.5 Git 的集成應用
#### 7.5.1 與 Jenkins 集成
Jenkins 是一個流行的開源自動化服務器，用於構建、部署和自動化各種軟件項目。
配置 Jenkins 與 Git 集成

1. 安裝 Jenkins 和 Git 插件。
2. 創建新的 Jenkins 任務，選擇 “Pipeline”。
3. 配置 Pipeline 腳本：
```
pipeline {
agent any
stages {
stage('Build') {
steps {
git 'https://github.com/username/repository.git'
sh 'make build'
}
}
stage('Test') {
steps {
sh 'make test'
}
stage('Deploy') {
steps {
sh 'make deploy'
}
}
```
#### 7.5.2 與 Travis CI 集成
Travis CI 是一個託管的持續集成服務，專為 GitHub 託管的開源項目設計。
配置 Travis CI 與 Git 集成

1. 登錄 Travis CI 帳戶並授權訪問 GitHub 倉庫。
2. 創建 .travis.yml 文件：
```
language: python
python:
```

- "3.14"
```
install:
```

- pip install -r requirements.txt
```
script:
```

- pytest
```
deploy:
provider: script
script: bash deploy.sh
on:
branch: main
```
#### 7.5.3 與 GitLab CI/CD 集成
GitLab CI/CD 是 GitLab 提供的內置持續集成和持續部署服務。
配置 GitLab CI/CD 與 Git 集成

1. 登錄 GitLab 帳戶並創建新項目。
2. 創建 .gitlab-ci.yml 文件：
```
stages:
```

- build
- test
- deploy
```
build:
stage: build
script:
```

- make build
```
test:
stage: test
script:
```

- make test
```
deploy:
stage: deploy
script:
```

- make deploy
```
only:
```

- main

## 小結
本章介紹了 Git 的各種工具和整合，包括圖形化工具、集成開發環境（IDE）和代碼託管平臺。這些工具和平臺可以幫助開發者更高效地進行分支管理、代碼審查和協同工作。此外，還介紹了一些 Git 的高級技巧，如使用 Git Alias、Reflog 恢復丟失的提交、Git Hooks、自動化測試和持續集成（CI/CD）的配置方法。這些技巧和實踐可以幫助開發者更靈活和高效地使用 Git 進行版本控制和項目管理。
8: Git 安全與最佳實踐
### 8.1 Git 安全概述
8.1.1 為什麼 Git 安全很重要？
Git 是分佈式版本控制系統，存儲著項目的所有歷史版本和敏感信息。如果安全性不足，可能會導致數據洩漏、未經授權的更改，甚至是整個項目的損毀。因此，確保 Git 的安全性對於保護項目和團隊至關重要。
#### 8.1.2 Git 安全的常見威脅

1. 未經授權的訪問：未經授權的用戶訪問和更改倉庫內容。
2. 敏感信息洩漏：代碼庫中包含敏感信息（如 API 密鑰、密碼）。
3. 歷史篡改：未經授權的歷史記錄修改。
4. 惡意代碼：惡意代碼被推送到倉庫，可能影響項目安全和穩定性。

### 8.2 Git 用戶認證
#### 8.2.1 SSH 鑰匙
使用 SSH 鑰匙進行身份驗證，提高遠程倉庫的安全性。
生成 SSH 鑰匙

1. 打開終端，生成新的 SSH 鑰匙：
```
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"
```

2. 根據提示，設置密鑰文件存儲位置和密碼。

添加 SSH 鑰匙到代理

1. 啟動 SSH 代理：
```
eval "$(ssh-agent -s)"
```

2. 添加私鑰到代理：
```
ssh-add ~/.ssh/id_rsa
```
將公鑰添加到 Git 平臺

1. 進入 GitHub、GitLab 或 Bitbucket 的設置頁面。
2. 找到 "SSH and GPG keys" 或類似選項，點擊 "New SSH key"。
3. 將 ~/.ssh/id_rsa.pub 文件中的公鑰內容複製並粘貼到相應字段，然後保存。

#### 8.2.2 HTTPS 認證
使用 HTTPS 認證是另一種安全的身份驗證方式。
配置 Git 使用 HTTPS 認證

1. 克隆倉庫：
```
git clone https://github.com/username/repository.git
```

2. 在每次推送或拉取時，輸入 Git 平臺的用戶名和密碼。為了提高安全性，可以使用個人訪問令牌（PAT）代替密碼。

設置個人訪問令牌（PAT）

1. 進入 GitHub、GitLab 或 Bitbucket 的設置頁面。
2. 找到 "Developer settings" 或類似選項，創建新的個人訪問令牌。
3. 設置令牌的名稱和權限範圍，生成並保存令牌。
4. 在需要輸入密碼時，使用個人訪問令牌代替。

### 8.3 保護敏感信息
#### 8.3.1 使用 .gitignore 文件
使用 .gitignore 文件來忽略不需要追蹤的文件和目錄，避免將敏感信息提交到倉庫中。
## 配置 .gitignore
在倉庫根目錄創建或編輯 .gitignore 文件，添加要忽略的文件和目錄：
```
# 忽略所有 .env 文件
.env
# 忽略所有 .key 文件
```
*.key
```
# 忽略特定目錄
secret/
```
#### 8.3.2 使用 Git 祕密掃描工具
Git 祕密掃描工具可以自動檢查代碼庫中的敏感信息，防止敏感信息洩漏。
常見的祕密掃描工具

1. GitGuardian：實時監控和掃描 GitHub 上的敏感信息洩漏。
2. TruffleHog：深度掃描 Git 歷史，查找可能的密鑰和祕密。
3. Gitleaks：快速掃描 Git 歷史，查找敏感信息。

使用 Gitleaks

1. 安裝 Gitleaks :
```
brew install gitleaks
```

2. 掃描本地倉庫：
```
gitleaks detect
```
### 8.4 Git 分支保護
#### 8.4.1 保護分支的概念
保護分支可以防止未經授權的推送和強制推送操作，確保代碼的穩定性和安全性。通過設置分支保護規則，可以強制代碼審查、測試通過等要求。
#### 8.4.2 在 GitHub 上設置保護分支

1. 進入 GitHub 倉庫的設置頁面。
2. 找到 "Branches" 頁面，選擇要保護的分支。
3. 點擊 "Add rule" 按鈕，設置保護規則。

## 常見的分支保護規則

- Require pull request reviews before merging：合併前需要 Pull Request 審查。
- Require status checks to pass before merging：合併前需要狀態檢查通過。
- Include administrators：包括管理員在內的所有人都需遵守規則。

#### 8.4.3 在 GitLab 上設置保護分支

1. 進入 GitLab 倉庫的設置頁面。
2. 找到 "Repository" -> "Branches" 頁面。
3. 在 "Protected branches" 部分，設置要保護的分支。

常見的分支保護規則

- No one can force push：禁止任何人強制推送。
- Developers + Maintainers can merge：只有開發者和維護者可以合併。

### 8.5 Git 代碼審查
#### 8.5.1 代碼審查的重要性
代碼審查可以發現潛在問題，提高代碼質量和一致性，促進團隊知識共享。通過代碼審查，可以確保代碼符合團隊的標準和最佳實踐。
#### 8.5.2 Pull Request 工作流程
Pull Request 工作流程是 Git 平臺常用的代碼審查方法。開發者在功能分支上進行開發，完成後發起 Pull Request，請求將更改合併到主分支。
發起 Pull Request

1. 提交更改並推送到功能分支。
2. 打開 GitHub 倉庫頁面，點擊 “New pull request” 按鈕。
3. 選擇目標分支和功能分支，點擊 “Create pull request” 按鈕。
4. 輸入描述信息，點擊 “Create pull request” 按鈕。

代碼審查

1. 團隊成員對 Pull Request 進行代碼審查，提出意見和建議。
2. 開發者根據審查意見進行修改，提交新的更改。
3. 代碼審查通過後，將 Pull Request 合併到主分支。

#### 8.5.3 Merge Request 工作流程
Merge Request 工作流程是 GitLab 上常用的代碼審查方法。開發者在功能分支上進行開發，完成後發起 Merge Request，請求將更改合併到主分支。
## 發起 Merge Request

1. 提交更改並推送到功能分支。
2. 打開 GitLab 倉庫頁面，點擊 “Merge Requests” 按鈕。
3. 點擊 “New merge request” 按鈕，選擇目標分支和功能分支。
4. 輸入描述信息，點擊 “Submit merge request” 按鈕。

代碼審查

1. 團隊成員對 Merge Request 進行代碼審查，提出意見和建議。
2. 開發者根據審查意見進行修改，提交新的更改。
3. 代碼審查通過後，將 Merge Request 合併到主分支。

### 8.6 Git 的最佳實踐
#### 8.6.1 保持提交歷史清晰
提交歷史應該簡潔明瞭，反映出每次變更的目的和內容。避免無意義的提交信息，有助於理解項目的演變過程。
撰寫良好的提交信息
良好的提交信息有助
於協作者理解更改的原因和內容。
提交信息格式
提交信息應該包括以下幾部分：

1. 標題：簡要描述更改，不超過 50 個字符。
2. 正文：詳細描述更改，解釋原因和實施方法。

提交信息示例
## 修復登錄頁面崩潰問題
當用戶輸入錯誤的憑據時，登錄頁面會崩潰。這是由於一個未捕獲的異常引起的。添加了異常處理邏輯，確保頁面不會崩潰，並顯示適當的錯誤信息。
#### 8.6.2 使用標籤管理版本
使用標籤來標記項目的重要里程碑，如發布新版本。標籤有助於回溯歷史版本，便於版本管理。
創建標籤
```
git tag v1.0.0
```
推送標籤到遠程倉庫
```
git push origin v1.0.0
```
#### 8.6.3 定期備份和恢復
定期備份 Git 倉庫，以防止數據丟失和損壞。備份可以使用 Git 本地倉庫的克隆或使用專門的備份工具。
克隆本地倉庫作為備份
```
git clone --mirror /path/to/repository /path/to/backup
```
恢復備份
```
git clone /path/to/backup /path/to/repository
```
#### 8.6.4 保護倉庫歷史
保護倉庫歷史可以防止未經授權的歷史篡改和強制推送操作。
禁用強制推送
在 GitHub 上禁用強制推送：

1. 進入倉庫的設置頁面。
2. 找到 "Branches" 頁面，設置保護規則。
3. 勾選 "Protect this branch" 和 "Do not allow force pushes"。

在 GitLab 上禁用強制推送：

1. 進入倉庫的設置頁面。
2. 找到 "Repository" -> "Branches" 頁面。
3. 在 "Protected branches" 部分，設置要保護的分支，並選擇 "No one can force push"。

### 8.7 Git 的自動化和持續集成
#### 8.7.1 自動化測試
自動化測試是確保代碼質量的重要環節。在合併分支之前，自動運行測試，確保代碼穩定。
配置自動化測試

1. 編寫單元測試、集成測試和端到端測試。
2. 配置 CI 工具自動運行測試。

使用 GitHub Actions 進行自動化測試

1. 創建 .github/workflows/test.yml 文件：
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
```

- uses: actions/checkout@v7
- name: Set up Python
```
uses: actions/setup-python@v7
with:
python-version: '3.14'
```

- name: Install dependencies
```
run: |
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- name: Run tests
```
run: |
pytest
```
#### 8.7.2 持續集成 (CI)
持續集成 (CI) 是一種軟件開發實踐，開發者頻繁地將代碼更改合併到主分支，每次合併後自動進行構建和測試。CI 的目的是早期發現和修復問題，確保代碼庫始終保持在一個可工作的狀態。
## 配置 CI 工具
選擇並配置 CI 工具，如 Jenkins、Travis CI 或 GitLab CI/CD。
使用 Jenkins 進行 CI

1. 安裝 Jenkins 和必要的插件。
2. 創建新的 Jenkins 任務，選擇 “Pipeline”。
3. 配置 Pipeline 腳本：
```
pipeline {
agent any
stages {
stage('Build') {
steps {
git 'https://github.com/username/repository.git'
sh 'make build'
}
}
stage('Test') {
steps {
sh 'make test'
}
}
stage('Deploy') {
steps {
sh 'make deploy'
}
}
}
}
```
#### 8.7.3 持續部署 (CD)
持續部署 (CD) 是一種軟件發布實踐，將每次通過 CI 測試的代碼更改自動部署到生產環境。CD 的目的是自動化發布過程，確保代碼可以快速、安全地交付給用戶。
## 配置 CD 工具
選擇並配置 CD 工具，如 GitLab CI/CD、CircleCI 或 GitHub Actions。
使用 GitLab CI/CD 進行 CD

1. 創建 .gitlab-ci.yml 文件：
```
stages:
```

- build
- test
- deploy
```
build:
stage: build
script:
```

- make build
```
test:
stage: test
script:
```

- make test
```
deploy:
stage: deploy
script:
```

- make deploy
```
only:
```

- main

## 小結
本章介紹了 Git 安全與最佳實踐，包括用戶認證、保護敏感信息、分支保護、代碼審查和持續集成等內容。這些實踐可以幫助開發者提高 Git 倉庫的安全性和代碼質量，確保項目的穩定性和可靠性。此外，還介紹了一些 Git 的高級技巧，如使用 Git Alias、Reflog 恢復丟失的提交、Git Hooks、自動化測試和持續集成等，這些技巧和實踐可以幫助開發者更靈活和高效地使用 Git 進行版本控制和項目管理。
9: Git 的實踐應用
### 9.1 開源項目管理
#### 9.1.1 開源項目的重要性
開源項目允許開發者共享和協作開發軟件，促進技術進步和創新。通過參與開源項目，開發者可以學習新技術、提高技能並與全球的開發者建立聯繫。
#### 9.1.2 使用 Git 管理開源項目
Git 是開源項目中最常用的版本控制系統。它提供了強大的分支管理和協作工具，幫助開發者高效地協作和管理項目。
創建開源項目倉庫

1. 登錄 GitHub、GitLab 或 Bitbucket 帳戶。
2. 點擊 "New repository" 按鈕。
3. 輸入倉庫名稱和描述，選擇公開（Public）。
4. 點擊 "Create repository" 按鈕創建倉庫。

設置項目文檔
良好的文檔有助於吸引貢獻者並促進協作。常見的項目文檔包括：
README.md：項目簡介、安裝和使用說明。
CONTRIBUTING.md：貢獻指南，包括如何報告問題、提交代碼和參與討論。
LICENSE：項目的開源授權文件，說明他人可以如何使用、修改和再分發這個項目。
### 9.2 分支策略和工作流
#### 9.2.1 Git Flow 工作流
Git Flow 是一種適用於大型項目的工作流，具有嚴格的分支管理策略。
分支模型

1. 主分支（master）：存儲穩定的發布版本。
2. 開發分支（develop）：用於進行日常開發。
3. 功能分支（feature）：用於開發新功能。
4. 釋出分支（release）：用於發布前的測試和修復。
5. 熱修復分支（hotfix）：用於修復主分支上的緊急問題。

Git Flow 的操作

1. 初始化 Git Flow :
```
git flow init
```

2. 創建功能分支：
```
git flow feature start new-feature
```

3. 完成功能開發：
```
git flow feature finish new-feature
```

4. 創建釋出分支：
```
git flow release start 1.0.0
```

5. 完成釋出：
```
git flow release finish 1.0.0
```

6. 創建熱修復分支：
```
git flow hotfix start 1.0.1
```

7. 完成熱修復：
```
git flow hotfix finish 1.0.1
```
#### 9.2.2 GitHub Flow 工作流
GitHub Flow 是一種簡化的工作流，適用於小型項目和持續部署。
工作流步驟

1. 創建功能分支：
```
git checkout -b new-feature
```

2. 提交更改：
```
git add.
```
git commit -m "描述你的更改"

3. 推送功能分支：
```
git push origin new-feature
```

4. $ \underline{\text{發起 Pull Request}} $：在 GitHub 上發起 Pull Request，請求將更改合併到主分支。
5. 代碼審查和合併：代碼審查通過後，將 Pull Request 合併到主分支。
6. 刪除功能分支：
```
git branch -d new-feature
git push origin --delete new-feature
```
### 9.3 持續集成與持續部署 (CI/CD)

<figure class="fig-svg"><svg viewBox="0 0 860 200" width="100%" role="img" aria-label="CI/CD 管線：push、安裝依賴、測試、建置、部署與監控" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="95" width="130" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="85" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">git push</text><text x="85" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">推送程式碼</text><rect x="180" y="95" width="150" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="255" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">CI：安裝</text><text x="255" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">pip install -r</text><rect x="360" y="95" width="150" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="435" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">CI：測試</text><text x="435" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">manage.py test</text><rect x="540" y="95" width="130" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="605" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">建置</text><text x="605" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">hexo／容器映像</text><rect x="700" y="95" width="140" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="770" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">部署與監控</text><text x="770" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">Pages／K8s</text><line x1="150" y1="126" x2="176" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="330" y1="126" x2="356" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="510" y1="126" x2="536" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="670" y1="126" x2="696" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="182" y="86" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#f0a04b">失敗即中斷</text></svg><figcaption>圖　CI/CD 管線：push 之後自動安裝依賴、跑測試（失敗即中斷），再建置與部署，最後由監控與日誌接手。</figcaption></figure>
#### 9.3.1 持續集成 (CI)
持續集成是一種軟件開發實踐，開發者頻繁地將代碼更改合併到主分支，每次合併後自動進行構建和測試，確保代碼庫始終保持在一個可工作的狀態。
## 配置持續集成工具
常見的 CI 工具包括 Jenkins、Travis CI 和 GitLab CI/CD。
使用 Jenkins 進行持續集成

1. 安裝 Jenkins 和必要的插件。
2. 創建新的 Jenkins 任務，選擇 “Pipeline”。
3. 配置 Pipeline 腳本：
```
pipeline {
agent any
stages {
stage('Build') {
steps {
git 'https://github.com/username/repository.git'
sh 'make build'
}
}
stage('Test') {
steps {
sh 'make test'
}
}
}
}
```
## 使用 Travis CI 進行持續集成

1. 創建 .travis.yml 文件：
```
language: python
python:
```

- "3.14"
```
install:
```

- pip install -r requirements.txt
```
script:
```

- pytest

#### 9.3.2 持續部署 (CD)
持續部署是一種軟件發布實踐，將每次通過 CI 測試的代碼更改自動部署到生產環境，確保代碼可以快速、安全地交付給用戶。
## 配置持續部署工具
常見的 CD 工具包括 GitLab CI/CD、CircleCI 和 GitHub Actions。
使用 GitLab CI/CD 進行持續部署

1. 創建 .gitlab-ci.yml 文件：
```
stages:
```

- build
- test
- deploy
```
build:
stage: build
script:
```

- make build
```
test:
stage: test
script:
```

- make test
```
deploy:
stage: deploy
script:
```

- make deploy
```
only:
```

- main

使用 GitHub Actions 進行持續部署

1. 創建 .github/workflows/deploy.yml 文件：
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
```

- uses: actions/checkout@v7
- name: Set up Python
```
uses: actions/setup-python@v7
with:
python-version: '3.14'
```

- name: Install dependencies
```
run: |
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- name: Run tests
```
run: |
pytest
```

- name: Deploy
```
run: |
make deploy
```
### 9.4 團隊協作與代碼審查
#### 9.4.1 團隊協作
團隊協作是軟件開發的重要組成部分。Git 提供了強大的工具，幫助開發者高效地協作和管理代碼。
## 分支管理
良好的分支管理策略有助於團隊協作。使用 Git Flow、GitHub Flow 或 GitLab Flow 等工作流，確保每個功能或修復都有自己的分支，避免不同功能之間的衝突。
## 代碼審查
代碼審查有助於提高代碼質量和一致性，促進團隊知識共享。通過 Pull Request 或 Merge Request，團隊成員可以對代碼進行審查，發現潛在問題，提出改進建議。
代碼審查步驟

1. 開發者完成功能或修復，提交更改並推送到功能分支。
2. 發起 Pull Request 或 Merge Request，請求將更改合併到主分支。
3. 團隊成員對 Pull Request 或 Merge Request 進行代碼審查，提出意見和建議。
4. 開發者根據審查意見進行修改，提交新的更改。
5. 代碼審查通過後，將 Pull Request 或 Merge Request 合併到主分支。

#### 9.4.2 開源協作
開源項目允許來自世界各地的開發者共同參與和貢獻。通過參與開源項目，開發者可以學習新技術、提高技能並與全球的開發者建立聯繫。
## 貢獻開源項目

1. 尋找感興趣的開源項目：在 GitHub、GitLab 或 Bitbucket 上尋找感興趣的開源項目，瀏覽項目的 README.md 和 CONTRIBUTING.md 文件。
2. \*\*

報告問題\*\*：如果發現問題，可以在項目的 Issue 頁面報告問題，描述問題的詳細信息和復現步驟。3. 提交代碼：如果希望修復問題或添加新功能，可以 fork 項目，創建功能分支，提交更改並發起 Pull Request 或 Merge Request。4. \*\*參與討論\*\*：積極參與項目的討論和代碼審查，提出意見和建議。
### 9.5 Git 的高級應用
9.5.1 Git Submodule
Git Submodule 是 Git 倉庫中的子倉庫，用於包含和管理外部依賴。
添加 Submodule
在主倉庫中添加 Submodule：
```
git submodule add https://github.com/username/submodule-repo.git path/to/submodule
```
## 初始化和更新 Submodule
克隆倉庫後，初始化和更新 Submodule：
```
git submodule init
git submodule update
```
9.5.2 Git LFS (Large File Storage)
Git LFS 是 Git 的一個擴展，用於管理和存儲大文件。通過 Git LFS，可以將大文件的存儲和版本控制交給專門的 LFS 服務器，減少 Git 倉庫的大小和壓力。
安裝 Git LFS
安裝 Git LFS :
```
git lfs install
```
跟蹤大文件
使用 Git LFS 跟蹤特定類型的大文件：
```
git lfs track "*.psd"
```
將 .gitattributes 文件添加到倉庫：
```
git add .gitattributes
git commit -m "Add Git LFS tracking for PSD files"
```
9.5.3 Git Hooks
Git Hooks 是在特定事件發生時自動執行的腳本。這些事件包括提交、合併、推送等。通過 Git Hooks，可以在這些事件發生時自動執行自定義操作。
## 配置 Git Hooks
在倉庫的 .git/hooks 目錄中創建 Hook 腳本。例如，創建一個 pre-commit Hook：
```
#!/bin/sh
# pre-commit hook example
echo "Running pre-commit hook"
./run-tests.sh
```
給腳本添加可執行權限：
```
chmod +x .git/hooks/pre-commit
```
### 9.6 Git 的自動化和持續集成
#### 9.6.1 自動化測試
自動化測試是確保代碼質量的重要環節。在合併分支之前，自動運行測試，確保代碼穩定。
配置自動化測試

1. 編寫單元測試、集成測試和端到端測試。
2. 配置 CI 工具自動運行測試。

使用 GitHub Actions 進行自動化測試

1. 創建 .github/workflows/test.yml 文件：
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
```

- uses: actions/checkout@v7
- name: Set up Python
```
uses: actions/setup-python@v7
with:
python-version: '3.14'
```

- name: Install dependencies
```
run: |
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- name: Run tests
```
run: |
pytest
```
#### 9.6.2 持續集成 (CI)
持續集成是一種軟件開發實踐，開發者頻繁地將代碼更改合併到主分支，每次合併後自動進行構建和測試，確保代碼庫始終保持在一個可工作的狀態。
## 配置 CI 工具
選擇並配置 CI 工具，如 Jenkins、Travis CI 或 GitLab CI/CD。
使用 Jenkins 進行持續集成

1. 安裝 Jenkins 和必要的插件。
2. 創建新的 Jenkins 任務，選擇 “Pipeline”。
3. 配置 Pipeline 腳本：
```
pipeline {
agent any
stages {
stage('Build') {
steps {
git 'https://github.com/username/repository.git'
sh 'make build'
}
}
stage('Test') {
steps {
sh 'make test'
}
}
}
}
```
#### 9.6.3 持續部署 (CD)
持續部署是一種軟件發布實踐，將每次通過 CI 測試的代碼更改自動部署到生產環境，確保代碼可以快速、安全地交付給用戶。
## 配置 CD 工具
選擇並配置 CD 工具，如 GitLab CI/CD、CircleCI 或 GitHub Actions。
使用 GitLab CI/CD 進行持續部署

1. 創建 .gitlab-ci.yml 文件：
```
stages:
```

- build
- test
- deploy
```
build:
stage: build
script:
```

- make build
```
test:
stage: test
script:
```

- make test
```
deploy:
stage: deploy
script:
```

- make deploy
```
only:
```

- main

使用 GitHub Actions 進行持續部署

1. 創建 .github/workflows/deploy.yml 文件：
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
```

- uses: actions/checkout@v7
- name: Set up Python
```
uses: actions/setup-python@v7
with:
python-version: '3.14'
```

- name: Install dependencies
```
run: |
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- name: Run tests
```
run: |
pytest
```

- name: Deploy
```
run: |
make deploy
```
### 9.7 Git 的性能優化
#### 9.7.1 優化大型倉庫
大型倉庫可能會導致性能問題，影響開發效率。通過優化大型倉庫，可以提高 Git 操作的速度和響應時間。
使用 Git LFS
Git LFS 可以幫助管理和存儲大文件，減少 Git 倉庫的大小和壓力。
清理未使用的文件
使用 git gc 命令清理未使用的文件，優化倉庫性能：
```
git gc --aggressive --prune=now
```
壓縮歷史記錄
使用 git repack 命令壓縮歷史記錄，減少倉庫大小：
```
git repack -a -d --depth=250 --window=250
```
#### 9.7.2 提高操作效率
通過一些技巧和工具，可以提高 Git 操作的效率，減少操作時間。
## 使用 Git Alias
Git Alias 是 Git 的別名功能，可以用來簡化命令。配置 Git Alias 可以提高操作效率。
在 .gitconfig 文件中添加別名配置：
```
[alias]
st = status
co = checkout
ci = commit
br = branch
lg = log --oneline --graph --decorate --all
```
使用簡化命令：
```
git st
git co branch-name
```
git ci -m "提交信息"
```
git br
git lg
```
使用並行操作
Git 提供了一些並行操作選項，可以提高操作效率。
使用 git fetch 命令時，添加 -j 選項以啟用並行操作：
```
git fetch -j4
```
## 小結
本章介紹了 Git 的實踐應用，包括開源項目管理、分支策略和工作流、持續集成與持續部署（CI/CD）、團隊協作與代碼審查、高級應用和性能優化等內容。這些實踐應用可以幫助開發者更靈活和高效地使用 Git 進行版本控制和項目管理，提高代碼質量和工作效率。此外，還介紹了一些 Git 的高級技巧，如使用 Git Submodule、Git LFS 和 Git Hooks，以及如何優化大型倉庫和提高操作效率等。
10: Git 在大型項目中的應用
### 10.1 大型項目的挑戰
#### 10.1.1 複雜的代碼基礎
大型項目通常擁有龐大而複雜的代碼基礎，涉及多個模塊和依賴關係。管理這些代碼需要高效的版本控制和協作工具。
#### 10.1.2 多開發者協作
大型項目通常由多個開發者共同開發，需要有效的協作機制和分支管理策略，以避免衝突和重複工作。
#### 10.1.3 項目管理和發布
大型項目需要嚴格的項目管理和版本控制，以確保代碼質量和發布的穩定性。
### 10.2 分支管理策略
#### 10.2.1 Git Flow 工作流
Git Flow 是一種適用於大型項目的工作流，具有嚴格的分支管理策略。
Git Flow 的分支模型

1. 主分支 (master): 存儲穩定的發布版本。
2. 開發分支 (develop): 用於進行日常開發。
3. 功能分支 (feature): 用於開發新功能。
4. 釋出分支 (release): 用於發布前的測試和修復。
5. 熱修復分支 (hotfix): 用於修復主分支上的緊急問題。

Git Flow 的操作

1. 初始化 Git Flow :
```
git flow init
```

2. 創建功能分支：
```
git flow feature start new-feature
```

3. 完成功能開發：
```
git flow feature finish new-feature
```

4. 創建釋出分支：
```
git flow release start 1.0.0
```

5. 完成釋出：
```
git flow release finish 1.0.0
```

6. 創建熱修復分支：
```
git flow hotfix start 1.0.1
```

7. 完成熱修復：
```
git flow hotfix finish 1.0.1
```
#### 10.2.2 GitLab Flow 工作流
GitLab Flow 結合了 Git Flow 和 GitHub Flow 的優點，提供了靈活的分支管理策略，適用於各種規模的項目。
GitLab Flow 的分支模型

1. 環境分支：為不同的環境（如開發、測試和生產）創建獨立的分支。
2. 功能分支 (feature): 每個新功能在主分支上創建一個新的功能分支。
3. 合併請求 (Merge Request): 完成工作後，提交更改並發起合併請求。

### 10.3 持續集成與持續部署 (CI/CD)
#### 10.3.1 持續集成 (CI)
持續集成 (CI) 是一種軟件開發實踐，開發者頻繁地將代碼更改合併到主分支，每次合併後自動進行構建和測試，確保代碼庫始終保持在一個可工作的狀態。
## 配置持續集成工具
常見的 CI 工具包括 Jenkins、Travis CI 和 GitLab CI/CD。
## 使用 Jenkins 進行持續集成

1. 安裝 Jenkins 和必要的插件。
2. 創建新的 Jenkins 任務，選擇 “Pipeline”。
3. 配置 Pipeline 腳本：
```
pipeline {
agent any
stages {
stage('Build') {
steps {
git 'https://github.com/username/repository.git'
sh 'make build'
}
}
stage('Test') {
steps {
sh 'make test'
}
}
}
```
#### 10.3.2 持續部署 (CD)
持續部署 (CD) 是一種軟件發布實踐，將每次通過 CI 測試的代碼更改自動部署到生產環境，確保代碼可以快速、安全地交付給用戶。
## 配置持續部署工具
常見的 CD 工具包括 GitLab CI/CD、CircleCI 和 GitHub Actions。
使用 GitLab CI/CD 進行持續部署

1. 創建 .gitlab-ci.yml 文件：
```
stages:
```

- build
- test
- deploy
```
build:
stage: build
script:
```

- make build
```
test:
stage: test
script:
```

- make test
```
deploy:
stage: deploy
script:
```

- make deploy
```
only:
```

- main

使用 GitHub Actions 進行持續部署

1. 創建 .github/workflows/deploy.yml 文件：
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
```

- uses: actions/checkout@v7
- name: Set up Python
```
uses: actions/setup-python@v7
with:
python-version: '3.14'
```

- name: Install dependencies
```
run: |
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- name: Run tests
```
run: |
pytest
```

- name: Deploy
```
run: |
make deploy
```
### 10.4 代碼審查與協作
#### 10.4.1 代碼審查的重要性
代碼審查可以發現潛在問題，提高代碼質量和一致性，促進團隊知識共享。通過代碼審查，可以確保代碼符合團隊的標準和最佳實踐。
#### 10.4.2 使用 Pull Request 進行代碼審查
Pull Request 工作流是 Git 平臺常用的代碼審查方法。開發者在功能分支上進行開發，完成後發起 Pull Request，請求將更改合併到主分支。
發起 Pull Request

1. 提交更改並推送到功能分支。
2. 打開 GitHub 倉庫頁面，點擊 “New pull request” 按鈕。
3. 選擇目標分支和功能分支，點擊 “Create pull request” 按鈕。
4. 輸入描述信息，點擊 “Create pull request” 按鈕。

代碼審查

1. 團隊成員對 Pull Request 進行代碼審查，提出意見和建議。
2. 開發者根據審查意見進行修改，提交新的更改。
3. 代碼審查通過後，將 Pull Request 合併到主分支。

#### 10.4.3 使用 Merge Request 進行代碼審查
Merge Request 工作流是 GitLab 上常用的代碼審查方法。開發者在功能分支上進行開發，完成後發起 Merge Request，請求將更改合併到主分支。
發起 Merge Request

1. 提交更改並推送到功能分支。
2. 打開 GitLab 倉庫頁面，點擊 “Merge Requests” 按鈕。
3. 點擊 “New merge request” 按鈕，選擇目標分支和功能分支。
4. 輸入描述信息，點擊 “Submit merge request” 按鈕。

代碼審查

1. 團隊成員對 Merge Request 進行代碼審查，提出意見和建議。
2. 開發者根據審查意見進行修改，提交新的更改。
3. 代碼審查通過後，將 Merge Request 合併到主分支。

### 10.5 代碼質量保障
#### 10.5.1 自動化測試
自動化測試是確保代碼質量的重要環節。在合併分支之前，自動運行測試，確保代碼穩定。
配置自動化測試

1. 編寫單元測試、集成測試和端到端測試。
2. 配置 CI 工具自動運行測試。

使用 GitHub Actions 進行自動化測試

1. 創建 .github/workflows/test.yml 文件：
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
```

- uses: actions/checkout@v7
- name: Set up Python
```
uses: actions/setup-python@v7
with:
python-version: '3.14'
```

- name: Install dependencies
```
run: |
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- name: Run tests
```
run: |
pytest
```
#### 10.5.2 靜態代碼分析
靜態代碼分析是一種自動化工具，用於檢查代碼中的潛在問題和不一致性。通過靜態代碼分析，可以提前發現並修復問題，提高代碼質量。
使用 ESLint 進行靜態代碼分析

1. 安裝 ESLint :
```
npm install eslint --save-dev
```

2. 初始化 ESLint 配置：
```
npx eslint --init
```

3. 配置 CI 工具運行 ESLint :

使用 GitHub Actions 配置 ESLint
創建 .github/workflows/lint.yml 文件：
```
name: Lint
on: [push, pull_request]
jobs:
lint:
runs-on: ubuntu-latest
steps:
```

- uses: actions/checkout@v7
- name: Set up Node.js
```
uses: actions/setup-node@v2
with:
node-version: "14"
```

- name: Install dependencies
```
run: npm install
```

- name: Run ESLint
```
run: npx eslint .
```
#### 10.5.3 測試覆蓋率報告
測試覆蓋率報告顯示了代碼中被測試覆蓋的部分，幫助開發者確保所有關鍵部分都被測試。
使用 Jest 生成測試覆蓋率報告

1. 安裝 Jest :
```
npm install jest --save-dev
```

2. 配置 Jest 生成覆蓋率報告：

在 package.json 中添加 Jest 配置：
```
{
"scripts": {
"test": "jest --coverage"
}
}
```

3. 生成測試覆蓋率報告：
```
npm test
```
### 10.6 大型倉庫的性能優化
#### 10.6.1 優化大型倉庫
大型倉庫可能會導致性能問題，影響開發效率。通過優化大型倉庫，可以提高 Git 操作的速度和響應時間。
使用 Git LFS
Git LFS 可以幫助管理和存儲大文件，減少 Git 倉庫的大小和壓力。
清理未使用的文件
使用 git gc 命令清理未使用的文件，優化倉庫性能：
```
git gc --aggressive --prune=now
```
壓縮歷史記錄
使用 git repack 命令壓縮歷史記錄，減少倉庫大小：
```
git repack -a -d --depth=250 --window=250
```
#### 10.6.2 提高操作效率
通過一些技巧和工具，可以提高 Git 操作的效率，減少操作時間。
## 使用 Git Alias
Git Alias 是 Git 的別名功能，可以用來簡化命令。配置 Git Alias 可以提高操作效率。
在 .gitconfig 文件中添加別名配置：
```
[alias]
st = status
co = checkout
ci = commit
br = branch
lg = log --oneline --graph --decorate --all
```
使用簡化命令：
```
git st
git co branch-name
```
git ci -m "提交信息"
```
git br
git lg
```
使用並行操作
Git 提供了一些並行操作選項，可以提高操作效率。
使用 git fetch 命令時，添加 -j 選項以啟用並行操作：
```
git fetch -j4
```
### 10.7 Git 的自動化和持續集成
#### 10.7.1 自動化測試
自動化測試是確保代碼質量的重要環節。在合併分支之前，自動運行測試，確保代碼穩定。
## 配置自動化測試

1. 編寫單元測試、集成測試和端到端測試。
2. 配置 CI 工具自動運行測試。

使用 GitHub Actions 進行自動化測試

1. 創建 .github/workflows/test.yml 文件：
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
```

- uses: actions/checkout@v7
- name: Set up Python
```
uses: actions/setup-python@v7
with:
python-version: '3.14'
```

- name: Install dependencies
```
run: |
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- name: Run tests
```
run: |
pytest
```
#### 10.7.2 持續集成 (CI)
持續集成是一種軟件開發實踐，開發者頻繁地將代碼更改合併到主分支，每次合併後自動進行構建和測試，確保代碼庫始終保持在一個可工作的狀態。
## 配置 CI 工具
選擇並配置 CI 工具，如 Jenkins、Travis CI 或 GitLab CI/CD。
使用 Jenkins 進行持續集成

1. 安裝 Jenkins 和必要的插件。
2. 創建新的 Jenkins 任務，選擇 “Pipeline”。
3. 配置 Pipeline 腳本：
```
pipeline {
agent any
stages {
stage('Build') {
steps {
git 'https://github.com/username/repository.git'
sh 'make build'
}
}
stage('Test') {
steps {
sh 'make test'
}
}
}
}
```
#### 10.7.3 持續部署 (CD)
持續部署是一種軟件發布實踐，將每次通過 CI 測試的代碼更改自動部署到生產環境，確保代碼可以快速、安全地交付給用戶。
## 配置 CD 工具
選擇並配置 CD 工具，如 GitLab CI/CD、CircleCI 或 GitHub Actions。
使用 GitLab CI/CD 進行持續部署

1. 創建 .gitlab-ci.yml 文件：
```
stages:
```

- build
- test
- deploy
```
build:
stage: build
script:
```

- make build
```
test:
stage: test
script:
```

- make test
```
deploy:
stage: deploy
script:
```

- make deploy
```
only:
```

- main

## 使用 GitHub Actions 進行持續部署

1. 創建 .github/workflows/deploy.yml 文件：
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
```

- uses: actions/checkout@v7
- name: Set up Python
```
uses: actions/setup-python@v7
with:
python-version: '3.14'
```

- name: Install dependencies
```
run: |
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- name: Run tests
```
run: |
pytest
```

- name: Deploy
```
run: |
make deploy
```
## 小結
本章介紹了 Git 在大型項目中的應用，包括分支管理策略、持續集成與持續部署（CI/CD）、代碼審查與協作、代碼質量保障、大型倉庫的性能優化等內容。這些實踐應用可以幫助開發者更靈活和高效地使用 Git 進行版本控制和項目管理，提高代碼質量和工作效率。此外，還介紹了一些 Git 的高級技巧，如使用 Git Submodule、Git LFS 和 Git Hooks，以及如何優化大型倉庫和提高操作效率等。
11: Git 在雲計算中的應用
### 11.1 雲計算概述
11.1.1 什麼是雲計算？
雲計算是一種通過互聯網提供計算資源和服務的模式。雲計算允許用戶根據需求動態調整計算資源，減少了硬件和軟件的運營成本，並提高了業務的靈活性和可擴展性。
#### 11.1.2 雲計算的服務模型

1. 基礎設施即服務 (IaaS)：提供虛擬化的計算資源，如虛擬機、存儲和網絡。
2. 平臺即服務 (PaaS)：提供應用程序開發和運行的平臺，包括操作系統、數據庫和開發工具。
3. 軟件即服務 (SaaS)：通過互聯網提供應用程序服務，用戶可以直接使用，而不需要管理底層基礎設施。

#### 11.1.3 雲計算的部署模型

1. 公有雲：由第三方服務提供商運營，資源通過互聯網公開提供。
2. 私有雲：由單一組織運營，資源僅供內部使用。
3. 混合雲：結合公有雲和私有雲，允許數據和應用在兩者之間轉移。

### 11.2 Git 與雲服務平臺的集成
#### 11.2.1 常見的雲服務平臺

1. Amazon Web Services (AWS)：提供廣泛的雲服務，包括計算、存儲和數據庫。
2. Microsoft Azure：提供雲計算、分析、存儲和網絡服務。
3. Google Cloud Platform (GCP)：提供計算、存儲和機器學習等服務。

#### 11.2.2 使用 Git 管理雲資源
通過基礎設施即代碼（IaC）的方式，將雲資源配置文件存儲在 Git 倉庫中，使用版本控制來管理和追蹤資源的變更。
## Terraform 與 Git 集成
Terraform 是一種流行的 IaC 工具，用於定義和管理雲基礎設施。可以將 Terraform 配置文件存儲在 Git 倉庫中，並使用 CI/CD 工具自動化部署。
創建 Terraform 配置文件

1. 創建 main.tf 文件，定義雲資源配置：
```
provider "aws" {
region = "us-west-2"
}
resource "aws_instance" "example" {
ami = "ami-0c55b159cbfafe1f0"
instance_type = "t2.micro"
}
```

2. 將配置文件添加到 Git 倉庫：
```
git add main.tf
git commit -m "Add initial Terraform configuration"
git push origin main
```
配置 CI/CD 工具自動部署
使用 GitLab CI/CD 進行自動部署：
創建 .gitlab-ci.yml 文件：
```
stages:
```

- deploy
```
deploy:
stage: deploy
script:
```

- terraform init
- terraform apply -auto-approve
```
only:
```

- main

### 11.3 容器化與編排
#### 11.3.1 Docker 容器化
Docker 是一種流行的容器化工具，用於將應用程序及其依賴打包成容器鏡像，確保應用程序可以在任何環境中一致地運行。
創建 Dockerfile
創建一個 Dockerfile 文件，定義如何構建容器鏡像：
```
# 使用 Python 基礎鏡像
FROM python:3.14
# 設置工作目錄
WORKDIR /app
# 複製當前目錄內容到容器中
COPY ./app
# 安裝依賴
RUN pip install -r requirements.txt
# 定義運行容器時的命令
CMD ["python", "app.py"]
```
構建 Docker 鏡像
使用 docker build 命令構建 Docker 鏡像：
```
docker build -t myapp:latest.
```
運行 Docker 容器
使用 docker run 命令運行 Docker 容器：
```
docker run -d -p 5000:5000 myapp:latest
```
#### 11.3.2 Kubernetes 容器編排
Kubernetes 是一個開源的容器編排平臺，用於自動化容器化應用程序的部署、擴展和管理。
配置 Kubernetes 集羣

1. 安裝 Kubernetes CLI 工具 kubectl。
2. 配置 Kubernetes 集羣，使用 Minikube 或其他託管服務（如 Google Kubernetes Engine, Amazon EKS）。

## 創建 Kubernetes 部署
創建一個 deployment.yml 文件，定義 Kubernetes 部署：
```
apiVersion: apps/v1
kind: Deployment
metadata:
name: myapp-deployment
spec:
replicas: 3
selector:
matchLabels:
app: myapp
template:
metadata:
labels:
app: myapp
spec:
containers:
```

- name: myapp
```
image: myapp:latest
ports:
```

- containerPort: 5000

## 部署到 Kubernetes 集羣
使用 kubectl apply 命令將部署應用到 Kubernetes 集羣：
```
kubectl apply -f deployment.yml
```
### 11.4 Git 與持續集成/持續交付 (CI/CD)
#### 11.4.1 配置持續集成
持續集成（CI）是一種軟件開發實踐，開發者頻繁地將代碼變更合併到主分支，每次合併後自動進行構建和測試，確保代碼庫始終保持在一個可工作的狀態。
使用 Jenkins 進行持續集成

1. 安裝 Jenkins 和必要的插件。
2. 創建新的 Jenkins 任務，選擇 “Pipeline”。
3. 配置 Pipeline 腳本：
```
pipeline {
agent any
stages {
stage('Build') {
steps {
git 'https://github.com/username/repository.git'
sh 'make build'
}
}
stage('Test') {
steps {
sh 'make test'
}
}
}
}
```
#### 11.4.2 配置持續交付
持續交付（CD）是一種軟件發布實踐，將每次通過 CI 測試的代碼變更自動部署到預生產或生產環境中，確保代碼可以快速、安全地交付給用戶。
使用 GitLab CI/CD 進行持續交付
創建 .gitlab-ci.yml 文件：
```
stages:
```

- build
- test
- deploy
```
build:
stage: build
script:
```

- make build
```
test:
stage: test
script:
```

- make test
```
deploy:
stage: deploy
script:
```

- make deploy
```
only:
```

- main

使用 GitHub Actions 進行持續交付
創建 .github/workflows/deploy.yml 文件：
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
```

- uses: actions/checkout@v7
- name: Set up Python
```
uses: actions/setup-python@v7
with:
python-version: '3.14'
```

- name: Install dependencies
```
run: |
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- name: Run tests
```
run: |
pytest
```

- name: Deploy
```
run: |
make deploy
```
### 11.5 監控與日誌管理
#### 11.5.1 使用 Prometheus 進行監控
Prometheus 是一個開源的系統監控和報警工具，專為可靠性和運行時性能而設計。
## 安裝 Prometheus

1. 下載 Prometheus :
```
wget https://github.com/prometheus/prometheus/releases/download/v2.27.1/prometheus-2.27.1.linux-amd64.tar.gz
tar xvfz prometheus-2.27.1.linux-amd64.tar.gz
cd prometheus-2
.27.1.linux-amd64
```

2. 配置 Prometheus :

編輯 prometheus.yml 配置文件，定義監控目標：
```
global:
scrape_interval: 15s
scrape_configs:
```

- job_name: "prometheus"
```
static_configs:
```

- targets: ["localhost:9090"]
3. 啟動 Prometheus :
```
./prometheus
```
#### 11.5.2 使用 Grafana 進行可視化
Grafana 是一個開源的數據可視化工具，與 Prometheus 集成，提供強大的監控儀錶板功能。
安裝 Grafana

1. 下載 Grafana :
```
wget https://dl.grafana.com/oss/release/grafana-8.0.0.linux-amd64.tar.gz
tar -zxvf grafana-8.0.0.linux-amd64.tar.gz
cd grafana-8.0.0
```

2. 啟動 Grafana :
```
./bin/grafana-server
```

3. 訪問 Grafana 網頁界面：

打開瀏覽器，訪問 http://localhost:3000，登錄並配置 Prometheus 數據源，創建監控儀錶板。
#### 11.5.3 使用 ELK 堆棧進行日誌管理
ELK 堆棧由 Elasticsearch、Logstash 和 Kibana 組成，是一個強大的日誌管理解決方案。（時代註記：下面的指令是 2021 年的 7.13.2 版本；現行 Elastic Stack 已到 8.x 以上，下載連結與設定格式略有不同。）
安裝 Elasticsearch

1. 下載並安裝 Elasticsearch：
```
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.13.2-linux-x86_64.tar.gz
tar -zxvf elasticsearch-7.13.2-linux-x86_64.tar.gz
cd elasticsearch-7.13.2
```

2. 啟動 Elasticsearch：
```
./bin/elasticsearch
```
安裝 Logstash

1. 下載並安裝 Logstash：
```
wget https://artifacts.elastic.co/downloads/logstash/logstash-7.13.2-linux-x86_64.tar.gz
tar -zxvf logstash-7.13.2-linux-x86_64.tar.gz
cd logstash-7.13.2
```

2. 配置 Logstash:

創建 logstash.conf 配置文件：
```
input {
file {
path => "/var/log/myapp.log"
start_position => "beginning"
}
}
output {
elasticsearch {
hosts => ["localhost:9200"]
}
}
```

3. 啟動 Logstash:
```
./bin/logstash -f logstash.conf
```
安裝 Kibana

1. 下載並安裝 Kibana：
```
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.13.2-linux-x86_64.tar.gz
tar -zxvf kibana-7.13.2-linux-x86_64.tar.gz
cd kibana-7.13.2
```

2. 啟動 Kibana:
```
./bin/kibana
```

3. 訪問 Kibana 網頁界面：

打開瀏覽器，訪問 http://localhost:5601，配置 Elasticsearch 數據源，創建和分析日誌儀錶板。
### 11.6 使用 Git 進行雲資源管理的最佳實踐
#### 11.6.1 基礎設施即代碼 (IaC) 的最佳實踐

1. 版本控制：將所有基礎設施配置文件存儲在 Git 倉庫中，使用版本控制來管理和追蹤變更。
2. 自動化部署：使用 CI/CD 工具自動化基礎設施的部署和管理，減少手動操作的錯誤風險。
3. 分環境管理：將不同環境（如開發、測試和生產）的配置文件分開管理，確保配置的獨立性和一致性。
4. 審核和審批流程：在基礎設施變更前進行代碼審查和審批，確保變更的合理性和安全性。

#### 11.6.2 容器化和編排的最佳實踐

1. 小型化容器：將應用程序拆分成小型、獨立的容器，每個容器只執行一個進程，提高容器的靈活性和可維護性。
2. 自動擴展：使用 Kubernetes 等編排工具，自動管理容器的擴展和縮減，確保系統的高可用性和彈性。
3. 持續集成與持續交付：集成 CI/CD 工具，實現容器鏡像的自動構建、測試和部署，提高交付效率。
4. 監控和日誌管理：使用 Prometheus 和 ELK 堆棧等工具，實時監控容器的運行狀態，收集和分析運行日誌，及時發現和解決問題。

#### 11.6.3 雲資源管理的安全實踐

1. 身份驗證和授權：使用安全的身份驗證和授權機制，確保只有授權用戶能夠訪問和管理雲資源。
2. 數據加密：對靜態和傳輸中的數據進行加密，保護敏感數據的安全。
3. 安全審計：定期審計雲資源的配置和訪問記錄，及時發現和修復安全漏洞。
4. 自動化安全測試：集成自動化安全測試工具，在部署過程中進行安全測試，確保系統的安全性。

