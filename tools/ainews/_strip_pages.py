# -*- coding: utf-8 -*-
"""Turn paged read_files output into a plain body file.

read_files prefixes every line with " NNN | ", which is what makes paging
lossless but also unusable as-is. This strips the prefix and removes the YAML
continuation indent, then writes body.txt for save_message.py.

    python tools/ainews/_strip_pages.py --in pages.txt --out body.txt
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LINE = re.compile(r"^\s*\d+\s\|\s?(.*)$")
INDENT = "            "      # 12 spaces of YAML block indent


def strip(text):
    out = []
    for raw in text.split("\n"):
        m = LINE.match(raw)
        line = m.group(1) if m else raw
        line = line.rstrip("\r")
        if line.startswith(INDENT):
            out.append(line[len(INDENT):])
        elif line.strip() == "":
            out.append("")
        else:
            out.append(line)
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="dst", required=True)
    args = ap.parse_args(argv)
    with open(args.src, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    body = strip(text)
    n = len(body)
    with open(args.dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print("wrote %s (%d chars)" % (args.dst, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
