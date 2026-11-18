---
title: 稽核 1,499 張 CC0 人像圖庫：ai-portrait-gallery 做對了什麼，又卡住了誰
date: 2026-11-18 20:00:00
categories:
  - AI 研究札記
tags:
  - ai-portrait-gallery
  - CC0
  - 網站稽核
  - 無障礙
  - WCAG
  - Core Web Vitals
  - SEO
  - Cloudflare Pages
  - Playwright
index_img: /img/covers/ai-portrait-gallery-audit-zh.png
banner_img: /img/covers/ai-portrait-gallery-audit-zh.png
---

有人在社群貼了一個網址：[ai-portrait-gallery.pages.dev](https://ai-portrait-gallery.pages.dev/)，只丟連結、沒有說明。這種貼法通常兩個意思之一——「這個我要照著做」或「這個壞了」。實際打開是前者：一個日本人做的 AI 人像參考圖庫，<strong>1,499 張</strong>圖、CC0 授權、不用註冊、沒有後端框架。

做得相當好。然後我把它當成一份待稽核的程式碼看了一遍——不是讀原始碼（站方沒有公開 repo），而是把它的靜態檔抓下來讀，再用無頭 Chromium 真的去按鍵盤、量對比度、記時間軸。結論是：<strong>視覺與文案接近專業水準，但無障礙與可被搜尋這兩件事上有幾個結構性缺口，其中一個會讓鍵盤使用者直接少掉 606 張圖。</strong>

以下是完整稽核。所有數字都是 2026-11-18 當天實測，重現方式寫在第六節。

<!-- more -->

> <strong>一句話總結</strong>：這是一個完成度很高的單頁圖庫，值得當「無建置步驟、純三檔」的範本抄；<br />
> 但它的 tab 分頁只做了一半——未選中的分頁 `tabIndex = -1` 而沒有任何方向鍵處理，<br />
> 所以「スタイリング」分頁和 4 個排行分類<strong>用鍵盤永遠按不到</strong>。<br />
> 這是 WCAG 2.1.1（Level A）等級的問題，修起來卻只要十行。

## 三十秒結論

| 問題 | 一句話回答 |
|---|---|
| **這是什麼站** | 日本營運者「あぎ」做的免費 AI 人像參考圖庫，1,499 張（フェイス 893 ／ スタイリング 606），CC0 1.0 |
| **解決什麼問題** | AI 生成圖片／影片時，用同一張參考圖把角色的臉固定成同一個人 |
| **技術構成** | Cloudflare Pages ＋ Pages Functions（`/api/ranking`、`/api/hit`）＋ 三個靜態檔，沒有打包、沒有框架 |
| **最嚴重問題** | 鍵盤到不了「スタイリング」分頁與 4 個排行分類（`tabIndex = -1` 且無方向鍵處理） |
| **第二嚴重** | `hidden` 屬性在 `.btn`／`.seg` 上完全失效——CSS `display` 覆蓋了瀏覽器預設，造成一個永遠顯示的無效按鈕 |
| **效能最重的一項** | 不是圖片，是 Google Fonts 的 **145 KB render-blocking CSS**（621 條 `@font-face`、497 個 woff2） |
| **對搜尋引擎** | 近乎隱形：沒有 `og:image`、沒有 `robots.txt`、沒有 `sitemap.xml`，1,499 張圖沒有任何可爬的網址 |
| **值得抄的地方** | 零建置、深淺色主題、`prefers-reduced-motion`、`width`/`height` 全給（CLS 0）、console 零錯誤 |

## 一、先確認它到底是什麼

| 項目 | 實測值 |
|---|---|
| 圖片總數 | 1,499 |
| フェイス（正面、素背景，對臉用） | 893 |
| スタイリング（含服裝、髮質、氛圍） | 606 |
| 縮圖 | 400×500 WebP，單張約 19 KB（最大 20.8 KB） |
| 原圖 | 1122×1402 PNG，1.9–2.3 MB |
| 髮型分類 | ショート 727 ／ ミディアム 376 ／ セミロング 260 ／ ロング 136 |
| 授權 | CC0 1.0，商用可、可改、不需署名 |
| 人物 | 全部 AI 生成的虛構人物，站方明言不冒充真人 |

技術上是三個檔案加兩支 API：

| 檔案 | 原始大小 | Brotli 後 |
|---|---|---|
| `data/images.js`（1,499 筆記錄） | 456,477 B | **32.3 KB** |
| `assets/app.js`（全部邏輯） | 14,961 B | **5.0 KB** |
| `assets/style.css` | 19,381 B | **5.0 KB** |

`/api/ranking` 回 200 與即時 JSON（內容與靜態 `data/ranking.js` 不同，代表排行真的在更新），`/api/hit` 回 204。資料面抽樣 25 筆 × 縮圖＋原圖共 50 個檔案，全部 200 且 `Content-Type` 正確。**沒有缺失的圖片。**

先說清楚：站方沒有公開原始碼，所以以下全部是<strong>從外部可觀測行為</strong>反推的結論，不是讀 code review 得來的。


## 二、先講做對的部分

稽核文最容易寫成負評，但這個站在「一個獨立開發者、零依賴」的前提下，完成度明顯高於平均值：

| 項目 | 實測結果 |
|---|---|
| Console 錯誤 | **0**（`console` error/warning 空、`pageerror` 空、失敗請求空） |
| 累積版面位移（CLS） | 來源就在 `img` 一律帶 `width`/`height`——縮圖與燈箱都沒有尺寸跳動 |
| 深色模式 | `prefers-color-scheme` 完整實作，不是只換背景色 |
| 動態偏好 | `prefers-reduced-motion` 一行 `* { transition: none !important }` 全關，寫法正確 |
| 焦點樣式 | 10 處 `:focus-visible`，沒有用 `outline: none` 偷偷關掉 |
| 圖片載入 | `loading="lazy"` ＋ `decoding="async"` ＋ 首屏 hero 圖 `fetchPriority="high"` |
| 失敗降級 | `/api/ranking` 3 秒逾時就退回靜態 `ranking.js`，且用 `rankDone` 守衛避免雙寫 |
| 統計 | `/api/hit` 用 `sendBeacon` 且整段 try/catch，打不出去也不影響操作 |
| 行動版 | 390 px 寬實測 `scrollWidth = clientWidth`，無橫向溢出 |

還有一個細節值得指出：它的無限滾動用 `IntersectionObserver` 觀察 `#sentinel`、`rootMargin: 400px` 預取，同時保留手動「もっと見る」按鈕當後備。這比純滾動載入穩健——只是那個按鈕後來壞了（下一節）。

內文的 `<dl>` 統計、`aria-hidden` 的裝飾性 SVG、每一個純圖示按鈕都有日文 `aria-label`——這些都不是模板能自動長出來的東西。

## 三、四個讓人卡住的錯

### 3.1 鍵盤使用者到不了「スタイリング」

這是整份稽核裡唯一我會用「阻斷級」形容的問題。

站上的分頁切換是 `role="tablist"` ＋ `role="tab"`，實作了 roving tabindex：

```js
t.setAttribute("aria-selected", on ? "true" : "false");
t.tabIndex = on ? 0 : -1;
```

未選中的分頁 `tabIndex = -1`，這本身是標準做法——<strong>前提是你必須同時實作方向鍵</strong>。而 `app.js` 全文只有一個 `keydown` 監聽器，只管燈箱的 Escape 與左右鍵，兩個 tablist 都沒接方向鍵。

實測（Chromium，焦點放在「フェイス」分頁）：

```
按 Tab        → { id: "", cls: "chip", text: "すべて 893" }   ← 直接跳到篩選 chip
按 ArrowRight → { id: "tab-face" }                            ← 沒有任何反應
```

結果是：<strong>「スタイリング」分頁用鍵盤永遠按不到</strong>，因為它 `tabIndex=-1`，而唯一能把焦點移過去的方式是方向鍵——偏偏沒接。排行區的 5 個分類同理，第 2 到第 5 個（ショート、ミディアム、セミロング、ロング）全部 `tabIndex=-1`。

以圖片數算，606 張（40%）的內容對純鍵盤使用者是關閉的。這是 WCAG 2.1.1 Keyboard，Level A。

修法是把 roving tabindex 補完，大約十行：

```js
function rovingKeys(list) {
  list.addEventListener("keydown", function (e) {
    var tabs = [].slice.call(list.querySelectorAll('[role="tab"]'));
    var i = tabs.indexOf(document.activeElement);
    if (i < 0) return;
    var n = e.key === "ArrowRight" ? i + 1 : e.key === "ArrowLeft" ? i - 1
          : e.key === "Home" ? 0 : e.key === "End" ? tabs.length - 1 : -1;
    if (n < 0) return;
    e.preventDefault();
    tabs[(n + tabs.length) % tabs.length].click();   // click 會連帶更新 tabIndex
  });
}
```

### 3.2 `hidden` 屬性在這兩個控制項上完全失效

這個 bug 很隱蔽，但影響是真的使用者。

HTML 的 `hidden` 屬性靠瀏覽器預設樣式表 `[hidden] { display: none }` 生效——而<strong>作者樣式的優先級高於瀏覽器預設樣式</strong>。這個站的 `.btn` 設了 `display: inline-block`、`.seg` 設了 `display: inline-flex`，於是 `hidden` 直接被覆蓋。

實測（執行時動態加上 `hidden`）：

```
#more.btn         → display: inline-block, rendered: true
#tab-styling.seg  → display: flex,         rendered: true
```

後果是「もっと見る」按鈕永遠顯示。程式裡明明寫了 `moreBtn.hidden = shown >= filtered.length`，但那個賦值不會有任何視覺效果。當某個篩選結果少於 60 張（或全部載完之後），畫面上仍掛著一顆按鈕，按下去什麼都不會發生——`showMore()` 算出的 `end = shown`，迴圈連一次都不跑。

一行 CSS 就能修：

```css
[hidden] { display: none !important; }
```

同一個原因也讓 `if (!secItems(sec).length) t.hidden = true` 失去意義（目前兩個分頁都有資料，所以還沒炸）。

### 3.3 燈箱宣告了 `aria-modal`，卻沒有 modal 該有的行為

燈箱是 `<div role="dialog" aria-modal="true">`，開關用 `hidden`。Escape 關閉、關閉後把焦點還回原本的元素，這兩件事都做對了。少的是**把焦點關在裡面**：

```
按 Tab 的軌跡：
[lb]lb-close → [lb]lb-prev → [lb]lb-next → [lb]lb-dl → [lb]lb-line
→ [BEHIND]BODY → [BEHIND]brand → [BEHIND]A → [BEHIND]A
```

焦點走出燈箱，進到背後 734 個節點的文件裡。對螢幕閱讀器使用者來說，`aria-modal="true"` 的意義是「外面不存在」——但實際上外面不但存在，還可以被 Tab 到。這個宣告變成一句謊話，比不宣告更糟。

修法不需要自己寫 focus trap，用 `inert`（現代瀏覽器全支援）：

```js
["header.site-header", "main", ".community", "footer.site-footer"]
  .forEach(function (s) {
    var el = document.querySelector(s);
    if (el) el.inert = true;        // 關閉時設回 false
  });
```

### 3.4 對搜尋引擎近乎隱形

這是「明明有 1,499 張獨特圖片，卻一張都不會被 Google 圖片搜到」的情況。

<strong>第一，社群分享卡片是空的。</strong>`<head>` 只有 `og:title` 與 `og:description`。實測：

```
og:type = null   og:image = null   og:url = null
twitter:card = null   twitter:image = null
```

這個站的推廣管道是 X（`@agi_aibusi`）和 LINE オープンチャット——兩個都靠連結預覽。沒有 `og:image`，貼出去就是一串裸連結。這是整份清單裡投入產出比最高的一項：四個 meta 標籤。

<strong>第二，所有不存在的網址都回 200 加首頁。</strong>

```
/robots.txt                  → 200 text/html（9,121 B，就是首頁）
/sitemap.xml                 → 200 text/html
/random-nonsense-xyz         → 200 text/html
/assets/nope.js              → 200 text/html
/img/thumb/doesnotexist.webp → 200 text/html
```

Cloudflare Pages 的 SPA catch-all。三個後果：`robots.txt` 和 `sitemap.xml` 表面存在、內容是 HTML（爬蟲要嘛忽略、要嘛當錯誤）；每一個打錯的網址都變成首頁的可索引重複副本；**缺少的圖片不會 404**——`<img>` 拿到 HTML 只顯示破圖，而 `download` 連結指向缺少的檔案時，使用者會得到一個改名成 `.png` 的 HTML 檔。

我抽樣 50 個引用檔案全部存在，所以這條目前是「潛在」而非「正在發生」；但只要建置流程漏掉一個檔案，它就會靜默失敗，站上沒有任何機制會通報。

<strong>第三，1,499 張圖沒有任何可爬的網址。</strong>圖庫完全由 JavaScript 生成，伺服器送出的 HTML 裡沒有半個 `<img>`。而且 60 張圖只有 **6 種 `alt` 字串**（`AI生成の架空の人物（ショート）` 之類），因為 `alt` 是用髮型拼出來的，同一髮型的每張圖 alt 都一樣——資訊量等於零，還和外層按鈕的 `aria-label` 重複朗讀一次。


## 四、效能：最重的資源不是圖片

直覺會以為圖片庫的瓶頸在圖片。這個站不是。

首頁載入（未節流）共 32 個請求、673 KB、734 個 DOM 節點。其中最重的一項：

| 資源 | 傳輸量 |
|---|---|
| `fonts.googleapis.com/css2?family=Noto+Serif+JP…` | **145 KB** |
| `data/images.js` | 32.3 KB |
| 最大的一張縮圖（共 29 張） | 20.8 KB |
| `assets/app.js` | 5.0 KB |
| `assets/style.css` | 5.0 KB |

那個 Google Fonts 網址回傳的是 **570,005 bytes 的純文字 CSS**，內含 **621 條 `@font-face`、497 個不同的 woff2 網址**（依 unicode-range 切子集）。它是 `<head>` 裡的 render-blocking `<link rel="stylesheet">`，所以首屏必須先等第三方 DNS＋TLS＋一個 RTT，再解析 621 條規則。本機實測 `start: 86 ms → end: 201 ms`，行動網路會放大好幾倍。

節流行動（4× CPU、1.6 Mbps、RTT 150 ms）實測：

| 指標 | 值 |
|---|---|
| FCP | 1,688 ms |
| load | 5,997 ms |
| 傳輸量 | 414 KB / 20 requests |

字型策略上，這個站用了三個家族：`Noto Serif JP`（標題）、`Zen Kaku Gothic New`（正文）、`Cormorant Garamond`（眉標與排行數字）。<strong>其中兩個是 CJK</strong>，而 CJK 字型的子集 CSS 天生龐大。

代價最高、最省事的順序是：先砍掉 `Cormorant Garamond`，把 `--latin` 指到系統襯線體（這個字型只出現在「Free Face Reference Library」「総合」這種短字串上）；剩下的兩個 CJK 家族若要留，用 `pyftsubset` 依實際用字裁切後自架——這個站的文案是靜態且很短的，幾百個字符就夠，成品會是一張個位數 KB 的 woff2，而且沒有第三方網域。

其他三項效能問題：

| 問題 | 實測 | 影響 |
|---|---|---|
| **快取標頭** | 全部資源 `Cache-Control: public, max-age=0, must-revalidate`，包含 `/img/**` | 檔名是內容雜湊（`f71f980dde3.webp`）永不改變的圖，回訪仍要逐張回伺服器驗證；一個 session 要驗證 30–60 張 |
| **燈箱只載縮圖** | 1440×900 視窗下：`naturalSize [400,500]`、`renderedCss [400,500]` | 站上文案說「下載原始 PNG 才能看清細節」，但預覽本身就卡在 400 px 寬 |
| **縮圖只有一種尺寸** | `thumb_w` 全部 400；390 px 寬時網格是兩欄，每張卡片約 180 px | 手機下載 400 px 的檔案顯示在 180 px 的格子裡，首屏 29 張共 481 KB |

燈箱那項特別值得講，因為它是「功能做出來了、但用不到」的典型：`lbImg.src = it.thumb`，一次都沒用過原圖。原圖是 1122×1402，只差一行 `img.onload` 之後換 `src` 就能漸進升級。

## 五、對比度：四個數字不合格

用 CSS 變數算出來的實際比值（WCAG AA 正文要求 4.5:1、非文字介面元素 3:1）：

| 元素 | 顏色 | 比值 | 門檻 |
|---|---|---|---|
| `.count`、`.card .label`、`.sec-note`、`.empty`、未選中的 `.seg` | `--muted #7a736b` on `--bg #f6f3ee` | **4.22** | 4.5 |
| `.chip small`（`opacity: .6` 疊在 `--fg` 上）→ `#74716e` | on `#f6f3ee` | **4.38** | 4.5 |
| 排行第 1 名徽章 | `#fff` on `--rose #c98b7f` | **2.81** | 4.5 |
| 焦點外框 `outline: 2px solid var(--rose)` | `#c98b7f` on `#f6f3ee`／`#fffdf9` | **2.54／2.76** | 3.0 |

`--muted` 被用在最關鍵的兩個位置：未選中的分頁標籤（主要導覽）與每張縮圖下方的唯一說明文字。深色模式反而全部合格（6.21–8.37），唯一例外是同一個第 1 名徽章：`#fff` on `--rose #d9a294` = **2.20**。

把 `--muted` 調深到 `#6f6860`（4.6:1）、焦點外框換成 `#a8635a`（≥3:1），徽章改成 `--fg` 疊 `--rose`，四個問題一次解決。

還有三個較小但真實的問題：

- **tab 的 ARIA 宣告不完整**：`aria-controls="grid"` 指向的 `#grid` 是個沒有 `role`、沒有 `tabindex` 的 `<ul>`，不是 `tabpanel`。半套 widget 比不宣告更難修。
- **`#count` 每次滾動都朗讀**：`aria-live="polite"` ＋ 每批載入都呼叫 `updateCount()`，螢幕閱讀器每滾一段就重念一次「フェイス 全893枚 / 表示中 180枚」。
- **`hidden` 之外還有一個 `hidden` 失效的潛在點**：空分頁的隱藏 guard 同樣無效（見 3.2）。

## 六、怎麼重現

全部結論都可以自己跑一次。我用的是本機既有的 Playwright `chromium-1248`：

```js
import { chromium } from 'file:///C:/Users/princ/AppData/Roaming/npm/node_modules/openclaw/node_modules/playwright-core/index.mjs';
const browser = await chromium.launch({
  headless: true,
  executablePath: 'C:/Users/princ/AppData/Local/ms-playwright/chromium-1248/chrome-win64/chrome.exe',
});
const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
await page.goto('https://ai-portrait-gallery.pages.dev/', { waitUntil: 'load' });

// 3.1 鍵盤能不能到 styling？
await page.evaluate(() => document.getElementById('tab-face').focus());
await page.keyboard.press('ArrowRight');
console.log(await page.evaluate(() => document.activeElement.id));   // 仍是 tab-face

// 3.2 hidden 到底有沒有用？
console.log(await page.evaluate(() => {
  const el = document.getElementById('more');
  el.setAttribute('hidden', '');
  return [getComputedStyle(el).display, el.getBoundingClientRect().height > 0];
}));                                                                 // ["inline-block", true]

// 3.3 焦點會不會跑出燈箱？
await page.evaluate(() => document.querySelector('#grid .thumb-btn').click());
for (let i = 0; i < 6; i++) {
  await page.keyboard.press('Tab');
  console.log(await page.evaluate(() =>
    (document.activeElement.closest('#lightbox') ? '[lb]' : '[BEHIND]') + document.activeElement.id));
}
```

節流量測走 CDP 的 `Emulation.setCPUThrottlingRate`（4）＋ `Network.emulateNetworkConditions`（1.6 Mbps、RTT 150 ms）。

有一件事要提醒：`FCP` 在快取暖機後會落在 384–888 ms 之間跳動，單跑一次就引用很容易誤導。上面那個 1,688 ms 是節流下的數字，比較能代表真實手機。

修法的最小版本：建置時為每一筆記錄輸出 `/i/<id>.html`，帶 `og:image`、髮型／風格文字與回首頁的連結，再產一份真的 `sitemap.xml`。產 `data/images.js` 的那個迴圈已經在手上了，同一圈就能生頁面。


## 七、實際下載一次：使用者視角

前面幾節都是站在外面量。這一節換成使用者：從首頁開始，只做一件事——下載一張圖。全程 6.6 秒、六個動作。

| # | 動作 | 實測結果 |
|---|---|---|
| 1 | 開首頁 | HTTP 200，`<title>` = `AIモデル顔データベース` |
| 2 | 按「ギャラリーを見る」 | 網址變 `#gallery`，フェイス 分頁，DOM 出現 60 張卡片 |
| 3 | 按髮型 chip「ミディアム」 | 網址被寫入 `#hair=…`（髮型的 percent-encoding），計數器變「フェイス 全893枚 / 表示中 229枚」 |
| 4 | 點第一張縮圖 | 燈箱開啟，載入 `img/thumb/f0ed328cb48.webp` |
| 5 | 按「ダウンロード」 | 瀏覽器存成 `ai-face-f0ed328cb48.png`，2,087,247 bytes |
| 6 | 檢查檔案 | PNG 標頭 `89504e470d0a1a0a`，<strong>1122×1402</strong>，1.99 MB |

第 3 步的網址實際長這樣：`#hair=%E3%83%9F%E3%83%87%E3%82%A3%E3%82%A2%E3%83%A0`。它同時也是這個站的主要導覽機制——所有篩選狀態都寫進 hash，所以可以直接貼給別人。壞處是分享出去的連結沒人看得懂，而且中文／日文使用者看到的是一串 percent-encoding。

chip 數字是<strong>依分頁分開統計</strong>的：フェイス 底下是 ショート 433／ミディアム 229／セミロング 154／ロング 77，加起來剛好 893；開頭提到的 727／376／260／136 則是兩個分頁的合計。同一個站上兩組數字，第一次看會以為自己記錯。

按下去之後，才看得到的四件事：

<strong>一、檔名是網站幫你取的，而且取得很好。</strong>存下來的不是 `f0ed328cb48.png`，而是 `ai-face-f0ed328cb48.png`——因為連結帶了 `download="ai-face-<id>.png"` 屬性。存十張不會撞名，也不會變成 `ai-face-(1).png`。這種小事多數圖庫都不做。

<strong>二、燈箱的說明文字比圖還大。</strong>燈箱字幕寫「ミディアム・2wayバングのワンカールミディアムボブ（2.0 MB）」，但畫面上那張是 400×500 的縮圖、19 KB。想看清細節必須先下載——可是多數人在看到 400 px 的圖時，就已經決定要不要下載了。這是第四節效能表裡「燈箱只載縮圖」那條的實際體感。

<figure>
<img src="/img/ai-portrait-gallery-audit-zh/lightbox.png" alt="燈箱預覽：在 1280×900 的視窗中置中顯示 400×500 的縮圖，下方字幕標示 2.0 MB" style="width:100%;border-radius:12px" />
<figcaption>圖 1：1280×900 的視窗裡，燈箱置中顯示的是 400×500、19 KB 的縮圖；字幕卻標「2.0 MB」。</figcaption>
</figure>

<strong>三、計數器寫「表示中 893 枚」，但 DOM 裡只有 60 張。</strong>這是寫這一節、真的按下去才發現的第五個問題：`updateCount()` 用的是 `filtered.length`（篩選後的總數），不是 `shown`（真正渲染出來的張數）。標籤寫「表示中」卻永遠顯示總數，只有把 229 張全部滾完之後，兩個數字才會剛好一致。對使用者的意思很具體：你不知道還要滾多久。

<strong>四、滾完 229 張之後，「もっと見る」還在。</strong>這就是 3.2 那個 `hidden` 失效的真實症狀——已經載到最後一張了，按鈕仍然掛在頁面底部，按下去沒有任何反應。

最後是下載到的那張圖本身。原檔照原樣放進來，沒有壓縮、沒有裁切：

<figure>
<img src="/img/ai-portrait-gallery-audit-zh/face-sample.png" alt="實際下載的參考圖：1122×1402 的正面人像，AI 生成的虛構人物，CC0 1.0 授權" style="width:100%;max-width:460px;border-radius:12px" />
<figcaption>圖 2：實際下載的檔案 <code>ai-face-f0ed328cb48.png</code>，1122×1402、2.0 MB。站方以 CC0 1.0 發佈，不需署名。</figcaption>
</figure>

> <strong>關於這張圖</strong>：站方規則是「CC0 可自由使用，但請不要重新散布圖片本身」。本文放的是實際下載的原始檔案，用途是記錄這個圖庫的產出品質，不是轉載圖庫。<br />
> 你要用的話，直接回原站下載比較好——順便讓站方的下載排行反映真實需求。

## 八、實務結論

### 如果你是這個站的主人

按「影響 ÷ 工時」排，前五項是：

| # | 改動 | 工時 | 換到什麼 |
|---|---|---|---|
| 1 | `#sections` 與 `#rank-tabs` 補上方向鍵處理 | ~10 行 | 606 張圖不再是滑鼠專屬（3.1，Level A 阻斷級） |
| 2 | `[hidden] { display: none !important; }` | 1 行 | 修掉那顆永遠顯示的無效「もっと見る」 |
| 3 | 燈箱開啟時對背景加 `inert` | 2 行 | modal 真的像 modal |
| 4 | `og:image`／`og:type`／`og:url`／`twitter:card` | 4 個標籤 | 在 X 和 LINE 上終於有預覽卡片 |
| 5 | `--muted` 與焦點外框各改一個色值 | 2 個值 | 四個對比度問題一次補到 AA |

接下來才是字型堆疊（效能最大單筆）與「每張圖一頁」的靜態化（唯一能帶來自然圖片流量的路）。

### 如果你是想抄這個架構的人

值得抄的：

- **零建置**。三個檔、沒有 bundler、沒有框架，`data/images.js` 就是一個 `window.GALLERY_IMAGES = [...]`。改一個字推上去就生效，這對個人站是巨大優勢。
- **資料與程式分離**。圖片清單是純資料檔，前端只負責渲染。想換資料源（改成 API、改成 CDN JSON）不用碰渲染邏輯。
- **失敗一律降級，不報錯**。統計打不出去、排行 API 逾時，畫面照常運作。
- **`width`/`height` 全給**。這是 CLS 為 0 的唯一原因，也是最常被忽略的一行。

不要抄的：

- **只做一半的 ARIA widget**。`role="tablist"` 一旦寫下去，方向鍵就是義務，不是加分項。沒把握就退回 `<button>` ＋ `aria-pressed`——那是無障礙的合法解，而且不會騙人。
- **在 `<head>` 掛 Google Fonts 的 CJK 家族**。145 KB 的阻塞 CSS 比整站 JavaScript 大三倍。
- **對 SPA catch-all 不加例外**。`/img/**` 一定要能 404，否則你的建置錯誤永遠不會被發現。
- **用內容雜湊檔名卻不快取**。`max-age=0` ＋ 唯一檔名是「兩邊的缺點都拿」。

## 九、查證與限制

這份稽核有幾個明確的邊界，講清楚比較誠實：

| 項目 | 狀態 |
|---|---|
| 原始碼 | **沒有拿到**。站方未公開 repo，全部結論來自外部可觀測行為（HTML／JS／CSS／HTTP 標頭／瀏覽器實測） |
| 對比度 | 從 CSS 變數計算，<strong>未涵蓋「文字疊在圖片上」</strong>的情況 |
| 自動化稽核 | **沒有跑 axe／Lighthouse**（本機未安裝）。3.1–3.4 全部是針對性手測，不是完整掃描 |
| 圖片完整性 | 抽樣 25 筆 × 縮圖＋原圖 = 50 個檔案，**全部存在**；未逐一驗證 2,998 個檔案 |
| 時間數字 | 單機單次、有快取影響；節流數字才具參考性 |
| 站方意圖 | 效能與 SEO 的取捨（例如刻意不讓圖被索引以呼應「請勿轉載」的請求）**有可能是有意的**，我無法區分 |

## 十、延伸

| 項目 | 網址 |
|---|---|
| 被稽核的站 | [ai-portrait-gallery.pages.dev](https://ai-portrait-gallery.pages.dev/) |
| 營運者 | [@agi_aibusi](https://x.com/agi_aibusi) |
| 授權條款 | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/deed.ja) |
| WCAG 2.1.1 Keyboard | [理解 2.1.1](https://www.w3.org/WAI/WCAG21/Understanding/keyboard.html) |
| 對比度計算 | [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) |

> <strong>查證說明</strong>：所有數字於 2026-11-18 直接對線上站台實測（Chromium 1248 ＋ curl），<br />
> 沒有引用任何二手描述。`FCP`、`load`、傳輸量會隨快取與網路變動，文中已標明是未節流或節流。<br />
>
> <strong>封面與圖表</strong>：封面由本機 ComfyUI 的 Qwen-Image 2.1 生成（刻意不含文字）；<br />
> 資料一律用表格——這篇的資料是「比值與字串」，表格比任何圖都精確。第七節那兩張是截圖與<br />
> 實際下載的檔案，不是示意圖。
