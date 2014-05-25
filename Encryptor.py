from Crypto.Cipher import AES
import base64
import os

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

def mask(key, maskNum):
    maskBytes = maskNum.to_bytes(16, byteorder="big")
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(maskBytes)

def read(path, key, maskNum):
    inputFile = open(path, "rb")
    data = inputFile.read()
    inputFile.close()
    result = b""
    maskBytes = mask(key, maskNum)
    while data != b"":
        currentSeg = data[:16]
        data = data[16:]
        currentMask = maskBytes[:len(currentSeg)]
        result += (int.from_bytes(currentSeg, byteorder="big") ^ int.from_bytes(currentMask, byteorder="big")).to_bytes(len(currentSeg), byteorder="big")
    return result

def write(path, data, key, maskNum):
    dirs = path[:(path.rfind("/"))]
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    result = b""
    maskBytes = mask(key, maskNum)
    while data != b"":
        currentSeg = data[:16]
        data = data[16:]
        currentMask = maskBytes[:len(currentSeg)]
        result += (int.from_bytes(currentSeg, byteorder="big") ^ int.from_bytes(currentMask, byteorder="big")).to_bytes(len(currentSeg), byteorder="big")
    outputFile = open(path, "wb")
    outputFile.write(result)
    outputFile.close()
