import Oram

class UserFileSys:
    def __init__(self, treeSize, z, segSize, maxStashSize):
        self._Oram = Oram.Oram(treeSize, z, segmentSize, maxStashSize)
        self._directory = {}          # directory holds number of segments in file
        self._segSize = segSize

    def write(self, userFileName):
        readFile = open(userFileName, "rb")
        segNum = 0
        while True:
            dataSeg = readFile.read(self._segSize)
            if not dataSeg:
                break            # break the loop once end of file is reached
            self._Oram.write(userFileName + "_" + str(segNum), dataSeg)
            segNum += 1

        self._directory[userFileName] = segNum + 1
        readFile.close()

    def read(self, userFileName):
        numSegments = self._directory[userFileName]
        result = b""
        for segNum in range(numSegments):
            result += self._Oram.read(userFileName + "_" + str(segNum))

        return result

    def delete(self, userFileName):
        numSegments = self._directory[userFileName]
        for segNum in range(numSegments):
            self._Oram.delete(userFileName + "_" + str(segNum))

        del self._directory[userFileName]
