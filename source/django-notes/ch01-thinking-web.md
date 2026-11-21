# 第 1 章 · 計算思維與網頁框架基礎

本章分兩部分：先認識計算思維的五個核心能力，再理解網站的運作與前後端、瀏覽器、UML 的角色。

## 1. 計算思維特徵

計算思維＝用電腦的方式思考：拆解問題、找規律、化繁為簡，再設計可執行的步驟。共有五個核心能力。

<figure class="fig-svg"><svg viewBox="0 0 820 190" width="100%" role="img" aria-label="計算思維的五個核心特徵：分解、模式識別、抽象、算法、問題的困難度與可解性" style="background:#0d1117;border-radius:10px"><g font-family="'Microsoft JhengHei','Segoe UI',sans-serif"><rect x="300" y="14" width="220" height="44" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="410" y="42" text-anchor="middle" font-size="14" fill="#e6edf3">計算思維</text><rect x="10" y="92" width="150" height="76" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="85" y="122" text-anchor="middle" font-size="14" fill="#e6edf3">分解</text><text x="85" y="144" text-anchor="middle" font-size="10.5" fill="#39d0d8">Decomposition</text><rect x="172" y="92" width="150" height="76" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="247" y="122" text-anchor="middle" font-size="14" fill="#e6edf3">模式識別</text><text x="247" y="144" text-anchor="middle" font-size="10.5" fill="#39d0d8">Pattern Recognition</text><rect x="334" y="92" width="150" height="76" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="409" y="122" text-anchor="middle" font-size="14" fill="#e6edf3">抽象</text><text x="409" y="144" text-anchor="middle" font-size="10.5" fill="#39d0d8">Abstraction</text><rect x="496" y="92" width="150" height="76" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="571" y="122" text-anchor="middle" font-size="14" fill="#e6edf3">算法</text><text x="571" y="144" text-anchor="middle" font-size="10.5" fill="#39d0d8">Algorithm</text><rect x="658" y="92" width="150" height="76" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="733" y="120" text-anchor="middle" font-size="13" fill="#e6edf3">困難度</text><text x="733" y="138" text-anchor="middle" font-size="13" fill="#e6edf3">與可解性</text><text x="733" y="158" text-anchor="middle" font-size="10.5" fill="#39d0d8">Solvability</text></g><figcaption>圖：計算思維的五個核心特徵。</figcaption></svg></figure>

### 1.1 分解（Decomposition）

**把大問題拆成小問題。** 由上而下逐層細分到可直接解決；可按關鍵因素、子任務功能或層次來拆。子問題要互相獨立、大小適中；拆小後可分別處理，再組合成整體解答。

### 1.2 模式識別（Pattern Recognition）

**在資料中看出模式、趨勢與規律，用來推測、預測或解釋現象。** 常用於機器學習、資料分析、影像處理。

#### 1.2.1 特徵提取
挑出有代表性的特徵（數字、文字、圖像）。

#### 1.2.2 分類與識別
把資料分到不同類別，並判斷新資料屬於哪一類。

#### 1.2.3 聚類分析
把相似資料自動歸群，發現潛在結構。

#### 1.2.4 模型建立與預測
建立模型描述規律，用來預測與決策。

#### 1.2.5 特徵選擇與維度降低
只留關鍵特徵、降低維度，避免「維度災難」與運算負擔。

### 1.3 抽象（Abstraction）

**只留重點、忽略細節，把問題簡化成模型。**

#### 1.3.1 目的
聚焦問題本質與關鍵關係。

#### 1.3.2 層次
高層看整體結構，低層細分成模組。

#### 1.3.3 方法
用公式、圖形、模型等更通用的形式表示。

#### 1.3.4 優點
好理解、可跨情境通用、易於模組化。

#### 1.3.5 挑戰
要拿捏「簡化」與「遺漏」之間的平衡。

### 1.4 算法（Algorithm）

**把「怎麼做」寫成明確、可依序執行的步驟**，是計算思維的核心。

#### 1.4.1 步驟與指令
由一連串明確指令組成，逐步推進。

#### 1.4.2 問題解決
定義問題 → 分析 → 設計解法 → 完成。

#### 1.4.3 效率與最佳化
看時間複雜度（耗時）與空間複雜度（耗記憶體）。

#### 1.4.4 問題分解與抽象
把問題拆小，並抽象成通用形式，擴大適用範圍。

#### 1.4.5 結構與設計
常見順序、循環、分支三種結構；選對資料結構是關鍵。

### 1.5 問題的困難度與可解性

有些問題計算上無解；可解的問題也有難易之別，會影響算法的選擇與效率。

**延伸閱讀**：Craig Larman《Applying UML and Patterns》；Booch 等《The Unified Modeling Language User Guide》。
## 2. 網頁框架開發基礎

網站本質上是一群放在伺服器上的檔案，透過網路讓使用者存取。

### 2.1 網站運作的基本要素

#### 2.1.1 域名
網站的唯一地址（如 www.example.com）；需註冊並指向伺服器 IP。

#### 2.1.2 Web 託管
把網站檔案放上伺服器、供網路存取的服務；伺服器負責處理 HTTP 請求。

#### 2.1.3 前端開發
使用者看到、可互動的部分：HTML（結構）、CSS（外觀）、JavaScript（互動）、前端框架（現成元件）。

#### 2.1.4 後端開發
伺服器端運算與資料處理；常用 PHP、Python、Ruby、Java，搭配資料庫（MySQL、PostgreSQL、MongoDB 等）。

#### 2.1.5 內容管理（CMS）
讓非工程師也能建置與管理內容，如 WordPress、Drupal、Joomla，靠範本與主題調整外觀。

#### 2.1.6 客戶端與伺服器通信
瀏覽器送 HTTP 請求、伺服器回傳檔案；可為無狀態，或用 cookie／token 維持狀態。

#### 2.1.7 網站安全
常見措施：加密（HTTPS）、身分認證、輸入驗證、防範 XSS／SQL 注入／DDoS。

<figure class="fig-svg"><svg viewBox="0 0 800 190" width="100%" role="img" aria-label="網站的請求流程：瀏覽器 → DNS 解析 → Web 伺服器 → 回應網頁" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><g font-family="'Microsoft JhengHei','Segoe UI',sans-serif"><rect x="20" y="64" width="150" height="60" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="95" y="90" text-anchor="middle" font-size="14" fill="#e6edf3">瀏覽器</text><text x="95" y="110" text-anchor="middle" font-size="11" fill="#39d0d8">輸入網址</text><line x1="172" y1="94" x2="208" y2="94" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="190" y="84" text-anchor="middle" font-size="10" fill="#7ee787">請求</text><rect x="212" y="64" width="150" height="60" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="287" y="90" text-anchor="middle" font-size="14" fill="#e6edf3">DNS</text><text x="287" y="110" text-anchor="middle" font-size="11" fill="#39d0d8">域名 → IP</text><line x1="364" y1="94" x2="400" y2="94" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="404" y="64" width="170" height="60" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="489" y="90" text-anchor="middle" font-size="14" fill="#e6edf3">Web 伺服器</text><text x="489" y="110" text-anchor="middle" font-size="11" fill="#39d0d8">Nginx / Apache</text><line x1="576" y1="94" x2="612" y2="94" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="616" y="64" width="160" height="60" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="696" y="90" text-anchor="middle" font-size="14" fill="#e6edf3">回應網頁</text><text x="696" y="110" text-anchor="middle" font-size="11" fill="#39d0d8">HTML / CSS / JS</text><path d="M489 124 L489 156 L95 156 L95 128" fill="none" stroke="#39d0d8" stroke-width="1.5" stroke-dasharray="5 4"/></g><text x="400" y="182" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">後端（Django 等）處理資料、產生動態內容後回傳</text><figcaption>圖：網站的一次請求流程。</figcaption></svg></figure>

### 2.2 維護與更新

定期維護才能保持正常、快速、安全：故障修復、效能優化、相容性、內容更新。

### 2.3 前端開發

使用者在瀏覽器看到、可互動的部分。主要技術：

1. **HTML**：網頁結構（用標籤定義元素）。
2. **CSS**：外觀與排版；樣式與結構分離，全站風格一致。
3. **JavaScript**：互動與動態，並以 AJAX 非同步取資料。
4. **前端框架／函式庫**：React、Angular、Vue.js、jQuery、Bootstrap。
5. **響應式設計**：用媒體查詢與彈性版面適配各種裝置。
6. **瀏覽器相容性**：在 Chrome、Firefox、Safari、Edge 表現一致。
7. **可用性與 UX**：介面直覺、好用。
8. **效能優化**：壓縮、快取、延遲載入等。
9. **建置工具**：npm／Yarn、Webpack／Gulp、Grunt。
10. **版本控制**：用 Git 追蹤與協作。
11. **除錯與測試**：開發者工具＋Jest／Selenium。
12. **前端安全**：輸入驗證、資料清理、防 XSS。

### 2.4 伺服器後端

處理邏輯、資料與前後端交換。主要組件：

1. **程式語言**：Python、Ruby、PHP、Java、C#、Node.js、Go。
2. **後端框架**：Django、Rails、Express、Laravel。
3. **資料庫（DBMS）**：MySQL、PostgreSQL、Oracle、SQL Server、MongoDB。
4. **RESTful API**：前後端溝通規範。
5. **身分驗證與授權**：RBAC、Token-based、OAuth。
6. **快取**：Redis、Memcached、Varnish。
7. **伺服器管理與部署**：架構、環境、負載平衡、備份監控。
8. **安全性**：防 XSS、CSRF、SQL 注入。
9. **第三方整合**：金流、郵件、地圖等。

### 2.5 瀏覽器

把網頁解析並顯示。主要組件與流程：

1. **使用者介面**：網址列、按鈕、書籤。
2. **渲染引擎**：WebKit、Blink、Gecko。
3. **HTML 解析器**：轉成 DOM。
4. **CSS 解析器**：轉成 CSSOM。
5. **JavaScript 引擎**：V8、SpiderMonkey。
6. **渲染樹**：結合 DOM 與 CSSOM。
7. **佈局與繪製**：計算位置大小並畫出。
8. **顯示**：輸出到螢幕等裝置。
9. **資源載入**：下載 HTML／CSS／JS／圖片。
10. **快取**：暫存資源、加快載入。
11. **AJAX**：非同步更新部分畫面。

<figure class="fig-svg"><svg viewBox="0 0 830 190" width="100%" role="img" aria-label="瀏覽器渲染流程：HTML→DOM、CSS→CSSOM、合成渲染樹、佈局、繪製" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><g font-family="'Microsoft JhengHei','Segoe UI',sans-serif"><rect x="20" y="30" width="140" height="50" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="90" y="60" text-anchor="middle" font-size="13.5" fill="#e6edf3">HTML</text><line x1="162" y1="55" x2="196" y2="55" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><rect x="200" y="30" width="140" height="50" rx="10" fill="#132030" stroke="#39d0d8" stroke-width="1.6"/><text x="270" y="60" text-anchor="middle" font-size="13.5" fill="#e6edf3">DOM</text><rect x="20" y="120" width="140" height="50" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="90" y="150" text-anchor="middle" font-size="13.5" fill="#e6edf3">CSS</text><line x1="162" y1="145" x2="196" y2="145" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><rect x="200" y="120" width="140" height="50" rx="10" fill="#132030" stroke="#39d0d8" stroke-width="1.6"/><text x="270" y="150" text-anchor="middle" font-size="13.5" fill="#e6edf3">CSSOM</text><path d="M340 55 L380 55 L380 95" fill="none" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><path d="M340 145 L380 145 L380 105" fill="none" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><rect x="392" y="76" width="140" height="50" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="462" y="106" text-anchor="middle" font-size="13.5" fill="#e6edf3">渲染樹</text><line x1="534" y1="101" x2="568" y2="101" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><rect x="572" y="76" width="110" height="50" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="627" y="106" text-anchor="middle" font-size="13" fill="#e6edf3">佈局</text><line x1="684" y1="101" x2="718" y2="101" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><rect x="722" y="76" width="96" height="50" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="770" y="106" text-anchor="middle" font-size="13" fill="#e6edf3">繪製</text></g><text x="416" y="182" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">DOM + CSSOM → 渲染樹 → 佈局（位置大小）→ 繪製到畫面</text><figcaption>圖：瀏覽器的渲染流程。</figcaption></svg></figure>

### 2.6 使用 UML 作網站系統分析與設計

**UML（統一建模語言）** 用圖形符號描述系統的結構、行為與互動；原用於軟體工程，也適用網站開發。

#### 2.6.1 UML 對網頁開發的幫助
- **需求分析**：把需求與互動視覺化。
- **架構與設計**：類圖／組件圖描述結構，行為圖描述流程。
- **介面設計**：用交互圖呈現操作流程。
- **資料庫設計**：用類圖對應實體與資料表。
- **系統集成**：描述組件間訊息傳遞。
- **文件生成**：產生設計與架構文件。

#### 2.6.2 UML 圖表類型
- **結構圖（靜態）**：類圖、物件圖、組件圖、部署圖。
- **行為圖（動態）**：用例圖、交互圖、狀態機圖、活動圖。
