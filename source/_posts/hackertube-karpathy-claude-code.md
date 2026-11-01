---
title: Karpathy 週末兩小時：抱怨 YouTube 推薦爛，就叫 Opus 5.5 做了個 HackerTube
date: 2026-11-02 01:20:00
categories:
  - AI Agent
tags:
  - Andrej Karpathy
  - HackerTube
  - Claude Code
  - Opus 5.5
  - Sonnet
  - Hacker News
  - Workflow
  - Vibe Coding
  - VPS 部署
  - 事實查核
toc: true
index_img: /img/covers/hackertube-karpathy-claude-code.png
banner_img: /img/covers/hackertube-karpathy-claude-code.png
---

> <strong>整理說明</strong>：本篇導讀自 Andrej Karpathy 於 2026-10-31 在自己部落格發表的〈[HackerTube](https://karpathy.bearblog.dev/hacker-tube/)〉，並以他在 Hacker News 討論串的補充留言、以及 Piotr Sobolewski 的〈[HackerTube: Karpathy built a YouTube alternative with Claude in 2 hours](https://sobolewski.pro/en/blog/hackertube-karpathy-claude-code)〉交叉補齊細節。**第 1～5 節為原文與討論串的內容整理**；**第 6 節之後（我的補充、不能照抄的地方）是我自己的看法**，兩種內容分開標註。引號內的英文皆為原文。整理日期 2026-11-02。

## 一句話總結

> **他抱怨的不是 YouTube 的內容，是「推薦」——於是他把推薦換掉了，底下那套播放器根本沒換。**

Karpathy 星期六早上跟 Opus 5.5 說了一句話：用 Hacker News 上被推薦過的影片，做一個我們自己的 YouTube。兩小時後 [hackertube.org](https://hackertube.org) 上線，內含 **6,454 支影片、150 個主題、2007–2026 年**。而整個過程他沒有讀一行 code、沒有下過一行終端指令。

---

## 1. 起點：週五晚上 11 點的那面牆

原文開頭的情境寫得很直白——不是技術問題，是疲勞加上失望：

> "It was Friday night at 11pm, I was tired, I went to YouTube to watch something and realized that I was looking at an **enshittified wall of slop**. Insanely exaggerated thumbnails, dumb recommendations of the same tired topics, truly terrible idiocracy-grade content. I'm sure this algorithm works well for the median person on the internet, but it definitely does not work for me."

（週五晚上 11 點，我累了，想看點東西，結果發現自己盯著一面被搞爛的垃圾牆。誇張到爆的縮圖、同樣那幾個無聊主題的爛推薦、真正低能級數的內容。我確信這套演算法對網路上的中位數使用者很有效，但對我完全沒用。）

他接著寫：「So this morning (Saturday) I took a hold of my Opus 5.5 and gave it the task」——星期五晚上的怒氣，星期六早上交給模型處理。

## 2. 他到底叫 AI 做了什麼

這一步是整個專案最容易被摘要漏掉、但技術含量最高的地方。不是「做個影片網站」，而是**先把資料挖出來、洗乾淨，再做介面**：

| 步驟 | 誰做的 | 內容 |
|---|---|---|
| ① 取資料 | Claude | 下載 **Hacker News 全部留言**的資料集（來自 Hugging Face） |
| ② 過濾 | Claude ＋ **Sonnet** | 在 **Workflow**（Claude Code 的功能）裡跑 Sonnet，濾掉 spam |
| ③ 收斂 | Claude | 最後留下**約 40,000 則**「推薦 YouTube 影片」的留言 |
| ④ 產出清單 | Claude | 對應出 **6,454 支影片**，跨 2007–2026、**150 個主題** |
| ⑤ 做介面 | Opus 5.5 | 套上 YouTube 式 UI |
| ⑥ 上線 | Opus 5.5 | 買網域、推上 VPS、secure／harden／optimize |

原文的句子是：

> "Opus downloaded all comments of HackerNews, filtered them, ran Sonnet over them in a Workflow (Claude Code feature), got rid of spam, and narrowed everything down to 40K comments recommending a YouTube video."

注意這裡的**雙模型分工**：Opus 5.5 是發號施令、寫程式、做架構的那個，**Sonnet 是被派去做幾萬則留言批次分類的打工人**。幾萬筆文本分類的 token 量不該用最貴的模型跑，這是一個很實際的成本判斷。

## 3. 網站實際做了什麼

原文列的六項功能，每一項都對應一個「YouTube 讓他不爽的點」：

| 功能 | 對應的痛點 |
|---|---|
| 內容來源是 HN 推薦，不是演算法 | 推薦的不是「最多人看」，是「懂的人願意貼出來」 |
| **用影片第 50% 位置的畫面當縮圖**，不用上傳的縮圖 | 直接消滅誇張縮圖 clickbait |
| **不用註冊帳號**的 For You 推薦，狀態存在瀏覽器 local session | 不必登入才能被推薦，也不必被追蹤 |
| **鍵盤快捷鍵** | 重度使用者的基本盤 |
| **Longs**（長片）篩選 | 把「想認真看點東西」跟「打發時間」分開 |
| **資料匯出**，可以丟給自己的 AI agent 複製一份 | 把成品當成 seed，而不是當成產品 |

其中「50% thumbnail」我認為是整個設計裡最聰明的一招：它不是用更好的演算法猜你喜歡什麼，而是**直接把創作者用來騙點擊的那張圖拿掉**。成本極低，效果直接。

另外每部影片都會顯示**當初推薦它的那則 HN 留言**——也就是說，「為什麼這支影片在這裡」是有出處的，不是黑箱。

## 4. 他的工作流設定（原文 EDIT 段）

原文在發文後補了一段「EDIT」，把流程講得更清楚。這是你摘要裡列的內容，我照原文校對一次：

- **工具**：Claude Code，Mac 桌面版
- **預設模型**：Opus 5.5，**effort 設在 Medium**
- **互動方式**：已經不做任何「傳統工程」的事了

> "I don't actually do anything resembling traditional engineering anymore (read/write code, run commands in a terminal, or etc.), I only talk to Claude and have it do everything."

**他自己動手的只有三件事：**

1. 到 Google Cloud 介面申請一組 **API key**，用來查詢 YouTube 影片的 metadata
2. 開一台 **VPS**
3. 買 **Domain name**（HN 留言補充：還設了 DNS record）

**然後這一句是重點：**

> "Once the box was up I gave Claude the IP and told it update, deploy, secure, harden and optimize the code, and it did the whole thing."

給了 IP，講了五個動詞（update、deploy、secure、harden、optimize），剩下的它自己做。

還有一句很人味的補充，說明他不是「按下按鈕就去看 Netflix」：

> "I worked on this in between Claude's actual work so it still feels a little bit like team work :)"

## 5. 討論串裡他才講的那些事

原文沒有、但在 HN 留言裡他自己補的，我覺得比原文更有訊息量：

1. **他的 prompt 越寫越短、越寫越「笨」**——因為模型反正聽得懂他要什麼。
2. 有時候只打一句 **"check recent cyber stuff"**，Claude 就自己開好幾個 **subagent** 去查。
3. 但他強調：**只有 Opus 5.5 及更新的模型他才敢這樣放手**。他的說法是「The thing is beast mode」。
4. 討論串進行中他還在邊聊邊加功能，例如加上用 **Filter 依日期排序**。

第 3 點值得單獨畫線：**「prompt 可以很懶」不是模型變強的自動結果，是他判斷「這個模型可以懶」之後的選擇。** 這兩件事常被混為一談。

---

## 6. 我的補充：三個不能照抄的結論

### 6.1 這不是「AI 兩小時做一個網站」，是「他把資料工程也外包了」

大部分人看到這則新聞，注意到的都是 UI 跟部署。但真正讓這個專案成立的是**第 2 節那條資料管線**：下載全量 HN 留言 → 跑 Sonnet 分類 → 收斂出 40K 則有效留言 → 對應出 6,454 支影片。

沒有這條管線，你做出來的只是一個「影片播放器外殼」，裡面沒有東西。而一般人在這裡卡住的機率，遠高於卡在刻 UI。

反過來說，這也解釋了為什麼他能兩小時做完：**HN 的留言資料集本來就是公開的、結構化的、而且他真的懂那個社群在討論什麼。** 換一個「資料要自己從零爬、還要處理 anti-bot」的題目，兩小時這個數字就不成立了。

### 6.2 「兩小時」是壓縮後的結果，不是全程

他自己在原文寫的是 "This takes ~2 hours now"——注意那個 **now**。這是他在已經很熟這套工具、很清楚自己要什麼的前提下，一次做完的時間。文章沒有公布 token 消耗量，而 Claude Code 在資料處理與多輪 debug 上的 token 燒法並不直覺。

對照組是 HN 討論串裡其他人的經驗：不少人說自己的 agent 會**做到一半就放棄、或前後自相矛盾**，懷疑自己兩小時做不出來。這個對比才是這則新聞真正的資訊。

### 6.3 兩個現實風險（跟技術無關）

| 風險 | 說明 |
|---|---|
| **YouTube ToS** | 討論串有人提到 Google 曾讓類似專案下線。HackerTube 用的是 embed 播放器，廣告還是會回到創作者身上，但風險仍在 |
| **利益揭露** | Karpathy 自 2026 年 5 月起在 Anthropic 的 pretraining 團隊工作。他誇 Claude Code，等於在誇自家公司的產品——這不影響技術觀察的價值，但讀的時候要知道 |

## 7. 如果我要照著做一次，我會抄哪幾件事

不是抄「兩小時」這個數字，是抄下面這四個決策：

1. **用「有出處的策展」取代「演算法推薦」**——HN 留言就是天然的 upvote 加理由。
2. **雙模型分層**：貴的模型做決策與架構，便宜的模型做大量批次分類。
3. **把「騙點擊的那一層」直接刪掉**（50% 縮圖），而不是想辦法去修正它。
4. **成品要能匯出**，讓別人（或別的 agent）能拿去當起點。

> **一句話收尾**：他真正討厭的是推薦，不是 YouTube。所以他把推薦換掉了——而換掉推薦所需要的，剛好是一條資料管線，不是一個更好的播放器。

---

## 參考資料

| 來源 | 連結 |
|---|---|
| 原文（Karpathy 部落格） | <https://karpathy.bearblog.dev/hacker-tube/> |
| HackerTube 本體 | <https://hackertube.org> |
| 背景補齊（Piotr Sobolewski） | <https://sobolewski.pro/en/blog/hackertube-karpathy-claude-code> |
