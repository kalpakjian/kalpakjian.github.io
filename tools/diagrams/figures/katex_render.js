// katex_render.js — render LaTeX to KaTeX HTML at build time.
//
// Reads JSON from stdin: {"items": [{"id": "...", "tex": "...", "display": true}]}
// Writes JSON to stdout: {"results": [{"id": "...", "html": "...", "error": null}]}
//
// Why build-time instead of the browser?
//   KaTeX output is static HTML + inline CSS. Rendering it ahead of time means
//   the page needs no KaTeX JavaScript at all, no CDN request, and no
//   flash-of-unstyled-math. It also matches this site's house rule of
//   "zero external resources" — the formula ships inside the HTML.

const katex = require("katex");

let raw = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (d) => (raw += d));
process.stdin.on("end", () => {
  const input = JSON.parse(raw);
  const out = { results: [] };

  for (const it of input.items) {
    try {
      const html = katex.renderToString(it.tex, {
        displayMode: !!it.display,
        throwOnError: false,
        strict: "ignore",
        output: "htmlAndMathml",
        trust: false,
      });
      out.results.push({ id: it.id, html, error: null });
    } catch (e) {
      out.results.push({ id: it.id, html: null, error: String(e.message || e) });
    }
  }
  process.stdout.write(JSON.stringify(out));
});
