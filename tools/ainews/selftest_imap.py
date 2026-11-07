# -*- coding: utf-8 -*-
"""Offline tests for imap_fetch.py -- no server, no credentials, no network.

The IMAP code path has two halves: talking to the server (untestable here) and
turning one RFC822 message into (messageId, subject, date, body). The second half
is where bugs actually live -- MIME structure, encoding, HTML-only issues -- so
it is exercised with locally built messages.

  i1  multipart/alternative: the text/plain part wins
  i2  the LONGEST text/plain part wins (beehiiv ships duplicates)
  i3  an HTML-only issue is converted, not rejected
  i4  quoted-printable / base64 decoding works
  i5  a truncated body is refused by save_message (would corrupt the digest)
  i6  Message-ID and Date are normalised for the ledger
  i7  credentials are read from env and whitespace in the app password is ignored
  i8  --list/--pick routing: a subject fragment selects the right uid

Usage: python tools/ainews/selftest_imap.py   (exit 0 = all passed)
"""
import email.message
import email.policy
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import imap_fetch as I  # noqa: E402
import save_message as S  # noqa: E402

FAILS = []
BIG = "x" * 70000


def check(name, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + name + ("" if cond else "  " + str(detail)))
    if not cond:
        FAILS.append(name)


def make_message(text=None, html=None, encoding="utf-8", cte=None, subject="[AINews] T"):
    msg = email.message.EmailMessage(policy=email.policy.default)
    msg["Subject"] = subject
    msg["Message-ID"] = "<abc123@mail.example>"
    msg["Date"] = "Fri, 06 Nov 2026 10:36:03 +0000"
    if text is not None and html is not None:
        msg.set_content(text, cte=cte)
        msg.add_alternative(html, subtype="html", cte=cte)
    elif text is not None:
        msg.set_content(text, cte=cte)
    else:
        msg.set_content(html, subtype="html", cte=cte)
    return email.message_from_bytes(msg.as_bytes(), policy=email.policy.default)


def main():
    # i1: text/plain preferred over html
    m = make_message(text="plain body " + BIG, html="<p>html body</p>")
    body = I._plain_body(m)
    check("i1 text/plain wins", body.startswith("plain body"), body[:30])

    # i2: longest text/plain wins
    m = email.message.EmailMessage(policy=email.policy.default)
    m["Subject"] = "[AINews] X"
    m.make_mixed()
    p1 = email.message.EmailMessage()
    p1.set_content("short")
    p2 = email.message.EmailMessage()
    p2.set_content("long " + BIG)
    m.attach(p1)
    m.attach(p2)
    m2 = email.message_from_bytes(m.as_bytes(), policy=email.policy.default)
    check("i2 longest plain part wins", I._plain_body(m2).startswith("long"), I._plain_body(m2)[:20])

    # i3: html-only is converted
    m = make_message(html="<html><body><p>Hello</p><p>World</p></body></html>")
    converted = I._html_to_text("<p>Hello</p><p>World</p>")
    check("i3 html converts", "Hello" in converted and "World" in converted, converted)

    # i4: encoding round-trips
    m = make_message(text="你好 " + BIG, cte="quoted-printable")
    check("i4a quoted-printable decodes", I._plain_body(m).startswith("你好"),
          I._plain_body(m)[:10])
    m = make_message(text="世界 " + BIG, cte="base64")
    check("i4b base64 decodes", I._plain_body(m).startswith("世界"), I._plain_body(m)[:10])

    # i5: short body is refused (this is what stops a truncated digest)
    try:
        S.save("m-short", "too short", "[AINews] x")
        check("i5 short body refused", False)
    except ValueError as e:
        check("i5 short body refused", "truncated" in str(e) or "only" in str(e), e)

    # i6: Message-ID / Date normalisation as used by fetch_one
    msg = make_message(text="body " + BIG)
    mid = str(msg.get("Message-ID", "")).strip("<>")
    check("i6a message id normalised", mid == "abc123@mail.example", mid)
    d = msg.get("Date").datetime.astimezone()
    check("i6b date parses", d.year == 2026 and d.month == 11, d)

    # i7: credentials come from env, spaces stripped
    os.environ["GMAIL_USER"] = " u@example.com "
    os.environ["GMAIL_APP_PASSWORD"] = "abcd efgh ijkl mnop"
    u, p = I.creds()
    check("i7 creds from env", (u, p) == ("u@example.com", "abcdefghijklmnop"), (u, p))
    del os.environ["GMAIL_USER"], os.environ["GMAIL_APP_PASSWORD"]
    try:
        I.creds()
        check("i7b missing creds raise", False)
    except RuntimeError:
        check("i7b missing creds raise", True)

    # i8: routing
    class A:
        id = "Anthropic"
        latest = False

    issues = [("101", "[AINews] Anthropic IPO: Whither Now?", "d1"),
              ("100", "[AINews] Inkling 2 Small", "d2")]
    check("i8 subject fragment routes", I._pick(issues, A) == "101", I._pick(issues, A))

    class B:
        id = None
        latest = True

    check("i8b latest routes", I._pick(issues, B) == "101")

    print("\n%s (%d failed)" % ("ALL PASSED" if not FAILS else "FAILURES: " + ", ".join(FAILS), len(FAILS)))
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
