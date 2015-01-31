#coding=utf-8

import Channel
import Logging
import Queue
from functools import partial

BUFFSIZE = 1024


class TcpConnection:
	"""
	TcpConnection handle I/O events.
	"""

	def __init__(self, loop, name, conn, addr):

		"""

		:rtype : TcpConnection
		"""
		self._loop = loop
		self._name = name
		self._conn = conn
		self._peer = addr
		self._channel = Channel.Channel(loop, conn.fileno())

		self._channel.set_read_callback(self.handle_read)
		self._channel.set_write_callback(self.handle_write)

		self._connection_cb = None
		self._message_cb = None
		self._write_complete_cb = None
		self._close_cb = None

		self._read_queue = Queue.Queue()
		self._write_queue = Queue.Queue()

		Logging.debug('TcpConnection::__init__ [%s] at [%d]' % (self._name, self._conn.fileno()))

	def name(self):
		return self._name

	def get_loop(self):
		return self._loop

	def handle_read(self):
		self._loop.assert_thread()

		res = None
		try:
			res = self._conn.recv(BUFFSIZE)
		except (OSError, IOError) as e:
			from DefaultPoller import error_from_exception
			import errno
			if error_from_exception(e) == errno.EPIPE:
				Logging.error('TcpConnection::handle_read errno.EPIPE')
			elif error_from_exception(e) == errno.EINTR:
				Logging.error('TcpConnection::handle_read errno.EINTR')
			elif error_from_exception(e) in [errno.EWOULDBLOCK, errno.EAGAIN]:
				Logging.debug('TcpConnection::handle_read errno.EGAIN, EWOULDBLOCK')
			else:
				import traceback
				Logging.error(e)
				traceback.print_exc()
				return

		if res:
			self._message_cb(self, res)
		else:
			Logging.info('TcpConnection::handle_read closing socket')
			self.handle_close()

	def handle_write(self):
		"""
		if have write event, pick a top from write queue and
		call system send() with nonblocking write, if there are
		data left to write, put them in end of the queue
		"""
		self._loop.assert_thread()
		if self._channel.is_writing():
			data = ''
			try:
				data = self._write_queue.get_nowait()
			except Queue.Empty:
				Logging.info('TcpConnection::handle_write write queue empty')

			# n = self._conn.send(data)
			n = 0
			try:
				n = self._conn.send(data)
			except (OSError, IOError) as e:
				from DefaultPoller import error_from_exception
				import errno
				if error_from_exception(e) == errno.EPIPE:
					Logging.error('TcpConnection::handle_write errno.EPIPE')
					return
				elif error_from_exception(e) == errno.EINTR:
					Logging.error('TcpConnection::handle_write errno.EINTR')
				elif error_from_exception(e) in [errno.EWOULDBLOCK, errno.EAGAIN]:
					Logging.debug('TcpConnection::handle_write errno.EGAIN, EWOULDBLOCK')
				else:
					import traceback
					Logging.error(e)
					traceback.print_exc()
					return

			# no error
			if n >= 0:
				remaining = len(data) - n
				# have write finish
				if remaining == 0 and self._write_complete_cb:
					self._loop.queue_in_loop(self._write_complete_cb)
			pass

	def handle_close(self):
		self._loop.assert_thread()
		if self._close_cb:
			self._close_cb(self)

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
		self._channel.set_read_enable()  # update channel(regist channel into loop)
		if self._connection_cb:
			self._connection_cb(self)

	def connection_destroyed(self):
		self._loop.assert_thread()
		self._channel.remove()
		self._channel.set_all_disable()
		pass

	def send(self, data):
		if self._loop.in_current_thread():
			self.__send_in_loop(data=data)
		else:
			_sil = partial(self.__send_in_loop, data)
			self._loop.run_in_loop(_sil)

	def __send_in_loop(self, data):
		self._loop.assert_thread()
		remaining = len(data)
		# if no thing in output queue, try writing directly
		# ͨ��û�й�ע��д�¼� ���ҷ��ͻ������û����� ֱ��write
		if not self._channel.is_writing() and self._write_queue.empty():
			try:
				n = self._conn.send(data)
			except (OSError, IOError) as e:
				from DefaultPoller import error_from_exception
				import errno
				if error_from_exception(e) == errno.EPIPE:
					Logging.error('TcpConnection::__send_in_loop errno.EPIPE')
					return
				elif error_from_exception(e) == errno.EINTR:
					Logging.error('TcpConnection::__send_in_loop errno.EINTR')
				elif error_from_exception(e) in [errno.EWOULDBLOCK, errno.EAGAIN]:
					Logging.debug('TcpConnection::__send_in_loop errno.EGAIN, EWOULDBLOCK')
				else:
					import traceback
					Logging.error(e)
					traceback.print_exc()
					return

			# no error
			if n >= 0:
				remaining = len(data) - n
				# have write finish
				if remaining == 0 and self._write_complete_cb:
					self._loop.queue_in_loop(self._write_complete_cb)

		# there are some data need to be send
		if remaining > 0:
			self._write_queue.put(data[n:])
			if not self._channel.is_writing():
				self._channel.set_write_enble()


