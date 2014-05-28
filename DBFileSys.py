import os
import Block

from os.path import expanduser
home = expanduser("~")
#print (home)

bucketLoc = "/Dropbox/buckets/"
useSync = True
if useSync == False:
    bucketLoc = "/Documents/buckets/"

def readBucket(bucketID, maxDataLength):
    if not os.path.exists(home + bucketLoc):
        os.makedirs(home + bucketLoc)
    inputFile = open(home + bucketLoc + str(bucketID), "rb")         # rb = read binary
    result = []
    while True:
        leafBytes = inputFile.read(4)
        if leafBytes == b"":
            break                                             # break if end of file
        segIDBytes = inputFile.read(4)
        dataLength = int.from_bytes(inputFile.read(4), byteorder = "little")
        data = inputFile.read(dataLength)
        inputFile.read(maxDataLength - dataLength)
        result.append(Block.Block(int.from_bytes(leafBytes, byteorder = "little"), int.from_bytes(segIDBytes, byteorder = "little"), data))

    inputFile.close()
    return result

def writeBucket(bucketID, blocks, maxDataLength):
    if not os.path.exists(home + bucketLoc):
        os.makedirs(home + bucketLoc)
    outputFile = open(home + bucketLoc + str(bucketID), "wb")        # wb = write binary
    for block in blocks:
        writeBlock(outputFile, block, maxDataLength)
        
    outputFile.close()

def writeStash(stash, maxDataLength):      # stash is a list of nodes in the stash
    outputFile = open(home + "/Dropbox/stash", "wb")
    for block in stash:
        writeBlock(outputFile, block, maxDataLength)

    outputFile.close()

def readStash(maxDataLength):         # returns a list where each element is a block in the stash
    if not os.path.exists(home + "/Dropbox/stash"):
        return "new ORAM"
    inputFile = open(home + "/Dropbox/stash", "rb")
    result = []
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

def writeBlock(outputFile, block, maxDataLength):
    outputFile.write(block.getLeaf().to_bytes(4, byteorder = "little"))
    outputFile.write(block.getSegID().to_bytes(4, byteorder = "little"))

    dataLength = len(block.getData())
    outputFile.write(dataLength.to_bytes(4, byteorder = "little"))
    outputFile.write(block.getData())
    outputFile.write(bytes(maxDataLength - dataLength))   # fill up empty space
