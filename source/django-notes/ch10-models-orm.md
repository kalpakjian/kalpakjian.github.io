# 第 10 章 · 模型、ORM 與查詢集

## 1. 模型系統

### 1.1 模型的概念

模型（Model）是對應資料庫表的 Python 類：每個類＝一張表、每個欄位＝一欄。寫 Python 即可操作資料庫，不需寫 SQL。

- **定義資料結構**：描述欄位與屬性。
- **操作資料**：新增、查詢、更新、刪除。
- **資料驗證**：定義欄位型別與驗證規則。

### 1.2 建立模型

模型是 `django.db.models.Model` 的子類：

```
# myapp/models.py
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)              # 標題
    content = models.TextField()                          # 內容
    author = models.CharField(max_length=100)             # 作者
    published_at = models.DateTimeField()                 # 發布時間
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(auto_now=True)      # 更新時間

    def __str__(self):
        return self.title
```

`__str__()` 決定模型在後台等的字串表示。

## 2. ORM（Object-Relational Mapping）

### 2.1 作用

ORM 把 Python 物件映射到資料庫表，可用物件方式操作資料庫，且不綁定特定資料庫。

- **物件 ↔ 資料列**、**欄位 ↔ 欄位**。

- **查詢集 API**：查詢、過濾、排序、更新、刪除。

### 2.2 建立／更新資料表（遷移）

```
# 1. 生成遷移檔
python manage.py makemigrations
# 2. 套用到資料庫
python manage.py migrate
```

## 3. 查詢集（QuerySet）API

<figure class="fig-svg"><svg viewBox="0 0 860 200" width="100%" role="img" aria-label="ORM 查詢鏈：QuerySet 鏈式呼叫、延遲求值、生成 SQL 到資料庫取回物件" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="95" width="190" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="115" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">QuerySet 鏈式呼叫</text><text x="115" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">filter()／order_by()／切片</text><rect x="240" y="95" width="170" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="325" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">延遲求值</text><text x="325" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">真正用到才查詢</text><rect x="440" y="95" width="120" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="500" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">SQL</text><text x="500" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">SELECT …</text><rect x="590" y="95" width="120" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="650" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">資料庫</text><text x="650" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">SQLite／PG</text><rect x="740" y="95" width="100" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="790" y="120" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">物件</text><text x="790" y="140" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">Model 實例</text><line x1="210" y1="126" x2="236" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="410" y1="126" x2="436" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="560" y1="126" x2="586" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="710" y1="126" x2="736" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="245" y="86" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">不快取、可再串接</text></svg><figcaption>圖　ORM 查詢鏈：鏈式呼叫只是組裝條件，QuerySet 延遲求值，真正迭代時才產生 SQL 並回傳 Model 實例。</figcaption></figure>

### 3.1 基本概念

QuerySet 是查詢與操作資料庫的介面，具**鏈式呼叫**與**延遲求值**（真正用到時才查詢）特性；透過模型管理器 `objects` 操作。

### 3.2 查詢資料

- `all()`：全部記錄。
- `filter()`：依條件過濾。
- `get()`：取單筆（不唯一或不存在會報錯）。
- `exclude()`：排除符合條件者。

```
Article.objects.all()
Article.objects.filter(author='John Doe')
Article.objects.get(id=1)
Article.objects.exclude(author='John Doe')
```

### 3.3 排序

用 `order_by()`；欄位前加 `-` 表示降序：

```
Article.objects.order_by('-published_at')
```

### 3.4 切片

支援 Python 切片，限制回傳數量：

```
latest = Article.objects.order_by('-published_at')[:5]
```

### 3.5 連表與聚合

- `select_related()`：外鍵連表查詢，減少查詢次數。
- `aggregate()` / `annotate()`：聚合（計數、平均、總和）。

```
Article.objects.select_related('author').all()

from django.db.models import Count
Article.objects.aggregate(Count('id'))
```

## 4. CRUD 操作

### 4.1 新增（Create）

```
# 方式一：create()
Article.objects.create(title='新的文章', content='...', author='Jane Doe')

# 方式二：實例 + save()
a = Article(title='另一篇', content='...', author='John Doe')
a.save()
```

### 4.2 讀取（Read）

用 `all()`、`filter()`、`get()` 等（見第 3 節）。

### 4.3 更新（Update）

```
a = Article.objects.get(id=1)
a.title = '更新後標題'
a.save()

# 批量更新
Article.objects.filter(author='John Doe').update(author='Jane Doe')
```

### 4.4 刪除（Delete）

```
Article.objects.get(id=1).delete()
Article.objects.all().delete()
```

## 5. 本章小結

模型是真實世界物件在資料庫的映射；ORM 讓你以 Python 操作資料庫；查詢集 API 提供 CRUD 與高級功能（連表、聚合）。
## 6. 模型關聯關係

<figure class="fig-svg"><svg viewBox="0 0 720 240" width="100%" role="img" aria-label="Django 三種模型關聯：一對多、多對多、一對一" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="70" width="120" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="80" y="98" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">Author</text><rect x="190" y="70" width="140" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="260" y="92" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">Article</text><text x="260" y="112" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">ForeignKey</text><text x="165" y="60" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">1 : N</text><line x1="140" y1="98" x2="186" y2="98" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="370" y="70" width="120" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="430" y="98" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">Tag</text><rect x="540" y="70" width="140" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="610" y="92" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">Article</text><text x="610" y="112" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">ManyToMany</text><text x="510" y="60" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">N : N</text><line x1="490" y1="98" x2="536" y2="98" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="20" y="160" width="120" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="80" y="188" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">User</text><rect x="190" y="160" width="140" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="260" y="182" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">Profile</text><text x="260" y="202" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">OneToOne</text><text x="165" y="150" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">1 : 1</text><line x1="140" y1="188" x2="186" y2="188" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/></svg><figcaption>圖 2　三種模型關聯：ForeignKey（一對多）、ManyToManyField（多對多）、OneToOneField（一對一）。</figcaption></figure>

Django 支援三種關聯，皆以欄位定義。

### 6.1 一對多（ForeignKey）

多篇文章屬於同一分類：

```
# myapp/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published_at = models.DateTimeField()
```

`on_delete=models.CASCADE`：分類被刪除時，底下的文章一併刪除。

### 6.2 多對多（ManyToManyField）

一篇文章有多個標籤、一個標籤屬於多篇文章；Django 自動建立中間表：

```
class Tag(models.Model):
    name = models.CharField(max_length=100)

class Article(models.Model):
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag)
```

### 6.3 一對一（OneToOneField）

如 User 與 Profile：

```
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
```

## 7. 關聯查詢

### 7.1 select_related()：外鍵連表

```
articles = Article.objects.select_related('category').all()
```

一次查詢就把關聯的分類撈出來，避免多次查詢。

### 7.2 prefetch_related()：多對多

```
articles = Article.objects.prefetch_related('tags').all()
```

先取主表，再以額外查詢批次載入多對多資料。

### 7.3 反向查詢

Django 自動產生反向屬性（`模型名_set`）：

```
category = Category.objects.get(id=1)
category.article_set.all()      # 該分類下所有文章

tag = Tag.objects.get(id=1)
tag.article_set.all()           # 帶有該標籤的所有文章
```

## 8. 高級查詢

### 8.1 聚合（Count / Sum / Avg）

```
from django.db.models import Count
Category.objects.annotate(num_articles=Count('article'))
```

### 8.2 F()：以欄位值運算

```
from django.db.models import F
Article.objects.update(clicks=F('clicks') + 1)   # 點擊數 +1
```

### 8.3 Q()：AND / OR 條件組合

```
from django.db.models import Q
Article.objects.filter(Q(title__icontains='Django') | Q(author='John'))
```

### 8.4 多級與合併查詢

```
# 同分類的其他文章
article = Article.objects.get(id=1)
Article.objects.filter(category=article.category).exclude(id=article.id)

# 合併兩個查詢集
q1 = Article.objects.filter(author='John')
q2 = Article.objects.filter(title__icontains='Python')
q1.union(q2)
```

## 9. 本章小結

本章說明三種模型關聯（FK / M2M / O2O）、關聯查詢優化（`select_related` / `prefetch_related` / 反向查詢）與高級查詢（聚合、`F()`、`Q()`、`union()`）。
## 10. Humanize 模塊

`humanize` 是 Django 的模板過濾器模組，把數字、日期、時間轉成更符合人類直覺的格式（如 `1000000` → `1,000,000`）。使用前先在模板 `{% load humanize %}`。

### 10.1 數字過濾器

- `intcomma`：加千分位逗號。`{{ 1000000|intcomma }}` → `1,000,000`
- `intword`：轉成詞語。`{{ 1200000|intword }}` → `1.2 million`
- `apnumber`：1～9 轉英文單詞（AP 格式）。

```
{% load humanize %}
{{ 1000000|intcomma }}
```

### 10.2 日期／時間過濾器

- `naturalday`：今天／昨天／日期。
- `naturaltime`：相對時間（如「10 分鐘前」）。

```
{% load humanize %}
{% if article.published_at|naturaltime %}
    {{ article.published_at|naturaltime }}
{% else %}
    {{ article.published_at|naturalday }}
{% endif %}
```

### 10.3 應用場景

- **電商**：價格、庫存加千分位（`intcomma`）。
- **部落格**：閱讀數（`intword`）、發布時間（`naturaltime`）。

```
{% load humanize %}
<p>商品價格：${{ product.price|intcomma }}</p>
<p>庫存數量：{{ product.stock|intcomma }} 件</p>
<p>閱讀次數：{{ article.views|intword }}</p>
<p>發布時間：{{ article.published_at|naturaltime }}</p>
```

### 10.4 自定義過濾器

放在 App 的 `templatetags/` 下：

```
# myapp/templatetags/custom_humanize.py
from django import template
register = template.Library()

@register.filter
def chinese_number(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return value
    if 10000 <= value < 100000000:
        return f'{value // 10000}萬'
    elif value >= 100000000:
        return f'{value // 100000000}億'
    return str(value)
```

```
{% load custom_humanize %}
觀看次數：{{ video.views|chinese_number }}
```

## 11. 本章小結

`humanize` 讓數字與日期更易讀；不足時可用自定義過濾器擴充。
## 12. 資料過濾系統

### 12.1 查詢集過濾

- `filter()`：符合條件；`exclude()`：排除條件。

```
Article.objects.filter(status='published')
Article.objects.exclude(status='draft')
```

**常用查找器（lookup）**

| 查找 | 說明 |
| --- | --- |
| `field=value` | 精確匹配 |
| `field__icontains='kw'` | 不分大小寫模糊匹配 |
| `field__range=(a, b)` | 範圍 |
| `field__gte` / `field__lte` | 大於等於／小於等於 |

```
Article.objects.filter(title__icontains='Django')
Article.objects.filter(published_at__year=2024)
Product.objects.filter(price__range=(100, 500))
```

### 12.2 表單過濾

用 `Form` 收集條件，再套用到查詢集。

```
# myapp/forms.py
from django import forms

class ArticleFilterForm(forms.Form):
    author = forms.CharField(required=False, label='作者')
    status = forms.ChoiceField(
        choices=[('draft', '草稿'), ('published', '已發布')], required=False)
    start_date = forms.DateField(required=False, label='開始日期')
    end_date = forms.DateField(required=False, label='結束日期')
```

```
# myapp/views.py
from .forms import ArticleFilterForm
from .models import Article

def article_list(request):
    form = ArticleFilterForm(request.GET or None)
    articles = Article.objects.all()
    if form.is_valid():
        if form.cleaned_data.get('author'):
            articles = articles.filter(author__icontains=form.cleaned_data['author'])
        if form.cleaned_data.get('status'):
            articles = articles.filter(status=form.cleaned_data['status'])
    return render(request, 'article_list.html', {'form': form, 'articles': articles})
```

### 12.3 基於 URL 的過濾

條件透過 URL 參數傳遞（方便分享）：

```
# myapp/views.py
def product_list(request):
    products = Product.objects.all()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    return render(request, 'product_list.html', {'products': products})
```

```
/products/?min_price=100&max_price=500
```

### 12.4 進階過濾

- **Q 物件**：多條件 AND / OR。

```
from django.db.models import Q
Article.objects.filter(Q(title__icontains='Django') | Q(content__icontains='Framework'))
```

- **關聯過濾**：透過關聯欄位過濾，搭配 `distinct()` 去重。

```
Article.objects.filter(tags__name='技術').distinct()
```

### 12.5 最佳實踐

- 提供**預設過濾條件**（如預設價格區間），減少使用者操作。

```
def product_list(request):
    products = Product.objects.all()
    min_price = request.GET.get('min_price', 50)
    max_price = request.GET.get('max_price', 500)
    products = products.filter(price__gte=min_price, price__lte=max_price)
    return render(request, 'product_list.html', {'products': products})
```

- 大量資料時用 **JavaScript / AJAX 非同步載入**，避免整頁刷新。

## 13. 本章小結

本章介紹 Django 的資料過濾：查詢集 API（`filter` / `exclude` / 查找器）、表單與 URL 過濾，以及 Q 物件與關聯過濾等進階技巧。
