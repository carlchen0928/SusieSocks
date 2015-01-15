import socket
import Logging


def eventfd_create():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as msg:
		Logging.error('eventfd_create create error %s' % msg)

	try:
		s.bind(('localhost', 0))
	except socket.error as msg:
		Logging.error('eventfd_create bind error %s' % msg)

	s.listen(5)


def eventfd_read(sock):
	return sock.recv(1)


def eventfd_write(sock):
	try:
		stemp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as msg:
		Logging.error('eventfd_write create error %s' % msg)
		return

	try:
		stemp.connect(sock.getsockname())
	except socket.error as msg:
		Logging.error('eventfd_write connect error %s' % msg)
		return

	n = stemp.send('1')
	if n != 1:
		Logging.error('event_write send error')

	stemp.close()