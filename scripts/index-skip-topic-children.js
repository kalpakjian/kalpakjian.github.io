'use strict';

/**
 * 首頁分頁只算「真正的文章」——把專題子頁從首頁的 index_posts 剔除。
 *
 * 為什麼需要（2026-10-30 專題大改組）：
 *   專題拆成多頁之後，子頁面仍然是 _posts 的貼文，用 front-matter
 *   `hide_from_home: true` 表示「不列首頁」（例：OCR 的 cover/toc/各章、
 *   gpu-unlock 的五篇子文章）。
 *
 *   問題：Fluid 主題的 index generator 吃的是 `locals.index_posts`
 *   （= 沒有 hide、也沒有 archive 的貼文），它不知道本站自訂的
 *   hide_from_home，於是首頁第 1 頁的 10 個名額會有 8 個被子頁佔走，
 *   真正要看的文章只剩 2 張卡片。
 *
 *   不要改用主題的 `hide: true`：那會把子頁從歸檔／分類／標籤一起移除，
 *   子頁自己身上的標籤連結就會變成 46 個 404（實測）。
 *
 * 做法：
 *   註冊一個 priority 20 的 before_generate（主題的在預設 10，會先跑），
 *   等主題算完 index_posts 之後，再把它過濾一次。
 *   只影響首頁分頁；歸檔、分類、標籤、RSS、sitemap、貼文頁全部照舊。
 */

const PRIORITY = 20;

hexo.extend.filter.register('before_generate', function () {
  const locals = this.locals;
  if (!locals || !locals.get) return;

  const indexPosts = locals.get('index_posts');
  if (!indexPosts) return;

  const filtered = indexPosts.filter(function (post) {
    return !post.hide_from_home;
  });

  if (filtered.length !== indexPosts.length) {
    this.log.info('[index-skip-topic-children] index_posts %d -> %d（剔除 %d 篇專題子頁）',
                  indexPosts.length, filtered.length,
                  indexPosts.length - filtered.length);
  }
  locals.set('index_posts', filtered);
}, PRIORITY);
