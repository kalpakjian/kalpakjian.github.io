# -*- coding: utf-8 -*-
"""Inventory of ASCII-art diagram blocks still to convert.

A fresh session should run this FIRST: it reports the live state instead of
relying on a status list that goes stale.

Usage:
    python inventory.py                    # per-note summary (remaining vs done)
    python inventory.py <note-dir>         # list that note's art blocks
    python inventory.py <note-dir> <n>     # dump block n (1-based among art blocks)
"""
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(REPO, "source")
BOX = "┌─┐│└┘├┤┬┴┼╔╗╚╝║═"
# 門檻 6：真正的樹狀/流程圖最少只用到 6 個框線字元（例如「├─」三個 × 兩列）。
# 先前用 8 會漏掉 6 張真圖（ai-intro / llm-intro / local-llm / tpot / neural-network /
# ai-model-factory），全部是小而關鍵的樹狀圖。
MIN_BOX = 6


def art_blocks(text):
    """[(body, first_line, lines, box_chars)] for every fenced block with box art."""
    out = []
    for m in re.finditer(r"(?s)```[a-z]*\r?\n(.*?)```", text):
        body = m.group(1)
        n = sum(1 for ch in body if ch in BOX)
        if n < MIN_BOX:
            continue
        lines = [l for l in body.split("\n") if l.strip()]
        out.append((body, lines[0].strip() if lines else "", len(lines), n))
    return out


CODE_HINT = re.compile(
    r"^\s*(#|//|\$|>|cd |pip |pip3 |python |python3 |java |npx |npm |curl |wget |"
    r"ollama |streamlit |docker |git |export |import |from |def |class |uvicorn |"
    r"flask |SET |set |PS |C:\\|~/)")


def is_code_block(body):
    """True when the box chars are only decorative separators inside a code block.

    Example that must NOT be converted (streamlit-flask-notes):
        # ── 終端機 1：Ollama ──
        ollama serve
    Converting it to an image would destroy copy-pasteable commands.
    """
    lines = [l for l in body.split("\n") if l.strip()]
    if not lines:
        return False
    hits = sum(1 for l in lines if CODE_HINT.match(l))
    return hits >= 2 and hits / float(len(lines)) >= 0.5


def notes():
    for p in sorted(glob.glob(os.path.join(SRC, "*", "*Study_Notes.md"))):
        yield os.path.basename(os.path.dirname(p)), p


def main():
    if len(sys.argv) == 1:
        done, todo = [], []
        for note, p in notes():
            blocks = art_blocks(io.open(p, encoding="utf-8").read())
            real = [b for b in blocks if not is_code_block(b[0])]
            skipped = len(blocks) - len(real)
            (todo if real else done).append((note, len(real), skipped))
        print("無待轉圖區塊: %d 份（含本來就沒有圖的筆記）" % len(done))
        for n, _, skip in done:
            print("   %-30s %s" % (n, "(跳過 %d 個裝飾性程式碼區塊)" % skip if skip else ""))
        print("\n仍待轉換: %d 份 / %d 個圖區塊"
              % (len(todo), sum(t[1] for t in todo)))
        for n, real, skip in sorted(todo, key=lambda x: -x[1]):
            print("   %-30s %2d 圖%s" % (n, real, "（另跳過 %d 裝飾）" % skip if skip else ""))
        print("\n用法: python inventory.py <note-dir>        # 列出該筆記的圖區塊")
        print("      python inventory.py <note-dir> <n>    # 印出第 n 個（1-based）")
        return 0

    note = sys.argv[1]
    p = os.path.join(SRC, note, [f for f in os.listdir(os.path.join(SRC, note))
                                 if f.endswith("Study_Notes.md")][0])
    blocks = art_blocks(io.open(p, encoding="utf-8").read())
    real = [b for b in blocks if not is_code_block(b[0])]
    if len(sys.argv) > 2:
        i = int(sys.argv[2]) - 1
        print(real[i][0])
        return 0
    print("%s: %d 個真圖區塊（另有 %d 個裝飾性區塊，通常不用轉）"
          % (note, len(real), len(blocks) - len(real)))
    for i, (body, first, nlines, nbox) in enumerate(real, 1):
        print("  art#%-2d %3d 行 %4d 框  %s" % (i, nlines, nbox, first[:60]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
