---
title: OpenAI 數學手稿庫事實查核：719 篇手稿、FFT 突破 n log n，與「AGI 已至」的距離
date: 2026-10-09 10:00:00
categories:
  - AI 研究追蹤
tags:
  - OpenAI
  - Lean
  - 形式化驗證
  - 計算複雜度
  - FFT
  - AGI
  - 事實查核
math: true
toc: true
index_img: /img/covers/openai-math-repo-fact-check.png
banner_img: /img/covers/openai-math-repo-fact-check.png
---

> <strong>整理說明</strong>：本文分兩部分。前半是對「OpenAI 一口氣發表數百篇數學論文、AGI 已至」這個流傳版本的修正；後半是逐項對照 <a href="https://github.com/openai/math">openai/math</a> 一手來源（README、<code>overview.tex</code>、<code>history.md</code>、<code>lean/docs/</code>、<code>lean/ComparatorChallenges/</code>）所做的查核紀錄，附上可重現的指令與 commit hash，並在最前面加上一張事實核對速查表。

<!-- more -->

## 一句話總結

> OpenAI 的內部模型展示了目前非常強的「數學研究代理」能力，但這批結果仍處於不同程度的驗證階段，<strong>不能等同於數百個問題已經被數學界正式確認</strong>。

更準確的說法是：這是「AI 開始能系統性參與數學研究」的重大訊號，但不是 AGI 已經被證明出現的證據。

## 事實核對速查表

先把結論攤開：這輪查核的核心修正都成立，方向比多數中文流傳版本嚴謹。真正的重點不是「722 篇已經解決數百個難題」，而是 OpenAI 公開了一批處於不同驗證階段的 AI 生成數學手稿，而且數量還在變動。

| 流傳說法 | 較準確的說法 | 評估 |
| --- | --- | --- |
| 「OpenAI 發布 722 項數學成果」 | 2026-10-06 初次發布為 722 篇手稿、372 個結果家族；其後撤回 3 篇，現為 719 篇。 | 正確，但需更新 |
| 「235 個附 Lean 證明」 | 「235 個附 Lean」是發布初期流傳的說法；現行 README 改以約 42% 頂層結果已形式化表述，且分母是手稿數而非結果族。 | 部分正確，但表述易誤導 |
| 「FFT 突破 $n\log n$」 | 條目宣稱對所有長度 $n$，DFT 可用 $O(n(\log n)^{1-10^{-13}})$ 次運算完成，即漸近低於 $n\log n$。 | 宣稱存在，但非實用加速 |
| 「Lean 已驗證」 | Lean 只檢查被形式化的命題之邏輯推導；它不能自動保證形式化命題等同論文宣稱的數學結果，也不能取代同行審查。 | 正確 |
| 「AGI 已至」 | 這顯示 AI 有很強的數學研究產出與形式化能力，但不足以證明 AGI；OpenAI 自己也說結果處於不同驗證階段，部分未形式化結果可能有問題。 | 過度推論 |

以下章節逐一展開這五列。

## 本文查核的對象

這篇文章的起點，是這支在中文圈廣泛流傳的影片：

<div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:10px; box-shadow:0 4px 14px rgba(0,0,0,0.15); margin:16px 0 8px;">
  <iframe src="https://www.youtube.com/embed/GZaOyjdsfvE" title="OpenAI一口气发布722项数学成果，数学专业最黑暗一天，AI数学新纪元真来了！" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="position:absolute; top:0; left:0; width:100%; height:100%;"></iframe>
</div>

<p style="font-size:0.9em; color:#888; margin-top:0;">〈OpenAI一口气发布722项数学成果，数学专业最黑暗一天，AI数学新纪元真来了！〉— <a href="https://www.youtube.com/@%E6%9F%8F%E6%8B%89%E5%9B%BE%E6%A2%A6%E8%A7%81%E7%94%B5%E5%AD%90%E7%BE%8A">柏拉图梦见电子羊</a>（YouTube）</p>

影片標題裡的「<strong>722 項數學成果</strong>」，正好就是本文要查核的數字。影片指出的方向——AI 在數學研究上的能力躍進——值得高度重視；但其中幾個關鍵數字，以及「AGI 已至」這個結論，在與 repo 一手資料逐項對照後需要修正。

## 先更正幾個關鍵數字

流傳版本常把「722 篇手稿、235 個附 Lean 證明」當成定論。實際的 repo README（commit `fd4aeeb2`，2026-10-08）原文是：

> The current catalogue contains <strong>719 manuscripts organized into 372 families</strong>.
> The repository has <strong>~42% top-line results formalized</strong>.
> On average, each result used <strong>three hours of ChatGPT Pro thinking compute</strong> with that model.
> Over the course of the evaluation, the model was posed approximately <strong>4,000 problems</strong>.

所以：

- 「722 篇」是發布初期數字：以初始 commit `adc7f124`（2026-10-06）驗證，當時的 README 確實寫的是 722 manuscripts / 372 families。
- 「719 篇」是目前 repo 顯示的數字（3 篇差額見〈其他結果應如何看〉）。
- 「235 個附 Lean」不宜理解為「235 篇完整論文已被 Lean 證明」；現行 repo 改以百分比表述，且 <code>history.md</code> 明確寫成 <code>300 / 719 = ~42%</code>——分母是<strong>手稿數</strong>，不是 372 個 family。
- Lean 只能檢查「形式化後的證明是否由公理和定理正確推出」，不能自動保證模型把問題定義對、定理表述對，或證明的結果真的具有原先宣稱的數學意義。

## FFT 突破是真是假？

公開目錄中確實有這個條目。<code>overview.tex</code> 條目 130 的原文是：

> <strong>Fourier transforms below $n\log n$.</strong> Gives a deterministic length-$n$ discrete Fourier transform algorithm using $O(n(\log n)^{1-\delta})$ operations for every $n$, with explicit $\delta=10^{-13}$. The model uses <strong>exact complex arithmetic, unrestricted coefficients and a supplied root of unity</strong>, and counts scalar preparation and logarithmic-word indexing.

也就是形式上低於 $O(n\log n)$。普通 FFT 的複雜度大約是

$$n\log n$$

新結果只把 $\log n$ 改成 $(\log n)^{0.9999999999999}$，改善倍率是

$$\frac{n(\log n)^{1-10^{-13}}}{n\log n} = (\log n)^{-10^{-13}}$$

除非 $n$ 大到天文數字，否則這個因子幾乎等於 1，差距也超不過常數因素、記憶體存取、平行化與實作成本；再加上模型假設<strong>精確複數運算、不受限係數與特定單位根</strong>，並把 scalar preparation 與 logarithmic-word indexing 都計入計算模型，這些都是理論計算模型下的設定。所以它是<strong>理論計算複雜度上的突破，不是工程上的 FFT 革命</strong>，也不是「明天 NumPy／FFTW 會變快」。

## Lean 到底證明了什麼：一個被多數報導搞反的細節

這是本文最需要修正的一點。流傳說法是「Lean 驗證的是比論文主張稍弱的版本」，但這個方向其實講反了。官方 scope note 顯示 FFT 形式化分成兩塊：一塊是<strong>逐點（subsequential）</strong>的弱化版，另一塊是<strong>均勻（uniform）</strong>的完整版。實際查核 <code>lean/</code> 目錄後，情況更細緻：

<strong>1. 強版（含 $\delta=10^{-13}$ 的均勻版本）已有完整證明。</strong>主形式化落在 <code>lean/OAI/Computability/FourierTransform/</code>（88 個 <code>.lean</code>）與 <code>lean/OAI/Computability/FourierCircuit/</code>（51 個 <code>.lean</code>）。逐一抓取這 139 個檔案掃描後，結果為 <code>sorry = 0</code>、<code>native_decide = 0</code>、<code>axiom = 0</code>。<code>Goal.lean</code> 中的目標是

$$O(n(\log n)^{1-10^{-13}}) = o(n\log n)$$

<strong>2. 反而是那個「弱化版」沒有證明。</strong><code>lean/docs/130.md</code> 對這一塊的說明是：

> The result is subsequential, with no all-length, bounded-coefficient, conditioning, or bit-complexity claim.

對應的 <code>lean/ComparatorChallenges/ExactFourier.lean</code> 內容是

```lean
def MainStatement : Prop :=
  ∀ c : ℝ, 0 < c → ∀ N₀ : ℕ, 2 ≤ N₀ → ∃ n : ℕ, N₀ ≤ n ∧
    ∃ C : Circuit n, C.Computes (fourierMatrix n) ∧
      (C.size : ℝ) < c * (n : ℝ) * Real.logb 2 (n : ℝ)

theorem main_theorem : MainStatement := by
  sorry
```

注意這敘述本身比論文主張弱得多：它只說「對任意常數 $c$，<strong>存在</strong>足夠大的 $n$ 能達到 $cn\log n$」，而不是「所有 $n$」。而它確實是 <code>sorry</code>（未證明）。

<code>ComparatorChallenges/</code> 全庫共 416 個 <code>.lean</code>，性質是提供給第三方驗證者獨立挑戰用的題目，抽樣多個皆含 <code>sorry</code>，這不代表主張為假，只代表那些檔案不是已完成的證明。

<strong>小結：</strong>強版已被完整形式化並證明，Comparator 裡那個弱化、逐點的陳述才是 <code>sorry</code>——「Lean 只驗證了較弱版本」的說法正好相反。但就算 Lean 通過，仍要人工確認形式化命題是否真正對應論文的數學主張、假設是否合理；官方 scope note 自承不管係數界、conditioning 與 bit-complexity，這比「$\delta$ 太小」是更根本的理由，也不能取代同行審查。

## 其他結果應如何看

這批內容確實涵蓋很高難度的領域：數論及 $L$-函數零點區域、Birch–Swinnerton-Dyer 猜想與 Hodge 猜想的部分情況、理論計算機科學中的複雜度和演算法問題、算術電路下界、拓撲、幾何、群論、偏微分方程和數理物理。

不過標題中的「解決」需要分級理解：

| 狀態 | 意義 |
| --- | --- |
| AI 產生猜想或證明草稿 | 仍只是候選答案 |
| 人類專家初步認為合理 | 有研究價值，但未定案 |
| Lean 檢查通過 | 某個形式化命題的推導被核驗 |
| 外部專家審閱並發表 | 數學界較正式的接受 |
| 後續研究建立在其上 | 才能確認真正影響力 |

repo 自己已說明：

> This collection includes results at different stages of verification. Not all have accompanying Lean formalizations. ... Some of the unformalized results could have issues.

這不是純粹理論上的擔心。<code>history.md</code>（2026-10-07）記錄了一次實際的撤回，原因是一處<strong>符號錯誤</strong>：

> In "Algebraicity of Weil classes on split abelian eightfolds" a <strong>sign error</strong> invalidates a stabilization-trace cancellation argument and the construction used by two dependent papers. As a result, we have withdrawn the following three manuscripts.

被撤回的三篇是：

- Algebraicity of Weil classes on split abelian eightfolds
- Algebraicity of Kuga–Satake Correspondences for K3 Surfaces
- The rational Hodge conjecture for products of K3 surfaces

同批還修了另外 14 篇、並更新 13 篇引用。這三篇的 README 與路徑皆已 404——也就是說<strong>三篇已從 repo 完全移除</strong>，只剩 <code>history.md</code> 的文字記錄，這正好解釋了 722 → 719 的帳。

## Unique Games 和「數百個定理」呢？

條目原文抽查結果：

- <strong>條目 102</strong>：「Proves Khot's Unique Games Conjecture.」——確實是完整解決的宣稱，連帶 Max-Cut 最佳硬度、Vertex Cover 因子 2、Min-UnCut、directed FVS。
- <strong>條目 107</strong>：「Proves $\omega \le 9/4$ over $\mathbb{C}$, giving $O_\varepsilon(n^{9/4+\varepsilon})$ arithmetic operations for square matrix multiplication.」
- <strong>條目 003</strong>：「zero-free in $\Re s > 7/8$, resolving the <strong>quasi</strong>-Riemann hypothesis.」——這是準黎曼假設，不是 RH 本身；其 scope note 還註明 "The paper's later applications are not included."
- <strong>條目 002</strong>（BSD）：限於 Selmer corank 為 0 或 1 的曲線，加上密度一的二次扭轉。
- <strong>條目 032</strong>（Hodge）：限於 CM abelian varieties。

不能全部用同一個「AI 已證明」標準看待。有些是完整解決，有些只是改善上界或下界，有些只處理特殊類別，有些是條件式結果，有些只是把已知方法推到新範圍。

例如矩陣乘法指數 $\omega \le 9/4$ 即使成立，也代表矩陣乘法的漸近上界改善，不等於所有 AI、GPU 或線性代數程式會即時變快；實際演算法還要考慮常數、記憶體、平行性及適用矩陣大小。

## 是否代表 AGI 已至？

判斷如下：

> <strong>「AGI 已至」是把「數學研究產出很強」直接外推成「通用智慧已達成」；兩者之間還隔著好幾道關卡。</strong>

目前至少還有三個限制，讓「AGI 已至」站不住腳：

1. <strong>驗證未完成</strong>：約 42% 頂層結果已形式化，其餘未必有 Lean 證明。
2. <strong>已有實際撤稿</strong>：官方 <code>history.md</code>（10 月 7 日；媒體多記為 10 月 8 日）已記錄撤回 3 篇、修訂 14 篇、更新 13 篇引用，詳見〈其他結果應如何看〉。
3. <strong>未經正常學術檢驗</strong>：這些是手稿與證明工件，不是已通過同行評審、被社群充分覆核的定論，附了 Lean 代碼也不例外；「人類數學協會」（AHM）甚至公開呼籲停止與 OpenAI 合作。

原因是「數學能力很強」只是 AGI 的一個面向。AGI 通常還需要同時具備：長期自主規劃、穩定處理開放式現實任務、跨領域遷移能力、自己發現重要問題而不只是批量嘗試既有問題、可靠地分辨正確與錯誤和無意義的結果、持續實驗修正驗證並與人類協作、在陌生環境中具備一般化能力。

這次展示最驚人的地方，未必是「一夜解決數百題」，而是它可能已經形成一個相當有效的研究流水線：

$$\text{問題搜尋} \rightarrow \text{產生猜想} \rightarrow \text{構造證明} \rightarrow \text{整理成論文} \rightarrow \text{Lean 形式化} \rightarrow \text{大量篩選}$$

這更像是<strong>高吞吐量的數學研究系統</strong>，而不是一個單獨聊天模型突然變成全知數學家。

值得一提的是，README 自己揭露了流程並非完全單一：Riemann zeta 零點區域與 Hodge 猜想的 CM 情況屬於「例外」，而且 $\Re s > 11/12$ 那篇的撰寫<strong>經過人工編輯</strong>（human edited for readability）。目前只為 10 個 result 開放了推理摘要。

## 查核紀錄：實際跑了什麼

為了讓這些數字可被驗證，以下是實際使用的方法：

```powershell
# 抓 README 與 history
Invoke-WebRequest https://raw.githubusercontent.com/openai/math/main/README.md
Invoke-WebRequest https://raw.githubusercontent.com/openai/math/main/history.md

# 驗證「722 是初期數字」——用初始 commit
Invoke-WebRequest https://raw.githubusercontent.com/openai/math/adc7f124/README.md

# 在 overview.tex 中定位條目原文
Select-String -Path ov.tex -Pattern 'Fourier transforms below'
Select-String -Path ov.tex -Pattern 'Unique Games|Matrix multiplication with exponent'

# 抓 FFT 的官方 scope note 與弱化版 Comparator 檔案
Invoke-WebRequest .../lean/docs/130.md
Invoke-WebRequest .../lean/ComparatorChallenges/ExactFourier.lean

# 掃描主形式化目錄是否有 sorry / native_decide / axiom
# lean/OAI/Computability/FourierTransform  -> 88 files, sorry=0, native_decide=0, axiom=0
# lean/OAI/Computability/FourierCircuit    -> 51 files, sorry=0, native_decide=0
```

另外抽樣 60 個 <code>Main.lean</code>（跨 Algebra、AlgebraicGeometry、Analysis 等）掃描，同樣為 <code>sorry = 0</code>、<code>axiom = 0</code>。<code>lean/docs/</code> 目前有 242 份 scope note。

## 結論

最準確的一句是：

> <strong>那道牆，的確破了；但實務上明天不會變快。</strong>

如果只能留一句話，定性如下：

> <strong>這是 AI 數學研究能力的重要躍升訊號，但不是「數百個重大難題已被解決」，更不是 AGI 已被證明的證據。</strong>

「AGI 已至」應該改成「數學研究型 AI 已進入一個新階段」——AGI 是否已至，仍要看它能否在數學以外的開放世界長期、可靠、自主地工作。AI 已從解題工具，開始接近可大規模產生與驗證研究候選結果的研究夥伴；而這條流水線是否真正改變數學，取決於有多少結果能經得起數學家獨立閱讀、形式化覆核、修正與後續研究檢驗，這才是下一個真正的分水嶺。

---

### 一手來源

- <a href="https://github.com/openai/math">openai/math</a>（README 為數字來源）
- <a href="https://github.com/openai/math/blob/main/overview.tex">overview.tex</a>（條目原文）
- <a href="https://github.com/openai/math/blob/main/history.md">history.md</a>（撤回與修正記錄）
- <a href="https://github.com/openai/math/blob/main/lean/docs/130.md">lean/docs/130.md</a>（FFT 形式化範圍）
- <a href="https://github.com/openai/math/blob/main/lean/ComparatorChallenges/ExactFourier.lean">ComparatorChallenges/ExactFourier.lean</a>（弱化版，含 <code>sorry</code>）

### 二手來源（流傳版本與後續報導）

- <a href="https://rits.shanghai.nyu.edu/ai/openai-drops-722-math-manuscripts-from-an-unreleased-model/">NYU Shanghai RITS — OpenAI Drops 722 Math Manuscripts From an Unreleased Model</a>（722 / 372、撤稿與修訂、約 42% 形式化）
- <a href="https://finance.sina.com.cn/jjxw/2026-10-10/doc-iniutqmf6048244.shtml">新浪財經（轉載機器之心）</a>（約 4,000 題、每項平均 3 小時、300 項核心結果 ≈ 42%）
- <a href="https://finance.sina.cn/stock/jdts/2026-10-10/detail-iniutqmf2041717.d.html">21 世紀經濟報導（新浪轉載）</a>（撤回 3 篇、修訂 14 篇、更新 13 篇引用）
- <a href="https://aidiscoveries.io/openai-releases-722-math-manuscripts-from-an-unreleased-ai-model-what-what-it-means-for-mathematics/">AI Discoveries — OpenAI Releases 722 Math Manuscripts From an Unreleased AI Model</a>（722 不等於 722 項獨立驗證的突破）
- <a href="https://ascendants.in/industry_events/openai-722-ai-math-papers-boycott-lean-proof-verification/">The Ascendants — OpenAI's 722 Math Papers Spark Boycott Calls</a>（Lean 驗證的界限與學界抵制爭議）

### 影片來源

- <a href="https://www.youtube.com/watch?v=GZaOyjdsfvE">OpenAI一口气发布722项数学成果，数学专业最黑暗一天，AI数学新纪元真来了！</a>— 柏拉图梦见电子羊（本文查核的對象）
