# -*- coding: utf-8 -*-
"""Regression tests for tools/ainews/detect.py.

The whole point of the detector is that detection may be frequent while the
WRITE stays idempotent. So the tests are mostly about "what does NOT fire":

  t1  a known messageId already in the ledger        -> not new
  t2  a messageId whose post already exists          -> not new (cold-ledger backfill)
  t3  a genuinely new issue                          -> new, and recorded once
  t4  the same new issue seen twice                  -> recorded once only
  t5  paged payload repeating one message            -> one record, not two
  t6  non-AINews senders / other subjects            -> ignored
  t7  the nested {results:[{response:{data:...}}]} envelope -> parsed
  t8  slugify() reproduces the slug of posts already published

Runs against a throwaway repo tree in a temp dir; nothing outside it is written.

Usage:
    python tools/ainews/selftest.py
Exit code: 0 = all passed, 1 = at least one failure.
"""
import io
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import detect  # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("PASS  %s" % name)
    else:
        print("FAIL  %s %s" % (name, detail))
        FAILS.append(name)


def msg(mid, subject, sender="Latent Space <lspace@mail.beehiiv.com>", ts="2026-11-07T03:05:54Z"):
    return {
        "messageId": mid,
        "threadId": mid,
        "subject": subject,
        "sender": sender,
        "messageTimestamp": ts,
        "display_url": "https://mail.google.com/mail/u/0/#inbox/%s" % mid,
    }


def main():
    tmp = tempfile.mkdtemp(prefix="ainews-selftest-")
    try:
        root = os.path.join(tmp, "repo")
        os.makedirs(os.path.join(root, "source", "_posts"))
        os.makedirs(os.path.join(root, "tools", "ainews"))

        # one already-published post, so t2 can exercise the cold-ledger path
        published_slug = detect.slugify("[AINews] Anthropic IPO: Whither Now?")
        with io.open(os.path.join(root, "source", "_posts", published_slug + ".md"),
                     "w", encoding="utf-8") as f:
            f.write("---\ntitle: x\n---\n")

        ledger = {"version": 1, "issues": {
            "1a19fe7ff898cb7e": {
                "subject": "[AINews] LLMs can read & write neural network weights!?!?",
                "slug": "ainews-weight-space-programming-zh",
                "date": "2026-11-03T05:35:42Z",
                "status": "published",
            }
        }}
        detect.save_ledger(ledger, root)

        NEW = "1aZZZnewissue0001"
        NEW_SUBJECT = "[AINews] Finetuning Is All You Need?"

        # t1/t3: mixed payload
        payload = {"data": {"messages": [
            msg("1a19fe7ff898cb7e", "[AINews] LLMs can read & write neural network weights!?!?"),
            msg("1a1b3f849653d148", "[AINews] Anthropic IPO: Whither Now?"),
            msg(NEW, NEW_SUBJECT),
            msg("spam01", "Best crypto deals", sender="spam@example.com"),
            msg("other01", "[AINews] not from the right sender", sender="someone@example.com"),
        ]}}
        led = detect.load_ledger(root)
        found = detect.detect(payload, led, root)
        check("t1 ledger hit is not new", all(r["messageId"] != "1a19fe7ff898cb7e" for r in found))
        check("t2 existing post is not new", all(r["messageId"] != "1a1b3f849653d148" for r in found))
        check("t3 new issue detected", [r["messageId"] for r in found] == [NEW], found)
        check("t6 non-AINews ignored",
              all(r["messageId"] not in ("spam01", "other01") for r in found))

        # t3b: record it, then re-detect
        detect.save_ledger(detect.record(found, led), root)
        led2 = detect.load_ledger(root)
        again = detect.detect(payload, led2, root)
        check("t4 second sighting is a no-op", again == [], again)
        check("t4 ledger holds exactly one new entry",
              list(k for k in led2["issues"] if k == NEW) == [NEW])

        # t5: paging repeats a message inside one payload
        dup = {"messages": [msg("dup0001", "[AINews] Twice"), msg("dup0001", "[AINews] Twice")]}
        led3 = {"version": 1, "issues": {}}
        d = detect.detect(dup, led3, root)
        check("t5 repeated message deduped", len(d) == 1, d)

        # t7: nested multi-tool envelope
        nested = {"results": [{"response": {"data": {"messages": [msg("nested01", "[AINews] Nested")]}}}]}
        n = detect.detect(nested, {"version": 1, "issues": {}}, root)
        check("t7 nested envelope parsed", [r["messageId"] for r in n] == ["nested01"], n)

        # t8: slug must match the post already on the site for that issue.
        # (The weight-space issue's slug was chosen by hand, not derived from
        # its subject; the ledger records that mapping, so this asserts the
        # derived form is at least stable and safe, not that it equals the
        # hand-picked one.)
        check("t8a slug matches published post",
              published_slug == "ainews-anthropic-ipo-whither-now-zh", published_slug)
        derived = detect.slugify("[AINews] LLMs can read & write neural network weights!?!?")
        check("t8b derived slug is clean ascii + suffix",
              derived.startswith("ainews-") and derived.endswith("-zh")
              and derived.replace("-", "").isalnum(), derived)

        # t9: the real ledger in the repo parses and is keyed by messageId
        real = os.path.join(detect.repo_root(), "tools", "ainews", detect.LEDGER_NAME)
        if os.path.exists(real):
            data = json.load(io.open(real, encoding="utf-8"))
            check("t9 repo ledger parses", isinstance(data.get("issues"), dict), type(data))
            check("t9 every entry has a slug",
                  all("slug" in v for v in data["issues"].values()))

        # t10: corrupt ledger is an error, not a silent reset (would re-post everything)
        with io.open(os.path.join(root, "tools", "ainews", detect.LEDGER_NAME), "w",
                     encoding="utf-8") as f:
            f.write("{ not json")
        try:
            detect.load_ledger(root)
            check("t10 corrupt ledger raises", False)
        except ValueError:
            check("t10 corrupt ledger raises", True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n%s (%d failed)" % ("ALL PASSED" if not FAILS else "FAILURES: " + ", ".join(FAILS), len(FAILS)))
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
