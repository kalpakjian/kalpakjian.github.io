# Using Local GPU for Machine Learning 學習筆記（考試溫習版）

> 課程：Certificate in Application of Computer Vision Technology (Part-time)
> 機構：匯縱專業發展中心（IVDC）
> 教材來源：`IVDC_Using Local GPU for ML.pptx` → PDF（26 頁）
> 本筆記按 PDF 原稿每一個標題逐一填充內容，並補上實際指令、版本對照、常見錯誤、模擬試題。
> 原稿為**安裝步驟截圖**（文字極少）；本筆記把每一步補上「要做什麼、用什麼指令、如何驗證」。
> 本機實測環境（Windows）：**RTX 4090 / 驅動 617.42 / CUDA 13.4 / PyTorch 2.14.1+cu132**。
> **附錄 G 另備一份 60 題的 MC 模擬試卷（含答案速查表與逐題詳解）**，適合考前完整計時練習。

---

## 目錄

| # | 章節 | PDF 頁 |
|---|------|--------|
| 1 | [Set up Nvidia Video Driver](#1-set-up-nvidia-video-driver) | 2–3 |
| 2 | [Install Visual Studio C++](#2-install-visual-studio-c) | 4–5 |
| 3 | [Install Anaconda](#3-install-anaconda) | 6–8 |
| 4 | [Anaconda Prompt](#4-anaconda-prompt) | 9 |
| 5 | [Setup Anaconda Path](#5-setup-anaconda-path) | 10 |
| 6 | [Install or check CUDA tool](#6-install-or-check-cuda-tool) | 11 |
| 7 | [Check version for PyTorch](#7-check-version-for-pytorch) | 12 |
| 8 | [CUDA Toolkit](#8-cuda-toolkit) | 13 |
| 9 | [cuDNN](#9-cudnn) | 14 |
| 10 | [Copy cuDNN bin files to CUDA](#10-copy-cudnn-bin-files-to-cuda) | 15 |
| 11 | [Copy cuDNN lib files to CUDA](#11-copy-cudnn-lib-files-to-cuda) | 16 |
| 12 | [Check Environment Variables](#12-check-environment-variables) | 17 |
| 13 | [Install Visual Studio Code](#13-install-visual-studio-code) | 18 |
| 14 | [Install Git](#14-install-git) | 19 |
| 15 | [Install PyTorch](#15-install-pytorch) | 20–21 |
| 16 | [Use Visual Studio Code](#16-use-visual-studio-code) | 22 |
| 17 | [Use Bash Shell (if needed)](#17-use-bash-shell-if-needed) | 23 |
| 18 | [Install Python (if needed)](#18-install-python-if-needed) | 24 |
| 19 | [Check GPU](#19-check-gpu) | 25 |
| 20 | [Set Path (if needed)](#20-set-path-if-needed) | 26 |
| A | [附錄 A：指令速查表](#附錄-a指令速查表) | — |
| B | [附錄 B：常見錯誤與陷阱](#附錄-b常見錯誤與陷阱) | — |
| C | [附錄 C：模擬試題（連答案）](#附錄-c模擬試題連答案) | — |
| D | [附錄 D：教材頁面索引對照](#附錄-d教材頁面索引對照) | — |
| E | [附錄 E：離線安裝提示](#附錄-e離線安裝提示) | — |
| F | [附錄 F：一頁精華（考前 10 分鐘）](#附錄-f一頁精華考前-10-分鐘) | — |
| G | [附錄 G：MC 模擬試卷（60 題）](#附錄-gmc-模擬試卷60-題) | — |
| H | [附錄 H：答錯題目 → 複習章節對照](#附錄-h答錯題目--複習章節對照) | — |

---

## 0. 30 秒總複習（考前最後掃描）

```
在本機用 GPU 跑 ML（Windows）的安裝順序：
  1. Nvidia 顯示驅動  →  2. Visual Studio C++（編譯器）
  3. Anaconda（Python 環境）  →  4. conda 指令 / PATH
  5. CUDA Toolkit（nvcc）  →  6. cuDNN（深度學習加速庫）
  7. 複製 cuDNN bin/lib → CUDA 安裝目錄  →  8. 檢查環境變數
  9. VS Code / Git  →  10. PyTorch（GPU 版）  →  11. 驗證 GPU

驗證三招：nvidia-smi  /  nvcc --version  /  torch.cuda.is_available()
```

| 你會用到的關鍵詞 | 一句話記法 |
|---|---|
| Nvidia Video Driver | 顯卡驅動；`nvidia-smi` 可看版本與 VRAM |
| Visual Studio C++ | CUDA 編譯需要 MSVC（Build Tools 即可） |
| Anaconda | Python 發行版＋`conda` 環境管理 |
| Anaconda Prompt | 已設好 conda 環境的終端 |
| Anaconda Path | 把 `conda` 加進 PATH（否則別處叫不到） |
| CUDA Toolkit | 提供 `nvcc` 與 CUDA 執行期 |
| cuDNN | NVIDIA 深度學習加速庫（要複製 bin/lib 進 CUDA） |
| Environment Variables | `CUDA_PATH`、`PATH` 的檢查 |
| Visual Studio Code | 編輯器（裝 Python 擴充即可跑） |
| Git | 版本控制（裝套件、拉 repo 常用） |
| PyTorch | 深度學習框架；要裝 **GPU 版（cuXXX）** |
| `torch.cuda.is_available()` | 回傳 `True` 才代表 GPU 可用 |

---

## 1. Set up Nvidia Video Driver

**目的**：先裝好顯卡驅動，系統才認得 GPU，之後的 CUDA 才能運作。

### 1.1 步驟

1. 到 NVIDIA 官網下載對應型號的驅動（或用 GeForce Experience）。
2. 安裝後**重開機**。
3. 開啟「命令提示字元」或 PowerShell，輸入 `nvidia-smi` 驗證。

### 1.2 驗證指令

```powershell
nvidia-smi
```

**本機實測輸出（節錄）**：

```text
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 617.42                 KMD Version: 617.42        CUDA UMD Version: 13.4     |
+-----------------------------------------+------------------------+----------------------+
|   0  NVIDIA GeForce RTX 4090      WDDM  |   00000000:01:00.0  On |                  Off |
|  0%   34C    P8             25W /  500W |    1982MiB /  24564MiB |      9%      Default |
+-----------------------------------------+------------------------+----------------------+
```

要看的三個數字：**驅動版本**、**VRAM 總量**、**CUDA UMD Version**（本機為 617.42 / 24564MiB / 13.4）。

> **考點**：`nvidia-smi` 是**驗證驅動＋GPU** 的第一招；它顯示的是**驅動支援的 CUDA 版本上限**，
> 不是實際安裝的 CUDA Toolkit 版本（後者要用 `nvcc --version`）。

---

## 2. Install Visual Studio C++

**目的**：CUDA 在 Windows 上需要 **MSVC 編譯器**；安裝 **Visual Studio Build Tools（含 C++ 工作負載）** 即可。

### 2.1 步驟

1. 下載 Visual Studio（社群版）或 **Build Tools for Visual Studio**。
2. 在安裝精靈中勾選「**使用 C++ 的桌面開發**（Desktop development with C++）」。
3. 確認包含 **MSVC v143 建置工具** 與 **Windows SDK**。
4. 安裝完成後重開機（建議）。

### 2.2 驗證

```powershell
# 確認 MSVC 編譯器存在（路徑依版本而異）
where.exe cl.exe
```

若 `cl.exe` 找不到，改用「x64 Native Tools Command Prompt for VS」開啟終端。

> **考點**：CUDA 需要的是 **C++ 編譯工具（MSVC）**，**不一定要完整 IDE**；
> 勾錯工作負載（例如只勾 .NET）會導致之後編譯 CUDA 失敗。

---

## 3. Install Anaconda

**目的**：Anaconda 提供 **Python 環境管理（conda）** 與科學計算套件，是 ML 最常用的環境。

### 3.1 步驟

1. 到 Anaconda 官網下載 **Windows 64-bit Installer**。
2. 安裝時可選「**Just Me**」；安裝路徑建議**不含中文與空白**。
3. 安裝精靈會問「Add Anaconda to my PATH environment variable」——
   **勾不勾都可**（不勾比較乾淨，之後用 Anaconda Prompt 即可）。
4. 安裝完成後開啟 **Anaconda Prompt** 驗證。

### 3.2 驗證指令

```powershell
conda --version
python --version
```

**本機實測輸出**：

```text
conda 24.9.2
```

（本機 Anaconda 安裝於 `C:\Users\princ\anaconda3`，`conda.exe` 在 `Scripts\` 底下。）

> **考點**：`conda` 同時是**套件管理器**與**環境管理器**；
> `conda create -n myenv python=3.11` 可建立獨立環境，避免污染 base。

---

## 4. Anaconda Prompt

**目的**：**Anaconda Prompt** 是一個已預先設定好 conda 環境變數的終端，
在裡面 `conda` / `python` 一定叫得到（不必手動設 PATH）。

### 4.1 開啟方式

- 開始功能表 → **Anaconda Prompt (anaconda3)**。
- 或在 PowerShell 中呼叫：

```powershell
# 直接執行 conda 的完整路徑（不必設 PATH）
& "$env:USERPROFILE\anaconda3\Scripts\conda.exe" --version
```

### 4.2 常用指令

```powershell
conda env list                 # 列出所有環境
conda activate myenv           # 切換環境
conda deactivate               # 離開環境
```

> **考點**：**Anaconda Prompt 與一般 CMD 的差別**在於環境變數是否已設好；
> 若在一般 CMD 打 `conda` 出現「不是內部或外部命令」，就是 PATH 沒設（見第 5 節）。

---

## 5. Setup Anaconda Path

**目的**：把 Anaconda 加進系統 **PATH**，讓任何終端都能直接使用 `conda` / `python`。

### 5.1 要加入 PATH 的三個資料夾

| 資料夾 | 內容 |
|--------|------|
| `<Anaconda>\` | `python.exe` |
| `<Anaconda>\Scripts\` | `conda.exe`、`pip.exe` |
| `<Anaconda>\Library\bin\` | 原生 DLL（**ML 套件常需要**） |

以本機為例：`C:\Users\princ\anaconda3\`、`C:\Users\princ\anaconda3\Scripts\`、`C:\Users\princ\anaconda3\Library\bin\`。

### 5.2 設定方式（GUI）

1. `Win` 搜尋「**環境變數**」→「編輯系統環境變數」。
2. 選 `Path` → **編輯** → **新增** 上述三個路徑 → 確定。
3. **重開終端**後驗證。

### 5.3 設定方式（PowerShell，當前使用者）

```powershell
$base = "$env:USERPROFILE\anaconda3"
[Environment]::SetEnvironmentVariable(
  "Path",
  [Environment]::GetEnvironmentVariable("Path","User") + ";$base;$base\Scripts;$base\Library\bin",
  "User")
```

> **考點**：改 PATH 後**必須重開終端**才生效；
> `Library\bin` 很容易被漏掉，導致 `import torch` 找不到 DLL。

---

## 6. Install or check CUDA tool

**目的**：確認是否已安裝 CUDA Toolkit，並檢查 `nvcc`（CUDA 編譯器）版本。

### 6.1 檢查指令

```powershell
nvcc --version
```

**本機實測輸出**：

```text
Cuda compilation tools, release 13.4, V13.4.92
Build cuda_13.4.r13.4/compiler.38855100_0
```

### 6.2 若尚未安裝

到 NVIDIA 的 **CUDA Toolkit Archive** 下載對應版本（見第 8 節）。

> **考點**：`nvcc --version` 顯示的是**已安裝的 CUDA Toolkit**；
> 而 `nvidia-smi` 顯示的是**驅動支援的上限**。兩者可能不同（本機：nvcc 13.4 / 驅動 UMD 13.4）。

---

## 7. Check version for PyTorch

**目的**：**先決定要裝哪個 CUDA 版本**，再回頭裝對應的 Toolkit 與 PyTorch GPU 版。

### 7.1 決策流程

```
1. 先到 pytorch.org 看「目前支援哪些 CUDA 版本」（例如 cu121 / cu124 / cu132 …）
2. 選擇一個你的驅動支援的版本（驅動版本要 ≥ 該 CUDA 版本）
3. 安裝對應的 CUDA Toolkit + cuDNN
4. 用官方指令安裝 PyTorch（會自動帶對應的 cuXXX）
```

### 7.2 對照原則

| 元件 | 要一致的東西 |
|------|-------------|
| Nvidia 驅動 | 支援的 CUDA 上限 ≥ 你要裝的 CUDA |
| CUDA Toolkit | 與 PyTorch 的 `cuXXX` 對應 |
| cuDNN | 版本要對應 CUDA Toolkit 的**主版本**（如 13.x） |
| PyTorch | 安裝檔名含 `cuXXX`（本機為 `+cu132`） |

> **考點**：最常見的坑是「**先裝了 PyTorch 才發現 CUDA 版本不合**」。
> 正確順序是 **先確認 PyTorch 支援的 CUDA 版本 → 再裝 Toolkit/cuDNN → 最後裝 PyTorch**。

---

## 8. CUDA Toolkit

**目的**：安裝 CUDA Toolkit，取得 `nvcc`、CUDA runtime 與函式庫。

### 8.1 步驟

1. 到 **CUDA Toolkit Archive**（NVIDIA 官網）選擇版本。
2. 下載 Windows 版 **Installer（exe / network）**。
3. 安裝時可選「**自訂（Custom）**」，至少要裝：
   - **CUDA**（Runtime / Development / Documentation）
   - **Visual Studio Integration**（若要用 VS 編譯）
4. 安裝完成後**重開終端**，執行 `nvcc --version` 驗證。

### 8.2 預設安裝路徑

```text
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.4\
```

其中：
| 資料夾 | 內容 |
|--------|------|
| `bin\` | `nvcc.exe`、CUDA runtime DLL |
| `lib\x64\` | 匯入庫（`.lib`） |
| `include\` | 標頭檔（`cuda.h` 等） |

> **考點**：記住 **CUDA 安裝根目錄**（`...\CUDA\v13.4\`），因為**第 10、11 節要把 cuDNN 的檔案複製進去**；
> 版本號（v13.4）要與你裝的一致。

---

## 9. cuDNN

**目的**：**cuDNN（CUDA Deep Neural Network library）** 是 NVIDIA 的深度學習加速庫，
PyTorch / TensorFlow 底層會用到它。

### 9.1 步驟

1. 到 **NVIDIA cuDNN** 頁面（需登入 NVIDIA 開發者帳號）。
2. 選擇**對應 CUDA 主版本**的 cuDNN（例如 CUDA 13.x → cuDNN for CUDA 13）。
3. 下載 **Windows zip**（不是 installer）。
4. 解壓縮，會得到三個資料夾：

```text
cudnn-windows-x86_64-<版本>_cuda13-archive\
  ├─ bin\      （cudnn64_9.dll 等）
  ├─ include\  （cudnn*.h）
  └─ lib\x64\  （cudnn.lib 等）
```

> **考點**：cuDNN 下載的是 **zip 壓縮檔**，需要**手動複製**到 CUDA 目錄（見第 10、11 節）；
> 版本必須對應 **CUDA 主版本**，否則會出現 `Could not locate cudnn_ops` 之類的錯誤。

---

## 10. Copy cuDNN bin files to CUDA

**目的**：把 cuDNN 的 **bin（DLL）** 複製到 CUDA 的 `bin\`，讓執行期找得到。

### 10.1 複製來源與目的

| 來源（cuDNN 解壓後） | 目的（CUDA 安裝目錄） |
|---------------------|----------------------|
| `...\cudnn...\bin\*` | `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.4\bin\` |

### 10.2 指令（PowerShell，系統管理員）

```powershell
$cudnn = "C:\path\to\cudnn-windows-x86_64-..._cuda13-archive"
$cuda  = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.4"

Copy-Item "$cudnn\bin\*"  "$cuda\bin\"  -Force
```

### 10.3 驗證

```powershell
Test-Path "$cuda\bin\cudnn64_9.dll"
```

> **考點**：**bin 一定要複製**，否則執行時會找不到 `cudnn64_*.dll`；
> 複製時要**系統管理員權限**（因為目的在 `Program Files`）。

---

## 11. Copy cuDNN lib files to CUDA

**目的**：把 cuDNN 的 **lib（`.lib` 匯入庫）** 複製到 CUDA 的 `lib\x64\`，讓**編譯**時能連結。

### 11.1 複製來源與目的

| 來源（cuDNN 解壓後） | 目的（CUDA 安裝目錄） |
|---------------------|----------------------|
| `...\cudnn...\lib\x64\*` | `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.4\lib\x64\` |

### 11.2 指令（PowerShell，系統管理員）

```powershell
$cudnn = "C:\path\to\cudnn-windows-x86_64-..._cuda13-archive"
$cuda  = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.4"

Copy-Item "$cudnn\lib\x64\*" "$cuda\lib\x64\" -Force
```

### 11.3 別忘了 include

```powershell
Copy-Item "$cudnn\include\*" "$cuda\include\" -Force
```

### 11.4 驗證三個資料夾都到位

```powershell
foreach ($f in "bin\cudnn64_9.dll","include\cudnn.h","lib\x64\cudnn.lib") {
  "$f : " + (Test-Path "$cuda\$f")
}
```

> **考點**：cuDNN 要複製的是**三份** —— `bin`（執行期 DLL）、`include`（標頭）、`lib\x64`（連結庫）。
> 只複製 bin 而漏了 lib，會出現 **連結錯誤（LNK2019）**。

---

## 12. Check Environment Variables

**目的**：確認 CUDA 相關環境變數是否正確設定，這是「明明裝了卻用不到」的最常見原因。

### 12.1 應該存在的變數

| 變數 | 值（本機為例） | 用途 |
|------|---------------|------|
| `CUDA_PATH` | `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.4` | CUDA 根目錄 |
| `CUDA_PATH_V13_4` | 同上 | 版本專用（安裝程式自動建立） |
| `Path` | 需含 `%CUDA_PATH%\bin` | 讓 `nvcc` 等指令可用 |

### 12.2 檢查指令

```powershell
# 檢視 CUDA 相關環境變數
Get-ChildItem Env: | Where-Object Name -like "CUDA*" | Format-Table -AutoSize

# 確認 PATH 內有 CUDA\bin
$env:Path -split ';' | Where-Object { $_ -like '*CUDA*' }
```

**本機實測（示意）**：

```text
CUDA_PATH       C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.4
CUDA_PATH_V13_4 C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.4
```

> **考點**：若 `CUDA_PATH` 不存在，代表安裝時沒勾選「加入環境變數」；
> 可手動新增，或重跑 CUDA 安裝程式修復。

---

## 13. Install Visual Studio Code

**目的**：安裝輕量編輯器 **VS Code**，用來寫 Python / 跑筆記本。

### 13.1 步驟

1. 到 code.visualstudio.com 下載 **Windows User Installer**。
2. 安裝時建議勾選「**Add to PATH**」與「Open with Code」。
3. 安裝後開啟，安裝必要擴充：
   - **Python**（Microsoft）
   - **Jupyter**（跑 .ipynb）
   - （可選）**Pylance**、**GitLens**

### 13.2 驗證

```powershell
code --version
```

> **考點**：VS Code 的 CLI（`code`）**只有在安裝時勾選「Add to PATH」才可用**；
> 本機若 `code` 不在 PATH，可直接從開始功能表開啟 VS Code。

---

## 14. Install Git

**目的**：安裝 **Git**，用於版本控制與取得（clone）範例專案。

### 14.1 步驟

1. 到 git-scm.com 下載 **Windows 版**。
2. 安裝選項大多**保持預設**即可（含 Git Bash、Git Credential Manager）。
3. 安裝完成後驗證。

### 14.2 驗證

```powershell
git --version
```

**本機實測輸出**：

```text
git version 2.53.0.windows.2
```

> **考點**：Git 安裝會一併提供 **Git Bash**（見第 17 節），在 Windows 上可用 Unix 指令；
> 若在 PowerShell 出現 `git` 找不到，通常是安裝時沒勾 PATH。

---

## 15. Install PyTorch

**目的**：安裝**支援 GPU 的 PyTorch**（檔名含 `cuXXX`，例如 `+cu132`）。

### 15.1 取得官方安裝指令

到 **pytorch.org** 的「Get Started」，選擇：
- PyTorch Build：**Stable**
- Your OS：**Windows**
- Package：**Conda** 或 **Pip**
- Compute Platform：**CUDA 對應版本**（例如 CUDA 12.1 / 12.4 / 13.2）

網站會產生對應指令，例如：

```powershell
# 範例（實際請以官網產生為準）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu132
```

或使用 conda：

```powershell
conda install pytorch torchvision torchaudio pytorch-cuda=13.2 -c pytorch -c nvidia
```

### 15.2 驗證版本

```powershell
python -c "import torch; print(torch.__version__)"
```

**本機實測輸出**：

```text
2.14.1+cu132
```

`+cu132` 代表這是**用 CUDA 13.2 編譯的 GPU 版**；若是 `+cpu` 就是 CPU 版（裝錯了）。

> **考點**：PyTorch 的 `+cuXXX` 後綴是**判斷 GPU 版的關鍵**；
> 裝到 CPU 版時 `torch.cuda.is_available()` 會回 `False`，重裝對應 `cuXXX` 即可。

---

## 16. Use Visual Studio Code

**目的**：用 VS Code 選對 **Python 解譯器（Interpreter）**，才能用到剛裝好的 GPU 環境。

### 16.1 步驟

1. 開啟 VS Code → **File ▸ Open Folder** 選專案資料夾。
2. `Ctrl+Shift+P` → 輸入 **Python: Select Interpreter**。
3. 選擇 **Anaconda 的 python**（例如 `...\anaconda3\python.exe` 或某個 conda 環境）。
4. 新增終端（`` Ctrl+` ``），確認提示字元顯示的環境正確。

### 16.2 建議的 settings.json

```json
{
  "python.defaultInterpreterPath": "C:\\Users\\<你>\\anaconda3\\python.exe",
  "terminal.integrated.defaultProfile.windows": "Command Prompt"
}
```

> **考點**：**「選錯 Interpreter」是 VS Code 跑不到 GPU 的頭號原因**——
> 右下角顯示的 Python 路徑必須是你裝了 PyTorch 的那個環境。

---

## 17. Use Bash Shell (if needed)

**目的**：若需要 Unix 風格指令，可用 **Git Bash**（安裝 Git 時一併安裝）。

### 17.1 開啟方式

- 開始功能表 → **Git Bash**
- 或在 VS Code 中把預設終端改成 Git Bash：

```json
{
  "terminal.integrated.profiles.windows": {
    "Git Bash": { "path": "C:\\Program Files\\Git\\bin\\bash.exe" }
  },
  "terminal.integrated.defaultProfile.windows": "Git Bash"
}
```

### 17.2 常見用途

```bash
# 在 Git Bash 中（Unix 風格）
which python
python -c "import torch; print(torch.cuda.is_available())"
```

> **考點**：Git Bash 與 PowerShell 的**路徑寫法不同**（`/c/Users/...` vs `C:\Users\...`）；
> 在 Git Bash 執行 conda 前，通常要先 `conda init bash` 或直接呼叫 `conda.exe`。

---

## 18. Install Python (if needed)

**目的**：**只有在不使用 Anaconda 時**才需要另外安裝官方 Python。

### 18.1 兩種選擇

| 方式 | 優點 | 注意 |
|------|------|------|
| **Anaconda**（建議） | 內建 conda 環境管理與科學套件 | 體積較大 |
| **官方 Python**（python.org） | 乾淨、輕量 | 需自行管理虛擬環境（venv） |

### 18.2 若裝官方 Python

1. 到 python.org 下載 Windows installer。
2. **務必勾選「Add python.exe to PATH」**。
3. 驗證：

```powershell
python --version
pip --version
```

### 18.3 建立虛擬環境（venv）

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> **考點**：**不要同時混用 Anaconda 與官方 Python 的 PATH**，否則容易出現
> 「`python` 指向 A、`pip` 裝到 B」的錯亂；擇一為主即可。

---

## 19. Check GPU

**目的**：用 PyTorch 確認 GPU 是否真的可用（**本章是原稿唯一的程式碼**，p25）。

### 19.1 原稿程式碼（實測通過）

```python
import torch
if torch.cuda.is_available():
    # Get the number of available GPUs
    gpu_count = torch.cuda.device_count()
    print(f"Number of GPUs available: {gpu_count}")
    print(f"{torch.cuda.get_device_name()}")
else:
    print("CUDA is not available. PyTorch is using the CPU.")
```

**本機實測輸出**：

```text
Number of GPUs available: 1
NVIDIA GeForce RTX 4090
```

### 19.2 更完整的檢查

```python
import torch
print("torch          :", torch.__version__)
print("cuda available :", torch.cuda.is_available())
print("cuda version   :", torch.version.cuda)
print("device count   :", torch.cuda.device_count())
if torch.cuda.is_available():
    print("device name    :", torch.cuda.get_device_name(0))
    print("capability     :", torch.cuda.get_device_capability(0))
```

**本機實測輸出**：

```text
torch          : 2.14.1+cu132
cuda available : True
cuda version   : 13.2
device count   : 1
device name    : NVIDIA GeForce RTX 4090
```

> **考點**：`torch.cuda.is_available()` 回 `True` 才算**成功**；
> 若回 `False`，依序檢查：PyTorch 是否為 `+cuXXX`、驅動版本、CUDA/cuDNN 是否對應。

---

## 20. Set Path (if needed)

**目的**：若某些指令仍找不到，補設定 **PATH**。

### 20.1 需要進 PATH 的常見項目

| 項目 | 路徑（本機為例） |
|------|-----------------|
| Anaconda | `C:\Users\princ\anaconda3\`、`\Scripts\`、`\Library\bin\` |
| CUDA | `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.4\bin\` |
| Git | `C:\Program Files\Git\cmd\` |

### 20.2 檢查與設定

```powershell
# 檢查目前 PATH
$env:Path -split ';' | Select-String -Pattern 'anaconda|CUDA|Git'

# 暫時加入（只對本終端有效）
$env:Path += ";C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.4\bin"
```

永久設定請用「環境變數」GUI（見第 5 節），設定後**重開終端**。

> **考點**：PATH 是「**找不到指令**」問題的最後一道檢查；
> 順序上通常先修 conda（第 5 節）與 CUDA（第 12 節），最後才動系統 PATH。

---

## 附錄 A：指令速查表

### A.1 驗證類（最常考）

| 指令 | 檢查什麼 | 本機實測 |
|------|---------|---------|
| `nvidia-smi` | 顯卡驅動、VRAM、GPU 使用率 | 617.42 / 24564MiB / RTX 4090 |
| `nvcc --version` | CUDA Toolkit 版本 | release 13.4, V13.4.92 |
| `conda --version` | conda 是否可用 | conda 24.9.2 |
| `python --version` | Python 版本 | — |
| `git --version` | Git 版本 | git 2.53.0.windows.2 |
| `code --version` | VS Code CLI（需在 PATH） | — |

### A.2 環境管理

| 指令 | 用途 |
|------|------|
| `conda env list` | 列出所有環境 |
| `conda create -n myenv python=3.11` | 建立環境 |
| `conda activate myenv` | 切換環境 |
| `conda deactivate` | 離開環境 |
| `conda install <pkg>` | 安裝套件（conda） |
| `pip install <pkg>` | 安裝套件（pip） |

### A.3 GPU 驗證（Python）

| 程式碼 | 意義 |
|--------|------|
| `torch.__version__` | PyTorch 版本（`+cuXXX` = GPU 版） |
| `torch.cuda.is_available()` | **True = GPU 可用** |
| `torch.version.cuda` | PyTorch 編譯用的 CUDA 版本 |
| `torch.cuda.device_count()` | GPU 數量 |
| `torch.cuda.get_device_name(0)` | GPU 名稱 |

### A.4 檔案複製（cuDNN → CUDA）

| 來源 | 目的 |
|------|------|
| `cudnn\bin\*` | `CUDA\vXX.X\bin\` |
| `cudnn\include\*` | `CUDA\vXX.X\include\` |
| `cudnn\lib\x64\*` | `CUDA\vXX.X\lib\x64\` |

---

## 附錄 B：常見錯誤與陷阱

### B.1 十大陷阱總表

| # | 陷阱 | 錯誤做法 | 正確做法 |
|---|------|---------|---------|
| 1 | 安裝順序 | 先裝 PyTorch 再看 CUDA | **先確認 PyTorch 支援的 CUDA → 再裝 Toolkit/cuDNN → 最後裝 PyTorch** |
| 2 | 驅動 vs Toolkit | 把 `nvidia-smi` 的版本當成已裝 CUDA | `nvidia-smi`＝驅動上限；`nvcc --version`＝實際 Toolkit |
| 3 | cuDNN 複製 | 只複製 `bin` | **`bin` + `include` + `lib\x64` 三份都要** |
| 4 | cuDNN 版本 | 隨便抓最新 | 要對應 **CUDA 主版本**（如 cuda13） |
| 5 | conda 找不到 | 在一般 CMD 直接打 `conda` | 用 **Anaconda Prompt**，或先把 conda 加入 PATH |
| 6 | PATH 漏項 | 只加 `anaconda3\` | 還要加 `\Scripts\` 與 `\Library\bin\` |
| 7 | 改 PATH 沒生效 | 沒重開終端 | 改完**重開終端** |
| 8 | VS Code 沒 GPU | 選錯 Python Interpreter | **Select Interpreter** 指到裝了 PyTorch 的環境 |
| 9 | 裝到 CPU 版 | `torch.__version__` 是 `+cpu` | 重裝 `+cuXXX` 版 |
| 10 | 權限不足 | 複製檔案到 `Program Files` 失敗 | 用**系統管理員**身分執行 |

### B.2 錯誤訊息對照

| 訊息 | 原因 | 處理 |
|------|------|------|
| `conda : 不是內部或外部命令` | conda 不在 PATH | 用 Anaconda Prompt 或設 PATH（第 5 節） |
| `'nvcc' 不是內部或外部命令` | CUDA `bin` 不在 PATH | 檢查 `CUDA_PATH` 與 PATH（第 12 節） |
| `Could not locate cudnn_ops_infer64_9.dll` | cuDNN bin 沒複製 | 複製 cuDNN `bin\*` 到 CUDA `bin\` |
| `LNK2019: unresolved external symbol` | cuDNN lib 沒複製 | 複製 `lib\x64\*` 與 `include\*` |
| `torch.cuda.is_available()` 回 `False` | 裝到 CPU 版 / CUDA 不符 | 重裝 `+cuXXX` 版（第 15 節） |
| `OSError: [WinError 126] 找不到指定的模組` | 缺 DLL（常為 `Library\bin`） | 把 `anaconda3\Library\bin` 加進 PATH |
| `CUDA out of memory` | VRAM 不足 | 減 batch size、關閉其他佔用 GPU 的程式 |

---

## 附錄 C：模擬試題（連答案）

### C.1 選擇題（20 題）

1. `nvidia-smi` 主要用來檢查？
   - A. Python 版本
   - B. 顯卡驅動與 GPU 狀態
   - C. Git 版本
   - D. 磁碟空間

2. `nvcc --version` 顯示的是？
   - A. 顯卡驅動版本
   - B. Python 版本
   - C. 已安裝的 CUDA Toolkit 版本
   - D. PyTorch 版本

3. 在 Windows 上編譯 CUDA 需要哪個編譯器？
   - A. MSVC（Visual Studio C++）
   - B. Java
   - C. Go
   - D. PHP

4. Anaconda 的 `conda` 同時是什麼？
   - A. 只有編輯器
   - B. 只有瀏覽器
   - C. 只有防毒軟體
   - D. 套件管理器與環境管理器

5. Anaconda Prompt 的特點是？
   - A. 只能跑 Linux
   - B. 已預先設好 conda 環境變數
   - C. 不能執行 python
   - D. 需要付費

6. 設定 Anaconda PATH 時，除了 `anaconda3\` 還要加哪兩個？
   - A. `bin\`、`lib\`
   - B. `tools\`、`docs\`
   - C. `Scripts\`、`Library\bin\`
   - D. `cache\`、`logs\`

7. cuDNN 是什麼？
   - A. NVIDIA 的深度學習加速庫
   - B. 一種程式語言
   - C. 一種顯卡型號
   - D. 一種檔案格式

8. cuDNN 官方下載的格式通常是？
   - A. `.msi` 安裝檔
   - B. `.deb` 套件
   - C. `.exe` 安裝精靈
   - D. **zip 壓縮檔**（需手動複製）

9. cuDNN 的 `bin` 檔案要複製到哪？
   - A. Python 安裝目錄
   - B. CUDA 安裝目錄的 `bin\`
   - C. Windows 系統資料夾
   - D. 桌面

10. CUDA Toolkit 的預設安裝路徑大致是？
    - A. `C:\Python\CUDA\`
    - B. `C:\Windows\CUDA\`
    - C. `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\vXX.X\`
    - D. `C:\Users\Public\CUDA\`

11. `torch.cuda.is_available()` 回傳 `True` 代表？
    - A. GPU 可用
    - B. 只能使用 CPU
    - C. 沒有安裝 PyTorch
    - D. 驅動未安裝

12. PyTorch 版本顯示 `2.14.1+cu132`，`+cu132` 代表？
    - A. 第 132 版
    - B. 支援 132 張顯卡
    - C. CPU 版本
    - D. 以 CUDA 13.2 編譯的 GPU 版

13. VS Code 中明明裝了 PyTorch 卻用不到 GPU，最常見原因是？
    - A. 螢幕解析度太低
    - B. 選錯 Python Interpreter
    - C. 沒裝瀏覽器
    - D. 鍵盤問題

14. 改了 PATH 之後指令仍找不到，通常是？
    - A. 電腦太慢
    - B. 需要重裝 Windows
    - C. 沒有重開終端
    - D. 需要換滑鼠

15. `CUDA_PATH` 環境變數的用途是？
    - A. 指向 CUDA 安裝根目錄
    - B. 儲存 Python 版本
    - C. 記錄 GPU 溫度
    - D. 存放圖片

16. Git Bash 是隨哪個軟體一起安裝的？
    - A. Anaconda
    - B. CUDA
    - C. VS Code
    - D. Git

17. 正確的安裝順序是？
    - A. PyTorch → CUDA → 驅動
    - B. 驅動 → VS C++ / Anaconda → CUDA / cuDNN → PyTorch
    - C. Anaconda → Git → 驅動
    - D. 順序無所謂

18. 安裝官方 Python 時，務必勾選什麼？
    - A. 安裝到 D 槽
    - B. 安裝所有語言套件
    - C. Add python.exe to PATH
    - D. 建立桌面捷徑

19. 出現 `LNK2019: unresolved external symbol` 通常是因為？
    - A. cuDNN 的 `lib`/`include` 沒複製到 CUDA
    - B. 螢幕太小
    - C. 沒裝 Git
    - D. 網路太慢

20. `OSError: [WinError 126] 找不到指定的模組` 常見原因是？
    - A. 記憶體不足
    - B. 螢幕壞了
    - C. 沒裝瀏覽器
    - D. 缺 DLL（常是 `anaconda3\Library\bin` 不在 PATH）

<details><summary>C.1 答案</summary>

1. **B** 2. **C** 3. **A** 4. **D** 5. **B** 6. **C** 7. **A** 8. **D** 9. **B** 10. **C**
11. **A** 12. **D** 13. **B** 14. **C** 15. **A** 16. **D** 17. **B** 18. **C** 19. **A** 20. **D**

</details>

### C.2 填充題（10 題）

1. 檢查顯卡驅動與 GPU 的指令是 ______。
2. 檢查 CUDA Toolkit 版本的指令是 ______。
3. Anaconda 的環境管理器指令是 ______。
4. 設定 Anaconda PATH 要加入的三個資料夾：`\`、`______`、`______`。
5. cuDNN 下載的是 ______ 檔，需要手動複製到 CUDA 目錄。
6. cuDNN 要複製的三個資料夾是 `bin`、`______`、`______`。
7. CUDA 的環境變數名稱是 ______。
8. PyTorch 版本後綴 `+cu132` 代表以 CUDA ______ 編譯的 ______ 版。
9. 驗證 GPU 是否可用的關鍵函式是 ______。
10. VS Code 要在命令面板執行「Python: ______」來選對環境。

<details><summary>C.2 答案</summary>

1. `nvidia-smi`
2. `nvcc --version`
3. `conda`
4. `Scripts\`；`Library\bin\`
5. zip（壓縮檔）
6. `include`；`lib\x64`
7. `CUDA_PATH`
8. 13.2；GPU
9. `torch.cuda.is_available()`
10. Select Interpreter

</details>

### C.3 簡答題（6 題）

1. 說明 `nvidia-smi` 與 `nvcc --version` 的差別。
2. 為什麼 cuDNN 要複製 `bin`、`include`、`lib\x64` 三份？
3. 說明 `conda` 的兩個角色，並各舉一個指令。
4. 設定 PATH 後為何要重開終端？漏掉 `Library\bin` 會怎樣？
5. `torch.cuda.is_available()` 回 `False` 時，列出你的排查順序。
6. VS Code 要如何確認正在使用正確的 Python 環境？

<details><summary>C.3 參考答案</summary>

1. `nvidia-smi` 顯示**驅動版本與 GPU 狀態**（含驅動支援的 CUDA 上限）；`nvcc --version` 顯示**實際安裝的 CUDA Toolkit 版本**。兩者可能不同。
2. `bin`＝執行期 DLL（否則找不到 `cudnn64_*.dll`）；`include`＝標頭檔（編譯需要）；`lib\x64`＝匯入庫（連結需要，缺了會 LNK2019）。
3. 角色一：**套件管理器**（`conda install numpy`）；角色二：**環境管理器**（`conda create -n myenv python=3.11`）。
4. 因為 PATH 是在程序啟動時讀取；改完**已開的終端不會更新**。漏掉 `Library\bin` 會導致 `import torch` 等出現 **WinError 126 找不到模組**。
5. 依序：① `torch.__version__` 是否為 `+cuXXX`；② 驅動是否夠新（`nvidia-smi`）；③ `CUDA_PATH` / PATH 是否正確；④ cuDNN 是否複製齊全；⑤ 是否有多個 Python 環境混淆。
6. `Ctrl+Shift+P` → **Python: Select Interpreter**，選擇裝有 PyTorch 的環境；右下角狀態列與終端提示字元會顯示目前解譯器路徑。

</details>

---

## 附錄 D：教材頁面索引對照

| PDF 頁 | 標題 | 本筆記對應章節 |
|--------|------|---------------|
| 1 | 封面：Using Local GPU for Machine Learning | — |
| 2 | Set up Nvidia Video Driver | 第 1 節 |
| 3 | Set up Nvidia Video Driver | 第 1 節 |
| 4 | Install Visual Studio C++ | 第 2 節 |
| 5 | Install Visual Studio C++ | 第 2 節 |
| 6 | Install Anaconda | 第 3 節 |
| 7 | Install Anaconda | 第 3 節 |
| 8 | Install Anaconda | 第 3 節 |
| 9 | Anaconda Prompt | 第 4 節 |
| 10 | Setup Anaconda Path | 第 5 節 |
| 11 | Install or check CUDA tool | 第 6 節 |
| 12 | Check version for Pytorch | 第 7 節 |
| 13 | CUDA Toolkit | 第 8 節 |
| 14 | cuDNN | 第 9 節 |
| 15 | Copy cuDNN bin files to CUDA | 第 10 節 |
| 16 | Copy cuDNN lib files to CUDA | 第 11 節 |
| 17 | Check Environment Variables | 第 12 節 |
| 18 | Install Visual Studio Code | 第 13 節 |
| 19 | Install Git | 第 14 節 |
| 20 | Install Pytorch | 第 15 節 |
| 21 | Install Pytorch | 第 15 節 |
| 22 | Use Visual Studio Code | 第 16 節 |
| 23 | Use Bash Shell (if needed) | 第 17 節 |
| 24 | Install Python (if needed) | 第 18 節 |
| 25 | Check GPU（含 PyTorch 程式碼） | 第 19 節 |
| 26 | Set Path (if needed) | 第 20 節 |

> 說明：原稿幾乎每頁都是**安裝精靈截圖**，只有 **p25** 含實際程式碼（PyTorch GPU 檢查）；
> 本筆記把每一步補上「目的、指令、驗證方式」，讓沒有截圖也能照著做。

---

## 附錄 E：離線安裝提示

### E.1 需要先下載的安裝檔（有網路時先備好）

| 項目 | 來源 | 檔名關鍵字 |
|------|------|-----------|
| Nvidia 驅動 | nvidia.com / GeForce Experience | `*-desktop-win10-win11-*.exe` |
| Visual Studio Build Tools | visualstudio.microsoft.com | `vs_BuildTools.exe` |
| Anaconda | anaconda.com | `Anaconda3-*-Windows-x86_64.exe` |
| CUDA Toolkit | NVIDIA CUDA Archive | `cuda_*_windows.exe` |
| cuDNN | NVIDIA Developer（需登入） | `cudnn-windows-x86_64-*_cuda13-archive.zip` |
| VS Code | code.visualstudio.com | `VSCodeUserSetup-x64-*.exe` |
| Git | git-scm.com | `Git-*-64-bit.exe` |

### E.2 離線安裝注意

- **cuDNN 需登入 NVIDIA 帳號**才能下載，建議**事先**下載好 zip。
- PyTorch 的 wheel 很大（數 GB），建議先用 `pip download` 或 `conda` 的離線包：
  ```powershell
  pip download torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu132 -d .\wheels
  # 離線安裝
  pip install --no-index --find-links .\wheels torch torchvision torchaudio
  ```
- **順序不能省**：驅動 → 編譯器/Anaconda → CUDA/cuDNN → PyTorch。

### E.3 沒有 GPU 時的替代

- 裝 **CPU 版 PyTorch** 仍可學習與跑小模型（`torch.cuda.is_available()` 會是 `False`）。
- 雲端替代：Colab、Kaggle、或雲端 GPU 服務（不必在本機裝 CUDA）。

---

## 附錄 F：一頁精華（考前 10 分鐘）

```text
【安裝順序（必背）】
  1 Nvidia 驅動 → 2 VS C++ (MSVC) → 3 Anaconda → 4 Anaconda Prompt
  5 Anaconda PATH → 6/7 確認 CUDA 版本 → 8 CUDA Toolkit → 9 cuDNN
  10/11 複製 cuDNN bin + lib(+include) → 12 檢查環境變數
  13 VS Code → 14 Git → 15 PyTorch(GPU 版) → 16-18 使用/選 Interpreter
  19 驗證 GPU → 20 補 PATH

【三大驗證指令】
  nvidia-smi            → 驅動 / VRAM / GPU 狀態
  nvcc --version        → 已裝的 CUDA Toolkit 版本
  conda --version       → conda 是否可用

【PyTorch GPU 檢查（p25 原稿程式碼）】
  import torch
  if torch.cuda.is_available():
      print(torch.cuda.device_count()); print(torch.cuda.get_device_name())
  else:
      print("CUDA is not available. PyTorch is using the CPU.")
  → 本機實測：1 / NVIDIA GeForce RTX 4090

【版本對照（本機實測）】
  驅動 617.42 ｜ nvcc CUDA 13.4 ｜ torch 2.14.1+cu132 ｜ conda 24.9.2 ｜ git 2.53.0

【三大關鍵觀念】
  (1) nvidia-smi ≠ nvcc：前者是驅動上限，後者是實際 Toolkit
  (2) cuDNN 要複製「bin + include + lib\x64」三份到 CUDA 目錄
  (3) +cuXXX 才是 GPU 版；is_available() 回 True 才算成功

【最常見三個坑】
  conda 找不到 → 用 Anaconda Prompt 或設 PATH(含 Scripts 與 Library\bin)
  改了 PATH 沒用 → 要重開終端
  VS Code 沒 GPU → Python: Select Interpreter 選對環境
```

---

## 附錄 G：MC 模擬試卷（60 題）

### G.1 作答說明與應試技巧

- **60 題單選**、滿分 60 分、建議 **75 分鐘**。
- 分三部分：**安裝前置與環境（1–20）**、**CUDA 與 cuDNN（21–40）**、**工具、PyTorch 與排錯（41–60）**。
- 答案分佈刻意打散（A/B/C/D 各 15 題），避免整排猜同一個字母。
- 建議先做完整份再看答案；答錯的題目請用「逐題詳解」對應回章節重讀。

### G.2 第一部分：安裝前置與環境（第 1–20 題）

1. `nvidia-smi` 主要用來檢查？
   - A. Python 版本
   - B. 顯卡驅動與 GPU 狀態
   - C. Git 版本
   - D. 磁碟空間

2. 安裝 Nvidia 顯示驅動後，通常建議？
   - A. 立刻重裝系統
   - B. 關閉防火牆
   - C. 重開機
   - D. 刪除驅動

3. 在 Windows 上編譯 CUDA 需要哪個編譯器？
   - A. MSVC（Visual Studio C++）
   - B. Java
   - C. Go
   - D. PHP

4. 安裝 Visual Studio 時要勾選哪個工作負載？
   - A. .NET 桌面開發
   - B. 遊戲開發（Unity）
   - C. 行動裝置開發
   - D. 使用 C++ 的桌面開發

5. Anaconda 主要提供什麼？
   - A. 只有瀏覽器
   - B. conda 環境與套件管理
   - C. 顯卡驅動
   - D. 防毒軟體

6. Anaconda 的安裝路徑建議？
   - A. 越深越好
   - B. 放在桌面
   - C. 不含中文與空白
   - D. 一定要在 D 槽

7. Anaconda Prompt 的特點是？
   - A. 已預先設好 conda 環境變數
   - B. 只能跑 Linux
   - C. 不能執行 python
   - D. 需要付費

8. 設定 Anaconda PATH 時要加入哪三個資料夾？
   - A. `bin\`、`lib\`、`docs\`
   - B. `tools\`、`cache\`、`logs\`
   - C. `include\`、`src\`、`test\`
   - D. 根目錄、`Scripts\`、`Library\bin\`

9. Anaconda 的 `Library\bin` 主要放什麼？
   - A. 圖片
   - B. 文件
   - C. 原生 DLL
   - D. 範例程式

10. 修改 PATH 之後，要如何才能生效？
    - A. 立刻生效
    - B. 重開終端
    - C. 重裝系統
    - D. 不用管

11. `conda --version` 用來驗證？
    - A. GPU 型號
    - B. CUDA 版本
    - C. Python 套件數量
    - D. conda 是否可用

12. `conda create -n myenv python=3.11` 的作用是？
    - A. 建立名為 myenv 的環境
    - B. 刪除環境
    - C. 安裝顯卡驅動
    - D. 更新 Windows

13. `conda activate myenv` 的作用是？
    - A. 刪除環境
    - B. 建立環境
    - C. 切換到 myenv 環境
    - D. 匯出環境

14. 在一般 CMD 打 `conda` 出現「不是內部或外部命令」，代表？
    - A. 沒裝 Anaconda
    - B. conda 不在 PATH
    - C. 電腦中毒
    - D. 需要重開機

15. `nvidia-smi` 顯示的「CUDA Version」代表？
    - A. 驅動支援的 CUDA 上限
    - B. 已安裝的 CUDA Toolkit
    - C. PyTorch 的 CUDA 版本
    - D. cuDNN 版本

16. `where.exe cl.exe` 用來檢查？
    - A. Git 是否安裝
    - B. Python 版本
    - C. CUDA 版本
    - D. MSVC 編譯器是否存在

17. 安裝 Anaconda 時，一般建議選擇？
    - A. 所有使用者
    - B. Just Me（僅本人）
    - C. 不要安裝
    - D. 只裝 Python

18. 安裝路徑含中文可能導致？
    - A. 硬碟損壞
    - B. 顯卡過熱
    - C. 部分套件或指令出錯
    - D. 網路變慢

19. 檢視 CUDA 相關環境變數的指令是？
    - A. `Get-ChildItem Env: | Where-Object Name -like "CUDA*"`
    - B. `dir cuda`
    - C. `ping cuda`
    - D. `tasklist`

20. `CUDA_PATH` 環境變數的用途是？
    - A. 儲存 Python 版本
    - B. 記錄 GPU 溫度
    - C. 存放圖片
    - D. 指向 CUDA 安裝根目錄

---

### G.3 第二部分：CUDA 與 cuDNN（第 21–40 題）

21. `nvcc --version` 顯示的是？
    - A. 已安裝的 CUDA Toolkit 版本
    - B. 顯卡驅動版本
    - C. Python 版本
    - D. Git 版本

22. CUDA Toolkit 的預設安裝路徑大致是？
    - A. `C:\Python\CUDA\`
    - B. `C:\Windows\CUDA\`
    - C. `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\vXX.X\`
    - D. `C:\Users\Public\CUDA\`

23. 安裝 CUDA Toolkit 時，至少要安裝哪些元件？
    - A. 只要 Documentation
    - B. CUDA（Runtime / Development）
    - C. 只要 Samples
    - D. 只要驅動

24. cuDNN 是什麼？
    - A. 一種程式語言
    - B. 一種顯卡型號
    - C. 一種檔案格式
    - D. NVIDIA 的深度學習加速庫

25. cuDNN 官方下載的格式通常是？
    - A. zip 壓縮檔
    - B. `.msi` 安裝檔
    - C. `.deb` 套件
    - D. `.exe` 安裝精靈

26. cuDNN 版本必須對應什麼？
    - A. Python 版本
    - B. 螢幕解析度
    - C. CUDA 主版本（如 cuda13）
    - D. 硬碟容量

27. cuDNN 解壓後通常包含哪三個資料夾？
    - A. `src`、`test`、`doc`
    - B. `bin`、`include`、`lib\x64`
    - C. `app`、`data`、`cache`
    - D. `x86`、`arm`、`wasm`

28. cuDNN 的 `bin` 檔案要複製到哪？
    - A. Python 安裝目錄
    - B. Windows 系統資料夾
    - C. 桌面
    - D. CUDA 安裝目錄的 `bin\`

29. cuDNN 的 `lib\x64` 檔案要複製到哪？
    - A. CUDA 安裝目錄的 `lib\x64\`
    - B. CUDA 安裝目錄的 `bin\`
    - C. Python 的 `site-packages`
    - D. 使用者文件夾

30. cuDNN 的 `include` 檔案要複製到哪？
    - A. `C:\Windows\System32`
    - B. 專案根目錄
    - C. CUDA 安裝目錄的 `include\`
    - D. Anaconda 的 `Scripts`

31. 只複製 cuDNN 的 `bin` 而漏了 `lib`，可能出現？
    - A. 螢幕變黑
    - B. 連結錯誤（LNK2019）
    - C. 網路斷線
    - D. 鍵盤失效

32. 執行時出現 `Could not locate cudnn_ops_infer64_9.dll` 代表？
    - A. Python 版本太新
    - B. Git 沒安裝
    - C. 螢幕解析度不對
    - D. cuDNN 的 `bin` 沒複製到 CUDA

33. 複製檔案到 `C:\Program Files\...` 需要什麼權限？
    - A. 系統管理員
    - B. 一般使用者
    - C. 訪客
    - D. 不需要權限

34. CUDA 安裝目錄的 `bin\` 主要放什麼？
    - A. 圖片
    - B. 文件
    - C. `nvcc.exe` 與 runtime DLL
    - D. 範例專案

35. 版本一致性的原則是？
    - A. 全部用最新版就好
    - B. 驅動支援的 CUDA 上限 ≥ 要安裝的 CUDA 版本
    - C. 版本隨便配
    - D. 只要 Python 對就好

36. 正確的安裝順序是？
    - A. PyTorch → CUDA → 驅動
    - B. Anaconda → Git → 驅動
    - C. 順序無所謂
    - D. 驅動 → 編譯器 / Anaconda → CUDA / cuDNN → PyTorch

37. 「先裝 PyTorch 才發現 CUDA 版本不合」的後果是？
    - A. 需要重裝對應 `cuXXX` 版本的 PyTorch
    - B. 電腦會壞掉
    - C. 無法開機
    - D. 資料全部遺失

38. `CUDA_PATH_V13_4` 這種變數是？
    - A. 使用者自訂
    - B. PyTorch 建立的
    - C. CUDA 安裝程式自動建立的版本專用變數
    - D. 隨機產生

39. 下載 cuDNN 通常需要什麼？
    - A. 付費訂閱
    - B. 登入 NVIDIA 開發者帳號
    - C. 學校信箱
    - D. 不需要任何帳號

40. CUDA Toolkit Archive 的用途是？
    - A. 查詢 GPU 溫度
    - B. 下載 Python
    - C. 查詢螢幕規格
    - D. 下載舊版／指定版本的 CUDA Toolkit

---

### G.4 第三部分：工具、PyTorch 與排錯（第 41–60 題）

41. VS Code 的命令列指令是？
    - A. `vscode`
    - B. `code`
    - C. `editor`
    - D. `vs`

42. 用 VS Code 寫 ML，建議安裝哪些擴充？
    - A. 只要主題
    - B. 只要圖示
    - C. 只要拼字檢查
    - D. Python 與 Jupyter

43. 安裝 Git 時會一併提供什麼？
    - A. Git Bash
    - B. CUDA
    - C. Anaconda
    - D. PyTorch

44. `git --version` 的用途是？
    - A. 更新 Git
    - B. 刪除 Git
    - C. 驗證 Git 是否安裝成功
    - D. 安裝 Git

45. PyTorch GPU 版安裝檔的後綴是？
    - A. `+gpu`
    - B. `+cuXXX`
    - C. `+cpu`
    - D. `+cuda`

46. 如何判斷 PyTorch 是 GPU 版？
    - A. 看檔名有沒有 gpu
    - B. 看安裝時間
    - C. 看檔案大小
    - D. `torch.__version__` 是否含 `+cuXXX`

47. `torch.cuda.is_available()` 回傳 `True` 代表？
    - A. GPU 可用
    - B. 只能使用 CPU
    - C. 沒有安裝 PyTorch
    - D. 驅動未安裝

48. `torch.cuda.device_count()` 回傳什麼？
    - A. VRAM 大小
    - B. CUDA 版本
    - C. GPU 數量
    - D. GPU 溫度

49. `torch.version.cuda` 代表什麼？
    - A. 顯卡驅動版本
    - B. PyTorch 編譯所用的 CUDA 版本
    - C. cuDNN 版本
    - D. Python 版本

50. `torch.cuda.is_available()` 回 `False`，最常見原因是？
    - A. 螢幕壞了
    - B. 沒裝 Git
    - C. 沒裝瀏覽器
    - D. 裝到 CPU 版或 CUDA 版本不符

51. VS Code 明明裝了 PyTorch 卻用不到 GPU，最常見原因是？
    - A. 選錯 Python Interpreter
    - B. 鍵盤問題
    - C. 螢幕太小
    - D. 沒開音效

52. VS Code 要選 Python 環境，命令是？
    - A. `Python: Run`
    - B. `Python: Debug`
    - C. `Python: Select Interpreter`
    - D. `Python: Format`

53. `OSError: [WinError 126] 找不到指定的模組` 常見原因是？
    - A. 記憶體不足
    - B. 缺 DLL（如 `anaconda3\Library\bin` 不在 PATH）
    - C. 螢幕壞了
    - D. 網路斷線

54. 遇到 `CUDA out of memory`，可以怎麼做？
    - A. 重裝 Windows
    - B. 換螢幕
    - C. 刪除驅動
    - D. 減小 batch size、關閉其他佔用 GPU 的程式

55. 安裝官方 Python 時務必勾選？
    - A. Add python.exe to PATH
    - B. 建立桌面捷徑
    - C. 安裝到 D 槽
    - D. 安裝所有語言

56. 建立虛擬環境（venv）的指令是？
    - A. `python venv new`
    - B. `conda make venv`
    - C. `python -m venv .venv`
    - D. `venv create`

57. 同時混用 Anaconda 與官方 Python 的風險是？
    - A. 顯卡過熱
    - B. `python` 與 `pip` 可能指向不同環境
    - C. 無法上網
    - D. 硬碟壞掉

58. 離線安裝 PyTorch 的作法之一是？
    - A. 直接複製別人電腦的檔案
    - B. 關掉網路安裝
    - C. 用 Windows 商店
    - D. `pip download` 後用 `pip install --no-index --find-links`

59. 沒有 GPU 時的替代方案是？
    - A. 用 CPU 版 PyTorch 或改用雲端 GPU（Colab/Kaggle）
    - B. 放棄學習
    - C. 只能買新電腦
    - D. 無法執行任何 Python

60. 本筆記實測的 PyTorch 版本是？
    - A. `1.0.0`
    - B. `2.0.0+cpu`
    - C. `2.14.1+cu132`
    - D. `3.0.0`

---

### G.5 答案速查表

| 題 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 答 | B | C | A | D | B | C | A | D | C | B |

| 題 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|
| 答 | D | A | C | B | A | D | B | C | A | D |

| 題 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|
| 答 | A | C | B | D | A | C | B | D | A | C |

| 題 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|
| 答 | B | D | A | C | B | D | A | C | B | D |

| 題 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|
| 答 | B | D | A | C | B | D | A | C | B | D |

| 題 | 51 | 52 | 53 | 54 | 55 | 56 | 57 | 58 | 59 | 60 |
|---|---|---|---|---|---|---|---|---|---|---|
| 答 | A | C | B | D | A | C | B | D | A | C |

**分數換算**：每題 1 分，滿分 60 分。答錯題目請對照下方詳解回到章節重讀。

### G.6 逐題詳解

**1. B** —— `nvidia-smi` 檢查驅動與 GPU 狀態（§1）。
**2. C** —— 裝完驅動建議重開機（§1.1）。
**3. A** —— CUDA 在 Windows 需要 MSVC（§2）。
**4. D** —— 勾「使用 C++ 的桌面開發」（§2.1）。
**5. B** —— Anaconda 提供 conda 環境與套件管理（§3）。
**6. C** —— 路徑不含中文與空白（§3.1）。
**7. A** —— Anaconda Prompt 已設好 conda 環境變數（§4）。
**8. D** —— 根目錄、`Scripts\`、`Library\bin\`（§5.1）。
**9. C** —— `Library\bin` 放原生 DLL（§5.1）。
**10. B** —— 改 PATH 後要重開終端（§5.2）。
**11. D** —— `conda --version` 驗證 conda 是否可用（§3.2）。
**12. A** —— 建立名為 myenv 的環境（§3.2）。
**13. C** —— `conda activate` 切換環境（§4.2）。
**14. B** —— conda 不在 PATH（§4.2）。
**15. A** —— `nvidia-smi` 的 CUDA Version＝驅動支援上限（§1.2）。
**16. D** —— 檢查 MSVC 編譯器（§2.2）。
**17. B** —— 建議 Just Me（§3.1）。
**18. C** —— 含中文可能導致套件／指令出錯（§3.1）。
**19. A** —— 用 `Get-ChildItem Env:` 過濾 CUDA*（§12.2）。
**20. D** —— `CUDA_PATH` 指向 CUDA 根目錄（§12.1）。
**21. A** —— `nvcc --version`＝已裝的 CUDA Toolkit（§6.1）。
**22. C** —— `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\vXX.X\`（§8.2）。
**23. B** —— 至少裝 CUDA Runtime / Development（§8.1）。
**24. D** —— cuDNN 是深度學習加速庫（§9）。
**25. A** —— cuDNN 下載 zip（§9.1）。
**26. C** —— 要對應 CUDA 主版本（§9.1）。
**27. B** —— `bin`、`include`、`lib\x64`（§9.1）。
**28. D** —— 複製到 CUDA `bin\`（§10.1）。
**29. A** —— 複製到 CUDA `lib\x64\`（§11.1）。
**30. C** —— 複製到 CUDA `include\`（§11.3）。

**31. B** —— 漏了 lib 會出現 LNK2019 連結錯誤（§11.4／附錄 B.2）。
**32. D** —— 找不到 cudnn DLL＝bin 沒複製（§10.3／附錄 B.2）。
**33. A** —— 需要系統管理員權限（§10.2）。
**34. C** —— CUDA `bin\` 放 `nvcc.exe` 與 runtime DLL（§8.2）。
**35. B** —— 驅動支援上限 ≥ 要裝的 CUDA（§7.2）。
**36. D** —— 驅動 → 編譯器/Anaconda → CUDA/cuDNN → PyTorch（附錄 F）。
**37. A** —— 需重裝對應 `cuXXX` 的 PyTorch（§7.2）。
**38. C** —— CUDA 安裝程式建立的版本專用變數（§12.1）。
**39. B** —— 需登入 NVIDIA 開發者帳號（§9.1／附錄 E.2）。
**40. D** —— Archive 用來下載舊版／指定版本 CUDA（§8.1）。
**41. B** —— VS Code 的 CLI 是 `code`（§13.2）。
**42. D** —— 建議裝 Python 與 Jupyter 擴充（§13.1）。
**43. A** —— Git 安裝一併提供 Git Bash（§14.2／§17）。
**44. C** —— `git --version` 驗證安裝成功（§14.2）。
**45. B** —— GPU 版後綴是 `+cuXXX`（§15.2）。
**46. D** —— 看 `torch.__version__` 是否含 `+cuXXX`（§15.2）。
**47. A** —— 回 `True`＝GPU 可用（§19.2）。
**48. C** —— `device_count()` 回傳 GPU 數量（§19.2）。
**49. B** —— `torch.version.cuda`＝PyTorch 編譯用的 CUDA 版本（§19.2）。
**50. D** —— 裝到 CPU 版或版本不符（附錄 B.2）。
**51. A** —— 選錯 Python Interpreter（§16.1）。
**52. C** —— `Python: Select Interpreter`（§16.1）。
**53. B** —— 缺 DLL（`Library\bin` 不在 PATH）（附錄 B.2）。
**54. D** —— 減 batch size、關閉佔用 GPU 的程式（附錄 B.2）。
**55. A** —— 勾 Add python.exe to PATH（§18.2）。
**56. C** —— `python -m venv .venv`（§18.3）。
**57. B** —— `python` 與 `pip` 可能指向不同環境（§18.3）。
**58. D** —— `pip download` + `--no-index --find-links`（附錄 E.2）。
**59. A** —— CPU 版 PyTorch 或雲端 GPU（附錄 E.3）。
**60. C** —— 本機實測為 `2.14.1+cu132`（§15.2／附錄 F）。

---

## 附錄 H：答錯題目 → 複習章節對照

| 答錯題號 | 建議複習章節 |
|---|---|
| 1–2 | §1 Nvidia 驅動與 `nvidia-smi` |
| 3–4 | §2 Visual Studio C++（MSVC） |
| 5–6 | §3 Anaconda 安裝 |
| 7 | §4 Anaconda Prompt |
| 8–10 | §5 Anaconda PATH 設定 |
| 11–14 | §3.2 / §4.2 conda 指令 |
| 15–16 | §1.2 / §2.2 驗證指令 |
| 17–18 | §3.1 安裝選項與路徑 |
| 19–20 | §12 環境變數檢查 |
| 21–23 | §6 / §8 CUDA Toolkit |
| 24–30 | §9–§11 cuDNN 與複製 |
| 31–33 | §10–§11 複製與權限、附錄 B.2 |
| 34–38 | §8.2 / §7.2 版本一致性 |
| 39–40 | §9.1 / §8.1 下載來源 |
| 41–44 | §13 / §14 VS Code 與 Git |
| 45–50 | §15 / §19 PyTorch 與 GPU 驗證 |
| 51–54 | §16 Interpreter、附錄 B.2 排錯 |
| 55–59 | §18 Python / venv、附錄 E 離線 |
| 60 | §15.2 版本驗證 |

---

*本篇為個人學習筆記整理，教材內容版權屬匯縱專業發展中心（IVDC）所有。*
