---
title: Rive 無頭渲染三條路線實測：官方 CLI、Playwright + WASM、自寫 C++ CPU renderer
date: 2026-10-22 20:00:00
categories:
  - 軟體工程
tags:
  - Rive
  - 動畫
  - 無頭渲染
  - Headless
  - WebAssembly
  - Playwright
  - C++
  - MSVC
  - Windows
  - 實測
index_img: /img/covers/rive-headless-three-routes.png
banner_img: /img/covers/rive-headless-three-routes.png
---

![Rive 無頭渲染三條路線實測](/img/covers/rive-headless-three-routes.png)

> 這篇是一次**橫向實測**：同一個目標——把 `.riv` 動畫在沒有視窗、沒有人盯著的環境裡算成一張圖片——
> 用三條完全不同的技術路線各做一遍，把量到的數字攤開來比。
>
> 起因是一篇 2023 年的舊文〈新一代跨平台、高效能動畫庫 - Rive〉。那篇把 Rive 的效能與狀態機講得很清楚，
> 但沒有回答兩個實務問題：**免費版與付費版到底差在哪**、**有沒有無頭（headless）的用法**。
>
> 我把兩個問題都實測完，還把 Rive 官方的 **C++ runtime 在本機編起來**：先自己寫了一個 CPU 光柵化 renderer，
> 再把官方的 GPU renderer 接到**離屏 texture** 上。三條路線都跑通、都有數據——最後那條的輸出與
> 官方 CLI 自己截的圖**位元完全相同**。
>
> 過程中包含我自己的**三次誤判**（第七、八節），以及官方文件那條路（Skia thumbnail generator）為什麼在 Windows 上根本跑不起來。

<!-- more -->

## 一、結論先講：三條路線、四條路徑

| | 路線 1：官方 CLI | 路線 2：官方 WASM + Playwright | 路線 3：C++ runtime（兩種實作，見下） |
|---|---|---|---|
| 一句話 | `rive --screenshot` | 在 headless Chrome 裡跑官方 runtime | 編 `rive.lib`，自己實作 `rive::Renderer` |
| 能渲染什麼 | **RML 專案**（或 `.rev` 轉出的專案） | **任意 `.riv`** | **任意 `.riv`** |
| 畫質 | 官方 GPU renderer，**與線上一致** | 官方 runtime，**與線上一致** | 自寫 CPU：**無反鋸齒、無圖片**；官方 GPU 離屏：**與線上一致** |
| 需要帳號 | **不用**（`--screenshot` 免登入） | 不用 | 不用 |
| 需要 GPU | 不用（但仍走官方 renderer） | 不用（瀏覽器可軟體算） | 完全不用 |
| 建置成本 | 一行安裝 | `npm i playwright-core @rive-app/canvas-advanced` | **MSVC + 1.25 GB `rive.lib` + 自己寫 800 行** |
| 適用 | CI 截圖、回歸、效能 | 任意素材、與線上一致 | 伺服器端／嵌入自有引擎 |

**我的建議**：預設走路線 1；要處理「別人給的 `.riv`」走路線 2；只有當你要**把 Rive 塞進自己的 C++ 產品**、
或需要在沒有瀏覽器的伺服器上算圖，才值得付出路線 3 的代價——**而且要選 3b（官方 GPU renderer 離屏），不是 3a**。

路線 3 的兩種實作差別很大，先講清楚：

| | 路線 3a：自寫 CPU renderer | 路線 3b：官方 GPU renderer + 離屏 texture |
|---|---|---|
| 畫質 | 自寫掃描線光柵器，**無反鋸齒** | 與線上完全一致（**反鋸齒、圖片、mesh、漸層都支援**） |
| 需要 GPU | **完全不用** | 需要（沒有可用 GPU 時自動退回 WARP 軟體算） |
| 建置成本 | 只要 `rive.lib` + 約 800 行自寫程式 | 還要 `rive_pls_renderer`（含 shader 產生步驟） |
| 驗證方式 | 顏色與幾何精確命中作者定義值 | 與官方 CLI 的截圖 **100% 像素相同** |
| 適合 | 理解原理、完全沒有 GPU 的環境 | **生產環境** |

<div style="max-width:640px;margin:1.6rem auto">
<img src="/img/rive-headless-three-routes/ch01-three-routes.jpg" alt="三條不同質地的光路從一點分岔，各自通往遠方" style="width:100%;border-radius:14px">
</div>

> 圖：本機 ComfyUI 的 Qwen-Image 2.1 生成（本站 house style，無文字）。

## 二、前置事實：Free 與付費到底差在哪

2023 那篇的時代，「編輯器要付費」是對的。但 **Rive 在 2025/10/20 改過一次計費方式**，
現在的分界線跟直覺不一樣：**編輯器完全免費，匯出也免費——代價是匯出的檔案執行時會播一段 Rive 的 splash 畫面。**

| | Free | Cadet | Voyager | Enterprise |
|---|---|---|---|---|
| 價格 | $0 | **$9/seat/月**（年繳；月繳 $17） | **$32/seat/月**（年繳；月繳 $39） | **$120/seat/月**（年繳） |
| 席次 | — | 3 席上限 | 25 席上限 | 無（$10M+ 年營收） |
| 匯出 | **可用，但帶 splash** | **不帶 splash** | 同 Cadet | 同 Voyager |
| 檔案 | 3 個協作檔案、1 個 project | 無限 | 無限 | 無限 |
| 素材上限 | 10 MB／檔 | 100 MB／檔 | 100 MB／檔 | 100 MB／檔 |
| 加值 | — | — | Libraries、CDN 託管、Embed 連結 | SSO、SOC2、自備 S3、專屬支援 |

三件容易誤解的事：

1. **沒有 runtime fee、沒有抽成**，runtime 是 MIT 開源，**已匯出的檔案永久可用**（`.riv` 不會回連伺服器）。
2. 付費牆只影響**新的匯出**，不影響**已經在跑的產品**。
3. **開發與測試永遠免費**：CLI 的 `--verify`、`--test`、`--screenshot`、`--bench` 全部免登入、可離線。
   只有 `--publish`（要簽章給 web 用的 `.riv`）才需要登入，而且未綁定 Cadet 以上工作區會被加浮水印。

> 一句話：**「免費版不能做事」是舊資訊；現在是「免費版可以做完，只是成品上會掛一張 Rive 的招牌」。**

<div style="max-width:640px;margin:1.6rem auto">
<img src="/img/rive-headless-three-routes/ch02-free-vs-paid.jpg" alt="一道半透明的光牆立在暗處，牆後的空間暢通無阻" style="width:100%;border-radius:14px">
</div>

> 圖：本機 ComfyUI 的 Qwen-Image 2.1 生成（本站 house style，無文字）。


## 三、路線 1：官方 Rive CLI（最實用，而且免費）

Rive 現在的 CLI 本身就是 headless-first：

```powershell
# Windows
irm https://releases.rive.app/cli/install.ps1 | iex
# macOS / Linux
curl -fsSL https://releases.rive.app/cli/install.sh | sh
```

> **實測踩到**：這台機器的 Windows PowerShell 5.1 **沒有 `Get-FileHash`**（模組被裁過），
> 官方安裝腳本會在下載完成後直接掛掉。我最後照腳本邏輯手動完成（下載 → 比對 SHA-256 → 解壓 → 寫入 PATH），
> 驗證值 `78da56a3…1efe1` 與官方 manifest 一致。**裝完請跑 `rive doctor`**。

### 三個真正有用的模式

```powershell
rive create myproject            # 產生 RML 專案（rive.yaml + scene.rml + AGENTS.md）
cd myproject
rive . --verify --format=json    # 只編譯不寫檔，CI 用
rive . --once                    # 產出未簽章 .riv
rive . --screenshot=build/out.png --advance=1s --viewport=390x844
rive . --bench=120               # 無視窗計時 120 帧 + WASM 記憶體成長
```

實測輸出：

```
{"success": true, "command": "verify", "data": {"riv": null, "bytes": 0, "buildMs": 15.7, "problems": []}, ...}
built build/cli-demo.riv (228 bytes, 14ms, 0 errors, 0 warnings)
bench advance: mean 0.001ms p50 0.001ms p95 0.002ms max 0.008ms
bench render:  mean 0.151ms p50 0.143ms p95 0.198ms max 0.365ms
bench memory:  0 -> 0 wasm pages (+0) over 120 frames
```

真實素材（官方範例 `hello_rive`，含 Luau 腳本 + WGSL shader）在 1 秒與 2 秒的 PNG **hash 不同**，
證明 `--advance` 真的在推進時間軸，不是只拍一張靜止畫面。

### 三個一定要知道的坑

1. **`--screenshot` 的路徑是相對於「當前目錄」**，不是專案目錄，而且**資料夾必須先存在**。
2. **不加 `--advance` 拍到的是靜止 pose**，不是動畫第一帧（state machine 還沒跑過）。
3. **整個專案資料夾的所有 `.rml` 會合併編譯成「一份文件」**。我把範例複製到自己裡面，變成
   `keyboard-menu\keyboard_menu\scene.rml`，同一份場景被編兩次 → `--verify` 回 **exit 1** 並指出 47 個
   `duplicate id "0:2"`。移除巢狀副本立刻恢復 `problems: []`。
   ——這也是 `--verify` 最有價值的用法：**結構性錯誤在 CI 就擋下來，訊息精確到行號。**

另外 `tests_demo` 範例故意含一條失敗測試，`rive . --test --format=json` 會回 **exit 6**
（`passed: 6, failed: 1`），CI 可以直接依退出碼分支，不必解析輸出。

## 四、路線 2：官方 WASM + Playwright（渲染任意 `.riv`）

Rive 的 JS runtime 有兩層 API，低階 API 的簽名是：

```ts
makeRenderer(canvas: HTMLCanvasElement | OffscreenCanvas, useOffscreenRenderer?: boolean): WrappedRenderer;
```

**它只吃 canvas 物件——官方沒有提供純 Node 的 renderer。** 所以「在 Node 裡 headless」實務上等於
「Node 驅動 headless 瀏覽器」，用你已經裝好的 Chrome 就好，不必下載額外瀏覽器：

```powershell
npm i playwright-core @rive-app/canvas-advanced
node render-headless.mjs out.png                            # DOM canvas 版
node render-headless.mjs out-offscreen.png offscreen.html   # Worker + OffscreenCanvas 版
```

腳本做的事：起一個只綁 `127.0.0.1` 的靜態 server → `chromium.launch({ channel: 'chrome', headless: true })`
→ 在頁面裡載入官方 runtime、`makeRenderer(canvas)`、自己跑 render loop → 把 `toDataURL()` 交回 Node 存檔。

實測（`vehicles.riv`，artboard `Jeep`）：

```
scene info: {"artboards":["Truck","Jeep"],"artboard":"Jeep","stateMachines":1,
             "animations":8,"bounds":{"minX":0,"minY":0,"maxX":1000,"maxY":1000}}
wrote vehicles-jeep.png (6892 bytes, png signature=true)
```

兩個版本（頁面上有 `<canvas>` vs 頁面上完全沒有 `<canvas>`、改用 Worker 裡的 `OffscreenCanvas`）
**SHA-256 完全相同**——代表「無畫面」那條路徑跟 DOM 路徑輸出一致。

> **實測踩到**：emscripten 的 glue code 會去要 `canvas_advanced.wasm`，但 npm 套件裡的檔名是 `rive.wasm`。
> 不處理就會得到 `both async and sync fetching of the wasm failed`。解法是 `locateFile` 把任何 `.wasm` 導到 `./rive.wasm`。

<div style="max-width:860px;margin:1.6rem 0">
<img src="/img/rive-headless-three-routes/runtime-compare.png" alt="同一份 vehicles.riv：左為官方 WASM runtime 渲染，右為自寫 CPU renderer（無圖片）" style="width:100%;border-radius:14px">
</div>

> 圖：同一份 `vehicles.riv`（artboard `Jeep`）。左邊是官方 WASM runtime（Playwright 驅動，含貼圖），
> 右邊是我自己寫的 CPU renderer —— 看得出來它只畫得出向量部分。

## 五、路線 3a：C++ runtime + 自寫 CPU renderer

### 5.1 先說壞消息：官方文件寫的那條路，在 Windows 上跑不起來

官方文件（C++ / External Renderer）指的現成範例是 `skia/thumbnail_generator`。它**無法在這台機器上執行**，
而且不是「有點難」，是**第一個 `source` 指令就會失敗**：

| 阻礙 | 證據 |
|---|---|
| `build.sh` 連啟動都不行 | 它會 `source dependencies/config_directories.sh`，而那個腳本的 `case "$(uname -s)"` **只認 `Linux*` 與 `Darwin*`**；Git Bash 得到 `unhandled:MINGW64_NT-10.0-26220`，接著去 source 一個**不存在的目錄**（`dependencies/` 只有 `linux/`、`macosx/`、`windows/`） |
| 它要**從原始碼編 Skia** | `make_skia_recorder.sh` 跑 `bin/gn gen out/static` + `ninja -C out/static`，還要 `python tools/git-sync-deps`（數 GB） |
| 公開快取不存在 | 我照 `cache_helper.sh` 的邏輯算出 hash（`cf099f31…`）後探測 `cdn.rive.app/archives/…`，**所有平台（含 Rive 自己的 `Darwin_arm64`）全部 403**；而同一網域對已知檔案回 200，所以 403 就是「不存在」 |
| 工具鏈缺 | 沒裝 `clang-cl`（premake 預設 toolset 是 ClangCL，直接 `error MSB8020`），也沒有 `gn` / `ninja` |

### 5.2 改成：MSVC 編 core，自己實作 External Renderer

好消息是 **C++ runtime 的核心本身是渲染器無關的**。它只要求你實作兩個介面：`rive::Renderer` 與 `rive::Factory`。
所以我把 core 編出來，然後自己寫了一個**零外部依賴**的 CPU renderer：

```
rive-runtime/tests/out/release/
    rive.lib            1,249 MB   ← core runtime（MSVC v143、/MT、LTO）
    rive_harfbuzz.lib     211 MB
    rive_yoga.lib          10 MB
    rive_sheenbidi.lib    0.3 MB
    miniaudio.lib         2.8 MB
app/rive_cpu_render.exe     2.4 MB  ← 自寫 renderer（約 800 行）
```

`main.cpp` 手寫了整個後端：`MyRenderer`（save/restore、`ctm = ctm * mat`、`clipPath`、`drawPath`、`modulateOpacity`）、
`MyFactory` / `MyPath` / `MyPaint` / `MyBuffer` / `MyShader`，加上**掃描線光柵器**（nonZero / evenOdd winding、
以像素中心取樣）、線性／徑向漸層、BMP 輸出。慣例不是猜的——全部對照 repo 內自己的參考實作
`utils/svg_renderer.cpp` 與 `utils/no_op_factory.cpp`。

用法：`rive_cpu_render <in.riv> <out.bmp> [w] [h] [seconds] [fps]`

```
before advancing: watermark pre-roll none
artboard bounds: 1920 x 1080 -> canvas 500 x 500
advanced 60 frames @ 60 fps (1.00 s)
draw calls: fills=36 strokes=5 clips=1 images=0 meshes=0
wrote f-jeep.bmp
```

<div style="max-width:860px;margin:1.6rem 0">
<img src="/img/rive-headless-three-routes/cpu-vs-cli.png" alt="同一場景同一時間：左為自寫 CPU renderer，右為官方 CLI 的 GPU renderer" style="width:100%;border-radius:14px">
</div>

> 圖：同一個場景（`rml_triangle`）、同一個時間點（0.5 秒）。左邊是自寫 CPU renderer（硬邊、無反鋸齒），
> 右邊是官方 CLI 的 GPU renderer。差異集中在邊緣與文字，幾何與顏色是對的。

<div style="max-width:640px;margin:1.6rem auto">
<img src="/img/rive-headless-three-routes/ch05-cpp-engine.jpg" alt="精密機械從一側射入細光束，另一側射出整齊的平行光束" style="width:100%;border-radius:14px">
</div>

> 圖：本機 ComfyUI 的 Qwen-Image 2.1 生成（本站 house style，無文字）。

## 六、真正卡住的六個坑

這一節是整篇最有用的部分——**路線 3 的難度不在寫 renderer，而在讓官方那套建置流程在 Windows 上跑起來**。

| 症狀 | 原因 | 解法 |
|---|---|---|
| `error MSB8020: 找不到 ClangCL 的生成工具` | premake 在 Windows 預設用 clang | `build_rive.sh release --toolset=msc` |
| premake 產生階段說 `make` 不是命令 | `premake5_pls_renderer.lua` 會在**產生階段**烘焙 PLS shader 標頭 | 放一個 no-op 的 `make.bat` shim。我先 grep 確認 `src/` **完全沒有**引用 `generated/shaders`，所以只有 `rive_pls_renderer` 需要那些檔 |
| **720 個** `error C2220: 警告被視為錯誤` | 這台機器系統代碼頁是 **936**，MSVC 對每個 UTF-8 檔吐 `C4819`，而專案開了 `fatalwarnings{All}` | 統計後發現 **C4819 是唯一出現的警告碼**（26,290 次、沒有其他），所以在 6 個 premake 檔加 `disablewarnings({ '4819' })` |
| `error C1083: 無法開啟來源檔案 "Files/Git/wd4819"` | **MSYS 會把以 `/` 開頭的環境變數值當路徑轉換**：`CL=/wd4819` 變成 `C:\Program Files\Git\wd4819` | 不要用 `CL` 環境變數，改用 premake 的 `disablewarnings` |
| 背景建置在 `vcvars64.bat` 之後就死 | 在沒有主控台的分離行程裡 `call` vcvars 會終止批次檔 | 完全不用 vcvars：MSBuild 自己會找 toolset，`cl.exe` 改用明確的 `INCLUDE` / `LIB` |
| 執行時 `0xC0000374`（heap corruption） | app 編譯時**沒帶 rive 的 defines**。`WITH_RIVE_TOOLS`、`RIVE_CANVAS`、`NDEBUG`、`_HAS_EXCEPTIONS=0` 會**增減 rive 自己標頭裡的成員**，於是 lib 與我的翻譯單元對同一個類別的佈局不一致 | 完全照 `rive.vcxproj` 的 define 集編譯，並對齊 `/GR-` 與「不使用 `/EHsc`」 |

> 這六個坑的共同形狀是：**症狀離原因很遠**。「找不到 make」的根因是「產生階段要烘焙 shader」；
> 「heap corruption」的根因是「少了一個前置定義」。這一類問題靠讀錯誤訊息解不開，要靠**回頭讀腳本與標頭**。

<div style="max-width:640px;margin:1.6rem auto">
<img src="/img/rive-headless-three-routes/ch06-pitfalls.jpg" alt="俯視的暗色迷宮，幾條橘色絆索橫在通道上，一個亮點已安全通過" style="width:100%;border-radius:14px">
</div>

> 圖：本機 ComfyUI 的 Qwen-Image 2.1 生成（本站 house style，無文字）。

## 七、驗證：量出來的數字，以及兩次誤判

「跑完沒報錯」不等於「畫對」。所以我用**顏色與幾何**去對：場景 `rml_triangle` 在 RML 裡就寫明了
背景 `#1D1D1D`、三角形 `#57A5E0`、標籤 `#E0E0E0`，而且三角形有一段「2 秒轉一圈」的 Spin 動畫。

量**三角形色塊的質心**（自寫 renderer 的輸出）：

| 請求時間 | 幀數 | 質心 | 對應角度 |
|---|---|---|---|
| 0.017 s | 1 | (249.5, 282.8) | 0° |
| 0.25 s | 15 | (227.2, 274.3) | 45° |
| 0.50 s | 30 | (216.2, 251.2) | 90° |
| 1.00 s | 60 | (247.8, 216.2) | 180° |
| 1.50 s | 90 | (282.8, 247.8) | 270° |
| 2.00 s | 120 | (251.2, 282.8) | 360°（回到原點） |

<div style="max-width:860px;margin:1.6rem 0">
<img src="/img/rive-headless-three-routes/rotation.png" alt="同一場景在 0/45/90/180/270/360 度六個時間點的渲染結果" style="width:100%;border-radius:14px">
</div>

> 圖：自寫 CPU renderer 在六個時間點的輸出。每 0.5 秒精準轉 90°，2 秒回到原點——與 RML 裡
> 「120 帧 @60fps、0 → 2π」的定義完全吻合。

顏色是**精確命中**（沒有反鋸齒，所以不會有中間色）：背景 `#1D1D1D` ×227,392 px、
三角形 `#57A5E0` ×21,999 px、標籤 `#E0E0E0` ×609 px 落在 bbox `x[72..377] y[418..451]`——
而 RML 把標籤放在 `x=70 y=410 w=360 h=60`。也就是說**文字是以向量字形外框畫出來的，位置完全正確**。

四個不同素材的實測結果：

| `.riv` | 結果 |
|---|---|
| `cli-demo.riv` | 250,000/250,000 px 精確 `#282828` |
| `rml_triangle.riv` | 旋轉與顏色如上 |
| `hello_rive.riv`（Luau 腳本 + WGSL shader） | exit 0，`fills=1 clips=1` |
| `vehicles.riv` artboard `Jeep`（1920×1080 → 500×500） | exit 0，`fills=36 strokes=5 clips=1` |

### 兩次誤判，都是「量錯指標」

**第一次：我以為動畫凍結了。** 我拿「三角形像素總數」當指標，看到 22000 / 21999 / 21999 幾乎不變，
就下結論「時間沒有推進」，還去追 `Watermark` 與 `deterministicMode`。
——但**旋轉不會改變面積**。改用 bbox 與質心之後，回頭驗證最早那批檔案，證明**第一次編譯的版本就已經在動**。
指標選錯，會讓你把「正確」判成「壞掉」，然後去修一個不存在的 bug。

**第二次：我以為只有藍色通道有值。** 分析器讀到 `#1D1D1D` 變成 `#00001D`，看起來像渲染器壞了。
真相是 **PowerShell 的 `-shl` 對 `[byte]` 會在 8 位內截斷**：`0x1D -shl 8 = 0`，
所以我自己的分析腳本把 R 與 G 通道吃掉了。渲染器從頭到尾都是對的。

> 這兩個誤判比任何成功都值得寫下來：**當「驗證工具」比「被驗證的東西」更容易出錯時，先懷疑工具。**

<div style="max-width:640px;margin:1.6rem auto">
<img src="/img/rive-headless-three-routes/ch07-verification.jpg" alt="暗色校準網格上有同心靶環與卡尺，一個亮點正好落在環心" style="width:100%;border-radius:14px">
</div>

> 圖：本機 ComfyUI 的 Qwen-Image 2.1 生成（本站 house style，無文字）。

## 八、路線 3b：把 D3D11 離屏也打通

自寫 renderer 只是權宜之計。真正的答案是：**用官方自己的 GPU renderer，但渲染到離屏 texture**。

**卡點**：`rive_pls_renderer` 需要一組在**產生階段**烘焙出來的 shader 標頭，官方用 `make` 做這件事，
而 Windows 上沒有 make（也沒有 POSIX shell）。我照 `renderer/src/shaders/Makefile` 的兩條 recipe
（`minify.py` 產 `.hpp`、`fxc` 產 D3D 標頭）用 Python 重寫成一個 `make` shim。

> 順帶發現：官方那條 make 在 Windows 上其實也編不過。`render_atlas.glsl` 的 `main()`
> **只在 `ATLAS_FEATHERED_FILL` / `ATLAS_FEATHERED_STROKE` 之下存在**，所以 Makefile 的通用
> `%.frag.h` 規則會讓 `fxc` 靜默失敗（exit 1、沒有訊息、也不產檔）。renderer 實際 include 的是
> 兩個 ATLAS 變體，所以我略過那一個輸出。

**接線全部照 repo 自己的參考實作**，不是猜的：

| 步驟 | 參考來源 |
|---|---|
| D3D11 裝置 + `MakeContext` + `flush` | `renderer/path_fiddle/fiddle_context_d3d.cpp` |
| 離屏 render target | `tests/common/offscreen_rendertarget_d3d.cpp` |
| texture readback | `FiddleContextD3DPLS::end()` |
| PNG 輸出 | `tests/common/write_png_file.cpp` |

<div style="max-width:860px;margin:1.6rem 0">
<img src="/img/rive-headless-three-routes/gpu-offscreen.png" alt="左：自寫 CPU renderer（硬邊）；中：官方 GPU renderer 離屏（反鋸齒）；右：同一路徑渲染含貼圖的 vehicles.riv" style="width:100%;border-radius:14px">
</div>

> 圖：左為自寫 CPU renderer（3 種顏色、硬邊）、中為官方 GPU renderer 的離屏輸出（540 種顏色，反鋸齒）、
> 右為同一條 GPU 路徑渲染 `vehicles.riv`（2116 種顏色，**含貼圖**）。

**驗證**：把離屏輸出與**官方 CLI 自己截的同一張圖**做像素比對 ——

```
identical pixels  : 250000 / 250000  (100.00%)
mean abs diff     : 0.00 / 255
worst channel diff: 0 / 255
```

**位元完全相同**：不用 CLI、不開視窗、自己在程式裡算，得到的結果與官方工具鏈一致。

> 中間我還犯了一個低級錯誤：readback 時多翻了一次列，圖是上下顛倒的。對照 CLI 時那 5.85% 的差異就是它造成的。
> `write_png_file.cpp` 的 `flipY=true` 意思是「**輸入是 bottom-up，幫我翻正**」，
> 而 D3D staging texture 本來就是 top-down。

## 九、限制與下一步

**自寫 CPU renderer 的限制**（GPU 版沒有這些問題，所以它現在的定位是「理解原理」與「沒有 GPU 時的後備」）：

- **不支援圖片與 mesh**：`decodeImage` 回 `nullptr`，`drawImage` / `drawImageMesh` 只計數。
- **沒有反鋸齒**：硬邊。
- **Clip 用 bbox 近似**，不是真正的路徑交集。
- **筆畫是逐段四邊形**：沒有 join、沒有 cap。
- **沒有腳本 VM、沒有文字圖集**：文字以字形外框呈現而非 shaping 後的文字排版。

**剩下的功課**：`rive_pls_renderer` 這條路目前只建了 D3D11（D3D12 的原始碼也在，但沒編）。
其他平台後端（Vulkan / WebGPU / Metal）各自需要不同的 shader 目標（`spirv` / `wgsl` / `metallib`），
而 `spirv` 還需要 glslang 之類的離線編譯器 —— 那是另一條獨立的建置鏈。

### 回到最開始的兩個問題

1. **免費版與付費版差在哪**：差在 **splash 畫面、檔案數、以及團隊／企業功能**。開發與測試完全免費。
2. **有沒有無頭用法**：有，而且**現在有四條**。先用官方 CLI；要處理任意素材用 **Playwright + 官方 WASM**；
   要嵌進自己的 C++ 產品、或需要在伺服器上算圖，用 **C++ runtime + 官方 GPU renderer 離屏**（畫質與線上一致）；
   自寫 CPU renderer 則適合完全沒有 GPU 的環境。

<div style="max-width:640px;margin:1.6rem auto">
<img src="/img/rive-headless-three-routes/ch04-browser-automation.jpg" alt="懸浮於暗處的空窗格內有發光節點網絡，一隻機械臂從側面伸入畫出一條光線" style="width:100%;border-radius:14px">
</div>

> 圖：本機 ComfyUI 的 Qwen-Image 2.1 生成（本站 house style，無文字）。
