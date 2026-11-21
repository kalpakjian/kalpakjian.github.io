---
title: Django 學習筆記總覽
date: 2026-11-21 20:00:00
---

![Django 學習筆記](/img/covers/django-cover.png)

> **課程**：Django 網站框架開發 — 8 份掃描檔、共 **405 頁**
> **做法**：OCR（Unlimited-OCR-2 打底 + Tesseract／PaddleOCR 交叉校對）→ 去頁眉頁腳、接回跨頁斷行 → 程式碼入框 → 人工校對 1,065 條爭議
> **本頁**：按課程結構拆成 **14 章**，每章一頁單檔 HTML，自帶側邊欄目錄、語法高亮與章節封面
> **版本基準**：**Django 5.2 LTS**（2025-04 發布，安全支援至 2028-04；Python 3.10–3.14），安裝指令與 CI 設定已按此更新
> **規模**：**939 段**程式碼、**9,000+ 行**筆記；全站零外部資源，離線可讀

---

## 1 · 計算思維與網頁框架基礎

![第 1 章 計算思維與網頁框架基礎](/img/covers/django-ch01.png)

- **範圍**：p.2–p.15（14 頁）
- **涵蓋**：分解、模式識別、抽象、算法四大特徵；前端與後端開發、Web 託管、瀏覽器與渲染流程；UML 系統分析入門
- **👉 [看筆記](/django-notes/ch01-thinking-web.html)**

---

## 2 · Python 簡介與安裝

![第 2 章 Python 簡介與安裝](/img/covers/django-ch02.png)

- **範圍**：p.16–p.23（8 頁）
- **涵蓋**：Python 的歷史與特性、應用方向與不足、Windows／macOS／Linux 安裝、環境變量配置、VSCode 設定
- **👉 [看筆記](/django-notes/ch02-python-intro.html)**

---

## 3 · Python3 基礎語法

![第 3 章 Python3 基礎語法](/img/covers/django-ch03.png)

- **範圍**：p.24–p.28（5 頁）
- **涵蓋**：編碼、保留字、註釋、縮進、類型判斷、input 與 print、import 與 from…import
- **👉 [看筆記](/django-notes/ch03-syntax.html)**

---

## 4 · 數據類型、運算符與數字

![第 4 章 數據類型、運算符與數字](/img/covers/django-ch04.png)

- **範圍**：p.29–p.47（19 頁）
- **涵蓋**：基本數據類型、算術／賦值／比較／位元／成員／身份運算符、優先級、數字類型與轉換、整數除法與冪運算
- **👉 [看筆記](/django-notes/ch04-datatypes.html)**

---

## 5 · 序列與容器類型

![第 5 章 序列與容器類型](/img/covers/django-ch05.png)

- **範圍**：p.48–p.60（13 頁）
- **涵蓋**：序列索引與切片、列表、元組、字典、集合、常用內置函數與運算
- **👉 [看筆記](/django-notes/ch05-sequence.html)**

---

## 6 · 流程控制、函數、模組與面向對象

![第 6 章 流程控制、函數、模組與面向對象](/img/covers/django-ch06.png)

- **範圍**：p.61–p.94（34 頁）
- **涵蓋**：if／while／for、pass、迭代器與生成器、函數參數與作用域、lambda、模組與包、異常處理、類與繼承、多繼承、主流框架比較
- **👉 [看筆記](/django-notes/ch06-control-oop.html)**

---

## 7 · Django 基礎與環境建置

![第 7 章 Django 基礎與環境建置](/img/covers/django-ch07.png)

- **範圍**：p.95–p.108（14 頁）
- **涵蓋**：MVT 架構、優勢與社羣資源、安裝 Django 5.2 LTS 與虛擬環境、建立第一個專案、專案結構、常見錯誤排查
- **👉 [看筆記](/django-notes/ch07-django-basics.html)**

---

## 8 · Project、App 與 settings 配置

![第 8 章 Project、App 與 settings 配置](/img/covers/django-ch08.png)

- **範圍**：p.109–p.128（20 頁）
- **涵蓋**：Project 與 App 的關係、settings.py 結構與常用配置、manage.py 與自定義命令、URL 配置與路由系統
- **👉 [看筆記](/django-notes/ch08-project-settings.html)**

---

## 9 · URL 路由、視圖與模板

![第 9 章 URL 路由、視圖與模板](/img/covers/django-ch09.png)

- **範圍**：p.129–p.146（18 頁）
- **涵蓋**：path() 與 include()、動態 URL 與路徑轉換器、函數視圖與類視圖、模板語法、上下文、模板繼承與自定義標籤
- **👉 [看筆記](/django-notes/ch09-views-templates.html)**

---

## 10 · 模型、ORM 與查詢集

![第 10 章 模型、ORM 與查詢集](/img/covers/django-ch10.png)

- **範圍**：p.147–p.173（27 頁）
- **涵蓋**：模型定義與遷移、一對多／多對多／一對一關聯、查詢集 API、F()／Q() 查詢、聚合與連表查詢、Humanize 過濾器
- **👉 [看筆記](/django-notes/ch10-models-orm.html)**

---

## 11 · 分頁、美化、認證與專案實作

![第 11 章 分頁、美化、認證與專案實作](/img/covers/django-ch11.png)

- **範圍**：p.174–p.209（36 頁）
- **涵蓋**：查詢過濾技巧、Paginator 分頁、Bootstrap 美化表單與後臺、認證框架（註冊／登入／登出／密碼重設）、messages 框架、活動報名專案實作
- **👉 [看筆記](/django-notes/ch11-auth-project.html)**

---

## 12 · 後端網站開發工作流程（單元三 · 第 1 章）

![第 12 章 後端網站開發工作流程](/img/covers/django-ch12.png)

- **範圍**：p.210–p.351（142 頁）
- **涵蓋**：後端職責與 IDE、版本控制概念、Git 安裝與配置、基本操作、分支與遠程倉庫、stash／submodule、Git Flow、圖形化工具、代碼託管與 PR／MR、Git Hooks、安全（.gitignore／分支保護）、CI/CD（Travis／Jenkins／GitHub Actions）、大型專案與效能
- **👉 [看筆記](/django-notes/ch12-backend-workflow.html)**

---

## 13 · 遠端開發環境（單元三 · 第 2 章）

![第 13 章 遠端開發環境](/img/covers/django-ch13.png)

- **範圍**：p.352–p.370（19 頁）
- **涵蓋**：從本地到雲端的環境轉移、雲端技術與遠端開發優勢、IaaS／PaaS／SaaS、本地架設與雲端比較（AWS／GCP／Azure）、效能與成本、雲原生與 DevOps、伺服器設置流程
- **👉 [看筆記](/django-notes/ch13-remote-dev.html)**

---

## 14 · UML 系統分析與設計（獨立篇章）

![第 14 章 UML 系統分析與設計](/img/covers/django-ch14.png)

- **範圍**：p.371–p.405（35 頁）
- **涵蓋**：UML 概論與歷史、應用範圍；用例圖、類圖、對象圖、序列圖、活動圖、狀態圖、組件圖、部署圖的基本元素與繪製步驟，以及綜合案例
- **👉 [看筆記](/django-notes/ch14-uml.html)**
