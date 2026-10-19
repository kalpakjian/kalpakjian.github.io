---
title: Linux 核心移除 AI 輔助標籤：Linus Torvalds 回的是「強制揭露」，不是「禁用 AI」
date: 2026-10-19 21:00:00
categories:
  - AI 研究追蹤
tags:
  - Linux
  - Linus Torvalds
  - 開源治理
  - AI 輔助開發
  - LKML
  - DCO
  - 事實查核
toc: true
index_img: /img/covers/linux-assisted-by-tag-removed.png
banner_img: /img/covers/linux-assisted-by-tag-removed.png
---

> <strong>整理說明</strong>：本文一手來源為 LKML 討論串原文（<a href="https://lkml.iu.edu/2610.1/13255.html">Linus Torvalds 2026-10-13 回信</a>、Laurent Pinchart 與 Kees Cook 的往來）、Linux 核心官方文件 <a href="https://docs.kernel.org/process/coding-assistants.html">AI Coding Assistants</a>、Sasha Levin 的移除 patch（<a href="https://lwn.net/Articles/1099653/">LWN 存檔</a>），以及 LWN、heise、The Register 的報導。查核日期為 <strong>2026-10-19</strong>；文中所有「目前狀態」皆以此日為準，時效限制見「被移除的、與沒有被移除的」一節。

<!-- more -->

## 一句話總結

> Linux 核心社群要拿掉的是「<strong>強制揭露</strong>」（每筆 commit 掛 `Assisted-by` 標籤），不是「<strong>品質要求</strong>」。Linus Torvalds 在這場爭論裡講得很直白：規管「不准用工具 X」的規則蠢到極點，真正該問的是提交者懂不懂自己在提交什麼、願不願意負責。

## 先更正一個常見的錯誤歸因

多數中文與英文報導的標題是「Linus 說禁止 AI 很蠢」，這句話沒錯，但**很容易被讀成「他在回應某個禁止 AI 產生 commit message 的提案」**。實際情況不是這樣。

Linus 那封信是 2026-10-13 在 LKML 上的 `Re: [PATCH] docs: remove Assisted-by references`，收件對象是 **Laurent Pinchart**——一位<strong>反對移除標籤</strong>的開發者。Linus 開頭就把對方的框架整個否定：

> No. What you are about is something entirely different. It has nothing to do with "expectations", and it has everything to do with your hangups.

Laurent 的立場原文是：

> I'm not happy removing the tag without adding another mechanism for required disclosure. Without that, I can foresee submitters pushing back on the question.

他甚至在同一天提出更具體的要求——把 Mesa 專案的規則搬過來，**要求 commit message 必須由人撰寫**：

> I'm increasingly thinking that the Mesa policy of requiring commit messages to be manually written (possibly with machine translation) could be applied to the kernel… Requiring a human-written message would be a good way to quickly ignore patches submitted by meat proxies.

**這正是讀懂 Linus 反諷的鑰匙**：他嘲笑的「不要用編輯器寫 commit message、不要靠倒退鍵掩飾錯字」，不是隨口舉例，而是<strong>直接對著「commit message 必須手寫」這個提案打的</strong>。他反的是「用揭露標籤或手寫訊息來間接規管 AI 使用」這條思路，而不是某個「禁止 AI 產生訊息」的提案。

## 事件時間線

| 日期 | 事件 |
| --- | --- |
| 2025-07 | LLM 標籤提案成形（The Register 記錄） |
| 2025-12-23 | Sasha Levin 撰寫 `coding-assistants.rst`，隨 7.0 週期納入文件 |
| 2026-01-06 | Jonathan Corbet 提交進主線（commit `78d979db6cef`） |
| 2026-07-02 | Jeff Layton 提案整段移除 → **未通過**；Greg Kroah-Hartman 當時主張保留 |
| 2026-08-03 | Christian Brauner 把格式簡化為 `Assisted-by: LLM`（commit `816d9992d9ed`） |
| 2026-10-08 | 布拉格 Maintainers Summit，約 30 位受邀開發者多數支持棄用 |
| 2026-10-09 | Levin 送出 v1（全文只有兩句），當天上午撤回 |
| 2026-10-13 | v2 送出並附上統計；Laurent Pinchart 反對；**Linus 當日回信** |
| 2026-10-14 | Corbet 收進 `docs-next`（commit `1e035297`） |
| 2026-10-19 | 尚未進 Linus 的樹；線上文件**仍要求**標籤 |

## Linus 的原文：兩個類比

以下為原文逐字引用（中文為我的翻譯）：

> Here's a new rule just for you: don't use compilers for any of your kernel submissions. Because if you can't show that you really understand what the machine is actually doing by writing your code in assembler, then I don't want to see your code contribution. You clearly aren't competent if you can't write it that way.

> And btw, you had better not use an editor to write that commit message either. Because I need you to show me that you can actually write a good commit message without using tools that make it easy to backspace and hide the mistakes you made while typing.

> Do you not see how UTTERLY STUPID those kinds of rules would be? So no. We're not going to make stupid rules that say "you can't use tools for X".

他接著說明自己真正的期待是什麼：

> The kind of expectations *I* have is that people do their best and I expect people to understand what they are doing. But that understanding has very little to do with what tools they use. And quite honestly, in my experience, the people I respect and call intelligent are not the ones that shy away from using new and interesting tools.

重點有兩個：**①「不准用工具 X」這種規則在邏輯上會一路滑坡到禁用編譯器與編輯器；② 理解力與工具選擇無關**。

## 標籤的來歷：三次轉折

這個標籤不是一次定案，而是三次拉鋸：

| 階段 | 內容 | 結果 |
| --- | --- | --- |
| 原始設計 | `Assisted-by: AGENT_NAME:MODEL_VERSION [TOOL1] [TOOL2]`，用來追蹤「哪個模型可能帶來特定 bug 或版權風險」 | 納入 7.0 文件 |
| 2026-07 淡化 | Christian Brauner：「imho we would just stop it with any disclosure requirements completely. It's useless imho.」；他認為標明模型是「替專有軟體公司免費打廣告」 | 格式簡化成 `Assisted-by: LLM` |
| 2026-10 移除 | Maintainers Summit 共識 → Levin 提案、Corbet 收進 `docs-next` | 文件層級已移除，**尚未進主線** |

被移除的舊文字（`submitting-patches.rst`）原本寫得很硬：

> If you used any sort of advanced coding tool in the creation of your patch, you need to acknowledge that use by adding an Assisted-by tag. Failure to do so may impede the acceptance of your work.

## 數字怎麼來的：18,533 與 10%

Levin 在 v2 的說明裡給出的理由（**這是他自己的計數，不是第三方重算**）：

> Roughly 10% of the 18,533 non-merge commits in 7.3 through -rc7 carry an Assisted-by tag, while actual LLM use is far more widespread.

他的推論是：有人不知道規則、有人刻意省略、幾乎沒有維護者會追問，**所以「沒有標籤」不代表「沒有用 AI」，「有標籤」也不代表什麼**。對照組可以看 LWN 7 月的記錄：7.2-rc4 時已有超過 1,200 筆 commit 帶標籤——數字本身在動，但佔比始終偏低。

## 被移除的、與沒有被移除的

| 項目 | 狀態 |
| --- | --- |
| `coding-assistants.rst` 的 Attribution 節 | **移除** |
| `submitting-patches.rst` 的 `Using Assisted-by:` 節 | **移除** |
| `checkpatch.pl` 對該標籤的特殊處理 | **移除** |
| 義大利文／葡巴／繁中翻譯頁的對應段落 | 移除（v2 擴大範圍） |
| `generated-content.rst`（工具生成內容指引） | **保留** |
| Developer Certificate of Origin（DCO） | **保留** |
| 提交者責任（review、授權、負全責） | **保留** |

官方文件對 DCO 的措辭沒有鬆動，逐字如下：

> AI agents MUST NOT add Signed-off-by tags. Only humans can legally certify the Developer Certificate of Origin (DCO).

人類提交者的四項責任也原封不動：檢視所有 AI 生成程式碼、確保授權合規、<strong>自己</strong>加上 `Signed-off-by`、承擔全部責任。

至於「揭露」搬到哪裡？依 heise 與後續查核，**改成在 patch 的 cover letter（隨附郵件）說明如何使用 AI 工具**，不再逐筆 commit 打標籤。這裡有個必須說清楚的時效限制：`docs-next` 是開發分支，**截至 2026-10-19，Linus 的樹與線上文件仍要求這個標籤**——「已移除」嚴格說是「已定調、尚未落地」。

## 反方其實講了什麼

把反對者簡化成「反 AI」是誤讀，他們的論點比標題細緻：

| 人物 | 主張 |
| --- | --- |
| Laurent Pinchart | 標籤在 git log 裡沒用，但「**缺少**標籤」是他要求補充說明的低成本工具；「I find the requirement of disclosure (regardless of whether it comes from an Assisted-by tag or something else) helpful for the middleground cases」 |
| Kees Cook | 給了 `Reviewed-by` 並說標籤「as redundant as specifying what editor I use」，但同時指出**要求手寫 commit message 同樣無法強制**，並自承沒通過「反向圖靈測試」——曾把人類寫的長篇 log 誤判為 LLM 產出 |
| Krzysztof Kozlowski | 要求補上理由，指出這等於推翻先前共識（而非不能改） |
| Jakub Kicinski | 早在 7 月就自己把收到的 patch 上的標籤刪掉 |
| Lorenzo Stoakes | `Acked-by` 支持，但認為對抗垃圾提交的長期策略是「aggressively ignore it」 |
| Greg Kroah-Hartman | 7 月主張保留（視為 LLM 參與的訊號），10 月轉為支持移除 |

社群討論（Lobsters 等）裡也出現兩類實務抱怨：驗證 LLM 產出的時間「差不多等於自己寫一遍」，以及「同事說『Claude 說可以』然後推上千行自己看不懂的 diff」。**這兩件事 `Signed-off-by` 都擋不住**——這是整場爭論最誠實的一點。

## Linus 自己也用 LLM，而且掛了標籤

最容易被忽略的旁證：在峰會前後，Linus 自己用 Claude Code 開發了一組 page-cache 最佳化的 patch 系列（8 個 patch），commit message 明白寫出程式、測試程式、已知問題清單與文字初稿都由 Claude Code 在他指導下產出，**而且每一筆都掛了 `Assisted-by: LLM`**。

所以他反對的從來不是標籤本身，而是<strong>「強制」</strong>。這也讓「他是不是在替 AI 護航」這個問題變得沒有意義：他護的是「自願使用、自己負責」這個原則。

## 對工程實務的啟示

如果你的專案也想抄這套規則，可操作的部分是這些：

1. **不要用工具痕跡當品質代理指標。** 標籤、文字風格、commit message 長度都會失真（Kees Cook 的反向圖靈測試就是實證）。
2. **把責任寫死、寫成可強制的形式。** `Signed-off-by`／DCO 是「只有人能簽」的承諾，這是少數真的能自動檢查的機制（DCO bot、CI 檢查）。
3. **揭露改成低摩擦的形式。** 從「每筆 commit 都要」改成「在 cover letter 說明」，是為了保住透明度又不製造無效欄位。
4. **給維護者「快速關閉」的權力。** 反垃圾提交的關鍵不是標籤，而是能無負擔地退回——這也是 Lorenzo 那句「aggressively ignore it」的實務版。
5. **反例值得並讀。** QGIS 在 2026-10-07 走相反方向，直接在主 repo 禁止 AI／agent 輔助的程式碼。同樣面對 LLM 洪水，兩個專案寫出完全相反的規則——這說明**目前沒有共識答案，只有取捨**。

## 評論與可商榷之處

1. **「移除標籤」與「沒有替代機制」之間有空窗。** Laurent 的核心擔憂不是標籤，而是「少了它之後，維護者拿什麼問問題」。cover letter 揭露在實務上比標籤更難被注意到，這個替代方案還沒有實測數據。
2. **共識的強度要講清楚。** Levin 的措辭是「a strong, though not unanimous, consensus」，而且他自己說當時沒有人在會議上主張保留——但「沒人 argue」與「一致同意」是兩件事。
3. **數字是提案者的自述。** 18,533 與 10% 出自 Levin 的 patch 說明，目前沒有第三方重算；引用時應保留出處。
4. **「揭露標籤」被證明無效，不代表「揭露」這件事無效。** 更可能的結論是：**逐筆 commit 的欄位設計錯了**，不是透明度的目標錯了。
5. **時效風險。** 本文寫於 `docs-next` 已收、主線未收的窗口；若你在幾週後讀到這篇，請以 `torvalds/linux` 的 `Documentation/process/coding-assistants.rst` 與線上文件為準。

## 一手來源

- Linus Torvalds，`Re: [PATCH] docs: remove Assisted-by references`（2026-10-13）：<https://lkml.iu.edu/2610.1/13255.html>
- Laurent Pinchart 的回覆（2026-10-13）：<https://lkml.iu.edu/2610.1/11715.html>、<https://lkml.iu.edu/2610.1/12173.html>
- Kees Cook 的回覆（2026-10-13）：<https://lkml.iu.edu/2610.1/13556.html>
- Sasha Levin，`docs: remove Assisted-by references`（v2，2026-10-13，LWN 存檔）：<https://lwn.net/Articles/1099653/>
- Linux 核心文件，AI Coding Assistants：<https://docs.kernel.org/process/coding-assistants.html>
- LWN，《Debating the role of large language models in the kernel community》（2026-07-21）：<https://lwn.net/Articles/1083275/>
- heise，《Linux may drop AI-code labels — Torvalds uses LLMs, too》（2026-10-16）：<https://www.heise.de/en/news/Linux-may-drop-AI-code-labels-Torvalds-uses-LLMs-too-11490773.html>
- The Register，《Linux kernel devs drop obligatory confession of AI tool usage》（2026-10-14）：<https://www.theregister.com/ai-and-ml/2026/10/14/linux-kernel-devs-drop-obligatory-confession-of-ai-tool-usage/5303140>
- INSIDE 中文報導（2026-10-18）：<https://www.inside.com.tw/article/42667-linus-torvalds-rejects-ai-ban-linux-kernel-assisted-by-tag-removal>

---

> **整理與版權聲明**：本文為新聞整理與事實查核，引用的 LKML 郵件、文件與報導版權屬原作者與各媒體所有；時間線、狀態表與「對工程實務的啟示」為我的整理與評論。若與後續主線狀態不符，以核心官方文件為準。
