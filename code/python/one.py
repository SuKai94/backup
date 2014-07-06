#coding: utf-8
'''
函数式编程
URL:http://coolshell.cn/articles/10822.html

函数式编程的好处：
1）代码更加简单
2）数据集，操作，返回值都放在了一起
3）读代码时，没有循环体，于是就少了一些临时变量，及变量倒来倒去
4）代码变成了在描述你要干什么，而不是怎么去干
'''

'''N1'''
login = 0

def is_login(f):
	def wrapper():
		if login == 1:
			print "login in html"
			f()
		else:
			print "logining html"
	return wrapper

@is_login
def test():
	print "i am test"

test()

'''N2'''
def inc(x):
	print 'inc()'
	def incx(y):
		print 'incx()'
		return x+y
	return incx

inc2 = inc(2)
inc5 = inc(5)

print inc2(5)
print inc5(5)

'''N3'''
def toupper(item):
	return item.upper()

upper_name = map(toupper, ["ni", "hao", "a"])
print upper_name

'''N4'''
squares = map(lambda x:x*x, range(3))
print squares

'''N5'''
print reduce(lambda x,y:x+y, [1,2,3])

'''N6'''
num = [2, -5, 9, 7, -2, 5, 3, 1, 0, -3, 8]
positive_num = filter(lambda x:x>0, num)
average = reduce(lambda x,y:x+y, positive_num) / len(positive_num)
print average


