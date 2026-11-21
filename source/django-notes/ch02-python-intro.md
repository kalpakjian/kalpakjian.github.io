# 第 2 章 · Python 簡介與安裝

## 1. Python 概述

### 1.1 什麼是 Python

Python（英式 /ˈpaɪθən/、美式 /ˈpaɪθɑːn/）是由荷蘭人 Guido van Rossum 於 1989 年發明、1991 年首次公開發行的**物件導向、解釋型**程式語言。它語法簡潔、可讀性高，兼具解釋性、互動性與腳本語言的特點。

<figure class="fig-svg"><svg viewBox="0 0 720 180" width="100%" role="img" aria-label="Python 執行流程：原始碼 → 位元碼 → Python 虛擬機 → 輸出" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><g font-family="'Microsoft JhengHei','Segoe UI',sans-serif"><rect x="20" y="60" width="150" height="60" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="95" y="86" text-anchor="middle" font-size="13.5" fill="#e6edf3">原始碼 .py</text><text x="95" y="106" text-anchor="middle" font-size="11" fill="#39d0d8">你寫的程式</text><line x1="172" y1="90" x2="210" y2="90" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><text x="191" y="80" text-anchor="middle" font-size="10" fill="#7ee787">編譯</text><rect x="214" y="60" width="160" height="60" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="294" y="86" text-anchor="middle" font-size="13.5" fill="#e6edf3">位元碼 .pyc</text><text x="294" y="106" text-anchor="middle" font-size="11" fill="#39d0d8">bytecode</text><line x1="376" y1="90" x2="414" y2="90" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="418" y="60" width="160" height="60" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="498" y="86" text-anchor="middle" font-size="13.5" fill="#e6edf3">Python 虛擬機</text><text x="498" y="106" text-anchor="middle" font-size="11" fill="#39d0d8">PVM 執行</text><line x1="580" y1="90" x2="618" y2="90" stroke="#39d0d8" stroke-width="1.8" marker-end="url(#a)"/><rect x="622" y="60" width="80" height="60" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="662" y="96" text-anchor="middle" font-size="13.5" fill="#e6edf3">輸出</text></g><text x="360" y="152" text-anchor="middle" font-size="11" fill="#39d0d8">CPython 會自動快取位元碼，加快下次載入；這也是 Python 跨平台的關鍵</text><figcaption>圖：Python 的執行流程。</figcaption></svg></figure>

### 1.2 發展歷史

- 1980 年代末誕生於荷蘭國家數學與計算機科學研究所，吸收 ABC、Modula-3、C/C++、Unix shell 等語言的特點。
- **2000 年**：Python 2.0 發布，加入垃圾回收並支援 Unicode。
- **2008 年**：Python 3.0（Py3k）發布，與 2.x 不完全相容。
- **2.7** 是 Python 2.x 的最後版本；**Python 3.x** 為目前主流。
- 以 PSF 授權開源：可自由使用、修改、再散布（含商業用途），修改後不強制開源。

### 1.3 優點

- **易學、易讀、易維護**：關鍵字少、語法明確。
- **標準庫豐富、跨平台**：在 UNIX、Windows、macOS 皆相容。
- **互動模式**：可在終端直接輸入程式並取得結果，方便測試。
- **可移植、可擴展**：可移植到多種平台；關鍵效能段落可用 C/C++ 撰寫再呼叫。
- **應用面廣**：提供資料庫介面、支援 GUI，也能嵌入 C/C++ 程式中。

### 1.4 缺點

- 屬解釋型語言，執行效率較低。
- 功能廣但不專精；對效能要求高的情境不是首選。

### 1.5 應用方向

- **網站開發**：YouTube、Reddit、Dropbox、豆瓣。
- **3D／向量繪圖**：Blender、Inkscape。
- **機器學習與 AI**：TensorFlow、Keras、PyTorch。
- **資料分析與爬蟲、科學計算與演算法**。
- **IDLE**：Python 內建 IDE，由 Guido 以 Python + Tkinter 開發。

## 2. 安裝與環境設定

### 2.1 安裝 Python 3

官網：https://www.python.org/

- **Windows**：下載 `python-3.14.10-amd64.exe`，雙擊後照預設選項安裝即可。
- **macOS**：系統通常自帶 Python 2.7；可至官網下載最新版。
- **Unix/Linux**：下載原始碼編譯安裝。

```
# tar -zxvf Python-3.14.10.tgz
# cd Python-3.14.10
# ./configure
# make && make install
```

安裝後檢查版本：

```
# python3 -V
Python 3.14.10
```

### 2.2 環境變數 PATH

若要在非安裝目錄執行 Python，需把 Python 目錄加入 `PATH`（Unix/Linux 區分大小寫，Windows 不區分）。

- **bash**：`export PATH="$PATH:/usr/local/bin/python"`
- **csh**：`setenv PATH "$PATH:/usr/local/bin/python"`
- **sh / ksh**：

```
PATH="$PATH:/usr/local/bin/python"
```

- **Windows（cmd）**：

```
path=%path%;C:\Python
```

#### 2.2.1 在 Windows 圖形介面設定

1. 右鍵「本機」→「內容」→「進階系統設定」。
2. 於「系統變數」中雙擊 `Path`。
3. 加入 Python 安裝路徑（多個路徑以 `;` 分隔）。
4. 開啟 cmd，輸入 `python` 驗證。

### 2.3 執行 Python

- 進入互動式解釋器：Unix/Linux 或 Windows/DOS 皆輸入 `python`。
- 離開：輸入 `exit()`。

### 2.4 用 VSCode 開發

VSCode（Visual Studio Code）是微軟的免費跨平台編輯器，輕量、對 Python 學習友善。設定步驟：

1. 安裝 Python 3。
2. 安裝 VS Code。
3. 安裝 **VS Code Python 擴展**（會一併安裝 Pylance 與 Jupyter）。
