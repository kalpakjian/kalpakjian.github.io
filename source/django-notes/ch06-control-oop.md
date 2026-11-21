# 第 6 章 · 流程控制、函數、模組與面向對象

## 1. 條件控制（if / elif / else）

Python 用縮排區分區塊，條件後要加冒號 `:`。

```
if condition_1:
    statement_block_1
elif condition_2:
    statement_block_2
else:
    statement_block_3
```

- 條件為 `True` 才執行對應區塊。
- `elif` 等於其他語言的 `else if`。
- Python 沒有 `switch-case`，但 3.10 起提供 `match-case`。

### 1.1 match-case（Python 3.10+）

```
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case _:
            return "Unknown"
```

### 1.2 實例：猜數字

```
number, guess = 7, -1
while guess != number:
    guess = int(input("請輸入你要猜的數字："))
    if guess == number:
        print("猜中了！")
    elif guess < number:
        print("猜小了")
    else:
        print("猜大了")
```

## 2. 循環（while / for）

- **while**：條件為真時重複執行。

```
n, s, i = 100, 0, 1
while i <= n:
    s += i; i += 1
print(s)        # 5050
```

- **for**：遍歷序列（列表、字串等）。

```
for i in ['a', 'b', 'c']:
    print(i)
```

### 2.1 break / continue / else

- `break`：跳出迴圈（對應的 `else` 不執行）。
- `continue`：略過本次、進入下一輪。
- `else`：迴圈正常結束時執行（被 `break` 中斷則不執行）。

```
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            break
    else:
        print(n, 'is a prime number')
```

### 2.2 pass

`pass` 不做任何事，用於「語法上需要語句、但不想做事」之處：

```
while True:
    pass
```

## 3. 迭代器與生成器

- **迭代器**：記住走訪位置的物件，只能往前；用 `iter()` 建立、`next()` 取值。

```
it = iter([1, 2, 3, 4])
print(next(it), next(it))
```

- **生成器**：使用 `yield` 的函數；每次遇到 `yield` 會暫停並保存狀態，下次再從原處繼續。

```
def fibonacci(n):
    a, b, c = 0, 1, 0
    while c <= n:
        yield a
        a, b = b, a + b
        c += 1

for x in fibonacci(10):
    print(x, end=' ')
```

## 4. 函數（Function）

用 `def` 定義：

```
def hello():
    print("hello World!")

def area(width, height):
    return width * height
```

### 4.1 變數作用域

函數內為**局部**變數、函數外為**全域**變數；同名時函數內優先用局部。

```
a = 4            # 全域
def f1():
    a = 17       # 局部
    print(a)     # 17
def f2():
    print(a)     # 4
```

### 4.2 關鍵字參數

呼叫時可用 `名稱=值`，順序可調換：

```
def parrot(voltage, state='a stiff', action='voom'):
    ...

parrot(1000)
parrot(voltage=1000, action='VOOOOOM')
parrot(action='VOOOOOM', voltage=1000)
```

### 4.3 可變參數 *args

用 `*args` 接收不定個數的參數（打包成元組）：

```
def mean(*args):
    if not args:
        return 0
    return sum(args) / len(args)

print(mean(45, 32, 89))
```
## 5. 常用數據結構（複習）

### 5.1 列表（List）方法

| 方法 | 說明 |
| --- | --- |
| `append(x)` | 尾端加入元素 |
| `extend(L)` | 併入另一個列表 |
| `insert(i, x)` | 在位置 i 插入 |
| `remove(x)` | 刪除第一個值為 x 的元素 |
| `pop([i])` | 移除並回傳第 i 個（預設最後一個） |
| `clear()` | 清空 |
| `index(x)` / `count(x)` | 索引／出現次數 |
| `sort()` / `reverse()` | 排序／反轉 |
| `copy()` | 複製 |

### 5.2 當堆棧使用

`append()` 推入、`pop()` 彈出（後進先出）：

```
stack = [3, 4, 5]
stack.append(6)
stack.pop()
```

### 5.3 列表推導式

語法：`[運算式 for 變數 in 序列 (if 條件)]`

```
vec2 = [3*x for x in [2, 4, 6]]
fruits = [w.strip() for w in [' banana', ' loganberry']]
```

### 5.4 元組 / 集合 / 字典

- **元組**：`t = 1, 2, 3`，不可修改；輸出時會有括號。
- **集合**：`{}` 或 `set()`（空集合必須用 `set()`）；支援集合運算、去重。
- **字典**：`{key: value}`，無序鍵值對；可用 `dict()` 或字典推導建立。

```
tel = {'jack': 4098, 'sape': 4139}
tel['guido'] = 4127
print(tel['jack'], 'guido' in tel)
print(sorted(tel.keys()))

ccc = dict([('sape', 4139), ('guido', 4127)])
bbb = {x: x**2 for x in (2, 4, 6)}
aaa = dict(sape=4139, guido=4127)
```

## 6. 模組（Module）

模組就是一個 `.py` 檔（含函數與變數），可被其他程式引入。

```
import sys
print(sys.argv)     # 命令列參數（列表）
print(sys.path)     # 模組搜尋路徑（列表）
```

### 6.1 匯入方式

```
import module1, module2            # 匯入整個模組
from modname import name1, name2   # 匯入指定部分
from modname import *              # 匯入全部（少用）
```

一個模組只會被匯入一次；搜尋路徑由 `sys.path` 決定，可用它引入不在路徑中的模組。

### 6.2 __name__ 屬性

模組被引入時 `__name__` 為模組名；直接執行時為 `'__main__'`。常用來區分「被引入」與「直接執行」：

```
if __name__ == '__main__':
    print('程式自身在執行')
else:
    print('我來自另一模組')
```

### 6.3 dir()

`dir(模組)` 會以字串列表回傳該模組定義的所有名稱。

## 7. 錯誤與異常

- **語法錯誤（SyntaxError）**：程式還沒執行就被檢查出來，例如少了冒號。
- **異常（Exception）**：語法正確、但執行時出錯：

| 異常 | 原因 |
| --- | --- |
| `ZeroDivisionError` | 除以零 |
| `NameError` | 使用未定義的名稱 |
| `TypeError` | 型別不符（如 `'2' + 2`） |

## 8. 面向對象（OOP）

### 8.1 基本名詞

- **類（Class）**：物件的藍圖，定義屬性與方法。
- **物件（Object）**：類的實例。
- **類變數**：所有實例共用；**實例變數**：各實例自有。
- **方法**：類中定義的函數。
- **繼承**：子類取得父類的欄位與方法，並可**重寫（override）**。

### 8.2 類定義與實例化

```
class MyClass:
    i = 12345
    def f(self):
        return 'hello world'

x = MyClass()
print(x.i, x.f())
```

`__init__(self)` 是建構方法，建立物件時初始化狀態。

### 8.3 繼承

以 `class 子類(父類)` 定義；找不到的方法往父類找。也支援**多重繼承** `class C(A, B)`。

```
class people:
    def __init__(self, n, a):
        self.name, self.age = n, a
    def speak(self):
        print(self.name, self.age)

class student(people):
    def __init__(self, n, a, g):
        people.__init__(self, n, a)   # 呼叫父類建構
        self.grade = g
    def speak(self):                  # 重寫父類方法
        print(self.name, self.age, self.grade)

s = student('ken', 10, 3)
s.speak()
```

### 8.4 類的專屬方法（魔術方法）

`__init__`（建構）、`__del__`（解構）、`__repr__`（列印）、`__len__`（長度）、`__add__` / `__sub__` / `__mul__`（運算）等。

## 9. 主流 Python 框架

| 框架 | 特色 | 適用場景 |
| --- | --- | --- |
| **Django** | 全功能、「電池全備」：ORM、表單、認證、後台 | 中大型、複雜的 Web 應用 |
| **Flask** | 輕量、可擴充、彈性高 | 小型專案、快速原型、單人開發 |
| **Tornado** | 非阻塞、高擴展、低延遲 | 高併發、即時通訊、即時資料處理 |
| **Bottle** | 極輕量、低依賴 | 小型應用、RESTful API |
| **web2py** | 全堆棧、強調簡單與安全 | 中大型、重視安全性的專案 |

### 9.1 FastAPI vs Django

- **性能**：FastAPI 為非同步框架，高併發下較快；Django 為同步框架，穩定但較慢。
- **易用性**：Django 內建功能多、上手快；FastAPI 極簡、彈性高。
- **擴展性**：Django 生態成熟、第三方庫多；FastAPI 生態成長中，API 開發競爭力強。
- **選擇建議**：要高效能 API → FastAPI；要功能完備的網站 → Django。

**參考資料**：https://www.w3cschool.cn/python3/
