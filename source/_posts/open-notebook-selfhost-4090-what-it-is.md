---
title: 'Open Notebook 是什麼、能做什麼、對我有什麼用：在 RTX 4090 上從 clone 跑到中文問答'
date: 2026-10-31 14:30:00
categories:
  - 技術筆記
tags:
  - Open Notebook
  - NotebookLM
  - 本地 LLM
  - RAG
  - SurrealDB
  - Ollama
  - bge-m3
  - LangGraph
  - 向量搜尋
  - 自架
  - RTX 4090
  - 實測
toc: true
index_img: /img/covers/open-notebook-selfhost-4090.png
banner_img: /img/covers/open-notebook-selfhost-4090.png
---

手邊有一批語音轉錄（1.2 GB、2,219 個檔）、一疊從 PDF 抽出來的簡報文字、還有三百多 MB 的部落格 Markdown。每次想問「我當初對這件事寫過什麼」，能用的只有 `Select-String` 和記憶。

`lfnovo/open-notebook` 號稱是自架的 NotebookLM，四萬多星。這篇不是轉述它的 README，而是把它**真的裝起來、真的丟資料、真的量時間**，然後回答三個問題：這是什麼、它能做什麼、對我的工作流到底有沒有用。文末附上我踩到的四個坑與完整可複製的啟動指令。

<!-- more -->

## 三十秒結論

| 問題 | 一句話回答 |
|---|---|
| **這是什麼** | MIT 授權、可完全自架的 NotebookLM 替代品。把來源檔變成向量索引，再讓你在上面問答、寫筆記、生成 podcast |
| **核心技術** | FastAPI + Next.js 16 + **SurrealDB 2.x**（圖、全文 BM25、向量搜尋放在同一個 DB）+ LangGraph |
| **能在我的 4090 上跑嗎** | **可以**。8B 聊天模型 + `bge-m3` 嵌入模型很順；**27B（19 GB / 32k context）目前跑不動** |
| **對我有什麼用** | 當「唯讀的第二大腦查詢層」**有用**；不能取代我既有的 PDF → HTML → 題庫產線 |
| **值不值得裝** | 需要「跨語料問答 + 附出處」就值得；只想要產出自動化就不值得 |
| **最大的隱形成本** | SurrealDB + API + worker + 前端共四個常駐程序，比「一支 Python 腳本」重得多 |

## 一、這是什麼

先講定位。它不是筆記軟體，也不是聊天介面——它的核心是「**來源（source）→ 切塊 → 向量 → 可引用的問答**」這條線。

| 項目 | 內容 |
|---|---|
| Repo | `github.com/lfnovo/open-notebook` |
| 授權 | **MIT** |
| 版本 | `pyproject.toml` 標 **1.15.0**；我 clone 的 HEAD 是 `a0f6f30`（2026-10-04） |
| 社群規模 | 約 **4.1 萬星**、4.7 千 fork、1,019 commits |
| 後端 | Python **3.11–3.12**（`>=3.11,<3.13`）、FastAPI、LangGraph 1.x |
| 前端 | Next.js **16**、React 19、TypeScript、Tailwind 4、TanStack Query、Zustand |
| 資料庫 | **SurrealDB 2.x**（rocksdb 或記憶體） |
| 部署 | Docker Compose（官方推薦）、從原始碼、**Windows 原生**、單一容器（已棄用） |

### 跟 Google NotebookLM 的差別

| 面向 | Open Notebook | NotebookLM |
|---|---|---|
| 資料位置 | 自己機器 | Google 雲端 |
| 模型選擇 | 20+ 供應商，含 Ollama / LM Studio / vLLM 本地端 | 只有 Google 模型 |
| Podcast 講者 | **1–4 位**，可自訂人設 | 固定 2 位 |
| 介面 | REST API + **MCP server**（可接 Claude Desktop、VS Code） | 無 |
| 中文介面 | 有（含繁中） | 有 |
| 付費 | 免費（自付 API 或本地推論電費） | 分級訂閱 |

最後一列那個 **MCP** 對我很關鍵：它代表可以把這個知識庫接進我日常用的 coding agent，而不是只能開一個網頁慢慢問。

## 二、它可以做什麼

### 功能面

| 能力 | 具體內容 |
|---|---|
| 多模態來源 | PDF、影片、音檔、網頁、純文字；另有「轉換（transformation）」管線可自訂處理流程 |
| 搜尋 | **全文 BM25** 與**向量搜尋**並存，不是二選一 |
| 問答 | 以 notebook 為範圍的聊天，以及單一來源的深入追問 |
| 筆記 | 從對話生成筆記，掛在 notebook 底下 |
| Podcast | 1–4 位講者的對話式語音，可套人設 |
| 模型管理 | 在 UI 的 `Manage → Models` 設定供應商與預設模型，憑證加密存在 DB |
| 介面 | REST API（Swagger 在 `/docs`）、MCP server |

### 架構：四個程序，順序不能亂

<!-- FIG1 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 650" role="img" aria-label="Open Notebook 的四個程序與呼叫方向：瀏覽器經 Next.js 前端打到 FastAPI，後端把長工作丟進 SurrealDB 的 command 佇列，由背景 worker 取走；資料與向量都存在 SurrealDB，聊天歷史存在 SQLite，模型走 Ollama" style="width:100%;height:auto;display:block">
<defs><marker id="m7d8590" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7d8590"/></marker><marker id="m3fb950" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#3fb950"/></marker><marker id="mfbbf24" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#fbbf24"/></marker><marker id="mc084fc" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#c084fc"/></marker></defs>
<rect x="0.75" y="0.75" width="978.5" height="648.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">四個程序的實際呼叫方向</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">實線＝同步呼叫；佇列是 SurrealDB 裡的一張表，不是獨立的訊息中介</text>
<rect x="380" y="112" width="220" height="50" rx="10" fill="#161b22" stroke="#58a6ff66" stroke-width="1.5"/>
<text x="490.0" y="142.4" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">瀏覽器</text>
<path d="M 490 162 L 490 188" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<rect x="330" y="190" width="320" height="64" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="490.0" y="220.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Next.js 前端</text>
<text x="490.0" y="242.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">開發 :3000 ／ 映像 :8502 · 代理 /api/*</text>
<path d="M 490 254 L 490 290" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<text x="500" y="278" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">HTTP + SSE</text>
<rect x="330" y="292" width="320" height="64" rx="10" fill="#161b22" stroke="#2dd4bf66" stroke-width="1.5"/>
<text x="490.0" y="322.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">FastAPI 後端 :5055</text>
<text x="490.0" y="344.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">chat / ask 同步處理，長工作往外送</text>
<rect x="48" y="292" width="230" height="64" rx="10" fill="#161b22" stroke="#7d859066" stroke-width="1.5"/>
<text x="163.0" y="322.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">SQLite checkpoint</text>
<text x="163.0" y="344.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">聊天歷史存在這裡</text>
<path d="M 328 324 L 282 324" fill="none" stroke="#7d8590" stroke-width="2" marker-end="url(#m7d8590)"/>
<text x="305" y="314" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">存檔</text>
<rect x="730" y="292" width="200" height="64" rx="10" fill="#161b22" stroke="#3fb95066" stroke-width="1.5"/>
<text x="830.0" y="322.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Ollama :11434</text>
<text x="830.0" y="344.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8B 聊天 + bge-m3</text>
<path d="M 652 324 L 726 324" fill="none" stroke="#3fb950" stroke-width="2" marker-end="url(#m3fb950)"/>
<text x="689" y="314" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">模型呼叫</text>
<rect x="390" y="388" width="200" height="44" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="490.0" y="414.86" font-size="13.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">command 佇列</text>
<path d="M 420 358 L 420 386" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#mfbbf24)"/>
<text x="428" y="371" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">submit</text>
<rect x="730" y="388" width="200" height="64" rx="10" fill="#161b22" stroke="#fbbf2466" stroke-width="1.5"/>
<text x="830.0" y="418.0" font-size="15" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">背景 worker</text>
<text x="830.0" y="440.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8 個 command</text>
<path d="M 590 410 L 690 410" fill="none" stroke="#fbbf24" stroke-width="2"/>
<path d="M 690 410 L 726 410" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#mfbbf24)"/>
<text x="640" y="400" font-size="11" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">pick up</text>
<rect x="48" y="486" width="882" height="84" rx="10" fill="#161b22" stroke="#c084fc66" stroke-width="1.5"/>
<text x="489.0" y="526.0" font-size="16.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">SurrealDB 2.x :8000</text>
<text x="489.0" y="548.0" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">notebook · source · source_embedding · note · chat_session ｜ 圖邊 reference / artifact / refers_to ｜ fn::text_search（BM25）· fn::vector_search</text>
<path d="M 360 358 L 360 484" fill="none" stroke="#c084fc" stroke-width="2" marker-end="url(#mc084fc)"/>
<path d="M 830 454 L 830 484" fill="none" stroke="#c084fc" stroke-width="2" marker-end="url(#mc084fc)"/>
<path d="M 490 434 L 490 484" fill="none" stroke="#c084fc" stroke-width="1.5"/>
<text x="500" y="470" font-size="11" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">工作也存在 DB</text>
<circle cx="77" cy="612" r="7" fill="#2dd4bf"/>
<text x="92" y="616" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">前端 / 後端</text>
<circle cx="287" cy="612" r="7" fill="#fbbf24"/>
<text x="302" y="616" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">背景工作</text>
<circle cx="497" cy="612" r="7" fill="#c084fc"/>
<text x="512" y="616" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">資料庫</text>
<circle cx="707" cy="612" r="7" fill="#3fb950"/>
<text x="722" y="616" font-size="13" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">模型推論</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left"><strong>圖一：四個程序的實際呼叫方向。</strong>前端只跟 API 說話，API 把長工作寫進 SurrealDB 的 <code>command</code> 表，背景 worker 用 LIVE query 取走。沒有 worker，來源處理與向量化會永遠停在 Queued——這是最容易誤判成「程式壞了」的地方。</figcaption>
</figure>
<!-- /FIG1 -->

| # | 程序 | 埠 | 我的啟動方式 |
|---|---|---|---|
| 1 | SurrealDB | 8000 | `surreal start ... rocksdb:surreal_data\mydatabase.db` |
| 2 | API | 5055 | `.venv\Scripts\python.exe run_api.py` |
| 3 | 背景 worker | — | `uv run --env-file .env surreal-commands-worker --import-modules commands` |
| 4 | 前端 | 3000 | `npm run dev` |

**worker 不是選配。** 來源抽取、向量化、podcast 全都是背景工作；沒有 worker，工作會永遠停在「Queued」，而且**不會報錯**——你只會覺得「怎麼都沒動」。

### 幾個實作上的細節

- **聊天歷史不在 SurrealDB**：LangGraph 的 `SqliteSaver` 把它存在 `data/sqlite-db/checkpoints.sqlite`。所以備份要連這個檔一起備。
- **關係是圖邊不是外鍵**：`reference`（來源 → notebook）、`artifact`（筆記 → notebook）、`refers_to`（對話 → notebook/來源）。
- **搜尋是兩個 DB 函式**：`fn::text_search`（BM25）與 `fn::vector_search`。
- **所有模型呼叫都經過 Esperanto**（`esperanto` 套件），程式碼裡沒有直接呼叫任何供應商 SDK。內容超過 **105,000 tokens** 會自動切到 `large_context` 預設模型。
- **逾時預設 180 秒**（`ESPERANTO_LLM_TIMEOUT`），刻意設在 UI 的 600 秒之下。

## 三、我怎麼裝的（原生 Windows，沒有 Docker）

我的機器沒有 Docker，也不想為了試一個工具裝整包 Docker Desktop，所以走官方的 **Windows 原生**路線。

| 需求 | 官方要求 | 我的機器 | 處理 |
|---|---|---|---|
| Python | 3.11–3.12 | **3.15.1**（太新） | `uv` 依 `.python-version` 自動抓 **3.12.13** |
| uv | 需要 | 0.13.5 | ✅ |
| Node.js | ≥ 20.9 | 24.22.1 | ✅ |
| ffmpeg | 需要（podcast/影音） | 已有 | ✅ |
| SurrealDB | 2.x | 沒有 | 下載 `surreal-v2.7.0.windows-amd64.exe` |
| Docker | 只有資料庫需要 | 沒有 | 用原生 exe 取代 |

安裝流程只有四步：`uv sync`（含 dev 依賴）→ 寫 `.env` → 起 SurrealDB → 起 API/worker/前端。

**第一次啟動最慢的是遷移**：資料庫是空的，25 個 migration 一個約 6 秒，總共約 **3 分鐘**才看到 `{"status":"healthy"}`。之後每次啟動只要幾秒（`Database is already at the latest version`）。

## 四、實測：把它當真專案跑一遍

**測試語料**：`05_Prompt_Engineering_raw.md`，從 92 頁 PDF 簡報抽出的文字，**43,304 字元**，中英混排（每頁頁尾還有中文版權聲明）。

| 階段 | 結果 |
|---|---|
| 內容抽取 + 存檔（`process_source`） | **16.5 秒** |
| 切塊 + `bge-m3` 向量化（`embed_source`） | **106 個 chunk / 42.5 秒** |
| 向量搜尋（查「Chain-of-Thought 的實際例子」） | 命中正確段落，**相似度 0.6250** |
| 中文問答（8B） | **2,381 字**，含模型載入約 45–60 秒 |
| 中文問答（27B） | ❌ **7 分鐘無輸出**，手動中止 |

<!-- FIG2 -->
<figure style="margin:20px 0;padding:14px 12px;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 430" role="img" aria-label="實測數據：首次資料庫遷移 180 秒、內容抽取 16.5 秒、106 個 chunk 向量化 42.5 秒；27B 模型加 32k context 佔用 23,508 MiB，只剩約 1,056 MiB 給 KV cache" style="width:100%;height:auto;display:block">
<rect x="0.75" y="0.75" width="978.5" height="428.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/>
<text x="48" y="52" font-size="25" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">實測數據：耗時與 VRAM 預算</text>
<text x="48" y="82" font-size="14.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一台機器（RTX 4090 24 GB）、同一份 92 頁簡報；時間為秒，記憶體為 MiB</text>
<text x="48" y="128" font-size="16" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">① 處理耗時</text>
<text x="48" y="166" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">首次資料庫遷移（25 個 migration）</text>
<rect x="48" y="174" width="300" height="15" rx="4" fill="#1c2230" stroke="#222b36" stroke-width="1.5"/>
<rect x="48" y="174" width="300.0" height="15" rx="4" fill="#fbbf24" stroke="#fbbf24" stroke-width="1.5"/>
<text x="356" y="186" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">180 s</text>
<text x="48" y="228" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">向量化 106 個 chunk（bge-m3）</text>
<rect x="48" y="236" width="300" height="15" rx="4" fill="#1c2230" stroke="#222b36" stroke-width="1.5"/>
<rect x="48" y="236" width="70.83333333333334" height="15" rx="4" fill="#2dd4bf" stroke="#2dd4bf" stroke-width="1.5"/>
<text x="356" y="248" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">42.5 s</text>
<text x="48" y="290" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">內容抽取 + 存檔</text>
<rect x="48" y="298" width="300" height="15" rx="4" fill="#1c2230" stroke="#222b36" stroke-width="1.5"/>
<rect x="48" y="298" width="27.5" height="15" rx="4" fill="#58a6ff" stroke="#58a6ff" stroke-width="1.5"/>
<text x="356" y="310" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">16.5 s</text>
<text x="48" y="372" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">程式碼端量到的，不含模型載入時間。</text>
<text x="520" y="128" font-size="16" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">② VRAM 佔用（總量 24,564 MiB）</text>
<text x="520" y="176" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">27B + 32k context</text>
<rect x="520" y="184" width="350" height="17" rx="4" fill="#1c2230" stroke="#222b36" stroke-width="1.5"/>
<rect x="520" y="184" width="334.95359062042013" height="17" rx="4" fill="#f472b6" stroke="#f472b6" stroke-width="1.5"/>
<text x="878" y="197" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">23,508 MiB</text>
<text x="520" y="246" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">8B + bge-m3</text>
<rect x="520" y="254" width="350" height="17" rx="4" fill="#1c2230" stroke="#222b36" stroke-width="1.5"/>
<rect x="520" y="254" width="106.8637029799707" height="17" rx="4" fill="#3fb950" stroke="#3fb950" stroke-width="1.5"/>
<text x="878" y="267" font-size="12.5" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7,500 MiB</text>
<rect x="520" y="300" width="350" height="66" rx="8" fill="#1c2230" stroke="#f472b666" stroke-width="1.5"/>
<text x="536" y="324" font-size="13" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">27B 只剩 1,056 MiB 給 KV cache</text>
<text x="536" y="348" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 7 分鐘 0 token；8B 才是可用組合</text>
</svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left"><strong>圖二：耗時與 VRAM。</strong>左側是程式碼端量到的時間，右側是 27B 與 8B 的實測佔用。24,564 MiB 的 4090 扣掉 19 GB 權重後，32k context 的 KV cache 只剩約 1 GiB——這就是第一輪 7 分鐘吐不出 token 的原因，不是程式錯誤。</figcaption>
</figure>
<!-- /FIG2 -->

搜尋回傳的不是「一份文件」，而是**命中的段落原文**，這點做得很對：

```
### Chain-of-Thought (CoT) — Description
What it is
Chain-of-Thought prompting asks the model to reason through a
task step by step before giving the final answer. ...
<!-- ===== PDF page 42 ===== -->
similarity: 0.6249
```

`<!-- PDF page 42 -->` 這種標記是我原本從 PDF 抽文字時留下的，它**原封不動被保留下來**——所以引用可以追回原始頁碼。這是它比「丟進聊天視窗問」強的地方。

## 五、品質驗證：我怎麼確認它沒亂編

只有速度沒有意義，RAG 最容易壞的地方是「講得很順但是編的」。所以我出一個**必須讀完全部 92 頁才能回答**的問題：

> 用繁體中文回答：這份簡報的議程（Agenda）有哪幾項？請條列，並說明投影片中提到的進階提示（prompting）技術有哪些。

**8B 模型的回答**（2,381 字，節錄）：

- 議程 **4 項**：Introduction to Prompt Engineering、Advanced Techniques、Applications & Tools、Conclusion & Future Directions——與投影片第 3 頁完全一致。
- 進階技術整理成 **6 大類**：基礎技巧（Zero-Shot / Few-Shot）、情境與角色（System / Role / Contextual / Markdown）、推理與規劃（CoT / TCoT / SoT / Step-Back）、高階整合（Least-to-Most / ToT / iToT / Self-Generated）、風格語氣（Persona / Predictive）、專門化（Constitutional AI / Perspective-Taking / Analogical / Multi-Modal）。

看起來很漂亮，但**漂亮正是需要查證的時候**。我把答案裡每個技術名稱拿回原始檔逐一比對：

| 技術名稱 | 原文出現次數 | 技術名稱 | 原文出現次數 |
|---|---|---|---|
| Zero-Shot | 4 | Few-Shot | 7 |
| Chain-of-Thought | 10 | Tabular (TCoT) | 7 |
| Skeleton (SoT) | 6 | Step-Back | 7 |
| Least-to-Most | 6 | Tree-of-Thought | 8 |
| iToT | 3 | Self-Generated | 6 |
| Persona | 12 | Predictive | 7 |
| Constitutional | 7 | Perspective-Taking | 5 |
| Analogical | 7 | Multi-Modal | 6 |

**16 個完整名稱全部命中。** 剩下 4 個（Markdown / Role / System / Contextual Prompting）在原文裡是以基礎詞形式出現（Markdown 9 次、Role 15 次、System 12 次、Contextual 7 次），屬於模型自己歸類的標籤，不是憑空發明。

結論：**8B 模型對這份 92 頁中英混排簡報的整理是可信的**，而且抓得到「分類」這種需要跨頁整合的結構。以本地 8B 來說，這個表現超出我原本的預期。

## 六、但 27B 在我的 4090 上跑不動

我第一輪預設用 `qwen3.8-27b-uncensored-32k`，結果：

| 指標 | 數值 |
|---|---|
| 模型大小 | 19 GB |
| `num_ctx` | 32,768 |
| GPU 記憶體 | 23,508 / 24,564 MiB（**只剩約 1 GB**） |
| GPU 使用率 | 持續 100% |
| 等待時間 | **超過 7 分鐘，0 個 token** |
| 處置 | 手動 kill `llama-server`，換 8B 才有回應 |

原因不難理解：19 GB 權重 + 32k context 的 KV cache 幾乎吃光 24 GB 的 4090，加上我機器上原本就有模型佔用。**這不是 Open Notebook 的問題，是 VRAM 預算問題**，但你如果照預設值填 27B，第一句話就會卡在那裡，還以為程式壞了。

可用的組合（實測）：

| 模型 | 大小 | 結果 |
|---|---|---|
| `qwen3-8b-heretic-32k` | 7.5 GB | ✅ 順，中文品質可用 |
| `bge-m3`（嵌入） | — | ✅ 106 chunk / 42.5 秒 |
| `qwen3.8-27b-uncensored-32k` | 19 GB | ❌ 需降 `num_ctx` 或改用量化版 |

## 七、四個會咬人的坑

| 坑 | 症狀 | 原因與解法 |
|---|---|---|
| **`.env` 帶 BOM** | `uv` 報 `Failed to parse environment file .env at position 0: 锘?` | PowerShell 的 `-Encoding utf8` 會寫入 BOM。改用 `UTF8Encoding($false)`，否則**加密金鑰會讀錯**，而且不會報錯 |
| **`POST /api/sources` 不吃 JSON** | 回 `{"detail":[{"loc":["body","type"],"msg":"Field required"}]}` | 主端點是 multipart；純 JSON 要打 `POST /api/sources/json` |
| **追問時前端像「卡住」** | SSE 只回 `user_message`，長時間空白，最後一次吐出全文 | `graphs/source_chat.py` 用的是 `model.invoke()` 而非串流，節點跑完才送。不是壞掉 |
| **`embedded_chunks` 顯示 0** | 列表顯示 `embedded: true` 但 `embedded_chunks: 0` | 列表端點的計數沒對上；DB 裡實際有 106 塊，**功能正常、顯示錯誤** |

## 八、所以對我有什麼用

講功能不痛不癢，直接對照我手上的語料：

| 目錄 | 內容 | 規模 |
|---|---|---|
| `whisper_work` | 語音轉錄稿 | **2,219 檔 / 1.2 GB** |
| `pdf-notes-work` | PDF 抽頁、MathJax、插圖、檢查腳本 | 3,777 檔 / 73 MB |
| `blog_repo` | 這個站的 Markdown | 10,602 檔 / 358 MB |

**現況：沒有向量索引。** 我確認過，機器上沒有 ChromaDB、沒有 FAISS、也沒有任何 `.db` 形式的向量資料；能查的只有 `Select-String`。這正是 Open Notebook 對我有價值的地方。

### 它做得到 vs 它做不到

| 我想要 | Open Notebook | 為什麼 |
|---|---|---|
| 「我三年前對這件事寫過什麼？」並附出處 | ✅ **強項** | 向量 + BM25 混合，回傳段落原文與頁碼 |
| 中文摘要 92 頁簡報、整理成 6 大類 | ✅ 實測通過 | 8B 就夠，16/16 技術名稱可回查 |
| 完全本地、不外傳 | ✅ | Ollama + bge-m3，全程在 4090 上 |
| 把書變成 podcast | ✅（未測品質） | 1–4 講者，需接 TTS |
| 取代我的 PDF → MathJax HTML 產線 | ❌ | 抽取器把版面壓成純文字，**公式與圖表會掉** |
| 取代 `build_*_quiz.py` 題庫生成 | ❌ | 它輸出對話，不輸出可發佈的頁面 |
| 掃描版中文書 OCR | ❌ | 需選配 `docling`（很重）；我的手翻拍頁它處理不了 |
| 當筆記的最終儲存處 | ⚠️ 不建議 | 筆記存在 DB 裡，不是 `.md` 檔；我的站是 git 版控的檔案，兩邊並存等於兩份真相 |

### 我的結論：當「唯讀查詢層」，不要當產線

三條路，我選第一條：

1. **唯讀第二大腦（推薦）**：只匯入轉錄稿與想查的 PDF，用它問答；原本的產線完全不動。價值等於「省下每次翻舊帳的時間」。
2. **接 MCP 給 coding agent**：讓 Cline 這類工具直接查語料，取代 `grep` 加手寫檢查腳本。
3. **跳過**：如果九成時間都是「已知主題、要做成頁面」，那缺的不是這個工具，是更好的全文索引——SQLite FTS5 就夠，不需要 SurrealDB。

## 九、如果你也想裝：最小步驟

```powershell
git clone https://github.com/lfnovo/open-notebook.git
cd open-notebook
uv sync                                   # 會依 .python-version 抓 Python 3.12
cd frontend; npm install; cd ..
```

`.env`（**注意不要有 BOM**）：

```ini
OPEN_NOTEBOOK_ENCRYPTION_KEY=你的隨機字串   # 必填，沒有預設值
SURREAL_URL=ws://localhost:8000/rpc        # 主機端執行要用 localhost，不是 surrealdb
SURREAL_USER=root
SURREAL_PASSWORD=root
```

四個程序，依序啟動：

```powershell
surreal start --log info --user root --pass root rocksdb:surreal_data\mydatabase.db
.\.venv\Scripts\python.exe run_api.py
uv run --env-file .env surreal-commands-worker --import-modules commands --max-tasks 5
cd frontend; npm run dev
```

驗證：`curl http://localhost:5055/health` 應回 `{"status":"healthy"}`，UI 在 `http://localhost:3000`。

模型不要寫在 `.env` 裡（那條路已標示棄用），開 UI → `Manage → Models` 新增 Ollama 憑證（`base_url=http://localhost:11434`、`num_ctx` 依你的模型調整），再新增一個 `language` 模型與一個 `embedding` 模型（我用 `bge-m3`），最後在預設值把 chat / transformation / large_context / tools 指到同一個聊天模型。

## 十、結論

- **它是什麼**：MIT 授權、可自架的 NotebookLM 替代品，核心是「來源 → 向量 → 可引用問答」。
- **它能做什麼**：多模態來源、BM25 + 向量混合搜尋、中文問答、筆記、1–4 人 podcast、REST API 與 MCP。
- **對我有什麼用**：把散在 1.2 GB 轉錄稿與幾百頁 PDF 裡的東西變成可問、可引用的介面。**不會**替我產出頁面或題庫。

用一句話總結這次實測：**它的問答品質比我預期好，它的安裝成本也比我預期高。** 8B + bge-m3 在 4090 上是舒服的組合；27B 請先算好 VRAM 再填。四個常駐程序對「一個人維護的知識庫」確實偏重，但換來的是「問一句就帶著頁碼回來」——這件事我原本做不到。

> 本文的數據全部來自 2026-10-31 在本機的實際安裝與執行，測試語料為 `05_Prompt_Engineering_raw.md`（43,304 字元 / 92 頁）。文中引用的 repo 規格以 clone 到的 `a0f6f30`（v1.15.0）為準；上游更新後數字可能變動。



