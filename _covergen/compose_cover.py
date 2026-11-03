#!/usr/bin/env python3
"""把 Qwen-Image 2.1 產的圖合成為站上封面：
  - index_img（首頁卡片）：疊上標題字（1344×768）
  - banner_img（文章頁橫幅）：無文字（1920×768），中央／右側留白給主題的日期浮層

Fluid 主題的 banner 用 background-size:cover 裁切並在中央疊日期／字數，
所以 banner 一定不能有文字；首頁卡片才是可以放標題的地方。
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
COVERS = os.path.join(REPO, "source", "img", "covers")
SLUG = "flashmap-bf16-losslessness"

REG = "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc"
TEAL, FG, MUT = "#2dd4bf", "#e6edf3", "#c3ccd6"


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


def veil_left(img, top_alpha=170, fade_to=330):
    """上方壓一層漸層暗幕（文字在左上時用）。"""
    w, h = img.size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for y in range(fade_to):
        a = int(top_alpha * (1 - y / float(fade_to)) ** 1.6)
        d.line([(0, y), (w, y)], fill=(9, 12, 17, a))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def veil_right(img, start=0.40, alpha=205):
    """右側壓一層橫向漸層暗幕（文字在右上時用）——不動左邊的亮部。"""
    w, h = img.size
    x0 = int(w * start)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x in range(x0, w):
        t = (x - x0) / float(w - x0)
        d.line([(x, 0), (x, h)], fill=(9, 12, 17, int(alpha * t ** 0.8)))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def make_cover(src, dst, anchor="left"):
    img = Image.open(src).convert("RGB")
    if img.size != (1344, 768):
        img = img.resize((1344, 768), Image.LANCZOS)
    img = veil_right(img) if anchor == "right" else veil_left(img)
    d = ImageDraw.Draw(img)
    w, h = img.size
    al = "ra" if anchor == "right" else "la"      # PIL anchor: 水平 l/m/r + 垂直 a/t/m/s/b/d
    x = w - 84 if anchor == "right" else 84

    if anchor == "right":
        # 強調條貼右緣
        d.rounded_rectangle([w - 62, 62, w - 56, 146], radius=3, fill=TEAL)
    else:
        d.rounded_rectangle([56, 62, 62, 146], radius=3, fill=TEAL)

    d.text((x, 60), "FLASHMAP  ·  SPECULATIVE DECODING", font=font(REG, 21),
           fill=TEAL, anchor=al)
    d.text((x, 96), "無損，但驗不出來", font=font(BOLD, 72), fill=FG, anchor=al)
    d.text((x, 196), "8/12 不一致，其實是 bf16 的浮點並列；換成 fp32 就 12/12",
           font=font(REG, 27), fill=MUT, anchor=al)

    d.text((x, 726), "RTX 4090 · Qwen3-8B + FlashMap-Qwen3-8B · vLLM 0.31.0",
           font=font(REG, 19), fill="#8b949e", anchor=al)
    img.save(dst, "PNG", optimize=True)
    print("index_img  ->", dst, img.size, os.path.getsize(dst) // 1024, "KB", "(anchor=%s)" % anchor)



def make_banner(src, dst):
    """banner 不加任何文字（主題會在上面疊日期／字數）。"""
    img = Image.open(src).convert("RGB")
    if img.size[0] != 1920:
        img = img.resize((1920, int(img.size[1] * 1920 / img.size[0])), Image.LANCZOS)
    img.save(dst, "PNG", optimize=True)
    print("banner_img ->", dst, img.size, os.path.getsize(dst) // 1024, "KB")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--cover", default="cand_B.png")
    ap.add_argument("--wide", default="cand_Bwide.png")
    ap.add_argument("--anchor", default="right", choices=["left", "right"])
    a = ap.parse_args()
    make_cover(os.path.join(HERE, "out", a.cover),
               os.path.join(COVERS, SLUG + ".png"), anchor=a.anchor)
    make_banner(os.path.join(HERE, "out", a.wide),
                os.path.join(COVERS, SLUG + "-banner.png"))
    sys.exit(0)
