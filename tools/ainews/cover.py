# -*- coding: utf-8 -*-
"""Stage 4b: generate the cover with Qwen-Image, pick a seed, install it.

WHY THIS IS A SEPARATE STEP WITH A HUMAN GATE
---------------------------------------------
The figures are deterministic: same data -> same SVG. The cover is not. A text2img
model can produce a beautiful image with the wrong metaphor, two extra fingers, or
a fake watermark, and no lint can tell.

So this script does the repeatable part -- build the prompt from the brief, render
N seeds, save candidates, run cheap automated checks (size, dimensions) -- and
stops. Installing a candidate into source/img/covers/ is a deliberate second step.

    python tools/ainews/cover.py --brief out/<id>/brief.json --slug ainews-x-zh
    python tools/ainews/cover.py --slug ainews-x-zh --pick 2

ComfyUI is optional: with --no-render it only writes the prompt, so the prompt can
be reviewed (or pasted into the ComfyUI UI) when the server is down.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
COVER_DIR = os.path.join(ROOT, "source", "img", "covers")
COVERGEN = os.path.join(ROOT, "_covergen")

BASE = ("Dark cinematic tech cover art, deep navy to teal gradient background, "
        "subtle grid texture, soft volumetric glow, glowing bokeh particles, "
        "professional engineering aesthetic, depth of field, no text, no words, "
        "no letters, no watermark, 16:9 composition, highly detailed")

# A motif is chosen from the headline's SHAPE, not its words: text2img models do
# not render product names, they render scenes. This mapping is the one genuinely
# creative choice in the pipeline, so it is an explicit table a human can edit.
MOTIFS = {
    "money": ("A colossal translucent column of white-cyan light rising from a dark "
              "reflective floor, made of thousands of thin stacked glass plates; a heavy "
              "band of storm cloud presses down on its upper third and the plates crack "
              "and shear sideways, shedding glowing fragments; rows of tiny distant "
              "figures look up from the floor; a single broken brass measuring scale lies "
              "abandoned in the foreground"),
    "weights": ("A vast three-dimensional lattice of thousands of tiny glowing nodes and "
                "thin luminous wires in deep perspective; a hand of flowing light reaches "
                "in and three fingertips touch individual nodes, each contact flaring into "
                "a cyan spark that ripples outward; one tangled knot of amber filaments "
                "unwinds into a single straight calm cyan line"),
    "model_release": ("A dense constellation of thousands of small glowing nodes "
                      "compressing into a single brilliant core of white-cyan light, "
                      "surrounded by concentric rings of fading amber embers, floating "
                      "above a dark mirror floor with a faint reflection"),
    "agent": ("A single luminous thread of light splitting into dozens of parallel "
              "strands, each threading through its own glowing hexagonal gate, then "
              "reconverging into one bright cable that runs into the distance; a few "
              "strands fray and dim at the edges"),
    "benchmark": ("A steep staircase of glowing translucent slabs ascending into darkness, "
                  "each step edge lit in cyan, small blocky forms resting on every step and "
                  "a faint amber haze filling the lowest steps"),
    "hardware": ("An open frame of densely packed glowing silicon dies in deep perspective, "
                 "linked by thick luminous teal conduits carrying bright pulses of light, "
                 "heat shimmer and fine copper traces visible between them"),
    "security": ("A tall translucent shield of layered hexagons standing in dark space, "
                 "its surface partly cracked with thin red fissures, thin cyan lines "
                 "probing it from several directions, sparks falling where they touch"),
    "default": ("A bright geometric structure of interconnected translucent panels rising "
                "from a dark reflective plane, thin cyan light running along every edge, "
                "faint particles drifting upward, deep navy haze behind"),
}


def pick_motif(brief):
    """Choose a scene from keywords in the subject + top candidates.

    Order matters and was tuned against real issues: "open-weight model release"
    contains the word `weights`, so the generic `weights` rule used to steal the
    Inkling story from `model_release`. Release/launch phrasing is checked first,
    and the interpretability rule now needs a narrower vocabulary.
    """
    text = " ".join([brief.get("subject") or ""] +
                    [c.get("summary") or "" for c in
                     (brief.get("headline_candidates") or [])[:3]]).lower()
    rules = [
        ("money", ("ipo", "valuation", "run rate", "raise", "funding", "revenue")),
        ("security", ("cyber", "jailbreak", "exploit", "attack", "vulnerab", "breach")),
        # a release of weights is a RELEASE; interpretability is not
        ("model_release", ("open-weight", "open weight", "apache 2.0", "released",
                           "release", "launch", "launched", "announc", "shipped")),
        ("weights", ("weight space", "interpretab", "steering", "ablation",
                     "gradient", "mechanistic", "natively read", "read & write")),
        ("benchmark", ("benchmark", "leaderboard", "scored", "score", "eval")),
        ("agent", ("agent", "harness", "swarm", "orchestrat", "subagent")),
        ("hardware", ("gpu", "npu", "tpu", "bandwidth", "tok/s", "inference")),
    ]
    for name, keys in rules:
        if any(k in text for k in keys):
            return name
    return "default"


def build_prompt(brief):
    motif = pick_motif(brief)
    return BASE + ". Central subject: " + MOTIFS[motif] + ".", motif



def check_candidate(path):
    """Cheap automated checks. Anything they cannot judge stays a human call."""
    issues = []
    size = os.path.getsize(path) if os.path.exists(path) else 0
    if size < 10000:
        issues.append("檔案太小（%d bytes）" % size)
    try:
        from PIL import Image
        im = Image.open(path)
        if im.size != (1344, 768):
            issues.append("尺寸 %s != 1344x768" % (im.size,))
    except Exception as e:                            # noqa: BLE001
        issues.append("無法讀取圖片：%s" % e)
    return issues


def render(brief, slug, seeds, out_dir):
    """Render candidates with the existing Qwen client (_covergen/qwen_cover.py)."""
    if COVERGEN not in sys.path:
        sys.path.insert(0, COVERGEN)
    import urllib.parse
    import urllib.request
    import qwen_cover as q  # noqa: E402

    prompt, motif = build_prompt(brief)
    os.makedirs(out_dir, exist_ok=True)
    made = []
    for seed in seeds:
        path = os.path.join(out_dir, "%s_seed%d.png" % (slug, seed))
        if os.path.exists(path) and os.path.getsize(path) > 10000:
            print("SKIP seed %d (exists)" % seed)
            made.append(path)
            continue
        print("GEN  seed %d (motif=%s)" % (seed, motif))
        imgs = q.generate(prompt, "cover_%s_seed%d" % (slug, seed), seed=seed)
        if not imgs:
            print("FAIL seed %d: ComfyUI returned no image" % seed)
            continue
        meta = imgs[0]
        qs = urllib.parse.urlencode({"filename": meta["filename"],
                                     "subfolder": meta.get("subfolder", ""),
                                     "type": meta.get("type", "output")})
        with urllib.request.urlopen("%s/view?%s" % (q.SERVER, qs)) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
        made.append(path)
    return made, prompt, motif


def install(slug, pick, out_dir):
    src = os.path.join(out_dir, "%s_seed%s.png" % (slug, pick))
    if not os.path.exists(src):
        cands = sorted(f for f in os.listdir(out_dir) if f.endswith(".png")) \
            if os.path.isdir(out_dir) else []
        if pick.isdigit() and 1 <= int(pick) <= len(cands):
            src = os.path.join(out_dir, cands[int(pick) - 1])
        else:
            print("ERROR: no candidate matched %r in %s" % (pick, out_dir), file=sys.stderr)
            return 1
    os.makedirs(COVER_DIR, exist_ok=True)
    dst = os.path.join(COVER_DIR, "%s.png" % slug)
    shutil.copyfile(src, dst)
    print("installed: %s" % dst)
    print("  -> frontmatter:\n     index_img: /img/covers/%s.png\n"
          "     banner_img: /img/covers/%s.png" % (slug, slug))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Render/pick an AINews cover with Qwen-Image.")
    ap.add_argument("--brief", help="brief.json (needed to render, not to --pick)")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--seeds", default="7401,7402,7403")
    ap.add_argument("--pick", help="seed number or 1-based index to install")
    ap.add_argument("--no-render", action="store_true", help="only write the prompt")
    args = ap.parse_args(argv)

    out_dir = os.path.join(HERE, "out", args.slug, "cover")
    if args.pick:
        return install(args.slug, args.pick, out_dir)

    if not args.brief:
        ap.error("--brief is required unless --pick is given")
    with open(args.brief, "r", encoding="utf-8-sig") as f:
        brief = json.load(f)

    prompt, motif = build_prompt(brief)
    os.makedirs(out_dir, exist_ok=True)
    pp = os.path.join(out_dir, "prompt.txt")
    with open(pp, "w", encoding="utf-8", newline="\n") as f:
        f.write("motif: %s\n\n%s\n" % (motif, prompt))
    print("prompt -> %s  (motif=%s)" % (pp, motif))

    if args.no_render:
        print("(--no-render: nothing rendered)")
        return 0

    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    made, _, _ = render(brief, args.slug, seeds, out_dir)
    for p in made:
        issues = check_candidate(p)
        print("  %s  %s" % (os.path.basename(p), "OK" if not issues else "; ".join(issues)))
    print("\n接著挑一張：python tools/ainews/cover.py --slug %s --pick <seed或序號>" % args.slug)
    return 0


if __name__ == "__main__":
    sys.exit(main())

