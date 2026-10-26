# -*- coding: utf-8 -*-
"""embed_flashmap_bf16.py -- 把 gen_flashmap_bf16.py 的 2 張圖內嵌進 _posts 文章。

為什麼不用 tools/diagrams/embed_figs.py：
  它只認 source/<note>/index.html + *_Study_Notes.md 的「筆記配對」；
  這篇是 source/_posts/ 的一般文章（沒有孿生 index.html），所以另外處理。

特性：
  - 錨點用單行字串比對（不靠行號，改文也不會錯位）
  - 以 <!-- FIGn --> 標記做幂等（重跑就地更新，不會重複插入）
  - 保留原本的 CRLF 行尾（寫回時 newline=""）
  - figure 區塊由 svglib 的 Svg.figure() 產生（深色圖卡 + figcaption + print-color-adjust）

用法：
    python embed_flashmap_bf16.py       # 內嵌／更新
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (gen_flashmap_bf16.py)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from gen_flashmap_bf16 import FIGS, build  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
POST = os.path.join(REPO, "source", "_posts", "flashmap-bf16-losslessness.md")

# (slug, 標記, 錨點（單行、唯一）, before／after)
PLAN = [
    ("flashmap-bf16-quant-grid", "FIG1",
     "## 三、四個實驗，把責任釘死在精度上", "before"),
    ("flashmap-bf16-two-shapes", "FIG2",
     "**「形狀會改變答案」這件事只在 bf16 發生，fp32 下完全消失。** 這也正好解釋了上游那句警語。",
     "after"),
]
CAPTIONS = {slug: cap for slug, _w, _h, _aria, _sub, _fn, cap in FIGS}


def theme_fix(fig):
    """Fluid 主題的 main.css 有一條硬規則：

        .markdown-body figcaption:not(.image-caption) { display: none; }

    所以 _posts 文章的圖說一定要帶 class="image-caption"，否則整段被隱藏
    （筆記的單檔 HTML 沒有載入主題 CSS，所以不受影響）。
    另外主題會給 .image-caption 加 opacity:.65 與 margin: -0.75rem auto 2rem，
    這裡一併覆蓋（opacity 還原、下緣留白歸零），維持深色圖卡上下留白對稱。
    """
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
        if start >= 0:                      # 已存在 → 就地更新（可重跑）
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
