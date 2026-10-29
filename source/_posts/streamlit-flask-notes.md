---
title: Streamlit and Flask 學習筆記（Lesson 9）
date: 2026-10-13 11:45:00
tags:
  - LLM
  - Streamlit
  - Flask
  - 學習筆記
  - Python
categories:
  - AI
  - 學習筆記
cover: /img/covers/streamlit-flask-notes.png
banner_img: /img/covers/streamlit-flask-notes.png
index_img: /img/covers/streamlit-flask-notes.png
archive: true
---

![Streamlit and Flask 學習筆記](/img/covers/streamlit-flask-notes.png)

「Certificate in Application of Large Language Model (LLM)」**Lesson 9 — Streamlit and Flask** 的完整學習筆記。

這課把前面幾課串起來：**Streamlit 做前端畫面、Flask 做後端 API、LiteLLM 呼叫本機 Ollama**。課程只有兩支加起來 58 行的程式，但裡面藏了 **兩個會直接回 500 的真實漏洞**。

<!-- more -->

## 這份筆記有什麼

- **`server.py`（12 行）、`app.py`（46 行）逐行重寫**，並補上 `README.md`／`ReadMe.txt` 的架構與啟動說明
- **所有程式碼都在本機實測**（Flask 3.1.3／Werkzeug 3.1.8／Streamlit 1.59.1／requests 2.33.0），實測輸出直接寫進內文
- **22 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **60 題互動 MC 測驗**（點選即時計分、進度自動存 localStorage）

## 章節

| # | 章節 |
|---|------|
| 1 | 為什麼要拆成前端與後端 |
| 2 | Flask 是什麼：最小應用 |
| 3 | 路由與 HTTP 方法（`@app.route`） |
| 4 | 第一個端點 `/greet` |
| 5 | `request.get_json()` 與它的危險邊界 |
| 6 | `jsonify()` 與中文編碼 |
| 7 | 錯誤狀態碼總表 |
| 8 | 用 `test_client` 測 Flask（不必開埠號） |
| 9 | 用 `requests` / `curl` 測真實 HTTP |
| 10 | Streamlit 是什麼：最小應用 |
| 11 | Streamlit 的執行模型：每次互動重跑整個腳本 |
| 12 | 常用 Streamlit 元件 |
| 13 | 表單互動：`st.button` 與回傳值 |
| 14 | 呼叫後端：`requests.post` |
| 15 | 錯誤處理與使用者回饋 |
| 16 | `st.spinner` 與等待體驗 |
| 17 | 整合 LiteLLM + Ollama |
| 18 | 啟動順序與連接埠 |
| 19 | 完整架構圖與資料流 |
| 20 | 本機實測總表（真實數據） |
| 21 | 常見錯誤與陷阱 |
| 22 | 考試重點整理 |

另有 **7 個附錄**：API 速查表、常見錯誤與陷阱、離線執行／安裝提示、一頁精華（考前 10 分鐘）、60 題 MC 互動測驗、答錯題目 → 複習章節

---

## 重點：60 題 MC 模擬試卷

**🖱️ [開始 60 題線上測驗](/streamlit-flask-notes/mc-quiz.html)**

- 60 題單選、滿分 60 分、建議 75 分鐘
- 分四個部分、依課程檔案與行號順序排列
- 答案分佈刻意打散（A/B/C/D 各 15 題）
- 點選即時計分、進度存在 localStorage、可切換「只看未答／只看答錯」

> 出題率最高的考點包括：**Flask 5000／Streamlit 8501／Ollama 11434**、
> **`methods` 不寫就只有 GET**、
> **405 vs 415 vs 400 vs 500 的差別**、
> **`st.button()` 只在被按下的那次重跑回 True**、
> **每次互動重跑整支腳本 → 用 `st.session_state`／`@st.cache_data`**、
> **`json=` 不是 `data=`**、
> **`requests` 預設沒有逾時**，
> 以及 **`app.py` 的兩個獨立區塊（一個走 Flask、一個直連 Ollama）**。

---

## ⚠️ 兩個真實漏洞

這份筆記最有價值的地方，是把課程裡**會直接讓使用者看到 500 錯誤**的地方找出來並給出正確改法：

| 位置 | 問題 | 正確做法 |
|---|---|---|
| `server.py` 的 `data.get(...)` | body 送 `[]`／`"abc"`／`42` → **HTTP 500** | 加 `isinstance(data, dict)` 檢查，回 **400** |
| `server.py` 的 `data.get("name", "Guest")` | `{"name": null}` → 回應變成 **`"Hello, None ..."`** | 用 `data.get("name") or "Guest"` |
| `app.py` 的 `else: st.error("Could not reach...")` | 405／500 也被說成「連不上」，誤導除錯 | 依 `status_code` 給不同訊息 |

**關鍵觀念**：`dict.get(k, default)` 的 `default` **只在 key 不存在時生效** —— key 存在但值是 `null` 時它會回 `None`。

---

## 本機實測的真實數字

| 項目 | 實測值 |
|---|---|
| `POST /greet` 往返 | **2.3 ms** |
| `Server` 標頭 | `Werkzeug/3.1.8 Python/3.11.15` |
| `GET /greet`（只註冊 POST） | **405**，`Allow: OPTIONS, POST` |
| `POST /greet` 送 `[]` | **500**（`AttributeError`） |
| `POST /greet` 送 `text/plain` | **415** |
| `POST /greet` 送壞 JSON | **400** |
| Streamlit `/_stcore/health` | **200 `ok`** |
| LiteLLM → Ollama | **2.82 s** |

---

## 離線也能用

筆記是**單一 HTML 檔、零外部資源**（CSS、語法高亮、22 張章節插圖全部內嵌），下載後直接雙擊就能看。

也可以下載原始 Markdown：

**📄 [Streamlit_Flask_Study_Notes.md](/streamlit-flask-notes/Streamlit_Flask_Study_Notes.md)**

---

## 建議使用順序

1. 先讀 §1–§4（架構、Flask 基礎、路由、`/greet`）
2. 重點讀 §5（`get_json()` 的危險邊界）與 §7（狀態碼），這兩節最常考
3. 讀 §8–§9，學會用 `test_client` 與 `requests` 兩種方式測 API
4. 讀 §10–§13，**務必弄懂「每次互動重跑整支腳本」**（§11）
5. 讀 §14–§17，把 `app.py` 的兩個區塊資料流畫一遍
6. 讀 §18–§21（啟動順序、架構、實測、陷阱）
7. 找個安靜的 75 分鐘，完整做一次**附錄 E 的 60 題線上互動測驗**
8. 考前 10 分鐘只看**附錄 D 一頁精華**

祝考試順利。

---

*本篇為個人學習筆記整理。*
