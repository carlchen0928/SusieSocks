import socket
import EventLoop
import select
import Poller


class Channel:
	def __init__(self, loop, fd):
		self._loop = loop
		self._fd = fd
		self._readCallback = None
		self._writeCallback = None
		self._errCallback = None
		self._revent = 0
		pass

	def set_read_callback(self, read_cb):
		self._readCallback = read_cb

	def set_write_callback(self, write_cb):
		self._writeCallback = write_cb

	def set_err_callback(self, err_cb):
		self._errCallback = err_cb

	def fd(self):
		return self._fd

	def handle_event(self):
		if self._revent & Poller.POLL_HUP:
			print 'Channel::handle_event() POLL_HUP'

		if self._revent & Poller.POLL_NVAL:
			print 'Channel::handle_event() POLL_NVAL'

		if self._revent & Poller.POLL_ERR:
			print 'Channel::handle_event() POLL_ERR'
			if self._errCallback:
				self._errCallback()

		if self._revent & Poller.POLL_IN:
			if self._readCallback:
				self._readCallback()

		if self._revent & Poller.POLL_OUT:
			if self._writeCallback:
				self._writeCallback()


