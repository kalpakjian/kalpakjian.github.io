# -*- coding: utf-8 -*-
"""Stage 3b: turn extract.json into a writing brief -- the machine's half.

WHAT THIS DOES AND DOES NOT DO
------------------------------
It gathers material. It does NOT decide what the story is.

That line was learned the hard way. Three attempts at ranking headlines by
keyword density (numbers x entities x benchmark terms, then + section weight +
position decay, then + release verbs - hedge penalty) all failed on the only
ground truth that exists: the two digests already published.

    1a19fe7ff898cb7e  Weight Space Programming -> machine picked an ISTA quant post
    1a1b3f849653d148  Anthropic IPO              -> machine picked Inkling, rank 4
                                                    for the actual headline

The reason is structural, not a tuning problem: the same story appears in
several consecutive issues (Inkling debuted on 11/06 and was recapped on 11/07),
so "release + many numbers" scores high in both, and knowing which issue OWNS a
story needs the news cycle, not term counts.

So the brief now groups candidates BY SECTION, in source order, and says so:

    "Twitter 摘要（作者已篩選）   1. ... 2. ... 3. ...
     "Reddit 摘要（社群討論）     1. ... 2. ..."

The score survives as `density_rank` -- a display hint, explicitly labelled as
NOT a measure of importance. A human (or a model with the source text) decides.

USAGE
    python tools/ainews/brief.py --extract out/<id>/extract.json --out out/<id>
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
# Release verbs outrank measurement verbs. A story that says "released / launched /
# announced" is news; "running / benchmarked / achieves" is a data point about
# something that already shipped. Without this, the Z.ai pipeline rumour (17
# numbers, 6 entities) beat the Inkling launch on the issue whose subject line
# IS Inkling.
RELEASE = ("released", "release", "launched", "launch", "announced", "ships",
           "shipped", "now available", "open weights", "open-weights", "open sourced",
           "open-sourced", "general availability")
HEDGE = ("reportedly", "allegedly", "rumor", "rumour", "unconfirmed", "claims",
         "claimed", "speculation", "speculat", "unverified", "said to",
         "expected to", "not independently verified", "no independent")
NOVELTY = ("launch", "release", "released", "open-weight", "open weight",
           "announced", "shipped", "ships", "available now", "general availability")
HEDGE = ("reportedly", "allegedly", "rumor", "rumour", "unconfirmed", "claims",
         "claimed", "speculation", "speculat", "unverified", "said to",
         "expected to", "not independently verified", "no independent")
NO_WRITE = ("sponsor", "brought to you by", "save your spot", "join andrew ng",
            "nodes 2026", "backblaze", "advertise", "unsubscribe",
            "behind latent space", "kill my saas", "aiei")


def _bullets(text):
    """Split a recap section into candidate story blocks.

    THE BUG THIS FIXES: the first version only kept `* ` lines, so it captured
    the *sub-points* of a story and threw away the story itself. AINews shapes a
    Twitter entry like this:

        **What happened**                          <- label
        **Thinking Machines released Inkling 2 Small, a 594B-total /
          17B-active multimodal MoE.**             <- THE STORY (not a bullet)
        * **Launch:** Announced at 31 on the ...   <- a sub-point
        * **Pricing:** ...

    Keeping only bullets meant the headline sentence never became a candidate,
    and every fragment that did was small -- which is why Reddit's dense
    hardware posts outscored the actual lead story on every issue tested.

    Now a block starts at EITHER a `* ` bullet OR a line that is entirely a
    bold claim (`**...**`), and everything indented or non-bulleted after it
    belongs to that block.
    """
    lines = text.split("\n")
    starts = []          # (line_index, is_bold_claim)
    for i, line in enumerate(lines):
        if re.match(r"^\* ", line):
            starts.append((i, False))
        elif re.match(r"^\*\*[^*]+\*\*\s*$", line) and len(line.strip()) > 40:
            starts.append((i, True))

    out = []
    for n, (i, _is_bold) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
        block = "\n".join(lines[i:end]).strip()
        if block:
            out.append(block)
    return out


# Position weight: AINews is ordered by editorial importance. The first story in
# `# AI Twitter Recap` is the lead; the Reddit recaps are community chatter the
# author already decided came second. Ignoring this was the second half of the
# ranking bug -- every one of the top 12 candidates came from Reddit while the
# actual lead story never appeared at all.
SECTION_WEIGHT = {
    "twitter": 1.0,           # curated by AINews -> highest signal
    "local": 0.45,
    "reddit_container": 0.40,
    "other": 0.35,
    "less_technical": 0.30,
}

# Human-facing section names. The source titles are English; the brief is Chinese.
SECTION_LABEL = {
    "twitter": "作者已篩選，優先閱讀",
    "local": "本地模型圈",
    "reddit_container": "社群討論，通常是補充",
    "less_technical": "非技術討論",
    "other": "其他",
}
# Within the twitter section position matters a lot: rank 0 is the lead story.
POSITION_DECAY = (1.0, 0.72, 0.58, 0.48, 0.42, 0.38)


def _position_factor(rank_in_section):
    if rank_in_section < len(POSITION_DECAY):
        return POSITION_DECAY[rank_in_section]
    return 0.30


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
    low = text.lower()
    numbers = len(NUM.findall(text))
    entities = len(_entities(text))
    bench = sum(1 for b in BENCH if b in low)
    novel = sum(1 for n in NOVELTY if n in low)
    release = sum(1 for r in RELEASE if r in low)
    hedged = sum(1 for h in HEDGE if h in low)
    # Weights, and why:
    #   release x4  -- the strongest single signal that an item is *news*
    #   numbers x2  -- concrete, but dense spec posts are usually follow-ups
    #   entities x2 -- named subject matters
    #   bench/nove  -- keep the old terms, lower, as tie-breakers
    #   hedged -6   -- a rumour must not outrank a confirmed release
    score = (release * 4 + numbers * 2 + entities * 2 + bench * 2 + novel * 2
             - hedged * 6)
    return max(0, score), {
        "numbers": numbers, "entities": entities, "benchmarks": bench,
        "novelty": novel, "release": release, "hedged": hedged}


def section_candidates(doc, per_section=6):
    """Group story candidates BY SECTION, in source order -- no global ranking.

    Why no ranking: see the module docstring. Three scoring schemes in a row
    disagreed with the two published digests, because importance depends on the
    news cycle (is this issue the DEBUT of the story, or a recap?), which term
    counts cannot see.

    The order inside a section IS preserved and IS meaningful: AINews lists the
    lead story first, and that editorial order is the only reliable signal in
    the source.

    `density_rank` is kept as a display hint (how many numbers/names the item
    carries) and is explicitly documented as NOT importance.
    """
    groups = []
    for sec in doc.get("sections") or []:
        key = sec.get("key")
        if key == "lede":
            continue
        items, seen = [], set()
        for pos, block in enumerate(_bullets(sec.get("text") or "")):
            score, why = _score(block)
            summary = _first_sentence(block)
            k = re.sub(r"\d+", "#", summary)[:70]
            if k in seen:
                continue
            seen.add(k)
            items.append({
                "section": key,
                "title": sec.get("title") or "",
                "order": pos,
                "summary": summary,
                "density": score,
                "density_why": why,
                "numbers": NUM.findall(block)[:6],
                "entities": _entities(block)[:6],
            })
            if len(items) >= per_section:
                break
        if items:
            groups.append({"section": key, "title": sec.get("title") or "",
                           "items": items})
    return groups


def density_rank(doc, top=6):
    """Flat, cross-section list sorted by density -- for reference only.

    Deliberately NOT called a headline ranking. Kept because it is genuinely
    useful for one thing: spotting which item carries the most quotable
    figures, regardless of where it sits in the issue.
    """
    flat = []
    for g in section_candidates(doc, per_section=99):
        flat.extend(g["items"])
    flat.sort(key=lambda c: -c["density"])
    return flat[:top]


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
            # 60 per section: the Inkling issue has 82 in the twitter block alone,
            # and the first cap (40) silently hid the later half of the issue --
            # exactly the numbers a writer needs for the "其他重點" section.
            "quantities": found[:60],
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

    Section count is NOT a gate on its own: a normal issue has exactly three
    sections (Twitter / Reddit / Less-technical) because that is how beehiiv
    splits it. The Inkling issue has 3 sections, 65 KB and 103 hard numbers, and
    the first version called it "short" purely for having three sections --
    a wrong verdict on the issue with the most material of the five tested.
    So sections are only a gate when the BODY is also thin.
    """
    st = doc.get("stats") or {}
    quantities = st.get("quantities", 0)
    chars = st.get("chars", 0)
    sections = st.get("sections", 0)
    reasons = []

    if chars < 40000:
        reasons.append("內文只有 %d 字元（< 40,000）" % chars)
    if quantities < 40:
        reasons.append("硬數字只有 %d 個（< 40）" % quantities)
    # a genuinely fragmented issue: small AND few sections
    if sections < 3 and chars < 60000:
        reasons.append("只有 %d 個分區且內文偏少" % sections)

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
        "sections": section_candidates(doc, per_section=6),
        "density_reference": density_rank(doc, top=5),
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

    L.append("## 各區塊要點（**依原文順序，不是重要性排序**）")
    L.append("")
    L.append("> AINews 的排列順序本身就是作者的編輯判斷：**每個區塊的第一則就是該區塊的頭條**。")
    L.append("> 下面不做跨區塊排名，因為同一則新聞會連續出現在多期（首發 vs 回顧），")
    L.append("> 靠詞頻無法分辨「這期是誰的新聞」。頭條請你讀完後自己決定。")
    L.append("")
    for g in brief.get("sections") or []:
        label = SECTION_LABEL.get(g["section"], g["section"])
        L.append("### %s（%s）" % (g["title"] or label, label))
        L.append("")
        for i, it in enumerate(g["items"], 1):
            mark = "**" if i == 1 else ""
            L.append("%d. %s%s%s" % (i, mark, it["summary"], mark))
            extra = []
            if it["numbers"]:
                extra.append("數字：" + "、".join(it["numbers"]))
            if it["entities"]:
                extra.append("實體：" + "、".join(it["entities"]))
            if extra:
                L.append("   - " + "｜".join(extra))
        L.append("")

    if brief.get("density_reference"):
        L.append("## 密度榜（**僅供參考，不是重要性**）")
        L.append("")
        L.append("> 這個排名只反映「數字與具名實體有多少」。硬體規格文幾乎一定排前面，")
        L.append("> 但它們常常是延伸討論，不是當期新聞。看這個榜請只用來找「哪則最有數字可引用」。")
        L.append("")
        for i, c in enumerate(brief["density_reference"], 1):
            L.append("%d. [%d] %s" % (i, c["density"], c["summary"][:80]))
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

