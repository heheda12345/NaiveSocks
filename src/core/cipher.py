
from Crypto.Hash import MD5

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

    def __init__(self, password):
        self.password = password
        
    def encode(self, bs: bytearray):
        # md5 = MD5.new()
        # md5.update(bs)
        # bs = md5.digest() + bs
        # bs = b'a' + bs
        # bs[0] ^= 1

        print(bs[0])
        bs[0] = bs[0]
        print(bs[0])
        # for i, v in enumerate(bs):
        #     bs[i] = v
        return

    def decode(self, bs: bytearray):
        # md5 = MD5.new()
        # md5.update(bs[16:])
        # print(len(bs))
        # print(md5.hexdigest())
        # for i, v in enumerate(md5.digest()):
        #     if bs[i] != v:
        #         raise MD5InconformityError
        # bs = bs[1:]
        # bs[0] ^= 1

        # for i, v in enumerate(bs):
        #     bs[i] = v
        print(bs[0])
        bs[0] = bs[0]
        print(bs[0])
        return

    # @classmethod
    # def NewCipher(cls, encodePassword: bytearray):
    #     decodePassword = encodePassword.copy()
    #     for i, v in enumerate(encodePassword):
    #         decodePassword[v] = i
    #     return cls(encodePassword, decodePassword)
