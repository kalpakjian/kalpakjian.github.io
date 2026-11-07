# -*- coding: utf-8 -*-
"""Probe: what does IMAP actually hand us for an AINews issue?

The MCP tool returned ~173 KB of markdown-ish text for the IPO issue. IMAP's
text/plain part measures ~58 KB for the same mail. Before building on either, we
need to know whether IMAP is
    (a) a shorter summary, or
    (b) the same content, differently wrapped.

How to tell without rendering anything: compare section headings, look for the
known marker strings, and count how far the body goes. If IMAP has
"# AI Twitter Recap" AND "AI Reddit Recap" AND the footer, it is the full issue
in a different encoding, and 58 KB is just the real size of the text.

    python tools/ainews/_probe_imap.py --uid 77129
"""
import argparse
import email
import email.policy
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import imap_fetch as I  # noqa: E402

MARKERS = [
    ("sponsor (NODES 2026)", "NODES 2026"),
    ("masthead", "AI News for"),
    ("twitter recap", "AI Twitter Recap"),
    ("reddit recap", "AI Reddit Recap"),
    ("localLlama group", "LocalLlama"),
    ("footer", "plain text version"),
    ("inkling", "Inkling"),
    ("schulman", "Schulman"),
    ("vals", "Vals"),
    ("ipo", "IPO"),
]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--uid", required=True)
    args = ap.parse_args(argv)

    m = I.connect()
    try:
        typ, data = m.uid("FETCH", args.uid, "(RFC822)")
        msg = email.message_from_bytes(data[0][1], policy=email.policy.default)
        print("subject:", msg.get("Subject"))
        print("date   :", msg.get("Date"))
        parts = []
        for part in msg.walk():
            ct = part.get_content_type()
            fn = part.get_filename()
            payload = part.get_payload(decode=True) or b""
            parts.append((ct, fn, len(payload)))
        print("\nparts:")
        for ct, fn, n in parts:
            print("  %-28s %-22s %8d bytes" % (ct, fn or "-", n))

        body = I._plain_body(msg)
        print("\nchosen text/plain: %d chars" % len(body))
        print("first 300:\n%s\n" % body[:300].replace("\r", ""))
        print("last 200:\n%s\n" % body[-200:].replace("\r", ""))

        print("markers:")
        for name, needle in MARKERS:
            print("  %-22s %s" % (name, "YES" if needle in body else "no"))

        heads = re.findall(r"^#{1,3}\s+(.+)$", body, re.M)
        print("\nmarkdown headings found: %d" % len(heads))
        for h in heads[:12]:
            print("   ", h[:60])

        # does it contain the deep technical detail we used in the digest?
        for probe in ("Schulman", "circumvent guardrails", "APEX-Agents", "81.7",
                      "CyberOffense", "Daybreak", "178.6"):
            print("  detail %-22s %s" % (probe, "YES" if probe in body else "no"))
    finally:
        try:
            m.logout()
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
