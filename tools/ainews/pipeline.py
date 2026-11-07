# -*- coding: utf-8 -*-
"""Stage 4d: end-to-end runner -- detect (already done) -> fetch -> extract -> brief -> figures.

This is the "one command" the schedule actually calls. Each stage is also usable
alone; this file only decides ORDER and what to do when a stage says "nothing".

Deliberately NOT included: writing the digest and publishing it. Those need
judgement (see DIGEST_CONTRACT.md §9), so the chain stops at "draft materials".

    python tools/ainews/pipeline.py              # fetch + extract + brief + figures
    python tools/ainews/pipeline.py --skip-fetch # work on already-saved message.json
    python tools/ainews/pipeline.py --qa         # also run the layout check

Exit codes: 0 = nothing new, 2 = produced materials, 1 = a stage failed.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script, *args):
    cmd = [sys.executable, os.path.join(HERE, script)] + list(args)
    print("\n=== %s ===" % " ".join([os.path.basename(script)] + list(args)))
    return subprocess.call(cmd)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="AINews material pipeline.")
    ap.add_argument("--skip-fetch", action="store_true",
                    help="do not touch IMAP; use existing message.json files")
    ap.add_argument("--qa", action="store_true", help="also run the figure layout check")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    produced = False

    if not args.skip_fetch:
        rc = run("fetch_new.py", "--no-chain", *( ["--dry-run"] if args.dry_run else [] ))
        if rc == 1:
            return 1
        if rc == 2:
            produced = True

    rc = run("extract_new.py", *( ["--dry-run"] if args.dry_run else [] ))
    if rc == 1:
        return 1
    if rc == 2:
        produced = True

    if args.dry_run:
        print("\n(dry run: stopping before figures)")
        return 2 if produced else 0

    # figures need a brief; run it for every issue that has one
    import json
    out_root = os.path.join(HERE, "out")
    if os.path.isdir(out_root):
        for name in sorted(os.listdir(out_root)):
            brief = os.path.join(out_root, name, "brief.json")
            if not os.path.exists(brief):
                continue
            rc = run("figures.py", "--brief", brief, "--out", os.path.dirname(brief))
            if rc != 0:
                return 1
            if args.qa:
                html = os.path.join(os.path.dirname(brief), "figures.html")
                if os.path.exists(html):
                    rc = run("_check_fig_layout.py", html)
                    if rc != 0:
                        print("layout check failed for %s" % name, file=sys.stderr)
                        return 1

    return 2 if produced else 0


if __name__ == "__main__":
    sys.exit(main())
