import re
'''正则表达式'''

'''
元字符表
. 匹配除换行符以外的任何单个字符，如"r.d"会匹配red,r d等，但是不会匹配read
* 匹配位于*之前的任意个字符，如"r*ed"会匹配rred,rrred,red等
+ 匹配位于+之前的一个或者多个字符（不能是0个）。如"r+ed"会匹配rred,rrred，但不会匹配"red"
? 匹配位于?之前的0个或者一个字符，如"r?ed"会匹配rred,red,不会匹配rrred
| 匹配位于|之前的或者之后的字符，如"red|blue"会匹配red,blue
^ 匹配行首
$ 匹配行尾
\ 匹配位于\之后的转义字符
[] 匹配位于[]中的任何一个字符，如r[ae]d，会匹配rad,red
() 将位于()中的内容作为一个整体
{} 按{}中的次数进行匹配
'''

'''
元字符还可以组合起来使用
.* 匹配任意个字符
.+ 匹配任意的一个或者多个字符
.? 匹配任意的0个或者一个字符
[a-zA-Z0-9]表示任意的字母或者数字
匹配网址：(http://www|www)\.[a-z0-9-]*\.[a-z]{2,3}
'''

'''
re模块
re.match()从字符串的第一个字符开始匹配
re.search()搜索整个字符串进行匹配
re.findall()在字符串中查找所有符合正则表达式的字符串，返回为一个列表
'''
s = 'Life can be good'
print re.match('can', s)
print re.search('can', s)
print re.match('l.*', s, re.I)#忽略大小写
re.findall('[a-z]{3}', s)
re.findall('[a-z]{1,3}', s)

'''
re.sub()用于替换字符串中符合正则的内容，返回替换后的字符串
re.subn()返回的则是一个元组
'''
s = 'Life can be bad'
re.sub('bad', 'good', s)
re.sub('bad|be', 'good', s)
re.sub('bad|be', 'good', s, 1)#只替换一次
re.subn('bad|be', 'good'. s, 1)#返回('Life can good bad', 1)

'''
以'\'开头的元字符
\b 匹配单词头或者单词尾
\B 与\b含义相反
\d 匹配任何数字
\D 匹配任何非数字
\s 匹配任何空白字符
\S 匹配任何非空白字符
\w 匹配任何字母，数字以及下划线
\W 与\w含义相反
在正则表达式中使用\b应写成\\b,比如re.compile('\\ba.?')，否则使用原始字符re.compile(r'\ba.?')
'''
s = 'Python can run on Windows'
re.findall('\\bo.+?\\b', s)#查找首字母为o的单词
re,findall('\\Bo.+?', s)#查找含字母o的单词，但不是首字母

'''
使用组：使用"()"来表示位于其中的内容属于一个组
'''
s = 'Phone No. 010-87654321'
r = re.compile(r'(\d+)-(\d+)')
m = r.search(s)
m.group(1)#'010'
m.group(2)#'87654321'
m.groups()#('010','87654321')

'''
通过使用"(?P<组名>)"为组设置一个名字
'''
s = 'Phone No. 010-87654321'
r = re.compile(r'(?P<Area>\d+)-(?P<No>\d+)')
m = r.search(s)
m.group('Area')#'010'
m.group('No')#'87654321'
m.groupdict()#{'Area':010','No':87654321'}







