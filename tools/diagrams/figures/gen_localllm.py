# -*- coding: utf-8 -*-
"""local-llm-notes: 6 ASCII blocks -> SVG.

  art#1  §4.1  量化命名 Q4_K_M 的解剖
  art#2  §11.3 llama3.2:1b 的解剖（模型名稱 + tag）
  art#3  §24.1 第一問：用現成 App 還是自己寫程式
  art#4  §24.2 第二問：你的文件在哪裡
  art#5  §27.1 兩條跑本機模型的路（HTTP vs 同行程）
  art#6  §30.2 混合架構：雲端生成 ＋ 本機嵌入
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from svglib import Svg, C, MUT, TXT, CARD2, MONO  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAIL = "#30363d"

QKM = [
    ("Q", "Quantized（量化）", "teal"),
    ("4", "每個權重約 4 bits", "blue"),
    ("K", "k-quant（新一代量化方法，混合精度）", "amber"),
    ("M", "變體：S(small) / M(medium) / L(large)", "violet"),
]

TAG = [
    ("llama3.2", "模型名稱", "teal"),
    (":1b", "tag（標籤）：指定版本／參數量／量化", "blue"),
]

Q1 = [
    ("只想跟模型聊天／問自己的文件", "→ 用現成 App（§24.2 往下走）", "teal"),
    ("要寫 Python、要接自己的系統、要自動化",
     "→ 用 Ollama 的 REST API（§14、§26、§27、§30）", "blue"),
]

Q2 = [
    (0, "只有一兩份文件，想馬上問　→　LM Studio（對話附加檔案，§9）", "teal"),
    (0, "一整批文件，想長期管理、分主題", "blue"),
    (1, "要團隊共用、要接雲端模型　→　AnythingLLM（工作區，§16–§18）", None),
    (1, "只有我自己、不想裝太多東西　→　GPT4All（My Documents，§21–§22）", None),
    (0, "沒有文件，只是要聊天", "amber"),
    (1, "想要漂亮介面　→　LM Studio", None),
    (1, "想用指令、要快　→　Ollama", None),
]

PATHS = [
    ("路徑 A（§14、§26）",
     [("Python", "teal"), ("Ollama（獨立行程）", "amber"), ("GGUF", "violet")],
     ["HTTP", ""]),
    ("路徑 B（課程）",
     [("Python", "teal"), ("同一個行程內推論", "blue")],
     ["直接載入 GGUF"]),
]


def outline_panel(s, x, y, w, h, root, rows, pitch=36, top=84):
    """Bordered panel: root line + a rail/indent tree supporting 3 levels."""
    s.rect(x, y, w, h, fill=CARD2, stroke="#2a6f68", rx=14)
    s.text(x + 28, y + 42, root, 18, TXT, "700")
    rail, sub, sub2 = x + 52, x + 108, x + 164
    ys = [y + top + i * pitch for i in range(len(rows))]
    s.line(rail, ys[0] - 6, rail, ys[-1] - 6, RAIL, 1.5)
    for i, (lvl, txt, stage) in enumerate(rows):
        sy = ys[i] - 6
        if lvl == 0:
            s.line(rail, sy, rail + 14, sy, RAIL, 1.5)
            s.text(rail + 20, ys[i], txt, 13.5, C[stage] if stage else TXT, "700")
        elif lvl == 1:
            s.line(sub, ys[i - 1] - 6 + 10, sub, sy, RAIL, 1.5)
            s.line(sub, sy, sub + 14, sy, RAIL, 1.5)
            s.text(sub + 20, ys[i], txt, 12.5, TXT)
        else:
            s.line(sub2, ys[i - 1] - 6 + 10, sub2, sy, RAIL, 1.5)
            s.line(sub2, sy, sub2 + 14, sy, RAIL, 1.5)
            s.text(sub2 + 20, ys[i], txt, 12, MUT)


def kv_rows(s, rows, y0=190, pitch=46, chip_x=180):
    """One monospace chip per row, meaning text to its right."""
    for i, (chip, label, stage) in enumerate(rows):
        y = y0 + i * pitch
        w = max(46, len(chip) * 8 + 20)
        s.rect(chip_x, y - 21, w, 34, fill="#0d1117", stroke=C[stage] + "99", rx=8)
        s.text(chip_x + w / 2, y + 3, chip, 13, C[stage], "700", "middle", MONO)
        s.text(chip_x + w + 20, y + 4, label, 12.5, TXT)


def fig_qkm(s):
    s.text(450, 134, "Q4_K_M", 30, TXT, "700", "middle", MONO)
    kv_rows(s, QKM)
    s.text(48, 366, "讀法：Q＝量化、4＝4 bits、K＝k-quant、M＝中size；"
                    "數字越小越省記憶體、品質越低。", 13, MUT)


def fig_tag(s):
    s.text(450, 134, "llama3.2:1b", 28, TXT, "700", "middle", MONO)
    kv_rows(s, TAG, y0=196)
    s.text(48, 300, "冒號後面是 tag：同一個模型可以有 llama3.2:1b、llama3.2:3b 等多種版本。", 13, MUT)



def fig_q1(s):
    s.box(300, 110, 300, 56, "你要做什麼？", None, "amber", tsize=15)
    for i, (title, detail, stage) in enumerate(Q1):
        x = 48 + i * 414
        s.rect(x, 220, 390, 86, fill=CARD2, stroke=C[stage] + "66", rx=12)
        s.text(x + 20, 254, title, 14, C[stage], "700")
        s.text(x + 20, 280, detail, 11.5, MUT)
    s.bus_out((450, 166), [(243, 220), (657, 220)])
    s.text(48, 350, "這是最重要的分岔：課程前半教你用 App，lesson67 之後的 Lab 全部要你自己寫；兩者都要會。",
           13, MUT)


def fig_q2(s):
    outline_panel(s, 48, 106, 904, 326, "你的文件在哪？", Q2)
    s.text(48, 472, "文件越少越隨便挑（LM Studio 附加檔案），文件越多越需要工作區管理（AnythingLLM／GPT4All）。",
           13, MUT)


def fig_paths(s):
    for r, (label, pills, arrows) in enumerate(PATHS):
        top = 130 + r * 70
        cy = top + 22
        s.text(48, cy + 5, label, 13.5, C["teal"] if r == 0 else C["blue"], "700")
        x = 260
        for i, (txt, stage) in enumerate(pills):
            w = s._est_w(txt, 12.5) + 30
            s.rect(x, top, w, 44, fill=CARD2, stroke=C[stage] + "66", rx=22)
            s.text(x + w / 2, cy + 5, txt, 12.5, TXT, "700", "middle")
            if i < len(pills) - 1:
                gap = 120
                s.arrow(x + w + 6, cy, x + w + gap - 6, cy, RAIL)
                if arrows[i]:
                    s.text(x + w + gap / 2, cy - 10, arrows[i], 11.5, MUT, "normal", "middle")
            x += w + 120
    s.text(48, 290, "路徑 A 是「兩個行程、用 HTTP 講話」；路徑 B 是「同一個行程、直接把 GGUF 載進來」。",
           13, MUT)


def fig_rag(s):
    s.rect(170, 130, 480, 90, fill=CARD2, stroke=C["blue"] + "66", rx=12)
    s.text(190, 162, "雲端", 14.5, C["blue"], "700")
    s.text(190, 192, "Groq：llama-3.1-8b-instant", 12.5, TXT)
    s.text(670, 192, "← 生成（要 API key、要網路）", 11.5, MUT)

    s.rect(170, 300, 480, 110, fill=CARD2, stroke=C["green"] + "66", rx=12)
    s.text(190, 332, "本機", 14.5, C["green"], "700")
    s.text(190, 362, "all-MiniLM-L6-v2（嵌入）", 12.5, TXT)
    s.text(190, 388, "VectorStoreIndex（索引）", 12.5, TXT)
    s.text(670, 374, "← 嵌入（不用 key、不外洩）", 11.5, MUT)

    s.arrow(410, 296, 410, 224)
    s.text(424, 264, "檢索到的段落", 11.5, MUT)

    s.text(48, 450, "嵌入要跑很多次（每個段落一次）→ 放本機免費又保護隱私；"
                    "生成只要跑一次 → 用雲端拿更好的品質。", 13, MUT)


FIGS = [
    ("localllm-qkm", "local-llm-notes", 1, 900, 400,
     "量化命名怎麼讀：Q4_K_M", "一個字元一個意思", fig_qkm,
     "圖 40：Q4_K_M 的解剖——Q（Quantized）、4（每個權重約 4 bits）、K（k-quant，混合精度）、"
     "M（中 size）。｜手繪 SVG 圖表"),
    ("localllm-tag", "local-llm-notes", 2, 900, 330,
     "llama3.2:1b 怎麼讀", "冒號前面是模型、後面是 tag", fig_tag,
     "圖 41：Ollama 模型名稱的解剖——llama3.2 是模型名稱，:1b 是 tag（指定版本／參數量／量化）。"
     "｜手繪 SVG 圖表"),
    ("localllm-q1", "local-llm-notes", 3, 900, 380,
     "第一問：你要做什麼？", "用現成 App，還是自己寫程式", fig_q1,
     "圖 42：第一問——只想聊天／問文件就用現成 App；要寫 Python、接自己的系統、要自動化，"
     "就走 Ollama 的 REST API。｜手繪 SVG 圖表"),
    ("localllm-q2", "local-llm-notes", 4, 1000, 500,
     "第二問：你的文件在哪裡？", "文件量與管理需求決定用哪個 App", fig_q2,
     "圖 43：第二問——一兩份文件用 LM Studio 附加檔案；一整批文件要長期管理就用 AnythingLLM"
     "（團隊／雲端）或 GPT4All（個人、輕量）；沒有文件只是聊天，漂亮介面選 LM Studio、"
     "要指令要快選 Ollama。｜手繪 SVG 圖表"),
    ("localllm-paths", "local-llm-notes", 5, 1000, 320,
     "兩條跑本機模型的路", "HTTP 給獨立行程，或同一個行程直接載入", fig_paths,
     "圖 44：兩條路——路徑 A（Python 用 HTTP 呼叫獨立的 Ollama 行程，再讀 GGUF）；"
     "路徑 B（Python 在同一個行程內直接載入 GGUF 推論）。｜手繪 SVG 圖表"),
    ("localllm-rag", "local-llm-notes", 6, 900, 480,
     "混合架構：雲端生成 ＋ 本機嵌入", "嵌入放本機、生成放雲端", fig_rag,
     "圖 45：混合架構——本機跑 all-MiniLM-L6-v2 做嵌入、VectorStoreIndex 做索引，"
     "把檢索到的段落送上雲端（Groq llama-3.1-8b-instant）生成答案。｜手繪 SVG 圖表"),
]

if __name__ == "__main__":
    for slug, note, art, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-30s %-18s art#%d %dx%d  %s"
              % (slug + ".svg", note, art, w, h,
                 "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))
