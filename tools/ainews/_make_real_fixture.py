# -*- coding: utf-8 -*-
"""Build a REAL full-message fixture from a saved Gmail JSON response.

Why: the extractor must be validated against a real 200 KB+ AINews body, not
only against the small synthetic fixture. This helper takes a JSON file that
holds the GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID response (any of the supported
envelopes), decodes the text/plain part when messageText is absent, and writes
tools/ainews/fixtures/real-<messageId>.json in the shape extract.py expects.

The fixture keeps messageText (plain text) only -- the 300 KB base64 HTML part
is dropped so the repo does not carry a duplicate of every issue.

Usage:
    python tools/ainews/_make_real_fixture.py <response.json> [--out <path>]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out")
    args = ap.parse_args(argv)

    with open(args.input, "r", encoding="utf-8-sig") as f:
        raw = json.load(f)
    msg = extract._pick_message(raw)
    if msg is None:
        print("ERROR: no message in %s" % args.input, file=sys.stderr)
        return 1

    text = msg.get("messageText") or ""
    if not text.strip():
        text = extract._body_from_payload(msg.get("payload") or {})
    if not text.strip():
        print("ERROR: no body found", file=sys.stderr)
        return 1

    fixture = {
        "_comment": "REAL AINews body captured from Gmail (plain-text part only; "
                    "the base64 HTML part is intentionally dropped). Used to "
                    "validate extract.py against production-sized input.",
        "data": {
            "messageId": msg.get("messageId", ""),
            "threadId": msg.get("threadId", ""),
            "subject": msg.get("subject", ""),
            "sender": msg.get("sender", ""),
            "messageTimestamp": msg.get("messageTimestamp", ""),
            "display_url": msg.get("display_url", ""),
            "messageText": text,
        },
    }
    out = args.out or os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "fixtures", "real-%s.json" % (msg.get("messageId") or "unknown"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(fixture, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %s (%d chars of body)" % (out, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
