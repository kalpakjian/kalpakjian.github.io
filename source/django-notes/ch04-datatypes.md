# 第 4 章 · 數據類型、運算符與數字

## 1. 基本數據類型

Python 3 有六種標準型別：**Number（數字）、String（字串）、List（列表）、Tuple（元組）、Set（集合）、Dictionary（字典）**。

變數本身沒有型別——型別屬於它所指的物件，可用 `type()` 查詢。

<figure class="fig-svg"><svg viewBox="0 0 700 250" width="100%" role="img" aria-label="Python 六種標準型別與可變／不可變分類" style="background:#0d1117;border-radius:10px"><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#39d0d8"/></marker></defs><g font-family="'Microsoft JhengHei','Segoe UI',sans-serif"><rect x="235" y="16" width="230" height="46" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="350" y="45" text-anchor="middle" font-size="14" fill="#e6edf3">Python 3 六種標準型別</text><path d="M350 62 L350 82 L175 82 L175 100" fill="none" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><path d="M350 62 L350 82 L525 82 L525 100" fill="none" stroke="#39d0d8" stroke-width="1.6" marker-end="url(#a)"/><rect x="60" y="104" width="230" height="132" rx="10" fill="#132030" stroke="#2c6fb1" stroke-width="1.6"/><text x="175" y="130" text-anchor="middle" font-size="13.5" fill="#39d0d8">不可變 immutable</text><text x="175" y="158" text-anchor="middle" font-size="12.5" fill="#e6edf3">Number（數字）</text><text x="175" y="182" text-anchor="middle" font-size="12.5" fill="#e6edf3">String（字串）</text><text x="175" y="206" text-anchor="middle" font-size="12.5" fill="#e6edf3">Tuple（元組）</text><rect x="410" y="104" width="230" height="132" rx="10" fill="#132030" stroke="#f0a04b" stroke-width="1.6"/><text x="525" y="130" text-anchor="middle" font-size="13.5" fill="#f0a04b">可變 mutable</text><text x="525" y="158" text-anchor="middle" font-size="12.5" fill="#e6edf3">List（列表）</text><text x="525" y="182" text-anchor="middle" font-size="12.5" fill="#e6edf3">Dictionary（字典）</text><text x="525" y="206" text-anchor="middle" font-size="12.5" fill="#e6edf3">Set（集合）</text><text x="350" y="242" text-anchor="middle" font-size="11.5" fill="#7ee787">「可變」指修改資料時會不會改變變數的引用位址</text></g><figcaption>圖：六種標準型別與可變／不可變分類。</figcaption></svg></figure>

## 2. Number（數字）

支援 `int`、`float`、`bool`、`complex`：

```
a, b, c, d = 20, 5.5, True, 4+3j
print(type(a), type(b), type(c), type(d))   # int float bool complex
```

- 也可用 `isinstance(x, int)` 判斷。
- 差異：`type()` 不把子類視為父類；`isinstance()` 會。

### 2.1 數字型別

- **int**：整數（Python 3 無大小限制，故沒有 Long）。
- **float**：浮點數，可用科學記號 `2.5e2`（=250）。
- **complex**：複數，如 `a + bj` 或 `complex(a, b)`。

數值型別**不可變**：改變值等於重新分配記憶體。

### 2.2 數字運算

- `/` 永遠回傳浮點數；`//` 取整、`%` 取餘、`**` 次方。

```
print(2 + 2)            # 4
print(50 - 5*6)         # 20
print((50 - 5*6) / 4)   # 5.0
print(17 / 3, 17 // 3, 17 % 3)   # 5.66.. 5 2
print(5 ** 2)           # 25
```

- `//` 的結果型別取決於運算元：`7//2 → 3`、`7.0//2 → 3.0`。
- 混合運算時整數會自動轉成浮點數。

### 2.3 型別轉換

把型別名稱當函式即可：`int(x)`、`float(x)`、`complex(x)`、`complex(x, y)`。

```
int(1.0)   # 1
```

## 3. String（字串）

- 用單引號或雙引號，`\` 轉義；前綴 `r` 為原始字串、`u` 為 Unicode。
- `+` 連接、`*` 重複。
- 索引：左起 `0`、右起 `-1`；切片 `[頭:尾]`（前閉後開）。
- 字串**不可變**（對索引賦值會報錯）。

```
s = 'Yes, he doesn\'t'
print(s, type(s), len(s))
print('C:\\some\\name')     # 反斜線會轉義
print(r'C:\\some\\name')    # 原始字串
word = 'Python'
print(word[0], word[-1])
print('ilovepython'[1:5])   # love
```

## 4. List（列表）

- 方括號、逗號分隔，元素可不同型別；可索引／切片；`+` 串接。
- 與字串不同：**元素可修改**；用 `del` 刪除。

```
a = ['him', 25, 100, 'her']
a[0] = 9          # 修改
del a[0]          # 刪除
print(a + [6, 7, 8])
```

## 5. Tuple（元組）

- 小括號、逗號分隔；**不可修改**；可索引／切片／`+` 串接。
- 單元素元組要加逗號：`(20,)`；空元組 `()`。
- 字串、list、tuple 都屬於 sequence（序列）。

```
tup = (1, 2, 3, 4, 5, 6)
print(tup[0], tup[1:5])
tup[0] = 11   # 非法：tuple 不支援元素賦值
```

## 6. Set（集合）

- 無序、不重複；用 `{}` 或 `set()` 建立（**空集合必須用 `set()`**，`{}` 是空字典）。
- 支援集合運算：`-` 差集、`|` 並集、`&` 交集、`^` 對稱差。

```
student = {'Tom', 'Jim', 'Mary', 'Tom'}   # 自動去重
a = set('abracadabra'); b = set('alacazam')
print(a - b, a | b, a & b, a ^ b)
```

## 7. Dictionary（字典）

- 無序的**鍵值對**集合：`{key: value}`。
- 鍵（key）必須**唯一且不可變**（字串、數字、元組）；值可為任意型別。
- 用 key 取值；`del` 刪除；另有 `keys()`、`values()`、`clear()` 等方法。

```
tel = {'Jack': 1557, 'Tom': 1320}
print(tel['Jack'])        # 取值
tel['Mary'] = 4127        # 新增／修改
del tel['Tom']            # 刪除
sorted(tel.keys())        # 依 key 排序
```

## 8. 運算符（Operator）

### 8.1 算術運算符

| 運算符 | 說明 |
| --- | --- |
| `+` `-` `*` `/` | 加、減、乘、除（`/` 回傳浮點數） |
| `%` | 取餘 |
| `**` | 次方 |
| `//` | 取整除法 |

### 8.2 比較運算符

`==`、`!=`、`<`、`>`、`<=`、`>=`；結果為 `True`／`False`（首字母大寫）。

### 8.3 賦值運算符

`=`、`+=`、`-=`、`*=`、`/=`、`%=`、`**=`、`//=`（如 `c += a` 等於 `c = c + a`）。

### 8.4 成員運算符

`in`／`not in`：判斷元素是否存在於序列中。

### 8.5 身分運算符

`is`／`is not`：判斷兩個變數是否指向同一個物件。

### 8.6 運算符優先級（高 → 低）

| 優先 | 運算符 |
| --- | --- |
| 1 | `()`、`[]`、`{}`（群組、索引、字典） |
| 2 | `x[i]`、`x[i:j]`、`x(...)`、`x.attr` |
| 3 | `**` |
| 4 | `+x`、`-x`、`~x` |
| 5 | `*`、`/`、`//`、`%`、`@` |
| 6 | `+`、`-` |
| 7 | `<<`、`>>` |
| 8 | `&` |
| 9 | `^` |
| 10 | `|` |
| 11 | `==`、`!=`、`<`、`<=`、`>`、`>=`、`in`、`is` |
| 12 | `not` |
| 13 | `and`、`or` |
