# -*- coding: utf-8 -*-
"""local-gpu-ml-notes：cuDNN 兩種取得方式的目錄結構對照（1 張）。

  cudnn-dir-compare   A. zip 解壓後  vs  B. installer 安裝後

House style 一律走 svglib.py（顏色不要寫死）；標籤一律真正的 <text>，方便 QA 量測。
這是 source/local-gpu-ml-notes/ 筆記，嵌入用 tools/diagrams/embed_figs.py
（該筆記的 md 與 index.html 同步維護，所以要走它而不是 _posts 專用的內嵌器）。
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from svglib import Svg, C, MUT, TXT, CARD, CARD2, MONO  # noqa: E402

HERE = _HERE

# (面板標題, 根目錄, 項目清單[(路徑, 說明)], 階段色, 亮點說明)
PANELS = [
    ("A. zip 直接解壓", "cudnn-windows-x86_64-<版本>_cuda13-archive\\",
     [("bin\\", "cudnn64_9.dll 等"),
      ("include\\", "cudnn*.h"),
      ("lib\\x64\\", "cudnn.lib 等")],
     "teal", "沒有版本資料夾"),
    ("B. installer 安裝", "C:\\Program Files\\NVIDIA\\CUDNN\\v9.22\\",
     [("bin\\13.2\\x64\\", "cudnn64_9.dll 等"),
      ("include\\13.2\\", "cudnn*.h"),
      ("lib\\13.2\\", "cudnn.lib 等")],
     "amber", "多一層版本資料夾 13.2"),
]


def folder(s, x, y, w, h, colour):
    """資料夾圖示：主體 + 左上角的頁籤。"""
    s.rect(x, y + 6, w, h - 6, fill=colour + "33", stroke=colour, rx=4, sw=2)
    s.rect(x, y, w * 0.42, 9, fill=colour + "66", stroke=colour, rx=3, sw=2)


def fig_tree(s):
    """圖 1：cuDNN zip 解壓 vs installer 安裝的目錄結構。"""
    pw = 440
    for pi, (title, root, items, stage, hint) in enumerate(PANELS):
        x0 = 48 + pi * 464
        col = C[stage]
        s.rect(x0, 118, pw, 300, fill=CARD2, stroke=col + "55", rx=14)
        s.text(x0 + 20, 148, title, 15, col, "700")
        s.text(x0 + 20, 172, hint, 11.5, MUT)

        # 根目錄
        folder(s, x0 + 20, 188, 26, 22, col)
        s.text(x0 + 56, 205, root, 11.5, TXT, "normal", "start", MONO)

        # 三層項目
        for ii, (path, note) in enumerate(items):
            y = 228 + ii * 56
            s.line(x0 + 33, 210, x0 + 33, y + 11, "#30363d", 1.5)
            s.line(x0 + 33, y + 11, x0 + 46, y + 11, "#30363d", 1.5)
            folder(s, x0 + 46, y, 24, 20, col)
            s.text(x0 + 80, y + 15, path, 12.5, TXT, "700", "start", MONO)
            s.text(x0 + 80, y + 33, note, 10.5, MUT)

    s.rect(48, 434, 904, 62, fill=CARD2, stroke=C["amber"] + "55", rx=10)
    s.text(68, 460,
           "重點不是「有沒有檔案」，是「版本資料夾長什麼樣」：zip 解壓是扁平的三層，", 13, TXT)
    s.text(68, 482,
           "installer 會在每個資料夾底下多塞一層版本號（13.2），所以「找檔案」的路徑完全不同。",
           13, MUT)


FIGS = [
    ("cudnn-dir-compare", 1000, 516,
     "cuDNN 兩種取得方式的目錄結構：zip 直接解壓是 bin／include／lib 三層，"
     "installer 安裝則在每層底下多一層版本資料夾 13.2",
     "cuDNN 的兩種目錄結構", "zip 解壓 vs installer 安裝", fig_tree,
     "圖 1：cuDNN 的 zip 解壓（左）與 installer 安裝（右）目錄結構對照——"
     "右邊每層底下多了一層版本資料夾，所以找檔案的路徑完全不同。｜手繪 SVG 圖表"),
]


def build(slug):
    """回傳指定 slug 的 Svg 物件。aria 與可見標題分開，避免 25px 標題超出畫布。"""
    for s_slug, w, h, aria, title, sub, fn, _cap in FIGS:
        if s_slug == slug:
            s = Svg(w, h, aria, title, sub)
            fn(s)
            return s
    raise SystemExit("unknown slug: %s" % slug)


def main():
    for slug, w, h, aria, title, sub, fn, _cap in FIGS:
        s = build(slug)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-40s %dx%d  %s"
              % (slug + ".svg", w, h, "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))


if __name__ == "__main__":
    main()
