---
archive: true   # 已歸入 /cnn/ 專題目錄，不列在首頁
title: 手寫數字辨識入門：用 MNIST 看懂 CNN 到底在學什麼（PyTorch 實作 ＋ feature map 視覺化）
date: 2026-10-27 13:20:00
categories:
  - 學習資源
tags:
  - CNN
  - 卷積神經網路
  - PyTorch
  - MNIST
  - 電腦視覺
  - 學習筆記
  - 實作
toc: true
math: true
index_img: /img/covers/cnn-mnist-lab.png
banner_img: /img/covers/cnn-mnist-lab.png
---

> 📚 這篇文章已歸入主題目錄：[CNN 專題](/cnn/)（九篇圖解系列、課程筆記與實驗都在那裡）。

> <strong>一句話結論</strong>：把 CS231n 筆記裡的公式寫成 <code>if</code> 會比背下來有用得多——我讓訓練迴圈在每個 epoch 開頭把「公式推導」與「實際張量形狀」逐層比對，任何一層對不上就印 <code>✗</code>。
> 這個小改動讓「輸出尺寸公式」從需要記憶的規則，變成每次跑都會自我驗證的斷言。

先說清楚：這篇預設讀者跟我一樣，是**沒受過正規訓練、只是想把東西弄懂**的人，不是要交作業的研究生。所以如果你看到「3Blue1Brown」「CS231n」「MNIST」這三個名字只覺得是一串英文加數字——**下一節就是為你寫的三分鐘白話版**，看完再往下走完全來得及。

這篇是 **3Blue1Brown 建立直覺 → CS231n 學嚴謹原理 → PyTorch 動手做** 這條路線的第一個完整實作紀錄。

不是再寫一份「CNN 入門教學」，而是把整條鏈路**跑到底並留下可重現的產物**：模型、7 項自我測試、訓練曲線，以及三張用來證明「CNN 真的在學特徵」的視覺化圖。

<!-- more -->

![用手寫數字看懂 CNN：filter、feature map 與感受野](/img/covers/cnn-mnist-lab.png)

---

## 先補課：三個名字、一個縮寫，各三分鐘

三個都是**免費資源**，都不用註冊帳號，也不是要安裝的套件。先補一個縮寫：

> **CNN = Convolutional Neural Network，卷積神經網路。** 先粗暴地想成「拿一個小窗口（例如 3×3 的格子）從左到右、從上到下掃過整張圖，每個位置算一個分數」的網路。那個小窗口叫 **kernel（卷積核，也叫 filter／濾波器）**，掃出來的結果叫 **feature map（特徵圖）**。本文後面出現的 filter、kernel、卷積核，指的都是同一件事。

| 名字 | 一句話 | 形態 | 在本文負責 |
|---|---|---|---|
| **3Blue1Brown** | 把數學畫成動畫的 YouTube 頻道 | 影片，兩份加起來約 1.5 小時 | 讓你「看見」卷積在做什麼 |
| **CS231n** | 史丹佛大學的電腦視覺課 | 課程影片 ＋ 免費線上筆記 | 給你公式與嚴謹定義 |
| **MNIST** | 7 萬張手寫數字圖片 | 資料集，壓縮後約 11 MB | 給你一個能算對錯的靶 |

### 3Blue1Brown：先讓你看見，再談公式

**3Blue1Brown** 是 Grant Sanderson 一個人的數學科普頻道（名字來自他一眼藍、一眼棕）。他用自製的動畫引擎把抽象數學「演」出來：向量、微積分、傅立葉轉換，以及神經網路。官方有中文頻道與字幕，英文不好也能看。

本文用到兩份：

- **[《But what is a convolution?》](https://www.youtube.com/watch?v=KuXjwB4LzSA)**（約 15 分鐘）：卷積核滑過影像時，每個位置到底在算什麼。答案其實很樸素——把 kernel 蓋住的那 3×3 個像素，跟 kernel 的 9 個數字**逐格相乘、全部加起來**，得到一個數字，然後往右移一格。看完這段，`nn.Conv2d(1, 16, 3, padding=1)` 就不再是黑盒。
- **[Neural Networks 系列](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)**（4 集，約 1 小時）：神經元與權重 → 梯度下降 → 反向傳播。它把「為什麼調權重會讓答案變好」畫成動畫，而不是丟一串偏導數給你。

**它給你直覺，不給你形狀。** 影片不會告訴你 28×28 經過 `padding=1`、`kernel=3` 之後仍然是 28×28，也不會告訴你這一層有幾個參數。所以它排第 1 站：先有畫面，再去碰程式。

### CS231n：把直覺寫成可以計算的規則

**CS231n**（全名 *Deep Learning for Computer Vision*，舊名 *Convolutional Neural Networks for Visual Recognition*）是史丹佛大學的電腦視覺課程，授課者包括李飛飛、Andrej Karpathy、Justin Johnson。課程影片公開（2017 版由 Karpathy 主講），但更多人讀的是它的**線上筆記**——免費、可搜尋、有公式，是這個領域最常被回頭查的「字典」。

本文從它拿走三樣東西：

1. **輸出尺寸公式** `W2 = floor((W1 - F + 2P) / S) + 1`：決定每一層的輸出是幾乘幾。
2. **感受野（receptive field）**：某個神經元「看得到」原圖多大的範圍。
3. **權重共享與參數量**：為什麼卷積的參數量跟影像大小無關。

還有一個隱藏好處：CS231n 的作業要求用純 numpy 從零寫 kNN → SVM → 兩層網路 → CNN。那是檢查「我是不是真的懂了」最狠的方式，比任何選擇題都準。

**它給你嚴謹，不給你 PyTorch。** 筆記裡幾乎不出現 `nn.Conv2d`，所以讀完你會算公式，卻可能寫不出來——這正是還需要第 4 站的原因。

### MNIST：那 7 萬張手寫數字

**MNIST** 全名 *Modified National Institute of Standards and Technology database*，是 Yann LeCun、Corinna Cortes、Christopher Burges 在 1998 年整理的資料集（經典的 LeNet-5 論文用的就是它）：

- **70,000 張** 28×28 灰階手寫數字（0–9），其中 **60,000 張訓練、10,000 張測試**
- **10 類**，每張都有標準答案，所以可以直接算準確率
- 原始檔是 **4 個 `.gz`**（IDX 自訂格式，開頭藏著 magic number 與維度），壓縮後約 11 MB
- 每張圖是先把數字縮進 20×20 的框、再依筆畫重心置中貼到 28×28 的畫布上——所以數字總是落在畫面正中央

它是電腦視覺的 “Hello World”：小到 CPU 幾秒就跑完一輪，又真實到能證明你的訓練迴圈沒寫錯。本文那個 **20,490 個參數**的小模型，3 個 epoch、11 秒就到 **98.47%**。

但要說清楚：**MNIST 現在是 sanity check，不是排行榜。** 它太簡單了，隨便一個 CNN 都能 99% 以上，所以它的價值是「先確認資料管線、梯度、形狀都對」，不是證明模型多強。真正的難題在 CIFAR-10、ImageNet。

> 回頭看「坑二」就說得通了：MNIST 的官方網站是 `yann.lecun.com`，連不上時 torchvision 會自動改走 S3 鏡像；而本文的「IDX 手動解析備援」處理的，就是那四個 `.gz` 裡的 magic number 與 shape。

### 第四個名字：fast.ai

嚴格說是第 4 站。**fast.ai** 是 Jeremy Howard 創辦的免費實務導向深度學習課程，Lesson 8 專門從程式碼角度拆解 convolution、pooling、dropout。它適合排在「已經有公式與直覺」之後，因為它解決的是最後一哩路：**讀得懂，但寫不出來**。

<hr>

**三分鐘版本總結**：3Blue1Brown 讓你知道「為什麼要這樣算」，CS231n 讓你算得出「這層輸出幾乘幾、有幾個參數」，MNIST 讓你有一個能立刻驗證對錯的靶。三個都免費，加起來不到一天的學習量，但少了任何一個，後面就會卡在很具體的地方。

---

## 這條路線的四站，缺一站就會卡住

把上面三個名字排進順序，就是這四站。每一站解決的問題不同，**跳過任何一站，卡住的點都很具體**：

| 站 | 資源 | 解決什麼問題 | 不看會卡在哪 |
|---|---|---|---|
| 1 | [3Blue1Brown《But what is a convolution?》](https://www.youtube.com/watch?v=KuXjwB4LzSA) | kernel 滑動時到底在算什麼 | 看公式會覺得「為什麼要這樣算」 |
| 2 | [3Blue1Brown Neural Networks 系列](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) | weights、activation、梯度下降 | 反向傳播變成背書 |
| 3 | [Stanford CS231n Convolutional Networks](https://cs231n.github.io/convolutional-networks/) | convolution、receptive field、輸出尺寸公式 | 會寫 `nn.Conv2d` 但不知道參數怎麼算 |
| 4 | [fast.ai Lesson 8 (CNNs)](https://course.fast.ai/Lessons/lesson8.html) | 從程式碼角度拆解 convolution、pooling、dropout | 讀得懂課本但寫不出來 |

第 3 站最值得精讀，第 4 站最能加速「從看懂到寫出來」。**如果你是第一次碰，順序不要顛倒**：先看第 1 站建立畫面，再回頭讀第 3 站的公式，否則很容易變成「公式都會算，但不知道它在算什麼」。

---

## 環境：兩個真實的坑

實測環境（2026-10-27）：

| 項目 | 值 |
|---|---|
| OS | Windows 11 |
| Python | 3.15.1（系統 Python） |
| PyTorch | **2.14.1+cpu** |
| torchvision | 0.29.1+cpu |
| matplotlib | 3.11.2 |
| 裝置 | CPU（無 CUDA wheel） |

**坑一：Python 3.15 太新，PyPI 還沒有對應 wheel 的直覺是錯的。** 事實上 `download.pytorch.org/whl/cpu` 已經有 `torch-2.14.1+cpu-cp315-cp315-win_amd64.whl`，直接安裝即可：

```powershell
python -m pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision
python -m pip install matplotlib
```

**坑二：`yann.lecun.com` 在這台機器被直接拒絕連線。** MNIST 的官方來源掛掉時不必換資料集——`ossci-datasets.s3.amazonaws.com` 這個鏡像可用，而且它是 torchvision 的預設來源，所以 `torchvision.datasets.MNIST(download=True)` 會自動走這條路。

我仍然在程式裡留了 **IDX 手動解析的備援路徑**：直接下載四個 `.gz`、自己解 magic number 與 shape，萬一 torchvision 的下載邏輯被改掉也還能跑。

---

## 模型：指南裡那個結構，一行沒改

```python
class SimpleCNN(nn.Module):
    def __init__(self, num_classes: int = 10, in_channels: int = 1) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_channels, 16, kernel_size=3, padding=1),  # 28x28 -> 28x28
            nn.ReLU(),
            nn.MaxPool2d(2),                                      # 28x28 -> 14x14
            nn.Conv2d(16, 32, kernel_size=3, padding=1),           # 14x14 -> 14x14
            nn.ReLU(),
            nn.MaxPool2d(2),                                      # 14x14 -> 7x7
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, num_classes),
        )
```

參數量只有 **20,490**，但測試集準確率有 **98.47%**。

---

## 讓程式自己驗證尺寸公式

CS231n 的輸出尺寸公式是：

$$W_2 = \left\lfloor \frac{W_1 - F + 2P}{S} \right\rfloor + 1$$

把它寫成函式，然後在訓練開頭把「公式推導」跟「實際算出來的張量形狀」逐層對照：

```python
def conv_out_size(w1: int, f: int, p: int, s: int) -> int:
    """CS231n 卷積輸出尺寸公式：W2 = floor((W1 - F + 2P) / S) + 1。"""
    return (w1 - f + 2 * p) // s + 1
```

實際跑出來的輸出（每次訓練都會重跑一遍）：

```
[shape] CS231n 公式: W2 = floor((W1 - F + 2P) / S) + 1
         Conv1: W1=28, F=3, P=1, S=1  ->  W2=(28-3+2*1)/1+1 = 28
         Pool1: W1=28, F=2, P=0, S=2  ->  W2=(28-2+2*0)/2+1 = 14
         Conv2: W1=14, F=3, P=1, S=1  ->  W2=(14-3+2*1)/1+1 = 14
         Pool2: W1=14, F=2, P=0, S=2  ->  W2=(14-2+2*0)/2+1 = 7
[shape] 公式推導 vs 實際輸出
  ✓ Conv2d      expected=(1, 16, 28, 28)   actual=(1, 16, 28, 28)
  ✓ ReLU        expected=(1, 16, 28, 28)   actual=(1, 16, 28, 28)
  ✓ MaxPool2d   expected=(1, 16, 14, 14)   actual=(1, 16, 14, 14)
  ✓ Conv2d      expected=(1, 32, 14, 14)   actual=(1, 32, 14, 14)
  ✓ ReLU        expected=(1, 32, 14, 14)   actual=(1, 32, 14, 14)
  ✓ MaxPool2d   expected=(1, 32, 7, 7)     actual=(1, 32, 7, 7)
  ✓ Flatten     expected=(1, 1568)         actual=(1, 1568)
  ✓ Linear      expected=(1, 10)           actual=(1, 10)
[shape] 全部層級形狀與公式一致: True
```

這段的價值在於：**一旦你改動 `padding` 或 `stride`，對不上的那一層會立刻跳出來**，而不是訓練跑完才發現 flatten 尺寸接錯。

---

## 訓練結果（Adam, lr=1e-3, batch=64, CPU）

| epoch | loss | train_acc | test_acc | 耗時 |
|---|---|---|---|---|
| 1 | 0.1909 | 0.9427 | 0.9815 | 3.5 s |
| 2 | 0.0590 | 0.9815 | 0.9839 | 3.5 s |
| 3 | 0.0445 | 0.9859 | **0.9847** | 3.6 s |

三個 epoch、**11 秒**、純 CPU。`train_acc` 與 `test_acc` 幾乎同步上升、沒有落差，這個規模下還看不到明顯過擬合；若把 epoch 拉到 50，train 會逼近 1.0 而 test 停在 0.99 左右，那時才需要 Dropout 或資料增強。

---

## 視覺化 ①：模型學到的 16 個 filter

![Conv1 的 16 個 3×3 filter](/img/cnn-mnist-lab/01_conv1_filters.png)

紅色是正權重、藍色是負權重。這些 kernel **不是我們指定的**，是梯度下降自己長出來的，而它們的形狀高度一致地符合直覺：

- **f0、f5、f9**：上下兩排正負相反 → 典型的**水平邊緣偵測器**
- **f2、f10**：對角線分佈 → **斜向邊緣偵測器**
- **f3、f6**：一側強一側弱但中間有過渡 → **定向／帶通型濾波器**

這就是 3Blue1Brown 動畫裡「卷積核可以被學出來」的實證：模型自己發現「偵測邊緣」比「偵測整塊灰階」更有用。

---

## 視覺化 ②：feature map — 同一張圖被拆成多個特徵通道

![第一層 feature map：不同 filter 對同一張手寫數字偵測到不同模式](/img/cnn-mnist-lab/02_conv1_feature_maps.png)

三張輸入（7、2、1）× 8 個 filter 的輸出，讀法是：**看哪裡亮**。

- 對數字 **7**：`f0`、`f1` 幾乎整條筆畫都亮 → 這兩個 filter 是「亮度／粗細」型；`f2` 只有輪廓亮 → 邊緣型；`f6`、`f7` 只有斜的那一筆亮 → 方向型。
- 對數字 **2**：`f4` 幾乎什麼都沒反應，但 `f5` 把曲線的部分點亮 → 兩個 filter 的「偏好」明顯不同。

**這就是「一張影像被拆成多個特徵通道」最直觀的樣子。** 也是為什麼卷積層的輸出通道數（這裡是 16）有意義：它代表模型可以同時追蹤 16 種不同的「看東西的方式」。

---

## 視覺化 ③：第二層特徵更抽象

![第二層 feature map（經 pooling 後再卷積）](/img/cnn-mnist-lab/03_conv2_feature_maps.png)

第二層的特徵圖明顯變得**稀疏且局部**：不是整條筆畫亮，而是只有「橫筆畫的那一段」「轉角那一塊」亮起來。

原因可以用感受野算清楚：

| 層 | 感受野（以輸入像素計） | 累積 stride |
|---|---|---|
| Conv1（k=3, s=1） | 3×3 | 1 |
| Pool1（k=2, s=2） | 4×4 | 2 |
| **Conv2（k=3, s=1）** | **8×8** | 2 |
| Pool2（k=2, s=2） | 10×10 | 4 |

Conv2 的每個輸出神經元看得到輸入的 **8×8 像素**，足以框住一整段筆畫或轉角——所以它學到的已經不是「邊緣」，而是「筆畫片段」。這就是「逐層抽象」在數字上的樣子。

---

## 權重共享：差 1,300 倍

| 層 | 參數量 | 算式 |
|---|---|---|
| Conv1 | 160 | 16 × 1 × 3 × 3 + 16 |
| Conv2 | 4,640 | 32 × 16 × 3 × 3 + 32 |
| Linear | 15,690 | 32 × 7 × 7 × 10 + 10 |
| **合計** | **20,490** | |

若第一層改成「全連接」且不做權重共享，光第一層就要 28 × 28 × 16 × 16 ≈ **20 萬**個參數，是現在的 1,300 倍，而且必然過擬合。

參數量與影像大小無關——這正是卷積相對全連接最根本的優勢。

---

## 七項自我測試

沒有測試的 ML 實作很容易「跑完就算對」，所以我補了 7 項（不需要 pytest，`python tests/test_model.py` 直接跑）：

```text
✓ test_conv_out_size_formula          公式對照 CS231n 標準範例
✓ test_expected_shapes_match_formula_table
✓ test_trace_shapes_matches_expected  公式推導 vs 實際張量（batch=1 與 batch=4）
✓ test_forward_output_shape            (4,1,28,28) → (4,10)
✓ test_weight_sharing_and_param_count  參數量逐層核算 = 20,490
✓ test_gradients_flow                  每層 .grad 存在、非 NaN、非全零
✓ test_receptive_field_growth          Conv2 感受野 = 8×8、最終 stride = 4
```

其中 `test_gradients_flow` 值得特別一提：它確認 **每一層** 的權重都真的收到梯度，這是「梯度消失」在第一層就發生的早期警訊。

寫測試的過程中我自己也踩了三個坑，全部是測試寫錯而不是模型寫錯：

1. 形狀比對的 `zip` 少一格，造成層級錯位（expected 多算了一層 input）
2. 感受野算成 7——**池化層也會增加感受野**（pooling 增加 1 像素跨度），正確值是 8
3. `MaxPool2d(2)` 的 `kernel_size` 是 int 不是 tuple，取 `kernel_size[0]` 會直接 TypeError

---

## 重現方式

專案路徑：`C:\Users\princ\cnn-mnist-lab`

```powershell
cd C:\Users\princ\cnn-mnist-lab

# 自我測試（7 項）
python tests\test_model.py

# 一鍵跑完整流程：訓練 → 評估 → 產生三張視覺化
python run_lab.py --epochs 3

# 單獨執行
python src\data.py                    # 只測資料管線
python src\train.py --epochs 5         # 只訓練
python src\visualize.py               # 只畫圖（讀 checkpoint）
```

檔案結構：

```text
cnn-mnist-lab/
├─ run_lab.py          一鍵流程
├─ src/model.py        SimpleCNN、conv_out_size、receptive_field_table
├─ src/data.py         MNIST 載入（torchvision + IDX 手動解析備援）
├─ src/train.py        訓練迴圈 + 公式/形狀自動比對
├─ src/visualize.py    filter 與 feature map 繪圖（CJK 字型自動偵測）
├─ tests/test_model.py 7 項自我測試
├─ outputs/            PNG 視覺化 + JSON 紀錄
└─ checkpoints/        模型權重
```

---

## 延伸練習（我留給自己的功課）

1. **加 Dropout 與 BatchNorm**（fast.ai Lesson 8 後半段），比較 test_acc 與過擬合曲線
2. **改 padding / stride**：把 `padding=1` 改成 0，看公式對照表會在哪一層報 `✗`——親眼見證公式的作用
3. **三層卷積架構**：Conv → ReLU → Pool ×3，對照 CS231n 的架構圖
4. **混淆矩陣**：印 10×10 矩陣，找出最容易混淆的數字對
5. **遷移學習**：ImageNet 預訓練 ResNet18 在 MNIST 上微調，體會 CNN 學到的特徵可以跨資料集重用

---

## 資源連結

**直覺（第 1、2 站）**

- 3Blue1Brown《But what is a convolution?》（約 15 分鐘）：<https://www.youtube.com/watch?v=KuXjwB4LzSA>
- 3Blue1Brown Neural Networks 系列（4 集，約 1 小時）：<https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi>
- Brandon Rohrer《卷積神經網路的運作原理》（中文翻譯，圖解派）：<https://brohrer.mcknote.com/zh-Hant/how_machine_learning_works/how_convolutional_neural_networks_work.html>

**原理（第 3 站）**

- Stanford CS231n 卷積網路筆記（本文公式出處）：<https://cs231n.github.io/convolutional-networks/>
- Stanford CS231n 課程官網：<https://cs231n.stanford.edu/>

**實作（第 4 站）**

- fast.ai Lesson 8 (CNNs)：<https://course.fast.ai/Lessons/lesson8.html>

**資料集**

- MNIST 官方頁面：<http://yann.lecun.com/exdb/mnist/>（本文實測時連不上，可改用鏡像）
- torchvision 預設鏡像：<https://ossci-datasets.s3.amazonaws.com/mnist/>



