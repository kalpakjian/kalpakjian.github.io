# -*- coding: utf-8 -*-
"""Rebuild a full message body from the YAML-ish cache of a tool response.

The tool's cached result prints `messageText:` followed by continuation lines
indented 12 spaces (YAML block style). Reading it in page-sized chunks and
joining the continuation lines recovers the exact body, which is the only way to
get a 200 KB payload onto disk without a live MCP call.

    python tools/ainews/_assemble_cached.py --id <messageId> --chunks chunks.txt \
        --subject "..." [--date ...]

`chunks.txt` holds the raw text of the cache pages concatenated (one file so the
shell does not mangle the content).
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import save_message  # noqa: E402

PREFIX = "            "      # 12 spaces: the YAML continuation indent


def extract_body(text):
    """Pull the messageText block out of the pretty-printed YAML."""
    lines = text.split("\n")
    out, started, stopped = [], False, False
    for raw in lines:
        line = raw.rstrip("\r")
        if not started:
            m = re.match(r"^\s+messageText: (.*)$", line)
            if m:
                started = True
                first = m.group(1)
                if first.startswith('"'):
                    first = first[1:]
                out.append(first)
            continue
        if stopped:
            continue
        # a new YAML key at a shallower indent ends the block
        if re.match(r"^\s{0,11}[A-Za-z_]+:", line) and not line.startswith(PREFIX):
            stopped = True
            continue
        if line.startswith(PREFIX):
            out.append(line[len(PREFIX):])
        elif line.strip() == "":
            out.append("")
        else:
            stopped = True
    body = "\n".join(out)
    # the block is a YAML double-quoted scalar: unescape and drop the trailing quote
    body = body.replace('\\r\\n', '\n').replace('\\n', '\n').replace('\\"', '"')
    body = body.replace('\\\\', '\\')
    body = re.sub(r'"\s*$', "", body.rstrip())
    return body


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--chunks", required=True)
    ap.add_argument("--subject", default="")
    ap.add_argument("--date", default="")
    args = ap.parse_args(argv)

    with open(args.chunks, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    body = extract_body(text)
    print("recovered %d chars" % len(body))
    try:
        path, n = save_message.save(args.id, body, args.subject, args.date)
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 1
    print("saved %s (%d chars)" % (path, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
