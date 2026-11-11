---
title: 一支 640×360 的太極拳影片，能變成可用的 3D 動作嗎？MediaPipe 與 GVHMR 兩條路線的實測
date: 2026-11-11 20:00:00
categories:
  - AI 研究札記
tags:
  - 動作捕捉
  - SMPL-X
  - GVHMR
  - MediaPipe
  - Blender
  - 實測
index_img: /img/covers/taichi-mocap-single-camera.png
banner_img: /img/covers/taichi-mocap-single-camera.png
---

## 一句話總結

一支 640×360、419 kbps、15 fps 的十分鐘太極拳影片，可以變成能用的 3D 動作資料；但「能用」與「精確」差了兩個量級：MediaPipe 的 17 關節版本關節位置誤差 <strong>37 cm</strong>，換成 GVHMR + SMPL-X 後降到 <strong>0.03 cm</strong>。

<span> </span><strong>真正的瓶頸不是模型，是素材本身</strong>：單眼、寬鬆白衣、腳被字幕壓住。解法是換路線，不是換更大的模型。

## 1. 素材與限制（先說壞消息）

| 項目 | 實測 |
|---|---|
| 解析度／位元率 | 640×360、419 kbps、H.264 |
| 幀率／長度 | 15 fps、633.16 s（9,497 幀） |
| 阻礙 | 人物僅約 150 px 高、白衣遮住肢體、字幕壓在腳上、右上角有浮水印 |

這些條件決定了後面所有數字的上限。單眼相機沒有真正的深度資訊，模型只能從「人體比例」與「動作連續性」去猜；衣服越寬鬆、遮擋越多，猜得越差。

## 2. 第一步不是模型，而是把畫面變乾淨

用 Real-ESRGAN x2（fp16、RTX 4090）先升頻，再交給偵測器：

| | 原始 | 增強後 |
|---|---|---|
| 解析度 | 640×360 | <strong>1280×720</strong> |
| 位元率 | 419 kbps | 2.25 Mbps |
| 檔案 | 33 MB | 178 MB |
| 處理耗時 | — | <strong>821 秒</strong>（9,497 幀，約 11.6 幀/秒） |

流程是「解碼 → hqdn3d 去噪 → GPU 超分 → x264 重編碼」，全程用管道串流、不落地中繼檔。去噪那一步很關鍵：419 kbps 的來源充滿塊狀雜訊，直接超分會把雜訊一起放大成「細節」。

## 3. 路線 A：MediaPipe 17 關節（快、免授權）

60 秒、900 幀的實測：<strong>0 幀漏檢</strong>，骨架疊在真人身上的位置肉眼看起來很準。

但一量骨長就露餡：同一根骨頭在不同幀的長度可以差到數十公分，最大關節位置偏差 <strong>37 cm</strong>（腳部最差）。原因是單眼深度估計不穩定，模型每幀各自猜一次深度。

<figure>
<img src="/img/taichi-mocap-single-camera/fig-overlay.jpg" alt="MediaPipe 偵測到的 33 個關節疊在太極拳示範者身上，左上角顯示可見度 0.84" />
<figcaption>圖 1：MediaPipe 的 2D 疊加結果。肉眼幾乎挑不出錯，但每幀的深度是獨立猜出來的，所以骨長會浮動。</figcaption>
</figure>

這一段還順手抓出兩個自己寫錯的 bug，兩個都是「看起來對、量起來錯」的類型：

1. Euler 角度反解寫錯：round-trip 誤差 1.97（應該接近 0）。用「把 BVH 通道還原回關節位置」的 FK 檢查才發現。
2. BVH 的通道值順序與階層宣告順序不一致：手臂的旋轉被貼到別的關節上。因為 FK 檢查是唯一可信的裁判，這類錯誤在畫面上不一定看得出來。

## 4. 最花時間的 bug：整個動作是鏡像

把 MediaPipe 的 y-down 座標只翻 y 軸（y 朝下 → y 朝上）會讓座標系從右手系變成左手系（det = −1），結果是<strong>整段動作變成照鏡子的版本</strong>：左右相反、前後也相反。

這種錯誤對稱性很高，FK 檢查抓不到（鏡像資料本身自洽），2D 疊加圖也抓不到（畫的是 2D 關鍵點）。判定方法是做一次 PnP 解相機，然後量「鼻子是否比耳朵靠近相機」：

| 版本 | 鼻子在耳朵前方的幀比例 | 投影回原片的誤差 |
|---|---|---|
| 只翻 y（錯） | <strong>0.18</strong> | 12.5 px |
| 翻 y 與 z（正） | <strong>0.83</strong> | 10.6 px |

修正只需一行：<code>(x, y, z) → (x, −y, −z)</code>，翻兩個軸才保持手性。

## 5. 路線 B：GVHMR + SMPL-X

GVHMR（SIGGRAPH Asia 2024／TPAMI 2026）用 SMPL-X 人體模型做世界座標的動作重建。這條路精確得多，但前置成本也高：

| 關卡 | 實況 |
|---|---|
| SMPL-X 本體模型 | 需要註冊＋驗證信，非商用授權；帳號沒驗證時登入只會回「Account not confirmed」 |
| pytorch3d 依賴 | 官方只提供 Linux wheel，Windows 沒有預編譯版 |
| 權重 | 5.3 GB（GVHMR 156 MB、HMR2 2.58 GB、ViTPose 2.43 GB、YOLO 130 MB） |

pytorch3d 的解法是寫一個純 torch 的替代套件：只實作 GVHMR 真正用到的 10 個旋轉轉換函式、一個 kNN、一個 <code>look_at_rotation</code>，其餘（渲染）留成會明確報錯的 stub，並在 demo 加上 <code>--no_render</code> 跳過預覽渲染。驗證方式是把公開的官方公式拉下來逐一比對，round-trip 誤差 <strong>低於 6e-7</strong>，12 個相關模組全部 import 成功。

全片（633 秒、18,994 幀 @30fps）的實測：

| 階段 | 耗時 |
|---|---|
| 前置（YOLO 追蹤＋ViTPose＋HMR2 特徵） | <strong>864.6 秒</strong> |
| 去噪器推論（40.9M 參數） | <strong>79.7 秒</strong> |

## 6. 精確度對照

| | MediaPipe 17 關節 | <strong>GVHMR + SMPL-X 22 關節</strong> |
|---|---|---|
| 骨長一致性（std） | 數十公分等級浮動 | <strong>0.00 cm</strong>（SMPL 是剛體） |
| BVH 還原誤差 | 37 cm | <strong>0.03 cm</strong> |
| 軀幹扭轉（twist） | 無 | 有 |
| 授權 | 免註冊 | SMPL-X 需註冊（非商用） |

中間還有一個容易被忽略的環節：<strong>匯出方式</strong>。第一版是從關節位置反推旋轉，雖然畫得出來，但掉了 twist，FK 誤差 12.51 cm；改成直接拿 SMPL-X 參數裡的 axis-angle（每根骨頭本來就有旋轉）之後降到 0.03 cm。也就是說，資料一直都在，是匯出時被我丟掉了。

<figure>
<img src="/img/taichi-mocap-single-camera/fig-sbs.jpg" alt="左：太極拳原始影片；右：同一時間點的 SMPL-X 骨架立體渲染（90 度側視）" />
<figcaption>圖 2：左為原始影片、右為 SMPL-X 骨架（側視 90 度）。骨架的骨長全程固定，腳掌高度也對得上；差異最大的是手部——GVHMR 只預測到手腕。</figcaption>
</figure>

## 7. 相機：一個「看起來像壞掉」的問題

骨架出來之後，最常被問的是「為什麼人物在走動」。原因是靜止機位＋單眼深度會讓世界座標慢慢漂移，實測水平漂移達 <strong>3.66 公尺</strong>（人物其實原地打拳）。處置是把骨盆的水平位移扣掉、只保留高度，動作本身不動。

相機方位則試了三種：正面偏 45 度（兩側）、正側面 90 度、以及 180 度轉身。最後交給使用者挑的是 <strong>90 度側視</strong>——太極拳的重心前後移、前後腳開合，側面看得最清楚。全片輸出兩個版本：背面（90 度）與正面（90 度＋180 度），兩者都是靜止機位、無音訊。

流程上還有一個教訓：<strong>先用 10 秒 sample 定角度，再跑全片</strong>。全片一次要 22 分鐘渲染，先看 sample 可以省下大量白工。

## 8. 資源實測（RTX 4090 24 GB）

| 階段 | 峰值 VRAM（扣掉桌面基準） | 用 GPU？ |
|---|---|---|
| Real-ESRGAN 超分 | +0.38 GB | 是（fp16） |
| MediaPipe 姿態 | 0 | 否（XNNPACK CPU） |
| GVHMR 全流程 | <strong>+3.9 GB</strong>（峰值 5.35 GB） | 是（瞬時可到 76%） |
| Blender 骨架渲染 | +0.03 GB | 是（Workbench 光柵化，平均 24%） |
| ffmpeg 編碼 | 0 | 否（libx264） |

換句話說整條線最高只用到 24 GB 的 22%。真正的 VRAM 大戶是背景同時開著的 ComfyUI——它載入模型時曾佔 22.8 GB，那時才需要先叫它釋放。

硬碟才是壓力點：18,994 張暫存 PNG 一度吃掉 <strong>9.8 GB</strong>，跑完已清。

## 9. 我的實務結論

1. <strong>要「能改、能重定向、能量角度」→ 走 GVHMR</strong>。動作是真正的 3D 骨架，換角色、換鏡頭、做教學分解都行。
2. <strong>要「今天就有結果、不想處理授權」→ 走 MediaPipe</strong>，接受腳部抖動與無 twist。
3. 能改善素材的話，效益遠大於換模型：緊身衣、腳不要被字幕遮住、≥720p、30 fps、單一人物。
4. 任何骨架管線都要有 <strong>FK 回歸檢查</strong>（把BVH通道還原回關節位置比對），否則「看起來對、其實錯了 12 公分」這種事會一路帶到成品。

## 10. 產出與腳本

| 檔案 | 用途 |
|---|---|
| <code>gvhmr_full.bvh</code> | 全片 22 骨動作，18,994 幀 @30fps（重定向用） |
| <code>gvhmr_full.npz</code> | 22 關節世界座標 |
| <code>gvhmr_full_side_by_side_front180.mp4</code> | 原片｜正面骨架對照（1920×540、10 分 33 秒） |
| <code>pose_extract.py</code> | MediaPipe 擷取 → BVH／npz（免授權路線） |
| <code>gvhmr_export.py</code> | SMPL-X 參數 → BVH（保留 twist） |
| <code>bvh_preview_blender.py</code> | Blender 無頭渲染骨架、可調視角 |
| <code>verify_bvh.py</code> | FK 回歸檢查（骨頭方向 cos、位置誤差） |

> <strong>查證說明</strong>：本文所有數字都是 2026-11-11 在本機（RTX 4090、ComfyUI 同機）實測取得，
> 不是引用排行榜。骨長、FK 誤差、投影誤差由同一套腳本量測；GPU／VRAM 以 nvidia-smi 1 秒採樣。
> 無法自行確認的是「畫面好不好看」——那需要人眼判斷，本文只提供可量測的部分。
>
> <strong>封面與圖表</strong>：封面由本機 ComfyUI 的 Qwen-Image 2.1 生成（刻意不含文字）；
> 內文圖片是實際輸出影片的截圖，非示意圖。
