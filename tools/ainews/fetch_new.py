# -*- coding: utf-8 -*-
"""Stage 2a driver: IMAP fetch every AINews issue the ledger has not seen yet.

Why this exists next to imap_fetch.py: that script fetches ONE issue chosen by
hand (useful when backfilling). This one walks the ledger, fetches everything
missing, and stops -- which is what a scheduled job needs.

It is also the only stage that can run fully unattended end to end:

    detect (ledger) -> imap fetch -> extract -> brief

so `--chain` runs all four, and a single cron entry is enough.

USAGE
    python tools/ainews/fetch_new.py                 # fetch all unseen, then chain
    python tools/ainews/fetch_new.py --dry-run
    python tools/ainews/fetch_new.py --no-chain       # fetch only
    python tools/ainews/fetch_new.py --max 1

Exit codes: 0 = nothing to do, 2 = fetched/processed something, 1 = error.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import detect  # noqa: E402
import imap_fetch  # noqa: E402
import save_message  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def _cells(ledger):
    return sorted((ledger.get("issues") or {}).items(),
                  key=lambda kv: kv[1].get("date", ""))


def _run(script, *args):
    cmd = [sys.executable, os.path.join(HERE, script)] + list(args)
    print("\n$ %s" % " ".join(os.path.basename(c) if c == sys.executable else c for c in cmd))
    return subprocess.call(cmd)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Fetch unseen AINews issues over IMAP.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-chain", action="store_true", help="do not run extract/brief")
    ap.add_argument("--max", type=int, default=0, help="stop after N issues")
    args = ap.parse_args(argv)

    try:
        ledger = detect.load_ledger()
    except (OSError, ValueError) as e:
        print("ERROR: ledger unreadable: %s" % e, file=sys.stderr)
        return 1

    # A ledger entry with status "detected" but no message.json is exactly the
    # backlog this script exists to clear.
    todo = []
    for mid, rec in _cells(ledger):
        if rec.get("status") == "published":
            continue
        msg = os.path.join(HERE, "out", mid, "message.json")
        if os.path.exists(msg):
            continue
        todo.append((mid, rec))
    if not todo:
        print("nothing to fetch (every known issue already has a message.json)")
        return 0

    print("%d issue(s) need a body" % len(todo))
    for mid, rec in todo:
        print("  %-18s %-10s %s" % (mid, rec.get("status", "?"), rec.get("subject", "")[:56]))

    # IMAP uids are not the ledger's messageIds, so match on the subject.
    try:
        conn = imap_fetch.connect()
    except Exception as e:                            # noqa: BLE001
        print("ERROR: %s" % e, file=sys.stderr)
        return 1

    fetched = 0
    try:
        issues = imap_fetch.list_issues(conn)
        by_subject = {subj: uid for uid, subj, _d in issues}
        for mid, rec in todo:
            subject = rec.get("subject", "")
            uid = by_subject.get(subject)
            if uid is None:
                # tolerate the subject having been edited slightly
                frag = subject[:40].lower()
                uid = next((u for u, s, _d in issues if frag and frag in s.lower()), None)
            if uid is None:
                print("MISS  %s  (no IMAP match for %r)" % (mid, subject[:50]))
                continue
            if args.dry_run:
                print("WOULD FETCH %s via uid %s" % (mid, uid))
                continue
            message_id, subj, iso, body = imap_fetch.fetch_one(conn, uid)
            try:
                path, n = save_message.save(mid, body, subj or subject, iso)
            except ValueError as e:
                print("FAIL  %s  %s" % (mid, e))
                continue
            print("OK    %s  %d chars -> %s" % (mid, n, os.path.basename(path)))
            fetched += 1
            if args.max and fetched >= args.max:
                break
    finally:
        try:
            conn.logout()
        except Exception:                             # noqa: BLE001
            pass

    if args.dry_run or not fetched:
        return 2 if fetched else 0

    if args.no_chain:
        return 2

    rc = _run("extract_new.py")
    if rc not in (0, 2):
        print("extract_new failed (rc=%d)" % rc, file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
