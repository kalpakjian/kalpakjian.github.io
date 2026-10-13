---
title: 專題：IVDC LLM 與生成式 AI 課程筆記
date: 2026-10-13 09:00:00
---

這是 **IVDC（匯縱專業發展中心）「Certificate in Application of Large Language Model (LLM) (Part-time)」** 課程的學習筆記專題。

我把課程教材（PowerPoint 匯出的 PDF）逐份重寫成**可離線閱讀**的筆記，每一份都附 **60 題互動 MC 測驗**（點選即時計分、進度自動儲存）。

> 以下依**課程官方順序**（`Lesson Plan.docx`）排列；✅ 已完成，⏳ 尚未製作。

---

## 課程順序總覽

| 課節 | 主題 | 筆記 |
|:---:|---|---|
| **Lesson 1** | Introduction to Generative AI | ✅ [Introduction to AI 學習筆記](/ai-intro-notes/) |
| **Lesson 2** | Using Local GPU for ML | ✅ [Using Local GPU for ML 學習筆記](/local-gpu-ml-notes/) |
| **Lesson 2** | Popular LLM | ⏳ 待補 |
| **Lesson 3** | Introduction to LLM (Theory) | ✅ [Introduction to LLM 學習筆記](/llm-intro-notes/) |
| **Lesson 4** | Responsible LLM | ⏳ 待補 |
| **Lesson 4** | Test | — |
| **Lesson 5** | Prompt Engineering | ✅ [Prompt Engineering 學習筆記](/prompt-engineering-notes/) |
| **Lesson 6** | Hugging Face for LLM | ⏳ 待補 |
| **Lesson 7** | Local LLM Apps | ⏳ 待補 |
| **Lesson 8** | LiteLLM | ✅ [LiteLLM 學習筆記](/litellm-notes/) |
| **Lesson 9** | Streamlit and Flask | ✅ [Streamlit and Flask 學習筆記](/streamlit-flask-notes/) |
| **Lesson 10** | Exam | — |

> 📌 **Lesson 1 與 Lesson 2 的前半（Using Local GPU for ML）** 與
> [IVDC 電腦視覺課程專題](/cv-course/) 共用同一份筆記（兩門課的共同模組），此處直接連結，不重複製作。

---

## 1 · Lesson 3 — Introduction to LLM（Theory）

![Introduction to LLM 學習筆記](/img/covers/llm-intro-notes-ivdc.png)

- **涵蓋**：原稿 47 頁、**30 個章節**——LLM 的定義與「Large」的兩層意義、與早期 NLP 的差別、客製化 LLM、預訓練 vs 微調（含指令微調／分類微調）、Transformer 的 encoder／decoder、self-attention、BERT vs GPT、zero-shot／few-shot、token 與成本、自迴歸生成、GPT-3 規模，再到**後半的輸入處理管線實作**（分詞 → token ID → 特殊 token → 滑動視窗 → DataLoader → embedding → 位置編碼 → 完整管線）
- **特別之處**：原稿**有 21 頁沒有文字層**（只有圖與程式碼截圖），筆記把關鍵圖**重畫成 12 張內嵌 SVG**，
  並把後半的程式碼**在本機實測**（PyTorch 2.14.1+cu132、tiktoken GPT-2）後把真實輸出寫進筆記
- 另有 **30 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/llm-intro-notes/)** ｜ [互動測驗 60 題](/llm-intro-notes/mc-quiz.html)

---

## 2 · Lesson 5 — Prompt Engineering

![Prompt Engineering 學習筆記](/img/covers/prompt-engineering-notes-ivdc.png)

- **涵蓋**：原稿 92 頁、**38 個章節**——從 prompt 的定義與四大要素（Instructions／Context／Input data／Output indicator）、temperature 與 top_p 兩顆確定性旋鈕、**六大任務**（摘要／問答／分類／角色扮演／程式生成／推理），到原稿分出的**七大類技術**逐一展開：
  - **基礎**：Zero-Shot／Few-Shot（In-Context Learning）／Clear Instructions
  - **上下文與角色**：System／Role／Contextual／Markdown Prompting
  - **推理與規劃**：CoT／Tabular CoT／Skeleton-of-Thought／Step-Back
  - **進階編排**：Least-to-Most／Tree-of-Thoughts／Interactive ToT／Self-Generated ICL
  - **專業與前沿**：Constitutional AI／Perspective-Taking／Analogical／Multi-Modal／Persona Consistency／Predictive
  - **知識與工具**：Generate Knowledge／PAL／ReAct
  - **應用與安全**：LLM + 外部工具三元件、Data-Augmented Generation、Model Safety、Prompt Injection／Leaking／Jailbreaking、RLHF
- **特別之處**：原稿把 20 幾頁 `Classroom Exercise` 寫成「**同一題目、有／沒有用該技術**」的成對示範，
  筆記逐題保留這個對照，並補上**可直接複製的 prompt 範本**與「**易混淆技術對照表**」（CoT vs ToT vs PAL vs ReAct、CAI vs RLHF…）
- 另有 **38 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/prompt-engineering-notes/)** ｜ [互動測驗 60 題](/prompt-engineering-notes/mc-quiz.html)

---

## 3 · Lesson 8 — LiteLLM

![LiteLLM 學習筆記](/img/covers/litellm-notes-ivdc.png)

- **涵蓋**：原稿 **18 格 notebook ＋ `lite.py`**、**22 個章節**——從 LiteLLM 的定位（**用 OpenAI chat 格式統一呼叫 146 個供應商**）、安裝與 API Key 管理，到原稿的五個供應商呼叫逐一拆解：
  - **五大供應商**：ChatGPT（`gpt-3.5-turbo`）／Claude-2（`claude-2`）／llama2 on Replicate（含 64 字元版本雜湊）／Command-Nightly（Cohere）／Azure OpenAI（`azure/` 前綴與 deployment-id）
  - **本機模型**：`lite.py` 逐行拆解——`api_base` 為什麼是「critical for local Ollama」、`temperature=0` 與 `top_p=1` 的意義
  - **補充章節**：模型命名規則與前綴總表、統一 I/O 契約、`messages` 三種角色、參數速查、串流輸出、例外類別、能力查詢、Token 計數、成本追蹤、Router／Fallbacks、LiteLLM Proxy
- **特別之處**：所有程式碼都在本機實測（litellm 1.91.2／openai 2.24.0／Ollama `smollm`），並把**「原稿當時正確、現在已失效」的三個落差**標出來：
  - `completion(model="claude-2", ...)` 在 1.91.2 會丟 `BadRequestError`，必須改 `anthropic/claude-2`
  - 原稿寫「50+ LLM APIs」，實測 `provider_list` 已有 **146** 個
  - 原稿用 `OpenAIObject` 描述回應，現為 LiteLLM 的 **`ModelResponse`**
- 另有 **22 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/litellm-notes/)** ｜ [互動測驗 60 題](/litellm-notes/mc-quiz.html)

---

## 4 · Lesson 9 — Streamlit and Flask

![Streamlit and Flask 學習筆記](/img/covers/streamlit-flask-notes-ivdc.png)

- **涵蓋**：原稿 `server.py`（12 行）＋ `app.py`（46 行）＋ `README.md`／`ReadMe.txt`、**22 個章節**——把三課串成一條線：
  - **Flask 後端**：微框架、`@app.route` 與 `methods`（不寫就只有 GET）、`request.get_json()`、`jsonify()` 的中文編碼、400／404／405／415／500 六個狀態碼
  - **測試**：`test_client`（不開埠號）與 `requests`／`curl`（真實網路）三種方式的取捨
  - **Streamlit 前端**：**每次互動重跑整支腳本**（最重要的觀念）、`st.session_state` 與 `@st.cache_data`、常用元件、`st.button` 的事件機制、label 重複陷阱
  - **整合**：`app.py` 的**兩個獨立區塊**——區塊 1 走 Flask、區塊 2 直連 LiteLLM→Ollama；啟動順序與三個埠號（5000／8501／11434）
- **特別之處**：找出原稿裡**會直接讓使用者看到 500 錯誤的三個真實缺陷**並給出正確改法，
  其中最關鍵的是 **`dict.get(k, default)` 的 `default` 只在 key 不存在時生效**——所以 `{"name": null}` 會回出 `"Hello, None ..."`
- 另有 **22 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/streamlit-flask-notes/)** ｜ [互動測驗 60 題](/streamlit-flask-notes/mc-quiz.html)

---

## 筆記的共同規格

| 項目 | 說明 |
|---|---|
| 格式 | **單一 HTML 檔、零外部資源**，下載後可離線雙擊開啟 |
| 版面 | 左側固定側邊欄 + **自動產生的巢狀目錄樹**（不會有壞連結） |
| 測驗 | 每份 **60 題互動 MC**：即時計分、進度存 localStorage、可列印 |
| 附錄 | 名詞與架構速查表、常見錯誤與陷阱、教材頁面索引對照、離線執行提示、一頁精華（考前 10 分鐘） |
| 原始檔 | 每頁都可下載原始 Markdown |
| 來源 | 忠實對照原稿每一個標題逐節重寫，並補上考點、指令與**本機實測數據** |

---

*教材內容版權屬匯縱專業發展中心（IVDC）所有；本專題僅為個人學習筆記整理。*
