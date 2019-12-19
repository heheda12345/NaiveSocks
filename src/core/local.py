import utils.config as lsConfig
from utils.utils import NetAddr
from core.mysocket import MySocket
import asyncio
import socket
import logging

class LocalServer(MySocket):
    def __init__(self, password, localAddr: NetAddr, remoteAddr: NetAddr):
        super().__init__(password)
        self.localAddr = localAddr
        self.remoteAddr = remoteAddr

    def start(self):
        self.set_loop(asyncio.get_event_loop())
        asyncio.ensure_future(self.listen(self.loop))
        self.loop.run_forever()
    
    async def listen(self, loop):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((self.localAddr.Addr, self.localAddr.Port))
            listener.listen(socket.SOMAXCONN)
            listener.setblocking(False)
            print("Listening to {} port {}...".format(self.localAddr.Addr, self.localAddr.Port))
            while True:
                con, addr = await self.loop.sock_accept(listener)
                print('Receive (%s:%d)', *addr)
                asyncio.ensure_future(self.handle(con))
        loop.stop()

    async def handle(self, con: socket.socket):
        remote = await self.connectToRemote()
        def cleanup(task):
            print("closeed!")
            con.close()
        asyncio.ensure_future(self.encode(con, remote)).add_done_callback(cleanup)

    async def connectToRemote(self):
        try:
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.setblocking(False)
            await self.loop.sock_connect(remote, self.remoteAddr)
        except Exception as err:
            raise ConnectionError("Can not connnect to {} port {}: {}".format(self.remoteAddr.Addr, self.remoteAddr.Port, err))
        return remote

