__author__ = 'yiyu'


class B:
	def __init__(self, a):
		self._a = a

	def p(self):
		print self._a

def cal(func, **kwargs):
	if func:
		if kwargs:
			func(kwargs)
		else:
			func()


b = B(10)

cal(b.p)