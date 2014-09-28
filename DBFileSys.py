import os
import pickle as pickle
import Block
import Encryptor

from os.path import expanduser
home = expanduser("~")
#print (home)

bucketLoc = "/Dropbox/buckets/"
useSync = True
if useSync == False:
    bucketLoc = "/Documents/buckets/"
bucketLoc = "./buckets/"
	
encrypt = True
key = "16characterslong"

def readBucket(bucketID, maxDataLength):
    if not os.path.exists(home + bucketLoc):
        os.makedirs(home + bucketLoc)

    inputFile = open(home + bucketLoc + str(bucketID), "rb")         # rb = read binary
    #bytesIn = inputFile.read()
    bytesIn = pickle.load(inputFile)		
    inputFile.close()
    if encrypt:
        bytesIn = Encryptor.decrypt(bytesIn, key)

    result = []
    while True:
        leafBytes = bytesIn[:4]
        bytesIn = bytesIn[4:]
        if leafBytes == b"":
            break                                             # break if end of file
        segIDBytes = bytesIn[:4]
        bytesIn = bytesIn[4:]
        dataLength = int.from_bytes(bytesIn[:4], byteorder = "little")
        bytesIn = bytesIn[4:]
        data = bytesIn[:dataLength]
        bytesIn = bytesIn[maxDataLength:]
        result.append(Block.Block(int.from_bytes(leafBytes, byteorder = "little"), int.from_bytes(segIDBytes, byteorder = "little"), data))
    
    return result

def writeBucket(bucketID, blocks, maxDataLength):
    if not os.path.exists(home + bucketLoc):
        os.makedirs(home + bucketLoc)
    result = b""
    for block in blocks:
        result += writeBlock(block, maxDataLength)
    
    if encrypt:
        result = Encryptor.encrypt(result, key)
    		
    outputFile = open(home + bucketLoc + str(bucketID), "wb")        # wb = write binary
    #outputFile.write(result)
    pickle.dump(result, outputFile)	
    outputFile.close()

def writeStash(stash, maxDataLength):      # stash is a list of nodes in the stash
    if not os.path.exists(home + "/Dropbox/stash"):
        os.makedirs(home + "/Dropbox/stash")

    result = b""
    for block in stash:
        result += writeBlock(block, maxDataLength)

    outputFile = open(home + "/Dropbox/stash", "wb")
    outputFile.write(result)
    outputFile.close()

def readStash(maxDataLength):         # returns a list where each element is a block in the stash
    if not os.path.exists(home + "/Dropbox/stash"):
        return "new ORAM"
    inputFile = open(home + "/Dropbox/stash", "rb")
    result = []
    
    # Same problem as in readBucket(). Try to read it less times.    
    while True:
        #print ("loop")
        leafBytes = inputFile.read(4)
        if leafBytes == b"":
            #print ("true")
            break                                             # break if end of file
        segIDBytes = inputFile.read(4)
        dataLength = int.from_bytes(inputFile.read(4), byteorder = "little")
        data = inputFile.read(dataLength)
        #print ("loop")
        inputFile.read(maxDataLength - dataLength)
        result.append(Block.Block(int.from_bytes(leafBytes, byteorder = "little"), int.from_bytes(segIDBytes, byteorder = "little"), data))

    inputFile.close()
    return result

def writeDictionary(fileName, dictionary):
    outputFile = open(home+ "/Dropbox/" + fileName, "wb")
    for i in range(len(dictionary)):
        key, value = dictionary.popitem()
        if fileName == "posMap":
            outputFile.write(key.to_bytes(4, byteorder = "little"))
        elif fileName == "segSizeMap" or fileName == "segIDMap":     # writing strings as a key instead
            keyLength = len(key)
            outputFile.write(keyLength.to_bytes(4, byteorder = "little"))
            outputFile.write(key.encode("utf-8"))

        outputFile.write(value.to_bytes(4, byteorder = "little"))

    outputFile.close()

def readDictionary(fileName):
    inputFile = open(home + "/Dropbox/" + fileName, "rb")
    result = {}
    while True:
        if fileName == "posMap":
            key = int.from_bytes(inputFile.read(4), byteorder = "little")
        elif fileName == "segSizeMap" or fileName == "segIDMap":
            keyLength = int.from_bytes(inputFile.read(4), byteorder = "little")
            key = inputFile.read(keyLength).decode("utf-8")
        if key == "" or key == 0:           # if end of file break
            break
        value = int.from_bytes(inputFile.read(4), byteorder = "little")
        result[key] = value
        #print (key, value)

    inputFile.close()
    return result

def writeBlock(block, maxDataLength):
    result = b""
    result += block.getLeaf().to_bytes(4, byteorder = "little")
    result += block.getSegID().to_bytes(4, byteorder = "little")

    dataLength = len(block.getData())
    result += dataLength.to_bytes(4, byteorder = "little")
    result += block.getData()
    result += bytes(maxDataLength - dataLength)   # fill up empty space
    return result
