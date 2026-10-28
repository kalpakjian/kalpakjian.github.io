---
title: 'IBM STAIR「幻覺少 65 倍」查核：65 這個數字論文沒寫，是 3.25 ÷ 0.05 算出來的'
date: 2026-10-29 05:00:00
categories:
  - 技術筆記
tags:
  - RAG
  - 檢索增強生成
  - IBM
  - STAIR
  - DSI
  - 生成式檢索
  - 幻覺
  - 事實查核
  - arXiv
  - Mistral
  - 長尾
toc: true
---

> <strong>整理說明</strong>：這篇是完整查核紀錄，不是轉述。我下載了 arXiv 2609.03874 v2 的 PDF 全文（11 頁），用 PyMuPDF 抽成純文字後逐節核對，**引文一律原文照錄並附英文原句**。<strong>論文原文、我的推導、貼文的說法</strong>三種來源分開標註，不混在一起講。查核日期 2026-10-29。

社群上那則貼文說「RAG is officially cooked」、「IBM 做的檢索器比微調過的 RAG 系統少 65 倍幻覺」。數字算得出來，但結論不是那樣。

這篇把整條線從頭走一遍：貼文說什麼 → 論文實際上是什麼 → 65 從哪裡來 → 哪個發現才是真的 → 那個真發現本身又要打幾折。

<!-- more -->

## 三十秒結論

| 項目 | 查核結果 |
|---|---|
| 論文是否存在 | **存在**。arXiv:2609.03874 v2，IBM Research（印度），2026-09-03 投稿、2026-10-13 改版 |
| 「幻覺少 65 倍」 | 算術成立（3.25% ÷ 0.05% = 65）。但**論文全文沒有「65x」這個說法** |
| 幻覺的定義 | 論文自訂：生成「非葉節點」，也就是無效的章節識別碼。**不是假答案、不是假引用** |
| 絕對改善 | 3.25% → 0.05%，**降 3.2 個百分點** |
| 整體錯誤率 | 24.31% → 18.67%，**檢索仍大約每五次錯一次** |
| 「先過濾、驗證再生成」 | **論文沒有這個機制**。STAIR 是「目錄＋查詢 → 生成章節標題」的生成式檢索器 |
| 真正的發現 | 訓練樣本越少的章節，STAIR 領先越多（**長尾效應**） |
| 貼文最站不住的一句 | 「Zero hallucinations means zero liability」——0.05% 不是 0，而且檢索在上游，管不到生成端 |

一句話：**65 倍是真的算得出來，但它量的是一個最窄的子指標；這篇論文有價值的部分在 Figure 3、Figure 4，不在摘要。**

---

## 一、起點：那則貼文

貼文的三個核心主張，後面三節會逐一處理：

1. 「IBM built a retriever that **hallucinates 65x less** than fine-tuned RAG systems.」
2. 「their system **actively filters and validates the retrieved data** before the generation step even begins.」
3. 「**Zero hallucinations means zero liability.**」

第 1 句是數字問題，第 2 句是機制問題，第 3 句是概念問題。三題分開答。

---

## 二、先確認論文到底存不存在

| 欄位 | 內容 |
|---|---|
| 標題 | STAIR (STructure Aware Information Retriever): A novel dataset and LLM based retriever for document structure augmentation |
| 作者 | Vineet Kumar、Meghanadh Pulivarthi、Vishwajeet Kumar、Jaydeep Sen、Riyaz Ahmad Bhat、Sachindra Joshi |
| 機構 | IBM（六位全部） |
| 第一作者註腳 | 「Work done while at IBM. Currently at Amazon Books Science.」 |
| 投稿／改版 | 2026-09-03（v1）、2026-10-13（v2） |
| 分類／授權 | cs.AI、CC BY 4.0 |
| DOI | 10.48550/arXiv.2609.03874 |

論文本身沒有問題，是一篇正常的研究論文。**問題出在二手轉述。**

---

## 三、STAIR 實際做什麼（和貼文說的剛好相反）

論文 §4、§5.2 描述的流程是四步：

1. **抽目錄**：把整本書的 ToC 抽出來，**葉節點**（沒有子章節的標題）當成檢索單位。
2. **造題**：用 Mixtral 8x7b 為每個段落生成多個合成問題，標到對應章節。
3. **微調**：用 LoRA 微調 Mistral Instruct v0.2。輸入＝**查詢＋整份目錄**，輸出＝**葉節點標題**（上限 64 tokens）。
4. **推論**：模型直接生成「哪一節」，再去那一節找答案。

**沒有重排序器、沒有驗證器、沒有 critic loop、沒有「過濾候選文件」這一步。** 它不撿回一批文件再篩掉雜訊；它直接生成一個章節名。

貼文說的「actively filters and validates the retrieved data before the generation step」——**這個機制在論文裡不存在**。這是整則貼文最嚴重的錯誤，因為它是貼文用來解釋「為什麼能少 65 倍」的因果故事。故事是編的，數字卻是真的，這種組合最難拆。

用一句話對照：

- 貼文版：**先撿一堆文件 → 過濾掉垃圾 → 再生成**
- 論文版：**先看目錄 → 直接指名哪一節 → 去那一節讀**

方向是相反的：一個在「下游清理」，一個在「上游定位」。

---

## 四、數字對帳

**Table 4**（Avg 欄，格式為 Recall@1 / Recall@3 / nDCG@3）：

| 系統 | Avg | 備註 |
|---|---|---|
| Mistral（未微調） | 13.8 / 16.4 / 15.4 | 零樣本，直接讀目錄 |
| BM25 | 59.5 / 77.6 / 70.1 | Elasticsearch 8.11.2 |
| Claude Haiku 4.5 | 45.6 / 64.1 / 56.4 | 零樣本。**比 BM25 還差** |
| DPR（NV-Embed-v2） | 68.7 / 85.4 / 78.6 | 未針對此語料微調 |
| DSI（微調） | 76.9 / 85.3 / 81.9 | 主要對照組 |
| **STAIR** | **82.6 / 90.8 / 87.5** | 微調＋目錄 |

論文把 82.6 對 76.9 寫成「+7.4%」——那是**相對值**；絕對值就是 **5.7 個百分點**。這兩個數字都對，但讀者的感受差很多。

**§6.2 錯誤分析**（這三個數字才是 65 倍的原料）：

| 系統 | 總錯誤率 | 其中「非葉節點」 |
|---|---|---|
| Mistral | 86.20% | 26.81% 的錯誤 |
| DSI | 24.31% | **3.25%** 的預測 |
| STAIR | 18.67% | **0.05%** 的預測 |

順帶一提：Claude Haiku 4.5 零樣本只有 45.6%，比 BM25 的 59.5% 還低。可見「從目錄挑出正確章節」對前沿模型一點也不簡單，這篇論文的任務設計並不水。

---

## 五、把「65」拆開

三件事要分清楚：

**（1）論文沒有說過 65。** 我對全文做字串比對：`6[5]` 只命中 **5 次**，全部落在表格的數字串裡（`659`、`9065`、`65.0` 之類），而且搜 `65x`、`65×`、`65 times` 是**零命中**。論文自己的措辭只有「less than 0.05%」。

**（2）65 是後人算出來的比值。** 3.25 ÷ 0.05 = 65。算術沒有錯，但它是**推導值**。一篇論文沒說過的倍數，變成了整則貼文的標題。

**（3）它建立在一個極小的基準率上。** 從 3.25% 降到 0.05%，聽起來是天壤之別，實際上是**降了 3.2 個百分點**。而同期**整體錯誤率只從 24.31% 降到 18.67%**——也就是說，這個系統**仍然大約每五次就錯一次**（選錯章節）。

用個比方：如果一家醫院的「誤診率」從 3.25% 降到 0.05%，但「病人活著走出醫院的比例」只從 75.7% 升到 81.3%，你會說醫療水準提升了，不會說「醫療已死、新時代來臨」。**65 倍那個數字，就是那個 3.25% 的子項。**

---

## 六、定義的破口（本節是重點）

§6.1 開頭，定義講得毫不含糊：

> **"We define hallucination as the generation of a non-leaf node (invalid document identifier)."**
> （我們把幻覺定義為：生成非葉節點，也就是無效的文件識別碼。）

然後 §6.2 案例一裡，DSI 對「學齡前兒童被大人貶低自主行為時會如何反應」這題，預測了：

> `2.2.2 Autonomy vs. Shame/Doubt (Preschool Years)`

而真正的目錄寫的是 `(Toddlerhood)`。作者的評語是：

> "However, careful consideration shows this is **a hallucinated header not present in the input ToC**."
> （仔細看就會發現，這是一個不存在於輸入目錄裡的、憑空生出來的標題。）

**這裡出現了致命的定義落差：**

那個 `(Preschool Years)` **不是非葉節點**。它是個語法合法、層級正確、看起來完全正常的**葉節點標題**，只是**書裡沒有這一節**。

也就是說：**它不會被計入 0.05%。**

> **作者自己點出的最真實失敗模式——「捏造一個很像的章節名」——正好落在他們主指標的盲區裡。**

65 倍量的是「吐出格式不合法的東西」，量不到「吐出格式合法但根本不存在」的標題。而後者才是 RAG 幻覺的日常長相。

再加一筆：§6.2 對 Mistral 同時列了「非葉節點 26.81%」與「幻覺 23.86%」兩個**並列**類別。如果幻覺就是非葉節點，這兩個數字不該分開列。**定義沒有全程一致**，這也是為什麼 0.05% 這個數字只能當成一個窄指標看。

---

## 七、消融實驗真正的發現：長尾

§6.1 的兩個結論，才是這篇論文值得讀的地方。

**Figure 3 —— 幻覺率 vs 每個葉節點的訓練樣本數**

> "the hallucination rate of STAIR remains nearly constant at close to zero, regardless of the number of training examples… In contrast, DSI, which does not use ToC, exhibits a higher hallucination rate than STAIR, **particularly for leaf nodes with fewer training examples**."

**Figure 4 —— Recall@1 vs 每個葉節點的訓練樣本數**

> "for leaf nodes with less number of training examples, the Recall@1 difference between DSI and STAIR is much higher… As the number of training examples for a leaf node increase, Recall@1 gap between DSI and STAIR **decreases** – although STAIR consistently achieves higher Recall@1 numbers."

作者給的解釋（這是**假設**，不是證明）：DSI 必須從訓練資料裡**間接推斷、並且記住**整本書的結構，所以出現頻率低的章節會被漏掉或記錯；STAIR 把目錄直接放進輸入，模型不需要「記住」結構，只要把查詢對齊到目錄。

### 為什麼這一格比 65 倍重要

企業文件的分佈天生是**長尾**的：大量冷門章節、新上線的產品手冊、沒人問過的附錄、今年才修的法規。那正好是 DSI 最弱、STAIR 優勢最大的一格。

「65 倍」只在一個極窄的子指標上成立；「**樣本越少，目錄越有用**」則是可以帶去別的語料、別的模型的結論。**後者才是這篇論文的貢獻。**

---

## 八、「唯一差別是 ToC」這句話，有四個折扣

論文 §6 寫：

> "**The only difference in the input** between DSI and STAIR is that STAIR leverages ToC."

但 §5.2 自己寫明微調設定：

> "We set the maximum input length to **14k tokens for STAIR** and **512 tokens for DSI** and a maximum output length of 64 tokens."

**14k 對 512，是 27 倍的輸入長度差。** 這不是「只差一個目錄」，這是「能不能一次看到整本書」的差別。作者把增益全部歸給 ToC（"This supports our hypothesis"），但實驗並沒有把輸入長度這個變數隔離掉。

另外三點：

- **Figure 3、Figure 4 是聚合圖，沒有誤差棒、沒有標出每一格的樣本數。** 而優勢最大的幾格，正是樣本量最少、變異最大的那幾格。
- **規模**：18 本書、6 個領域、全英文；問題由 Mixtral 8x7b 從段落合成，不是真人問的；目錄是人工編輯好的乾淨階層。
- **單次實驗**：一個資料集、一次 LoRA 微調（r=16、α=32、上限 200 epochs、早停耐心 20）。沒有第二個語料庫的複現。

---

## 九、最後給你一個比例感

同一張 Table 4，從左讀到右：

| 階段 | Recall@1 | 這一步貢獻多少 |
|---|---|---|
| Mistral 未微調 | 13.8% | — |
| ＋任務微調＋語料知識注入（DSI） | 76.9% | **+63.1 個百分點** |
| ＋目錄結構（STAIR） | 82.6% | **+5.7 個百分點** |

**真正的槓桿是「微調＋把語料知識注入模型」，不是目錄。** 目錄是疊在上面的一層邊際增益。

貼文把那個 **5.7 個百分點**講成了架構革命，順便把 63 個百分點的功勞整碗端給了「新架構」。這不是說 5.7pp 不值得研究——它在**長尾章節**上會被放大，那才是重點——而是說，**它撐不起「RAG is officially cooked」這句標題**。

---

## 十、作者自己怎麼說局限（逐字）

> "Our current evaluation is limited to corpora where a global structure exists. While this setting is suitable for initial validation, **it may not fully represent the diversity of real-world use cases**. In future work, we plan to extend our evaluation to standard benchmarks by artificially inducing a Table of Contents structure."

翻成白話：**這套方法要求語料本身有乾淨的階層目錄。** 有目錄的文件（教科書、產品手冊、10-K、法規彙編、SAP 說明頁——這些都是論文自己舉的例子）適用；沒有目錄的（聊天紀錄、散落的郵件、亂長的 wiki）不適用。

這句話寫在論文最後一節（References 之前），貼文裡沒有出現。

---

## 十一、所以這篇論文到底該怎麼用

**適合的場景**

- 語料有真實的階層結構：技術手冊、產品文件、年報、法規、內部 SOP。
- 長尾嚴重：大量章節很少被問到，向量檢索老是撈不到。
- 你想要的是「**定位到哪一節**」，而不是「撈一段相似文字」。

**不適合的場景**

- 語料沒有結構，或結構是事後硬套的。
- 需要的是跨章節推理、多文件彙整（STAIR 只回答「哪一節」，不回答「為什麼」）。
- 你的瓶頸在生成端忠實性——**檢索做得再好，也治不了模型拿著正確章節亂講。**

**如果要自己驗證**

不要只量「非葉節點率」。至少加兩個指標：

1. **捏造標題率**：模型吐出的章節名，有多少根本不在目錄裡（語法合法但不存在）。
2. **端到端忠實性**：拿到正確章節之後，答案是否真的被那一節支持。

論文自己的案例一就示範了第一種錯誤有多容易發生，只是它沒有被計入 0.05%。

---

## 十二、這次查核是怎麼做的（可重現）

```powershell
# 1. 抓原始 PDF（v2，4.3 MB / 11 頁）
Invoke-WebRequest -Uri 'https://arxiv.org/pdf/2609.03874v2' -OutFile "$env:TEMP\stair.pdf"

# 2. 抽文字（PyMuPDF），42,426 字元
python -c "import pymupdf; d=pymupdf.open(r'$env:TEMP\stair.pdf'); print(sum(len(p.get_text()) for p in d))"

# 3. 依章節標題切段，逐字讀 §5（實驗）、§6（結果與消融）、§8（局限）

# 4. 字串比對，確認「65 倍」不是論文的主張
#    6[5]        -> 5 次，全部在表格數字裡
#    65x|65×|65 times -> 0 次
```

四步都不需要任何 API 或付費工具，任何人都能重跑一次。**這也是這類「驚人倍數」貼文最該被對待的方式：不要問「真的嗎」，直接去看原始檔案裡那個字串在不在。**

---

## 參考資料

- 論文摘要頁：[arxiv.org/abs/2609.03874](https://arxiv.org/abs/2609.03874)
- 全文 PDF（v2）：[arxiv.org/pdf/2609.03874v2](https://arxiv.org/pdf/2609.03874v2)
- 全文 HTML（v2）：[arxiv.org/html/2609.03874v2](https://arxiv.org/html/2609.03874v2)
- Hugging Face 論文頁：[huggingface.co/papers/2609.03874](https://huggingface.co/papers/2609.03874)
- 基準測試 SearchTome 已在 Hugging Face 上釋出；程式碼在論文提供的 GitHub 連結

---

## 附：這類貼文的三個辨識特徵

這次三樣全中，之後看到類似寫法可以直接提高警覺：

1. **一個巨大的倍數，但它是相對值。** 3.25% → 0.05% 是 65 倍，也是 3.2 個百分點。標題只會寫前者。
2. **一個被重新定義的指標，沿用最嚇人的那個詞。** 「幻覺」在這裡＝格式不合法，不是內容不實。同一個詞，兩種量級。
3. **一套你在方法章節裡找不到的機制。** 「主動過濾與驗證」聽起來很合理，但論文裡沒有這個東西。**合理 ≠ 存在。**

> 查核的成本，往往只是一次點擊加上一次全文搜尋。這次的原始連結就在貼文裡，而它跟貼文講的不一樣。


