import Poller
import select
import Channel


class DefaultPoller(Poller):
	def __init__(self):
		self._poller = select.poll()

	def update_channel(self, channel):
		assert isinstance(channel, Channel)

		self._poller.register(channel.fd(), channel.event())