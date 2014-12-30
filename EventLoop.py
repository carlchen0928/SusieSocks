import socket
import Poller
import Channel
import Logging
import threading


class EventLoop:
	def __init__(self):
		self._looping = False
		self._quit = False
		self._poller = Poller()
		self._activeChannels = []
		self._currentChannel = None
		self._tid = threading.current_thread().ident
		pass

	def loop(self):
		assert not self._looping
		self.assert_thread()
		self._looping = True
		self._quit = False
		Logging.debug('EventLoop start looping')

		while not self._quit:
			self._activeChannels = []
			try:
				self._activeChannels = self._poller.poll()
			except:
				pass
		pass

	def assert_thread(self):
		if not self.in_current_thread():
			Logging.critical('EventLoop should run in one thread. '
							 'Current thread is %d, Created thread is %d'
							 % (threading.current_thread().ident, self._tid))

	def in_current_thread(self):
		return threading.current_thread().ident == self._tid

	def quit(self):
		self._quit = True

		# maybe this loop have been hang up or into sleep,
		# in other thread, we want this thread quit, we should
		# at first to wake him up, and he will run into loop
		if not self.in_current_thread():
			wakeup_self()

	def update_channel(self, channel):
		assert self == channel.owner_loop()
		self.assert_thread()
		self._poller.update_channel(channel)

	def remove_channel(self, channel):
		assert self == channel.owner_loop()
		self.assert_thread()
		self._poller.remove_channel(channel)

	def has_channel(self, channel):
		assert self == channel.owner_loop()
		self.assert_thread()
		self._poller.has_channel(channel)

