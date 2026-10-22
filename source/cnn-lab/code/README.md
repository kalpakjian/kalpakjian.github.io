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
