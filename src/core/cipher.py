
from Crypto.Cipher import AES
from Crypto.Hash import MD5

class MD5InconformityError(Exception):
    """MD5值不一致"""

class Cipher:

    def __init__(self, key):
        self.key = bytes(key[:16])
        self.IV = bytes(key[-16:])
        self.mode = AES.MODE_CBC
        
    def encode(self, bs: bytearray):
        md5 = MD5.new()
        md5.update(bs)
        bs = bs + md5.digest()

        padding = 16 - len(bs) % 16
        for _ in range(padding):
            bs.append(padding)
        
        cryptor = AES.new(bytes(self.key), self.mode, self.IV)
        return cryptor.encrypt(bytes(bs))

    def decode(self, bs: bytearray):
        cryptor = AES.new(bytes(self.key), self.mode, self.IV)
        bs = bytearray(cryptor.decrypt(bytes(bs)))

        padding = bs[-1]
        if padding < 1 or padding > 16:
            raise Exception
        for _ in range(padding):
            if bs.pop() != padding:
                raise Exception
        
        md5 = MD5.new()
        md5.update(bs[:-16])
        if bs[-16:] != md5.digest():
            raise MD5InconformityError
        return bs[:-16]