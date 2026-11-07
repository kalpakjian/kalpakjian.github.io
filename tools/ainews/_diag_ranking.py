# -*- coding: utf-8 -*-
"""Diagnose WHY the headline ranking failed -- per-candidate score breakdown.

The failure is known (Inkling ranked 6th on an issue where it was the lead
story). What is not known is which term did the damage. This prints, for the top
N candidates, the exact contribution of each scoring component plus the section
the candidate came from, so the fix can target the actual cause instead of
re-weighting blindly.

    python tools/ainews/_diag_ranking.py <messageId>
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brief as B  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    if len(sys.argv) < 2:
        print("usage: _diag_ranking.py <messageId>", file=sys.stderr)
        return 2
    mid = sys.argv[1]
    path = os.path.join(HERE, "out", mid, "extract.json")
    with open(path, encoding="utf-8-sig") as f:
        doc = json.load(f)

    print("issue: %s" % doc.get("subject"))
    print("sections in order:")
    for s in doc.get("sections") or []:
        print("  [%d] %-16s %6d chars  %s"
              % (s.get("index"), s.get("key"), len(s.get("text") or ""),
                 (s.get("title") or "")[:40]))

    print("\ntop 12 candidates with score anatomy:")
    cands = B.headline_candidates(doc, top=12)
    for i, c in enumerate(cands, 1):
        w = c["why"]
        print("%2d. [%3d] %-14s nums=%-2d ent=%-2d bench=%-2d novel=%-2d  %s"
              % (i, c["score"], c["section"], w["numbers"], w["entities"],
                 w["benchmarks"], w["novelty"], c["summary"][:60]))

    print("\ndid the real story appear at all?")
    for needle in ("Inkling", "Kimi K3.1", "Anthropic", "Weight Space", "open weight"):
        hits = [(i + 1, c["summary"][:50]) for i, c in enumerate(cands)
                if needle.lower() in (c["summary"] + " " + " ".join(c["entities"])).lower()]
        print("  %-14s %s" % (needle, hits if hits else "ABSENT from top 12"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
