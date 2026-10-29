# -*- coding: utf-8 -*-
"""Batch 2: five more quantitative tables -> hand-drawn SVG charts.

    python build_batch2_charts.py

  generalization-notes §2.3  degree 的 RMSE 光譜（U 形）
  generalization-notes §7.4  alpha 的 RMSE（正則化過頭）
  ml-models-notes      §10.5 決策樹設定：訓練 vs 測試
  ml-models-notes      §8.4  校準指標（Brier / LogLoss / ECE）
  h2o-automl-notes     §3.7  Leaderboard 前 5 名
  tpot-notes           §3.2  組合數：相乘不是相加

Idempotent: same `<!-- FIGURE:<slug> -->` guard as build_three_charts.py.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from svglib import Svg, C, TXT, MUT  # noqa: E402
from build_three_charts import polyline, dot, grid  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SRC = os.path.join(REPO, "source")

TEAL, AMBER, ROSE, GREEN, BLUE, VIOLET = (C["teal"], C["amber"], C["rose"],
                                          C["green"], C["blue"], C["violet"])


def bar(s, x, y, w, h, colour, rx=4, opacity=0.86):
    s.p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" '
               'fill="%s" opacity="%s"/>' % (x, y, w, h, rx, colour, opacity))


def fig_degree(s):
    degrees = ["1", "2", "3", "5", "9", "15"]
    train = [4.111, 1.580, 1.560, 1.448, 1.394, 1.907]
    test = [4.565, 2.005, 2.025, 2.231, 2.179, 5.131]

    left, right, top, bottom = 118, 846, 140, 380

    def x(i):
        return 150 + i * 122

    def y(v):
        return bottom - v / 5.5 * (bottom - top)

    for t in (0, 1, 2, 3, 4, 5):
        grid(s, left, y(t), right, y(t))
        s.text(left - 10, y(t) + 4, "%d" % t, 11.5, MUT, anchor="end")
    s.line(left, bottom, right, bottom, "#7d8590", 1.2)
    for i, d in enumerate(degrees):
        s.text(x(i), bottom + 22, d, 12, MUT, anchor="middle")
    s.text(left, bottom + 44, "degree", 12.5, MUT)
    s.text(48, 112, "RMSE", 11.5, MUT)

    s.p.append('<path d="M %s %s L %s %s" fill="none" stroke="%s" stroke-width="1.4" '
               'stroke-dasharray="5 4" opacity="0.85"/>'
               % (x(1), top - 6, x(1), bottom, GREEN))
    s.text(x(1) + 12, y(2.005) - 18, "甜點區 degree=2（測試 2.005）", 12, GREEN, "700")

    polyline(s, [(x(i), y(v)) for i, v in enumerate(train)], TEAL)
    polyline(s, [(x(i), y(v)) for i, v in enumerate(test)], AMBER)
    for i in range(len(degrees)):
        dot(s, x(i), y(train[i]), TEAL)
        dot(s, x(i), y(test[i]), AMBER)

    s.text(x(5) + 6, y(5.131) + 6, "5.131", 12, AMBER, "700")
    s.text(x(2) + 6, y(1.560) + 18, "訓練 1.560", 11.5, TEAL)

    dot(s, 650, 112, TEAL, 5)
    s.text(664, 116, "訓練 RMSE", 12, MUT)
    dot(s, 770, 112, AMBER, 5)
    s.text(784, 116, "測試 RMSE", 12, MUT)
    s.text(48, 440, "測試誤差是 U 形：degree 2 最低（2.005），再往上就爬升；"
                    "degree 15 訓練誤差反而變大、測試爆到 5.131。", 12.5, MUT)


def fig_alpha(s):
    labels = ["0", "1e-4", "0.01", "1", "100", "10000"]
    train = [1.907, 1.166, 1.167, 1.262, 1.647, 2.202]
    test = [5.131, 9.216, 8.796, 7.872, 2.546, 3.995]

    left, right, top, bottom = 118, 846, 140, 380

    def x(i):
        return 150 + i * 122

    def y(v):
        return bottom - v / 10.0 * (bottom - top)

    for t in (0, 2, 4, 6, 8, 10):
        grid(s, left, y(t), right, y(t))
        s.text(left - 10, y(t) + 4, "%d" % t, 11.5, MUT, anchor="end")
    s.line(left, bottom, right, bottom, "#7d8590", 1.2)
    for i, d in enumerate(labels):
        s.text(x(i), bottom + 22, d, 12, MUT, anchor="middle")
    s.text(left, bottom + 44, "alpha（L2 強度）", 12.5, MUT)
    s.text(48, 112, "RMSE", 11.5, MUT)

    s.p.append('<path d="M %s %s L %s %s" fill="none" stroke="%s" stroke-width="1.4" '
               'stroke-dasharray="5 4" opacity="0.85"/>'
               % (x(4), top - 6, x(4), bottom, GREEN))
    s.text(x(4) + 12, y(2.546) - 44, "alpha=100（測試 2.546）", 12, GREEN, "700")

    polyline(s, [(x(i), y(v)) for i, v in enumerate(train)], TEAL)
    polyline(s, [(x(i), y(v)) for i, v in enumerate(test)], AMBER)
    for i in range(len(labels)):
        dot(s, x(i), y(train[i]), TEAL)
        dot(s, x(i), y(test[i]), AMBER)

    s.text(x(1) + 8, y(9.216) - 12, "9.216", 12, AMBER, "700")

    dot(s, 650, 112, TEAL, 5)
    s.text(664, 116, "訓練 RMSE", 12, MUT)
    dot(s, 770, 112, AMBER, 5)
    s.text(784, 116, "測試 RMSE", 12, MUT)
    s.text(48, 440, "alpha 不是越大或越小越好：太小幾乎沒作用（9.216）、"
                    "100 最好（2.546），開到 10000 連訓練誤差都上升＝欠擬合。", 12.5, MUT)


def fig_trees(s):
    names = ["gini", "entropy", "depth=1", "depth=3", "depth=5", "None"]
    train = [1.0000, 1.0000, 0.9271, 0.9799, 0.9950, 1.0000]
    test = [0.9181, 0.9474, 0.9123, 0.9240, 0.9298, 0.9181]

    left, right, top, bottom = 118, 846, 142, 372
    lo, hi = 0.90, 1.005

    def x(i):
        return 172 + i * 118

    def y(v):
        return bottom - (v - lo) / (hi - lo) * (bottom - top)

    for t in (0.90, 0.925, 0.95, 0.975, 1.00):
        grid(s, left, y(t), right, y(t))
        s.text(left - 10, y(t) + 4, "%.3f" % t, 11.5, MUT, anchor="end")
    s.line(left, bottom, right, bottom, "#7d8590", 1.2)
    for i, n in enumerate(names):
        s.text(x(i), bottom + 22, n, 11.5, MUT, anchor="middle")

    for i in range(len(names)):
        bar(s, x(i) - 26, y(train[i]), 24, bottom - y(train[i]), TEAL)
        bar(s, x(i) + 2, y(test[i]), 24, bottom - y(test[i]), AMBER)
        s.text(x(i) + 14, y(test[i]) - 8, "%.4f" % test[i], 10, AMBER, "700", "middle")

    s.text(48, 112, "準確率", 11.5, MUT)
    bar(s, 640, 100, 12, 12, TEAL, 3)
    s.text(660, 111, "訓練", 12, MUT)
    bar(s, 720, 100, 12, 12, AMBER, 3)
    s.text(740, 111, "測試", 12, MUT)

    s.text(48, 412, "depth=1 兩邊都低（0.9271／0.9123）＝欠擬合；gini 與 None 訓練 1.0000、"
                    "測試 0.9181＝過擬合。", 12.5, MUT)


def fig_calibration(s):
    models = ["SVC+Platt", "RF", "RF+校準"]
    colours = [TEAL, AMBER, ROSE]
    panels = [
        ("Brier ↓", [0.0658, 0.0359, 0.0399], 0.08, (0.00, 0.04, 0.08)),
        ("LogLoss ↓", [0.2206, 0.1184, 0.1351], 0.26, (0.00, 0.13, 0.26)),
        ("ECE ↓", [0.0557, 0.0545, 0.0738], 0.10, (0.00, 0.05, 0.10)),
    ]
    top, bottom = 168, 330
    xs = [100, 360, 620]
    pw = 230

    for (title, vals, vmax, ticks), x0 in zip(panels, xs):
        s.text(x0, 146, title, 13, TXT, "700")
        for t in ticks:
            gy = bottom - t / vmax * (bottom - top)
            grid(s, x0, gy, x0 + pw, gy)
            s.text(x0 - 8, gy + 4, ("%.2f" % t), 10.5, MUT, anchor="end")
        for k, v in enumerate(vals):
            bx = x0 + 44 + k * 62
            bh = v / vmax * (bottom - top)
            bar(s, bx, bottom - bh, 40, bh, colours[k])
            s.text(bx + 20, bottom - bh - 8, "%.4f" % v, 10.5, colours[k], "700", "middle")
        s.p.append('<path d="M %s %s L %s %s" fill="none" stroke="#7d8590" '
                   'stroke-width="1.2"/>' % (x0, bottom, x0 + pw, bottom))
        for k, m in enumerate(models):
            s.text(x0 + 64 + k * 62, bottom + 20, m, 10.5, MUT, anchor="middle")

    for k, m in enumerate(models):
        bar(s, 70 + k * 130, 98, 12, 12, colours[k], 3)
        s.text(90 + k * 130, 109, m, 12, MUT)

    s.text(48, 372, "AUC 0.9696／0.9923／0.9921、準確率 0.9181／0.9415／0.9415："
                    "校準只改「分數→機率」，不改排序，也不是無腦加分項。", 12.5, MUT)



def fig_leaderboard(s):
    rows = [("SE BestOfFamily_6", 1.4468, 1.0084), ("SE BestOfFamily_7", 1.4488, 0.9986),
            ("SE BestOfFamily_4", 1.4505, 1.0072), ("GBM_grid_77", 1.4647, 1.0196),
            ("GBM_grid_49", 1.4718, 1.0443)]
    left, right, top, step = 268, 790, 152, 40
    lo, hi = 1.444, 1.474

    def x(v):
        return left + (v - lo) / (hi - lo) * (right - left)

    s.text(left, 130, "rmse（越小越好，排序依據）", 11.5, MUT)
    s.text(812, 130, "mae", 11.5, MUT)

    for v in (1.445, 1.455, 1.465):
        grid(s, x(v), top - 14, x(v), top + len(rows) * step - 12)
        s.text(x(v), top + len(rows) * step + 8, "%.3f" % v, 10.5, MUT, anchor="middle")

    for i, (name, rmse, mae) in enumerate(rows):
        cy = top + i * step
        bar(s, left, cy - 10, x(rmse) - left, 20, TEAL if i else AMBER)
        s.text(left - 12, cy + 4, name, 11.5, TXT, "700" if i == 0 else "normal", "end")
        s.text(x(rmse) + 8, cy + 4, "%.4f" % rmse, 11, AMBER)
        s.text(812, cy + 4, "%.4f" % mae, 11, MUT)

    s.text(48, 392, "前 5 名的 rmse 只差 0.025（1.4468→1.4718），但 mae 幾乎並列"
                    "（0.9986–1.0443）：排序看 rmse，別把差距讀成碾壓。", 12.5, MUT)


def fig_combos(s):
    rows = [("RandomForest（27×3）", 81), ("SVC（27×3）", 81),
            ("KNN（12×3）", 36), ("DecisionTree（27×3）", 81)]
    left, right, top, step = 300, 760, 150, 44
    vmax = 90

    def x(v):
        return left + v / vmax * (right - left)

    for v in (0, 30, 60, 90):
        grid(s, x(v), top - 14, x(v), top + len(rows) * step - 16)
        s.text(x(v), top + len(rows) * step + 6, str(v), 10.5, MUT, anchor="middle")

    for i, (name, n) in enumerate(rows):
        cy = top + i * step
        bar(s, left, cy - 12, x(n) - left, 24, TEAL if n > 36 else AMBER)
        s.text(left - 12, cy + 4, name, 11.5, TXT, "normal", "end")
        s.text(x(n) + 10, cy + 4, "%d 種" % n, 11.5, TEAL if n > 36 else AMBER, "700")

    s.text(left, top + len(rows) * step + 34, "合計 279 種", 16, ROSE, "700")
    s.text(left + 130, top + len(rows) * step + 34,
           "＝ 27×3 + 27×3 + 12×3 + 27×3", 11.5, MUT)
    s.text(48, 392, "多一個維度是相乘不是相加：超參數 27 種 × 前處理 3 種 = 81；"
                    "四個模型加起來 279 種，而且這還只是玩具級。", 12.5, MUT)



CHARTS = [
    dict(slug="generalization-degree", w=900, h=470,
         aria="多項式 degree 的 RMSE 光譜：訓練與測試誤差",
         title="複雜度光譜：測試誤差是 U 形", sub="30 筆訓練、2000 筆新資料",
         fn=fig_degree,
         caption="圖 13：<strong>degree 的 RMSE 光譜</strong>——測試誤差在 degree=2 最低"
                 "（2.005），degree 15 訓練誤差反而上升到 1.907、測試爆到 5.131。"
                 "｜手繪 SVG 圖表",
         md_anchor="兩個關鍵讀法：",
         html_anchor="<p>兩個關鍵讀法：</p>",
         files=["generalization-notes/Generalization_Study_Notes.md",
                "generalization-notes/index.html"]),

    dict(slug="generalization-alpha", w=900, h=470,
         aria="L2 正則化 alpha 的 RMSE：訓練與測試誤差",
         title="L2 的 alpha：太小沒作用、太大欠擬合", sub="degree=15 多項式，乳癌資料集",
         fn=fig_alpha,
         caption="圖 14：<strong>alpha 的 RMSE</strong>——太小幾乎沒作用（測試 9.216）、"
                 "alpha=100 最好（2.546），開到 10000 連訓練誤差都上升＝正則化過度。"
                 "｜手繪 SVG 圖表",
         md_anchor="**這張表有兩個考點**",
         html_anchor="<p><strong>這張表有兩個考點</strong>",
         files=["generalization-notes/Generalization_Study_Notes.md",
                "generalization-notes/index.html"]),

    dict(slug="ml-trees-settings", w=900, h=430,
         aria="決策樹六種設定的訓練與測試準確率",
         title="決策樹設定：訓練 vs 測試", sub="breast_cancer，單次切分",
         fn=fig_trees,
         caption="圖 26：<strong>決策樹六種設定</strong>——depth=1 兩邊都低（欠擬合）；"
                 "gini 與 None 訓練 1.0000、測試 0.9181（過擬合）；entropy 的 0.9474 "
                 "屬單次切分波動。｜手繪 SVG 圖表",
         md_anchor="> **考點**：① Gini 與熵",
         html_anchor="① Gini 與熵", html_blockquote=True,
         files=["ml-models-notes/ML_Models_Study_Notes.md",
                "ml-models-notes/index.html"]),

    dict(slug="ml-calibration", w=900, h=400,
         aria="三個模型的校準指標：Brier、LogLoss、ECE",
         title="校準指標：三個模型比一比", sub="breast_cancer；三項都是越小越好",
         fn=fig_calibration,
         caption="圖 27：<strong>校準指標</strong>——隨機森林本來就校準得不錯，再校準反而"
                 "讓 Brier（0.0359→0.0399）與 ECE（0.0545→0.0738）變差；AUC 幾乎不變。"
                 "｜手繪 SVG 圖表",
         md_anchor="> ⚠️ **反直覺結果**",
         html_anchor="反直覺結果", html_blockquote=True,
         files=["ml-models-notes/ML_Models_Study_Notes.md",
                "ml-models-notes/index.html"]),

    dict(slug="h2o-leaderboard", w=900, h=415,
         aria="H2O AutoML Leaderboard 前五名的 rmse 與 mae",
         title="Leaderboard 前 5 名：rmse 差距只有 0.025",
         sub="AutoML 依 rmse 由小到大排序，第一名＝最佳",
         fn=fig_leaderboard,
         caption="圖 10：<strong>Leaderboard 前 5 名</strong>——rmse 從 1.4468 到 1.4718，"
                 "差距只有 0.025；mae 幾乎並列（0.9986–1.0443），別把排序讀成碾壓。"
                 "｜手繪 SVG 圖表",
         md_anchor="**怎麼讀 `model_id`？**",
         html_anchor="<p><strong>怎麼讀 <code>model_id</code>？</strong></p>",
         files=["h2o-automl-notes/H2O_AutoML_Study_Notes.md",
                "h2o-automl-notes/index.html"]),

    dict(slug="tpot-combos", w=900, h=410,
         aria="TPOT 搜尋空間：四種演算法的組合數與合計 279 種",
         title="組合數：相乘不是相加", sub="4 種演算法 × 3 種前處理 × 各 3 個超參數",
         fn=fig_combos,
         caption="圖 20：<strong>組合數</strong>——超參數 27 種 × 前處理 3 種 = 81，"
                 "四個模型合計 279 種；再多一個維度就是再乘一次。｜手繪 SVG 圖表",
         md_anchor="而且這還只是",
         html_anchor="<p>而且這還只是",
         files=["tpot-notes/TPOT_Study_Notes.md", "tpot-notes/index.html"]),
]


def upsert(path, block, slug, anchor, blockquote=False):
    t = io.open(path, encoding="utf-8").read().replace("\r\n", "\n")
    open_m = "<!-- FIGURE:%s -->" % slug
    close_m = "<!-- /FIGURE:%s -->" % slug

    if open_m in t and close_m in t:
        t = re.sub(re.escape(open_m) + r".*?" + re.escape(close_m),
                   lambda m: block, t, count=1, flags=re.S)
    else:
        if anchor not in t:
            raise SystemExit("anchor not found in %s: %r" % (path, anchor[:40]))
        idx = t.index(anchor)
        if blockquote:
            bq = t.rfind("<blockquote>", 0, idx)
            if bq < 0:
                raise SystemExit("no <blockquote> before anchor in " + path)
            idx = bq
        t = t[:idx] + block + "\n\n" + t[idx:]

    io.open(path, "w", encoding="utf-8", newline="\r\n").write(t)


def main():
    for ch in CHARTS:
        s = Svg(ch["w"], ch["h"], ch["aria"], ch["title"], ch["sub"])
        ch["fn"](s)
        bad = s.check()
        s.save(os.path.join(HERE, ch["slug"] + ".svg"),
               os.path.join(HERE, "_m_" + ch["slug"] + ".html"))
        block = s.figure(ch["caption"], marker="FIGURE:" + ch["slug"])
        for rel in ch["files"]:
            path = os.path.join(SRC, rel.replace("/", os.sep))
            upsert(path, block, ch["slug"],
                   ch["md_anchor"] if rel.endswith(".md") else ch["html_anchor"],
                   blockquote=ch.get("html_blockquote", False) and rel.endswith(".html"))
        print("wrote %-30s %dx%d  collisions=%d"
              % (ch["slug"] + ".svg", ch["w"], ch["h"], len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))


if __name__ == "__main__":
    main()


