---
title: Hexo 與 Python 的 io：兩個常被搞混的名字（含 8.1.2 現況與實測）
date: 2026-10-20 18:00:00
categories:
  - 學習資源
tags:
  - Hexo
  - Python
  - 靜態網站
  - 實測
toc: true
index_img: /img/covers/hexo-and-python-io.png
banner_img: /img/covers/hexo-and-python-io.png
---

![Hexo 與 Python 的 io：兩個常被搞混的名字](/img/covers/hexo-and-python-io.png)

> <strong>這篇是〈用 Python 解決問題：24 類工作 × 48 個套件總整理〉的補充獨立篇。</strong>那張流傳很廣的資訊圖上除了 24 組「痛點 → 工具」，還混進了兩個<strong>不是 Python 套件</strong>的名字：<strong>Hexo</strong> 與 <strong>io</strong>。它們跟「Python 選型」不是同一條線，所以搬出來單獨講。
> 兩段都不長：前段是 <strong>Hexo（Node.js 靜態網站產生器）</strong>的現況、指令與比較，後段是<strong>Python 標準庫 <code>io</code></strong> 的本機實測與三個實務場景。

<!-- more -->

## 為什麼會有這篇

那張資訊圖（Pooja Pawar〈How to use Python for problem-solving〉）把 24 組「問題 → 工具」排成一張表，其中有兩個名字特別容易誤讀：

- <strong>Hexo</strong>：它<strong>不是 Python 套件</strong>，是 Node.js 寫的靜態網站產生器——本站就是用它架的。
- <strong>io</strong>：可能是 Hexo 官網的網域 <code>hexo.io</code>，也可能是 Python 標準庫的 <code>io</code>（<code>StringIO</code>／<code>BytesIO</code>）。兩個完全不同的東西共用同一個縮寫。

以下把兩件事各自講清楚。

## 一、Hexo：Node.js 的靜態網站產生器

<strong>Hexo 不在圖上，因為它不是 Python 套件</strong>——它是用 Node.js 寫的<strong>靜態網站產生器</strong>：你寫 Markdown，Hexo 在幾秒內產生純靜態 HTML／CSS／JS，丟到 GitHub Pages、Netlify、Cloudflare Pages、Vercel 就能上線。<strong>本站（AI Tech Notes）就是 Hexo + Fluid 主題 + GitHub Actions 部署</strong>，所以它值得單獨一篇。

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
| <code>hexo deploy</code> | 依 <code>_config.yml</code> 的 <code>deploy</code> 設定發布（本站用 <code>hexo-deployer-git</code>） |
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

<code>hexo init</code> 產生的 hexo-starter 預設相依（<code>package.json</code>）：<code>hexo ^8.0.0</code>、<code>hexo-renderer-marked ^7.0.0</code>、<code>hexo-renderer-ejs</code>、<code>hexo-renderer-stylus</code>、<code>hexo-server ^3.0.0</code>、<code>hexo-theme-landscape ^1.0.0</code>，以及 index／archive／category／tag 四個 generator。

常用外掛與主題：<code>hexo-deployer-git</code>（推 GitHub Pages）、<code>hexo-generator-searchdb</code>（站內搜尋）、<code>hexo-generator-feed</code>、<code>hexo-generator-sitemap</code>；主題常見 NexT、Butterfly、Fluid、Stellar、Volantis。

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

## 二、「io」的兩種解讀

「io」這個縮寫在圖上會出現兩種完全不同的意思，先看一張圖，再逐一拆解。

![記憶體緩衝：資料從左邊流進去、從右邊流出來，全程不落地](/img/hexo-and-python-io/ch02-python-io-buffer.jpg)

> 圖：本機 ComfyUI 的 Qwen-Image 2.1 生成（本站 house style，無文字）。

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

<code>io</code> 是 Python 標準庫，提供檔案與緩衝區的統一介面：<code>open()</code> 的底層就是它，而 <code>io.StringIO</code>（文字緩衝）與 <code>io.BytesIO</code>（位元組緩衝）可以用來<strong>產生「像檔案的物件」而不落地成檔案</strong>。

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


## 附錄：延伸連結

- Hexo 官網與文件：<a href="https://hexo.io/docs/" target="_blank" rel="noopener">hexo.io/docs</a>、<a href="https://hexo.io/docs/commands" target="_blank" rel="noopener">指令表</a>
- Hexo 8.0.0 發布說明：<a href="https://hexo.io/news/2025/09/16/hexo-8-0-0-released/" target="_blank" rel="noopener">hexo.io/news</a>
- Hexo 起始專案（預設相依）：<a href="https://github.com/hexojs/hexo-starter" target="_blank" rel="noopener">hexojs/hexo-starter</a>
- 原始資訊圖：Pooja Pawar〈How to use Python for problem-solving〉
- 主文：<a href="/2026/10/16/python-problem-solving-toolkit/">用 Python 解決問題：24 類工作 × 48 個套件總整理</a>

> <strong>圖片來源</strong>：封面與章節插圖由本機 ComfyUI 的 <strong>Qwen-Image 2.1</strong> 生成（本站 house style：暗色 cinematic、無文字）；文中「原圖」為 Pooja Pawar 的資訊圖〈How to use Python for problem-solving〉，僅作引用與討論之用，版權歸原作者所有。Hexo 版本與連結為 <strong>2026-10-16</strong> 官方來源查證結果，<code>io</code> 範例為本機 Python 3.11.15 實測輸出。
