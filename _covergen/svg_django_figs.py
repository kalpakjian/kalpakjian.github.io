# -*- coding: utf-8 -*-
"""Django 筆記用的內嵌 SVG 圖（手繪、深色圖卡、文字精準；不用 AI 生圖畫文字）。"""

FONT = "'Microsoft JhengHei','Segoe UI',sans-serif"
CARD = "#0d1117"
BOX = "#132030"
STROKE = "#2c6fb1"
TEXT = "#e6edf3"
ACC = "#39d0d8"
WARM = "#f0a04b"


def _box(x, y, w, h, label, sub="", stroke=STROKE):
    t = ('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" stroke="%s" stroke-width="1.6"/>'
         % (x, y, w, h, BOX, stroke))
    t += ('<text x="%d" y="%d" text-anchor="middle" font-family="%s" font-size="15" fill="%s">%s</text>'
          % (x + w // 2, y + (h // 2 if not sub else h // 2 - 6), FONT, TEXT, label))
    if sub:
        t += ('<text x="%d" y="%d" text-anchor="middle" font-family="%s" font-size="11.5" fill="%s">%s</text>'
              % (x + w // 2, y + h // 2 + 14, FONT, ACC, sub))
    return t


def _arrow(x1, y1, x2, y2, curve=0):
    if curve:
        d = "M%d %d Q%d %d %d %d" % (x1, y1, (x1 + x2) // 2, y1 + curve, x2, y2)
        return '<path d="%s" fill="none" stroke="%s" stroke-width="1.8" marker-end="url(#a)"/>' % (d, ACC)
    return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.8" marker-end="url(#a)"/>'
            % (x1, y1, x2, y2, ACC))


DEFS = ('<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="%s"/></marker></defs>' % ACC)


def _wrap(body, w, h, aria, caption):
    return ('<figure class="fig-svg"><svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="%s" '
            'style="background:%s;border-radius:10px">%s%s</svg>'
            '<figcaption>%s</figcaption></figure>' % (w, h, aria, CARD, DEFS, body, caption))


def mvt():
    b = _box(20, 90, 130, 62, "瀏覽器", "發送請求")
    b += _box(190, 90, 130, 62, "urls.py", "URL 路由")
    b += _box(360, 20, 130, 62, "View 視圖", "業務邏輯")
    b += _box(360, 160, 130, 62, "Template", "模板渲染", stroke=WARM)
    b += _box(540, 20, 130, 62, "Model 模型", "ORM")
    b += _box(720, 20, 120, 62, "資料庫", "SQLite／PG")
    b += _arrow(150, 121, 186, 121)
    b += _arrow(320, 105, 356, 62)
    b += _arrow(490, 51, 536, 51)
    b += _arrow(670, 51, 716, 51)
    b += _arrow(720, 70, 490, 70)
    b += _arrow(425, 82, 425, 156)
    b += _arrow(360, 191, 154, 155)
    b += ('<text x="700" y="118" font-family="%s" font-size="11.5" fill="%s">查詢結果</text>'
          % (FONT, ACC))
    b += ('<text x="440" y="122" font-family="%s" font-size="11.5" fill="%s">HTML</text>' % (FONT, WARM))
    return _wrap(b, 860, 250, "Django MVT 架構：瀏覽器、URL 路由、視圖、模型、模板與資料庫的關係",
                 "圖 1　Django 的 MVT 架構：請求經 URL 路由進入視圖，視圖透過模型存取資料庫，再把資料交給模板渲染成 HTML。")


def relations():
    b = _box(20, 70, 120, 56, "Author")
    b += _box(190, 70, 140, 56, "Article", "ForeignKey")
    b += ('<text x="165" y="60" font-family="%s" font-size="11" fill="%s">1 : N</text>' % (FONT, ACC))
    b += _arrow(140, 98, 186, 98)
    b += _box(370, 70, 120, 56, "Tag")
    b += _box(540, 70, 140, 56, "Article", "ManyToMany")
    b += ('<text x="510" y="60" font-family="%s" font-size="11" fill="%s">N : N</text>' % (FONT, ACC))
    b += _arrow(490, 98, 536, 98)
    b += _box(20, 160, 120, 56, "User")
    b += _box(190, 160, 140, 56, "Profile", "OneToOne")
    b += ('<text x="165" y="150" font-family="%s" font-size="11" fill="%s">1 : 1</text>' % (FONT, ACC))
    b += _arrow(140, 188, 186, 188)
    return _wrap(b, 720, 240, "Django 三種模型關聯：一對多、多對多、一對一",
                 "圖 2　三種模型關聯：ForeignKey（一對多）、ManyToManyField（多對多）、OneToOneField（一對一）。")


def gitflow():
    y_main, y_dev, y_feat, y_rel, y_fix = 170, 120, 70, 30, 210
    b = '<line x1="150" y1="%d" x2="820" y2="%d" stroke="%s" stroke-width="2"/>' % (y_main, y_main, STROKE)
    b += '<line x1="150" y1="%d" x2="820" y2="%d" stroke="%s" stroke-width="2"/>' % (y_dev, y_dev, ACC)
    b += '<line x1="200" y1="%d" x2="330" y2="%d" stroke="%s" stroke-width="1.8"/>' % (y_dev, y_feat, WARM)
    b += '<line x1="330" y1="%d" x2="420" y2="%d" stroke="%s" stroke-width="1.8"/>' % (y_feat, y_dev, WARM)
    b += '<line x1="450" y1="%d" x2="560" y2="%d" stroke="%s" stroke-width="1.8"/>' % (y_dev, y_rel, WARM)
    b += '<line x1="560" y1="%d" x2="640" y2="%d" stroke="%s" stroke-width="1.8"/>' % (y_rel, y_main, WARM)
    b += '<line x1="640" y1="%d" x2="760" y2="%d" stroke="%s" stroke-width="1.8"/>' % (y_main, y_fix, WARM)
    b += '<line x1="760" y1="%d" x2="800" y2="%d" stroke="%s" stroke-width="1.8"/>' % (y_fix, y_main, WARM)
    for x in (120, 200, 420, 640, 800):
        b += '<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (x, y_main, ACC)
    for x in (120, 200, 420, 560):
        b += '<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (x, y_dev, "#7ee787")
    b += ('<text x="20" y="%d" font-family="%s" font-size="12" fill="%s">master／main</text>' % (y_main + 5, FONT, TEXT))
    b += ('<text x="20" y="%d" font-family="%s" font-size="12" fill="%s">develop</text>' % (y_dev + 5, FONT, "#7ee787"))
    b += ('<text x="212" y="%d" font-family="%s" font-size="12" fill="%s">feature 分支</text>' % (y_feat - 6, FONT, WARM))
    b += ('<text x="470" y="%d" font-family="%s" font-size="12" fill="%s">release</text>' % (y_rel - 6, FONT, WARM))
    b += ('<text x="668" y="%d" font-family="%s" font-size="12" fill="%s">hotfix</text>' % (y_fix - 6, FONT, WARM))
    return _wrap(b, 860, 250, "Git Flow 分支模型：main、develop、feature、release、hotfix",
                 "圖 3　Git Flow：長期分支 main／develop，短期分支 feature、release、hotfix 各自合併回對應的長期分支。")

def url_flow():
    b = _box(20, 90, 150, 62, "請求", "GET /post/42")
    b += _box(210, 90, 190, 62, "urlpatterns", "path() 由上而下比對")
    b += _box(450, 20, 200, 62, "視圖", "post_detail(request, id=42)")
    b += _box(450, 165, 200, 62, "404", "沒有規則匹配", stroke=WARM)
    b += _box(700, 20, 140, 62, "回應", "HttpResponse")
    b += _arrow(170, 121, 206, 121)
    b += _arrow(400, 108, 446, 62)
    b += _arrow(400, 134, 446, 190)
    b += _arrow(650, 51, 696, 51)
    return _wrap(b, 860, 250, "Django URL 路由解析：請求依 urlpatterns 逐條比對，命中就呼叫視圖，否則回 404",
                 "圖　URL 路由解析：請求進來後由 urlpatterns 逐條比對，<code>path('post/&lt;int:id&gt;/')</code> 命中就把 id 傳給視圖，沒有命中則回 404。")


def auth_flow():
    b = _box(20, 95, 150, 62, "登入表單", "POST 帳號密碼")
    b += _box(210, 95, 160, 62, "authenticate()", "驗證帳密")
    b += _box(410, 95, 150, 62, "login()", "寫入 session")
    b += _box(600, 95, 150, 62, "登入後頁面", "redirect")
    b += _box(210, 12, 160, 58, "驗證失敗", "回表單顯示錯誤", stroke=WARM)
    b += _box(395, 190, 180, 58, "登出", "LogoutView（只收 POST）", stroke=WARM)
    b += _arrow(170, 126, 206, 126)
    b += _arrow(290, 95, 290, 74)
    b += _arrow(370, 126, 406, 126)
    b += _arrow(560, 126, 596, 126)
    b += _arrow(485, 157, 485, 186)
    b += _arrow(560, 219, 690, 160)
    return _wrap(b, 800, 262, "Django 認證流程：表單、authenticate、login 寫入 session、登出需用 POST",
                 "圖　認證流程：<code>authenticate()</code> 驗證帳密，成功才呼叫 <code>login()</code> 寫入 session；"
                 "登出走 <code>LogoutView</code>，Django 5.0 起只接受 POST。")


def cicd():
    b = _box(20, 95, 130, 62, "git push", "推送程式碼")
    b += _box(180, 95, 150, 62, "CI：安裝", "pip install -r")
    b += _box(360, 95, 150, 62, "CI：測試", "manage.py test")
    b += _box(540, 95, 130, 62, "建置", "hexo／容器映像")
    b += _box(700, 95, 140, 62, "部署與監控", "Pages／K8s")
    for x1, x2 in ((150, 176), (330, 356), (510, 536), (670, 696)):
        b += _arrow(x1, 126, x2, 126)
    b += ('<text x="182" y="86" font-family="%s" font-size="11" fill="%s">失敗即中斷</text>' % (FONT, WARM))
    return _wrap(b, 860, 200, "CI/CD 管線：push、安裝依賴、測試、建置、部署與監控",
                 "圖　CI/CD 管線：push 之後自動安裝依賴、跑測試（失敗即中斷），再建置與部署，最後由監控與日誌接手。")


def orm_chain():
    b = _box(20, 95, 190, 62, "QuerySet 鏈式呼叫", "filter()／order_by()／切片")
    b += _box(240, 95, 170, 62, "延遲求值", "真正用到才查詢")
    b += _box(440, 95, 120, 62, "SQL", "SELECT …")
    b += _box(590, 95, 120, 62, "資料庫", "SQLite／PG")
    b += _box(740, 95, 100, 62, "物件", "Model 實例")
    for x1, x2 in ((210, 236), (410, 436), (560, 586), (710, 736)):
        b += _arrow(x1, 126, x2, 126)
    b += ('<text x="245" y="86" font-family="%s" font-size="11" fill="%s">不快取、可再串接</text>' % (FONT, ACC))
    return _wrap(b, 860, 200, "ORM 查詢鏈：QuerySet 鏈式呼叫、延遲求值、生成 SQL 到資料庫取回物件",
                 "圖　ORM 查詢鏈：鏈式呼叫只是組裝條件，QuerySet 延遲求值，真正迭代時才產生 SQL 並回傳 Model 實例。")


FIGURES = [
    (7, "#### 1.2.2 MVT 架構", mvt()),
    (8, "### 4.1 Django 的 URL 配置", url_flow()),
    (10, "## 8.1 模型中的關聯關係", relations()),
    (10, "## 7.3 使用 Django 的查詢集 API", orm_chain()),
    (11, "### 13.4. 用戶登錄與登出功能", auth_flow()),
    (12, "#### 6.2.2 Git Flow 的分支模型", gitflow()),
    (13, "### 9.3 持續集成與持續部署 (CI/CD)", cicd()),
]
