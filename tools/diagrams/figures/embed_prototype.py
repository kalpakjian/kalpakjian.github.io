# -*- coding: utf-8 -*-
"""embed_prototype.py -- 把 gen_prototype.py 的圖內嵌進 _posts 文章。

沿用 embed_pytoolkit.py 的作法（_posts 文章沒有孿生 index.html）：
  - 錨點用單行字串比對（不靠行號）
  - 以 <!-- FIGn --> 標記做幂等（重跑就地更新）
  - 保留原本的 CRLF 行尾
  - figcaption 必須帶 class="image-caption"（Fluid 主題會隱藏沒有這個 class 的圖說）

用法：
    python embed_prototype.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.dirname(_HERE))
from gen_prototype import FIGS, build  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
POST = os.path.join(REPO, "source", "_posts", "prototype-over-specs.md")

# (slug, 標記, 錨點（單行、唯一）, before／after)
PLAN = [
    ("prototype-two-branches", "FIG1",
     "| 問題類型 | 產出物 | 機制 |", "before"),
]
CAPTIONS = {f[0]: f[8] for f in FIGS}


def theme_fix(fig):
    """Fluid 主題：沒有 class="image-caption" 的 figcaption 會被 display:none 隱藏。"""
    return fig.replace('<figcaption style="',
                       '<figcaption class="image-caption" '
                       'style="opacity:1;margin-bottom:0;', 1)


def main():
    text = io.open(POST, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in text else "\n"
    changed = 0
    for slug, marker, anchor, where in PLAN:
        fig = theme_fix(build(slug).figure(CAPTIONS[slug], marker)).replace("\n", nl)
        start = text.find("<!-- %s -->" % marker)
        if start >= 0:
            end = text.find("<!-- /%s -->" % marker, start)
            if end < 0:
                raise SystemExit("unterminated marker: %s" % marker)
            end += len("<!-- /%s -->" % marker)
            text = text[:start] + fig + text[end:]
            changed += 1
            print("UPDATED         %-5s %s" % (marker, slug))
            continue
        i = text.find(anchor)
        if i < 0:
            raise SystemExit("anchor not found: %r" % anchor)
        if where == "before":
            text = text[:i] + fig + nl + nl + text[i:]
        else:
            j = i + len(anchor)
            text = text[:j] + nl + nl + fig + text[j:]
        changed += 1
        print("INSERTED        %-5s %s" % (marker, slug))
    if changed:
        io.open(POST, "w", encoding="utf-8", newline="").write(text)
    print("%d figure(s) embedded -> %s" % (changed, POST))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
