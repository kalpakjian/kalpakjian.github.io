# -*- coding: utf-8 -*-
"""cnn-cheatsheet: turn CNN_Cheat_Sheet.md into a single-file index.html.

Reuses the renderer and the stylesheet of the two notes pages, so the new page
looks identical without copying 200 lines of markdown-to-HTML code.

    python build_cheatsheet.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_cnn2_notes import build_toc, md_to_html, strip_styles  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DIR = os.path.join(REPO, "source", "cnn-cheatsheet")
MD = os.path.join(DIR, "CNN_Cheat_Sheet.md")
HTML = os.path.join(DIR, "index.html")

TPL = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CNN 速查表（CNN 1 ＋ CNN 2 合訂）｜AI Tech Notes</title>
<meta name="description" content="輸出尺寸、參數速算、核心速查、術語、陷阱與一頁精華：CNN 1 與 CNN 2 兩份筆記共用的附錄只維護這一頁。">
<style>{css}</style>
<style>{codecss}</style>
</head>
<body>
<div class="layout">
<nav class="sidebar">
  <a class="home" href="/">← 回到 AI Tech Notes</a>
  <a class="home" href="/cv-course/">📚 課程專題</a>
  <a class="quiz" href="/cnn-notes/">📘 CNN 1 學習筆記</a>
  <a class="quiz" href="/cnn2-notes/">📗 CNN 2 學習筆記</a>
  <h1>CNN 速查表</h1>
  <div class="sub">CNN 1 ＋ CNN 2 合訂 · 考前速查</div>
  <div class="toc">
{toc}
  </div>
</nav>
<main>
{body}
</main>
</div>
</body>
</html>
"""


def main():
    md = io.open(MD, encoding="utf-8").read()
    body, headings = md_to_html(md)
    css = strip_styles(io.open(os.path.join(REPO, "source", "cnn-notes", "index.html"),
                               encoding="utf-8").read())
    codecss = ("pre.code{background:#0d1117;color:#c9d1d9;border:1px solid #222b36;"
               "border-radius:8px;padding:12px 14px;overflow-x:auto;line-height:1.55;"
               "font-size:13.5px}pre.code code{font-family:ui-monospace,Consolas,monospace}")
    page = TPL.format(css=css, codecss=codecss, toc=build_toc(headings), body=body)
    io.open(HTML, "w", encoding="utf-8", newline="\n").write(page)
    print("headings:", len(headings), "| html:", len(page), "chars ->", HTML)


if __name__ == "__main__":
    main()
