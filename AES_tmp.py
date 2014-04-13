# Installation of the PyCrypto package for windows
# Download prebuilt version at http://www.voidspace.org.uk/python/modules.shtml#pycrypto

from Crypto.Cipher import AES
from random import randint

# AES (the one we use) operates on 128-bit input each time. Key also has to be 128-bit (16 bytes)
# This implementation takes bytes (or strings) as input

# secret key, convert to bytes
SK = randint(0, 1 << 128)	
SK = SK.to_bytes(16, byteorder='big')

cipher = AES.new(SK, AES.MODE_ECB)

# counter, input to AES, convert to bytes
counter = 5213		
counter = counter.to_bytes(16, byteorder='big')

mask = cipher.encrypt(counter)

print(len(counter), counter)
print(len(mask), mask)

# TODO: Now we have the mask, how do we XOR on a bunch of bytes?
# Luckily, the package also provides that. 
# Look at Crypto.Cipher.XOR at http://pythonhosted.org//pycrypto/