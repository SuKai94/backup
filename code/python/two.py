#coding: utf-8
'''
Decorator in Python
URL:
1)http://coolshell.cn/articles/11265.html
2)http://www.cnblogs.com/rhcad/archive/2011/12/21/2295507.html
'''

'''N1'''
def hello1(fn):
	print "i am hello1"
	def wrapper():
		print "hello1, %s" % fn.__name__
		fn()
		print "goodbye1, %s" % fn.__name__
	print "here"
	return wrapper

'''
foo = hello(foo)
'''
@hello1
def foo():
	print "i am foo"

foo()

'''N2 计数器'''
def logging_decorator(func):
    def wrapper():
        wrapper.count += 1
        print "The function I modify has been called {0} time(s)".format(wrapper.count)
        func()
    wrapper.count = 0
    return wrapper

@logging_decorator
def a_function():
    print "I'm a normal function."

a_function()

a_function()

'''N3 使用*args'''
'''1）形参使用'''
def function_with_many_arguments(*args):
    print args

function_with_many_arguments('hello', 123, True)

'''2）实参使用'''
def function_with_3_parameters(num, boolean, string):
    print "num is " + str(num)
    print "boolean is " + str(boolean)
    print "string is " + string

arg_list = [1, False, 'decorators']

# arg_list will be expanded into 3 positional arguments by the `*` symbol
function_with_3_parameters(*arg_list)

'''N4 使用**kwargs'''
'''1）形参使用'''
def function_with_many_keyword_args(**kwargs):
	print kwargs

function_with_many_keyword_args(a='apples', b='bananas', c='cantalopes')

'''2）实参使用'''
def multiply_name(count=0, name=''):
    print name * count

arg_dict = {'count': 3, 'name': 'Brian'}

multiply_name(**arg_dict)

'''类的装饰器'''
foo = ['important', 'foo', 'stuff']

def add_foo(klass):
    klass.foo = foo
    return klass

@add_foo
class Person(object):
    pass

brian = Person()
print brian.foo

'''装饰器类'''
class IdentityDecorator(object):
    def __init__(self, func):
        self.func = func

    def __call__(self):
        self.func()

@IdentityDecorator
def a_function():
    print "I'm a normal function."

a_function()

'''带参数的装饰器'''
def deco(func):
    def wrapper(a, b):
        print "before myfunc() called."
        ret = func(a, b)
        print "after myfunc() called. result: %s" % ret
        return ret
    return wrapper
 
@deco
def myfunc(a, b):
    print " myfunc(%s,%s) called." % (a, b)
    return a + b
 
myfunc(1, 2)

'''对参数不确定的函数进行装饰'''
def deco(func):
    def _deco(*args, **kwargs):
        print "before %s called." % func.__name__
        ret = func(*args, **kwargs)
        print "after %s called. result: %s" % (func.__name__, ret)
        return ret
    return _deco
 
@deco
def myfunc(a, b):
    print "myfunc(%s,%s) called." % (a, b)
    return a+b
 
@deco
def myfunc2(a, b, c):
    print "myfunc2(%s,%s,%s) called." % (a, b, c)
    return a+b+c
 
myfunc(1, 2)
myfunc2(3, 4, 5)

'''让装饰器带参数'''
def deco(arg):
    def _deco(func):
        def __deco():
            print("before %s called [%s]." % (func.__name__, arg))
            func()
            print("  after %s called [%s]." % (func.__name__, arg))
        return __deco
    return _deco
 
@deco("mymodule")
def myfunc():
    print(" myfunc() called.")
 
@deco("module2")
def myfunc2():
    print(" myfunc2() called.")
 
myfunc()
myfunc2()