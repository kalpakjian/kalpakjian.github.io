# -*- coding: utf-8 -*-
"""把整理好的 OCR 筆記切成 14 章 md，供 notes_to_html.py 轉單檔 HTML。

    python build_django_notes.py [--split-only]

來源：C:\\Users\\princ\\OneDrive\\Documents\\Scan_20261121_OCR_clean.md
輸出：<blog>\\source\\django-notes\\chNN-<slug>.md
重用 clean_ocr_notes.py 的頁面切分／去頁眉／跨頁接句，保證章節內容與總覽一致。
"""
import io
import os
import re
import sys

sys.path.insert(0, r"C:\Users\princ\OneDrive\Documents")
import clean_ocr_notes as c  # noqa: E402

BLOG = r"C:\Users\princ\kalpakjian.github.io"
OUTDIR = os.path.join(BLOG, "source", "django-notes")

# (slug, 章名, 起頁, 迄頁) —— 邊界對齊原稿章節起始頁
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
    ("git-basics", "後端開發與 Git 基礎", 210, 296),
    ("collab-cicd", "協作、安全與 CI/CD", 297, 352),
    ("cloud-uml", "雲端開發與 UML 系統分析", 353, 405),
]

# 站上筆記寫作契約：這幾個詞在成品中必須 0 次
FORBIDDEN = [("本節", "這一節"), ("本文", "本筆記")]

# 原稿把模板範例拆成裸 HTML，會在成品變成真連結（CI 內部連結閘門會擋）→ 改回程式碼片段
CONTENT_FIXES = [
    (
        '請先 <a href="/login/" >登入</a> 。 </p>',
        '需要登入才能看內容時，模板用 `{% url \'login\' %}` 產生登入連結（`<a>` 連結文字寫「登入」）。',
    ),
]

# 2026-11 覆核：前端／Actions 版本 + 教材年份留下的工具（只加一句時代註記，不改寫教材結構）
ERA_FIXES = [
    # B1 Bootstrap：5.3.0-alpha1（2022 的 alpha）→ 現行 5.3.9
    ("bootstrap@5.3.0-alpha1", "bootstrap@5.3.9"),
    # B2 GitHub Actions：v2（Node12 時代）→ v7
    ("actions/checkout@v2", "actions/checkout@v7"),
    ("actions/setup-python@v2", "actions/setup-python@v7"),
    # C1 Travis CI：免費額度 2021 收緊
    (
        "常見的 CI 工具包括 Jenkins、Travis CI 和 CircleCI。",
        "常見的 CI 工具包括 Jenkins、Travis CI 和 CircleCI。"
        "（時代註記：Travis CI 的免費額度自 2021 年大幅收緊，新專案多改用 GitHub Actions 或 GitLab CI；"
        "這一節保留是為了理解概念。）",
    ),
    # C2 CentOS 7/8 已停止維護
    (
        "在 CentOS/Fedora 上：",
        "在 CentOS Stream／Rocky Linux／Fedora 上（CentOS 7 於 2024-06、CentOS 8 於 2021-12 已停止維護）：",
    ),
    ("常見的選擇有 Linux（如 Ubuntu、CentOS）", "常見的選擇有 Linux（如 Ubuntu LTS、Rocky Linux）"),
    # C3 ELK 7.13.2（2021）
    (
        "ELK 堆棧由 Elasticsearch、Logstash 和 Kibana 組成，是一個強大的日誌管理解決方案。",
        "ELK 堆棧由 Elasticsearch、Logstash 和 Kibana 組成，是一個強大的日誌管理解決方案。"
        "（時代註記：下面的指令是 2021 年的 7.13.2 版本；現行 Elastic Stack 已到 8.x 以上，"
        "下載連結與設定格式略有不同。）",
    ),
    # C4 GitHub 新倉庫預設 main
    (
        "使用主分支（master）和開發分支（develop）。",
        "使用主分支（master）和開發分支（develop）。"
        "（時代註記：GitHub 自 2020 年起新倉庫預設分支名為 `main`，原理相同。）",
    ),
    (
        "使用主分支 (master) 和開發分支 (develop)。",
        "使用主分支 (master) 和開發分支 (develop)。"
        "（時代註記：GitHub 自 2020 年起新倉庫預設分支名為 `main`，原理相同。）",
    ),
]

# OCR 把 SRI 雜湊拆成兩行，貼進專案會被瀏覽器拒載 → 直接移除 integrity / crossorigin
INTEGRITY_RE = re.compile(r'integrity="sha384-[^"]*"\s*\n(crossorigin="anonymous"\s*\n)?')


def render_md(items, no, title):
    out = ["# 第 %d 章 · %s" % (no, title), ""]
    # 原稿標題層級不一致（同一層有時是 h3 有時是 h4），依「本章實際出現的層級」重新映射：
    # 最淺 → ##（側邊欄第一層），下一層 → ###，其餘 → ####。單元標題（h2）當分隔，不進正文。
    levels = sorted({it[1] for it in items if it[0] == "h" and it[1] > 2})
    level_map = {lv: min(2 + i, 4) for i, lv in enumerate(levels)}
    code = []

    def flush():
        if code:
            out.append("```\n%s\n```" % "\n".join(code))
            del code[:]

    for it in items:
        if it[0] == "c":
            code.append(it[1])
            continue
        flush()
        if it[0] == "h":
            if it[1] == 2:  # 單元標題
                continue
            out.append("#" * level_map[it[1]] + " " + it[2])
        else:
            out.append(c.BULLET_SUB.sub("- ", it[1]))
        out.append("")
    flush()
    text = "\n".join(out).rstrip() + "\n"
    for old, new in FORBIDDEN + CONTENT_FIXES:
        text = text.replace(old, new)
    # A：套用總稿（clean_ocr_notes.py）已驗證的版本修正表（Django 5.2 LTS、Python 3.14、from django.* …）
    for old, new in c.VERSION_UPDATES:
        text = text.replace(old, new)
    # B/C：前端與 Actions 版本、教材年份註記
    for old, new in ERA_FIXES:
        text = text.replace(old, new)
    text = INTEGRITY_RE.sub("", text)
    # 正文的 ** 是冪運算符或 OCR 裝飾線，留在正文會被當成粗體配對 → 轉義（程式碼區塊內不動）
    lines, in_code = [], False
    for ln in text.split("\n"):
        if ln.startswith("```"):
            in_code = not in_code
        elif not in_code and "**" in ln:
            ln = ln.replace("**", r"\*\*")
        lines.append(ln)
    return "\n".join(lines) + "\n"


def main():
    lines = io.open(c.SRC, encoding="utf-8").read().splitlines()
    pages = c.split_pages(lines)
    os.makedirs(OUTDIR, exist_ok=True)
    total = 0
    for i, (slug, title, p1, p2) in enumerate(CHAPTERS, 1):
        subset = [(n, body) for n, body in pages if p1 <= n <= p2]
        assert subset, "第 %d 章找不到頁面 %d-%d" % (i, p1, p2)
        items = c.merge_wrapped(c.build_items(subset))
        md = render_md(items, i, title)
        path = os.path.join(OUTDIR, "ch%02d-%s.md" % (i, slug))
        if os.path.exists(path) and "--force" not in sys.argv:
            old = io.open(path, encoding="utf-8").read()
            if old != md:
                print("ch%02d %-16s SKIP（.md 有手改，未覆蓋；要整章重切請加 --force）" % (i, slug))
                continue
        io.open(path, "w", encoding="utf-8", newline="\n").write(md)
        heads = len(re.findall(r"^#{2,4} ", md, re.M))
        fences = md.count("```") // 2
        print("ch%02d %-16s p.%3d-%3d  %5d 行  %3d 節  %3d 段程式碼"
              % (i, slug, p1, p2, md.count("\n"), heads, fences))
        total += 1
    print("共 %d 章 → %s" % (total, OUTDIR))


if __name__ == "__main__":
    main()
