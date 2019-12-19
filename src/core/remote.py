import utils.config as lsConfig
from utils.utils import NetAddr
from core.mysocket import MySocket
import asyncio
import socket
import logging

class RemoteServer(MySocket):
    def __init__(self, password, addr: NetAddr):
        super().__init__(password)
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
                print('Receive (%s:%d)', *addr)
                asyncio.ensure_future(self.handle(con))
        loop.stop()

    async def handle(self, con: socket.socket):
        buf = await self.decode(con)
        print(buf)
        if (not buf or buf[0] != 0x5):
            con.close()
            return
        
        
