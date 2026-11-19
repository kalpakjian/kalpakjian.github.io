---
title: Python數據分析 學習筆記總覽
date: 2026-11-19 10:00:00
---

> **課程**：Python數據分析 — 8 份掃描 PDF、共 **404 頁**
> **做法**：雙引擎 OCR（Tesseract + Unlimited-OCR-2）交叉校對 → 逐段重跑程式碼 → 圖表以 SVG 重製
> **本頁**：按課程 13 章拆成 13 個單檔頁面，每頁自帶目錄、搜尋、頁碼徽章與原掃描圖
> **實跑成績**：抽出 **343 段**程式碼，**293 段**在本機執行成功（50 段仍失敗，原因逐段列在 repo 的 `docs/OCR_unrunnable_fixes.md`），產出 35 張彩色 SVG 圖
> **公式**：OCR 直接吐出的 LaTeX 共 **142 條**（40 display + 102 inline），轉檔時用 `latex2mathml` 換成 MathML — 不需 CDN、不需 JS，文字仍可選取。另附 **20 項自動驗證**：用 numpy／sympy／statsmodels 重算矩陣加減乘、β̂、SE、TSS=ESS+RSS，並用教材資料集 UN11 重跑迴歸係數，全數吻合

## 1 · 行業簡介

![第 1 章 行業簡介](/img/covers/python-da-ch01.png)

- **範圍**：p.2–p.24（23 頁）
- **涵蓋**：未來勞動趨勢、IT 產業的角色與教育、軟體開發生命週期簡介、常見的 SDLC 模型、瀑布模型 Waterfall - 設計、迭代模型 Iterative - 設計
- **👉 [看筆記](/python-da-notes/ch01-industry.html)**

---

## 2 · Python 數據分析開發工具及工作流程

![第 2 章 Python 數據分析開發工具及工作流程](/img/covers/python-da-ch02.png)

- **範圍**：p.25–p.74（50 頁）
- **涵蓋**：Python數據分析開發工具及工作流程、Python 受歡迎程度、Python 系列、本課程中的 Python 和安裝、按兩下已安裝資料夾中的 IDLE、IDE 和編輯器
- **👉 [看筆記](/python-da-notes/ch02-python-tools.html)**

---

## 3 · 基礎統計學原理

![第 3 章 基礎統計學原理](/img/covers/python-da-ch03.png)

- **範圍**：p.75–p.91（17 頁）
- **涵蓋**：我們日常生活中的統計數據、統計數據幫助我們、總體和樣本、採樣、樣本偏差、什麼是樣本偏差？
- **👉 [看筆記](/python-da-notes/ch03-statistics.html)**

---

## 4 · 矩陣代數基礎

![第 4 章 矩陣代數基礎](/img/covers/python-da-ch04.png)

- **範圍**：p.92–p.122（31 頁）
- **涵蓋**：代數 - 簡介、OLS/線性迴歸模型、失業率與實質 GDP（1949-2023）、OLS（Ordinary Least Square）線性迴歸參數估計、OLS 迴歸的基本假設、估計參數的標準誤差
- **👉 [看筆記](/python-da-notes/ch04-linear-algebra.html)**

---

## 5 · 數據分析及可視化基礎

![第 5 章 數據分析及可視化基礎](/img/covers/python-da-ch05.png)

- **範圍**：p.123–p.160（38 頁）
- **涵蓋**：數據庫、資料庫基本概念、SQL 簡介、SQL 是結構化查詢語言的縮寫。、資料庫管理系統（DBMS）、架構 Schema
- **👉 [看筆記](/python-da-notes/ch05-viz-basics.html)**

---

## 6 · Python 數據分析技巧

![第 6 章 Python 數據分析技巧](/img/covers/python-da-ch06.png)

- **範圍**：p.161–p.204（44 頁）
- **涵蓋**：Object-oriented programming 物件化程式設計、更新屬性 & 刪除實例 Update、通過方法更新屬性 Update at、如果超類和子類中都存在相同的方法怎麼辦？、super（）方法、多重繼承 Multiple Inheritance
- **👉 [看筆記](/python-da-notes/ch06-dataskills.html)**

---

## 7 · NumPy 套件

![第 7 章 NumPy 套件](/img/covers/python-da-ch07.png)

- **範圍**：p.205–p.232（28 頁）
- **涵蓋**：Numpy套件、什麼是 NumPy、檢查安裝的版本、創建簡單的一維陣列、Numpy 陣列物件、創建二維陣列
- **👉 [看筆記](/python-da-notes/ch07-numpy.html)**

---

## 8 · Pandas 套件

![第 8 章 Pandas 套件](/img/covers/python-da-ch08.png)

- **範圍**：p.233–p.270（38 頁）
- **涵蓋**：檢查版本、通用術語翻譯、匯入和匯出數據、將.csv 文件導入 Pandas DataFrame、數據幀的過濾和選擇 Filtering & Selection of a DataFrame、添加新列
- **👉 [看筆記](/python-da-notes/ch08-pandas.html)**

---

## 9 · 數據可視化工具介紹與比較

![第 9 章 數據可視化工具介紹與比較](/img/covers/python-da-ch09.png)

- **範圍**：p.271–p.292（22 頁）
- **涵蓋**：簡介及比較數據視覺化工具、視覺化的四個重點、溝通的形式、口頭交流、書面交流、物理通信
- **👉 [看筆記](/python-da-notes/ch09-viz-tools.html)**

---

## 10 · Matplotlib 套件

![第 10 章 Matplotlib 套件](/img/covers/python-da-ch10.png)

- **範圍**：p.293–p.322（30 頁）
- **涵蓋**：安装 Install using PIP、在 Jupyter Notebook、檢查 version、Matplotlib Interfaces 兩大介面、Matplotlib 架構、該圖分為幾個部分
- **👉 [看筆記](/python-da-notes/ch10-matplotlib.html)**

---

## 11 · Seaborn 套件

![第 11 章 Seaborn 套件](/img/covers/python-da-ch11.png)

- **範圍**：p.323–p.358（36 頁）
- **涵蓋**：概論、繪製堆疊直方圖-sns.histplot、Relation Plot 關係圖 - sns.relplot、Discover the code 程式碼探究、風速 Heatmap and Covid-19 Hotspot、估計回歸擬合 Estimate regression fits- sns.regplot
- **👉 [看筆記](/python-da-notes/ch11-seaborn.html)**

---

## 12 · Plotly 套件

![第 12 章 Plotly 套件](/img/covers/python-da-ch12.png)

- **範圍**：p.359–p.396（38 頁）
- **涵蓋**：Plotly套件、Plotly 將數據值分配、自定義地理、散點圖、在一個parallel coordinates、Plotly套件 Part 2
- **👉 [看筆記](/python-da-notes/ch12-plotly.html)**

---

## 13 · 數據分析專案：Storytelling

![第 13 章 數據分析專案：Storytelling](/img/covers/python-da-ch13.png)

- **範圍**：p.397–p.404（8 頁）
- **涵蓋**：數據分析專案 Storytelling for Data Analysis、數據分析專業 Storytelling for Data Analysis
- **👉 [看筆記](/python-da-notes/ch13-storytelling.html)**
