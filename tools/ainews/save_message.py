# -*- coding: utf-8 -*-
"""Save a Gmail message payload to out/<messageId>/message.json -- the missing link.

THE PROBLEM THIS SOLVES
-----------------------
The fetch tool returns the body inline, but a real AINews issue is 170-220 KB.
Tool output gets truncated in the transcript, and the tool's own cache file is
not reachable from a normal shell, so "just save what came back" does not work.

The pipeline therefore needs the payload written to disk BY THE PROCESS THAT
RECEIVED IT, i.e. the agent session must write the file. This helper makes that
step one command and validates the result, so a truncated write fails loudly
instead of producing a mysteriously short digest two stages later.

USAGE (agent session)
    # after GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID, write the text/plain body to a
    # file, then:
    python tools/ainews/save_message.py --id <messageId> --body-file body.txt \
        --subject "[AINews] ..." [--date 2026-11-06T10:36:03Z] [--url ...]

    # or from an already-saved JSON response:
    python tools/ainews/save_message.py --id <messageId> --json-response resp.json

Exit codes: 0 = saved and sane, 1 = refused (too short / empty / missing id).
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import detect  # noqa: E402
import extract as X  # noqa: E402

# A real issue's plain-text body is ~200 KB. Anything under this is almost
# certainly a truncated tool response, and letting it through would produce a
# digest built on a fragment -- the worst possible failure for this pipeline.
MIN_BODY = 60_000


def out_dir(message_id, root=None):
    return os.path.join(root or detect.repo_root(), "tools", "ainews", "out", message_id)


def save(message_id, body, subject="", date="", url="", sender="", root=None):
    if not message_id:
        raise ValueError("message_id is required (it is the ledger key)")
    if len(body) < MIN_BODY:
        raise ValueError("body is only %d chars (< %d). This is almost always a "
                         "truncated fetch response; save the full text/plain part."
                         % (len(body), MIN_BODY))
    d = out_dir(message_id, root)
    os.makedirs(d, exist_ok=True)
    payload = {"data": {
        "messageId": message_id,
        "threadId": message_id,
        "subject": subject,
        "sender": sender or "Latent Space <lspace@mail.beehiiv.com>",
        "messageTimestamp": date,
        "display_url": url or ("https://mail.google.com/mail/u/0/#inbox/%s" % message_id),
        "messageText": body,
    }}
    path = os.path.join(d, "message.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False)
        f.write("\n")
    return path, len(body)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Persist a fetched AINews message for the pipeline.")
    ap.add_argument("--id", required=True, help="Gmail messageId (ledger key)")
    ap.add_argument("--body-file", help="file holding the plain-text body")
    ap.add_argument("--json-response", help="saved GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID response")
    ap.add_argument("--subject", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--url", default="")
    args = ap.parse_args(argv)

    if args.json_response:
        with open(args.json_response, "r", encoding="utf-8-sig") as f:
            raw = json.load(f)
        msg = X._pick_message(raw)
        if msg is None:
            print("ERROR: no message object in %s" % args.json_response, file=sys.stderr)
            return 1
        body = msg.get("messageText") or X._body_from_payload(msg.get("payload") or {})
        subject = args.subject or msg.get("subject", "")
        date = args.date or msg.get("messageTimestamp", "")
        url = args.url or msg.get("display_url", "")
    elif args.body_file:
        with open(args.body_file, "r", encoding="utf-8-sig") as f:
            body = f.read()
        subject, date, url = args.subject, args.date, args.url
    else:
        ap.error("either --body-file or --json-response is required")

    try:
        path, n = save(args.id, body, subject, date, url)
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 1
    print("saved %s (%d chars)" % (path, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
