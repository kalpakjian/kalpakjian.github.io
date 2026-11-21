# 第 3 章 · Python3 基礎語法

## 1. 基礎規則

### 1.1 編碼

Python 3 原始碼預設為 **UTF-8**，字串皆為 Unicode。若要指定其他編碼：

```
# -*- coding: cp-1252 -*-
```

### 1.2 標識符（識別字）

命名規則：

- 第一個字元必須是字母或底線 `_`。
- 其餘可為字母、數字、底線。
- 區分大小寫。
- Python 3 允許非 ASCII 標識符。

### 1.3 保留字（關鍵字）

保留字不可作為標識符。可用 `keyword` 模組查詢：

```
import keyword
print(keyword.kwlist)
```

### 1.4 註釋

- **單行**：以 `#` 開頭。

```
# 這是單行註釋
```

- **多行**：用三個單引號或三個雙引號包住。嚴格說 Python 只有單行註釋，三引號其實是「多行字串」。

### 1.5 縮進

Python 用**縮排**表示程式區塊；同一區塊的縮排空格數必須一致。

```
def hi():
    print('hi')  # 縮排
```

## 2. 數據類型

### 2.1 六種標準類型

- **不可變（3 種）**：Number（數字）、String（字串）、Tuple（元組）。
- **可變（3 種）**：List（列表）、Dictionary（字典）、Set（集合）。

### 2.2 可變 vs 不可變

「可變」指的是**修改資料時會不會改變變數的引用位址**：

- **不可變**：改變值等於新建物件；相同值的物件以引用計數共用。
- **可變**：修改只改變值、不改引用位址；同值的不同物件各自佔一份記憶體。

### 2.3 類型判斷

用 `type()` 查看型別：

```
isStr = "餅瑞瑪"; print(type(isStr))
isInt = 1000;      print(type(isInt))
isTuple = ('德瑪', '20', 'x'); print(type(isTuple))
isList = ['d', '4', '垃圾'];   print(type(isList))
```

### 2.4 字串（String）重點

- 單引號與雙引號等價，但不可混用。
- 三引號可包多行字串。
- `\` 為轉義字元；前綴 `r`/`R` 表示自然字串（`\n` 不換行）。
- 前綴 `u`/`U` 表示 Unicode 字串。
- 字串**不可變**；沒有獨立字元型別（一個字元＝長度 1 的字串）。
- 相鄰字串字面值會自動串接；用 `+` 連接、`*` 重複。
- 索引：左起 `0`、右起 `-1`；切片語法 `變數[頭:尾:步長]`。

## 3. 輸入與輸出

### 3.1 輸入 input()

`input([提示字串])` 會印出提示並讀取輸入，按 Enter 後才繼續；輸入結果一律是字串。

```
x = input("輸入吧，少年：")
print(x)
print(type(x))
```

### 3.2 輸出 print()

`print()` 是基本輸出函式：

```
print("Hello, World!")
str = "Hello, World!"
print(str)
```

### 3.3 同一行寫多條語句

語句之間用分號 `;` 分隔：

```
import sys; x = 'nothing'; sys.stdout.write(x + '\n')
```

## 4. 模組與程式區塊

### 4.1 import 與 from…import

- 匯入整個模組：`import somemodule`
- 匯入單一函式：`from somemodule import somefunction`
- 匯入多個函式：`from somemodule import firstfunc, secondfunc, thirdfunc`
- 匯入全部：`from somemodule import *`

### 4.2 程式區塊（suite）

縮排相同的一組語句構成「程式區塊」。`if`、`while`、`def`、`class` 等複合語句以關鍵字開頭、以冒號 `:` 結尾，其後縮排的程式碼即為該區塊：

```
if expression:
    suite
elif expression:
    suite
else:
    suite
```

## 5. 第一個程式：Fibonacci 數列

```
a, b = 0, 1
while b < 10:
    print(b)
    a, b = b, a + b
```

`a, b = b, a + b` 會**先算右邊、再同時賦值**，等價於：

```
n = b
m = a + b
a = n
b = m
```
