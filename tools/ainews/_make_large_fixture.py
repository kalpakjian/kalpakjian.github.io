# -*- coding: utf-8 -*-
"""Build a REAL-SHAPED large fixture (deterministic, no network).

Why synthetic-large rather than shipped-real:
  The genuine issue is ~216 KB and lives in Gmail; shipping it into the repo
  would duplicate every issue and still only prove one sample. Instead this
  script reproduces the exact *structure* beehiiv emits -- sponsor block,
  lede, View image/Caption pairs, masthead, rule separators, "# AI Twitter
  Recap" with empty H2 crumbs, "# AI Reddit Recap" with "## /r/..." groups,
  the full footer -- and repeats the recap payload until the body is ~200 KB.

  That is what the extractor's scale properties actually depend on: the number
  of separators, the number of empty-H2 crumbs, and the noise patterns. A
  hand-written 900-byte fixture cannot exercise those.

The real-issue fragments below are copied verbatim from issue
1a1b06e0f230a991 (Inkling 2 Small) so marker strings ("NODES 2026",
"brought to you by", "View image:", the footer) are the production ones.

Usage:
    python tools/ainews/_make_large_fixture.py            # -> fixtures/large-issue.json
    python tools/ainews/_make_large_fixture.py --target-kb 400
"""
import argparse
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SEP = "\u2014" * 27

SPONSOR = (
    "\u201cBuild AI systems with context graphs and agentic memory. **Join Andrew Ng and "
    "AI engineers at NODES 2026 for 100+ live technical sessions**. Free, online, 24 hours. "
    "[Save your spot](https://neo4j.com/nodes/)!\u201c \u2014 \r\n\r\n\r\n\r\n"
)
LEDE = (
    "There was a time in the early days of Thinking Machines when their going concern as "
    "a neolab was very much in doubt. Those days are clearly behind us.\r\n\r\n"
    "Anyway, here\u2019s [Inkling 2 Small](https://thinkingmachines.ai/news/inkling-2-small/) "
    "- pretrained from scratch in less than 3 days on <12T tokens native NVFP4.\r\n\r\n"
    "View image: (https://media.beehiiv.com/cdn-cgi/image/fit=scale-down/uploads/a/image.png?t=1)\r\n"
    "Caption: \r\n\r\n"
    "People are calling it \u201cthe smartest western open weight model by a margin\u201d.\r\n\r\n"
)
MASTHEAD = (
    "\u201cAI News for 11/04/2026-11/05/2026 is brought to you by our friends at Neo4J\u201c \u2014 \r\n\r\n"
    + SEP + "\r\n\r\n"
)
FOOTER = (
    SEP + "\r\n\r\n"
    "You are reading a plain text version of this post. For the best experience, copy and "
    "paste this link in your browser to view the post online:\r\n\r\n"
    "https://lspace.beehiiv.com/p/ainews-inkling-2-small\r\n"
)

TWITTER_ITEM = (
    "* **Launch:** Announced at 31 on the Artificial Analysis Intelligence Index, "
    "\u201ca big jump over its predecessor.\u201d Available for fine-tuning and inference on "
    "Tinker ([@kimmonismus](https://x.com/kimmonismus/status/2118652677689126965)).\r\n\r\n"
    "  * **Architecture**: 594B total, 17B active, accepts image inputs and supports "
    "variable effort ([@kimmonismus](https://x.com/k/1)).\r\n\r\n"
)
REDDIT_ITEM = (
    "* [**QWEN 3.8 FN - 8bit FP quant - 96.32 tokens/s**](https://www.reddit.com/r/LocalLLM/x/) "
    "(Activity: 1258): Reaching **`96.32 tok/s`** on coding workloads with **`3`** draft tokens, "
    "at **`8-bit FP`** quantization and ~**`95k`** context.\r\n\r\n"
)
SUBS = [
    ("/r/LocalLlama + /r/localLLM Recap", "local"),
    ("Less Technical AI Subreddit Recap", "less_technical"),
]


def build(target_kb=200):
    parts = [SPONSOR, LEDE, MASTHEAD]
    parts.append("# AI Twitter Recap\r\n\r\n## \r\n**What happened**\r\n\r\n"
                 "**Thinking Machines released Inkling 2 Small, a 594B-total / 17B-active "
                 "multimodal MoE.**\r\n\r\n")
    i = 0
    while sum(len(p) for p in parts) < target_kb * 1024 * 0.45:
        parts.append(TWITTER_ITEM.replace("Launch", "Launch %d" % i))
        i += 1
    parts.append(SEP + "\r\n\r\n# AI Reddit Recap\r\n\r\n")
    for title, _key in SUBS:
        parts.append("## %s\r\n\r\n" % title)
        j = 0
        while j < 25:
            parts.append("### %d. Post %d\r\n\r\n%s" % (j + 1, j + 1, REDDIT_ITEM))
            j += 1
        parts.append(SEP + "\r\n\r\n")
    parts.append(FOOTER)
    body = "".join(parts)
    return {
        "_comment": "Synthetic but production-shaped AINews body (~%d KB). Structure and "
                    "noise patterns are copied from issue 1a1b06e0f230a991 so the extractor's "
                    "scale behaviour can be tested without shipping a real issue." % target_kb,
        "data": {
            "messageId": "large00000000001",
            "threadId": "large00000000001",
            "subject": "[AINews] Large fixture: structure stress",
            "sender": "Latent Space <lspace@mail.beehiiv.com>",
            "messageTimestamp": "2026-11-06T10:36:03Z",
            "display_url": "https://mail.google.com/mail/u/0/#inbox/large00000000001",
            "messageText": body,
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target-kb", type=int, default=200)
    args = ap.parse_args()
    data = build(args.target_kb)
    out = os.path.join(HERE, "fixtures", "large-issue.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %s  body=%d chars  separators=%d  crumbs=%d"
          % (out, len(data["data"]["messageText"]),
             data["data"]["messageText"].count(SEP),
             data["data"]["messageText"].count("## \r\n")))


if __name__ == "__main__":
    main()
