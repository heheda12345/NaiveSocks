import utils.config as lsConfig
from utils.utils import NetAddr
from core.mysocket import MySocket
import asyncio
import socket

class RemoteServer(MySocket):
    def __init__(self, key, addr: NetAddr):
        super().__init__(key)
        self.addr = addr

    def start(self):
        self.set_loop(asyncio.get_event_loop())
        asyncio.ensure_future(self.listen(self.loop))
        self.loop.run_forever()
    
    async def listen(self, loop):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(self.addr)
            listener.listen(socket.SOMAXCONN)
            listener.setblocking(False)
            print("Listening to {} port {}...".format(self.addr.Addr, self.addr.Port))
            while True:
                con, addr = await self.loop.sock_accept(listener)
                print('Connect to {}:{} Succ!'.format(*addr))
                asyncio.ensure_future(self.handle(con))
        loop.stop()

    async def handle(self, con: socket.socket):
        buf = await self.decodeOne(con)
        print(buf)
        if not buf or buf[0] != 0x5:
            con.close()
            return
        await self.encodeOne(con, bytearray((0x05, 0x00)))
        buf = await self.decodeOne(con)
        print(buf, len(buf))
        if len(buf) < 7 or buf[0] != 0x5 or buf[1] != 0x1:
            con.close()
            return

        webPort = int(buf[-2:].hex(), 16)
        webFamily = None
        webSocket = None
        if buf[3] == 0x1: # ipv4
            webIP = socket.inet_ntop(socket.AF_INET, buf[4: 8])
            webFamily = socket.AF_INET
        elif buf[3] == 0x3: # domain name
            webIP = buf[5:-2].decode()
        elif buf[3] == 0x4: # ipv6
            webIP = socket.inet_ntop(socket.AF_INET6, buf[4: 4 + 16])
            webFamily = socket.AF_INET6
        webAddress = NetAddr(Addr = webIP, Port = webPort)
        
        if webFamily is not None:
            try:
                webSocket = socket.socket(family=webFamily, type=socket.SOCK_STREAM)
                webSocket.setblocking(False)
                await self.loop.sock_connect(webSocket, webAddress)
            except OSError:
                if webSocket is not None:
                    webSocket.close()
                    webSocket = None
        else:
            for res in await self.loop.getaddrinfo(webIP, webPort):
                webFamily, socktype, proto, _, webAddress = res
                print("domain {}: {}".format(webIP, webAddress))
                try:
                    webSocket = socket.socket(webFamily, socktype, proto)
                    webSocket.setblocking(False)
                    await self.loop.sock_connect(webSocket, webAddress)
                    break
                except OSError:
                    if webSocket is not None:
                        webSocket.close()
                        webSocket = None
        
        if webSocket is None:
            return
        await self.encodeOne(con, 
                             bytearray((0x05, 0x00, 0x00, 0x01, buf[3], 0x00, 0x00, 0x00, 0x00, 0x00)))
        def cleanUp(task):
            print("closeed!")
            con.close()
        asyncio.ensure_future(
            asyncio.gather(
                asyncio.ensure_future(self.decodeCopy(con, webSocket)),
                asyncio.ensure_future(self.encodeCopy(webSocket, con)),
                loop=self.loop,
                return_exceptions=True)).add_done_callback(cleanUp)
        
