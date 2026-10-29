# 《Deep Learning》（花書）正體中文導讀

> 來源網站：<https://www.deeplearningbook.org/>　《Deep Learning》Ian Goodfellow、Yoshua Bengio、Aaron Courville（MIT Press，2016）<br />
> 原文狀態：2016 年出版，線上 HTML 版由作者免費公開，內容已定稿<br />
> 性質說明：<strong>這是原創的中文導讀，逐章整理概念脈絡與公式骨架，不是原文的譯本，也不含原文段落</strong><br />
> 涵蓋範圍：第 1–20 章 ＋ 導論與符號章，共 21 個單元；另加 A–F 六個附錄<br />
> 圖表：14 張手繪 SVG（Python 產生器輸出、內嵌、零外部資源）<br />
> 實測環境：Python 3.15.1 ＋ NumPy 2.x；文中可重算的數字都在本機跑過（見附錄 D）<br />
> 🖱️ <strong>互動測驗（推薦）</strong>：附錄 E 提供 <strong>40 題線上測驗</strong>（即時計分、進度自動存在瀏覽器）→ <a href="mc-quiz.html">開始作答</a>

**目錄**

| # | 章節 |
|---|---|
| 0 | [怎麼用這份導讀](#0-怎麼用這份導讀) |
| 1 | [導論：這本書想解決什麼問題](#1-導論這本書想解決什麼問題) |
| 2 | [線性代數：整個深度學習的共同語言](#2-線性代數整個深度學習的共同語言) |
| 3 | [機率與資訊理論：不確定性的語言](#3-機率與資訊理論不確定性的語言) |
| 4 | [數值計算：把公式變成能跑的程式](#4-數值計算把公式變成能跑的程式) |
| 5 | [機器學習基礎：模型好不好的判準](#5-機器學習基礎模型好不好的判準) |
| 6 | [深度前饋網路：從 XOR 開始](#6-深度前饋網路從-xor-開始) |
| 7 | [正則化：對抗過擬合](#7-正則化對抗過擬合) |
| 8 | [訓練的最佳化：為什麼深度網路難訓練](#8-訓練的最佳化為什麼深度網路難訓練) |
| 9 | [卷積網路：把影像的先驗寫進架構](#9-卷積網路把影像的先驗寫進架構) |
| 10 | [序列模型：RNN 與長期依賴](#10-序列模型rnn-與長期依賴) |
| 11 | [實務方法論：把模型做到能用](#11-實務方法論把模型做到能用) |
| 12 | [應用：規模帶來的質變](#12-應用規模帶來的質變) |
| 13 | [線性因子模型：解開潛在變數](#13-線性因子模型解開潛在變數) |
| 14 | [自編碼器：學一個夠用的瓶頸](#14-自編碼器學一個夠用的瓶頸) |
| 15 | [表徵學習：什麼是好特徵](#15-表徵學習什麼是好特徵) |
| 16 | [結構化機率模型：用圖約束機率](#16-結構化機率模型用圖約束機率) |
| 17 | [蒙地卡羅方法：用取樣逼近](#17-蒙地卡羅方法用取樣逼近) |
| 18 | [配分函數：那個算不出來的 Z](#18-配分函數那個算不出來的-z) |
| 19 | [近似推論：把推論變成最佳化](#19-近似推論把推論變成最佳化) |
| 20 | [深度生成模型：學會生成](#20-深度生成模型學會生成) |
| A | [符號與中英對照速查表](#附錄-a符號與中英對照速查表) |
| B | [常見誤解與陷阱](#附錄-b常見誤解與陷阱) |
| C | [原文資源與延伸閱讀](#附錄-c原文資源與延伸閱讀) |
| D | [一頁精華（考前 10 分鐘）](#附錄-d一頁精華考前-10-分鐘) |
| E | [互動式線上測驗（40 題）](#附錄-e互動式線上測驗40-題) |
| F | [答錯題目 → 複習章節對照](#附錄-f答錯題目-複習章節對照) |

## 0　怎麼用這份導讀

《Deep Learning》被中文讀者叫「花書」（封面是畢卡索風格的幾何人臉）。它之所以難讀，不是因為數學多，而是因為<strong>三種語言同時出現</strong>：

1. **線性代數與機率的記號**（第 2、3 章）
2. **機器學習的評估語言**（第 5 章：容量、泛化、驗證集）
3. **工程與研究的取捨語言**（第 8、11 章：為什麼收斂不了、該先修哪裡）

三個部分的分工可以這樣記：<strong>Part I 是工具箱，Part II 是可操作的系統，Part III 是仍在演進的前線</strong>。

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 462" width="100%" role="img" aria-label="全書地圖：三大部分與 20 章的分工" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:900px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="arch-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><text x="450" y="26" font-size="14" fill="#9aa4b2" text-anchor="middle" font-weight="600">三大部分 = 三種問題意識</text><rect x="30" y="42" width="260" height="44" rx="10" fill="#1c2430" stroke="#58a6ff" stroke-width="1.2"/><text x="44" y="60" font-size="11.5" fill="#58a6ff" text-anchor="start" font-weight="700">Part I</text><text x="44" y="77" font-size="11.5" fill="#9aa4b2" text-anchor="start" font-weight="400">應用數學與機器學習基礎</text><rect x="30" y="92" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="44" y="113.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">1　導論：什麼是深度學習</text><rect x="30" y="132" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="44" y="153.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">2　線性代數</text><rect x="30" y="172" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="44" y="193.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">3　機率與資訊理論</text><rect x="30" y="212" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="44" y="233.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">4　數值計算</text><rect x="30" y="252" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="44" y="273.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">5　機器學習基礎</text><rect x="320" y="42" width="260" height="44" rx="10" fill="#1c2430" stroke="#39d0d8" stroke-width="1.2"/><text x="334" y="60" font-size="11.5" fill="#39d0d8" text-anchor="start" font-weight="700">Part II</text><text x="334" y="77" font-size="11.5" fill="#9aa4b2" text-anchor="start" font-weight="400">現代實用深度網路</text><rect x="320" y="92" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="334" y="113.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">6　深度前饋網路</text><rect x="320" y="132" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="334" y="153.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">7　正則化</text><rect x="320" y="172" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="334" y="193.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">8　訓練的最佳化</text><rect x="320" y="212" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="334" y="233.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">9　卷積網路</text><rect x="320" y="252" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="334" y="273.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">10　序列模型：RNN</text><rect x="320" y="292" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="334" y="313.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">11　實務方法論</text><rect x="320" y="332" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="334" y="353.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">12　應用</text><rect x="610" y="42" width="260" height="44" rx="10" fill="#1c2430" stroke="#bc8cff" stroke-width="1.2"/><text x="624" y="60" font-size="11.5" fill="#bc8cff" text-anchor="start" font-weight="700">Part III</text><text x="624" y="77" font-size="11.5" fill="#9aa4b2" text-anchor="start" font-weight="400">深度學習研究</text><rect x="610" y="92" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="624" y="113.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">13　線性因子模型</text><rect x="610" y="132" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="624" y="153.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">14　自編碼器</text><rect x="610" y="172" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="624" y="193.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">15　表徵學習</text><rect x="610" y="212" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="624" y="233.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">16　結構化機率模型</text><rect x="610" y="252" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="624" y="273.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">17　蒙地卡羅方法</text><rect x="610" y="292" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="624" y="313.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">18　配分函數</text><rect x="610" y="332" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="624" y="353.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">19　近似推論</text><rect x="610" y="372" width="260" height="34" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="624" y="393.5" font-size="12.2" fill="#e6edf3" text-anchor="start" font-weight="400">20　深度生成模型</text><text x="450" y="450" font-size="12" fill="#6e7681" text-anchor="middle" font-weight="400">Part I 是工具箱，Part II 是可操作的系統，Part III 是仍在演進的研究前線</text></svg>
<figcaption>圖 1：全書三大部分與 20 章的分工。Part I 提供工具箱，Part II 是可操作的系統，Part III 是研究前線。</figcaption>
</figure>

### 0.1 三條閱讀路徑

同一本書，三種讀者應該走三條完全不同的路徑。照順序從第 1 章讀到第 20 章，是效率最低的讀法。

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 366" width="100%" role="img" aria-label="三種讀者的閱讀路徑" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:900px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="path-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><text x="450" y="26" font-size="13.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">這本書 20 章，沒有必要照順序讀</text><rect x="25" y="46" width="172" height="88" rx="10" fill="#1c2430" stroke="#58a6ff" stroke-width="1.2"/><text x="39" y="78" font-size="13" fill="#58a6ff" text-anchor="start" font-weight="700">實作者</text><text x="39" y="102" font-size="11" fill="#9aa4b2" text-anchor="start" font-weight="400">先能把模型跑起來</text><text x="39" y="122" font-size="10.5" fill="#6e7681" text-anchor="start" font-weight="400">共 7 章</text><rect x="215" y="72" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="253" y="95" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 1</text><line x1="293" y1="90" x2="305" y2="90" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="307" y="72" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="345" y="95" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 5</text><line x1="385" y1="90" x2="397" y2="90" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="399" y="72" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="437" y="95" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 6</text><line x1="477" y1="90" x2="489" y2="90" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="491" y="72" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="529" y="95" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 7</text><line x1="569" y1="90" x2="581" y2="90" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="583" y="72" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="621" y="95" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 8</text><line x1="661" y1="90" x2="673" y2="90" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="675" y="72" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="713" y="95" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 9</text><line x1="753" y1="90" x2="765" y2="90" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="767" y="72" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="805" y="95" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 11</text><rect x="25" y="150" width="172" height="88" rx="10" fill="#1c2430" stroke="#bc8cff" stroke-width="1.2"/><text x="39" y="182" font-size="13" fill="#bc8cff" text-anchor="start" font-weight="700">研究者</text><text x="39" y="206" font-size="11" fill="#9aa4b2" text-anchor="start" font-weight="400">追上研究前線</text><text x="39" y="226" font-size="10.5" fill="#6e7681" text-anchor="start" font-weight="400">共 6 章</text><rect x="215" y="176" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="253" y="199" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 6</text><line x1="293" y1="194" x2="305" y2="194" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="307" y="176" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="345" y="199" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 9</text><line x1="385" y1="194" x2="397" y2="194" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="399" y="176" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="437" y="199" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 10</text><line x1="477" y1="194" x2="489" y2="194" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="491" y="176" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="529" y="199" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 14</text><line x1="569" y1="194" x2="581" y2="194" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="583" y="176" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="621" y="199" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 19</text><line x1="661" y1="194" x2="673" y2="194" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="675" y="176" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="713" y="199" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 20</text><rect x="25" y="254" width="172" height="88" rx="10" fill="#1c2430" stroke="#39d0d8" stroke-width="1.2"/><text x="39" y="286" font-size="13" fill="#39d0d8" text-anchor="start" font-weight="700">理論派</text><text x="39" y="310" font-size="11" fill="#9aa4b2" text-anchor="start" font-weight="400">把推論與學習看清楚</text><text x="39" y="330" font-size="10.5" fill="#6e7681" text-anchor="start" font-weight="400">共 6 章</text><rect x="215" y="280" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="253" y="303" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 2</text><line x1="293" y1="298" x2="305" y2="298" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="307" y="280" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="345" y="303" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 3</text><line x1="385" y1="298" x2="397" y2="298" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="399" y="280" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="437" y="303" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 4</text><line x1="477" y1="298" x2="489" y2="298" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="491" y="280" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="529" y="303" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 17</text><line x1="569" y1="298" x2="581" y2="298" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="583" y="280" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="621" y="303" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 18</text><line x1="661" y1="298" x2="673" y2="298" stroke="#30363d" stroke-width="2.4" stroke-linecap="round" marker-end="url(#pth-ar)"/><rect x="675" y="280" width="76" height="36" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="713" y="303" font-size="11.5" fill="#e6edf3" text-anchor="middle" font-weight="600">Ch 19</text><text x="450" y="354" font-size="11.5" fill="#6e7681" text-anchor="middle" font-weight="400">不管走哪條路，第 5 章（機器學習基礎）與第 11 章（實務方法論）都值得先讀</text></svg>
<figcaption>圖 2：三種讀者的閱讀路徑：實作者、研究者、理論派走的路線不同，但第 5 章與第 11 章都值得先讀。</figcaption>
</figure>

| 讀者 | 起點 | 為什麼這樣排 |
|---|---|---|
| 想動手做 | 第 1 → 5 → 6 → 7 → 8 → 9 → 11 章 | 先有評估紀律（第 5 章），再學模型與訓練；第 11 章教你怎麼除錯 |
| 想追上研究 | 第 6 → 9 → 10 → 14 → 19 → 20 章 | 前饋、卷積、序列三種骨架，接著是表徵與生成模型 |
| 想懂理論 | 第 2 → 3 → 4 → 17 → 18 → 19 章 | 先補數學，再直攻「難算的配分函數」這條主線 |

### 0.2 這份導讀刻意不做的事

原文的線上版是 MIT Press 合約下的 HTML 形式（作者稱之為「弱 DRM」），<strong>著作權屬於作者與出版社</strong>；官網 FAQ 也明確說明中文翻譯權已由人民郵電出版社取得。因此這份導讀：

- **不做全文翻譯**，也不摘錄原文段落；所有文字是重新組織的中文說明
- **公式只保留骨架**（哪一項在做什麼），完整推導請對照原書
- **圖全部重畫**：14 張 SVG 是為了讓「多層網路、圖模型、取樣」這些概念在中文版面裡一眼看懂

---

## 1　導論：這本書想解決什麼問題

### 一句話

<strong>深度學習不是一個演算法，而是一條「用可學習的表示取代人工特徵」的路線。</strong>

### 1.1 三個同心圓

| 層次 | 定義 | 例子 |
|---|---|---|
| 人工智慧 AI | 讓機器表現出智慧的任何方法 | 專家系統、搜尋、規劃 |
| 機器學習 ML | 從資料中自動找出規則 | 線性回歸、SVM、決策樹 |
| 深度學習 DL | 用多層可微函數學「表示」 | CNN、RNN、Transformer、擴散模型 |

差別在**表示（representation）是誰做的**：傳統機器學習靠人設計特徵（HOG、SIFT、n-gram），深度學習讓模型自己學。

### 1.2 三次浪潮與「為什麼是現在」

| 時期 | 名稱 | 卡在哪裡 |
|---|---|---|
| 1940s–1960s | 控制論（cybernetics） | 只有單層感知機，無法表示 XOR |
| 1980s–1990s | 聯結主義（connectionism） | 反向傳播已發明，但資料與算力不足 |
| 2006 之後 | 深度學習 | 資料變大、模型變大、GPU 普及，三件事同時到位 |

書中反覆強調一個判準：**規模（scale）本身就是方法**。同一個演算法，資料量與模型容量放大兩個數量級，行為會質變。第 12 章（應用）整章都在講這件事。

### 1.3 考核自己在哪一層

- 只會呼叫框架 → 你懂的是**工具**
- 能解釋為什麼要驗證集、為什麼要正則化 → 你懂的是**方法**
- 能判斷「這個任務該用哪種歸納偏誤」→ 你懂的是**深度學習**

> <strong>華語讀者最常誤解的一點</strong>：「深度」指的是**表示層數**，不是「更聰明的演算法」。一個 3 層網路配上正確的評估流程，通常贏過一個 30 層但沒有驗證集的網路。

---

## 2　線性代數：整個深度學習的共同語言

### 一句話

<strong>深度學習的所有運算，最後都長成「張量加減乘」——只是張量的階數不同。</strong>

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 300" width="100%" role="img" aria-label="張量的階數：從純量到三階張量" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:900px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="tensor-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><text x="450" y="26" font-size="13.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">階數（rank）= 要用幾個索引才能指到一個元素</text><text x="140" y="56" font-size="12" fill="#39d0d8" text-anchor="middle" font-weight="700">0 階</text><rect x="45" y="68" width="190" height="150" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><circle cx="140" cy="150" r="11" fill="#58a6ff" stroke="none" stroke-width="1.4"/><text x="140" y="155" font-size="12" fill="#08131f" text-anchor="middle" font-weight="700">a</text><text x="140" y="244" font-size="12.5" fill="#e6edf3" text-anchor="middle" font-weight="600">純量 scalar</text><text x="140" y="264" font-size="11" fill="#9aa4b2" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">shape: ()</text><text x="350" y="56" font-size="12" fill="#39d0d8" text-anchor="middle" font-weight="700">1 階</text><rect x="255" y="68" width="190" height="150" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="320" y="108" width="22" height="18" rx="4" fill="#58a6ff" stroke="none" stroke-width="1.2"/><rect x="320" y="130" width="22" height="18" rx="4" fill="#58a6ff" stroke="none" stroke-width="1.2"/><rect x="320" y="152" width="22" height="18" rx="4" fill="#58a6ff" stroke="none" stroke-width="1.2"/><rect x="320" y="174" width="22" height="18" rx="4" fill="#58a6ff" stroke="none" stroke-width="1.2"/><text x="366" y="155" font-size="12.5" fill="#58a6ff" text-anchor="start" font-weight="700">a</text><text x="350" y="244" font-size="12.5" fill="#e6edf3" text-anchor="middle" font-weight="600">向量 vector</text><text x="350" y="264" font-size="11" fill="#9aa4b2" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">shape: (n,)</text><text x="560" y="56" font-size="12" fill="#39d0d8" text-anchor="middle" font-weight="700">2 階</text><rect x="465" y="68" width="190" height="150" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="526" y="122" width="22" height="18" rx="3" fill="#39d0d8" stroke="#0d1117" stroke-width="1.2"/><rect x="550" y="122" width="22" height="18" rx="3" fill="#39d0d8" stroke="#0d1117" stroke-width="1.2"/><rect x="574" y="122" width="22" height="18" rx="3" fill="#39d0d8" stroke="#0d1117" stroke-width="1.2"/><rect x="526" y="144" width="22" height="18" rx="3" fill="#39d0d8" stroke="#0d1117" stroke-width="1.2"/><rect x="550" y="144" width="22" height="18" rx="3" fill="#39d0d8" stroke="#0d1117" stroke-width="1.2"/><rect x="574" y="144" width="22" height="18" rx="3" fill="#39d0d8" stroke="#0d1117" stroke-width="1.2"/><rect x="526" y="166" width="22" height="18" rx="3" fill="#39d0d8" stroke="#0d1117" stroke-width="1.2"/><rect x="550" y="166" width="22" height="18" rx="3" fill="#39d0d8" stroke="#0d1117" stroke-width="1.2"/><rect x="574" y="166" width="22" height="18" rx="3" fill="#39d0d8" stroke="#0d1117" stroke-width="1.2"/><text x="560" y="244" font-size="12.5" fill="#e6edf3" text-anchor="middle" font-weight="600">矩陣 matrix</text><text x="560" y="264" font-size="11" fill="#9aa4b2" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">shape: (m, n)</text><text x="770" y="56" font-size="12" fill="#39d0d8" text-anchor="middle" font-weight="700">3 階</text><rect x="675" y="68" width="190" height="150" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="750" y="138" width="22" height="18" rx="3" fill="#6a4c9c" stroke="#0d1117" stroke-width="1.2"/><rect x="774" y="138" width="22" height="18" rx="3" fill="#6a4c9c" stroke="#0d1117" stroke-width="1.2"/><rect x="750" y="160" width="22" height="18" rx="3" fill="#6a4c9c" stroke="#0d1117" stroke-width="1.2"/><rect x="774" y="160" width="22" height="18" rx="3" fill="#6a4c9c" stroke="#0d1117" stroke-width="1.2"/><rect x="737" y="127" width="22" height="18" rx="3" fill="#6a4c9c" stroke="#0d1117" stroke-width="1.2"/><rect x="761" y="127" width="22" height="18" rx="3" fill="#6a4c9c" stroke="#0d1117" stroke-width="1.2"/><rect x="737" y="149" width="22" height="18" rx="3" fill="#6a4c9c" stroke="#0d1117" stroke-width="1.2"/><rect x="761" y="149" width="22" height="18" rx="3" fill="#6a4c9c" stroke="#0d1117" stroke-width="1.2"/><rect x="724" y="116" width="22" height="18" rx="3" fill="#bc8cff" stroke="#0d1117" stroke-width="1.2"/><rect x="748" y="116" width="22" height="18" rx="3" fill="#bc8cff" stroke="#0d1117" stroke-width="1.2"/><rect x="724" y="138" width="22" height="18" rx="3" fill="#bc8cff" stroke="#0d1117" stroke-width="1.2"/><rect x="748" y="138" width="22" height="18" rx="3" fill="#bc8cff" stroke="#0d1117" stroke-width="1.2"/><text x="770" y="244" font-size="12.5" fill="#e6edf3" text-anchor="middle" font-weight="600">張量 tensor</text><text x="770" y="264" font-size="11" fill="#9aa4b2" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">shape: (m, n, k)</text><text x="450" y="290" font-size="11.8" fill="#6e7681" text-anchor="middle" font-weight="400">同一個維度 n 可以是幾萬維 —— 深度學習就是在大張量上做線性代數</text></svg>
<figcaption>圖 3：張量的階數：從 0 階純量到 3 階張量，階數等於「要用幾個索引才能指到一個元素」。</figcaption>
</figure>

### 2.1 四個必須分清楚的物件

| 物件 | 階數 | 索引方式 | 在神經網路裡的角色 |
|---|---|---|---|
| 純量 scalar | 0 | 無 | 損失值、學習率 |
| 向量 vector | 1 | a<sub>i</sub> | 一筆樣本的特徵 |
| 矩陣 matrix | 2 | A<sub>i,j</sub> | 一層的權重、一個 batch |
| 張量 tensor | 3+ | A<sub>i,j,k</sub> | 一個 batch 的圖片（N×H×W×C） |

### 2.2 五個真正會用到的工具

1. **矩陣乘法**：`(m×n)·(n×p) → (m×p)`。神經網路一層就是 `h = σ(Wx + b)`，而一個 batch 是 `H = σ(XWᵀ + b)`。
2. **範數（norm）**：衡量「大小」。L2 是歐氏距離、L1 偏愛稀疏、L∞ 看最大分量。第 7 章的正則化就是在損失裡加一項範數。
3. **特徵分解**：只有<strong>實對稱矩陣</strong>保證有實特徵值與正交特徵向量；一般矩陣不保證。
4. **奇異值分解 SVD**：對**任意**矩陣都成立，`A = UΣVᵀ`。它是 PCA、壓縮、偽逆的共同底層。
5. **Moore-Penrose 偽逆**：`A⁺ = VΣ⁺Uᵀ`，用來解「無解」或「無窮多解」的線性系統——第 5 章拿它解釋「為什麼線性回歸其實沒有唯一的解」。

### 2.3 一個常被跳過的細節

書中特別提醒：**PCA 不是「找出最重要的維度」，而是「找出重建誤差最小的線性子空間」**。兩者聽起來一樣，但在數學上是不同角度——後者才能推廣到第 13 章的機率 PCA 與第 14 章的自編碼器。

> <strong>章末考點</strong>：任意矩陣一定可以 SVD，但不一定可以特徵分解；偽逆解出來的是「最小範數解」。

---

## 3　機率與資訊理論：不確定性的語言

### 一句話

<strong>機率讓我們「量化不確定」，資訊理論讓我們「量化驚訝」——而訓練神經網路就是在最小化驚訝。</strong>

### 3.1 三組一定要分開的詞

| 容易混的兩組 | 差別 |
|---|---|
| 頻率派 vs 貝氏派 | 參數是「固定的未知數」還是「有分布的隨機變數」 |
| PMF vs PDF | 離散（可以加總）vs 連續（只能積分） |
| 條件機率 vs 聯合機率 | `P(y|x)`（判別）與 `P(x,y)`（生成）—— 第 20 章整章建立在這個差別上 |

### 3.2 常用分布：記住「什麼時候會出現」

| 分布 | 什麼場合出現 |
|---|---|
| Bernoulli | 二元分類的輸出、Dropout 的遮罩 |
| Multinoulli（categorical） | 多類分類的 softmax 輸出、語言模型的下一個詞 |
| 常態 Gaussian | 回歸的誤差、VAE 的潛在分布先驗 |
| 指數／Laplace | 稀疏先驗（L1 正則化的機率版本） |
| 經驗分布 | 訓練集本身，就是最大似然的來源 |

### 3.3 資訊理論的三個量

<div class="eq">自資訊　I(x) = −log P(x)　　（越不可能的事件，資訊量越大）</div>
<div class="eq">熵　　　H(x) = −E<sub>x∼P</sub> log P(x)　　（一個分布有多「不確定」）</div>
<div class="eq">KL 散度　D<sub>KL</sub>(P‖Q) = E<sub>x∼P</sub> log [P(x) / Q(x)]　　（用 Q 近似 P 要付的代價）</div>

KL 散度**不對稱**（`D(P‖Q) ≠ D(Q‖P)`），所以它不是距離。這個不對稱在變分推論裡是關鍵：第 19 章選定的方向，會決定近似分布是「覆蓋所有模式」還是「鎖定一個模式」。

### 3.4 為什麼 softplus 會出現在書裡

ReLU 的平滑版本 `ζ(x) = log(1 + eˣ)` 叫 softplus。書中拿它說明一件事：<strong>很多「啟用函數」其實是某個機率模型的自然推論</strong>，不是憑感覺挑的。

---

## 4　數值計算：把公式變成能跑的程式

### 一句話

<strong>數學上等價的式子，在浮點數上不等價——這一章教你在實作前先想「會不會爆」。</strong>

### 4.1 三個必踩的坑

| 坑 | 症狀 | 解法 |
|---|---|---|
| 上溢 overflow | `exp(1000)` 變 `inf`，softmax 全變 `nan` | 先減去最大值：`softmax(z) = softmax(z − max z)` |
| 下溢 underflow | 很多小機率相乘變 0，`log(0)` 變 `-inf` | 在對數空間相加，不要相乘 |
| 病態條件 ill-conditioning | 輸入微小擾動讓輸出劇烈變化 | 看 Hessian 的條件數；用正規化或更好的參數化 |

### 4.2 梯度下降的三個層次

1. **一階**：`θ ← θ − η∇f(θ)`。只要算梯度，便宜但慢。
2. **牛頓法**：用 Hessian 的逆 `θ ← θ − H⁻¹∇f`。一步到位的二次收斂，但 `H` 是 n×n，深度網路不可能算。
3. **擬牛頓（L-BFGS）**：用歷史梯度近似 `H⁻¹`。小模型好用，大模型仍回到一階＋自適應學習率。

### 4.3 約束最佳化與 KKT

書中用廣義 Lagrangian 統一處理「等式約束」與「不等式約束」，得到 KKT 條件。**這一節的實務價值只有一句**：如果你打算自己寫一個帶約束的損失（例如「權重必須非負」），請先確認它可以用重新參數化（`w = eᵘ`）解決，那比 KKT 好寫得多。

> <strong>章末考點</strong>：`log-sum-exp` 技巧、梯度消失與梯度爆炸的數值來源、Hessian 條件數與「峽谷地形」的關係。

---

## 5　機器學習基礎：模型好不好的判準

### 一句話

<strong>這一章是全書最重要的一章：它定義了「好」是什麼意思，後面 15 章都在這個定義下工作。</strong>

### 5.1 學習演算法的五個零件

任何機器學習系統都可以拆成五個零件。少一個就不知道自己在調什麼。

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 350" width="100%" role="img" aria-label="學習演算法的五個零件與資料切分" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:900px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="mlflow-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><text x="450" y="26" font-size="13.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">機器學習 = 在假設空間裡，用資料把「損失」壓下去</text><rect x="18" y="46" width="152" height="88" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="94" y="72" font-size="14.5" fill="#58a6ff" text-anchor="middle" font-weight="700">資料</text><text x="94" y="96" font-size="11.8" fill="#e6edf3" text-anchor="middle" font-weight="400">樣本 × 標籤</text><text x="94" y="118" font-size="11.2" fill="#6e7681" text-anchor="middle" font-weight="400">決定上限</text><line x1="174" y1="90" x2="195" y2="90" stroke="#30363d" stroke-width="2.2" stroke-linecap="round" marker-end="url(#mlf-ar)"/><rect x="200" y="46" width="152" height="88" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="276" y="72" font-size="14.5" fill="#58a6ff" text-anchor="middle" font-weight="700">模型</text><text x="276" y="96" font-size="11.8" fill="#e6edf3" text-anchor="middle" font-weight="400">假設空間 f(x;θ)</text><text x="276" y="118" font-size="11.2" fill="#6e7681" text-anchor="middle" font-weight="400">決定表達力</text><line x1="356" y1="90" x2="377" y2="90" stroke="#30363d" stroke-width="2.2" stroke-linecap="round" marker-end="url(#mlf-ar)"/><rect x="382" y="46" width="152" height="88" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="458" y="72" font-size="14.5" fill="#58a6ff" text-anchor="middle" font-weight="700">損失</text><text x="458" y="96" font-size="11.8" fill="#e6edf3" text-anchor="middle" font-weight="400">代理目標函數</text><text x="458" y="118" font-size="11.2" fill="#6e7681" text-anchor="middle" font-weight="400">決定往哪走</text><line x1="538" y1="90" x2="559" y2="90" stroke="#30363d" stroke-width="2.2" stroke-linecap="round" marker-end="url(#mlf-ar)"/><rect x="564" y="46" width="152" height="88" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="640" y="72" font-size="14.5" fill="#58a6ff" text-anchor="middle" font-weight="700">最佳化</text><text x="640" y="96" font-size="11.8" fill="#e6edf3" text-anchor="middle" font-weight="400">梯度／動量／Adam</text><text x="640" y="118" font-size="11.2" fill="#6e7681" text-anchor="middle" font-weight="400">決定走多快</text><line x1="720" y1="90" x2="741" y2="90" stroke="#30363d" stroke-width="2.2" stroke-linecap="round" marker-end="url(#mlf-ar)"/><rect x="746" y="46" width="152" height="88" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="822" y="72" font-size="14.5" fill="#58a6ff" text-anchor="middle" font-weight="700">評估</text><text x="822" y="96" font-size="11.8" fill="#e6edf3" text-anchor="middle" font-weight="400">驗證集＋測試集</text><text x="822" y="118" font-size="11.2" fill="#6e7681" text-anchor="middle" font-weight="400">決定可信度</text><text x="18" y="172" font-size="12.8" fill="#e6edf3" text-anchor="start" font-weight="700">資料切分：三種集合各管一件事</text><rect x="30" y="186" width="504" height="46" rx="8" fill="#58a6ff" stroke="none" stroke-width="1.2"/><text x="44" y="206" font-size="12.5" fill="#08131f" text-anchor="start" font-weight="700">訓練集 60%</text><text x="44" y="223" font-size="11" fill="#0d1117" text-anchor="start" font-weight="400">用來調整參數 θ</text><rect x="534" y="186" width="168" height="46" rx="8" fill="#d29922" stroke="none" stroke-width="1.2"/><text x="548" y="206" font-size="12.5" fill="#08131f" text-anchor="start" font-weight="700">驗證集 20%</text><text x="548" y="223" font-size="11" fill="#0d1117" text-anchor="start" font-weight="400">用來選超參數</text><rect x="702" y="186" width="168" height="46" rx="8" fill="#3fb950" stroke="none" stroke-width="1.2"/><text x="716" y="206" font-size="12.5" fill="#08131f" text-anchor="start" font-weight="700">測試集 20%</text><text x="716" y="223" font-size="11" fill="#0d1117" text-anchor="start" font-weight="400">只回報一次成績</text><circle cx="36" cy="264" r="3" fill="#d29922" stroke="none" stroke-width="1.4"/><text x="48" y="268" font-size="11.8" fill="#9aa4b2" text-anchor="start" font-weight="400">驗證集拿來選模型，測試集拿來報成績 —— 用測試集挑超參數＝偷看考卷</text><circle cx="36" cy="288" r="3" fill="#d29922" stroke="none" stroke-width="1.4"/><text x="48" y="292" font-size="11.8" fill="#9aa4b2" text-anchor="start" font-weight="400">訓練誤差幾乎一定下降，泛化誤差不一定（第 5 章與第 7 章都在處理這件事）</text><circle cx="36" cy="312" r="3" fill="#d29922" stroke="none" stroke-width="1.4"/><text x="48" y="316" font-size="11.8" fill="#9aa4b2" text-anchor="start" font-weight="400">資料分布漂移（dataset shift）時，三種集合都要重新切分（第 11 章）</text></svg>
<figcaption>圖 4：學習演算法的五個零件（資料、模型、損失、最佳化、評估）與訓練／驗證／測試三種集合的分工。</figcaption>
</figure>

### 5.2 容量：擬合能力與泛化能力的拔河

<strong>訓練誤差</strong>幾乎一定隨容量下降；<strong>泛化誤差</strong>是 U 形。兩條線之間的縫叫<strong>泛化差距（generalization gap）</strong>。

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 392" width="100%" role="img" aria-label="容量與誤差：訓練誤差下降、泛化誤差是 U 形" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:880px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="capacity-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><line x1="96" y1="300" x2="830" y2="300" stroke="#6e7681" stroke-width="1.4" stroke-linecap="round"/><line x1="96" y1="300" x2="96" y2="56" stroke="#6e7681" stroke-width="1.4" stroke-linecap="round"/><text x="60" y="62" font-size="12" fill="#9aa4b2" text-anchor="start" font-weight="400">誤差</text><text x="830" y="326" font-size="12" fill="#9aa4b2" text-anchor="end" font-weight="400">模型容量 →</text><text x="84" y="304" font-size="11" fill="#6e7681" text-anchor="end" font-weight="400">小</text><text x="834" y="304" font-size="11" fill="#6e7681" text-anchor="start" font-weight="400">大</text><rect x="652" y="56" width="178" height="244" fill="#d29922" opacity="0.18" rx="6"/><text x="741" y="76" font-size="12" fill="#d29922" text-anchor="middle" font-weight="700">過擬合區</text><line x1="102" y1="272.16" x2="824" y2="272.16" stroke="#6e7681" stroke-width="1.4" stroke-linecap="round" stroke-dasharray="6 5"/><text x="824" y="263.16" font-size="11" fill="#6e7681" text-anchor="end" font-weight="400">貝氏誤差（底線）</text><path d="M102,193.28 L109.22,198.684 L116.44,203.774 L123.66,208.567 L130.88,213.081 L138.1,217.332 L145.32,221.336 L152.54,225.106 L159.76,228.657 L166.98,232.001 L174.2,235.15 L181.42,238.116 L188.64,240.909 L195.86,243.54 L203.08,246.017 L210.3,248.35 L217.52,250.548 L224.74,252.617 L231.96,254.566 L239.18,256.401 L246.4,258.129 L253.62,259.757 L260.84,261.29 L268.06,262.734 L275.28,264.093 L282.5,265.374 L289.72,266.579 L296.94,267.715 L304.16,268.784 L311.38,269.792 L318.6,270.74 L325.82,271.634 L333.04,272.475 L340.26,273.267 L347.48,274.013 L354.7,274.716 L361.92,275.378 L369.14,276.001 L376.36,276.588 L383.58,277.141 L390.8,277.661 L398.02,278.152 L405.24,278.613 L412.46,279.048 L419.68,279.458 L426.9,279.843 L434.12,280.207 L441.34,280.549 L448.56,280.871 L455.78,281.174 L463,281.46 L470.22,281.729 L477.44,281.982 L484.66,282.221 L491.88,282.446 L499.1,282.657 L506.32,282.857 L513.54,283.044 L520.76,283.221 L527.98,283.388 L535.2,283.544 L542.42,283.692 L549.64,283.831 L556.86,283.962 L564.08,284.085 L571.3,284.202 L578.52,284.311 L585.74,284.414 L592.96,284.511 L600.18,284.602 L607.4,284.688 L614.62,284.769 L621.84,284.846 L629.06,284.918 L636.28,284.985 L643.5,285.049 L650.72,285.109 L657.94,285.166 L665.16,285.219 L672.38,285.269 L679.6,285.316 L686.82,285.361 L694.04,285.403 L701.26,285.442 L708.48,285.479 L715.7,285.514 L722.92,285.547 L730.14,285.578 L737.36,285.607 L744.58,285.635 L751.8,285.661 L759.02,285.685 L766.24,285.708 L773.46,285.73 L780.68,285.75 L787.9,285.769 L795.12,285.788 L802.34,285.805 L809.56,285.821 L816.78,285.836 L824,285.85" fill="none" stroke="#58a6ff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M102,250.7 L109.22,252.489 L116.44,254.151 L123.66,255.695 L130.88,257.128 L138.1,258.459 L145.32,259.693 L152.54,260.838 L159.76,261.898 L166.98,262.879 L174.2,263.786 L181.42,264.623 L188.64,265.394 L195.86,266.102 L203.08,266.752 L210.3,267.345 L217.52,267.885 L224.74,268.374 L231.96,268.814 L239.18,269.208 L246.4,269.557 L253.62,269.864 L260.84,270.13 L268.06,270.355 L275.28,270.543 L282.5,270.693 L289.72,270.807 L296.94,270.886 L304.16,270.931 L311.38,270.943 L318.6,270.923 L325.82,270.871 L333.04,270.787 L340.26,270.674 L347.48,270.53 L354.7,270.357 L361.92,270.155 L369.14,269.925 L376.36,269.666 L383.58,269.379 L390.8,269.065 L398.02,268.724 L405.24,268.356 L412.46,267.961 L419.68,267.54 L426.9,267.092 L434.12,266.618 L441.34,266.118 L448.56,265.593 L455.78,265.042 L463,264.465 L470.22,263.863 L477.44,263.236 L484.66,262.584 L491.88,261.906 L499.1,261.204 L506.32,260.476 L513.54,259.724 L520.76,258.947 L527.98,258.145 L535.2,257.319 L542.42,256.468 L549.64,255.592 L556.86,254.692 L564.08,253.767 L571.3,252.818 L578.52,251.844 L585.74,250.846 L592.96,249.823 L600.18,248.776 L607.4,247.705 L614.62,246.609 L621.84,245.489 L629.06,244.345 L636.28,243.177 L643.5,241.984 L650.72,240.767 L657.94,239.525 L665.16,238.26 L672.38,236.97 L679.6,235.656 L686.82,234.318 L694.04,232.955 L701.26,231.569 L708.48,230.158 L715.7,228.723 L722.92,227.264 L730.14,225.78 L737.36,224.273 L744.58,222.741 L751.8,221.185 L759.02,219.605 L766.24,218.001 L773.46,216.373 L780.68,214.72 L787.9,213.044 L795.12,211.343 L802.34,209.618 L809.56,207.869 L816.78,206.096 L824,204.298" fill="none" stroke="#3fb950" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><rect x="118" y="74" width="268" height="62" rx="8" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><line x1="132" y1="94" x2="162" y2="94" stroke="#58a6ff" stroke-width="2.4" stroke-linecap="round"/><text x="170" y="98" font-size="11" fill="#e6edf3" text-anchor="start" font-weight="400">訓練誤差：容量越大越貼合</text><line x1="132" y1="118" x2="162" y2="118" stroke="#3fb950" stroke-width="2.4" stroke-linecap="round"/><text x="170" y="122" font-size="11" fill="#e6edf3" text-anchor="start" font-weight="400">泛化誤差：先降後升的 U 形</text><text x="440" y="378" font-size="11.8" fill="#6e7681" text-anchor="middle" font-weight="400">容量不足＝欠擬合（兩條線都高）；容量過大＝過擬合（兩條線張開）</text></svg>
<figcaption>圖 5：容量與誤差：訓練誤差單調下降，泛化誤差是先降後升的 U 形，兩者之間的縫就是泛化差距。</figcaption>
</figure>

| 現象 | 訓練誤差 | 測試誤差 | 對策 |
|---|---|---|---|
| 欠擬合 underfitting | 高 | 高 | 加大模型、訓練更久、更好的特徵 |
| 過擬合 overfitting | 低 | 高 | 更多資料、正則化（第 7 章）、早停 |
| 剛剛好 | 低 | 低 | —— 但只能用驗證集判斷 |

### 5.3 估計量的偏差與方差

書中把期望測試誤差拆成三塊：

<div class="eq">E[誤差] = 偏差² ＋ 方差 ＋ 不可約噪聲</div>

- **偏差**：模型假設太強（例如用直線擬合曲線）
- **方差**：模型對訓練集太敏感（換一批資料，答案就變）
- **不可約噪聲**：資料本身的隨機性，誰都消不掉

<strong>這條分解解釋了為什麼「更大的模型」不是萬靈丹</strong>：容量↑ 通常偏差↓、方差↑。

### 5.4 最大似然：為什麼大家都用交叉熵

最大似然等於最小化 `−log p_model(y|x)`，也就是**交叉熵**。所以：

- 分類用交叉熵、回歸用 MSE，不是習慣問題，而是<strong>對應不同的機率假設</strong>（categorical 與 Gaussian）
- 加上 L2 正則化的最大似然 ＝ 最大後驗（MAP）＋ Gaussian 先驗

### 5.5 促使深度學習的兩個難題

1. **維度詛咒**：維度越高，空間越空。用網格逼近一個 100 維函數是不可行的。
2. **流形假設**：真實資料其實集中在一個低維流形上。深度學習的賭注就是「先驗地相信這個流形存在」。

> <strong>章末考點</strong>：偏差－方差分解、為什麼驗證集不能用來訓練、`容量`與`資料量`必須一起談。

---

## 6　深度前饋網路：從 XOR 開始

### 一句話

<strong>前饋網路 = 一堆仿射變換中間夾非線性；沒有非線性，疊幾層都等於一層。</strong>

### 6.1 XOR：最小的反例

XOR 的四個點 (0,0)、(1,1) 屬類別 0，(0,1)、(1,0) 屬類別 1。**任何一條直線都無法分開它們**，所以單層線性模型註定失敗。

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 400" width="100%" role="img" aria-label="XOR：一條直線分不開，兩條線可以" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:880px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="xor-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><text x="440" y="26" font-size="13.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">XOR 是全書最便宜的反例：它證明線性模型的天花板</text><rect x="25" y="44" width="390" height="288" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="220" y="66" font-size="12.8" fill="#ff7b72" text-anchor="middle" font-weight="700">單層線性模型：一條直線</text><line x1="93" y1="276" x2="269" y2="276" stroke="#30363d" stroke-width="1" stroke-linecap="round"/><line x1="121" y1="300" x2="121" y2="128" stroke="#30363d" stroke-width="1" stroke-linecap="round"/><line x1="93" y1="202" x2="269" y2="202" stroke="#30363d" stroke-width="1" stroke-linecap="round"/><line x1="195" y1="300" x2="195" y2="128" stroke="#30363d" stroke-width="1" stroke-linecap="round"/><line x1="93" y1="128" x2="269" y2="128" stroke="#30363d" stroke-width="1" stroke-linecap="round"/><line x1="269" y1="300" x2="269" y2="128" stroke="#30363d" stroke-width="1" stroke-linecap="round"/><circle cx="121" cy="276" r="8" fill="#3fb950" stroke="none" stroke-width="1.4"/><circle cx="195" cy="202" r="8" fill="#3fb950" stroke="none" stroke-width="1.4"/><rect x="114" y="195" width="14" height="14" rx="3" fill="#d29922" stroke="none" stroke-width="1.2"/><rect x="188" y="269" width="14" height="14" rx="3" fill="#d29922" stroke="none" stroke-width="1.2"/><text x="220" y="316" font-size="11.2" fill="#9aa4b2" text-anchor="middle" font-weight="400">兩類點交錯排列，任何直線都只能切一半</text><line x1="158" y1="138" x2="158" y2="284" stroke="#ff7b72" stroke-width="2" stroke-linecap="round" stroke-dasharray="7 5"/><rect x="465" y="44" width="390" height="288" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="660" y="66" font-size="12.8" fill="#39d0d8" text-anchor="middle" font-weight="700">一層隱藏單元：兩條線</text><line x1="533" y1="276" x2="709" y2="276" stroke="#30363d" stroke-width="1" stroke-linecap="round"/><line x1="561" y1="300" x2="561" y2="128" stroke="#30363d" stroke-width="1" stroke-linecap="round"/><line x1="533" y1="202" x2="709" y2="202" stroke="#30363d" stroke-width="1" stroke-linecap="round"/><line x1="635" y1="300" x2="635" y2="128" stroke="#30363d" stroke-width="1" stroke-linecap="round"/><line x1="533" y1="128" x2="709" y2="128" stroke="#30363d" stroke-width="1" stroke-linecap="round"/><line x1="709" y1="300" x2="709" y2="128" stroke="#30363d" stroke-width="1" stroke-linecap="round"/><circle cx="561" cy="276" r="8" fill="#3fb950" stroke="none" stroke-width="1.4"/><circle cx="635" cy="202" r="8" fill="#3fb950" stroke="none" stroke-width="1.4"/><rect x="554" y="195" width="14" height="14" rx="3" fill="#d29922" stroke="none" stroke-width="1.2"/><rect x="628" y="269" width="14" height="14" rx="3" fill="#d29922" stroke="none" stroke-width="1.2"/><text x="660" y="316" font-size="11.2" fill="#9aa4b2" text-anchor="middle" font-weight="400">兩條線夾出的帶狀區域就是類別 1</text><polygon points="561,239 598,276 672,276 561,165" fill="#39d0d8" opacity="0.22"/><line x1="561" y1="239" x2="598" y2="276" stroke="#39d0d8" stroke-width="2.4" stroke-linecap="round"/><line x1="561" y1="165" x2="672" y2="276" stroke="#39d0d8" stroke-width="2.4" stroke-linecap="round"/><text x="440" y="384" font-size="11.8" fill="#6e7681" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">h1 = step(x1 + x2 − 0.5)、h2 = step(x1 + x2 − 1.5)，輸出 y = h1 − h2</text></svg>
<figcaption>圖 6：XOR 的最小反例：單層線性模型只能畫一條直線；一層隱藏單元用兩條線夾出帶狀區域解決問題。</figcaption>
</figure>

解法：一層隱藏單元把「兩條線」變成兩個新特徵 `h₁`、`h₂`，輸出層再做一次線性組合。這就是書中說的：<strong>隱藏層的作用是「改變表示的座標系」</strong>，讓原本不可分的問題在新座標下變成可分的。

### 6.2 輸出單元：選錯就訓練不動

| 任務 | 輸出單元 | 損失 | 為什麼 |
|---|---|---|---|
| 二元分類 | sigmoid | binary cross-entropy | 梯度不會飽和，且輸出可解釋為機率 |
| 多類分類 | softmax | categorical cross-entropy | 各類互斥，總和為 1 |
| 多標籤 | 多個 sigmoid | 各別 binary CE | 標籤不互斥 |
| 回歸 | 線性 | MSE（Gaussian） | 對應常態誤差假設 |
| 回歸（怕離群值） | 線性 | MAE（Laplace） | 對應 Laplace 誤差假設 |

### 6.3 隱藏單元：ReLU 為什麼統治一切

| 單元 | 式子 | 特性 |
|---|---|---|
| sigmoid / tanh | `1/(1+e⁻ˣ)`、`tanh` | 兩端飽和 → 梯度消失 |
| ReLU | `max(0, x)` | 大面積線性，梯度不會飽和；一半輸出為 0（稀疏） |
| Leaky／PReLU | `max(αx, x)` | 修掉「死亡 ReLU」 |
| Maxout | 取多組線性的最大值 | 理論上可逼近任何凸函數 |

### 6.4 萬能逼近與「深比寬好」

- **萬能逼近定理**：一個夠寬的單隱藏層網路可以逼近任何連續函數——但「存在」不等於「學得到」。
- **深度帶來的指數級效率**：某些函數用深網路需要 O(k) 個單元，用淺網路需要 O(2ᵏ)。這是 Part II 一路的伏筆（第 15 章正式講）。

### 6.5 反向傳播：不是演算法，是鏈式法則的排程

反向傳播只是<strong>「用計算圖把鏈式法則排成從輸出往輸入的順序」</strong>。兩個必須分開的概念：

- **前向**：算出每個節點的數值
- **反向**：算出每個節點的梯度（`∂L/∂節點`）

成本大約是前向的兩倍——這是它勝過數值微分（成本與參數數成正比）的原因。第 8 章會處理「鏈太長時梯度會爆或消」。

---

## 7　正則化：對抗過擬合

### 一句話

<strong>正則化 = 把「你對答案的偏好」寫進損失函數或訓練流程。</strong>

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 376" width="100%" role="img" aria-label="正則化工具箱：六種壓住過擬合的手段" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:900px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="reg-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><text x="450" y="26" font-size="13.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">正則化 = 用「偏好簡單解」換「更好的泛化」</text><rect x="25" y="44" width="270" height="136" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="39" y="58" width="4" height="18" rx="2" fill="#58a6ff" stroke="none" stroke-width="1.2"/><text x="51" y="73" font-size="13" fill="#58a6ff" text-anchor="start" font-weight="700">權重衰減（L2）</text><text x="41" y="102" font-size="11.8" fill="#e6edf3" text-anchor="start" font-weight="400">損失加 λ‖w‖²</text><text x="41" y="124" font-size="11.8" fill="#9aa4b2" text-anchor="start" font-weight="400">權重被拉向 0，解更平滑</text><text x="41" y="152" font-size="11" fill="#6e7681" text-anchor="start" font-weight="400">最常用的起手式</text><rect x="315" y="44" width="270" height="136" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="329" y="58" width="4" height="18" rx="2" fill="#39d0d8" stroke="none" stroke-width="1.2"/><text x="341" y="73" font-size="13" fill="#39d0d8" text-anchor="start" font-weight="700">L1 稀疏</text><text x="331" y="102" font-size="11.8" fill="#e6edf3" text-anchor="start" font-weight="400">損失加 λ‖w‖₁</text><text x="331" y="124" font-size="11.8" fill="#9aa4b2" text-anchor="start" font-weight="400">不重要的權重被壓成正好 0</text><text x="331" y="152" font-size="11" fill="#6e7681" text-anchor="start" font-weight="400">自帶特徵選擇</text><rect x="605" y="44" width="270" height="136" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="619" y="58" width="4" height="18" rx="2" fill="#3fb950" stroke="none" stroke-width="1.2"/><text x="631" y="73" font-size="13" fill="#3fb950" text-anchor="start" font-weight="700">Dropout</text><text x="621" y="102" font-size="11.8" fill="#e6edf3" text-anchor="start" font-weight="400">訓練時隨機丟掉單元</text><text x="621" y="124" font-size="11.8" fill="#9aa4b2" text-anchor="start" font-weight="400">等於訓練指數多個子網路</text><text x="621" y="152" font-size="11" fill="#6e7681" text-anchor="start" font-weight="400">推論要乘保留機率</text><rect x="25" y="196" width="270" height="136" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="39" y="210" width="4" height="18" rx="2" fill="#d29922" stroke="none" stroke-width="1.2"/><text x="51" y="225" font-size="13" fill="#d29922" text-anchor="start" font-weight="700">早停</text><text x="41" y="254" font-size="11.8" fill="#e6edf3" text-anchor="start" font-weight="400">驗證誤差回升就停</text><text x="41" y="276" font-size="11.8" fill="#9aa4b2" text-anchor="start" font-weight="400">免費、不必改模型</text><text x="41" y="304" font-size="11" fill="#6e7681" text-anchor="start" font-weight="400">代價：要留驗證集</text><rect x="315" y="196" width="270" height="136" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="329" y="210" width="4" height="18" rx="2" fill="#bc8cff" stroke="none" stroke-width="1.2"/><text x="341" y="225" font-size="13" fill="#bc8cff" text-anchor="start" font-weight="700">資料增強</text><text x="331" y="254" font-size="11.8" fill="#e6edf3" text-anchor="start" font-weight="400">翻轉、裁切、加噪</text><text x="331" y="276" font-size="11.8" fill="#9aa4b2" text-anchor="start" font-weight="400">把不變性寫進資料</text><text x="331" y="304" font-size="11" fill="#6e7681" text-anchor="start" font-weight="400">要挑對欄位不變性</text><rect x="605" y="196" width="270" height="136" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="619" y="210" width="4" height="18" rx="2" fill="#ff7b72" stroke="none" stroke-width="1.2"/><text x="631" y="225" font-size="13" fill="#ff7b72" text-anchor="start" font-weight="700">集成／參數共享</text><text x="621" y="254" font-size="11.8" fill="#e6edf3" text-anchor="start" font-weight="400">多模型平均、CNN 共用權</text><text x="621" y="276" font-size="11.8" fill="#9aa4b2" text-anchor="start" font-weight="400">縮小方差，等效正則化</text><text x="621" y="304" font-size="11" fill="#6e7681" text-anchor="start" font-weight="400">用推論成本換穩定</text><text x="450" y="362" font-size="11.8" fill="#6e7681" text-anchor="middle" font-weight="400">選哪一個？先看資料量：資料多 → 弱正則化；資料少 → Dropout ＋ 資料增強優先</text></svg>
<figcaption>圖 7：正則化工具箱：六種壓住過擬合的手段，分別作用在損失、訓練流程與資料三個層面。</figcaption>
</figure>

### 7.1 參數範數懲罰

<div class="eq">L̃(w) = L(w) + α‖w‖₂²　（L2／weight decay）　　L̃(w) = L(w) + α‖w‖₁　（L1）</div>

| 懲罰 | 效果 | 幾何解釋 |
|---|---|---|
| L2 | 權重整體變小、解平滑 | 解落在圓形約束球上 |
| L1 | 部分權重正好為 0 | 解落在菱形約束的頂點（稀疏） |

書中一個很重要的提醒：<strong>L2 在最佳點附近會讓有效學習率下降</strong>，所以「加了 weight decay 之後要重調學習率」。

### 7.2 資料面與結構面的正則化

| 手段 | 機制 | 什麼時候用 |
|---|---|---|
| 資料增強 | 把已知的不變性寫進資料 | 影像（翻轉裁切）、語音（時間拉伸） |
| 雜訊注入 | 輸入加噪＝對權重的平滑性約束 | 小資料集、容易過擬合的模型 |
| 早停 | 在驗證誤差回升時停 | 幾乎永遠該做，成本最低 |
| 參數共享 | 同一組權重用在多處（CNN、RNN） | 有結構先驗時 |
| Dropout | 訓練時隨機丟單元 | 全連接層多、資料少 |
| 集成 | 多模型平均 | 推論預算寬鬆時 |
| 對抗訓練 | 對輸入的微小擾動保持穩定 | 需要魯棒性時 |

### 7.3 Dropout 的三個實務細節

1. 訓練時以機率 `p` 保留單元，推論時<strong>要乘上 `p`</strong>（或訓練時就做 inverted dropout）
2. 它近似「同時訓練指數多個共享權重的子網路」，所以是集成的一種便宜替代
3. 與 BatchNorm 一起用時要小心順序（通常是 conv → norm → activation → dropout）

> <strong>章末考點</strong>：L1 與 L2 的幾何差異、為什麼早停等於一種正則化、Dropout 推論時為什麼要縮放。

---

## 8　訓練的最佳化：為什麼深度網路難訓練

### 一句話

<strong>深度學習的最佳化困難，來自「地貌」而不是「演算法不夠好」。</strong>

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 372" width="100%" role="img" aria-label="梯度下降：同一個碗，三種學習率" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:900px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="grad-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><text x="450" y="26" font-size="13.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">同一個碗、同一個起點，只改學習率 η</text><text x="160" y="52" font-size="13" fill="#58a6ff" text-anchor="middle" font-weight="700">η 太小</text><rect x="25" y="64" width="270" height="240" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><path d="M52,162 Q160,276.7 268,162" fill="none" stroke="#6e7681" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="264.76" cy="166.373" r="5.4" fill="#58a6ff" stroke="#0d1117" stroke-width="1.4"/><circle cx="261.52" cy="170.614" r="5.4" fill="#58a6ff" stroke="#0d1117" stroke-width="1.4"/><circle cx="257.2" cy="176.06" r="5.4" fill="#58a6ff" stroke="#0d1117" stroke-width="1.4"/><circle cx="251.8" cy="182.535" r="5.4" fill="#58a6ff" stroke="#0d1117" stroke-width="1.4"/><circle cx="245.32" cy="189.817" r="5.4" fill="#58a6ff" stroke="#0d1117" stroke-width="1.4"/><circle cx="237.76" cy="197.638" r="5.4" fill="#58a6ff" stroke="#0d1117" stroke-width="1.4"/><circle cx="229.12" cy="205.69" r="5.4" fill="#58a6ff" stroke="#0d1117" stroke-width="1.4"/><text x="160" y="272" font-size="11.2" fill="#9aa4b2" text-anchor="middle" font-weight="400">走得很穩，但 500 步還在半路</text><text x="450" y="52" font-size="13" fill="#3fb950" text-anchor="middle" font-weight="700">η 剛好</text><rect x="315" y="64" width="270" height="240" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><path d="M342,162 Q450,276.7 558,162" fill="none" stroke="#6e7681" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="554.76" cy="166.373" r="5.4" fill="#3fb950" stroke="#0d1117" stroke-width="1.4"/><circle cx="516.96" cy="207.554" r="5.4" fill="#3fb950" stroke="#0d1117" stroke-width="1.4"/><circle cx="486.72" cy="227.446" r="5.4" fill="#3fb950" stroke="#0d1117" stroke-width="1.4"/><circle cx="467.28" cy="234.106" r="5.4" fill="#3fb950" stroke="#0d1117" stroke-width="1.4"/><circle cx="456.48" cy="235.734" r="5.4" fill="#3fb950" stroke="#0d1117" stroke-width="1.4"/><circle cx="451.08" cy="235.993" r="5.4" fill="#3fb950" stroke="#0d1117" stroke-width="1.4"/><text x="450" y="272" font-size="11.2" fill="#9aa4b2" text-anchor="middle" font-weight="400">誤差單調下降，最後停在谷底</text><text x="740" y="52" font-size="13" fill="#ff7b72" text-anchor="middle" font-weight="700">η 太大</text><rect x="605" y="64" width="270" height="240" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><path d="M632,162 Q740,276.7 848,162" fill="none" stroke="#6e7681" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="844.76" cy="166.373" r="5.4" fill="#ff7b72" stroke="#0d1117" stroke-width="1.4"/><circle cx="644.96" cy="178.694" r="5.4" fill="#ff7b72" stroke="#0d1117" stroke-width="1.4"/><circle cx="822.08" cy="193.258" r="5.4" fill="#ff7b72" stroke="#0d1117" stroke-width="1.4"/><circle cx="673.04" cy="207.554" r="5.4" fill="#ff7b72" stroke="#0d1117" stroke-width="1.4"/><circle cx="790.76" cy="219.653" r="5.4" fill="#ff7b72" stroke="#0d1117" stroke-width="1.4"/><circle cx="704.36" cy="227.941" r="5.4" fill="#ff7b72" stroke="#0d1117" stroke-width="1.4"/><text x="740" y="272" font-size="11.2" fill="#9aa4b2" text-anchor="middle" font-weight="400">跨過谷底、來回彈跳，甚至發散</text><text x="450" y="352" font-size="11.8" fill="#6e7681" text-anchor="middle" font-weight="400">實務上不會直接猜 η：動量、RMSProp、Adam 都是在「自動調步伐」（第 8 章）</text></svg>
<figcaption>圖 8：梯度下降與學習率：同一個碗、同一個起點，η 太小走太慢、太大會跨過谷底。</figcaption>
</figure>

### 8.1 四種地貌問題

| 問題 | 長相 | 後果 |
|---|---|---|
| 病態（ill-conditioning） | 一個方向很陡、另一個很平 | 學習率怎麼調都不對：陡的爆、平的慢 |
| 局部極小 | 四周都比它高 | 高維下其實罕見，而且通常已經夠好 |
| 鞍點 | 一個方向上升、一個方向下降 | <strong>高維的真正殺手</strong>：梯度接近 0，但不是解 |
| 懸崖（cliff） | 誤差曲面突然垂直下墜 | 一步跨太大就「彈飛」，權重全毀 |

### 8.2 從 SGD 到 Adam：一條演化線

| 方法 | 關鍵想法 | 代價 |
|---|---|---|
| SGD | 用 minibatch 估梯度 | 對學習率極敏感 |
| 動量 momentum | 累積過去的方向，抑制震盪 | 多一個超參數 β |
| Nesterov | 先「看一步」再算梯度 | 收斂略快 |
| AdaGrad | 每個參數有自己的學習率（除以歷史梯度平方和） | 學習率單調衰減，後期幾乎不動 |
| RMSProp | 用移動平均修掉 AdaGrad 的衰減 | 好調，實務常用 |
| Adam | 動量 ＋ RMSProp ＋ 偏差修正 | 預設首選，但泛化有時略差 |

### 8.3 初始化：不是細節，是能不能開始訓練

<div class="eq">Xavier／Glorot：Var(w) = 2 / (n<sub>in</sub> + n<sub>out</sub>)</div>
<div class="eq">He／Kaiming（配 ReLU）：Var(w) = 2 / n<sub>in</sub></div>

理由只有一個：**保持每一層的變異數不變**，否則 50 層之後訊號會爆掉或消失。偏差 `b` 通常初始化為 0。

### 8.4 BatchNorm 的真正作用

書中把它放在「最佳化」章而不是「正則化」章，理由是：<strong>它主要解決的是「訓練不穩定」，不是「過擬合」</strong>。把每層輸入重新標準化，等於讓每個參數看到的尺度穩定，允許更大的學習率。

> <strong>章末考點</strong>：鞍點與局部極小的區別、為什麼 Adam 一開始要偏差修正、初始化公式裡的 `n_in`／`n_out` 各代表什麼。

---

## 9　卷積網路：把影像的先驗寫進架構

### 一句話

<strong>卷積不是「更強的層」，而是「把三個先驗寫進權重」：局部性、平移等變性、參數共享。</strong>

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 424" width="100%" role="img" aria-label="卷積：局部連接與參數共享" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:900px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="conv-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><text x="450" y="26" font-size="13.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">同一組 9 個權重，掃過輸入的每一個 3×3 鄰域</text><text x="142" y="54" font-size="11.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">輸入 6×6</text><rect x="40" y="66" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="74" y="66" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="108" y="66" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="142" y="66" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="176" y="66" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="210" y="66" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="40" y="100" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="74" y="100" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="108" y="100" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="142" y="100" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="176" y="100" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="210" y="100" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="40" y="134" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="74" y="134" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="108" y="134" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="142" y="134" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="176" y="134" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="210" y="134" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="40" y="168" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="74" y="168" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="108" y="168" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="142" y="168" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="176" y="168" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="210" y="168" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="40" y="202" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="74" y="202" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="108" y="202" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="142" y="202" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="176" y="202" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="210" y="202" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="40" y="236" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="74" y="236" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="108" y="236" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="142" y="236" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="176" y="236" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="210" y="236" width="30" height="30" rx="4" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><rect x="38" y="64" width="102" height="102" fill="none" stroke="#d29922" stroke-width="2.4" rx="6"/><text x="322" y="54" font-size="11.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">濾波器 3×3（9 個權重）</text><rect x="292" y="66" width="26" height="26" rx="4" fill="#1c2430" stroke="#d29922" stroke-width="1.2"/><text x="305" y="84" font-size="11" fill="#d29922" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">1</text><rect x="322" y="66" width="26" height="26" rx="4" fill="#1c2430" stroke="#d29922" stroke-width="1.2"/><text x="335" y="84" font-size="11" fill="#d29922" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">0</text><rect x="352" y="66" width="26" height="26" rx="4" fill="#1c2430" stroke="#d29922" stroke-width="1.2"/><text x="365" y="84" font-size="11" fill="#d29922" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">-1</text><rect x="292" y="96" width="26" height="26" rx="4" fill="#1c2430" stroke="#d29922" stroke-width="1.2"/><text x="305" y="114" font-size="11" fill="#d29922" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">2</text><rect x="322" y="96" width="26" height="26" rx="4" fill="#1c2430" stroke="#d29922" stroke-width="1.2"/><text x="335" y="114" font-size="11" fill="#d29922" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">0</text><rect x="352" y="96" width="26" height="26" rx="4" fill="#1c2430" stroke="#d29922" stroke-width="1.2"/><text x="365" y="114" font-size="11" fill="#d29922" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">-2</text><rect x="292" y="126" width="26" height="26" rx="4" fill="#1c2430" stroke="#d29922" stroke-width="1.2"/><text x="305" y="144" font-size="11" fill="#d29922" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">1</text><rect x="322" y="126" width="26" height="26" rx="4" fill="#1c2430" stroke="#d29922" stroke-width="1.2"/><text x="335" y="144" font-size="11" fill="#d29922" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">0</text><rect x="352" y="126" width="26" height="26" rx="4" fill="#1c2430" stroke="#d29922" stroke-width="1.2"/><text x="365" y="144" font-size="11" fill="#d29922" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">-1</text><text x="492" y="54" font-size="11.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">輸出 4×4</text><rect x="470" y="66" width="30" height="30" rx="4" fill="#39d0d8" stroke="#30363d" stroke-width="1.2"/><rect x="504" y="66" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="538" y="66" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="572" y="66" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="470" y="100" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="504" y="100" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="538" y="100" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="572" y="100" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="470" y="134" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="504" y="134" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="538" y="134" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="572" y="134" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="470" y="168" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="504" y="168" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="538" y="168" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><rect x="572" y="168" width="30" height="30" rx="4" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><line x1="250" y1="115" x2="284" y2="115" stroke="#30363d" stroke-width="2" stroke-linecap="round" marker-end="url(#cv-ar)"/><line x1="394" y1="115" x2="462" y2="115" stroke="#30363d" stroke-width="2" stroke-linecap="round" marker-end="url(#cv-ar)"/><rect x="666" y="66" width="208" height="102" rx="10" fill="#1c2430" stroke="#30363d" stroke-width="1.2"/><text x="678" y="88" font-size="12" fill="#39d0d8" text-anchor="start" font-weight="700">參數共享</text><text x="678" y="110" font-size="11" fill="#e6edf3" text-anchor="start" font-weight="400">9 個權重 → 整張圖</text><text x="678" y="130" font-size="11" fill="#9aa4b2" text-anchor="start" font-weight="400">全連接要 6×6×4×4 = 576</text><text x="678" y="150" font-size="11" fill="#9aa4b2" text-anchor="start" font-weight="400">卷積只要 9（差 64 倍）</text><circle cx="42" cy="314" r="3" fill="#39d0d8" stroke="none" stroke-width="1.4"/><text x="56" y="318" font-size="11.8" fill="#9aa4b2" text-anchor="start" font-weight="400">局部連接：每個輸出只看 3×3 的鄰域 —— 影像的相關性本來就是局部的</text><circle cx="42" cy="340" r="3" fill="#39d0d8" stroke="none" stroke-width="1.4"/><text x="56" y="344" font-size="11.8" fill="#9aa4b2" text-anchor="start" font-weight="400">參數共享：同一個濾波器掃過全圖 —— 貓在左上或右下都是貓</text><circle cx="42" cy="366" r="3" fill="#39d0d8" stroke="none" stroke-width="1.4"/><text x="56" y="370" font-size="11.8" fill="#9aa4b2" text-anchor="start" font-weight="400">平移等變性：輸入平移一格，輸出特徵也平移一格（不是不變，是等變）</text></svg>
<figcaption>圖 9：卷積的局部連接與參數共享：同一組 9 個權重掃過整張輸入，參數量比全連接少幾十倍。</figcaption>
</figure>

### 9.1 三個先驗，三個好處

| 先驗 | 機制 | 好處 |
|---|---|---|
| 局部性 | 每個輸出只看 k×k 鄰域 | 參數大減、符合影像統計 |
| 平移等變性 | 同一濾波器掃全圖 | 貓在左上或右下都能辨識 |
| 多通道共享 | 同一組權重用於整個空間 | 樣本效率大幅提升 |

### 9.2 輸出尺寸與參數量（面試最常考）

<div class="eq">輸出邊長 = ⌊(W − K + 2P) / S⌋ + 1</div>
<div class="eq">卷積層參數量 = K × K × C<sub>in</sub> × C<sub>out</sub> + C<sub>out</sub></div>

以 3×3、C_in=64、C_out=128 為例：`3×3×64×128 + 128 = 73,856` 個參數。若換成全連接（輸入 32×32×64），參數量會多出三個數量級。

### 9.3 池化與「不變」的層次

- **池化**（max／average）給的是**局部平移不變**，代價是丟掉位置資訊
- 想保留位置 → 用 stride 卷積（learned pooling）取代固定池化
- **膨脹卷積（dilated）**：在不大幅增加參數下擴大感受野，常用於語意分割

### 9.4 卷積的三種等價視角

1. **訊號處理**：卷積是濾波（真正的數學卷積是翻轉後滑動）
2. **稀疏矩陣乘法**：把卷積寫成一個巨大但稀疏的 Toeplitz 矩陣
3. **參數共享的全連接**：每個輸出單元共用同一組權重

三種看法在實作上分別對應 FFT 卷積、im2col＋GEMM、cuDNN 的隱式 GEMM——這也是第 12 章「大規模深度學習」的技術底層。

---

## 10　序列模型：RNN 與長期依賴

### 一句話

<strong>RNN 把「深度」放在時間軸上，於是它同時得到參數共享與梯度消失。</strong>

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 396" width="100%" role="img" aria-label="RNN 的展開圖與長期依賴問題" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:900px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="rnn-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><text x="450" y="26" font-size="13.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">把「時間」攤平成一條鏈：同一組權重，重複使用</text><rect x="99" y="52" width="52" height="22" rx="11" fill="#1c2430" stroke="none" stroke-width="1.2"/><text x="125" y="66.96" font-size="11" fill="#3fb950" text-anchor="middle" font-weight="600">y₁</text><rect x="50" y="84" width="150" height="76" rx="10" fill="#161b22" stroke="#39d0d8" stroke-width="1.2"/><text x="125" y="116" font-size="15" fill="#39d0d8" text-anchor="middle" font-weight="700">h₁</text><text x="125" y="140" font-size="10.5" fill="#6e7681" text-anchor="middle" font-weight="400">同一組 W</text><rect x="99" y="168" width="52" height="22" rx="11" fill="#1c2430" stroke="none" stroke-width="1.2"/><text x="125" y="182.96" font-size="11" fill="#58a6ff" text-anchor="middle" font-weight="600">x₁</text><line x1="125" y1="74" x2="125" y2="82" stroke="#30363d" stroke-width="1.4" stroke-linecap="round" marker-end="url(#rnn-ar)"/><line x1="125" y1="162" x2="125" y2="160" stroke="#30363d" stroke-width="1.4" stroke-linecap="round" marker-end="url(#rnn-ar)"/><line x1="202" y1="122" x2="248" y2="122" stroke="#30363d" stroke-width="1.4" stroke-linecap="round" marker-end="url(#rnn-ar)"/><rect x="299" y="52" width="52" height="22" rx="11" fill="#1c2430" stroke="none" stroke-width="1.2"/><text x="325" y="66.96" font-size="11" fill="#3fb950" text-anchor="middle" font-weight="600">y₂</text><rect x="250" y="84" width="150" height="76" rx="10" fill="#161b22" stroke="#39d0d8" stroke-width="1.2"/><text x="325" y="116" font-size="15" fill="#39d0d8" text-anchor="middle" font-weight="700">h₂</text><text x="325" y="140" font-size="10.5" fill="#6e7681" text-anchor="middle" font-weight="400">同一組 W</text><rect x="299" y="168" width="52" height="22" rx="11" fill="#1c2430" stroke="none" stroke-width="1.2"/><text x="325" y="182.96" font-size="11" fill="#58a6ff" text-anchor="middle" font-weight="600">x₂</text><line x1="325" y1="74" x2="325" y2="82" stroke="#30363d" stroke-width="1.4" stroke-linecap="round" marker-end="url(#rnn-ar)"/><line x1="325" y1="162" x2="325" y2="160" stroke="#30363d" stroke-width="1.4" stroke-linecap="round" marker-end="url(#rnn-ar)"/><line x1="402" y1="122" x2="448" y2="122" stroke="#30363d" stroke-width="1.4" stroke-linecap="round" marker-end="url(#rnn-ar)"/><rect x="499" y="52" width="52" height="22" rx="11" fill="#1c2430" stroke="none" stroke-width="1.2"/><text x="525" y="66.96" font-size="11" fill="#3fb950" text-anchor="middle" font-weight="600">y₃</text><rect x="450" y="84" width="150" height="76" rx="10" fill="#161b22" stroke="#39d0d8" stroke-width="1.2"/><text x="525" y="116" font-size="15" fill="#39d0d8" text-anchor="middle" font-weight="700">h₃</text><text x="525" y="140" font-size="10.5" fill="#6e7681" text-anchor="middle" font-weight="400">同一組 W</text><rect x="499" y="168" width="52" height="22" rx="11" fill="#1c2430" stroke="none" stroke-width="1.2"/><text x="525" y="182.96" font-size="11" fill="#58a6ff" text-anchor="middle" font-weight="600">x₃</text><line x1="525" y1="74" x2="525" y2="82" stroke="#30363d" stroke-width="1.4" stroke-linecap="round" marker-end="url(#rnn-ar)"/><line x1="525" y1="162" x2="525" y2="160" stroke="#30363d" stroke-width="1.4" stroke-linecap="round" marker-end="url(#rnn-ar)"/><line x1="602" y1="122" x2="648" y2="122" stroke="#30363d" stroke-width="1.4" stroke-linecap="round" marker-end="url(#rnn-ar)"/><rect x="699" y="52" width="52" height="22" rx="11" fill="#1c2430" stroke="none" stroke-width="1.2"/><text x="725" y="66.96" font-size="11" fill="#3fb950" text-anchor="middle" font-weight="600">y₄</text><rect x="650" y="84" width="150" height="76" rx="10" fill="#161b22" stroke="#39d0d8" stroke-width="1.2"/><text x="725" y="116" font-size="15" fill="#39d0d8" text-anchor="middle" font-weight="700">h₄</text><text x="725" y="140" font-size="10.5" fill="#6e7681" text-anchor="middle" font-weight="400">同一組 W</text><rect x="699" y="168" width="52" height="22" rx="11" fill="#1c2430" stroke="none" stroke-width="1.2"/><text x="725" y="182.96" font-size="11" fill="#58a6ff" text-anchor="middle" font-weight="600">x₄</text><line x1="725" y1="74" x2="725" y2="82" stroke="#30363d" stroke-width="1.4" stroke-linecap="round" marker-end="url(#rnn-ar)"/><line x1="725" y1="162" x2="725" y2="160" stroke="#30363d" stroke-width="1.4" stroke-linecap="round" marker-end="url(#rnn-ar)"/><text x="450" y="206" font-size="11.5" fill="#6e7681" text-anchor="middle" font-weight="400">展開後就是一個很深的網路：同一條權重被乘了很多次</text><rect x="25" y="220" width="408" height="132" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="41" y="244" font-size="12" fill="#ff7b72" text-anchor="start" font-weight="700">梯度消失：連乘讓訊號衰減</text><rect x="48" y="268" width="30" height="58" rx="4" fill="#ff7b72" stroke="none" stroke-width="1.2"/><rect x="88" y="283" width="30" height="43" rx="4" fill="#ff7b72" stroke="none" stroke-width="1.2"/><rect x="128" y="295" width="30" height="31" rx="4" fill="#ff7b72" stroke="none" stroke-width="1.2"/><rect x="168" y="304" width="30" height="22" rx="4" fill="#ff7b72" stroke="none" stroke-width="1.2"/><text x="48" y="344" font-size="10" fill="#6e7681" text-anchor="start" font-weight="400">t−4　　t−3　　t−2　　t−1</text><text x="214" y="262" font-size="11" fill="#9aa4b2" text-anchor="start" font-weight="400">每往回一層就乘一次 Jacobian</text><text x="214" y="282" font-size="11" fill="#e6edf3" text-anchor="start" font-weight="400">特徵值 &lt; 1 → 消失</text><text x="214" y="302" font-size="11" fill="#e6edf3" text-anchor="start" font-weight="400">特徵值 &gt; 1 → 爆炸（用 clip 擋）</text><rect x="455" y="220" width="420" height="132" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="471" y="244" font-size="12" fill="#3fb950" text-anchor="start" font-weight="700">LSTM／GRU：用閘門開一條加法捷徑</text><rect x="474" y="258" width="96" height="24" rx="12" fill="#1c2430" stroke="none" stroke-width="1.2"/><text x="522" y="273.96" font-size="11" fill="#d29922" text-anchor="middle" font-weight="600">遺忘閘 f</text><rect x="582" y="258" width="96" height="24" rx="12" fill="#1c2430" stroke="none" stroke-width="1.2"/><text x="630" y="273.96" font-size="11" fill="#d29922" text-anchor="middle" font-weight="600">輸入閘 i</text><rect x="690" y="258" width="96" height="24" rx="12" fill="#1c2430" stroke="none" stroke-width="1.2"/><text x="738" y="273.96" font-size="11" fill="#d29922" text-anchor="middle" font-weight="600">輸出閘 o</text><text x="474" y="306" font-size="11" fill="#e6edf3" text-anchor="start" font-weight="400">cell state 走加法：C_t = f·C_{t−1} + i·g</text><text x="474" y="328" font-size="11" fill="#9aa4b2" text-anchor="start" font-weight="400">梯度沿加法路徑直通，不必連乘（第 10 章）</text></svg>
<figcaption>圖 10：RNN 展開後是一條很深的鏈；梯度沿時間連乘會消失，LSTM 用加法路徑與三個閘門繞開它。</figcaption>
</figure>

### 10.1 展開圖：一個網路，四個時間點

`hₜ = f(hₜ₋₁, xₜ; W)` —— 同一組 `W` 重複使用。展開後就是一個**權重綁定的深網路**，深度 = 時間步數。

### 10.2 為什麼梯度會消失／爆炸

反向傳播時，梯度要連乘每一個時間步的 Jacobian `∂hₜ/∂hₜ₋₁`。若它的奇異值 < 1，乘 50 次就變 0；> 1 就變 inf。

| 症狀 | 解法 |
|---|---|
| 梯度爆炸 | 梯度裁剪（clip by norm）、更小的學習率 |
| 梯度消失 | LSTM／GRU 的加法捷徑、skip connection、門控 |

### 10.3 LSTM 的三個閘門

| 閘門 | 作用 |
|---|---|
| 遺忘閘 f | 決定舊的 cell state 要留多少 |
| 輸入閘 i | 決定新的候選值要寫多少 |
| 輸出閘 o | 決定要輸出多少給 hidden state |

關鍵在 `Cₜ = f ⊙ Cₜ₋₁ + i ⊙ g`：**加法那條路徑讓梯度直通**，不必每層連乘。GRU 把它簡化成兩個閘門（更新、重置），參數更少、效果接近。

### 10.4 其他「記得更久」的辦法

- **ESN（回聲狀態網路）**：只訓練輸出層，內部權重固定
- **leaky unit／skip connection**：讓部分狀態直接跳過幾步
- **記憶增強（memory-augmented）**：外部記憶矩陣，可讀可寫
- **深度 RNN**：堆疊多層，不同層學不同時間尺度

> <strong>章末考點</strong>：BPTT 與普通反向傳播的差別、梯度裁剪為什麼只裁範數不裁方向、LSTM 為什麼能緩解（不是「解決」）梯度消失。

---

## 11　實務方法論：把模型做到能用

### 一句話

<strong>大多數「模型不夠好」其實是「流程不夠好」：先確認指標、再量基準、最後才調超參數。</strong>

### 11.1 四步決策流程

1. **決定指標**：用什麼數字判斷成功？(準確率不夠 → 用 F1／AUC／per-class recall)
2. **建立端到端基準**：先做一個最笨但完整的系統（含部署與評估），再逐段改進
3. **判斷瓶頸**：是資料不夠、模型不夠、還是訓練不夠？（用學習曲線分辨）
4. **再調超參數**：只有前三步都確認過，調參才有意義

### 11.2 學習曲線怎麼讀

| 曲線形狀 | 診斷 | 該做什麼 |
|---|---|---|
| 訓練誤差一直高 | 欠擬合 | 加大模型、訓練更久、更好的特徵 |
| 訓練低、驗證高且差距大 | 過擬合 | 更多資料、正則化 |
| 兩條都低但驗證卡住 | 分布不匹配 | 檢查切分與資料收集方式 |
| 驗證誤差比訓練誤差還低 | 驗證集太小或洩漏 | 重切資料集 |

### 11.3 超參數搜尋

| 方法 | 什麼時候用 |
|---|---|
| 手動 | 只有 1–2 個關鍵超參數（例如學習率） |
| 網格 | 維度 ≤ 3，且每個維度取值少 |
| 隨機搜尋 | <strong>預設首選</strong>：同樣預算下通常優於網格 |
| 貝氏最佳化 | 每次訓練很貴（幾小時以上）時值得 |

### 11.4 除錯的四個動作

1. **視覺化**：把輸入、預測、錯誤案例畫出來（大部分 bug 一眼就看得出來）
2. **找最差案例**：不是平均最差，而是單筆最離譜的那些
3. **單位測試**：梯度檢查、形狀檢查、小資料集能否過擬合（<strong>能過擬合 10 筆資料，才證明模型沒有寫錯</strong>）
4. **監控訓練曲線**：損失、梯度範數、參數更新比例

> <strong>章末考點</strong>：為什麼「先用小資料集確認能過擬合」是最有效的除錯手段、隨機搜尋為何優於網格。

---

## 12　應用：規模帶來的質變

### 一句話

<strong>當資料與算力放大兩個數量級，同一套演算法會出現新的行為——這不是行銷詞，是第 1 章就埋下的論點。</strong>

### 12.1 大規模訓練的三個工程支柱

| 支柱 | 內容 |
|---|---|
| 資料平行 | 每個 GPU 吃不同 batch，梯度 AllReduce |
| 模型平行 | 一層放不下 → 切層、切張量 |
| 混合精度 | FP16／BF16 前向 ＋ FP32 主權重 |

### 12.2 四個領域的共同模式

| 領域 | 關鍵歸納偏誤 | 代表架構 |
|---|---|---|
| 電腦視覺 | 局部性、平移等變性 | CNN、ResNet |
| 語音辨識 | 時間平移、頻譜局部性 | 卷積＋RNN、CTC |
| 自然語言 | 長距離依賴、序列順序 | RNN、注意力、Transformer |
| 多模態 | 跨模態對齊 | 對比學習（CLIP 類） |

### 12.3 書中沒說、但現在必須知道的

2016 年的原文沒有 Transformer、沒有擴散模型。但書中的判準仍然適用：

- **先問「這個任務的不變性是什麼」**，再選架構
- **先問「推論預算是多少」**，再決定模型大小
- **先問「資料怎麼來的」**，再談模型改進

> <strong>章末考點</strong>：為什麼 CNN 的參數共享在小資料上特別有效、CTC 解決了什麼對齊問題。

---

## 13　線性因子模型：解開潛在變數

### 一句話

<strong>線性因子模型假設「看得到的 x」是「看不到的 h」經過線性混合再加上噪聲。</strong>

<div class="eq">x = W h + b + noise</div>

### 13.1 四個成員

| 模型 | 對 h 的假設 | 用途 |
|---|---|---|
| 機率 PCA | h ∼ Gaussian | 降維、可解釋方向 |
| 獨立成分分析 ICA | h 各維獨立且非高斯 | 盲源分離（雞尾酒會問題） |
| 慢特徵分析 SFA | h 隨時間變化慢 | 影片、時序特徵 |
| 稀疏編碼 | h 稀疏 | 學過完備字典 |

### 13.2 為什麼要先講線性

因為它<strong>可以解析求解</strong>：PCA 的解就是共變異數矩陣的特徵向量，ICA 的解可以透過最大化非高斯性得到。先看懂「有解析解的版本」，才知道第 14 章的非線性版本（自編碼器）到底多付了什麼代價。

---

## 14　自編碼器：學一個夠用的瓶頸

### 一句話

<strong>自編碼器 = 編碼器 ＋ 瓶頸 ＋ 解碼器，目標是「重建自己」；瓶頸逼它只留下重要資訊。</strong>

### 14.1 六種變體

| 變體 | 加了什麼約束 | 學到什麼 |
|---|---|---|
| 欠完備 | 瓶頸維度 < 輸入維度 | PCA 的非線性推廣 |
| 正則化（weight decay） | 權重小 | 平滑的表示 |
| 稀疏 | 編碼大部分為 0 | 局部、可組合的特徵 |
| 去噪 | 輸入加噪，重建乾淨版 | 學到資料流形（重要） |
| 收縮 | 對輸入擾動不敏感 | 穩定的表示 |
| 變分 VAE | 編碼輸出分布 | 可生成新樣本（第 20 章） |

### 14.2 為什麼去噪自編碼器最重要

「從加噪的輸入重建乾淨的輸入」逼模型學到**資料所在的流形**，而不是記住每個樣本。這條思路一路通向後來的擴散模型（第 20 章末尾的生成模型評估也在談同一件事）。

> <strong>章末考點</strong>：欠完備與稀疏的差別、去噪自編碼器為什麼能學到流形、VAE 與普通自編碼器的目標差異。

---

## 15　表徵學習：什麼是好特徵

### 一句話

<strong>好表示 = 能讓下游任務變成「簡單函數」的表示。</strong>

### 15.1 好表示的四個條件

| 條件 | 意思 |
|---|---|
| 平滑 | 輸入小變動，表示也只小變動 |
| 多因子可分 | 不同解釋因子佔用不同的方向 |
| 稀疏／分散 | 一個概念由少數單元或少數方向表示 |
| 層次化 | 低層語法、高層語意 |

### 15.2 三個重要論點

1. **貪婪逐層無監督預訓練**：在標註資料稀缺的年代，這是讓深網路能訓練起來的關鍵；現在多半被更好的初始化與正則化取代。
2. **遷移學習與領域自適應**：表徵可重用，是因為「底層特徵」跨任務共享。
3. **深度的指數增益**：某些函數用深網路表達只需線性成長的參數，淺網路則需要指數成長——這是全書對「為什麼要深」最強的理論回答。

---

## 16　結構化機率模型：用圖約束機率

### 一句話

<strong>用圖宣告「誰和誰直接相關」，就能用少得多的參數描述一個高維分布。</strong>

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 336" width="100%" role="img" aria-label="三種用圖描述機率模型的方式" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:900px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="pgm-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><text x="450" y="26" font-size="13.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">圖 = 條件獨立性的宣告；邊 = 誰可以直接影響誰</text><rect x="25" y="44" width="270" height="244" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="160" y="68" font-size="11.8" fill="#58a6ff" text-anchor="middle" font-weight="700">有向圖（貝氏網路）</text><rect x="315" y="44" width="270" height="244" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="450" y="68" font-size="11.8" fill="#d29922" text-anchor="middle" font-weight="700">無向圖（馬可夫隨機場）</text><rect x="605" y="44" width="270" height="244" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="740" y="68" font-size="11.8" fill="#bc8cff" text-anchor="middle" font-weight="700">兩層的 RBM</text><line x1="149" y1="124" x2="110" y2="164" stroke="#30363d" stroke-width="1.8" stroke-linecap="round" marker-end="url(#pg1-ar)"/><line x1="171" y1="124" x2="210" y2="164" stroke="#30363d" stroke-width="1.8" stroke-linecap="round" marker-end="url(#pg1-ar)"/><line x1="114" y1="178" x2="190" y2="178" stroke="#30363d" stroke-width="1.8" stroke-linecap="round" marker-end="url(#pg1-ar)"/><circle cx="160" cy="112" r="16" fill="#1c2430" stroke="#58a6ff" stroke-width="1.4"/><text x="160" y="116" font-size="12" fill="#e6edf3" text-anchor="middle" font-weight="700">a</text><circle cx="98" cy="178" r="16" fill="#1c2430" stroke="#58a6ff" stroke-width="1.4"/><text x="98" y="182" font-size="12" fill="#e6edf3" text-anchor="middle" font-weight="700">b</text><circle cx="222" cy="178" r="16" fill="#1c2430" stroke="#58a6ff" stroke-width="1.4"/><text x="222" y="182" font-size="12" fill="#e6edf3" text-anchor="middle" font-weight="700">c</text><text x="160" y="224" font-size="10.5" fill="#9aa4b2" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">p(a, b, c) = p(a) p(b|a) p(c|a, b)</text><text x="160" y="246" font-size="10.8" fill="#6e7681" text-anchor="middle" font-weight="400">每個節點一個條件分布</text><text x="160" y="266" font-size="10.8" fill="#6e7681" text-anchor="middle" font-weight="400">取樣要照拓樸順序</text><polygon points="450,112 388,178 512,178" fill="#d29922" opacity="0.16"/><line x1="450" y1="112" x2="388" y2="178" stroke="#d29922" stroke-width="1.6" stroke-linecap="round"/><line x1="450" y1="112" x2="512" y2="178" stroke="#d29922" stroke-width="1.6" stroke-linecap="round"/><line x1="388" y1="178" x2="512" y2="178" stroke="#d29922" stroke-width="1.6" stroke-linecap="round"/><circle cx="450" cy="112" r="16" fill="#1c2430" stroke="#d29922" stroke-width="1.4"/><text x="450" y="116" font-size="12" fill="#e6edf3" text-anchor="middle" font-weight="700">a</text><circle cx="388" cy="178" r="16" fill="#1c2430" stroke="#d29922" stroke-width="1.4"/><text x="388" y="182" font-size="12" fill="#e6edf3" text-anchor="middle" font-weight="700">b</text><circle cx="512" cy="178" r="16" fill="#1c2430" stroke="#d29922" stroke-width="1.4"/><text x="512" y="182" font-size="12" fill="#e6edf3" text-anchor="middle" font-weight="700">c</text><text x="450" y="224" font-size="10.5" fill="#9aa4b2" text-anchor="middle" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">p(a, b, c) = ψ(a,b) ψ(a,c) ψ(b,c) / Z</text><text x="450" y="246" font-size="10.8" fill="#6e7681" text-anchor="middle" font-weight="400">沒有方向，只有相容性</text><text x="450" y="266" font-size="10.8" fill="#6e7681" text-anchor="middle" font-weight="400">Z 就是配分函數（第 18 章）</text><line x1="674" y1="128" x2="706" y2="170" stroke="#bc8cff" stroke-width="1.1" stroke-linecap="round"/><line x1="674" y1="128" x2="774" y2="170" stroke="#bc8cff" stroke-width="1.1" stroke-linecap="round"/><line x1="740" y1="128" x2="706" y2="170" stroke="#bc8cff" stroke-width="1.1" stroke-linecap="round"/><line x1="740" y1="128" x2="774" y2="170" stroke="#bc8cff" stroke-width="1.1" stroke-linecap="round"/><line x1="806" y1="128" x2="706" y2="170" stroke="#bc8cff" stroke-width="1.1" stroke-linecap="round"/><line x1="806" y1="128" x2="774" y2="170" stroke="#bc8cff" stroke-width="1.1" stroke-linecap="round"/><circle cx="674" cy="112" r="14" fill="#1c2430" stroke="#bc8cff" stroke-width="1.4"/><circle cx="740" cy="112" r="14" fill="#1c2430" stroke="#bc8cff" stroke-width="1.4"/><circle cx="806" cy="112" r="14" fill="#1c2430" stroke="#bc8cff" stroke-width="1.4"/><circle cx="706" cy="186" r="14" fill="#1c2430" stroke="#bc8cff" stroke-width="1.4"/><circle cx="774" cy="186" r="14" fill="#1c2430" stroke="#bc8cff" stroke-width="1.4"/><text x="740" y="84" font-size="10.5" fill="#6e7681" text-anchor="middle" font-weight="400">隱藏層 h</text><text x="740" y="214" font-size="10.5" fill="#6e7681" text-anchor="middle" font-weight="400">可見層 v</text><text x="740" y="244" font-size="10.5" fill="#9aa4b2" text-anchor="middle" font-weight="400">同層不相連 → 給定一層，另一層就條件獨立</text><text x="740" y="268" font-size="10.8" fill="#6e7681" text-anchor="middle" font-weight="400">所以可以整層平行取樣</text></svg>
<figcaption>圖 11：三種用圖描述機率模型的方式：有向圖（可算似然）、無向圖（要面對 Z）、兩層 RBM（可平行取樣）。</figcaption>
</figure>

### 16.1 有向 vs 無向

| | 有向圖（貝氏網路） | 無向圖（馬可夫隨機場） |
|---|---|---|
| 語意 | 因果／生成順序 | 相容性（誰和誰合得來） |
| 分解 | `p(x) = ∏ p(xᵢ | pa(xᵢ))` | `p(x) = ∏ ψ(x_c) / Z` |
| 取樣 | 照拓樸順序 | 通常要靠 MCMC |
| 難點 | 難以表示「循環相依」 | `Z` 算不出來 |

### 16.2 為什麼深度學習最後選了有向圖（大部分時候）

因為有向圖的似然**可以逐項計算**，不需要配分函數。無向圖（能量模型）雖然表達力強，但每次評估都要面對 `Z`——這就是第 18 章整章存在的理由。

### 16.3 圖帶來的兩個實務好處

- **參數效率**：稀疏圖 → 每個因子只看少數變數
- **推論可分解**：圖結構決定能不能用動態規劃或平行取樣

---

## 17　蒙地卡羅方法：用取樣逼近

### 一句話

<strong>當積分算不出來，就抽樣本平均它。</strong>

<div class="eq">E<sub>x∼p</sub>[f(x)] ≈ (1/n) Σ f(x<sup>(i)</sup>)，x<sup>(i)</sup> ∼ p(x)</div>

### 17.1 三種取樣策略

| 方法 | 想法 | 限制 |
|---|---|---|
| 直接取樣 | 從目標分布抽 | 多數分布抽不出來 |
| 重要性取樣 | 從好抽的 q 抽，用權重修正 | 高維時權重方差爆炸 |
| MCMC | 造一條穩態為 p 的馬可夫鏈 | 混合慢、相鄰樣本相關 |

### 17.2 MCMC 的核心難題：混合

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 368" width="100%" role="img" aria-label="MCMC 的混合問題：兩座山中間的低密度谷" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:880px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="mcmc-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><text x="440" y="26" font-size="13.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">馬可夫鏈只能走「附近」，跳不過中間那條細谷</text><polygon points="50,283.812 54.4,283.091 58.8,282.265 63.2,281.325 67.6,280.257 72,279.051 76.4,277.694 80.8,276.172 85.2,274.473 89.6,272.585 94,270.496 98.4,268.193 102.8,265.667 107.2,262.907 111.6,259.906 116,256.657 120.4,253.156 124.8,249.4 129.2,245.39 133.6,241.13 138,236.625 142.4,231.887 146.8,226.928 151.2,221.765 155.6,216.419 160,210.915 164.4,205.28 168.8,199.547 173.2,193.75 177.6,187.928 182,182.121 186.4,176.372 190.8,170.727 195.2,165.231 199.6,159.931 204,154.874 208.4,150.105 212.8,145.67 217.2,141.61 221.6,137.966 226,134.774 230.4,132.067 234.8,129.871 239.2,128.211 243.6,127.103 248,126.559 252.4,126.585 256.8,127.18 261.2,128.339 265.6,130.049 270,132.292 274.4,135.044 278.8,138.278 283.2,141.961 287.6,146.056 292,150.523 296.4,155.319 300.8,160.4 305.2,165.718 309.6,171.228 314,176.883 318.4,182.636 322.8,188.443 327.2,194.261 331.6,200.048 336,205.767 340.4,211.383 344.8,216.864 349.2,222.182 353.6,227.311 358,232.232 362.4,236.925 366.8,241.378 371.2,245.58 375.6,249.522 380,253.201 384.4,256.614 388.8,259.761 393.2,262.645 397.6,265.27 402,267.64 406.4,269.762 410.8,271.642 415.2,273.287 419.6,274.705 424,275.903 428.4,276.886 432.8,277.662 437.2,278.234 441.6,278.607 446,278.784 450.4,278.767 454.8,278.558 459.2,278.155 463.6,277.558 468,276.765 472.4,275.772 476.8,274.576 481.2,273.173 485.6,271.559 490,269.73 494.4,267.68 498.8,265.407 503.2,262.908 507.6,260.181 512,257.226 516.4,254.044 520.8,250.638 525.2,247.014 529.6,243.18 534,239.147 538.4,234.927 542.8,230.538 547.2,225.999 551.6,221.332 556,216.562 560.4,211.718 564.8,206.83 569.2,201.932 573.6,197.059 578,192.248 582.4,187.537 586.8,182.966 591.2,178.574 595.6,174.4 600,170.483 604.4,166.86 608.8,163.565 613.2,160.632 617.6,158.089 622,155.964 626.4,154.277 630.8,153.047 635.2,152.286 639.6,152.002 644,152.198 648.4,152.873 652.8,154.019 657.2,155.624 661.6,157.672 666,160.141 670.4,163.005 674.8,166.237 679.2,169.804 683.6,173.671 688,177.802 692.4,182.158 696.8,186.701 701.2,191.391 705.6,196.19 710,201.057 714.4,205.958 718.8,210.855 723.2,215.716 727.6,220.51 732,225.208 736.4,229.785 740.8,234.219 745.2,238.491 749.6,242.584 754,246.486 758.4,250.187 762.8,253.679 767.2,256.959 771.6,260.024 776,262.876 780.4,265.516 784.8,267.95 789.2,270.184 793.6,272.225 798,274.081 802.4,275.762 806.8,277.278 811.2,278.64 815.6,279.857 820,280.941 824.4,281.902 828.8,282.751 833.2,283.498 837.6,284.152 842,284.723 842,288 50,288" fill="#58a6ff" opacity="0.18"/><path d="M50,283.812 L54.4,283.091 L58.8,282.265 L63.2,281.325 L67.6,280.257 L72,279.051 L76.4,277.694 L80.8,276.172 L85.2,274.473 L89.6,272.585 L94,270.496 L98.4,268.193 L102.8,265.667 L107.2,262.907 L111.6,259.906 L116,256.657 L120.4,253.156 L124.8,249.4 L129.2,245.39 L133.6,241.13 L138,236.625 L142.4,231.887 L146.8,226.928 L151.2,221.765 L155.6,216.419 L160,210.915 L164.4,205.28 L168.8,199.547 L173.2,193.75 L177.6,187.928 L182,182.121 L186.4,176.372 L190.8,170.727 L195.2,165.231 L199.6,159.931 L204,154.874 L208.4,150.105 L212.8,145.67 L217.2,141.61 L221.6,137.966 L226,134.774 L230.4,132.067 L234.8,129.871 L239.2,128.211 L243.6,127.103 L248,126.559 L252.4,126.585 L256.8,127.18 L261.2,128.339 L265.6,130.049 L270,132.292 L274.4,135.044 L278.8,138.278 L283.2,141.961 L287.6,146.056 L292,150.523 L296.4,155.319 L300.8,160.4 L305.2,165.718 L309.6,171.228 L314,176.883 L318.4,182.636 L322.8,188.443 L327.2,194.261 L331.6,200.048 L336,205.767 L340.4,211.383 L344.8,216.864 L349.2,222.182 L353.6,227.311 L358,232.232 L362.4,236.925 L366.8,241.378 L371.2,245.58 L375.6,249.522 L380,253.201 L384.4,256.614 L388.8,259.761 L393.2,262.645 L397.6,265.27 L402,267.64 L406.4,269.762 L410.8,271.642 L415.2,273.287 L419.6,274.705 L424,275.903 L428.4,276.886 L432.8,277.662 L437.2,278.234 L441.6,278.607 L446,278.784 L450.4,278.767 L454.8,278.558 L459.2,278.155 L463.6,277.558 L468,276.765 L472.4,275.772 L476.8,274.576 L481.2,273.173 L485.6,271.559 L490,269.73 L494.4,267.68 L498.8,265.407 L503.2,262.908 L507.6,260.181 L512,257.226 L516.4,254.044 L520.8,250.638 L525.2,247.014 L529.6,243.18 L534,239.147 L538.4,234.927 L542.8,230.538 L547.2,225.999 L551.6,221.332 L556,216.562 L560.4,211.718 L564.8,206.83 L569.2,201.932 L573.6,197.059 L578,192.248 L582.4,187.537 L586.8,182.966 L591.2,178.574 L595.6,174.4 L600,170.483 L604.4,166.86 L608.8,163.565 L613.2,160.632 L617.6,158.089 L622,155.964 L626.4,154.277 L630.8,153.047 L635.2,152.286 L639.6,152.002 L644,152.198 L648.4,152.873 L652.8,154.019 L657.2,155.624 L661.6,157.672 L666,160.141 L670.4,163.005 L674.8,166.237 L679.2,169.804 L683.6,173.671 L688,177.802 L692.4,182.158 L696.8,186.701 L701.2,191.391 L705.6,196.19 L710,201.057 L714.4,205.958 L718.8,210.855 L723.2,215.716 L727.6,220.51 L732,225.208 L736.4,229.785 L740.8,234.219 L745.2,238.491 L749.6,242.584 L754,246.486 L758.4,250.187 L762.8,253.679 L767.2,256.959 L771.6,260.024 L776,262.876 L780.4,265.516 L784.8,267.95 L789.2,270.184 L793.6,272.225 L798,274.081 L802.4,275.762 L806.8,277.278 L811.2,278.64 L815.6,279.857 L820,280.941 L824.4,281.902 L828.8,282.751 L833.2,283.498 L837.6,284.152 L842,284.723" fill="none" stroke="#58a6ff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><line x1="50" y1="288" x2="842" y2="288" stroke="#6e7681" stroke-width="1.4" stroke-linecap="round"/><text x="250" y="106" font-size="12" fill="#58a6ff" text-anchor="middle" font-weight="700">模式 A</text><text x="640" y="126" font-size="12" fill="#58a6ff" text-anchor="middle" font-weight="700">模式 B</text><circle cx="150" cy="239.192" r="4.2" fill="#3fb950" stroke="none" stroke-width="1.4"/><circle cx="178" cy="203.399" r="4.2" fill="#3fb950" stroke="none" stroke-width="1.4"/><circle cx="206" cy="168.668" r="4.2" fill="#3fb950" stroke="none" stroke-width="1.4"/><circle cx="232" cy="147.208" r="4.2" fill="#3fb950" stroke="none" stroke-width="1.4"/><circle cx="258" cy="143.441" r="4.2" fill="#3fb950" stroke="none" stroke-width="1.4"/><circle cx="282" cy="156.916" r="4.2" fill="#3fb950" stroke="none" stroke-width="1.4"/><circle cx="306" cy="182.712" r="4.2" fill="#3fb950" stroke="none" stroke-width="1.4"/><circle cx="600" cy="186.485" r="4.2" fill="#3fb950" stroke="none" stroke-width="1.4"/><circle cx="628" cy="169.776" r="4.2" fill="#3fb950" stroke="none" stroke-width="1.4"/><circle cx="656" cy="171.142" r="4.2" fill="#3fb950" stroke="none" stroke-width="1.4"/><circle cx="684" cy="190.036" r="4.2" fill="#3fb950" stroke="none" stroke-width="1.4"/><path d="M352,208 Q452,176 556,206" fill="none" stroke="#ff7b72" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="7 5"/><text x="449" y="158" font-size="11" fill="#ff7b72" text-anchor="middle" font-weight="400">接受率極低 → 幾乎不跨越</text><text x="449" y="306" font-size="11" fill="#6e7681" text-anchor="middle" font-weight="400">兩峰之間的低密度區域</text><text x="449" y="326" font-size="11" fill="#6e7681" text-anchor="middle" font-weight="400">（鏈卡在單一模式裡，估計就會偏）</text><text x="50" y="350" font-size="11.5" fill="#9aa4b2" text-anchor="start" font-weight="400">對策：多鏈、溫度／平行回火（parallel tempering）、更好的提案分布</text></svg>
<figcaption>圖 12：MCMC 的混合問題：兩座模式之間隔著低密度谷，鏈幾乎不會跨越，估計因此偏掉。</figcaption>
</figure>

書中用「模式之間的距離」解釋為什麼 MCMC 在深度學習裡常失敗：**高維空間裡，不同模式之間隔著大片低密度區域，鏈幾乎不會跨越**。對策是多鏈、溫度／平行回火、或用更好的提案分布（這也是後來 HMC／NUTS 的方向）。

### 17.3 Gibbs 取樣

一次只更新一個變數、其餘固定。在 RBM 這種「層內不相連」的結構上特別方便——可以整層平行更新。

---

## 18　配分函數：那個算不出來的 Z

### 一句話

<strong>能量模型的所有麻煩，都來自一個分母：Z = Σ exp(−E(x))。</strong>

### 18.1 為什麼似然的梯度其實不需要 Z

<div class="eq">∇<sub>θ</sub> log p(x) = −∇<sub>θ</sub>E(x) − E<sub>p(x′)</sub>[−∇<sub>θ</sub>E(x′)]</div>

第二項需要「從模型本身取樣」。也就是說：<strong>訓練能量模型 = 一直拿模型自己的樣本去對抗真實樣本</strong>。這正是對比散度（CD）與 GAN 的共同祖先。

### 18.2 六種繞過 Z 的方法

| 方法 | 核心 |
|---|---|
| 隨機最大似然 ＋ MCMC | 用短鏈近似模型樣本（CD-k） |
| 偽似然 | 用 `p(xᵢ|x₋ᵢ)` 避開 Z |
| 分數匹配 | 直接學 `∇ₓ log p(x)`，Z 消失 |
| 去噪分數匹配 | 用加噪資料估分數（擴散模型的基礎） |
| 噪聲對比估計 NCE | 把「密度估計」變成「分類真假」 |
| 估計 Z 本身 | 退火重要性取樣、橋接取樣 |

<strong>這張表是 Part III 的樞紐</strong>：後面第 19 章的變分推論、第 20 章的 VAE／GAN，都是在回答「Z 怎麼辦」。

---

## 19　近似推論：把推論變成最佳化

### 一句話

<strong>算不出後驗 `p(h|x)`，就找一個好算的 `q(h)` 儘量靠近它。</strong>

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 356" width="100%" role="img" aria-label="變分推論：把 log p(x) 拆成 ELBO 與 KL" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:900px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="elbo-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><text x="450" y="26" font-size="13.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">我們最大化的其實是 ELBO —— 一個可算的下界</text><text x="170" y="56" font-size="12" fill="#9aa4b2" text-anchor="start" font-weight="400" font-family="Cascadia Mono,Consolas,monospace">log p(x) =</text><rect x="300" y="42" width="330" height="46" rx="8" fill="#58a6ff" stroke="none" stroke-width="1.2"/><text x="465" y="70" font-size="13" fill="#08131f" text-anchor="middle" font-weight="700">ELBO（可計算）</text><rect x="640" y="42" width="190" height="46" rx="8" fill="#d29922" stroke="none" stroke-width="1.2"/><text x="735" y="70" font-size="13" fill="#08131f" text-anchor="middle" font-weight="700">KL ≥ 0</text><line x1="420" y1="96" x2="350" y2="130" stroke="#30363d" stroke-width="2" stroke-linecap="round" marker-end="url(#el-ar)"/><line x1="545" y1="96" x2="620" y2="130" stroke="#30363d" stroke-width="2" stroke-linecap="round" marker-end="url(#el-ar)"/><rect x="150" y="132" width="290" height="108" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="295" y="158" font-size="12.5" fill="#39d0d8" text-anchor="middle" font-weight="700" font-family="Cascadia Mono,Consolas,monospace">E_q[log p(x, z)]</text><text x="295" y="184" font-size="11.2" fill="#9aa4b2" text-anchor="middle" font-weight="400">重建項：解碼器要把資料解釋得夠好</text><text x="295" y="210" font-size="11" fill="#6e7681" text-anchor="middle" font-weight="400">這一項讓樣本像真的</text><rect x="530" y="132" width="290" height="108" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1.2"/><text x="675" y="158" font-size="12.5" fill="#bc8cff" text-anchor="middle" font-weight="700" font-family="Cascadia Mono,Consolas,monospace">KL(q(z)‖p(z)) ≥ 0</text><text x="675" y="184" font-size="11.2" fill="#9aa4b2" text-anchor="middle" font-weight="400">複雜度懲罰：q 離先驗越遠越貴</text><text x="675" y="210" font-size="11" fill="#6e7681" text-anchor="middle" font-weight="400">推論網路（encoder）就是在學 q</text><text x="450" y="268" font-size="12" fill="#e6edf3" text-anchor="middle" font-weight="400">兩股力量互相拉扯：重建要準、潛在分布要規矩（第 19、20 章）</text><text x="450" y="292" font-size="11.5" fill="#6e7681" text-anchor="middle" font-weight="400">VAE 就是把這個目標寫成兩顆網路：encoder 輸出 μ、σ，decoder 輸出機率</text><text x="450" y="340" font-size="11.5" fill="#9aa4b2" text-anchor="middle" font-weight="400">注意：ELBO 是下界，不是等號 —— 差距正好是 KL(q(z)‖p(z|x))</text></svg>
<figcaption>圖 13：變分推論把 log p(x) 拆成 ELBO 與 KL：最大化 ELBO 等於同時拉高重建機率、並讓 q 靠近先驗。</figcaption>
</figure>

### 19.1 三條路線

| 路線 | 做法 | 代表 |
|---|---|---|
| 期望最大化 EM | 交替算後驗與更新參數 | 混合模型、HMM |
| MAP 推論 | 只找眾數，不求整個分布 | 稀疏編碼 |
| 變分推論 | 最大化 ELBO（可算下界） | VAE、變分貝氏 |

### 19.2 ELBO 的兩項在吵架

`ELBO = E_q[log p(x,z)] − KL(q(z)‖p(z))`

- 第一項要「解釋得準」→ q 收窄到某個模式
- 第二項要「接近先驗」→ q 攤平、覆蓋多個模式
- 兩項的平衡點，就是 VAE 樣本偏模糊的原因（posterior collapse 是極端情況）

### 19.3 學一個推論網路

把 `q` 換成一個神經網路（encoder），就變成 amortized inference：**一次前向得到近似後驗**，不必對每筆資料重新最佳化。這是 VAE 最大的工程貢獻。

---

## 20　深度生成模型：學會生成

### 一句話

<strong>生成模型的分歧點不是「誰更強」，而是「你選擇面對哪個難算的量」。</strong>

<figure class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 396" width="100%" role="img" aria-label="深度生成模型四家族：目標函數決定一切" font-family="Noto Sans TC,Microsoft JhengHei,PingFang TC,Segoe UI,sans-serif" style="background:#0d1117;color:#e6edf3;max-width:900px;height:auto;display:block;margin:0 auto;border-radius:10px"><defs><marker id="gen-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9aa4b2"/></marker></defs><text x="450" y="26" font-size="13.5" fill="#9aa4b2" text-anchor="middle" font-weight="600">同樣想學 p(x)，四種寫法各有代價</text><rect x="25" y="42" width="410" height="148" rx="10" fill="#161b22" stroke="#58a6ff" stroke-width="1.2"/><text x="43" y="72" font-size="13" fill="#58a6ff" text-anchor="start" font-weight="700">VAE（變分自編碼器）</text><circle cx="49" cy="92" r="2.6" fill="#58a6ff" stroke="none" stroke-width="1.4"/><text x="61" y="96" font-size="11.3" fill="#9aa4b2" text-anchor="start" font-weight="400">encoder 輸出 μ、σ，decoder 輸出分布</text><circle cx="49" cy="116" r="2.6" fill="#58a6ff" stroke="none" stroke-width="1.4"/><text x="61" y="120" font-size="11.3" fill="#9aa4b2" text-anchor="start" font-weight="400">目標：ELBO（重建 ＋ KL）</text><circle cx="49" cy="140" r="2.6" fill="#58a6ff" stroke="none" stroke-width="1.4"/><text x="61" y="144" font-size="11.3" fill="#9aa4b2" text-anchor="start" font-weight="400">優點：一次前向就取樣；缺點：樣本偏模糊</text><rect x="465" y="42" width="410" height="148" rx="10" fill="#161b22" stroke="#3fb950" stroke-width="1.2"/><text x="483" y="72" font-size="13" fill="#3fb950" text-anchor="start" font-weight="700">GAN（對抗網路）</text><circle cx="489" cy="92" r="2.6" fill="#3fb950" stroke="none" stroke-width="1.4"/><text x="501" y="96" font-size="11.3" fill="#9aa4b2" text-anchor="start" font-weight="400">生成器騙、判別器抓（雙人零和賽局）</text><circle cx="489" cy="116" r="2.6" fill="#3fb950" stroke="none" stroke-width="1.4"/><text x="501" y="120" font-size="11.3" fill="#9aa4b2" text-anchor="start" font-weight="400">沒有似然，只有「像不像」</text><circle cx="489" cy="140" r="2.6" fill="#3fb950" stroke="none" stroke-width="1.4"/><text x="501" y="144" font-size="11.3" fill="#9aa4b2" text-anchor="start" font-weight="400">優點：樣本銳利；缺點：訓練不穩、模式崩壞</text><rect x="25" y="206" width="410" height="148" rx="10" fill="#161b22" stroke="#bc8cff" stroke-width="1.2"/><text x="43" y="236" font-size="13" fill="#bc8cff" text-anchor="start" font-weight="700">能量模型（RBM／DBM）</text><circle cx="49" cy="256" r="2.6" fill="#bc8cff" stroke="none" stroke-width="1.4"/><text x="61" y="260" font-size="11.3" fill="#9aa4b2" text-anchor="start" font-weight="400">p(x) ∝ exp(−E(x))／Z</text><circle cx="49" cy="280" r="2.6" fill="#bc8cff" stroke="none" stroke-width="1.4"/><text x="61" y="284" font-size="11.3" fill="#9aa4b2" text-anchor="start" font-weight="400">取樣靠 MCMC、學習靠對比散度</text><circle cx="49" cy="304" r="2.6" fill="#bc8cff" stroke="none" stroke-width="1.4"/><text x="61" y="308" font-size="11.3" fill="#9aa4b2" text-anchor="start" font-weight="400">優點：理論清楚；缺點：Z 難算、混合慢</text><rect x="465" y="206" width="410" height="148" rx="10" fill="#161b22" stroke="#d29922" stroke-width="1.2"/><text x="483" y="236" font-size="13" fill="#d29922" text-anchor="start" font-weight="700">自回歸（NADE／PixelRNN）</text><circle cx="489" cy="256" r="2.6" fill="#d29922" stroke="none" stroke-width="1.4"/><text x="501" y="260" font-size="11.3" fill="#9aa4b2" text-anchor="start" font-weight="400">p(x) = ∏ p(x_i | x_&lt;i)</text><circle cx="489" cy="280" r="2.6" fill="#d29922" stroke="none" stroke-width="1.4"/><text x="501" y="284" font-size="11.3" fill="#9aa4b2" text-anchor="start" font-weight="400">把生成拆成一連串預測</text><circle cx="489" cy="304" r="2.6" fill="#d29922" stroke="none" stroke-width="1.4"/><text x="501" y="308" font-size="11.3" fill="#9aa4b2" text-anchor="start" font-weight="400">優點：似然可精算；缺點：取樣要逐步</text><text x="450" y="382" font-size="11.8" fill="#6e7681" text-anchor="middle" font-weight="400">第 20 章的主軸：不是「哪個模型最好」，而是「你願意為哪個量付出計算成本」</text></svg>
<figcaption>圖 14：深度生成模型四家族：VAE、GAN、能量模型、自回歸——差別在願意為哪個量付出計算成本。</figcaption>
</figure>

### 20.1 四條主線

| 家族 | 目標 | 難點 | 現在的地位 |
|---|---|---|---|
| 玻爾茲曼機／RBM／DBM | 能量模型 | Z 與混合 | 理論重要，實務少用 |
| VAE | ELBO | 樣本偏模糊 | 表示學習、壓縮 |
| GAN | 對抗賽局 | 訓練不穩、模式崩壞 | 高品質生成 |
| 自回歸／擴散 | 精確似然 | 取樣慢 | 目前的主流生成路線 |

### 20.2 玻爾茲曼機為什麼仍然值得讀

它是「**用取樣代替微分**」這個想法的原型：RBM 的層內不相連，讓 Gibbs 取樣可以整層平行；DBM 則是多層能量模型，用來做無監督預訓練。讀懂它，才能理解為什麼後來的對比學習、噪聲對比估計都是同一個骨架。

### 20.3 生成模型的評估

| 指標 | 量什麼 | 問題 |
|---|---|---|
| 對數似然 | 對資料的機率密度 | 有些模型算不出來 |
| 樣本品質 | 人眼／Inception Score／FID | 與似然不一定相關 |
| 模式覆蓋 | 是否漏掉整類樣本 | FID 對小缺陷不敏感 |

> <strong>全書結論</strong>：深度學習的進展不是「找到單一最好的模型」，而是「針對每個任務，選一組可以承擔的計算與統計取捨」。

---

## 附錄 A：符號與中英對照速查表

### A.1 符號

| 符號 | 讀法 | 意思 |
|---|---|---|
| a | 純量 | 單一數字 |
| **a** | 向量 | 一維陣列（本書用粗體） |
| **A** | 矩陣 | 二維陣列 |
| **A** | 張量 | 三維以上（與矩陣共用粗體大寫） |
| θ | theta | 全部可學習參數 |
| ∇<sub>θ</sub> | nabla | 對 θ 的梯度 |
| η | eta | 學習率 |
| λ、α | lambda／alpha | 正則化係數 |
| σ | sigma | sigmoid 函數，或標準差 |
| ⊙ | 圓圈點 | 逐元素相乘 |
| ‖w‖<sub>p</sub> | norm | Lp 範數 |
| D<sub>KL</sub> | KL | KL 散度 |
| Z | 配分函數 | 機率歸一化常數 |

### A.2 中英對照

| 中文 | English | 一句話 |
|---|---|---|
| 容量 | capacity | 模型能擬合多複雜的函數 |
| 泛化 | generalization | 在新資料上的表現 |
| 正則化 | regularization | 用偏好換泛化 |
| 超參數 | hyperparameter | 不是用梯度學的參數 |
| 隱藏單元 | hidden unit | 中間層的一個神經元 |
| 表徵／表示 | representation | 資料被轉換後的形式 |
| 潛在變數 | latent variable | 觀察不到的解釋因子 |
| 配分函數 | partition function | 能量模型的歸一化分母 |
| 變分下界 | ELBO | 可算的似然下界 |
| 模式崩壞 | mode collapse | 生成器只會生少數幾種樣本 |

---

## 附錄 B：常見誤解與陷阱

### B.1 十個最常見的誤解

| # | 誤解 | 事實 |
|---|---|---|
| 1 | 「層數越多越好」 | 沒有正則化與殘差連接，深層只會更難訓練 |
| 2 | 「訓練誤差低就是好模型」 | 只看訓練誤差等於沒看 |
| 3 | 「測試集可以用來調參」 | 用了就變成驗證集，成績會樂觀偏誤 |
| 4 | 「Dropout 在推論時也要丟」 | 推論要嘛乘保留機率、要嘛訓練時用 inverted dropout |
| 5 | 「Adam 一定比 SGD 好」 | 影像分類上 SGD＋動量常泛化更好 |
| 6 | 「L1 和 L2 只是公式不同」 | L1 產生稀疏解、L2 產生平滑解 |
| 7 | 「BatchNorm 是正則化」 | 它主要解決最佳化穩定性 |
| 8 | 「梯度消失只是 sigmoid 的問題」 | 深層連乘本身就會消失，與啟用函數無關 |
| 9 | 「生成模型只要看起來像就好」 | 模式覆蓋與似然是不同的事 |
| 10 | 「有 GPU 就會快」 | 沒有把資料搬運與精度算清楚，常常更慢 |

### B.2 症狀 → 原因速查

| 症狀 | 先檢查 |
|---|---|
| 損失變 `nan` | 學習率太大、`log(0)`、除以 0、混合精度溢位 |
| 損失完全不動 | 標籤與輸入沒對上、學習率太小、梯度被 detach |
| 驗證分數比訓練高很多 | 驗證集太小、有資料洩漏、Dropout 在推論沒關 |
| 訓練前幾步就爆 | 初始化尺度錯、沒有梯度裁剪、學習率沒 warmup |
| 只有某一類全錯 | 類別不平衡、損失沒有加權 |

---

## 附錄 C：原文資源與延伸閱讀

### C.1 原文與官方資源

- 官方網站（免費 HTML 版）：<https://www.deeplearningbook.org/>
- 作者提供的 LaTeX 模板與記號頁（寫論文時可直接對齊符號）
- 官方習題（Exercises）與授課投影片（Lectures）都在同一站

### C.2 本站可以接著讀的筆記

| 主題 | 站內頁面 |
|---|---|
| 機器學習入門地圖 | /ml-textbook-notes/ |
| 神經網路基礎（激勵函數、反向傳播） | /neural-network-notes/ |
| 卷積網路實作 | /cnn-notes/ |
| 泛化與模型選擇 | /generalization-notes/ |
| 大型語言模型入門 | /llm-intro-notes/ |

### C.3 讀完這本之後

1. 想補**實作**：找一個框架（PyTorch），把第 6、9 章的模型自己寫一遍
2. 想補**理論**：機率圖模型（Koller & Friedman）、資訊幾何
3. 想追**前沿**：Transformer、擴散模型、表示學習的對比學習路線

---

## 附錄 D：一頁精華（考前 10 分鐘）

| 章 | 只記這一句 |
|---|---|
| 1 | 深度學習＝可學習的表示，規模本身是方法 |
| 2 | 一切都是張量運算；SVD 對任意矩陣成立 |
| 3 | 交叉熵＝負對數似然；KL 不對稱 |
| 4 | 先減最大值再 exp；病態條件讓學習率無解 |
| 5 | 容量↑ 偏差↓ 方差↑；驗證集不能訓練 |
| 6 | 沒有非線性，疊幾層都等於一層 |
| 7 | 正則化＝把偏好寫進損失 |
| 8 | 高維的敵人是鞍點，不是局部極小 |
| 9 | 局部性＋參數共享＋平移等變性 |
| 10 | RNN 的深度在時間軸；LSTM 用加法捷徑 |
| 11 | 先指標、再基準、最後才調參 |
| 12 | 規模帶來質變，但要先問不變性是什麼 |
| 13 | x = Wh + noise，線性版本有解析解 |
| 14 | 瓶頸逼它只留重要資訊；去噪逼它學流形 |
| 15 | 好表示讓下游任務變簡單 |
| 16 | 有向圖可算似然，無向圖要面對 Z |
| 17 | 取樣平均代替積分；MCMC 卡在混合 |
| 18 | 似然梯度不需要 Z，但需要模型自己的樣本 |
| 19 | 算不出後驗就最大化 ELBO |
| 20 | 選模型＝選你願意承擔的計算 |

### D.1 離線執行提示

這份導讀是**單一 HTML 檔、零外部資源**：CSS、14 張 SVG 全部內嵌，下載後雙擊就能讀，關掉網路也不會掉圖。

圖表由 Python 產生器輸出（純標準庫，座標抽成常數、重複卡片用迴圈），產線腳本放在工作目錄、不進版控。要注意的是：<strong>圖是 build time 內嵌的</strong>，直接改 `index.html` 會在下次重建時被覆蓋——要換一張圖，請改產生器再重建，不要手改 HTML。

---

## 附錄 E：互動式線上測驗（40 題）

### E.1 開始測驗

**40 題單選，滿分 40，建議 50 分鐘。** 點選答案即自動計分，作答進度存在瀏覽器（localStorage），關掉隔天再開可以接續。

<div class="cta"><a href="mc-quiz.html">🖱️ 開始 40 題線上測驗</a></div>

題目依三個部分排列：第 1–14 題（Part I 數學與 ML 基礎）、第 15–27 題（Part II 網路與訓練）、第 28–40 題（Part III 研究主題）。

### E.2 使用方式

| 按鈕 | 作用 |
|---|---|
| 顯示答案 | 揭曉正解與解析（再按一次隱藏） |
| 全部／未作答／答錯 | 篩選題目，只練不會的 |
| 題號格子 | 跳到該題；綠＝對、紅＝錯 |
| 重置 | 清空作答紀錄（無法復原） |

### E.3 評分參考

| 分數 | 判讀 | 建議 |
|---|---|---|
| 36–40 | 骨架清楚 | 直接讀原書第 17–20 章 |
| 28–35 | 大致掌握 | 回頭讀第 5、8 章 |
| 20–27 | 名詞熟、機制不熟 | 依附錄 F 對照重讀 |
| < 20 | 需要先補基礎 | 先讀第 2、3、5 章 |

---

## 附錄 F：答錯題目 → 複習章節對照

| 題號 | 主題 | 回去讀 |
|---|---|---|
| 1–4 | 深度學習的定位與歷史 | 第 1 章 |
| 5–8 | 張量、SVD、偽逆 | 第 2 章 |
| 9–11 | 機率分布、KL、交叉熵 | 第 3 章 |
| 12–14 | 數值穩定、最佳化基礎 | 第 4 章 |
| 15–18 | 容量、偏差方差、驗證集 | 第 5 章 |
| 19–21 | XOR、輸出單元、反向傳播 | 第 6 章 |
| 22–24 | L1／L2、Dropout、早停 | 第 7 章 |
| 25–26 | 鞍點、Adam、初始化 | 第 8 章 |
| 27 | 卷積尺寸與參數量 | 第 9 章 |
| 28–30 | RNN、BPTT、LSTM | 第 10 章 |
| 31–32 | 實務流程、學習曲線 | 第 11 章 |
| 33–34 | 自編碼器、表徵學習 | 第 13–15 章 |
| 35–37 | 圖模型、MCMC、配分函數 | 第 16–18 章 |
| 38–40 | ELBO、VAE、生成模型評估 | 第 19–20 章 |

---

*這份導讀是個人學習整理；原文著作權屬 Ian Goodfellow、Yoshua Bengio、Aaron Courville 與 MIT Press。*
