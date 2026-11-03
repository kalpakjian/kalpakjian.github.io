# _covergen — 部落格封面產線

封面分兩步：**先產無文字的底圖（Qwen-Image 2.1／本地 ComfyUI），再用 PIL 疊文字**。
這樣同一張底圖可以同時當首頁卡片（有標題）與文章 banner（不能有字，主題會在中央疊日期／字數）。

```
gen_cover_*.py  ──ComfyUI HTTP──▶  _covergen/out/*.png（無文字）
                                      │
compose_cover*.py（或 gen_cover_report.py --bg）──PIL──▶  source/img/covers/*.png
```

## 檔案

| 檔案 | 用途 |
|---|---|
| `gen_cover_qwen.py` | 最早的 Qwen-Image 產圖腳本（單張） |
| `gen_cover_cnn.py` | 「CNN 專題」那篇的 4 張候選（A / B / Awide / Bwide） |
| `compose_cover.py`、`compose_cover_cnn.py` | 把候選疊成 index_img＋banner_img（`SLUG` 寫在檔頭，換篇要改） |
| `gen_cover_report_qwen.py` | 「25 頁教材核對報告」那篇的 4 張候選 |
| `gen_cover_report.py` | 同篇的文字編排；`--bg` 吃 Qwen 圖、不給就畫程序化背景 |

## 前置

```bash
# ComfyUI（本機）
cd ~/Projects/ComfyUI && .venv/bin/python main.py --listen 127.0.0.1 --port 8188
# 需要的模型（models/ 底下）
#   diffusion_models/qwen_image_2.1_int8_convrot.safetensors
#   text_encoders/qwen3vl_8b_int8_convrot.safetensors
#   vae/qwen_image_2.1_vae_bf16.safetensors
```

管線固定用 `KSampler(euler / simple, steps=30, cfg=1.0)`，RTX 4090 上 1344×768 約 25–30 秒一張。

## 用法

```bash
# 1) 產候選（--only A 只跑一張）
../ComfyUI/.venv/bin/python _covergen/gen_cover_report_qwen.py
# 2) 疊字：index 卡片用 A、banner 用 Awide
/tmp/venv-cpu/bin/python _covergen/gen_cover_report.py \
    --bg _covergen/out/report_A.png --bg-banner _covergen/out/report_Awide.png
```

輸出直接寫進 `source/img/covers/`，檔名對應文章 front-matter 的 `index_img` / `banner_img`。

## 慣例與眉角

- **banner 不能有字**：Fluid 主題用 `background-size:cover` 裁切並在中央蓋日期／字數。
- **卡片文字壓左側**：`gen_cover_report.py` 會從 76% 往右壓暗色漸層；
  沒有這層的話，Qwen 圖右側的洋紅光會把標題吃掉（實測踩過一次）。
- **檔案大小**：站上其他封面 0.8–0.9 MB，別壓到很低；`_covergen/out/` 產 10–15 MB 的原始圖，**不版控**。
- **可換路徑**：`COMFYUI_DIR` 環境變數可覆寫 ComfyUI 位置（預設 `~/Projects/ComfyUI`）。
