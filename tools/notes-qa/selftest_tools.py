# -*- coding: utf-8 -*-
"""Regression tests for the tools/notes-qa scripts.

Builds a throwaway repo-shaped tree in a temp dir:

    <tmp>/repo/source/demo-notes/index.html          header block, bad id, dup TOC row
    <tmp>/repo/source/demo-notes/Demo_Study_Notes.md
    <tmp>/repo/source/demo-notes/mc-quiz.html        lone LF, for normalize_crlf
    <tmp>/repo/source/not-a-note/index.html          must be ignored (no *_Study_Notes.md)
    <tmp>/repo/tools/notes-qa/<copies of the scripts>
    <tmp>/repo/rules.txt                             for yk_replace2.ps1

then runs each tool from a FOREIGN cwd (so a cwd-based path could never work) and
asserts the expected edit landed. Nothing outside the temp tree is ever written.

Portable: Windows (powershell.exe) and Linux (pwsh); no hardcoded paths.

Usage:
    python tools/notes-qa/selftest_tools.py

Exit code: 0 = every tool behaved, 1 = at least one regression.
"""
from __future__ import annotations

import locale
import os
import shutil
import subprocess
import sys
import tempfile

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = ("regen_ids.ps1", "fix_toc_dup.ps1", "fix_header_br.ps1",
           "yk_replace2.ps1", "normalize_crlf.ps1")

HTML = (
    "<h1>Demo</h1>\r\n"
    "<blockquote>\r\n"
    "<p>\u8ab2\u7a0b\uff1aCertificate in Application of AI (Part-time)</p>\r\n"
    "<p>\u6a5f\u69cb\uff1a\u532f\u7e31\u5c08\u696d\u767c\u5c55\u4e2d\u5fc3\uff08IVDC\uff09</p>\r\n"
    "</blockquote>\r\n"
    '<h2 id="bad id!!">1. AI \u662f\u4ec0\u9ebc</h2>\r\n'
    "<table>\r\n<tr>\r\n<td>1</td>\r\n"
    '<td><a href="#bad id!!">1. AI \u662f\u4ec0\u9ebc</a></td>\r\n'
    "</tr>\r\n</table>\r\n"
)
MD = (
    "## 1. AI \u662f\u4ec0\u9ebc\n\n"
    "| # | \u7ae0\u7bc0 |\n|---|------|\n"
    "| 1 | [1. AI \u662f\u4ec0\u9ebc](#bad id!!) |\n"
)
QUIZ = "const QUESTIONS = [];\n"          # lone LF on purpose
ORPHAN = "<p>no md here</p>\n"            # lone LF, must stay untouched

_results = []


def find_shell():
    for name in ("pwsh", "powershell"):
        p = shutil.which(name)
        if p:
            return p
    raise SystemExit("neither pwsh nor powershell is on PATH")


SHELL = find_shell()
ENC = "utf-8" if os.name != "nt" else locale.getpreferredencoding(False)


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def bytes_of(path):
    with open(path, "rb") as f:
        return f.read()


def build(root):
    """(Re)create the fixture tree and return the paths we assert on."""
    if os.path.isdir(root):
        shutil.rmtree(root)
    src = os.path.join(root, "source", "demo-notes")
    orphan = os.path.join(root, "source", "not-a-note")
    tools = os.path.join(root, "tools", "notes-qa")
    for d in (src, orphan, tools):
        os.makedirs(d)
    write(os.path.join(src, "index.html"), HTML)
    write(os.path.join(src, "Demo_Study_Notes.md"), MD)
    write(os.path.join(src, "mc-quiz.html"), QUIZ)
    write(os.path.join(orphan, "index.html"), ORPHAN)
    for n in SCRIPTS:
        shutil.copy2(os.path.join(TOOLS_DIR, n), os.path.join(tools, n))
    write(os.path.join(root, "rules.txt"), "IVDC@@@IVDC-ORG\r\n")
    return {
        "html": os.path.join(src, "index.html"),
        "md": os.path.join(src, "Demo_Study_Notes.md"),
        "quiz": os.path.join(src, "mc-quiz.html"),
        "orphan": os.path.join(orphan, "index.html"),
        "tools": tools,
        "rules": os.path.join(root, "rules.txt"),
        "root": root,
    }


def run(script, *args, cwd="."):
    """Run a fixture copy of `script`; `cwd` defaults to a foreign directory."""
    cmd = [SHELL, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script]
    cmd += list(args)
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       encoding=ENC, errors="replace")
    out = ((p.stdout or "") + (p.stderr or "")).strip().replace("\n", " | ")
    return p.returncode, out


def check(name, cond, detail=""):
    _results.append(bool(cond))
    print("%s %-20s %s" % ("PASS" if cond else "FAIL", name, detail))


def main():
    tmp = tempfile.mkdtemp(prefix="notes-qa-selftest-")
    repo = os.path.join(tmp, "repo")
    try:
        f = build(repo)
        # foreign cwd: the temp root, which is NOT the fixture repo root
        foreign = tmp

        # 1) regen_ids.ps1 -- bad id and href reslugged, md link synced
        rc, out = run(os.path.join(f["tools"], "regen_ids.ps1"), cwd=foreign)
        h, m = read(f["html"]), read(f["md"])
        check("regen_ids.ps1",
              rc == 0 and 'id="1-ai-' in h and 'href="#1-ai-' in h and "](#1-ai-" in m,
              "rc=%d  %s" % (rc, out))

        # 2) fix_toc_dup.ps1 -- duplicated "1. " dropped from html and md rows
        f = build(repo)
        rc, out = run(os.path.join(f["tools"], "fix_toc_dup.ps1"), cwd=foreign)
        h, m = read(f["html"]), read(f["md"])
        check("fix_toc_dup.ps1",
              rc == 0 and '<td><a href="#bad id!!">AI ' in h and "| 1 | [AI " in m,
              "rc=%d  %s" % (rc, out))

        # 3) fix_header_br.ps1 -- the label line in the header block gets <br />
        f = build(repo)
        rc, out = run(os.path.join(f["tools"], "fix_header_br.ps1"), cwd=foreign)
        check("fix_header_br.ps1", rc == 0 and "<br />" in read(f["html"]),
              "rc=%d  %s" % (rc, out))

        # 4) yk_replace2.ps1 -- rule file applied
        f = build(repo)
        rc, out = run(os.path.join(f["tools"], "yk_replace2.ps1"),
                      "-ruleFile", f["rules"], cwd=foreign)
        check("yk_replace2.ps1", rc == 0 and "IVDC-ORG" in read(f["html"]),
              "rc=%d  %s" % (rc, out))

        # 5) normalize_crlf.ps1 -DryRun -- must report and must NOT write
        f = build(repo)
        rc, out = run(os.path.join(f["tools"], "normalize_crlf.ps1"), "-DryRun",
                      cwd=foreign)
        check("normalize dry run",
              rc == 0 and b"\r" not in bytes_of(f["md"]) and "to fix" in out,
              "rc=%d  %s" % (rc, out))

        # 6) normalize_crlf.ps1 -- fixes lone LF, leaves non-note folders alone
        rc, out = run(os.path.join(f["tools"], "normalize_crlf.ps1"), cwd=foreign)
        quiz = bytes_of(f["quiz"])
        check("normalize real run",
              rc == 0 and b"\r\n" in bytes_of(f["md"])
              and quiz.count(b"\n") == quiz.count(b"\r\n")
              and b"\r" not in bytes_of(f["orphan"]),
              "rc=%d  %s" % (rc, out))

        # 7) idempotent on a second run
        rc, out = run(os.path.join(f["tools"], "normalize_crlf.ps1"), cwd=foreign)
        check("normalize idempotent", rc == 0 and "files fixed = 0" in out,
              "rc=%d  %s" % (rc, out))

        # 8) the gate must still reject the deliberately broken sample
        rc, out = run(os.path.join(TOOLS_DIR, "qa_notes.ps1"),
                      "-Root", os.path.join(TOOLS_DIR, "qa_selftest"), "-Quiet",
                      cwd=foreign)
        check("gate rejects sample", rc == 1 and "failures = 1" in out,
              "rc=%d  %s" % (rc, out))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    if all(_results):
        print("ALL PASS (%d checks)" % len(_results))
        return 0
    print("SOME FAILED (%d/%d)" % (_results.count(False), len(_results)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
