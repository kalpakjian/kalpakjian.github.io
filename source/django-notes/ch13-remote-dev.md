# 第 13 章 · 遠端開發環境

## 1. 從本地到雲端

### 1.1 開發環境的轉變

傳統開發要在本地設定整套環境（Web 伺服器、資料庫、語言與框架），雖有完全控制權，卻有「設定繁瑣、環境不一致、難以模擬生產環境」等問題。隨著雲端技術成熟，開發環境逐漸轉向雲端，帶來遠端協作、快速部署與彈性資源。

### 1.2 雲端的優勢

- **資源彈性**：按需調整運算資源，避免浪費。
- **高可用**：故障轉移、多重備份與全球資料中心。
- **協作便利**：團隊可在同一雲端環境開發、測試、部署。

### 1.3 雲端服務三種模式

| 模式 | 提供什麼 | 例子 |
| --- | --- | --- |
| **IaaS**（基礎設施即服務） | 虛擬機、儲存、網路等基礎資源 | AWS、Google Cloud、Azure |
| **PaaS**（平台即服務） | 執行環境（OS、資料庫、中介軟體、工具） | Heroku、Google App Engine、Azure App Services |
| **SaaS**（軟體即服務） | 直接可用的應用程式 | Salesforce、Dropbox、Google Workspace |

## 2. 雲端服務架構詳解

<figure class="fig-svg"><svg viewBox="0 0 720 300" width="100%" role="img" aria-label="雲端服務三模式：IaaS / PaaS / SaaS 的抽象層級與責任劃分" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#f0a04b"/></marker></defs><g font-family="'Microsoft JhengHei','Segoe UI',sans-serif"><line x1="100" y1="256" x2="100" y2="52" stroke="#f0a04b" stroke-width="1.8" marker-end="url(#a)"/><text x="80" y="160" text-anchor="middle" font-size="11.5" fill="#f0a04b" transform="rotate(-90 80 160)">抽象程度越高 →</text><rect x="170" y="40" width="300" height="56" rx="10" fill="#132030" stroke="#39d0d8" stroke-width="1.8"/><text x="320" y="66" text-anchor="middle" font-size="15" fill="#e6edf3">SaaS 軟體即服務</text><text x="320" y="86" text-anchor="middle" font-size="11.5" fill="#39d0d8">直接用現成應用</text><text x="492" y="64" font-size="12" fill="#e6edf3">Salesforce · Dropbox</text><text x="492" y="84" font-size="12" fill="#e6edf3">Google Workspace</text><rect x="170" y="120" width="300" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.8"/><text x="320" y="146" text-anchor="middle" font-size="15" fill="#e6edf3">PaaS 平台即服務</text><text x="320" y="166" text-anchor="middle" font-size="11.5" fill="#39d0d8">用平台開發與部署</text><text x="492" y="144" font-size="12" fill="#e6edf3">Heroku</text><text x="492" y="164" font-size="12" fill="#e6edf3">Google App Engine</text><rect x="170" y="200" width="300" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.8"/><text x="320" y="226" text-anchor="middle" font-size="15" fill="#e6edf3">IaaS 基礎設施即服務</text><text x="320" y="246" text-anchor="middle" font-size="11.5" fill="#39d0d8">用虛擬機／儲存／網路</text><text x="492" y="224" font-size="12" fill="#e6edf3">AWS · GCP · Azure</text><text x="492" y="244" font-size="12" fill="#e6edf3">EC2 · Compute Engine</text></g><figcaption>圖：雲端服務三模式（IaaS / PaaS / SaaS）。</figcaption></svg></figure>

### 2.1 IaaS

提供虛擬化硬體（運算、儲存、網路），開發者自行安裝 OS、資料庫、伺服器。

- **在 Web 開發的角色**：彈性擴縮、完全控制（適合高自訂／高安全需求）。
- **常見服務商**：AWS（EC2／S3／RDS）、Google Cloud（Compute Engine，強於資料分析與 ML）、Azure（Virtual Machines，與 Microsoft 生態整合佳）。

### 2.2 PaaS

比 IaaS 更高層的抽象，提供執行環境，開發者只需專注程式碼。

- **應用場景**：快速原型、多語言框架支援、自動擴縮與維護。
- **如何簡化開發**：自動化部署、內建 CI/CD、自動擴縮。
- **常見服務商**：Heroku、Google App Engine、Azure App Services。

### 2.3 SaaS

最高層：完全託管的應用，透過網路即可使用，無需安裝與管理。

- **優勢**：快速部署、全球可存取、自動更新。
- **對企業開發的幫助**：可透過 API 整合（如 Salesforce），把非核心功能外包。
- **常見服務商**：Salesforce、Dropbox、Google Workspace。

## 3. 設置本地伺服器

### 3.1 概述

傳統做法是多數手動設定 Web 伺服器（Apache、Nginx）、資料庫（MySQL、PostgreSQL）與語言框架。

- **優點**：完全控制、無網路依賴。
- **挑戰**：環境設定複雜、環境不一致、難以模擬生產環境。

### 3.2 架設步驟

1. **選作業系統**：常用 Linux（Ubuntu LTS、Rocky Linux）。
2. **安裝 Web 伺服器**：Apache（彈性）或 Nginx（高效能、低記憶體）。
3. **設定資料庫**：MySQL／PostgreSQL（關聯式）、MongoDB（NoSQL）。
4. **安裝語言與框架**：如 Python（Django／Flask）、Node.js、PHP（Laravel）。
5. **設定開發工具**：IDE（VS Code、IntelliJ）、測試與除錯環境。

## 4. 設置雲端伺服器

### 4.1 步驟與考量

先選服務類型：

- **IaaS**：需高度自訂、完全控制（AWS EC2、Google Compute Engine）。
- **PaaS**：想簡化部署、專注開發。
- **SaaS**：不需自建（如 Google Workspace）。

部署考量：**資源配置**（CPU／RAM／儲存）、**可擴展性**（自動擴縮）、**安全性**（加密、認證、防火牆）。

### 4.2 AWS

1. 建立 EC2 執行個體。
2. 設定安全組（只開放必要連接埠，如 80／443）。
3. 以 SSH 連入，安裝 Web 伺服器、資料庫與應用環境。
4. 設定 Auto Scaling 與 ELB（負載平衡）。

### 4.3 Google Cloud

1. 建立 Compute Engine 虛擬機。
2. 安裝 Web 伺服器與資料庫。
3. 用 Cloud Storage／Firestore 存放靜態資源與資料。

### 4.4 Azure

提供 App Services 與 Virtual Machines，流程類似；依需求選擇虛擬機或 App Services。

## 5. 本地 vs 雲端：對比

| 面向 | 本地 | 雲端 |
| --- | --- | --- |
| **性能與彈性** | 適合小型專案、免網路 | 隨時擴縮、免硬體維護 |
| **安全與隱私** | 資料在本地、易控制 | 提供加密、MFA、DDoS 防禦等 |
| **成本** | 小型專案較省 | 大量資源／長期營運更具性價比 |

## 6. 未來趨勢

- **雲原生**：以微服務 + 容器（Docker／Kubernetes）打造，善用雲端優勢。
- **DevOps 與 CI/CD**：自動化開發、測試、部署，縮短週期、提升品質。
- **邊緣運算與分散式雲**：把運算移到接近資料源處，降低延遲（適合 IoT、5G）。

## 7. 結論

選本地或雲端取決於專案規模、資源需求與團隊能力：大型、多團隊、長期營運適合雲端；小型、個人專案本地即可。持續關注技術趨勢，才能在競爭中保持領先。

**參考資料**：https://www.ibm.com/topics/iaas-paas-saas
## 8. 專案實作：網絡應用設計與開發

以「網絡應用開發專案」為例，說明從市場需求到部署的完整流程。

### 8.1 市場需求分析

- **即時性與高可用**：需 24 小時不間斷、能處理大流量。
- **使用者體驗（UX）**：介面要簡單、直觀、美觀。
- **跨平台相容**：桌機／平板／手機皆能順暢運作（響應式設計）。
- **資料隱私與安全**：需具備強大安全機制。

### 8.2 目標用戶

- **個人用戶**：社交、娛樂、個人理財。
- **企業用戶**：電商、CRM／ERP、協作工具。
- **專業用戶**：金融分析、工程設計、科研工具。

### 8.3 開發流程

1. 需求收集與分析。
2. 介面與 UX 設計（含響應式）。
3. 技術架構設計（框架、資料庫、伺服器）。
4. 前端與後端開發。
5. 測試與優化（功能、效能、安全）。
6. 部署與持續維護。

### 8.4 用 Python 開發

- **優勢**：簡單易學、框架豐富（Django／Flask）、生態完整。
- **Django vs Flask**：Django 功能齊全（後台、認證、ORM），適合大型／企業級；Flask 輕量靈活，適合小型或需特殊結構。
- **前端整合**：Django 模板產生動態頁；Flask 可設計 API 搭配 React／Vue 做單頁應用（SPA）。

### 8.5 後端與資料庫

- **後端考量**：用戶認證與權限（Django 內建／Flask-Login）、API 設計（DRF／Flask-RESTful）。
- **資料庫**：關聯式（MySQL／PostgreSQL）或 NoSQL（MongoDB）。
  - Django ORM：以物件操作資料庫、自動產生 SQL。
  - Flask：用 SQLAlchemy 等第三方庫，彈性高。
- **效能與安全**：加索引、分片／複製、加密儲存。

<figure class="fig-svg"><svg viewBox="0 0 780 210" width="100%" role="img" aria-label="Django 生產部署架構：瀏覽器 → Nginx → Gunicorn/uWSGI → Django → 資料庫" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><g font-family="'Microsoft JhengHei','Segoe UI',sans-serif"><rect x="24" y="60" width="130" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="89" y="86" text-anchor="middle" font-size="14" fill="#e6edf3">瀏覽器</text><text x="89" y="106" text-anchor="middle" font-size="11" fill="#39d0d8">HTTPS</text><line x1="156" y1="88" x2="188" y2="88" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="192" y="60" width="150" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="267" y="84" text-anchor="middle" font-size="14" fill="#e6edf3">Nginx</text><text x="267" y="104" text-anchor="middle" font-size="11" fill="#39d0d8">反向代理／靜態檔</text><line x1="344" y1="88" x2="376" y2="88" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="380" y="60" width="170" height="56" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="465" y="84" text-anchor="middle" font-size="14" fill="#e6edf3">Gunicorn / uWSGI</text><text x="465" y="104" text-anchor="middle" font-size="11" fill="#39d0d8">WSGI 應用伺服器</text><line x1="552" y1="88" x2="584" y2="88" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="588" y="60" width="160" height="56" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="668" y="84" text-anchor="middle" font-size="14" fill="#e6edf3">Django 應用</text><text x="668" y="104" text-anchor="middle" font-size="11" fill="#39d0d8">views / ORM</text><path d="M120 116 L120 150 L660 150 L660 118" fill="none" stroke="#39d0d8" stroke-width="1.5" stroke-dasharray="5 4"/><rect x="40" y="158" width="170" height="30" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.4"/><text x="125" y="178" text-anchor="middle" font-size="12" fill="#e6edf3">PostgreSQL / MySQL</text><text x="410" y="178" font-size="11.5" fill="#39d0d8">↑ 資料存取（ORM 產生 SQL）</text></g><figcaption>圖：Django 的生產部署架構。</figcaption></svg></figure>

### 8.6 伺服器與部署

- **本地或雲端**：依需求選擇；雲端彈性高，適合高流量與全球用戶。
- **設定流程**：選 Linux → 安裝 Nginx／Apache → 用 Gunicorn／uWSGI 跑 Python 應用 → 設定 HTTPS 與防火牆。
- **自動化部署**：用 Jenkins、GitLab CI 等實現 CI/CD。

### 8.7 小結

網絡應用開發涵蓋需求分析、設計、前後端、資料庫與部署；Python（Django／Flask）提供完整工具鏈，可依需求選擇架構，交付高效、可用又安全的應用。

**參考資料**：https://git-scm.com/doc
