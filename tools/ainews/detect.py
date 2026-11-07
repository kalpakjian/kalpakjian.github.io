# -*- coding: utf-8 -*-
"""Detect new AINews issues in Gmail and record them in a ledger.

WHY THIS EXISTS
---------------
AINews (Latent Space) lands at an irregular time -- observed arrivals on
2026-11-03 05:35, 11-04 19:18, 11-05 06:24, 11-06 10:36 and 11-07 03:05 UTC.
"Check once a day" therefore has an unbounded lag (up to 24 h) for no benefit,
and "check every minute" is equally pointless if the write is not idempotent.
The real requirement is:

    * detection may run as often as you like, because
    * the WRITE is keyed on Gmail messageId, so a second sighting is a no-op.

That split is what this script implements. It never writes a post, never calls
a model, and never touches the network itself: it takes the message list that
the caller already fetched (see run_ainews_poll.ps1) and decides what is new.
Keeping it I/O-free is what makes it testable (selftest.py) and safe on a timer.

USAGE
-----
    python tools/ainews/detect.py --input payload.json --dry-run
    python tools/ainews/detect.py --input payload.json --notify-dir out/
    python tools/ainews/detect.py --show

EXIT CODES
----------
    0 = no new issue
    2 = at least one new issue found (recorded unless --dry-run)
    1 = error (bad payload, unreadable ledger)

Ledger: tools/ainews/seen.json (committed -- it is the site's memory of which
issues have been covered, so a fresh clone does not republish them).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys

SENDER = "lspace@mail.beehiiv.com"
SUBJECT_PREFIX = "[AINews]"
LEDGER_NAME = "seen.json"

# "[AINews] Anthropic IPO: Whither Now?" -> "ainews-anthropic-ipo-whither-now-zh"
_SLUG_STRIP = re.compile(r"[^a-z0-9]+")


def repo_root() -> str:
    """<repo>/tools/ainews/detect.py -> <repo>. Works from any cwd."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def ledger_path(root=None) -> str:
    return os.path.join(root or repo_root(), "tools", "ainews", LEDGER_NAME)


def slugify(subject: str) -> str:
    """Turn a newsletter subject into the post slug used by this site.

    The "-zh" suffix is deliberate: every AINews post here is a Chinese digest,
    so the slug stays self-describing next to the English original.
    """
    text = subject
    for prefix in (SUBJECT_PREFIX, "AINews", "[AINews]"):
        if text.startswith(prefix):
            text = text[len(prefix):]
    text = _SLUG_STRIP.sub("-", text.lower()).strip("-")
    if len(text) > 60:
        text = text[:60].rstrip("-")
    return "ainews-%s-zh" % (text or "untitled")


def load_ledger(root=None) -> dict:
    path = ledger_path(root)
    if not os.path.exists(path):
        return {"version": 1, "sender": SENDER, "issues": {}}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("issues", {})
    return data


def save_ledger(data: dict, root=None) -> str:
    path = ledger_path(root)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data["updated"] = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, path)  # atomic: a killed run never leaves a half ledger


def _iter_messages(payload):
    """Yield message dicts from the shapes a Gmail payload can take.

    The Composio GMAIL_FETCH_EMAILS response nests as
      {data: {messages: [...]}}                            (direct tool result)
    or
      {results: [{response: {data: {messages: [...]}}}]}    (multi-tool envelope)
    The poll script saves the former; accept both so a hand-saved file works too.
    """
    if isinstance(payload, list):
        for item in payload:
            yield from _iter_messages(item)
        return
    if not isinstance(payload, dict):
        return
    msgs = payload.get("messages")
    if isinstance(msgs, list):
        for m in msgs:
            if isinstance(m, dict):
                yield m
    for key in ("data", "response", "results"):
        if key in payload:
            yield from _iter_messages(payload[key])


def _is_ainews(msg: dict) -> bool:
    sender = (msg.get("sender") or "").lower()
    subject = msg.get("subject") or ""
    return SENDER in sender and subject.strip().startswith(SUBJECT_PREFIX)


def classify(msg: dict, ledger: dict, root=None) -> dict:
    """Normalise one message into the record we keep in the ledger."""
    mid = msg.get("messageId") or ""
    subject = (msg.get("subject") or "").strip()
    slug = slugify(subject)
    post = os.path.join(root or repo_root(), "source", "_posts", slug + ".md")
    return {
        "messageId": mid,
        "threadId": msg.get("threadId") or mid,
        "subject": subject,
        "date": msg.get("messageTimestamp") or "",
        "slug": slug,
        "display_url": msg.get("display_url") or "",
        # A post may already exist even when the ledger is cold (backfill, or an
        # issue I wrote by hand before this tool existed). Treating an existing
        # file as "covered" means the first run on this repo does not re-announce
        # the two issues already published.
        "post_exists": os.path.exists(post),
        "seen": mid in ledger.get("issues", {}),
    }


def detect(payload, ledger: dict, root=None) -> list:
    """Return AINews messages that are neither in the ledger nor already published."""
    out, dupes = [], set()
    for msg in _iter_messages(payload):
        if not _is_ainews(msg):
            continue
        rec = classify(msg, ledger, root)
        if not rec["messageId"] or rec["messageId"] in dupes:
            continue  # paging repeats messages; the ledger key must stay unique
        dupes.add(rec["messageId"])
        if rec["seen"] or rec["post_exists"]:
            continue
        out.append(rec)
    out.sort(key=lambda r: r.get("date") or "")
    return out


def record(found: list, ledger: dict) -> dict:
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for rec in found:
        ledger.setdefault("issues", {})[rec["messageId"]] = {
            "subject": rec["subject"],
            "slug": rec["slug"],
            "date": rec["date"],
            "status": "detected",
            "detected_at": now,
        }
    return ledger


def write_alert(found: list, out_dir: str) -> str:
    """Write the alert as JSONL so the PowerShell notifier needs no JSON parser."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "new-issues.jsonl")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for rec in found:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return path


def _show(root) -> int:
    data = load_ledger(root)
    issues = data.get("issues", {})
    print("ledger: %s" % ledger_path(root))
    if not issues:
        print("  (empty)")
        return 0
    for mid, rec in sorted(issues.items(), key=lambda kv: kv[1].get("date", "")):
        print("  %-18s %-10s %s  %s"
              % (mid, rec.get("status", "?"), rec.get("date", "")[:10], rec.get("slug", "")))
    print("  total: %d" % len(issues))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Detect new AINews issues (ledger-idempotent).")
    ap.add_argument("--input", help="JSON file holding a GMAIL_FETCH_EMAILS payload (- for stdin)")
    ap.add_argument("--dry-run", action="store_true", help="report but do not write the ledger")
    ap.add_argument("--notify-dir", help="write new-issues.jsonl here for the notifier")
    ap.add_argument("--show", action="store_true", help="print the ledger and exit")
    ap.add_argument("--root", help="repo root override (defaults to <script>/../..)")
    args = ap.parse_args(argv)

    root = args.root or repo_root()
    if args.show:
        return _show(root)
    if not args.input:
        ap.error("--input is required unless --show is given")

    try:
        if args.input == "-":
            payload = json.load(sys.stdin)
        else:
            with open(args.input, "r", encoding="utf-8-sig") as f:
                payload = json.load(f)
    except (OSError, ValueError) as e:
        print("ERROR: cannot read payload: %s" % e, file=sys.stderr)
        return 1

    try:
        ledger = load_ledger(root)
    except (OSError, ValueError) as e:
        print("ERROR: ledger is not valid JSON: %s" % e, file=sys.stderr)
        return 1

    found = detect(payload, ledger, root)
    if not found:
        print("no new AINews issue")
        return 0

    for rec in found:
        print("NEW  %s  %s" % (rec["messageId"], rec["subject"]))

    if args.notify_dir:
        print("alert:", write_alert(found, args.notify_dir))

    if args.dry_run:
        print("dry run: ledger not modified")
        return 2

    print("ledger:", save_ledger(record(found, ledger), root))
    return 2


if __name__ == "__main__":
    sys.exit(main())
