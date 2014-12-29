import Poller
import select
import Channel
import Logging

'''
default poll() system call
'''


class DefaultPoller(Poller):
	def __init__(self):
		self._poller = select.poll()

	def update_channel(self, channel):
		assert isinstance(channel, Channel)
		if channel.is_none_event():
			Logging.warning('update_channel listen event is none, skip.')
			return

		self._poller.register(channel.fd(), channel.event())

	def remove_channel(self, channel):
		assert isinstance(channel, Channel)
		assert channel in self._channelMap

		self._poller.unregister(channel.fd())

	def poll(self, timeout_ms=None):
		events = self._poller.poll(timeout_ms)
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