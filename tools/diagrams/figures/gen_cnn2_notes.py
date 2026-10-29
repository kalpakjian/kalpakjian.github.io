# -*- coding: utf-8 -*-
"""cnn2-notes: build the SVG figures for the CNN 2 lesson page.

    python gen_cnn2_notes.py        # writes fig/*.svg + prints the caption map

`build_cnn2_notes.py`然后負責把它們內嵌進 md 並轉成 index.html。
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cnn2-notes")

BG, INK, DIM = "#0d1117", "#e6edf3", "#8b949e"
TEAL, AMBER, ROSE, BLUE = "#4ecdc4", "#e0a458", "#ff7b72", "#58a6ff"
FONT = "'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif"

# 每張圖唯一的 aria-label（契約 §12.2：量測工具與螢幕閱讀器都靠它定位）
ARIA = {
    "overview": "CNN 分類網路架構：Input → Conv 32 → Pool → Conv 64 → Pool → Flatten → Dense 1024 → Softmax 10 類",
    "hierarchy": "表徵學習的三層階梯：低層學邊緣與暗斑，中層組合出眼睛、耳朵、鼻子，高層才有臉部結構",
    "local": "卷積層的局部連接：3×3 濾波器滑過 6×6 輸入的一小塊 patch，同一組權重滑遍全圖",
    "volume": "輸出體積與步幅：6×6 輸入、3×3 核、stride 2 得到 3×3 輸出，depth 等於濾波器數量",
    "pool": "2×2 最大池化：4×4 輸入取每個鄰域的最大值，降成 2×2 輸出且沒有參數",
    "tasks": "同一個卷積 backbone 接四種任務頭：分類、分割、上色、控制",
    "params": "參數量分佈：1,668,490 個參數中 Dense(1024) 佔 1,639,424（98.2%），Conv 層共 18,816（1.1%），輸出層 10,250（0.6%）",
    "accuracy": "CIFAR-10 準確率階梯：課程架構 0.80、加 dropout 0.81、小型 VGG 0.89、VGG+cutout 0.94、ResNet-18+cutout 0.96",
}


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(slug, w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{ARIA[slug]}">{DEFS}'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')


DEFS = (f'<defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        f'orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{DIM}"/></marker></defs>')


def box(x, y, w, h, label, colour=TEAL, size=13, sub=""):
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="none" '
           f'stroke="{colour}" stroke-width="1.6"/>'
           f'<text x="{x + w / 2}" y="{y + h / 2 + (-4 if sub else 5)}" fill="{INK}" '
           f'font-size="{size}" text-anchor="middle" font-family="{FONT}">{esc(label)}</text>')
    if sub:
        out += (f'<text x="{x + w / 2}" y="{y + h / 2 + 13}" fill="{DIM}" font-size="10.5" '
                f'text-anchor="middle" font-family="{FONT}">{esc(sub)}</text>')
    return out


def arrow(x1, y1, x2, y2, colour=DIM):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" '
            f'stroke-width="1.5" marker-end="url(#a)"/>')


def label(x, y, text, colour=DIM, size=11.5, anchor="start"):
    return (f'<text x="{x}" y="{y}" fill="{colour}" font-size="{size}" '
            f'text-anchor="{anchor}" font-family="{FONT}">{esc(text)}</text>')


def grid(x, y, n, cell, colour, fills=(), tag=""):
    out = []
    for i in range(n):
        for j in range(n):
            out.append(f'<rect x="{x + j * cell}" y="{y + i * cell}" width="{cell}" '
                       f'height="{cell}" fill="none" stroke="{colour}" stroke-width="0.8" '
                       f'opacity="0.5"/>')
    for (r, c, col) in fills:
        out.append(f'<rect x="{x + c * cell}" y="{y + r * cell}" width="{cell}" '
                   f'height="{cell}" fill="{col}" opacity="0.3"/>')
    if tag:
        out.append(label(x, y - 7, tag))
    return "".join(out)


def fig_overview():
    steps = [("Input", "影像"), ("Conv 32", "3×3+ReLU"), ("Pool", "2×2"),
             ("Conv 64", "3×3+ReLU"), ("Pool", "2×2"), ("Flatten", "→ 向量"),
             ("Dense", "1024+ReLU"), ("Softmax", "10 類")]
    bw, gap, bh, y = 96, 16, 56, 60
    body, x = [label(20, 30, "前五層學特徵，後三層做分類", AMBER, 12.5)], 20
    for i, (main, sub) in enumerate(steps):
        col = TEAL if i < 5 else (AMBER if i < 7 else ROSE)
        body.append(box(x, y, bw, bh, main, col, 12, sub))
        if i < len(steps) - 1:
            body.append(arrow(x + bw, y + bh / 2, x + bw + gap - 3, y + bh / 2))
        x += bw + gap
    body.append(label(20, y + bh + 30, "可訓練的權重只在 Conv 與 Dense；Pool 與 Softmax 沒有參數"))
    return svg("overview", 920, 165, "".join(body))


def fig_hierarchy():
    tiers = [("低層", "邊緣、暗斑", TEAL, 30), ("中層", "眼睛、耳朵、鼻子", BLUE, 280),
             ("高層", "臉部結構", AMBER, 530)]
    body = []
    for tag, what, col, x in tiers:
        body.append(f'<rect x="{x}" y="36" width="230" height="80" rx="9" fill="none" '
                    f'stroke="{col}" stroke-width="1.8"/>')
        body.append(label(x + 16, 62, tag, col, 12.5))
        body.append(label(x + 16, 92, what, INK, 14))
    body.append(arrow(262, 76, 276, 76))
    body.append(arrow(512, 76, 526, 76))
    body.append(label(30, 146, "沒有人教它「眼睛長什麼樣」——三層都是訓練時順手學出來的"))
    return svg("hierarchy", 800, 165, "".join(body))


def fig_local():
    body = [grid(30, 26, 6, 26, DIM, fills=[(1, 1, AMBER), (1, 2, AMBER), (2, 1, AMBER),
                                             (2, 2, AMBER)], tag="輸入 6×6"),
            f'<rect x="56" y="52" width="52" height="52" fill="none" stroke="{AMBER}" '
            f'stroke-width="2.2"/>',
            arrow(196, 88, 240, 88),
            box(244, 58, 140, 58, "一個神經元", TEAL, 12.5, "加權和 + bias"),
            arrow(388, 88, 424, 88),
            box(428, 68, 52, 38, "ReLU", BLUE, 12.5),
            arrow(484, 88, 520, 88),
            box(524, 58, 156, 58, "特徵圖 1 格", AMBER, 12.5, "同一組權重滑遍全圖"),
            label(30, 200, "3×3 濾波器 = 9 個權重，走到哪裡都同一組")]
    return svg("local", 700, 215, "".join(body))


def fig_volume():
    body = [grid(24, 30, 6, 24, DIM, fills=[(0, 0, TEAL), (0, 2, TEAL), (2, 0, TEAL),
                                            (2, 2, TEAL), (4, 0, TEAL), (4, 2, TEAL)],
                 tag="輸入 6×6，k=3、s=2"),
            arrow(192, 102, 226, 102),
            grid(230, 42, 3, 24, TEAL, tag="輸出 3×3"),
            box(340, 34, 300, 60, "O = (N + 2P − F) / S + 1", AMBER, 15),
            label(340, 120, "depth（d）= 濾波器數量，不是輸入通道數", TEAL, 12),
            label(230, 152, "每一格 = 一個濾波器在該位置的輸出")]
    return svg("volume", 660, 195, "".join(body))


def fig_pool():
    vals = [[1, 3, 2, 0], [4, 6, 1, 2], [0, 2, 8, 5], [1, 1, 3, 4]]
    cell = 28
    body = [grid(30, 30, 4, cell, DIM, tag="輸入 4×4")]
    for r in range(4):
        for c in range(4):
            body.append(label(30 + c * cell + cell / 2, 30 + r * cell + 18,
                              str(vals[r][c]), INK, 12, "middle"))
    for (r0, c0) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        body.append(f'<rect x="{30 + c0 * cell}" y="{30 + r0 * cell}" width="{2 * cell}" '
                    f'height="{2 * cell}" fill="none" stroke="{AMBER}" stroke-width="2"/>')
    body.append(arrow(158, 86, 196, 86))
    body.append(grid(200, 58, 2, cell, TEAL, tag="輸出 2×2"))
    for i, v in enumerate([6, 2, 2, 8]):
        body.append(label(200 + (i % 2) * cell + cell / 2, 58 + (i // 2) * cell + 18,
                          str(v), AMBER, 13, "middle"))
    body.append(box(310, 34, 300, 58, "面積 ÷ 4、參數 0 個", BLUE, 14,
                    "鄰域內平移，輸出可能不變"))
    body.append(label(310, 128, "代價：只知道「這區有」，不知道在哪個像素"))
    return svg("pool", 630, 150, "".join(body))


def fig_tasks():
    heads = [("分類 head", "全連接 + softmax", AMBER), ("分割 head", "全卷積 + 轉置卷積", BLUE),
             ("上色 head", "2 個色度通道", AMBER), ("控制 head", "方向盤、油門", BLUE)]
    bh, dy, y0 = 38, 46, 12
    body = [box(24, 64, 150, 62, "卷積 backbone", TEAL, 12.5, "同一組特徵抽取器")]
    for k, (name, sub, col) in enumerate(heads):
        y = y0 + k * dy
        body.append(arrow(178, 95, 216, y + bh / 2))
        body.append(box(220, y, 190, bh, name, col, 11.5, sub))
    body.append(label(24, 210, "換頭就換任務：分割、上色、超解析、端到端控制都是這樣組出來的"))
    return svg("tasks", 470, 220, "".join(body))


def fig_params():
    """參數量分佈：1,668,490 個參數裡 98.2% 在 Flatten 之後。"""
    total = 1668490
    segs = [("Dense(1024)", 1639424, AMBER, "98.2%"),
            ("Conv 32 + Conv 64", 18816, TEAL, "1.1%"),
            ("Dense(10, softmax)", 10250, BLUE, "0.6%")]
    bw, x0, y0, bh = 820, 40, 56, 44
    body = [label(40, 30, "1,668,490 個參數，98.2% 集中在 Flatten 之後", AMBER, 13)]
    x = x0
    for name, n, col, pct in segs:
        w = bw * n / total
        rx = 3 if w > 20 else 0
        body.append(f'<rect x="{x:.2f}" y="{y0}" width="{w:.2f}" height="{bh}" '
                    f'rx="{rx}" fill="{col}" opacity="0.85"/>')
        x += w
    body.append(f'<rect x="{x0}" y="{y0}" width="{bw}" height="{bh}" rx="1" '
                f'fill="none" stroke="{DIM}" stroke-width="0.8" opacity="0.5"/>')
    for i, (name, n, col, pct) in enumerate(segs):
        ly = 148 + i * 30
        body.append(f'<rect x="40" y="{ly - 10}" width="12" height="12" rx="3" '
                    f'fill="{col}" opacity="0.85"/>')
        body.append(label(62, ly, "%s  %s（%s）" % (name, format(n, ","), pct),
                          INK, 12.5))
    body.append(label(40, 148 + 3 * 30, "MaxPool / Flatten：0 個參數", DIM, 11.5))
    return svg("params", 900, 250, "".join(body))


def fig_accuracy():
    """六組設定的準確率階梯（橫軸從 0.70 起，避免差異被壓扁）。"""
    data = [("課程的架構（20 輪）", 0.80), ("加上 dropout 0.3", 0.81),
            ("小型 VGG（6 層卷積 + BN）", 0.89), ("VGG + cutout（200 輪）", 0.94),
            ("ResNet-18 + cutout（200 輪）", 0.96)]
    x0, x1, lo, hi = 210, 860, 0.70, 1.00
    body = [label(30, 30, "同一份資料：換架構與排程，0.80 → 0.96", AMBER, 13)]

    def vx(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    for t in (0.70, 0.80, 0.90, 1.00):
        body.append(f'<line x1="{vx(t):.1f}" y1="52" x2="{vx(t):.1f}" y2="262" '
                    f'stroke="{DIM}" stroke-width="0.8" opacity="0.22"/>')
        body.append(label(vx(t), 284, "%.2f" % t, DIM, 11, "middle"))

    for i, (name, v) in enumerate(data):
        cy = 78 + i * 40
        col = TEAL if i < 2 else (AMBER if i < 4 else ROSE)
        body.append(f'<rect x="{x0}" y="{cy - 11}" width="{vx(v) - x0:.1f}" '
                    f'height="22" rx="4" fill="{col}" opacity="0.85"/>')
        body.append(label(x0 - 12, cy + 4, name, INK, 11.5, "end"))
        body.append(label(vx(v) + 10, cy + 4, "%.2f" % v, col, 12.5))

    body.append(f'<line x1="{x0}" y1="52" x2="{x0}" y2="262" stroke="{DIM}" '
                f'stroke-width="1"/>')
    body.append(label(30, 284, "橫軸從 0.70 起", DIM, 10.5))
    return svg("accuracy", 900, 300, "".join(body))


FIGS = {"overview": fig_overview, "hierarchy": fig_hierarchy, "local": fig_local,
        "volume": fig_volume, "pool": fig_pool, "tasks": fig_tasks,
        "params": fig_params, "accuracy": fig_accuracy}

CAPTIONS = {
    "overview": "整個分類網路：前五層抽特徵，後三層把特徵變成類別分數；可訓練的參數只在 Conv 與 Dense。",
    "hierarchy": "表徵學習的階層：第一層看到邊緣，第二層組合出部件，第三層才有物件結構。",
    "local": "局部連接：一個神經元只讀一小塊 patch，同一組權重滑過整張圖就是參數共享。",
    "volume": "輸出體積與步幅。depth 由濾波器數量決定，面積由公式算。",
    "pool": "最大池化：2×2 取最大，面積變四分之一，而且沒有參數可學。",
    "tasks": "同一個 backbone、換一個頭，就是另一個任務。",
    "params": "參數量分佈：98.2% 集中在 Flatten 之後的 Dense(1024)，卷積層本身只佔 1.1%。",
    "accuracy": "六組設定的 CIFAR-10 測試準確率；換架構與長排程把 0.80 推到 0.96（橫軸從 0.70 起）。",
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, fn in FIGS.items():
        path = os.path.join(OUT, slug + ".svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(fn())
        print("wrote", path)


if __name__ == "__main__":
    main()

