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

# ---- positive control for hard check 11 (quiz options must render text) ----
_GOOD_QS = ",".join('{"q":"q%d","o":["a","b","c","d"],"a":0}' % i
                    for i in range(1, 21))
GOOD_QUIZ = (
    '<!DOCTYPE html>\n<html lang="zh-Hant">\n<head><meta charset="utf-8">'
    '<title>Good quiz (QA fixture)</title></head>\n<body>\n<script>\n'
    "const QUESTIONS = [" + _GOOD_QS + "];\n"
    "function renderQuestions(){\n"
    "  let html = '';\n"
    "  for(let i=0;i<QUESTIONS.length;i++){\n"
    "    const q = QUESTIONS[i];\n"
    "    html += '<ul class=\"opts\">';\n"
    "    for(let k=0;k<q.o.length;k++){\n"
    "      html += '<li class=\"opt\" data-q=\"' + i + '\" data-k=\"' + k + '\">';\n"
    "      html += '<span>' + esc(q.o[k]) + '</span></li>';\n"
    "    }\n"
    "    html += '</ul>';\n"
    "  }\n"
    "  return html;\n"
    "}\n"
    "</script>\n</body>\n</html>\n"
)
GOOD_HTML = (
    '<!DOCTYPE html>\r\n<html lang="zh-Hant">\r\n<head><meta charset="utf-8">'
    "<title>Good note (QA fixture)</title></head>\r\n<body>\r\n"
    '<h1 id="good-note">Good \u7b46\u8a18\uff08QA \u6e2c\u8a66\u6a23\u672c\uff09</h1>\r\n'
    "<blockquote>\r\n"
    "\u8ab2\u7a0b\uff1a\u793a\u7bc4\u7528<br />\r\n"
    "\u6a5f\u69cb\uff1a\u793a\u7bc4\u6a5f\u69cb<br />\r\n"
    "\u6db5\u84cb\u6a94\u6848\uff1a<code>demo.pptx</code><br />\r\n"
    "\u672c\u7b46\u8a18\u4f9d\u8ab2\u7a0b\u5927\u7db1\u586b\u5145\u5167\u5bb9\u3002<br />\r\n"
    '<a class="quiz" href="mc-quiz.html">\u4e92\u52d5\u6e2c\u9a57\uff0820 \u984c\uff09</a></p>\r\n'
    "</blockquote>\r\n"
    '<h2 id="1-\u793a\u7bc4\u7ae0\u7bc0">1. \u793a\u7bc4\u7ae0\u7bc0</h2>\r\n'
    "<table><tbody>\r\n"
    '<tr><td>1</td><td><a href="#1-\u793a\u7bc4\u7ae0\u7bc0">'
    "\u793a\u7bc4\u7ae0\u7bc0</a></td></tr>\r\n"
    "</tbody></table>\r\n"
    "<ul><li>\u7b2c\u4e00\u9805</li><li>\u7b2c\u4e8c\u9805</li></ul>\r\n"
    "</body>\r\n</html>\r\n"
)
GOOD_MD = (
    "## 1. \u793a\u7bc4\u7ae0\u7bc0\r\n\r\n"
    "| # | \u7ae0\u7bc0 |\r\n|---|------|\r\n"
    "| 1 | [\u793a\u7bc4\u7ae0\u7bc0](#1-\u793a\u7bc4\u7ae0\u7bc0) |\r\n"
)

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
    good = os.path.join(root, "source", "good-notes")
    tools = os.path.join(root, "tools", "notes-qa")
    for d in (src, orphan, good, tools):
        os.makedirs(d)
    write(os.path.join(src, "index.html"), HTML)
    write(os.path.join(src, "Demo_Study_Notes.md"), MD)
    write(os.path.join(src, "mc-quiz.html"), QUIZ)
    write(os.path.join(orphan, "index.html"), ORPHAN)
    # positive control for the option-text check: a quiz that DOES render the
    # letter + option text, which the gate must accept.
    write(os.path.join(good, "index.html"), GOOD_HTML)
    write(os.path.join(good, "Good_Study_Notes.md"), GOOD_MD)
    write(os.path.join(good, "mc-quiz.html"), GOOD_QUIZ)
    for n in SCRIPTS:
        shutil.copy2(os.path.join(TOOLS_DIR, n), os.path.join(tools, n))
    write(os.path.join(root, "rules.txt"), "IVDC@@@IVDC-ORG\r\n")
    return {
        "html": os.path.join(src, "index.html"),
        "md": os.path.join(src, "Demo_Study_Notes.md"),
        "quiz": os.path.join(src, "mc-quiz.html"),
        "orphan": os.path.join(orphan, "index.html"),
        "good": os.path.join(good, "index.html"),
        "goodquiz": os.path.join(good, "mc-quiz.html"),
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

        # 9) the gate must flag a quiz whose option rows render without text
        #    (the shared shell built '<li class="opt">' but never appended the
        #    letter + option text + '</li>', so readers saw no options at all).
        rc, out = run(os.path.join(TOOLS_DIR, "qa_notes.ps1"),
                      "-Root", os.path.join(TOOLS_DIR, "qa_selftest"),
                      cwd=foreign)
        check("gate flags empty options",
              rc == 1 and "quiz options render without text" in out,
              "rc=%d  %s" % (rc, out))

        # 10) positive control: a quiz that DOES render the option text must
        #     pass, so the new check cannot false-positive on a healthy note.
        rc, out = run(os.path.join(TOOLS_DIR, "qa_notes.ps1"),
                      "-Root", os.path.join(repo, "source"), cwd=foreign)
        check("gate accepts good quiz",
              "PASS  good-notes" in out and "FAIL  good-notes" not in out,
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
