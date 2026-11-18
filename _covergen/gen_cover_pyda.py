"""產生「Python 初級數據分析員證書」13 章的課程頁封面（1344×768，與站上其他封面同尺寸）。

與 gen_cover_report.py 同一條程序化路線：近黑底 + 細格線 + 兩團光暈 + 左側文字塊，
右側依章節畫對應的圖樣（長條／曲線／矩陣／表格／散點）。不需要 ComfyUI。

用法：
    python _covergen/gen_cover_pyda.py            # 13 張 → source/img/covers/python-da-chNN.png
    python _covergen/gen_cover_pyda.py --only 8   # 只重畫第 8 章
"""
import argparse
import math
import os

from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
COVERS = os.path.join(REPO, "source", "img", "covers")

# Noto（Linux CI／WSL）優先，其次 Windows 內建的微軟正黑體
REG_CANDIDATES = [
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    r"C:\Windows\Fonts\msjh.ttc",
    r"C:\Windows\Fonts\msyh.ttc",
]
BOLD_CANDIDATES = [
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
    r"C:\Windows\Fonts\msjhbd.ttc",
    r"C:\Windows\Fonts\msyhbd.ttc",
]

BG = (10, 14, 20)
FG = (230, 237, 243)
SUB = (200, 213, 225)
MUT = (120, 136, 152)


def font(cands, size):
    for path in cands:
        if not os.path.exists(path):
            continue
        for i in range(8):
            try:
                return ImageFont.truetype(path, size, index=i)
            except OSError:
                break
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    raise SystemExit("no CJK font found; edit REG_CANDIDATES / BOLD_CANDIDATES")


def backdrop(w, h, accent):
    """近黑底 + 兩團光暈（accent 左下、另一側微光）+ 細格線。"""
    img = Image.new("RGB", (w, h), BG)
    px = img.load()
    ax, ay, az = accent
    for y in range(h):
        for x in range(0, w, 2):
            d1 = math.hypot(x - w * 0.78, y - h * 0.22) / (w * 0.42)
            d2 = math.hypot(x - w * 0.98, y - h * 1.02) / (w * 0.5)
            c1 = max(0.0, 1 - d1) ** 3
            c2 = max(0.0, 1 - d2) ** 3
            val = (min(255, BG[0] + int(c1 * ax * 0.42 + c2 * 10)),
                   min(255, BG[1] + int(c1 * ay * 0.42 + c2 * 12)),
                   min(255, BG[2] + int(c1 * az * 0.42 + c2 * 14)))
            px[x, y] = val
            if x + 1 < w:
                px[x + 1, y] = val

    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, w, 56):
        d.line([(x, 0), (x, h)], fill=accent + (16,), width=1)
    for y in range(0, h, 56):
        d.line([(0, y), (w, y)], fill=accent + (16,), width=1)
    return img



def m_bars(d, box, a, hot):
    x0, y0, x1, y1 = box
    n = 7
    step = (x1 - x0) / n
    heights = [0.35, 0.62, 0.48, 0.86, 0.55, 0.74, 0.95]
    d.line([(x0, y1), (x1, y1)], fill=a + (110,), width=2)
    for i, h in enumerate(heights):
        bx = x0 + i * step + step * 0.16
        by = y1 - (y1 - y0) * h
        col = hot if i == 3 else a
        d.rounded_rectangle([(bx, by), (bx + step * 0.62, y1)], 4, fill=col + (70 if i != 3 else 150,),
                            outline=col + (190,), width=2)


def m_line(d, box, a, hot):
    x0, y0, x1, y1 = box
    d.line([(x0, y1), (x1, y1)], fill=a + (110,), width=2)
    d.line([(x0, y0), (x0, y1)], fill=a + (110,), width=2)
    pts = []
    for i in range(41):
        t = i / 40
        v = 0.5 + 0.34 * math.sin(t * 5.1 + 0.6) * (0.45 + 0.55 * t)
        pts.append((x0 + t * (x1 - x0), y1 - v * (y1 - y0)))
    d.polygon(pts + [(x1, y1), (x0, y1)], fill=a + (58,))
    d.line(pts, fill=a + (240,), width=4, joint="curve")
    ex, ey = pts[-1]
    d.ellipse([(ex - 9, ey - 9), (ex + 9, ey + 9)], fill=hot + (230,))


def m_matrix(d, box, a, hot):
    x0, y0, x1, y1 = box
    n = 5
    cell = min(x1 - x0, y1 - y0) // n
    for gx in range(n):
        for gy in range(n):
            x, y = x0 + gx * cell, y0 + gy * cell
            on = (gx * 3 + gy * 5) % 7 in (0, 3)
            d.rectangle([(x, y), (x + cell - 4, y + cell - 4)],
                        fill=a + (150 if on else 26,),
                        outline=(hot if on else a) + (210 if on else 70,), width=2 if on else 1)
    d.line([(x0 - 14, y0), (x0 - 14, y0 + n * cell)], fill=a + (200,), width=3)
    d.line([(x0 + n * cell + 8, y0), (x0 + n * cell + 8, y0 + n * cell)], fill=a + (200,), width=3)


def m_table(d, box, a, hot):
    x0, y0, x1, y1 = box
    rows, cols = 5, 4
    rh = (y1 - y0) / rows
    cw = (x1 - x0) / cols
    d.rounded_rectangle([(x0, y0), (x1, y0 + rh * 0.9)], 4, fill=a + (170,), outline=a + (220,), width=2)
    for r in range(1, rows):
        for c in range(cols):
            x, y = x0 + c * cw, y0 + r * rh
            d.rectangle([(x, y), (x + cw, y + rh)], outline=a + (70,), width=1)
            if c == cols - 1:
                d.rectangle([(x + 6, y + rh * 0.34), (x + cw - 10, y + rh * 0.6)], fill=a + (190,))
            else:
                d.rectangle([(x + 6, y + rh * 0.42), (x + cw - 16, y + rh * 0.56)], fill=a + (70,))


def m_scatter(d, box, a, hot):
    x0, y0, x1, y1 = box
    d.line([(x0, y1), (x1, y1)], fill=a + (110,), width=2)
    d.line([(x0, y0), (x0, y1)], fill=a + (110,), width=2)
    d.line([(x0 + 10, y1 - 22), (x1 - 10, y0 + 26)], fill=hot + (200,), width=3)
    for i in range(26):
        t = ((i * 37) % 89) / 89.0
        vy = 0.15 + 0.7 * t + ((i * 53) % 31) / 130.0
        cx = x0 + 16 + t * (x1 - x0 - 28)
        cy = y1 - min(0.94, vy) * (y1 - y0 - 8)
        r = 6 if i % 5 else 10
        d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(hot if i % 5 == 0 else a) + (170,),
                  outline=(hot if i % 5 == 0 else a) + (220,))


def m_bubbles(d, box, a, hot):
    x0, y0, x1, y1 = box
    d.line([(x0, y1), (x1, y1)], fill=a + (110,), width=2)
    d.line([(x0, y0), (x0, y1)], fill=a + (110,), width=2)
    spec = [(0.18, 0.30, 34), (0.40, 0.55, 52), (0.62, 0.34, 26),
            (0.80, 0.68, 44), (0.50, 0.82, 20), (0.90, 0.24, 16)]
    for i, (fx, fy, r) in enumerate(spec):
        cx, cy = x0 + fx * (x1 - x0), y1 - fy * (y1 - y0)
        d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=a + (70,),
                  outline=(hot if i in (1, 3) else a) + (210,), width=3 if i in (1, 3) else 2)


def m_layers(d, box, a, hot):
    x0, y0, x1, y1 = box
    n = 4
    hh = (y1 - y0) / n
    for i in range(n):
        y = y0 + i * hh
        d.rounded_rectangle([(x0 + i * 12, y), (x1 - i * 12, y + hh * 0.68)], 8,
                            fill=a + (150 if i == 1 else 46,),
                            outline=(hot if i == 1 else a) + (215 if i == 1 else 150,), width=2)
        d.rounded_rectangle([(x0 + i * 12 + 24, y + hh * 0.22),
                             (x0 + i * 12 + 24 + (130 + i * 26), y + hh * 0.22 + 14)], 6,
                            fill=(hot if i == 1 else a) + (150,))


def m_brackets(d, box, a, hot):
    x0, y0, x1, y1 = box
    mid = (y0 + y1) // 2
    w = 26
    d.line([(x0 + w, y0), (x0, y0), (x0, mid), (x0 + w, mid)], fill=a + (210,), width=4)
    d.line([(x0 + w, y1), (x0, y1), (x0, mid), (x0 + w, mid)], fill=a + (210,), width=4)
    d.line([(x1 - w, y0), (x1, y0), (x1, mid), (x1 - w, mid)], fill=a + (210,), width=4)
    d.line([(x1 - w, y1), (x1, y1), (x1, mid), (x1 - w, mid)], fill=a + (210,), width=4)
    inner_c = (x0 + x1) // 2
    for i, ln in enumerate((150, 210, 120, 176)):
        y = y0 + 90 + i * 62
        col = hot if i == 1 else a
        d.rounded_rectangle([(inner_c - ln // 2, y), (inner_c + ln // 2, y + 14)], 7, fill=col + (160,))



# (章號, 標題, 一句話, 頁碼, accent, 圖樣)
CHAPTERS = [
    (1, "行業簡介", "SDLC 與數據分析在開發流程中的位置", "p.2–24", (45, 212, 191), m_layers),
    (2, "Python 數據分析開發工具及工作流程", "變數、容器、函數、模組、CLI 與 API", "p.25–74", (247, 183, 86), m_brackets),
    (3, "基礎統計學原理", "平均數、中位數、分佈與抽樣偏差", "p.75–91", (155, 124, 246), m_line),
    (4, "矩陣代數基礎", "向量、矩陣運算與 OLS 線性迴歸", "p.92–122", (232, 62, 140), m_matrix),
    (5, "數據分析及可視化基礎", "SQL、資料庫與視覺化的四個重點", "p.123–160", (96, 165, 250), m_bars),
    (6, "Python 數據分析技巧", "物件導向、模組、封裝與套件打包", "p.161–204", (163, 230, 53), m_layers),
    (7, "NumPy 套件", "ndarray、broadcasting、ufunc 與切片", "p.205–232", (250, 204, 21), m_matrix),
    (8, "Pandas 套件", "DataFrame 篩選、groupby 與時間序列", "p.233–270", (34, 211, 238), m_table),
    (9, "數據可視化工具介紹與比較", "五套工具：Matplotlib 到 Power BI", "p.271–292", (155, 124, 246), m_bubbles),
    (10, "Matplotlib 套件", "兩大介面、figure 架構與子圖", "p.293–322", (45, 212, 191), m_line),
    (11, "Seaborn 套件", "relplot／histplot／lmplot 與熱力圖", "p.323–358", (232, 62, 140), m_scatter),
    (12, "Plotly 套件", "互動圖表、Dash 與時間序列繪圖", "p.359–396", (96, 165, 250), m_bubbles),
    (13, "數據分析專案：Storytelling", "有效與無效圖表，用數據說一個故事", "p.397–404", (247, 183, 86), m_bars),
]

HOT = (235, 240, 246)  # 強調點一律近白，避免第二套色相打架

# Qwen 底圖的檔名（= plan_pyda_covers.json 的 slug，也是章節頁檔名）
ART_SLUGS = {
    1: "ch01-industry", 2: "ch02-python-tools", 3: "ch03-statistics", 4: "ch04-linear-algebra",
    5: "ch05-viz-basics", 6: "ch06-dataskills", 7: "ch07-numpy", 8: "ch08-pandas",
    9: "ch09-viz-tools", 10: "ch10-matplotlib", 11: "ch11-seaborn", 12: "ch12-plotly",
    13: "ch13-storytelling",
}


def wrap(d, text, fnt, max_w, max_lines=3):
    """把標題切成 1–3 行，行寬盡量平均（避免出現只有一兩個字的孤行）。"""
    def wid(s):
        return d.textlength(s, font=fnt)

    def cuts_for(k):
        if k == 1:
            return [] if wid(text) <= max_w else None
        n = len(text)
        if k == 2:
            best, best_score = None, None
            for i in range(1, n):
                a, b = text[:i].strip(), text[i:].strip()
                if not a or not b:
                    continue
                wa, wb = wid(a), wid(b)
                if wa <= max_w and wb <= max_w:
                    score = abs(wa - wb)
                    if best_score is None or score < best_score:
                        best, best_score = [i], score
            return best
        best, best_score = None, None
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                parts = [text[:i].strip(), text[i:j].strip(), text[j:].strip()]
                if not all(parts):
                    continue
                ws = [wid(p) for p in parts]
                if max(ws) <= max_w:
                    score = max(ws) - min(ws)
                    if best_score is None or score < best_score:
                        best, best_score = [i, j], score
        return best

    for k in range(1, max_lines + 1):
        cuts = cuts_for(k)
        if cuts is not None:
            bounds = [0] + cuts + [len(text)]
            return [text[bounds[i]:bounds[i + 1]].strip() for i in range(len(bounds) - 1)]
    return [text]


def load_bg(path, w, h):
    """Qwen 產的無文字底圖：裁成目標比例，左側壓漸層暗幕讓標題讀得出來。"""
    src = Image.open(path).convert("RGB")
    sw, sh = src.size
    scale = max(w / sw, h / sh)
    src = src.resize((int(sw * scale + 0.5), int(sh * scale + 0.5)), Image.LANCZOS)
    left, top = (src.width - w) // 2, (src.height - h) // 2
    img = src.crop((left, top, left + w, top + h))

    scrim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(scrim)
    stop = int(w * 0.74)
    for x in range(stop):
        a = int(242 * (1 - x / stop) ** 0.60)
        d.line([(x, 0), (x, h)], fill=BG + (a,))
    d.rectangle([(0, h - 64), (w, h)], fill=BG + (110,))
    return Image.alpha_composite(img.convert("RGBA"), scrim).convert("RGB")


def make(num, title, blurb, pages, accent, motif, bg_dir=None):
    w, h = 1344, 768
    art = os.path.join(bg_dir, ART_SLUGS[num] + ".png") if bg_dir else None
    if art and os.path.exists(art):
        img = load_bg(art, w, h)
        d = ImageDraw.Draw(img, "RGBA")
    else:
        img = backdrop(w, h, accent)
        d = ImageDraw.Draw(img, "RGBA")
        motif(d, (742, 200, 1244, 630), accent, HOT)

    f_kick, f_title, f_sub, f_meta = font(REG_CANDIDATES, 27), font(BOLD_CANDIDATES, 54), \
        font(REG_CANDIDATES, 28), font(REG_CANDIDATES, 24)

    d.text((116, 92), f"港專 · Python 數據分析 · 第 {num} 章", font=f_kick, fill=accent + (255,))
    y = 146
    tlines = wrap(d, title, f_title, 648)[:3]
    for ln in tlines:
        d.text((112, y), ln, font=f_title, fill=FG)
        y += 66
    d.rectangle([(72, 92), (80, y - 44)], fill=accent + (255,))
    y += 10
    d.line([(116, y), (116 + 470, y)], fill=accent + (140,), width=2)
    y += 26
    for ln in wrap(d, blurb, f_sub, 620)[:2]:
        d.text((116, y), ln, font=f_sub, fill=SUB)
        y += 42
    d.text((116, 700), f"{pages} · 404 頁掃描筆記 · OCR + 重跑", font=f_meta, fill=MUT)
    d.text((w - 116 - d.textlength("kalpakjian.github.io", font=f_meta), 700),
           "kalpakjian.github.io", font=f_meta, fill=(110, 125, 140))

    out = os.path.join(COVERS, f"python-da-ch{num:02d}.png")
    img.save(out, optimize=True)
    print("wrote", out, img.size, f"{os.path.getsize(out)/1048576:.2f} MB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=int, default=0, help="只畫第 N 章")
    ap.add_argument("--bg-dir", default=os.path.join(HERE, "out", "pyda"),
                    help="Qwen-Image 底圖目錄（chNN.png）；沒有底圖就退回程序化背景")
    args = ap.parse_args()
    os.makedirs(COVERS, exist_ok=True)
    bg_dir = args.bg_dir if os.path.isdir(args.bg_dir) else None
    print("background:", bg_dir or "(procedural)")
    for row in CHAPTERS:
        if args.only and row[0] != args.only:
            continue
        make(*row, bg_dir=bg_dir)
