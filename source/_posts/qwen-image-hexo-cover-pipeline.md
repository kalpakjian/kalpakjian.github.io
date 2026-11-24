---
title: 用本機 Qwen-Image 2.1 做 Hexo 封面：3 張候選、約 11 秒一張、覆蓋 PNG 就上線
date: 2026-11-24 18:00:00
categories:
  - AI
  - 技術雜談
tags:
  - Qwen-Image
  - ComfyUI
  - Hexo
  - 封面
  - 自動化
  - GitHub Pages
toc: true
index_img: /img/covers/qwen-image-hexo-cover-pipeline.png
banner_img: /img/covers/qwen-image-hexo-cover-pipeline.png
---

![文字流進透鏡、一張圖出來：封面產線](/img/covers/qwen-image-hexo-cover-pipeline.png)

> 這篇是封面產線的操作筆記，不是模型評測：從一句 MOTIF 到文章頂部那張圖。
>
> 全在本機跑（RTX 4090 ＋ ComfyUI 0.45.0），<strong>1344×768、25 steps、cfg 2.5，約 11 秒一張</strong>。
>
> 換封面<strong>不動 markdown</strong>：覆蓋同名 PNG 就行，`index_img`／`banner_img` 兩行都不用改。
>
> 順便記下今天實際踩到的三個坑：`comfy-aimdo` 版本、`candidates/` 命名、`git add -A`。

<!-- more -->

## 一、為什麼不叫雲端 API

| 理由 | 說明 |
| --- | --- |
| 可重現 | 一個資產一個固定 seed，同 seed = 同圖 |
| 風格一致 | 全站共用同一個 BASE 字串，色調不會一站一色 |
| 無版權風險 | 本機擴散模型產出，不必逐張確認授權條款 |
| 成本 | 已付的 GPU；3 張約 33 秒 |

代價也要講清楚：<strong>模型不會寫中文字</strong>。CJK 字形會爛成方塊或鬼畫符，所以提示詞一律禁止出現文字，圖只負責意境，標題交給文章本身。

## 二、產線全貌

```
MOTIF 一句
   ↓  BASE + MOTIF 組成提示詞
3 個 seed 各出一張（1344×768）
   ↓  目視挑 1（看文字、浮水印、結構崩壞）
複製到 source/img/covers/<slug>.png
   ↓  git add / commit / push
GitHub Actions：hexo generate → deploy
```

前四步在本機（約 1 分鐘），後兩步是既有的部署管線。

## 三、環境與工作流

| 項目 | 值 |
| --- | --- |
| ComfyUI | `D:\AI\ComfyUI`，0.45.0，`http://127.0.0.1:8188` |
| Workflow | `workflows\image\qwen_image_2_1_text2img_api.json` |
| UNET | `qwen_image_2.1_int8_convrot.safetensors` |
| CLIP | `qwen3vl_8b_bf16.safetensors`（`type=qwen_image`） |
| VAE | `qwen_image_2.1_vae_bf16.safetensors` |
| 尺寸／步數／CFG | 1344×768／25／2.5（CFG 2.5 是 Qwen-Image 的甜蜜點，不是 SD 的 7） |
| Sampler | `euler` ＋ `simple` |

工作流只有八個節點，客戶端要覆寫的欄位也就這幾個：

| node | class_type | 覆寫 |
| --- | --- | --- |
| 1／2／3 | UNETLoader／CLIPLoader／VAELoader | 模型檔名 |
| 4 | EmptyLatentImage | `width`／`height`／`batch_size` |
| 5 | CLIPTextEncode | `text` |
| 6 | KSampler | `seed`／`steps`／`cfg` |
| 7 | VAEDecode | — |
| 8 | SaveImage | `filename_prefix` |

三個 API 就夠用：`POST /prompt` 送工作流、`GET /history/<prompt_id>` 輪詢、`GET /view?filename=...` 取圖。輪詢間隔 2 秒。

<strong>坑：</strong>workflow JSON 存成 <strong>UTF-8 with BOM</strong>，Python 要用 `encoding="utf-8-sig"` 開，否則 `json.load` 直接炸。

## 四、提示詞分工：BASE ＋ MOTIF

BASE 負責風格，固定不動；MOTIF 只寫主體與語意，<strong>不要</strong>重複「深藍背景、發光、無文字」——那是 BASE 的事，重複描述會讓權重失衡。

```text
BASE = "Dark cinematic tech illustration, deep navy to teal gradient background,
        subtle grid texture, soft volumetric glow, glowing bokeh particles,
        thin luminous cyan wireframe accents, professional engineering aesthetic,
        shallow depth of field, generous negative space, no text, no words,
        no letters, no numbers, no watermark, no logo, 16:9 composition,
        highly detailed, clean composition with one clear focal subject"
```

本文這張的 MOTIF：

```text
a luminous horizontal production line: translucent stacked panels of flowing
lines dissolving into light on the left, passing through a single glowing lens
ring at the centre, and re-emerging on the right as one framed landscape image,
with three faint parallel streams converging into that single frame
```

組合方式就是 `BASE + ". Central subject: " + MOTIF + "."`。<strong>改了 BASE 就要整批重出</strong>，否則新舊圖擺在同一頁會看出色調不一致。

## 五、候選模式：3 個 seed 挑 1

封面會長期掛在文章頂部與首頁卡片，第一張就定稿太賭。慣例是出 3 張、目視、挑 1。種子用 `73NN`：

| seed | 這張 | 結果 |
| --- | --- | --- |
| 7304 | 堆疊面板 → 透鏡 → 風景畫框 | 可用，但右側畫框偏重 |
| 7305 | 同上，光束從左緣直接切出畫面 | 左邊被裁掉，淘汰 |
| **7306** | 面板 → 光環 → 畫框，三段都完整在畫面內 | **採用** |

批次腳本要有續跑守衛：目標檔已存在且大於 10 KB 就 SKIP，避免重跑整批，也避免半張壞圖被當成完成品。

挑圖只看三件事：有沒有文字或浮水印、主體有沒有糊掉、有沒有人體或結構崩壞。有問題<strong>只換該張的 seed（+100）重跑</strong>，不要動 BASE。

## 六、換封面為什麼不用改文章

front-matter 只有兩行指到同一張圖：

```yaml
index_img: /img/covers/qwen-image-hexo-cover-pipeline.png
banner_img: /img/covers/qwen-image-hexo-cover-pipeline.png
```

所以換封面 = 覆蓋同名 PNG。上次替《Hexo 與 Python 的 io》換封面的實測：

| | 舊 | 新 |
| --- | --- | --- |
| bytes | 969,121 | 837,719 |

驗證方式不必開瀏覽器，直接問線上那顆檔多大：

```bash
curl -sL -o NUL -w 'HTTP=%{http_code} BYTES=%{size_download}\n' \
  https://kalpakjian.github.io/img/covers/hexo-and-python-io.png
```

`BYTES` 對上本機檔案大小，就是真的換掉了；還在跑舊值，就是 Pages 還沒建置完（這次約 3 分鐘）或 CDN 快取（`max-age=600`）。

## 七、今天踩到的三個坑

### 1. `comfy-aimdo` 版本落後，模型載入就死

```
ModelVBAR.__init__() got an unexpected keyword argument 'pageout_callback'
```

ComfyUI 升到 0.45.0，但 `comfy-aimdo` 還停在 0.5.6（core 要求 0.6.0）。修法：

```powershell
D:\AI\ComfyUI\python_embeded\python.exe -m pip install "comfy-aimdo==0.6.0"
```

同一個 `system_stats` 裡現在仍寫著 `comfy-kitchen 0.2.39`（要求 0.2.41），而站上的 `tools/comfyui/start_comfyui.ps1` 把它<strong>釘死在 0.2.39</strong>。下次升 core 會在這裡再炸一次。

### 2. 從 shell 啟動 ComfyUI，會連帶被砍

用 `Start-Process` 起的 ComfyUI 是子行程，命令一超時，整個 process tree 被收掉——日誌停在 `Using pytorch attention` 就沒有然後了。改成用 WMI 建立脫離 job 的行程：

```powershell
$cl = 'cmd.exe /c "set PYTHONIOENCODING=utf-8&& set PYTHONUTF8=1&& cd /d D:\AI\ComfyUI && python_embeded\python.exe -s main.py --windows-standalone-build > logs\comfy.out.log 2>&1"'
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine=$cl}
```

`PYTHONIOENCODING` 那兩個環境變數不是裝飾：Windows 主控台是 GBK，logger 吐 emoji 時會 `UnicodeEncodeError`，直接把行程帶走。

### 3. `.gitignore` 是白名單式，`candidates/` 名字要對

站上的規則是「腳本要版控，產出的圖不要」：

```text
_covergen/candidates/
_covergen/**/candidates/
```

這兩條只匹配<strong>目錄名正好是 `candidates`</strong> 的路徑。第一次把候選放進 `_covergen/hexo2io_candidates/`，結果 2.5 MB 的 PNG 全掛在 untracked；而 `_covergen/` 底下本來就還有數百個未追蹤的 `yk*_rules.txt`、`batch_*.py`——<strong>一次 `git add -A` 就會全掃進去</strong>。

正確做法：候選一律進 `_covergen/candidates/<主題>/`，提交用明確路徑而不是 `-A`：

```bash
git add source/img/covers/<slug>.png _covergen/cover_<主題>.py
```

## 八、時間與體積

| 項目 | 實測 |
| --- | --- |
| 單張生成 | 約 11 秒（1344×768／25 steps／RTX 4090） |
| 3 張候選 | 約 33 秒（不含首次載入模型） |
| 原始 PNG | 718 KB – 838 KB／張 |
| 進版控 | 只放選中的那張 |

候選留在本機、不進 git；要重出同一張，seed 就是答案。

## 九、檢查清單

- MOTIF 一句，只寫主體，不寫風格與禁字
- 3 個 seed，目視挑 1（文字／浮水印／結構）
- 尺寸 1344×768、PNG
- 覆蓋 `source/img/covers/<slug>.png`，與 front-matter 同名
- 候選放 `_covergen/candidates/<主題>/`
- `git add` 用明確路徑
- push 後用 `size_download` 對線上檔案大小

---

<strong>一句話總結：</strong>封面難的從來不是生成，是<strong>可重現</strong>——固定 seed、固定 BASE、固定尺寸，換一張只是改一個數字。
