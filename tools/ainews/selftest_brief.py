# -*- coding: utf-8 -*-
"""Regression tests for tools/ainews/brief.py (stage 3b: writing brief).

The brief is the machine's half of the job, so the tests are about the two ways
that half can go wrong:

  it can MISS material   -> a real headline story never becomes a candidate
  it can ADD noise       -> sponsors, dates, label words fill the candidates

Every rule in this file started as a bug seen on real data; the docstring of each
test says which one.

Usage: python tools/ainews/selftest_brief.py   (exit 0 = all passed)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brief as B  # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + name + ("" if cond else "  " + str(detail)))
    if not cond:
        FAILS.append(name)


def sec(key, text, title=""):
    return {"key": key, "title": title or key, "text": text}


def doc(**kw):
    base = {
        "messageId": "m1",
        "subject": "[AINews] Test",
        "date": "2026-11-07T03:05:54Z",
        "display_url": "https://example.invalid/x",
        "lede": "The framing paragraph.",
        "sections": [],
        "stats": {"sections": 5, "chars": 90000, "words": 9000,
                  "headings": 40, "quantities": 120},
    }
    base.update(kw)
    return base


def main():
    # t1: a story carrying numbers, entities and a benchmark outranks filler.
    #     BUG: without scoring, the first bullet in the issue became the headline.
    d = doc(sections=[
        sec("twitter",
            "* **Inkling 2 Small is out:** Thinking Machines released a 594B MoE "
            "scoring 81.7% on ARC-AGI-2 at $0.27 per task.\n"
            "* Some people discussed the vibes of the release in general terms.\n",
            "AI Twitter Recap")])
    cands = B.headline_candidates(d)
    check("t1 highest-scoring story first",
          cands and "Inkling" in cands[0]["summary"], cands[:1])

    # t2: numbers without a unit are not 'hard numbers'.
    #     BUG: the date 2026-11-06 was counted as a quantity.
    check("t2a date is not a quantity", not B.NUM.findall("published 2026-11-06"))
    check("t2b unit number is a quantity", bool(B.NUM.findall("594B")), B.NUM.findall("594B"))
    check("t2c percent is a quantity", bool(B.NUM.findall("81.7%")))

    # t3: label words must not become entities.
    #     BUG: "Announced", "Architecture", "Available" outscored the model name,
    #     because every sentence-initial capital counted.
    ents = B._entities("Launch: Announced at 31 on the Index. Available now on Tinker.")
    check("t3 label words excluded",
          all(e.lower() not in ("launch", "announced", "available") for e in ents), ents)
    check("t3b known proper noun kept", any("Tinker" in e for e in ents), ents)

    # t4: near-identical bullets collapse to one candidate.
    #     BUG: a fixture with "Launch 0..5" produced six identical candidates.
    d4 = doc(sections=[sec("twitter",
                           "\n".join("* Release %d: the 594B model scored 81.7%% now."
                                     % i for i in range(6)))])
    c4 = B.headline_candidates(d4, top=5)
    check("t4 near-duplicates deduped", len(c4) == 1, len(c4))

    # t5: the source's own hedges are surfaced so they stay hedged.
    #     BUG: 'reportedly' claims were being written as fact.
    d5 = doc(sections=[sec("twitter",
                           "* GPT-6.2 Astra is reportedly visible in Codex analytics.\n"
                           "* The model is confirmed to ship on Tuesday.\n")])
    flagged = B.flagged_claims(d5)
    check("t5 hedge flagged", any("reportedly" in f["text"] for f in flagged), flagged)
    check("t5b plain statement not flagged",
          not any("confirmed to ship" in f["text"] for f in flagged), flagged)

    # t6: sponsor strings must land in do_not_write.
    d6 = doc(sections=[sec("twitter",
                           "Join Andrew Ng and AI engineers at NODES 2026 for sessions.\n")])
    check("t6 sponsor detected", "nodes 2026" in B.do_not_write(d6), B.do_not_write(d6))

    # t7: verdict downgrades a thin or promotional issue.
    #     BUG: an activity announcement would have been written as a 9k digest.
    thin = doc(stats={"sections": 2, "chars": 5000, "words": 500,
                      "headings": 4, "quantities": 3})
    check("t7 thin issue -> short", B.verdict(thin)["mode"] == "short", B.verdict(thin))
    promo = doc(subject="[AINews] Behind Latent Space: Kill My SaaS",
                stats={"sections": 6, "chars": 90000, "words": 9000,
                       "headings": 40, "quantities": 200})
    check("t7b promo issue -> short", B.verdict(promo)["mode"] == "short", B.verdict(promo))
    check("t7c rich issue -> digest", B.verdict(doc())["mode"] == "digest")

    # t8: the rendered brief carries the checklist a writer needs.
    md = B.render_markdown(B.build_brief(d))
    for needle in ("頭條候選", "數字清單", "交稿前自檢"):
        check("t8 brief has %s" % needle, needle in md)

    # t9: contradiction watch surfaces a unit with many distinct values.
    d9 = doc(sections=[sec("twitter",
                           "* A scored 61%, another 64%, a third 71%, a fourth 81.7%.\n")])
    cw = B.contradiction_watch(d9)
    check("t9 percent spread surfaced", any(c["unit"] == "%" for c in cw), cw)

    print("\n%s (%d failed)" % ("ALL PASSED" if not FAILS else "FAILURES: " + ", ".join(FAILS), len(FAILS)))
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
