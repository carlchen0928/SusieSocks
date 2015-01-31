import Poller
import select
import Channel
import Logging
import errno

'''
default poll() system call
'''


class KQueuePoller(Poller.Poller):

	MAX_EVENTS = 1024

	def __init__(self):
		Poller.Poller.__init__(self)
		self._poller = select.kqueue()

	def __control(self, fd, mode, flag):
		events = []
		if mode & Poller.POLL_IN:
			events.append(select.kevent(fd, select.KQ_FILTER_READ, flag))

		if mode & Poller.POLL_OUT:
			events.append(select.kevent(fd, select.KQ_FILTER_WRITE, flag))

		for e in events:
			self._poller.control([e], 0)
		pass

	def update_channel(self, channel):
		assert isinstance(channel, Channel.Channel)
		if channel.is_none_event():
			Logging.warning('update_channel listen event is none, skip.')
			return

		self._channelMap[channel.fd()] = channel
		self.__control(channel.fd(), channel.event(), select.KQ_EV_ADD)

	def remove_channel(self, channel):
		assert isinstance(channel, Channel.Channel)
		assert channel.fd() in self._channelMap

		del self._channelMap[channel.fd()]
		self.__control(channel.fd(), channel.event(), select.KQ_EV_DELETE)

	def poll(self, timeout_ms=None):
		try:
			events = self._poller.control(None, KQueuePoller.MAX_EVENTS, timeout_ms)
		except (OSError, IOError) as e:
			if error_from_exception(e) in (errno.EINTR, errno.EPIPE):
				Logging.error('poll error: %s' % e)
			else:
				import traceback
				Logging.error('poll error: %s' % e)
				traceback.print_exc()
				return None

		active_channels = []

		if len(events) == 0:
			Logging.debug('poll time out, limit is %d' % timeout_ms)
		elif len(events) > 0:
			for e in events:
				fd = e.ident
				flag = Poller.POLL_NULL
				if e.filter & select.KQ_FILTER_READ:
					flag |= Poller.POLL_IN
				elif e.filter & select.KQ_FILTER_WRITE:
					flag |= Poller.POLL_OUT

				self.fill_active_channels(fd, flag, active_channels)

		return active_channels

	def fill_active_channels(self, fd, flag, active_channels):
		assert fd in self._channelMap
		channel = self._channelMap[fd]
		assert channel.fd() == fd
		channel.set_revent(flag)
		active_channels.append(channel)


def error_from_exception(e):
	if hasattr(e, 'errno'):
		return e.errno
	elif e.args:
		return e.args[0]
	else:
		return None