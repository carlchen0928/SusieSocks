__author__ = 'yiyu'


# class B:
# 	def run1(self, func, **kargs):
# 		func(kargs)
#
# class A:
# 	def __init__(self, ba):
# 		self._st = '111'
# 		self._b = ba
#
# 	def func(self, data):
# 		self._b.run1(self.run, data=data)
#
# 	def run(self, data):
# 		print data['data']
# 		print self._st
#
#
#
#
# b = B()
# a = A(b)
# a.func('fadafd')

def func():
	try:
		n = 3
	except:
		print 'haha'

	print n

func()