import socket
import logging
from core.cipher import Cipher, MD5InconformityError
from Crypto.Hash import MD5

BUFFER_SIZE = 1024

class MySocket:
    def __init__(self, key):
        self.cipher = Cipher(key)

    def set_loop(self, loop):
        self.loop = loop

    async def recv(self, src: socket.socket, buf_size: int):
        data = await self.loop.sock_recv(src, buf_size)
        # print("recv {}".format(data))
        return data

    async def send(self, dst: socket.socket, data: bytearray):
        # print("send {}".format(data))
        await self.loop.sock_sendall(dst, data)
        # print("end!")

    async def encodeOne(self, dst: socket.socket, data: bytearray):
        # print("[Encoder-One] . -> {}:{} {}".format(*dst.getsockname(), data)) 
        data = bytes(self.cipher.encode(bytearray(data)))
        await self.send(dst, data)

    async def encodeCopy(self, src: socket.socket, dst: socket.socket):
        while (True):
            data = await self.recv(src, BUFFER_SIZE - 16)
            if not data:
                # print("No more data")
                break
            # print("[Encoder] {}:{} -> {}:{} {}".format(*src.getsockname(), *dst.getsockname(), data))
            h = MD5.new()
            h.update(data)
            print(h.hexdigest())
            data = bytes(self.cipher.encode(bytearray(data)))
            h = MD5.new()
            h.update(data)
            print(h.hexdigest())
            await self.send(dst, data)

    async def decodeOne(self, src: socket.socket):
        data = await self.recv(src, BUFFER_SIZE)
        h = MD5.new()
        h.update(data)
        print(h.hexdigest())
        data = bytes(self.cipher.decode(bytearray(data)))
        h = MD5.new()
        h.update(data)
        print(h.hexdigest())
        # print("[Decoder-One] {}:{} -> . {}" .format(*src.getsockname(), data))
        return data

    async def decodeCopy(self, src: socket.socket, dst: socket.socket):
        while (True):
            data = await self.recv(src, BUFFER_SIZE)
            if not data:
                break
            h = MD5.new()
            h.update(data)
            print(h.hexdigest())
            data = bytes(self.cipher.decode(bytearray(data)))
            h = MD5.new()
            h.update(data)
            print(h.hexdigest())
            # print("[Decoder] {}:{} -> {}:{} {}".format(*src.getsockname(), *dst.getsockname(), data))
            await self.send(dst, data)