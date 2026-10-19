# -*- coding: utf-8 -*-
"""共用 SVG 圖表產生器（本站內嵌圖表統一風格 + 版面基本元件）。

一個地方管 house style（深色圖卡、配色、字型）與版面元件，所以每一張轉換後的
圖看起來都像同一套。新圖表只要提供「資料」，不要重寫排版程式碼。

用法：
    from svglib import Svg, C
    s = Svg(900, 600, "我的圖", "標題", "副標")
    s.card(100, 100, 300, 60, "標題", "副標", stage="teal", num="1")
    s.arrow(250, 160, 250, 200)
    s.save("out.svg", "out_measure.html")
"""
import io

# ---- house style -------------------------------------------------------------
BG, CARD, CARD2 = "#0d1117", "#161b22", "#1c2230"
LINE, TXT, MUT = "#30363d", "#e6edf3", "#8b949e"
FONT = "'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif"
MONO = "'Cascadia Mono',Consolas,'Courier New',monospace"

C = dict(teal="#2dd4bf", blue="#58a6ff", amber="#fbbf24", violet="#c084fc",
         green="#3fb950", rose="#f472b6", gray="#7d8590", ink="#08141a")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Svg(object):
    def __init__(self, w, h, aria, title=None, subtitle=None):
        self.w, self.h, self.aria = w, h, aria
        self.p = []
        self.defs = []
        self._markers = {}
        self.segs = []          # line/arrow segments, for the collision check
        self.txts = []          # (x, y, est_width, size, anchor)
        if title:
            self.text(48, 52, title, 25, TXT, "700")
        if subtitle:
            self.text(48, 82, subtitle, 14.5, MUT)

    # ---- collision self-check -------------------------------------------------
    @staticmethod
    def _est_w(s, size):
        return sum(size if ord(c) > 0x2E80 else size * 0.52 for c in s)

    def check(self):
        """Report text boxes that a connector line runs through.

        getBBox() only compares text vs text; this catches the other half
        (labels sitting on arrows / rails), which is otherwise only visible
        by zooming in on the rendered PNG.
        """
        bad = []
        for (x, y, w, size, anchor) in self.txts:
            x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
            bx0, bx1 = x0 - 1, x0 + w + 1
            by0, by1 = y - size * 0.78, y + size * 0.28
            for (sx1, sy1, sx2, sy2) in self.segs:
                hit = False
                for i in range(41):
                    t = i / 40.0
                    px, py = sx1 + (sx2 - sx1) * t, sy1 + (sy2 - sy1) * t
                    if bx0 <= px <= bx1 and by0 <= py <= by1:
                        hit = True
                        break
                if hit:
                    bad.append(((sx1, sy1, sx2, sy2), (round(bx0), round(by0),
                                                       round(bx1), round(by1))))
        return bad

    # ---- primitives ----------------------------------------------------------
    def text(self, x, y, s, size=15, fill=TXT, weight="normal",
             anchor="start", font=FONT):
        a = ' text-anchor="%s"' % anchor if anchor != "start" else ""
        w = ' font-weight="%s"' % weight if weight != "normal" else ""
        self.p.append('<text x="%s" y="%s" font-size="%s" fill="%s"%s%s '
                      'font-family="%s">%s</text>' % (x, y, size, fill, w, a, font, esc(s)))
        self.txts.append((x, y, self._est_w(s, size), size, anchor))

    def rect(self, x, y, w, h, fill=CARD, stroke=LINE, rx=10, sw=1.5):
        s = ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
             'stroke="%s" stroke-width="%s"/>' % (x, y, w, h, rx, fill, stroke, sw))
        self.p.append(s)
        return s

    def line(self, x1, y1, x2, y2, stroke="#7d8590", width=2):
        self.p.append('<path d="M %s %s L %s %s" fill="none" stroke="%s" '
                      'stroke-width="%s"/>' % (x1, y1, x2, y2, stroke, width))
        self.segs.append((x1, y1, x2, y2))

    def marker(self, colour, name=None):
        name = name or ("m" + colour.replace("#", ""))
        if name not in self._markers:
            self._markers[name] = colour
            self.defs.append(
                '<marker id="%s" viewBox="0 0 10 10" refX="8.5" refY="5" '
                'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                '<path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker>' % (name, colour))
        return name

    def arrow(self, x1, y1, x2, y2, colour="#7d8590", width=2):
        m = self.marker(colour)
        self.p.append('<path d="M %s %s L %s %s" fill="none" stroke="%s" '
                      'stroke-width="%s" marker-end="url(#%s)"/>'
                      % (x1, y1, x2, y2, colour, width, m))
        self.segs.append((x1, y1, x2, y2))

    def badge(self, cx, cy, label, colour, r=15, size=14):
        self.p.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="0.92"/>'
                      % (cx, cy, r, colour))
        self.text(cx, cy + size * 0.38, label, size, C["ink"], "700", "middle")

    def card(self, x, y, w, h, title, detail=None, stage="teal", num=None,
             fill=CARD, rx=10, tsize=15.5, dsize=12):
        col = C[stage]
        self.rect(x, y, w, h, fill=fill, stroke=col + "66", rx=rx)
        tx = x + 16
        if num is not None:
            self.badge(x + 32, y + h / 2, num, col)
            tx = x + 60
        if detail:
            self.text(tx, y + h / 2 - 3, title, tsize, TXT, "700")
            self.text(tx, y + h / 2 + 18, detail, dsize, MUT)
        else:
            self.text(tx, y + h / 2 + tsize * 0.36, title, tsize, TXT, "700")

    def box(self, x, y, w, h, label, sub=None, stage="teal", fill=CARD, rx=10,
            tsize=15, dsize=11.5, align="middle"):
        """Centred label box (no badge) — for layer / architecture diagrams."""
        col = C[stage]
        self.rect(x, y, w, h, fill=fill, stroke=col + "66", rx=rx)
        cx = x + w / 2 if align == "middle" else x + 14
        if sub:
            self.text(cx, y + h / 2 - 2, label, tsize, TXT, "700", align)
            self.text(cx, y + h / 2 + 20, sub, dsize, MUT, "normal", align)
        else:
            self.text(cx, y + h / 2 + tsize * 0.36, label, tsize, TXT, "700", align)

    # ---- buses ---------------------------------------------------------------
    def bus_out(self, src, targets, colour="#7d8590", stub=24):
        """One source -> vertical bus -> an arrow into each target centre."""
        x, y = src
        ty = min(t[1] for t in targets) - stub
        self.line(x, y, x, ty, colour)
        self.line(min(t[0] for t in targets), ty, max(t[0] for t in targets), ty, colour)
        for tx, tyy in targets:
            self.arrow(tx, ty, tx, tyy - 2, colour)

    def bus_in(self, sources, target, colour="#7d8590", stub=24):
        """Many sources -> vertical bus -> one arrow into the target centre."""
        x, y = target
        sy = max(s[1] for s in sources) + stub
        for sx, syy in sources:
            self.line(sx, syy, sx, sy, colour)
        self.line(min(s[0] for s in sources), sy, max(s[0] for s in sources), sy, colour)
        self.arrow(x, sy, x, y - 2, colour)

    def legend(self, items, y, x=48, step=215):
        for i, (stage, label) in enumerate(items):
            lx = x + i * step
            self.p.append('<circle cx="%s" cy="%s" r="7" fill="%s"/>'
                          % (lx + 7, y - 4, C[stage]))
            self.text(lx + 22, y, label, 13, MUT)

    # ---- output --------------------------------------------------------------
    def _wrap(self):
        head = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
                'role="img" aria-label="%s" '
                'style="width:100%%;height:auto;display:block">'
                % (self.w, self.h, esc(self.aria)))
        body = [head]
        if self.defs:
            body.append("<defs>" + "".join(self.defs) + "</defs>")
        body.append('<rect x="0.75" y="0.75" width="%s" height="%s" rx="16" '
                    'fill="%s" stroke="#222b36" stroke-width="1.5"/>'
                    % (self.w - 1.5, self.h - 1.5, BG))
        body.extend(self.p)
        body.append("</svg>")
        return "\n".join(body)

    def save(self, svg_path, measure_path=None):
        svg = self._wrap()
        io.open(svg_path, "w", encoding="utf-8", newline="\n").write(svg)
        if measure_path:
            io.open(measure_path, "w", encoding="utf-8", newline="\n").write(
                '<!DOCTYPE html>\n<html lang="zh-Hant"><head><meta charset="utf-8">'
                '<title>measure</title><style>body{background:#0d1117;margin:0;'
                'padding:20px}svg{display:block}</style></head><body>\n'
                + svg + '\n</body></html>\n')
        return svg

    def figure(self, caption, marker="FIGURE"):
        """Site figure markup (dark card + figcaption) with the SVG inlined."""
        svg = self._wrap()
        return ('<!-- %s -->\n<figure style="margin:20px 0;padding:14px 12px;'
                'background:#0d1117;border:1px solid #222b36;border-radius:12px;'
                'text-align:center;-webkit-print-color-adjust:exact;'
                'print-color-adjust:exact">\n' % marker + svg + "\n"
                '<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;'
                'line-height:1.65;text-align:left">' + caption + '</figcaption>\n'
                '</figure>\n<!-- /%s -->' % marker)
