# 第 7 章 · Django 基礎與環境建置

## 1. Django 基礎

### 1.1 使用 Django 建立開發環境

Django 是一個開源的 Python Web 框架，旨在讓開發過程變得更快捷且更方便維護。Django 強調重用性、低耦合、快速開發，以及 "Don't Repeat Yourself" (DRY) 的開發理念。這使得開發者能夠專注於應用邏輯，而不是解決低層次的細節問題，如 SQL 查詢的編寫或表單驗證。

Django 最初由新聞網站的開發團隊設計，針對的是需要快速部署、修改頻繁且穩定性要求高的新聞內容管理系統。隨著時間推移，Django 被廣泛應用於不同類型的 Web 應用開發，如社交網絡、電子商務平臺、內容管理系統等。

#### 1.1.1 Django 的主要特點

1. 快速開發

Django 的高層次抽象使得 Web 開發變得非常迅速。無論是處理表單、驗證數據，還是設計後臺管理系統，Django 提供了一整套高效工具來處理這些常見的需求。

2. 完全功能的管理介面

Django 內建了一個強大且可擴展的管理介面，使得網站管理員可以輕鬆管理網站內容。開發者只需定義模型，Django 就會自動生成對應的管理界面，這在開發 CMS （內容管理系統）時特別有用。

3. 豐富的庫與模組

Django 內建了眾多強大的工具和功能模組，如 ORM（對象關聯映射）、模板引擎、表單處理、URL 路由、驗證系統等等。此外，Django 社羣也非常活躍，提供了大量擴展和第三方模組來補充 Django 的原生功能。

4. 安全性

Django 提供了防範常見 Web 安全威脅的內建功能，如防止 SQL 注入、跨站腳本攻擊 (XSS)、跨站請求偽造 (CSRF) 等，保護網站免受攻擊。

5. 可擴展性

Django 的模組化設計使得它易於擴展和修改。無論是增加新的功能模塊，還是自定義框架的行為，Django 都能夠靈活適應。

### 1.2 使用 Django 進行基本開發 (MVT 框架)

在學習 Django 之前，我們需要了解其架構模式。許多 Web 框架使用 MVC（Model-View-Controller）架構，Django 則使用一種叫做 MVT（Model-View-Template）的變體架構。

#### 1.2.1 MVC 架構

MVC 是一種軟體設計模式，用來將應用程序分成三個主要部分：

- Model（模型）：負責數據邏輯和資料庫的互動。

- View（視圖）：處理顯示邏輯，呈現數據給用戶。

- Controller（控制器）：負責接受輸入並將其轉發給相應的模型和視圖。

#### 1.2.2 MVT 架構

在 Django 中，MVT 架構替代了傳統的 MVC 架構：

- Model（模型）：同樣負責數據邏輯和與資料庫的互動。Django 的 ORM（對象關聯映射）允許開發者使用 Python 對象來進行數據庫操作，而無需直接編寫 SQL。

- View（視圖）：處理業務邏輯，從模型中獲取數據並將其傳遞給模板渲染。

- Template（模板）：負責數據的顯示邏輯，將動態內容呈現在靜態 HTML 頁面中。

## Django 中 MVT 的具體角色

1. Model：定義了應用的數據結構，並與資料庫直接互動。你可以在模型中定義字段和方法，來確保數據的完整性。

2. View：處理應用邏輯，根據用戶的請求，從模型中獲取數據並將其傳遞給模板。視圖是控制應用業務流程的核心。

3. Template：負責將視圖傳遞過來的數據渲染成 HTML，並發送給用戶的瀏覽器。

## Django 中的 URL 路由器

在傳統的 MVC 架構中，控制器負責接受用戶的輸入並選擇相應的視圖。在 Django 中，這一功能被 URLConf（URL 配置）取代。Django 使用 URLConf 來定義 URL 模式，並將不同的 URL 分派給相應的視圖函數。

### 1.3 Django 的優勢與應用場景

Django 的設計目標是簡化 Web 應用開發，無論是個人網站還是大型企業應用，它都能勝任。以下列出 Django 的一些應用場景以及其在不同領域的優勢。

#### 1.3.1 Django 的優勢

1. 高效開發

Django 將開發中常見的任務，如數據庫操作、表單驗證、用戶認證等，進行高度封裝，開發者無需從零開始實現這些功能。這極大地提升了開發效率，讓開發者能在短時間內構建穩定的應用。

2. 全面的文檔

Django 擁有非常詳細且完整的官方文檔，涵蓋了從安裝、配置到高級功能的所有方面，這對於新手來說非常友好，也有助於解決開發中遇到的問題。

3. 大規模社羣支持

Django 擁有一個龐大且活躍的開發者社羣，社羣成員會定期分享擴展功能、解決常見問題，並開發許多第三方包以增強 Django 的功能。這意味著開發者能輕鬆找到解決方案，並可利用社羣資源來加速開發進度。

4. 高安全性

Django 默認集成了多種安全功能，避免開發者犯下常見的安全錯誤，這讓 Django 特別適合於對安全性要求高的項目，如銀行、電子商務等。

#### 1.3.2 Django 的應用場景

1. 內容管理系統 (CMS)

許多內容驅動型網站，如新聞網站或博客系統，都使用 Django 來處理大規模的內容創建、管理與發布。Django 的管理介面能快速搭建出一個功能齊全的後臺管理系統，便於管理文章、標籤、分類等內容。

2. 電子商務平臺

Django 的 ORM 和強大的資料庫處理功能，使得它成為構建電子商務平臺的理想選擇。從管理產品、訂單、付款到處理用戶帳戶和物流，Django 能夠快速應對電子商務開發中的多種需求。

3. 社交網絡

Django 可以用來開發複雜的社交網絡，處理大量用戶生成的內容、消息推送、實時通信等。其擴展性使得開發者能輕鬆實現用戶關係、動態、消息系統等功能。

4. 學術與研究網站

許多教育機構、研究組織選擇使用 Django 來開發學術資源平臺。Django 的靈活性和高效開發特性，讓開發者可以迅速構建功能完善的學術系統，並處理大規模數據。

5. 數據分析與視覺化

由於 Django 與 Python 完美整合，開發者可以使用 Django 作為數據分析應用的後端框架，並結合 Python 的數據科學庫如 Pandas、NumPy 來進行數據處理與分析，實現強大的數據可視化功能。

### 1.4 Django 的社羣與資源

作為一個成熟且受歡迎的框架，Django 擁有豐富的資源和社羣支持。無論是初學者還是經驗豐富的開發者，都可以從這些資源中受益，進一步提升開發技能。

#### 1.4.1 官方文檔

Django 的官方文檔是學習框架最重要的資源之一。官方文檔提供了清晰的 API 說明、入門指南，以及詳細的功能講解，這對於解決開發中的各類問題非常有幫助。

官方文檔網址： $ \underline{\text{https://docs.djangoproject.com/zh-hans/stable/}} $

#### 1.4.2 社羣論壇與線上資源

Django 擁有活躍的社羣論壇，開發者可以在這些論壇上提出問題、分享經驗，並參與到社羣的討論中。以下是幾個受歡迎的 Django 社羣資源：

- StackOverflow : Django 相關的提問和回答是 StackOverflow 上最活躍的 Python 相關話題之一。

- Django 社羣論壇：提供了專門的 Django 討論區，讓開發者能相互交流和學習。

#### 1.4.3 第三方擴展包

Django 的第三方擴展包極為豐富，幾乎可以滿足所有的開發需求。從用戶驗證到 API 開發，這些包都經過社羣驗證，能快速集成到你的應用中。

#### 1.4.4 Django 的版本更新

Django 團隊保持定期更新框架版本，以解決已知的漏洞和提升性能。建議開發者定期檢查並升級至最新的穩定版本，以保持項目安全性與兼容性。

2：設置開發環境

### 2.1 準備工作

在開始 Django 開發之前，我們需要為開發設置適當的環境，這包括安裝所需的軟件和配置虛擬環境。本章將帶領你逐步完成這些操作，並開始你的第一個 Django 專案。

#### 2.1.1 安裝 Python

Django 是基於 Python 的框架，因此第一步是安裝 Python。你需要檢查你的電腦是否已安裝了正確版本的 Python。Django 5.2 支援 Python 3.10 至 3.14，建議安裝 Python 3.14 的最新版本；Python 3.10 已於 2026 年 10 月停止支援，Python 3.15 目前未列入 Django 5.2 的支援範圍。

## 檢查 Python 安裝

在 macOS 和 Linux 系統上，打開終端（Terminal），輸入以下命令：

```
python3 --version
```
在 Windows 系統上，打開命令提示符（Command Prompt），輸入：

```
python --version
```
若顯示的 Python 版本為 3.x.x，即表示已安裝正確版本。如果沒有安裝，請前往 Python 官方網站 下載並安裝最新的 Python 3.x 版本。

## 安裝 Python

1. 進入 Python 官方下載頁面。

2. 根據你的作業系統選擇相應的版本。

3. 安裝時，請勾選 "Add Python to PATH" 選項，以確保可以在命令行中直接調用 python 命令。

#### 2.1.2 安裝 pip

pip 是 Python 的包管理工具，用來安裝、更新和管理 Python 軟件包。通常，Python 3.x 自帶 pip。你可以通過以下命令檢查 pip 是否已安裝：

```
pip --version
```
若未安裝 pip，可參考官方指引安裝：

pip 官方安裝指引

### 2.2 安裝 Django

在安裝好 Python 和 pip 之後，我們便可以安裝 Django。Django 可以通過 pip 進行安裝，這是最常見也是推薦的方式。

#### 2.2.1 Django 版本選擇

Django 團隊會定期發布功能版本與 LTS（長期支持）版本。本課程以 Django 5.2 LTS 為準：2025 年 4 月 2 日發布，安全支援至 2028 年 4 月，支援 Python 3.10 至 3.14。生產環境建議使用 LTS 版本，想試用新功能才安裝最新的功能版本；不論哪一種，都應使用該系列最新的補丁版本。

#### 2.2.2 使用 pip 安裝 Django

在終端或命令提示符中執行以下命令來安裝 Django 5.2 LTS 的最新補丁版本（需要 Python 3.10 或以上）：

```
pip install "django~=5.2"
```
若需要固定 5.2 系列的版本，可以指定版本號，例如：

```
pip install "django==5.2.*"
```
確認 Django 安裝成功

安裝完成後，可以輸入以下命令來檢查 Django 是否安裝成功，並顯示版本號：

```
django-admin --version
```
### 2.3 建立虛擬環境

虛擬環境是一個獨立的 Python 執行環境，它允許你在不同的專案中使用不同版本的 Python 和套件，避免衝突。Django 開發通常推薦使用虛擬環境。

#### 2.3.1 安裝虛擬環境工具

Python 提供內建的 venv 工具來建立虛擬環境。你可以通過以下命令檢查 venv 是否可用：

```
python3 -m venv --help
```
如果沒有問題，就可以使用 venv 來創建虛擬環境。

#### 2.3.2 建立虛擬環境

在你的專案目錄下（如 myproject/），創建虛擬環境：

```
python3 -m venv venv
```
這會在當前目錄下創建一個名為 venv 的虛擬環境文件夾，該文件夾包含了獨立的 Python 執行環境和包管理工具。

#### 2.3.3 啟動虛擬環境

在 macOS 和 Linux 系統上，使用以下命令啟動虛擬環境：

```
source venv/bin/activate
```
在 Windows 系統上，使用以下命令啟動虛擬環境：

```
venv\Scripts\activate
```
啟動虛擬環境後，你的終端提示符會變成類似（venv），表示目前正處於虛擬環境中。

停用虛擬環境

當你完成工作並想退出虛擬環境時，輸入以下命令：

```
deactivate
```
### 2.4 創建第一個 Django 專案

現在我們已經準備好開發環境，接下來將創建第一個 Django 專案，並運行一個簡單的 Web 伺服器來檢視結果。

#### 2.4.1 使用 django-admin 創建專案

Django 提供了 django-admin 工具，用來創建和管理 Django 專案。在虛擬環境啟動的狀態下，執行以下命令創建新專案：

```
django-admin startproject myproject
```
這會創建一個名為 myproject 的新 Django 專案，內部包含以下基本結構：

```
myproject/
manage.py
myproject/
__init__.py
settings.py
urls.py
asgi.py
wsgi.py
```
manage.py：一個實用命令行工具，用於與 Django 專案互動。

settings.py：專案的設置與配置文件。

urls.py：負責 URL 路由配置。

asgi.py / wsgi.py : Django 的 ASGI 和 WSGI 伺服器入口文件。

#### 2.4.2 運行開發伺服器

進入專案目錄後，使用 manage.py 命令運行 Django 開發伺服器：

```
python manage.py runserver
```
你將看到以下輸出：

```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
September 15, 2024 - 12:45:08
Django version 5.2.19, using settings 'myproject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
打開瀏覽器，訪問 http://127.0.0.1:8000/，你應該能看到 Django 的歡迎頁面，這說明 Django 開發伺服器已成功運行。

### 2.5 Django 專案結構詳解

Django 自動生成的專案結構包含了一些關鍵文件和文件夾，我們將逐一解釋這些文件的用途。

2.5.1 manage.py

manage.py 是 Django 的命令行工具，用於執行各種管理命令，如啟動伺服器、遷移資料庫、創建應用等。你可以通過以下命令查看 manage.py 支持的所有命令：

```
python manage.py --help
```
常用命令包括：

- runserver：啟動開發伺服器。

- migrate：執行資料庫遷移。

- createsuperuser：創建超級用戶（管理員帳戶）。

- startapp：創建一個新的 Django 應用。

2.5.2 settings.py

settings.py 是 Django 專案的配置文件，定義了數據庫配置、應用列表、中間件、模板路徑等。在開發過程中，你將頻繁修改這個文件來配置你的專案。

## 關鍵配置項目

- DEBUG：設置為 True，表示處於開發模式，將顯示詳細的錯誤信息。發布到生產環境時應設置為 False。

\*\*ALLOWED

HOSTS\*\*：定義允許訪問 Django 應用的域名列表。在開發環境下通常設置為空列表，但在生產環境中必須指定具體的域名。

INSTALLED_APPS：列出所有已安裝並啟用的 Django 應用。你將會在此處添加自定義應用或第三方擴展包。

MIDDLEWARE：列出所有啟用的中間件。中間件是處理請求和響應的過程中應用的一些處理程序。你可以在這裡啟用或禁用某些功能，如會話管理、CSRF保護等。

TEMPLATES：定義模板引擎的設置。這部分配置負責告訴 Django 在哪裡查找 HTML 模板文件。

DATABASES：設置資料庫配置，默認使用 SQLite 資料庫。你可以修改這裡來切換至 MySQL、PostgreSQL 等其他資料庫。

2.5.3 urls.py

urls.py 負責處理 URL 路由配置。在這個文件中，你可以定義 URL 與視圖的對應關係。每當用戶請求一個 URL，Django 會通過這個文件來判斷應該調用哪個視圖來處理請求。

2.5.4 asgi.py / wsgi.py

這兩個文件是 Django 專案的伺服器入口點，分別用於 ASGI（Asynchronous Server Gateway Interface）和 WSGI（Web Server Gateway Interface）。在大多數情況下，你不需要修改這些文件。

wsgi.py 用於標準的同步應用。

asgi.py 用於支援異步功能的應用，如 WebSocket。

### 2.6 常見問題與錯誤排查

即使按照正確步驟設置環境和創建專案，你仍可能遇到一些常見錯誤或問題。這裡列出了一些常見問題及其解決方案。

2.6.1 問題：伺服器無法啟動

原因 1: Django 未安裝

解決方案：檢查是否在虛擬環境中運行，並且 Django 是否正確安裝。嘗試重新安裝 Django：

```
pip install "django~=5.2"
```
原因 2：端口被佔用

解決方案：如果 8000 端口被其他應用佔用，可以指定其他端口來啟動伺服器：

```
python manage.py runserver 8080
```
2.6.2 問題：無法訪問伺服器

原因：ALLOWED_HOSTS 配置錯誤

解決方案：在 settings.py 中，確保 ALLOWED_HOSTS 列表包含本地主機 IP 地址：

```
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```
3: Django 中的 Project 與 App，配置 settings.py 和 manage.py 命令

在 Django 框架中，Project（項目）和 App（應用）是兩個基本概念。理解這兩者之間的區別對於構建高效、可擴展的應用程序至關重要。此外，Django 提供了靈活的配置系統，通過 settings.py 文件來管理項目的全局設置，同時提供了 manage.py 命令來管理和運行開發相關的任務。本章將詳細介紹 Project 和 App 之間的區別，配置 settings.py，以及 常見的 manage.py 命令 和它們的使用場景。
