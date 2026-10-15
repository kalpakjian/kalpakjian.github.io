'use strict';

/**
 * 首頁資源總覽：文章 / 專題 / 學習筆記
 *
 * 為什麼需要這支腳本：
 *   Fluid 主題的 layout/index.ejs 只會輸出「文章卡片清單」，首頁完全沒有專題與學習筆記的入口；
 *   主題的 theme.custom_html 雖然可以塞 HTML，但那是「全站每一頁」都會輸出，不適合。
 *   所以這裡用 Hexo 原生支援的 scripts/ 目錄註冊 after_render:html 過濾器：
 *   只在首頁（index.ejs 產出的文章清單之前）注入兩個區塊 + 一個「文章」標題，其他頁面完全不動。
 *
 * 偵測方式（不依賴主題內部路徑）：
 *   1. 只處理含 `<div class="row mx-auto index-card">` 的 HTML（目前全站只有 public/index.html 有）。
 *   2. 用 data-home-resources 標記避免重複注入（layout.ejs 外層會再過一次同一個過濾器）。
 *
 * 維護方式：只要改下面的 TOPICS / NOTES 兩個陣列，不需要動主題或樣板。
 *   1. 在 TOPICS（專題）或 NOTES（學習筆記）加一個物件：
 *      { kicker, title, href, desc, links: [{ label, href }] }
 *   2. npx hexo clean && npx hexo generate，然後檢查 public/index.html。
 *   3. 導覽列另有兩個下拉群組（_config.fluid.yml 的 navbar.menu：專題、學習筆記），記得同步。
 *   4. 樣式在 source/css/custom.css（.home-resources / .res-card / .res-link）。
 *
 * ⚠️ 本目錄只能放 .js：Hexo 會嘗試載入 scripts/ 底下的「每一個」檔案，
 *    放了 .md 之類的檔案會在每次建置時噴 ERROR（Script load failed）。
 */

const MARKER = 'data-home-resources';

// 專題：長篇系列（source 底下 skip_render 的獨立靜態站）
const TOPICS = [
  {
    kicker: 'Rails World 2026 開幕演講',
    title: '手寫程式碼的時代正式結束｜DHH 宣布退休',
    href: '/dhh-rails-world-2026/index.html',
    desc:
      'DHH 在 Rails World 2026 宣布：他從 2026 年 3 月起不再手寫程式碼，37signals 全公司跟進，' +
      '「手寫」變成要修的 bug。整場演講的十大重點、時間線與關鍵數字，以及台灣團隊躲不掉的三個問題。',
    links: [
      { label: '總覽', href: '/dhh-rails-world-2026/index.html' },
      { label: '全文整理', href: '/dhh-rails-world-2026/article.html' },
      { label: '時間線與數字', href: '/dhh-rails-world-2026/timeline.html' },
      { label: '三個問題', href: '/dhh-rails-world-2026/questions.html' }
    ]
  },
  {
    kicker: 'Coding Agent Harness · 八章',
    title: '從零打造一個 coding agent',
    href: '/coding-agent/',
    desc:
      '六個零件、一個迴圈，與 Ralph 迴圈真正的位置。把任何 coding agent 拆成模型／工具／迴圈／' +
      'Context 管理器／護欄／驗證器，附約 90 行可跑的 Python 骨架，再用 Cline CLI 與 Pi 兩個開源 ' +
      'harness 對照，並補上接上本地模型的八次實測。',
    links: [
      { label: '總覽', href: '/coding-agent/' },
      { label: '01 六個零件', href: '/coding-agent/ch01-six-parts.html' },
      { label: '03 護欄與驗證', href: '/coding-agent/ch03-guardrails-verify.html' },
      { label: '06 一手實測', href: '/coding-agent/ch06-experiment.html' },
      { label: '08 結語', href: '/coding-agent/ch08-standard.html' },
      { label: '導讀文章', href: '/2026/10/11/building-a-coding-agent/' }
    ]
  }
];

// 學習筆記：課程／教材整理成的離線筆記，每份都有互動測驗
const NOTES = [
  {
    kicker: 'IVDC · 電腦視覺課程',
    title: 'IVDC 電腦視覺課程 學習筆記',
    href: '/cv-course/',
    desc:
      '6 份可離線閱讀的學習筆記：AI 導論、Local GPU、電腦視覺導論、OpenCV、Responsible AI、' +
      '神經網路與機器學習。每份都附 60 題互動 MC 測驗，程式碼與數字都在本機實測（RTX 4090）。',
    links: [
      { label: '課程總覽', href: '/cv-course/' },
      { label: 'AI 導論', href: '/ai-intro-notes/' },
      { label: 'Local GPU', href: '/local-gpu-ml-notes/' },
      { label: '電腦視覺導論', href: '/cv-intro-notes/' },
      { label: 'OpenCV', href: '/opencv-notes/' },
      { label: 'Responsible AI', href: '/responsible-ai-notes/' },
      { label: '神經網路與 ML', href: '/neural-network-notes/' }
    ]
  },
  {
    kicker: 'IVDC · LLM 與生成式 AI 課程',
    title: 'IVDC LLM 與生成式 AI 課程 學習筆記',
    href: '/llm-course/',
    desc:
      '7 份可離線閱讀的學習筆記：Popular LLM、LLM 理論、Prompt Engineering、Hugging Face、' +
      'Local LLM Apps、LiteLLM、Streamlit & Flask。所有 Lab 都在本機實測，並標出課程與現行版本的落差。',
    links: [
      { label: '課程總覽', href: '/llm-course/' },
      { label: 'Popular LLM', href: '/popular-llm-notes/' },
      { label: 'LLM 理論', href: '/llm-intro-notes/' },
      { label: 'Prompt Engineering', href: '/prompt-engineering-notes/' },
      { label: 'Hugging Face', href: '/huggingface-notes/' },
      { label: 'Local LLM Apps', href: '/local-llm-notes/' },
      { label: 'LiteLLM', href: '/litellm-notes/' },
      { label: 'Streamlit & Flask', href: '/streamlit-flask-notes/' }
    ]
  },
  {
    kicker: 'AutoML · 四單元 100 頁',
    title: 'AutoML 應用證書課程 學習筆記',
    href: '/automl-course/',
    desc:
      '四個單元、100 頁課程整理成一份可離線閱讀的學習筆記：AutoML 基礎與 AI 倫理、核心算法與模型評估、' +
      'Azure ML Studio 實戰、開源工具（Colab + TPOT）。60 頁 SmartArt 圖表已還原成可搜尋的文字。',
    links: [
      { label: '課程總覽', href: '/automl-course/' },
      { label: '學習筆記', href: '/automl-notes/' },
      { label: '互動測驗 60 題', href: '/automl-notes/mc-quiz.html' }
    ]
  }
];

// 三個區塊的標題（順序：專題 → 學習筆記 → 文章）
const GROUPS = [
  {
    id: 'topics',
    icon: 'icon-books',
    title: '專題',
    sub: '長期更新的系列：把一個題目從頭寫到尾，每一章都能單獨連結。',
    cards: TOPICS
  },
  {
    id: 'notes',
    icon: 'icon-notebook',
    title: '學習筆記',
    sub: '課程與教材整理成的離線筆記，每份都附互動測驗與本機實測數據。',
    cards: NOTES
  },
  {
    id: 'articles',
    icon: 'icon-articles',
    title: '文章',
    sub: '最新發佈的文章，依時間排序。',
    cards: []
  }
];


function esc(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function renderCard(card) {
  const links = (card.links || [])
    .map(link => `<a class="res-link" href="${esc(link.href)}">${esc(link.label)}</a>`)
    .join('\n          ');

  return [
    '      <article class="res-card">',
    card.kicker ? `        <span class="res-kicker">${esc(card.kicker)}</span>` : '',
    `        <h3 class="res-title"><a href="${esc(card.href)}">${esc(card.title)}</a></h3>`,
    `        <p class="res-desc">${esc(card.desc)}</p>`,
    links ? `        <div class="res-links">\n          ${links}\n        </div>` : '',
    '      </article>'
  ].filter(Boolean).join('\n');
}

function renderGroup(group) {
  const cards = group.cards.map(renderCard).join('\n');
  const grid = cards ? `\n    <div class="home-resources-grid">\n${cards}\n    </div>` : '';

  return [
    `<section class="home-resources" id="${group.id}" ${MARKER}="${group.id}">`,
    '    <h2 class="home-resources-title">',
    `      <i class="iconfont ${group.icon}" aria-hidden="true"></i><span>${esc(group.title)}</span>`,
    '    </h2>',
    `    <p class="home-resources-sub">${esc(group.sub)}</p>${grid}`,
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

  const block = GROUPS.map(renderGroup).join('\n\n  ');

  this.log.debug(
    'home-resources: 首頁資源總覽已注入（專題 %d / 學習筆記 %d）',
    TOPICS.length,
    NOTES.length
  );

  return `${str.slice(0, index)}${block}\n\n  ${str.slice(index)}`;
});

