# -*- coding: utf-8 -*-
"""Quality check: does the brief rank the story the human actually led with?

Unit tests prove the RULES behave; they do not prove the brief is USEFUL. This
compares the machine's top candidate against the headline the published digest
chose -- if the brief ranks the real story low, the ranking is wrong no matter
how many tests pass.

Needs out/<slug>/extract.json, which only exists after a real issue has been
fetched and extracted. Missing fixtures are reported, not failed: CI has no Gmail
access, and this is a judgement aid rather than a gate.

    python tools/ainews/_check_brief_quality.py
    python tools/ainews/_check_brief_quality.py --strict   # fail when MISS

Exit codes: 0 = all present cases ranked the headline first (or nothing present,
or only MISS in non-strict mode), 1 = a case ranked it below first with --strict,
2 = nothing to check.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brief as B  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# published slug -> tokens that must appear in a good top candidate
CASES = [
    ("ainews-weight-space-programming-zh",
     ["weight space", "weight-space", "read & write", "weights"]),
    ("ainews-anthropic-ipo-whither-now-zh",
     ["anthropic", "ipo", "80b", "1t", "valuation"]),
]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if the headline is not ranked first")
    args = ap.parse_args(argv)

    print("brief quality check (machine ranking vs. the published headline)\n")
    checked = misses = 0
    for slug, expect in CASES:
        path = os.path.join(HERE, "out", slug, "extract.json")
        if not os.path.exists(path):
            print("- %-38s (no extract.json; skipped)" % slug)
            continue
        checked += 1
        with open(path, encoding="utf-8-sig") as f:
            doc = json.load(f)
        cands = B.headline_candidates(doc, top=6)
        hit = None
        for rank, c in enumerate(cands, 1):
            blob = (c["summary"] + " " + " ".join(c["entities"])).lower()
            if any(e in blob for e in expect):
                hit = rank
                break
        top = cands[0]["summary"][:64] if cands else "(none)"
        status = "OK" if hit == 1 else ("RANK %d" % hit if hit else "MISS")
        print("- %-38s %-7s top: %s" % (slug[:38], status, top))
        if hit != 1:
            misses += 1

    if not checked:
        print("\nnothing to check (run extract_new.py on a fetched issue first)")
        return 2

    print("\n%d case(s) checked, %d not ranked first" % (checked, misses))
    print("(advisory: a miss means the scoring weights need work, not that the post was wrong)")
    return 1 if (args.strict and misses) else 0


if __name__ == "__main__":
    sys.exit(main())

