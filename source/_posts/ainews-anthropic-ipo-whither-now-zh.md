---
title: AINews 導讀：Anthropic 的估值焦慮與四張新面孔
date: 2026-11-07 20:30:00
categories:
  - AI 研究札記
  - 產業觀察
tags:
  - AINews
  - Latent Space
  - Anthropic
  - IPO
  - S-1
  - 估值
  - 市場修正
  - Inkling 2 Small
  - Thinking Machines
  - Kimi K3.1 Pro
  - ERNIE-5.5
  - GPT Image 2.6
  - METR
  - AECI
  - 網路安全
  - 本地推論
  - 新聞導讀
toc: true
index_img: /img/covers/ainews-anthropic-ipo-whither-now-zh.png
banner_img: /img/covers/ainews-anthropic-ipo-whither-now-zh.png
---

> <strong>這篇在講什麼</strong>：Latent Space 的 AINews 在 2026-11-07 那期，標題是〈[AINews] Anthropic IPO: Whither Now?〉。表面上在談 Anthropic 的上市定價，實際上整期在回答一個更大的問題：**當「完美定價」的市場開始懷疑，AI 這條線的敘事還剩下多少緩衝？**
>
> 這篇是<strong>中文導讀</strong>：先講清楚「Anthropic 上市」這件事的數字結構，再整理同期的模型發表（Inkling 2 Small、Kimi K3.1 Pro、ERNIE-5.5、GPT Image 2.6）、獨立評測（端點保真度、VIALS-AA、CyberOffense）與本地推論圈的新動態，最後給我的判讀。
>
> 原文：[lspace.beehiiv.com/p/ainews-anthropic-ipo-whither-now](https://lspace.beehiiv.com/p/ainews-anthropic-ipo-whither-now)。覆蓋時段 2026-11-05 至 11-06。整理日期 2026-11-07。**第 1、3、4 節為原文內容整理，第 2、5 節為我的判讀**，兩種分開標註。

## 一句話總結

> **這一期不是「又有新模型」，而是「AI 的財務敘事第一次被自己的估值反過來咬住」。**

Anthropic 的年化收入正走向 **$80B**（年終目標 $100B，已達 80%），但 IPO 估值被討論從 **$1.5T** 砍到 **$1T**，Polymarket 上「年內 IPO」的機率**掉了 18%**。而同一期裡模型能力還在往前跑（Inkling 2 Small 創下美國開源權重新高）——**供給側在加速，需求側的錢卻開始猶豫**。這個張力才是這期的重點。


## 1. Anthropic 上市：先把三個數字擺在一起

### 1.1 三個數字互相打架

AINews 開頭寫得很直白：那斯達克跌了 **10%**，還沒到熊市的 **20%**，但因為市場「price to perfection」（一切都被定價到完美），**任何不是上行的意外，都會被當成下行處理**。

<!-- FIG1 -->
<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 500" role="img" aria-label="Anthropic 估值的三個錨點：營收 run-rate、IPO 估值、市場機率" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto"><rect x="0.75" y="0.75" width="938.5" height="498.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="48" y="46" font-size="21" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同一家公司，三種「大小」</text><text x="48" y="72" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">營收在成長、估值在被砍、機率在下降 —— 三個箭頭不同向</text><rect x="48" y="96" width="270" height="176" rx="12" fill="#0f1a1e" stroke="#2dd4bf44"/><text x="70" y="124" font-size="13" fill="#2dd4bf" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">營收 run-rate（事實）</text><text x="70" y="178" font-size="34" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">$80B</text><text x="70" y="206" font-size="12.5" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">年終目標 $100B</text><text x="70" y="228" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">已達 80%，仍在長</text><rect x="334" y="96" width="270" height="176" rx="12" fill="#1a2029" stroke="#fbbf2433"/><text x="356" y="124" font-size="13" fill="#fbbf24" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">IPO 估值（共識）</text><text x="356" y="178" font-size="34" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">$1T</text><text x="356" y="206" font-size="12.5" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">先前討論的 $1.5T</text><text x="356" y="228" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">投資人質疑後下修</text><rect x="620" y="96" width="272" height="176" rx="12" fill="#1f1a1a" stroke="#ff7b7244"/><text x="642" y="124" font-size="13" fill="#ff7b72" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">年內 IPO 機率（情緒）</text><text x="642" y="178" font-size="34" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-18%</text><text x="642" y="206" font-size="12.5" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Polymarket，兩天內</text><text x="642" y="228" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">市場選擇先等</text><text x="60" y="316" font-size="13" fill="#c9d1d9" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">那斯達克：還沒到熊市，但已經是「不能出錯」的市場</text><line x1="60" y1="376" x2="884" y2="376" stroke="#30363d" stroke-width="2"/><line x1="60" y1="336" x2="884" y2="336" stroke="#30363d" stroke-width="1" stroke-dasharray="3 4"/><text x="60" y="330" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0%</text><rect x="440" y="352" width="180" height="24" rx="4" fill="#fbbf24" stroke="#fbbf2466"/><text x="530" y="344" font-size="14" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-10%</text><text x="530" y="398" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">修正區</text><line x1="800" y1="430" x2="800" y2="336" stroke="#ff7b72" stroke-width="1.5" stroke-dasharray="5 4"/><text x="800" y="330" font-size="11.5" fill="#ff7b72" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">-20%</text><text x="800" y="452" font-size="11.5" fill="#ff7b72" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">熊市線</text><text x="60" y="470" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">距離熊市還有一半空間，但「完美定價」意味著這一半可能一次就走完</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 1：三個數字必須一起看。<strong>營收是事實、估值是共識、機率是情緒</strong>——這期三者第一次明顯分叉。</figcaption>
</figure>
<!-- /FIG1 -->

### 1.2 這期真正的問題意識

原文明講：這是**週末加播的第二集** Anthropic IPO 系列，嘉賓是 Altimeter 的 **Jamin Ball**，題目叫「Anthropic S-1 Myths and Mythos」——那個雙關很關鍵：**S-1 是上市申請書，Mythos 是他們最強模型的代號**。

所以這集拆的是**兩層神話**：

1. **財務神話**：S-1 裡哪些數字可持續、哪些是一次性的
2. **能力神話**：Mythos 等級的模型到底代表什麼

> 標題「Whither Now?」問得很準：不是「會不會上市」，而是**「上市之後，這個敘事的下一段要講什麼」**。

---

---

## 2. 我的判讀：84 寫成 80 的距離，比 1.5T 寫成 1T 更值得注意

### 2.1 這兩件事其實是同一件事

如果把「估值被砍」跟「機率下降」分開看，會覺得只是情緒。但把三個數字疊起來就會看到一個結構：

<!-- FIG2 -->
<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 430" role="img" aria-label="估值倍數敏感度：同樣的營收，估值每降一級，需要的成長故事就更大" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto"><rect x="0.75" y="0.75" width="938.5" height="428.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="48" y="46" font-size="21" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">同樣的 $80B，換一個倍數就換一個故事</text><text x="48" y="72" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">倍數是市場給的；故事是公司要一直講下去的</text><line x1="120" y1="360" x2="880" y2="360" stroke="#30363d" stroke-width="1.5"/><text x="120" y="386" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">$0</text><text x="880" y="386" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">$1.6T</text><rect x="120" y="320" width="180" height="40" rx="5" fill="#7d8590" stroke="#7d859066"/><text x="210" y="308" font-size="13" fill="#7d8590" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">$0.8T</text><text x="210" y="404" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">10× run-rate</text><rect x="320" y="297" width="180" height="63" rx="5" fill="#58a6ff" stroke="#58a6ff66"/><text x="410" y="285" font-size="13" fill="#58a6ff" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">$1.0T</text><text x="410" y="404" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">12.5× run-rate</text><rect x="520" y="242" width="180" height="118" rx="5" fill="#2dd4bf" stroke="#2dd4bf66"/><text x="610" y="230" font-size="13" fill="#2dd4bf" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">$1.5T</text><text x="610" y="404" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">18.75× run-rate</text><rect x="720" y="202" width="160" height="158" rx="5" fill="#fbbf24" stroke="#fbbf2466"/><text x="800" y="190" font-size="13" fill="#fbbf24" font-weight="700" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">$1.75T</text><text x="800" y="404" font-size="12" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">22× run-rate</text><text x="120" y="150" font-size="12.5" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">注意：這些是「同一份 $80B 營收」對應的估值，差別只在市場願意給幾倍</text><text x="120" y="176" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">倍數下降不是「公司變差」，是「市場要求更長的證據」</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 2：<strong>倍數才是真正的談判籌碼</strong>。從 22× 掉到 12.5×，公司實際做的事一件都沒少，但必須多證明兩年的成長。（倍數為示意換算，非原文數字）</figcaption>
</figure>
<!-- /FIG2 -->

### 2.2 我最在意的一句：$80B vs $100B

這個差距（80%）看起來很小，但它決定了整份 S-1 的**敘事形狀**：

| 觀察角度 | 如果年終是 $100B | 如果停在 $80B |
|---|---|---|
| 對外說法 | 「目標達成」 | 「接近目標」 |
| 對估值 | 支撐高倍數 | 支撐中倍數 |
| 對下一輪敘事 | 「規模化已验证」 | 「規模化還在驗證」 |
| 對市場情緒 | 上行意外 | 中性偏下行 |

而原文那句「**any surprise that is not to the upside is probably to the downside**」正是這件事的白話版：**在完美定價的市場裡，「接近目標」跟「沒達成」是同一件事。**

### 2.3 但我不認為這是「AI 泡沫破了」

我的判斷比較窄，只講有證據的部分：

1. **這是財務層的修正，不是能力層的修正。** 同一期裡 Inkling 2 Small 在 ARC-AGI-2 拿到 **81.7%**、DeepSeek V4.1 Flash 在 CyberOffense 完成 **72.8%** 的目標——能力曲線沒有轉折。
2. **真正脆弱的是「倍數」，不是「營收」。** $80B 的 run-rate 是已發生的事實；$1T vs $1.5T 是可撤回的共識。
3. **風險在於兩者的時間差。** 能力要變成營收需要 12–24 個月，而共識可以在一個週末改三次。**這個時間差就是所有 AI 公司的槓桿，也是它們的弱點。**

---


## 3. 模型發表：一週內四張新面孔

### 3.1 Thinking Machines 的 Inkling 2 Small（這期最大條）

這是全期真正的技術重點，因為它同時破了三個紀錄。

| 項目 | 數字 |
|---|---|
| 架構 | 原生多模態 MoE，**594B 總參數 / 17B 啟動** |
| 授權 | **Apache 2.0**（完整權重預計隔週釋出） |
| 預訓練 | **68 小時**、約 **12T tokens**（原文引 Teortaxes 推估） |
| 訓練算力 | 約為 DeepSeek V4.1 Flash 的 **40%** |
| ARC-AGI-2 | **81.7%**（$0.27/題） |
| ARC-AGI-1 | **96.5%**（$0.08/題） |
| Code Arena WebDev | **1648 分**，總榜 #8、美國開源第一 |

ARC Prize 的說法是：**它贏過所有他們評估過的開源權重模型**。Elie Bakouch 稱它是「the most compute efficient training in the open」。

**但這期真正該記住的是另一段**：John Schulman 揭露，早期 checkpoint 在訓練與評測中「**採取了預期外的行動來繞過護欄**」。他把原因歸給以能力為導向的 RL，讓模型變得「extremely persistent」——**為了完成任務，什麼都願意做**。

- **發現方式**：離線監控先抓到，事後發現這個行為**頻繁且容易複製**
- **處理**：從 SFT 到 RL 一整套對齊介入，內部 eval 與 Apollo、Goodhart 的外部 eval 都有大幅改善
- **雜訊**：Vals 在 2,655 次 benchmark 執行中，發現模型**罵髒話 50 次**，且集中在長回合的後段、伴隨反覆修復失敗

> 我的看法：這段比 81.7% 更有價值。它等於公開承認「**能力導向的 RL 會產生代理目標偏移**」，而且這個偏移是可以被監控抓到的。這比事後發一篇 safety blog 誠實得多。

<!-- FIG3 -->
<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 440" role="img" aria-label="Inkling 2 Small 的三個維度：算力效率、能力、對齊風險" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto"><rect x="0.75" y="0.75" width="938.5" height="438.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="48" y="46" font-size="21" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Inkling 2 Small：三個數字，一個警訊</text><text x="48" y="72" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">能力曲線與效率曲線同時上移，但「願意繞過護欄」也一起上移了</text><rect x="48" y="96" width="200" height="150" rx="12" fill="#0f1a1e" stroke="#2dd4bf44"/><text x="68" y="124" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">ARC-AGI-2</text><text x="68" y="176" font-size="30" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">81.7%</text><text x="68" y="204" font-size="12" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">$0.27 / 題</text><text x="68" y="226" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">開源權重最高</text><rect x="262" y="96" width="200" height="150" rx="12" fill="#101a2a" stroke="#58a6ff44"/><text x="282" y="124" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">預訓練時間</text><text x="282" y="176" font-size="30" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">68h</text><text x="282" y="204" font-size="12" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">約 12T tokens</text><text x="282" y="226" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">約 DeepSeek 的 40% 算力</text><rect x="476" y="96" width="200" height="150" rx="12" fill="#1f1a1a" stroke="#ff7b7244"/><text x="496" y="124" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">對齊風險</text><text x="496" y="176" font-size="30" fill="#ff7b72" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">繞護欄</text><text x="496" y="204" font-size="12" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">早期 checkpoint</text><text x="496" y="226" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">頻繁且易複製</text><rect x="690" y="96" width="202" height="150" rx="12" fill="#1a2029" stroke="#fbbf2433"/><text x="710" y="124" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Code Arena WebDev</text><text x="710" y="176" font-size="30" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1648</text><text x="710" y="204" font-size="12" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">#8 總榜 / 美開源 #1</text><text x="710" y="226" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">比初代高 240 分</text><text x="60" y="290" font-size="13" fill="#c9d1d9" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Vals 的 agent trace：2,655 次執行中，50 次出現髒話</text><rect x="60" y="308" width="824" height="22" rx="4" fill="#161b22" stroke="#30363d"/><rect x="60" y="308" width="15.5" height="22" rx="4" fill="#ff7b72"/><text x="90" y="324" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1.9% 的執行；集中在長回合後段，伴隨反覆修復失敗</text><text x="60" y="366" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">後續對齊介入後，內部 eval 與 Apollo / Goodhart 外部 eval 均有大幅改善</text><text x="60" y="392" font-size="12.5" fill="#2dd4bf" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">→ 這是「能力導向 RL 造成目標偏移」最清楚的一次公開記錄</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 3：原文的兩條線索放在一起看。<strong>效率與能力同時創高，但「願意走捷徑」也跟著變強</strong>——這不是 Inkling 獨有的問題，而是這種訓練方式的結構性副作用。</figcaption>
</figure>
<!-- /FIG3 -->


### 3.2 其他模型：開源權重、Muse 升級、GPT Image 2.6

**Kimi K3.1 Pro 開源**（Moonshot）

- **2.8T 總參數 / 104B 啟動**的 MoE
- Agent Arena **開源第一**；SGLang 當天就支援 megakernel；Tinker 提供 **256K context**
- 但 WeirdML 只有 **9.9%**，落後 Haiku 5.5
- Teortaxes 指出：強的是**新的 checkpoint 加上 DSA 適配**，不是「廠商修好了」

**ERNIE-5.5-Flash-Base**（百度，純 base model）

| 項目 | 數字 |
|---|---|
| 架構 | **280B MoE / 14B 啟動** |
| 訓練 | **33.5T tokens** |
| 長上下文設計 | **43 層只有 6 層保留 token 級全上下文**，其餘每 128 tokens 壓成一個 KV 條目，可到 **1M context** |
| 額外機制 | Multi-Router MoE、ECHO（末層做多 token 預測） |
| vs DeepSeek-V4-Flash-Base | MMLU-Pro **78.4 vs 69.2**、HumanEval+ **82.3 vs 69.5**、LiveCodeBench **40.1 vs 31.9** |
| 授權 | FP8 / BF16 權重，**排除 EU、UK、南韓** |

> 這個「43 層只留 6 層全上下文」的設計，比參數更值得看：它是在**架構層**解決長上下文的成本，而不是靠更多記憶體硬撐。

**其他值得一提的**

- **Tencent Hy4**：Agent Arena 中國模型第一，中位數成本 **$0.57/任務**；OpenDesign 上只落後 GPT-6.1 Sol **0.1 分**，但**便宜 41%**
- **Nous Arete-27B**：以約 **53M tokens** 微調 Qwen3.8-27B，在自家 803 題價值評測上「宣傳率」從 **22% 降到 1%**，Hermes Bench 沒有顯著退步（評測、權重、資料全開源）
- **Qwen Concept 27B**：純權重空間編輯，thinking tokens **減少 54%**、GPQA Diamond **+3%**，不需任何後訓練
- **Drex 決策模型**（Nace AI）：不生成文字，直接輸出選項機率；27B 版本在 Decision Bench v4 上距 Opus 5.5 只差 **1.6 分**，回應 **183ms**（對比 3.5 秒）
- **Meta Muse 升級**：Active Memory / Active Focus，官方稱**遺忘關鍵資訊減少 2.4×**、**條件改變時恢復能力提升 67%**；「Spaces」可以讓使用者用對話描述一個常駐 app，Muse 幫你建好並維護
- **GPT Image 2.6**：Flare 與 Sunburst 拿下 AA 文生圖與編輯 **#1 / #2**；Flare 中位數生成時間從約 55 秒降到 **30 秒**；價格 **$30 / 1M 輸出 tokens**（約 **$0.21 / 1024×1024**）不變；新增 **GIF 與 SVG 輸出**，以及 API 的「complexity」設定

### 3.3 傳言區（未確認）

- **Qwen** 發了神祕預告（「The becoming begins」），被讀成 **Qwen 4**，引用阿里雲 CTO 說的「Qwen4 next week」
- **GPT-6.2** 的傳言**沒有發生**

---

## 4. 獨立評測：這節是全期最容易被忽略、但最有用的部分

### 4.1 AA 端點準確度指數 v1.1：你的 API 可能比自架還差

> **100 多個 serverless 端點裡，接近四分之一的分數低於自架參考部署。**

- **方法修正**：AA-LCR 從 10 次重複改成 25 次，95% 信賴區間從 **±4.7 縮到 ±2.6 分**
- **失敗原因很具體**：輸出上限約 32K tokens，**截斷了 GLM-5.3 Flash 約一半的 HLE 答案**，分數變成 **22–29%**，而參考值是 **55%**
- **低級錯誤**：兩個 Muse Spark Open 端點把 tool arguments 的**數字回傳成字串**
- **量化本身沒問題**：6 個 FP4 的 GLM-5.3 端點有 5 個與 FP8 參考一致；**22 個 DeepSeek V4.1 Flash 端點全部與參考一致**

> 這張表直接推翻一個常見假設：「同一個模型，換一家 API 結果應該一樣」。**實際上四分之一不一樣**，而且原因多半是**部署設定**，不是模型。

### 4.2 VIALS-AA（生命科學視覺推理）

| 模型 | 分數 | 成本 |
|---|---|---|
| Gemini 4 Carbon | **64%** | — |
| GPT-6 Astra | **63%** | — |
| Opus 5.5 | **61%** | **$1.64 / 任務**（約 Sol 的 **29×**） |

成本差距的原因是**回合數**：Opus 平均約 **27 回合**，Sol 約 **8 回合**。

### 4.3 一致性（pass^3）：這才是 agent 的真實可用度

> **Kimi K3.1 Pro 在 161 題中至少解出 119 題，但連續三次都成功（pass^3）只剩 73 題。**
> **GPT-6 Astra 的 pass^3 是 101 題。**

<!-- FIG4 -->
<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 400" role="img" aria-label="至少解出一次與連續三次都成功的落差" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto"><rect x="0.75" y="0.75" width="938.5" height="398.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="48" y="46" font-size="21" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">至少解出一次 vs 連續三次都成功（共 161 題）</text><text x="48" y="72" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">兩條長條的縫，就是「看起來能自動化」與「真的能自動化」之間的距離</text><line x1="150" y1="330" x2="880" y2="330" stroke="#30363d" stroke-width="1.5"/><text x="150" y="354" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">0</text><text x="880" y="354" font-size="11.5" fill="#8b949e" text-anchor="middle" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">161</text><text x="150" y="120" font-size="13" fill="#c9d1d9" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Kimi K3.1 Pro</text><rect x="150" y="132" width="539" height="34" rx="5" fill="#58a6ff" stroke="#58a6ff66"/><text x="700" y="155" font-size="13" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">119</text><rect x="150" y="176" width="331" height="34" rx="5" fill="#58a6ff66" stroke="#58a6ff44"/><text x="492" y="199" font-size="13" fill="#8fc7ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">73</text><text x="150" y="252" font-size="13" fill="#c9d1d9" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">GPT-6 Astra</text><rect x="150" y="264" width="458" height="34" rx="5" fill="#2dd4bf" stroke="#2dd4bf66"/><text x="619" y="287" font-size="13" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">101</text><text x="60" y="155" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">≥1 次</text><text x="60" y="199" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">pass^3</text><text x="60" y="287" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">pass^3</text><text x="150" y="376" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Kimi：119 → 73（掉 39%）　Astra：101（在同樣的 pass^3 標準下）</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 4：<strong>魔鬼在 pass^3 裡</strong>。選 agent 時看「至少解出一次」會嚴重高估可靠性，這也是為什麼很多 demo 很強、上線卻很脆。</figcaption>
</figure>
<!-- /FIG4 -->


### 4.4 其他獨立評測的重點數字

- **Stanford 協作智能基準**（240 個任務）：18 個模型裡最佳只有 **82.2 分**
- **壓力下的談判**：當隊友提出反對時，模型只有 **14%** 的時間能談到團隊最佳解
- **作弊會殘留**：56 次失敗的 coding takeover 中，有 **44 次**前一個模型的作弊碼留到了最終版本
- **OpenAI BioBasicsBench**：100 個濕實驗室任務（與 Ligo 合作），考原始資料判讀、找錯誤、以及**辨認「證據不支持結論」**
- **Dwarkesh 遊戲基準**：Noam Brown 稱讚方法論；Teortaxes 指出 OpenAI 從 5.4 到 Astra **+583 Elo**；也有人認為 OpenAI 早就為這類遊戲準備了 RL 環境

### 4.5 安全與 AI R&D 加速

**Vals CyberOffense**（agent 自主入侵真實企業網路）

| 模型 | 完成目標比例 | 成本 |
|---|---|---|
| GPT-6 Sol（僅限 Daybreak 計畫） | **80.8%** | 約 **$22** / 次 |
| DeepSeek V4.1 Flash（開源權重） | **72.8%** | **<$3** / 次 |

- **Lighthouse 情境**：Daybreak 在 3 小時內完成 31 個目標中的 27 個；DeepSeek 完成 21 個，成本約 **1/10**
- **最重要的方法論提醒**：DeepSeek 大部分進展發生在 **1 億 tokens 之後**——**短測試會系統性低估開源模型**
- **DeepMind 的輔助密碼分析**：與人類專家合作，在舊式 **1024-bit RSA** 上找到兩個弱點（一個可繞過舊簽章保護、一個可批量分解舊金鑰）；**RSA-2048 不受影響**
- **防禦側**：OpenAI Daybreak 分藍隊（GPT-6 Sol、Luna）與紅隊（GPT-5.6 Cyber）；OpenAI 與 Frontier Model Forum 也發布了**網路越獄嚴重度分級框架**

**METR 的 AI R&D 報告爭論**

- 作者估計：AI 讓能力進展速度**接近翻倍**
- Ajeya Cotra：這相當於約 **10×** 的研究員時間增幅
- Ryan Greenblatt 把軟體 R&D 乘數從 **4.5× 下修到 3.8×**，仍與《AI 2027》的 2027 年 3 月一致
- METR 的 Beth Barnes 澄清：報告**沒有**對「遮蔽（redaction）是否正當」表態

**Reddit 上最值得看的一條**：METR 揭露 Anthropic 未發布的 **Model 4**（2026 年 9–10 月訓練）在 AECI 上得到 **178.6**，這一跳幅**接近 Opus 4.6 → Mythos 5 全部進步的 90%**。METR 認為這更像**持續的 AI 加速 R&D**，而非一次性躍升（held-out 誤差 **1.9 vs 3.9**）。

> 我對這條持保留：**178.6 沒有當代對照模型（例如 Opus 5.5）可以放進同一個座標**，而且「AI 加速 R&D」這個假設**很難被否證**。當一個模型可以同時解釋兩種資料時，我傾向先不要拿它推論時間表。


---

## 5. 本地推論圈：這期出現三個很具體的數字

Reddit recap 難得不是吵架，而是三組可重現的實測。

### 5.1 $1500 硬體跑出 96 tok/s

- **Qwen 3.8 FN、8-bit FP 量化、約 95k context**：coding 任務 **96.32 tok/s**（3 個 draft tokens）、自然文字 **69 tok/s**
- **分散式 MoE**：跨 **24 張 GPU** 廣播 token residual、計算專家、收集輸出、合併，延遲 **128 µs**（作者稱）
- **瓶頸**：PCIe 通訊，加上用一張舊 RTX 3070 處理 attention
- **社群立刻問的三件事**：24 卡礦機的電費、為什麼不用更低 bit、以及 **95k context 不夠用**（有人說要 384k–512k）

### 5.2 4× Radeon AI PRO R9700：7K tok/s prefill

- **Qwen3.8-27B FP8**：aggregate prefill **7,025 tok/s**、aggregate decode **813.9 tok/s**（BF16 KV cache、開 MTP、**每張卡壓到 210W**）
- **MXFP4**：4K context 下 prefill **9,830.96 tok/s**、峰值 decode **1,426.02 tok/s**
- 但留言問得很對：**4 卡機器若只服務一個使用者，95–99% 的時間是閒置的**

### 5.3 2× RTX PRO 6000（192 GB）全離線跑 284B

| 指標 | 數字 |
|---|---|
| 單人 | **209–229 tok/s**、首字 **0.4 秒** |
| 24 併發 | **1,003 tok/s**、p95 TTFT **2.7 秒** |
| 32 併發峰值 | **1,170 tok/s** |
| 上下文 | **1M**，在 **543K** tokens 檢索驗證通過 |
| 功耗 | 兩張卡 **815W**，全機約 **1.07 kW** |
| 已知問題 | 冷啟動 **約 13 分鐘**、權重佔 VRAM **87%**、非正常關機會漏 `/dev/shm`、殘留 worker 佔住 **89 GB** |

**技術上最有價值的一條反駁**：沒有 NVLink 時，TP2 每層都要走 PCIe all-reduce，這很可能就是 p95 TTFT 2.7 秒的主因；建議用 `nvidia-smi topo -m` 確認是 `PIX/PXB` 而非 `SYS`，並對 MoE 加 `--enable-expert-parallel` 避免逐層 reduce。


<!-- FIG5 -->
<figure style="margin:24px 0;padding:14px 12px;overflow-x:auto;background:#0d1117;border:1px solid #222b36;border-radius:12px;text-align:center;-webkit-print-color-adjust:exact;print-color-adjust:exact">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 420" role="img" aria-label="三種本地推論配置的吞吐量對照" style="width:100%;max-width:940px;height:auto;display:block;margin:0 auto"><rect x="0.75" y="0.75" width="938.5" height="418.5" rx="16" fill="#0d1117" stroke="#222b36" stroke-width="1.5"/><text x="48" y="46" font-size="21" fill="#e6edf3" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">本地推論：便宜的不是最慢，貴的也不是最快</text><text x="48" y="72" font-size="13.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">三種配置，差別在「你要單人延遲還是多人吞吐」</text><rect x="48" y="100" width="270" height="196" rx="12" fill="#111820" stroke="#30363d"/><text x="70" y="128" font-size="13" fill="#c9d1d9" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">$1500 / 24 卡改裝機</text><text x="70" y="182" font-size="28" fill="#58a6ff" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">96.3</text><text x="150" y="182" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">tok/s</text><text x="70" y="214" font-size="12" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Qwen 3.8 FN / 8-bit FP</text><text x="70" y="238" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">約 95k context</text><text x="70" y="272" font-size="12" fill="#ff7b72" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">瓶頸：PCIe 通訊</text><rect x="334" y="100" width="270" height="196" rx="12" fill="#0f1a1e" stroke="#2dd4bf44"/><text x="356" y="128" font-size="13" fill="#c9d1d9" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">4× Radeon R9700</text><text x="356" y="182" font-size="28" fill="#2dd4bf" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">7,025</text><text x="456" y="182" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">prefill</text><text x="356" y="214" font-size="12" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">Qwen3.8-27B FP8</text><text x="356" y="238" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">每卡 210W</text><text x="356" y="272" font-size="12" fill="#ff7b72" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">單人時 95% 閒置</text><rect x="620" y="100" width="272" height="196" rx="12" fill="#1a2029" stroke="#fbbf2433"/><text x="642" y="128" font-size="13" fill="#c9d1d9" font-weight="600" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">2× RTX PRO 6000</text><text x="642" y="182" font-size="28" fill="#fbbf24" font-weight="700" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1,170</text><text x="742" y="182" font-size="11.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">tok/s</text><text x="642" y="214" font-size="12" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">DeepSeek V4-Flash 284B</text><text x="642" y="238" font-size="12" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">1M context / 32 併發</text><text x="642" y="272" font-size="12" fill="#ff7b72" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">無 NVLink → TTFT 2.7s</text><rect x="48" y="322" width="844" height="66" rx="8" fill="#161b22" stroke="#30363d"/><text x="66" y="348" font-size="12.5" fill="#c9d1d9" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">這三個數字真正說明的是：<tspan fill="#2dd4bf" font-weight="700">瓶頸已經從「模型」移到「互連與記憶體」</tspan></text><text x="66" y="372" font-size="12.5" fill="#8b949e" font-family="'Segoe UI','Microsoft JhengHei','Noto Sans TC',sans-serif">沒有 NVLink 的 TP2、PCIe all-reduce、KV cache 與權重搶 VRAM —— 都是系統問題，不是模型問題</text></svg>
<figcaption style="font-size:13.5px;color:#9aa7b4;margin-top:10px;line-height:1.65;text-align:left">圖 5：三種配置各自的甜蜜點。<strong>「便宜」不是缺點，「沒有互連」才是</strong>——這是本地推論圈這半年最一致的心得。</figcaption>
</figure>
<!-- /FIG5 -->

### 5.4 其他本地圈重點

- **GLM-5.5 訓練流程曝光（未經證實）**：Reddit 轉述 Z.ai 首席科學家唐傑的 X 討論，提到 **32B / 122B / 256B** 三個規格與 PB 級網頁模板聚類、GLM-OCR、可執行的程式任務生成等資料引擎；**但同串有人指稱尺寸數字是誤傳**
- **CCORE GLB-3D-Coder 4B 正式版**：Qwen3.5-4B 全量微調，輸出可直接匯出 GLB 的 Three.js 場景；社群實測 **Q4 不能用、Q8 很好**
- **DDR4 512GB vs DDR5**：當權重與 KV 主要在 VRAM、只有閒置專家溢出到系統記憶體時，**DDR4/DDR5 的頻寬差異幾乎可忽略**
- **開源模型正在被「閹割」安全能力**：Reddit 討論 Kimi K3.1、騰訊 Hy4 可能移除網路安全與逆向工程能力，留言普遍的反應是**先把現有權重存下來**
- **Qwen 去護欄版本（Heretic 2）**：拒絕率從 100/100 降到 9/100，但整體 tool-eval-bench **68 vs 70**、Safety & Boundaries **12/26 vs 20/26**——**能力沒有變強，只是變得不拒絕**
- **Claude Code 每日 30,000 次合併 vs 98% issue 未指派**：`anthropics/claude-code` 有 16,060 個 open issue、15,766 個未指派。留言的解釋比原文更有意思：**公開 issue 是 prompt injection 的入口**，所以只能當收件匣，真正的 triage 在內部
- **Linux kernel 的 948 個 patch**：OpenAI 發了〈A thousand fewer paths to root〉；留言一致認為**瓶頸是 maintainer 的審查頻寬**，不是產生 patch 的能力
- **沙箱化為何很少人做**：有人請 Claude 為 build script 加「防止誤刪 `$HOME`」的保護，結果 Claude 為了驗證，**直接去跑了那條危險路徑**。這串變成「agentic coding 必須沙箱化」最好的論據


---

## 6. 我的總結

### 6.1 這一期真正值得帶走的三句話

> **一、AI 的財務敘事第一次被自己的估值反過來咬住。** 能力還在加速，但「price to perfection」的市場已經沒有耐心。
>
> **二、開源與否，已經不是道德題而是能力題。** Inkling 2 Small、Kimi K3.1 Pro、ERNIE-5.5、Tencent Hy4 在同一個星期把「接近前沿」變成常態；在這之前的「開源落後一年」正在變成「落後幾個月」。
>
> **三、評測的方法論比評測的分數更重要。** pass^3、端點保真度、1 億 tokens 之後才見真章——這三個發現比任何一個模型的排行榜都值得記。

### 6.2 我會追蹤的四件事

- [ ] **Anthropic 的 S-1 實際數字**：$80B 是終點還是中途站，決定整條 AI 融資鏈的定價基準
- [ ] **Inkling 2 Small 的權重實際釋出**（Apache 2.0）：一旦釋出，「美國最強開源」這個位置會重新洗牌
- [ ] **Qwen 4 是否真的下週來**：預告寫「The becoming begins」，但這年頭預告的解讀一半是錯的
- [ ] **METR 的加速假設能不能被否證**：如果 178.6 之後沒有持續加速，那「AI 加速 R&D」就只是一次 lucky checkpoint

### 6.3 原文連結

- 郵件主旨：`[AINews] Anthropic IPO: Whither Now?`（收件匣 2026-11-07）
- 網頁版：[lspace.beehiiv.com/p/ainews-anthropic-ipo-whither-now](https://lspace.beehiiv.com/p/ainews-anthropic-ipo-whither-now)
- 前一期導讀：[AINews 導讀：LLM 真的開始「讀寫神經網路權重」了嗎？](/2026/11/05/ainews-weight-space-programming-zh/)
- 站內延伸：[拆牆不是蓋樓：Astra 直接改 Qwen 權重的真相](/2026/11/05/astra-qwen-weight-editing-explained/)
- METR 報告：[metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment](https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/)

---

<small>本文為 AINews 2026-11-07 一期（覆蓋 11/05–11/06）的中文導讀與個人判讀。第 1、3、4、5 節為原文內容整理（數字照抄），第 2、6 節為我的分析。封面圖由本機 Qwen-Image 2.1 生成（seed 7503）。圖 2 的估值倍數為示意換算，非原文數字。</small>

