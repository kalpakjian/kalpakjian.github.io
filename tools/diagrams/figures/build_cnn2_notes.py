# -*- coding: utf-8 -*-
"""cnn2-notes: inline the SVGs into the markdown, then render a single-file index.html.

    python build_cnn2_notes.py

Markdown stays the source of truth: `<!-- CNN2-FIGURE:slug -->` becomes a <figure>
with the SVG inline (so the page has zero external assets), then the whole md is
converted to index.html with the same layout the other lesson pages use.
"""
import html
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_cnn2_notes import CAPTIONS  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DIR = os.path.join(REPO, "source", "cnn2-notes")
MD = os.path.join(DIR, "CNN2_Study_Notes.md")
HTML = os.path.join(DIR, "index.html")
CSS = os.path.join(REPO, "tools", "notes-html", "notes.css")

FIG_TPL = ('<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;'
           'border:1px solid #222b36;border-radius:12px;text-align:center;'
           '-webkit-print-color-adjust:exact;print-color-adjust:exact">\n{s}\n'
           '<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;'
           'line-height:1.65;text-align:left">{c}</figcaption>\n</figure>')


def inline_svg(slug):
    path = os.path.join(HERE, "cnn2-notes", slug + ".svg")
    svg = io.open(path, encoding="utf-8").read().strip()
    svg = re.sub(r'\swidth="[^"]*"|\sheight="[^"]*"', "", svg, count=2)
    return svg.replace("<svg", '<svg style="width:100%;height:auto;display:block"', 1)


def slugify(text):
    t = re.sub(r"<[^>]+>", "", text)
    t = t.replace(" ", "-").lower()
    t = re.sub(r"[^\w\u4e00-\u9fff\-]", "", t)
    return re.sub(r"-{2,}", "-", t).strip("-")


def inline_md(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t


def md_to_html(md):
    lines = md.split("\n")
    out, i, headings = [], 0, []
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            lang, i = line[3:].strip(), i + 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append('<pre class="code"><code>%s</code></pre>' % "\n".join(buf))
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            hid = slugify(text)
            headings.append((level, text, hid))
            out.append(f'<h{level} id="{hid}">{inline_md(text)}</h{level}>')
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:\-|]+\|$", lines[i + 1]):
            head = [c.strip() for c in line.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            out.append("<table><thead><tr>" + "".join(f"<th>{inline_md(c)}</th>" for c in head)
                       + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in r) + "</tr>"
                                 for r in rows)
                       + "</tbody></table>")
            continue
        if re.match(r"^[-*]\s+", line) or re.match(r"^\d+\.\s+", line):
            ordered = bool(re.match(r"^\d+\.\s+", line))
            tag = "ol" if ordered else "ul"
            items = []
            while i < len(lines) and (re.match(r"^[-*]\s+", lines[i])
                                      or re.match(r"^\d+\.\s+", lines[i])):
                item = re.sub(r"^([-*]|\d+\.)\s+", "", lines[i])
                i += 1
                # continuation lines (indented)
                while i < len(lines) and lines[i].startswith("  ") and lines[i].strip():
                    item += " " + lines[i].strip()
                    i += 1
                items.append(item)
            out.append(f"<{tag}>" + "".join(f"<li>{inline_md(x)}</li>" for x in items) + f"</{tag}>")
            continue
        if line.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip("> ").rstrip())
                i += 1
            out.append("<blockquote><p>" + "<br />".join(inline_md(x) for x in buf)
                       + "</p></blockquote>")
            continue
        if line.strip() in ("---", "***"):
            out.append("<hr>")
            i += 1
            continue
        if line.startswith('<figure') or line.startswith('<svg'):
            buf = [line]
            while "</figure>" not in buf[-1] and i + 1 < len(lines):
                i += 1
                buf.append(lines[i])
            out.append("\n".join(buf))
            i += 1
            continue
        if line.startswith("<") and line.rstrip().endswith(">"):
            out.append(line)
            i += 1
            continue
        if not line.strip():
            i += 1
            continue
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{1,4}\s|\||>|```|[-*]\s|\d+\.\s|---|<)", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>" + inline_md(" ".join(buf)) + "</p>")
    return "\n".join(out), headings


TPL = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CNN 2 學習筆記｜AI Tech Notes</title>
<meta name="description" content="CNN（二）：局部連接、輸出體積、ReLU、池化、空洞卷積，以及把課程的模型真的跑起來的六組實測。">
<style>{css}</style>
<style>{codecss}</style>
</head>
<body>
<div class="layout">
<nav class="sidebar">
  <a class="home" href="/">← 回到 AI Tech Notes</a>
  <a class="home" href="/cv-course/">📚 課程專題</a>
  <a class="quiz" href="mc-quiz.html">🖱️ 互動測驗（49 題）</a>
  <h1>CNN 2 學習筆記</h1>
  <div class="sub">Lesson 7 · Convolutional Neural Network (CNN) II</div>
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


def build_toc(headings):
    out, in_sub, li_open = [], False, False
    for level, text, hid in headings:
        if level <= 1:
            continue
        if level == 2:
            if in_sub:
                out.append("</ul>")
                in_sub = False
            if li_open:
                out.append("</li>")
            out.append(f'<li><a href="#{hid}">{html.escape(text)}</a>')
            li_open = True
        elif level == 3:
            if not in_sub:
                out.append("<ul>")
                in_sub = True
            out.append(f'<li><a href="#{hid}">{html.escape(text)}</a></li>')
    if in_sub:
        out.append("</ul>")
    if li_open:
        out.append("</li>")
    return "<ul>\n" + "\n".join(out) + "\n</ul>"


def strip_styles(html_page):
    a = html_page.find("<style>")
    b = html_page.find("</style>", a)
    return html_page[a + 7:b]


def main():
    md = io.open(MD, encoding="utf-8").read()

    md = re.sub(r"<!-- CNN2-FIGURE:([a-z]+) -->.*?<!-- /CNN2-FIGURE:\1 -->",
                r"<!-- CNN2-FIGURE:\1 -->", md, flags=re.S)
    used = []

    def repl(m):
        slug = m.group(1)
        if slug not in CAPTIONS:
            raise SystemExit("unknown figure: " + slug)
        used.append(slug)
        return ("<!-- CNN2-FIGURE:%s -->\n%s\n<!-- /CNN2-FIGURE:%s -->"
                % (slug, FIG_TPL.format(s=inline_svg(slug), c=CAPTIONS[slug]), slug))

    md = re.sub(r"<!--\s*CNN2-FIGURE:([a-z]+)\s*-->", repl, md)
    io.open(MD, "w", encoding="utf-8", newline="\n").write(md)

    body, headings = md_to_html(md)
    css = strip_styles(io.open(os.path.join(REPO, "source", "cnn-notes", "index.html"),
                               encoding="utf-8").read())
    codecss = ("pre.code{background:#0d1117;color:#c9d1d9;border:1px solid #222b36;"
               "border-radius:8px;padding:12px 14px;overflow-x:auto;line-height:1.55;"
               "font-size:13.5px}pre.code code{font-family:ui-monospace,Consolas,monospace}")
    page = TPL.format(css=css, codecss=codecss, toc=build_toc(headings), body=body)
    io.open(HTML, "w", encoding="utf-8", newline="\n").write(page)

    print("figures embedded:", ", ".join(used))
    print("headings:", len(headings), "| md:", len(md), "chars | html:",
          len(page), "chars")


if __name__ == "__main__":
    main()

