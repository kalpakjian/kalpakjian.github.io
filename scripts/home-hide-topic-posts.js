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
 *       2026-10-28 修正：改以「單張卡片」regex 取代 split(MARKER)，避免最後一張卡片
 *       被隱藏時，把分頁器／footer／全部 <script> 一起吃掉（首頁 HTML 被截斷、
 *       封面圖停在 loading.gif）。
 *       2026-10-30 專題大改組：專題子頁改吃 Fluid 主題自己的 `hide: true`（在
 *       before_generate 就從 locals.posts 移除，分頁因此只算真正的文章），
 *       目前**沒有任何貼文使用 hide_from_home**，本檔保留作為備援機制。
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
    // post.path 一般沒有前導斜線（2026/10/28/foo/），但 front-matter 用
    // `permalink: ocr/foo/` 覆寫時 Hexo 會保留前導斜線（/ocr/foo/）；
    // 直接加 '/' 會變成 '//ocr/foo/'，比對不到卡片上的 href="/ocr/foo/"。
    if (post && post.hide_from_home) {
      hiddenPaths.push('/' + String(post.path).replace(/^\/+/, ''));
    }
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

  // 以「一張卡片的完整範圍」為單位比對，而不是 str.split(MARKER)。
  //
  // 為什麼不能 split：split 之後，最後一張卡片之後的「收尾」——分頁器、footer、
  // 以及 <body> 底部的全部 <script>（含 img-lazyload.js）——會黏在最後一個
  // chunk 上。只要最後一張卡片剛好是 hide_from_home 的文章（首頁第 1 頁的
  // 第 10 篇就是），整段收尾會被一起丟掉：HTML 在最後一張卡片的 </div> 後
  // 直接結束、沒有 </body></html>、沒有任何主題 JS，於是封面圖的
  // <img srcset="/img/loading.gif" lazyload> 永遠等不到 img-lazyload.js
  // 把 srcset 拿掉，首頁封面就全部停在 loading.gif。
  //
  // 每張卡片固定從 MARKER 開始，到該卡唯一的 </article> 加外層 </div> 結束
  // （index.ejs 一篇只渲染一個 <article>，卡片內沒有其他 </article>）。
  const CARD_RE = /<div class="row mx-auto index-card">[\s\S]*?<\/article>\s*<\/div>/g;

  let dropped = 0;
  const out = str.replace(CARD_RE, function (card) {
    const hidden = hiddenPaths.some(function (p) {
      return card.indexOf('href="' + p + '"') !== -1 ||
             card.indexOf('src="' + p) !== -1;
    });
    if (!hidden) return card;
    dropped++;
    return '';
  });
  if (dropped) {
    this.log.debug('hide_from_home: 首頁文章清單移除 %d 篇', dropped);
  }
  return out;
});
