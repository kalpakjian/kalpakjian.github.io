# 第 9 章 · URL 路由、視圖與模板

### 5.1 Django 視圖的基本概念

#### 5.1.1 視圖的作用

視圖是 Django 應用中處理 HTTP 請求的主要組件。當用戶在瀏覽器中輸入 URL 並發送請求時，Django 會將該請求路由到對應的視圖。視圖可以根據請求中的數據進行處理，如查詢數據庫、處理表單數據或執行其他業務邏輯，然後生成並返回一個響應。

視圖的主要功能包括：

處理請求：視圖接收用戶的請求，並解析請求中的數據（如查詢參數、表單數據等）。

執行業務邏輯：視圖執行應用中的核心業務邏輯，如數據庫查詢、數據計算或其他處理。

- 返回響應：視圖根據處理結果生成相應的 HTTP 響應，這可以是動態生成的 HTML 頁面、JSON 數據或重定向等。

#### 5.1.2 視圖的類型

在 Django 中，視圖有兩種主要的實現方式：

1. 函數視圖（Function-based Views，FBV）：視圖用 Python 函數實現，處理 HTTP 請求並返回響應。

2. 類視圖（Class-based Views，CBV）：視圖用 Python 類實現，將業務邏輯封裝到類方法中，提供了更靈活和可重用的結構。

兩種視圖的區別在於組織方式和擴展性。函數視圖簡單直觀，適合小型項目或簡單的邏輯，而類視圖通過面向對象的方式提供了更強的擴展性，適合處理複雜的應用邏輯。

### 5.2 函數視圖

#### 5.2.1 函數視圖的基本結構

函數視圖（Function-based Views, FBV）是最簡單的視圖實現方式。它是一個接受HTTP請求對象並返回HTTP響應對象的普通Python函數。函數視圖的結構簡單，直接處理請求並返回結果。

範例：簡單的函數視圖

```
# myapp/views.py
from django.http import HttpResponse
def index(request):
```
return HttpResponse("歡迎來到我的網站！")

在這個例子中，index 函數接受一個 request 對象，該對象包含了所有關於當前 HTTP 請求的信息。函數返回一個 HttpResponse，即一個簡單的包含 "歡迎來到我的網站！" 字符串的響應。

#### 5.2.2 處理 GET 和 POST 請求

在 Django 中，視圖可以處理多種 HTTP 方法，如 GET 和 POST。GET 請求通常用於從伺服器獲取數據（如加載網頁），而 POST 請求用於提交數據（如表單提交）。函數視圖可以通過 request.method 來檢查請求的類型並做出不同的響應。

範例：處理 GET 和 POST 請求

```
# myapp/views.py
from django.shortcuts import render
from django.http import HttpResponse
def contact(request):
if request.method == 'POST':
# 處理表單提交邏輯
```
return HttpResponse("表單已成功提交！")

```
else:
# 返回空的表單頁面
return render(request, 'contact.html')
```
在這個例子中，當用戶通過 GET 請求訪問 /contact/ 時，Django 會返回一個帶有表單的頁面（contact.html）；當用戶提交表單後，POST 請求被發送到同一個視圖，視圖將處理表單數據並返回成功消息。

#### 5.2.3 使用上下文數據渲染模板

函數視圖通常需要將數據傳遞給模板來生成動態內容。Django 提供了 render() 函數來將視圖中的上下文數據與模板結合，從而生成 HTML 響應。

範例：將上下文數據傳遞給模板

```
# myapp/views.py
from django.shortcuts import render
def index(request):
context = {
```
'title': '我的首頁',

'welcome_message': '歡迎來到我的網站！'

```
}
return render(request, 'index.html', context)
```
在這個例子中，我們將上下文數據（title 和 welcome_message）傳遞給 index.html 模板，模板可以使用這些數據來生成最終的 HTML 頁面。

#### 5.2.4 處理表單數據

視圖不僅僅用於顯示靜態頁面，它們還可以處理用戶提交的表單數據。當用戶通過表單提交數據後，視圖可以從 request.POST 中獲取表單數據並進行處理。

範例：處理表單提交

```
# myapp/views.py
from django.http import HttpResponse
def submit_form(request):
if request.method == 'POST':
name = request.POST.get('name')
email = request.POST.get('email')
```
return HttpResponse(f"姓名: {name}, 電子郵件: {email}")

return HttpResponse("請通過 POST 提交表單")

在這個例子中，我們處理了一個簡單的表單提交，從 POST 請求中獲取了用戶輸入的 name 和 email，並返回了它們。

### 5.3 類視圖

#### 5.3.1 類視圖的基本概念

類視圖（Class-based Views, CBV）是 Django 提供的一種更結構化的視圖實現方式。它將視圖邏輯封裝到類中，並通過類的繼承和方法覆蓋來擴展和重用視圖邏輯。類視圖的主要優勢在於代碼重用和結構化設計，適合處理更複雜的視圖邏輯。

類視圖中，每個 HTTP 請求方法（如 GET、POST）對應於類中的不同方法，如 get() 和 post()。這使得代碼更加清晰且便於擴展。

範例：簡單的類視圖

```
# myapp/views.py
from django.http import HttpResponse
from django.views import View
class IndexView(View):
def get(self, request):
```
return HttpResponse("歡迎來到我的網站！")在這個例子中，IndexView 是一個類視圖，我們使用 get() 方法來處理 GET 請求，並返回一個簡單的文本響應。

#### 5.3.2 基本類視圖的使用

Django 提供了一些內建的基礎類視圖，如 TemplateView 和 RedirectView，它們可以用來簡化常見的視圖操作。

```
TemplateView
```
TemplateView 是一個常用的類視圖，用來渲染靜態模板並返回 HTML 響應。當你只需要顯示一個簡單的模板頁面時，TemplateView 是一個不錯的選擇。

範例：使用 TemplateView 渲染模板

```
# myapp/views.py
from django.views.generic import TemplateView
class AboutView(TemplateView):
template_name = 'about.html'
```
這個視圖將渲染 about.html 模板，並返回其內容作為響應。template_name 屬性指定了模板的路徑。

```
RedirectView
```
RedirectView 用於將用戶重定向到另一個 URL。它非常適合處理頁面遷移或重定向。

範例：使用 RedirectView 進行重定向

```
# myapp/views.py
from django.views.generic import RedirectView
class HomeRedirectView(RedirectView):
url = '/home/'
```
這個視圖會將所有對 HomeRedirectView 的請求重定向到 /home/ URL。

#### 5.3.3 處理 GET 和 POST 請求

類視圖通過將每個 HTTP 方法映射到對應的方法來處理請求。例如，get() 方法用於處理 GET 請求，而 post() 方法則用於處理 POST 請求。你可以在一個類視圖中同時定義這些方法，從而更靈活地處理不同類型的請求。

範例：處理 GET 和 POST 請求的類視圖

```
# myapp/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
class ContactView(View):
def get(self, request):
return render(request, 'contact.html')
def post(self, request):
name = request.POST.get('name')
message = request.POST.get('message')
```
return HttpResponse(f"收到來自 {name} 的信息: {message}")

在這個範例中，ContactView 視圖使用 get() 方法返回一個空白表單頁面，使用 post() 方法來處理表單提交並返回結果。

#### 5.3.4 繼承與覆蓋

類視圖的另一個強大特性是 繼承 和 方法覆蓋。你可以創建一個基礎類視圖，並通過繼承來擴展其功能。這樣可以減少代碼重複，並提高代碼的可維護性。

範例：使用繼承擴展類視圖

```
# myapp/views.py
class BaseView(View):
def get(self, request):
```
return HttpResponse("這是基礎視圖")

```
class CustomView(BaseView):
def get(self, request):
response = super().get(request)
```
return HttpResponse(response.content + b" 並且這是自定義的內容")

在這個範例中，CustomView 繼承自 BaseView，並通過 super() 調用了父類的 get() 方法，同時在響應中添加了自定義內容。

### 5.4 視圖與 URL 的連接

#### 5.4.1 函數視圖與 URL 的連接

在 Django 中，視圖與 URL 的連接是通過 urls.py 文件中的 path() 函數來實現的。無論是函數視圖還是類視圖，都可以通過 path() 與特定的 URL 路徑進行關聯。

範例：將函數視圖與 URL 連接

```
# myapp/urls.py
from django.urls import path
from .import views
urlpatterns = [
```
path("views.index, name='index'), # 連接函數視圖

```
]
```
這裡，我們將 index 函數視圖與根 URL (/) 進行了連接。

#### 5.4.2 類視圖與 URL 的連接

對於類視圖，你需要使用 as_view() 方法來將類轉換為可以處理請求的可調用對象。as_view() 方法會返回一個類視圖的實例，並將其與 URL 進行綁定。

範例：將類視圖與 URL 連接

```
# myapp/urls.py
from django.urls import path
from .views import IndexView
urlpatterns = [
```
path("IndexView.as_view(), name='index'), # 連接類視圖

```
]
```
在這裡，我們使用 IndexView.as_view() 來將類視圖與 URL 進行連接。

### 5.5 視圖中的上下文與模板交互

#### 5.5.1 使用上下文數據渲染模板

視圖通常需要與模板進行交互，從而生成動態的 HTML 頁面。在視圖中，我們可以將數據放入上下文（Context）中，然後將這些數據傳遞給模板進行渲染。

範例：傳遞上下文數據到模板

```
# myapp/views.py
from django.shortcuts import render
def index(request):
context = {
```
'title': '我的首頁',

'welcome_message': '歡迎來到我的網站！'

```
}
}
}
return render(request, 'index.html', context)
```
在這個範例中，我們將上下文數據（title 和 welcome_message）傳遞給 index.html 模板。模板可以使用這些數據來生成最終的 HTML 頁面。

#### 5.5.2 在類視圖中使用上下文

類視圖中的上下文數據可以通過覆蓋 get_context_data() 方法來傳遞。get_context_data() 方法允許我們向模板添加額外的上下文數據。

範例：在類視圖中傳遞上下文數據

```
# myapp/views.py
from django.views.generic import TemplateView
class IndexView(TemplateView):
template_name = 'index.html'
def get_context_data(self, **kwargs):
context = super().get_context_data(**kwargs)
```
context['title'] = '我的首頁'

context['welcome_message'] = '歡迎來到我的網站！'

```
return context
```
在這裡，我們覆蓋了 get_context_data() 方法，將 title 和 welcome_message 添加到上下文中，然後傳遞給模板進行渲染。

### 5.6 總結

在本章中，我們詳細介紹了 Django 中的 視圖系統，包括 函數視圖 和 類視圖 的基本概念與應用。我們學習瞭如何通過視圖來處理 GET 和 POST 請求，並瞭解了視圖與 URL 之間的連接方式。同時，我們探討瞭如何在視圖中使用上下文數據來渲染模板，以生成動態的 HTML 頁面。

6: Django 的模板系統

模板（Template）是 Django 用來渲染動態 HTML 頁面的系統，它將後端數據與 HTML 結合，從而生成用戶可以在瀏覽器中查看的內容。Django 的模板系統提供了靈活的語法，允許開發者在模板中嵌入變量和表達式，還支持模板繼承、過濾器、自定義標籤等高級功能。

在本章中，我們將深入探討 Django 模板系統的基礎知識，學習如何使用模板語法來渲染上下文數據，實現頁面模塊化的 模板繼承，並瞭解 模板過濾器和 自定義模板標籤 的應用。

### 6.1 Django 模板的基本概念

#### 6.1.1 模板的作用

Django 中的模板是用來生成動態 HTML 頁面的工具，它允許開發者將後端視圖中的數據與 HTML 結合，從而實現動態的網頁內容。每當用戶請求一個網頁時，Django 會渲染對應的模板並返回結果給用戶。

模板的作用包括：

- 動態內容渲染：模板可以將上下文數據（如用戶信息、文章內容）插入到HTML中，從而生成個性化的頁面。

頁面展示控制：模板允許使用條件語句和循環來控制頁面上的數據展示。

頁面佈局管理：通過模板繼承，開發者可以設置基本頁面框架，並在不同頁面中繼承和擴展這些框架。

#### 6.1.2 模板文件的結構

Django 的模板通常存儲在應用的 templates/ 目錄中，並以 .html 為擴展名。模板文件本質上是 HTML 文件，但可以包含特殊的 模板標籤 和 變量語法，用來動態渲染數據。

範例：簡單的 Django 模板

```
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8" />
{{ title }}</title>
```
<!-- 渲染上下文中的 title 變量 -->

```
</head>
{{ welcome_message }}</h1>
```
<!-- 渲染上下文中的歡迎消息 -->

```
</body>
</html>
```
在這個範例中，{{title}} 和 {{welcome_message}} 是變量標記，它們會被視圖中提供的上下文數據替換。

### 6.2 Django 模板語法

#### 6.2.1 模板變量

在 Django 模板中，變量使用 雙大括號 {{}} 來表示。變量的值來自視圖函數提供的上下文數據，當模板被渲染時，這些變量會被具體的數據替換。

範例：使用變量渲染數據

```
<!-- templates/index.html -->
```
歡迎來到 {{ site_name }} ! </h1>

我們有 {{ num_posts }} 篇博客文章。</p>

假設視圖函數提供瞭如下上下文：

```
context = {
```
'site_name': '我的網站',

```
'num_posts': 42
}
```
渲染後的 HTML 會是：

歡迎來到 我的網站！</h1>

我們有 42 篇博客文章。</p>

#### 6.2.2 模板標籤

模板標籤使用 {%%} 表示，通常用於控制流程（如條件語句、循環）或調用模板過濾器和模板標籤。常見的模板標籤有 for（循環）、if（條件判斷）和 block（模板繼承）。

## if 條件語句

if 標籤用來根據條件渲染不同的內容。它可以用來判斷變量是否存在或是否滿足某些條件。

範例：使用 if 進行條件渲染

```
<!-- templates/user_profile.html -->
{% if user.is_authenticated %}
```
歡迎回來，{{ user.username }} ! </p>

```
{% else %}
```
需要登入才能看內容時，模板用 `{% url 'login' %}` 產生登入連結（`<a>` 連結文字寫「登入」）。

```
{% endif %}
```
for 循環

for 標籤用於遍歷列表或查詢集，從而渲染多個數據項。

範例：使用 for 循環渲染文章列表

```
<!-- templates/blog_list.html -->
{ % for post in posts % }
{{ post.title }} - {{ post.author }}</li>
{% endfor %}
</ul>
```
假設上下文中的 posts 是一個包含多篇文章的列表，該模板會渲染每篇文章的標題和作者。

### 6.3 上下文數據的渲染

#### 6.3.1 傳遞上下文到模板

在視圖函數中，我們使用 Django 提供的 render() 函數來將模板與上下文數據結合，然後將結果返回給用戶。上下文是一個包含數據的字典，模板中的變量可以使用這些數據來生成動態內容。

範例：在視圖中傳遞上下文

```
# myapp/views.py
from django.shortcuts import render
def index(request):
context = {
```
'title': '我的首頁',

'welcome_message': '歡迎來到我的網站！',

'site_name': '我的網站',

```
'num_posts': 42
}
return render(request, 'index.html', context)
```
在這裡，我們將上下文數據傳遞給 index.html 模板，模板可以使用這些數據來渲染頁面。

#### 6.3.2 上下文處理器

上下文處理器（Context Processors）是一組函數，它們可以在每個模板中自動提供一些全局可用的上下文數據。Django 提供了一些內建的上下文處理器，例如用來提供當前用戶信息、請求對象和網站設置等。

範例：自定義上下文處理器

你可以創建自定義上下文處理器來提供全局變量，這些變量將在所有模板中可用。

```
# myapp/context_processors.py
def site_info(request):
return {
```
'site_name': '我的網站',

'site_description': '這是一個示例網站'

```
}
```
然後，在 settings.py 中將上下文處理器添加到 TEMPLATES 設置中：

```
# settings.py
TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [],
'APP_DIRS': True,
'OPTIONS': {
'context_processors': [
'django.template.context_processors.request',
```
'myapp.context_processors.site_info', # 添加自定義上下文處理器

```
],
},
]
```
現在，site_name 和 site_description 變量將在所有模板中可用。

### 6.4 模板繼承

#### 6.4.1 模板繼承的概念

模板繼承允許你在一個基礎模板中定義網頁的通用結構，然後在具體頁面中繼承這個基礎模板並填充具體的內容。這種方法可以幫助你在應用中保持一致的頁面佈局，同時避免重複代碼。

#### 6.4.2 定義基礎模板

基礎模板定義了網頁的通用結構和樣式，並使用 \*\*{% block %

}\*\* 標籤來設置可以被子模板覆蓋的區域。

範例：定義一個基礎模板

```
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8" />
```
{% block title %}我的網站{% endblock %}</td>

```
</head>
```
我的網站標題</h1>

```
</header>
```
<a href="/">首頁</a></li>

<a href="/about/">關於我們</a></li>

```
</ul>
</nav>
{% block content %} {% endblock %} </main>
```
&copy; 2024 我的網站</p>

```
</footer>
</body>
</html>
```
在這裡，{% block title %} 和 {% block content %} 是兩個區域，子模板可以覆蓋這些區域來顯示具體的內容。

#### 6.4.3 繼承基礎模板

子模板可以使用 {% extends %} 標籤來繼承基礎模板，並使用 {% block %} 標籤來覆蓋父模板中的區域。

範例：繼承基礎模板的子模板

```
<!-- templates/index.html -->
```
{% extends 'base.html' %} {% block title %}首頁 - 我的網站{% endblock %} {% block content %}

歡迎來到我的網站！</h2>

這是首頁的具體內容。</p>

```
{% endblock %}
```
在這裡，index.html 繼承了 base.html，並覆蓋了 title 和 content 區域的內容。

### 6.5 模板過濾器和自定義模板標籤

#### 6.5.1 模板過濾器

模板過濾器 是用來修改變量輸出的工具。過濾器可以對變量進行格式化、轉換或其他處理。過濾器使用管道符號 | 來應用。

範例：使用模板過濾器當前日期：{{ current_dateldate:"Y-m-d" }}</p>

文章數量：{{ num_postsldefault:"暫無文章" }}</p>

- date 過濾器用於格式化日期。

- default 過濾器提供一個默認值，當變量為空時使用該值。

#### 6.5.2 自定義模板過濾器

你可以創建自定義的模板過濾器來執行特定的格式化或處理邏輯。

範例：創建自定義過濾器

```
# myapp/templatetags/my_filters.py
from django import template
register = template.Library()
@register.filter(name='add_exclamation')
def add_exclamation(value):
return f"{value}!"
```
然後在模板中使用自定義過濾器：

```
<!-- templates/index.html -->
{{ welcome_messageladd_exclamation }}</p>
```
#### 6.5.3 自定義模板標籤

自定義模板標籤允許你創建複雜的邏輯來在模板中使用。這些標籤可以實現比過濾器更強大的功能。

範例：創建自定義模板標籤

```
# myapp/template tags/my_tags.py
from django import template
register = template.Library()
@register.simple_tag
def multiply(a, b):
return a * b
```
然後在模板中使用自定義標籤：

```
<!-- templates/calculate.html -->
{% load my_tags %}
```
結果：{% multiply 5 3 %} </p>

### 6.6 總結

在本章中，我們詳細介紹了 Django 的 模板系統，包括 模板語法、上下文數據的渲染、模板繼承，以及如何使用 模板過濾器和 自定義模板標籤 來生成動態網頁。通過學習這些概念和技術，你可以構建靈活且可重用的前端頁面。

7: Django 的模型系統與 CRUD 操作

在 Django 中，模型（Models）是數據庫與應用之間的橋樑，它們負責定義數據的結構並與數據庫進行交互。Django 提供了強大的 ORM（Object-Relational Mapping），使開發者可以通過 Python 代碼來執行對數據庫的操作，而不需要直接編寫 SQL 查詢。CRUD 操作是 Web 應用中常見的操作模式，它包括創建（Create）、讀取（Read）、更新（Update）和刪除（Delete）數據。

本章將詳細介紹 Django 的模型系統與 CRUD 操作，並講解如何使用 Django 提供的查詢集 API 來查詢和操作數據。

