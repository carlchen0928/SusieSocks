import Channel
import Logging
import Queue
import DefaultPoller

BUFFSIZE = 1024


class TcpConnection:
	"""
	TcpConnection handle I/O events.
	"""

	def __init__(self, loop, name, conn, addr):
		self._loop = loop
		self._name = name
		self._conn = conn
		self._peer = addr
		self._channel = Channel(loop, conn.fileno())

		self._channel.set_read_callback(TcpConnection.handle_read)
		self._channel.set_write_callback(TcpConnection.handle_write)

		self._connection_cb = None
		self._message_cb = None
		self._write_complete_cb = None
		self._close_cb = None

		self._read_queue = Queue()
		self._write_queue = Queue()

		Logging.debug('TcpConnection::__init__ [%s] at [%d]' % (self._name, self._fd))

	def handle_read(self):
		self._loop.assert_thread()
		res = self._conn.recv(BUFFSIZE)
		if res:
			self._message_cb(res)
		else:
			Logging.info('TcpConnection::handle_read closing socket')
			Logging.info(self._conn.getpeername())
			self.handle_close()

	def handle_write(self):
		pass

	def handle_close(self):
		self._loop.assert_thread()
		self._channel.set_all_diable()
		if self._close_cb:
			self._close_cb(self._conn)

	def handle_error(self):
		# TODO
		pass

	def set_message_callback(self, message_callback):
		self._message_cb = message_callback

	def set_connection_callback(self, connection_callback):
		self._connection_cb = connection_callback

	def set_write_complete_callback(self, write_complete_callback):
		self._write_complete_cb = write_complete_callback

	def set_close_callback(self, close_callback):
		self._close_cb = close_callback

	def connection_established(self):
		self._loop.assert_thread()
		self._channel.set_read_enable()
		if self._connection_cb:
			self._connection_cb()

	def send(self, data):
		if self._loop.assert_thread():
			self._conn.send(data)
		else:
			self.__send_inloop(data)

	def __send_in_loop(self, data):
		self._loop.assert_thread()

		if not self._channel.is_writing():
			n = self._conn.send(data)
