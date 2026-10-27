# -*- coding: utf-8 -*-
"""embed_gpuunlock_topic.py -- 把 gen_gpuunlock_topic.py 的 2 張圖內嵌進 gpu-unlock 專題頁。

為什麼不用 tools/diagrams/embed_figs.py：
  它只認 source/<note>/index.html + *_Study_Notes.md 的「筆記配對」；
  這個專題頁是 source/gpu-unlock/index.md 單檔，沒有孿生的 md，所以另外處理。
  （同構的先例：embed_rtx40_unlock.py、embed_rtx50_blackwell.py。）

特性：
  - 以 <!-- FIGn --> / <!-- /FIGn --> 標記做幂等（重跑不會重複插入）
  - 保留原本的 CRLF 行尾（寫回時 newline=""）
  - figure 區塊由 svglib 的 Svg.figure() 產生（深色圖卡 + figcaption + print-color-adjust）

用法：
    python embed_gpuunlock_topic.py            # 內嵌（已存在就就地更新）
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (gen_gpuunlock_topic.py)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from gen_gpuunlock_topic import FIGS, build  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
PAGE = os.path.join(REPO, "source", "gpu-unlock", "index.md")

# (slug, 標記)
PLAN = [
    ("gpuunlock-lineage", "FIG1"),
    ("gpuunlock-five-posts", "FIG2"),
]
CAPTIONS = {slug: cap for slug, _w, _h, _aria, _title, _sub, _fn, cap in FIGS}


def theme_fix(fig):
    """Fluid 主題的 main.css 有一條硬規則：

        .markdown-body figcaption:not(.image-caption) { display: none; }

    所以圖說一定要帶 class="image-caption"，否則整段被隱藏。
    另外主題會給 .image-caption 加 opacity:.65 與 margin: -0.75rem auto 2rem，
    這裡一併覆蓋（opacity 還原、下緣留白歸零），維持深色圖卡上下留白對稱。
    """
    return fig.replace('<figcaption style="',
                       '<figcaption class="image-caption" '
                       'style="opacity:1;margin-bottom:0;', 1)


def main():
    text = io.open(PAGE, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in text else "\n"
    changed = 0
    for slug, marker in PLAN:
        fig = theme_fix(build(slug).figure(CAPTIONS[slug], marker)).replace("\n", nl)
        start = text.find("<!-- %s -->" % marker)
        if start < 0:
            raise SystemExit("marker not found: %s" % marker)
        end = text.find("<!-- /%s -->" % marker, start)
        if end < 0:
            raise SystemExit("unterminated marker: %s" % marker)
        end += len("<!-- /%s -->" % marker)
        text = text[:start] + fig + text[end:]
        changed += 1
        print("UPDATED         %-5s %s" % (marker, slug))
    if changed:
        io.open(PAGE, "w", encoding="utf-8", newline="").write(text)
    print("%d figure(s) embedded -> %s" % (changed, PAGE))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
