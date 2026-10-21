---
title: Hexo 與 Python 的 io：兩個常被搞混的名字（含 github.io、8.1.2 現況與實測）
date: 2026-10-20 18:00:00
categories:
  - 學習資源
tags:
  - Hexo
  - Python
  - 靜態網站
  - GitHub Pages
  - 實測
toc: true
index_img: /img/covers/hexo-and-python-io.png
banner_img: /img/covers/hexo-and-python-io.png
---

![Hexo 與 Python 的 io：兩個常被搞混的名字](/img/covers/hexo-and-python-io.png)

> <strong>這篇是〈用 Python 解決問題：24 類工作 × 48 個套件總整理〉的補充獨立篇。</strong>
>
> 那張流傳很廣的資訊圖上除了 24 組「痛點 → 工具」，還混進了兩個<strong>不是 Python 套件</strong>的名字：<strong>Hexo</strong> 與 <strong>io</strong>。
>
> 它們跟「Python 選型」不是同一條線，所以搬出來單獨講。
>
> 兩段都不長：前段是 <strong>Hexo（Node.js 靜態網站產生器）</strong>的現況、指令與比較；後段把「io」拆成三種解讀——<code>hexo.io</code>、Python 標準庫 <code>io</code>，以及本站真正天天在用的 <code>github.io</code>。

<!-- more -->

## 為什麼會有這篇

那張資訊圖（Pooja Pawar〈How to use Python for problem-solving〉）把 24 組「問題 → 工具」排成一張表，其中有兩個名字特別容易誤讀：

- <strong>Hexo</strong>：它<strong>不是 Python 套件</strong>，是 Node.js 寫的靜態網站產生器——本站就是用它架的。
- <strong>io</strong>：三個完全不同的東西共用同一個縮寫（圖上只涉及前兩個）。
  - 一個是 Hexo 官網的網域 <code>hexo.io</code>
  - 一個是 Python 標準庫的 <code>io</code>（<code>StringIO</code>／<code>BytesIO</code>）
  - 一個是本站的網址 <code>github.io</code>（GitHub Pages 的預設網域）——<strong>最常用，但不是直接使用</strong>

以下把 Hexo 與三種「io」各自講清楚。

## 一、Hexo：Node.js 的靜態網站產生器

<strong>Hexo 不在圖上，因為它不是 Python 套件</strong>——它是用 Node.js 寫的<strong>靜態網站產生器</strong>。

你寫 Markdown，Hexo 在幾秒內產生純靜態 HTML／CSS／JS，丟到 GitHub Pages、Netlify、Cloudflare Pages、Vercel 就能上線。

<strong>本站（AI Tech Notes）就是 Hexo + Fluid 主題 + GitHub Actions 部署</strong>，所以它值得單獨一篇。

先看這張圖：Hexo 做的事就是這件事。

![Markdown 進去、靜態網頁出來：Hexo 就是這條產線](/img/hexo-and-python-io/ch01-hexo-static-site.jpg)

> 圖：本機 ComfyUI 的 Qwen-Image 2.1 生成（本站 house style，無文字）。

### 官方現況（2026-10-16 查證）

| 項目 | 內容 |
| --- | --- |
| 官網 | <code>hexo.io</code>（<code>/docs</code> 文件、<code>/plugins</code> 外掛、<code>/themes</code> 主題、<code>/news</code> 公告；站上有正體中文語系） |
| 最新版本 | <strong>hexo 8.1.2</strong>、<strong>hexo-cli 4.3.2</strong> |
| 8.0.0 發布 | 2025-09-16 |
| 8.x 破壞性變更 | 移除 Node.js 16／18 支援，<code>engines.node</code> 要求 <strong>≥ 20.19.0</strong>（7.x 只需 14+） |
| 本機環境 | Node <strong>v24.14.1</strong> ✅ 可用 Hexo 8；本機部落格的 <code>package.json</code> 標示 <code>hexo 8.1.2</code> |
| 渲染器 | Hexo 8 核心<strong>不內建</strong> Markdown 渲染器，靠外掛（<code>hexo init</code> 產生的 hexo-starter 預設用 <code>hexo-renderer-marked</code>） |

### 基本指令

| 指令 | 做什麼 |
| --- | --- |
| <code>hexo init [folder]</code> | 初始化網站（clone hexo-starter + landscape 主題，並自動安裝依賴） |
| <code>hexo new [layout] &lt;title&gt;</code> | 產生新文章（<code>layout</code> 省略時用 <code>default_layout</code>；<code>draft</code> 產生草稿） |
| <code>hexo server</code> | 本機預覽，預設 <code>http://localhost:4000</code> |
| <code>hexo generate</code> | 產生靜態檔到 <code>public/</code>（<code>-d</code> 產生後直接部署、<code>-w</code> 監看） |
| <code>hexo deploy</code> | 依 <code>_config.yml</code> 的 <code>deploy</code> 設定發布（常見外掛 <code>hexo-deployer-git</code>；本站改用 GitHub Actions，見解讀 C） |
| <code>hexo clean</code> | 清掉 <code>db.json</code> 與 <code>public/</code> |
| <code>hexo publish</code>／<code>hexo render</code>／<code>hexo migrate</code>／<code>hexo list</code>／<code>hexo config</code> | 草稿轉正式／單檔渲染／從其他部落格系統匯入／列出路由／讀寫設定 |
| 全域選項 | <code>--safe</code>（停用外掛除錯）、<code>--debug</code>、<code>--config</code>、<code>--draft</code>、<code>--cwd</code> |

### 目錄結構與預設相依

| 路徑 | 用途 |
| --- | --- |
| <code>_config.yml</code> | 站台設定（標題、URL、permalink、theme…） |
| <code>source/_posts/</code> | 文章（Markdown + front-matter） |
| <code>source/_drafts/</code> | 草稿（預設不輸出） |
| <code>scaffolds/</code> | 新文章模板 |
| <code>themes/</code> 或 npm 主題套件 | 佈景主題（本站用 npm 安裝的 <code>hexo-theme-fluid</code>） |
| <code>public/</code> | 產生出來的靜態檔 |

<code>hexo init</code> 產生的 hexo-starter 預設相依（<code>package.json</code>）：

- <code>hexo ^8.0.0</code>
- <code>hexo-renderer-marked ^7.0.0</code>（Markdown 渲染）
- <code>hexo-renderer-ejs</code>、<code>hexo-renderer-stylus</code>
- <code>hexo-server ^3.0.0</code>
- <code>hexo-theme-landscape ^1.0.0</code>
- index／archive／category／tag 四個 generator

常用外掛：

- <code>hexo-deployer-git</code>：推 GitHub Pages
- <code>hexo-generator-searchdb</code>：站內搜尋
- <code>hexo-generator-feed</code>：RSS
- <code>hexo-generator-sitemap</code>：sitemap

常見主題：NexT、Butterfly、Fluid、Stellar、Volantis。

### Hexo 與其他靜態網站產生器

| 工具 | 語言 | 產生速度 | 生態 | 適合 |
| --- | --- | --- | --- | --- |
| <strong>Hexo</strong> | Node.js | 快 | 主題與外掛極多，中文圈最流行 | 個人技術部落格 |
| Hugo | Go（單一執行檔） | 極快 | 主題多、設定式 | 文章量很大、CI 要快 |
| Jekyll | Ruby | 較慢 | GitHub Pages 原生支援 | 舊站、想直接推 GitHub Pages |
| Astro | Node／JS | 快 | 現代元件 + Islands | 想要元件化又輸出靜態 |
| VitePress | Node／Vue | 快 | 文件導向、內建搜尋 | 技術文件站 |
| MkDocs（Material） | <strong>Python</strong> | 快 | 文件導向 | Python 專案文件 |
| Pelican | <strong>Python</strong> | 中 | 部落格、Jinja2 模板 | 想用純 Python 寫部落格 |

### 什麼時候用 Hexo，什麼時候不要

| 需求 | 選它 | 為什麼 |
| --- | --- | --- |
| 純內容、SEO、不想維運伺服器 | <strong>Hexo</strong> + GitHub Pages／Cloudflare Pages | 靜態檔、免費、快、零後端 |
| 要登入、資料庫、後台管理 | Django | 動態全端框架 |
| 小型 API 或 ML 推論服務 | FastAPI | async + 自動文件 |
| 內部資料儀表板 | Streamlit | 幾十行就能完成 |
| 環境一致打包 | Docker | 映像檔 |
| 一鍵雲端部署 | Render | PaaS（也能部署 Hexo 產生的靜態站） |

> 反過來說：<strong>如果網站需要會員、購物車、即時留言，Hexo 就不適合</strong>——靜態網站沒有後端，那類需求要接第三方服務（如 Giscus、Algolia）或改用 Django／FastAPI。

## 二、「io」的三種解讀

「io」至少有三種完全不同的意思：兩個網域、一個標準庫。嚴格說，圖上只涉及前兩種；第三種是本站每天在用、卻不在圖上的那個。先看對照表，再逐一拆解。

| 寫法 | 屬於什麼 | 本站的角色 |
| --- | --- | --- |
| <code>hexo.io</code> | Hexo 官網的網域 | 查文件、查版本 |
| <code>github.io</code> | GitHub Pages 的預設網域 | 本站網址；部署的結果 |
| <code>io</code>（程式碼裡） | Python 標準庫 | 寫程式時處理記憶體 I/O |

### 解讀 A：<code>hexo.io</code>——Hexo 的官方網域

如果你指的是網址裡的 <code>io</code>，那就是 Hexo 官網。常用的幾個入口：

| 網址 | 內容 |
| --- | --- |
| <code>hexo.io/docs</code> | 文件：安裝需求、設定、指令、寫作、主題開發 |
| <code>hexo.io/docs/commands</code> | 全部 CLI 指令與參數 |
| <code>hexo.io/plugins</code> | 外掛市集 |
| <code>hexo.io/themes</code> | 主題市集 |
| <code>hexo.io/news/2025/09/16/hexo-8-0-0-released/</code> | 8.0.0 發布說明（移除 Node 16／18 支援） |

### 解讀 B：Python 標準庫 <code>io</code>——記憶體中的 I/O 抽象

![記憶體緩衝：資料從左邊流進去、從右邊流出來，全程不落地](/img/hexo-and-python-io/ch02-python-io-buffer.jpg)

> 圖：本機 ComfyUI 的 Qwen-Image 2.1 生成（本站 house style，無文字）。

<code>io</code> 是 Python 標準庫，提供檔案與緩衝區的統一介面：<code>open()</code> 的底層就是它。

其中 <code>io.StringIO</code>（文字緩衝）與 <code>io.BytesIO</code>（位元組緩衝）可以用來<strong>產生「像檔案的物件」而不落地成檔案</strong>。

本機實測（Python 3.11.15）：

```python
import io

s = io.StringIO()
s.write("hello")
s.seek(0)
print(repr(s.read()))        # 'hello'

b = io.BytesIO(b"\x89PNG")
print(b.read(1))             # b'\x89'
```

實際會用到的三個場景：

1. <strong>把圖表直接變成 bytes 上傳／回傳</strong>：Matplotlib 先寫進 <code>BytesIO</code>，再交給 API 或 <code>st.image()</code>，不必產生暫存檔。
2. <strong>把上傳的 Excel 餵給 pandas</strong>：<code>pd.read_excel(io.BytesIO(uploaded_bytes))</code>。
3. <strong>測試檔案處理邏輯</strong>：用 <code>StringIO</code> 餵假內容，不必在測試裡真的開檔。

如果你的「io」指的是<strong>各種格式的輸入輸出套件</strong>，對照關係是：

| 格式 | 套件 |
| --- | --- |
| Excel <code>.xlsx</code> | openpyxl（pandas 的引擎） |
| PDF | pypdf（結構操作）、pdfplumber（內容擷取） |
| 影像 | Pillow（檔案 I/O）、OpenCV（影像與視訊管線） |
| CSV／JSON／設定檔 | 標準庫 <code>csv</code>、<code>json</code>、<code>pathlib</code>、<code>io</code> |
| 資料庫 | sqlite3（標準庫）、SQLAlchemy（ORM） |
| HTTP | <code>requests</code>／<code>httpx</code>（抓取）、FastAPI（提供） |

### 解讀 C：<code>github.io</code>——GitHub Pages 的預設網域（最常用，但不是直接使用）

<code>github.io</code> 既不是 Python 套件，也不是一個要另外註冊的服務。它是 <strong>GitHub Pages</strong> 配給每個帳號的預設網域：把靜態檔放進 repo，GitHub 就從這個網域把網站送出去。

| 站台類型 | repo 名稱 | 預設網址 |
| --- | --- | --- |
| 使用者／組織站 | <code>&lt;owner&gt;.github.io</code> | <code>https://&lt;owner&gt;.github.io/</code> |
| 專案站 | 任意 repo | <code>https://&lt;owner&gt;.github.io/&lt;repo&gt;/</code> |

本站是前者：<code>https://kalpakjian.github.io/</code>。瀏覽器打開的 <code>github.io</code> 背後沒有另一台伺服器，而是 GitHub Pages 直接把 repo 裡的靜態檔當網站供應。

<strong>為什麼說「不是直接使用」</strong>

你不會開 <code>github.io</code> 的後台，也不會把檔案「上傳到 github.io」；真正操作的是 GitHub 上的 repo。本站的流程是：

1. 文章寫在 <code>source/_posts/*.md</code>
2. 本機或 CI 執行 <code>hexo generate</code>，產出 <code>public/</code>
3. <code>.github/workflows/pages.yml</code> 用 <code>actions/upload-pages-artifact</code> 打包 <code>public/</code>，再用 <code>actions/deploy-pages</code> 發布
4. GitHub 把同一份靜態檔掛到 <code>https://kalpakjian.github.io/</code>

把這四步畫成圖，就是這樣：

<!-- FIG-DEPLOY -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 570" role="img" aria-label="github.io 部署管線：Markdown 到 Pages" style="width:100%;height:auto;display:block">
<defs><marker id="mDeployArrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<g font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">
<rect x="0.75" y="0.75" width="998.5" height="568.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700">github.io 從哪裡來：Hexo → GitHub Actions → Pages</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e">本站沒有 gh-pages 分支，也沒有用 hexo deploy；push 到 main 就自動重建</text>
<rect x="48" y="132" width="280" height="132" rx="12" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<circle cx="78" cy="163" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="78" y="168.4" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle">1</text>
<text x="104" y="167" font-size="16" fill="#e6edf3" font-weight="700">寫文章</text>
<text x="72" y="188" font-size="12" fill="#8b949e">Markdown + front-matter</text>
<text x="72" y="222" font-size="12.5" fill="#2dd4bf">source/_posts/</text>
<text x="72" y="242" font-size="12.5" fill="#2dd4bf">*.md</text>
<rect x="360" y="132" width="280" height="132" rx="12" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<circle cx="390" cy="163" r="15" fill="#58a6ff" opacity="0.92"/>
<text x="390" y="168.4" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle">2</text>
<text x="416" y="167" font-size="16" fill="#e6edf3" font-weight="700">執行 Hexo</text>
<text x="384" y="188" font-size="12" fill="#8b949e">Hexo 8.1.2／本機 0.4 秒</text>
<text x="384" y="222" font-size="12.5" fill="#58a6ff">hexo generate</text>
<text x="384" y="242" font-size="12.5" fill="#58a6ff">public/</text>
<rect x="672" y="132" width="280" height="132" rx="12" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<circle cx="702" cy="163" r="15" fill="#c084fc" opacity="0.92"/>
<text x="702" y="168.4" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle">3</text>
<text x="728" y="167" font-size="16" fill="#e6edf3" font-weight="700">純靜態檔</text>
<text x="696" y="188" font-size="12" fill="#8b949e">沒有後端、沒有資料庫</text>
<text x="696" y="222" font-size="12.5" fill="#c084fc">HTML／CSS／JS</text>
<text x="696" y="242" font-size="12.5" fill="#c084fc">img／search.xml</text>
<path d="M 330 198 L 354 198" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#mDeployArrow)"/>
<path d="M 642 198 L 666 198" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#mDeployArrow)"/>
<path d="M 812 264 L 812 284 Q 812 294 802 294 L 198 294 Q 188 294 188 304 L 188 320" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#mDeployArrow)"/>
<rect x="340" y="272" width="320" height="28" fill="#0d1117"/>
<text x="500" y="288" font-size="12" fill="#8b949e" text-anchor="middle">artifact：public/ 打包後的靜態檔</text>
<rect x="48" y="330" width="280" height="132" rx="12" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<circle cx="78" cy="361" r="15" fill="#fbbf24" opacity="0.92"/>
<text x="78" y="366.4" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle">4</text>
<text x="104" y="365" font-size="16" fill="#e6edf3" font-weight="700">打包 artifact</text>
<text x="72" y="386" font-size="12" fill="#8b949e">GitHub Actions</text>
<text x="72" y="420" font-size="12.5" fill="#fbbf24">actions/upload-</text>
<text x="72" y="440" font-size="12.5" fill="#fbbf24">pages-artifact</text>
<rect x="360" y="330" width="280" height="132" rx="12" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="390" cy="361" r="15" fill="#f472b6" opacity="0.92"/>
<text x="390" y="366.4" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle">5</text>
<text x="416" y="365" font-size="16" fill="#e6edf3" font-weight="700">部署 Pages</text>
<text x="384" y="386" font-size="12" fill="#8b949e">actions/deploy-pages</text>
<text x="384" y="420" font-size="12.5" fill="#f472b6">pages: write</text>
<text x="384" y="440" font-size="12.5" fill="#f472b6">id-token: write</text>
<rect x="672" y="330" width="280" height="132" rx="12" fill="#161b22" stroke="#3fb95099" stroke-width="2"/>
<circle cx="702" cy="361" r="15" fill="#3fb950" opacity="0.92"/>
<text x="702" y="366.4" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle">6</text>
<text x="728" y="365" font-size="16" fill="#e6edf3" font-weight="700">上線（本站）</text>
<text x="696" y="386" font-size="12" fill="#8b949e">GitHub Pages 的預設網域</text>
<text x="696" y="420" font-size="12.5" fill="#3fb950">https://</text>
<text x="696" y="440" font-size="13.5" fill="#3fb950" font-weight="700">kalpakjian.github.io/</text>
<path d="M 330 396 L 354 396" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#mDeployArrow)"/>
<path d="M 642 396 L 666 396" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#mDeployArrow)"/>
<text x="48" y="502" font-size="13" fill="#8b949e">三個「io」裡，本站流量最大、天天在用的就是最後那張卡；但它只是部署結果的網址。</text>
<text x="48" y="528" font-size="13" fill="#7d8590">另一條路是 hexo deploy → gh-pages 分支；本專案沒有 deploy 區段，所以不走這條。</text>
</g>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖：本站的發布管線——Markdown 進、<code>github.io</code> 出；中間沒有 <code>gh-pages</code> 分支。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG-DEPLOY -->

所以三個「io」裡，本站<strong>流量最大、天天在用</strong>的其實是 <code>github.io</code>；但它只是<strong>部署結果的網址</strong>，不是拿來寫程式或設定的物件。這也是它最容易在「工具清單」裡被誤放的原因。

> <strong>本專案沒有 <code>gh-pages</code> 分支，也沒有使用 <code>hexo deploy</code></strong>：<code>_config.yml</code> 的 deploy 區段是空的，發布完全交給 GitHub Actions。前面指令表保留 <code>hexo deploy</code>，是給「想用 <code>hexo-deployer-git</code> 推 <code>gh-pages</code>」的站台參考。

<strong>幾個容易搞混的點</strong>

- <code>github.io</code> ≠ <code>github.com</code>：前者是網站網址，後者是原始碼 repo。
- <code>github.io</code> ≠ 產品名稱：產品叫 <strong>GitHub Pages</strong>，<code>github.io</code> 只是它的預設網域。
- 免費方案的 Pages 來源 repo 需公開；Pro／Team／Enterprise 可用私有 repo。
- 額度：來源 repo 建議 ≤ 1 GB、發布站 ≤ 1 GB、流量軟限制 100 GB／月；用自訂 Actions workflow 發布時，<strong>不受每小時 10 次建置</strong>的軟限制。
- 可以綁自訂網域（CNAME）；綁了以後網址不再是 <code>github.io</code>，但主機仍是 GitHub Pages。
- <code>github.io</code> 在 Public Suffix List 上，瀏覽器把每個 <code>&lt;owner&gt;.github.io</code> 視為獨立站台，cookie 不會跨帳號互通。

一句話：<code>hexo.io</code> 查文件、<code>github.io</code> 看本站、程式裡的 <code>io</code> 處理緩衝。

## 附錄：延伸連結

- Hexo 官網與文件：<a href="https://hexo.io/docs/" target="_blank" rel="noopener">hexo.io/docs</a>、<a href="https://hexo.io/docs/commands" target="_blank" rel="noopener">指令表</a>
- Hexo 8.0.0 發布說明：<a href="https://hexo.io/news/2025/09/16/hexo-8-0-0-released/" target="_blank" rel="noopener">hexo.io/news</a>
- Hexo 起始專案（預設相依）：<a href="https://github.com/hexojs/hexo-starter" target="_blank" rel="noopener">hexojs/hexo-starter</a>
- GitHub Pages 是什麼：<a href="https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages" target="_blank" rel="noopener">docs.github.com/pages</a>
- Pages 使用額度：<a href="https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits" target="_blank" rel="noopener">GitHub Pages limits</a>
- 用自訂 Actions workflow 發布：<a href="https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages" target="_blank" rel="noopener">Using custom workflows</a>
- 自訂網域：<a href="https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages" target="_blank" rel="noopener">About custom domains</a>
- 原始資訊圖：Pooja Pawar〈How to use Python for problem-solving〉
- 主文：<a href="/2026/10/16/python-problem-solving-toolkit/">用 Python 解決問題：24 類工作 × 48 個套件總整理</a>

> <strong>圖片來源</strong>：封面與章節插圖由本機 ComfyUI 的 <strong>Qwen-Image 2.1</strong> 生成（本站 house style：暗色 cinematic、無文字）。
>
> 文中「原圖」為 Pooja Pawar 的資訊圖〈How to use Python for problem-solving〉，僅作引用與討論之用，版權歸原作者所有。
>
> Hexo 版本與連結為 <strong>2026-10-16</strong> 官方來源查證結果；GitHub Pages 網域、額度與部署方式為 <strong>2026-10-21</strong> 官方文件查證；<code>io</code> 範例為本機 Python 3.11.15 實測輸出。
