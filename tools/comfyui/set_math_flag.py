"""Add `math: true` to the front-matter of the posts that contain real LaTeX.

Why not install hexo-renderer-mathjax globally?

  * hexo-renderer-mathjax@0.9.0 injects MathJax 2.7.9 into EVERY page,
    which collides with the Fluid theme's own MathJax 3.x injection
    (layout/_partials/plugins/math.ejs).
  * The theme already supports this: with `math.specific: true` a post
    opts in via `math: true` in its front-matter, and the theme then
    loads MathJax 3 with inlineMath = [['$','$']].

Why not enable it everywhere?

  * `$` is also used as a currency sign on this site.  For example
    azure-automl-bank-churn-walkthrough.md has 13 occurrences of things
    like `$0.17/hr`, `US$`, `HK$` and rive-headless-three-routes.md has
    3 more.  Turning on math parsing for those would corrupt them into
    garbled equations.

So: enable it per post, only where the `$` really is LaTeX.

Usage:
    python set_math_flag.py            # add the flag where it is missing
"""
import io
import os
import re
import sys

BASE = r"C:\Users\princ\blog\source\_posts"

# Posts whose `$...$` really is LaTeX.
TARGETS = [
    "linear-regression-notes.md",
    "ml-textbook-notes.md",
]


def add_flag(path):
    raw = io.open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"

    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", raw, re.S)
    if not m:
        print("SKIP (no front-matter): %s" % os.path.basename(path))
        return False

    fm = m.group(1)
    if re.search(r"^math:\s*true", fm, re.M):
        print("OK (already set): %s" % os.path.basename(path))
        return False

    # Insert `math: true` right before `toc:` if present, else at the end of
    # the front-matter block — matching how the other posts are laid out.
    if re.search(r"^toc:\s", fm, re.M):
        new_fm = re.sub(r"^toc:\s", "math: true" + nl + "toc: ", fm, count=1, flags=re.M)
    else:
        new_fm = fm + nl + "math: true"

    new_raw = "---" + nl + new_fm + nl + "---" + nl + raw[m.end():]
    io.open(path, "w", encoding="utf-8", newline="").write(new_raw)
    print("SET math:true -> %s" % os.path.basename(path))
    return True


def main():
    changed = 0
    for name in TARGETS:
        p = os.path.join(BASE, name)
        if not os.path.exists(p):
            print("MISSING: %s" % name)
            continue
        if add_flag(p):
            changed += 1
    print("%d file(s) updated" % changed)
    return 0 if changed else 0


if __name__ == "__main__":
    sys.exit(main())
