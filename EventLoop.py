import socket
import Poller
import Channel
import Logging
import threading
import Eventfd


class EventLoop:
	def __init__(self):
		self._looping = False
		self._quit = False
		self._poller = Poller()
		self._activeChannels = []
		self._currentChannel = None
		self._tid = threading.current_thread().ident
		self._event_handling = False
		self._eventfd = Eventfd.eventfd_create()
		self._event_channel = Channel.Channel(self, self._eventfd.fileno())
		self._pending_func = []
		self._mutex = threading.Lock()
		self._calling_pending = False
		pass

	def loop(self):
		assert not self._looping
		self.assert_thread()
		self._looping = True
		self._quit = False
		Logging.debug('EventLoop start looping')

		while not self._quit:
			self._activeChannels = []
			self._activeChannels = self._poller.poll()

			self._event_handling = True
			for chn in self._activeChannels:
				self._currentChannel = chn
				self._currentChannel.handle_event()

			self._currentChannel = None
			self._event_handling = False
			self.do_pending()

		self._looping = False
		Logging.info('EventLoop %d stop looping' % self._tid)

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
	# TODO: wait until this thread wakeup
	# if not self.in_current_thread():
	# 	self.wakeup()

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

	def run_in_loop(self, functor, **kargs):
		if self.in_current_thread():
			functor(kargs)
		else:
			self.queue_in_loop(functor, **kargs)

	def queue_in_loop(self, functor, **kargs):
		self._mutex.acquire()
		self._pending_func.append([functor, kargs])
		self._mutex.release()

		if not self.in_current_thread() or self._calling_pending:
			self.wake_up()

	def wake_up(self):
		Eventfd.eventfd_write(self._eventfd)

	def handle_read(self):
		n = Eventfd.eventfd_read(self._eventfd)
		if len(n) != 1:
			Logging.error('EventLoop::handle_read read n bytes')

	def do_pending(self):
		self._calling_pending = True
		self._mutex.acquire()
		functors = self._pending_func
		self._mutex.release()

		for [func, kargs] in functors:
			if kargs != {}:
				func(kargs)
			else:
				func()
		self._calling_pending = False





