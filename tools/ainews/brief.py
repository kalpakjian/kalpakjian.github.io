# -*- coding: utf-8 -*-
"""Stage 3b: turn extract.json into a writing brief -- the machine's half of the work.

WHY THIS EXISTS
---------------
Writing a digest needs two different kinds of work:

  * judgement   -- what is the story, what do I actually believe, what does the
                   evidence fail to support
  * bookkeeping -- which three numbers matter, which section is the headline,
                   which claims contradict each other, what did the source
                   explicitly call unconfirmed

Only the second kind is automatable, and it is also the part that eats the most
time. So this script produces no prose at all. It produces a short, ordered
brief that a human (or a model) writes FROM:

    headline candidates   ranked by how many hard numbers + names they carry
    number ledger         every quantity with its section, so writing can cite
                          exact figures without re-reading 100 KB
    unconfirmed claims    sentences the source itself flagged as rumour
    contradiction watch   same metric, different values in different sections
    counterpoint seeds    places where the source itself hedged
    do-not-write list     sponsors, activities, boilerplate that must not appear

The brief is deliberately dumb and explainable: every line can be traced to a
rule in RANKING_RULES below, so when it picks a bad headline I can fix the rule
rather than guess at a model's mood.

USAGE
    python tools/ainews/brief.py --extract out/<id>/extract.json
    python tools/ainews/brief.py --extract out/<id>/extract.json --out out/<id>
    python tools/ainews/brief.py --extract out/<id>/extract.json --json

Exit codes: 0 = ok, 1 = error.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# RANKING_RULES -- why a candidate is promoted. Keep these readable: the whole
# point is that a bad ranking is a fixable rule, not a mysterious model choice.
#
#   hard numbers    a summary carrying "%", "tok/s", "B/T parameters", "$" is
#                   concrete and quotable; a summary with none is usually framing
#   named entities  models, labs, people: capitalised multi-word tokens
#   benchmark words the site's readers search for these
#   novelty words   release/launch/open-weight outrank "discussed"
#
# A quantity must have a unit to count as "hard". `12T` (tokens) and `T` are
# ambiguous with dates/words, so the number must be followed by a unit AND not
# be preceded by a digit (which would make it part of a date like 2026-11-06).
NUM = re.compile(r"(?<![\d\-/])\$?\d[\d.]*\s?(?:%|x\b|B\b|T\b|M\b|K\b|k\b|tok/s|ms\b|hours?\b|days?\b|tokens?\b|GW\b)", re.I)
ENTITY = re.compile(r"\b(?:[A-Z][A-Za-z0-9.\-]+)(?:\s+[A-Z][A-Za-z0-9.\-]+){0,2}\b")
# Capitalised sentence-openers and list labels are not entities. Without this,
# "Announced", "Architecture" and "Available" outscore the model name itself,
# because the scoring counts distinct capitalised tokens.
NOT_ENTITY = {
    "launch", "announced", "available", "architecture", "licensing", "results",
    "headline", "mitigation", "mitigations", "detection", "release", "update",
    "the", "this", "that", "these", "those", "there", "they", "then", "and",
    "but", "for", "with", "from", "into", "over", "under", "after", "before",
    "according", "reported", "reportedly", "meanwhile", "however", "also",
    "if", "in", "on", "at", "as", "of", "to", "a", "an", "it", "its",
    "why", "what", "how", "when", "where", "which", "who", "whom",
    "yes", "no", "not", "more", "less", "new", "now", "first", "last",
    "people", "users", "commenters", "one", "two", "three", "four", "five",
}
BENCH = ("benchmark", "eval", "arena", "arc-agi", "swe-bench", "livecodebench",
         "mmlu", "gpqa", "index", "scored", "score", "accuracy", "pass^")
NOVELTY = ("launch", "release", "released", "open-weight", "open weight",
           "announced", "shipped", "ships", "available now", "general availability")
HEDGE = ("reportedly", "allegedly", "rumor", "rumour", "unconfirmed", "claims",
         "claimed", "speculation", "speculat", "unverified", "said to",
         "expected to", "not independently verified", "no independent")
NO_WRITE = ("sponsor", "brought to you by", "save your spot", "join andrew ng",
            "nodes 2026", "backblaze", "advertise", "unsubscribe",
            "behind latent space", "kill my saas", "aiei")


def _bullets(text):
    """Split a recap section into its top-level bullets.

    beehiiv nests with two-space indents; only column-0 `* ` items are top-level
    stories, and taking every line would yield thousands of fragments.
    """
    out, cur = [], []
    for line in text.split("\n"):
        if re.match(r"^\* ", line):
            if cur:
                out.append("\n".join(cur).strip())
            cur = [line]
        elif cur:
            cur.append(line)
    if cur:
        out.append("\n".join(cur).strip())
    return out


def _first_sentence(block, limit=220):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", block)   # links -> label
    text = re.sub(r"\*\*|`", "", text)
    text = re.sub(r"^\*\s*", "", text).strip()
    m = re.search(r"^(.{20,%d}?[.。!?])\s" % limit, text, re.S)
    head = m.group(1) if m else text[:limit]
    return re.sub(r"\s+", " ", head).strip()


KNOWN = (
    "qwen", "claude", "gemini", "inkling", "deepseek", "kimi", "gpt", "opus",
    "astra", "sol", "mythos", "tinker", "anthropic", "openai", "google",
    "meta", "muse", "mistral", "glm", "ernie", "llama", "nemotron", "hy4",
    "hunyuan", "sakana", "sawara", "backblaze", "neo4j", "nvidia", "rubin",
    "blackwell", "radeon", "arc", "prize", "arena", "vals", "metr", "aime",
    "swebench", "swe-bench", "livecodebench", "mmlu", "gpqa", "humaneval",
    "latent", "space", "ainews",
)


def _entities(text):
    """Capitalised runs that look like real names (models, labs, people).

    Sentence-initial capitals ("Reaching", "Post", "Activity") are the main
    source of false entities in these summaries -- they are capitalised only
    because they start a sentence or a label. A token is kept when any of:

      * it appears more than once in the block (proper names repeat)
      * it is capitalised somewhere other than the first character
      * it contains a digit or an internal capital (GPT-6, MMLU-Pro, Mi355X)
      * it is in KNOWN (one-shot proper nouns: Tinker, Mythos, Anthropic)

    which removes label noise without shipping an NER model.
    """
    runs = [m.group(0) for m in ENTITY.finditer(text)]
    counts = {}
    for r in runs:
        for w in r.split():
            counts[w] = counts.get(w, 0) + 1

    out = []
    for r in runs:
        keep = []
        for w in r.split():
            lw = w.lower().strip(".,")
            if lw in NOT_ENTITY:
                continue
            mid_cap = any(ch.isupper() for ch in w[1:])
            has_digit = any(ch.isdigit() for ch in w)
            if (counts.get(w, 0) > 1 or mid_cap or has_digit
                    or lw in KNOWN):
                keep.append(w)
        if not keep:
            continue
        cand = " ".join(keep)
        if len(keep) == 1 and len(cand) < 4:
            continue
        out.append(cand)
    return sorted(set(out))


def _score(text):
    numbers = len(NUM.findall(text))
    entities = len(_entities(text))
    bench = sum(1 for b in BENCH if b in text.lower())
    novel = sum(1 for n in NOVELTY if n in text.lower())
    return numbers * 3 + entities * 2 + bench * 2 + novel * 2, {
        "numbers": numbers, "entities": entities, "benchmarks": bench, "novelty": novel}


def headline_candidates(doc, top=6):
    cands = []
    for sec in doc.get("sections") or []:
        if sec.get("key") == "lede":
            continue
        for block in _bullets(sec.get("text") or ""):
            score, why = _score(block)
            if score <= 0:
                continue
            cands.append({
                "section": sec.get("key"),
                "title": sec.get("title") or "(lede)",
                "summary": _first_sentence(block),
                "score": score,
                "why": why,
                "numbers": NUM.findall(block)[:6],
                "entities": _entities(block)[:6],
            })
    cands.sort(key=lambda c: -c["score"])
    # De-duplicate on the summary with digit runs normalised, so near-identical
    # bullets from a fixture (or a twice-posted story) collapse to one candidate.
    seen, out = set(), []
    for c in cands:
        k = re.sub(r"\d+", "#", c["summary"])[:70]
        if k in seen:
            continue
        seen.add(k)
        out.append(c)
        if len(out) >= top:
            break
    return out


def _dedupe(items):
    """De-duplicate while keeping first-seen order."""
    return list(dict.fromkeys(items))


def number_ledger(doc):
    """Every quantity in the source, with the section it came from.

    Writing needs exact figures; this ledger is why nobody has to re-read 100 KB.
    Grouped by section (not sorted by value) so a writer can see what each part
    of the issue actually established.
    """
    ledger = []
    for sec in doc.get("sections") or []:
        text = sec.get("text") or ""
        found = _dedupe(NUM.findall(text))
        if not found:
            continue
        ledger.append({
            "section": sec.get("key"),
            "title": sec.get("title") or "",
            "count": len(found),
            "quantities": found[:40],
        })
    return ledger


def flagged_claims(doc):
    """Sentences the SOURCE itself hedged -- these must stay hedged in the post.

    DIGEST_CONTRACT §7 forbids turning 'reportedly' into fact. Surfacing them
    here makes the rule enforceable at writing time instead of at review time.
    """
    out, seen = [], set()
    for sec in doc.get("sections") or []:
        for line in (sec.get("text") or "").split("\n"):
            low = line.lower()
            hits = [h for h in HEDGE if h in low]
            if not hits:
                continue
            clean = re.sub(r"\*\*|`", "", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)).strip()
            if len(clean) < 30:
                continue
            key = clean[:70]
            if key in seen:
                continue
            seen.add(key)
            out.append({"section": sec.get("key"), "markers": hits, "text": clean[:260]})
    return out[:12]


def contradiction_watch(doc):
    """Same unit, many distinct values -- the risk of quoting the wrong one.

    The most embarrassing digest error is quoting one number while the issue
    itself states another (leaderboard vs. narrative). This lists each unit with
    enough distinct values that a careless writer could pick the wrong one.
    """
    seen = {}
    for sec in doc.get("sections") or []:
        for line in (sec.get("text") or "").split("\n"):
            for q in NUM.findall(line):
                unit = re.sub(r"[\d.,\s]", "", q).strip().lower()
                if unit not in ("%", "b", "t", "m", "tok/s"):
                    continue
                value = re.sub(r"[^\d.]", "", q).strip(".")
                if value:
                    seen.setdefault(unit, {}).setdefault(value, set()).add(sec.get("key"))
    out = []
    for unit, values in seen.items():
        if len(values) < 4:
            continue
        out.append({"unit": unit, "distinct_values": len(values),
                    "examples": sorted(values, key=lambda v: -len(v))[:6]})
    return out


def do_not_write(doc):
    """Substrings that must never reach the post (contract §7)."""
    text = "\n".join((s.get("text") or "") for s in doc.get("sections") or []).lower()
    return [p for p in NO_WRITE if p in text]


def verdict(doc):
    """Should this issue get a full digest? (contract §6)

    The machine's opinion only: it answers 'is there enough material', not 'is it
    interesting'. A human can always override upward.
    """
    st = doc.get("stats") or {}
    reasons = []
    if st.get("quantities", 0) < 40:
        reasons.append("硬數字只有 %d 個（< 40）" % st.get("quantities", 0))
    if st.get("chars", 0) < 40000:
        reasons.append("內文只有 %d 字元（< 40,000）" % st.get("chars", 0))
    if st.get("sections", 0) < 4:
        reasons.append("只有 %d 個分區（< 4）" % st.get("sections", 0))
    subject = (doc.get("subject") or "").lower()
    if any(p in subject for p in ("behind latent space", "aiei", "kill my saas")):
        reasons.append("標題是活動／訪談宣傳")
    return {"mode": "digest" if not reasons else "short", "reasons": reasons}



def build_brief(doc):
    return {
        "messageId": doc.get("messageId", ""),
        "subject": doc.get("subject", ""),
        "date": doc.get("date", ""),
        "display_url": doc.get("display_url", ""),
        "verdict": verdict(doc),
        "stats": doc.get("stats", {}),
        "lede": (doc.get("lede") or "")[:1200],
        "section_map": [
            {"key": s.get("key"), "title": s.get("title"), "chars": len(s.get("text") or "")}
            for s in doc.get("sections") or []
        ],
        "headline_candidates": headline_candidates(doc),
        "number_ledger": number_ledger(doc),
        "flagged_claims": flagged_claims(doc),
        "contradiction_watch": contradiction_watch(doc),
        "do_not_write": do_not_write(doc),
    }


def render_markdown(brief):
    """The brief as a checklist a human writes FROM -- not as prose."""
    L = []
    v = brief["verdict"]
    L.append("# 寫稿大綱：%s" % brief["subject"])
    L.append("")
    L.append("- messageId: `%s`" % brief["messageId"])
    L.append("- 日期: %s" % brief["date"])
    L.append("- 原文: %s" % brief["display_url"])
    L.append("- **建議模式：%s**%s" % (
        v["mode"], "" if not v["reasons"] else "（" + "；".join(v["reasons"]) + "）"))
    st = brief.get("stats") or {}
    L.append("- 規模: %s 分區 / %s 字元 / %s 個硬數字 / %s 個標題"
             % (st.get("sections"), st.get("chars"), st.get("quantities"), st.get("headings")))
    L.append("")

    if brief["lede"]:
        L.append("## 主編導言（敘事角度，優先參考）")
        L.append("")
        L.append("> " + brief["lede"].replace("\n\n", "\n> ").replace("\n", "\n> "))
        L.append("")

    L.append("## 頭條候選（依『硬數字 × 具名實體 × 評測名詞 × 新穎性』排序）")
    L.append("")
    for i, c in enumerate(brief["headline_candidates"], 1):
        L.append("### %d. [%d 分] %s" % (i, c["score"], c["title"]))
        L.append("")
        L.append("- 摘要：%s" % c["summary"])
        L.append("- 數字：%s" % ("、".join(c["numbers"]) or "（無）"))
        L.append("- 實體：%s" % ("、".join(c["entities"]) or "（無）"))
        L.append("- 計分：數字 %d、實體 %d、評測 %d、新穎 %d"
                 % (c["why"]["numbers"], c["why"]["entities"],
                    c["why"]["benchmarks"], c["why"]["novelty"]))
        L.append("")

    L.append("## 數字清單（寫稿時照抄，不要重算）")
    L.append("")
    for row in brief["number_ledger"]:
        L.append("- **%s**（%s 項）：%s" % (row["title"] or row["section"], row["count"],
                                          "、".join(row["quantities"])))
    L.append("")

    if brief["flagged_claims"]:
        L.append("## 原文自己標記為未確認的說法（**寫稿時必須保留保留語氣**）")
        L.append("")
        for f in brief["flagged_claims"]:
            L.append("- [%s｜%s] %s" % (f["section"], "/".join(f["markers"]), f["text"]))
        L.append("")

    if brief["contradiction_watch"]:
        L.append("## 同單位多值（小心引用錯）")
        L.append("")
        for c in brief["contradiction_watch"]:
            L.append("- 單位 `%s`：%d 個不同數值，例：%s"
                     % (c["unit"], c["distinct_values"], "、".join(c["examples"])))
        L.append("")

    if brief["do_not_write"]:
        L.append("## 不可寫入的內容（贊助／活動）")
        L.append("")
        L.append("- " + "、".join(brief["do_not_write"]))
        L.append("")

    L.append("## 交稿前自檢")
    L.append("")
    L.append("1. 每個數字都出現在上面的清單裡")
    L.append("2. 「我的判讀」有一個可反駁的主張，且有『我會錯在哪』")
    L.append("3. 未確認說法都保留了『據稱／未證實』")
    L.append("4. 圖 ≥2、表 ≥5、字數 4,000–12,000")
    L.append("5. 跑 `digest_lint.py` 0 error、`check_bold_render.py` 0 字面星號")
    L.append("")
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build a writing brief from extract.json.")
    ap.add_argument("--extract", required=True)
    ap.add_argument("--out", help="write brief.json + brief.md here")
    ap.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    args = ap.parse_args(argv)

    try:
        with open(args.extract, "r", encoding="utf-8-sig") as f:
            doc = json.load(f)
    except (OSError, ValueError) as e:
        print("ERROR: cannot read %s: %s" % (args.extract, e), file=sys.stderr)
        return 1

    brief = build_brief(doc)
    md = render_markdown(brief)

    if args.json:
        print(json.dumps(brief, ensure_ascii=False, indent=2))
    else:
        print(md)

    if args.out:
        os.makedirs(args.out, exist_ok=True)
        jp = os.path.join(args.out, "brief.json")
        mp = os.path.join(args.out, "brief.md")
        with open(jp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(brief, f, ensure_ascii=False, indent=2)
            f.write("\n")
        with open(mp, "w", encoding="utf-8", newline="\n") as f:
            f.write(md)
        print("\nwrote: %s" % jp, file=sys.stderr)
        print("wrote: %s" % mp, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

