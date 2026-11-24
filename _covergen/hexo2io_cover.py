"""hexo-and-python-io 封面候選：本機 Qwen-Image 2.1，3 個種子。

    python hexo2io_cover.py

沿用 batch_rai_series.py 的 BASE（house style）與 tools/comfyui/gen_cover.py
的 class_type 查找法。輸出到 _covergen/candidates/hexo2io/（由 .gitignore 排除）。
"""
import json
import os
import time
import urllib.parse
import urllib.request
import uuid

BASE_URL = "http://127.0.0.1:8188"
WORKFLOW = r"D:\AI\ComfyUI\workflows\image\qwen_image_2_1_text2img_api.json"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "candidates", "hexo2io")
W, H = 1344, 768
SEEDS = [7301, 7302, 7303]

BASE = ("Dark cinematic tech illustration, deep navy to teal gradient background, "
        "subtle grid texture, soft volumetric glow, glowing bokeh particles, "
        "thin luminous cyan wireframe accents, professional engineering aesthetic, "
        "shallow depth of field, generous negative space, no text, no words, "
        "no letters, no numbers, no watermark, no logo, 16:9 composition, "
        "highly detailed, clean composition with one clear focal subject")

# 一個名字、三種指涉：同一發光節點分出三條岔開的光路。
MOTIF = ("one bright glowing hub node dividing into three divergent luminous "
         "pathways: one rising into a floating hexagonal lattice structure, "
         "one unspooling into a smooth ribbon of flowing light streams, "
         "one arcing away toward a distant grid of translucent page-like tiles")


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
            i["filename_prefix"] = f"hexo2io_{seed}"
    return api


def run(prompt, seed):
    out = os.path.join(OUT_DIR, f"hexo2io_{seed}.png")
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
