# -*- coding: utf-8 -*-
"""Rebuild a note page from its markdown while keeping the existing page shell.

The cnn-notes page has no builder script left in the repo (its docstring points at
a `notes_to_html.py` that no longer exists), so instead of re-creating the whole
template we only replace the two generated regions: the sidebar TOC and <main>.
CSS, nav links, titles and footers stay exactly as they are.

    python rebuild_notes_from_md.py cnn-notes CNN_Study_Notes.md
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_cnn2_notes import build_toc, md_to_html  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def rebuild(dir_name, md_name):
    md_path = os.path.join(REPO, "source", dir_name, md_name)
    html_path = os.path.join(REPO, "source", dir_name, "index.html")
    md = io.open(md_path, encoding="utf-8").read()
    html = io.open(html_path, encoding="utf-8").read()

    body, headings = md_to_html(md)

    # 1) sidebar TOC: everything between <div class="toc"> and the </div> that closes it
    start = html.index('<div class="toc">') + len('<div class="toc">')
    end = html.rindex("</div>", start, html.index("</nav>"))
    html = html[:start] + "\n" + build_toc(headings) + "\n  " + html[end:]

    # 2) main content
    m0 = html.index("<main>") + len("<main>")
    m1 = html.index("</main>")
    html = html[:m0] + "\n" + body + "\n" + html[m1:]

    io.open(html_path, "w", encoding="utf-8", newline="\n").write(html)
    print(f"{dir_name}: {len(headings)} headings -> {len(html):,} chars")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: rebuild_notes_from_md.py <dir> <md file>")
    rebuild(sys.argv[1], sys.argv[2])
