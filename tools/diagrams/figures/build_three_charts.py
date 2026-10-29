# -*- coding: utf-8 -*-
"""Three quantitative tables -> hand-drawn SVG charts.

    python build_three_charts.py

  generalization-notes  §8.2  max_depth 驗證曲線
  orange-ai-notes       分類模型 14 個  CA / AUC
  automl-unit2-extra    §10.3 手肘法 + 輪廓係數（取代原本的 JPEG 插圖）

Markdown stays the source of truth: the figure block is inserted into both the
.md and the paired index.html, guarded by `<!-- FIGURE:<slug> -->` markers so a
second run replaces instead of duplicating.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from svglib import Svg, C, TXT, MUT  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SRC = os.path.join(REPO, "source")

TEAL, AMBER, ROSE, GREEN = C["teal"], C["amber"], C["rose"], C["green"]


# ---- small chart primitives (svglib has boxes/arrows, not series) ------------
def polyline(s, pts, colour, width=2.4):
    d = "M " + " L ".join("%.1f %.1f" % (x, y) for x, y in pts)
    s.p.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s" '
               'stroke-linejoin="round" stroke-linecap="round"/>' % (d, colour, width))
    for a, b in zip(pts, pts[1:]):
        s.segs.append((a[0], a[1], b[0], b[1]))


def dot(s, x, y, colour, r=4.5):
    s.p.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, r, colour))


def grid(s, x1, y1, x2, y2, colour="#30363d", opacity=0.45):
    """Grid line that is NOT registered as a connector (keeps check() focused)."""
    s.p.append('<path d="M %s %s L %s %s" fill="none" stroke="%s" '
               'stroke-width="1" opacity="%s"/>' % (x1, y1, x2, y2, colour, opacity))
# ---- 1. generalization: validation curve ------------------------------------
def fig_validation(s):
    depths = ["1", "2", "3", "5", "8", "12", "不限"]
    train = [0.9290, 0.9513, 0.9742, 0.9947, 1.0000, 1.0000, 1.0000]
    val = [0.9015, 0.9248, 0.9202, 0.9273, 0.9250, 0.9250, 0.9250]

    left, right, top, bottom = 118, 842, 140, 392
    lo, hi = 0.88, 1.005

    def x(i):
        return 152 + i * 108

    def y(v):
        return bottom - (v - lo) / (hi - lo) * (bottom - top)

    s.text(48, 112, "分數", 11.5, MUT)
    for t in (0.90, 0.925, 0.95, 0.975, 1.00):
        grid(s, left, y(t), right, y(t))
        s.text(left - 10, y(t) + 4, "%.3f" % t, 11.5, MUT, anchor="end")
    s.line(left, bottom, right, bottom, "#7d8590", 1.2)
    for i, d in enumerate(depths):
        s.text(x(i), bottom + 22, d, 12, MUT, anchor="middle")
    s.text(left, bottom + 38, "max_depth", 12.5, MUT)

    # best-validation marker
    s.p.append('<path d="M %s %s L %s %s" fill="none" stroke="%s" stroke-width="1.4" '
               'stroke-dasharray="5 4" opacity="0.85"/>'
               % (x(3), top - 6, x(3), bottom, GREEN))

    polyline(s, [(x(i), y(v)) for i, v in enumerate(train)], TEAL)
    polyline(s, [(x(i), y(v)) for i, v in enumerate(val)], AMBER)
    for i in range(len(depths)):
        dot(s, x(i), y(train[i]), TEAL)
        dot(s, x(i), y(val[i]), AMBER)

    s.text(x(3) + 10, y(0.9273) - 14, "驗證最佳 0.9273（depth=5）", 12, GREEN, "700")
    s.text(x(4) + 10, y(1.0) + 20, "訓練滿分 1.0000", 11.5, TEAL)
    s.text(x(4) + 10, y(0.9250) + 26, "驗證停在 0.9250", 11.5, AMBER)

    dot(s, 640, 112, TEAL, 5)
    s.text(654, 116, "訓練分數", 12, MUT)
    dot(s, 754, 112, AMBER, 5)
    s.text(768, 116, "驗證分數", 12, MUT)

    s.text(48, 452, "depth 1→5 兩條線一起上升；5→8 之後訓練滿分、驗證反而下滑"
                    "——教科書級的過擬合指紋。", 12.5, MUT)

# ---- 2. orange-ai: CA bars + AUC dots ---------------------------------------
def fig_models(s):
    rows = [
        ("kNN", 0.9667, 0.9869), ("Logistic Regression", 0.9667, 0.9977),
        ("Stacking", 0.9667, 0.9970), ("Calibrated Learner", 0.9600, 0.9968),
        ("SVM", 0.9600, 0.9700), ("AdaBoost", 0.9600, 0.9783),
        ("Gradient Boosting", 0.9533, 0.9890), ("Neural Network", 0.9533, 0.9965),
        ("Tree", 0.9467, 0.9613), ("Random Forest", 0.9467, 0.9954),
        ("CN2 Rule Induction", 0.8933, 0.9551), ("Naive Bayes", 0.8733, 0.9813),
        ("SGD", 0.8333, 0.8750), ("Constant（基準線）", 0.3333, 0.5000),
    ]
    left, right, top = 252, 812, 156
    bottom = top + len(rows) * 32

    def x(v):
        return left + v * (right - left)

    s.p.append('<rect x="620" y="102" width="26" height="12" rx="3" fill="%s"/>' % TEAL)
    s.text(654, 112, "CA（長條）", 12, MUT)
    dot(s, 764, 108, AMBER, 5)
    s.text(776, 112, "AUC（圓點）", 12, MUT)

    for v in (0.0, 0.25, 0.50, 0.75, 1.00):
        grid(s, x(v), top - 10, x(v), bottom)
        s.text(x(v), bottom + 22, "%.2f" % v, 11.5, MUT, anchor="middle")

    for i, (name, ca, auc) in enumerate(rows):
        cy = top + 12 + i * 32
        base = i == len(rows) - 1
        col = ROSE if base else TEAL
        s.p.append('<rect x="%s" y="%s" width="%.1f" height="18" rx="4" fill="%s" '
                   'opacity="0.85"/>' % (left, cy - 9, ca * (right - left), col))
        s.text(left - 12, cy + 4, name, 12, TXT, "700" if base else "normal", "end")
        s.text(x(ca) - 8, cy + 4, "%.4f" % ca, 11.5, "#08141a", "700", "end")
        dot(s, x(auc), cy, AMBER, 4.5)

    s.text(left, bottom + 46,
           "Constant 就是「永遠猜最多數類別」：CA = 50/150 = 0.3333、AUC = 0.5；"
           "任何模型都要先贏過它。", 12.5, MUT)


# ---- 3. automl-unit2: elbow + silhouette ------------------------------------
def fig_elbow(s):
    ks = list(range(1, 11))
    inertia = [19652.395, 9051.816, 1773.737, 203.891, 184.407,
               165.716, 148.074, 129.730, 117.922, 104.542]
    sil_ks = list(range(2, 11))
    sil = [0.6155, 0.7993, 0.8756, 0.7552, 0.6102, 0.4540, 0.3411, 0.3379, 0.3592]

    top, bottom = 168, 400

    # panel 1 -- inertia
    lx, lr = 88, 438

    def x1(k):
        return lx + (k - 1) / 9.0 * (lr - lx)

    def y1(v):
        return bottom - v / 20000.0 * (bottom - top)

    s.text(lx, 146, "① inertia（WCSS）：找轉折點", 13, TXT, "700")
    for t in (0, 5000, 10000, 15000, 20000):
        grid(s, lx, y1(t), lr, y1(t))
        s.text(lx - 8, y1(t) + 4, "%s" % format(t, ","), 10.5, MUT, anchor="end")
    s.line(lx, bottom, lr, bottom, "#7d8590", 1.2)
    for k in ks:
        s.text(x1(k), bottom + 20, str(k), 11, MUT, anchor="middle")
    s.text((lx + lr) / 2, bottom + 44, "K", 12, MUT, anchor="middle")
    polyline(s, [(x1(k), y1(v)) for k, v in zip(ks, inertia)], TEAL)
    for k, v in zip(ks, inertia):
        dot(s, x1(k), y1(v), TEAL, 4)

    s.p.append('<path d="M %s %s L %s %s" fill="none" stroke="%s" stroke-width="1.4" '
               'stroke-dasharray="5 4" opacity="0.85"/>'
               % (x1(4), top - 4, x1(4), bottom, GREEN))
    s.text(x1(4) - 6, top + 12, "手肘 K=4", 11.5, GREEN, "700", "end")
    s.text(248, 340, "K=4→5 降幅 1569.9 → 19.5", 12, AMBER, "700")

    # panel 2 -- silhouette
    rx, rr = 546, 856

    def x2(k):
        return rx + (k - 2) / 8.0 * (rr - rx)

    def y2(v):
        return bottom - (v - 0.30) / 0.65 * (bottom - top)

    s.text(rx, 146, "② silhouette：越高越好", 13, TXT, "700")
    for t in (0.40, 0.60, 0.80):
        grid(s, rx, y2(t), rr, y2(t))
        s.text(rx - 8, y2(t) + 4, "%.2f" % t, 10.5, MUT, anchor="end")
    s.line(rx, bottom, rr, bottom, "#7d8590", 1.2)
    for k in sil_ks:
        s.text(x2(k), bottom + 20, str(k), 11, MUT, anchor="middle")
    s.text((rx + rr) / 2, bottom + 44, "K", 12, MUT, anchor="middle")
    polyline(s, [(x2(k), y2(v)) for k, v in zip(sil_ks, sil)], AMBER)
    for k, v in zip(sil_ks, sil):
        dot(s, x2(k), y2(v), AMBER, 4)

    s.p.append('<path d="M %s %s L %s %s" fill="none" stroke="%s" stroke-width="1.4" '
               'stroke-dasharray="5 4" opacity="0.85"/>'
               % (x2(4), top - 4, x2(4), bottom, GREEN))
    s.text(x2(4) + 8, y2(0.8756) - 12, "最高 0.8756", 11.5, GREEN, "700")

    s.text(48, 470, "兩個方法一致指向 K = 4：inertia 的降幅在 K=4→5 之間從 1569.9 崩到 "
                    "19.5（手肘），輪廓係數也在 K=4 達到最高。", 12.5, MUT)


# ---- chart registry ---------------------------------------------------------
CHARTS = [
    dict(slug="generalization-validation", w=900, h=470,
         aria="決策樹 max_depth 的驗證曲線：訓練分數與驗證分數",
         title="驗證曲線：max_depth 的甜點區", sub="乳癌資料集，5 折交叉驗證",
         fn=fig_validation,
         caption="圖 12：<strong>驗證曲線</strong>——depth 1→5 兩條線一起上升；"
                 "depth 8 之後訓練滿分 1.0000、驗證反而停在 0.9250，是過擬合的指紋。"
                 "｜手繪 SVG 圖表",
         md_anchor="**這張表就是「架構控制」的實證**",
         html_anchor="<p><strong>這張表就是「架構控制」的實證</strong>",
         files=["generalization-notes/Generalization_Study_Notes.md",
                "generalization-notes/index.html"]),

    dict(slug="orange-models-ca-auc", w=900, h=665,
         aria="iris 14 個分類模型的 CA 與 AUC 比較（含 Constant 基準線）",
         title="14 個分類模型：CA 長條、AUC 圓點", sub="iris 交叉驗證，random_state=42",
         fn=fig_models,
         caption="圖 28：<strong>14 個分類模型的 CA / AUC</strong>——最右邊的 Constant "
                 "（0.3333 / 0.5000）是基準線；CA 同分時看 AUC，"
                 "Logistic Regression 的 AUC 最高。｜手繪 SVG 圖表",
         md_anchor="> ⚠️ **可重現性說明**",
         html_anchor="<p>⚠️ <strong>可重現性說明</strong>",
         files=["orange-ai-notes/Orange_AI_Study_Notes.md",
                "orange-ai-notes/index.html"]),

    dict(slug="ch10-elbow-silhouette", w=900, h=500,
         aria="手肘法與輪廓係數：inertia 與 silhouette 隨 K 的變化，最佳 K=4",
         title="手肘法 + 輪廓係數：兩個方法一起指到 K=4",
         sub="300 點、真實 4 群、cluster_std=0.60",
         fn=fig_elbow,
         caption="圖 10：<strong>手肘法與輪廓係數</strong>——inertia 的降幅在 K=4→5 "
                 "之間從 1569.9 崩到 19.5（手肘），輪廓係數也在 K=4 達到最高 0.8756。"
                 "｜手繪 SVG 圖表",
         md_anchor="<!-- FIGURE:ch10-elbow-silhouette -->",
         html_anchor="<!-- FIGURE:ch10-elbow-silhouette -->",
         files=["automl-unit2-extra-notes/AutoML_Unit2_Extra_Study_Notes.md",
                "automl-unit2-extra-notes/index.html"]),
]


def upsert(path, block, slug, anchor):
    t = io.open(path, encoding="utf-8").read().replace("\r\n", "\n")
    open_m = "<!-- FIGURE:%s -->" % slug
    close_m = "<!-- /FIGURE:%s -->" % slug

    if open_m in t and close_m in t:
        t = re.sub(re.escape(open_m) + r".*?" + re.escape(close_m),
                   lambda m: block, t, count=1, flags=re.S)
    elif slug == "ch10-elbow-silhouette" and open_m in t:
        # legacy block: <!-- FIGURE:... --> ... <!-- /FIGURE -->  (base64 JPEG)
        pat = re.escape(open_m) + r".*?" + re.escape("<!-- /FIGURE -->")
        t, n = re.subn(pat, lambda m: block, t, count=1, flags=re.S)
        if n != 1:
            raise SystemExit("legacy figure block not replaced in " + path)
    else:
        if anchor not in t:
            raise SystemExit("anchor not found in %s: %r" % (path, anchor[:40]))
        t = t.replace(anchor, block + "\n\n" + anchor, 1)

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
                   ch["md_anchor"] if rel.endswith(".md") else ch["html_anchor"])
        print("wrote %-30s %dx%d  collisions=%d"
              % (ch["slug"] + ".svg", ch["w"], ch["h"], len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))


if __name__ == "__main__":
    main()


