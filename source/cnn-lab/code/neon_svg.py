# -*- coding: utf-8 -*-
"""neon_svg.py — NEON 風格 SVG 的共用工具組（零依賴、可完全離線）。

為什麼要有這支：`img/` 裡 12 張圖原本是手寫 SVG，每次新圖都要複製貼上
`<defs>` 與一堆顏色，很容易漏掉光暈邊界（`x/y/width/height` 沒留 220% 就會被裁）。
這裡把「版型」抽成函式，新圖只填座標與文字。

色票與 `img/00_cover.svg`～`img/12_lessons.svg` 完全一致。

用法：
    from neon_svg import *
    svg = (open_svg(900, 320, "示意圖：三層卷積")
           + frame(900, 320)
           + title(60, 90, "三層卷積", "每一層都在縮小空間、增加通道", 780)
           + pill(60, 170, 190, "Conv 3×3", CYAN)
           + bullet(66, 250, "內文不加 filter，保持可讀", PINK)
           + "</svg>\n")
    write("out.svg", svg)

    python neon_svg.py out.svg      # 產生一張示範圖，用來確認環境正常
"""
from __future__ import annotations

import sys
from pathlib import Path

# ── 色票（與既有 12 張圖一致，不要任意新增）─────────────────
BG_A, BG_B, BG_C = "#0d1424", "#0b1220", "#130d24"
GRID = "#16233a"
CYAN, VIOLET, PINK = "#22d3ee", "#a78bfa", "#f472b6"
TEAL, AMBER, GREEN = "#2dd4bf", "#fbbf24", "#3fb950"
TXT, TXT2, TXT3 = "#e6edf3", "#9aa7b6", "#8b949e"
CARD, CARD_DEEP = "#0f1720", "#0a1420"

FONT = "'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif"

#: 光暈邊界：留 220% 才不會把 blur 裁掉（x = -60%）
FILTER_BOX = 'x="-60%" y="-60%" width="220%" height="220%"'


def defs(extra: str = "") -> str:
    """共用 defs。`extra` 可塞額外的 marker／漸層（id 不要與下面重複）。"""
    return f"""  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{BG_A}"/>
      <stop offset="52%" stop-color="{BG_B}"/>
      <stop offset="100%" stop-color="{BG_C}"/>
    </linearGradient>
    <pattern id="gr" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="{GRID}" stroke-width="1"/>
    </pattern>
    <filter id="gl" {FILTER_BOX}>
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="gl2" {FILTER_BOX}>
      <feGaussianBlur stdDeviation="10" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{CYAN}"/>
      <stop offset="50%" stop-color="{VIOLET}"/>
      <stop offset="100%" stop-color="{PINK}"/>
    </linearGradient>{extra}
  </defs>"""


def open_svg(w: int, h: int, label: str, extra_defs: str = "") -> str:
    """開頭：`aria-label` 是 measure_text.py 辨識與去重的依據，必填。"""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"\n'
        f'     viewBox="0 0 {w} {h}" font-family="{FONT}" role="img"\n'
        f'     aria-label="{label}">\n'
        f"{defs(extra_defs)}\n"
    )


def frame(w: int, h: int, radius: int = 16) -> str:
    """底層：漸層 + 網格 + 1.5px 霓虹描邊。"""
    return (
        f'  <rect width="{w}" height="{h}" fill="url(#bg)"/>\n'
        f'  <rect width="{w}" height="{h}" fill="url(#gr)" opacity=".55"/>\n'
        f'  <rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="{radius}"\n'
        f'        fill="none" stroke="{CYAN}" stroke-opacity=".22" stroke-width="1.5"/>\n'
    )


def title(x: int, y: int, text: str, sub: str = "", rule_w: int = 0,
          size: int = 34) -> str:
    """大標 + 副標 + 三色分隔線。"""
    out = [f'  <text x="{x}" y="{y}" font-size="{size}" font-weight="700"\n'
           f'        fill="{TXT}" filter="url(#gl2)">{text}</text>']
    if sub:
        out.append(f'  <text x="{x}" y="{y + 34}" font-size="14" fill="{VIOLET}"\n'
                   f'        filter="url(#gl)">{sub}</text>')
    if rule_w:
        out.append(f'  <line x1="{x}" y1="{y + 54}" x2="{x + rule_w}" y2="{y + 54}"\n'
                   f'        stroke="url(#rule)" stroke-width="3" filter="url(#gl)"/>')
    return "\n".join(out) + "\n"


def card(x: int, y: int, w: int, h: int, color: str, label: str = "",
         sub: str = "", radius: int = 10, fill: str = CARD) -> str:
    """圓角卡片 +（可選）標題與說明；卡片發光，內文不發光。"""
    out = [f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}"\n'
           f'        fill="{fill}" stroke="{color}" stroke-width="1.5" filter="url(#gl)"/>']
    if label:
        out.append(f'  <text x="{x + w // 2}" y="{y + 26}" font-size="12.5"\n'
                   f'        font-weight="700" text-anchor="middle" fill="{color}"\n'
                   f'        filter="url(#gl)">{label}</text>')
    if sub:
        out.append(f'  <text x="{x + w // 2}" y="{y + 45}" font-size="9.5"\n'
                   f'        text-anchor="middle" fill="{TXT2}">{sub}</text>')
    return "\n".join(out) + "\n"


def pill(x: int, y: int, w: int, text: str, color: str, h: int = 34) -> str:
    """膠囊標籤（封面與章節頁的統計數字都用它）。"""
    return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h // 2}"\n'
            f'        fill="{CARD}" stroke="{color}" stroke-width="1.3" filter="url(#gl)"/>\n'
            f'  <text x="{x + w // 2}" y="{y + h // 2 + 5}" font-size="12.5"\n'
            f'        text-anchor="middle" fill="{color}" filter="url(#gl)">{text}</text>\n')


def bullet(x: int, y: int, text: str, color: str = CYAN) -> str:
    """圓點 + 一行說明（內文一律不加 filter）。"""
    return (f'  <circle cx="{x}" cy="{y - 4}" r="3.5" fill="{color}" filter="url(#gl)"/>\n'
            f'  <text x="{x + 14}" y="{y}" font-size="12.5" fill="{TXT2}">{text}</text>\n')


def legend(x: int, y: int, items: list, step: int = 26,
           cols: int = 1, col_w: int = 220) -> str:
    """色塊圖例。items = [(顏色, 說明), …]"""
    out = []
    for i, (color, text) in enumerate(items):
        cx = x + (i % cols) * col_w
        cy = y + (i // cols) * step
        out.append(f'  <rect x="{cx}" y="{cy - 11}" width="12" height="12" rx="3"\n'
                   f'        fill="{CARD}" stroke="{color}" stroke-width="1.4"/>\n'
                   f'  <text x="{cx + 18}" y="{cy}" font-size="10" fill="{TXT2}">{text}</text>')
    return "\n".join(out) + "\n"


def write(path, markup: str) -> Path:
    """寫檔（UTF-8、結尾補一個換行），回傳實際路徑。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(markup if markup.endswith("\n") else markup + "\n", encoding="utf-8")
    return p


def demo(w: int = 900, h: int = 320) -> str:
    """一張自我檢查用的示範圖：四個元素都在，代表工具組正常。"""
    return (
        open_svg(w, h, "NEON 工具組自我檢查：標題、膠囊、卡片、圖例")
        + frame(w, h)
        + "\n"
        + title(60, 92, "NEON 工具組", "零依賴 Python → SVG，可完全離線", 780)
        + "\n"
        + pill(60, 176, 190, "open_svg()", CYAN)
        + pill(266, 176, 190, "frame()", VIOLET)
        + pill(472, 176, 190, "title() / pill()", PINK)
        + pill(678, 176, 162, "legend()", AMBER)
        + "\n"
        + bullet(66, 258, "同一段 defs 換座標就能生新圖，風格不會跑掉", CYAN)
        + bullet(66, 284, "光暈只加在標題與外框，內文保持可讀", PINK)
        + f'\n  <text x="{w - 40}" y="{h - 18}" text-anchor="end" font-size="10.5"'
        f' fill="{TXT3}">{w}×{h} · 無外部資源 · 可離線重建</text>\n'
        "</svg>\n"
    )


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "_template.svg"
    p = write(target, demo())
    print(f"written: {p.resolve()} ({p.stat().st_size} bytes)")

