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
		while not self._quit:
			self._activeChannels = []
			try:
				self._activeChannels = self._poller.poll()
			except:
				pass
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

