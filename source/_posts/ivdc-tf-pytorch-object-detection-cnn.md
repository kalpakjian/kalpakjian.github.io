---
archive: true   # 已歸入 /cnn/ 專題目錄，不列在首頁
title: 同一份課堂材料，用 TensorFlow 與 PyTorch 各跑一遍：物件偵測與 CNN 實作筆記
date: 2026-11-03 21:00:00
categories:
  - 學習筆記
  - 電腦視覺
  - 深度學習
tags:
  - IVDC
  - TensorFlow
  - PyTorch
  - 物件偵測
  - Object Detection
  - CNN
  - 卷積神經網路
  - MNIST
  - YOLOv8
  - Faster R-CNN
  - SSD MobileNet
  - OpenCV
  - 即時偵測
  - 模型比較
  - CPU 推論
toc: true
index_img: /img/covers/ivdc-tf-pytorch-detection-cnn.png
banner_img: /img/covers/ivdc-tf-pytorch-detection-cnn.png
---

> 📚 這篇文章已歸入主題目錄：[CNN 專題](/cnn/)（九篇圖解系列、課程筆記與實驗都在那裡）。

![同一份課堂材料，用 TensorFlow 與 PyTorch 各跑一遍](/img/covers/ivdc-tf-pytorch-detection-cnn.png)

> <strong>這篇是什麼</strong>：IVDC「電腦視覺技術應用」課程裡一份 25 頁的簡報，
> 主題是「用 TensorFlow 與 PyTorch 做物件偵測與 CNN」。簡報本身**只有標題是文字層**，
> 所有程式碼都是截圖，所以我逐頁讀圖把程式碼還原成可執行的檔案，
> 然後**在真機上實測每一段**，把速度、準確度、以及踩到的坑全部記下來。
>
> <strong>為什麼值得寫</strong>：這份材料最有價值的地方不是任何單一 API，
> 而是同一個網路結構用兩套框架各寫一遍，讓你看見<strong>框架只是語法，架構才是本體</strong>。
> 文中附上逐層對照表。另外，實測過程發現四個會讓程式當場掛掉的問題，
> 這些是簡報不會告訴你的。
>
> <strong>📚 課程筆記版</strong>：完整筆記（含目錄、名詞速查、常見陷阱、一頁精華與 40 題測驗）
> → <a href="/ivdc-det-notes/">Lesson 8 物件偵測與 CNN 學習筆記</a>


## 一、這份材料在教什麼

簡報的結構其實很對稱，分成前後兩大塊，每塊都用兩個框架各講一次：

| 區塊 | 簡報內容 | 產出的腳本 |
|---|---|---|
| 物件偵測（TensorFlow） | SSD MobileNet V2，先單張圖再即時 webcam | `01`、`02` |
| 物件偵測（PyTorch） | Faster R-CNN 單張圖、即時 webcam | `03`、`04` |
| 物件偵測（推薦方案） | YOLOv8 四行搞定 | `05` |
| CNN 分類（TensorFlow） | MNIST 數字分類，五個階段 | `06` |
| CNN 分類（PyTorch） | MNIST 數字分類，同樣五個階段 | `07` |

兩個 CNN 區塊的流程完全一樣，都是<strong>載入資料 → 建模型 → 訓練 → 看輸出 → 單張推論</strong>。
這種安排是刻意的：先讓你看懂一個，再看另一個版本，差異就只剩下 API 名稱。

順帶一提，簡報對模型選擇有明確建議，這些建議在實測中被驗證是對的：

- **SSD MobileNet V2**：快，適合即時應用，初學者最容易上手
- **EfficientDet**：準確度更好，速度尚可
- **Faster R-CNN**：準確度高但慢
- **YOLOv8**：速度與準確度平衡最好，標註「Recommended」
- **DETR**：Transformer 架構，準確度好但吃資源

### 25 頁對照表（拿到 PDF 就能跟著看）

我把簡報逐頁核過一遍，這張表是拿掉猜測後的結果。「↓」代表那一頁的程式碼截圖被向下捲動箭頭蓋住：

| 頁 | 標題 | 內容 | 狀態 |
|---|---|---|---|
| 1 | Certificate in Application… | 封面 | 文字層只有這頁與各頁大標題 |
| 2 | Tensorflow for Object Detection | SSD MobileNet V2 單張圖 | **↓ 第 16 行以下看不到** |
| 3 | Real Time Webcam Detection | TF webcam 迴圈 | **↓ 第 16 行以下看不到** |
| 4 | Real Time Object Detection | 五個模型建議（含 EfficientDet） | 純文字 |
| 5 | Pytorch for Object Detection | Faster R-CNN 單張圖 | **↓ 第 12 行以下看不到** |
| 6 | Real Time Webcam Detection | torch webcam | **↓ 第 13 行以下看不到** |
| 7 | Yolo (Recommended) | 四行程式 + 模型比較 | 只有 4 行 |
| 8 | Tensorflow for CNN | 匯入 + 印版本 | — |
| 9 | Tensorflow for CNN | 與第 8 頁完全相同 | **重複頁** |
| 10–12 | Load Data | `mnist.load_data()` → 形狀 → `reshape` + `/255.0` | — |
| 13 | CNN | Keras Sequential 模型 | — |
| 14 | CNN Model Output | `compile` + `fit(epochs=5, validation_split=0.1)` | — |
| 15 | CNN Model Output | 示範輸出 `0.95 / 0.15` → `0.99 / 0.03` | 標題寫 Example output |
| 16–17 | Classification Result | `predict` + `argmax`、輸出 7/7 | — |
| 18 | Or you could use Pytorch | 匯入 + 印版本 | **↓** |
| 19 | Load Data | `torchvision.datasets.MNIST` | **↓ 第 16 行以下看不到** |
| 20 | Load Data | 預期輸出 60000／10000／`(1, 28, 28)` | — |
| 21 | CNN | `nn.Module` 版 CNN | 底部兩行被裁掉 |
| 22 | CNN Model Output | `DataLoader` + `CrossEntropyLoss` + `Adam(lr=0.001)` | **↓ 第 16 行以下看不到** |
| 23 | CNN Model Output | 示範輸出 `0.1805` → `0.0225` | 標題寫 Example output |
| 24–25 | Classification Result | torch 版推論、輸出 7/7 | 第 25 頁與第 17 頁同 |

兩個順帶的觀察：

- **被箭頭遮住的是 7 頁，不是 3 頁**（第 2、3、5、6、18、19、22 頁）。我第一版寫「三處」是低估，
  當時只有 PDF 的截圖可看，沒有逐頁比對行號。
- 第 15／23 頁的輸出是<strong>投影片自己的示範值</strong>——第 23 頁旁邊還寫著
  「Take a screenshot showing: Training command / Epochs / Loss values」。
  所以「跟簡報數字接近」不能當正確性證據，它本來就不是量測結果。

## 二、先把環境量清楚

在寫任何程式之前，我先確認機器上有什麼。這個動作後來證明非常關鍵，
因為它直接揭露了第一個致命問題。

| 套件 | 版本 | 狀態 |
|---|---|---|
| Python | 3.15.1 | — |
| torch | 2.14.1+cpu | 已裝 |
| torchvision | 0.29.1+cpu | 已裝 |
| numpy | 2.5.4 | 已裝 |
| opencv | 5.0.0 | 已裝，但<strong>沒有 GUI</strong> |
| matplotlib / pillow | 3.11.2 / 13.0.0 | 已裝 |
| tensorflow | — | <strong>未裝</strong> |
| ultralytics | — | <strong>未裝</strong> |

我寫了一支自檢腳本，之後每次換機器都先跑它：

```python
"""相機 + 顯示環境自檢 (Pre-exam environment check)."""
import importlib
import sys

PACKAGES = [
    ("cv2", "opencv-python"),
    ("torch", "torch"),
    ("torchvision", "torchvision"),
    ("tensorflow", "tensorflow"),
    ("ultralytics", "ultralytics"),
]
for module, package in PACKAGES:
    try:
        mod = importlib.import_module(module)
        print(f"  OK      {module:16s} {getattr(mod, '__version__', '?')}")
    except Exception as exc:
        print(f"  MISSING {module:16s} -> pip install {package}")

# 關鍵：imshow 要用「真的呼叫一次」來測，不能只檢查函式存在
import cv2
import numpy as np
try:
    print("  UI 框架:", cv2.currentUIFramework() or "(空 = 無)")
    cv2.imshow("__probe__", np.zeros((20, 20, 3), np.uint8))
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    print("  OK  可以正常彈窗")
except Exception as exc:
    print(f"  失敗: {exc}")
```

### 自檢時踩到的第一個坑：`hasattr(cv2, "imshow")` 會騙你

我一開始以為檢查函式存不存在就夠了，結果發現那是錯的：

```
>>> hasattr(cv2, "imshow")
True
>>> cv2.imshow("t", np.zeros((10, 10, 3), np.uint8))
cv2.error: (-2:Unspecified error) The function is not implemented.
Rebuild the library with Windows, GTK+ 2.x or Cocoa support.
```

這是因為裝的是 `opencv-python-headless`——<strong>函式在、但後端沒有實作</strong>。
`currentUIFramework()` 回傳空字串就是徵兆。

修法是換成帶 GUI 的版本：

```powershell
pip uninstall opencv-python-headless -y
pip install opencv-python
```

換完之後自檢顯示 `UI 框架: WIN32`，`imshow` 正常。

## 三、物件偵測：TensorFlow 版

簡報第 2 頁給的是單張圖片的流程。那頁的截圖被向下捲動箭頭蓋住，**第 16 行以下看不到**，
所以尾巴幾行是我用 TF-Hub 標準介面補的。原文照抄、補的標出來：

```python
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load pre-trained object detection model
model = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")

# Load image
image = cv2.imread("image.jpg")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Prepare image
input_tensor = tf.convert_to_tensor(image_rgb, dtype=tf.uint8)  # 原文可見的最後一行（第 15 行）
input_tensor = tf.expand_dims(input_tensor, 0)                  # 第 16 行，被箭頭遮住

# [補完] 以下簡報上完全看不到，依 TF-Hub 標準介面補
detections = model(input_tensor)
boxes = detections["detection_boxes"][0].numpy()
scores = detections["detection_scores"][0].numpy()
classes = detections["detection_classes"][0].numpy().astype(int)
```

<small>原文的註解是英文（`# Load pre-trained object detection model`／`# Load image`／`# Prepare image`），
照抄不改；`numpy` 與 `matplotlib` 兩行也在原文第 4–5 行，後面被遮住的程式碼用不到，腳本裡仍保留，
方便你對行號。</small>

即時 webcam 版本（簡報第 3 頁）的骨架是這樣，下面同樣是補完後的完整迴圈：

```python
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    input_tensor = tf.convert_to_tensor(rgb, dtype=tf.uint8)
    input_tensor = tf.expand_dims(input_tensor, 0)

    detections = model(input_tensor)

    # 補完：門檻過濾 + 畫框
    for box, score, cls in zip(
        detections["detection_boxes"][0].numpy(),
        detections["detection_scores"][0].numpy(),
        detections["detection_classes"][0].numpy().astype(int),
    ):
        if score < 0.5:
            continue
        ymin, xmin, ymax, xmax = box
        h, w = frame.shape[:2]
        cv2.rectangle(frame, (int(xmin * w), int(ymin * h)),
                      (int(xmax * w), int(ymax * h)), (0, 0, 255), 2)

    cv2.imshow("Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

注意 `detection_boxes` 的座標是<strong>歸一化的 0～1</strong>（順序是 `ymin, xmin, ymax, xmax`），
要乘回畫面寬高才能畫。這一點很容易寫錯。

## 四、物件偵測：PyTorch 版

同一件事換一套框架，差異一目了然。簡報第 5 頁（單張圖）與第 6 頁（webcam）用的模型都是
`fasterrcnn_resnet50_fpn(weights="DEFAULT")`：

```python
import torch
import torchvision
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Load pre-trained Faster R-CNN model
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")
model.eval()

# [補完] 第 12 行以下被箭頭遮住，依 torchvision 標準介面補完
image = Image.open("image.jpg").convert("RGB")
transform = transforms.ToTensor()
tensor = transform(image).unsqueeze(0)      # (1, 3, H, W)

with torch.no_grad():
    prediction = model(tensor)[0]

boxes = prediction["boxes"].numpy()      # 絕對像素座標，不是歸一化
scores = prediction["scores"].numpy()
labels = prediction["labels"].numpy()
```

跟 TensorFlow 版比，有兩個關鍵差異值得記住：

1. **`model.eval()` 一定要呼叫**。Faster R-CNN 在 train 模式下會回傳 loss 而不是預測框。
2. **PyTorch 回傳的是絕對像素座標** `[x0, y0, x1, y1]`，TensorFlow 給的是歸一化的比例。
   從一個框架換到另一個，這個地方最容易出錯。

另外 `prediction` 的鍵是 `boxes`／`scores`／`labels`，跟 TensorFlow 的
`detection_boxes`／`detection_scores`／`detection_classes` 一一對應但名字不同。

### 即時 webcam 版

```python
import cv2
import torchvision
from PIL import Image
from torchvision import transforms

model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")
model.eval()
transform = transforms.ToTensor()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    tensor = transform(Image.fromarray(rgb)).unsqueeze(0)

    with torch.no_grad():
        prediction = model(tensor)[0]

    for box, score, label in zip(
        prediction["boxes"].numpy(),
        prediction["scores"].numpy(),
        prediction["labels"].numpy(),
    ):
        if score < 0.5:
            break      # 已依分數降序排列，可以直接 break
        x0, y0, x1, y1 = [int(v) for v in box]
        cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)

    cv2.imshow("PyTorch Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
```

這裡有個小技巧：torchvision 的偵測結果**已經依信心分數由高到低排序**，
所以門檻判斷可以用 `break` 而不是 `continue`，省下後續迭代。

## 五、YOLOv8：四行方案

簡報第 7 頁標題就叫「Yolo (Recommended)」，內文只有四行：

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.predict(source=0, show=True)
```

就這四行，webcam 即時偵測就跑起來了。這是三個方案裡最簡潔的，
也難怪簡報推薦它。`source=0` 是 webcam，換成圖片路徑就是單張偵測。

實際使用時我會加上幾個參數，比較實用：

```python
results = model.predict(
    source=0,
    show=True,
    conf=0.25,
    imgsz=640,      # 推論解析度，影響速度與小目標偵測能力
    stream=True,    # webcam 要開，否則會一次吃完所有幀
)
```

## 六、實測：速度與準確度的取捨

這是全篇最容易誤讀的一段，因為<strong>比較必須同一段畫面</strong>。
上一版我把 torchvision 的 FPS（webcam 實況）和 YOLO 的準確度（官方 `bus.jpg`）並排，
再相除得出「差 34 倍」——算術沒錯，但那是跨基準線的相除。
這次全部重測：<strong>同一台機器、同一張 1280×720 的實機影格、同一個 0.5 門檻、CPU 單張推論</strong>。
畫面就是那台洗衣機（正好是下面要講的陷阱本身）：

| 模型（torchvision／ultralytics 函式名） | 延遲 | 速度 | 最高信心 | ≥0.5 檢出 | 猜成什麼 |
|---|---|---|---|---|---|
| `fasterrcnn_resnet50_fpn`（簡報原版） | 731 ms | **1.4 FPS** | 0.584 | 1 | `toilet` |
| `fasterrcnn_resnet50_fpn` ＋ `min_size=400` | 266 ms | 3.8 FPS | 0.494 | 0 | — |
| `fasterrcnn_mobilenet_v3_large_fpn` | 137 ms | 7.3 FPS | **0.697** | 2 | `toilet`、`refrigerator` |
| `fasterrcnn_mobilenet_v3_large_320_fpn` | 29 ms | 34.6 FPS | 0.464 | <strong>0</strong> | — |
| `ssdlite320_mobilenet_v3_large` | 30 ms | 33.1 FPS | 0.561 | 1 | `refrigerator` |
| `yolov8n` imgsz=640 | 28 ms | 35.8 FPS | 0.404 | <strong>0</strong> | `refrigerator` |
| `yolov8n` imgsz=960 | 36 ms | 27.5 FPS | 0.253 | <strong>0</strong> | `refrigerator` |
| `yolov8n` imgsz=1280 | 33 ms | 30.0 FPS | 0.394 | <strong>0</strong> | `toilet` |

三個反直覺的結果：

1. **最快的兩個模型一個東西都沒偵測到**：`..._320_fpn`（34.6 FPS）與 `yolov8n`（三種解析度都是 0）。
   它把輸入縮到 320×320、或整張圖縮到 640，小目標全部糊掉，信心最高只到 0.40–0.46。
2. **這一幕沒有任何模型答對**——<strong>洗衣機不在 COCO 的 80 個類別裡</strong>，模型只能硬猜。
   Faster R-CNN 猜 `toilet`，YOLO 猜 `refrigerator` 或 `toilet`。
   （上一版寫「硬猜成 `toilet` 或 `truck`」，實測是 `toilet` 或 `refrigerator`，`truck` 沒出現。）
3. **「快」跟「有用」是兩件事**：34.6 FPS 的模型不是「看得很準」，是「很快地什麼都沒看到」。

<strong>同一基準下的差距是 25.6 倍</strong>（1.4 → 35.8 FPS），不是 34 倍——上一版把兩個不同場景相除了。
<strong>`min_size` 也真的有用</strong>：731 → 266 ms（2.7 倍），而這一幕本來就沒有真陽性可掉
（最高信心 0.584 → 0.494），所以是純賺。

換成「有答案」的官方測試圖 `bus.jpg`，YOLOv8n 就恢復正常（同一台機器）：

| `imgsz` | 延遲 | 速度 | ≥0.5 檢出 | 內容 |
|---|---|---|---|---|
| 640 | 27.6 ms | 36.2 FPS | 4 | `bus 0.873` ＋ `person 0.866 / 0.853 / 0.825` |
| 960 | 29.6 ms | 33.8 FPS | 4 | 同樣四個，`person 0.886` 最高 |
| 1280 | 41.8 ms | 23.9 FPS | 6 | 多出 `bus 0.690 / 0.634 / 0.542` <strong>三個重複框</strong> |

所以「解析度拉高、檢出更多」要打折看：1280 多出來的是<strong>同一台公車被框三次</strong>，
外加一個信心 0.289 的 `skateboard`。解析度不是免費的午餐，NMS 也救不回重疊框。

<small>上一版（Windows／另一台機器）量到 `fasterrcnn_resnet50_fpn` 1.1 FPS、`yolov8n` 640 是 37.4 FPS，
和這裡的 1.4／36.2 同一個量級——差別只在「有沒有用同一段畫面比」。上面的表全部是
2026-11 在 Linux（torch 2.15.0+cpu / torchvision 0.29.2+cpu / ultralytics 8.4.201 / OpenCV 5.0.0）
配一支 1280×720 的 USB 攝影機量的。這些是<strong>單次量測</strong>，同一台機器重跑會有 ±10% 跳動
（`ssdlite320` 我在 26–33 ms 之間看過）；但「哪個模型 0 檢出、猜成哪一類」每次跑都一樣。
要重跑這張表：

```bash
python bench/bench_detection.py --camera 0 --yolo     # 在 ivdc_handout repo 裡
```</small>

## 七、CNN 分類：TensorFlow 版

簡報第 8～17 頁，用 MNIST 手寫數字做分類。五個階段很清楚。

### 載入資料

```python
from tensorflow.keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

print("Training Data Shape:", x_train.shape)   # (60000, 28, 28)
print("Test Data Shape:", x_test.shape)        # (10000, 28, 28)
```

### 前處理

```python
x_train = x_train.reshape(-1, 28, 28, 1) / 255.0
x_test = x_test.reshape(-1, 28, 28, 1) / 255.0
```

`reshape` 多出來的那一維是<strong>通道數</strong>。`Conv2D` 要求輸入是 `(H, W, C)`，
灰階圖的 C 就是 1。除以 255 是正規化到 0～1。

### 建立模型

```python
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dense(10, activation="softmax"),
])
```

### 編譯與訓練

```python
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

history = model.fit(
    x_train, y_train,
    epochs=5,
    validation_split=0.1,
)
```

簡報給的預期輸出是準確率從 0.95 爬到 0.99，損失從 0.15 降到 0.03（第 15 頁，標題就是「Example output」，是示範值不是量測值）。

我實際跑了一次（TF 2.21.0 / Keras 3.15.1 / Python 3.11 / CPU，5 epochs、batch 32）：

```
Epoch 1/5 - accuracy: 0.9574 - loss: 0.1398 - val_accuracy: 0.9787 - val_loss: 0.0756
Epoch 2/5 - accuracy: 0.9859 - loss: 0.0461 - val_accuracy: 0.9872 - val_loss: 0.0440
Epoch 3/5 - accuracy: 0.9901 - loss: 0.0312 - val_accuracy: 0.9877 - val_loss: 0.0473
Epoch 4/5 - accuracy: 0.9926 - loss: 0.0228 - val_accuracy: 0.9888 - val_loss: 0.0422
Epoch 5/5 - accuracy: 0.9946 - loss: 0.0164 - val_accuracy: 0.9873 - val_loss: 0.0476
Test loss: 0.0404
Test accuracy: 0.9872
```

跟簡報預期同一個量級（loss 0.140 → 0.016，test 0.9872）。

<strong>為什麼之前驗不了</strong>：這台機器的 Python 3.15 沒有 TensorFlow 的 wheel，
而我當時沒想到用臨時環境繞過去。正確做法：

```bash
uv run --no-project --python 3.11 --with tensorflow-cpu -- python 06_tf_cnn_mnist.py
```

### 單張推論

```python
import numpy as np
import matplotlib.pyplot as plt

index = 0
plt.imshow(x_test[index].reshape(28, 28), cmap="gray")
plt.show()

prediction = model.predict(x_test[index:index + 1])
print("Predicted Class:", np.argmax(prediction))
print("Actual Class:", y_test[index])
```

`np.argmax` 取出 10 個機率裡最大的那個索引，那就是預測的數字。

## 八、CNN 分類：PyTorch 版

同樣五個階段，換 PyTorch 寫。這段我實際跑完了完整訓練。

### 載入資料

```python
import torchvision
import torchvision.transforms as transforms

transform = transforms.ToTensor()

train_dataset = torchvision.datasets.MNIST(
    root="./data", train=True, download=True, transform=transform)
test_dataset = torchvision.datasets.MNIST(
    root="./data", train=False, download=True, transform=transform)

print("Training samples:", len(train_dataset))   # 60000
print("Test samples:", len(test_dataset))        # 10000
print("Image shape:", train_dataset[0][0].shape) # torch.Size([1, 28, 28])
```

注意這裡的形狀是 `(1, 28, 28)`——通道在最前面，跟 TensorFlow 的
`(28, 28, 1)` 剛好相反。這是兩套框架最根本的差異之一。

### 建立模型

```python
import torch
import torch.nn as nn

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3)
        self.fc1 = nn.Linear(64 * 5 * 5, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 64 * 5 * 5)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x
```

<strong>`64 * 5 * 5` 這個數字怎麼來的</strong>：28 進 3×3 卷積（無 padding）→ 26，
池化 → 13，再卷積 → 11，再池化 → 5。所以特徵圖是 `64 × 5 × 5`。
這個計算是初學者最常卡住的地方。

注意 PyTorch 版<strong>最後一層沒有 softmax</strong>。因為 `CrossEntropyLoss` 內部已經含 softmax，
再加一次會變成算了兩次。

### 訓練

```python
import torch.optim as optim

train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=64, shuffle=True)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(5):
    running_loss = 0.0
    for images, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch {epoch + 1}/5, Loss: {running_loss / len(train_loader):.4f}")
```

### 評估

簡報沒貼這段，但它的輸出裡有 `Test accuracy`，中間缺的就是這幾行：

```python
model.eval()
correct = 0
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=512)
with torch.no_grad():
    for images, labels in test_loader:
        correct += (torch.argmax(model(images), dim=1) == labels).sum().item()
print(f"Test accuracy: {correct / len(test_dataset):.4f} ({correct}/{len(test_dataset)})")
```

### 實測結果

這是本機實際跑出來的完整輸出：

```
PyTorch Version: 2.14.1+cpu
Training samples: 60000
Test samples: 10000
Image shape: torch.Size([1, 28, 28])
CNN(
  (conv1): Conv2d(1, 32, kernel_size=(3, 3), stride=(1, 1))
  (pool): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
  (conv2): Conv2d(32, 64, kernel_size=(3, 3), stride=(1, 1))
  (fc1): Linear(in_features=1600, out_features=128, bias=True)
  (fc2): Linear(in_features=128, out_features=10, bias=True)
)
Epoch 1/5, Loss: 0.1847
Epoch 2/5, Loss: 0.0521
Epoch 3/5, Loss: 0.0372
Epoch 4/5, Loss: 0.0289
Epoch 5/5, Loss: 0.0218
Test accuracy: 0.9909 (9909/10000)
Predicted Class: 7
Actual Class: 7
```

跟簡報的範例輸出（loss 0.1805 → 0.0225）落同一個量級。

<strong>但 loss 曲線不能當「架構還原正確」的證明</strong>：隨機初始化、shuffle 順序一換就會漂，
差 0.01 是日常。真正硬的證據是<strong>參數量</strong>——兩套框架都是 **225,034**
（1×32×9+32、32×64×9+64、1600×128+128、128×10+10），這才是「同一個網路」的意思。
我另外獨立跑一次得到 0.1868／0.0558／0.0373／0.0283／0.0214、test 0.9904，也落在同一條線上。

<strong>注意 `fc1` 的 `in_features=1600`</strong>，正是 `64 × 5 × 5`，跟前面算的一致。

### 單張推論

```python
image, actual_label = test_dataset[0]

with torch.no_grad():
    output = model(image.unsqueeze(0))
    predicted_label = torch.argmax(output, dim=1).item()

print("Predicted Class:", predicted_label)
print("Actual Class:", actual_label)
```

`image.unsqueeze(0)` 是把 `(1, 28, 28)` 變成 `(1, 1, 28, 28)`——加上 batch 維度。
PyTorch 模型永遠吃批次，即使只有一張圖。

## 九、兩套框架逐層對照

把兩個版本並排看，這才是這份材料真正的教學重點。

| TensorFlow / Keras | PyTorch | 說明 |
|---|---|---|
| `layers.Conv2D(32, (3,3), activation='relu')` | `nn.Conv2d(1, 32, 3)` + `torch.relu` | PyTorch 激活函式要自己接 |
| `layers.MaxPooling2D((2,2))` | `nn.MaxPool2d(2, 2)` | 等價 |
| `layers.Conv2D(64, (3,3), activation='relu')` | `nn.Conv2d(32, 64, 3)` + `torch.relu` | 等價 |
| `layers.Flatten()` | `x.view(-1, 64*5*5)` | PyTorch 要自己算維度 |
| `layers.Dense(128, activation='relu')` | `nn.Linear(64*5*5, 128)` + `torch.relu` | 等價 |
| `layers.Dense(10, activation='softmax')` | `nn.Linear(128, 10)` | <strong>PyTorch 不加 softmax</strong> |
| `loss='sparse_categorical_crossentropy'` | `nn.CrossEntropyLoss()` | 後者內建 softmax |
| `optimizer='adam'` | `optim.Adam(lr=1e-3)` | 兩邊預設都是 1e-3（實測 Keras 3.15.1 與 torch 2.15.0）；PyTorch 慣例把 lr 顯式寫出來 |
| 輸入 `(28, 28, 1)` | 輸入 `(1, 28, 28)` | <strong>通道位置相反</strong> |
| `model.fit(...)` | 自己寫訓練迴圈 | PyTorch 沒有高階 API |

三條最值得記住的差異：

1. **通道位置**：TF 是 `(H, W, C)`，PyTorch 是 `(C, H, W)`。
2. **softmax**：TF 的 `Dense(10, activation='softmax')` 對應 PyTorch 的
   `nn.Linear(128, 10)` <strong>不加激活</strong>，因為 `CrossEntropyLoss` 已經內含。
3. **訓練迴圈**：Keras 一行 `fit()`，PyTorch 要手寫
   `zero_grad → forward → loss → backward → step` 五步。

## 十、四個會讓程式當場掛掉的坑

這些是簡報不會告訴你、但實測一定會遇到的。

### 坑一：攝影機不一定在 index 0

這是最陰險的一個。`cv2.VideoCapture(0)` <strong>會成功開啟、不會報錯</strong>，
但畫面上是純黑。你不會看到任何錯誤訊息，只會覺得「怎麼都偵測不到東西」。

實測列舉本機攝影機：

| 索引 | 畫面平均亮度 | 實際狀況 |
|---|---|---|
| camera 0 | 2.4 | 虛擬設備，黑畫面 |
| camera 1 | 2.5 | 黑畫面 |
| camera 2 | 93～110 | <strong>真正的攝影機</strong> |

修法是逐個試、看畫面亮度：

```python
def pick_camera(preferred=0, max_index=6, min_brightness=20.0, warmup=1.0):
    """回傳第一個真的有畫面的攝影機（已開好、已暖機）。"""
    order = [preferred] + [i for i in range(max_index + 1) if i != preferred]
    for idx in order:
        # 注意這一行：寫死 CAP_DSHOW，在 Linux/macOS 上會每個 index 都開不起來
        api = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY
        cap = cv2.VideoCapture(idx, api)
        if not cap.isOpened():
            cap.release()
            continue
        mean = -1.0
        t0 = time.time()
        while time.time() - t0 < warmup:   # 等自動曝光穩定（用時間，不是固定幀數）
            ok, frame = cap.read()
            if ok and frame is not None:
                mean = float(frame.mean())
        if mean >= min_brightness:
            print(f"using camera {idx} (brightness {mean:.0f})")
            return cap
        cap.release()
        print(f"camera {idx}: black (mean {mean:.1f}) - skip")
    return None
```

### 坑二：Windows 上要用 DirectShow

`VideoCapture(0)` 不指定後端時，Windows 會自己挑，但常常挑到打不開的那個。
實測 `CAP_MSMF` 就是打不開的。要依序重試：

```python
backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
for api in backends:
    cap = cv2.VideoCapture(0, api)
    if cap.isOpened():
        break
```

### 坑三：攝影機剛開的前幾幀不能用

自動曝光需要 1～2 秒才穩定，這段時間的畫面會過曝或全黑。
直接拿去偵測會得到一堆假結果。

<strong>這裡有個容易寫錯的地方</strong>：丟「10 幀」聽起來夠，但 30 fps 下只有 0.33 秒，
根本不到 1～2 秒。要用時間當條件：

```python
import time

t0 = time.time()
while time.time() - t0 < 1.5:      # warmup：1.5 秒
    cap.read()
# 開始真正處理
```

### 坑四：`imshow` 沒有 fallback 會直接崩

如果程式跑在 headless 環境（例如考試機、伺服器），
`cv2.imshow` 會拋出 `not implemented` 例外，整個程式當場結束。
正確做法是先偵測、不能彈窗就轉成存檔模式：

```python
def imshow_available():
    try:
        cv2.imshow("__probe__", np.zeros((4, 4, 3), np.uint8))
        cv2.waitKey(1)
        cv2.destroyWindow("__probe__")
        return True
    except Exception:
        return False

show_gui = imshow_available()
# 之後用 if show_gui: cv2.imshow(...) 包起來
```

## 十一、檔案清單

全部腳本都在 **[kalpakjian/ivdc_handout](https://github.com/kalpakjian/ivdc_handout)** 的 `src/`，各自獨立可跑。
每一支都用註解標了 `# [原文]`（簡報截圖讀得到）與 `# [補完]`（截圖被遮住／講義省略），
標在原本那一行旁邊——不用回頭翻這篇文章找「哪段是他補的」。

| 檔案 | 內容 |
|---|---|
| [`00_check_env.py`](https://github.com/kalpakjian/ivdc_handout/blob/main/src/00_check_env.py) | 環境自檢（套件、GUI、攝影機） |
| [`01_tf_object_detection_image.py`](https://github.com/kalpakjian/ivdc_handout/blob/main/src/01_tf_object_detection_image.py) | TF 單張圖偵測 |
| [`02_tf_webcam_detection.py`](https://github.com/kalpakjian/ivdc_handout/blob/main/src/02_tf_webcam_detection.py) | TF 即時偵測 |
| [`03_torch_object_detection_image.py`](https://github.com/kalpakjian/ivdc_handout/blob/main/src/03_torch_object_detection_image.py) | PyTorch 單張圖偵測 |
| [`04_torch_webcam_detection.py`](https://github.com/kalpakjian/ivdc_handout/blob/main/src/04_torch_webcam_detection.py) | PyTorch 即時偵測（多模型可切換） |
| [`05_yolo_detection.py`](https://github.com/kalpakjian/ivdc_handout/blob/main/src/05_yolo_detection.py) | YOLOv8 偵測 |
| [`06_tf_cnn_mnist.py`](https://github.com/kalpakjian/ivdc_handout/blob/main/src/06_tf_cnn_mnist.py) | TF CNN 分類 |
| [`07_torch_cnn_mnist.py`](https://github.com/kalpakjian/ivdc_handout/blob/main/src/07_torch_cnn_mnist.py) | PyTorch CNN 分類 |

跑法（每支都支援 `--no-show` 與 `--max-frames`，沒有螢幕的機器也跑得完）：

```bash
python 00_check_env.py                                   # 先自檢
python 04_torch_webcam_detection.py                      # 即時偵測
python 04_torch_webcam_detection.py --model fasterrcnn_mobilenet_320
python 04_torch_webcam_detection.py --model fasterrcnn_resnet50_fpn --min-size 400
python 07_torch_cnn_mnist.py                             # CNN 訓練
python 02_tf_webcam_detection.py --no-show --max-frames 60
```

## 十二、幾點檢討

**簡報的「Real Time」需要打折看。** 標題寫的是即時偵測，但簡報示範的
Faster R-CNN + resnet50 在 CPU 上只有 1.1～1.4 FPS（兩台機器各量一次）。這不是簡報寫錯，
而是它假設有 GPU。在 CPU 環境下必須換 backbone 或改用 YOLO 才真的即時。

不過「換 backbone」之前還有一個更便宜的旋鈕沒提：`fasterrcnn_resnet50_fpn` 預設
`min_size=800`，會把 720p 的短邊放大到 800（約 1422×800），CPU 上光這一步就吃掉大半時間。
降到 400 通常能拿回 2～3 倍 FPS，掉不到幾個點：

```python
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(
    weights="DEFAULT", min_size=400, max_size=667)
```

**「推薦 YOLO」只在「好用」這件事上成立。** 同一段畫面上 `yolov8n`（640）35.8 FPS
對上簡報示範的 `fasterrcnn_resnet50_fpn` 1.4 FPS，差 <strong>25.6 倍</strong>，而且只有四行程式碼。
但換成同一個 torchvision 家族的 `ssdlite320_mobilenet_v3_large`（33.1 FPS），
在 `bus.jpg` 上它的信心其實<strong>更高</strong>：`person 0.989`／`bus 0.985`，
YOLOv8n 是 `person 0.866`／`bus 0.873`。
所以「記 YOLO」的理由是<strong>四行程式碼、換模型不用改程式</strong>，不是數字最漂亮——
速度與準確度的天花板，`ssdlite320` 站在同一格。

**還原截圖程式碼有風險。** 逐頁比對之後，被截圖的向下捲動箭頭遮住程式碼的是
<strong>7 頁</strong>（第 2、3、5、6、18、19、22 頁），我第一版只寫「三處」是低估。
補完的部分依框架的標準介面寫，而且每一段都在腳本裡標註了哪些是原文、
哪些是補的——這種標註習慣比程式碼本身重要，否則半年後連自己都分不清。
腳本現在公開在 [kalpakjian/ivdc_handout](https://github.com/kalpakjian/ivdc_handout)，
`# [原文]`／`# [補完]` 就標在原本那幾行旁邊，讀者可以直接查證。

**TensorFlow 那三支腳本，改版後補跑了。** 這台機器的 Python 3.15 裝不上 TensorFlow，
但我原本下的結論（「所以只驗證語法」）是錯的——用 `uv run --python 3.11` 隔離環境就行：
`06_tf_cnn_mnist.py` 實跑 test accuracy **0.9872**、`01` 在官方 `bus.jpg` 上
person 0.861／bus 0.756、`02` 在 webcam 上 **8.6 FPS**。

**真正卡住人的是 `tensorflow_hub` 被 setuptools 版本搞死。** 它 import 時會
`from pkg_resources import parse_version`，而 setuptools 81 之後把 `pkg_resources` 移除了。
實測 setuptools 84.0.0 → `ModuleNotFoundError: No module named 'pkg_resources'`，
而且錯在 import 階段，訊息完全看不出跟 TF Hub 有關（很容易誤判成模型網址壞了）。裝舊的就好：

```bash
uv run --no-project --python 3.11 --with tensorflow-cpu \
    --with tensorflow-hub --with 'setuptools<81' -- python 01_tf_object_detection_image.py
```

順帶一個容易誤判的：`tfhub.dev` 的網址用 `curl` 去摸會回 404（網頁層已下架），
但 `hub.load()` 仍然解析得到模型檔。**404 不代表模型沒了**，別急著換 URL。

**torchvision 的 SSD 家族沒有 `.weights` 屬性。** 想印類別名稱時
`model.weights.meta["categories"]` 在 Faster R-CNN 上可以，在 `ssdlite320_mobilenet_v3_large`
上會 `AttributeError`；要改從 `WeightsEnum` 拿
（`get_weight("SSDLite320_MobileNet_V3_Large_Weights.DEFAULT")`）。

**最後，換一個說法。** 這一版把「實測」兩個字重新校準：數字都附環境
（TF 2.21.0 / Keras 3.15.1 / torch 2.15.0+cpu / torchvision 0.29.2+cpu / OpenCV 5.0.0 / Python 3.11 與 3.14），
跑不動的項目直接寫跑不動，而不是用「應該吻合」填空。
