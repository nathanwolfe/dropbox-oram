import Oram
import DBFileSys

class UserFileSys:
    def __init__(self, treeSize, z, segSize, maxStashSize, growR, targetR, shrinkR):
        self._Oram = Oram.Oram(treeSize, z, segSize, maxStashSize, growR, targetR, shrinkR)
        self._segSizeMap = {}          # holds number of segments in file
        self._segIDMap = {}         # holds segIDs of the file segments
        self._segSize = segSize
        self._curSegID = 1

        self.debug = False

    def write(self, userFileName):
        readFile = open(userFileName, "rb")
        segNum = 0
        while True:
            dataSeg = readFile.read(self._segSize)
            if not dataSeg:
                break            # break the loop once end of file is reached

            if self.debug:
                print ("segName: " + str(userFileName + "_" + str(segNum)))
            self._segIDMap[userFileName + "_" + str(segNum)] = self._curSegID
            self._Oram.write(self._segIDMap[userFileName + "_" + str(segNum)], dataSeg)
            self._curSegID += 1
            segNum += 1

        self._segSizeMap[userFileName] = segNum
        readFile.close()

    def read(self, userFileName):
        if userFileName in self._segSizeMap:
            numSegments = self._segSizeMap[userFileName]
            result = b""
            for segNum in range(numSegments):
                if self.debug:
                    print ("READING FILE " + str(self._segIDMap[userFileName + "_" + str(segNum)]))
                    print (self._Oram.read(self._segIDMap[userFileName + "_" + str(segNum)]))
                result += self._Oram.read(self._segIDMap[userFileName + "_" + str(segNum)])
            return result

        else:
            print ("Reading nonexistent file...")

    def delete(self, userFileName):
        if userFileName in self._segSizeMap:
            numSegments = self._segSizeMap[userFileName]
            for segNum in range(numSegments):
                self._Oram.delete(self._segIDMap[userFileName + "_" + str(segNum)])
                del self._segIDMap[userFileName + "_" + str(segNum)]
        
            del self._segSizeMap[userFileName]

        else:
            print ("Deleting nonexistent file...")

    def writeEverything(self):
        DBFileSys.writeStash(self._Oram.getStash().getNodes(), self._segSize)     # I shouldn't access private member variables right?
        DBFileSys.writeDictionary("posMap", self._Oram.getPosMap().getMap())
        DBFileSys.writeDictionary("segSizeMap", self._segSizeMap)
        DBFileSys.writeDictionary("segIDMap", self._segIDMap)

    def readEverything(self):
        self._Oram.setStash(DBFileSys.readStash(self._segSize))
        self._Oram.setPosMap(DBFileSys.readDictionary("posMap"))
        self._segSizeMap = DBFileSys.readDictionary("segSizeMap")
        self._segIDMap = DBFileSys.readDictionary("segIDMap")

test = UserFileSys(101, 3, 3000, 10, 1.8, 2.0, 2.2)
test.write("Birds.jpg")
test.writeEverything()
test.readEverything()
#print("checkpoint1")
pic = test.read("Birds.jpg")
#print ("checkpoint")
output = open("file.jpg", "wb")
output.write(pic)
output.close()
