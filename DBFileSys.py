import Block

def readBucket(bucketID, maxDataLength):
    inputFile = open("blocks/" + str(bucketID), "rb")         # rb = read binary
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
    return result

def writeBucket(bucketID, blocks, maxDataLength):
    outputFile = open("blocks/" + str(bucketID), "wb")        # wb = write binary
    for block in blocks:
        outputFile.write(block.getLeaf().to_bytes(4, byteorder = "little"))
        outputFile.write(block.getSegID().to_bytes(4, byteorder = "little"))

        dataLength = len(block.getData())
        outputFile.write(dataLength.to_bytes(4, byteorder = "little"))
        outputFile.write(block.getData())
        outputFile.write(bytes(maxDataLength - dataLength))   # fill up empty space
