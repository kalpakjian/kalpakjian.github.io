"""Re-encode a .ps1 file as UTF-8 with BOM (and CRLF).

Windows PowerShell 5.1 reads .ps1 files as ANSI unless there is a UTF-8 BOM.
A BOM-less UTF-8 file with CJK comments therefore gets mojibake, which can
break string terminators and make the whole script fail to parse — and the
error message then points at an unrelated line.

This script reads the file as UTF-8 (ignoring any existing BOM), normalises
to CRLF, and writes it back with a BOM.

Usage:
    python write_ps1.py <target.ps1>
    python write_ps1.py <target.ps1> --check     # report only, don't write
"""
import io
import sys

BOM = b"\xef\xbb\xbf"


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)

    target = sys.argv[1]
    check_only = "--check" in sys.argv

    data = open(target, "rb").read()
    has_bom = data[:3] == BOM
    body = data[3:] if has_bom else data
    text = body.decode("utf-8")
    text = text.replace("\r\n", "\n").replace("\n", "\r\n")

    if check_only:
        print("%s  BOM=%s  CRLF=%d" % (target, has_bom, text.count("\r\n")))
        return 0 if has_bom else 1

    with open(target, "wb") as f:
        f.write(BOM)
        f.write(text.encode("utf-8"))

    out = open(target, "rb").read()
    print("wrote %s  (%d bytes, BOM=%s)" % (target, len(out), out[:3] == BOM))
    return 0


if __name__ == "__main__":
    sys.exit(main())
