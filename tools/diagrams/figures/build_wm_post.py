"""Rebuild the xr-vs-world-model post from its clean base.

Order matters:
  1. restore the clean markdown (source of truth: _work/post_backup.md)
  2. embed the SVG figures
  3. pre-render the LaTeX to static KaTeX HTML

Step 3 rewrites the whole file, so it has to run last — otherwise the
figures would be wiped.

Usage:  python tools/diagrams/figures/build_wm_post.py
"""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BLOG = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
POST = os.path.join(BLOG, "source", "_posts", "xr-vs-world-model.md")
BASE = os.path.join(HERE, "xr-vs-world-model.base.md")
PY = sys.executable


def run(script, *args):
    cmd = [PY, script] + list(args)
    print("\n$ %s" % " ".join(os.path.basename(c) for c in cmd))
    r = subprocess.run(cmd, cwd=os.path.dirname(script), capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (("\n[stderr]\n" + r.stderr) if r.stderr else "")
    print(out.strip()[-1500:])
    if r.returncode != 0:
        raise SystemExit("FAILED: %s (exit %d)" % (script, r.returncode))


def main():
    # 1. restore the clean markdown
    if not os.path.exists(BASE):
        raise SystemExit("missing clean base: %s" % BASE)
    with io.open(BASE, encoding="utf-8", newline="") as fh:
        base = fh.read()
    with io.open(POST, "w", encoding="utf-8", newline="") as fh:
        fh.write(base)
    print("restored clean base -> %s" % POST)

    # 2. figures
    run(os.path.join(HERE, "embed_wm.py"))

    # 3. math (must be last: it rewrites the file)
    run(os.path.join(HERE, "katex_pre.py"), POST)

    print("\nOK: post rebuilt with figures + static KaTeX math")


if __name__ == "__main__":
    main()
