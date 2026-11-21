# 第 11 章 · 分頁、美化、認證與專案實作

### 11.1 分頁的基本概念

分頁的主要目的是將大數據集分成多個小的數據塊，讓用戶可以按頁瀏覽。通常，分頁功能包括：

每頁顯示固定數量的記錄。

提供導航控件，讓用戶可以輕鬆跳轉到下一頁、上一頁或特定頁面。

顯示當前頁面的狀態，如當前頁數、總頁數等。

Django 提供了一個內建的 Paginator 類，用來處理數據的分頁邏輯，並提供了方便的接口來管理頁面的顯示。

### 11.2 使用 Paginator 進行分頁

#### 11.2.1 創建分頁器

要實現分頁，首先需要使用 Django 的 Paginator 類來創建分頁器。Paginator 類接受兩個參數：

1. 要分頁的對象列表：通常是一個查詢集。

2. 每頁顯示的記錄數：定義每頁需要顯示的記錄數量。

範例：使用 Paginator 創建分頁器

```
# myapp/views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Article
def article_list(request):
article_list = Article.objects.all() # 獲取所有文章
paginator = Paginator(article_list, 10) # 每頁顯示 10 條記錄
page_number 173
```
在這裡，我們使用 Paginator 對文章列表進行分頁，每頁顯示 10 條記錄。get_page() 方法會根據頁碼返回對應頁面的數據，並且在頁碼無效時自動處理異常。

#### 11.2.2 在模板中顯示分頁數據

接下來，我們需要在模板中顯示分頁數據和分頁導航。Django 提供了 page_obj，該對象包含當前頁面的數據以及分頁相關的信息，如是否有上一頁、下一頁等。

範例：在模板中顯示分頁導航

```
<!-- templates/article_list.html -->
{% for article in page_obj %}
{{ article.title }}</li>
{% endfor %}
</ul>
<div class="pagination">
```
頁 {{ page_obj.number }} 共 {{ page_obj.paginator.num_pages }} </span>

<!-- 顯示上一頁按鈕 -->

```
{% if page_obj.has_previous %}
```
<a href="?page={{ page_obj.previous_page_number }}">上一頁</a>

```
{% endif %}
```
<!-- 顯示下一頁按鈕 -->

```
{% if page_obj.has_next %}
```
<a href="?page={{ page_obj.next_page_number }}">下一頁</a>

```
{% endif %}
</div>
```
在這個範例中，page_obj 包含當前頁面的數據，我們通過循環來顯示當前頁的文章。同時，我們還使用 page_obj.has_previous 和 page_obj.has_next 來顯示上一頁和下一頁的導航按鈕。

### 11.3 處理分頁參數

#### 11.3.1 保留查詢參數

當我們在進行分頁時，可能會遇到需要保留其他查詢參數的情況，例如在篩選後進行分頁，這時我們希望篩選條件能夠保持在 URL 中。

範例：保留查詢參數進行分頁

```
# myapp/views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Article
def article_list(request):
    article_list = Article.objects.all()
    paginator = Paginator(article_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # 獲取其他查詢參數
    query_params = request.GET.copy()
    if 'page' in query_params:
        pass  # 內容省略
```
del query_params['page'] # 刪除分頁參數，避免重複

```
query_string = query_params.urlencode()
return render(request, 'article_list.html', {'page_obj': page_obj, 'query_string': query_string})
```
在模板中，我們可以使用這些保留的參數：

```
<div class="pagination">
{% if page_obj.has_previous %}
<a href="?page={{ page_obj.previous_page_number }}&{{ query_string }}"
```
>上一頁</a>

>

```
{% endif %} {% if page_obj.has_next %}
```
<a href="?page={{ page_obj.next_page_number }}&{{ query_string }}">下一頁</a>

```
{% endif %}
</div>
```
這樣，其他查詢參數將會被保留在 URL 中，確保篩選條件在分頁過程中保持不變。

### 11.4 自定義分頁控制

#### 11.4.1 設置每頁顯示的數量

有時，應用中需要允許用戶自定義每頁顯示的記錄數量。你可以通過查詢參數或表單來實現這一點。

範例：用戶設置每頁顯示數量

```
# myapp/views.py
def article_list(request):
    article_list = Article.objects.all()
    per_page = request.GET.get('per_page', 10) # 默認每頁顯示 10 條記錄
    paginator = Paginator(article_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'article_list.html', {'page_obj': page_obj})
```
在模板中，使用一個下拉框讓用戶選擇每頁顯示的數量：

```
<form method="GET">
```
<label for="per_page">每頁顯示：</label>

```
<select name="per_page" onchange="this.form.submit()">
<option value="5" {% if page_obj.paginator.per_page == 5 %}selected{% endif %}
%}>5</option>
<option value="10" {% if page_obj.paginator.per_page == 10 %}selected{% endif %}
%}>10</option>
<option value="20" {% if page_obj.paginator.per_page == 20 %}selected{% endif %}
%}>20</option>
</select>
</form>
```
#### 11.4.2 分頁範圍顯示

在某些應用中，為了提升用戶體驗，我們可能希望顯示更靈活的分頁導航，例如只顯示當前頁附近的頁碼，這樣可以避免過長的分頁導航條。

範例：顯示當前頁附近的頁碼

```
<div class="pagination">
{% if page_obj.has_previous %}
```
<a href="?page=1">第一頁</a>

<a href="?page={{ page_obj.previous_page_number }}">上一頁</a>

```
{% endif %} {% for num in page_obj.paginator.page_range %} {% if num >= page_obj.numberladd:-2 and num <= page_obj.numberladd:2 %} {% if num == page_obj.number %}
{{ num }}</span>
{% else %}
<a href="?page={{ num }}">{{ num }}</a>
{% endif %} {% endif %} {% endfor %} {% if page_obj.has_next %}
```
<a href="?page={{ page_obj.next_page_number }}">下一頁</a>

<a href="?page={{ page_obj.paginator.num_pages }}">最後一頁</a>

```
{% endif %}
</div>
```
這樣的分頁導航將只顯示當前頁附近的頁碼，提升可讀性。

### 11.5 使用 Ajax 進行分頁

傳統的分頁需要刷新整個頁面，但在現代 Web 應用中，使用 Ajax 可以實現更好的用戶體驗，讓分頁過程在不刷新整個頁面的情況下完成。

#### 11.5.1 基本的 Ajax 分頁實現

範例：使用 Ajax 請求分頁數據

1. 在視圖中返回分頁的 HTML：

```
from django.template.loader import render_to_string
from django.http import JsonResponse
def article_list(request):
    article_list = Article.objects.all()
    paginator = Paginator(article_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/article_list.html', {'page_obj': page_obj})
        return JsonResponse({'html': html})
        return render(request, 'article_list.html', {'page_obj': page_obj})
```
2. 創建一個 partials/article_list.html 模板來渲染數據。

```
{% for article in page_obj %}
{{ article.title }}</li>
{% endfor %}
</ul>
```
這樣的實現方式可以讓分頁過程變得更加流暢，提升用戶體驗。

### 11.6 總結

在本章中，我們深入探討了 Django 的分頁系統，學習瞭如何使用 Paginator 來進行數據分頁，並在模板中顯示分頁導航。我們還探討瞭如何處理分頁參數、允許用戶設置每頁顯示的數量，並介紹瞭如何使用 Ajax 實現動態分頁。

掌握這些技巧後，開發者可以輕鬆實現靈活的分頁功能，從而有效地處理大數據集並提升應用的性能和用戶體驗。

12: Django 與前端框架整合

使用 Bootstrap 美化 Django 頁面

在 Django 項目中，美化前端界面是提升用戶體驗的重要部分。儘管 Django 提供了強大的後端開發功能，但在前端方面，使用框架如 Bootstrap 能夠迅速提升頁面的外觀和響應式設計。Bootstrap 是一個非常流行的 HTML、CSS 和 JavaScript 框架，它使得構建漂亮且響應式的網站變得簡單且高效。

在本章中，我們將介紹如何將 Bootstrap 集成到 Django 項目中，並使用 Bootstrap 的組件來設計和美化 Django 頁面。

12. Bootstrap 簡介

Bootstrap 是由 Twitter 開發的一個開源前端框架，旨在幫助開發者快速構建現代化、響應式的網頁。Bootstrap 提供了大量的預設樣式、佈局和組件，如導航欄、按鈕、表單、卡片和模式框等，並且內建了響應式網格系統，使得頁面能夠自適應不同尺寸的設備。

### 12.1 為什麼使用 Bootstrap?

- 快速開發：Bootstrap 提供了許多預設樣式和組件，開發者無需從頭設計每個元素。

- 響應式設計：Bootstrap 內建了響應式佈局系統，可以讓網站自動適應不同設備的屏幕尺寸。

- 一致的設計：通過使用 Bootstrap，你可以保證網站各個部分的設計風格保持一致。

- 擴展性：開發者可以自定義 Bootstrap，並根據需求擴展樣式。

### 12.2. 在 Django 項目中引入 Bootstrap

#### 12.2.1 通過 CDN 引入 Bootstrap

在 Django 頁面中使用 Bootstrap 最簡單的方法是通過 CDN（內容分發網絡）直接加載 Bootstrap 的 CSS 和 JavaScript 文件。你只需要在模板文件的 標籤中加入 Bootstrap 的 CDN 連結。

範例：在 Django 模板中引入 Bootstrap

```
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
{% block title %}My Django Site{% endblock %}
```
<!-- 引入 Bootstrap CSS -->

```
<link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.9/dist/css/bootstrap.min.css"
rel="stylesheet"
/>
</head>
```
<!-- 主內容區塊 -->

```
{% block content %} {% endblock %}
```
<!-- 引入 Bootstrap JavaScript -->

```
<script
src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.9/dist/js/bootstrap.bundle.min.js"
```
></script>

```
</body>
</html>
```
這樣，我們的 Django 頁面已經加載了 Bootstrap 的 CSS 和 JavaScript 文件，接下來我們可以使用 Bootstrap 提供的組件和樣式。

#### 12.2.2 使用 Bootstrap 的網格系統

Bootstrap 的網格系統基於 12 列布局，可以非常靈活地設計響應式的頁面佈局。使用 row 和 col 類別，你可以創建自適應的佈局。

範例：使用網格系統創建基本佈局

```
<!-- templates/home.html -->
{% extends 'base.html' %} {% block content %}
<div class="container">
<div class="row">
<div class="col-md-4">
<div class="card">
<div class="card-body">
```
<h5 class="card-title">欄目 1</h5>

<p class="card-text">這是第一個欄目中的內容。</p>

```
</div>
</div>
</div>
<div class="col-md-4">
<div class="card">
<div class="card-body">
```
<h5 class="card-title">欄目 2</h5>

<p class="card-text">這是第二個欄目中的內容。</p>

```
</div>
</div>
</div>
<div class="col-md-4">
<div class="card">
<div class="card-body">
```
<h5 class="card-title">欄目 3</h5>

```
</div>
</div>
```
<p class="card-text">這是第三個欄目中的內容。</p>

```
</div>
</div>
</div>
</div>
{% endblock %}
```
在這個範例中，我們使用 Bootstrap 的網格系統將內容分成三列，並使用 card 組件來顯示每個欄目。

### 12.3. 使用 Bootstrap 美化 Django 表單

在 Django 中，表單是非常常見的元素，Bootstrap 提供了大量的預設樣式來美化表單，使其更具吸引力且易於使用。

12.3.1 自動應用 Bootstrap 樣式到 Django 表單

我們可以使用 Django 的 widget_tweaks 第三方庫來自動將 Bootstrap 的樣式應用到 Django 表單上。

安裝 django-widget-tweaks

首先，安裝 django-widget-tweaks：

```
pip install django-widget-tweaks
```
然後將它添加到 settings.py 中的已安裝應用：

```
# settings.py
INSTALLED_APPS = [
'widget_tweaks',
# 其他應用
]
```
使用 widget_tweaks 應用 Bootstrap 樣式

接下來，我們可以在模板中使用 widget_tweaks 將 Bootstrap 的樣式應用到表單字段。

```
<!-- templates/register.html -->
{% extends 'base.html' % } { % load widget_tweaks % } { % block content % }
<div class="container mt-5">
```
註冊</h2>

```
<form method="post">
{% csrf_token %}
<div class="mb-3">{{ form.usernameladd_class:"form-control" }} </div>
<div class="mb-3">{{ form.emailladd_class:"form-control" }} </div>
<div class="mb-3">{{ form.password.add_class:"form-control" }} </div>
<div class="mb-3">{{ form.password2ladd_class:"form-control" }} </div>
```
<button type="submit" class="btn btn-primary">註冊</button>

```
</form>
</div>
{% endblock %}
```
在這個範例中，我們使用 widget_tweaks 的 add_class 過濾器將 Bootstrap 的 form-control 類別應用到每個表單字段，這樣表單就會自動使用 Bootstrap 樣式進行渲染。

### 12.4. 美化 Django 的管理後臺

Django 的內建管理後臺功能強大，但默認樣式比較樸素。我們可以使用 django-admin-interface 這個第三方庫來美化 Django 管理後臺，使其更具現代感。

#### 12.4.1 安裝 django-admin-interface

首先，安裝 django-admin-interface：

```
pip install django-admin-interface
```
然後在 settings.py 中添加該應用：

```
# settings.py
INSTALLED_APPS = [
'admin_interface',
'colorfield',
'django.contrib.admin',
# 其他應用
]
```
接著運行遷移命令：

```
python manage.py migrate
```
#### 12.4.2 自定義 Django 管理後臺樣式

安裝好 django-admin-interface 後，我們可以通過管理後臺的 "Theme" 設置來自定義後臺的配色方案和佈局，這使得 Django 管理後臺更加美觀且易於使用。

### 12.5. 使用 Bootstrap 的其他組件

Bootstrap 提供了很多現成的組件，如導航欄、按鈕、模態框（Modal）、標籤頁（Tabs）等，這些組件可以讓你的 Django 頁面更加豐富和交互性更強。

#### 12.5.1 導航欄（Navbar）

範例：在 Django 項目中使用 Bootstrap 的導航欄

```
<!-- templates/base.html -->
<nav class="navbar navbar-expand-lg navbar-light bg-light">
<div class="container-fluid">
```
<a class="navbar-brand" href="#">我的網站</a>

```
<button
class="navbar-toggler"
type="button"
data-bs-toggle="collapse"
</button>
</div>
data-bs-target="#navbarNav"
aria-controls="navbarNav"
aria-expanded="false"
aria-label="Toggle navigation"
```
>

```
<span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse" id="navbarNav">
<ul class="navbar-nav">
<li class="nav-item">
```
<a class="nav-link active" aria-current="page" href="#">首頁</a>

```
</li>
<li class="nav-item">
```
<a class="nav-link" href="#">功能</a>

```
</li>
<li class="nav-item">
```
<a class="nav-link" href="#">聯繫我們</a>

```
</li>
</ul>
</div>
</div>
</nav>
```
這個導航欄可以自適應不同設備的屏幕，並且使用了 Bootstrap 的 collapse 功能，當屏幕變小時會自動收縮成按鈕形式。

#### 12.5.2 模態框（Modal）

範例：在 Django 頁面中使用模態框

```
<button
type="button"
class="btn btn-primary"
data-bs-toggle="modal"
data-bs-target="#exampleModal"
```
>

打開模態框

```
</button>
```
<!-- 模態框 -->

```
<div
class="modal fade"
id="exampleModal"
tabindex="-1"
aria-labelledby="exampleModalLabel"
aria-hidden="true"
```
>

```
<div class="modal-dialog">
<div class="modal-content">
<div class="modal-header">
```
<h5 class="modal-title" id="exampleModalLabel">模態框標題</h5>

```
<button
type="button"
class="btn-close"
data-bs-dismiss="modal"
aria-label="Close"
</button>
</div>
```
<div class="modal-body">這是模態框的內容</div>

```
<div class="modal-footer">
<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
```
關閉

```
</button>
```
<button type="button" class="btn btn-primary">保存變更</button>

```
</div>
</div>
</div>
```
這個模態框可以用來展示額外的信息或用戶交互表單，且不會重新加載頁面。

### 12.6. 總結

在本章中，我們學習瞭如何將 Bootstrap 集成到 Django 項目中，並使用 Bootstrap 的組件和樣式美化頁面。Bootstrap 提供了大量現成的樣式和工具，可以幫助我們快速構建響應式且美觀的 Django 網站。通過掌握這些技巧，你可以顯著提升 Django 項目的前端外觀和用戶體驗。

13 : Django 用戶註冊與登錄系統

在大多數 Web 應用中，用戶註冊與登錄系統 是基本且關鍵的功能，讓用戶可以創建帳戶、登錄應用並存取個人資料。Django 提供了一套完整的認證框架，方便我們快速地實現這些功能。通過這個系統，用戶可以安全地註冊、登錄和管理自己的帳戶。

在本章中，我們將學習如何構建一個完整的 Django 用戶註冊與登錄系統，包括註冊、登錄、登出、密碼重設等功能。這些功能將為我們的應用提供一個穩定且安全的用戶認證系統。

### 13.1. Django 認證框架介紹

Django 的內建認證系統處理了常見的用戶相關功能，包括：

- 用戶註冊和登錄

- 密碼加密存儲

- 用戶身份驗證

- 權限控制（管理員與普通用戶）

- 登出和密碼重設功能

我們可以使用 Django 自帶的視圖和表單快速實現這些功能，同時也能靈活地定製這些視圖來滿足具體需求。

### 13.2. 創建 Django 項目與應用

首先，我們將創建一個新的 Django 項目並添加應用來處理用戶認證。

#### 13.2.1 創建 Django 項目與應用

使用以下命令來創建一個新的 Django 項目和應用：

```
django-admin startproject myproject
cd myproject
python manage.py startapp accounts
```
在 settings.py 中添加應用到已安裝應用列表中：

```
# settings.py
INSTALLED_APPS = [
'accounts',
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
]
```
接下來，我們將實現用戶註冊和登錄功能。

### 13.3. 用戶註冊功能

13.3.1 使用 Django 內建的 UserCreationForm

Django 提供了 UserCreationForm，這是一個用來註冊新用戶的表單。我們可以使用這個表單來輕鬆實現用戶註冊功能。

## 創建註冊視圖

在 accounts/views.py 中創建註冊視圖，該視圖會處理用戶的註冊請求並保存新用戶。

login(request, user) # 自動登錄
return redirect('home') # 重定向到主頁面

```
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
        else:
            form = UserCreationForm()
            return render(request, 'accounts/register.html', {'form': form})
```
## 配置 URL 路由

我們需要將註冊視圖連接到 URL。在 accounts/urls.py 中添加對應的路由：

```
# accounts/urls.py
from django.urls import path
from .import views
urlpatterns = [
path('register/', views.register, name='register'),
]
```
別忘了將這個路由文件包含在主路由中。在 myproject/urls.py 中引入 accounts 應用的路由：

```
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
path('admin/', admin.site.urls),
path('accounts/', include('accounts.urls')), # 包含用戶路由
]
```
## 創建註冊模板

創建一個註冊表單的模板文件 templates/accounts/register.html :

```
<!-- templates/accounts/register.html -->
<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
```
註冊</title>

```
</head>
```
註冊</h2>

```
<form method="post">
{% csrf_token %} {{ form.as_p }}
```
<button type="submit">註冊</button>

```
</form>
</body>
</html>
```
這樣，當用戶訪問 /accounts/register/ 時，會看到註冊表單，並且可以創建新帳戶。

### 13.4. 用戶登錄與登出功能

Django 提供了現成的登錄和登出視圖，我們可以直接使用，並為其設置對應的 URL 路徑。

#### 13.4.1 使用內建登錄視圖

Django 內建了 LoginView，它會處理登錄表單的顯示和用戶認證。

## 配置登錄 URL

在 accounts/urls.py 中配置登錄視圖的路由：

```
# accounts/urls.py
from django.contrib.auth import views as auth_views
urlpatterns += [
path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
```
- LoginView 使用自定義模板 login.html 顯示登錄表單。

- LogoutView 則處理用戶登出的邏輯，並且登出後自動重定向到主頁。

- 注意：Django 5.0 起 LogoutView 只接受 POST 請求（以 GET 登出已被移除），模板要用表單提交（`<form method="post">{% csrf_token %}<button type="submit">登出</button></form>`），不能用 `<a href>` 連結。

創建登錄模板

我們需要創建一個 login.html 文件來顯示登錄表單：

```
<!-- templates/accounts/login.html -->
<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
```
登錄</title>

```
</head>
```
登錄</h2>

```
<form method="post">
{% csrf_token %} {{ form.as_p }}
```
<button type="submit">登錄</button>

```
</form>
</body>
</html>
```
登錄成功後，用戶將被重定向到預設的 next URL，或主頁。

### 13.5. 密碼重設功能

Django 還提供了內建的密碼重設功能，允許用戶重設他們的密碼。

#### 13.5.1 密碼重設流程

Django 內建的密碼重設功能包括四個步驟：

1. 重設密碼請求：用戶輸入他們的電子郵件，系統會發送一封重設密碼的郵件。

2. 郵件發送確認：顯示確認郵件已發送的頁面。

3. 設置新密碼：用戶通過郵件中的鏈接設置新密碼。

4. 完成密碼重設：顯示密碼重設成功的頁面。

#### 13.5.2 配置密碼重設的 URL

我們可以使用 Django 內建的密碼重設視圖來處理這一流程。首先，配置對應的 URL 路徑：

```
# accounts/urls.py
from django.contrib.auth import views as auth_views
urlpatterns += [
path('password_reset',
auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
name='password_reset',
path('password_reset_done',
auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
name='password_reset_done'),
path('reset/ / /',
auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
name='password_reset_confirm'),
path('password_reset_complete/',
auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
```
#### 13.5.3 設置郵件服務

Django 會發送包含密碼重設鏈接的電子郵件。因此，我們需要在 settings.py 中配置郵件服務器。

```
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
```
#### 13.5.4 創建模板

我們還需要為每個密碼重設步驟創建模板，例如：

```
<!-- templates/accounts/password_reset.html -->
```
重設密碼</h2>

```
<form method="post">
{% csrf_token %} {{ form.as_p }}
```
<button type="submit">發送重設鏈接</button>

```
</form>
```
### 13.6. 總結

在本章中，我們學習瞭如何在 Django 中使用內建的工具和表單來實現完整的用戶認證系統，這包括用戶註冊、登錄、登出以及密碼重設功能。Django 的認證系統非常靈活且安全，我們可以根據具體需求進行擴展和自定義。

14: 使用 Django 消息框架和外部庫

在 Django 中，messages 框架提供了一種方便的方式來顯示臨時消息，通常用於向用戶反饋信息（如成功、錯誤、警告等）。這些消息在用戶執行某些操作（如提交表單、登錄、註冊等）後顯示，並且會在頁面重新加載後自動消失。

Django 的 messages 框架內置了多種類型的消息，例如：

messages.debug: 調試信息

messages.info: 一般信息

- messages.success: 成功信息

- messages.warning: 警告信息

- messages.error: 錯誤信息

接下來，我們將展示如何在 Django 項目中使用 messages 框架，包括設置、顯示消息以及處理不同的消息類型。

### 14.1. 設置 Django messages 框架

messages 框架是 Django 的內建功能，通常默認已經啟用。我們只需要確保在項目的 settings.py 文件中，MIDDLEWARE 和 TEMPLATES 配置包含相關設置。

#### 14.1.1 確認 MIDDLEWARE 配置

確保 MIDDLEWARE 中包含 Django.contrib.messages.middleware.MessageMiddleware，這個中間件處理每個請求的消息存儲和顯示。

```
# settings.py
MIDDLEWARE = [
'django.middleware.security.SecurityMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware', # 確保這一行存在
'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```
#### 14.1.2 確認 context_processors 配置

在 TEMPLATES 設置中，確保 $ \underline{\text{django.contrib.messages.context_processors.messages}} $ 存在於 context_processors 列表中，這樣可以讓模板能夠訪問 messages。

```
# settings.py
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
'django.contrib.messages.context_processors.messages', # 確保這一行存在
],
},
]
]
```
### 14.2. 使用 messages 在視圖中傳遞消息

Django 提供了幾個內置的消息類型（如 success, error, warning 等），我們可以在視圖中調用這些消息類型，並將信息傳遞給模板進行顯示。

#### 14.2.1 使用 messages 在視圖中設置消息

以下是如何在 Django 視圖中使用消息系統的範例。假設我們有一個註冊用戶的視圖，註冊成功後，我們想顯示一個成功消息。

```
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '註冊成功！歡迎使用本網站。')
            return redirect('login')  # 註冊成功後跳轉到登錄頁面
        else:
            messages.error(request, '註冊失敗，請檢查表單內容。')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
```

在這個例子中，我們在表單提交成功後使用了 messages.success 來設置一個成功消息，而當表單提交失敗時，則使用 messages.error 來設置錯誤消息。

#### 14.2.2 messages 的其他類型

除了 success 和 error，Django 還有以下幾種類型的消息：

messages.debug(request, "這是一條調試信息"): 用於顯示調試信息。

messages.info(request, "這是一條信息消息"): 用於顯示一般信息。

messages.warning(request, "這是一條警告消息"): 用於顯示警告信息。

### 14.3. 在模板中顯示消息

我們需要在模板中遍歷並顯示所有傳遞過來的消息。Django 的 messages 系統會自動將消息傳遞到模板中，並且可以使用模板語法進行顯示。

#### 14.3.1 顯示消息的模板代碼

以下是顯示 messages 的標準模板代碼，它會遍歷所有的消息並根據消息類型來應用不同的樣式：

```
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
{% block title %}My Django Site{% endblock %}
<link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.9/dist/css/bootstrap.min.css"
rel="stylesheet"
```
>

```
</head>
<div class="container">
```
<!-- 消息顯示區域 -->

```
{% if messages %}
<div class="mt-3">
{% for message in messages %}
<div
class="alert alert-{{ message.tags }} alert-dismissible fade show"
role="alert"
```
>

```
{{ message }}
<button
type="button"
class="btn-close"
data-bs-dismiss="alert"
aria-label="Close"
```
></button>

```
</div>
{% endfor %}
</div>
{% endif %} {% block content %} {% endblock %}
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.9/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```
在這個範例中，alert alert-{{ message.tags }} 根據消息的類型（如 success, error, info）來設置不同的 Bootstrap 樣式，從而使消息顯示更加美觀。當用戶執行某個動作（如註冊或登錄）後，消息會顯示在頁面頂部，並帶有可關閉的按鈕。

### 14.4. messages 框架的進階設置

有時，我們希望自定義 messages 的一些行為，Django 提供了許多選項讓我們進行配置。

#### 14.4.1 更改消息的存儲方式

Django 默認使用 SessionStorage 來存儲消息，這意味著消息會存儲在會話中，並在下一個請求中顯示。你也可以選擇使用 CookieStorage 來存儲消息。你可以在 settings.py 中進行設置：

```
# settings.py
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
```
#### 14.4.2 自定義消息標籤

如果你想自定義消息的樣式類型，或者自定義每種消息的顯示方式，可以使用MESSAGE_TAGS來定義不同類型消息的樣式標籤。

```
# settings.py
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
message_constants.DEBUG: 'secondary',
message_constants.INFO: 'info',
message_constants.SUCCESS: 'success',
message_constants.WARNING: 'warning',
message_constants.ERROR: 'danger',
}
```
在這個範例中，我們將不同類型的消息對應到 Bootstrap 的樣式類別，例如將 message.error 對應到 danger 類別。

### 14.5. 常見應用場景

#### 14.5.1 註冊成功後顯示歡迎消息

當用戶成功註冊後，顯示一個歡迎消息：

messages.success(request, '恭喜！您的帳戶已成功創建。')

#### 14.5.2 登錄失敗後顯示錯誤消息

當用戶登錄失敗時，顯示一個錯誤消息提示：

messages.error(request, '登錄失敗，請檢查您的用戶名和密碼。')

#### 14.5.3 表單提交錯誤提示

當用戶提交的表單數據無效時，顯示一個錯誤提示消息：

messages.warning(request, '表單提交有誤

，請檢查輸入內容。)

### 14.6. 總結

Django 的 messages 框架是一個強大且靈活的工具，用於向用戶顯示各種類型的臨時消息。它可以提升用戶體驗，讓用戶清楚瞭解操作結果。通過與 Bootstrap 或其他前端框架結合，我們可以實現美觀且直觀的消息顯示。

本章涵蓋了從基礎到進階的 messages 使用方式，通過掌握這些技巧，你可以為應用添加實時反饋功能，並提升整體的用戶互動性。

15：設計並完成自定義 Django 項目

Django 是一個強大且靈活的 Web 框架，允許開發者快速構建高度定製化的應用。通過結合 Django 的內建功能與自定義邏輯，我們可以設計並完成一個符合具體需求的項目。本章將探討如何從零開始設計並完成一個自定義的 Django 項目，涵蓋項目設計思路、模型定義、視圖開發、模板渲染、前端美化、數據庫操作及部署等關鍵步驟。

本章的目標是幫助你掌握如何設計和開發一個完整的自定義 Django 項目，並提供實際的步驟來完成開發流程。

### 15.1. 項目設計與需求分析

在開發 Django 項目之前，首先要進行需求分析和項目設計。這是項目成功的基礎，清晰的目標和需求將決定項目結構、功能設計和技術選型。

#### 15.1.1 明確需求

假設我們的項目是一個簡單的事件管理系統，允許用戶創建、查看和報名參加事件。具體需求包括：

用戶能夠註冊、登錄系統。

用戶可以創建事件，設置時間、地點和詳細說明。

所有用戶都能查看事件列表和詳細內容。

用戶可以報名參加事件，並且系統會記錄報名人數。

管理員可以管理事件，包括編輯和刪除事件。

#### 15.1.2 設計項目結構

根據需求，我們將系統劃分為以下模塊：

1. 用戶系統：註冊、登錄、登出、密碼重置。

2. 事件管理系統：事件的創建、查看、編輯和刪除。

3. 報名系統：用戶能夠報名參加事件。

#### 15.1.3 數據庫模型設計

每個功能模塊的核心是數據庫模型，我們需要為事件和報名系統設計數據庫模型。

### 15.2. 建立 Django 項目

在分析完需求並設計結構後，我們可以開始實際開發。首先，創建一個新的 Django 項目和應用。

#### 15.2.1 創建項目與應用

使用 Django 自帶的命令行工具來創建項目和應用：

```
django-admin startproject eventmanager
cd eventmanager
python manage.py startapp events
```
eventmanager 是我們的主項目，而 events 則是用來處理事件管理和報名的應用。

在 settings.py 中添加我們的應用：

```
# settings.py
INSTALLED_APPS = [
'events',
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
]
```
#### 15.2.2 設置路由和應用結構

我們需要設置主路由來處理應用的 URL 路徑。在 eventmanager/urls.py 中包括 events 應用的 URL。

```
# eventmanager/urls.py
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
path('admin/', admin.site.urls),
path('events/', include('events.urls')), # 包含事件應用的路由
]
```
接下來，創建一個 $ \underline{\text{urls.py}} $ 文件來處理事件應用中的路由：

```
# events/urls.py
from django.urls import path
from . import views
urlpatterns = [
path(", views.event_list, name='event_list'),
path('create/', views.event_create, name='event_create'),
path('<int:id>', views.event_detail, name='event_detail'),
path('<int:id>/edit/, views.event_edit, name='event_edit'),
path('<int:id>/delete/, views.event_delete, name='event_delete'),
]
```
### 15.3. 設計數據庫模型

接下來，我們將定義項目中的數據庫模型，這將是整個應用邏輯的核心部分。每個事件應該有標題、時間、地點、描述以及最大報名人數。用戶可以通過事件的 ID 進行報名。

#### 15.3.1 定義事件模型

在 models.py 文件中定義事件和報名模型：

```
# events/models.py
from django.db import models
from django.contrib.auth.models import User
class Event(models.Model):
title = models.CharField(max_length=200)
description = models.TextField()
location = models.CharField(max_length=200)
event_date = models.DateTimeField()
max_attendees = models.PositiveIntegerField()
created_by = models.ForeignKey(User, on_delete=models.CASCADE)
created_at = models.DateTimeField(auto_now_add=True)
def __str__(self):
return self.title
class Registration(models.Model):
event = models.ForeignKey(Event, related_name=registrations', on_delete=models.CASCADE)
user = models.ForeignKey(User, on_delete=models.CASCADE)
registered_at = models.DateTimeField(auto_now_add=True)
def __str__(self):
return f{'self.user.username} registered for {self.event.title}
```
這裡我們定義了兩個模型：

- Event 模型包含事件的所有信息。

- Registration 模型記錄了用戶報名的事件。

運行遷移命令以將模型應用到數據庫中：

```
python manage.py makemigrations
python manage.py migrate
```
### 15.4. 開發視圖與業務邏輯

有了數據模型後，我們需要編寫視圖來處理數據邏輯和業務操作，如創建事件、編輯事件、查看事件詳情等。

#### 15.4.1 創建和查看事件

我們首先編寫事件的創建和查看視圖。

```
# events/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from .forms import EventForm
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user # 將當前用戶設為創建者
            event.save()
            return redirect('event_list')
        else:
            form = EventForm()
            return render(request, 'events/event_form.html', {'form': form})
def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, 'events/event_detail.html', {'event': event})
```
在這裡，我們創建了三個視圖：

1. event_list：顯示所有事件列表。

2. event_create：處理創建新事件的邏輯。

3. event_detail：顯示事件的詳細信息。

#### 15.4.2 編輯與刪除事件

管理員應能夠編輯和刪除事件，我們也需要編寫這些操作的視圖：

```
def event_edit(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', id=event.id)
        else:
            form = EventForm(instance=event)
            return render(request, 'events/event_form.html', {'form': form})
def event_delete(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
        return render(request, 'events/event_confirm_delete.html', {'event': event})
```
### 15.5. 使用 Django 表單處理用戶輸入

為了處理事件的創建和編輯，我們需要使用 Django 表單來獲取用戶輸入數據。首先，創建一個 forms.py 文件。

```
# events/forms.py
from Django import forms
from .models import Event
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'event_date', 'max_attendees']
```
這個表單將生成一個事件的輸入表單，包含事件的標題、描述、地點等信息。

### 15.6. 報名系統

除了事件管理，我們還需要為用戶提供報名參加事件的功能。

#### 15.6.1 報名邏輯

在 views.py 中添加報名功能：

```
from .models import Registration
def event_register(request, id):
    event = get_object_or_404(Event, id=id)
    if Registration.objects.filter(event=event, user=request.user).exists():
        # 如果用戶已經報名，則提示錯誤
        messages.error(request, '你已經報名過此活動。')
    elif event.registrations.count() >= event.max_attendees:
        # 如果報名已滿
        pass  # 內容省略
```
```
elif event.registrations.count() >= event.max_attendees:
# 如果報名已滿
messages.error(request, '報名已滿。')
else:
# 添加報名
Registration.objects.create(event=event, user=request.user)
```
messages.success(request, '成功報名活動！')

```
return redirect('event_detail', id=event.id)
```
15.7. 美化前端：使用 Bootstrap

為了讓頁面更加美觀，我們可以使用 Bootstrap 來美化前端。這部分我們在模板文件中引入 Bootstrap，並將表單和按鈕進行樣式化。

範例模板：

```
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
Event Manager</title>
<link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.9/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<div class="container mt-5">{% block content %} {% endblock %} </div>
</body>
</html>
```
### 15.8. 項目部署

開發完成後，項目需要部署到生產環境。使用工具如 Gunicorn 作為應用服務器，並將 Nginx 作為反向代理來處理靜態文件。數據庫可以使用 PostgreSQL 來替代開發時使用的 SQLite，以確保數據安全和應用穩定性。

### 15.9. 總結

本章中，我們學習瞭如何設計並完成一個自定義的 Django 項目，並且通過需求分析、數據庫模型設計、視圖開發以及前端美化的步驟，實現了一個完整的事件管理系統。我們還學習瞭如何使用 Django 的表單和消息框架處理用戶交互，並在完成後部署應用到生產環境。

參考資料：

```
https://docs.djangoproject.com/en/5.2/
```
