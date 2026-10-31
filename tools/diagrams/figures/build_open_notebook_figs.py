# -*- coding: utf-8 -*-
"""產生 Open Notebook 實測文的兩張內嵌圖，並就地注入文章（冪等）。

沿用 tools/diagrams/svglib.py 的 house style：深色圖卡 #0d1117、teal/amber/
violet 配色、JhengHei 字型，跟站上其他圖表同一套。

重跑即更新：文章裡以 <!-- FIG1 --> … <!-- /FIG1 --> 包住，替換不會重複插入。

    python tools/diagrams/figures/build_open_notebook_figs.py
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools", "diagrams"))
sys.stdout.reconfigure(encoding="utf-8")

from svglib import Svg, C, MUT, TXT  # noqa: E402

POST = os.path.join(
    REPO, "source", "_posts", "open-notebook-selfhost-4090-what-it-is.md"
)


def build_arch():
    """四個程序的呼叫方向。"""
    s = Svg(
        980,
        650,
        "Open Notebook 的四個程序與呼叫方向：瀏覽器經 Next.js 前端打到 FastAPI，"
        "後端把長工作丟進 SurrealDB 的 command 佇列，由背景 worker 取走；"
        "資料與向量都存在 SurrealDB，聊天歷史存在 SQLite，模型走 Ollama",
        "四個程序的實際呼叫方向",
        "實線＝同步呼叫；佇列是 SurrealDB 裡的一張表，不是獨立的訊息中介",
    )

    s.box(380, 112, 220, 50, "瀏覽器", None, "blue")
    s.arrow(490, 162, 490, 188)

    s.box(330, 190, 320, 64, "Next.js 前端",
          "開發 :3000 ／ 映像 :8502 · 代理 /api/*", "teal")
    s.arrow(490, 254, 490, 290)
    s.text(500, 278, "HTTP + SSE", 11.5, MUT)

    s.box(330, 292, 320, 64, "FastAPI 後端 :5055",
          "chat / ask 同步處理，長工作往外送", "teal")

    s.box(48, 292, 230, 64, "SQLite checkpoint", "聊天歷史存在這裡", "gray")
    s.arrow(328, 324, 282, 324, "#7d8590")
    s.text(305, 314, "存檔", 11, MUT, anchor="middle")

    s.box(730, 292, 200, 64, "Ollama :11434", "8B 聊天 + bge-m3", "green")
    s.arrow(652, 324, 726, 324, C["green"])
    s.text(689, 314, "模型呼叫", 11, MUT, anchor="middle")

    s.box(390, 388, 200, 44, "command 佇列", None, "amber", tsize=13.5)
    s.arrow(420, 358, 420, 386, C["amber"])
    s.text(428, 371, "submit", 11, MUT)

    s.box(730, 388, 200, 64, "背景 worker", "8 個 command", "amber")
    s.line(590, 410, 690, 410, C["amber"])
    s.arrow(690, 410, 726, 410, C["amber"])
    s.text(640, 400, "pick up", 11, MUT, anchor="middle")

    s.box(
        48, 486, 882, 84,
        "SurrealDB 2.x :8000",
        "notebook · source · source_embedding · note · chat_session ｜ "
        "圖邊 reference / artifact / refers_to ｜ "
        "fn::text_search（BM25）· fn::vector_search",
        "violet", tsize=16.5, dsize=11.5,
    )
    s.arrow(360, 358, 360, 484, C["violet"])
    s.arrow(830, 454, 830, 484, C["violet"])
    s.line(490, 434, 490, 484, C["violet"], 1.5)
    s.text(500, 470, "工作也存在 DB", 11, MUT)

    s.legend(
        [("teal", "前端 / 後端"), ("amber", "背景工作"),
         ("violet", "資料庫"), ("green", "模型推論")],
        y=616, x=70, step=210,
    )
    return s


def build_metrics():
    """耗時與 VRAM 預算。"""
    s = Svg(
        980,
        430,
        "實測數據：首次資料庫遷移 180 秒、內容抽取 16.5 秒、106 個 chunk 向量化 42.5 秒；"
        "27B 模型加 32k context 佔用 23,508 MiB，只剩約 1,056 MiB 給 KV cache",
        "實測數據：耗時與 VRAM 預算",
        "同一台機器（RTX 4090 24 GB）、同一份 92 頁簡報；時間為秒，記憶體為 MiB",
    )

    s.text(48, 128, "① 處理耗時", 16, TXT, "700")
    scale_s = 300.0 / 180.0
    rows = [
        ("首次資料庫遷移（25 個 migration）", 180, "180 s", "amber"),
        ("向量化 106 個 chunk（bge-m3）", 42.5, "42.5 s", "teal"),
        ("內容抽取 + 存檔", 16.5, "16.5 s", "blue"),
    ]
    y = 166
    for label, val, shown, stage in rows:
        s.text(48, y, label, 12.5, MUT)
        s.rect(48, y + 8, 300, 15, fill="#1c2230", stroke="#222b36", rx=4)
        s.rect(48, y + 8, max(6, val * scale_s), 15,
               fill=C[stage], stroke=C[stage], rx=4)
        s.text(356, y + 20, shown, 12.5, TXT, "700")
        y += 62

    s.text(48, 372, "程式碼端量到的，不含模型載入時間。", 11.5, MUT)

    s.text(520, 128, "② VRAM 佔用（總量 24,564 MiB）", 16, TXT, "700")
    scale_m = 350.0 / 24564.0
    vrows = [
        ("27B + 32k context", 23508, "23,508 MiB", "rose"),
        ("8B + bge-m3", 7500, "7,500 MiB", "green"),
    ]
    y = 176
    for label, val, shown, stage in vrows:
        s.text(520, y, label, 12.5, MUT)
        s.rect(520, y + 8, 350, 17, fill="#1c2230", stroke="#222b36", rx=4)
        s.rect(520, y + 8, max(6, val * scale_m), 17,
               fill=C[stage], stroke=C[stage], rx=4)
        s.text(878, y + 21, shown, 12.5, TXT, "700")
        y += 70

    s.rect(520, 300, 350, 66, fill="#1c2230", stroke=C["rose"] + "66", rx=8)
    s.text(536, 324, "27B 只剩 1,056 MiB 給 KV cache", 13, TXT, "700")
    s.text(536, 348, "→ 7 分鐘 0 token；8B 才是可用組合", 12.5, MUT)

    return s


def build_taxonomy():
    """6 類 20 種提示技術（8B 的答案，名稱已回查原始檔）。"""
    s = Svg(
        980,
        620,
        "從 92 頁簡報歸納出的六類提示技術：基礎技巧 2 種、情境與角色 4 種、"
        "推理與規劃 4 種、高階整合 4 種、風格與語氣 2 種、專門化 4 種，共 20 種",
        "從 92 頁簡報歸納出的 6 類 20 種提示技術",
        "8B 模型的答案；名稱回查結果：16 個完整命中、4 個為模型改寫的標籤",
    )

    cats = [
        ("1", "基礎技巧", "teal", ["Zero-Shot", "Few-Shot"]),
        ("2", "情境與角色", "blue", ["System", "Role", "Contextual", "Markdown"]),
        ("3", "推理與規劃", "amber",
         ["Chain-of-Thought", "Tabular CoT", "Skeleton-of-Thought", "Step-Back"]),
        ("4", "高階整合", "violet",
         ["Least-to-Most", "Tree-of-Thoughts", "Interactive ToT", "Self-Generated"]),
        ("5", "風格與語氣", "rose", ["Persona", "Predictive"]),
        ("6", "專門化", "green",
         ["Constitutional AI", "Perspective-Taking", "Analogical", "Multi-Modal"]),
    ]

    cw, ch = 290, 176
    xs = [48, 345, 642]
    ys = [122, 318]
    for i, (num, name, stage, items) in enumerate(cats):
        x = xs[i % 3]
        y = ys[i // 3]
        col = C[stage]
        s.rect(x, y, cw, ch, fill="#161b22", stroke=col + "66", rx=10)
        s.badge(x + 32, y + 34, num, col)
        s.text(x + 62, y + 39, name, 15.5, TXT, "700")
        s.text(x + 62, y + 58, "%d 種" % len(items), 11.5, MUT)
        ly = y + 92
        for it in items:
            s.p.append('<circle cx="%s" cy="%s" r="3.5" fill="%s"/>'
                       % (x + 28, ly - 4, col))
            s.text(x + 40, ly, it, 12.5, TXT)
            ly += 21

    s.text(48, 592,
           "※ 這 6 個分類是我要求「用中文整理」後模型自己歸納的，簡報原文沒有這層結構。",
           11.5, MUT)
    return s


def build_decision():
    """該不該用：同一工具，三種需求三種答案。"""
    s = Svg(
        980,
        500,
        "決策流：需要跨語料問答或讓 agent 查語料時值得安裝；要產出 HTML、題庫或 OCR 時"
        "不該用；只要全文檢索則 SQLite FTS5 就足夠",
        "你要的是問答，還是產出？",
        "同一個工具，三種需求三種答案",
    )

    s.box(360, 112, 260, 54, "你的需求是哪一種？", None, "blue", tsize=14.5)

    cards = [
        ("跨語料問答", ["文件、轉錄稿", "混在一起問"], "值得裝", "green"),
        ("讓 agent 查語料", ["接到 Cline 的 MCP", "取代 grep"], "值得裝", "green"),
        ("產出 HTML／題庫", ["既有產線", "已經在做"], "不要用", "rose"),
        ("只要全文檢索", ["單機、不需向量", "一個 SQLite 檔"], "FTS5 就夠", "amber"),
    ]

    xs = [48, 273, 498, 723]
    cw, ch, top = 209, 168, 280
    targets = []
    for x, (title, subs, verdict, stage) in zip(xs, cards):
        col = C[stage]
        s.rect(x, top, cw, ch, fill="#161b22", stroke=col + "66", rx=10)
        s.text(x + cw / 2, top + 36, verdict, 15, col, "700", "middle")
        s.text(x + cw / 2, top + 74, title, 14, TXT, "700", "middle")
        ly = top + 104
        for sub in subs:
            s.text(x + cw / 2, ly, sub, 11.5, MUT, anchor="middle")
            ly += 22
        targets.append((x + cw / 2, top))

    s.bus_out((490, 166), targets, colour="#7d8590", stub=34)

    s.text(48, 476,
           "判斷依據：它輸出的是「對話 + 引用」，不是可發佈的頁面。要交付檔案，既有產線仍是唯一選擇。",
           11.5, MUT)
    return s


def build_timeline():
    """來源 → 切塊 → 向量 → 索引 → 引用 的五階段資料流。"""
    s = Svg(
        980,
        360,
        "資料流時間軸：92 頁 PDF 抽出 43,304 字元後切成 106 塊，用 bge-m3 向量化"
        "寫入 SurrealDB，檢索時以 0.625 相似度命中並回傳段落原文與頁碼；"
        "聊天只走前兩段，Ask 走完全程",
        "從檔案到可引用答案：五個階段",
        "同一份 92 頁簡報，全部在本機完成；數字為實測值",
    )

    stages = [
        ("來源", ["92 頁 PDF", "43,304 字元"], "16.5 s", "blue"),
        ("切塊", ["400 tokens/塊", "overlap 15%"], "106 塊", "teal"),
        ("向量化", ["bge-m3（Ollama）", "寫入 source_embedding"], "42.5 s", "amber"),
        ("索引", ["BM25 + 向量", "SurrealDB 雙索引"], "2 個 function", "violet"),
        ("檢索 → 引用", ["段落原文 + 頁碼", "可追溯 [source:id]"], "0.625", "green"),
    ]

    xs = [96, 288, 480, 672, 864]
    for i, (title, details, value, stage) in enumerate(stages):
        cx = xs[i]
        col = C[stage]
        s.rect(cx - 82, 96, 164, 92, fill="#161b22", stroke=col + "66", rx=10)
        s.text(cx, 126, title, 14, TXT, "700", "middle")
        ly = 150
        for d in details:
            s.text(cx, ly, d, 11.5, MUT, anchor="middle")
            ly += 19
        s.badge(cx, 214, str(i + 1), col, r=15, size=13)
        s.text(cx, 252, value, 12.5, col, "700", "middle")

    for i in range(4):
        s.arrow(xs[i] + 17, 214, xs[i + 1] - 17, 214, "#7d8590", 1.8)

    # 誰走哪幾段（括號 + 端點刻線）
    s.line(96, 292, 288, 292, C["rose"], 2)
    s.line(96, 292, 96, 284, C["rose"], 2)
    s.line(288, 292, 288, 284, C["rose"], 2)
    s.text(192, 276, "聊天：只走 ①→②（把全文塞進 prompt）", 11, C["rose"], anchor="middle")
    s.line(96, 328, 864, 328, C["teal"], 2)
    s.line(96, 328, 96, 320, C["teal"], 2)
    s.line(864, 328, 864, 320, C["teal"], 2)
    s.text(480, 312, "Ask：走完 ①→⑤（檢索、引用、綜合）", 11, C["teal"], anchor="middle")

    return s


CAP_ARCH = (
    "<strong>圖一：四個程序的實際呼叫方向。</strong>"
    "前端只跟 API 說話，API 把長工作寫進 SurrealDB 的 <code>command</code> 表，"
    "背景 worker 用 LIVE query 取走。沒有 worker，來源處理與向量化會永遠停在 Queued——"
    "這是最容易誤判成「程式壞了」的地方。"
)

CAP_METRICS = (
    "<strong>圖二：耗時與 VRAM。</strong>"
    "左側是程式碼端量到的時間，右側是 27B 與 8B 的實測佔用。"
    "24,564 MiB 的 4090 扣掉 19 GB 權重後，32k context 的 KV cache 只剩約 1 GiB——"
    "這就是第一輪 7 分鐘吐不出 token 的原因，不是程式錯誤。"
)

CAP_TAX = (
    "<strong>圖三：6 類 20 種提示技術。</strong>"
    "這個分類結構是 8B 模型自己歸納的——原始簡報只是一頁一頁介紹技術，沒有這層組織。"
    "20 個名稱我逐一回查：16 個完整命中，4 個是模型把原文的基礎詞"
    "（System / Role / Contextual / Markdown）改寫成標籤，不是憑空發明。"
)

CAP_DEC = (
    "<strong>圖四：該不該用。</strong>"
    "決定因素不是「它功能多不多」，而是「你要的是問答還是產出」。"
    "左邊兩種需求值得裝，右邊兩種不值得——尤其是產出型工作，"
    "它給的是對話與引用，不是可發佈的頁面。"
)

CAP_FLOW = (
    "<strong>圖五：資料流時間軸。</strong>"
    "五個階段全部在本機完成，數字是實測值。注意下半部兩條括號——"
    "單一來源聊天只走 ①→②（把全文塞進 prompt），"
    "只有 Ask 會走完 ①→⑤（檢索、引用、綜合）。這就是「算不算 RAG」的分界線。"
)

FIGS = [
    ("FIG1", "open-notebook-arch", build_arch, CAP_ARCH),
    ("FIG2", "open-notebook-metrics", build_metrics, CAP_METRICS),
    ("FIG3", "open-notebook-taxonomy", build_taxonomy, CAP_TAX),
    ("FIG4", "open-notebook-decision", build_decision, CAP_DEC),
    ("FIG5", "open-notebook-timeline", build_timeline, CAP_FLOW),
]


def inject(text, marker, fragment):
    """Replace <!-- marker --> … <!-- /marker --> in place; raise when absent."""
    pattern = re.compile(
        r"<!--\s*%s\s*-->.*?<!--\s*/%s\s*-->" % (marker, marker), re.S
    )
    if not pattern.search(text):
        raise SystemExit("找不到 %s 標記，請先在文章放 <!-- %s --> … <!-- /%s -->"
                         % (marker, marker, marker))
    return pattern.sub(lambda _m: fragment, text, count=1)


def main():
    fig_dir = HERE
    post_path = POST
    with io.open(post_path, "r", encoding="utf-8") as fh:
        before = fh.read()

    text = before
    for marker, name, builder, caption in FIGS:
        svg = builder()
        svg_path = os.path.join(fig_dir, name + ".svg")
        svg.save(svg_path)
        text = inject(text, marker, svg.figure(caption, marker))
        print("%-6s %-26s %6d bytes svg" % (marker, name + ".svg",
                                            os.path.getsize(svg_path)))

    if text == before:
        print("文章內容未變（圖與現有內容一致）")
        return
    with io.open(post_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("已更新 %s（%d → %d bytes）" % (post_path, len(before), len(text)))


if __name__ == "__main__":
    main()
