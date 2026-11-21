# 第 8 章 · Project、App 與 settings 配置

## 3. Django 的 Project 與 App

### 3.1 概述

- **Project（專案）**：整個 Web 應用的最外層容器，包含所有設定、URL 配置與 App 清單。
- **App（應用）**：專案內的功能模塊（如部落格、用戶認證），專注單一功能，可被多個專案重用。

### 3.2 Project 的結構

用 `django-admin startproject` 建立，結構如下：

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

- `manage.py`：命令列工具，管理專案（遷移、跑伺服器等）。
- `myproject/`：與專案同名的內部資料夾，放核心設定。
- `__init__.py`：空文件，標記為 Python 套件。
- `settings.py`：專案設定（資料庫、靜態檔路徑等）。
- `urls.py`：URL 與視圖的對應。
- `asgi.py` / `wsgi.py`：ASGI / WSGI 伺服器入口（部署用）。

### 3.3 App 的結構

用 `python manage.py startapp myapp` 建立：

```
myapp/
    migrations/
        __init__.py
    __init__.py
    admin.py
    apps.py
    models.py
    views.py
    tests.py
```

- `migrations/`：資料庫遷移檔（模型改動後自動產生）。
- `admin.py`：後台管理設定，註冊模型。
- `apps.py`：App 的設定與初始化。
- `models.py`：模型定義（對應資料庫表）。
- `views.py`：視圖，處理請求並回傳回應。
- `tests.py`：測試檔。

### 3.4 兩者的關係

Project 是**容器**、App 是**組件**：一個 Project 可包含多個 App。Project 負責全域配置（`settings.py`）、URL 路由與 App 註冊（`INSTALLED_APPS`）；App 專注自身功能、可獨立開發與重用。

### 3.5 什麼時候該建立新 App

- **功能劃分明確**：與現有邏輯無關（如「用戶認證」與「部落格」各自獨立）。
- **邏輯隔離**：功能太複雜、難以與現有 App 整合。
- **未來可能重用**：封裝成獨立 App 便於搬移與整合。

### 3.6 總結

Project 是容器、App 是功能模塊；`settings.py` 管理全域設定、`manage.py` 執行各種管理命令，兩者是 Django 開發的核心工具。
## 4. 配置 settings.py

### 4.1 settings.py 的結構

典型的 `settings.py`：

```
# settings.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent   # 專案根目錄

DEBUG = True                    # 是否為除錯模式
ALLOWED_HOSTS = []              # 允許訪問的主機

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',                    # 自己的應用
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'
TEMPLATES = [ ... ]             # 模板引擎設定
DATABASES = { ... }             # 資料庫設定
STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

### 4.2 常見配置項目

#### DEBUG
控制是否為除錯模式。`True` 時顯示詳細錯誤，方便開發；**上線必須設為 `False`**，以免洩漏敏感資訊。

#### ALLOWED_HOSTS
控制哪些主機可訪問本專案。`DEBUG = False` 時必須指定允許的域名或 IP：

```
ALLOWED_HOSTS = ['example.com', 'www.example.com']
```

#### INSTALLED_APPS
已載入的 App 清單，含 Django 內建（`auth`、`admin` 等）與自訂 App（如 `myapp`）。

#### MIDDLEWARE
請求與回應之間的中間件清單，每個負責一方面（安全、會話、認證等）。

#### DATABASES
資料庫設定，支援 SQLite、PostgreSQL、MySQL、Oracle 等。

```
# SQLite（預設）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

```
# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### STATIC_URL 與 STATICFILES_DIRS
`STATIC_URL` 設定靜態檔的訪問路徑；`STATICFILES_DIRS` 指定額外的靜態檔搜尋目錄。

```
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

## 5. manage.py 命令

`manage.py` 是專案的管理工具，執行各種開發、測試與維運操作。

### 5.1 常見命令

#### runserver
啟動開發伺服器（可指定埠）：

```
python manage.py runserver        # http://127.0.0.1:8000
python manage.py runserver 8080   # http://127.0.0.1:8080
```

#### makemigrations / migrate
改模型後：`makemigrations` 產生遷移檔，`migrate` 套用到資料庫。

```
python manage.py makemigrations
python manage.py migrate
```

#### createsuperuser
建立超級用戶（管理後台帳號），依提示輸入帳密。

```
python manage.py createsuperuser
```

#### shell
啟動互動式 Python Shell，直接與模型、資料互動。

```
python manage.py shell
```

#### test
執行專案測試。

```
python manage.py test
```

### 5.2 自定義命令

1. 在 App 下建立 `management/commands/` 目錄與指令檔：

```
myapp/
    management/
        commands/
            mycommand.py
```

2. 撰寫指令：

```
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = '這是一個自定義命令範例'

    def handle(self, *args, **kwargs):
        self.stdout.write("執行自定義命令")
```

3. 執行：

```
python manage.py mycommand
```
## 6. Django 的 URL 配置與路由系統

URL 路由負責把使用者請求的 URL 映射到對應的視圖。

### 6.1 URL 配置（URLconf）

<figure class="fig-svg"><svg viewBox="0 0 860 250" width="100%" role="img" aria-label="Django URL 路由解析：請求依 urlpatterns 逐條比對，命中就呼叫視圖，否則回 404" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="90" width="150" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="95" y="115" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">請求</text><text x="95" y="135" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">GET /post/42</text><rect x="210" y="90" width="190" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="305" y="115" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">urlpatterns</text><text x="305" y="135" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">path() 由上而下比對</text><rect x="450" y="20" width="200" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="550" y="45" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">視圖</text><text x="550" y="65" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">post_detail(request, id=42)</text><rect x="450" y="165" width="200" height="62" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="550" y="190" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">404</text><text x="550" y="210" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">沒有規則匹配</text><rect x="700" y="20" width="140" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="770" y="45" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">回應</text><text x="770" y="65" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">HttpResponse</text><line x1="170" y1="121" x2="206" y2="121" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="400" y1="108" x2="446" y2="62" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="400" y1="134" x2="446" y2="190" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="650" y1="51" x2="696" y2="51" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/></svg><figcaption>圖　URL 路由解析：請求進來後由 urlpatterns 逐條比對，<code>path('post/&lt;int:id&gt;/')</code> 命中就把 id 傳給視圖，沒有命中則回 404。</figcaption></figure>

Django 用 **URLconf** 將 URL 模式映射到視圖，設定寫在 `urls.py`。用 `path()` 定義模式，參數如下：

| 參數 | 說明 |
| --- | --- |
| `route` | URL 模式，如 `'about/'`、`'post/<int:id>/'` |
| `view` | 匹配時呼叫的視圖 |
| `kwargs` | 傳給視圖的額外關鍵字參數 |
| `name` | 模式名稱，供反向解析（reverse）用 |

```
# myproject/urls.py
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),          # 管理後台
    path('', views.index, name='index'),      # 首頁
    path('about/', views.about, name='about'),
]
```

### 6.2 靜態 URL 與動態 URL

- **靜態 URL**：固定路徑，如 `/about/`。
- **動態 URL**：含變量，依參數產生不同頁面，如 `post/<int:id>/`。

```
urlpatterns = [
    path('about/', views.about, name='about'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
]
```

### 6.3 路徑轉換器

| 轉換器 | 匹配 |
| --- | --- |
| `<int:var>` | 整數 |
| `<str:var>` | 字串（不含 `/`） |
| `<slug:var>` | slug（字母、數字、`-`、`_`） |
| `<uuid:var>` | UUID |
| `<path:var>` | 完整路徑（含 `/`） |

### 6.4 用 include() 拆分 URLconf

應用變大時，用 `include()` 把各 App 的 URL 分開管理：

```
# myproject/urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),   # 交給 blog 應用的 urls.py
]
```

### 6.5 視圖與 URL 的連接

**函數視圖**：接受 `request`、回傳回應。

```
# myapp/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("歡迎來到我的網站！")
```

```
# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
]
```

**動態 URL 與視圖參數**：URL 變量會以參數傳入視圖。

```
def post_detail(request, id):
    return HttpResponse(f"這是文章 {id} 的詳情頁面")
```

**用 kwargs 傳遞附加參數**：

```
urlpatterns = [
    path('post/<int:id>/', views.post_detail, {'author': 'John'}, name='post_detail'),
]
```

```
def post_detail(request, id, author):
    return HttpResponse(f"文章 {id} 由 {author} 撰寫")
```

### 6.6 動態 URL 的應用

- **部落格**：用 slug 標識文章，`post/<slug:slug>/` 動態生成文章頁。
- **電商**：用產品 ID，`product/<int:id>` 動態生成商品頁。
- **表單提交**：提交後用 `redirect()` 導回文章頁。

```
from django.shortcuts import redirect

def submit_comment(request, post_id):
    if request.method == 'POST':
        # 儲存評論...
        return redirect('post_detail', id=post_id)
```

## 7. Django 視圖系統（導論）

視圖（View）負責處理 HTTP 請求、產生 HTTP 回應，並與模板協作生成動態 HTML。視圖分**函數視圖**與**類視圖**兩種，細節見後續章節。
