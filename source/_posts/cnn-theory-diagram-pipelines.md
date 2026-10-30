---
title: 用 AI 生成「複雜理論示意圖」：六條路線實測（附 CNN 範例）
date: 2026-10-31 08:30:00
categories:
  - AI
  - 工具實測
tags:
  - AI
  - 示意圖
  - Paper2Any
  - AutoFigure
  - SAM3
  - SDXL
  - CNN
  - 工作流
---

很多人問：能不能用 AI 直接畫出「複雜但有正確標籤」的理論示意圖？這篇把六條路線在同一台機器（RTX 4090）上全部跑過一遍，結論先講：

> **示意圖的瓶頸不是「畫得像不像」，而是「標籤對不對」。**
> 能用的路線都是「LLM 寫結構與文字 → 輸出向量」；純擴散模型（SDXL、Qwen-Image）只能提供質感，不能提供語義。

## 一張表看結果

| 路線 | 判定 | 單次耗時 | 單次花費 |
|---|---|---|---|
| A. Paper2Any `tech_route`（文字/PDF → SVG） | ✅ 主力 | 1.5–12 分鐘 | $0.008–0.02 |
| B. AutoFigure-Edit（插圖 → 向量） | ✅ 有質感、無文字 | ~5 分鐘 | ~$0.01 |
| C. Paper2Any `exp_data`（實驗圖表） | ⚠️ 表格可用 | 2.8 分鐘 | ~$0.01 |
| D. 本機 Ollama（8B / 27B） | ⚠️ 幻覺 / 太慢 | 3–18 分鐘 | $0 |
| E. ComfyUI（Qwen-Image、SDXL） | ❌ 只能當底圖 | ~40 秒 | $0 |
| F. Gemini / GPT-image（雲端） | ❌ 所在地區 403 | — | — |

## 一、為什麼純 AI 生圖做不到

擴散模型不懂文字，也不懂拓撲。實測 Qwen-Image 2.1（int8）：

![Qwen-Image 生成的示意圖：只有兩個方框，文字是 Roar Gaga 與 Aopu](/img/report-2026-10-31/bad_qwen.png)

換成 SDXL base 1.0，構圖確實像流程圖了（方框、菱形、箭頭都有）：

![SDXL 生成的流程圖：構圖正確但所有文字都是亂碼](/img/report-2026-10-31/bad_sdxl.png)

**但文字全部是亂碼。** 理論圖的價值有一半在 `Cross-Attention`、`InfoNCE`、`Dice Loss` 這些詞不能錯，所以這條路走不通。

## 二、六條路線實測

### A. Paper2Any `tech_route`：一句話到可編輯 SVG

輸入一段方法描述，LLM 直接寫 SVG 程式碼，再用 cairosvg 實際渲染驗證，失敗就帶著錯誤訊息回頭修。

![技術路線圖：Input、Cross-Attention Fusion、Decoding、Losses 四層架構](/img/report-2026-10-31/route_short.png)

- 耗時 **1.5 分鐘**、花費 **$0.008**
- 產出 `technical_route_bw_*.svg`（12.7 KB）+ PNG
- 標籤 100% 對應輸入，**零幻覺**

餵一份 4.25 MB 的真實講義 PDF 也可以：

![由 CNN 講義 PDF 生成的概覽圖](/img/report-2026-10-31/route_pdf_cnn.png)

代價是時間拉長到約 12 分鐘，而且 `Implementation:` 這類長標籤會和內文重疊，需要在 Inkscape 微調。

### B. AutoFigure-Edit：插圖 → 向量

這條不是「生圖」，而是「把一張點陣插圖重建成可編輯向量」。流程是四段：

1. 生一張**不含文字**的插圖（我用 SDXL，40 秒）

![SDXL 生的抽象圖示插圖：只有圖示與箭頭，沒有文字](/img/report-2026-10-31/sdxl_base.png)

2. 用 **SAM3** 自動偵測圖示位置（本機推論，3.21 GB 權重）

![SAM3 偵測結果：19 個編號佔位框 AF01–AF19](/img/report-2026-10-31/sam3_seg.png)

3. 用 **RMBG-2.0** 把每個圖示去背
4. 讓 **LLM 重建 SVG**，把圖示嵌回去

![AutoFigure-Edit 產出的可編輯向量圖（Kimi K3.1 版）](/img/report-2026-10-31/af_kimi.png)

- 最終 `final.svg` **765 KB**：19 個嵌入圖示、104 條 path、9 個 rect
- 換 GLM-5.3 會得到不同風格（37 個 rect、68 條 path，更方塊化）

![改用 GLM-5.3 重建的版本：造型更幾何化](/img/report-2026-10-31/af_glm.png)

**限制**：SVG 裡沒有 `<text>`，因為輸入插圖本來就沒文字。標籤要自己補。

### C. `exp_data`：實驗圖表

![exp_data 產出的表格圖：藍色表頭、隔行底色](/img/report-2026-10-31/exp_table.png)

表格圖可用（2.8 分鐘），但統計圖步驟失敗。數據圖還是建議直接寫 matplotlib。

### D. 本機開源模型：快的不準，準的不快

| 模型 | 耗時 | 結果 |
|---|---|---|
| `qwen3-8b-heretic` | 約 3 分鐘 | **嚴重幻覺** |
| `qwen3.8-27b-uncensored` | 18.5 分鐘 | 內容正確、無幻覺 |

8B 那次最值得記錄：SVG 裡寫進了 `arXiv:2410.10934`、`DevAI: 55 Tasks`、`MetaGPT`、`Agent-as-a-Judge` —— 全是我沒給的內容。

![8B 模型的輸出：把記憶中的論文框架整套搬進來](/img/report-2026-10-31/bad_8b.png)

### E. ComfyUI 本地擴散模型

你機器上的 Qwen-Image 2.1（int8）與 SDXL base 1.0 都試過：

| 模型 / 參數 | 結果 |
|---|---|
| Qwen-Image / cfg 3.5 / 20 steps | 線條極淡、字變 `cro-attention` |
| Qwen-Image / cfg 7 / 30 steps | 只剩一個 `Sliacler` 破字方塊 |
| SDXL / dpmpp_2m / 30 steps | 構圖像流程圖、文字全亂碼 |

### F. 雲端影像模型：地區限制

| 模型 | 結果 |
|---|---|
| `google/gemini-3.1-pro-preview` | ❌ 403 `not available in your region` |
| `anthropic/claude-sonnet-5.5` | ❌ 403 |
| `openai/gpt-5.5` | ❌ 403 |
| `moonshotai/kimi-k2` | ✅ 200 |
| `moonshotai/kimi-k3.1-pro`（vision） | ✅ 200 |
| `z-ai/glm-5.3-flashx`（vision） | ✅ 200 |

403 的 routing 步驟是 `Gate Endpoints with Geo Restrictions`，屬供應商端地理限制。

## 三、決策樹：你要的圖該走哪條

```
你要的圖是什麼類型？
│
├─ ① 有明確節點與箭頭（方法流程、模型架構、技術路線）
│     → A. tech_route（文字或 PDF 直接餵）
│       · 要標籤一定正確 → 這是唯一選擇
│       · 要更複雜 → 拆成 3–4 個子模組分別生成，再在 Inkscape 併版
│
├─ ② 有機造型／圖示化（抽象概念、裝置、封面插圖）
│     → B. AutoFigure-Edit（底圖 → SAM3 切圖示 → RMBG 去背 → LLM 重建 SVG）
│       · 文字要自己補
│
├─ ③ 數據圖表（柱狀、折線、混淆矩陣）
│     → matplotlib（可重現、可版控）
│
└─ ④ 想要「一句話出高品質完整圖」
      → 需要 GPT-image / Gemini image 等級模型
      → 目前所在地區 403，需換供應商
```

最實務的組合是：**`tech_route` 出結構與文字 → 匯出 SVG → 在 Inkscape 用 AutoFigure 產的圖示替換節點圖形**。LLM 管正確性，擴散模型管質感。

## 四、CNN 實戰案例

用同一套管線生成「CNN 基本原理」兩張圖，走的是 `paper2technical` 工作流：

```
一句話描述
  → paper_idea_extractor（抽取方法要點）
  → technical_route_bw_svg_generator（ReAct + cairosvg 驗證）
  → technical_route_colorize_svg（有 --palette 才走）
  → 輸出 SVG + PNG
```

### ① CNN 整體架構（黑白，1.5 分鐘）

![CNN 整體架構：Input → Conv → ReLU → Pool → 特徵階層 → Flatten → FC → Softmax](/img/report-2026-10-31/cnn_arch.png)

含 40+ 標籤：Input & Preprocessing、Convolutional Block、Hierarchical Feature Learning（Early / Middle / Deep + receptive field）、Classification Head、Training Process。

### ② 卷積運算原理（黑白，1.5 分鐘）

![卷積運算原理：3×3 kernel 滑動、權重共享、局部連接、stride 與 padding](/img/report-2026-10-31/cnn_conv.png)

含 Sliding Window、Kernel 3×3、Stride & Padding、Element-wise Product & Sum、Weight Sharing、Local Connectivity、Feature Map。

### ③ 加上配色（各約 10 分鐘）

我把 `--palette` 補進了 CLI（原本沒有暴露這個參數，所以永遠只能出黑白）：

```python
parser.add_argument("--palette", default="",
    choices=["", "academic_blue", "teal_orange", "slate_rose"])
req = Paper2FigureRequest(..., tech_route_palette=args.palette)
```

![CNN 架構彩色版：academic_blue 色卡](/img/report-2026-10-31/cnn_arch_color.png)

![卷積原理彩色版：四色全用](/img/report-2026-10-31/cnn_conv_color.png)

**但這裡有個實測教訓**：`technical_route_colorize_svg` 不是「把黑白圖上色」，而是**讓 LLM 重新生成一整份著色 SVG**。

| 階段 | 耗時 | 費用 |
|---|---|---|
| 黑白生成 | 1.5 分鐘 | ~$0.008 |
| colorize | **7–8 分鐘** | **~$0.04–0.05** |
| **單張合計** | **約 10 分鐘** | **約 $0.05** |

我原本估彩色只要 $0.02–0.03，**實測貴一倍**（輸入 context 多了整份黑白 SVG，輸出 token 也幾乎等量）。

所以修正後的建議：
- 只要 1–2 張、想要顏色 → **Inkscape 手動改色**（30 秒、免費、可控）
- 要批次或要能重跑 → 用 `--palette`，接受每張 10 分鐘、$0.05

## 五、總帳

| 項目 | 數字 |
|---|---|
| 今天總花費 | **$0.58**（OpenRouter，上限 $50） |
| 若只做正事（A + B/Kimi） | 不到 $0.05 |
| 修掉的環境問題 | 9 處（Windows 缺 triton、SAM3 dtype 衝突、RMBG gated…） |

其中 **SAM3 的 dtype 衝突**最花時間：官方權重是 bfloat16，但程式各處產生 float32，最後靠在呼叫層全域攔截 `F.linear / conv2d` 才穩定。

## 六、結論

1. **示意圖的瓶頸是語義，不是畫技。** 能用的一定是「LLM 寫 SVG」這條路。
2. **擴散模型只適合生底圖**（不含文字），再交給向量化流程處理。
3. **本地小模型會張冠李戴**，把記憶中的論文框架搬進來；大模型則慢到不能迭代。
4. **彩色化的成本被低估**：比黑白貴 5–6 倍，而且只是「重寫一份」。
5. 目前最划算：`tech_route` 出結構 + AutoFigure 的圖示補質感，單張不到 3 美分、兩分鐘內完成。

---

*所有數據來自本機實測（2026-10-31，Windows / RTX 4090），非估算。*

