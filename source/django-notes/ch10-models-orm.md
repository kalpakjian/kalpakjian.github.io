# 第 10 章 · 模型、ORM 與查詢集

## 7.1 Django 的模型系統

### 7.1.1 模型的概念

在 Django 中，模型是對應於數據庫表的 Python 類。每個模型類對應數據庫中的一個表，每個模型的字段對應表中的列。通過模型，開發者可以使用 Python 代碼來進行數據庫操作，而無需直接編寫 SQL 語句。

模型的主要功能包括：

- 定義數據結構：描述數據的字段及其屬性。

- 操作數據：創建、查詢、更新和刪除數據。

- 數據驗證：定義字段的數據類型和驗證規則。

### 7.1.2 創建模型

模型是 Django 應用的基礎，我們可以通過定義模型類來描述數據表的結構。每個模型都是 django.db.models.Model 的子類，並包含若干字段，每個字段對應數據表中的一列。

範例：定義一個簡單的文章模型

```
# myapp/models.py
from django.db import models
class Article(models.Model):
title = models.CharField(max_length=200) # 標題
content = models.TextField() # 內容
author = models.CharField(max_length=100) # 作者
published_at = models.DateTimeField() # 發布時間
created_at = models.DateTimeField(auto_now_add=True) # 創建時間
updated_at = models.DateTimeField(auto_now=True) # 更新時間
def __str__(self):
return self.title
```
在這裡，我們定義了一個 Article 模型，包含文章的標題、內容、作者、發布時間等字段。__str__() 方法用於定義模型的字符串表示，方便在 Django 的管理後臺中顯示。

7.2 Django 的 ORM (Object-Relational Mapping)

### 7.2.1 ORM 的作用

ORM（Object-Relational Mapping）是 Django 用來將 Python 對象映射到數據庫表的工具。ORM 允許開發者以對象的方式來操作數據庫，而無需編寫 SQL 查詢語句。這使得數據庫操作更加簡單和直觀，且數據庫的具體實現對開發者透明。

ORM 的主要功能包括：

- 數據庫表與模型對象的映射：每個模型對象代表數據庫中的一行數據。

- 字段與數據類型的映射：每個模型字段對應數據表中的一列。

- 查詢集 API：提供查詢、過濾、排序、更新和刪除數據的 API。

### 7.2.2 創建數據庫表

當我們定義好模型後，Django 提供了遷移工具來創建或更新數據庫中的表結構。遷移工具會根據模型定義生成對應的 SQL 語句，並執行這些語句來更新數據庫。

創建或更新數據庫表的步驟如下：

1. 生成遷移文件：根據模型定義生成 SQL 語句。

2. 應用遷移：執行遷移，將模型變更應用到數據庫。

範例：創建數據庫表

```
# 1. 生成遷移文件
python manage.py makemigrations
# 2. 應用遷移
python manage.py migrate
```
makemigrations 命令會根據模型變化生成遷移文件，而 migrate 命令會將這些變更應用到數據庫，從而創建或更新數據庫表。

## 7.3 使用 Django 的查詢集 API

### 7.3.1 查詢集的基本概念

查詢集（QuerySet）是 Django 提供的用來查詢和操作數據庫的一個接口。查詢集是一個懶加載的數據集，只有在需要時（如進行迭代、打印或評估結果時）才會執行真正的數據庫查詢。

查詢集 API 是 Django ORM 的核心，它允許我們以簡潔的方式查詢數據庫中的記錄、過濾數據、進行排序和更新。

### 7.3.2 查詢數據

在 Django 中，通過模型的管理器（默認為 objects）可以查詢數據庫中的記錄。以下是一些常見的查詢方法：

all()：查詢所有數據

all() 方法會返回模型中所有記錄的查詢集。

範例：查詢所有文章

```
articles = Article.objects.all()
```
filter()：過濾數據

filter() 方法允許我們根據條件過濾查詢集中的數據。

範例：查詢特定作者的文章

```
articles_by_john = Article.objects.filter(author='John Doe')
```
get()：獲取單個記錄

get() 方法用於查詢單個記錄。如果查詢結果不唯一（多於一個或不存在），則會引發錯誤。

範例：查詢 ID 為 1 的文章

```
article = Article.objects.get(id=1)
```
exclude()：排除特定數據

exclude() 方法用來排除符合特定條件的數據。

範例：排除某位作者的文章

```
articles_not_by_john = Article.objects.exclude(author='John Doe')
```
### 7.3.3 排序數據

Django 提供了 order_by() 方法來對查詢集中的數據進行排序。我們可以根據單個或多個字段來排序，並指定升序或降序。

範例：按發布時間降序排列文章

```
articles = Article.objects.order_by('-published_at')
```
在這裡，負號 - 表示按降序排序。

### 7.3.4 切片與限制數據

查詢集支持 Python 的切片語法，允許我們從結果集中提取部分數據。例如，我們可以限制查詢返回的結果數量，或者提取前幾條記錄。

範例：提取最新的五篇文章

```
latest_articles = Article.objects.order_by('published_at')[5]
```
7.4 CRUD 操作：創建、讀取、更新和刪除數據

### 7.4.1 創建數據

創建新的數據記錄有兩種方式：一種是通過模型對象的 create() 方法，另一種是通過創建模型實例，然後手動調用 save() 方法來保存數據。

範例 1：使用 create() 方法創建數據

```
article = Article.objects.create(
title='新的文章',
content='這是文章的內容',
author='Jane Doe',
published_at=2024-01-01 12:00:00'
)
```
範例 2：使用 save() 方法創建數

據

```
article = Article(
title='另一篇文章',
content='文章內容',
author='John Doe',
published_at=2024-01-01 12:00:00'
)
article.save()
```
### 7.4.2 讀取數據

使用查詢集 API 可以輕鬆地讀取和過濾數據。已經在上一節中展示了幾個常見的查詢方法，包括 all()、filter() 和 get()。

### 7.4.3 更新數據

要更新現有記錄，我們可以先查詢該記錄，然後修改其屬性並調用 save() 方法來保存更改。

範例：更新文章標題

```
article = Article.objects.get(id=1)
article.title = '更新後的文章標題'
article.save()
```
此外，Django 也提供了批量更新的功能，可以使用 update() 方法對查詢集中的多個記錄進行更新。

範例：批量更新文章作者

```
Article.objects.filter(author='John Doe').update(author='Jane Doe')
```
### 7.4.4 刪除數據

要刪除數據，可以使用 delete() 方法。這個方法可以應用於單個對象或查詢集。

範例：刪除單個文章

```
article = Article.objects.get(id=1)
article.delete()
```
範例：刪除所有文章

```
Article.objects.all().delete()
```
## 7.5 查詢集的高級應用

### 7.5.1 連表查詢與 select_related()

在多個模型之間存在外鍵關係時，我們可以使用 select_related() 方法來進行連表查詢，這可以減少數據庫查詢次數，提升性能。

範例：連表查詢

```
articles = Article.objects.select_related('author').all()
```
這將一次性查詢文章及其關聯的作者，避免每次訪問作者字段時進行額外的查詢。

### 7.5.2 聚合查詢

Django 提供了 aggregate() 和 annotate() 方法來執行數據的聚合查詢（如計數、平均值、總和等）。

範例：計算文章總數

```
from django.db.models import Count
article_count = Article.objects.aggregate(Count('id'))
```
## 7.6 總結

在本章中，我們詳細介紹了 Django 的 模型系統 和 ORM（Object-Relational Mapping）的基礎知識，並學習瞭如何使用查詢集 API 來進行數據的 創建、讀取、更新和刪除（CRUD） 操作。我們還探討了查詢集的高級功能，如連表查詢和聚合查詢，這些功能使得 Django 能夠高效地與數據庫交互。

8: Django 的數據庫查詢與關聯關係

在 Django 中，數據庫關聯是指模型之間的相互關係，如一對一、一對多和多對多關係。Django 提供了強大的工具來處理這些關係，並通過查詢集 API 進行關聯查詢。理解並能夠有效地處理這些關係，對於構建複雜的 Web 應用至關重要。

本章將深入探討 Django 模型中的關聯關係，並介紹如何通過 Django 的查詢集 API 進行高效的數據查詢和關聯操作。

## 8.1 模型中的關聯關係

### 8.1.1 一對多關係（ForeignKey）

在 Django 中，一對多關係 是最常見的關聯類型，通過 ForeignKey 字段來實現。例如，一篇文章可能屬於一個特定的分類（Category），但一個分類可以有多篇文章，這就是典型的一對多關係。

範例：文章與分類的關係

```
# myapp/models.py
from django.db import models
class Category(models.Model):
name = models.CharField(max_length=100)
def __str__(self):
return self.name
class Article(models.Model):
title = models.CharField(max_length=200)
content = models.TextField()
category = models.ForeignKey(Category, on_delete=models.CASCADE) # 一篇文章對應一個分類
published_at = models.DateTimeField()
def __str__(self):
return self.title
```
在這個例子中，我們通過 ForeignKey 字段將文章（Article）與分類（Category）關聯起來。on_delete=models.CASCADE 表示當某個分類被刪除時，該分類下的所有文章也會被自動刪除。

### 8.1.2 多對多關係（ManyToManyField）

多對多關係 表示兩個模型可以相互擁有多個關聯。例如，一篇文章可以有多個標籤（Tag），同時每個標籤也可以關聯到多篇文章。Django 使用 ManyToManyField 來處理多對多關係。

範例：文章與標籤的多對多關係

```
# myapp/models.py
class Tag(models.Model):
name = models.CharField(max_length=100)
def __str__(self):
return self.name
class Article(models.Model):
title = models.CharField(max_length=200)
content = models.TextField()
tags = models.CharField(Tag) # 一篇文章可以有多個標籤
def __str__(self):
return self.title
```
在這裡，一篇文章可以擁有多個標籤，而一個標籤也可以屬於多篇文章。Django 自動處理多對多關係背後的數據庫表，不需要手動創建中間表。

### 8.1.3 一對一關係 (OneToOneField)

一對一關係 表示兩個模型之間有唯一的對應關係。例如，用戶和用戶資料（Profile）通常是一對一的關係。Django 提供了 OneToOneField 來處理這類關係。

範例：用戶與用戶資料的關係

```
# myapp/models.py
from django.contrib.auth.models import User
class Profile(models.Model):
user = models.OneToOneField(User, on_delete=models.CASCADE) # 每個用戶對應一個資料
bio = models.TextField()
def __str__(self):
return self.user.username
```
在這個例子中，我們使用 OneToOneField 將 Profile 模型與 User 模型關聯起來，這表示每個用戶只能有一個對應的資料。

## 8.2 Django 的查詢集 API 與關聯查詢

8.2.1 使用 select_related() 進行一對多關聯查詢

在處理一對多關係時，Django 提供了 select_related() 方法，這是一個性能優化工具，允許我們通過 連表查詢 一次性獲取相關數據，減少數據庫查詢次數。

範例：查詢文章及其對應的分類

```
articles = Article.objects.select_related('category').all()
```
這裡的 select_related('category') 會在查詢文章的同時，也將對應的分類數據一起查詢出來，從而避免多次查詢。

8.2.2 使用 prefetch_related() 進行多對多關聯查詢

在多對多關係中，Django 提供了 prefetch_related() 方法來優化查詢。這個方法會先獲取主表數據，然後再通過一次額外的查詢來加載關聯的多對多數據，從而減少數據庫查詢的負擔。

範例：查詢文章及其標籤

```
articles = Article.objects.prefetch_related('tags').all()
```
在這裡，prefetch_related('tags')會加載所有文章的標籤，並將結果進行優化。

### 8.2.3 反向查詢

Django 自動為關聯關係創建了反向查詢屬性，這使得我們可以通過關聯對象進行反向查詢。例如，我們可以通過分類來查詢所有屬於該分類的文章，或者通過標籤來查詢所有帶有該標籤的文章。

通過分類查詢文章

```
category = Category.objects.get(id=1)
articles_in_category = category.article_set.all() # 查詢該分類下的所有文章
```
article_set 是 Django 自動生成的反向查詢屬性，表示該分類下的所有文章。

通過標籤查詢文章

```
tag = Tag.objects.get(id=1)
articles_with_tag = tag.article_set.all() # 查詢所有帶有該標籤的文章
```
同樣，article_set 在這裡表示與該標籤關聯的所有文章。

## 8.3 查詢集 API 的高級應用

### 8.3.1 聚合查詢

Django 提供了強大的聚合查詢功能，允許我們進行統計操作，如 計數、總和、平均值 等。常用的聚合函數包括 Count()、Sum()、Avg() 等。

範例：計算每個分類下的文章數量

```
from django.db.models import Count
category_counts = Category.objects.annotate(num_articles=Count('article'))
```
這裡的 annotate() 方法會為每個分類添加一個 num_articles 屬性，表示該分類下的文章數量。

### 8.3.2 F() 查詢與更新

Django 的 F() 表達式允許我們在查詢中直接使用數據庫中的字段值進行操作，這對於進行數據更新時非常有用。

範例：將所有文章的點擊次數加 1

```
from django.db.models import F
Article.objects.update(clicks=F('clicks') + 1)
```
這裡，F('clicks') + 1 表示將每篇文章的點擊次數自增 1，並將結果保存到數據庫中。

### 8.3.3 Q() 查詢

在處理複雜查詢時，我們可以使用 Q() 對象來實現 AND 和 OR 條件的組合查詢。這允許我們在一個查詢中實現多個條件的靈活組合。

範例：查詢標題中包含 "Django" 或作者為 "John" 的文章

```
from django.db.models import Q
articles = Article.objects.filter(Q(title_icontains='Django') | Q(author='John'))
```
這個查詢會返回所有標題中包含 "Django" 或作者為 "John" 的文章。

## 8.4 模型間的複雜關聯查詢

### 8.4.1 通過多級關聯進行查詢

Django 的查詢集 API 允許我們通過多級關聯進行數據查詢。例如，我們可以通過文章查詢到與該文章相關的分類，再通過分類查詢該分類下的其他文章。

範例：查詢某篇文章的同類文章（屬於相同分類的文章）

```
article = Article.objects.get(id=1)
related_articles = Article.objects.filter(category=article.category).exclude(id=article.id)
```
這裡，我們首先查詢了某篇文章的分類，然後查詢該分類下的其他文章，並排除當前文章。

### 8.4.2 連表查詢與合併結果

當需要查詢來自多個表的數據時，我們可以使用 Django 的查詢集 API 進行連表查詢，並通過 union()、intersection() 和 difference() 等方法合併查詢結果。

範例：合併兩個查詢集的結果

```
queryset1 = Article.objects.filter(author='John')
queryset2 = Article.objects.filter(title__icontains='Python')
combined_queryset = queryset1.union(queryset2)
```
這個範例中，我們將兩個不同的查詢結果合併成一個查詢集，返回的數據包含所有作者為 "John" 的文章以及標題中包含 "Python" 的文章。

## 8.5 總結

在本章中，我們詳細介紹了 Django 中的數據庫查詢與關聯關係，學習瞭如何使用 Django 的 ForeignKey、ManyToManyField 和 OneToOneField 來處理模型之間的關聯。我們還探討瞭如何通過查詢集 API 進行高效的關聯查詢，包括使用 select_related() 和 prefetch_related() 進行優化查詢。最後，我們介紹了 Q() 和 F() 等高級查詢技術，以便處理複雜的數據查詢場景。

掌握這些技巧後，你將能夠構建高效且靈活的數據查詢邏輯，從而更好地處理 Django 應用中的數據關聯問題。

9: Django 的 Humanize 模塊

在 Web 應用中，數據通常需要以人類易於理解的方式呈現。例如，我們不希望用戶看到數字 1000000，而是更希望它顯示為 1,000,000。Django 的 humanize 模塊 正是為瞭解決這些需求，它提供了一些過濾器來將數字、日期和時間等數據轉換成更符合人類閱讀習慣的格式。

本章將介紹 Django 的 humanize 模塊，學習如何使用其提供的過濾器來格式化數據，並探討一些實際應用場景。

## 9.1 Humanize 模塊的基本介紹

Django 的 humanize 模塊是一個模板過濾器模塊，專門用來將數字、日期、時間等數據轉換為更符合人類直觀理解的格式。這些過濾器可以應用於 Django 的模板中，幫助提升用戶體驗，特別是當應用中顯示大量數據時，數據的可讀性至關重要。

### 9.1.1 啟用 Humanize 模塊

要在模板中使用 humanize 模塊，需要首先在模板中加載它。你可以在模板的開頭使用 {% load humanize %} 來加載這個模塊。

範例：加載 humanize 模塊

```
{ % load humanize % }
```
## 9.2 數字格式化過濾器

humanize 提供了多種過濾器來格式化數字，使其更易於閱讀或更符合常見的數據表示方式。

9.2.1 intcomma：數字加逗號

intcomma 過濾器會將數字進行逗號分隔，使得長數字更易於閱讀。這在顯示貨幣或大型數字時非常有用。

範例：使用 intcomma 添加逗號

```
{% load humanize %}
{ 1000000intcomma }</p>
```
<!-- 輸出：1,000,000 -->

這裡的 1000000 會被格式化為 1,000,000。

9.2.2 intword：將數字轉換為詞語

intword 過濾器可以將大數字轉換為更簡單的詞語表示。這在需要以簡潔的方式顯示數據時非常有用，例如在顯示用戶數或點擊次數時。

範例：使用 intword 將數字轉換為詞語

```
{% load humanize %}
{ 1200000lintword }</p>
```
<!-- 輸出：1.2 million -->

這裡，1200000 會被轉換為 1.2 million。

9.2.3 apnumber：轉換為一到九的單詞形式

apnumber 過濾器將數字 1 到 9 轉換為對應的英文單詞。這在需要遵循 AP 標準格式的文章或內容中很常用。

範例：使用 apnumber 將數字轉換為單詞

```
{% load humanize %}
{{7lapnumber }}</p>
```
<!-- 輸出：seven -->

這裡，7 會被轉換為 seven。

## 9.3 日期和時間的格式化過濾器

除了數字格式化外，humanize 模塊還提供了多種日期和時間的格式化過濾器，讓時間顯示更符合日常語言習慣。

9.3.1 naturaltime：相對時間顯示

naturaltime 過濾器可以將時間轉換為相對於當前時間的自然表達方式，例如 “10 minutes ago” （10 分鐘前）、“3 days ago” （3 天前）。

範例：使用 naturaltime 顯示相對時間

```
{% load humanize %}
{ { article.published_atlnaturaltime }</p>
```
如果 published_at 是 10 分鐘前的時間，這段模板會輸出 “10 minutes ago”。

9.3.2 naturalday：自然語言顯示日期

naturalday 過濾器用來將日期顯示為自然語言形式。如果日期是今天，會顯示“today”，如果是昨天，則顯示“yesterday”，否則顯示具體的日期。

範例：使用 naturalday 顯示日期

```
{ % load humanize % }
{ { article.published_atlnaturalday } }</p>
```
這裡，如果 published_at 是昨天的日期，模板將輸出 “yesterday”。

9.3.3 naturaltime 與 naturalday 的組合

我們還可以將 naturaltime 和 naturalday 過濾器結合使用，讓時間顯示更加靈活。當時間距離現在較短時，顯示“幾分鐘前”，如果時間較遠，則顯示具體的日期。

範例：組合使用時間過濾器

```
{% load humanize %} {% if article.published_atlnaturaltime %}
{ { article.published_atlnaturaltime } }</p>
{% else %}
{ { article.published_atlnaturalday } }</p>
{% endif %}
```
這樣可以靈活顯示最近的時間和過去的日期。

## 9.4 應用場景與實踐

Django 的 humanize 模塊可以應用於多種場景，特別是需要展示大量數字或日期的應用。在這裡，我們將探討一些常見的使用場景，並展示如何靈活應用 humanize 過濾器。

### 9.4.1 電商網站中的應用

在電商網站中，價格和商品數量的顯示通常需要進行格式化，以提高用戶體驗。使用humanize的intcomma可以輕鬆實現貨幣的格式化顯示。

範例：格式化價格與商品數量

```
{% load humanize %}
```
商品價格：${{ product.pricelintcomma }}</p>

庫存數量：{{ product.stocklintcomma }} 件</p>

這裡的價格和庫存數量會自動加上逗號，讓數據更加易讀。

### 9.4.2 博客或新聞網站中的應用

在博客或新聞網站中，閱讀數量和發布時間是用戶常關注的信息。使用 intword 和 naturaltime 可以讓這些數據更加直觀。

範例：格式化閱讀量與發布時間

```
{% load humanize %}
```
閱讀次數：{{ article.viewslintword }}</p>

發布時間：{{ article.published_atnaturaltime }}</p>

這樣，數字如 1200 會顯示為 1.2k，而發布時間會顯示為 “10 分鐘前”。

## 9.5 高級應用與自定義

雖然 Django 的 humanize 模塊已經提供了許多實用的過濾器，但你也可以根據需求創建自定義的過濾器來進一步擴展其功能。

### 9.5.1 創建自定義過濾器

假設我們需要一個新的過濾器，將數字格式化為中文單位（如萬、億）。我們可以通過 Django 的模板標籤系統來實現。

範例：自定義數字格式化過濾器

```
# myapp/template tags/custom_humanize.py
from django import template
register = template.Library()
@register.filter
def chinese_number(value):
try:
value = int
(value)
if value >= 10000 and value < 100000000:
```
return f{'value // 10000}萬'

```
elif value >= 100000000:
```
return f{'value // 100000000}億'

```
else:
return str(value)
except (ValueError, TypeError):
return value
```
這個自定義過濾器會將數字轉換為中文單位，如 15000 會顯示為 1 萬。

### 9.5.2 在模板中使用自定義過濾器

創建完自定義過濾器後，你可以像使用內建過濾器一樣在模板中使用它。

範例：使用自定義過濾器

```
{ % load custom_humanize % }
```
觀看次數：{{ video.viewslchinese_number }}</p>

這裡，15000會顯示為1萬，120000000會顯示為1億。

## 9.6 總結

在本章中，我們學習了 Django 的 humanize 模塊，以及如何使用它來將數字和日期轉換為更加人性化的格式。我們探討了幾個常用的過濾器，如 intcomma、intword 和 naturaltime，並展示了它們的應用場景。通過這些過濾器，開發者可以顯著提升應用中數據的可讀性和用戶體驗。

掌握 humanize 的使用技巧後，開發者可以輕鬆處理大量數據的顯示，並將複雜的數據轉換為用戶易於理解的形式。對於特殊需求，還可以通過自定義過濾器來進一步擴展其功能。

10: Django 的數據過濾系統

在現代 Web 應用中，數據的過濾和篩選是非常常見的需求。用戶通常需要在大量數據中找到符合條件的記錄，例如根據日期篩選文章、按價格篩選商品、或者根據特定屬性查找用戶。在 Django 中，我們可以使用其內建的查詢集 API 和其他過濾工具，實現靈活、高效的數據過濾功能。

本章將深入探討如何在 Django 中實現數據過濾，介紹查詢集的過濾方法、表單過濾的應用，以及一些常見的高級過濾技術，如基於 URL 的過濾和動態篩選功能。

## 10.1 查詢集 API 中的過濾方法

Django 的查詢集 API 是進行數據過濾的基礎工具。通過查詢集，我們可以根據特定條件篩選數據、進行精確查詢或模糊查詢、排序數據，以及根據多條件組合進行篩選。

10.1.1 基本的 filter() 與 exclude() 方法

filter() 是 Django 中最常用的查詢方法，用來篩選符合特定條件的數據。你可以根據模型字段設置過濾條件，並且查詢可以是精確匹配或模糊查詢。

範例：使用 filter() 進行數據過濾

```
# 查詢所有發布狀態為 "published" 的文章
published_articles = Article.objects.filter(status='published')
# 查詢特定作者的文章
john_articles = Article.objects.filter(author='John Doe')
```
exclude() 方法的作用則相反，它用來排除符合特定條件的記錄。

範例：使用 exclude() 排除數據

```
# 排除所有草稿狀態的文章
non_draft_articles = Article.objects.exclude(status='draft')
```
### 10.1.2 常見的查詢查找器

Django 提供了一組查找器，用來對不同類型的數據進行過濾查詢。常見的查找器包括：

- 精確匹配：field_name=value

- 模糊匹配：name__icontains='keyword'（不區分大小寫）

- 範圍查詢：field_name_range=(start, end)

- 大於/小於查詢：field_name_gte=value（大於或等於）和 field_name_lte=value（小於或等於）

範例：使用查找器進行數據過濾

```
# 查詢標題中包含 "Django" 的文章
django_articles = Article.objects.filter(title__icontains='Django')
# 查詢發布時間在 2024 年的文章
articles_in_2024 = Article.objects.filter(published_at__year=2024)
# 查詢價格範圍在 100 到 500 的商品
filtered_products = Product.objects.filter(price__range=(100, 500))
```
這些查找器可以靈活組合使用，實現複雜的查詢和過濾邏輯。

## 10.2 表單與數據過濾的結合

在許多 Web 應用中，數據過濾往往需要通過表單來實現。例如，用戶通過篩選表單選擇某個日期範圍、分類或關鍵字，來篩選出符合條件的數據。在 Django 中，表單和查詢集 API 可以結合使用，從而實現動態的數據過濾。

### 10.2.1 基本表單過濾的實現

我們可以使用 Django 的 Form 類來創建一個過濾表單，並通過查詢集過濾數據。

範例：使用表單進行簡單的數據過濾

```
# myapp/forms.py
from Django import forms
class ArticleFilterForm(forms.Form):
author = forms.CharField(required=False, label='作者')
status = forms.ChoiceField(choices=[('draft', '草稿'), ('published', '已發布')], required=False)
start_date = forms.DateField(required=False, label='開始日期')
end_date = forms.DateField(required=False, label='結束日期')
```
接下來，我們需要在視圖中處理表單數據並進行過濾：

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
if form.cleaned_data.get('start_date') and form.cleaned_data.get('end_date'):
articles = articles.filter(published_at__range=(form.cleaned_data['start_date'], form.cleaned_data['end_date']))
return render(request, 'article_list.html', {'form': form, 'articles': articles})
```
在模板中，我們可以渲染這個過濾表單，並顯示過濾後的結果：

```
<!-- templates/article_list.html -->
<form method="GET">
{{ form.as_p }}
```
<button type="submit">節選</button>

```
</form>
{% for article in articles %}
{{ article.title }} - {{ article.author }} - {{ article.published_at }}
</li>
{% empty %}
```
暫無符合條件的文章。</li>

```
{% endfor %}
</ul>
```
通過這樣的設計，用戶可以根據不同條件篩選文章數據。

## 10.3 基於 URL 的數據過濾

有時候，過濾條件可以通過 URL 參數直接傳遞，這樣可以讓過濾功能更加靈活並便於分享。例如，電商網站的篩選結果頁面可以通過 URL 傳遞價格範圍、品牌等條件。

### 10.3.1 使用 URL 參數進行過濾

我們可以通過 URL 傳遞過濾參數，並在視圖中根據這些參數進行數據過濾。

範例：根據 URL 參數進行過濾

```
# myapp/views.py
def product_list(request):
products = Product.objects.all()
# 根據 URL 中的價格範圍進行過濾
min_price = request.GET.get('min_price')
max_price = request.GET.get('max_price')
if min_price:
products = products.filter(price__gte=min_price)
if max_price:
products = products.filter(price__lte=max_price)
return render(request, 'product_list.html', {'products': products})
```
這樣，我們可以通過以下 URL 來篩選商品：

```
/products/?min_price=100&max_price=500
```
### 10.3.2 動態篩選條件的應用

有時，我們可能希望用戶能夠在頁面上動態改變篩選條件，比如點擊某個按鈕或選擇某個分類時即刻更新結果。這種情況下，我們可以使用 JavaScript 與 URL 結合來動態過濾數據。

範例：使用篩選按鈕動態改變 URL

```
<!-- templates/product_list.html -->
```
<a href="?min_price=100&max_price=200">價格範圍 100-200</a>

<a href="?min_price=200&max_price=300">價格範圍 200-300</a>

```
{% for product in products %}
<
li> {{ product.name }} - {{ product.price }}</li>
{% empty %}
```
暫無符合條件的商品。</li>

```
{% endfor %}
</ul>
```
這樣，用戶點擊不同的篩選按鈕時，URL會自動更新，並顯示篩選後的結果。

## 10.4 高級過濾技術

除了基本的數據過濾方法外，Django 還提供了一些高級的過濾技術，適用於更複雜的場景，如聯表查詢中的過濾、多條件組合過濾等。

### 10.4.1 使用 Q 對象進行複雜過濾

Q 對象允許我們進行複雜的查詢，特別是需要進行 多條件 OR 查詢 或 多條件 AND 查詢 的情況。Q 對象可以通過邏輯運算符 & 和 | 來組合多個查詢條件。

範例：使用 Q 進行多條件查詢

```
from django.db.models import Q
# 查詢標題中包含 'Django' 或內容中包含 'Framework' 的文章
filtered_articles = Article.objects.filter(
Q(_icontains='Django') | Q(content__icontains='Framework')
)
```
這裡，Q 對象允許我們同時查詢符合兩個條件的記錄，並用 OR 關係來進行數據過濾。

### 10.4.2 聯表查詢中的過濾

當模型之間存在外鍵關係或多對多關係時，我們可以使用 select_related 或 prefetch_related 來優化聯表查詢，並在查詢中加入過濾條件。

範例：查詢有特定標籤的文章

```
# 查詢所有標籤為 '技術' 的文章
articles_with_tag = Article.objects.filter(tags__name='技術').distinct()
```
這裡，我們使用聯表查詢來過濾出所有與特定標籤關聯的文章。

## 10.5 數據過濾最佳實踐

在實際應用中，為了提高數據過濾的效率和用戶體驗，我們可以遵循以下幾個最佳實踐：

### 10.5.1 提供預設過濾條件

在進行數據過濾時，可以為用戶提供預設的過濾條件，這樣用戶不必每次都手動輸入篩選條件。例如，電商網站可以提供熱門篩選條件如“價格區間”或“品牌”。

範例：使用預設過濾條件

```
def product_list(request):
products = Product.objects.all()
# 設置預設價格篩選條件
min_price = request.GET.get('min_price', 50)
max_price = request.GET.get('max_price', 500)
products = products.filter(price__gte=min_price, price__lte=max_price)
return render(request, 'product_list.html', {'products': products})
```
### 10.5.2 使用異步加載提升體驗

對於篩選大量數據的情況，可以使用 JavaScript 和 Ajax 來異步加載過濾結果，這樣用戶不必刷新整個頁面就可以看到更新後的數據。

## 10.6 總結

在本章中，我們深入探討了 Django 中的數據過濾系統，學習瞭如何通過查詢集 API 進行數據過濾，並展示瞭如何結合表單來實現靈活的篩選功能。我們還探討了基於 URL 的過濾方法，並介紹了一些高級過濾技術，如 Q 對象和聯表查詢中的過濾。

```
\pagebreak
```
11: Django 的分頁系統

在現代 Web 應用中，數據量往往非常龐大，當數據過多時，將所有數據一次性展示給用戶不僅會降低性能，還會對用戶體驗造成負面影響。此時，我們可以通過分頁（Pagination），將數據按頁顯示，每頁顯示一定數量的記錄。Django 提供了一個強大的內建分頁系統，讓開發者可以輕鬆實現數據的分頁顯示。

本章將介紹如何使用 Django 的分頁工具進行數據分頁，如何在模板中顯示分頁導航，並探討一些高級的分頁技術，如自定義分頁控制和查詢參數的處理。

