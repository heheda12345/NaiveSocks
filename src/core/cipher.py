
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
        # self.key = bytes(key[:16])
        # self.IV = bytes(key[-16:])
        # self.mode = AES.MODE_CBC
        self.S = bytearray(range(256))
        for idx in key:
            self.S = self.S[idx:idx+1] + self.S[:idx] + self.S[idx+1:]
        
        self.T = bytearray(range(256))
        for i in range(256):
            self.T[self.S[i]] = i
        
    def encode(self, bs: bytearray):
        # try:
        #     cryptor = AES.new(bytes(self.key), self.mode, self.IV)
            # ciphertext = cryptor.encrypt(bs)
            # self.ciphertext = cryptor.encrypt(pad(text))
            # md5 = MD5.new()
            # md5.update(bs)
            # bs[0] ^= 1
            # print(type(bs))
            # print(bs[0])
            # print(bs[0])
        for i, v in enumerate(bs):
            bs[i] = self.S[v]
            # AES()
            # return self.cryptor.encrypt(bs)
        #     padding = 16 - len(bs) % 16
        #     for _ in range(padding):
        #         bs.append(padding)
        #     pass
        # except Exception as e:
        #     print(e)
        # return cryptor.encrypt(bytes(bs))
        # try:
        #     bs = b'a' * 16 + bs
        # except Exception as e:
        #     print(e)
        return bs

    def decode(self, bs: bytearray):
        # cryptor = AES.new(bytes(self.key), self.mode, self.IV)
        # md5 = MD5.new()
        # md5.update(bs[16:])
        # for i, v in enumerate(md5.digest()):
        #     if bs[i] != v:
        #         raise MD5InconformityError
        # print(type(bs))

        # print(bs[0:])
        # print(type(bs[0:]))
        # for i, v in enumerate(bs):
        #     bs[i] = v ^ 1
        # print(bs[0])
        # print(bs[0])
        # return self.cryptor.decrypt(bs)
        # print(len(bs))
        # print(type(self.cryptor.decrypt(bytes(bs))))
        # print(len(self.cryptor.decrypt(bytes(bs))))
        # bs = bytearray(cryptor.decrypt(bytes(bs)))
        # padding = bs[-1]
        # if padding < 1 or padding > 16:
        #     raise Exception
        # for _ in range(padding):
        #     if bs.pop() != padding:
        #         raise Exception
        
        for i, v in enumerate(bs):
            bs[i] = self.T[v]
        return bs

    # @classmethod
    # def NewCipher(cls, encodePassword: bytearray):
    #     decodePassword = encodePassword.copy()
    #     for i, v in enumerate(encodePassword):
    #         decodePassword[v] = i
    #     return cls(encodePassword, decodePassword)
