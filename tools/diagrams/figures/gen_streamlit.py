# -*- coding: utf-8 -*-
"""streamlit-flask-notes: 3 ASCII blocks -> SVG.

  block #2  : 四層架構速覽
  block #52 : app.py 的兩個 UI 區塊
  block #64 : 完整架構（瀏覽器 → Streamlit → Flask / LiteLLM → Ollama）
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
sys.path.insert(0, os.path.dirname(_HERE))   # 上一層：svglib.py 在這裡
from svglib import Svg, C, MUT, TXT, CARD2  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def label(s, x, y, txt, anchor="middle"):
    s.text(x, y, txt, 11.5, C["gray"] if False else "#8b949e", "normal", anchor)


def fig_stack(s):
    s.box(120, 120, 360, 62, "使用者瀏覽器", None, "teal")
    s.box(120, 216, 360, 62, "Streamlit 前端", "app.py（埠 8501）", "teal")
    s.box(120, 312, 360, 62, "LiteLLM", "model = ollama/smollm", "violet")
    s.box(600, 216, 250, 62, "Flask 後端", "server.py（埠 5000）", "blue")
    s.box(600, 312, 250, 62, "Ollama", "127.0.0.1:11434", "amber")
    s.arrow(300, 182, 300, 214)
    vlabel(s, 300, 202, "HTTP :8501")
    s.arrow(480, 247, 598, 247, C["blue"])
    label(s, 539, 239, "POST /greet")
    s.arrow(300, 278, 300, 310, C["violet"])
    label(s, 310, 298, "completion()", "start")
    s.arrow(480, 343, 598, 343, C["amber"])
    label(s, 539, 335, "HTTP")
    s.text(48, 430, "瀏覽器只跟 Streamlit 講話；Streamlit 再分頭呼叫 Flask（問候）與 "
                    "LiteLLM（問 LLM），LiteLLM 最後把請求轉給本機 Ollama。", 13, MUT)


def fig_blocks(s):
    s.rect(80, 120, 740, 330, fill=CARD2, stroke="#2a6f68", rx=14)
    s.text(102, 152, "app.py（Streamlit，埠 8501）", 15, TXT, "700")
    s.box(110, 172, 680, 96, "區塊 1：問候", "輸入名字 → POST /greet → Flask（埠 5000）",
          "teal", fill="#0d1117")
    s.line(110, 296, 790, 296, "#30363d", 1.5)
    s.text(450, 290, "st.divider()", 12, MUT, "normal", "middle")
    s.box(110, 316, 680, 96, "區塊 2：問 LLM", "輸入問題 → completion() → Ollama（埠 11434）",
          "violet", fill="#0d1117")
def panel(s, x, y, w, h, title, lines, stage):
    """A bordered panel with a title and a list of monospace code lines."""
    s.rect(x, y, w, h, fill="#0d1117", stroke=C[stage] + "66", rx=10)
    s.text(x + 16, y + 28, title, 14, TXT, "700")
    for i, ln in enumerate(lines):
        s.text(x + 16, y + 52 + i * 22, ln, 11.5, MUT, "normal", "start",
               "'Cascadia Mono',Consolas,monospace")


def vlabel(s, x, y, txt):
    s.text(x + 9, y, txt, 11.5, MUT, "normal", "start")


def fig_arch(s):
    s.box(300, 110, 360, 62, "使用者瀏覽器", "http://localhost:8501", "teal")
    s.arrow(480, 172, 480, 220)
    vlabel(s, 480, 200, "WebSocket / HTTP")

    s.rect(150, 222, 660, 196, fill=CARD2, stroke="#2a6f68", rx=14)
    s.text(172, 252, "Streamlit 前端　app.py", 15, TXT, "700")
    panel(s, 167, 272, 266, 124, "區塊 1：問候",
          ["st.text_input(name)", "st.button(...)", "→ requests.post"],
          "teal")
    panel(s, 525, 272, 270, 124, "區塊 2：問 LLM",
          ["st.text_input(question)", 'st.button("Ask LLM")',
           "→ completion()"], "teal")

    s.arrow(300, 396, 300, 466, C["blue"])
    vlabel(s, 300, 440, "requests.post")
    s.arrow(660, 396, 660, 466, C["violet"])
    vlabel(s, 660, 440, "completion()")

    panel(s, 170, 468, 260, 126, "Flask 後端　server.py",
          ["@app.route('/greet',", "          POST)",
           "request.get_json()", "jsonify({...})"], "blue")
    panel(s, 530, 468, 260, 88, "LiteLLM", ['model="ollama/smollm"'], "violet")

    s.arrow(660, 556, 660, 604, C["amber"])
    vlabel(s, 660, 586, "HTTP")
    panel(s, 530, 606, 260, 76, "Ollama", ["http://127.0.0.1:11434"], "amber")

    s.text(48, 722, "兩條獨立的後端路線：問候走 Flask（自己寫的 API），問 LLM 走 "
                    "LiteLLM（統一模型介面），LiteLLM 再轉給本機 Ollama。", 13, MUT)


FIGS = [
    ("streamlit-arch-overview", 2, 900, 480, "Streamlit + Flask + LiteLLM 四層架構",
     "誰呼叫誰、走哪個埠", fig_stack,
     "圖 1：四層架構速覽——瀏覽器只跟 Streamlit 講話，Streamlit 再分頭呼叫 "
     "Flask 與 LiteLLM。"),
    ("streamlit-app-blocks", 52, 900, 540, "app.py 的兩個 UI 區塊",
     "一個頁面、兩條後端路線", fig_blocks,
     "圖 2：app.py 內部的兩個區塊——問候走 Flask，問 LLM 走 Ollama，"
     "中間的 st.divider() 只是視覺分隔。"),
    ("streamlit-arch-full", 64, 960, 760, "Streamlit + Flask + LiteLLM 完整架構",
     "從瀏覽器點擊到 Ollama 回應的完整路徑", fig_arch,
     "圖 3：完整架構——每一層的檔案、埠號與實際呼叫的函式。"),
]

if __name__ == "__main__":
    for slug, blk, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-28s block #%-3d %dx%d" % (slug + ".svg", blk, w, h))
