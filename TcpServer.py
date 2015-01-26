import EventLoop
import Acceptor
import DefaultCallbacks
import Logging
import TcpConnection


class TcpServer:
	def __init__(self, loop, server_addr, name, option=True):
		self._loop = loop
		self._port = server_addr[1]
		self._name = name
		self._acceptor = Acceptor.Acceptor(loop, server_addr, option)
		self._connection_cb = DefaultCallbacks.default_connection_cb
		self._message_cb = DefaultCallbacks.default_message_cb
		self._started = False
		self._connections = {}

		self._acceptor.set_newconnection_cb(self.new_connection)

	def set_connection_cb(self, cb):
		self._connection_cb = cb

	def set_message_cb(self, cb):
		self._message_cb = cb

	def set_write_complete_cb(self, cb):
		pass

	def start(self):
		if not self._started:
			assert not self._acceptor.listenning()
			self._loop.run_in_loop(self._acceptor.listen)

	def new_connection(self, conn, addr):
		"""

		:rtype : void
		"""
		self._loop.assert_thread()
		conn_name = self._name + str(addr)
		Logging.info('TcpServer::new_connection [%s] --> [%s]' % (self._name, conn_name))
		new_conn = TcpConnection.TcpConnection(self._loop, conn_name, conn, addr)

		self._connections[conn_name] = new_conn

		new_conn.set_connection_callback(self._connection_cb)
		new_conn.set_message_callback(self._message_cb)
		new_conn.set_write_complete_callback(None)  # FIXME
		new_conn.set_close_callback(None)  # FIXME

		self._loop.run_in_loop(new_conn.connection_established)

		pass

	def remove_connection(self, conn):
		self._loop.run_in_loop(self.remove_connection_inloop, {'conn': conn})
		pass

	def remove_connection_inloop(self, conn):
		self._loop.assert_thread()
		Logging.info('TcpServer::remove_connection [%s] - [%s]' % (self._name, conn.name()))
		del self._connections[conn.name()]

		loop = conn.get_loop()
		loop.run_in_loop(conn.connection_destroyed)

	def __del__(self):
		self._loop.assert_thread()
		Logging.info('TcpServer::__del__ [%s]' % self._name)

		for it in self._connections:
			it.get_loop().run_in_loop(it.connection_destroyed)
		pass