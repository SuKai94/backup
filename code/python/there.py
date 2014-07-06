#coding: utf-8
import threading
import time

'''func函数没有等待线程完成就输出了0 1 2 3 4，除非加入线程的join（）函数'''
class mythread(threading.Thread):
	def __init__(self, id):
		threading.Thread.__init__(self)
		self.id = id

	def run(self):
		time.sleep(10)
		print 'i am', self.id

def func():
	t.start()
	t.join()
	for i in range(5):
		print i

t = mythread(2)
func()

'''isAlive查看线程是否运行'''
class mythread(threading.Thread):
	def __init__(self, id):
		threading.Thread.__init__(self)
		self.id = id

	def run(self):
		print 'i am', self.id

def func():
	t.start()
	print t.isAlive()

t = mythread(2)
func()

'''setName(),getName()'''
class mythread(threading.Thread):
	def __init__(self, threadname):
		threading.Thread.__init__(self, name=threadname)

	def run(self):
		print self.getName()

t = mythread('tt')
t.start()
t.setName('TT')
print t.getName()

'''
setDaemon()
主线程退出，不管子线程是否完成都随着主线程退出
'''


'''
简单的线程同步,对全局变量i的操作放在acquire和release之间，每次仅允许一个线程对i进行操作
也可以使用ondition()对象，使用条件变量保持线程同步
还可以使用队列保持线程同步
'''
class mythread(threading.Thread):
	def __init__(self, threadname):
		threading.Thread.__init__(self, name=threadname)

	def run(self):
		global x
		lock.acquire()
		for i in range(3):
			x = x + 1
		time.sleep(2)
		print x
		lock.release()

lock = threading.RLock()
t1 = []
for i in range(10):
	t = mythread(str(i))
	t1.append(t)

x = 0
for i in t1:
	i.start()

'''
线程间通信
使用Event对象实现线程间的通信
'''
class mythread(threading.Thread):
	def __init__(self, threadname):
		threading.Thread.__init__(self, name = threadname)

	def run(self):
		global event
		if event.isSet():
			event.clear()
			event.wait()
			print self.getName()
		else:
			print self.getName()
			event.set()

event = threading.Event()
event.set()
t1 = []
for i in range(10):
	t = mythread(str(i))
	t1.append(t)

for i in t1:
	i.start()





