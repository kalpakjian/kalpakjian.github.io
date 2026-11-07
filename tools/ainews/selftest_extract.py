# -*- coding: utf-8 -*-
"""Regression tests for tools/ainews/extract.py (stage 2).

What matters here is that boilerplate does NOT reach the writer, and that
section boundaries survive -- the two failure modes that made the early
hand-written digests messy:

  t1  sponsor block / masthead / "View image" / "Caption:" / footer removed
  t2  lede captured as its own section
  t3  "# AI Twitter Recap" classified as `twitter`
  t4  empty `## ` + bold crumb folds into the crumb (no stray heading)
  t5  Reddit container splits into `## /r/...` sub-sections (split BEFORE fold)
  t6  invisible characters and lone-CR padding lines are gone
  t7  a message with no body raises instead of writing an empty file
  t8  the base64 text/plain payload fallback works
  t9  stats count sections/quantities plausibly
  t10 the on-disk fixture extracts without leaving boilerplate

Usage: python tools/ainews/selftest_extract.py   (exit 0 = all passed)
"""
import base64
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract  # noqa: E402

FAILS = []
SEP_LINE = "\u2014" * 20


def check(name, cond, detail=""):
    if cond:
        print("PASS  %s" % name)
    else:
        print("FAIL  %s %s" % (name, detail))
        FAILS.append(name)


def build_body():
    return "\u201cSponsor text here\u201c \u2014  \r\n\r\n\r\n" \
        "Lede paragraph one.\u200b\r\n\r\n" \
        "View image: (https://media.beehiiv.com/x.png)\r\nCaption: \r\n" \
        "\u201cAI News for 11/01/2026-11/02/2026 brought to you by\u201c \u2014 \r\n\r\n" \
        + SEP_LINE + "\r\n\r\n" \
        "# AI Twitter Recap\r\n\r\n## \r\n**What happened**\r\n\r\n" \
        "**Bold claim with 594B total.**\r\n\r\n" \
        + SEP_LINE + "\r\n\r\n" \
        "# AI Reddit Recap\r\n\r\n" \
        "## /r/LocalLlama + /r/localLLM Recap\r\n\r\n### 1. Post one\r\n\r\nBody A.\r\n\r\n" \
        "## Less Technical AI Subreddit Recap\r\n\r\n### 2. Post two\r\n\r\nBody B.\r\n\r\n" \
        + SEP_LINE + "\r\n\r\n" \
        "You are reading a plain text version of this post.\r\nhttps://lspace.beehiiv.com/p/x\r\n"


def main():
    msg = {"messageId": "m1", "subject": "[AINews] T", "messageText": build_body()}
    doc = extract.extract_message(msg)
    all_text = "\n".join(s["text"] for s in doc["sections"])

    check("t1a sponsor removed", "Sponsor text" not in all_text)
    check("t1b masthead removed", "brought to you by" not in all_text)
    check("t1c image/caption removed",
          "View image" not in all_text and "Caption:" not in all_text)
    check("t1d footer removed", "reading a plain text version" not in all_text)

    check("t2 lede is its own section",
          doc["lede"].startswith("Lede paragraph one"), doc["lede"][:40])

    keys = [s["key"] for s in doc["sections"]]
    check("t3 twitter classified", "twitter" in keys, keys)

    tw = next(s for s in doc["sections"] if s["key"] == "twitter")
    check("t4 empty H2 folded into crumb",
          "**What happened**" in tw["text"] and not any(
              l.strip() == "##" for l in tw["text"].split("\n")), tw["text"][:60])

    reddit = next(s for s in doc["sections"] if s["key"] == "reddit_container")
    subs = reddit.get("subsections") or []
    check("t5 reddit has 2 sub-sections", len(subs) == 2, [s["title"] for s in subs])
    check("t5a local sub key", subs and subs[0]["key"] == "local", subs[:1])
    check("t5b less-technical sub key", len(subs) == 2 and subs[1]["key"] == "less_technical")
    check("t5c sub bodies kept", "Body A" in subs[0]["text"] and "Body B" in subs[1]["text"])

    check("t6a zero-width removed", "\u200b" not in all_text)
    check("t6b no lone-CR lines", not any(l.strip() == "\r" for l in all_text.split("\n")))
    check("t6c no double blank lines",
          "\n\n\n" not in all_text, repr(all_text[:80]))

    try:
        extract.extract_message({"messageId": "m2", "messageText": "   "})
        check("t7 empty body raises", False)
    except ValueError:
        check("t7 empty body raises", True)

    raw = build_body().encode("utf-8")
    b64 = base64.urlsafe_b64encode(raw).decode().rstrip("=")
    fallback = {"messageId": "m3", "payload": {
        "mimeType": "multipart/alternative",
        "parts": [{"mimeType": "text/html", "body": {"data": "PGI-eA=="}},
                  {"mimeType": "text/plain", "body": {"data": b64}}]}}
    doc3 = extract.extract_message(fallback)
    check("t8 payload fallback works", "Lede paragraph one" in doc3["lede"], doc3["lede"][:40])

    st = doc["stats"]
    check("t9 stats sane",
          st["sections"] >= 3 and st["quantities"] >= 1 and st["words"] > 10, st)

    fixture = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "fixtures", "full-message-sample.json")
    with io.open(fixture, encoding="utf-8") as f:
        raw_msg = json.load(f)
    docf = extract.extract_message(raw_msg["data"])
    full = "\n".join(s["text"] for s in docf["sections"])
    check("t10a fixture extracts", docf["stats"]["sections"] >= 3, docf["stats"])
    check("t10b fixture has no sponsor leakage",
          "Join Andrew Ng" not in full and "NODES 2026" not in full)
    check("t10c fixture lede present", "Thinking Machines" in docf["lede"])

    print("\n%s (%d failed)" % ("ALL PASSED" if not FAILS else "FAILURES: " + ", ".join(FAILS), len(FAILS)))
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
