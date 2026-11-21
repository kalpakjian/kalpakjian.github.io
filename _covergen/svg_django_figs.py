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

FIGURES = [
    (7, "#### 1.2.2 MVT 架構", mvt()),
    (10, "## 8.1 模型中的關聯關係", relations()),
    (12, "#### 6.2.2 Git Flow 的分支模型", gitflow()),
]
