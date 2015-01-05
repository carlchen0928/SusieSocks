import socket

def create_listen_fd():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
	sock.setblocking(False)
	return sock



class Acceptor:
	def __init__(self, loop, addr, reuseport):
		self._loop = loop
		self._sock = create_listen_fd()
		pass