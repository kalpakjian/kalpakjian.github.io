# -*- coding: utf-8 -*-
"""cnn-gradcam: build the four figures for the Grad-CAM page."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cnn-gradcam")
sys.path.insert(0, HERE)

from gen_cnn_illustrated import (  # noqa: E402
    BG, CELL, INK, DIM, LINE, TEAL, BLUE, AMBER, ROSE, VIOLET,
    esc, text, rect, arrow, matrix_g, empty_grid)

DEFS = ('<defs><marker id="argc" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="%s"/></marker></defs>' % DIM)

ARIA = {
    "flow": "Grad-CAM 的七個步驟：前向取得特徵圖、選類別、反向求梯度、對梯度取平均得到 alpha、加權疊加、ReLU、上採樣疊圖",
    "math": "Grad-CAM 手算：梯度圖平均得到 alpha 0.25、0.1、負 0.2，加權疊加得 2.6、負 0.3、2.1、0.2，ReLU 後只剩三格",
    "layer": "選哪一層做 Grad-CAM：早期 56×56 解析度高但語意淺、中期 28×28、最後 7×7 語意強但要放大 32 倍",
    "shortcut": "熱圖只說模型看哪裡：兩張圖都可能答對，但一張看狗、一張看背景草地，後者代表模型學到捷徑",
}

CAPTIONS = {
    "flow": "七個步驟裡，只有「反向傳播」這一步比 CAM 多了成本；換來的是不必改架構。",
    "math": "梯度的平均是權重、梯度本身不是：同一組特徵圖，CAM 用 0.8、Grad-CAM 用 0.25，熱圖就不一樣。",
    "layer": "越後面語意越強、解析度越低；論文預設用最後一層，需要細節時才往前一層。",
    "shortcut": "熱圖漂亮不代表模型學對：亮在背景草地就是典型的捷徑特徵（shortcut learning）。",
}


def svg(slug, w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'role="img" aria-label="%s">%s<rect x="0.75" y="0.75" width="%s" '
            'height="%s" rx="16" fill="%s" stroke="#222b36" stroke-width="1.5"/>%s</svg>'
            % (w, h, esc(ARIA[slug]), DEFS, w - 1.5, h - 1.5, BG, body))


def chip(x, y, w, h, label, sub, colour, size=11):
    out = [rect(x, y, w, h, stroke=colour + "aa", sw=1.3, fill=CELL, rx=7),
           text(x + w / 2, y + (24 if sub else h / 2 + 4), label, size, INK, "700",
                "middle")]
    if sub:
        out.append(text(x + w / 2, y + h / 2 + 14, sub, 8.5, DIM, "normal", "middle"))
    return "".join(out)


def fig_flow():
    steps = [("1", "前向", "A¹…Aᴷ", TEAL), ("2", "選類別", "yᶜ", TEAL),
             ("3", "反向", "∂yᶜ/∂Aᵏ", BLUE), ("4", "梯度平均", "αᵏᶜ", AMBER),
             ("5", "加權疊加", "Lᶜ", AMBER), ("6", "ReLU", "只留正", VIOLET),
             ("7", "上採樣", "224×224", ROSE)]
    body = [text(40, 44, "Grad-CAM 的七個步驟", 20, INK, "700"),
            text(40, 72, "前六步都在特徵圖上算；只有最後一步是為了畫出來", 13, DIM)]
    for i, (num, name, sub, colour) in enumerate(steps):
        x = 36 + i * 136
        body.append(rect(x, 116, 120, 92, stroke=colour + "88", sw=1.4, fill=CELL,
                         rx=9))
        body.append(text(x + 14, 142, num + ".", 11.5, colour, "700"))
        body.append(text(x + 34, 142, name, 11.5, INK, "700"))
        body.append(text(x + 60, 176, sub, 9.5, DIM, "normal", "middle"))
        if i < len(steps) - 1:
            body.append(arrow(x + 122, 162, x + 133, 162))
    body.append(rect(36, 232, 928, 96, stroke=BLUE + "55", fill="#1c2230", rx=12))
    body.append(text(56, 260, "公式：α[k, c] = (1/Z) ΣΣ ∂yᶜ/∂Aᵏ(i, j)　　"
                               "Lᶜ = ReLU( Σ_k α[k, c] · Aᵏ )", 12, INK, "700"))
    body.append(text(56, 288, "Z = H×W；ReLU 之後只留下「支持這個類別」的區域。", 11.5, DIM))
    body.append(text(56, 312, "跟 CAM 的差別只有權重來源：一個拿線性層的 w，一個拿梯度的平均。",
                     11.5, DIM))
    body.append(text(40, 356, "成本：多一次反向傳播；好處：不必改架構、不必重訓。", 12, DIM))
    return svg("flow", 1000, 380, "".join(body))



def fig_math():
    grads = [([[0.2, 0.4], [0.1, 0.3]], "α₁ = 0.25", TEAL),
             ([[0.1, 0.1], [0.1, 0.1]], "α₂ = 0.10", BLUE),
             ([[-0.2, -0.2], [-0.2, -0.2]], "α₃ = −0.20", VIOLET)]
    body = [text(40, 44, "手算一次：梯度圖 → 權重 → 加權疊加", 20, INK, "700"),
            text(40, 72, "三張 2×2 特徵圖、三張梯度圖；α 是梯度圖的平均", 13, DIM)]
    for i, (g, a, colour) in enumerate(grads):
        x = 50 + i * 150
        body.append(text(x, 108, "∂y/∂A%d" % (i + 1), 10.5, DIM))
        body.append(matrix_g(x, 118, 44, g, 10, colour, ()))
        body.append(text(x + 44, 220, a, 11.5, colour, "700", "middle"))
    body.append(text(500, 108, "L = Σ α · A", 10.5, DIM))
    body.append(matrix_g(500, 118, 44, [[2.6, -0.3], [2.1, 0.2]], 9.5, AMBER, [(0, 1)]))
    body.append(text(544, 220, "加權疊加", 10.5, DIM, "normal", "middle"))
    body.append(arrow(556, 140, 596, 140))
    body.append(text(700, 108, "ReLU(L)", 10.5, DIM))
    body.append(matrix_g(660, 118, 44, [[2.6, 0.0], [2.1, 0.2]], 9.5, ROSE, ()))
    body.append(text(704, 220, "負值清掉", 10.5, DIM, "normal", "middle"))
    body.append(rect(50, 252, 900, 104, stroke=BLUE + "55", fill="#1c2230", rx=12))
    body.append(text(70, 280, "① α₁ = (0.2 + 0.4 + 0.1 + 0.3) / 4 = 0.25　"
                               "② L(0,0) = 0.25×10 + 0.1×1 − 0.2×0 = 2.6", 11.5, INK))
    body.append(text(70, 306, "③ L(0,1) = 0.25×0 + 0.1×1 − 0.2×2 = −0.3 → ReLU 後變 0（4 格去掉 1 格）",
                     11.5, DIM))
    body.append(text(70, 334, "同一組特徵圖改用 CAM 的權重 0.8 / 0.1 / −0.2，"
                               "熱圖會是 8.1 / −0.3 / 6.5 / 1.3——兩張圖不一樣。", 11.5, DIM))
    return svg("math", 1000, 380, "".join(body))


def fig_layer():
    layers = [("早期 conv", "56×56×64", 16, "×4", TEAL, "細節清楚，看到的是邊緣、紋理"),
              ("中期 conv", "28×28×128", 10, "×8", BLUE, "折衷：部件層級"),
              ("最後 conv", "7×7×512", 7, "×32", ROSE, "語意最強，但只有 49 格")]
    body = [text(40, 44, "要拿哪一層做 Grad-CAM？", 20, INK, "700"),
            text(40, 72, "同一個模型、同一張影像，換一層就是另一張熱圖", 13, DIM)]
    for i, (name, shape, n, scale, colour, note) in enumerate(layers):
        x = 60 + i * 300
        size = 96.0
        body.append(rect(x, 100, 250, 200, stroke=colour + "88", sw=1.4, fill=CELL,
                         rx=10, opacity=0.6))
        body.append(text(x + 16, 126, name, 12, colour, "700"))
        body.append(text(x + 16, 148, shape, 11, INK))
        body.append(rect(x + 16, 162, size, size, stroke=colour, sw=1.2, rx=2,
                         fill=colour + "14"))
        for k in range(1, n):
            p = x + 16 + size * k / n
            q = 162 + size * k / n
            body.append('<line x1="%s" y1="162" x2="%s" y2="%s" stroke="%s" '
                        'stroke-width="0.6" opacity="0.5"/>' % (p, p, 162 + size, colour))
            body.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
                        'stroke-width="0.6" opacity="0.5"/>'
                        % (x + 16, q, x + 16 + size, q, colour))
        body.append(text(x + 128, 214, "熱圖", 10, DIM))
        body.append(text(x + 128, 236, "上採樣 " + scale, 10.5, colour, "700"))
        body.append(text(x + 16, 286, note, 10, DIM))
    body.append(text(40, 332, "論文預設用最後一層卷積：仍保留空間資訊，又已經是高階語意；"
                               "要更細的位置時往前一兩層（解析度換語意）。", 12, DIM))
    return svg("layer", 1000, 360, "".join(body))


def fig_shortcut():
    body = [text(40, 44, "熱圖漂亮，不代表模型學對了", 20, INK, "700"),
            text(40, 72, "同一題「黃金獵犬」，兩種模型都能答對，但看的東西不一樣", 13, DIM)]
    panels = [("模型 A：看狗", TEAL, [(3, 3), (4, 4), (3, 5), (5, 4)], "高亮在頭與身體"),
              ("模型 B：看背景草地", ROSE, [(0, 0), (1, 1), (0, 2), (1, 3)], "高亮在右下角草地")]
    for i, (name, colour, cells, note) in enumerate(panels):
        x = 60 + i * 460
        body.append(rect(x, 96, 400, 230, stroke=colour + "88", sw=1.4, fill=CELL, rx=12,
                         opacity=0.6))
        body.append(text(x + 16, 122, name, 12, colour, "700"))
        for (r, c) in cells:
            body.append(rect(x + 60 + c * 34, 140 + r * 34, 34, 34, stroke=colour,
                             sw=1.2, fill=colour + "44", rx=3))
        body.append(empty_grid(x + 60, 140, 34, 6, LINE, 0.7, 0.4))
        body.append(text(x + 16, 300, note, 10.5, DIM))
    body.append(rect(60, 344, 890, 70, stroke=AMBER + "55", fill="#1c2230", rx=12))
    body.append(text(80, 370, "兩張熱圖都在說「我看這裡」，但只有 A 的答案有道理。", 12, INK))
    body.append(text(80, 396, "亮在背景＝捷徑特徵（shortcut learning）；這時要換資料、做"
                               "遮擋測試（occlusion），不能只看準確率。", 11.5, DIM))
    return svg("shortcut", 1000, 430, "".join(body))


FIGS = {"flow": fig_flow, "math": fig_math, "layer": fig_layer,
        "shortcut": fig_shortcut}


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug in FIGS:
        path = os.path.join(OUT, slug + ".svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(FIGS[slug]())
        print("wrote", path)
    print("\nfigures:", len(CAPTIONS))


if __name__ == "__main__":
    main()
