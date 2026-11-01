'use strict';

/**
 * 首頁資源總覽：專題（左欄）/ 學習筆記（右欄）/ 文章
 *
 * 為什麼需要這支腳本：
 *   Fluid 主題的 layout/index.ejs 只會輸出「文章卡片清單」，首頁完全沒有專題與學習筆記的入口；
 *   主題的 theme.custom_html 雖然可以塞 HTML，但那是「全站每一頁」都會輸出，不適合。
 *   所以這裡用 Hexo 原生支援的 scripts/ 目錄註冊 after_render:html 過濾器：
 *   只在首頁（index.ejs 產出的文章清單之前）注入「兩欄標題清單 + 文章標題」，其他頁面完全不動。
 *
 * 版面（2026-10-19 改版）：兩欄只輸出標題，沒有小標、簡介與膠囊連結。
 *   左欄＝專題（TOPICS）、右欄＝學習筆記（NOTES），每項連到該系列的總覽頁；
 *   章節／測驗等下載與子頁面入口改由導覽列（_config.fluid.yml 的 navbar.menu）與各總覽頁提供。
 *   ≤768px 時兩欄自動堆疊成單欄（見 source/css/custom.css）。
 *
 * 偵測方式（不依賴主題內部路徑）：
 *   1. 只處理含 `<div class="row mx-auto index-card">` 的 HTML（目前全站只有 public/index.html 有）。
 *   2. 用 data-home-resources 標記避免重複注入（layout.ejs 外層會再過一次同一個過濾器）。
 *
 * 維護方式：只要改下面的 TOPICS / NOTES 兩個陣列，不需要動主題或樣板。
 *   1. 在 TOPICS（專題）或 NOTES（學習筆記）加一個物件：{ title, href }
 *   2. npx hexo clean && npx hexo generate，然後檢查 public/index.html。
 *   3. 導覽列另有兩個下拉群組（_config.fluid.yml 的 navbar.menu：專題、學習筆記），記得同步。
 *   4. 樣式在 source/css/custom.css（.home-resources-2col / .home-resources-title / .res-list）。
 *
 * ⚠️ 本目錄只能放 .js：Hexo 會嘗試載入 scripts/ 底下的「每一個」檔案，
 *    放了 .md 之類的檔案會在每次建置時噴 ERROR（Script load failed）。
 */

const MARKER = 'data-home-resources';

// 專題：長篇系列（source 底下 skip_render 的獨立靜態站），或單篇長文＋一手來源的入口
// 只輸出標題（連到系列總覽頁）；章節等子頁面入口由導覽列與各總覽頁提供
// 專題（首頁左欄）：每筆帶 date 欄位，輸出時由新到舊排序。
// date 用 ISO 日期字串（YYYY-MM-DD）；新增專題只要補上日期，順序自動對。
const TOPICS = [
  { title: 'CNN 專題：九篇圖解系列、課程筆記與實驗', href: '/cnn/', date: '2026-10-30' },
  { title: 'OCR：正體中文書頁辨識與校對', href: '/ocr/', date: '2026-10-28' },
  { title: 'CNN 專題：十個實驗，和三次被推翻的假設', href: '/cnn-lab/', date: '2026-10-27' },
  { title: 'gpu-unlock 專題：NVIDIA 消費級卡那道「半速鎖」怎麼被打開的', href: '/gpu-unlock/', date: '2026-10-25' },
  { title: '從零打造一個 coding agent', href: '/coding-agent/', date: '2026-10-11' },
  { title: '手寫程式碼的時代正式結束｜DHH 宣布退休', href: '/dhh-rails-world-2026/index.html', date: '2026-09-27' }
];

// 由新到舊（同一天依原順序穩定排序）。
const TOPICS_SORTED = TOPICS.map(function (item, i) { return { item: item, i: i }; })
  .sort(function (a, b) {
    if (a.item.date === b.item.date) return a.i - b.i;
    return a.item.date < b.item.date ? 1 : -1;
  })
  .map(function (x) { return x.item; });

// 學習筆記：課程／教材整理成的離線筆記，每份都有互動測驗
const NOTES = [
  { title: '電腦視覺課程', href: '/cv-course/' },
  { title: 'LLM 與生成式 AI 課程', href: '/llm-course/' },
  { title: 'AutoML 應用證書課程', href: '/automl-course/' }
];

// 左欄＝專題、右欄＝學習筆記；「文章」標題之後接主題產生的最新文章清單
//
// 2026-11-01：首頁不再顯示專題與學習筆記兩欄，只保留「文章」標題 + 卡片清單。
//   兩個入口改由頁頂導覽列的下拉式表單提供（_config.fluid.yml 的 navbar.menu：
//   `topics` / `notes` 兩個群組），因此首頁不需要重複列一次。
//
//   保留這個空陣列的用意：整支腳本（偵測首頁、注入「文章」標題、防重複注入）
//   都還在運作，要恢復兩欄時只要把 TOPICS / NOTES 的內容填回去即可，
//   不需要改任何其他檔案。COLUMNS 為空時 renderColumn 不會被呼叫。
//
//   ⚠️ source/css/custom.css 的 .home-resources-2col / .res-list 等樣式
//   暫時沒有使用者；恢復兩欄時會直接生效，所以先不刪。
const COLUMNS = [
  // { id: 'topics', icon: 'icon-books', title: '專題', items: TOPICS_SORTED },
  // { id: 'notes', icon: 'icon-notebook', title: '學習筆記', items: NOTES }
];

const ARTICLES = { id: 'articles', icon: 'icon-articles', title: '文章' };


function esc(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// 只輸出標題清單（沒有小標、簡介與膠囊連結）
function renderList(items) {
  const rows = items
    .map(item => `        <li><a href="${esc(item.href)}">${esc(item.title)}</a></li>`)
    .join('\n');

  return `      <ul class="res-list">\n${rows}\n      </ul>`;
}

function renderColumn(col) {
  return [
    `    <section class="home-resources-col" id="${col.id}" ${MARKER}="${col.id}">`,
    '      <h2 class="home-resources-title">',
    `        <i class="iconfont ${col.icon}" aria-hidden="true"></i><span>${esc(col.title)}</span>`,
    '      </h2>',
    renderList(col.items),
    '    </section>'
  ].join('\n');
}

function renderArticlesHeading() {
  return [
    `<section class="home-resources" id="${ARTICLES.id}" ${MARKER}="${ARTICLES.id}">`,
    '    <h2 class="home-resources-title">',
    `      <i class="iconfont ${ARTICLES.icon}" aria-hidden="true"></i><span>${esc(ARTICLES.title)}</span>`,
    '    </h2>',
    '  </section>'
  ].join('\n');
}

hexo.extend.filter.register('after_render:html', function (str) {
  if (typeof str !== 'string') return str;

  // 已經注入過（外層 layout.ejs 會再過一次同一個過濾器）
  if (str.indexOf(MARKER) !== -1) return str;

  // 只認首頁的文章清單：目前全站只有 index.ejs 產出的首頁有這個標記
  const anchor = '<div class="row mx-auto index-card">';
  const index = str.indexOf(anchor);
  if (index === -1) return str;

  const block = [
    // COLUMNS 目前是空的（首頁不顯示專題／學習筆記兩欄），
    // 空陣列時連外層 .home-resources-2col 都不輸出，避免留下一塊
    // 帶 2.5rem 下邊距的空白。
    ...(COLUMNS.length
      ? ['  <div class="home-resources-2col">',
         COLUMNS.map(renderColumn).join('\n'),
         '  </div>']
      : []),
    '  ' + renderArticlesHeading()
  ].join('\n');

  this.log.info(
    'home-resources: 首頁已注入（專題 %d / 學習筆記 %d / 文章清單由主題輸出）',
    COLUMNS.length ? TOPICS.length : 0,
    COLUMNS.length ? NOTES.length : 0
  );

  return `${str.slice(0, index)}${block}\n\n  ${str.slice(index)}`;
});

