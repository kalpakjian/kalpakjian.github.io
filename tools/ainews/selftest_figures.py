# -*- coding: utf-8 -*-
"""Regression tests for tools/ainews/figures.py (stage 4: templated SVG).

A templated chart can be wrong in ways a unit test normally misses, so the tests
target exactly the defects seen while building this:

  f1  `$1T` parses (an earlier regex returned None and dropped every $ figure)
  f2  the date 2026-11-06 is NOT a quantity
  f3  a bar chart refuses to mix units (594B vs 96.32 tok/s is meaningless)
  f4  one data point is not a chart -> layout skipped, not drawn
  f5  KPI row needs >= 2 cards
  f6  every generated <svg> has NO blank line (the bug that deleted all <rect>)
  f7  every generated svg contains <rect> and <text>
  f8  figures carry a figcaption and the site's figure wrapper
  f9  long values are shortened so they cannot overflow a card
  f10 section keys map to Chinese chart labels

Usage: python tools/ainews/selftest_figures.py   (exit 0 = all passed)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figures as F  # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + name + ("" if cond else "  " + str(detail)))
    if not cond:
        FAILS.append(name)


def main():
    check("f1a $1T parses", F._qty("$1T") == (1.0, "T", "$1T"), F._qty("$1T"))
    check("f1b $80B parses", F._qty("$80B")[0] == 80.0, F._qty("$80B"))
    check("f2 date is not a quantity", F._qty("2026-11-06") is None)
    check("f2b percent parses", F._qty("81.7%")[0] == 81.7)

    # f3: two different units must not become one chart
    brief_mixed = {"headline_candidates": [
        {"summary": "A 594B model", "numbers": ["594B"], "score": 9},
        {"summary": "runs at 96.32 tok/s", "numbers": ["96.32 tok/s"], "score": 8},
    ]}
    bars = F._pick_bars(brief_mixed)
    check("f3 mixed units -> no bar chart", bars == [], bars)

    brief_same = {"headline_candidates": [
        {"summary": "594B total and 17B active", "numbers": ["594B", "17B"], "score": 9}]}
    bars2 = F._pick_bars(brief_same)
    check("f3b same unit -> 2 bars", len(bars2) == 2, bars2)

    # f4/f5: a layout without enough data is skipped rather than drawn badly
    check("f4 single bar -> None", F.fig_bar_compare([("a", 1, "teal", "1B")],
                                                     "t", "s", "a") is None)
    check("f5 one KPI card -> None", F.fig_kpi_row([("1T", "x", "", "teal")],
                                                   "t", "s", "a") is None)

    # f6-f8: markup hygiene on every layout that does produce output
    figs = []
    s = F.fig_kpi_row([("594B", "Twitter 摘要", "", "teal"),
                       ("81.7%", "本地模型圈", "", "blue"),
                       ("96.32 tok/s", "非技術討論", "", "amber")],
                      "四個硬數字", "副標", "aria")
    if s:
        figs.append(("kpi", s.figure("說明", marker="FIG1")))
    s = F.fig_ranking([{"summary": "Inkling 2 Small released with 594B params",
                        "score": 14, "numbers": []},
                       {"summary": "QWEN runs 96 tok/s", "score": 9, "numbers": []}],
                      "頭條排序", "副標", "aria")
    if s:
        figs.append(("ranking", s.figure("說明", marker="FIG2")))
    s = F.fig_bar_compare([("594B total", 594, "teal", "594B"),
                           ("17B active", 17, "blue", "17B")],
                          "量級", "副標", "aria")
    if s:
        figs.append(("bars", s.figure("說明", marker="FIG3")))

    check("f6 three layouts rendered", len(figs) == 3, len(figs))
    for name, html in figs:
        block = re.search(r"<svg\b.*?</svg>", html, re.S)
        check("f6 %s svg has no blank line" % name,
              block is not None and "\n\n" not in block.group(0))
        check("f7 %s has rect+text" % name,
              "<rect" in (block.group(0) if block else "") and
              "<text" in (block.group(0) if block else ""))
        check("f8 %s is a site figure" % name,
              "<figcaption" in html and "figure style=" in html)

    # f9: long values are truncated, so a 12-char cap must hold
    check("f9 long value truncated", len(F._short("96.32 tokens per second", 12)) <= 12)

    # f10: Chinese labels
    check("f10 twitter label is Chinese", F._zh_title("twitter") == "Twitter 摘要")

    # f11: build_figures on a rich brief yields FIG1..FIGn markers
    rich = {
        "subject": "[AINews] Test issue with enough data",
        "number_ledger": [{"section": "twitter", "title": "AI Twitter Recap",
                           "quantities": ["594B", "81.7%"]},
                          {"section": "local", "title": "AI Reddit Recap",
                           "quantities": ["96.32 tok/s"]}],
        "headline_candidates": [
            {"summary": "Inkling 2 Small: 594B total and 17B active", "score": 14,
             "numbers": ["594B", "17B"]},
            {"summary": "QWEN reaches 96.32 tok/s", "score": 9, "numbers": ["96.32 tok/s"]},
        ],
    }
    out = F.build_figures(rich)
    markers = [m for m, _ in out]
    check("f11 markers unique", len(markers) == len(set(markers)), markers)
    check("f11 has FIG1", "FIG1" in markers, markers)

    print("\n%s (%d failed)" % ("ALL PASSED" if not FAILS else "FAILURES: " + ", ".join(FAILS), len(FAILS)))
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
