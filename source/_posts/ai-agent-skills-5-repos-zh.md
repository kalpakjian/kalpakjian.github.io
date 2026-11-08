---
title: 五個 AI Agent Skills 技能庫導讀：從「會寫程式」到「會做軟體工程」
date: 2026-11-08 21:40:00
categories:
  - AI 研究札記
  - 工具鏈
tags:
  - Agent Skills
  - SKILL.md
  - Claude Code
  - Codex
  - Cursor
  - Superpowers
  - Matt Pocock
  - ECC
  - Awesome LLM Apps
  - Addy Osmani
  - 導讀
  - 開源專案
toc: true
index_img: /img/covers/ai-agent-skills-5-repos-zh.png
banner_img: /img/covers/ai-agent-skills-5-repos-zh.png
---

![AI Agent Skills 技能庫導讀](/img/covers/ai-agent-skills-5-repos-zh.png)

## 一句話總結

編碼代理已經很會寫程式，但軟體工程不是只有寫程式。
<strong>Agent Skill（代理技能）把「怎麼做」寫成可重複載入的檔案</strong>，讓代理每次都用同一套流程做事，不必你每次重講一遍。

這篇導讀整理的原文是 KDnuggets 的
[5 Best GitHub Repositories for AI Agent Skills](https://www.kdnuggets.com/5-best-github-repositories-for-ai-agent-skills)（Abid Ali Awan，2026-10-21）。
原文沒有寫授權，星數也已經過時；下面每個數字我都回到專案頁重新查證過，
<strong>並補上原文漏掉的授權差異</strong>。

## 1. 先弄清楚：Agent Skill 到底是什麼

不是外掛、不是 MCP server、也不是另一個 agent framework。
它就是一個資料夾，裡面放一份 `SKILL.md`（front-matter 寫名稱與「什麼時候該用」），
再加上選用的腳本與參考資料。代理在開工前讀它，然後照著做。

這件事的差別在於<strong>可重複</strong>：

| | 每次貼一段落落長的提示詞 | 用 Agent Skill |
|---|---|---|
| 觸發方式 | 你要記得貼 | 依 `description` 自動命中 |
| 一致性 | 每次寫法都不同 | 每次都同一套流程 |
| 複雜度 | 塞在對話裡，容易被沖掉 | 拆成多個檔案，按需載入 |
| 可維護 | 改一次就要重貼一次 | 改檔案即可，進版控 |

所以「技能」解決的不是「代理不夠聰明」，而是<strong>「代理每次都要重新學你的規矩」</strong>。

## 2. 五套技能庫，其實不是同一種東西

多數文章喜歡把這五個並列成「前五名」，但它們的定位差異很大。
我把它們放在兩個維度上：<strong>誰握著流程</strong>，以及<strong>除了 SKILL.md 還附帶多少東西</strong>。

<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 470" role="img" aria-label="五套 agent skills 技能庫在流程掌控與隨附機械兩個維度上的位置" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto"><rect x="0.75" y="0.75" width="938.5" height="468.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="21" fill="#e6edf3" font-weight="700" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">五套技能庫的位置：流程掌控 × 隨附機械</text><text x="40" y="70" font-size="13.5" fill="#8b949e" font-weight="400" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">橫軸：誰握著流程　縱軸：除了 SKILL.md 還附帶多少東西</text><rect x="120" y="92" width="760" height="288" rx="12" fill="#0f141b" stroke="#222b36"/><line x1="500" y1="92" x2="500" y2="380" stroke="#1d2733" stroke-dasharray="6 6"/><line x1="120" y1="250" x2="880" y2="250" stroke="#1d2733" stroke-dasharray="6 6"/><text x="128" y="406" font-size="12.5" fill="#8b949e" font-weight="400" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">← 框架接管流程</text><text x="872" y="406" font-size="12.5" fill="#8b949e" font-weight="400" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">自己組裝 →</text><text x="108" y="136" font-size="12.5" fill="#8b949e" font-weight="400" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只有技能檔</text><text x="108" y="360" font-size="12.5" fill="#8b949e" font-weight="400" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">平台級</text><text x="134" y="118" font-size="12" fill="#3d4b5c" font-weight="400" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">方法論／完整流程</text><text x="866" y="118" font-size="12" fill="#3d4b5c" font-weight="400" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">生產級流程＋評測</text><text x="134" y="368" font-size="12" fill="#3d4b5c" font-weight="400" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">平台＋記憶＋生態</text><circle cx="232" cy="176" r="7" fill="#2dd4bf" opacity="0.9"/><circle cx="232" cy="176" r="13" fill="none" stroke="#2dd4bf" opacity="0.35"/><text x="232" y="154" font-size="14" fill="#2dd4bf" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Superpowers</text><text x="232" y="210" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">完整方法論</text><circle cx="330" cy="300" r="7" fill="#bc8cff" opacity="0.9"/><circle cx="330" cy="300" r="13" fill="none" stroke="#bc8cff" opacity="0.35"/><text x="330" y="278" font-size="14" fill="#bc8cff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ECC</text><text x="330" y="334" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">平台／記憶</text><circle cx="560" cy="200" r="7" fill="#58a6ff" opacity="0.9"/><circle cx="560" cy="200" r="13" fill="none" stroke="#58a6ff" opacity="0.35"/><text x="560" y="178" font-size="14" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Pocock</text><text x="560" y="234" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">小型可組合</text><circle cx="716" cy="160" r="7" fill="#fbbf24" opacity="0.9"/><circle cx="716" cy="160" r="13" fill="none" stroke="#fbbf24" opacity="0.35"/><text x="716" y="138" font-size="14" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Osmani</text><text x="716" y="194" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">六階段＋evals</text><circle cx="500" cy="300" r="7" fill="#ff7b72" opacity="0.9"/><circle cx="500" cy="300" r="13" fill="none" stroke="#ff7b72" opacity="0.35"/><text x="500" y="278" font-size="14" fill="#ff7b72" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Awesome LLM Apps</text><text x="500" y="334" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">範例程式庫</text></svg>
圖 1：把五套放在兩個維度上，就能看出它們不是同一種東西。<strong>Superpowers 是方法論、Pocock 是零件箱、Osmani 是生產線，ECC 是平台，Awesome LLM Apps 則是範例集。</strong>
</figure>

一句話版本：

- <strong>Superpowers</strong> 直接給你一套開發方法論，你照著走。
- <strong>Pocock</strong> 給你一箱零件，你自己組。
- <strong>Osmani</strong> 給你一條有品質閘門的生產線（六階段 + 9 個指令）。
- <strong>ECC</strong> 給的是一整個平台：技能、本能、記憶、hooks、多語言 rules。
- <strong>Awesome LLM Apps</strong> 根本不是流程，它是 100+ 個可跑的範例集。

原文把 ECC 說成「把編碼代理變成工程平台」，這個描述是準的；
但原文沒有提到它另外還有 `instinct-import`、`evolve` 這類<strong>會從工作過程累積行為</strong>的機制，
那才是它與其他四套最大的差別。

## 3. 逐一套看：亮點與代價

### 3.1 Superpowers — 把流程交出去

`obra/superpowers`，Jesse Vincent（Prime Radiant）。

技能分四組：測試（`test-driven-development`、`root-cause-tracing`）、
除錯（`systematic-debugging` 四階段根因流程、`verification-before-completion`）、
協作（`brainstorming`、`writing-plans`、`subagent-driven-development`、
`requesting-code-review`／`receiving-code-review`、`using-git-worktrees`）、
後設（`writing-skills`）。

實際跑起來是這樣：你丟出一個需求，它先<strong>反問</strong>你要什麼，
設計核可後才寫計畫，再用子代理實作、走 TDD、審查、驗證，最後才收分支。

代價有三個，原文沒講：

1. <strong>它會改你的工作方式</strong>，不只是加能力。如果你已經有既定的 Git 流程，會覺得被綁住。
2. 專案<strong>原則上不接受新的技能投稿</strong>，也不接受代理代寫的 PR。想客製就自己 fork。
3. 內建<strong>可關閉的遙測</strong>（只回報版本號），要關得設 `SUPERPOWERS_DISABLE_TELEMETRY`。

### 3.2 Skills for Real Engineers — 保持小、保持可拆

`mattpocock/skills`，Matt Pocock。

README 開頭就在批評 GSD、BMAD、Spec-Kit：
「它們想幫你，但同時拿走了你的控制權，讓流程本身的 bug 很難修。」
所以這裡的技能刻意做小，分成「你主動呼叫」與「模型自己判斷」兩類。

最值得先試的是 `grill-with-docs`：它不猜你要什麼，而是<strong>反過來訪談你</strong>，
一邊問一邊建立共用的領域模型、統一術語，同步更新 `CONTEXT.md` 與 ADR。
`code-review` 則是雙軸審查（標準 vs. 規格，用平行子代理互不污染），
`pr` 會要你判斷這是「單向門」還是「雙向門」。

代價：<strong>只接受協作者開 PR</strong>，所以它更像一份「參考實作」，不是社群共養的套件。

### 3.3 ECC — 技能只是其中一個模組

`affaan-m/ECC`，Affaan。四套裡面提交數最多（4,327 次）。

除了技能，它還帶：<strong>instincts</strong>（可匯入／匯出／演化的行為）、
<strong>hooks</strong>（PreToolUse／PostToolUse／Stop，含 session 記憶持久化）、
<strong>per-language rules</strong>（TypeScript、Python、Go、Swift、PHP、ArkTS，
含 80% 覆蓋率要求），以及 MCP 設定與 Docker scaffold。

代價很明顯：<strong>裝得最重、改動最頻繁</strong>。
它適合已經把代理當「工作環境」而不是「工具」的人。

### 3.4 Agent Skills — 有品質閘門的生產線

`addyosmani/agent-skills`，Addy Osmani。

形狀最清楚：六個階段對應 9 個斜線指令
（`/spec`、`/plan`、`/build`、`/test`、`/review`、`/ship`…），
另附 4 個角色、7 份檢查清單、25 個評測案例、13 支驗證腳本。

判斷標準直接取自 Google 工程文化：Hyrum 定律（API 設計）、
碧昂絲規則與測試金字塔（測試）、Chesterton's Fence（簡化）、
主幹開發（Git）、Shift Left 與功能旗標（CI/CD），
還有一個專門把程式碼當<strong>負債</strong>處理的棄用技能。

它最特別的地方是自己附了 `docs/comparison.md`：
老實地把 Superpowers、Pocock、它自己三方對照，甚至附上受控的對照實驗連結。

### 3.5 Awesome LLM Apps — 不是方法論，是材料庫

`Shubhamsaboo/awesome-llm-apps`，Shubham Saboo。

100+ 個可跑的範例（Apache-2.0，README 直接寫「clone、上線、甚至轉售都行」）：
starter／advanced agents、always-on agents、voice agents、generative UI、
MCP agents、RAG tutorials、Google ADK 與 OpenAI Agents SDK 速成。

它跟其他四套<strong>不衝突</strong>，可以並存。要裝單一技能只要一行：

```bash
npx skills add https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/agent_skills/project-graveyard
```

## 4. 原文沒說、但我覺得更重要的三件事

<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 470" role="img" aria-label="五個專案在技能數量、可驗證性與額外資產上的對照" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto"><rect x="0.75" y="0.75" width="938.5" height="468.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="21" fill="#e6edf3" font-weight="700" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">安裝之後你實際拿到什麼</text><text x="40" y="70" font-size="13.5" fill="#8b949e" font-weight="400" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同為寬鬆授權（4×MIT、1×Apache-2.0），內容物差很多</text><text x="330" y="116" font-size="12.5" fill="#8b949e" font-weight="600" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">技能／指令</text><text x="540" y="116" font-size="12.5" fill="#8b949e" font-weight="600" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">可驗證性</text><text x="730" y="116" font-size="12.5" fill="#8b949e" font-weight="600" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">額外資產</text><text x="44" y="116" font-size="12.5" fill="#8b949e" font-weight="600" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">專案</text><rect x="28" y="122" width="884" height="52" rx="10" fill="#111820"/><rect x="28" y="122" width="4" height="52" rx="2" fill="#2dd4bf"/><text x="44" y="152" font-size="13.5" fill="#2dd4bf" font-weight="700" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Superpowers</text><text x="330" y="152" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">技能 20+</text><text x="540" y="152" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">evals harness</text><text x="730" y="152" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">多代理 plugin</text><rect x="28" y="180" width="4" height="52" rx="2" fill="#58a6ff"/><text x="44" y="210" font-size="13.5" fill="#58a6ff" font-weight="700" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Pocock</text><text x="330" y="210" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">技能 25+</text><text x="540" y="210" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">changesets</text><text x="730" y="210" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">PR 限協作者</text><rect x="28" y="238" width="884" height="52" rx="10" fill="#111820"/><rect x="28" y="238" width="4" height="52" rx="2" fill="#fbbf24"/><text x="44" y="268" font-size="13.5" fill="#fbbf24" font-weight="700" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Osmani</text><text x="330" y="268" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">技能＋9 指令</text><text x="540" y="268" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">evals 25 例</text><text x="730" y="268" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4 角色 7 清單</text><rect x="28" y="296" width="4" height="52" rx="2" fill="#bc8cff"/><text x="44" y="326" font-size="13.5" fill="#bc8cff" font-weight="700" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ECC</text><text x="330" y="326" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">技能＋指令</text><text x="540" y="326" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">hooks＋記憶</text><text x="730" y="326" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">多語言 rules</text><rect x="28" y="354" width="884" height="52" rx="10" fill="#111820"/><rect x="28" y="354" width="4" height="52" rx="2" fill="#ff7b72"/><text x="44" y="384" font-size="13.5" fill="#ff7b72" font-weight="700" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Awesome LLM Apps</text><text x="330" y="384" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">100+ 範例</text><text x="540" y="384" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">agent_skills</text><text x="730" y="384" font-size="12.5" fill="#c9d1d9" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Apache-2.0</text><text x="44" y="442" font-size="12" fill="#57657a" font-weight="400" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">「可驗證性」＝ 專案自己有沒有附評測，讓你能判斷某個技能到底有沒有效。</text></svg>
圖 2：同樣叫「技能庫」，內容物差別很大。<strong>Osmani 附了 25 個評測案例，Pocock 只讓協作者送 PR，Awesome LLM Apps 則是可直接轉售的 Apache-2.0 範例集。</strong>
</figure>

### 4.1 星數不能當品質指標，而且原文的數字已經過時

原文刊出時寫的是 285.5K／260.1K／256.7K／137.3K／93.6K，
我實查後是 314.2K／317.8K／299.2K／144.1K／113.9K。
<strong>排序也變了：Pocock 已經超越 Superpowers。</strong>

而且這類專案的星數成長有很大一部分來自「一鍵安裝 plugin」帶來的曝光紅利，
跟技能本身好不好用不是同一件事。

### 4.2 四套是 MIT，一套不是

四個是 MIT，但 <strong>Awesome LLM Apps 是 Apache-2.0</strong>。
商用與 fork 都沒問題，差別在 Apache-2.0 多了專利授權條款與聲明保留義務。
原文完全沒提授權；如果你要在公司內部落地，這件事比星數重要。

### 4.3 不要疊著裝

Superpowers、Pocock、Osmani 三者都覆蓋「規劃／TDD／審查」這批同樣的觸發點。
同時載入會讓代理收到<strong>互相衝突的指示</strong>：一個要你先寫計畫、一個要你先訪談你、
一個要你走 `/spec`。衝突的結果通常不是「更嚴謹」，而是「卡住」或「只挑最省事的那條路」。

我的順序建議：

1. 先挑一套當主幹（團隊要稽核 → Osmani；想讓流程被決定 → Superpowers；想自己組 → Pocock）。
2. 只補你缺的單一技能，不要整套搬。
3. 跑一兩週後再改 `SKILL.md`。原文作者最後也是這樣講的：
   價值不在「讓代理變聰明」，而是<strong>教它你希望軟體怎麼被做出來</strong>。

## 5. 我的實務結論

我會這樣用：

- <strong>Osmani 的六階段</strong>當骨架，因為它有明確的進入／離開條件，適合跟 CI 掛在一起。
- <strong>Pocock 的 grill-with-docs</strong> 拆出來單獨用，它解決的是「需求沒講清楚」這個最大宗問題。
- <strong>ECC 的 hooks 與 rules</strong> 只取「提交前跑測試」這一段，不整套裝。
- <strong>Awesome LLM Apps</strong> 當範例庫，需要某個 agent 樣板時去翻。

最後一個判別方法：這些技能的品質落差很大，
有些只是把一段提示詞包成資料夾，有些則真的把流程寫成可驗證的狀態機。
<strong>看它有沒有附評測。</strong>
有 evals 的，至少作者願意被檢驗；沒有的，就只能自己實測。

## 6. 原文與延伸

| 專案 | 網址 | 星數（實查） | 授權 |
|---|---|---|---|
| Superpowers | [obra/superpowers](https://github.com/obra/superpowers) | 314.2K | MIT |
| Skills for Real Engineers | [mattpocock/skills](https://github.com/mattpocock/skills) | 317.8K | MIT |
| ECC | [affaan-m/ECC](https://github.com/affaan-m/ECC) | 299.2K | MIT |
| Awesome LLM Apps | [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | 144.1K | Apache-2.0 |
| Agent Skills | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 113.9K | MIT |

原文：[5 Best GitHub Repositories for AI Agent Skills](https://www.kdnuggets.com/5-best-github-repositories-for-ai-agent-skills)（KDnuggets）

> <strong>查證說明</strong>：本文星數與授權於 2026-11-08 直接讀取各專案 GitHub 頁面；
> 星數每天都在變，引用前請自行複查。原文提到的安裝指令
> （`/plugin install superpowers@claude-plugins-official`）我沒有實測。
>
> <strong>封面與圖表</strong>：封面由本機 ComfyUI 的 Qwen-Image 2.1 生成（刻意不含文字，說明放在圖說）；
> 圖 1、圖 2 為手繪內嵌 SVG，不是 AI 生圖——含中文標籤的圖表交給 AI 生圖會爛成方塊。
