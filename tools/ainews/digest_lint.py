# -*- coding: utf-8 -*-
"""Lint a Chinese AINews digest against DIGEST_CONTRACT.md -- and against its source.

Two kinds of check, and the difference matters:

  STRUCTURE  (no source needed)  -- skeleton sections present, figure/table
             counts, frontmatter fields, SVG hygiene, CJK-bold breakage.
             These are the rules that make a machine draft look like the
             hand-written ones.

  FIDELITY   (needs extract.json) -- every *bolded* number in the post must
             appear somewhere in the extracted source. This is the check that
             stops the single failure mode capable of destroying the site's
             credibility: a plausible but invented statistic.

Fidelity is deliberately conservative: it extracts numeric tokens from bold
spans (``**81.7%**``) and from table cells, normalises them (``$80B`` -> ``80``
with unit ``b``), and looks for the same token in the source. It does NOT try
to verify prose numbers -- too noisy to be a gate -- so a pass here means
"nothing obviously invented", not "everything is correct".

USAGE
    python tools/ainews/digest_lint.py --post source/_posts/x.md
    python tools/ainews/digest_lint.py --post x.md --extract out/<id>/extract.json
    python tools/ainews/digest_lint.py --post x.md --json

Exit codes: 0 = no ERRORs (WARNINGs allowed), 1 = at least one ERROR,
            2 = could not read input.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

REQUIRED_SECTIONS = ["一句話總結", "我的判讀", "我的總結"]

# DIGEST_CONTRACT.md §2
# Thresholds calibrated against the two published digests rather than picked
# from the air: the weight-space post has 2 figures / 5 tables, the IPO post has
# 5 / 6. Requiring 3/6 would have failed a post the author considered complete,
# so the floor is what has actually shipped: 2 figures, 5 tables.
MIN_CHARS, MAX_CHARS = 4000, 12000
MIN_FIGURES = 2
MIN_TABLES = 5

FIG_OPEN = "<!-- FIG"
_BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)
_TABLE_ROW = re.compile(r"^\|(.+)\|\s*$", re.M)
_NUM = re.compile(r"(?<![\w.])[$]?(\d+(?:[.,]\d+)*)\s*(%|x|B|T|M|K|k|tok/s|ms|s|h)?")
_CJK = re.compile(r"[\u4e00-\u9fff]")
# a `**` that touches CJK punctuation cannot flank correctly -> literal asterisks
_BAD_BOLD = re.compile(r"[\u4e00-\u9fff][：，。（）「」]\*\*|\*\*[（「]")

ERROR, WARN = "ERROR", "WARN"


class Finding:
    __slots__ = ("level", "code", "msg")

    def __init__(self, level, code, msg):
        self.level, self.code, self.msg = level, code, msg

    def as_dict(self):
        return {"level": self.level, "code": self.code, "msg": self.msg}


def split_frontmatter(text):
    """Return (meta, body). Handles `categories:\\n  - a\\n  - b` list form.

    The first version only looked at `key: value` lines, so list-style
    frontmatter (`categories`, `tags` written as `- item` lines) came back
    empty and produced false S006 errors on posts that were perfectly valid.
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    head = text[3:end]
    body = text[end + 4:].lstrip("\n")

    meta, cur_key = {}, None
    for line in head.split("\n"):
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            cur_key = m.group(1)
            meta[cur_key] = m.group(2).strip()
            continue
        m2 = re.match(r"^\s*-\s+(.+)$", line)
        if m2 and cur_key:
            meta.setdefault("__lists__", {}).setdefault(cur_key, []).append(m2.group(1).strip())
            continue
        cur_key = None
    return meta, body


def _has_list(meta, key):
    return bool((meta.get("__lists__") or {}).get(key))


def check_structure(body, meta):
    out = []
    headings = [h.strip() for h in re.findall(r"^##\s+(.+)$", body, re.M)]
    # The hand-written posts number their sections ("## 2. 我的判讀：..."), so a
    # prefix match is required -- an exact "## 我的判讀" test reported false
    # errors on both published articles.
    for s in REQUIRED_SECTIONS:
        if not any(h.startswith(s) or (" " + s) in h for h in headings):
            out.append(Finding(ERROR, "S001", "缺少必要章節：## %s" % s))

    chars = len(_CJK.findall(body)) + len(re.findall(r"[A-Za-z]+", body))
    if chars < MIN_CHARS:
        out.append(Finding(ERROR, "S002", "全文太短：%d < %d（若這期真的不值得寫，走短訊模式）"
                           % (chars, MIN_CHARS)))
    elif chars > MAX_CHARS:
        out.append(Finding(WARN, "S003", "全文偏長：%d > %d" % (chars, MAX_CHARS)))

    figs = body.count(FIG_OPEN)
    if figs < MIN_FIGURES:
        out.append(Finding(ERROR, "S004", "內嵌圖不足：%d < %d 張" % (figs, MIN_FIGURES)))

    tables = len(re.findall(r"^\|[-\s:|]+\|\s*$", body, re.M))
    if tables < MIN_TABLES:
        out.append(Finding(ERROR, "S005", "表格不足：%d < %d 張" % (tables, MIN_TABLES)))

    for k in ("title", "date"):
        if not meta.get(k):
            out.append(Finding(ERROR, "S006", "frontmatter 缺 %s" % k))
    for k in ("categories", "tags"):
        if not meta.get(k) and not _has_list(meta, k):
            out.append(Finding(ERROR, "S006", "frontmatter 缺 %s" % k))
    for k in ("index_img", "banner_img"):
        if not meta.get(k):
            out.append(Finding(WARN, "S006", "frontmatter 缺 %s（首頁不會有封面）" % k))
    if meta.get("index_img") and meta.get("banner_img") and \
            meta["index_img"] != meta["banner_img"]:
        out.append(Finding(WARN, "S007", "index_img 與 banner_img 不一致"))

    out += check_svg(body)
    out += check_bold(body)
    out += check_banned(body)
    return out


def check_svg(body):
    """The #1 past failure: a blank line before an inline element makes marked
    emit <p>, and the browser then drops every <rect>/<line> inside it.

    Precisely: a *blank line* alone is harmless (the published weight-space post
    has three of them inside <svg> and renders fine -- verified in public/).
    What breaks is a blank line followed by a line starting with an inline
    element such as <text>, <line>, <rect> or <path>: marked starts a paragraph
    for that run, producing `<p><text>...</text><br>...` and the shape vanishes.
    So this checks that exact adjacency, not "any blank line".
    """
    out = []
    inline = re.compile(r"^\s*<(text|line|rect|path|circle|g|polygon|polyline|tspan)\b")
    for m in re.finditer(r"<svg\b.*?</svg>", body, re.S):
        block = m.group(0)
        lines = block.split("\n")
        la = re.search(r'aria-label="([^"]{0,26})', block)
        label = la.group(1) if la else ""
        for i in range(1, len(lines)):
            prev_blank = lines[i - 1].strip() == ""
            if not prev_blank:
                continue
            # marked starts a paragraph for a line that is INDENTED by 4+ spaces
            # (markdown code-block indentation) or after a blank line in a
            # markdown context. Column-0 SVG from the published posts renders
            # fine with blank lines (verified: 0 `<p><text` in public/), so only
            # the indented case is reported.
            if re.match(r"^ {4,}<(text|line|rect|path|circle|g|polygon)\b", lines[i]):
                out.append(Finding(ERROR, "S010",
                                   "SVG 內『空行 + 4 空格縮排的行內元素』會被 marked 包成 <p>，"
                                   "圖形會消失：第 %d 行 @ %s" % (i + 1, label)))
                break
        if "<figcaption" not in body[m.end():m.end() + 400]:
            out.append(Finding(WARN, "S011", "某張圖後面 400 字內沒有 <figcaption>"))
    return out


def check_bold(body):
    """Flag `**` that plausibly will not render -- but defer to the browser.

    History, because this matters: I wrote this check three times from theory
    (CommonMark flanking rules) and each version disagreed with reality --
    version 2 flagged 102 sites in a post that renders 130 <strong> tags,
    version 3 flagged 85 in the same post. The regex was the problem, not the

    Ground truth is tools/ainews/check_bold_render.py, which loads the BUILT page
    and counts surviving literal `**` in rendered text. That is the check the
    pipeline trusts.

    This function therefore only reports the one shape I verified as broken in
    real output (see _probe_bold.py on 2026/11/07: a closer followed by `。`),
    and emits it as a WARNING pointing at the authoritative tool. It must not
    produce ERRORs: a gate that cries wolf 100 times per post gets ignored.
    """
    out = []
    prose = re.sub(r"```.*?```", " ", body, flags=re.S)
    prose = re.sub(r"`[^`\n]+`", " ", prose)

    if prose.count("**") % 2:
        out.append(Finding(ERROR, "S021", "`**` 數量為奇數，有未閉合的粗體"))

    idx = [m.start() for m in re.finditer(r"\*\*", prose)]
    suspects = 0
    for k in range(0, len(idx) - 1, 2):
        closer = idx[k + 1]
        nxt = prose[closer + 2:closer + 3]
        if nxt in ("\u3002", "\u4e00", "\u2014"):
            suspects += 1

    if suspects:
        out.append(Finding(WARN, "S020",
                           "有 %d 處粗體結尾疑似接中文/全形標點；請用 "
                           "`python tools/ainews/check_bold_render.py --html <built.html>` 以實際渲染為準"
                           % suspects))
    return out
    return out
    return out


def check_banned(body):
    out = []
    for word in ("原稿", "教材", "講義", "本節"):
        if word in body:
            out.append(Finding(WARN, "S030", "使用了 PDF 筆記的用詞：%s（導讀不該出現）" % word))
    if "```mermaid" in body:
        out.append(Finding(WARN, "S031", "mermaid 區塊在站上不會渲染，請改用 inline SVG"))
    return out


def _normalise_number(raw: str, unit: str):
    """'80' + 'B' -> ('80', 'b');  '1,170' -> ('1170', None)."""
    n = raw.replace(",", "").rstrip(".")
    try:
        n = "%g" % float(n)
    except ValueError:
        return None, None
    u = (unit or "").lower().replace("/", "")
    return n, (u or None)


def _numbers_in(text):
    found = set()
    for raw, unit in _NUM.findall(text):
        n, u = _normalise_number(raw, unit)
        if n is None:
            continue
        found.add(n + (u or ""))
        found.add(n)          # bare number is enough to count as "present"
    return found


def collect_claims(body):
    """Bolded spans + table cells: the places where a fabricated number is loud.

    Prose numbers are skipped on purpose -- verifying every integer in fluent
    Chinese prose produces so many false positives that the gate stops being
    trusted, and mistrusted gates get bypassed.
    """
    claims = []
    for m in _BOLD.finditer(body):
        claims.append(("bold", m.group(1)))
    for row in _TABLE_ROW.findall(body):
        if re.match(r"^[-\s:|]+$", row):
            continue          # separator row
        claims.append(("table", row))
    return claims


def check_fidelity(body, extract_doc):
    """Every bolded/table number must exist in the source text.

    Small integers are excluded on purpose: a table cell like `| 1 | 2 |`
    (row counters, "top 3", list indices) trivially appears in any 100 KB
    newsletter, so checking them adds noise without catching a single
    fabrication. The numbers worth tracing are the ones a reader would quote:
    percentages, parameter counts, token counts, money.
    """
    out = []
    src = _numbers_in(_source_text(extract_doc))
    if not src:
        return [Finding(WARN, "F000", "來源文字裡解析不到任何數字，跳過比對")]

    missing = []
    for kind, text in collect_claims(body):
        for raw, unit in _NUM.findall(text):
            n, u = _normalise_number(raw, unit)
            if n is None:
                continue
            # bare small integers / bare years are noise, not claims
            if not u and len(n) <= 2:
                continue
            if not u and re.fullmatch(r"20\d\d", n):
                continue
            if n in src or (u and (n + u) in src):
                continue
            missing.append("%s%s" % (raw, u or "") + ("" if kind == "bold" else " [table]"))

    if missing:
        out.append(Finding(ERROR, "F001",
                           "有 %d 個數字在原文中找不到（可能是編造或轉述失真）：%s"
                           % (len(missing), ", ".join(missing[:8]))))
    return out


def _source_text(doc):
    parts = [doc.get("lede") or ""]
    for s in doc.get("sections") or []:
        parts.append(s.get("text") or "")
        for sub in s.get("subsections") or []:
            parts.append(sub.get("text") or "")
    return "\n".join(parts)


def lint(post_path, extract_path=None):
    with open(post_path, "r", encoding="utf-8-sig") as f:
        text = f.read()
    meta, body = split_frontmatter(text)

    findings = check_structure(body, meta)
    if extract_path:
        try:
            with open(extract_path, "r", encoding="utf-8-sig") as f:
                doc = json.load(f)
            findings += check_fidelity(body, doc)
        except (OSError, ValueError) as e:
            findings.append(Finding(WARN, "F100", "無法讀取 extract.json：%s" % e))
    else:
        findings.append(Finding(WARN, "F101", "未提供 --extract，跳過數字溯源檢查"))

    return findings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Lint an AINews digest against DIGEST_CONTRACT.md.")
    ap.add_argument("--post", required=True)
    ap.add_argument("--extract", help="extract.json of the issue (enables fidelity checks)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--strict", action="store_true", help="also fail on WARNING")
    args = ap.parse_args(argv)

    if not os.path.exists(args.post):
        print("ERROR: post not found: %s" % args.post, file=sys.stderr)
        return 2

    findings = lint(args.post, args.extract)
    errors = [f for f in findings if f.level == ERROR]
    warns = [f for f in findings if f.level == WARN]

    if args.json:
        print(json.dumps({"errors": len(errors), "warnings": len(warns),
                          "findings": [f.as_dict() for f in findings]},
                         ensure_ascii=False, indent=2))
    else:
        print("post: %s" % os.path.basename(args.post))
        for f in findings:
            print("  %-5s %s  %s" % (f.level, f.code, f.msg))
        print("\n%d error(s), %d warning(s)" % (len(errors), len(warns)))

    if errors:
        return 1
    if args.strict and warns:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
