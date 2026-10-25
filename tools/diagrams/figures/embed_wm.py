# -*- coding: utf-8 -*-
"""embed_wm.py -- 把 gen_wm.py 的 3 張圖內嵌進 xr-vs-world-model 這篇 _posts 文章。

這篇是 source/_posts/ 的一般文章（沒有 index.html 孿生檔），所以不用
tools/diagrams/embed_figs.py（後者只吃 source/<note>/ 筆記 + *_Study_Notes.md），
改用同目錄的 embed_dossier.py 當範本。

特性：
  - 錨點用單行字串比對（不靠行號，改文也不會錯位）
  - 以 <!-- FIGn --> 標記做幂等（重跑不會重複插入）
  - 保留原本的 CRLF 行尾（寫回時 newline=""）
  - figure 區塊由 svglib 的 Svg.figure() 產生（深色圖卡 + figcaption + print-color-adjust）

用法：
    python embed_wm.py            # 內嵌（已存在就就地更新）
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from gen_wm import FIGS, build  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
POST = os.path.join(REPO, "source", "_posts", "xr-vs-world-model.md")

# (slug, 標記, 錨點（單行、唯一）, before／after)
PLAN = [
    ("wm-three-3d", "FIG1", "## 一、「做出 3D」其實有三種方式", "after"),
    ("wm-human-vs-ai", "FIG2", "## 二、核心不是「重建」，是「理解」", "after"),
    ("wm-two-branches", "FIG3", "## 三、兩個分支，兩種驗證方式", "after"),
    ("wm-capability-matrix", "FIG4", "這條取捨還有一層更深的含意。", "after"),
    ("wm-2026-timeline", "FIG5", "## 四、2026 年的現況：四件事把這個框架推到了實證階段", "after"),
]
CAPTIONS = {f[0]: f[8] for f in FIGS}


def theme_fix(fig):
    """Fluid 主題的 main.css 有一條硬規則：

        .markdown-body figcaption:not(.image-caption) { display: none; }

    圖說一定要帶 class="image-caption"，否則整段被隱藏。
    另外主題會給 .image-caption 加 opacity:.65 與 margin: -0.75rem auto 2rem，
    這裡一併覆蓋（opacity 還原、下緣留白歸零），維持深色圖卡上下留白對稱。
    """
    return fig.replace('<figcaption style="',
                       '<figcaption class="image-caption" '
                       'style="opacity:1;margin-bottom:0;', 1)


def strip_figure(text, marker):
    """Remove an existing <!-- FIGn --> ... <!-- /FIGn --> block."""
    start = text.find("<!-- %s -->" % marker)
    if start < 0:
        return text, False
    end = text.find("<!-- /%s -->" % marker, start)
    if end < 0:
        raise SystemExit("unterminated marker: %s" % marker)
    end += len("<!-- /%s -->" % marker)
    # also swallow the blank lines that separated it
    while text[end:end + 2] == "\r\n":
        end += 2
    return text[:start] + text[end:], True


def main():
    text = io.open(POST, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in text else "\n"
    changed = 0
    for slug, marker, anchor, where in PLAN:
        fig = theme_fix(build(slug).figure(CAPTIONS[slug], marker)).replace("\n", nl)

        # If the figure already exists somewhere, drop it first: the anchor may
        # have moved, and we want the figure to land in the new place.
        text, existed = strip_figure(text, marker)
        if existed:
            print("REMOVED         %-5s (re-anchoring)" % marker)

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


if __name__ == "__main__":
    main()
