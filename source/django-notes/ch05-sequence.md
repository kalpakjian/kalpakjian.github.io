# 第 5 章 · 序列與容器類型

## Python3 序列

在編程語言中，將以某種方式(比如通過編號)組合起來的數據元素(如數字，字符串乃至其他數據結構)集合稱為數據結構。在 python 中，最基本的數據結構為序列(sequence，簡寫為 seq)。

所謂序列，指的是一塊可存放多個值的連續內存空間，這些值按一定順序排列，可通過每個值所在位置的編號(稱為索引)訪問它們。

為了更形象的認識序列，可以將它看做是一家旅店，那麼店中的每個房間就如同序列存儲數據的一個個內存空間，每個房間所特有的房間號就相當於索引值。也就是說，通過房間號(索引)我們可以找到這家旅店(序列)中的每個房間(內存空間)。

在 Python 中，序列類型包括字符串、列表、元組、集合和字典，這些序列支持以下幾種通用的操作，但比較特殊的是，集合和字典不支持索引、切片、相加和相乘操作。

字符串也是一種常見的序列(所以以下的例子以字符串作為)，它也可以直接通過索引訪問字符串內的字符。

## 序列索引

序列中，每個元素都有屬於自己的編號(索引)。從起始元素開始，索引值從0開始遞增，如圖1所示。

除此之外，Python 還支持索引值是負數，此類索引是從右向左計數，換句話說，從最後一個元素開始計數，從索引值-1開始，如圖2所示。

無論是採用正索引值，還是負索引值，都可以訪問序列中的任何元素。以字符串為例

```
str = "python"
print(str[0], "=", str[-6])
print(str[5], "=", str[-1])
```
## 序列切片

切片操作是訪問序列中元素的另一種方法，它可以訪問一定範圍內的元素，通過切片操作，可以生成一個新的序列。序列實現切片操作的語法格式如下：

```
sname[start : end : step]
```
其中，各個參數的含義分別是：

sname：表示序列的名稱；

start：表示切片的開始索引位置(包括該位置)，此參數也可以不指定，會默認為0，也就是從序列的開頭進行切片；

end：表示切片的結束索引位置(不包括該位置)，如果不指定，則默認為序列的長度；

step：表示在切片過程中，隔幾個存儲位置(包含當前位置)取一次元素，也就是說，如果 step 的值大於 1，則在進行切片去序列元素時，會“跳躍式”的取元素。如果省略設置 step 的值，則最後一個冒號就可以省略。

例如，對字符串 “python” 進行切片：

```
str = "python"
# 取索引區間為[0,2]之間（不包括索引2處的字符）的字符串
print(str[:2])
# 隔1個字符取一個字符，區間是整個字符串
print(str[:2])
# 取整個字符串，此時[]中只需一個冒號即可
print(str[:])
```
運行結果為：

```
py
pto
python
```
## 序列相加

Python 中，支持兩種類型相同的序列使用 “+” 運算符做相加操作，它會將兩個序列進行連接，但不會去除重複的元素。這裡所說的 “類型相同”，指的是 “+” 運算符的兩側序列要麼都是列表類型，要麼都是元組類型，要麼都是字符串。

例如，前面章節中我們已經實現用“+”運算符連接2個(甚至多個)字符串，如下所示：

```
str1 = "py"
str2 = "th"
str3 = "on"
print(" : ", str1 + str2 + str3)
```
## 序列相關的內置函數

函數</td> 功能</td></tr> len()</td> 計算序列的長度，即返回序列中包含多少個元素。</td></tr> max()</td> 找出序列中的最大元素。注意，對序列使用sum()函數時，做加和操作的必須都是數字，不能是字符或字符串，否則該函數將拋出異常，因爲解釋器無法判定是要做連接操作（+ 運算符可以連接兩個序列），這是做加和操作。</td></tr> min()</td> 找出序列中的最小元素。</td></tr> list()</td> 將序列轉換爲列表。</td></tr> str()</td> 將序列轉換爲字符串。</td></tr> sum()</td> 計算元素和。</td></tr> sorted()</td> 當元素進行排序。</td></tr> reversed()</td> 反向序列中的元素。</td></tr> enumerate()</td> 將序列組合爲一個索引序列，多用在for循環中。</td></tr></table>

部分序列不能應用其中的部分函數，比如字典中不能直接使用list，詳細的函數介紹請參閱相應數類型的函數介紹。

這裡給大家給幾個例子：

```
str4 = "python-django"
#找出最大的字符
print(max(str4))
#找出最小的字符
print(min(str4))
#對字符串中的元素進行排序
print(sorted(str4))
```
輸出結果為：

```
y
a
['a', 'd', 'g', 'h', 'j', 'n', 'n', 'o', 'o', 'p', 't', 'y']
```
## Python3 列表

列表(list)也是最常用的 Python 數據類型之一，它以一個方括號內包含多個其他數據項(字符串，數字等甚至是另一個列表)，數據項間以逗號作為分隔的數據類型。列表的數據項不需要具有相同的類型。(這點是與其他語言的數組的一個區別)創建一個列表，只要把逗號分隔的不同的數據項使用方括號括起來即可。如下所示：

```
list1 = ['js', 'py', 'css', 'html']
list2 = ['15', '26', '50']
print("list1 : ", list1)
print("list2 : ", list2)
```
## 訪問列表中的值

與字符串的索引一樣，列表索引從 0 開始，第二個索引是 1，依此類推。通過索引列表可以進行截取、組合等操作。列表索引的操作：

```
list1 = ['js', 'py', 'css', 'html']
print("list1的第一項：", list1[0])
print("list1的最後一項：", list1[-1])
```
運行結果：

list1的第一項：js

list1的最後一項：html以下是列表切片的操作：

```
list1 = ['js', 'py', 'css', 'html']
print("list1的前3項：", list1[0:3])
print("list1的2、3項：", list1[1:3])
```
運行結果：

list1的前3項：['js', 'py', 'css']

list1的2、3項：['py', 'css']

## 更新列表

你可以對列表的數據項進行修改或更新，你也可以使用 append() 方法來添加列表項，如下所示：

```
list1 = ['js', 'py', 'css', 'html']
print("list1的第三個元素為：", list1[2])
list1[2] = "sass"
print("list1的第三個元素為：", list1[2])
list1.append(jss)
print("追加列表項後的list1: ", list1)
```
運行結果：

list1的第三個元素為：css

list1的第三個元素為：sass

追加列表項後的list1: ['js', 'py', 'sass', 'html', 'jsx']

刪除列表元素

可以使用 del 語句來刪除列表的的元素，如下實例：

```
list1 = ['js', 'py', 'css', 'html']
del list1[0]
print("刪除列表項後的list1: ", list1)
```
運行結果：

刪除列表項後的list1: ['py', 'css', 'html']

## Python3 元組

Python 的元組(tuple，簡寫為 tup)與列表類似，不同之處在於元組的元素不能修改。元組使用小括號()，列表使用方括號[]。元組創建很簡單，只需要在括號中添加元素，並使用逗號隔開即可。

如下實例：

```
tup1 = ('d1', 'd2', 'd3', 'd4')
tup2 = ('1996', '2000', '2012', '2023')
tup3 = '1', '2', '3', '4'
tup4 = ()
tuple = (99,)
print(type(tup3))
print(type(tup4))
print(type(tuple))
```
運行結果：

```
<class 'tuple'>
<class 'tuple'>
<class 'tuple'>
```
訪問元組

元組可以使用下標索引來訪問元組中的值，如下實例：

```
tup1 = ('d1', 'd2', 'd3', 'd4')
tup2 = ('1996', '2000', '2012', '2023')
print ("tup1[0]: ", tup1[0])
print ("tup2[1:5]: ", tup2[1:5])
```
運行結果：

```
tup1[0]: d1
tup2[1:5]: ('2000', '2012', '2023')
```
修改元組

元組中的元素值是不允許修改的，但我們可以對元組進行連接組合，如下實例：

```
tupn1 = ('order', '66')
tupn2 = ('star', 'war')
tupn3 = tupn1 + tupn2
print(tupn3)
```
運行結果：

```
('order', '66', 'star', 'war')
```
元組內置函數

## Python 元組包含了以下內置函數

序號</td> 方法及描述</td> 範例</td></tr> 1</td> len(tuple)\n計算元組元素值數。</td> >>> tuple1 = (&#x27;google&#x27;, &#x27;W3CSchool&#x27;, &#x27;Taobao&#x27;)\n>>> len(tuple1)\n3\n&gt;&gt;&gt;</td></tr> 2</td> max(tuple)\n返回元組中元素最大值。</td> &gt;&gt;&gt; tuple2 = (&#x27;5&#x27;, &#x27;4&#x27;, &#x27;8&#x27;)\n&gt;&gt;&gt; max(tuple2)\n&#x27;8&#x27;\n&gt;&gt;&gt;</td></tr> 3</td> min(tuple)\n返回元組中元素最小值。</td> &gt;&gt;&gt; tuple2 = (&#x27;5&#x27;, &#x27;4&#x27;, &#x27;8&#x27;)\n&gt;&gt;&gt; min(tuple2)\n&#x27;4&#x27;\n&gt;&gt;&gt;</td></tr> 4</td> tuple(seq)\n將列表轉換爲元組。</td> &gt;&gt;&gt; list1 = [&#x27;google&#x27;, &#x27;Taobao&#x27;, &#x27;W3CSchool&#x27;, &#x27;Baidu&#x27;]\n&gt;&gt;&gt; tuple1-tuple(list1)\n&gt;&gt;&gt; tuple1\n(&#x27;google&#x27;, &#x27;Taobao&#x27;, &#x27;W3CSchool&#x27;, &#x27;Baidu&#x27;)\n&gt;&gt;&gt;</td></tr> 5</td> operator(tuple1, tuple 2)\n軟荷值元組元素</td> &gt;&gt;&gt; import operator\n&gt;&gt;&gt; dict1 = (1, 2, 3)\n&gt;&gt;&gt; dict2 = (&#x27;a&#x27;, &#x27;b&#x27;, &#x27;c&#x27;)\n&gt;&gt;&gt; operator.eq(dict1, dict2)\nFalse</td></tr></table>

## 關於元組是不可變的

所謂元組的不可變指的是元組所指向的內存中的內容不可變。

```
tup66 = ('s', 't', 'a', 'r', 'w', 'a', 'r', 's')
tup66[0] = 'S'
Traceback (most recent call last):
tup66[0] = 'S'
typeError: 'tuple' object does not support item assignment
```
從以上實例可以看出，重新賦值的元組 tup，綁定到新的對象了，不是修改了原來的對象。

## Python3 字典

在 Python3 中字典(dictionary，簡寫為 dict)是另一種可變容器模型，且可存儲任意類型對象。

字典的每個鍵值(key=>value) 對用冒號(:)分割，每個對之間用逗號(,)分割，整個字典包括在花括號({})中，格式如下所示：

```
dict = {key1 : value1, key2 : value2}
```
鍵必須是唯一的，但值則不必(上表中 Danna 和 Alice 的鍵是不同的，值卻是相同的)。值可以取任何數據類型，但鍵必須是不可變的，如字符串，數字或元組。

一個簡單的字典實例：

```
dict={'China': 'CN', 'Hong Kong': 'HK', 'Taiwan': 'TW'}
```
也可如此創建字典：

```
dict1= {
China':86}
dict2 = {'Hong Kong': 22.30858031775129, 114.16673551288073}
```
訪問字典裡的值

與列表取值類似，但列表取值時使用索引，字典取值時使用 key，如下實例：

以上實例輸出結果：

```
dict[Country]: China
dict[code]: 86
```
修改字典

向字典添加新內容的方法是增加新的鍵/值對，修改或刪除已有鍵/值對如下實例：

```
dict = {'Country': 'China', 'abbreviation': 'CN', 'code': '86'}
dict['Country'] = 'Hong Kong'
dict['abbreviation'] = "HK"
dict['code'] = 852
print("dict[Country]: ", dict['Country'])
print("dict['abbreviation']: ", dict['abbreviation'])
print("dict[code]: ", dict['code'])
```
以上實例輸出結果：

```
dict[Country]: Hong Kong
dict['abbreviation']: HK
dict[code]: 852
```
## 字典鍵的特性

字典值可以沒有限制地取任何 Python 對象，既可以是標準的對象，也可以是用戶定義的，但鍵不行。

兩個重要的點需要記住：

1. 不允許同一個鍵出現兩次。創建時如果同一個鍵被賦值兩次，後一個值會被記住，如下實例：

```
dict = {'Country': 'China', 'abbreviation': 'CN', 'code': '86', 'Country': 'Taiwan'}
print("dict[Country]:", dict['Country'])
```
以上實例輸出結果：

```
dict[Country]: Taiwan
```
2. 鍵必須不可變，所以可以用數字，字符串或元組充當，而用列表就不行，如下實例：

```
dict = {['Country']: 'China', 'abbreviation': 'CN', 'code': 86}
print("dict['Country']: ",dict['Country'])
```
以上實例輸出結果：

```
Traceback (most recent call last):
...\index.py", line 23, in
dict = {['Country']: 'China', 'abbreviation': 'CN', 'code': 86}
TypeError: unhashable type: 'list'
```
字典內置函數&方法

Python 字典包含了以下內置函數：

len() 計算字典元素個數，即鍵的總數。

```
dict = {'Country': 'China', 'abbreviation': 'CN', 'code': 86}
print(len(dict))
```
str() 以字符串的形式輸出字典(字符串可打印，字典不可打印)。

```
dict = {'Country': 'China', 'abbreviation': 'CN', 'code': 86}
print(str(dict))
```
type() 返回輸入的變量類型，如果變量是字典就返回字典類型。

```
dict = {'Country': 'China', 'abbreviation': 'CN', 'code': 86}
print(type(dict))
```
## Python3 集合

集合(set)是一個無序的不重複元素序列。因此在每次運行的時候集合的運行結果的內容都是相同的，但元素的排列順序卻不是固定的，所以本章中部分案例的運行結果會出現與給出結果不同的情況(運行結果不唯一)。

可以使用大括號 { } 或者 set() 函數創建集合，注意：創建一個空集合必須用 set() 而不是 { }，因為 { } 是用來創建一個空字典。

創建格式：

```
parame = {value01,value02,...}
```
或者

```
set(value)
```
集合實例：

```
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
print(basket) # 這裡演示的是去重功能
print('orange' in basket) # 快速判斷元素是否在集合內
print('crabgrass' in basket)
```
運行結果：

```
{'pear', 'banana', 'orange', 'apple'}
True
False
```
集合的運算：

```
a = set('abracadabra')
b = set('alacazam')
print(a)
print(b)
print(a-b)
print(a|b)
print(a&b)
print(a^b)
```
運行結果：

```
{'b', 'd', 'a', 'c', 'r'}
{'1', 'z', 'm', 'a', 'c'}
{'r', 'd', 'b'}
{'1', 'z', 'b', 'm', 'd', 'a', 'c', 'r'}
{'c', 'a'}
{'1', 'z', 'b', 'm', 'r', 'd'}
```
## 集合的基本操作

添加元素語法格式如下：

```
s.add(x)
```
將元素 x 添加到集合 s 中，如果元素已存在，則不進行任何操作。

```
thisset = set("s", "ss", "sss")
thisset.add("ssss")
print(thisset)
```
運行結果：

```
{'s', 'ss', 'ssss', 'sss'}
```
還有一個方法，也可以添加元素，且參數可以是列表，元組，字典等，語法格式如下：

```
s.update(x)
```
x 可以有多個，用逗號分開。

實例：

```
thisset = set("s", "ss", "sss")
thisset.update({'s1', 1})
print(thisset)
thisset.update([11, 1], ["s1", "s2"])
print(thisset)
```
移除元素

語法格式如下：

```
s.remove(x)
```
將元素 x 從集合 s 中移除，如果元素不存在，則會發生錯誤。

實例：

```
thisset = set("s", "ss", "sss")
thisset.remove('sss')
print(thisset)
```
用 remove() 如果元素不存在，會發生錯誤

用 discard() 如果元素不存在，不會發生錯誤隨機刪除集合中的一個元素，語法格式如下：

```
s.pop()
```
實例：

```
thisset = set("s", "ss", "sss")
```
輸出結果：

```
1.
s
{'sss', 'ss'}
2.
sss
{'s', 'ss'}
3.
ss
{'sss', 's'}
4.
ss
{'sss', 's'}
```
## 結果每次都不同

set 集合的 pop 方法會對集合進行無序的排列，然後將這個無序排列集合的左面第一個元素進行刪除。因為這個過程是不確定的，所以刪除結果也是不確定的，不建議使用這種方式進行刪除。

計算集合元素個數

語法格式如下：

計算集合 s 的元素個數。

實例：

```
thisset = set("s", "ss", "sss")
print(len(thisset))
```

