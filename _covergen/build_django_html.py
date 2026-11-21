# -*- coding: utf-8 -*-
"""14 章 md → 單檔 HTML（opencv-notes 風格）＋ 章節封面／副標／上一章下一章。

    python build_django_html.py [--only ch07]

前置：build_django_notes.py 已產出 source/django-notes/chNN-*.md
輸出：source/django-notes/chNN-*.html（skip_render，原樣上線）
"""
import io
import os
import re
import subprocess
import sys

BLOG = r"C:\Users\princ\kalpakjian.github.io"
NOTES = os.path.join(BLOG, "source", "django-notes")
TOOL = r"C:\Users\princ\.agents\skills\pdf-to-md-notes\scripts\notes_to_html.py"
COURSE_URL = "/django-course/"
TOTAL = 14

# slug, 章名, 起頁, 迄頁
CHAPTERS = [
    ("thinking-web", "計算思維與網頁框架基礎", 2, 15),
    ("python-intro", "Python 簡介與安裝", 16, 23),
    ("syntax", "Python3 基礎語法", 24, 28),
    ("datatypes", "數據類型、運算符與數字", 29, 47),
    ("sequence", "序列與容器類型", 48, 60),
    ("control-oop", "流程控制、函數、模組與面向對象", 61, 94),
    ("django-basics", "Django 基礎與環境建置", 95, 108),
    ("project-settings", "Project、App 與 settings 配置", 109, 128),
    ("views-templates", "URL 路由、視圖與模板", 129, 146),
    ("models-orm", "模型、ORM 與查詢集", 147, 173),
    ("auth-project", "分頁、美化、認證與專案實作", 174, 209),
    ("backend-workflow", "後端網站開發工作流程", 210, 351),
    ("remote-dev", "遠端開發環境", 352, 370),
    ("uml", "UML 系統分析與設計", 371, 405),
]

EXTRA_CSS = """
/* ---- Django 學習筆記：章節封面 + 章節導覽（本站既有慣例） ---- */
main .sub{font-size:13px;color:var(--muted);margin:-8px 0 16px}
figure.hero{margin:0 0 26px}
figure.hero img{width:100%;height:auto;border-radius:10px;border:1px solid var(--border);display:block}
figure.hero figcaption{font-size:12.5px;color:var(--muted);margin-top:6px;text-align:center}
figure.fig-svg{margin:22px 0 26px}
figure.fig-svg svg{display:block;width:100%;height:auto;print-color-adjust:exact;-webkit-print-color-adjust:exact}
figure.fig-svg figcaption{font-size:12.5px;color:var(--muted);margin-top:8px;text-align:center}
.chnav{display:flex;gap:8px;flex-wrap:wrap;margin:30px 0 10px;font-size:13px}
.chnav a{flex:1;min-width:150px;text-align:center;text-decoration:none;color:var(--accent2);
  border:1px solid var(--border);border-radius:6px;padding:9px 10px;background:#fff}
.chnav a:hover{background:#eaeef2}
.chnav a.course{font-weight:700}
"""


def build_one(no, slug, title, p1, p2):
    md = os.path.join(NOTES, "ch%02d-%s.md" % (no, slug))
    html_path = os.path.join(NOTES, "ch%02d-%s.html" % (no, slug))
    page_title = "第 %d 章 %s — Django 學習筆記" % (no, title)
    subtitle = "Django 網站框架開發 · 學習筆記<br>第 %d 章 · %s" % (no, title)
    cmd = [
        sys.executable, TOOL, md, "--out", html_path,
        "--title", page_title,
        "--sidebar-title", "Django 學習筆記",
        "--subtitle", subtitle,
        "--home-url", COURSE_URL, "--home-text", "← 課程總覽",
        "--no-math",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        print("  !! 轉檔失敗", r.stdout, r.stderr)
        return False

    html = io.open(html_path, encoding="utf-8").read()
    cover = "/img/covers/django-ch%02d.png" % no
    sub = "p.%d–p.%d　%d 頁　第 %d/%d 章" % (p1, p2, p2 - p1 + 1, no, TOTAL)
    hero = (
        '<div class="sub">%s</div>\n'
        '<figure class="hero"><img src="%s" alt="第 %d 章 封面">'
        "<figcaption>封面插圖：Qwen-Image 2.1 生成</figcaption></figure>" % (sub, cover, no)
    )
    html, n = re.subn(r"(</h1>)", r"\1\n" + hero, html, count=1)
    assert n == 1, "找不到章節 h1，無法插入封面"

    nav = ['<div class="chnav">']
    if no > 1:
        s, t = CHAPTERS[no - 2][0], CHAPTERS[no - 2][1]
        nav.append('<a href="/django-notes/ch%02d-%s.html">← 第 %d 章 %s</a>' % (no - 1, s, no - 1, t))
    else:
        nav.append('<a href="%s">← 課程總覽</a>' % COURSE_URL)
    nav.append('<a class="course" href="%s">課程總覽</a>' % COURSE_URL)
    if no < TOTAL:
        s, t = CHAPTERS[no][0], CHAPTERS[no][1]
        nav.append('<a href="/django-notes/ch%02d-%s.html">第 %d 章 %s →</a>' % (no + 1, s, no + 1, t))
    nav.append("</div>")
    html = html.replace("</main>", "\n".join(nav) + "\n</main>")
    html = html.replace("</head>", "<style>%s</style>\n</head>" % EXTRA_CSS, 1)

    io.open(html_path, "w", encoding="utf-8", newline="\n").write(html)

    # 交付前檢查
    assert html.count("<h1") == 2, "h1 數量異常（側邊欄+內文應為 2）"  # sidebar + chapter
    assert cover in html
    assert 'src="http' not in html, "出現外部資源"
    assert html.count("```") == 0
    print("  ch%02d %-16s %7d KB  圖 %d 張" % (no, slug, len(html) // 1024, html.count("<img")))
    return True


def main():
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    for i, (slug, title, p1, p2) in enumerate(CHAPTERS, 1):
        if only and only not in ("ch%02d" % i, slug):
            continue
        build_one(i, slug, title, p1, p2)


if __name__ == "__main__":
    main()
