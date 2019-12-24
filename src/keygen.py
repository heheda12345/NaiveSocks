
from core.password import randomPassword, dumpPassword
# import binascii
# from Crypto.Hash import MD5

with open('key.pem', 'wb') as f:
    f.write(dumpPassword(randomPassword()))

# h = MD5.new()
# h.update(a)
# print(h.hexdigest())
