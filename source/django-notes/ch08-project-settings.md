# 第 8 章 · Project、App 與 settings 配置

### 3.1 Django 的 Project 與 App

#### 3.1.1 概述

在 Django 框架中，Project（項目）是一個整體的 Web 應用，包含所有配置和設置，而 App（應用）是 Project 中的一個功能模塊。Django 鼓勵將應用劃分為多個功能模塊，以便更好地管理代碼、實現重用和分離關注點。

- Project：是 Django 應用的最外層容器，包含了所有設置、URL 配置和應用列表。

- App：是一個功能具體的模塊，例如博客應用、用戶認證應用等。每個應用應該專注於一個特定功能，並能夠被多個項目重用。

#### 3.1.2 Django Project 的結構

當你使用 django-admin startproject 命令創建一個 Django 項目時，Django 會自動生成一個項目目錄，並為你配置好一個基礎結構。以下是典型的 Django Project 結構：

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
- manage.py：這是一個命令行工具，用來管理 Django 項目的運行和調試。通過這個文件，你可以執行各種與項目相關的操作，例如遷移數據庫、運行開發伺服器等。

- myproject/：內部文件夾，與項目同名，包含項目的核心設置和配置。

。__init__.py：一個空文件，用於將目錄標記為 Python 包。

- settings.py：項目的配置文件，管理項目的全局設置（如數據庫配置、靜態文件路徑等）。

- urls.py：項目的 URL 配置文件，管理 URL 和視圖之間的映射。

- asgi.py：ASGI 配置文件，用於異步服務的部署。

- wsgi.py：WSGI 配置文件，用於傳統服務的部署。

#### 3.1.3 Django App 的結構

Django 的每個應用都是一個獨立的模塊，可以被不同的項目共享和重用。當你創建一個應用時（使用 python manage.py startapp），Django 會為你生成一個應用的基本結構：

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
- migrations/：這個目錄存放應用的數據庫遷移文件。每當你修改模型時，Django會生成相應的遷移文件。

- __init__.py：這是一個空文件，標記目錄為 Python 包。

- admin.py：用於定義應用在 Django 管理站點中的配置，這裡可以註冊模型並定義其在管理後臺的呈現方式。

- apps.py：用於應用的配置，Django 通過這個文件來管理應用的初始化。

- models.py：應用的模型定義文件，管理與資料庫表相關的代碼。

- views.py：應用的視圖文件，處理用戶請求並返回響應。

- tests.py：應用的測試文件，用於編寫單元測試和集成測試，確保應用的功能正常。

#### 3.1.4 Project 和 App 之間的關係

Project 和 App 之間的關係是一種 容器與組件的關係。Project 是一個更高層次的容器，管理應用的配置和統一入口，而 App 是具體的功能模塊，Project 可以包含多個 App。

## Project 是全局配置的核心

Project 包含了整個 Django 應用的全局配置，管理應用的生命週期。這裡是 Project 負責的幾個重要方面：

- 全局設置：如數據庫連接、靜態文件、語言和時區等。

- URL 路由：定義應用的 URL 結構，將不同的 URL 路由到對應的 App 和視圖。

- 應用的註冊：Project 通過 settings.py 中的 INSTALLED_APPS 註冊所有的 App，確保 Django 認識到它們的存在。

## App 是功能模塊的組成部分

App 專注於具體的功能開發，專為某個功能（如博客、認證等）設計和構建。每個 App 之間可以相對獨立運行和開發，這為重用性提供了便利。

## Project 可以包含多個 App

一個 Project 通常會包含多個 App，每個 App 都專注於處理某一類具體的功能。以下是一個典型的例子：

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
blog/ # 博客應用

```
migrations/
admin.py
apps.py
models.py
views.py
```
accounts/ # 用戶帳戶管理應用

```
migrations/
admin.py
apps.py
models.py
views.py
```
在這個例子中，blog 是一個博客應用，負責處理與文章、評論相關的邏輯，而 accounts 則負責用戶帳戶管理。這兩個應用都屬於同一個 Project，它們之間可以共存並互相配合工作。

#### 3.1.5 什麼時候應該創建新的 App

決定是否創建一個新 App 取決於你所開發的功能是否可以被視為一個獨立的模塊。如果這個功能將來可能會被重用或有單獨的責任範圍，那麼創建一個新 App 是更好的選擇。

以下情況下應考慮創建新 App：

- 功能劃分明確：當功能與現有應用邏輯無關時，應考慮創建新 App。例如，用戶認證系統和博客系統應該是兩個獨立的 App。

- 邏輯隔離：當一個功能模塊的邏輯過於複雜且無法與現有應用進行良好的集成時，應創建新 App。

- 未來重用：如果這個功能模塊將來可能會被其他項目重用，那麼將其封裝為一個獨立的 App 可以更容易進行遷移和整合。

### 3.2 配置 settings.py

settings.py 是 Django 項目中最重要的配置文件之一，負責管理項目的全局設置。這個文件中包含了與數據庫、靜態文件、應用程序等相關的設置。

#### 3.2.1 settings.py 文件的結構

典型的 settings.py 文件由多個設置參數組

成，每個參數控制 Django 項目的不同方面。以下是一些常見的設置項：

```
# settings.py
from pathlib import Path

# 專案根目錄（Django 2.0 起用 pathlib，3.2+ 的 startproject 就是這樣產生）
BASE_DIR = Path(__file__).resolve().parent.parent

# 基本設置
DEBUG = True # 是否處於調試模式
ALLOWED_HOSTS = [] # 設定允許訪問的主機
# 應用程式註冊
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'myapp', # 自己的應用
]
# 中間件
MIDDLEWARE = [
'django.middleware.security.SecurityMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# URL 設置
ROOT_URLCONF = 'myproject.urls'
# 模板設置
TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [],
'APP_DIRS': True,
'OPTIONS': {
'context_processors': [
'django.template.context_processors.debug',
'django.template.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
],
},
],
# 數據庫設置
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
}
}
# 靜態文件設置
STATIC_URL = '/static/'
# 預設主鍵型別（Django 3.2 起 startproject 會產生；未設定時 migrate 會出現 W042 警告）
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```
#### 3.2.2 常見配置項目解析

```
DEBUG
```
DEBUG 是控制項目是否處於調試模式的設置。當 DEBUG=True 時，Django 會顯示詳細的錯誤信息，這在開發階段非常有用。但在生產環境中，必須將 DEBUG 設置為 False，以避免泄露敏感信息。

```
ALLOWED_HOSTS
```
ALLOWED_HOSTS 用來控制哪些主機可以訪問 Django 項目。這是一個安全設置，當 DEBUG=False 時，必須指定允許訪問的域名或 IP 地址。

範例：

```
ALLOWED_HOSTS = ['example.com', 'www.example.com']
INSTALLED_APPS
```
INSTALLED_APPS 是一個包含所有應用的列表，Django 會根據這個列表來加載應用。這裡既包括 Django 內建應用（如 auth 和 admin），也包括你自己開發的應用（如 myapp）。

```
MIDDLEWARE
```
MIDDLEWARE 是一組在處理請求和響應時會被調用的中間件。每個中間件都負責處理某一個方面的邏輯，比如安全性、會話管理、認證等。

```
DATABASES
```
DATABASES 配置項用來設置項目使用的數據庫。Django 支持多種數據庫，包括 SQLite、PostgreSQL、MySQL 和 Oracle。以下是使用 SQLite 的基本配置：

```
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
}
}
```
如果你使用的是 PostgreSQL，可以這樣配置：

```
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
STATIC_URL 和 STATICFILES_DIRS

STATIC_URL 是用來設置靜態文件的訪問路徑。開發階段的靜態文件通常存放在應用內的 static 文件夾中。你可以通過 STATICFILES_DIRS 來指定靜態文件的搜索目錄。

範例：

```
STATIC_URL = '/static/'
STATICFILES_DIRS = [
BASE_DIR / "static",
]
```
### 3.3 manage.py 命令

manage.py 是 Django 項目中的命令行工具，它使得管理 Django 項目變得更加簡單。通過 manage.py，你可以執行各種與項目開發、測試和運行相關的操作，如運行開發伺服器、創建遷移、執行測試等。

#### 3.3.1 常見的 manage.py 命令

```
runserver
```
runserver 是最常用的命令之一，它啟動 Django 的開發伺服器，讓你可以在本地測試應用。

範例：

```
python manage.py runserver
```
你還可以指定伺服器運行的端口號：

```
python manage.py runserver 8080
```
這樣伺服器將運行在 http://127.0.0.1:8080。

```
migrate
```
migrate 命令用來將數據庫遷移應用到實際的資料庫中。當你修改模型後，必須先創建遷移文件，再運行 migrate 命令來更新資料庫。

範例：

```
python manage.py migrate
makemigrations
```
makemigrations 命令用來生成數據庫遷移文件。當你對模型進行修改後，必須先運行 makemigrations 來生成相應的遷移文件。

範例：

```
python manage.py makemigrations
createsuperuser
```
createsuperuser 命令用來創建一個具有管理權限的超級用戶。這個用戶可以登錄 Django 的管理後臺，並進行數據管理。

範例：

```
python manage.py createsuperuser
```
按照提示輸入用戶名、電子郵件和密碼後，即可創建一個超級用戶。

```
shell
```
shell 命令啟動 Django 的互動式 Python Shell，允許你在命令行中直接與 Django 的模型和數據進行交互。

範例：

```
python manage.py shell
```
你可以在 Shell 中進行即時的數據庫查詢和測試。

```
test
```
test 命令用來運行項目的測試。Django 提供了一個內建的測試框架，允許你編寫和運行單元測試和集成測試。

範例：

```
python manage.py test
```
這會運行所有已經定義的測試用例。

#### 3.3.2 自定義 manage.py 命令

Django 允許你創建自定義的 manage.py 命令來處理一些特定的操作。這對於需要自動化任務或管理工具的項目特別有用。

範例：創建自定義命令

1. 在應用的 management/commands/ 目錄下創建一個新的 Python 文件。結構如下：

```
myapp/
management/
commands/
mycommand.py
```
2. 編寫自定義命令邏輯：

```
from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = '這是一個自定義命令範例'
def handle(self, *args, **kwargs):
    pass  # 內容省略
```
self.stdout.write("執行自定義命令")

3. 執行自定義命令：

```
python manage.py mycommand
```
這將輸出 執行自定義命令。

### 3.4 總結

在本章中，我們詳細介紹了 Django 的 Project 和 App 的區別，學習瞭如何設置和配置項目以及應用，並深入探討了 settings.py 文件中的常見設置項目。此外，我們還介紹了 manage.py 命令的使用，並學習瞭如何創建自定義命令來進行項目管理。這些概念和工具是 Django 開發過程中不可或缺的一部分，掌握它們將有助於開發和管理高效、可擴展的 Django 應用。

4: Django 的 URL 配置與路由系統

Django 框架的 URL 路由系統 是一個關鍵的組成部分，負責將用戶的 URL 請求映射到相應的視圖函數。它的作用是將瀏覽器發送的 URL 與應用內的處理邏輯（即視圖）進行匹配。掌握 URL 配置和路由系統對於 Django 應用的開發至關重要。本章將詳細介紹如何設置 URL 配置、實現 URL 路由、配置 urls.py 文件，以及如何將視圖函數與 URL 連接，並深入探討動態 URL 的應用。

### 4.1 Django 的 URL 配置

<figure class="fig-svg"><svg viewBox="0 0 860 250" width="100%" role="img" aria-label="Django URL 路由解析：請求依 urlpatterns 逐條比對，命中就呼叫視圖，否則回 404" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="90" width="150" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="95" y="115" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">請求</text><text x="95" y="135" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">GET /post/42</text><rect x="210" y="90" width="190" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="305" y="115" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">urlpatterns</text><text x="305" y="135" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">path() 由上而下比對</text><rect x="450" y="20" width="200" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="550" y="45" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">視圖</text><text x="550" y="65" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">post_detail(request, id=42)</text><rect x="450" y="165" width="200" height="62" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="550" y="190" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">404</text><text x="550" y="210" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">沒有規則匹配</text><rect x="700" y="20" width="140" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="770" y="45" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">回應</text><text x="770" y="65" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">HttpResponse</text><line x1="170" y1="121" x2="206" y2="121" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="400" y1="108" x2="446" y2="62" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="400" y1="134" x2="446" y2="190" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="650" y1="51" x2="696" y2="51" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/></svg><figcaption>圖　URL 路由解析：請求進來後由 urlpatterns 逐條比對，<code>path('post/&lt;int:id&gt;/')</code> 命中就把 id 傳給視圖，沒有命中則回 404。</figcaption></figure>

#### 4.1.1 URL 配置的概念

在 Django 中，URL 配置（URLconf）是一個將 URL 模式映射到視圖的系統。它的作用是根據用戶輸入的 URL 路徑來定位對應的處理邏輯（即視圖）。Django 使用 urls.py 文件來管理 URLconf，其中包含了所有 URL 模式及其對應的視圖。

Django 通過 path() 函數來定義 URL 模式，該函數允許將 URL 路徑和處理該路徑的視圖函數關聯起來。每當用戶訪問網站時，Django 會根據 URLconf 來匹配用戶輸入的 URL，並調用對應的視圖函數來生成響應。

#### 4.1.2 urls.py 文件的結構

urls.py 文件是 URLconf 的配置文件，通常放置在 Django 項目目錄下的根目錄以及每個應用內部。項目根目錄的 urls.py 文件負責處理全局的 URL 路徑，而每個應用內的 urls.py 則管理該應用的特定路徑。

以下是一個典型的 urls.py 文件結構範例：

path('admin/', admin.site.urls), # 管理站點的 URL 路徑
path(", views.index, name='index'), # 根路徑映射到首頁視圖
path('about/', views.about, name='about'), # 靜態 "關於我們" 頁面

```
# myproject/urls.py
from django.contrib import admin
from django.urls import path
from myapp import views
urlpatterns = [
]
```
在這個範例中，我們定義了三個 URL 路徑：

1. /admin/：對應 Django 自帶的管理後臺。

2. /：對應網站的首頁，當用戶訪問根 URL（即 http://127.0.0.1:8000/）時，views.index 函數將被調用。

3. /about/：對應 "關於我們" 頁面，該頁面的處理邏輯位於 views.about 中。

每個 URL 路徑都與具體的視圖函數關聯，並且可以為其命名（通過 name 參數），以便在模板或其他視圖中進行 URL 反向解析。

### 4.2 URL 路由的基礎

#### 4.2.1 靜態 URL 與動態 URL

在 Django 中，URL 可以分為 靜態 URL 和 動態 URL：

- 靜態 URL 是不變的路徑，用於訪問固定的頁面。例如，/about/ 是一個靜態 URL，它永遠指向 "關於我們" 頁面。

- 動態 URL 是可以變化的 URL，它包含動態變量，允許根據不同的參數生成不同的頁面內容。例如，博客文章的 URL 可以包含文章的 ID，從而動態生成不同的文章頁面。

範例：定義靜態和動態 URL

path('about/', views.about, name='about'), # 靜態 URL
path('post/<int:id>/, views.post_detail, name='post_detail'), # 動態 URL

```
# myapp/urls.py
from django.urls import path
from . import views
urlpatterns = [
]
```
在這裡，about/ 是靜態 URL，無論何時訪問，總是映射到同一個 "關於我們" 頁面。post/<int:id>/ 是動態 URL，其中 <int:id> 是一個變量，它表示動態部分，用於表示文章的 ID。

#### 4.2.2 URL 路徑轉換器

Django 提供了多種 路徑轉換器，用於定義 URL 中動態部分的數據類型。常見的路徑轉換器包括：

- <int:variable>：匹配一個整數。

- <str:variable>：匹配一個字符串。

- <slug:variable>：匹配一個 slug（短標題，由字母、數字、連字符和下劃線組成）。

- <uuid:variable>：匹配一個 UUID。

- <path:variable>：匹配完整的路徑，包括斜線。

範例：使用路徑轉換器

path('post/<int:id>/, views.post_detail, name='post_detail'), # 匹配整數 ID
path('category/<slug:slug>/, views.category_detail, name='category_detail'), # 匹配 slug

```
# 使用不同的路徑轉換器來匹配不同類型的動態 URL
urlpatterns = [
]
```
在這裡，post/<int:id/> 只匹配數字 ID，而 category/<slug:slug/> 則匹配包含字母和數字的 slug。

### 4.3 ur1s.py 配置詳解

#### 4.3.1 使用 path() 函數定義 URL

Django 使用 path() 函數來定義 URL 模式並將其映射到視圖。path() 函數的基本格式如下：

```
path(route, view, kwargs=None, name=None)
```
- route：定義 URL 模式，是用戶請求的 URL 路徑（如 'about/' 或 'post/<int:id>/'）。

- view：指定當 URL 匹配時調用的視圖函數。

- kwargs：一個可選的關鍵字參數字典，將會傳遞給視圖。

- name：URL 模式的名稱，允許你在其他地方（如模板）使用這個名稱來引用該 URL。

範例：使用 path() 定義 URL

path("views.index, name='index'), # 定義根 URL
path('contact/', views.contact, name='contact'), # 靜態 URL
path('post/<int:id>/, views.post_detail, name='post_detail'), # 動態 URL

```
# myapp/urls.py
from django.urls import path
from . import views
urlpatterns = [
]
```
#### 4.3.2 URLconf 中的 include()

隨著應用的增長，將所有 URL 都放在一個文件中會導致代碼難以維護。Django 提供了 include() 函數來將 URLconf 分割到不同的應用中。這樣，主 URLconf 文件可以將請求分發到不同的應用，而每個應用內的 URLconf 文件負責處理具體的路徑。

範例：在主項目的 urls.py 中使用 include()

path('admin/', admin.site.urls), # 管理後臺 URL
path('blog/', include('blog.urls')), # 將 URL 分發到博客應用的 URLconf

```
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
]
```
在這個例子中，當用戶訪問 /blog/ 開頭的 URL 時，Django 會將這些請求分發到 blog 應用的 urls.py 文件中處理。這種設計使得每個應用的 URLconf 可以獨立管理，從而提高了代碼的可維護性。

### 4.4 視圖與 URL 的連接

#### 4.4.1 視圖的基本概念

Django 的視圖（View）負責處理用戶的 HTTP 請求並返回響應。每個 URL 模式都需要映射到一個具體的視圖函數，該函數的作用是根據請求來生成並返回一個合適的響應（如 HTML 頁面、JSON 數據等）。

視圖可以是普通的 函數視圖 或 類視圖。在這一節中，我們將首先介紹函數視圖，後續章節將討論類視圖。

#### 4.4.2 定義函數視圖

函數視圖是一個接受 HTTP 請求對象並返回 HTTP 響應對象的 Python 函數。以下是一個簡單的視圖函數範例：

```
# myapp/views.py
from django.http import HttpResponse
def index(request):
    pass  # 內容省略
```
return HttpResponse("歡迎來到我的網站！")

在這個例子中，index 視圖函數接受一個 request 對象，並返回一個簡單的 HttpResponse，即一個包含純文本 "歡迎來到我的網站！" 的響應。

#### 4.4.3 視圖與 URL 的連接

一旦視圖定義好，我們需要將它們與 URL 進行連接，這是通過 urls.py 文件中的 path() 函數來完成的。

範例：將視圖與 URL 連接

```
# myapp/urls.py
from django.urls import path
from . import views
urlpatterns = [
```
path(", views.index, name='index'), # 將根 URL 連接到 index 視圖

path('contact/', views.contact, name='contact'), # 將 contact/ URL 連接到 contact 視圖

這樣，當用戶訪問 http://127.0.0.1:8000/ 時，index 視圖將被調用並返回對應的響應；

當用戶訪問 http://127.0.0.1:8000/contact/ 時，contact 視圖將處理該請求。

#### 4.4.4 處理動態 URL

在動態 URL 中，我們需要從 URL 中提取變量，並將這些變量傳遞給視圖函數。視圖函數可以使用這些變量來生成不同的內容或查詢資料庫。

範例：處理動態 URL 的視圖

```
# myapp/views.py
from django.http import HttpResponse
def post_detail(request, id):
    pass  # 內容省略
```
return HttpResponse(f"這是文章 {id} 的詳情頁面")

在這個範例中，post_detail 視圖函數接受一個 id 參數，該參數來自 URL 中的動態部分。當用戶訪問 /post/5/ 時，id 將是 5，視圖會返回 "這是文章 5 的詳情頁面"。

#### 4.4.5 使用 kwargs 來傳遞附加參數

除了通過 URL 提取變量外，你還可以使用 kwargs 來將附加的參數傳遞給視圖函數。這對於需要靜態傳遞一些特定數據的場景很有用。

範例：使用 kwargs 傳遞參數

```
# myapp/urls.py
urlpatterns = [
path('post/<int:id>/, views.post_detail, {'author': 'John'}, name='post_detail'),
]
```
在這裡，我們將一個 author 參數通過 kwargs 傳遞給視圖。

```
# myapp/views.py
def post_detail(request, id, author):
    pass  # 內容省略
```
return HttpResponse(f"文章 {id} 由 {author} 撰寫")

這樣，當訪問 /post/5/ 時，除了 id=5 之外，還會有 author='John' 的附加參數被傳遞給 post_detail 視圖。

### 4.5 動態 URL 的應用

動態 URL 在構建 Web 應用中至關重要，特別是在構建多頁面應用或 RESTful API 時，動態 URL 可以讓你輕鬆處理不同的資源和頁面。

4.5.1 應用場景 1：博客系統中的動態文章 URL

在博客系統中，通常會有許多文章，每篇文章都有一個唯一的 ID 或 slug。你可以使用動態 URL 來顯示不同文章的內容。

範例：博客文章的動態 URL

```
# myapp/urls.py
urlpatterns = [
path('post/<slug:slug>/, views.post_detail, name='post_detail'), # 使用 slug 作為文章標識
]
# myapp/views.py
def post_detail(request, slug):
# 根據 slug 從資料庫中查找文章
post = get_object_or_404(Post, slug=slug)
```
return HttpResponse(f"這是文章 {post.title} 的詳情頁面")

在這個範例中，我們使用 slug 作為文章的唯一標識，並動態生成不同文章的詳情頁面。

4.5.2 應用場景 2：電商網站中的產品頁面

在電商網站中，動態 URL 可以用來顯示不同產品的詳情頁面。例如，每個產品都有一個唯一的 ID，通過動態 URL 可以查詢對應的產品並顯示其信息。

範例：產品詳情的動態 URL

```
# shop/urls.py
urlpatterns = [
path('product/<int:id>', views.product_detail, name='product_detail'),
]
# shop/views.py
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
```
return HttpResponse(f"這是產品 {product.name} 的詳情頁面")

這樣，當用戶訪問 /product/42/ 時，會加載 ID 為 42 的產品詳情頁面。

#### 4.5.3 動態 URL 與表單提交

動態 URL 也可以用於處理表單提交。例如，用戶提交評論後，你可以重定向他們到該評論所屬的文章頁面。

範例：處理評論提交並重定向

```
# blog/views.py
from django.shortcuts import redirect
def submit_comment(request, post_id):
    if request.method == 'POST':
        # 保存評論邏輯
        return redirect('post_detail', id=post_id)
```
在這裡，我們使用動態 URL 和 redirect() 函數，將用戶重定向回評論所屬的文章詳情頁。

### 4.6 總結

在本章中，我們詳細介紹了 Django 的 URL 路由系統，學習瞭如何設置 靜態與動態 URL、配置 urls.py 文件，以及如何將 視圖與 URL 進行連接。我們還探討了動態 URL 的實際應用場景，包括博客文章詳情頁和電商網站的產品頁面。在掌握這些基本技術之後，你將能夠靈活地設計和構建各種動態 Web 應用。

5: Django 視圖系統

視圖（Views）是 Django 框架的核心組件之一，負責處理用戶的 HTTP 請求並生成相應的 HTTP 響應。在 Django 中，視圖的作用是將業務邏輯和數據處理集中在一個函數或類中，然後通過將結果返回給用戶。視圖還負責與模板進行交互，從而生成動態的 HTML 頁面。

在本章中，我們將深入探討 Django 視圖的概念，並詳細介紹 函數視圖 和 類視圖的區別，學習如何處理 GET 和 POST 請求，以及如何將視圖與 URL 進行連接 和上下文與模板的交互。
