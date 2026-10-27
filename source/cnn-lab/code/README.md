# CNN 專題 · 程式碼

這七支腳本產生專題裡所有數字與圖片。全部在 Windows + Python 3.14 + PyTorch 2.14（CUDA）上實測。

| 檔案 | 用途 | 出現在 |
|---|---|---|
| `cnn_check.py` | 逐層尺寸追蹤、參數量、padding 缺失與 GAP 對照 | 第 2 章 |
| `train_cnn.py` | 訓練（MNIST / CIFAR-10、small / wide、erase / bg-mix） | 第 3、9、11 章 |
| `inspect_model.py` | 特徵圖、Grad-CAM、遮擋敏感度、錯誤分析、kernel 視覺化 | 第 3–7 章 |
| `occlusion_experiment.py` | 遮擋 ratio 的統計實驗（正確 vs 錯誤） | 第 6 章 |
| `error_taxonomy.py` | decisive / mixed / blind 錯誤分型 | 第 8 章 |
| `confusion_probe.py` | 混淆矩陣與單一捷徑比率（bird→plane） | 第 9、11 章 |
| `background_swap.py` | 反事實測試（改背景 / 遮物件） | 第 10 章 |
| `neon_svg.py` | NEON 版型工具組（`defs` / `frame` / `title` / `pill` / `card` / `legend`） | 全 13 張圖 |
| `build_figs.py` | SVG 產線：結構驗證 → 套版重生 → Chrome 量測 → 聯絡表 | 全 13 張圖 |

## 安裝

```powershell
pip install torch torchvision matplotlib datasets pillow tqdm
```

## 最短重現路徑

```powershell
# 第 2 章
python cnn_check.py

# 第 3–7 章（MNIST）
python train_cnn.py --dataset mnist --epochs 3 --dump-maps --plot
python inspect_model.py --dataset mnist --n 4 --kernels --errors 3 --occlusion

# 第 9–11 章（CIFAR-10，會自動從 HuggingFace 取資料）
python train_cnn.py --dataset cifar10 --arch wide --epochs 15 --batch-size 512 --lr 4e-3 --out run_wide
python confusion_probe.py --ckpt run_wide\cifar10\best.pt --class bird --tag wide
python error_taxonomy.py --classes bird,dog,ship --k 40 --ckpt run_wide\cifar10\best.pt
python background_swap.py --ckpt run_wide\cifar10\best.pt --class bird --n 300 --tag bird
```

> 每個腳本頂部都有 docstring 說明參數；`--help` 也可查。

## 圖檔產線（SVG）

`img/` 的 13 張圖不是用繪圖軟體畫的，是手寫 SVG；`build_figs.py` 負責驗證與重生。

```powershell
python build_figs.py               # 結構驗證 + Chrome 文字量測（退出碼 0 = 全過）
python build_figs.py --preview     # 產生 code/_preview.png，13 張一次目視
python build_figs.py --template    # 用 neon_svg 產生 img/_template.svg（新圖起點）
python build_figs.py --regen       # 只補 role="img" 與 filter 邊界，改前備份到 img/_backup_*
```

新圖從版型工具組開始，色票與 `img/00_cover.svg`～`12_lessons.svg` 完全一致：

```python
import sys; sys.path.insert(0, "code")
from neon_svg import *
svg = (open_svg(900, 320, "圖說：三層卷積")
       + frame(900, 320)
       + title(60, 90, "三層卷積", "空間變小、通道變多", 780)
       + "</svg>\n")
write("img/13_new.svg", svg)
```

驗證分兩層，缺一不可：

| 層 | 工具 | 抓什麼 | 抓不到什麼 |
|---|---|---|---|
| 量測 | `measure_text.py`（Chrome `getBBox`） | 疊字、文字超出卡片、文字超出畫布 | 文字壓在圖形／線上 |
| 目視 | `build_figs.py --preview` 或 `shot_svg.py --scale 2` | 標籤壓節點、線穿過字、圖例被蓋 | 需要人眼，無法自動化 |

> 2026-10-28 首次量測：13 張中 **8 張有既存排版問題**（`04_kernels`、`06_occlusion`、`07_confusion`、`08_swap`、`09_ab_results`、`10_confidence`、`11_taxonomy`、`12_lessons`）——多為標籤疊字、y 軸標籤超出畫布、標題超出卡片；`00`／`01`／`02`／`03`／`05` 結構與排版皆通過。
