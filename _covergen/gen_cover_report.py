"""產生 ivdc-det-report 的封面。

- 預設：程序化背景（近黑＋cyan/magenta 光暈＋格線）
- 加 --bg：改用 Qwen-Image 產的圖當底，左側壓一層暗色漸層讓字讀得出來
  （Qwen 圖由 gen_cover_report_qwen.py 產生在 _covergen/out/report_*.png）

- index_img 1344×768：首頁卡片，可放標題
- banner_img 1920×768：文章頁橫幅，**不能有文字**（主題會在中央疊日期／字數）

用法：
    /tmp/venv-cpu/bin/python _covergen/gen_cover_report.py
    /tmp/venv-cpu/bin/python _covergen/gen_cover_report.py --bg _covergen/out/report_A.png
"""
import argparse
import math
import os

from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
COVERS = os.path.join(REPO, "source", "img", "covers")
REG = "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc"

BG = (10, 14, 20)
CYAN = (45, 212, 191)
MAG = (232, 62, 140)
FG = (230, 237, 243)
MUT = (168, 182, 196)


def font(path, size, want="TC"):
    for i in range(8):
        try:
            f = ImageFont.truetype(path, size, index=i)
        except OSError:
            break
        if want in f.getname()[0]:
            return f
    return ImageFont.truetype(path, size)


def backdrop(w, h):
    """近黑底 + 細格線 + 兩團光暈（cyan 左下、magenta 右上）。"""
    img = Image.new("RGB", (w, h), BG)
    px = img.load()
    for y in range(h):
        for x in range(0, w, 2):  # 每 2 px 取樣即可，速度考量
            d1 = math.hypot(x - w * 0.12, y - h * 0.95) / (w * 0.55)
            d2 = math.hypot(x - w * 0.92, y - h * 0.08) / (w * 0.5)
            r, g, b = BG
            c1 = max(0.0, 1 - d1) ** 3
            c2 = max(0.0, 1 - d2) ** 3
            r += int(c1 * 8 + c2 * 46)
            g += int(c1 * 62 + c2 * 10)
            b += int(c1 * 56 + c2 * 34)
            val = (min(r, 255), min(g, 255), min(b, 255))
            px[x, y] = val
            if x + 1 < w:
                px[x + 1, y] = val

    d = ImageDraw.Draw(img, "RGBA")
    step = 56
    for x in range(0, w, step):
        d.line([(x, 0), (x, h)], fill=(45, 212, 191, 18), width=1)
    for y in range(0, h, step):
        d.line([(0, y), (w, y)], fill=(45, 212, 191, 18), width=1)
    return img


def load_bg(path, w, h):
    """把 Qwen 圖裁成目標比例，左側壓上暗色漸層讓文字讀得出來。"""
    src = Image.open(path).convert("RGB")
    sw, sh = src.size
    scale = max(w / sw, h / sh)
    src = src.resize((int(sw * scale + 0.5), int(sh * scale + 0.5)), Image.LANCZOS)
    left = (src.width - w) // 2
    top = (src.height - h) // 2
    img = src.crop((left, top, left + w, top + h))

    scrim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(scrim)
    # 左 62% 從 88% 黑漸淡到 0，讓標題區乾淨、右側主體保留亮度
    stop = int(w * 0.76)
    for x in range(stop):
        a = int(238 * (1 - x / stop) ** 0.62)
        d.line([(x, 0), (x, h)], fill=(BG[0], BG[1], BG[2], a))
    d.rectangle([(0, 0), (w, int(h * 0.14))], fill=(BG[0], BG[1], BG[2], 110))
    d.rectangle([(0, int(h * 0.86)), (w, h)], fill=(BG[0], BG[1], BG[2], 140))
    return Image.alpha_composite(img.convert("RGBA"), scrim).convert("RGB")


def index_cover(bg=None):
    w, h = 1344, 768
    img = load_bg(bg, w, h) if bg else backdrop(w, h)
    d = ImageDraw.Draw(img)
    d.rectangle([(72, 92), (80, 92 + 210)], fill=MAG)

    f_kicker = font(REG, 30)
    f_title = font(BOLD, 74)
    f_sub = font(REG, 34)
    f_meta = font(REG, 28)

    d.text((116, 92), "IVDC · 深度學習 · 課後核對", font=f_kicker, fill=CYAN)
    d.text((112, 150), "25 頁簡報逐頁核對", font=f_title, fill=FG)
    d.text((112, 246), "勘誤 10 項", font=f_title, fill=FG)

    d.line([(116, 372), (700, 372)], fill=(45, 212, 191, 110), width=2)
    d.text((116, 400), "物件偵測與 CNN：把截圖還原成可執行檔案", font=f_sub, fill=(210, 222, 232))
    d.text((116, 452), "7 頁程式碼被遮 · TensorFlow／PyTorch／YOLOv8", font=f_sub, fill=(210, 222, 232))

    for i, (t, c) in enumerate([("9 支腳本", FG), ("0 錯誤", CYAN), ("MIT", MUT)]):
        x = 116 + i * 230
        d.rounded_rectangle([(x, 560), (x + 190, 626)], 10, outline=c, width=2)
        fw = d.textlength(t, font=f_meta)
        d.text((x + (190 - fw) / 2, 578), t, font=f_meta, fill=c)

    d.text((116, 676), "kalpakjian.github.io", font=font(REG, 24), fill=(110, 125, 140))
    out = os.path.join(COVERS, "ivdc-det-report.png")
    img.save(out)
    print("wrote", out, img.size)


def banner_cover(bg=None):
    """banner 只放圖、不加字（主題會在中央疊日期／字數）。"""
    if bg:
        w, h = 1920, 768
        src = Image.open(bg).convert("RGB")
        sw, sh = src.size
        scale = max(w / sw, h / sh)
        src = src.resize((int(sw * scale + 0.5), int(sh * scale + 0.5)), Image.LANCZOS)
        left = (src.width - w) // 2
        top = (src.height - h) // 2
        img = src.crop((left, top, left + w, top + h))
    else:
        w, h = 1920, 768
        img = backdrop(w, h)
        d = ImageDraw.Draw(img, "RGBA")
        d.rectangle([(120, 210), (150, 558)], fill=MAG)
        for i in range(4):
            y = 214 + i * 88
            d.line([(180, y), (180 + 150 - i * 22, y)], fill=(45, 212, 191, 120), width=3)
        for i in range(6):
            cx, cy, r = 1590 - i * 26, 190 + i * 30, 120 - i * 12
            d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=(232, 62, 140, 60), width=2)
    out = os.path.join(COVERS, "ivdc-det-report-banner.png")
    img.save(out)
    print("wrote", out, img.size)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bg", default=None, help="index 卡片的底圖（Qwen 產的 PNG）")
    ap.add_argument("--bg-banner", default=None, help="banner 的底圖（省略時不重畫 banner）")
    args = ap.parse_args()

    os.makedirs(COVERS, exist_ok=True)
    index_cover(args.bg)
    if args.bg_banner:
        banner_cover(args.bg_banner)
