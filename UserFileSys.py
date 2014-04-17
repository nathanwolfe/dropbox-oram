import Oram

class UserFileSys:
    def __init__(self, treeSize, z, segSize, maxStashSize):
        self._Oram = Oram.Oram(treeSize, z, segSize, maxStashSize)
        self._segSizeMap = {}          # holds number of segments in file
        self._segIDMap = {}         # holds segIDs of the file segments
        self._segSize = segSize
        self._curSegID = 0

    def write(self, userFileName):
        readFile = open(userFileName, "rb")
        segNum = 0
        while True:
            dataSeg = readFile.read(self._segSize)
            if not dataSeg:
                break            # break the loop once end of file is reached
            self._segIDMap[userFileName + "_" + str(segNum)] = self._curSegID
            self._Oram.write(self._segIDMap[userFileName + "_" + str(segNum)], dataSeg)
            self._curSegID += 1
            segNum += 1

        self._segSizeMap[userFileName] = segNum
        readFile.close()

    def read(self, userFileName):
        numSegments = self._segSizeMap[userFileName]
        result = b""
        for segNum in range(numSegments):
            print("testing")
            result += self._Oram.read(self._segIDMap[userFileName + "_" + str(segNum)])

        return result

    def delete(self, userFileName):
        numSegments = self._segSizeMap[userFileName]
        for segNum in range(numSegments):
            self._Oram.delete(self._segIDMap[userFileName + "_" + str(segNum)])

        del self._segSizeMap[userFileName]

test = UserFileSys(100, 3, 3000, 10)
test.write("Birds.jpg")
pic = test.read("Birds.jpg")
output = open("file.jpg", "wb")
output.write(pic)
output.close()
