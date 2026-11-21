# 第 6 章 · 流程控制、函數、模組與面向對象

運行結果：

清空集合

語法格式如下：

```
s.clear()
```
清空集合 s。

實例：

```
thisset = set(("s", "ss", "sss"))
thisset.clear()
print(thisset)
```
運行結果：

```
set()
```
## 判斷元素是否在集合中存在

判斷元素 x 是否在集合 s 中，存在則返回 True，不存在則返回 False。實例：

```
thisset = set(("s", "ss", "sss"))
print("ss" in thisset)
print("sssss" in thisset)
```
運行結果：

```
True
False
```
## Python3 條件控制

if 語句 Python 條件語句是通過一條或多條語句的執行結果(True 或者 False)來決定執行的代碼塊Python 中 if 語句的一般形式如下所示：

```
if condition_1:
    statement_block_1
```
流程圖如下所示：

這種 if 語句只有在符合條件的時候才會執行代碼塊內的代碼，是一種比較常見的用法。另一種常見的用法是：

```
if condition_1:
    statement_block_1
else:
    statement_block_2
```
流程圖如下所示：

這種語句是一種常用的 if-else 語句，通常用於二分支結構的條件語句代碼。

在一些時候，我們可能需要多分支的條件語句代碼，可以在 if-else 語句中混合 elif 語句進行使用：

Python 中用elif 代替了else if，所以if語句的關鍵字為：if - elif - else。

```
if condition_1:
    statement_block_1
elif condition_2:
    statement_block_2
else:
    statement_block_3
```
流程圖如下所示：

如果"condition_1" 為 True 將執行"statement_block_1" 塊語句，如果"condition_1" 為 False，將判斷"condition_2"，如果"condition_2" 為 True 將執行"statement_block_2" 塊語句，如果"condition_2" 為 False，將執行"statement_block_3" 塊語句。

使用第一種常用的 if 語句搭配合適的條件可以實現第二種和第三種語句的全部效果，但在執行效率和代碼可讀性上會變得比較糟糕。

注意：

每個條件後面要使用冒號(:)，表示接下來是滿足條件後要執行的語句塊。

使用縮進來劃分語句塊，相同縮進數的語句在一起組成一個語句塊。

在 Python 中沒有 switch - case 語句，但在 python3 中添加了用法類似的 match-case 語句。

match-case 語句(python3.10 新特性)

在其他語言(比如說經典的 C 語言)中有一種多分支條件判斷語句，可以進行模式匹配(通俗的講，就是將傳入的內容跟多個已存在的樣例進行比較，找到相同的案例並按照該案例的代碼進行處理，如果沒有相同案例就按默認案例進行處理，可以查看其他編程語言的條件語句的 Switch 相關部分內容進行比較參考)。在 python3.10 中也引入了這樣的新特性。

一個 match 語句的使用示例：

```
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong with the Internet"
```
上述代碼等價於：

```
def http_error(status):
    if status == 400:
        return "Bad request"
    elif status == 404:
        return "Not found"
    elif status == 418:
        return "I'm a teapot"
    else:
        return "Something's wrong with the Internet"
```
以下為 if 中常用的操作運算符:


| 操作符 | 描述 |
| --- | --- |
| &lt; | 小於 |
| &lt;= | 小於或等於 |
| &gt; | 大於 |
| &gt;= | 大於或等於 |
| \*\* | 等於,比較對像是否相等 |
| != | 不等於 |


## 實例

```
print(5 == 6)
# 使用變量
x = 5
y = 8
print(x == y)
number = 7
guess = -1
print("猜數字！")
while guess != number:
    guess = int(input("請輸入你要猜的數字"))
    if guess == number:
        print("你猜中了，真厲害！")
    elif guess < number:
        print("猜小了，再猜猜？")
    elif guess > number:
        print("猜大了，在猜猜？")
```
Python3 循環

介紹 Python 循環語句的使用。

Python 中的循環語句有 for 和 while。

Python 循環語句的控制結構圖如下所示：

## while 循環

Python 中 while 語句的一般形式：

while 判斷條件：

```
statements
```
同樣需要注意冒號和縮進。另外，在 Python 中沒有 do-while 循環。以下實例使用了 while 來計算 1 到 100 的總和：

```
n = 100
sum = 0
counter = 1
while counter <= n:
    sum = sum + counter
    counter += 1
    print('Sum of 1 until %d: %d' % (n,sum))
```
執行結果如下：

```
Sum of 1 until 100: 5050
```
for 語句

Python for 循環可以遍歷任何序列的項目，如一個列表或者一個字符串。

for 循環的一般格式如下：

```
for in :
else:
    pass  # 內容省略
```
Python for 循環實例：

```
DC = ['BvS', '水水俠', '神奇女俠', '大超回歸']
for x in DC:
    print(x)
```
執行結果如下：

```
BvS
```
水水俠

神奇女俠

大超回歸

range()函數

如果你需要遍歷數字序列，可以使用內置 range() 函數。它會生成數列，例如：

```
for i in range(10):
    print(i)
    # 你也可以使用range 指定區間的值：
    for i in range(5,9):
        print(i)
        #也可以使range 以指定數字開始並指定不同的增量
        for i in range(0, 10, 3):
            print(i)
            #負數：
            for i in range(-10, -100, -30):
                print(i)
```
您可以結合 range() 和 len() 函數以遍歷一個序列的索引，如下所示：

```
#--- range() + len()
aa = ['a', 's', 'd', 'f', 'g']
for i in range(len(aa)):
    print(i, aa[i])
```
可以使用 range() 函數來創建一個列表：

```
pp = list(range(5))
print(pp)
```
break 和 continue 語句及循環中的 else 子句

break 語句可以跳出 for 和 while 的循環體。如果你從 for 或 while 循環中終止，任何對應的循環 else 塊將不執行。

continue 語句被用來告訴 Python 跳過當前循環中的當此循環，然後繼續進行下一輪循環。

循環語句可以有 else 子句；它在窮盡列表(以 for 循環)或條件變為假(以 while 循環)循環終止時被執行，但循環被 break 終止時不執行，如下查尋質數的循環例子：

```
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '**', n//x)
            break
        else:
            # 循環中沒有找到元素
            print(n, 'is a prime number')
```
## pass 語句

pass 語句什麼都不做。它只在語法上需要一條語句但程序不需要任何操作時使用。例如：

```
while True:
    pass
```
最小的類：

```
class MyEmptyClass:
    pass
```
Python3 迭代器與生成器 - 迭代器迭代是 Python 最強大的功能之一，是訪問集合元素的一種方式。

迭代器是一個可以記住遍歷的位置的對象。

迭代器對像從集合的第一個元素開始訪問，直到所有的元素被訪問完結束。迭代器只能往前不會後退。

迭代器有兩個基本的方法：iter()和next()。

字符串，列表或元組對像都可用於創建迭代器：

```
list = [1, 2, 3, 4]
it = iter(list)
print(next(it))
print(next(it))
```
迭代器對象可以使用常規 for 語句進行遍歷：

```
list = [1, 2, 3, 4]
it = iter(list) # 創建迭代器對象
for x in it:
    print(x, end="")
```
## 生成器

在 Python 中，使用了 yield 的函數被稱為生成器(generator)。跟普通函數不同的是，生成器是一個返回迭代器的函數，只能用於迭代操作，更簡單點理解生成器就是一個迭代器。在調用生成器運行的過程中，每次遇到 yield 時函數會暫停並保存當前所有的運行信息，返回 yield 的值。並在下一次執行 next() 方法時從當前位置繼續運行。

以下實例使用 yield 實現斐波那契數列：

```
import sys
```
def fibonacci(n): # 生成器函數 - 斐波那契

```
a, b, counter = 0, 1, 0
while True:
    if (counter > n):
        return
        yield a
        a, b = b, a + b
        counter += 1
        f = fibonacci(10) # f 是一個迭代器，由生成器返回生成
        while True:
            try:
                print (next(f), end="")
            except StopIteration:
                sys.exit()
```
Python3 函數

本章節我們將為大家介紹 Python 中函數的應用。

Python 定義函數使用 def 關鍵字，一般格式如下：

def 函數名（參數列表）：

函數體讓我們使用函數來輸出"Hello World!"：

```
def hello():
    print("hello World!")
    hello()
```
更複雜點的應用，函數中帶上參數變量：

```
def area(width, height):
    return width * height
def print_welcome(name):
    print("Welcome", name)
    print_welcome("Fred")
    w = 4
    h = 5
    print("width =", w, " height =", h, " area =", area(w, h))
```
輸出結果：

```
Welcome Fred
width = 4 height = 5 area = 20
```
## 函數變量作用域

定義在函數內部的變量擁有一個局部作用域，定義在函數外的擁有全局作用域。通過以下實例，你可以清楚瞭解 Python 函數變量的作用域：

```
a = 4 # 全局變量
def print_func1():
    a = 17 # 局部變量
    print("in print_func a = ", a)
def print_func2():
    print("in print_func a = ", a)
    print_func1()
    print_func2()
    print("a = ", a)
```
運行結果：

```
in print_func a = 17
in print_func a = 4
a = 4
```
## 關鍵字參數

函數也可以使用 kwarg = value 的關鍵字參數形式被調用。例如，以下函數：

```
def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    print("-- This parrot wouldn't", action, end='')
    print("if you put", voltage, "volts through it.")
    print("-- Lovely plumage, the", type)
    print("-- It's", state, "!")
```
可以以下幾種方式被調用：

```
parrot(1000) # 1 positional argument
parrot(voltage=1000) # 1 keyword argument
parrot(voltage=1000000, action='VOOOOOM') # 2 keyword arguments
parrot(action='VOOOOOM', voltage=1000000) # 2 keyword arguments
parrot('a million', 'bereft of life', 'jump') # 3 positional arguments
parrot('a thousand', state='pushing up the daisies') # 1 positional, 1 keyword
```
以下為錯誤調用方法：

```
parrot() # required argument missing
parrot(voltage=5.0, 'dead') # non-keyword argument after a keyword argument
parrot(110, voltage=220) # duplicate value for the same argument
parrot(actor='John Cleese') # unknown keyword argument
```
## 返回值

Python 函數使用 return 語句返回函數值，可以將函數作為一個值賦值給指定變量：

```
def return_sum(x,y):
    c = x + y
    return c
    res = return_sum(4,5)
    print(res)
```
## 可變參數列表

最後，一個較不常用的功能是可以讓函數調用可變個數的參數。

這些參數被包裝進一個元組(查看元組和序列)。

在這些可變個數的參數之前，可以有零到多個普通的參數：

```
def arithmetic_mean(*args):
    if len(args) == 0:
        return 0
    else:
        sum = 0
        for x in args:
            sum += x
            return sum / len(args)
            print(arithmetic_mean(45,32,89,78))
            print(arithmetic_mean(8989.8,78787.78,3453,78778.73))
            print(arithmetic_mean(45,32))
            print(arithmetic_mean(45))
            print(arithmetic_mean())
```
## Python3 數據結構

## 列表

Python 中列表是可變的，這是它區別於字符串和元組的最重要的特點，一句話概括即：列表可以修改，而字符串和元組不能修改。以下是 Python 中列表的方法：


| 方法 | 描述 |
| --- | --- |
| list.append(x) | 把一個元素添加到列表的結尾，相當於a[len(a):] = [x]。 |
| list.extend(L) | 通過添加指定列表的所有元素來擴充列表，相當於a[len(a):] = L。 |
| list.insert(i, x) | 在指定位置插入一個元素。第一個參數是準備插入到其前面的那個元素的索引，例如a.insert(0, x)會插入到整個列表之前，而a.insert(len(a), x)相當於a.append(x)。 |
| list.remove(x) | 刪除列表中值為x的第一個元素。如果沒有這樣的元素，就會返回一個錯誤。 |
| list.pop([i]) | 從列表的指定位置刪除元素，並將其返回。如果沒有指定索引，a.pop()返回最後一個元素。元素隨即從列表中被刪除。（方法中i兩邊的方括號表示這個參數是可選的，而不是要求你輸入一對方括號，你會經常在Python庫參考手冊中遇到這樣的標記。） |
| list.clear() | 移除列表中的所有項，等於del a[i]。 |
| list.index(x) | 返回列表中第一個值為x的元素的索引。如果沒有匹配的元素就會返回一個錯誤。 |
| list.count(x) | 返回x在列表中出現的次數。 |
| list.sort() | 對列表中的元素進行排序。 |
| list.reverse() | 倒排列表中的元素。 |
| list.copy() | 返回列表的滾複製，等於a[i]。 |
| 下面示例演示了列表的大部分方法： |


```
a = [66.25, 333, 333, 1, 1234.5]
print(a.count(333), a.count(66.25), a.count('x'))
a.insert(2, -1)
a.append(333)
print(a)
print(a.index(333))
a.remove(333)
print(a)
a.reverse()
print(a)
a.sort()
print(a)
```
注意：類似 insert, remove 或 sort 等修改列表的方法沒有返回值。

## 將列表當做堆棧使用

列表的方法使得列表可以很方便的作為一個堆棧來使用，堆棧作為特定的數據結構，最先進入的元素會最後一個被釋放(後進先出)。用 append() 方法可以把一個元素添加到堆棧頂。用不指定索引的 pop() 方法可以把一個元素從堆棧頂釋放出來。例如：

```
stack = [3, 4, 5]
stack.append(6)
stack.append(7)
print(stack)
stack.pop()
print(stack.pop())
print(stack)
stack.pop()
print(stack.pop())
print(stack)
stack.pop()
print(stack.pop())
print(stack)
print(stack)
```
## 列表推導式

列表推導式提供了從序列創建列表的簡單途徑。通常應用程序將一些操作應用於某個序列的每個元素，用其獲得的結果作為生成新列表的元素，或者根據確定的判定條件創建子序列。

每個列表推導式都在 for 之後跟一個表達式，然後有零到多個 for 或 if 子句。返回結果是一個根據表達從其後的 for 和 if 上下文環境中生成出來的列表。如果希望表達式推導出一個元組，就必須使用括號。

語法格式：

結果值1 if 判斷條件 else 結果2 for 變量名 in 原列表

這裡我們將列表中每個數值乘三，獲得一個新的列表：

```
vec = [2, 4, 6]
vec2 = [3*x for x in vec]
print(vec2)
```
這裡我們對序列裡每一個元素逐個調用某方法：

```
freshfruit = [' banana', ' loganberry', ' passion fruit']
freshfruit2 = [weapon.strip() for weapon in freshfruit]
print(freshfruit2)
```
## 嵌套列表解析

Python 的列表還可以嵌套。以下實例展示了 $ 3 \times 4 $ 的矩陣列表：

```
matrix = [
,
,
,
]
```
以下實例將3 * 4 的矩陣列表轉換為4 * 3 列表：

```
#兩個方法
list1 = [[row[i] for row in matrix] for i in range(4)]
print(list1)
transposed = []
for i in range(4):
    transposed.append([row[i] for row in matrix])
    print(transposed)
```
元組和序列

元組由若干逗號分隔的值組成，例如：

```
t = 12345, 54321, 'hello!'
print(t[0])
print(t)
# tuples
u = t, (1, 2, 3, 4, 5)
print(u)
```
如你所見，元組在輸出時總是有括號的，以便於正確表達嵌套結構。在輸入時可能有或沒有括號，不過括號通常是必須的(如果元組是更大的表達式的一部分)。

集合

集合是一個無序不重複元素的集。基本功能包括關係測試和消除重複元素。

可以用大括號({}) 創建集合。注意:如果要創建一個空集合,你必須用 set() 而不是{}；後者創建一個空的字典，下一節我們會介紹這個數據結構。

以下是一個簡單的演示：

```
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
print(basket)
print('orange' in basket)
print('crabgrass' in basket)
a = set('abracadabra')
b = set('alacazam')
print(a)
print(a - b)
print(a | b)
print(a & b)
print(a ^ b)
aa = {x for x in 'abracadabra' if x not in 'abc'}
print(aa)
```
字典

另一個非常有用的 Python 內建數據類型是字典。

序列是以連續的整數為索引，與此不同的是，字典以關鍵字為索引，關鍵字可以是任意不可變類型，通常用字符串或數值。

理解字典的最佳方式是把它看做無序的鍵=> 值對集合。在同一個字典之內，關鍵字必須是互不相同。

一對大括號創建一個空的字典：{}。

這是一個字典運用的簡單例子：

```
tel = {'jack': 4098, 'sape': 4139}
tel['guido'] = 4127
print(tel)
print(tel['jack'])
del tel['sape']
tel['irv'] = 4127
print(tel)
print(list(tel.keys()))
print(sorted(tel.keys()))
print('guido' in tel)
print('jack' not in tel)
#構造函數dict()直接從鍵值對元組列表中構建字典·如果有固定的模式，列表推聯式指定特定的鍵值對：
ccc = dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
print(ccc)
# 字典推導可以用來創建任意鍵和值的表達式詞典：
bbb = {x: x**2 for x in (2, 4, 6)}
print(bbb)
#如果鍵字只是整單的字符串，使用鍵字參數指定鍵值對有時候更方便：
aaa = dict(sape=4139, guido=4127, jack=4098)
```
Python3(模塊)

模塊是一個包含所有你定義的函數和變量的文件，其後綴名是.py。模塊可以被別的程序引入，以使用該模塊中的函數等功能。這也是使用 Python 標準庫的方法。下面是一個使用 Python 標準庫中模塊的例子。

```
import sys
print('命令行參數如下：')
for i in sys.argv:
    print(i)
    print('\\n\\nPython 路徑為：', sys.path, '\\n')
```
1、import sys 引入 Python 標準庫中的 sys.py 模塊；這是引入某一模塊的方法。

2、sys.argv 是一個包含命令行參數的列表。

3、sys.path 包含了一個 Python 解釋器自動查找所需模塊的路徑的列表。

## import 語句

如果要使用 Python 源文件，只需在另一個源文件裡執行 import 語句，import 語句語法如下：

```
import module1, module2, module3
```
當解釋器遇到 import 語句，如果模塊在當前的搜索路徑就會被導入。

搜索路徑是一個解釋器會先進行搜索的所有目錄的列表。如果想要導入模塊 support，需要把命令放在腳本的頂端：

```
# filename: support.py
def print_func( par ):
    print("Hello : ", par)
    return
```
(support.py) index.py 引入 support 模塊：

```
import support
support.print_func('okok')
```
一個模塊只會被導入一次，不管你執行了多少次 import。這樣可以防止導入模塊被一遍又一遍地執行。

當我們使用 import 語句的時候，Python 解釋器是怎樣找到對應的文件的呢？這就涉及到 Python 的搜索路徑，搜索路徑是由一系列目錄名組成的，Python 解釋器就依次從這些目錄中去尋找所引入的模塊。

因此若像我一樣在當前目錄下存在與要引入模塊同名的文件，就會把要引入的模塊屏蔽掉。

瞭解了搜索路徑的概念，就可以在腳本中修改 sys.path 來引入一些不在搜索路徑中的模塊。

代碼如下： fibo.py

def fib(n): # 定義到 n 的斐波那契數列

```
a, b = 0, 1
while b < n:
    print(b, end='')
    a, b = b, a + b
    print()
```
def fib2(n): # 返回到 n 的斐波那契數列

```
result = []
a, b = 0, 1
while b < n:
    result.append(b)
    a, b = b, a + b
    return result
```
導入這個 fibo 模塊：

```
import fibo
fibo.fib(10)
print(fibo.fib2(20))
print(fibo.__name__)
```
## from ... import 語句

Python 的 from 語句讓你從模塊中導入一個指定的部分到當前命名空間中，語法如下：

```
from modname import name1, name2, name3
```
例如，要導入模塊 fibo 的 fib 函數，使用如下語句：

```
from fibo import fib, fib2
```
這個聲明不會把整個 fibo 模塊導入到當前的命名空間中，它只會將 fibo 裡的 fib 函數引入進來。

from ... import * 語句

把一個模塊的所有內容全都導入到當前的命名空間也是可行的，只需使用如下聲明：

```
from modname import *
```
這提供了一個簡單的方法來導入一個模塊中的所有項目。然而這種聲明不該被過多的使用。

## _name_屬性

一個模塊被另一個程序第一次引入時，其主程序將運行。如果我們想在模塊被引入時，模塊中的某一程序塊不執行，我們可以用_name_屬性來使該程序塊僅在該模塊自身運行時執行。

```
if __name__ == '__main__':
    print('程序自身在通行')
else:
    print('我來自另一模塊')
```
每個模塊都有一個_name_屬性，當其值是'main'時，表明該模塊自身在運行，否則是被引入。

每個_name_與_main底下是雙下劃線，是“__”去掉中間的空格。

```
dir()
#內置的函數 dir() 可以找到模塊內定義的所有名稱，以一個字符串列表的形式返回：
import fibo, sys
print(dir(fibo))
print(dir(sys))
```
## Python3 錯誤和異常

作為 Python 初學者，在剛學習 Python 編程時，經常會看到一些報錯信息 Python 有兩種錯誤很容易辨認：語法錯誤和異常。

語法錯誤

Python 的語法錯誤或者稱之為解析錯，是初學者經常碰到的，如下實例

```
while True print('Hello world')
File " ", line 1, in ?
while True print('Hello world')
^
SyntaxError: invalid syntax
```
這個例子中，函數 print() 被檢查到有錯誤，是它前面缺少了一個冒號(:)。

語法分析器指出了出錯的一行，並且在最先找到的錯誤的位置標記了一個小小的箭頭。

## 異常

即便 Python 程序的語法是正確的，在運行它的時候，也有可能發生錯誤。運行期檢測到的錯誤被稱為異常。

大多數的異常都不會被程序處理，都以錯誤信息的形式展現在這裡：

>>> 10 * (1/0)

```
Traceback (most recent call last):
File " ", line 1, in ?
ZeroDivisionError: division by zero
```
>>> 4 + spam*3

```
Traceback (most recent call last):
File " ", line 1, in ?
NameError: name 'spam' is not defined
```
>>> '2' + 2

```
Traceback (most recent call last):
File " ", line 1, in ?
TypeError: Can't convert 'int' object to str implicitly
```
異常以不同的類型出現，這些類型都作為信息的一部分打印出來：例子中的類型有

ZeroDivisionError, NameError 和 TypeError。

錯誤信息的前面部分顯示了異常發生的上下文，並以調用棧的形式顯示具體信息。

## Python3 面向對象

Python 從設計之初就是一門面向對象的語言，正因為如此，在 Python 中創建一個類和對像是很容易的。簡單的瞭解下面向對象的一些基本特徵。

## Python3 面向對象技術簡介

類(Class): 用來描述具有相同的屬性和方法的對象的集合。它定義了該集合中每個對象所共有的屬性和方法。對像是類的實例。

類變量：類變量在整個實例化的對像中是公用的。類變量定義在類中且在函數體之外。類變量通常不作為實例變量使用。

數據成員：類變量或者實例變量用於處理類及其實例對象的相關的數據。

方法重寫：如果從父類繼承的方法不能滿足子類的需求，可以對其進行改寫，這個過程叫方法的覆蓋(override)，也稱為方法的重寫。

局部變量：定義在方法中的變量，只作用於當前實例的類。

實例變量：在類的聲明中，屬性是用變量來表示的。這種變量就稱為實例變量，是在類聲明的內部但是在類的其他成員方法之外聲明的。

繼承：即一個派生類(derived class)繼承基類(base class)的字段和方法。繼承也允許把一個派生類的對像作為一個基類對像對待。例如，有這樣一個設計：一個 Dog 類型的對象 派生自 Animal 類，這是模擬"是一個(is-a) "關係(例圖，Dog 是一個 Animal)。

實例化：創建一個類的實例，類的具體對象。

方法：類中定義的函數。

對象：通過類定義的數據結構實例。對象包括兩個數據成員(類變量和實例變量)和方法。

類定義

```
class ClassName:
# <statement-1>
# .
# .
# .
# <statement-N>
    pass  # 內容省略
```
類實例化後，可以使用其屬性，實際上，創建一個類之後，可以通過類名訪問其屬性。

## 類對象

類對象支持兩種操作：屬性引用和實例化。

屬性引用使用和 Python 中所有的屬性引用一樣的標準語法：obj.name。

類對象創建後，類命名空間中所有的命名都是有效屬性名。所以如果類定義是這樣：

```
class MyClass:
    pass  # 內容省略
```
"""一個簡單的類實例"""

```
i = 12345
def f(self):
    return 'hello world'
    # 實例化類
    x = MyClass()
    # 訪問類的屬性和方法
    print("MyClass 類的屬性 i 為：", x.i)
    print("MyClass 類的方法 f 輸出為：", x.f())
```
實例化類：

```
# 實例化類
x = MyClass()
# 訪問類的屬性和方法
```
以上創建了一個新的類實例並將該對象賦給局部變量 x，x 為空的對象。

執行以上程序輸出結果為：

MyClass 類的屬性 i 為：12345

MyClass 類的方法 f 輸出為：hello world

很多類都傾向於將對象創建為有初始狀態的。因此類可能會定義一個名為_init_()的特殊方法（構造方法），像下面這樣：

```
def _init_(self):
    self.data = []
```
## 繼承

Python 同樣支持類的繼承，如果一種語言不支持繼承，類就沒有什麼意義。派生類的定義如下所示：

```
class DerivedClassName(BaseClassName):
# <statement-1>
# .
# .
# .
# <statement-N>
    pass  # 內容省略
```
需要注意圓括號中基類的順序，若是基類中有相同的方法名，而在子類使用時未指定，Python 從左至右搜索即方法在子類中未找到時，從左到右查找基類中是否包含方法。

BaseClassName (示例中的基類名)必須與派生類定義在一個作用域內。除了類，還可以用表達式，基類定義在另一個模塊中時這一點非常有用：

```
class DerivedClassName(modname.BaseClassName):
    pass  # 內容省略
```
實例

```
# 類定義
class people:
    # 定義基本屬性
    name = ''
    age = 0
    # 定義私有屬性，私有屬性在額外部無法直接進行訪問
    _weight = 0
    # 定義構造方法
def __init__(self, n, a, w):
    self.name = n
    self.age = a
    self._weight = w
def speak(self):
    print("%s 說：我 %d 處：" %(self.name, self.age))
    #單獨承示例
class student(people):
    grade = ''
def __init__(self, n, a, w, g):
    # 調用父類的構造
    people.__init__(self, n, a, w)
    self.grade = g
    # 覆為父類的方法
def speak(self):
    print("%s 說：我 %d 處了，我在讀 %d 年級"%(self.name, self.age, self.grade))
    s = student('ken', 10, 60, 3)
    s.speak()
```
多繼承

Python 同樣有限的支持多繼承形式。多繼承的類定義形如下例：

```
class DerivedClassName(Base1, Base2, Base3):
# <statement-1>
# .
# .
# .
# <statement-N>
    pass  # 內容省略
```
需要注意圓括號中父類的順序，若是父類中有相同的方法名，而在子類使用時未指定，Python從左至右搜索即方法在子類中未找到時，從左到右查找父類中是否包含方法。

```
# 鎖定義
class people:
    #定義基本屬性
    name = ''
    age = 0
    #定義私有屬性，私有屬性在標外部無法直接進行訪問
    _weight = 0
    #定義構造方法
def _init_(self, n, a, w):
    self.name = n
    self.age = a
    self._weight = w
def speak(self):
    print("%s 說：我 %d 處：" %(self.name, self.age))
    #單維承示例
class student(people):
    grade = ''
def _init_(self, n, a, w, g):
    # 調用父類的構造
    people._init_(self, n, a, w)
    self.grade = g
    # 覆商父類的方法
def speak(self):
    print("%s 說：我 %d 處了，我在讀 %d 年級" % (self.name, self.age, self.grade))
```
## 方法重寫

如果你的父類方法的功能不能滿足你的需求，你可以在子類重寫你父類的方法，實例如下：

class Parent: # 定義父類

```
def myMethod(self):
    print('調用父類方法')
```
class Child(Parent): # 定義子類

```
def myMethod(self):
    print('調用子類方法')
    c = Child() # 子類實例
```
c.myMethod() # 子類調用重寫方法

類的專屬方法：

- __init__：構造函數，在生成對象時調用

- __del__：析構函數，釋放對象時使用

- __repr__：打印，轉換

- __setitem__：按照索引賦值

- getitem：按照索引獲取值

- __len__：獲得長度

- __cmp__：比較運算

- __call__：函數調用

- __add__：加運算

- __sub__：減運算

- __mul__：乘運算

- __div__：除運算

- __mod__：求餘運算

- __pow__：乘方

參考資料：

```
https://www.w3cschool.cn/python3/
```
## 識別主流 Python 框架的功能及應用場景

以下是一些主流的 Python 框架及其功能和應用場景的簡要描述：

1) Django

功能：Django 是一個全功能的、高級的 Python Web 框架，提供了許多內置的功能和工具，包括 ORM(對象關係映射)、表單處理、身份驗證、管理後臺等。

應用場景：Django 適用於構建複雜而大型的 Web 應用程式，尤其是需要快速發展和高效率開發的場景。它適用於中大型團隊合作開發，並在安全性、可維護性和擴展性方面具有優勢。

2) Flask :

功能： Flask 是一個輕量級的 Python Web 框架，提供了基本的功能和核心組件，同時具有可擴展性和靈活性。

應用場景：Flask 適用於簡單而輕量的 Web 應用程式，特別是在快速原型開發、小型項目或單個開發者的場景中。它以其簡單易用和高度可定製的特點受到許多開發者的歡迎。

3) Tornado :

功能：Tornado 是一個非阻塞式的 Python Web 框架，具有高度的擴展性和低延遲性能。它內建了支持同步和非同步處理的工具，並與大量的 IO 操作相容。

應用場景：Tornado 適用於需要高性能、高併發和真實時間性能的 Web 應用程式。它常用於即時通訊應用程式、實時分析、實時數據處理等場景。

4) Bottle :

功能：Bottle 是一個輕量級的 Python Web 框架，具有簡單易用的 API 和最小的依賴性，適合小型應用程式和小型項目的開發。

應用場景：Bottle 適用於簡單的 Web 應用程式和 RESTful API 開發，尤其在小型項目和快速原型開發的情境中非常方便。

5) web2py :

功能： web2py 是一個全堆棧的 Python Web 框架，提供了完整的解決方案，包括 ORM 、驗證、安全性等。它強調開發的簡單性和可靠性。

應用場景：web2py 適用於開發中型和大型的 Web 應用程式，尤其在對安全性和可靠性要求較高的場景中。該框架具有簡單的學習曲線，並提供了易於使用的工具和內建功能。

需要注意的是，以上僅是對於這些框架的簡要描述，每個框架還有更多的功能和特點，並且在特定情境下可能存在更多的應用場景。選擇合適的框架應該根據項目的具體需求、開發者的偏好以及框架本身的特性來進行評估。

## FastAPI 與 Django 的比較

在現代網路開發框架中，FastAPI 與 Django 是兩個常見的選擇。這兩個框架各有其優點，適用於不同的開發需求。以下將從性能、易用性、擴展性等方面來比較這兩者。

1). 性能

FastAPI 被設計為高效能的非同步框架，使用 Python 的異步（asynchronous）功能。這使得 FastAPI 在處理大量同時請求時，能夠表現得更為出色。根據官方測試，FastAPI 的性能甚至可以與 Node.js 等非同步框架相媲美。

另一方面，Django 是一個傳統的同步框架，性能較為穩定，但在大量並發請求下，處理速度可能不及 FastAPI。Django 主要著重於功能完備性與易用性，而非極致的性能優化。

2). 易用性

Django 以「電池全備」的方式著稱，這意味著它內建了眾多功能，如用戶認證、管理介面、ORM（Object-Relational Mapping）等。對於開發者來說，這使得 Django 更加方便快速上手。即使是較為複雜的項目，Django 也能提供現成的解決方案。

FastAPI 則以極簡主義和靈活性著稱。它的核心功能簡潔，開發者可以根據需要自行選擇第三方工具。這使得 FastAPI 更加靈活，特別適合那些希望對每個部分都有更多掌控權的開發者。

3). 擴展性與社羣支持Django 擁有龐大的使用者羣體與豐富的第三方庫支持，使得擴展和自定義非常容易。許多現有的插件可以直接集成到專案中，省去了大量的開發時間和成本。

相比之下，FastAPI 的生態系統還在快速發展中，儘管它的社羣不如 Django 成熟，但在某些領域（例如 API 開發）具有強大的競爭力。此外，因為 FastAPI 是基於 Pydantic 和 Starlette 的，因此開發者能夠使用這些工具進行擴展。

4). 何時使用 FastAPI? 何時使用 Django?

如果您的項目重點是構建高性能的 API 服務，尤其是需要處理大量的並發請求，並且希望利用 Python 的非同步功能，那麼 FastAPI 是理想的選擇。

如果您需要一個功能完備的網路應用框架，並且希望快速啟動項目而不必從零開始設計後端架構，Django 會是更好的選擇。Django 適合構建內容管理系統（CMS）、電子商務平臺等需要強大數據庫支持的應用。

5). 結論

FastAPI 和 Django 各自針對不同的使用場景進行了優化。FastAPI 更注重性能和靈活性，而 Django 提供了豐富的功能和較低的學習門檻。在選擇這兩個框架時，應根據項目的具體需求來決定。
