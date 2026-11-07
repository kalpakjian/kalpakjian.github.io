# -*- coding: utf-8 -*-
"""Check that the cover motif matches the story (advisory, no rendering).

Motif selection is the one creative choice in the pipeline, so it gets its own
check: feed the subjects of the two published digests and assert the chosen scene
is the one a human would have picked.

    python tools/ainews/_check_motifs.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cover  # noqa: E402

# subject / headline -> expected motif, from what the published covers show
CASES = [
    ("[AINews] Anthropic IPO: Whither Now?",
     "A gigantic valuation, $1T vs $1.5T", "money"),
    ("[AINews] LLMs can read & write neural network weights!?!?",
     "Weight Space Programming reads weights directly", "weights"),
    ("[AINews] Inkling 2 Small: 17A-594B trained in 68 hours",
     "Thinking Machines launched a new open-weight model", "model_release"),
]


def main():
    fails = 0
    for subject, summary, want in CASES:
        brief = {"subject": subject,
                 "headline_candidates": [{"summary": summary, "score": 10, "numbers": []}]}
        got = cover.pick_motif(brief)
        ok = got == want
        print(("PASS  " if ok else "FAIL  ") + "%-46s -> %-14s (want %s)"
              % (subject[:46], got, want))
        if not ok:
            fails += 1
    print("\n%s" % ("ALL PASSED" if not fails else "%d mismatch" % fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
