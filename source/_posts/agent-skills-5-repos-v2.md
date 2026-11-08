---
title: 五個 AI Agent Skills 資源庫：把「怎麼做」寫成檔案之後
date: 2026-11-08 22:30:00
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
  - AgentShield
  - Awesome LLM Apps
  - Addy Osmani
  - constraint-driven-development
  - 導讀
toc: true
index_img: /img/covers/agent-skills-5-repos-v2.png
banner_img: /img/covers/agent-skills-5-repos-v2.png
---

![五個 AI Agent Skills 資源庫](/img/covers/agent-skills-5-repos-v2.png)

## 一句話總結

編碼代理不缺寫程式的力氣，缺的是<strong>「每次都照同一套規矩做」</strong>。
Agent Skill 就是一個資料夾：一份 `SKILL.md` 寫清楚「什麼時候該用、步驟是什麼、做完的標準是什麼」，
代理在開工前讀它，於是需求分析、測試、除錯、review 這些流程不必每次重講。

這篇導讀整理 KDnuggets 的
[5 Best GitHub Repositories for AI Agent Skills](https://www.kdnuggets.com/5-best-github-repositories-for-ai-agent-skills)，
但<strong>每一個數字我都回到 GitHub API 重新數過</strong>——原文刊出後有幾個值和今天對不上，差異在 §4 逐一列出。

> 這是重寫版。前一版漏掉了 `AgentShield`、`constraint-driven-development`
> 與實際目錄計數，這版補齊並標明查證方式。
<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 500" role="img" aria-label="五個 agent skills 資源庫在流程嚴謹度與隨附機械上的定位" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto"><rect x="0.75" y="0.75" width="938" height="498" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="21" fill="#e6edf3" font-weight="700" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">五個技能庫：流程嚴謹度 × 隨附機械</text><text x="40" y="70" font-size="13" fill="#8b949e" font-weight="400" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">橫軸往右＝流程越被框架綁住　縱軸往下＝除了 SKILL.md 還帶越多東西</text><rect x="150" y="96" width="730" height="304" rx="12" fill="#0f141b" stroke="#222b36"/><line x1="515" y1="96" x2="515" y2="400" stroke="#1d2733" stroke-dasharray="6 6"/><line x1="150" y1="250" x2="880" y2="250" stroke="#1d2733" stroke-dasharray="6 6"/><text x="158" y="426" font-size="12.5" fill="#8b949e" font-weight="400" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">← 自主組合</text><text x="872" y="426" font-size="12.5" fill="#8b949e" font-weight="400" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">完整方法論 →</text><text x="138" y="140" font-size="12.5" fill="#8b949e" font-weight="400" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只有技能</text><text x="138" y="380" font-size="12.5" fill="#8b949e" font-weight="400" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">平台級</text><text x="164" y="122" font-size="12" fill="#3d4b5c" font-weight="400" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">零件箱</text><text x="866" y="122" font-size="12" fill="#3d4b5c" font-weight="400" text-anchor="end" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">生產線＋關卡</text><text x="164" y="388" font-size="12" fill="#3d4b5c" font-weight="400" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">記憶＋生態</text><circle cx="300" cy="180" r="7" fill="#2dd4bf" opacity="0.9"/><circle cx="300" cy="180" r="13" fill="none" stroke="#2dd4bf" opacity="0.35"/><text x="300" y="158" font-size="14" fill="#2dd4bf" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Superpowers</text><text x="300" y="214" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">完整方法論</text><circle cx="330" cy="310" r="7" fill="#bc8cff" opacity="0.9"/><circle cx="330" cy="310" r="13" fill="none" stroke="#bc8cff" opacity="0.35"/><text x="330" y="288" font-size="14" fill="#bc8cff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ECC</text><text x="330" y="344" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">314 技能 / 71 代理</text><circle cx="600" cy="195" r="7" fill="#58a6ff" opacity="0.9"/><circle cx="600" cy="195" r="13" fill="none" stroke="#58a6ff" opacity="0.35"/><text x="600" y="173" font-size="14" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Pocock</text><text x="600" y="229" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">小型可組合</text><circle cx="742" cy="165" r="7" fill="#fbbf24" opacity="0.9"/><circle cx="742" cy="165" r="13" fill="none" stroke="#fbbf24" opacity="0.35"/><text x="742" y="143" font-size="14" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Osmani</text><text x="742" y="199" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">25 技能 / 六階段</text><circle cx="452" cy="315" r="7" fill="#ff7b72" opacity="0.9"/><circle cx="452" cy="315" r="13" fill="none" stroke="#ff7b72" opacity="0.35"/><text x="452" y="293" font-size="14" fill="#ff7b72" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Awesome LLM Apps</text><text x="452" y="349" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">100+ 範例</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：把五套放上兩個維度，就能看出它們不是同一種東西——<strong>Superpowers 是方法論、Pocock 是零件箱、Osmani 是生產線、ECC 是平台，Awesome LLM Apps 則是範例集。</strong></figcaption>
</figure>

## 1. 它解決的不是「代理不夠聰明」

多數人第一次用編碼代理，會貼一大段落落長的指示：「先規劃、再寫測試、不要亂改、最後給我 review」。
問題是三十分鐘後那段話就被沖掉了，代理只記得最近幾輪。

技能的機制很簡單，但效果不一樣：

| | 每次貼一段提示詞 | 用 SKILL.md |
|---|---|---|
| 觸發 | 你要記得貼 | 依 `description` 自動命中 |
| 一致性 | 每次寫法都不同 | 每次跑同一套流程 |
| 內容長度 | 塞在對話裡，容易被截斷 | 拆成多檔，按需載入 |
| 維護 | 改一次就要重貼一次 | 改檔案、進版控、可 review |

所以「技能」真正修的是<strong>「代理每次都要重新學你的規矩」</strong>——
它把口頭約定變成有版本的檔案。

## 2. 五個資源庫在哪個位置

它們常被並列成「前五名」，但五個東西的形狀差很多。
我用兩個維度擺放：<strong>流程被綁得多緊</strong>，以及<strong>除了 SKILL.md 還附帶多少機械</strong>。

<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 470" role="img" aria-label="依需求選擇 agent skills 資源庫的決策流程" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto"><rect x="0.75" y="0.75" width="938" height="468" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="40" y="44" font-size="21" fill="#e6edf3" font-weight="700" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">先問自己：我缺的是「流程」還是「材料」？</text><text x="40" y="70" font-size="13" fill="#8b949e" font-weight="400" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">只挑一個主幹，跑一兩週再客製 SKILL.md——不要三套一起裝</text><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#3d4b5c"/></marker></defs><rect x="370" y="100" width="200" height="62" rx="10" fill="#0f141b" stroke="#e6edf3" stroke-width="1.2"/><text x="470" y="130" font-size="13.5" fill="#e6edf3" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">你要交付什麼？</text><text x="470" y="152" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">先分清楚缺哪一塊</text><line x1="400" y1="162" x2="230" y2="214" stroke="#3d4b5c" stroke-width="1.4" marker-end="url(#a)"/><line x1="470" y1="162" x2="470" y2="214" stroke="#3d4b5c" stroke-width="1.4" marker-end="url(#a)"/><line x1="540" y1="162" x2="710" y2="214" stroke="#3d4b5c" stroke-width="1.4" marker-end="url(#a)"/><rect x="110" y="214" width="240" height="72" rx="10" fill="#0f141b" stroke="#fbbf24" stroke-width="1.2"/><text x="230" y="244" font-size="13.5" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">流程不穩</text><text x="230" y="266" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每次都重新講一遍</text><rect x="350" y="214" width="240" height="72" rx="10" fill="#0f141b" stroke="#2dd4bf" stroke-width="1.2"/><text x="470" y="244" font-size="13.5" fill="#2dd4bf" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">要團隊稽核</text><text x="470" y="266" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">可驗證、可回滾</text><rect x="590" y="214" width="240" height="72" rx="10" fill="#0f141b" stroke="#bc8cff" stroke-width="1.2"/><text x="710" y="244" font-size="13.5" fill="#bc8cff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">缺記憶／安全</text><text x="710" y="266" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">跨 session 累積</text><line x1="230" y1="286" x2="230" y2="330" stroke="#3d4b5c" stroke-width="1.4" marker-end="url(#a)"/><line x1="470" y1="286" x2="470" y2="330" stroke="#3d4b5c" stroke-width="1.4" marker-end="url(#a)"/><line x1="710" y1="286" x2="710" y2="330" stroke="#3d4b5c" stroke-width="1.4" marker-end="url(#a)"/><rect x="110" y="330" width="240" height="74" rx="10" fill="#0f141b" stroke="#fbbf24" stroke-width="1.2"/><text x="230" y="360" font-size="13.5" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Osmani</text><text x="230" y="382" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">六階段＋25 技能</text><rect x="350" y="330" width="240" height="74" rx="10" fill="#0f141b" stroke="#2dd4bf" stroke-width="1.2"/><text x="470" y="360" font-size="13.5" fill="#2dd4bf" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Superpowers</text><text x="470" y="382" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">完整方法論</text><rect x="590" y="330" width="240" height="74" rx="10" fill="#0f141b" stroke="#bc8cff" stroke-width="1.2"/><text x="710" y="360" font-size="13.5" fill="#bc8cff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ECC</text><text x="710" y="382" font-size="11.5" fill="#8b949e" font-weight="400" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">314 技能／71 代理</text><text x="110" y="434" font-size="12" fill="#8b949e" font-weight="400" text-anchor="start" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">要可組合的零件箱 → Pocock；要範例程式碼 → Awesome LLM Apps</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：先問「我缺哪一塊」，再決定裝哪一套。<strong>三個分支互斥；確認主幹跑順了，才考慮再加第二個。</strong></figcaption>
</figure>

一句話版本：

- <strong>Superpowers</strong>：直接給你一套開發方法論，照著走。
- <strong>Pocock</strong>：給你一箱零件，自己組。
- <strong>Osmani</strong>：給你一條有品質關卡的生產線（DEFINE→PLAN→BUILD→VERIFY→REVIEW→SHIP）。
- <strong>ECC</strong>：給你一整座平台，技能只是其中一個模組。
- <strong>Awesome LLM Apps</strong>：不是流程，是 100+ 個可跑的範例。

## 3. 逐個看：亮點與代價

### 3.1 Superpowers — 把流程交出去

`obra/superpowers`，Jesse Vincent（Prime Radiant），MIT，約 314K 星。

它不只是加能力，而是<strong>改變代理做事的順序</strong>：先反問需求 → 設計核可 → 寫計畫 →
子代理實作 → TDD → review → 驗證 → 才收分支。
除錯走 `systematic-debugging` 的四階段根因，不准「亂改到剛好會過」。

代價三個，原文沒講：

1. <strong>它會改你的工作方式</strong>。既有的 Git 流程會被它接管一段。
2. 專案<strong>原則上不收新技能投稿</strong>，也不接受代理代寫的 PR。
3. 內建<strong>可關閉的遙測</strong>（只回報版本），用 `SUPERPOWERS_DISABLE_TELEMETRY` 關掉。

### 3.2 Skills for Real Engineers — 保持小、保持可拆

`mattpocock/skills`，Matt Pocock，MIT，約 318K 星（目前星數最高）。

README 開頭就在批 GSD、BMAD、Spec-Kit：「它們想幫你，但同時拿走了控制權，
讓流程本身的 bug 很難修。」所以這裡的技能刻意做小，分「你主動呼叫」與「模型自己判斷」兩類。

最值得先試的是 `grill-with-docs`：它<strong>反過來訪談你</strong>，邊問邊建共用領域模型、
統一術語、同步更新 `CONTEXT.md` 與 ADR——把「猜」換成「問」。
`code-review` 是雙軸（標準 vs. 規格，平行子代理互不污染），`pr` 會要你判斷單向門還是雙向門。

代價：<strong>只接受協作者開 PR</strong>，所以它更像參考實作，不是社群共養的套件。

### 3.3 ECC — 技能只是其中一個模組

`affaan-m/ECC`，Affaan Mustafa，MIT，約 299K 星，4,327 次提交（五套裡最活躍）。

它的重點不是技能數量（雖然多到誇張），而是<strong>會累積</strong>：

- **記憶**：`unified-memory`、`context-and-decisions`、`context-budget`，跨 session 保留決策。
- **持續學習**：`continuous-learning`、`continuous-learning-v2`，加上 `/instinct-status`、
  `/instinct-import`、`/instinct-export`、`/evolve`、`/prune`，把工作過程中的行為蒸餾成可重用的「本能」。
- **安全掃描**：<strong>AgentShield</strong>，掃 secrets、權限、hooks 與 MCP 設定。
  它有自己的 CLI（`agentshield scan`、`agentshield init`）、GitHub Action、SARIF／HTML／JSON 報告與政策包。

代價很明顯：<strong>裝得最重、改動最頻繁</strong>。適合已經把代理當「工作環境」而非「工具」的人。

### 3.4 Agent Skills — 有品質關卡的生產線

`addyosmani/agent-skills`，Addy Osmani，MIT，約 114K 星。

形狀最清楚：六個階段對應 9 個指令
（`/spec`、`/plan`、`/build`、`/test`、`/review`、`/ship`、`/constraints`、`/code-simplify`、`/webperf`），
另附 4 個角色、7 份檢查清單、25 個評測案例。

判斷標準直接取自 Google 工程文化：Hyrum 定律（API）、碧昂絲規則與測試金字塔、
Chesterton's Fence（簡化）、主幹開發、Shift Left 與功能旗標。

<strong>最值得抄的一招是 `constraint-driven-development`</strong>。它的主張常被誤解成
「把檢查往後丟以省時間」，但 SKILL.md 原文說的是另一件事：

> Constraint-driven development defines what "good enough to ship" means, before anyone argues about it in a pull request.

它做的事是：訪談你「哪些維度重要」（覆蓋率、效能、無障礙），把數字寫進 **`CONSTRAINTS.md`**，
然後<strong>盯著 diff 有沒有偷偷降標準</strong>——新增 `@ts-ignore`、`eslint-disable`、
跳過或刪掉測試、把門檻調低。原文有一句很到位：

> "The agent proposed relaxing a threshold instead of fixing the code."

至於「昂貴檢查放後段」，那是它講的<strong>階段擺放（placement）</strong>：
先跑一套 diff-only、幾秒鐘的「floor」，慢的檢查（完整測試、安全掃描、效能）留在後面。
原文也講清楚這不是效能藉口：<strong>"It's only a placement error, not an argument against constraints."</strong>

### 3.5 Awesome LLM Apps — 不是方法論，是材料庫

`Shubhamsaboo/awesome-llm-apps`，Shubham Saboo，<strong>Apache-2.0</strong>，約 144K 星。

100+ 個可跑範例（README 直接寫「clone、上線、甚至轉售都行」）：
starter／advanced agents、always-on、voice、generative UI、MCP agents、RAG tutorials，
以及 Google ADK 與 OpenAI Agents SDK 的速成。裡面還有像
<strong>Scope Creep Detector</strong>、<strong>Commit Archaeologist</strong> 這種單點技能。

它和其他四套<strong>不衝突</strong>，可以並存。裝單一技能只要一行：

```bash
npx skills add https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/agent_skills/project-graveyard
```


## 4. 原文數字 vs 我實測（這節是重點）

我用 GitHub API 直接數目錄，不靠 README 的自述。結果：

| 項目 | 原文／常見說法 | 我實測（2026-11-08） | 差異原因 |
|---|---|---|---|
| ECC 技能 | 292 | **314** | 目錄持續增加 |
| ECC 代理 | 68 | **71** | 同上 |
| Osmani 技能 | 24 | **25** | 多一個 `using-agent-skills`（meta 技能） |
| 星數第一 | Superpowers | **Pocock 317.8K** | 已超越 |
| 授權 | 原文未提 | 4×MIT、**1×Apache-2.0** | Awesome LLM Apps 是 Apache-2.0 |

三點實務提醒：

1. <strong>目錄數 ≠ 可用技能數</strong>。ECC 的 `skills/` 有 314 個目錄，但裡面混了
   `plankton-code-quality`、`codehealth-mcp` 這種需要額外安裝的選項。
2. <strong>星數會騙人</strong>。這類專案的成長很大一部分來自「一鍵裝 plugin」的曝光紅利，
   跟技能本身好不好用不是同一件事。
3. <strong>授權要看</strong>。四套 MIT、一套 Apache-2.0；商用都在允許範圍，
   但 Apache-2.0 多了專利授權條款與聲明保留義務。要在公司落地，這比星數重要。

## 5. 怎麼選：先挑一個，別全裝

三套（Superpowers／Pocock／Osmani）都覆蓋「規劃、TDD、review」這批同樣的觸發點。
同時載入的結果不是「更嚴謹」，而是<strong>代理收到互相衝突的指示</strong>：
一個要你先寫計畫、一個要你先訪談你、一個要你走 `/spec`。
實際表現通常是卡住，或只挑最省事的那條路。


我的順序建議：

1. 先挑<strong>一個</strong>當主幹，跑一兩週。
2. 只補你確實缺的單一技能，不要整套搬。
3. 再改 `SKILL.md`。原文作者也是這樣收尾的——價值不在「讓代理更聰明」，
   而是<strong>教它你希望軟體怎麼被做出來</strong>。

判別品質的方法很簡單：<strong>看它有沒有附評測</strong>。
Osmani 有 25 個 evals、Superpowers 有 harness、Pocock 有 changesets；
有評測的，至少作者願意被檢驗。

## 6. 原文與延伸

| 專案 | 網址 | 星數 | 授權 | 技能／代理數 |
|---|---|---|---|---|
| Superpowers | [obra/superpowers](https://github.com/obra/superpowers) | 314.2K | MIT | 技能 20+ |
| Skills for Real Engineers | [mattpocock/skills](https://github.com/mattpocock/skills) | 317.8K | MIT | 技能 25+ |
| ECC | [affaan-m/ECC](https://github.com/affaan-m/ECC) | 299.2K | MIT | 314 技能／71 代理 |
| Awesome LLM Apps | [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | 144.1K | Apache-2.0 | 100+ 範例 |
| Agent Skills | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 113.9K | MIT | 25 技能／9 指令 |

原文：[5 Best GitHub Repositories for AI Agent Skills](https://www.kdnuggets.com/5-best-github-repositories-for-ai-agent-skills)（KDnuggets）

> <strong>查證說明</strong>：星數、授權與目錄數於 2026-11-08 透過 GitHub REST API 直接讀取
> （`stargazers_count`、`license.spdx_id`、`contents/` 的目錄計數），不是抄 README 的自述。
> 星數每天變動，引用前請自行複查。`constraint-driven-development` 與 AgentShield 的敘述
> 均取自各自的 SKILL.md 與 `docs/` 原文引述；我沒有實跑任何一個技能庫。
>
> <strong>封面與圖表</strong>：封面由本機 ComfyUI 的 Qwen-Image 2.1 生成（刻意不含文字，文字交給圖說）；
> 圖 1、圖 2 為手繪內嵌 SVG——含中文標籤的圖表若交給 AI 生圖，字形會爛成方塊。
