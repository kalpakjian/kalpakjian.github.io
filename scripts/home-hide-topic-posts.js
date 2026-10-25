'use strict';

/**
 * 首頁文章清單：移除「已收錄進專題頁」的文章。
 *
 * 為什麼需要這個：
 *   某些文章會被整理成一個專題頁（例：/gpu-unlock/），專題頁已經列出它們。
 *   首頁的「文章」欄位再列一次等於重複，而且這幾篇往往是最新、排在最前面，
 *   會把首頁擠滿同一主題。
 *
 * 怎麼標記：
 *   在文章的 front-matter 加一行 `hide_from_home: true`。
 *   這個旗標只影響首頁；歸檔頁、分類頁、標籤頁、RSS、sitemap 與專題頁照常列出。
 *
 * 為什麼用 HTML 過濾器而不是改資料：
 *   - 主題在 node_modules（themes/ 只有 .gitkeep），改不了主題檔，
 *     而且 CI 會跑 npm ci，改動會被洗掉。
 *   - 在 before_generate 改 locals.posts 會連帶影響歸檔頁與 RSS（它們也吃 locals.posts）。
 *   - 所以走 after_render，只動首頁；判斷依據是 index-card 這個只出現在首頁的 class
 *     （與 home-resources.js 同一套邏輯）。
 *
 * 版本：2026-10-25 初版。
 */

// 首頁每篇文章的外層容器；這個 class 只出現在首頁（歸檔／分類／文章頁都沒有）。
const MARKER = '<div class="row mx-auto index-card">';

// before_generate 階段蒐集要隱藏的文章路徑（帶前導斜線，與 HTML 裡的 href 一致）。
// 兩個坑：
//   1. Hexo 呼叫 before_generate 時傳的第一個參數是 null
//      （hexo/dist/hexo/index.js 的 execFilter('before_generate', null, {context: this})），
//      拿不到 locals 參數；但 this 綁的是 Hexo 實例。
//   2. this.locals 的欄位是 getter registry，不是平面屬性，要用 locals.get('posts') 取得。
let hiddenPaths = [];

hexo.extend.filter.register('before_generate', function () {
  hiddenPaths = [];
  const locals = this.locals;
  const posts = (locals && locals.get && locals.get('posts')) || [];
  posts.forEach(function (post) {
    if (post && post.hide_from_home) hiddenPaths.push('/' + post.path);
  });
  if (hiddenPaths.length) {
    this.log.debug('hide_from_home: 隱藏 %d 篇（%s）', hiddenPaths.length,
                   hiddenPaths.join(', '));
  }
});

hexo.extend.filter.register('after_render:html', function (str, data) {
  if (typeof str !== 'string') return str;
  if (!hiddenPaths.length) return str;
  if (str.indexOf(MARKER) === -1) return str;   // 不是首頁

  // 以 MARKER 切開：parts[0] 是前置內容，parts[i] 是第 i 篇的內文 + 它的收尾 </div>。
  // 整段丟掉等於連同該篇一起移除，而且不影響其他篇的 div 配對。
  const parts = str.split(MARKER);
  if (parts.length < 2) return str;

  let out = parts[0];
  let dropped = 0;
  for (let i = 1; i < parts.length; i++) {
    const chunk = parts[i];
    const hidden = hiddenPaths.some(function (p) {
      return chunk.indexOf('href="' + p + '"') !== -1 ||
             chunk.indexOf('src="' + p) !== -1;
    });
    if (hidden) {
      dropped++;
      continue;
    }
    out += MARKER + chunk;
  }
  if (dropped) {
    this.log.debug('hide_from_home: 首頁文章清單移除 %d 篇', dropped);
  }
  return out;
});
