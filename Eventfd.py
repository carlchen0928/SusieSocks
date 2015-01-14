import socket

def eventfd_create():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('127.0.0.1', 9999))
	s.listen(5)


def eventfd_read(sock):
	return sock.recv(1)
	pass


def eventfd_write(sock):
	temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	temp.connect(sock.getsockname())
	temp.send(1)
	temp.close()
	pass