# 第 4 章 · 數據類型、運算符與數字

執行以上程序，輸出結果為：

```
1
1
2
3
5
8
```
這個例子介紹了幾個新特徵。

第一行包含了一個複合賦值：

變量 a 和 b 同時得到新值 0 和 1 。

最後一行也使用了複合賦值的方法：等價於 c = a，a = b，b = b + c。

最後嘗試使用 if 條件控制

```
age = int(input("請輸入你家狗狗的年齡："))
print("")
if age < 0:
    print("請輸入正確的年齡：")
elif age == 1:
    print("相當於 14 歲的人：")
elif age == 2:
    print("相當於 22 歲的人：")
elif age > 2:
    human = 22 + (age -2)*5
    print("對應人類年齡：", human)
    ### 退出提示，本地環境下可以使用這樣的退出提示使代碼更易用
    input('點擊 enter 鍵退出')
```
(在 index1.py)

## Python3 基本數據類型

在 Python 中，變量就是變量，它沒有類型，我們所說的"類型"是變量所指的內存中對象的類型。Python 3 中有六個標準的數據類型：

Numbers (數字)

String (字符串)

List (列表)

Tuple (元組)

Sets (集合)

Dictionaries (字典)Numbers(數字)

Python 3 支持 int （整型）、float （浮點型）、bool （布爾型）、complex （複數）。

數值類型的賦值和計算都是很直觀的，就像大多數語言一樣。內置的 type() 函數可以用來查詢 變量所指的對像類型。

```
a, b, c, d = 20, 5.5, True, 4+3j
print(type(a), type(b), type(c), type(d))
# <class 'int'> <class 'float'> <class 'bool'> <class 'complex'>
```
還可以用 isinstance 來判斷：

```
aa = 111
print(isinstance(aa, int))
```
isinstance 和 type 的區別在於：

type ()不會認為子類是一種父類類型。

isinstance ()會認為子類是一種父類類型。

```
class A:
    pass
class B(A):
    pass
    print(isinstance(A(), A))
    print(type(A) == A)
    print(isinstance(B(), A))
    print(type(B) == A)
```
當你指定一個值時，Number 對象就會被創建：

```
var1 = 1
var2 = 10
```
1. Python 可以同時為多個變量賦值，如 a, b = 1, 2。

2. 一個變量可以通過賦值指向不同類型的對象。

3. 數值的除法（/）總是返回一個浮點數，要獲取整數使用//操作符。

4. 在混合計算時，Python 會把整型轉換成為浮點數 (index.py)String（字符串）

Python 中的字符串 str 用單引號('')或雙引號("") 括起來，同時使用反斜槓() 轉義特殊字符。

```
s = 'Yes, he doesn\'t'
print(s, type(s), len(s))
```
如果你不想讓反斜槓發生轉義，可以在字符串前面添加一個 r，表示原始字符串：

```
print('C:\some\name')
print(r'C:\some\name')
```
字符串可以使用+ 運算符串連接在一起，或者用* 運算符重複：

```
print('str' + 'ing', 'my'*3)
```
Python 中的字符串有兩種索引方式，

第一種是從左往右，從0開始依次增加；

第二種是從右往左，從-1開始依次減少。

注意，沒有單獨的字符類型，一個字符就是長度為1的字符串。

```
word = 'Python'
print(word[0], word[5])
print(word[-1], word[-6])
```
還可以對字符串進行切片，獲取一段子串。用冒號分隔兩個索引，形式為變量[頭下標：尾下標]。

截取的範圍是前閉後開的(頭下標取，尾下標不取)，並且兩個索引都可以省略：

```
word = 'ilovepython'
word[1:5]
word[:]
word[5:]
word[-10:-6]
```
與 C 字符串不同的是，Python 字符串不能被改變。向一個索引位置賦值，比如 word[0] = 'm' 會導致錯誤。

注意：

1. 反斜槓可以用來轉義，使用 r 可以讓反斜槓不發生轉義。

2. 字符串可以用+ 運算符連接在一起，用* 運算符重複。

3. Python 中的字符串有兩種索引方式，從左往右以 0 開始，從右往左以 -1 開始。

4. Python 中的字符串不能改變。

```
(index1.py)
```
List(列表)

List(列表)是 Python 中使用最頻繁的數據類型。

列表是寫在方括號之間、用逗號分隔開的元素列表。列表中元素的類型可以不相同：

```
a = ['him', 25, 100, 'her']
print(a)
```
和字符串一樣，列表同樣可以被索引和切片，列表被切片後返回一個包含所需元素的新列表。詳細的在這裡就不贅述了。

列表還支持串聯操作，使用+ 操作符：

```
a = [1, 2, 3, 4, 5]
a + [6, 7, 8]
```
與 Python 字符串不一樣的是，列表中的元素是可以改變的：

```
a = [1, 2, 3, 4, 5, 6]
a[0] = 9
a[2:5] = [13, 14, 15]
a
```
a[2:5] = [] # 刪除

```
a
```
List 內置了很多方法，例如 append()、pop() 等等，這在後面會講到。

注意：

1. List 寫在方括號之間，元素用逗號隔開。

2. 和字符串一樣，List 可以被索引和切片。

3. List 可以使用+ 操作符進行拼接。

4. List 中的元素是可以改變的。

```
(index2.py)
```
Tuple(元組)

元組(tuple)與列表類似，不同之處在於元組的元素不能修改。元組寫在小括號裡，元素之間用逗號隔開。

元組中的元素類型也可以不相同：

```
a = (1991, 2014, 'physics', 'math')
print(a, type(a), len(a))
```
元組與字符串類似，可以被索引且下標索引從 0 開始，也可以進行截取/切片(看上面，這裡不再贅述)。

其實，可以把字符串看作一種特殊的元組。

```
tup = (1, 2, 3, 4, 5, 6)
print(tup[0], tup[1:5])
tup[0] = 11 # 修改元組元素的操作是非法的
```
雖然 tuple 的元素不可改變，但它可以包含可變的對象，比如 list 列表。

構造包含 0 個或 1 個元素的 tuple 是個特殊的問題，所以有一些額外的語法規則

```
tup1 = () # 空元組
tup2 = (20,) # 一個元素，需要在元素後添加組號
```
另外，元組也支持用+ 操作符：

```
tup1, tup2 = (1, 2, 3), (4, 5, 6)
print(tup1 + tup2)
```
string、list 和 tuple 都屬於 sequence （序列）。

注意：

1. 與字符串一樣，元組的元素不能修改。

2. 元組也可以被索引和切片，方法都是一樣的。

3. 注意構造包含 0 或 1 個元素的元組的特殊語法規則。

4. 元組也可以使用+ 操作符進行拼接。

```
(index3.py)
```
Sets(集合)

集合(set)是一個無序不重複元素的集。

基本功能是進行成員關係測試和消除重複元素。

可以使用大括號或者 set() 函數創建 set 集合，注意：創建一個空集合必須用 set() 而不是 {}，因為 {} 是用來創建一個空字典。

```
student = {'Tom', 'Jim', 'Mary', 'Tom', 'Jack', 'Rose'}
print(student)
# set可以進行集合運算
a = set('abracadabra')
b = set('alacazam')
print(a)
print(a - b) # a和b的差集
print(a | b) # a和b的並集
print(a & b) # a和b的交集
print(a ^ b) # a和b中不同時存在的元素
(index4.py)
```
Dictionaries(字典)

字典(dictionary)是 Python 中另一個非常有用的內置數據類型。

字典是一種映射類型(mapping type)，它是一個無序的鍵值對(key-value)集合。

關鍵字(key)必須使用不可變類型，也就是說 list 和包含可變類型的 tuple 不能做關鍵字。在同一個字典中，關鍵字(key)必須互不相同。

```
dic = {} # 創建空字典
tel = {'Jack':1557, 'Tom':1320, 'Rose':1886}
print(tel)
print(tel['Jack']) # 主要的操作：通過key查詢
```
del tel['Rose'] # 刪除一個鍵值對

tel['Mary'] = 4127 # 添加一個鍵值對

```
print(tel)
```
list(tel.keys()) # 返回所有key組成的list

sorted(tel.keys()) # 按key排序

另外，字典類型也有一些內置的函數，例如 clear()、keys()、values() 等。

注意：

1. 字典是一種映射類型，它的元素是鍵值對。

2. 字典的關鍵字必須為不可變類型，且不能重複。

3. 創建空字典使用{}。

```
(index5.py)
```
## Python3 註釋

Python3 註釋可以確保對模塊，函數，方法和行內註釋使用正確的風格，有專門的符號和格式，有單行與多行的區別。

Python 中的註釋有單行註釋和多行註釋：

Python 中單行註釋以#開頭，例如：

```
# 我就是注釋
print("Hello, World")
```
多行註釋用三個單引號("")或者三個雙引號("")將需要註釋的內容囊括起來，例如：1、單引號("")

這是多行註釋，用三個單引號

這是多行註釋，用三個單引號

這是多行註釋，用三個單引號

```
print("Hello, World!")
```
2、雙引號("")

這是多行註釋，用三個雙引號

這是多行註釋，用三個雙引號

這是多行註釋，用三個雙引號

```
print("Hello, World!")
```
## Python3 運算符

Python 的運算符。舉個簡單的例子 $ 4+5=9 $。例子中，4 和 5 被稱為運算符，“+”稱為運算符。Python 語言支持以下類型的運算符：

算術運算符

比較(關係)運算符

賦值運算符

總編輯運算符

成員運算符

身分運算符

運算符優先級

## Python 算術運算符

下面假設變量 a 爲 21，變量 b 爲 10：


| 運算符 | 描述 | 類別 |
| --- | --- | --- |
| + | 加 - 兩個對像加 | a + b 輸出結果 31 |
| - | 減 - 得到負數或者是一個數減去另一個數 | a - b 輸出結果 11 |
| * | 乘 - 兩個數相乘或者是返回一個被重新恢復若干次的字符串 | a * b 輸出結果 210 |
| / | 除 - x 除以 y | a / b 輸出結果 2.1 |
| % | 取模 - 返回剛除法的餘數 | a % b 輸出結果 1 |
| \*\* | 模 - 返回 x 的 y 次模 | a \*\* b 為 21 的 10 次方 |
| // | 取整除 - 返回商的整數部分 | 9//2 輸出結果 4, 9.0//2.0 輸出結果 4.0 |


下面實例演示了 Python 所有運算符的操作：

```
a = 21
b = 10
c = 0
c = a + b
print("a+b 的值爲：", c)
c = a - b
print("a-b 的值爲：", c)
c = a * b
print("a*b 的值爲：", c)
c = a / b
print("a/b 的值爲：", c)
c = a % b
print("a%b 的值爲：", c)
aa = 2
bb = 3
cc = aa**bb
print("aa**bb 的值爲：", cc)
aaa = 10
bbb = 5
ccc = aaa//bbb
print("aaa//bbb 的值爲：", ccc)
```
以上實例輸出結果：

a 不等於 b

a 不等於 b

a 大於等於 b

a 大於 b

aa 小於等於 bb

aa 小於 bb

Python 比較運算符

下面假設變量 a 為 10，變量 b 為 20：


| 運算符 | 描述 | 實例 |
| --- | --- | --- |
| = | 簡單的資產運算符 | c = a + b 將 a + b 的計算結果賦值為 c |
| += | 加法賦值運算符 | c += a 等效於 c = c + a |
| -= | 減法賦值運算符 | c -= a 等效於 c = c - a |
| *= | 乘法賦值運算符 | c *= a 等效於 c = c * a |
| /= | 除法賦值運算符 | c /= a 等效於 c = c / a |
| %= | 取模值運算符 | c %= a 等效於 c = c % a |
| \*\*= | 賦值運算符 | c \*\*= a 等效於 c = c \*\* a |
| //= | 取整除賦值運算符 | c //= a 等效於 c = c // a |


所有比較運算符返回 1 表示真，返回 0 表示假。這個分別與特殊的變化量 True 和 False 等價。

注意：True 和 False 的首字母為大寫。

下面實例演示了 Python 所有比較運符的操作：

```
a = 21
b = 10
c = 0
if (a == b):
    print("a 等於 b")
else:
    print("a 不等於 b")
    if (a != b):
        print("a 不等於 b")
    else:
        print("a 等於 b")
        if (a < b):
            print("a 小於 b")
        else:
            print("a 大於等於 b")
            if (a > b):
                print("a 大於 b")
            else:
                print("a 小於等於 b")
                aa = 5;
                ba = 20;
                if (aa <= bb):
                    print("aa 小於等於 bb")
                else:
                    print("aa 大於 bb")
                    if (aa >= bb):
                        print("aa 大於等於 bb")
                    else:
                        print("aa 小於 bb")
```
以上實例輸出結果：

a 不等於 b

a 不等於 b

a 大於等於 b

a 大於 b

aa 小於等於 bb

aa 小於 bb

```
(index1.py)
```
## Python 賦值運算符

下面假設變量 a 為 10，變量 b 為 20：


| 運算符 | 描述 | 實例 |
| --- | --- | --- |
| = | 簡單的資產運算符 | c = a + b 將 a + b 的計算結果賦值為 c |
| += | 加法賦值運算符 | c += a 等效於 c = c + a |
| -= | 減法賦值運算符 | c -= a 等效於 c = c - a |
| *= | 乘法賦值運算符 | c *= a 等效於 c = c * a |
| /= | 除法賦值運算符 | c /= a 等效於 c = c / a |
| %= | 取模值運算符 | c %= a 等效於 c = c % a |
| \*\*= | 賦值運算符 | c \*\*= a 等效於 c = c \*\* a |
| //= | 取整除賦值運算符 | c //= a 等效於 c = c // a |


以下實例演示了 Python 所有賦值運算符的操作：

```
a = 21
b = 10
c = 0
c = a + b
print("1 - c 的值爲：", c)
c += a
print("2 - c 的值爲：", c)
c *= a
print("3 - c 的值爲：", c)
c /= a
print("4 - c 的值爲：", c)
c = 2
c %= a
print("5 - c 的值爲：", c)
c **= a
print("6 - c 的值爲：", c)
c //= a
print("7 - c 的值爲：", c)
```
以上實例輸出結果：

1 - c 的值爲：31

2 - c 的值爲：52

3 - c 的值爲：1092

4 - c 的值爲：52.0

5 - c 的值爲：2

6 - c 的值爲：2097152

7 - c 的值爲：99864

```
(index2.py)
```
Python 總編輯算符

Python 語言支持總編輯運算符，以下假設置量 a 為 10，b 為 20：


| 運算符 | 總編輯表達式 | 描述 | 實例 |
| --- | --- | --- | --- |
| and | x and y | 布爾“與”-如果 x 為 False, x 和 y 返回 False, 否則它返回 y 的計算值。 | (a and b) 返回 20. |
| or | x or y | 布爾“或”-如果 x 是 True, 它返回 x 的值, 否則它返回 y 的計算值。 | (a or b) 返回 10. |
| not | not x | 布爾“非”-如果 x 為 True, 返回 False, 如果 x 為 False, 則返回 True。 | not(a and b) 返回 False |
| 以上實例輸出結果： |


```
a = 10
b = 20
if (a and b):
    print("1 - 變量 a 和 b 都為 true")
else:
    print("1 - 變量 a 和 b 有一個不為 true")
    if (a or b):
        print("2 - 變量 a 和 b 都為 true，或其中一個變量為 true")
    else:
        print("2 - 變量 a 和 b 都不為 true")
        # 修改變量 a 的值
        a = 0
        if (a and b):
            print("3 - 變量 a 和 b 都為 true")
        else:
            print("3 - 變量 a 和 b 有一個不為 true")
            if (a or b):
                print("4 - 變量 a 和 b 都為 true，或其中一個變量為 true")
            else:
                print("4 - 變量 a 和 b 都不為 true")
                if not(a and b):
                    print("5 - 變量 a 和 b 都為 false，或其中一個變量為 false")
                else:
                    print("5 - 變量 a 和 b 都為 true")
```
以上實例輸出結果：

1 - 變量 a 和 b 都為 true

2 - 變量 a 和 b 都為 true，或其中一個變量為 true

3 - 變量 a 和 b 有一個不為 true

4 - 變量 a 和 b 都為 true，或其中一個變量為 true

5 - 變量 a 和 b 都為 false，或其中一個變量為 false

```
(index3.py)
```
## Python 成員運算符

除了以上的一些運算符之外，Python 還支持成員運算符，測試實例中包含了一系列的成員，包含字符串，列表或元組。


| 運算符 | 描述 | 實例 |
| --- | --- | --- |
| in | 如果在指定的順序中找到值返回True,否則返回 False。 | x 在 y 順序中,如果 x 在 y 順序中返回 True。 |
| not in | 如果在指定的順序中沒有找到值返回 True,否則返回 False。 | x 不在 y 順序中,如果 x 不在 y 順序中返回 True。 |


下面實例演示了 Python 所有成員運算符的操作：

```
a = 10
b = 20
list = [1, 2, 3, 4, 5];
if (a in list):
    print("1 - 變量 a 在給定的列表中 list 中")
else:
    print("1 - 變量 a 不在給定的列表中 list 中")
    if (b not in list):
        print("2 - 變量 b 不在給定的列表中 list 中")
    else:
        print("2 - 變量 b 在給定的列表中 list 中")
        # 修改變量 a 的值
        a = 2
        if (a in list):
            print("3 - 變量 a 在給定的列表中 list 中")
        else:
            print("3 - 變量 a 不在給定的列表中 list 中")
```
以上實例輸出結果：

1 - 變量 a 不在給定的列表中 list 中

2 - 變量 b 不在給定的列表中 list 中

3 - 變量 a 在給定的列表中 list 中

```
(index4.py)
```
## Python 身分運算符

## 身體運算符用於比較兩個對象的存貯單位


| 運算符 | 描述 | 實例 |
| --- | --- | --- |
| is | 是判斷兩個標誌符是不是引用自己一個對象 | x is y, 如果 id(x) 等於 id(y), is返回結果 True |
| is not | is not is not is not is 判斷兩個標誌符是不是引用自不同對照象 | x 不是 y, 如果 id(x) 不等於 id(y),不是返回結果 True |


示了 Python 的所有運算符的操作：

```
a = 20
b = 20
if (a is b):
    print("1 - a 和 b 有相同的標識")
else:
    print("1 - a 和 b 沒有相同的標識")
    if (id(a) == id(b)):
        print("2 - a 和 b 有相同的標識")
    else:
        print("2 - a 和 b 沒有相同的標識")
        # 修改變量 b 的值
        b = 30
        if (a is b):
            print("3 - a 和 b 有相同的標識")
        else:
            print("3 - a 和 b 沒有相同的標識")
            if (a is not b):
                print("4 - a 和 b 沒有相同的標識")
            else:
                print("4 - a 和 b 有相同的標識")
```
以上實例輸出結果：

1 - a 和 b 有相同的標識

2 - a 和 b 有相同的標識

3 - a 和 b 沒有相同的標識

4 - a 和 b 沒有相同的標識

```
(index2.py)
```
## Python 運算符優先級

以下表格列出了從最高到最低優先級的所有運算符：


| 運算符 | 描述 |
| --- | --- |
| (expressions...), [expressions...], {key: value...}, {expressions...} | 因括號的表達式 |
| x[index], x[index:index], x(arguments...), x.attribute | 讀取，切片，調用，屬性引用 |
| await x | await 表達式 |
| \*\* | 乘方(指數) |
| +x, -x, -x | 正，負，按位非 NOT |
| *, @, /, //, % | 乘，矩陣乘，除，整除，取餘 |
| +,- | 加和減 |
| &lt;&lt;, &gt;&gt; | 移位 |
| &amp; | 按位與 AND |
| ^ | 按位異或 XOR |
| | | 按位或 OR |
| in, not in, is, is not, &lt;, &lt;=, &gt;, &gt;=, !=, == | 比較運算，包括成員檢測和標識號檢測 |
| not x | 邏輯非 NOT |
| and | 邏輯與 AND |
| or | 邏輯或 OR |
| if -- else | 條件表達式 |
| lambda | lambda 表達式 |
| := | 賦值表達式 |
| 下面實例演示了 Python 所有運算符高級的操作： |


```
a = 20
b = 10
c = 15
d = 5
e = 0
e = (a + b) * c / d # (30 * 15) / 5
```
print ("(a + b) * c / d 運算結果為：", e)

```
e = ((a + b) * c) / d # (30 * 15) / 5
```
print ("((a + b) * c) / d 運算結果為：", e)

```
e = (a + b) * (c / d); # (30) * (15/5)
```
print ("(a + b) * (c / d) 運算結果為：", e)

```
e = a + (b * c) / d; # 20 + (150/5)
```
print ("a + (b * c) / d 運算結果為：", e)

以上實例輸出結果：

(a + b) * c / d 運算結果為：90.0

((a + b) * c) / d 運算結果為：90.0

(a + b) * (c / d) 運算結果為：90.0

a + (b * c) / d 運算結果為：50.0

```
(index6.py)
```
## Python3 數字

Python 數字類型用於數值的儲存。數值類型是不允許改變的，如果改變數字數據類型的值，將重新分配內存空間。

以下實例在變量賦值時 Number 對象將被創建：

```
var1 = 1
var2 = 10
```
Python 支持三種不同的數值類型：

整型(Int) - 通常被稱為是整型或整數，是正或負整數，不帶小數點。Python3 整型是沒有限制大小的，可以當作 Long 類型使用，所以 Python3 沒有 Python2 的 Long 類型。

浮點型(float) - 浮點型由整數部分與小數部分組成，浮點型也可以使用科學計數法表示 $ (2.5e2 = 2.5 \times 10^{2} = 250) $

複數( (complex)) - 複數由實數部分和虛數部分構成，可以用 a + bj,或者 complex(a,b)表示，複數的實部 a 和虛部 b 都是浮點型。

## Python 數字類型轉換

我們需要對數據內置的類型進行轉換，數據類型的轉換，你只需要將數據類型作為函數名即可。

- nt(x)將 x 轉換為一個整數。

- $ \text{loat}(x) $ 將 x 轉換到一個浮點數。

- complex(x)將 x 轉換到一個複數，實數部分為 x ，虛數部分為 0 。

- complex(x, y)將 x 和 y 轉換到一個複數，實數部分為 x ，虛數部分為 y 。 x 和 y 是數字表達式。

以下實例將浮點數變量 a 轉換為整數：

```
a = 1.0
int(a)
1
```
## Python 數字運算

Python 解釋器可以作為一個簡單的計算器，您可以在解釋器裡輸入一個表達式，它將輸出表達式的值。

表達式的語法很直白：+，-，*和/，和其它語言(如 Pascal 或 C)裡一樣。例如：

```
a = 2+2
print(a)
a1 = 50 - 5*6
print(a1)
a2 = (50 - 5*6) / 4
print(a2)
a3 = 8 / 5 # 總是返回一個浮點數
print(a3)
```
注意：在不同的機器上浮點運算的結果可能會不一樣。

在整數除法中，除法/總是返回一個浮點數，如果只想得到整數的結果，丟棄可能的分數部分，可以使用運算符//：

```
# b = 17 / 3 # 整數除法返回浮點型
# print(b)
# b1 = 17 // 3# 整數除法返回下取整後的結果
# print(b1)
# b2 = 17 % 3# % 操作符返回除法的餘數
# print(b2)
# b3 = 5 * 3 + 2
# print(b3)
```
注意：//得到的並不一定是整數類型的數，它與分母分子的數據類型有關係。

```
c = 7 // 2
print(c)
c1 = 7.0 // 2
print(c1)
c2 = 7 // 2.0
print(c2)
```
(index.py) 等號=用於給變量賦值。賦值之後，除了下一個提示符，解釋器不會顯示任何結果。

```
width = 20
height = 5*9
print(width * height)
```
(index.py) Python 可以使用\*\*操作來進行冪運算：

```
d = 5 ** 2
print(d)
d1 = 2 ** 7
print(d1)
```
(index.py) 不同類型的數混合運算時會將整數轉換為浮點數：

```
e = 3 * 3.75 / 1.5
print(e)
e1 = 7.0 / 2
print(e1)
```
