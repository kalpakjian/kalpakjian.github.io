"""〈Qwen-Image 封面產線〉一文的封面：3 個種子，候選挑一張。

    python cover_qwen_pipeline.py

BASE 沿用 batch_rai_series.py 的 house style；輸出到 candidates/（gitignore）。
選中的那張才複製到 source/img/covers/qwen-image-hexo-cover-pipeline.png。
"""
import json
import os
import time
import urllib.parse
import urllib.request
import uuid

BASE_URL = "http://127.0.0.1:8188"
WORKFLOW = r"D:\AI\ComfyUI\workflows\image\qwen_image_2_1_text2img_api.json"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "candidates", "qwen_pipeline")
W, H = 1344, 768
SEEDS = [7304, 7305, 7306]

BASE = ("Dark cinematic tech illustration, deep navy to teal gradient background, "
        "subtle grid texture, soft volumetric glow, glowing bokeh particles, "
        "thin luminous cyan wireframe accents, professional engineering aesthetic, "
        "shallow depth of field, generous negative space, no text, no words, "
        "no letters, no numbers, no watermark, no logo, 16:9 composition, "
        "highly detailed, clean composition with one clear focal subject")

# 文字 → 透鏡 → 一張圖：產線的語意。
MOTIF = ("a luminous horizontal production line: translucent stacked panels of "
         "flowing lines dissolving into light on the left, passing through a "
         "single glowing lens ring at the centre, and re-emerging on the right "
         "as one framed landscape image, with three faint parallel streams "
         "converging into that single frame")


def post(path, payload):
    req = urllib.request.Request(BASE_URL + path, json.dumps(payload).encode(),
                                 {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def build(prompt, seed):
    api = json.load(open(WORKFLOW, encoding="utf-8-sig"))
    for node in api.values():
        cls, i = node["class_type"], node["inputs"]
        if cls == "CLIPTextEncode":
            i["text"] = prompt
        elif cls == "KSampler":
            i["seed"] = seed
            i["steps"] = 25
            i["cfg"] = 2.5
        elif cls == "EmptyLatentImage":
            i.update({"width": W, "height": H, "batch_size": 1})
        elif cls == "SaveImage":
            i["filename_prefix"] = f"qwenpipeline_{seed}"
    return api


def run(prompt, seed):
    out = os.path.join(OUT_DIR, f"qwenpipeline_{seed}.png")
    if os.path.exists(out) and os.path.getsize(out) > 10_000:
        print(f"SKIP {seed} (exists)")
        return
    pid = post("/prompt", {"prompt": build(prompt, seed), "client_id": uuid.uuid4().hex})["prompt_id"]
    for _ in range(90):
        time.sleep(2)
        try:
            hist = json.load(urllib.request.urlopen(f"{BASE_URL}/history/{pid}", timeout=20))
        except Exception:
            continue
        if pid not in hist:
            continue
        for node in hist[pid]["outputs"].values():
            for img in node.get("images", []):
                url = (f"{BASE_URL}/view?filename={urllib.parse.quote(img['filename'])}"
                       f"&subfolder={img.get('subfolder', '')}&type={img.get('type', 'output')}")
                data = urllib.request.urlopen(url, timeout=60).read()
                open(out, "wb").write(data)
                print(f"saved {out} {len(data)} bytes")
                return
        print(f"no image for seed {seed}: {hist[pid]['outputs']}")
        return
    print(f"timeout seed {seed}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    prompt = f"{BASE}. Central subject: {MOTIF}."
    print(f"prompt chars: {len(prompt)}")
    for s in SEEDS:
        run(prompt, s)


if __name__ == "__main__":
    main()
