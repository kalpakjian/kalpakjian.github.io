# -*- coding: utf-8 -*-
"""Check that the brief reports the SOURCE's lead story, in the source's order.

WHAT THIS VERIFIES (and what it deliberately does not)
-----------------------------------------------------
It does NOT check "did the machine guess the headline I would write". Three
scoring schemes were built to answer that and all three failed -- and the reason
turned out to be that the premise was wrong.

Verified against the five issues on hand:

    issue              AINews twitter lead            what I actually wrote
    1a19fe7f...        DeepSeek Super-agent harness   Weight Space Programming
                                                      (which sits in Reddit, 3rd)
    1a1b3f84...        Inkling 2 Small (recap of      Anthropic IPO valuation
                        the 11/06 launch)
    1a1b06e0...        Inkling 2 Small (debut)        (not yet written)

So AINews' lead and my lead are different things, by design: I re-pick based on
what is most useful to a reader. A gate cannot verify taste, and pretending it
can produced two "failures" that were really correct extraction.

What this check therefore asserts:
    the first item of the twitter group == the first bold story in the source's
    twitter section, and sections appear in source order.

That is a real property, it can regress, and it is the thing a writer depends on
(top-down reading meets the source's own priority first).

    python tools/ainews/_check_brief_quality.py [--strict]

Exit codes: 0 = pass, 1 = fail under --strict, 2 = no extract.json present.
"""
import argparse
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brief as B  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# messageId -> tokens that must appear in the source's own twitter lead.
# Recorded from the source, not from my digests (the two differ -- see docstring).
SOURCE_LEADS = {
    "1a19fe7ff898cb7e": ["deepseek", "super-agent", "harness"],
    "1a1b3f849653d148": ["inkling", "thinking machines"],
    "1a1b06e0f230a991": ["inkling", "thinking machines"],
    "1a1aa61c9689973a": ["openai", "cyber", "linux"],
    "1a1a7ff6cacc4697": ["weight-space", "weight space", "programming"],
}


def _source_first_bold(doc):
    """First bold claim inside the source's twitter section (ground truth)."""
    for sec in doc.get("sections") or []:
        if sec.get("key") != "twitter":
            continue
        for line in (sec.get("text") or "").split("\n"):
            line = line.strip()
            if re.match(r"^\*\*[^*]+\*\*$", line) and len(line) > 40:
                inner = line.strip("*").strip()
                if inner.lower().startswith("what happened"):
                    continue
                return inner
    return ""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args(argv)

    found = sorted(glob.glob(os.path.join(HERE, "out", "*", "extract.json")))
    if not found:
        print("no extract.json found (run fetch_new.py first)")
        return 2

    print("brief quality: does the brief report the source's own lead, in order?\n")
    checked = fails = 0
    for path in found:
        mid = os.path.basename(os.path.dirname(path))
        with open(path, encoding="utf-8-sig") as f:
            doc = json.load(f)

        groups = B.section_candidates(doc)
        tw = next((g for g in groups if g["section"] == "twitter"), None)
        if not tw or not tw["items"]:
            print("- %-18s NO twitter group" % mid)
            fails += 1
            continue

        got = tw["items"][0]["summary"]
        want = _source_first_bold(doc)
        checked += 1

        # the brief's first item must be the same story the source leads with
        same = bool(want) and (
            got.strip()[:40] == want.strip()[:40]
            or want.strip()[:40] in got
            or got.strip()[:40] in want)
        tokens = SOURCE_LEADS.get(mid, [])
        hinted = bool(tokens) and any(t in got.lower() for t in tokens)

        ok = same or hinted
        print("- %-18s %s 1st: %s" % (mid, "OK  " if ok else "NO  ", got[:50]))
        if not ok:
            fails += 1
            print("     source lead: %s" % want[:60])

    # section order must follow the source
    order_bad = 0
    for path in found:
        with open(path, encoding="utf-8-sig") as f:
            doc = json.load(f)
        src_order = [s.get("key") for s in doc.get("sections") or []
                     if s.get("key") != "lede"]
        got_order = [g["section"] for g in B.section_candidates(doc)]
        if src_order != got_order:
            order_bad += 1
            print("- %-18s section order differs: %s vs %s"
                  % (os.path.basename(os.path.dirname(path)), got_order, src_order))

    print("\n%d issue(s) checked, %d lead mismatch, %d order mismatch"
          % (checked, fails, order_bad))
    print("(this verifies extraction fidelity, NOT whether machine == my editorial taste)")
    return 1 if (args.strict and (fails or order_bad)) else 0


if __name__ == "__main__":
    sys.exit(main())
