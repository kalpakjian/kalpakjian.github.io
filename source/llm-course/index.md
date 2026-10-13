---
title: 專題：IVDC LLM 與生成式 AI 課程筆記
date: 2026-10-13 09:00:00
---

這是 **IVDC（匯縱專業發展中心）「Certificate in Application of Large Language Model (LLM) (Part-time)」** 課程的學習筆記專題。

我把課程內容逐份整理成**可離線閱讀**的筆記，每一份都附 **60 題互動 MC 測驗**（點選即時計分、進度自動儲存）。

> 以下依**課程官方順序**（`Lesson Plan.docx`）排列；✅ 已完成，⏳ 尚未製作。

---

## 課程順序總覽

| 課節 | 主題 | 筆記 |
|:---:|---|---|
| **Lesson 1** | Introduction to Generative AI | ✅ [Introduction to AI 學習筆記](/ai-intro-notes/) |
| **Lesson 2** | Using Local GPU for ML | ✅ [Using Local GPU for ML 學習筆記](/local-gpu-ml-notes/) |
| **Lesson 2** | Popular LLM | ✅ [Popular LLM Models 學習筆記](/popular-llm-notes/) |
| **Lesson 3** | Introduction to LLM (Theory) | ✅ [Introduction to LLM 學習筆記](/llm-intro-notes/) |
| **Lesson 4** | Responsible LLM | ✅ [Responsible AI 學習筆記](/responsible-ai-notes/) |
| **Lesson 4** | Test | — |
| **Lesson 5** | Prompt Engineering | ✅ [Prompt Engineering 學習筆記](/prompt-engineering-notes/) |
| **Lesson 6** | Hugging Face for LLM | ✅ [Hugging Face for LLM 學習筆記](/huggingface-notes/) |
| **Lesson 7** | Local LLM Apps | ✅ [Local LLM Apps 學習筆記](/local-llm-notes/) |
| **Lesson 8** | LiteLLM | ✅ [LiteLLM 學習筆記](/litellm-notes/) |
| **Lesson 9** | Streamlit and Flask | ✅ [Streamlit and Flask 學習筆記](/streamlit-flask-notes/) |
| **Lesson 10** | Exam | — |

> 📌 **Lesson 1 與 Lesson 2 的前半（Using Local GPU for ML）** 與
> [IVDC 電腦視覺課程專題](/cv-course/) 共用同一份筆記（兩門課的共同模組），此處直接連結，不重複製作。
>
> 📌 **Lesson 4（Responsible LLM）** 的內容與電腦視覺課程的
> [Responsible AI 學習筆記](/responsible-ai-notes/) 高度重疊（同一份本節家族，僅 14 頁），
> 因此比照 Lesson 1 的做法直接連結，不重複製作。

---

## 1 · Lesson 2 — Popular LLM Models

![Popular LLM Models 學習筆記](/img/covers/popular-llm-notes-ivdc.png)

- **涵蓋**：**33 個章節**——三條主線一路展開：
  - **產品線**：ChatGPT（含 GPT 三個字母的展開）／Gemini（舊名 Bard）／Copilot／Llama（**開放權重**）／Grok（**xAI**）／Perplexity（**AI 搜尋引擎**）／Kimi／通義（**Qwen**）／DeepSeek，以及「**與 Google 搜尋有何不同**」的五層對比
  - **原理線**：Predictive AI（五類演算法、四領域、**五步流程**）vs Generative AI（四種核心技術、三階段運作），再到 **GAN**（生成器／判別器、零和對抗、交替訓練、收斂與崩壞、損失函數）與 **Diffusion**（Forward 加噪／Reverse 去噪、SDE、DDPM、**DDIM 是加速取樣器**）
  - **應用線**：Hybrid AI 的**兩種**定義、醫療／電商／招聘三案例、RAG（**不訓練模型，只建索引**）、**LLM vs RAG** 的五維對照
  四支 Lab（`LLM.ipynb`／`RAG.ipynb`／`Predictive AI.ipynb`／`Gen AI.ipynb`）全部在本機實測
  （torch 2.14.1+cu132／transformers 5.17.0／RTX 4090），真實輸出直接寫進內文
- **抓到的兩個問題**：
  - `RAG.ipynb` 的 `max_length=50` 遇上 **153 token** 的 prompt → 直接 `ValueError`（要改 **`max_new_tokens`**）
  - 本節說 SD 生成「may take **30-60 seconds**」，本機 4090 只要 **0.61 秒**（數字來自 Colab T4）
- 另有 **33 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/popular-llm-notes/)** ｜ [互動測驗 60 題](/popular-llm-notes/mc-quiz.html)

---

## 2 · Lesson 3 — Introduction to LLM（Theory）

![Introduction to LLM 學習筆記](/img/covers/llm-intro-notes-ivdc.png)

- **涵蓋**：**30 個章節**——LLM 的定義與「Large」的兩層意義、與早期 NLP 的差別、客製化 LLM、預訓練 vs 微調（含指令微調／分類微調）、Transformer 的 encoder／decoder、self-attention、BERT vs GPT、zero-shot／few-shot、token 與成本、自迴歸生成、GPT-3 規模，再到**後半的輸入處理管線實作**（分詞 → token ID → 特殊 token → 滑動視窗 → DataLoader → embedding → 位置編碼 → 完整管線）
  並把後半的程式碼**在本機實測**（PyTorch 2.14.1+cu132、tiktoken GPT-2）後把真實輸出寫進筆記
- 另有 **30 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/llm-intro-notes/)** ｜ [互動測驗 60 題](/llm-intro-notes/mc-quiz.html)

---

## 3 · Lesson 5 — Prompt Engineering

![Prompt Engineering 學習筆記](/img/covers/prompt-engineering-notes-ivdc.png)

- **涵蓋**：**38 個章節**——從 prompt 的定義與四大要素（Instructions／Context／Input data／Output indicator）、temperature 與 top_p 兩顆確定性旋鈕、**六大任務**（摘要／問答／分類／角色扮演／程式生成／推理），到本節分出的**七大類技術**逐一展開：
  - **基礎**：Zero-Shot／Few-Shot（In-Context Learning）／Clear Instructions
  - **上下文與角色**：System／Role／Contextual／Markdown Prompting
  - **推理與規劃**：CoT／Tabular CoT／Skeleton-of-Thought／Step-Back
  - **進階編排**：Least-to-Most／Tree-of-Thoughts／Interactive ToT／Self-Generated ICL
  - **專業與前沿**：Constitutional AI／Perspective-Taking／Analogical／Multi-Modal／Persona Consistency／Predictive
  - **知識與工具**：Generate Knowledge／PAL／ReAct
  - **應用與安全**：LLM + 外部工具三元件、Data-Augmented Generation、Model Safety、Prompt Injection／Leaking／Jailbreaking、RLHF
- **特別之處**：本節把 20 幾頁 `Classroom Exercise` 寫成「**同一題目、有／沒有用該技術**」的成對示範，
  筆記逐題保留這個對照，並補上**可直接複製的 prompt 範本**與「**易混淆技術對照表**」（CoT vs ToT vs PAL vs ReAct、CAI vs RLHF…）
- 另有 **38 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/prompt-engineering-notes/)** ｜ [互動測驗 60 題](/prompt-engineering-notes/mc-quiz.html)

---

## 4 · Lesson 6 — Hugging Face for LLM

![Hugging Face for LLM 學習筆記](/img/covers/huggingface-notes-ivdc.png)

- **涵蓋**：**43 個章節**——從「模型從哪裡來」一路講到「怎麼改、怎麼上線」：
  - **生態系三層架構**（本節骨架）：**① Hub ② Core ML Libraries ③ Inference & Deployment**
  - **Hub 四件套**：Model Hub（**300k+ 模型**）／Dataset Hub／**Spaces**（Gradio／Streamlit／Static／Docker）／文件與版控
  - **核心函式庫**：`transformers`／`datasets`／`tokenizers`／`diffusers`／**`peft`**
  - **三種 Tokenizer 深入對比**（本節用 **10 頁**講這個，是全課考題最密集處）：
    **WordPiece**（`##`、最大似然合併、BERT 系）／**BPE**（byte-level、貪婪合併、GPT 系）／**SentencePiece**（`▁`、BPE 或 Unigram、T5／LLaMA）
  - **微調技術**：**PEFT = LoRA／QLoRA／Adapters**，LoRA 公式 **`W' = W + A × B`**、QLoRA = LoRA ＋ **4-bit（NF4 ＋ double quantization）**
  - **部署工具鏈**：Accelerate／Optimum／**TGI**／**Inference Endpoints**／**Safetensors**／`huggingface_hub`／Model Cards
- **三個 Lab 逐格拆解**：`HF_transformer.ipynb`（11 格，**ViT 影像 ＋ AST 音訊**）、`HF_LLM.ipynb`（**PEFT／LoRA**）、`HF_dataset.ipynb`（**AG News ＋ Tiny ImageNet**）
- **本機實測完全複現本節數字**（RTX 4090）：LoRA 的 **`147,456 / 82,060,032 / 0.1797%`**、影像的 **`book jacket 12.9%`**、音訊的 **`Ding 55.9%`**——證明本節**技術內容正確**
- **實測抓到的問題共 14 項**，其中三個最嚴重：
  - **`target_modules=["c_attn"]` 只對 GPT-2 有效**——換成 Llama／Qwen 會直接 **`ValueError`**（可攜寫法是 `"all-linear"`）
  - **`peft` 因為 `torchaudio` CUDA 版本不符而完全無法匯入**，錯誤訊息卻指向 `BloomPreTrainedModel`，**完全誤導**；解法是 `pip uninstall -y torchaudio`（**實查確認：torchaudio 根本沒有 cu132 建置**，最高只到 2.11.0+cu130，所以這不是裝錯、是只能這樣裝）
  - **本節用兩頁教 Streaming，三個 Lab 一次都沒用**——實測串流取 200 筆 **0.002 秒** vs 完整下載 **12.58 秒**
  - 其餘包括：**p34 ＝ p35 整頁重複**、**註解說 DeiT 卻用 ViT**、**說用 wav2vec2 卻用 AST**、**熱連結新聞站裁切圖導致 12.9% 的失敗預測卻不加說明**、**Tiny ImageNet 已按類別排序使「找魚」示範失效**、**`Adaptors` 拼錯**、**QLoRA 全名誤植**、**p39 空項目符號**、**`LoRA.txt` 的 `matrics`**
- **⚠️ 過時資訊已逐項查證更正**（2026-10）：
  - **Model Hub「300k+ models」→ 實查已是 `2M+`**（約 6.7 倍），Datasets 也已是 `500k+`
  - **`hf cache scan` 是錯的指令**（不存在）；正確是 `hf cache list`／`prune`／`rm`／`verify`
  - **`hf` CLI 實際有 25+ 個子指令**（原筆記只列 4 個）
  - **`huggingface_hub` 最新已是 `2.2.0`**（本機實測用 1.24.0，跨大版本）
  - 附「**本機實測 vs 最新**」完整版本對照表
- 另有 **43 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **👉 [看筆記](/huggingface-notes/)** ｜ [互動測驗 60 題](/huggingface-notes/mc-quiz.html)

---

## 5 · Lesson 7 — Local LLM Apps

![Local LLM Apps 學習筆記](/img/covers/local-llm-notes-ivdc.png)

- **涵蓋**：**39 個章節**——四個桌面 App 各一段操作手冊，再加上 Lab 與 NLP 補充：
  - **LM Studio**：下載安裝 → 首跑引導（`google/gemma-3-4b`，3.34 GB）→ **`GPU Offload`／`Context Length`** → 從 Hugging Face 抓 **`TheBloke/deepseek-llm-7B-base-GGUF`（`Q4_K_S`，4.03 GB）** → **附加檔案問答**
  - **Ollama**：`ollama run` → **模型選擇表**（六個模型的參數與大小）→ `list`／`serve`／**埠 11434** → 用 Python 打 REST API
  - **AnythingLLM**：工作區（Workspace）與 **provider 清單**（含 **Ollama／LM Studio**）
  - **GPT4All**：**My Documents**、允許的副檔名 `docx,pdf,txt,md,rst`、**對自己的檔案提問**
  - **Lab**：`testollama.py`、`app_web.py`、`LangChain.ipynb`、`LangIndex.ipynb`、`RAG.ipynb`、`train.py`、`Modelfile`
  - **NLP 補充**（95 頁 deck）：Tokenizing／停用詞／Stemming／Lemmatizing／POS／Chunking／NER／文字分類／**Extractive vs Abstractive 摘要**
  筆記逐頁補上「**這一步在做什麼、為什麼**」，並在每節標明對應 PDF 頁碼
- **實測抓到的問題共 14 項**，其中兩個最嚴重：
  - **`testollama.py` 寫死 `"model": "llama3"`**——**不在本節自己的模型表裡**，照著做一定 **HTTP 404**
  - **`LangIndex.ipynb` 把真實的 Groq API key 寫死在程式碼裡**，而且**沒有那把 key 的學員根本跑不動** →
    筆記提供「**改用 `llama-index-llms-ollama`**」的替代路徑（只需改 3 個地方），並在本機實測跑通
  - 其餘包括：`train.jsonl` **73 行只有 1 個唯一樣本**、`train.py` **教 LoRA 卻是全參數微調**、
    `Modelfile` 的 **`TEMPLATE {{ .Prompt }}` 沒有角色標記**、`RAG.ipynb` 的 **`max_length` 誤用**、
    `torch.tensor([ord(c)…])` **假嵌入**、`GTP4ALL`／`Imstudio` 拼字錯誤、`phi3` **三種寫法**、
    `ReadMe.txt` 沿用講師帳號路徑
- **本機實測數據**（Ollama 0.40.3）：`smollm` 對話 **1.38 秒**、RAG 建索引 **0.10 秒**／查詢 **0.43 秒**、
  **模型不存在回 404**、`mymodel` 其實是 **GPT-2 124M**
- 另有 **39 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **⚠️ 版本時效已查證（2026-10）**：**Ollama 0.40.3 查證後仍是目前最新版**（2026-10-11 發布），所以全部 Ollama 實測數字仍然有效；
  但 **LM Studio 已到 `0.4.26`**（本筆記撰寫時是  0.4.6，落後 20 個 patch），且 **`huggingface_hub[cli]` 這個 extra 已被移除**（CLI 指令是 `hf`，不是 `huggingface-cli`）。見筆記 **§38.9**
- **👉 [看筆記](/local-llm-notes/)** ｜ [互動測驗 60 題](/local-llm-notes/mc-quiz.html)

---

## 6 · Lesson 8 — LiteLLM

![LiteLLM 學習筆記](/img/covers/litellm-notes-ivdc.png)

- **涵蓋**：本節 **18 格 notebook ＋ `lite.py`**、**22 個章節**——從 LiteLLM 的定位（**用 OpenAI chat 格式統一呼叫 146 個供應商**）、安裝與 API Key 管理，到五個供應商呼叫逐一拆解：
  - **五大供應商**：ChatGPT（`gpt-3.5-turbo`）／Claude-2（`claude-2`）／llama2 on Replicate（含 64 字元版本雜湊）／Command-Nightly（Cohere）／Azure OpenAI（`azure/` 前綴與 deployment-id）
  - **本機模型**：`lite.py` 逐行拆解——`api_base` 為什麼是「critical for local Ollama」、`temperature=0` 與 `top_p=1` 的意義
  - **補充章節**：模型命名規則與前綴總表、統一 I/O 契約、`messages` 三種角色、參數速查、串流輸出、例外類別、能力查詢、Token 計數、成本追蹤、Router／Fallbacks、LiteLLM Proxy
- **特別之處**：所有程式碼都在本機實測（litellm 1.91.2／openai 2.24.0／Ollama `smollm`），並把**「本節當時正確、現在已失效」的三個落差**標出來：
  - `completion(model="claude-2", ...)` 在 1.91.2 會丟 `BadRequestError`，必須改 `anthropic/claude-2`
  - 本節寫「50+ LLM APIs」，實測 `provider_list` 已有 **146** 個
  - 本節用 `OpenAIObject` 描述回應，現為 LiteLLM 的 **`ModelResponse`**
- 另有 **22 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **⚠️ 版本時效已查證（2026-10）**：**`litellm 1.91.2` → 最新 `1.105.0`**（落後 14 個 minor），
  底層 **`openai` 已從 2.x 跨到 `3.29.0`**（大版本，例外階層可能改名）；
  且官方現在定位為「**Rust core ＋ Python SDK** 的 AI Gateway」（支援 **100+** LLM API，程式內 `provider_list` 實測 **146**）。見筆記 **§2.1**
- **👉 [看筆記](/litellm-notes/)** ｜ [互動測驗 60 題](/litellm-notes/mc-quiz.html)

---

## 7 · Lesson 9 — Streamlit and Flask

![Streamlit and Flask 學習筆記](/img/covers/streamlit-flask-notes-ivdc.png)

- **涵蓋**：`server.py`（12 行）＋ `app.py`（46 行）＋ `README.md`／`ReadMe.txt`、**22 個章節**——把三課串成一條線：
  - **Flask 後端**：微框架、`@app.route` 與 `methods`（不寫就只有 GET）、`request.get_json()`、`jsonify()` 的中文編碼、400／404／405／415／500 六個狀態碼
  - **測試**：`test_client`（不開埠號）與 `requests`／`curl`（真實網路）三種方式的取捨
  - **Streamlit 前端**：**每次互動重跑整支腳本**（最重要的觀念）、`st.session_state` 與 `@st.cache_data`、常用元件、`st.button` 的事件機制、label 重複陷阱
  - **整合**：`app.py` 的**兩個獨立區塊**——區塊 1 走 Flask、區塊 2 直連 LiteLLM→Ollama；啟動順序與三個埠號（5000／8501／11434）
- **特別之處**：找出**會直接讓使用者看到 500 錯誤的三個真實缺陷**並給出正確改法，
  其中最關鍵的是 **`dict.get(k, default)` 的 `default` 只在 key 不存在時生效**——所以 `{"name": null}` 會回出 `"Hello, None ..."`
- 另有 **22 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **⚠️ 版本時效已查證（2026-10）**：**Flask 3.1.3 查證後仍是目前最新版**，所以全部 Flask 實測數字仍然有效；
  但 **Streamlit 已到 `1.65.0`**（實測用 1.59.1，落後 6 個 minor）。見筆記 **§20.6**
- **👉 [看筆記](/streamlit-flask-notes/)** ｜ [互動測驗 60 題](/streamlit-flask-notes/mc-quiz.html)

---

## 筆記的共同規格

| 項目 | 說明 |
|---|---|
| 格式 | **單一 HTML 檔、零外部資源**，下載後可離線雙擊開啟 |
| 版面 | 左側固定側邊欄 + **自動產生的巢狀目錄樹**（不會有壞連結） |
| 測驗 | 每份 **60 題互動 MC**：即時計分、進度存 localStorage、可列印 |
| 附錄 | 名詞與架構速查表、常見錯誤與陷阱、離線執行提示、一頁精華（考前 10 分鐘） |
| 原始檔 | 每頁都可下載原始 Markdown |
| 來源 | 依課程大綱逐節重寫，並補上考點、指令與**本機實測數據** |

---

*本專題為個人學習筆記整理。*
