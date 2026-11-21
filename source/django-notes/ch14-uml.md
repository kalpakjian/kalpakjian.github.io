# 第 14 章 · UML 系統分析與設計
## 課程大綱

### 課程介紹

本課程旨在介紹統一建模語言（UML）的基本概念和實踐，幫助學員掌握用 UML 來建模和設計軟件系統的技能。課程將涵蓋 UML 的各種圖表及其應用。

### 課程目標

- 理解 UML 的基本概念和歷史背景
- 掌握各種 UML 圖表的繪製和應用
- 能夠使用 UML 進行軟件需求分析、設計和文檔編寫
- 提升建模和設計軟件系統的能力

### 課程安排

### 第一週：UML 概述

- UML 的起源和發展
- UML 的基本概念和用途
- UML 的優勢和應用範圍

### 第二週：用例圖 (Use Case Diagram)

- 用例圖的基本構成
- 參與者 (Actors) 和用例 (Use Cases)
- 用例圖的繪製和應用

### 第三週：類圖 (Class Diagram)

- 類圖的基本構成
- 類圖的繪製和應用

### 第四週：對象圖 (Object Diagram)

- 對象圖的基本構成
- 對象 (Objects) 和鏈接 (Links)
- 對象圖的繪製和應用

### 第五週：序列圖 (Sequence Diagram)

- 序列圖的基本構成
- 生命線 (Lifelines) 和消息 (Messages)
- 序列圖的繪製和應用

### 第六週：活動圖 (Activity Diagram)

- 活動圖的基本構成
- 活動 (Activities)、決策點 (Decision Points) 和併發 (Concurrency)
- 活動圖的繪製和應用

### 第七週：狀態圖 (State Diagram)

- 狀態圖的基本構成
- 狀態 (States)、過渡 (Transitions) 和事件 (Events)
- 狀態圖的繪製和應用

### 第八週：組件圖 (Component Diagram)

- 組件圖的基本構成
- 組件 (Components) 和界面 (Interfaces)
- 組件圖的繪製和應用

### 第九週：部署圖 (Deployment Diagram)

- 部署圖的基本構成
- 節點 (Nodes) 和工件 (Artifacts)
- 部署圖的繪製和應用

### 第十週：實踐應用

- 綜合案例分析
- UML 在軟件開發中的實踐應用
- 學員專案展示和評估

## 第 1 章：UML 概述

### 1.1 統一建模語言（UML）簡介
統一建模語言（Unified Modeling Language，簡稱 UML）是一種標準化的建模語言，用於指定、可視化、構建和記錄軟件系統的各種工件。UML 由 OMG（Object Management Group）於 1997 年提出，目的是統一和標準化當時流行的多種建模語言，以提高軟件開發過程的效率和質量。
### 1.2 UML 的歷史背景
在 20 世紀 90 年代初期，軟件工程界出現了許多不同的建模方法和語言，如 Booch 方法、OMT 方法（Object Modeling Technique）和 OOSE 方法（Object-Oriented Software Engineering）。這些方法各有優勢，但也造成了標準不統一、互操作性差等問題。為瞭解決這些問題，Grady Booch、James Rumbaugh 和 Ivar Jacobson 三位著名的軟件工程師聯合提出了 UML，將各種方法的優點結合起來，形成了一個統一的標準。
### 1.3 UML 的基本概念
UML 的核心在於提供了一套標準化的符號和圖表，用於描述軟件系統的靜態結構和動態行為。UML 包括以下幾種主要的圖表：

1. **用例圖（Use Case Diagram）**：描述系統與外部使用者之間的互動。
2. **類圖（Class Diagram）**：描述系統中的類及其關係。
3. **對象圖（Object Diagram）**：描述系統在某一時刻的對象及其關係。
4. **序列圖（Sequence Diagram）**：描述對象之間的交互順序。
5. **活動圖（Activity Diagram）**：描述系統中的活動流程。
6. **狀態圖（State Diagram）**：描述對象在不同狀態下的行為。
7. **組件圖（Component Diagram）**：描述系統的物理組件及其依賴關係。
8. **部署圖（Deployment Diagram）**：描述系統的物理佈署結構。

### 1.4 UML 的應用範圍
UML 廣泛應用於軟件開發的各個階段，包括需求分析、系統設計、編碼、測試和維護。通過 UML，開發團隊可以更好地理解和溝通系統的需求和設計，從而提高軟件開發的效率和質量。具體來說，UML 的應用範圍包括但不限於以下幾個方面：

1. **需求分析**：用例圖可以幫助開發團隊與客戶明確系統的需求，確定系統的功能範圍和邊界。
2. **系統設計**：類圖、對象圖和組件圖可以幫助設計師確定系統的靜態結構和動態行為，進行詳細的系統設計。
3. **編碼**：UML 圖表可以作為編碼的藍圖，指導開發人員編寫代碼，確保代碼與設計的一致性。
4. **測試**：活動圖和狀態圖可以幫助測試人員設計測試用例，確保系統的各個功能和流程都能正常工作。
5. **維護**：UML 圖表可以作為系統的文檔，幫助維護人員理解和修改系統。

### 1.5 UML 的優勢
使用 UML 有以下幾個主要優勢：

1. **標準化**：UML 是一種國際標準，使用 UML 可以確保開發團隊之間的溝通和協作。
2. **可視化**：UML 提供了一套豐富的圖表，幫助開發人員可視化地描述和理解系統。
3. **靈活性**：UML 可以應用於各種軟件開發方法，包括面向對象方法、面向服務方法等。
4. **可擴展性**：UML 支持自定義擴展，可以根據具體項目的需求進行擴展和定製。
5. **工具支持**：市場上有許多支持 UML 的建模工具，可以幫助開發團隊提高效率和質量。

### 1.6 小結
本章介紹了 UML 的基本概念、歷史背景、應用範圍和優勢。通過這些內容，我們對 UML 有了一個初步的瞭解。在接下來的章節中，我們將深入學習 UML 的各種圖表及其應用，並通過實踐活動掌握 UML 的使用技巧。
第 2 章：用例圖（Use Case Diagram）
### 2.1 用例圖概述

<figure class="fig-svg"><svg viewBox="0 0 770 292" width="100%" role="img" aria-label="UML 用例圖：訪客、會員、管理員與活動報名系統的用例關係" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="210" y="24" width="360" height="244" rx="12" fill="none" stroke="#2c6fb1" stroke-width="1.6"/><text x="390" y="48" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">活動報名系統</text><ellipse cx="390" cy="96" rx="96" ry="30" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="390" y="101" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">瀏覽活動</text><ellipse cx="390" cy="176" rx="96" ry="30" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="390" y="181" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">報名活動</text><ellipse cx="390" cy="246" rx="96" ry="30" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="390" y="251" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">審核報名</text><rect x="20" y="76" width="110" height="50" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="75" y="101" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">訪客</text><rect x="20" y="151" width="110" height="50" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="75" y="176" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">會員</text><rect x="640" y="221" width="110" height="50" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="695" y="246" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">管理員</text><line x1="130" y1="101" x2="292" y2="96" stroke="#39d0d8" stroke-width="1.4"/><line x1="130" y1="176" x2="292" y2="176" stroke="#39d0d8" stroke-width="1.4"/><line x1="640" y1="246" x2="488" y2="246" stroke="#39d0d8" stroke-width="1.4"/></svg><figcaption>圖　用例圖：左邊兩位參與者（訪客、會員）與右邊的管理員，各自連到系統邊界內對應的用例。</figcaption></figure>
用例圖（Use Case Diagram）是一種用於描述系統功能和使用者之間交互的 UML 圖表。它主要用來捕捉和記錄系統的功能需求，幫助開發團隊和客戶之間進行溝通和交流。用例圖由用例（Use Cases）、參與者（Actors）和它們之間的關係組成。
### 2.2 用例圖的基本元素
用例圖的基本元素包括：

1. **用例（Use Case）**：用例表示系統的一個功能或行為，可以是具體的功能操作，如“登錄系統”、“查詢訂單”等。用例通常用橢圓形表示，內部寫上用例的名稱。
2. **參與者（Actor）**：參與者表示與系統交互的角色，通常是人類使用者或其他系統。參與者通常用簡單的人形符號表示，並標註參與者的名稱。
3. **關係（Relationships）**：用例和參與者之間的關係主要包括以下幾種：
    - **關聯（Association）**：用來表示參與者與用例之間的交互，通常用實線表示，線的兩端可以加箭頭以表示交互的方向。
    - **包含（Include）**：用來表示一個用例包含了另一個用例的行為，通常用虛線箭頭表示，箭頭指向被包含的用例。
    - **擴展（Extend）**：用來表示一個用例可以在特定條件下擴展另一個用例的行為，通常用虛線箭頭表示，箭頭指向被擴展的用例。
    - **泛化（Generalization）**：用來表示用例或參與者之間的繼承關係，通常用帶空心箭頭的實線表示，箭頭指向父用例或父參與者。

### 2.3 用例圖的繪製步驟
繪製用例圖的一般步驟如下：

1. **識別系統邊界**：確定系統的範圍和邊界，畫出系統邊界框。
2. **識別參與者**：找出所有與系統交互的角色，繪製參與者符號並標註名稱。
3. **識別用例**：根據需求識別系統的功能，繪製用例符號並標註名稱。
4. **建立關係**：根據需求和交互情況，建立參與者與用例之間的關聯，並標註必要的包含、擴展和泛化關係。
5. **檢查和完善**：檢查用例圖的完整性和正確性，確保所有需求和功能都得到了描述，並根據反饋進行完善。

### 2.4 用例圖的實例分析
為了更好地理解用例圖的使用，我們來看一個具體的實例：一個簡單的線上購物系統。<br />
**系統邊界**：線上購物系統的邊界包括用戶登錄、商品瀏覽、訂單處理和支付等功能。<br />
**參與者**：這個系統的主要參與者包括客戶（Customer）、系統管理員（Admin）和支付網關（Payment Gateway）。<br />
**用例**：根據需求識別系統的主要功能：

- 客戶可以“登錄系統”（Login to System）和“瀏覽商品”（Browse Products）。
- 客戶可以“添加商品到購物車”（Add Products to Cart）和“查看購物車”（View Cart）。
- 客戶可以“下訂單”（Place Order）和“進行支付”（Make Payment）。
- 系統管理員可以“管理商品”（Manage Products）和“查看訂單”（View Orders）。
- 支付網關負責“處理支付”（Process Payment）。

關係：

- 客戶與“登錄系統”、“瀏覽商品”、“添加商品到購物車”、“查看購物車”、“下訂單”和“進行支付”之間有關聯。
- 系統管理員與“管理商品”和“查看訂單”之間有關聯。
- 支付網關與“處理支付”之間有關聯。
- “進行支付”用例包含“處理支付”用例。

下面是這個線上購物系統的用例圖示例：

<figure class="fig-svg"><svg viewBox="0 0 860 680" width="100%" role="img" aria-label="UML 用例圖：線上購物系統的 9 個用例，客戶、支付網關、系統管理員與其關聯" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="250" y="20" width="380" height="640" rx="12" fill="none" stroke="#2c6fb1" stroke-width="1.6"/><text x="440" y="46" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">線上購物系統</text><ellipse cx="440" cy="80" rx="120" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="85" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">登錄系統</text><ellipse cx="440" cy="144" rx="120" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="149" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">瀏覽商品</text><ellipse cx="440" cy="208" rx="120" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="213" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">添加商品到購物車</text><ellipse cx="440" cy="272" rx="120" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="277" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">查看購物車</text><ellipse cx="440" cy="336" rx="120" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="341" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">下訂單</text><ellipse cx="440" cy="400" rx="120" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="405" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">進行支付</text><ellipse cx="440" cy="464" rx="120" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="469" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">處理支付</text><ellipse cx="440" cy="528" rx="120" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="533" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">管理商品</text><ellipse cx="440" cy="592" rx="120" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="597" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">查看訂單</text><rect x="30" y="215" width="140" height="50" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="100" y="245" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">客戶</text><line x1="170" y1="240" x2="320" y2="80" stroke="#39d0d8" stroke-width="1.4"/><line x1="170" y1="240" x2="320" y2="144" stroke="#39d0d8" stroke-width="1.4"/><line x1="170" y1="240" x2="320" y2="208" stroke="#39d0d8" stroke-width="1.4"/><line x1="170" y1="240" x2="320" y2="272" stroke="#39d0d8" stroke-width="1.4"/><line x1="170" y1="240" x2="320" y2="336" stroke="#39d0d8" stroke-width="1.4"/><line x1="170" y1="240" x2="320" y2="400" stroke="#39d0d8" stroke-width="1.4"/><rect x="690" y="439" width="140" height="50" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="760" y="469" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">支付網關</text><line x1="690" y1="464" x2="566" y2="464" stroke="#39d0d8" stroke-width="1.4"/><rect x="690" y="520" width="140" height="50" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="760" y="550" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">系統管理員</text><line x1="690" y1="545" x2="566" y2="528" stroke="#39d0d8" stroke-width="1.4"/><line x1="690" y1="545" x2="566" y2="592" stroke="#39d0d8" stroke-width="1.4"/><path d="M320 400 H272 V464 H314" fill="none" stroke="#39d0d8" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#a)"/><text x="296" y="392" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="10.5" fill="#39d0d8">«include»</text></svg><figcaption>圖　用例圖：線上購物系統的 9 個用例——客戶連到 6 個購物用例，支付網關連到「處理支付」，系統管理員連到「管理商品」「查看訂單」，且「進行支付」包含「處理支付」。</figcaption></figure>
### 2.5 用例圖的實踐應用
用例圖在軟件開發的各個階段都有廣泛應用，特別是在需求分析和系統設計階段。具體來說，用例圖的實踐應用包括：

1. **需求捕捉和分析**：用例圖幫助開發團隊捕捉和分析客戶需求，確定系統需要實現的功能，並與客戶進行有效溝通。
2. **功能描述和文檔編寫**：用例圖可以作為系統功能描述的基礎，幫助編寫需求規格文檔，確保開發團隊對系統功能的理解一致。
3. **設計和開發指導**：用例圖為系統的設計和開發提供了指導，幫助設計師和開發人員理解和實現系統的功能和交互。
4. **測試用例設計**：用例圖為測試人員設計測試用例提供了依據，幫助確保系統的各個功能點都能被測試覆蓋。
5. **項目管理和溝通**：用例圖作為一種可視化工具，幫助項目管理人員與客戶、開發團隊和其他相關人員進行有效的溝通和協作。

### 2.6 小結
本章介紹了用例圖的基本概念、構成元素、繪製步驟和實踐應用。通過這些內容，我們對用例圖有了深入的理解。在接下來的章節中，我們將繼續學習 UML 的其他圖表及其應用，並通過實踐活動進一步掌握 UML 的使用技巧。
第 3 章：類圖（Class Diagram）
### 3.1 類圖概述

<figure class="fig-svg"><svg viewBox="0 0 720 280" width="100%" role="img" aria-label="UML 類圖：Category、Article、Tag、Comment 四個類別與關聯" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="90" width="170" height="78" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="20" y1="116" x2="190" y2="116" stroke="#2c6fb1" stroke-width="1.2"/><line x1="20" y1="142" x2="190" y2="142" stroke="#2c6fb1" stroke-width="1.2"/><text x="105" y="108" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">Category</text><text x="28" y="132" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">+ name: CharField</text><text x="28" y="158" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">+ slug: SlugField</text><rect x="260" y="90" width="190" height="78" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="260" y1="116" x2="450" y2="116" stroke="#2c6fb1" stroke-width="1.2"/><line x1="260" y1="142" x2="450" y2="142" stroke="#2c6fb1" stroke-width="1.2"/><text x="355" y="108" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">Article</text><text x="268" y="132" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">+ title: CharField</text><text x="268" y="158" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">+ published: Boolean</text><rect x="520" y="20" width="160" height="78" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="520" y1="46" x2="680" y2="46" stroke="#2c6fb1" stroke-width="1.2"/><line x1="520" y1="72" x2="680" y2="72" stroke="#2c6fb1" stroke-width="1.2"/><text x="600" y="38" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">Tag</text><text x="528" y="62" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">+ name: CharField</text><text x="528" y="88" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8"></text><rect x="520" y="170" width="170" height="78" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="520" y1="196" x2="690" y2="196" stroke="#2c6fb1" stroke-width="1.2"/><line x1="520" y1="222" x2="690" y2="222" stroke="#2c6fb1" stroke-width="1.2"/><text x="605" y="188" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">Comment</text><text x="528" y="212" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">+ body: TextField</text><text x="528" y="238" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">+ created: DateTime</text><line x1="190" y1="129" x2="256" y2="129" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="200" y="120" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">1 : N</text><line x1="450" y1="105" x2="516" y2="60" stroke="#39d0d8" stroke-width="1.5"/><text x="462" y="76" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">N : N</text><line x1="450" y1="150" x2="516" y2="200" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="452" y="196" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">1 : N</text></svg><figcaption>圖　類圖：每個類別分三格（類名／屬性／方法）；<code>Category 1:N Article</code>、<code>Article N:N Tag</code>、<code>Article 1:N Comment</code>。</figcaption></figure>
類圖（Class Diagram）是 UML 中用於描述系統靜態結構的圖表之一。它展示了系統中的類及其屬性、操作和類之間的關係。類圖是面向對象設計的重要工具，幫助開發者在設計階段構建系統的邏輯模型。
### 3.2 類圖的基本元素
類圖由以下基本元素組成：

1. **類（Class）**：類是對象的模板或藍圖，定義了一組具有相同屬性和行為的對象。類通常表示為一個包含三部分的矩形：
    - **類名（Class Name）**：位於矩形的頂部，用來標識類。
    - **屬性（Attributes）**：位於中間部分，描述類的特性或狀態。
    - **操作（Operations）**：位於底部，描述類的行為或方法。
2. **屬性（Attributes）**：屬性是類的特性或狀態。屬性通常包含名稱和類型，如name: String。
3. **操作（Operations）**：操作是類的行為或方法。操作通常包含名稱和參數，如addItem(item:Item): void。
4. **關係（Relationships）**：類之間的關係主要包括以下幾種：
    - **關聯（Association）**：表示類之間的靜態聯繫。關聯通常用實線表示，可以在兩端加上箭頭以標識方向。
    - **聚合（Aggregation）**：表示整體和部分之間的關係。聚合通常用帶空心菱形的實線表示，菱形指向整體。
    - **組合（Composition）**：表示一種強聚合關係，部分不能獨立存在。組合用帶實心菱形的實線表示，菱形指向整體。
    - **繼承（Inheritance）**：表示父類和子類之間的關係。繼承用帶空心三角形的實線表示，三角形指向父類。
    - **實現（Realization）**：表示類實現接口的關係。實現用帶空心三角形的虛線表示，三角形指向接口。

### 3.3 類圖的繪製步驟
繪製類圖的一般步驟如下：

1. **識別類**：根據需求識別系統中的主要類，並繪製出這些類的矩形。
2. **定義屬性和操作**：為每個類定義屬性和操作，並在矩形中填寫。
3. **建立類之間的關係**：根據類之間的相互作用，建立關聯、聚合、組合、繼承和實現等關係。
4. **檢查和完善**：檢查類圖的完整性和正確性，確保所有的類、屬性、操作和關係都得到了描述，並根據反饋進行完善。

### 3.4 類圖的實例分析
為了更好地理解類圖的使用，我們來看一個具體的實例：一個簡單的圖書館管理系統。<br />
**識別類**：根據需求識別系統中的主要類：

- 書籍 (Book)
- 會員 (Member)
- 借閱記錄 (LoanRecord)

定義屬性和操作：

- 書籍類 (Book) :
    - **屬性**: title: String、author: String、isbn: String
    - **操作**：getDetails(): String
- 會員類 (Member) :
    - **屬性**: name: String、memberId: String
    - **操作**：register(), borrowBook(book: Book): LoanRecord
- 借閱記錄類 (LoanRecord) :
    - **屬性**：loanDate: Date、returnDate: Date
    - **操作**：markReturned()

建立類之間的關係：

- 會員和書籍之間有借閱關係，對應借閱記錄。
- 借閱記錄與會員和書籍之間存在聚合關係。

下面是這個圖書館管理系統的類圖示例：

<figure class="fig-svg"><svg viewBox="0 0 860 470" width="100%" role="img" aria-label="UML 類圖：圖書館管理系統的 Member、LoanRecord、Book 三個類與關聯" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="150" width="260" height="134" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="20" y1="176" x2="280" y2="176" stroke="#2c6fb1" stroke-width="1.2"/><line x1="20" y1="226" x2="280" y2="226" stroke="#2c6fb1" stroke-width="1.2"/><text x="150" y="168" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">Member 會員</text><text x="30" y="196" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">- name: String</text><text x="30" y="216" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">- memberId: String</text><text x="30" y="244" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">+ register()</text><text x="30" y="264" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">+ borrowBook(book: Book): LoanRecord</text><rect x="360" y="40" width="240" height="114" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="360" y1="66" x2="600" y2="66" stroke="#2c6fb1" stroke-width="1.2"/><line x1="360" y1="116" x2="600" y2="116" stroke="#2c6fb1" stroke-width="1.2"/><text x="480" y="58" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">LoanRecord 借閱記錄</text><text x="370" y="86" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">- loanDate: Date</text><text x="370" y="106" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">- returnDate: Date</text><text x="370" y="134" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">+ markReturned()</text><rect x="360" y="330" width="240" height="134" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="360" y1="356" x2="600" y2="356" stroke="#2c6fb1" stroke-width="1.2"/><line x1="360" y1="426" x2="600" y2="426" stroke="#2c6fb1" stroke-width="1.2"/><text x="480" y="348" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">Book 書籍</text><text x="370" y="376" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">- title: String</text><text x="370" y="396" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">- author: String</text><text x="370" y="416" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">- isbn: String</text><text x="370" y="444" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">+ getDetails(): String</text><line x1="280" y1="206" x2="356" y2="120" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="292" y="150" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">1</text><text x="336" y="128" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">*</text><line x1="480" y1="156" x2="480" y2="326" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="486" y="194" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">*</text><text x="486" y="316" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">1</text></svg><figcaption>圖　類圖：Member 與 LoanRecord 一對多、LoanRecord 與 Book 多對一；每個類分三格（類名／屬性／操作）。</figcaption></figure>

### 3.5 類圖的實踐應用
類圖在軟件開發的各個階段都有廣泛應用，特別是在系統設計和架構設計階段。具體來說，類圖的實踐應用包括：

1. **系統設計**：類圖幫助設計師確定系統的靜態結構，定義類及其屬性、操作和類之間的關係。
2. **代碼生成**：類圖可以作為代碼生成的基礎，許多建模工具支持從類圖生成代碼，幫助開發人員提高效率。
3. **文檔編寫**：類圖可以作為系統設計文檔的一部分，幫助開發團隊和其他相關人員理解系統的結構和設計。
4. **重構和優化**：類圖可以幫助開發團隊在重構和優化系統時，識別和調整類及其關係，改進系統的結構和性能。

### 3.6 類圖的設計原則
在設計類圖時，需要遵循以下幾個重要的設計原則：

1. 單一責任原則（Single Responsibility Principle, SRP）：每個類應該只有一個職責，即只做一件事情。
2. 開放封閉原則（Open/Closed Principle, OCP）：類應該對擴展開放，對修改封閉，即應該可以通過擴展來增加新功能，而不修改現有代碼。
3. 里氏替換原則（Liskov Substitution Principle, LSP）：子類應該可以替換父類，並且程序的行為不會發生改變。
4. 接口隔離原則（Interface Segregation Principle, ISP）：應該為客戶提供專門的接口，而不是提供大的綜合性的接口。
5. 依賴倒置原則（Dependency Inversion Principle, DIP）：應該依賴於抽象，而不是依賴於具體實現。

### 3.7 小結
本章介紹了類圖的基本概念、構成元素、繪製步驟和實踐應用。通過這些內容，我們對類圖有了深入的理解，並掌握了類圖的設計原則。在接下來的章節中，我們將繼續學習 UML 的其他圖表及其應用，並通過實踐活動進一步掌握 UML 的使用技巧。
第 4 章：對象圖（Object Diagram）
### 4.1 對象圖概述

<figure class="fig-svg"><svg viewBox="0 0 660 210" width="100%" role="img" aria-label="UML 物件圖：cat1 與 article1 兩個實例以及 category 連結" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="30" y="60" width="210" height="74" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="30" y1="86" x2="240" y2="86" stroke="#2c6fb1" stroke-width="1.2"/><text x="135" y="78" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3" text-decoration="underline">cat1 : Category</text><text x="40" y="106" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">name = "Python"</text><text x="40" y="128" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">slug = "python"</text><rect x="360" y="60" width="250" height="96" rx="6" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><line x1="360" y1="86" x2="610" y2="86" stroke="#f0a04b" stroke-width="1.2"/><text x="485" y="78" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3" text-decoration="underline">article1 : Article</text><text x="370" y="106" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">title = "Django 入門"</text><text x="370" y="128" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">published = True</text><text x="370" y="150" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">category = cat1</text><line x1="240" y1="96" x2="356" y2="96" stroke="#39d0d8" stroke-width="1.6"/><text x="248" y="88" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">category</text><text x="30" y="24" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#e6edf3">物件圖＝某一刻的實例快照（名稱加底線）</text></svg><figcaption>圖　物件圖：cat1 : Category 與 article1 : Article 是實際存在的資料，名稱加底線代表實例；兩個物件之間的連線對應類圖的關聯。</figcaption></figure>
對象圖（Object Diagram）是 UML 的一種圖表，用於描述系統在特定時刻的對象實例及其之間的關係。與類圖不同，對象圖關注的是對象的實例化狀態，展示了系統運行過程中的具體狀態。對象圖通常用於靜態結構的實例化表示，有助於理解和分析系統的動態行為。
### 4.2 對象圖的基本元素
對象圖由以下基本元素組成：

1. **對象（Object）**：對象是類的實例，表示系統中的具體實體。對象通常表示為帶下劃線的矩形，格式為 objectName : ClassName。
2. **鏈接（Link）**：鏈接表示對象之間的關係，通常用實線表示。鏈接可以帶有名稱和多重性。

### 4.3 對象圖的繪製步驟
繪製對象圖的一般步驟如下：

1. **識別對象**：根據需求識別系統中的具體對象，並繪製出這些對象的矩形。
2. **定義屬性值**：為每個對象定義具體的屬性值，展示對象在特定時刻的狀態。
3. **建立對象之間的鏈接**：根據對象之間的相互作用，建立鏈接，並標註必要的鏈接名稱和多重性。
4. **檢查和完善**：檢查對象圖的完整性和正確性，確保所有的對象、屬性值和鏈接都得到了描述，並根據反饋進行完善。

### 4.4 對象圖的實例分析
為了更好地理解對象圖的使用，我們來看一個具體的實例：一個簡單的圖書館管理系統中的對象圖。<br />
**識別對象**：根據需求識別系統中的具體對象：

- **書籍（Book）**: book1: Book, book2: Book
- **會員（Member）**: member1: Member
- **借閱記錄（LoanRecord）**: loan1: LoanRecord

定義屬性值：

- book1: Book
    - title: "UML Basics"
    - author: "John Doe"
    - isbn: "1234567890"
- book2: Book
    - title: "Advanced UML"
    - author: "Jane Smith"
    - isbn: "0987654321"
- member1: Member
    - name: "Alice"
    - memberld: "M001"
- loan1: LoanRecord
    - loanDate: "2024-01-01"
    - returnDate: "2024-01-15"

建立對象之間的鏈接：

- member1: Member 與 loan1: LoanRecord 之間有一個借閱鏈接。
- loan1: LoanRecord 與 book1: Book 之間有一個借閱鏈接。

下面是這個圖書館管理系統的對象圖示例：

<figure class="fig-svg"><svg viewBox="0 0 860 350" width="100%" role="img" aria-label="UML 物件圖：member1、loan1、book1 三個實例與借閱鏈接" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="60" width="250" height="74" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="20" y1="86" x2="270" y2="86" stroke="#2c6fb1" stroke-width="1.2"/><text x="145" y="78" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3" text-decoration="underline">member1 : Member</text><text x="30" y="106" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">name = "Alice"</text><text x="30" y="128" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">memberId = "M001"</text><rect x="330" y="60" width="250" height="74" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="330" y1="86" x2="580" y2="86" stroke="#2c6fb1" stroke-width="1.2"/><text x="455" y="78" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3" text-decoration="underline">loan1 : LoanRecord</text><text x="340" y="106" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">loanDate = "2024-01-01"</text><text x="340" y="128" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">returnDate = "2024-01-15"</text><rect x="620" y="60" width="220" height="96" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="620" y1="86" x2="840" y2="86" stroke="#2c6fb1" stroke-width="1.2"/><text x="730" y="78" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3" text-decoration="underline">book1 : Book</text><text x="630" y="106" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">title = "UML Basics"</text><text x="630" y="128" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">author = "John Doe"</text><text x="630" y="150" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">isbn = "1234567890"</text><rect x="620" y="220" width="220" height="96" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="620" y1="246" x2="840" y2="246" stroke="#2c6fb1" stroke-width="1.2"/><text x="730" y="238" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3" text-decoration="underline">book2 : Book</text><text x="630" y="266" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">title = "Advanced UML"</text><text x="630" y="288" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">author = "Jane Smith"</text><text x="630" y="310" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">isbn = "0987654321"</text><line x1="270" y1="96" x2="326" y2="96" stroke="#39d0d8" stroke-width="1.6"/><text x="272" y="88" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">borrow</text><line x1="580" y1="96" x2="616" y2="96" stroke="#39d0d8" stroke-width="1.6"/><text x="582" y="88" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">loan</text><text x="620" y="212" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">（本次借閱未用到 book2）</text></svg><figcaption>圖　物件圖：名稱加底線代表實例；member1 經 loan1 連到 book1，對應類圖 Member—LoanRecord—Book 的關聯。</figcaption></figure>

### 4.5 對象圖的實踐應用
對象圖在軟件開發的各個階段都有廣泛應用，特別是在系統分析和設計階段。具體來說，對象圖的實踐應用包括：

1. **系統狀態分析**：對象圖幫助分析系統在特定時刻的狀態，理解和展示系統中的對象及其之間的關係。
2. **動態行為演示**：對象圖可以用來演示系統的動態行為，如用例場景中的對象交互。
3. **系統設計**：對象圖為系統設計提供了實例化的視圖，有助於設計師在具體的上下文中理解類之間的關係。
4. **測試用例設計**：對象圖可以用來設計測試用例，展示測試過程中系統的具體狀態和對象交互。

### 4.6 對象圖與類圖的區別
對象圖和類圖在 UML 中都有重要作用，但它們有以下幾個主要區別：

1. **抽象層次**：類圖描述的是系統的靜態結構和類之間的關係，是一種抽象模型；對象圖描述的是系統在特定時刻的實例化狀態，是類圖的具體實例。
2. **關注點**：類圖關注的是類及其屬性、操作和類之間的關係；對象圖關注的是對象及其具體屬性值和對象之間的鏈接。
3. **時間點**：類圖是靜態的，不隨時間變化；對象圖是動態的，展示了系統在特定時刻的狀態。
4. **用途**：類圖主要用於系統設計和架構設計；對象圖主要用於系統狀態分析和動態行為演示。

### 4.7 小結
本章介紹了對象圖的基本概念、構成元素、繪製步驟和實踐應用。通過這些內容，我們對對象圖有了深入的理解，並掌握了對象圖與類圖的區別。在接下來的章節中，我們將繼續學習 UML 的其他圖表及其應用，並通過實踐活動進一步掌握 UML 的使用技巧。
第 5 章：序列圖（Sequence Diagram）
### 5.1 序列圖概述

<figure class="fig-svg"><svg viewBox="0 0 860 292" width="100%" role="img" aria-label="UML 序列圖：瀏覽器、視圖、模型、模板之間的訊息往來" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="30" y="12" width="120" height="46" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="90" y="35" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">瀏覽器</text><line x1="90" y1="58" x2="90" y2="270" stroke="#2c6fb1" stroke-width="1.2" stroke-dasharray="5 4"/><rect x="250" y="12" width="120" height="46" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="310" y="35" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">視圖</text><line x1="310" y1="58" x2="310" y2="270" stroke="#2c6fb1" stroke-width="1.2" stroke-dasharray="5 4"/><rect x="470" y="12" width="120" height="46" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="530" y="35" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">模型</text><line x1="530" y1="58" x2="530" y2="270" stroke="#2c6fb1" stroke-width="1.2" stroke-dasharray="5 4"/><rect x="670" y="12" width="120" height="46" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="730" y="35" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">模板</text><line x1="730" y1="58" x2="730" y2="270" stroke="#2c6fb1" stroke-width="1.2" stroke-dasharray="5 4"/><line x1="90" y1="96" x2="304" y2="96" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><text x="200" y="89" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">GET /post/42</text><line x1="310" y1="132" x2="524" y2="132" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><text x="420" y="125" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">query(id=42)</text><line x1="530" y1="168" x2="316" y2="168" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><text x="420" y="161" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">Article 物件</text><line x1="310" y1="204" x2="724" y2="204" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><text x="520" y="197" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">render(context)</text><line x1="730" y1="240" x2="96" y2="240" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><text x="410" y="233" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">HTML 回應</text></svg><figcaption>圖　序列圖：由上往下代表時間順序，實線箭頭是訊息；視圖先向模型取資料，再把 context 交給模板。</figcaption></figure>
序列圖（Sequence Diagram）是 UML 的一種圖表，用於描述對象之間的交互過程及其消息傳遞的順序。它展示了對象之間的動態合作過程，是理解和設計系統動態行為的重要工具。序列圖特別適合用於描述用例中的場景。
### 5.2 序列圖的基本元素
序列圖由以下基本元素組成：

1. **生命線（Lifeline）**：表示系統中的對象或角色，通常用帶有虛線的矩形表示，矩形上方標註對象或角色的名稱。
2. **消息（Message）**：表示對象之間的通信，通常用箭頭表示。根據消息的不同，箭頭可以分為同步消息、異步消息和返回消息。
3. **激活（Activation）**：表示對象在某一時間段內處於活動狀態，通常用窄矩形表示，放在生命線上。
4. **組合片段（Combined Fragment）**：表示控制結構，如條件分支、循環和並行，通常用帶標籤的框表示。

### 5.3 序列圖的繪製步驟
繪製序列圖的一般步驟如下：

1. **識別生命線**：根據需求識別系統中的對象或角色，並繪製出這些生命線。
2. **定義消息**：根據用例場景定義對象之間的通信消息，並用箭頭表示消息的傳遞順序。
3. **標註激活**：在生命線上標註對象的激活狀態，展示對象在消息傳遞過程中的活動情況。
4. **添加組合片段**：根據需求添加控制結構，如條件分支、循環和並行，並用組合片段表示。
5. **檢查和完善**：檢查序列圖的完整性和正確性，確保所有的對象、消息和控制結構都得到了描述，並根據反饋進行完善。

### 5.4 序列圖的實例分析
為了更好地理解序列圖的使用，我們來看一個具體的實例：一個簡單的線上購物系統中的序列圖。<br />
**識別生命線**：根據需求識別系統中的對象或角色：

- 客戶 (Customer)
- 網站 (Website)
- 資料庫 (Database)
- 支付系統 (Payment System)

定義消息：

- 客戶訪問網站並瀏覽商品
- 客戶選擇商品並添加到購物車
- 網站向資料庫查詢商品庫存
- 資料庫返回庫存信息
- 客戶提交訂單
- 網站向支付系統發送支付請求
- 支付系統處理支付並返回結果
- 網站確認訂單並通知客戶

下面是這個線上購物系統的序列圖示例：

<figure class="fig-svg"><svg viewBox="0 0 860 580" width="100%" role="img" aria-label="UML 序列圖：客戶、網站、資料庫與支付系統在線上購物流程中的訊息順序" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="25" y="24" width="170" height="40" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="110" y="49" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3">Customer 客戶</text><line x1="110" y1="64" x2="110" y2="540" stroke="#2c6fb1" stroke-width="1.2" stroke-dasharray="4 5"/><rect x="255" y="24" width="170" height="40" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="340" y="49" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3">Website 網站</text><line x1="340" y1="64" x2="340" y2="540" stroke="#2c6fb1" stroke-width="1.2" stroke-dasharray="4 5"/><rect x="485" y="24" width="170" height="40" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="570" y="49" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3">Database 資料庫</text><line x1="570" y1="64" x2="570" y2="540" stroke="#2c6fb1" stroke-width="1.2" stroke-dasharray="4 5"/><rect x="675" y="24" width="170" height="40" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="760" y="49" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3">Payment 支付系統</text><line x1="760" y1="64" x2="760" y2="540" stroke="#2c6fb1" stroke-width="1.2" stroke-dasharray="4 5"/><line x1="110" y1="110" x2="340" y2="110" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><text x="118" y="104" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">瀏覽商品（Browse items）</text><line x1="110" y1="155" x2="340" y2="155" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><text x="118" y="149" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">加入購物車（Add to cart）</text><line x1="110" y1="200" x2="340" y2="200" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><text x="118" y="194" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">提交訂單（Submit order）</text><line x1="340" y1="250" x2="570" y2="250" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><text x="348" y="244" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">查詢庫存（Check inventory）</text><line x1="570" y1="295" x2="340" y2="295" stroke="#39d0d8" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#a)"/><text x="348" y="289" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">庫存資訊（Inventory info）</text><line x1="340" y1="345" x2="760" y2="345" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><text x="348" y="339" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">支付請求（Payment request）</text><line x1="760" y1="390" x2="340" y2="390" stroke="#39d0d8" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#a)"/><text x="348" y="384" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">支付結果（Payment result）</text><line x1="340" y1="440" x2="110" y2="440" stroke="#39d0d8" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#a)"/><text x="118" y="434" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">確認訂單（Confirm order）</text><line x1="340" y1="485" x2="110" y2="485" stroke="#39d0d8" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#a)"/><text x="118" y="479" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">訂單明細（Order details）</text></svg><figcaption>圖　序列圖：客戶瀏覽商品、加入購物車、提交訂單；網站查詢庫存後向支付系統請求付款，再回覆訂單確認與明細。</figcaption></figure>
### 5.5 序列圖的實踐應用
序列圖在軟件開發的各個階段都有廣泛應用，特別是在需求分析和系統設計階段。具體來說，序列圖的實踐應用包括：

1. **需求捕捉和分析**：序列圖幫助開發團隊捕捉和分析系統的動態行為，理解和描述用例中的場景和對象之間的交互。
2. **功能設計和實現**：序列圖為系統功能設計和實現提供了詳細的動態視圖，幫助開發人員編寫代碼並實現系統功能。
3. **測試用例設計**：序列圖為測試人員設計測試用例提供了依據，幫助確保系統的動態行為和交互過程都能被測試覆蓋。
4. **系統文檔編寫**：序列圖可以作為系統設計文檔的一部分，幫助開發團隊和其他相關人員理解和記錄系統的動態行為。

### 5.6 序列圖的設計原則
在設計序列圖時，需要遵循以下幾個重要的設計原則：

1. **簡潔明瞭**：序列圖應該清晰明瞭，避免過於複雜和冗長。每個對象和消息都應該有明確的標識和描述。
2. **合理分解**：對於複雜的場景，可以將其分解成多個子場景，用多個序列圖分別描述，避免單個序列圖過於龐大。
3. **一致性**：序列圖應該與其他 UML 圖表保持一致，特別是類圖和活動圖，確保系統的靜態結構和動態行為一致。
4. **關注點分離**：序列圖應該關注特定的場景或功能，避免將多個場景或功能混在一起，確保每個序列圖都有明確的目的和範圍。

### 5.7 序列圖與其他 UML 圖表的關係
序列圖與其他 UML 圖表有著緊密的關係，它們共同描述了系統的靜態結構和動態行為。具體來說，序列圖與其他 UML 圖表的關係包括：

1. **類圖（Class Diagram）**：類圖描述系統的靜態結構，定義了類及其屬性和操作；序列圖描述系統的動態行為，展示了對象之間的交互和消息傳遞。序列圖中的對象和消息應該與類圖中的類和操作對應。
2. **活動圖（Activity Diagram）**：活動圖描述系統中的活動流程和控制流；序列圖描述對象之間的交互過程。序列圖中的消息和交互過程可以對應到活動圖中的活動和控制流。
3. **用例圖（Use Case Diagram）**：用例圖描述系統的功能需求和參與者；序列圖描述用例中的具體場景和交互過程。序列圖中的對象和消息應該與用例圖中的用例和參與者對應。
4. **狀態圖（State Diagram）**：狀態圖描述對象的狀態變化和事件；序列圖描述對象之間的交互和消息傳遞。序列圖中的消息可以觸發狀態圖中的狀態變化。

### 5.8 小結
本章介紹了序列圖的基本概念、構成元素、繪製步驟和實踐應用。通過這些內容，我們對序列圖有了深入的理解，並掌握了序列圖與其他 UML 圖表的關係。在接下來的章節中，我們將繼續學習 UML 的其他圖表及其應用，並通過實踐活動進一步掌握 UML 的使用技巧。
第 6 章：活動圖（Activity Diagram）
### 6.1 活動圖概述

<figure class="fig-svg"><svg viewBox="0 0 860 240" width="100%" role="img" aria-label="UML 活動圖：瀏覽活動、判斷名額、填表報名或顯示已滿" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><circle cx="60" cy="60" r="14" fill="#39d0d8"/><rect x="20" y="100" width="160" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="100" y="128" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">瀏覽活動</text><text x="300" y="76" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#e6edf3">名額足夠？</text><polygon points="300,90 380,124 300,158 220,124" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><rect x="430" y="96" width="150" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="505" y="124" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">填表報名</text><rect x="430" y="186" width="150" height="56" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="505" y="214" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">顯示已滿</text><rect x="700" y="96" width="130" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="765" y="124" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">送出報名</text><circle cx="790" cy="200" r="16" fill="none" stroke="#2c6fb1" stroke-width="2"/><circle cx="790" cy="200" r="10" fill="#39d0d8"/><line x1="60" y1="74" x2="60" y2="96" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="100" y1="156" x2="216" y2="132" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="380" y1="124" x2="426" y2="124" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="392" y="116" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#7ee787">是</text><line x1="300" y1="158" x2="300" y2="214" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="300" y1="214" x2="426" y2="214" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="310" y="206" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#f0a04b">否</text><line x1="580" y1="124" x2="696" y2="124" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="765" y1="152" x2="788" y2="182" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="580" y1="214" x2="772" y2="206" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/></svg><figcaption>圖　活動圖：實心圓是起點、同心圓是終點；菱形是判斷節點，兩條分支各自走到結束。</figcaption></figure>
活動圖（Activity Diagram）是 UML 的一種圖表，用於描述系統中的活動流程和控制流。它展示了系統的動態行為，特別是流程驅動的行為。活動圖類似於流程圖，適用於描述業務過程、工作流程和操作中的邏輯。
### 6.2 活動圖的基本元素
活動圖由以下基本元素組成：

1. **活動（Activity）**：表示一個具體的工作或行動，通常用圓角矩形表示。
2. **流程（Flow）**：表示活動之間的控制流或數據流，通常用箭頭表示。
3. **初始節點（Initial Node）**：表示活動流程的開始，通常用實心圓表示。
4. **終止節點（Final Node）**：表示活動流程的結束，終止節點分為活動終止節點（實心圓內帶圓圈）和流程終止節點（實心圓）。
5. **決策節點（Decision Node）**：表示流程的分支，通常用菱形表示，並在分支箭頭上標註條件。
6. **合併節點（Merge Node）**：表示分支流程的合併，通常用菱形表示。
7. **分叉節點（Fork Node）**：表示流程的並行分叉，通常用實心長方形表示。
8. **匯合節點（Join Node）**：表示並行流程的匯合，通常用實心長方形表示。
9. **泳道（Swimlane）**：表示活動的責任方或參與者，將活動圖劃分為若干區域，每個區域代表一個責任方或參與者。

### 6.3 活動圖的繪製步驟
繪製活動圖的一般步驟如下：

1. **識別活動和流程**：根據需求識別系統中的具體活動和流程，並繪製出這些活動和流程。
2. **定義初始和終止節點**：在活動圖上標註初始節點和終止節點，明確活動流程的開始和結束。
3. **建立活動之間的流程**：根據活動之間的邏輯關係，建立活動之間的流程，並用箭頭表示。
4. **添加決策和合併節點**：根據需求添加決策節點和合併節點，標註條件和合併點。
5. **添加分叉和匯合節點**：根據需求添加分叉節點和匯合節點，表示並行流程的分叉和匯合。
6. **劃分泳道**：根據活動的責任方或參與者，將活動圖劃分為若干泳道，每個泳道代表一個責任方或參與者。
7. **檢查和完善**：檢查活動圖的完整性和正確性，確保所有的活動、流程和控制結構都得到了描述，並根據反饋進行完善。

### 6.4 活動圖的實例分析
為了更好地理解活動圖的使用，我們來看一個具體的實例：一個簡單的訂單處理系統中的活動圖。<br />
**識別活動和流程**：根據需求識別系統中的具體活動：

- 接收訂單 (Receive Order)
- 驗證訂單 (Validate Order)
- 確認庫存 (Check Inventory)
- 生成發票 (Generate Invoice)
- 發送發票 (Send Invoice)
- 發貨（Ship Order）

定義初始和終止節點：

- **初始節點**：開始訂單處理（Start Order Processing）
- **終止節點**：完成訂單處理（Order Processing Complete）

建立活動之間的流程：

- 開始訂單處理 → 接收訂單 → 驗證訂單 → 確認庫存
- 確認庫存 → 生成發票 → 發送發票 → 發貨 → 完成訂單處理

添加決策和合併節點：

- 驗證訂單後，如果訂單有效，則進行確認庫存；如果訂單無效，則結束處理。

下面是這個訂單處理系統的活動圖示例：

<figure class="fig-svg"><svg viewBox="0 0 860 720" width="100%" role="img" aria-label="UML 活動圖：訂單處理流程，含訂單有效性的決策分支" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><circle cx="330" cy="40" r="11" fill="#e6edf3"/><line x1="330" y1="51" x2="330" y2="74" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="230" y="76" width="200" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="330" y="108" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">接收訂單</text><line x1="330" y1="128" x2="330" y2="154" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="230" y="156" width="200" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="330" y="188" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">驗證訂單</text><line x1="330" y1="208" x2="330" y2="236" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><polygon points="330,238 410,283 330,328 250,283" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="330" y="288" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">訂單有效？</text><line x1="330" y1="328" x2="330" y2="350" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="340" y="344" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">是</text><rect x="230" y="352" width="200" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="330" y="384" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">確認庫存</text><line x1="330" y1="404" x2="330" y2="430" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="230" y="432" width="200" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="330" y="464" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">生成發票</text><line x1="330" y1="484" x2="330" y2="510" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="230" y="512" width="200" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="330" y="544" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">發送發票</text><line x1="330" y1="564" x2="330" y2="590" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="230" y="592" width="200" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="330" y="624" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">發貨</text><line x1="330" y1="644" x2="330" y2="668" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><circle cx="330" cy="682" r="13" fill="none" stroke="#e6edf3" stroke-width="1.8"/><circle cx="330" cy="682" r="7" fill="#e6edf3"/><text x="352" y="687" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">終止節點（完成訂單處理）</text><line x1="410" y1="283" x2="466" y2="283" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="424" y="275" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">否</text><rect x="468" y="257" width="170" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="553" y="278" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">結束處理</text><text x="553" y="296" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="10.5" fill="#39d0d8">（訂單無效）</text></svg><figcaption>圖　活動圖：接收訂單後驗證，訂單有效才確認庫存、生成與發送發票、發貨；無效則直接結束處理。</figcaption></figure>
### 6.5 活動圖的實踐應用
活動圖在軟件開發的各個階段都有廣泛應用，特別是在需求分析和系統設計階段。具體來說，活動圖的實踐應用包括：

1. **業務過程建模**：活動圖幫助開發團隊和業務人員捕捉和分析業務過程，理解和描述業務活動和流程。
2. **工作流程設計**：活動圖為工作流程設計提供了詳細的視圖，幫助設計師和開發人員設計和實現系統的工作流程。
3. **功能設計和實現**：活動圖為系統功能設計和實現提供了詳細的動態視圖，幫助開發人員編寫代碼並實現系統功能。
4. **測試用例設計**：活動圖為測試人員設計測試用例提供了依據，幫助確保系統的動態行為和流程都能被測試覆蓋。
5. **系統文檔編寫**：活動圖可以作為系統設計文檔的一部分，幫助開發團隊和其他相關人員理解和記錄系統的動態行為。

### 6.6 活動圖的設計原則
在設計活動圖時，需要遵循以下幾個重要的設計原則：

1. **簡潔明瞭**：活動圖應該清晰明瞭，避免過於複雜和冗長。每個活動和流程都應該有明確的標識和描述。
2. **合理分解**：對於複雜的活動流程，可以將其分解成多個子流程，用多個活動圖分別描述，避免單個活動圖過於龐大。
3. **一致性**：活動圖應該與其他 UML 圖表保持一致，特別是用例圖和序列圖，確保系統的靜態結構和動態行為一致。
4. **關注點分離**：活動圖應該關注特定的活動或流程，避免將多個活動或流程混在一起，確保每個活動圖都有明確的目的和範圍。
5. **考慮異常流程**：在設計活動圖時，應該考慮可能的異常流程和處理方式，確保系統能夠應對各種情況。

### 6.7 活動圖與其他 UML 圖表的關係
活動圖與其他 UML 圖表有著緊密的關係，它們共同描述了系統的靜態結構和動態行為。具體來說，活動圖與其他 UML 圖表的關係包括：

1. **用例圖（Use Case Diagram）**：用例圖描述系統的功能需求和參與者；活動圖描述用例中的具體活動和流程。活動圖中的活動和流程應該與用例圖中的用例對應。
2. **序列圖（Sequence Diagram）**：序列圖描述對象之間的交互過程和消息傳遞；活動圖描述活動之間的流程和控制流。序列圖中的消息和交互過程可以對應到活動圖中的活動和流程。
3. **狀態圖（State Diagram）**：狀態圖描述對象的狀態變化和事件；活動圖描述活動之間的流程和控制流。活動圖中的流程和控制流可以觸發狀態圖中的狀態變化。
4. **類圖（Class Diagram）**：類圖描述系統的靜態結構，定義了類及其屬性和操作；活動圖描述系統的動態行為，展示了活動之間的流程和控制流。活動圖中的活動和流程應該與類圖中的類和操作對應。

### 6.8 小結
本章介紹了活動圖的基本概念、構成元素、繪製步驟和實踐應用。通過這些內容，我們對活動圖有了深入的理解，並掌握了活動圖與其他 UML 圖表的關係。在接下來的章節中，我們將繼續學習 UML 的其他圖表及其應用，並通過實踐活動進一步掌握 UML 的使用技巧。
第7章：狀態圖（State Diagram）
### 7.1 狀態圖概述

<figure class="fig-svg"><svg viewBox="0 0 830 240" width="100%" role="img" aria-label="UML 狀態圖：草稿、已發佈、已下架三個狀態與轉換" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="40" y="96" width="170" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="125" y="121" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">草稿</text><text x="125" y="141" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">draft</text><rect x="330" y="96" width="170" height="62" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="415" y="121" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">已發佈</text><text x="415" y="141" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">published</text><rect x="620" y="96" width="170" height="62" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="705" y="121" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">已下架</text><text x="705" y="141" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">archived</text><circle cx="20" cy="127" r="10" fill="#39d0d8"/><line x1="30" y1="127" x2="36" y2="127" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="210" y1="127" x2="326" y2="127" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="222" y="118" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#7ee787">發佈</text><line x1="500" y1="127" x2="616" y2="127" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="512" y="118" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#f0a04b">下架</text><path d="M415 158 Q415 196 300 196 Q120 196 120 162" fill="none" stroke="#39d0d8" stroke-width="1.5" marker-end="url(#a)"/><text x="250" y="214" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">編輯（回到草稿）</text></svg><figcaption>圖　狀態圖：圓角框是狀態、箭頭是轉換；「編輯」會讓已發佈的文章回到草稿狀態。</figcaption></figure>
狀態圖（State Diagram）是 UML 的一種圖表，用於描述對象在其生命週期中所經歷的各種狀態以及導致狀態變化的事件。狀態圖特別適合於描述具有複雜狀態轉換的對象或系統，例如控制系統、工作流管理系統和實時系統。
### 7.2 狀態圖的基本元素
狀態圖由以下基本元素組成：

1. **狀態（State）**：表示對象在某一時刻的狀態，通常用圓角矩形表示。
2. **轉換（Transition）**：表示對象從一個狀態轉換到另一個狀態的過程，通常用帶箭頭的線表示。
3. **事件（Event）**：觸發狀態轉換的事件，通常標註在轉換箭頭旁。
4. **動作（Action）**：在狀態或轉換過程中執行的行為，通常標註在狀態或轉換箭頭旁。
5. **初始狀態（Initial State）**：表示狀態機的開始狀態，通常用實心圓表示。
6. **終止狀態（Final State）**：表示狀態機的結束狀態，通常用實心圓內帶圓圈表示。

### 7.3 狀態圖的繪製步驟
繪製狀態圖的一般步驟如下：

1. **識別狀態**：根據需求識別對象在其生命週期中所經歷的各種狀態，並繪製出這些狀態。
2. **定義初始和終止狀態**：在狀態圖上標註初始狀態和終止狀態，明確狀態機的開始和結束。
3. **建立狀態之間的轉換**：根據狀態之間的相互關係，建立狀態之間的轉換，並用箭頭表示。
4. **標註事件和動作**：在轉換箭頭旁標註觸發轉換的事件和執行的動作，描述狀態轉換的條件和過程。
5. **檢查和完善**：檢查狀態圖的完整性和正確性，確保所有的狀態、轉換、事件和動作都得到了描述，並根據反饋進行完善。

### 7.4 狀態圖的實例分析
為了更好地理解狀態圖的使用，我們來看一個具體的實例：一個簡單的門鎖系統的狀態圖。<br />
**識別狀態**：根據需求識別門鎖系統的各種狀態：

- 門鎖關閉 (Locked)
- 門鎖打開 (Unlocked)
- 門鎖報警 (Alarmed)

定義初始和終止狀態：

- **初始狀態**：門鎖關閉 (Locked)
- **終止狀態**：無（因為門鎖系統是持續運行的）

建立狀態之間的轉換：

- 門鎖關閉 → 門鎖打開：插入正確鑰匙
- 門鎖打開 → 門鎖關閉：拔出鑰匙
- 門鎖關閉 → 門鎖報警：插入錯誤鑰匙
- 門鎖報警 → 門鎖關閉：報警解除

標註事件和動作：

- **插入正確鑰匙**：Unlock（解鎖）
- **拔出鑰匙**：Lock（上鎖）
- **插入錯誤鑰匙**：Trigger Alarm（觸發報警）
- **報警解除**：Reset Alarm（重置報警）

下面是這個門鎖系統的狀態圖示例：

<figure class="fig-svg"><svg viewBox="0 0 860 400" width="100%" role="img" aria-label="UML 狀態圖：門鎖系統的關閉、打開與報警三種狀態及轉換" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><circle cx="240" cy="50" r="9" fill="#e6edf3"/><line x1="240" y1="59" x2="240" y2="106" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="140" y="110" width="200" height="56" rx="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="240" y="145" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">門鎖關閉（Locked）</text><rect x="140" y="300" width="200" height="56" rx="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="240" y="335" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">門鎖打開（Unlocked）</text><rect x="600" y="205" width="200" height="56" rx="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="700" y="240" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">門鎖報警（Alarmed）</text><line x1="205" y1="166" x2="205" y2="296" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="196" y="236" text-anchor="end" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">Unlock（插入正確鑰匙）</text><line x1="275" y1="296" x2="275" y2="166" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="284" y="236" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">Lock（拔出鑰匙）</text><line x1="340" y1="148" x2="594" y2="222" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="516" y="144" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">Trigger（插入錯誤鑰匙）</text><line x1="700" y1="205" x2="352" y2="124" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="520" y="96" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">Reset Alarm（報警解除）</text></svg><figcaption>圖　狀態圖：插入正確鑰匙由關閉轉為打開、拔出鑰匙回到關閉、插入錯誤鑰匙觸發報警，報警解除後回到關閉。</figcaption></figure>
### 7.5 狀態圖的實踐應用
狀態圖在軟件開發的各個階段都有廣泛應用，特別是在需求分析和系統設計階段。具體來說，狀態圖的實踐應用包括：

1. **狀態驅動系統建模**：狀態圖幫助開發團隊和業務人員捕捉和分析狀態驅動的系統行為，理解和描述對象在其生命週期中的狀態轉換。
2. **系統設計和實現**：狀態圖為系統設計和實現提供了詳細的動態視圖，幫助設計師和開發人員設計和實現系統的狀態機。
3. **測試用例設計**：狀態圖為測試人員設計測試用例提供了依據，幫助確保系統的狀態轉換和動態行為都能被測試覆蓋。
4. **系統文檔編寫**：狀態圖可以作為系統設計文檔的一部分，幫助開發團隊和其他相關人員理解和記錄系統的動態行為。

### 7.6 狀態圖的設計原則
在設計狀態圖時，需要遵循以下幾個重要的設計原則：

1. **簡潔明瞭**：狀態圖應該清晰明瞭，避免過於複雜和冗長。每個狀態和轉換都應該有明確的標識和描述。
2. **合理分解**：對於複雜的狀態機，可以將其分解成多個子狀態機，用多個狀態圖分別描述，避免單個狀態圖過於龐大。
3. **一致性**：狀態圖應該與其他 UML 圖表保持一致，特別是用例圖和活動圖，確保系統的靜態結構和動態行為一致。
4. **關注點分離**：狀態圖應該關注特定的對象或系統，避免將多個對象或系統的狀態機混在一起，確保每個狀態圖都有明確的目的和範圍。
5. **考慮異常狀態**：在設計狀態圖時，應該考慮可能的異常狀態和處理方式，確保系統能夠應對各種情況。

### 7.7 狀態圖與其他 UML 圖表的關係
狀態圖與其他 UML 圖表有著緊密的關係，它們共同描述了系統的靜態結構和動態行為。具體來說，狀態圖與其他 UML 圖表的關係包括：

1. **用例圖（Use Case Diagram）**：用例圖描述系統的功能需求和參與者；狀態圖描述用例中的具體狀態和狀態轉換。狀態圖中的狀態和轉換應該與用例圖中的用例和參與者對應。
2. **活動圖（Activity Diagram）**：活動圖描述活動之間的流程和控制流；狀態圖描述對象在其生命週期中的狀態和狀態轉換。活動圖中的活動和流程可以對應到狀態圖中的狀態和轉換。
3. **序列圖（Sequence Diagram）**：序列圖描述對象之間的交互過程和消息傳遞；狀態圖描述對象的狀態變化和狀態轉換。序列圖中的消息可以觸發狀態圖中的狀態變化。
4. **類圖（Class Diagram）**：類圖描述系統的靜態結構，定義了類及其屬性和操作；狀態圖描述對象的動態行為，展示了對象在其生命週期中的狀態和狀態轉換。狀態圖中的狀態和轉換應該與類圖中的類和操作對應。
### 7.8 小結
本章介紹了狀態圖的基本概念、構成元素、繪製步驟和實踐應用。通過這些內容，我們對狀態圖有了深入的理解，並掌握了狀態圖與其他 UML 圖表的關係。在接下來的章節中，我們將繼續學習 UML 的其他圖表及其應用，並通過實踐活動進一步掌握 UML 的使用技巧。
第 8 章：組件圖（Component Diagram）
### 8.1 組件圖概述

<figure class="fig-svg"><svg viewBox="0 0 860 210" width="100%" role="img" aria-label="UML 組件圖：模板層、視圖層、模型層與資料庫的依賴關係" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="30" y="90" width="170" height="66" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="115" y="117" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">模板層</text><text x="115" y="137" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">templates／block</text><rect x="178" y="98" width="14" height="22" rx="2" fill="#0d1117" stroke="#39d0d8" stroke-width="1.2"/><line x1="182" y1="105" x2="188" y2="105" stroke="#39d0d8" stroke-width="1.2"/><rect x="250" y="90" width="180" height="66" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="340" y="117" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">視圖層</text><text x="340" y="137" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">views.py</text><rect x="408" y="98" width="14" height="22" rx="2" fill="#0d1117" stroke="#39d0d8" stroke-width="1.2"/><line x1="412" y1="105" x2="418" y2="105" stroke="#39d0d8" stroke-width="1.2"/><rect x="480" y="90" width="180" height="66" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="570" y="117" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">模型層</text><text x="570" y="137" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">models.py／ORM</text><rect x="638" y="98" width="14" height="22" rx="2" fill="#0d1117" stroke="#39d0d8" stroke-width="1.2"/><line x1="642" y1="105" x2="648" y2="105" stroke="#39d0d8" stroke-width="1.2"/><rect x="700" y="90" width="130" height="66" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="765" y="117" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">資料庫</text><text x="765" y="137" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">PostgreSQL</text><rect x="808" y="98" width="14" height="22" rx="2" fill="#0d1117" stroke="#39d0d8" stroke-width="1.2"/><line x1="812" y1="105" x2="818" y2="105" stroke="#39d0d8" stroke-width="1.2"/><line x1="200" y1="123" x2="246" y2="123" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="430" y1="123" x2="476" y2="123" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="660" y1="123" x2="696" y2="123" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="30" y="60" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#e6edf3">方框右上角是 UML 的 component 標記</text><text x="30" y="196" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">箭頭由左往右：上層依賴下層</text></svg><figcaption>圖　組件圖：每個方框是一個可替換的元件，箭頭代表依賴；視圖層依賴模型層，模型層依賴資料庫。</figcaption></figure>
組件圖（Component Diagram）是 UML 的一種圖表，用於描述系統中的物理組件及其相互之間的關係。組件圖展示了系統的物理結構，特別是系統中各個組件如何協作來完成系統功能。組件圖特別適合於描述大型系統的模塊化結構，幫助開發者理解和設計系統的物理架構。
### 8.2 組件圖的基本元素
組件圖由以下基本元素組成：

1. **組件（Component）**：表示系統中的物理模塊或代碼單元，通常用矩形表示，矩形左上角有一個小矩形標識，組件內部可以標註組件的名稱和接口。
2. **接口（Interface）**：表示組件提供或需要的功能，通常用小圓圈或帶箭頭的小矩形表示。提供接口（provided interface）用小圓圈表示，需求接口（required interface）用帶箭頭的小矩形表示。
3. **依賴關係（Dependency）**：表示組件之間的依賴關係，通常用虛線箭頭表示，箭頭指向被依賴的組件或接口。
4. **連接器（Connector）**：表示組件之間的通信通道，通常用實線表示，用於連接組件和接口。

### 8.3 組件圖的繪製步驟
繪製組件圖的一般步驟如下：

1. **識別組件**：根據需求識別系統中的主要組件，並繪製出這些組件的矩形。
2. **定義接口**：為每個組件定義提供和需求的接口，並用小圓圈和小矩形表示。
3. **建立依賴關係**：根據組件之間的相互依賴，建立組件之間的依賴關係，並用虛線箭頭表示。
4. **添加連接器**：根據需求添加組件之間的連接器，表示組件之間的通信通道。
5. **檢查和完善**：檢查組件圖的完整性和正確性，確保所有的組件、接口、依賴關係和連接器都得到了描述，並根據反饋進行完善。

### 8.4 組件圖的實例分析
為了更好地理解組件圖的使用，我們來看一個具體的實例：一個簡單的網絡購物系統的組件圖。<br />
**識別組件**：根據需求識別系統中的主要組件：

- 用戶界面 (User Interface)
- 購物車 (Shopping Cart)
- 訂單處理 (Order Processing)
- 支付網關 (Payment Gateway)
- 資料庫 (Database)

定義接口：

- 用戶界面提供和需求的接口：顯示商品（Display Products）、添加到購物車（Add to Cart）、提交訂單（Submit Order）
- 購物車提供和需求的接口：計算總價（Calculate Total）、顯示購物車（View Cart）
- 訂單處理提供和需求的接口：處理訂單（Process Order）、更新庫存（Update Inventory）
- 支付網關提供和需求的接口：處理支付（Process Payment）
- 資料庫提供和需求的接口：查詢庫存（Query Inventory）、更新庫存（Update Inventory）

建立依賴關係：

- 用戶界面依賴購物車和訂單處理
- 購物車依賴資料庫
- 訂單處理依賴支付網關和資料庫

添加連接器：

- 用戶界面連接到購物車和訂單處理的接口
- 購物車連接到資料庫的接口
- 訂單處理連接到支付網關和資料庫的接口

下面是這個網絡購物系統的組件圖示例：

<figure class="fig-svg"><svg viewBox="0 0 860 540" width="100%" role="img" aria-label="UML 組件圖：User Interface、Shopping Cart、Order Processing、Database、Payment Gateway" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="290" y="30" width="280" height="100" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="430" y="54" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">«component» User Interface</text><text x="304" y="76" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">• Display Products</text><text x="304" y="94" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">• Add to Cart</text><text x="304" y="112" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">• Submit Order</text><rect x="60" y="230" width="250" height="88" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="185" y="254" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">«component» Shopping Cart</text><text x="74" y="276" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">• Calculate Total</text><text x="74" y="294" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">• View Cart</text><rect x="550" y="230" width="260" height="88" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="680" y="254" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">«component» Order Processing</text><text x="564" y="276" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">• Process Order</text><text x="564" y="294" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">• Update Inventory</text><rect x="60" y="420" width="250" height="88" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="185" y="444" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">«component» Database</text><text x="74" y="466" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">• Query Inventory</text><text x="74" y="484" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">• Update Inventory</text><rect x="550" y="420" width="260" height="88" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="680" y="444" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">«component» Payment Gateway</text><text x="564" y="466" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">• Process Payment</text><line x1="350" y1="130" x2="195" y2="226" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="510" y1="130" x2="665" y2="226" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="185" y1="318" x2="185" y2="416" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="650" y1="318" x2="650" y2="416" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="560" y1="318" x2="300" y2="418" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/></svg><figcaption>圖　組件圖：用戶界面接到購物車與訂單處理，購物車與訂單處理共用資料庫，訂單處理再接到支付網關。</figcaption></figure>
### 8.5 組件圖的實踐應用
組件圖在軟件開發的各個階段都有廣泛應用，特別是在系統設計和架構設計階段。具體來說，組件圖的實踐應用包括：

1. **模塊化設計**：組件圖幫助開發團隊進行系統的模塊化設計，確定系統中的主要組件及其相互依賴關係，從而提高系統的可維護性和可擴展性。
2. **接口設計**：組件圖為組件之間的接口設計提供了詳細的視圖，幫助設計師和開發人員定義組件提供和需求的接口，從而確保組件之間的良好協作。
3. **系統集成**：組件圖為系統集成提供了指導，幫助開發團隊理解和實現組件之間的通信和依賴關係，從而確保系統的正常運行。
4. **測試用例設計**：組件圖為測試人員設計測試用例提供了依據，幫助確保系統的組件和接口都能被測試覆蓋，從而提高系統的可靠性。
5. **系統文檔編寫**：組件圖可以作為系統設計文檔的一部分，幫助開發團隊和其他相關人員理解和記錄系統的物理架構。

### 8.6 組件圖的設計原則
在設計組件圖時，需要遵循以下幾個重要的設計原則：

1. **簡潔明瞭**：組件圖應該清晰明瞭，避免過於複雜和冗長。每個組件和接口都應該有明確的標識和描述。
2. **高內聚低耦合**：組件之間應該遵循高內聚低耦合的設計原則，確保組件內部功能的緊密相關性和組件之間的低依賴性，從而提高系統的可維護性和可擴展性。
3. **一致性**：組件圖應該與其他 UML 圖表保持一致，特別是類圖和序列圖，確保系統的靜態結構和動態行為一致。
4. **關注點分離**：組件圖應該關注特定的系統層次或模塊，避免將不同層次或模塊的組件混在一起，確保每個組件圖都有明確的目的和範圍。
5. **考慮重用性**：在設計組件圖時，應該考慮組件的重用性，確保組件可以在不同系統或項目中重用，從而提高開發效率和降低成本。

### 8.7 組件圖與其他 UML 圖表的關係
組件圖與其他 UML 圖表有著緊密的關係，它們共同描述了系統的靜態結構和動態行為。具體來說，組件圖與其他 UML 圖表的關係包括：

1. **類圖（Class Diagram）**：類圖描述系統的靜態結構，定義了類及其屬性和操作；組件圖描述系統的物理結構，展示了系統中的物理組件及其相互之間的關係。組件圖中的組件和接口應該與類圖中的類和操作對應。
2. **序列圖（Sequence Diagram）**：序列圖描述對象之間的交互過程和消息傳遞；組件圖描述組件之間的依賴關係和通信通道。序列圖中的對象交互和消息傳遞應該與組件圖中的組件依賴和連接器對應。
3. **用例圖（Use Case Diagram）**：用例圖描述系統的功能需求和參與者；組件圖描述系統的物理結構和組件之間的關係。用例圖中的功能需求應該分配到組件圖中的組件上。
4. **活動圖（Activity Diagram）**：活動圖描述活動之間的流程和控制流；組件圖描述組件之間的依賴關係和通信通道。活動圖中的活動和流程可以對應到組件圖中的組件和接口。
### 8.8 小結
本章介紹了組件圖的基本概念、構成元素、繪製步驟和實踐應用。通過這些內容，我們對組件圖有了深入的理解，並掌握了組件圖與其他 UML 圖表的關係。在接下來的章節中，我們將繼續學習 UML 的其他圖表及其應用，並通過實踐活動進一步掌握 UML 的使用技巧。
第 9 章：部署圖（Deployment Diagram）
### 9.1 部署圖概述

<figure class="fig-svg"><svg viewBox="0 0 860 228" width="100%" role="img" aria-label="UML 部署圖：使用者端瀏覽器、伺服器節點的 Nginx／Gunicorn／Django／PostgreSQL" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="26" width="220" height="180" rx="12" fill="none" stroke="#2c6fb1" stroke-width="1.4"/><text x="130" y="48" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">使用者端</text><rect x="50" y="70" width="160" height="100" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="130" y="114" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">瀏覽器</text><text x="130" y="134" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">HTML／CSS／JS</text><rect x="270" y="26" width="300" height="190" rx="12" fill="none" stroke="#2c6fb1" stroke-width="1.4"/><text x="420" y="48" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">伺服器節點</text><rect x="292" y="66" width="120" height="60" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="352" y="90" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">Nginx</text><text x="352" y="110" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">靜態／代理</text><rect x="432" y="66" width="122" height="60" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="493" y="90" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">Gunicorn</text><text x="493" y="110" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">WSGI</text><rect x="292" y="158" width="120" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="352" y="178" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">Django</text><text x="352" y="198" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">應用程式</text><rect x="432" y="158" width="122" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="493" y="178" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">PostgreSQL</text><text x="493" y="198" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">資料庫</text><rect x="630" y="66" width="180" height="126" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="720" y="123" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">物件儲存</text><text x="720" y="143" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">媒體檔案／備份</text><line x1="210" y1="120" x2="288" y2="96" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="412" y1="96" x2="428" y2="96" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="352" y1="128" x2="352" y2="154" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="493" y1="128" x2="493" y2="154" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="554" y1="100" x2="626" y2="100" stroke="#39d0d8" stroke-width="1.5" stroke-dasharray="4 3"/></svg><figcaption>圖　部署圖：外框是節點（node），裡面的方框是執行的元件；Nginx 轉給 Gunicorn，Django 連 PostgreSQL 與物件儲存。</figcaption></figure>
部署圖（Deployment Diagram）是 UML 的一種圖表，用於描述系統的物理部署結構。它展示了系統的硬件節點、軟件構件以及它們之間的關係，幫助開發者理解和設計系統的物理架構。部署圖特別適合於描述分佈式系統和網絡系統的部署情況，幫助確保系統的性能、可靠性和可擴展性。
### 9.2 部署圖的基本元素
部署圖由以下基本元素組成：

1. **節點（Node）**：表示系統中的硬件設備或運行時環境，通常用立方體表示。節點可以分為設備節點（Device Node）和執行環境節點（Execution Environment Node）。
2. **構件（Component）**：表示運行在節點上的軟件模塊或應用程序，通常用矩形表示。
3. **關係（Relationship）**：表示節點和構件之間的關係，通常用實線表示。
4. **接口（Interface）**：表示構件提供或需要的功能，通常用小圓圈或帶箭頭的小矩形表示。
5. **連接器（Connector）**：表示節點或構件之間的通信通道，通常用實線或虛線表示。

### 9.3 部署圖的繪製步驟
繪製部署圖的一般步驟如下：

1. **識別節點**：根據需求識別系統中的主要節點，並繪製出這些節點的立方體。
2. **定義構件**：為每個節點定義運行在其上的構件，並用矩形表示。
3. **建立關係**：根據節點和構件之間的相互關係，建立節點和構件之間的關係，並用實線表示。
4. **添加接口**：根據需求添加構件的接口，表示構件提供或需要的功能。
5. **添加連接器**：根據需求添加節點或構件之間的連接器，表示通信通道。
6. **檢查和完善**：檢查部署圖的完整性和正確性，確保所有的節點、構件、關係、接口和連接器都得到了描述，並根據反饋進行完善。

### 9.4 部署圖的實例分析
為了更好地理解部署圖的使用，我們來看一個具體的實例：一個簡單的企業應用系統的部署圖。<br />
**識別節點**：根據需求識別系統中的主要節點：

- 客戶端 (Client)
- 應用服務器 (Application Server)
- 數據庫服務器 (Database Server)

定義構件：

- 客戶端運行 Web 瀏覽器構件
- 應用服務器運行 Web 應用構件
- 數據庫服務器運行數據庫構件

建立關係：

- 客戶端與應用服務器之間有通信關係
- 應用服務器與數據庫服務器之間有通信關係

添加接口：

- Web 應用構件提供 HTTP 接口
- 數據庫構件提供 SQL 接口

添加連接器：

- 客戶端連接到應用服務器的 HTTP 接口
- 應用服務器連接到數據庫服務器的 SQL 接口

下面是這個企業應用系統的部署圖示例：

<figure class="fig-svg"><svg viewBox="0 0 860 640" width="100%" role="img" aria-label="UML 部署圖：客戶端、應用服務器與數據庫服務器三個節點及其構件" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="270" y="20" width="320" height="128" rx="8" fill="none" stroke="#2c6fb1" stroke-width="1.8"/><rect x="270" y="20" width="320" height="28" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="430" y="39" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">«device» 客戶端 Client</text><rect x="286" y="66" width="288" height="34" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.4"/><text x="430" y="88" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#e6edf3">«artifact» Web 瀏覽器構件</text><rect x="270" y="208" width="320" height="172" rx="8" fill="none" stroke="#2c6fb1" stroke-width="1.8"/><rect x="270" y="208" width="320" height="28" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="430" y="227" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">«device» 應用服務器 Application Server</text><rect x="286" y="254" width="288" height="34" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.4"/><text x="430" y="276" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#e6edf3">«artifact» Web 應用構件</text><rect x="286" y="300" width="288" height="34" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.4"/><text x="430" y="322" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#e6edf3">«artifact» HTTP 接口</text><rect x="270" y="440" width="320" height="172" rx="8" fill="none" stroke="#2c6fb1" stroke-width="1.8"/><rect x="270" y="440" width="320" height="28" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="430" y="459" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">«device» 數據庫服務器 Database Server</text><rect x="286" y="486" width="288" height="34" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.4"/><text x="430" y="508" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#e6edf3">«artifact» 資料庫構件</text><rect x="286" y="532" width="288" height="34" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.4"/><text x="430" y="554" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#e6edf3">«artifact» SQL 接口</text><line x1="430" y1="148" x2="430" y2="204" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="430" y1="380" x2="430" y2="436" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="440" y="182" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">HTTP</text><text x="440" y="414" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">SQL</text></svg><figcaption>圖　部署圖：客戶端的瀏覽器構件以 HTTP 連到應用服務器（Web 應用構件、HTTP 接口），再以 SQL 連到數據庫服務器（資料庫構件、SQL 接口）。</figcaption></figure>
### 9.5 部署圖的實踐應用
部署圖在軟件開發的各個階段都有廣泛應用，特別是在系統設計和部署階段。具體來說，部署圖的實踐應用包括：

1. **系統架構設計**：部署圖幫助開發團隊進行系統的架構設計，確定系統中的硬件節點、軟件構件及其相互關係，從而提高系統的性能、可靠性和可擴展性。
2. **部署方案設計**：部署圖為系統的部署方案設計提供了詳細的視圖，幫助設計師和運維人員規劃系統的物理部署，確保系統能夠在預期的運行環境中正常運行。
3. **系統集成和測試**：部署圖為系統集成和測試提供了指導，幫助開發團隊理解和實現節點和構件之間的通信和依賴關係，從而確保系統的正常運行。
4. **系統文檔編寫**：部署圖可以作為系統設計和部署文檔的一部分，幫助開發團隊和其他相關人員理解和記錄系統的物理架構和部署方案。

### 9.6 部署圖的設計原則
在設計部署圖時，需要遵循以下幾個重要的設計原則：

1. **簡潔明瞭**：部署圖應該清晰明瞭，避免過於複雜和冗長。每個節點和構件都應該有明確的標識和描述。
2. **高內聚低耦合**：部署圖應該遵循高內聚低耦合的設計原則，確保系統中各個節點和構件內部功能的緊密相關性和節點之間的低依賴性，從而提高系統的可維護性和可擴展性。
3. **一致性**：部署圖應該與其他 UML 圖表保持一致，特別是組件圖和類圖，確保系統的靜態結構和動態行為一致。
4. **關注點分離**：部署圖應該關注特定的系統層次或模塊，避免將不同層次或模塊的節點和構件混在一起，確保每個部署圖都有明確的目的和範圍。
5. **考慮可擴展性**：在設計部署圖時，應該考慮系統的可擴展性，確保系統能夠應對未來的擴展需求，從而提高系統的可用性和靈活性。

### 9.7 部署圖與其他 UML 圖表的關係
部署圖與其他 UML 圖表有著緊密的關係，它們共同描述了系統的靜態結構和動態行為。具體來說，部署圖與其他 UML 圖表的關係包括：

1. **組件圖（Component Diagram）**：組件圖描述系統的物理結構和組件之間的關係；部署圖描述系統的物理部署結構和節點之間的關係。部署圖中的節點和構件應該與組件圖中的組件和接口對應。
2. **類圖（Class Diagram）**：類圖描述系統的靜態結構，定義了類及其屬性和操作；部署圖描述系統的物理部署結構和節點之間的關係。部署圖中的構件應該與類圖中的類和操作對應。
3. **序列圖（Sequence Diagram）**：序列圖描述對象之間的交互過程和消息傳遞；部署圖描述節點和構件之間的通信通道。序列圖中的對象交互和消息傳遞應該與部署圖中的節點和連接器對應。
4. **用例圖（Use Case Diagram）**：用例圖描述系統的功能需求和參與者；部署圖描述系統的物理部署結構和節點之間的關係。用例圖中的功能需求應該分配到部署圖中的構件上。

### 9.8 小結
本章介紹了部署圖的基本概念、構成元素、繪製步驟和實踐應用。通過這些內容，我們對部署圖有了深入的理解，並掌握了部署圖與其他 UML 圖表的關係。在接下來的章節中，我們將繼續學習 UML 的其他圖表及其應用，並通過實踐活動進一步掌握 UML 的使用技巧。
第 10 章：綜合案例分析與實踐應用
### 10.1 綜合案例簡介
在前面的章節中，我們學習了 UML 的各種圖表及其應用，包括用例圖、類圖、對象圖、序列圖、活動圖、狀態圖、組件圖和部署圖。為了鞏固這些知識，本章將通過一個綜合案例，展示如何在一個完整的軟件開發過程中應用這些 UML 圖表。我們將以一個線上圖書館管理系統為例，從需求分析到設計和部署，全面應用 UML 圖表。
### 10.2 案例需求分析
線上圖書館管理系統的主要功能包括：

1. 用戶註冊和登錄
2. 書籍瀏覽和搜索
3. 借閱書籍
4. 還書
5. 管理員管理書籍和用戶

### 10.3 用例圖設計
根據需求分析，繪製線上圖書館管理系統的用例圖。用例圖展示了系統的功能需求和參與者。
用例圖：

<figure class="fig-svg"><svg viewBox="0 0 860 580" width="100%" role="img" aria-label="UML 用例圖：線上圖書館管理系統的 7 個用例與用戶、管理員" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="250" y="20" width="380" height="540" rx="12" fill="none" stroke="#2c6fb1" stroke-width="1.6"/><text x="440" y="46" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">線上圖書館管理系統</text><ellipse cx="440" cy="84" rx="118" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="89" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">註冊</text><ellipse cx="440" cy="146" rx="118" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="151" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">登錄</text><ellipse cx="440" cy="208" rx="118" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="213" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">瀏覽／搜索書籍</text><ellipse cx="440" cy="270" rx="118" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="275" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">借閱書籍</text><ellipse cx="440" cy="332" rx="118" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="337" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">還書</text><ellipse cx="440" cy="394" rx="118" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="399" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">管理書籍</text><ellipse cx="440" cy="456" rx="118" ry="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.5"/><text x="440" y="461" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">管理用戶</text><rect x="30" y="170" width="140" height="50" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="100" y="200" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">用戶</text><line x1="170" y1="195" x2="322" y2="84" stroke="#39d0d8" stroke-width="1.4"/><line x1="170" y1="195" x2="322" y2="146" stroke="#39d0d8" stroke-width="1.4"/><line x1="170" y1="195" x2="322" y2="208" stroke="#39d0d8" stroke-width="1.4"/><line x1="170" y1="195" x2="322" y2="270" stroke="#39d0d8" stroke-width="1.4"/><line x1="170" y1="195" x2="322" y2="332" stroke="#39d0d8" stroke-width="1.4"/><rect x="690" y="372" width="140" height="50" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="760" y="402" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="15" fill="#e6edf3">管理員</text><line x1="690" y1="397" x2="558" y2="394" stroke="#39d0d8" stroke-width="1.4"/><line x1="690" y1="397" x2="558" y2="456" stroke="#39d0d8" stroke-width="1.4"/></svg><figcaption>圖　用例圖：用戶連到註冊、登錄、瀏覽／搜索書籍、借閱書籍、還書；管理員連到管理書籍、管理用戶。</figcaption></figure>

### 10.4 類圖設計
根據用例圖，繪製系統的類圖。類圖展示了系統的靜態結構，包括類、屬性、操作和類之間的關係。
類圖：

<figure class="fig-svg"><svg viewBox="0 0 860 430" width="100%" role="img" aria-label="UML 類圖：線上圖書館的 User、Loan、Book、Admin 四個類與關聯" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="90" width="190" height="94" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="20" y1="116" x2="210" y2="116" stroke="#2c6fb1" stroke-width="1.2"/><line x1="20" y1="146" x2="210" y2="146" stroke="#2c6fb1" stroke-width="1.2"/><text x="115" y="108" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">User 用戶</text><text x="30" y="136" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">- username: String</text><text x="30" y="164" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">+ register()</text><rect x="300" y="90" width="210" height="94" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="300" y1="116" x2="510" y2="116" stroke="#2c6fb1" stroke-width="1.2"/><line x1="300" y1="146" x2="510" y2="146" stroke="#2c6fb1" stroke-width="1.2"/><text x="405" y="108" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">Loan 借閱</text><text x="310" y="136" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">- loanDate: Date</text><text x="310" y="164" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">+ markReturned()</text><rect x="600" y="90" width="220" height="94" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="600" y1="116" x2="820" y2="116" stroke="#2c6fb1" stroke-width="1.2"/><line x1="600" y1="146" x2="820" y2="146" stroke="#2c6fb1" stroke-width="1.2"/><text x="710" y="108" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">Book 書籍</text><text x="610" y="136" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">- title: String</text><text x="610" y="164" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">+ getDetails()</text><rect x="300" y="300" width="210" height="94" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="300" y1="326" x2="510" y2="326" stroke="#2c6fb1" stroke-width="1.2"/><line x1="300" y1="356" x2="510" y2="356" stroke="#2c6fb1" stroke-width="1.2"/><text x="405" y="318" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">Admin 管理員</text><text x="310" y="346" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">- staffId: String</text><text x="310" y="374" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">+ manageBook()</text><line x1="210" y1="140" x2="296" y2="140" stroke="#39d0d8" stroke-width="1.6"/><text x="216" y="132" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">1 : *</text><line x1="510" y1="140" x2="596" y2="140" stroke="#39d0d8" stroke-width="1.6"/><text x="518" y="132" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">* : 1</text><line x1="480" y1="300" x2="700" y2="188" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="560" y="272" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">* : *</text></svg><figcaption>圖　類圖：User 1:N Loan、Loan N:1 Book、Admin N:N Book；每個類分三格（類名／屬性／操作）。</figcaption></figure>

### 10.5 對象圖設計
根據類圖，繪製系統的對象圖。對象圖展示了系統在某一時刻的對象實例及其之間的關係。
對象圖：

<figure class="fig-svg"><svg viewBox="0 0 860 190" width="100%" role="img" aria-label="UML 物件圖：用戶1、借閱1、書籍1 三個實例與借閱鏈接" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="20" y="60" width="250" height="74" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="20" y1="86" x2="270" y2="86" stroke="#2c6fb1" stroke-width="1.2"/><text x="145" y="78" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3" text-decoration="underline">用戶1 : User</text><text x="30" y="106" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">用戶名：Alice</text><text x="30" y="128" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">電子郵件：alice@example.com</text><rect x="330" y="60" width="250" height="74" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="330" y1="86" x2="580" y2="86" stroke="#2c6fb1" stroke-width="1.2"/><text x="455" y="78" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3" text-decoration="underline">借閱1 : Loan</text><text x="340" y="106" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">借閱日期：2024-01-01</text><text x="340" y="128" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">還書日期：2024-01-15</text><rect x="620" y="60" width="220" height="96" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><line x1="620" y1="86" x2="840" y2="86" stroke="#2c6fb1" stroke-width="1.2"/><text x="730" y="78" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#e6edf3" text-decoration="underline">書籍1 : Book</text><text x="630" y="106" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">書名：UML基礎</text><text x="630" y="128" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">作者：John Doe</text><text x="630" y="150" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">ISBN: 1234567890</text><line x1="270" y1="96" x2="326" y2="96" stroke="#39d0d8" stroke-width="1.6"/><text x="272" y="88" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">Borrow</text><line x1="580" y1="96" x2="616" y2="96" stroke="#39d0d8" stroke-width="1.6"/><text x="582" y="88" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">Borrow</text></svg><figcaption>圖　物件圖：名稱加底線代表實例；用戶1 經借閱1 連到書籍1，對應類圖 User—Loan—Book 的關聯。</figcaption></figure>

### 10.6 序列圖設計
根據用例圖，繪製系統的序列圖。序列圖展示了對象之間的交互過程及其消息傳遞的順序。
序列圖：

<figure class="fig-svg"><svg viewBox="0 0 860 330" width="100%" role="img" aria-label="UML 序列圖：用戶註冊流程中 User、Library System、Database 的訊息順序" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="25" y="20" width="170" height="40" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="110" y="45" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#e6edf3">User 用戶</text><line x1="110" y1="60" x2="110" y2="290" stroke="#2c6fb1" stroke-width="1.2" stroke-dasharray="4 5"/><rect x="345" y="20" width="170" height="40" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="430" y="45" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#e6edf3">Library System 系統</text><line x1="430" y1="60" x2="430" y2="290" stroke="#2c6fb1" stroke-width="1.2" stroke-dasharray="4 5"/><rect x="665" y="20" width="170" height="40" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="750" y="45" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12" fill="#e6edf3">Database 資料庫</text><line x1="750" y1="60" x2="750" y2="290" stroke="#2c6fb1" stroke-width="1.2" stroke-dasharray="4 5"/><line x1="110" y1="110" x2="430" y2="110" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><text x="270" y="102" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">註冊（register）</text><line x1="430" y1="175" x2="750" y2="175" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><text x="590" y="167" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">存儲用戶信息（storeUser）</text><line x1="430" y1="240" x2="110" y2="240" stroke="#39d0d8" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#a)"/><text x="270" y="232" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#e6edf3">註冊成功通知（registerSuccess）</text></svg><figcaption>圖　序列圖：用戶送出註冊，系統將資料寫入資料庫，最後回覆註冊成功通知。</figcaption></figure>

### 10.7 活動圖設計
根據用例圖，繪製系統的活動圖。活動圖展示了系統中的活動流程和控制流。
活動圖：

<figure class="fig-svg"><svg viewBox="0 0 860 570" width="100%" role="img" aria-label="UML 活動圖：用戶註冊流程，含資料有效性的決策分支" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><circle cx="330" cy="34" r="11" fill="#e6edf3"/><line x1="330" y1="45" x2="330" y2="68" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="230" y="70" width="200" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="330" y="102" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">輸入用戶信息</text><line x1="330" y1="122" x2="330" y2="148" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="230" y="150" width="200" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="330" y="182" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">檢查用戶信息</text><line x1="330" y1="202" x2="330" y2="232" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><polygon points="330,234 412,280 330,326 248,280" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="330" y="285" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">資料有效？</text><line x1="330" y1="326" x2="330" y2="348" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="340" y="342" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">是</text><rect x="230" y="350" width="200" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="330" y="382" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">存儲用戶</text><line x1="330" y1="402" x2="330" y2="428" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="230" y="430" width="200" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="330" y="462" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">註冊成功</text><line x1="330" y1="482" x2="330" y2="508" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="342" y="500" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">結束</text><circle cx="330" cy="522" r="13" fill="none" stroke="#e6edf3" stroke-width="1.8"/><circle cx="330" cy="522" r="7" fill="#e6edf3"/><line x1="412" y1="280" x2="466" y2="280" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="424" y="272" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#39d0d8">否</text><rect x="468" y="254" width="170" height="52" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="553" y="286" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">提示錯誤</text><path d="M553 306 V522 H346" fill="none" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/></svg><figcaption>圖　活動圖：輸入資料後檢查，有效則存儲用戶、顯示註冊成功；無效則提示錯誤，兩條路都走到結束。</figcaption></figure>

### 10.8 狀態圖設計
根據類圖，繪製系統的狀態圖。狀態圖展示了對象在其生命週期中所經歷的各種狀態以及導致狀態變化的事件。
狀態圖：

<figure class="fig-svg"><svg viewBox="0 0 860 640" width="100%" role="img" aria-label="UML 狀態圖：用戶帳戶由未註冊到已註銷的七個狀態與轉換事件" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><circle cx="240" cy="24" r="9" fill="#e6edf3"/><line x1="240" y1="33" x2="240" y2="46" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="130" y="50" width="220" height="56" rx="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="240" y="85" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">未註冊</text><rect x="130" y="130" width="220" height="56" rx="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="240" y="165" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">註冊中</text><line x1="240" y1="106" x2="240" y2="126" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="228" y="120" text-anchor="end" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">提交註冊</text><rect x="130" y="210" width="220" height="56" rx="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="240" y="245" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">已註冊</text><line x1="240" y1="186" x2="240" y2="206" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="228" y="200" text-anchor="end" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">註冊成功</text><rect x="130" y="290" width="220" height="56" rx="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="240" y="325" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">登錄中</text><line x1="240" y1="266" x2="240" y2="286" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="228" y="280" text-anchor="end" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">登錄</text><rect x="130" y="370" width="220" height="56" rx="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="240" y="405" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">已登錄</text><line x1="240" y1="346" x2="240" y2="366" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="228" y="360" text-anchor="end" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">登錄成功</text><rect x="130" y="450" width="220" height="56" rx="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="240" y="485" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">注銷中</text><line x1="240" y1="426" x2="240" y2="446" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="228" y="440" text-anchor="end" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">注銷</text><rect x="130" y="530" width="220" height="56" rx="26" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="240" y="565" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="14" fill="#e6edf3">已注銷</text><line x1="240" y1="506" x2="240" y2="526" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="228" y="520" text-anchor="end" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11" fill="#39d0d8">注銷完成</text></svg><figcaption>圖　狀態圖：未註冊→註冊中→已註冊→登錄中→已登錄→注銷中→已註銷，箭頭上的文字是觸發轉換的事件。</figcaption></figure>

### 10.9 組件圖設計
根據類圖和序列圖，繪製系統的組件圖。組件圖展示了系統中的物理模塊及其相互依賴關係。
組件圖：

<figure class="fig-svg"><svg viewBox="0 0 860 470" width="100%" role="img" aria-label="UML 組件圖：用戶界面、業務邏輯層、資料層三層與依賴方向" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="240" y="20" width="380" height="104" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="430" y="44" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">用戶界面（User Interface）</text><text x="258" y="68" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#e6edf3">• 註冊（register）</text><text x="258" y="88" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#e6edf3">• 登錄（login）</text><text x="258" y="108" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#e6edf3">• 搜索書籍（searchBooks）</text><rect x="240" y="190" width="380" height="104" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="430" y="214" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">業務邏輯層（Business Logic）</text><text x="258" y="238" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#e6edf3">• 處理用戶註冊（handleRegister）</text><text x="258" y="258" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#e6edf3">• 處理用戶登錄（handleLogin）</text><text x="258" y="278" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#e6edf3">• 處理書籍搜索（handleSearchBooks）</text><rect x="240" y="360" width="380" height="84" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="430" y="384" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#39d0d8">資料層（Data Layer）</text><text x="258" y="408" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#e6edf3">• 存儲用戶信息（storeUser）</text><text x="258" y="428" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#e6edf3">• 查詢書籍（queryBooks）</text><line x1="430" y1="124" x2="430" y2="186" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="430" y1="294" x2="430" y2="356" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/></svg><figcaption>圖　組件圖：用戶界面依賴業務邏輯層，業務邏輯層依賴資料層；箭頭由上往下代表呼叫方向。</figcaption></figure>

### 10.10 部署圖設計
根據組件圖，繪製系統的部署圖。部署圖展示了系統的物理部署結構，包括硬件節點、軟件構件及其相互關係。
部署圖：

<figure class="fig-svg"><svg viewBox="0 0 860 490" width="100%" role="img" aria-label="UML 部署圖：客戶端、應用服務器、數據庫服務器三個節點與構件" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><rect x="260" y="20" width="340" height="108" rx="8" fill="none" stroke="#2c6fb1" stroke-width="1.8"/><rect x="260" y="20" width="340" height="28" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="430" y="39" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#39d0d8">客戶端（Client）</text><rect x="276" y="66" width="308" height="34" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.4"/><text x="430" y="88" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#e6edf3">用戶界面構件（User Interface Component）</text><rect x="260" y="190" width="340" height="108" rx="8" fill="none" stroke="#2c6fb1" stroke-width="1.8"/><rect x="260" y="190" width="340" height="28" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="430" y="209" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#39d0d8">應用服務器（Application Server）</text><rect x="276" y="236" width="308" height="34" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.4"/><text x="430" y="258" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#e6edf3">業務邏輯構件（Business Logic Component）</text><rect x="260" y="360" width="340" height="108" rx="8" fill="none" stroke="#2c6fb1" stroke-width="1.8"/><rect x="260" y="360" width="340" height="28" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="430" y="379" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#39d0d8">數據庫服務器（Database Server）</text><rect x="276" y="406" width="308" height="34" rx="6" fill="#132030" stroke="#2c6fb1" stroke-width="1.4"/><text x="430" y="428" text-anchor="middle" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="11.5" fill="#e6edf3">資料層構件（Data Layer Component）</text><line x1="430" y1="128" x2="430" y2="186" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><line x1="430" y1="298" x2="430" y2="356" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/></svg><figcaption>圖　部署圖：用戶界面構件在客戶端，業務邏輯構件在應用服務器，資料層構件在數據庫服務器，箭頭代表呼叫方向。</figcaption></figure>

### 10.11 綜合案例總結
通過以上的綜合案例分析，我們展示瞭如何在一個完整的軟件開發過程中應用各種 UML 圖表。每個圖表都有其特定的用途和優勢，幫助開發團隊從不同的角度理解和設計系統。具體來說：

1. **用例圖**：幫助捕捉和分析系統的功能需求，確定系統的功能範圍和參與者。
2. **類圖**：幫助設計系統的靜態結構，定義系統中的類及其屬性、操作和類之間的關係。
3. **對象圖**：幫助分析系統在特定時刻的狀態，展示對象的實例化關係。
4. **序列圖**：幫助設計和分析對象之間的動態交互，展示消息傳遞的順序。
5. **活動圖**：幫助設計和分析系統中的活動流程和控制流，展示系統的動態行為。
6. **狀態圖**：幫助設計和分析對象的狀態變化，展示對象的生命週期。
7. **組件圖**：幫助設計系統的物理結構，展示系統中的物理模塊及其相互依賴關係。
8. **部署圖**：幫助設計系統的物理部署結構，展示硬件節點、軟件構件及其相互關係。

### 10.12 實踐應用
在實際開發過程中，開發團隊應該根據具體項目的需求，選擇合適的 UML 圖表來進行需求分析、系統設計和部署。以下是一些實踐應用的建議：

1. **項目啟動階段**：在項目啟動階段，開發團隊可以使用用例圖來捕捉和分析系統的功能需求，確定系統的功能範圍和參與者。這有助於確保所有利益相關者對系統的需求有一致的理解。
2. **系統設計階段**：在系統設計階段，開發團隊可以使用類圖、對象圖、序列圖、活動圖和狀態圖來設計和分析系統的靜態結構和動態行為。這有助於確保系統的設計合理、高效且滿足需求。
3. **系統實現階段**：在系統實現階段，開發團隊可以使用組件圖和部署圖來設計系統的物理結構和部署方案，確保系統能夠在預期的運行環境中正常運行。
4. **系統測試階段**：在系統測試階段，開發團隊可以使用各種 UML 圖表來設計測試用例，確保系統的功能、性能和可靠性都能被測試覆蓋。
5. **系統維護階段**：在系統維護階段，開發團隊可以使用 UML 圖表來記錄和分析系統的變更需求，幫助確保系統的維護和升級工作順利進行。

### 10.13 小結
本章通過一個綜合案例，展示瞭如何在一個完整的軟件開發過程中應用各種 UML 圖表。我們通過需求分析、用例圖設計、類圖設計、對象圖設計、序列圖設計、活動圖設計、狀態圖設計、組件圖設計和部署圖設計，全面展示了 UML 圖表的應用。這些圖表幫助開發團隊從不同的角度理解和設計系統，確保系統的功能、性能和可靠性滿足需求。在實際開發過程中，開發團隊應該根據具體項目的需求，靈活運用這些 UML 圖表，從而提高軟件開發的效率和質量。

