# -*- coding: utf-8 -*-
"""Pre-render LaTeX in a Markdown post to static KaTeX HTML.

Why: the theme's MathJax path renders in the browser (needs JS, causes a
flash of unstyled math, and pulls a CDN script). KaTeX output is plain
HTML + inline CSS, so rendering it at build time gives professional math
typography with zero runtime JavaScript and zero external requests.

The KaTeX stylesheet is inlined into the post's first use, so the page
still has no external resources.

Usage:
    python katex_pre.py <post.md>            # render in place
    python katex_pre.py <post.md> --check    # report only
"""
import base64
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NODE = r"C:\Program Files\nodejs\node.exe"
RENDER_JS = os.path.join(HERE, "katex_render.js")
KATEX_CSS = os.path.join(os.path.dirname(HERE), "..", "..", "node_modules",
                         "katex", "dist", "katex.min.css")
FONTS_DIR = os.path.join(os.path.dirname(KATEX_CSS), "fonts")
FONT_FILES = set(f[:-len(".woff2")] for f in os.listdir(FONTS_DIR)
                 if f.endswith(".woff2"))

# Block math: $$...$$ and \[...\] ; then inline $...$ and \(...\).
BLOCK_RE = re.compile(r"\$\$(.+?)\$\$|\\\[(.+?)\\\]", re.S)
INLINE_RE = re.compile(r"(?<![\$\w])\$([^$\n]+?)\$(?!\$)|\\\((.+?)\\\)")

# Don't touch anything inside a fenced code block or an existing <svg>.
FENCE_RE = re.compile(r"(?s)```.*?```")


def split_segments(text):
    """Yield (is_code, chunk) so we only touch prose."""
    pos = 0
    for m in FENCE_RE.finditer(text):
        if m.start() > pos:
            yield (False, text[pos:m.start()])
        yield (True, m.group(0))
        pos = m.end()
    if pos < len(text):
        yield (False, text[pos:])


def collect(text):
    """Find every math span in the prose, return (spans, template)."""
    spans = []
    out = []
    counter = [0]

    for is_code, chunk in split_segments(text):
        if is_code:
            out.append(chunk)
            continue

        # block math
        def blk(m):
            counter[0] += 1
            key = "b%d" % counter[0]
            tex = (m.group(1) if m.group(1) is not None else m.group(2)).strip()
            spans.append({"id": key, "tex": tex, "display": True})
            return "\x00MATH:%s\x00" % key
        chunk = BLOCK_RE.sub(blk, chunk)

        # inline math
        def inl(m):
            counter[0] += 1
            key = "i%d" % counter[0]
            tex = (m.group(1) if m.group(1) is not None else m.group(2)).strip()
            spans.append({"id": key, "tex": tex, "display": False})
            return "\x00MATH:%s\x00" % key
        chunk = INLINE_RE.sub(inl, chunk)

        out.append(chunk)

    return spans, "".join(out)


def render(spans):
    if not spans:
        return {}
    payload = json.dumps({"items": spans})
    p = subprocess.run([NODE, RENDER_JS], input=payload, capture_output=True,
                       text=True, encoding="utf-8", timeout=120)
    if p.returncode != 0:
        raise RuntimeError("katex_render.js failed: %s" % p.stderr[:500])
    data = json.loads(p.stdout)
    res = {}
    for r in data["results"]:
        if r.get("error"):
            print("  !! katex error on %s: %s" % (r["id"], r["error"]))
            res[r["id"]] = None
            continue
        html = r.get("html") or ""
        # KaTeX does NOT throw on a bad expression — it returns a red
        # <span class="katex-error"> instead. Treat that as a failure,
        # otherwise the broken formula silently ships to the page.
        if 'class="katex-error"' in html:
            title = re.search(r'katex-error" title="([^"]*)"', html)
            print("  !! katex parse error on %s: %s"
                  % (r["id"], title.group(1) if title else "unknown"))
            res[r["id"]] = None
            continue
        res[r["id"]] = html
    return res


def collect_fonts(html):
    """Return the set of KaTeX font families referenced by the rendered math."""
    fams = set()
    for m in re.finditer(r"font-family:\s*(KaTeX_[A-Za-z]+)", html):
        fams.add(m.group(1))
    return fams


def font_files_for(fams, fonts_dir):
    """Map font families to the woff2 files that provide them.

    KaTeX names its files KaTeX_<Family>-<Style>.woff2, where the family in
    the CSS is the part after 'KaTeX_'. We match on that prefix.
    """
    want = {}
    for fam in fams:
        base = "KaTeX_" + fam.split("_", 1)[1] if fam.count("_") > 1 else fam
        want[fam] = base
    files = {}
    for f in sorted(os.listdir(fonts_dir)):
        if not f.endswith(".woff2"):
            continue
        stem = f[:-len(".woff2")]
        for fam, base in want.items():
            if stem.startswith(base):
                files.setdefault(fam, []).append(os.path.join(fonts_dir, f))
    return files


def data_uri(path):
    with open(path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    return "data:font/woff2;base64," + b64


def inline_fonts(css, fonts_dir, needed=None):
    """Rewrite the @font-face src url() references to data URIs.

    `needed` is an optional set of file stems (e.g. {"KaTeX_Main-Regular"})
    to embed. When given, only those are inlined; the rest are dropped from
    the stylesheet entirely so the page makes no request for them.
    """
    used = {}

    def repl(m):
        url = m.group(1)
        fname = os.path.basename(url)
        stem = fname[:-len(".woff2")] if fname.endswith(".woff2") else fname
        if needed is not None and stem not in needed:
            return "src:local(%s)" % stem
        full = os.path.join(fonts_dir, fname)
        if not os.path.exists(full):
            return m.group(0)
        used[fname] = full
        return "src:url(%s) format('woff2')" % data_uri(full)

    out = re.sub(r"src:url\((fonts/[^)]+)\)", repl, css)
    return out, used


def font_stems_for(html, fonts_dir, css=""):
    """Which KaTeX font files does this article's math actually need?

    Static CSS reasoning is unreliable: KaTeX binds families to classes via
    several overlapping rules (.mathnormal -> KaTeX_Math italic, .mord ->
    KaTeX_Main normal, ...). Rather than guess, we take the list of
    (family, weight, style) triples that a real browser reported while
    rendering the page, and map each to its @font-face file.

    The probe writes a JSON like:
        {"KaTeX_Main": {"400/normal": 79}, "KaTeX_Math": {"400/italic": 13}}

    which maps to KaTeX_Main-Regular.woff2 and KaTeX_Math-Italic.woff2.
    """
    faces = load_face_probe()
    if not faces:
        # No probe available: fall back to the two faces KaTeX uses for
        # ordinary maths, which covers Latin letters, digits and accents.
        faces = {"KaTeX_Main": {"400/normal": 1}, "KaTeX_Math": {"400/italic": 1}}

    stems = set()
    for fam, variants in faces.items():
        for variant in variants:
            weight, style = variant.split("/")
            # KaTeX file names: KaTeX_<Family>-Regular / -Bold / -Italic /
            # -BoldItalic. Note KaTeX_Math only ships an Italic face.
            base = fam
            if weight in ("700", "800", "900", "bold"):
                base += "-Bold"
            else:
                base += "-Regular"
            if style in ("italic", "oblique"):
                # KaTeX_Math-Regular does not exist; its only face is Italic.
                if base.endswith("-Regular") and (base + "Italic") not in FONT_FILES:
                    base = base[:-len("Regular")] + "Italic"
                else:
                    base += "Italic"
            if base in FONT_FILES:
                stems.add(base)
    return stems, set(faces.keys())


# probe output: family -> {"weight/style": count}
FACE_PROBE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "katex_faces.json")


def load_face_probe():
    """Read the browser-measured face list, if the probe has been run."""
    if not os.path.exists(FACE_PROBE):
        return {}
    try:
        return json.load(io.open(FACE_PROBE, encoding="utf-8"))
    except Exception:
        return {}


def available_fonts(fonts_dir):
    """Set of KaTeX font stems available on disk."""
    return set(f[:-len(".woff2")] for f in os.listdir(fonts_dir)
               if f.endswith(".woff2"))


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    path = sys.argv[1]
    check_only = "--check" in sys.argv

    raw = io.open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"

    spans, template = collect(raw)
    print("found %d math span(s):" % len(spans))
    for s in spans:
        print("   %-4s display=%-5s %s" % (s["id"], s["display"], s["tex"][:60]))

    if not spans:
        print("nothing to do")
        return 0

    rendered = render(spans)
    ok = [k for k, v in rendered.items() if v]
    print("rendered %d/%d" % (len(ok), len(spans)))
    if len(ok) != len(spans):
        print("some spans failed — aborting without writing")
        return 1

    if check_only:
        return 0

    # substitute back
    def sub(m):
        return rendered[m.group(1)]

    result = re.sub(r"\x00MATH:([bi]\d+)\x00", sub, template)

    # KaTeX's HTML may contain bare LF. The repo pins *.md to CRLF, so
    # normalise every line ending before writing.
    result = result.replace("\r\n", "\n").replace("\n", nl)

    # Inline the KaTeX stylesheet once, right after the front-matter.
    # The fonts are embedded as data URIs so the page makes no external
    # request at all — this site does not ship CDN dependencies.
    if "<style id=\"katex-inline\">" not in result:
        css = io.open(KATEX_CSS, encoding="utf-8").read()
        fonts_dir = os.path.join(os.path.dirname(KATEX_CSS), "fonts")
        # Only embed the faces the rendered math actually references.
        stems, fams = font_stems_for("".join(rendered.values()), fonts_dir, css)
        css, used = inline_fonts(css, fonts_dir, needed=stems)
        print("font families used : %s" % ", ".join(sorted(fams)))
        print("embedded %d font file(s), +%d KB"
              % (len(used), sum(os.path.getsize(p) for p in used.values()) // 1024))
        # keep CRLF: the repo's .gitattributes pins *.md to eol=crlf, and a
        # lone-LF inside the CSS block would trip the QA gate.
        css = css.replace("\r\n", "\n").replace("\n", "\r\n")
        block = ('<style id="katex-inline">\r\n%s\r\n</style>\r\n' % css)
        m = re.search(r"^---\r?\n.*?\r?\n---\r?\n", result, re.S)
        if m:
            result = result[:m.end()] + nl + block + result[m.end():]
        else:
            result = block + result

    io.open(path, "w", encoding="utf-8", newline="").write(result)
    print("written -> %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
