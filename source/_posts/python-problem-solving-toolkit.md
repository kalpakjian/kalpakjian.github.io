---
title: 用 Python 解決問題：24 類工作 × 48 個套件總整理（附同類比較、Hexo 與 io 補充）
date: 2026-10-16 09:30:00
categories:
  - AI
  - 學習資源
tags:
  - Python
  - 套件比較
  - 工具選型
  - Hexo
  - 實測
  - LLM
toc: true
index_img: /img/covers/python-problem-solving-toolkit.png
banner_img: /img/covers/python-problem-solving-toolkit.png
---

![用 Python 解決問題：24 類工作 × 48 個套件總整理](/img/covers/python-problem-solving-toolkit.png)

> <strong>整理說明</strong>：這篇從一張流傳很廣的資訊圖「How to use Python for problem-solving」（作者 Pooja Pawar）出發，把圖上 24 組「問題 → 工具」展開成一份可以查的工具書。全文四塊：①<strong>48 個套件的一句話簡介</strong>（依 11 個工作領域分組）；②<strong>同類套件的取捨比較</strong>；③<strong>24 列選型速查＋對原圖的 5 處修正</strong>；④<strong>Hexo 與「io」的補充</strong>。
> 數字都標了出處與查證日期（<strong>2026-10-16</strong>）：本機套件版本是用 <code>importlib.metadata</code> 實掃 Python 3.11.15 環境得到，Hexo／pypdf 等外部版本則查官方來源。
> 全文盡量白話，沒寫過 Python 的人也能看懂選型邏輯。

<!-- more -->

## 一句話總結

> 那張圖真正的價值不是「背 48 個套件名字」，而是示範一種<strong>問題導向的選型方式</strong>：先講清楚卡在哪裡，再挑工具。圖上的「A + B」其實混了兩種關係——<strong>互補</strong>（pandas + openpyxl）與<strong>同類二選一</strong>（Flask／Django）；分清楚這件事，比記住清單更重要。

## 30 秒版本

- 24 列其實只涵蓋 <strong>11 個工作領域</strong>：資料處理、視覺化、Web／API、自動化與爬蟲、文件與媒體、機器學習、深度學習、大數據與流程、資料庫、GUI、AI／Notebook。
- 「Use: A + B」有兩種語意：<strong>互補</strong>（pandas + openpyxl、Matplotlib + Seaborn、pytest + unittest）與<strong>二選一</strong>（Flask／Django、TensorFlow／PyTorch、venv／conda、Airflow／Prefect、Tkinter／PyQt）。後者不該兩個都學。
- 本機實掃（Python 3.11.15）：圖上 42 個可安裝套件中<strong>已裝 17 個</strong>；標準庫的 <code>io</code>、<code>sqlite3</code>、<code>tkinter</code>、<code>venv</code>、<code>unittest</code> 全部可用。
- 對原圖有 <strong>5 處要修正</strong>：PyPDF2 已停更（改用 pypdf）、SQLAlchemy 與 sqlite3 不同層級、schedule 不是桌面自動化、「Flask + Django」不是相加、cron／Task Scheduler 不是 Python 套件。
- <strong>Hexo 不在圖上</strong>：它是 Node.js 的靜態網站產生器（hexo.io），最新 <strong>8.1.2</strong>，8.x 要求 Node.js ≥ 20.19.0。本站就是 Hexo，跟 Python 不衝突。
- 「io」有兩種解讀：<strong>hexo.io</strong>（Hexo 官網／文件）或<strong>標準庫 <code>io</code></strong>（<code>StringIO</code>／<code>BytesIO</code>／<code>open()</code> 的底層）。文末各有一段。

<!-- FIG1 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" role="img" aria-label="互補與二選一：兩種關係" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="998.5" height="598.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">互補與二選一：兩種關係</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同類套件怎麼選的第一步</text>
<rect x="48" y="106" width="440" height="400" rx="14" fill="#1c2230" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="76" y="148" font-size="17" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">互補（加法）：兩個一起用更強</text>
<text x="76" y="176" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一條管線的前後兩段，各管一件事</text>
<rect x="76" y="204" width="176" height="64" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="92" y="233.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">pandas</text>
<text x="92" y="254.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">表格清理與分析</text>
<rect x="284" y="204" width="176" height="64" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="300" y="233.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">openpyxl</text>
<text x="300" y="254.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只在 .xlsx 必要</text>
<path d="M 164 268 L 164 312" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 372 268 L 372 312" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 164 312 L 372 312" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 268 312 L 268 340" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="148" y="342" width="240" height="60" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="268.0" y="370.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">乾淨的 DataFrame</text>
<text x="268.0" y="392.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">.xlsx 也讀得進去</text>
<text x="76" y="444" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">少一個就會壞：缺 openpyxl 時</text>
<text x="76" y="466" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">pandas.read_excel() 直接丟例外。</text>
<text x="76" y="492" font-size="12.5" fill="#2dd4bf" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">判準：會同時出現在同一條管線。</text>
<rect x="512" y="106" width="440" height="400" rx="14" fill="#1c2230" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="540" y="148" font-size="17" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">二選一（減法）：挑一個學到會</text>
<text x="540" y="176" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩條路回答的是同一個問題</text>
<rect x="540" y="200" width="384" height="50" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="732.0" y="230.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">要做網站／提供 API</text>
<path d="M 732 250 L 732 274" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 628 274 L 836 274" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 628 274 L 628 298" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<path d="M 836 274 L 836 298" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="540" y="300" width="176" height="64" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="556" y="329.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Flask</text>
<text x="556" y="350.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">微框架、原型</text>
<rect x="748" y="300" width="176" height="64" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="764" y="329.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Django</text>
<text x="764" y="350.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">全端、admin</text>
<path d="M 628 364 L 628 386" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 836 364 L 836 386" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 628 386 L 836 386" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 732 386 L 732 404" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="540" y="406" width="384" height="56" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="732.0" y="432.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一個終點：HTTP 服務</text>
<text x="732.0" y="454.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">所以它們是替代關係</text>
<text x="540" y="500" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩條路都到得了，同時精通成本高。</text>
<text x="48" y="546" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">互補：pandas＋NumPy、Matplotlib＋Seaborn、pytest＋unittest</text>
<text x="48" y="572" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">二選一：Flask／Django、TensorFlow／PyTorch、venv／conda、Airflow／Prefect</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：互補（加法）vs 二選一（減法）——左邊兩個一起用會更強，右邊兩個只回答同一個問題。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG1 -->

## 原圖：這份整理的來源

以下是本文逐項展開的原始資訊圖（作者 Pooja Pawar，〈How to use Python for problem-solving〉）。本文沒有照抄它的結論，而是逐列補上<strong>版本查證、同類比較與修正建議</strong>：

![How to use Python for problem-solving（原始資訊圖）](/img/infographics/how-to-use-python-for-problem-solving.jpg)

> 圖上 24 列對應的 48 個套件，本文都補了「本機安裝狀態」與「什麼時候該用哪個」；其中 <strong>5 處需要修正</strong>（PyPDF2 停更、SQLAlchemy 層級、schedule 誤用、Flask／Django 互斥、cron 不是 Python 套件），整理在「24 列選型速查」一節。

## 這張圖值得看的地方

1. <strong>用痛點當索引</strong>：「我卡在哪裡」比「有哪些套件」好查，也更接近真實的開發順序。
2. <strong>一列只給兩個工具</strong>：降低選擇焦慮，適合當學習路線的起點。
3. <strong>覆蓋面完整</strong>：從清資料一路到部署、測試、排程，是一條完整的專案生命週期。

## 但圖有三個限制

1. <strong>沒有區分「互補」與「互斥」</strong>：Flask 與 Django 是替代關係；venv 與 conda 通常二選一；TensorFlow 與 PyTorch 同時精通成本很高。
2. <strong>沒有標示規模與情境</strong>：pandas 與 Dask 的差別是資料量、sqlite3 與 PostgreSQL 的差別是併發與多人協作，圖上都沒有。
3. <strong>少數配對過時或層級不同</strong>：PyPDF2 已停更、SQLAlchemy 與 sqlite3 不是同層級、schedule 常被誤解成系統排程器。

## 11 個領域 × 24 列的對應

<!-- FIG2 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 800" role="img" aria-label="11 個工作領域地圖" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="998.5" height="798.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">11 個工作領域地圖</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">24 列痛點 → 11 個工作領域</text>
<rect x="48" y="106" width="904" height="52" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>
<text x="500" y="138" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">24 列痛點 → 11 個工作領域：這就是原圖的目錄</text>
<rect x="48" y="186" width="280" height="116" rx="12" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<circle cx="76" cy="214" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="76" y="218.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1</text>
<text x="102" y="219" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">資料整理與分析</text>
<text x="64" y="244" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">清資料、分析資料</text>
<text x="64" y="268" font-size="11.5" fill="#2dd4bf" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">pandas · NumPy · openpyxl</text>
<rect x="360" y="186" width="280" height="116" rx="12" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<circle cx="388" cy="214" r="15" fill="#58a6ff" opacity="0.92"/>
<text x="388" y="218.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2</text>
<text x="414" y="219" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">視覺化與儀表板</text>
<text x="376" y="244" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">視覺化、做儀表板</text>
<text x="376" y="268" font-size="11.5" fill="#58a6ff" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Matplotlib · Seaborn · Plotly</text>
<text x="376" y="290" font-size="11.5" fill="#58a6ff" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Streamlit</text>
<rect x="672" y="186" width="280" height="116" rx="12" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<circle cx="700" cy="214" r="15" fill="#c084fc" opacity="0.92"/>
<text x="700" y="218.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">3</text>
<text x="726" y="219" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Web 與 API</text>
<text x="688" y="244" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">做網站、做 API</text>
<text x="688" y="268" font-size="11.5" fill="#c084fc" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Flask／Django · FastAPI</text>
<text x="688" y="290" font-size="11.5" fill="#c084fc" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Django REST Framework</text>
<rect x="48" y="326" width="280" height="116" rx="12" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<circle cx="76" cy="354" r="15" fill="#fbbf24" opacity="0.92"/>
<text x="76" y="358.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4</text>
<text x="102" y="359" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">自動化與爬蟲</text>
<text x="64" y="384" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">自動化任務、爬網站</text>
<text x="64" y="408" font-size="11.5" fill="#fbbf24" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">schedule · Selenium</text>
<text x="64" y="430" font-size="11.5" fill="#fbbf24" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">BeautifulSoup · Scrapy</text>
<rect x="360" y="326" width="280" height="116" rx="12" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="388" cy="354" r="15" fill="#f472b6" opacity="0.92"/>
<text x="388" y="358.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5</text>
<text x="414" y="359" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">文件、影像與文字</text>
<text x="376" y="384" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">PDF、影像、文字</text>
<text x="376" y="408" font-size="11.5" fill="#f472b6" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">pypdf · pdfplumber · OpenCV</text>
<text x="376" y="430" font-size="11.5" fill="#f472b6" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Pillow · NLTK · spaCy</text>
<rect x="672" y="326" width="280" height="116" rx="12" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<circle cx="700" cy="354" r="15" fill="#3fb950" opacity="0.92"/>
<text x="700" y="358.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">6</text>
<text x="726" y="359" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">機器學習、深度學習與時序</text>
<text x="688" y="384" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">建 ML／DL 模型、時序</text>
<text x="688" y="408" font-size="11.5" fill="#3fb950" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">scikit-learn · XGBoost · PyTorch</text>
<text x="688" y="430" font-size="11.5" fill="#3fb950" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">TensorFlow／Keras · Prophet</text>
<rect x="48" y="466" width="280" height="116" rx="12" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<circle cx="76" cy="494" r="15" fill="#58a6ff" opacity="0.92"/>
<text x="76" y="498.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7</text>
<text x="102" y="499" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">大數據與工作流</text>
<text x="64" y="524" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">處理大資料、跑資料管線</text>
<text x="64" y="548" font-size="11.5" fill="#58a6ff" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Dask · PySpark · Airflow／Prefect</text>
<rect x="360" y="466" width="280" height="116" rx="12" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<circle cx="388" cy="494" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="388" y="498.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8</text>
<text x="414" y="499" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">資料庫</text>
<text x="376" y="524" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">接資料庫</text>
<text x="376" y="548" font-size="11.5" fill="#2dd4bf" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">sqlite3（標準庫）· SQLAlchemy</text>
<rect x="672" y="466" width="280" height="116" rx="12" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<circle cx="700" cy="494" r="15" fill="#c084fc" opacity="0.92"/>
<text x="700" y="498.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">9</text>
<text x="726" y="499" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GUI</text>
<text x="688" y="524" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">做 GUI</text>
<text x="688" y="548" font-size="11.5" fill="#c084fc" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Tkinter（標準庫）· PyQt</text>
<rect x="48" y="606" width="280" height="116" rx="12" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<circle cx="76" cy="634" r="15" fill="#fbbf24" opacity="0.92"/>
<text x="76" y="638.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10</text>
<text x="102" y="639" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">工程化：測試、環境、部署、排程</text>
<text x="64" y="664" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">測試、環境、排程、部署</text>
<text x="64" y="688" font-size="11.5" fill="#fbbf24" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">pytest · venv／conda · Docker</text>
<text x="64" y="710" font-size="11.5" fill="#fbbf24" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Render · cron／Task Scheduler</text>
<rect x="360" y="606" width="280" height="116" rx="12" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="388" cy="634" r="15" fill="#f472b6" opacity="0.92"/>
<text x="388" y="638.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">11</text>
<text x="414" y="639" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">AI 與 Notebook</text>
<text x="376" y="664" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">建 AI 應用、做 Notebook</text>
<text x="376" y="688" font-size="11.5" fill="#f472b6" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">LangChain · OpenAI · Jupyter／Colab</text>
<rect x="672" y="606" width="280" height="116" rx="12" fill="#161b22" stroke="#f472b666" stroke-width="1.5"/>
<circle cx="700" cy="634" r="15" fill="#f472b6" opacity="0.92"/>
<text x="700" y="638.94" font-size="13" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">!</text>
<text x="726" y="639" font-size="14" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">5 處要修正</text>
<text x="688" y="664" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">PyPDF2 停更、SQLAlchemy 層級、</text>
<text x="688" y="688" font-size="11.5" fill="#f472b6" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">schedule 誤用、Flask／Django、</text>
<text x="688" y="710" font-size="11.5" fill="#f472b6" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">cron 不是 Python 套件</text>
<text x="48" y="758" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">從清資料（1）到部署與測試（10），這 11 個領域就是一條專案生命週期；</text>
<text x="48" y="784" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">圖上「A + B」的組合，有的是互補、有的是二選一（見圖 1 的判準）。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：11 個工作領域 × 24 列痛點——這 12 張卡就是原圖的目錄，也是一條從清資料到部署的專案生命週期。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG2 -->

| 領域 | 圖上的痛點問句 |
| --- | --- |
| 資料整理與分析 | 清資料、分析資料 |
| 視覺化與儀表板 | 視覺化、做儀表板 |
| Web 與 API | 做網站、做 API |
| 自動化與爬蟲 | 自動化任務、爬網站 |
| 文件與媒體 | PDF、影像、文字 |
| 機器學習 | 建 ML 模型 |
| 深度學習 | 建 DL 模型 |
| 時間序列 | 時序資料 |
| 大數據與流程 | 處理大資料、跑資料管線 |
| 資料庫與 GUI | 接資料庫、做 GUI |
| 工程化與部署 | 測試、環境、排程、部署 |
| AI 與 Notebook | 建 AI 應用、做 Notebook |

## 48 個套件一句話簡介

以下每張表的「本機」欄，是本機（Python 3.11.15、hermes venv）以 <code>importlib.metadata</code> 實掃的結果。

### 1）資料整理與分析

| 套件 | 一句話 | 本機 |
| --- | --- | --- |
| pandas | 表格資料核心：DataFrame、groupby、merge、時間索引，讀寫 CSV／Excel／SQL | ✅ 3.0.6 |
| NumPy | 多維陣列 <code>ndarray</code> 與向量化運算；pandas、scikit-learn、PyTorch 的底層 | ✅ 2.4.6 |
| openpyxl | 直接讀寫 <code>.xlsx</code>（公式、樣式、儲存格格式、圖表）；pandas 讀 Excel 的引擎之一 | ❌ 未安裝 |

> ⚠️ 少了 openpyxl 時，<code>pandas.read_excel("x.xlsx")</code> 會直接丟 <code>Missing optional dependency 'openpyxl'</code>——本機目前正是缺這個。

### 2）視覺化與儀表板

| 套件 | 一句話 | 本機 |
| --- | --- | --- |
| Matplotlib | 最底層的繪圖庫，幾乎所有 Python 繪圖都建在它之上；可控性最高、可出出版級圖 | ✅ 3.11.2 |
| Seaborn | 建在 Matplotlib 上的統計視覺化（分布、回歸、分面、長格式資料），預設樣式好看 | ✅ 0.13.2 |
| Plotly | 互動式圖表（hover／zoom／框選），輸出 HTML；Plotly Express 提供高階介面 | ❌ 未安裝 |
| Streamlit | 把 Python 腳本直接變成資料 App／儀表板，不必寫 HTML／CSS／JS，支援熱重載 | ✅ 1.59.1 |

### 3）Web 與 API

| 套件 | 一句話 | 本機 |
| --- | --- | --- |
| Flask | 微框架：路由 + 模板 + 自行挑擴充；輕、適合原型與小型 API | ✅ 3.1.3 |
| Django | 全套框架：ORM、admin 後台、auth、migration、forms；適合內容型與大型網站 | ❌ 未安裝 |
| FastAPI | Starlette + Pydantic：async、型別驗證、自動產生 OpenAPI／Swagger 文件 | ✅ 0.133.1 |
| Django REST Framework | Django 的 REST API 擴充（Serializer／ViewSet／Router／權限） | ❌ 未安裝 |

### 4）自動化與爬蟲

| 套件 | 一句話 | 本機 |
| --- | --- | --- |
| schedule | 純 Python 的「行程內」排程器（每 X 分鐘執行）；沒有持久化，程式關掉就沒了 | ❌ 未安裝 |
| Selenium | 瀏覽器自動化（WebDriver）：E2E 測試與需要 JS 的頁面抓取；較重、要對應 driver | ❌ 未安裝 |
| BeautifulSoup | 容錯高的 HTML／XML 解析器，只負責解析，不負責抓取 | ✅ 4.15.0 |
| Scrapy | 非同步爬蟲框架：排程、去重、Pipeline、Middleware 齊全，適合大規模結構化爬取 | ❌ 未安裝 |

### 5）文件、影像與文字

| 套件 | 一句話 | 本機 |
| --- | --- | --- |
| PyPDF2 | 舊的 PDF 合併／分割／擷取；<strong>已停止維護（PyPI 最後版本 3.0.1）</strong> | ❌ 未安裝 |
| pypdf | PyPDF2 的後繼專案（PyPI 最新 6.20.1），API 相容但已修掉大量問題 | ✅ 6.19.0 |
| pdfplumber | 基於 pdfminer.six，表格與文字座標擷取最強，附視覺化除錯 | ❌ 未安裝 |
| OpenCV | 電腦視覺工業標準：影像／視訊 I/O、濾波、特徵、DNN 推論 | ✅ 5.0.0.93 |
| Pillow（PIL） | 影像檔案 I/O 與基本編輯（縮放、裁切、格式轉換、繪字） | ✅ 12.3.0 |
| NLTK | 教學與研究取向的 NLP 工具箱：語料庫、分詞、POS、經典演算法 | ✅ 3.10.3 |
| spaCy | 工業級 NLP：預訓練 pipeline（tokenize／POS／NER／依存），快、可訓練自訂模型 | ❌ 未安裝 |

### 6）機器學習、深度學習與時序

| 套件 | 一句話 | 本機 |
| --- | --- | --- |
| scikit-learn | 傳統 ML 一站式：前處理、模型、交叉驗證、Pipeline、指標，API 一致 | ✅ 1.9.1 |
| XGBoost | 梯度提升樹（GBDT），表格資料的競賽王者，也提供 sklearn 風格 API | ❌ 未安裝 |
| TensorFlow | Google 的 DL 框架：Keras 高階 API，加上 TFLite／TFX／Serving 部署生態 | ❌ 未安裝 |
| PyTorch | Meta 的 DL 框架：動態圖、除錯直覺，研究與 HuggingFace 生態主流 | ✅ 2.14.1+cu132 |
| statsmodels | 統計推論：OLS／GLM／ARIMA、假設檢定、信賴區間，報表風格接近 R | ❌ 未安裝 |
| Prophet | Meta 的加法式時序模型（趨勢＋季節＋假日），對缺值與異常值穩健 | ❌ 未安裝 |

### 7）大數據與工作流

| 套件 | 一句話 | 本機 |
| --- | --- | --- |
| Dask | 平行／超記憶體運算，API 模仿 pandas 與 NumPy，從單機多核到分散式叢集 | ❌ 未安裝 |
| PySpark | Spark 的 Python API：分散式大資料處理 + Spark SQL／MLlib | ❌ 未安裝 |
| Apache Airflow | 以 DAG 為單位的批次編排平台：Web UI、重試、backfill、告警；元件多、較重 | ❌ 未安裝 |
| Prefect | Python 原生工作流編排：裝飾器即 flow／task，可雲端或自架，比 Airflow 輕 | ❌ 未安裝 |

### 8）資料庫

| 套件 | 一句話 | 本機 |
| --- | --- | --- |
| SQLAlchemy | ORM + Core：多種資料庫、連線池、Alembic 遷移工具 | ✅ 2.0.54 |
| sqlite3 | 標準庫內建的嵌入式資料庫驅動：單一檔案、零設定 | ✅ 標準庫 |

> ⚠️ 原圖把兩者並列，但它們<strong>不是同一層級</strong>：SQLAlchemy 可以跑在 sqlite3 之上（<code>create_engine("sqlite:///app.db")</code>）。同層級的對照應該是「ORM（SQLAlchemy）vs 原生 driver（sqlite3／psycopg／asyncpg）」。

### 9）GUI

| 套件 | 一句話 | 本機 |
| --- | --- | --- |
| Tkinter | 標準庫內建 GUI，輕量跨平台，適合小工具；外觀較舊 | ✅ 標準庫 |
| PyQt | Qt 的 Python 綁定（GPL／商業授權）：元件豐富、外觀專業、可用 Qt Designer | ❌ 未安裝 |

### 10）工程化：測試、環境、部署、排程

| 工具 | 一句話 | 本機 |
| --- | --- | --- |
| pytest | 測試框架：純 assert、fixture、parametrize、外掛生態豐富 | ✅ 8.3.5 |
| unittest | 標準庫的 xUnit 風格測試框架，免安裝；樣板碼較多 | ✅ 標準庫 |
| venv | 標準庫虛擬環境，輕量、跟著 Python 一起附帶 | ✅ 標準庫 |
| conda | 跨語言套件與環境管理，能處理 CUDA／MKL 等非 Python 依賴 | ❌ 未安裝 |
| Docker | 容器化打包成映像檔，跨環境一致，解決「我電腦可以跑」 | ❌ 系統層工具 |
| Render | PaaS 部署（Web Service／Cron／Postgres／Static Site），從 Git 一鍵部署 | ❌ 雲端服務 |
| cron | Unix／Linux 的系統排程器 | ❌ 非 Windows |
| Task Scheduler | Windows 工作排程器（GUI 或 <code>schtasks</code>） | ✅ 系統內建 |

### 11）AI 與 Notebook

| 套件 | 一句話 | 本機 |
| --- | --- | --- |
| LangChain | LLM 應用框架：prompt、chain、tool、retriever、memory、agent、RAG | ❌ 未安裝 |
| OpenAI | 官方 SDK：Chat／Responses API、embeddings、圖片、語音 | ✅ 2.24.0 |
| Jupyter | 互動式 notebook（<code>.ipynb</code>）：cell 執行、即時輸出、內嵌圖表 | ❌ 未安裝 |
| Google Colab | 雲端 Jupyter：免安裝、免費 GPU／TPU、容易分享 | ❌ 雲端服務 |

## 同類套件怎麼選（PK 表）

圖上把同類工具並排，但沒說怎麼選。以下用「什麼時候用哪個」重新整理。

<!-- FIG3 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1060" role="img" aria-label="選型五問決策流程" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker></defs>
<rect x="0.75" y="0.75" width="998.5" height="1058.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">選型五問決策流程</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">先問規模與情境，再挑工具</text>
<rect x="48" y="106" width="904" height="52" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>
<text x="500" y="138" font-size="14" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">先問情境（Q1–Q2），再問產出與團隊（Q3–Q5）</text>
<rect x="48" y="190" width="384" height="84" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<circle cx="80" cy="232.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="80" y="237.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Q1</text>
<text x="108" y="229.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">資料放得進記憶體嗎？</text>
<text x="108" y="250.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">規模決定工具，不是喜好</text>
<path d="M 432 232.0 L 496 232.0" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 496 182.0 L 496 282.0" fill="none" stroke="#7d8590" stroke-width="2"/>
<rect x="560" y="162.0" width="392" height="40" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="576" y="186.5" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">放得進（GB 級）：pandas ＋ NumPy</text>
<path d="M 496 182.0 L 558 182.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="560" y="212.0" width="392" height="40" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="576" y="236.5" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">放不進、單機多核：Dask</text>
<path d="M 496 232.0 L 558 232.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="560" y="262.0" width="392" height="40" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="576" y="286.5" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">已有 Spark 叢集（TB 級）：PySpark</text>
<path d="M 496 282.0 L 558 282.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="354" width="384" height="84" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<circle cx="80" cy="396.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="80" y="401.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Q2</text>
<text x="108" y="393.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">幾個人同時寫入？</text>
<text x="108" y="414.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">併發決定資料庫</text>
<path d="M 432 396.0 L 496 396.0" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 496 371.0 L 496 421.0" fill="none" stroke="#7d8590" stroke-width="2"/>
<rect x="560" y="351.0" width="392" height="40" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="576" y="375.5" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只有你、原型或測試：sqlite3（標準庫）</text>
<path d="M 496 371.0 L 558 371.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="560" y="401.0" width="392" height="40" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="576" y="425.5" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">多人、正式環境：PostgreSQL ＋ SQLAlchemy</text>
<path d="M 496 421.0 L 558 421.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="518" width="384" height="84" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<circle cx="80" cy="560.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="80" y="565.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Q3</text>
<text x="108" y="557.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">圖要給誰看？</text>
<text x="108" y="578.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">產出形式決定繪圖層</text>
<path d="M 432 560.0 L 496 560.0" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 496 510.0 L 496 610.0" fill="none" stroke="#7d8590" stroke-width="2"/>
<rect x="560" y="490.0" width="392" height="40" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="576" y="514.5" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">出版級靜態圖：Matplotlib ＋ Seaborn</text>
<path d="M 496 510.0 L 558 510.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="560" y="540.0" width="392" height="40" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="576" y="564.5" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">要 hover／zoom：Plotly</text>
<path d="M 496 560.0 L 558 560.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="560" y="590.0" width="392" height="40" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="576" y="614.5" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">整個互動儀表板：Streamlit</text>
<path d="M 496 610.0 L 558 610.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="682" width="384" height="84" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<circle cx="80" cy="724.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="80" y="729.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Q4</text>
<text x="108" y="721.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">團隊已經有 Django 嗎？</text>
<text x="108" y="742.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">⚠️ Flask／Django 二選一，不是相加</text>
<path d="M 432 724.0 L 496 724.0" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 496 699.0 L 496 749.0" fill="none" stroke="#7d8590" stroke-width="2"/>
<rect x="560" y="679.0" width="392" height="40" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="576" y="703.5" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">新專案、要 API：FastAPI</text>
<path d="M 496 699.0 L 558 699.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="560" y="729.0" width="392" height="40" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="576" y="753.5" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">已有 Django 專案：Django ＋ DRF</text>
<path d="M 496 749.0 L 558 749.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="48" y="846" width="384" height="84" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<circle cx="80" cy="888.0" r="15" fill="#2dd4bf" opacity="0.92"/>
<text x="80" y="893.32" font-size="14" fill="#08141a" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Q5</text>
<text x="108" y="885.0" font-size="15.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">程式跑在哪裡？</text>
<text x="108" y="906.0" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">打包與託管是兩件事</text>
<path d="M 432 888.0 L 496 888.0" fill="none" stroke="#7d8590" stroke-width="2"/>
<path d="M 496 863.0 L 496 913.0" fill="none" stroke="#7d8590" stroke-width="2"/>
<rect x="560" y="843.0" width="392" height="40" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="576" y="867.5" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">要環境一致、自己管：Docker</text>
<path d="M 496 863.0 L 558 863.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="560" y="893.0" width="392" height="40" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="576" y="917.5" font-size="12.5" fill="#e6edf3" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">要一鍵上線、不維運：Render</text>
<path d="M 496 913.0 L 558 913.0" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<text x="48" y="1006" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">右邊若是兩條路，先確認是「互補」還是「二選一」——⚠️ 那幾組只能挑一個。</text>
<text x="48" y="1032" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一組問題換個情境就會換答案：先問清楚卡在哪裡，再打開套件清單。</text>
</svg>
<figcaption class="image-caption" style="opacity:1;margin-bottom:0;font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 3：選型五問——先問規模與併發（Q1／Q2），再問產出與團隊（Q3–Q5），右邊就是落點；⚠️ 那幾組是二選一，不是相加。｜手繪 SVG 圖表</figcaption>
</figure>
<!-- /FIG3 -->

### 資料處理：先看規模

| 工具 | 資料規模 | 核心介面 | 什麼時候用它 |
| --- | --- | --- | --- |
| NumPy | 單機記憶體 | ndarray | 純數值矩陣運算，或當其他套件的底層 |
| pandas | 單機記憶體（約 GB 級） | DataFrame | 九成的表格清理與分析首選 |
| Dask | 單機多核到分散式、可超記憶體 | pandas-like | 檔案大到裝不進 RAM，但不想學 Spark |
| PySpark | 分散式 TB 級以上 | DataFrame／SQL | 資料在 HDFS／S3，已有 Spark 叢集 |
| sqlite3 | 單機檔案 | SQL | 小型持久化、原型、測試 |
| SQLAlchemy | 同上（支援多種 DB） | ORM／Core | 需要 ORM、要換 DB、要 Alembic 遷移 |

### 視覺化：從靜態到互動

| 工具 | 產出 | 特色 | 什麼時候用它 |
| --- | --- | --- | --- |
| Matplotlib | 靜態 PNG／SVG／PDF | 完全可控、出版級 | 論文與報告要精準排版 |
| Seaborn | 靜態 | 統計圖一行就有預設美觀 | EDA 快速看分布與相關 |
| Plotly | 互動 HTML | hover／zoom、3D、地圖 | 要互動、要嵌進網頁 |
| Streamlit | Web App | 腳本即 App、含 widget | 內部儀表板、Demo |

### Web、API 與靜態網站

| 工具 | 類型 | 學習曲線 | 什麼時候用它 |
| --- | --- | --- | --- |
| Flask | 動態微框架 | 低 | 小 API、原型、想自己決定架構 |
| Django | 動態全端框架 | 中 | 需要 admin／ORM／auth 的完整網站 |
| FastAPI | 動態 API 框架 | 低到中 | async 高效能 API、ML 推論服務 |
| Django REST Framework | Django 的 API 擴充 | 中 | 已有 Django 專案要出 REST API |
| Hexo | <strong>靜態網站產生器</strong>（Node.js） | 低 | 純內容部落格與文件，不想維運伺服器 |

### 爬蟲：一條由輕到重的鏈

<code>requests</code>／<code>httpx</code>（抓取）→ BeautifulSoup（靜態頁解析）→ Selenium／Playwright（需要 JS、要點擊）→ Scrapy（大規模、去重、Pipeline、分散式）。圖上只列了中間與最後一環。

### 深度學習

| 工具 | 風格 | 優勢 | 什麼時候用它 |
| --- | --- | --- | --- |
| TensorFlow／Keras | Keras 高階 API | 部署生態（TFLite／TFX／Serving）、行動與邊緣裝置 | 要上手機／邊緣、企業既有 TF 技術棧 |
| PyTorch | 動態圖 | 除錯直覺、研究與 HuggingFace 生態主流 | 研究、自訂模型、社群範例多 |

### 時間序列

| 工具 | 定位 | 什麼時候用它 |
| --- | --- | --- |
| statsmodels | 統計推論（ARIMA／SARIMAX／GLM、檢定） | 要解釋係數、要信賴區間 |
| Prophet | 加法式趨勢＋季節＋假日 | 商業資料、多季節性、缺值多、要好調 |

### 文件、影像與文字

| 對比 | A | B | 怎麼選 |
| --- | --- | --- | --- |
| PDF | pypdf（原 PyPDF2） | pdfplumber | 合併／分割／加密 → pypdf；表格與文字定位擷取 → pdfplumber |
| 影像 | Pillow | OpenCV | 開檔／縮圖／格式轉換 → Pillow；濾波／特徵／視訊／偵測 → OpenCV |
| NLP | NLTK | spaCy | 教學、語料、經典演算法 → NLTK；生產環境 NER／POS 管線 → spaCy |

### 測試、環境、排程、GUI、Notebook

| 對比 | A | B | 怎麼選 |
| --- | --- | --- | --- |
| 測試 | pytest | unittest | 新專案用 pytest；既有 unittest 也能直接被 pytest 執行 |
| 環境 | venv | conda | 純 Python → venv；需 CUDA／MKL 等非 Python 依賴或跨語言 → conda |
| 排程 | schedule／cron／Task Scheduler | Airflow／Prefect | 單機定時 → 前者；有依賴關係、要重試與監控 → 後者 |
| 編排 | Airflow | Prefect | 大型團隊、要成熟 UI 與生態 → Airflow；Python 原生、動態流程、快上手 → Prefect |
| GUI | Tkinter | PyQt | 小工具、零依賴 → Tkinter；專業外觀、複雜介面 → PyQt（或 PySide6） |
| Notebook | Jupyter | Colab | 本機／離線／自訂環境 → Jupyter；臨時要 GPU、免安裝、要分享 → Colab |

### 部署：打包與平台是兩件事

| 工具 | 層級 | 說明 |
| --- | --- | --- |
| Docker | 打包 | 把執行環境做成映像檔，任何地方結果一致 |
| Render | 平台 | 吃 Git repo 自動部署（Web／Cron／DB／Static Site）；同類有 Railway、Fly.io、Vercel、Netlify、Cloudflare Pages |

> 換句話說：<strong>Docker 解決「跑得起來」，Render 解決「放在哪裡跑」</strong>。兩個一起用很正常。

## 24 列選型速查（含 5 處修正）

| 痛點 | 圖上建議 | 補充與修正 |
| --- | --- | --- |
| 清理髒資料 | pandas + openpyxl | 互補：openpyxl 只在處理 <code>.xlsx</code> 時必要 |
| 分析資料 | NumPy + pandas | 互補：NumPy 負責數值底層，pandas 負責表格 |
| 視覺化 | Matplotlib + Seaborn | 互補：要互動再加 Plotly |
| 儀表板 | Streamlit + Plotly | 互補；對外正式產品可考慮 Dash 或 Panel |
| 建網站 | Flask + Django | ⚠️ <strong>二選一</strong>，不是相加 |
| 自動化任務 | schedule + Selenium | ⚠️ 桌面自動化更該用 <code>pyautogui</code>／<code>pywinauto</code>／Playwright |
| 爬網站 | BeautifulSoup + Scrapy | 互補；抓取底層建議再學 <code>requests</code>／<code>httpx</code> |
| 處理 PDF | PyPDF2 + pdfplumber | ⚠️ <strong>改用 pypdf</strong>（PyPDF2 最後版本 3.0.1，已停更） |
| 處理影像 | OpenCV + PIL Pillow | 互補，兩者都會用到 |
| 處理文字 | NLTK + spaCy | 互補；生產環境以 spaCy 為主 |
| 建 ML 模型 | scikit-learn + XGBoost | 互補，表格資料的黃金組合 |
| 建 DL 模型 | TensorFlow + PyTorch | ⚠️ <strong>二選一</strong>即可，同時精通成本高 |
| 時序資料 | statsmodels + Prophet | 互補：要統計檢定選前者，要快速可用的預測選後者 |
| 處理大資料 | Dask + PySpark | 互補：先 Dask，規模真的到叢集才上 PySpark |
| 建 API | FastAPI + DRF | ⚠️ 新專案用 FastAPI；已有 Django 才用 DRF |
| 接資料庫 | SQLAlchemy + sqlite3 | ⚠️ <strong>不同層級</strong>；正式環境把 sqlite3 換成 PostgreSQL |
| 做 GUI | Tkinter + PyQt | <strong>二選一</strong> |
| 跑資料管線 | Airflow + Prefect | <strong>二選一</strong>，不要同時上 |
| 部署 App | Docker + Render | 互補：打包與託管 |
| 測試程式 | pytest + unittest | 互補；主力放 pytest |
| 管理環境 | venv + conda | <strong>二選一</strong>，通常不需要並存 |
| 排程腳本 | cron + Task Scheduler | 兩者都不是 Python 套件；Python 原生可用 APScheduler |
| 建 AI 應用 | LangChain + OpenAI | 互補（框架 + 模型供應商），也可換 LlamaIndex、<code>openai-agents</code> |
| 做 Notebook | Jupyter + Google Colab | 同源：Colab 就是雲端 Jupyter |

### 五個選型原則

1. <strong>先問資料量與併發，再問套件</strong>：單機 GB 級用 pandas，超出記憶體用 Dask，多人同時寫入就別用 sqlite3。
2. <strong>同類工具挑一個學到會用就好</strong>：Flask／Django／FastAPI 都是「HTTP 框架」，先會一個，換框架只花幾天。
3. <strong>把「互補」與「替代」分開記</strong>：pandas + NumPy 是加法；Flask vs Django 是減法。
4. <strong>版本時效要查</strong>：PyPDF2 這類「教學文還在用、但已停更」的套件是最大的地雷，<code>pypdf</code> 就是活例子。
5. <strong>用標準庫打底</strong>：<code>io</code>、<code>sqlite3</code>、<code>tkinter</code>、<code>venv</code>、<code>unittest</code>、<code>json</code>、<code>pathlib</code> 都不用裝，很多場景根本不需要第三方套件。

## 補充一：Hexo 與這張圖的關係

<strong>Hexo 不在圖上，因為它不是 Python 套件</strong>——它是用 Node.js 寫的<strong>靜態網站產生器</strong>：你寫 Markdown，Hexo 在幾秒內產生純靜態 HTML／CSS／JS，丟到 GitHub Pages、Netlify、Cloudflare Pages、Vercel 就能上線。<strong>本站（AI Tech Notes）就是 Hexo + Fluid 主題 + GitHub Actions 部署</strong>，所以它值得單獨一段。

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

## 補充二：「io」的兩種解讀

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

## 附錄 A：本機環境盤點（2026-10-16 實掃）

掃描方式：對 42 個圖上可安裝套件逐一呼叫 <code>importlib.metadata.version()</code>，再用 <code>importlib</code> 檢查標準庫模組。

<strong>已安裝 17 個</strong>：pandas 3.0.6、NumPy 2.4.6、Matplotlib 3.11.2、Seaborn 0.13.2、Streamlit 1.59.1、Flask 3.1.3、FastAPI 0.133.1、BeautifulSoup 4.15.0、pypdf 6.19.0、OpenCV 5.0.0.93、Pillow 12.3.0、NLTK 3.10.3、scikit-learn 1.9.1、PyTorch 2.14.1+cu132、SQLAlchemy 2.0.54、pytest 8.3.5、OpenAI 2.24.0。

<strong>標準庫可用</strong>：<code>io</code>、<code>sqlite3</code>、<code>tkinter</code>、<code>venv</code>、<code>unittest</code>、<code>json</code>、<code>pathlib</code>。

<strong>缺口 25 個</strong>：openpyxl、plotly、Django、DRF、schedule、Selenium、Scrapy、PyPDF2、pdfplumber、spaCy、XGBoost、TensorFlow、statsmodels、Prophet、Dask、PySpark、Airflow、Prefect、PyQt5／PyQt6、virtualenv、conda、LangChain、JupyterLab、Notebook。

補齊指令（已排除不建議安裝的 PyPDF2，以及不是 pip 套件的 conda）：

```bash
pip install openpyxl plotly django djangorestframework schedule selenium scrapy \
    pdfplumber spacy xgboost statsmodels prophet dask pyspark apache-airflow \
    prefect langchain jupyterlab
```

> ⚠️ 兩個提醒：<strong>spaCy</strong> 要另外下載語言模型（<code>python -m spacy download zh_core_web_sm</code>）；<strong>Prophet</strong> 與 <strong>PySpark</strong> 需要編譯或 JDK 依賴，建議分開安裝、一次一個，裝失敗比較好定位。

## 附錄 B：延伸連結

- Hexo 官網與文件：<a href="https://hexo.io/docs/" target="_blank" rel="noopener">hexo.io/docs</a>、<a href="https://hexo.io/docs/commands" target="_blank" rel="noopener">指令表</a>
- Hexo 8.0.0 發布說明：<a href="https://hexo.io/news/2025/09/16/hexo-8-0-0-released/" target="_blank" rel="noopener">hexo.io/news</a>
- Hexo 起始專案（預設相依）：<a href="https://github.com/hexojs/hexo-starter" target="_blank" rel="noopener">hexojs/hexo-starter</a>
- pypdf（PyPDF2 的後繼）：<a href="https://pypi.org/project/pypdf/" target="_blank" rel="noopener">PyPI pypdf</a>、<a href="https://pypi.org/project/PyPDF2/" target="_blank" rel="noopener">PyPI PyPDF2（最後 3.0.1）</a>
- 原始資訊圖：Pooja Pawar〈How to use Python for problem-solving〉

> <strong>圖片來源</strong>：封面由本部落格的 <strong>Qwen-Image 2.1</strong> 封面產生流程製作（暗色 cinematic 風格，與全站一致）；文中「原圖」為 Pooja Pawar 的資訊圖〈How to use Python for problem-solving〉，僅作引用與逐項討論之用，版權歸原作者所有。套件版本為 <strong>2026-10-16</strong> 本機實掃與官方來源查證結果。
