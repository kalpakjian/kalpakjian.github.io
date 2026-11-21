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


def use_case():
    # 系統邊界 + 參與者框 + 橢圓用例
    b = '<rect x="210" y="24" width="360" height="244" rx="12" fill="none" stroke="%s" stroke-width="1.6"/>' % STROKE
    b += ('<text x="390" y="48" text-anchor="middle" font-family="%s" font-size="13" fill="%s">活動報名系統</text>'
          % (FONT, ACC))
    def oval(cx, cy, label):
        return ('<ellipse cx="%d" cy="%d" rx="96" ry="30" fill="%s" stroke="%s" stroke-width="1.5"/>'
                '<text x="%d" y="%d" text-anchor="middle" font-family="%s" font-size="13" fill="%s">%s</text>'
                % (cx, cy, BOX, STROKE, cx, cy + 5, FONT, TEXT, label))
    b += oval(390, 96, "瀏覽活動")
    b += oval(390, 176, "報名活動")
    b += oval(390, 246, "審核報名")
    b += _box(20, 76, 110, 50, "訪客")
    b += _box(20, 151, 110, 50, "會員")
    b += _box(640, 221, 110, 50, "管理員")
    b += '<line x1="130" y1="101" x2="292" y2="96" stroke="%s" stroke-width="1.4"/>' % ACC
    b += '<line x1="130" y1="176" x2="292" y2="176" stroke="%s" stroke-width="1.4"/>' % ACC
    b += '<line x1="640" y1="246" x2="488" y2="246" stroke="%s" stroke-width="1.4"/>' % ACC
    return _wrap(b, 770, 292, "UML 用例圖：訪客、會員、管理員與活動報名系統的用例關係",
                 "圖　用例圖：左邊兩位參與者（訪客、會員）與右邊的管理員，各自連到系統邊界內對應的用例。")


def class_diagram():
    def cls(x, y, w, name, attrs, ops):
        h = 78
        t = '<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="%s" stroke="%s" stroke-width="1.6"/>' % (
            x, y, w, h, BOX, STROKE)
        t += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2"/>' % (x, y + 26, x + w, y + 26, STROKE)
        t += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2"/>' % (x, y + 52, x + w, y + 52, STROKE)
        t += ('<text x="%d" y="%d" text-anchor="middle" font-family="%s" font-size="13" fill="%s">%s</text>'
              % (x + w // 2, y + 18, FONT, TEXT, name))
        t += ('<text x="%d" y="%d" font-family="%s" font-size="11" fill="%s">%s</text>'
              % (x + 8, y + 42, FONT, ACC, attrs))
        t += ('<text x="%d" y="%d" font-family="%s" font-size="11" fill="%s">%s</text>'
              % (x + 8, y + 68, FONT, ACC, ops))
        return t
    b = cls(20, 90, 170, "Category", "+ name: CharField", "+ slug: SlugField")
    b += cls(260, 90, 190, "Article", "+ title: CharField", "+ published: Boolean")
    b += cls(520, 20, 160, "Tag", "+ name: CharField", "")
    b += cls(520, 170, 170, "Comment", "+ body: TextField", "+ created: DateTime")
    b += _arrow(190, 129, 256, 129)
    b += ('<text x="200" y="120" font-family="%s" font-size="11" fill="%s">1 : N</text>' % (FONT, ACC))
    b += '<line x1="450" y1="105" x2="516" y2="60" stroke="%s" stroke-width="1.5"/>' % ACC
    b += ('<text x="462" y="76" font-family="%s" font-size="11" fill="%s">N : N</text>' % (FONT, ACC))
    b += _arrow(450, 150, 516, 200)
    b += ('<text x="452" y="196" font-family="%s" font-size="11" fill="%s">1 : N</text>' % (FONT, ACC))
    return _wrap(b, 720, 280, "UML 類圖：Category、Article、Tag、Comment 四個類別與關聯",
                 "圖　類圖：每個類別分三格（類名／屬性／方法）；<code>Category 1:N Article</code>、"
                 "<code>Article N:N Tag</code>、<code>Article 1:N Comment</code>。")


def sequence():
    lanes = [("瀏覽器", 90), ("視圖", 310), ("模型", 530), ("模板", 730)]
    b = ""
    for name, x in lanes:
        b += _box(x - 60, 12, 120, 46, name)
        b += '<line x1="%d" y1="58" x2="%d" y2="270" stroke="%s" stroke-width="1.2" stroke-dasharray="5 4"/>' % (
            x, x, STROKE)
    msgs = [(90, 310, 96, "GET /post/42"), (310, 530, 132, "query(id=42)"),
            (530, 310, 168, "Article 物件"), (310, 730, 204, "render(context)"),
            (730, 90, 240, "HTML 回應")]
    for x1, x2, y, label in msgs:
        arrow = "marker-end"
        if x2 < x1:
            b += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6" %s="url(#a)"/>' % (
                x1, y, x2 + 6, y, ACC, arrow)
        else:
            b += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6" %s="url(#a)"/>' % (
                x1, y, x2 - 6, y, ACC, arrow)
        b += ('<text x="%d" y="%d" text-anchor="middle" font-family="%s" font-size="11" fill="%s">%s</text>'
              % ((x1 + x2) // 2, y - 7, FONT, TEXT, label))
    return _wrap(b, 860, 292, "UML 序列圖：瀏覽器、視圖、模型、模板之間的訊息往來",
                 "圖　序列圖：由上往下代表時間順序，實線箭頭是訊息；視圖先向模型取資料，再把 context 交給模板。")


def template_inherit():
    b = _box(300, 20, 260, 62, "base.html", "{% block content %}", stroke=WARM)
    b += _box(30, 170, 210, 62, "index.html", "extends base.html")
    b += _box(320, 170, 210, 62, "article.html", "extends base.html")
    b += _box(610, 170, 210, 62, "about.html", "extends base.html")
    for x in (135, 425, 715):
        b += '<line x1="%d" y1="170" x2="%d" y2="86" stroke="%s" stroke-width="1.6" marker-start="url(#a)"/>' % (
            x, 430, ACC)
    b += ('<text x="430" y="256" text-anchor="middle" font-family="%s" font-size="11" fill="%s">'
          '{%% block content %%} 由子模板覆寫，其餘沿用 base.html</text>' % (FONT, WARM))
    return _wrap(b, 860, 272, "Django 模板繼承：base.html 被三個子模板 extends",
                 "圖　模板繼承：子模板 <code>{% extends \"base.html\" %}</code>，只覆寫自己需要的 block，"
                 "共用導覽列與頁尾。")


def activity():
    b = '<circle cx="60" cy="60" r="14" fill="%s"/>' % ACC
    b += _box(20, 100, 160, 56, "瀏覽活動")
    b += '<text x="300" y="76" font-family="%s" font-size="12" fill="%s">名額足夠？</text>' % (FONT, TEXT)
    b += ('<polygon points="300,90 380,124 300,158 220,124" fill="%s" stroke="%s" stroke-width="1.6"/>'
          % (BOX, STROKE))
    b += _box(430, 96, 150, 56, "填表報名")
    b += _box(430, 186, 150, 56, "顯示已滿", stroke=WARM)
    b += _box(700, 96, 130, 56, "送出報名")
    b += '<circle cx="790" cy="200" r="16" fill="none" stroke="%s" stroke-width="2"/><circle cx="790" cy="200" r="10" fill="%s"/>' % (STROKE, ACC)
    b += _arrow(60, 74, 60, 96)
    b += _arrow(100, 156, 216, 132)
    b += _arrow(380, 124, 426, 124)
    b += '<text x="392" y="116" font-family="%s" font-size="11" fill="%s">是</text>' % (FONT, "#7ee787")
    b += _arrow(300, 158, 300, 214)
    b += _arrow(300, 214, 426, 214)
    b += '<text x="310" y="206" font-family="%s" font-size="11" fill="%s">否</text>' % (FONT, WARM)
    b += _arrow(580, 124, 696, 124)
    b += _arrow(765, 152, 788, 182)
    b += _arrow(580, 214, 772, 206)
    return _wrap(b, 860, 240, "UML 活動圖：瀏覽活動、判斷名額、填表報名或顯示已滿",
                 "圖　活動圖：實心圓是起點、同心圓是終點；菱形是判斷節點，兩條分支各自走到結束。")


def state():
    b = _box(40, 96, 170, 62, "草稿", "draft")
    b += _box(330, 96, 170, 62, "已發佈", "published", stroke=WARM)
    b += _box(620, 96, 170, 62, "已下架", "archived")
    b += '<circle cx="20" cy="127" r="10" fill="%s"/>' % ACC
    b += _arrow(30, 127, 36, 127)
    b += _arrow(210, 127, 326, 127)
    b += ('<text x="222" y="118" font-family="%s" font-size="11" fill="%s">發佈</text>' % (FONT, "#7ee787"))
    b += _arrow(500, 127, 616, 127)
    b += ('<text x="512" y="118" font-family="%s" font-size="11" fill="%s">下架</text>' % (FONT, WARM))
    b += '<path d="M415 158 Q415 196 300 196 Q120 196 120 162" fill="none" stroke="%s" stroke-width="1.5" marker-end="url(#a)"/>' % ACC
    b += ('<text x="250" y="214" font-family="%s" font-size="11" fill="%s">編輯（回到草稿）</text>' % (FONT, ACC))
    return _wrap(b, 830, 240, "UML 狀態圖：草稿、已發佈、已下架三個狀態與轉換",
                 "圖　狀態圖：圓角框是狀態、箭頭是轉換；「編輯」會讓已發佈的文章回到草稿狀態。")


def deployment():
    b = '<rect x="20" y="26" width="220" height="180" rx="12" fill="none" stroke="%s" stroke-width="1.4"/>' % STROKE
    b += ('<text x="130" y="48" text-anchor="middle" font-family="%s" font-size="11.5" fill="%s">使用者端</text>'
          % (FONT, ACC))
    b += _box(50, 70, 160, 100, "瀏覽器", "HTML／CSS／JS")
    b += '<rect x="270" y="26" width="300" height="190" rx="12" fill="none" stroke="%s" stroke-width="1.4"/>' % STROKE
    b += ('<text x="420" y="48" text-anchor="middle" font-family="%s" font-size="11.5" fill="%s">伺服器節點</text>'
          % (FONT, ACC))
    b += _box(292, 66, 120, 60, "Nginx", "靜態／代理")
    b += _box(432, 66, 122, 60, "Gunicorn", "WSGI")
    b += _box(292, 158, 120, 52, "Django", "應用程式")
    b += _box(432, 158, 122, 52, "PostgreSQL", "資料庫")
    b += _box(630, 66, 180, 126, "物件儲存", "媒體檔案／備份")
    b += _arrow(210, 120, 288, 96)
    b += _arrow(412, 96, 428, 96)
    b += _arrow(352, 128, 352, 154)
    b += _arrow(493, 128, 493, 154)
    b += '<line x1="554" y1="100" x2="626" y2="100" stroke="%s" stroke-width="1.5" stroke-dasharray="4 3"/>' % ACC
    return _wrap(b, 860, 228, "UML 部署圖：使用者端瀏覽器、伺服器節點的 Nginx／Gunicorn／Django／PostgreSQL",
                 "圖　部署圖：外框是節點（node），裡面的方框是執行的元件；Nginx 轉給 Gunicorn，Django 連 PostgreSQL 與物件儲存。")


def rebase_merge():
    G = "#7ee787"
    # 左：merge（分支出去再合併回來，留下菱形合併 commit）
    b = '<line x1="40" y1="110" x2="380" y2="110" stroke="%s" stroke-width="2"/>' % STROKE
    for x in (60, 120, 300, 360):
        b += '<circle cx="%d" cy="110" r="6" fill="%s"/>' % (x, ACC)
    b += '<path d="M120 110 Q150 170 210 170 Q260 170 300 116" fill="none" stroke="%s" stroke-width="2"/>' % G
    for x in (170, 240):
        b += '<circle cx="%d" cy="170" r="6" fill="%s"/>' % (x, G)
    b += ('<polygon points="300,96 312,110 300,124 288,110" fill="%s" stroke="%s" stroke-width="1.4"/>'
          % (CARD, WARM))
    b += ('<text x="40" y="44" font-family="%s" font-size="12.5" fill="%s">merge：留下一個合併 commit（菱形）</text>'
          % (FONT, TEXT))
    b += ('<text x="176" y="196" font-family="%s" font-size="11" fill="%s">feature 分支</text>' % (FONT, G))
    # 右：rebase（歷史攤平，原 commit 被重寫）
    b += '<line x1="470" y1="110" x2="820" y2="110" stroke="%s" stroke-width="2"/>' % STROKE
    for x in (500, 560, 620, 680, 760):
        b += '<circle cx="%d" cy="110" r="6" fill="%s"/>' % (x, ACC)
    b += '<path d="M680 104 Q700 60 742 52" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="5 4"/>' % WARM
    b += '<circle cx="748" cy="52" r="5" fill="none" stroke="%s" stroke-width="1.6"/>' % WARM
    b += ('<text x="470" y="44" font-family="%s" font-size="12.5" fill="%s">rebase：歷史攤平成一直線</text>'
          % (FONT, TEXT))
    b += ('<text x="590" y="196" font-family="%s" font-size="11" fill="%s">原 commit 被重寫（虛線）</text>'
          % (FONT, WARM))
    return _wrap(b, 860, 220, "Git merge 與 rebase 的歷史差異：合併 commit 對比線性歷史",
                 "圖　merge 會在兩條歷史交會處留下一個合併 commit（菱形）；rebase 則把分支 commit 重寫到目標分支之後，歷史變成一直線。")


def object_diagram():
    def obj(x, y, w, name, attrs, stroke=STROKE):
        h = 30 + 22 * len(attrs)
        t = '<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" stroke="%s" stroke-width="1.6"/>' % (
            x, y, w, h, BOX, stroke)
        t += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2"/>' % (x, y + 26, x + w, y + 26, stroke)
        t += ('<text x="%d" y="%d" text-anchor="middle" font-family="%s" font-size="12.5" fill="%s" '
              'text-decoration="underline">%s</text>' % (x + w // 2, y + 18, FONT, TEXT, name))
        for i, a in enumerate(attrs):
            t += ('<text x="%d" y="%d" font-family="%s" font-size="11" fill="%s">%s</text>'
                  % (x + 10, y + 46 + 22 * i, FONT, ACC, a))
        return t
    b = obj(30, 60, 210, "cat1 : Category", ["name = \"Python\"", "slug = \"python\""])
    b += obj(360, 60, 250, "article1 : Article",
             ["title = \"Django 入門\"", "published = True", "category = cat1"], stroke=WARM)
    b += '<line x1="240" y1="96" x2="356" y2="96" stroke="%s" stroke-width="1.6"/>' % ACC
    b += ('<text x="248" y="88" font-family="%s" font-size="11" fill="%s">category</text>' % (FONT, ACC))
    b += ('<text x="30" y="24" font-family="%s" font-size="12" fill="%s">物件圖＝某一刻的實例快照（名稱加底線）</text>'
          % (FONT, TEXT))
    return _wrap(b, 660, 210, "UML 物件圖：cat1 與 article1 兩個實例以及 category 連結",
                 "圖　物件圖：cat1 : Category 與 article1 : Article 是實際存在的資料，"
                 "名稱加底線代表實例；兩個物件之間的連線對應類圖的關聯。")


def component_diagram():
    def comp(x, y, w, h, label, sub=""):
        t = _box(x, y, w, h, label, sub)
        t += ('<rect x="%d" y="%d" width="14" height="22" rx="2" fill="%s" stroke="%s" stroke-width="1.2"/>'
              % (x + w - 22, y + 8, CARD, ACC))
        t += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2"/>' % (
            x + w - 18, y + 15, x + w - 12, y + 15, ACC)
        return t
    b = comp(30, 90, 170, 66, "模板層", "templates／block")
    b += comp(250, 90, 180, 66, "視圖層", "views.py")
    b += comp(480, 90, 180, 66, "模型層", "models.py／ORM")
    b += comp(700, 90, 130, 66, "資料庫", "PostgreSQL")
    for x1, x2 in ((200, 246), (430, 476), (660, 696)):
        b += _arrow(x1, 123, x2, 123)
    b += ('<text x="30" y="60" font-family="%s" font-size="12" fill="%s">方框右上角是 UML 的 component 標記</text>'
          % (FONT, TEXT))
    b += ('<text x="30" y="196" font-family="%s" font-size="11" fill="%s">箭頭由左往右：上層依賴下層</text>' % (FONT, ACC))
    return _wrap(b, 860, 210, "UML 組件圖：模板層、視圖層、模型層與資料庫的依賴關係",
                 "圖　組件圖：每個方框是一個可替換的元件，箭頭代表依賴；視圖層依賴模型層，模型層依賴資料庫。")


FIGURES = [
    (7, "#### 1.2.2 MVT 架構", mvt()),
    (8, "### 4.1 Django 的 URL 配置", url_flow()),
    (10, "## 8.1 模型中的關聯關係", relations()),
    (10, "## 7.3 使用 Django 的查詢集 API", orm_chain()),
    (11, "### 13.4. 用戶登錄與登出功能", auth_flow()),
    (12, "#### 6.2.2 Git Flow 的分支模型", gitflow()),
    (12, "#### 5.1.2 變基與合併的區別", rebase_merge()),
    (12, "### 9.3 持續集成與持續部署 (CI/CD)", cicd()),
    (9, "### 6.4 模板繼承", template_inherit()),
    (14, "### 2.1 用例圖概述", use_case()),
    (14, "### 3.1 類圖概述", class_diagram()),
    (14, "### 4.1 對象圖概述", object_diagram()),
    (14, "### 5.1 序列圖概述", sequence()),
    (14, "### 6.1 活動圖概述", activity()),
    (14, "### 7.1 狀態圖概述", state()),
    (14, "### 8.1 組件圖概述", component_diagram()),
    (14, "### 9.1 部署圖概述", deployment()),
]
