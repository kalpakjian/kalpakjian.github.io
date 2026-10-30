# -*- coding: utf-8 -*-
"""cnn-illustrated: inline the SVGs into the markdown, then render index.html.

    python build_cnn_illustrated.py

Same shape as tools/diagrams/figures/build_cnn2_notes.py: markdown stays the
single source of truth, `<!-- CNNI-FIGURE:slug -->` becomes a <figure> with the
SVG inline (zero external assets), then the whole md is rendered to index.html
with the layout the other note pages use.
"""
import html
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DIR = os.path.join(REPO, "source", "cnn-illustrated")
MD = os.path.join(DIR, "CNN_Illustrated_Study_Notes.md")
HTML = os.path.join(DIR, "index.html")
FIGS = os.path.join(HERE, "cnn-illustrated")

sys.path.insert(0, HERE)
from gen_cnn_illustrated import CAPTIONS  # noqa: E402

FIG_TPL = ('<figure style="margin:22px 0;padding:14px 12px;background:#0d1117;'
           'border:1px solid #222b36;border-radius:12px;text-align:center;'
           '-webkit-print-color-adjust:exact;print-color-adjust:exact">\n{s}\n'
           '<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;'
           'line-height:1.65;text-align:left">{c}</figcaption>\n</figure>')

RAW_TAGS = r"</?(?:strong|em|code|br\s*/?)>"


def inline_svg(slug):
    path = os.path.join(FIGS, slug + ".svg")
    svg = io.open(path, encoding="utf-8").read().strip()
    return svg.replace("<svg", '<svg style="width:100%;height:auto;display:block"', 1)


def slugify(text):
    t = re.sub(r"<[^>]+>", "", text)
    t = t.replace(" ", "-").lower()
    t = re.sub(r"[^\w\u4e00-\u9fff\-]", "", t)
    return re.sub(r"-{2,}", "-", t).strip("-")


def inline_md(t):
    store = []

    def stash(m):
        store.append(m.group(0))
        return "\x00%d\x00" % (len(store) - 1)

    t = re.sub(RAW_TAGS, stash, t)
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    for i, s in enumerate(store):
        t = t.replace("\x00%d\x00" % i, s)
    return t


def join_lines(buf):
    out = ""
    for line in buf:
        if out and re.search(r"[A-Za-z0-9]$", out) and re.match(r"[A-Za-z0-9]", line):
            out += " " + line
        else:
            out += line
    return out


def md_to_html(md):
    lines = md.split("\n")
    out, headings, i = [], [], 0
    guard = 0
    while i < len(lines):
        guard += 1
        if guard > 200000:
            raise RuntimeError("stuck at line %d: %r" % (i, lines[i][:160]))
        line = lines[i]
        if line.startswith("```"):
            i += 1
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
            out.append('<h%d id="%s">%s</h%d>' % (level, hid, inline_md(text), level))
            i += 1
            continue
        if line.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].strip())
                i += 1
            out.append("<blockquote><p>%s</p></blockquote>"
                       % "<br />".join(inline_md(b) for b in buf if b))
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(
                r"^\|[\s:\-|]+\|$", lines[i + 1]):
            head = [c.strip() for c in line.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            out.append("<table><thead><tr>"
                       + "".join("<th>%s</th>" % inline_md(c) for c in head)
                       + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join("<td>%s</td>" % inline_md(c) for c in r)
                                 + "</tr>" for r in rows)
                       + "</tbody></table>")
            continue
        if line.startswith("<"):
            buf = []
            while i < len(lines) and lines[i].strip():
                buf.append(lines[i])
                i += 1
            out.append("\n".join(buf))
            continue
        if re.match(r"^[-*]\s", line):
            items = []
            while i < len(lines) and (re.match(r"^[-*]\s", lines[i])
                                      or (lines[i].startswith("  ") and items)):
                if re.match(r"^[-*]\s", lines[i]):
                    items.append([lines[i][2:].strip()])
                else:
                    items[-1].append(lines[i].strip())
                i += 1
            out.append("<ul>" + "".join("<li>%s</li>" % inline_md(join_lines(it))
                                        for it in items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s", line):
            items = []
            while i < len(lines) and (re.match(r"^\d+\.\s", lines[i])
                                      or (lines[i].startswith("  ") and items)):
                if re.match(r"^\d+\.\s", lines[i]):
                    items.append([re.sub(r"^\d+\.\s", "", lines[i])])
                else:
                    items[-1].append(lines[i].strip())
                i += 1
            out.append("<ol>" + "".join("<li>%s</li>" % inline_md(join_lines(it))
                                        for it in items) + "</ol>")
            continue
        if re.match(r"^-{3,}$", line.strip()):
            out.append("<hr />")
            i += 1
            continue
        if not line.strip():
            i += 1
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{1,4}\s|\||>|```|[-*]\s|\d+\.\s|-{3,}$|<)", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>" + inline_md(join_lines(buf)) + "</p>")
    return "\n".join(out), headings


TPL = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>圖解 CNN：卷積神經網路｜AI Tech Notes</title>
<meta name="description" content="圖解 CNN：從一張 5×5 的黑白小圖開始，把卷積、ReLU、池化、全連接與 softmax 一路算到類別機率；8 張手繪內嵌 SVG，所有數字本機實測。">
<style>{css}</style>
<style>{codecss}</style>
</head>
<body>
<div class="layout">
<nav class="sidebar">
  <a class="home" href="/">← 回到 AI Tech Notes</a>
  <a class="home" href="/cv-course/">📚 課程專題</a>
  <a class="home" href="CNN_Illustrated_Study_Notes.md">📄 下載原始 Markdown</a>
  <a class="quiz" href="mc-quiz.html">🖱️ 互動測驗（30 題）</a>
  <h1>圖解 CNN：卷積神經網路</h1>
  <div class="sub">四種層的圖解 · 卷積 → ReLU → 池化 → 全連接</div>
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
            out.append('<li><a href="#%s">%s</a>' % (hid, html.escape(text)))
            li_open = True
        elif level == 3:
            if not in_sub:
                out.append("<ul>")
                in_sub = True
            out.append('<li><a href="#%s">%s</a></li>' % (hid, html.escape(text)))
    if in_sub:
        out.append("</ul>")
    if li_open:
        out.append("</li>")
    return "<ul>\n" + "\n".join(out) + "\n</ul>"


def strip_styles(page):
    a = page.find("<style>")
    b = page.find("</style>", a)
    return page[a + 7:b]


def read_text(path):
    return io.open(path, encoding="utf-8", newline="").read().replace("\r\n", "\n")


def write_crlf(path, text):
    io.open(path, "w", encoding="utf-8", newline="\r\n").write(text)


def main():
    md = read_text(MD)

    # a rebuild must not stack figure blocks: drop whatever sits between markers
    md = re.sub(r"<!-- CNNI-FIGURE:([a-z]+) -->.*?<!-- /CNNI-FIGURE:\1 -->",
                r"<!-- CNNI-FIGURE:\1 -->", md, flags=re.S)
    used = []

    def repl(m):
        slug = m.group(1)
        if slug not in CAPTIONS:
            raise SystemExit("unknown figure: " + slug)
        used.append(slug)
        return ("<!-- CNNI-FIGURE:%s -->\n%s\n<!-- /CNNI-FIGURE:%s -->"
                % (slug, FIG_TPL.format(s=inline_svg(slug), c=CAPTIONS[slug]), slug))

    md = re.sub(r"<!--\s*CNNI-FIGURE:([a-z]+)\s*-->", repl, md)
    write_crlf(MD, md)

    body, headings = md_to_html(md)
    css = strip_styles(read_text(os.path.join(REPO, "source", "cnn-notes", "index.html")))
    codecss = ("pre.code{background:#0d1117;color:#c9d1d9;border:1px solid #222b36;"
               "border-radius:8px;padding:12px 14px;overflow-x:auto;line-height:1.55;"
               "font-size:13.5px}pre.code code{font-family:ui-monospace,Consolas,monospace;"
               "color:#c9d1d9;background:none;padding:0}")
    page = TPL.format(css=css, codecss=codecss, toc=build_toc(headings), body=body)
    write_crlf(HTML, page)

    print("figures embedded:", ", ".join(used))
    print("headings:", len(headings), "| md:", len(md), "chars | html:",
          len(page), "chars")


if __name__ == "__main__":
    main()
