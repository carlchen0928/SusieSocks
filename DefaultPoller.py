import Poller
import select
import Channel
import Logging
import errno

'''
default poll() system call
'''


def error_from_exception(e):
	if hasattr(e, 'errno'):
		return e.errno
	elif e.args:
		return e.args[0]
	else:
		return None


class DefaultPoller(Poller):
	def __init__(self):
		self._poller = select.poll()

	def update_channel(self, channel):
		assert isinstance(channel, Channel)
		if channel.is_none_event():
			Logging.warning('update_channel listen event is none, skip.')
			return

		self._channelMap[channel.fd()] = channel
		self._poller.register(channel.fd(), channel.event())

	def remove_channel(self, channel):
		assert isinstance(channel, Channel)
		assert channel.fd() in self._channelMap

		del self._channelMap[channel.fd()]
		self._poller.unregister(channel.fd())

	def poll(self, timeout_ms=None):
		try:
			events = self._poller.poll(timeout_ms)
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
			for fd, flag in events:
				self.fill_active_channels(fd, flag, active_channels)

		return active_channels

	def fill_active_channels(self, fd, flag, active_channels):
		assert fd in self._channelMap
		channel = self._channelMap[fd]
		assert channel.fd() == fd
		channel.set_revent(flag)
		active_channels.append(channel)
