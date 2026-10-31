# -*- coding: utf-8 -*-
"""cnn-cam-vs-gradcam: build the three comparison figures."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cnn-cam-vs-gradcam")
sys.path.insert(0, HERE)

from gen_cnn_illustrated import (  # noqa: E402
    BG, CELL, INK, DIM, LINE, TEAL, BLUE, AMBER, ROSE, VIOLET,
    esc, text, rect, arrow, matrix_g, empty_grid)

DEFS = ('<defs><marker id="arcg" markerWidth="8" markerHeight="8" refX="6" refY="3" '
        'orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="%s"/></marker></defs>' % DIM)

ARIA = {
    "formula": "兩個公式並排：CAM 用訓練好的權重 w 乘特徵圖，Grad-CAM 用梯度平均 alpha 乘特徵圖，兩者只差在那 K 個數字怎麼來",
    "per-image": "同一組分類權重 w，對兩張不同影像：純 GAP 加 Linear 的模型 alpha 完全不變，中間有 ReLU 時 alpha 才隨影像改變",
    "cost": "成本與能力對照：CAM 一次前向就能算、但需要 GAP 架構；Grad-CAM 每個類別要一次反向，幾乎任何 CNN 都能用",
}

CAPTIONS = {
    "formula": "同一個式子，只差在那 K 個數字是「學來的」還是「當場算的」。",
    "per-image": "實測：純 GAP + Linear 時 α 與影像無關（等於 w/(H·W)）；加了 ReLU 之後 α 才隨影像變。",
    "cost": "能力換成本：Grad-CAM 通用，但每解釋一個類別就要一次反向傳播。",
}


def svg(slug, w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'role="img" aria-label="%s">%s<rect x="0.75" y="0.75" width="%s" '
            'height="%s" rx="16" fill="%s" stroke="#222b36" stroke-width="1.5"/>%s</svg>'
            % (w, h, esc(ARIA[slug]), DEFS, w - 1.5, h - 1.5, BG, body))


def fig_formula():
    body = [text(40, 44, "同一個式子，只差那 K 個數字", 20, INK, "700"),
            text(40, 72, "兩者都是「加權疊加特徵圖，再 ReLU」；差別在權重怎麼來", 13, DIM)]
    body.append(rect(30, 96, 450, 210, stroke=TEAL + "77", sw=1.4, fill=CELL, rx=12,
                     opacity=0.6))
    body.append(text(50, 124, "原始 CAM", 13, TEAL, "700"))
    body.append(text(50, 156, "L = ReLU( Σ_k  w[k, c] · A_k )", 13, INK, "700"))
    body.append(text(50, 186, "w[k, c]：Linear(K → C) 的權重", 11.5, DIM))
    body.append(text(50, 210, "訓練時學好、存在模型裡", 11.5, DIM))
    body.append(text(50, 240, "前提：最後一層卷積後面接 GAP", 11.5, ROSE))
    body.append(text(50, 272, "→ 一次前向 + 查表就能畫", 11.5, DIM))

    body.append(rect(520, 96, 450, 210, stroke=VIOLET + "77", sw=1.4, fill=CELL, rx=12,
                     opacity=0.6))
    body.append(text(540, 124, "Grad-CAM", 13, VIOLET, "700"))
    body.append(text(540, 156, "L = ReLU( Σ_k  α[k, c] · A_k )", 13, INK, "700"))
    body.append(text(540, 186, "α[k, c] = mean( ∂yᶜ / ∂A_k )", 11.5, DIM))
    body.append(text(540, 210, "推論時對這張影像算出來的", 11.5, DIM))
    body.append(text(540, 240, "前提：只要該層能反向傳播", 11.5, TEAL))
    body.append(text(540, 272, "→ 每個類別多一次反向", 11.5, DIM))

    body.append('<path d="M 480 200 L 512 200" stroke="%s" stroke-width="1.6" '
                'marker-end="url(#arcg)"/>' % DIM)
    body.append(text(496, 190, "換", 10, DIM, "normal", "middle"))
    body.append(text(40, 344, "一句話：CAM 的權重是「模型的常識」，Grad-CAM 的權重是"
                               "「這張圖的即時判斷」。", 12, DIM))
    return svg("formula", 1000, 380, "".join(body))


def fig_per_image():
    body = [text(40, 44, "α 真的「隨影像改變」嗎？實測", 20, INK, "700"),
            text(40, 72, "同一組分類權重，換一張影像，權重會變嗎？答案取決於中間有沒有非線性",
                 13, DIM)]
    # w (fixed)
    body.append(rect(40, 96, 250, 120, stroke=TEAL + "88", sw=1.4, fill=CELL, rx=10))
    body.append(text(56, 120, "分類層權重 w（固定）", 11, TEAL, "700"))
    body.append(text(56, 148, "w[1, 狗] = 1.20", 11.5, INK))
    body.append(text(56, 172, "w[2, 狗] = −0.50", 11.5, INK))
    body.append(text(56, 196, "w[3, 狗] = 0.80", 11.5, INK))
    body.append(arrow(296, 156, 336, 156))
    # two images
    body.append(rect(340, 96, 210, 120, stroke=BLUE + "88", sw=1.4, fill=CELL, rx=10))
    body.append(text(356, 120, "影像 A", 11, BLUE, "700"))
    body.append(text(356, 148, "α = [0.019, −0.018, 0.025]", 10.5, INK))
    body.append(text(356, 176, "（純 GAP 時：0.075 / −0.031 / 0.05）", 9.5, DIM))
    body.append(text(356, 200, "4×4 → H·W = 16", 9.5, DIM))
    body.append(rect(340, 232, 210, 120, stroke=VIOLET + "88", sw=1.4, fill=CELL, rx=10))
    body.append(text(356, 256, "影像 B", 11, VIOLET, "700"))
    body.append(text(356, 284, "α = [0.038, −0.014, 0.031]", 10.5, INK))
    body.append(text(356, 312, "（純 GAP 時：同一組數字）", 9.5, DIM))
    body.append(text(356, 336, "α 只在這裡不同", 9.5, DIM))
    body.append(rect(580, 96, 390, 256, stroke=AMBER + "77", sw=1.4, fill=CELL, rx=12))
    body.append(text(600, 122, "兩種情況要分清楚", 12, AMBER, "700"))
    body.append(text(600, 152, "① 純 GAP + Linear（沒有中間層）", 11.5, INK))
    body.append(text(616, 176, "α = w / (H·W) → 每張圖都一樣", 11, DIM))
    body.append(text(616, 198, "這時 Grad-CAM 就等於 CAM", 11, DIM))
    body.append(text(600, 232, "② 中間有 ReLU（真實網路）", 11.5, INK))
    body.append(text(616, 256, "∂y/∂A = w/(H·W) · 1[A > 0]", 11, DIM))
    body.append(text(616, 278, "正值比例隨影像變 → α 也變", 11, DIM))
    body.append(text(616, 300, "影像 A 的正值比例 0.25 / 0.56 / 0.50", 10, DIM))
    body.append(text(616, 320, "影像 B 的正值比例 0.50 / 0.44 / 0.62", 10, DIM))
    body.append(text(40, 400, "所以「Grad-CAM 的權重隨影像改變」這句話要加條件："
                               "在 CAM 適用的那種純線性末端上，它其實不變。", 12, DIM))
    return svg("per-image", 1000, 430, "".join(body))


def fig_cost():
    rows = [("Conv → GAP → Linear", "可以", "可以", TEAL),
            ("Conv → Flatten → FC", "不行", "可以", ROSE),
            ("Conv → 1×1 conv → GAP → Linear", "不行", "可以", ROSE),
            ("ResNet / DenseNet（線性頭）", "要看頭", "可以", AMBER)]
    body = [text(40, 44, "能力與成本：換到什麼", 20, INK, "700"),
            text(40, 72, "同一張熱圖，CAM 便宜但挑架構；Grad-CAM 通用但要多做反向", 13, DIM)]
    body.append(text(60, 108, "架構", 11, DIM))
    body.append(text(520, 108, "CAM", 11, DIM))
    body.append(text(700, 108, "Grad-CAM", 11, DIM))
    for i, (arch, cam, gc, colour) in enumerate(rows):
        y = 140 + i * 42
        body.append(text(60, y, arch, 11.5, INK))
        body.append(text(520, y, cam, 11.5, colour if cam == "不行" else TEAL, "700"))
        body.append(text(700, y, gc, 11.5, TEAL, "700"))
    body.append(rect(40, 320, 920, 84, stroke=BLUE + "55", fill="#1c2230", rx=12))
    body.append(text(60, 348, "成本：CAM = 1 次前向 + 查表；Grad-CAM = 1 次前向 + 每個類別 1 次反向。",
                     12, INK))
    body.append(text(60, 374, "1000 類全部畫一輪 = 1,000 次反向，所以實務上只挑 1–3 個類別看。",
                     11.5, DIM))
    body.append(text(40, 420, "這也是 Grad-CAM 常被拿來做除錯而不是即時監控的原因。", 12, DIM))
    return svg("cost", 1000, 450, "".join(body))


FIGS = {"formula": fig_formula, "per-image": fig_per_image, "cost": fig_cost}


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

