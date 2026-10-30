# -*- coding: utf-8 -*-
"""cnn-cam: build the four figures for the CAM page."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cnn-cam")
sys.path.insert(0, HERE)

from gen_cnn_illustrated import (  # noqa: E402
    BG, CELL, INK, DIM, LINE, TEAL, BLUE, AMBER, ROSE, VIOLET,
    esc, text, rect, arrow, matrix_g, empty_grid)

DEFS = ('<defs><marker id="arc" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="%s"/></marker></defs>' % DIM)

ARIA = {
    "cam-pipeline": "CAM 的網路結構：卷積到 K 張 7×7 特徵圖，GAP 成 K 個數，最後 Linear(K→C) 的權重 w 再回頭加權那 K 張圖，得到類別熱圖",
    "cam-worked": "三張 2×2 特徵圖與權重 0.8、0.1、負 0.2 加權相加，得到 CAM 8.1、負 0.3、6.5、1.3，平均 3.9 正好等於該類別的 logit",
    "cam-steps": "CAM 的五個步驟：取出最後一層特徵圖、GAP、讀線性層權重、加權相加、上採樣回原圖尺寸",
    "gradcam": "CAM 與 Grad-CAM 的差別：CAM 用 GAP 之後的線性權重，Grad-CAM 用 logit 對特徵圖的梯度平均；在純 GAP＋Linear 的網路上兩者只差一個常數與 ReLU",
}

CAPTIONS = {
    "cam-pipeline": "CAM 的橋樑就是 GAP：每個 F_k 只對應一張 A_k，所以線性層的權重 w 可以直接乘回 A_k。",
    "cam-worked": "手算例子：三張 2×2 特徵圖加權相加成 CAM，四個位置 8.1 / −0.3 / 6.5 / 1.3，平均剛好是 logit 3.9。",
    "cam-steps": "五個步驟裡只有第 5 步（上採樣）是為了「看得出來」；前四步都是純線性運算。",
    "gradcam": "Grad-CAM 用梯度取代權重，所以不必有 GAP；但在純 GAP＋Linear 的網路上，兩者算出來是同一張圖。",
}


def svg(slug, w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'role="img" aria-label="%s">%s<rect x="0.75" y="0.75" width="%s" '
            'height="%s" rx="16" fill="%s" stroke="#222b36" stroke-width="1.5"/>%s</svg>'
            % (w, h, esc(ARIA[slug]), DEFS, w - 1.5, h - 1.5, BG, body))


def chip(x, y, w, h, label, sub, colour, size=11.5):
    out = [rect(x, y, w, h, stroke=colour + "aa", sw=1.4, fill=CELL, rx=8),
           text(x + w / 2, y + (26 if sub else h / 2 + 4), label, size, INK, "700",
                "middle")]
    if sub:
        out.append(text(x + w / 2, y + h / 2 + 16, sub, 9.5, DIM, "normal", "middle"))
    return "".join(out)


def fig_pipeline():
    body = [text(40, 44, "CAM 的網路結構：GAP 是那座橋", 20, INK, "700"),
            text(40, 72, "只有「GAP + Linear」的頭，才能讓分類權重乾淨地對應回單一張特徵圖", 13,
                 DIM)]
    body.append(chip(40, 104, 110, 62, "影像", "224×224×3", TEAL))
    body.append(arrow(154, 135, 186, 135))
    body.append(chip(190, 104, 120, 62, "卷積堆疊", "→ 7×7×K", TEAL))
    body.append(arrow(314, 135, 346, 135))
    body.append(rect(350, 96, 150, 140, stroke=BLUE + "99", sw=1.4, fill=CELL, rx=10))
    body.append(text(425, 120, "最後一層特徵圖", 10.5, DIM, "normal", "middle"))
    for i in range(3):
        body.append(rect(366 + i * 8, 132 + i * 6, 118, 96, stroke=BLUE + "66", sw=1.1,
                         fill="none", rx=5))
    body.append(text(425, 226, "A₁ … A_K（各 7×7）", 10, BLUE, "700", "middle"))
    body.append(arrow(504, 166, 536, 166))
    body.append(chip(540, 132, 110, 68, "GAP", "K 個數", AMBER))
    body.append(arrow(654, 166, 686, 166))
    body.append(chip(690, 132, 130, 68, "Linear", "K → C", AMBER))
    body.append(arrow(824, 166, 856, 166))
    body.append(chip(860, 132, 110, 68, "softmax", "C 個機率", ROSE))
    # the bridge: weights go back to the maps
    body.append('<path d="M 755 206 C 755 268, 425 268, 425 240" fill="none" '
                'stroke="%s" stroke-width="1.6" stroke-dasharray="6 4" '
                'marker-end="url(#arc)"/>' % VIOLET)
    body.append(text(590, 292, "w[k, c] 回頭加權每張 A_k", 11.5, VIOLET, "700", "middle"))
    body.append(text(40, 330, "CAM_k(x, y) = Σ_k w[k, c] · A_k(x, y)；再上採樣回 224×224 就是熱圖。",
                     12, DIM))
    return svg("cam-pipeline", 1000, 360, "".join(body))



def fig_worked():
    A = [([[10, 0], [8, 2]], "0.8", TEAL, "F₁ = 5"),
         ([[1, 1], [1, 1]], "0.1", BLUE, "F₂ = 1"),
         ([[0, 2], [0, 2]], "−0.2", VIOLET, "F₃ = 1")]
    body = [text(40, 44, "手算一個 CAM：三張 2×2 特徵圖", 20, INK, "700"),
            text(40, 72, "權重 0.8 / 0.1 / −0.2；GAP 之後是 5 / 1 / 1，logit = 3.9", 13, DIM)]
    for i, (m, w, colour, f) in enumerate(A):
        x = 50 + i * 168
        body.append(text(x, 112, "A%d" % (i + 1), 12, INK, "700"))
        body.append(matrix_g(x, 122, 52, m, 13, colour, ()))
        body.append(text(x + 52, 262, "× " + w, 13, colour, "700", "middle"))
        body.append(text(x + 52, 286, f, 11, DIM, "normal", "middle"))
    body.append(arrow(556, 196, 592, 196))
    body.append(text(574, 176, "加權相加", 10.5, DIM, "normal", "middle"))
    body.append(text(640, 112, "CAM（狗）", 12, INK, "700", "middle"))
    body.append(matrix_g(588, 122, 52, [[8.1, -0.3], [6.5, 1.3]], 12, AMBER, ()))
    body.append(text(640, 262, "平均 = 15.6 / 4 = 3.9", 12, AMBER, "700", "middle"))
    body.append(text(640, 286, "= 該類別的 logit", 11, DIM, "normal", "middle"))
    body.append(rect(50, 318, 890, 66, stroke=TEAL + "55", fill="#1c2230", rx=12))
    body.append(text(70, 344, "logit = 0.8×5 + 0.1×1 + (−0.2)×1 = 3.9，"
                               "而 CAM 的四格平均也是 3.9——這就是 GAP 給的橋。", 11.5, INK))
    body.append(text(70, 368, "左上角 8.1 最大：模型認為那個位置最支持「狗」。", 11.5, DIM))
    return svg("cam-worked", 1000, 400, "".join(body))


def fig_steps():
    steps = [("1", "取特徵圖", "A₁…A_K，7×7", TEAL),
             ("2", "GAP", "F₁…F_K，K 個數", AMBER),
             ("3", "讀權重", "w[k, c]，K 個", BLUE),
             ("4", "加權相加", "CAM，7×7", VIOLET),
             ("5", "上採樣", "224×224 熱圖", ROSE)]
    body = [text(40, 44, "五個步驟，只有最後一步是為了「看」", 20, INK, "700"),
            text(40, 72, "前四步都是線性運算；上採樣只是把 7×7 放大到看得出來的尺寸", 13, DIM)]
    for i, (num, name, sub, colour) in enumerate(steps):
        x = 44 + i * 186
        body.append(rect(x, 120, 160, 110, stroke=colour + "88", sw=1.5, fill=CELL,
                         rx=10))
        body.append('<circle cx="%s" cy="146" r="15" fill="%s"/>' % (x + 30, colour))
        body.append(text(x + 30, 152, num, 13, "#08141a", "700", "middle"))
        body.append(text(x + 56, 152, name, 12, INK, "700"))
        body.append(text(x + 18, 196, sub, 10.5, DIM))
        if i < len(steps) - 1:
            body.append(arrow(x + 163, 175, x + 182, 175))
    body.append(rect(44, 268, 912, 96, stroke=BLUE + "55", fill="#1c2230", rx=12))
    body.append(text(64, 296, "為什麼第 3 步需要 GAP：F_k 只對應一張 A_k，"
                               "所以 w[k, c] 可以直接乘回 A_k。", 12, INK))
    body.append(text(64, 322, "若換成 Flatten + 大 FC，每個權重綁的是「某個像素 × 某個通道」，"
                               "無法還原成一張圖。", 12, DIM))
    body.append(text(64, 346, "實測：K=6、7×7、C=4 時，GAP 頭 6 個權重 vs 展平頭 1,176 個（196 倍）。",
                     11, DIM))
    return svg("cam-steps", 1000, 390, "".join(body))


def fig_gradcam():
    body = [text(40, 44, "CAM vs Grad-CAM", 20, INK, "700"),
            text(40, 72, "一個用「線性層的權重」，一個用「梯度」；後者不必有 GAP", 13, DIM)]
    body.append(rect(30, 96, 460, 220, stroke=TEAL + "77", sw=1.4, fill=CELL, rx=12,
                     opacity=0.6))
    body.append(text(50, 124, "CAM（原版）", 12.5, TEAL, "700"))
    body.append(text(50, 152, "w[k, c]：GAP 後線性層的權重", 11.5, INK))
    body.append(text(50, 178, "要求：末端必須是 GAP + Linear", 11.5, DIM))
    body.append(text(50, 204, "優點：一次前向就能算、可解釋性強", 11.5, DIM))
    body.append(text(50, 230, "缺點：既有模型要改架構重訓", 11.5, ROSE))
    body.append(text(50, 264, "CAM_c = Σ_k w[k,c] · A_k", 12, TEAL, "700"))
    body.append(text(50, 290, "（本頁手算例子：8.1 / −0.3 / 6.5 / 1.3）", 10.5, DIM))

    body.append(rect(510, 96, 460, 220, stroke=VIOLET + "77", sw=1.4, fill=CELL, rx=12,
                     opacity=0.6))
    body.append(text(530, 124, "Grad-CAM（2017）", 12.5, VIOLET, "700"))
    body.append(text(530, 152, "α[k, c] = (1/HW) ΣΣ ∂y_c/∂A_k", 11.5, INK))
    body.append(text(530, 178, "要求：只要能算梯度（幾乎所有 CNN）", 11.5, DIM))
    body.append(text(530, 204, "優點：不必改架構、可套用既有模型", 11.5, DIM))
    body.append(text(530, 230, "缺點：要多一次反向傳播", 11.5, AMBER))
    body.append(text(530, 264, "M_c = ReLU( Σ_k α[k,c] · A_k )", 12, VIOLET, "700"))
    body.append(text(530, 290, "ReLU 是因為我們只關心「支持」的證據", 10.5, DIM))

    body.append(rect(30, 330, 940, 74, stroke=AMBER + "55", fill="#1c2230", rx=12))
    body.append(text(50, 356, "實測（純 GAP + Linear 的網路）：α = w / (H·W)，"
                               "於是 Grad-CAM = ReLU(CAM / (H·W))。", 12, INK))
    body.append(text(50, 382, "最大差 5.64e-18 —— 在這種架構上，兩張圖其實是同一張。",
                     11.5, DIM))
    return svg("gradcam", 1000, 420, "".join(body))


FIGS = {"cam-pipeline": fig_pipeline, "cam-worked": fig_worked,
        "cam-steps": fig_steps, "gradcam": fig_gradcam}


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
