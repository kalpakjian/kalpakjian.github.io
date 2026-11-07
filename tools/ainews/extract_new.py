# -*- coding: utf-8 -*-
"""Stage 2 driver: extract every newly detected issue into out/<messageId>/.

The Gmail fetch itself needs the Composio MCP tool (an agent session), so this
script does not talk to Gmail. It joins the two halves:

    agent:  GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID -> out/<id>/message.json
    here :  out/<id>/message.json             -> out/<id>/source.txt + extract.json

It walks the ledger, finds entries with status=detected that have a message.json
but no source.txt yet, and extracts them. That makes it safely re-runnable: an
already-extracted issue is skipped, so it can run on the same timer as the poll.

USAGE
    python tools/ainews/extract_new.py                 # all pending
    python tools/ainews/extract_new.py --only <id>     # one issue
    python tools/ainews/extract_new.py --force         # re-extract everything
    python tools/ainews/extract_new.py --dry-run       # say what would happen

Exit codes: 0 = nothing pending / all succeeded, 2 = something was extracted,
1 = at least one failure.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import detect  # noqa: E402
import extract  # noqa: E402

OUT_NAME = "out"


def out_root(root=None):
    return os.path.join(root or detect.repo_root(), "tools", "ainews", OUT_NAME)


def issue_dir(message_id, root=None):
    return os.path.join(out_root(root), message_id)


def pending(ledger, root=None, only=None, force=False):
    jobs = []
    for mid, rec in sorted(ledger.get("issues", {}).items()):
        if only and mid != only:
            continue
        if not force and rec.get("status") not in ("detected", "extracted"):
            continue
        d = issue_dir(mid, root)
        msg_path = os.path.join(d, "message.json")
        txt_path = os.path.join(d, "source.txt")
        if not os.path.exists(msg_path):
            jobs.append((mid, d, "no-message.json"))
            continue
        if os.path.exists(txt_path) and not force:
            continue
        jobs.append((mid, d, "ready"))
    return jobs


def run_job(message_id, d, root=None):
    with open(os.path.join(d, "message.json"), "r", encoding="utf-8-sig") as f:
        raw = json.load(f)
    msg = extract._pick_message(raw)
    if msg is None:
        raise ValueError("message.json holds no message object")
    doc = extract.extract_message(msg)
    txt, js = extract.write_outputs(doc, d)
    return doc, txt, js


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Extract pending AINews issues to text.")
    ap.add_argument("--only", help="extract just this messageId")
    ap.add_argument("--force", action="store_true", help="re-extract even if source.txt exists")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--root", help="repo root override")
    args = ap.parse_args(argv)

    root = args.root or detect.repo_root()
    try:
        ledger = detect.load_ledger(root)
    except (OSError, ValueError) as e:
        print("ERROR: ledger unreadable: %s" % e, file=sys.stderr)
        return 1

    jobs = pending(ledger, root, args.only, args.force)
    if not jobs:
        print("nothing pending")
        return 0

    failures = 0
    extracted = 0
    for mid, d, why in jobs:
        if why == "no-message.json":
            print("SKIP %s  (waiting for the agent to save message.json)" % mid)
            continue
        if args.dry_run:
            print("WOULD EXTRACT %s -> %s" % (mid, d))
            continue
        try:
            doc, txt, js = run_job(mid, d, root)
        except Exception as e:                      # noqa: BLE001 - report, keep going
            print("FAIL %s: %s: %s" % (mid, type(e).__name__, e))
            failures += 1
            continue
        st = doc["stats"]
        print("OK   %s  sections=%d chars=%d -> %s"
              % (mid, st["sections"], st["chars"], os.path.basename(txt)))
        extracted += 1
        _mark(ledger, mid, "extracted", root)

    if failures:
        print("\n%d failure(s)" % failures)
        return 1
    return 2 if extracted else 0


def _mark(ledger, message_id, status, root=None):
    rec = ledger.get("issues", {}).get(message_id)
    if not rec:
        return
    rec["status"] = status
    detect.save_ledger(ledger, root)


if __name__ == "__main__":
    sys.exit(main())
