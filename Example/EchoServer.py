__author__ = 'yiyu'


import TcpServer
import EventLoop
import Logging


class EchoServer:
	def __init__(self, loop, addr):
		self._server = TcpServer.TcpServer(loop, addr, 'echo_server')
		self._server.set_connection_cb(self.on_connection)
		self._server.set_message_cb(self.on_message)
		pass

	def start(self):
		self._server.start()
		pass

	def on_connection(self, conn):
		Logging.info('Echo Server on_connection')
		pass

	def on_message(self, conn, buff):
		Logging.info('Get message: %s' % buff)
		conn.send(buff)
		pass



loop = EventLoop.EventLoop()
es = EchoServer(loop, ('0.0.0.0', 8222))
es.start()
loop.loop()