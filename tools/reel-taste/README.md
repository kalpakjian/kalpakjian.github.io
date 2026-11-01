# reel-taste — 你自己的串流推薦站

一個**零後端、零帳號、零追蹤**的個人推薦頁：匯入你自己的觀看紀錄，
用可解釋的「口味向量」推薦下一步看什麼。

線上：<https://kalpakjian.github.io/reel-taste/>

---

## 為什麼不用「接 API」的方式做

Netflix、Disney+、HBO Max、Prime Video **都沒有開放的觀看紀錄 API**：

| 平台 | 現況（2026-11） |
|---|---|
| Netflix | 只能從「下載你的個人資料」拿到 `ViewingActivity.csv`，通常要等（最長 30 天），且**沒有評分** |
| Trakt | 有正式的 CSV／JSON 匯出，是四家之外最完整的來源（含 1–10 分） |
| Letterboxd | 有 `ratings.csv`／`diary.csv`，評分 0.5–5 星 |
| Disney+ / HBO Max / Prime Video | 目前**沒有**可用的匯出；實務上靠瀏覽器擴充功能 scrobble 到 Trakt |

所以這個站走「匯出 → 丟進來」的半自動路線：不碰帳號密碼、不依賴任何一家
的私有端點，也就不會因為對方改版而整組壞掉。

## 檔案結構

| 檔案 | 角色 |
|---|---|
| `index.html` | 三個分頁的介面（匯入 / 口味 / 推薦） |
| `recommender.js` | **推薦引擎（純函式）**：口味向量、時間衰減、評分、多樣性重排 |
| `import.js` | **解析器（純函式）**：Netflix／Trakt／Letterboxd CSV、純文字 |
| `tmdb.js` | TMDB 查詢層；沒 key 時退回站內快照 |
| `app.js` | UI 控制器：DOM 綁定、localStorage、三個分頁的渲染 |
| `demo-data.js` | 示範紀錄與離線候選片單（虛構） |
| `data/catalog.json` | 離線目錄快照（無 key 時的候選池） |

`recommender.js` 與 `import.js` 都是 UMD 形式，所以**同一份程式碼**
在瀏覽器（`window.ReelTaste`）與 Node（`require()`）都能跑——這是為了可測試。

## 推薦怎麼算的

1. **口味向量**：每筆觀看紀錄貢獻一個權重
   `權重 = 完播率 × 評分加成 × 時間衰減`
   - 完播率 < 20% 視為「試過不喜歡」，乘 0.5 但仍保留負向訊號
   - 自己標的評分權重 1.0、平台回報的 0.6、沒有評分 0
   - 時間衰減用**半衰期**（預設 540 天，可調 270 / 540 / 1080）
2. **候選入池門檻（硬性）**：`vote >= 6.5` 且 `votes >= 200`。
   寧可少推薦幾部，也不要推薦 12 人評 9.9 分的雜訊片。
3. **排序**：類型 0.60 + 語言 0.15 + 年代 0.10 + 品質 0.15
4. **多樣性重排**：同一個主類型最多 N 部（預設 6，可調 3 / 6 / 20）
5. **理由**：每張卡片都寫得出「為什麼」，會引用你實際看過的片
   （例：`你常看 劇情（如《Shogun》）`）

## 隱私

- 觀看紀錄、手動清單、「不想看」標記、TMDB key 全部只存 **localStorage**
- 沒有任何後端，檔案不會上傳
- 唯一的外部請求是：你主動填了 TMDB key 之後，對 TMDB 查片名 metadata
- 「匯出」按鈕會把全部資料存成 JSON，可以帶走

---

## 開發者：怎麼驗證

兩支測試，一支配 CI：

```bash
# 1) 純函式（引擎 + 解析器），不需要瀏覽器
node tools/reel-taste/selftest.js        # 31 checks

# 2) 端到端：真的開 Chrome，按「載入示範資料」，檢查 DOM
npx hexo generate                        # 先產生 public/
node tools/reel-taste/smoke.js           # 20 checks，並截圖
```

`selftest.js` 涵蓋：CSV 引號/換行/BOM、Netflix 多集去重、時間衰減、
硬性門檻、多樣性上限、理由不為 undefined。

`smoke.js` 涵蓋：模組載入、示範資料跑通、推薦內容正確性（已看過的不出現、
低分片被濾掉）、口味頁長條圖、✕ 排除與 localStorage 持久化、重載後狀態、
Console 無例外。

> 踩過的坑（都已寫進測試）：`Math.pow(1, d) === 1` 讓時間衰減完全失效；
> Netflix CSV 標題像 `Shogun: Season 1: Crimson Sky` 需要截斷才去重；
> `explain()` 多接一個 `taste` 參數時，舊呼叫端會靜默產出錯誤字串。
