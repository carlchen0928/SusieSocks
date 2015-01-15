import select
import socket
import threading
import time
import KQueuePoller
import Poller

#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setblocking(False)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server_address = ("127.0.0.1", 10001)
#
# server.bind(server_address)
#
# server.listen(10)
# READ_ONLY = (select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR)
# READ_WRITE = (READ_ONLY | select.POLLOUT)
# poller = select.poll()
# poller.register(server, READ_ONLY)
#
# fd_to_sock = {server.fileno() : server}
#
# while True:
# 	events = poller.poll()
# 	print events
# 	for fd, flag in events:
# 		if flag & (select.POLLIN | select.POLLPRI):
# 			print 'read'
# 		else:
# 			print 'error'
#
# poll = KQueuePoller.KQueuePoller()
# fdc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('0.0.0.0', 10001)
# fdc.setblocking(False)
# fdc.bind(server_address)
# fd = fdc.fileno()
# fdc.listen(5)
# poll.poll()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 0))
s.listen(5)
print s.getsockname()

(conn, addr) = s.accept()
while True:
	n = conn.recv(10)
	if n == '':
		break
	print n, len(n)

print 'end'

