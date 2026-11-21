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
