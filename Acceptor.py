import socket
import Logging
import Channel
import EventLoop

def create_listen_fd():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
	sock.setblocking(False)
	return sock



class Acceptor:
	def __init__(self, loop, addr, reuseport):
		self._loop = loop
		self._sock = create_listen_fd()
		if reuseport:
			if hasattr(socket, 'SO_REUSEPORT'):
				self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
			else:
				Logging.error('system not support SO_REUSEPORT')

		assert isinstance(addr, tuple)

		self._sock.bind(addr)

		self._channel = Channel(loop, self._sock.fileno())
		self._channel.set_read_callback(self.handle_read)
		self._newconnection_cb = None
		self._listenning = False

	def set_newconnection_cb(self, callback):
		self._newconnection_cb = callback

	def handle_read(self):
		self._loop.assert_thread()

		(conn, addr) = self._sock.accept()
		Logging.debug('accept a new connection (%s:%d)' % addr)

		if conn:
			if self._newconnection_cb:
				self._newconnection_cb(conn, addr)
			else:
				conn.close()

	def listen(self):
		self._loop.assert_thread()
		self._listenning = True
		self._sock.listen(5)
		self._channel.set_read_enble()
		Logging.debug('start listen on %s' % self._sock.getsockname())

	def listenning(self):
		return self._listenning