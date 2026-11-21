# 第 5 章 · 序列與容器類型

## 1. 序列（Sequence）

「序列」是一塊可存放多個值的連續記憶體，值按順序排列，可用**索引**存取。可想像成旅店：房間＝記憶體位置、房號＝索引。

Python 的序列包含字串、列表、元組、集合、字典（其中集合與字典不支援索引、切片、相加、相乘）。

### 1.1 索引

索引從 `0` 起算；也支援負索引（`-1` 為最後一個）。

```
s = "python"
print(s[0], s[-6])   # p p
print(s[5], s[-1])   # n n
```

### 1.2 切片

語法 `sname[start:end:step]`（前閉後開）：

- `start`：起始索引（預設 0）
- `end`：結束索引（預設長度）
- `step`：間隔（預設 1）

```
s = "python"
print(s[:2])    # py
print(s[::2])   # pto（每隔 1 個取 1 個）
print(s[:])     # python
```

<figure class="fig-svg"><svg viewBox="0 0 780 230" width="100%" role="img" aria-label="Python 序列索引與切片：左起 0、右起 -1；切片 [start:end:step] 含頭不含尾" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><text x="30" y="32" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="13" fill="#e6edf3">序列：索引左起 0、右起 -1；切片 s[start:end:step]（含頭不含尾）</text><g font-family="'Microsoft JhengHei','Segoe UI',sans-serif" text-anchor="middle"><text x="93" y="80" font-size="12.5" fill="#39d0d8">0</text><text x="165" y="80" font-size="12.5" fill="#39d0d8">1</text><text x="237" y="80" font-size="12.5" fill="#39d0d8">2</text><text x="309" y="80" font-size="12.5" fill="#39d0d8">3</text><text x="381" y="80" font-size="12.5" fill="#39d0d8">4</text><text x="453" y="80" font-size="12.5" fill="#39d0d8">5</text><rect x="60" y="92" width="66" height="54" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><rect x="132" y="92" width="66" height="54" rx="8" fill="#132030" stroke="#39d0d8" stroke-width="2"/><rect x="204" y="92" width="66" height="54" rx="8" fill="#132030" stroke="#39d0d8" stroke-width="2"/><rect x="276" y="92" width="66" height="54" rx="8" fill="#132030" stroke="#39d0d8" stroke-width="2"/><rect x="348" y="92" width="66" height="54" rx="8" fill="#132030" stroke="#39d0d8" stroke-width="2"/><rect x="420" y="92" width="66" height="54" rx="8" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="93" y="128" font-size="22" fill="#e6edf3">P</text><text x="165" y="128" font-size="22" fill="#e6edf3">y</text><text x="237" y="128" font-size="22" fill="#e6edf3">t</text><text x="309" y="128" font-size="22" fill="#e6edf3">h</text><text x="381" y="128" font-size="22" fill="#e6edf3">o</text><text x="453" y="128" font-size="22" fill="#e6edf3">n</text><text x="93" y="170" font-size="12.5" fill="#7ee787">-6</text><text x="165" y="170" font-size="12.5" fill="#7ee787">-5</text><text x="237" y="170" font-size="12.5" fill="#7ee787">-4</text><text x="309" y="170" font-size="12.5" fill="#7ee787">-3</text><text x="381" y="170" font-size="12.5" fill="#7ee787">-2</text><text x="453" y="170" font-size="12.5" fill="#7ee787">-1</text></g><text x="520" y="110" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#f0a04b">s[1:5] → 'ytho'</text><text x="520" y="132" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#f0a04b">s[::2] → 'pto'</text><text x="520" y="154" font-family="'Microsoft JhengHei','Segoe UI',sans-serif" font-size="12.5" fill="#f0a04b">s[::-1] → 反轉</text><figcaption>圖：Python 序列（字串）的索引與切片。</figcaption></svg></figure>

### 1.3 相加

型別相同的序列可用 `+` 連接（不去重）：

```
print("py" + "th" + "on")   # python
```

### 1.4 常用內置函數

| 函數 | 功能 |
| --- | --- |
| `len()` | 長度（元素個數） |
| `max()` / `min()` | 最大／最小元素 |
| `list()` / `str()` | 轉為列表／字串 |
| `sum()` | 元素加總（元素須為數字） |
| `sorted()` | 排序 |
| `reversed()` | 反轉 |
| `enumerate()` | 產生索引序列（常用於 for） |

```
s = "python-django"
print(max(s), min(s))
print(sorted(s))
```

## 2. List（列表）

方括號、逗號分隔，元素可不同型別。

### 2.1 建立與訪問

```
list1 = ['js', 'py', 'css', 'html']
print(list1[0], list1[-1])       # js html
print(list1[0:3], list1[1:3])    # 前 3 項 / 第 2、3 項
```

### 2.2 更新與刪除

以索引修改元素；`append()` 追加；`del` 刪除。

```
list1[2] = "sass"
list1.append("jsx")
del list1[0]
```

## 3. Tuple（元組）

小括號、逗號分隔；元素**不可修改**，但可索引／切片／`+` 連接。

```
tup1 = ('d1', 'd2', 'd3', 'd4')
two = ()          # 空元組
one = (99,)       # 單元素元組（逗號不可省）
print(tup1[0], tup1[1:5])
print(('order', '66') + ('star', 'war'))   # 連接
```

內建函數：`len()`、`max()`、`min()`、`tuple()`（把列表轉元組）。

## 4. Dictionary（字典）

無序的**鍵值對**集合：`{key: value}`。鍵必須唯一且不可變（字串、數字、元組），值可為任意型別。

### 4.1 基本操作

```
d = {'China': 'CN', 'Hong Kong': 'HK'}
print(d['China'])        # 取值
d['Taiwan'] = 'TW'       # 新增／修改
del d['Hong Kong']       # 刪除
```

### 4.2 鍵的特性

- **鍵不可重複**：重複賦值以最後一次為準。
- **鍵必須不可變**：用列表當鍵會報 `TypeError: unhashable type: 'list'`。

### 4.3 內建函數

`len()`（鍵數）、`str()`、`type()`，以及 `keys()`、`values()`、`clear()` 等方法。

## 5. Set（集合）

無序、不重複的元素集合；用 `{}` 或 `set()` 建立（空集合必須用 `set()`）。

### 5.1 去重與成員測試

```
basket = {'apple', 'orange', 'apple', 'pear'}
print(basket)                 # 自動去重
print('orange' in basket)     # True
```

### 5.2 集合運算

```
a = set('abracadabra'); b = set('alacazam')
print(a - b)   # 差集
print(a | b)   # 並集
print(a & b)   # 交集
print(a ^ b)   # 對稱差
```

### 5.3 基本操作

| 操作 | 說明 |
| --- | --- |
| `s.add(x)` | 加入元素（已存在則不動作） |
| `s.update(x)` | 加入多個元素（可為列表、元組等） |
| `s.remove(x)` | 移除元素（不存在會報錯） |
| `s.discard(x)` | 移除元素（不存在不報錯） |
| `s.pop()` | 隨機移除一個元素（結果不確定，不建議） |
| `len(s)` | 元素個數 |
