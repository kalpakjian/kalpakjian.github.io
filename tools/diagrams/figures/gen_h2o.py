# -*- coding: utf-8 -*-
"""h2o-automl-notes: 3 ASCII blocks -> SVG.

  art#1  全流程一覽：官網 -> 終端機 -> 瀏覽器 -> Flow x3 -> 編輯器 -> Excel -> 收工
  art#2  §3.7 model_id 的解剖（演算法／第幾名／專案／時間戳）
  art#3  §4.3 模型存放路徑的解剖（目錄／模型名稱）
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from svglib import Svg, C, MUT, TXT, CARD2, MONO  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAIL = "#7d8590"

STEPS = [
    ("官網", "teal", [
        "H2O.ai 官網 → 向下捲動點擊「Start Using H2O AutoML」",
        "→ latest stable release page → Download H2O",
    ]),
    ("終端機", "blue", [
        "cd ~/Downloads → unzip h2o-3.46.0.11.zip → cd h2o-3.46.0.11 → java -jar h2o.jar",
        "※ 只支援 Java 8–17；Java 23 要加 -Dsys.ai.h2o.debug.allowJavaVersions=23",
        "※ 這個終端機視窗不能關，只能最小化（它正在跑 WebUI 的後台伺服器）",
    ]),
    ("瀏覽器", "violet", [
        "http://localhost:54321　→　H2O Flow Web UI（p.8）",
    ]),
    ("Flow", "amber", [
        "Data ▼ → Import Files → 貼上路徑 → 搜尋 → ＋ → Import",
        "→ Parse these files → Ticker 改 Enum → Parse → 得到 monthly_training_set.hex",
    ]),
    ("Flow", "amber", [
        "Model ▼ → Run AutoML → training_frame / response_column",
        "→ ignored_columns: Date → max_runtime_secs: 300 → 取消兩個 CV 勾選 → Build Model → View",
    ]),
    ("Flow", "amber", [
        "Leaderboard（依 rmse 排序，第一個＝最佳）→ 點第一個模型",
        "→ Model ▼ → Export Model → 填路徑 → Export",
    ]),
    ("Cursor / VSCode", "green", [
        "建 venv → pip install h2o pandas → 貼上 prompt 生成 stock_prediction.py",
        "→ 把 model_path 填成剛剛匯出的路徑 → 執行程式",
    ]),
    ("Excel", "rose", [
        "開啟 trend_2024_2027.csv → Insert → Pivot Chart",
        "→ Legend: Ticker / Axis: Date / Values: predict_Close → Change Chart Type → Line",
    ]),
    ("收工", "gray", [
        "Flow 的 Admin ▼ → Shut Down，或在終端機按 Ctrl + C（p.38）",
    ]),
]

MODEL_ID = [("StackedEnsemble_BestOfFamily", "演算法", "teal"),
            ("_6", "第 6 名", "blue"),
            ("_AutoML_1", "專案名", "amber"),
            ("_20260707_121423", "時間戳", "violet")]

MODEL_PATH = [("/Users/xxxx/xxxx/xxxx", "模型存放路徑", "violet"),
              ("/best_model", "模型名稱", "green")]


def fig_walkthrough(s):
    y = 106
    prev = None
    for i, (tool, stage, lines) in enumerate(STEPS, 1):
        h = 56 + len(lines) * 20
        if prev is not None:
            s.arrow(80, prev, 80, y - 2, RAIL)
        s.rect(48, y, 904, h, fill=CARD2, stroke=C[stage] + "66", rx=12)
        s.badge(80, y + 30, str(i), C[stage], r=15, size=13)
        s.text(108, y + 35, tool, 14.5, C[stage], "700")
        for j, ln in enumerate(lines):
            s.text(108, y + 62 + j * 20, ln, 11.5, MUT)
        prev = y + h
        y = prev + 16

    s.text(48, 1134, "從下載到出圖一條龍：官網 → 終端機 → 瀏覽器 → Flow（匯入／訓練／匯出）"
                      "→ 編輯器 → Excel → 收工。", 13, MUT)


def chips(s, y, items, h=46, adv=8.0, pad=30, gap=12, cx=500, mono=13):
    """A row of monospace chips with a leader line + label under each."""
    widths = [len(t) * adv + pad for t, _, _ in items]
    total = sum(widths) + gap * (len(items) - 1)
    x = cx - total / 2.0
    for (txt, label, stage), w in zip(items, widths):
        s.rect(x, y, w, h, fill="#0d1117", stroke=C[stage] + "99", rx=10)
        s.text(x + w / 2, y + h / 2 + 4.5, txt, mono, C[stage], "700", "middle", MONO)
        s.line(x + w / 2, y + h, x + w / 2, y + h + 20, "#30363d", 1.5)
        s.text(x + w / 2, y + h + 42, label, 13.5, TXT, "700", "middle")
        x += w + gap


def fig_model_id(s):
    s.text(450, 126, "StackedEnsemble_BestOfFamily_6_AutoML_1_20260707_121423",
           13, TXT, "700", "middle", MONO)
    chips(s, 160, MODEL_ID)
    s.text(48, 302, "名字＝演算法＿第幾名＿AutoML 專案＿訓練時間戳；"
                    "從最後一段時間戳可以看出這個模型是何時訓練的。", 12, MUT)


def fig_model_path(s):
    s.text(450, 126, "/Users/xxxx/xxxx/xxxx/best_model", 13, TXT, "700", "middle", MONO)
    chips(s, 160, MODEL_PATH)
    s.text(48, 296, "前面的目錄必須先自己建好（否則匯出失敗）；最後一段是自己取的模型名稱，"
                    "匯出後會變成一個資料夾。", 12, MUT)


FIGS = [
    ("h2o-walkthrough", "h2o-automl-notes", 1, 1000, 1160,
     "H2O AutoML：從下載到出圖的一條龍", "九個站點，每一步都有明確產出", fig_walkthrough,
     "圖 7：全流程一覽——官網下載 → 終端機啟動 h2o.jar → 瀏覽器開 Flow → 匯入／訓練／匯出，"
     "再到編輯器寫預測程式、Excel 畫走勢圖、收工關伺服器。｜手繪 SVG 圖表"),
    ("h2o-model-id", "h2o-automl-notes", 2, 900, 350,
     "model_id 怎麼讀", "Leaderboard 上的名字就是一份履歷", fig_model_id,
     "圖 8：model_id 的解剖——演算法（StackedEnsemble_BestOfFamily）＋第 6 名＋AutoML 專案名"
     "＋訓練時間戳。｜手繪 SVG 圖表"),
    ("h2o-model-path", "h2o-automl-notes", 3, 900, 320,
     "模型存放路徑怎麼讀", "哪一段是目錄、哪一段是模型名稱", fig_model_path,
     "圖 9：模型存放路徑的解剖——前面的目錄要自己先建好，最後一段是自己取的模型名稱"
     "（匯出後是一個資料夾）。｜手繪 SVG 圖表"),
]

if __name__ == "__main__":
    for slug, note, art, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-30s %-18s art#%d %dx%d  %s"
              % (slug + ".svg", note, art, w, h,
                 "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))
