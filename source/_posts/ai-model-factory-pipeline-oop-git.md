---
title: 大型 AI 模型不是一個人「一次過訓完」的——把專案拆成工廠流水線：繼承、工廠模式與 Git 協作
date: 2026-10-10 10:00:00
categories:
  - 軟體工程
tags:
  - 模組化
  - 設計模式
  - 工廠模式
  - 繼承與覆寫
  - 前中後訓練
  - Git
  - git blame
  - 自動駕駛
  - 協作開發
  - 程式碼審查
toc: true
index_img: /img/covers/ai-model-factory-pipeline-oop-git.png
banner_img: /img/covers/ai-model-factory-pipeline-oop-git.png
---

> <strong>整理說明</strong>：本篇整理自一則討論「大型 AI 模型與自動駕駛模型如何被工程化」的社群貼文觀點，並補上物件導向、工廠模式與 Git 的技術細節，同時對「純 camera 與融合模型」那段加上必要的澄清。名詞解釋與工具用法以官方文件與維基百科為準，此為學習整理用途。

<!-- more -->

## 一句話總結

> 大型 AI 模型不是一個人「一次過訓完」的成品，而是一條<strong>工廠流水線</strong>：模型被拆成多個<strong>可分工、可重用、可替換</strong>的模組；程式碼則靠<strong>物件導向設計</strong>（繼承、工廠模式）與 <strong>Git</strong> 讓多人安全協作。

貼文真正想傳達的其實不是幾個時髦名詞，而是三條工程紀律：

1. <strong>模組化</strong>——讓不同的人可以同時改不同的部分，而不互相踩腳。
2. <strong>版控紀律</strong>——每次修改都可回溯、可審查、可分工。
3. <strong>可驗證性</strong>——每個模組都能獨立測試，最後才組裝成完整模型。

---

## 他在講什麼？用語對照表

| 貼文用語 | 實際意思 | 對應的技術 |
| --- | --- | --- |
| 繼承 + overwrite | 新模型類別繼承舊模型類別，只改寫有差異的方法；其他功能照用 | OOP 繼承與方法<strong>覆寫（override）</strong> |
| 工廠模式 | 用統一介面建立不同模型／模組，方便拆件、替換、組合 | Factory Method / Abstract Factory |
| 前／中／後訓練 | 前段訓感知模組，中段訓規劃控制，後段用 RL 微調整體 | 多階段訓練（pretrain → mid-train → post-train RL） |
| Git 版控 | 記錄每次修改，可回溯、分工、合併，避免一人改壞整包 code | Git branch / merge / pull request |
| `git blame` | 查某行程式碼最後是誰、在哪個 commit 改的 | `git blame`、`git log -L` |

---

## 繼承為何能「沒實作也能跑」？

例如原本有一個 `BaseModel`，已寫好資料載入、訓練迴圈、儲存、評估等功能。升級時只要寫：

```python
class NewModel(BaseModel):
    def forward(self, x):
        # 只改這裡：換掉新的網路結構
        ...
```

`NewModel` 沒有重新寫 `train()`、`save()`，但它們仍然存在，因為是從 `BaseModel` <strong>繼承</strong>下來的。這就是「沒實作某個 function 也能跑」的原因。只覆寫 `forward()`，等於只替換有差異的部分，其他整個模型基礎設施都重用。

### 機制：屬性查找會往上找，但 `self` 仍然是子類別

```python
class BaseModel:
    def load_data(self):
        """資料載入：所有模型共用"""
        ...

    def forward(self, x):
        """模型前向傳播：每個模型不同"""
        raise NotImplementedError

    def backward(self, pred, target):
        """反向傳播：所有模型共用"""
        ...

    def train(self, epochs=10):
        """訓練迴圈：所有模型共用"""
        for epoch in range(epochs):
            for x, y in self.load_data():
                pred = self.forward(x)      # ← 這裡會呼叫子類別的實作
                self.backward(pred, y)
            print(f"epoch {epoch} done")

    def evaluate(self, loader):
        ...

    def save(self, path):
        ...
```

當你呼叫 `NewModel().train()` 時，發生的順序是：

1. `NewModel` 找不到 `train` → 沿著<strong>方法解析順序（MRO）</strong>往 `BaseModel` 找 → 找到 `BaseModel.train`。
2. 執行 `BaseModel.train` 時，`self` 指向的仍然是 <strong>`NewModel` 實例</strong>。
3. 因此 `self.forward(x)` 會解析到 `NewModel.forward`，而不是 `BaseModel.forward`。

這就是<strong>多型（polymorphism）</strong>：父類別寫好流程，子類別只提供差異點。這種「父類別定流程、子類別填細節」的寫法有個正式名字——<strong>樣板方法模式（Template Method）</strong>。

### 「沒實作也能跑」的兩個前提

| 前提 | 說明 | 踩雷的後果 |
| --- | --- | --- |
| 父類別必須<strong>真的有實作</strong> | 若 `BaseModel` 只是空殼、關鍵方法全部 `raise NotImplementedError`，子類別沒覆寫就會直接爆 | 呼叫 `train()` 時噴 `NotImplementedError` |
| <strong>覆寫的方法簽章與回傳格式要一致</strong> | `forward()` 回傳的 tensor 形狀、dtype、命名要符合父類別 `backward()` 的預期 | 程式「看起來能跑」，但 loss 是 NaN 或維度錯誤 |

第二點正是「<strong>看起來能動</strong>」與「<strong>真的能動</strong>」的差別：繼承讓你少寫程式碼，但不會幫你檢查介面契約。所以共用介面最好用型別註解、資料類別（dataclass）或單元測試把契約固定下來。

---

## 「工廠模式」在模型開發裡的角色

工廠模式是把「建立物件」這件事集中到一個工廠方法，呼叫方不需要自己 `new` 具體類別；子類別或設定檔可以決定實際生成哪種模型。

```python
class ModelFactory:
    _registry = {}

    @classmethod
    def register(cls, name):
        """用裝飾器把模型註冊進工廠"""
        def deco(model_cls):
            cls._registry[name] = model_cls
            return model_cls
        return deco

    @classmethod
    def create(cls, name, **kwargs):
        if name not in cls._registry:
            raise KeyError(f"未知的模型類型：{name}")
        return cls._registry[name](**kwargs)


@ModelFactory.register("camera")
class CameraModel(BaseModel):
    def forward(self, x):
        ...


@ModelFactory.register("fusion")
class FusionModel(BaseModel):
    def forward(self, x):
        ...
```

呼叫端只需要一行，完全不需要知道具體類別：

```python
model = ModelFactory.create(cfg["model_type"], **cfg["model_args"])
model.train()
```

### 在自動駕駛模型裡的樣子

<div class="pipeline">
  <div class="pipeline-title">ModelFactory —— 統一介面，不同模組各自訓練</div>
  <div class="pipeline-track">
    <div class="pipeline-node"><span class="node-name">CameraModel</span><span class="node-desc">感知 · 單獨訓練 camera</span></div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-node"><span class="node-name">LidarModel</span><span class="node-desc">感知 · 單獨訓練 lidar</span></div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-node"><span class="node-name">FusionModel</span><span class="node-desc">融合 · camera + lidar</span></div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-node"><span class="node-name">PlanningModel</span><span class="node-desc">規劃控制 · action／規控</span></div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-node"><span class="node-name">FullRLModel</span><span class="node-desc">後訓練 · 全模型 RL 微調</span></div>
  </div>
</div>

好處是：

- <strong>分工</strong>：A 組訓 camera、B 組訓 lidar、C 組訓 fusion、D 組訓 planning。
- <strong>重用</strong>：camera 模組升級時，不必重寫整個系統。
- <strong>可替換</strong>：日後把 lidar 換成純 camera，只要換掉對應模組或工廠設定。
- <strong>可測試</strong>：每個模組可獨立驗證，再組合成完整模型。
- <strong>可設定化</strong>：實驗用 YAML 指定 `model_type` 就能跑不同組合，不必改程式碼。

<div class="callout">
  <div class="callout-title">重點澄清</div>
  <p>所以作者說的「一個模型拆成工廠流水線」，重點<strong>不是「工廠模式」字面本身</strong>，而是：<strong>模型架構必須模組化</strong>，才能讓多人同時訓練不同部分，最後組裝成一個模型。工廠模式只是讓這件事在程式碼層面「可以被安全組裝」的手段之一。</p>
</div>

---

## 前／中／後訓練：把訓練拆成流水線

| 階段 | 訓什麼 | 典型目標 | 常見手法 |
| --- | --- | --- | --- |
| 前段（感知） | Camera / Lidar / Fusion 模組 | 特徵提取、偵測、深度、時序理解 | 監督式學習、大規模標註資料、自監督預訓練 |
| 中段（規劃控制） | Planning 模組 | 行為決策、軌跡生成、規控銜接 | 模仿學習、規則式規控、離線 RL |
| 後段（整體微調） | 整個模型（端到端） | 系統層級表現、人類偏好對齊 | RL／偏好優化、閉環模擬與回饋 |

為什麼要分段，而不是端到端一次訓完？

- <strong>錯誤可歸因</strong>：表現變差時，能先判斷是感知、規劃還是整體微調的問題。
- <strong>可獨立迭代</strong>：感知模組改版不需要重跑整個後訓練流程。
- <strong>可平行開發</strong>：不同團隊在同一時間推進不同階段，靠介面與測試對齊。
- <strong>成本可控</strong>：後段 RL 最貴，只在前面穩定後才啟動。

---

## Git 為何是基本技能？

中大型模型專案通常多人同時改 code。Git 會記錄檔案與程式碼的歷史版本，讓團隊能檢視變更、回復版本、用 branch 分頭開發，再合併回主線。

### 用遊戲存檔來理解

| Git 概念 | 遊戲比喻 | 實務用途 |
| --- | --- | --- |
| `commit` | 存檔點 | 一次有意義的修改紀錄 |
| `branch` | 開新存檔測試玩法，不影響主存檔 | 隔離開發中的功能或修 bug |
| `merge` | 把測試成功的改動合回主線 | 功能完成後併回 `main` |
| `revert` / `checkout` | 讀取舊存檔 | 回退錯誤改動或查看舊版本 |
| `git blame` | 查「這一行是誰、哪次存檔改的」 | 追溯問題脈絡 |

### 多人模型專案的標準節奏

```text
main（永遠可發佈）
 ├─ feature/camera-v2       ← A 組：升級 camera 模組
 ├─ feature/planning-rl     ← B 組：改規控與 RL 微調
 └─ fix/lidar-time-sync     ← C 組：修感測器時間同步 bug
        ↓  Pull Request + Code Review + CI 測試
      合併回 main（每個人都能追到「為什麼這樣改」）
```

Git 的 branch 機制讓開發者可在獨立空間改功能或修 bug，不直接影響主專案；之後再 merge 回去。

### `git blame` 的正確用法

`git blame` 顯示每一行程式碼最後一次被修改的 commit、作者與時間。它<strong>不是拿來問罪的工具</strong>，而是找脈絡的入口：

```bash
# 誰、哪個 commit 改的
git blame -L 120,160 model/forward.py

# 這段程式碼的演變史（比 blame 更有用）
git log -L 120,160:model/forward.py --oneline

# 找出「哪個 commit 讓測試開始壞掉」
git bisect start
git bisect bad HEAD
git bisect good v1.2.0
```

---

## 「融合模型 vs 純 camera」那段

他的論點是：如果團隊本來就會做 camera、lidar 及兩者融合，那麼他們已具備處理感知輸入、特徵提取、時序資訊、規控銜接等能力；改做純 camera 方案時，主要是移除 lidar 分支與調整融合架構，而不是從零學起。

但要注意，這不代表「完全沒差」：

| 維度 | 融合（camera + lidar） | 純 camera |
| --- | --- | --- |
| 深度資訊 | lidar 直接量測，較可靠 | 需依賴視覺深度估計、多幀幾何與資料規模 |
| 失效模式 | lidar 對光照較不敏感，夜間仍可運作 | 受夜間、逆光、雨霧影響較大 |
| 資料需求 | 標註需求相對較低 | 更吃資料量與情境多樣性 |
| 安全設計 | 感測器冗餘（模態互補） | 需要時間冗餘、模型冗餘或地圖先驗 |
| 驗證方式 | 可做多模態交叉驗證 | 需針對視覺邊界情境另行設計測試 |

<div class="callout">
  <div class="callout-title">一句話分清楚</div>
  <p>「純算法角度原理一樣」指的是<strong>工程能力可遷移</strong>；不是說兩種感測方案在資料、可靠性和硬體設計上完全等價。能力可遷移，但風險模型要重新設計。</p>
</div>

---

## 最後一句的重點：沒人在意 code 是不是 LLM 寫的

意思是：AI 可以幫你寫 code，但真正被審核的是：

1. <strong>模型效果是否更好</strong>——有沒有 baseline、指標與可重現的實驗紀錄。
2. <strong>是否符合團隊 coding style</strong>——命名、介面、日誌、錯誤處理是否一致。
3. <strong>是否會破壞其他人的模組</strong>——介面是否向後相容、有沒有回歸測試。
4. <strong>是否能通過測試、code review 與 Git 版控流程</strong>——能不能被追溯、被回退。

換言之，LLM 是生產力工具；但在多人模型專案裡，<strong>模組化設計、測試、Git 紀律和責任追蹤</strong>才是能不能把 code 放進主線的關鍵。

### 可以立刻照做的檢查清單

- [ ] 新增模型時，先問「它繼承誰、覆寫哪些方法、介面契約是什麼」。
- [ ] 模型建立一律走工廠或設定檔，不要在訓練腳本裡散落 `new` 具體類別。
- [ ] 每個模組都要有能獨立跑的測試或最小重現指令。
- [ ] 一個功能一個 branch、一個 PR，說明「為什麼改」而不只是「改了什麼」。
- [ ] 合併前跑過 CI；合併後保留可回退的 commit 紀錄。
- [ ] 用 `git blame`／`git log -L` 追脈絡，而不是追責任。

---

## 一頁速查表

| 概念 | 一句話 | 工具或語法 |
| --- | --- | --- |
| 繼承 + 覆寫 | 共用流程放父類別，只換有差異的方法 | `class NewModel(BaseModel)` |
| 樣板方法 | 父類別定流程、子類別填細節 | `self.forward()` 多型呼叫 |
| 工廠模式 | 用統一介面建立不同模型，方便替換與組合 | `ModelFactory.create(name)` |
| 前／中／後訓練 | 感知 → 規劃控制 → 整體 RL 微調 | 分階段訓練流程 |
| 版控 | 每次修改都可回溯、可分工、可合併 | `git commit` / `branch` / `merge` |
| 責任追蹤 | 查某行程式碼的來歷與演變 | `git blame` / `git log -L` |

---

## 延伸連結

- 🏭 設計模式：[Factory method pattern](https://en.wikipedia.org/wiki/Factory_method_pattern)
- 📚 版控入門：[About Version Control — Pro Git](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
- 🧭 Git 指南：[Git Guides](https://github.com/git-guides)
- 👥 協作流程：[What is Collaboration in Git?](https://www.geeksforgeeks.org/git/what-is-collaboration-in-git/)

---

> <strong>版權聲明</strong>：本篇為社群觀點之學習整理與技術補充，名詞定義引用自維基百科與 Git 官方文件。程式碼範例為說明用途之簡化版本，非任何特定專案之原始碼。如有錯誤或遺漏，歡迎來信指正。
