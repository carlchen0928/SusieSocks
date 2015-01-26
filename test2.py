import EchoServer
import EventLoop


loop = EventLoop.EventLoop()
es = EchoServer.EchoServer(loop, ('0.0.0.0', 9999))
es.start()
loop.loop()