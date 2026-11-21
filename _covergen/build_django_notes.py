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
import ast
import sys
import warnings

warnings.filterwarnings("ignore")  # ast.parse 筆記片段時會有 "\s" 之類 SyntaxWarning

sys.path.insert(0, r"C:\Users\princ\OneDrive\Documents")
import clean_ocr_notes as c  # noqa: E402
import svg_django_figs as figs  # noqa: E402

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

# 第二輪（2026-11）：settings 範例與 Git 指令，讓範例貼上就能跑
SAMPLE_FIXES = [
    # BASE_DIR 用了 3 次卻沒有定義 → 補上 startproject 的寫法
    (
        "# settings.py\n# 基本設置\n",
        "# settings.py\nfrom pathlib import Path\n\n"
        "# 專案根目錄（Django 2.0 起用 pathlib，3.2+ 的 startproject 就是這樣產生）\n"
        "BASE_DIR = Path(__file__).resolve().parent.parent\n\n# 基本設置\n",
    ),
    # git stash save：Git 2.16 起建議 push -m
    ('git stash save "描述信息"', 'git stash push -m "描述信息"'),
]

# STATIC_URL 範例缺結尾引號（SyntaxError）；該行後面就是收尾的 fence，可精準定位
STATIC_BLOCK_RE = re.compile(r"STATIC_URL = '/static/\n```")
STATIC_BLOCK_FIX = (
    "STATIC_URL = '/static/'\n"
    "# 預設主鍵型別（Django 3.2 起 startproject 會產生；未設定時 migrate 會出現 W042 警告）\n"
    "DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'\n"
    "```"
)


# ---------------- OCR 結構修復：合併被切碎的 fence、重建遺失的縮排 ----------------
FENCE = "```"
PAIRS = {"(": ")", "[": "]", "{": "}"}
PY_HINT = re.compile(r"^\s*(import|from|def|class|print|if|for|while|try|with|return)\b|"
                     r"models\.|=\s*models\.|\bprint\(", re.M)


def _balanced(code):
    depth, quote = 0, None
    for ch in code:
        if quote:
            if ch == quote:
                quote = None
            continue
        if ch in "'\"":
            quote = ch
        elif ch in PAIRS:
            depth += 1
        elif ch in PAIRS.values():
            depth -= 1
    return depth


def _parses(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def _reindent(code):
    """OCR 丟掉縮排 → 依結尾的 `:` 重建；只有 ast.parse 過才採用（4 空格優先，其次 2）。"""
    for width in (4, 2):
        out, level = [], 0
        prev_ends_colon = False
        for line in code.splitlines():
            s = line.strip()
            if not s:
                out.append("")
                continue
            if re.match(r"^(def|class|import|from)\b", s) and not prev_ends_colon:
                level = 0  # 片段裡新開的定義／import 回到頂層（但 class 內的方法不算）
            elif re.match(r"^(else|elif|except|finally|case)\b", s):
                level = max(level - 1, 0)
            out.append(" " * (width * level) + s)
            prev_ends_colon = s.endswith(":")
            if prev_ends_colon:
                level += 1
        cand = "\n".join(out)
        if cand != code and _parses(cand):
            return cand
        # 片段被截斷（最後一行是註解、後面應還有 body）→ 補 pass，讓它至少語法合法
        if not _parses(cand):
            last = next((ln for ln in reversed(cand.splitlines()) if ln.strip()), "")
            indent = " " * (len(last) - len(last.lstrip()))
            cand2 = cand + "\n" + indent + "pass  # 內容省略"
            if _parses(cand2):
                return cand2
    return code


def _merge_split_fences(lines):
    """把被 OCR 切成兩段的 fence 接回去：
    ① 前段括號不平衡、後段就在旁邊 → 合併
    ② 後段以 else: / elif / except / finally / } ] ) 開頭 → 是同一段程式的續尾，合併（中間說明文字搬到區塊前）
    """
    CONTINUATION = re.compile(r"^(else\s*:|elif\b|except\b|finally\s*:|\}|\]|\))")

    blocks, cur, start = [], None, 0
    for i, line in enumerate(lines):
        if line.startswith(FENCE):
            if cur is None:
                cur, start = [], i
            else:
                blocks.append((start, i, "\n".join(cur)))
                cur = None
        elif cur is not None:
            cur.append(line)

    merged, drop_ranges = {}, []
    for idx, (a, b, code) in enumerate(blocks[:-1]):
        nxt = blocks[idx + 1]
        nxt_code = nxt[2].strip()
        if not code.strip() or not nxt_code:
            continue
        gap = [g for g in lines[b + 1:nxt[0]] if g.strip()]
        if len(gap) > 3:
            continue
        continuation = bool(CONTINUATION.match(nxt_code.splitlines()[0]))
        if not continuation and _balanced(code.strip()) == 0:
            continue
        prose, joiner = [], ""
        if gap:
            g = gap[0].strip()
            is_prose = not re.search(r"[(){}\[\],=]", g) or re.search(r"[。：]$", g)
            if continuation and is_prose:
                prose = list(gap)         # 說明文字搬到合併後的區塊前
            elif not is_prose and len(gap) == 1:
                joiner = g                # 本來就是程式碼的一行
            elif not continuation:
                continue
            else:
                prose = list(gap)
        body = code.rstrip() + ("\n" + joiner if joiner else "") + "\n" + nxt_code
        merged[a] = (prose, body)
        drop_ranges.append((nxt[0], nxt[1]))       # 下一段（含內容）併入前段 → 整段移除
        drop_ranges.append((b + 1, nxt[0] - 1))    # 中間那行（已被當成程式碼或搬到前面）也不能留

    end_of = {a: b for a, b, _ in blocks}
    out, i = [], 0
    while i < len(lines):
        if i in merged:
            prose, body = merged[i]
            if prose:
                out.extend(prose)
                out.append("")
            out.extend([FENCE, body, FENCE])
            i = end_of[i] + 1
            continue
        if any(lo <= i <= hi for lo, hi in drop_ranges):
            i += 1
            continue
        out.append(lines[i])
        i += 1
    return out

# 第三批：OCR 吃掉字元的明確修正（不動「故意示範錯誤」的段落，例如 while True print(...)）
BLOCK_FIXES = [
    ("def hi:\nprint('hi') //縮進了", "def hi():\nprint('hi')  # 縮進"),
    ("s = 'Yes, he doesn't'", "s = 'Yes, he doesn\\'t'"),
    ("list=\nit = iter(list)", "list = [1, 2, 3, 4]\nit = iter(list)"),
    ("list=\nit = iter(list) # 創建迭代器對象", "list = [1, 2, 3, 4]\nit = iter(list)  # 創建迭代器對象"),
    ('thisset = set("s", "ss", "sss"))', 'thisset = set(("s", "ss", "sss"))'),
    ("print('str+'ing', 'my'*3)", "print('str' + 'ing', 'my'*3)"),
    ("{ % load humanize % }", "{% load humanize %}"),
    ("import module1[,module2[, ... moduleN]", "import module1, module2, module3"),
    ("from modname import name1[, name2[, ... nameN]", "from modname import name1, name2, name3"),
    ("class ClassName;", "class ClassName:"),
    # OCR 把括號搬了位
    ("print(type(A)) == A)", "print(type(A) == A)"),
    ("print(type(B)) == A)", "print(type(B) == A)"),
    # 區塊裡混進了執行結果（不是程式碼）
    ("<class 'int'> <class 'float'> <class 'bool'> <class 'complex'>",
     "# <class 'int'> <class 'float'> <class 'bool'> <class 'complex'>"),
    # 類別骨架的佔位符改成註解，才能當程式碼看
    ("<statement-1>", "# <statement-1>"),
    ("<statement-N>", "# <statement-N>"),
    # 只有 class 宣告、body 被 OCR 吃掉
    ("class MyClass:\n```", "class MyClass:\npass  # 類別主體（其餘省略）\n```"),
    # 自訂命令範例少了 body
    ("def handle(self, *args, **kwargs):\n```",
     "def handle(self, *args, **kwargs):\nself.stdout.write('Hello from my command')\n```"),
    # Django 4.0 已移除 request.is_ajax() → 改用標頭判斷
    ("if request.is/ajax():",
     "if request.headers.get('x-requested-with') == 'XMLHttpRequest':"),
    # match/case 的分層不是「遇到 : 就縮進」，手寫正確版本
    ('def http_error(status):\nmatch status:\ncase 400:\nreturn "Bad request"\ncase 404:\nreturn "Not found"\ncase 418:\nreturn "I\'m a teapot"\ncase _:\nreturn "Something\'s wrong with the Internet"',
     "def http_error(status):\n    match status:\n        case 400:\n            return \"Bad request\"\n"
     "        case 404:\n            return \"Not found\"\n        case 418:\n            return \"I'm a teapot\"\n"
     "        case _:\n            return \"Something's wrong with the Internet\""),
    # f-string 括號放錯位置
    ("return f{'value // 100000000}億'", "return f'{value // 100000000}億'"),
    # 參數用點號
    ("def event_delete(request.id):", "def event_delete(request, id):"),
]

ORPHAN_TAGS = (("</p>", "<p>"), ("</td>", "<td"), ("</tr>", "<tr>"), ("</table>", "<table"))

# 三處「程式碼被說明文字切散＋片段重複」的區段，直接改寫成完整片段（前後說明文字保留）
REGION_REWRITES = [
    (
        "```\n# myapp/views.py\nfrom django.shortcuts import render\ndef index(request):\ncontext = {",
        "在這裡，我們將上下文數據傳遞給 index.html 模板",
        "```\n# myapp/views.py\nfrom django.shortcuts import render\n\n\n"
        "def index(request):\n    context = {\n        'title': '我的首頁',\n"
        "        'welcome_message': '歡迎來到我的網站！',\n        'site_name': '我的網站',\n"
        "        'num_posts': 42,\n    }\n    return render(request, 'index.html', context)\n```\n\n",
    ),
    (
        "```\n# myapp/template tags/custom_humanize.py",
        "這個自定義過濾器會將數字轉換為中文單位",
        "```\n# myapp/templatetags/custom_humanize.py\nfrom django import template\n\n"
        "register = template.Library()\n\n\n@register.filter\ndef chinese_number(value):\n"
        "    try:\n        value = int(value)\n    except (ValueError, TypeError):\n        return value\n"
        "    if 10000 <= value < 100000000:\n        return f'{value // 10000}萬'\n"
        "    elif value >= 100000000:\n        return f'{value // 100000000}億'\n    return str(value)\n```\n\n",
    ),
    (
        "#### 14.2.1 使用 messages 在視圖中設置消息",
        "在這個例子中，我們在表單提交成功後使用了 messages.success",
        "#### 14.2.1 使用 messages 在視圖中設置消息\n\n"
        "以下是如何在 Django 視圖中使用消息系統的範例。假設我們有一個註冊用戶的視圖，"
        "註冊成功後，我們想顯示一個成功消息。\n\n"
        "```\n# accounts/views.py\nfrom django.shortcuts import render, redirect\n"
        "from django.contrib.auth.forms import UserCreationForm\nfrom django.contrib import messages\n\n\n"
        "def register(request):\n    if request.method == 'POST':\n"
        "        form = UserCreationForm(request.POST)\n        if form.is_valid():\n            form.save()\n"
        "            messages.success(request, '註冊成功！歡迎使用本網站。')\n"
        "            return redirect('login')  # 註冊成功後跳轉到登錄頁面\n        else:\n"
        "            messages.error(request, '註冊失敗，請檢查表單內容。')\n    else:\n"
        "        form = UserCreationForm()\n"
        "    return render(request, 'accounts/register.html', {'form': form})\n```\n\n",
    ),
    (
        "#### 15.6.1 報名邏輯",
        "15.7. 美化前端：使用 Bootstrap",
        "#### 15.6.1 報名邏輯\n\n在 views.py 中添加報名功能：\n\n"
        "```\nfrom .models import Registration\n\n\n"
        "def event_register(request, id):\n    event = get_object_or_404(Event, id=id)\n"
        "    if Registration.objects.filter(event=event, user=request.user).exists():\n"
        "        messages.error(request, '你已經報名過此活動。')\n"
        "    elif event.registrations.count() >= event.max_attendees:\n"
        "        messages.error(request, '報名已滿。')\n    else:\n"
        "        Registration.objects.create(event=event, user=request.user)\n"
        "        messages.success(request, '成功報名活動！')\n"
        "    return redirect('event_detail', id=event.id)\n```\n\n",
    ),
]


def _apply_region_rewrites(text):
    applied = 0
    for start, end, new in REGION_REWRITES:
        i = text.find(start)
        if i < 0:
            continue
        j = text.find(end, i)
        if j < 0:
            continue
        text = text[:i] + new + text[j:]
        applied += 1
    return text, applied


def _strip_orphan_closers(code):
    """只有收尾標籤、沒有對應開頭的 HTML 碎片 → 移除（配對正常的保留）。"""
    for close, open_ in ORPHAN_TAGS:
        excess = code.count(close) - code.count(open_)
        while excess > 0:
            m = re.search(r"(?m)^\s*" + re.escape(close) + r"\s*\n", code) or \
                re.search(r"[ \t]*" + re.escape(close), code)
            if not m:
                break
            code = code[:m.start()] + code[m.end():]
            excess -= 1
    return code




def _rows_to_md(body):
    """把 OCR 拍平的 HTML 表格（…</td>…</tr>）轉成 markdown 表格。"""
    s = re.sub(r"</?(table|thead|tbody|tfoot)[^>]*>", "", body)
    rows = []
    for chunk in re.split(r"</?tr[^>]*>", s):
        cells = [c.strip() for c in re.split(r"</?t[dh][^>]*>", chunk)]
        cells = [c for c in cells if c]
        if cells:
            rows.append("| " + " | ".join(cells) + " |")
    if rows:
        n = rows[0].count("|") - 1
        rows.insert(1, "|" + " --- |" * n)
    return rows


def _dumps_to_tables(text):
    """① 含多個 </td> 的程式碼區塊 → markdown 表格
    ② 內容含 markdown 標題（OCR fence 配對錯位、把整段說明吞進去）→ 拆掉 fence，逐行把表格殘骸轉掉
    """
    out, cur, in_code = [], None, False
    for line in text.splitlines():
        if line.startswith(FENCE):
            if in_code:
                body = "\n".join(cur)
                mis_fenced = False  # 拆 fence 風險太高（會把程式碼行放生到 fence 外），只做表格轉換
                table_dump = (body.count("</td>") >= 3
                              and not PY_HINT.search(body)
                              and not re.search(r"^\s*(git|pip|python|curl|wget|docker|kubectl)", body, re.M))
                if table_dump or mis_fenced:
                    for ln in cur:
                        if "</td>" in ln:
                            out.extend(_rows_to_md(ln))
                        else:
                            out.append(ln)
                else:
                    out.extend([FENCE] + cur + [FENCE])
                cur, in_code = None, False
            else:
                cur, in_code = [], True
            continue
        if in_code:
            cur.append(line)
        else:
            out.append(line)
    if in_code and cur:
        body = "\n".join(cur)
        mis_fenced = False
        if body.count("</td>") >= 3:
            for ln in cur:
                if "</td>" in ln:
                    out.extend(_rows_to_md(ln))
                else:
                    out.append(ln)
        else:
            out.extend([FENCE] + cur + [FENCE])
    # ③ 剩下的裸行（已不在 fence 內）：含 2 個以上 </td> 的 OCR 表格殘骸 → markdown 表格
    fixed = []
    for ln in "\n".join(out).splitlines():
        if ln.count("</td>") >= 2:
            fixed.append("")
            fixed.extend(_rows_to_md(ln))
            fixed.append("")
        else:
            fixed.append(ln)
    return "\n".join(fixed)


def _insert_figures(text, no):
    """把本章對應的 SVG 圖插在指定標題之後。"""
    for ch, anchor, svg in figs.FIGURES:
        if ch != no:
            continue
        i = text.find(anchor)
        if i < 0:
            continue
        end = text.find("\n", i)
        text = text[:end + 1] + "\n" + svg + "\n" + text[end + 1:]
    return text


JUNK_LINE = re.compile(r"^(20\d\d[/-]\d{1,2}[/-]\d{1,2}|[\w\u4e00-\u9fff.-]+\.(md|pptx|pdf|key))$")
JUNK_TOKEN = re.compile(
    r"[（(]\s*(在\s*)?index\d*\.py\s*[）)]"
    r"|在\s*index\d*\.py\s*[（(]用\s*python\s*index\d*\.py\s*開啟[）)]"
    r"|[（(]用\s*python\s*index\d*\.py\s*開啟[）)]"
)


def _strip_ocr_junk(text):
    """去掉簡報頁尾殘留：單獨一行的日期／來源檔名（程式碼區塊內也刪），以及 (index.py) 這類標記。"""
    out, in_code = [], False
    for line in text.splitlines():
        if line.startswith(FENCE):
            in_code = not in_code
            out.append(line)
            continue
        if JUNK_LINE.match(line.strip()):
            continue  # 整行只有日期或檔名 → 一定是頁尾殘留，程式碼區塊內也一樣
        if in_code:
            out.append(line)
        else:
            cleaned = JUNK_TOKEN.sub("", line).rstrip()
            if cleaned.strip():
                out.append(cleaned)
    # 清空後留下來的空程式碼區塊一起收掉
    fixed, i = [], 0
    while i < len(out):
        if out[i].startswith(FENCE):
            if i + 1 < len(out) and out[i + 1].startswith(FENCE):
                i += 2
                continue
            if i + 2 < len(out) and not out[i + 1].strip() and out[i + 2].startswith(FENCE):
                i += 3
                continue
        fixed.append(out[i])
        i += 1
    return "\n".join(fixed) + "\n"


def _fix_placeholders(code):
    """教材骨架的佔位行（單一個 . 或 <statement-N>）→ 註解；只有宣告沒有 body → 補 pass。"""
    lines = [("# ." if ln.strip() == "." else ln) for ln in code.splitlines()]
    code = "\n".join(lines)
    if not PY_HINT.search(code) or _parses(code):
        return code
    if code.rstrip().endswith(":"):
        return code.rstrip() + "\n    pass  # 內容省略"
    # body 全是註解（經典 class 骨架）→ Python 不接受，補一個 pass
    ls = code.splitlines()
    head = next((i for i, ln in enumerate(ls) if re.match(r"^(class|def)\b.*:\s*$", ln.strip())), None)
    if head is not None and all((not ln.strip()) or ln.strip().startswith("#") for ln in ls[head + 1:]):
        return code.rstrip() + "\n    pass  # 內容省略"
    return code


def _reindent_pass(lines):
    out, cur = [], None
    for line in lines:
        if line.startswith(FENCE):
            if cur is None:
                cur = []
                out.append(line)
            else:
                code = _strip_orphan_closers("\n".join(cur))
                for old, new in BLOCK_FIXES:
                    code = code.replace(old, new)
                code = _fix_placeholders(code)
                if PY_HINT.search(code) and not _parses(code):
                    code = _reindent(code)
                out.extend(code.splitlines())
                out.append(line)
                cur = None
        elif cur is not None:
            cur.append(line)
        else:
            out.append(line)
    if cur is not None:
        out.extend(cur)
    return out


def repair_code_blocks(text):
    lines = _merge_split_fences(text.splitlines())
    return "\n".join(_reindent_pass(lines))



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
    text = repair_code_blocks(text)  # 先修結構（合併被切碎的 fence、重建縮排），再做文字替換
    text = _strip_ocr_junk(text)     # 去掉頁尾日期／來源檔名／(index.py) 標記
    text = _insert_figures(text, no)  # 手繪 SVG 圖（MVT／模型關聯／Git Flow）
    text = _dumps_to_tables(text)    # OCR 拍平的 HTML 表格 → markdown 表格
    text, _n = _apply_region_rewrites(text)
    for old, new in FORBIDDEN + CONTENT_FIXES:
        text = text.replace(old, new)
    # A：套用總稿（clean_ocr_notes.py）已驗證的版本修正表（Django 5.2 LTS、Python 3.14、from django.* …）
    for old, new in c.VERSION_UPDATES:
        text = text.replace(old, new)
    # B/C：前端與 Actions 版本、教材年份註記
    for old, new in ERA_FIXES:
        text = text.replace(old, new)
    # 第二輪：settings 範例可執行性 + Git 指令語法
    for old, new in SAMPLE_FIXES:
        text = text.replace(old, new)
    text = STATIC_BLOCK_RE.sub(STATIC_BLOCK_FIX, text)
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
