---
title: 「絲襪物理」其實是布料模擬的極限測試：讀 Sakura Rabbit 的 Unity HDRP Stocking Tears 演示
date: 2026-11-25 20:00:00
categories:
  - 技術雜談
tags:
  - Unity
  - HDRP
  - 布料模擬
  - Shader
  - 導讀
index_img: /img/covers/unity-stocking-physics-hdrp-zh.png
banner_img: /img/covers/unity-stocking-physics-hdrp-zh.png
---

![張力下的細網布料：被拉尖、邊緣留著撕開的線頭](/img/covers/unity-stocking-physics-hdrp-zh.png)

> 這篇是導讀，不是教學：80.lv 的報導只講「看起來怎樣」，<strong>沒有一個字的技術拆解</strong>。
>
> 所以我把它拆成三層看：幾何（拉伸與拓撲）、光學（越拉越透）、資料（哪些數字查得到、哪些查不到）。
>
> 結論先講：這類演示的價值不在「絲襪」，而在<strong>布料同時是外觀也是結構</strong>這種很少被一起處理的耦合。

<!-- more -->

## 一句話總結

Sakura Rabbit 的 Stocking Tears 是一個 <strong>Unity HDRP 互動演示</strong>：滑鼠抓住絲襪往外拉，布料被拉長、變透明；持續受張力就起勾絲，放手瞬間破洞彈開，靠近既有撕口再拉會把洞擴大。工程以付費會員附件形式發佈（`Stocking Tears_Project.7z`），<strong>是 Unity 專案，不是可執行檔</strong>。

## 一、演示實際做了什麼

| 操作 | 看到的結果 | 技術上意味著 |
| --- | --- | --- |
| 拖曳布料 | 針織被拉長、透光度上升 | 幾何變形饋入材質（UV 拉伸 → 不透明度／折射） |
| 持續保持張力 | 起勾絲；撕裂前手與布料一起抖動 | 張力累積成損傷狀態，不是單純的碰撞反應 |
| 放開 | 破洞彈開 | 彈性回彈把損傷放大成拓撲改變 |
| 拉近既有撕口 | 洞變大 | 破口邊緣是可繼續斷裂的邊界 |
| 切換視角 | 全身動態／貼近看針織、線頭、破邊 | 兩套相機：一套看運動，一套看材質細節 |
| 按鍵 | `1` 釘住或放開手、`2` 修復破洞與勾絲 | 有狀態機，可重置 |

還有兩個容易忽略的細節：角色有待機循環動畫，被拉住時會<strong>低頭看</strong>；黑白兩色可切換。

## 二、為什麼這件事比看起來難

一般布料模擬（旗子、外套、窗簾）解的是「形狀」；絲襪同時要解三件事：

| 層次 | 一般布料 | 絲襪（這次演示） |
| --- | --- | --- |
| 幾何 | 頂點位置、褶皺 | 網眼被拉成菱形，局部伸長率極高 |
| 光學 | 不透明漫反射 | <strong>半透明</strong>：拉伸改變遮蓋率與折射，越拉越透 |
| 拓撲 | 幾乎不變 | 勾絲 → 破洞 → 擴張，網格要<strong>真的斷</strong> |

第三層才是分水嶺。破洞如果只是貼一張 alpha 遮罩演出來，近距離視角一看就破功；線頭、撕邊要有自己的幾何，拉伸出來的網眼也得在傾斜視角下站得住。而「越拉越透」意味著著色器必須知道<strong>張力</strong>，只靠 UV 做不到。

換句話說，這是一套把布料求解器的內部資料（strain／stretch）餵給 shader 的系統，公開的影片只是最外層的皮。

## 三、報導沒說、但你要先知道的四件事

1. <strong>它不是遊戲，也買不到「玩」</strong>。附件是 `.7z` 的 Unity 專案，得自己開 Unity ＋ HDRP 才有畫面，沒有獨立 exe、沒有試玩版。
2. <strong>授權卡得很緊</strong>。貼文寫明僅限個人學習、研究與教學，禁止轉售、轉讓、公開分享與重新上傳專案或核心內容，而且<strong>格式轉換、重新打包、小幅度修改都不算實質修改</strong>。想放進作品集或商業專案，得先取得同意。
3. <strong>報導沒有技術內容</strong>。80.lv 用兩段話講完成果，mesh、constraint、shader 一個字都沒提。當它是成果驗證可以，當它是教學不行。
4. <strong>HDRP 的硬體門檻是真的</strong>。她在另一條通路（Unity 中文課堂）賣工程檔時順便送雲端編輯器，針對的就是「電腦帶不動 HDRP」這個痛點。

再加一個實務觀察：這類演示的觀眾門檻其實很低——大家只看「像不像」。真正該驗的是張力曲線會不會過衝、破洞擴張速率會不會指數爆炸、低幀率下約束求解會不會抖。這些在宣傳影片裡一個都看不出來。

## 四、如果我要自己做，最小路線

以下是<strong>我的推測路線，不是她的做法</strong>（她沒有公開實作）：

| 需求 | 最省的做法 |
| --- | --- |
| 拉伸與回彈 | Unity 內建 Cloth 或自寫 position-based dynamics，網眼用低解析度網格 |
| 越拉越透 | 頂點階段算伸長率 → 傳到片元 → 遮蓋率與折射隨之變化 |
| 勾絲 | 對超過門檻的 constraint 標記損傷，累積到閾值才斷 |
| 破洞擴張 | 斷 constraint 而不是刪三角形；邊界留線頭幾何 |

順序建議反過來：先把「張力 → 透明度」做到可信，再做斷裂。前者一天能完成、風險最低；後者一旦動到拓撲，除錯成本是前者的十倍以上，而且每次調整參數都要重看一遍動畫。

## 五、原文與延伸

| 項目 | 網址 | 實查 |
| --- | --- | --- |
| 80.lv 報導 | [Pull, Stretch & Explore Realistic Stocking Physics In Unity](https://80.lv/articles/pull-stretch-explore-realistic-stocking-physics-in-unity) | 2026-11-11 刊出；無技術拆解 |
| 作者 Patreon（工程檔） | [Rabbit Sakura — Stocking Tears](https://www.patreon.com/SakuraRabbit) | 貼文鎖定；附件 `Stocking Tears_Project.7z`；頁面以 HKD 計價 |
| 作者 Fanbox | [Sakura Rabbit 樱花兔](https://sakura-rabbit.fanbox.cc/) | 同一工程的另一條通路（日元） |
| Unity 中文課堂 | [樱花兔独家工程文件](https://learn.u3d.cn/) | ¥399 任選兩份，含雲端編輯器；是否含這次最新工程<strong>未確認</strong> |

> <strong>查證說明</strong>：本文事實於 2026-11-25 直接讀報導與作者貼文；付費牆後的正文細節未讀，
> Fanbox 價格頁是 JS 渲染、抓不到檔位與數字。
> 第二、四部分的技術推論是我的拆解，<strong>未經作者確認、也未實測</strong>。
>
> <strong>封面</strong>：本機 ComfyUI 的 Qwen-Image 2.1 生成，刻意不含任何文字（含中文的圖交給擴散模型只會爛成方塊）。
