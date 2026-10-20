# -*- coding: utf-8 -*-
"""python-problem-solving-toolkit（_posts 文章）：3 張內嵌 SVG 圖表。

  圖 1  pytoolkit-complement-vs-alternative  「互補（加法）」vs「二選一（減法）」
  圖 2  pytoolkit-domain-map                 11 個工作領域 × 24 列痛點
  圖 3  pytoolkit-choose-flow                選型五問決策流程

這篇是 source/_posts/ 的一般文章（沒有 index.html 孿生檔），所以嵌入步驟用同目錄的
embed_pytoolkit.py，而不是 tools/diagrams/embed_figs.py（後者只吃 source/<note>/ 筆記）。

House style 一律走 svglib.py（顏色不要寫死）；標籤一律真正的 <text>，方便 QA 量測。
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from svglib import Svg, C, MUT, TXT, CARD, CARD2  # noqa: E402

HERE = _HERE
RAIL = "#7d8590"


def fig_relation(s):
    """圖 1：互補（加法）vs 二選一（減法）。"""
    # ---- 左：互補 ----
    s.rect(48, 106, 440, 400, fill=CARD2, stroke=C["teal"] + "66", rx=14)
    s.text(76, 148, "互補（加法）：兩個一起用更強", 17, TXT, "700")
    s.text(76, 176, "同一條管線的前後兩段，各管一件事", 12.5, MUT)
    s.card(76, 204, 176, 64, "pandas", "表格清理與分析", "teal")
    s.card(284, 204, 176, 64, "openpyxl", "只在 .xlsx 必要", "blue")
    s.line(164, 268, 164, 312, RAIL)
    s.line(372, 268, 372, 312, RAIL)
    s.line(164, 312, 372, 312, RAIL)
    s.arrow(268, 312, 268, 340, RAIL)
    s.box(148, 342, 240, 60, "乾淨的 DataFrame", ".xlsx 也讀得進去", "teal")
    s.text(76, 444, "少一個就會壞：缺 openpyxl 時", 12.5, MUT)
    s.text(76, 466, "pandas.read_excel() 直接丟例外。", 12.5, MUT)
    s.text(76, 492, "判準：會同時出現在同一條管線。", 12.5, C["teal"])

    # ---- 右：二選一 ----
    s.rect(512, 106, 440, 400, fill=CARD2, stroke=C["amber"] + "66", rx=14)
    s.text(540, 148, "二選一（減法）：挑一個學到會", 17, TXT, "700")
    s.text(540, 176, "兩條路回答的是同一個問題", 12.5, MUT)
    s.box(540, 200, 384, 50, "要做網站／提供 API", None, "amber")
    s.line(732, 250, 732, 274, RAIL)
    s.line(628, 274, 836, 274, RAIL)
    s.arrow(628, 274, 628, 298, RAIL)
    s.arrow(836, 274, 836, 298, RAIL)
    s.card(540, 300, 176, 64, "Flask", "微框架、原型", "teal")
    s.card(748, 300, 176, 64, "Django", "全端、admin", "violet")
    s.line(628, 364, 628, 386, RAIL)
    s.line(836, 364, 836, 386, RAIL)
    s.line(628, 386, 836, 386, RAIL)
    s.arrow(732, 386, 732, 404, RAIL)
    s.box(540, 406, 384, 56, "同一個終點：HTTP 服務", "所以它們是替代關係", "amber")
    s.text(540, 500, "兩條路都到得了，同時精通成本高。", 12.5, MUT)

    # ---- 圖下註腳 ----
    s.text(48, 546, "互補：pandas＋NumPy、Matplotlib＋Seaborn、pytest＋unittest", 13, MUT)
    s.text(48, 572, "二選一：Flask／Django、TensorFlow／PyTorch、venv／conda、Airflow／Prefect",
           13, MUT)


DOMAINS = [
    ("資料整理與分析", "清資料、分析資料",
     ["pandas · NumPy · openpyxl"], "teal"),
    ("視覺化與儀表板", "視覺化、做儀表板",
     ["Matplotlib · Seaborn · Plotly", "Streamlit"], "blue"),
    ("Web 與 API", "做網站、做 API",
     ["Flask／Django · FastAPI", "Django REST Framework"], "violet"),
    ("自動化與爬蟲", "自動化任務、爬網站",
     ["schedule · Selenium", "BeautifulSoup · Scrapy"], "amber"),
    ("文件、影像與文字", "PDF、影像、文字",
     ["pypdf · pdfplumber · OpenCV", "Pillow · NLTK · spaCy"], "rose"),
    ("機器學習、深度學習與時序", "建 ML／DL 模型、時序",
     ["scikit-learn · XGBoost · PyTorch", "TensorFlow／Keras · Prophet"], "green"),
    ("大數據與工作流", "處理大資料、跑資料管線",
     ["Dask · PySpark · Airflow／Prefect"], "blue"),
    ("資料庫", "接資料庫",
     ["sqlite3（標準庫）· SQLAlchemy"], "teal"),
    ("GUI", "做 GUI",
     ["Tkinter（標準庫）· PyQt"], "violet"),
    ("工程化：測試、環境、部署、排程", "測試、環境、排程、部署",
     ["pytest · venv／conda · Docker", "Render · cron／Task Scheduler"], "amber"),
    ("AI 與 Notebook", "建 AI 應用、做 Notebook",
     ["LangChain · OpenAI · Jupyter／Colab"], "rose"),
]
CARD_W, CARD_H = 280, 116
XS = [48, 360, 672]
YS = [186, 326, 466, 606]


def _domain_card(s, x, y, num, name, question, kit, stage):
    s.rect(x, y, CARD_W, CARD_H, fill=CARD, stroke=C[stage] + "66", rx=12)
    s.badge(x + 28, y + 28, num, C[stage], r=15, size=13)
    s.text(x + 54, y + 33, name, 14, TXT, "700")
    s.text(x + 16, y + 58, question, 12, MUT)
    for i, ln in enumerate(kit):
        s.text(x + 16, y + 82 + i * 22, ln, 11.5, C[stage])


def fig_domains(s):
    """圖 2：11 個工作領域 × 24 列痛點（原圖的目錄）。"""
    s.rect(48, 106, 904, 52, fill="#0d1117", stroke="#30363d", rx=10)
    s.text(500, 138, "24 列痛點 → 11 個工作領域：這就是原圖的目錄", 14, TXT, "700", "middle")

    for i, (name, q, kit, stage) in enumerate(DOMAINS):
        _domain_card(s, XS[i % 3], YS[i // 3], str(i + 1), name, q, kit, stage)

    # 第 12 格：全文重點（5 處修正）——順便把 3×4 的格子填滿
    _domain_card(s, XS[2], YS[3], "!", "5 處要修正", "PyPDF2 停更、SQLAlchemy 層級、",
                 ["schedule 誤用、Flask／Django、", "cron 不是 Python 套件"], "rose")

    s.text(48, 758, "從清資料（1）到部署與測試（10），這 11 個領域就是一條專案生命週期；", 13, MUT)
    s.text(48, 784, "圖上「A + B」的組合，有的是互補、有的是二選一（見圖 1 的判準）。", 13, MUT)


QUESTIONS = [
    ("Q1", "資料放得進記憶體嗎？", "規模決定工具，不是喜好", [
        "放得進（GB 級）：pandas ＋ NumPy",
        "放不進、單機多核：Dask",
        "已有 Spark 叢集（TB 級）：PySpark"]),
    ("Q2", "幾個人同時寫入？", "併發決定資料庫", [
        "只有你、原型或測試：sqlite3（標準庫）",
        "多人、正式環境：PostgreSQL ＋ SQLAlchemy"]),
    ("Q3", "圖要給誰看？", "產出形式決定繪圖層", [
        "出版級靜態圖：Matplotlib ＋ Seaborn",
        "要 hover／zoom：Plotly",
        "整個互動儀表板：Streamlit"]),
    ("Q4", "團隊已經有 Django 嗎？", "⚠️ Flask／Django 二選一，不是相加", [
        "新專案、要 API：FastAPI",
        "已有 Django 專案：Django ＋ DRF"]),
    ("Q5", "程式跑在哪裡？", "打包與託管是兩件事", [
        "要環境一致、自己管：Docker",
        "要一鍵上線、不維運：Render"]),
]
Q_X, Q_W, Q_H = 48, 384, 84
A_X, A_W, A_H, A_GAP = 560, 392, 40, 10
RAIL_X, ROW0, PITCH = 496, 190, 164


def fig_choose(s):
    """圖 3：選型五問決策流程（每列：一個問題 → 匯流排 → 落點卡）。"""
    s.rect(48, 106, 904, 52, fill="#0d1117", stroke="#30363d", rx=10)
    s.text(500, 138, "先問情境（Q1–Q2），再問產出與團隊（Q3–Q5）", 14, TXT, "700", "middle")

    for i, (num, q, detail, answers) in enumerate(QUESTIONS):
        y = ROW0 + i * PITCH
        s.card(Q_X, y, Q_W, Q_H, q, detail, "teal", num=num)

        total = len(answers) * A_H + (len(answers) - 1) * A_GAP
        top = y + Q_H / 2.0 - total / 2.0
        c0 = top + A_H / 2.0
        c1 = top + (len(answers) - 1) * (A_H + A_GAP) + A_H / 2.0

        s.line(Q_X + Q_W, y + Q_H / 2.0, RAIL_X, y + Q_H / 2.0, RAIL)
        if c1 > c0:
            s.line(RAIL_X, c0, RAIL_X, c1, RAIL)
        for j, ans in enumerate(answers):
            ty = top + j * (A_H + A_GAP)
            cy = ty + A_H / 2.0
            s.rect(A_X, ty, A_W, A_H, fill=CARD, stroke=C["blue"] + "66", rx=10)
            s.text(A_X + 16, cy + 4.5, ans, 12.5, TXT)
            s.arrow(RAIL_X, cy, A_X - 2, cy, RAIL)

    s.text(48, 1006, "右邊若是兩條路，先確認是「互補」還是「二選一」——⚠️ 那幾組只能挑一個。",
           13, MUT)
    s.text(48, 1032, "同一組問題換個情境就會換答案：先問清楚卡在哪裡，再打開套件清單。", 13, MUT)


FIGS = [
    ("pytoolkit-complement-vs-alternative", 1000, 600,
     "互補與二選一：兩種關係", "同類套件怎麼選的第一步", fig_relation,
     "圖 1：互補（加法）vs 二選一（減法）——左邊兩個一起用會更強，"
     "右邊兩個只回答同一個問題。｜手繪 SVG 圖表"),
    ("pytoolkit-domain-map", 1000, 800,
     "11 個工作領域地圖", "24 列痛點 → 11 個工作領域", fig_domains,
     "圖 2：11 個工作領域 × 24 列痛點——這 12 張卡就是原圖的目錄，"
     "也是一條從清資料到部署的專案生命週期。｜手繪 SVG 圖表"),
    ("pytoolkit-choose-flow", 1000, 1060,
     "選型五問決策流程", "先問規模與情境，再挑工具", fig_choose,
     "圖 3：選型五問——先問規模與併發（Q1／Q2），再問產出與團隊（Q3–Q5），"
     "右邊就是落點；⚠️ 那幾組是二選一，不是相加。｜手繪 SVG 圖表"),
]


def build(slug):
    """回傳指定 slug 的 Svg 物件（embed_pytoolkit.py 也用它產生 figure 區塊）。"""
    for s_slug, w, h, aria, sub, fn, _cap in FIGS:
        if s_slug == slug:
            s = Svg(w, h, aria, aria, sub)
            fn(s)
            return s
    raise SystemExit("unknown slug: %s" % slug)


def main():
    for slug, w, h, aria, sub, fn, _cap in FIGS:
        s = build(slug)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-40s %dx%d  %s"
              % (slug + ".svg", w, h, "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))


if __name__ == "__main__":
    main()
