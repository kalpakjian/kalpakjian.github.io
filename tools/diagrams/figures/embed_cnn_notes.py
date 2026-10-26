# -*- coding: utf-8 -*-
"""cnn-notes: 把 gen_cnn_notes.py 產生的 SVG 圖表內嵌進筆記的 Markdown。

用法:
    python embed_cnn_notes.py

行為:
  - 讀取 source/cnn-notes/CNN_Study_Notes.md
  - 把每一個 `<!-- CNN-FIGURE:slug -->` 換成 <figure> + 內嵌 SVG + <figcaption>
  - 圖說文字直接取自 gen_cnn_notes.py 的 FIGS（單一真相，不在這裡重複維護）

index.html 由 notes_to_html.py 從 md 產生，所以圖表會自動流到網頁頁面；
md 與 html 的標題永遠一致，品質閘門的「標題一致」檢查才會過。
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_cnn_notes import FIGS                       # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SVG_DIR = os.path.join(HERE, "cnn-notes")
MD = os.path.join(REPO, "source", "cnn-notes", "CNN_Study_Notes.md")

CAPTIONS = {slug: cap for slug, _note, _art, _w, _h, _t, _s, _fn, cap in FIGS}

FIG_TPL = (
    '<!-- CNN-FIGURE:{slug} -->\n'
    '<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;'
    'border:1px solid #222b36;border-radius:12px;text-align:center;'
    '-webkit-print-color-adjust:exact;print-color-adjust:exact">\n'
    '{svg}\n'
    '<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;'
    'line-height:1.65;text-align:left">{cap}</figcaption>\n'
    '</figure>\n'
    '<!-- /CNN-FIGURE:{slug} -->')


def svg_for(slug):
    path = os.path.join(SVG_DIR, slug + ".svg")
    svg = io.open(path, encoding="utf-8").read().strip()
    m = re.match(r"<svg\b[^>]*>", svg)
    tag = re.sub(r'\s(width|height)="[^"]*"', "", m.group(0))
    if "style=" not in tag:
        tag = tag.replace(">", ' style="width:100%;height:auto;display:block">', 1)
    return tag + svg[m.end():]


def main():
    md = io.open(MD, encoding="utf-8").read()

    # idempotent: collapse an already-embedded figure back to its bare marker,
    # so running this twice does not nest one <figure> inside another and does
    # not lose the figure altogether.
    md = re.sub(r"<!-- CNN-FIGURE:([a-z0-9\-]+) -->.*?<!-- /CNN-FIGURE:[a-z0-9\-]+ -->",
                r"<!-- CNN-FIGURE:\1 -->", md, flags=re.S)

    used = []

    def repl(m):
        slug = m.group(1)
        # 筆記裡用簡稱（cortex-layers），產生器用完整檔名（cnn-cortex-layers）
        key = slug if slug in CAPTIONS else ("cnn-" + slug)
        if key not in CAPTIONS:
            raise SystemExit("unknown figure slug: %s" % slug)
        used.append(key)
        return FIG_TPL.format(slug=key, svg=svg_for(key), cap=CAPTIONS[key])

    md2 = re.sub(r"<!--\s*CNN-FIGURE:([a-z0-9\-]+)\s*-->", repl, md)
    md2 = re.sub(r"\n{3,}", "\n\n", md2)
    io.open(MD, "w", encoding="utf-8", newline="\n").write(md2)

    missing = [s for s in CAPTIONS if s not in used]
    print("embedded %d figure(s): %s" % (len(used), ", ".join(used)))
    if missing:
        print("WARNING 沒有被引用的圖: %s" % ", ".join(missing))
    print("md: %s -> %s bytes" % (MD, format(len(md2.encode("utf-8")), ",")))


if __name__ == "__main__":
    main()
