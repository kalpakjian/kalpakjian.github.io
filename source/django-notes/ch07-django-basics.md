# 第 7 章 · Django 基礎與環境建置

## 1. Django 基礎

### 1.1 什麼是 Django

Django 是開源的 Python Web 框架，主打**快速開發、易維護、可重用、低耦合**，遵循 DRY（Don't Repeat Yourself）。它把常見工作（資料庫、表單驗證、認證等）都封裝好，讓開發者專注在應用邏輯。最初為新聞網站設計，現廣泛用於社交、電商、CMS 等。

**主要特點**

- **快速開發**：高階抽象，處理表單、驗證、後台都很省事。
- **內建管理介面**：定義好模型即自動產生後台，特別適合 CMS。
- **豐富的庫與模組**：ORM、模板引擎、表單、URL 路由、驗證等，社群龐大。
- **安全性**：內建防 SQL 注入、XSS、CSRF 等。
- **可擴展**：模組化設計，易於擴充與客製。

### 1.2 MVT 架構

Django 採用 **MVT（Model-View-Template）**，是 MVC 的變體。

<figure class="fig-svg"><svg viewBox="0 0 860 250" width="100%" role="img" aria-label="Django MVT 架構：瀏覽器、URL 路由、視圖、模型、模板與資料庫的關係" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="90" width="130" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="85" y="115" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">瀏覽器</text><text x="85" y="135" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">發送請求</text><rect x="190" y="90" width="130" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="255" y="115" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">urls.py</text><text x="255" y="135" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">URL 路由</text><rect x="360" y="20" width="130" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="425" y="45" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">View 視圖</text><text x="425" y="65" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">業務邏輯</text><rect x="360" y="160" width="130" height="62" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="425" y="185" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">Template</text><text x="425" y="205" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">模板渲染</text><rect x="540" y="20" width="130" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="605" y="45" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">Model 模型</text><text x="605" y="65" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">ORM</text><rect x="720" y="20" width="120" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="780" y="45" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">資料庫</text><text x="780" y="65" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">SQLite／PG</text><line x1="150" y1="121" x2="186" y2="121" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="320" y1="105" x2="356" y2="62" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="490" y1="51" x2="536" y2="51" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="670" y1="51" x2="716" y2="51" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="720" y1="70" x2="490" y2="70" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="425" y1="82" x2="425" y2="156" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="360" y1="191" x2="154" y2="155" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="700" y="118" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">查詢結果</text><text x="440" y="122" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#f0a04b">HTML</text></svg><figcaption>圖 1　Django 的 MVT 架構：請求經 URL 路由進入視圖，視圖透過模型存取資料庫，再把資料交給模板渲染成 HTML。</figcaption></figure>

| 職責 | MVC | Django MVT |
| --- | --- | --- |
| 資料 | Model | **Model**：資料結構與資料庫互動（透過 ORM，不必寫 SQL） |
| 顯示 | View | **Template**：把資料渲染成 HTML |
| 控制 | Controller | **View**：處理業務邏輯，取資料交給 Template；URL 分派由 **URLConf（urls.py）** 負責 |

- **Model**：定義資料結構，與資料庫互動。
- **View**：處理請求邏輯，從 Model 取資料交給 Template。
- **Template**：把資料渲染成 HTML 回傳給瀏覽器。
- **URL 路由器（urls.py）**：把不同 URL 分派給對應的 View。

### 1.3 優勢與應用場景

**優勢**

- **高效開發**：常用功能已封裝，不必從零實作。
- **文件完整**：官方文檔詳盡，對新手友善。
- **社群龐大**：第三方套件豐富，問題容易找到解答。
- **高安全性**：內建多種安全機制，適合金融、電商等高要求場景。

**應用場景**

- **內容管理系統（CMS）**：新聞網站、部落格。
- **電子商務**：商品、訂單、付款、物流。
- **社交網絡**：用戶關係、動態、訊息。
- **學術／研究網站**：學術資源平台、大型資料。
- **資料分析與視覺化**：結合 Pandas、NumPy。

### 1.4 社群與資源

- **官方文檔**：https://docs.djangoproject.com/zh-hans/stable/
- **社群**：StackOverflow、Django 討論區。
- **第三方套件**：涵蓋認證、API 等各種需求。
- **版本更新**：定期釋出，建議保持最新穩定版。

## 2. 設置開發環境

### 2.1 準備工作

#### 2.1.1 安裝 Python

Django 5.2 支援 Python 3.10～3.14（建議 3.14）。檢查版本：

```
python3 --version    # macOS / Linux
python --version     # Windows
```

安裝時記得勾選「Add Python to PATH」。

#### 2.1.2 安裝 pip

pip 是 Python 的套件管理工具，Python 3 通常已內建。檢查：

```
pip --version
```

### 2.2 安裝 Django

#### 2.2.1 版本選擇

課程以 **Django 5.2 LTS**（2025-04 發布，支援至 2028-04）為準。生產環境建議用 LTS，並使用該系列最新的補丁版本。

#### 2.2.2 用 pip 安裝

```
pip install "django~=5.2"        # 5.2 系列最新補丁
pip install "django==5.2.*"      # 固定 5.2 系列
django-admin --version           # 確認安裝
```

### 2.3 建立虛擬環境

虛擬環境讓不同專案使用各自的 Python 版本與套件，避免衝突。

```
python3 -m venv venv             # 建立
source venv/bin/activate         # 啟動（macOS / Linux）
venv\Scripts\activate            # 啟動（Windows）
deactivate                       # 停用
```

啟動後提示符會變成 `(venv)`。

### 2.4 建立第一個專案

```
django-admin startproject myproject
```

產生的結構：

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

啟動開發伺服器：

```
python manage.py runserver
```

打開 http://127.0.0.1:8000/ 看到歡迎頁面，即代表成功。

### 2.5 專案結構詳解

| 檔案 | 用途 |
| --- | --- |
| `manage.py` | 命令列工具（runserver、migrate、createsuperuser、startapp 等） |
| `settings.py` | 全域設定（資料庫、App 清單、中介軟體、模板、靜態檔…） |
| `urls.py` | URL 路由與視圖的對應 |
| `asgi.py` / `wsgi.py` | 伺服器入口：wsgi 同步、asgi 支援非同步（如 WebSocket） |

**settings.py 常見設定**：`DEBUG`（開發 True、上線 False）、`ALLOWED_HOSTS`、`INSTALLED_APPS`、`MIDDLEWARE`、`TEMPLATES`、`DATABASES`。

### 2.6 常見問題排查

- **伺服器無法啟動**
  - Django 未安裝 → 重新安裝：`pip install "django~=5.2"`
  - 埠被佔用 → 換埠：`python manage.py runserver 8080`
- **無法訪問**
  - `ALLOWED_HOSTS` 設定：`ALLOWED_HOSTS = ['127.0.0.1', 'localhost']`

## 3. Project 與 App（導論）

Django 中 **Project（專案）** 是整體應用、掌管所有設定與入口；**App（應用）** 是專案內的功能模組（如部落格、帳號）。一個 Project 可包含多個 App，透過 `settings.py` 的 `INSTALLED_APPS` 註冊；細節見下一章。
