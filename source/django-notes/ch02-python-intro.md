# 第 2 章 · Python 簡介與安裝

## 1. Python 概述

### 1.1 什麼是 Python

Python（英式 /ˈpaɪθən/、美式 /ˈpaɪθɑːn/）是由荷蘭人 Guido van Rossum 於 1989 年發明、1991 年首次公開發行的**物件導向、解釋型**程式語言。它語法簡潔、可讀性高，兼具解釋性、互動性與腳本語言的特點。

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
