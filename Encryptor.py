from Crypto.Cipher import AES
from random import randint
import base64
import os

def mask(key, maskNum):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(maskNum)

def read(path, key):
    inputFile = open(path, "rb")
    maskNum = inputFile.read(16)
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

def write(path, data, key):
    dirs = path[:(path.rfind("/"))]
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    maskNum = randint(0, 1 << 128).to_bytes(16, byteorder="big")
    result = maskNum
    maskBytes = mask(key, maskNum)
    while data != b"":
        currentSeg = data[:16]
        data = data[16:]
        currentMask = maskBytes[:len(currentSeg)]
        result += (int.from_bytes(currentSeg, byteorder="big") ^ int.from_bytes(currentMask, byteorder="big")).to_bytes(len(currentSeg), byteorder="big")
    outputFile = open(path, "wb")
    outputFile.write(result)
    outputFile.close()
