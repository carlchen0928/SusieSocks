import socket
import EventLoop
import select
import Poller

NoneEvent = 0
ReadEvent = Poller.POLL_IN
WriteEvent = Poller.POLL_OUT


class Channel:
	def __init__(self, loop, fd):
		self._loop = loop
		self._fd = fd
		self._readCallback = None
		self._writeCallback = None
		self._errCallback = None
		self._revent = 0
		self._event = -1
		pass

	def set_read_callback(self, read_cb):
		self._readCallback = read_cb

	def set_write_callback(self, write_cb):
		self._writeCallback = write_cb

	def set_err_callback(self, err_cb):
		self._errCallback = err_cb

	def set_read_enble(self):
		self._event |= ReadEvent
		self.update()

	def set_read_disable(self):
		self._event &= ~ReadEvent
		self.update()

	def set_write_enble(self):
		self._event |= WriteEvent
		self.update()

	def set_write_disable(self):
		self._event &= ~WriteEvent
		self.update()

	def fd(self):
		return self._fd

	def event(self):
		return self._event

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

	def update(self):
		assert isinstance(self._loop, EventLoop)
		self._loop.update_channel(self)


