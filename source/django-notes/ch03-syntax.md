# 第 3 章 · Python3 基礎語法
## Python3 基礎語法
## 編碼
默認情況下，Python 3 源碼文件以 UTF-8 編碼，所有字符串都是 unicode 字符串。當然你也可以為源碼文件指定不同的編碼：
```
# -*- coding: cp-1252 -*-
```
標識符
第一個字符必須是字母表中字母或下劃線'。
標識符的其他的部分有字母、數字和下劃線組成。
標識符對大小寫敏感。
在 Python 3 中，非 ASCII 編碼的標識符也是允許的了。
## Python 保留字
保留字即關鍵字，我們不能把它們用作任何標識符名稱。Python 的標準庫提供了一個關鍵詞模塊，我們可以使用它來查看當前版本的所有保留字：
>>> import keyword
>>> keyword.kwlist
```
['False', 'None', 'True', '__peg_parser__', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
```
## 註釋
Python 中單行註釋以#開頭，多行註釋採用三對單引號("")或者三對雙引號("")將註釋括起來。
```
#這是單行註釋
0000
```
這是多行註釋
這是多行註釋
```
0000
```
\*\*\*\**
也可以用三個單引號來進行多行註釋
\*\*\*\**
實際上 python 註釋只有一種，就是單行註釋，多行註釋的這種使用方法類似於 java 的 javadoc，三引號的這種使用方法實際上是用來聲明多行長字符串的。
## 縮進
Python 最具特色的就是使用縮進來表示代碼塊。縮進的空格數是可變的，但是同一個代碼塊的語句必須包含相同的縮進空格數。
```
def hi():
    print('hi')  # 縮進
```
標準數據類型
Python 中有六個標準的數據類型：
Number (數字)
String (字符串)
List (列表)
Tuple (元組)
Set (集合)
Dictionary (字典)
Python3 的六個標準數據類型：
不可變數據(3個)：Number (數字)、String(字符串)、Tuple (元組)
可變數據(3 個)：List (列表)、Dictionary(字典)、Set(集合)
可變數據和不可變數據是相對於引用地址來說的，不可變數據類型不允許變量的值發生變化，如果改變了的變量的值，相當於新建了一個對象，而對於相同的值的對象，內部會有一個引用計數來記錄有多少個變量引用了這個對象。可變數據類型允許變量的值發生變化。對變量進行修改操作只會改變變量的值，不會新建對象，變量引用的地址也不會發生變化，不過對於相同的值的不同對象，在內存中則會存在不同的對象，即每個對像都有自己的地址，相當於內存中對於同值的對象保存了多份，這裡不存在引用計數，是實實在在的對象。
簡單地講，可變數據和不可變數據的“變”是相對於引用地址來說的，不是不能改變其數據，而是改變數據的時候會不會改變變量的引用地址。
## 類型判斷
例子
```
isStr = "餅瑞瑪"
print(type(isStr))
isInt = 1000
print(type(isInt))
isTuple = ('德瑪', '20', 'x')
print(type(isTuple))
isList = ['d', '4', '垃圾']
print(type(isList))
```
字符串
Python 中單引號和雙引號使用完全相同，但單引號和雙引號不能匹配。
使用三對引號("或")可以囊括一個多行字符串。
與其他語言相似，python 也使用"作為轉義字符
自然字符串，通過在字符串前加 r 或 R。如 r"this is a line with \n" 則\n 會顯示，並不是換行。
Python 允許處理 unicode 字符串，加前綴 u 或 U，如 u"this is an unicode string"。
字符串是不可變的。
按字面意義級聯字符串，如"this " "is " "string"會被自動轉換為 this is string。
字符串可以用+運算符連接在一起，用*運算符重複。
Python 中的字符串有兩種索引方式，從左往右以 0 開始，從右往左以-1 開始。
Python 中的字符串不能改變(詳見上一小點的引用)。
Python 沒有單獨的字符類型，一個字符就是長度為 1 的字符串。
字符串的截取的語法格式如下：變量[頭下標：尾下標：步長]
## 輸入&等待用戶輸入
input 函數可以用來接受輸入，它可以傳入一個字符串，當 input 函數調用的時候，會在控制台打印這個字符串(所以這個字符串通常被用來做輸入的提示信息)
input函數會讀取輸入內容直到讀到回車，也就是說，內容輸入完畢後要按回車鍵才能執行。
## 例子
```
input("記得接Enter：")
x=input("輸入把少年：")
print(x)
print(type(x))
```
## 同一行顯示多條語句
Python 可以在同一行中使用多條語句，語句之間使用分號(;) 分割，以下是一個簡單的實例：
```
import sys; x = 'nothing'; sys.stdout.write(x + '\n')
```
輸出結果為：
```
nothing
```
## import 與 from...import
在 Python 用 import 或者 from...import 來導入相應的模塊。
將整個模塊(somemodule)導入，格式為：
```
import somemodule
```
從某個模塊中導入某個函數，格式為：
```
from somemodule import somefunction
```
從某個模塊中導入多個函數，格式為：
```
from somemodule import firstfunc, secondfunc, thirdfunc
```
將某個模塊中的全部函數導入，格式為：
```
from somemodule import *
```
多個語句構成代碼組
縮進相同的一組語句構成一個代碼塊，我們稱之代碼組。
像 if、while、def 和 class 這樣的複合語句，首行以關鍵字開始，以冒號(:) 結束，該行之後的一行或多行代碼構成代碼組。
我們將首行及後面的代碼組稱為一個子句(clause)。
實例：
```
if expression :
    suite
elif expression :
    suite
else :
    suite
```
## print 輸出
print 函數是 python 的基本輸出函數，他可以將變量輸出(或者說，打印)到控制台。在第一個 python 程序中，我們就用到了 print 函數：
```
print("Hello, World!")
str = "Hello, World!"
print(str)
```
Python3 編程第一步
在下例裡，我們能寫出一個初步的斐波納契數列如下：
```
a, b = 0, 1
while b < 10:
    print(b)
    a, b = b, a + b
```
其中代碼 a, b = b, a + b 的計算方式為先計算右邊的表達式，然後同時賦值給左邊，等價於：
```
n = b
m = a + b
a = n
b = m
```
