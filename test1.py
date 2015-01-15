import socket
import errno


def errno_from_exception(e):
	"""Provides the errno from an Exception object.

	There are cases that the errno attribute was not set so we pull
	the errno out of the args but if someone instatiates an Exception
	without any args you will get a tuple error. So this function
	abstracts all that behavior to give you a safe way to get the
	errno.
	"""

	if hasattr(e, 'errno'):
		return e.errno
	elif e.args:
		return e.args[0]
	else:
		return None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 0))
s.connect(('127.0.0.1', 21424))
s.setblocking(0)

sendstr = '012345678901234567890987653472461278463128462378'
i = 20
while i > 0:
	sendstr += sendstr
	i -= 1

while True:
	try:
		n = s.send(sendstr)
		print n
	except (OSError, IOError) as e:
		if errno_from_exception(e) == errno.EPIPE:
			print 'epipe'
		elif errno_from_exception(e) == errno.EINTR:
			print 'eintr'
		elif errno_from_exception(e) == errno.EWOULDBLOCK:
			print 'ewouldblock'
			print 'already send %d' % n
			print 'left %d' % (len(sendstr) - n)
		elif errno_from_exception(e) == errno.EAGAIN:
			print 'eagain'
		else:
			print 'nonononon'