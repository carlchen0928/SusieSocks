
class my:
	def __init__(self):
		self.h = 'haha'

	def set(self):
		self.h = 'xixi'

m = my()
print m.h

def func(arg):
	arg.set()
	print arg.h

func(m)
print m.h