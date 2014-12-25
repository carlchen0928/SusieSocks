import socket
import Poller
import Channel


class EventLoop:
	def __init__(self):
		self._looping = False
		self._quit = False
		self._poller = Poller()
		self._activeChannels = []
		self._currentChannel = None
		pass

	def loop(self):
		pass

	def quit(self):
		self._quit = True
		pass

	def update_channel(self, channel):
		pass

	def remove_channel(self, channel):
		pass

	def has_channel(self, channel):
		pass

