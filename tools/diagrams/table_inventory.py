# -*- coding: utf-8 -*-
"""Inventory of quantitative markdown tables that would read better as a chart.

Companion to `inventory.py`:

    inventory.py        -> ASCII box-art blocks that should become SVG diagrams
    table_inventory.py  -> tables whose columns are mostly numbers (bar / line chart)

A table is reported when it has

    * at least 3 body rows,
    * at least one label column (mostly text), and
    * at least one numeric column (>= 70% of its cells parse as a number).

Usage:
    python table_inventory.py               # ranked candidates across every note
    python table_inventory.py <note-dir>    # one note, with section headings
    python table_inventory.py --all         # include tables that score below 3 rows
"""
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(REPO, "source")

NUM = re.compile(
    r"^[~≈<>]?\s*[-+]?\d[\d,]*(\.\d+)?\s*(%|pp|分|分鐘|ms|s|×|x|M|K|GB|MB|維)?$")
SEP = re.compile(r"^\|[\s:\-|]+\|$")
HEAD = re.compile(r"^(#{2,4})\s+(.*)$")

# 「目錄／索引／對照表」不是量化比較，轉成圖表沒有意義。
SKIP_SECTION = re.compile(r"目錄|索引|對照|總表|速查|清單|一覽|總覽")
# 這些欄位是「序號」不是「量測值」。
INDEX_HEADERS = {"#", "no", "no.", "編號", "序號", "排名", "章", "章節", "§",
                 "步驟", "個案", "pdf 頁", "頁", "頁碼", "單元", "lesson", "unit"}


def clean(cell):
    c = cell.strip()
    c = re.sub(r"\*\*|`|<[^>]+>", "", c)
    return c.strip()


def split_row(line):
    return [clean(c) for c in line.strip().strip("|").split("|")]


def tables(md):
    """[(section, header, rows)] for every markdown table in the file."""
    out, section, lines = [], "(前言)", md.split("\n")
    i = 0
    while i < len(lines):
        m = HEAD.match(lines[i])
        if m:
            section = m.group(2).strip()
            i += 1
            continue
        if lines[i].startswith("|") and i + 1 < len(lines) and SEP.match(lines[i + 1]):
            header = split_row(lines[i])
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            out.append((section, header, rows))
            continue
        i += 1
    return out


def looks_like_index(name, cells):
    if name.strip().lower() in INDEX_HEADERS:
        return True
    # 1,2,3,... 這種連號欄位是序號，不是量測值。
    vals = []
    for x in cells:
        try:
            vals.append(int(x.replace(",", "")))
        except ValueError:
            return False
    return vals == list(range(1, len(vals) + 1))


def analyse(header, rows):
    ncol = len(header)
    rows = [r for r in rows if len(r) == ncol]
    if not rows:
        return None
    numeric, labels = [], []
    for c in range(ncol):
        cells = [r[c] for r in rows if r[c]]
        if not cells:
            continue
        hits = sum(1 for x in cells if NUM.match(x))
        share = hits / float(len(cells))
        if share >= 0.7 and not looks_like_index(header[c], cells):
            numeric.append((header[c], share, hits, len(cells)))
        elif share < 0.7:
            labels.append((header[c], share, hits, len(cells)))
    if not numeric or not labels:
        return None
    score = len(rows) * max(n[1] for n in numeric) * len(numeric)
    return {"rows": len(rows), "numeric": numeric, "labels": labels, "score": score}


def main():
    only = None
    show_all = False
    for a in sys.argv[1:]:
        if a == "--all":
            show_all = True
        else:
            only = a

    picked, scanned, total = [], 0, 0
    for p in sorted(glob.glob(os.path.join(SRC, "*", "*Study_Notes.md"))):
        note = os.path.basename(os.path.dirname(p))
        if only and note != only:
            continue
        scanned += 1
        md = io.open(p, encoding="utf-8").read()
        for section, header, rows in tables(md):
            total += 1
            if SKIP_SECTION.search(section):
                continue
            info = analyse(header, rows)
            if not info:
                continue
            if info["rows"] < 3 and not show_all:
                continue
            picked.append((info["score"], note, section, header, info))

    picked.sort(key=lambda x: (-x[0], x[1], x[2]))
    print("掃描 %d 份筆記、%d 張表格，其中 %d 張是量化比較（可考慮轉圖表）\n"
          % (scanned, total, len(picked)))
    for score, note, section, header, info in picked:
        nums = "、".join("%s %.0f%%" % (h, s * 100) for h, s, _, _ in info["numeric"])
        print("%-28s %2d 列  %s" % (note, info["rows"], " | ".join(header)[:64]))
        print("%-28s        §%s" % ("", section[:60]))
        print("%-28s        數值欄：%s" % ("", nums))
    if not picked:
        print("沒有符合條件的表格。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
