import EchoServer
import EventLoop


loop = EventLoop.EventLoop()
es = EchoServer.EchoServer(loop, ('0.0.0.0', 8222))
es.start()
loop.loop()