# Lesson 8：TensorFlow 與 PyTorch 的物件偵測與 CNN 學習筆記

> 同一堂課用兩套框架各寫一遍：物件偵測（webcam 與 YOLO）與 CNN 分類（MNIST）。<br />
> 本筆記把簡報裡以截圖呈現的程式碼逐段還原成可執行版本，並在真機上重新實測每一段。<br />
> 量到的速度與準確度直接寫進內文，速度不如預期的地方也照實記錄。<br />
> 只想複習考點的話，看附錄 C 的一頁精華就夠。

## 0. 30 秒總複習（考前最後掃描）

```
物件偵測：載入模型 → 讀圖轉張量 → 模型推論 → 過濾門檻 → 畫框 → 顯示
CNN 分類：載入資料 → 前處理(reshape/255) → 建模型 → 訓練 → 單張推論
```

| 想問的事 | 一句話答案 |
|---|---|
| 兩套框架最根本的差異 | 張量格式：TF 是 `(H,W,C)`，PyTorch 是 `(C,H,W)` |
| PyTorch 為何不加 softmax | `CrossEntropyLoss` 內含 softmax，加了等於算兩次 |
| TensorFlow 的框座標格式 | 歸一化 0～1，順序 `ymin, xmin, ymax, xmax` |
| PyTorch 的框座標格式 | 絕對像素，順序 `x0, y0, x1, y1` |
| CPU 上最快又能用的模型 | YOLOv8n `imgsz=640`，實測約 37 FPS |
| 簡報示範的模型為何卡 | `fasterrcnn_resnet50` 在 CPU 只有約 1 FPS |
| 為何 `Conv2D` 要 reshape | 要補上通道維度，灰階圖通道數為 1 |
| `64 × 5 × 5` 怎麼來的 | 28→26→13→11→5，兩次卷積兩次池化 |
| 攝影機開得起來卻全黑 | 索引不對，實際裝置可能不在 0 |
| 為何 imshow 會當掉 | headless 版 opencv 沒有實作 GUI 後端 |

## 1. 這份材料在教什麼

課程簡報的結構很對稱，分成兩大塊，每塊都用兩個框架各講一次：

| 區塊 | 內容 | 對應腳本 |
|---|---|---|
| 物件偵測（TensorFlow） | SSD MobileNet V2，單張圖與即時 webcam | `01`、`02` |
| 物件偵測（PyTorch） | Faster R-CNN，單張圖與即時 webcam | `03`、`04` |
| 物件偵測（推薦方案） | YOLOv8，四行程式 | `05` |
| CNN 分類（TensorFlow） | MNIST 數字分類，五個階段 | `06` |
| CNN 分類（PyTorch） | MNIST 數字分類，同樣五個階段 | `07` |

兩個 CNN 區塊的流程完全一樣，都是**載入資料 → 建模型 → 訓練 → 看輸出 → 單張推論**。
這種安排是刻意的：先看懂一個，再看另一個，差異就只剩 API 名稱。

課程對模型選擇也有明確建議：

| 模型 | 特性 |
|---|---|
| SSD MobileNet V2 | 快，適合即時應用，初學者最容易上手 |
| EfficientDet | 準確度更好，速度尚可 |
| Faster R-CNN | 準確度高但慢 |
| YOLOv8 | 速度與準確度平衡最好，課程標註為推薦方案 |
| DETR | Transformer 架構，準確度好但吃資源 |

## 2. 先把環境量清楚

在寫任何程式之前先確認機器上有什麼。這個動作後來證明很關鍵，
因為它直接揭露了第一個致命問題。

| 套件 | 版本 | 狀態 |
|---|---|---|
| Python | 3.15.1 | 可用 |
| torch | 2.14.1+cpu | 已裝 |
| torchvision | 0.29.1+cpu | 已裝 |
| numpy | 2.5.4 | 已裝 |
| opencv | 5.0.0 | 已裝，但沒有 GUI |
| matplotlib | 3.11.2 | 已裝 |
| pillow | 13.0.0 | 已裝 |
| tensorflow | 未安裝 | 需另外安裝 |
| ultralytics | 未安裝 | 需另外安裝 |

自檢腳本的核心是這一段。注意 <strong>`imshow` 必須真的呼叫一次</strong>，
不能只檢查函式是否存在：

```python
import importlib
import cv2
import numpy as np

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

try:
    print("  UI 框架:", cv2.currentUIFramework() or "(空 = 無)")
    cv2.imshow("__probe__", np.zeros((20, 20, 3), np.uint8))
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    print("  OK  可以正常彈窗")
except Exception as exc:
    print(f"  失敗: {exc}")
```

### 2.1 第一個坑：`hasattr` 檢查不出 imshow 的問題

`hasattr(cv2, "imshow")` 會回傳 `True`，但實際呼叫卻拋出例外：

```
cv2.error: (-2:Unspecified error) The function is not implemented.
Rebuild the library with Windows, GTK+ 2.x or Cocoa support.
```

這是因為裝的是 `opencv-python-headless`，<strong>函式存在、後端沒有實作</strong>。
`currentUIFramework()` 回傳空字串就是徵兆。修法是換成帶 GUI 的版本：

```powershell
pip uninstall opencv-python-headless -y
pip install opencv-python
```

換完之後 `UI 框架` 顯示 `WIN32`，`imshow` 恢復正常。

## 3. 物件偵測：TensorFlow 版

課程示範使用 TF-Hub 的 SSD MobileNet V2。載入模型與前處理的部分如下：

```python
import tensorflow as tf
import tensorflow_hub as hub
import cv2

MODEL_URL = "https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2"

model = hub.load(MODEL_URL)

image = cv2.imread("image.jpg")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

input_tensor = tf.convert_to_tensor(image_rgb, dtype=tf.uint8)
input_tensor = tf.expand_dims(input_tensor, 0)   # (1, H, W, 3)
```

推論與取結果的部分，簡報的截圖被遮住了，依標準介面補完：

```python
detections = model(input_tensor)

boxes = detections["detection_boxes"][0].numpy()
scores = detections["detection_scores"][0].numpy()
classes = detections["detection_classes"][0].numpy().astype(int)
```

<strong>這裡最容易寫錯的是座標格式</strong>：`detection_boxes` 是歸一化的 0～1，
順序為 `ymin, xmin, ymax, xmax`，要各自乘上畫面寬高才能畫。

### 3.1 即時 webcam 版

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

    h, w = frame.shape[:2]
    for box, score in zip(detections["detection_boxes"][0].numpy(),
                          detections["detection_scores"][0].numpy()):
        if score < 0.5:
            continue
        ymin, xmin, ymax, xmax = box
        cv2.rectangle(frame, (int(xmin * w), int(ymin * h)),
                      (int(xmax * w), int(ymax * h)), (0, 0, 255), 2)

    cv2.imshow("Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

## 4. 物件偵測：PyTorch 版

同一件事換一套框架，差異一目了然。課程示範的模型是 `fasterrcnn_resnet50_fpn`：

```python
import torch
import torchvision
from torchvision import transforms
from PIL import Image

model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")
model.eval()

image = Image.open("image.jpg").convert("RGB")
transform = transforms.ToTensor()
tensor = transform(image).unsqueeze(0)      # (1, 3, H, W)

with torch.no_grad():
    prediction = model(tensor)[0]

boxes = prediction["boxes"].numpy()
scores = prediction["scores"].numpy()
labels = prediction["labels"].numpy()
```

跟 TensorFlow 版比，有兩個關鍵差異：

1. <strong>`model.eval()` 一定要呼叫</strong>。Faster R-CNN 在 train 模式下回傳的是 loss，不是預測框。
2. <strong>座標是絕對像素</strong>，順序 `[x0, y0, x1, y1]`，不需要再乘寬高。

鍵名對照如下，兩套框架一一對應但名稱不同：

| TensorFlow | PyTorch |
|---|---|
| `detection_boxes` | `boxes` |
| `detection_scores` | `scores` |
| `detection_classes` | `labels` |

### 4.1 即時 webcam 版

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

    for box, score in zip(prediction["boxes"].numpy(),
                          prediction["scores"].numpy()):
        if score < 0.5:
            break      # 已依分數降序排列
        x0, y0, x1, y1 = [int(v) for v in box]
        cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)

    cv2.imshow("PyTorch Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
```

torchvision 的偵測結果已經依信心分數由高到低排序，
所以門檻判斷可以用 `break` 而不是 `continue`。

## 5. YOLOv8：四行方案

課程把 YOLO 標為推薦方案，內文只有四行：

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.predict(source=0, show=True)
```

實務上會加上幾個參數：

```python
results = model.predict(
    source=0,
    show=True,
    conf=0.25,
    imgsz=640,      # 推論解析度
    stream=True,    # webcam 要開
)
```

## 6. 實測：速度與準確度的取捨

課程把這段標題定為即時偵測，但實測並不是每個模型都做得到。
以下數字取自同一台機器、同一個 1280×720 畫面，程式跑在 CPU 上：

| 模型 | 速度 | 最高信心分數 | 檢出數 |
|---|---|---|---|
| `fasterrcnn_resnet50` | 1.1 FPS | 0.830 | 4 |
| `fasterrcnn_mobilenet` | 5.4 FPS | 0.938 | 1 |
| `fasterrcnn_mobilenet_320` | 24.6 FPS | 0.194 | 0 |
| `ssdlite320` | 19.5 FPS | 0.355 | 1 |

> ⚠️ 這張表是**跨基準線**的舊版數字（torchvision 用 webcam 實況、YOLO 用 `bus.jpg`）。同一段畫面重測後的結果與解讀，以文章版為準 → [同一份課堂材料，用 TensorFlow 與 PyTorch 各跑一遍](https://kalpakjian.github.io/2026/11/03/ivdc-tf-pytorch-object-detection-cnn/)

<strong>這裡有一個反直覺的結果</strong>：最快的 `mobilenet_320` 竟然什麼都沒偵測到。
它把輸入縮到 320×320，小目標全部糊掉，加上場景光線偏暗，信心分數最高只有 0.19。
所以快與有用是兩件事，預設值要選在平衡點上。

YOLOv8n 的表現好很多，而且解析度可控：

| imgsz | 速度 | 準確度（官方測試圖） |
|---|---|---|
| 640 | 37.4 FPS | bus 0.87、person 0.87／0.85／0.83 |
| 960 | 18.8 FPS | 中間檔 |
| 1280 | 11.1 FPS | 同圖檢出 7 個，小目標更完整 |

YOLO 在 640 解析度下就有約 37 FPS，比課程示範的 Faster R-CNN 快約 34 倍，
準確度也沒有犧牲。課程標註推薦方案，實測確實如此。

<strong>要注意的另一個陷阱</strong>：用昏暗的室內畫面測 YOLO 也會 0 檢出。
不是所有東西都在 COCO 的 80 個類別裡，洗衣機不在其中，
模型會硬猜成 toilet 或 truck，信心分數自然低。換成官方測試圖就完全正常。

## 7. CNN 分類：TensorFlow 版

用 MNIST 手寫數字做分類，五個階段。

### 7.1 載入資料

```python
from tensorflow.keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

print("Training Data Shape:", x_train.shape)   # (60000, 28, 28)
print("Test Data Shape:", x_test.shape)        # (10000, 28, 28)
```

### 7.2 前處理

```python
x_train = x_train.reshape(-1, 28, 28, 1) / 255.0
x_test = x_test.reshape(-1, 28, 28, 1) / 255.0
```

`reshape` 多出來的那一維是<strong>通道數</strong>。`Conv2D` 要求輸入為 `(H, W, C)`，
灰階圖的 C 就是 1。除以 255 是正規化到 0～1。

### 7.3 建立模型

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

### 7.4 編譯與訓練

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

### 7.5 單張推論

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

`np.argmax` 取出 10 個機率裡最大的索引，那就是預測的數字。

## 8. CNN 分類：PyTorch 版

同樣五個階段，換 PyTorch 寫。這段已在本機完整跑完訓練。

### 8.1 載入資料

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

形狀是 `(1, 28, 28)`，通道在最前面，跟 TensorFlow 的 `(28, 28, 1)` 相反。
這是兩套框架最根本的差異之一。

### 8.2 建立模型

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

<strong>`64 × 5 × 5` 這個數字怎麼來的</strong>：28 進 3×3 卷積（無 padding）得 26，
池化得 13，再卷積得 11，再池化得 5。所以特徵圖是 `64 × 5 × 5`。
這個計算是初學者最常卡住的地方。

PyTorch 版<strong>最後一層沒有 softmax</strong>。因為 `CrossEntropyLoss` 內部已經含 softmax，
再加一次等於算了兩遍。

### 8.3 訓練

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

### 8.4 實測結果

本機實際跑完的完整輸出：

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

注意 `fc1` 的 `in_features=1600`，正是 `64 × 5 × 5`，跟前面的計算一致。

### 8.5 單張推論

```python
image, actual_label = test_dataset[0]

with torch.no_grad():
    output = model(image.unsqueeze(0))
    predicted_label = torch.argmax(output, dim=1).item()

print("Predicted Class:", predicted_label)
print("Actual Class:", actual_label)
```

`image.unsqueeze(0)` 把 `(1, 28, 28)` 變成 `(1, 1, 28, 28)`，也就是加上 batch 維度。
PyTorch 模型永遠吃批次，即使只有一張圖。

## 9. 兩套框架逐層對照

把兩個版本並排看，這才是這份材料真正的教學重點。

| TensorFlow / Keras | PyTorch | 說明 |
|---|---|---|
| `layers.Conv2D(32, (3,3), activation='relu')` | `nn.Conv2d(1, 32, 3)` + `torch.relu` | 激活函式要自己接 |
| `layers.MaxPooling2D((2,2))` | `nn.MaxPool2d(2, 2)` | 等價 |
| `layers.Conv2D(64, (3,3), activation='relu')` | `nn.Conv2d(32, 64, 3)` + `torch.relu` | 等價 |
| `layers.Flatten()` | `x.view(-1, 64*5*5)` | 要自己算維度 |
| `layers.Dense(128, activation='relu')` | `nn.Linear(64*5*5, 128)` + `torch.relu` | 等價 |
| `layers.Dense(10, activation='softmax')` | `nn.Linear(128, 10)` | 不加 softmax |
| `loss='sparse_categorical_crossentropy'` | `nn.CrossEntropyLoss()` | 後者內建 softmax |
| `optimizer='adam'` | `optim.Adam(lr=1e-3)` | 兩邊預設都是 1e-3（實測） |
| 輸入 `(28, 28, 1)` | 輸入 `(1, 28, 28)` | 通道位置相反 |
| `model.fit(...)` | 自己寫訓練迴圈 | PyTorch 沒有高階 API |

三條最值得記住的差異：

1. **通道位置**：TF 是 `(H, W, C)`，PyTorch 是 `(C, H, W)`。
2. **softmax**：TF 的 `Dense(10, activation='softmax')` 對應 PyTorch 的
   `nn.Linear(128, 10)` <strong>不加激活</strong>，因為 `CrossEntropyLoss` 已經內含。
3. **訓練迴圈**：Keras 一行 `fit()`，PyTorch 要手寫
   `zero_grad → forward → loss → backward → step` 五步。

## 10. 四個會讓程式當場掛掉的坑

這些是課程不會告訴你、但實測一定會遇到的。

### 10.1 攝影機不一定在 index 0

這是最陰險的一個。`cv2.VideoCapture(0)` <strong>會成功開啟、不會報錯</strong>，
但畫面上是純黑。不會看到任何錯誤訊息，只會覺得怎麼都偵測不到東西。

實測列舉本機攝影機：

| 索引 | 畫面平均亮度 | 實際狀況 |
|---|---|---|
| camera 0 | 2.4 | 虛擬設備，黑畫面 |
| camera 1 | 2.5 | 黑畫面 |
| camera 2 | 93～110 | 真正的攝影機 |

修法是逐個試、看畫面亮度：

```python
def pick_camera(preferred=0, max_index=6, min_brightness=20.0):
    """回傳第一個真的有畫面的攝影機索引。"""
    order = [preferred] + [i for i in range(max_index + 1) if i != preferred]
    for idx in order:
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap.release()
            continue
        mean = -1.0
        for _ in range(12):          # 等自動曝光穩定
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

### 10.2 Windows 上要用 DirectShow

`VideoCapture(0)` 不指定後端時，Windows 會自己挑，但常常挑到打不開的那個。
實測 `CAP_MSMF` 就是打不開的。要依序重試：

```python
backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
for api in backends:
    cap = cv2.VideoCapture(0, api)
    if cap.isOpened():
        break
```

### 10.3 攝影機剛開的前幾幀不能用

自動曝光需要 1～2 秒才穩定，這段時間的畫面會過曝或全黑。
直接拿去偵測會得到一堆假結果。修法是丟掉前 N 幀：

```python
frames = 0
while True:
    ret, frame = cap.read()
    frames += 1
    if frames <= 10:      # warmup
        continue
    # 開始真正處理
```

### 10.4 imshow 沒有 fallback 會直接崩

如果程式跑在 headless 環境（例如考試機、伺服器），
`cv2.imshow` 會拋出例外，整個程式當場結束。
正確做法是先偵測、不能彈窗就轉成存檔模式：

```python
import numpy as np

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

## 11. 檔案清單

全部腳本各自獨立可跑：

| 檔案 | 內容 |
|---|---|
| `00_check_env.py` | 環境自檢（套件、GUI、攝影機） |
| `01_tf_object_detection_image.py` | TF 單張圖偵測 |
| `02_tf_webcam_detection.py` | TF 即時偵測 |
| `03_torch_object_detection_image.py` | PyTorch 單張圖偵測 |
| `04_torch_webcam_detection.py` | PyTorch 即時偵測（多模型可切換） |
| `05_yolo_detection.py` | YOLOv8 偵測 |
| `06_tf_cnn_mnist.py` | TF CNN 分類 |
| `07_torch_cnn_mnist.py` | PyTorch CNN 分類 |

跑法：

```powershell
python 00_check_env.py                                   # 先自檢
python 04_torch_webcam_detection.py                      # 即時偵測
python 04_torch_webcam_detection.py --model fasterrcnn_resnet50
python 07_torch_cnn_mnist.py                             # CNN 訓練
```

## 12. 幾點檢討

**課程標題的即時偵測需要打折看。** 標題寫的是即時偵測，但課程示範的
Faster R-CNN + resnet50 在 CPU 上只有 1.1 FPS。這不是課程寫錯，
而是它假設有 GPU。在 CPU 環境下必須換 backbone 或改用 YOLO 才真的即時。

**推薦 YOLO 是有道理的。** 實測差距 34 倍，而且 YOLO 的程式碼只有四行。
如果只能記一個方案，記 YOLO。

**還原截圖程式碼有風險。** 課程簡報有三處程式碼被滾動箭頭遮住，
只能依框架的標準介面補完。補完的部分在腳本裡都標註了哪些是原文、
哪些是補的，這種標註習慣比程式碼本身重要。

**TensorFlow 那三支腳本，改版後補跑了。** 用 `uv run --python 3.11` 隔離環境就行（06 實跑 test accuracy 0.9872、01 在 bus.jpg 上 person 0.861／bus 0.756、02 在 webcam 上 8.6 FPS）。真正卡住人的是 `tensorflow_hub` 依賴 `pkg_resources`，而 setuptools 81 之後把它移除了（實測 84.0.0 → ModuleNotFoundError），要 `--with 'setuptools<81'`。原本的 Python 3.15
裝不上 TensorFlow，所以 `01`／`02`／`06` 只驗證了語法與錯誤處理路徑。
PyTorch 那條線（`03`／`04`／`07`）是完整跑過的。

---

*本頁為個人學習筆記整理。*

## 附錄 A：名詞速查

| 名詞 | 說明 |
|---|---|
| 物件偵測 | 找出圖中物件的位置（框）與類別 |
| 邊界框（bounding box） | 框住物件的矩形，格式各框架不同 |
| 信心分數（score） | 模型對該偵測的信心，0～1 |
| 非極大值抑制（NMS） | 去掉重疊的重複框，偵測模型內部處理 |
| COCO 80 類 | 通用偵測模型的類別集，不含洗衣機等 |
| `detection_boxes` | TF 的框，歸一化 0～1，順序 ymin/xmin/ymax/xmax |
| `boxes` | PyTorch 的框，絕對像素，順序 x0/y0/x1/y1 |
| `model.eval()` | 切到推論模式，偵測模型必呼叫 |
| `torch.no_grad()` | 關閉梯度記錄，省記憶體並加速 |
| `unsqueeze(0)` | 加上 batch 維度 |
| 通道位置 | TF 用 (H,W,C)，PyTorch 用 (C,H,W) |
| `CrossEntropyLoss` | PyTorch 的交叉熵，內建 softmax |
| `sparse_categorical_crossentropy` | Keras 對應版本，標籤為整數時使用 |
| `ToTensor()` | PIL 影像轉張量，同時縮放到 0～1 |
| stride | 卷積核移動步長 |
| 特徵圖（feature map） | 卷積輸出的每個通道 |
| warmup 幀 | 攝影機開頭不穩定的幀，應丟棄 |

## 附錄 B：常見陷阱

| 症狀 | 原因 | 處理 |
|---|---|---|
| 畫面全黑但不報錯 | 選到虛擬攝影機 | 逐個索引試亮度 |
| `objects 0` 但畫面正常 | 門檻太高或物件不在 COCO 類別 | 降門檻、換真實物件 |
| `The function is not implemented` | headless opencv | 裝 `opencv-python` 或改存檔模式 |
| 一直 1 FPS | resnet50 太重 | 換 mobilenet backbone 或 YOLO |
| 框畫在錯的位置 | TF 忘了乘寬高 | 歸一化座標要乘回像素 |
| `mat1 and mat2 shapes cannot be multiplied` | `view` 的維度算錯 | 檢查 `64*5*5` |
| 偵測模型回傳 loss 不是框 | 忘了 `model.eval()` | 補呼叫 |
| 訓練 loss 不下降 | 忘了除以 255 正規化 | 前處理補上 |
| `cannot open video source` | 攝影機被其他程式占用 | 關掉 Teams／Zoom／微信 |
| CUDA out of memory | 批次太大 | 降 batch size |

## 附錄 C：一頁精華（考前 10 分鐘）

```
【物件偵測三方案】

TensorFlow   hub.load(SSD MobileNet V2)
             → tf.expand_dims(img, 0)
             → detections["detection_boxes"]（歸一化 0~1）

PyTorch      fasterrcnn_resnet50_fpn(weights="DEFAULT")
             → model.eval()（必呼叫）
             → prediction["boxes"]（絕對像素 x0,y0,x1,y1）

YOLO         YOLO("yolov8n.pt").predict(source=0, show=True)
             （四行完成，實測最快）

【CNN 五階段】
載入 → 前處理(reshape + /255) → 建模型 → 訓練 → 單張推論

【張量格式】
TF      (60000, 28, 28, 1)    通道在最後
PyTorch (60000, 1, 28, 28)    通道在前
```

## 附錄 D：互動測驗（40 題）

本筆記附 40 題線上測驗，即時計分、進度自動儲存，可離線使用。




