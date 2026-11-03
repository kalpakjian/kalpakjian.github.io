#!/usr/bin/env python3
"""用本地 ComfyUI + Qwen-Image 2.1 產「CNN」這篇的封面候選（無外部 API）。

沿用 gen_cover_qwen.py 的 graph（官方模板 image_qwen_image_2_1_t2i.json 攤平），
只換提示詞與尺寸。風格與章節內插圖統一：近黑底 + cyan/magenta 霓虹。

用法：
    ../ComfyUI/.venv/bin/python gen_cover_cnn.py            # 全部
    ../ComfyUI/.venv/bin/python gen_cover_cnn.py --only A   # 單一
"""
import argparse
import json
import os
import shutil
import sys
import time
import urllib.request

BASE = "http://127.0.0.1:8188"
COMFY = os.environ.get("COMFYUI_DIR", "/home/kalpakjian/Projects/ComfyUI")
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

STEPS = 30
CFG = 1.0
SAMPLER, SCHED = "euler", "simple"
UNET = "qwen_image_2.1_int8_convrot.safetensors"
CLIP = "qwen3vl_8b_int8_convrot.safetensors"
VAE = "qwen_image_2.1_vae_bf16.safetensors"

NOTEXT = (" Absolutely no text, no typography, no letters, no words, no numbers, "
          "no logos, no watermark, no signature, no captions, pure imagery only.")

NEON = (" Neon cyberpunk technical render, intense saturated cyan and magenta glow on "
        "a deep near-black background, thin electric-blue lattice lines, volumetric "
        "haze, bloom, high contrast, cinematic, ultra detailed.")

# 封面主體：3×3 卷積核掃過像素格，身後的 magenta 特徵圖層
COVER = ("A glowing cyan wireframe 3x3 filter grid hovering slightly above a dark "
         "plane of small square pixels, dragging a bright violet light trail across "
         "the grid, three translucent magenta feature-map sheets floating behind it "
         "and receding into darkness, each sheet a faint glowing grid of dots, "
         "concentric rings of light where the filter touches the pixels, "
         "macro depth of field, minimal composition, high detail.")

# 寬版：主體集中在左三分之一，右側留白給主題的日期／字數浮層
WIDEL = ("Panoramic composition: a glowing cyan wireframe 3x3 filter grid sweeping "
         "over a dark grid of square pixels, hugging the left third of the frame, "
         "violet light trail, three translucent magenta feature-map sheets receding "
         "toward the left edge, the centre and right two thirds fade into calm empty "
         "near-black space with a faint vignette, volumetric light.")

# 寬版另一版：層層堆疊的特徵圖像霓虹階梯
WIDER = ("Panoramic composition: a staircase of translucent glowing magenta "
         "feature-map planes receding into darkness on the right third of the frame, "
         "a cyan wireframe filter grid lighting the nearest plane, thin bright "
         "lattice lines connecting the planes, the left two thirds is calm empty "
         "near-black space with a faint vignette, volumetric light.")

PROMPTS = [
    ("A", 1344, 768, COVER + NEON + NOTEXT, 7071),
    ("B", 1344, 768, COVER.replace("cyan wireframe", "magenta wireframe")
                              .replace("magenta feature-map", "cyan feature-map") + NEON + NOTEXT, 7072),
    ("Awide", 1920, 760, WIDEL + NEON + NOTEXT, 7073),
    ("Bwide", 1920, 760, WIDER + NEON + NOTEXT, 7074),
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
              "inputs": {"images": ["8", 0], "filename_prefix": "qwen_cnn"}},
    }


def post(payload):
    req = urllib.request.Request(
        BASE + "/prompt",
        data=json.dumps({"prompt": payload, "client_id": "covergen-cnn"}).encode(),
        headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=120))


def wait(prompt_id, timeout=1800):
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
                raise SystemExit("execution error: %s" % json.dumps(st)[:1200])
    raise SystemExit("timeout waiting for %s" % prompt_id)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    args = ap.parse_args()

    os.makedirs(OUTDIR, exist_ok=True)
    todo = [p for p in PROMPTS if args.only is None or p[0] == args.only]
    for tag, w, h, prompt, seed in todo:
        print("[%s] %dx%d seed=%d submitting ..." % (tag, w, h, seed), flush=True)
        r = post(build_graph(prompt, seed, w, h))
        hist = wait(r["prompt_id"])
        for im in hist["outputs"]["9"]["images"]:
            src = os.path.join(COMFY, "output", im.get("subfolder", ""), im["filename"])
            dst = os.path.join(OUTDIR, "cnn_%s.png" % tag)
            shutil.copyfile(src, dst)
            print("[%s] -> %s (%d KB)" % (tag, dst, os.path.getsize(dst) // 1024), flush=True)
    print("done")


if __name__ == "__main__":
    sys.exit(main())
