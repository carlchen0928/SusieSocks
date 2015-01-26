import socket
import EventLoop
import select
import Poller
import Logging

NoneEvent = 0
ReadEvent = (Poller.POLL_IN | Poller.POLL_PRI)
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

	def set_read_callback(self, read_cb):
		self._readCallback = read_cb

	def set_write_callback(self, write_cb):
		self._writeCallback = write_cb

	def set_err_callback(self, err_cb):
		self._errCallback = err_cb

	def set_read_enable(self):
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

	def set_all_disable(self):
		self._event &= ~WriteEvent
		self._event &= ~ReadEvent
		self.update()

	def set_revent(self, revent):
		self._revent = revent

	def fd(self):
		return self._fd

	def event(self):
		return self._event

	def is_none_event(self):
		return self._event is NoneEvent

	def handle_event(self):
		if self._revent & Poller.POLL_HUP:
			Logging.error('Channel::handle_event() POLL_HUP, fd: %d' % self.fd())

		if self._revent & Poller.POLL_NVAL:
			Logging.error('Channel::handle_event() POLL_NVAL, fd: %d' % self.fd())

		if self._revent & Poller.POLL_ERR:
			Logging.error('Channel::handle_event() POLL_ERR, fd: %d' % self.fd())
			if self._errCallback:
				self._errCallback()

		if self._revent & (Poller.POLL_IN | Poller.POLL_PRI):
			if self._readCallback:
				self._readCallback()

		if self._revent & Poller.POLL_OUT:
			if self._writeCallback:
				self._writeCallback()

	def update(self):
		assert isinstance(self._loop, EventLoop)
		self._loop.update_channel(self)

	def owner_loop(self):
		return self._loop

	def is_writing(self):
		return self._event & WriteEvent

	def remove(self):
		self._loop.remove_channel(self)


