# 第 11 章 · 分頁、美化、認證與專案實作

## 1. 分頁（Pagination）

### 1.1 基本概念

把大數據集切成多頁，讓使用者逐頁瀏覽：每頁固定筆數、提供導覽（上一頁／下一頁／特定頁）、顯示當前頁與總頁數。Django 內建 `Paginator` 處理分頁邏輯。

### 1.2 使用 Paginator

`Paginator(物件列表, 每頁筆數)`；`get_page(頁碼)` 會處理無效頁碼。

```
# myapp/views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Article

def article_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 10)          # 每頁 10 筆
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'article_list.html', {'page_obj': page_obj})
```

### 1.3 模板顯示分頁

`page_obj` 含當前頁資料與分頁資訊（是否有上／下一頁等）。

```
<!-- templates/article_list.html -->
<ul>
{% for article in page_obj %}
    <li>{{ article.title }}</li>
{% endfor %}
</ul>

<div class="pagination">
    <span>第 {{ page_obj.number }} 頁，共 {{ page_obj.paginator.num_pages }} 頁</span>
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">上一頁</a>
    {% endif %}
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">下一頁</a>
    {% endif %}
</div>
```

### 1.4 保留查詢參數

篩選後分頁時，要讓其他查詢參數保留在 URL 中：

```
# myapp/views.py
def article_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']              # 移除 page，避免重複
    query_string = query_params.urlencode()
    return render(request, 'article_list.html', {'page_obj': page_obj, 'query_string': query_string})
```

```
<a href="?page={{ page_obj.previous_page_number }}&{{ query_string }}">上一頁</a>
```

### 1.5 自訂每頁數量

```
# myapp/views.py
def article_list(request):
    articles = Article.objects.all()
    per_page = request.GET.get('per_page', 10)    # 預設每頁 10 筆
    paginator = Paginator(articles, per_page)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'article_list.html', {'page_obj': page_obj})
```

```
<select name="per_page" onchange="this.form.submit()">
    <option value="5" {% if page_obj.paginator.per_page == 5 %}selected{% endif %}>5</option>
    <option value="10" {% if page_obj.paginator.per_page == 10 %}selected{% endif %}>10</option>
</select>
```

### 1.6 只顯示附近頁碼

```
{% for num in page_obj.paginator.page_range %}
    {% if num >= page_obj.number|add:"-2" and num <= page_obj.number|add:"2" %}
        {% if num == page_obj.number %}
            <span>{{ num }}</span>
        {% else %}
            <a href="?page={{ num }}">{{ num }}</a>
        {% endif %}
    {% endif %}
{% endfor %}
```

### 1.7 Ajax 分頁

不刷新整頁，改用 Ajax 取回部分 HTML：

```
# myapp/views.py
from django.template.loader import render_to_string
from django.http import JsonResponse

def article_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/article_list.html', {'page_obj': page_obj})
        return JsonResponse({'html': html})
    return render(request, 'article_list.html', {'page_obj': page_obj})
```

```
<!-- partials/article_list.html -->
{% for article in page_obj %}
    <li>{{ article.title }}</li>
{% endfor %}
```

### 1.8 小結

用 `Paginator` 即可分頁；可保留查詢參數、自訂每頁數量、只顯示附近頁碼，並以 Ajax 做到無刷新分頁。
## 2. Django 與 Bootstrap 整合

Bootstrap 是由 Twitter 開發的開源前端框架，提供大量預設樣式、版面系統與組件（導覽列、按鈕、表單、卡片、模態框等），並內建響應式網格，能快速做出美觀、自適應的頁面。

### 2.1 為什麼用 Bootstrap

- **快速開發**：現成樣式與組件，不必從頭設計。
- **響應式**：自動適應不同螢幕尺寸。
- **設計一致**：各頁風格統一。
- **可擴充**：可自訂與擴展樣式。

### 2.2 用 CDN 引入

```
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Django Site{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.9/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    {% block content %}{% endblock %}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.9/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### 2.3 網格系統

Bootstrap 採 **12 欄** 網格，用 `row` / `col-*` 排版：

```
<!-- templates/home.html -->
{% extends 'base.html' %}
{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-4">
            <div class="card"><div class="card-body">
                <h5 class="card-title">欄目 1</h5>
                <p class="card-text">這是第一個欄目中的內容。</p>
            </div></div>
        </div>
        <div class="col-md-4">
            <div class="card"><div class="card-body">
                <h5 class="card-title">欄目 2</h5>
                <p class="card-text">這是第二個欄目中的內容。</p>
            </div></div>
        </div>
        <div class="col-md-4">
            <div class="card"><div class="card-body">
                <h5 class="card-title">欄目 3</h5>
                <p class="card-text">這是第三個欄目中的內容。</p>
            </div></div>
        </div>
    </div>
</div>
{% endblock %}
```

### 2.4 美化表單（django-widget-tweaks）

```
pip install django-widget-tweaks
```

```
# settings.py
INSTALLED_APPS = [
    'widget_tweaks',
    # ...
]
```

```
<!-- templates/register.html -->
{% extends 'base.html' %}
{% load widget_tweaks %}
{% block content %}
<div class="container mt-5">
    <h2>註冊</h2>
    <form method="post">
        {% csrf_token %}
        <div class="mb-3">{{ form.username|add_class:"form-control" }}</div>
        <div class="mb-3">{{ form.email|add_class:"form-control" }}</div>
        <div class="mb-3">{{ form.password1|add_class:"form-control" }}</div>
        <div class="mb-3">{{ form.password2|add_class:"form-control" }}</div>
        <button type="submit" class="btn btn-primary">註冊</button>
    </form>
</div>
{% endblock %}
```

### 2.5 美化管理後台（django-admin-interface）

```
pip install django-admin-interface
```

```
# settings.py
INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    # ...
]
```

```
python manage.py migrate
```

安裝後可在後台的 **Theme** 設定配色與版面。

### 2.6 常用組件

**導覽列（Navbar）**

```
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">我的網站</a>
        <button class="navbar-toggler" type="button"
                data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item"><a class="nav-link active" href="#">首頁</a></li>
                <li class="nav-item"><a class="nav-link" href="#">功能</a></li>
                <li class="nav-item"><a class="nav-link" href="#">聯繫我們</a></li>
            </ul>
        </div>
    </div>
</nav>
```

**模態框（Modal）**

```
<button type="button" class="btn btn-primary"
        data-bs-toggle="modal" data-bs-target="#exampleModal">
    打開模態框
</button>

<div class="modal fade" id="exampleModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">模態框標題</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">這是模態框的內容</div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">關閉</button>
                <button type="button" class="btn btn-primary">保存變更</button>
            </div>
        </div>
    </div>
</div>
```

### 2.7 小結

用 CDN 引入 Bootstrap 即可美化頁面；搭配網格、卡片、表單樣式與常用組件（Navbar／Modal），能快速做出響應式介面；後台可用 `django-admin-interface` 美化。
## 3. 用戶註冊與登入

Django 內建認證框架，涵蓋註冊／登入、密碼加密、身份驗證、權限控制、登出與密碼重設。

### 3.1 建立專案與 App

```
django-admin startproject myproject
cd myproject
python manage.py startapp accounts
```

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

### 3.2 用戶註冊（UserCreationForm）

```
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)          # 自動登入
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
```

```
# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
]
```

```
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]
```

```
<!-- templates/accounts/register.html -->
<h2>註冊</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">註冊</button>
</form>
```

存取 `/accounts/register/` 即可看到註冊表單並建立帳號。

### 3.3 登入與登出

Django 提供內建的 `LoginView` 與 `LogoutView`。

<figure class="fig-svg"><svg viewBox="0 0 800 262" width="100%" role="img" aria-label="Django 認證流程：表單、authenticate、login 寫入 session、登出需用 POST" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="95" width="150" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="95" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">登入表單</text><text x="95" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">POST 帳號密碼</text><rect x="210" y="95" width="160" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="290" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">authenticate()</text><text x="290" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">驗證帳密</text><rect x="410" y="95" width="150" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="485" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">login()</text><text x="485" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">寫入 session</text><rect x="600" y="95" width="150" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="675" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">登入後頁面</text><text x="675" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">redirect</text><rect x="210" y="12" width="160" height="58" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="290" y="35" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">驗證失敗</text><text x="290" y="55" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">回表單顯示錯誤</text><rect x="395" y="190" width="180" height="58" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="485" y="213" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">登出</text><text x="485" y="233" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">LogoutView（只收 POST）</text><line x1="170" y1="126" x2="206" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="290" y1="95" x2="290" y2="74" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="370" y1="126" x2="406" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="560" y1="126" x2="596" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="485" y1="157" x2="485" y2="186" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="560" y1="219" x2="690" y2="160" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/></svg><figcaption>圖　認證流程：<code>authenticate()</code> 驗證帳密，成功才呼叫 <code>login()</code> 寫入 session；登出走 <code>LogoutView</code>，Django 5.0 起只接受 POST。</figcaption></figure>

```
# accounts/urls.py
from django.contrib.auth import views as auth_views

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
```

```
<!-- templates/accounts/login.html -->
<h2>登錄</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">登錄</button>
</form>
```

**注意**：Django 5.0 起 `LogoutView` 只接受 **POST**（已移除 GET 登出）。模板要用表單提交：

```
<form method="post">
    {% csrf_token %}
    <button type="submit">登出</button>
</form>
```

不能用 `<a href>` 連結登出。

### 3.4 小結

用 Django 內建認證即可快速完成註冊、登入、登出與權限控制；`UserCreationForm`、`LoginView`、`LogoutView` 是最常用的工具。
## 4. Messages 框架

`messages` 用於在使用者操作後顯示一次性提示（成功、錯誤、警告等），常搭配 Bootstrap alert。

### 4.1 使用 messages

```
# accounts/views.py
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '註冊成功！歡迎使用本網站。')
            return redirect('login')
        else:
            messages.error(request, '註冊失敗，請檢查表單內容。')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
```

### 4.2 訊息類型

- `messages.debug(request, "…")`：除錯訊息
- `messages.info(request, "…")`：一般訊息
- `messages.success(request, "…")`：成功
- `messages.warning(request, "…")`：警告
- `messages.error(request, "…")`：錯誤

### 4.3 在模板顯示

```
<!-- templates/base.html -->
{% if messages %}
<div class="mt-3">
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    {% endfor %}
</div>
{% endif %}
```

`alert-{{ message.tags }}` 會依訊息類型套用對應的 Bootstrap 樣式。

### 4.4 進階設定

更改儲存方式（預設 SessionStorage）：

```
# settings.py
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
```

自訂訊息標籤對應的樣式：

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

### 4.5 常見應用

- 註冊成功：`messages.success(request, '恭喜！您的帳戶已成功創建。')`
- 登錄失敗：`messages.error(request, '登錄失敗，請檢查您的用戶名和密碼。')`
- 表單驗證失敗：`messages.warning(request, '表單提交有誤，請檢查輸入內容。')`

### 4.6 小結

`messages` 提供一次性的使用者提示，搭配 Bootstrap alert 美觀好讀；也可自訂訊息標籤與儲存方式。
## 5. 專案實作：事件管理系統

以「事件管理」為例，示範從需求到部署的完整流程。

### 5.1 需求與專案結構

**需求**：用戶可註冊／登入；建立、查看、編輯、刪除事件；查看事件列表與詳情；報名活動並記錄人數；管理員可管理事件。

**模組**：用戶系統、事件管理、報名系統。

### 5.2 建立專案

```
django-admin startproject eventmanager
cd eventmanager
python manage.py startapp events
```

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

```
# eventmanager/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
]
```

```
# events/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('<int:id>/', views.event_detail, name='event_detail'),
    path('<int:id>/edit/', views.event_edit, name='event_edit'),
    path('<int:id>/delete/', views.event_delete, name='event_delete'),
]
```

### 5.3 資料庫模型

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
    event = models.ForeignKey(Event, related_name='registrations', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} registered for {self.event.title}'
```

```
python manage.py makemigrations
python manage.py migrate
```

### 5.4 表單

```
# events/forms.py
from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'event_date', 'max_attendees']
```

### 5.5 視圖

```
# events/views.py
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Registration
from .forms import EventForm

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user     # 將當前用戶設為創建者
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, 'events/event_detail.html', {'event': event})

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

def event_register(request, id):
    event = get_object_or_404(Event, id=id)
    if Registration.objects.filter(event=event, user=request.user).exists():
        messages.error(request, '你已經報名過此活動。')
    elif event.registrations.count() >= event.max_attendees:
        messages.error(request, '報名已滿。')
    else:
        Registration.objects.create(event=event, user=request.user)
        messages.success(request, '成功報名活動！')
    return redirect('event_detail', id=event.id)
```

### 5.6 前端（Bootstrap）

```
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Event Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.9/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">{% block content %}{% endblock %}</div>
</body>
</html>
```

### 5.7 部署

以 **Gunicorn** 作為應用伺服器、**Nginx** 作為反向代理與靜態檔服務；資料庫改用 **PostgreSQL**，以確保資料安全與應用穩定。

### 5.8 小結

以事件管理系統為例，走過需求分析 → 建專案 → 模型 → 表單 → 視圖 → 前端 → 部署的完整流程。

**參考資料**：https://docs.djangoproject.com/en/5.2/
