---
title: 用 RTX 4090 做正體中文書頁 OCR：Indra、RapidOCR、PaddleOCR、Surya 實測與 A+B+C 三層校對
date: 2026-10-28 01:30:00
categories:
  - OCR
tags:
  - OCR
  - PaddleOCR
  - RapidOCR
  - Surya
  - Indra OCR
  - 正體中文
  - 直排文字
  - RTX 4090
  - CUDA
  - 文件數位化
  - LLM 校對
  - 本地 LLM
  - 資料隱私
  - Qwen
  - Ollama
  - Python
  - 實測
toc: true
---

手邊有一批手機翻拍的正體中文書頁（直排、雙欄、含印章與圖說），目標是把它變成可校對、可搜尋的文字稿。這篇記錄了完整過程：四個 OCR 引擎在同一批頁面上的實測、兩個一定會踩到的 Windows + CUDA 坑、以及最後用「Surya 骨架 + Paddle 補漏 + A/B/C 三層校對」把錯字壓下來的做法。

<!-- more -->

## 一、測試條件

- 硬體：RTX 4090 24GB（驅動 621.01，CUDA UMD 13.5）
- 系統：Windows 11
- 樣本：11 張手機翻拍書頁，2458×3321 上下，直排雙欄、含印章與易經圖說
- 評分方式：同一頁、同一組關鍵詞（樂天知命、仁者定命、金瓶梅、許冠傑、浪子心聲…），比對字數（召回）、關鍵詞命中、耗時，並人工判讀可讀性

## 二、四個引擎實測

| 引擎 | 模型 | 裝置 | 召回字數 | 關鍵詞命中 | 純推論/頁 | 判定 |
|---|---|---|---|---|---|---|
| PaddleOCR 3.7 | PP-OCRv6 medium + `chinese_cht` | 4090 GPU | **683** | 4/5 | **1.1 s** | 召回最高、行最完整 |
| Surya 0.22 | surya-ocr-2（GGUF / llama.cpp） | 4090 GPU | 734 | **5/5** | 4–9 s | 順序與段落結構最好 |
| RapidOCR 3.10 | PP-OCRv6 medium | 4090 GPU | 514 | 4–5/5 | 0.6 s | 最快，但會漏行 |
| Tesseract 5.5 | `chi_tra_vert`、PSM 5 | CPU | 771 | **0/5** | 3.2 s | 直排全亂碼，不可用 |
| EasyOCR 1.7 | `ch_tra` | 4090 GPU | 0 | — | — | 直排細長框裁切失敗 |
| Indra OCR | 1M 參數 ONNX | CPU | ~400 | — | 0.3 s | 錯字多（「仁者定令」） |

### 幾個值得記住的結論

1. **Tesseract 的直排模型不等於能用**：`chi_tra_vert` + PSM 5 在這批頁面上關鍵詞命中 0，771 字全是噪音。
2. **EasyOCR 對直排沒有抵抗力**：它把細長欄位裁切成空圖，直接 `cv2.resize` 失敗。
3. **Surya 與 PaddleOCR 各贏一半**：
   - 總序頁：Surya 讀出完整段落、順序正確，《金瓶梅》第十四回、許冠傑、黎彼得全對；Paddle 行序錯亂。
   - 作者簡介頁：Paddle 464 字、4/5；Surya 只有 315 字、1/5，還整段漏掉「陳雲是香港客家人…」。
4. **同源引擎不會互補**：RapidOCR 就是 PP-OCR 的 ONNX 版，與 PaddleOCR 同模型家族，實測 Rapid 的內容有 **98.3%** 已包含在 Paddle 之中。

## 三、兩個一定會踩的坑

### 坑 1：OpenCV 讀不到中文路徑

`cv2.imread` 在 Windows 走 ANSI 路徑，`C:\...\Pictures\序章\` 一律回 `None`，錯誤訊息是 `can't open/read file`。

解法：偵測非 ASCII 路徑就複製到暫存資料夾。

```python
from pathlib import Path
def _ascii_folder(src: Path) -> Path:
    try:
        str(src).encode("ascii")
        return src
    except UnicodeEncodeError:
        pass
    import hashlib, shutil, tempfile
    tag = hashlib.md5(str(src).encode("utf-8")).hexdigest()[:8]
    dst = Path(tempfile.gettempdir()) / f"ocr_ascii_{tag}"
    dst.mkdir(parents=True, exist_ok=True)
    for p in src.iterdir():
        if p.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            shutil.copy2(p, dst / p.name)
    return dst
```

### 坑 2：Paddle 與 torch 搶 CUDA runtime

`paddlepaddle-gpu` 與 `torch` 在同一進程會互踩 DLL：
`Error loading "torch\lib\cudnn_cnn64_9.dll"` 或 `shm.dll`。

實測有效的解法是**先 import torch，再 import paddle**：

```python
import torch          # 必須先載入
from paddleocr import PaddleOCR

ocr = PaddleOCR(lang="chinese_cht", device="gpu",
                use_doc_unwarping=False,
                use_textline_orientation=False)
```

這一步讓 Paddle 從 112 秒（CPU fallback）降到 **1.11 秒**。

另外，為 onnxruntime-gpu 安裝的 `nvidia-cudnn-cu12` 會反過來弄壞 torch，兩者只能留一個；我的做法是移除它，讓 onnxruntime 改用 torch 自帶的 cuDNN。

## 四、雙引擎跑同一批，值不值得？

先把「同源」與「異質」分開看。

### 同源（Paddle + RapidOCR）：不值得

| 指標 | 數值 |
|---|---|
| Paddle 總字數 | 6,291 |
| Rapid 總字數 | 4,706 |
| 兩者共有字元 | 4,624 |
| Rapid 的內容已被 Paddle 涵蓋 | **98.3%** |
| Paddle 多出、Rapid 沒有 | 1,667 字（26.5%） |

同家族模型的錯誤高度相關，投票、取交集都不會變準，等於多花一倍時間換不到正確率。

### 異質（Paddle + Surya）：有互補，但要靠規則對齊

同一頁上兩者各錯不同地方，實測互補證據（作者簡介頁）：

- **Surya 漏、Paddle 有**：「地氣候不冷不熱…良莠不齊，淹留此地，亦樂事也」（整段）、「陳雲是香港客家人…」（整段）
- **Paddle 漏、Surya 有**：段落順序、標題層級、跨欄閱讀順序

所以分工是明確的：**Surya 提供骨架（順序、段落），Paddle 提供召回（不漏字）**。

## 五、Surya 骨架 + Paddle 補漏

### 座標系是第一個難關

Surya 回傳原圖座標（`image_bbox` 2458×3321），但 Paddle 對直排頁回傳的是**旋轉 90° 後**的座標（x/y 尺度互換）。両者直接比對會完全對不上。

解法：偵測到 x/y 尺度與頁面相反時，把兩邊一起轉置，再正規化成 0–1 相對座標。

```python
transposed = abs(pw - sh) < abs(pw - sw)   # Paddle 寬度接近 Surya 高度
if transposed:
    for l in lines:      # (x0,y0,x1,y1) -> (y0,x0,y1,x1)
        x0, y0, x1, y1 = l["bbox"]
        l["bbox"] = [y0, x0, y1, x1]
    for b in blocks:
        x0, y0, x1, y1 = b["bbox"]
        b["bbox"] = [y0, x0, y1, x1]
    pw, ph = ph, pw
    sw, sh = sh, sw
```

### bbox 覆蓋 ≠ 內容覆蓋

第一版用「Paddle 行中心點落在 Surya 區塊框內」判斷是否已收錄，結果 Surya 的段落框很大（一整段），框內有 17 行 Paddle 文字被判為「已收錄」，但它實際只讀出其中一半。

改成**文字 n-gram 覆蓋率**：取該行 4-gram，計算有多少比例出現在 Surya 全文，低於 0.35 且長度 ≥12 字才視為漏讀。

```python
def ng(s):
    t = re.sub(r"[\s\W_]+", "", s, flags=re.UNICODE)
    return {t[i:i+4] for i in range(max(0, len(t)-3))}

surya_ng = set().union(*(ng(b["text"]) for b in blocks))
for ln in lines:
    line_ng = ng(ln["text"])
    ln["coverage"] = len(line_ng & surya_ng) / len(line_ng) if line_ng else 1.0
```

### 插入位置：交集面積，不是距離

漏讀的文字要插回正確位置。用「與哪個 Surya 區塊的 bbox 交集面積最大」決定，插在該區塊之後（依 `reading_order`）。

```python
def inter_area(a, b):
    x0, y0 = max(a[0], b[0]), max(a[1], b[1])
    x1, y1 = min(a[2], b[2]), min(a[3], b[3])
    return max(0.0, x1 - x0) * max(0.0, y1 - y0)
```

### 碎塊頁的例外處理

Surya 在目錄頁切成 329 個區塊、某正文頁切成 311 個，`reading_order` 完全不可靠，還會重複輸出同一段（同一句「吧！」重複 40 次）。

處理原則：

1. 文字完全相同的區塊只保留一次
2. 區塊數 > 100 的頁面放棄 Surya，改用 Paddle 行 + 幾何排序（直排轉置後的排序鍵是 `(-cy, cx)`：欄由右至左、欄內由上而下）
3. 短行（<12 字）不補，避免印章與頁碼雜訊

### 合併結果

11 頁中 9 頁走「Surya 骨架 + 補漏」，2 頁走「Paddle 幾何排序」，共補回 **11 處**漏讀，全部標記 `[補自 Paddle]` 以便回溯。

## 六、A+B+C 三層校對

補漏只解決「少字」，沒解決「錯字」。所以再加三層：

| 階段 | 做法 | 產出 | 數量 |
|---|---|---|---|
| **A 異文清單** | 文字 4-gram 配對 Surya↔Paddle，逐字 diff | `異文清單.csv` | 347 筆 |
| **B 規則式自動修正** | 相似度 ≥0.85、Paddle 信心 ≥0.95、差異為 ≤4 短漢字、兩側有上下文 | `修正記錄.csv` | 11 處 |
| **C LLM 校對** | qwen3.8:27b（Ollama，temperature 0），限定「只改錯字與漏字，禁止刪字」 | `*.llm.md` | 28 處 |

### B：規則式修正的條件

```python
if p["similarity"] < 0.85 or p["paddle_conf"] < 0.95:
    continue
if not (HAN.match(s_snip) and HAN.match(p_snip)):   # 只改漢字
    continue
if re.search(r"[0-9一二三四五六七八九十百千〇○]", s_snip + p_snip):
    continue                                        # 數字差異交給 LLM
if full.count(before[-2:] + s_snip) >= 2:
    continue                                        # 原寫法在書中他處也出現 → 不改
```

三條防線缺一不可。少了第一條，Paddle 讀錯的「第五屆」會蓋掉正確的「第九屆」；少了第三條，所有標點都會被改掉。

### C：LLM 校對的 prompt 設計

關鍵是**給具體錯誤範例**，否則模型會過度保守（實測 gemma4:12b 完全不改）：

```text
你是專業的繁體中文（正體字）校對員。任務：找出 OCR 造成的錯別字並修正。
OCR 常見錯誤：形近字誤認（胡→語、信→俗、有→布、寇→姦）、同音字、少一筆（天→夭）、
冷僻詞被讀錯（受脤→受脈）、漏字（命裏無時寫→命裏無時莫強求）。
本書已確認的錯字對照（看到左邊就改成右邊）：
胡言學家→語言學家、民信學家→民俗學家、有政司署→布政司署、天折→夭折、
迎寇赴會→迎姦赴會、受脈→受脤、當貴自是福來投→富貴自是福來投、
良菁不齊→良莠不齊、產留此地→淹留此地、鳥龜→烏龜、致文組首獎→散文組首獎。
嚴格規則：
1) 只改錯字與明顯漏字；
2) 絕對不可刪除任何字、不可改寫句子、不可調整順序；
3) 原文若含「[補自 Paddle]」等標記，必須原樣保留；
4) 不要自行增補標點；
5) 不確定就保留原文。只輸出修正後的全文。
```

### 最有用的不是換模型，是「錯字對照表」

第一版 prompt 只寫「請改正錯字」，結果 27B 模型漏掉冷僻詞「受脈→受脤」、也漏掉「當貴→富貴」。把這本書已確認的錯字對照直接列進 prompt 後，同一顆模型立刻補上這兩處。

換句話說：**本地模型的弱點不是知識不足，而是不知道「這本書」的錯誤長什麼樣**。一份 20 行的錯字對照表，比換更大的模型有效。

### 本地模型實測（同一頁、同一 prompt）

| 模型 | 改動數 | 受脈→受脤 | 當貴→富貴 | 風險 |
|---|---|---|---|---|
| qwen3.8:27b（Q4） | 2–5 處 | ✅ | ❌→✅（加對照表後） | 最穩，不刪字 |
| gemma4:26b | 4–8 處 | ✅ | ✅ | 會順手刪字、改「有→無」 |
| qwen3.8-27b-uncensored | 2–6 處 | ✅ | ❌ | 無明顯優勢 |

結論：**qwen3.8:27b 當主力（穩），gemma4:26b 當第二意見（召回高但需人工複核）**。

### 為什麼用本地而不是雲端

| 考量 | 本地 | 雲端 |
|---|---|---|
| 資料外傳 | 無 | 需上傳 |
| 成本 | 0 | 11 頁約 US$0.1–0.3 |
| 品質 | 中上（Q4 量化） | 更好 |
| VRAM | 佔 17–20 GB | 0 |

這批是尚未定稿的書稿，**選擇不外傳**優先於邊際的準確率提升。若日後處理的是公開資料，雲端模型會是更好的選擇。

> 注意：Ollama 清單中若有 `:cloud` 標籤的模型（例如 `minimax-m3:cloud`），那是送到雲端推論，處理敏感文件時必須避開。

用 `/api/chat` 而不是 `/api/generate`，並加 `"think": false`。原因：這個模型會先產生大量思考內容，`/api/generate` + `num_predict` 太小會讓 `content` 整個是空的（HTTP 200 但回應 0 字）。

### 實際抓到的錯字

| 原文（錯） | 修正（正） | 階段 |
|---|---|---|
| 本名不傳。**胡**言學家 | **語**言學家 | B |
| 及民**信**學家 | 民**俗**學家 | B |
| 英治政府**有**政司署 | **布**政司署 | B |
| 李瓶兒迎**寇**赴會 | 迎**姦**赴會 | B |
| 命裏無時**寫** | 命裏無時**莫強求** | C |
| **鳥**龜和白鶴 | **烏**龜 | C |
| 獲第九屆…**致**文組首獎 | **散**文組首獎 | C |
| 曾**SISS** | 曾**近榮** | C＋人工 |
| 陳摶**圗**南 | **圖**南 | C |

「致文組→散文組」是 B 抓不到、C 才修好的；「命裏無時寫→莫強求」則是 LLM 補回漏字的典型例子。

### LLM 之後：最後一哩還是要問人

LLM 修完後，我用程式掃出「Surya 與 Paddle 各執一詞、而最終稿採用了其中一方」的 11 個點（每點附前後 14 字上下文），逐條確認。其中 6 條只是引號增減，5 條真的影響字義：

| 上下文 | 誤 | 正 | 判斷依據 |
|---|---|---|---|
| 化學老師**曾近□**（1925–2011） | 曾近樂 | **曾近榮** | 香港「曾 Sir」本名 |
| 《易》乾卦，**《□傳》**「各正性命」 | 《易傳》 | **《彖傳》** | 此句出自乾卦《彖傳》 |
| 《武英殿**十□經注疏》**本 | 十二經 | **十三經** | 武英殿本即十三經 |
| 善心不是**孜孜□□** | 孜孜乾乾 | **孜孜矻矻** | 韓愈〈爭臣論〉成語 |
| 「……事業」**□杜預注** | 句，杜預注 | **句：晉·杜預注** | 註疏格式（杜預為晉人） |

這 5 條 LLM 全都沒抓到。原因不是模型笨，而是**它沒有人可以查證的外部依據**：人名、書名版本、成語出處，都超出「一段文字的上下文」能判斷的範圍。

所以流程固定成：

```text
find_uncertain.py   → 掃出待確認點（附上下文、兩邊讀法）
        ↓ 逐條問人
apply_manual_fix.py → 套用並記錄理由（人工確認修正.json）
```

一句話：**LLM 能把錯誤壓到個位數，但要收尾的那幾條，只有人能定。**

## 七、成果

- 最終全書：7,729 字（11 頁）
- 合計修正：B 11 處 + C 31 處 + 人工確認 5 處
- 冷僻詞與專名也修好了：「受脈」→「受**脤**」、「當貴」→「**富貴**」、「曾近樂」→「曾**近榮**」、《易傳》→《**彖傳**》、十二經→**十三經**、「孜孜乾乾」→「孜孜**矻矻**」
- 所有補漏段落保留 `[補自 Paddle]` 標記，可逐段回溯

## 八、還沒解決的問題

1. **少數專名仍有分歧**：`小聚義`／`小眾義` 兩邊各執一詞，這類需要回看原頁。
2. **碎塊頁的標點**是 LLM 補的，不完全等於原文。
3. **錯字對照表需要人工累積**：目前的做法是「跑一輪 → 人工看修正表 → 把確認的錯字補進 prompt → 再跑一輪」，第二輪才把冷僻詞收乾淨。
4. **最有效的改善其實是重拍**：平整、正對、均勻光、300dpi 平板掃描，所有引擎的準確率會一起上升，這比任何後處理都划算。

## 九、可重複使用的流程

```bash
# 1) PaddleOCR（召回最高）
python paddle_batch.py

# 2) Surya（順序與段落最好，需 llama.cpp + GGUF）
set SURYA_INFERENCE_BACKEND=llamacpp
set LLAMA_CPP_BINARY=C:\Users\princ\llamacpp\llama-server.exe
surya_ocr C:\path\to\images --output_dir C:\path\to\surya_out

# 3) 合併：Surya 骨架 + Paddle 補漏
python merge_surya_paddle.py --stem <檔名>
python build_book.py

# 4) A+B+C 校對
python analyze_pairs.py          # A
python autofix.py                # B
python llm_proofread.py --model qwen3.8:27b   # C
python build_final.py            # 整合輸出
```

## 十、小結

如果只記四件事：

1. **同源引擎不要一起跑**（Paddle + RapidOCR 有 98.3% 重疊），要互補就選異質模型（Paddle + Surya）。
2. **bbox 覆蓋不等於內容覆蓋**，判斷 OCR 是否漏讀要用文字 n-gram，不是框。
3. **LLM 校對的關鍵是「錯字對照表」**：給範例、關思考、限制刪字；換更大的模型，不如補一張 20 行的本書錯字表。
4. **最後幾條錯誤只有人能定**：人名、書名版本、成語出處，LLM 沒有查證依據，掃出來逐條問人最快。

這套流程目前能把一批手機翻拍的正體中文直排書頁，做到「可直接閱讀、少數專名需人工確認」的程度。要再往上，關鍵已經不在模型，而在拍攝品質與人工校對的最後一哩。


