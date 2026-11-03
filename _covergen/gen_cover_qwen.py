#!/usr/bin/env python3
"""用 ComfyUI 的 API 以 Qwen-Image 2.1 產部落格封面候選（無文字氛圍圖）。

為什麼不用 GUI：這台是無頭操作，而且候選圖要可重現（固定 seed + 固定 graph）。

Graph 來源：ComfyUI 內建的官方模板
  .venv/lib/python3.12/site-packages/comfyui_workflow_templates_json/templates/
      image_qwen_image_2_1_t2i.json
它是 subgraph 包裝的，這裡把它攤平成 /prompt 需要的 API 格式：
  UNETLoader → QwenImage21Cache → KSampler
  CLIPLoader(qwen_image) → TextEncodeQwenImage21（同時輸出 positive / negative）
  EmptyLatentImage → KSampler，KSampler → VAEDecode → SaveImage
官方參數（模板註解）：cfg 固定 1、steps 約 25–40、sampler euler、scheduler simple；
cfg=1 時 negative_prompt 不生效，所以「不要文字」必須寫在正向提示裡。

用法：
    python gen_cover_qwen.py            # 產全部候選
    python gen_cover_qwen.py --only A   # 只產某一個
"""
import argparse
import json
import os
import random
import shutil
import sys
import time
import urllib.request

BASE = "http://127.0.0.1:8188"
COMFY = os.environ.get("COMFYUI_DIR", "/home/kalpakjian/Projects/ComfyUI")
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

W, H = 1344, 768          # 與站上既有封面同尺寸
STEPS = 25
CFG = 1.0                 # 官方路徑固定 1（negative 不生效）
SAMPLER, SCHED = "euler", "simple"
UNET = "qwen_image_2.1_int8_convrot.safetensors"
CLIP = "qwen3vl_8b_int8_convrot.safetensors"
VAE = "qwen_image_2.1_vae_bf16.safetensors"

NOTEXT = (" Absolutely no text, no typography, no letters, no words, no numbers, "
          "no logos, no watermark, no signature, no captions, pure imagery only.")

PROMPTS = [
    ("A", W, H, "Abstract dark technical illustration: two softly glowing points almost "
          "overlapping on a single thin horizontal rule, one cyan and one magenta, "
          "a faint halo where they touch, deep near-black background with a very "
          "subtle dark grid, cinematic macro depth of field, minimal, elegant, "
          "high detail." + NOTEXT, 111),
    ("B", W, H, "Conceptual visualization of floating point quantization: a staircase of "
          "soft glowing steps descending into darkness, cyan isometric lattice "
          "fading into mist on the left, one step dissolving where two values "
          "merge, deep navy-black background, volumetric light, minimal tech "
          "aesthetic, refined, high detail." + NOTEXT, 222),
    ("C", W, H, "Two nearly identical luminous beads resting on a dark measuring rule, one "
          "cyan one magenta, separated by a hairline gap that catches the light, "
          "macro photography style, very shallow depth of field, soft bokeh, "
          "near-black background, minimal and calm, high detail." + NOTEXT, 333),
    ("D", W, H, "Abstract grid of tiny dark tiles receding into fog, exactly two adjacent "
          "tiles briefly lit cyan and magenta at the boundary where they meet, "
          "cinematic rim light, deep black background, minimal, precise, high "
          "detail." + NOTEXT, 444),
    # 寬版 banner（B）：等腰梯階壓在左半，右半留給主題的日期／字數浮層
    ("Bwide", 1920, 760,
     "Wide panoramic abstract render: a glowing saturated cyan isometric staircase "
     "of translucent blocks descending from the upper left, concentrated in the left "
     "half of the frame, thin bright lattice lines, the right half of the frame fades "
     "into deep calm near-black space with a faint vignette, volumetric light, "
     "minimal, precise, high detail." + NOTEXT, 445),

    # 寬版 banner：主體壓在左三分之一，中央與右側留給主題的日期／字數浮層
    ("Cwide", 1920, 760,
     "Wide panoramic macro photograph on a black background: one small bead glows "
     "bright saturated cyan, the other bead glows bright saturated magenta, both "
     "resting on a dark measuring rule and grouped tightly in the left third of the "
     "frame, a thin hairline of light between them, the right two thirds of the "
     "frame is empty calm near-black space with a faint vignette, strong coloured "
     "glow reflecting on the metal rule, shallow depth of field, cinematic, minimal, "
     "high detail." + NOTEXT, 335),
]


def build_graph(prompt, seed, w, h):
    return {
        "1": {"class_type": "UNETLoader",
              "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader",
              "inputs": {"clip_name": CLIP, "type": "qwen_image"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "4": {"class_type": "QwenImage21Cache",
              "inputs": {"model": ["1", 0], "device": "auto", "dtype": "default"}},
        "5": {"class_type": "TextEncodeQwenImage21",
              "inputs": {"clip": ["2", 0], "prompt": prompt,
                         "negative_prompt": "", "resolution": 1024}},
        "6": {"class_type": "EmptyLatentImage",
              "inputs": {"width": w, "height": h, "batch_size": 1}},
        "7": {"class_type": "KSampler",
              "inputs": {"model": ["4", 0], "seed": seed, "steps": STEPS, "cfg": CFG,
                         "sampler_name": SAMPLER, "scheduler": SCHED,
                         "positive": ["5", 0], "negative": ["5", 1],
                         "latent_image": ["6", 0], "denoise": 1.0}},
        "8": {"class_type": "VAEDecode",
              "inputs": {"samples": ["7", 0], "vae": ["3", 0]}},
        "9": {"class_type": "SaveImage",
              "inputs": {"images": ["8", 0], "filename_prefix": "qwen_cover"}},
    }


def post(payload):
    req = urllib.request.Request(
        BASE + "/prompt",
        data=json.dumps({"prompt": payload, "client_id": "covergen"}).encode(),
        headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=120))


def wait(prompt_id, timeout=900):
    t0 = time.time()
    while time.time() - t0 < timeout:
        time.sleep(2)
        try:
            h = json.load(urllib.request.urlopen(BASE + "/history/" + prompt_id, timeout=60))
        except Exception:
            continue
        if prompt_id in h:
            st = h[prompt_id].get("status", {})
            if st.get("completed"):
                return h[prompt_id]
            if st.get("status_str") == "error":
                raise SystemExit("execution error: %s" % json.dumps(st)[:800])
    raise SystemExit("timeout waiting for %s" % prompt_id)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="只產某一組（A/B/C/D）")
    args = ap.parse_args()

    os.makedirs(OUTDIR, exist_ok=True)
    todo = [p for p in PROMPTS if args.only is None or p[0] == args.only]
    for tag, w, h, prompt, seed in todo:
        print("[%s] %dx%d seed=%d submitting ..." % (tag, w, h, seed), flush=True)
        r = post(build_graph(prompt, seed, w, h))
        pid = r["prompt_id"]
        hist = wait(pid)
        imgs = hist["outputs"]["9"]["images"]
        for im in imgs:
            src = os.path.join(COMFY, "output", im.get("subfolder", ""), im["filename"])
            dst = os.path.join(OUTDIR, "cand_%s.png" % tag)
            shutil.copyfile(src, dst)
            print("[%s] -> %s (%d bytes)" % (tag, dst, os.path.getsize(dst)), flush=True)
    print("done")


if __name__ == "__main__":
    sys.exit(main())
