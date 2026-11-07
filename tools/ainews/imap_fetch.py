# -*- coding: utf-8 -*-
"""Stage 2a: fetch AINews issues over IMAP -- the piece MCP cannot schedule.

WHY IMAP AND NOT THE MCP TOOL
-----------------------------
A real issue is 170-220 KB of plain text. The MCP tool returns it inline, which
means:
  * the transcript truncates it, and
  * the tool's cache is not a filesystem path, so a scheduled process cannot read
    it afterwards.
Result: the payload can only be carried through an agent conversation, which is
exactly what a nightly job cannot do.

IMAP avoids all of that: the server hands over raw RFC822 bytes, Python parses
them, and the body is written straight to disk. No transcript, no cache, no
size ceiling.

CREDENTIALS
-----------
Read from the environment, never from a file in the repo:

    GMAIL_USER=you@gmail.com
    GMAIL_APP_PASSWORD=abcd efgh ijkl mnop     (16-char app password, spaces ok)

An app password requires 2-step verification on the account. A normal account
password will be rejected by Gmail for IMAP as of the last several years.

USAGE
    python tools/ainews/imap_fetch.py --list
    python tools/ainews/imap_fetch.py --latest
    python tools/ainews/imap_fetch.py --id <messageId>
    python tools/ainews/imap_fetch.py --latest --dry-run

Exit codes: 0 = ok (or nothing new), 1 = error, 2 = wrote a message file.
"""
from __future__ import annotations

import argparse
import email
import email.policy
import imaplib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import detect  # noqa: E402
import save_message  # noqa: E402

HOST = "imap.gmail.com"
SEARCH = '(FROM "lspace@mail.beehiiv.com" SUBJECT "AINews")'


def creds():
    user = os.environ.get("GMAIL_USER", "").strip()
    pw = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    if not user or not pw:
        raise RuntimeError(
            "missing credentials: set GMAIL_USER and GMAIL_APP_PASSWORD.\n"
            "  Gmail needs an APP PASSWORD (16 chars) -- 2-step verification -> "
            "App passwords. A normal password will be rejected for IMAP.")
    return user, pw.replace(" ", "")


def connect():
    user, pw = creds()
    m = imaplib.IMAP4_SSL(HOST)
    m.login(user, pw)
    m.select("INBOX", readonly=True)
    return m


def list_issues(m):
    """Return [(uid, subject, date)] for AINews messages, newest first."""
    typ, data = m.uid("SEARCH", None, SEARCH)
    if typ != "OK":
        raise RuntimeError("IMAP search failed: %s" % typ)
    uids = (data[0] or b"").split()
    out = []
    for uid in uids:
        typ, msg_data = m.uid("FETCH", uid, "(BODY.PEEK[HEADER.FIELDS (SUBJECT DATE)])")
        if typ != "OK" or not msg_data:
            continue
        header = b""
        for part in msg_data:
            if isinstance(part, tuple):
                header += part[1]
        msg = email.message_from_bytes(header, policy=email.policy.default)
        out.append((uid.decode(), str(msg.get("Subject", "")).strip(),
                    str(msg.get("Date", "")).strip()))
    out.sort(key=lambda r: r[0], reverse=True)
    return out


def _plain_body(msg):
    """Longest text/plain part, decoded; falls back to HTML stripped of tags."""
    best = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain" and not part.get_filename():
                try:
                    txt = part.get_content()
                except (LookupError, UnicodeDecodeError):
                    payload = part.get_payload(decode=True) or b""
                    txt = payload.decode("utf-8", "replace")
                if len(txt) > len(best):
                    best = txt
    else:
        try:
            best = msg.get_content()
        except (LookupError, UnicodeDecodeError):
            best = (msg.get_payload(decode=True) or b"").decode("utf-8", "replace")
    return best


def _html_to_text(html):
    """Crude but adequate: AINews HTML is linear, so strip tags and keep breaks."""
    html = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", html)
    html = re.sub(r"(?i)<br\s*/?>", "\n", html)
    html = re.sub(r"(?i)</(p|div|tr|li|h[1-6])>", "\n", html)
    html = re.sub(r"<[^>]+>", "", html)
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&quot;", '"'), ("&#39;", "'")):
        html = html.replace(a, b)
    return re.sub(r"\n{3,}", "\n\n", html)


def fetch_one(m, uid):
    """Download one message, return (message_id, subject, date, body)."""
    typ, data = m.uid("FETCH", uid, "(RFC822)")
    if typ != "OK" or not data or not isinstance(data[0], tuple):
        raise RuntimeError("IMAP fetch failed for uid %s" % uid)
    msg = email.message_from_bytes(data[0][1], policy=email.policy.default)

    subject = str(msg.get("Subject", "")).strip()
    date = msg.get("Date")
    iso = date.datetime.astimezone().strftime("%Y-%m-%dT%H:%M:%SZ") if date else ""
    message_id = str(msg.get("Message-ID", "")).strip("<>")

    body = _plain_body(msg)
    if len(body) < save_message.MIN_BODY:
        # html-only issues exist; convert rather than fail
        html = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    try:
                        cand = part.get_content()
                    except (LookupError, UnicodeDecodeError):
                        continue
                    if len(cand) > len(html):
                        html = cand
        if html:
            converted = _html_to_text(html)
            if len(converted) > len(body):
                body = converted
    return message_id, subject, iso, body


def _pick(issues, args):
    if args.id:
        for uid, subject, date in issues:
            if args.id in (uid,):
                return uid
        # fall back to a subject match so a Gmail web id can be used loosely
        for uid, subject, date in issues:
            if args.id.lower() in subject.lower():
                return uid
        return None
    return issues[0][0] if issues else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Fetch AINews issues over IMAP.")
    ap.add_argument("--list", action="store_true", help="list matching issues and exit")
    ap.add_argument("--latest", action="store_true", help="fetch the newest issue")
    ap.add_argument("--id", help="IMAP uid or subject fragment")
    ap.add_argument("--as-message-id",
                    help="store under this id instead of the RFC822 Message-ID "
                         "(the ledger keys issues by its own id, so a mismatch "
                         "makes the pipeline unable to find the file)")
    ap.add_argument("--dry-run", action="store_true", help="show what would be written")
    args = ap.parse_args(argv)

    try:
        m = connect()
    except Exception as e:                            # noqa: BLE001
        print("ERROR: %s" % e, file=sys.stderr)
        return 1

    try:
        issues = list_issues(m)
        if not issues:
            print("no AINews mail found")
            return 0
        if args.list or not (args.latest or args.id):
            for uid, subject, date in issues[:15]:
                print("%-8s %-52s %s" % (uid, subject[:52], date))
            return 0

        uid = _pick(issues, args)
        if uid is None:
            print("ERROR: no issue matched %r" % args.id, file=sys.stderr)
            return 1

        message_id, subject, iso, body = fetch_one(m, uid)
        store_id = args.as_message_id or message_id
        print("uid %s | %s | %d chars body" % (uid, subject[:60], len(body)))
        if args.dry_run:
            print("(dry run: not saved)")
            return 0
        path, n = save_message.save(store_id, body, subject, iso)
        print("saved %s (%d chars)" % (path, n))
        return 2
    finally:
        try:
            m.logout()
        except Exception:                             # noqa: BLE001
            pass


if __name__ == "__main__":
    sys.exit(main())

