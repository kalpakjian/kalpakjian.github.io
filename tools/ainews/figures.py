# -*- coding: utf-8 -*-
"""Stage 4: turn a writing brief into inline SVG figures -- templated, not drawn.

WHY TEMPLATES
-------------
Hand-drawing each chart (what I did for the first two digests) does not scale to
one issue every two days. But "let a model draw an SVG" is worse: text collides,
numbers drift, and the house style breaks.

So this module does neither. It defines four fixed LAYOUTS and fills them from
data the brief already computed:

    kpi_row    big-number cards      <- brief.number_ledger (top quantities)
    bar_compare paired horizontal bars <- headline candidate's numbers
    ranking    ordered list with bars  <- headline_candidates scores
    timeline   two-point change        <- before/after quantities in one claim

Every layout shares tools/diagrams/svglib.py, so the figures match every other
inlined diagram on the site (same dark card, same palette, same font). All SVG is
emitted as ONE unbroken line per element with no blank lines inside <svg> -- the
exact failure that silently deleted every <rect> in an earlier post.

DESIGN RULE: a figure is only produced when the data supports it. If a layout
would need more numbers than the brief has, it is skipped and reported, because a
chart with two invented points is worse than no chart.

USAGE
    python tools/ainews/figures.py --brief out/<id>/brief.json --out out/<id>
    python tools/ainews/figures.py --brief ... --list
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "diagrams"))
try:
    from svglib import Svg, C, TXT, MUT, CARD  # noqa: E402
except ImportError:                               # pragma: no cover
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "tools", "diagrams"))
    from svglib import Svg, C, TXT, MUT, CARD     # noqa: E402

NUMU = re.compile(r"(?<![\d.\-])\d[\d.,]*\s?(?:%|x\b|B\b|T\b|M\b|K\b|k\b|tok/s|ms\b|hours?\b|days?\b|tokens?\b|GW\b)", re.I)

# Mirrors brief.SECTION_LABEL. Duplicated on purpose: figures.py must stay
# importable on its own (it is also used from the ComfyUI-side scripts), and a
# cross-import would drag the whole brief module in for one dict.
SECTION_LABEL = {
    "lede": "主編導言",
    "twitter": "作者已篩選",
    "local": "本地模型圈",
    "reddit_container": "社群討論",
    "less_technical": "非技術討論",
    "other": "其他",
}


def _qty(text):
    """Pull (value, unit, raw) out of '594B' / '81.7%' / '$1T'.

    `$` is stripped before matching so `$1T` behaves exactly like `1T`; treating
    it as part of the pattern made the regex match the inner `1T` and then fail,
    which silently dropped every money figure from the charts.
    """
    clean = (text or "").replace("$", "")
    m = NUMU.search(clean)
    if not m:
        return None
    raw = m.group(0).strip()
    num = re.search(r"\d[\d.,]*", raw)
    if not num:
        return None
    val = num.group(0).replace(",", "").rstrip(".")
    try:
        f = float(val)
    except ValueError:
        return None
    unit = raw[num.end():].strip()
    # keep the leading "$" in the display string when the source had one
    money = (text or "").lstrip().startswith("$") or ("$" + raw) in (text or "")
    return f, unit, ("$" if money else "") + raw


def _fmt(x):
    """Compact axis/number formatting that never shows 594.0."""
    if x == int(x):
        return "%d" % int(x)
    if abs(x) >= 100:
        return "%.0f" % x
    return ("%.2f" % x).rstrip("0").rstrip(".")




# ---------------------------------------------------------------------------
# Layout 1: KPI row -- big numbers on cards
# ---------------------------------------------------------------------------
def fig_kpi_row(items, title, subtitle, aria):
    """2-4 big-number cards. items = [(value_str, label, detail, stage), ...]

    Value size shrinks with card width: `96.32 tokens` at 30px overflowed a
    4-card layout by 1px (caught by _check_fig_layout.py, invisible on screen).
    """
    items = items[:4]
    if len(items) < 2:
        return None
    n = len(items)
    gap = 18
    card_w = (940 - 96 - gap * (n - 1)) / float(n)
    vmax = 30 if card_w >= 250 else (25 if card_w >= 210 else 21)
    s = Svg(940, 300, aria, title, subtitle)
    for i, (val, label, detail, stage) in enumerate(items):
        x = 48 + i * (card_w + gap)
        col = C[stage]
        s.rect(x, 108, card_w, 150, fill=CARD, stroke=col + "55", rx=12)
        s.text(x + 20, 140, _short(label, int(card_w // 8)), 12.5, MUT)
        # 12 chars is what fits at vmax inside card_w - 40
        s.text(x + 20, 196, _short(val, 12), vmax, col, "700")
        if detail:
            s.text(x + 20, 226, _short(detail, 30), 12, TXT)
    return s


# ---------------------------------------------------------------------------
# Layout 2: horizontal bar comparison
# ---------------------------------------------------------------------------
def fig_bar_compare(rows, title, subtitle, aria, unit_hint=""):
    """rows = [(label, value, stage, value_str), ...] sorted by the caller."""
    rows = [r for r in rows if r[1] is not None][:6]
    if len(rows) < 2:
        return None
    top = max(r[1] for r in rows) or 1.0
    h = 130 + 44 * len(rows) + 60
    s = Svg(940, h, aria, title, subtitle)
    bar_x, bar_max = 330, 520
    for i, (label, val, stage, raw) in enumerate(rows):
        y = 120 + i * 44
        col = C[stage]
        # right-align the label so it always ends just before the bar and can
        # never run under it; 18 chars is what fits in the 270px column
        s.text(bar_x - 20, y + 18, _short(label, 18), 12.5, TXT, "normal", "end")
        w = max(3.0, bar_max * (val / top))
        s.rect(bar_x, y, w, 26, fill=col, stroke=col + "66", rx=5)
        s.text(bar_x + w + 10, y + 18, raw, 13, col, "700")
    s.line(bar_x - 12, 106, bar_x - 12, 120 + 44 * len(rows) - 8, stroke="#30363d")
    s.text(48, h - 22, unit_hint or "長條長度 = 數值大小（同一張圖內可比，跨圖不可比）", 11.5, MUT)
    return s


# ---------------------------------------------------------------------------
# Layout 3: ranked list (headline candidates)
# ---------------------------------------------------------------------------
def fig_ranking(groups, title, subtitle, aria):
    """One row per section: its title, and the lead item the source put first.

    Adapted from the old ranked-candidates chart. There is no score bar any more,
    because there is no cross-section ranking; the bar is replaced by the
    section's share of the issue, which is a fact rather than a judgement.
    """
    rows = [g for g in (groups or []) if g.get("items")]
    if len(rows) < 2:
        return None
    h = 130 + 56 * len(rows) + 40
    s = Svg(940, h, aria, title, subtitle)
    stages = ("teal", "blue", "amber", "violet", "gray")
    for i, g in enumerate(rows):
        y = 118 + i * 56
        col = C[stages[i % 5]]
        label = SECTION_LABEL.get(g["section"], g["title"] or g["section"])
        s.text(48, y + 18, _short(label, 14), 12.5, col, "700")
        s.text(48, y + 38, _short(g["items"][0]["summary"], 62), 12, TXT)
        s.text(760, y + 28, "%d 則" % len(g["items"]), 12, MUT, "normal", "end")
    s.line(48, h - 44, 892, h - 44, stroke="#30363d")
    s.text(48, h - 22, "每一列＝一個區塊；第二行是第一則（原文順序，非重要性）", 11.5, MUT)
    return s

def _short(s, n=52):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s or "")
    s = re.sub(r"\*\*|`", "", s).strip()
    return s if len(s) <= n else s[: n - 1] + "…"


# ---------------------------------------------------------------------------
# Layout 4: before/after delta (two bars + the difference called out)
# ---------------------------------------------------------------------------
def fig_delta(before, after, title, subtitle, aria, label_before="之前", label_after="之後"):
    """Two bars: before/after a change. before/after = (value, unit, raw)."""
    if not before or not after:
        return None
    b, a = before[0], after[0]
    top = max(b, a) or 1.0
    h = 330
    s = Svg(940, h, aria, title, subtitle)
    base_y, bar_h, max_w = 250, 40, 520
    for i, (val, raw, stage, lab) in enumerate(
            [(b, before[2], "gray", label_before), (a, after[2], "teal", label_after)]):
        y = 140 + i * 66
        w = max(3.0, max_w * (val / top))
        col = C[stage]
        s.text(60, y + 26, lab, 13, TXT, "600")
        s.rect(170, y + 4, w, bar_h, fill=col, stroke=col + "66", rx=6)
        s.text(170 + w + 12, y + 30, raw, 15, col, "700")
    s.line(170, base_y + 8, 170 + max_w, base_y + 8, stroke="#30363d")
    s.text(60, h - 18, "兩條長條是同一件事的前後；沒有第三條就代表沒有對照組", 11.5, MUT)
    return s


# ---------------------------------------------------------------------------
# driver: pick which figures the brief supports, emit site markup
# ---------------------------------------------------------------------------
LAYOUTS = ("kpi_row", "ranking", "bar_compare", "delta")


def _pick_kpi(brief):
    """Up to 4 quantities that read as headline facts.

    One per section keeps the row meaningful; if a section's first quantity is
    too long for a card (>12 chars) the next one is taken instead of dropping
    the section. With only 2-3 sections an issue still yields 2-4 cards because
    later quantities in the same section are fair game -- the earlier version
    stopped at one per section and produced a single card on a 3-section issue.
    """
    items, seen = [], set()
    for row in brief.get("number_ledger") or []:
        label = _zh_title(row.get("section") or "")
        for raw in row.get("quantities") or []:
            if len(items) >= 4:
                break
            q = _qty(raw)
            if not q or raw in seen or len(raw) > 12:
                continue
            seen.add(raw)
            stage = ("teal", "blue", "amber", "violet")[len(items) % 4]
            items.append((q[2], label, "", stage))
        if len(items) >= 4:
            break
    return items


def _pick_bars(brief):
    """Numbers from the lead item of each section -- ONLY within the same unit.

    A bar chart compares lengths; comparing 594B against 96.32 tok/s is
    meaningless. Rows are grouped by unit and only the largest same-unit group is
    charted. Input changed with the section-grouped brief: candidates now live
    under brief["sections"][i]["items"], and the lead item is the one the source
    itself put first -- which is the honest choice for a comparison chart.
    """
    buckets = {}
    for g in brief.get("sections") or []:
        for it in (g.get("items") or [])[:3]:
            for raw in it.get("numbers") or []:
                q = _qty(raw)
                if not q:
                    continue
                label = _label_for(raw, it.get("summary") or "")
                buckets.setdefault(q[1].lower(), []).append((label, q[0], raw))
    if not buckets:
        return []
    unit, rows = max(buckets.items(), key=lambda kv: len(kv[1]))
    if len(rows) < 2:
        return []
    stages = ("teal", "blue", "amber", "violet", "gray")
    return [(lab, val, stages[i % 5], raw)
            for i, (lab, val, raw) in enumerate(rows[:6])]


def _label_for(raw, summary):
    """Short label for a bar: the words sitting next to the number.

    Returns `"594B total"` rather than the section name -- two bars both
    labelled "AI Twitter Recap" say nothing. Kept short because the label column
    is 240px wide and an over-long label is silently clipped.
    """
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", summary or "")
    s = re.sub(r"\*\*|`", "", s)
    idx = s.find(raw)
    if idx < 0:
        return raw
    tail = s[idx + len(raw): idx + len(raw) + 26].strip(" ，,.:：;")
    word = tail.split()[0].strip("，,.:：;") if tail else ""
    if len(word) < 3 or not word[0].isalpha():
        return raw
    return _short("%s %s" % (raw, word), 20)


def _zh_title(key):
    """Section titles are English in the source; the chart is Chinese."""
    return {
        "lede": "主編導言",
        "twitter": "作者已篩選",
        "local": "本地模型圈",
        "reddit_container": "社群討論",
        "less_technical": "非技術討論",
        "other": "其他",
    }.get(key, key)


def build_figures(brief, tag="FIG"):
    """Return [(marker, html), ...] for every layout the data supports.

    A layout is skipped when its inputs are too thin: one bar is not a chart,
    and a KPI row of a single card is a label.
    """
    out = []
    subject = _short(brief.get("subject") or "", 60)

    kpi = _pick_kpi(brief)
    s = fig_kpi_row(kpi, "這一期的四個硬數字", subject, "本期關鍵量化指標")
    if s:
        cap = "圖 1：本期各區塊最具體的四個數字。數字全部取自原文，未經換算。"
        out.append(("FIG1", s.figure(cap, marker="FIG1")))

    s = fig_ranking(brief.get("sections") or [],
                    "各區塊的頭條（依原文順序）", "第一則＝該區塊頭條；不是跨區塊的重要性排序",
                    "各區塊頭條")
    if s:
        cap = "圖 2：每個區塊的第一則。原文的排列順序就是作者的編輯判斷。"
        out.append(("FIG2", s.figure(cap, marker="FIG2")))

    bars = _pick_bars(brief)
    s = fig_bar_compare(bars, "同一則新聞裡的量級對比", subject, "同一則新聞的數值對比")
    if s:
        cap = "圖 3：同一則新聞內可相比的數值。"
        out.append(("FIG3", s.figure(cap, marker="FIG3")))

    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build templated SVG figures from a brief.")
    ap.add_argument("--brief", required=True)
    ap.add_argument("--out", help="write figures.html / figures.json here")
    ap.add_argument("--list", action="store_true", help="only list which layouts are possible")
    args = ap.parse_args(argv)

    try:
        with open(args.brief, "r", encoding="utf-8-sig") as f:
            brief = json.load(f)
    except (OSError, ValueError) as e:
        print("ERROR: cannot read %s: %s" % (args.brief, e), file=sys.stderr)
        return 1

    figs = build_figures(brief)
    if args.list:
        print("layouts with enough data: %s"
              % (", ".join(m for m, _ in figs) if figs else "(none)"))
        return 0

    for marker, html in figs:
        print(html)
        print()

    if not figs:
        print("(no figure: the brief does not carry enough comparable numbers)")
        return 0

    if args.out:
        os.makedirs(args.out, exist_ok=True)
        hp = os.path.join(args.out, "figures.html")
        with open(hp, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n\n".join(h for _, h in figs) + "\n")
        print("wrote: %s" % hp, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

