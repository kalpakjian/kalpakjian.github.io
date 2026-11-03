#!/usr/bin/env python3
"""用本地 ComfyUI + Qwen-Image 2.1 產「逐頁核對報告」這篇的封面候選（無外部 API）。

沿用 gen_cover_cnn.py 的 graph（UNETLoader / CLIPLoader / VAELoader /
QwenImage21Cache / TextEncodeQwenImage21 / KSampler / VAEDecode / SaveImage），
只換提示詞與尺寸。風格與站上其他封面一致：近黑底 + cyan/magenta 霓虹。

概念：一疊發光的半透明「程式碼面板」，最下面那塊的底邊被一道光斜切掉
（＝簡報截圖被向下箭頭遮住），旁邊浮著一個 cyan 環（＝逐頁核對）。

用法：
    ../ComfyUI/.venv/bin/python gen_cover_report_qwen.py            # 全部
    ../ComfyUI/.venv/bin/python gen_cover_report_qwen.py --only A   # 單一
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

NEON = (" Neon cyberpunk technical render, saturated cyan and magenta glow against a "
        "deep near-black background, thin electric-blue lattice lines, volumetric haze, "
        "bloom, high contrast, cinematic, ultra detailed.")

# 主體：一疊半透明「程式碼面板」，最底一塊的底邊被光斜切（＝截圖被遮住）
COVER = ("A stack of thin translucent glass panels floating in deep darkness, each panel "
         "etched with faint glowing horizontal lines resembling blurred source code, "
         "the lowest panel's bottom edge sliced off by a thin bright cyan beam as if "
         "cropped mid-line, a small glowing cyan ring hovering above one panel like a "
         "magnifier, magenta volumetric light spilling from behind the stack, "
         "macro depth of field, minimal composition, high detail.")

# B：色相反轉，改成一道 magenta 掃描光切過面板
COVER_B = ("A stack of thin translucent glass panels floating in deep darkness, each panel "
           "etched with faint glowing horizontal lines resembling blurred source code, "
           "a single magenta scanning beam sweeping across the stack and cutting the bottom "
           "panel's edge, a small glowing magenta ring hovering above one panel, cyan "
           "volumetric light spilling from behind, macro depth of field, minimal "
           "composition, high detail.")

# 寬版：主體壓在左三分之一，中央與右側留黑給主題的日期／字數浮層
WIDE_L = ("Panoramic composition: a stack of thin translucent glass panels hugging the left "
          "third of the frame, each etched with faint glowing horizontal code-like lines, "
          "the lowest panel's edge sliced by a bright cyan beam, a small cyan ring hovering "
          "beside them, magenta rim light, the centre and right two thirds fade into calm "
          "empty near-black space with a faint vignette, volumetric light.")

WIDE_R = ("Panoramic composition: a stack of thin translucent glass panels hugging the left "
          "third of the frame, a magenta scanning beam cutting across the stack, faint "
          "glowing code-like lines on each panel, a small cyan loupe ring floating in front, "
          "thin bright lattice lines, the centre and right two thirds is empty near-black "
          "space with a soft vignette, volumetric light.")

PROMPTS = [
    ("A", 1344, 768, COVER + NEON + NOTEXT, 8081),
    ("B", 1344, 768, COVER_B + NEON + NOTEXT, 8082),
    ("Awide", 1920, 768, WIDE_L + NEON + NOTEXT, 8083),
    ("Bwide", 1920, 768, WIDE_R + NEON + NOTEXT, 8084),
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
              "inputs": {"images": ["8", 0], "filename_prefix": "qwen_report"}},
    }


def post(payload):
    req = urllib.request.Request(
        BASE + "/prompt",
        data=json.dumps({"prompt": payload, "client_id": "covergen-report"}).encode(),
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
                raise SystemExit("execution error: %s" % json.dumps(st)[:1500])
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
            dst = os.path.join(OUTDIR, "report_%s.png" % tag)
            shutil.copyfile(src, dst)
            print("[%s] -> %s (%d KB)" % (tag, dst, os.path.getsize(dst) // 1024), flush=True)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
