import EventLoop
import Acceptor
import DefaultCallbacks
import Logging


class TcpServer:
	def __init__(self, loop, server_addr, name, option=True):
		self._loop = loop
		self._port = server_addr[1]
		self._name = name
		self._acceptor = Acceptor.Acceptor(loop, server_addr, option)
		self._connection_cb = DefaultCallbacks.default_connection_cb
		self._message_cb = DefaultCallbacks.default_message_cb
		self._started = False

		self._acceptor.set_newconnection_cb(self.new_connection)

	def start(self):
		if not self._started:
			assert not self._acceptor.listenning()
			self._loop.run_in_loop(self._acceptor.listen)

	def new_connection(self, conn, addr):
		self._loop.assert_thread()
		conn_name = self._name + str(addr)
		Logging.info('TcpServer::new_connection [%s] --> [%s]' % (self._name, conn_name))
		conn = TcpConnection()

		pass

	def __del__(self):
		pass