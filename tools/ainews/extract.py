# -*- coding: utf-8 -*-
"""Stage 2: turn a fetched AINews email into clean, structured source text.

WHY
---
Stage 1 (detect.py) answers "is there a new issue". Stage 2 answers "what is
actually IN it", in a shape the writing stage can consume without re-parsing
MIME, quoted-printable, or beehiiv's template.

What the raw body looks like (verified against real issues):

    <sponsor block quoted with curly quotes>      -> drop
    <editorial lede: the author's framing>        -> KEEP, this is the story
    View image: (https://media.beehiiv.com/...)   -> drop
    Caption:                                      -> drop
    "AI News for MM/DD/YYYY-MM/DD/YYYY ..."       -> drop (masthead)
    ---------------- (separator)                  -> section boundary
    # AI Twitter Recap
    ## \r\n**What happened**\r\n ...              -> KEEP (empty H2 + crumb)
    # AI Reddit Recap
    ## /r/LocalLlama + /r/localLLM Recap
    ### 1. ...                                    -> KEEP
    ...
    "You are reading a plain text version ..."    -> drop (footer)

Everything except the lede and the recaps is boilerplate that otherwise leaks
into a digest (the hand-written posts had to strip it by eye).

USAGE
-----
    python tools/ainews/extract.py --input out/<id>/message.json
    python tools/ainews/extract.py --input msg.json --out out/<id>
    python tools/ainews/extract.py --input msg.json --stats

Outputs (when --out is given):
    <out>/source.txt      normalised plain text, sections separated by rule lines
    <out>/extract.json    {lede, sections, stats}

Exit codes: 0 = ok, 1 = error / no usable body.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

# beehiiv/SparkPost leave zero-width and bidi junk all over the plain-text part.
_INVISIBLE = dict.fromkeys(
    [0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF, 0x00A0, 0x2007, 0x202F,
     0x202A, 0x202B, 0x202C, 0x202D, 0x202E]
)

SEP = "\u2014" * 20
_FOOTER = "You are reading a plain text version of this post"
_H1 = re.compile(r"^#\s+(.+?)\s*$")
_H2 = re.compile(r"^##(?!#)\s*(.*)$")
_H3 = re.compile(r"^###\s+(.+?)\s*$")
_MASTHEAD = re.compile(r"^\u201cAI News for\s+\d{2}/\d{2}/\d{4}", re.I)
_SPONSOR_TAIL = re.compile(r"\u201c\s*\u2014\s*$")
_IMAGE_LINE = re.compile(r"^View image:\s*\(.*\)$", re.I)
_CAPTION_LINE = re.compile(r"^Caption:\s*$", re.I)


def normalise(text: str) -> str:
    """Strip invisibles, unify newlines, right-strip every line.

    The raw part contains hundreds of lines that are a lone \\r. They carry no
    meaning and would break blank-line logic, so they become empty strings.
    """
    if not text:
        return ""
    text = text.translate(_INVISIBLE)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in text.split("\n"))


def _blank(line: str) -> bool:
    return not line.strip()


def drop_boilerplate(lines):
    """Remove sponsor/masthead/image/caption/footer noise; keep section rules."""
    kept = []
    for line in lines:
        s = line.strip()
        if s.startswith(_FOOTER):
            break                      # the footer marks the end of the post
        if _MASTHEAD.match(s) or _SPONSOR_TAIL.search(s):
            continue
        if _IMAGE_LINE.match(s) or _CAPTION_LINE.match(s):
            continue
        if s.startswith(SEP[:10]):
            kept.append(SEP)


def drop_boilerplate(lines):
    """Remove sponsor/masthead/image/caption/footer noise; keep section rules."""
    kept = []
    for line in lines:
        s = line.strip()
        if s.startswith(_FOOTER):
            break                      # the footer marks the end of the post
        if _MASTHEAD.match(s) or _SPONSOR_TAIL.search(s):
            continue
        if _IMAGE_LINE.match(s) or _CAPTION_LINE.match(s):
            continue
        if s.startswith(SEP[:10]):
            kept.append(SEP)
            continue
        kept.append(line)
    return kept


def collapse_blanks(lines):
    out = []
    for line in lines:
        if _blank(line) and (not out or _blank(out[-1]) or out[-1] == SEP):
            continue
        out.append("" if _blank(line) else line)
    while out and _blank(out[-1]):
        out.pop()
    while out and _blank(out[0]):
        out.pop(0)
    return out


def classify_title(title: str) -> str:
    t = title.lower()
    if "twitter" in t:
        return "twitter"
    if ("localllama" in t) or ("localllm" in t):
        return "local"
    if "local" in t and "recap" in t:
        return "local"
    if "less technical" in t or "singularity" in t or "claudeai" in t:
        return "less_technical"
    if "reddit" in t:
        # A bare "# AI Reddit Recap" is only a container. Real issues usually put
        # a rule between sub-reddit groups, so each group becomes its own
        # section -- but if no rule is present the container keeps them nested.
        return "reddit_container"
    return "other"


def sub_sections(block_lines):
    """Split a container block into `## ...` groups (Reddit sub-reddit groups).

    Returns [(subtitle, [lines])]; the first group's leading H1 lines stay with
    the container so nothing is lost.
    """
    groups, cur, cur_title = [], [], None
    for line in block_lines:
        m = _H2.match(line)
        if m and m.group(1).strip():
            if cur:
                groups.append((cur_title, cur))
            cur, cur_title = [line], m.group(1).strip()
        else:
            cur.append(line)
    if cur:
        groups.append((cur_title, cur))
    return groups


def split_sections(lines):
    """Split on the rule, then name each block by its first heading."""
    blocks, cur = [], []
    for line in lines:
        if line == SEP:
            if any(not _blank(l) for l in cur):
                blocks.append(cur)
            cur = []
        else:
            cur.append(line)
    if any(not _blank(l) for l in cur):
        blocks.append(cur)

    sections = []
    for idx, block in enumerate(blocks):
        headings = []
        for line in block:
            m = _H1.match(line) or _H3.match(line)
            if m:
                headings.append(m.group(1).strip())
                continue
            m2 = _H2.match(line)
            if m2 and m2.group(1).strip():
                headings.append(m2.group(1).strip())
        title = headings[0] if headings else ""
        key = "lede" if (idx == 0 and not title) else classify_title(title)
        sections.append({
            "index": idx,
            "key": key,
            "title": title,
            "headings": headings,
            "lines": block,
        })
    return sections


def fold_empty_h2(lines):
    """`## ` followed by a bold crumb collapses to the crumb.

    The plain-text part emits an empty H2 and then the actual label on the next
    line; left alone it renders as a stray heading in a digest.
    """
    out, i = [], 0
    while i < len(lines):
        m = _H2.match(lines[i])
        if m and not m.group(1).strip():
            j = i + 1
            while j < len(lines) and _blank(lines[j]):
                j += 1
            if j < len(lines):
                out.append(lines[j].strip())
                i = j + 1
                continue
        out.append(lines[i])
        i += 1
    return out


def stats_of(sections) -> dict:
    all_text = "\n".join(s["text"] for s in sections)
    by_key = {s["key"]: len(s["text"]) for s in sections}
    quantities = re.findall(
        r"\b\d[\d,.]*\s?(?:%|x|B\b|T\b|M\b|tok/s|hours?|days?|tokens?)\b", all_text)
    return {
        "sections": len(sections),
        "chars": len(all_text),
        "words": len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-/.]*", all_text)),
        "headings": sum(len(s["headings"]) for s in sections),
        "quantities": len(quantities),
        "chars_by_section": by_key,
    }


def _body_from_payload(payload: dict) -> str:
    """Fallback: the longest base64url text/plain part, walking nested parts."""
    import base64

    def walk(p):
        yield p
        for c in p.get("parts") or []:
            yield from walk(c)

    best = ""
    for part in walk(payload):
        if part.get("mimeType") == "text/plain":
            data = (part.get("body") or {}).get("data") or ""
            if not data:
                continue
            pad = "=" * ((4 - len(data) % 4) % 4)
            try:
                txt = base64.urlsafe_b64decode((data + pad).encode()).decode("utf-8", "replace")
            except Exception:
                continue
            if len(txt) > len(best):
                best = txt
    return best


def extract_message(msg: dict) -> dict:
    """msg = one Gmail message dict. messageText first, MIME payload as fallback."""
    body = msg.get("messageText") or ""
    if not body.strip():
        body = _body_from_payload(msg.get("payload") or {})
    if not body.strip():
        raise ValueError("no usable body (messageText empty and no text/plain part)")

    lines = collapse_blanks(drop_boilerplate(normalise(body).split("\n")))
    sections = split_sections(lines)
    for s in sections:
        # Split the container BEFORE folding, otherwise `## /r/LocalLlama` has
        # already collapsed to a plain line and the sub-group boundary is lost.
        raw_subs = sub_sections(s["lines"]) if s["key"] == "reddit_container" else []

        # fold crumbs then re-collapse, so the blank line left behind disappears
        s["lines"] = collapse_blanks(fold_empty_h2(s["lines"]))
        s["text"] = "\n".join(s["lines"]).strip()

        # a container block ("# AI Reddit Recap") carries several sub-groups;
        # expose them so the writer can cite /r/LocalLlama vs /r/ClaudeAI precisely
        if raw_subs:
            subs = []
            for subtitle, sub_lines in raw_subs:
                if subtitle is None:
                    continue
                subs.append({
                    "title": subtitle,
                    "key": classify_title(subtitle),
                    "text": "\n".join(collapse_blanks(fold_empty_h2(sub_lines))).strip(),
                })
            s["subsections"] = subs

    lede = next((s["text"] for s in sections if s["key"] == "lede"), "")
    return {
        "messageId": msg.get("messageId", ""),
        "threadId": msg.get("threadId", ""),
        "subject": msg.get("subject", ""),
        "sender": msg.get("sender", ""),
        "date": msg.get("messageTimestamp", ""),
        "display_url": msg.get("display_url", ""),
        "lede": lede,
        "sections": [{k: s[k] for k in ("index", "key", "title", "headings", "text")}
                     | ({"subsections": s["subsections"]} if "subsections" in s else {})
                     for s in sections],
        "stats": stats_of([{"key": s["key"], "text": s["text"],
                            "headings": s["headings"]} for s in sections]),
    }


def render_source_txt(doc: dict) -> str:
    """Human-readable source.txt: one block per section, rule-separated."""
    out = ["# SOURCE: %s" % doc["subject"], ""]
    out += ["messageId: %s" % doc["messageId"],
            "date: %s" % doc["date"],
            "url: %s" % doc["display_url"], ""]
    for s in doc["sections"]:
        out += ["=" * 78, "[%d] %s  (%s)" % (s["index"], s["key"], s["title"] or "(no heading)"),
                "=" * 78, s["text"], ""]
        for sub in s.get("subsections") or []:
            out += ["-" * 70, "  > %s  [%s]" % (sub["title"], sub["key"]), sub["text"], ""]
    return "\n".join(out).rstrip() + "\n"


def write_outputs(doc: dict, out_dir: str) -> tuple:
    os.makedirs(out_dir, exist_ok=True)
    txt_path = os.path.join(out_dir, "source.txt")
    json_path = os.path.join(out_dir, "extract.json")
    with open(txt_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(render_source_txt(doc))
    with open(json_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return txt_path, json_path


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Extract clean source text from an AINews email.")
    ap.add_argument("--input", required=True, help="JSON holding one Gmail message payload")
    ap.add_argument("--out", help="output directory (source.txt + extract.json)")
    ap.add_argument("--stats", action="store_true", help="print stats only")
    args = ap.parse_args(argv)

    try:
        with open(args.input, "r", encoding="utf-8-sig") as f:
            raw = json.load(f)
    except (OSError, ValueError) as e:
        print("ERROR: cannot read %s: %s" % (args.input, e), file=sys.stderr)
        return 1

    msg = _pick_message(raw)
    if msg is None:
        print("ERROR: no message dict found in %s" % args.input, file=sys.stderr)
        return 1

    try:
        doc = extract_message(msg)
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 1

    st = doc["stats"]
    print("%s" % doc["subject"])
    print("  sections=%d chars=%d words=%d headings=%d quantities=%d"
          % (st["sections"], st["chars"], st["words"], st["headings"], st["quantities"]))
    for s in doc["sections"]:
        print("    [%d] %-16s %6d chars  %s"
              % (s["index"], s["key"], len(s["text"]), (s["title"] or "")[:44]))

    if args.out and not args.stats:
        txt, js = write_outputs(doc, args.out)
        print("wrote:", txt)
        print("wrote:", js)
    return 0


def _pick_message(raw):
    """Accept a bare message, {data:{...}}, or the {results:[{response:{data:...}}]} shape."""
    if isinstance(raw, dict):
        if raw.get("messageId") and ("messageText" in raw or "payload" in raw):
            return raw
        for key in ("data", "response"):
            got = _pick_message(raw.get(key))
            if got:
                return got
        results = raw.get("results")
        if isinstance(results, list):
            for item in results:
                got = _pick_message(item)
                if got:
                    return got
    return None


if __name__ == "__main__":
    sys.exit(main())

