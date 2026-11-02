# -*- coding: utf-8 -*-
"""prototype-over-specs: 兩個分支（問題性質決定原型型態）。

  fig 1  §4 設計問題 → 分岔：邏輯型原型 / 介面型原型
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.dirname(_HERE))
from svglib import Svg, C, MUT, TXT, CARD2  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAIL = "#7d8590"


def fig_branches(s):
    # ---- 起點：一個還沒定案的問題 ----
    s.box(48, 112, 330, 62, "一個還沒定案的設計問題", "先問：這是「能不能聊清楚」的嗎？", "amber", tsize=15)

    s.arrow(213, 174, 213, 200, RAIL)
    s.box(48, 200, 330, 52, "先用對話把問題逼出來", "grilling session（便宜、答案不一定可靠）", "amber", tsize=13.5)

    # ---- 判斷句 ----
    s.arrow(213, 252, 213, 282, RAIL)
    s.rect(48, 282, 330, 56, fill=CARD2, stroke=C["teal"] + "66", rx=12)
    s.text(213, 305, "關鍵問題是「長什麼樣」", 13.5, TXT, "700", anchor="middle")
    s.text(213, 325, "或「怎麼表現」？", 13.5, TXT, "700", anchor="middle")

    # ---- 左分支：邏輯 ----
    s.line(378, 310, 470, 310, RAIL, 2)
    s.line(470, 310, 470, 190, RAIL, 2)
    s.line(470, 190, 512, 190, RAIL, 2)

    s.box(512, 158, 340, 62, "① 邏輯／狀態模型對不對？", "例：狀態機的邊界情況推不出來", "blue", tsize=13.5)
    s.rect(512, 236, 340, 150, fill=CARD2, stroke=C["blue"] + "66", rx=12)
    s.text(528, 262, "產出：單一可分享 HTML 檔", 13, TXT, "700")
    for j, ln in enumerate([
        "自包含，雙擊就能開（不用 build／server）",
        "標籤化狀態面板，每次點擊後重繪",
        "分頁走查：一個 tab 一個情境",
        "邏輯層是純模組（沒有一行 DOM）",
    ]):
        s.text(528, 288 + j * 24, "· " + ln, 11.5, MUT)
    s.text(528, 384, "→ 驗證過的邏輯可直接搬進正式碼", 11.5, C["blue"], "700")

    # ---- 右分支：介面 ----
    s.line(470, 310, 470, 470, RAIL, 2)
    s.line(470, 470, 512, 470, RAIL, 2)

    s.box(512, 438, 340, 62, "② 這到底該長什麼樣？", "例：不確定搜尋結果該怎麼呈現", "teal", tsize=13.5)
    s.rect(512, 516, 340, 150, fill=CARD2, stroke=C["teal"] + "66", rx=12)
    s.text(528, 542, "產出：同一路由上數個變體", 13, TXT, "700")
    for j, ln in enumerate([
        "浮動底欄 ＋ ?variant= 參數切換",
        "變體必須在「結構」上分歧，不是換色",
        "在真實頁面／真實資料密度上渲染",
        "空白頁上評估的變體永遠看起來沒問題",
    ]):
        s.text(528, 568 + j * 24, "· " + ln, 11.5, MUT)
    s.text(528, 664, "→ 挑一個，再與其他變體的元素混搭", 11.5, C["teal"], "700")

    # ---- 底部收束：② 底部 → 左移框外 → 進入紫色框左緣 ----
    s.line(682, 668, 682, 690, RAIL, 2)
    s.line(682, 690, 470, 690, RAIL, 2)
    s.line(470, 690, 470, 726, RAIL, 2)
    s.arrow(470, 726, 512, 726, RAIL)

    s.box(512, 700, 340, 52, "答案先落地，原型進分支", "main 只留決定，原型留作「證據」", "violet", tsize=13.5)

    # ---- 左下：共通點（與右側說明區塊上緣對齊） ----
    s.text(48, 430, "兩條產線的共通點：", 12.5, TXT, "700")
    for j, ln in enumerate([
        "狀態存在記憶體、零設定就能跑，",
        "每一步之後都看得到完整狀態。",
        "",
        "一旦開始「加固」它——加測試、",
        "接真資料庫、為未來做一般化——",
        "你就已經不是在原型了。",
        "",
        "如果做了一天還沒做完，",
        "問題太大了，要拆。",
    ]):
        s.text(48, 456 + j * 22, ln, 11.5, MUT)

    s.text(48, 700, "問題的性質決定原型的型態；", 13, MUT, "700")
    s.text(48, 722, "不是每種問題都該做同一種原型。", 13, MUT, "700")


FIGS = [
    ("prototype-two-branches", "prototype-over-specs", 1, 900, 790,
     "兩個分支：問題性質決定原型的型態",
     "邏輯／狀態問題走單檔 HTML，外觀／表現問題走多變體", fig_branches,
     "圖 1：`/prototype` 的兩條產線——左邊回答「邏輯對不對」，產出單一自包含 HTML；"
     "右邊回答「該長什麼樣」，產出同路由上的數個結構性變體。兩者共同的硬規則是不寫測試、"
     "不接真資料庫、不做抽象。｜手繪 SVG 圖表"),
]

def build(slug):
    """依 slug 重建單張圖，回傳 Svg 物件（供 embed 腳本呼叫）。"""
    for _slug, _note, _art, w, h, title, sub, fn, _cap in FIGS:
        if _slug == slug:
            s = Svg(w, h, title, title, sub)
            fn(s)
            return s
    raise SystemExit("unknown slug: %s" % slug)


if __name__ == "__main__":
    for slug, note, art, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-32s %-22s art#%d %dx%d  %s"
              % (slug + ".svg", note, art, w, h,
                 "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))
