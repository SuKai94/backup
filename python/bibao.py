#coding: utf-8

'''
s_bibao函数功能：求属性集的闭包。
函数参数为：所有输入的函数依赖列表f，属性集s。
函数返回值：s+
'''
def s_bibao(f, s):
	while True:
		'''azjb函数功能：判断字符串a是不是字符串b的子集'''
		azjb = lambda a,b:True if len(filter(lambda x:x in list(b), list(a)))==len(a) else False
		a = filter(lambda x:azjb(x.split('->')[0], s) and not azjb(x.split('->')[1], s), f)
		if not len(a):
			return s
		s = s + ''.join(map(lambda x:x.split('->')[1], a))

'''
sub函数：求集合father的所有子集
'''
sub = lambda father: reduce(lambda x,y:[z.union([y]) for z in x] + x, father, [set()])

'''
函数功能：求所有的函数依赖关系F+
'''
def all_bibao(attribute, f):
	'''attr_son为attribute集合的所有子集列表'''
	attr_son = sub(attribute)
	res = []
	for t in attr_son:
		t_s = ''.join(list(t))
		if not len(t_s):
			continue
		son = sub(list(s_bibao(f, t_s)))
		for t1 in son:
			t1_s = ''.join(list(t1))
			if len(t1_s):
				res.append('%s->%s' % (t_s, t1_s))
			else:
				res.append('%s->%s' % (t_s, 'NULL'))
	return res

'''
all_attribute函数：求得所有出现的属性
'''
def all_attribute(attribute, all_t):
	for t in all_t:
		if t not in attribute:
			attribute.append(t)
	return attribute
	

if __name__ == '__main__':
	print '请输入函数依赖,假定所有的属性都是大写字母A到Z表示。'
	print '先输入依赖左边的属性，然后再输入依赖右边的属性，表示A->B。输入END结束。'
	
	'''
	f列表用于存放所有函数依赖，存放格式为A->B
	attribute列表用于存放所有出现的属性
	'''
	f = []
	attribute = []

	'''输入所有函数依赖，注意考虑异常'''
	flag = num = 1
	while True:
		t = raw_input()
		if t.upper()=='END':
			break
		if not t:
			continue
		if ' ' in t:
			if len(t.split()) == 1:
				if (flag%2):				
					left_t = ' '.join(t.split())
					flag = flag+1
				else:
					right_t = ' '.join(t.split())
					t = left_t.upper()+'->'+right_t.upper()
					print '完成第',num,'个依赖 ',t
					attribute = all_attribute(attribute, all_t = (left_t.upper()+right_t.upper()))
					f.append(t)
					num = num+1
					flag = flag+1
				continue
			if len(t.split()) == 0:
				continue
			t = ' '.join(t.split())
			(left_t,right_t) = t.split(' ')
			t = left_t.upper()+'->'+right_t.upper()
			print '完成第',num,'个依赖 ',t
			attribute = all_attribute(attribute, all_t = (left_t.upper()+right_t.upper()))
			f.append(t)
			num = num+1
			continue
		if (flag%2):
			left_t = t
			flag = flag+1
		else:
			right_t = t
			t = left_t.upper()+'->'+right_t.upper()
			print '完成第',num,'个依赖 ',t
			attribute = all_attribute(attribute, all_t = (left_t.upper()+right_t.upper()))
			f.append(t)
			num = num+1
			flag = flag+1
	
	while True:
		t = raw_input('请输入属性集求闭包\n')
		if t.upper() == 'END':
			break
		res = t.upper()+'+: '+'%s' % s_bibao(f, t.upper())
		print res
	
	# print sub(attribute)
	res = all_bibao(attribute, f)
	print len(res)
	print '你输入的函数依赖的闭包F+是：'
	for t in res:
		print t


