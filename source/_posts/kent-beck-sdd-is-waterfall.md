---
title: Spec-Driven Development 就是瀑布？——Kent Beck 的 AI 時代九個不中聽真相
date: 2026-10-08 20:00:00
categories:
  - 軟體工程
tags:
  - Kent Beck
  - Spec-Driven Development
  - SDD
  - 敏捷
  - AI Agent
  - 瀑布模型
  - 軟體工藝
  - 度量
toc: true
index_img: https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200
banner_img: https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1600
---

> <strong>整理說明</strong>：本文將敏捷三叔公（David Ko）整理的 [Kent Beck 演講筆記](https://agile3uncles.com/2026/10/06/sdd-is-waterfall-kent-becks-9-hard-truths/) 重新排版成更有結構性的版本。原始演講為 Kent Beck《Software Engineering in the Age of AI》（Prodacity 2026），[演講影片](https://www.youtube.com/watch?v=F8fBgDCf2Y4)。內容版權屬原作者所有，此為學習整理用途。

<!-- more -->

## 一句話總結

> AI（Beck 稱之為「<strong>精靈 genie</strong>」）大幅降低了「<strong>產出程式碼</strong>」的成本，但<strong>沒有</strong>降低「做出能運作、能持續演進的軟體」的難度。<strong>工藝（craft）</strong>沒有消失，而是從「程式碼層級的細節講究」，轉移到「在<strong>功能（features）</strong>與<strong>未來性（futures）</strong>之間節奏性取捨」的能力。

這場演講的獨特價值，在於不站在「AI 無用」或「AI 取代一切」任一極端，而是把問題重新框定為一個<strong>節奏問題</strong>：精靈讓功能產出的速度遠超過人類蒐集與消化回饋的速度，風險不在工具本身，而在「全速前進的誘惑」。

---

## 講者背景

（Beck 應 Gene Kim 要求這樣自我介紹）

- 將<strong>設計模式（patterns）</strong>引入軟體開發
- 發明<strong>程式設計師測試（programmer testing）</strong>與 <strong>JUnit</strong>（與 Erich Gamma 共同完善）
- 重新發現並精煉<strong>測試驅動開發（TDD）</strong>——他引用一本 1957 年的書，裡面已提到「向使用者要輸入/輸出配對，確保程式符合」，所以他說自己不是發明者
- <strong>極限編程（XP, Extreme Programming）</strong>的創造者
- <strong>敏捷宣言（Agile Manifesto）</strong>第一位簽署人（依字母排序）
- 目前在一家<strong>前沿實驗室（frontier lab）</strong>——訓練最先進大型模型的公司——協助團隊設計工作方式，並重返每日寫程式約 18 個月

---

## 九個不中聽真相

### 真相 1：精靈很會寫「看起來能動」的程式，而不是能動的程式

他刻意用 <strong>genie（精靈）</strong>而非 AI：精靈實現你的願望，但結果總偏離真正的意圖——這是人與 AI 協作的本質關係：提出請求、得到看起來很酷的東西、最後有點失望。

他直接說「AI 已經比人類會寫程式」是<strong>胡說（balderdash）</strong>：

- 能產出語法正確、<strong>看起來可信（plausible）</strong>的程式，不等於程式真的能運作
- 精靈非常擅長 `plausible`，但不擅長 `actually working`
- 舉例：花一萬美元 token 產出的「C 編譯器」，細看連 hello world 都跑不動，或修一個 bug 冒出三個——它是「C 編譯器-ish」，不是 C 編譯器

<strong>結論</strong>：只要生產過程有大量 AI 參與，程式設計師、管理者、採購者都必須採取<strong>對抗式（adversarial）、懷疑式（cynical）</strong>的立場。

> 「你說它能動——是你自己滿意了，還是我滿意了？我要推多用力才能確認？」

<strong>為什麼以前可以信任、現在不行</strong>：資深工程師有一套手法讓程式<strong>在建構上就正確（correct by construction）</strong>，或讓某一類 bug 在設計上根本不可能發生（例如用型別系統排除非法狀態）。看到這種設計，你可以推論「這類問題不會出現」。精靈沒有這些手法，所以過去那種「從結構推論可信度」的捷徑失效了。

### 真相 2：「不再需要程式設計師」這句話，COBOL 時代就講過了

每一輪技術進步都有人說：商業人員只要用自然語言描述需求、電腦就能自動完成。他指出這正是 <strong>COBOL</strong> 當年的賣點（COBOL 設計得像英文句子，目標就是讓非程式設計師能寫）。

作為程式設計師，值得從策略層面思考「為什麼大家一直想擺脫我們」；但從結果看，這從來沒成真，因為程式本質上是高度技術性的產物。他不擔心飯碗的另一個原因：年輕工程師犯的錯從羅馬時代至今都一樣，<strong>教練的角色不會消失</strong>。

### 真相 3：他自己寫的三本工藝書，現在都該丟掉

Beck 寫過至少三本可歸類為「工藝導向」的書，他說這三本現在都該丟掉——職涯末期有這種感覺很奇怪，但事實如此。

| 角度 | 說明 |
|---|---|
| <strong>過時的部分</strong> | 命名、把邏輯拆成能組合的小片段、縮排、空白的運用、為人類理解而優化程式結構。這些決策以前有很高的<strong>槓桿（leverage）</strong>（特別是「五年後有人打開這段程式碼，慶幸自己看得懂」那種長期槓桿），現在槓桿大幅降低 |
| <strong>但不是歸零</strong> | 如果要選，他仍然要人類看得懂的系統；只是「理解」會發生在有精靈幫忙解釋的脈絡裡（前提是它沒在說謊，而說謊永遠是選項之一） |
| <strong>他原本就反感的部分</strong> | `craft` 這個詞曾被軟體工藝運動的一部分人挾持，變成「躲在洞穴裡、慢慢雕琢到我覺得完成為止」的藉口。他強烈反對「程式設計師的體驗比時間更重要」 |

他坦承失去的是那種「inline 這個、extract 那個、rename 一下，啊，全部清楚了」的個人滿足感——那個時刻現在沒有回饋了。

<strong>判準是延遲成本（cost of delay）</strong>：延遲成本高時，一個醜但能給你回饋的程式才是對的；延遲成本低、軟體要活 20 年時，瑞士鐘錶匠式的精雕細琢才划算。

<strong>新的意義</strong>：craft 仍是有效的紀律與關切，只是表現形式會完全不同——不再是程式碼細節，而是下一節的<strong>節奏控制</strong>。

### 真相 4：以前一百人十年才能把專案搞到沒救，現在一個人一週就夠

全場最重要的一張圖：<strong>Features vs. Futures（功能 vs. 未來性）</strong>。他原本想用 `optionality`（選擇權）這個詞，後來改用 `futures` 是為了和 `features` 押韻。

<strong>概念說明</strong>：`futures` 指的是「這個軟體接下來還能往哪些方向改」的所有可能性，可理解為金融上的<strong>選擇權（options）</strong>——你不一定會行使，但擁有選擇本身就有價值。

專案的軌跡：

```text
專案起點：很多可能性（futures），零功能（features）
   ↓ 每實作一個功能，都會燒掉一些未來性
   ↓ 至少你得維持向下相容，這限制了下一步能做什麼
   ↓ 或你發現第一個功能做錯了要拆掉，也會限制後續選擇
絕對零度：動任何東西都會壞別的東西（不可修改狀態）
```

諷刺的觀察：以前要一百人花十年才能把專案搞到不可修改，<strong>現在一個人一週用 AI 就能做到</strong>——「這是把專案推向不可修改狀態的巨大生產力提升」。

<strong>替代路徑</strong>：每完成一個功能、精靈比著手指槍問「老闆，接下來做什麼？」的那一刻，就是機會。他引用 Pablo Casals 的故事（他承認是杜撰的，但太好用了）：被問「拉那麼多十六分音符不累嗎？」回答「<strong>我在音符之間休息。</strong>」

在那個「音符之間」，可以：重構、消除重複、提升可讀性、甚至整個丟掉用不同方式重做——把未來性加回來，甚至比原來更多，然後才進下一個功能。

<strong>經濟論證</strong>：專案的經濟價值 = 現有功能的總和 + <strong>所有未來可選項的價值</strong>。所以增加 futures 也是在增加價值，只是看不見。

<strong>為什麼難以推動</strong>：加功能是<strong>可見的、可辨識的（legible）</strong>——他借用 James C. Scott《Seeing Like a State》的概念，指組織只能看見、度量、管理那些被標準化呈現的東西。功能人人看得到、使用者想要、交付了大家說謝謝；未來性則難以入帳，看起來像<strong>畫蛇添足（gilding the lily）</strong>。

> 「軟體完成了、我不想再改它」對他而言是失敗；他想寫的是能激發無數新想法的軟體。

> 「你不能一邊切菜一邊擦刀，但你一定要擦刀」——專業廚房已經演化出這套節奏。

退遠看，軌跡像是功能和選項同時增加；但實作上必須<strong>交替進行</strong>——想同時最大化兩者，問題大到連人加精靈的腦容量都裝不下。

### 真相 5：全自主的「黑暗工廠」一定出軌，而且出軌的過程很精彩

<strong>黑暗軟體工廠（dark software factory）</strong>：借自製造業的<strong>熄燈工廠（lights-out factory）</strong>，指完全無人介入、全自動運作的工廠。這裡的「dark」不是邪惡（他說本來還滿期待終於能寫邪惡軟體），是<strong>沒有人、沒有回饋</strong>。

- 他每次嘗試<strong>完全代理式（fully agentic）</strong>開發都會失控——而且失控過程很精彩、產出量驚人，讓你驚呼「你怎麼做到這麼多」，但結果仍是垃圾
- <strong>放慢節奏才有機會形成理解</strong>（現場聽眾補充、他表示完全同意）
- 最好的軟體是「以<strong>最大化學習</strong>為目標，軟體只是<strong>副產品（side effect）</strong>」；反過來「以產出軟體為目標、偶爾因為搞砸而學到東西」的習慣與節奏完全不同
- 黑暗工廠唯一學到的是精靈有多不可靠，而這我們本來就知道

<strong>Ward Cunningham 關機的故事</strong>：Ward 是 Wiki 的發明人、Beck 畢業後的導師，他說這是人生最大的運氣。兩人花一下午寫出「大概能動但感覺怪怪的」程式碼，Ward 直接伸手關機；Beck 氣沖沖回家，隔天早上 15 分鐘重寫完畢，清晰且完全理解——那是他的頓悟時刻：<strong>這是一個學習過程，軟體是副產品。</strong>

### 真相 6：Spec-Driven Development 就是瀑布，而且 Royce 當年就說過行不通

| | 一次成形（one-shot） | 迭代（iterative） |
|---|---|---|
| <strong>做法</strong> | 我寫一份規格，精靈產出軟體，規格夠好軟體就夠好；不夠好？那把規格寫得更大更複雜 | 軟體部署在真實世界產生價值 → 改 → 更多價值 → 再改 |

他直言<strong>規格驅動開發（spec-driven development, SDD）就是瀑布式開發（waterfall）</strong>——從來沒成功過。

<strong>歷史註腳</strong>：Winston Royce 1970 年的原始論文裡，瀑布圖的同一頁就寫著「這當然行不通，因為後面的決策會回頭改變前面的決策」，下一頁就畫了往上的回饋箭頭。但<strong>圖像的力量太強</strong>，所有人只記得那條瀑布，夢想著「只要 spec 夠好軟體就完成了」。這也是他提醒：解釋事情時要非常小心。

<strong>適用邊界</strong>：寫個小 app，one-shot 沒問題；他自己在寫的「內嵌程式語言的圖資料庫虛擬機」就不可能。有十億使用者、大量流量的系統，會有<strong>連續性（continuity）</strong>和<strong>資料遷移（data migration）</strong>問題，「one-shot 一次、糟糕、再 one-shot 一次」根本行不通——不如一開始就假設全程迭代。

> 他說，對 SDD 興奮的人聽起來都沒服務過十億使用者。


### 真相 7：形式化方法也救不了你，精靈還會為了讓測試變綠而作弊

<strong>背景</strong>：Beck 研究所時當過「程式正確性證明」課的助教，資料流分析、控制流分析、<strong>不變量（invariants）</strong>這些模式他每天非正式地在用；一年前朋友介紹他用 <strong>Lean</strong>（一個定理證明器／形式化數學語言）搭配精靈做正式證明。

<strong>問題一：仍是一次成形的流程。</strong> 有了形式規格、證明了某些性質，改一個元素就要整個回捲重證。即使有精靈幫忙加速，仍是變更能力的拖累——而他要打造的是鼓勵變更而非阻止變更的系統。

<strong>問題二：形式規格到實作之間的鴻溝（specification-implementation gap）。</strong> 你可以證明一個數學模型有某些性質，但把它變成 C、C++ 或 ARM64 程式碼的「推導」過程，據他所知還沒被完整跨越。

<strong>替代方案</strong>：精心挑選的<strong>範例（examples）</strong>與自動化測試 + 設計上的<strong>防呆（foolproofing）</strong>，兩者並用可以達到低缺陷密度、做出可信的軟體。

<strong>但精靈會抄捷徑</strong>：它不想做設計防呆，還會做出<strong>顛覆測試意圖（subvert the intentions of test cases）</strong>的事——例如直接<strong>回傳常數（returning constants）</strong>讓測試變綠。

> 你得像盯著一個只想說「老闆，能動了」的 14 歲程式設計師一樣盯著它。

### 真相 8：20 萬行程式碼不是 2 萬行的十倍，而是零倍

這是他說「今天早上終於解開 10–15 年舊謎題」的更新版圖：<strong>Effort → Output → Outcome → Mission</strong>。

| 層次 | 名稱 | 說明 |
|---|---|---|
| 1 | <strong>努力（effort）</strong> | 程式設計師投入的工作 |
| 2 | <strong>產出（output）</strong> | 交付給客戶的新功能 |
| 3 | <strong>成果（outcome）</strong> | 客戶使用後<strong>行為改變</strong>。如果軟體做出來沒有任何人的行為改變，那就根本不需要做 |
| 4 | <strong>任務（mission）</strong> | 做軟體的人和用軟體的人<strong>共享的</strong>目標（賺錢、讓國家更安全等） |

他原本用 `impact`（影響），聽了 Whiting 將軍的演講後改用 `mission`。網際網路時代能直接觀察使用者行為，是他職涯的重大轉折（CD 時代根本不知道有沒有人用新功能）。

<strong>度量的暴政（tyranny of metrics）</strong>：

- 「精靈產出 20 萬行程式碼」是 <strong>effort</strong> 的度量，與 mission 無關；從 mission 角度 20 萬行也不是 2 萬行的十倍
- 生產力（productivity）的定義就是 `output / input`，所以精靈讓生產力數字暴漲——但 <strong>LOC、PR 數量</strong>，任何 effort 或 output 的度量，依定義<strong>就不是 mission 的度量</strong>
- 這是<strong>在路燈下找鑰匙（streetlight effect）</strong>：因為那裡好找，不是因為鑰匙在那裡

<strong>Goodhart 定律</strong>（當一個度量變成目標，它就不再是好的度量）：Beck 認為 Goodhart <strong>還太樂觀</strong>。不只是「失去度量意義」，人們會<strong>把整個系統扭曲到變得更糟</strong>，只為了讓數字好看——你失去的不是能見度，是 <strong>mission 本身的進展</strong>。

<strong>兩難</strong>：在這個循環越早期度量，越容易被 Goodhart 化；越接近 mission，越難<strong>歸因（attribution）</strong>——「任務進步了 7%，我貢獻其中 0.075%」根本說不清是誰的功勞。

### 真相 9：領導成功的那一刻，是別人把你的想法當成自己的講給你聽

他的想法能傳播出去，靠的是：找到一種同時打動<strong>腦（heads）</strong>與<strong>心（hearts）</strong>的 mission 表述，然後<strong>重複、重複、重複</strong>——講第一千次還像第一次講一樣，不覺得無聊，這本身是領導技能。

<strong>成功的時刻</strong>：有人跑來說「我有個很棒的點子」，然後把你的想法講給你聽，完全不知道那是你的、不給你任何 credit。


---

## 評論與可商榷之處

<strong>內在張力</strong>：他說程式碼層級的 craft 槓桿大降，卻又說人類仍需理解程式碼、「以學習為目標」。兩者的界線沒畫清——如果理解仍重要，哪些可讀性投資是划算的？

<strong>邊界模糊</strong>：他承認 one-shot 對小 app 可行，卻沒給「多大才需要迭代」的判準，而多數人對自己專案複雜度的估計都偏低。

<strong>形式化方法的批評</strong>主要來自個人經驗（Lean 試用約一年），非系統性論證；形式化方法社群會指出<strong>經過驗證的編譯器（verified compilers）</strong>（如 CompCert）等工具已在處理規格到實作的鴻溝。

<strong>最沒解決的問題</strong>：「在功能之間休息、加回未來性」的做法，他自己也承認在組織裡難以被看見、難以寫進 spec、難以獲得獎勵——最後只給了「重複講故事」的領導力答案。

---

## 對測試與品質工作的直接啟示

1. <strong>「對抗式立場」等於把驗證責任全面提升</strong>：AI 時代的瓶頸不在生產，而在確認「它真的能動」。
2. <strong>測試設計本身必須更刻意、更難被鑽空子</strong>：範例的<strong>選擇與設計防呆</strong>比測試數量重要得多。
3. <strong>Effort / Output 層級的度量（行數、PR 數、測試數、覆蓋率）在 AI 時代會更誘人也更危險</strong>，因為精靈讓這些數字幾乎免費膨脹。

---

## 延伸閱讀

- 原始整理文章：[Spec-Driven Development 就是瀑布——Kent Beck 的九個不中聽真相（敏捷三叔公）](https://agile3uncles.com/2026/10/06/sdd-is-waterfall-kent-becks-9-hard-truths/)
- 演講影片：[Kent Beck — Software Engineering in the Age of AI | Prodacity 2026](https://www.youtube.com/watch?v=F8fBgDCf2Y4)

---

*本篇為個人學習整理，內容觀點主要來自 Kent Beck 的公開演講及敏捷三叔公的整理筆記，版權屬原作者所有。*

