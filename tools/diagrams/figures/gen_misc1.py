# -*- coding: utf-8 -*-
"""Two small notes, one diagram each.

  litellm-notes         block #57 : LiteLLM Proxy 模型閘道
  neural-network-notes  block #3  : 問題類型 -> 激活函數 決策樹
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import Svg, C, MUT, TXT, CARD2  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def vlabel(s, x, y, txt):
    s.text(x + 9, y, txt, 11.5, MUT, "normal", "start")


def elbow(s, x1, y1, x2, y2, midx, colour="#7d8590"):
    """H -> V -> H connector ending in an arrow (for trees)."""
    s.line(x1, y1, midx, y1, colour)
    s.line(midx, y1, midx, y2, colour)
    s.arrow(midx, y2, x2 - 2, y2, colour)


def fig_litellm(s):
    s.box(300, 110, 300, 56, "OpenWebUI（或任何前端）", None, "teal")
    s.arrow(450, 166, 450, 202)
    vlabel(s, 450, 186, "OpenAI 相容 API")

    s.box(250, 204, 400, 64, "LiteLLM Proxy", "模型閘道（唯一對外入口）", "violet")

    s.line(450, 268, 450, 292)
    s.line(240, 292, 660, 292)
    for cx in (240, 660):
        s.arrow(cx, 292, cx, 314, "#7d8590")
    s.text(48, 349, "模型", 12.5, MUT)
    s.box(120, 316, 240, 58, "Ollama", "本機模型", "amber")
    s.box(480, 316, 360, 58, "雲端 LLM", "OpenAI / Azure / Anthropic / …", "blue")

    s.line(450, 374, 450, 382)
    s.line(240, 382, 660, 382)
    for cx in (240, 660):
        s.arrow(cx, 382, cx, 404, "#7d8590")
    s.text(48, 439, "狀態與工具", 12.5, MUT)
    s.box(120, 406, 240, 58, "Postgres", "虛擬金鑰 · 預算 · 用量 · 日誌", "green")
    s.box(480, 406, 360, 58, "MCP 工具", "tooling", "rose")

    s.text(48, 516, "前端只認一個 OpenAI 相容端點；由 LiteLLM 決定要打本機 Ollama 還是雲端，"
                    "並把金鑰、預算與用量記在 Postgres。", 13, MUT)


def fig_nn(s):
    s.box(60, 135, 130, 48, "Problem", None, "teal")
    s.box(270, 74, 180, 44, "Classification", None, "blue")
    s.box(270, 200, 180, 44, "Regression", None, "amber")
    for y, t in ((20, "Binary Classification → TLU"),
                 (76, "Multiclass Classification → Softmax"),
                 (132, "Multilabel Classification → Sigmoid")):
        s.box(530, y, 280, 40, t, None, "violet", tsize=12)
    elbow(s, 190, 159, 270, 96, 230)
    elbow(s, 190, 159, 270, 222, 230)
    for y in (40, 96, 152):
        elbow(s, 450, 96, 530, y, 490, C["violet"])
    s.text(48, 268, "先問「這是什麼類型的問題」，再決定輸出層要用哪個激活函數——"
                    "二元分類用 TLU、多類別用 Softmax、多標籤用 Sigmoid、迴歸用 ReLU。", 13, MUT)


FIGS = [
    ("litellm-proxy-gateway", "litellm-notes", 1, 900, 560,
     "LiteLLM Proxy：模型閘道", "前端只認一個端點，由它決定打本機還是雲端", fig_litellm,
     "圖 24：LiteLLM Proxy 的角色——唯一的對外入口，向下分流到本機 Ollama 與雲端 LLM，"
     "並把狀態寫進 Postgres。｜手繪 SVG 圖表"),
    ("nn-problem-to-activation", "neural-network-notes", 1, 900, 300,
     "問題類型 → 激活函數", "先分類問題，再挑輸出層", fig_nn,
     "圖 39：問題類型決定激活函數——分類問題再細分二元／多類別／多標籤，"
     "迴歸問題用 ReLU。｜手繪 SVG 圖表"),
]

if __name__ == "__main__":
    for slug, note, art, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        flag = "OK" if not bad else "COLLISION x%d" % len(bad)
        print("wrote %-30s %-24s art#%d %dx%d  %s" % (slug + ".svg", note, art, w, h, flag))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))
