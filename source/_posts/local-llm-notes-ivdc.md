---
title: Local LLM Apps 學習筆記（IVDC Lesson 7）
date: 2026-10-13 12:20:00
tags:
  - LLM
  - Ollama
  - LM Studio
  - GPT4All
  - AnythingLLM
  - RAG
  - IVDC
  - 學習筆記
  - Python
categories:
  - AI
  - 學習筆記
cover: /img/covers/local-llm-notes-ivdc.png
banner_img: /img/covers/local-llm-notes-ivdc.png
index_img: /img/covers/local-llm-notes-ivdc.png
archive: true
---

![Local LLM Apps 學習筆記](/img/covers/local-llm-notes-ivdc.png)

IVDC「Certificate in Application of Large Language Model (LLM)」**Lesson 7 — Local LLM Apps** 的完整學習筆記。

這一課的主題很單純：**把 LLM 裝在自己的電腦上跑**。教材用四個桌面應用程式走完一遍——LM Studio、Ollama、AnythingLLM、GPT4All——然後課程附的 Lab 資料夾再把同一件事**用程式重做一次**。

<!-- more -->

## 這份筆記有什麼

- **教材 44 頁逐頁重寫**。⚠️ 但教材 **43 頁是純截圖**（全份文字層只有約 2,705 字元），
  所以筆記逐頁補上「**這一步在做什麼、為什麼**」，並在每節標明對應的 PDF 頁碼
- **四個 App 完整拆解**：
  - **LM Studio**：下載 → 首跑引導 → **GPU Offload 與 Context Length** → 從 Hugging Face 抓 GGUF → 附加檔案問答
  - **Ollama**：安裝 → `ollama run` → **模型選擇表** → `list`／`serve`／**埠 11434** → 用 Python 打 REST API
  - **AnythingLLM**：工作區、provider 清單（含 **Ollama／LM Studio**）
  - **GPT4All**：**My Documents**、允許的副檔名、**對自己的檔案提問**
- **Lab 逐行拆解**：`testollama.py`、`app_web.py`、`LangChain.ipynb`、`LangIndex.ipynb`、`RAG.ipynb`、`train.py`、`Modelfile`
- **NLP 基礎補充**：95 頁的 Text Summarization deck（Tokenizing／停用詞／Stemming／Lemmatizing／POS／Chunking／NER／文字分類／摘要）
- **39 張 Qwen-Image 2.1 章節插圖**（內嵌，維持單檔離線）
- **60 題互動 MC 測驗**（點選即時計分、進度自動存 localStorage）
- **所有程式碼與數字都在本機實測**（Python 3.11.15／Ollama 0.40.3／llama-index 0.14.25），實測輸出直接寫進內文

## 章節

| # | 章節 | 教材來源 |
|---|------|--------|
| 1 | 課程地圖：Lesson 7 在教什麼 | p1 |
| 2 | 為什麼要跑本機 LLM | 補充 |
| 3 | 技術底層：GGUF、量化、llama.cpp 與 Ollama 的關係 | 補充 |
| 4 | 量化命名規則速查 | 補充 |
| 5 | LM Studio：下載與安裝 | p3–p8 |
| 6 | LM Studio：首次啟動與選模型 | p9–p10 |
| 7 | LM Studio：設定與資源分配 | p11、p15 |
| 8 | LM Studio：換模型（從 Hugging Face 直接抓） | p12–p14 |
| 9 | LM Studio：上傳檔案並提問（本機 RAG 的第一次現身） | p16 |
| 10 | Ollama：下載與安裝 | p18–p19 |
| 11 | Ollama：模型選擇表（教材唯一的實質內容頁） | p20 |
| 12 | Ollama：`ollama run` 安裝模型與對話 | p21–p24 |
| 13 | Ollama：`ollama list`、`ollama serve` 與埠號 | p25–p26 |
| 14 | `testollama.py` 逐行拆解 | `testollama.py` |
| 15 | ⚠️ 教材把 LLM 輸出硬轉成 tensor 的問題 | `testollama.py` |
| 16 | AnythingLLM：安裝與歡迎頁 | p27–p30 |
| 17 | AnythingLLM：選擇 LLM 模型與換模型 | p31–p34 |
| 18 | AnythingLLM：提問 | p35 |
| 19 | GPT4All：安裝與模型安裝 | p36–p39 |
| 20 | GPT4All：提問 | p40 |
| 21 | GPT4All：My Documents 設定與加入文件／目錄 | p41–p43 |
| 22 | GPT4All：對自己的檔案提問（本機 RAG 的雛形） | p44 |
| 23 | 四個 App 對照總表 | 整理 |
| 24 | 怎麼選：決策樹 | 整理 |
| 25 | Open WebUI 與 Streamlit：為什麼要自己寫 | `Open WebUI.pptx` |
| 26 | `app_web.py` 逐行拆解 | `app_web.py` |
| 27 | LangChain ＋ LlamaCpp：在 Python 裡直接跑 GGUF | `LangChain.ipynb` |
| 28 | RAG 概念：關鍵字 RAG vs 向量 RAG | `RAG.ipynb` |
| 29 | ⚠️ `RAG.ipynb` 的 `max_length` 陷阱 | `RAG.ipynb` |
| 30 | LlamaIndex ＋ Groq：雲端 LLM ＋ 本機嵌入 | `LangIndex.ipynb` |
| 31 | ⚠️ Groq API Key 寫死 ＋ 本機替代路徑 | `LangIndex.ipynb` |
| 32 | LoRA 與本機微調（`train.py`） | `train.py`／`LoRA.txt` |
| 33 | ⚠️ `train.jsonl`：73 行只有 1 個唯一樣本 | `train.jsonl` |
| 34 | 轉 GGUF 與 `ollama create` | `ReadMe.txt`／`Modelfile` |
| 35 | DQN 迷宮：強化學習補充 | `Maze.ipynb` |
| 36 | NLP 基礎（一）：Tokenizing、停用詞、Stemming 與 Lemmatizing | NLP deck p8–p22 |
| 37 | NLP 基礎（二）：POS tagging、Chunking、NER 與文字分類 | NLP deck p19–p40 |
| 38 | 本機實測總表（真實數據） | 實測 |
| 39 | 考試重點整理 | 整理 |

另有 **7 個附錄**：指令與 API 速查表、常見錯誤與陷阱、教材頁面索引對照、離線執行／安裝提示、一頁精華（考前 10 分鐘）、60 題 MC 互動測驗、答錯題目 → 複習章節對照。

---

## 重點：60 題 MC 模擬試卷

**🖱️ [開始 60 題線上測驗](/local-llm-notes/mc-quiz.html)**

- 60 題單選、滿分 60 分、建議 75 分鐘
- 分五個部分各 12 題、依教材與 Lab 順序排列
- 答案分佈刻意打散（A/B/C/D 各 15 題）
- 點選即時計分、進度存在 localStorage、可切換「只看未答／只看答錯」

> 出題率最高的考點包括：**只有 Ollama 同時有 CLI 與 REST API（埠 11434）**、
> **只有 AnythingLLM 不自帶模型、必須接 provider**、
> **GGUF 是單一檔案格式、llama.cpp 才是推論引擎**、
> **`Q4_K_M` 是最推薦的量化等級**、
> **Ollama 對「模型不存在」回 404 而不是 400**、
> **`max_length` 是「輸入＋輸出」總長，RAG 要用 `max_new_tokens`**、
> **Stemming 是「砍」、Lemmatizing 是「查」**，
> 以及**摘要分 Extractive（抽原文句子）與 Abstractive（生成新句子）**。

---

## ⚠️ 這份筆記最有價值的部分：14 個實作陷阱與教材勘誤

照著教材做**會直接失敗**的地方，筆記全部標出來了：

| 位置 | 缺陷 |
|---|---|
| **`testollama.py`** | 寫死 **`"model": "llama3"`**——**不在教材自己的模型表裡**，照著做一定 **404** |
| **`LangIndex.ipynb`** | 把**真實可用的 Groq API key 寫死在程式碼裡**；而且**沒有那把 key 的學員根本跑不動** |
| **`train.jsonl`** | **73 行全部相同**（唯一樣本數 ＝ 1），樣本本身還是佔位字串 |
| **`train.py`** | 教材教 **LoRA**，但腳本實際是**全參數微調**，**完全沒有使用 `peft`** |
| **`Modelfile`** | **`TEMPLATE {{ .Prompt }}`** 沒有角色標記 → `/api/chat` 送進去的 `messages` 被丟掉 |
| **`RAG.ipynb`** | **`max_length`** 誤用（它是輸入＋輸出的總長，應改用 `max_new_tokens`） |
| **`testollama.py`** | `torch.tensor([ord(c)…])` 是**假嵌入**，只是 ASCII 碼、沒有語意 |
| **p36／p37** | `GPT4All` 被拼成 **`GTP4ALL`／`GTP4All`** |
| **p16** | `lmstudio` 被拼成 **`Imstudio`** |
| **p20** | 同一列 `phi3:3.8b` vs `ollama run phi3`；`app_web.py` 又出現第三種 `phi3:mini` |
| **`ReadMe.txt`** | 路徑寫 **`C:\Users\Teacher\...`**（講師的帳號） |
| **`run.txt`** | `accelerate` 出現兩次；`peft` 裝了卻沒用 |
| **`LoRA.txt`** | `matrics` 應為 `matrices` |
| **頁尾** | p1 與 p95 留著母片**未替換的佔位字串** |

### 沒有 Groq key 也能跑：本機替代路徑

`LangIndex.ipynb` 本來就是「**雲端 LLM ＋ 本機嵌入**」的混合架構，所以**只要換掉 LLM 那一行**：

```python
# 把 llama-index-llms-groq 換成 llama-index-llms-ollama
from llama_index.llms.ollama import Ollama

Settings.llm = Ollama(
    model="llama3.2:1b",
    base_url="http://127.0.0.1:11434",   # 教材說「可能要改 port」就是改這個
    request_timeout=180.0,
)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2")
```

**只需要改 3 個地方，其餘程式碼完全不動。** 本機實測結果（4 份文件、top-2）：

```
index built in 0.10 s
query OK in 0.43 s
sources: [{'topic': 'overview'}, {'topic': 'RAG'}]
```

檢索完全正確，但**答案幾乎照抄檢索到的段落**——這是小模型的典型行為，也是 RAG 最值得注意的教學點：**檢索正確 ≠ 回答正確**。

---

## 本機實測的真實數字

| 項目 | 實測值 |
|---|---|
| Ollama 版本 | **0.40.3** |
| Ollama 監聽 | **`0.0.0.0:11434` ＋ `[::]:11434`** |
| `smollm:latest` 單輪對話 | **1.38 秒** |
| `mymodel:latest` 單輪對話 | **10.91 秒**（且短指令回**空字串**） |
| RAG 建索引（4 份文件） | **0.10 秒** |
| RAG 檢索 ＋ 生成 | **0.43 秒** |
| `mymodel` 的真實身分 | **GPT-2 124M／F16／252 MB／僅 completion** |
| `train.jsonl` | **73 行、1 個唯一樣本** |
| `ollama.embed()` | **全部回 501**（需以 `--embeddings` 啟動） |

---

## 離線也能用

筆記是**單一 HTML 檔、零外部資源**（CSS、語法高亮、31 條數學公式的 SVG、39 張章節插圖全部內嵌），下載後直接雙擊就能看。

**Ollama 是這課唯一能完全離線跑起來的組合** —— 拉完模型後，不需要任何 API key、任何網路。

也可以下載原始 Markdown：

**📄 [Local_LLM_Apps_Study_Notes.md](/local-llm-notes/Local_LLM_Apps_Study_Notes.md)**

---

## 建議使用順序

1. 先讀 §1–§4（定位、為什麼跑本機、GGUF 與量化），建立整體座標
2. 依教材順序讀 §5–§22，**四個 App 都動手裝一次**
3. 讀 §23–§24（對照表與決策樹），確認自己該用哪一個
4. 進 Lab：§25–§31，**把 `app_web.py` 跑起來、把 RAG 管線看懂**
5. 讀 §32–§34（LoRA／微調／轉 GGUF），理解「自己造模型」的完整鏈路
6. 讀 §35–§37（RL 補充與 NLP 基礎）
7. 找個安靜的 75 分鐘，完整做一次**附錄 F 的 60 題線上互動測驗**
8. 考前 10 分鐘只看**附錄 E 一頁精華**

祝考試順利。

---

*本篇為個人學習筆記整理，教材內容版權屬匯縱專業發展中心（IVDC）所有。*
