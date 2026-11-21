# 第 9 章 · URL 路由、視圖與模板

## 1. Django 視圖的基本概念

### 1.1 視圖的作用

視圖是 Django 處理 HTTP 請求的主要組件。請求進來後，Django 會依 URL 路由到對應視圖；視圖負責：

- **處理請求**：接收並解析請求中的資料（查詢參數、表單資料等）。
- **執行業務邏輯**：資料庫查詢、計算等。
- **回傳回應**：依結果產生 HTTP 回應（HTML、JSON、重定向等）。

### 1.2 視圖的類型

1. **函數視圖（FBV）**：用 Python 函數實作，簡單直觀，適合小型專案。
2. **類視圖（CBV）**：用 Python 類實作，透過繼承與方法覆寫擴充，可重用性高，適合複雜邏輯。

## 2. 函數視圖（FBV）

### 2.1 基本結構

接受 `request`、回傳 `HttpResponse` 的普通函數：

```
# myapp/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("歡迎來到我的網站！")
```

### 2.2 處理 GET 與 POST

用 `request.method` 判斷請求類型：

```
# myapp/views.py
from django.shortcuts import render
from django.http import HttpResponse

def contact(request):
    if request.method == 'POST':
        return HttpResponse("表單已成功提交！")   # 處理表單
    else:
        return render(request, 'contact.html')     # 顯示空表單
```

### 2.3 用上下文渲染模板

用 `render()` 把「上下文資料 + 模板」結合成 HTML：

```
# myapp/views.py
from django.shortcuts import render

def index(request):
    context = {
        'title': '我的首頁',
        'welcome_message': '歡迎來到我的網站！',
    }
    return render(request, 'index.html', context)
```

### 2.4 處理表單資料

用 `request.POST` 取得表單欄位：

```
# myapp/views.py
from django.http import HttpResponse

def submit_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        return HttpResponse(f"姓名: {name}, 電子郵件: {email}")
    return HttpResponse("請通過 POST 提交表單")
```

<figure class="fig-svg"><svg viewBox="0 0 700 212" width="100%" role="img" aria-label="函數視圖 FBV 與類視圖 CBV 的對照" style="background:#0d1117;border-radius:10px"><g font-family="'Microsoft JhengHei','Segoe UI',sans-serif"><rect x="24" y="20" width="310" height="172" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="179" y="48" text-anchor="middle" font-size="14" fill="#e6edf3">函數視圖 FBV</text><text x="44" y="80" font-family="'Consolas','Menlo',monospace" font-size="12.5" fill="#39d0d8">def index(request):</text><text x="44" y="104" font-family="'Consolas','Menlo',monospace" font-size="12.5" fill="#39d0d8">    return HttpResponse(...)</text><text x="44" y="142" font-size="12" fill="#e6edf3">簡單直觀、適合小型專案</text><text x="44" y="164" font-size="12" fill="#e6edf3">以 request.method 判斷方法</text><rect x="366" y="20" width="310" height="172" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="521" y="48" text-anchor="middle" font-size="14" fill="#e6edf3">類視圖 CBV</text><text x="386" y="80" font-family="'Consolas','Menlo',monospace" font-size="12.5" fill="#39d0d8">class IndexView(View):</text><text x="386" y="104" font-family="'Consolas','Menlo',monospace" font-size="12.5" fill="#39d0d8">    def get(self, request): ...</text><text x="386" y="142" font-size="12" fill="#e6edf3">可繼承重用、結構化</text><text x="386" y="164" font-size="12" fill="#e6edf3">URL 以 .as_view() 掛載</text></g><figcaption>圖：函數視圖（FBV）與類視圖（CBV）。</figcaption></svg></figure>

## 3. 類視圖（CBV）

### 3.1 基本概念

類視圖把邏輯封裝進類，每個 HTTP 方法對應一個方法（`get()`、`post()`），適合複雜、需重用的視圖。

```
# myapp/views.py
from django.http import HttpResponse
from django.views import View

class IndexView(View):
    def get(self, request):
        return HttpResponse("歡迎來到我的網站！")
```

### 3.2 內建通用視圖

Django 提供多個通用類視圖，常用：

- **TemplateView**：渲染靜態模板。
- **RedirectView**：重定向到指定 URL。

```
# myapp/views.py
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = 'about.html'
```

### 3.3 在 urls.py 使用類視圖

類視圖要用 `.as_view()` 轉成可呼叫的視圖：

```
from django.urls import path
from .views import IndexView, AboutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
]
```
## 4. 模板（Template）系統

模板負責把視圖傳來的資料渲染成 HTML。

### 4.1 模板設定

在 `settings.py` 的 `TEMPLATES` 指定模板目錄；慣例放在 App 的 `templates/` 下。

### 4.2 模板語法

- **變數**：`{{ variable }}`
- **標籤**：`{% tag %}`
- **註解**：`{# comment #}`

```
<h1>{{ title }}</h1>
<p>{{ welcome_message }}</p>
{% if user.is_authenticated %}歡迎，{{ user.username }}{% endif %}
```

### 4.3 模板繼承

以基礎模板定義共用結構，子模板覆蓋其中的區塊。

<figure class="fig-svg"><svg viewBox="0 0 860 272" width="100%" role="img" aria-label="Django 模板繼承：base.html 被三個子模板 extends" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="300" y="20" width="260" height="62" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="430" y="45" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">base.html</text><text x="430" y="65" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">{% block content %}</text><rect x="30" y="170" width="210" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="135" y="195" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">index.html</text><text x="135" y="215" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">extends base.html</text><rect x="320" y="170" width="210" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="425" y="195" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">article.html</text><text x="425" y="215" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">extends base.html</text><rect x="610" y="170" width="210" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="715" y="195" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">about.html</text><text x="715" y="215" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">extends base.html</text><line x1="135" y1="170" x2="430" y2="86" stroke="#39d0d8" stroke-width="1.6" marker-start="url(#a)"/><line x1="425" y1="170" x2="430" y2="86" stroke="#39d0d8" stroke-width="1.6" marker-start="url(#a)"/><line x1="715" y1="170" x2="430" y2="86" stroke="#39d0d8" stroke-width="1.6" marker-start="url(#a)"/><text x="430" y="256" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#f0a04b">{% block content %} 由子模板覆寫，其餘沿用 base.html</text></svg><figcaption>圖　模板繼承：子模板 <code>{% extends "base.html" %}</code>，只覆寫自己需要的 block，共用導覽列與頁尾。</figcaption></figure>

**基礎模板**

```
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}我的網站{% endblock %}</title>
</head>
<body>
    <header><h1>我的網站標題</h1></header>
    <nav>
        <ul>
            <li><a href="/">首頁</a></li>
            <li><a href="/about/">關於我們</a></li>
        </ul>
    </nav>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer><p>&copy; 2024 我的網站</p></footer>
</body>
</html>
```

**子模板**

```
<!-- templates/index.html -->
{% extends 'base.html' %}
{% block title %}首頁 - 我的網站{% endblock %}
{% block content %}
    <h2>歡迎來到我的網站！</h2>
    <p>這是首頁的具體內容。</p>
{% endblock %}
```

- `{% block 名稱 %}`：可被子模板覆蓋的區塊。
- `{% extends 'base.html' %}`：繼承基礎模板。

### 4.4 模板過濾器

過濾器（用 `|`）用來修改變數輸出：

```
<p>當前日期：{{ current_date|date:"Y-m-d" }}</p>
<p>文章數量：{{ num_posts|default:"暫無文章" }}</p>
```

- `date`：格式化日期。
- `default`：變數為空時提供預設值。

### 4.5 自定義過濾器與標籤

放在 App 的 `templatetags/` 下，先 `register = template.Library()`。

**自定義過濾器**

```
# myapp/templatetags/my_filters.py
from django import template
register = template.Library()

@register.filter(name='add_exclamation')
def add_exclamation(value):
    return f"{value}!"
```

```
<!-- templates/index.html -->
{{ welcome_message|add_exclamation }}
```

**自定義標籤**

```
# myapp/templatetags/my_tags.py
from django import template
register = template.Library()

@register.simple_tag
def multiply(a, b):
    return a * b
```

```
<!-- templates/calculate.html -->
{% load my_tags %}
<p>結果：{% multiply 5 3 %}</p>
```

## 5. 本章總結

本章介紹了 Django 的**視圖**（函數視圖、類視圖）與**模板**系統（語法、上下文渲染、模板繼承、過濾器與自定義標籤），是打造動態頁面的核心。
