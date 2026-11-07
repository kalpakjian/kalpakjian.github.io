# -*- coding: utf-8 -*-
"""Ad-hoc probe: quantity parsing edge cases (kept because shell quoting eats $)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figures as F  # noqa: E402

CASES = ["$1T", "1T", "594B", "81.7%", "$0.21", "96.32 tok/s", "2026-11-06",
         "$80B", "64k", "12T", "3 days", "$1.2M"]
for c in CASES:
    print("%-14r -> %r" % (c, F._qty(c)))
