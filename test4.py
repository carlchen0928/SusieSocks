__author__ = 'yiyuchen'

import socket,select

s = socket.socket()
s.bind(("127.0.0.1", 8222))
s.listen(5)

kq = select.kqueue()
events = [select.kevent(s.fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD)]
kq.control(events, 0)
connmap = {}

while True:
	eventlist = kq.control(events, 5)
	if eventlist:
		for e in eventlist:
			if e.ident == s.fileno() and e.filter == select.KQ_FILTER_READ:
				(conn, addr) = s.accept()
				connmap[conn.fileno()] = conn
				kq.control([select.kevent(conn.fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD)], 0)
			elif e.filter == select.KQ_FILTER_READ:
				conn = connmap[e.ident]
				data = conn.recv(1024)
				print data
