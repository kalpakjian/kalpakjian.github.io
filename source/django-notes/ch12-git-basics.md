# 第 12 章 · 後端開發與 Git 基礎
1 後端網站開發工作流程：
### 1.1 後端開發概述 $ ^{*} $
在現代軟體開發中，後端開發扮演著關鍵的角色，負責管理應用程式的核心邏輯、資料庫互動及伺服器的維護。隨著軟體技術的不斷進步，開發者擁有了更多工具來提升開發效率，其中，整合開發環境（IDE，Integrated Development Environment）是最為重要的一種工具。不同的IDE為開發者提供了不同的功能和優勢，從代碼編輯到除錯再到專案管理，皆可涵蓋。本筆記將深入探討各種IDE在後端開發中的應用，並比較其優缺點，幫助開發者根據需求選擇最適合的IDE。
### 1.2 IDE 在後端開發中的作用
IDE 是開發人員進行代碼編寫、調試和測試的重要工具，特別是在後端開發中，它能夠簡化代碼管理和專案結構。透過自動補全、語法高亮、內建版本控制系統等功能，開發者可以更專注於業務邏輯的實現，而非繁瑣的基礎設置。此外，現代的 IDE 往往還支持多種語言和框架，使得開發者能夠在同一工具內進行跨語言開發。
\*\*3. 熱門後端開發 IDE 比較 \*\*
3.1 Visual Studio Code (VS Code)
介紹與背景：
Visual Studio Code（VS Code）是微軟於 2015 年推出的輕量級、跨平臺的開源編輯器，迅速成為許多後端開發者的首選。它支援多種語言和框架，並且擁有數千個社羣開發的擴展插件，涵蓋了從 JavaScript 到 Python 及 PHP 等各種後端語言。
主要功能：
- 擴展性強：VS Code 具有豐富的擴展庫，無論是語法高亮、代碼自動完成、還是測試框架整合，都可以透過插件來實現。
- 內建 Git 支援：無需切換至其他終端，開發者可以在 VS Code 中直接使用 Git 進行版本控制，這大大提升了工作流程的效率。
- 強大的除錯功能：VS Code 的 Debugger 支援多種後端語言，並且能夠與 Docker 容器集成，實現容器化應用程式的調試。
- 整合終端：VS Code 內置終端，開發者可以在同一個界面中管理系統命令，無需切換視窗，節省了時間。
使用案例：VS Code 在後端開發中適用於多種語言，尤其是 JavaScript 與 Node.js。許多大型開源項目如 Express.js 和 Meteor.js 都是使用 VS Code 進行開發的。此外，Facebook、Google 等大型科技公司中的開發團隊也廣泛使用 VS Code 來開發微服務及 API。
優點：
- 輕量級且快速，適合初學者與資深開發者。
- 支援廣泛的擴展插件，靈活定製工作流程。
- 跨平臺支援（Windows、macOS、Linux）。
缺點：
- 雖然是輕量級編輯器，但隨著插件數量的增加，可能會影響性能。
- 對於大型項目或複雜的 Java 專案，可能不如 IntelliJ IDEA 那樣強大。
3.2 \*\*IntelliJ IDEA \*\*
介紹與背景：
IntelliJ IDEA 是由 JetBrains 開發的一款 IDE，特別針對 Java 和 Kotlin 開發而設計。自推出以來，IntelliJ IDEA 被許多專業開發者認為是市場上最強大的 Java 開發工具之一。它以出色的智能代碼完成、自動化工具和框架支援著稱，特別適合於企業級應用和大型專案的開發。
主要功能：
- 智能代碼補全：IntelliJ IDEA 可以基於代碼上下文，為開發者提供極為精準的代碼補全建議，減少了代碼錯誤並加快開發速度。
- 框架支援：它內建對 Spring、Hibernate、Maven 等流行框架的支援，使得 Java 開發者可以更快地建立複雜的後端應用程式。
- 內建版本控制系統：不僅支援 Git，還支援 CVS、Subversion 等其他版本控制工具，對於大型企業專案的協作至關重要。
- 強大的重構工具：IntelliJ 的代碼重構功能使得開發者能夠輕鬆、安全地修改代碼，這對於大型專案的維護和升級特別重要。
使用案例：IntelliJ IDEA 被廣泛應用於企業級 Java 開發項目中，如金融科技公司、電子商務平臺及各種微服務架構中。Airbnb、Netflix 和 Uber 等技術公司在其核心服務的開發過程中大量使用 IntelliJ IDEA。
優點：
- 極其強大的 Java 框架支援，對於企業應用尤為理想。
- 出色的代碼自動完成和重構功能，幫助開發者高效編寫和維護代碼。
- 支援廣泛的插件，能夠擴展到多種語言開發，如 Python、PHP 等。
缺點：
- 資源佔用較大，對於低配備電腦可能運行較慢。
- 免費版（Community Edition）不支援企業功能，如 Java EE 和數據庫工具等，需要購買商業版。
3.3 \*\*PyCharm \*\*
介紹與背景：
PyCharm 是 JetBrains 的另一款 IDE，專注於 Python 開發。由於 Python 在後端開發中廣泛應用於數據分析、人工智慧、網絡應用開發等領域，PyCharm 成為了許多 Python 開發者的首選工具。
主要功能：
- 專為 Python 設計：PyCharm 提供了對 Python 特有的語法自動完成、代碼檢查、以及虛擬環境的內建支援，特別適合開發 Python 後端應用。
- Web 框架整合：對於使用 Django、Flask 等框架的後端開發者來說，PyCharm 提供了強大的整合工具，使得建立、管理及除錯這些應用更加輕鬆。
- 數據庫工具：PyCharm 提供了內建的 SQL 整合工具，使得開發者能夠在 IDE 內管理數據庫，並進行數據查詢與編輯。
- 科學運算支援：內建對 Jupyter Notebook、NumPy、Pandas 等科學運算工具的支援，適合同時進行後端開發與數據分析的開發者。
使用案例：PyCharm 被許多使用 Python 開發後端服務的公司採用，包括 Pinterest、Dropbox 和 Instacart。特別是在數據驅動的後端應用中，PyCharm 的科學運算功能提供了極大的便利。
優點：
- 專為 Python 設計，無縫整合流行的 Python 框架。
- 出色的數據庫管理和除錯工具。
- 強大的測試支持，內建單元測試框架和測試驅動開發工具。
缺點：
- 免費版功能較少，商業版才支援 Django 等框架。
- 對於處理大型專案，可能會有性能瓶頸。
3.4 Eclipse
介紹與背景：
Eclipse 是歷史悠久的開源 IDE，最早由 IBM 開發，後來成為 Eclipse Foundation 的旗艦產品。Eclipse 最初主要針對 Java 開發，現在支援多種編程語言。它擁有龐大的插件庫，可以定製化以支持不同語言、框架和工具。
主要功能：
- 多語言支援：儘管 Eclipse 最初設計用於 Java 開發，但它支援眾多其他語言，如 C/C++、PHP、Python 等，這使其成為多語言開發的強大工具。
- 插件生態系統：Eclipse 擁有豐富的插件生態系統，開發者可以通過 Marketplace 添加需要的功能，如代碼檢查、版本控制及測試框架整合等。
- 大規模專案支持：Eclipse 是一款高度可擴展的 IDE，特別適合用於企業級大型專案的開發和維護。
使用案例：Eclipse 在企業應用開發中廣泛應用，如銀行系統、醫療軟件及大型電子商務平臺開發。許多公司在早期的 Java 專案中採用了 Eclipse，至今仍然是一些傳統企業的重要工具。
優點：
- 支援多種語言和框架，靈活性強。
- 完全免費，對於需要開源解決方案的企業來說是理想選擇。
- 大型專案的穩定性和兼容性高。
缺點：
- 介面相對過時，學習曲線較陡。
- 相比其他現代 IDE（如 IntelliJ），性能稍顯遲緩。
3.5 NetBeans
介紹與背景：
NetBeans 是 Oracle 支持的開源 IDE，最早設
計用於 Java 開發，但也支援 PHP、HTML5 和 C/C++ 等多種語言。它的界面相對簡潔，適合初學者使用，同時對於專業開發者也提供了強大的功能。
主要功能：
- Java 開發支援：NetBeans 內建支援 Java EE、Java SE 以及各種 Java 框架，對於 Java 開發者來說非常方便。
- 自動化工具：NetBeans 提供了強大的代碼重構、代碼生成和語法檢查工具，使得代碼維護更加輕鬆。
- 跨平臺支援：與 VS Code 一樣，NetBeans 支援多種作業系統（Windows、macOS、Linux），使其成為跨平臺開發的理想選擇。
使用案例：NetBeans 主要用於教育環境和企業內部的 Java 應用開發，如政府機構的行政系統、學校的教務系統及中小型企業的業務應用。它的簡單易用性使其在初學者中也有一定的市場。
優點：
- 簡潔的界面，適合新手使用。
- 支援多語言且擴展性強。
- 與 Oracle 產品（如 GlassFish 伺服器）集成度高。
缺點：
- 插件和生態系統不如其他 IDE（如 Eclipse 和 IntelliJ）豐富。
- 在大型專案中，性能表現較差。
補充小節：雲端 IDE 的崛起
隨著開發工具的進步，雲端 IDE 逐漸成為一種趨勢。像 GitHub Codespaces、AWS Cloud9 這樣的雲端 IDE 提供了完整的開發環境，開發者可以直接在瀏覽器中進行代碼編寫和調試，這些工具不僅免去了繁瑣的本地設置，還提高了團隊協作的便利性。隨著企業雲端化進程的加快，這類工具在後端開發中的應用必將越來越廣泛。
\*\*4. 選擇 IDE 時的考量因素 \*\*
在選擇後端開發的 IDE 時，開發者應根據以下幾個方面進行綜合考量：
- 語言及框架支援
- 編譯與調試功能
- 插件及擴展性
- 性能及資源佔用
- 社羣及支援
不同的開發需求會對 IDE 的選擇產生不同影響。例如，對於需要使用多種語言和框架的全端開發者，VS Code 可能更具吸引力；而對於專注於 Java 開發的專業團隊，IntelliJ IDEA 無疑是更合適的選擇。
5. IDE 及後端開發的未來趨勢
隨著技術的進步，未來的 IDE 很可能會朝著自動化、雲端化和協作化的方向發展。自動補全技術將進一步提高代碼編寫的效率，而雲端 IDE 使得開發不再受限於本地硬體資源。此外，遠端協作工具的整合，將使得團隊開發更加流暢。開發者需要隨時關注這些趨勢，以保持在後端開發中的競爭力。
6. 結論
在後端開發中，選擇合適的 IDE 是提升工作效率的關鍵。本筆記比較了 Visual Studio Code、IntelliJ IDEA、PyCharm、Eclipse 及 NetBeans 等主流 IDE，探討了各自的優勢和適用場景。無論是針對初學者還是資深開發者，不同的 IDE 都能根據需求提供適合的工具和功能。隨著技術的發展，開發者應持續探索新的開發工具與技術，以應對不斷變化的軟體開發環境。
Git 工具
1：版本控制基礎
### 1.1 版本控制概念
1.1.1 什麼是版本控制？
版本控制是一種管理計算機文件變化的系統。它允許用戶在不同時間點對文件進行修改、保存和恢復。版本控制系統（VCS）能夠記錄每一次的變更，並且能夠回溯到任意一次變更的歷史版本。
#### 1.1.2 版本控制的重要性
版本控制在軟件開發中非常重要，它能夠帶來以下好處：
1. 歷史記錄：保存所有變更歷史，可以隨時查看或恢復到之前的版本。
2. 協作開發：允許多名開發人員同時對項目進行修改，並且能夠有效管理和合併這些修改。
3. 錯誤修復：在發生錯誤時，可以快速回退到穩定版本。
4. 分支與合併：支持分支開發，讓不同功能可以並行開發，最後合併回主線。
#### 1.1.3 版本控制的類型
版本控制系統主要分為三類：本地版本控制系統、集中式版本控制系統和分散式版本控制系統。
## 本地版本控制系統
本地版本控制系統在本地計算機上管理文件的變更。這種方法簡單，但容易出現版本衝突和數據丟失的問題。
## 集中式版本控制系統
集中式版本控制系統（如 Subversion，SVN）使用單一的中央服務器來保存所有版本的文件，客戶端通過連接到中央服務器進行文件的檢出和提交。這種方法能夠更好地協同工作，但如果中央服務器崩潰，所有歷史數據可能都會丟失。
## 分散式版本控制系統
分散式版本控制系統（如 Git）每個開發者的工作目錄都是一個完整的代碼倉庫，包含所有歷史數據。這種方法提供了更高的靈活性和容錯性，即使某一個倉庫崩潰，也能從其他倉庫恢復數據。
### 1.2 Git 簡介
#### 1.2.1 Git 的歷史和背景
Git 是由 Linus Torvalds 為 Linux 內核開發而創建的分散式版本控制系統。自 2005 年發布以來，Git 已經成為世界上最流行的版本控制系統之一，被廣泛應用於開源和商業項目中。
#### 1.2.2 Git 與其他版本控制系統的比較
Git 與其他版本控制系統相比，具有以下幾個顯著優勢：
1. 速度快：Git 的本地操作速度非常快，因為它在本地倉庫中進行大多數操作，而不是與遠程服務器通信。
2. 分散式：每個開發者都有一個完整的倉庫，這使得 Git 更加靈活和可靠。
3. 高效分支與合併：Git 提供了強大的分支管理功能，能夠輕鬆創建、切換和合併分支。
4. 數據完整性：Git 使用 SHA-1 哈希算法保證數據的完整性，所有數據在存儲時都經過校驗，確保數據不會被意外修改。
#### 1.2.3 安裝 Git
在 Windows 上安裝 Git
1. 下載 Git for Windows 安裝包：Git 官網下載
2. 運行安裝程序，按照提示進行安裝。
3. 打開命令提示符，輸入 git --version 確認安裝成功。
在 macOS 上安裝 Git
1. 打開終端。
2. 使用 Homebrew 安裝 Git :
3. brew install git
4. 輸入 git --version 確認安裝成功。
在 Linux 上安裝 Git
1. 打開終端。
2. 根據不同的 Linux 發行版，使用以下命令安裝 Git：
。在 Debian/Ubuntu 上：
- sudo apt-get update
- sudo apt-get install git
。在 CentOS Stream／Rocky Linux／Fedora 上（CentOS 7 於 2024-06、CentOS 8 於 2021-12 已停止維護）：
- sudo yum install git
3. 輸入 git --version 確認安裝成功。
### 1.3 Git 配置
#### 1.3.1 配置用戶信息
在使用 Git 之前，需要配置用戶信息，這些信息會被記錄在每次提交中。
```
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```
#### 1.3.2 設置文本編輯器
Git 允許用戶設置默認的文本編輯器，當需要編輯提交信息或進行交互式操作時會使用這個編輯器。
```
git config --global core.editor "vim"
```
#### 1.3.3 配置文件 .gitconfig
Git 的配置文件 .gitconfig 位於用戶主目錄下，可以通過編輯這個文件來進行更高級的配置。
常見配置示例
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
### 1.4 Git 基本操作
#### 1.4.1 初始化 Git 倉庫
創建新倉庫
在本地創建一個新的 Git 倉庫：
```
mkdir myproject
cd myproject
git init
```
克隆現有倉庫
從遠程倉庫克隆一個新的倉庫到本地：
```
git clone https://github.com/username/repository.git
```
#### 1.4.2 添加文件到暫存區
將文件添加到暫存區，以便在下一次提交中包括這些更改：
```
git add filename
```
可以使用通配符添加多個文件：
```
git add *.txt
```
#### 1.4.3 提交更改
提交暫存區中的更改，並添加提交信息：
git commit -m "提交信息"
如果希望在提交時編輯提交信息，可以省略 -m 選項：
```
git commit
```
#### 1.4.4 查看狀態
使用 git status 命令可以查看當前工作目錄的狀態，包括已修改但未提交的文件、未跟蹤的文件等：
```
git status
```
#### 1.4.5 檢查日誌
使用 git log 命令可以查看提交歷史：
```
git log
```
可以使用 --oneline 選項簡化輸出：
```
git log --oneline
```
### 1.5 分支管理
#### 1.5.1 分支概念
為什麼使用分支？
分支允許開發者在同一個代碼庫中同時開發多個功能或修復多個問題，而不會互相干擾。每個分支都是代碼庫的一個獨立副本，可以自由地進行修改，最後再合併到主分支中。
分支的優勢
1. 並行開發：多個開發者可以在不同分支上同時工作，提高開發效率。
2. 隔離風險：新功能和修復在獨立的分支上開發，不會影響穩定的主分支。
3. 版本控制：可以輕鬆回溯到某一特定分支的狀態，方便進行版本管理。
#### 1.5.2 分支操作
創建分支
創建新分支並切換到該分支：
```
git checkout -b new-branch
```
切換分支
切換到已存在的分支：
```
git checkout branch-name
```
## 合併分支
將另一個分支的更改合併到當前分支：
```
git merge branch-name
```
## 解決合併衝突
在合併過程中，可能會遇到衝突，需要手動解決。解決衝突後，使用 git add 添加解決衝突的文件，然後提交：
```
git add resolved-file
```
git commit -m "解決合併衝突"
### 1.6 遠程倉庫
#### 1.6.1 遠程倉庫概念
什麼是遠程倉庫？
遠程倉庫是託管在服務器上的 Git 倉庫，允許多名開發者通過網絡進行協作開發。遠程倉庫通常託管在平臺如 GitHub、GitLab 或 Bitbucket 上。
## 本地倉庫與遠程倉庫的區別
本地倉庫僅存儲在開發者的計算機上，遠程倉庫則存儲在服務器上，並且可以被多名開發者訪問。本地倉庫的操作不會影響遠程倉庫，只有在推送更改時，遠程倉庫才會更新。
#### 1.6.2 遠程操作
添加遠程倉庫
將遠程倉庫添加到本地倉庫：
```
git remote add origin https://github.com/username/repository.git
```
推送更改到遠程倉庫
將本地倉庫的更改推送到遠程倉庫：
```
git push origin branch-name
```
拉取遠程倉庫的更新
從遠程倉庫拉取最新的更改到本地倉庫：
```
git pull origin branch-name
```
同步遠程分支
同步本地和遠程分支列表：
```
git fetch
```
### 1.7 Git 的常見工作流程
#### 1.7.1 Feature 分支工作流程
Feature 分支工作流程是一種常見的 Git 工作流程，用於開發新功能。
1. 從主分支創建一個新功能分支。
2. 在新功能分支上開發功能。
3. 完成功能後，將新功能分支合併回主分支。
4. 刪除新功能分支。
```
git checkout main
git checkout -b new-feature
# 開發新功能
git add.
```
git commit -m "添加新功能"
```
git checkout main
git merge new-feature
git branch -d new-feature
```
#### 1.7.2 Git Flow 工作流程
Git Flow 是一種複雜的工作流程，適用於大型項目，具有嚴格的分支管理策略。
1. 使用主分支（master）和開發分支（develop）。（時代註記：GitHub 自 2020 年起新倉庫預設分支名為 `main`，原理相同。）
2. 每個新功能在 develop 分支上創建一個 feature 分支。
3. 完成功能後，將 feature 分支合併回 develop 分支。
4. 釋出新版本時，從 develop 分支創建一個 release 分支，進行最後的測試和修復。
5. 確認 release 分支穩定後，合併到 master 分支，並創建一個標籤。
6. 如果發現重大錯誤，從 master 分支創建 hotfix 分支，修復後合併回 master 和 develop 分支。
### 1.8 Git 的常見命令和技巧
#### 1.8.1 刪除文件
從工作目錄和暫存區中刪除文件：
```
git rm filename
```
git commit -m "刪除文件"只從暫存區中刪除文件，保留工作目錄中的文件：
```
git rm --cached filename
```
git commit -m "從暫存區中刪除文件"
#### 1.8.2 移動或重命名文件
移動或重命名文件，並提交更改：
```
git mv old-filename new-filename
```
git commit -m "重命名文件"
#### 1.8.3 查看分支
查看本地和遠程分支：
```
git branch -a
```
1.8.4 合併沒有快進 (No Fast-Forward) 的分支
在合併時使用 --no-ff 選項，強制創建一個新的提交，保留分支歷史：
```
git merge --no-ff branch-name
```
#### 1.8.5 生成補丁文件
生成一個包含更改的補丁文件：
```
git diff > patch-file.patch
```
應用補丁文件：
```
git apply patch-file.patch
```
#### 1.8.6 忽略文件
在倉庫根目錄創建 .gitignore 文件，指定要忽略的文件和目錄：
```
# 忽略所有 .log 文件
```
*.log
```
# 忽略 node_modules 目錄
node_modules/
```
### 1.9 GitHub 和 GitLab 簡介
1.9.1 GitHub
GitHub 是世界上最大的代碼託管平臺，提供基於 Git 的版本控制服務。GitHub 還提供許多協作功能，如 Pull Request、Issues 和 Actions 等，幫助開發者更好地協同工作。
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
1.9.2 GitLab
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
### 1.10 Git 的常見問題和解決方案
#### 1.10.1 回滾提交
撤銷最近一次提交，但保留更改
使用 git reset 命令撤銷最近一次提交，但保留更改在工作目錄中：
```
git reset --soft HEAD~1
```
## 完全撤銷最近一次提交和更改
使用 git reset 命令撤銷最近一次提交和更改：
```
git reset --hard HEAD~1
```
#### 1.10.2 撤銷已提交的文件
如果錯誤地提交了一些文件，可以使用 git reset 將這些文件從提交中移除：
```
git reset HEAD^
git add files-to-keep
```
git commit -m "撤銷錯誤提交"
#### 1.10.3 修復錯誤的提交信息
如果提交信息有誤，可以使用 git commit --amend 來修改最近一次提交的信息：
git commit --amend -m "新的提交信息"
#### 1.10.4 回溯歷史版本
如果需要回溯到某個歷史版本，可以使用 git checkout 命令：
```
git checkout commit-hash
```
回到最新版本：
```
git checkout main
```
#### 1.10.5 解決合併衝突
合併過程中，如果出現衝突，需要手動解決。解決衝突後，使用 git add 添加解決衝突的文件，然後提交：
```
git add resolved-file
```
git commit -m "解決合併衝突"
### 1.11 Git 的進階技巧
#### 1.11.1 使用 Git Alias
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
使用別名命令：
```
git st
git co branch-name
```
git ci -m "提交信息"
#### 1.11.2 使用 Git Hooks
## Git Hooks 是在
特定事件發生時自動執行的腳本。常見的 hooks 包括 pre-commit、pre-push 和 post-commit 等。
## 配置 Hook
在倉庫的 .git/hooks 目錄中創建 hook 腳本，例如 pre-commit：
```
#!/bin/sh
# pre-commit hook example
echo "Running pre-commit hook"
./run-tests.sh
```
啟用 Hook
給腳本添加可執行權限：
```
chmod +x .git/hooks/pre-commit
```
#### 1.11.3 使用 Git Submodules
Git Submodules 是 Git 倉庫中的子倉庫，適用於包含外部依賴的情況。
添加子模組
在主倉庫中添加子模組：
```
git submodule add https://github.com/username/submodule-repo.git path/to/submodule
```
初始化和更新子模組
克隆倉庫後，初始化和更新子模組：
```
git submodule init
git submodule update
```
## 小結
本章介紹了版本控制的基本概念，Git 的簡介和安裝，Git 的基本操作，分支管理，遠程倉庫操作，以及一些常見的工作流程和命令。這些知識為後續深入學習 Git 打下了堅實的基礎。
2: Git 基本操作
### 2.1 Git 配置
#### 2.1.1 配置用戶信息
在使用 Git 之前，首先需要配置用戶信息。這些信息會被記錄在每次提交中，幫助你和其他協作者瞭解每次更改的來源。
```
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```
#### 2.1.2 設置文本編輯器
Git 允許用戶設置默認的文本編輯器，當需要編輯提交信息或進行交互式操作時會使用這個編輯器。
```
git config --global core.editor "vim"
```
#### 2.1.3 配置文件 .gitconfig
Git 的配置文件 .gitconfig 位於用戶主目錄下，可以通過編輯這個文件來進行更高級的配置。
## 常見配置示例
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
### 2.2 初始操作
#### 2.2.1 初始化 Git 倉庫
在本地創建一個新的 Git 倉庫：
```
mkdir myproject
cd myproject
git init
```
此命令會在當前目錄下創建一個名為 .git 的隱藏目錄，這個目錄包含了所有 Git 所需的倉庫文件。
#### 2.2.2 克隆現有倉庫
從遠程倉庫克隆一個新的倉庫到本地：
```
git clone https://github.com/username/repository.git
```
此命令會在當前目錄下創建一個名為 repository 的目錄，並將遠程倉庫中的所有內容下載到該目錄中。
### 2.3 基本命令
#### 2.3.1 添加文件到暫存區
將文件添加到暫存區，以便在下一次提交中包括這些更改：
```
git add filename
```
可以使用通配符添加多個文件：
```
git add *.txt
```
#### 2.3.2 提交更改
提交暫存區中的更改，並添加提交信息：
git commit -m "提交信息"
如果希望在提交時編輯提交信息，可以省略 -m 選項：
```
git commit
```
#### 2.3.3 查看狀態
使用 git status 命令可以查看當前工作目錄的狀態，包括已修改但未提交的文件、未跟蹤的文件等：
```
git status
```
#### 2.3.4 檢查日誌
使用 git log 命令可以查看提交歷史：
```
git log
```
可以使用 --oneline 選項簡化輸出：
```
git log --oneline
```
#### 2.3.5 比較文件差異
使用 git diff 命令可以比較文件的不同版本之間的差異：
```
git diff
```
比較工作目錄和暫存區之間的差異：
```
git diff --staged
```
### 2.4 分支管理
#### 2.4.1 創建分支
創建新分支並切換到該分支：
```
git checkout -b new-branch
```
這個命令等同於以下兩個命令的組合：
```
git branch new-branch
git checkout new-branch
```
#### 2.4.2 切換分支
切換到已存在的分支：
```
git checkout branch-name
```
#### 2.4.3 合併分支
將另一個分支的更改合併到當前分支：
```
git merge branch-name
```
#### 2.4.4 解決合併衝突
在合併過程中，可能會遇到衝突，需要手動解決。解決衝突後，使用 git add 添加解決衝突的文件，然後提交：
```
git add resolved-file
```
git commit -m "解決合併衝突"
### 2.5 遠程倉庫
#### 2.5.1 添加遠程倉庫
將遠程倉庫添加到本地倉庫：
```
git remote add origin https://github.com/username/repository.git
```
#### 2.5.2 推送更改到遠程倉庫
將本地倉庫的更改推送到遠程倉庫：
```
git push origin branch-name
```
#### 2.5.3 拉取遠程倉庫的更新
從遠程倉庫拉取最新的更改到本地倉庫：
```
git pull origin branch-name
```
#### 2.5.4 同步遠程分支
同步本地和遠程分支列表：
```
git fetch
```
### 2.6 標籤管理
#### 2.6.1 創建標籤
創建輕量標籤：
```
git tag tag-name
```
創建帶有註釋的標籤：
git tag -a tag-name -m "標籤描述"
#### 2.6.2 查看標籤
查看所有標籤：
```
git tag
```
#### 2.6.3 刪除標籤
刪除本地標籤：
```
git tag -d tag-name
```
刪除遠程標籤：
```
git push origin :refs/tags/tag-name
```
#### 2.6.4 推送標籤到遠程倉庫
將標籤推送到遠程倉庫：
```
git push origin tag-name
```
一次性推送所有標籤：
```
git push origin --tags
```
### 2.7 Git 忽略文件
#### 2.7.1 使用 .gitignore 文件
在倉庫根目錄創建 .gitignore 文件，指定要忽略的文件和目錄：
```
# 忽略所有 .log 文件
```
*.log
```
# 忽略 node_modules 目錄
node_modules/
# 忽略特定文件
secret.txt
```
#### 2.7.2 檢查忽略文件
檢查 .gitignore 文件是否生效：
```
git status
```
如果文件仍然出現在 git status 的輸出中，確保這些文件沒有被添加到暫存區或已被提交。
### 2.8 撤銷和回滾操作
#### 2.8.1 撤銷修改
撤銷工作目錄中的修改：
```
git checkout -- filename
```
#### 2.8.2 撤銷已添加到暫存區的文件
撤銷暫存區中的文件，但保留工作目錄中的修改：
```
git reset HEAD filename
```
#### 2.8.3 回滾提交
撤銷最近一次提交，但保留更改在工作目錄中：
```
git reset --soft HEAD~1
```
完全撤銷最近一次提交和更改：
```
git reset --hard HEAD~1
```
#### 2.8.4 使用 revert 命令回滾提交
回滾特定提交，並創建一個新的提交來記錄這一操作：
```
git revert commit-hash
```
### 2.9 使用 Stash
#### 2.9.1 保存工作進度
使用 git stash 保存當前的工作進度，以便稍後恢復：
```
git stash
```
#### 2.9.2 查看 Stash 列表
查看已保存的工作進度列表：
```
git stash list
```
#### 2.9.3 恢復工作進度
恢復最近一次保存的工作進度：
```
git stash apply
```
恢復並刪除最近一次保存的工作進度：
```
git stash pop
```
#### 2.9.4 刪除 Stash
刪除指定的工作進度：
```
git stash drop stash@{0}
```
刪除所有保存的工作進度：
```
git stash clear
```
### 2.10 比較和分析
#### 2.10.1 比較提交之間的差異
使用 git diff 比較兩個提交之間的差異：
```
git diff commit1 commit2
```
#### 2.10.2 查看提交歷史
使用 git log 查看提交歷史：
```
git log
```
顯示每個提交的差異：
```
git log -p
```
#### 2.10.3 查看文件的變更歷史
使用 git blame 查看文件的變更歷史，顯示每一行代碼的最後修改者：
```
git blame filename
```
#### 2.10.4 使用 git bisect 查找問題提交
使用 git bisect 查找引入問題的提交：
```
git bisect start
git bisect bad HEAD
git bisect good commit-hash
```
然後，Git 會自動切換到不同的提交，直到找到引入問題的提交。當找到問題提交時，結束二分查找：
```
git bisect reset
```
### 2.11 Git 的日常工作流程
#### 2.11.1 克隆遠程倉庫
從遠程倉庫克隆項目到本地：
```
git clone https://github.com/username/repository.git
```
#### 2.11.2 創建和切換分支
創建一個新分支並切換到該分支：
```
git checkout -b new-branch
```
#### 2.11.3 提交更改
添加修改到暫存區並提交：
```
git add.
```
git commit -m "描述你的更改"
#### 2.11.4 推送和拉取
將本地分支推送到遠程倉庫：
```
git push origin new-branch
```
從遠程倉庫拉取最新的更改：
```
git pull origin main
```
#### 2.11.5 合併分支
將新分支合併到主分支：
```
git checkout main
git merge new-branch
```
### 2.12 Git 的高級功能
#### 2.12.1 使用子模組
Git 子模組允許你將一個 Git 倉庫作爲另一個 Git 倉庫的子目錄。
添加子模組
```
git submodule add https://github.com/username/submodule-repo.git path/to/submodule
```
初始化和更新子模組
克隆倉庫後，初始化和更新子模組：
```
git submodule init
git submodule update
```
#### 2.12.2 使用鉤子 (Hooks)
Git 鉤子是腳本，在特定事件發生時自動執行。
配置鉤子
在 .git/hooks 目錄中創建鉤子腳本，例如 pre-commit：
```
#!/bin/sh
# pre-commit hook example
echo "Running pre-commit hook"
./run-tests.sh
```
啟用鉤子
給腳本添加可執行權限：
```
chmod +x .git/hooks/pre-commit
```
### 2.13 Git 的最佳實踐
#### 2.13.1 撰寫良好的提交信息
良好的提交信息有助於協作者理解更改的原因和內容。
提交信息格式
提交信息應該包括以下幾部分：
1. 標題：簡要描述更改，不超過 50 個字符。
2. 正文：詳細描述更改，解釋原因和實施方法。
提交信息示例
## 修復登錄頁面崩潰問題
當用戶輸入錯誤的憑據時，登錄頁面會崩潰。這是由於一個未捕獲的異常引起的。添加了異常處理邏輯，確保頁面不會崩潰，並顯示適當的錯誤信息。
#### 2.13.2 保持提交歷史簡潔
保持提交歷史簡潔，避免無意義的提交信息，有助於理解項目的演變過程。
使用 rebase 清理歷史
使用 rebase 命令清理提交歷史：
```
git rebase -i HEAD~n
```
然後，在交互式界面中選擇要修改或合併的提交。
#### 2.13.3 使用標籤管理版本
使用標籤來標記項目的重要里程碑，如發布新版本。
創建標籤
```
git tag v1.0.0
```
推送標籤到遠程倉庫
```
git push origin v1.0.0
```
## 小結
本章介紹了 Git 的基本操作，包括配置、初始操作、基本命令、分支管理、遠程倉庫、標籤管理、忽略文件、撤銷和回滾操作、使用 Stash、比較和分析、日常工作流程、高級功能和最佳實踐。這些內容幫助你掌握了 Git 的基本使用方法和常見操作，為進一步深入學習和使用 Git 打下了堅實的基礎。
3：分支管理
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
