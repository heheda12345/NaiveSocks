import socket
import logging
from core.cipher import Cipher

BUFFER_SIZE = 1024

class MySocket:
    def __init__(self, password):
        self.cipher = Cipher(password)

    def set_loop(self, loop):
        self.loop = loop

    async def recv(self, src: socket.socket):
        data = await self.loop.sock_recv(src, BUFFER_SIZE)
        print("recv {}".format(data))
        return data

    async def send(self, dst: socket.socket, data: bytearray):
        print("send {}".format(data))
        await self.loop.sock_sendall(dst, data)
        print("end!")


    async def encode(self, src: socket.socket, dst: socket.socket):
        while (True):
            data = await self.recv(src)
            if not data:
                break
            print("[Encoder] %s:%d %s", *src.getsockname(), data)
            self.cipher.encode(data)
            await self.send(dst, data)

    async def decodeOne(self, src: socket.socket):
        data = await self.recv(src)
        self.cipher.decode(data)
        return data

    async def decode(self, src: socket.socket):
        while (True):
            data = await self.recv(src)
            if not data:
                break
            self.cipher.decode(data)
            print("[Decoder] %s:%d %s", *src.getsockname(), data)
            # await self.send(dst, data)