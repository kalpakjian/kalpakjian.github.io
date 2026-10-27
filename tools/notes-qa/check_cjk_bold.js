/**
 * check_cjk_bold.js —— 找出「`**` 粗體在中文字旁邊失效、變成字面星號」的地方。
 *
 * 問題根源（CommonMark 的 flanking 規則）：
 *   `**粗體**` 要能成對，結尾的 `**` 必須是 right-flanking、開頭的 `**` 必須是 left-flanking。
 *   中日文裡這兩條很容易同時不成立：
 *     · 結尾 `**` 前面是標點（`**（fuse）**`）而且後面緊接中文字 → 不是 right-flanking → 收不了尾
 *     · 開頭 `**` 後面是標點（`**「2 倍」`）而且前面是中文字 → 不是 left-flanking → 開不了頭
 *   結果就是整段 `**` 以字面星號輸出，讀者看到的是 `**粗體**` 而不是粗體。
 *
 * 修法（單一處最省事）：把那一段改成 HTML 標籤
 *     `**（fuse）**` → `<strong>（fuse）</strong>`
 *   站上其他文章本來就在 blockquote 裡用 `<strong>整理說明</strong>`，所以這是既有寫法。
 *
 * 為什麼是「警告」而不是品質閘門的硬性檢查：
 *   NOTE_STYLE_CONTRACT §12.3 的前例——硬性檢查一旦全站紅燈，真正的缺陷訊號會被淹掉。
 *   所以這支工具是**獨立的、唯讀的**檢查器，不接進 qa_notes.ps1 的阻擋流程。
 *
 * 用法：
 *   node tools/notes-qa/check_cjk_bold.js            # 掃全站，有問題 exit 1
 *   node tools/notes-qa/check_cjk_bold.js <檔案.md>  # 只掃某幾個檔案
 *
 * 輸出：檔案、行號、去掉標籤後的該行文字。
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { marked } = require('marked');

const REPO = path.resolve(__dirname, '..', '..');
const SKIP_DIRS = new Set(['img', 'categories', 'tags', 'node_modules', 'public']);

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP_DIRS.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else if (entry.name.endsWith('.md')) out.push(full);
  }
  return out;
}

// 程式碼區塊裡的 ** 是合法的（例如 Python 的 ** 運算子），要先濾掉。
function stripCode(html) {
  return html
    .replace(/<pre[\s\S]*?<\/pre>/g, '')
    .replace(/<code[\s\S]*?<\/code>/g, '');
}

function checkFile(file) {
  const src = fs.readFileSync(file, 'utf8');
  const html = marked.parse(src);
  const bad = [];
  stripCode(html)
    .split('\n')
    .forEach((line) => {
      if (line.indexOf('**') !== -1) {
        bad.push(line.replace(/<[^>]+>/g, '').trim());
      }
    });
  return bad;
}

function main(argv) {
  const targets = argv.length
    ? argv.map((f) => path.resolve(REPO, f))
    : walk(path.join(REPO, 'source')).sort();

  let total = 0;
  let files = 0;
  for (const f of targets) {
    if (!fs.existsSync(f)) {
      console.error('SKIP (not found): ' + f);
      continue;
    }
    const bad = checkFile(f);
    if (!bad.length) continue;
    files += 1;
    total += bad.length;
    console.log('### ' + path.relative(REPO, f) + '  (' + bad.length + ')');
    bad.slice(0, 6).forEach((l) => console.log('    ' + l.slice(0, 140)));
    if (bad.length > 6) console.log('    ... 還有 ' + (bad.length - 6) + ' 行');
  }
  console.log('\n受影響檔案 ' + files + ' 個 / 共 ' + total + ' 行');
  console.log('修法：把該處的 **粗體** 改成 <strong>粗體</strong>（不要在 ** 旁邊直接接中文字）');
  return total ? 1 : 0;
}

if (require.main === module) {
  process.exitCode = main(process.argv.slice(2));
}

module.exports = { checkFile, walk };
