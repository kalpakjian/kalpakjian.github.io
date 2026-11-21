# 第 15 章（附加）· FBI 連環殺手：最簡 Django 範例

**導讀**：這是一個**最小可運作**的 Django 專案——只有 3 個模型、1 個視圖、1 個模板，完整走過 **Model → View → Template** 的流程，非常適合當作「第一個 Django 專案」的範本。

**專案原始碼（GitHub）**：https://github.com/kalpakjian/fbi-serial-killer

## 1. 專案簡介

- **主題**：FBI 探員捉拿連環殺手的記錄（純示範資料）。
- **功能**：一個頁面列出所有「捉拿記錄」，含探員、殺手、日期、地點、詳情。
- **技術**：Django 5.2 + SQLite + Bootstrap（CDN）。
- **重點**：3 個模型之間用 **ForeignKey** 關聯；視圖用 `select_related()` 一次取回關聯資料。

## 2. 專案結構

```
fbi_project/
    manage.py
    db.sqlite3
    requirements.txt
    fbi_project/              # 專案設定
        settings.py
        urls.py
        wsgi.py / asgi.py
    fbi_serial_killer/        # 應用（App）
        models.py             # 3 個模型
        views.py              # 1 個視圖
        urls.py
        admin.py
        seed_data.py          # 產生示範資料
        migrations/
        templates/fbi_serial_killer/capture_list.html
```

這是典型的 **Project（容器）+ App（功能模組）** 結構：設定放在 `fbi_project/`，功能放在 `fbi_serial_killer/`。
## 3. 模型（models.py）

三個模型：`FBI_Agent`（探員）、`Serial_Killer`（連環殺手）、`Capture`（捉拿記錄，用 FK 關聯前兩者）。

<figure class="fig-svg"><svg viewBox="0 0 760 232" width="100%" role="img" aria-label="FBI 範例的三個模型與外鍵關聯：FBI_Agent 與 Serial_Killer 透過 Capture 記錄關聯" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><g font-family="'Microsoft JhengHei','Segoe UI',sans-serif"><rect x="24" y="70" width="190" height="96" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="119" y="98" text-anchor="middle" font-size="14" fill="#e6edf3">FBI_Agent</text><text x="119" y="120" text-anchor="middle" font-size="11" fill="#39d0d8">name · badge_number</text><text x="119" y="138" text-anchor="middle" font-size="11" fill="#39d0d8">join_year · specialization</text><text x="119" y="158" text-anchor="middle" font-size="11" fill="#7ee787">探員</text><rect x="285" y="58" width="190" height="120" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.8"/><text x="380" y="86" text-anchor="middle" font-size="14" fill="#e6edf3">Capture</text><text x="380" y="108" text-anchor="middle" font-size="11" fill="#39d0d8">capture_date</text><text x="380" y="126" text-anchor="middle" font-size="11" fill="#39d0d8">location · details</text><text x="380" y="148" text-anchor="middle" font-size="11" fill="#f0a04b">agent (FK)</text><text x="380" y="166" text-anchor="middle" font-size="11" fill="#f0a04b">serial_killer (FK)</text><rect x="546" y="70" width="190" height="96" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="641" y="98" text-anchor="middle" font-size="14" fill="#e6edf3">Serial_Killer</text><text x="641" y="120" text-anchor="middle" font-size="11" fill="#39d0d8">name · alias</text><text x="641" y="138" text-anchor="middle" font-size="11" fill="#39d0d8">victim_count · …</text><text x="641" y="158" text-anchor="middle" font-size="11" fill="#7ee787">連環殺手</text><line x1="214" y1="118" x2="283" y2="118" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="248" y="108" text-anchor="middle" font-size="11" fill="#e6edf3">1 : N</text><line x1="546" y1="118" x2="477" y2="118" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="512" y="108" text-anchor="middle" font-size="11" fill="#e6edf3">N : 1</text></g><figcaption>圖：三個模型與外鍵關聯。</figcaption></svg></figure>

```
# fbi_serial_killer/models.py
from django.db import models

class FBI_Agent(models.Model):
    name = models.CharField(max_length=100, verbose_name="探員姓名")
    badge_number = models.CharField(max_length=10, unique=True, verbose_name="徽章編號")
    join_year = models.IntegerField(verbose_name="入職年份")
    specialization = models.CharField(max_length=100, verbose_name="專長領域", blank=True)

    class Meta:
        verbose_name = "FBI探員"
        verbose_name_plural = "FBI探員"

    def __str__(self):
        return f"{self.name} ({self.badge_number})"

class Serial_Killer(models.Model):
    name = models.CharField(max_length=100, verbose_name="姓名")
    alias = models.CharField(max_length=100, verbose_name="別名", blank=True)
    crime_period_start = models.IntegerField(verbose_name="犯罪開始年份")
    crime_period_end = models.IntegerField(verbose_name="犯罪結束年份")
    victim_count = models.IntegerField(verbose_name="受害人數量")
    description = models.TextField(verbose_name="犯罪描述", blank=True)

    class Meta:
        verbose_name = "連環殺手"
        verbose_name_plural = "連環殺手"

    def __str__(self):
        return f"{self.name} ({self.alias})" if self.alias else self.name

class Capture(models.Model):
    agent = models.ForeignKey(FBI_Agent, on_delete=models.CASCADE, verbose_name="負責探員")
    serial_killer = models.ForeignKey(Serial_Killer, on_delete=models.CASCADE, verbose_name="連環殺手")
    capture_date = models.DateField(verbose_name="捉拿日期")
    location = models.CharField(max_length=200, verbose_name="捉拿地點")
    details = models.TextField(verbose_name="捉拿詳情", blank=True)

    class Meta:
        verbose_name = "捉拿記錄"
        verbose_name_plural = "捉拿記錄"

    def __str__(self):
        return f"{self.serial_killer} 於 {self.capture_date} 在 {self.location} 被捕"
```

**重點**

- `verbose_name`：後台與表單顯示的中文名稱。
- `blank=True`：表單可留空；`unique=True`：徽章編號不可重複。
- `on_delete=models.CASCADE`：探員或殺手被刪除時，相關捉拿記錄一併刪除。
- `__str__()`：讓物件在後台以可讀字串呈現。
## 4. 視圖與路由

```
# fbi_serial_killer/views.py
from django.shortcuts import render
from .models import Capture

def capture_list(request):
    captures = Capture.objects.select_related('agent', 'serial_killer').all()
    return render(request, 'fbi_serial_killer/capture_list.html', {'captures': captures})
```

```
# fbi_serial_killer/urls.py
from django.urls import path
from . import views

app_name = 'fbi_serial_killer'

urlpatterns = [
    path('captures/', views.capture_list, name='capture_list'),
]
```

```
# fbi_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fbi_serial_killer.urls')),
]
```

**重點**：`select_related('agent','serial_killer')` 會用**一次連表查詢**把關聯物件一起撈回來，避免逐筆再查（N+1 問題）。

## 5. 模板（capture_list.html）

用 Bootstrap 表格 + `{% for %}`／`{% empty %}`：

```
<table class="table table-striped table-bordered">
    <thead class="table-dark">
        <tr>
            <th>探員</th><th>連環殺手</th><th>捉拿日期</th><th>地點</th><th>詳情</th>
        </tr>
    </thead>
    <tbody>
        {% for capture in captures %}
        <tr>
            <td>{{ capture.agent.name }}</td>
            <td>{{ capture.serial_killer.name }}</td>
            <td>{{ capture.capture_date }}</td>
            <td>{{ capture.location }}</td>
            <td>{{ capture.details }}</td>
        </tr>
        {% empty %}
        <tr><td colspan="5" class="text-center">無捉拿記錄</td></tr>
        {% endfor %}
    </tbody>
</table>
```

- `capture.agent.name`：透過 FK 直接取關聯物件的欄位（Django 模板自動處理）。
- `{% empty %}`：沒有資料時顯示的內容。

## 6. 產生示範資料（seed_data.py）

`seed_data.py` 會先清空資料表，再批次建立 21 位探員、連環殺手與捉拿記錄：

```
FBI_Agent.objects.bulk_create(fbi_agent_objects)   # 批次建立
Capture.objects.bulk_create(capture_objects)
```

**注意**：檔案內有一行寫死的路徑（`sys.path.append('/Users/...')`），換到你的環境要改成自己的專案路徑。

## 7. 執行步驟

```
# 1. 建立並啟用虛擬環境
python -m venv venv
venv\Scripts\activate           # Windows
source venv/bin/activate        # macOS / Linux

# 2. 安裝套件
pip install -r requirements.txt

# 3. 建立資料表
python manage.py migrate

# 4. 產生示範資料
python fbi_serial_killer/seed_data.py

# 5. 啟動伺服器
python manage.py runserver
```

打開 http://127.0.0.1:8000/captures/ 即可看到捉拿記錄表。

## 8. 重點整理

- 這是 **Model → View → Template** 的最小完整範例。
- 3 個模型用 **ForeignKey** 串起「探員－捉拿－殺手」。
- 視圖只需一行 `select_related()` 就兼顧正確性與效能。
- 模板用 `{% for %}` 走訪、`{% empty %}` 處理空資料。
