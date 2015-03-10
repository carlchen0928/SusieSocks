__author__ = 'yiyu'


import TcpServer
import EventLoop
import Logging
import time


class TimeServer:
	def __init__(self, loop, addr):
		self._server = TcpServer.TcpServer(loop, addr, 'time_server')
		self._server.set_connection_cb(self.on_connection)
		self._server.set_message_cb(self.on_message)
		pass

	def start(self):
		self._server.start()
		pass

	def on_connection(self, conn):
		Logging.info('Time Server get connection %s' % conn.name())
		conn.send(time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime()))
		conn.shutdown()

	def on_message(self, conn, buff):
		Logging.info('discard message: %s from %s' % (buff, conn.name()))


loop = EventLoop.EventLoop()
es = TimeServer(loop, ('0.0.0.0', 8222))
es.start()
loop.loop()