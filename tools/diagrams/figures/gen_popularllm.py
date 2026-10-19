# -*- coding: utf-8 -*-
"""popular-llm-notes: 7 ASCII blocks -> SVG.

  art#1  §14.1 聚合 App（一個介面、多個模型）
  art#2  §22.1 四層同心圓 AI ⊃ ML ⊃ DL ⊃ Generative AI
  art#3  §24.1 GAN：Generator / Discriminator 與梯度回傳
  art#4  §25.2 Diffusion 的 Forward（加噪）與 Reverse（去噪）
  art#5  §27.1 混合式：預測式 AI + 生成式 AI 接力
  art#6  §31.2 黃漆褪色題的時間軸
  art#7  §B.3 本機 torchaudio 問題的根因鏈（呼叫堆疊）
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


def fig_aggregator(s):
    s.box(300, 116, 300, 62, "聚合 App", "單一介面", "teal", tsize=16)
    s.bus_out((450, 178), [(200, 234), (450, 234), (700, 234)])
    for x, name, stage in ((110, "GPT", "blue"), (360, "Gemini", "violet"),
                           (610, "Claude", "amber")):
        s.box(x, 234, 180, 62, name, None, stage, tsize=15)
    s.text(830, 272, "…", 20, MUT, "700", "middle")
    s.text(48, 342, "一個介面、多個模型：使用者不必分別訂閱 ChatGPT／Gemini／Claude，"
                    "而是透過第三方 App 依需求切換。", 13, MUT)


def fig_nested(s):
    layers = [
        (60, 110, 780, 384, "Artificial Intelligence", "teal"),
        (120, 170, 660, 300, "Machine Learning", "blue"),
        (180, 230, 540, 216, "Deep Learning", "violet"),
        (240, 290, 420, 132, "Generative AI", "rose"),
    ]
    for x, y, w, h, label, stage in layers:
        s.rect(x, y, w, h, fill="none", stroke=C[stage] + "99", rx=16, sw=1.5)
        s.text(x + 26, y + 36, label, 15.5, C[stage], "700")
    s.text(450, 372, "創造新內容", 17, TXT, "700", "middle")
    s.text(48, 524, "每一個都包含在下一個裡面：生成式 AI 是 AI 的一種，"
                    "但「AI 就是生成式 AI」是錯的。", 13, MUT)


def fig_gan(s):
    s.box(200, 116, 220, 56, "隨機雜訊 z", None, "teal", tsize=14)
    s.arrow(310, 172, 310, 212)
    s.box(200, 214, 220, 64, "Generator", "神經網路 1", "blue")
    s.arrow(310, 278, 310, 316)
    s.text(322, 302, "假資料", 11.5, MUT)
    s.box(200, 318, 220, 64, "Discriminator", "神經網路 2", "violet")
    s.box(620, 318, 220, 64, "真資料 x", None, "amber", tsize=14)
    s.arrow(616, 350, 424, 350)

    s.line(310, 382, 310, 428, RAIL, 2)
    s.line(310, 428, 100, 428, RAIL, 2)
    s.line(100, 428, 100, 246, RAIL, 2)
    s.arrow(100, 246, 196, 246, RAIL)
    s.text(322, 400, "真 / 假", 11.5, MUT)
    s.text(110, 452, "梯度：回頭更新 Generator 的權重", 11.5, MUT)

    s.text(48, 508, "生成器的輸出直接接判別器的輸入，所以梯度可以一路回傳到生成器——"
                    "這就是 GAN 的對抗訓練。", 13, MUT)



def fig_diffusion(s):
    rows = [
        (140, "Forward：加噪", "teal", ["清晰圖片", "半雜訊", "純雜訊"], "加噪",
         "（訓練時，這一步是「已知」的數學過程）"),
        (250, "Reverse：去噪", "violet", ["純雜訊", "半雜訊", "生成的圖片"], "去噪",
         "（這一步是「模型要學」的部分）"),
    ]
    for top, label, stage, boxes, arrow, note in rows:
        cy = top + 28
        s.text(48, cy + 5, label, 13.5, C[stage], "700")
        for i, txt in enumerate(boxes):
            x = 230 + i * 240
            s.box(x, top, 180, 56, txt, None, stage, tsize=13.5)
            if i < len(boxes) - 1:
                s.arrow(x + 186, cy, x + 234, cy, RAIL)
                s.text(x + 210, cy - 10, arrow, 11.5, MUT, "normal", "middle")
        s.text(230, top + 78, note, 11.5, MUT)
    s.text(48, 372, "考點：Forward 是加噪、Reverse 是去噪，順序不能顛倒；"
                    "而且只有 Reverse 需要訓練。", 13, MUT)


def fig_hybrid(s):
    s.box(350, 116, 200, 54, "歷史資料", None, "teal", tsize=14)
    s.arrow(450, 170, 450, 204)
    s.box(300, 206, 300, 64, "Predictive AI", "預測：會發生什麼？", "blue")
    s.arrow(450, 270, 450, 304)
    s.text(462, 292, "預測結果", 11.5, MUT)
    s.box(300, 306, 300, 64, "Generative AI", "創造：該說什麼、該產出什麼？", "violet")
    s.arrow(450, 370, 450, 404)
    s.text(462, 392, "個人化內容 / 說明 / 建議", 11.5, MUT)
    s.box(350, 406, 200, 54, "決策者", None, "green", tsize=14)
    s.text(48, 508, "預測式 AI 先回答「會發生什麼」，生成式 AI 再回答「該說什麼」——"
                    "兩者接力，才構成混合式系統。", 13, MUT)


def fig_timeline(s):
    cols = [(160, 200), (380, 200), (600, 260)]
    s.rect(48, 130, 812, 46, fill=CARD2, stroke="#30363d", rx=10)
    s.text(93, 159, "房間", 13, MUT, "700", "middle")
    for (x, w), head in zip(cols, ("現在", "1 年後", "2 年後")):
        s.text(x + w / 2, 159, head, 13.5, TXT, "700", "middle")

    rows = [
        ("藍", [("藍", TXT), ("黃（漆成黃）", C["amber"]), ("白 ✅（自動褪色）", C["green"])]),
        ("黃", [("黃", C["amber"]), ("白 ✅", C["green"]), ("白 ✅（不用動）", C["green"])]),
        ("白", [("白", TXT), ("白 ✅", C["green"]), ("白 ✅", C["green"])]),
    ]
    for i, (name, cells) in enumerate(rows):
        y = 184 + i * 58
        s.rect(48, y, 812, 52, fill=CARD2, stroke="#222b36", rx=10)
        s.text(93, y + 32, name, 14, TXT, "700", "middle")
        for (x, w), (txt, colour) in zip(cols, cells):
            s.text(x + w / 2, y + 32, txt, 12.5, colour, "normal", "middle")

    s.text(48, 390, "黃漆一年會自己褪成白——所以「藍先漆成黃」比「直接漆白」更快達成目標，"
                    "這題要的正是這條推理鏈。", 13, MUT)


def fig_cuda_chain(s):
    rows = [
        ("transformers 5.17.0", "teal"),
        ("modeling_layers.py", "blue"),
        ("processing_utils.py", "blue"),
        ("audio_utils.py:58　import torchaudio　← 寫死在這裡", "violet"),
        ("torchaudio/_extension/utils.py", "amber"),
        ("_check_cuda_version()　→　RuntimeError", "rose"),
    ]
    for i, (txt, stage) in enumerate(rows):
        x = 48 + 48 * i
        y = 150 + i * 46
        if i:
            s.line(x - 24, y - 34, x - 24, y - 8, "#30363d", 1.5)
            s.line(x - 24, y - 8, x - 4, y - 8, "#30363d", 1.5)
        s.text(x, y, txt, 12.5, C[stage], "700", "start", MONO)
    s.text(48, 452, "越下層越接近真正的原因：audio_utils.py 的 import 先失敗，"
                    "上面幾層只是被拖垮的受害者。", 13, MUT)


FIGS = [
    ("popularllm-aggregator", "popular-llm-notes", 1, 900, 380,
     "聚合 App：一個介面、多個模型", "使用者不必分別訂閱每一家", fig_aggregator,
     "圖 34：聚合 App——單一介面往下接 GPT／Gemini／Claude 等多個模型，"
     "使用者依需求切換。｜手繪 SVG 圖表"),
    ("popularllm-nested", "popular-llm-notes", 2, 900, 560,
     "四層同心圓：AI ⊃ ML ⊃ DL ⊃ 生成式 AI", "每一個都包含在下一個裡面", fig_nested,
     "圖 35：四層同心圓——Artificial Intelligence ⊃ Machine Learning ⊃ Deep Learning ⊃ "
     "Generative AI，最內圈才是「創造新內容」。｜手繪 SVG 圖表"),
    ("popularllm-gan", "popular-llm-notes", 3, 900, 540,
     "GAN：兩個網路怎麼接起來", "生成器造假、判別器抓假，梯度回頭更新生成器", fig_gan,
     "圖 36：GAN 的資料流——隨機雜訊 z 進 Generator 產生假資料，與真資料 x 一起進 "
     "Discriminator；判別結果的梯度回頭更新 Generator 的權重。｜手繪 SVG 圖表"),
    ("popularllm-diffusion", "popular-llm-notes", 4, 900, 400,
     "Diffusion：Forward 加噪、Reverse 去噪", "只有 Reverse 需要訓練", fig_diffusion,
     "圖 37：Diffusion 的兩個過程——Forward 把清晰圖片逐步加噪成純雜訊（已知的數學過程），"
     "Reverse 再一步步去噪生成圖片（模型要學的部分）。｜手繪 SVG 圖表"),
    ("popularllm-hybrid", "popular-llm-notes", 5, 900, 540,
     "混合式：預測式 ＋ 生成式", "先預測會發生什麼，再生成該說什麼", fig_hybrid,
     "圖 38：混合式系統——歷史資料先過 Predictive AI（預測會發生什麼），"
     "預測結果再交給 Generative AI（生成該說什麼），最後交給決策者。｜手繪 SVG 圖表"),
    ("popularllm-timeline", "popular-llm-notes", 6, 900, 430,
     "黃漆褪色題的時間軸", "藍→黃→白、黃→白、白→白", fig_timeline,
     "圖 39：時間軸——藍房間漆成黃一年後自動褪成白；黃房間放著就變白；白房間始終是白，"
     "所以「漆成黃色」是對的。｜手繪 SVG 圖表"),
    ("popularllm-cuda-chain", "popular-llm-notes", 7, 900, 480,
     "torchaudio 問題的根因鏈", "由下往上看，才知道是誰把誰拖垮", fig_cuda_chain,
     "圖 40：根因鏈——transformers 經 modeling_layers／processing_utils 匯入 audio_utils，"
     "在第 58 行寫死 import torchaudio，最後在 _check_cuda_version() 爆 RuntimeError。"
     "｜手繪 SVG 圖表"),
]

if __name__ == "__main__":
    for slug, note, art, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-30s %-20s art#%d %dx%d  %s"
              % (slug + ".svg", note, art, w, h,
                 "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))
