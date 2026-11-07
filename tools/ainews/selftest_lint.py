# -*- coding: utf-8 -*-
"""Regression tests for tools/ainews/digest_lint.py (stage 3 gate).

The gate has two jobs that pull in opposite directions:

  * catch real defects (missing sections, no figures, numbers not in the source)
  * NOT cry wolf on the posts already published -- a gate that fails good work
    gets disabled, and then it protects nothing

Both are tested, plus the specific regressions found while building it:

  t1  a published digest passes with 0 errors (golden sample)
  t2  a digest missing "## 我的判讀" fails
  t3  a digest with fewer figures than the floor fails
  t4  a fabricated bolded number fails fidelity (F001)
  t5  a number that IS in the source passes fidelity
  t6  frontmatter written as `- item` lists is understood (S006 regression)
  t7  numbered headings ("## 2. 我的判讀：...") satisfy the section check
  t8  SVG with column-0 blank lines is NOT flagged (S010 regression)
  t9  SVG with 4-space-indented inline elements after a blank IS flagged
  t10 odd number of `**` is an error

Usage: python tools/ainews/selftest_lint.py   (exit 0 = all passed)
"""
import io
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import digest_lint as dl  # noqa: E402

FAILS = []
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

FIG = ('<!-- FIG{n} -->\n<figure><svg xmlns="http://www.w3.org/2000/svg" '
       'viewBox="0 0 940 400"><rect x="0" y="0" width="100" height="50"/>\n'
       '<text x="1" y="2">x</text></svg><figcaption>圖：說明</figcaption></figure>\n')
TABLE = "| a | b |\n|---|---|\n| 1 | 2 |\n"


def check(name, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + name + ("" if cond else "  " + str(detail)))
    if not cond:
        FAILS.append(name)


def nums(bold):
    return "| 指標 | 值 |\n|---|---|\n| ARC-AGI-2 | %s |\n" % bold


def make_post(tmpdir, figs=2, tables=5, fabricate=False):
    figs_html = "".join(FIG.format(n=i + 1) for i in range(figs))
    tables_md = TABLE * tables
    bold = "**12345%**" if fabricate else "**81.7%**"
    body = (
        "---\ntitle: t\ndate: 2026-11-07 20:30:00\n"
        "categories:\n  - A\ntags:\n  - x\n"
        "index_img: /img/c.png\nbanner_img: /img/c.png\n---\n\n"
        "## 一句話總結\n\n這是摘要。\n\n"
        "## 1. 頭條\n\n" + "內容" * 400 + "\n\n" + nums(bold) + "\n\n" + figs_html + "\n"
        + tables_md + "\n"
        "## 2. 我的判讀：一句主張\n\n" + "判讀" * 400 + "\n\n" + figs_html + "\n"
        "## 3. 速覽\n\n" + "速覽" * 300 + "\n\n" + tables_md + "\n"
        "## 4. 深入\n\n" + "深入" * 400 + "\n\n" + figs_html + "\n"
        "## 5. 我的總結\n\n" + "總結" * 200 + "\n"
    )
    p = os.path.join(tmpdir, "post.md")
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(body)
    return p


def main():
    # t1: the two published posts must be error-free (golden samples)
    for name in ("ainews-weight-space-programming-zh.md",
                 "ainews-anthropic-ipo-whither-now-zh.md"):
        p = os.path.join(ROOT, "source", "_posts", name)
        if not os.path.exists(p):
            continue
        errs = [x for x in dl.lint(p) if x.level == dl.ERROR]
        check("t1 published post passes: %s" % name[:30], not errs,
              [x.msg[:70] for x in errs])

    # t2: missing required section
    with tempfile.TemporaryDirectory() as d:
        p = make_post(d)
        body = io.open(p, encoding="utf-8").read().replace("## 2. 我的判讀", "## 2. 別的東西")
        io.open(p, "w", encoding="utf-8").write(body)
        errs = [x for x in dl.lint(p) if x.level == dl.ERROR]
        check("t2 missing 我的判讀 is caught",
              any(x.code == "S001" for x in errs), [x.code for x in errs])

    # t3: too few figures
    with tempfile.TemporaryDirectory() as d:
        p = make_post(d, figs=0)
        errs = [x for x in dl.lint(p) if x.level == dl.ERROR]
        check("t3 missing figures is caught",
              any(x.code == "S004" for x in errs), [x.code for x in errs])

    # t4/t5: fidelity against a source
    with tempfile.TemporaryDirectory() as d:
        src = {"lede": "ARC-AGI-2 scored 81.7% on the benchmark.",
               "sections": [{"text": "The model has 594B total params.", "subsections": []}]}
        sp = os.path.join(d, "extract.json")
        with io.open(sp, "w", encoding="utf-8") as f:
            json.dump(src, f)

        p_ok = make_post(d, fabricate=False)
        errs = [x for x in dl.lint(p_ok, sp) if x.level == dl.ERROR]
        check("t5 number present in source passes fidelity",
              not any(x.code == "F001" for x in errs), [x.msg[:60] for x in errs])

        p_bad = make_post(d, fabricate=True)
        errs = [x for x in dl.lint(p_bad, sp) if x.level == dl.ERROR]
        check("t4 fabricated number fails fidelity",
              any(x.code == "F001" for x in errs), [x.code for x in errs])

    # t6: list-form frontmatter
    meta, _ = dl.split_frontmatter(
        "---\ntitle: t\ndate: 2026-01-01\ncategories:\n  - A\ntags:\n  - x\n---\nbody\n")
    check("t6 list frontmatter parsed",
          dl._has_list(meta, "categories") and dl._has_list(meta, "tags"), meta)

    # t7: numbered headings satisfy the section requirement
    with tempfile.TemporaryDirectory() as d:
        p = make_post(d)
        errs = [x for x in dl.lint(p) if x.level == dl.ERROR]
        check("t7 numbered headings accepted",
              not any(x.code == "S001" for x in errs), [x.msg[:50] for x in errs])

    # t8: column-0 blank line inside svg must NOT be flagged
    f = dl.check_svg(FIG.format(n=1))
    check("t8 column-0 svg not flagged",
          not any(x.code == "S010" for x in f), [x.msg for x in f])

    # t9: indented inline element after a blank line IS flagged
    svg_bad = ("<svg xmlns='http://www.w3.org/2000/svg'>\n<rect x='0' y='0'/>\n\n"
               "    <text x='1' y='2'>x</text>\n</svg>")
    f = dl.check_svg(svg_bad)
    check("t9 indented svg line flagged",
          any(x.code == "S010" for x in f), [x.msg for x in f])

    # t10: unclosed bold
    f = dl.check_bold("這是 **沒有閉合的粗體")
    check("t10 odd delimiters flagged",
          any(x.code == "S021" for x in f), [x.msg for x in f])

    print("\n%s (%d failed)" % ("ALL PASSED" if not FAILS else "FAILURES: " + ", ".join(FAILS), len(FAILS)))
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
