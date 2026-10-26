# -*- coding: utf-8 -*-
"""tpot-notes: 8 張內嵌 SVG 圖表（4 個 ASCII 圖區塊 → SVG，另加 4 張新圖）。

  art#1  §0    30 秒總複習流程      → tpot-flow
  art#2  §4.3  TPOT 六步工作流程    → tpot-workflow
  art#3  §5.5  樹狀管線（分叉再合併）→ tpot-tree-pipeline
  art#4  附錄B.4 0.x → 1.1.0 對照   → tpot-api-diff
  新圖   §3    排列組合爆炸（本機實算 279/465/744）→ tpot-combo-explosion
  新圖   §5    基因演算法四步驟循環  → tpot-genetic-loop
  新圖   §9    Colab 五步流程        → tpot-colab-steps
  新圖   §9.8  本機實測結果（贏家詛咒）→ tpot-measured-results

輸出：
  tools/diagrams/figures/<slug>.svg          （入版控，與其他筆記一致）
  tools/diagrams/figures/_m_<slug>.html      （量測用，gitignored）
  _work/tpot/svg/<slug>.figure.html          （build_notes.py 內嵌用的 <figure> 區塊）
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # 同層（figures/）
sys.path.insert(0, os.path.dirname(_HERE))    # 上層（svglib.py）
from svglib import Svg, C, MUT, TXT, CARD2, MONO, LINE  # noqa: E402

HERE = _HERE
FIGDIR = r"C:\Users\princ\blog\_work\tpot\svg"
RAIL = "#7d8590"


def note(s, x, y, t, size=12.5, fill=MUT, anchor="start"):
    s.text(x, y, t, size, fill, "normal", anchor)


def chip_row(s, x0, y, w, h, items, stages, gap=14, tsize=12.5):
    """一排等寬小卡（用於把四個步驟／三個零件並排）。"""
    for i, (label, stage) in enumerate(zip(items, stages)):
        cx = x0 + i * (w + gap)
        s.box(cx, y, w, h, label, None, stage, tsize=tsize)
        if i:
            s.arrow(cx - gap + 1, y + h / 2, cx - 3, y + h / 2, RAIL, 1.6)


# --------------------------------------------------------------------- 1
def fig_flow(s):
    """§0：30 秒總複習的完整流程（取代原本 17 行 ASCII 圖）。"""
    s.box(240, 108, 420, 52, "資料 + 答案", "X 特徵（150×4）＋ y 標籤（3 類）", "blue")
    s.arrow(450, 160, 450, 186)
    note(s, 468, 180, "train_test_split(random_state=42)")
    s.box(240, 188, 420, 52, "訓練集 / 測試集", "112 筆 ／ 38 筆（留一份當期末考）", "teal")

    s.arrow(450, 240, 450, 266)
    note(s, 468, 260, "TPOTClassifier(...)：設定預算與指標")
    s.rect(150, 268, 600, 104, fill=CARD2, stroke=C["violet"] + "66", rx=12)
    s.text(174, 296, "基因演算法（四個步驟循環）", 14, C["violet"], "700")
    chip_row(s, 170, 310, 128, 44, ["初始族群", "適者生存", "交配與突變", "迭代"],
             ["teal", "blue", "violet", "amber"])

    s.arrow(450, 372, 450, 398)
    note(s, 468, 392, ".fit(X_train, y_train)：開始演化搜尋")
    s.box(240, 400, 420, 52, "最佳管線 fitted_pipeline_",
          "本機實測：邏輯迴歸 ＋ 前處理（不是隨機森林）", "amber", dsize=11.5)
    s.arrow(450, 452, 450, 478)
    note(s, 468, 472, "accuracy_score(y_test, tpot.predict(X_test))")
    s.box(240, 480, 420, 52, "準確率 0.9474（36/38）", "內部 CV 0.9822 → 贏家詛咒", "green")
    note(s, 48, 570, "本機實測：5 代 × 20 族群 ≈ 100 條管線，約 51 秒跑完。", 13)


# --------------------------------------------------------------------- 2
def fig_workflow(s):
    """§4.3：TPOT 六步工作流程，右欄標出「誰負責」（取代 12 行 ASCII 圖）。"""
    steps = [
        ("你準備資料（清理、編碼、切分）", "TPOT 只吃乾淨的數值矩陣", "blue", "TPOT 不幫你"),
        ("train_test_split → X_train / X_test", "留一份沒看過的當期末考", "blue", "你決定"),
        ("TPOTClassifier(...) 設定預算與指標", "generations、population_size、scorers、cv", "violet", "TPOT 幫你"),
        (".fit(X_train, y_train) 開始搜尋", "基因演算法：約 100 條管線輪流上場", "violet", "TPOT 幫你"),
        ("最佳管線 fitted_pipeline_", "前處理 ＋ 特徵選擇 ＋ 模型 ＋ 參數", "amber", "TPOT 幫你"),
        ("打分數與部署", "accuracy_score(...) ／ joblib.dump(...)", "green", "你決定"),
    ]
    note(s, 750, 100, "誰負責", 12.5)
    for i, (title, detail, stage, owner) in enumerate(steps):
        y = 106 + i * 68
        s.card(110, y, 620, 54, title, detail, stage, num=str(i + 1))
        note(s, 750, y + 32, owner, 12.5)
        if i < len(steps) - 1:
            s.arrow(420, y + 54, 420, y + 68 - 2)
    note(s, 48, 536, "TPOT 只負責「找模型」這一段；定義問題、清理資料、選指標、判讀結果仍然是人的工作。", 13)


# --------------------------------------------------------------------- 3
def fig_combo(s):
    """§3：排列組合爆炸（左：乘法；右：本機實算的組合數）。"""
    note(s, 48, 120, "組合數是「相乘」成長的", 13)
    s.box(60, 140, 240, 44, "4 種演算法", None, "blue", tsize=13)
    s.text(150, 196, "×", 18, MUT, "700", "middle")
    s.box(60, 206, 240, 44, "3 種前處理", None, "teal", tsize=13)
    s.text(150, 262, "×", 18, MUT, "700", "middle")
    s.box(60, 272, 240, 44, "3 個超參數", None, "violet", tsize=13)
    s.arrow(150, 316, 150, 340)
    s.box(60, 342, 240, 58, "279 種組合", "本機實算（僅 4 個模型）", "amber", tsize=17)
    note(s, 60, 424, "再多一種前處理 → 465 種", 12)

    note(s, 430, 120, "組合數（前處理種類越多，組合數越大）", 13)
    s.line(415, 400, 862, 400, RAIL, 1.5)
    s.text(408, 340, "組合數", 11.5, MUT, "normal", "end")
    bars = [("1 種", 93, "blue"), ("3 種", 279, "teal"),
            ("5 種", 465, "violet"), ("8 種", 744, "rose")]
    for i, (label, val, stage) in enumerate(bars):
        x = 430 + i * 110
        h = val * 200.0 / 744
        s.rect(x, 400 - h, 90, h, fill=CARD2, stroke=C[stage] + "66", rx=6)
        s.text(x + 45, 400 - h - 10, str(val), 12.5, TXT, "700", "middle")
        s.text(x + 45, 424, label, 11.5, MUT, "normal", "middle")
    note(s, 48, 470, "GridSearchCV 18 條管線 × 5 折 = 90 次 fit → 3.94 秒；"
                     "要覆蓋 279 種組合約 61 秒（本機實測推估）。", 13)


# --------------------------------------------------------------------- 4
def fig_genetic_loop(s):
    """§5：基因演算法四步驟（環狀）。"""
    s.box(110, 110, 300, 62, "① 初始族群", "隨機生成一批模型（population_size）", "teal")
    s.box(490, 110, 300, 62, "② 適者生存", "用 CV 分數淘汰差的（scorers ＋ cv）", "blue")
    s.box(490, 300, 300, 62, "③ 交配與突變", "結合好的、隨機微調（0.2 ／ 0.7）", "violet")
    s.box(110, 300, 300, 62, "④ 不斷迭代", "繁衍 5 代 → 冠軍模型（generations）", "amber")

    s.arrow(412, 141, 486, 141)
    s.arrow(640, 174, 640, 296)
    s.arrow(488, 331, 414, 331)
    s.arrow(260, 298, 260, 176)
    s.text(450, 240, "每一代都在「繁衍 + 淘汰」", 13, MUT, "normal", "middle")
    note(s, 48, 420, "本機實測：5 代 × 20 族群 ≈ 100 條管線、約 51 秒；"
                     "預算越大通常分數越好（但不保證）。", 13)


# --------------------------------------------------------------------- 5
def fig_tree(s):
    """§5.5：樹狀管線（分叉再合併）——取代 2 行 ASCII 圖。"""
    s.box(300, 108, 300, 50, "原始特徵", "150 筆 × 4 欄", "gray")
    s.bus_out((450, 158), [(240, 232), (450, 232), (660, 232)], RAIL, 24)
    for x, label, stage in ((150, "StandardScaler", "blue"),
                            (360, "MinMaxScaler", "teal"),
                            (570, "Normalizer", "violet")):
        s.box(x, 232, 180, 48, label, None, stage, tsize=12.5)
    s.bus_in([(240, 280), (450, 280), (660, 280)], (450, 356), RAIL, 24)
    s.box(240, 356, 420, 52, "FeatureUnion", "把多條支線的特徵併在一起", "amber", dsize=11.5)
    s.arrow(450, 408, 450, 434)
    s.box(280, 436, 340, 52, "SelectPercentile", "percentile ≈ 87%", "teal", dsize=11.5)
    s.arrow(450, 488, 450, 514)
    s.box(240, 516, 420, 52, "LogisticRegression", "C ≈ 27020 · penalty=elasticnet · solver=saga",
          "green", dsize=11.5)
    note(s, 48, 606, "TPOT 允許「分叉再合併」，這就是它叫「樹狀」的原因；本機實測的最佳管線正是這條。", 13)


# --------------------------------------------------------------------- 6
def fig_colab(s):
    """§9：Colab 五步流程。"""
    steps = [
        ("開啟 Google Colab 並新增筆記本",
         "colab.research.google.com → 新增筆記本（New Notebook）", "blue"),
        ("安裝 TPOT 工具包",
         "!pip install tpot（驚嘆號＝作業系統指令；約 10～20 秒）", "teal"),
        ("建立程式碼區塊（Cell）",
         "點「+ 程式碼 (+ Code)」開一個空白儲存格", "violet"),
        ("貼上五段程式",
         "匯入套件 → 切分資料 → 設定參數 → fit → 打分數", "amber"),
        ("執行並檢視成果",
         "Shift + Enter → 進度條 Generation 5/5 → 印出準確率", "green"),
    ]
    for i, (title, detail, stage) in enumerate(steps):
        y = 106 + i * 76
        s.card(110, y, 620, 60, title, detail, stage, num=str(i + 1))
        if i < len(steps) - 1:
            s.arrow(420, y + 60, 420, y + 76 - 2)
    note(s, 48, 520, "課堂上大約要等 2～3 分鐘；本機（processes=False）實測 5 代 × 20 族群約 51 秒。", 13)


# --------------------------------------------------------------------- 7
def fig_results(s):
    """§9.8：本機實測結果（贏家詛咒 + 測試集大小 + 搜尋時間）。"""
    note(s, 48, 120, "① 內部 CV 分數 vs 測試集分數", 13)
    s.text(60, 152, "內部交叉驗證最佳（在約 100 條裡挑最好的）", 12, MUT)
    s.rect(60, 160, 236, 26, fill=CARD2, stroke=C["teal"] + "66", rx=6)
    s.text(306, 180, "0.9822", 13, TXT, "700")
    s.text(60, 218, "測試集實際分數（沒看過的 38 筆）", 12, MUT)
    s.rect(60, 226, 227, 26, fill=CARD2, stroke=C["green"] + "66", rx=6)
    s.text(297, 246, "0.9474", 13, TXT, "700")
    s.text(60, 286, "差距 0.0348 → 贏家詛咒", 12.5, C["rose"], "700")

    note(s, 480, 120, "② 測試集只有 38 筆：錯 1 筆就掉 2.6%", 13)
    for i in range(38):
        col, row = i % 19, i // 19
        x, y = 480 + col * 18, 152 + row * 20
        last = (i == 37)
        s.rect(x, y, 15, 15, fill=C["rose"] + "55" if last else CARD2,
               stroke=C["rose"] if last else LINE, rx=3, sw=1.2)
    s.text(480, 216, "每一格 = 1 筆；錯 1 筆 = 1 ÷ 38 ≈ 2.6%", 12, MUT)

    note(s, 48, 340, "③ 搜尋時間：約 51 秒（多次實測 45.6～51.7 秒）", 13)
    s.rect(48, 356, 300, 22, fill=CARD2, stroke=C["amber"] + "66", rx=6)
    s.text(360, 373, "5 代 × 20 族群 ≈ 100 條管線", 12, MUT)
    note(s, 48, 470, "課堂簡報的 0.973 與本機 0.9474 只差一題——不要把單一分數當成絕對值。", 13)


# --------------------------------------------------------------------- 8
def fig_api_diff(s):
    """附錄 B.4：0.x 教學文 → 1.1.0 的六行改寫（取代 8 行 ASCII 圖）。"""
    s.box(70, 108, 330, 44, "0.x 教學文寫的", None, "rose", tsize=14)
    s.box(500, 108, 340, 44, "TPOT 1.1.0 要改成", None, "green", tsize=14)
    rows = [
        ("verbosity=2", "verbose=2"),
        ("config_dict='Default'", "search_space='linear'"),
        ("tpot.export('pipeline.py')", "joblib.dump(tpot.fitted_pipeline_, ...)"),
        ("tpot.score(X_test, y_test)", "accuracy_score(y_test, tpot.predict(X_test))"),
        ("tpot._fitted_pipeline", "tpot.fitted_pipeline_"),
        ("TPOTClassifier()", "TPOTClassifier(processes=False, generations=5)"),
    ]
    for i, (left, right) in enumerate(rows):
        y = 170 + i * 70
        s.rect(70, y, 330, 52, fill=CARD2, stroke=C["rose"] + "55", rx=8)
        s.rect(500, y, 340, 52, fill=CARD2, stroke=C["green"] + "55", rx=8)
        s.text(82, y + 32, left, 11.5, TXT, "normal", "start", MONO)
        s.text(512, y + 32, right, 11.5, TXT, "normal", "start", MONO)
        s.arrow(408, y + 26, 492, y + 26)
    note(s, 48, 600, "每一列都是本機實際跑出來的結果；完整 traceback 收在附錄 B.2。", 13)


# --------------------------------------------------------------------- 9
def fig_racetrack_roles(s):
    """§6.4：用比喻記住 TPOT 的定位（取代 4 行 ASCII 樹狀圖）。

    這一張補的是「三個角色分工」——圖 6 畫的是賽車場景、6.1／6.2 是對照表，
    都沒有把「你負責什麼／它負責什麼／它交付什麼」講成結構。
    """
    s.box(190, 106, 520, 56, "TPOT = 賽車改裝的自動化實驗室", None, "amber", tsize=17)

    roles = [
        ("你負責", "人類", ["零件箱：sklearn 可用的元件", "賽道：訓練資料"], "blue"),
        ("它負責", "TPOT", ["不斷試組合、測秒數", "淘汰慢的、繁衍快的"], "teal"),
        ("它交付", "成果", ["一台調到最好的車（管線）", "改裝清單（節點與參數）"], "green"),
    ]
    w, gap, y, h = 244, 36, 232, 132
    xs = [48 + i * (w + gap) for i in range(3)]
    for i, (title, who, lines, st) in enumerate(roles):
        x = xs[i]
        s.rect(x, y, w, h, fill=CARD2, stroke=C[st] + "66", rx=12)
        s.badge(x + 30, y + 30, who, C[st], r=15, size=12)
        s.text(x + 54, y + 35, title, 15.5, TXT, "700")
        s.line(x + 18, y + 54, x + w - 18, y + 54, RAIL, 1.2)
        for j, ln in enumerate(lines):
            s.text(x + 18, y + 80 + j * 24, ln, 12.5, MUT)

    # 根 → 三個角色
    s.line(450, 162, 450, 198, RAIL, 1.5)
    s.line(xs[0] + w / 2, 198, xs[2] + w / 2, 198, RAIL, 1.5)
    for x in xs:
        s.arrow(x + w / 2, 198, x + w / 2, y - 4, RAIL)

    note(s, 48, 396, "比喻的關鍵字是「自動試組合」與「附上改裝清單」。", 13)
    note(s, 48, 418, "考試若問「TPOT 幫你省下什麼」：省下人工嘗試組合的時間，"
                     "而不是省下「理解問題」的功夫。", 12.5)


FIGS = [
    ("tpot-flow", 1, 900, 600, "TPOT 完整流程：30 秒總複習",
     "從資料到準確率，中間那格就是基因演算法", fig_flow,
     "圖 11：TPOT 完整流程——資料 → 切分 → 設定預算 → 演化搜尋（基因演算法四步驟循環）"
     "→ 最佳管線 → 打分數。本機實測約 51 秒、準確率 0.9474。｜手繪 SVG 圖表"),
    ("tpot-workflow", 2, 900, 560, "TPOT 六步工作流程：誰負責哪一段",
     "右欄標出「TPOT 幫你／你決定」", fig_workflow,
     "圖 12：TPOT 六步工作流程——TPOT 只負責「找模型」（第 3～5 步），準備資料、切分、"
     "打分數與部署仍由人負責。｜手繪 SVG 圖表"),
    ("tpot-combo-explosion", 3, 900, 520, "排列組合爆炸：為什麼人工調參不可能窮舉",
     "4 演算法 × 3 前處理 × 3 參數 = 279 種（本機實算）", fig_combo,
     "圖 13：組合數是相乘成長的——本機實算 279 種組合；前處理增加到 8 種就變 744 種。"
     "GridSearchCV 只跑 18 條管線就要 3.94 秒。｜手繪 SVG 圖表"),
    ("tpot-genetic-loop", 4, 900, 480, "基因演算法：四個步驟的循環",
     "初始族群 → 適者生存 → 交配與突變 → 不斷迭代", fig_genetic_loop,
     "圖 14：基因演算法四步驟——每一代都在繁衍與淘汰，最後留下冠軍模型；"
     "預算越大通常分數越好。｜手繪 SVG 圖表"),
    ("tpot-tree-pipeline", 5, 900, 640, "樹狀管線：分叉再合併",
     "為什麼它叫 Tree-based Pipeline", fig_tree,
     "圖 15：樹狀管線示意——多條前處理支線經 FeatureUnion 合併後再進模型；"
     "本機實測的最佳管線正是這條。｜手繪 SVG 圖表"),
    ("tpot-colab-steps", 6, 900, 560, "Colab 五步流程",
     "從開筆記本到印出準確率", fig_colab,
     "圖 16：Colab 實作五步——開筆記本 → !pip install tpot → 開程式碼區塊 → 貼五段程式"
     "→ Shift+Enter 執行並看進度條。｜手繪 SVG 圖表"),
    ("tpot-measured-results", 7, 900, 520, "本機實測結果：贏家詛咒與測試集大小",
     "內部 CV 0.9822 vs 測試集 0.9474", fig_results,
     "圖 17：本機實測——內部交叉驗證 0.9822 比測試集 0.9474 樂觀（贏家詛咒）；"
     "測試集只有 38 筆，錯 1 筆就差 2.6%。｜手繪 SVG 圖表"),
    ("tpot-api-diff", 8, 900, 640, "0.x 教學文 → TPOT 1.1.0：六行改寫對照",
     "每一列都是本機實際跑出來的結果", fig_api_diff,
     "圖 18：API 對照——verbosity→verbose、score()→accuracy_score、export()→joblib "
     "等六處改寫；左欄寫法在 1.1.0 會直接報錯。｜手繪 SVG 圖表"),
    ("tpot-racetrack-roles", 9, 900, 440, "TPOT 的三個角色分工",
     "你給零件箱與賽道，它負責試車與篩選", fig_racetrack_roles,
     "圖 19：TPOT 的三個角色——你負責給它零件箱（sklearn 可用的元件）與賽道（訓練資料），"
     "TPOT 負責不斷試組合、測秒數、淘汰慢的並繁衍快的，最後交付一台調到最好的車（管線）"
     "與改裝清單（節點與參數）。｜手繪 SVG 圖表"),
]

if __name__ == "__main__":
    os.makedirs(FIGDIR, exist_ok=True)
    for slug, art, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        io.open(os.path.join(FIGDIR, slug + ".figure.html"), "w",
                encoding="utf-8", newline="\n").write(s.figure(cap, "SVGFIG"))
        print("wrote %-30s art#%-2s %dx%d  %s"
              % (slug + ".svg", art, w, h,
                 "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))


