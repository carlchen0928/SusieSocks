__author__ = 'yiyu'


class B:
	def run1(self, func, **kargs):
		if kargs != {}:
			print 'none'
			func(kargs)

class A:
	def __init__(self, ba):
		self._st = '111'
		self._b = ba

	def func(self):
		self._b.run1(self.run)

	def run(self):
		print self._st




b = B()
a = A(b)
a.func()
#
# def func():
# 	try:
# 		n = 3
# 	except:
# 		print 'haha'
#
# 	print n
#
# func()