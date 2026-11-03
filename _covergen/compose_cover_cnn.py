#!/usr/bin/env python3
"""把 cnn_B.png / cnn_Awide.png 合成為 CNN 這一篇的 index_img 與 banner_img。

沿用 compose_cover.py 的版式：
  index_img 1344×768，左上角壓漸層暗幕 + 標題字
  banner_img 1920×寬，完全不壓字（Fluid 主題會在上面疊日期／字數）
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
COVERS = os.path.join(REPO, "source", "img", "covers")
SLUG = "cnn-1-convnet-neon"

REG = "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc"
CYAN, FG, MUT = "#22d3ee", "#e6edf3", "#c3ccd6"


def pick_face(path, want="TC"):
    for i in range(8):
        try:
            f = ImageFont.truetype(path, 20, index=i)
        except OSError:
            break
        if want in f.getname()[0]:
            return i
    return 0


def font(path, size):
    return ImageFont.truetype(path, size, index=pick_face(path))


def veil_left(img, top_alpha=200, fade_to=430):
    w, h = img.size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for y in range(fade_to):
        a = int(top_alpha * (1 - y / float(fade_to)) ** 1.5)
        d.line([(0, y), (w, y)], fill=(6, 9, 14, a))
    # 左側再壓一層，讓文字區更乾淨
    for x in range(int(w * 0.55)):
        t = x / (w * 0.55)
        d.line([(x, 0), (x, h)], fill=(6, 9, 14, int(120 * (1 - t) ** 1.2)))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def make_cover(src, dst):
    img = Image.open(src).convert("RGB")
    if img.size != (1344, 768):
        img = img.resize((1344, 768), Image.LANCZOS)
    img = veil_left(img)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([56, 62, 62, 150], radius=3, fill=CYAN)
    d.text((84, 60), "IVDC · CNN I  ·  卷積神經網絡", font=font(REG, 21), fill=CYAN)
    d.text((84, 96), "濾波器就是眼睛", font=font(BOLD, 74), fill=FG)
    d.text((86, 196), "從視覺皮層到 LeNet-5：61,750 個參數是怎麼算出來的", font=font(REG, 26), fill=MUT)
    d.text((84, 726), "36 頁課程簡報 · 9 張手繪 SVG · 封面 Qwen-Image 2.1", font=font(REG, 19), fill="#8b949e")
    img.save(dst, "PNG", optimize=True)
    print("index_img  ->", dst, img.size, os.path.getsize(dst) // 1024, "KB")


def make_banner(src, dst):
    img = Image.open(src).convert("RGB")
    if img.size[0] != 1920:
        img = img.resize((1920, int(img.size[1] * 1920 / img.size[0])), Image.LANCZOS)
    img.save(dst, "PNG", optimize=True)
    print("banner_img ->", dst, img.size, os.path.getsize(dst) // 1024, "KB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cover", default="cnn_B.png")
    ap.add_argument("--wide", default="cnn_Awide.png")
    a = ap.parse_args()
    os.makedirs(COVERS, exist_ok=True)
    make_cover(os.path.join(HERE, "out", a.cover), os.path.join(COVERS, SLUG + ".png"))
    make_banner(os.path.join(HERE, "out", a.wide), os.path.join(COVERS, SLUG + "-banner.png"))
