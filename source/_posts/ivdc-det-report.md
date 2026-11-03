---
title: 簡報只有標題是文字：25 頁物件偵測與 CNN 教材的逐頁還原與核對報告
date: 2026-11-04 14:30:00
categories:
  - 學習筆記
  - 電腦視覺
  - 深度學習
tags:
  - IVDC
  - 物件偵測
  - Object Detection
  - CNN
  - TensorFlow
  - PyTorch
  - YOLOv8
  - 勘誤
  - 可重現性
  - Colab
toc: true
index_img: /img/covers/ivdc-det-report.png
banner_img: /img/covers/ivdc-det-report-banner.png
---

![簡報只有標題是文字](/img/covers/ivdc-det-report.png)

> <strong>這篇是什麼</strong>：一份 25 頁課程簡報的<strong>逐頁核對報告</strong>。
> 那份簡報只有大標題是文字層，所有程式碼都是截圖；我先把它還原成 9 支可執行腳本，
> 再逐頁比對我自己寫的筆記，結果<strong>抓到 10 項錯誤</strong>（其中 5 項是我自己文章的錯）。
>
> <strong>為什麼值得公開</strong>：因為錯的都是「看起來很合理」的那種——模型名稱簡寫、
> 學習率預設值、用 loss 曲線證明架構正確、把兩個不同場景的 FPS 相除。
> 這些錯誤不會讓程式掛掉，只會讓結論膨風。
>
> <strong>產出物</strong>：
> 腳本與筆記本 → [kalpakjian/ivdc_handout](https://github.com/kalpakjian/ivdc_handout)
> ｜ 原始筆記 → [同一份課堂材料，用 TensorFlow 與 PyTorch 各跑一遍](/2026/11/03/ivdc-tf-pytorch-object-detection-cnn/)
> ｜ 課程筆記版 → [Lesson 8 物件偵測與 CNN 學習筆記](/ivdc-det-notes/)

## 一、摘要

- <strong>頁碼宣稱全部正確</strong>：第 2、3、5、7、8–17、18–25 頁都對得上。
- <strong>修正 10 項</strong>事實或推論錯誤（見 §三）。
- 被向下捲動箭頭遮住程式碼的是 <strong>7 頁</strong>，不是原本寫的「3 處」。
- TensorFlow 那條線原本宣告「無法驗證」，後來證明可以（`uv run --python 3.11`），已補跑、test accuracy <strong>0.9872</strong>。
- 速度表原本是<strong>跨基準線相除</strong>（webcam 的 FPS ÷ 別張圖的信心），改成同一張影格的單一基準重測後，差距從「34 倍」變成 <strong>25.6 倍</strong>。

## 二、25 頁對照

「↓」＝該頁的程式碼截圖被向下捲動箭頭蓋住。

| 頁 | 標題 | 內容 | 狀態 |
|---|---|---|---|
| 1 | Certificate in Application… | 封面 | 文字層只有封面與各頁大標題 |
| 2 | Tensorflow for Object Detection | SSD MobileNet V2 單張圖 | <strong>↓ 第 16 行以下</strong> |
| 3 | Real Time Webcam Detection | TF webcam 迴圈 | <strong>↓ 第 16 行以下</strong> |
| 4 | Real Time Object Detection | 模型建議（SSD MobileNet V2／EfficientDet／Faster R-CNN／YOLO） | 純文字 |
| 5 | Pytorch for Object Detection | `fasterrcnn_resnet50_fpn(weights="DEFAULT")` | <strong>↓ 第 12 行以下</strong> |
| 6 | Real Time Webcam Detection | torch webcam | <strong>↓ 第 13 行以下</strong> |
| 7 | Yolo (Recommended) | 四行程式 ＋ 模型比較（含 DETR） | 只有 4 行 |
| 8 | Tensorflow for CNN | 匯入 ＋ 印版本 | — |
| 9 | Tensorflow for CNN | 與第 8 頁完全相同 | <strong>重複頁</strong> |
| 10–12 | Load Data | `mnist.load_data()` → 形狀 → `reshape` + `/255.0` | — |
| 13 | CNN | Keras `Sequential` 模型 | — |
| 14 | CNN Model Output | `compile` ＋ `fit(epochs=5, validation_split=0.1)` | — |
| 15 | CNN Model Output | 示範輸出 `0.95 / 0.15` → `0.99 / 0.03` | 標題寫 Example output |
| 16–17 | Classification Result | `predict` ＋ `argmax`、輸出 7/7 | — |
| 18 | Or you could use Pytorch | 匯入 ＋ 印版本 | <strong>↓</strong> |
| 19 | Load Data | `torchvision.datasets.MNIST` | <strong>↓ 第 16 行以下</strong> |
| 20 | Load Data | 預期輸出 60000／10000／`(1, 28, 28)` | — |
| 21 | CNN | `nn.Module` 版 CNN | 底部兩行被裁掉（不是箭頭） |
| 22 | CNN Model Output | `DataLoader` ＋ `CrossEntropyLoss` ＋ `Adam(lr=0.001)` | <strong>↓ 第 16 行以下</strong> |
| 23 | CNN Model Output | 示範輸出 `0.1805` → `0.0225` | 標題寫 Example output |
| 24–25 | Classification Result | torch 版推論、輸出 7/7 | 第 25 頁與第 17 頁同 |

被遮住的共 <strong>7 頁</strong>：第 2、3、5、6、18、19、22。
每一支腳本的 docstring 都寫了它對應哪一頁、從第幾行開始是「補完」——
這樣半年後才分得出哪一段是教材原文、哪一段是我補的。

## 三、勘誤清單

### 3.1 簡報沒說、但一定會踩的（5 項）

| # | 現象 | 正確做法 | 證據 |
|---|---|---|---|
| 1 | `hasattr(cv2, "imshow")` 回 `True`，但呼叫就丟 `(-2:Unspecified error) The function is not implemented` | 要<strong>真的呼叫一次</strong>才驗得出來；`currentUIFramework()` 回空字串是徵兆 | OpenCV 5.0.0 headless 實測，訊息與簡報引用一致 |
| 2 | `cv2.VideoCapture(0)` 開得起來卻是全黑 | 逐個 index 試、量畫面平均亮度 | 實機 camera 0 亮度 2.4／camera 2 亮度 93–110 |
| 3 | `cv2.VideoCapture(0, cv2.CAP_DSHOW)` 在 Linux／macOS <strong>每個 index 都失敗</strong> | 依平台選 backend：`CAP_DSHOW if win32 else CAP_ANY` | Linux 實測 `isOpened()=False` vs `CAP_ANY=True` |
| 4 | 「丟 10 幀暖機」在 30 fps 只有 0.33 秒，自動曝光要 1–2 秒 | 用時間判斷（`while time.time()-t0 < 1.5`） | 兩者差 4–6 倍 |
| 5 | `tensorflow_hub` import 就死：`No module named 'pkg_resources'` | setuptools ≥ 81 已移除 `pkg_resources`；本機要 `pip install 'setuptools<81'` | setuptools 84.0.0 實測；<strong>Colab 是 80.10.2，不需要</strong> |

### 3.2 我自己文章寫錯的（5 項，已全部更正）

| # | 原本寫 | 正確 | 怎麼發現 |
|---|---|---|---|
| 6 | `optimizer='adam'` 與 `optim.Adam(lr=1e-3)`<strong>「預設學習率不同」</strong> | 兩邊預設<strong>都是 1e-3</strong> | 讀 API：Keras 3.15.1 = 0.001、torch = 0.001 |
| 7 | 表格用 `fasterrcnn_resnet50`／`fasterrcnn_mobilenet` 等簡寫 | torchvision 只有 `fasterrcnn_resnet50_fpn`、`fasterrcnn_mobilenet_v3_large_fpn`、`..._320_fpn`、`ssdlite320_mobilenet_v3_large`，簡寫會 `AttributeError` | 讀 `torchvision.models.detection.faster_rcnn.__all__` |
| 8 | 「實測結果幾乎吻合」（TF 段） | 當時<strong>根本沒跑</strong>；補跑後 test accuracy <strong>0.9872</strong> | `uv run --python 3.11 --with tensorflow-cpu` 實跑 |
| 9 | 「loss 幾乎逐位吻合，<strong>證明架構還原正確</strong>」 | loss 受初始化影響，不能當證據；硬證據是<strong>參數量 225,034</strong>（兩框架一致） | 兩邊 `count_params()`／`numel()` 實測 |
| 10 | 「實測差距 <strong>34 倍</strong>」（`37.4 ÷ 1.1`） | <strong>25.6 倍</strong>（1.4 → 35.8 FPS，同一張影格）；34 是跨基準線相除 | 同場景重測（見 §四） |

還有兩處說法要修：

- 「硬猜成 `toilet` 或 <strong>`truck`</strong>」→ 實測是 `toilet` 或 <strong>`refrigerator`</strong>，`truck` 從沒出現。
- 「<strong>記 YOLO</strong>，因為速度與準確度天花板最好」→ 理由其實是<strong>四行程式碼</strong>。
  `ssdlite320` 在 `bus.jpg` 上信心反而更高（`person 0.989`／`bus 0.985` vs `0.866`／`0.873`），
  速度也幾乎相同（33.1 vs 35.8 FPS）。把「好用」講成「最準」是不誠實的。

第 6 到第 9 項有一個共同點：<strong>它們都不是跑不動的錯，是不會被抓到的錯</strong>。
`**` 那類排版錯 CI 會紅，但「兩個預設值其實一樣」不會有人幫你檢查。

## 四、實測數據（同一張 1280×720 實機影格）

Linux／CPU、門檻 0.5、單張推論；畫面是洗衣機——正好是「不在 COCO 80 類別裡」的那種場景。

| 模型 | 延遲 | 速度 | 最高信心 | ≥0.5 檢出 | 猜成什麼 |
|---|---|---|---|---|---|
| `fasterrcnn_resnet50_fpn`（簡報原版） | 731 ms | <strong>1.4 FPS</strong> | 0.584 | 1 | `toilet` |
| `fasterrcnn_resnet50_fpn` ＋ `min_size=400` | 266 ms | 3.8 FPS | 0.494 | 0 | — |
| `fasterrcnn_mobilenet_v3_large_fpn` | 137 ms | 7.3 FPS | <strong>0.697</strong> | 2 | `toilet`、`refrigerator` |
| `fasterrcnn_mobilenet_v3_large_320_fpn` | 29 ms | 34.6 FPS | 0.464 | <strong>0</strong> | — |
| `ssdlite320_mobilenet_v3_large` | 30 ms | 33.1 FPS | 0.561 | 1 | `refrigerator` |
| `yolov8n` 640 | 28 ms | 35.8 FPS | 0.404 | <strong>0</strong> | `refrigerator` |
| `yolov8n` 960 | 36 ms | 27.5 FPS | 0.253 | <strong>0</strong> | `refrigerator` |
| `yolov8n` 1280 | 33 ms | 30.0 FPS | 0.394 | <strong>0</strong> | `toilet` |

三個結論：

1. <strong>最快的模型一個東西都沒偵測到</strong>——「快」跟「有用」是兩件事。
2. <strong>這一幕沒有模型答對</strong>，因為洗衣機不在 COCO 類別裡，只能硬猜。
3. <strong>`min_size=400` 換來 2.7 倍</strong>（731→266 ms），而此場景本來就沒有真陽性可掉，是純賺。

換到有答案的 `bus.jpg`（YOLOv8n，同一台機器）：

| `imgsz` | 延遲 | 速度 | ≥0.5 檢出 | 內容 |
|---|---|---|---|---|
| 640 | 27.6 ms | 36.2 FPS | 4 | `bus 0.873` ＋ `person 0.866 / 0.853 / 0.825` |
| 960 | 29.6 ms | 33.8 FPS | 4 | 同樣四個，`person 0.886` 最高 |
| 1280 | 41.8 ms | 23.9 FPS | 6 | 多出 `bus 0.690 / 0.634 / 0.542` <strong>三個重複框</strong> |

> 解析度拉高、檢出變多要打折看：1280 多出來的是<strong>同一台公車被框三次</strong>，
> 外加一個 0.289 的 `skateboard`。NMS 救不回重疊框。

這張表可以用 repo 裡的 `bench/bench_detection.py` 原樣重跑：

```bash
python bench/bench_detection.py --camera 0 --yolo      # 現場抓一張 1280×720 再跑
python bench/bench_detection.py --frame frame.jpg --yolo
```

## 五、環境矩陣

同一份程式碼在三個地方跑過或將要跑，差別在版本：

| 項目 | 本機（Linux，量測基準） | Colab 2026.10（同版本重現） | 原作者 Windows（舊數字） |
|---|---|---|---|
| Python | 3.14.8／3.11／3.13 | 3.13.18 | 3.15.1 |
| torch / torchvision | 2.15.0+cpu / 0.29.2+cpu | <strong>2.11.0+cpu / 0.26.0+cpu</strong> | 2.14.1+cpu / 0.29.1+cpu |
| TensorFlow / hub | 2.21.0 / 0.16.1 | 2.21.0 / 0.16.1（皆預裝） | 未安裝（原宣告裝不上） |
| setuptools | 84（<strong>需 &lt; 81</strong>） | <strong>80.10.2（不需降版）</strong> | — |
| OpenCV | 5.0.0（headless） | 5.0.0.93 | 5.0.0 |
| ultralytics | 8.4.201 | 需 `%pip install`（未預裝） | 8.x |
| webcam / GUI | 有相機、無 GUI | <strong>皆無</strong> → 用 `--video` | 有 |

<strong>Colab 的版本是我從 `googlecolab/backend-info` 的 pip-freeze 抄下來鎖的</strong>，
不是「應該差不多」。9 支腳本在本機與 Colab 同版本兩套環境都完整跑過。

## 六、在 Colab 上跑（沒有 webcam 怎麼辦）

Colab 是「無螢幕、無相機、Linux、已預裝大半套件」的環境。實測後的三條規則：

1. <strong>沒有 webcam</strong> → `02`／`04` 加 `--video clip.mp4`，用影片取代攝影機，其餘流程一行不改。
2. <strong>用 `%run`，不要用 `!python`</strong> → `!python` 走 shell 的 PATH，可能指到另一顆直譯器
   （我實測踩到：notebook kernel 是 3.13，`!python` 卻用了系統 3.14，於是 `No module named 'cv2'`）。
3. <strong>`setuptools` 不用降版</strong>（Colab 是 80.10.2）。唯一要補裝的是 `ultralytics`。

沒有相機又要示範「即時偵測」時，用一張圖合成一段影片就好：

```python
import cv2
img = cv2.imread("bus.jpg")
w = cv2.VideoWriter("clip.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 15.0, (img.shape[1], img.shape[0]))
for _ in range(30):
    w.write(img)
w.release()
```

筆記本（用 Colab 開，完全自包含、不需要 clone）：

- [ivdc_exam_all_in_one.ipynb](https://colab.research.google.com/github/kalpakjian/ivdc_handout/blob/main/colab/ivdc_exam_all_in_one.ipynb)
  —— 9 支腳本用 `%%writefile` 內嵌
- [ivdc_exam_quickstart.ipynb](https://colab.research.google.com/github/kalpakjian/ivdc_handout/blob/main/colab/ivdc_exam_quickstart.ipynb)
  —— `git clone` 版

| 症狀 | 解法 |
|---|---|
| `cv2.error ... not implemented ... GTK+` | 不要 `imshow`；用 `--no-show`，圖以 `display(Image(...))` 呈現 |
| `[錯誤] 找不到有畫面的攝影機` | Colab 沒相機 → `--video clip.mp4` |
| `No module named 'ultralytics'` | `%pip install -q ultralytics` |
| `No module named 'cv2'` 且用了 `!python` | 改成 `%run` |
| TF 印 `CUDA Runtime error ... GPU will not be used` | CPU runtime 的正常 stub，不影響結果 |
| Runtime disconnected | `Runtime → Run all`（全部重跑 &lt; 2 分鐘） |

## 七、我怎麼確認這份報告本身沒有再錯一次

被上一次的經驗嚇到，這次每個結論都配一個可重跑的檢查：

| 項目 | 方法 | 結果 |
|---|---|---|
| 9 支腳本語法 | `python -m py_compile` | 全通過 |
| 腳本行為 | 實機 webcam／影片／圖片逐支執行 | 全通過 |
| 簡報頁碼 | 25 頁逐頁渲染成 PNG 後人工比對 | 7 頁遮擋、2 處重複頁、1 處裁切 |
| notebook（clone 版） | nbclient + ipykernel，Colab 同版本 | 23 格、<strong>0 錯誤</strong> |
| notebook（自包含版） | 同上，<strong>從空目錄</strong>（無 git、無 repo） | 43 格、<strong>0 錯誤</strong>；`%%writefile` 產物與 repo <strong>md5 一致</strong> |
| 站內連結 | `tools/notes-qa/check_public_links.py` | 649 頁／19,684 連結、<strong>0 broken</strong> |
| 中文粗體 | `tools/notes-qa/check_cjk_bold.js` | 0 受影響 |

## 八、還沒驗的（誠實標記）

1. <strong>Windows 專屬路徑</strong>：`CAP_DSHOW` vs `CAP_MSMF` 的實際行為，以及作者機器的原始 1.1 FPS。
   這台是 Linux，量不到；不影響任何結論，只是平台註記。
2. <strong>Colab GPU runtime</strong>：上面的 Colab 驗證是在 CPU 版同版本環境做的。
   T4／L4 上 `torch.cuda.is_available()` 應為 `True`（`07` 支援 `--device cuda`），未實測。
3. <strong>講師口述內容</strong>不在比對範圍——我只核對能從 PDF 讀到的東西。

## 九、重跑

```bash
git clone https://github.com/kalpakjian/ivdc_handout && cd ivdc_handout
python src/00_check_env.py                                    # 先自檢
python src/03_torch_object_detection_image.py --image bus.jpg --model ssdlite320
python src/04_torch_webcam_detection.py --video clip.mp4      # 沒有相機時
python bench/bench_detection.py --camera 0 --yolo             # 重跑 §四 那張表
```

TensorFlow 線若在自己電腦被 setuptools 卡住：

```bash
uv run --no-project --python 3.11 --with tensorflow-cpu \
    --with tensorflow-hub --with 'setuptools<81' -- python src/06_tf_cnn_mnist.py
```

---

<strong>一句話總結</strong>：這次真正的收穫不是「把截圖變成程式碼」，
而是發現<strong>「有跑」跟「有驗」是兩件事</strong>——9 支腳本都跑得動，
但裡面有 5 個宣稱是我自己寫錯的，而且每一個看起來都很合理。
把檢查方式一起寫出來，是唯一能讓下一個人不用重踩的方法。

> 完整報告、腳本、兩本筆記本：[kalpakjian/ivdc_handout](https://github.com/kalpakjian/ivdc_handout)
> （MIT；課程簡報著作權屬匯縱專業發展中心，repo 不含簡報原檔。）
