import select
import socket
import threading
import time

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

class myThread(threading.Thread):
	def run(self):
		time.sleep(1)
		print self.ident
		print 'haha'

t = myThread()
t.start()
print threading.current_thread().ident
t.join()