"""Generate the CNN 2 cover with the local Qwen-Image workflow.

    python gen_cover.py "prompt text"

Reuses the API graph exported by ui_to_api.py (qwen_api.json), overrides the
prompt / size, submits to ComfyUI, waits, and writes
source/img/covers/cnn2-notes.png at 1344x768 (same size as the other covers).
"""
import json
import time
import urllib.request
import uuid

BASE = "http://127.0.0.1:8188"
API = r"C:\Users\princ\qwen_api.json"
OUT = r"C:\Users\princ\kalpakjian.github.io\source\img\covers\cnn2-notes.png"
W, H = 1344, 768

NEG = ("text, words, letters, watermark, signature, logo, ui, frame, border, "
       "lowres, blurry, jpeg artifacts, deformed")

PROMPT = (
    "dark navy tech illustration, glowing teal and amber accents, abstract 3D "
    "visualisation of convolutional filters sliding across a glowing grid of "
    "feature maps, stacked layers receding into depth, thin luminous lines "
    "connecting low-level edges to high-level shapes, volumetric haze, "
    "cinematic lighting, ultra clean composition, wide banner, no text"
)


def post(path, payload):
    req = urllib.request.Request(BASE + path, json.dumps(payload).encode(),
                                 {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def normalise(api):
    """Repair the two artefacts of UI->API conversion for KSampler."""
    for node in api.values():
        if node["class_type"] != "KSampler":
            continue
        i = node["inputs"]
        i["sampler_name"] = "euler"
        i["scheduler"] = "simple"
        i["denoise"] = 1.0
        if not isinstance(i.get("steps"), int):
            i["steps"] = 20
        if not isinstance(i.get("cfg"), (int, float)):
            i["cfg"] = 2.5
        if not isinstance(i.get("seed"), int):
            i["seed"] = 7303
    return api


def main():
    api = json.load(open(API, encoding="utf-8"))
    api = normalise(api)
    texts = [k for k, v in api.items() if v["class_type"] == "CLIPTextEncode"]
    for node in api.values():
        if node["class_type"] == "KSampler":
            node["inputs"].setdefault("positive", [texts[0], 0])
            node["inputs"].setdefault("negative", [texts[-1], 0])
    sizes = [k for k, v in api.items()
             if v["class_type"].startswith(("EmptySD3LatentImage", "EmptyLatentImage"))]
    print("text nodes:", texts, "| size nodes:", sizes)
    api[texts[0]]["inputs"]["text"] = PROMPT
    for k in texts[1:]:
        api[k]["inputs"]["text"] = NEG
    for k in sizes:
        api[k]["inputs"].update({"width": W, "height": H, "batch_size": 1})

    res = post("/prompt", {"prompt": api, "client_id": uuid.uuid4().hex})
    pid = res["prompt_id"]
    print("queued", pid)

    for _ in range (120):
        time.sleep(3)
        try:
            hist = json.load(urllib.request.urlopen(f"{BASE}/history/{pid}", timeout=20))
        except Exception:
            continue
        if pid in hist:
            outs = hist[pid]["outputs"]
            for node in outs.values():
                for img in node.get("images", []):
                    url = (f"{BASE}/view?filename={urllib.parse.quote(img['filename'])}"
                           f"&subfolder={img.get('subfolder','')}&type={img.get('type','output')}")
                    data = urllib.request.urlopen(url, timeout=60).read()
                    open(OUT, "wb").write(data)
                    print("saved", OUT, len(data), "bytes")
                    return
            print("finished but no image in outputs:", outs)
            return
    print("timeout waiting for the image")


if __name__ == "__main__":
    import urllib.parse  # noqa: E402
    main()
