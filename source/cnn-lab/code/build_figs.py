# -*- coding: utf-8 -*-
"""build_figs.py — cnn-lab 的 SVG 產線：結構驗證 → 套版重生 → 量測 → 預覽。

它做四件事，全部離線（只借用本機 Chrome 當渲染器）：

  1. 結構驗證   每張圖的 XML、width/height 與 viewBox 是否一致、id 是否唯一、
                每個 url(#id) 是否找得到、filter 有沒有留 220% 邊界、有沒有外部資源。
  2. 套版重生   --regen：只做「外科手術」——補 role="img"、補 aria-label、
                補 filter 邊界；改前先備份到 img/_backup_時間戳/，內容不動。
  3. 文字量測   把所有圖內嵌成一份暫存 HTML，呼叫 svg-figure-qa 的
                measure_text.py（Chrome getBBox），退出碼直接沿用。
  4. 預覽       --preview：產生一張 12 圖聯絡表 PNG（一次目視全部）。

用法：
    python build_figs.py                    # 驗證 + 量測（預設）
    python build_figs.py --preview          # 另外產生 _preview.png
    python build_figs.py --template         # 產生 img/_template.svg（新圖起點）
    python build_figs.py --regen            # 套版重生（有備份）
    python build_figs.py --no-measure       # 只做結構驗證（不開 Chrome）
    python build_figs.py --json report.json # 另存機器可讀報告
    python build_figs.py --chrome "C:\\...\\chrome.exe" --scale 2

退出碼：0 = 結構與量測全過；1 = 有問題（可直接掛進 CI／pre-commit）
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
IMG = HERE.parent / "img"
NEON = HERE / "neon_svg.py"
MEASURE = Path.home() / ".agents" / "skills" / "svg-figure-qa" / "scripts" / "measure_text.py"

FILTER_BOX = 'x="-60%" y="-60%" width="220%" height="220%"'
MAX_BYTES = 64 * 1024

CHROME_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def find_chrome(explicit: str | None = None) -> str | None:
    for p in [explicit or ""] + CHROME_CANDIDATES:
        if p and os.path.exists(p):
            return p
    return None


def figures() -> list[Path]:
    """img/ 底下所有「正式」圖檔（底線開頭的是模板／暫存，不算）。"""
    return sorted(p for p in IMG.glob("*.svg") if not p.name.startswith("_"))


# ── 1. 結構驗證 ──────────────────────────────────────────────
def check_one(path: Path) -> tuple[list[str], list[str]]:
    issues: list[str] = []
    warns: list[str] = []
    raw = path.read_text(encoding="utf-8")

    def add(msg: str) -> None:
        issues.append(msg)

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        return [f"XML 解析失敗：{exc}"], []

    if root.tag.split("}")[-1] != "svg":
        add("根節點不是 <svg>")

    w, h = root.get("width"), root.get("height")
    vb = root.get("viewBox")
    if not vb:
        add("缺少 viewBox")
    elif w and h:
        try:
            nums = [float(v) for v in re.split(r"[,\s]+", vb.strip())]
            if len(nums) != 4:
                add(f"viewBox 格式不對：{vb!r}")
            elif abs(nums[2] - float(w)) > 0.01 or abs(nums[3] - float(h)) > 0.01:
                add(f"width/height {w}×{h} 與 viewBox {nums[2]:g}×{nums[3]:g} 不一致")
        except ValueError:
            add(f"viewBox／width／height 不是數字：{vb!r} / {w!r} / {h!r}")

    if not root.get("aria-label"):
        add("缺少 aria-label（measure_text.py 靠它辨識與去重）")
    if root.get("role") != "img":
        warns.append('建議補 role="img"')

    ids = re.findall(r'\bid="([^"]+)"', raw)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        add("重複 id：" + ", ".join(dup))

    for ref in sorted(set(re.findall(r"url\(#([^)]+)\)", raw))):
        if ref not in ids:
            add(f"url(#{ref}) 找不到對應 id")

    for m in re.finditer(r"<filter\b[^>]*>", raw):
        tag = m.group(0)
        fid = re.search(r'id="([^"]+)"', tag)
        name = fid.group(1) if fid else "?"
        if not re.search(r'width="\d{3,}%"', tag):
            warns.append(f"filter #{name} 沒設 width/height 百分比，光暈可能被裁")

    if re.search(r'(?:href|src)="https?://', raw):
        add("含外部資源（href/src 指向 http），違反單檔原則")
    if re.search(r'<image\b', raw):
        warns.append("含 <image>（點陣圖），無法保證向量清晰度")

    size = path.stat().st_size
    if size > MAX_BYTES:
        warns.append(f"檔案 {size / 1024:.1f} KB 偏大（> {MAX_BYTES // 1024} KB）")
    if "<text" not in raw:
        warns.append("沒有任何 <text>，量測會跳過")
    if "JhengHei" not in raw and "Noto Sans TC" not in raw:
        warns.append("未宣告中文字型，換機器可能 fallback")

    return issues, warns


# ── 2. 套版重生（只補屬性，不動內容）─────────────────────────
def regen(paths: list[Path]) -> tuple[list[str], Path | None]:
    changed: list[str] = []
    backup = IMG / ("_backup_" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    for p in paths:
        raw = p.read_text(encoding="utf-8")
        new = raw

        # 2a. 補 role="img"
        head = re.search(r"<svg\b[^>]*>", new)
        if head and 'role="img"' not in head.group(0):
            tag = head.group(0)
            patched = tag[:-1] + ' role="img">' if tag.endswith(">") else tag
            new = new.replace(tag, patched, 1)

        # 2b. 補 filter 邊界（沒有百分比才補，避免改到既有數值）
        def fix_filter(m: re.Match) -> str:
            tag = m.group(0)
            if re.search(r'width="\d{3,}%"', tag):
                return tag
            return tag[:-1].rstrip() + " " + FILTER_BOX + ">"

        new = re.sub(r"<filter\b[^>]*>", fix_filter, new)

        if new != raw:
            backup.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, backup / p.name)
            p.write_text(new, encoding="utf-8")
            changed.append(p.name)

    return changed, backup


# ── 3. 量測（借用 svg-figure-qa 的 Chrome getBBox）────────────
def measure(paths: list[Path], chrome: str) -> int:
    body = "\n".join(p.read_text(encoding="utf-8") for p in paths)
    page = ('<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">'
            "<style>body{margin:0;background:#0b1220}svg{display:block;margin:8px}</style>"
            "</head><body>" + body + "</body></html>")
    tmp = Path(tempfile.gettempdir()) / "_cnn_lab_figs.html"
    tmp.write_text(page, encoding="utf-8")
    r = subprocess.run([sys.executable, str(MEASURE), str(tmp), "--chrome", chrome],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "").strip()
    if out:
        print(out)
    if r.stderr.strip():
        print(r.stderr.strip()[:800])
    return r.returncode


# ── 4. 聯絡表（一次目視 12 張）───────────────────────────────
def contact_sheet(paths: list[Path], chrome: str, scale: int = 1) -> Path:
    col_w, gap, pad, cols = 760, 28, 32, 2
    cells, w_h = [], []
    for p in paths:
        raw = p.read_text(encoding="utf-8")
        m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', raw)
        w, h = (float(m.group(1)), float(m.group(2))) if m else (880.0, 480.0)
        cells.append((p.name, re.sub(r"<\?xml[^>]*\?>", "", raw).strip()))
        w_h.append(h * col_w / w)

    rows = [w_h[i:i + cols] for i in range(0, len(w_h), cols)]
    total_h = int(pad + 96 + sum(max(r) + gap for r in rows) + pad)
    total_w = int(pad * 2 + cols * col_w + gap * (cols - 1))

    grid = []
    for name, svg in cells:
        grid.append(f'<figure><div class="lab">{name}</div>{svg}</figure>')
    html_doc = (
        '<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><style>'
        "html,body{margin:0;background:#070b14;}"
        "h1{font:700 22px 'Segoe UI','Microsoft JhengHei',sans-serif;color:#e6edf3;"
        f"margin:{pad}px 0 0 {pad}px;}}"
        ".grid{display:grid;grid-template-columns:repeat(%d,%dpx);gap:%dpx;padding:%dpx;}"
        "figure{margin:0;} .lab{font:11px 'Segoe UI',sans-serif;color:#8b949e;"
        "letter-spacing:.04em;margin:0 0 6px 2px;} svg{width:100%%;height:auto;display:block;}"
        '</style></head><body><h1>cnn-lab · %d 張圖 · %s</h1><div class="grid">'
        % (cols, col_w, gap, pad, len(cells), datetime.now().strftime("%Y-%m-%d %H:%M"))
        + "".join(grid) + "</div></body></html>"
    )
    tmp = Path(tempfile.gettempdir()) / "_cnn_lab_sheet.html"
    tmp.write_text(html_doc, encoding="utf-8")
    out = HERE / "_preview.png"
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}",
                    f"--window-size={total_w},{total_h}",
                    f"--screenshot={out}",
                    "file:///" + str(tmp).replace("\\", "/")],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
    return out


# ── CLI ─────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description="cnn-lab SVG 產線：驗證／重生／量測／預覽")
    ap.add_argument("--preview", action="store_true", help="產生 _preview.png 聯絡表")
    ap.add_argument("--template", action="store_true", help="產生 img/_template.svg")
    ap.add_argument("--regen", action="store_true", help="補 role／filter 邊界（會備份）")
    ap.add_argument("--no-measure", action="store_true", help="跳過 Chrome 量測")
    ap.add_argument("--chrome", default=None, help="Chrome／Edge 執行檔路徑")
    ap.add_argument("--scale", type=int, default=1, help="聯絡表縮放（2 = 2×）")
    ap.add_argument("--json", dest="json_out", default=None, help="另存 JSON 報告")
    args = ap.parse_args()

    paths = figures()
    if not paths:
        print(f"找不到圖：{IMG}")
        return 1
    print(f"圖檔目錄：{IMG}\n共 {len(paths)} 張\n")

    if args.template:
        sys.path.insert(0, str(HERE))
        import neon_svg
        p = neon_svg.write(IMG / "_template.svg", neon_svg.demo())
        print(f"[template] {p.name}（{p.stat().st_size} bytes）\n")

    if args.regen:
        changed, backup = regen(paths)
        if changed:
            print(f"[regen] 改動 {len(changed)} 張：{', '.join(changed)}；備份在 {backup}\n")
        else:
            print("[regen] 12 張全部符合規範，沒有改動\n")

    report: dict = {"generated": datetime.now().isoformat(timespec="seconds"),
                    "dir": str(IMG), "files": [], "measure": None, "preview": None}
    bad = 0
    for p in paths:
        issues, warns = check_one(p)
        print(f"[{'OK  ' if not issues else 'FAIL'}] {p.name:<18} {p.stat().st_size / 1024:6.1f} KB")
        for msg in issues:
            print(f"         x {msg}")
        for msg in warns:
            print(f"         ! {msg}")
        bad += bool(issues)
        report["files"].append({"name": p.name, "bytes": p.stat().st_size,
                                "issues": issues, "warnings": warns})
    print(f"\n結構檢查：{len(paths)} 張，{bad} 張有問題")

    rc = 1 if bad else 0
    chrome = find_chrome(args.chrome)

    if not args.no_measure:
        if not chrome:
            print("[measure] 找不到 Chrome／Edge，跳過（--chrome 可指定）")
        elif not MEASURE.exists():
            print(f"[measure] 找不到 {MEASURE}，跳過")
        else:
            code = measure(paths, chrome)
            report["measure"] = {"tool": str(MEASURE), "returncode": code}
            rc = rc or (1 if code else 0)

    if args.preview:
        if chrome:
            out = contact_sheet(paths, chrome, args.scale)
            report["preview"] = str(out)
            print(f"[preview] {out}")
        else:
            print("[preview] 需要 Chrome／Edge")

    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[report] {args.json_out}")

    return rc


if __name__ == "__main__":
    sys.exit(main())

