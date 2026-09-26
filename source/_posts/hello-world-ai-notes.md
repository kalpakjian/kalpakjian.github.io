---
title: Hello World - 我的 AI 技術筆記
date: 2026-09-27 10:00:00
categories:
  - 學習資源
tags:
  - AI
  - LLM
  - Hexo
  - 開發筆記
index_img: https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1200
banner_img: https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1600
---

歡迎來到我的全新技術部落格 **AI Tech Notes**！

本站建立於 Hexo 靜態網站框架之上，主題採用極簡高質感的 Fluid，並透過 GitHub Actions / GitHub Pages 自動化發佈。

---

## 為什麼建立這個 Blog？

在 AI 模型日新月異的時代（從雲端前沿模型到可以在個人工作站運行的本地端 LLM），我們正在見證計算機歷史上最大的典範轉移。這個部落格將持續記錄：

1. **本地 LLM (Local LLM)**：Ollama、vLLM、GGUF 量化模型調校與個人工作站推論經驗。
2. **AI 工具實測 (AI Tools)**：Claude Code、Cline、Cursor 等 Agent 工具在實際專案中的工作流整合。
3. **學習資源 (Learning Resources)**：Prompt Engineering、Agent 架構、前後端技術思考。
4. **硬件與效能 (Hardware & Benchmarks)**：GPU 顯存吞吐測試、推論延遲評測與成本最佳化。

---

## 精選專題推薦

我們剛整合了經典專題分析：
- 📖 [【專題】Rails 之父退休了：DHH 宣告手寫程式碼的時代正式結束](/dhh-rails-world-2026/index.html)
- ⏱️ [跳躍、停滯、再跳躍：歷史時間線與關鍵數字](/dhh-rails-world-2026/timeline.html)
- ❓ [讀完之後：台灣軟體團隊躲不掉的三個問題](/dhh-rails-world-2026/questions.html)

---

## 程式碼區塊示範 (Python)

以下是一個使用 Python 調用本地 Ollama 服務的簡單範例：

```python
import requests

def ask_local_llm(prompt: str, model: str = "llama3.3") -> str:
    """向本地 Ollama 實例發送請求"""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("response", "")
    raise RuntimeError(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    result = ask_local_llm("用繁體中文以三句話總結 Agent 協作的核心。")
    print("AI 回覆:\n", result)
```

## 指令列示範 (PowerShell / Bash)

在 Windows PowerShell 或 Linux Bash 中測試本地 GPU 狀態：

```bash
# 檢查 NVIDIA 顯卡資訊與顯存佔用
nvidia-smi

# 啟動本地 Ollama 服務並拉取最新模型
ollama run llama3.3
```

---

## 圖片展示示範

以下為高解析度 AI 視覺藝術範例：

![AI Abstract Landscape](https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1000)

> 「帶著喜悅回顧那個親手寫程式的時代，然後接受它已經結束了。」— DHH
