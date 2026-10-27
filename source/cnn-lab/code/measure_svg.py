# -*- coding: utf-8 -*-
"""measure_svg.py — transform-aware 的 SVG 文字量測（本機 Chrome，離線）。

為什麼不用現成的 measure_text.py：
    那支是為「筆記頁內嵌 SVG」寫的，直接拿 `<text x=…>` 的座標跟 viewBox 比。
    cnn-lab 的圖大量使用 `<g transform="translate(…)">`，座標是「群組內座標」，
    於是 `translate(90,80)` 裡 x=-10 的 y 軸標籤會被誤判成「超出畫布」（實際在 x=80）。
    卡片判定也會把長條圖的 `<rect rx="4" fill="url(#barA)">` 當成卡片。

這支的差別只有三點：
    1. 用 `getBBox()` + `getCTM()` 換算成「畫布座標」後才比較。
    2. 卡片只認「實色填色」的圓角矩形（`fill` 是 hex，不是 `url(#…)`）。
    3. 額外回報「文字 vs 卡片」與「文字 vs 畫布」的實際 px 數，方便修圖。

判定代碼：
    [OVERLAP] 兩段文字邊界框相交超過 tol（兩軸都要超過）
    [CARD]    文字右緣超出所屬卡片右緣超過 inset
    [EDGE]    文字邊界框超出 viewBox

用法：
    python measure_svg.py img                 # 整個資料夾
    python measure_svg.py img/09_ab_results.svg img/10_confidence.svg
    python measure_svg.py img --chrome "C:\\...\\chrome.exe" --json r.json

退出碼：0 = 全部通過；1 = 有問題。
"""
from __future__ import annotations

import argparse
import html as htmllib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    # CI（ubuntu-latest）與 macOS
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

JS = r"""
<script>
function gbox(el) {
  var b = el.getBBox();
  var root = el.ownerSVGElement || el;
  var m = root.getCTM().inverse().multiply(el.getCTM());
  var pts = [[b.x, b.y], [b.x + b.width, b.y],
             [b.x, b.y + b.height], [b.x + b.width, b.y + b.height]];
  var xs = [], ys = [];
  for (var i = 0; i < pts.length; i++) {
    var q = new DOMPoint(pts[i][0], pts[i][1]).matrixTransform(m);
    xs.push(q.x); ys.push(q.y);
  }
  var x = Math.min.apply(null, xs), y = Math.min.apply(null, ys);
  return {x: x, y: y,
          w: Math.max.apply(null, xs) - x, h: Math.max.apply(null, ys) - y};
}
var out = [];
document.querySelectorAll('.fig').forEach(function (w) {
  var svg = w.querySelector('svg');
  var vb = (svg.getAttribute('viewBox') || '0 0 800 600')
             .trim().split(/[\s,]+/).map(Number);
  var texts = [];
  svg.querySelectorAll('text').forEach(function (t) {
    var b = gbox(t);
    texts.push({x: b.x, y: b.y, w: b.w, h: b.h, t: t.textContent});
  });
  var cards = [];
  svg.querySelectorAll('rect').forEach(function (r) {
    var rx = parseFloat(r.getAttribute('rx') || '0');
    var fill = r.getAttribute('fill') || '';
    if (!(rx >= 4) || !fill || fill === 'none' || fill.indexOf('url(') === 0) return;
    var b = gbox(r);
    if (b.w >= vb[2] - 2 || b.h >= vb[3] - 2) return;
    cards.push({x: b.x, y: b.y, w: b.w, h: b.h});
  });
  out.push({name: w.getAttribute('data-name'), vb: vb, texts: texts, cards: cards});
});
document.getElementById('out').textContent = JSON.stringify(out);
</script>
"""


def find_chrome(explicit: str | None = None) -> str | None:
    if explicit and os.path.exists(explicit):
        return explicit
    # PATH 上的名稱（CI 常見：google-chrome / chromium）
    for name in ("google-chrome", "google-chrome-stable", "chromium",
                 "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    for p in CHROME_CANDIDATES:
        if p and os.path.exists(p):
            return p
    return None


def collect(targets: list[str]) -> list[Path]:
    out: list[Path] = []
    for t in targets:
        p = Path(t)
        if p.is_dir():
            out += sorted(x for x in p.glob("*.svg") if not x.name.startswith("_"))
        elif p.suffix.lower() == ".svg":
            out.append(p)
    return out


def measure(paths: list[Path], chrome: str) -> dict:
    """把每張 SVG 內嵌成一份暫存 HTML，交給 Chrome 量測，回傳 {檔名: 量測結果}。"""
    body = []
    for p in paths:
        raw = p.read_text(encoding="utf-8")
        raw = re.sub(r"<\?xml[^>]*\?>", "", raw).strip()
        body.append(f'<div class="fig" data-name="{htmllib.escape(p.name, True)}">{raw}</div>')
    page = ('<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">'
            "<style>body{margin:0;background:#0b1220}svg{display:block}</style></head><body>"
            + "\n".join(body) + '<pre id="out"></pre>' + JS + "</body></html>")
    tmp = Path(tempfile.gettempdir()) / "_measure_svg.html"
    tmp.write_text(page, encoding="utf-8")
    r = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--dump-dom",
                        "--virtual-time-budget=10000",
                        "file:///" + str(tmp).replace("\\", "/")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r'<pre id="out">([\s\S]*?)</pre>', r.stdout or "")
    if not m:
        raise SystemExit(f"量測失敗：Chrome 沒有回傳結果（{len(r.stdout or '')} bytes）")
    return {d["name"]: d for d in json.loads(htmllib.unescape(m.group(1)))}


def evaluate(fig: dict, tol: float = 1.6, inset: float = 4.0) -> list[tuple[str, str]]:
    """回傳 [(代碼, 說明)]；座標都已換算成畫布座標。"""
    vbw, vbh = fig["vb"][2], fig["vb"][3]
    texts, cards = fig["texts"], fig["cards"]
    probs: list[tuple[str, str]] = []

    for i, a in enumerate(texts):
        ax2, ay2 = a["x"] + a["w"], a["y"] + a["h"]
        if a["x"] < -tol or a["y"] < -tol or ax2 > vbw + tol or ay2 > vbh + tol:
            probs.append(("EDGE", "%r  文字 %.0f..%.0f / %.0f..%.0f（畫布 %g×%g）"
                          % (a["t"], a["x"], ax2, a["y"], ay2, vbw, vbh)))
        for b in texts[i + 1:]:
            ox = min(ax2, b["x"] + b["w"]) - max(a["x"], b["x"])
            oy = min(ay2, b["y"] + b["h"]) - max(a["y"], b["y"])
            if ox > tol and oy > tol:
                probs.append(("OVERLAP", "%r  <->  %r（重疊 %.0f×%.0f px）"
                              % (a["t"], b["t"], ox, oy)))

    for c in cards:
        cx2 = c["x"] + c["w"]
        for a in texts:
            inside = c["x"] - 2 <= a["x"] <= cx2 and c["y"] <= a["y"] + a["h"] / 2 <= c["y"] + c["h"]
            if not inside:
                continue
            if a["x"] + a["w"] > cx2 - inset:
                probs.append(("CARD", "%r  文字 %.0f..%.0f 超出卡片 %.0f..%.0f"
                              % (a["t"], a["x"], a["x"] + a["w"], c["x"], cx2)))
    return probs


def report(paths: list[Path], chrome: str, tol: float = 1.6, inset: float = 4.0,
           quiet: bool = False) -> tuple[int, dict]:
    """量測並印出問題；回傳 (有問題的張數, 統計)。"""
    data = measure(paths, chrome)
    bad, counts, per_file = 0, {}, {}
    for p in paths:
        fig = data.get(p.name)
        if not fig:
            continue
        probs = evaluate(fig, tol, inset)
        if probs:
            bad += 1
            per_file[p.name] = len(probs)
            for kind, msg in probs:
                counts[kind] = counts.get(kind, 0) + 1
            if not quiet:
                print(f"[{p.name}]")
                for kind, msg in probs:
                    print(f"    [{kind}] {msg}")
    total = sum(counts.values())
    detail = "、".join(f"{k} {v}" for k, v in sorted(counts.items())) or "無"
    print(f"\n量測：{len(paths)} 張，{bad} 張有問題（{total} 條：{detail}）")
    if per_file:
        print("　有問題的圖：" + "、".join(f"{k} {v} 條" for k, v in per_file.items()))
    return bad, {"files": per_file, "counts": counts, "total": total}


def main() -> int:
    ap = argparse.ArgumentParser(description="transform-aware SVG 文字量測（Chrome getBBox）")
    ap.add_argument("targets", nargs="+", help="SVG 檔或資料夾")
    ap.add_argument("--chrome", default=None, help="Chrome／Edge 執行檔路徑")
    ap.add_argument("--tol", type=float, default=1.6, help="容忍像素（預設 1.6）")
    ap.add_argument("--inset", type=float, default=4.0, help="卡片內縮（預設 4）")
    ap.add_argument("--json", dest="json_out", default=None, help="另存 JSON")
    ap.add_argument("--quiet", action="store_true", help="只印總結")
    a = ap.parse_args()

    paths = collect(a.targets)
    if not paths:
        print("找不到 SVG")
        return 1
    chrome = find_chrome(a.chrome)
    if not chrome:
        print("找不到 Chrome／Edge：用 --chrome 指定，或設 CHROME_PATH")
        return 1
    bad, stats = report(paths, chrome, a.tol, a.inset, a.quiet)
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(stats, ensure_ascii=False, indent=2),
                                    encoding="utf-8")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

