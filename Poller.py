import Channel

POLL_NULL = 0x00
POLL_IN = 0x01
POLL_OUT = 0x04
POLL_ERR = 0x08
POLL_HUP = 0x10
POLL_NVAL = 0x20


class Poller:
	def __init__(self):
		self._channelMap = {}

	def has_channel(self, channel):
		return channel.fd() in self._channelMap