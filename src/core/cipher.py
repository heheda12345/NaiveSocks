
from Crypto.Cipher import AES

class MD5InconformityError(Exception):
    """MD5值不一致"""

class Cipher:
    """
        Cipher class is for the encipherment of data flow.
        One octet is in the range 0 ~ 255 (2 ^ 8).
        To do encryption, it just maps one byte to another one.
        Example:
            encodePassword
            | index | 0x00 | 0x01 | 0x02 | 0x03 | ... | 0xff | || 0x02ff0a04
            | ----- | ---- | ---- | ---- | ---- | --- | ---- | ||
            | value | 0x01 | 0x02 | 0x03 | 0x04 | ... | 0x00 | \/ 0x03000b05
            decodePassword
            | index | 0x00 | 0x01 | 0x02 | 0x03 | 0x04 | ... | || 0x03000b05
            | ----- | ---- | ---- | ---- | ---- | ---- | --- | ||
            | value | 0xff | 0x00 | 0x01 | 0x02 | 0x03 | ... | \/ 0x02ff0a04
        It just shifts one step to make a simply encryption, encode and decode.
    """

    # def __init__(self, encodePassword: bytearray,
    #              decodePassword: bytearray) -> None:
    #     self.encodePassword = encodePassword.copy()
    #     self.decodePassword = decodePassword.copy()

    def __init__(self, key):
        self.key = bytes(key[:16])
        self.IV = bytes(key[-16:])
        self.mode = AES.MODE_CBC
        
    def encode(self, bs: bytearray):
        cryptor = AES.new(bytes(self.key), self.mode, self.IV)
        padding = 16 - len(bs) % 16
        for _ in range(padding):
            bs.append(padding)
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
        return bs

    # @classmethod
    # def NewCipher(cls, encodePassword: bytearray):
    #     decodePassword = encodePassword.copy()
    #     for i, v in enumerate(encodePassword):
    #         decodePassword[v] = i
    #     return cls(encodePassword, decodePassword)
